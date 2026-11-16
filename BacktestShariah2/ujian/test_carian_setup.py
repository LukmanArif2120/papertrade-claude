"""Ujian carian setup CS01 (`kajian/carian_setup/`, pradaftar `kajian/SPEC_CARIAN_SETUP.md`):
ruang carian dikunci, tiada pandang ke hadapan, mekanik dagangan SPEC §4 dan pengumpulan skor SPEC §6."""
import json
import os
import sys
import unittest

import numpy as np
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SINI, '..', 'kajian', 'carian_setup'))
import cs_atom as atom  # noqa: E402
import cs_teras as teras  # noqa: E402

A1, A2, OP = teras.peraturan_keluar(len(atom.KELUAR))
NR = len(A1)
JENIS = np.zeros(len(atom.KELUAR), np.int64)
PAR = np.zeros(len(atom.KELUAR))
for _a, (_j, _v) in atom.LALUAN.items():
    JENIS[_a] = 1 if _j == 'chand' else 2
    PAR[_a] = _v


def _saham(n, benih):
    rng = np.random.default_rng(benih)
    c = 50 * np.exp(np.cumsum(rng.normal(0.0005, 0.02, n)))
    o = c * (1 + rng.normal(0, 0.005, n))
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.006, n)))
    l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.006, n)))
    ix = pd.bdate_range('2019-01-02', periods=n)
    return pd.DataFrame({'open': o, 'high': h, 'low': l, 'close': c, 'volume': rng.integers(2e5, 3e6, n).astype(float)},
                        index=ix)


def _peraturan(a, b=None, op=1):
    """Indeks peraturan keluar bagi atom a (tunggal) atau pasangan (a, b) dengan op 2 = ATAU, 3 = DAN."""
    for r in range(NR):
        if b is None and OP[r] == 1 and A1[r] == a:
            return r
        if b is not None and OP[r] == op and A1[r] == a and A2[r] == b:
            return r
    raise KeyError((a, b, op))


class TestKunci(unittest.TestCase):
    def test_ruang_carian_dikunci(self):
        self.assertEqual((len(atom.PENCETUS), len(atom.PENAPIS), len(atom.KELUAR), len(atom.HENTI)), (49, 30, 24, 4))
        self.assertEqual(NR, 1 + 24 + 2 * 276)
        self.assertEqual(teras.NH * NR, 2308)
        self.assertEqual((atom.TMAX, teras.TMAX, atom.KOS, teras.KOS), (20, 20, 0.005, 0.005))
        self.assertEqual(atom.TEMPOH['431'], (('Latih', 20200102, 20230630), ('Sah', 20230703, 20260828)))
        self.assertEqual(atom.TEMPOH['kunci'], (('K1', 20100104, 20191231), ('K2', 20200102, 20260828)))

    def test_tempoh_cs02_dikunci(self):
        # Pindaan 13 Nov 2026 (b): pemenang mesti untung dalam dua era; K3 tidak dipakai carian.
        self.assertEqual(atom.TEMPOH['A'], (('E1', 20100104, 20191231), ('E2', 20200102, 20241231)))
        self.assertEqual(atom.TEMPOH['B'], (('K1', 20100104, 20191231), ('K2', 20200102, 20241231),
                                            ('K3', 20250102, 20260828)))
        self.assertLess(atom.TEMPOH['A'][1][2], atom.TEMPOH['B'][2][1])


class TestTiadaPandangHadapan(unittest.TestCase):
    def test_bar_lama_tidak_berubah_bila_data_masa_depan_ditambah(self):
        g = _saham(700, 1)
        rs = pd.Series(np.random.default_rng(2).uniform(0, 100, 700), index=g.index)
        satu = pd.Series(1.0, index=g.index)
        penuh = atom.indikator(g, rs, satu, satu)
        pendek = atom.indikator(g.iloc[:560], rs.iloc[:560], satu.iloc[:560], satu.iloc[:560])
        for kump_p, kump_s in zip(penuh[:3], pendek[:3]):
            for nama in kump_p:
                self.assertTrue(np.array_equal(kump_p[nama][:560], kump_s[nama]), nama)
        self.assertTrue(np.allclose(penuh[3][:560], pendek[3], equal_nan=True))

    def test_mula_isyarat_tidak_merentas_saham(self):
        sig = np.array([1, 1, 0, 1, 1, 1, 0, 1], bool)
        self.assertEqual(atom.mula_isyarat(sig, np.array([0, 4, 8])).tolist(),
                         [True, False, False, True, True, False, False, True])


class TestMekanik(unittest.TestCase):
    def setUp(self):
        n = 40
        self.o = np.full(n, 100.0)
        self.h = np.full(n, 101.0)
        self.l = np.full(n, 99.0)
        self.c = np.full(n, 100.0)
        self.atr = np.full(n, 2.0)
        self.X = np.zeros((len(atom.KELUAR), n), np.uint8)

    def jalan(self, s, r, i=5):
        R, hp, sk = teras.hasil_satu(np.array([i]), self.o, self.h, self.l, self.c, self.atr, self.X, JENIS, PAR,
                                     A1, A2, OP, s, r)
        return R[0], hp[0], sk[0]

    def test_tiada_keluar_jual_tutup_sesi_20(self):
        self.c[6 + 19] = 110.0
        self.h[6 + 19] = 111.0
        R, hp, _ = self.jalan(0, 0)
        self.assertAlmostEqual(R, 0.10 - 0.005)
        self.assertEqual(hp, 20)

    def test_keluar_indikator_hari_beli_dijual_buka_esok_bukan_hari_sama(self):
        self.X[0, 6] = 1                       # X01 benar pada tutup hari beli
        self.o[7] = 103.0
        R, hp, sk = self.jalan(0, _peraturan(0))
        self.assertAlmostEqual(R, 0.03 - 0.005)
        self.assertEqual((hp, sk), (1, 1))

    def test_henti_tidak_aktif_intrahari_pada_hari_beli(self):
        self.l[6] = 80.0                       # rendah hari beli jauh di bawah henti, tutup kekal 100
        R, hp, _ = self.jalan(0, 0)
        self.assertAlmostEqual(R, -0.005)
        self.assertEqual(hp, 20)

    def test_tutup_hari_beli_bawah_henti_jual_buka_esok(self):
        self.c[6] = 90.0
        self.l[6] = 89.0
        self.o[7] = 91.0
        R, hp, _ = self.jalan(0, 0)
        self.assertAlmostEqual(R, -0.09 - 0.005)
        self.assertEqual(hp, 1)

    def test_henti_intrahari_sesi_kedua_pada_paras(self):
        self.l[7] = 91.0                       # H1 = 92
        R, hp, _ = self.jalan(0, 0)
        self.assertAlmostEqual(R, -0.08 - 0.005)
        self.assertEqual(hp, 2)

    def test_jurang_bawah_henti_jual_pada_buka(self):
        self.o[8] = 85.0
        self.l[8] = 84.0
        R, hp, _ = self.jalan(1, 0)            # H2 = 90
        self.assertAlmostEqual(R, -0.15 - 0.005)
        self.assertEqual(hp, 3)

    def test_henti_atr(self):
        self.l[7] = 93.5                       # H3 = 100 - 3 x 2 = 94; H4 = 92
        self.assertAlmostEqual(self.jalan(2, 0)[0], -0.06 - 0.005)
        self.assertAlmostEqual(self.jalan(3, 0)[0], -0.005)

    def test_pasangan_atau_dan(self):
        self.X[0, 8] = 1                       # X01 pada sesi 2
        self.X[1, 10] = 1                      # X02 pada sesi 4
        self.X[0, 10] = 1
        self.o[9], self.o[11] = 104.0, 107.0
        self.assertEqual(self.jalan(0, _peraturan(0, 1, 2))[1], 3)      # ATAU: sesi 2 -> jual buka sesi 3
        self.assertAlmostEqual(self.jalan(0, _peraturan(0, 1, 2))[0], 0.04 - 0.005)
        self.assertEqual(self.jalan(0, _peraturan(0, 1, 3))[1], 5)      # DAN: sesi 4 -> jual buka sesi 5
        self.assertAlmostEqual(self.jalan(0, _peraturan(0, 1, 3))[0], 0.07 - 0.005)

    def test_chandelier_ikut_tutup_tertinggi_sejak_beli(self):
        self.c[6:12] = [100, 105, 110, 115, 108.5, 108.5]               # X18: 115 - 3 x 2 = 109 > 108.5 pada sesi 4
        self.h[6:12] = 116
        self.o[11] = 108.0
        R, hp, _ = self.jalan(1, _peraturan(17))
        self.assertAlmostEqual(R, 0.08 - 0.005)
        self.assertEqual(hp, 5)

    def test_satu_posisi_setiap_saham(self):
        ev = np.array([5, 8, 30, 31, 45])
        sk = np.array([19, 19, 3, 3, 3])
        tid = np.zeros(60, np.int32)
        tid[40:] = 1
        self.assertEqual(teras.satu_posisi(ev, sk, tid).tolist(), [True, False, True, False, True])

    def test_pilih_slot_had_slot_dan_saham_sedang_dipegang(self):
        # dua saham (tid 0: bar 0-59, tid 1: bar 60-119), hari = indeks bar dalam saham
        tid = np.repeat([0, 1], 60).astype(np.int32)
        hari = np.tile(np.arange(60), 2)
        ev = np.array([5, 8, 65, 30, 95])          # saham0 hari5, saham0 hari8, saham1 hari5, saham0 hari30, saham1 hari35
        sk = np.array([10, 3, 10, 3, 3])
        susun = np.lexsort((np.arange(5), hari[ev + 1]))
        satu = teras.pilih_slot(ev, sk, tid, hari, susun, 1)
        self.assertEqual(satu.tolist(), [True, False, False, True, True])    # 1 slot: isyarat serentak ditolak
        dua = teras.pilih_slot(ev, sk, tid, hari, susun, 2)
        self.assertEqual(dua.tolist(), [True, False, True, True, True])      # saham sedang dipegang tidak dibeli lagi

    def test_jumlah_harian_dibahagi_slot(self):
        self.c[6:9] = [102, 104, 106]
        ev = np.array([5])
        R, hp, sk = teras.hasil_satu(ev, self.o, self.h, self.l, self.c, self.atr, self.X, JENIS, PAR, A1, A2, OP, 0, 0)
        jum, bil = teras.jumlah_harian(ev, R, sk, self.o, self.c, np.arange(40), 40)
        self.assertEqual(int(bil.sum()), 20)
        self.assertAlmostEqual(float(jum.sum()), float(np.log1p(R[0])), delta=0.01)

    def test_buku_harian_menyamai_pulangan_dagangan(self):
        self.c[6:9] = [102, 104, 106]
        self.X[0, 8] = 1
        self.o[9] = 105.0
        ev = np.array([5])
        R, hp, sk = teras.hasil_satu(ev, self.o, self.h, self.l, self.c, self.atr, self.X, JENIS, PAR, A1, A2, OP, 0,
                                     _peraturan(0))
        bk = teras.buku_harian(ev, R, sk, hp, self.o, self.c, np.arange(40), 40)
        self.assertEqual(np.count_nonzero(bk), 4)
        self.assertAlmostEqual(float(np.prod(1 + bk) - 1), R[0], delta=5e-4)   # kos dibahagi dua hari, dikompaun


class TestLabelTangkap(unittest.TestCase):
    """SPEC pindaan (d): label kadar tangkap."""

    def setUp(self):
        import cs_tangkap
        self.label = cs_tangkap.label
        self.o = np.full(40, 100.0)
        self.l = np.full(40, 99.0)
        self.c = np.full(40, 100.0)

    def jalan(self):
        return self.label(np.array([5]), self.o, self.l, self.c)[0].tolist()

    def test_lari_naik_minggu_pertama_capai_10_dan_kekal(self):
        self.c[6:26] = np.linspace(102, 125, 20)          # sesi 5 = 106.8, sesi 20 = 125
        self.assertEqual(self.jalan(), [1, 1, 1, 0, 1])

    def test_henti_dahulu_bermakna_gagal_walaupun_naik_kemudian(self):
        self.l[8] = 91.0                                  # henti -8 % pada sesi 3
        self.c[12:26] = 130.0
        m5, t10, t20, gagal, lari = self.jalan()
        self.assertEqual((t10, t20, gagal, lari), (0, 0, 1, 0))

    def test_capai_10_tetapi_jatuh_semula_bukan_lari(self):
        self.c[6:12] = [103, 106, 108, 110, 112, 111]     # m5 dan t10 benar
        self.c[25] = 104.0                                # tutup sesi 20 di bawah +10 %
        self.assertEqual(self.jalan(), [1, 1, 0, 0, 0])


class TestHadapan(unittest.TestCase):
    """SPEC pindaan (f): penjejak hadapan mesti memakai mekanik yang sama dengan backtest."""

    def setUp(self):
        import cs_hadapan
        self.H = cs_hadapan
        rng = np.random.default_rng(7)
        n = 400
        c = 50 * np.exp(np.cumsum(rng.normal(0, 0.03, n)))
        o = c * (1 + rng.normal(0, 0.01, n))
        self.pan = {'o': o, 'h': np.maximum(o, c) * 1.01, 'l': np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.02, n))),
                    'c': c, 'atr': 0.03 * c, 'X': (rng.random((len(atom.KELUAR), n)) < 0.15).astype(np.uint8),
                    'mula': np.array([0, n]), 'tid': np.zeros(n, np.int32)}

    def test_simulasi_menyamai_teras_bagi_tetingkap_lengkap(self):
        p = self.pan
        ev = np.arange(30, 360)
        for s, r in [(0, 0), (1, 5), (2, 18), (3, 19), (0, 20), (1, 300), (2, 400), (3, NR - 1)]:
            R, hp, sk = teras.hasil_satu(ev, p['o'], p['h'], p['l'], p['c'], p['atr'], p['X'], JENIS, PAR, A1, A2, OP, s, r)
            for k, i in enumerate(ev):
                x = self.H.simulasi(p, int(i), s, r, pegang_min=1)              # tanpa pegang minimum = enjin lama
                self.assertEqual(x['status'], 'TUTUP')
                self.assertAlmostEqual(x['R'], R[k], places=10, msg=(s, r, i))
                self.assertEqual((x['sesi'], x['bar_keluar']), (hp[k], i + 1 + sk[k]), (s, r, i))

    def test_pegang_minimum_penjejak(self):
        """Pindaan (p): indikator keluar hanya menjual mulai buka sesi ke-4; henti rugi tidak berubah."""
        self.assertEqual(atom.PEGANG_MIN, 3)
        p = self.pan
        awal = 0
        for s, r in [(1, 5), (2, 18), (0, 20), (1, 300), (3, NR - 1)]:
            for i in range(30, 360):
                x1, x3 = self.H.simulasi(p, i, s, r, pegang_min=1), self.H.simulasi(p, i, s, r)
                if x3['sebab'] == 'keluar indikator':
                    self.assertGreaterEqual(x3['sesi'], 3, (s, r, i))           # dipegang penuh 3 sesi
                self.assertGreaterEqual(x3['bar_keluar'], i + 2)                # tiada jualan pada hari beli
                if x1['sebab'] == 'keluar indikator' and x1['sesi'] < 3:
                    awal += 1
                    self.assertGreaterEqual(x3['bar_keluar'], x1['bar_keluar'])
                else:                                                           # henti, had masa atau indikator lewat: sama
                    self.assertEqual((x3['sebab'], x3['sesi'], x3['R']), (x1['sebab'], x1['sesi'], x1['R']), (s, r, i))
        self.assertGreater(awal, 0)                                             # ujian benar-benar menyentuh kes jualan awal

    def test_status_tetingkap_belum_lengkap(self):
        p = dict(self.pan)
        p['X'] = np.zeros_like(p['X'])
        p['l'] = p['c'] * 0.999                                        # tiada henti
        p['o'] = p['c'].copy()
        n = len(p['c'])
        self.assertEqual(self.H.simulasi(p, n - 1, 0, 0)['status'], 'TUNGGU_BELI')
        p['c'] = np.linspace(50, 60, n)                                # naik perlahan: tiada henti tutup hari beli
        p['o'] = p['c'].copy()
        p['l'] = p['c'] * 0.999
        x = self.H.simulasi(p, n - 4, 0, 0)
        self.assertEqual((x['status'], x['sesi']), ('TERBUKA', 3))
        p['X'][0, n - 1] = 1                                           # isyarat keluar pada bar terakhir
        self.assertEqual(self.H.simulasi(p, n - 4, 0, _peraturan(0))['status'], 'JUAL_ESOK')

    def test_takrif_boleh_dibaca_semula(self):
        import cs_cari
        self.assertEqual(self.H.dari_takrif('M84.t7|F23@5+F26|H2|X11 ATAU X21'),
                         {'pencetus': 'M84.t7', 'fs': [22, 25], 'amb': [5.0, None],
                          'lajur': 1 * cs_cari.NR + _peraturan(10, 20, 2)})
        self.assertEqual(self.H.dari_takrif('N73|F16+F23|H4|X07 DAN X21')['lajur'], 3 * cs_cari.NR + _peraturan(6, 20, 3))
        self.assertEqual(self.H.dari_takrif('P13|-|H1|X00'), {'pencetus': 'P13', 'fs': [-1, -1], 'amb': [None, None], 'lajur': 0})


class TestKumpul(unittest.TestCase):
    def test_skor_menyamai_kiraan_terus(self):
        rng = np.random.default_rng(3)
        n, K = 900, 12
        Rm = rng.normal(0.01, 0.08, (n, K)).astype(np.float32)
        tp = rng.integers(0, 2, n)
        Fm = (rng.random((n, 3)) < 0.6).astype(np.uint8)
        f1 = np.array([-1, 0, 0, 2], np.int64)
        f2 = np.array([-1, -1, 1, -1], np.int64)
        S = np.zeros((4, 2, K))
        Q = np.zeros((4, 2, K))
        N2 = np.zeros((4, 2), np.int64)
        teras.kumpul_tambah(Rm[:500], tp[:500], Fm[:500], f1, f2, S, Q, N2)
        teras.kumpul_tambah(Rm[500:], tp[500:], Fm[500:], f1, f2, S, Q, N2)
        tepi = np.round(np.arange(-0.10, 0.1001, 0.001), 4)
        idx, st, stw, hist = teras.kumpul_skor(S, Q, N2, np.array([0, 1, 2, 3]), 50, 3, tepi)
        for ci in range(4):
            m = np.ones(n, bool)
            for f in (f1[ci], f2[ci]):
                if f >= 0:
                    m &= Fm[:, f] > 0
            skor = np.full(K, np.inf)
            for p in (0, 1):
                x = Rm[m & (tp == p)].astype(float)
                self.assertEqual(N2[ci, p], len(x))
                skor = np.minimum(skor, x.mean(0) - 2 * x.std(0) / np.sqrt(len(x)))
            self.assertEqual(idx[ci, 0], int(np.argmax(skor)))
            self.assertAlmostEqual(float(st[ci, 0, 0]), float(skor.max()), places=5)
            self.assertAlmostEqual(float(stw[ci, 0]), float(skor[ci]), places=5)
            self.assertEqual(int(hist[ci].sum()), K)

    def test_gabungan_kurang_n_min_tidak_diskor(self):
        S = np.zeros((1, 2, 4))
        Q = np.zeros((1, 2, 4))
        N2 = np.array([[120, 99]])
        idx, _, _, hist = teras.kumpul_skor(S, Q, N2, np.array([0]), 100, 2, np.array([0.0]))
        self.assertEqual(idx[0].tolist(), [-1, -1])
        self.assertEqual(int(hist.sum()), 0)


class TestRingkas(unittest.TestCase):
    """cs_ringkas: pecahan prasyarat/syarat dan nama pendek (tiada pengiraan baharu)."""

    def test_bahagi(self):
        import cs_ringkas
        self.assertEqual(cs_ringkas.bahagi('F20 >= 30% di bawah puncak 52 minggu DAN F27 rejim QQQ OFF'),
                         ('QQQ OFF', '>= 30% di bawah puncak 52 minggu'))
        self.assertEqual(cs_ringkas.bahagi('F17 RS >= 90 DAN F28 SPY > SMA200'), ('SPY > SMA200', 'RS >= 90'))
        self.assertEqual(cs_ringkas.bahagi('RS >= 95 DAN ATR% >= 4'), ('–', 'RS >= 95 + ATR% >= 4'))
        self.assertEqual(cs_ringkas.bahagi(float('nan')), ('–', '–'))

    def test_pasaran_sepadan_ruang_carian(self):
        import cs_ringkas
        # Tiga penapis peringkat pasaran dalam ruang carian (cs_atom.PENAPIS indeks 25-27).
        for kod, nama in cs_ringkas.PASARAN.items():
            i = int(kod[1:]) - 1
            self.assertIn(i, (25, 26, 27))
            self.assertTrue(str(atom.PENAPIS[i]).startswith(kod + ' '))
            self.assertIn(nama, str(atom.PENAPIS[i]))

    def test_nama_pendek(self):
        import cs_ringkas
        self.assertEqual(cs_ringkas.nama_pendek('M92 CCI-50 (benih M, varian 2: cci_50=91, rma_atr_14=15)'), 'M92 CCI-50 (ditala 2)')
        self.assertEqual(cs_ringkas.nama_pendek('N40 OBV tinggi baharu + MA50 (benih N)'), 'N40 OBV tinggi baharu + MA50')

    def test_registry_semua_dipecah(self):
        import cs_ringkas
        t = cs_ringkas.pembahagian()
        self.assertEqual(t.id.tolist()[:3], ['F01', 'F02', 'F03'])
        lama = t[~t.pusingan.isin(['CS05', 'CS06', 'CS07', 'CS13'])]
        self.assertEqual(len(lama), 38)
        self.assertTrue(set(lama.prasyarat_pasaran) <= {'–', 'QQQ ON', 'QQQ OFF', 'SPY > SMA200'})
        self.assertEqual(int((t.jejak_hadapan == 'ya').sum()), 8)

    def test_rekod_semua_masuk_sepadan_cs03(self):
        """semua_masuk.csv.gz ialah rekod penuh larian CS03 yang sama: bilangan dan skor sepadan dengan meta dan senarai."""
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS03')
        b = pd.read_csv(os.path.join(d, 'semua_masuk.csv.gz'))
        with open(os.path.join(d, 'meta.json')) as f:
            self.assertEqual(len(b), json.load(f)['masuk_diskor'])
        k = pd.read_csv(os.path.join(d, 'senarai_kunci.csv'))
        self.assertAlmostEqual(b.skor.max() / 100, k.skor.max(), places=4)
        self.assertEqual(len(pd.read_csv(os.path.join(d, 'SEMUA_PENCETUS.csv'))), 500)

class TestCS05(unittest.TestCase):
    """SPEC pindaan 14 Nov 2026 (i): lapisan prasyarat, enjin CS05 dan rekodnya."""

    def test_ruang_dikunci(self):
        import cs_cs05 as c5
        import cs_lapis as lapis
        import cs_prasyarat as pr
        self.assertEqual((lapis.N1, lapis.N2, lapis.ANJAK), (33, 15, 437))
        self.assertEqual((c5.NS, c5.NC, c5.NQ1, c5.NQ2, c5.NQ), (27, 379, 34, 16, 544))
        self.assertEqual(500 * c5.NQ * c5.NC, 103_088_000)
        self.assertFalse({25, 26, 27} & set(c5.SAHAM.tolist()))          # penapis pasaran lama berpindah ke prasyarat
        self.assertEqual((c5.N_ATAS, c5.N_KELAS, c5.N_SENARAI, c5.MAKS_PRA, c5.MAKS_TANPA), (2000, 5, 200, 3, 3))
        kod = [x[:4] for x in lapis.PASARAN + lapis.KUMPULAN]
        self.assertEqual(len(set(kod)), 48)
        self.assertTrue(all(k[:2] in ('QA', 'QB', 'QC', 'QG', 'QH') for k in kod[:33]))
        self.assertTrue(all(k[:2] in ('QD', 'QE', 'QF') for k in kod[33:]))
        lama = {x[:3]: x[4:] for x in pr.PRASYARAT}                      # 38 prasyarat (h) dimasukkan tanpa pemilihan
        sama = [x for x in lapis.PASARAN + lapis.KUMPULAN if x[1] != 'H']
        self.assertEqual(len(sama), 38)
        for x in sama:
            self.assertEqual(lama[x[1:4]], x[5:])

    def test_kumpul5_menyamai_kiraan_terus(self):
        import cs_cs05 as c5
        import cs_lapis as lapis
        rng = np.random.default_rng(3)
        n = 400
        tp = rng.integers(0, 2, n)
        V = rng.random((n, 3))
        Fm = (rng.random((n, c5.NS)) < 0.4).astype(np.uint8)
        L1 = (rng.random((n, lapis.N1)) < 0.3).astype(np.uint8)
        L2 = (rng.random((n, lapis.N2)) < 0.3).astype(np.uint8)
        Acc = np.zeros((c5.NQ, c5.NC, 2, 4))
        c5.kumpul5(tp, V, Fm, L1, L2, c5.PASANG, Acc)
        for _ in range(200):
            q1, q2, ci = rng.integers(-1, lapis.N1), rng.integers(-1, lapis.N2), rng.integers(0, c5.NC)
            m = np.ones(n, bool)
            if q1 >= 0:
                m &= L1[:, q1] > 0
            if q2 >= 0:
                m &= L2[:, q2] > 0
            for cc in (c5.C1[ci], c5.C2[ci]):
                if cc >= 0:
                    m &= Fm[:, cc] > 0
            flat = ((q1 + 1) * c5.NQ2 + q2 + 1) * c5.NC + ci
            for p in (0, 1):
                mm = m & (tp == p)
                np.testing.assert_allclose(Acc.reshape(-1, 2, 4)[flat, p], [mm.sum(), *V[mm].sum(axis=0)], atol=1e-9)
            a, b, f1, f2 = c5.nyah(flat)
            self.assertEqual((int(a), int(b)), (q1, q2))
            self.assertEqual(int(f1), -1 if c5.C1[ci] < 0 else int(c5.SAHAM[c5.C1[ci]]))
            self.assertEqual(int(f2), -1 if c5.C2[ci] < 0 else int(c5.SAHAM[c5.C2[ci]]))

    def test_skor_dua_asas(self):
        import cs_cs05 as c5
        import cs_tangkap as tk
        Acc = np.zeros((2, 1, 2, 4))
        Acc[0, 0] = [[200, 40, 20, 10], [100, 15, 9, 5]]                 # n, lari, asas hari, asas era
        Acc[1, 0] = [[99, 40, 1, 1], [500, 100, 1, 1]]                   # kurang 100 dalam era pertama
        ok, sp, sj = c5.skor_acc(Acc)
        self.assertEqual(ok[:, 0].tolist(), [True, False])
        self.assertTrue(np.isnan(sp[1, 0]) and np.isnan(sj[1, 0]))
        self.assertAlmostEqual(sp[0, 0], min(tk.lb_lari(200, 0.20, 0.10), tk.lb_lari(100, 0.15, 0.09)))
        self.assertAlmostEqual(sj[0, 0], min(tk.lb_lari(200, 0.20, 0.05), tk.lb_lari(100, 0.15, 0.05)))

    def _qqq(self):
        lo = np.r_[np.full(300, 100.0), np.linspace(100, 85, 30), [85.5, 86, 86.5, 87, 89.5, 90, 91], np.full(40, 92.0)]
        return lo, lo + 0.5, np.ones(len(lo))

    def test_ftd_hari_keempat_dengan_volum(self):
        import cs_lapis as lapis
        lo, cl, vol = self._qqq()                                        # hari rendah = bar 329; bar 334 naik 2.9 %
        self.assertEqual(int(lapis.ftd(lo, cl, vol).sum()), 0)           # volum tidak lebih tinggi: bukan FTD
        vol[334] = 2.0
        f = lapis.ftd(lo, cl, vol)
        self.assertEqual(np.flatnonzero(f).tolist(), list(range(334, 354)))     # benar 20 sesi dari hari FTD
        vol[334], vol[332] = 1.0, 2.0                                    # kenaikan besar pada sesi ke-3: terlalu awal
        cl[332] = cl[331] * 1.02
        self.assertEqual(int(lapis.ftd(lo, cl, vol).sum()), 0)

    def test_ftd_terbatal_bila_tutup_bawah_rendah(self):
        import cs_lapis as lapis
        lo, cl, vol = self._qqq()
        vol[334] = 2.0
        cl[340], lo[340] = 84.0, 83.5                                    # tutup di bawah rendah hari rendah (85)
        f = lapis.ftd(lo, cl, vol)
        self.assertTrue(f[334:340].all())
        self.assertFalse(f[340:].any())

    def test_pakar_tiada_pandang_hadapan(self):
        import cs_lapis as lapis
        rng = np.random.default_rng(5)
        n = 900
        hu = np.arange(n)

        def bina(m):
            mk = lambda: pd.DataFrame({'close': 100 * np.exp(np.cumsum(rng2.normal(0, 0.012, n)))[:m]}, index=hu[:m])
            rng2 = np.random.default_rng(5)
            q, s = mk(), mk()
            for d in (q, s):
                d['low'] = d.close * 0.99
                d['volume'] = rng2.integers(1e6, 5e6, n)[:m].astype(float)
            h = pd.DataFrame({k: rng2.integers(50, 900, n)[:m].astype(float) for k in ('naik', 'turun', 'n4n', 'n4t')},
                             index=hu[:m])
            return lapis.pakar(q, s, h)

        penuh, pendek = bina(n), bina(700)
        self.assertEqual(sorted(penuh), [f'QH{i:02d}' for i in range(1, 11)])
        for k in penuh:
            np.testing.assert_array_equal(penuh[k].to_numpy()[:700], pendek[k].to_numpy(), err_msg=k)
        self.assertGreater(sum(int(v.sum()) for v in penuh.values()), 0)
        del rng

    def test_plasebo_kekal_bilangan_setiap_saham(self):
        import cs_lapis as lapis
        rng = np.random.default_rng(7)
        a = (rng.random((3, 1500)) < 0.2).astype(np.uint8)
        mula = np.array([0, 600, 1100, 1500])
        b = lapis.anjak_saham(a, mula)
        for t in range(3):
            np.testing.assert_array_equal(a[:, mula[t]:mula[t + 1]].sum(axis=1), b[:, mula[t]:mula[t + 1]].sum(axis=1))
        np.testing.assert_array_equal(b[:, 600:1100], np.roll(a[:, 600:1100], lapis.ANJAK, axis=1))
        self.assertFalse(np.array_equal(a, b))

    def test_kadar5_prasyarat_penapis_dan_satu_posisi(self):
        import cs_cs05 as c5
        N = 200
        pan = {'F': np.zeros((30, N), np.uint8), 'tid': np.zeros(N, np.int32), 'tempoh': np.zeros(N, np.int8),
               'hari': np.arange(N)}
        pan['tempoh'][100:] = 1
        pan['F'][15, :] = 1                                              # F16 benar di mana-mana
        pan['F'][22, 50:] = 1                                            # F23 benar mulai bar 50
        Lr = (np.zeros((33, N), np.uint8), np.zeros((15, N), np.uint8))
        Lr[0][9, 40:] = 1                                                # QA10 benar mulai bar 40
        Lr[1][8, :120] = 1                                               # QF01 benar hingga bar 119
        X = np.zeros((N, 15), np.float32)
        X[:, 4], X[:, 9], X[:, 14] = 1.0, 0.25, 0.125
        ev = np.array([10, 45, 60, 65, 90, 115, 150])
        v = c5.kadar5(pan, X, Lr, ev, -1, -1, -1, -1)                    # 60 dan 65 jatuh dalam pegangan 45 (20 sesi)
        self.assertEqual((v[0]['n'], v[1]['n']), (3, 2))
        v = c5.kadar5(pan, X, Lr, ev, 9, 8, 15, 22)                      # QA10 + QF01 + F16 + F23: bar 60, 90, 115
        self.assertEqual((v[0]['n'], v[0]['hari'], v[1]['n']), (2, 2, 1))
        self.assertAlmostEqual(v[0]['lari'] - v[0]['a_lari'], 0.75)
        self.assertAlmostEqual(v[0]['lari'] - v[0]['e_lari'], 0.875)
        self.assertTrue(np.isnan(c5.skor_tepat(v, 'a_')))                # kurang 100 isyarat: tiada skor

    def test_rekod_cs05(self):
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS05')
        with open(os.path.join(d, 'meta.json')) as f:
            meta = json.load(f)
        self.assertEqual(meta['masuk_dicuba'], 103_088_000)
        self.assertEqual(meta['pencetus'], 500)
        m = pd.read_csv(os.path.join(d, 'SEMUA_PENCETUS.csv'))
        self.assertEqual(len(m), 500)
        self.assertTrue(set(m.kelas.dropna()) <= {'IKUT TREND', 'PANTULAN'})
        p = pd.read_csv(os.path.join(d, 'papan.csv'))
        self.assertEqual(sorted(p.papan.unique()), ['jumlah', 'pilih'])
        for kod in ('pilih', 'jumlah'):
            x = p[p.papan == kod].drop_duplicates('kedudukan')
            self.assertLessEqual(len(x), 10)
            self.assertEqual(x.masuk.str.split(' ').str[0].str.split('.').str[0].nunique(), len(x))   # satu setiap keluarga
            pra = x.prasyarat[x.prasyarat != 'tiada'].str.split(' DAN ').explode()
            self.assertLessEqual(int((x.prasyarat == 'tiada').sum()), 3)
            if len(pra):
                self.assertLessEqual(int(pra.value_counts().max()), 3)

    def test_registry_lajur_prasyarat_dan_kohort_kekal(self):
        bs2 = os.path.join(SINI, '..')
        reg = pd.read_csv(os.path.join(bs2, 'data', 'registry_F.csv'), dtype=str).fillna('')
        self.assertEqual(list(reg.columns)[-6:], ['prasyarat', 'syarat', 'menang_K1', 'menang_K2', 'menang_K3', 'menang'])
        self.assertTrue((reg.prasyarat != '').all() and (reg.syarat != '').all())
        self.assertEqual(reg.id.tolist(), [f'F{i:02d}' for i in range(1, len(reg) + 1)])
        lama = reg[~reg.pusingan.isin(['CS05', 'CS06', 'CS07', 'CS13'])]
        self.assertEqual(len(lama), 38)
        self.assertTrue(set(lama.prasyarat) <= {'tiada', 'QQQ ON', 'QQQ OFF', 'SPY > SMA200'})
        for t in reg[reg.pusingan == 'CS05'].itertuples():
            bhg = t.takrif.split('|')
            self.assertEqual(len(bhg), 4 if t.prasyarat == 'tiada' else 5)
            self.assertEqual(t.status, 'BACKTEST')
        with open(os.path.join(bs2, 'jejak_f', 'kohort.json')) as f:      # pindaan (i): kohort jejak hadapan tidak berubah
            self.assertEqual([a['id'] for a in json.load(f)['ahli']], ['F21', 'F22', 'F34', 'F27', 'F28', 'F38', 'F30', 'F24'])

class TestLengkap(unittest.TestCase):
    """SPEC pindaan 14 Nov 2026 (j): pegang + keluar + henti ikut kadar tangkap yang direalisasi."""

    def test_ambang_dikunci(self):
        import cs_lengkap as lg
        self.assertEqual((lg.JADI, lg.RUGI, lg.K), (0.10, -0.08, 2308))

    def test_tambah_asas_menyamai_kiraan_terus(self):
        import cs_lengkap as lg
        rng = np.random.default_rng(11)
        Rm = rng.normal(0, 0.12, (500, 37)).astype(np.float32)
        g = rng.integers(0, 9, 500)
        m5 = rng.random(500) < 0.4
        TJ, TR, TT = (np.zeros((9, 37), np.uint16) for _ in range(3))
        lg.tambah_asas(Rm, g, m5, TJ, TR, TT)
        R64 = Rm.astype(np.float64)
        for x in range(9):
            np.testing.assert_array_equal(TJ[x], (R64[g == x] >= 0.10).sum(axis=0))
            np.testing.assert_array_equal(TR[x], (R64[g == x] <= -0.08).sum(axis=0))
            np.testing.assert_array_equal(TT[x], (R64[(g == x) & m5] >= 0.10).sum(axis=0))      # pindaan (k): tangkap penuh

    def _pan(self, naik):
        N = 400
        c = 100 * (1 + naik) ** np.arange(N)
        return {'o': c.copy(), 'h': c * 1.001, 'l': c * 0.999, 'c': c, 'atr': np.full(N, 1.0),
                'X': np.zeros((len(atom.KELUAR), N), np.uint8), 'tid': np.zeros(N, np.int32),
                'tempoh': (np.arange(N) >= 200).astype(np.int8), 'hari': np.arange(N)}

    def test_nilai_l_jadi_rugi_dan_asas(self):
        import cs_lengkap as lg
        N, e = 400, np.array([10, 20, 40, 70, 210, 240])           # 20 jatuh dalam pegangan 10 (X00: 20 sesi)
        X = np.zeros((N, 15), np.float32)
        X[40, 4] = 1                                                # satu saham berlabel lari
        X[[10, 40], 0] = 1                                          # dua saham naik >= 5 % minggu pertama
        Tb = {'g': np.zeros(N, np.int32), 'ge': np.zeros(N, np.int32), 'n': np.array([50]),
              'TJ': np.full((1, lg.K), 10, np.uint16), 'TR': np.full((1, lg.K), 5, np.uint16),
              'TT': np.full((1, lg.K), 4, np.uint16), 'TTe': np.full((1, lg.K), 0.05, np.float32),
              'TJe': np.full((1, lg.K), 0.3, np.float32), 'TRe': np.full((1, lg.K), 0.1, np.float32)}
        v = lg.nilai_l(self._pan(0.01), X, e, 0, Tb)                # naik 1 % sehari: tutup sesi 20 = +20.8 % - kos
        self.assertEqual((v[0]['n'], v[1]['n']), (3, 2))
        self.assertEqual((v[0]['k10'], v[0]['rugi8'], v[0]['pegang']), (1.0, 0.0, 20.0))
        self.assertAlmostEqual(v[0]['purata'], 1.01 ** 19 - 1 - 0.005, places=9)
        self.assertEqual((v[0]['n_lari'], v[0]['k10_lari']), (1, 1.0))
        self.assertAlmostEqual(v[0]['a_k10'], 0.2)
        self.assertAlmostEqual(v[0]['a_rugi8'], 0.1)
        self.assertAlmostEqual(v[0]['e_k10'], 0.3, places=6)
        self.assertAlmostEqual(v[0]['tp'], 2 / 3)                   # jadi DAN naik >= 5 % minggu pertama (bar 10 dan 40)
        self.assertAlmostEqual(v[0]['a_tp'], 0.08)
        self.assertAlmostEqual(v[0]['e_tp'], 0.05, places=6)
        v = lg.nilai_l(self._pan(0.0), X, e, 0, Tb)                 # harga rata: R = -kos; tidak jadi, tidak rugi8
        self.assertEqual((v[0]['k10'], v[0]['rugi8']), (0.0, 0.0))
        v = lg.nilai_l(self._pan(-0.01), X, e, 0, Tb)               # turun 1 % sehari: henti -8 % kena
        self.assertEqual((v[0]['k10'], v[0]['rugi8']), (0.0, 1.0))
        self.assertLess(v[0]['pegang'], 20)

    def test_pilih_lajur_memilih_yang_paling_kerap_jadi(self):
        import cs_lengkap as lg
        pan = self._pan(0.01)                                       # naik terus: memegang 20 sesi paling kerap jadi
        pan['X'][0, :] = 1                                          # X01 sentiasa menyala: jual pada buka sesi 2
        e = np.arange(5, 370, 1)
        c = lg.pilih_lajur(pan, e)
        self.assertGreaterEqual(c, 0)
        s, r = divmod(c, NR)
        self.assertFalse(OP[r] == 1 and A1[r] == 0)                 # bukan X01 tunggal (jual awal)
        self.assertFalse(OP[r] == 2 and 0 in (A1[r], A2[r]))        # bukan pasangan ATAU yang mengandungi X01
        self.assertEqual(lg.pilih_lajur(pan, e[:150]), -1)          # era kedua tiada isyarat: tiada pilihan
        m5 = np.ones(len(e), bool)
        self.assertEqual(lg.pilih_lajur(pan, e, m5), c)             # semua naik minggu pertama: pilihan sama
        self.assertGreaterEqual(lg.pilih_lajur(pan, e, ~m5), 0)     # tiada tangkap penuh langsung: masih pulang lajur sah

    def test_rekod_lengkap(self):
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS05')
        m = pd.read_csv(os.path.join(d, 'SEMUA_PENCETUS.csv'))
        for kol in ('pilih_S_jadi', 'pilih_P_jadi', 'jumlah_P_jadi', 'pilih_P_keluar_l', 'pilih_P_asas_jadi'):
            self.assertIn(kol, m.columns)
        self.assertTrue(m.pilih_P_keluar_l.dropna().str.match(r'^H[1-4] · X\d\d').all())
        p = pd.read_csv(os.path.join(d, 'papan.csv'))
        self.assertTrue({'L1', 'L2', 'L_pilih_k10', 'L_x00_k10'} <= set(p.columns))
        for nama in ('SEMUA_PENCETUS_LENGKAP.md', 'TOP50.md'):
            self.assertTrue(os.path.exists(os.path.join(d, nama)))
        reg = pd.read_csv(os.path.join(SINI, '..', 'data', 'registry_F.csv'), dtype=str).fillna('')
        cs5 = reg[reg.pusingan == 'CS05']
        self.assertEqual(cs5.id.tolist(), [f'F{i}' for i in range(39, 58)])      # ID kekal pada peraturan masuk
        x = p.drop_duplicates('id').set_index('id')
        for r in cs5.itertuples():                                              # registry = setup lengkap pindaan (j)
            self.assertEqual(r.takrif, x.takrif[r.id])

class TestCS06(unittest.TestCase):
    """SPEC pindaan 14 Nov 2026 (k): sasaran tangkap penuh dan tala bersama prasyarat."""

    def test_grid_prasyarat_dikunci(self):
        import cs_lapis as lapis
        kod = {x[:4]: x[5:] for x in lapis.PASARAN + lapis.KUMPULAN}
        tetap = {'QA01', 'QA02', 'QA03', 'QA04', 'QB03', 'QG01', 'QG02', 'QG04', 'QH07', 'QH08', 'QH09', 'QF05'}
        self.assertEqual(set(lapis.GRID_PRA), set(kod) - tetap)                 # 36 berambang + 12 tetap = 48
        for k, (grid, asal, templat) in lapis.GRID_PRA.items():
            self.assertIn(asal, grid, k)
            self.assertEqual(grid, sorted(grid), k)
            self.assertEqual(templat.format(f'{asal:g}'), kod[k], k)            # nilai pradaftar (i) menghasilkan teks asal
        self.assertEqual(lapis.GRID_PRA['QF01'][0], [2, 3, 5, 7, 10])
        self.assertEqual(lapis.GRID_PRA['QA06'][0], [5, 7.5, 10, 15, 20, 25])

    def test_ftd_tempoh_aktif_boleh_tala(self):
        import cs_lapis as lapis
        lo = np.r_[np.full(300, 100.0), np.linspace(100, 85, 30), [85.5, 86, 86.5, 87, 89.5, 90, 91],
                   92 + 0.01 * np.arange(40)]                                   # naik perlahan: tiada rendah 20 sesi baharu
        cl, vol = lo + 0.5, np.ones(len(lo))
        vol[334] = 2.0
        for n in (10, 20, 30):
            self.assertEqual(np.flatnonzero(lapis.ftd(lo, cl, vol, n)).tolist(), list(range(334, 334 + n)))

    def test_dataran_n(self):
        import cs_tala6 as t6
        G = np.full((1, 1, 1, 1), 0.03)
        self.assertEqual(t6.dataran_n(G)[0, 0, 0, 0], 0.03)                     # tiada paksi ditala: skor sel itu sendiri
        G = np.array([0.01, 0.09, 0.02, np.nan, 0.05]).reshape(5, 1, 1, 1)
        D = t6.dataran_n(G).ravel()
        self.assertAlmostEqual(D[0], 0.05)                                      # median (0.01, 0.09)
        self.assertAlmostEqual(D[1], 0.02)                                      # puncak 0.09 diratakan oleh jirannya
        self.assertAlmostEqual(D[2], 0.055)                                     # jiran: 0.09, 0.02, nan -> median dua yang ada
        self.assertTrue(np.isnan(D[3]))                                         # sel tanpa skor tidak mendapat markah
        self.assertTrue(np.isnan(D[4]))                                         # hanya 1 daripada 2 sel kotak: kurang 2
        G = np.full((3, 3, 1, 1), np.nan)
        G[1, 1] = 0.2
        G[0, 0] = 0.1
        D = t6.dataran_n(G)[:, :, 0, 0]
        self.assertTrue(np.isnan(D[1, 1]))                                      # tengah: 2 daripada 9 sel, kurang separuh kotak
        self.assertAlmostEqual(D[0, 0], 0.15)                                   # penjuru: 2 daripada 4 sel kotaknya

    def test_paksi_grid_dan_teks(self):
        import collections

        import cs_lapis as lapis
        import cs_tala6 as t6
        R = collections.namedtuple('R', 'q1 q2 f1 f2')
        q1 = [x[:4] for x in lapis.PASARAN].index('QA08')
        q2 = [x[:4] for x in lapis.KUMPULAN].index('QF01')
        pk = t6.Paksi(R(q1, q2, 1, 19))                                         # F02 tutup > MA50 (tetap), F20 jatuh (berambang)
        self.assertEqual(pk.bentuk, (5, 5, 1, 5))
        self.assertEqual(tuple(g[i] for g, i in zip(pk.grid, pk.ii)), (10, 5, None, 30))
        t = pk.teks((10, 5, None, 30))
        self.assertEqual(t['prasyarat'], 'rejim ON baharu (<= 10 sesi) + earnings dalam 1-5 sesi akan datang')
        self.assertEqual(t['syarat'], 'tutup > MA50 + >= 30% di bawah puncak 52 minggu')
        t = pk.teks((20, 3, None, 40))
        self.assertEqual((t['kod_pra'], t['kod_pen']), ('QA08@20+QF01@3', 'F02+F20@40'))
        self.assertEqual(t['prasyarat'], 'rejim ON baharu (<= 20 sesi) + earnings dalam 1-3 sesi akan datang')
        pk = t6.Paksi(R(-1, [x[:4] for x in lapis.KUMPULAN].index('QF05'), -1, -1))      # SUE > 0: tiada ambang
        self.assertEqual(pk.bentuk, (1, 1, 1, 1))
        self.assertEqual(pk.teks((None, None, None, None))['kod_pra'], 'QF05')

    def test_istilah_dan_sasaran(self):
        import cs_cs05 as c5
        self.assertEqual((c5.S_PIAWAI, c5.R_PIAWAI), (3, 0))                    # pegang piawai: H4 + X00
        self.assertIn(c5.SASARAN, ('lari', 'tp'))
        self.assertEqual(c5.istilah('label «lari»'), 'label "lari"')

    def test_rekod_cs06(self):
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS06')
        with open(os.path.join(d, 'meta.json')) as f:
            meta = json.load(f)
        self.assertEqual((meta['pusingan'], meta['sasaran'], meta['masuk_dicuba']), ('CS06', 'tp', 103_088_000))
        m = pd.read_csv(os.path.join(d, 'SEMUA_PENCETUS.csv'))
        self.assertEqual(len(m), 500)
        self.assertIn('pilih_P_tpp', m.columns)                                 # lajur sasaran dinamakan tpp, bukan lari
        self.assertFalse([c for c in m.columns if 'lari' in c])
        p = pd.read_csv(os.path.join(d, 'papan.csv'))
        self.assertEqual(sorted(p.papan.unique()), ['jumlah', 'pilih'])
        t = pd.read_csv(os.path.join(d, 'tala.csv'))
        self.assertEqual(len(t), 20)
        with open(os.path.join(d, 'tala_meta.json')) as f:
            tm = json.load(f)
        self.assertEqual(tm['induk'], 20)
        self.assertEqual(tm['tala_menolong'], bool(tm['anak'] and tm['anak_menang_kedua'] > tm['anak'] / 2))
        teks = open(os.path.join(d, 'LAPORAN.md'), encoding='utf-8').read()
        self.assertNotRegex(teks, r'(?<!")\blari\b(?!")')                       # istilah ditukar; hanya label "lari" CS05 kekal
        reg = pd.read_csv(os.path.join(SINI, '..', 'data', 'registry_F.csv'), dtype=str).fillna('')
        self.assertEqual(reg[reg.pusingan == 'CS05'].id.tolist(), [f'F{i}' for i in range(39, 58)])
        c6 = reg[reg.pusingan == 'CS06']
        self.assertTrue((c6.status == 'BACKTEST').all())
        self.assertTrue(c6.takrif.map(lambda x: len(x.split('|')) in (4, 5)).all())
        self.assertTrue((c6.prasyarat != '').all() and (c6.syarat != '').all())

class TestKadarMenang(unittest.TestCase):
    """Permintaan pengguna 14 Nov 2026: setiap setup F dipaparkan bersama kadar menang (cs_ringkas, registry F)."""

    def setUp(self):
        self.bs2 = os.path.join(SINI, '..')
        self.reg = pd.read_csv(os.path.join(self.bs2, 'data', 'registry_F.csv'), dtype=str).fillna('')
        self.hasil = os.path.join(self.bs2, 'kajian', 'carian_setup', 'hasil')

    def test_setiap_setup_ada_kadar_menang(self):
        m = self.reg.menang.astype(float)
        self.assertTrue(((m > 0) & (m < 1)).all())
        for r in self.reg.itertuples():                                         # gabungan = purata berwajaran bilangan belian
            n = {t: float(getattr(r, f'n_{t}') or 0) for t in ('K1', 'K2', 'K3')}
            x = {t: getattr(r, f'menang_{t}') for t in n}
            jum = sum(n[t] * float(x[t]) for t in n if n[t] and x[t] != '')
            bil = sum(n[t] for t in n if n[t] and x[t] != '')
            self.assertAlmostEqual(float(r.menang), jum / bil, places=3, msg=r.id)

    def test_sepadan_dengan_fail_hasil(self):
        import cs_ringkas
        M = cs_ringkas.kadar_menang()
        d = pd.read_csv(os.path.join(self.hasil, 'CS03', 'papan.csv'))
        x = d[(d.id == 'F27') & (d.tempoh == 'K1')].R_menang.iloc[0]
        self.assertAlmostEqual(M[('CS03', 'F27')]['K1'], x)
        self.assertAlmostEqual(float(self.reg.set_index('id').menang_K1['F27']), x, places=4)
        self.assertEqual({k[0] for k in M}, {'CS01', 'CS02', 'CS03', 'CS04', 'CS05', 'CS06'})

    def test_jadual_kadar_menang(self):
        t = pd.read_csv(os.path.join(self.hasil, 'KADAR_MENANG.csv'))
        self.assertEqual(t.id.tolist(), self.reg.id.tolist())
        self.assertTrue(t.menang.notna().all())
        teks = open(os.path.join(self.hasil, 'KADAR_MENANG.md'), encoding='utf-8').read()
        self.assertEqual(teks.count('\n| `F'), len(self.reg))
        r = t.set_index('id').loc['F27']
        self.assertIn(f"| **{r.menang * 100:.0f}** | {round(r.menang * 10)} / {10 - round(r.menang * 10)} |", teks)
        self.assertEqual(int((t.jejak_hadapan == 'ya').sum()), 8)

class TestPortfolio6(unittest.TestCase):
    """SPEC pindaan 14 Nov 2026 (l): portfolio 10 slot bagi setup berprasyarat."""

    def test_dikunci_dan_takrif(self):
        import cs_lapis as lapis
        import cs_portfolio6 as p6
        self.assertEqual((p6.SETUP, p6.N_SLOT, p6.HAD_MDD, p6.N_ULANG), (['F39', 'F40', 'F58', 'F49'], 10, 0.10, 200))
        self.assertEqual(p6.GABUNGAN, {'PILIH3': ['F39', 'F40', 'F58'], 'SEMUA4': ['F39', 'F40', 'F58', 'F49']})
        d = p6.dari_takrif5('M73.2|F02+F20|H3|X09 DAN X21|QA08+QF01')
        self.assertEqual((d['pencetus'], d['f1'], d['f2']), ('M73.2', 1, 19))
        self.assertEqual(lapis.PASARAN[d['q1']][:4], 'QA08')
        self.assertEqual(lapis.KUMPULAN[d['q2']][:4], 'QF01')
        self.assertEqual(d['lajur'] // NR, 2)                                   # H3
        d = p6.dari_takrif5('N73|F16+F23|H4|X07 DAN X21')                        # tanpa prasyarat
        self.assertEqual((d['q1'], d['q2']), (-1, -1))

    def test_ukur(self):
        import cs_portfolio6 as p6
        r = np.r_[np.full(126, 0.001), [-0.10], np.full(125, 0.001)]
        c, m = p6.ukur(r)
        self.assertAlmostEqual(m, -0.10)
        self.assertAlmostEqual(c, float(np.prod(1 + r) - 1))                    # 252 sesi = setahun

    def test_rekod_portfolio(self):
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS06')
        t = pd.read_csv(os.path.join(d, 'portfolio.csv'))
        self.assertEqual(t.setup.tolist(), ['F39', 'F40', 'F58', 'F49', 'PILIH3', 'SEMUA4'])
        self.assertTrue((t.diambil <= t.isyarat).all())
        for r in t.itertuples():                                                # bacaan dikunci pindaan (l)
            self.assertEqual(bool(r.menambah), bool(r.cagr_had > 0 and r.cagr_had > r.rawak95_cagr_had))
        self.assertTrue(os.path.exists(os.path.join(d, 'PORTFOLIO.md')))


class TestAkhir(unittest.TestCase):
    """SPEC pindaan 14 Nov 2026 (m): kedudukan akhir semua setup F lawan matlamat."""

    def test_dikunci(self):
        import cs_akhir as ak
        self.assertEqual((ak.MIN_BELIAN, ak.MIN_TAHUN, ak.JARAK_EPISOD, ak.KUNCI), (300, 10, 5, ('K1', 'K2', 'K3')))

    def test_label2(self):
        import cs_akhir as ak
        n = teras.TMAX + 2

        def siri(c5, c20, rendah=None):
            c = np.full(n, 100.0)
            c[5:] = c5                                                          # bar beli = 1; sesi 5 = bar 5
            c[teras.TMAX] = c20                                                 # sesi 20 = bar TMAX
            o, lo = c.copy(), c.copy()
            o[1] = 100.0
            if rendah is not None:
                lo[10] = rendah
            return o, lo, c
        ev = np.array([0])
        for (c5, c20, rendah), (m10, terus) in {(106.0, 108.0, None): (0, 1),    # +6 % minggu 1, naik lagi
                                                (111.0, 120.0, None): (1, 1),    # +11 % minggu 1, naik lagi
                                                (106.0, 105.0, None): (0, 0),    # tidak naik lagi selepas minggu 1
                                                (104.0, 130.0, None): (0, 0),    # minggu 1 < 5 %
                                                (106.0, 108.0, 91.0): (0, 0)}.items():   # henti -8 % kena
            o, lo, c = siri(c5, c20, rendah)
            r = ak.label2(ev, o, lo, c)[0]
            self.assertEqual((int(r[0]), int(r[1])), (m10, terus), (c5, c20, rendah))
            self.assertAlmostEqual(float(r[2]), max(c5, c20) / 100.0 - 1, places=5)

    def test_episod(self):
        import cs_akhir as ak
        lab = np.zeros(40, bool)
        lab[[2, 3, 4, 8, 20, 38]] = True                                        # saham 1: bar 0-29; saham 2: bar 30-39
        ep, k = ak.episod(lab, np.array([0, 30, 40]))
        self.assertEqual(k, 3)                                                  # 2-8 digabung (jarak < 5), 20, 38
        self.assertEqual(ep[[2, 3, 4, 8]].tolist(), [0, 0, 0, 0])
        self.assertEqual((int(ep[20]), int(ep[38]), int(ep[5])), (1, 2, -1))
        lab[:] = False
        lab[[29, 30]] = True                                                    # bersebelahan tetapi saham berlainan
        self.assertEqual(ak.episod(lab, np.array([0, 30, 40]))[1], 2)

    def test_rekod_kedudukan(self):
        import cs_akhir as ak
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil')
        t = pd.read_csv(os.path.join(d, 'KEDUDUKAN_AKHIR.csv'))
        reg = pd.read_csv(os.path.join(SINI, '..', 'data', 'registry_F.csv'), dtype=str)
        mahu = [i for i, p in zip(reg.id, reg.pusingan) if p == 'CS07' or (p != 'CS04' and int(i[1:]) <= 69)]
        self.assertEqual(sorted(t.id), sorted(mahu))                            # F01-F30, F39-F69 dan setup CS07
        self.assertTrue(t[t.pusingan == 'CS07'].dipercayai.all())               # penjelasan (n)-2: hanya yang dipercayai didaftarkan
        self.assertTrue(t.jual_awal.between(0, 0.5).all())                      # pindaan (p): lajur jualan sebelum sesi ke-4 (henti rugi)
        self.assertLess(float(t[t.dipercayai].jual_awal.median()), 0.05)
        self.assertEqual(t.kedudukan.tolist(), list(range(1, len(t) + 1)))
        for r in t.itertuples():                                                # takrif "dipercayai" dikunci pindaan (m)
            self.assertEqual(bool(r.dipercayai), bool(r.belian >= ak.MIN_BELIAN and r.tahun_aktif >= ak.MIN_TAHUN
                                                      and min(r.kl_K1, r.kl_K2, r.kl_K3) > 0), r.id)
            self.assertLessEqual(r.terus, r.m5 + 1e-9)                          # naik lagi sebahagian daripada naik >= 5 %
            self.assertLessEqual(r.m10, r.m5 + 1e-9)
        n = int(t.dipercayai.sum())
        self.assertTrue(t.dipercayai[:n].all())                                 # dipercayai dahulu
        for blok in (t[:n], t[n:]):                                             # kemudian ikut kadar naik lagi
            self.assertTrue((np.diff(blok.terus) <= 1e-9).all())
        self.assertTrue(os.path.exists(os.path.join(d, 'KEDUDUKAN_AKHIR.md')))


class TestCS07(unittest.TestCase):
    """SPEC pindaan 14 Nov 2026 (n): keluarga pencetus berparameter, enjin keluar baharu, mesin berkala."""

    def test_grid_keluarga_dan_asal(self):
        import cs_param as kp
        G = kp.grid()
        self.assertEqual((len(G), len({x[0] for x in G}), len({x[1] for x in G})), (656, 656, 25))
        self.assertEqual(tuple(sorted({x[1] for x in G})), kp.KELUARGA)
        asal = kp.asal()
        self.assertEqual(len(asal), 41)
        g = _saham(700, 3)
        rs = pd.Series(np.random.default_rng(1).uniform(0, 100, len(g)), index=g.index).rolling(5).mean()
        on = pd.Series(1.0, index=g.index)
        M = kp.kira(g, rs, G)
        P = atom.indikator(g, rs, on, on)[0]
        nama = [x[0] for x in G]
        for k, a in asal.items():                                               # ahli asal = pencetus P asal, tepat
            if a.startswith('P'):
                self.assertTrue((M[nama.index(k)] == P[a]).all(), (k, a))

    def test_keluarga_tiada_pandang_hadapan(self):
        import cs_param as kp
        g = _saham(600, 5)
        rs = pd.Series(np.random.default_rng(2).uniform(0, 100, len(g)), index=g.index)
        G = kp.grid()
        penuh, potong = kp.kira(g, rs, G), kp.kira(g.iloc[:520], rs.iloc[:520], G)
        self.assertTrue((penuh[:, :520] == potong).all())
        rng = np.random.default_rng(9)
        Gr = [(f'{f}.r', f, kp.rawak(f, rng)) for f in kp.KELUARGA for _ in range(3)]
        self.assertTrue((kp.kira(g, rs, Gr)[:, :520] == kp.kira(g.iloc[:520], rs.iloc[:520], Gr)).all())
        self.assertTrue(all(isinstance(kp.teks(f, p), str) for _, f, p in Gr))

    def test_atom_keluar_dan_peraturan(self):
        import cs_keluar7 as k7
        self.assertEqual((k7.NA, int((k7.JENIS == 0).sum()), k7.NR, k7.NG, k7.NH), (97, 78, 9410, 3, 8))
        self.assertEqual((k7.N_SEJAGAT, k7.SIMPAN_MIN), (30, 0.90))
        self.assertEqual(len({a[0] for a in k7.ATOM}), 97)
        self.assertEqual(k7.kod_peraturan(0), 'X00')
        g = _saham(500, 7)
        self.assertEqual(k7.siri(g).shape, (78, 500))
        self.assertTrue((k7.siri(g)[:, :430] == k7.siri(g.iloc[:430])).all())      # tiada pandang hadapan
        teks = [a[3] for a in k7.ATOM]                                          # setiap atom lama ada dalam ruang baharu
        for t in ('tutup < MA10', 'MA10 < MA20', 'RSI14 silang turun bawah 70', 'Supertrend(10, 3.0) turun',
                  'Chandelier 3.0xATR14 dari tutup tertinggi', 'tutup < 92% tutup tertinggi sejak beli', '+DI14 < -DI14'):
            self.assertIn(t, teks)

    def _pan7(self):
        import cs_keluar7 as k7
        g = _saham(420, 11)
        rs = pd.Series(50.0, index=g.index)
        on = pd.Series(1.0, index=g.index)
        P, F, X, atr = atom.indikator(g, rs, on, on)
        pan = {k: g[n].to_numpy(float) for k, n in (('o', 'open'), ('h', 'high'), ('l', 'low'), ('c', 'close'))}
        pan['atr'] = atr
        pan['X'] = np.stack([X[n[:3]] for n in atom.KELUAR]).astype(np.uint8)
        return pan, k7.siri(g).astype(np.uint8), np.arange(260, 380)

    def test_kernel_keluar_pariti_enjin_lama(self):
        import cs_keluar7 as k7
        pan, XA, ev = self._pan7()
        S = k7.sedia_pan(pan, XA, ev, pegang_min=1)                 # tanpa pegang minimum = enjin lama
        teks = [a[3] for a in k7.ATOM]
        for lama, baharu in ((0, 'tutup < MA10'), (8, 'MACD(12,26,9) < isyarat'), (13, 'Supertrend(10, 3.0) turun'),
                             (17, 'Chandelier 3.0xATR14 dari tutup tertinggi'), (19, 'tutup < 92% tutup tertinggi sejak beli'),
                             (21, 'hari turun dengan volum >= 1.5x')):
            for s_lama, s_baharu in ((0, 0), (1, 1), (2, 4), (3, 5)):
                Ro = teras.hasil_satu(ev, pan['o'], pan['h'], pan['l'], pan['c'], pan['atr'], pan['X'], JENIS, PAR,
                                      A1, A2, OP, s_lama, _peraturan(lama))[0]
                Rn = k7.hasil(*S[:7], k7.A1, k7.A2, k7.OP, s_baharu, (1 + teks.index(baharu)) * k7.NG)[0]
                self.assertTrue(np.allclose(Ro, Rn), (baharu, s_lama))
        Ro = teras.hasil_satu(ev, pan['o'], pan['h'], pan['l'], pan['c'], pan['atr'], pan['X'], JENIS, PAR, A1, A2, OP, 3, 0)[0]
        self.assertTrue(np.allclose(Ro, k7.hasil(*S[:7], k7.A1, k7.A2, k7.OP, 5, 0)[0]))          # X00, 4xATR14

    def test_syarat_aktif_dan_kumpul(self):
        import cs_keluar7 as k7
        pan, XA, ev = self._pan7()
        S = k7.sedia_pan(pan, XA, ev)
        M, ARM = S[0], S[1]
        self.assertTrue(((ARM[:, 1] & ~ARM[:, 0]) == 0).all())                  # aktif +10 % sebahagian daripada aktif +5 %
        r = 1 + [a[3] for a in k7.ATOM].index('tutup < MA10')
        R0, s0 = k7.hasil(*S[:7], k7.A1, k7.A2, k7.OP, 5, r * k7.NG)
        R2, s2 = k7.hasil(*S[:7], k7.A1, k7.A2, k7.OP, 5, r * k7.NG + 2)
        self.assertTrue((s2 >= s0).all())                                       # syarat aktif hanya melewatkan keluar
        tiada = ARM[:, 1] == 0                                                  # tidak pernah +10 %: sama seperti X00
        self.assertTrue(np.allclose(R2[tiada], k7.hasil(*S[:7], k7.A1, k7.A2, k7.OP, 5, 0)[0][tiada]))
        Acc = k7.kumpul(*S, np.zeros(len(ev), np.int64), 1, k7.A1, k7.A2, k7.OP)
        self.assertEqual(Acc.shape, (k7.NH, k7.NKOL, 1, k7.NST))
        self.assertTrue((Acc[..., 0] == len(ev)).all())
        self.assertAlmostEqual(float(Acc[5, r * k7.NG, 0, 5]), float(R0.sum()), places=3)
        self.assertAlmostEqual(float(Acc[5, r * k7.NG, 0, 2]), float((R0 >= 0.10).sum()))
        lab = S[7]
        self.assertTrue((lab[:, 1] <= lab[:, 0]).all())                         # terus sebahagian daripada m5

    def test_pegang_minimum(self):
        import cs_keluar7 as k7
        self.assertEqual(k7.PEGANG_MIN, 3)                                      # dikunci pindaan (p)
        pan, XA, ev = self._pan7()
        S, S1 = k7.sedia_pan(pan, XA, ev), k7.sedia_pan(pan, XA, ev, pegang_min=1)
        self.assertTrue(((S[0] & 3) == 0).all())                                # tiada bit indikator bagi tutup sesi 1 dan 2
        self.assertTrue(((S1[0] & ~3) == S[0]).all())
        for kol in (k7.NG * 5, k7.NG * 40, k7.NG * 90):
            R, sk = k7.hasil(*S[:7], k7.A1, k7.A2, k7.OP, 5, kol)
            R1, sk1 = k7.hasil(*S1[:7], k7.A1, k7.A2, k7.OP, 5, kol)
            henti = S[2][:, 5]                                                  # indeks sesi henti (99 = tiada)
            awal = sk < 3                                                       # dijual sebelum buka sesi ke-4
            self.assertTrue((sk >= 1).all())                                    # tiada jualan pada hari beli
            self.assertTrue(((henti[awal] == sk[awal]) | S[4][awal, 5]).all())  # jualan awal hanya kerana henti rugi
            self.assertTrue((sk >= np.minimum(sk1, 3)).all())                   # tidak pernah lebih awal daripada enjin lama
            self.assertTrue((sk[~awal] >= 3).all())

    def test_rekod_cs07(self):
        import cs_cs07 as c7
        import cs_keluar7 as k7
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS07')
        P = pd.read_csv(os.path.join(d, 'tala_masuk.csv'))
        pas = P[P.ibu.notna() & ~P.sama & P.kl_anak.notna() & P.kl_ibu.notna()]
        self.assertGreater(len(pas), 100)
        self.assertGreater(int((pas.kl_anak > pas.kl_ibu).sum()), len(pas) / 2)  # bacaan dikunci (n)(a): tala menolong
        self.assertGreater(float((pas.kl3_anak - pas.kl3_ibu).median()), 0)
        K = pd.read_csv(os.path.join(d, 'keluar.csv'))
        L = K[K.tp_lama.notna()]
        menolong = int(((L.tp_pilih > L.tp_x00) & (L.tp_pilih > L.tp_lama)).sum())
        self.assertLessEqual(menolong, len(L) / 2)                              # bacaan dikunci (n)(b): keluar TIDAK menolong
        self.assertTrue(set(K.henti) <= set(k7.HENTI))
        pb = pd.read_csv(os.path.join(d, 'papan_masuk.csv'))
        self.assertLessEqual(len(pb), 12)
        reg = pd.read_csv(os.path.join(SINI, '..', 'data', 'registry_F.csv'), dtype=str).fillna('')
        r7 = reg[reg.pusingan == 'CS07']
        self.assertEqual(len(r7), 8)
        self.assertEqual(r7.id.tolist(), [f'F{n}' for n in range(88, 96)])
        for tk in r7.takrif:                                                    # takrif CS07 boleh dihurai dan dijana semula
            x = c7.dari_takrif7(tk)
            self.assertEqual(c7.takrif7(x['pencetus'], x['q1'], x['q2'], x['f1'], x['f2'], x['s'], x['kol']), tk)
        self.assertEqual(reg.id.tolist()[:87], [f'F{n:02d}' for n in range(1, 88)])   # F lama kekal

    def test_mesin_kelompok_tetap(self):
        import cs_mesin as ms
        import cs_tala7 as t7
        G1, T1 = ms.kelompok(3, n_m=5)
        G2, T2 = ms.kelompok(3, n_m=5)
        self.assertEqual((G1, T1), (G2, T2))                                    # benih = nombor larian
        self.assertEqual((len(G1), ms.N_K, ms.N_NILAI_B), (25 * 12, 12, 15))
        self.assertNotEqual(ms.kelompok(4, n_m=5)[0], G1)
        self.assertTrue(all(t[0].endswith(f'.{ms.V_ASAS + 3}') and t[2] for t in T1))
        self.assertEqual((t7.induk('K07.012'), t7.induk('M73.5s3'), t7.induk('N16')), ('K07', 'M73', 'N16'))
        self.assertEqual((len(t7.varian_m1()), t7.V_RAWAK, t7.N_M_SETEMPAT, t7.N_SETEMPAT), (1072, tuple(range(3, 11)), 50, 8))


class TestCS08(unittest.TestCase):
    """SPEC pindaan 14 Nov 2026 (q): lorong kedua (beli selepas pengesahan uptrend, pegang sampai trend tamat)."""

    def test_dikunci(self):
        import cs_trend8 as t8
        self.assertEqual((t8.H_MAX, t8.NAIK, t8.NAIK2, t8.JATUH, t8.TB), (126, 0.50, 1.00, 0.15, 0.30))
        self.assertEqual((t8.NA, t8.NH, t8.NG, t8.NKOL), (38, 6, 3, 115))
        self.assertEqual((t8.N_PAPAN, t8.MAKS_INDUK, t8.MAKS_PRA, t8.N_SEJAGAT, t8.MIN_BELIAN, t8.MIN_TAHUN), (12, 2, 3, 10, 200, 8))
        self.assertEqual(t8.PEGANG_MIN, 3)
        self.assertEqual(len({a[0] for a in t8.ATOM}), 38)

    def test_label_besar(self):
        import cs_trend8 as t8
        n = t8.H_MAX + 3
        c = np.full(n, 100.0)
        o = c.copy()
        ev = np.array([0])
        c1 = c.copy(); c1[60:] = 155.0                                          # +55 % tanpa jatuh dahulu
        c2 = c.copy(); c2[10] = 84.0; c2[60:] = 160.0                           # jatuh -16 % dahulu: bukan pelari besar
        c3 = c.copy(); c3[40:] = 210.0                                          # +110 %
        for cc, (b50, b100) in ((c1, (1, 0)), (c2, (0, 0)), (c3, (1, 1))):
            r = t8.label8(ev, o, cc)[0]
            self.assertEqual((int(r[0]), int(r[1])), (b50, b100))
        self.assertAlmostEqual(float(t8.label8(ev, o, c3)[0, 2]), 1.10, places=5)

    def test_kernel_keluar_lawan_kiraan_kasar(self):
        import cs_trend8 as t8
        rng = np.random.default_rng(5)
        n = 520
        c = 50 * np.exp(np.cumsum(rng.normal(0.001, 0.03, n)))
        o = c * (1 + rng.normal(0, 0.006, n))
        g = pd.DataFrame({'open': o, 'high': np.maximum(o, c) * 1.006, 'low': np.minimum(o, c) * 0.994, 'close': c,
                          'volume': rng.integers(2e5, 3e6, n).astype(float)}, index=pd.bdate_range('2019-01-02', periods=n))
        k1 = pd.Series(1.0, index=g.index)
        atr = atom.indikator(g, k1 * 50, k1, k1)[3]
        lo = g.low.to_numpy()
        XT = t8.siri(g).astype(np.uint8)
        self.assertTrue((t8.siri(g)[:, :450] == t8.siri(g.iloc[:450])).all())      # tiada pandang hadapan
        ev = np.arange(260, 380)
        R, SK = t8._hasil({'o': o, 'l': lo, 'c': c, 'atr': atr}, XT, ev)

        def kasar(i, s, kol):
            e = i + 1
            P = o[e]
            L = [P * .9, P * .85, P * .8, P - 4 * atr[i], P - 6 * atr[i], min(P * .85, P - 5 * atr[i])][s]
            if c[e] <= L:
                return o[e + 1] / P - 1 - t8.KOS, 1
            hc = c[e]
            a, gk = divmod(kol - 1, t8.NG) if kol else (None, None)
            for d in range(t8.H_MAX):
                b = e + d
                if d >= 1 and o[b] <= L:
                    return o[b] / P - 1 - t8.KOS, d
                if d >= 1 and lo[b] <= L:
                    return L / P - 1 - t8.KOS, d
                hc = max(hc, c[b])
                if kol and 2 <= d <= t8.H_MAX - 2:
                    j = t8.JENIS[a]
                    ya = (XT[t8.BARIS[a], b] != 0 if j == 0 else c[b] < hc - t8.PAR[a] * atr[b] if j == 1
                          else c[b] < t8.PAR[a] * hc if j == 2 else (d + 1 >= t8.PAR[a] and c[b] < P))
                    if ya and (gk == 0 or hc >= P * (1.10 if gk == 1 else 1.20)):
                        return o[b + 1] / P - 1 - t8.KOS, d + 1
            return c[e + t8.H_MAX - 1] / P - 1 - t8.KOS, t8.H_MAX - 1
        for s, kol in [(0, 0), (1, 1), (2, 5), (3, 40), (4, 77), (5, 100), (1, 114), (0, 60)]:
            for k in range(0, len(ev), 9):
                r, sk = kasar(int(ev[k]), s, kol)
                self.assertAlmostEqual(r, float(R[k, s, kol]), places=5, msg=(s, kol, k))
                self.assertEqual(sk, int(SK[k, s, kol]), (s, kol, k))
        self.assertTrue((SK >= 1).all())                                        # tiada jualan pada hari beli
        self.assertTrue(((SK[:, :, 1:] < 3) == (SK[:, :, :1] < 3)).all())       # sebelum sesi ke-4 hanya henti rugi

    def test_rekod_cs08(self):
        import cs_trend8 as t8
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS08')
        D = pd.read_csv(os.path.join(d, 'papan.csv'))
        self.assertEqual(D.id.tolist(), [f'T{i:02d}' for i in range(1, 13)])
        for r in D.itertuples():                                                # takrif Dipercayai-T dikunci pindaan (q)
            self.assertEqual(bool(r.dipercayai), bool(r.n >= t8.MIN_BELIAN and r.tahun >= t8.MIN_TAHUN
                                                      and min(r.kl_K1, r.kl_K2, r.kl_K3) > 0), r.id)
            self.assertLessEqual(r.besar100, r.besar + 1e-9)
            self.assertIn(r.henti, t8.HENTI)
        self.assertGreaterEqual(int(D.dipercayai.sum()), len(D) / 2)            # bacaan dikunci: lorong trend ada kelebihan
        self.assertLessEqual(int((D.tb_semua > D.tb_semua_x00).sum()), len(D) / 2)   # keluar TIDAK menolong
        self.assertTrue(os.path.exists(os.path.join(d, 'LAPORAN.md')))


class TestCS09(unittest.TestCase):
    """SPEC pindaan 15 Nov 2026 (r): keluar daripada maklumat yang belum dicuba (pasaran, sektor, earnings, relatif,
    kemuncak, laluan)."""

    def test_ruang_dikunci(self):
        import collections

        import cs_keluar7 as k7
        import cs_keluar9 as k9
        self.assertEqual(dict(collections.Counter(a[1] for a in k9.ATOM9)), {'P': 22, 'S': 2, 'E': 10, 'R': 5, 'K': 17, 'L': 24})
        self.assertEqual((k9.NB, k9.NL, k9.N_SIRI, k9.NR, k9.NH * k9.NKOL), (80, 97, 56, 21922, 526128))
        self.assertEqual((k9.N_SEJAGAT, k9.SIMPAN_MIN, k9.TP_LONGGAR, k9.N_K3_MIN), (30, 0.90, 0.005, 30))
        self.assertEqual(len({a[0] for a in k9.ATOM9}), 80)
        self.assertFalse({a[5] for a in k9.ATOM9} & {a[3] for a in k7.ATOM})        # tiada atom baharu yang sudah ada dalam CS07
        self.assertEqual(k9.kod_peraturan(0), 'X00')
        self.assertEqual(k9.kod_peraturan(k9.KOL_ARAS), 'Y08.10 ATAU Y09.4@10')    # penanda aras = keluar sejagat terbaik CS07
        self.assertEqual(k9.HENTI[k9.S_ARAS], '5xATR14')
        op = collections.Counter(k9.OP.tolist())
        self.assertEqual((op[0], op[1]), (1, 80))
        lama = (k9.A1 < k9.NL) & (k9.A2 < k9.NL) & (k9.OP > 0)                      # lama x lama: hanya penanda aras
        self.assertEqual(int(lama.sum()), 1)
        self.assertEqual(k9.kelas_peraturan(k9.KOL_ARAS), 'lama')

    def _data(self):
        import cs_keluar9 as k9
        g = _saham(420, 21)
        rng = np.random.default_rng(4)
        XB = (rng.random((k9.N_SIRI + 1, len(g))) < 0.15).astype(np.uint8)
        return g, XB, np.arange(260, 380, 3).astype(np.int64)

    def test_kernel_atom_baharu_menyamai_kiraan_naif(self):
        import cs_keluar9 as k9
        g, XB, ev = self._data()
        o, l, c = (g[n].to_numpy(float) for n in ('open', 'low', 'close'))
        atr = c * 0.03
        for pm in (1, 3):
            M = k9.sedia_baharu(ev, o, l, c, atr, XB, k9.JENIS9, k9.PAR9, k9.PAR29, k9.BARIS9, k9.N_SIRI, pm)
            for k, i in enumerate(ev):
                e = i + 1
                P = o[e]
                for a, (_, _, j, par, par2, _, _) in enumerate(k9.ATOM9):
                    m = 0
                    for d in range(k9.TMAX - 1):
                        b = e + d
                        seg = c[e:b + 1]
                        hc, dh = seg.max(), int(np.argmax(seg))
                        ya = (XB[k9.BARIS9[a], b] != 0 if j == 0 else d - dh >= par if j == 4
                              else (hc > P and c[b] <= P + (1 - par) * (hc - P)) if j == 5
                              else (d + 1 >= par and c[b] < P * (1 + par2)) if j == 6
                              else (hc >= P * (1 + par) and c[b] < P * (1 + par2)) if j == 7
                              else (d > dh and c[b] < l[e + dh]) if j == 8
                              else XB[k9.N_SIRI, e:b + 1].sum() >= par if j == 9
                              else c[b] < hc - (par if d + 1 <= 10 else par2) * atr[b])
                        if ya and d >= pm - 1:
                            m |= 1 << d
                    self.assertEqual(m, int(M[k, a]), (pm, k, a))
            if pm == 3:
                self.assertTrue(((M & 3) == 0).all())                           # pegang minimum: tiada bit sesi 1 dan 2

    def test_bahagian_lama_sama_dengan_cs07_dan_penanda_aras(self):
        import cs_keluar7 as k7
        import cs_keluar9 as k9
        g, XB, ev = self._data()
        pan = {k: g[n].to_numpy(float) for k, n in (('o', 'open'), ('h', 'high'), ('l', 'low'), ('c', 'close'))}
        pan['atr'] = pan['c'] * 0.03
        XA = k7.siri(g).astype(np.uint8)
        S7, S9 = k7.sedia_pan(pan, XA, ev), k9.sedia_pan(pan, XA, XB, ev)
        self.assertEqual(S9[0].shape, (len(ev), 177))
        self.assertTrue((S9[0][:, :97] == S7[0]).all())
        for a, b in zip(S7[1:], S9[1:]):
            self.assertTrue(np.array_equal(a, b))
        kod = [k7.kod_peraturan(r * k7.NG) for r in range(k7.NR)]
        r7 = kod.index('Y08.10 ATAU Y09.4')
        for s in (0, 5, 6):                                                     # penanda aras dalam ruang baharu = peraturan CS07
            self.assertTrue(np.allclose(k7.hasil(*S7[:7], k7.A1, k7.A2, k7.OP, s, r7 * k7.NG + 2)[0],
                                        k7.hasil(*S9[:7], k9.A1, k9.A2, k9.OP, s, k9.KOL_ARAS)[0]))
            self.assertTrue(np.allclose(k7.hasil(*S7[:7], k7.A1, k7.A2, k7.OP, s, 0)[0],
                                        k7.hasil(*S9[:7], k9.A1, k9.A2, k9.OP, s, 0)[0]))

    def test_siri_tiada_pandang_hadapan(self):
        import cs_keluar9 as k9
        g = _saham(500, 13)
        self.assertEqual(k9.siri_k(g).shape, (18, 500))
        self.assertTrue((k9.siri_k(g)[:, :430] == k9.siri_k(g.iloc[:430])).all())
        q = _saham(500, 14)
        b50 = pd.Series(np.random.default_rng(3).uniform(0.2, 0.8, 500)).rolling(5).mean()
        S = k9.siri_qqq(q.close.reset_index(drop=True), q.low.reset_index(drop=True), b50)
        S2 = k9.siri_qqq(q.close.iloc[:430].reset_index(drop=True), q.low.iloc[:430].reset_index(drop=True), b50.iloc[:430])
        self.assertEqual(len(S), 11)
        for k in S:
            self.assertTrue((S[k][:430] == S2[k]).all(), k)

    def test_siri_earnings(self):
        import cs_keluar9 as k9
        n = 60
        c = np.full(n, 100.0)
        o = c.copy()
        c[30], o[30] = 94.0, 97.0                                               # sesi reaksi: tutup -6 %, tutup < buka
        c[31:] = 95.0
        tarikh = (20240101 + np.arange(n)).astype(np.int32)                     # "tarikh" berturutan (ujian sahaja)
        pan = {'o': o, 'c': c, 'tarikh': tarikh, 'mula': np.asarray([0, n]), 'ticker': np.asarray(['AAA'])}
        # pemfailan pada hari indeks 29 selepas tutup (lewat) -> sesi reaksi = indeks 30
        E = k9.earnings_siri(pan, {'AAA': (np.asarray([int(tarikh[29])]), np.asarray([True]))})
        kod = {a[5]: a[0] for a in k9.ATOM9 if a[1] == 'E'}
        esok = E[kod['earnings pada sesi berikutnya (jual sebelum laporan)']]
        self.assertEqual(np.flatnonzero(esok).tolist(), [29])
        r5 = E[kod['reaksi earnings terakhir (0-5 sesi lalu) <= -5%']]
        self.assertEqual(np.flatnonzero(r5).tolist(), list(range(30, 36)))
        self.assertEqual(np.flatnonzero(E[kod['hari reaksi earnings (0-5 sesi lalu) tutup < buka']]).tolist(), list(range(30, 36)))
        self.assertEqual(np.flatnonzero(E[kod['0-10 sesi selepas earnings DAN tutup < tutup sebelum earnings']]).tolist(),
                         list(range(30, 41)))
        self.assertEqual(np.flatnonzero(E[kod['3 hingga 10 sesi selepas reaksi earnings']]).tolist(), list(range(33, 41)))
        self.assertFalse(E[kod['reaksi earnings terakhir (0-5 sesi lalu) <= 0%']][:30].any())   # tiada apa sebelum reaksi

    def test_bacaan_dikunci(self):
        import cs_keluar9 as k9
        n = 10
        asas = dict(n_K3=np.full(n, 50), tp_x00T=0.10, tp_aras7=0.11, simpan_T=0.95, rugi8_T=0.20, rugi8_aras7=0.20,
                    tp_K3_T=0.12, tp_K3_x00T=0.10, pur_R=0.03, pur_x00R=0.02, rugi8_R=0.18, rugi8_x00R=0.20, tp_R=0.10,
                    tp_x00R=0.10, simpan_R=0.95, pur_K3_R=0.03, pur_K3_x00R=0.02)
        T = pd.DataFrame({**asas, 'tp_T': [0.12] * 6 + [0.105] * 4})            # 6/10 mengatasi X00 DAN penanda aras
        B = k9.bacaan(T)
        self.assertEqual((B['n1'], B['atas_x00'], B['atas_aras7'], B['ya1'], B['n2'], B['ya2']), (6, 10, 6, True, 10, True))
        self.assertFalse(k9.bacaan(T.assign(tp_T=[0.12] * 5 + [0.105] * 5))['ya1'])     # tepat separuh tidak cukup
        self.assertFalse(k9.bacaan(T.assign(simpan_T=0.85))['ya1'])                     # jual awal
        self.assertFalse(k9.bacaan(T.assign(tp_K3_T=0.10))['ya1'])                      # tiada tambahan pada 2025-26
        self.assertFalse(k9.bacaan(T.assign(rugi8_T=0.22))['ya1'])                      # rugi naik lebih 1 mata
        self.assertFalse(k9.bacaan(T.assign(rugi8_R=0.20))['ya2'])                      # rugi tidak turun
        self.assertFalse(k9.bacaan(T.assign(tp_R=0.09))['ya2'])                         # tangkap penuh dikorbankan
        self.assertFalse(k9.bacaan(T.assign(pur_K3_R=0.02))['ya2'])

    def test_rekod_cs09(self):
        import cs_keluar9 as k9
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS09')
        T = pd.read_csv(os.path.join(d, 'keluar.csv'))
        ids = pd.read_csv(os.path.join(d, '..', 'KEDUDUKAN_AKHIR.csv')).id.tolist()
        self.assertEqual(sorted(T.id), sorted(ids))                             # semua setup kedudukan akhir dinilai
        self.assertTrue(set(T.henti_T) | set(T.henti_R) <= set(k9.HENTI))
        B = k9.bacaan(T)
        self.assertFalse(B['ya1'])                                              # bacaan dikunci (r) 1: keluar baharu TIDAK menolong
        self.assertFalse(B['ya2'])                                              # bacaan dikunci (r) 2: potong rugi TIDAK menolong
        self.assertLessEqual(B['n1'], len(T) / 2)
        md = open(os.path.join(d, 'KELUAR.md'), encoding='utf-8').read()
        self.assertIn(f"**{B['n1']} daripada {B['n']}**", md)
        self.assertIn('Keputusan bacaan 1: keluar baharu TIDAK menolong', md)
        self.assertIn('Keputusan bacaan 2: potong rugi TIDAK menolong', md)
        S = pd.read_csv(os.path.join(d, 'sejagat.csv'))
        self.assertEqual((int((S.senarai == 'T').sum()), int((S.senarai == 'aras CS07').sum())), (k9.N_SEJAGAT, 1))
        self.assertLessEqual(int((S.senarai == 'R').sum()), k9.N_SEJAGAT)
        self.assertTrue(S[S.senarai == 'T'].kelas.str.contains('K').all())      # hanya kelas kemuncak masuk senarai sejagat
        reg = pd.read_csv(os.path.join(SINI, '..', 'data', 'registry_F.csv'), dtype=str).fillna('')
        self.assertNotIn('CS09', set(reg.pusingan))                             # pusingan ini tidak mendaftar atau mengubah setup F


class TestCS10(unittest.TestCase):
    """SPEC pindaan 15 Nov 2026 (s): keluar daripada maklumat baharu pada lorong trend T01-T12 (pegang 126 sesi)."""

    def test_ruang_dikunci(self):
        import collections

        import cs_keluar10 as k10
        import cs_trend8 as t8
        self.assertEqual(dict(collections.Counter(a[1] for a in k10.ATOM10)), {'P': 22, 'S': 2, 'E': 10, 'R': 6, 'K': 24, 'L': 26})
        self.assertEqual((k10.NB, k10.NL, k10.NA, k10.NR, k10.NH * k10.NKOL), (90, 38, 128, 16385, 294930))
        self.assertEqual((k10.N_SEJAGAT, k10.SIMPAN_MIN, k10.TP_LONGGAR, k10.H_MAX, k10.TB), (10, 0.90, 0.005, 126, 0.30))
        self.assertEqual((k10.HENTI, k10.AKTIF), (t8.HENTI, t8.AKTIF))
        self.assertEqual(len({a[0] for a in k10.ATOM10}), 90)
        self.assertFalse({a[6] for a in k10.ATOM10} & {a[3] for a in t8.ATOM})      # tiada atom baharu yang sudah ada dalam CS08
        self.assertEqual(k10.kod_peraturan(0), 'X00')
        self.assertEqual(k10.nama_peraturan((1 + 1) * k10.NG), t8.ATOM[1][3])       # peraturan tunggal = 1 + atom
        self.assertEqual(int((k10.JENIS == 0).sum()), k10.N_SIRI)

    def test_papan_cs08_dibaca_semula(self):
        import cs_keluar10 as k10
        P = k10.papan8()
        self.assertEqual([b['id'] for b in P], [f'T{i:02d}' for i in range(1, 13)])
        nama = {b['id']: b['pencetus'] for b in P}
        self.assertEqual((nama['T01'], nama['T03'], nama['T04'], nama['T07'], nama['T11']),
                         ('M27.9s8', 'M14.2', 'K01.074', 'P45', 'K23.005'))
        self.assertTrue(all(b['q2'] == 13 for b in P))                           # semua memakai hasil suku tumbuh >= 20 % (QF06)
        self.assertEqual([t[0] for t in k10.k9.tugas_m([b['pencetus'] for b in P])],
                         ['M137.4', 'M14.3', 'M10.9s7', 'M10.9s8', 'M27.9s6', 'M27.9s8', 'M92.3s1'])

    def _data(self):
        import cs_keluar10 as k10
        rng = np.random.default_rng(5)
        n = 700
        c = 50 * np.exp(np.cumsum(rng.normal(0.001, 0.03, n)))
        o = c * (1 + rng.normal(0, 0.008, n))
        lo = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.01, n)))
        X = (rng.random((k10.N_SIRI, n)) < 0.03).astype(np.uint8)
        return o, lo, c, c * 0.035, X, np.arange(260, 560, 9).astype(np.int64)

    def test_kernel_pariti_cs_trend8(self):
        import cs_keluar10 as k10
        import cs_trend8 as t8
        o, lo, c, atr, X, ev = self._data()
        for pm in (1, 3):
            R8, SK8 = t8.hasil_semua(ev, o, lo, c, atr, X[:k10.N_XT], t8.JENIS, t8.PAR, t8.BARIS, pm)
            st = k10.sedia(ev, o, lo, c, atr, X, k10.JENIS, k10.PAR, k10.PAR2, k10.PAR3, k10.BARIS, pm)
            for s in range(k10.NH):
                for kol8 in range(t8.NKOL):                                     # X00 dan setiap atom lama x syarat aktif
                    kol = 0 if kol8 == 0 else (1 + (kol8 - 1) // t8.NG) * k10.NG + (kol8 - 1) % t8.NG
                    R, sk = k10.hasil(*st[:7], k10.A1, k10.A2, k10.OP, s, kol)
                    self.assertTrue(np.allclose(R, R8[:, s, kol8], atol=1e-5), (pm, s, kol8))
                    self.assertTrue((sk == SK8[:, s, kol8]).all(), (pm, s, kol8))
            lab = t8.label8(ev, o, c)
            self.assertTrue((lab[:, 0] == st[7][:, 0]).all())
            if pm == 3:
                self.assertTrue(((st[0][:, :, 0] & 3) == 0).all())              # pegang minimum: tiada bit sesi 1 dan 2

    def test_atom_baharu_pasangan_dan_kumpul(self):
        import cs_keluar10 as k10
        o, lo, c, atr, X, ev = self._data()
        st = k10.sedia(ev, o, lo, c, atr, X, k10.JENIS, k10.PAR, k10.PAR2, k10.PAR3, k10.BARIS, 3)
        M, ARM = st[0], st[1]
        for k, i in enumerate(ev):
            e = i + 1
            P = o[e]
            for a in range(k10.NL, k10.NA):
                j, par, par2, par3 = k10.JENIS[a], k10.PAR[a], k10.PAR2[a], k10.PAR3[a]
                m = [0, 0]
                for d in range(2, k10.H_MAX - 1):
                    b = e + d
                    seg = c[e:b + 1]
                    hc, dh = seg.max(), int(np.argmax(seg))
                    ya = (X[k10.BARIS[a], b] != 0 if j == 0 else d - dh >= par if j == 4
                          else (hc > P and c[b] <= P + (1 - par) * (hc - P)) if j == 5
                          else (d + 1 >= par and c[b] < P * (1 + par2)) if j == 6
                          else (hc >= P * (1 + par) and c[b] < P * (1 + par2)) if j == 7
                          else (d > dh and c[b] < lo[e + dh]) if j == 8
                          else c[b] < hc - (par if d + 1 <= par3 else par2) * atr[b] if j == 10
                          else c[b] < hc - (par if hc < P * (1 + par3) else par2) * atr[b])
                    if ya:
                        m[d // 63] |= 1 << (d % 63)
                self.assertEqual((m[0], m[1]), (int(M[k, a, 0]), int(M[k, a, 1])), (k, a))
        x = lambda r, g: np.array([k10._x(M[k], ARM[k], k10.A1, k10.A2, k10.OP, r, g) for k in range(len(ev))])
        a, b = 3, 60
        r_atau = int(np.flatnonzero((k10.OP == 2) & (k10.A1 == a) & (k10.A2 == b))[0])
        self.assertTrue((x(r_atau, 0) == np.minimum(x(1 + a, 0), x(1 + b, 0))).all())            # ATAU = yang lebih awal
        self.assertTrue((x(r_atau + 1, 0) >= np.maximum(x(1 + a, 0), x(1 + b, 0))).all())        # DAN tidak lebih awal
        self.assertTrue((x(1 + a, 2) >= x(1 + a, 1)).all() and (x(1 + a, 1) >= x(1 + a, 0)).all())   # syarat aktif melewatkan
        Acc = k10.kumpul(*st, np.zeros(len(ev), np.int64), 1, k10._A1S, k10._A2S, k10._OPS)
        self.assertEqual(Acc.shape, (k10.NH, (k10.NA + 1) * k10.NG, 1, k10.NST))
        R, _ = k10.hasil(*st[:7], k10._A1S, k10._A2S, k10._OPS, 4, (1 + b) * k10.NG)
        self.assertTrue((Acc[..., 0] == len(ev)).all())
        self.assertAlmostEqual(float(Acc[4, (1 + b) * k10.NG, 0, 4]), float(R.sum()), places=3)
        self.assertAlmostEqual(float(Acc[4, (1 + b) * k10.NG, 0, 1]), float((R >= 0.30).sum()))
        self.assertAlmostEqual(float(Acc[4, (1 + b) * k10.NG, 0, 6]), float(R[st[7][:, 0] > 0].sum()), places=3)

    def test_siri_panel_dan_syarikat(self):
        import cs_keluar10 as k10
        c = np.arange(1.0, 21.0)
        pan = {'c': np.concatenate([c, c * 2]), 'mula': np.asarray([0, 20, 40]), 'tid': np.repeat([0, 1], 20)}
        s = k10.sma_panel(pan, 5)
        self.assertTrue(np.isnan(s[:4]).all() and np.isnan(s[20:24]).all())      # tidak merentas saham
        self.assertAlmostEqual(float(s[4]), 3.0)
        self.assertAlmostEqual(float(s[24]), 6.0)
        x = np.zeros(40, bool)
        x[[18, 19, 20]] = True
        g = k10.kira_golek(x, pan['mula'], pan['tid'], 3)
        self.assertEqual((int(g[19]), int(g[20]), int(g[21]), int(g[23])), (2, 1, 1, 0))
        n = 40
        pan = {'o': np.full(n, 100.0), 'c': np.full(n, 100.0), 'tarikh': (20240101 + np.arange(n)).astype(np.int32),
               'mula': np.asarray([0, n]), 'ticker': np.asarray(['AAA'])}
        pan['c'][20:] = 88.0                                                    # sesi reaksi indeks 20: -12 %
        E = k10.syarikat_siri(pan, {'AAA': (np.asarray([int(pan['tarikh'][19])]), np.asarray([True]))},
                              {'AAA': (np.asarray([int(pan['tarikh'][10]), int(pan['tarikh'][25])]), np.asarray([1.0, -2.0]),
                                       np.asarray([0.30, 0.05]))})
        kod = {a[6]: a[0] for a in k10.ATOM10 if a[1] == 'E'}
        self.assertEqual(np.flatnonzero(E[kod['reaksi earnings terakhir (0-5 sesi lalu) <= -10%']]).tolist(), list(range(20, 26)))
        self.assertEqual(np.flatnonzero(E[kod['earnings pada sesi berikutnya (jual sebelum laporan)']]).tolist(), [19])
        self.assertEqual(np.flatnonzero(E[kod['hasil suku terkini tumbuh < 20%']]).tolist(), list(range(26, n)))   # diumumkan SEBELUM hari bar
        self.assertEqual(np.flatnonzero(E[kod['hasil suku terkini tumbuh < 0%']]).tolist(), [])
        self.assertEqual(np.flatnonzero(E[kod['kejutan untung terkini negatif (SUE < 0)']]).tolist(), list(range(26, n)))

    def test_bacaan_dikunci(self):
        import cs_keluar10 as k10
        n = 12
        asas = dict(n_K3=np.full(n, 20), tb_x00T=0.20, tb_cs08=0.20, simpan_T=0.95, rugi15_T=0.40, rugi15_cs08=0.40,
                    K3_tb_T=5.0, K3_tb_x00T=4.0, pur_R=0.08, pur_x00R=0.06, rugi15_R=0.35, rugi15_x00R=0.40, tb_R=0.20,
                    tb_x00R=0.20, simpan_R=0.95, K3_R_R=2.0, K3_R_x00R=1.0)
        T = pd.DataFrame({**asas, 'tb_T': [0.25] * 7 + [0.20] * 5})             # 7/12 mengatasi X00 dan keluar CS08
        B = k10.bacaan(T)
        self.assertEqual((B['n1'], B['ya1'], B['n2'], B['ya2'], B['n_k3']), (7, True, 12, True, 240))
        self.assertAlmostEqual(B['k3_T'], 12 / 240)
        self.assertFalse(k10.bacaan(T.assign(tb_T=[0.25] * 6 + [0.20] * 6))['ya1'])     # tepat separuh tidak cukup
        self.assertFalse(k10.bacaan(T.assign(simpan_T=0.85))['ya1'])                    # menjual pelari besar terlalu awal
        self.assertFalse(k10.bacaan(T.assign(K3_tb_T=4.0))['ya1'])
        self.assertFalse(k10.bacaan(T.assign(rugi15_T=0.42))['ya1'])
        self.assertFalse(k10.bacaan(T.assign(rugi15_R=0.40))['ya2'])
        self.assertFalse(k10.bacaan(T.assign(K3_R_R=1.0))['ya2'])

    def test_rekod_cs10(self):
        import cs_keluar10 as k10
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS10')
        T = pd.read_csv(os.path.join(d, 'keluar.csv'))
        self.assertEqual(T.id.tolist(), [f'T{i:02d}' for i in range(1, 13)])
        self.assertLess(float((T.pariti_tb_x00_cs08 - T.tb_cs08).abs().max()), 1e-4)     # pariti dengan hasil/CS08/papan.csv
        self.assertTrue((T.pariti_n == T.pariti_n_cs08).all())
        B = k10.bacaan(T)
        self.assertTrue(B['ya1'])                                               # bacaan dikunci (s) 1: keluar baharu MENOLONG (dijual >= +30 %)
        self.assertFalse(B['ya2'])                                              # bacaan dikunci (s) 2: potong rugi TIDAK menolong
        self.assertGreater(B['n1'], len(T) / 2)
        md = open(os.path.join(d, 'KELUAR.md'), encoding='utf-8').read()
        self.assertIn(f"**{B['n1']} daripada {B['n']}**", md)
        self.assertIn('Keputusan bacaan 1: keluar baharu MENOLONG', md)
        self.assertIn('Keputusan bacaan 2: potong rugi TIDAK menolong', md)
        S = pd.read_csv(os.path.join(d, 'sejagat.csv'))
        self.assertEqual(int((S.senarai == 'T').sum()), k10.N_SEJAGAT)
        self.assertTrue((S[S.senarai == 'T'].kelas == 'K').all())               # semua keluar sejagat T = kelas kemuncak
        bukan_x00 = T[T.keluar_T != 'X00']                                      # kaveat direkod: purata dagangan tidak naik
        self.assertLessEqual(float((bukan_x00.pur_T - bukan_x00.pur_x00T).median()), 0.0)
        p8 = pd.read_csv(os.path.join(d, '..', 'CS08', 'papan.csv'))
        self.assertTrue(p8.keluar.str.startswith('X00').all())                  # papan T01-T12 tidak diubah oleh CS10


class TestCS11(unittest.TestCase):
    """SPEC pindaan 15 Nov 2026 (t): ukuran longgar `naik`, pegang selepas 4 minggu, kekerapan, banding M / N / F."""

    def _data(self):
        rng = np.random.default_rng(7)
        n = 900
        c = 50 * np.exp(np.cumsum(rng.normal(0.001, 0.03, n)))
        o = c * (1 + rng.normal(0, 0.008, n))
        h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.008, n)))
        lo = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.01, n)))
        pan = dict(o=o, h=h, l=lo, c=c, atr=c * 0.035, mula=np.asarray([0, n]), tid=np.zeros(n, np.int64))
        return pan, np.arange(260, 700, 5).astype(np.int64)

    def test_dikunci(self):
        import cs_semak11 as s11
        self.assertEqual((s11.T20, s11.H, s11.NAIK_MIN, s11.NAIK_LANTAI), (20, 126, 0.02, 0.10))
        self.assertEqual((s11.MIN_BELIAN, s11.MIN_TAHUN, s11.MIN_SETAHUN), (300, 10, 24))
        self.assertEqual(s11.CARA, ['J20', 'P-MA20', 'P-MA20x2', 'P-MA50', 'P-R10', 'P-CH4', 'P-126'])
        self.assertEqual(s11.HENTI[s11.S_ASAL], '4xATR14')

    def test_label_menyamai_kiraan_naif(self):
        import cs_semak11 as s11
        pan, ev = self._data()
        o, lo, c = pan['o'], pan['l'], pan['c']
        Lb = s11.label11(ev, o, lo, c)
        for k, i in enumerate(ev):
            e = i + 1
            P, seg = o[e], c[e:e + 20]
            h8 = c[e] <= .92 * P or any(o[e + d] <= .92 * P or lo[e + d] <= .92 * P for d in range(1, 20))
            m5 = c[e + 4] >= 1.05 * P
            naik = c[e + 19] >= 1.02 * P and c[e + 19] > seg.mean() and seg.min() > .90 * P
            mahu = [m5, m5 and c[e + 19] > c[e + 4] and not h8, naik, naik and c[e + 19] >= 1.10 * P, naik and c[e + 19] >= 1.20 * P]
            self.assertEqual([bool(x) for x in Lb[k]], [bool(x) for x in mahu], k)
        self.assertTrue((Lb[:, 3] <= Lb[:, 2]).all() and (Lb[:, 4] <= Lb[:, 3]).all())

    def test_jual20_sama_dengan_cs_keluar7(self):
        import cs_keluar7 as k7
        import cs_semak11 as s11
        pan, ev = self._data()
        g = pd.DataFrame({'open': pan['o'], 'high': pan['h'], 'low': pan['l'], 'close': pan['c'], 'volume': 1e6},
                         index=pd.bdate_range('2019-01-02', periods=len(pan['c'])))
        st = k7.sedia_pan(pan, k7.siri(g).astype(np.uint8), ev)
        for s in range(8):
            R7, sk7 = k7.hasil(*st[:7], k7.A1, k7.A2, k7.OP, s, 0)
            R, sk, kena = s11.jual20(ev, pan['o'], pan['l'], pan['c'], pan['atr'], s)
            self.assertTrue(np.allclose(R, R7, atol=1e-9) and (sk == sk7).all(), s)
            self.assertTrue((sk >= 1).all())                                    # tiada jualan pada hari beli
            self.assertTrue(((sk < 19) <= kena).all())                          # jualan sebelum hari ke-20 hanya kerana stop loss

    def test_pegang_menyamai_simulasi_hari_demi_hari(self):
        import cs_semak11 as s11
        pan, ev = self._data()
        o, lo, c, atr = pan['o'], pan['l'], pan['c'], pan['atr']
        ev = ev[ev + 127 < len(c)]
        B = s11.siri_trend(pan)
        s20 = pd.Series(c).rolling(20).mean().to_numpy()
        self.assertTrue((B[0] == (c < s20)).all())

        def sim(i, s, m):
            e = i + 1
            P = o[e]
            Ls = [P * .92, P * .90, P * .88, P * .85, P - 3 * atr[i], P - 4 * atr[i], P - 5 * atr[i], min(P * .90, P - 4 * atr[i])][s]
            jual_esok, hc, akhir = c[e] <= Ls, c[e], 19 if m == 0 else 125
            for d in range(1, akhir + 1):
                b = e + d
                if jual_esok or o[b] <= Ls:
                    return o[b] / P - 1 - s11.KOS, d
                if lo[b] <= Ls:
                    return Ls / P - 1 - s11.KOS, d
                hc = max(hc, c[b])
                if d == akhir:
                    return c[b] / P - 1 - s11.KOS, d
                if 1 <= m <= 5 and d >= 19 and ((B[m - 1, b] != 0) if m <= 4 else (c[b] < hc - 4 * atr[b])):
                    jual_esok = True
        for s in (1, 5, 6):
            R, SK = s11.pegang(ev, o, lo, c, atr, B, s)
            for k, i in enumerate(ev):
                for m in range(s11.NC):
                    r, sk = sim(int(i), s, m)
                    self.assertAlmostEqual(r, float(R[k, m]), places=9, msg=(s, k, m))
                    self.assertEqual(sk, int(SK[k, m]), (s, k, m))
            self.assertTrue((SK >= 1).all())                                    # tiada jualan pada hari beli
            self.assertTrue((SK[:, 1:] >= np.minimum(SK[:, :1], 19)).all())     # cara pegang tidak pernah menjual lebih awal daripada J20

    def test_rekod_cs11(self):
        import cs_semak11 as s11
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS11')
        T = pd.read_csv(os.path.join(d, 'semak_f.csv'))
        F, M, N = (T[T.kump == k] for k in ('F', 'M asal', 'N asal'))
        self.assertEqual((len(F), len(M), len(N)), (69, 134, 49))
        self.assertTrue(F.swing.all())                                          # tiada jualan hari beli; jualan awal hanya stop loss
        self.assertGreater(F.terus.median(), 2 * M.terus.median())              # ukuran ketat: F jauh mengatasi M dan N asal
        self.assertGreater(F.terus.median(), 2 * N.terus.median())
        self.assertGreater(F.m5.median(), 2 * M.m5.median())
        self.assertLess(abs(float((F.naik - F.a_naik).median())), 0.01)         # ukuran longgar: F hampir sama dengan rawak hari sama
        self.assertLessEqual(int(F.lulus_naik.sum()), 5)
        self.assertEqual(int(F.menepati.sum()), int((F.lulus_naik & (F.prasyarat.fillna('') != '')).sum()))
        for r in F.itertuples():                                                # takrif "lulus ukuran longgar" dikunci pindaan (t)
            mahu = bool(r.n >= s11.MIN_BELIAN and r.tahun >= s11.MIN_TAHUN and min(r.kl_naik_K1, r.kl_naik_K2, r.kl_naik_K3) > 0)
            self.assertEqual(bool(r.lulus_naik), mahu, r.id)
        P = pd.read_csv(os.path.join(d, 'pegang.csv'))
        b = P[P.set == 'B'].pivot(index='id', columns='cara')
        self.assertEqual(sorted(P.cara.unique()), sorted(s11.CARA))
        for cr in s11.CARA[1:]:                                                 # pegang lebih lama: purata naik, kadar menang turun
            self.assertGreater(int((b['purata'][cr] > b['purata']['J20']).sum()), len(b) / 2, cr)
            self.assertLess(float((b['menang'][cr] - b['menang']['J20']).median()), -0.02, cr)
        md = open(os.path.join(d, 'SEMAK_F.md'), encoding='utf-8').read()
        self.assertIn('Keputusan: pegang selepas 4 minggu TIDAK menolong', md)
        reg = pd.read_csv(os.path.join(SINI, '..', 'data', 'registry_F.csv'), dtype=str).fillna('')
        self.assertNotIn('CS11', set(reg.pusingan))                             # pusingan ini tidak mendaftar atau mengubah setup F


class TestCS12(unittest.TestCase):
    """SPEC pindaan 15 Nov 2026 (u): carian baharu dipangkatkan ikut ukuran longgar `naik`, cara pegang B."""

    def test_dikunci(self):
        import cs_cari12 as c12
        import cs_semak11 as s11
        self.assertEqual((c12.N_ATAS, c12.N_KAWALAN, c12.BENIH_KAWALAN, c12.N_BACA), (5, 300, 20261115, 100))
        self.assertEqual((c12.k7.HENTI[c12.S_HENTI], s11.CARA[c12.CARA_B]), ('4xATR14', 'P-MA20'))

    def test_bacaan_dikunci(self):
        import cs_cari12 as c12
        asas = dict(peranan=['calon'] * 120 + ['kawalan'] * 50, skor_A=list(np.linspace(0.2, 0.01, 120)) + [np.nan] * 50)
        T = pd.DataFrame({**asas, 'lulus': [True] * 70 + [False] * 50 + [True] * 5 + [False] * 45, 'kl_naik': [0.05] * 120 + [0.0] * 50})
        B = c12.bacaan(T)
        self.assertEqual((B['n_calon'], B['atas'], B['kawalan']), (120, 100, 50))
        self.assertAlmostEqual(B['atas_lulus'], 0.70)
        self.assertTrue(B['ya'])
        self.assertFalse(c12.bacaan(T.assign(kl_naik=0.01))['ya'])                      # kelebihan terlalu kecil
        self.assertFalse(c12.bacaan(T.assign(lulus=[True] * 40 + [False] * 80 + [True] * 5 + [False] * 45))['ya'])   # kurang separuh
        self.assertFalse(c12.bacaan(T.assign(lulus=[True] * 70 + [False] * 50 + [True] * 30 + [False] * 20))['ya'])  # kawalan terlalu hampir

    def test_rekod_cs12(self):
        import cs_cari12 as c12
        import cs_semak11 as s11
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS12')
        c = pd.read_csv(os.path.join(d, 'calon.csv.gz'))
        k = pd.read_csv(os.path.join(d, 'kawalan.csv'))
        self.assertEqual(len(k), c12.N_KAWALAN)
        self.assertGreater(len(c), 1000)                                        # tiada had bilangan calon
        self.assertTrue((c.skor_A > 0).all() and c.skor_A.is_monotonic_decreasing)
        for r in c.head(300).itertuples():                                      # takrif "lulus" dikunci
            mahu = bool(r.n >= s11.MIN_BELIAN and r.tahun >= s11.MIN_TAHUN and min(r.kl_naik_K1, r.kl_naik_K2, r.kl_naik_K3) > 0)
            self.assertEqual(bool(r.lulus), mahu, r.id)
        B = c12.bacaan(pd.concat([c.assign(peranan='calon'), k.assign(peranan='kawalan')], ignore_index=True))
        self.assertFalse(B['ya'])                                               # bacaan dikunci (u): carian TIDAK berhasil
        e = c[(c.n >= s11.MIN_BELIAN) & (c.tahun >= s11.MIN_TAHUN)]
        ek = k[(k.n >= s11.MIN_BELIAN) & (k.tahun >= s11.MIN_TAHUN)]
        self.assertGreater(float((e.kl_naik_K1 > 0).mean()), 0.7)               # pada tahun carian calon mengatasi rawak ...
        self.assertLess(float((e.kl_naik_K3 > 0).mean()), 0.5)                  # ... tetapi tidak pada 2025-26
        self.assertLess(abs(float((e.kl_naik_K3 > 0).mean()) - float((ek.kl_naik_K3 > 0).mean())), 0.10)
        md = open(os.path.join(d, 'CARIAN.md'), encoding='utf-8').read()
        self.assertIn('Keputusan: carian ikut ukuran longgar TIDAK berhasil', md)
        reg = pd.read_csv(os.path.join(SINI, '..', 'data', 'registry_F.csv'), dtype=str).fillna('')
        self.assertNotIn('CS12', set(reg.pusingan))                             # tiada calon ukuran longgar didaftarkan sebagai kod F


class TestCS13(unittest.TestCase):
    """SPEC pindaan 15 Nov 2026 (v): daftar SEMUA setup naik laju yang lulus (tanpa had bilangan) + senarai utama F + cara pegang B."""

    def test_dikunci(self):
        import cs_daftar13 as d13
        import cs_semak11 as s11
        self.assertEqual((d13.N_ATAS, d13.N_KAWALAN, d13.BENIH_KAWALAN), (5, 300, 20261116))
        self.assertEqual((d13.JACCARD, d13.B1_BEZA, d13.B2_MIN, d13.B2_BEZA), (0.80, 0.20, 0.60, 0.10))
        self.assertEqual((d13.MENANG_PILIH, d13.PURATA_PILIH, d13.MIN_K3), (0.50, 0.02, 20))
        self.assertEqual((d13.k7.HENTI[d13.S_HENTI], s11.CARA[d13.CARA_B], d13.KOD_HENTI, d13.KOD_PEGANG, d13.ID_MULA),
                         ('4xATR14', 'P-MA20', 'G6', 'PB', 96))
        self.assertEqual(d13.takrif13('K19.011', 2, 0, 8, 16).split('|')[2:4], ['G6', 'PB'])

    def _T(self, lulus_c, k3_c, lulus_k, k3_k, n=100):
        f = lambda bil, m: [True] * int(round(bil * m)) + [False] * (m - int(round(bil * m)))
        return pd.DataFrame({'peranan': ['calon'] * n + ['kawalan'] * n + ['calon'] * 10, 'layak': [True] * (2 * n) + [False] * 10,
                             'lulus': f(lulus_c, n) + f(lulus_k, n) + [False] * 10,
                             'kl_terus_K3': [0.02 if x else -0.02 for x in f(k3_c, n) + f(k3_k, n)] + [0.05] * 10})

    def test_bacaan_dikunci(self):
        import cs_daftar13 as d13
        B = d13.bacaan(self._T(0.45, 0.70, 0.12, 0.50))
        self.assertEqual((B['n_calon'], B['calon_layak'], B['kawalan_layak'], B['n_lulus']), (110, 100, 100, 45))
        self.assertTrue(B['b1'] and B['b2'] and B['ya'])
        self.assertAlmostEqual(B['nasib'], 0.12 / 0.45)
        self.assertFalse(d13.bacaan(self._T(0.30, 0.70, 0.12, 0.50))['ya'])              # B1: beza lulus < 20 mata
        self.assertFalse(d13.bacaan(self._T(0.45, 0.58, 0.12, 0.40))['ya'])              # B2: 2025-26 < 60 %
        self.assertFalse(d13.bacaan(self._T(0.45, 0.65, 0.12, 0.58))['ya'])              # B2: beza dengan kawalan < 10 mata

    def test_kembar(self):
        import cs_daftar13 as d13
        r = lambda *x: np.concatenate([np.arange(a, b) for a, b in x]).astype(np.int32)
        kos = np.zeros(0, np.int32)
        K = {'_n': {'A': 10000, 'B': 10000},
             'F01': dict(e_B=r((0, 100)), e_A=kos),
             'C0001': dict(e_B=r((0, 95), (200, 205)), e_A=kos),                 # 95 / 105 dengan F01 -> kembar F01
             'C0002': dict(e_B=r((1000, 1050)), e_A=r((1000, 1050))),            # baharu
             'C0003': dict(e_B=r((1000, 1050)), e_A=r((1000, 1040), (2000, 2010))),   # 90 / 110 dengan C0002 -> kembar
             'C0004': dict(e_B=r((1000, 1050)), e_A=r((3000, 3050))),            # 50 / 150 -> bukan kembar
             'C0005': dict(e_B=r((1000, 1050)), e_A=r((1000, 1050)))}            # tidak lulus -> tidak disemak
        T = pd.DataFrame({'peranan': ['F'] + ['calon'] * 5, 'id': ['F01', 'C0001', 'C0002', 'C0003', 'C0004', 'C0005'],
                          'lulus': [True, True, True, True, True, False], 'skor_A': [np.nan, 0.5, 0.4, 0.3, 0.2, 0.1]})
        self.assertEqual(d13.kembar(T, K), {'C0001': 'F01', 'C0002': '', 'C0003': 'C0002', 'C0004': ''})

    def test_lengkap_satu_posisi_tiada_jual_hari_beli(self):
        import cs_daftar13 as d13
        import cs_semak11 as s11
        g = _saham(700, 13)
        n = len(g)
        pan = {k: g[m].to_numpy(float) for k, m in (('o', 'open'), ('h', 'high'), ('l', 'low'), ('c', 'close'))}
        pan.update(atr=pan['c'] * 0.03, mula=np.asarray([0, n]), tid=np.zeros(n, np.int64), sah=np.ones(n, bool),
                   tempoh=(np.arange(n) >= 300).astype(np.int8))
        Bt = np.zeros((4, n), np.uint8)
        Bt[0] = pan['c'] < pd.Series(pan['c']).rolling(20).mean().to_numpy()
        ev = np.arange(60, 650, 7)
        L = d13.lengkap(pan, Bt, ev)
        sah = ev[ev + s11.H < n]
        R, SK = s11.pegang(np.ascontiguousarray(sah, dtype=np.int64), pan['o'], pan['l'], pan['c'], pan['atr'], Bt, d13.S_HENTI)
        ambil, akhir = [], -1
        for k, e in enumerate(sah):                                             # satu posisi: isyarat semasa dipegang diabaikan
            if e > akhir:
                ambil.append(k)
                akhir = e + 1 + SK[k, d13.CARA_B]
        self.assertEqual(L['n_semua'], len(sah))
        self.assertEqual(L['n'], len(ambil))
        self.assertAlmostEqual(L['purata'], float(R[ambil, d13.CARA_B].mean()))
        self.assertAlmostEqual(L['menang'], float((R[ambil, d13.CARA_B] > 0).mean()))
        self.assertEqual(L['jual_hari_beli'], 0)
        self.assertEqual(sum(v['n'] for v in L['K']), L['n'])
        self.assertTrue((SK[:, d13.CARA_B] >= 1).all())

    def test_rekod_cs13(self):
        import hashlib
        import cs_daftar13 as d13
        import cs_semak11 as s11
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS13')
        c = pd.read_csv(os.path.join(d, 'calon.csv.gz')).fillna({'kembar_kepada': '', 'id_F': ''})
        k = pd.read_csv(os.path.join(d, 'kawalan.csv'))
        U = pd.read_csv(os.path.join(d, 'senarai_utama.csv'))
        J = json.load(open(os.path.join(d, 'bacaan.json')))
        reg = pd.read_csv(os.path.join(SINI, '..', 'data', 'registry_F.csv'), dtype=str).fillna('')
        self.assertEqual(len(k), d13.N_KAWALAN)
        self.assertGreater(len(c), 1000)                                        # tiada had bilangan calon
        self.assertTrue((c.skor_A > 0).all() and c.skor_A.is_monotonic_decreasing)
        for r in pd.concat([c.head(300), c[c.id_F != '']]).itertuples():        # takrif "lulus" dikunci
            layak = bool(r.n >= s11.MIN_BELIAN and r.tahun >= s11.MIN_TAHUN)
            self.assertEqual((bool(r.layak), bool(r.lulus)), (layak, bool(layak and min(r.kl_terus_K1, r.kl_terus_K2, r.kl_terus_K3) > 0)), r.id)
        B = d13.bacaan(pd.concat([c.assign(peranan='calon'), k.assign(peranan='kawalan')], ignore_index=True))
        self.assertEqual((B['ya'], B['b1'], B['b2'], B['n_lulus']), (J['ya'], J['b1'], J['b2'], J['n_lulus']))
        self.assertTrue((c.kembar_kepada[~c.lulus] == '').all())
        self.assertTrue(c.untuk_daftar.equals(c.lulus & (c.kembar_kepada == '')))
        r13 = reg[reg.pusingan == 'CS13']
        lama = reg.iloc[:95]
        self.assertEqual(lama.id.tolist(), [f'F{i:02d}' for i in range(1, 96)])  # F01-F95 kekal: ID, takrif, henti, keluar
        cap = hashlib.sha256(lama[['id', 'pusingan', 'takrif', 'henti', 'keluar', 'status']].to_csv(index=False).encode()).hexdigest()
        self.assertEqual(cap, CAP_F_LAMA)
        if not J['ya']:                                                         # bacaan gagal -> tiada kod baharu
            self.assertEqual(len(r13), 0)
            return
        D = c[c.untuk_daftar]
        self.assertEqual(len(r13), len(D))                                      # SEMUA yang lulus dan bukan kembar didaftarkan
        self.assertEqual(r13.id.tolist(), [f'F{i}' for i in range(d13.ID_MULA, d13.ID_MULA + len(r13))])
        self.assertEqual(r13.takrif.tolist(), D.takrif.tolist())                # ikut susunan skor A
        self.assertEqual(dict(zip(D.takrif, D.id_F)), dict(zip(r13.takrif, r13.id)))
        self.assertTrue((c.id_F[~c.untuk_daftar] == '').all())
        self.assertTrue((r13.status == 'BACKTEST').all() and (r13.henti == 'G6 4xATR14').all() and r13.keluar.str.startswith('PB ').all())
        self.assertTrue(r13.takrif.map(lambda x: x.split('|')[2:4] == ['G6', 'PB'] and len(x.split('|')) == 5).all())
        self.assertEqual(reg.takrif.nunique(), len(reg))
        self.assertEqual(U.kedudukan.tolist(), list(range(1, len(U) + 1)))     # senarai utama
        self.assertTrue(U.pilihan.equals((U.menang_B >= d13.MENANG_PILIH) & (U.purata_B >= d13.PURATA_PILIH)))   # keputusan 16 Nov 2026
        self.assertTrue(U.pilihan.iloc[:int(U.pilihan.sum())].all())            # setup pilihan dipaparkan dahulu
        self.assertEqual(J['n_pilihan'], int(U.pilihan.sum()))
        for _, g in U.groupby('pilihan'):                                       # dalam setiap kumpulan: ikut kadar tangkap
            self.assertTrue(g.terus.is_monotonic_decreasing)
        self.assertEqual(set(J['semak_masa']), {'pilih', 'lain'})
        self.assertEqual((int((U.asal == 'lama').sum()), int((U.asal == 'baharu').sum())), (42, len(r13)))
        self.assertEqual(set(U.id[U.asal == 'baharu']), set(r13.id))
        self.assertEqual(int(U.jual_hari_beli.sum()), 0)                        # tiada jualan pada hari beli
        self.assertTrue((U.hari_B[U.asal == 'baharu'] >= 20).all())             # median pegang sekurang-kurangnya 20 hari
        md = open(os.path.join(d, 'DAFTAR.md'), encoding='utf-8').read()
        self.assertIn('Keputusan: carian naik laju BERHASIL', md)


class TestCS14(unittest.TestCase):
    """SPEC pindaan 16 Nov 2026 (x): cara pegang "jual yang rugi, pegang yang untung", tanpa had masa."""

    def _data(self):
        rng = np.random.default_rng(11)
        n = 1500
        c = 50 * np.exp(np.cumsum(rng.normal(0.0008, 0.03, n)))
        o = c * (1 + rng.normal(0, 0.008, n))
        h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.008, n)))
        lo = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.01, n)))
        pan = dict(o=o, h=h, l=lo, c=c, atr=c * 0.035, mula=np.asarray([0, n]), tid=np.zeros(n, np.int64))
        return pan, np.arange(260, 1300, 7).astype(np.int64)

    def test_dikunci(self):
        import cs_pegang14 as p14
        self.assertEqual((p14.W, len(p14.CALON), len(p14.KELAS_A), len(p14.KELAS_B)), (109, 35, 3, 32))
        self.assertEqual((p14.MIN_DAG, p14.MIN_K3, p14.D_MENANG, p14.D_RUGI), (30, 20, -0.02, 0.02))
        self.assertEqual((p14.T20, p14.SMA_N, list(p14.CH_K), p14.JATUH, p14.HAD), (20, (20, 50, 100, 200), [4.0, 6.0, 8.0], 0.75, (126, 252, 0)))
        self.assertEqual((p14.CARA[p14.SEKARANG], p14.CARA[p14.P126], p14.CARA[p14.SIMPAN], p14.CARA[0]), ('r0.t1.126', 'r0.t0.126', 'r0.t0.0', 'J20'))
        self.assertEqual(p14.k7.HENTI[p14.S_HENTI], '4xATR14')
        self.assertEqual(sorted(p14.CARA[w] for w in p14.KELAS_A), ['r1.t0.0', 'r2.t0.0', 'r3.t0.0'])
        self.assertTrue(all(p14.HW[w] == 0 and p14.TW[w] > 0 for w in p14.KELAS_B) and p14.SIMPAN not in p14.CALON)

    def test_menyamai_enjin_cs11(self):
        """Cara dengan had 126 sesi mesti sama dengan cs_semak11.pegang (enjin senarai utama)."""
        import cs_pegang14 as p14
        import cs_semak11 as s11
        pan, ev = self._data()
        R0, SK0 = s11.pegang(ev, pan['o'], pan['l'], pan['c'], pan['atr'], s11.siri_trend(pan), p14.S_HENTI)
        R, SK, TB = p14.hasil14(*p14.atom_panel(pan, ev), p14.RW, p14.TW, p14.HW)
        for lama, baru in (('J20', 'J20'), ('P-MA20', 'r0.t1.126'), ('P-MA50', 'r0.t2.126'), ('P-CH4', 'r0.t5.126'), ('P-126', 'r0.t0.126')):
            a, b = s11.CARA.index(lama), p14.CARA.index(baru)
            self.assertTrue(np.allclose(R[:, b], R0[:, a], atol=1e-12) and (SK[:, b] == SK0[:, a]).all(), lama)
            self.assertFalse(TB[:, b].any())
        self.assertGreater(len(set(SK0[:, 1])), 10)

    def _naif(self, pan, i, r, t, had):
        o, lo, c, atr = pan['o'], pan['l'], pan['c'], pan['atr']
        e, akhir = i + 1, len(c) - 1
        P, a0 = o[e], atr[i]
        Ls, kos = P - 4 * a0, 0.005
        if c[e] <= Ls:
            return o[e + 1] / P - 1 - kos, 1, False
        sma = lambda b, n: c[b - n + 1:b + 1].mean() if b - n + 1 >= 0 else np.nan
        hc = c[e]
        for d in range(0, akhir - e + 1):
            b = e + d
            if d >= 1 and (o[b] <= Ls or lo[b] <= Ls):
                return (o[b] if o[b] <= Ls else Ls) / P - 1 - kos, d, False
            hc = max(hc, c[b])
            if had and d == had - 1:
                return c[b] / P - 1 - kos, d, False
            if d < 19 or b == akhir:
                continue
            rugi = {0: False, 1: c[b] < P, 2: c[b] < P - a0, 3: d == 19 and c[b] < P}[r]
            trend = {0: False, 1: c[b] < sma(b, 20), 2: c[b] < sma(b, 50), 3: c[b] < sma(b, 100), 4: c[b] < sma(b, 200),
                     5: c[b] < hc - 4 * atr[b], 6: c[b] < hc - 6 * atr[b], 7: c[b] < hc - 8 * atr[b], 8: c[b] < 0.75 * hc}[t]
            if (rugi or trend) and not (had and d + 1 > had - 1):
                return o[b + 1] / P - 1 - kos, d + 1, False
        return c[akhir] / P - 1 - kos, akhir - e, True

    def test_menyamai_kiraan_naif(self):
        import cs_pegang14 as p14
        pan, ev = self._data()
        R, SK, TB = p14.hasil14(*p14.atom_panel(pan, ev), p14.RW, p14.TW, p14.HW)
        terbuka = 0
        for nama in ('r1.t0.0', 'r2.t0.0', 'r3.t0.0', 'r3.t2.0', 'r1.t3.0', 'r2.t7.0', 'r0.t8.0', 'r0.t4.0', 'r0.t6.252', 'r1.t2.252', 'r0.t0.0', 'r3.t5.126'):
            w = p14.CARA.index(nama)
            r, t, had = int(nama[1]), int(nama[4]), int(nama.split('.')[2])
            for k, i in enumerate(ev):
                mahu = self._naif(pan, int(i), r, t, had)
                self.assertAlmostEqual(R[k, w], mahu[0], 10, (nama, k))
                self.assertEqual((int(SK[k, w]), bool(TB[k, w])), mahu[1:], (nama, k))
                terbuka += mahu[2]
        self.assertGreater(terbuka, 0)                                   # ada posisi yang masih terbuka pada hujung data
        w1, w0 = p14.CARA.index('r1.t0.0'), p14.CARA.index('r0.t0.0')
        self.assertTrue((SK[:, w1] <= SK[:, w0]).all())                  # menambah peraturan tidak boleh melambatkan jualan

    def test_statistik_satu_posisi(self):
        import cs_pegang14 as p14
        ev = np.array([10, 12, 40, 5, 6], np.int64)
        tid = np.array([0, 0, 0, 1, 1], np.int64)
        tp = np.array([0, 0, 2, 1, 1], np.int64)
        R = np.array([[0.10, 0.60], [0.50, 0.50], [-0.20, -0.20], [0.02, 0.02], [0.30, 0.30]])
        SK = np.array([[5, 1], [3, 3], [9, 9], [0, 2], [4, 4]], np.int64)
        TB = np.zeros((5, 2), bool)
        TB[2, 0] = True
        S = p14.stat14(ev, tid, tp, R, SK, TB)
        g = lambda w, k: S[w, p14.IX[k]]
        # cara 0: isyarat 12 diabaikan (saham 0 dipegang hingga bar 16); saham 1: isyarat 6 selepas bar jual 6? 5+1+0 = 6 -> diabaikan
        self.assertEqual(g(0, 'n'), 3)
        self.assertAlmostEqual(g(0, 'purata'), (0.10 - 0.20 + 0.02) / 3)
        self.assertAlmostEqual(g(0, 'menang'), 2 / 3)
        self.assertAlmostEqual(g(0, 'rugi15'), 1 / 3)
        self.assertAlmostEqual(g(0, 'terbuka'), 1 / 3)
        self.assertEqual((g(0, 'sesi_med'), g(0, 'n_K1'), g(0, 'n_K2'), g(0, 'n_K3')), (6, 1, 1, 1))
        self.assertAlmostEqual(g(0, 'per20'), (0.10 - 0.20 + 0.02) / (6 + 10 + 1) * 20)
        # cara 1: saham 0 jual pada bar 12 -> isyarat 12 diabaikan (bar jual), isyarat 40 diambil; saham 1 jual bar 8 -> isyarat 6 diabaikan
        self.assertEqual(g(1, 'n'), 3)
        self.assertAlmostEqual(g(1, 'k50'), 1 / 3)
        self.assertAlmostEqual(g(1, 'purata_K1'), 0.60)

    def test_pemilihan_dan_bacaan(self):
        import cs_pegang14 as p14
        n = 40
        S = np.zeros((n, p14.W, p14.NS))
        S[:, :, p14.IX['n']] = 100
        S[:, :, p14.IX['n_K3']] = 25
        S[:, :, p14.IX['menang']] = 0.50
        S[:, :, p14.IX['rugi15']] = 0.10
        S[:, :, p14.IX['purata']] = 0.02
        S[:, :, p14.IX['purata_K3']] = 0.02
        a, b = p14.CARA.index('r1.t2.0'), p14.CARA.index('r0.t7.0')
        S[:, a, p14.IX['purata']] = 0.04                                 # lebih baik, menang dan rugi besar hampir sama
        S[:, a, p14.IX['menang']] = 0.49
        S[:, a, p14.IX['purata_K3']] = 0.03
        S[:, b, p14.IX['purata']] = 0.09                                 # purata tertinggi tetapi menang jatuh 8 mata
        S[:, b, p14.IX['menang']] = 0.42
        D = dict(ids=[f'F{i}' for i in range(n)], A=S, B=S.copy())
        B, ok = p14.bacaan(D)
        self.assertEqual((B['n_layak'], B['semua']['cara'], B['semua']['menepati_A'], B['semua']['ya']), (n, 'r1.t2.0', True, True))
        self.assertEqual(B['kelas_B']['cara'], 'r1.t2.0')
        self.assertFalse(B['kelas_A']['ya'])                             # tiada cara kelas A yang lebih baik daripada cara sekarang
        D['B'][:, a, p14.IX['rugi15']] = 0.13                            # syarat (3) gagal pada saham tidak dilihat
        self.assertFalse(p14.bacaan(D)[0]['semua']['ya'])
        D['B'][:, a, p14.IX['rugi15']] = 0.10
        D['B'][:, a, p14.IX['purata_K3']] = 0.01                         # syarat (4): 2025-26 lebih rendah
        self.assertFalse(p14.bacaan(D)[0]['semua']['ya'])
        S2 = S.copy()
        S2[:, p14.CALON, p14.IX['menang']] = 0.40                        # tiada calon menepati syarat -> purata tertinggi antara semua
        B2, _ = p14.bacaan(dict(ids=D['ids'], A=S2, B=S2.copy()))
        self.assertEqual((B2['semua']['cara'], B2['semua']['menepati_A'], B2['semua']['ya']), ('r0.t7.0', False, False))
        D['A'][:5, p14.SEKARANG, 0] = 10                                 # < 30 dagangan cara sekarang -> tidak layak
        self.assertEqual(p14.bacaan(D)[0]['n_layak'], n - 5)


    def test_fail_hasil(self):
        """Fail hasil CS14 konsisten sesama sendiri; cara sekarang = angka senarai utama; senarai utama tidak diubah."""
        import cs_pegang14 as p14
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS14')
        B = json.load(open(os.path.join(d, 'bacaan.json'), encoding='utf-8'))
        T = pd.read_csv(os.path.join(d, 'cara.csv'))
        G = pd.read_csv(os.path.join(d, 'tangga.csv'))
        X = pd.read_csv(os.path.join(d, 'setup.csv.gz'))
        U = pd.read_csv(os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS13', 'senarai_utama.csv'))
        self.assertEqual((B['n_setup'], len(X), len(U), len(T), len(G)), (2001, 2001, 2001, 2 * p14.W, 3 * len(p14.TANGGA)))
        self.assertEqual(B['cara'], p14.CARA)
        self.assertTrue(B['pariti']['n'] == 0 and B['pariti']['hari'] == 0 and max(B['pariti'][k] for k in ('menang', 'purata', 'rugi15')) < 2e-5)
        X, U = X.set_index('id'), U.set_index('id')
        self.assertTrue(np.allclose(X.loc[U.index, 'r0.t1.126:menang'], U.menang_B, atol=1e-4))
        self.assertTrue(np.allclose(X.loc[U.index, 'r0.t1.126:purata'], U.purata_B, atol=1e-4))
        tb = T[T.set == 'B'].set_index('cara')
        for k in ('semua', 'kelas_A', 'kelas_B'):
            x = B[k]
            self.assertEqual(x['cara'], p14.CARA[x['w']])
            self.assertEqual(x['ya'], x['s1'] and x['s2'] and x['s3'] and x['s4'])
            self.assertAlmostEqual(x['d_purata'], tb.loc[x['cara'], 'd_purata'], 4)
            self.assertEqual(x['sama'], abs(x['d_purata']) < p14.SAMA)
        self.assertIn(B['semua']['w'], p14.CALON)
        self.assertIn(B['kelas_A']['w'], p14.KELAS_A)
        # dapatan yang dilaporkan: tiada calon yang menaikkan purata >= 0.1 mata tanpa kadar menang jatuh > 2 mata (kumpulan B)
        c = tb.loc[[p14.CARA[w] for w in p14.CALON]]
        self.assertFalse(((c.d_purata >= p14.SAMA) & (c.d_menang >= p14.D_MENANG)).any())
        self.assertTrue(B['semua']['sama'] and not B['kelas_A']['ya'])
        # kawalan rawak: pegang lebih longgar menaikkan purata saham rawak juga
        self.assertEqual(B['n_kawalan'], p14.N_KAWALAN)
        self.assertGreater(tb.loc['r0.t7.0', 'rawak_purata'], tb.loc['r0.t1.126', 'rawak_purata'])
        self.assertEqual(sorted(G.cara.unique()), sorted(p14.TANGGA))
        self.assertEqual(sorted(G.n_setup.unique()), [42, 210, 2001])


class TestCS16(unittest.TestCase):
    """SPEC pindaan 16 Nov 2026 (z): "ujian solid" — tiga angka pengguna, takrif SOLID, tarikh laporan diteka, senarai pendek."""

    def _pan(self):
        rng = np.random.default_rng(15)
        n = 1500
        c = 40 * np.exp(np.cumsum(rng.normal(0.0006, 0.035, n)))
        o = c * (1 + rng.normal(0, 0.008, n))
        lo = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.01, n)))
        hari = pd.bdate_range('2012-01-03', periods=n)
        tarikh = (hari.year * 10000 + hari.month * 100 + hari.day).to_numpy().astype(np.int32)
        return dict(o=o, l=lo, c=c, atr=c * 0.04, mula=np.asarray([0, n]), tid=np.zeros(n, np.int64), tarikh=tarikh,
                    hari=np.arange(n), tempoh=np.where(np.arange(n) < 700, 0, np.where(np.arange(n) < 1200, 1, 2)).astype(np.int8))

    def test_dikunci(self):
        import cs_solid16 as s15
        self.assertEqual((s15.MIN_N, s15.MIN_TAHUN, s15.MIN_K3, s15.KL_MIN), (300, 10, 20, 0.03))
        self.assertEqual((s15.THN_MIN_N, s15.THN_MIN_BIL, s15.THN_BAHAGIAN, s15.BUANG_HARI, s15.KL_BAKI), (15, 8, 0.70, 10, 0.01))
        self.assertEqual((s15.ADIK_MAKS, s15.ADIK_MIN_N, s15.ADIK_MIN_BIL, s15.ADIK_BAHAGIAN, s15.TAMBAH_MIN), (30, 100, 3, 0.60, 0.01))
        self.assertEqual((s15.RAMAL_TAHUN, s15.RAMAL_SUKU, s15.S8_BAHAGIAN, s15.JACCARD, s15.B1_MAKS, s15.B2_BEZA), (364, 91, 0.5, 0.50, 0.05, 0.10))
        self.assertEqual((s15.Q_F01, s15.Q_F04, s15.k7.HENTI[s15.S_HENTI]), (8, 11, '4xATR14'))
        self.assertEqual(s15.LABEL[:4], ('m5', 'terus', 'm10', 'm10d'))

    def test_label_menyamai_kiraan_naif(self):
        import cs_solid16 as s15
        pan = self._pan()
        ev = np.arange(50, 1400, 3).astype(np.int64)
        L = s15.label15(ev, pan['o'], pan['c'])
        for k, i in enumerate(ev):
            e, P, c = i + 1, pan['o'][i + 1], pan['c']
            mahu = [c[e + 4] >= 1.10 * P, c[e + 9] >= 1.10 * P, c[e:e + 5].max() >= 1.05 * P, c[e:e + 5].max() >= 1.10 * P, c[e:e + 10].max() >= 1.10 * P]
            self.assertEqual([bool(x) for x in L[k]], [bool(x) for x in mahu], k)
        self.assertTrue((L[:, 0] <= L[:, 3]).all() and (L[:, 1] <= L[:, 4]).all() and (L[:, 3] <= L[:, 2]).all())
        self.assertGreater(L.sum(0).min(), 0)

    def test_ukur_menyamai_kiraan_naif(self):
        import cs_semak11 as s11
        import cs_solid16 as s15
        pan = self._pan()
        n = len(pan['c'])
        rng = np.random.default_rng(3)
        Lab = (rng.random((n, 7)) < 0.3).astype(np.float32)
        As = rng.random((n, 7)).astype(np.float32) * 0.4
        ev = np.arange(30, 1450, 4).astype(np.int64)
        d, e = s15.ukur15(pan, Lab, As, ev)
        R, sk, st = s11.jual20(ev, pan['o'], pan['l'], pan['c'], pan['atr'], s15.S_HENTI)
        amb = teras.satu_posisi(ev, sk, pan['tid'])
        self.assertTrue((e == ev[amb]).all())
        x = (Lab[e, 1] - As[e, 1]).astype(float)
        self.assertEqual(d['n'], len(e))
        self.assertAlmostEqual(d['kl_terus'], float(Lab[e, 1].mean()) - float(As[e, 1].mean()), 12)
        self.assertAlmostEqual(d['m10d'], float(Lab[e, 3].mean()), 12)
        T = pd.DataFrame({'thn': pan['tarikh'][e] // 10000, 'hari': pan['hari'][e], 'x': x, 'tp': pan['tempoh'][e]})
        g = T.groupby('thn').x.agg(['size', 'sum'])
        g = g[g['size'] >= s15.THN_MIN_N]
        self.assertEqual((d['thn_bil'], d['thn_pos']), (len(g), int((g['sum'] > 0).sum())))
        self.assertEqual(d['tahun'], T.thn.nunique())
        for p in range(3):
            self.assertAlmostEqual(d[f'kl_K{p + 1}'], float((Lab[e[T.tp == p], 1] - As[e[T.tp == p], 1]).mean()), 6)
        h = T.groupby('hari').x.sum().sort_values(ascending=False)
        buang = set(h.index[:s15.BUANG_HARI])
        baki = T[~T.hari.isin(buang)]
        self.assertAlmostEqual(d['kl_baki'], baki.x.mean(), 9)
        self.assertLess(d['kl_baki'], x.mean())                              # membuang hari terbaik menurunkan kelebihan
        self.assertEqual(s15.ukur15(pan, Lab, As, np.zeros(0, np.int64))[0]['n'], 0)

    def test_syarat(self):
        import cs_solid16 as s15
        baik = dict(n=400, tahun=12, n_K3=25, kl_terus=0.05, kl_K1=0.04, kl_K2=0.06, kl_K3=0.02, thn_bil=10, thn_pos=7, kl_m5=0.03,
                    kl_m10=0.01, kl_m10d=0.02, kl_baki=0.015)
        self.assertEqual(s15.syarat(baik), dict(s1=True, s2=True, s3=True, s4=True, s5=True))
        for k, v, s in (('n', 299, 's1'), ('tahun', 9, 's1'), ('n_K3', 19, 's1'), ('kl_terus', 0.029, 's2'), ('kl_K3', 0.0, 's2'),
                        ('kl_K2', float('nan'), 's2'), ('thn_pos', 6, 's3'), ('thn_bil', 7, 's3'), ('kl_m10', -0.001, 's4'),
                        ('kl_m10d', float('nan'), 's4'), ('kl_baki', 0.009, 's5'), ('kl_baki', float('nan'), 's5')):
            d = dict(baik, **{k: v})
            if k == 'thn_bil':
                d['thn_pos'] = 7
            self.assertFalse(s15.syarat(d)[s], (k, v))
        self.assertFalse(any(s15.syarat(dict(n=0, tahun=0)).values()))

    def test_tarikh_diteka(self):
        import cs_solid16 as s15
        hari = pd.bdate_range('2015-01-02', periods=700)
        d = (hari.year * 10000 + hari.month * 100 + hari.day).to_numpy().astype(np.int32)
        cari_ = lambda t: int(np.searchsorted(d, int(pd.Timestamp(t).strftime('%Y%m%d'))))
        ev = np.array([cari_(t) for t in ('2015-02-10', '2015-05-12', '2015-08-11', '2015-11-10', '2016-02-09', '2016-05-17', '2016-08-09')])
        p = s15.ramal_indeks(d, ev)
        self.assertEqual(p[0], -1)                                           # laporan pertama: tiada tekaan
        self.assertEqual(p[1], cari_(pd.Timestamp('2015-02-10') + pd.Timedelta(days=91)))    # < 4 laporan terdahulu: + 91 hari
        self.assertEqual(p[4], cari_(pd.Timestamp('2015-02-10') + pd.Timedelta(days=364)))   # suku sama tahun lepas + 364 hari
        self.assertEqual(p[4], ev[4])                                        # 2015-02-10 + 364 hari = 2016-02-09 (tepat)
        self.assertEqual(p[5] - ev[5], cari_('2016-05-10') - cari_('2016-05-17'))            # laporan lewat seminggu: tekaan 5 sesi awal
        self.assertTrue((p[1:] >= 0).all())

    def test_senarai_pendek(self):
        import cs_solid16 as s15
        U = pd.DataFrame({'id_F': ['F1', 'F2', 'F3', 'F4'], 'solid': [True, True, True, False], 'boleh_dibuat': [False, True, True, True],
                          'terus': [0.30, 0.20, 0.25, 0.40], 'kl_terus': [0.1, 0.1, 0.1, 0.1]})
        beli = {'F1': np.arange(0, 100), 'F2': np.arange(0, 60), 'F3': np.arange(40, 140), 'F4': np.arange(500, 600)}
        w = s15.wakil(U, beli)
        # susunan: boleh dibuat dahulu (F3 0.25, F2 0.20), kemudian F1. F2 lawan F3: 20/140 -> berbeza. F1 lawan F3: 60/140 = 0.43 -> berbeza;
        # F1 lawan F2: 60/100 = 0.60 -> serupa dengan F2
        self.assertEqual(w, {'F3': '', 'F2': '', 'F1': 'F2'})
        self.assertNotIn('F4', w)                                            # bukan solid -> tidak dinilai

    def test_bacaan_dikunci(self):
        import cs_solid16 as s15
        def T(sc, sk1, sk2, sce=None):
            f = lambda bil, m: [True] * int(round(bil * m)) + [False] * (m - int(round(bil * m)))
            c = pd.DataFrame({'jenis': 'calon', 'q2': [8] * 100 + [3] * 100, 'solid': f(sc if sce is None else sce, 100) + f(sc, 100)})
            k1 = pd.DataFrame({'jenis': 'K1', 'q2': 3, 'solid': f(sk1, 100)})
            k2 = pd.DataFrame({'jenis': 'K2', 'q2': 8, 'solid': f(sk2, 100)})
            X = pd.concat([c, k1, k2], ignore_index=True)
            for s in ('s1', 's2', 's3', 's4', 's5', 's7'):
                X[s] = True
            return X
        B = s15.bacaan(T(0.40, 0.02, 0.10))
        self.assertTrue(B['b1'] and B['b2'])
        self.assertAlmostEqual(B['nasib'], 0.02 / 0.40)
        self.assertEqual((B['solid_calon'], B['solid_K1'], B['solid_K2'], B['n_calon_earnings']), (80, 2, 10, 100))
        self.assertFalse(s15.bacaan(T(0.40, 0.06, 0.10))['b1'])                  # peraturan rawak lulus > 5 %
        self.assertFalse(s15.bacaan(T(0.40, 0.02, 0.35))['b2'])                  # beza dengan kawalan laporan kewangan < 10 mata
        self.assertTrue(s15.bacaan(T(0.10, 0.02, 0.35, sce=0.50))['b2'])


    def test_fail_hasil(self):
        """Fail hasil CS16 konsisten sesama sendiri dan dengan senarai utama; registry dan senarai utama tidak diubah."""
        import cs_solid16 as s15
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS16')
        B = json.load(open(os.path.join(d, 'bacaan.json'), encoding='utf-8'))
        U = pd.read_csv(os.path.join(d, 'solid.csv.gz'))
        Kw = pd.read_csv(os.path.join(d, 'kawalan.csv'))
        Pr = pd.read_csv(os.path.join(d, 'prasyarat.csv'))
        S13 = pd.read_csv(os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS13', 'senarai_utama.csv')).set_index('id')
        self.assertEqual((len(U), B['n_utama'], len(S13)), (2001, 2001, 2001))
        self.assertEqual(set(U.id), set(S13.index))
        self.assertTrue(np.allclose(U.set_index('id').loc[S13.index, 'terus'], S13.terus, atol=6e-5))       # solid.csv.gz: 4 titik perpuluhan
        self.assertTrue(np.allclose(U.set_index('id').loc[S13.index, 'm5'], S13.m5, atol=6e-5))
        self.assertEqual((int(U.solid.sum()), int(U.wakil.sum())), (B['solid_utama'], B['wakil']))
        # takrif SOLID dikira semula daripada lajur syarat
        semula = U.s1 & U.s2 & U.s3 & U.s4 & U.s5 & U.s7 & (U.s6 != 'gagal')
        self.assertTrue((semula == U.solid).all())
        self.assertTrue((U.wakil <= U.solid).all() and (U[U.solid & ~U.wakil].serupa_dengan.fillna('') != '').all())
        self.assertTrue(set(U[U.solid & ~U.wakil].serupa_dengan) <= set(U[U.wakil].id))
        self.assertTrue((U.boleh_dibuat == (~U.tarikh | U.s8)).all())
        s = U[U.solid]
        self.assertTrue((s.n >= s15.MIN_N).all() and (s.kl_terus >= s15.KL_MIN - 1e-6).all() and (s.kl_K3 > 0).all())
        self.assertTrue((s.thn_pos >= s15.THN_BAHAGIAN * s.thn_bil - 1e-9).all() and (s.kl_baki >= s15.KL_BAKI - 1e-6).all())
        self.assertTrue(((s.kl_m5 > 0) & (s.kl_m10 > 0) & (s.kl_m10d > 0)).all())
        # tiga angka pengguna: label bersarang (10 % seminggu <= 5 % seminggu; "pernah" >= pada tutup)
        self.assertTrue((U.m10 <= U.m5 + 1e-9).all() and (U.p5 >= U.m5 - 1e-9).all() and (U.p10d >= U.m10d - 1e-9).all())
        # kawalan dan bacaan dikunci
        self.assertEqual((len(Kw[Kw.jenis == 'K1']), len(Kw[Kw.jenis == 'K2']), B['n_K1'], B['n_K2']), (300, 300, 300, 300))
        self.assertTrue((Kw[Kw.jenis == 'K2'].q2 == s15.Q_F01).all())
        self.assertEqual(int(Kw[Kw.jenis == 'K1'].solid.sum()), B['solid_K1'])
        self.assertEqual(B['b1'], B['kadar_K1'] <= s15.B1_MAKS)
        self.assertEqual(B['b2'], B['kadar_calon_earnings'] >= B['kadar_K2'] + s15.B2_BEZA)
        self.assertTrue(B['b1'] and not B['b2'])                                 # dapatan yang dilaporkan
        # "prasyarat sahaja": laporan kewangan 1-5 sesi sendiri lulus S1-S5
        q = Pr[(Pr.q1 == -1) & (Pr.q2 == s15.Q_F01)].iloc[0]
        self.assertTrue(bool(q.solid_s1_s5) and q.kl_terus > 0.03 and q.thn_pos == q.thn_bil)
        self.assertGreater(B['ramal']['positif'], 0.9)


class TestJenisTrend(unittest.TestCase):
    """SPEC pindaan 16 Nov 2026 (w): tinjauan jenis dan tempoh trend menaik (zigzag ATR; deskriptif)."""

    def test_dikunci(self):
        import cs_jenis_trend as jt
        self.assertEqual(jt.SAIZ, ((2.0, 'kecil'), (4.0, 'sederhana'), (8.0, 'besar')))
        self.assertEqual([x[0] for x in jt.LAJU], [0.0025, 0.005, 0.01, np.inf])
        self.assertEqual((jt.MIN_SESI, jt.BULAN, [x[0] for x in jt.BAKUL][:3]), (5, 21, [21, 63, 126]))

    def test_zigzag_sintetik(self):
        import cs_jenis_trend as jt
        lin = lambda a, b, n: list(np.linspace(a, b, n + 1)[1:])
        c = np.asarray([100.0] + lin(100, 80, 10) + lin(80, 120, 20) + lin(120, 115, 2) + lin(115, 130, 6) + lin(130, 110, 5)
                       + lin(110, 150, 16) + lin(150, 100, 10))
        atr = np.full(len(c), 2.0)                                              # had = 4 x 2 = 8 mata
        T, P, U, D, G, n_awal, n_gantung = jt.zigzag(c, atr, np.asarray([0, len(c)]), 4.0)
        self.assertEqual((n_awal, n_gantung), (0, 0))
        self.assertEqual(c[T].tolist(), [80.0, 110.0])                          # dua trend: 80 -> 130 dan 110 -> 150
        self.assertEqual(c[P].tolist(), [130.0, 150.0])
        self.assertEqual((P - T).tolist(), [28, 16])
        self.assertAlmostEqual(G[0], 1 - 115 / 120)                             # turun di tengah jalan (tidak termasuk kejatuhan penamat)
        self.assertAlmostEqual(G[1], 0.0)
        self.assertTrue((c[U] >= c[T] + 8).all() and (c[U - 1] < c[T] + 8).all())    # dikenal pada bar pertama yang naik >= had
        self.assertTrue((c[D] <= c[P] - 8).all() and (c[D - 1] > c[P] - 8).all())    # disahkan tamat pada bar pertama yang jatuh >= had
        T2 = jt.zigzag(c[11:], atr[11:], np.asarray([0, len(c) - 11]), 4.0)     # bermula di dasar: ayunan pertama terpotong -> dibuang
        self.assertEqual((len(T2[0]), T2[5]), (1, 1))
        T3 = jt.zigzag(c[:-10], atr[:-10], np.asarray([0, len(c) - 10]), 4.0)   # trend terakhir belum tamat -> dibuang
        self.assertEqual((len(T3[0]), T3[6]), (1, 1))

    def test_zigzag_sifat_pada_data_rawak(self):
        import cs_jenis_trend as jt
        rng = np.random.default_rng(5)
        c = 50 * np.exp(np.cumsum(rng.normal(0.0003, 0.02, 3000)))
        mula = np.asarray([0, 1500, 3000])                                      # dua saham
        for k in (2.0, 4.0, 8.0):
            atr = np.full(len(c), 1.0)
            T, P, U, D, G, _, _ = jt.zigzag(c, atr, mula, k)
            self.assertGreater(len(T), 3)
            self.assertTrue((T < U).all() and (U <= P).all() and (P < D).all())
            self.assertTrue(((T < 1500) == (D < 1500)).all())                   # tiada trend merentas dua saham
            for t, p, d in zip(T, P, D):
                self.assertEqual(c[p], c[t:d + 1].max())
                self.assertEqual(c[t], c[t:p + 1].min())
            self.assertTrue((G >= 0).all() and (G * c[T] < k * 1.0).all())      # turun di tengah jalan (mata) sentiasa di bawah had

    def test_rekod(self):
        d = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'TREND')
        J = pd.read_csv(os.path.join(d, 'jenis_trend.csv'))
        s = J[J.jadual == 'saiz'].set_index('saiz')
        self.assertEqual(s.index.tolist(), ['kecil', 'sederhana', 'besar'])
        self.assertTrue(s.sesi_50.is_monotonic_increasing and s.naik_50.is_monotonic_increasing)
        self.assertTrue(s.setahun.is_monotonic_decreasing)
        for jd in ('tempoh', 'jenis'):
            for _, g in J[J.jadual == jd].groupby('saiz'):
                self.assertAlmostEqual(float(g.bahagian.sum()), 1.0, places=3)
                self.assertEqual(int(g.n.sum()), int(s.n[g.saiz.iloc[0]]))
        md = open(os.path.join(d, 'JENIS_TREND.md'), encoding='utf-8').read()
        self.assertIn('BUKAN isyarat beli atau jual', md)
        self.assertIn('Bahagian yang boleh dikenal semasa berlaku', md)


CAP_F_LAMA = 'e4b8fd20bb8f78a123e32c2eef75c55c42c8f27e1a50ee81ea2b4a7b7001edd5'


if __name__ == '__main__':
    unittest.main()
