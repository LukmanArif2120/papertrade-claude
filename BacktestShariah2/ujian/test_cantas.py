"""Ujian standard/cantas.py. TestKunci = pradaftar SPEC_CANTAS.md (9 Nov 2026); jangan ubah tanpa keputusan pengguna."""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import cantas as C  # noqa: E402


def _baris(**kw):
    r = dict(id='M01', nama='x', keluarga='M', status='BELUM CUKUP', pantau='OK', hari_beli=16, n=100,
             hari0_pct=0.0, t4_sesi=16, t4_pul=0.0, t4_spus=0.0, t4_mdd=-2.0)
    r.update(kw)
    return r


class TestKunci(unittest.TestCase):
    def test_ambang(self):
        self.assertEqual((C.C1_HARI_BELI, C.C1_POSISI, C.C1_HARI0_PCT), (12, 30, 20.0))
        self.assertEqual(C.C2_PANTAU, ('BERSARA', 'GANTUNG'))
        self.assertEqual(C.C4_LARIAN, 2)
        self.assertEqual((C.C5_SESI, C.C5_JURANG, C.C5_MDD), (63, 5.0, -10.0))
        self.assertEqual(C.BULAN_CADANG, 2)


class TestPeraturan(unittest.TestCase):
    def test_c1_hanya_mxx_dan_ambang(self):
        self.assertEqual([k for k, _ in C.nilai(_baris(hari0_pct=20.0))], ['C1'])
        self.assertEqual(C.nilai(_baris(hari0_pct=19.9)), [])
        self.assertEqual(C.nilai(_baris(hari0_pct=50.0, n=29)), [])
        self.assertEqual(C.nilai(_baris(hari0_pct=50.0, keluarga='N')), [])

    def test_c2_c3_c4(self):
        self.assertEqual([k for k, _ in C.nilai(_baris(pantau='GANTUNG'))], ['C2'])
        self.assertEqual([k for k, _ in C.nilai(_baris(status='NEGATIF'))], ['C3'])
        self.assertEqual(C.nilai(_baris(status='GAGAL'), None), [])
        self.assertEqual([k for k, _ in C.nilai(_baris(status='GAGAL'), dict(status='GAGAL'))], ['C4'])

    def test_c5(self):
        r = _baris(t4_sesi=63, t4_pul=-16.0, t4_spus=-10.0, t4_mdd=-12.0)
        self.assertEqual([k for k, _ in C.nilai(r)], ['C5'])
        self.assertEqual(C.nilai(_baris(t4_sesi=62, t4_pul=-16.0, t4_spus=-10.0, t4_mdd=-12.0)), [])
        self.assertEqual(C.nilai(_baris(t4_sesi=63, t4_pul=-14.9, t4_spus=-10.0, t4_mdd=-12.0)), [])
        self.assertEqual(C.nilai(_baris(t4_sesi=63, t4_pul=-16.0, t4_spus=-10.0, t4_mdd=-9.9)), [])

    def test_bulan_berturut_dan_fail(self):
        kol = list(_baris().keys())
        M1 = dict(harga_pada='2026-11-06', kol=kol, rows=[list(_baris(hari0_pct=30.0).values())])
        out1 = C.kira(M1, None)
        self.assertEqual(out1[0]['bulan_berturut'], 1)
        M2 = dict(M1, harga_pada='2026-12-01')
        out2 = C.kira(M2, dict(kaedah=out1))
        self.assertEqual(out2[0]['bulan_berturut'], 2)
        M3 = dict(M1, harga_pada='2026-12-15')               # bulan sama: tidak bertambah
        self.assertEqual(C.kira(M3, dict(kaedah=out2))[0]['bulan_berturut'], 2)
        M4 = dict(M1, harga_pada='2027-01-05', rows=[list(_baris(hari0_pct=0.0).values())])
        self.assertEqual(C.kira(M4, dict(kaedah=out2))[0]['bulan_berturut'], 0)
        with tempfile.TemporaryDirectory() as d:
            ks, oj, om = (os.path.join(d, x) for x in ('ks.json', 'c.json', 'C.md'))
            json.dump(M1, open(ks, 'w'))
            asal = (C.KS, C.OUT_JSON, C.OUT_MD)
            C.KS, C.OUT_JSON, C.OUT_MD = ks, oj, om
            try:
                self.assertEqual(C.main(), 0)
                self.assertIn('Calon cantas: 1 daripada 1', open(om, encoding='utf-8').read())
                self.assertEqual(C.main(), 0)                 # larian kedua membaca cantas.json lama
            finally:
                C.KS, C.OUT_JSON, C.OUT_MD = asal


if __name__ == '__main__':
    unittest.main()
