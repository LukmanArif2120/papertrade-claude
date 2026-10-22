# Ujian kod/peristiwa.py (22 Okt 2026): faktor peristiwa besar digunakan sekali pada stor, bar baharu mentah diselaraskan,
# dividen >= 2% menjadi baris faktor, calon jurang tanpa earnings, dan posisi C merentasi tarikh_ex dilaras sekali.
import csv, os, sys, tempfile, unittest
import numpy as np, pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'kod'))
import peristiwa as P  # noqa: E402
import harga_yf  # noqa: E402

T = [int(x.strftime('%Y%m%d')) for x in pd.bdate_range('2026-10-01', periods=30)]


def bar(tarikh, tutup, t='DD'):
    c = np.asarray(tutup, float)
    return pd.DataFrame(dict(ticker=t, date=tarikh, open=c, high=c * 1.01, low=c * 0.99, close=c, volume=1000))


def faktor(d, rows):
    p = os.path.join(d, 'faktor.csv'); P.tulis(pd.DataFrame(rows), p); return P.muat(p)


class TestPeristiwa(unittest.TestCase):
    def test_guna_stor_dan_bar_baharu(self):
        # spin-off pada T[20] (faktor 0.4): mentah 100 -> 40. Selepas pelarasan, siri seragam (tiada jurang palsu).
        mentah = np.r_[[100.0] * 20, [40.0] * 10]
        with tempfile.TemporaryDirectory() as d:
            rows = faktor(d, [dict(saham='DD', tarikh_ex=str(pd.Timestamp(str(T[20])).date()), jenis='spin_off', faktor='0.4',
                                   sumber='ujian', catatan='', ditambah='')])
            stor = {'harga_A.csv': bar(T[:22], mentah[:22])}
            log = P.guna_stor(stor, d, rows)
            self.assertEqual(len(log), 1)
            np.testing.assert_allclose(stor['harga_A.csv'].close.values, 40.0)
            self.assertEqual(P.guna_stor(stor, d, rows), [])                       # sekali sahaja
            baru = P.laras_baru(bar(T[15:30], mentah[15:30]), rows)                 # tetingkap merentasi tarikh_ex
            np.testing.assert_allclose(baru.close.values, 40.0)
            # sebelum tarikh_ex berlaku (bar akhir < ex): tiada pelarasan
            self.assertEqual(P.guna_stor({'harga_A.csv': bar(T[:15], mentah[:15])}, os.path.join(d, 'x') if os.makedirs(os.path.join(d, 'x')) is None else d, rows), [])
            np.testing.assert_allclose(P.laras_baru(bar(T[:15], mentah[:15]), rows).close.values, 100.0)

    def test_gabung_harga_yf_dengan_faktor(self):
        mentah = np.r_[[100.0] * 20, [40.0] * 10]
        with tempfile.TemporaryDirectory() as d:
            fk = os.path.join(d, 'faktor.csv')
            P.tulis(pd.DataFrame([dict(saham='DD', tarikh_ex=str(pd.Timestamp(str(T[20])).date()), jenis='spin_off', faktor='0.4',
                                       sumber='ujian', catatan='', ditambah='')]), fk)
            lama_f = P.FAKTOR; P.FAKTOR = fk
            try:
                stor = {'harga_A.csv': bar(T[:22], mentah[:22])}
                stor, nota = harga_yf.gabung(stor, bar(T[18:30], mentah[18:30]), d)
            finally:
                P.FAKTOR = lama_f
            x = stor['harga_A.csv'].sort_values('date')
            np.testing.assert_allclose(x.close.values, 40.0)
            self.assertEqual([r['keputusan'] for r in nota['log_laras']], ['faktor'])

    def test_dividen_dan_calon(self):
        with tempfile.TemporaryDirectory() as d:
            fk, dv, cl = (os.path.join(d, f) for f in ('faktor.csv', 'dividen.csv', 'calon.csv'))
            P.simpan_dividen(pd.DataFrame(dict(ticker=['A', 'B'], date=[T[10], T[10]], dividen=[0.3, 3.0])), dv)
            ix = pd.to_datetime([str(x) for x in T])
            g = pd.DataFrame(dict(open=50.0, high=51.0, low=49.0, close=50.0, volume=1e6), index=ix)
            baru = P.tambah_dari_dividen({'A': g, 'B': g}, fk, dv, mula='2026-09-01')
            self.assertEqual([(x['saham'], x['jenis'], x['faktor']) for x in baru], [('B', 'dividen_khas', '0.940000')])
            self.assertEqual(P.tambah_dari_dividen({'A': g, 'B': g}, fk, dv, mula='2026-09-01'), [])
            h = g.copy(); h.iloc[25:, :4] = 40.0; h.iloc[25, 0] = 40.0                 # jurang −20% pada T[25]
            e = g.copy(); e.iloc[25:, :4] = 40.0
            c = P.kesan_calon({'X': h, 'E': e}, ix, {'E': [str(ix[25].date())]}, cl, fk)
            self.assertEqual([x['saham'] for x in c], ['X'])                          # E: hari earnings -> bukan calon
            self.assertEqual(P.kesan_calon({'X': h}, ix, {}, cl, fk), [])             # tidak berulang

    def test_laras_c(self):
        lajur = ['tarikh_beli', 'saham', 'kaedah', 'harga_beli', 'harga_terkini', 'untung_pct', 'henti', 'sasaran', 'keluar',
                 'tarikh_keluar', 'harga_keluar', 'untung_akhir_pct', 'nota', 'tidak_dibeli', 'keluar_henti']
        rows = [dict(tarikh_beli='2026-10-05', saham='DD', kaedah='M01', harga_beli='100', harga_terkini='41', henti='90', keluar='False'),
                dict(tarikh_beli='2026-10-05', saham='DD', kaedah='M02', harga_beli='100', harga_terkini='99', keluar='True',
                     tarikh_keluar='2026-10-10', harga_keluar='99'),                                  # keluar sebelum ex
                dict(tarikh_beli='2026-10-20', saham='DD', kaedah='M03', harga_beli='40', harga_terkini='41', keluar='False')]
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'claude_2.csv')
            with open(p, 'w', newline='') as f:
                w = csv.DictWriter(f, lajur); w.writeheader()
                for r in rows:
                    w.writerow({k: r.get(k, '') for k in lajur})
            fr = pd.DataFrame([dict(saham='DD', tarikh_ex='2026-10-15', jenis='spin_off', faktor='0.4', sumber='u', catatan='', ditambah='')])
            x = P.laras_c(d, fr)
            self.assertEqual([y[2] for y in x], ['M01'])
            with open(p) as f:
                out = list(csv.DictReader(f))
            self.assertEqual((out[0]['harga_beli'], out[0]['henti'], out[0]['untung_pct']), ('40', '36', '2.50'))
            self.assertEqual(out[1]['harga_beli'], '100')
            self.assertEqual(P.laras_c(d, fr), [])


if __name__ == '__main__':
    unittest.main()
