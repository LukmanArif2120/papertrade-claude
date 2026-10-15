# Ujian standard/gred.py
import os, sys, unittest
from datetime import date
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import gred as G  # noqa: E402


class UjiGred(unittest.TestCase):
    def test_rs_pangkat(self):
        ix = pd.bdate_range('2025-01-01', periods=260)
        c = pd.DataFrame({'KUAT': np.linspace(10, 30, 260), 'SEDERHANA': np.linspace(10, 12, 260),
                          'LEMAH': np.linspace(30, 10, 260)}, index=ix)
        rs = G.rs_rating(c)
        self.assertGreater(rs['KUAT'], rs['SEDERHANA'])
        self.assertGreater(rs['SEDERHANA'], rs['LEMAH'])
        self.assertTrue(((rs >= 1) & (rs <= 99)).all())

    def test_rs_data_pendek(self):
        c = pd.DataFrame({'X': range(100)}, index=pd.bdate_range('2025-01-01', periods=100))
        self.assertTrue(G.rs_rating(c).empty)

    def test_sempadan_gred(self):
        self.assertEqual([G.gred_rs(x) for x in [99, 90, 89, 80, 79, 60, 59, 40, 39, None]],
                         ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', '–'])
        self.assertEqual([G.gred_kumpulan(x) for x in [80, 79.9, 60, 40, 20, 19, None]],
                         ['A', 'B', 'B', 'C', 'D', 'E', '–'])
        self.assertEqual([G.gred_qr(x) for x in [None, 22, 21, 16, 15, 11, 10, 6, 5, 0]],
                         ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E'])

    def test_hari_dagangan(self):
        self.assertEqual(G.hari_dagangan(date(2026, 10, 9), date(2026, 10, 13)), 2)  # Jumaat -> Selasa
        self.assertEqual(G.hari_dagangan(date(2026, 10, 13), date(2026, 10, 13)), 0)

    def test_tajuk_berita(self):
        self.assertEqual(G.nilai_tajuk('Goldman Sachs Upgrades KB Home to Buy, Raises Target Price to $60'), 1)
        self.assertEqual(G.nilai_tajuk('Goldman Sachs Maintains KB Home With Hold Rating, Cuts Target Price to $56'), -1)
        self.assertEqual(G.nilai_tajuk('Morgan Stanley Initiates KB Home With Sell Rating'), -1)
        self.assertEqual(G.nilai_tajuk('DHI, LEN, KBH: Trending With Analysts'), 0)

    def test_mata_pemangkin(self):
        m, ring = G.mata_pemangkin({'berita': [{'tajuk': 'X upgrades Y', 'hari_lalu': 1},
                                               {'tajuk': 'Y beats estimates', 'hari_lalu': 2},
                                               {'tajuk': 'Y news', 'hari_lalu': 3}],
                                    'earnings_lalu_hari': 5, 'earnings_gerak_pct': 6.0,
                                    'volum_nisbah': 2.5, 'naik_5h': 4.0, 'institusi': 'kumpul'})
        # naik taraf 2 + atasi 2 (<= 3 hari, penuh) + 3 berita 1 + earnings 2 + volum 1 + institusi 1
        self.assertEqual(m, 2 + 2 + 1 + 2 + 1 + 1)
        self.assertEqual(G.gred_pemangkin(m), 'A')
        self.assertEqual(G.mata_pemangkin({})[0], 0)
        self.assertEqual(G.gred_pemangkin(-1), 'E')
        m, _ = G.mata_pemangkin({'berita': [{'tajuk': 'old upgrade', 'hari_lalu': 20}]})
        self.assertEqual(m, 0)

    def test_pautan_berita(self):
        import json
        u = json.loads(G.pautan_berita([
            {'tajuk': 'Y news', 'hari_lalu': 1, 'url': 'https://a/1'},
            {'tajuk': 'X upgrades Y', 'hari_lalu': 4, 'url': 'https://a/2'},
            {'tajuk': 'Y beats', 'hari_lalu': 2, 'url': 'http://tidak-selamat'},
            {'tajuk': 'lama upgrade', 'hari_lalu': 20, 'url': 'https://a/3'}]))
        self.assertEqual([x['url'] for x in u], ['https://a/2', 'https://a/1'])
        self.assertEqual(G.pautan_berita([{'tajuk': 'tiada url', 'hari_lalu': 1}]), '')
        self.assertEqual(G.pautan_berita(None), '')

    def test_kelas_tajuk(self):
        self.assertEqual(G.kelas_tajuk('Acme beats Q3 estimates, raises full-year guidance')[0], 'beat_naik_panduan')
        self.assertEqual(G.kelas_tajuk('Acme Prices $50 Million Public Offering of Common Stock'), ('offering', -3))
        self.assertEqual(G.kelas_tajuk('Acme to Join S&P 500')[1], 3)
        self.assertEqual(G.kelas_tajuk('FDA approves Acme drug for lung cancer')[0], 'fda')
        self.assertEqual(G.kelas_tajuk('Acme awarded $1.2 billion contract by U.S. Army')[0], 'kontrak_besar')
        self.assertEqual(G.kelas_tajuk('<em>Acme</em> Announces Partnership With NVIDIA')[0], 'kontrak_besar')
        self.assertEqual(G.kelas_tajuk('Acme Keeps Quarterly Dividend at $0.60'), (None, 0))

    def test_relevan(self):
        self.assertEqual(G.nama_teras('CF Industries Holdings, Inc.'), 'CF Industries')
        self.assertEqual(G.nama_teras('Infleqtion'), 'Infleqtion')
        self.assertFalse(G.relevan('Vertex and Moderna Advance <em>CF</em> MRNA Therapy', 'CF', 'CF Industries Holdings'))
        self.assertTrue(G.relevan('<em>CF</em> Industries Keeps Quarterly Dividend', 'CF', 'CF Industries Holdings'))
        self.assertTrue(G.relevan('Fertilizer stocks rally (CF)', 'CF', ''))
        self.assertTrue(G.relevan('Why INFQ stock is soaring', 'INFQ', ''))
        self.assertFalse(G.relevan('Why AI stocks are soaring', 'AI', ''))

    def test_susutan_dan_offering(self):
        m, _ = G.mata_pemangkin({'berita': [{'tajuk': 'X upgrades Y', 'hari_lalu': 7}]})
        self.assertEqual(m, 1)  # 2 x 0.5
        m, ring = G.mata_pemangkin({'berita': [{'tajuk': 'Y announces $20 million registered direct offering', 'hari_lalu': 1}]})
        self.assertEqual(m, -3)
        self.assertEqual(G.gred_pemangkin(m), 'E')
        self.assertIn('pencairan', ring)

    def test_analisis_dan_orang_dalam(self):
        hari = date(2026, 10, 15)
        ms = lambda s: int(pd.Timestamp(s + ' 09:00', tz='America/New_York').timestamp() * 1000)
        d = {'data': {'inst_rating_summary_list': [
            {'institution_info': {'institution_en_name': 'Bernstein'},
             'rating_item_list': [{'rating': 3, 'target_price': 162, 'recommendation_date': ms('2026-10-13'), 'rating_url': 'https://t/1'}]},
            {'institution_info': {'institution_en_name': 'BMO'},
             'rating_item_list': [{'rating': 3, 'target_price': 135, 'recommendation_date': ms('2026-10-06')},
                                  {'rating': 3, 'target_price': 135, 'recommendation_date': ms('2026-08-07')}]},
            {'institution_info': {'institution_en_name': 'Freedom'},
             'rating_item_list': [{'rating': 3, 'target_price': 150, 'recommendation_date': ms('2026-10-14')},
                                  {'rating': 2, 'target_price': 133, 'recommendation_date': ms('2026-08-26')}]},
            {'institution_info': {'institution_en_name': 'UBS'},
             'rating_item_list': [{'rating': 3, 'target_price': 150, 'recommendation_date': ms('2026-10-12')},
                                  {'rating': 3, 'target_price': 130, 'recommendation_date': ms('2026-07-01')}]}]}}
        a = {x['firma']: x for x in G.analisis_moomoo(d, hari)}
        self.assertEqual(a['Bernstein']['kategori'], 'mula_beli')
        self.assertNotIn('BMO', a)  # ulang rating, sasaran sama
        self.assertEqual(a['Freedom']['kategori'], 'naik_taraf')
        self.assertEqual(a['UBS']['kategori'], 'naik_sasaran_besar')
        self.assertEqual(a['Bernstein']['tarikh'], '2026-10-13')
        od = G.orang_dalam_moomoo({'data': {'trades': [
            {'name': 'A', 'transaction_type': 'Open Market Purchase', 'trade_shares': 1000, 'max_trade_date_str': '2026-10-01'},
            {'name': 'B', 'transaction_type': 'Purchase', 'trade_shares': 500, 'max_trade_date_str': '2026-10-08'},
            {'name': 'C', 'transaction_type': 'Other Acquisition', 'trade_shares': 900, 'max_trade_date_str': '2026-10-08'},
            {'name': 'D', 'transaction_type': 'Purchase', 'trade_shares': 900, 'max_trade_date_str': '2026-08-01'}]}}, hari)
        self.assertEqual(od, {'bilangan': 2, 'tarikh': '2026-10-08'})

    def test_pengesahan_panas(self):
        idx = pd.bdate_range('2026-09-01', '2026-10-14')
        c = pd.Series(10.0, index=idx); v = pd.Series(1e6, index=idx)
        c.loc['2026-10-09':] = [11.0, 11.2, 11.1, 11.3]; v.loc['2026-10-09'] = 3.5e6
        s = G.pengesahan(c, v, '2026-10-08', selepas_tutup=True)
        self.assertEqual(s['hari'], '2026-10-09')
        self.assertEqual(s['gerak_pct'], 10.0)
        self.assertEqual(s['volum_x'], 3.5)
        self.assertTrue(s['kekal'])
        p = {'berita': [{'tajuk': 'Acme beats, raises guidance', 'tarikh': '2026-10-08', 'selepas_tutup': True}]}
        m, ring = G.mata_pemangkin({**p, 'pengesahan': s}, date(2026, 10, 9))
        self.assertEqual(m, 3 + 2)
        self.assertTrue(ring.startswith('🔥 PANAS'))
        m, ring = G.mata_pemangkin({**p, 'pengesahan': {**s, 'gerak_pct': -4.0, 'kekal': False}}, date(2026, 10, 9))
        self.assertEqual(m, 3 - 1)
        self.assertIn('pasaran tolak', ring)
        self.assertIsNone(G.pengesahan(c, v, '2026-10-20'))

    def test_kumpul(self):
        import json, tempfile, os
        hari = date(2026, 10, 15)
        with tempfile.TemporaryDirectory() as d:
            ts = int(pd.Timestamp('2026-10-14 17:30', tz='America/New_York').timestamp())
            with open(os.path.join(d, 'berita_CF.json'), 'w') as f:
                json.dump([{'type': 'text', 'text': json.dumps({'data': [
                    {'title': '<em>CF</em> Industries beats estimates', 'publish_time': ts, 'url': 'https://n/1'},
                    {'title': 'Vertex advances <em>CF</em> therapy', 'publish_time': ts, 'url': 'https://n/2'}]})}], f)
            e = G.kumpul_pemangkin(d, {'CF': 'CF Industries Holdings'}, hari)['CF']
            self.assertEqual(len(e['berita']), 1)
            self.assertEqual(e['berita'][0]['tarikh'], '2026-10-14')
            self.assertTrue(e['berita'][0]['selepas_tutup'])
            self.assertEqual(e['dikumpul'], '2026-10-15')
        self.assertTrue(G.segar({'dikumpul': '2026-10-13'}, hari))
        self.assertFalse(G.segar({'dikumpul': '2026-10-09'}, hari))

    def test_keseluruhan(self):
        self.assertEqual(G.gred_keseluruhan(['A', 'A', '–', 'B']), 'A')
        self.assertEqual(G.gred_keseluruhan(['–', '–']), '–')
        self.assertEqual(G.gred_keseluruhan(['C', 'C', 'D']), 'C')


if __name__ == '__main__':
    unittest.main()
