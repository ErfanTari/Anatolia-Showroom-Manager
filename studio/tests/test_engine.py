"""Behavioral checks against isolated copies of the authoritative pilot data."""
import unittest,sys,tempfile,sqlite3,json,io,csv
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'backend'))
from store import connect,DEFAULT_DB,revision
import engine

class DomainTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.c=connect(Path(self.tmp.name)/'test.sqlite')
        with connect(DEFAULT_DB)as source:source.backup(self.c)
    def tearDown(self):self.c.close();self.tmp.cleanup()
    def s(self):return engine.state(self.c)
    def make(self,**kw):return engine.create_scenario(self.c,{'mode':'new_product','product_id':'tuscano-burgundy','base_revision':revision(self.c),**kw})
    def scenario(self,id):return next(x for x in self.s()['scenarios']if x['id']==id)
    def ready(self):
        s=self.s();ch=engine.plan(s,'new_product','tuscano-burgundy')[0];vid=ch['variant_id'];v=next(x for x in s['variants']if x['id']==vid)
        self.c.execute("UPDATE products SET lifecycle='active' WHERE id=?",(v['product_id'],))
        self.c.execute("UPDATE variants SET sku='TEST-NEW-SKU',lifecycle='active',availability='available',thickness_mm=12 WHERE id=?",(vid,))
        self.c.execute("UPDATE rules SET status='confirmed' WHERE kind='format'");self.c.commit()
        return self.make(),ch
    def test_source_has_all_slots_and_alias(self):
        s=self.s();self.assertEqual(len(s['slots']),194);self.assertEqual(len(s['placements']),194)
        p=next(p for p in s['products']if p['id']=='tuscano-burgundy');self.assertIn('Tuscano Rosso',p['aliases']);self.assertTrue(p['hit'])
    def test_planner_deterministic_and_broadens_coverage(self):
        s=self.s();a=engine.plan(s);b=engine.plan(s);self.assertEqual(a,b)
        after=engine.evaluate(s,a);self.assertGreater(after['summary']['unique_designs'],s['review']['summary']['unique_designs'])
        slots={x['id']:x for x in s['slots']}
        for ch in a:self.assertFalse(slots[ch['slot_id']]['locked']);self.assertFalse(slots[ch['slot_id']]['intentional_repeat'])
    def test_plans_do_not_rewrite_installed_data(self):
        before=self.s()['placements'];self.make();self.assertEqual(self.s()['placements'],before)
    def test_lifecycle_blocks_product_and_variant(self):
        s=self.s();ch=engine.plan(s,'new_product','tuscano-burgundy')[0]
        next(v for v in s['variants']if v['id']==ch['variant_id'])['lifecycle']='discontinued'
        with self.assertRaisesRegex(ValueError,'discontinued'):engine.validate_changes(s,[ch])
    def test_format_and_locked_slots_block(self):
        s=self.s();ch=engine.plan(s,'new_product','tuscano-burgundy')[0];ch['slot_id']='APS-R3-FLOOR';ch['from_variant_id']=next(a for a in s['placements']if a['slot_id']==ch['slot_id'])['variant_id']
        with self.assertRaisesRegex(ValueError,'protected'):engine.validate_changes(s,[ch])
    def test_release_exposes_missing_data(self):
        id=self.make()
        with self.assertRaisesRegex(ValueError,'Released SKU'):engine.release(self.c,id,revision(self.c),'merch')
        self.assertEqual(self.scenario(id)['status'],'draft')
    def test_agent_cannot_release(self):
        id=self.make()
        with self.assertRaises(PermissionError):engine.release(self.c,id,revision(self.c),'agent')
    def test_full_workflow_changes_observed_only_on_verification(self):
        id,ch=self.ready();engine.release(self.c,id,revision(self.c),'merch')
        t=next(t for t in self.s()['tasks']if t['scenario_id']==id)
        for stage in ['ordered','prepared','installed']:
            engine.update_task(self.c,t['id'],{'stage':stage,'evidence':'TEST evidence '+stage},revision(self.c),'manager')
            actual=next(a for a in self.s()['placements']if a['slot_id']==ch['slot_id']);self.assertEqual(actual['variant_id'],ch['from_variant_id'])
        engine.update_task(self.c,t['id'],{'stage':'verified','evidence':'TEST photo verification','disposition':'Removed slab stored in TEST bay'},revision(self.c),'manager')
        actual=next(a for a in self.s()['placements']if a['slot_id']==ch['slot_id']);self.assertEqual(actual['variant_id'],ch['variant_id'])
        self.assertEqual(self.scenario(id)['status'],'completed')
        r=revision(self.c);engine.update_task(self.c,t['id'],{'stage':'verified'},r,'manager');self.assertEqual(revision(self.c),r)
    def test_no_skipping_evidence_or_double_release(self):
        id,ch=self.ready();engine.release(self.c,id,revision(self.c),'merch');t=next(t for t in self.s()['tasks']if t['scenario_id']==id)
        with self.assertRaises(ValueError):engine.update_task(self.c,t['id'],{'stage':'verified'},revision(self.c),'manager')
        with self.assertRaises(ValueError):engine.release(self.c,id,revision(self.c),'merch')
    def test_stale_source_rejects_writes(self):
        r=revision(self.c);engine.edit(self.c,'products',[{'id':'oro-noir','notes':'TEST'}],r,'merch')
        with self.assertRaises(ValueError):engine.create_scenario(self.c,{'mode':'refresh','base_revision':r})
    def test_csv_is_atomic_and_validates_ids(self):
        r=revision(self.c);before=next(p for p in self.s()['products']if p['id']=='oro-noir')['notes']
        with self.assertRaises(ValueError):engine.import_csv(self.c,'products',f'base_revision,id,notes\n{r},oro-noir,CHANGED\n{r},NOT-REAL,bad\n',dry_run=False)
        self.assertEqual(next(p for p in self.s()['products']if p['id']=='oro-noir')['notes'],before);self.assertEqual(revision(self.c),r)
    def test_dry_run_does_not_write(self):
        r=revision(self.c);engine.import_csv(self.c,'products',f'base_revision,id,notes\n{r},oro-noir,CHANGED\n')
        self.assertNotEqual(next(p for p in self.s()['products']if p['id']=='oro-noir')['notes'],'CHANGED');self.assertEqual(revision(self.c),r)
    def test_csv_placement_creates_draft(self):
        s=self.s();ch=engine.plan(s,'new_product','tuscano-burgundy')[0]
        text=f"base_revision,slot_id,variant_id,face_id\n{revision(self.c)},{ch['slot_id']},{ch['variant_id']},{ch['face_id']}\n"
        result=engine.import_csv(self.c,'placements',text,dry_run=False);self.assertEqual(self.scenario(result['scenario_id'])['status'],'draft')
        self.assertEqual(self.s()['placements'],s['placements'])
    def test_face_identity_enforced(self):
        s=self.s();ch=engine.plan(s,'new_product','tuscano-burgundy')[0];ch['face_id']=next(f['id']for f in s['faces']if f['product_id']=='oro-noir')
        with self.assertRaisesRegex(ValueError,'Face'):engine.validate_changes(s,[ch])
    def test_geometry_bounds_route_collision_and_rotation(self):
        s=self.s();f=next(f for f in s['fixtures']if f['relocatable'])
        self.assertTrue(engine.geometry_errors(s,f,{'x_mm':-1000,'z_mm':6000,'yaw_deg':0}))
        self.assertTrue(engine.geometry_errors(s,f,{'x_mm':14500,'z_mm':6000,'yaw_deg':90}))
        other=next(x for x in s['fixtures']if x['relocatable']and x['id']!=f['id'])
        self.assertTrue(engine.geometry_errors(s,f,{k:other[k]for k in ['x_mm','z_mm','yaw_deg']}))
        self.assertTrue(engine.overlap(engine.rect(f),engine.rect(f)))
    def test_manager_observation_has_evidence_and_audit(self):
        a=self.s()['placements'][0]
        with self.assertRaises(ValueError):engine.observe(self.c,{'base_revision':revision(self.c),'slot_id':a['slot_id'],'variant_id':a['variant_id'],'evidence':''},'manager')
        engine.observe(self.c,{'base_revision':revision(self.c),'slot_id':a['slot_id'],'variant_id':a['variant_id'],'evidence':'TEST onsite photo'},'manager')
        self.assertEqual(self.s()['events'][0]['action'],'observe')
    def test_mcp_role_and_tool_contract(self):
        import mcp_server
        init=mcp_server.dispatch({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-11-25'}})
        self.assertEqual(init['result']['protocolVersion'],'2025-11-25')
        self.assertEqual(len(mcp_server.dispatch({'id':2,'method':'tools/list'})['result']['tools']),3)
        self.assertFalse(any('release'in t['name']for t in mcp_server.TOOLS))

if __name__=='__main__':unittest.main()
