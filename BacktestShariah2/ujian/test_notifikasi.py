# Ujian standard/notifikasi.py: baris < 200 aksara, "tak beli" dinyatakan, sesi belum siap dikesan.
import contextlib, io, json, os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import notifikasi as N


def jalan(st, *arg):
    d = tempfile.mkdtemp()
    with open(os.path.join(d, 'status_harian.json'), 'w') as f:
        json.dump(st, f)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        N.main(list(arg) + ['--folder', d])
    return out.getvalue().strip()


MALAM = dict(sesi='2026-10-26', keluar_baru_jumlah=dict(C=120, M=1), keluar_baru=dict(C=dict(henti=80, sasaran=10, isyarat=30)),
             menunggu=40, tidak_dibeli=['AAA M01'], senarai_beli=650, saham_unik=300)


class TestNotifikasi(unittest.TestCase):
    def test_malam_siap(self):
        s = jalan({'malam': MALAM}, 'malam', '--masa', '2026-10-27 07:17')   # Selasa 3:17 ptg MYT
        self.assertIn('Harian 2026-10-26: keluar C 120 (henti 80, isyarat 30, sasaran 10), M 1', s)
        self.assertIn('senarai beli 650 (300 saham) untuk 2026-10-27', s)
        self.assertLess(len(s), 200)

    def test_malam_belum(self):
        s = jalan({'malam': dict(MALAM, sesi='2026-10-23')}, 'malam', '--masa', '2026-10-27 07:17', '--gagal', 'harian.yml')
        self.assertTrue(s.startswith('Harian 2026-10-26 BELUM siap (sesi terakhir diproses: 2026-10-23)'))
        self.assertIn('GAGAL: harian.yml', s)

    def test_malam_sabtu(self):   # Sabtu MYT memproses sesi Jumaat
        s = jalan({'malam': dict(MALAM, sesi='2026-10-30')}, 'malam', '--masa', '2026-10-31 07:17')
        self.assertIn('untuk 2026-11-02', s)

    def test_beli(self):
        b = dict(tarikh='2026-10-27', direkod=640, saham_unik=290, dilangkau=10, buka_lewat=['X M01'],
                 sumber_buka='buka sementara yfinance 09:40 NY')
        s = jalan({'beli': b}, 'beli', '--masa', '2026-10-27 14:20', '--tambah', 'db ok')
        self.assertEqual(s, 'Beli 2026-10-27: 640 direkod (290 saham), 10 dilangkau, 1 buka lewat; '
                            'buka sementara yfinance 09:40 NY | db ok')

    def test_tak_beli(self):
        s = jalan({'beli': dict(tarikh='2026-10-27', direkod=0, nota='tak beli: senarai_beli belum dikemas kini')},
                  'beli', '--masa', '2026-10-27 14:20')
        self.assertTrue(s.startswith('Tak beli 2026-10-27: tak beli: senarai_beli'))
        s = jalan({'beli': dict(tarikh='2026-10-26', direkod=600)}, 'beli', '--masa', '2026-10-27 14:20')
        self.assertTrue(s.startswith('Tak beli 2026-10-27 (belum direkod; belian terakhir 2026-10-26)'))
        self.assertEqual(jalan({}, 'beli', '--masa', '2026-10-31 14:20'), 'Tak beli 2026-10-31: pasaran AS tutup')

    def test_had_panjang(self):
        s = jalan({'beli': dict(tarikh='2026-10-27', direkod=0, nota='x' * 400)}, 'beli', '--masa', '2026-10-27 14:20')
        self.assertEqual(len(s), N.HAD)


if __name__ == '__main__':
    unittest.main()
