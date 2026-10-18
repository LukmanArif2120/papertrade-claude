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
        # skema 18 Okt 2026: A/B hanya jika disahkan; RS >= 80 tidak/belum disahkan -> C; < 70 -> D
        self.assertEqual([G.gred_rs(x, True) for x in [99, 90, 89, 80, 79, 70, 69, 1, None]],
                         ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', '–'])
        self.assertEqual([G.gred_rs(x, s) for x, s in [(99, False), (85, None), (75, False), (60, True)]],
                         ['C', 'C', 'C', 'D'])
        self.assertEqual([G.gred_kumpulan(x) for x in [80, 79.9, 60, 40, 20, 19, None]],
                         ['A', 'B', 'B', 'C', 'D', 'E', '–'])
        self.assertEqual([G.gred_qr(x) for x in [None, 22, 21, 16, 15, 11, 10, 6, 5, 0]],
                         ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E'])
        # selepas QR: 0–1 hari -> sekurang-kurangnya C, 2–3 -> sekurang-kurangnya B; gred lebih buruk kekal
        self.assertEqual([G.gred_qr(60, s) for s in [0, 1, 2, 3, 4, None]], ['C', 'C', 'B', 'B', 'A', 'A'])
        self.assertEqual([G.gred_qr(None, 1), G.gred_qr(8, 1), G.gred_qr(3, 2), G.gred_qr(13, 3)], ['C', 'D', 'E', 'C'])

    def test_keseluruhan_baris(self):
        r = {'kaedah': 'M01', 'gred_sektor': 'E', 'gred_industri': 'A', 'gred_pemangkin': 'C', 'gred_qr': 'A'}
        self.assertEqual(G.keseluruhan_baris(r, {'M01': 'momentum'}), 'B')      # (4+2+4)/3; Sektor tidak dikira
        self.assertEqual(G.keseluruhan_baris(r, {'M01': 'pantulan'}), 'B')      # (2+4)/2; Industri tidak terpakai
        self.assertEqual(G.keseluruhan_baris(dict(r, gred_pemangkin='E', gred_qr='E'), {'M01': 'pantulan'}), 'E')

    def test_pasca_qr(self):
        self.assertEqual(G.sejak_qr(date(2026, 10, 15), date(2026, 10, 19)), 2)    # Khamis -> Isnin
        self.assertIsNone(G.sejak_qr(date(2026, 10, 19), date(2026, 10, 19)))
        self.assertIsNone(G.sejak_qr(None, date(2026, 10, 19)))
        self.assertEqual(G.tanda_pasca_qr('Nasdaq', 2), 'Nasdaq; QR lalu 2 hari')
        self.assertEqual(G.tanda_pasca_qr('Nasdaq', 4), 'Nasdaq')

    def test_rs_pengesahan(self):
        self.assertTrue(G.disahkan(5.0, 1.0, True))
        self.assertFalse(G.disahkan(5.0, 1.0, False))
        self.assertFalse(G.disahkan(-1.0, 1.0, True))
        self.assertFalse(G.disahkan(5.0, -0.5, True))
        self.assertIsNone(G.disahkan(None, 1.0, True))
        self.assertEqual(G.tanda_rs(96, 5.0, 1.0, True), 'RS 95+: purata tertinggi tetapi berisiko (median ≈ 0)')
        self.assertEqual(G.tanda_rs(85, 5.0, 1.0, False), 'tidak disahkan: pasaran lemah (SPY < SMA200)')
        self.assertEqual(G.tanda_rs(75, -5.0, -1.0, False), '')

    def test_rs_stor_dan_pasaran(self):
        import tempfile, json as _j
        ix = pd.bdate_range('2025-01-01', periods=300)
        c = pd.DataFrame({'KUAT': np.linspace(10, 40, 300), 'LEMAH': np.linspace(40, 10, 300),
                          'MURAH': np.linspace(1, 4, 300), 'SED': np.linspace(10, 11, 300)}, index=ix)
        spy = pd.Series(np.linspace(100, 150, 300), index=ix)
        st, atas = G.rs_semua(c, spy, None)
        self.assertTrue(atas)
        self.assertNotIn('MURAH', st.rs.dropna().index)            # tutup < USD5 tidak dipangkat
        self.assertEqual(set(st.rs_sumber), {'stor'})
        r = {}; G.isi_rs(r, st.loc['KUAT'], atas)
        self.assertEqual((r['gred_rs'], r['rs_sah'], r['rs_sumber']), ('A', 'ya', 'stor'))
        r = {}; G.isi_rs(r, st.loc['LEMAH'], atas)
        self.assertEqual(r['gred_rs'], 'D')
        with tempfile.TemporaryDirectory() as d:   # rs_pasaran sesi sama diutamakan; sesi lain diabaikan
            sesi = str(ix[-1].date())
            pd.DataFrame([dict(tarikh=sesi, ticker='SED', rs=88, skor=0.1, mutlak12=3.0, mansfield=2.0, rs_industri=70)]
                         ).to_csv(os.path.join(d, 'rs_pasaran.csv'), index=False)
            _j.dump({'spy_atas200': {sesi: True}}, open(os.path.join(d, 'status.json'), 'w'))
            st2, _ = G.rs_semua(c, spy, d)
            self.assertEqual((st2.loc['SED', 'rs'], st2.loc['SED', 'rs_sumber']), (88, 'pasaran'))
            self.assertEqual(st2.loc['KUAT', 'rs_sumber'], 'stor')
            r = {}; G.isi_rs(r, st2.loc['SED'], True)
            self.assertEqual((r['gred_rs'], r['rs_industri']), ('B', 70))
            st3, _ = G.rs_semua(c.iloc[:-1], spy, d)
            self.assertEqual(set(st3.rs_sumber), {'stor'})

    def test_hari_dagangan(self):
        self.assertEqual(G.hari_dagangan(date(2026, 10, 9), date(2026, 10, 13)), 2)  # Jumaat -> Selasa
        self.assertEqual(G.hari_dagangan(date(2026, 10, 13), date(2026, 10, 13)), 0)

    def test_tajuk_berita(self):
        self.assertEqual(G.nilai_tajuk('Goldman Sachs Upgrades KB Home to Buy, Raises Target Price to $60'), 1)
        self.assertEqual(G.nilai_tajuk('Goldman Sachs Maintains KB Home With Hold Rating, Cuts Target Price to $56'), -1)
        self.assertEqual(G.nilai_tajuk('Morgan Stanley Initiates KB Home With Sell Rating'), -1)
        self.assertEqual(G.nilai_tajuk('DHI, LEN, KBH: Trending With Analysts'), 0)

    def test_pemangkin_v3_k1_dan_gred(self):
        hari = date(2026, 10, 16)
        self.assertEqual(G.nilai_pemangkin({}, hari, 10)[:2], (2, 'B'))
        self.assertEqual(G.nilai_pemangkin({}, hari, 21)[:2], (2, 'B'))
        self.assertEqual(G.nilai_pemangkin({}, hari, 5)[:2], (1, 'C'))
        self.assertEqual(G.nilai_pemangkin({}, hari, 0)[:2], (0, 'D'))   # earnings hari ini: tiada premium tersisa
        m, g, ring = G.nilai_pemangkin({}, hari, None)
        self.assertEqual((m, g, ring), (0, 'D', 'tiada pemangkin'))
        self.assertEqual(G.nilai_pemangkin({}, hari, 22)[1], 'D')
        self.assertEqual([G.gred_pemangkin(x) for x in [4, 3, 2, 1, 0, -1, None]], ['A', 'A', 'B', 'C', 'D', 'E', '–'])

    def test_pemangkin_v3_k2_reaksi_melampau(self):
        idx = pd.bdate_range('2026-08-03', '2026-10-15')
        c = pd.Series(10.0, index=idx); v = pd.Series(1e6, index=idx); spy = pd.Series(500.0, index=idx)
        c.loc['2026-10-09':] = 12.5; v.loc['2026-10-09'] = 5e6        # selepas tutup 8 Okt: +25% pada 9 Okt
        p = {'earnings_lalu_tarikh': '2026-10-08', 'earnings_selepas_tutup': None}
        m, g, ring = G.nilai_pemangkin(p, date(2026, 10, 16), None, c, v, spy)
        self.assertEqual((m, g), (4, 'A'))                             # umur 4 hari dagangan
        self.assertTrue(ring.startswith('🔥 PANAS'))
        self.assertIn('+25.0%', ring)
        m, g, _ = G.nilai_pemangkin(p, date(2026, 10, 16), 8, c, v, spy)
        self.assertEqual((m, g), (6, 'A'))
        spy.loc['2026-10-09':] = 550.0                                  # pasaran +10% hari sama -> lebihan +15%
        self.assertEqual(G.nilai_pemangkin(p, date(2026, 10, 16), None, c, v, spy)[:2], (0, 'D'))
        c2 = c[:'2026-10-09']; c2 = pd.concat([c2, pd.Series(12.5, index=pd.bdate_range('2026-10-12', periods=14))])
        v2 = v.reindex(c2.index).fillna(1e6)
        m, g, _ = G.nilai_pemangkin(p, date(2026, 10, 30), None, c2, v2, None)
        self.assertEqual((m, g), (3, 'A'))                              # umur 14 hari: separuh
        c3 = pd.concat([c2, pd.Series(12.5, index=pd.bdate_range('2026-10-30', periods=7))]); v3 = v.reindex(c3.index).fillna(1e6)
        self.assertEqual(G.nilai_pemangkin(p, date(2026, 11, 9), None, c3, v3, None)[:2], (0, 'D'))   # umur > 20
        self.assertEqual(G.nilai_pemangkin({'earnings_gerak_pct': 22.0, 'earnings_lalu_hari': 3}, date(2026, 10, 16))[:2], (4, 'A'))
        m, g, ring = G.nilai_pemangkin({'earnings_gerak_pct': 22.0, 'earnings_lalu_hari': 3,
                                        'berita': [{'tajuk': 'Acme prices $500 million convertible notes offering', 'hari_lalu': 1}]}, date(2026, 10, 16))
        self.assertEqual((m, g), (4, 'C'))
        self.assertFalse(ring.startswith('🔥'))
        self.assertEqual(G.nilai_pemangkin({'earnings_gerak_pct': 12.0, 'earnings_lalu_hari': 3}, date(2026, 10, 16))[:2], (0, 'D'))

    def test_pemangkin_v3_veto(self):
        hari = date(2026, 10, 16)
        b = lambda tajuk, h=3: {'berita': [{'tajuk': tajuk, 'hari_lalu': h}]}
        m, g, ring = G.nilai_pemangkin(b('Acme announces $20 million registered direct offering'), hari, 10)
        self.assertEqual((m, g), (2, 'C'))
        self.assertIn('pencairan', ring)
        self.assertEqual(G.nilai_pemangkin(b('Acme prices secondary offering of shares by selling stockholders'), hari, 10)[1], 'B')
        self.assertEqual(G.nilai_pemangkin(b('Acme agrees to be acquired by Globex for $30 per share in cash'), hari, 10)[1], 'D')
        self.assertEqual(G.nilai_pemangkin(b('Acme PDUFA date set for November 12'), hari, 10)[1], 'C')
        self.assertEqual(G.nilai_pemangkin(b('Acme reports positive topline results from Phase 3 trial'), hari, 3)[1], 'C')  # K1 sahaja
        self.assertEqual(G.nilai_pemangkin(b('FDA advisory committee to review Acme drug on Nov 3'), hari, 10)[1], 'C')
        self.assertEqual(G.nilai_pemangkin(b('Acme announces $20 million registered direct offering', 40), hari, 10)[1], 'B')
        self.assertEqual(G.nilai_pemangkin(b('Acme upgraded to Buy at UBS'), hari, 10)[:2], (2, 'B'))   # analisis: tiada mata
        self.assertEqual(G.veto_tajuk('Acme Keeps Quarterly Dividend'), None)

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
