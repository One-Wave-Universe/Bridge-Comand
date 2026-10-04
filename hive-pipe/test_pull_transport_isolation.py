import json,subprocess,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import chatgpt_terminal_pull as b

class PullIsolation(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.store=b.StateStore(Path(self.tmp.name)/"state.json")
        self.route=b.Route("primary","transport","chatgpt-terminal")
    def tearDown(self): self.tmp.cleanup()
    def request(self):
        return {"id":"proof","argv":["whoami"],"cwd":"/home/Scales/One-Wave-Science",
                "timeout":30,"intention":"identity probe","consequence":"read only"}
    def test_write_auth_failure_does_not_block_read(self):
        writer=b.TransportStateMachine([self.route],self.store,clock=lambda:10)
        reader=b.TransportStateMachine([self.route],self.store,clock=lambda:10,direction="read")
        writer.failure(self.route,"could not read Username")
        self.assertEqual(writer.ordered(),[])
        self.assertEqual(reader.ordered(),[self.route])
    def test_failed_pending_delivery_still_polls(self):
        c=b.BridgeController([self.route],self.store)
        def fail_pending(): c.transport.failure(self.route,"authentication failed")
        with patch.object(c.requests,"recover"),patch.object(c.requests,"retry_pending",side_effect=fail_pending), \
             patch.object(b,"read_request",return_value=None) as read:
            c.cycle()
            read.assert_called_once_with(self.route)
    def test_read_failure_does_not_poison_delivery(self):
        w=b.TransportStateMachine([self.route],self.store,clock=lambda:10)
        r=b.TransportStateMachine([self.route],self.store,clock=lambda:10,direction="read")
        r.failure(self.route,"fetch timeout")
        self.assertEqual(w.ordered(),[self.route])
        self.assertEqual(r.ordered(),[])
    def test_matching_connector_return_prevents_reexecution(self):
        req=b.validate_request(json.dumps(self.request()))
        returned={"id":req["id"],"request_digest":req["digest"],"completed_at":"now","exit_code":0}
        c=b.BridgeController([self.route],self.store)
        with patch.object(b,"published_result",return_value=returned),patch.object(b,"execute_request") as execute:
            self.assertFalse(c.requests.accept(self.route,"commit",json.dumps(self.request())))
            execute.assert_not_called()
            self.assertEqual(self.store.data["requests"]["proof"]["phase"],"acknowledged")
    def test_wrong_digest_result_not_accepted(self):
        req=b.validate_request(json.dumps(self.request()))
        completed=subprocess.CompletedProcess([],0,json.dumps({"id":"proof","request_digest":"wrong","completed_at":"now"}),"")
        with patch.object(b,"run_git",return_value=completed):
            self.assertIsNone(b.published_result(self.route,req))
    def test_same_id_changed_content_still_rejected(self):
        req=b.validate_request(json.dumps(self.request()))
        c=b.BridgeController([self.route],self.store)
        c.requests._set("proof",phase="acknowledged",digest="different")
        with patch.object(b,"published_result") as result,patch.object(b,"execute_request") as execute, \
             patch.object(b,"write_result"),patch.object(c.requests,"deliver",return_value=False):
            c.requests.accept(self.route,"commit",json.dumps(self.request()))
            result.assert_not_called();execute.assert_not_called()
    def test_read_failure_backoff_still_applies(self):
        r=b.TransportStateMachine([self.route],self.store,clock=lambda:10,direction="read")
        r.failure(self.route,"fetch timeout")
        self.assertEqual(r.ordered(),[])
        r.success(self.route)
        self.assertEqual(r.ordered(),[self.route])

if __name__=="__main__": unittest.main()
