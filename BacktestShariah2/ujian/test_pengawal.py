"""Ujian pengawal.py — semakan kesegaran papertrade M dan N, dan SEMPADAN auto-betul.

Ujian yang paling penting dalam fail ini ialah `test_sempadan_auto_betul`. Pengawal yang
membetulkan terlalu banyak lebih berbahaya daripada pengawal yang membetulkan terlalu sedikit:
mengisi gred dengan nilai hari ini menukar medan titik-masa menjadi maklumat masa hadapan, dan
memecah dokumen db sebelum halaman dashboard ditukar kepada subBhg() membuat halaman kehilangan
baris secara SENYAP. Kedua-duanya kelihatan seperti pembetulan dan kedua-duanya merosakkan data.
"""
import csv
import json
import os
import sys
import tempfile
import unittest

import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'standard'))

import pengawal as P  # noqa: E402

LAJUR = ['saham', 'kaedah', 'id_kaedah', 'tarikh_beli', 'tarikh_isyarat', 'harga_beli',
         'harga_terkini', 'keluar', 'tidak_dibeli', 'sumber', 'keluar_henti']


def tulis(dir_, baris):
    os.makedirs(dir_, exist_ok=True)
    with open(os.path.join(dir_, 'claude.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=LAJUR)
        w.writeheader()
        for r in baris:
            w.writerow({k: r.get(k, '') for k in LAJUR})


def pos(saham, kaedah, **kw):
    d = dict(saham=saham, kaedah=kaedah, id_kaedah=kaedah, tarikh_beli='2026-11-02',
             tarikh_isyarat='2026-10-30', harga_beli='10', harga_terkini='11',
             keluar='', tidak_dibeli='', sumber='isyarat', keluar_henti='False')
    d.update(kw)
    return d


def sediakan(tmp, baris, malam, sesi=('2026-10-30', '2026-11-02')):
    pt = os.path.join(tmp, 'pt')
    tulis(pt, baris)
    with open(os.path.join(pt, 'status_harian.json'), 'w', encoding='utf-8') as f:
        json.dump(dict(malam=malam, beli=dict(tarikh='2026-11-02', direkod=2)), f)
    stor = os.path.join(tmp, 'stor')
    os.makedirs(stor, exist_ok=True)
    d = pd.DataFrame(dict(ticker='SPY', date=[int(s.replace('-', '')) for s in sesi],
                          open=1.0, high=1.0, low=1.0, close=1.0, volume=1))
    d.to_csv(os.path.join(stor, 'harga_idx.csv'), index=False)
    for t, f_ in (('AAA', 'harga_A.csv'), ('BBB', 'harga_B.csv')):
        pd.DataFrame(dict(ticker=t, date=[int(s.replace('-', '')) for s in sesi],
                          open=1.0, high=1.0, low=1.0, close=1.0, volume=1)).to_csv(
            os.path.join(stor, f_), index=False)
    lj = os.path.join(tmp, 'lejar')
    os.makedirs(lj, exist_ok=True)
    with open(os.path.join(lj, 'status.json'), 'w', encoding='utf-8') as f:
        json.dump(dict(sesi_terakhir=sesi[-1]), f)
    return pt, stor, lj


MALAM_OK = dict(sesi='2026-11-02', senarai_keluarga={'M': 10, 'N': 20},
                ralat_kaedah=[], kaedah_tanpa_modul=[])


def nama(S, n):
    return next(h for h in S.hasil if h['nama'] == n)


class TestSemakan(unittest.TestCase):
    def jalankan(self, baris, malam, **kw):
        tmp = tempfile.mkdtemp()
        pt, stor, lj = sediakan(tmp, baris, malam, **kw)
        return P.semak(pt, stor, lj, None)

    def test_keadaan_baik(self):
        S = self.jalankan([pos('AAA', 'M01', keluar_henti='True'),
                           pos('BBB', 'N19X13', keluar_henti='True')], MALAM_OK)
        for n in ('sesi terkini diproses', 'senarai beli ada Mxx', 'senarai beli ada Nxx',
                  'posisi Mxx dikemas kini', 'posisi Nxx dikemas kini', 'lejar segar'):
            self.assertTrue(nama(S, n)['ok'], n + ': ' + nama(S, n)['butiran'])

    def test_kohort_n_hilang_dikesan(self):
        """Semakan yang menjawab soalan sebenar pengguna: adakah Nxx masih hidup?"""
        m = dict(MALAM_OK, senarai_keluarga={'M': 10})
        S = self.jalankan([pos('AAA', 'M01', keluar_henti='True')], m)
        self.assertTrue(nama(S, 'senarai beli ada Mxx')['ok'])
        self.assertFalse(nama(S, 'senarai beli ada Nxx')['ok'])

    def test_sesi_tertinggal_dikesan_dan_boleh_dibetulkan(self):
        m = dict(MALAM_OK, sesi='2026-10-30')
        S = self.jalankan([pos('AAA', 'M01', keluar_henti='True')], m)
        h = nama(S, 'sesi terkini diproses')
        self.assertFalse(h['ok'])
        self.assertTrue(h['boleh_betul'])
        self.assertIn('kejar.py', ' '.join(h['remedi']))

    def test_posisi_n_tidak_dikemas_kini_dikesan(self):
        """Pepijat 3 Nov 2026: 835 posisi Nxx tidak dikemas kini dan tiada apa-apa menyedarinya."""
        S = self.jalankan([pos('AAA', 'M01', keluar_henti='True'),
                           pos('BBB', 'N19X13', harga_terkini='', keluar_henti='True')], MALAM_OK)
        self.assertTrue(nama(S, 'posisi Mxx dikemas kini')['ok'])
        self.assertFalse(nama(S, 'posisi Nxx dikemas kini')['ok'])

    def test_ralat_kaedah_dilaporkan(self):
        m = dict(MALAM_OK, ralat_kaedah=['N19X13: sedia: KeyError'])
        S = self.jalankan([pos('AAA', 'M01', keluar_henti='True')], m)
        self.assertFalse(nama(S, 'tiada kaedah ralat')['ok'])

    def test_lorong2_baki_sah_diterima(self):
        """Posisi yang tickernya tiada bar pada hari beli tidak boleh dinilai oleh sesiapa.
        Pengawal yang menjerit setiap hari tentang itu akan diabaikan."""
        S = self.jalankan([pos('AAA', 'M01', keluar_henti='True'),
                           pos('ZZZ', 'N19X13', keluar_henti='')], MALAM_OK)   # ZZZ tiada dalam stor
        h = nama(S, 'lorong 2 dinilai')
        self.assertTrue(h['ok'], h['butiran'])
        self.assertIn('tidak boleh', h['butiran'])

    def test_lorong2_boleh_dinilai_dikesan(self):
        """Tetapi posisi yang ADA bar dan masih tiada lorong 2 ialah kegagalan sebenar."""
        S = self.jalankan([pos('AAA', 'M01', keluar_henti=''),
                           pos('BBB', 'N19X13', keluar_henti='True')], MALAM_OK)
        h = nama(S, 'lorong 2 dinilai')
        self.assertFalse(h['ok'], h['butiran'])
        self.assertTrue(h['boleh_betul'])


class TestSempadanAutoBetul(unittest.TestCase):
    """Apa yang pengawal dibenarkan betulkan SENDIRI ialah keputusan reka bentuk, bukan kebetulan."""

    BOLEH = {'sesi terkini diproses', 'lorong 2 dinilai', 'fail posisi dalam had db', 'sahkan.py 0 ralat'}

    def test_senarai_remedi_tepat(self):
        tmp = tempfile.mkdtemp()
        pt, stor, lj = sediakan(tmp, [pos('AAA', 'M01', keluar_henti='True')], MALAM_OK)
        S = P.semak(pt, stor, lj, None)
        boleh = {h['nama'] for h in S.hasil if h['boleh_betul']}
        self.assertEqual(boleh, self.BOLEH,
                         'Senarai remedi automatik berubah. Setiap tambahan mesti idempoten DAN '
                         'tidak membuat keputusan baharu - lihat docstring pengawal.py.')

    def test_yang_tidak_boleh_kekal_tidak_boleh(self):
        """Gred, kaedah ralat, lejar dan belian TIDAK boleh diauto-betulkan: masing-masing
        memerlukan keputusan manusia atau milik workflow lain."""
        tmp = tempfile.mkdtemp()
        pt, stor, lj = sediakan(tmp, [pos('AAA', 'M01', keluar_henti='True')], MALAM_OK)
        S = P.semak(pt, stor, lj, None)
        for n in ('tiada kaedah ralat', 'tiada posisi tanpa modul', 'lejar segar', 'belian direkod',
                  'semua modul kaedah dimuat', 'senarai beli ada Nxx'):
            self.assertFalse(nama(S, n)['boleh_betul'], n)


if __name__ == '__main__':
    unittest.main()
