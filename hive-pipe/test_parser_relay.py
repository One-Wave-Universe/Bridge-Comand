#!/usr/bin/env python3
import importlib.util,json,tempfile
from pathlib import Path
P=Path(__file__).with_name("parser_relay.py")
s=importlib.util.spec_from_file_location("parser_relay",P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def main():
 r={"id":"relay-test","argv":["uname","-a"],"intention":"test","consequence":"read only"}
 assert m.validate(r)["id"]=="relay-test"
 try:m.validate({"id":"x","argv":[],"intention":"x","consequence":"x"})
 except ValueError:pass
 else:raise AssertionError("empty argv accepted")
 with tempfile.TemporaryDirectory() as d:
  q=Path(d)/"request.json";st=Path(d)/"state.json";q.write_text(json.dumps(r))
  old=m.route_state;m.route_state=lambda:[{"route":"pull","live":False,"detail":"inactive"},{"route":"gateway","live":False,"detail":"inactive"}]
  assert m.cycle(q,st)==2
  x=json.loads(st.read_text())["requests"]["relay-test"];assert x["phase"]=="VOID" and x["failures"]==1
  m.route_state=lambda:[{"route":"gateway","live":True,"detail":"active"}]
  assert m.cycle(q,st)==0
  x=json.loads(st.read_text())["requests"]["relay-test"];assert x["phase"]=="FIELD" and x["selected_route"]=="gateway"
  m.route_state=old
 print("PARSER_RELAY_TEST_OK")
if __name__=="__main__":main()
