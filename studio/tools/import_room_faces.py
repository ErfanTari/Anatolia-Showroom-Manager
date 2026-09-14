"""Add production face sets used by room tiling; never edit placement evidence.

Reads the small shared-drive WebP files. Original/color-match archive folders are
excluded. Missing square face packs may use labeled visual cuts of larger slabs.
"""
from pathlib import Path
import sys,json,re,hashlib,shutil
from PIL import Image,ImageStat
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
from store import connect,now,log
from engine import state
MARKET=Path('/Volumes/CreativeTR/Marketing_Faces/___Low_resolution__Site')

def slug(name):
    name=re.sub(r'\s+Block\s+\d+.*','',name,flags=re.I).lower().replace('_',' ')
    name=name.replace('pietra imperialle','pietra imperiale').replace('statuario extra','statuario')
    name=re.sub(r'\bgemma bronz\b','gemma bronze',name)
    return re.sub(r'[^a-z0-9]+','-',name).strip('-')

def main():
    match=re.search(r'<script id="product-data" type="application/json">(.*?)</script>',(MARKET/'index.html').read_text(),re.S)
    catalog={slug(p['name']):p for p in json.loads(match[1])}
    added=[];summary=[]
    with connect()as c:
        before=[tuple(r)for r in c.execute('SELECT * FROM placements ORDER BY slot_id')]
        variants=c.execute("SELECT DISTINCT v.product_id,v.width_mm,v.height_mm FROM variants v JOIN placements p ON p.variant_id=v.id JOIN slots s ON s.id=p.slot_id WHERE s.type IN ('floor','application')").fetchall()
        selected={}
        for v in variants:
            product=catalog.get(v['product_id']);w,h=v['width_mm'],v['height_mm']
            if not product or not w or not h:continue
            sizes=[s for s in product['sizes']if s['width']*10+25>=w and s['height']*10+25>=h and s['faces'] and 'before_color_match'not in s['faces'][0].lower()]
            if not sizes:continue
            size=min(sizes,key=lambda s:(abs(s['width']*10-w)+abs(s['height']*10-h),s['faces'][0]))
            selected[(v['product_id'],size['faces'][0])]=size
        for (design,_),size in sorted(selected.items()):
            summary.append({'design':design,'format':size['format'],'faces':len(size['faces'])})
            for index,relative in enumerate(size['faces']):
                source=MARKET/relative
                key=hashlib.sha256(relative.encode()).hexdigest()[:16]
                dest=ROOT/'web/assets/faces'/(key+'.webp')
                digest=hashlib.sha256(source.read_bytes()).hexdigest()
                if not dest.exists()or hashlib.sha256(dest.read_bytes()).hexdigest()!=digest:shutil.copy2(source,dest)
                dest.chmod(0o644)
                with Image.open(dest)as im:
                    width,height=im.size;im=im.convert('RGB');im.thumbnail((32,32));rgb=[round(x)for x in ImageStat.Stat(im).mean[:3]]
                face=dict(id='FACE-'+key,design_id=design,width_mm=round(size['width']*10),height_mm=round(size['height']*10),face_index=index+1,path='assets/faces/'+dest.name,source_kind='production marketing derivative',source_relative=relative,pixel_width=width,pixel_height=height,sha256=digest,rgb=rgb,installed_face_verified=False,available_faces=size['faceCount'])
                exists=c.execute('SELECT data_json FROM faces WHERE id=?',(face['id'],)).fetchone()
                if not exists or json.loads(exists[0])!=face:
                    c.execute('INSERT INTO faces VALUES(?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET data_json=excluded.data_json',(face['id'],design,face['width_mm'],face['height_mm'],json.dumps(face)))
                    added.append(face['id'])
        assert before==[tuple(r)for r in c.execute('SELECT * FROM placements ORDER BY slot_id')]
        if added:
            c.execute("INSERT INTO meta VALUES('asset_updated_at',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(now(),))
            log(c,'asset_import','room_face_sets','APS',{'added_or_updated':len(added),'sets':summary,'installed_placements_changed':False})
        c.commit()
        s=state(c);s.pop('_product_index',None);s['meta'].update(mode='snapshot',exported_at=now())
        (ROOT/'web/data/state.json').write_text(json.dumps(s,ensure_ascii=False,separators=(',',':')))
        register=json.loads((ROOT/'sources/face-register.json').read_text())
        register['faces']=[json.loads(r[0])for r in c.execute('SELECT data_json FROM faces ORDER BY id')]
        register['policy']='Production design/format references. Complete available sets for tiled rooms; other displays retain the initial bounded selection. Exact installed faces and cuts unverified.'
        (ROOT/'sources/face-register.json').write_text(json.dumps(register,ensure_ascii=False,indent=2))
        (ROOT/'sources/room-face-sets.json').write_text(json.dumps({'sets':summary,'layout_policy':'Deterministic per-tile distribution, no mirroring or rotation; larger-face crops are illustrative.','placements_changed':False},indent=2))
    print(json.dumps({'added_or_updated_faces':len(added),'sets':summary},indent=2))

if __name__=='__main__':main()
