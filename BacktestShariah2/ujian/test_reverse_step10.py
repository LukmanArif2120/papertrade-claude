"""Join peristiwa sah x lajur SEC (REVERSE/step10_sec.py; SPEC_FASA2.md §4.2-§4.3).

Ujian di sini mengunci sifat tiada-lookahead secara struktur, bukan dengan memeriksa keputusan.
"""
import json, os, sys, unittest

import numpy as np
import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'REVERSE'))
import step10_sec as T  # noqa: E402

H = pd.DatetimeIndex(['2024-02-01', '2024-05-02', '2024-08-01', '2024-10-31', '2025-02-05']).to_numpy()


class TestKitaran(unittest.TestCase):
    def test_pengumuman_pertama_tiada_jangkaan(self):
        self.assertTrue(pd.isna(T._kitaran(H)[0]))

    def test_jangkaan_guna_selang_lalu_sahaja(self):
        j = T._kitaran(H)
        # jangkaan[1] = hari[1] + selang pertama (91 hari)
        self.assertEqual(pd.Timestamp(j[1]), pd.Timestamp('2024-05-02') + pd.Timedelta(days=91))

    def test_hirisan_tidak_berubah_oleh_masa_hadapan(self):
        """Sifat utama: jangkaan untuk k pengumuman pertama mesti sama sama ada baris kemudian ada
        atau tidak. Kalau kiraan pernah melihat ke hadapan, ujian ini gagal."""
        penuh = T._kitaran(H)
        for k in range(1, len(H) + 1):
            sebahagian = T._kitaran(H[:k])
            a = pd.to_datetime(penuh[:k])
            b = pd.to_datetime(sebahagian)
            self.assertTrue(((a == b) | (pd.isna(a) & pd.isna(b))).all(), k)

    def test_selang_terlalu_panjang_diabaikan(self):
        h = pd.DatetimeIndex(['2020-01-01', '2024-01-01', '2024-04-01']).to_numpy()
        j = T._kitaran(h)
        self.assertTrue(pd.isna(j[0]))
        self.assertTrue(pd.isna(j[1]))                      # selang 4 tahun > SELANG_MAKS
        self.assertFalse(pd.isna(j[2]))                     # selang 91 hari diterima

    def test_satu_pengumuman(self):
        j = T._kitaran(H[:1])
        self.assertEqual(len(j), 1)
        self.assertTrue(pd.isna(j[0]))


class TestJoinTiadaLookahead(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p = os.path.join(AKAR, 'REVERSE', 'sec_join.csv')
        if not os.path.exists(p):
            raise unittest.SkipTest('REVERSE/sec_join.csv belum dijana')
        cls.g = pd.read_csv(p, parse_dates=['tarikh', 'hari_tersedia', 'tarikh_umum'])

    def test_hari_tersedia_tidak_pernah_selepas_peristiwa(self):
        """Nilai SEC yang dilekatkan mesti sudah tersedia pada hari peristiwa."""
        a = self.g.dropna(subset=['hari_tersedia'])
        self.assertTrue(len(a) > 0)
        self.assertTrue((a.hari_tersedia <= a.tarikh).all())

    def test_hari_sejak_earnings_tidak_negatif(self):
        h = self.g.hari_sejak_earnings.dropna()
        self.assertTrue(len(h) > 0)
        self.assertGreaterEqual(h.min(), 0)

    def test_pengumuman_mendahului_ketersediaan(self):
        """§4.2: hari tersedia >= tarikh pengumuman (selepas tutup -> sesi berikut)."""
        a = self.g.dropna(subset=['hari_tersedia', 'tarikh_umum'])
        self.assertTrue((a.hari_tersedia >= a.tarikh_umum).all())

    def test_liputan_cukup_tahun_layak(self):
        """§9.7: ambang 3,000 dikenakan SETIAP TAHUN, dan §9.5 menuntut >= 10 tahun layak.

        Bukan "semua tahun lulus": mandat XBRL berperingkat 2009-2011 bermakna tahun awal
        (2012-2014) boleh kekal di bawah ambang dan dikecualikan. Yang mesti benar ialah tahun
        yang LAYAK cukup banyak untuk penilaian dijalankan."""
        p = os.path.join(AKAR, 'REVERSE', 'sec_liputan.csv')
        if not os.path.exists(p):
            self.skipTest('sec_liputan.csv belum dijana')
        # Semasa isian awal SEC belum siap, liputan memang belum cukup: itu keadaan yang
        # dijangka, bukan kegagalan. Penegasan hanya bermakna selepas belum_diisi = 0.
        st = os.path.join(AKAR, 'BacktestShariah2', 'data', 'sec', 'status.json')
        if os.path.exists(st):
            with open(st, encoding='utf-8') as f:
                baki = json.load(f).get('belum_diisi')
            if baki not in (0, '0'):
                self.skipTest(f'isian awal SEC belum siap (belum_diisi={baki})')
        L = pd.read_csv(p)
        for k in T.LAJUR_SEC:
            layak = int((L[f'n_{k}'] >= 3000).sum())
            self.assertGreaterEqual(layak, 10, f'{k}: hanya {layak} tahun layak daripada {len(L)}')

    def test_tiada_lajur_hasil_dalam_join(self):
        """Peringkat 2 ialah BINA JOIN sahaja: tiada lajur pulangan/hasil, supaya pradaftar §5 kekal."""
        larang = {'pulangan', 'hasil_run', 'puncak', 'pulangan_dagangan', 'ekuiti', 'mdd'}
        self.assertEqual(larang & set(self.g.columns), set())


class TestLajurDikunci(unittest.TestCase):
    def test_lajur_sec_dikunci(self):
        # SPEC_FASA2.md §2: tiada tambahan lajur separuh jalan.
        self.assertEqual(T.LAJUR_SEC, ['sue', 'tumbuh_hasil', 'pecutan_hasil'])

    def test_tarikh_8k_sebenar_berikut_tidak_diguna(self):
        """§4.3: hanya jangkaan daripada kitaran lalu. Kod tidak boleh mengandungi merge arah 'forward'."""
        with open(os.path.join(AKAR, 'REVERSE', 'step10_sec.py'), encoding='utf-8') as f:
            src = f.read()
        self.assertIn("direction='backward'", src)
        self.assertNotIn("direction='forward'", src)
        self.assertNotIn("direction='nearest'", src)


if __name__ == '__main__':
    unittest.main()
