// Smoke-tests the Showroom Manager outside a browser.
//
//     node tools/check_showrooms.js
//
// Loads the real data files, runs products/renderVals for every showroom, and
// asserts that:
//   - every {{ binding }} used in the template resolves
//   - every data group is claimed by exactly one non-muted plan zone, and every
//     product is therefore reachable by clicking the plan
//   - no two labelled zones overlap and none escape the plan box
//   - every zone / station / panel selection produces a non-empty context panel
//   - the detail modal opens and "Locate on Floor Plan" finds a target
//   - every facet value, format highlight and section renders without throwing
//   - switching showrooms back and forth does not leak the memoised products
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const REPO = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(REPO, 'Showroom Manager.dc.html'), 'utf8');

// ---- minimal browser surface -------------------------------------------------
const listeners = {};
const win = {
  addEventListener: (k, f) => { (listeners[k] = listeners[k] || []).push(f); },
  removeEventListener: (k, f) => { listeners[k] = (listeners[k] || []).filter(x => x !== f); },
};
const doc = {
  getElementById: () => null,
  querySelector: () => null,
  createElement: () => ({ setAttribute(){}, appendChild(){}, classList:{toggle(){},add(){},remove(){}}, style:{}, querySelectorAll:()=>[], querySelector:()=>null }),
  createElementNS: () => ({ setAttribute(){}, appendChild(){}, dataset:{} }),
  contains: () => false,
};
const React = { createElement: (t, p, ...c) => ({ t, p, c }), Fragment: 'Fragment', isValidElement: () => false };
class DCLogic {
  constructor(props){ this.props = props || {}; }
  setState(u){ const p = typeof u === 'function' ? u(this.state) : u; this.state = Object.assign({}, this.state, p); }
}

const ctx = vm.createContext({
  window: win, document: doc, React, DCLogic, console,
  setTimeout: () => 0, clearTimeout: () => {}, requestAnimationFrame: () => {},
  Set, Map, Object, Array, Math, String, Number, JSON, RegExp, Boolean, Error, isNaN, parseInt, parseFloat,
});
ctx.window.window = ctx.window;
ctx.globalThis = ctx;

// data files, in helmet order
for (const f of ['showroom-data.js', 'data/showroom-manisa.js', 'data/showroom-ekinox.js',
                 'data/showroom-ankara.js', 'data/showroom-turkuaz.js', 'showrooms.js']) {
  vm.runInContext(fs.readFileSync(path.join(REPO, f), 'utf8'), ctx, { filename: f });
}

const src = html.match(/<script type="text\/x-dc"[^>]*>\n([\s\S]*?)\n<\/script>/)[1];
vm.runInContext(src + '\n;globalThis.__Component = Component;', ctx, { filename: 'component.js' });

// ---- collect every {{ binding }} used in the template ------------------------
const tpl = html.slice(html.indexOf('<x-dc>'), html.indexOf('</x-dc>'));
const roots = new Set();
// sc-for introduces a local alias; those are resolved per-item, not from renderVals.
const aliases = new Set([...tpl.matchAll(/<sc-for[^>]*\bas="([^"]+)"/g)].map(m => m[1]));
const literals = new Set(['true', 'false', 'null', 'undefined']);
for (const m of tpl.matchAll(/\{\{\s*([A-Za-z_$][\w$]*)/g)) {
  if (!aliases.has(m[1]) && !literals.has(m[1])) roots.add(m[1]);
}

// ---- run every showroom ------------------------------------------------------
let fail = 0;
const ids = ctx.window.SHOWROOMS.map(s => s.id);
for (const id of ids) {
  const c = new ctx.__Component({ accent: '#A07E5A', density: 'Comfortable', showTextures: true });
  c.state = { view: 'app', section: 'floorplan', showroomId: id,
    filters: { collection:'All', format:'All', colour:'All', finish:'All', size:'All', room:'All' },
    selected: null, hiFormat: null, dataReady: true, sel: null, openGroups: {}, lightbox: null,
    galleryRoom: 1, galleryPhoto: {}, galleryHover: null };

  const P = c.products;
  const v = c.renderVals();
  const missing = [...roots].filter(k => v[k] === undefined);
  const zones = c.planZones;
  const clickable = zones.filter(z => z.type !== 'muted');

  console.log(`\n=== ${id} — ${c.meta.name} ===`);
  console.log(`  products ${P.length}  |  formats ${new Set(P.map(p=>p.fmt)).size}  |  collections ${new Set(P.map(p=>p.col)).size}` +
              `  |  zones ${zones.length} (${clickable.length} clickable)  |  nav ${v.navItems.map(n=>n.label).join('/')}`);
  if (missing.length) { console.log('  MISSING BINDINGS:', missing.join(', ')); fail++; }

  // every product must be reachable from exactly one zone (non-APS)
  if (id !== 'aps') {
    const groups = new Set(c.dataGroups.map(g => g.key));
    const claimed = new Map();
    clickable.forEach(z => (z.keys || []).forEach(k => claimed.set(k, (claimed.get(k)||0) + 1)));
    const orphan = [...groups].filter(k => !claimed.has(k));
    const dupe = [...claimed].filter(([, n]) => n > 1).map(([k]) => k);
    const ghost = [...claimed.keys()].filter(k => !groups.has(k));
    if (orphan.length) { console.log('  ORPHAN GROUPS (no zone):', orphan.join(', ')); fail++; }
    if (dupe.length)   { console.log('  GROUPS IN >1 ZONE:', dupe.join(', ')); fail++; }
    if (ghost.length)  { console.log('  ZONE KEYS WITH NO GROUP:', ghost.join(', ')); fail++; }
    const reach = clickable.reduce((n, z) => n + c.zoneProducts(z).length, 0);
    if (reach !== P.length) { console.log(`  UNREACHABLE: ${P.length - reach} of ${P.length} products not on any zone`); fail++; }
  }

  // Zone boxes must stay inside the plan and must not overlap another *labelled*
  // zone — an overlap hides one of the two captions on the rendered plan.
  for (const z of zones) {
    if (z.x < 0 || z.y < 0 || z.x + z.w > 100 || z.y + z.h > 100) {
      console.log(`  ZONE OUT OF BOUNDS: ${z.id} (${z.x},${z.y} ${z.w}x${z.h})`); fail++;
    }
  }
  for (let i = 0; i < zones.length; i++) for (let j = i + 1; j < zones.length; j++) {
    const a = zones[i], b = zones[j];
    // A floor field is meant to sit under things; skip that pairing.
    if (a.type === 'floor' || b.type === 'floor') continue;
    const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
    const oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
    if (ox > 0.5 && oy > 0.5) { console.log(`  ZONES OVERLAP: ${a.id} / ${b.id} (${ox.toFixed(1)}% x ${oy.toFixed(1)}%)`); fail++; }
  }

  // exercise every zone / station selection and the detail modal
  const sels = id === 'aps'
    ? [{type:'system',key:'s160'},{type:'system',key:'s120'},{type:'system',key:'wf'},{type:'system',key:'rot'},
       {type:'system',key:'tower'},{type:'floor',key:'floor'},{type:'panel',key:0},...c.STN.map(s=>({type:'station',key:s.id}))]
    : clickable.map(z => ({ type: z.type, key: z.id }));
  for (const sel of sels) {
    c.state.sel = sel;
    try {
      const vv = c.renderVals();
      const n = (vv.ctx.items||[]).length || (vv.ctx.groups||[]).reduce((a,g)=>a+g.items.length,0) || (vv.ctx.faces||[]).length;
      if (!vv.ctx.isEmpty && n === 0) { console.log(`  EMPTY PANEL for ${sel.type}:${sel.key}`); fail++; }
    } catch (e) { console.log(`  THREW on ${sel.type}:${sel.key} — ${e.message}`); fail++; }
  }
  c.state.sel = null;

  // detail modal + "locate on plan" for a sample of products
  for (const p of P.filter((_, i) => i % Math.max(1, Math.floor(P.length / 12)) === 0)) {
    c.state.selected = p.id;
    try {
      const vv = c.renderVals();
      if (!vv.selOpen) { console.log(`  detail did not open for ${p.id}`); fail++; }
      c.viewSelOnPlan();
      if (c.state.sel === null && !p.station) { console.log(`  no plan target for ${p.n} (${p.fmt}, group=${p.group})`); fail++; }
      c.state.section = 'floorplan';
    } catch (e) { console.log(`  THREW on detail ${p.n} — ${e.message}`); fail++; }
  }
  c.state.selected = null; c.state.sel = null;

  // every facet value + format highlight must render
  for (const f of c.FMT) { c.state.hiFormat = f; c.renderVals(); }
  c.state.hiFormat = null;
  for (const key of ['collection','format','colour','finish','size','room']) {
    const vals = [...new Set(P.map(p => p[{collection:'col',format:'fmt',colour:'colour',finish:'f',size:'sz',room:'room'}[key]]))];
    for (const val of vals) { c.state.filters = Object.assign({}, c.state.filters, { [key]: val }); c.renderVals(); }
    c.state.filters = Object.assign({}, c.state.filters, { [key]: 'All' });
  }

  // sections
  for (const s of v.navItems.map(n => n.label)) {
    c.state.section = { 'Overview':'overview','Gallery':'gallery','Floor Plan':'floorplan','Sliding Panels':'sliding','Beyond':'beyond' }[s];
    try { c.renderVals(); } catch (e) { console.log(`  THREW on section ${s} — ${e.message}`); fail++; }
  }
}

// switching between showrooms must not leak state
{
  const c = new ctx.__Component({ accent: '#A07E5A' });
  c.state = { view:'app', section:'overview', showroomId:'aps',
    filters:{collection:'All',format:'All',colour:'All',finish:'All',size:'All',room:'All'},
    selected:null, hiFormat:null, dataReady:true, sel:null, openGroups:{}, lightbox:null,
    galleryRoom:1, galleryPhoto:{}, galleryHover:null };
  const counts = {};
  for (const id of [...ids, ...ids.slice().reverse()]) {
    c.switchShowroom(id);
    const n = c.products.length;
    if (counts[id] !== undefined && counts[id] !== n) { console.log(`  CACHE LEAK: ${id} gave ${counts[id]} then ${n}`); fail++; }
    counts[id] = n;
    c.renderVals();
  }
  console.log('\nswitch cycle:', Object.entries(counts).map(([k,n])=>`${k}=${n}`).join('  '));
}

console.log(fail ? `\n${fail} FAILURE(S)` : '\nALL CHECKS PASSED');
process.exit(fail ? 1 : 0);
