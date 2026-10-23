# Ujian sambungan gred kewangan v7.1 (standard/gred_kewangan.py, standard/gred_kewangan_isi.py; spec §11–13):
# v7 dahulu, separuh tahun, tahunan, sejarah pendek, aliran tunai ganti, peralihan tahun kewangan, asas <= 0,
# median sektor/semua, model bank / insurans / REIT, isi semula baris '–'.
import os, sys, csv, json, tempfile, unittest
from datetime import date

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.dirname(__file__))
import gred_kewangan as GK  # noqa: E402
from test_gred_kewangan import syarikat  # noqa: E402

P, K, T = GK.P, GK.K, GK.T


def pelapor_separuh(tahun=8, mula=2018, g=0.10):
    """Pelapor separuh tahun sintetik (tahun kewangan Jun): H1 = Q6 kumulatif (Jul–Dis), tahunan (Jun); suku Q2/Q4
    hanya kunci kira-kira (seperti BHP dalam Moomoo)."""
    sep, tah, suku = [], [], []
    for i in range(tahun):
        y = mula + i
        r1, r2 = 100.0 * (1 + g) ** i, 110.0 * (1 + g) ** i
        aset = 10 * (r1 + r2)

        def p(r):
            op = r * 0.30
            return {'Total Operating Revenue': r, 'Operating Profit': op, 'Non-Operating Interest Expense': r * 0.01,
                    'Pretax Profit': op - r * 0.01, 'Tax': (op - r * 0.01) * 0.3, 'Net Profit': (op - r * 0.01) * 0.7,
                    'Net Income to Parent Company': (op - r * 0.01) * 0.7, 'Diluted EPS': (op - r * 0.01) * 0.007}

        def t(r):
            ni = (r * 0.29) * 0.7
            return {'Operating Cash Flow': ni * 1.3, 'Change in Working Capital': 0.0,
                    'Depreciation & Depletion & Amortization': r * 0.05, 'Free Cash Flow': ni * 0.8,
                    'Net Common Stock Issuance': 0.0, 'Net Income from Continuing Operations': ni}
        kk = {'Total Assets': aset, 'Total Current Assets': aset * 0.3, 'Total Current Liabilities': aset * 0.1,
              'Total Non-Current Liabilities': aset * 0.2, 'Total Liabilities': aset * 0.3,
              'Cash and Cash Equivalents & Short-Term Investments': aset * 0.05,
              'Long Term Debt and Capital Lease Obligation': aset * 0.15, 'Total Equity': aset * 0.7,
              "Stockholders' Equity": aset * 0.7, 'Retained Earnings': aset * 0.4}
        h1 = f'{y - 1}-12-31'; fy = f'{y}-06-30'
        sep.append({'tamat': h1, 'label': f'{y}/Q6', P: p(r1), K: {}, T: t(r1)})
        tah.append({'tamat': fy, 'label': f'{y}/FY', P: {n: p(r1)[n] + p(r2)[n] for n in p(r1)}, K: dict(kk),
                    T: {n: t(r1)[n] + t(r2)[n] for n in t(r1)}})
        suku.append({'tamat': h1, 'label': f'{y}/Q2', P: {}, K: dict(kk), T: {}})
        suku.append({'tamat': fy, 'label': f'{y}/Q4', P: {}, K: dict(kk), T: {}})
    return {'ticker': 'SEP', 'suku': suku, 'tahunan': tah, 'separuh': sep, 'terbit': {}, 'saham_terbit': None}


def bank(n=24, mula=2020):
    suku = []
    for i in range(n):
        th, q = mula + i // 4, i % 4 + 1
        f = 1.02 ** i
        aset, pinj, dep = 1000.0 * f, 600.0 * f, 750.0 * f
        nii, non, nie, prov = 8.0 * f, 4.0 * f, 6.6 * f, -0.9 * f
        pt = nii + non - nie + prov
        suku.append({'tamat': (pd.Timestamp(year=th, month=3 * q, day=1) + pd.offsets.MonthEnd(0)).date().isoformat(),
                     'label': f'{th}/Q{q}',
                     P: {'Total Operating Revenue': nii + non, 'Net Interest Income': nii, '-Interest Income': nii * 1.8,
                         '-Interest Expense': nii * 0.8, 'Non-Interest Income': non, 'Non-Interest Expense': nie,
                         'Credit Losses Provision': prov, 'Pretax Profit': pt, 'Tax': pt * 0.2, 'Net Profit': pt * 0.8,
                         'Net Income to Parent Company': pt * 0.8, 'Diluted EPS': pt * 0.008},
                     K: {'Total Assets': aset, 'Net Loan': pinj, 'Total Deposits': dep, 'Total Liabilities': aset * 0.9,
                         'Total Equity': aset * 0.1, "Stockholders' Equity": aset * 0.1,
                         'Goodwill and Other Intangible Assets': aset * 0.01, '-Preferred Stock': aset * 0.005,
                         'Cash, Cash Equivalents & Federal Funds Sold': aset * 0.1,
                         '-Current Debt': aset * 0.02, '-Long Term Debt': aset * 0.1,
                         'Short-Term Debt and Capital Lease Obligation': aset * 0.02,
                         'Long Term Debt and Capital Lease Obligation': aset * 0.1},
                     T: {'Net Common Stock Issuance': -1.0}})
    return {'ticker': 'BNK', 'suku': suku, 'tahunan': [], 'terbit': {}, 'saham_terbit': None, 'struktur': 'BANK_MSTAR'}


class UjiV7Dahulu(unittest.TestCase):
    def test_v7_kekal_apabila_bergred(self):
        r = GK.kira(syarikat(n=50, mula=2014), hari_ini=date(2026, 10, 18), sektor='Industrials', industri='Machinery')
        self.assertIn(r['gred'], ('A', 'B'))
        self.assertEqual(r['butiran']['versi'], '7')            # laluan v7 tepat
        self.assertNotIn('sebab_v7', r['butiran'])
        self.assertNotIn('semakan_ganti', r['butiran'])

    def test_lanjut_hanya_jika_v7_tiada(self):
        k = syarikat(n=50, mula=2014)
        v7 = GK.kira_teras(k, None, date(2026, 10, 18), None, 'Industrials', 'Machinery', 'standard', False)
        r = GK.kira(k, hari_ini=date(2026, 10, 18), sektor='Industrials', industri='Machinery')
        self.assertEqual((r['gred'], r['K'], r['U'], r['T'], r['S']), (v7['gred'], v7['K'], v7['U'], v7['T'], v7['S']))


class UjiTempoh(unittest.TestCase):
    def test_separuh_h2_tahunan_tolak_h1(self):
        k = pelapor_separuh()
        sp = GK.tempoh_separuh(k)
        self.assertEqual([e['label'] for e in sp[:2]], ['2018/Q2', '2018/Q4'])
        h1, h2 = sp[0], sp[1]
        fy = k['tahunan'][0]
        self.assertAlmostEqual(h1[P]['Total Operating Revenue'] + h2[P]['Total Operating Revenue'],
                               fy[P]['Total Operating Revenue'])
        self.assertEqual(h2[K]['Total Assets'], fy[K]['Total Assets'])     # kunci kira-kira suku Q4 sepadan

    def test_kira_separuh(self):
        k = pelapor_separuh()
        self.assertEqual(GK.kira_teras(k, None, date(2025, 10, 15), None, 'Basic Materials', 'Copper', 'standard',
                                       False)['gred'], '–')                # v7: 1 suku berturut
        r = GK.kira(k, hari_ini=date(2025, 10, 15), sektor='Basic Materials', industri='Copper')
        self.assertNotEqual(r['gred'], '–')
        self.assertEqual(r['tempoh_data'], 'separuh')
        self.assertEqual(r['tempoh'], '2025/Q4')
        self.assertIn('data separuh tahun', r['ringkas'])
        self.assertIn('data_separuh_tahun', r['butiran']['nota'])
        self.assertNotEqual(r['keyakinan'], 'tinggi')

    def test_separuh_point_in_time(self):
        k = pelapor_separuh()
        # H2 2025 (= tahunan tamat 30 Jun 2025) tanpa rekod siaran: + 60 hari -> 29 Ogo 2025
        self.assertEqual(GK.kira(k, hari_ini=date(2025, 8, 28), sektor='Basic Materials', industri='Copper')['tempoh'],
                         '2025/Q2')
        self.assertEqual(GK.kira(k, hari_ini=date(2025, 8, 29), sektor='Basic Materials', industri='Copper')['tempoh'],
                         '2025/Q4')
        # H1 2025 (tamat 31 Dis 2024): + 90 hari -> 31 Mac 2025
        self.assertEqual(GK.kira(k, hari_ini=date(2025, 3, 30), sektor='Basic Materials', industri='Copper')['tempoh'],
                         '2024/Q4')

    def test_tahunan_sahaja(self):
        k = pelapor_separuh()
        k.pop('separuh')
        r = GK.kira(k, hari_ini=date(2025, 10, 15), sektor='Basic Materials', industri='Copper')
        self.assertEqual(r['tempoh_data'], 'tahunan')
        self.assertIn('data tahun', r['ringkas'])

    def test_sejarah_pendek(self):
        k = syarikat(n=7, mula=2025)        # 2025/Q1 – 2026/Q3
        r = GK.kira(k, hari_ini=date(2026, 12, 1), sektor='Industrials', industri='Machinery')
        self.assertEqual(r['butiran']['sebab_v7'], '7 suku berturut (< 8)')
        self.assertTrue(r['butiran'].get('sejarah_pendek'))
        self.assertNotEqual(r['gred'], '–')
        self.assertEqual(r['keyakinan'], 'rendah')
        self.assertIn('sejarah pendek', r['ringkas'])
        self.assertEqual(GK.kira(syarikat(n=3, mula=2026), hari_ini=date(2026, 12, 1))['gred'], '–')

    def test_peralihan_tahun_kewangan(self):
        k = syarikat(n=16, mula=2022)
        q = k['suku']
        # suku ke-9 dan seterusnya dianjak 61 hari (jurang 152 hari) dengan label melangkau (2023/Q4 -> 2024/Q2)
        anjak = lambda e: (pd.Timestamp(e['tamat']) + pd.Timedelta(days=61)).date().isoformat()
        q2 = q[:8] + [dict(q[8], tamat=anjak(q[8]), label='2024/Q2')] + [dict(e, tamat=anjak(e)) for e in q[9:]]
        self.assertEqual(len(GK.suku_berturut(q2)), 8)                     # v7: rantaian putus
        self.assertEqual(len(GK.suku_berturut(q2, 4, True)), 16)           # v7.1: satu peralihan dibenarkan
        q3 = q[:8] + q[9:]                                                 # jurang 182 hari: suku hilang
        self.assertEqual(len(GK.suku_berturut(q3, 4, True)), 7)
        q4 = q[:8] + [dict(q[8], tamat=anjak(q[8]))] + [dict(e, tamat=anjak(e)) for e in q[9:]]
        self.assertEqual(len(GK.suku_berturut(q4, 4, True)), 8)            # label bersambung: bukan peralihan


class UjiGanti(unittest.TestCase):
    def test_aliran_tunai_lewat(self):
        k = syarikat(n=28, mula=2019)
        k['suku'][-1][T] = {}                     # 10-Q/10-K suku terakhir belum difailkan
        q = k['suku']
        self.assertIsNone(GK.ttm(q, q)['ocf'])    # v7
        m = GK.ttm(q, q, 4, None, True)
        self.assertEqual(m['tunai_ganti'], 'lewat_1_tempoh')
        self.assertAlmostEqual(m['ocf'], sum(e[T]['Operating Cash Flow'] for e in q[-5:-1]))
        r = GK.kira(k, hari_ini=date(2026, 3, 1), sektor='Industrials', industri='Machinery')
        self.assertIn('aliran_tunai_lewat_1_tempoh', r['butiran']['nota'])

    def test_aliran_tunai_tahunan(self):
        k = syarikat(n=28, mula=2019)
        for e in k['suku'][-3:]:
            e[T] = {}
        q = k['suku']
        m = GK.ttm(q, q, 4, k['tahunan'], True)
        self.assertEqual(m['tunai_ganti'], 'tahunan')
        self.assertAlmostEqual(m['ocf'], k['tahunan'][-1][T]['Operating Cash Flow'])

    def test_asas_negatif(self):
        self.assertTrue(GK.lulus_tumbuh(0.5, -0.2, 0.18))      # pusing untung
        self.assertFalse(GK.lulus_tumbuh(-0.1, -0.2, 0.18))    # masih rugi
        self.assertTrue(GK.lulus_tumbuh(1.2, 1.0, 0.18))
        self.assertFalse(GK.lulus_tumbuh(1.1, 1.0, 0.18))
        self.assertIsNone(GK.lulus_tumbuh(None, 1.0, 0.18))

    def test_tahunan_dijumlah_suku(self):
        k = syarikat(n=12, mula=2023)
        k['tahunan'][-1][P] = {}; k['tahunan'][-1][T] = {}
        v7 = GK.isi_tahunan(k['tahunan'], k['suku'])
        self.assertEqual(v7[-1][P], {})
        t = GK.isi_tahunan(k['tahunan'], k['suku'], True)
        self.assertAlmostEqual(t[-1][P]['Total Operating Revenue'],
                               sum(e[P]['Total Operating Revenue'] for e in k['suku'][-4:]))
        self.assertTrue(t[-1]['dijumlah_suku'])

    def test_median_sandaran(self):
        with tempfile.TemporaryDirectory() as d:
            peta = {}
            for i in range(6):
                json.dump(syarikat(n=12, mula=2023, margin_op=0.10 + 0.02 * i), open(os.path.join(d, f'S{i}.json'), 'w'))
                peta[f'S{i}'] = 'Specialty Industrial Machinery' if i < 3 else 'Tools & Accessories'
            med = GK.median_industri(d, peta, date(2026, 10, 18))
            m = med['Specialty Industrial Machinery']
            self.assertIsNone(m['margin_op'])                       # < 5 rakan industri
            self.assertAlmostEqual(m['sektor']['margin_op'], 0.16, places=6)   # Industrials: 6 rakan
            g = set()
            self.assertIsNone(GK.median_pakai(m, 'margin_op'))      # v7
            self.assertAlmostEqual(GK.median_pakai(m, 'margin_op', g, 'U:x', True), 0.16, places=6)
            self.assertEqual(g, {'U:x'})


class UjiModelKewangan(unittest.TestCase):
    def test_jenis_model(self):
        biasa = syarikat(n=12)
        self.assertEqual(GK.jenis_model(biasa, 'Financial Services', 'Capital Markets'), 'standard')
        self.assertEqual(GK.jenis_model(biasa, 'Industrials', 'Machinery'), 'standard')
        self.assertEqual(GK.jenis_model(bank(), 'Financial Services', 'Banks - Regional'), 'bank')
        self.assertEqual(GK.jenis_model({'struktur': 'INSURANCE_MSTAR', 'suku': []}, '', ''), 'insurans')
        self.assertEqual(GK.jenis_model(biasa, 'Financial Services', 'Insurance Brokers'), 'standard')
        self.assertEqual(GK.jenis_model(biasa, 'Real Estate', 'REIT - Retail'), 'reit')
        kosong = {'suku': [{'label': '2026/Q2', 'tamat': '2026-06-30', P: {'Total Revenue as Reported': 1.0}, K: {}, T: {}}]}
        self.assertEqual(GK.jenis_model(kosong, 'Financial Services', 'Credit Services'), 'tidak_dikenali')

    def test_bank(self):
        r = GK.kira(bank(), hari_ini=date(2026, 3, 1), sektor='Financial Services', industri='Banks - Regional')
        self.assertEqual(r['model'], 'bank')
        self.assertEqual(r['peringkat'], 'bank')
        b = r['butiran']
        # TCE/aset = (10% − 0.5% − 1%) / 99% = 8.6% -> B; pinjaman/deposit 80% -> A
        self.assertEqual(b['k_asas'], {'tce_aset': 'B', 'pinjaman_deposit': 'A'})
        self.assertEqual(r['K'], 'B')
        self.assertAlmostEqual(b['nisbah']['kecekapan'], 0.55, places=4)
        self.assertIn(r['U'], ('A', 'B', 'C', 'D', 'E'))
        self.assertIn(r['T'], ('A', 'B', 'C', 'D', 'E'))
        # pendapatan faedah = 1.8 x NII > 5% hasil -> Syariah tidak lulus
        self.assertIn(r['syariah'], ('gagal', 'gagal_sebahagian'))

    def test_insurans(self):
        k = syarikat(n=24, mula=2020)
        for e in k['suku']:
            r_ = e[P]['Total Operating Revenue']
            e[P].update({'Total Premiums Earned': r_ * 0.9, 'Loss Adjustment Expense': r_ * 0.6,
                         'Policy Acquisition Expense': r_ * 0.1, 'Underwriting Expenses': r_ * 0.1,
                         'Net Investment Income': r_ * 0.08})
        k['struktur'] = 'INSURANCE_MSTAR'
        r = GK.kira(k, hari_ini=date(2026, 3, 1), sektor='Financial Services', industri='Insurance - Property & Casualty')
        self.assertEqual(r['model'], 'insurans')
        self.assertAlmostEqual(r['butiran']['nisbah']['nisbah_gabungan'], 0.8 / 0.9, places=4)
        self.assertIn(r['K'], ('A', 'B', 'C', 'D', 'E'))

    def test_reit(self):
        k = syarikat(n=24, mula=2020, hutang_aset=0.40, tunai_aset=0.02)
        for e in k['suku']:
            e[T]['Cash Dividends Paid'] = -e[P]['Net Income to Parent Company'] * 0.8
        r = GK.kira(k, hari_ini=date(2026, 3, 1), sektor='Real Estate', industri='REIT - Industrial')
        self.assertEqual(r['model'], 'reit')
        self.assertEqual(r['peringkat'], 'REIT')
        self.assertEqual(r['butiran']['k_asas']['hutang_aset'], 'B')       # 40% -> B (<= 45%)
        ffo = sum(GK.ffo_e(e) for e in k['suku'][-4:])
        self.assertAlmostEqual(r['butiran']['nisbah']['ffo'], round(ffo, 4), places=3)


class UjiSimpan(unittest.TestCase):
    def test_label_sama_tarikh_berbeza(self):
        a = [{'tamat': '2025-07-31', 'label': '2025/Q4', 'medan': {'Total Operating Revenue': 1}},
             {'tamat': '2025-12-31', 'label': '2025/Q4', 'medan': {'Total Operating Revenue': 2}}]
        g = GK.gabung_tempoh([(P, a)])
        self.assertEqual([(e['tamat'], e[P]['Total Operating Revenue']) for e in g],
                         [('2025-07-31', 1), ('2025-12-31', 2)])
        g2 = GK.gabung_lama(g, GK.gabung_tempoh([(K, [{'tamat': '2025-12-31', 'label': '2025/Q4',
                                                        'medan': {'Total Assets': 9}}])]))
        self.assertEqual(len(g2), 2)
        self.assertEqual(g2[1][K]['Total Assets'], 9)

    def test_simpan_separuh_dan_struktur(self):
        with tempfile.TemporaryDirectory() as d:
            m, out = os.path.join(d, 'm'), os.path.join(d, 'k')
            os.makedirs(m)
            rep = lambda label, ms, ft, st='NORMAL_MSTAR': {
                'date_time': ms, 'period_text': label, 'financial_type': ft, 'structure_name': st,
                'item_list': [{'display_name': 'Total Operating Revenue', 'data': 5.0}]}
            json.dump({'data': {'report_list': [rep('2026/Q6', 1767110400000, 5)]}}, open(os.path.join(m, 'ABC_1_6_cp1.json'), 'w'))
            json.dump({'data': {'report_list': [rep('2026/Q2', 1782748800000, 2, 'BANK_MSTAR')]}},
                      open(os.path.join(m, 'ABC_1_9_p1.json'), 'w'))
            GK.simpan(m, out, '2026-10-23')
            k = json.load(open(os.path.join(out, 'ABC.json')))
            self.assertEqual([e['label'] for e in k['separuh']], ['2026/Q6'])
            self.assertEqual(k['struktur'], 'BANK_MSTAR')


class UjiIsiSemula(unittest.TestCase):
    def test_isi_baris_tiada_sahaja(self):
        import gred_kewangan_isi as ISI
        with tempfile.TemporaryDirectory() as d:
            pt, kw, hg = (os.path.join(d, x) for x in ('pt', 'kw', 'hg'))
            for x in (pt, kw, hg):
                os.makedirs(x)
            json.dump(syarikat(n=50, mula=2014), open(os.path.join(kw, 'AAA.json'), 'w'))
            json.dump(pelapor_separuh(tahun=9, mula=2018), open(os.path.join(kw, 'SEP.json'), 'w'))
            ix = pd.bdate_range('2025-06-02', '2026-10-16')
            with open(os.path.join(hg, 'harga_A.csv'), 'w', newline='') as f:
                w = csv.writer(f); w.writerow(['ticker', 'date', 'close', 'volume'])
                for t in ('AAA', 'SEP', 'BBB'):
                    for i, x in enumerate(ix):
                        w.writerow([t, x.strftime('%Y-%m-%d'), 50 + i * 0.01, 1000])
            lajur = ['tarikh_beli', 'saham', 'tarikh_isyarat', 'tidak_dibeli', 'gred_pada', 'gred_kewangan',
                     'kewangan_ringkas', 'kewangan_tempoh', 'kewangan_butiran']
            rows = [{'tarikh_beli': '2026-10-08', 'saham': 'AAA', 'gred_pada': 'isi semula 2026-10-17 (RS & QR pada 2026-10-07)',
                     'gred_kewangan': '–', 'kewangan_ringkas': '– (tiada data kewangan)'},
                    {'tarikh_beli': '2026-10-08', 'saham': 'SEP', 'gred_pada': '', 'gred_kewangan': '',
                     'kewangan_ringkas': ''},
                    {'tarikh_beli': '2026-10-08', 'saham': 'AAA', 'gred_pada': '2026-10-07', 'gred_kewangan': 'B',
                     'kewangan_ringkas': 'B (asal)'},
                    {'tarikh_beli': '2026-10-08', 'saham': 'BBB', 'tidak_dibeli': 'True', 'gred_kewangan': '–'},
                    {'tarikh_beli': '2026-10-08', 'saham': 'BBB', 'gred_kewangan': '–'}]
            for nm in ('moomoo.csv', 'claude.csv'):
                with open(os.path.join(pt, nm), 'w', newline='') as f:
                    w = csv.DictWriter(f, fieldnames=lajur); w.writeheader(); w.writerows(rows)
            asal = open(os.path.join(pt, 'moomoo.csv')).read()
            ISI.main(['--harga', hg, '--folder', pt, '--kewangan', kw, '--tarikh', '2026-10-23', '--uji'])
            self.assertEqual(open(os.path.join(pt, 'moomoo.csv')).read(), asal)        # --uji: tiada tulis
            ISI.main(['--harga', hg, '--folder', pt, '--kewangan', kw, '--tarikh', '2026-10-23'])
            mm = list(csv.DictReader(open(os.path.join(pt, 'moomoo.csv'))))
            self.assertIn(mm[0]['gred_kewangan'], ('A', 'B', 'C', 'D', 'E'))
            self.assertIn('kewangan isi semula 23 Okt (v7.1, penyata <= 2026-10-07)', mm[0]['gred_pada'])
            self.assertEqual(mm[0]['kewangan_butiran'], '')                           # moomoo: tiada butiran
            self.assertIn('data separuh tahun', mm[1]['kewangan_ringkas'])
            self.assertEqual((mm[2]['gred_kewangan'], mm[2]['kewangan_ringkas']), ('B', 'B (asal)'))   # tidak disentuh
            self.assertEqual(mm[3]['gred_kewangan'], '–')                              # tidak_dibeli: diabaikan
            self.assertEqual(mm[3]['gred_pada'], '')
            self.assertEqual(mm[4]['kewangan_ringkas'], '– (tiada data kewangan)')


if __name__ == '__main__':
    unittest.main()
