"""Read production-face previews first, original print files only for missing designs.

Never writes to the shared drives. Every published derivative has provenance and a hash.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageStat
import re,json,hashlib,shutil,subprocess,os
ROOT=Path(__file__).resolve().parents[2];STUDIO=ROOT/'studio'
MARKET=Path('/Volumes/CreativeTR/Marketing_Faces/___Low_resolution__Site')
ORIGINAL=Path('/Volumes/CreativeTeam/0000_ORIGINAL_RGB_Files/1.Hat_(160x320_12mm)')
DEST=STUDIO/'web/assets/faces';DEST.mkdir(parents=True,exist_ok=True)
def slug(name):
    name=re.sub(r'\s+Block\s+\d+.*','',name,flags=re.I)
    name=re.sub(r'^(Majesto|Lustra)\s+','',name,flags=re.I)
    name=name.lower().replace('_',' ').replace('tuscano rosso','tuscano burgundy').replace('pietra imperialle','pietra imperiale').replace('statuario extra','statuario').replace('crosscut coas ','crosscut coast ')
    name=re.sub(r'\bgemma bronz\b','gemma bronze',name)
    name=re.sub(r'\bgraphit\b','graphite',name)
    return re.sub(r'[^a-z0-9]+','-',name).strip('-')
manifest=json.loads((STUDIO/'sources/marketing-face-manifest.json').read_text())
out=[];failures=[]
for p in manifest:
    design=slug(p['name'])
    if design in ['serena-base','onyx']:continue # Generic folders don't identify a released color.
    for size in p['sizes']:
        for index,rel in enumerate(size['faces'][:3]):
            src=MARKET/rel
            if not src.exists():continue
            key=hashlib.sha256(rel.encode()).hexdigest()[:16];dest=DEST/(key+'.webp')
            if not dest.exists():shutil.copy2(src,dest)
            try:
                with Image.open(dest) as im:
                    dims=im.size;im=im.convert('RGB');im.thumbnail((32,32));rgb=ImageStat.Stat(im).mean[:3]
                out.append(dict(id='FACE-'+key,design_id=design,width_mm=round(size['width']*10),height_mm=round(size['height']*10),face_index=index+1,path='assets/faces/'+dest.name,source_kind='production marketing derivative',source_relative=rel,pixel_width=dims[0],pixel_height=dims[1],sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),rgb=[round(x)for x in rgb],installed_face_verified=False,available_faces=size['faceCount']))
            except Exception as e:failures.append({'source':rel,'error':str(e)})
print(f'Marketing previews: {len(out)} faces / {len(set(x["design_id"]for x in out))} designs.',flush=True)

# Explicit spelling aliases from the reviewed BOM/portfolio and folder names.
fallback={
'armani-noir':'Armani_Noir_GRA_0024','calacatta-carrara':'Calacatta_Carrera_GRA_0055',
'fusion-white':'Fusion_White_GRA_0072','nero-marquina':'Nero_Marquina_Extra_GRA_0061',
'montagna-jade':'Montagna_Jade_GRA_0068','super-white':'Super_White_GRA_0023',
'calacatta-viola':'Calacatta_Vioala_GRA_0009','cristallo':'Cristallo_Quarzite_GRA_0064',
'marina-white':'Marina_White_GRA_0021','colorado-lincoln':'Colorado_Lincoln(Calacatta_Nero_Borghini)_GRA_0001_2',
'arabescato-vagli':'Arabescato_Vagli_GRA_0007','grigio-quarzo':'Grigio_Quarzo_GRA_0027',
'panda':'Panda_GRA_0015','calacatta-picasso':'Picasso_GRA_0017','montagna-grey':'Montania_Grey_GRA_0003'}
jobs=[]
for design,folder in fallback.items():
    if any(x['design_id']==design for x in out):continue
    candidates=[]
    for d,dirs,files in os.walk(ORIGINAL/folder):
        dirs[:]=[x for x in dirs if not x.startswith('.')]
        for file in files:
            p=Path(d)/file
            if file.startswith('.')or p.suffix.lower()not in ['.tif','.tiff','.jpg','.jpeg','.png']:continue
            candidates.append(p)
    # Prefer a clean production face file over a document/render; otherwise retain a gap.
    candidates=[p for p in candidates if not any(x in str(p).lower() for x in ['render','layout','montaj','label','logo','contact','mood'])]
    candidates.sort(key=lambda p:(p.suffix.lower()not in ['.jpg','.jpeg','.png'],p.stat().st_size,str(p)))
    if candidates:jobs.append((design,candidates[0]))
    else:failures.append({'design':design,'error':'No unambiguous image file found'})

def convert(job):
    design,src=job;rel=src.relative_to(ORIGINAL.parent).as_posix();key=hashlib.sha256(rel.encode()).hexdigest()[:16];dest=DEST/(key+'.webp')
    if not dest.exists():
        result=subprocess.run(['/opt/homebrew/bin/magick','-limit','memory','384MiB','-limit','map','768MiB',str(src)+'[0]','-thumbnail','1024x1024>','-colorspace','sRGB','-strip','-quality','86',str(dest)],capture_output=True,text=True,timeout=240)
        if result.returncode:raise RuntimeError(result.stderr[-500:])
    with Image.open(dest)as im:
        dims=im.size;im=im.convert('RGB');im.thumbnail((32,32));rgb=ImageStat.Stat(im).mean[:3]
    if max(dims)/min(dims)<1.6 or max(dims)/min(dims)>2.2:raise ValueError('Image is not a single slab aspect ratio; manual review required')
    return dict(id='FACE-'+key,design_id=design,width_mm=1600,height_mm=3200,face_index=1,path='assets/faces/'+dest.name,source_kind='original print derivative',source_relative=rel,pixel_width=dims[0],pixel_height=dims[1],sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),rgb=[round(x)for x in rgb],installed_face_verified=False,available_faces=None)
with ThreadPoolExecutor(max_workers=2)as pool:
    futures=[(j,pool.submit(convert,j))for j in jobs]
    for (design,src),future in futures:
        try:out.append(future.result());print('Original fallback:',design,flush=True)
        except Exception as e:failures.append({'design':design,'source':str(src.relative_to(ORIGINAL.parent)),'error':str(e)})
(STUDIO/'sources/face-register.json').write_text(json.dumps({'faces':out,'failures':failures,'policy':'Production design and format references. Exact installed face is unverified. Up to three marketing faces per format plus bounded original fallbacks.'},indent=2))
print(json.dumps({'faces':len(out),'designs':len(set(x['design_id']for x in out)),'fallback_failures':len(failures)},indent=2))
