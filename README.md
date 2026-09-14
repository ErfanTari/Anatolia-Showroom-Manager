# Anatolia Showroom Manager

**Live site:** https://erfantari.github.io/Anatolia-Showroom-Manager/

**APS Showroom Studio:** [Online 3D review](https://erfantari.github.io/Anatolia-Showroom-Manager/studio/web/) · [Open the local Studio](http://127.0.0.1:8765/studio/web/) · [Project guide](studio/README.md) · [12 team decisions](studio/docs/TEAM_DECISIONS.md).

The new `studio/` application connects all 194 APS slots to one SQLite placement record, adds 765 production-face previews, visibility and duplication review, deterministic proposals, CSV exchange and installation tasks. Room tiles use varied production faces at product scale. The online Studio is a public, read-only review snapshot. Run `Start_APS_Simulation.command` and open `http://127.0.0.1:8765/studio/web/` to save changes through the local application. Authentication is planned for a later increment. The older five-showroom catalogue is documented below.

**Five showrooms · Türkiye**

An interactive single-file web dashboard that catalogues every surface, display format and
zone of Anatolia's showrooms. It combines a filterable product gallery, a clickable schematic
floor plan and a full detail modal — all driven from the BOM data files.

Pick a showroom from the top of the sidebar; every section rebinds to it.

| # | Showroom | Place | Stage | Surfaces |
|---|---|---|---|---|
| 1 | APS Temporary Showroom | Aliağa · İzmir | Installed | 174 |
| 2 | Öz Yapı Showroom | Manisa | Built | 103 |
| 3 | Ekinox Showroom | Bursa | Built | 70 |
| 4 | Ark Yapı · Banyo Marka | Ankara | BOM only | 60 |
| 5 | Turkuaz Seba Central | İstanbul | Concept | 91 |

Only APS has booth photography and the 3D sliding-panel rack, so the **Gallery photo strip**
and **Sliding Panels** section appear for it alone; the other four hide them until assets exist.

---

## Quick Start

Open `Showroom Manager.dc.html` in any modern browser. No build step, no server required — all
logic is self-contained in the file. Everything below must sit alongside it.

```
Showroom_Main_repo/
├── Showroom Manager.dc.html   ← open this
├── support.js                 ← DC framework runtime
├── showrooms.js               ← showroom registry (meta + floor-plan zones)
├── showroom-data.js           ← APS BOM data
├── data/
│   ├── showroom-manisa.js     ← generated from the BOMs
│   ├── showroom-ekinox.js
│   ├── showroom-ankara.js
│   └── showroom-turkuaz.js
├── tools/
│   ├── build_showroom_data.py ← BOM .xlsx  →  data/showroom-*.js
│   ├── build_showroom_docs.py ← BOM .xlsx  →  "Showroom Data.md" tables
│   └── check_showrooms.js     ← headless smoke test (node tools/check_showrooms.js)
├── two new showrooms/         ← the four source BOMs + drawings
└── From_website/              ← 53 product images
```

---

## Dashboard Sections

### Hero
Full-screen entry screen with a Ken Burns background. Click **Enter the Showroom** to proceed to the app.

### Showroom Switcher
The five showrooms sit at the top of the sidebar, active one accented. Switching resets the
section to Overview and clears filters, selection and highlight — nothing leaks between floors.

### Overview
- Summary stats: total surfaces, display formats used, plan zones (booth stations on APS), collections
- Format taxonomy grid — click any format to jump straight to a filtered gallery
- Booth photography, room by room (APS only; the others show what is still missing and where it goes)

### Gallery
Filterable product grid. Filters: Collection, Format, Colour Family, Finish, Size, Location. Each card shows the product photo (from `From_website/`), name, collection, and spec line. Click any card to open the **Detail Modal** with full product specs, format chip, location, and a *Locate on Floor Plan* button.

### Floor Plan
Schematic top-down view. **APS** keeps its hand-measured drawing:
- **Sliding Banks A & B** — click to list all slabs in that bank
- **Waterfall** — click to list all 21 cascade displays
- **Fixed Panel Library** — click any vertical line to read that panel's A/B faces
- **Sample Tower** — click to list finishes board
- **Rotating Units** — click to list the two swivel tile displays
- **Main Floors** — click to list all porcelain floor products
- **Stations 01–08** — click to list all surfaces staged in that station vignette

The **other four** render generically from `showrooms.js`:
- **System zones** (sliding banks, libraries, waterfalls, rotating runs) — click for a flat,
  numbered product run
- **Station zones** (rooms, cube sets, sub-size boards) — click for expandable buckets, grouped
  by format, or by location when one format runs long (the ten Turkuaz sub-size boards)
- **Floor zones** — click to list the floor fields
- **Muted zones** — stairs, partner wings, concept areas with no Anatolia BOM rows; drawn dashed
  and not clickable
- **Ankara** additionally shows GF / mezzanine band labels, since its plan comes from location
  codes rather than a drawing

**Format Legend** — click any format chip to highlight only that format across the plan;
**Clear** resets it. Works on all five.

### Sliding Panels (APS only)
Interactive 3D-style rack of both sliding banks — hover a panel to reveal its full slab face,
click to lock it. Hidden for showrooms without `SLIDING_DATA`.

### Beyond
Roadmap panel. **Multi-Showroom Switching is now live**; live inventory sync, sample request
tracking and A/B merchandising tests remain locked.

---

## Booth Layout — APS (Aliağa)

The showroom reads as **two mirrored C / reverse-C wings** around a **central display island**.
Layouts for the other four are described in `Showroom Data.md`.

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

Gallery card backgrounds and floor-plan texture previews all load from `From_website/`. The folder contains **53 JPEGs** sourced directly from the Anatolia website, ensuring colour-accurate, high-resolution representations.

Products without a matching image (Publica variants, Lithoform Twilight, Lustra Onyx, Ceppo di Gre, Terrazzo Delicato, Serena Dusk/Pewter/Valley) fall back to a flat colour swatch derived from their colour family.

---

## Data Files

### `showroom-data.js` (APS)
Auto-generated from **APS BOM 2026-06-09**. Exports `window.ANATOLIA_DATA` with five arrays:

| Key | Contents |
|---|---|
| `sliding160` | 24 entries for Sliding Bank A (160×320) |
| `sliding120` | 24 entries for Sliding Bank B (120×280) |
| `waterfall` | 21 entries for the Waterfall display |
| `fixed` | 46 entries for the Fixed Panel Library (A + B faces) |
| `rotating` | 20 entries for the two Rotating Tile Units |

Each entry is `[name, finish, thickness, productNo, colourCategory, locationLabel]`.

Station vignette products, floor tiles, the tower finishes board, and waterfall-on-wall installations are hard-coded in the `EXTRAS` array inside the HTML logic and do not need to be regenerated from the BOM.

### `data/showroom-<id>.js` (Manisa · Ekinox · Ankara · Turkuaz)
**Generated — do not hand-edit.** Each sets `window.SHOWROOM_DATA['<id>'] = { groups: [...] }`,
where a group is `{ key, label, fmt, room, size, numbered, rows }` and each row is the 8-tuple

```
[name, finish, thickness, productNo, colourCategory, location, size, fmt]
```

`size` and `fmt` are `null` when the group default applies — mixed groups (a bathroom's walls
plus its vanity, a sub-size board's four tile formats) carry them per row.

Regenerate with:

```sh
python3 tools/build_showroom_data.py           # writes data/showroom-*.js
python3 tools/build_showroom_data.py --check   # verify row counts, write nothing
python3 tools/build_showroom_docs.py           # refresh the tables in "Showroom Data.md"
```

The build script asserts an expected row count per group, so a silent change in a workbook
fails loudly instead of quietly shifting the dashboard.

### `tools/check_showrooms.js`
Headless smoke test — `node tools/check_showrooms.js`, no dependencies. Runs the component
logic for all five showrooms and checks that every template binding resolves, every data group
is claimed by exactly one plan zone, no two labelled zones overlap, every zone click fills the
context panel, *Locate on Floor Plan* finds a target for every product, and switching showrooms
doesn't leak the memoised products array. Run it after touching `showrooms.js` or the data.

### `showrooms.js`
The showroom registry: `window.SHOWROOMS`, one entry per floor.

- `meta` — every identity string the UI shows (name, partner, city, area, stage, tagline,
  floor-plan blurb and caption, sidebar lines, hero image, source documents).
- `plan` — the schematic floor plan: `aspect`, optional `bands`, and `zones` in percentage
  coordinates. A zone is `{ id, type, keys, label, sub, fmt, art, x, y, w, h }`, where `type`
  is `system` (flat numbered run), `station` (grouped by format), `floor`, or `muted`
  (drawn but not clickable), and `keys` names the data groups the zone contains.
- APS carries `bespokePlan: true` — its floor plan is the hand-measured drawing built into
  the HTML and is rendered by its own branch, untouched.

> The four new plans are **schematic**: zone shapes are proportional reads of the PDFs, not
> survey geometry. Rebuild any of them with the `showroom-floor-plan` skill against the LAY
> sheet when true dimensions are needed.

### `Showroom Data.md`
Human-readable reference for all five showrooms. The APS section is hand-written; the four
new sections sit between `<!-- BEGIN/END GENERATED SHOWROOM TABLES -->` and are produced by
`tools/build_showroom_docs.py`, so they cannot drift from the JS the dashboard loads.

### BOM spreadsheets
`APS_TemproraryShowroom_BOM_20260609.xlsx` (APS) and the four workbooks in
`two new showrooms/`. These are the single source of truth — everything else is derived.

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

**When a BOM changes (Manisa · Ekinox · Ankara · Turkuaz):**
1. Drop the new workbook into `two new showrooms/` and point `BOOKS` in
   `tools/build_showroom_data.py` at it.
2. Run `python3 tools/build_showroom_data.py --check`. If a group's row count moved, update
   `EXPECTED` in the script *after* confirming the change is real.
3. Run `python3 tools/build_showroom_data.py` then `python3 tools/build_showroom_docs.py`.
4. Add any new product images to `From_website/` plus a matching `IMGMAP` entry.

**When the APS BOM changes:**
1. Update `Showroom Data.md` (section 1) with the new product placement.
2. Regenerate `showroom-data.js` from the BOM (or hand-edit the five arrays to match).
3. Station vignette products, floors, the tower and waterfall-on-wall installations live in
   the `APS_EXTRAS` getter inside the HTML.

**When adding a sixth showroom:**
1. Add a builder to `tools/build_showroom_data.py` returning a list of groups, register it in
   `BOOKS` / `BUILDERS` / `EXPECTED`, and run the script.
2. Add a `<script src="./data/showroom-<id>.js">` line to the `<helmet>` block in the HTML.
3. Append an entry to `window.SHOWROOMS` in `showrooms.js` with `meta` and `plan.zones`.
   Every data group must be claimed by exactly one non-muted zone.
4. Add a blurb to `BLURBS` in `tools/build_showroom_docs.py` and regenerate the docs.

No change to the HTML logic is needed — the switcher, stats, gallery, floor plan, context
panel and *Locate on Floor Plan* are all driven from the registry.

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
- **State**: Held in `this.state` — `view` (hero/app), `showroomId` (which showroom is active), `section` (overview/gallery/floorplan/sliding/beyond), `filters`, `selected` (open detail ID), `hiFormat` (highlighted format on plan), `sel` (active floor-plan selection).
- **Showroom accessors**: `showroom` / `meta` / `isAps` / `dataGroups` / `planZones` / `zoneProducts()` resolve everything showroom-specific from `state.showroomId`. APS-only data lives behind `APS_*` getters (`APS_EXTRAS`, `APS_SYS`, `APS_STN`, `APS_ROOM_PHOTOS`, `APS_PHOTO_TAGS`, `APS_FURNITURE_PINS`, `APS_SLIDING_DATA`).
- **Products array**: Built once per showroom and memoised in `this._p`, keyed on `showroomId|dataReady`. APS combines `window.ANATOLIA_DATA` with `APS_EXTRAS`; the others walk `window.SHOWROOM_DATA[id].groups`. Every product carries `group` (its data group) so `Locate on Floor Plan` can find its zone.
- **Data loading**: the data files are appended to `<head>` by the helmet and therefore load asynchronously and out of order. `componentDidMount` polls until the registry and every showroom it names have arrived before setting `dataReady`.
- **Image path**: `From_website/<filename>.jpg` — relative to the HTML file location.
- **No build/bundler**: Safe to edit the HTML directly and reload in the browser.
