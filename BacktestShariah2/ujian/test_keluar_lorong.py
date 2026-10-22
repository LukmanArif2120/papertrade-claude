# Ujian standard/keluar_lorong.py: lorong 2 (pegang selagi naik, sejak 19 Okt 2026: Chandelier tutup 4×ATR14,
# paras hanya naik, tanpa henti kaedah).
import csv, os, sys, tempfile, unittest
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import keluar_lorong as K  # noqa: E402
import enjin  # noqa: E402

IX = [str(x.date()) for x in pd.bdate_range('2026-08-03', periods=80)]
PRA = 20          # bar sejarah sebelum hari beli (ATR14 sudah ada pada hari beli)


def bar(c, o=None, h=None, l=None):
    c = np.array(c, float); o = c.copy() if o is None else np.array(o, float)
    h = np.maximum(o, c) if h is None else np.array(h, float); l = np.minimum(o, c) if l is None else np.array(l, float)
    return IX[:len(c)], o, h, l, c


def langkah(tutup):
    """Bar dengan tinggi = tutup + 1, rendah = tutup − 1, buka = tutup semalam. Langkah tutup ±1 -> julat sebenar 2, jadi ATR14 = 2
    dan paras keluar = puncak − 8."""
    c = np.array(tutup, float); o = np.r_[c[0], c[:-1]]
    return IX[:len(c)], o, c + 1, c - 1, c


def siri(*kaki):
    """PRA bar mendatar pada 100 diikuti kaki (sasaran tutup) dengan langkah 1 setiap bar."""
    t = [100.0] * PRA
    for x in kaki:
        d = 1 if x > t[-1] else -1
        t += list(np.arange(t[-1] + d, x + d / 2, d))
    return t


class UjiLorong(unittest.TestCase):
    def test_atr_sama_enjin(self):
        rng = np.random.default_rng(1); c = 50 * np.exp(np.cumsum(rng.normal(0, .02, 60)))
        o = c * np.exp(rng.normal(0, .01, 60)); h = np.maximum(o, c) * 1.01; l = np.minimum(o, c) * .99
        g = pd.DataFrame(dict(open=o, high=h, low=l, close=c))
        np.testing.assert_allclose(K.atr(h, l, c), enjin.atr(g).to_numpy(), equal_nan=True)

    def test_pegang_naik(self):
        ix, o, h, l, c = langkah(siri(110))          # beli 100 pada bar PRA, naik ke 110
        L2, _ = K.nilai_baris(ix, o, h, l, c, ix[PRA], 100.0)
        self.assertEqual(L2['keluar_henti'], 'False')
        self.assertEqual(L2['status_henti'], f'Pegang (paras keluar 102.00; puncak 110.00; {len(c) - 1 - PRA} hari)')

    def test_keluar_tutup_bawah_paras(self):
        # puncak 110, paras 102: tutup 101 -> jual pada buka bar seterusnya
        t = siri(110, 101) + [100.5]
        ix, o, h, l, c = langkah(t)
        j = len(t) - 2                                # bar tutup 101 dalam kaki turun
        L2, _ = K.nilai_baris(ix, o, h, l, c, ix[PRA], 100.0)
        self.assertEqual((L2['keluar_henti'], L2['tarikh_keluar_henti'], L2['harga_keluar_henti'], L2['untung_henti_pct']),
                         ('True', ix[j + 1], '101', '1.00'))
        self.assertIn('tutup 101.00 bawah paras keluar 102.00 pada', L2['status_henti'])

    def test_satu_dua_hari_turun_tidak_keluar(self):
        # turun 3 hari berturut dari puncak (peraturan lama keluar selepas 2) -> masih atas paras
        ix, o, h, l, c = langkah(siri(110, 107, 109))
        L2, _ = K.nilai_baris(ix, o, h, l, c, ix[PRA], 100.0)
        self.assertEqual(L2['keluar_henti'], 'False'); self.assertIn('paras keluar 102.00', L2['status_henti'])

    def test_paras_hanya_naik(self):
        # bar julat besar menaikkan ATR (calon paras turun), tetapi paras kekal 102 -> tutup 101.5 keluar
        t = siri(110) + [109.0, 101.5, 101.0]
        ix, o, h, l, c = langkah(t)
        k = len(siri(110)); h[k], l[k] = 115.0, 95.0
        self.assertLess(110 - 4 * K.atr(h, l, c)[k], 102)
        L2, _ = K.nilai_baris(ix, o, h, l, c, ix[PRA], 100.0)
        self.assertEqual((L2['tarikh_keluar_henti'], L2['harga_keluar_henti']), (ix[k + 2], '101.5'))

    def test_henti_kaedah_tidak_dipakai(self):
        # rendah jatuh jauh bawah harga beli (henti kaedah biasa) tetapi tutup kekal atas paras -> tiada keluar
        ix, o, h, l, c = langkah(siri(103))
        l[PRA + 1] = 90.0
        r = dict(saham='X', kaedah='M01', tarikh_beli=ix[PRA], harga_beli='100', henti='95', keluar='True')
        K.kemas_baris(r, {'X': (ix, o, h, l, c)}, [])
        self.assertEqual((r['keluar_henti'], r['tutup_semua']), ('False', 'False'))

    def test_menunggu(self):
        t = siri(110, 101)
        ix, o, h, l, c = langkah(t)
        L2, _ = K.nilai_baris(ix, o, h, l, c, ix[PRA], 100.0)
        self.assertEqual(L2['keluar_henti'], 'False')
        self.assertTrue(L2['status_henti'].startswith('Tutup 101.00 bawah paras keluar 102.00 pada'))
        self.assertIn('menunggu', L2['status_henti'])

    def test_atr_belum_ada(self):
        ix, o, h, l, c = bar([100, 103, 102, 105])
        L2, _ = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0)
        self.assertEqual(L2['keluar_henti'], 'False'); self.assertIn('paras keluar belum ada', L2['status_henti'])

    def test_harga_tidak_sepadan(self):
        ix, o, h, l, c = bar([50, 51])
        L2, sebab = K.nilai_baris(ix, o, h, l, c, ix[0], 100.0)
        self.assertIsNone(L2); self.assertIn('tidak sepadan', sebab)


class UjiBaris(unittest.TestCase):
    H = {'X': langkah(siri(110, 101) + [100.5])}

    def baris(self, **kw):
        return dict(dict(saham='X', kaedah='M01', tarikh_beli=IX[PRA], harga_beli='100', henti='95', keluar='True'), **kw)

    def test_beku_dan_tutup_semua(self):
        r = self.baris()
        K.kemas_baris(r, self.H, [])
        self.assertEqual((r['keluar_henti'], r['tutup_semua']), ('True', 'True'))
        r['harga_keluar_henti'] = '94.5'          # lorong yang sudah keluar (peraturan semasa) dibekukan
        K.kemas_baris(r, self.H, [])
        self.assertEqual(r['harga_keluar_henti'], '94.5')

    def test_peraturan_lama_dikira_semula(self):
        # keluar dengan peraturan lama (2 tutup turun / kena henti): status tanpa PENANDA -> dikira semula sekali
        r = self.baris(keluar_henti='True', tarikh_keluar_henti=IX[PRA + 1], harga_keluar_henti='95', untung_henti_pct='-5.00',
                       status_henti='Keluar: kena henti (4 Sep @ 95.00)')
        K.kemas_baris(r, self.H, [])
        self.assertEqual((r['keluar_henti'], r['harga_keluar_henti']), ('True', '101'))
        self.assertIn(K.PENANDA, r['status_henti'])

    def test_keluar_paksa_dibekukan(self):
        # 22 Okt 2026 (R4): keluar paksa tidak_layak.py (isyarat palsu / delist) tidak dibuka semula
        for st in ('Keluar: isyarat palsu, saham diambil alih (umum 2026-10-20; senarai) — tutup 2026-10-21 @ 45.68',
                   'Keluar: delist / tiada data 6 sesi — tutup akhir 2026-10-16 @ 94.96'):
            r = self.baris(keluar_henti='True', tarikh_keluar_henti=IX[PRA + 1], harga_keluar_henti='95', untung_henti_pct='-5.00',
                           status_henti=st)
            K.kemas_baris(r, self.H, [])
            self.assertEqual((r['keluar_henti'], r['harga_keluar_henti'], r['status_henti']), ('True', '95', st))

    def test_semula_kira_lorong_yang_sudah_keluar(self):
        H = {'X': langkah(siri(110))}
        r = self.baris(keluar='False', keluar_henti='True', tarikh_keluar_henti=IX[PRA + 1], harga_keluar_henti='95',
                       untung_henti_pct='-5.00', status_henti='Keluar: tutup 94.00 bawah paras keluar 95.00 pada 1 Sep (2 Sep @ 95.00)')
        K.kemas_baris(r, H, [])
        self.assertEqual(r['harga_keluar_henti'], '95')            # beku
        K.kemas_baris(r, H, [], semula=('henti',))
        self.assertEqual((r['keluar_henti'], r['harga_keluar_henti']), ('False', ''))

    def test_tidak_dibeli_kosong(self):
        r = dict(saham='X', kaedah='M01', tarikh_beli='', tidak_dibeli='True')
        K.kemas_baris(r, {}, [])
        self.assertEqual(r['tutup_semua'], '')

    def test_fail(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, 'claude.csv'), 'w', newline='') as f:
                w = csv.writer(f); w.writerow(['tarikh_beli', 'saham', 'kaedah', 'harga_beli', 'henti', 'keluar', 'capai_10', 'keluar_10'])
                w.writerow([IX[PRA], 'X', 'M01', '100', '95', 'False', 'True', 'False'])
            H = {'X': langkah(siri(110))}
            asal = K.muat_harga; K.muat_harga = lambda stor: H
            try:
                K.main(['--folder', d, '--stor', d])
            finally:
                K.muat_harga = asal
            r = list(csv.DictReader(open(os.path.join(d, 'claude.csv'))))[0]
        self.assertEqual((r['keluar_henti'], r['tutup_semua']), ('False', 'False'))
        self.assertIn('paras keluar 102.00', r['status_henti'])
        self.assertNotIn('capai_10', r); self.assertNotIn('keluar_10', r)   # lajur lorong 10% dibuang


if __name__ == '__main__':
    unittest.main()
