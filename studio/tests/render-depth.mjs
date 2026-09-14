import {createRequire}from'node:module';
import path from'node:path';
import {homedir}from'node:os';
const require=createRequire(import.meta.url);
const runtime=process.env.STUDIO_NODE_MODULES||path.join(homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const {chromium}=require(require.resolve('playwright',{paths:[runtime]}));
import fs from'node:fs/promises';
import assert from'node:assert/strict';
const url=process.env.STUDIO_URL||'http://127.0.0.1:8765/studio/web/';
const browser=await chromium.launch({headless:true,...(process.env.STUDIO_CHROMIUM?{executablePath:process.env.STUDIO_CHROMIUM}:{})});

const page=await browser.newPage({viewport:{width:1600,height:1050}});
const sub=(a,b)=>a.map((v,i)=>v-b[i]),dot=(a,b)=>a.reduce((n,v,i)=>n+v*b[i],0);
const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const normal=p=>{const n=cross(sub(p[1],p[0]),sub(p[2],p[0])),l=Math.hypot(...n);return n.map(v=>v/l);};
function overlaps(a,b){
 const n=normal(a),m=normal(b);
 if(Math.abs(dot(n,m))<.999999||Math.abs(dot(n,sub(a[0],b[0])))>.001)return false;
 for(const p of [a,b])for(let i=0;i<4;i++){
  const edge=sub(p[(i+1)%4],p[i]),raw=cross(n,edge),l=Math.hypot(...raw),axis=raw.map(v=>v/l);
  const pa=a.map(v=>dot(v,axis)),pb=b.map(v=>dot(v,axis));
  if(Math.min(Math.max(...pa),Math.max(...pb))-Math.max(Math.min(...pa),Math.min(...pb))<.0001)return false;
 }
 return true;
}
try{
 await page.goto(url,{waitUntil:'networkidle'});await page.waitForFunction(()=>window.APS_SIMULATION?.getRenderSurfaces);
 const {planes,tiled}=await page.evaluate(()=>APS_SIMULATION.getRenderSurfaces()),conflicts=[];
 for(let i=0;i<planes.length;i++)for(let j=i+1;j<planes.length;j++)if(overlaps(planes[i].points,planes[j].points))conflicts.push([planes[i].slot_id||planes[i].id,planes[j].slot_id||planes[j].id]);
 assert.deepEqual(conflicts,[],'Overlapping coplanar presentation surfaces');
 for(const s of tiled)assert.ok(Math.abs(s.tile_area+s.grout_area-s.area)<.00002,`${s.key}: grout must occupy only joints, without covering tiles`);
 await fs.mkdir('tmp/source-review',{recursive:true});
 for(const room of [2,3,5]){
  await page.locator(`[data-room="${room}"]`).click();await page.waitForTimeout(2200);
  await page.screenshot({path:`tmp/source-review/room${room}-depth-fixed.png`});
 }
 // Camera motion exercises the depth pass at both close and overview scales.
 await page.locator('#wholeRoom').click();await page.waitForTimeout(2200);
 const canvas=page.locator('#viewport canvas'),r=await canvas.boundingBox();
 await page.mouse.move(r.x+r.width*.6,r.y+r.height*.6);await page.mouse.down();await page.mouse.move(r.x+r.width*.72,r.y+r.height*.53,{steps:24});await page.mouse.up();await page.waitForTimeout(500);
 await page.screenshot({path:'tmp/source-review/overview-depth-fixed.png'});
 console.log(JSON.stringify({planes:planes.length,tiled_surfaces:tiled.length,coplanar_overlaps:conflicts,grout:'joint-only area verified'}));
}finally{await browser.close();}
