// Author and verify the human exchange tables with the workspace artifact tool.
// Operational re-exports also work without Node through backend/cli.py export.
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire}from'node:module';
import {homedir}from'node:os';
const require=createRequire(import.meta.url);
const runtime=process.env.ARTIFACT_NODE_MODULES||path.join(homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const {Workbook}=await import(require.resolve('@oai/artifact-tool',{paths:[runtime]}));
const out=path.resolve(import.meta.dirname,'../data/exports');
const tables=JSON.parse(await fs.readFile(path.join(out,'tables.json'),'utf8'));
const wb=Workbook.create(),written=[];
const text=v=>v==null?'':v instanceof Date?v.toISOString():String(v);
const same=(a,b)=>text(a)===text(b)||(typeof b==='string'&&/^\d{4}-\d{2}-\d{2}T/.test(b)&&Date.parse(text(a))===Date.parse(b));
const csv=matrix=>'\uFEFF'+matrix.map(row=>row.map(v=>{const s=text(v);return /[",\r\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;}).join(',')).join('\r\n')+'\r\n';
for(const [name,rows]of Object.entries(tables)){
  const headers=Object.keys(rows[0]),matrix=[headers,...rows.map(r=>headers.map(h=>r[h]))];
  const sheet=wb.worksheets.add(name),range=sheet.getRangeByIndexes(0,0,matrix.length,headers.length);
  range.setNumberFormat('@');range.values=matrix;const stored=range.values;
  for(let r=0;r<matrix.length;r++)for(let c=0;c<headers.length;c++)if(!same(stored[r]?.[c],matrix[r][c]))throw Error(`Cell changed: ${name}, row ${r+1}, field ${headers[c]}: ${JSON.stringify(stored[r]?.[c])} != ${JSON.stringify(matrix[r][c])}`);
  written.push({name,rows:rows.length,columns:headers.length,matrix:stored});
}
wb.recalculate();
const check=await wb.inspect({kind:'region',sheetId:'questions',range:'A1:D3',maxChars:1300,tableMaxRows:3,tableMaxCols:4});
console.log(check.ndjson);
for(const t of written)await fs.writeFile(path.join(out,t.name+'.csv'),csv(t.matrix));
await fs.writeFile(path.join(out,'manifest.json'),JSON.stringify({source:'../showroom.sqlite',revision:tables.products[0].base_revision,encoding:'UTF-8 with BOM',units:'millimetres, degrees',tables:written.map(({matrix,...t})=>t)},null,2));
console.log(JSON.stringify({tables:written.length,records:written.reduce((n,t)=>n+t.rows,0),verified:true}));
