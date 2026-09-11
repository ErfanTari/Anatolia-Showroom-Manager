"""Verify source/snapshot consistency and local assets before publishing."""
from pathlib import Path
import sys,json,hashlib,csv,subprocess
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'backend'))
from store import connect,revision
import engine

def main():
    with connect()as c:
        assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        assert not c.execute('PRAGMA foreign_key_check').fetchall()
        current=engine.state(c);snapshot=json.loads((ROOT/'web/data/state.json').read_text())
        assert snapshot['meta']['revision']==revision(c)
        assert snapshot['placements']==current['placements'],'Export the current placements before publishing.'
        assert snapshot['fixtures']==current['fixtures'],'Export current fixture positions.'
        assert snapshot['review']==current['review'],'Export current review rules.'
    assert len(snapshot['slots'])==194
    for face in snapshot['faces']:
        path=ROOT/'web'/face['data']['path'];assert path.is_file(),str(path)
        assert hashlib.sha256(path.read_bytes()).hexdigest()==face['data']['sha256'],str(path)
    for table in engine.EDITABLE:
        with (ROOT/f'data/exports/{table}.csv').open(encoding='utf-8-sig',newline='')as f:
            data=list(csv.DictReader(f))
        assert len(data)==len(snapshot[table]),table
        assert all(int(r['base_revision'])==snapshot['meta']['revision']for r in data),table
    for variant in snapshot['variants']:
        texture=variant['preview'].get('texture')
        if texture:assert (ROOT/'web'/texture).resolve().is_file(),texture
    tracked=set(subprocess.check_output(['git','ls-files','-z'],cwd=ROOT.parent).decode().split('\0'))
    for face in snapshot['faces']:assert 'studio/web/'+face['data']['path']in tracked,'Stage the face asset.'
    print(json.dumps({'revision':snapshot['meta']['revision'],'slots':len(snapshot['slots']),'face_hashes_verified':len(snapshot['faces']),'csv_tables_verified':len(engine.EDITABLE),'sqlite':'integrity and foreign keys passed'}))
if __name__=='__main__':main()
