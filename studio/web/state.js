// SQLite's HTTP state and its published snapshot share the same contract.
export let state;
export let connected=false;
const local=['127.0.0.1','localhost'].includes(location.hostname);
if(local){
  try{const r=await fetch('/api/state',{cache:'no-store'});if(r.ok){state=await r.json();connected=state.meta.mode==='connected';}}catch{}
}
if(!state){const r=await fetch('data/state.json');if(!r.ok)throw Error('The showroom snapshot could not be loaded.');state=await r.json();}
export function replaceState(value){state=value;}
export async function request(path,payload={}){
  if(!connected)throw Error('This is the published review snapshot. Start the local Studio to save changes to SQLite.');
  const r=await fetch('/api/'+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({base_revision:state.meta.revision,...payload})});
  const result=await r.json();if(!r.ok)throw Error(result.error||'The change was not saved.');return result;
}
export async function refresh(){if(connected){const r=await fetch('/api/state',{cache:'no-store'});if(!r.ok)throw Error('The local database connection is unavailable.');state=await r.json();}return state;}
export function recordFor(variantId,faceId=null){
  const v=state.variants.find(v=>v.id===variantId);if(!v)return null;
  const p=state.products.find(p=>p.id===v.product_id);
  const faces=state.faces.filter(f=>f.product_id===p.id).sort((a,b)=>(Math.abs(a.width_mm-(v.width_mm||1600))+Math.abs(a.height_mm-(v.height_mm||3200)))-(Math.abs(b.width_mm-(v.width_mm||1600))+Math.abs(b.height_mm-(v.height_mm||3200)))||a.id.localeCompare(b.id));
  const face=state.faces.find(f=>f.id===faceId&&f.product_id===p.id)||faces[0];
  const preview=v.preview||{},raw=v.source||{};
  return {...raw,id:v.id,product_id:p.id,name:p.name,sku:v.sku||'',finish:v.finish,
    size:v.width_mm&&v.height_mm?`${v.width_mm} × ${v.height_mm} mm`:'Dimensions unconfirmed',
    thickness:v.thickness_mm?`${v.thickness_mm} mm`:'Unconfirmed',width_m:(v.width_mm||1600)/1000,height_m:(v.height_mm||3200)/1000,
    texture:face?.data.path||preview.texture||null,texture_crop:face?null:preview.texture_crop,
    texture_note:face?`${face.data.source_kind} · ${face.data.pixel_width} × ${face.data.pixel_height} px · production design reference; exact installed face unverified`:preview.texture_note||'No production face matched; source preview or neutral material shown.',
    face_id:face?.id,positioning:p.positioning,hit:p.hit,lifecycle:v.lifecycle};
}
