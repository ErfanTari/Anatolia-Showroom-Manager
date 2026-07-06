# APS Temporary Showroom — Layout Reference

_Source of truth for the floor-plan page. Derived from `APS_TemporaryShowroomProject_20251121 2.pdf`, sheet **LAY** (page 2). Complements `Showroom Data.md` (which lists the products) — this file describes **where everything sits**._

## Envelope

- Overall: **2900 × 1343.8 cm** (≈ 380 m²), landscape, aspect ≈ 0.463.
- Horizontal split: **left wing 1250 | central corridor 400 | right wing 1250** cm.
- Each wing = **outer column (≈445 cm, against the outside wall)** + **inner column (toward the centre)**.
- Vertical bands: **top 367.8 | middle 608.2 | bottom 367.8** cm.
- The **middle band of each inner column** holds the central pre-fix panels. The corridor is the porcelain walkway; the **entrance is at its bottom-centre**.

Five horizontal slots across the booth: `L-outer · L-inner · corridor · R-inner · R-outer`.

## Areas (1–8)

Each area is a room/zone with up to four wall faces. **Face letters A–B–C–D = top · right · bottom · left wall** of that area.

| Area | Identity | Position | Display object inside it |
|---|---|---|---|
| **1** | Bathroom | bottom of left inner column (bottom-centre-left) | room vignette — bathtub, walls |
| **2** | Lounge | left outer column, lower | chaise lounge, armchair, TV |
| **3** | Meeting / Dining Room | left outer column, top (top-left corner) | meeting table + chairs |
| **4** | Sliding Bank A | top of left inner column (top-centre-left) | **sliding panels, 160 × 320 cm** (24 slabs) |
| **5** | Sliding Bank B | top of right inner column (top-centre-right) | **sliding panels, 120 × 280 cm** (mirror of 4) |
| **6** | Waterfall | right outer column, top (top-right corner) | **waterfall** — angled rack, on the wall, in the middle of the area |
| **7** | Kitchen | right outer column, lower (bottom-right corner) | kitchen counter, hood |
| **8** | Rotating | bottom of right inner column (bottom-centre-right) | **rotating tile displays** — two rectangular swivel panels |

The booth is broadly **mirror-symmetric**: left wing (areas 1–4) ↔ right wing (areas 5–8). The only asymmetry of note: area 4 had a **sample tower** (a bookshelf of sample chips) in front of its sliding bank; area 5 has no tower. _The tower is omitted from the current floor-plan rendering._

## Central floor — Pre-fix Panels

- **24 panels installed as diagonal walls**, spread horizontally across the central floor (not concentrated in the corridor).
- **12 per wing** — in the middle band of each inner column.
- Each group of 12 = **6 columns × 2 rows** (6 top + 6 bottom).
- Drawn in plan as alternating diagonal slashes forming an X / diamond chain.
- **22 panels are two-sided** (a different product front vs back). **2 are bookmatch** — the same slab mirrored on both faces — and sit in the centre with ↔ arrows on the LAY sheet: **Calacatta Noir Block 34** and **Macchia Vecchia Block 42**. The plan tints the two bookmatch panels a warm tan to distinguish them.
- **Face maths:** 22 × 2 faces + 2 × 1 face = **46 faces = 24 panels.** This reconciles the earlier confusion — `showroom-data.js` holds 46 face entries, which is 24 panels (not 23) once the two bookmatch slabs are counted as single-entry panels.

## Display systems summary

| System | Area | Format | Size | Count |
|---|---|---|---|---|
| Sliding Bank A | 4 | Sliding Panel | 160 × 320 cm | 24 slabs |
| Sliding Bank B | 5 | Sliding Panel | 120 × 280 cm | 24 mini-slabs |
| Waterfall | 6 | Waterfall | 60 × 280 cm | 21 displays |
| Pre-fix Panels | central | Pre-fixed Panel (double-sided) | 160 × 320 / 162 × 322 cm | 24 panels |
| Rotating units | 8 | Rotating Panel | 120 × 120 cm | 2 units |
| Porcelain floor | corridor + walkways | Floor | 120 × 120 cm | — |

## Other LAY-sheet drawings in this PDF set

- **LAY** (p.2) — this layout.
- **FLR** (p.3) — floor-tile fields with product callouts.
- **RCP** (p.4) — lighting & electrical (track rails, speakers, outlets).
- **CT01** (p.5) — Arabescato Corchia slab-cutting templates for the entrance feature (faces 1B/1C/1D).

> ✅ **Resolved 2026-07-06:** `EXTRAS` in `Showroom Manager.dc.html` reconciled against `APS_TemporaryShowroom_BOM_20260609` — station numbers were fixed (bathroom/vanity moved off station 3 onto 1; meeting-room walls/table moved off station 4 onto 3), missing rows added (4C Foresta, 8A Gemma Bronze, full 8B–8D wall mix, fireplace hearth, vanity top, Statuario B-grade), and floor rows were retagged per-room with corrected product numbers. Clicking a room (station) on the floor plan now merges its wall/floor/furniture (`EXTRAS`, matched by `station`) with its display system (sliding bank / waterfall / rotating, matched by `room`), so one click shows panels + wall/room + furniture together. See `Showroom Data.md`'s station table and the BOM CSV for the source data.
