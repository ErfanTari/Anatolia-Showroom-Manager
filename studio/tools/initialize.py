"""One-time migration of the reviewed APS model. Never overwrites an existing DB."""
from pathlib import Path
from collections import defaultdict,Counter
import sys,json,re,hashlib,unicodedata
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'backend'))
from store import connect,now,log
def read(n):return json.loads((ROOT/'sources'/n).read_text())
def canonical(name):
    name=re.sub(r'\s+Block\s+\d+.*','',name,flags=re.I);name=re.sub(r'^(Majesto|Lustra)\s+','',name,flags=re.I)
    name=re.sub(r'\s+bookmatch.*|\s+honed$','',name,flags=re.I);name=re.sub(r'\s*\(.*?\)','',name)
    name=re.sub(r'Lithoform\s+(\w+)\s*-\s*(Crosscut|Veincut)',r'Lithoform \2 \1',name,flags=re.I)
    n=' '.join(name.replace('_',' ').split()).title()
    n=n.replace('Pietra Imperialle','Pietra Imperiale').replace('Tuscano Rosso','Tuscano Burgundy').replace('Statuario Extra','Statuario')
    n=re.sub(r'\bGemma Bronz\b','Gemma Bronze',n);n=re.sub(r'\bArchiteq Graphit\b','Architeq Graphite',n)
    if n.endswith('Crosscut Coas'):n+='t'
    return n
def pid(name):return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',canonical(name)).encode('ascii','ignore').decode().lower()).strip('-')
def family(name):
    for f in ['Lithoform Crosscut','Lithoform Veincut','Architeq','Serena','Monoforma','Onyx']:
        if name.startswith(f):return f
    return name
def dims(value):
    m=re.search(r'(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)',value or '')
    if not m:return None,None
    a,b=map(float,m.groups());factor=10 if max(a,b)<=322 else 1
    return round(min(a,b)*factor),round(max(a,b)*factor)
def put(c,table,record):
    cols=list(record);c.execute(f'INSERT OR IGNORE INTO {table} ({",".join(cols)}) VALUES ({",".join("?"for _ in cols)})',[record[k]for k in cols])
def main():
    c=connect();c.executescript((ROOT/'backend/schema.sql').read_text())
    if c.execute("SELECT 1 FROM meta WHERE key='revision'").fetchone():print('Existing database retained. Use validated imports/commands for changes.');return
    source=read('aps-source-records.json');scene=read('scene-manifest.json');slots=read('initial-slots.json');options=read('assortment-options.json');facepack=read('face-register.json')
    c.execute('BEGIN IMMEDIATE')
    for k,v in {'revision':'1','schema_version':'1','source_sha256':source['sha256'],'policy_version':'APS-draft-2026-09-10','created_at':now(),'source_rows_json':json.dumps(source['records']),'portfolio_json':json.dumps(options)}.items():put(c,'meta',{'key':k,'value':v})
    put(c,'showrooms',{'id':'APS','name':'APS Temporary Showroom','geometry_json':json.dumps({k:v for k,v in scene.items()if k!='fixtures'}),'source_note':'APS plan 2025-11-21, BOM 2026-06-09, user-confirmed pilot. Geometry remains provisional.'})
    names={pid(r['name']):canonical(r['name'])for r in source['records']}
    for o in options:
        n=canonical(o['name_as_listed'] or o['reference_name'])
        if n and not any(t in n.lower()for t in ['confirmed','random','total','check','consider','faces','proposed','cancel']) and not re.fullmatch(r'[\d .-]+',n):names.setdefault(pid(n),n)
    for f in facepack['faces']:names.setdefault(f['design_id'],canonical(f['design_id'].replace('-',' ')))
    names['tuscano-burgundy']='Tuscano Burgundy'
    rawfaces=defaultdict(list)
    for f in facepack['faces']:rawfaces[f['design_id']].append(f)
    for id,name in sorted(names.items()):
        rgb=rawfaces[id][0]['rgb']if rawfaces[id]else None
        lightness=round((.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2])/255*100,2)if rgb else None
        temp='warm'if rgb and rgb[0]-rgb[2]>8 else 'neutral'if rgb else 'unconfirmed'
        commercial=name=='Travertino Classico'or name.startswith('Lithoform Veincut')
        put(c,'products',dict(id=id,name=name,family=family(name),positioning='commercial'if commercial else'unknown',hit=int(id in ['oro-noir','tuscano-burgundy']),lifecycle='unconfirmed',required=0,color_group=temp,color_rank=-lightness if lightness is not None else None,priority_source='User examples 2026-09-10'if commercial or id in ['oro-noir','tuscano-burgundy']else'Merch confirmation needed',notes='Color order derived from production preview brightness; draft for Merch review.',aliases_json=json.dumps(['Tuscano Rosso']if id=='tuscano-burgundy'else[])))
    variant_for={};firstvariant={};counter=Counter()
    for r in source['records']:
        id='SKU-'+r['sku'] if r['sku'] else 'SOURCE-'+r['id'];design=pid(r['name']);variant_for[r['id']]=id;firstvariant.setdefault(design,id)
        w,h=dims(r['size']);th=re.search(r'[\d.]+',r['thickness']);preview={k:r.get(k)for k in ['texture','texture_crop','texture_note']}
        if preview['texture']and preview['texture'].startswith('../'):preview['texture']='../../'+preview['texture'][3:]
        put(c,'variants',dict(id=id,product_id=design,sku=r['sku']or None,finish=r['finish']or'Unconfirmed',width_mm=w,height_mm=h,thickness_mm=float(th[0])if th else None,lifecycle='unconfirmed',availability='installed_reference'if r['sku']else'unknown',source_json=json.dumps(r),preview_json=json.dumps(preview)))
    # A photo identification is a separate non-SKU variant, not an invented furniture item number.
    base=next(r for r in source['records']if pid(r['name'])=='verdi-alpi')
    put(c,'variants',dict(id='PHOTO-VERDI-KITCHEN',product_id='verdi-alpi',sku=None,finish='Unconfirmed furniture finish',width_mm=None,height_mm=None,thickness_mm=None,lifecycle='unconfirmed',availability='installed_reference',source_json=json.dumps({'name':'Verdi Alpi','source_workbook':'Room 7 photograph / user identification','group':'furniture'}),preview_json=json.dumps({k:base.get(k)for k in ['texture','texture_note']})))
    variant_for['APS-PHOTO-VERDI-ALPI']='PHOTO-VERDI-KITCHEN'
    # Portfolio options supply candidate formats, never manufactured SKU numbers.
    for o in options:
        design=pid(o['name_as_listed']or o['reference_name'])
        if design not in names:continue
        w,h=dims(o['option_as_listed'])
        if not w and o['source_sheet']in['6mm','12mm']:w,h=1600,3200
        if not w:continue
        finish=o['marketing_header']or o['technical_header']or'Unconfirmed';th=o.get('thickness_mm')or None
        key=hashlib.sha256(f'{design}:{w}:{h}:{finish}:{th}'.encode()).hexdigest()[:14]
        put(c,'variants',dict(id='OPTION-'+key,product_id=design,sku=None,finish=finish,width_mm=w,height_mm=h,thickness_mm=th,lifecycle='unconfirmed',availability='unknown',source_json=json.dumps(o),preview_json='{}'))
    for f in facepack['faces']:
        if f['design_id']not in names:continue
        put(c,'faces',dict(id=f['id'],product_id=f['design_id'],width_mm=f['width_mm'],height_mm=f['height_mm'],data_json=json.dumps(f)))
    for w,h in [(1200,2800),(1600,3200)]:
        put(c,'variants',dict(id=f'OPTION-TUSCANO-{w}-{h}',product_id='tuscano-burgundy',sku=None,finish='Unconfirmed',width_mm=w,height_mm=h,thickness_mm=None,lifecycle='unconfirmed',availability='unknown',source_json=json.dumps({'source':'User-confirmed Tuscano Rosso alias; production-face format; release SKU required'}),preview_json='{}'))
    fs={f['id']:f for f in scene['fixtures']}
    for f in fs.values():
        put(c,'fixtures',dict(id=f['id'],showroom_id='APS',room=f['room'],type=f['type'],x_mm=f['x']*1000,z_mm=f['z']*1000,yaw_deg=f['yaw'],width_mm=f['width']*1000,height_mm=f['height']*1000,depth_mm=100 if f['type']=='fixed'else 205 if f['type']=='waterfall'else 680,relocatable=int(f['type']=='fixed'),geometry_verified=0,extra_json=json.dumps(f)))
    def face_for(design,w,h,index):
        pool=rawfaces[design]
        if not pool:return None
        pool=sorted(pool,key=lambda f:(abs(f['width_mm']-(w or 1600))+abs(f['height_mm']-(h or 3200)),f['face_index'],f['id']))
        best=pool[0];same=[f for f in pool if (f['width_mm'],f['height_mm'])==(best['width_mm'],best['height_mm'])]
        return same[index%len(same)]['id']
    for s in slots:
        f=fs.get(s['fixture_id']);variant=variant_for.get(s['record_id']);v=dict(c.execute('SELECT * FROM variants WHERE id=?',(variant,)).fetchone())if variant else None
        locked=s['type']not in ['fixed','sliding','rotating','waterfall'];tier='secondary';score=45;basis='Accessible on a guided showroom visit; provisional map classification.'
        if locked:tier='commercial'if s['type']=='floor'else'secondary';score=30 if s['type']=='floor'else 50
        elif f['type']=='fixed':
            central=abs(f['x']-14.5)<3.4;front_to_entry=s['side']if'side'in s else s.get('face')
            if central and front_to_entry=='front':tier='prime';score=92;basis='Central gallery face oriented towards the entrance route; sightline survey still required.'
        elif f['type']=='sliding':
            if f['position']in [12,13]:tier='prime';score=85;basis='Proposed first-presented face at the mirrored bank opening; confirm closed-bank presentation order.'
            else:score=35;basis='Inside the sliding bank; accessible after pull-out, not assumed visible when closed.'
        elif f['type']=='rotating':score=55 if s['face']=='front'else 30;basis='Front carrier face or reverse side; exposure depends on operation.'
        seq=f"R{s['room']}-{s['type']}" if not locked else None
        if f and f['type']=='rotating':seq+=f"-U{f['unit']}-{s['face']}"
        if f and f['type']=='sliding':seq+=f"-U{f['unit']}"
        intentional=int(bool(f and f['type']=='fixed'and v and v['product_id']in['calacatta-noir','macchia-vecchia']))
        put(c,'slots',dict(id=s['id'],showroom_id='APS',fixture_id=s['fixture_id'],room=s['room'],title=s['title'],type=s['type'],side=s.get('face'),width_mm=round(f['width']*1000)if f else v['width_mm']if v else None,height_mm=round(f['height']*1000)if f else v['height_mm']if v else None,locked=int(locked),intentional_repeat=intentional,visibility_tier=tier,visibility_score=score,visibility_basis=basis,sequence_group=seq,sequence_rank=f.get('position',int(re.search(r'(\d+)$',f['id'])[0])if re.search(r'(\d+)$',f['id'])else 0)if f else None,source_json=json.dumps(s)))
        design=v['product_id']if v else None;face=face_for(design,v['width_mm'],v['height_mm'],counter[design])if v else None;counter[design]+=1
        put(c,'placements',dict(slot_id=s['id'],variant_id=variant,face_id=face,state='reported_installed'if variant else'capacity_only',evidence='User-provided APS BOM/photos, reviewed 2026-09-09. Selected production image does not identify the exact installed face.',updated_at=now(),revision=1))
    rules=[
      ('R01','Protect live installations','locked','hard',{},'confirmed','User: live rooms and furniture stay fixed during routine refresh.'),
      ('R02','Fit the display format','format','hard',{'nominal_tolerance_mm':25},'draft','Whole panels require matching nominal format; waterfall may use a verified cut from a larger slab.'),
      ('R03','Exclude discontinued products','lifecycle','hard',{},'confirmed','A discontinued product cannot be proposed for a new installation.'),
      ('R04','Add missing designs first','coverage','soft',{'weight':100},'confirmed','User: use scarce movable slots to broaden the range.'),
      ('R05','Reduce repeated finishes','duplicate','soft',{'weight':35,'allow_intentional_bookmatch':True},'confirmed','Repeats can remain for bookmatch or a distinct useful finish/application.'),
      ('R06','Give Hit products prime exposure','hit_visibility','soft',{'weight':65,'minimum_score':80},'draft','User examples: Oro Noir and Tuscano Burgundy. Visibility tiers need a Merch/site review.'),
      ('R07','Keep color families together','color_adjacency','soft',{'weight':25},'draft','Group family/temperature and order light to dark. Initial ranks are image-derived suggestions.'),
      ('R08','Minimize disruption','change_cost','soft',{'weight':12,'max_changes':6},'draft','Prefer a product swap within an existing compatible fixture before moving its frame.'),
      ('R09','Protect the central route','geometry','hard',{'route_x_min_mm':13900,'route_x_max_mm':15100,'minimum_gap_mm':100},'draft','Illustrative keep-out strip, not an accessibility/building-code dimension. Design must supply verified geometry.'),
      ('R10','Release only complete work packages','release','hard',{'require_sku_for_orders':True,'require_lifecycle_for_orders':True,'require_geometry_review_for_moves':True},'confirmed','A visual proposal may contain missing data. Ordering/installing must expose and resolve those gaps.')]
    for id,name,kind,strength,param,status,reason in rules:put(c,'rules',dict(id=id,name=name,kind=kind,strength=strength,enabled=1,parameters_json=json.dumps(param),owner='Merch + Interior Design'if kind in['format','geometry']else'Merch',status=status,rationale=reason))
    qs=[
      ('Q01','Sales','Which products are Hit, in which market, and until when?','Oro Noir and Tuscano Burgundy are Hit examples; add market and effective dates.'),
      ('Q02','Sales','Which sales metric should influence priority, and over what period?','Showroom/region sales and margin as a limited secondary input; preserve launch exploration.'),
      ('Q03','Sales','What is the released SKU, finish, launch date and stock for each proposed new product?','Confirm Tuscano Burgundy and Architeq candidates before ordering.'),
      ('Q04','Merch','Which designs and finishes must every APS visit expose?','Maximize distinct designs in movable displays. Mark must-have designs explicitly.'),
      ('Q05','Merch','When is a repeat useful, and how many are allowed?','Retain documented bookmatch; prefer a new finish or format to an exact repeat.'),
      ('Q06','Merch','Which color groups and order should each family use?','Draft: family, warm/neutral subgroup, then light to dark. Confirm Architeq and Serena ranks.'),
      ('Q07','Merch','Which slots count as prime, secondary and commercial exposure?','Review the proposed map overlay and closed-bank front positions.'),
      ('Q08','Merch','Who can release changes, with what move/budget limit?','Merch releases work. Designers/agents propose. Showroom managers record actual completion.'),
      ('Q09','Interior Design','What are approved fixture sizes, thickness/load limits and travel envelopes?','Supply versioned supplier CAD/GLB and dimensioned constraints, including 6/9/12 mm compatibility.'),
      ('Q10','Interior Design','Which routes, services, sightlines and fixed anchors must remain clear?','Mark verified keep-outs and minimum clearances on the APS plan. Current map limits are draft.'),
      ('Q11','Interior Design','What defines Anatolia identity in a live room or display run?','Provide three approved and three rejected examples covering density, color balance, lighting and furniture.'),
      ('Q12','Merch + Showroom','Who orders, prepares, moves and verifies each item, and what proves completion?','Use a role-owned task with receipt/preparation/installation evidence and disposition of removed material.')]
    for id,team,q,a in qs:put(c,'questions',dict(id=id,team=team,question=q,proposed_answer=a))
    for id,title,owner in [('SETUP-01','Confirm prime locations and color order','Merch'),('SETUP-02','Supply fixture limits and measured keep-outs','Interior Design'),('SETUP-03','Confirm Tuscano Burgundy SKUs, availability and launch status','Sales / Product'),('SETUP-04','Verify W9F items and exact kitchen SKU','Showroom manager')]:
        put(c,'tasks',dict(id=id,scenario_id=None,title=title,kind='collect_input',owner=owner,due_date=None,stage='to_do',slot_id=None,variant_id=None,requires_order=0,evidence='',disposition='',dependencies_json='[]',details_json='{}',updated_at=now()))
    log(c,'migration','initialize','APS',{'source_hash':source['sha256'],'slots':len(slots),'user_decisions':['Tuscano Burgundy alias','protect live installations','broaden movable-display coverage']});c.commit()
    print({t:c.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]for t in['products','variants','faces','fixtures','slots','placements','rules','questions','tasks']})
if __name__=='__main__':main()
