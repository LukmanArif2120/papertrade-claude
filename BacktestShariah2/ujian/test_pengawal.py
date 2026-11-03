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


def sediakan(tmp, baris, malam, sesi=('2026-10-30', '2026-11-02'), lejar_sesi=None):
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
        json.dump(dict(sesi_terakhir=lejar_sesi or sesi[-1]), f)
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

    def test_sesi_tertinggal_dikesan(self):
        """Sesi terkini belum diproses: dikesan, dan dirutekan kepada harian.yml - bukan kejar.py,
        yang sengaja tidak menyentuh sesi terkini (lihat TestRoutingRemedi)."""
        m = dict(MALAM_OK, sesi='2026-10-30')
        S = self.jalankan([pos('AAA', 'M01', keluar_henti='True')], m)
        h = nama(S, 'sesi terkini diproses')
        self.assertFalse(h['ok'])
        self.assertEqual(h['cetus'], 'harian.yml')

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


class TestRoutingRemedi(unittest.TestCase):
    """Remedi mesti dipadankan dengan BENTUK jurang, bukan dengan nama semakan.

    kejar.py sengaja tidak menyentuh sesi TERKINI (itu kerja langkah malam harian.yml). Jadi
    memanggilnya apabila yang hilang ialah sesi terkini tidak melakukan apa-apa - pengawal akan
    melaporkan "remedi jalan tetapi semakan masih gagal", iaitu jujur tetapi tidak berguna. Kes itu
    ditemui oleh ujian hujung-ke-hujung pada 3 Nov 2026, bukan oleh pembacaan kod.
    """

    def jalankan(self, sesi_diproses, lejar_sesi=None):
        tmp = tempfile.mkdtemp()
        m = dict(MALAM_OK, sesi=sesi_diproses)
        pt, stor, lj = sediakan(tmp, [pos('AAA', 'M01', keluar_henti='True')], m,
                                sesi=('2026-10-29', '2026-10-30', '2026-11-02'),
                                lejar_sesi=lejar_sesi)
        return P.semak(pt, stor, lj, None)

    def test_lubang_di_belakang_guna_kejar(self):
        h = nama(self.jalankan('2026-10-29'), 'sesi terkini diproses')
        self.assertTrue(h['boleh_betul'])
        self.assertIn('kejar.py', ' '.join(h['remedi']))
        self.assertIsNone(h['cetus'])
        self.assertIn('lubang di belakang', h['butiran'])

    def test_sesi_terkini_hilang_cetus_harian(self):
        """Tiada lubang di belakang, cuma sesi terkini: harian.yml belum menjalankan tugasnya."""
        h = nama(self.jalankan('2026-10-30'), 'sesi terkini diproses')
        self.assertFalse(h['boleh_betul'], 'jangan panggil kejar di sini: ia tidak akan buat apa-apa')
        self.assertIsNone(h['remedi'])
        self.assertEqual(h['cetus'], 'harian.yml')

    def test_lejar_basi_cetus_lejar(self):
        h = nama(self.jalankan('2026-11-02', lejar_sesi='2026-10-30'), 'lejar segar')
        self.assertFalse(h['ok'])
        self.assertEqual(h['cetus'], 'lejar.yml')
        self.assertFalse(h['boleh_betul'], 'lejar 46 minit: cetus workflownya, jangan jalankan di sini')


class TestHadKejarPengawal(unittest.TestCase):
    """Pengawal memegang kunci concurrency `papertrade`, dan beli.yml berkongsi kunci itu.

    beli.yml ada pintu KERAS 09:31-17:00 NY. Jika rantaian beratur menolak beli melepasi 17:00
    NY, belian hari itu TIDAK berlaku - dan tidak seperti imbasan, ia tidak boleh dikejar esok:
    harga buka hari itu sudah berlalu. Jadi berapa lama pengawal memegang kunci ialah soalan
    integriti data, bukan soalan prestasi."""

    def test_had_lalai_dua_sesi(self):
        import argparse
        ap = argparse.ArgumentParser()
        P.main.__globals__  # pastikan modul dimuat
        tmp = tempfile.mkdtemp()
        m = dict(MALAM_OK, sesi='2026-10-29')
        pt, stor, lj = sediakan(tmp, [pos('AAA', 'M01', keluar_henti='True')], m,
                                sesi=('2026-10-29', '2026-10-30', '2026-11-02'))
        a = argparse.Namespace(maks_kejar=2)
        h = nama(P.semak(pt, stor, lj, a), 'sesi terkini diproses')
        self.assertIn('--maks', h['remedi'])
        self.assertEqual(h['remedi'][h['remedi'].index('--maks') + 1], '2',
                         'had kejar pengawal mesti kecil: ia memegang kunci yang beli.yml perlukan')
        del ap


class TestSempadanAutoBetul(unittest.TestCase):
    """Apa yang pengawal dibenarkan betulkan SENDIRI ialah keputusan reka bentuk, bukan kebetulan."""

    BOLEH = {'sesi terkini diproses', 'lorong 2 dinilai', 'fail posisi dalam had db', 'sahkan.py 0 ralat'}

    def test_senarai_remedi_tepat(self):
        tmp = tempfile.mkdtemp()
        pt, stor, lj = sediakan(tmp, [pos('AAA', 'M01', keluar_henti='True')], MALAM_OK)
        S = P.semak(pt, stor, lj, None)
        boleh = {h['nama'] for h in S.hasil if h['boleh_betul']}
        self.assertTrue(boleh <= self.BOLEH,
                        f'Remedi automatik baharu: {boleh - self.BOLEH}. Setiap tambahan mesti '
                        'idempoten DAN tidak membuat keputusan baharu - lihat docstring pengawal.py.')
        # Setiap nama dalam BOLEH mesti wujud sebagai semakan: senarai tidak boleh hanyut diam-diam.
        self.assertTrue(self.BOLEH <= {h['nama'] for h in S.hasil})

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
