#!/usr/bin/env python3
"""Regenerate the four new-showroom sections of "Showroom Data.md".

Reads the same workbooks as build_showroom_data.py (via its builders, so the
tables can never drift from the JS the dashboard loads) and splices the result
between the BEGIN/END markers in the doc. The APS section above the markers is
hand-written and is never touched.

    python3 tools/build_showroom_docs.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import openpyxl  # noqa: E402

from build_showroom_data import BOOKS, BUILDERS, ROOT, SRC  # noqa: E402

DOC = ROOT / "Showroom Data.md"
START = "<!-- BEGIN GENERATED SHOWROOM TABLES -->"
END = "<!-- END GENERATED SHOWROOM TABLES -->"

ORDER = ["manisa", "ekinox", "ankara", "turkuaz"]

# The layout prose — the part no script can read off a spreadsheet.
BLURBS = {
    "manisa": {
        "title": "2 · Öz Yapı Showroom — Manisa",
        "meta": "_≈ 480 m² single storey · Built_\n"
                "_Source: `Manisa_Öz Yapı_BOM_20260716.xlsx` + "
                "`Anatolia_ÖZYAPI ManisaShowroom_20260108.pdf` (LAY + RCP)._",
        "prose":
            "A long east–west floor. The **60 × 280 cm product library** (capacity 51) runs along the\n"
            "north-west wall in three stacked rack runs; the **angled sliding unit** (“Açılı Sürgülü\n"
            "Sergileme”, capacity 24) sits at its foot as two facing books — Panel A and Panel B,\n"
            "twelve positions each.\n\n"
            "Panels **A-2** and **B-2** are sub-size boards: one MDF panel carrying the same colour in\n"
            "120×120, 60×120, 60×60 and 30×60. That is why each sliding group holds 15 rows rather\n"
            "than 12 — eleven full 120 × 280 panels plus the four tiles on the board.\n\n"
            "The staged rooms wrap the south and east edges: bathroom (6A–7E), fireplace\n"
            "(Şömine, 5A–5G), entrance bookmatch + decorative cubes (1A–2E), kitchen & sales\n"
            "(4A–4C) and the library wall (3A–3G).\n\n"
            "> The Manisa sheet carries `N/A` in the **Pre Cut** column on Panels 10 and 36. That is\n"
            "> *not* a cancellation — it means no pre-cut is required. All 51 library panels are kept.",
    },
    "ekinox": {
        "title": "3 · Ekinox Showroom — Bursa",
        "meta": "_≈ 83 m² open area · Built · shared floor_\n"
                "_Source: `EkinoxBursa_BOM_wSecondRoundSlabs_20250826 (1).xlsx` + "
                "`AnatoliaEkinoxShowroom_Bursa_20250416.pdf` (LAY)._",
        "prose":
            "A shared floor. Anatolia takes the **west wing**; a partner bath brand takes the east\n"
            "wing, which carries no Anatolia BOM rows and is drawn muted on the plan. Storage and\n"
            "WCs run along the north wall, and an 83.03 m² open hall with the entrance sits between\n"
            "the two wings.\n\n"
            "The west wing holds two display banks of ten 120 × 280 panels (A-2 and A-4 are sub-size\n"
            "boards), a 60 × 280 library of thirty, a clad column, three decorative cubes, and the\n"
            "kitchen, meeting/TV and bathroom settings.\n\n"
            "> Two library rows are marked **CANCEL** in the BOM Notes column — Panel 10 (Lithoform\n"
            "> Crosscut Coast, Vintage) and Panel 29 (Marina White) — and are excluded, leaving 30\n"
            "> panels numbered 01–30. Their slots were refilled by the `NEW ADD` rows (Pietra\n"
            "> Imperiale on Panel 10, Travertino Titanium on Panel 29).\n"
            ">\n"
            "> The 2025-04-16 drawing quotes an earlier capacity (31 + 24 + 10 = 65 products); the\n"
            "> 2025-08-26 BOM supersedes it and is what the dashboard shows.",
    },
    "ankara": {
        "title": "4 · Ark Yapı · Banyo Marka — Ankara",
        "meta": "_Ground floor + mezzanine · BOM only — no drawing issued_\n"
                "_Source: `Ankara Ark Yapı _20260715_BOM -_ 1.xlsx`. No LAY sheet supplied._",
        "prose":
            "The only showroom without an architectural drawing. Its plan in the dashboard is a\n"
            "**schematic derived from the BOM location codes**, not a measured layout: the `GF-` /\n"
            "`MF-` prefixes split it into a ground-floor band and a mezzanine band, and every block\n"
            "on the plan is one BOM location group. Positions are indicative only — the product\n"
            "runs behind each block are exact.\n\n"
            "The workbook's `code` sheet defines the coding scheme: location (`GF`/`MF`/`B1`/`L1`),\n"
            "area (`ENT`/`LOB`/`KIT`/`BTH`/`MT01`/`DLA`/…), surface (`FL`/`WL`/`CT`/`TOP`/`VAN`/…)\n"
            "and element (`CUBE01–11`/`SLP01–06`/`TBL01–02`/`FPL01`/…).\n\n"
            "> Product numbers ending in `*` mark substitutions; the `*` is stripped when the data\n"
            "> file is generated. The Aeterna sample tower is a fixture line (`9902-2477-0`, 75\n"
            "> A-shape chips) with no colour or size of its own, so it is entered descriptively.",
    },
    "turkuaz": {
        "title": "5 · Turkuaz Seba Central — İstanbul",
        "meta": "_≈ 240 m² · Concept (Option 01)_\n"
                "_Source: `Turkuaz_İstShowroom_BOM_20260405.xlsx` + "
                "`Turkuaz_ConceptPresentation.pdf` (Option 01)._",
        "prose":
            "Concept stage. Everything Anatolia shows sits in a **single angled + sliding unit** at\n"
            "the entrance end. Its 36 positions interleave in the BOM: 26 are full **mini slabs**\n"
            "(120 × 280 cm) and 10 are **sub-size boards** (positions 8, 11, 14, 17, 20, 23, 26, 29,\n"
            "32, 35), each carrying one colour in four to five formats down to 5 cm and 10 cm hex\n"
            "mosaic. Twelve 160 × 320 slabs sit above them.\n\n"
            "A second sheet (“Ekstra 8 Ürün 120x 280”) adds one extra 120 × 280 slab to eight of the\n"
            "ten boards, plus one Grigio Quarzo noted as replacing Foresta.\n\n"
            "> The remaining concept areas — bath vignette, island unit, service kitchen and WCs —\n"
            "> carry no Anatolia BOM rows and are shown muted on the plan.\n"
            ">\n"
            "> The concept PDF quotes 44 products (12 + 12 + 9 + 11); the 2026-04-05 BOM expands the\n"
            "> unit to 91 rows and is what the dashboard shows.",
    },
}


def section(sid, groups):
    b = BLURBS[sid]
    out = [f"# {b['title']}", "", b["meta"], "", b["prose"], "",
           "### Groups at a glance", "",
           "| Group | Format | Location | Rows | Default size |",
           "|---|---|---|---|---|"]
    for g in groups:
        out.append(f"| {g['label']} | {g['fmt']} | {g['room']} | {len(g['rows'])} | {g['size']} |")
    out += ["", f"**Total: {sum(len(g['rows']) for g in groups)} surfaces.**", ""]

    for g in groups:
        out += [f"### {g['label']} — {g['room']}", ""]
        if g.get("note"):
            out += [f"_{g['note']}_", ""]
        out += ["| Location | Product | Finish | Thk | Size | Product No |",
                "|---|---|---|---|---|---|"]
        for n, f, th, no, _cat, loc, sz, _fmt in g["rows"]:
            out.append(f"| {loc} | {n} | {f} | {th} | {sz or g['size']} | {no} |")
        out.append("")
    return "\n".join(out)


def main():
    parts = []
    for sid in ORDER:
        wb = openpyxl.load_workbook(SRC / BOOKS[sid], data_only=True)
        parts.append(section(sid, BUILDERS[sid](wb)))

    block = (START + "\n"
             "<!-- Regenerate with: python3 tools/build_showroom_docs.py -->\n\n"
             + "\n\n---\n\n".join(parts) + "\n\n" + END)

    text = DOC.read_text(encoding="utf-8")
    if START in text and END in text:
        head = text.split(START, 1)[0]
        tail = text.split(END, 1)[1]
        text = head + block + tail
    else:
        text = text.rstrip() + "\n\n---\n\n" + block + "\n"
    DOC.write_text(text, encoding="utf-8")
    print(f"wrote {DOC} — {sum(len(p) for p in parts)} chars of generated tables")


if __name__ == "__main__":
    main()
