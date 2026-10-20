# Ujian portfolio maya 10 slot (standard/portfolio_slot.py): had slot, satu posisi setiap saham, susunan RS, keluar lorong 2,
# saiz ikut ekuiti, kawalan rawak deterministik.
import os, sys, unittest
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import portfolio_slot as ps

HARI = ['2026-10-16', '2026-10-19', '2026-10-20', '2026-10-21']


def calon(rows):
    P = pd.DataFrame(rows, columns=['saham', 'id_kaedah', 'tarikh_isyarat', 'rs', 'tarikh_beli', 'harga_beli', 'keluar',
                                    'tarikh_keluar_henti', 'harga_keluar_henti'])
    return P.sort_values(['tarikh_beli', 'saham', 'id_kaedah']).reset_index(drop=True)


def baris(s, rs, beli='2026-10-16', keluar=None, hk=np.nan, kaedah='M01'):
    return [s, kaedah, '2026-10-15', rs, beli, 10.0, keluar is not None, keluar or '', hk]


class TestPortfolioSlot(unittest.TestCase):
    def test_had_slot_rs_dan_satu_saham(self):
        rows = [baris(f'S{i:02d}', 50 + i) for i in range(15)] + [baris('S14', 64, kaedah='M02'), baris('S13', 63, kaedah='M03')]
        R, E = ps.bina(calon(rows), 'RS_10', HARI[:1], lambda s, d: 10.0)
        self.assertEqual(len(R), 10)
        self.assertEqual(R.saham.nunique(), 10)
        self.assertEqual(set(R.saham), {f'S{i:02d}' for i in range(5, 15)})      # RS tertinggi dahulu, pendua saham dilangkau
        self.assertAlmostEqual(E.ekuiti.iloc[-1], 1.0)
        self.assertAlmostEqual(E.tunai.iloc[-1], 0.0)

    def test_keluar_lorong2_bebaskan_slot_dan_saiz_ikut_ekuiti(self):
        rows = [baris(f'S{i:02d}', 90 - i) for i in range(10)]
        rows[0] = baris('S00', 90, keluar='2026-10-20', hk=12.0)                  # +20% pada buka 20 Okt
        rows += [baris('BARU', 99, beli='2026-10-20'), baris('LEWAT', 98, beli='2026-10-20')]
        R, E = ps.bina(calon(rows), 'RS_10', HARI, lambda s, d: 10.0)
        k = R[R.status == 'Keluar'].iloc[0]
        self.assertEqual(k.saham, 'S00')
        self.assertAlmostEqual(k.untung_pct, 100 * (1.2 * 0.999 / 1.001 - 1), places=6)
        hasil = 0.1 * 1.2 * 0.999 / 1.001
        self.assertIn('BARU', set(R.saham)); self.assertNotIn('LEWAT', set(R.saham))   # satu slot kosong sahaja
        b = R[R.saham == 'BARU'].iloc[0]
        self.assertAlmostEqual(b.saiz_pct, 10.0, places=6)                          # 10% ekuiti semalam (1.0)
        self.assertAlmostEqual(E.ekuiti.iloc[-1], 0.9 + hasil, places=9)
        self.assertEqual(int(E.bil_posisi.iloc[-1]), 10)

    def test_rawak_tetap_dan_berbeza_daripada_rs(self):
        rows = [baris(f'S{i:02d}', i) for i in range(40)]
        a, _ = ps.bina(calon(rows), 'RAWAK_10', HARI[:1], lambda s, d: 10.0)
        b, _ = ps.bina(calon(rows), 'RAWAK_10', HARI[:1], lambda s, d: 10.0)
        r, _ = ps.bina(calon(rows), 'RS_10', HARI[:1], lambda s, d: 10.0)
        self.assertEqual(list(a.saham), list(b.saham))
        self.assertNotEqual(set(a.saham), set(r.saham))

    def test_rs_tiada_paling_akhir(self):
        rows = [baris(f'S{i:02d}', np.nan) for i in range(5)] + [baris(f'T{i:02d}', 10 + i) for i in range(8)]
        R, _ = ps.bina(calon(rows), 'RS_10', HARI[:1], lambda s, d: 10.0)
        self.assertEqual(sum(R.saham.str.startswith('T')), 8)

    def test_mdd_dari_ekuiti_mula(self):
        self.assertAlmostEqual(ps.mdd([0.94]), -0.06)


if __name__ == '__main__':
    unittest.main()
