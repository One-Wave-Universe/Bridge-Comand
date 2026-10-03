import time,unittest,json,subprocess
from unittest.mock import patch
import gateway

class Trust(unittest.TestCase):
    def claims(self):return {'iss':gateway.ISSUER,'aud':gateway.AUDIENCE,'repository':gateway.REPOSITORY,'repository_owner':'One-Wave-Universe','ref':gateway.BRANCH,'workflow_ref':gateway.WORKFLOW,'event_name':'push','exp':time.time()+60}
    def test_owner_workflow(self):gateway.validate_claims(self.claims())
    def test_other_repository(self):
        c=self.claims();c['repository']='someone/other'
        with self.assertRaises(ValueError):gateway.validate_claims(c)
    def test_other_branch(self):
        c=self.claims();c['ref']='refs/heads/main'
        with self.assertRaises(ValueError):gateway.validate_claims(c)
    def test_expired(self):
        c=self.claims();c['exp']=time.time()-1
        with self.assertRaises(ValueError):gateway.validate_claims(c)
    def test_fake_unsigned(self):
        with self.assertRaises(Exception):gateway.authenticate('fake.token.signature')
    def test_private_or_unknown_endpoint(self):
        for url in ['http://gwosc.org/api/v2/runs','https://127.0.0.1/','https://gwosc.org@localhost/','https://gwosc.org:999/api/v2/runs','https://opendata.cern.ch/record/1']:
            with self.assertRaises(ValueError):gateway.metadata_url(url)
    def test_all_registered_metadata_access(self):
        for url in ['https://gwosc.org/api/v2/catalogs','https://gwosc.org/api/v2/runs/O3a/timelines','https://opendata.cern.ch/api/records/?q=ATLAS','https://www.hepdata.net/record/1?format=json']:
            self.assertEqual(gateway.metadata_url(url),url)
    def test_signed_in_gpt_requires_complete_turn(self):
        events=[{'type':'thread.started','thread_id':'test-thread'},{'type':'item.completed','item':{'type':'agent_message','text':'actual answer'}},{'type':'turn.completed'}]
        result=subprocess.CompletedProcess([],0,'\n'.join(map(json.dumps,events)),'')
        with patch('gateway.pathlib.Path.exists',return_value=True),patch('gateway.subprocess.run',return_value=result) as run:
            out=gateway.chat({'actor':'GPT','prompt':'question','system':'reference first'})
            self.assertEqual(out['answer'],'actual answer')
            self.assertIn('read-only',run.call_args.args[0])
            self.assertIn('--ephemeral',run.call_args.args[0])
        result.stdout=json.dumps(events[1])
        with patch('gateway.pathlib.Path.exists',return_value=True),patch('gateway.subprocess.run',return_value=result):
            with self.assertRaisesRegex(ValueError,'incomplete'):gateway.chat({'actor':'GPT','prompt':'question'})
    def test_missing_grok_auth_fails_independently(self):
        with patch.dict(gateway.os.environ,{},clear=True):
            with self.assertRaisesRegex(ValueError,'not configured'):gateway.chat({'actor':'GROK','prompt':'question'})
        self.assertIsNot(gateway.ACTOR_LOCKS['GPT'],gateway.ACTOR_LOCKS['CLAUDE'])

if __name__=='__main__':unittest.main()
