# Ujian standard/jalur_jangka.py — jalur jangkaan ke hadapan (carta kedua helaian posisi).
#
# Ujian ini wujud kerana LIMA nombor salah dihantar dalam satu petang semasa ciri itu dibina
# (1 Nov 2026), dan kesemuanya kelas yang sama: kuantiti yang kelihatan munasabah tetapi
# mengukur PERISTIWA YANG BERLAINAN daripada labelnya.
#   1. mae5 berasaskan rendah intrabar sedangkan mae_cl21 berasaskan tutup (fe822a2)
#   2. P(sentuh) menilai halangan TETAP sedangkan paras lorong 2 MENAIK (f637922)
#   3. desil ditanam ikut pangkat-dalam-tarikh tetapi dibaca ikut nilai mutlak (f637922)
#   4. penganggar ATR masa-larian purata mudah, jadual ditanam pada Wilder (379f5f7)
#   5. 129 posisi yang isyarat jualnya sudah tercetus masih menerbitkan jalur (379f5f7)
#
# Empat daripada lima ditangkap oleh semakan bebas, bukan oleh pembina. Pemeriksaan yang akan
# menangkap kesemuanya ialah SATU: bandingkan nombor yang dikira dengan simulasi PERATURAN
# SEBENAR pada data yang sama, sebelum ia dipaparkan. Itu `test_ratchet_*` di bawah.
#
# Pelajaran repo yang dipatuhi di sini (REVERSE/MOMENTUM_PEGANG.md §8a): ujian asap yang tidak
# boleh gagal tidak menguji apa-apa. Setiap ujian di bawah dibina supaya ia GAGAL pada versi kod
# sebelum pembetulannya — `test_ratchet_bukan_halangan_tetap` khususnya lulus hanya jika simulasi
# paras menaik diguna, dan gagal pada P(MAE <= jarak).
import json
import os
import sys
import unittest

import numpy as np
import pandas as pd

AKAR = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(AKAR, 'REVERSE', 'teras'))
import jalur_jangka as JJ  # noqa: E402


class UjianSimulatorParas(unittest.TestCase):
    """_p_tercetus mesti mengikut rekursi paras MENAIK, bukan halangan tetap."""

    @staticmethod
    def _siri():
        """Siri yang membezakan kedua-dua peraturan.

        tutup: 100 (bar masuk-1), kemudian 110, 120, 110, 100, 90.
        ATR dipaksa malar 5.0, jadi 4 x ATR = 20.
          selepas 110: puncak 110, paras = 110-20 =  90
          selepas 120: puncak 120, paras = 120-20 = 100   (menaik)
          tutup 110 >= 100, tutup 100 >= 100 -> belum
          tutup  90 <  100 -> TERCETUS
        Halangan TETAP pada 80 tidak pernah tercetus: min(tutup hadapan) = 90 > 80.
        """
        tk = np.array(['T'] * 7)
        o = np.array([100.0, 100.0, 110.0, 120.0, 110.0, 100.0, 90.0])
        c = np.array([100.0, 110.0, 120.0, 110.0, 100.0, 90.0, 90.0])
        atr = np.full(7, 5.0)
        return tk, o, c, atr

    def test_ratchet_bukan_halangan_tetap(self):
        tk, o, c, atr = self._siri()
        # paras awal -20% daripada buka(t+1)=100 -> 80. Halangan tetap TIDAK akan tercetus.
        out, sah = JJ._p_tercetus(tk, o, c, atr, H=5, grid=[-20])
        self.assertTrue(bool(out[0][0]),
                        'paras MENAIK sepatutnya tercetus pada tutup 90 < paras 100; '
                        'jika ini gagal, kod kembali kepada halangan tetap')
        # semakan silang: halangan tetap pada -20% memang TIDAK tercetus pada siri ini
        mae = c[1:6].min() / o[1] - 1.0
        self.assertGreater(mae * 100, -20.0,
                           'siri ujian rosak: halangan tetap sepatutnya TIDAK tercetus di sini')

    def test_paras_tidak_pernah_turun(self):
        """Selepas puncak jatuh, paras mesti kekal pada paras tertinggi, bukan mengikut puncak turun."""
        tk, o, c, atr = self._siri()
        # paras awal sangat rendah (-90%) supaya hanya mekanisme ratchet boleh mencetuskannya
        out, sah = JJ._p_tercetus(tk, o, c, atr, H=5, grid=[-90])
        self.assertTrue(bool(out[0][0]), 'tanpa ratchet paras kekal -90% dan tidak akan tercetus')

    def test_tidak_melintas_sempadan_ticker(self):
        """Tetingkap hadapan tidak boleh mengambil harga ticker lain (pepijat o[kk+1] merentas ticker)."""
        tk = np.array(['A'] * 4 + ['B'] * 4)
        o = np.array([100.0] * 4 + [10.0] * 4)
        c = np.array([100.0, 100.0, 100.0, 100.0, 1.0, 1.0, 1.0, 1.0])
        atr = np.full(8, 1.0)
        out, sah = JJ._p_tercetus(tk, o, c, atr, H=3, grid=[-50])
        # bar terakhir A (indeks 3) tidak boleh "tercetus" kerana kejatuhan milik B
        self.assertFalse(bool(out[0][3]), 'tetingkap melintas sempadan ticker')
        self.assertFalse(bool(sah[3]), 'bar sempadan ticker mesti DILUAR penyebut, bukan dikira 0')
        self.assertTrue(bool(sah[0]), 'bar dengan tetingkap lengkap mesti dalam penyebut')


class UjianSongsangGrid(unittest.TestCase):
    """p_sentuh menyongsang grid MENURUN; hujung dan kes sudah-tercetus mesti betul."""

    def setUp(self):
        self.grid = JJ.GRID_MAE
        self.sel = {'p_sentuh': [float(100 - i * 5) for i in range(len(self.grid))]}

    def test_monotonik_menurun_dengan_jarak(self):
        a = JJ.p_sentuh(self.sel, -2.0, self.grid)
        b = JJ.p_sentuh(self.sel, -20.0, self.grid)
        self.assertGreater(a, b, 'paras yang lebih jauh mesti kurang berkemungkinan tercetus')

    def test_apit_pada_hujung(self):
        self.assertAlmostEqual(JJ.p_sentuh(self.sel, -0.5, self.grid), self.sel['p_sentuh'][0], 3)
        self.assertAlmostEqual(JJ.p_sentuh(self.sel, -999.0, self.grid), self.sel['p_sentuh'][-1], 3)

    def test_jarak_positif_bermakna_sudah_tercetus(self):
        """Tutup sudah di bawah paras: 100%, bukan None ('tidak diketahui')."""
        self.assertEqual(JJ.p_sentuh(self.sel, 0.0, self.grid), 100.0)
        self.assertEqual(JJ.p_sentuh(self.sel, 3.2, self.grid), 100.0)
        self.assertIsNone(JJ.p_sentuh(self.sel, float('nan'), self.grid))


class UjianPenganggarATR(unittest.TestCase):
    """_atr_pct mesti guna penganggar yang MENANAM jadual (Wilder), bukan purata mudah."""

    def test_wilder_bukan_purata_mudah(self):
        r = np.random.default_rng(3)
        n = 200
        c = 100 + np.cumsum(r.normal(0, 1.5, n))
        h = c + np.abs(r.normal(0, 1.0, n))
        l = c - np.abs(r.normal(0, 1.0, n))
        dapat = JJ._atr_pct(h, l, c)
        from ind import _wilder
        pc = np.r_[np.nan, c[:-1]]
        tr = np.fmax(h - l, np.fmax(np.abs(h - pc), np.abs(l - pc)))
        jangka = _wilder(pd.Series(tr), 14).to_numpy() / c * 100.0
        np.testing.assert_allclose(dapat[20:], jangka[20:], rtol=1e-9,
                                   err_msg='_atr_pct tidak sepadan Wilder ind.py')
        sma = pd.Series(tr).rolling(14).mean().to_numpy() / c * 100.0
        self.assertFalse(np.allclose(dapat[20:], sma[20:], rtol=1e-6),
                         'purata mudah dan Wilder tidak boleh sama; ujian ini vakum')


class UjianJadual(unittest.TestCase):
    """Semakan struktur pada jadual yang DIKOMIT — ia yang dibaca setiap malam."""

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(JJ.JADUAL):
            raise unittest.SkipTest('jadual.json tiada')
        with open(JJ.JADUAL) as f:
            cls.j = json.load(f)

    def test_versi_direkod(self):
        self.assertEqual(self.j.get('versi'), JJ.VERSI,
                         'jadual dijana oleh versi kod lain; jana semula')

    def test_setiap_desil_setiap_ufuk_ada(self):
        for H in JJ.UFUK:
            for d in range(JJ.NDESIL):
                self.assertIn(f'{H}|{d}', self.j['sel'])

    def test_lebar_jalur_bertambah_dengan_volatiliti(self):
        """Dapatan terasnya: lebar BOLEH diramal. Jika ini gagal, pengkondisian rosak."""
        for H in JJ.UFUK:
            lebar = [self.j['sel'][f'{H}|{d}']['term'][4] - self.j['sel'][f'{H}|{d}']['term'][0]
                     for d in range(JJ.NDESIL)]
            self.assertEqual(lebar, sorted(lebar), f'lebar tidak monotonik pada H={H}: {lebar}')

    def test_mae_lebih_dalam_pada_ufuk_lebih_panjang(self):
        """Pemeriksaan yang akan menangkap pepijat asas-rendah-lawan-tutup (fe822a2)."""
        for d in range(JJ.NDESIL):
            m5 = self.j['sel'][f'5|{d}']['mae50']
            m21 = self.j['sel'][f'21|{d}']['mae50']
            self.assertLess(m21, m5, f'mae50 21 hari mesti lebih dalam daripada 5 hari (d{d})')

    def test_paras_menaik_sekurang_kurangnya_halangan_tetap(self):
        """P(paras menaik) >= P(halangan tetap) secara matematik, setiap sel, setiap ambang."""
        for H in JJ.UFUK:
            for d in range(JJ.NDESIL):
                s = self.j['sel'][f'{H}|{d}']
                if 'p_tetap' not in s:
                    continue
                for g, pm, pt in zip(self.j['grid_mae'], s['p_sentuh'], s['p_tetap']):
                    self.assertGreaterEqual(
                        pm + 0.05, pt,
                        f'H={H} d{d} ambang {g}: paras menaik {pm} < halangan tetap {pt}')

    def test_p_sentuh_menurun_dengan_jarak(self):
        for H in JJ.UFUK:
            for d in range(JJ.NDESIL):
                p = self.j['sel'][f'{H}|{d}']['p_sentuh']
                self.assertEqual(p, sorted(p, reverse=True),
                                 f'p_sentuh tidak monotonik pada H={H} d{d}')

    def test_tepi_desil_konsisten_dengan_median_sel(self):
        tepi = self.j['atr_pct_tepi']
        self.assertEqual(len(tepi), JJ.NDESIL - 1)
        self.assertEqual(tepi, sorted(tepi))
        for d in range(JJ.NDESIL):
            med = self.j['sel'][f'21|{d}']['atr_pct_median']
            lo = tepi[d - 1] if d else -np.inf
            hi = tepi[d] if d < JJ.NDESIL - 1 else np.inf
            self.assertTrue(lo <= med <= hi,
                            f'median atr_pct desil {d} ({med}) di luar tepinya [{lo}, {hi}]')


class UjianDokumen(unittest.TestCase):
    """Posisi yang isyarat jualnya sudah tercetus tidak boleh menerbitkan jalur ke hadapan."""

    @staticmethod
    def _harga(n=120, benih=5):
        r = np.random.default_rng(benih)
        c = 100 + np.cumsum(r.normal(0.05, 1.2, n))
        return pd.DataFrame({'date': pd.bdate_range('2026-01-05', periods=n),
                             'open': c, 'high': c + 1.0, 'low': c - 1.0, 'close': c})

    def test_status_bawah_jual_lepas_dilangkau(self):
        if not os.path.exists(JJ.JADUAL):
            self.skipTest('jadual.json tiada')
        H = {'AAA': self._harga()}
        # satu baris siri setiap status; hanya 'kunci' layak
        def baris(status):
            return [[101, 100.0, 90.0, 110.0, status, None, 100.0, 101.0, 99.0]]
        for status in ('bawah', 'jual', 'lepas'):
            d = JJ.dokumen(H, [[f'AAA|2026-01-05', baris(status)]])
            self.assertEqual(len(d['rows']), 0, f"status '{status}' sepatutnya dilangkau")
        d = JJ.dokumen(H, [['AAA|2026-01-05', baris('kunci')]])
        self.assertEqual(len(d['rows']), 1, "status 'kunci' sepatutnya menerbitkan jalur")
        self.assertLess(d['rows'][0][1]['jarak'], 0)


if __name__ == '__main__':
    unittest.main()
