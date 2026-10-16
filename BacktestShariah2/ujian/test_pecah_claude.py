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
