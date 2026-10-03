#!/usr/bin/env python3
"""One bounded refresh of the Jetson metadata cache. No timer or retry."""
import hashlib,json,pathlib,time,urllib.request,os
import gateway

SOURCES=[
 ('cern','https://opendata.cern.ch/api/records/?size=1'),
 ('gwosc','https://gwosc.org/api/v2/catalogs'),
]

def refresh():
    root=gateway.METADATA_ROOT
    root.mkdir(parents=True,exist_ok=True)
    results=[]
    for label,url in SOURCES:
        gateway.metadata_url(url)
        req=urllib.request.Request(url,headers={'User-Agent':'Repo-Lens-Jetson/1','Accept':'application/json'})
        with urllib.request.build_opener(gateway.RegisteredRedirect()).open(req,timeout=60) as response:
            raw=response.read(gateway.MAX_METADATA+1)
            final=response.url
            http={k:response.headers.get(k) for k in ['Content-Type','ETag','Last-Modified']}
        if len(raw)>gateway.MAX_METADATA:raise ValueError('Metadata exceeds byte budget; snapshot not saved')
        source=json.loads(raw)
        sha=hashlib.sha256(raw).hexdigest()
        retrieved=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
        folder=root/label
        folder.mkdir(exist_ok=True)
        target=folder/(sha+'.json')
        # Content-addressed immutable snapshots preserve exact provider bytes.
        try:
            with target.open('xb') as f:f.write(raw)
        except FileExistsError:
            if target.read_bytes()!=raw:raise ValueError('Snapshot hash collision or corruption')
        receipt={'provider':gateway.HOSTS[urllib.parse.urlsplit(final).hostname],
                 'source_class':'real','source_kind':'provider-native-metadata',
                 'requested_url':url,'final_url':final,'retrieved_at':retrieved,
                 'worker':'Jetson','bytes':len(raw),'sha256':sha,
                 'relative_path':str(target.relative_to(root)),
                 'http_metadata':http,
                 'pagination':{'next':source.get('next') if isinstance(source,dict) else None,
                   'coverage':'One bounded endpoint response. No unrequested pages or bulk data fetched.'},
                 'derived_transform':None,
                 'interpretation':'External metadata retrieval, not evidence supporting One-Wave physics.'}
        stamp=str(time.time_ns())
        receipt_path=folder/(sha+'.'+stamp+'.receipt.json')
        with receipt_path.open('x') as f:json.dump(receipt,f,indent=2)
        # Exercise the exact same dispatcher used by the council.
        verified=gateway.metadata_tool({'operation':'read','relative_path':receipt['relative_path'],'purpose':'Verify fresh metadata snapshot through council bridge'})
        if verified['sha256']!=sha or verified['source_record']!=source:raise ValueError('Council snapshot read mismatch')
        results.append(receipt)
        print(json.dumps({'status':'COMPLETE',**receipt}),flush=True)
    listing=gateway.metadata_tool({'operation':'list','purpose':'Verify repaired Jetson cache'})
    print(json.dumps({'status':listing['status'],'local_files':len(listing['files']),'metadata_root':str(root)}),flush=True)
    return results

if __name__=='__main__':refresh()
