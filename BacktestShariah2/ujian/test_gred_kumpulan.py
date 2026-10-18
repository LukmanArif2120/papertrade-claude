# Ujian standard/gred_kumpulan.py dan laluan v2 gred.py tambah (--kumpulan)
import csv, os, sys, tempfile, unittest
from datetime import date
from types import SimpleNamespace
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import gred_kumpulan as K  # noqa: E402
import gred as G  # noqa: E402


def pasaran(n=330):
    """Tiga industri (4 saham setiap satu): Kuat naik, Rata, Lemah turun; SPY rata."""
    t = pd.bdate_range('2025-01-01', periods=n)
    x = np.arange(n)
    harga = {}
    for i in range(4):
        harga[f'K{i}'] = 20 * (1.004 + 0.0002 * i) ** x
        harga[f'R{i}'] = 20 * (1.0003 + 0.00005 * i) ** x + 0.2 * np.sin(x / 7 + i)
        harga[f'L{i}'] = 60 - (0.1 + 0.005 * i) * x
    C = pd.DataFrame(harga, index=t)
    peta = pd.DataFrame({'industri': ['Semiconductors'] * 4 + ['Banks - Regional'] * 4 + ['Oil & Gas E&P'] * 4},
                        index=[f'K{i}' for i in range(4)] + [f'R{i}' for i in range(4)] + [f'L{i}' for i in range(4)])
    peta['sektor'] = peta.industri.map(K.SEKTOR_INDUSTRI)
    spy = pd.Series(400.0, index=t)
    return C, peta, spy


class UjiGredKumpulan(unittest.TestCase):
    def test_sempadan(self):
        self.assertEqual([K.gred(x) for x in [95, 80.1, 80, 61, 41, 21, 20, 0]], list('AABBCDEE'))
        self.assertEqual(K.gred(np.nan), '–')

    def test_susunan_industri_dan_komponen(self):
        C, peta, spy = pasaran()
        S = K.siri(C, peta, spy)
        sk = S['Industri']['skor'].iloc[-1]
        self.assertGreater(sk['Semiconductors'], sk['Banks - Regional'])
        self.assertGreater(sk['Banks - Regional'], sk['Oil & Gas E&P'])
        for k in ['w1', 'w3']:
            self.assertEqual(S['Industri'][k].iloc[-1]['Semiconductors'], 1.0)
            self.assertEqual(S['Industri'][k].iloc[-1]['Oil & Gas E&P'], 0.0)
        a = S['Sektor']['a200'].iloc[-1]
        self.assertEqual(a['Technology'], 1.0); self.assertEqual(a['Energy'], 0.0)

    def test_tiada_skor_sebelum_cukup_sejarah(self):
        C, peta, spy = pasaran(200)          # < 252 bar: Mansfield RS belum wujud
        self.assertTrue(K.siri(C, peta, spy)['Industri']['skor'].isna().all().all())

    def test_harga_bawah_5_tidak_layak(self):
        C, peta, spy = pasaran()
        C[[f'L{i}' for i in range(4)]] = 3.0      # semua saham Lemah < USD5 -> industri itu tiada skor
        S = K.siri(C, peta, spy)
        self.assertTrue(np.isnan(S['Industri']['skor'].iloc[-1].get('Oil & Gas E&P', np.nan)))

    def test_snapshot(self):
        C, peta, spy = pasaran()
        snap = K.snapshot(K.siri(C, peta, spy), peta, '2026-10-19 12:00 MYT')
        self.assertEqual(list(snap.columns), K.LAJUR)
        ind = snap[snap.jenis == 'Industri'].set_index('nama')
        self.assertEqual(ind.loc['Semiconductors', 'gred'], 'A')
        self.assertEqual(ind.loc['Semiconductors', 'sektor'], 'Technology')
        self.assertIn(ind.loc['Oil & Gas E&P', 'gred'], 'DE')     # 3 industri: pangkat terendah = 33.3


class UjiTambahV2(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        t = pd.bdate_range('2025-06-02', periods=260)
        rows = []
        for tk, k in [('AAA', 1.002), ('BBB', 0.999)]:
            for i, dt in enumerate(t):
                rows.append(dict(ticker=tk, date=dt.strftime('%Y%m%d'), open=10, high=10, low=10, close=10 * k ** i,
                                 volume=1000))
        pd.DataFrame(rows).to_csv(os.path.join(self.d, 'harga_A.csv'), index=False)
        with open(os.path.join(self.d, 'peta.csv'), 'w') as f:
            f.write('ticker,industri,plate_code\nAAA,Semiconductors,X\nBBB,Oil & Gas E&P,Y\n')
        self.kum = os.path.join(self.d, 'gred_kumpulan.csv')
        with open(self.kum, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=K.LAJUR); w.writeheader()
            for j, nm, sk in [('Industri', 'Semiconductors', 90.0), ('Industri', 'Oil & Gas E&P', 10.0),
                              ('Sektor', 'Technology', 70.0), ('Sektor', 'Energy', 15.0)]:
                w.writerow(dict(tarikh='2026-10-16', jenis=j, nama=nm, sektor='', n=10, skor=sk, gred=K.gred(sk)))
        self.sb = os.path.join(self.d, 'senarai_beli.csv')
        with open(self.sb, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['saham', 'kaedah', 'sektor', 'industri']); w.writeheader()
            w.writerow(dict(saham='AAA', kaedah='M05', sektor='Tech', industri='x'))
            w.writerow(dict(saham='BBB', kaedah='M01', sektor='Energy', industri='y'))   # M01 = pantulan

    def jalan(self, tarikh='2026-10-19'):
        a = SimpleNamespace(csv=self.sb, harga=self.d, kumpulan=self.kum, sektor=None, pasaran=None,
                            peta=os.path.join(self.d, 'peta.csv'), acara=None, nasdaq=None, pemangkin=None, tarikh=tarikh)
        G.tambah(a)
        return {r['saham']: r for r in csv.DictReader(open(self.sb, newline=''))}

    def test_gred_daripada_fail_kumpulan(self):
        r = self.jalan()
        self.assertEqual((r['AAA']['gred_industri'], r['AAA']['skor_industri']), ('A', '90.0'))
        self.assertEqual((r['AAA']['gred_sektor'], r['AAA']['sektor_us']), ('B', 'Technology'))
        self.assertEqual(r['BBB']['gred_industri'], 'E')

    def test_keseluruhan_v2(self):
        r = self.jalan()
        # momentum: industri dikira; sektor dan RS tidak (RS dibuang sejak 18 Okt 2026)
        self.assertEqual(r['AAA']['gred_keseluruhan'],
                         G.gred_keseluruhan(['A', r['AAA']['gred_pemangkin'], r['AAA']['gred_qr']]))
        # pantulan (M01): industri E tidak dikira
        self.assertEqual(r['BBB']['gred_keseluruhan'],
                         G.gred_keseluruhan([r['BBB']['gred_pemangkin'], r['BBB']['gred_qr']]))

    def test_fail_basi(self):
        r = self.jalan('2026-11-30')
        self.assertEqual((r['AAA']['gred_industri'], r['AAA']['gred_sektor'], r['AAA']['skor_industri']), ('–', '–', ''))

    def test_jenis_kaedah(self):
        j = G.peta_jenis_kaedah()
        self.assertEqual(len(j), 134)
        self.assertEqual(j['M01'], 'pantulan')
        self.assertEqual(G.id_kaedah('M122 Sesuatu'), 'M122')
        self.assertEqual(G.id_kaedah(''), '')


if __name__ == '__main__':
    unittest.main()
