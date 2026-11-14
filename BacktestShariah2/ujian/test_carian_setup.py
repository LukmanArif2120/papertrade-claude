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
        lama = t[~t.pusingan.isin(['CS05', 'CS06', 'CS07'])]
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
        lama = reg[~reg.pusingan.isin(['CS05', 'CS06', 'CS07'])]
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


if __name__ == '__main__':
    unittest.main()
