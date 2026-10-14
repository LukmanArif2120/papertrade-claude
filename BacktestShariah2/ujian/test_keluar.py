# Ujian fungsi keluar() dalam standard/harian_nilai_keluar.py.
# Skrip itu memuat data semasa diimport, jadi fungsi keluar() diambil terus daripada kod sumber (ast)
# supaya ujian tidak bergantung pada stor harga.
import ast, os, unittest
import numpy as np, pandas as pd

SUMBER = os.path.join(os.path.dirname(__file__), '..', 'standard', 'harian_nilai_keluar.py')


def _muat_keluar():
    tree = ast.parse(open(SUMBER, encoding='utf-8').read())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'keluar')
    ns = {'pd': pd, 'np': np}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), SUMBER, 'exec'), ns)
    return ns['keluar']


keluar = _muat_keluar()


def bar(rows, stop=90.0, tgt=np.nan):
    """rows: senarai (open, high, low, close[, exitc]); bar 0 = hari isyarat (2026-10-01)."""
    ix = pd.bdate_range('2026-10-01', periods=len(rows))
    g = pd.DataFrame([r[:4] for r in rows], index=ix, columns=['open', 'high', 'low', 'close'])
    g['stop'] = stop
    g['tgt'] = tgt
    g['exitc'] = [bool(r[4]) if len(r) > 4 else False for r in rows]
    return g


TI = '2026-10-01'


class UjiKeluar(unittest.TestCase):
    def test_kena_henti_hari_masuk_pada_paras_henti(self):
        g = bar([(100, 101, 99, 100), (100, 100, 89, 95)])
        x, sp = keluar(g, TI, 100, None)
        self.assertEqual((x['t'], x['p'], x['why']), (g.index[1], 90.0, 'kena henti'))
        self.assertEqual(sp, 90.0)

    def test_buka_jurang_bawah_henti_jual_pada_buka(self):
        g = bar([(100, 101, 99, 100), (100, 101, 95, 99), (85, 86, 80, 84)])
        x, _ = keluar(g, TI, 100, None)
        self.assertEqual((x['t'], x['p']), (g.index[2], 85.0))
        self.assertIn('buka bawah henti', x['why'])

    def test_hari_masuk_tiada_semakan_jurang(self):
        # Buka hari masuk di bawah henti tidak dikira jurang; henti kena pada paras henti
        g = bar([(100, 101, 99, 100), (88, 92, 87, 91)])
        x, _ = keluar(g, TI, 88, None)
        self.assertEqual((x['p'], x['why']), (90.0, 'kena henti'))

    def test_sasaran_tidak_dinilai_pada_hari_masuk(self):
        g = bar([(100, 101, 99, 100), (100, 130, 99, 120), (120, 121, 119, 120)], tgt=110.0)
        x, _ = keluar(g, TI, 100, None)
        self.assertEqual(x['t'], g.index[2])
        self.assertIn('capai sasaran (buka atas sasaran)', x['why'])
        self.assertEqual(x['p'], 120.0)

    def test_sasaran_guna_tgt_hari_sebelumnya(self):
        g = bar([(100, 101, 99, 100), (100, 102, 99, 101), (101, 112, 100, 108)], tgt=110.0)
        g.iloc[2, g.columns.get_loc('tgt')] = 200.0  # tgt hari ini tidak dipakai
        x, _ = keluar(g, TI, 100, None)
        self.assertEqual((x['t'], x['p'], x['why']), (g.index[2], 110.0, 'capai sasaran'))

    def test_isyarat_keluar_jual_pada_buka_esok(self):
        g = bar([(100, 101, 99, 100), (100, 102, 99, 101, True), (103, 104, 102, 103)])
        x, _ = keluar(g, TI, 100, None)
        self.assertEqual((x['t'], x['p']), (g.index[2], 103.0))
        self.assertTrue(x['why'].startswith('isyarat keluar kaedah'))

    def test_isyarat_keluar_bar_terakhir_menunggu(self):
        g = bar([(100, 101, 99, 100), (100, 102, 99, 101, True)])
        x, _ = keluar(g, TI, 100, None)
        self.assertEqual(x['why'], 'menunggu')
        self.assertIsNone(x['t'])
        self.assertEqual(x['isy'], g.index[1])

    def test_had_masa_jual_pada_tutup(self):
        g = bar([(100, 101, 99, 100), (100, 102, 99, 101), (101, 103, 100, 102.5)])
        x, _ = keluar(g, TI, 100, 2)
        self.assertEqual((x['t'], x['p']), (g.index[2], 102.5))
        self.assertIn('had masa 2 hari', x['why'])

    def test_henti_didahulukan_atas_sasaran_hari_sama(self):
        g = bar([(100, 101, 99, 100), (100, 101, 99, 100), (100, 115, 85, 100)], tgt=110.0)
        x, _ = keluar(g, TI, 100, None)
        self.assertEqual(x['why'], 'kena henti')

    def test_tiada_henti_tiada_keluar(self):
        g = bar([(100, 101, 99, 100), (100, 102, 50, 101)], stop=np.nan)
        x, sp = keluar(g, TI, 100, None)
        self.assertIsNone(x)
        self.assertEqual(sp, -np.inf)

    def test_tiada_bar_isyarat(self):
        g = bar([(100, 101, 99, 100)])
        x, why = keluar(g, '2025-01-01', 100, None)
        self.assertIsNone(x)
        self.assertEqual(why, 'tiada bar isyarat')


if __name__ == '__main__':
    unittest.main()
