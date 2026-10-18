# Ujian standard/gred_kira_semula.py (kira semula gred skema semasa pada tarikh rujukan asal)
import csv, json, os, sys, tempfile, unittest
from datetime import date
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import gred_kira_semula as KS  # noqa: E402


class UjiKiraSemula(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        p = lambda n: os.path.join(self.d, n)
        with open(p('eps.csv'), 'w') as f:
            f.write('ticker,tarikh,masa,eps_anggaran,eps_sebenar,kejutan_pct\n'
                    'AAA,2026-07-20,16:05,1,1.2,20\nAAA,2026-10-12,16:05,1,1.3,30\nBBB,2026-08-01,07:00,1,1,0\n')
        json.dump({'saham': {'BBB': {'lalu': '2026-10-13', 'lalu_masa': 'time-pre-market'},
                             'CCC': {'lalu': '2026-10-01', 'lalu_masa': 'time-not-supplied'}}}, open(p('nas.json'), 'w'))
        with open(p('kum.csv'), 'w') as f:
            f.write('tarikh,jenis,nama,sektor,n,skor,gred\n2026-10-15,Industri,Semiconductors,Technology,9,91.2,A\n'
                    '2026-10-15,Sektor,Technology,Technology,50,55.0,C\n2026-10-15,Industri,Kecil,X,2,0,–\n')

    def test_earnings_lalu(self):
        e = KS.peta_earnings_lalu(os.path.join(self.d, 'eps.csv'), os.path.join(self.d, 'nas.json'))
        self.assertEqual(e['AAA'], [('2026-07-20', True), ('2026-10-12', True)])
        self.assertEqual(e['BBB'], [('2026-08-01', False), ('2026-10-13', False)])
        self.assertEqual(e['CCC'], [('2026-10-01', None)])
        self.assertEqual(KS.lalu_sebelum(e['AAA'], date(2026, 10, 12)), (date(2026, 7, 20), True))   # hari sama tidak dikira
        self.assertEqual(KS.lalu_sebelum(e['AAA'], date(2026, 10, 13)), (date(2026, 10, 12), True))
        self.assertEqual(KS.lalu_sebelum(None, date(2026, 10, 13)), (None, None))

    def test_kumpulan_sejarah(self):
        k = KS.peta_kumpulan_sejarah(os.path.join(self.d, 'kum.csv'))
        self.assertEqual(k['2026-10-15'][1], {'Semiconductors': (91.2, 'A')})
        self.assertEqual(k['2026-10-15'][0], {'Technology': (55.0, 'C')})
        self.assertEqual(KS.peta_kumpulan_sejarah(os.path.join(self.d, 'tiada.csv')), {})

    def test_kira_baris(self):
        idx = pd.bdate_range('2025-09-01', '2026-10-16')
        c = pd.DataFrame({'AAA': np.linspace(10, 12, len(idx))}, index=idx)
        c.loc['2026-10-13':, 'AAA'] *= 1.3                      # reaksi earnings selepas tutup 12 Okt: +30%
        v = pd.DataFrame({'AAA': 1e6}, index=idx); v.loc['2026-10-13', 'AAA'] = 5e6
        spy = pd.Series(500.0, index=idx)
        ctx = dict(c=c, v=v, spy=spy, rs=None, cache={}, tarikh='2026-10-18',
                   kum=KS.peta_kumpulan_sejarah(os.path.join(self.d, 'kum.csv')),
                   ear=KS.peta_earnings_lalu(os.path.join(self.d, 'eps.csv'), None),
                   pind={'AAA': 'Semiconductors'}, pem={}, jenis={'M01': 'momentum', 'M02': 'pantulan'})
        r = {'saham': 'AAA', 'kaedah': 'M01', 'hari_ke_earnings': '', 'gred_qr': 'A', 'sumber_earnings': 'Nasdaq',
             'gred_pada': '2026-10-16; lama'}
        from collections import Counter
        kira = Counter()
        KS.kira_baris(r, pd.Timestamp('2026-10-15'), date(2026, 10, 16), ctx, kira)
        self.assertEqual((r['gred_industri'], r['gred_sektor']), ('A', 'C'))
        self.assertEqual(r['gred_pemangkin'], 'A')                 # +30% lawan pasaran, umur 2 hari
        self.assertEqual(r['gred_qr'], 'A')                        # QR lalu 4 hari dagangan sebelum 16 Okt: tiada had
        self.assertEqual(r['gred_keseluruhan'], 'A')
        self.assertEqual(r['gred_pada'], '2026-10-16; lama; skema semasa 2026-10-18 (S/I v2, rujukan 2026-10-15)')
        r2 = dict(r, kaedah='M02')
        KS.kira_baris(r2, pd.Timestamp('2026-10-15'), date(2026, 10, 16), ctx, kira)
        self.assertEqual(r2['gred_pada'].count('skema semasa'), 1)  # catatan tidak berganda
        KS.kira_baris(r, pd.Timestamp('2026-10-12'), date(2026, 10, 13), ctx, kira)
        self.assertEqual(r['gred_qr'], 'C')                        # QR lalu 1 hari dagangan: sekurang-kurangnya C
        self.assertEqual(r['sumber_earnings'], 'Nasdaq; QR lalu 1 hari')
        self.assertEqual(r['gred_pemangkin'], 'D')                 # harga <= 12 Okt: reaksi belum berlaku
        KS.kira_baris(r, pd.Timestamp('2026-10-13'), date(2026, 10, 14), ctx, kira)
        self.assertEqual((r['gred_qr'], r['sumber_earnings']), ('B', 'Nasdaq; QR lalu 2 hari'))   # tidak berganda
        self.assertEqual(kira['sektor/industri tiada data sesi itu'], 2)


if __name__ == '__main__':
    unittest.main()
