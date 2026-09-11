"""Preserve embedded workbook images with sheet/cell anchors; no image inference."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import xml.etree.ElementTree as ET
import json, posixpath, hashlib
root=Path(__file__).resolve().parents[1]
source=root.parent/'products '/'Assortment confirmation list with names 260618_1.xlsx'
out=root/'output/assortment';(out/'media').mkdir(exist_ok=True)
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','xdr':'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
def col(n):
    s=''
    while n:n,k=divmod(n-1,26);s=chr(65+k)+s
    return s
with ZipFile(source) as z:
    def rels(file):
        p=posixpath.join(posixpath.dirname(file),'_rels',posixpath.basename(file)+'.rels')
        if p not in z.namelist():return {}
        return {r.attrib['Id']:posixpath.normpath(posixpath.join(posixpath.dirname(file),r.attrib['Target'])).lstrip('/') for r in ET.fromstring(z.read(p)) if r.attrib.get('TargetMode')!='External'}
    media=[]
    for name in z.namelist():
        if not name.startswith('xl/media/'):continue
        data=z.read(name);dest=out/'media'/posixpath.basename(name);dest.write_bytes(data)
        media.append({'file':'media/'+dest.name,'workbook_part':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    anchors=[];wr=rels('xl/workbook.xml')
    for s in ET.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet',ns):
        part=wr[s.attrib['{'+ns['r']+'}id']];sr=rels(part)
        for d in ET.fromstring(z.read(part)).findall('s:drawing',ns):
            drawing=sr[d.attrib['{'+ns['r']+'}id']];dr=rels(drawing)
            for anchor in ET.fromstring(z.read(drawing)):
                start=anchor.find('xdr:from',ns)
                for blip in anchor.findall('.//a:blip',ns):
                    target=dr.get(blip.attrib.get('{'+ns['r']+'}embed'))
                    if not target:continue
                    rn=int(start.find('xdr:row',ns).text)+1 if start is not None else None
                    cn=int(start.find('xdr:col',ns).text)+1 if start is not None else None
                    anchors.append({'sheet':s.attrib['name'],'cell':f'{col(cn)}{rn}' if rn else None,'row':rn,'column':cn,'media':'media/'+posixpath.basename(target),'association':'Drawing anchor only; product identity requires review.'})
    (out/'media_index.json').write_text(json.dumps({'source':source.name,'media':media,'anchors':anchors},indent=2))
print(f'Preserved {len(media)} embedded image files with {len(anchors)} sheet/cell anchors.')
