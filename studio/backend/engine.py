"""Shared deterministic domain layer for HTTP, CSV, CLI and MCP.

Proposals never rewrite observed placements. Only a verified task or an explicit
manager observation changes the current showroom, in one audited transaction.
"""
import json, math, uuid, csv, io
from collections import Counter, defaultdict
from store import rows, revision, now, log, bump, transaction, ROOT

ROLES = {'merch', 'designer', 'manager', 'agent'}
STAGES = ['to_do', 'ordered', 'prepared', 'installed', 'verified']

def unpack(row):
    d = dict(row)
    for k in list(d):
        if k.endswith('_json'):
            d[k[:-5]] = json.loads(d.pop(k))
    return d

def state(c):
    result = {t: [unpack(x) for x in rows(c, f'SELECT * FROM {t} ORDER BY id')]
              for t in ['products','variants','faces','fixtures','slots','rules','questions','scenarios','tasks','showrooms']}
    result['placements'] = rows(c, 'SELECT * FROM placements ORDER BY slot_id')
    meta = dict(c.execute('SELECT key,value FROM meta'))
    result['source'] = {'sha256':meta['source_sha256'],'records':json.loads(meta['source_rows_json'])}
    result['portfolio'] = json.loads(meta['portfolio_json'])
    result['meta'] = {k:v for k,v in meta.items() if not k.endswith('_json')}
    result['meta']['revision'] = revision(c)
    result['events'] = [unpack(x) for x in rows(c,'SELECT * FROM events ORDER BY id DESC LIMIT 80')]
    result['review'] = evaluate(result)
    return result

def indexes(s):
    return ({x['id']:x for x in s['products']}, {x['id']:x for x in s['variants']},
            {x['id']:x for x in s['slots']}, {x['slot_id']:x for x in s['placements']})

def rule(s, kind):
    return next((r for r in s['rules'] if r['kind']==kind and r['enabled']), None)

def parameters(s,kind):
    r=rule(s,kind)
    return r['parameters'] if r else {}

def compatibility(s,slot,variant):
    """Nominal visual feasibility; does not certify load, stock or fabrication."""
    products=s.get('_product_index')
    if products is None:products={p['id']:p for p in s['products']};s['_product_index']=products
    errors=[]
    if slot['locked']: errors.append('Live installation / furniture is protected.')
    if variant['lifecycle']=='discontinued' or products[variant['product_id']]['lifecycle']=='discontinued':
        errors.append('Product or variant is discontinued.')
    w,h=variant['width_mm'],variant['height_mm'];sw,sh=slot['width_mm'],slot['height_mm']
    tolerance=parameters(s,'format').get('nominal_tolerance_mm',25)
    if not all([w,h,sw,sh]):errors.append('A verified product/display format is missing.')
    elif slot['type']=='waterfall':
        if w+tolerance<sw or h+tolerance<sh:errors.append('Slab is too small for this cut panel.')
    elif abs(w-sw)>tolerance or abs(h-sh)>tolerance:errors.append('Nominal product format does not fit this slot.')
    return errors

def evaluate(s,changes=None):
    products,variants,slots,placements=indexes(s)
    placements={k:dict(v) for k,v in placements.items()}
    for change in changes or []:
        if change['kind']=='placement':placements[change['slot_id']]['variant_id']=change['variant_id']
    used=defaultdict(list);issues=[];fits=[];repeat_groups=[]
    def issue(code,level,slot,description,product=None):
        issues.append(dict(code=code,level=level,slot_id=slot['id'] if slot else None,
                           product_id=product,description=description))
    for sid,a in placements.items():
        if a['variant_id']:
            v=variants[a['variant_id']];used[v['product_id']].append(sid)
    for design,ids in sorted(used.items()):
        movable=[i for i in ids if not slots[i]['locked']]
        if len(ids)>1 and movable:
            exact=Counter(placements[i]['variant_id'] for i in movable)
            repeat_groups.append(dict(product_id=design,name=products[design]['name'],slot_ids=ids,
                movable_count=len(movable),distinct_finishes=len(set(variants[placements[i]['variant_id']]['finish']for i in ids)),
                intentional=all(slots[i]['intentional_repeat']for i in movable)))
            if rule(s,'duplicate'):
                for i in movable:
                    if not slots[i]['intentional_repeat']:
                        msg='Same variant repeated; candidate for broader coverage.' if exact[placements[i]['variant_id']]>1 else 'Design appears elsewhere. A distinct finish may justify this placement.'
                        issue('duplicate','review',slots[i],msg,design)
    for sid,a in placements.items():
        if not a['variant_id']:continue
        v=variants[a['variant_id']];p=products[v['product_id']];slot=slots[sid];problems=[]
        if p['lifecycle']=='discontinued' or v['lifecycle']=='discontinued':problems.append(('discontinued','Product/variant is discontinued; schedule a reviewed replacement.'))
        if rule(s,'hit_visibility') and p['hit'] and slot['visibility_score']<parameters(s,'hit_visibility').get('minimum_score',80) and not slot['locked']:
            problems.append(('hit_exposure','Hit product is behind a secondary face. Review its first-view exposure.'))
        if p['positioning']=='prime' and slot['visibility_tier']!='prime' and not slot['locked']:
            problems.append(('prime_exposure','Prime-positioned product is on a secondary face; confirm its role.'))
        if slot['visibility_tier']=='prime' and p['positioning']=='commercial':
            problems.append(('commercial_prime','Commercial example occupies a prime face. Confirm an intentional exception or review.'))
        for code,msg in problems:issue(code,'attention',slot,msg,p['id'])
        if slot['intentional_repeat'] and not problems:fits.append(dict(slot_id=sid,product_id=p['id'],description='Documented bookmatch repetition is intentional.'))
        if not problems and ((p['hit'] and slot['visibility_tier']=='prime') or (p['positioning']=='commercial' and slot['type']=='floor')):
            fits.append(dict(slot_id=sid,product_id=p['id'],description='Hit product has prime exposure.'if p['hit']else'Commercial product shown in a live floor application.'))
    # Group/order issues stay suggestions until Merch confirms the image-derived ranks.
    sequences=defaultdict(list)
    for slot in slots.values():
        if slot['sequence_group'] and slot['type']=='rotating' and placements[slot['id']]['variant_id']:
            sequences[slot['sequence_group']].append(slot)
    if rule(s,'color_adjacency'):
        for group,seq in sequences.items():
            seq.sort(key=lambda x:(x['sequence_rank'],x['id']))
            keys=[]
            for slot in seq:
                p=products[variants[placements[slot['id']]['variant_id']]['product_id']]
                keys.append((p['family'],p['color_group'],p['color_rank'] if p['color_rank'] is not None else 999,p['id']))
            ordered=sorted(keys)
            for slot,actual,target in zip(seq,keys,ordered):
                if actual!=target:issue('color_order','review',slot,'Draft family/color sequence could be improved in this rotating run.',actual[3])
    missing=[]
    for p in s['products']:
        if p['id']in used or p['lifecycle']=='discontinued':continue
        candidates=[v for v in s['variants']if v['product_id']==p['id'] and v['lifecycle']!='discontinued']
        matches=[]
        for slot in s['slots']:
            if any(not compatibility(s,slot,v)for v in candidates):matches.append(slot['id'])
        missing.append(dict(product_id=p['id'],name=p['name'],hit=p['hit'],required=p['required'],compatible_slot_ids=matches,
            alternative='Replace a repeat in a compatible movable display.'if matches else'Add a labeled library sample or propose a verified display format; no compatible current slot was identified.'))
    missing.sort(key=lambda p:(-p['hit'],-p['required'],p['name']))
    return dict(issues=issues,good=fits,duplicates=repeat_groups,missing=missing,
        summary=dict(occupied_slots=sum(bool(x['variant_id'])for x in placements.values()),unique_designs=len(used),
        catalogue_designs=len(products),missing_designs=len(missing),repeated_designs=len(repeat_groups),
        attention_slots=len(set(x['slot_id']for x in issues if x['level']=='attention')),good_slots=len(fits)),
        basis='Observed BOM/photo setup; visibility, format limits and color order are provisional. Catalogue includes unconfirmed portfolio options.')

def choose_face(s,variant):
    pool=[f for f in s['faces']if f['product_id']==variant['product_id']]
    if not pool:return None
    return min(pool,key=lambda f:(abs(f['width_mm']-(variant['width_mm']or 1600))+abs(f['height_mm']-(variant['height_mm']or 3200)),f['id']))['id']

def release_blockers(s,change):
    if change['kind']=='fixture':
        f=next(f for f in s['fixtures']if f['id']==change['fixture_id'])
        errors=geometry_errors(s,f,change['to'])
        if not f['geometry_verified'] or not rule(s,'geometry') or rule(s,'geometry')['status']!='confirmed':
            errors.append('Interior Design must verify the fixture and approve measured keep-outs/travel clearances.')
        return errors
    products,variants,slots,placements=indexes(s)
    slot=slots[change['slot_id']];v=variants[change['variant_id']]
    errors=compatibility(s,slot,v)
    if slot['intentional_repeat']:errors.append('Documented bookmatch pairing must be reviewed as a whole group.')
    if not v['sku']:errors.append('Released SKU is missing.')
    if v['lifecycle']!='active' or products[v['product_id']]['lifecycle']!='active':errors.append('Sales/Product must confirm active product and variant status.')
    if v['availability']!='available':errors.append('Stock / procurement availability is unconfirmed.')
    if not v['thickness_mm']:errors.append('Product thickness is missing.')
    if not rule(s,'format') or rule(s,'format')['status']!='confirmed':errors.append('Merch/Design must confirm fixture format, thickness and load compatibility.')
    if slot['type']=='waterfall':errors.append('A cut drawing and fabrication approval are required for this waterfall panel.')
    return errors

def rect(f):
    a=math.radians(f['yaw_deg']);co,si=math.cos(a),math.sin(a)
    return [(f['x_mm']+x*co+z*si,f['z_mm']-x*si+z*co)for x,z in
            [(-f['width_mm']/2,-f['depth_mm']/2),(f['width_mm']/2,-f['depth_mm']/2),(f['width_mm']/2,f['depth_mm']/2),(-f['width_mm']/2,f['depth_mm']/2)]]

def overlap(a,b,gap=0):
    for polygon in (a,b):
        for i in range(4):
            p,q=polygon[i],polygon[(i+1)%4];axis=(-(q[1]-p[1]),q[0]-p[0]);norm=math.hypot(*axis)
            aa=[(x*axis[0]+z*axis[1])/norm for x,z in a];bb=[(x*axis[0]+z*axis[1])/norm for x,z in b]
            if max(aa)+gap<=min(bb)or max(bb)+gap<=min(aa):return False
    return True

def geometry_errors(s,fixture,target):
    if not fixture['relocatable']:return ['Fixture is anchored or its relocation has not been authorized.']
    if set(target)!={'x_mm','z_mm','yaw_deg'}:return ['A move requires x_mm, z_mm and yaw_deg only.']
    if any(not isinstance(v,(int,float)) or not math.isfinite(v)for v in target.values()):return ['Coordinates must be finite numbers in millimetres.']
    f={**fixture,**target};polygon=rect(f);errors=[];geom=s['showrooms'][0]['geometry'];fp=geom['footprint']
    if any(x<0 or z<0 or x>fp['width']*1000 or z>fp['depth']*1000 for x,z in polygon):errors.append('Fixture extends outside the showroom footprint.')
    param=parameters(s,'geometry');xmin=param.get('route_x_min_mm',13900);xmax=param.get('route_x_max_mm',15100)
    if max(x for x,z in polygon)>xmin and min(x for x,z in polygon)<xmax:errors.append('Fixture crosses the draft central-route keep-out.')
    # Current movable frames are in the gallery. Proposals cannot enter reconstructed live rooms.
    for room in geom['rooms']:
        x1,z1,x2,z2=[v*1000 for v in room['bounds']]
        if overlap(polygon,[(x1,z1),(x2,z1),(x2,z2),(x1,z2)]):errors.append(f"Move enters protected live/display room {room['id']}.")
    for other in s['fixtures']:
        if other['id']!=f['id'] and overlap(polygon,rect(other),param.get('minimum_gap_mm',100)):
            errors.append('Collision / draft spacing conflict with '+other['id'])
    return errors

def validate_changes(s,changes):
    products,variants,slots,placements=indexes(s);seen=set()
    if not changes:raise ValueError('No feasible changes were found. Review format or source gaps.')
    for change in changes:
        kind=change.get('kind');identity=change.get('slot_id') if kind=='placement'else change.get('fixture_id')
        if (kind,identity)in seen:raise ValueError('Duplicate change target: '+str(identity))
        seen.add((kind,identity))
        if kind=='placement':
            if identity not in slots or change.get('variant_id')not in variants:raise ValueError('Unknown slot or variant.')
            if placements[identity]['variant_id']!=change.get('from_variant_id'):raise ValueError('Placement changed since the proposal was prepared.')
            errors=compatibility(s,slots[identity],variants[change['variant_id']])
            if errors:raise ValueError('; '.join(errors))
            if slots[identity]['intentional_repeat']:raise ValueError('Protect the documented bookmatch pair.')
            face=next((f for f in s['faces']if f['id']==change.get('face_id')),None)
            if change.get('face_id') and (not face or face['product_id']!=variants[change['variant_id']]['product_id']):raise ValueError('Face does not belong to the proposed product.')
        elif kind=='fixture':
            f=next((f for f in s['fixtures']if f['id']==identity),None)
            if not f:raise ValueError('Unknown fixture.')
            if any(f[k]!=v for k,v in change.get('from',{}).items()):raise ValueError('Fixture position changed.')
            errors=geometry_errors(s,f,change['to'])
            if errors:raise ValueError('; '.join(errors))
        else:raise ValueError('Unknown change kind.')

def plan(s,mode='refresh',product_id=None,fixture_id=None,target=None,max_changes=None):
    products,variants,slots,placements=indexes(s);changes=[]
    if mode=='fixture':
        f=next((f for f in s['fixtures']if f['id']==fixture_id),None)
        if not f:raise ValueError('Choose a known fixture.')
        changes=[dict(kind='fixture',fixture_id=f['id'],**{'from':{k:f[k]for k in ['x_mm','z_mm','yaw_deg']},'to':target},reason='Designer/agent layout proposal; keeps source assignments on the same frame.')]
    elif mode=='color_order':
        groups=defaultdict(list)
        for slot in s['slots']:
            if slot['type']=='rotating' and not slot['locked']:groups[slot['sequence_group']].append(slot)
        for seq in groups.values():
            seq.sort(key=lambda x:(x['sequence_rank'],x['id']));occupied=[x for x in seq if placements[x['id']]['variant_id']]
            def key(slot):
                v=variants[placements[slot['id']]['variant_id']];p=products[v['product_id']]
                return p['family'],p['color_group'],p['color_rank'] if p['color_rank'] is not None else 999,p['id'],v['id']
            ordered=sorted(occupied,key=key)
            for slot,donor in zip(occupied,ordered):
                a=placements[slot['id']];b=placements[donor['id']]
                if a['variant_id']!=b['variant_id']:
                    changes.append(dict(kind='placement',slot_id=slot['id'],from_variant_id=a['variant_id'],variant_id=b['variant_id'],face_id=b['face_id'],reason='Keep family/temperature together, then light to dark; Merch must confirm suggested color ranks.'))
    elif mode in ['refresh','new_product']:
        if mode=='new_product' and product_id not in products:raise ValueError('Choose a known product.')
        max_changes=max(1,min(20,int(max_changes or parameters(s,'change_cost').get('max_changes',6))))
        for _ in range(1 if mode=='new_product' else max_changes):
            current={sid:a['variant_id']for sid,a in placements.items()}
            for change in changes:current[change['slot_id']]=change['variant_id']
            counts=Counter(variants[v]['product_id']for v in current.values()if v)
            exact=Counter(current.values());changed={x['slot_id']for x in changes};best=None
            for slot in sorted(s['slots'],key=lambda x:x['id']):
                sid=slot['id'];old=variants.get(current[sid]);oldp=products.get(old['product_id'])if old else None
                if slot['locked'] or slot['intentional_repeat'] or sid in changed:continue
                if old and counts[old['product_id']]<=1 and oldp['lifecycle']!='discontinued' and old['lifecycle']!='discontinued':continue
                for v in sorted(s['variants'],key=lambda x:x['id']):
                    p=products[v['product_id']]
                    if mode=='new_product' and p['id']!=product_id:continue
                    if v['id']==current[sid] or counts[p['id']]>0 or compatibility(s,slot,v):continue
                    # Candidates must come from an assortment/BOM variant, not an image alone.
                    score=parameters(s,'coverage').get('weight',0)+p['required']*100
                    score+=parameters(s,'hit_visibility').get('weight',0)*p['hit']*slot['visibility_score']/100
                    score+=parameters(s,'duplicate').get('weight',0)*(1 if exact[current[sid]]>1 else .4)
                    score-=parameters(s,'change_cost').get('weight',0)
                    score-=30 if slot['type']=='waterfall' else 0
                    # Unresolved source spellings and concepts stay visible but cannot displace a verified identity.
                    if not v['sku'] and not any(f['product_id']==p['id']for f in s['faces']):continue
                    score+=3 if v['sku'] else 0
                    score-=15 if oldp and oldp['hit'] and slot['visibility_tier']=='prime' else 0
                    candidate=(round(score,3),sid,v['id'])
                    if best is None or candidate[0]>best[0]:best=(candidate[0],sid,v['id'])
            if best is None:break
            score,sid,vid=best;v=variants[vid]
            changes.append(dict(kind='placement',slot_id=sid,from_variant_id=placements[sid]['variant_id'],variant_id=vid,face_id=choose_face(s,v),score=score,
                reason='Add an unrepresented design by replacing a movable repeat; preserve at least one existing presentation. Score includes coverage, repeat value, Hit exposure and change cost.'))
    else:raise ValueError('Unknown planning mode.')
    validate_changes(s,changes)
    return changes

def create_scenario(c,request,actor='merch'):
    if actor not in ROLES:raise PermissionError('Unknown operator role.')
    with transaction(c,request.get('base_revision')):
        s=state(c);changes=request.get('changes') or plan(s,**{k:request[k]for k in ['mode','product_id','fixture_id','target','max_changes']if k in request})
        validate_changes(s,changes)
        for ch in changes:ch['blockers']=release_blockers(s,ch)
        id='PLAN-'+uuid.uuid4().hex[:10];mode=request.get('mode','manual')
        titles={'refresh':'Broader coverage · movable displays','color_order':'Rotating panels · family and color order','fixture':'Fixture position study'}
        title=request.get('title') or titles.get(mode,'Merch placement proposal')
        if mode=='new_product' and not request.get('title'):
            title='Introduce '+next(p['name']for p in s['products']if p['id']==request['product_id'])
        c.execute('INSERT INTO scenarios VALUES(?,?,?,?,?,?,?,?,?)',(id,title,mode,revision(c),'draft',now(),actor,json.dumps(changes),json.dumps({'before':s['review']['summary'],'after':evaluate(s,changes)['summary']})))
        log(c,actor,'propose',id,{'changes':len(changes),'mode':mode})
    return id

def release(c,id,expected,actor):
    if actor!='merch':raise PermissionError('Merch authority is required to release a work package.')
    with transaction(c,expected):
        row=c.execute('SELECT * FROM scenarios WHERE id=?',(id,)).fetchone()
        if not row:raise ValueError('Unknown proposal.')
        scenario=unpack(row)
        if scenario['status']!='draft':raise ValueError('Only a draft can be released once.')
        if scenario['base_revision']!=revision(c):raise ValueError('Source revision changed. Generate a fresh proposal.')
        s=state(c);validate_changes(s,scenario['changes'])
        blockers=[b for change in scenario['changes']for b in release_blockers(s,change)]
        if blockers:raise ValueError('Release blocked: '+'; '.join(dict.fromkeys(blockers)))
        for i,ch in enumerate(scenario['changes']):
            tid=f'{id}-TASK-{i+1:02d}';sid=ch.get('slot_id');vid=ch.get('variant_id')
            c.execute('INSERT INTO tasks VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(tid,id,'Move '+ch['fixture_id'] if ch['kind']=='fixture' else 'Replace display at '+sid,ch['kind'],'Merch / installation team',None,'to_do',sid,vid,int(ch['kind']=='placement' and scenario['mode']!='color_order'),'', '', '[]',json.dumps(ch),now()))
        c.execute("UPDATE scenarios SET status='released' WHERE id=?",(id,));log(c,actor,'release',id,{'tasks':len(scenario['changes'])})

def update_task(c,id,payload,expected,actor):
    if actor not in ['merch','manager']:raise PermissionError('Merch or showroom management records work progress.')
    with transaction(c,expected):
        row=c.execute('SELECT * FROM tasks WHERE id=?',(id,)).fetchone()
        if not row:raise ValueError('Unknown task.')
        t=unpack(row);stage=payload.get('stage',t['stage']);evidence=payload.get('evidence',t['evidence']).strip();disposition=payload.get('disposition',t['disposition']).strip()
        if stage not in STAGES:raise ValueError('Unknown work stage.')
        skip_order=not t['requires_order'] and t['stage']=='to_do' and stage=='prepared'
        if t['kind']!='collect_input' and not skip_order and STAGES.index(stage)>STAGES.index(t['stage'])+1:raise ValueError('Record each preparation/installation step in order.')
        if STAGES.index(stage)<STAGES.index(t['stage']):raise ValueError('Completed work stages cannot be silently rolled back.')
        if stage!=t['stage'] and stage in ['ordered','prepared','installed','verified'] and not evidence:raise ValueError('Add receipt, preparation, installation or verification evidence.')
        if t['stage']=='verified' and stage!=t['stage']:raise ValueError('Verified tasks are final.')
        if stage=='verified' and t['stage']!='verified' and t['kind']!='collect_input':
            if not disposition:raise ValueError('Record where the removed material goes, or explain that no material was removed.')
            ch=t['details'];s=state(c)
            if ch['kind']=='placement':
                old=c.execute('SELECT * FROM placements WHERE slot_id=?',(t['slot_id'],)).fetchone()
                if old['variant_id']!=ch['from_variant_id']:raise ValueError('The observed placement changed during this work. Merch must reconcile it.')
                c.execute('UPDATE placements SET variant_id=?,face_id=?,state=?,evidence=?,updated_at=?,revision=revision+1 WHERE slot_id=?',(t['variant_id'],ch.get('face_id'),'verified_installed',evidence,now(),t['slot_id']))
            else:
                f=next(f for f in s['fixtures']if f['id']==ch['fixture_id'])
                if any(f[k]!=v for k,v in ch['from'].items()):raise ValueError('Fixture changed during work; reconcile before verification.')
                errors=geometry_errors(s,f,ch['to'])
                if errors:raise ValueError('; '.join(errors))
                c.execute('UPDATE fixtures SET x_mm=?,z_mm=?,yaw_deg=? WHERE id=?',(*[ch['to'][k]for k in ['x_mm','z_mm','yaw_deg']],ch['fixture_id']))
            bump(c)
        due=payload.get('due_date',t['due_date']) or None
        if due:
            from datetime import date
            date.fromisoformat(due)
        c.execute('UPDATE tasks SET stage=?,owner=?,due_date=?,evidence=?,disposition=?,updated_at=? WHERE id=?',(stage,payload.get('owner',t['owner']),due,evidence,disposition,now(),id))
        if t['scenario_id'] and not c.execute("SELECT 1 FROM tasks WHERE scenario_id=? AND stage!='verified'",(t['scenario_id'],)).fetchone():c.execute("UPDATE scenarios SET status='completed' WHERE id=?",(t['scenario_id'],))
        log(c,actor,'task_update',id,{'from':t['stage'],'to':stage,'evidence':evidence,'disposition':disposition})

def observe(c,payload,actor):
    if actor not in ['merch','manager']:raise PermissionError('Only Merch or a showroom manager records physical observations.')
    if not payload.get('evidence','').strip():raise ValueError('Describe the observation and provide its photo/reference.')
    with transaction(c,payload.get('base_revision')):
        s=state(c);products,variants,slots,placements=indexes(s);sid=payload.get('slot_id');vid=payload.get('variant_id')
        if sid not in slots or vid not in variants:raise ValueError('Unknown slot or product variant.')
        # Reality may differ from the plan, including protected applications. Record it and flag it;
        # design rules must not force staff to falsify what is physically present.
        before=placements[sid];face=payload.get('face_id')
        if face and not any(f['id']==face and f['product_id']==variants[vid]['product_id']for f in s['faces']):raise ValueError('Face/product mismatch.')
        c.execute('UPDATE placements SET variant_id=?,face_id=?,state=?,evidence=?,updated_at=?,revision=revision+1 WHERE slot_id=?',(vid,face,'manager_observed',payload['evidence'],now(),sid))
        bump(c);log(c,actor,'observe',sid,{'before':before,'variant_id':vid,'evidence':payload['evidence']})

EDITABLE={
 'products':['positioning','hit','lifecycle','required','color_group','color_rank','priority_source','notes'],
 'variants':['sku','finish','width_mm','height_mm','thickness_mm','lifecycle','availability'],
 'slots':['visibility_tier','visibility_score','visibility_basis','intentional_repeat'],
 'fixtures':['geometry_verified'],
 'rules':['enabled','parameters_json','status','rationale'],
 'questions':['answer','status','owner','evidence']}

def edit(c,table,records,expected,actor,dry_run=False):
    if table not in EDITABLE:raise ValueError('This table is not directly editable. Import placements as a draft proposal.')
    if actor not in ['merch','designer'] or (actor=='designer' and table not in ['questions','fixtures']):raise PermissionError('Merch owns product and placement guidelines; Design owns fixture evidence.')
    allowed=EDITABLE[table];seen=set()
    with transaction(c,expected):
        for entry in records:
            id=entry.get('id')
            if not id or id in seen:raise ValueError('Missing or duplicate record ID.')
            seen.add(id)
            if not c.execute(f'SELECT 1 FROM {table} WHERE id=?',(id,)).fetchone():raise ValueError('Unknown ID: '+id)
            changes={k:v for k,v in entry.items()if k in allowed}
            if not changes:raise ValueError('No editable fields supplied.')
            for k,v in list(changes.items()):
                if k in ['hit','required','enabled','intentional_repeat','geometry_verified']:
                    if str(v)not in ['0','1']:raise ValueError(k+' must be 0 or 1.')
                    changes[k]=int(v)
                if k in ['color_rank','width_mm','height_mm','thickness_mm','visibility_score']:
                    changes[k]=None if v in ['',None] else float(v)
                    if changes[k]is not None and not math.isfinite(changes[k]):raise ValueError(k+' must be finite.')
                    if k in ['width_mm','height_mm','thickness_mm'] and changes[k] is not None and changes[k]<=0:raise ValueError('Dimensions must be positive millimetres.')
                if k=='sku':changes[k]=str(v).strip()or None
                if k=='lifecycle' and v not in ['active','unconfirmed','discontinued']:raise ValueError('Unknown lifecycle.')
                if k=='availability' and v not in ['unknown','installed_reference','available','unavailable']:raise ValueError('Unknown availability.')
                if k=='parameters_json':
                    params=json.loads(v)
                    if not isinstance(params,dict):raise ValueError('Rule parameters must be a JSON object.')
                    if any(isinstance(x,(int,float))and(not math.isfinite(x)or x<0)for x in params.values()):raise ValueError('Rule numbers must be finite and nonnegative.')
            c.execute(f'UPDATE {table} SET '+','.join(k+'=?'for k in changes)+' WHERE id=?',[*changes.values(),id])
            log(c,actor,'edit_'+table,id,changes)
        if not dry_run:bump(c)
        else:c.rollback()

def export(c):
    s=state(c);destination=ROOT/'web/data';destination.mkdir(parents=True,exist_ok=True)
    s.pop('_product_index',None)
    s['meta'].update(mode='snapshot',exported_at=now())
    (destination/'state.json').write_text(json.dumps(s,ensure_ascii=False,separators=(',',':')))
    out=ROOT/'data/exports';out.mkdir(parents=True,exist_ok=True)
    tables={}
    for table in [*EDITABLE,'placements','tasks']:
        data=rows(c,f'SELECT * FROM {table}')
        fields=['id',*EDITABLE[table]] if table in EDITABLE else list(data[0]) if data else []
        if table=='products':fields=['id','name','family',*EDITABLE[table]]
        if table=='variants':fields=['id','product_id',*EDITABLE[table]]
        if table=='slots':fields=['id','room','title','type','locked','width_mm','height_mm',*EDITABLE[table]]
        if table=='fixtures':fields=['id','room','type','x_mm','z_mm','yaw_deg','width_mm','height_mm','depth_mm','relocatable',*EDITABLE[table]]
        if table=='rules':fields=['id','name','kind','strength','owner',*EDITABLE[table]]
        if table=='questions':fields=['id','team','question','proposed_answer',*EDITABLE[table]]
        tables[table]=[{'base_revision':revision(c),**{k:x[k]for k in fields}}for x in data]
    (out/'tables.json').write_text(json.dumps(tables,ensure_ascii=False,indent=2))
    # Runtime export for the software's repeatable refresh command. Initial human templates
    # are also authored/verified with the workspace spreadsheet artifact tool.
    for table,data in tables.items():
        if not data:continue
        with (out/(table+'.csv')).open('w',newline='',encoding='utf-8-sig')as f:
            writer=csv.DictWriter(f,fieldnames=list(data[0]));writer.writeheader();writer.writerows(data)
    return {'revision':revision(c),'slots':len(s['slots']),'path':str(destination/'state.json')}

def import_csv(c,table,text,actor='merch',dry_run=True):
    data=list(csv.DictReader(io.StringIO(text.lstrip('\ufeff'))))
    if not data:raise ValueError('CSV has no rows.')
    bases={r.pop('base_revision',None)for r in data}
    if len(bases)!=1 or None in bases:raise ValueError('All rows need one matching base_revision.')
    expected=int(next(iter(bases)))
    if expected!=revision(c):raise ValueError('Stale CSV. Export the current revision before editing.')
    if table=='placements':
        s=state(c);_,variants,slots,current=indexes(s);changes=[];seen=set()
        for r in data:
            sid=r.get('slot_id');vid=r.get('variant_id')or None
            if sid in seen or sid not in slots:raise ValueError('Duplicate or unknown slot.')
            seen.add(sid)
            if vid!=current[sid]['variant_id'] or (r.get('face_id')or None)!=current[sid]['face_id']:
                if vid not in variants:raise ValueError('Unknown variant.')
                changes.append(dict(kind='placement',slot_id=sid,from_variant_id=current[sid]['variant_id'],variant_id=vid,face_id=r.get('face_id')or None,reason='Human CSV placement proposal.'))
        validate_changes(s,changes)
        return {'changes':changes,'dry_run':dry_run}if dry_run else {'scenario_id':create_scenario(c,{'base_revision':expected,'changes':changes,'mode':'csv'},actor)}
    edit(c,table,data,expected,actor,dry_run)
    return {'rows':len(data),'dry_run':dry_run,'revision':revision(c)}
