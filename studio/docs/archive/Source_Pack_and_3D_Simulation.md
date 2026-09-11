# APS source pack and first interactive 3D simulation

Prepared 9 September 2026. This implements the spatial prototype in the foundation plan using the supplied sources. APS remains the pilot; Prime/Commercial is positioning and Hit is a separate flag. Merch owns policy above showroom management. The long-term system should design end-to-end; this first model establishes the evidence and surface identities that the deterministic engine will need.

## What is working

The local simulation is at `http://127.0.0.1:8765/simulation/`. Start it with `python3 -m http.server 8765 --bind 127.0.0.1` from the repository root if needed.

The scene includes eight spaces, 48 sliding panels, 24 fixed panels with 48 faces, 21 waterfall panels, and two rotating units with five double-sided carriers each. It also includes live wall/floor applications, an Oro Noir meeting table, six chairs, sample trays, TV and pendant, a bathroom vanity/tub, fireplace seating, a photo-based Verdi Alpi kitchen island/counter, and a sample tower capacity model.

The viewer supports orbit, plan and eye-level cameras; room navigation; surface inspection; search by product/SKU/finish; sliding and rotating movements; front/back inspection; room-photo comparison; source-page review; and exportable local material studies. A study carries stable slot IDs and the source BOM hash. It does not update installation status or claim compatibility approval.

The separate source and scene manifests are the useful foundation here. A product has a source record, a fixture has an identity, and each usable face has a slot. A renderer, a future solver and an MCP interface can all refer to those same IDs. No designer needs to recreate those links for every review.

## Source findings and reconciliation

| Supplied source | What it establishes | Limits retained |
|---|---|---|
| APS_TemporaryShowroomProject_20251121.pdf, 19 pages | Overall 29.00 × 13.438 m plan; two 12.50 m wings and 4.00 m central corridor; room/wall labels, floor assignments and fixed face sequence | Internal positions traced approximately. Overall footprint is not a surveyed usable-area calculation. No CAD coordinates or confirmed heights supplied. |
| APS_TemproraryShowroom_BOM_20260609.xlsx | 188 named product/application/sample rows plus hardware entries; product numbers, finish, size, quantities and source notes | User identifies these sources as current setup. No independent September site verification was performed. Procurement extras are not automatically additional installed slots. |
| APS_TemporaryShowroom_BOM_20260609.csv | All 188 workbook product rows match on location, name, product number and size; nine additional rows are hardware | The CSV and XLSX are kept, not merged into two competing authorities. |
| Porcelain_Collection_Merch_Brochure.pdf | Fixture forms, dimensions, codes and intended panel formats on the requested pages | A brochure is reference evidence, not a complete manufacturing or kinematic model. |
| Assortment confirmation list with names 260618_1.xlsx | Portfolio naming/finish/size options across nine tabs; 112 embedded image files | Not a released SKU master. User text mentions 251105; the supplied June file is the one exported. |
| APS room photographs, including Oro Noir table and kitchen | Installed appearance, furniture form and contextual placement | Perspective photos do not establish fabrication dimensions, true color, exact face or material SKU. |
| AnatoliaEkinoxShowroom_Bursa_V2_20250826.pdf | Secondary showroom/design reference, reviewed separately | Bursa geometry is not used to fill gaps in APS. |

The fixed-panel source reconciliation is material: the two central upper front positions use Calacatta Noir, and the two central lower back positions use Macchia Vecchia. Each has BOM quantity two. The old viewer's duplicate face mapping used different products. The new 48-face assignment accounts for every fixed BOM quantity. Final installed front/back orientation still needs a numbered walk-through.

Sliding positions come from the BOM's numbered Slab/Mini locations, not an image-array index. Six mini positions differed in the older viewer; the simulation uses the workbook's positions.

Rotating placement follows the Turkish BOM notes at rows 71 and 81: the first five products are fronts, the next five are backs; the first unit is on the kitchen/Lithoform side and the second on the bathroom/Serena side.

W9F contains three Onyx entries without SKUs and with approval/production-pending notes. They remain searchable source records and are excluded from the installed surfaces pending clarification. The tower's 75-chip capacity is represented with blank capacity markers; a physical chip inventory was not supplied.

## Fixture reference extracted for future modelling

Dimensions below are converted to metres for the scene. Retain the original units in source evidence; use integer millimetres in the future technical catalogue.

| Display | Source | Confirmed reference facts | Still needed |
|---|---|---|---|
| Waterfall | Brochure pp. 31–33 | Three 600 × 2800 mm panels per module. Module 1655 W × 2936 H × 205 D mm; kit 9901-0085-0. Six-panel arrangement 1699 W × 620 D mm; twelve-panel 3305 W × 620 D mm. APS has seven kits. | Actual join angle, fixing points, back clearances and exact placement of connectors. |
| Fixed | pp. 37–40 | 1600 × 3200 mm slab format; single/double sides; frame 1450 W × 3200 H mm, code 9902-3333. Bookmatch pairs use adjacent positions. | Approved thickness/load envelope, frame feet and anchoring. Brochure references 6 mm; several APS slabs are thicker, so compatibility needs technical confirmation. |
| Sliding full slab | pp. 45, 47 | 1600 × 3200 mm format, mirrored units; APS has 12 + 12 positions. Frame schematic labels include 2097 mm span, 1706 mm diagonal, 1234 mm support height and 1225 mm base width. | Exact geometry associated with each labelled dimension, track vector, travel, stops and clearances. 1234 mm is not the slab height. |
| Sliding mini slab | pp. 45, 46, 48 | 1200 × 2800 mm format, mirrored units, 12 + 12 APS positions; 900 mm base-width label. | Same mechanical definitions; do not infer travel from the diagonal drawing dimension. |
| Rotating 120 × 120 | pp. 50–51 | Code 9902-3105-0; five double-sided carriers, ten tiles. Frame 1565 W × 680 D × 1495 H mm. | Pull-out stroke, hinge origin/axis, interlock sequence and allowed rotation directions. Current animation is illustrative. |
| Other rotating formats | pp. 52–54 | 90 × 90: code 3104, 1265 W × 680 D × 1197 H mm. 60 × 120: code 3106, 965 W × 680 D × 1496 H mm. 90 × 180: code 3107, 1265 W × 680 D × 2094 H mm. | Confirm against supplier drawings before modelling new installations. |
| Furniture | APS BOM + photos | Oro Noir meeting tabletop 1250 × 2800 mm. Kitchen identified as Verdi Alpi by the user/photo. | Fabricator drawings, height/edge/underside/leg details; kitchen dimensions and exact SKU/finish. |

Brochure p. 50 says “8–10 cm” tile thickness; the APS rotating BOM says 9 mm. The conflicting brochure text is preserved as an issue, not adopted as a deterministic mounting rule.

## Texture recovery and confidence

The existing `assets/products` directory contained 57 `.jpg` files whose contents were failed-download JSON messages, and some valid JPEGs were product renders with backgrounds. Those cannot function as reliable tile textures. The simulation uses valid embedded assortment swatches where a reviewed product-name match is available, with a fallback to existing sliding-panel images. Original assets have not been overwritten.

The workbook sometimes reuses a composite image across colors. The model records UV crop windows for explicitly labelled Coast/Beige, Vista/Grey and Dunes/Ivory swatches. It also excludes an embedded title banner on the Arabescato Corchia image. Original images remain unchanged. This is a visible approximation of product design, not certification of production face, gloss, true color or bookmatch alignment.

## CSV deliverables

`output/assortment/assortment-csv-pack.zip` includes all nine tab CSVs, a 1,191-row option index, the source/hash manifest, original formula metadata, embedded images and their sheet/cell anchor index.

| Tab | Source grid | Role |
|---|---:|---|
| Names | 79 × 19 | Reference/proposed names and assortment notes |
| 12mm | 73 × 17 | 12 mm finish options |
| 6mm | 72 × 17 | 6 mm finish options |
| Subsize | 68 × 19 | Multiple cut sizes, finishes and 20 mm options |
| Mosaic | 56 × 15 | Mosaic options with a different header structure |
| Sheet4 | 33 × 6 | Naming/finish notes |
| Sheet3 | 9 × 14 | Summary counts |
| Sheet2 | 1 × 1, empty | Retained empty sheet |
| Sheet1 | 1 × 1, empty | Retained empty sheet |

The raw tabs preserve cells, line breaks and totals. The option index splits multiline options, excludes totals and preserves sheet/cell references, both finish-header rows and raw notes. It does not infer release status, stock or final SKUs. All 57 original formulas and their cached values are retained separately; CSV cannot carry live spreadsheet formulas, formatting or embedded imagery by itself.

## Suitable source formats for AI and deterministic design

PDF is useful: keep it as immutable, dated evidence. Pair it with structured records and editable technical assets so the system does not have to rediscover the same facts from a page every time.

1. **Product master — SQLite with CSV import/export.** One SKU per row, linked to stable collection/color/finish IDs. Fields: nominal and actual dimensions in mm, thickness, approved uses, face count, lifecycle/effective dates, positioning, independent Hit flag, supply/availability status and market eligibility. Add source, revision, owner and verification status. Distinguish physical product finish from marketing finish name. This is a proposed pilot architecture; choose the later server deployment against [SQLite's documented use cases](https://www.sqlite.org/whentouse.html).
2. **Fixtures — editable CAD plus a lightweight GLB.** Request DWG/DXF or STEP/native 3D from the fixture supplier, plus a web GLB with metres, Y-up, transforms applied, sensible origin and separate moving parts. The coordinate/unit convention follows the [Khronos glTF specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#coordinate-system-and-units). Supply an accompanying JSON record for approved product sizes/thickness/load, pivot axes, travel limits, keep-out envelope, slot IDs and fixture revision. Do not encode these facts only in mesh names.
3. **Showroom — dimensioned plan plus a scene manifest.** Surveyed coordinates for shell, openings, columns, fixed anchors, power/water and permanent installations. Name each wall/fixture/face with a durable ID, and link the source drawing page/revision. Separate the measured building from movable fixture placement and from material assignments.
4. **Textures — clean, straight-on product faces.** Prefer a TIFF/PNG master and web JPEG/WebP, without logos, labels, perspective, drop shadows or frame edges. Give each face its own file and record the physical coverage, orientation, SKU/design ID, finish and color-profile information. Normal/roughness maps help later, but a clean base-color face is the first priority. A bookmatch needs an explicit A/B relationship.
5. **Photos — named evidence, not the database.** Record showroom, room, wall/fixture/face ID, date, direction and verification owner. Keep originals; generate a web copy. A quick numbered walk-through video can efficiently confirm front/back placement and moving mechanisms.
6. **Rules — structured conditions plus Markdown rationale.** Store hard eligibility constraints and ranked preferences in versioned JSON/SQLite/CSV. Markdown explains Anatolia's objectives, examples and exceptions to an agent. The agent proposes a scenario through the same validated operations as the UI; it does not directly rewrite authoritative tables.

The operating flow should be: import staging → validation → reviewed source snapshot → deterministic scenario → explanation/diff → Merch-controlled release → execution tasks → observed installation evidence. Showroom managers can report reality; that observation should not silently change Merch's brand rules. A future agent can run the complete design process within the approved policy and explain unresolved constraints.

## The next collection round

**Before meeting Merch — we can do now:** use this model to identify locations, annotate source issues, compare room photos, export the portfolio tables and collect a short list of candidate swaps. Preserve Prime/Commercial/Hit as unknown until Merch supplies them; do not guess from the pictures or sales impressions.

**Merch owner:** confirm the released SKU list, Prime/Commercial positioning and Hit flag; define required collection/color/finish coverage; specify color order for Architeq and other families; identify discontinuations and launch dates; define when repeats are acceptable and which finish should be preferred in each display type. Provide a small set of good/bad placement examples and ranked tradeoffs for limited capacity.

**Design/technical owner:** provide the APS CAD plan and fixture files; verify mounting envelopes for the actual 6/9/12 mm products; measure kitchen furniture and the missing tabletop construction details; confirm permanent-object positions, clearance and fixture motion. Deliver clean texture masters for the core APS products first.

**Showroom manager:** perform a numbered face-by-face walkthrough using the manifest IDs; confirm the corrected sliding/fixed positions, W9F status and current sample inventory. Capture dated photos for exceptions and replacements.

**Our implementation side:** convert the reviewed records into the SQLite schema from the foundation plan; add import validation and stable SKU/finish aliases; move application geometry out of the renderer into the scene manifest; add a deterministic assignment evaluator with feasibility failures and explanations; then introduce lifecycle-triggered redesign diffs, observed-status updates and feedback capture. MCP and agents should use those operations after their invariants are tested.

## Six decisions to settle next

1. Is the June 2026 assortment workbook the intended current portfolio authority, or is there a later released SKU export?
2. Have the three W9F Onyx items now been produced/installed, or should they remain pending?
3. Which exact kitchen SKU/finish and fabricated dimensions should replace the photo-based Verdi Alpi placeholder?
4. Can the fixture supplier provide pivot/travel models and explicit thickness/load limits, particularly for fixed panels and the rotating unit?
5. Which one approved ordering should Architeq use: one light-to-dark sequence or separate warm/neutral sequences?
6. For the first deterministic redesign, should the primary objective be full range coverage, Hit visibility, new-launch exposure or minimum replacement effort when those compete? Merch should assign the hierarchy.

No answer to these is required to explore the current simulation. They are the next inputs needed to turn a visual reference into an autonomous, operational design system.
