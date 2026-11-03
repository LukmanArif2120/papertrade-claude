"""Ujian watchlist Nxx: syarat terurai MESTI setara dengan topeng masuk sebenar.

Watchlist melaporkan "berapa hampir" sesuatu saham daripada mencetus. Untuk itu setiap masuk
Nxx perlu diurai kepada syarat atom (`_nxx.SYARAT_MASUK`). Penguraian itu DITULIS TANGAN di
sebelah topeng, bukan diterbitkan daripadanya - pilihan yang disengajakan, supaya laluan imbasan
yang menghasilkan isyarat tidak perlu disentuh langsung.

Harga pilihan itu ialah risiko PESONG: satu salah taip (`< 30` sedangkan topeng `<= 30`, atau
syarat tertinggal) dan watchlist melaporkan "hampir mencetus" bagi peraturan yang BUKAN peraturan
sebenar - tanpa ralat, tanpa petunjuk, pada setiap hari. Ujian ini ialah satu-satunya perkara
yang menghalangnya: ia membandingkan DAN bagi syarat terurai dengan topeng asal, bar demi bar,
pada HARGA SEBENAR daripada stor. Jika ia gagal, penguraian itu salah - bukan ujian ini.
"""
import os
import sys
import unittest

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BS2 = os.path.join(AKAR, 'BacktestShariah2')
sys.path.insert(0, os.path.join(BS2, 'kod'))
sys.path.insert(0, os.path.join(BS2, 'kod', 'kaedah'))
sys.path.insert(0, os.path.join(BS2, 'standard'))

import _nxx as NX  # noqa: E402

STOR = os.path.join(BS2, 'data', 'harga', 'stor')
N_TICKER = 40          # cukup untuk menemui kedua-dua keadaan benar dan palsu bagi setiap syarat


def muat_ticker(n=N_TICKER):
    from stor import frames_dict, muat
    fr, _ = frames_dict(muat(STOR))
    tk = [t for t in sorted(fr) if len(fr[t]) >= 300][:n]
    return {t: fr[t] for t in tk}


@unittest.skipUnless(os.path.exists(os.path.join(STOR, 'harga_idx.csv')), 'stor harga tiada')
class TestSyaratSetaraTopeng(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fr = muat_ticker()
        cls.ind = {t: NX.indikator(g) for t, g in cls.fr.items()}

    def test_setiap_masuk_setara(self):
        """DAN(syarat terurai) == topeng masuk, pada setiap bar setiap ticker."""
        import inspect

        import numpy as np
        gagal = []
        for nama, fn in sorted(NX.SYARAT_MASUK.items()):
            masuk = getattr(NX, nama)
            # Tanda tangan BERBEZA dan bilangan parameter TIDAK memadai: n119 mengambil (g)
            # sahaja, bukan (f). Memanggilnya dengan f memberi AttributeError yang mengelirukan,
            # jadi parameter dipadankan ikut NAMA.
            par = list(inspect.signature(masuk).parameters)
            beza_jumlah = 0
            for t, g in self.fr.items():
                f = self.ind[t]
                hujah = {'f': f, 'g': g}
                topeng = masuk(*[hujah[x] for x in par]).fillna(False).astype(bool)
                kon = None
                for _, c, _j in fn(f, g):
                    c = c.fillna(False).astype(bool) if hasattr(c, 'fillna') else c
                    kon = c if kon is None else (kon & c)
                beza = int((np.asarray(kon) != np.asarray(topeng)).sum())
                beza_jumlah += beza
            if beza_jumlah:
                gagal.append(f'{nama}: {beza_jumlah} bar berbeza')
        self.assertEqual(gagal, [], 'penguraian syarat terpesong daripada topeng masuk:\n  ' +
                         '\n  '.join(gagal))

    def test_liputan_masuk_yang_dipakai(self):
        """Setiap masuk yang 94 modul produksi pakai mesti ada dalam jadual."""
        import glob
        import re
        dipakai = set()
        for p in glob.glob(os.path.join(BS2, 'kod', 'kaedah', 'N*.py')):
            with open(p, encoding='utf-8') as fh:
                dipakai |= set(re.findall(r'NX\.(n\d+)\(', fh.read()))
        hilang = sorted(dipakai - set(NX.SYARAT_MASUK))
        self.assertEqual(hilang, [], f'masuk produksi tanpa penguraian syarat: {hilang}')


@unittest.skipUnless(os.path.exists(os.path.join(STOR, 'harga_idx.csv')), 'stor harga tiada')
class TestBentukSyarat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fr = muat_ticker(12)
        cls.ind = {t: NX.indikator(g) for t, g in cls.fr.items()}

    def test_triple_sah(self):
        """syarat() mesti memulangkan (label: str, dipenuhi: bool, jarak: float|None)."""
        for nama in sorted(NX.SYARAT_MASUK):
            for t, g in self.fr.items():
                for label, ok, j in NX.syarat(nama, self.ind[t], g):
                    self.assertIsInstance(label, str, nama)
                    self.assertIsInstance(ok, bool, nama)
                    self.assertTrue(j is None or isinstance(j, float), f'{nama} {label}: {j!r}')
                    if j is not None:
                        self.assertGreaterEqual(j, 0.0, f'{nama} {label}: jarak negatif')

    def test_jarak_hanya_bagi_yang_belum(self):
        """Jarak hanya bermakna bagi syarat yang BELUM dipenuhi; yang sudah mesti None."""
        for nama in sorted(NX.SYARAT_MASUK):
            for t, g in self.fr.items():
                for label, ok, j in NX.syarat(nama, self.ind[t], g):
                    if ok:
                        self.assertIsNone(j, f'{nama} {label}: sudah dipenuhi tetapi ada jarak')

    def test_hampir_syarat_menolak_hujung(self):
        """Semua sudah (= isyarat) atau semua belum (terlalu jauh) bukan calon watchlist."""
        self.assertIsNone(NX.hampir_syarat([('a', True, None), ('b', True, None)], 300, 60))
        self.assertIsNone(NX.hampir_syarat([('a', False, 1.0), ('b', False, 2.0)], 300, 60))
        d = NX.hampir_syarat([('a', True, None), ('b', False, 3.0)], 300, 60)
        self.assertEqual(d['syarat_dipenuhi'], '1/2')
        self.assertEqual(d['jarak_pct'], 3.0)
        self.assertIsNone(d['paras'], 'paras harga tidak boleh didakwa bagi ambang indikator')

    def test_bar_tidak_cukup(self):
        self.assertIsNone(NX.hampir_syarat([('a', True, None), ('b', False, 1.0)], 10, 60))


if __name__ == '__main__':
    unittest.main()
