# Ujian sumber pemangkin percuma: standard/pemangkin_actions.py (Actions) dan gred.py --yahoo/--nasdaq
import csv, json, os, sys, tempfile, time, unittest
from datetime import date, datetime, timezone
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import gred as G  # noqa: E402
import pemangkin_actions as PA  # noqa: E402

HARI = date(2026, 10, 16)
utc = lambda s: int(pd.Timestamp(s, tz='America/New_York').timestamp())


class UjiPemangkinActions(unittest.TestCase):
    def test_berita_yf_format_baharu_dan_lama(self):
        sejak = utc('2026-10-05 00:00')
        items = [{'id': 'a', 'content': {'title': 'Acme Robotics beats estimates', 'pubDate': '2026-10-15T21:30:00Z',
                                         'canonicalUrl': {'url': 'https://finance.yahoo.com/a'}}},
                 {'id': 'b', 'content': {'title': 'Stock market today: Dow rises', 'pubDate': '2026-10-15T14:00:00Z'}},
                 {'title': 'Acme Robotics wins Army contract', 'providerPublishTime': utc('2026-10-14 10:00'), 'link': 'https://x/b'},
                 {'id': 'c', 'content': {'title': 'Acme Robotics old news', 'pubDate': '2026-09-01T10:00:00Z'}}]
        b = PA.berita_yf(items, sejak, 'ACME', 'Acme Robotics Inc.')
        self.assertEqual([x['url'] for x in b], ['https://finance.yahoo.com/a', 'https://x/b'])
        self.assertEqual(b[0]['masa'], int(datetime(2026, 10, 15, 21, 30, tzinfo=timezone.utc).timestamp()))

    def test_analisis_dan_orang_dalam_yf(self):
        idx = pd.to_datetime(['2026-10-14 12:00', '2026-10-10 12:00', '2026-09-01 12:00'])
        df = pd.DataFrame({'Firm': ['UBS', 'BMO', 'Citi'], 'ToGrade': ['Buy', 'Outperform', 'Sell'],
                           'FromGrade': ['', 'Market Perform', 'Neutral'], 'Action': ['main', 'up', 'down'],
                           'currentPriceTarget': [150.0, 120.0, 0.0], 'priorPriceTarget': [130.0, 0.0, 0.0]}, index=idx)
        a = PA.analisis_yf(df, date(2026, 10, 5))
        self.assertEqual([x['firma'] for x in a], ['UBS', 'BMO'])
        self.assertEqual(a[0]['sasaran_lalu'], 130.0)
        self.assertIsNone(a[1]['sasaran_lalu'])
        od = pd.DataFrame({'Text': ['Purchase at price 10.00 per share.', 'Sale at price 11.00 per share.', ''],
                           'Insider': ['A', 'B', 'C'], 'Shares': [1000, 500, 10],
                           'Start Date': pd.to_datetime(['2026-10-08', '2026-10-09', '2026-10-09'])})
        o = PA.orang_dalam_yf(od, date(2026, 9, 15))
        self.assertEqual(o, [{'tarikh': '2026-10-08', 'nama': 'A', 'teks': 'Purchase at price 10.00 per share.', 'saham': 1000}])
        self.assertEqual(PA.analisis_yf(pd.DataFrame(), date(2026, 10, 5)), [])

    def test_rss_dan_berita_nasdaq(self):
        from unittest import mock
        rss = (b'<?xml version="1.0"?><rss><channel><item><title>Acme Robotics beats estimates</title>'
               b'<link>https://finance.yahoo.com/n/1</link><pubDate>Thu, 15 Oct 2026 21:30:00 +0000</pubDate></item>'
               b'<item><title>Tanpa tarikh</title><link>https://x/2</link></item></channel></rss>')
        jwb = mock.Mock(content=rss); jwb.raise_for_status = lambda: None
        with mock.patch('requests.get', return_value=jwb):
            n = PA.rss_yahoo('ACME')
        self.assertEqual(n, [{'title': 'Acme Robotics beats estimates', 'link': 'https://finance.yahoo.com/n/1',
                              'pubDate': int(datetime(2026, 10, 15, 21, 30, tzinfo=timezone.utc).timestamp())}])
        self.assertEqual(len(PA.berita_yf(n, utc('2026-10-05 00:00'), 'ACME', 'Acme Robotics')), 1)
        jwb = mock.Mock(); jwb.raise_for_status = lambda: None
        jwb.json = lambda: {'data': {'rows': [{'title': 'Acme Robotics wins contract', 'url': '/articles/acme-1',
                                               'created': 'Oct 14, 2026'}, {'title': 'x', 'created': 'semalam'}]}}
        with mock.patch('requests.get', return_value=jwb):
            n = PA.berita_nasdaq('ACME')
        self.assertEqual([x['link'] for x in n], ['https://www.nasdaq.com/articles/acme-1'])

    def test_tiada_data_bukan_ralat(self):
        class YFDataException(Exception):
            pass
        self.assertTrue(PA.tiada_data(KeyError('upgradeDowngradeHistory')))
        self.assertTrue(PA.tiada_data(YFDataException('No upgrade/downgrade history found for X')))
        self.assertFalse(PA.tiada_data(YFDataException('*** YAHOO! FINANCE IS CURRENTLY DOWN! ***')))
        self.assertFalse(PA.tiada_data(ConnectionError('reset')))
        self.assertTrue(PA.tiada_data(Exception('HTTP Error 404: ')))

    def test_main_cache_setiap_ticker(self):
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, 'senarai_beli.csv')
            with open(f, 'w', newline='', encoding='utf-8') as h:
                w = csv.writer(h); w.writerow(['saham', 'nama']); w.writerows([['AAA', 'Aaa Corp'], ['BBB', 'Bbb Inc']])
            keluar = os.path.join(d, 'pem')
            dipanggil = []

            def ty(nama, hari_ini, had_saat=0):
                dipanggil.append(sorted(nama))
                k = int(time.time())
                return {t: ({'diambil': k, 'berita': [], 'analisis': [], 'orang_dalam': [], 'ralat': ['berita: X']} if t == 'BBB'
                            else {'diambil': k, 'berita': [], 'analisis': [], 'orang_dalam': []}) for t in nama}
            tn = lambda hari_ini, simpan: {'dari': '', 'hingga': '', 'hari_ralat': 0, 'ralat': [], 'saham': {'AAA': {'lalu': '2026-08-01'}}}
            arg = ['--csv', f, '--keluar', keluar]
            PA.main(arg, ty, tn, HARI)
            st = json.load(open(os.path.join(keluar, 'status.json')))
            self.assertEqual((st['yahoo_dikumpul'], st['yahoo_ralat'], st['lengkap']), (1, 1, False))
            PA.main(arg, ty, tn, HARI)       # larian kedua: hanya BBB (beralat) diambil semula
            self.assertEqual(dipanggil, [['AAA', 'BBB'], ['BBB']])
            y = json.load(open(os.path.join(keluar, 'yahoo.json')))
            self.assertEqual((y['tarikh'], sorted(y['saham'])), ('2026-10-16', ['AAA', 'BBB']))
            PA.main(arg, ty, tn, date(2026, 10, 17))   # hari baharu: semua diambil semula
            self.assertEqual(dipanggil[-1], ['AAA', 'BBB'])
            PA.main(arg + ['--segar-jam', '0'], ty, tn, date(2026, 10, 17))   # entri lama (> had jam): diambil semula
            self.assertEqual(dipanggil[-1], ['AAA', 'BBB'])


class UjiGredYahooNasdaq(unittest.TestCase):
    def test_berita_analisis_orang_dalam_yahoo(self):
        b = G.berita_yahoo([{'tajuk': 'Acme Robotics beats, raises guidance', 'masa': utc('2026-10-15 16:30'), 'url': 'https://y/1'},
                            {'tajuk': 'Fed holds rates', 'masa': utc('2026-10-15 14:00'), 'url': 'https://y/2'}],
                           'ACME', 'Acme Robotics Inc.', HARI)
        self.assertEqual(len(b), 1)
        self.assertEqual((b[0]['tarikh'], b[0]['selepas_tutup'], b[0]['hari_lalu'], b[0]['sumber']), ('2026-10-15', True, 1, 'yahoo'))
        a = G.analisis_yahoo([
            {'tarikh': '2026-10-14', 'firma': 'UBS', 'tindakan': 'main', 'ke': 'Buy', 'sasaran': 150.0, 'sasaran_lalu': 130.0},
            {'tarikh': '2026-10-09', 'firma': 'UBS', 'tindakan': 'up', 'ke': 'Buy'},          # bukan terkini firma itu
            {'tarikh': '2026-10-13', 'firma': 'BMO', 'tindakan': 'up', 'ke': 'Outperform'},
            {'tarikh': '2026-10-12', 'firma': 'Citi', 'tindakan': 'init', 'ke': 'Sector Underperform'},
            {'tarikh': '2026-10-12', 'firma': 'JPM', 'tindakan': 'init', 'ke': 'Overweight'},
            {'tarikh': '2026-10-12', 'firma': 'MS', 'tindakan': 'init', 'ke': 'Equal-Weight'},
            {'tarikh': '2026-10-11', 'firma': 'RBC', 'tindakan': 'reit', 'ke': 'Outperform', 'sasaran': 90.0, 'sasaran_lalu': 100.0},
            {'tarikh': '2026-10-11', 'firma': 'GS', 'tindakan': 'main', 'ke': 'Buy', 'sasaran': 100.0, 'sasaran_lalu': 100.0},
            {'tarikh': '2026-09-20', 'firma': 'BofA', 'tindakan': 'down', 'ke': 'Neutral'}], HARI)
        k = {x['firma']: (x['kategori'], x['mata']) for x in a}
        self.assertEqual(k, {'UBS': ('naik_sasaran_besar', 2), 'BMO': ('naik_taraf', 2), 'Citi': ('mula_jual', -2),
                             'JPM': ('mula_beli', 2), 'RBC': ('potong_sasaran', -2)})
        od = G.orang_dalam_yahoo([{'tarikh': '2026-10-08', 'nama': 'A', 'saham': 1000}, {'tarikh': '2026-10-09', 'nama': 'B', 'saham': 5},
                                  {'tarikh': '2026-10-09', 'nama': 'A', 'saham': 50}, {'tarikh': '2026-08-01', 'nama': 'C', 'saham': 9}], HARI)
        self.assertEqual(od, {'bilangan': 2, 'tarikh': '2026-10-09'})

    def test_earnings_nasdaq(self):
        o, d = G.earnings_nasdaq({'lalu': '2026-10-13', 'lalu_masa': 'time-after-hours', 'seterusnya': '2027-01-20'}, HARI)
        self.assertEqual((o['earnings_lalu_tarikh'], o['earnings_lalu_hari'], o['earnings_selepas_tutup']), ('2026-10-13', 3, True))
        self.assertEqual(d, date(2027, 1, 20))
        o, d = G.earnings_nasdaq({'lalu': '2026-10-16', 'lalu_masa': 'time-pre-market'}, HARI)   # laporan hari ini
        self.assertEqual((o, d), ({}, HARI))
        o, d = G.earnings_nasdaq({'lalu': '2026-09-01', 'lalu_masa': 'time-not-supplied'}, HARI)
        self.assertIsNone(o['earnings_selepas_tutup'])
        self.assertIsNone(d)
        self.assertEqual(G.earnings_nasdaq(None, HARI), ({}, None))

    def test_reaksi_earnings_masa_tidak_diketahui(self):
        idx = pd.bdate_range('2026-09-01', '2026-10-14')
        c = pd.Series(10.0, index=idx); v = pd.Series(1e6, index=idx)
        c.loc['2026-10-09':] = 11.0; v.loc['2026-10-09'] = 4e6            # pengumuman 8 Okt selepas tutup
        self.assertEqual(G.reaksi_earnings(c, v, '2026-10-08'), 10.0)
        self.assertEqual(G.reaksi_earnings(c, v, '2026-10-08', False), 0.0)   # masa diketahui: hari pengumuman
        c2 = c.copy(); v2 = pd.Series(1e6, index=idx)
        c2.loc['2026-10-08':] = 9.0; v2.loc['2026-10-08'] = 5e6           # pengumuman 8 Okt sebelum dibuka
        self.assertEqual(G.reaksi_earnings(c2, v2, '2026-10-08'), -10.0)
        self.assertIsNone(G.reaksi_earnings(c, v, '2026-10-14'))           # hari berikutnya belum ada

    def test_kumpul_dan_tambah(self):
        with tempfile.TemporaryDirectory() as d:
            p = lambda n: os.path.join(d, n)
            idx = pd.bdate_range('2025-09-01', '2026-10-15')
            hr = []
            for t, mula in (('AAA', 10.0), ('BBB', 20.0), ('CCC', 30.0)):
                for i, x in enumerate(idx):
                    c = mula * (1 + 0.001 * i)
                    if t == 'AAA' and x >= pd.Timestamp('2026-10-14'):
                        c *= 1.25                                   # reaksi earnings 13 Okt selepas tutup: +25%
                    hr.append([t, x.strftime('%Y-%m-%d'), round(c, 4), 1e6])
            pd.DataFrame(hr, columns=['ticker', 'date', 'close', 'volume']).to_csv(p('harga_A.csv'), index=False)
            with open(p('sektor.csv'), 'w', encoding='utf-8') as h:
                h.write('tarikh,jenis,nama,skor_panas\n2026-10-15,Sektor,Technology,70\n')
            with open(p('senarai_beli.csv'), 'w', newline='', encoding='utf-8') as h:
                w = csv.writer(h); w.writerow(['saham', 'nama', 'sektor', 'industri'])
                w.writerows([['AAA', 'Aaa Robotics Inc.', 'Technology', ''], ['BBB', 'Bbb Corp', 'Technology', ''],
                             ['CCC', 'Ccc Ltd', 'Technology', ''], ['DDD', 'Ddd Inc', 'Technology', '']])
            k = utc('2026-10-16 08:30')                         # 8:30 malam MYT tarikh imbasan
            yahoo = {'tarikh': '2026-10-16', 'saham': {
                'AAA': {'diambil': k, 'berita': [{'tajuk': 'Aaa Robotics upgraded at UBS', 'masa': utc('2026-10-15 09:00'), 'url': 'https://y/a'}],
                        'analisis': [{'tarikh': '2026-10-15', 'firma': 'UBS', 'tindakan': 'up', 'ke': 'Buy'}], 'orang_dalam': []},
                'BBB': {'diambil': k, 'berita': [], 'analisis': [], 'orang_dalam': []},
                'CCC': {'diambil': k, 'berita': [], 'analisis': [], 'orang_dalam': [], 'ralat': ['berita: HTTPError']},
                'DDD': {'diambil': utc('2026-10-15 23:00'), 'berita': [], 'analisis': [], 'orang_dalam': []}}}
            json.dump(yahoo, open(p('yahoo.json'), 'w'))
            json.dump({'tarikh': '2026-10-16', 'hari_ralat': 0, 'saham': {
                'AAA': {'lalu': '2026-10-13', 'lalu_masa': 'time-after-hours', 'seterusnya': ''},
                'BBB': {'lalu': '2026-08-20', 'lalu_masa': 'time-pre-market', 'seterusnya': '2026-10-27', 'seterusnya_masa': 'time-pre-market'}}},
                open(p('nas.json'), 'w'))
            # entri Moomoo BBB hari ini (Peringkat 2) tidak boleh ditimpa oleh Yahoo
            json.dump({'BBB': {'dikumpul': '2026-10-16', 'sumber_pemangkin': 'moomoo', 'berita': [], 'analisis': [],
                               'orang_dalam': {'bilangan': 2, 'tarikh': '2026-10-10'}}}, open(p('pem.json'), 'w'))
            G.main(['kumpul', '--yahoo', p('yahoo.json'), '--nasdaq', p('nas.json'), '--csv', p('senarai_beli.csv'),
                    '--keluar', p('pem.json'), '--tarikh', '2026-10-16'])
            pem = json.load(open(p('pem.json')))
            self.assertEqual(sorted(pem), ['AAA', 'BBB'])     # CCC beralat, DDD diambil pagi (11 pagi MYT): tidak dipakai
            self.assertEqual(pem['AAA']['sumber_pemangkin'], 'yahoo')
            self.assertEqual(pem['AAA']['earnings_lalu_tarikh'], '2026-10-13')
            self.assertEqual(pem['BBB']['orang_dalam'], {'bilangan': 2, 'tarikh': '2026-10-10'})
            G.main(['tambah', '--csv', p('senarai_beli.csv'), '--harga', d, '--sektor', p('sektor.csv'),
                    '--pemangkin', p('pem.json'), '--nasdaq', p('nas.json'), '--tarikh', '2026-10-16'])
            r = {x['saham']: x for x in csv.DictReader(open(p('senarai_beli.csv'), encoding='utf-8'))}
            self.assertEqual((r['BBB']['tarikh_earnings'], r['BBB']['sumber_earnings'], r['BBB']['gred_qr']), ('2026-10-27', 'Nasdaq', 'D'))
            self.assertEqual((r['AAA']['sumber_earnings'], r['AAA']['gred_qr']), ('anggaran; QR lalu 3 hari', 'B'))   # QR lalu 13 Okt: 3 hari -> B
            self.assertEqual((r['CCC']['sumber_earnings'], r['CCC']['gred_qr'], r['CCC']['gred_pemangkin']), ('tiada data', '–', '–'))
            # pemangkin v3: K2 (reaksi +25%, umur 1 hari dagangan dalam stor) -> A; K1 (earnings 7 hari dagangan lagi) -> B; naik taraf: tiada mata
            self.assertEqual((r['AAA']['gred_pemangkin'], r['AAA']['mata_pemangkin']), ('A', '4'))
            self.assertTrue(r['AAA']['pemangkin'].startswith('🔥 PANAS · reaksi earnings +25.1% lawan pasaran (1 hari lalu) +4'))
            self.assertEqual((r['BBB']['gred_pemangkin'], r['BBB']['mata_pemangkin']), ('B', '2'))
            self.assertIn('earnings 7 hari dagangan lagi', r['BBB']['pemangkin'])
            self.assertEqual(r['DDD']['gred_pemangkin'], '–')   # tiada data earnings dan berita
            # fail Yahoo semalam tidak dipakai
            yahoo['tarikh'] = '2026-10-15'; json.dump(yahoo, open(p('yahoo.json'), 'w'))
            os.remove(p('pem.json'))
            G.main(['kumpul', '--yahoo', p('yahoo.json'), '--keluar', p('pem.json'), '--tarikh', '2026-10-16'])
            self.assertEqual(json.load(open(p('pem.json'))), {})


if __name__ == '__main__':
    unittest.main()
