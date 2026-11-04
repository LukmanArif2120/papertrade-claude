import contextlib, csv, io, os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
import pecah_claude as pc

HDR = ['tarikh_beli', 'saham', 'kaedah', 'harga_beli', 'keluar', 'tidak_dibeli', 'nota']


def buat(folder, nama, n, mula=0, keluar=False):
    rows = [['2026-10-14', f'S{mula + i:04d}', 'M02', '20.34', 'True' if keluar else 'False', '',
             'nota panjang ' * 40] for i in range(n)]
    pc.tulis(os.path.join(folder, nama), HDR, rows)
    return rows


def jalan(argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        kod = pc.main(argv)
    return kod, out.getvalue()


class TestPecahClaude(unittest.TestCase):
    def test_lapor_dan_pecah_kekalkan_semua_baris(self):
        with tempfile.TemporaryDirectory() as d:
            a = buat(d, 'claude.csv', 50)
            b = buat(d, 'claude_2.csv', 600, mula=1000)
            kod, _ = jalan(['--folder', d, '--had', '200000', '--sasaran', '150000'])
            self.assertEqual(kod, 1)  # lapor sahaja: claude_2 melebihi
            self.assertFalse(os.path.exists(os.path.join(d, 'claude_3.csv')))
            kod, _ = jalan(['--folder', d, '--had', '200000', '--sasaran', '150000', '--pecah'])
            self.assertEqual(kod, 0)
            semua, n = [], 2
            while os.path.exists(os.path.join(d, pc.nama_fail(n))):
                h, r = pc.baca(os.path.join(d, pc.nama_fail(n)))
                self.assertEqual(h, HDR)
                self.assertLessEqual(pc.ukur(n, HDR, r)['unjuran'], 200000)
                semua += r
                n += 1
            self.assertGreater(n, 3)  # sekurang-kurangnya satu fail baharu
            self.assertEqual(semua, b)  # susunan dan isi kekal; baris hujung dipindah
            self.assertLessEqual(pc.ukur(2, HDR, pc.baca(os.path.join(d, 'claude_2.csv'))[1])['unjuran'], 150000)
            self.assertEqual(pc.baca(os.path.join(d, 'claude.csv'))[1], a)

    def test_crlf_dan_tiada_perubahan_jika_dalam_had(self):
        with tempfile.TemporaryDirectory() as d:
            buat(d, 'claude.csv', 10)
            p = os.path.join(d, 'claude.csv')
            asal = open(p, 'rb').read()
            self.assertIn(b'\r\n', asal)
            kod, _ = jalan(['--folder', d, '--pecah'])
            self.assertEqual(kod, 0)
            self.assertEqual(open(p, 'rb').read(), asal)

    def test_posisi_keluar_tidak_diunjur_membesar(self):
        u_buka = pc.ukur(2, HDR, [['2026-10-14', 'A', 'M02', '1', 'False', '', 'x']])
        u_tutup = pc.ukur(2, HDR, [['2026-10-14', 'A', 'M02', '1', 'True', '', 'x']])
        self.assertEqual(u_buka['terbuka'], 1)
        self.assertEqual(u_tutup['terbuka'], 0)
        self.assertEqual(u_buka['unjuran'] - u_buka['anggaran'], pc.TUMBUH)

    def test_nilai_bertaip_seperti_db(self):
        self.assertIs(pc.nilai('True'), True)
        self.assertEqual(pc.nilai('20'), 20)
        self.assertEqual(pc.nilai('20.0'), 20.0)
        self.assertEqual(pc.nilai('M02'), 'M02')


if __name__ == '__main__':
    unittest.main()


class TestMetaClaudeBerskala(unittest.TestCase):
    """Meta `papertrade/claude` mesti berskala dengan bilangan kaedah, dan mesti TERLEBIH.

    Dokumen itu membawa medan `slot` dengan SATU entri setiap kaedah (jana_db.py, cari
    `docs['papertrade/claude'].update`). Pemalar lama `META = {'claude': 12000}` ditala ketika repo
    ada ~134 kaedah; kohort 94 kombinasi Nxx menjadikannya 226 entri = 27,947 bait dan anggaran
    terkurang 17,945 bait (8.6%) pada dokumen TERBESAR — satu-satunya dokumen yang pemecah ini
    wujud untuk melindungi, dan 123 fail lain tepat +-0.3% jadi tiada apa-apa lain yang mendedahkannya.

    Kegagalan di sini SENYAP dan berakibat: `--pecah` tidak memecah fail yang ia sangka masih kecil,
    dokumen melepasi 262,144, jana_db.py SystemExit, dan tolakan db MALAM berhenti sepenuhnya.
    """

    # Diukur 4 Nov 2026 daripada dokumen db papertrade/claude yang sebenar.
    SLOT_ENTRI = 226
    SLOT_BAIT = 27947
    META_BUKAN_ROWS = 29945

    def test_meta_berskala_dengan_bilangan_kaedah(self):
        """Pemalar tetap ialah model yang SALAH: tambah kaedah, meta mesti naik."""
        self.assertGreater(pc.meta_claude(226), pc.meta_claude(134))
        naik = pc.meta_claude(135) - pc.meta_claude(134)
        self.assertEqual(naik, pc.SLOT_SETIAP_KAEDAH)

    def test_meta_menampung_ukuran_sebenar_4nov(self):
        """Pada 226 kaedah, meta mesti >= 29,945 bait yang diukur — jika tidak kita terkurang lagi."""
        self.assertGreaterEqual(pc.meta_claude(self.SLOT_ENTRI), self.META_BUKAN_ROWS)

    def test_slot_setiap_kaedah_tidak_bawah_ukuran(self):
        self.assertGreaterEqual(pc.SLOT_SETIAP_KAEDAH, self.SLOT_BAIT / self.SLOT_ENTRI)

    def test_anggaran_meliputi_dokumen_berbentuk_sebenar(self):
        """Ujian regresi sebenar: bina dokumen berbentuk sama seperti jana_db dan bandingkan.

        Inilah semakan yang tidak pernah wujud — META ditaip tangan dan tiada apa-apa yang
        membandingkannya dengan dokumen yang jana_db SEBENARNYA hasilkan.
        """
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
        from bahagi_db import bait
        with tempfile.TemporaryDirectory() as d:
            rows = [['2026-10-14', f'S{i:04d}', 'M02', '20.34', 'False', '', 'nota'] for i in range(60)]
            hdr = ['tarikh_beli', 'saham', 'id_kaedah', 'harga_beli', 'keluar', 'tidak_dibeli', 'nota']
            pc.tulis(os.path.join(d, 'claude.csv'), hdr, rows)
            bk = 226
            dok = dict(dibina='2026-11-04 10:00 MYT', harga_pada='2026-11-03',
                       nota='n' * 300,
                       nota_slot='claude_terbuka = posisi Papertrade C yang belum tutup kedua-dua lorong; '
                                 'moomoo = posisi Moomoo warisan (sumber harian) yang belum keluar.',
                       rows=[dict(zip(hdr, r)) for r in rows],
                       slot={f'M{i:02d}': dict(claude_jumlah=64, claude_terbuka=64, moomoo=3,
                                               moomoo_termasuk_warisan=4, nama='Bollinger Band + RSI')
                             for i in range(bk)},
                       batal={f'B{i}': dict(n=3, sebab='tidak cair') for i in range(29)})
            h, rr = pc.baca(os.path.join(d, 'claude.csv'))
            anggaran = pc.ukur(1, h, rr, bk)['anggaran']
            self.assertGreaterEqual(
                anggaran, bait(dok),
                f'anggaran {anggaran} TERKURANG lawan dokumen sebenar {bait(dok)} — '
                'pemecah akan membiarkan dokumen melepasi had db')

    def test_bil_kaedah_dikira_merentas_semua_fail(self):
        with tempfile.TemporaryDirectory() as d:
            hdr = ['tarikh_beli', 'saham', 'id_kaedah']
            pc.tulis(os.path.join(d, 'claude.csv'), hdr, [['2026-10-14', 'AAA', 'M01'],
                                                          ['2026-10-14', 'BBB', 'M02']])
            pc.tulis(os.path.join(d, 'claude_2.csv'), hdr, [['2026-10-15', 'CCC', 'M02'],
                                                            ['2026-10-15', 'DDD', 'N19X13']])
            self.assertEqual(pc.bil_kaedah_folder(d), 3)   # M01, M02, N19X13 (M02 tidak dikira dua kali)

    def test_fail_bukan_pertama_tidak_dapat_meta_slot(self):
        """Hanya papertrade/claude membawa `slot`; claude_N yang lain tidak."""
        with tempfile.TemporaryDirectory() as d:
            hdr = ['tarikh_beli', 'saham', 'id_kaedah']
            rows = [['2026-10-14', 'AAA', 'M01']]
            pc.tulis(os.path.join(d, 'claude_2.csv'), hdr, rows)
            h, rr = pc.baca(os.path.join(d, 'claude_2.csv'))
            self.assertEqual(pc.ukur(2, h, rr, 226)['anggaran'],
                             pc.META_LAIN + 13 + sum(pc.saiz_baris(h, r) for r in rr))
