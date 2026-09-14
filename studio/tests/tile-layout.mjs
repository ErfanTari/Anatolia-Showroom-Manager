import assert from 'node:assert/strict';
import fs from 'node:fs';
import {facePool,tileLayout}from'../web/tile-layout.js';
const state=JSON.parse(fs.readFileSync(new URL('../web/data/state.json',import.meta.url)));
const record={product_id:'calacatta-noir',width_m:1.198,height_m:1.198};
const faces=facePool(record,state.faces);
assert.equal(faces.length,20);
assert.ok(faces.every(f=>f.product_id==='calacatta-noir'&&f.width_mm===1200&&f.height_mm===1200));
const args={width:4.65,height:6.718,tileWidth:1.2,tileHeight:1.2,faces,seed:'APS-R2-FLOOR:0'};
const layout=tileLayout(args);
assert.deepEqual(layout,tileLayout(args),'Reload must preserve the layout.');
assert.equal(layout.length,24);
assert.equal(new Set(layout.map(t=>t.face_id)).size,20);
for(const t of layout){
  assert.ok(t.x+t.width<=args.width+1e-8&&t.y+t.height<=args.height+1e-8);
  assert.equal(t.illustrative_cut,false);
  for(const neighbor of layout.filter(n=>(n.row===t.row&&n.col===t.col-1)||(n.col===t.col&&n.row===t.row-1)))assert.notEqual(t.face_id,neighbor.face_id);
  const [x,y,w,h]=t.crop;assert.ok(x>=0&&y>=0&&w>0&&h>0&&x+w<=1+1e-8&&y+h<=1+1e-8);
}
assert.ok(Math.abs(layout.reduce((n,t)=>n+t.width*t.height,0)-args.width*args.height)<1e-8,'Clipped boundary tiles cover the surface exactly.');
const serena=facePool({...record,product_id:'serena-crater'},state.faces);
assert.equal(serena.length,10);assert.ok(serena.every(f=>f.width_mm===1200&&f.height_mm===2800));
const cut=tileLayout({...args,faces:serena});assert.ok(cut.every(t=>t.illustrative_cut&&t.crop[3]<.44));
assert.ok(facePool({...record,product_id:'lithoform-crosscut-dunes'},state.faces).every(f=>!/before_color_match/.test(f.data.source_relative)));
assert.equal(tileLayout({...args,faces:[]}).length,24);
assert.throws(()=>tileLayout({...args,tileWidth:0}),/Positive/);
console.log('Tile layout: 20 Calacatta Noir faces, no adjacent repeats, stable layout, correct edge cuts and labeled slab crops verified.');
