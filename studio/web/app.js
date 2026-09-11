import * as THREE from 'three';
import { OrbitControls } from './vendor/OrbitControls.js';

const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
import {state,recordFor,replaceState} from './state.js';
const source={...state.source,records:state.source.records.map(r=>{const d=recordFor(r.sku?'SKU-'+r.sku:'SOURCE-'+r.id);return {...r,texture:d?.texture||r.texture,texture_crop:d?d.texture_crop:r.texture_crop,texture_note:d?.texture_note||r.texture_note};})};
const manifest={...state.showrooms[0].geometry,fixtures:state.fixtures.map(f=>({...f.extra,x:f.x_mm/1000,z:f.z_mm/1000,yaw:f.yaw_deg,width:f.width_mm/1000,height:f.height_mm/1000}))};
const portfolio=state.portfolio;
const records=new Map(source.records.map(r=>[r.id,r]));
for(const v of state.variants)records.set(v.id,recordFor(v.id));
for(const a of state.placements)if(a.variant_id)records.set('PLACEMENT-'+a.slot_id,recordFor(a.variant_id,a.face_id));
const slots=new Map(), fixtures=new Map(), pickable=[], labels=[], animated=[];
const studies=new Map();
let selected=null, activeRoom=0, view='orbit', catalog='installed', targetCamera=null;
const container=$('#viewport');
const scene=new THREE.Scene();scene.background=new THREE.Color('#eae9e2');
const camera=new THREE.PerspectiveCamera(42,1,.05,250);
let renderer;
try{renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'high-performance'});}catch(error){
  $('#loading').hidden=true;$('#sceneError').hidden=false;$('#sceneError').textContent='The 3D view needs WebGL. Open this page in a browser with graphics acceleration enabled. Source files and CSV exports remain available.';throw error;
}
renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;
container.appendChild(renderer.domElement);
const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.07;controls.minDistance=1.2;controls.maxDistance=75;controls.maxPolarAngle=Math.PI*.49;
controls.addEventListener('start',()=>targetCamera=null);
scene.add(new THREE.HemisphereLight('#fffaf0','#b5b6a0',2.7));
const sun=new THREE.DirectionalLight('#fff9e9',3.6);sun.position.set(-12,28,10);sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.left=-25;sun.shadow.camera.right=25;sun.shadow.camera.top=22;sun.shadow.camera.bottom=-22;sun.shadow.normalBias=.035;sun.shadow.bias=-.00015;scene.add(sun);
const fill=new THREE.DirectionalLight('#edf2ff',1.6);fill.position.set(20,15,-18);scene.add(fill);
const building=new THREE.Group();building.position.set(-14.5,0,-6.719);scene.add(building);
const walls=new THREE.Group();building.add(walls);
const labelGroup=new THREE.Group();building.add(labelGroup);
const colors={metal:'#393d33',wood:'#554638',stone:'#e8e6dc',chair:'#a39e8b',trim:'#b1a287'};
const plain=c=>new THREE.MeshStandardMaterial({color:c,roughness:.8});
const metal=plain(colors.metal), wood=plain(colors.wood), ivory=plain('#ebe9df'), black=plain('#222720');
const materialCache=new Map(), textureCache=new Map(), imageSources=new Map();
const imageKey=r=>`${r?.texture||''}:${(r?.texture_crop||[]).join(',')}`;
const imageRecords=[...new Map([...records.values()].filter(r=>r.texture).map(r=>[imageKey(r),r])).values()];
await Promise.all(imageRecords.map(async r=>{
  const im=new Image();im.src=r.texture;try{await im.decode();}catch{console.warn('Preview unavailable',r.id);return;}
  if(r.texture_crop){const [x,y,w,h]=r.texture_crop;const c=document.createElement('canvas');c.width=Math.round(im.width*w);c.height=Math.round(im.height*h);c.getContext('2d').drawImage(im,x*im.width,y*im.height,w*im.width,h*im.height,0,0,c.width,c.height);imageSources.set(imageKey(r),c);}else imageSources.set(imageKey(r),im);
}));
function preview(r){const im=imageSources.get(imageKey(r));return im instanceof HTMLCanvasElement?im.toDataURL('image/jpeg',.9):r.texture;}
function texture(record){if(!record?.texture)return null;const key=imageKey(record);if(!textureCache.has(key)){const loaded=imageSources.get(key);const t=loaded?new THREE.Texture(loaded):new THREE.TextureLoader().load(record.texture);t.needsUpdate=true;t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());textureCache.set(key,t);}return textureCache.get(key);}
function material(record,repeatX=1,repeatY=1){
  const key=`${record?.id||'blank'}:${imageKey(record)}:${repeatX.toFixed(2)}:${repeatY.toFixed(2)}`;
  if(materialCache.has(key))return materialCache.get(key);
  let map=texture(record);
  if(map&&(repeatX!==1||repeatY!==1)){map=map.clone();map.wrapS=map.wrapT=THREE.RepeatWrapping;map.repeat.set(repeatX,repeatY);map.needsUpdate=true;}
  const m=new THREE.MeshStandardMaterial({map,color:map?'#ffffff':'#dbd9cb',roughness:/polish/i.test(record?.finish)? .32:.75,metalness:.015,side:THREE.DoubleSide});
  materialCache.set(key,m);return m;
}
function box(w,h,d,x,y,z,mat=ivory,parent=building){const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;}
function plane(w,h,x,y,z,mat,parent=building){const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),mat);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;}
function cyl(radius,height,x,y,z,mat=metal,parent=building,top=radius){const m=new THREE.Mesh(new THREE.CylinderGeometry(top,radius,height,24),mat);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;}
function sphere(radius,x,y,z,mat,parent=building){const m=new THREE.Mesh(new THREE.SphereGeometry(radius,20,14),mat);m.position.set(x,y,z);m.castShadow=true;parent.add(m);return m;}
function rod(a,b,r=.025,mat=metal,parent=building){const p=new THREE.Vector3(...a),q=new THREE.Vector3(...b),d=q.clone().sub(p);const m=cyl(r,d.length(),...p.clone().add(q).multiplyScalar(.5).toArray(),mat,parent);m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());return m;}
function register(id,recordId,room,title,meta={}){if(slots.has(id))return slots.get(id);const a=state.placements.find(a=>a.slot_id===id);const row=state.slots.find(s=>s.id===id);if(!row)throw Error('Geometry has an unregistered slot: '+id);const s={id,recordId:a?.variant_id,record:records.get('PLACEMENT-'+id),room,title:row.title,meshes:[],...meta};slots.set(id,s);return s;}
function bind(mesh,slot){const current=mesh.material;const m=material(slot.record).clone();if(current.map?.repeat&&(current.map.repeat.x!==1||current.map.repeat.y!==1)&&m.map){m.map=m.map.clone();m.map.repeat.copy(current.map.repeat);m.map.wrapS=m.map.wrapT=THREE.RepeatWrapping;}m.side=current.side;mesh.material=m;mesh.userData.slotId=slot.id;slot.meshes.push(mesh);pickable.push(mesh);return mesh;}
function appliedBox(w,h,d,x,y,z,slot,parent=building){return bind(box(w,h,d,x,y,z,material(slot.record),parent),slot);}
function surface(w,h,x,y,z,slot,yaw=0,parent=walls,repeat=false){const m=plane(w,h,x,y,z,material(slot.record,repeat?w/(slot.record?.width_m||1.6):1,repeat?h/(slot.record?.height_m||3.2):1),parent);m.rotation.y=yaw;return bind(m,slot);}
function sourceRecord(row){return `APS-APS_Tempry-${String(row).padStart(3,'0')}`;}
function appSlot(row,room,title){return register(`APS-R${room}-APP-${row}`,sourceRecord(row),room,title,{type:'application',source:'APS BOM · APS_Tempry',uncertainty:'Surface extents reconstructed from the APS drawing and room photographs.'});}
function label(text,x,z,scale=1){
  const point=new THREE.Object3D();point.position.set(x,3.6,z);labelGroup.add(point);
  const element=document.createElement('div');element.className='room-tag';element.textContent=text;container.appendChild(element);labels.push({point,element});return point;
}

// The plan coordinate system is preserved throughout, then translated once for orbiting.
box(30.2,.22,14.6,14.5,-.18,6.719,plain('#d5d5c8'));
const courtyard=box(4,.025,13.438,14.5,-.02,6.719,plain('#d4d6c9'));
for(const room of manifest.rooms){
  const [x1,z1,x2,z2]=room.bounds,w=x2-x1,d=z2-z1;
  const s=register(`APS-R${room.id}-FLOOR`,sourceRecord(room.floor_row),room.id,`${room.name} floor`,{type:'floor',uncertainty:'Zone boundary traced from floor plan; texture is representative.'});
  const m=plane(w,d,(x1+x2)/2,.014,(z1+z2)/2,material(s.record,w/(s.record?.width_m||1.2),d/(s.record?.height_m||1.2)));m.rotation.x=-Math.PI/2;bind(m,s);
  // Fine joints are explicit geometry so the tile scale is readable in the model.
  const tile=s.record?.width_m||1.2;
  for(let x=x1+tile;x<x2-.05;x+=tile)box(.009,.006,d,x,.018,(z1+z2)/2,plain('#a3a597'));
  for(let z=z1+tile;z<z2-.05;z+=tile)box(w,.006,.009,(x1+x2)/2,.018,z,plain('#a0a194'));
  label(`${String(room.id).padStart(2,'0')}  ${room.name.toUpperCase()}`,(x1+x2)/2,(z1+z2)/2);
}
for(const [x1,x2] of [[4.95,12.5],[16.5,24.05]]){
  const m=plane(x2-x1,6.082,(x1+x2)/2,.014,6.719,material(records.get(sourceRecord(2)),(x2-x1)/1.198,6.082/1.198));m.rotation.x=-Math.PI/2;
  bind(m,register(`APS-H-FLOOR-${x1}`,sourceRecord(2),0,'Fixed gallery floor',{type:'floor'}));
}
label('ANATOLIA  /  APS',14.5,12.4,.85);
// Back and end walls; entrance edge is cut away for legibility.
for(const [x1,x2]of[[0,12.5],[16.5,29]]){box(x2-x1,3.2,.16,(x1+x2)/2,1.6,.08,ivory,walls);box(x2-x1,.65,.14,(x1+x2)/2,.325,13.37,ivory,walls);}
for(const x of[.08,28.92])box(.16,3.2,13.438,x,1.6,6.719,ivory,walls);
for(const x of[4.8,24.2])for(const [z,d]of[[.82,1.64],[6.72,.8],[12.61,1.64]])box(.3,3.2,d,x,1.6,z,ivory,walls);
for(const x of[2.35,26.7])box(4.7,2.9,.18,x,1.45,6.72,ivory,walls);
for(const x of[8.72,20.28])for(const z of[3.57,9.87])box(3.2,3.2,.20,x,1.6,z,ivory,walls);
for(const x of[12.35,16.65])for(const z of[.83,12.6])box(.3,3.2,1.66,x,1.6,z,ivory,walls);
// A recessed plinth beneath each fixed display keeps the frame distinct from the slab.
for(const f of manifest.fixtures){
  const g=new THREE.Group();g.position.set(f.x,0,f.z);g.rotation.y=THREE.MathUtils.degToRad(f.yaw);building.add(g);
  const obj={definition:f,group:g,open:0,target:0,face:'front',slots:[]};fixtures.set(f.id,obj);
  const moving=new THREE.Group();g.add(moving);obj.moving=moving;
  let height=f.height,cy=height/2+.08,parent=moving;
  if(f.type==='fixed'){
    box(1.45,.08,.22,0,.04,0,metal,g);box(.035,3.2,.065,-.735,1.65,0,metal,g);box(.035,3.2,.065,.735,1.65,0,metal,g);
  }else if(f.type==='sliding'){
    box(f.width+.04,.08,.10,0,.055,0,metal,moving);box(f.width+.04,.045,.09,0,height+.1,0,metal,moving);
    box(.035,height,.07,-f.width/2-.025,cy,0,metal,moving);box(.035,height,.07,f.width/2+.025,cy,0,metal,moving);
    box(.045,.04,1.7,0,.04,-.3,metal,g);animated.push(obj);
  }else if(f.type==='waterfall'){
    box(.64,2.936,.045,0,1.468,0,wood,g);box(.64,.06,.205,0,.03,0,wood,g);cy=1.48;
  }else{
    const pivot=new THREE.Group();pivot.position.y=1.39;moving.add(pivot);obj.pivot=pivot;parent=pivot;cy=-.6;
    box(1.24,1.24,.032,0,cy,0,metal,pivot);animated.push(obj);
  }
  for(const face of['front','back']){
    const recordId=f[face];if(!recordId)continue;
    const s=register(`${f.id}-${face}`,recordId,f.room,`${f.type==='fixed'?'Fixed panel':f.type==='sliding'?'Sliding panel':f.type==='waterfall'?'Waterfall':'Rotating carrier'} ${f.position||f.id.split('-').at(-1)} · ${face}`,{type:f.type,fixture:obj,face,source:f.source,uncertainty:f.uncertainty});
    obj.slots.push(s);
    const outwardFront=face==='front';
    const positiveZ=f.type==='rotating'?!outwardFront:outwardFront;
    const m=plane(f.width,height,0,cy,positiveZ?.038:-.038,material(s.record),parent);
    if(!positiveZ)m.rotation.y=Math.PI;
    // Distinct FrontSide faces make selection correspond to the visible side.
    m.material=m.material.clone();m.material.side=THREE.FrontSide;bind(m,s);
  }
  if(!f.back)box(f.width,.015,.02,0,cy-height/2,0,metal,parent);
}
// Two 120 × 120 rotating display frames, each with five double-sided carriers.
for(const x of[17.95,22.6]){
  box(1.565,.1,.68,x,.05,12.18,wood);box(1.565,.12,.68,x,1.435,12.18,wood);
  for(const dx of[-.745,.745])box(.07,1.40,.68,x+dx,.74,12.18,wood);
}

// Live installations: explicit records for floors, wall surfaces, fabricated objects.
surface(4.35,3.18,2.33,1.6,.175,appSlot(14,3,'Meeting room · W3A'),0,walls,true);
surface(6.3,3.18,.175,1.6,3.35,appSlot(15,3,'Meeting room · W3D, Statuario'),Math.PI/2,walls,true);
surface(4.35,2.87,2.33,1.46,6.61,appSlot(14,3,'Meeting room · W3C'),Math.PI,walls,true);
surface(1.6,3.18,.184,1.6,5.7,appSlot(16,3,'Meeting room · second Statuario source'),Math.PI/2);
surface(4.35,2.87,2.33,1.46,6.82,appSlot(10,2,'Living space · W2A'),0,walls,true);
surface(6.3,3.18,.175,1.6,10.04,appSlot(10,2,'Living space · W2D'),Math.PI/2,walls,true);
surface(4.35,2.8,2.33,1.5,13.25,appSlot(11,2,'Living space · Calacatta Noir wall'),Math.PI,walls,true);
surface(3.18,3.18,8.72,1.6,9.985,appSlot(7,1,'Bathroom · W1A'),0,walls,true);
surface(3.18,3.18,8.72,1.6,13.25,appSlot(7,1,'Bathroom · W1C'),Math.PI,walls,true);
surface(1.62,3.18,5,1.6,12.52,appSlot(8,1,'Bathroom · W1D'),Math.PI/2,walls,true);
surface(1.62,3.18,12.19,1.6,12.52,appSlot(8,1,'Bathroom · W1B'),-Math.PI/2,walls,true);
surface(3.18,3.18,8.72,1.6,3.45,appSlot(18,4,'Slab gallery · Foresta wall'),Math.PI,walls,true);
surface(4.35,3.18,26.68,1.6,.175,appSlot(26,6,'Waterfall gallery · Corchia wall'),0,walls,true);
surface(4.35,2.8,26.68,1.5,13.25,appSlot(27,7,'Kitchen · W7C'),Math.PI,walls,true);
surface(3.18,3.18,20.28,1.6,9.985,appSlot(28,8,'Tile library · Gemma Bronze'),0,walls,true);

function chair(x,z,yaw=0,parent=building){const g=new THREE.Group();g.position.set(x,0,z);g.rotation.y=yaw;parent.add(g);const seat=box(.52,.13,.54,0,.47,0,plain(colors.chair),g);box(.52,.52,.095,0,.79,-.225,plain(colors.chair),g);for(const dx of[-.21,.21])for(const dz of[-.2,.2])rod([dx,.42,dz],[dx*1.35,.025,dz*1.5],.018,metal,g);return g;}
function roundedTop(w,d,h,mat){const shape=new THREE.Shape(),r=d/2,half=w/2-r;
  shape.moveTo(-half,-r);shape.lineTo(half,-r);shape.absarc(half,0,r,-Math.PI/2,Math.PI/2,false);shape.lineTo(-half,r);shape.absarc(-half,0,r,Math.PI/2,Math.PI*1.5,false);
  const geo=new THREE.ExtrudeGeometry(shape,{depth:h,bevelEnabled:true,bevelSize:.015,bevelThickness:.008,bevelSegments:2,steps:1,curveSegments:30});geo.rotateX(-Math.PI/2);geo.computeBoundingBox();
  const uv=geo.attributes.uv,pos=geo.attributes.position;for(let i=0;i<uv.count;i++)uv.setXY(i,(pos.getX(i)+w/2)/w,(pos.getZ(i)+d/2)/d);
  const m=new THREE.Mesh(geo,mat);m.castShadow=true;m.receiveShadow=true;return m;
}
const tableSlot=appSlot(17,3,'Oro Noir · meeting tabletop');tableSlot.uncertainty='Tabletop 1.25 × 2.80 m from BOM; top edge, height, legs and chairs reconstructed from the supplied photograph.';
const table=roundedTop(2.8,1.25,.035,material(tableSlot.record));table.position.set(2.3,.75,3.48);table.rotation.y=Math.PI/2;building.add(table);bind(table,tableSlot);
for(const z of[2.5,4.46]){rod([1.99,.72,z],[1.68,.025,z-.18],.045);rod([2.61,.72,z],[2.94,.025,z+.18],.045);rod([1.78,.25,z],[2.83,.25,z],.035);}
for(const x of[1.30,3.30])for(const z of[2.85,4.08])chair(x,z,x<2?Math.PI/2:-Math.PI/2);
chair(2.3,1.7,0);chair(2.3,5.22,Math.PI);
for(const z of[3.08,3.98]){box(.56,.05,.43,2.3,.81,z,black);for(let i=0;i<8;i++)box(.23,.26,.027,2.15+(i%2)*.29,.96,z-.15+Math.floor(i/2)*.065,plain(['#ddd9c8','#aca995','#f0eee6','#c8c7bc'][i%4]));}
box(.08,1.03,1.85,.255,2.20,3.48,metal,walls);box(.09,.95,1.75,.31,2.20,3.48,black,walls);
const lightPts=[];for(let i=0;i<=40;i++){let t=i/40;lightPts.push(new THREE.Vector3(2.3+Math.sin(t*Math.PI*4)*.3,2.65+Math.cos(t*Math.PI*4)*.09,2.15+t*2.6));}
const luminaire=new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(lightPts),70,.04,8,false),new THREE.MeshStandardMaterial({color:'#f9e9b9',emissive:'#e7ca81',emissiveIntensity:.7}));building.add(luminaire);
for(const z of[2.25,4.65])rod([2.3,2.75,z],[2.3,3.28,z],.008);

// Fireplace, seating and a low stone table.
const hearth=appSlot(13,2,'Travertino Titanium · fireplace hearth');appliedBox(.8,.23,2.7,.64,.12,10.1,hearth);
const fireplace=appSlot(12,2,'Travertino Titanium · fireplace surround');appliedBox(.40,2.8,2.7,.44,1.63,10.1,fireplace);
box(.035,.62,1.32,.655,.77,10.1,black);box(.04,.065,1.14,.68,.52,10.1,new THREE.MeshStandardMaterial({color:'#9f6528',emissive:'#d39345',emissiveIntensity:.6}));
box(.065,.88,1.54,.68,2.05,10.1,black);chair(1.55,8.16,.4);chair(2.55,8.16,-.3);
box(1.7,.23,.75,2.03,.37,11.74,plain('#d1cbb7'));box(1.7,.34,.14,2.03,.66,12.02,plain('#d1cbb7'));
box(.7,.36,1.2,2.5,.20,10.13,plain('#b7ae96'));
// Bathroom: fabricated vanity surface, oval tub, mirrors and armchair.
const vanity=appSlot(9,1,'Pietra Imperiale · bathroom vanity');appliedBox(2.4,.14,.62,8.72,.86,10.39,vanity);box(2.28,.5,.52,8.72,.54,10.38,wood);
for(const x of[8.15,9.28]){box(.46,.05,.36,x,.945,10.4,ivory);rod([x,.94,10.18],[x,1.2,10.18],.018);rod([x,1.2,10.18],[x,1.2,10.36],.018);const mir=plane(.83,1.12,x,1.98,10.004,plain('#b4bdb2'),walls);}
const tub=roundedTop(1.8,.83,.51,plain('#edece3'));tub.position.set(8.72,.04,12.35);building.add(tub);const inner=roundedTop(1.45,.61,.025,plain('#d1d6cd'));inner.position.set(8.72,.568,12.35);building.add(inner);rod([9.8,0,12.45],[9.8,.92,12.45],.026);rod([9.8,.92,12.45],[9.5,.92,12.45],.022);chair(6.15,12.12,.6);

// The kitchen material is a user/photo identification; no fabricated SKU was supplied.
const verdi=[...records.values()].find(r=>r.name==='Verdi Alpi'&&r.group==='fixed');
const kitchenRecord={id:'APS-PHOTO-VERDI-ALPI',name:'Verdi Alpi · kitchen furniture',sku:'',finish:'Not specified for furniture',size:'Fabricated dimensions not supplied',texture:verdi.texture,texture_note:'Product design preview; photo/user identification, exact fabricated SKU unverified',source_workbook:'User-supplied room 7 photograph',source_sheet:'Photo reference',source_row:'—',notes:''};records.set(kitchenRecord.id,kitchenRecord);
const kitchen=register('APS-R7-KITCHEN-TOP',kitchenRecord.id,7,'Verdi Alpi · island and counter',{type:'furniture',uncertainty:'Island assumed 1.2 × 2.45 × 0.92 m; wall counter and backsplash approximated from photo. Confirm SKU, finish and dimensions.'});
box(1.06,.83,2.3,26.88,.42,10.05,wood);appliedBox(1.22,.11,2.46,26.88,.89,10.05,kitchen);
appliedBox(.70,.08,3.4,28.47,.91,10.05,kitchen);box(.63,.83,3.4,28.52,.42,10.05,wood);
surface(2.8,.92,28.79,1.46,10.05,kitchen,-Math.PI/2);
for(const z of[7.5,12.24])box(.65,2.95,1.3,28.52,1.48,z,wood);
box(.65,.63,3.3,28.52,2.68,10.05,wood);
for(let z=7;z<13.2;z+=.22)box(.025,2.90,.012,28.174,1.46,z,plain('#433a2e'));
for(const z of[9.25,10.2,11.12]){cyl(.24,.09,25.78,.68,z,plain('#b9ab90'));for(const dx of[-.12,.12])rod([25.78+dx,.66,z],[25.78+dx*1.5,.02,z],.021);}
cyl(.11,.38,26.87,1.15,9.35,plain('#d7c6ab'),building,.07);
// Sample tower geometry follows its 75-chip capacity, not an invented sample inventory.
const tower=register('APS-R4-SAMPLE-TOWER',null,4,'Sample tower · 75-chip capacity',{type:'tower',uncertainty:'Hardware 9902-2066-0 from BOM. Chip assortment is not supplied; blank chips indicate capacity only.'});
box(.75,1.45,.36,6.1,.73,3.15,wood);
for(let row=0;row<15;row++)for(let col=0;col<5;col++)bind(box(.11,.065,.09,5.82+col*.14,.13+row*.087,3.36,plain('#dfdaca')),tower);
// Sample board uses the nine source finish rows; individual chip counts are illustrative.
source.records.filter(r=>r.group==='samples').forEach((r,i)=>{const s=register(`APS-R3-SAMPLE-${i}`,r.id,3,`${r.name} sample board`,{type:'sample',uncertainty:'Finish identity from BOM; chip position and shape are illustrative.'});surface(.30,.24,.19,1.0+(i%3)*.30,.8+Math.floor(i/3)*.37,s,Math.PI/2);});

// Subsize composition: each source row remains separately selectable.
const taj=source.records.filter(r=>r.location==='W5C');
taj.forEach((r,i)=>{const s=register(`APS-R5-SUB-${i}`,r.id,5,`Taj Mahal · ${r.size}`,{type:'subsize',uncertainty:'Individual product sizes from BOM; composition scaled into the wall zone from photos.'});let dims=[[1.2,2.8],[.6,1.2],[1.2,1.2],[.30,.30],[.6,.6],[.3,.6],[.9,.9]][i];let pos=[[19.45,1.5],[20.45,2.30],[21.05,.78],[20.08,.85],[21.15,2.55],[20.37,1.18],[21.13,1.88]][i];surface(dims[0],dims[1],pos[0],pos[1],3.448,s,Math.PI);});
const sub=source.records.filter(r=>r.group==='application'&&r.source_row>=29&&r.source_row<=42);
sub.forEach((r,i)=>{const s=register(`APS-R8-SUB-${i}`,r.id,8,`${r.location} · ${r.name}`,{type:'subsize',uncertainty:'BOM products/sizes; display composition approximated from the room photograph.'});const col=i%7,row=Math.floor(i/7);surface(.75,1.0,17.55+col*.9,.68+row*1.14,13.24,s,Math.PI);});

function plant(x,z,scale=1){cyl(.16*scale,.35*scale,x,.18*scale,z,plain('#a99c84'),building,.22*scale);for(let i=0;i<7;i++){const a=i*2.4;const leaf=sphere(.16*scale,x+Math.sin(a)*.15*scale,.52*scale+(i%3)*.1*scale,z+Math.cos(a)*.15*scale,plain(['#74805c','#87916b','#586a4a'][i%3]));leaf.scale.set(.7,2,.6);}}
plant(4.1,12.9);plant(24.9,7.6);plant(26.87,10.95,.55);plant(19.55,10.35,.8);plant(3.9,.7);

// Selection outline is drawn around the actual clicked surface, including articulated panels.
const highlight=new THREE.Box3Helper(new THREE.Box3(),new THREE.Color('#a58743'));highlight.material.depthTest=false;highlight.material.transparent=true;highlight.material.opacity=.95;highlight.renderOrder=100;highlight.visible=false;scene.add(highlight);
const raycaster=new THREE.Raycaster(),pointer=new THREE.Vector2();let down=null;
renderer.domElement.addEventListener('pointerdown',e=>down={x:e.clientX,y:e.clientY});
renderer.domElement.addEventListener('pointerup',e=>{
  if(!down||Math.hypot(e.clientX-down.x,e.clientY-down.y)>5)return;
  const rect=renderer.domElement.getBoundingClientRect();pointer.set((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1);raycaster.setFromCamera(pointer,camera);
  const hits=raycaster.intersectObjects(pickable).filter(h=>{let p=h.object;while(p){if(!p.visible)return false;p=p.parent;}return true;});if(hits[0])select(slots.get(hits[0].object.userData.slotId));
});
function cameraTo(position,target){targetCamera={position:new THREE.Vector3(...position),target:new THREE.Vector3(...target)};}
function centerRoom(room){const r=manifest.rooms.find(r=>r.id===room);if(!r)return new THREE.Vector3(0,0,0);const[x1,z1,x2,z2]=r.bounds;return new THREE.Vector3((x1+x2)/2-14.5,0,(z1+z2)/2-6.719);}
function frameRoom(room=activeRoom){
  const c=centerRoom(room);
  controls.enableRotate=view!=='plan';controls.mouseButtons.LEFT=view==='plan'?THREE.MOUSE.PAN:THREE.MOUSE.ROTATE;
  if(view==='plan'){targetCamera=null;camera.position.set(c.x,room?15:39,c.z+.001);controls.target.set(c.x,0,c.z);controls.maxPolarAngle=Math.PI*.49;controls.update();}
  else if(view==='walk'){
    if(!room)cameraTo([0,1.65,6.5],[0,1.6,-4.6]);
    else{const r=manifest.rooms.find(r=>r.id===room);const depth=r.bounds[3]-r.bounds[1];cameraTo([c.x,1.65,c.z+depth*.42],[c.x,1.6,c.z-depth*.4]);}
    controls.minDistance=.25;controls.maxPolarAngle=Math.PI*.91;
  }else{cameraTo(room?[c.x+6.7,10,c.z+8.5]:[24,31,31],room?[c.x,.8,c.z]:[0,0,0]);controls.minDistance=1.2;controls.maxPolarAngle=Math.PI*.49;}
}
function roomNav(room){activeRoom=room;$$('.room').forEach(b=>b.classList.toggle('active',Number(b.dataset.room||0)===room));
  const r=manifest.rooms.find(r=>r.id===room);$('#roomCaption').innerHTML=r?`<span class="eyebrow">APS / ROOM ${String(room).padStart(2,'0')}</span><h1>${escape(r.name)}</h1><p>${escape(r.subtitle)}</p>`:'<span class="eyebrow">APS / TEMPORARY SHOWROOM</span><h1>One space. Every surface.</h1><p>Explore the current collection in context.</p>';
  frameRoom(room);
}
$('#rooms').innerHTML=manifest.rooms.map(r=>`<button class="room" data-room="${r.id}"><span class="room-number">${String(r.id).padStart(2,'0')}</span><span><b>${escape(r.name)}</b><small>${escape(r.subtitle)}</small></span></button>`).join('');
$$('.room').forEach(b=>b.addEventListener('click',()=>roomNav(Number(b.dataset.room||0))));
$$('[data-view]').forEach(b=>b.addEventListener('click',()=>{view=b.dataset.view;$$('[data-view]').forEach(b=>b.classList.toggle('active',b.dataset.view===view));$('#cameraHelp').textContent=view==='walk'?'Drag to look around · W A S D to move · Q / E to turn · Click a surface':view==='plan'?'Drag to pan · Scroll to zoom · Click a surface':'Drag to orbit · Right-drag to pan · Scroll to zoom · Click a surface';frameRoom();}));
$('#resetCamera').onclick=()=>frameRoom();$('#wallsToggle').onchange=e=>walls.visible=e.target.checked;$('#labelsToggle').onchange=e=>labelGroup.visible=e.target.checked;
function effectiveRecord(s){return records.get(studies.get(s.id))||s.record;}
function select(slot,focus=false){
  selected=slot;$('#emptySelection').hidden=true;$('#selectionDetail').hidden=false;activateTab('selected');renderSelection();
  if(slot.fixture?.definition.type==='rotating')slot.fixture.face=slot.face;
  if(focus){const p=new THREE.Vector3();slot.meshes[0]?.getWorldPosition(p);if(slot.meshes[0]){const box3=new THREE.Box3().setFromObject(slot.meshes[0]);const size=box3.getSize(new THREE.Vector3()).length();cameraTo([p.x+Math.max(2.4,size*.8),p.y+Math.max(2.3,size*.5),p.z+Math.max(3,size*.8)],[p.x,p.y,p.z]);}}
  $('#selectionStatus').textContent=slot.id;
}
function renderSelection(){
  if(!selected)return;const s=selected,r=effectiveRecord(s),room=manifest.rooms.find(x=>x.id===s.room),f=s.fixture,study=studies.has(s.id);
  const geoNote=s.uncertainty||'Reconstructed source model; geometry remains approximate.';
  $('#selectionDetail').innerHTML=`<div class="eyebrow">${escape(s.title)}</div>${study?'<span class="study-badge">LOCAL STUDY · SOURCE BASELINE RETAINED</span>':''}<div class="material-preview">${r?.texture?`<img src="${escape(preview(r))}" alt="${escape(r.name)} product design">`:''}<span class="tag">${escape(r?.finish||'CAPACITY / GEOMETRY REFERENCE')}</span></div><h2 class="detail-name">${escape(r?.name||s.title)}</h2><div class="sku">${escape(r?.sku||'Exact SKU not supplied')}</div><div class="facts"><div class="fact"><small>Product size</small><b>${escape(r?.size||'75 chip capacity')}</b></div><div class="fact"><small>Thickness</small><b>${escape(r?.thickness||'Not specified')}</b></div><div class="fact"><small>Space</small><b>${room?`${s.room} · ${escape(room.name)}`:'Fixed gallery'}</b></div><div class="fact"><small>Surface</small><b>${escape(s.face||s.type)}</b></div></div><div class="actions">${f&&['sliding','rotating'].includes(s.type)?`<button id="operateFixture" class="primary">${f.target>0?'Return to rack':s.type==='sliding'?'Pull out panel':'Pull out & tilt'}</button>`:''}${f?.definition.back?'<button id="otherFace">View other face</button>':''}<button id="focusSurface">Focus ↗</button></div>${r?.texture?'<button class="small-button" id="studyMaterial">Visual material study</button>':''}<button class="small-button" id="placementActions">Placement & observation actions →</button>${study?'<button class="small-button" id="resetSurface">Restore this surface</button>':''}<div class="source-note"><b>${r?.source_sheet==='Photo reference'?'Photo / user identification':'Source evidence'}</b>${escape(r?.source_workbook||'APS BOM hardware list')}<br>${escape(r?.source_sheet||'APS_Tempry')}${r?.source_row?` · row ${escape(r.source_row)}`:''}<br>${escape(s.source||'APS drawing + supplied room photo')}<a href="#" id="inspectEvidence">Open source library ↗</a></div><div class="source-note warning"><b>Model confidence</b>${escape(geoNote)}${r?.texture_note?`<br>${escape(r.texture_note)}.`:''}</div>${r?.notes?`<details><summary>Original source notes</summary><p style="font-size:10px;white-space:pre-line">${escape(r.notes)}</p></details>`:''}${room?`<img class="detail-photo" id="selectionPhoto" src="references/${room.photo}" alt="Installed ${escape(room.name)} reference"><button class="small-button" id="selectionPhotoButton">Compare installed photograph ↗</button>`:''}`;
  $('#placementActions').onclick=()=>window.dispatchEvent(new CustomEvent('studio:slot',{detail:s.id}));
  $('#operateFixture')?.addEventListener('click',()=>{operate(f);renderSelection();});
  $('#otherFace')?.addEventListener('click',()=>{const next=f.slots.find(x=>x.id!==s.id);select(next);if(s.type==='rotating'&&f.target){const p=new THREE.Vector3();f.group.getWorldPosition(p);cameraTo([p.x+2.4,3.9,p.z-4],[p.x,1.2,p.z-.9]);}else focusFace(next);});
  $('#focusSurface').onclick=()=>focusFace(s);
  $('#studyMaterial')?.addEventListener('click',()=>{$('#studyDialog').showModal();$('#studySearch').value='';renderStudy();});
  $('#resetSurface')?.addEventListener('click',()=>{restore(s);renderSelection();});
  $('#inspectEvidence').onclick=e=>{e.preventDefault();openEvidence(s.type==='fixed'?'fixed':s.type==='waterfall'?'waterfall':s.type==='rotating'?'rotating':s.type==='sliding'?'sliding':'plan');};
  $('#selectionPhoto')?.addEventListener('click',()=>showPhoto(s.room));$('#selectionPhotoButton')?.addEventListener('click',()=>showPhoto(s.room));
}
function focusFace(s){const mesh=s.meshes[0];if(!mesh)return;const p=new THREE.Vector3();mesh.getWorldPosition(p);const normal=new THREE.Vector3(0,0,1).transformDirection(mesh.matrixWorld);if(s.type==='floor')normal.set(0,1,0);const distance=['fixed','sliding','waterfall'].includes(s.type)?5.1:3.6;const c=p.clone().addScaledVector(normal,distance);c.y=Math.max(c.y,p.y+1.15);cameraTo(c.toArray(),p.toArray());}
function operate(f){
  const open=f.target===0;
  // A single extended carrier per bank keeps the preview legible.
  if(open)for(const other of animated)if(other!==f&&other.definition.type===f.definition.type&&other.definition.room===f.definition.room)other.target=0;
  f.target=open?1:0;
  if(open&&f.definition.type==='rotating'){const p=new THREE.Vector3();f.group.getWorldPosition(p);cameraTo([p.x+2.4,4,p.z-4],[p.x,1.1,p.z-1]);}
}
function adjacent(delta){const list=[...slots.values()].filter(s=>s.fixture&&(!activeRoom||s.room===activeRoom));if(!list.length){toast('Select a surface in this room.');return;}const idx=list.findIndex(s=>s.id===selected?.id);select(list[(idx+delta+list.length)%list.length],true);}
$('#nextObject').onclick=()=>adjacent(1);$('#previousObject').onclick=()=>adjacent(-1);
$('#visitTable').onclick=()=>{roomNav(3);select(tableSlot);cameraTo([-7.7,4.2,-.7],[-12.2,1,-3.24]);};
function showPhoto(room){const r=manifest.rooms.find(r=>r.id===(room||3));$('#photoTitle').textContent=`${r.id} · ${r.name}`;$('#photoImage').src=`references/${r.photo}`;$('#photoDialog').showModal();}
$('#comparePhoto').onclick=()=>showPhoto(activeRoom||selected?.room||3);

function activateTab(name){$$('[data-tab]').forEach(b=>b.classList.toggle('active',b.dataset.tab===name));$('#selectedPanel').hidden=name!=='selected';$('#productsPanel').hidden=name!=='products';if(name==='products')renderSearch();}
$$('[data-tab]').forEach(b=>b.onclick=()=>activateTab(b.dataset.tab));
$$('[data-catalog]').forEach(b=>b.onclick=()=>{catalog=b.dataset.catalog;$$('[data-catalog]').forEach(b=>b.classList.toggle('active',b.dataset.catalog===catalog));renderSearch();});
$('#productSearch').oninput=renderSearch;
function matches(r,q){return !q||[r.name,r.sku,r.finish,r.location,r.area].join(' ').toLowerCase().includes(q);}
function renderSearch(){const q=$('#productSearch').value.toLowerCase().trim();
  if(catalog==='installed'){
    const installed=new Set(state.placements.map(a=>a.variant_id));const rows=[...records.values()].filter(r=>installed.has(r.id)&&!r.id.startsWith('PLACEMENT-')&&matches(r,q));$('#searchCount').textContent=`${rows.length} installed variants · placements from SQLite`;
    $('#productResults').innerHTML=rows.slice(0,100).map(r=>`<button class="product-row" data-record="${escape(r.id)}">${r.texture?`<img loading="lazy" src="${escape(preview(r))}" alt="">`:'<span style="width:35px">◇</span>'}<span><b>${escape(r.name)}</b><small>${escape(r.sku||'No SKU')} · ${escape(r.finish)}<br>${escape(r.location||r.source_sheet)} · ${escape(r.area||'Photo reference')}</small></span></button>`).join('');
    $$('[data-record]').forEach(b=>b.onclick=()=>{const slot=[...slots.values()].find(s=>s.recordId===b.dataset.record);if(slot){select(slot,true);}else{const r=records.get(b.dataset.record);toast(`${r.location}: source record retained; not placed in the installed model. ${r.notes||''}`);}});
  }else{
    const result=portfolio.filter(r=>[r.name_as_listed,r.reference_name,r.marketing_header,r.technical_header,r.option_as_listed].join(' ').toLowerCase().includes(q));
    $('#searchCount').textContent=`${result.length} source options · not a verified SKU catalogue${result.length>100?' · first 100 shown':''}`;
    $('#productResults').innerHTML=result.slice(0,100).map(r=>`<div class="portfolio-item"><b>${escape(r.name_as_listed||r.reference_name)}</b><small>${escape(r.marketing_header||r.technical_header)} · ${escape(r.option_as_listed)}${r.thickness_mm?` · ${r.thickness_mm} mm`:''}</small><small>${escape(r.source_sheet)}!${escape(r.source_cell)}${r.notes_as_listed?` · ${escape(r.notes_as_listed)}`:''}</small></div>`).join('');
  }
}
function renderStudy(){const q=$('#studySearch').value.toLowerCase().trim();const seen=new Set();const rows=[...records.values()].filter(r=>{if(!r.texture||seen.has(r.sku||r.name)||!matches(r,q))return false;seen.add(r.sku||r.name);return true;});$('#studyResults').innerHTML=rows.slice(0,80).map(r=>`<button class="product-row" data-study-record="${r.id}"><img loading="lazy" src="${escape(preview(r))}" alt=""><span><b>${escape(r.name)}</b><small>${escape(r.sku)} · ${escape(r.finish)} · ${escape(r.size)}</small></span></button>`).join('');$$('[data-study-record]').forEach(b=>b.onclick=()=>{applyStudy(selected,records.get(b.dataset.studyRecord));$('#studyDialog').close();renderSelection();toast('Material study applied to this surface. Export JSON to retain it.');});}
$('#studySearch').oninput=renderStudy;
function applyStudy(s,r){studies.set(s.id,r.id);for(const mesh of s.meshes){mesh.userData.baselineMaterial??=mesh.material;const m=material(r).clone();m.side=mesh.material.side;mesh.material=m;}}
function restore(s){studies.delete(s.id);for(const mesh of s.meshes){if(mesh.userData.baselineMaterial){mesh.material=mesh.userData.baselineMaterial;delete mesh.userData.baselineMaterial;}}}
$('#clearStudy').onclick=()=>{for(const id of [...studies.keys()])restore(slots.get(id));renderSelection();toast('All surfaces restored to the source baseline.');};
$('#exportStudy').onclick=()=>{const data={schema_version:1,showroom_id:'APS',kind:'unapproved_visual_material_study',base_source_sha256:source.sha256,created_at:new Date().toISOString(),changes:[...studies].map(([id,recordId])=>({slot_id:id,baseline_record_id:slots.get(id).recordId,proposed_record_id:recordId,proposed_sku:records.get(recordId).sku})),limitations:['No compatibility, stock, lifecycle or Merch-priority validation has been performed.','This file does not update installation status.']};const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='APS-material-study.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};

const evidencePages={
  plan:{title:'APS · layout & floor plan',description:'Overall dimensions come from the drawing dated 21 November 2025. Internal geometry is reconstructed for this interactive review.',images:['aps-plan.png','aps-floors.png']},
  waterfall:{title:'Waterfall · modular display',description:'Brochure pp. 31–33. Three 60 × 280 cm panels per module; 1.655 m width, 2.936 m height, 0.205 m depth. APS lists seven kits: nine wall panels plus twelve central faces.',images:['fixture-page-31.jpg','fixture-page-32.jpg','fixture-page-33.jpg']},
  fixed:{title:'Fixed panels · both faces',description:'Brochure pp. 37–40. A 1.45 m wide × 3.20 m high frame supports a 160 × 320 cm display. APS fixed quantities total 48 faces on 24 panels. Product pairing is reconciled against drawing p. 2.',images:['fixture-page-37.jpg','fixture-page-38.jpg','fixture-page-39.jpg','fixture-page-40.jpg']},
  sliding:{title:'Sliding panels · mirrored banks',description:'Brochure pp. 45–48. Mirrored 12-panel units for 160 × 320 and 120 × 280 cm products. The 123.4 cm dimension is a support dimension, not slab height. Exact travel and hinge coordinates require a fixture model.',images:['fixture-page-45.jpg','fixture-page-46.jpg','fixture-page-47.jpg','fixture-page-48.jpg']},
  rotating:{title:'Rotating panels · pull out, then tilt',description:'Brochure pp. 50–54. APS uses two 120 × 120 cm units, 9902-3105-0. Each contains five carriers / ten faces. Frame: 1.565 × 0.680 × 1.495 m. The animation approximates the mechanism; brochure p. 50 thickness text conflicts with APS 9 mm.',images:['fixture-page-50.jpg','fixture-page-51.jpg','fixture-page-52.jpg','fixture-page-53.jpg','fixture-page-54.jpg']},
  assortment:{title:'Anatolia assortment · source exports',description:'Supplied file: Assortment confirmation list with names 260618_1.xlsx. All nine tabs are exported, including empty sheets and notes/summary tabs. The older 251105 file mentioned in the request was not supplied.',html:'<a href="../../../output/assortment/assortment_options.csv" download>↓ Searchable assortment options CSV</a><a href="../../../output/assortment/README.md" download>↓ All nine CSV tabs + source metadata</a><a href="../../../output/assortment/manifest.json" target="_blank">Export manifest ↗</a><a href="../../../output/assortment/formula_metadata.json" target="_blank">Original formulas and cached values ↗</a><p>Option rows do not establish SKU, release status, stock, priority or suitability. Embedded workbook images are indexed separately for future matching.</p>'},
  confidence:{title:'What the model knows',description:'Source facts, assumptions and unresolved details remain visible so this can grow into a reliable operational model.',html:`<ul>${manifest.assumptions.map(s=>`<li>${escape(s)}</li>`).join('')}</ul><a href="data/state.json" target="_blank">Fixture and slot manifest ↗</a><a href="data/state.json" target="_blank">All 188 APS source records ↗</a><a href="../docs/archive/Source_Pack_and_3D_Simulation.md" target="_blank">Source guide and next measurements ↗</a>`}
};
$('#evidenceNav').innerHTML=Object.entries(evidencePages).map(([id,r])=>`<button data-evidence="${id}">${escape(r.title.split(' · ')[0])}</button>`).join('');
function evidenceContent(id){const p=evidencePages[id];$('#evidenceTitle').textContent=p.title;$('#evidenceDescription').textContent=p.description;$('#evidenceContent').innerHTML=p.html||p.images.map(name=>`<img loading="lazy" src="references/${name}" alt="${escape(p.title)} source reference ${name}">`).join('');$$('[data-evidence]').forEach(b=>b.classList.toggle('active',b.dataset.evidence===id));}
function openEvidence(id='plan'){evidenceContent(id);$('#evidence').showModal();}
$$('[data-evidence]').forEach(b=>b.onclick=()=>evidenceContent(b.dataset.evidence));$('#evidenceButton').onclick=()=>openEvidence();
$$('[data-close]').forEach(b=>b.onclick=()=>document.getElementById(b.dataset.close).close());
$$('dialog').forEach(d=>d.addEventListener('click',e=>{if(e.target===d){const b=d.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)d.close();}}));
let toastTimer;function toast(text){$('#toast').textContent=text;$('#toast').classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('visible'),4500);}

const keys=new Set();window.addEventListener('keydown',e=>{if(['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)||$('dialog[open]'))return;if(view==='walk'&&['w','a','s','d','q','e'].includes(e.key.toLowerCase())){keys.add(e.key.toLowerCase());e.preventDefault();targetCamera=null;}});window.addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()));window.addEventListener('blur',()=>keys.clear());
function resize(){const w=Math.max(1,container.clientWidth),h=Math.max(1,container.clientHeight);renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();}
new ResizeObserver(resize).observe(container);resize();
camera.position.set(24,31,31);controls.target.set(0,0,0);controls.update();
const overlayItems=[];
let previousTime=performance.now();
function tick(now){const dt=Math.min((now-previousTime)/1000,.3);previousTime=now;
  if(targetCamera){camera.position.lerp(targetCamera.position,1-Math.exp(-dt*5));controls.target.lerp(targetCamera.target,1-Math.exp(-dt*5));if(camera.position.distanceTo(targetCamera.position)<.015&&controls.target.distanceTo(targetCamera.target)<.015)targetCamera=null;}
  if(view==='walk'&&keys.size){const dir=controls.target.clone().sub(camera.position);dir.y=0;dir.normalize();const right=new THREE.Vector3(-dir.z,0,dir.x);const step=new THREE.Vector3();if(keys.has('w'))step.add(dir);if(keys.has('s'))step.sub(dir);if(keys.has('d'))step.add(right);if(keys.has('a'))step.sub(right);step.multiplyScalar(dt*2);camera.position.add(step);controls.target.add(step);if(keys.has('q')||keys.has('e')){const turn=controls.target.clone().sub(camera.position).applyAxisAngle(new THREE.Vector3(0,1,0),dt*(keys.has('q')?1:-1));controls.target.copy(camera.position).add(turn);}}
  for(const f of animated){f.open+=(f.target-f.open)*(1-Math.exp(-dt*5));if(f.definition.type==='sliding'){f.moving.position.z=f.open*1.65;f.moving.position.x=f.open*(f.definition.yaw>0?.28:-.28);}else{f.moving.position.z=-Math.min(1,f.open*2)*1.65;const angle=(f.face==='back'?-1:1)*Math.max(0,(f.open-.4)/.6)*Math.PI/2;f.pivot.rotation.x+=(angle-f.pivot.rotation.x)*(1-Math.exp(-dt*10));}}
  controls.update();
  for(const {point,element} of labels){const p=new THREE.Vector3();point.getWorldPosition(p);p.project(camera);element.hidden=!labelGroup.visible||p.z>1||p.z<0||view==='walk';element.style.left=`${(p.x*.5+.5)*container.clientWidth}px`;element.style.top=`${(-p.y*.5+.5)*container.clientHeight}px`;}
  if(selected?.meshes.length){const b=new THREE.Box3();selected.meshes.forEach(m=>b.expandByObject(m));highlight.box.copy(b);highlight.visible=true;}
  for(const item of overlayItems)item.helper.box.setFromObject(item.mesh);
  if(container.clientWidth&&container.clientHeight)renderer.render(scene,camera);requestAnimationFrame(tick);
}
requestAnimationFrame(tick);$('#loading').hidden=true;
// Read-only diagnostic surface for source/slot checks and local smoke validation.
window.APS_SIMULATION={ready:true,sourceRecordCount:source.records.length,fixtureCount:fixtures.size,slotCount:slots.size,fixtureTypes:manifest.fixtures.reduce((o,f)=>(o[f.type]=(o[f.type]||0)+1,o),{}),getStudy:()=>[...studies],getSelected:()=>selected?.id,selectSlot:id=>{const s=slots.get(id);if(s)select(s,true);},getUnplaced:()=>source.records.filter(r=>![...slots.values()].some(s=>s.recordId===r.id)).map(r=>({id:r.id,name:r.name,location:r.location})),getFixtureState:id=>{const f=fixtures.get(id);return f?{open:f.open,target:f.target}:null;}};

const baseMaterials=new Map();
window.APS_SIMULATION.setOverlay=(mode='none',onlyIds=null)=>{
  for(const item of overlayItems){scene.remove(item.helper);item.helper.geometry.dispose();item.helper.material.dispose();}overlayItems.length=0;
  const issues=new Map(state.review.issues.map(i=>[i.slot_id,i.level]));const good=new Set(state.review.good.map(i=>i.slot_id));
  const duplicate=new Set(state.review.issues.filter(i=>i.code==='duplicate').map(i=>i.slot_id));
  for(const row of state.slots){const slot=slots.get(row.id);if(!slot)continue;
    let color=null;if(mode==='visibility'&&(row.fixture_id||row.type==='floor'))color={prime:0xb77730,secondary:0x527f8f,commercial:0x6c7650}[row.visibility_tier];
    if(mode==='review'&&issues.has(row.id))color=issues.get(row.id)==='attention'?0xcc624c:0xc49b3c;
    if(mode==='duplicates'&&duplicate.has(row.id))color=0xc49b3c;
    if(mode==='good'&&good.has(row.id))color=0x448468;
    if(onlyIds?.includes(row.id))color=0xd06341;else if(onlyIds)color=null;
    if(color)for(const mesh of slot.meshes){const helper=new THREE.Box3Helper(new THREE.Box3().setFromObject(mesh),color);helper.material.depthTest=false;helper.material.transparent=true;helper.material.opacity=.95;helper.renderOrder=30;scene.add(helper);overlayItems.push({helper,mesh});}
  }
  return overlayItems.length;
};
window.APS_SIMULATION.applySnapshot=async(newState,proposal=null)=>{
  replaceState(newState);studies.clear();
  const changes=proposal?.changes||[];
  for(const a of state.placements){const slot=slots.get(a.slot_id);if(!slot)continue;const ch=changes.find(x=>x.kind==='placement'&&x.slot_id===a.slot_id);const r=recordFor(ch?.variant_id||a.variant_id,ch?.face_id||a.face_id);slot.record=r;slot.recordId=r?.id;
    if(r){records.set(r.id,r);if(r.texture&&!imageSources.has(imageKey(r))){const im=new Image();im.src=r.texture;try{await im.decode();imageSources.set(imageKey(r),im);}catch{}}}
    for(const mesh of slot.meshes){const m=material(r).clone();m.side=mesh.material.side;if(mesh.material.map?.repeat&&(mesh.material.map.repeat.x!==1||mesh.material.map.repeat.y!==1)&&m.map){m.map=m.map.clone();m.map.repeat.copy(mesh.material.map.repeat);m.map.wrapS=m.map.wrapT=THREE.RepeatWrapping;}mesh.material=m;delete mesh.userData.baselineMaterial;}
  }
  for(const f of state.fixtures){const object=fixtures.get(f.id);if(!object)continue;const ch=changes.find(x=>x.kind==='fixture'&&x.fixture_id===f.id);const pos=ch?.to||f;object.group.position.set(pos.x_mm/1000,0,pos.z_mm/1000);object.group.rotation.y=THREE.MathUtils.degToRad(pos.yaw_deg);}
  renderSelection();window.APS_SIMULATION.setOverlay(proposal?'proposal':'none',proposal?changes.flatMap(x=>x.slot_id?[x.slot_id]:state.slots.filter(s=>s.fixture_id===x.fixture_id).map(s=>s.id)):null);
};
window.APS_SIMULATION.getAssignments=()=>[...slots.values()].map(s=>({slot_id:s.id,variant_id:s.recordId,texture:s.record?.texture}));
window.APS_SIMULATION.getOverlayCount=()=>overlayItems.length;
window.dispatchEvent(new Event('studio:ready'));

window.APS_SIMULATION.getFixturePosition=id=>{const f=fixtures.get(id);return f?{x_mm:f.group.position.x*1000,z_mm:f.group.position.z*1000,yaw_deg:THREE.MathUtils.radToDeg(f.group.rotation.y)}:null;};
