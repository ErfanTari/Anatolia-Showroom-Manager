"""Build the reviewable APS fixture/slot manifest from the extracted BOM."""
from pathlib import Path
import json, re

root=Path(__file__).resolve().parents[1]
src=json.loads((root/'simulation/data/aps-source-records.json').read_text())
records=src['records']
group=lambda name:[r for r in records if r['group']==name]
rooms=[
 dict(id=1,name='Bathroom',subtitle='Pietra Imperiale · Arabescato Corchia',bounds=[4.95,9.76,12.5,13.438],photo='room1-1c.jpg',floor_row=3),
 dict(id=2,name='Living space',subtitle='Calacatta Noir · Travertino Titanium',bounds=[0,6.72,4.65,13.438],photo='room2-2a.jpg',floor_row=4),
 dict(id=3,name='Meeting room',subtitle='Oro Noir table · Lithoform Vista',bounds=[0,0,4.65,6.72],photo='room3-perspective.jpg',floor_row=5),
 dict(id=4,name='Slab gallery',subtitle='24 sliding slabs · sample library',bounds=[4.95,0,12.5,3.678],photo='room4-sliding-panel-a.jpg',floor_row=2),
 dict(id=5,name='Mini slab gallery',subtitle='24 sliding panels · Taj Mahal',bounds=[16.5,0,24.05,3.678],photo='room5-sliding-panel-b-3.jpg',floor_row=2),
 dict(id=6,name='Waterfall gallery',subtitle='21 panels · seven three-panel modules',bounds=[24.35,0,29,6.72],photo='room6-6d-waterfall.jpg',floor_row=2),
 dict(id=7,name='Kitchen',subtitle='Verdi Alpi island · Travertino Classico',bounds=[24.35,6.72,29,13.438],photo='room7-furniture.jpg',floor_row=6),
 dict(id=8,name='Tile library',subtitle='20 rotating faces · subsize displays',bounds=[16.5,9.76,24.05,13.438],photo='room8-rotating-panels.jpg',floor_row=2),
]
fixtures=[]
for rn,gname,width in [(4,'sliding160',1.6),(5,'sliding120',1.2)]:
    ordered=sorted(group(gname),key=lambda r:int(re.search(r'\d+',r['area'])[0]))
    center=8.72 if rn==4 else 20.28
    for i,r in enumerate(ordered):
        side=i//12;j=i%12
        fixtures.append(dict(id=f'APS-R{rn}-SL-{i+1:02}',type='sliding',room=rn,
            x=center+(-2.48+j*.175 if side==0 else .555+j*.175),z=.9,
            yaw=45 if side==0 else -45,width=width,height=3.2 if rn==4 else 2.8,
            unit=side+1,position=i+1,front=r['id'],back=None,
            source='BOM numbered positions; mirrored fixture geometry from brochure pp. 45–48',
            uncertainty='Bank location approximated from APS plan; travel/pivots are illustrative.'))

# Page 2 assigns Calacatta Noir to the two central upper fronts, and Macchia
# Vecchia to the two central lower backs. Their BOM quantities are two each.
# The old viewer duplicated Viola/Cremo instead; do not carry that mapping over.
pairs=[[(0,22),(1,21),(2,20),(3,19),(4,18),(5,17)],
       [(5,16),(6,15),(7,14),(8,13),(9,12),(10,11)],
       [(23,45),(24,44),(25,43),(26,42),(27,41),(28,40)],
       [(29,40),(30,39),(31,38),(32,37),(33,36),(34,35)]]
fixed=group('fixed')
for bank,row in enumerate(pairs):
    for j,(a,b) in enumerate(row):
        fixtures.append(dict(id=f'APS-H-FX-{bank*6+j+1:02}',type='fixed',room=0,
            x=(6.35 if bank%2==0 else 15.85)+j*1.36,z=5.45 if bank<2 else 8.0,
            yaw=(45 if j%2==0 else -45)*(1 if bank<2 else -1),width=1.6,height=3.2,
            front=fixed[a]['id'],back=fixed[b]['id'],
            source='APS drawing p. 2 face sequence, reconciled with BOM quantities',
            uncertainty='Panel centerpoints/angles traced approximately; installed face orientation needs a numbered site walk.'))

for i,r in enumerate(group('waterfall')):
    if i<9:x,z,yaw=28.64,1.15+i*.58,-90
    elif i<15:x,z,yaw=26.65,1.9+(i-9)*.58,90
    else:x,z,yaw=26.32,1.9+(i-15)*.58,-90
    fixtures.append(dict(id=f'APS-R6-WF-{i+1:02}',type='waterfall',room=6,x=x,z=z,yaw=yaw-9,
        width=.6,height=2.8,front=r['id'],back=None,position=i+1,
        source='BOM waterfall sequence and brochure pp. 31–33',
        uncertainty='Six central positions per side and nine wall positions; local angle/spacing approximated.'))

rot=group('rotating')
for unit in range(2):
    for j in range(5):
        fixtures.append(dict(id=f'APS-R8-RT-{unit+1}-{j+1}',type='rotating',room=8,
            x=22.6 if unit==0 else 17.95,z=12.4-j*.11,yaw=0,width=1.2,height=1.2,
            unit=unit+1,position=j+1,front=rot[unit*10+j]['id'],back=rot[unit*10+5+j]['id'],
            source='BOM row 71/81: first five front, next five back; brochure p. 51, 9902-3105-0',
            uncertainty='Frame envelope 1.565 × 0.68 × 1.495 m; pull-out stroke and hinge motion are illustrative.'))

data=dict(version=1,showroom_id='APS',name='APS Temporary Showroom',source_sha256=src['sha256'],
    coordinate_system='metres; x left-to-right, z top-to-bottom on APS plan; Y up in renderer',
    footprint=dict(width=29,depth=13.438,corridor_width=4,source='APS drawing p. 2, dimensions in cm converted to m'),
    rooms=rooms,fixtures=fixtures,
    assumptions=[
        'User identifies APS drawing/BOM/photos as the current setup. No new site survey has been performed.',
        'Overall plan dimensions are from the drawing; internal positions are approximate traces, not CAD survey coordinates.',
        'Default wall height 3.2 m, furniture shapes from photos. Meeting tabletop 1.25 × 2.80 m from BOM.',
        'Kitchen slab identity follows user/photo description; exact SKU and fabricated dimensions are not supplied.',
        'Textures show product designs. Production faces, finish response, lighting and bookmatch are illustrative.',
        'W9F entries lack SKUs and retain approval/production notes; excluded from installed 3D surfaces.',
        'Sample tower capacity is 75; individual installed chips are not enumerated in the supplied BOM.',
        'Brochure p. 50 thickness says 8–10 cm; conflicts with APS 9 mm. Not adopted as a mounting constraint.',
        'This review model does not certify circulation, mounting, load capacity or fabrication fit.',
    ])
(root/'simulation/data/scene-manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
assert len(fixtures)==103
assert len({f['id'] for f in fixtures})==len(fixtures)
from collections import Counter
actual=Counter(s for f in fixtures if f['type']=='fixed' for s in (f['front'],f['back']))
assert actual==Counter({r['id']:r['quantity_a']+r['quantity_b'] for r in fixed})
print(f'{len(fixtures)} fixtures; 24 fixed panels / 48 faces match BOM quantities; all IDs unique.')
