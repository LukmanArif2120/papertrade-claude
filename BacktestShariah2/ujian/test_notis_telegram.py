import contextlib, io, os, sys, unittest
from datetime import datetime, timezone
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
import notis_telegram as nt


class TestNotisTelegram(unittest.TestCase):
    def test_jenis_rutin(self):
        self.assertEqual(nt.jenis_rutin('Kemas kini 6:02 pagi 2026-10-16: 160 keluar\n\nbadan')[0], 'pagi')
        self.assertEqual(nt.jenis_rutin('Log 6:02 pagi 2026-10-16: betulkan')[0], 'pagi')
        self.assertEqual(nt.jenis_rutin('Imbas 8:02 malam 2026-10-15: 403 senarai beli')[0], 'imbas')
        self.assertEqual(nt.jenis_rutin('Beli 9:35 NY 2026-10-15: 391 direkod')[0], 'beli')
        self.assertIsNone(nt.jenis_rutin('Harga harian (yfinance): sesi 20261015')[0])
        self.assertIsNone(nt.jenis_rutin('')[0])

    def test_mesej_komit_tapis_rutin_sahaja(self):
        ev = {'commits': [{'message': 'Dashboard: lencana'}, {'message': 'Beli 9:35 NY 2026-10-16: 12 direkod, 3 dilangkau\n\nx'}]}
        m = nt.mesej_komit(ev)
        self.assertIn('Beli 9:35 NY 2026-10-16: 12 direkod, 3 dilangkau', m)
        self.assertNotIn('Dashboard: lencana', m)
        self.assertIsNone(nt.mesej_komit({'commits': [{'message': 'Saringan TradingView: 2026-10-16'}]}))

    def test_mesej_gagal(self):
        self.assertIsNone(nt.mesej_gagal({'workflow_run': {'conclusion': 'success'}}))
        m = nt.mesej_gagal({'workflow_run': {'name': 'Semak data', 'conclusion': 'failure', 'head_branch': 'main',
                                             'head_commit': {'message': ''}, 'html_url': 'https://x'}})
        self.assertIn('Semak data', m)

    def test_sauh(self):
        t = datetime(2026, 10, 16, 1, 30, tzinfo=timezone.utc)
        self.assertEqual(nt.sauh('22:00', t), datetime(2026, 10, 15, 22, 0, tzinfo=timezone.utc))
        t2 = datetime(2026, 10, 16, 23, 13, tzinfo=timezone.utc)
        self.assertEqual(nt.sauh('22:00', t2), datetime(2026, 10, 16, 22, 0, tzinfo=timezone.utc))

    def test_pengawas_cuti_dan_ada_komit(self):
        jumaat = datetime(2026, 10, 16, 23, 13, tzinfo=timezone.utc)   # sesi NY Jumaat 16 Okt
        with mock.patch.object(nt, 'hari_dagangan_ny', return_value=True):
            self.assertIsNone(nt.mesej_pengawas('pagi', '22:00', jumaat, semak_komit=lambda *a: True))
            m = nt.mesej_pengawas('pagi', '22:00', jumaat, semak_komit=lambda *a: False)
            self.assertIn('Kemas kini 6:02 pagi MYT', m)
        with mock.patch.object(nt, 'hari_dagangan_ny', return_value=False):
            self.assertIsNone(nt.mesej_pengawas('pagi', '22:00', jumaat, semak_komit=lambda *a: False))

    def test_hantar_tanpa_rahsia_tidak_gagal(self):
        with mock.patch.dict(os.environ, {'TELEGRAM_TOKEN': '', 'TELEGRAM_TO': ''}):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(nt.hantar('ujian'), 0)
            self.assertIn('belum disediakan', out.getvalue())


if __name__ == '__main__':
    unittest.main()
