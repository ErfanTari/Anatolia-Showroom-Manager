#!/usr/bin/env python3
"""Generate data/showroom-<id>.js from the four new-showroom BOM workbooks.

Same role for Manisa / Ekinox / Ankara / Turkuaz that the hand-built
`showroom-data.js` plays for APS: the BOM spreadsheet is the single source of
truth, this script is the only thing that reads it, and the dashboard only ever
sees the generated JS.

    python3 tools/build_showroom_data.py            # write data/showroom-*.js
    python3 tools/build_showroom_data.py --check    # verify counts, write nothing

Each generated file sets

    window.SHOWROOM_DATA['<id>'] = { groups: [...] }

where a group is

    { key, label, fmt, room, size, numbered, rows: [row, ...] }

and a row is the 8-tuple

    [name, finish, thickness, productNo, colourCategory, location, size, fmt]

`size` and `fmt` are null when the group default applies — mixed groups (a
bathroom's walls + vanity, a subsize board's four tile formats) carry them
per row. The shape deliberately mirrors the positional arrays in
`showroom-data.js` so `products` in the dashboard can walk both the same way.
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

try:
    import openpyxl
except ImportError:  # pragma: no cover
    sys.exit("openpyxl is required:  pip install openpyxl")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "two new showrooms"
OUT = ROOT / "data"

BOOKS = {
    "manisa": "Manisa_Öz Yapı_BOM_20260716.xlsx",
    "ekinox": "EkinoxBursa_BOM_wSecondRoundSlabs_20250826 (1).xlsx",
    "ankara": "Ankara Ark Yapı _20260715_BOM -_ 1.xlsx",
    "turkuaz": "Turkuaz_İstShowroom_BOM_20260405.xlsx",
}

# ---------------------------------------------------------------- normalising

def txt(v):
    """Cell -> collapsed single-line string ('' for empty)."""
    if v is None:
        return ""
    s = unicodedata.normalize("NFC", str(v))
    s = s.replace("\xa0", " ").replace("\n", " ")
    return re.sub(r"\s+", " ", s).strip()


def size(v):
    """'120x 280 cm' / '60 X 120 cm' / '162 x 322' -> '120 × 280 cm'."""
    s = txt(v)
    if not s:
        return ""
    s = re.sub(r"\s*[xX×]\s*", " × ", s)
    s = re.sub(r"(\d)\s*cm", r"\1 cm", s)
    if not re.search(r"(cm|mm|Ø|in)\b", s):
        s += " cm"
    return re.sub(r"\s+", " ", s).strip()


def thick(v):
    """'6mm' / ' 9 mm' -> '6 mm'."""
    s = txt(v)
    m = re.search(r"([\d.]+)\s*mm", s, re.I)
    return f"{m.group(1)} mm" if m else s


def prodno(v):
    """Strip the '*' the Ankara/Turkuaz sheets append to substituted SKUs."""
    return txt(v).rstrip("*").strip()


def name(v):
    return txt(v)


# Colour families, most specific first — the tail of each pattern list is what
# the dashboard's flatCol()/colourFam() already understand. Verified against
# every product name in showroom-data.js (see --check).
FAMILIES = [
    # 'calacatta oro' before the noir rule so Calacatta Oro doesn't read as Oro Noir.
    ("gold",       r"calacatta oro|taj mahal|french vanil|forge eleganza|vanilla"),
    ("noir",       r"noir|nero|marquina|sahara|panda"),
    ("onyx",       r"onyx"),
    ("terrazzo",   r"publica|terrazzo|ceppo"),
    ("travertine", r"travertino|travertine|gemma bronze|bronze"),
    ("green",      r"verdi alpi|verde|jade|foresta"),
    ("grey",       r"serena|monoforma|lithoform|colorado|grigio|montagna grey|pietra imperiale|"
                   r"atlantic ocean|silhouette|storm|shale|flint|pewter|dunes|twilight|quarzo|imperiale"),
    ("calacatta",  r"calacatta|bianco|statuario|arabescato|carrara|cristallo|super white|marina white|"
                   r"fusion white|crystal|macchia|picasso|ariel|viola|corchia|borghini|cremo|stratura|"
                   r"dior|gioia|white|blanco"),
]


def family(product_name):
    s = product_name.lower()
    for fam, pattern in FAMILIES:
        if re.search(pattern, s):
            return fam
    return "grey"


def rows_of(ws, first=2):
    """Yield (row_index, dict) for every non-empty data row."""
    header = {txt(ws.cell(1, c).value): c for c in range(1, ws.max_column + 1)}
    for r in range(first, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, ws.max_column + 1)]
        if all(v is None or txt(v) == "" for v in vals):
            continue
        yield r, header


def cell(ws, r, header, *names):
    for n in names:
        if n in header:
            v = ws.cell(r, header[n]).value
            if v is not None:
                return v
    return None


def cancelled(ws, r, header):
    """True only for an explicit CANCEL in the Notes column.

    Deliberately does NOT treat 'N/A' as a cancellation: in the Manisa sheet
    'N/A' appears in the *Pre Cut* column (that panel needs no pre-cut), and
    dropping those rows would punch holes in the 01–51 panel run.
    """
    note = txt(cell(ws, r, header, "Notes"))
    return "CANCEL" in note.upper()


# ------------------------------------------------------------------- assembly

def group(key, label, fmt, room, size_default, rows, numbered=False, note=None):
    g = {
        "key": key,
        "label": label,
        "fmt": fmt,
        "room": room,
        "size": size_default,
        "numbered": numbered,
        "rows": rows,
    }
    if note:
        g["note"] = note
    return g


def row(n, f, th, no, loc, sz=None, fmt=None):
    # An empty size must stay None so the group default applies — a few BOM rows
    # (Ekinox's kitchen counters) leave the Size column blank.
    return [name(n), txt(f), thick(th), prodno(no), family(name(n)),
            txt(loc), sz or None, fmt]


# ------------------------------------------------------------------- showrooms

def build_manisa(wb):
    ws = wb["Manisa_ÖZ YAPI 2025"]
    hdr = {txt(ws.cell(1, c).value): c for c in range(1, ws.max_column + 1)}

    def g(r, *names):
        return cell(ws, r, hdr, *names)

    def mk(r, loc=None, sz=None, fmt=None):
        return row(g(r, "Colour"), g(r, "Finish"), g(r, "Thickness"),
                   g(r, "Product No"), loc if loc is not None else txt(g(r, "Area")),
                   sz or size(g(r, "Size")), fmt)

    slidingA, slidingB, library = [], [], []
    for r in range(24, 54):
        if cancelled(ws, r, hdr):
            continue
        area = txt(g(r, "Area"))
        sz = size(g(r, "Size"))
        # Panels A-2 / B-2 carry four sub-size tiles on one MDF board; the BOM
        # leaves the Area blank on one of the B-2 continuation rows.
        if not area:
            area = "Panel B-2"
        target = slidingA if area.startswith("Panel A") else slidingB
        loc = area if sz.startswith("120 × 280") else f"{area} · {sz}"
        target.append(mk(r, loc=loc, sz=sz))

    for r in range(54, 105):
        if cancelled(ws, r, hdr):
            continue
        library.append(mk(r, loc=txt(g(r, "Area"))))

    # Architecture: everything above the display systems, split by BOM Location.
    def arch(rng, fmts):
        out = []
        for r in rng:
            if cancelled(ws, r, hdr):
                continue
            out.append(mk(r, loc=txt(g(r, "Area")), fmt=fmts.get(r, "On Wall")))
        return out

    return [
        group("slidingA", "Sliding Panel A", "Sliding Panel", "Sliding Bank A",
              "120 × 280 cm", slidingA, numbered=True),
        group("slidingB", "Sliding Panel B", "Sliding Panel", "Sliding Bank B",
              "120 × 280 cm", slidingB, numbered=True),
        group("library", "Product Library", "Pre-fixed Panel", "Product Library",
              "60 × 280 cm", library, numbered=True,
              note="60 × 280 cm Ürün Kütüphanesi · capacity 51"),
        group("entry", "Entrance", "On Wall", "Entrance", "120 × 280 cm",
              arch(range(3, 9), {5: "In Furniture", 6: "In Furniture", 8: "In Furniture"})),
        group("kitchen", "Kitchen & Sales", "On Wall", "Kitchen & Sales", "120 × 280 cm",
              arch(range(9, 13), {11: "In Furniture", 12: "In Furniture"})),
        group("libraryWall", "Library Wall", "On Wall", "Library Wall", "120 × 280 cm",
              arch(range(13, 15), {})),
        group("fireplace", "Fireplace", "On Wall", "Fireplace", "120 × 280 cm",
              arch(range(15, 18), {15: "In Furniture", 16: "In Furniture"})),
        group("bath", "Bathroom", "On Wall", "Bathroom", "120 × 280 cm",
              arch(range(18, 24), {18: "In Furniture"})),
        group("floors", "Floors", "Floor", "Main Floors", "120 × 120 cm",
              arch(range(2, 3), {2: "Floor"})),
    ]


def build_ekinox(wb):
    ws = wb["Ekinox Bursa 2025"]
    hdr = {txt(ws.cell(1, c).value): c for c in range(1, ws.max_column + 1)}

    def g(r, *names):
        return cell(ws, r, hdr, *names)

    def mk(r, loc=None, sz=None, fmt=None):
        return row(g(r, "Colour"), g(r, "Finish"), g(r, "Thickness"),
                   g(r, "Product No"), loc if loc is not None else txt(g(r, "Area")),
                   sz or size(g(r, "Size")), fmt)

    panelsA, panelsB, library = [], [], []
    for r in range(16, 42):
        if cancelled(ws, r, hdr):
            continue
        area = txt(g(r, "Area"))
        sz = size(g(r, "Size"))
        loc = area if sz.startswith("120 × 280") else f"{area} · {sz}"
        (panelsA if area.startswith("Panel A") else panelsB).append(mk(r, loc=loc, sz=sz))

    for r in range(42, 74):
        if cancelled(ws, r, hdr):          # rows 51 & 72 are marked CANCEL
            continue
        library.append(mk(r, loc=txt(g(r, "Area"))))
    library.sort(key=lambda x: int(re.search(r"(\d+)", x[5]).group(1)))

    def arch(rng, fmts, default="On Wall"):
        return [mk(r, loc=txt(g(r, "Area")), fmt=fmts.get(r, default))
                for r in rng if not cancelled(ws, r, hdr)]

    return [
        group("panelsA", "Display Panel A", "Sliding Panel", "Display Bank A",
              "120 × 280 cm", panelsA, numbered=True),
        group("panelsB", "Display Panel B", "Sliding Panel", "Display Bank B",
              "120 × 280 cm", panelsB, numbered=True),
        group("library", "Product Library", "Pre-fixed Panel", "Product Library",
              "60 × 280 cm", library, numbered=True,
              note="60 × 280 cm Ürün Kütüphanesi · 30 panels after 2 cancellations"),
        group("kitchen", "Kitchen", "In Furniture", "Kitchen", "162 × 322 cm",
              arch(range(3, 5), {}, default="In Furniture")),
        group("meeting", "Meeting Area", "In Furniture", "Meeting Area", "125 × 280 cm",
              arch(range(5, 8), {7: "On Wall"}, default="In Furniture")),
        group("bath", "Bathroom", "On Wall", "Bathroom", "160 × 320 cm",
              arch(range(8, 11), {})),
        group("column", "Column Cladding", "On Wall", "Column", "120 × 280 cm",
              arch(range(11, 13), {})),
        group("cubes", "Decorative Cubes", "In Furniture", "Decorative Cubes",
              "162 × 322 cm", arch(range(13, 16), {}, default="In Furniture")),
        group("floors", "Floors", "Floor", "Main Floors", "120 × 120 cm",
              arch(range(2, 3), {2: "Floor"})),
    ]


def build_ankara(wb):
    ws = wb["Ark Yapı_Banyo Marka Ankara"]
    hdr = {txt(ws.cell(1, c).value): c for c in range(1, ws.max_column + 1)}

    def g(r, *names):
        return cell(ws, r, hdr, *names)

    def mk(r, loc=None, sz=None, fmt=None):
        return row(g(r, "Colour"), g(r, "Finish"), g(r, "Thickness"),
                   g(r, "Product No"), loc if loc is not None else txt(g(r, "Location")),
                   sz or size(g(r, "Size")), fmt)

    def span(a, b, loc=None, fmt=None):
        return [mk(r, loc=loc(r) if callable(loc) else loc, fmt=fmt) for r in range(a, b)]

    def area(r):
        return txt(g(r, "Area"))

    def code_area(r):
        return f"{txt(g(r, 'Location'))} · {area(r)}"

    # The Aeterna sample tower is a fixture line (9902-…) with no colour/size,
    # so it is described rather than parsed.
    tower = [row("Aeterna Finishes Sample Tower", "Polished · Honed · Satin", "6 mm",
                 "9902-2477-0", "75 × 30 × 30 cm A-shape chips", "30 × 30 cm", "Tower")]

    return [
        group("sliding160", "Sliding Panels", "Sliding Panel", "Sliding Bank 160",
              "160 × 320 cm", span(28, 40, loc=lambda r: txt(g(r, "Location"))), numbered=True),
        group("sliding120", "Mini Slabs", "Sliding Panel", "Sliding Bank 120",
              "120 × 280 cm", span(40, 52, loc=lambda r: txt(g(r, "Location"))), numbered=True),
        group("waterfall", "Waterfall Slabs", "Waterfall", "Waterfall",
              "60 × 280 cm", span(52, 58, loc=lambda r: txt(g(r, "Location"))), numbered=True),
        group("rotating", "Rotating Tile Displays", "Rotating Panel", "Rotating Units",
              "—", span(58, 61, loc=lambda r: f"{txt(g(r,'Location'))} · {size(g(r,'Size'))}"),
              numbered=True),
        group("tower", "Sample Tower", "Tower", "Sample Tower", "30 × 30 cm", tower),
        group("fireplace", "Fireplace", "On Wall", "Fireplace", "—",
              [mk(6, loc=code_area(6), fmt="In Furniture"), mk(7, loc=code_area(7))]),
        group("meeting", "Meeting Area", "In Furniture", "Meeting Area", "—",
              [mk(8, loc=code_area(8), fmt="In Furniture"),
               mk(9, loc=code_area(9), fmt="On Wall"),
               mk(10, loc=code_area(10), fmt="In Furniture")]),
        group("bath", "Bathroom", "On Wall", "Bathroom", "—",
              [mk(11, loc=code_area(11)), mk(12, loc=code_area(12)),
               mk(13, loc=code_area(13), fmt="In Furniture")]),
        group("design", "Design Area", "On Wall", "Design Area", "—",
              [mk(14, loc=code_area(14), fmt="In Furniture"), mk(15, loc=code_area(15))]),
        group("stairs", "Stair Wall & Treads", "On Wall", "Stairs", "120 × 280 cm",
              [mk(16, loc=code_area(16))]),
        group("cubes", "Decorative Cubes", "In Furniture", "Decorative Cubes",
              "162 × 322 cm", span(17, 28, loc=area, fmt="In Furniture")),
        group("floors", "Floors", "Floor", "Main Floors", "120 × 120 cm",
              span(2, 6, loc=code_area, fmt="Floor")),
    ]


def build_turkuaz(wb):
    ws = wb["Turkuaz_BOM"]
    hdr = {txt(ws.cell(1, c).value): c for c in range(1, ws.max_column + 1)}

    def g(r, *names):
        return cell(ws, r, hdr, *names)

    def mk(r, loc=None, sz=None, fmt=None):
        return row(g(r, "Colour"), g(r, "Finish"), g(r, "Thickness"),
                   g(r, "Product No"), loc if loc is not None else txt(g(r, "Area")),
                   sz or size(g(r, "Size")), fmt)

    slabs, minis, boards = [], [], []
    for r in range(2, ws.max_row + 1):
        area = txt(g(r, "Area"))
        if not area:
            continue
        sz = size(g(r, "Size"))
        if area.startswith("Slab"):
            slabs.append(mk(r, loc=area))
        elif area.startswith("Mini Slab"):
            minis.append(mk(r, loc=area))
        elif area.lower().startswith("subsize board"):
            boards.append((r, mk(r, loc=f"{area} · {sz}", sz=sz)))

    def num(label):
        m = re.search(r"(\d+)", label)
        return int(m.group(1)) if m else 0

    # Mini slabs and boards interleave in the sheet (positions 1–36 of one unit);
    # group them by number but keep BOM order for a board's own sizes.
    minis.sort(key=lambda x: num(x[5]))
    boards.sort(key=lambda rr: (num(rr[1][5]), rr[0]))
    boards = [b for _, b in boards]

    # Sheet 2 assigns one extra 120 × 280 slab to eight of the subsize boards
    # (its Descripcion column carries the full product name).
    extras = []
    ws2 = wb.worksheets[1]
    for r in range(1, ws2.max_row + 1):
        board = txt(ws2.cell(r, 2).value)
        sku = txt(ws2.cell(r, 3).value)
        desc = txt(ws2.cell(r, 4).value)
        if not sku or not desc:
            continue
        m = re.search(r"in\s+(.+?)\s+(Polished|Honed|Silk|Satin|Vintage|Grained|Patinated|Organic Matte)",
                      desc)
        pname = m.group(1) if m else desc
        finish = m.group(2) if m else ""
        loc = board.title() if board else txt(ws2.cell(r, 5).value) or "Reserve"
        extras.append(row(pname, finish, "6 mm", sku, loc, "120 × 280 cm", "Sliding Panel"))

    return [
        group("slabs", "Full Slabs", "Sliding Panel", "Sliding Unit · Slabs",
              "160 × 320 cm", slabs, numbered=True),
        group("minis", "Mini Slabs", "Sliding Panel", "Sliding Unit · Mini Slabs",
              "120 × 280 cm", minis, numbered=True),
        group("boards", "Subsize Boards", "On Wall", "Subsize Boards", "—", boards,
              note="Ten boards, each carrying that colour in four to five sub-sizes"),
        group("extras", "Extra Mini Slabs", "Sliding Panel", "Extra Mini Slabs",
              "120 × 280 cm", extras,
              note="Sheet 'Ekstra 8 Ürün 120x 280' — one added slab per subsize board"),
    ]


BUILDERS = {
    "manisa": build_manisa,
    "ekinox": build_ekinox,
    "ankara": build_ankara,
    "turkuaz": build_turkuaz,
}

# Counts asserted after every build — these come from reading the BOMs and the
# drawings, so a silent change in a workbook shows up as a failure here.
EXPECTED = {
    # 15 = 11 full 120 × 280 panels + the 4 sub-size tiles on the A-2 / B-2 board.
    "manisa": {"slidingA": 15, "slidingB": 15, "library": 51, "floors": 1},
    "ekinox": {"panelsA": 16, "panelsB": 10, "library": 30, "floors": 1},
    "ankara": {"sliding160": 12, "sliding120": 12, "waterfall": 6,
               "rotating": 3, "cubes": 11, "floors": 4},
    "turkuaz": {"slabs": 12, "minis": 26, "boards": 44, "extras": 9},
}

HEADER = ("// Auto-generated by tools/build_showroom_data.py from\n"
          "//   two new showrooms/{book}\n"
          "// Do not hand-edit — re-run the script instead. See 'Showroom Data.md'.\n")


def emit(sid, groups):
    payload = {"groups": groups}
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return (HEADER.format(book=BOOKS[sid])
            + "window.SHOWROOM_DATA = window.SHOWROOM_DATA || {};\n"
            + f"window.SHOWROOM_DATA[{json.dumps(sid)}] = {body};\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify counts and print a summary without writing")
    ap.add_argument("--only", help="build a single showroom id")
    args = ap.parse_args()

    failures = []
    all_groups = {}
    for sid, book in BOOKS.items():
        if args.only and sid != args.only:
            continue
        path = SRC / book
        if not path.exists():
            failures.append(f"{sid}: missing workbook {path}")
            continue
        wb = openpyxl.load_workbook(path, data_only=True)
        groups = BUILDERS[sid](wb)
        counts = {g["key"]: len(g["rows"]) for g in groups}
        total = sum(counts.values())

        for key, want in EXPECTED[sid].items():
            got = counts.get(key)
            if got != want:
                failures.append(f"{sid}.{key}: expected {want} rows, got {got}")

        print(f"{sid:9s} {total:4d} surfaces  " +
              "  ".join(f"{k}={v}" for k, v in counts.items()))

        all_groups[sid] = groups
        if not args.check:
            OUT.mkdir(exist_ok=True)
            (OUT / f"showroom-{sid}.js").write_text(emit(sid, groups), encoding="utf-8")

    if failures:
        print("\nFAILED:", file=sys.stderr)
        for f in failures:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nok" + ("" if args.check else f" — wrote {OUT}/showroom-*.js"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
