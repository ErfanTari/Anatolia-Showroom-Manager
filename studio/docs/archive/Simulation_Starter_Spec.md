# APS Simulation Template 0.1 — starter specification

Proposed build brief · 7 September 2026

This is a specification for the next implementation, not an implemented 3D simulator or a verified geometry model. It accompanies the [foundation plan](</Users/erfan.tari/Projects/Showroom/Showroom_Main_repo/docs/planning/Showroom_Foundation_Plan.md>).

## 1. What the first template must prove

Build an interactive, textured APS pilot from one scene manifest. Selecting an object in the plan, elevation or 3D view resolves to the same fixture, slot, product and revision. Switching a proposed product updates all three views. The current installation remains separately available.

Two scene presets serve different purposes:

- **APS pilot:** one sliding bank, representative fixed A/B panels, an approved color series and one live room scene placed against the current APS reference. Initially mark unverified measurements and placements as provisional.
- **Fixture test room:** one example of all seven display types, arranged in a simple synthetic room. Clearly label this as a test room, with no claim that it reproduces an Anatolia showroom or uses approved dimensions beyond supplied standards.

Reuse existing APS/product imagery. Do not make a second hardcoded product list for the simulation. The current six sliding-order disagreements must be resolved through source/field reconciliation before those positions are described as confirmed.

## 2. Scene and geometry conventions

- Persist architectural dimensions in millimeters; declare the coordinate system and convert once to meters for the renderer.
- Use a right-handed runtime frame: Y up; X and Z on the floor. Define the origin and plan-north transform per showroom. Do not interchange plan Y and world Y implicitly.
- Each instance references a template ID/version, immutable object ID, display address, parent, transform, geometry confidence, source and revision.
- Separate visible geometry, product-bearing surfaces, collision footprints, and operating/maintenance clearance envelopes.
- Treat walls/floors as real surfaces or polygons, not capacity-only boxes. Complex cuts can remain simplified visually while their dimensional status is disclosed.
- Store fixture placement separately from panel movement. Moving a sliding panel for inspection must not alter its recorded installation location.
- Keep texture mapping in physical units. Record whether a source image depicts one full tile/slab, a cropped region, or a repeatable pattern.
- A surface selection carries stable application/slot identity. Mesh indexes and array positions are temporary rendering details.

## 3. The seven fixture contracts

| Type | Components and assignable material areas | Required parameters | Interaction / critical behavior |
|---|---|---|---|
| Live installation | Zone surfaces: floor, each wall, optional fireplace/TV surrounds; props as separate objects | Room envelope, openings, surface polygons, material roles, tile/slab layout, grout, services, template constraints | Enter/isolate scene; select each application; display correct material scale; preserve room composition |
| Fixed panel | Frame, panel component, independently addressed side A and side B | Usable width/height, substrate/thickness, mounting method, physical-piece sharing, position/angle | View both sides; separate product assignments; never infer quantity or bookmatch from appearance alone |
| Sliding panel | Rack/books/rails, ordered panel components, assignable faces | Actual display size, capacity, rail order and visibility, travel axis/distance, thickness/load acceptance, stops/clearances | Open/close selected panel along its real travel; expose full face; show closed-state versus opened exposure |
| Rotating panel | Base/frame, pivoted carrier, 120 × 120 cm display when specified by the verified model | Pivot position/axis, vertical and horizontal poses, angle limits, carrier dimensions, support/clearance | Tilt from vertical display into the floor-demonstration pose and back; check swept volume rather than merely spinning around a vertical pole |
| Tower | Cabinet, shelves/drawers/pockets, individual cut sample slots | Slot structure, sample dimensions, per-pocket quantity capacity, access direction, represented finish/design | Select a sample; show missing/damaged/available state; no automatic claim that one tower row covers the catalog |
| Waterfall | Linked three-panel assembly, freestanding or directly wall-mounted | Per-panel width/height, relative angles, offsets/gaps, supported faces, direction/order, fixing/clearance | Inspect the three side-by-side panels; preserve linked ordering; model the wall-mounted subtype explicitly |
| Slab furniture | Assembly for basin, counter or table: top, sides, fascia, edges, cutouts, supports | Standard dimensions, component polygons, slab thickness, join/edge rules, cutout/support constraints, face/orientation mapping | Select the assembly or component; preserve material continuity; show bill of materials and fabrication maturity |

The user's reference sizes are 120 × 280 cm mini-slabs, 160 × 320 cm slabs, and 120 × 120 cm rotating floor displays. Treat these as relevant nominal product sizes, not the external dimensions or capacities of every rack. Existing records also contain other product and cut sizes, including 162 × 322 cm. Keep purchase size, usable mounting size and finished size distinct.

The observed APS waterfall count must be mapped to real triple-panel assemblies; do not assume 21 viewer rows automatically means seven physical units. The same principle applies to rotating units, towers and bookmatched surfaces.

## 4. Material and object inputs

### Material record

Required: material ID; canonical SKU/design reference; finish; face ID or explicitly unknown; image path; image's physical width/height; crop/rotation; image revision; provisional/approved status.

Optional refinements: roughness/normal maps, finish preset, directional texture metadata, approved bookmatch relationships, alternate production faces, edge appearance and displacement budget. Use a placeholder material when a texture is missing and label it in the inspector. Never quietly substitute a visually similar product.

For floor tiles, use correct tile dimensions and grout; vary faces using a stable seed and the available approved face set. For slabs, preserve full-face orientation and avoid unintended tiling. Polished/honed/silk representations can initially use reviewed finish presets; they are illustrative until assessed against reference samples.

### Reusable scene object

Required: template/version; named components; dimension parameters; fixed and movable parts; product-assignable surfaces; local transforms; bounding/clearance volumes; anchor points; source evidence; confidence.

For furniture or complex mechanical objects, retain an editable Design source plus a lightweight GLB for viewing. A revised model must keep or explicitly migrate component IDs and material slots.

### Visibility record

Start with Merch/Design-marked entry viewpoints and visible faces, plus closed/open rack states. Record the source and confidence of these exposure labels. Later add geometric sightline estimation with occlusion. A panel at the front of an array is not necessarily visible from the entrance.

## 5. Scene manifest field contract

This is a conceptual example; the values and IDs beginning with `example` are illustrative. Production validation and a machine-readable schema are implementation work.

```json
{
  "schema_version": "0.1-proposed",
  "scene_id": "example-aps-pilot",
  "showroom_id": "aps",
  "state_kind": "scenario",
  "plan_revision": "example-plan-001",
  "base_observation_revision": "example-observation-001",
  "geometry_revision": "example-survey-001",
  "units": "mm",
  "runtime_frame": "right-handed-y-up",
  "geometry_status": "provisional",
  "fixtures": [
    {
      "instance_id": "example-fixed-panel-01",
      "template_id": "example-fixed-double-sided",
      "template_version": "0.1",
      "address": "APS/GF/PILOT/FIXED/P01",
      "position_mm": [0, 0, 0],
      "rotation_degrees": [0, 0, 0],
      "slot_ids": ["example-slot-a", "example-slot-b"]
    }
  ],
  "slots": [
    {"slot_id": "example-slot-a", "side": "A", "state": "unknown"},
    {"slot_id": "example-slot-b", "side": "B", "state": "empty"}
  ],
  "assignments": [],
  "materials": [],
  "annotations": ["Demonstration structure; no approved fixture dimensions supplied"]
}
```

Production assignments reference slot/application ID, SKU, material asset, piece/assembly identity and any orientation/layout details. Actual observed occupancy is stored independently; the manifest is a generated projection of the selected state. Cache keys include geometry, template, material and assignment revisions.

## 6. First interaction flow

1. Open APS and see the selected state/date and verification coverage.
2. Click a panel in plan or 3D; its elevation and inspector open together.
3. See product, SKU, finish, dimensions, fixture address, source and latest observation.
4. Enter a scenario, select a compatible replacement, and see the affected views update.
5. Inspect coverage gains/losses and rule explanations; incompatible choices explain their rejection.
6. Compare Current and Scenario using identical camera positions.
7. Open the proposed work preview: product in/out, quantities, dependencies and unknown inputs.
8. In field mode, record what is actually there or add feedback. Role permissions control release separately.

Use a compact inspector and overlays instead of putting rule implementation details into the main shopping/manager experience. Show human language such as “This finish is not approved for this floor use” or “These three panels belong to one color sequence.”

## 7. Build order

| Step | Build | Reuse / dependency |
|---|---|---|
| 1 | Slot/assignment/material contracts and source map | Current data and pilot reconciliation |
| 2 | One fixed A/B panel and a parameterized sliding rack | Existing textures; verified template dimensions where available |
| 3 | Shared plan/elevation/3D selection and current/scenario switching | Same manifest for all views |
| 4 | One live scene with floor, walls and neutral furniture | APS references and Design role definitions |
| 5 | Correct rotating motion, tower slots, triple-panel waterfall | Mechanical measurements and fixture glossary |
| 6 | Parameterized basin/counter/table components | Design standard assemblies |
| 7 | Rule overlays, before/after comparison and work preview | Planner/validator interface |
| 8 | Branded finish, lighting, camera controls and performance pass | Approved visual references and target hardware |

The test room proves the general fixture vocabulary even if the first field-verified APS area uses only a subset. Continue expanding the same model until the complete showroom is represented.

## 8. Acceptance checks

- Every represented product surface selects the same stable record in all views.
- Changes in the scenario do not overwrite the current state.
- Front/back and ordering match the confirmed fixture map, including the APS positions currently in conflict.
- Texture scale and orientation are correct for at least one tile, full slab, mini-slab and cut sample.
- Sliding and rotating states use the correct axes and have visible operating envelopes in inspection mode.
- Waterfall is three angled adjacent panels, with a wall-mounted alternative.
- Furniture and multi-surface walls can reference linked material applications without duplicate procurement counts.
- Empty, unknown, missing-texture and provisional geometry states are distinguishable.
- A floor/live-use swap cannot appear validated if application eligibility is unknown.
- Mouse and touch users can select, inspect, open/close and compare without relying on hover alone.
- Test on the actual Merch laptop and field phone/tablet. Proposed target: responsive selection and at least 30 fps in the pilot scene; measure before committing larger-scene budgets.
- Exported scene data reloads with the same identities and assignments. A rendering export never becomes an unreviewed change to operational records.

## 9. Growth into complete autonomous design

The simulator's object contracts are also the design engine's building blocks. Add a brief-driven template selector, candidate fixture positions, circulation checks, visibility estimation and product assignment using these same objects. Each generated complete layout becomes another versioned scene manifest with a coverage report and implementation estimate.

The acceptance demonstration is a measured shell plus an assortment brief producing a complete valid showroom with no manual positioning or product assignment. Approximate geometry, unresolved mounting limits or missing room rules must appear as blockers to validated release, even when a conceptual simulation can still be displayed.
