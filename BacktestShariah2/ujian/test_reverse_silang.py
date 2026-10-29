"""Ujian unit bagi REVERSE/step13_silang.py (grid dikunci, parsing lajur, pembekuan kuintil)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(AKAR))
from REVERSE import step13_silang as SX  # noqa: E402


class TestGridDikunci(unittest.TestCase):
    """Spec §3 menetapkan grid; melebarkannya memerlukan pradaftar baharu."""

    def test_enam_konteks_harga(self):
        self.assertEqual(len(SX.HARGA), 6)
        self.assertEqual(SX.HARGA, ['atr_pct', 'julat20', 'bb_lebar', 'cerun_ma50',
                                    'j_ma200', 'j_52w_tinggi'])

    def test_empat_syarat_sec(self):
        self.assertEqual(len(SX.SEC), 4)
        self.assertIn('q5:pecutan_hasil&sejak_earnings_le5', SX.SEC)

    def test_grid_silang_48(self):
        # 6 lajur harga x 2 hujung x 4 syarat SEC = 48
        self.assertEqual(len(SX.HARGA) * 2 * len(SX.SEC), 48)

    def test_gate_a_ambang_sama_dengan_fasa2(self):
        from REVERSE import step11_sec_nilai as S11
        self.assertEqual(SX.MIN_N, S11.MIN_N)
        self.assertEqual(SX.PECAHAN_KONSISTEN, S11.PECAHAN_KONSISTEN)
        self.assertEqual(SX.MIN_TAHUN, S11.MIN_TAHUN)
        self.assertEqual(SX.AMBANG_TAHUN, S11.AMBANG_TAHUN)

    def test_tahun_min_sama_dengan_fasa2(self):
        self.assertEqual(SX.TAHUN_MIN, 2012)


class TestLajurAsas(unittest.TestCase):
    def test_kuintil_harga_tunggal(self):
        self.assertEqual(SX.lajur_asas('q5:atr_pct'), ['atr_pct'])

    def test_kuintil_sec_tunggal(self):
        self.assertEqual(SX.lajur_asas('q1:sue'), ['sue'])

    def test_silang_dua_lajur(self):
        self.assertEqual(SX.lajur_asas('q5:atr_pct+q5:sue'), ['atr_pct', 'sue'])

    def test_silang_tiga_bahagian(self):
        # Induk SEC yang sendirinya kombinasi: q5:pecutan_hasil&sejak_earnings_le5
        r = SX.lajur_asas('q5:julat20+q5:pecutan_hasil&sejak_earnings_le5')
        self.assertEqual(r, ['julat20', 'pecutan_hasil'])

    def test_tingkap_earnings_bukan_lajur_data(self):
        # sejak_earnings_le5 bukan lajur kuintil; ia tidak menyekat populasi.
        self.assertEqual(SX.lajur_asas('sejak_earnings_le5'), [])


class TestBatasHarga(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.asal = SX.CACHE
        SX.CACHE = Path(self.tmp.name)

    def tearDown(self):
        SX.CACHE = self.asal
        self.tmp.cleanup()

    def _d(self, n=500, geser=0.0):
        rng = np.random.default_rng(7)
        return pd.DataFrame({k: rng.normal(geser, 1.0, n) for k in SX.HARGA})

    def test_membeku_pada_larian_pertama(self):
        b = SX.batas_harga(self._d())
        self.assertTrue((SX.CACHE / 'kuintil_harga.json').exists())
        self.assertEqual(sorted(b), sorted(SX.HARGA))
        for k in SX.HARGA:
            self.assertLess(b[k]['q1'], b[k]['q5'])

    def test_larian_kedua_guna_nilai_beku(self):
        b1 = SX.batas_harga(self._d())
        # Data yang SANGAT berbeza tidak boleh menukar sempadan yang sudah dibekukan.
        b2 = SX.batas_harga(self._d(geser=100.0))
        self.assertEqual(b1, b2)

    def test_lajur_terlalu_sedikit_dilangkau(self):
        b = SX.batas_harga(self._d(n=50))
        self.assertEqual(b, {})

    def test_fail_beku_json_sah(self):
        SX.batas_harga(self._d())
        j = json.loads((SX.CACHE / 'kuintil_harga.json').read_text())
        self.assertTrue(all('n' in v for v in j.values()))


if __name__ == '__main__':
    unittest.main()
