import json, os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
import jana_db as jd


class UjianSesiStor(unittest.TestCase):
    """Tarikh data harian/status: sandaran daripada stor harga apabila status_harian.json tiada (mod bayang)."""

    def tulis(self, d, isi):
        p = os.path.join(d, 'status.json')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(isi if isinstance(isi, str) else json.dumps(isi))
        return p

    def test_format_iso(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(jd.sesi_stor(self.tulis(d, {'terkini': {'sesi': 20261016}})), '2026-10-16')
            self.assertEqual(jd.sesi_stor(self.tulis(d, {'terkini': {'sesi': '20261016'}})), '2026-10-16')

    def test_tiada_atau_rosak(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(jd.sesi_stor(os.path.join(d, 'tiada.json')), '')
            self.assertEqual(jd.sesi_stor(self.tulis(d, '{rosak')), '')
            self.assertEqual(jd.sesi_stor(self.tulis(d, {'terkini': {}})), '')
            self.assertEqual(jd.sesi_stor(self.tulis(d, {'terkini': {'sesi': '2026-10-16'}})), '')
            self.assertEqual(jd.sesi_stor(self.tulis(d, [])), '')


if __name__ == '__main__':
    unittest.main()
