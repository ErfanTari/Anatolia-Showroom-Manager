from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
root=Path(__file__).resolve().parents[1]/'output/assortment'
dest=root/'assortment-csv-pack.zip'
files=[p for p in root.rglob('*') if p.is_file() and p.suffix!='.zip' and p.name!='.DS_Store']
with ZipFile(dest,'w',ZIP_DEFLATED) as z:
    for p in sorted(files):z.write(p,p.relative_to(root))
print(f'{dest.name}: {len(files)} files, {dest.stat().st_size:,} bytes')
