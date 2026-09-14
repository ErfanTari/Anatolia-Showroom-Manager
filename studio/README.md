# Anatolia Showroom Studio

APS pilot: one placement database, a production-face 3D model, deterministic refresh proposals, and a work board that records installation evidence.

[Online 3D review](https://erfantari.github.io/Anatolia-Showroom-Manager/studio/web/) · [Open the local application](http://127.0.0.1:8765/studio/web/) · [Process sketch](https://erfantari.github.io/Anatolia-Showroom-Manager/showroom-process/) · [Team decisions](docs/TEAM_DECISIONS.md)

## Start the working application

Double-click `Start_APS_Simulation.command` in the repository root, or run from that directory:

```sh
python3 studio/backend/server.py --port 8765
```

Open **http://127.0.0.1:8765/studio/web/**. Python 3.10+ and a browser with WebGL are sufficient. Three.js is bundled locally. The server binds to this computer only.

The header says **SQLite connected** when forms save to the database. The GitHub Pages version displays a **read-only review snapshot**: 3D navigation, map highlights and saved proposal comparisons work there; SQLite writes require the local application. Publishing does not create a hosted database service. The approved public release includes this pilot's placement database, exported snapshot and 765 small production-face assets; shared-drive print originals remain on the drive. Access is currently public. Authentication and protected hosting are planned for a later increment.

## What to try

1. In **Simulation**, select APS and use its room sub-tabs. Select a surface to inspect its product and production-face evidence. Room floors and tiled walls distribute different production faces at product scale; the Living space floor uses all 20 supplied Calacatta Noir 120 × 120 faces. Pull out sliding panels and tilt rotating panels.
2. Choose **Visibility tiers** to review proposed prime, secondary and commercial locations. Compare the classification with the actual entrance route.
3. In **Placement review**, inspect repeated designs, exposure concerns, justified bookmatch pairs, missing designs and rotating-panel color order. Highlight any finding on the map.
4. In **Work plan**, compare the Tuscano Burgundy proposal or generate a broader-coverage refresh. Live installations and furniture stay protected. Proposals do not change the reported installation.
5. In **Data & guidelines**, answer the 12 team decisions, confirm product/variant data or edit a rule. Import a CSV with validation and a matching source revision.
6. Merch releases a complete proposal into tasks. Ordering, preparation and installation require evidence. **Verified** records the new actual placement. A manager can also record an observed change directly from a selected surface.

## Source and ownership

- `data/showroom.sqlite` is authoritative. It contains 194 slots, 193 assigned presentations, 103 display carriers/frames, product variants, rules, work packages and audit events.
- `data/exports/` contains eight CSV exchange tables. `base_revision` protects against importing an old file over newer work. Placement imports create proposals.
- `web/data/state.json` is a derived publication snapshot. The renderer resolves every selectable slot through the database's placement records. Frame positions also come from the database.
- `sources/` retains the initial APS migration evidence and face manifest. It is not a second editable placement source.
- `web/assets/faces/` holds 765 browser-sized production previews for 57 design identities. 155 of the 193 assigned presentations currently match one. Room surfaces use complete available face sets, with larger-format cuts labeled in the inspector. Others retain source previews; exact installed face identity and arrangement remain unverified.

Tuscano Burgundy is the current name; Tuscano Rosso is an alias. Prime/Commercial positioning is separate from the Hit flag. Merch has authority above showroom management. The system and agents may independently create proposals; Merch controls work release.

## Maintain the project

```text
studio/
  backend/       SQLite schema, shared rules, HTTP server, CLI, MCP adapter
  data/          authoritative database and derived CSV exchange files
  docs/          concise current documentation; earlier planning in archive/
  sources/       initial migration evidence and asset provenance
  tests/         isolated behavioral tests
  tools/         initial migration, face import, CSV authoring, publication checks
  web/           interactive application and bundled browser assets
```

```sh
# Validate the rule/workflow behavior without changing the real database
python3 -m unittest discover -s studio/tests -v

# Check deterministic room tiling, face selection and edge cuts
node studio/tests/tile-layout.mjs

# Browser checks against the running local application (requires Playwright)
node studio/tests/browser.mjs
node studio/tests/room-faces.mjs
node studio/tests/render-depth.mjs

# Inspect current findings
python3 studio/backend/cli.py evaluate

# Regenerate CSV files and the public review snapshot from SQLite
python3 studio/backend/cli.py export

# Validate an edited product CSV, then apply it deliberately
python3 studio/backend/cli.py import --table products --file studio/data/exports/products.csv
python3 studio/backend/cli.py import --table products --file studio/data/exports/products.csv --apply
```

For each operating update: back up SQLite, import or use the forms, review the result, export, then commit and push the intended files. Do not re-run initial migration as an update mechanism. `initialize.py` retains an existing database. Shared-drive originals are never modified or copied into GitHub.

Current limitations and the next acceptance criteria are in [ROADMAP.md](docs/ROADMAP.md). The app is a local pilot with an explicit trusted operator role, not a deployed multi-user authorization system. [DATA_AND_ASSETS.md](docs/DATA_AND_ASSETS.md) describes the data contract and input formats. [AGENT_CONTRACT.md](docs/AGENT_CONTRACT.md) describes agent access.
