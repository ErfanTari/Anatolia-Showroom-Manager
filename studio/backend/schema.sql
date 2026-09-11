PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS showrooms(id TEXT PRIMARY KEY,name TEXT NOT NULL,geometry_json TEXT NOT NULL,source_note TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS products(
 id TEXT PRIMARY KEY,name TEXT NOT NULL,family TEXT NOT NULL,positioning TEXT NOT NULL DEFAULT 'unknown' CHECK(positioning IN('prime','commercial','unknown')),
 hit INTEGER NOT NULL DEFAULT 0 CHECK(hit IN(0,1)),lifecycle TEXT NOT NULL DEFAULT 'unconfirmed' CHECK(lifecycle IN('active','unconfirmed','discontinued')),
 required INTEGER NOT NULL DEFAULT 0 CHECK(required IN(0,1)),color_group TEXT NOT NULL DEFAULT 'unconfirmed',color_rank REAL,priority_source TEXT NOT NULL,
 notes TEXT NOT NULL DEFAULT '',aliases_json TEXT NOT NULL DEFAULT '[]');
CREATE TABLE IF NOT EXISTS variants(
 id TEXT PRIMARY KEY,product_id TEXT NOT NULL REFERENCES products(id),sku TEXT UNIQUE,finish TEXT NOT NULL,width_mm INTEGER,height_mm INTEGER,thickness_mm REAL,
 lifecycle TEXT NOT NULL DEFAULT 'unconfirmed',availability TEXT NOT NULL DEFAULT 'unknown',source_json TEXT NOT NULL,preview_json TEXT NOT NULL,
 CHECK(width_mm IS NULL OR width_mm>0),CHECK(height_mm IS NULL OR height_mm>0));
CREATE TABLE IF NOT EXISTS faces(id TEXT PRIMARY KEY,product_id TEXT NOT NULL REFERENCES products(id),width_mm INTEGER NOT NULL,height_mm INTEGER NOT NULL,data_json TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS fixtures(id TEXT PRIMARY KEY,showroom_id TEXT NOT NULL REFERENCES showrooms(id),room INTEGER NOT NULL,type TEXT NOT NULL,x_mm REAL NOT NULL,z_mm REAL NOT NULL,yaw_deg REAL NOT NULL,width_mm REAL NOT NULL,height_mm REAL NOT NULL,depth_mm REAL NOT NULL,relocatable INTEGER NOT NULL DEFAULT 0,geometry_verified INTEGER NOT NULL DEFAULT 0,extra_json TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS slots(id TEXT PRIMARY KEY,showroom_id TEXT NOT NULL REFERENCES showrooms(id),fixture_id TEXT REFERENCES fixtures(id),room INTEGER NOT NULL,title TEXT NOT NULL,type TEXT NOT NULL,side TEXT,width_mm INTEGER,height_mm INTEGER,locked INTEGER NOT NULL DEFAULT 0,intentional_repeat INTEGER NOT NULL DEFAULT 0,visibility_tier TEXT NOT NULL CHECK(visibility_tier IN('prime','secondary','commercial')),visibility_score REAL NOT NULL,visibility_basis TEXT NOT NULL,sequence_group TEXT,sequence_rank INTEGER,source_json TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS placements(slot_id TEXT PRIMARY KEY REFERENCES slots(id),variant_id TEXT REFERENCES variants(id),face_id TEXT REFERENCES faces(id),state TEXT NOT NULL DEFAULT 'reported_installed',evidence TEXT NOT NULL,updated_at TEXT NOT NULL,revision INTEGER NOT NULL DEFAULT 1);
CREATE TABLE IF NOT EXISTS rules(id TEXT PRIMARY KEY,name TEXT NOT NULL,kind TEXT NOT NULL,strength TEXT NOT NULL CHECK(strength IN('hard','soft')),enabled INTEGER NOT NULL CHECK(enabled IN(0,1)),parameters_json TEXT NOT NULL,owner TEXT NOT NULL,status TEXT NOT NULL CHECK(status IN('draft','confirmed')),rationale TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS questions(id TEXT PRIMARY KEY,team TEXT NOT NULL,question TEXT NOT NULL,proposed_answer TEXT NOT NULL,answer TEXT NOT NULL DEFAULT '',status TEXT NOT NULL DEFAULT 'open',owner TEXT NOT NULL DEFAULT '',evidence TEXT NOT NULL DEFAULT '');
CREATE TABLE IF NOT EXISTS scenarios(id TEXT PRIMARY KEY,title TEXT NOT NULL,mode TEXT NOT NULL,base_revision INTEGER NOT NULL,status TEXT NOT NULL CHECK(status IN('draft','released','completed','superseded')),created_at TEXT NOT NULL,actor TEXT NOT NULL,changes_json TEXT NOT NULL,evaluation_json TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY,scenario_id TEXT REFERENCES scenarios(id),title TEXT NOT NULL,kind TEXT NOT NULL,owner TEXT NOT NULL,due_date TEXT,stage TEXT NOT NULL,slot_id TEXT REFERENCES slots(id),variant_id TEXT REFERENCES variants(id),requires_order INTEGER NOT NULL DEFAULT 0,evidence TEXT NOT NULL DEFAULT '',disposition TEXT NOT NULL DEFAULT '',dependencies_json TEXT NOT NULL DEFAULT '[]',details_json TEXT NOT NULL,updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT NOT NULL,actor TEXT NOT NULL,action TEXT NOT NULL,entity_id TEXT NOT NULL,details_json TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS placements_variant ON placements(variant_id);
CREATE INDEX IF NOT EXISTS slots_showroom ON slots(showroom_id);
CREATE INDEX IF NOT EXISTS tasks_scenario ON tasks(scenario_id);
