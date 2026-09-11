"""Exercise the actual HTTP boundary against an isolated SQLite copy."""
import unittest,sys,tempfile,os,json,threading
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'backend'))
from store import connect,DEFAULT_DB
from server import Handler

class HTTPTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();db=str(Path(self.temp.name)/'test.sqlite')
        with connect(DEFAULT_DB)as source,connect(db)as target:source.backup(target)
        self.old=os.environ.get('STUDIO_DB');os.environ['STUDIO_DB']=db
        self.server=ThreadingHTTPServer(('127.0.0.1',0),Handler);self.server.role='merch'
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.url=f'http://127.0.0.1:{self.server.server_port}'
    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join()
        if self.old is None:os.environ.pop('STUDIO_DB',None)
        else:os.environ['STUDIO_DB']=self.old
        self.temp.cleanup()
    def call(self,path,payload=None,origin=None):
        headers={'Content-Type':'application/json'}
        if origin:headers['Origin']=origin
        req=Request(self.url+'/api/'+path,data=json.dumps(payload).encode()if payload is not None else None,headers=headers)
        try:
            with urlopen(req,timeout=10)as response:return response.status,json.load(response)
        except HTTPError as e:return e.code,json.load(e)
    def test_edit_persists_and_rejects_stale_request(self):
        code,s=self.call('state');self.assertEqual(code,200);r=s['meta']['revision']
        body={'table':'questions','records':[{'id':'Q01','answer':'TEST answer','owner':'TEST Merch','status':'answered','evidence':'TEST meeting'}],'base_revision':r}
        code,value=self.call('edit',body);self.assertEqual(code,200)
        code,s=self.call('state');self.assertEqual(next(q for q in s['questions']if q['id']=='Q01')['answer'],'TEST answer')
        self.assertEqual(self.call('edit',body)[0],400)
    def test_role_cannot_be_spoofed_and_cross_origin_is_rejected(self):
        self.server.role='agent';code,s=self.call('state')
        body={'id':s['scenarios'][0]['id'],'base_revision':s['meta']['revision'],'actor':'merch','role':'merch'}
        self.assertEqual(self.call('release',body)[0],403)
        self.assertEqual(self.call('propose',{'base_revision':s['meta']['revision'],'mode':'refresh'},'https://example.invalid')[0],403)
        self.assertEqual(self.call('propose',{'mode':'refresh'})[0],400)

if __name__=='__main__':unittest.main()
