import os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
import jana_db as jd


class UjianGarisHarga(unittest.TestCase):
    """prestasi/garis dan prestasi/mfe: siri tutup posisi terbuka, SPY sejak belian terawal, kenaikan maksimum."""

    def stor(self, d):
        with open(os.path.join(d, 'harga_A.csv'), 'w') as f:
            f.write('ticker,date,open,high,low,close,volume\n'
                    'AAA,20261001,10,10.5,9.8,10,1\nAAA,20261002,10,12,9.9,11,1\nAAA,20261005,11,11.5,10.5,11.2,1\n'
                    'BBB,20261001,20,21,19,20,1\nBBB,20261002,20,25,19,24,1\nBBB,20261005,24,24.5,22,23,1\n')
        with open(os.path.join(d, 'harga_idx.csv'), 'w') as f:
            f.write('ticker,date,open,high,low,close,volume\nSPY,20260930,600,601,599,600,1\n'
                    'SPY,20261001,601,603,600,602,1\nSPY,20261002,602,605,601,604,1\nQQQ,20261001,500,501,499,500,1\n')

    def test_garis_dan_mfe(self):
        C = [dict(saham='AAA', kaedah='M01', tarikh_beli='2026-10-02', harga_beli='10', keluar='False', tutup_semua='False'),
             dict(saham='BBB', kaedah='M02', tarikh_beli='2026-10-01', harga_beli='20', keluar='True', tarikh_keluar='2026-10-05',
                  harga_keluar='23.5', tutup_semua='True'),
             dict(saham='BBB', kaedah='M03', tarikh_beli='2026-10-01', harga_beli='20', tidak_dibeli='True')]
        with tempfile.TemporaryDirectory() as d:
            self.stor(d)
            g, mfe = jd.garis_harga([], C, d)
        # BBB keluar pada sesi terakhir (5 Okt) -> masih ada siri (terbuka pada sesi sebelum); siri bermula 1 Okt
        self.assertEqual(g['tarikh'], [20261001, 20261002, 20261005])
        self.assertEqual(g['rows'], [dict(s='AAA', c=[10.0, 11.0, 11.2]), dict(s='BBB', c=[20.0, 24.0, 23.0])])
        # SPY sejak belian terawal (1 Okt), QQQ diabaikan
        self.assertEqual(g['spy'], [[20261001, 601.0, 602.0], [20261002, 602.0, 604.0]])
        m = dict(mfe)
        self.assertEqual(m['C|AAA|M01|2026-10-02'], 20.0)        # tinggi 12 / 10
        self.assertEqual(m['C|BBB|M02|2026-10-01'], 25.0)        # tinggi sebelum hari keluar (25) / 20
        self.assertNotIn('C|BBB|M03|2026-10-01', m)              # tidak dibeli

    def test_keluar_lama_tiada_siri(self):
        C = [dict(saham='BBB', kaedah='M02', tarikh_beli='2026-10-01', harga_beli='20', keluar='True', tarikh_keluar='2026-10-02',
                  harga_keluar='24', tutup_semua='True'),
             dict(saham='AAA', kaedah='M01', tarikh_beli='2026-10-02', harga_beli='10', keluar='False')]
        with tempfile.TemporaryDirectory() as d:
            self.stor(d)
            g, _ = jd.garis_harga([], C, d)
        self.assertEqual([x['s'] for x in g['rows']], ['AAA'])
        self.assertEqual(g['tarikh'], [20261002, 20261005])

    def test_mfe_minimum_sifar(self):
        C = [dict(saham='AAA', kaedah='M01', tarikh_beli='2026-10-05', harga_beli='20', keluar='False')]
        with tempfile.TemporaryDirectory() as d:
            self.stor(d)
            _, mfe = jd.garis_harga([], C, d)
        self.assertEqual(dict(mfe)['C|AAA|M01|2026-10-05'], 0.0)


if __name__ == '__main__':
    unittest.main()
