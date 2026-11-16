import json, tempfile, unittest
from pathlib import Path
from skills.audit.scripts.prepare_research_audit import prepare
from skills.audit.scripts.validate_research_audit import validate
from skills.audit.scripts.revision_impact import compare
SAMPLE="""# ABSTRAK

Penelitian inventaris.

# BAB I PENDAHULUAN

## 1.2 Rumusan Masalah
1. Bagaimana merancang sistem inventaris?
2. Bagaimana menguji kebutuhan sistem?

## 1.3 Tujuan Penelitian
1. Merancang sistem inventaris.

# BAB III METODOLOGI PENELITIAN

## 3.2 Teknik Analisis Data
Data dianalisis secara deskriptif.

# BAB V KESIMPULAN

1. Sistem inventaris berhasil dirancang.
"""
class Tests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.root=Path(self.t.name);self.src=self.root/'draft.md';self.src.write_text(SAMPLE,encoding='utf-8');self.ws=self.root/'ws';prepare(self.src,self.ws,'undergraduate','id')
 def tearDown(self):self.t.cleanup()
 def audit(self):
  checks={f'RC{i:02d}':{'status':'not_assessable','coverage':'limited','basis':'Belum dinilai','missing':'Reviewer'} for i in range(1,11)}
  checks['RC02']={'status':'found','coverage':'full','basis':'Pertanyaan dibandingkan dengan tujuan'}
  q='Bagaimana menguji kebutuhan sistem?'
  return {'summary':'Uji konsistensi pertanyaan dan tujuan.','checks':checks,'findings':[{'id':'F-01','check':'RC02','title':'Tujuan belum menjawab pertanyaan kedua','severity':'major','status':'confirmed','confidence':'high','location':{'line':1},'quote':q,'problem':'Pertanyaan kedua tidak memiliki tujuan yang dinyatakan.','impact':'Keterlacakan tujuan dan metode terganggu.','recommendation':'Tambahkan tujuan yang sesuai atau persempit pertanyaan berdasarkan desain sebenarnya.'}]}
 def test_prepare_maps_research_chain(self):
  m=json.loads((self.ws/'research_map.json').read_text());self.assertEqual(len(m['chain']['problem']),2);self.assertEqual(len(m['chain']['objective']),1)
 def test_machine_count_is_candidate(self):
  f=json.loads((self.ws/'machine_findings.json').read_text());self.assertTrue(any(x['status']=='candidate' for x in f))
 def test_workspace_collision(self):
  with self.assertRaises(Exception):prepare(self.src,self.ws,'undergraduate','id')
 def test_valid_quote_and_schema(self):
  err,fs=validate(self.ws,self.audit());self.assertEqual(err,[]);self.assertEqual(fs[0]['location']['line'],9)
 def test_invalid_quote_rejected(self):
  a=self.audit();a['findings'][0]['quote']='Kalimat ini tidak ada di sumber.';e,_=validate(self.ws,a);self.assertTrue(any('not found verbatim' in x for x in e))
 def test_critical_requires_high_confirmed(self):
  a=self.audit();a['findings'][0]['severity']='critical';a['findings'][0]['confidence']='medium';e,_=validate(self.ws,a);self.assertTrue(any('critical requires' in x for x in e))
 def test_found_requires_a_finding(self):
  a=self.audit();a['checks']['RC03']={'status':'found','coverage':'full','basis':'Checked'};e,_=validate(self.ws,a);self.assertTrue(any('found without valid finding' in x for x in e))
 def test_not_assessable_requires_missing(self):
  a=self.audit();a['checks']['RC04'].pop('missing');e,_=validate(self.ws,a);self.assertTrue(any('needs missing input' in x for x in e))
 def test_duplicate_ids_rejected(self):
  a=self.audit();a['findings'].append(dict(a['findings'][0]));e,_=validate(self.ws,a);self.assertTrue(any('duplicate ID' in x for x in e))
 def test_revision_impact_flags_possible_stale_value(self):
  old=['# BAB IV','Akurasi 95%.','# BAB V','Kesimpulan akurasi 95%.'];new=['# BAB IV','Akurasi 92%.','# BAB V','Kesimpulan akurasi 95%.'];_,_,c=compare(old,new);self.assertTrue(any(x[0]=='95%' for x in c))
if __name__=='__main__':unittest.main()
