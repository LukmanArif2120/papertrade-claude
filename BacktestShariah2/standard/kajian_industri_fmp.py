# Kajian gred industri pada peringkat industri, data FMP `historical-industry-performance` (seluruh NASDAQ + NYSE,
# purata perubahan harian sama berat setiap industri, 2016–kini). Pelengkap `standard/kajian_industri.py` (yfinance).
#
# Data: kajian/industri_fmp/fmp_industri_harian.csv.gz (date, industri, bursa, purata_ubah_pct), dikumpul melalui
# alat MCP FMP (nama dengan "&" mesti dihantar sebagai "%26"; jika tidak FMP memulangkan [] palsu).
#
# Guna: python3 kajian_industri_fmp.py [--keluar kajian/industri_fmp]
# Kaedah: pulangan harian industri = purata NASDAQ dan NYSE (dipotong ±30%); industri dengan >= 1000 hari data.
# Skor = pangkat persentil antara industri; gred ikut kuintil. Pulangan hadapan h hari (tutup t hingga tutup t+h)
# tolak purata semua industri; sampel tidak bertindih (setiap h hari).
import os, argparse
import numpy as np
import pandas as pd

BS2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UFUK = (10, 21, 63)


def muat(f):
    d = pd.read_csv(f, dtype={'date': str})
    d['date'] = pd.to_datetime(d.date)
    d['r'] = d.purata_ubah_pct.clip(-30, 30) / 100
    W = d.pivot_table(index='date', columns='industri', values='r', aggfunc='mean').sort_index()
    W = W[W.index.dayofweek < 5]
    W = W.loc[:, W.notna().sum() >= 1000]
    return (1 + W.fillna(0)).cumprod().where(W.notna().cumsum() > 0)


def varian(lv):
    L = lambda a, b=0: lv.shift(b) / lv.shift(a) - 1
    pk = lambda x: x.rank(axis=1, pct=True)
    return {
        'V0 semasa tanpa breadth (1M.30 3M.25 1W.15)': (0.30 * pk(L(21)) + 0.25 * pk(L(63)) + 0.15 * pk(L(5))) / 0.70,
        'V1 1M (Moskowitz-Grinblatt)': pk(L(21)),
        'V4 3M': pk(L(63)),
        'V2 6M (IBD/MSCI)': pk(L(126)),
        'V3 12-1 bulan': pk(L(252, 21)),
        'V5 1M+6M': 0.5 * pk(L(21)) + 0.5 * pk(L(126)),
        'K2 1W sahaja': pk(L(5)),
        'V7 12M': pk(L(252)),
    }


def nilai(lv, V, h):
    fwd = lv.shift(-h) / lv - 1
    fx = fwd.sub(fwd.mean(axis=1), axis=0)
    tt = lv.index[252::h]
    tt = tt[tt <= lv.index[-h - 1]]
    out = []
    for k, s in V.items():
        q = s.loc[tt]; x = fx.loc[tt]
        M = pd.DataFrame({G: x.where((q > lo) & (q <= hi)).mean(axis=1)
                          for G, (lo, hi) in zip('ABCDE', [(.8, 1), (.6, .8), (.4, .6), (.2, .4), (-1, .2)])})
        sp = (M.A - M.E).dropna()
        yr = M.groupby(M.index.year).mean()
        mm = M.mean()
        out.append({'ufuk': h, 'varian': k, **{G: mm[G] * 100 for G in 'ABCDE'}, 'A-E': sp.mean() * 100,
                    't': sp.mean() / sp.std() * np.sqrt(len(sp)), 'tahun_positif_pct': ((yr.A - yr.E) > 0).mean() * 100,
                    'monotonik': pd.Series(mm.values).rank().corr(pd.Series([5, 4, 3, 2, 1])),
                    'A-E 2016-2019': (sp[:'2019'].mean()) * 100, 'A-E 2020-2022': sp['2020':'2022'].mean() * 100,
                    'A-E 2023-kini': sp['2023':].mean() * 100, 'tarikh': len(sp)})
    return out


def md(df, n=2):
    df = df.copy()
    for k in df.columns:
        if pd.api.types.is_float_dtype(df[k]):
            df[k] = df[k].round(n)
    b = ['| ' + ' | '.join(map(str, df.columns)) + ' |', '|' + '---|' * len(df.columns)]
    return '\n'.join(b + ['| ' + ' | '.join('' if pd.isna(v) else str(v) for v in r) + ' |' for r in df.itertuples(index=False)])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--keluar', default=os.path.join(BS2, 'kajian', 'industri_fmp'))
    a = ap.parse_args(argv)
    lv = muat(os.path.join(a.keluar, 'fmp_industri_harian.csv.gz'))
    V = varian(lv)
    R = pd.DataFrame([r for h in UFUK for r in nilai(lv, V, h)])
    R.to_csv(os.path.join(a.keluar, 'varian.csv'), index=False, float_format='%.4g')
    lap = ['# Kajian gred industri: data FMP (peringkat industri)\n',
           f'Dijana oleh `standard/kajian_industri_fmp.py`. {lv.shape[1]} industri, {len(lv)} hari '
           f'({lv.index[0].date()} hingga {lv.index[-1].date()}). Lebihan (%) = pulangan industri tolak purata semua industri; '
           'sampel tidak bertindih. Breadth tiada dalam data FMP.\n']
    for h in UFUK:
        lap += [f'## {h} hari\n', md(R[R.ufuk == h].drop(columns='ufuk')), '']
    open(os.path.join(a.keluar, 'RINGKASAN.md'), 'w', encoding='utf-8').write('\n'.join(lap) + '\n')
    print(R[R.ufuk == 10][['varian', 'A-E', 't', 'monotonik']].round(2).to_string(index=False))


if __name__ == '__main__':
    main()
