import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
import siri_v158 as SV  # noqa: E402


class TestUntungSemua(unittest.TestCase):
    SP = {20261001: (100.0, 101.0), 20261002: (102.0, 99.0), 20261005: (98.0, 100.0)}

    def test_dijual_guna_harga_jualan_dan_spus_buka_ke_buka(self):
        C = [dict(saham='A', harga_beli='10', tarikh_beli='2026-10-01', keluar='True', tarikh_keluar='2026-10-02', harga_keluar='9'),
             dict(saham='B', harga_beli='20', tarikh_beli='2026-10-01', keluar='False')]
        H = {'B': {20261001: 21.0, 20261002: 22.0, 20261005: 24.0}}
        r = SV.untung_semua(C, H, self.SP)
        self.assertEqual(r['t'], [20261001, 20261002, 20261005])
        # sesi 1: kedua-dua terbuka; A tiada harga -> hanya B dikira
        self.assertEqual(r['n'][0], 1)
        # sesi 3: A dijual (-10%), B +20% -> purata +5%
        self.assertAlmostEqual(r['u'][2], 5.0, places=3)
        # SPUS: A buka 1 Okt -> buka 2 Okt (+2%), B buka 1 Okt -> tutup 5 Okt (0%) -> purata +1%
        self.assertAlmostEqual(r['s'][2], 1.0, places=3)

    def test_tidak_dibeli_dan_tidak_sah_diabaikan(self):
        C = [dict(saham='A', harga_beli='10', tarikh_beli='2026-10-01', tidak_dibeli='True'),
             dict(saham='A', harga_beli='10', tarikh_beli='2026-10-01', tidak_sah='True')]
        self.assertEqual(SV.untung_semua(C, {'A': {20261001: 11}}, self.SP)['t'], [])

    def test_belian_masa_depan_tidak_masuk_sesi_lalu(self):
        C = [dict(saham='A', harga_beli='10', tarikh_beli='2026-10-05', keluar='False')]
        r = SV.untung_semua(C, {'A': {20261005: 10.5}}, self.SP)
        self.assertEqual(r['t'], [20261005])


if __name__ == '__main__':
    unittest.main()
