#!/usr/bin/env python3
"""Repo Lens Jetson gateway: free DeepSeek relay and read-only science metadata.

Only the specified owner's Repo Lens GitHub Actions workflow can call it.
There is no shell, filesystem, repository-write or credential-export endpoint.
"""
import base64, hashlib, http.server, json, os, socket, threading, time, subprocess, pathlib, re
import urllib.request, urllib.error, urllib.parse
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

ISSUER='https://token.actions.githubusercontent.com'
AUDIENCE='repo-lens-jetson'
REPOSITORY='One-Wave-Universe/Builds'
BRANCH='refs/heads/feature/repo-lens-deepseek-jetson-20261003'
WORKFLOW=REPOSITORY+'/.github/workflows/repo-lens.yml@'+BRANCH
RELAY=os.environ.get('DEEPSEEK_WEB_BASE_URL','http://192.168.55.100:3000').rstrip('/')
JWKS={'until':0,'keys':[]}
KEY_LOCK=threading.Lock()
CHAT_LOCK=threading.Lock()
ACTOR_LOCKS={actor:threading.Lock() for actor in ['GPT','CLAUDE','GROK']}
CODEX='/home/Scales/.local/share/repo-lens/codex-runtime-0.160.0/bin/codex'
CLAUDE='/home/Scales/.local/share/repo-lens/claude-runtime-2.1.288/bin/claude'
MAX_METADATA=2000000
class UsageLimit(ValueError): pass

def client_usage_limit(result):
    if not result.returncode:return False
    # Classify only a failed client's controlled error fields, never echo its output.
    messages=[]
    for line in result.stdout.splitlines():
        try:item=json.loads(line)
        except ValueError:continue
        if not isinstance(item,dict):continue
        if item.get('is_error'):messages.append(str(item.get('result','')))
        if item.get('type') in {'error','turn.failed'}:messages.append(json.dumps(item.get('error',{})))
    return bool(re.search(r"hit your (?:session|usage) limit|usage limit reached|rate limit|insufficient_quota|credit_balance_exhausted",' '.join(messages),re.I))
HOSTS={
 'opendata.cern.ch':'CERN Open Data',
 'www.hepdata.net':'HEPData', 'hepdata.net':'HEPData',
 'gwosc.org':'GWOSC/LIGO/Virgo/KAGRA', 'www.gwosc.org':'GWOSC/LIGO/Virgo/KAGRA',
 'mast.stsci.edu':'MAST', 'heasarc.gsfc.nasa.gov':'HEASARC',
 'gea.esac.esa.int':'Gaia Archive',
}

def unb64(s):return base64.urlsafe_b64decode(s+'='*((4-len(s)%4)%4))

def validate_claims(c, now=None):
    now=time.time() if now is None else now
    if c.get('iss')!=ISSUER or c.get('aud')!=AUDIENCE:raise ValueError('Wrong issuer or audience')
    if c.get('repository')!=REPOSITORY or c.get('repository_owner')!='One-Wave-Universe':raise ValueError('Wrong repository owner')
    if c.get('ref')!=BRANCH or c.get('workflow_ref')!=WORKFLOW or c.get('event_name')!='push':raise ValueError('Wrong workflow or branch')
    if not isinstance(c.get('exp'),(float,int)) or c['exp']<=now:raise ValueError('Expired identity')
    if c.get('nbf',0)>now+30 or c.get('iat',0)>now+30:raise ValueError('Identity not yet valid')
    return c

def authenticate(token):
    pieces=token.split('.')
    if len(pieces)!=3:raise ValueError('Invalid identity')
    h=json.loads(unb64(pieces[0]));c=json.loads(unb64(pieces[1]))
    if h.get('alg')!='RS256':raise ValueError('Wrong signature algorithm')
    with KEY_LOCK:
        if JWKS['until']<time.time() or not any(k.get('kid')==h.get('kid') for k in JWKS['keys']):
            with urllib.request.urlopen(ISSUER+'/.well-known/jwks',timeout=20) as response:JWKS['keys']=json.load(response)['keys']
            JWKS['until']=time.time()+300
        k=next((k for k in JWKS['keys'] if k.get('kid')==h.get('kid') and k.get('kty')=='RSA'),None)
    if not k:raise ValueError('Unknown signing key')
    public=rsa.RSAPublicNumbers(int.from_bytes(unb64(k['e']),'big'),int.from_bytes(unb64(k['n']),'big')).public_key()
    public.verify(unb64(pieces[2]),(pieces[0]+'.'+pieces[1]).encode(),padding.PKCS1v15(),hashes.SHA256())
    return validate_claims(c)

def metadata_url(url):
    u=urllib.parse.urlsplit(url)
    if u.scheme!='https' or u.hostname not in HOSTS or u.port not in (None,443) or u.username or u.password or u.fragment:raise ValueError('Unregistered metadata URL')
    if len(url)>4000:raise ValueError('Metadata URL too long')
    if u.hostname.endswith('gwosc.org') and not u.path.startswith(('/api/','/eventapi/','/timeline/')):raise ValueError('Use a GWOSC metadata endpoint')
    if u.hostname=='opendata.cern.ch' and not u.path.startswith('/api/'):raise ValueError('Use CERN metadata API')
    return url

class RegisteredRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        metadata_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def fetch_metadata(query):
    url=metadata_url(query['url']);purpose=str(query.get('purpose',''))
    if not purpose or len(purpose)>2000:raise ValueError('Metadata purpose required')
    req=urllib.request.Request(url,headers={'User-Agent':'Repo-Lens-Jetson/1','Accept':'application/json'})
    with urllib.request.build_opener(RegisteredRedirect()).open(req,timeout=60) as response:
        final=response.url;raw=response.read(MAX_METADATA+1);headers={k:response.headers.get(k) for k in ['Content-Type','ETag','Last-Modified']}
    if len(raw)>MAX_METADATA:raise ValueError('Metadata exceeds byte budget; no partial data returned')
    source=json.loads(raw)
    return {'provider':HOSTS[urllib.parse.urlsplit(final).hostname],'requested_url':url,'final_url':final,'purpose':purpose,'retrieved_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'worker':'Jetson','hostname':socket.gethostname(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'http_metadata':headers,'source_kind':'metadata','source_record':source,'pagination':'Provider pagination fields remain in source_record. This receipt covers this endpoint response, not unrequested archive pages.','units_calibration_quality':'Preserved where present in unchanged source_record; missing fields are unknown.'}

def chat(body):
    if not isinstance(body.get('prompt'),str) or not 1<=len(body['prompt'])<=240000:raise ValueError('Prompt must be 1..240000 characters')
    system=str(body.get('system',''))
    if len(system)>12000:raise ValueError('System instruction too long')
    actor=body.get('actor','DEEPSEEK')
    if actor not in ['DEEPSEEK','GPT','CLAUDE','GROK']:raise ValueError('Unknown actor')
    if actor in ['GPT','CLAUDE']:
        binary=CODEX if actor=='GPT' else CLAUDE
        if not pathlib.Path(binary).exists():raise ValueError(actor+' client not installed')
        prompt=system+'\n\n'+body['prompt']
        args=[binary,'exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','read-only','--json','--color','never','-'] if actor=='GPT' else [binary,'-p','--output-format','json','--tools','','--no-session-persistence']
        with ACTOR_LOCKS[actor]:r=subprocess.run(args,input=prompt,capture_output=True,text=True,cwd=str(pathlib.Path(__file__).parent),timeout=240)
        if client_usage_limit(r):raise UsageLimit('Provider usage limit reached')
        if r.returncode:raise ValueError(actor+' client failed; check local sign-in and plan limits')
        if actor=='GPT':
            events=[json.loads(line) for line in r.stdout.splitlines() if line.startswith('{')]
            if not any(x.get('type')=='turn.completed' for x in events):raise ValueError('GPT turn incomplete')
            answer='\n'.join(x['item'].get('text','') for x in events if x.get('type')=='item.completed' and x.get('item',{}).get('type')=='agent_message')
            identity=next((x.get('thread_id') for x in events if x.get('type')=='thread.started'),None)
        else:
            result=json.loads(r.stdout)
            if result.get('is_error'):raise ValueError('Claude turn failed')
            answer=result.get('result','');identity=result.get('session_id')
        if not isinstance(answer,str) or not answer.strip():raise ValueError(actor+' returned no visible answer')
        return {'provider':'openai' if actor=='GPT' else 'anthropic','transport':'signed-in-'+actor.lower()+'-client-on-Jetson','model':'Codex signed-in session' if actor=='GPT' else 'Claude signed-in session','response_id':identity,'answer':answer.strip()}
    if actor=='GROK':
        key=os.environ.get('XAI_API_KEY')
        if not key:raise ValueError('Grok authenticated route not configured')
        packet={'model':os.environ.get('GROK_MODEL','grok-4.7'),'input':system+'\n\n'+body['prompt'],'store':False}
        req=urllib.request.Request('https://api.x.ai/v1/responses',data=json.dumps(packet).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+key},method='POST')
        with ACTOR_LOCKS[actor]:
            with urllib.request.urlopen(req,timeout=240) as response:x=json.load(response)
        if x.get('status')!='completed':raise ValueError('Grok output incomplete')
        answer='\n'.join(p.get('text','') for item in x.get('output',[]) for p in item.get('content',[]) if p.get('type')=='output_text')
        if not answer.strip():raise ValueError('Grok returned no visible answer')
        return {'provider':'xai','transport':'Grok API via Jetson','model':x.get('model',packet['model']),'response_id':x.get('id'),'answer':answer.strip()}
    packet={'messages':[{'role':'system','content':system},{'role':'user','content':body['prompt']}],'extra_body':{'deepthink':False,'web_search':False,'expert_mode':False}}
    req=urllib.request.Request(RELAY+'/v1/chat/completions',data=json.dumps(packet).encode(),headers={'Content-Type':'application/json'},method='POST')
    with CHAT_LOCK:
        with urllib.request.urlopen(req,timeout=210) as response:x=json.load(response)
    choices=x.get('choices') or []
    if not choices or choices[0].get('finish_reason')!='stop':raise ValueError('DeepSeek output incomplete')
    answer=choices[0].get('message',{}).get('content')
    if not isinstance(answer,str) or not answer.strip():raise ValueError('No visible DeepSeek answer')
    return {'provider':'deepseek','transport':'free-web-firefox-via-Jetson','model':x.get('model') or 'web-session (model not exposed)','response_id':x.get('id'),'answer':answer.strip()}

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def send(self,status,data):
        raw=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    def do_GET(self):
        if self.path=='/health':self.send(200,{'ok':True,'service':'repo-lens-jetson','transport':'OIDC','capabilities':['deepseek-free-web','registered-science-metadata']})
        else:self.send(404,{'error':'Not found'})
    def do_POST(self):
        try:
            auth=self.headers.get('Authorization','')
            if not auth.startswith('Bearer '):raise ValueError('Identity required')
            authenticate(auth[7:])
        except Exception:self.send(401,{'error':'Valid Repo Lens GitHub Actions identity required'});return
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<=1000000:raise ValueError('Request size outside limit')
            body=json.loads(self.rfile.read(n))
            if self.path=='/metadata':out=fetch_metadata(body)
            elif self.path=='/chat':out=chat(body)
            else:self.send(404,{'error':'Not found'});return
            self.send(200,out)
        except UsageLimit:self.send(429,{'error':{'code':'provider_rate_limit'}})
        except urllib.error.HTTPError as e:
            if self.path=='/chat' and e.code==429:self.send(429,{'error':{'code':'provider_rate_limit'}})
            else:self.send(502,{'error':'Upstream HTTP '+str(e.code)})
        except Exception as e:self.send(400,{'error':str(e) if isinstance(e,ValueError) else type(e).__name__})

if __name__=='__main__':http.server.ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('REPO_LENS_PORT','8778'))),Handler).serve_forever()
