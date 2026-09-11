import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { homedir } from 'node:os';
const require=createRequire(import.meta.url);
const runtime=process.env.ARTIFACT_NODE_MODULES||path.join(homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const {Workbook}=await import(require.resolve('@oai/artifact-tool',{paths:[runtime]}));

const root=path.resolve(import.meta.dirname,'..');
const input=JSON.parse(await fs.readFile(path.join(root,'tmp/source-review/assortment-grids.json'),'utf8'));
const options=JSON.parse(await fs.readFile(path.join(root,'tmp/source-review/assortment-options.json'),'utf8'));
const out=path.join(root,'output/assortment');
await fs.mkdir(path.join(out,'tabs'),{recursive:true});
const cell=v=>v===null||v===undefined?'':typeof v==='boolean'?(v?'TRUE':'FALSE'):String(v);
const csv=rows=>'\uFEFF'+rows.map(row=>row.length===1&&cell(row[0])===''?'""':row.map(v=>{const s=cell(v);return /[",\r\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;}).join(',')).join('\r\n')+'\r\n';
const column=n=>{let s='';for(;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
const wb=Workbook.create();
const manifest={source_workbook:input.source,source_sha256:input.sha256,export_date:'2026-09-09',encoding:'UTF-8 with BOM',delimiter:',',formula_policy:'Source cached values; exact original formulas preserved in formula_metadata.json. No recalculation or source editing.',sheets:[]};
for(const [i,g]of input.sheets.entries()){
  const ws=wb.worksheets.add(g.sheet);
  const range=ws.getRange(`A1:${column(g.column_count)}${g.row_count}`);
  if(g.rows.some(row=>row.some(v=>v!==null&&v!==''))) range.values=g.rows;
  const stored=range.values;
  const actual=Array.from({length:g.row_count},(_,r)=>Array.from({length:g.column_count},(_,c)=>stored[r]?.[c]??null));
  for(let r=0;r<g.row_count;r++)for(let c=0;c<g.column_count;c++)if(cell(actual[r][c])!==cell(g.rows[r]?.[c]))throw Error(`Value changed at ${g.sheet}!${column(c+1)}${r+1}`);
  const filename=`${String(i+1).padStart(2,'0')}_${g.sheet.replace(/[^A-Za-z0-9_-]+/g,'_')}.csv`;
  await fs.writeFile(path.join(out,'tabs',filename),csv(actual));
  manifest.sheets.push({sheet:g.sheet,csv:`tabs/${filename}`,rows:g.row_count,columns:g.column_count,source_state:g.state,nonempty_rows:g.rows.filter(r=>r.some(v=>v!==null&&v!=='')).length});
}
const headers=Object.keys(options[0]);
const ws=wb.worksheets.add('Extracted options');
const matrix=[headers,...options.map(r=>headers.map(h=>r[h]))];
ws.getRange(`A1:${column(headers.length)}${matrix.length}`).values=matrix;
await fs.writeFile(path.join(out,'assortment_options.csv'),csv(ws.getRange(`A1:${column(headers.length)}${matrix.length}`).values));
await fs.writeFile(path.join(out,'manifest.json'),JSON.stringify({...manifest,normalized_option_rows:options.length},null,2));
await fs.writeFile(path.join(out,'formula_metadata.json'),JSON.stringify(input.formulas,null,2));
console.log(JSON.stringify({exported_tabs:manifest.sheets.length,option_rows:options.length,retained_formulas:input.formulas.length,source_cells_verified:input.sheets.reduce((n,s)=>n+s.row_count*s.column_count,0)}));
