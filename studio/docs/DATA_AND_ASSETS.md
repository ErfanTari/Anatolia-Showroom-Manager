# Data and asset contract

## One authoritative operating record

SQLite owns the current showroom. The browser requests `/api/state` locally. GitHub Pages loads an exported snapshot with the same structure. Every selectable mesh resolves its `slot_id` through `placements`; the renderer does not choose installed products from a separate BOM list. The original rows remain evidence and help reconstruct fixed architectural geometry.

Use millimetres for stored dimensions/coordinates, degrees for yaw, stable text IDs for identities, and UTC timestamps for audit events. The renderer converts millimetres to metres. Source sizes in cm retain their raw source text alongside the normalized variant.

| Table / CSV | One row represents | Human-editable input |
|---|---|---|
| products | Design/color identity | Prime/Commercial/unknown positioning, independent Hit flag, lifecycle, required flag, color group/rank and decision source |
| variants | SKU or unreleased portfolio option | SKU, finish, width/height/thickness, lifecycle and availability |
| faces (SQLite / JSON) | One production preview with provenance | Source format, path, hash, image dimensions and exact-installed-face verification state |
| fixtures | A frame or display carrier | Geometry verification flag; position changes enter as layout proposals |
| slots | One assignable face/application | Visibility tier, score, basis and intentional repeat; format and protected status are retained |
| placements | Current occupant of a slot | CSV changes create a **draft**, including face changes; physical observations use the app |
| rules | One configurable guideline | Enabled flag, JSON parameters, draft/confirmed status and rationale |
| questions | One team decision | Answer, status, named owner and evidence |
| scenarios (SQLite / JSON) | A complete proposed set of changes | Revision, mode, reasons, before/after metrics and release dependencies |
| tasks | One work item | Owner, due date, progress, evidence and removed-material disposition through the app |
| events (SQLite / JSON) | One recorded action | Append through the domain layer; no UI editing |

The initial catalogue contains 108 source-derived design names; 68 occur in the reported setup. It includes unconfirmed portfolio/development identities and potential spelling aliases. These counts are not a certified list of saleable products. Automatic new-design candidates require an existing SKU or a matched production identity; source-only names remain for reconciliation.

## CSV exchange

1. Export the current tables from the app or `python3 studio/backend/cli.py export`.
2. Keep IDs and `base_revision`. Edit the appropriate fields. Import IDs/SKUs as **text** in Excel, use UTF-8 CSV, and keep dimensions numeric in mm.
3. Use **Validate only** first. Validation rejects unknown/duplicate IDs, invalid enums, non-finite dimensions, stale revisions and incompatible placement proposals. The whole import rolls back on failure.
4. Apply. Product/rule updates change the source revision. Placement updates create a draft scenario. Export again before another editing round.

The initial eight files are also authored and value-checked with the spreadsheet artifact tool. CSV carries values, not cell styling or formulas. The original portfolio's nine-tab CSV export and cached-formula metadata remain in `output/assortment/`.

Do not edit `state.json` to update the showroom. It is overwritten by export. Do not maintain an independently editable Excel master beside SQLite. An Excel workbook can be added later as a governed input interface to these same tables.

New catalogue identities currently enter through a reviewed migration/import extension; existing-row CSV imports deliberately reject unknown IDs to catch typos. Large new showroom shells, fixture families and cut fabrication packages need the next schema/geometry increment described in the roadmap.

## Materials for AI and simulation

| Material | Preferred deliverable | Required companion information |
|---|---|---|
| Production face | sRGB JPEG/WebP, 1,024–2,048 px long edge; retain aspect ratio and unaltered design | Product/variant ID, source face ID, width/height/thickness, finish, orientation, bookmatch relation, original-file reference, hash |
| Fixture | GLB for the viewer; STEP or supplier CAD for dimensions | Stable type/version, origin, units, axes, usable slots, thickness/load limits, anchors, collision and travel envelopes |
| Plan | Dimensioned DXF/IFC or a clean CAD export; SVG for review | Origin, scale, floor elevation, walls/doors, services, route/keep-out polygons and revision |
| Fabricated furniture | GLB plus fabrication drawing/cut list | Source slab variant/face, cut UV region, joins, edge build-up, finish, dimensions and fabrication approval |
| Installed evidence | Numbered JPEG/WebP photos | Showroom/room/slot ID, capture date, direction, observed SKU/finish and observer |
| Brand rule | Structured CSV/SQLite fields plus a short Markdown explanation | Owner, effective date, applicability, priority, hard/soft nature, exception examples and approval evidence |

PDF is useful evidence. Preserve it with filename, revision and page references, then extract dimensions and constraints into structured fields. A drawing image alone does not establish a machine-checkable clearance or material limit. The brochure's waterfall pp. 31–33, fixed pp. 37–40, sliding pp. 45–48 and rotating pp. 50–54 remain accessible in the source library.

## Face import performed for this pilot

The preferred drive already contains WebP derivatives in `Marketing_Faces/___Low_resolution__Site/Textures`. The importer reads up to three faces per source format, preserves aspect ratio, records the source-relative path and SHA-256, and copies only the browser assets. It collected 660 marketing derivatives plus three bounded original-file derivatives (663 total). Marketing derivatives are generally 720 px on the long edge; the three original derivatives are at most 1,024 px.

Original fallbacks covered Arabescato Vagli, Calacatta Carrara and Calacatta Viola. Twelve fallback attempts were left unresolved: several originals are multi-gigabyte PSB files or lack an unambiguous standalone face; a Picasso candidate failed the single-slab aspect-ratio check. Full print originals were not imported. `sources/face-register.json` retains the gaps and source-relative evidence.

155 assigned presentations have a production preview; 38 retain source previews. Preview F001/F002 numbering is a derivative sequence, not a certified factory face ID. The chosen image is not proof of the exact installed face, finish or cut. Floors repeat at source tile scale; furniture UVs and cut locations remain illustrative. Do not generate artificial veins as a substitute for production faces.

## Operating safeguards and limits

The service is a trusted, local, single-operator pilot. Its role is selected at process startup (`--role merch`, `designer`, `manager`, or `agent`), not accepted from a browser payload. It is not enterprise authentication. Agent access uses the same Python domain functions and cannot release work or record physical completion.

SQLite transactions and base revisions prevent partial/stale source edits. Work stages do not increment the placement revision until physical verification changes the actual record. Direct observations increment it immediately and retain an audit event. Existing drafts become stale and must be regenerated after source changes.

Before operational multi-user hosting: add SSO and server-enforced identities, permissions by showroom, attachment storage, backup/restore automation, a durable event queue, migration tooling and concurrency tests. Keep customer/personnel feedback and future sales data out of the public review snapshot unless explicitly intended for publication.
