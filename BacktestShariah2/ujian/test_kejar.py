"""Ujian kejar.py — pemilihan sesi tertinggal dan sumber harga buka lampau.

Yang diuji di sini ialah LOGIK PEMILIHAN, bukan imbasan kaedah: imbasan itu `harian_c.cmd_malam`
yang sama yang sudah diuji di tempat lain, dan kejar.py memanggilnya melalui subproses dengan
hujah yang sama seperti produksi. Ujian `test_subproses_produksi` memastikan laluan panggilan itu
sendiri hidup — pelajaran 1 Nov 2026: ujian yang mengimport modul terus boleh lulus sambil
produksi gagal dengan ModuleNotFoundError.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STD = os.path.join(AKAR, 'BacktestShariah2', 'standard')
sys.path.insert(0, STD)

import kejar as K  # noqa: E402


def stor_palsu(dir_, sesi):
    os.makedirs(dir_, exist_ok=True)
    pd.DataFrame(dict(ticker=['SPY'] * len(sesi), date=[int(s.replace('-', '')) for s in sesi],
                      open=1.0, high=1.0, low=1.0, close=1.0, volume=1)).to_csv(
        os.path.join(dir_, 'harga_idx.csv'), index=False)


def folder_palsu(dir_, malam_sesi, beli_tarikh=None):
    os.makedirs(dir_, exist_ok=True)
    st = {'malam': {'sesi': malam_sesi}}
    if beli_tarikh:
        st['beli'] = {'tarikh': beli_tarikh}
    with open(os.path.join(dir_, 'status_harian.json'), 'w', encoding='utf-8') as f:
        json.dump(st, f)


def jalan(args):
    p = subprocess.run([sys.executable, os.path.join(STD, 'kejar.py')] + args,
                       capture_output=True, text=True)
    return p, json.loads((p.stdout or p.stderr).strip().splitlines()[-1])


class TestPilihSesi(unittest.TestCase):
    SESI = ['2026-10-28', '2026-10-29', '2026-10-30', '2026-11-02']

    def sediakan(self, tmp, malam_sesi, beli=None):
        stor_palsu(os.path.join(tmp, 'stor'), self.SESI)
        folder_palsu(os.path.join(tmp, 'pt'), malam_sesi, beli)
        return ['--folder', os.path.join(tmp, 'pt'), '--stor', os.path.join(tmp, 'stor'),
                '--isyarat', os.path.join(tmp, 'isy'), '--kering']

    def test_lubang_dikesan(self):
        """Keadaan sebenar 2 Nov 2026: terakhir diproses 10-29, stor sampai 11-02.
        10-30 ialah lubang; 11-02 BUKAN kerja kejar (ia kerja langkah `malam` biasa)."""
        with tempfile.TemporaryDirectory() as tmp:
            _, d = jalan(self.sediakan(tmp, '2026-10-29'))
            self.assertEqual(d['dikejar'], ['2026-10-30'])
            self.assertEqual([b['tarikh'] for b in d['belian']], ['2026-11-02'])

    def test_tiada_lubang(self):
        """Keadaan biasa: sesi terakhir diproses ialah sesi sebelum bar terakhir stor."""
        with tempfile.TemporaryDirectory() as tmp:
            _, d = jalan(self.sediakan(tmp, '2026-10-30'))
            self.assertEqual(d['dikejar'], [])
            self.assertEqual(d['sesi_stor_akhir'], '2026-11-02')

    def test_sesi_terakhir_bukan_kerja_kejar(self):
        """Walaupun sesi terakhir stor belum diproses, kejar TIDAK menyentuhnya: ia ada
        pengawal datanya sendiri (data_belum_muktamad) dalam langkah `malam`."""
        with tempfile.TemporaryDirectory() as tmp:
            _, d = jalan(self.sediakan(tmp, '2026-10-29'))
            self.assertNotIn('2026-11-02', d['dikejar'])

    def test_lubang_besar_berhenti(self):
        """Lubang melebihi --maks bermakna sesuatu yang lebih besar rosak: berhenti dengan kod 2
        dan jangan sentuh apa-apa, supaya manusia melihat dahulu."""
        with tempfile.TemporaryDirectory() as tmp:
            a = self.sediakan(tmp, '2026-10-01')
            stor_palsu(os.path.join(tmp, 'stor'),
                       [f'2026-10-{d:02d}' for d in range(2, 30)] + ['2026-11-02'])
            p, d = jalan(a + ['--maks', '3'])
            self.assertEqual(p.returncode, 2)
            self.assertEqual(d['dikejar'], [])
            self.assertTrue(any('--maks' in x for x in d['nota']))

    # Nota: laluan "beli sudah direkod -> dilangkau" TIDAK diuji di sini dengan sengaja. Mengujinya
    # memerlukan larian `malam` SEBENAR (tanpa --kering), dan harian_c.py memakai stor harga repo,
    # bukan stor palsu ujian — jadi ujian itu akan mencetuskan imbasan 134 kaedah penuh. Guard itu
    # satu baris perbandingan tarikh terhadap status_harian.json dan boleh dibaca terus.

    def test_tiada_rujukan_status(self):
        """Tanpa malam.sesi tiada rujukan untuk mengejar — jangan teka, jangan tulis."""
        with tempfile.TemporaryDirectory() as tmp:
            stor_palsu(os.path.join(tmp, 'stor'), self.SESI)
            os.makedirs(os.path.join(tmp, 'pt'))
            _, d = jalan(['--folder', os.path.join(tmp, 'pt'), '--stor', os.path.join(tmp, 'stor'),
                          '--isyarat', os.path.join(tmp, 'isy'), '--kering'])
            self.assertEqual(d['dikejar'], [])
            self.assertTrue(d['nota'])


class TestBukaLampau(unittest.TestCase):
    def test_buka_tarikh_betul(self):
        """Belian lampau mesti memakai harga buka SEBENAR hari itu, bukan harga semasa."""
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, 'terkini.csv')
            pd.DataFrame(dict(ticker=['AAA', 'BBB', 'AAA'], date=[20261030, 20261102, 20261102],
                              open=[10.0, 20.0, 11.0], high=1, low=1, close=1,
                              volume=[1, 2, 3])).to_csv(p, index=False)
            f = K.buka_sesi(p, '2026-11-02', tmp)
            d = pd.read_csv(f)
            self.assertEqual(sorted(d.ticker), ['AAA', 'BBB'])
            self.assertEqual(float(d[d.ticker == 'AAA'].open.iloc[0]), 11.0)

    def test_tiada_bar_pulang_none(self):
        """Pagi sebelum pasaran dibuka: tiada bar, jadi JANGAN rekod belian tanpa harga."""
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, 'terkini.csv')
            pd.DataFrame(dict(ticker=['AAA'], date=[20261030], open=[10.0], high=1, low=1,
                              close=1, volume=[1])).to_csv(p, index=False)
            self.assertIsNone(K.buka_sesi(p, '2026-11-03', tmp))

    def test_buka_sifar_dibuang(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, 'terkini.csv')
            pd.DataFrame(dict(ticker=['AAA', 'BBB'], date=[20261102, 20261102], open=[0.0, 5.0],
                              high=1, low=1, close=1, volume=[1, 1])).to_csv(p, index=False)
            d = pd.read_csv(K.buka_sesi(p, '2026-11-02', tmp))
            self.assertEqual(list(d.ticker), ['BBB'])


class TestLaluanProduksi(unittest.TestCase):
    def test_subproses_produksi(self):
        """kejar.py mesti boleh dijalankan sebagai skrip, cara harian.yml menjalankannya."""
        p = subprocess.run([sys.executable, os.path.join(STD, 'kejar.py'), '--help'],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn('--maks', p.stdout)


if __name__ == '__main__':
    unittest.main()
