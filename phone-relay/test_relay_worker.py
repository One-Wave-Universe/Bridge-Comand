import pathlib, tempfile
from relay_worker import handoff, receipt
r={"id":"t-1","source":"chatgpt","target":"gemini","question":"dogs?",
   "references":["repo:file"]}
h=handoff(r)
assert h["state"]=="REQUEST" and "REQUEST_ID: t-1" in h["share_text"]
x=receipt(r,"REQUEST_ID: t-1\nDogs are mammals.")
assert x["state"]=="RESPONSE" and x["ok"] and x["id"]=="t-1"
print("PHONE_RELAY_TEST_OK")
