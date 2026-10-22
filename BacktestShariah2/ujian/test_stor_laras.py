# Ujian kod/stor.py nisbah_laras/gabung_kline dan harga_yf.gabung_satu (22 Okt 2026): sejarah lama dilaras hanya jika nisbah
# bar bertindih seragam; satu bar salah atau perubahan separa tidak lagi menulis semula seluruh sejarah.
import os, sys, tempfile, unittest
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import stor  # noqa: E402
import harga_yf  # noqa: E402


def bar(tarikh, tutup, t='X'):
    c = np.asarray(tutup, float)
    return pd.DataFrame(dict(ticker=t, date=tarikh, open=c, high=c * 1.01, low=c * 0.99, close=c, volume=1000))


T = [20261001 + i for i in range(20)]


class TestNisbahLaras(unittest.TestCase):
    def test_sama_laras_anomali(self):
        lama = bar(T[:15], np.linspace(50, 60, 15))
        self.assertEqual(stor.nisbah_laras(lama, bar(T[10:20], np.r_[lama.close.values[10:], [61] * 5]))[1], 'sama')
        b = bar(T[10:20], np.r_[lama.close.values[10:] / 2, [30] * 5])            # pecahan 2:1 seragam
        r, kep, n, s = stor.nisbah_laras(lama, b)
        self.assertEqual((kep, n), ('laras', 5)); self.assertAlmostEqual(r, 0.5)
        c = lama.close.values[10:].copy(); c[:3] = c[:3] * 0.95                    # 3 daripada 5 bar berubah (separa)
        self.assertEqual(stor.nisbah_laras(lama, bar(T[10:20], np.r_[c, [61] * 5]))[1], 'anomali')
        self.assertEqual(stor.nisbah_laras(lama, bar(T[14:20], np.r_[lama.close.values[14:] * 0.98, [61] * 5]))[1], 'anomali')
        self.assertEqual(stor.nisbah_laras(lama, bar(T[14:20], np.r_[lama.close.values[14:] / 3, [20] * 5]))[1], 'laras')

    def test_gabung_tidak_laras_anomali_dan_log(self):
        lama = bar(T[:15], np.linspace(50, 60, 15))
        c = lama.close.values[10:].copy(); c[:3] = c[:3] * 0.9
        baru = bar(T[10:20], np.r_[c, [61] * 5])
        x = harga_yf.gabung_satu(lama, baru, log := [])
        np.testing.assert_allclose(x.sort_values('date').close.values[:10], lama.close.values[:10])   # sejarah lama tidak berubah
        self.assertEqual(log[0]['keputusan'], 'anomali')
        stor.LOG_LARAS.clear()
        d = stor.gabung_kline(lama, 'X', bar(T[10:20], np.r_[lama.close.values[10:] / 2, [30] * 5]).drop(columns='ticker'))
        np.testing.assert_allclose(d.sort_values('date').close.values[:10], lama.close.values[:10] / 2)
        self.assertEqual(stor.LOG_LARAS[-1]['keputusan'], 'laras')
        with tempfile.TemporaryDirectory() as dd:
            self.assertEqual(stor.tulis_log_laras(dd, stor.LOG_LARAS), 1)
            self.assertEqual(stor.tulis_log_laras(dd, log), 1)
            self.assertEqual(len(pd.read_csv(os.path.join(dd, 'log_laras.csv'))), 2)


if __name__ == '__main__':
    unittest.main()
