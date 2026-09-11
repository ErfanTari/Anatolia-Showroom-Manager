# Showroom foundation — team readiness and decisions

Working coordination pack · 7 September 2026

Companion to the [foundation plan](</Users/erfan.tari/Projects/Showroom/Showroom_Main_repo/docs/planning/Showroom_Foundation_Plan.md>). The lists below are proposed assignments to **roles**, not messages sent to people or commitments made on their behalf.

Confirmed: APS pilot; Prime/Commercial positioning plus independent Hit; Merch authority above showroom management; the system must independently design a complete showroom. The immediate shared objective is an APS simulation and a validated refresh scenario that establish reusable standards for full autonomous design.

## 1. Decision ownership

| Decision | Accountable role | Contributors | Operational rule |
|---|---|---|---|
| What must be represented and where emphasis belongs | Merch lead | Product, Sales, Design | Merch publishes assortment and priority policy |
| Product identity, status and technical use | Product master/technical owner | Merch, manufacturing | Imported specification conflicts go back to this owner |
| Fixture geometry, mounting and approved room recipes | Design standards lead | Fixture supplier, fabrication, Merch | Publish versioned reusable standards |
| What is physically installed | Showroom manager as observer; designated verifier where required | Installer, Merch | Evidence becomes observation history even when noncompliant |
| Routine change release | Merch-controlled policy; named release owner still needed | Showroom manager, logistics | Autonomous generation is always available; execution limits must be explicit |
| Spend, purchase and fabrication release | Named budget/procurement owner, to be confirmed | Merch, logistics, finance | A generated BOM alone does not authorize an order |
| Data contracts, engine behavior and application reliability | Development/product-system owner | All domain owners | No guessed physical or business rule becomes authoritative data |

Design contributes reusable knowledge at the beginning and when a genuinely new fixture or room pattern is introduced. Routine layout and product assignment should then be performed by the system.

## 2. Merch checklist

| Priority | To do | Concrete deliverable | Ready when |
|---|---|---|---|
| P0 | Name a Merch owner and backup | Owner register | Rule questions have a clear decision-maker |
| P0 | Define APS's target assortment | Design/color list with required/desirable status and market scope | “Show everything” has an explicit denominator |
| P0 | Assign positioning and Hit | Prime/Commercial list plus independent Hit dates/scope | Unknown classifications are marked, not guessed |
| P0 | Define exposure goals | Entry-visible surfaces, front rack positions, live-scene roles | Hit and Prime placement can be judged objectively |
| P0 | Approve color-series order | Series membership, warm/neutral grouping, rank and exceptions | A person can lay out one run using only the specification |
| P0 | Define refresh boundaries | Locked surfaces, maximum moves, routine budget, renovation scope | Planner knows what it may change |
| P0 | Give example design decisions | 10–15 accepted/rejected placement examples with reasons | Examples explain both expected outcome and tradeoff |
| P0 | Clarify missing-capacity policy | Required versus desirable coverage and escalation route | Infeasible designs have a useful next action |
| P1 | Define repeat exposure | When another finish, size or application adds value; maximum repetitions | Extra slots are allocated consistently |
| P1 | Define launch/discontinue policy | Date logic, market applicability, phase-out timing, renovation exceptions | Status changes have predictable consequences |
| P1 | Define authority and exception policy | Release limits, local manager permissions, Merch locks and expiry | The system can distinguish routine work from exceptions |
| P1 | Define task and communication rules | Owner roles, dependencies, due-date logic, notification channels | A proposed swap creates a meaningful work package |
| P2 | Define sales influence | Allowed metric, review period, cap, launch exploration allocation | Sales cannot unintentionally erase brand/launch objectives |
| P2 | Review recurring exceptions | Rule revision candidates and accepted counterexamples | Knowledge improves rather than accumulating unexplained overrides |

**Merch workshop exercise:** choose one good APS bay and one that should improve. For each, explain focal product, supporting products, order, finish mix, duplicates, and what should stay unchanged. Then test a new Hit product, a discontinued finish, two spare positions, a reduced budget and an unavailable slab. Capture the rule that explains each answer, not only the answer itself.

## 3. Design checklist

| Priority | To do | Concrete deliverable | Ready when |
|---|---|---|---|
| P0 | Confirm terminology and fixture variants | Illustrated seven-type glossary | Waterfall, fixed faces and rotating motion are unambiguous |
| P0 | Establish APS coordinates and evidence | Measured envelope, origin, axis, levels, drawing revision | Known dimensions and approximations are distinguishable |
| P0 | Survey the first pilot area | Fixture IDs, mounting surfaces, panel sequence, photos | A physical position can be matched to one record |
| P0 | Specify all seven template types | Dimensions, usable areas, sides, capacity, motion and support rules | Another person could model each fixture without guessing |
| P0 | Verify sliding and rotating mechanics | Manufacturer limits or measurements; movement sketch/video reference | The viewer and clearance checks use the correct motion |
| P0 | Define installation suitability inputs | Application criteria by SKU/finish and relevant conditions | Floor/furniture/fireplace rules refer to approved evidence |
| P0 | Define material mapping rules | True texture scale, orientation, face variants, grout, finish presets | A tile is not stretched into an arbitrary slab |
| P1 | Author first room recipes | Bathroom/vanity, lounge/fireplace, meeting/table, product library | Each has material roles, geometry dependencies and allowed variations |
| P1 | Define space planning rules | Entrances, paths, services, clearance envelopes, fixed/movable boundaries | A shell layout can be validated against a complete input set |
| P1 | Supply reusable models | Lightweight GLB plus editable source and dimensions | Model surfaces map to stable template component names |
| P1 | Define standard furniture assemblies | Basin, counter, table: components, edges, cutouts, supports, joins | Quantities and texture continuity are traceable |
| P1 | Define branded appearance | Typography, colors, labels, lighting/camera presets, approved references | Simulation can be visually reviewed against an agreed target |
| P2 | Publish fabrication recipes | Verified cutting layouts, kerf, waste assumptions, spare policy, pack units | Standard output can be classified as fabrication-ready |
| P2 | Create holdout briefs | Measured shells and expected minimum requirements | Autonomous design is evaluated beyond one memorized APS example |

Do not spend the first week creating photoreal models of every chair. Accurate fixture dimensions, addressable surfaces, material scale and motion have greater initial value. Simple neutral furniture can establish composition while detailed assets are prepared.

## 4. Our development checklist

| Priority | To do | Concrete deliverable | Ready when |
|---|---|---|---|
| P0 | Register every pilot source and revision | Source register and conflict log | A value can be traced to a file/page/row or field observation |
| P0 | Reconcile product aliases and source counts | Raw-to-canonical mapping with exclusions and unresolved items | Viewer/workbook/physical counts are not conflated |
| P0 | Define IDs, units and state contracts | Schema draft and example records | Every view and import has the same meaning for a slot and placement |
| P0 | Design standard imports | Column dictionary, validation messages, preview/commit behavior | Repeated import is safe and foreign-key conflicts are visible |
| P0 | Build canonical pilot storage | SQLite migrations and attributed records | Records cannot silently overwrite another authority's fields |
| P0 | Generate one scene manifest | Shared 2D/elevation/3D input and selection IDs | No separate hardcoded product order survives in the pilot |
| P0 | Build APS Simulation Template 0.1 | A bounded interactive pilot plus seven-type test scene | Geometry confidence and current/scenario state are visible |
| P1 | Implement rule evaluator and planner | Eligibility, grouped assignments, ordering, coverage, stable explanations | Merch's agreed examples pass and conflicts are explained |
| P1 | Produce complete change sets | Before/after state, quantities, reservations, dependent tasks | A displaced item has a recorded destination/disposition |
| P1 | Add manager and Merch flows | Observation, proposal, lock, exception, release, verification | Managers can report truth; Merch authority is enforced |
| P1 | Establish reliability | Revision checks, idempotency, history, backups, restore, delivery outbox | Concurrent edits/retries do not corrupt state or duplicate work |
| P1 | Build autonomous layout generation | Brief → fixture count/template selection → geometry → product assignment | Empty-shell milestone needs no manual position/assignment step |
| P2 | Standardize second showroom onboarding | Reusable template and import configuration | No bespoke showroom UI or product-array patch is needed |
| P2 | Connect feedback and sales | Small capture flow, attributed sales snapshots, transparent metrics | Context, sample size and data dates are visible |
| P2 | Add MCP and agent evaluation | Typed domain tools and permissions; evaluated design/coordination prompts | Agent proposals pass the same rules and cannot bypass release policy |

Initial work can use all existing showrooms as read-only source examples while only the verified APS pilot is eligible for operational recommendations.

## 5. Materials register

“Available” below means present in the repository, not verified against today's showroom.

| Pack | Available now | Still needed | Owner | What it unlocks |
|---|---|---|---|---|
| APS space | Layout reference and drawing PDF | As-built measurements, confirmed entrances/services, current revision | Design + manager | Accurate placement and autonomous layout |
| Current assignments | BOMs, generated data, photographs | Field confirmation, empty/blocked slots, resolved ordering | Manager + Merch | Trustworthy current state |
| Product master | Product numbers, names, finishes, sizes in existing data | Canonical export, lifecycle, actual dimensions, technical use | Product owner | Eligibility and lifecycle redesign |
| Priorities | Intent described in this discussion | Real Prime/Commercial/Hit assignments and target assortment | Merch | Strategic placement |
| Color sequences | Images and existing product group names | Approved series membership, temperature group and rank | Merch + Design | Deterministic adjacency |
| Fixtures | Photos, drawings, counts and an SVG rack mockup | Verified template dimensions, mounting capacities, pivots/travel | Design/supplier | Correct 3D and motion |
| Material assets | Product and sliding images | SKU/face mappings, true physical crop size, finish presets, missing faces | Product imagery + Design | Trustworthy texture scale and surface variation |
| Furniture | Photos and some BOM surface references | Standard basin/counter/table assemblies, cutouts and supports | Design/fabrication | Complete room generation |
| Quantity/supply | Source BOM quantity information to preserve | Pack sizes, waste/spare standards, stock, lead times, cost bands | Logistics + fabrication | Executable work packages |
| Launch example | Tuscano Rosso media | Confirmed name/SKUs, release date, stock, real priority | Product owner + Merch | Real launch pilot; media alone supports only a simulation |
| Operations | No shared operational backend identified in reviewed app | Roles, accounts, field language, device/connectivity, notification channel | Merch + IT + manager | Field loop and deployment |
| Performance | No canonical sales/feed source established in review | Metric definition, export sample, units, attribution and period | Sales/data owner | Governed performance-based prioritization |

### Minimum input for a useful simulation now

- Existing APS geometry as an explicitly provisional reference.
- Existing panel textures with a reviewed mapping for the pilot products.
- Stable pilot fixture/slot IDs and a declared current/scenario distinction.
- Simple parametric objects using known dimensions; unknown mechanics stay visibly provisional.
- One candidate rule profile using clearly marked test priorities until Merch provides real classifications.

This can show the design and interaction model. It cannot yet claim a verified as-built showroom, real launch recommendation, physical fit, or construction-ready quantity package.

## 6. Starter templates to prepare

These are field contracts for the next implementation step. They intentionally do not introduce another editable source of truth before the schema is agreed.

| Template | Minimum fields |
|---|---|
| Showroom brief | Showroom ID, market, objectives, measured shell revision, target assortment version, budget/currency, required zones, locked elements, desired date, objective profile |
| Merch range | Design ID, positioning, Hit flag or campaign, market/showroom scope, valid dates, required/desirable coverage, minimum useful exposure, duplication limits |
| SKU master import | Source SKU, canonical design ID, finish, nominal and actual sizes, thickness, units, lifecycle/effective dates, application references, source revision |
| Color-series order | Series ID, design ID, temperature group, group rank, within-group rank, permitted breaks, owner, version |
| Fixture standard | Template ID/version, type, dimensions, components/sides, capacities, mounting limits, motion/clearance, accepted assemblies, source/evidence |
| Current-state survey | Showroom/fixture/slot, observed SKU or unknown, quantity/unit, condition, observation time, observer, evidence, confidence, prior revision |
| Rule card | ID/version, objective, scope, strength, recognized type, parameters, rationale, source, owner, examples, exceptions |
| Change package | Plan revision, base state, add/remove/move/retain, quantities and units, costs, dependencies, reservations, owners, target dates |
| Customer feedback | Showroom, optional slot, SKU or design, time, exposure type, category, sentiment/interest, optional note |

## 7. First ten working days

This is a proposed kickoff sequence, not a calendar booking. If an input is delayed, use the time for independent template work; do not replace the missing fact with an unmarked guess.

| Window | Merch | Design / manager | Our side | Joint review output |
|---|---|---|---|---|
| Days 1–2 | Pilot brief, range priorities, locks | Terminology, source revisions, pilot location survey | Source/conflict register, schema draft | Agreed pilot boundary and input owners |
| Days 3–4 | Color run and accepted/rejected examples | Sliding/fixed measurements and scene material roles | IDs, alias mapping, import preview, first scene manifest | One fixture's slots/products align across source and view |
| Days 5–6 | Review visibility and diversity metrics | Verify one live scene and motion requirements | 2D/elevation/basic 3D; current/scenario switch | First visible simulation reviewed against photos/measurements |
| Days 7–8 | Launch, discontinue and spare-slot policies | Review eligibility and physical limits | Rule evaluator, scenario candidates, explanations | No hidden rule conflict or invented placement |
| Days 9–10 | Accept or correct design reasoning | Confirm pilot mapping and asset gaps | Integrated demo; backlog and estimate revision | Decision to expand APS coverage and implement operational loop |

A useful Day 10 demonstration selects one product in 3D, shows all its APS occurrences, proposes a compatible replacement in a scenario, explains the choice, and displays the corresponding work preview. This is a target; successful completion depends on the pilot inputs and implementation capacity.

## 8. Decisions that matter most

Ask these in small groups as their implementation boundary approaches. The first three high-level questions have already been answered in this discussion and should not be asked again.

| Decision still needed | Suggested working position | Why / latest sensible moment |
|---|---|---|
| Who owns canonical SKUs and lifecycle? | Product/ERP/PIM owner; keep temporary records attributed | Before real product recommendations |
| What does APS have to represent? | Required designs plus selected finishes/applications; desirable extras | Before evaluating coverage |
| Which physical areas are currently changeable? | Movable display products first; permanent floors/walls locked for routine refresh | Before a real change proposal |
| How is Hit scoped and how long does it last? | Market/showroom/campaign with effective dates | Before production scoring |
| Does front of a sliding bank mean rail position, first visible closed face, or presentation sequence? | Record each separately; Merch chooses exposure policy | Before visibility scoring |
| Which fixture models are standard variants? | Measured dimensions and mechanics per template version | Before physical-fit or full-layout validation |
| How should color families break when a run is too small? | Explicit Merch fallback; do not silently break a mandatory group | Before constrained ordering |
| Who can release routine work, at what spend/move limit? | Merch-owned policy, with automatic release only where explicitly defined | Before operational release or procurement integration |
| Can dealer managers rearrange locally? | Record all actual changes; requests/permissions remain scoped by Merch | Before manager write access |
| Where will the application run and who signs in? | Private operational application; SQLite beside its backend initially | Before remote field use |
| Which language and capture method work in the showroom? | Turkish/English-ready labels; mobile selection/QR plus spreadsheet import | Before field usability pilot |
| Are stock, samples and bookmatch faces identifiable? | Use inventory references where available; mark availability unknown otherwise | Before supply commitments |
| What counts as an acceptable complete design? | Hard constraints satisfied; required brief complete; quality examples agreed | Before autonomous layout acceptance |
| How many users/writes/showrooms and what uptime are expected? | Measure pilot usage; choose deployment from actual access needs | Before production architecture sizing |
| Which sales export is reliable and attributable? | Begin with clearly labeled regional/company context if showroom attribution is absent | Before sales affects ranking |
| Which notifications and recipients are desired? | Role-based actionable alerts, not repeated unchanged status | Before connecting a communication channel |

## 9. Coordination rhythm and evidence of progress

Use a short weekly decision review with one representative from Merch, Design, the showroom and development. Review only: the latest visible result, unresolved factual gaps, rejected/accepted design examples, and decisions that block the next gate. Maintain a named owner and due date for each open input.

Use four shared registers: **sources/conflicts**, **rules/examples**, **templates/asset readiness**, and **pilot changes/issues**. A rule disagreement should produce an example and a decision; a missing dimension should produce a survey task; a rendering issue should remain a rendering issue. This keeps business judgment, physical facts and implementation defects understandable.

The first meaningful success is a verified APS area and one complete refresh decision that Merch can explain, a manager can implement, and the system can verify. The subsequent required success is a complete design generated from a measured shell using the accumulated standards.
