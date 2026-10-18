# Ujian standard/gred_kewangan.py (gred kewangan v7; spec/GRED_KEWANGAN_v7.md)
import os, sys, math, json, tempfile, unittest
from datetime import date

import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import gred_kewangan as GK  # noqa: E402

P, K, T = GK.P, GK.K, GK.T


def akhir_suku(tahun, q):
    return pd.Timestamp(year=tahun, month=3 * q, day=1) + pd.offsets.MonthEnd(0)


def syarikat(n=28, g=0.20, mula=2019, margin_op=0.25, hutang_aset=0.22, tunai_aset=0.10, ocf_x=1.2, lain=None, muda=False):
    """Syarikat sintetik: n suku bermula Q1 tahun `mula`, hasil tumbuh g setahun."""
    suku = []
    for i in range(n):
        th, q = mula + i // 4, i % 4 + 1
        r = 100.0 * (1 + g) ** (i / 4)
        op = r * margin_op
        fa = r * 0.01
        x = (lain or {}).get(i, 0.0)
        pt = op - fa + x
        tx = max(pt, 0) * 0.21
        ni = pt - tx
        aset = 8 * r
        hut = aset * hutang_aset
        e = {'tamat': akhir_suku(th, q).date().isoformat(), 'label': f'{th}/Q{q}',
             P: {'Total Operating Revenue': r, 'Cost of Revenue': r * 0.4, 'Gross Profit': r * 0.6,
                 'Operating Expense': r * 0.6 - op, 'Selling and Admin Expenses': r * 0.2, 'Operating Profit': op,
                 'Non-Operating Interest Expense': fa, 'Non-Operating Interest Income': r * 0.001,
                 'Other Income (Expense)': x, 'Pretax Profit': pt, 'Tax': tx, 'Net Profit': ni,
                 'Net Income to Parent Company': ni, 'Diluted EPS': ni / 100},
             K: {'Total Assets': aset, 'Total Current Assets': aset * 0.40, 'Total Current Liabilities': aset * 0.15,
                 'Total Non-Current Liabilities': aset * 0.25, 'Total Liabilities': aset * 0.40,
                 'Cash and Cash Equivalents & Short-Term Investments': aset * tunai_aset,
                 'Short-Term Debt and Capital Lease Obligation': hut * 0.1,
                 'Long Term Debt and Capital Lease Obligation': hut * 0.9,
                 '-Current Debt': hut * 0.1, '-Long Term Debt': hut * 0.9,
                 'Total Equity': aset * 0.60, "Stockholders' Equity": aset * 0.60, 'Retained Earnings': aset * 0.30,
                 'Receivables': aset * 0.10, 'Inventory': aset * 0.05, 'Net PPE': aset * 0.20},
             T: {'Operating Cash Flow': ni * ocf_x if not muda else -r * 0.3, 'Change in Working Capital': 0.0,
                 'Depreciation & Depletion & Amortization': r * 0.05,
                 'Free Cash Flow': (ni * ocf_x - r * 0.04) if not muda else -r * 0.35,
                 'Net Common Stock Issuance': -1.0, 'Net Income from Continuing Operations': ni}}
        if muda:
            e[P]['Operating Profit'] = -r * 0.30
        suku.append(e)
    tahunan = []
    for th in range(mula, mula + n // 4):
        qs = [e for e in suku if e['label'].startswith(f'{th}/')]
        a = {'tamat': qs[-1]['tamat'], 'label': f'{th}/FY', P: {}, K: {}, T: {}}
        for b in (P, T):
            for kk in qs[0][b]:
                a[b][kk] = sum(e[b][kk] for e in qs)
        tahunan.append(a)
    return {'ticker': 'X', 'suku': suku, 'tahunan': tahunan, 'terbit': {}, 'saham_terbit': None}


class UjiNormal(unittest.TestCase):
    def test_tamat_utc8(self):
        # 2026-06-30 00:00 UTC+8 = 2026-06-29 16:00 UTC
        self.assertEqual(GK.tamat_tempoh(1782748800000), date(2026, 6, 30))

    def test_gabung_ikut_label(self):
        a = [{'tamat': '2021-10-29', 'label': '2022/Q3', 'medan': {'Total Operating Revenue': 1}}]
        b = [{'tamat': '2021-10-30', 'label': '2022/Q3', 'medan': {'Total Assets': 5}}]
        g = GK.gabung_tempoh([(P, a), (K, b)])
        self.assertEqual(len(g), 1)
        self.assertEqual(g[0][P]['Total Operating Revenue'], 1)
        self.assertEqual(g[0][K]['Total Assets'], 5)

    def test_simpan_fail_mentah(self):
        with tempfile.TemporaryDirectory() as d:
            m, out = os.path.join(d, 'm'), os.path.join(d, 'k')
            os.makedirs(m)
            rep = {'data': {'report_list': [{'date_time': 1782748800000, 'period_text': '2026/Q3',
                                             'item_list': [{'display_name': 'Total Operating Revenue', 'data': 600.0},
                                                           {'display_name': 'Basic EPS', 'data': None}]}]}}
            json.dump(rep, open(os.path.join(m, 'ABC_1_9.json'), 'w'))
            json.dump({'data': {'records': [{'period_text': '2026/Q3', 'pub_trading_day_str': '2026-07-29',
                                             'pub_type': 2, 'is_current': False},
                                            {'period_text': '2026/Q4', 'pub_trading_day_str': '2026-11-01',
                                             'is_current': True}]}}, open(os.path.join(m, 'ABC_eph.json'), 'w'))
            GK.simpan(m, out, '2026-10-18')
            k = json.load(open(os.path.join(out, 'ABC.json')))
            self.assertEqual(k['suku'][0]['tamat'], '2026-06-30')
            self.assertEqual(k['suku'][0][P], {'Total Operating Revenue': 600.0})   # medan None dibuang
            self.assertEqual(k['terbit'], {'2026/Q3': {'pub': '2026-07-29', 'jenis': 2}})   # is_current dibuang


class UjiMasa(unittest.TestCase):
    def test_tersedia(self):
        e = {'label': '2026/Q2', 'tamat': '2026-06-30'}
        self.assertFalse(GK.tersedia(e, {}, date(2026, 8, 13)))     # 44 hari
        self.assertTrue(GK.tersedia(e, {}, date(2026, 8, 14)))      # 45 hari
        t = {'2026/Q2': {'pub': '2026-07-29', 'jenis': 2}}          # selepas tutup -> esok
        self.assertFalse(GK.tersedia(e, t, date(2026, 7, 29)))
        self.assertTrue(GK.tersedia(e, t, date(2026, 7, 30)))
        self.assertFalse(GK.tersedia({'label': '2025/Q4', 'tamat': '2025-12-31'}, {}, date(2026, 2, 28)))

    def test_suku_berturut(self):
        k = syarikat(12)
        q = k['suku'][:5] + k['suku'][6:]
        self.assertEqual(len(GK.suku_berturut(q)), 6)


class UjiMetrik(unittest.TestCase):
    def test_satu_kali_teras(self):
        k = syarikat(12, lain={10: 200.0})
        e = k['suku'][10]
        self.assertTrue(GK.satu_kali(e))
        self.assertLess(GK.untung_teras(e), GK.untung_induk(e))
        m = GK.ttm(k['suku'], k['suku'])
        self.assertTrue(m['satu_kali'])
        self.assertAlmostEqual(m['ni'], m['ni_lapor'] - 200.0 * 0.79, places=6)

    def test_q4_ragu(self):
        k = syarikat(8)
        e = json.loads(json.dumps(k['suku'][7]))   # 2020/Q4
        e[P]['Research & Development'] = -50.0
        self.assertTrue(GK.q4_ragu(e, k['suku'][4:7]))
        self.assertFalse(GK.q4_ragu(k['suku'][7], k['suku'][4:7]))

    def test_gred_semakan(self):
        self.assertEqual(GK.gred_semakan({'a': True, 'b': True, 'c': True, 'd': True}), 'A')
        self.assertEqual(GK.gred_semakan({i: i < 5 for i in range(6)}), 'B')
        self.assertEqual(GK.gred_semakan({i: i < 3 for i in range(6)}), 'C')
        self.assertEqual(GK.gred_semakan({i: i < 2 for i in range(6)}), 'D')
        self.assertEqual(GK.gred_semakan({i: i < 1 for i in range(6)}), 'E')
        self.assertEqual(GK.gred_semakan({'a': True, 'b': None, 'c': None, 'd': True, 'e': True}), '–')   # < 4 dikira

    def test_histerisis(self):
        self.assertEqual(GK.histerisis(['B', 'B', 'A']), 'B')       # naik 1 huruf sekali: tangguh
        self.assertEqual(GK.histerisis(['B', 'A', 'A']), 'A')       # 2 tempoh berturut
        self.assertEqual(GK.histerisis(['A', 'A', 'C']), 'C')       # >= 2 huruf: terus
        self.assertEqual(GK.histerisis(['B', 'C', 'B']), 'B')
        self.assertEqual(GK.histerisis(['–', '–']), '–')

    def test_gabung_had_k(self):
        self.assertEqual(GK.gabung({'K': 'D', 'U': 'A', 'T': 'A', 'S': 'A'}), 'C')   # purata B, had K+1 = C
        self.assertEqual(GK.gabung({'K': 'A', 'U': 'B', 'T': 'B', 'S': 'C'}), 'B')
        self.assertEqual(GK.gabung({'K': '–', 'U': 'A', 'T': 'A', 'S': 'A'}), '–')
        self.assertEqual(GK.gabung({'K': 'A', 'U': '–', 'T': '–', 'S': 'A'}), '–')

    def test_jarak_mungkir(self):
        ix = pd.bdate_range('2025-01-01', periods=300)
        h = pd.Series(np.linspace(50, 60, 300), index=ix)
        b0 = {'hutang_pendek': 0.0, 'hutang_panjang': 0.0}
        self.assertEqual(GK.jarak_mungkir(h, 1e6, b0), math.inf)
        rng = np.random.default_rng(1)
        h2 = pd.Series(10 * np.exp(np.cumsum(rng.normal(-0.003, 0.05, 300))), index=ix)
        rendah = GK.jarak_mungkir(h2, 1e6, {'hutang_pendek': 3e7, 'hutang_panjang': 2e7})
        tinggi = GK.jarak_mungkir(h, 1e6, {'hutang_pendek': 1e6, 'hutang_panjang': 1e6})
        self.assertLess(rendah, 1)
        self.assertGreater(tinggi, 5)
        self.assertIsNone(GK.jarak_mungkir(h.iloc[:100], 1e6, b0))


class UjiKekukuhan(unittest.TestCase):
    def sub(self, k):
        q = GK.suku_berturut(k['suku'])
        return GK.sub_gred(q, k['suku'], GK.isi_tahunan(k['tahunan'], k['suku']), None, 'Technology', 'Software')

    def test_jalur_hutang(self):
        # hutang bersih 12% aset = 0.96 x hasil suku; EBITDA TTM ~ 1.2 x hasil suku -> ~0.8x -> A
        self.assertEqual(self.sub(syarikat())['k_asas']['hutang_ebitda'], 'A')
        # hutang 60% aset, tunai 10%: hutang bersih 4 x hasil suku / EBITDA ~1.2 -> ~3.3x -> C
        r = self.sub(syarikat(hutang_aset=0.60))
        self.assertEqual(r['k_asas']['hutang_ebitda'], 'C')

    def test_tunai_bersih(self):
        r = self.sub(syarikat(hutang_aset=0.05, tunai_aset=0.30))
        self.assertEqual(r['k_asas'], {'hutang_ebitda': 'A', 'ffo_hutang': 'A'})

    def test_altman_semakan_silang(self):
        # untung tertahan sangat negatif (belian balik) -> Z'' rendah tetapi K tidak dihadkan tanpa DD lemah
        k = syarikat()
        for e in k['suku']:
            e[K]['Retained Earnings'] = -e[K]['Total Assets'] * 2
        r = self.sub(k)
        self.assertIn('altman_z2<1.1', r['nota'])
        self.assertEqual(r['K'], 'A')

    def test_larian_tunai(self):
        r = self.sub(syarikat(muda=True, g=0.30, tunai_aset=0.30))
        self.assertIn(r['K'], ('D', 'E'))
        self.assertEqual(r['peringkat'], 'muda')


class UjiSyariah(unittest.TestCase):
    def b(self, hutang_bf, tunai=0.1):
        return {'aset': 100.0, 'hutang': 50.0, 'hutang_berfaedah': hutang_bf, 'tunai': tunai * 100}

    def test_pajakan_dikecualikan(self):
        s = GK.syariah(self.b(20.0), {'hasil': 100.0, 'pend_faedah': 1.0}, None, None)
        self.assertEqual(s['status'], 'lulus')
        self.assertEqual(s['jarak_pp']['hutang/aset'], 13.0)

    def test_satu_kaedah_gagal_sebahagian(self):
        s = GK.syariah(self.b(40.0), {'hasil': 100.0, 'pend_faedah': 1.0}, None, None)
        self.assertEqual(s['status'], 'gagal_sebahagian')

    def test_tunai_sahaja_sebahagian(self):
        s = GK.syariah(self.b(10.0, tunai=0.5), {'hasil': 100.0, 'pend_faedah': 1.0}, None, None)
        self.assertEqual(s['status'], 'gagal_sebahagian')

    def test_semua_kaedah_gagal(self):
        h = pd.Series([1.0] * 800, index=pd.bdate_range('2023-01-01', periods=800))
        s = GK.syariah(self.b(40.0), {'hasil': 100.0, 'pend_faedah': 1.0}, h, 50.0)   # mcap 50
        self.assertEqual(s['status'], 'gagal')

    def test_hampir_had(self):
        s = GK.syariah(self.b(32.0), {'hasil': 100.0, 'pend_faedah': 1.0}, None, None)
        self.assertEqual(s['status'], 'hampir_had')


class UjiHujungKeHujung(unittest.TestCase):
    def test_syarikat_sihat(self):
        r = GK.kira(syarikat(n=50, mula=2014), hari_ini=date(2026, 10, 18), sektor='Industrials', industri='Machinery')
        self.assertIn(r['gred'], ('A', 'B'))
        self.assertEqual(r['K'], 'A')
        self.assertEqual(r['syariah'], 'lulus')
        self.assertIn('keyakinan', r['ringkas'])

    def test_syarikat_lemah(self):
        k = syarikat(n=50, mula=2014, g=-0.10, margin_op=0.02, hutang_aset=0.70, tunai_aset=0.02, ocf_x=0.5)
        r = GK.kira(k, hari_ini=date(2026, 10, 18), sektor='Industrials', industri='Machinery')
        self.assertIn(r['gred'], ('D', 'E'))
        self.assertIn(r['K'], ('D', 'E'))

    def test_data_pendek_dan_bank(self):
        self.assertEqual(GK.kira(syarikat(n=6, mula=2025), hari_ini=date(2026, 10, 18))['gred'], '–')
        r = GK.kira(syarikat(n=50, mula=2014), hari_ini=date(2026, 10, 18), sektor='Financial Services', industri='Banks')
        self.assertEqual(r['gred'], '–')

    def test_point_in_time(self):
        k = syarikat(n=50, mula=2014)
        r = GK.kira(k, hari_ini=date(2026, 8, 13), sektor='Industrials', industri='Machinery')
        self.assertEqual(r['tempoh'], '2026/Q1')     # Q2 (tamat 30 Jun) belum tersedia sebelum 45 hari
        r = GK.kira(k, hari_ini=date(2026, 8, 14), sektor='Industrials', industri='Machinery')
        self.assertEqual(r['tempoh'], '2026/Q2')

    def test_beneish_stabil(self):
        k = syarikat(n=12)
        q = k['suku']
        m, m4 = GK.ttm(q, q), GK.ttm(q[:-4], q)
        bm = GK.beneish(m, m4, GK.imbangan(q[-1]), GK.imbangan(q[-5]))
        self.assertLess(bm, -1.78)

    def test_median_industri(self):
        with tempfile.TemporaryDirectory() as d:
            peta = {}
            for i in range(6):
                k = syarikat(n=12, mula=2023, margin_op=0.10 + 0.02 * i)
                json.dump(k, open(os.path.join(d, f'S{i}.json'), 'w'))
                peta[f'S{i}'] = 'Machinery'
            med = GK.median_industri(d, peta, date(2026, 10, 18))
            self.assertAlmostEqual(med['Machinery']['margin_op'], 0.16, places=6)
            peta2 = {f'S{i}': 'Machinery' for i in range(4)}
            self.assertIsNone(GK.median_industri(d, peta2, date(2026, 10, 18))['Machinery']['margin_op'])


if __name__ == '__main__':
    unittest.main()
