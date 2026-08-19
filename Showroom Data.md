# Anatolia Showroom Manager — Data Reference

The manager now covers **five showrooms**. This file documents all of them:

| Showroom | Place | Stage | Data file | Source BOM |
|---|---|---|---|---|
| **APS Temporary** | Aliağa · İzmir | Installed | `showroom-data.js` (hand-built) | `APS_TemporaryShowroom_BOM_20260609` |
| **Öz Yapı** | Manisa | Built | `data/showroom-manisa.js` | `Manisa_Öz Yapı_BOM_20260716` |
| **Ekinox** | Bursa | Built | `data/showroom-ekinox.js` | `EkinoxBursa_BOM_wSecondRoundSlabs_20250826` |
| **Ark Yapı · Banyo Marka** | Ankara | BOM only | `data/showroom-ankara.js` | `Ankara Ark Yapı_20260715` |
| **Turkuaz Seba Central** | İstanbul | Concept | `data/showroom-turkuaz.js` | `Turkuaz_İstShowroom_BOM_20260405` |

The four `data/showroom-*.js` files are **generated** — run `python3 tools/build_showroom_data.py`
after any BOM change rather than editing them. The workbooks in `two new showrooms/` are the
source of truth; the tables in this file are a readable mirror of what the script extracts.

> Note: this file was previously titled "Anatolia Ekinox Showroom" while describing the APS
> Aliağa booth. Renamed 2026-07-29, now that a real Ekinox (Bursa) showroom is in the manager.

---

# 1 · APS Temporary Showroom — Aliağa, İzmir

_380 m² (≈ 29.0 × 13.4 m) · Temporary Factory Showroom_
_Source: APS BOM 2026-06-09 + APS Temporary Showroom drawings 2025-11-21._

---

## Booth structure

The booth reads as two facing **C / reverse-C** wings wrapped around a **central display island**.

- **Central island** — the merchandising heart: the 160×320 sliding bank + Sample Tower (left), the 24 double-sided **Fixed Panel Library** (centre), the 120×280 sliding bank + **Waterfall** installation (right).
- **Perimeter stations 1–8** — each numbered station has up to four faces (A/B/C/D) and stages **floor + wall + furniture + panel** as a room vignette (meeting room, fireplace/living, bathroom, kitchen, size-study wall, rotating displays).

### Display systems at a glance

| System | Location | Format | Count | Size |
|---|---|---|---|---|
| Sliding bank A | Room 4 | Sliding Panel | 24 slabs | 160 × 320 cm |
| Sliding bank B | Room 5 | Sliding Panel | 24 mini-slabs | 120 × 280 cm |
| Waterfall | Room 6 | Waterfall | 21 displays | 60 × 280 cm |
| Fixed Panel Library | Hall | Pre-fixed Panel (double-sided) | 24 panels / 46 faces | 160×320 & 162×322 cm |
| Rotating tile units | Room 8 | Rotating Panel | 2 units (~21 tiles) | 120 × 120 cm |
| Porcelain floor | Main Floors | Floor | 8 fields | 120 × 120 cm |
| Size-study wall (5C) | Station 5 | On Wall | 1 study | multi-size + hex mosaic |
| Fireplace (Station 2) | Living | In Furniture | 1 | Travertino Titanium |

---

## Sliding Bank A — Room 4 · 160 × 320 cm (24 slabs)

_Pull-out sliding panels. Arranged left→right; 12 mm slabs sit on the outermost rails. Click the bank on the plan to see this list._

| # | Product | Finish | Thk | Product No |
|---|---|---|---|---|
| Slab 1 | Onyx Halo | Honed | 12 mm | 8000-0467-1 |
| Slab 2 | Monoforma Silhouette | Polished | 12 mm | 8000-0521-1 |
| Slab 3 | Armani Noir | Honed | 6 mm | 8000-0186-0 |
| Slab 4 | Calacatta Carrara | Honed | 6 mm | 8000-0046-0 |
| Slab 5 | Fusion White | Honed | 6 mm | 8000-0246-0 |
| Slab 6 | Publica Thunder | Organic Matte | 6 mm | 8000-0565-0 |
| Slab 7 | Nero Marquina | Polished | 6 mm | 8000-0268-1 |
| Slab 8 | Montagna Jade | Honed | 6 mm | 8000-0262-0 |
| Slab 9 | Serena Flint | Honed | 6 mm | 8000-0543-1 |
| Slab 10 | Travertino Titanium | Grained | 6 mm | 8000-0538-0 |
| Slab 11 | Super White | Honed | 6 mm | 8000-0294-0 |
| Slab 12 | Publica Terrain | Patinated | 6 mm | 8000-0562-0 |
| Slab 13 | Cristallo | Polished | 6 mm | 8000-0232-0 |
| Slab 14 | Calacatta Viola | Polished | 6 mm | 8000-0048-0 |
| Slab 15 | Publica Horizon | Patinated | 6 mm | 8000-0560-0 |
| Slab 16 | French Vanilla | Polished | 6 mm | 8000-0529-0 |
| Slab 17 | Serena Crater | Honed | 6 mm | 8000-0541-1 |
| Slab 18 | Marina White | Polished | 6 mm | 8000-0256-0 |
| Slab 19 | Lithoform Crosscut Dunes | Vintage | 6 mm | 8000-0549-0 |
| Slab 20 | Travertino Classico | Grained | 6 mm | 8000-0577-0 |
| Slab 21 | Taj Mahal | Honed | 6 mm | 8000-0599-0 |
| Slab 22 | Monoforma Storm | Polished | 12 mm | 8000-0519-1 |
| Slab 23 | Colorado Lincoln | Polished | 12 mm | 8000-0463-1 |
| Slab 24 | Calacatta Noir | Satin | 12 mm | 8000-0476-1 |

## Sliding Bank B — Room 5 · 120 × 280 cm (24 mini-slabs)

_Pull-out sliding panels, left→right. Click the bank on the plan to see this list._

| # | Product | Finish | Thk | Product No |
|---|---|---|---|---|
| Mini Slab 01 | Lithoform Crosscut Twilight | Honed | 6 mm | 8500-0089-0 |
| Mini Slab 02 | Lithoform Veincut Twilight | Honed | 6 mm | 8500-0101-0 |
| Mini Slab 03 | Lustra Onyx Feather | Polished | 6 mm | 8500-0686-0 |
| Mini Slab 04 | Majesto Arabescato Corchia | Honed | 6 mm | 8500-0013-1 |
| Mini Slab 05 | Majesto Atlantic Ocean | Polished | 6 mm | 8500-0053-0 |
| Mini Slab 06 | Majesto Bianco Dior | Polished | 6 mm | 8500-0046-0 |
| Mini Slab 07 | Majesto Calacatta Borghini | Honed | 6 mm | 8500-0033-1 |
| Mini Slab 08 | Majesto Calacatta Corchia | Polished | 6 mm | 8500-0018-0 |
| Mini Slab 09 | Serena Pewter | Honed | 6 mm | 8500-0074-0 |
| Mini Slab 10 | Majesto Verdi Alpi | Honed | 6 mm | 8500-0041-1 |
| Mini Slab 12 | Majesto Crystal Bianco | Honed | 6 mm | 8500-0057-1 |
| Mini Slab 11 | Lustra Onyx Sage | Polished | 6 mm | 8500-0064-0 |
| Mini Slab 13 | Majesto Forge Eleganza | Honed | 6 mm | 8500-0039-0 |
| Mini Slab 14 | Majesto Statuario | Polished | 6 mm | 8500-0014-0 |
| Mini Slab 15 | Monoforma Moonlight | Silk | 6 mm | 8500-0111-0 |
| Mini Slab 16 | Serena Valley | Honed | 6 mm | 8500-0078-0 |
| Mini Slab 17 | Lustra Onyx Hazel | Honed | 6 mm | 8500-0067-0 |
| Mini Slab 18 | Lithoform Crosscut Dunes | Honed | 6 mm | 8500-0080-0 |
| Mini Slab 22 | Lithoform Veincut Dunes | Honed | 6 mm | 8500-0092-0 |
| Mini Slab 19 | Majesto Macchia Vecchia | Polished | 6 mm | 8500-0042-0 |
| Mini Slab 20 | Majesto Calacatta Cremo | Honed | 6 mm | 8500-0027-1 |
| Mini Slab 21 | Majesto Oro Noir | Honed | 6 mm | 8500-0045-0 |
| Mini Slab 23 | Lustra Onyx Crema | Honed | 6 mm | 8500-0063-0 |
| Mini Slab 24 | Majesto Sahara Noir | Honed | 6 mm | 8500-0049-0 |

## Waterfall — Room 6 · 60 × 280 cm (21 displays)

_Slabs cascading counter→floor. Two runs: one starts kitchen-side (Lithoform Crosscut Coast / Display 10), one starts courtyard-mirror-side (Display 16). Each waterfall installation carries ~6 products front & back._

| # | Product | Finish | Thk | Product No |
|---|---|---|---|---|
| Waterfall Display 01 | Lithoform Crosscut Coast | Honed | 6 mm | 8500-0083-0 |
| Waterfall Display 02 | Lithoform Veincut Coast | Honed | 6 mm | 8500-0095-0 |
| Waterfall Display 03 | Majesto Gemma Bronze | Honed | 6 mm | 8500-0031-0 |
| Waterfall Display 04 | Majesto French Vanilla | Honed | 6 mm | 8500-0037-0 |
| Waterfall Display 05 | Serena Crater | Honed | 6 mm | 8500-0070-1 |
| Waterfall Display 06 | Majesto Calacatta Noir | Honed | 6 mm | 8500-0051-1 |
| Waterfall Display 07 | Monoforma Oasis | Silk | 6 mm | 8500-0113-0 |
| Waterfall Display 08 | Majesto Taj Mahal | Honed | 6 mm | 8500-0035-1 |
| Waterfall Display 09 | Majesto Bianco Stratura | Polished | 6 mm | 8500-0028-1 |
| Waterfall Display 10 | Majesto Ariel Bianco | Honed | 6 mm | 8500-0023-0 |
| Waterfall Display 11 | Majesto Travertino Classico | Honed | 6 mm | 8500-0052-0 |
| Waterfall Display 12 | Lithoform Crosscut Vista | Honed | 6 mm | 8500-0086-0 |
| Waterfall Display 13 | Lithoform Veincut Vista | Honed | 6 mm | 8500-0098-0 |
| Waterfall Display 14 | Monoforma Moonlight | Honed | 6 mm | 8500-0631-0 |
| Waterfall Display 15 | Serena Dusk | Honed | 6 mm | 8500-0076-0 |
| Waterfall Display 16 | Serena Flint | Organic Matte | 6 mm | 8500-0069-0 |
| Waterfall Display 17 | Majesto Ceppo di Gre | Honed | 6 mm | 8500-0058-0 |
| Waterfall Display 18 | Serena Shale | Honed | 6 mm | 8500-0072-1 |
| Waterfall Display 19 | Lustra Onyx Halo | Honed | 6 mm | 8500-0061-0 |
| Waterfall Display 20 | Majesto Travertino Titanium | Organic Matte | 6 mm | 8500-0059-0 |
| Waterfall Display 21 | Majesto Bianco Gioia | Honed | 6 mm | 8500-0017-0 |

## Fixed Panel Library — Hall · pre-fixed panels (46 faces → 24 panels)

_Centre island, diagonal walls. Most panels show one product on the **A (front)** face and a different one on the **B (back)** face. **Two panels are bookmatch** — the same slab mirrored on both faces — and so use a single product entry each: **Calacatta Noir Block 34** (P03) and **Macchia Vecchia Block 42** (P21). That is why 46 face-entries make **24** panels, not 23: 22 two-sided × 2 + 2 bookmatch × 1 = 46. Hover a panel on the plan to read its faces._

| Panel | Front (A face) | Back (B face) |
|---|---|---|
| P01 | Bianco Gioia Block 19 Bookmatch | Onyx Halo Block 44 Bookmatch |
| P02 | Arabescato Vagli Block 34 | Bianco Dior Block 38 |
| **P03** | **Calacatta Noir Block 34** | **= same (bookmatch)** |
| P04 | Nero Marquina Block 26 | Verdi Alpi |
| P05 | Calacatta Corchia Block 43 | Armani Noir Block 17 |
| P06 | Crystal Bianco Block 50 | Serena Shale |
| P07 | Publica Thunder | Monoforma Silhouette |
| P08 | Ariel Bianco Block 33 | Calacatta Viola Block 41 |
| P09 | Foresta Block 56 | Travertino Classico |
| P10 | Travertino Titanium Block 39 | Grigio Quarzo Block 21 |
| P11 | Ceppo di Gre Block 71 | Terrazzo Delicato |
| P12 | Fusion White Block 27 | Montagna Jade Block 14 |
| P13 | Panda Block 22 | Super White Block 28 |
| P14 | Calacatta Carrara Block 23 | Atlantic Ocean Honed |
| P15 | Montagna Grey Block 11 | Pietra Imperiale |
| P16 | Calacatta Cremo Block 31 | Sahara Noir Block 15 |
| P17 | Bianco Stratura Block 18 | Lithoform Veincut Coast |
| P18 | Lithoform Crosscut Coas | French Vanilla |
| P19 | Arabescato Corchia Block 59 | Forge Eleganza |
| P20 | Calacatta Oro Block 12 | Oro Noir Block 25 Bookmatch |
| **P21** | **Macchia Vecchia Block 42** | **= same (bookmatch)** |
| P22 | Taj Mahal Block 36 | Marina White Block 46 |
| P23 | Calacatta Picasso Block 32 | Gemma Bronze Block 45 |
| P24 | Statuario Block 16 | Calacatta Borghini Block 48 |

_Note: P24 pairs the two slabs (Statuario, Calacatta Borghini) that the bookmatch panels left unpaired in the old 23-row table. If the wall-elevation sheets specify different front/back pairings, adjust here and in `fixedPanels()`._

## Rotating Tile Units — Room 8 · 120 × 120 cm porcelain

_Two swivel units. **Right unit** (kitchen-side, Lithoform/Lustra): first 5 tiles on the front panel, next 5 behind. **Left unit** (bathroom-side, Serena): same split._

| # | Product | Finish | Thk | Product No |
|---|---|---|---|---|
| Rotating Tile Display | Lustra Onyx Crema | Polished | 9 mm | 8500-0152-0 |
| Rotating Tile Display | Lustra Onyx Hazel | Polished | 9 mm | 8500-0156-0 |
| Rotating Tile Display | Majesto Calacatta Cremo | Honed | 9 mm | 8500-0131-0 |
| Rotating Tile Display | Majesto Calacatta Oro | Honed | 9 mm | 8500-0129-0 |
| Rotating Tile Display | Majesto French Vanilla | Polished | 9 mm | 8500-0136-0 |
| Rotating Tile Display | Majesto Pietra Imperiale | Polished | 9 mm | 8500-0643-0 |
| Rotating Tile Display | Majesto Taj Mahal | Polished | 9 mm | 8500-0134-0 |
| Rotating Tile Display | Lithoform Crosscut Coast | Organic Matte | 9 mm | 8500-0174-0 |
| Rotating Tile Display | Lithoform Crosscut Twilight | Organic Matte | 9 mm | 8500-0180-0 |
| Rotating Tile Display | Lithoform Crosscut Vista | Organic Matte | 9 mm | 8500-0177-0 |
| Rotating Tile Display | Lustra Onyx Feather | Polished | 9 mm | 8500-0688-0 |
| Rotating Tile Display | Lustra Onyx Sage | Polished | 9 mm | 8500-0154-0 |
| Rotating Tile Display | Majesto Bianco Gioia | Polished | 9 mm | 8500-0122-0 |
| Rotating Tile Display | Majesto Calacatta Borghini | Honed | 9 mm | 8500-0133-0 |
| Rotating Tile Display | Majesto Calacatta Corchia | Polished | 9 mm | 8500-0124-0 |
| Rotating Tile Display | Majesto Crystal Bianco | Polished | 9 mm | 8500-0146-0 |
| Rotating Tile Display | Majesto Forge Eleganza | Polished | 9 mm | 8500-0138-0 |
| Rotating Tile Display | Majesto Statuario | Honed | 9 mm | 8500-0121-0 |
| Rotating Tile Display | Serena Dusk | Organic Matte | 9 mm | 8500-0167-0 |
| Rotating Tile Display | Serena Pewter | Organic Matte | 9 mm | 8500-0165-0 |

## Porcelain Floors — Main Floors · 120 × 120 cm

| Field | Product |
|---|---|
| F1–F4 | Serena Crater Honed |
| F5 | Lithoform Crosscut Dunes Honed |
| F6 | Majesto Arabescato Corchia Honed |
| F7 | Majesto Ceppo di Gre Honed |
| F8 | Majesto Calacatta Noir Honed |

## Perimeter stations 1–8 (walls · floor · furniture)

| Station | Faces | Wall installation | Notes |
|---|---|---|---|
| 1 — Bathroom | 1A–1D | **1A·1C** Pietra Imperiale (Honed) + **1B·1D** Arabescato Corchia (Polished bookmatch) | **1A** Vanity top (Pietra Imperiale Satin, 12 mm) |
| 2 — Living/Fireplace | 2A–2D | **2A·2B·2D** Lithoform Veincut Vista + **2C** Majesto Calacatta Noir (waterfall-on-wall) | Fireplace in the middle — Travertino Titanium face (6 mm) + hearth (Grained, 12 mm) |
| 3 — Meeting/Library | 3A–3D | **3A·3B·3C** Lithoform Crosscut Vista + **3D** Statuario Block 16 & Block 17 (B-grade) | Pendant-lit table (Oro Noir, 125×280 cm), library shelves |
| 4 — Sliding Bank A | 4A–4D | **4C** Foresta (Polished, single bookmatched panel) | 160×320 sliding bank staged in this room (see Sliding Bank A above) |
| 5 — Sliding Bank B | 5A–5D | **5C** Majesto Taj Mahal "sizes at a glance" wall | 120×120 / 60×120 / 90×90 / 60×60 / 30×60 / 5 cm hex mosaic / 120×280 slab · 120×280 sliding bank staged in this room |
| 6 — Waterfall/Corchia | 6A–6D | **6A** Majesto Calacatta Corchia 120×280 (waterfall-on-wall, random install) | Freestanding waterfall cascade display also staged in this room |
| 7 — Kitchen/Travertino | 7A–7D | **7C** Majesto Travertino Classico 120×280 (waterfall-on-wall, random install) | Kitchen counter + hood (no BOM slab code) |
| 8 — Rotating/Porcelain | 8A–8D | **8A** Gemma Bronze · **8B** Lithoform Crosscut Vista/Twilight · **8C** Lithoform Crosscut/Veincut mix + Serena (Shale/Valley/Crater/Dusk) · **8D** Serena Pewter/Flint | Near the 2 rotating tile displays (20 tiles) |

> ⚠️ Fixed 2026-07-06: rows 4 and 5 previously described "Meeting-room walls" — that was Station 3's content misattributed to Station 4 under an old area numbering. Station 4 is Sliding Bank A's room (wall 4C = Foresta only); Station 3 is the Meeting/Library room. `EXTRAS` in `Showroom Manager.dc.html` reconciled to match — see the BOM CSV (`APS_TemporaryShowroom_BOM_20260609.csv`) for the source rows.

## Furniture & fixtures

- Decorative Cube 01/02 (40×80×80 cm), Decorative Cube 02 (90×90×35 cm), Decorative Cube 05 / Bench (160×40×40 cm)
- Chaise Lounge, Armchair, TV, Meeting table + chairs
- Fireplace (Travertino Titanium, Station 2), Library shelves (LED-lit), Music Centre, Kitchen hood (LED under-light)
- 2× Rotating 120×120 tile displays

---

<!-- BEGIN GENERATED SHOWROOM TABLES -->
<!-- Regenerate with: python3 tools/build_showroom_docs.py -->

# 2 · Öz Yapı Showroom — Manisa

_≈ 480 m² single storey · Built_
_Source: `Manisa_Öz Yapı_BOM_20260716.xlsx` + `Anatolia_ÖZYAPI ManisaShowroom_20260108.pdf` (LAY + RCP)._

A long east–west floor. The **60 × 280 cm product library** (capacity 51) runs along the
north-west wall in three stacked rack runs; the **angled sliding unit** (“Açılı Sürgülü
Sergileme”, capacity 24) sits at its foot as two facing books — Panel A and Panel B,
twelve positions each.

Panels **A-2** and **B-2** are sub-size boards: one MDF panel carrying the same colour in
120×120, 60×120, 60×60 and 30×60. That is why each sliding group holds 15 rows rather
than 12 — eleven full 120 × 280 panels plus the four tiles on the board.

The staged rooms wrap the south and east edges: bathroom (6A–7E), fireplace
(Şömine, 5A–5G), entrance bookmatch + decorative cubes (1A–2E), kitchen & sales
(4A–4C) and the library wall (3A–3G).

> The Manisa sheet carries `N/A` in the **Pre Cut** column on Panels 10 and 36. That is
> *not* a cancellation — it means no pre-cut is required. All 51 library panels are kept.

### Groups at a glance

| Group | Format | Location | Rows | Default size |
|---|---|---|---|---|
| Sliding Panel A | Sliding Panel | Sliding Bank A | 15 | 120 × 280 cm |
| Sliding Panel B | Sliding Panel | Sliding Bank B | 15 | 120 × 280 cm |
| Product Library | Pre-fixed Panel | Product Library | 51 | 60 × 280 cm |
| Entrance | On Wall | Entrance | 6 | 120 × 280 cm |
| Kitchen & Sales | On Wall | Kitchen & Sales | 4 | 120 × 280 cm |
| Library Wall | On Wall | Library Wall | 2 | 120 × 280 cm |
| Fireplace | On Wall | Fireplace | 3 | 120 × 280 cm |
| Bathroom | On Wall | Bathroom | 6 | 120 × 280 cm |
| Floors | Floor | Main Floors | 1 | 120 × 120 cm |

**Total: 103 surfaces.**

### Sliding Panel A — Sliding Bank A

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Panel A-1 | Calacatta Cremo | Honed | 6 mm | 120 × 280 cm | 8500-0027-1 |
| Panel A-2 · 120 × 120 cm | Calacatta Cremo | Polished | 9 mm | 120 × 120 cm | 8500-0130-0 |
| Panel A-2 · 60 × 120 cm | Calacatta Cremo | Honed | 9 mm | 60 × 120 cm | 8500-0131-0 |
| Panel A-2 · 60 × 60 cm | Calacatta Cremo | Honed | 9 mm | 60 × 60 cm | 8500-0220-0 |
| Panel A-2 · 30 × 60 cm | Calacatta Cremo | Honed | 9 mm | 30 × 60 cm | 8500-0316-0 |
| Panel A-3 | Macchia Vecchia | Polished | 6 mm | 120 × 280 cm | 8500-0042-0 |
| Panel A-4 | Oro Noir | Polished | 6 mm | 120 × 280 cm | 8500-0044-0 |
| Panel A-5 | Foresta | Polished | 6 mm | 120 × 280 cm | 8000-0236-0 |
| Panel A-6 | Pietra Imperiale | Honed | 6 mm | 120 × 280 cm | 8000-0282-0 |
| Panel A-7 | Sahara Noir | Polished | 6 mm | 120 × 280 cm | 8500-0048-0 |
| Panel A-8 | Calacatta Noir | Honed | 6 mm | 120 × 280 cm | 8500-0051-1 |
| Panel A-9 | Montagna Jade | Honed | 6 mm | 120 × 280 cm | 8000-0262-0 |
| Panel A-10 | Armani Noir | Honed | 6 mm | 120 × 280 cm | 8000-0186-0 |
| Panel A-11 | Bianco Dior | Polished | 6 mm | 120 × 280 cm | 8500-0046-0 |
| Panel A-12 | Verdi Alpi | Polished | 6 mm | 120 × 280 cm | 8500-0040-1 |

### Sliding Panel B — Sliding Bank B

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Panel B-1 | Majesto Calacatta Noir | Polished | 6 mm | 120 × 280 cm | 8500-0050-1 |
| Panel B-2 · 120 × 120 cm | Majesto Calacatta Noir | Polished | 9 mm | 120 × 120 cm | 8500-0144-0 |
| Panel B-2 · 60 × 120 cm | Majesto Calacatta Noir | Honed | 9 mm | 60 × 120 cm | 8500-0438-0 |
| Panel B-2 · 60 × 60 cm | Majesto Calacatta Noir | Honed | 9 mm | 60 × 60 cm | 8500-0438-0 |
| Panel B-2 · 30 × 60 cm | Majesto Calacatta Noir | Honed | 9 mm | 30 × 60 cm | 8500-0438-0 |
| Panel B-3 | Calacatta Viola | Honed | 6 mm | 120 × 280 cm | 8000-0050-0 |
| Panel B-4 | Calacatta Picasso | Polished | 6 mm | 120 × 280 cm | 8000-0224-0 |
| Panel B-5 | Calacatta Cremo | Honed | 6 mm | 120 × 280 cm | 8500-0027-1 |
| Panel B-6 | Majesto Bianco Stratura | Honed | 6 mm | 120 × 280 cm | 8500-0029-1 |
| Panel B-7 | Marina White | Honed | 6 mm | 120 × 280 cm | 8000-0258-0 |
| Panel B-8 | Calacatta Carrara | Polished | 6 mm | 120 × 280 cm | 8000-0044-0 |
| Panel B-9 | Fusion White | Polished | 6 mm | 120 × 280 cm | 8000-0244-0 |
| Panel B-10 | Montagna Grey | Polished | 6 mm | 120 × 280 cm | 8000-0264-0 |
| Panel B-11 | Majesto Arabescato Corchia | Honed | 6 mm | 120 × 280 cm | 8500-0013-0 |
| Panel B-12 | Majesto Travertino Titanium | Honed | 6 mm | 120 × 280 cm | 8500-0054-0 |

### Product Library — Product Library

_60 × 280 cm Ürün Kütüphanesi · capacity 51_

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Panel 01 | Serena Crater | Honed | 6 mm | 60 × 280 cm | 8500-0070-1 |
| Panel 02 | Serena Dusk | Honed | 6 mm | 60 × 280 cm | 8500-0076-0 |
| Panel 03 | Serena Flint | Organic Matte | 6 mm | 60 × 280 cm | 8500-0069-0 |
| Panel 04 | Serena Pewter | Honed | 6 mm | 60 × 280 cm | 8500-0074-0 |
| Panel 05 | Serena Shale | Honed | 6 mm | 60 × 280 cm | 8500-0072-1 |
| Panel 06 | Serena Valley | Honed | 6 mm | 60 × 280 cm | 8500-0078-0 |
| Panel 07 | Lithoform Crosscut Vista | Organic Matte | 6 mm | 60 × 280 cm | 8500-0087-0 |
| Panel 08 | Lithoform Crosscut Dunes | Honed | 6 mm | 60 × 280 cm | 8500-0080-0 |
| Panel 09 | Lithoform Crosscut Coast | Honed | 6 mm | 60 × 280 cm | 9902-2921-0 |
| Panel 10 | Lithoform Crosscut Coast | Vintage | 6 mm | 60 × 280 cm | 8500-0085-0 |
| Panel 11 | Lithoform Veincut Vista | Organic Matte | 6 mm | 60 × 280 cm | 8500-0099-0 |
| Panel 12 | Lithoform Veincut Dunes | Honed | 6 mm | 60 × 280 cm | 8500-0092-0 |
| Panel 13 | Lithoform Veincut Coast | Honed | 6 mm | 61 × 280 cm | 8500-0095-0 |
| Panel 14 | Lithoform Crosscut Twilight | Organic Matte | 6 mm | 60 × 280 cm | 8500-0090-0 |
| Panel 15 | Monoforma Moonlight | Honed | 6 mm | 60 × 280 cm | 8500-0631-0 |
| Panel 16 | Monoforma Moonlight | Silk | 6 mm | 60 × 280 cm | 8500-0111-0 |
| Panel 17 | Monoforma Oasis | Polished | 6 mm | 60 × 280 cm | 8500-0112-0 |
| Panel 18 | Publica Thunder | Patinated | 6 mm | 60 × 280 cm | 8000-0564-0 |
| Panel 19 | Publica Terrain | Organic Matte | 6 mm | 60 × 280 cm | 8000-0563-0 |
| Panel 20 | Publica Horizon | Patinated | 6 mm | 60 × 280 cm | 8000-0560-0 |
| Panel 21 | Calacatta Carrara | Polished | 6 mm | 60 × 280 cm | 8000-0044-0 |
| Panel 22 | Majesto Ceppo di Gre | Honed | 6 mm | 60 × 280 cm | 8500-0058-0 |
| Panel 23 | Fusion White | Polished | 6 mm | 60 × 280 cm | 8000-0244-0 |
| Panel 24 | Sahara Noir | Polished | 6 mm | 60 × 280 cm | 8500-0048-0 |
| Panel 25 | Lustra Onyx Halo | Polished | 6 mm | 60 × 280 cm | 8500-0060-0 |
| Panel 26 | Montagna Jade Block 14 Bookmatch | Honed | 6 mm | 60 × 280 cm | 8000-0262-0 |
| Panel 27 | Fusion White | Honed | 6 mm | 60 × 280 cm | 8000-0246-0 |
| Panel 28 | Nero Marquina | Honed | 6 mm | 60 × 280 cm | 8000-0270-0 |
| Panel 29 | Ariel Bianco | Polished | 6 mm | 60 × 280 cm | 9902-2862-0 |
| Panel 30 | Panda | Polished | 6 mm | 60 × 280 cm | 9902-2960-0 |
| Panel 31 | Oro Noir | Polished | 6 mm | 60 × 280 cm | 9902-2959-0 |
| Panel 32 | Pietra Imperiale | Honed | 6 mm | 60 × 280 cm | 9902-2962-0 |
| Panel 33 | Majesto Bianco Stratura | Polished | 6 mm | 60 × 280 cm | 8500-0028-0 |
| Panel 34 | Pietra Imperiale | Polished | 6 mm | 60 × 280 cm | 8000-0280-0 |
| Panel 35 | Majesto Statuario | Honed | 6 mm | 60 × 280 cm | 8500-0015-0 |
| Panel 36 | Marina White | Honed | 6 mm | 60 × 280 cm | 8000-0258-0 |
| Panel 37 | Macchia Vecchia | Polished | 6 mm | 60 × 280 cm | 9902-2937-0 |
| Panel 38 | Majesto Statuario | Polished | 6 mm | 60 × 280 cm | 8500-0014-0 |
| Panel 39 | Gemma Bronze | Polished | 6 mm | 60 × 280 cm | 9902-2919-0 |
| Panel 40 | Foresta | Honed | 6 mm | 60 × 280 cm | 8000-0238-0 |
| Panel 41 | Crystal Bianco | Polished | 6 mm | 60 × 280 cm | 9902-2907-0 |
| Panel 42 | Foresta | Polished | 6 mm | 60 × 280 cm | 9902-2909-0 |
| Panel 43 | Calacatta Picasso | Honed | 6 mm | 60 × 280 cm | 9902-2894-0 |
| Panel 44 | Grigio Quarzo | Honed | 6 mm | 60 × 280 cm | 8000-0250-0 |
| Panel 45 | Bianco Dior | Honed | 6 mm | 60 × 280 cm | 8500-0047-0 |
| Panel 46 | Bianco Gioia | Polished | 6 mm | 60 × 280 cm | 8000-0196-0 |
| Panel 47 | Armani Noir | Polished | 6 mm | 60 × 280 cm | 9902-2865-0 |
| Panel 48 | Arabescato Corchia | Honed | 6 mm | 60 × 280 cm | 8500-0013-0 |
| Panel 49 | Calacatta Borghini | Honed | 6 mm | 60 × 280 cm | 9902-2876-0 |
| Panel 50 | Verdi Alpi | Polished | 6 mm | 60 × 280 cm | 9902-2998-0 |
| Panel 51 | Montagna Grey | Polished | 6 mm | 60 × 280 cm | 8000-0264-0 |

### Entrance — Entrance

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| L duvar 1A , 1B | Majesto Travertino Classico | Honed | 6 mm | 120 × 280 cm | 8500-0052-0 |
| L duvar 1D , 1E | Majesto Taj Mahal | Honed | 6 mm | 120 × 280 cm | 8500-0035-2 |
| Dekoratif Küp 01, 1C | Travertino Classico Block 55 Bookmatch | Grained | 12 mm | 80 × 80 × 60 cm | 8000-0172-1 |
| Dekoratif Küp 02, 1F | Taj Mahal Block 36 Bookmatch | Polished | 12 mm | 80 × 80 × 60 cm | 8000-0417-0 |
| Giriş Bookmatch , 2A , 2B, 2C, 2D | Gemma Bronze Block 45 Bookmatch | Polished | 6 mm | 160 × 320 cm | 8000-0208-0 |
| Masa Tablası, 2E | Calacatta Oro Block 12 Bookmatch | Honed | 12 mm | 80 cm Ø | 8000-0086-1 |

### Kitchen & Sales — Kitchen & Sales

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Tezgah arkası yan duvar, 4B | Lithoform Crosscut Vista | Honed | 6 mm | 120 × 280 cm | 8500-0086-0 |
| Tezgah arkası duvar, 4C | Lithoform Crosscut Vista | Honed | 6 mm | 120 × 280 cm | 8500-0086-0 |
| Mobilya Tezgahı , 4C | Lithoform Crosscut Vista | Honed | 6 mm | 120 × 280 cm | 8500-0086-0 |
| Ada Tezgah , 4A | Lithoform Veincut Vista | Organic Matte | 6 mm | 120 × 280 cm | 8500-0099-0 |

### Library Wall — Library Wall

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Bookmatch Duvar, 3A,3B, 3C, 3D | Majesto Bianco Dior Bookmatch | Polished | 6 mm | 120 × 280 cm | 8500-0046-0 |
| Yan Duvarlar, 3E, 3F, 3G | Majesto Calacatta Borghini | Honed | 6 mm | 120 × 280 cm | 8500-0033-1 |

### Fireplace — Fireplace

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Şömine , 5A, 5B, 5C, 5D | Panda Block 22 Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0278-0 |
| Şömine Alt Tabla | Panda Block 22 Bookmatch | Honed | 12 mm | 162 × 322 cm | 8000-0146-1 |
| Yan duvarlar, 5F, 5G ,5E | Lustra Onyx Halo | Honed | 6 mm | 120 × 280 cm | 8500-0061-0 |

### Bathroom — Bathroom

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Banyo tezgahı, 6D | Calacatta Corchia Block 43 Bookmatch | Satin | 12 mm | 162 × 322 cm | 8000-0322-1 |
| Banyo tezgah arkası duvar, 6A | Calacatta Corchia Block 43 Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0202-0 |
| Banyo oda etrafı duvarlar 6E, 6F | Majesto Forge Eleganza | Honed | 6 mm | 120 × 280 cm | 8500-0039-0 |
| Küvet yanı duvar, 7C | Majesto Travertino Titanium | Honed | 6 mm | 120 × 280 cm | 8500-0054-0 |
| Banyo L duvar 7A, 7B | Majesto Travertino Titanium | Honed | 6 mm | 120 × 280 cm | 8500-0054-0 |
| Banyo L duvar 7E, 7D | Majesto Oro Noir | Polished | 6 mm | 120 × 280 cm | 8500-0044-0 |

### Floors — Main Floors

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Genel Showroom | Serena Crater | Honed | 9 mm | 120 × 120 cm | 8500-0160-0 |


---

# 3 · Ekinox Showroom — Bursa

_≈ 83 m² open area · Built · shared floor_
_Source: `EkinoxBursa_BOM_wSecondRoundSlabs_20250826 (1).xlsx` + `AnatoliaEkinoxShowroom_Bursa_20250416.pdf` (LAY)._

A shared floor. Anatolia takes the **west wing**; a partner bath brand takes the east
wing, which carries no Anatolia BOM rows and is drawn muted on the plan. Storage and
WCs run along the north wall, and an 83.03 m² open hall with the entrance sits between
the two wings.

The west wing holds two display banks of ten 120 × 280 panels (A-2 and A-4 are sub-size
boards), a 60 × 280 library of thirty, a clad column, three decorative cubes, and the
kitchen, meeting/TV and bathroom settings.

> Two library rows are marked **CANCEL** in the BOM Notes column — Panel 10 (Lithoform
> Crosscut Coast, Vintage) and Panel 29 (Marina White) — and are excluded, leaving 30
> panels numbered 01–30. Their slots were refilled by the `NEW ADD` rows (Pietra
> Imperiale on Panel 10, Travertino Titanium on Panel 29).
>
> The 2025-04-16 drawing quotes an earlier capacity (31 + 24 + 10 = 65 products); the
> 2025-08-26 BOM supersedes it and is what the dashboard shows.

### Groups at a glance

| Group | Format | Location | Rows | Default size |
|---|---|---|---|---|
| Display Panel A | Sliding Panel | Display Bank A | 16 | 120 × 280 cm |
| Display Panel B | Sliding Panel | Display Bank B | 10 | 120 × 280 cm |
| Product Library | Pre-fixed Panel | Product Library | 30 | 60 × 280 cm |
| Kitchen | In Furniture | Kitchen | 2 | 162 × 322 cm |
| Meeting Area | In Furniture | Meeting Area | 3 | 125 × 280 cm |
| Bathroom | On Wall | Bathroom | 3 | 160 × 320 cm |
| Column Cladding | On Wall | Column | 2 | 120 × 280 cm |
| Decorative Cubes | In Furniture | Decorative Cubes | 3 | 162 × 322 cm |
| Floors | Floor | Main Floors | 1 | 120 × 120 cm |

**Total: 70 surfaces.**

### Display Panel A — Display Bank A

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Panel A-1 | Calacatta Corchia | Polished | 6 mm | 120 × 280 cm | 8500-0018-1 |
| Panel A-2 · 120 × 120 cm | Calacatta Corchia | Honed | 9 mm | 120 × 120 cm | 8500-0125-0 |
| Panel A-2 · 60 × 120 cm | Calacatta Corchia | Honed | 9 mm | 60 × 120 cm | 8500-0432-0 |
| Panel A-2 · 60 × 60 cm | Calacatta Corchia | Polished | 9 mm | 60 × 60 cm | 8500-0219-0 |
| Panel A-2 · 30 × 60 cm | Calacatta Corchia | Polished | 9 mm | 30 × 60 cm | 8500-0315-0 |
| Panel A-3 | Taj Mahal | Polished | 6 mm | 120 × 280 cm | 8500-0034-1 |
| Panel A-4 · 120 × 120 cm | Taj Mahal | Honed | 9 mm | 120 × 120 cm | 8500-0135-0 |
| Panel A-4 · 60 × 120 cm | Taj Mahal | Polished | 9 mm | 60 × 120 cm | 8500-0530-0 |
| Panel A-4 · 60 × 60 cm | Taj Mahal | Polished | 9 mm | 60 × 60 cm | 8500-0297-0 |
| Panel A-4 · 30 × 60 cm | Taj Mahal | Polished | 9 mm | 30 × 60 cm | 8500-0405-0 |
| Panel A-5 | Arabescato Corchia | Honed | 6 mm | 120 × 280 cm | 8500-0013-1 |
| Panel A-6 | Statuario | Polished | 6 mm | 120 × 280 cm | 8500-0014-0 |
| Panel A-7 | Ariel Bianco | Honed | 6 mm | 120 × 280 cm | 8500-0023-0 |
| Panel A-8 | Calacatta Cremo | Honed | 6 mm | 120 × 280 cm | 8500-0027-1 |
| Panel A-9 | Bianco Stratura | Polished | 6 mm | 120 × 280 cm | 8500-0028-1 |
| Panel A-10 | Gemma Bronze | Polished | 6 mm | 120 × 280 cm | 8500-0030-0 |

### Display Panel B — Display Bank B

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Panel B-1 | Calacatta Borghini | Polished | 6 mm | 120 × 280 cm | 8500-0032-1 |
| Panel B-2 | Forge Eleganza | Honed | 6 mm | 120 × 280 cm | 8500-0039-0 |
| Panel B-3 | Atlantic Ocean | Polished | 6 mm | 120 × 280 cm | 8500-0053-0 |
| Panel B-4 | Macchia Vecchia | Honed | 6 mm | 120 × 280 cm | 8500-0043-0 |
| Panel B-5 | Oro Noir | Polished | 6 mm | 120 × 280 cm | 8500-0044-0 |
| Panel B-6 | Sahara Noir | Polished | 6 mm | 120 × 280 cm | 8500-0048-0 |
| Panel B-7 | Crystal Bianco | Honed | 6 mm | 120 × 280 cm | 8500-0057-1 |
| Panel B-8 | Ceppo Di Gre | Honed | 6 mm | 120 × 280 cm | 8500-0058-0 |
| Panel B-9 | Onyx Halo | Polished | 6 mm | 120 × 280 cm | 8500-0060-0 |
| Panel B-10 | Bianco Dior | Honed | 6 mm | 120 × 280 cm | 8500-0047-0 |

### Product Library — Product Library

_60 × 280 cm Ürün Kütüphanesi · 30 panels after 2 cancellations_

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Panel 01 | Serena Crater | Honed | 6 mm | 60 × 280 cm | 8500-0070-1 |
| Panel 02 | Serena Dusk | Honed | 6 mm | 60 × 280 cm | 8500-0076-0 |
| Panel 03 | Serena Flint | Organic Matte | 6 mm | 60 × 280 cm | 8500-0069-0 |
| Panel 04 | Serena Pewter | Honed | 6 mm | 60 × 280 cm | 8500-0074-0 |
| Panel 05 | Serena Shale | Honed | 6 mm | 60 × 280 cm | 8500-0072-1 |
| Panel 06 | Serena Valley | Honed | 6 mm | 60 × 280 cm | 8500-0078-0 |
| Panel 07 | Lithoform Crosscut Vista | Organic Matte | 6 mm | 60 × 280 cm | 8500-0087-0 |
| Panel 08 | Lithoform Crosscut Dunes | Honed | 6 mm | 60 × 280 cm | 8500-0080-0 |
| Panel 09 | Lithoform Crosscut Coast | Honed | 6 mm | 60 × 280 cm | 8500-0083-0 |
| Panel 10 | Pietra Imperiale | Polished | 6 mm | 60 × 280 cm | 8000-0280-0 |
| Panel 11 | Lithoform Veincut Vista | Organic Matte | 6 mm | 60 × 280 cm | 8500-0099-0 |
| Panel 12 | Lithoform Veincut Dunes | Honed | 6 mm | 60 × 280 cm | 8500-0092-0 |
| Panel 13 | Lithoform Veincut Coast | Honed | 6 mm | 60 × 280 cm | 8500-0095-0 |
| Panel 14 | Monoforma Moonlight | Honed | 6 mm | 60 × 280 cm | 8500-0631-0 |
| Panel 15 | Monoforma Moonlight | Polished | 6 mm | 60 × 280 cm | 8500-0110-0 |
| Panel 16 | Monoforma Oasis | Polished | 6 mm | 60 × 280 cm | 8500-0112-0 |
| Panel 17 | Monoforma Silhouette | Silk | 6 mm | 60 × 280 cm | 8500-0117-0 |
| Panel 18 | Publica Thunder | Patinated | 6 mm | 60 × 280 cm | 8000-0564-0 |
| Panel 19 | Publica Terrain | Organic Matte | 6 mm | 60 × 280 cm | 8000-0563-0 |
| Panel 20 | Publica Horizon | Patinated | 6 mm | 60 × 280 cm | 8000-0560-0 |
| Panel 21 | Calacatta Carrara | Polished | 6 mm | 60 × 280 cm | 8000-0044-0 |
| Panel 22 | Panda | Honed | 6 mm | 60 × 280 cm | 8000-0278-0 |
| Panel 23 | Fusion White | Polished | 6 mm | 60 × 280 cm | 8000-0244-0 |
| Panel 24 | Calacatta Picasso | Polished | 6 mm | 60 × 280 cm | 8000-0224-0 |
| Panel 25 | Calacatta Viola | Honed | 6 mm | 60 × 280 cm | 8000-0050-0 |
| Panel 26 | Foresta | Honed | 6 mm | 60 × 280 cm | 8000-0238-0 |
| Panel 27 | Armani Noir | Honed | 6 mm | 60 × 280 cm | 8000-0186-0 |
| Panel 28 | Nero Marquina | Honed | 6 mm | 60 × 280 cm | 8000-0270-0 |
| Panel 29 | Travertino Titanium | Honed | 6 mm | 60 × 280 cm | 8500-0054-0 |
| Panel 30 | Montagna Jade | Honed | 6 mm | 60 × 280 cm | 8000-0262-0 |

### Kitchen — Kitchen

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Ada Unite Tezgahi | Calacatta Noir | Honed | 12 mm | 162 × 322 cm | 8000-0082-1 |
| Mutfak tezgah ve tezgah arasi | Calacatta Noir | Honed | 12 mm | 162 × 322 cm | 8000-0082-1 |

### Meeting Area — Meeting Area

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Buyuk Masa Tablasi 01 | Travertino Classico | Honed | 12 mm | 125 × 280 cm | 8000-0174-1 |
| Buyuk Masa Tablasi 02 | Super White | Honed | 12 mm | 125 × 280 cm | 8000-0170-1 |
| Tv Unitesi arka pano ve tezgah | Gemma Bronze | Honed | 6 mm | 160 × 320 cm | 8000-0210-0 |

### Bathroom — Bathroom

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Kuvet Arkasi Duvar/Kolon | Bianco Gioia | Polished | 6 mm | 160 × 320 cm | 8000-0196-0 |
| Dus alani ici Duvar | Bianco Gioia | Polished | 6 mm | 160 × 320 cm | 8000-0196-0 |
| Tezgah Arkasi Duvar | Bianco Dior | Polished | 6 mm | 160 × 320 cm | 8000-0192-0 |

### Column Cladding — Column

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Kolon etrafi urun doseme 01 | Verdi Alpi | Polished | 6 mm | 120 × 280 cm | 8500-0040-1 |
| Kolon etrafi urun doseme 02 | Arabescato Corchia | Honed | 6 mm | 120 × 280 cm | 8500-0013-1 |

### Decorative Cubes — Decorative Cubes

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Dekoratif Kup 01 | Calacatta Oro | Honed | 12 mm | 90 × 90 × 35 cm | 8000-0086-1 |
| Dekoratif Kup 02 | Publica Horizon | Patinated | 12 mm | 80 × 80 × 60 cm | 8000-0477-1 |
| Dekoratif Kup 03 | Lithoform Crosscut Coast | Vintage | 12 mm | 60 × 60 × 90 cm | 8000-0487-1 |

### Floors — Main Floors

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Genel Showroom | Serena Shale | Organic Matte | 9 mm | 120 × 120 cm | 8500-0163-0 |


---

# 4 · Ark Yapı · Banyo Marka — Ankara

_Ground floor + mezzanine · BOM only — no drawing issued_
_Source: `Ankara Ark Yapı _20260715_BOM -_ 1.xlsx`. No LAY sheet supplied._

The only showroom without an architectural drawing. Its plan in the dashboard is a
**schematic derived from the BOM location codes**, not a measured layout: the `GF-` /
`MF-` prefixes split it into a ground-floor band and a mezzanine band, and every block
on the plan is one BOM location group. Positions are indicative only — the product
runs behind each block are exact.

The workbook's `code` sheet defines the coding scheme: location (`GF`/`MF`/`B1`/`L1`),
area (`ENT`/`LOB`/`KIT`/`BTH`/`MT01`/`DLA`/…), surface (`FL`/`WL`/`CT`/`TOP`/`VAN`/…)
and element (`CUBE01–11`/`SLP01–06`/`TBL01–02`/`FPL01`/…).

> Product numbers ending in `*` mark substitutions; the `*` is stripped when the data
> file is generated. The Aeterna sample tower is a fixture line (`9902-2477-0`, 75
> A-shape chips) with no colour or size of its own, so it is entered descriptively.

### Groups at a glance

| Group | Format | Location | Rows | Default size |
|---|---|---|---|---|
| Sliding Panels | Sliding Panel | Sliding Bank 160 | 12 | 160 × 320 cm |
| Mini Slabs | Sliding Panel | Sliding Bank 120 | 12 | 120 × 280 cm |
| Waterfall Slabs | Waterfall | Waterfall | 6 | 60 × 280 cm |
| Rotating Tile Displays | Rotating Panel | Rotating Units | 3 | — |
| Sample Tower | Tower | Sample Tower | 1 | 30 × 30 cm |
| Fireplace | On Wall | Fireplace | 2 | — |
| Meeting Area | In Furniture | Meeting Area | 3 | — |
| Bathroom | On Wall | Bathroom | 3 | — |
| Design Area | On Wall | Design Area | 2 | — |
| Stair Wall & Treads | On Wall | Stairs | 1 | 120 × 280 cm |
| Decorative Cubes | In Furniture | Decorative Cubes | 11 | 162 × 322 cm |
| Floors | Floor | Main Floors | 4 | 120 × 120 cm |

**Total: 60 surfaces.**

### Sliding Panels — Sliding Bank 160

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Sliding Panels 1 | Calacatta Viola Block 41 Bookmatch | Polished | 6 mm | 160 × 320 cm | 8000-0048-0 |
| Sliding Panels 2 | Oro Noir Block 25 Bookmatch | Polished | 6 mm | 160 × 320 cm | 8000-0272-0 |
| Sliding Panels 3 | Pietra Imperiale Block 30 Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0282-0 |
| Sliding Panels 4 | Macchia Vecchia Block 42 Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0252-0 |
| Sliding Panels 5 | Sahara Noir | Polished | 6 mm | 160 × 320 cm | 8000-0594-0 |
| Sliding Panels 6 | Super White Block 28 Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0294-0 |
| Sliding Panels 7 | Armani Noir Block 17 Bookmatch | Polished | 6 mm | 160 × 320 cm | 8000-0184-0 |
| Sliding Panels 8 | Bianco Dior Block 38 Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0194-0 |
| Sliding Panels 9 | Bianco Stratura | Honed | 6 mm | 160 × 320 cm | 8000-0523-0 |
| Sliding Panels 10 | Taj Mahal Block 36 Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0413-0 |
| Sliding Panels 11 | Gemma Bronze Block 45 Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0208-0 |
| Sliding Panels 12 | Calacatta Noir | Polished | 6 mm | 160 × 320 cm | 8000-0590-0 |

### Mini Slabs — Sliding Bank 120

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Mini Slab 1 | Lithoform Crosscut Vista | Honed | 6 mm | 120 × 280 cm | 8500-0086-0 |
| Mini Slab 2 | Lithoform Veincut Twilight | Honed | 6 mm | 120 × 280 cm | 8500-0101-0 |
| Mini Slab 3 | Bianco Gioia | Polished | 6 mm | 120 × 280 cm | 8500-0016-0 |
| Mini Slab 4 | Majesto Calacatta Cremo | Honed | 6 mm | 120 × 280 cm | 8500-0027-1 |
| Mini Slab 5 | Majesto Atlantic Ocean | Polished | 6 mm | 120 × 280 cm | 8500-0053-0 |
| Mini Slab 6 | Majesto Calacatta Borghini | Honed | 6 mm | 120 × 280 cm | 8500-0033-1 |
| Mini Slab 7 | Majesto Calacatta Corchia | Polished | 6 mm | 120 × 280 cm | 8500-0018-0 |
| Mini Slab 8 | Serena Pewter | Honed | 6 mm | 120 × 280 cm | 8500-0074-0 |
| Mini Slab 9 | Majesto Crystal Bianco | Honed | 6 mm | 120 × 280 cm | 8500-0057-1 |
| Mini Slab 10 | Majesto Macchia Vecchia | Polished | 6 mm | 120 × 280 cm | 8500-0042-0 |
| Mini Slab 11 | Majesto Forge Eleganza | Honed | 6 mm | 120 × 280 cm | 8500-0039-0 |
| Mini Slab 12 | Lustra Onyx Halo | Honed | 6 mm | 120 × 280 cm | 8500-0061-0 |

### Waterfall Slabs — Waterfall

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Mini Half Slab 1 | Macchia Vecchia | Honed | 6 mm | 60 × 280 cm | 8500-0043-0 |
| Mini Half Slab 2 | Serena Valley | Honed | 6 mm | 60 × 280 cm | 8500-0078-0 |
| Mini Half Slab 3 | Majesto Calacatta Noir | Polished | 6 mm | 60 × 280 cm | 8500-0050-1 |
| Mini Half Slab 4 | Monoforma Moonlight | Polished | 6 mm | 60 × 280 cm | 8500-0631-0 |
| Mini Half Slab 5 | Majesto Statuario | Polished | 6 mm | 60 × 280 cm | 8500-0014-0 |
| Mini Half Slab 6 | Monoforma Silhouette | Silk | 6 mm | 60 × 280 cm | 8500-0117-0 |

### Rotating Tile Displays — Rotating Units

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| RTD 1 · 60 × 120 cm | Forge Eleganza | Polished | 9 mm | 60 × 120 cm | 8500-0455-0 |
| RTD 2 · 90 × 90 cm | French Vanilla | Polished | 9 mm | 90 × 90 cm | 8500-0568-0 |
| RTD 3 · 120 × 120 cm | Taj Mahal | Polished | 9 mm | 120 × 120 cm | 8500-0134-0 |

### Sample Tower — Sample Tower

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| 75 × 30 × 30 cm A-shape chips | Aeterna Finishes Sample Tower | Polished · Honed · Satin | 6 mm | 30 × 30 cm | 9902-2477-0 |

### Fireplace — Fireplace

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| FPL-01 · Şömine | Verdi Alpi | Polished | 12 mm | 162 × 322 cm | 8000-0176-1 |
| FPL-02 · Şömine Duvar | Lithoform Veincut Dunes | Honed | 6 mm | 120 × 280 cm | 8500-0092-0 |

### Meeting Area — Meeting Area

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| GF-MT-01 · Toplantı Masa Tablası | Bianco Dior Block 38 Bookmatch | Honed | 12 mm | 162 × 322 cm | 8000-0062-1 |
| GF-MT-02 · Toplantı Duvar | Montagna Grey Block 11 Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0266-1 |
| GF-MT-03 · Toplantı Alanı Dolap Üzeri Tezgah | Lithoform Crosscut Twilight | Honed | 6 mm | 120 × 280 cm | 8500-0089-0 |

### Bathroom — Bathroom

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| MF-BATH 01 · Banyo lavabo arka duvar | Arabescato Corchia Block 59 Bookmatch | Polished | 12 mm | 160 × 320 cm | 8000-0036-0 |
| MF-BATH 02 · Banyo Duvar | Arabescato Corchia | Honed | 6 mm | 120 × 280 cm | 8500-0013-1 |
| MF-BATH 03 · Banyo Lavabo Tezgah | Arabescato Corchia Block 59 Bookmatch | Honed | 12 mm | 162 × 322 cm | 8000-0010-1 |

### Design Area — Design Area

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| MF-TOP 01 · Tasarım Masa Tablası | Serena Shale | Honed | 12 mm | 162 × 322 cm | 8000-0494-1 |
| MF-WL 01 · Tasarım Alanı Duvar | Lithoform Crosscut Twilight | Honed | 6 mm | 120 × 280 cm | 8500-0089-0 |

### Stair Wall & Treads — Stairs

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| MF-ST+WL 01 · Merdiven Duvar + Basamak | Travertino Titanium | Honed | 6 mm | 120 × 280 cm | 8500-0054-0 |

### Decorative Cubes — Decorative Cubes

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Decorative cube 1 60 x 150 x 35 cm (2 adet) | Calacatta Corchia Block 43 Bookmatch | Honed | 12 mm | 162 × 322 cm | 8000-0034-1 |
| Decorative cube 2 30 x 30 x 40 cm | Montagna Jade | Honed | 12 mm | 162 × 322 cm | 8000-0130-1 |
| Decorative cube 3 40x 40 x 50 cm | Nero Marquina | Honed | 12 mm | 162 × 322 cm | 8000-0138-1 |
| Decorative cube 4 50 x50 x 60 cm | Ariel Bianco Block 33 Bookmatch | Honed | 12 mm | 162 × 322 cm | 8000-0030-1 |
| Decorative cube 5 160 x 40 x 40 cm | Crystal Bianco Block 50 Bookmatch | Honed | 12 mm | 162 × 322 cm | 8000-0440-2 |
| Decorative cube 6 160x 40 x40 cm | Grigio Quarzo Block 21 Bookmatch | Honed | 12 mm | 162 × 322 cm | 8000-0118-1 |
| Decorative cube 7 50 x 60 x 70 cm | Sahara Noir Block 15 | Honed | 12 mm | 162 × 322 cm | 8000-0154-1 |
| Decorative cube 8 50 x 60 x 70 cm | Calacatta Borghini Block 48 Bookmatch | Honed | 12 mm | 162 × 322 cm | 8000-0434-2 |
| Decorative cube 9 50 x 60 x 70 cm | Forge Eleganza Block 20 Bookmatch | Satin | 12 mm | 162 × 322 cm | 8000-0484-1 |
| Decorative cube 10 50 x 60 x 70 cm | Macchia Vecchia Block 42 Bookmatch | Polished | 12 mm | 162 × 322 cm | 8000-0120-1 |
| Decorative cube 11 50 x 60 x 70 cm | Calacatta Noir Block 34 Bookmatch | Honed | 12 mm | 162 × 322 cm | 8000-0082-1 |

### Floors — Main Floors

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| GF-F01 · Giriş Kat Zemin | Majesto Ceppo di Gre | Honed | 9 mm | 120 × 120 cm | 8500-0148-0 |
| GF-F02 · Giriş Kat Zemin | Serena Crater | Honed | 9 mm | 120 × 120 cm | 8500-0160-0 |
| MF-01 · Asma Kat Genel Zemin | Serena Shale | Honed | 9 mm | 120 × 120 cm | 8500-0162-0 |
| MF-02 · Banyo Zemin | Serena Flint | Honed | 9 mm | 120 × 120 cm | 8500-0158-0 |


---

# 5 · Turkuaz Seba Central — İstanbul

_≈ 240 m² · Concept (Option 01)_
_Source: `Turkuaz_İstShowroom_BOM_20260405.xlsx` + `Turkuaz_ConceptPresentation.pdf` (Option 01)._

Concept stage. Everything Anatolia shows sits in a **single angled + sliding unit** at
the entrance end. Its 36 positions interleave in the BOM: 26 are full **mini slabs**
(120 × 280 cm) and 10 are **sub-size boards** (positions 8, 11, 14, 17, 20, 23, 26, 29,
32, 35), each carrying one colour in four to five formats down to 5 cm and 10 cm hex
mosaic. Twelve 160 × 320 slabs sit above them.

A second sheet (“Ekstra 8 Ürün 120x 280”) adds one extra 120 × 280 slab to eight of the
ten boards, plus one Grigio Quarzo noted as replacing Foresta.

> The remaining concept areas — bath vignette, island unit, service kitchen and WCs —
> carry no Anatolia BOM rows and are shown muted on the plan.
>
> The concept PDF quotes 44 products (12 + 12 + 9 + 11); the 2026-04-05 BOM expands the
> unit to 91 rows and is what the dashboard shows.

### Groups at a glance

| Group | Format | Location | Rows | Default size |
|---|---|---|---|---|
| Full Slabs | Sliding Panel | Sliding Unit · Slabs | 12 | 160 × 320 cm |
| Mini Slabs | Sliding Panel | Sliding Unit · Mini Slabs | 26 | 120 × 280 cm |
| Subsize Boards | On Wall | Subsize Boards | 44 | — |
| Extra Mini Slabs | Sliding Panel | Extra Mini Slabs | 9 | 120 × 280 cm |

**Total: 91 surfaces.**

### Full Slabs — Sliding Unit · Slabs

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Slab 1 | Majesto Arabescato Corchia | Polished | 6 mm | 160 × 320 cm | 8000-0036-0 |
| Slab 2 | Verdi Alpi | Polished | 6 mm | 160 × 320 cm | 8000-0596-0 |
| Slab 3 | Majesto Bianco Dior Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0194-0 |
| Slab 4 | Super White Block 28 Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0294-0 |
| Slab 5 | Armani Noir Block 17 Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0186-0 |
| Slab 6 | Grigio Quarzo Block 21 Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0250-0 |
| Slab 7 | Atlantic Ocean | Polished | 6 mm | 160 × 320 cm | 8000-0188-0 |
| Slab 8 | Oro Noir | Polished | 6 mm | 160 × 320 cm | 8000-0272-0 |
| Slab 9 | Majesto Gemma Bronze Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0210-0 |
| Slab 10 | Calacatta Viola Block 41 Bookmatch | Honed | 6 mm | 160 × 320 cm | 8000-0050-0 |
| Slab 11 | Nero Marquina | Honed | 6 mm | 160 × 320 cm | 8000-0270-1 |
| Slab 12 | Macchia Vecchia | Polished | 6 mm | 160 × 320 cm | 8000-0252-0 |

### Mini Slabs — Sliding Unit · Mini Slabs

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Mini Slab 1 | French Vanilia | Honed | 6 mm | 120 × 280 cm | 8500-0037-0 |
| Mini Slab 2 | Sahara Noir | Honed | 6 mm | 120 × 280 cm | 8500-0049-0 |
| Mini Slab 3 | Majesto Forge Eleganza | Honed | 6 mm | 120 × 280 cm | 8500-0039-0 |
| Mini Slab 4 | Majesto Calacatta Corchia | Honed | 6 mm | 120 × 280 cm | 8500-0019-0 |
| Mini Slab 5 | Monoforma Moonlight | Honed | 6 mm | 120 × 280 cm | 8500-0631-0 |
| Mini Slab 6 | Majesto Statuario | Honed | 6 mm | 120 × 280 cm | 8500-0015-0 |
| Mini Slab 7 | Majesto Calacatta Borghini | Polished | 6 mm | 120 × 280 cm | 8500-0032-1 |
| Mini Slab 9 | Majesto Pietra Imperiale | Polished | 6 mm | 120 × 280 cm | 8500-0645-0 |
| Mini Slab 10 | Majesto Travertino Classico | Honed | 6 mm | 120 × 280 cm | 8500-0052-0 |
| Mini Slab 12 | Travertino Titanium | Honed | 6 mm | 120 × 280 cm | 8500-0054-0 |
| Mini Slab 13 | Lustra Onyx Crema | Honed | 6 mm | 120 × 280 cm | 8500-0063-0 |
| Mini Slab 15 | Lustra Onyx Hazel | Honed | 6 mm | 120 × 280 cm | 8500-0067-0 |
| Mini Slab 16 | Majesto Ceppo di Gre | Honed | 6 mm | 120 × 280 cm | 8500-0058-0 |
| Mini Slab 18 | Majesto Ariel Bianco | Honed | 6 mm | 120 × 280 cm | 8500-0023-0 |
| Mini Slab 19 | Serena Crater | Honed | 6 mm | 120 × 280 cm | 8500-0070-0 |
| Mini Slab 21 | Serena Valley | Honed | 6 mm | 120 × 280 cm | 8500-0078-0 |
| Mini Slab 22 | Serena Dusk | Honed | 6 mm | 120 × 280 cm | 8500-0076-0 |
| Mini Slab 24 | Serena Pewter | Honed | 6 mm | 120 × 280 cm | 8500-0074-0 |
| Mini Slab 25 | Lithoform Veincut Dunes | Honed | 6 mm | 120 × 280 cm | 8500-0092-0 |
| Mini Slab 27 | Lithoform Veincut Coast | Honed | 6 mm | 120 × 280 cm | 8500-0095-0 |
| Mini Slab 28 | Lithoform Veincut Vista | Honed | 6 mm | 120 × 280 cm | 8500-0098-0 |
| Mini Slab 30 | Lithoform Veincut Twilight | Honed | 6 mm | 120 × 280 cm | 8500-0101-0 |
| Mini Slab 31 | Majesto Taj Mahal | Polished | 6 mm | 120 × 280 cm | 8500-0034-1 |
| Mini Slab 33 | Majesto Calacatta Cremo | Honed | 6 mm | 120 × 280 cm | 8500-0027-1 |
| Mini Slab 34 | Majesto Bianco Gioia | Honed | 6 mm | 120 × 280 cm | 8500-0017-0 |
| Mini Slab 36 | Majesto Calacatta Noir | Polished | 6 mm | 120 × 280 cm | 8500-0050-1 |

### Subsize Boards — Subsize Boards

_Ten boards, each carrying that colour in four to five sub-sizes_

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Subsize Board 8 · 60 × 60 cm | Majesto Calacatta Borghini | Honed | 9 mm | 60 × 60 cm | 8500-0214-0 |
| Subsize Board 8 · 30 × 60 cm | Majesto Calacatta Borghini | Vintage | 9 mm | 30 × 60 cm | 8500-0311-0 |
| Subsize Board 8 · 5 cm | Majesto Calacatta Borghini | Vintage | 9 mm | 5 cm | 8510-0008-0 |
| Subsize Board 8 · 60 × 120 cm | Majesto Calacatta Borghini | Polished | 9 mm | 60 × 120 cm | 8500-0431-0 |
| Subsize Board 8 · 120 × 120 cm | Majesto Pietra Imperiale | Honed | 9 mm | 120 × 120 cm | 8500-0644-0 |
| Subsize Board 11 · 30 × 60 cm | Majesto Travertino Classico | Grained | 9 mm | 30 × 60 cm | 8500-0406-0 |
| Subsize Board 11 · 5 cm | Majesto Travertino Classico | Organic Matte | 9 mm | 5 cm | 8510-0017-0 |
| Subsize Board 11 · 60 × 120 cm | Majesto Travertino Classico | Organic Matte | 9 mm | 60 × 120 cm | 8500-0533-0 |
| Subsize Board 11 · 60 × 120 cm | Travertino Titanium | Honed | 9 mm | 60 × 120 cm | 8500-0535-0 |
| Subsize Board 14 · 30 × 60 cm | Lustra Onyx Feather | Honed | 9 mm | 30 × 60 cm | 8500-0691-0 |
| Subsize Board 14 · 60 × 60 cm | Lustra Onyx Feather | Polished | 9 mm | 60 × 60 cm | 8500-0690-0 |
| Subsize Board 14 · 5 cm | Lustra Onyx Feather | Honed | 9 mm | 5 cm | 8510-0044-0 |
| Subsize Board 14 · 120 × 120 cm | Lustra Onyx Sage | Honed | 9 mm | 120 × 120 cm | 8500-0155-0 |
| Subsize Board 17 · 120 × 120 cm | Majesto Ceppo di Gre | Honed | 9 mm | 120 × 120 cm | 8500-0148-0 |
| Subsize Board 17 · 60 × 120 cm | Majesto Ceppo di Gre | Organic Matte | 9 mm | 60 × 120 cm | 8500-0446-0 |
| Subsize Board 17 · 5 cm | Majesto Ceppo di Gre | Organic Matte | 9 mm | 5 cm | 8510-0020-0 |
| Subsize Board 17 · 60 × 60 cm | Majesto Ceppo di Gre | Grained | 9 mm | 60 × 60 cm | 8500-0229-0 |
| Subsize Board 17 · 30 × 60 cm | Majesto Ceppo di Gre | Grained | 9 mm | 30 × 60 cm | 8500-0325-0 |
| Subsize Board 20 · 60 × 60 cm | Serena Crater | Vintage | 9 mm | 60 × 60 cm | 8500-0276-0 |
| Subsize Board 20 · 10 cm | Serena Crater | Organic Matte | 9 mm | 10 cm | 8510-0026-0 |
| Subsize Board 20 · 60 × 120 cm | Serena Crater | Organic Matte | 9 mm | 60 × 120 cm | 8500-0508-0 |
| Subsize Board 20 · 120 × 120 cm | Serena Valley | Honed | 9 mm | 120 × 120 cm | 8500-0168-0 |
| Subsize Board 23 · 60 × 60 cm | Serena Shale | Vintage | 9 mm | 60 × 60 cm | 8500-0288-0 |
| Subsize Board 23 · 60 × 120 cm | Serena Shale | Organic Matte | 9 mm | 60 × 120 cm | 8500-0520-0 |
| Subsize Board 23 · 10 cm | Serena Shale | Organic Matte | 9 mm | 10 cm | 8510-0027-0 |
| Subsize Board 23 · 120 × 120 cm | Serena Flint | Honed | 9 mm | 120 × 120 cm | 8500-0158-0 |
| Subsize Board 26 · 30 × 60 cm | Lithoform Crosscut Dunes | Vintage | 9 mm | 30 × 60 cm | 8500-0345-0 |
| Subsize Board 26 · 90 × 90 cm | Lithoform Crosscut Dunes | Organic Matte | 9 mm | 90 × 90 cm | 8500-0572-0 |
| Subsize Board 26 · 10 cm | Lithoform Crosscut Dunes | Organic Matte | 9 mm | 10 cm | 8510-0031-0 |
| Subsize Board 26 · 60 × 60 cm | Lithoform Crosscut Coast | Honed | 9 mm | 60 × 60 cm | 8500-0241-0 |
| Subsize Board 26 · 60 × 120 cm | Lithoform Crosscut Coast | Organic Matte | 9 mm | 60 × 120 cm | 8500-0460-0 |
| Subsize Board 29 · 60 × 60 cm | Lithoform Crosscut Vista | Vintage | 9 mm | 60 × 60 cm | 8500-0252-0 |
| Subsize Board 29 · 10 cm | Lithoform Crosscut Vista | Organic Matte | 9 mm | 10 cm | 8510-0033-0 |
| Subsize Board 29 · 60 × 120 cm | Lithoform Crosscut Vista | Organic Matte | 9 mm | 60 × 120 cm | 8500-0478-0 |
| Subsize Board 29 · 120 × 120 cm | Lithoform Crosscut Twilight | Honed | 9 mm | 120 × 120 cm | 8500-0179-0 |
| Subsize Board 32 · 60 × 120 cm | Majesto Taj Mahal | Polished | 9 mm | 60 × 120 cm | 8500-0530-0 |
| Subsize Board 32 · 60 × 60 cm | Majesto Taj Mahal | Honed | 9 mm | 60 × 60 cm | 8500-0295-0 |
| Subsize Board 32 · 5 cm | Majesto Taj Mahal | Honed | 9 mm | 5 cm | 8510-0009-0 |
| Subsize Board 32 · 30 × 60 cm | Majesto Taj Mahal | Honed | 9 mm | 30 × 60 cm | 8500-0403-0 |
| Subsize Board 32 · 120 × 120 cm | Majesto Calacatta Cremo | Honed | 9 mm | 120 × 120 cm | 8500-0131-0 |
| Subsize Board 35 · 60 × 60 cm | Majesto Bianco Gioia | Honed | 9 mm | 60 × 60 cm | 8500-0211-0 |
| Subsize Board 35 · 30 × 60 cm | Majesto Bianco Gioia | Vintage | 9 mm | 30 × 60 cm | 8500-0305-0 |
| Subsize Board 35 · 5 cm | Majesto Bianco Gioia | Vintage | 9 mm | 5 cm | 8510-0002-0 |
| Subsize Board 35 · 120 × 120 cm | Majesto Calacatta Noir | Polished | 9 mm | 120 × 120 cm | 8500-0144-0 |

### Extra Mini Slabs — Extra Mini Slabs

_Sheet 'Ekstra 8 Ürün 120x 280' — one added slab per subsize board_

| Location | Product | Finish | Thk | Size | Product No |
|---|---|---|---|---|---|
| Subsize Board 23 | Majesto Forge Eleganza | Honed | 6 mm | 120 × 280 cm | 8500-0039-0 |
| Subsize Board 35 | Majesto Crystal Bianco | Honed | 6 mm | 120 × 280 cm | 8500-0057-1 |
| Subsize Board 14 | Monoforma Oasis | Polished | 6 mm | 120 × 280 cm | 8500-0112-0 |
| Subsize Board 8 | Monoforma Silhouette | Silk | 6 mm | 120 × 280 cm | 8500-0117-0 |
| Subsize Board 20 | Serena Shale | Honed | 6 mm | 120 × 280 cm | 8500-0072-0 |
| Subsize Board 32 | Majesto Crystal Bianco | Honed | 6 mm | 120 × 280 cm | 8500-0057-1 |
| Subsize Board 26 | Lithoform Crosscut Dunes | Honed | 6 mm | 120 × 280 cm | 8500-0080-0 |
| Subsize Board 29 | Lithoform Crosscut Coast | Honed | 6 mm | 120 × 280 cm | 8500-0083-0 |
| foresta yerine gelecek | Grigio Quarzo Block 21 Bookmatch Cut | Honed | 6 mm | 120 × 280 cm | 8000-0250-0 |


<!-- END GENERATED SHOWROOM TABLES -->
