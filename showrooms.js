// Showroom registry — one entry per floor the manager can switch between.
// Loaded after showroom-data.js and data/showroom-*.js.
//
// `meta` feeds every identity string in the UI (sidebar, overview hero, floor
// plan header and caption). `plan` is a schematic zone map in percentage
// coordinates, read off the architectural PDFs in "two new showrooms/".
//
//   zone.type   'system'  flat, numbered product run (a sliding bank, a library)
//               'station' a room — grouped by format (walls / floor / furniture)
//               'floor'   the floor field
//               'muted'   drawn but not clickable (stairs, partner wings, areas
//                         that carry no Anatolia BOM rows)
//   zone.keys   which data groups in data/showroom-<id>.js the zone contains
//   zone.art    'slats' | 'rack' | 'grid' | 'discs' | 'plain' — how it is drawn
//
// APS keeps `bespokePlan:true`: its floor plan is the hand-tuned, PDF-measured
// drawing already in the HTML and is rendered by its own branch, untouched.
//
// The four new plans are SCHEMATIC — zone shapes are proportional reads of the
// PDFs, not measured survey geometry. Anything that needs true dimensions
// should be rebuilt with the `showroom-floor-plan` skill against the LAY sheet.

window.SHOWROOMS = [
  {
    id: 'aps',
    bespokePlan: true,
    meta: {
      name: 'APS Temporary Showroom',
      partner: 'Anatolia Product Showroom',
      city: 'Aliağa',
      region: 'İzmir',
      area: '380 m²',
      stage: 'Installed',
      tagline: 'A complete reading of the floor — by surface, format and station.',
      blurb: 'A schematic top-down of the booth — two facing C / reverse-C wings of stations around a central island. Click a sliding bank or waterfall to read its product run; hover a centre panel for its front & back faces; click a station for its walls, floor and furniture. Use the legend to illuminate one format.',
      planCaption: '380 m² · Temporary Showroom · Aliağa',
      sidebarNote: 'Temporary Showroom',
      sidebarPlace: 'Aliağa · İzmir',
      sidebarAccent: '380 m² · C + reverse-C',
      hero: 'assets/photos/onyx-hall.jpg',
      source: 'APS_TemporaryShowroom_BOM_20260609 · APS_TemporaryShowroomProject_20251121 (LAY + RCP)'
    }
  },

  {
    id: 'manisa',
    meta: {
      name: 'Öz Yapı Showroom',
      partner: 'Öz Yapı',
      city: 'Manisa',
      region: 'Manisa',
      area: '≈ 480 m²',
      stage: 'Built',
      tagline: 'A long single-storey floor — library wall, angled sliding bank, four staged rooms.',
      blurb: 'A schematic top-down of the Manisa floor. The 60 × 280 cm product library runs along the north-west wall (capacity 51); the angled 120 × 280 cm sliding unit sits at its foot in two facing books of twelve. Click a bank or the library to read its run; click a room for its walls, counters and cubes.',
      planCaption: 'Öz Yapı · Manisa · schematic from the 2026-01-08 LAY sheet',
      sidebarNote: 'Öz Yapı Showroom',
      sidebarPlace: 'Manisa',
      sidebarAccent: 'Library 51 · Sliding 24',
      source: 'Manisa_Öz Yapı_BOM_20260716 · Anatolia_ÖZYAPI ManisaShowroom_20260108 (LAY + RCP)'
    },
    plan: {
      aspect: 44,
      entrance: 48,
      zones: [
        { id: 'floors', type: 'floor', keys: ['floors'], label: 'Main Floors', sub: 'Serena Crater 120 × 120 · whole floor', fmt: 'Floor', art: 'grid', x: 40, y: 32, w: 21, h: 14 },
        { id: 'library', type: 'station', keys: ['library'], label: 'Product Library', sub: '60 × 280 · capacity 51', fmt: 'Pre-fixed Panel', art: 'rack', x: 2, y: 3, w: 36, h: 41 },
        { id: 'slidingB', type: 'system', keys: ['slidingB'], label: 'Panel B', sub: '120 × 280 · book II', fmt: 'Sliding Panel', art: 'slats', x: 15, y: 49, w: 11, h: 22 },
        { id: 'slidingA', type: 'system', keys: ['slidingA'], label: 'Panel A', sub: '120 × 280 · book I', fmt: 'Sliding Panel', art: 'slats', x: 27, y: 49, w: 11, h: 22 },
        { id: 'bath', type: 'station', keys: ['bath'], label: 'Bathroom', sub: 'Banyo Teşhir · 6A–7E', fmt: 'On Wall', art: 'plain', x: 2, y: 75, w: 16, h: 23 },
        { id: 'fireplace', type: 'station', keys: ['fireplace'], label: 'Fireplace', sub: 'Şömine · Panda 5A–5G', fmt: 'In Furniture', art: 'plain', x: 20, y: 78, w: 14, h: 20 },
        { id: 'entry', type: 'station', keys: ['entry'], label: 'Entrance', sub: 'Giriş · bookmatch + cubes', fmt: 'On Wall', art: 'plain', x: 49, y: 75, w: 20, h: 23 },
        { id: 'kitchen', type: 'station', keys: ['kitchen'], label: 'Kitchen & Sales', sub: 'Mutfak Teşhir + Satış · 4A–4C', fmt: 'In Furniture', art: 'plain', x: 63, y: 40, w: 20, h: 22 },
        { id: 'libraryWall', type: 'station', keys: ['libraryWall'], label: 'Library Wall', sub: 'Kütüphane · 3A–3G', fmt: 'On Wall', art: 'plain', x: 71, y: 75, w: 24, h: 23 },
        { id: 'stairs', type: 'muted', label: 'Stairs', sub: '15 treads', x: 38, y: 3, w: 11, h: 24 },
        { id: 'adjacent', type: 'muted', label: 'Adjacent display', sub: 'Not in the Anatolia BOM', x: 51, y: 3, w: 46, h: 24 }
      ]
    }
  },

  {
    id: 'ekinox',
    meta: {
      name: 'Ekinox Showroom',
      partner: 'Ekinox',
      city: 'Bursa',
      region: 'Bursa',
      area: '≈ 83 m² open area',
      stage: 'Built',
      tagline: 'A shared floor — the Anatolia wing west, a partner bath wing east.',
      blurb: 'A schematic top-down of the Bursa floor. Anatolia occupies the west wing: two display banks of ten, a 60 × 280 cm library of thirty, a clad column, three cubes and the bath and meeting settings. The east wing is a partner brand and carries no Anatolia BOM rows, so it is shown muted.',
      planCaption: 'Ekinox · Bursa · schematic from the 2025-04-16 LAY sheet',
      sidebarNote: 'Ekinox Showroom',
      sidebarPlace: 'Bursa',
      sidebarAccent: 'Library 30 · Panels 20',
      source: 'EkinoxBursa_BOM_wSecondRoundSlabs_20250826 · AnatoliaEkinoxShowroom_Bursa_20250416 (LAY)'
    },
    plan: {
      aspect: 50,
      entrance: 52,
      zones: [
        { id: 'floors', type: 'floor', keys: ['floors'], label: 'Main Floors', sub: 'Serena Shale 120 × 120', fmt: 'Floor', art: 'grid', x: 1, y: 14, w: 46, h: 84 },
        { id: 'store', type: 'muted', label: 'Depo · WC', sub: 'Back of house', x: 1, y: 2, w: 46, h: 10 },
        { id: 'panelsA', type: 'system', keys: ['panelsA'], label: 'Bank A', sub: '120 × 280 · ten', fmt: 'Sliding Panel', art: 'slats', x: 2, y: 16, w: 13, h: 24 },
        { id: 'panelsB', type: 'system', keys: ['panelsB'], label: 'Bank B', sub: '120 × 280 · ten', fmt: 'Sliding Panel', art: 'slats', x: 16, y: 16, w: 13, h: 24 },
        { id: 'library', type: 'station', keys: ['library'], label: 'Product Library', sub: '60 × 280 · thirty', fmt: 'Pre-fixed Panel', art: 'rack', x: 30, y: 16, w: 17, h: 24 },
        { id: 'column', type: 'station', keys: ['column'], label: 'Column', sub: 'Kolon etrafı döşeme', fmt: 'On Wall', art: 'plain', x: 25, y: 44, w: 22, h: 12 },
        { id: 'cubes', type: 'station', keys: ['cubes'], label: 'Cubes', sub: 'Mosaic alanı · three', fmt: 'In Furniture', art: 'plain', x: 25, y: 59, w: 22, h: 12 },
        { id: 'meeting', type: 'station', keys: ['meeting'], label: 'Meeting & TV', sub: 'Toplantı Alanı', fmt: 'In Furniture', art: 'plain', x: 2, y: 44, w: 21, h: 12 },
        { id: 'kitchen', type: 'station', keys: ['kitchen'], label: 'Kitchen', sub: 'Ada ünite tezgahı', fmt: 'In Furniture', art: 'plain', x: 2, y: 59, w: 21, h: 12 },
        { id: 'bath', type: 'station', keys: ['bath'], label: 'Bathroom', sub: 'Duş alanı · Banyo', fmt: 'On Wall', art: 'plain', x: 2, y: 74, w: 45, h: 24 },
        { id: 'open', type: 'muted', label: 'Açık Alan', sub: '83.03 m² · entrance hall', x: 49, y: 2, w: 22, h: 96 },
        { id: 'partner', type: 'muted', label: 'Partner Wing', sub: 'Not in the Anatolia BOM', x: 73, y: 2, w: 26, h: 96 }
      ]
    }
  },

  {
    id: 'ankara',
    meta: {
      name: 'Ark Yapı Showroom',
      partner: 'Ark Yapı · Banyo Marka',
      city: 'Ankara',
      region: 'Ankara',
      area: 'Ground + mezzanine',
      stage: 'BOM only',
      tagline: 'Two levels read from location codes — no drawing issued yet.',
      blurb: 'Ankara has no LAY sheet yet, so this plan is a schematic derived from the BOM location codes rather than a measured drawing: the GF-/MF- prefixes split it into a ground-floor band and a mezzanine band, and each block is one BOM location group. Positions are indicative only — click a block to read its exact product run.',
      planCaption: 'Ark Yapı · Ankara · schematic from BOM location codes (no drawing issued)',
      sidebarNote: 'Ark Yapı · Banyo Marka',
      sidebarPlace: 'Ankara',
      sidebarAccent: 'GF + mezzanine · 60 surfaces',
      source: 'Ankara Ark Yapı_20260715_BOM — no architectural drawing supplied'
    },
    plan: {
      aspect: 58,
      entrance: 50,
      bands: [
        { label: 'Ground Floor · GF', y: 0.5 },
        { label: 'Mezzanine · MF', y: 48.5 }
      ],
      zones: [
        { id: 'sliding160', type: 'system', keys: ['sliding160'], label: 'Sliding Panels', sub: '160 × 320 · twelve', fmt: 'Sliding Panel', art: 'slats', x: 3, y: 6, w: 22, h: 17 },
        { id: 'sliding120', type: 'system', keys: ['sliding120'], label: 'Mini Slabs', sub: '120 × 280 · twelve', fmt: 'Sliding Panel', art: 'slats', x: 27, y: 6, w: 22, h: 17 },
        { id: 'waterfall', type: 'system', keys: ['waterfall'], label: 'Waterfall', sub: '60 × 280 · six', fmt: 'Waterfall', art: 'slats', x: 51, y: 6, w: 14, h: 17 },
        { id: 'rotating', type: 'system', keys: ['rotating'], label: 'Rotating', sub: 'Three size runs', fmt: 'Rotating Panel', art: 'discs', x: 67, y: 6, w: 14, h: 17 },
        { id: 'tower', type: 'system', keys: ['tower'], label: 'Sample Tower', sub: 'Aeterna · 75 chips', fmt: 'Tower', art: 'rack', x: 83, y: 6, w: 14, h: 17 },
        { id: 'fireplace', type: 'station', keys: ['fireplace'], label: 'Fireplace', sub: 'FPL-01 · FPL-02', fmt: 'In Furniture', art: 'plain', x: 3, y: 26, w: 22, h: 17 },
        { id: 'meeting', type: 'station', keys: ['meeting'], label: 'Meeting', sub: 'GF-MT-01…03', fmt: 'In Furniture', art: 'plain', x: 27, y: 26, w: 22, h: 17 },
        { id: 'cubes', type: 'station', keys: ['cubes'], label: 'Decorative Cubes', sub: 'CUBE 01–11 · GF + MF', fmt: 'In Furniture', art: 'plain', x: 51, y: 26, w: 30, h: 17 },
        { id: 'bath', type: 'station', keys: ['bath'], label: 'Bathroom', sub: 'MF-BATH 01…03', fmt: 'On Wall', art: 'plain', x: 3, y: 54, w: 22, h: 17 },
        { id: 'design', type: 'station', keys: ['design'], label: 'Design Area', sub: 'MF-TOP · MF-WL', fmt: 'On Wall', art: 'plain', x: 27, y: 54, w: 22, h: 17 },
        { id: 'stairs', type: 'station', keys: ['stairs'], label: 'Stairs', sub: 'MF-ST+WL 01', fmt: 'On Wall', art: 'plain', x: 51, y: 54, w: 30, h: 17 },
        { id: 'floors', type: 'floor', keys: ['floors'], label: 'Floors', sub: 'GF-F01/02 · MF-01/02', fmt: 'Floor', art: 'grid', x: 3, y: 76, w: 94, h: 16 }
      ]
    }
  },

  {
    id: 'turkuaz',
    meta: {
      name: 'Turkuaz Seba Central',
      partner: 'Turkuaz Seba',
      city: 'İstanbul',
      region: 'İstanbul',
      area: '≈ 240 m²',
      stage: 'Concept',
      tagline: 'Concept Option 01 — one angled sliding unit carrying the whole range.',
      blurb: 'Concept stage. The plan follows Option 01 of the Turkuaz concept presentation: a single angled + sliding unit at the entrance end carries the full range — twelve 160 × 320 slabs, twenty-six mini slabs and ten sub-size boards. Areas without Anatolia BOM rows (bath vignette, island unit, service kitchen) are shown muted.',
      planCaption: 'Turkuaz Seba Central · İstanbul · Concept Option 01 · ≈ 240 m²',
      sidebarNote: 'Turkuaz Seba Central',
      sidebarPlace: 'İstanbul',
      sidebarAccent: 'Concept · Option 01',
      source: 'Turkuaz_İstShowroom_BOM_20260405 · Turkuaz_ConceptPresentation (Option 01)'
    },
    plan: {
      aspect: 92,
      entrance: 50,
      zones: [
        { id: 'service', type: 'muted', label: 'Service Kitchen · WC', sub: 'Servis Mutfağı · no BOM rows', x: 6, y: 3, w: 88, h: 16 },
        { id: 'island', type: 'muted', label: 'Island Unit', sub: 'Ada ünitesi · concept', x: 52, y: 23, w: 42, h: 20 },
        { id: 'bathv', type: 'muted', label: 'Bath Vignette', sub: 'Sanitary display · concept', x: 6, y: 23, w: 42, h: 20 },
        { id: 'slabs', type: 'system', keys: ['slabs'], label: 'Full Slabs', sub: '160 × 320 · twelve', fmt: 'Sliding Panel', art: 'slats', x: 6, y: 47, w: 42, h: 20 },
        { id: 'minis', type: 'system', keys: ['minis'], label: 'Mini Slabs', sub: '120 × 280 · twenty-six', fmt: 'Sliding Panel', art: 'slats', x: 52, y: 47, w: 42, h: 20 },
        { id: 'boards', type: 'station', keys: ['boards'], label: 'Subsize Boards', sub: 'Ten boards · four to five sizes each', fmt: 'On Wall', art: 'rack', x: 6, y: 71, w: 42, h: 20 },
        { id: 'extras', type: 'system', keys: ['extras'], label: 'Extra Mini Slabs', sub: 'One per board · sheet 2', fmt: 'Sliding Panel', art: 'slats', x: 52, y: 71, w: 42, h: 20 }
      ]
    }
  }
];
