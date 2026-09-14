// Pure, repeatable physical tile layout. All dimensions here are metres.
const archived=f=>/before_color_match/i.test(f.data?.source_relative||'');
export function facePool(record,faces){
  if(!record?.product_id)return [];
  const w=record.width_m*1000,h=record.height_m*1000;
  const pool=faces.filter(f=>f.product_id===record.product_id&&!archived(f)&&f.width_mm+25>=w&&f.height_mm+25>=h);
  if(!pool.length)return [];
  pool.sort((a,b)=>(Math.abs(a.width_mm-w)+Math.abs(a.height_mm-h))-(Math.abs(b.width_mm-w)+Math.abs(b.height_mm-h))||a.id.localeCompare(b.id));
  const best=pool[0];
  return pool.filter(f=>f.width_mm===best.width_mm&&f.height_mm===best.height_mm).sort((a,b)=>(a.data?.face_index||0)-(b.data?.face_index||0)||a.id.localeCompare(b.id));
}
function rng(key){let n=2166136261;for(const c of key)n=Math.imul(n^c.charCodeAt(0),16777619);return ()=>{n+=0x6D2B79F5;let t=Math.imul(n^n>>>15,1|n);t^=t+Math.imul(t^t>>>7,61|t);return ((t^t>>>14)>>>0)/4294967296;};}
export function tileLayout({width,height,tileWidth,tileHeight,faces=[],seed='APS',preferredFace=null}){
  if(![width,height,tileWidth,tileHeight].every(n=>Number.isFinite(n)&&n>0))throw Error('Positive, finite surface/tile dimensions are required.');
  const columns=Math.ceil((width-1e-8)/tileWidth),rows=Math.ceil((height-1e-8)/tileHeight);
  if(columns*rows>4096)throw Error('Tile grid exceeds the room-preview limit.');
  const random=rng(seed),usage=faces.map(()=>0),chosen=[],tiles=[];
  for(let row=0;row<rows;row++)for(let col=0;col<columns;col++){
    const left=col?chosen.at(-1):-1,above=row?chosen[(row-1)*columns+col]:-1;
    let candidates=faces.map((_,i)=>i).filter(i=>i!==left&&i!==above);
    if(!candidates.length)candidates=faces.map((_,i)=>i);
    const min=Math.min(...candidates.map(i=>usage[i]));candidates=candidates.filter(i=>usage[i]===min);
    let index=candidates.length?candidates[Math.floor(random()*candidates.length)]:-1;
    if(!tiles.length&&faces.some(f=>f.id===preferredFace))index=faces.findIndex(f=>f.id===preferredFace);
    if(index>=0)usage[index]++;chosen.push(index);
    const face=faces[index]||null,x=col*tileWidth,y=row*tileHeight;
    const w=Math.min(tileWidth,width-x),h=Math.min(tileHeight,height-y);
    const exact=face&&Math.abs(face.width_mm-tileWidth*1000)<=25&&Math.abs(face.height_mm-tileHeight*1000)<=25;
    const cw=face&&!exact?Math.min(1,tileWidth*1000/face.width_mm):1;
    const ch=face&&!exact?Math.min(1,tileHeight*1000/face.height_mm):1;
    // Keep the production grain direction. Crop offsets are stable across reloads.
    const cropX=(1-cw)*random(),cropY=(1-ch)*random();
    tiles.push({row,col,x,y,width:w,height:h,face,face_id:face?.id||null,
      crop:[cropX,cropY,cw*w/tileWidth,ch*h/tileHeight],illustrative_cut:!!face&&!exact});
  }
  return tiles;
}
