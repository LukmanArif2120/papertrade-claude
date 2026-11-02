"""Ujian registry Nxx — keluarga kedua selari dengan Mxx."""
import csv
import json
import os
import sys
import tempfile
import unittest

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'standard'))

import registry_n as R  # noqa: E402


class TestStruktur(unittest.TestCase):
    def test_semak_bersih(self):
        self.assertEqual(R.semak(), [])

    def test_bilangan(self):
        # jumlah dipradaftar; menambah baris mesti kemas kini ujian ini dengan sengaja
        self.assertEqual(len(R.MASUK), 147)
        self.assertEqual(len(R.KELUAR), 45)
        self.assertEqual(len(R.CARA), 12)
        self.assertEqual(len(R.URUTAN), 14)   # U14 ditambah oleh E3 (SPEC_INSTRUMEN.md)
        self.assertEqual(len(R.GABUNGAN), 8)
        self.assertEqual(len(R.SAIZ), 10)
        self.assertEqual(len(R.ALAM), 8)
        self.assertEqual(len(R.PEGANG), 6)
        self.assertEqual(len(R.IMBANG), 5)
        self.assertEqual(len(R.KORELASI), 4)
        self.assertEqual(len(R.INSTRUMEN), 4)
        self.assertEqual(len(R.PAKSI_LAIN), 10)

    def test_id_berturutan(self):
        self.assertEqual([b[0] for b in R.MASUK], [f'N{i:02d}' for i in range(1, 148)])
        self.assertEqual([b[0] for b in R.KELUAR], [f'X{i:02d}' for i in range(1, 46)])
        self.assertEqual([b[0] for b in R.CARA], [f'C{i:02d}' for i in range(1, 13)])
        self.assertEqual([b[0] for b in R.URUTAN], [f'U{i:02d}' for i in range(1, 15)])
        for nama, baris, awalan in R.paksi():
            self.assertEqual([b[0] for b in baris],
                             [f'{awalan}{i:02d}' for i in range(1, len(baris) + 1)], nama)

    def test_medan_penuh(self):
        for b in R.MASUK:
            self.assertEqual(len(b), 8, b[0])
            for medan in b[:7]:        # nota dibenarkan kosong
                self.assertTrue(str(medan).strip(), b[0])
        for _n, baris, _a in R.paksi():
            for b in baris:
                self.assertEqual(len(b), 6, b[0])
                for medan in b[:5]:
                    self.assertTrue(str(medan).strip(), b[0])

    def test_lajur_sepadan(self):
        self.assertEqual(len(R.LAJUR), 8)

    def test_nama_unik(self):
        nama = [b[2] for b in R.MASUK]
        self.assertEqual(len(set(nama)), len(nama))

    def test_peraturan_masuk_unik(self):
        aturan = [b[3] for b in R.MASUK]
        self.assertEqual(len(set(aturan)), len(aturan))

    def test_peraturan_keluar_unik(self):
        aturan = [b[1] for b in R.KELUAR]
        self.assertEqual(len(set(aturan)), len(aturan))


class TestStatus(unittest.TestCase):
    def test_status_sah(self):
        semua = [b[6] for b in R.MASUK]
        for _n, baris, _a in R.paksi():
            semua += [b[4] for b in baris]
        for st in semua:
            self.assertTrue(st in ('DIUJI', 'SEDIA') or st.startswith('PERLU:'), st)

    def test_diuji_ada_nota(self):
        # DIUJI tanpa angka tidak berguna
        for b in R.MASUK:
            if b[6] == 'DIUJI':
                self.assertTrue(b[7].strip(), b[0])
        for _n, baris, _a in R.paksi():
            for b in baris:
                if b[4] == 'DIUJI':
                    self.assertTrue(b[5].strip(), b[0])

    def test_perlu_ada_nama_indikator(self):
        for b in R.MASUK:
            if b[6].startswith('PERLU:'):
                self.assertTrue(b[6].split(':', 1)[1].strip(), b[0])

    def test_perlu_sudah_diaudit(self):
        """Setiap token PERLU mesti ada kelas yang diaudit dalam REVERSE/audit_perlu.json.

        Punca masalah yang audit 2 Nov 2026 dedahkan: status `PERLU:<x>` DITAIP TANGAN dan
        dua ujian di atas hanya menyemak BENTUK rentetan, jadi label boleh salah selama
        berbulan tanpa sesiapa tahu. Dua memang salah — `N123`/`N142` dilabel perlukan data
        SEC yang sebenarnya ADA dan dijejak git. Ujian ini menutup punca itu secara
        STRUKTUR: token PERLU baharu tidak boleh masuk tanpa dikelaskan dahulu (KOD_SAHAJA /
        SUDAH_ADA / DATA_LUAR / BUKAN_INDIKATOR). Ia tidak menyemak kelas itu BETUL — itu
        kerja audit — tetapi ia menghalang label yang tidak pernah disemak langsung.
        """
        fail = os.path.join(AKAR, 'REVERSE', 'audit_perlu.json')
        if not os.path.exists(fail):
            self.skipTest('REVERSE/audit_perlu.json tiada')
        with open(fail, encoding='utf-8') as f:
            A = json.load(f)
        diaudit = {t['token'] for t in A['token']}
        semua = [b[6] for b in R.MASUK]
        for _n, baris, _a in R.paksi():
            semua += [b[4] for b in baris]
        hilang = sorted({st.split(':', 1)[1] for st in semua
                         if st.startswith('PERLU:')} - diaudit)
        self.assertEqual(hilang, [], f'token PERLU belum diaudit: {hilang} — '
                                     'jalankan audit dan kemas kini REVERSE/audit_perlu.json')

    def test_n01_adalah_dapatan_pengguna(self):
        n01 = R.MASUK[0]
        self.assertEqual(n01[0], 'N01')
        self.assertIn('ma10', n01[3])
        self.assertIn('ma20', n01[3])
        self.assertIn('vol_n50', n01[3])
        self.assertEqual(n01[6], 'DIUJI')

    def test_c01_adalah_asas_repo(self):
        c01 = R.CARA[0]
        self.assertEqual(c01[0], 'C01')
        self.assertEqual(c01[4], 'DIUJI')
        self.assertIn('buka', c01[1])
        self.assertIn('KOLAM_EKOR', c01[5])

    def test_cara_lain_belum_diuji(self):
        # hanya C01 pernah diuji; jika ini gagal, seseorang menanda DIUJI tanpa hasil
        self.assertEqual([b[0] for b in R.CARA if b[4] == 'DIUJI'], ['C01'])

    def test_u05_papan_ditanda_jangan_guna(self):
        # KAEDAH_TERBAIK.md: pangkat backtest tiada kuasa ramalan; nota mesti menyatakannya
        u05 = [b for b in R.URUTAN if b[0] == 'U05'][0]
        self.assertIn('JANGAN', u05[5])

    def test_u03_clenow_sebaran_sifar(self):
        u03 = [b for b in R.URUTAN if b[0] == 'U03'][0]
        self.assertEqual(u03[4], 'DIUJI')
        self.assertIn('0.00', u03[5])

    def test_pandas_ta_bukan_kebergantungan(self):
        # pandas_ta memaksa numpy<2.3; ia rujukan spesifikasi sahaja
        import os
        req = os.path.join(R.AKAR, 'requirements-kajian.txt')
        teks = open(req, encoding='utf-8').read()
        self.assertNotIn('pandas-ta==', teks)
        self.assertNotIn('pandas_ta==', teks)

    def test_rejim_kalendar_ada_amaran_pendedahan(self):
        # N101-N110 memilih MASA bukan saham = peruntukan tunai; spec mesti menyatakannya
        kel = {b[1] for b in R.MASUK if b[0] in
               ('N101', 'N105', 'N107', 'N108', 'N110')}
        self.assertEqual(kel, {'KALENDAR', 'REJIM'})

    def test_n122_pembetulan_ambang_direkod(self):
        # saya tersilap ingat $20 juta; sumber beri $10 juta. Pembetulan mesti kekal direkod.
        n122 = [b for b in R.MASUK if b[0] == 'N122'][0]
        self.assertIn('10 juta', n122[3])
        self.assertIn('PEMBETULAN', n122[7])

    def test_n130_orb_amaran_kos(self):
        n130 = [b for b in R.MASUK if b[0] == 'N130'][0]
        self.assertEqual(n130[6], 'PERLU:intraday')
        self.assertIn('SIFAR', n130[7])

    def test_n131_amaran_fdr_62(self):
        # satu baris tetapi 62 ujian; tanpa amaran ini FDR akan salah 62 kali
        n131 = [b for b in R.MASUK if b[0] == 'N131'][0]
        self.assertIn('62 UJIAN BERASINGAN', n131[7])
        self.assertIn('morningstar', n131[7])

    def test_sapuan6_semua_perlu_data(self):
        # dapatan: N131-N147 tiada satu pun boleh diuji dengan apa yang repo ada
        baru = [b for b in R.MASUK if int(b[0][1:]) >= 131]
        self.assertEqual(len(baru), 17)
        self.assertEqual([b for b in baru if b[6] == 'SEDIA'], [])

    def test_u12_gtja_bukti_luaran(self):
        u12 = [b for b in R.URUTAN if b[0] == 'U12'][0]
        self.assertIn('17 daripada 191', u12[5])
        self.assertIn('BELUM dibaca', u12[5])

    def test_gb01_semua_masuk_adalah_dan(self):
        # kesilapan struktur: 147 MASUK semuanya penapis DAN, yang SETUP.md ukur gagal
        gb01 = [b for b in R.GABUNGAN if b[0] == 'GB01'][0]
        self.assertEqual(gb01[4], 'DIUJI')
        self.assertIn('0 daripada 598', gb01[5])

    def test_gb02_belum_diuji(self):
        gb02 = [b for b in R.GABUNGAN if b[0] == 'GB02'][0]
        self.assertEqual(gb02[4], 'SEDIA')
        self.assertIn('BELUM PERNAH DIUJI', gb02[5])

    def test_lima_calon_tanpa_sumber_baharu(self):
        # GB02, GB04, GB08, SZ10, IS02 mesti SEDIA: tiada data/domain baharu diperlukan
        cari = {'GB02': R.GABUNGAN, 'GB04': R.GABUNGAN, 'GB08': R.GABUNGAN,
                'SZ10': R.SAIZ, 'IS02': R.INSTRUMEN}
        for _id, senarai in cari.items():
            b = [x for x in senarai if x[0] == _id][0]
            self.assertEqual(b[4], 'SEDIA', _id)

    def test_hasil_nxx_sepadan_registry(self):
        # setiap id dalam HASIL_NXX mesti wujud dan menjadi DIUJI dalam keluaran
        ids = {b[0] for b in R.MASUK}
        self.assertTrue(set(R.HASIL_NXX) <= ids)
        self.assertEqual(len(R.HASIL_NXX), 66)
        for b in R.MASUK:
            if b[0] in R.HASIL_NXX:
                self.assertEqual(R.kemas_masuk(b)[6], 'DIUJI', b[0])
                self.assertIn('NXX.md', R.kemas_masuk(b)[7])

    def test_nxx_tiada_gate3_lulus(self):
        # 0 daripada 280 lulus ketiga-tiga gate; jika ada yang lulus, nota mesti berubah
        for v in R.HASIL_NXX.values():
            self.assertIn('gate3 gagal', v)

    def test_tajuk_paksi_lengkap(self):
        for nama, _b, _a in R.paksi()[3:]:
            self.assertIn(nama, R.TAJUK_PAKSI)

    def test_kira(self):
        km = R._kira(R.MASUK, 6)
        self.assertEqual(sum(km.values()), len(R.MASUK))
        self.assertGreater(km['SEDIA'], 0)


class TestSemakTangkapRalat(unittest.TestCase):
    def _dengan(self, masuk):
        asal = R.MASUK
        try:
            R.MASUK = masuk
            return R.semak()
        finally:
            R.MASUK = asal

    def test_tangkap_id_terlangkau(self):
        m = [('N01', 'MA', 'a', 'x', 's', 'p', 'SEDIA', ''),
             ('N03', 'MA', 'b', 'y', 's', 'p', 'SEDIA', '')]
        self.assertTrue(any('tidak berturutan' in x for x in self._dengan(m)))

    def test_tangkap_status_tidak_dikenali(self):
        m = [('N01', 'MA', 'a', 'x', 's', 'p', 'MUNGKIN', '')]
        self.assertTrue(any('tidak dikenali' in x for x in self._dengan(m)))

    def test_tangkap_cara_tidak_berturutan(self):
        asal = R.CARA
        try:
            R.CARA = [('C02', 'a', 's', 'p', 'SEDIA', '')]
            self.assertTrue(any('tidak berturutan' in x for x in R.semak()))
        finally:
            R.CARA = asal

    def test_tangkap_urutan_tidak_berturutan(self):
        asal = R.URUTAN
        try:
            R.URUTAN = [('U02', 'a', 's', 'p', 'SEDIA', '')]
            self.assertTrue(any('tidak berturutan' in x for x in R.semak()))
        finally:
            R.URUTAN = asal

    def test_tangkap_medan_kurang(self):
        m = [('N01', 'MA', 'a', 'x', 's', 'p', 'SEDIA')]
        self.assertTrue(any('medan' in x for x in self._dengan(m)))


class TestKeluaran(unittest.TestCase):
    def test_csv_dan_spec_ditulis(self):
        asal_csv, asal_spec = R.CSV, R.SPEC
        with tempfile.TemporaryDirectory() as d:
            try:
                R.CSV = os.path.join(d, 'registry_N.csv')
                R.SPEC = os.path.join(d, 'SPEC_SEMUA_N.md')
                n = R.tulis_csv()
                R.tulis_spec()
                self.assertEqual(
                    n, len(R.MASUK) + sum(len(b) for _n, b, _a in R.paksi()))
                with open(R.CSV, encoding='utf-8') as f:
                    baris = list(csv.DictReader(f))
                self.assertEqual(len(baris), n)
                self.assertEqual(baris[0]['id'], 'N01')
                self.assertEqual(baris[len(R.MASUK)]['keluarga'], 'KELUAR')
                self.assertEqual(baris[-1]['keluarga'], 'INSTRUMEN')
                teks = open(R.SPEC, encoding='utf-8').read()
                self.assertIn('SPEC SEMUA N', teks)
                self.assertIn('N147', teks)
                self.assertIn('X45', teks)
                self.assertIn('C12', teks)
                self.assertIn('U13', teks)
                for tanda in ('GB02', 'SZ10', 'AL02', 'PG06', 'IB05', 'KR04', 'IS02'):
                    self.assertIn(tanda, teks)
                self.assertIn('Kesilapan struktur dalam registry ini', teks)
                self.assertIn('kadar pulangan sudah boleh diukur', teks)
                self.assertIn('peruntukan tunai yang disamarkan', teks)
                self.assertIn('Sempadan K / M / N', teks)
                self.assertIn('Saluran rangkaian', teks)
                self.assertIn('Jangan sunting fail ini secara manual', teks)
            finally:
                R.CSV, R.SPEC = asal_csv, asal_spec

    def test_fail_repo_segerak(self):
        """Fail yang dikomit mesti sepadan dengan senarai dalam skrip."""
        with open(R.CSV, encoding='utf-8') as f:
            baris = list(csv.DictReader(f))
        self.assertEqual(len(baris),
                         len(R.MASUK) + sum(len(b) for _n, b, _a in R.paksi()))
        self.assertEqual([b['id'] for b in baris[:len(R.MASUK)]], [b[0] for b in R.MASUK])

    def test_main_pulang_sifar(self):
        asal_csv, asal_spec = R.CSV, R.SPEC
        with tempfile.TemporaryDirectory() as d:
            try:
                R.CSV = os.path.join(d, 'a.csv')
                R.SPEC = os.path.join(d, 'b.md')
                self.assertEqual(R.main(), 0)
            finally:
                R.CSV, R.SPEC = asal_csv, asal_spec


if __name__ == '__main__':
    unittest.main()
