# Anatolia Showroom Manager

**APS Factory Temporary Showroom — Aliağa, İzmir, Türkiye**
**Anatolia × AETERNA · 380 m²**

An interactive single-file web dashboard that catalogues every surface, display format, and booth station of the APS temporary showroom. It combines a filterable product gallery, a clickable schematic floor plan, and a full detail modal — all driven from the BOM data file.

---

## Quick Start

Open `Showroom Manager.dc.html` in any modern browser. No build step, no server required — all logic is self-contained in the file. `showroom-data.js` and `support.js` must be in the same directory.

```
Showroom_Main_repo/
├── Showroom Manager.dc.html   ← open this
├── showroom-data.js           ← BOM data (auto-generated)
├── support.js                 ← DC framework runtime
└── From_website/              ← 52 product images
```

---

## Dashboard Sections

### Hero
Full-screen entry screen with a Ken Burns background. Click **Enter the Showroom** to proceed to the app.

### Overview
- Summary stats: total surfaces, display formats, booth stations, collections
- Format taxonomy grid — click any format to jump straight to a filtered gallery
- Collection bar chart and display-system / station index (click a row to highlight it on the floor plan)

### Gallery
Filterable product grid. Filters: Collection, Format, Colour Family, Finish, Size, Location. Each card shows the product photo (from `From_website/`), name, collection, and spec line. Click any card to open the **Detail Modal** with full product specs, format chip, location, and a *Locate on Floor Plan* button.

### Floor Plan
Schematic top-down view of the 380 m² booth. Interactive elements:
- **Sliding Banks A & B** — click to list all slabs in that bank
- **Waterfall** — click to list all 21 cascade displays
- **Fixed Panel Library** — click any vertical line to read that panel's A/B faces
- **Sample Tower** — click to list finishes board
- **Rotating Units** — click to list the two swivel tile displays
- **Main Floors** — click to list all porcelain floor products
- **Stations 01–08** — click to list all surfaces staged in that station vignette
- **Format Legend** — click any format chip to highlight only that format across the entire plan

### Beyond
Roadmap panel listing locked future capabilities: live inventory sync, sample request tracking, multi-showroom switching, A/B merchandising tests.

---

## Booth Layout

The showroom reads as **two mirrored C / reverse-C wings** around a **central display island**.

```
┌──────────────────── 29 m ────────────────────┐
│  [3] [2] [1]  │  CENTRAL ISLAND  │  [5] [6] [7]  │
│               │  Bank A + Tower  │               │
│       [4]     │  Panel Library   │  [8]          │
│               │  Bank B + W'fall │               │
└───────────────┴──────────────────┴───────────────┘
                     ↑ Entrance
```

### Central Island

| System | Room | Format | Count | Size |
|---|---|---|---|---|
| Sliding Bank A | Room 4 | Sliding Panel | 24 slabs | 160 × 320 cm |
| Sliding Bank B | Room 5 | Sliding Panel | 24 mini-slabs | 120 × 280 cm |
| Waterfall | Room 6 | Waterfall | 21 displays | 60 × 280 cm |
| Fixed Panel Library | Hall | Pre-fixed Panel (double-sided) | 24 panels / 46 faces | 160 × 320 cm |
| Sample Tower | Hall | Tower | 1 finishes board | — |
| Rotating Units | Room 8 | Rotating Panel | 2 units · 20 tiles | 120 × 120 cm |

### Perimeter Stations

| Station | Theme | Key Surface |
|---|---|---|
| 01 | Entrance Feature Wall | Arabescato Corchia bookmatch |
| 02 | Living Room · Fireplace | Travertino Titanium (fireplace insert) + Lithoform Veincut Vista walls |
| 03 | Bathroom | Pietra Imperiale + Bianco Gioia |
| 04 | Meeting Room | Oro Noir table top + Lithoform Crosscut Vista walls |
| 05 | Size-Study Wall | Taj Mahal in 7 formats (120×120 to 5 cm hex mosaic) |
| 06 | Corchia Waterfall Wall | Majesto Calacatta Corchia 120×280 waterfall-on-wall |
| 07 | Travertino Wall | Majesto Travertino Classico 120×280 waterfall-on-wall |
| 08 | Porcelain Wall + Rotating | Serena family + Lithoform porcelain walls |

### Porcelain Floors

| Field | Product |
|---|---|
| F1–F4 | Serena Crater Honed 120×120 |
| F5 | Lithoform Crosscut Dunes Honed 120×120 |
| F6 | Majesto Arabescato Corchia Honed 120×120 |
| F7 | Majesto Ceppo di Gre Honed 120×120 |
| F8 | Majesto Calacatta Noir Honed 120×120 |

---

## Product Images

Gallery card backgrounds and floor-plan texture previews all load from `From_website/`. The folder contains **52 JPEGs** sourced directly from the Anatolia website, ensuring colour-accurate, high-resolution representations.

Products without a matching image (Publica variants, Lithoform Twilight, Lustra Onyx, Ceppo di Gre, Terrazzo Delicato, Serena Dusk/Pewter/Valley) fall back to a flat colour swatch derived from their colour family.

---

## Data Files

### `showroom-data.js`
Auto-generated from **APS BOM 2026-06-09**. Exports `window.ANATOLIA_DATA` with four arrays:

| Key | Contents |
|---|---|
| `sliding160` | 24 entries for Sliding Bank A (160×320) |
| `sliding120` | 24 entries for Sliding Bank B (120×280) |
| `waterfall` | 21 entries for the Waterfall display |
| `fixed` | 46 entries for the Fixed Panel Library (A + B faces) |
| `rotating` | 20 entries for the two Rotating Tile Units |

Each entry is `[name, finish, thickness, productNo, colourCategory, locationLabel]`.

Station vignette products, floor tiles, the tower finishes board, and waterfall-on-wall installations are hard-coded in the `EXTRAS` array inside the HTML logic and do not need to be regenerated from the BOM.

### `Showroom Data.md`
Human-readable single source of truth. Contains the full product list for every display system and station, the panel-pair table for the Fixed Panel Library, and notes on the booth structure. **Edit this file first** when the BOM changes, then regenerate `showroom-data.js`.

### `APS_TemproraryShowroom_BOM_20260609.xlsx`
Master BOM spreadsheet (latest revision: 2026-06-09). Source for `showroom-data.js`.

---

## Reference Documents

### `APS_TemporaryShowroomProject_20251121 2.pdf`
Full architectural drawing set for the APS temporary showroom. Sheets included:

| Sheet | Title | Contents |
|---|---|---|
| LAY | Layout | Full floor plan — all 8 stations, central island, furniture, dimensions (29 × 13.4 m) |
| FLR | Floor Tiles Layout | 120×120 porcelain tile fields with product callouts |
| RCP | Lighting & Electrical | Reflected ceiling plan — track lighting rails, speaker positions, electrical outlets |
| CT01 | Slab Cutting Templates | Arabescato Corchia Block 59 bookmatch cut guides for Stations 1B / 1C / 1D |

### `AnatoliaEkinoxShowroom_Bursa_V2_20250826.pdf`
Technical drawings for the **Anatolia Ekinox Showroom, Bursa** (a related permanent showroom). Sheets included:

| Sheet | Title | Contents |
|---|---|---|
| — | TV Unit | Front elevation, side section, top view of 322 cm tall TV wall unit |
| — | TV Unit Slab Cuts | Gemma Bronze 160×320 bookmatch — arka duvar, üst tabla, ön alın, yan kapama pieces |
| — | Wall Installations – Bathroom | Bianco Gioia Block 19 bookmatch — shower front/rear walls, bathtub surround, 45° miter corners |
| — | Wall Installations – Column 01 (A/B) | Majesto Verdi Alpi 120×280 — A and B faces of decorative column, upper/lower cuts |
| — | Wall Installations – Column 01 (C/D) | Majesto Verdi Alpi 120×280 — C and D faces, ceiling-height scribing note |

### `Anatolia showroom manager.zip`
Source upload bundle used to seed the dashboard. Contains the two PDFs above, the BOM Excel, a plain-text BOM dump (`_bom_dump.txt`), early product texture JPEGs (now superseded by `From_website/`), and a reference screenshot.

---

## Updating the Dashboard

**When the BOM changes:**
1. Update `Showroom Data.md` with the new product placement.
2. Regenerate `showroom-data.js` from the BOM (or hand-edit the four arrays to match).
3. Add any new product images to `From_website/` and add a matching entry to `IMGMAP` inside the `<script>` block in `Showroom Manager.dc.html`.

**When adding a product image:**
- Place the file in `From_website/` (JPEG, any resolution — the browser scales it).
- In the `IMGMAP` getter (around line 441 of the HTML), add `['product name keyword', 'Exact_Filename_Without_Extension']` before the catch-all entries.
- Keys are matched case-insensitively against the product name; the `Majesto` prefix is stripped automatically before matching.

**When changing display format colours or icons:**
- `ACC` getter: hex accent per format name.
- `icon()` method: SVG path per format name.
- `DESC` getter: one-line description per format name.

---

## Collections Reference

| Collection | Typical Format | Character |
|---|---|---|
| Majesto | Slabs, panels, tiles | Premium natural stone look; calacatta, travertine, onyx, green marble |
| Lithoform | Slabs, panels, tiles | Concrete / stone hybrid; crosscut and veincut patterns |
| Lustra Onyx | Mini-slabs, tiles | Translucent onyx in Crema, Hazel, Feather, Sage, Halo variants |
| Serena | Mini-slabs, tiles, walls | Soft grey porcelain; Crater, Flint, Shale, Dusk, Pewter, Valley |
| Monoforma | Slabs | Minimalist large-format; Storm, Silhouette, Moonlight, Oasis |
| Publica | Slabs | Organic terrazzo / patinated surface; Thunder, Terrain, Horizon |
| Travertino | Slabs | Classic travertine; Classico (grained) and Titanium (grained dark) |
| Sintered Slab | Various | All other large-format sintered surfaces not in a named collection |

---

## Technical Notes

- **Framework**: The `.dc.html` format uses a proprietary `DCLogic` base class (provided by `support.js`). `renderVals()` returns a flat object of template bindings; `{{ expr }}` interpolations in the HTML are resolved by the runtime. No external dependencies are bundled.
- **State**: Held in `this.state` — `view` (hero/app), `section` (overview/gallery/floorplan/beyond), `filters`, `selected` (open detail ID), `hiFormat` (highlighted format on plan), `sel` (active floor-plan selection).
- **Products array**: Built once and memoised in `this._p`. Combines BOM arrays from `showroom-data.js` with the hard-coded `EXTRAS` array. Total ~170 surfaces.
- **Image path**: `From_website/<filename>.jpg` — relative to the HTML file location.
- **No build/bundler**: Safe to edit the HTML directly and reload in the browser.
