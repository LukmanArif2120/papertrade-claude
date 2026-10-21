# Ujian kod/ambil_alih.py: penapis saham sedang diambil alih (sejak 21 Okt 2026) — corak harga terkunci, senarai sah,
# tiada pandang depan, dan penutupan posisi Papertrade C yang dibeli selepas pengumuman (isyarat palsu, tidak_sah).
import csv, os, sys, tempfile, unittest
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import ambil_alih as AA  # noqa: E402

IX = pd.bdate_range('2026-01-05', periods=200)
UMUM = 150    # indeks bar pengumuman


def saham(benih=1, umum=UMUM, jurang=0.40, julat_umum=0.008, julat_selepas=0.004, volum_x=20, n=200):
    """Bar biasa (julat ~3%, volum 1 juta), kemudian pada bar `umum` jurang buka +jurang, volum x volum_x dan julat sempit."""
    r = np.random.default_rng(benih)
    c = 50 * np.cumprod(1 + r.normal(0, 0.01, n)); o = np.r_[c[0], c[:-1]].copy()
    h = np.maximum(o, c) * 1.015; l = np.minimum(o, c) * 0.985; v = np.full(n, 1e6)
    if umum is not None:
        p = c[umum - 1] * (1 + jurang)
        for i in range(umum, n):
            j = julat_umum if i == umum else julat_selepas
            o[i] = p if i == umum else c[i - 1]
            c[i] = p * (1 + 0.001 * np.sin(i)); h[i] = max(o[i], c[i]) * (1 + j / 2); l[i] = min(o[i], c[i]) * (1 - j / 2)
            v[i] = 1e6 * (volum_x if i == umum else 3)
    return pd.DataFrame(dict(open=o, high=h, low=l, close=c, volume=v), index=IX[:n])


class TestKesan(unittest.TestCase):
    def test_corak_ambil_alih_dikesan_dari_hari_pengumuman(self):
        g = saham()
        self.assertEqual(AA.kesan_harga(g.iloc[:UMUM + 1]), IX[UMUM])
        self.assertEqual(AA.kesan_harga(g), IX[UMUM])

    def test_tiada_pandang_depan(self):
        g = saham()
        self.assertIsNone(AA.kesan_harga(g.iloc[:UMUM]))
        x = AA.tapis({'X': g}, IX[UMUM - 1], senarai=[])
        self.assertEqual(x, {})
        self.assertIn('X', AA.tapis({'X': g}, IX[UMUM], senarai=[]))

    def test_lonjakan_earnings_berjulat_lebar_tidak_dikesan(self):
        self.assertIsNone(AA.kesan_harga(saham(julat_umum=0.08, julat_selepas=0.03)))

    def test_volum_biasa_tidak_dikesan(self):
        self.assertIsNone(AA.kesan_harga(saham(volum_x=2)))

    def test_saham_tidak_cair_tidak_dikesan(self):
        g = saham(); g.loc[g.index[:UMUM], 'high'] = g.close[:UMUM]; g.loc[g.index[:UMUM], 'low'] = g.close[:UMUM]
        self.assertIsNone(AA.kesan_harga(g))

    def test_perjanjian_gagal_penapis_tamat(self):
        g = saham(n=200).copy()
        # 15 bar terakhir: harga jatuh dan bergerak semula (julat lebar)
        for k, i in enumerate(range(185, 200)):
            c = g.close.iloc[UMUM] * (0.7 + 0.02 * (k % 3))
            g.iloc[i] = [c, c * 1.03, c * 0.97, c, 2e6]
        self.assertIsNone(AA.kesan_harga(g))


class TestSenarai(unittest.TestCase):
    def test_senarai_sah_dan_bukan(self):
        biasa = saham(umum=None)
        sen = [dict(saham='Y', tarikh_umum=str(IX[100].date()), tarikh_tamat=str(IX[180].date()), pembeli='P',
                    harga_tawaran='60', bayaran='saham'),
               dict(saham='X', tarikh_umum='', tarikh_tamat='', pembeli='', harga_tawaran='', bayaran='bukan')]
        fr = {'X': saham(), 'Y': biasa}
        self.assertEqual(set(AA.tapis(fr, IX[160], sen)), {'Y'})          # X: bukan ambil alih (corak dimatikan)
        self.assertEqual(set(AA.tapis(fr, IX[99], sen)), set())           # sebelum pengumuman
        self.assertEqual(set(AA.tapis(fr, IX[180], sen)), set())          # perjanjian tamat
        self.assertIn('tawaran $60', AA.teks(AA.tapis(fr, IX[160], sen)['Y']))


class TestPosisi(unittest.TestCase):
    LAJUR = ['tarikh_beli', 'saham', 'kaedah', 'id_kaedah', 'sektor', 'industri', 'harga_beli', 'unit', 'harga_terkini',
             'untung_pct', 'hari', 'henti', 'sasaran', 'isyarat_keluar', 'keluar', 'tarikh_keluar', 'harga_keluar',
             'untung_akhir_pct', 'sumber', 'tidak_sah', 'sebab_tidak_sah', 'tidak_dibeli', 'keluar_henti',
             'tarikh_keluar_henti', 'harga_keluar_henti', 'untung_henti_pct', 'status_henti', 'tutup_semua']

    def test_tutup_dan_tanda_palsu(self):
        g = saham(n=180)
        akhir = str(IX[179].date())
        rows = [dict(tarikh_beli=str(IX[140].date()), saham='X', kaedah='M01', harga_beli='50', keluar='False'),   # sebelum: sah
                dict(tarikh_beli=str(IX[UMUM + 2].date()), saham='X', kaedah='M02', harga_beli='70', keluar='False'),
                dict(tarikh_beli=str(IX[185].date()), saham='X', kaedah='M03', harga_beli='70', keluar='False'),    # selepas bar akhir
                dict(tarikh_beli=str(IX[UMUM + 2].date()), saham='Z', kaedah='M04', harga_beli='50', keluar='False')]
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'claude_9.csv')
            with open(p, 'w', newline='') as f:
                w = csv.DictWriter(f, self.LAJUR); w.writeheader()
                for r in rows:
                    w.writerow({k: r.get(k, '') for k in self.LAJUR})
            x = AA.tanda_posisi(d, {'X': g, 'Z': saham(umum=None, n=180)}, senarai=[])
            out = list(csv.DictReader(open(p)))
            self.assertEqual(len(x), 2)
            self.assertEqual(out[0]['tidak_sah'], '')
            m2 = out[1]
            self.assertEqual((m2['tidak_sah'], m2['keluar'], m2['tarikh_keluar'], m2['keluar_henti'], m2['tutup_semua']),
                             ('True', 'True', akhir, 'True', 'True'))
            self.assertEqual(float(m2['harga_keluar']), round(float(g.close.iloc[-1]), 4))
            self.assertTrue(m2['sebab_tidak_sah'].startswith('isyarat palsu: saham diambil alih'))
            self.assertEqual((out[2]['tidak_sah'], out[2]['keluar']), ('True', 'False'))
            self.assertIn('menunggu', out[2]['isyarat_keluar'])
            self.assertEqual(out[3]['tidak_sah'], '')
            # larian kedua: tiada perubahan lagi bagi posisi yang sudah ditutup
            self.assertEqual([y[2] for y in AA.tanda_posisi(d, {'X': g}, senarai=[])], ['M03'])


if __name__ == '__main__':
    unittest.main()
