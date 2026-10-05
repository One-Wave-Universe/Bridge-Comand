import importlib.util,pathlib,sys,unittest
from unittest.mock import patch
HERE=pathlib.Path(__file__).parent
sys.path.insert(0,str(HERE))
def module(name):
 s=importlib.util.spec_from_file_location(name,HERE/(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=module('gemini_web_bridge');d=module('deepseek_web_bridge')
class Tests(unittest.TestCase):
 def test_gemini_packet_only_omits_tools(self):
  with patch.object(g,'post_json',return_value={'choices':[{'message':{'content':'answer'}}]}) as post:
   self.assertEqual(g.GeminiWebAgent(None,no_tools=True).run('packet',max_tool_rounds=1),'answer');self.assertEqual(post.call_args.args[1]['tools'],[])
 def test_deepseek_packet_only_omits_tools(self):
  def post(url,payload,*args):self.assertEqual(payload['tools'],[]);return {'choices':[{'message':{'content':'answer'}}]}
  self.assertEqual(d.DeepSeekWebAgent(None,web_api_key='fixture',no_tools=True,post_json=post).run('packet',max_tool_rounds=1),'answer')
 def test_packet_only_rejects_unsolicited_tools(self):
  response={'choices':[{'message':{'tool_calls':[{'id':'x','function':{'name':'terminal_run','arguments':'{}'}}]}}]}
  with patch.object(g,'post_json',return_value=response),patch.object(g,'dispatch_tool') as dispatch:
   with self.assertRaises(RuntimeError):g.GeminiWebAgent(None,no_tools=True).run('packet',max_tool_rounds=1)
   dispatch.assert_not_called()
  with patch.object(d,'dispatch_tool') as dispatch:
   with self.assertRaises(RuntimeError):d.DeepSeekWebAgent(None,web_api_key='fixture',no_tools=True,post_json=lambda *a:response).run('packet',max_tool_rounds=1)
   dispatch.assert_not_called()
 def test_default_tools_preserved(self):
  with patch.object(g,'post_json',return_value={'choices':[{'message':{'content':'answer'}}]}) as post:
   g.GeminiWebAgent(None).run('packet',max_tool_rounds=1);self.assertEqual(post.call_args.args[1]['tools'],g.DEEPSEEK_TOOLS)
if __name__=='__main__':unittest.main()
