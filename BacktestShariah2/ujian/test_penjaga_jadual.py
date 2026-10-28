import os, sys, unittest
from datetime import datetime, timedelta, timezone

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'standard'))
import penjaga_jadual as pj


def utc(*a):
    return datetime(*a, tzinfo=timezone.utc)


class TestPenjagaJadual(unittest.TestCase):
    def test_cetusan_hari_kerja(self):
        # Isnin 19 Okt 2026 hingga Sabtu 24 Okt: '40 13 * * 1-5' = 5 kali
        t = pj.cetusan('40 13 * * 1-5', utc(2026, 10, 19), utc(2026, 10, 24, 23, 59))
        self.assertEqual([x.day for x in t], [19, 20, 21, 22, 23])
        self.assertTrue(all((x.hour, x.minute) == (13, 40) for x in t))

    def test_cetusan_dom_dow_atau(self):
        # '17 3 1-7 1,4,7,10 6': hari 1–7 ATAU Sabtu, dalam Okt
        t = pj.cetusan('17 3 1-7 1,4,7,10 6', utc(2026, 10, 1), utc(2026, 10, 31, 23, 59))
        self.assertEqual([x.day for x in t], [1, 2, 3, 4, 5, 6, 7, 10, 17, 24, 31])

    def test_had_buka_dan_ny(self):
        self.assertEqual(pj.had_masa('buka', utc(2026, 10, 19, 21, 37)), utc(2026, 10, 20, 13, 0))
        self.assertEqual(pj.had_masa('buka', utc(2026, 10, 20, 0, 23)), utc(2026, 10, 20, 13, 0))
        # EDT (UTC-4): 9:15 NY = 13:15 UTC; EST (UTC-5) Disember: 14:15 UTC
        self.assertEqual(pj.had_masa(('ny', 9, 15), utc(2026, 10, 19, 11, 47)), utc(2026, 10, 19, 13, 15))
        self.assertEqual(pj.had_masa(('ny', 9, 15), utc(2026, 12, 7, 11, 47)), utc(2026, 12, 7, 14, 15))

    def test_dispatch_bila_jadual_hilang(self):
        crons = ['47 11 * * 1-5', '17 12 * * 1-5']
        kini = utc(2026, 10, 19, 12, 50)
        t, perlu = pj.keputusan(crons, ('ny', 9, 15), [], kini)
        self.assertEqual(t, utc(2026, 10, 19, 12, 17))
        self.assertTrue(perlu)
        # larian 11:50 dikira bagi 11:47 sahaja; cetusan 12:17 masih perlu
        self.assertTrue(pj.keputusan(crons, ('ny', 9, 15), [utc(2026, 10, 19, 11, 50)], kini)[1])
        self.assertFalse(pj.keputusan(crons, ('ny', 9, 15), [utc(2026, 10, 19, 12, 40)], kini)[1])

    def test_tunggu_lewat_dan_had(self):
        crons = ['47 11 * * 1-5', '17 12 * * 1-5']
        # 12:30: cetusan 12:17 belum lewat 30 minit -> sasaran 11:47
        self.assertEqual(pj.sasaran(crons, ('ny', 9, 15), utc(2026, 10, 19, 12, 30)), utc(2026, 10, 19, 11, 47))
        # selepas 9:15 NY tiada dispatch petang
        self.assertEqual(pj.keputusan(crons, ('ny', 9, 15), [], utc(2026, 10, 19, 13, 20)), (None, False))
        # harga 21:37 masih didispatch pada 02:00 esok, tidak selepas 13:00 UTC
        h = ['37 21 * * 1-5', '23 0 * * 2-6']
        self.assertEqual(pj.sasaran(h, 'buka', utc(2026, 10, 20, 2, 0)), utc(2026, 10, 20, 0, 23))
        self.assertIsNone(pj.sasaran(h, 'buka', utc(2026, 10, 20, 13, 5)))

    def test_hujung_minggu_tiada(self):
        self.assertIsNone(pj.sasaran(['40 13 * * 1-5'], ('ny', 16, 45), utc(2026, 10, 18, 15, 0)))

    def test_cron_workflow_sebenar(self):
        folder = os.path.join(AKAR, '.github', 'workflows')
        for fail in pj.JAGA:
            crons = pj.baca_cron(os.path.join(folder, fail))
            self.assertTrue(crons, fail)
            for c in crons:
                pj.cetusan(c, utc(2026, 10, 19), utc(2026, 10, 20))

    def test_semua_workflow_berjadual_dijaga(self):
        # Peraturan CLAUDE.md: setiap workflow berjadual mesti ada dalam JAGA. penjaga_jadual.yml menjaga dirinya
        # (cron sendiri setiap jam), jadi ia dikecualikan.
        folder = os.path.join(AKAR, '.github', 'workflows')
        berjadual = {f for f in sorted(os.listdir(folder)) if f.endswith('.yml') and pj.baca_cron(os.path.join(folder, f))}
        self.assertEqual(berjadual - {'penjaga_jadual.yml'} - set(pj.JAGA), set())

    def test_autotune_suku_dalam_jaga(self):
        self.assertIn('autotune_suku.yml', pj.JAGA)


if __name__ == '__main__':
    unittest.main()
