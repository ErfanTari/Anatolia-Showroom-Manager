"""Loopback-only local application; GitHub Pages serves the exported review snapshot."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from pathlib import Path
import argparse,json,os,sys
from store import connect,ROOT
import engine

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT.parent),**kwargs)
    def json(self,value,status=200):
        body=json.dumps(value,ensure_ascii=False).encode();self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(body)))
        self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
    def valid_origin(self):
        host=self.headers.get('Host','').split(':')[0]
        if host not in ['127.0.0.1','localhost']:raise PermissionError('Only local connections are accepted.')
        origin=self.headers.get('Origin')
        if origin and origin not in [f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}']:
            raise PermissionError('Cross-origin writes are not accepted.')
    def do_GET(self):
        if urlparse(self.path).path=='/api/state':
            try:
                self.valid_origin()
                with connect()as c:s=engine.state(c)
                s['meta'].update(mode='connected',operator_role=self.server.role)
                self.json(s)
            except Exception as e:self.json({'error':str(e)},400)
        else:
            # Do not expose source-control internals or local backup files through the server.
            from urllib.parse import unquote
            parts=Path(unquote(urlparse(self.path).path)).parts
            if any(p.startswith('.')or p in ['backups','__pycache__']for p in parts):self.send_error(403);return
            super().do_GET()
    def do_POST(self):
        try:
            self.valid_origin();length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=4_000_000:raise ValueError('Request must be between 1 byte and 4 MB.')
            body=json.loads(self.rfile.read(length));path=urlparse(self.path).path;role=self.server.role
            with connect()as c:
                if path=='/api/propose':result={'scenario_id':engine.create_scenario(c,body,role)}
                elif path=='/api/release':engine.release(c,body['id'],body['base_revision'],role);result={'released':body['id']}
                elif path=='/api/task':engine.update_task(c,body['id'],body,body['base_revision'],role);result={'updated':body['id']}
                elif path=='/api/observe':engine.observe(c,body,role);result={'observed':body['slot_id']}
                elif path=='/api/edit':engine.edit(c,body['table'],body['records'],body['base_revision'],role);result={'updated':body['table']}
                elif path=='/api/import':result=engine.import_csv(c,body['table'],body['csv'],role,body.get('dry_run',True))
                elif path=='/api/export':result=engine.export(c)
                else:self.json({'error':'Unknown endpoint'},404);return
            self.json(result)
        except PermissionError as e:self.json({'error':str(e)},403)
        except (ValueError,KeyError,TypeError)as e:self.json({'error':str(e)},400)
        except Exception as e:
            import traceback;traceback.print_exc();self.json({'error':'Operation failed; no partial update was committed. '+str(e)},500)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765);parser.add_argument('--role',choices=sorted(engine.ROLES),default=os.environ.get('STUDIO_ROLE','merch'));args=parser.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler);server.role=args.role
    print(f'Anatolia Studio: http://127.0.0.1:{args.port}/studio/web/ | trusted local role: {args.role}',flush=True)
    server.serve_forever()
if __name__=='__main__':main()
