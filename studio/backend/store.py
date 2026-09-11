from pathlib import Path
from datetime import datetime,timezone
from contextlib import contextmanager
import sqlite3,json,os
ROOT=Path(__file__).resolve().parents[1]
DEFAULT_DB=ROOT/'data/showroom.sqlite'
def now():return datetime.now(timezone.utc).isoformat(timespec='seconds')
class Connection(sqlite3.Connection):
    def __exit__(self,*args):
        try:return super().__exit__(*args)
        finally:self.close()
def connect(path=None):
    p=Path(path or os.environ.get('STUDIO_DB',DEFAULT_DB));p.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(p,timeout=15,factory=Connection);c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON');c.execute('PRAGMA busy_timeout=15000');return c
def rows(c,sql,args=()):return [dict(r)for r in c.execute(sql,args)]
def revision(c):return int(c.execute("SELECT value FROM meta WHERE key='revision'").fetchone()[0])
def log(c,actor,action,entity,details):c.execute('INSERT INTO events(created_at,actor,action,entity_id,details_json) VALUES(?,?,?,?,?)',(now(),actor,action,entity,json.dumps(details)))
def bump(c):c.execute("UPDATE meta SET value=CAST(value AS INTEGER)+1 WHERE key='revision'");return revision(c)
@contextmanager
def transaction(c,expected=None):
    if expected is None:raise ValueError('A base revision is required for a source change.')
    c.execute('BEGIN IMMEDIATE')
    try:
        if expected is not None and revision(c)!=int(expected):raise ValueError('The source changed. Refresh and review the latest revision before saving.')
        yield c;c.commit()
    except Exception:c.rollback();raise
