"""Ujian bagi `REVERSE/semak_latih.py` — pengesah bebas SEMAKAN_LATIH.md.

Ujian ini memastikan laporan tidak boleh hanyut daripada fail keputusan tanpa CI gagal,
dan bahawa pengesah itu sendiri masih menangkap kes yang sepatutnya ditangkap.
"""
import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

AKAR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(AKAR))

import REVERSE.semak_latih as SL  # noqa: E402


class TestSemakLatih(unittest.TestCase):
    def test_semua_nombor_dihasilkan_semula(self):
        """Kesemua nombor SEMAKAN_LATIH.md mesti dihasilkan semula; --semak keluar 0."""
        with redirect_stdout(io.StringIO()) as buf:
            kod = SL.main(['--semak'])
        self.assertEqual(kod, 0, buf.getvalue()[-3000:])
        self.assertIn('dihasilkan semula melalui laluan bebas', buf.getvalue())

    def test_sifar_kesan_cagr_luar_sampel_melepasi_fdr(self):
        """Dapatan teras: tiada kesan CAGR luar sampel melepasi BH-FDR."""
        with redirect_stdout(io.StringIO()) as buf:
            SL.main([])
        self.assertIn('kesan CAGR luar sampel melepasi FDR: 0', buf.getvalue())
        self.assertIn('kesan MDD  luar sampel melepasi FDR: 3', buf.getvalue())

    def test_ujian_tanda_betul(self):
        """Ujian tanda dua-hujung pada kes yang diketahui."""
        self.assertEqual(SL.tanda([1.0] * 5)[2], 2 / 32)
        self.assertEqual(SL.tanda([1, -1])[:2], (1, 2))
        self.assertEqual(SL.tanda([1.0, -1.0])[2], 1.0)
        self.assertEqual(SL.tanda([0.0, 0.0])[1], 0)          # seri diabaikan
        self.assertAlmostEqual(SL.tanda([1, 1, 1, 1, 1, 1, -1])[2], 0.125)

    def test_bh_memilih_prefiks_tersusun(self):
        """BH mesti memulangkan senarai tersusun dan indeks potong yang betul."""
        uji = [('a', 0.001), ('b', 0.2), ('c', 0.009), ('d', 0.9)]
        u, amb, kmax = SL.bh(uji, q=0.05)
        self.assertEqual([r[0] for r in u], ['a', 'c', 'b', 'd'])
        self.assertEqual(kmax, 1)                              # 0.001 dan 0.009 lulus
        self.assertAlmostEqual(amb[0], 0.0125)

    def test_pengesah_menangkap_dakwaan_salah(self):
        """Jika dakwaan dipalsukan, --semak MESTI keluar 1 (ujian tidak sia-sia)."""
        asal = SL.DAKWA_A['1']
        SL.DAKWA_A['1'] = (99.0,) + asal[1:]
        try:
            with redirect_stdout(io.StringIO()) as buf:
                kod = SL.main(['--semak'])
            self.assertEqual(kod, 1)
            self.assertIn('TIDAK DIHASILKAN SEMULA', buf.getvalue())
        finally:
            SL.DAKWA_A['1'] = asal

    def test_sel_degenerat_memberi_sifar_tepat(self):
        """A2/A3 x U02 ialah tiada-op ikut binaan -> Δ = 0.00 tepat."""
        import csv
        import statistics as stx
        with (AKAR / 'REVERSE' / 'hierarki.csv').open() as fh:
            H = list(csv.DictReader(fh))
        med, _ = SL.med_sel(H, ['saring', 'urutan', 'slot', 'had'], 'cagr')
        for sr in ('A2', 'A3'):
            d = [v - med[('A0', u, s, h)]
                 for (sg, u, s, h), v in med.items() if sg == sr and u == 'U02']
            self.assertEqual(len(d), 4)
            self.assertAlmostEqual(stx.median(d), 0.0, places=6)


if __name__ == '__main__':
    unittest.main()
