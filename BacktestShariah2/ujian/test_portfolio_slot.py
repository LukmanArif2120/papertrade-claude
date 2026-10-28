# Ujian portfolio maya 10 slot (standard/portfolio_slot.py): had slot, satu posisi setiap saham, susunan RS, keluar lorong 2,
# saiz ikut ekuiti, kawalan rawak deterministik, saiz berskala risiko RISIKO_10.
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

    def test_beku_kuota_lorong_dan_gantung(self):
        # 22 Okt 2026 (Fasa 4 item 13): kuota setiap kaedah, slot tidak terpakai dikongsi, lorong kaedah, mula_jejak, gantung
        def b2(s, kaedah, beli='2026-10-16', k1=None, h1=np.nan):
            r = baris(s, 50, beli=beli, kaedah=kaedah) + [k1 or '', h1, k1 is not None]
            return r
        kol = ['saham', 'id_kaedah', 'tarikh_isyarat', 'rs', 'tarikh_beli', 'harga_beli', 'keluar', 'tarikh_keluar_henti',
               'harga_keluar_henti', 'tarikh_keluar', 'harga_keluar1', 'keluar1']
        rows = [b2(f'A{i}', 'M70') for i in range(8)] + [b2(f'B{i}', 'M03') for i in range(2)] + [b2('LAMA', 'M70', beli='2026-10-15')]
        P = pd.DataFrame(rows, columns=kol)
        cfg = dict(mula='2026-10-16', kuota={'M70': 4, 'M03': 3, 'M18': 3}, lorong={'M70': 'kaedah', 'M03': 'henti', 'M18': 'henti'})
        R, E = ps.bina(P, 'GABUNGAN_10', ['2026-10-15'] + HARI[:1], lambda s, d: 10.0, cfg)
        self.assertNotIn('LAMA', set(R.saham)); self.assertEqual(E.tarikh.iloc[0], '2026-10-16')     # hanya >= mula_jejak
        self.assertEqual(len(R), 10)                                   # M70 4 kuota + M03 2 + 4 slot M03/M18 kosong dikongsi ke M70
        self.assertEqual((R.id_kaedah == 'M70').sum(), 8)
        self.assertEqual(set(R.lorong), {'kaedah', 'henti'})
        # lorong kaedah: keluar pada hari d direalisasi selepas belian hari itu (slot bebas esok)
        rows = [b2(f'A{i}', 'M70', k1='2026-10-19' if i == 0 else None, h1=11.0 if i == 0 else np.nan) for i in range(10)]
        rows += [b2('BARU1', 'M70', beli='2026-10-19'), b2('BARU2', 'M70', beli='2026-10-20')]
        cfg1 = dict(mula='2026-10-16', kuota={'M70': 10}, lorong={'M70': 'kaedah'})
        R, E = ps.bina(pd.DataFrame(rows, columns=kol), 'TOP1_10', HARI[:3], lambda s, d: 10.0, cfg1)
        self.assertNotIn('BARU1', set(R.saham)); self.assertIn('BARU2', set(R.saham))
        k = R[R.status == 'Keluar'].iloc[0]
        self.assertEqual((k.saham, k.tarikh_keluar), ('A0', '2026-10-19'))
        self.assertAlmostEqual(k.untung_pct, 100 * (1.1 * 0.999 / 1.001 - 1), places=6)
        # gantung: tiada belian baharu kaedah itu mulai tarikh log
        R, _ = ps.bina(pd.DataFrame(rows, columns=kol), 'TOP1_10', HARI[:3], lambda s, d: 10.0, cfg1, {'M70': '2026-10-19'})
        self.assertEqual(set(R.tarikh_beli), {'2026-10-16'})

    def test_risiko10_saiz_berskala_atr_dan_susunan_sama_rs(self):
        """RISIKO_10: saiz = risiko/(K x ATR%), dihadkan SAIZ_MIN..SAIZ_MAKS; susunan calon sama dengan RS_10."""
        rows = [baris('A', 90), baris('B', 80), baris('C', 70)]
        atr = {'A': 0.25, 'B': 2.5, 'C': 50.0}          # ATR% sangat rendah / sederhana / sangat tinggi
        R, E = ps.bina(calon(rows), 'RISIKO_10', HARI[:1], lambda s, d: 10.0,
                       atrp=lambda s, d: atr[s])
        saiz = dict(zip(R.saham, R.saiz_pct))
        # A: 0.010/(4*0.0025) = 1.0 -> dihadkan SAIZ_MAKS; C: 0.010/(4*0.50) = 0.005 -> dihadkan SAIZ_MIN
        self.assertAlmostEqual(saiz['A'], ps.SAIZ_MAKS * 100, places=4)
        self.assertAlmostEqual(saiz['C'], ps.SAIZ_MIN * 100, places=4)
        self.assertAlmostEqual(saiz['B'], ps.RISIKO / (ps.K_ATR * 0.025) * 100, places=4)
        self.assertGreater(saiz['A'], saiz['B'])        # ATR rendah -> posisi lebih besar
        self.assertGreater(saiz['B'], saiz['C'])
        r_rs, _ = ps.bina(calon(rows), 'RS_10', HARI[:1], lambda s, d: 10.0)
        self.assertEqual(list(R.saham), list(r_rs.saham))   # susunan dipasangkan dengan RS_10

    def test_risiko10_atr_tiada_jatuh_balik_saiz_tetap(self):
        rows = [baris('A', 90)]
        R, _ = ps.bina(calon(rows), 'RISIKO_10', HARI[:1], lambda s, d: 10.0, atrp=lambda s, d: None)
        self.assertAlmostEqual(float(R.saiz_pct.iloc[0]), ps.W * 100, places=4)
        R2, _ = ps.bina(calon(rows), 'RISIKO_10', HARI[:1], lambda s, d: 10.0)   # atrp=None
        self.assertAlmostEqual(float(R2.saiz_pct.iloc[0]), ps.W * 100, places=4)

    def test_rs10_tidak_terjejas_oleh_atrp(self):
        """Lorong sedia ada mesti kekal sama walaupun atrp dihantar."""
        rows = [baris(f'S{i:02d}', 50 + i) for i in range(12)]
        a, _ = ps.bina(calon(rows), 'RS_10', HARI[:2], lambda s, d: 10.0)
        b, _ = ps.bina(calon(rows), 'RS_10', HARI[:2], lambda s, d: 10.0, atrp=lambda s, d: 5.0)
        self.assertEqual(list(a.saham), list(b.saham))
        self.assertTrue(np.allclose(a.saiz_pct.astype(float), b.saiz_pct.astype(float)))

    def test_log_gantung(self):
        import json, tempfile
        with tempfile.TemporaryDirectory() as d:
            pp, lg = os.path.join(d, 'papan.json'), os.path.join(d, 'gantung.csv')
            with open(pp, 'w') as f:
                json.dump(dict(rows=[dict(id='M70', pantau='GANTUNG', p_sebab='x'), dict(id='M99', pantau='BERSARA'), dict(id='M03', pantau='OK')]), f)
            cfg = {'GABUNGAN_10': dict(kuota={'M70': 4, 'M03': 3})}
            self.assertEqual(ps.log_gantung(cfg, '2026-11-20', pp, lg), {'M70': '2026-11-23'})   # Jumaat -> Isnin
            with open(pp, 'w') as f:
                json.dump(dict(rows=[dict(id='M70', pantau='OK')]), f)
            self.assertEqual(ps.log_gantung(cfg, '2026-11-30', pp, lg), {'M70': '2026-11-23'})   # log kekal (tambah sahaja)

    def test_mdd_dari_ekuiti_mula(self):
        self.assertAlmostEqual(ps.mdd([0.94]), -0.06)


if __name__ == '__main__':
    unittest.main()
