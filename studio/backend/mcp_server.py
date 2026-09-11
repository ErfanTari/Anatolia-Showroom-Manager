"""Small MCP stdio adapter. Agents can read, evaluate and save drafts; never release work.
Protocol baseline: 2025-11-25. Transport is newline-delimited JSON-RPC on stdio.
"""
import sys,json
from store import connect,revision
import engine
TOOLS=[
 {'name':'showroom_summary','description':'Read APS revision, coverage, issues and missing product alternatives.','inputSchema':{'type':'object','properties':{}}},
 {'name':'showroom_records','description':'Read products, variants, slots, rules, fixtures or questions from SQLite.','inputSchema':{'type':'object','properties':{'table':{'type':'string','enum':['products','variants','slots','placements','fixtures','rules','questions','scenarios','tasks']},'id':{'type':'string'}},'required':['table']}},
 {'name':'propose_showroom','description':'Create a validated draft using deterministic refresh, new-product, color-order or fixture-move rules. Does not order, release, or change installed status.','inputSchema':{'type':'object','properties':{'mode':{'type':'string','enum':['refresh','new_product','color_order','fixture']},'product_id':{'type':'string'},'fixture_id':{'type':'string'},'base_revision':{'type':'integer'},'target':{'type':'object','properties':{'x_mm':{'type':'number'},'z_mm':{'type':'number'},'yaw_deg':{'type':'number'}},'required':['x_mm','z_mm','yaw_deg'],'additionalProperties':False}},'required':['mode','base_revision'],'additionalProperties':False}}]
def call(name,args):
    with connect()as c:
        if name=='showroom_summary':s=engine.state(c);return {'revision':revision(c),'review':s['review']}
        if name=='showroom_records':
            if args['table']not in TOOLS[1]['inputSchema']['properties']['table']['enum']:raise ValueError('Unknown table.')
            data=engine.state(c)[args['table']]
            return [x for x in data if not args.get('id')or x.get('id',x.get('slot_id'))==args['id']]
        if name=='propose_showroom':return {'scenario_id':engine.create_scenario(c,args,'agent')}
        raise ValueError('Unknown tool.')
def dispatch(message):
    method=message.get('method');id=message.get('id');params=message.get('params',{})
    if id is None:return None
    if method=='initialize':
        requested=params.get('protocolVersion');version=requested if requested in ['2024-11-05','2025-03-26','2025-06-18','2025-11-25']else'2025-11-25'
        value={'protocolVersion':version,'capabilities':{'tools':{'listChanged':False}},'serverInfo':{'name':'anatolia-showroom','version':'0.2.0'}}
    elif method=='ping':value={}
    elif method=='tools/list':value={'tools':TOOLS}
    elif method=='tools/call':
        try:value={'content':[{'type':'text','text':json.dumps(call(params['name'],params.get('arguments',{})),ensure_ascii=False)}],'isError':False}
        except Exception as e:value={'content':[{'type':'text','text':str(e)}],'isError':True}
    else:return {'jsonrpc':'2.0','id':id,'error':{'code':-32601,'message':'Method not found'}}
    return {'jsonrpc':'2.0','id':id,'result':value}
if __name__=='__main__':
    for line in sys.stdin:
        try:
            result=dispatch(json.loads(line))
            if result is not None:print(json.dumps(result,ensure_ascii=False),flush=True)
        except Exception:print(json.dumps({'jsonrpc':'2.0','id':None,'error':{'code':-32700,'message':'Invalid JSON-RPC request'}}),flush=True)
