"""Validate source preservation, fixture quantities and every placed image."""
from pathlib import Path
from collections import Counter
from PIL import Image
import csv,json
root=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((root/p).read_text())
source=load('simulation/data/aps-source-records.json')
manifest=load('simulation/data/scene-manifest.json')
byid={r['id']:r for r in source['records']}
assert len(byid)==188
assert len({f['id']for f in manifest['fixtures']})==103
assert Counter(f['type']for f in manifest['fixtures'])=={'sliding':48,'fixed':24,'waterfall':21,'rotating':10}
for f in manifest['fixtures']:
    for side in ['front','back']:
        if f[side]:assert f[side] in byid,f
for rn in [4,5]:
    bank=[f for f in manifest['fixtures'] if f['type']=='sliding' and f['room']==rn]
    assert sorted(f['position'] for f in bank)==list(range(1,25))
    assert len({f['front'] for f in bank})==24
fixed=Counter(f[side]for f in manifest['fixtures']if f['type']=='fixed'for side in ['front','back'])
assert fixed==Counter({r['id']:r['quantity_a']+r['quantity_b']for r in byid.values()if r['group']=='fixed'})
for f in [f for f in manifest['fixtures']if f['type']=='rotating']:
    assert byid[f['back']]['source_row']-byid[f['front']]['source_row']==5
for r in byid.values():
    if r['location']=='W9F':continue
    assert r['texture'],r['id']
    with Image.open(root/'simulation'/r['texture']) as im:im.verify()
    if 'texture_crop'in r:
        x,y,w,h=r['texture_crop'];assert min(x,y)>=0 and min(w,h)>0 and x+w<=1 and y+h<=1
g=load('tmp/source-review/assortment-grids.json');exports=load('output/assortment/manifest.json')
def cell(v):
    if v is None:return ''
    if isinstance(v,bool):return 'TRUE'if v else 'FALSE'
    return str(v)
for sheet,export in zip(g['sheets'],exports['sheets']):
    with (root/'output/assortment'/export['csv']).open(encoding='utf-8-sig',newline='')as f:actual=list(csv.reader(f))
    expected=[[cell(v) for v in row]for row in sheet['rows']]or[['']]
    assert actual==expected,sheet['sheet']
assert len(exports['sheets'])==9
assert len(load('output/assortment/formula_metadata.json'))==57
key=lambda a,b,c,d:tuple(' '.join(str(v or '').split())for v in [a,b,c,d])
with (root/'APS_TemporaryShowroom_BOM_20260609.csv').open(encoding='utf-8-sig',newline='')as f:csvrows=list(csv.DictReader(f))
a=Counter(key(r['location'],r['name'],r['sku_as_listed'],r['size'])for r in byid.values())
b=Counter(key(r['Location'],r['Product/Colour'],r['Product No'],r['Size'])for r in csvrows)
assert not a-b
assert sum((b-a).values())==9
print('PASS: 188 source rows, 103 fixtures, 48 fixed faces, rotating front/back pairs, all placed images, 9 CSV tab grids, 57 formulas, and APS CSV/XLSX reconciliation.')
