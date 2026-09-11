"""All writes reuse the same validation as the application and MCP."""
import argparse,json
from pathlib import Path
from store import connect,revision
import engine
def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['evaluate','export','propose','import']);p.add_argument('--mode',default='refresh');p.add_argument('--product-id');p.add_argument('--table');p.add_argument('--file');p.add_argument('--apply',action='store_true');p.add_argument('--role',choices=sorted(engine.ROLES),default='merch');args=p.parse_args()
    with connect()as c:
        if args.command=='evaluate':result=engine.state(c)['review']
        elif args.command=='export':result=engine.export(c)
        elif args.command=='propose':result=engine.create_scenario(c,{'base_revision':revision(c),'mode':args.mode,'product_id':args.product_id},args.role)
        else:result=engine.import_csv(c,args.table,Path(args.file).read_text(encoding='utf-8-sig'),args.role,not args.apply)
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
