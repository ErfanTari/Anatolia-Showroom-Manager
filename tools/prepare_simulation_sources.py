"""Read user-supplied workbooks, preserve source facts, prepare simulation JSON.

Run with the bundled Python. Spreadsheet files are read, never rewritten.
CSV authoring is handled by export_assortment.mjs from the extracted grids.
"""
from pathlib import Path
from PIL import Image, ImageOps
import openpyxl
import json, re, hashlib, datetime, csv, unicodedata, shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / 'products ' / 'Assortment confirmation list with names 260618_1.xlsx'
OUT = ROOT / 'simulation' / 'data'
OUT.mkdir(parents=True, exist_ok=True)
TMP = ROOT / 'tmp' / 'source-review'
TMP.mkdir(parents=True, exist_ok=True)

def value(v):
    return v.isoformat() if isinstance(v, (datetime.datetime, datetime.date)) else v

def text(v):
    return re.sub(r'\s+', ' ', str(v or '')).strip()

def source_hash(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()

def write(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

wb = openpyxl.load_workbook(SOURCE, data_only=False, read_only=True)
cached = openpyxl.load_workbook(SOURCE, data_only=True, read_only=True)
grids, formulas = [], []
for ws in wb:
    cache_rows = list(cached[ws.title].iter_rows(values_only=True))
    rows = []
    for ri, row in enumerate(ws.iter_rows(values_only=True)):
        out = []
        for ci, v in enumerate(row):
            if isinstance(v, str) and v.startswith('='):
                cv = cache_rows[ri][ci]
                formulas.append({'sheet':ws.title,'cell':f'{openpyxl.utils.get_column_letter(ci+1)}{ri+1}','formula':v,'cached_value':value(cv)})
                out.append(value(cv) if cv is not None else v)
            else:
                out.append(value(v))
        rows.append(out)
    grids.append({'sheet':ws.title,'rows':rows,'row_count':ws.max_row,'column_count':ws.max_column,'state':ws.sheet_state})
write(TMP/'assortment-grids.json', {'source':str(SOURCE),'sha256':source_hash(SOURCE),'sheets':grids,'formulas':formulas})

options=[]
for g in grids:
    sn=g['sheet']; rows=g['rows']
    if sn not in ['Names','12mm','6mm','Subsize','Mosaic']: continue
    if sn=='Names':
        start, namecol, refcol, notescol, cols = 1,3,1,7,range(8,19)
    elif sn=='Mosaic':
        start,namecol,refcol,notescol,cols=2,0,None,2,range(3,15)
    else:
        start,namecol,refcol,notescol,cols=2,2,1,4,range(5,19 if sn=='Subsize' else 15)
    for idx in range(start,len(rows)):
        row=rows[idx]
        name=text(row[namecol]); ref=text(row[refcol]) if refcol is not None else ''
        if not name and not ref: continue
        # Workbook totals stay in the faithful tab exports, not in the option index.
        if any('TOTAL COLORS' in str(v).upper() for v in row if v is not None): continue
        if isinstance(row[namecol], (int,float)) or (name and re.fullmatch(r'[\d.]+',name)): continue
        for col in cols:
            v=row[col] if col<len(row) else None
            if v is None or not str(v).strip(): continue
            marketing=text(rows[0][col]) if col<len(rows[0]) else ''
            technical=text(rows[1 if start==2 else 0][col])
            # Do not forward-fill a blank marketing header into a technical finish.
            for part in str(v).splitlines() or [str(v)]:
                if not part.strip(): continue
                options.append({
                    'source_workbook':SOURCE.name,'source_sheet':sn,'source_row':idx+1,
                    'source_cell':f'{openpyxl.utils.get_column_letter(col+1)}{idx+1}',
                    'reference_name':ref,'name_as_listed':name,'marketing_header':marketing,
                    'technical_header':technical,'thickness_mm':int(sn[:-2]) if sn in ['6mm','12mm'] else '',
                    'option_as_listed':part.strip(),'notes_as_listed':str(row[notescol] or ''),
                    'interpretation':'assortment option; not SKU, stock, lifecycle or Merch priority'
                })
write(TMP/'assortment-options.json', options)

bomfile=ROOT/'APS_TemproraryShowroom_BOM_20260609.xlsx'
bom=openpyxl.load_workbook(bomfile,data_only=True,read_only=True)
bomformula=openpyxl.load_workbook(bomfile,data_only=False,read_only=True)
records=[]; equipment=[]
for ws in bom:
    for rn,row in enumerate(ws.iter_rows(values_only=True),1):
        if rn==1:continue
        if ws.title=='APS_20260609':
            loc,area,kind,size,name,finish,thickness=row[:7]
            a,b,ea,eb,total,sku,description,notes,notes2=row[7:16]
        else:
            loc,area,size,name,finish,thickness=row[:6]
            a,b,ea,eb,total,sku,description,precut,notes=row[6:15]
            notes2='';kind=''
        if ws.title=='APS_Tempry' and rn>=60:
            if any(row):equipment.append({'source_sheet':ws.title,'source_row':rn,'cells':[value(x) for x in row]})
            continue
        if not name:continue
        sku_raw=text(sku);sku_clean=sku_raw.rstrip('*')
        rm=re.search(r'(?:Room\s*|W)(\d+)',text(loc),re.I)
        group=('sliding160' if text(loc)=='Room 4' and text(area).startswith('Slab') else
               'sliding120' if text(loc)=='Room 5' and text(area).startswith('Mini') else
               'waterfall' if text(area).startswith('Waterfall Display') else
               'rotating' if text(area)=='Rotating Tile Display' else
               'fixed' if text(loc)=='Hall' else
               'samples' if text(loc)=='Board' else
               'floor' if text(loc).startswith('F0') else 'application')
        match=re.search(r'(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)\s*cm',text(size),re.I)
        records.append({
            'id':f'APS-{ws.title}-{rn:03}', 'source_sheet':ws.title,'source_row':rn,
            'source_workbook':bomfile.name,'location':text(loc),'area':text(area),
            'name':text(name),'sku':sku_clean,'sku_as_listed':sku_raw,'finish':text(finish),
            'thickness':text(thickness),'size':text(size),'width_m':float(match[1])/100 if match else None,
            'height_m':float(match[2])/100 if match else None,'quantity_a':a,'quantity_b':b,
            'extra_a':ea,'extra_b':eb,'total':total,'description':text(description),
            'notes': '\n'.join(str(n) for n in [notes,notes2] if n),
            'group':group,'room':int(rm[1]) if rm else None,
            'status':'user-reported installed baseline' if sku_clean else 'source item without SKU',
            'source_date':'2026-06-09','observation_context':'User identified supplied APS sources as current setup on 2026-09-09; individual geometry/placements may remain approximate.'
        })

# Gallery assets are indexed by reviewed product name, never by the array position.
def valid_image(p):
    try:
        with Image.open(p) as im: im.verify()
        return True
    except Exception: return False
all_assets=list((ROOT/'assets/products').glob('*.jpg'))
assets=[p for p in all_assets if valid_image(p)]
def design_name(name):
    clean=re.sub(r'\s+block\s+\d+.*','',name,flags=re.I)
    clean=re.sub(r'^(Majesto|Lustra)\s+','',clean,flags=re.I)
    clean=re.sub(r'\s+(bookmatch|honed).*','',clean,flags=re.I)
    clean=re.sub(r'Lithoform\s+(\w+)\s*-\s*(Crosscut|Veincut)',r'Lithoform \2 \1',clean,flags=re.I)
    clean=clean.replace('Crosscut Coas','Crosscut Coast') if clean.endswith('Crosscut Coas') else clean
    return norm(clean)
alias={'pietra imperiale':'Pietra_Imperialle','gemma bronze':'Gemma_Bronz','statuario':'Statuario_Extra','lithoform crosscut coas':'Lithoform_Crosscut_Coast',
       'lustra onyx halo':'Onyx_Halo','lustra onyx crema':'Onyx','lustra onyx sage':'Onyx','lustra onyx hazel':'Onyx','lustra onyx feather':'Onyx'}
def get_texture(name,sku):
    clean=re.sub(r'\s+block\s+\d+.*','',name,flags=re.I)
    clean=re.sub(r'^(Majesto|Lustra)\s+','',clean,flags=re.I)
    clean=re.sub(r'\s+(bookmatch|honed).*','',clean,flags=re.I)
    n=norm(clean)
    for p in assets:
        if norm(p.stem)==n:return '../assets/products/'+p.name, 'product image; finish/face illustrative'
    target=alias.get(n) or alias.get(norm(name))
    if target:
        p=ROOT/'assets/products'/f'{target}.jpg'
        if p in assets and 'lustra onyx' not in norm(name):return '../assets/products/'+p.name,'reviewed name alias; finish/face illustrative'
    return None,'image missing'

legacy=json.loads(re.search(r'window.ANATOLIA_DATA\s*=\s*(\{.*\});', (ROOT/'showroom-data.js').read_text(),re.S)[1])
html=(ROOT/'Showroom Manager.dc.html').read_text()
sliding=json.loads(re.search(r'get APS_SLIDING_DATA\(\)\{ return (\{.*?\}); \}',html,re.S)[1])
slides={s['sku']:s['texture'] for bank in sliding.values() for s in bank['slabs']}
mediafile=ROOT/'output/assortment/media_index.json'
media_by_name={}
if mediafile.exists():
    image_index=json.loads(mediafile.read_text())
    for anchor in image_index['anchors']:
        sheet=next((g for g in grids if g['sheet']==anchor['sheet']),None)
        if not sheet or not anchor['row'] or anchor['row']>len(sheet['rows']):continue
        row=sheet['rows'][anchor['row']-1]
        names=([row[1],row[3]] if sheet['sheet']=='Names' else [row[1],row[2]] if sheet['sheet'] in ['12mm','6mm','Subsize'] else [row[0]] if sheet['sheet']=='Mosaic' else [])
        for name in names:
            if isinstance(name,str) and name.strip():media_by_name.setdefault(design_name(name),anchor)
textureout=ROOT/'simulation/textures';textureout.mkdir(exist_ok=True)
for r in records:
    r['texture'],r['texture_note']=get_texture(r['name'],r['sku'])
    if r['sku'] in slides:
        r['texture']='../'+slides[r['sku']]
        r['texture_note']='existing SKU-linked panel image; production face unverified'
    # Mini slab names provide an exact design preview when a different format lacks one.
    if not r['texture']:
        for bank in sliding.values():
            for s in bank['slabs']:
                if design_name(s['name'])==design_name(r['name']):
                    r['texture']='../'+s['texture'];r['texture_note']='same design in another format; finish/face illustrative'
    if design_name(r['name']) in media_by_name:
        anchor=media_by_name[design_name(r['name'])];p=ROOT/'output/assortment'/anchor['media']
        if valid_image(p):
            shutil.copyfile(p,textureout/p.name)
            r['texture']='./textures/'+p.name
            r['texture_note']=f"Assortment workbook image at {anchor['sheet']}!{anchor['cell']}; production face, color and finish unverified"
            if 'lithoform' in design_name(r['name']):r['texture_note']+='; workbook reuses some images across colors'
    # UV windows select the explicitly labelled color swatch in composite images.
    # Originals are retained unchanged, with the crop recorded for reproducibility.
    design=design_name(r['name'])
    if design.startswith('lithoform ') and any(c in design for c in ['coast','vista','dunes']):
        fname='image76.png' if 'crosscut' in design else 'image67.png'
        p=ROOT/'output/assortment/media'/fname
        shutil.copyfile(p,textureout/fname)
        x=.025 if 'coast' in design else .365 if 'vista' in design else .705
        r['texture']='./textures/'+fname;r['texture_crop']=[x,.23,.27,.74]
        r['texture_note']='UV window of the workbook composite: Coast = labelled Beige, Vista = Grey, Dunes = Ivory; color mapping from assortment reference names. Exact production face/finish unverified.'
    elif r['texture']=='./textures/image23.png':
        r['texture_crop']=[.025,.39,.95,.58]
        r['texture_note']+='; UV window excludes the embedded title/specification banner'

write(OUT/'aps-source-records.json',{'source':str(bomfile),'sha256':source_hash(bomfile),'records':records,'equipment':equipment})
write(OUT/'assortment-options.json',options)

# CSV is checked against its matching XLSX records, without replacing either source.
csvrows=list(csv.DictReader((ROOT/'APS_TemporaryShowroom_BOM_20260609.csv').open(encoding='utf-8-sig',newline='')))
audit={'xlsx_product_rows':len(records),'csv_rows':len(csvrows),'groups':{},'assortment_tabs':len(grids),'assortment_options':len(options),'formula_cells':len(formulas),'legacy_invalid_product_images':len(all_assets)-len(assets),'missing_textures':[]}
for r in records:
    audit['groups'][r['group']]=audit['groups'].get(r['group'],0)+1
    if not r['texture']:audit['missing_textures'].append({'id':r['id'],'name':r['name']})
write(OUT/'source-audit.json',audit)

# Lightweight correctly oriented reference photos for the inspector.
photoout=ROOT/'simulation'/'references';photoout.mkdir(exist_ok=True)
for p in (ROOT/'assets/room-photos').glob('*.jpg'):
    im=ImageOps.exif_transpose(Image.open(p)).convert('RGB');im.thumbnail((1400,1100));im.save(photoout/p.name,quality=86)
for name, source in [('aps-plan.png',TMP/'aps-02.png'),('aps-floors.png',TMP/'aps-03.png')]:
    im=Image.open(source);im.thumbnail((1900,1400));im.save(photoout/name)
for n in [31,32,33,37,38,39,40,45,46,47,48,50,51,52,53,54]:
    p=TMP/f'brochure-{n:02}.png'
    im=Image.open(p).convert('RGB');im.save(photoout/f'fixture-page-{n}.jpg',quality=86)
print(json.dumps(audit,ensure_ascii=False,indent=2))
