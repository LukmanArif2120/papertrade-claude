"""Ujian plasebo bagi gate KEMAHIRAN kad skor (G3 lift masuk, NEGATIF) — peraturan tetap pindaan 7 Nov 2026.

Peraturan (`standard/SPEC_KAD_SKOR.md`, "Pindaan 7 Nov 2026"): gate yang mendakwa mengukur kemahiran mesti
memberi kadar lulus palsu <= 5% pada tiga plasebo sebelum dikunci, pada panel A02 2010-2026:
  bebas   - 15 saham rawak setiap hari daripada kolam
  lekit   - saham yang sama cenderung dipilih semula (kebarangkalian kekal 0.8 sehari, larian purata 5 hari),
            seperti isyarat "keadaan" yang menyala berhari-hari
  condong - sentiasa memilih daripada tercile ATR tertinggi (pendedahan faktor turun-naik)
Setiap plasebo diuji dalam tingkap 60 hari beli (kematangan G1), ufuk tetap UFUK sesi, dengan reka bentuk
lama dan baharu. Fungsi SE yang diuji ialah fungsi PRODUKSI (`lift_kaedah._se_kl`, `lift_kaedah.se_dua_hala`),
jadi keputusan ini mengesahkan kod yang benar-benar berjalan setiap malam.

Kolam: alam A02 bulan itu, tutup semalam >= USD10, nilai dagang 20 hari >= USD5 juta (anggaran alam Lejar:
saham patuh Syariah >= USD10). Asas tidak memakai tinggal-satu-keluar kerana 15 daripada ~1,500 saham sehari
memberi kesan ~1%.

BUKAN untuk larian malam: memerlukan Release `autotune-data-a02` (~220 MB, dimuat turun ke cache AUTOTUNE).
  python3 BacktestShariah2/standard/plasebo_gate.py [--ulang 3]
Keluaran: BacktestShariah2/laporan/PLASEBO_GATE.md
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
AKAR = os.path.dirname(BS2)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(AKAR, 'AUTOTUNE'))
import lift_kaedah as lk  # noqa: E402

MD = os.path.join(BS2, 'laporan', 'PLASEBO_GATE.md')
K = 15            # pilihan setiap hari
TINGKAP = 60      # hari beli setiap tingkap (kematangan G1)
HAD_PALSU = 0.05  # peraturan tetap


def panel():
    """Kolam saham-hari A02 dengan pulangan ufuk tetap lk.UFUK dan tercile ATR."""
    from teras import data  # AUTOTUNE/teras/data.py
    import glob
    d = data.ambil(tag='autotune-data-a02')
    u = pd.read_parquet(os.path.join(d, 'universe.parquet'))
    df = pd.concat([pd.read_parquet(f, columns=['ticker', 'date', 'open', 'high', 'low', 'close', 'volume'])
                    for f in sorted(glob.glob(os.path.join(str(d), 'harga_20*.parquet')))], ignore_index=True)
    df = df.sort_values(['ticker', 'date']).reset_index(drop=True)
    for c in ('open', 'high', 'low', 'close'):
        df[c] = df[c].astype('float64')
    g = df.groupby('ticker', sort=False)
    pc = g.close.shift(1)
    tr = np.maximum(df.high - df.low, np.maximum((df.high - pc).abs(), (df.low - pc).abs()))
    atr = tr.groupby(df.ticker, sort=False).transform(lambda s: s.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean())
    df['atrp'] = (atr / df.close * 100).groupby(df.ticker, sort=False).shift(1)
    dv20 = (df.close * df.volume).groupby(df.ticker, sort=False).transform(lambda s: s.rolling(20, min_periods=20).mean())
    df['r'] = (g.close.shift(-(lk.UFUK - 1)) / df.open - 1) * 100 - lk.KOS
    bulan = df.date.dt.strftime('%Y-%m')
    uk = set(zip(u.bulan, u.ticker))
    univ = np.fromiter(((b, t) in uk for b, t in zip(bulan, df.ticker)), bool, len(df))
    ok = univ & (pc >= 10) & (dv20.groupby(df.ticker, sort=False).shift(1) >= 5e6) & df.r.notna() & df.atrp.notna()
    P = df.loc[ok & (df.date >= '2010-03-01'), ['ticker', 'date', 'r', 'atrp']].reset_index(drop=True)
    hari = np.array(sorted(P.date.unique()))
    P['hi'] = P.date.map({d: i for i, d in enumerate(hari)})
    iso = P.date.dt.isocalendar()
    P['minggu'] = (iso.year * 100 + iso.week).astype(int)
    P['q'] = P.groupby('hi').atrp.transform(lambda s: np.floor(s.rank(method='first') * 3 / (len(s) + 1e-9)).clip(0, 2))
    P['L_hari'] = P.r - P.groupby('hi').r.transform('mean')
    P['L_hq'] = P.r - P.groupby(['hi', 'q']).r.transform('mean')
    return P


def pilih(P, jenis, rng):
    by = P.groupby('hi').indices
    qv = P.q.to_numpy()
    tv = P.ticker.to_numpy(dtype=object)          # sekali sahaja: to_numpy setiap hari terlalu perlahan
    out, aktif = [], set()
    for d in range(int(P.hi.max()) + 1):
        ix = by.get(d)
        if ix is None:
            continue
        if jenis == 'bebas':
            out.extend(rng.choice(ix, min(K, len(ix)), replace=False))
        elif jenis == 'condong':
            c = ix[qv[ix] == 2]
            out.extend(rng.choice(c, min(K, len(c)), replace=False))
        else:  # lekit
            tk = tv[ix]
            ada = {t: i for t, i in zip(tk, ix)}
            aktif = {t for t in aktif if t in ada and rng.random() < 0.8}
            while len(aktif) < K:
                aktif.add(tk[rng.integers(len(tk))])
            out.extend(ada[t] for t in aktif)
    return np.array(out)


REKA = {  # nama: (lajur lift, fungsi SE)
    'LAMA: asas hari, kluster hari beli': ('L_hari', lambda S, c: lk._se_kl(S[c] - S[c].mean(), S.hi)),
    'asas hari, kluster minggu': ('L_hari', lambda S, c: lk._se_kl(S[c] - S[c].mean(), S.minggu)),
    'asas hari x ATR, kluster saham': ('L_hq', lambda S, c: lk._se_kl(S[c] - S[c].mean(), S.ticker)),
    'BAHARU: asas hari x ATR, dua hala saham+minggu': ('L_hq', lambda S, c: lk.se_dua_hala(S[c], S.ticker, S.minggu)),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ulang', type=int, default=3)
    a = ap.parse_args()
    P = panel()
    rng = np.random.default_rng(2026)
    hasil = []
    for jenis in ('bebas', 'lekit', 'condong'):
        for _ in range(a.ulang):
            X = P.loc[pilih(P, jenis, rng)].copy()
            X['tw'] = X.hi // TINGKAP
            for _, S in X.groupby('tw'):
                if S.hi.nunique() < TINGKAP * 0.9:
                    continue
                for nama, (col, fse) in REKA.items():
                    se, g = fse(S, col)
                    df = g if nama.startswith('BAHARU') else g - 1
                    m = float(S[col].mean())
                    hasil.append((jenis, nama, m, se, df))
    R = pd.DataFrame(hasil, columns=['plasebo', 'reka', 'm', 'se', 'df'])
    R['palsu'] = np.abs(R.m / R.se) > stats.t.ppf(0.975, R.df.clip(lower=1))
    T = R.groupby(['reka', 'plasebo'], sort=False).agg(tingkap=('m', 'size'), palsu=('palsu', 'mean'),
                                                       sd=('m', 'std'), se=('se', 'mean'))
    T['kalibrasi'] = T.sd / T.se
    lulus = T.xs('BAHARU: asas hari x ATR, dua hala saham+minggu', level='reka').palsu.max() <= HAD_PALSU
    A = ['# Ujian plasebo gate kemahiran (G3 lift masuk, NEGATIF)', '',
         f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh `standard/plasebo_gate.py`. Panel A02 2010–2026, '
         f'ufuk {lk.UFUK} sesi, tingkap {TINGKAP} hari beli, {K} pilihan sehari, {a.ulang} ulangan setiap plasebo. '
         'Fungsi SE = fungsi produksi `lift_kaedah`.', '',
         f"**Reka bentuk BAHARU {'LULUS' if lulus else 'GAGAL'}** peraturan tetap (kadar lulus palsu ≤ "
         f"{HAD_PALSU:.0%} pada ketiga-tiga plasebo).", '',
         '| Reka bentuk | Plasebo | Tingkap | Kadar lulus palsu | SD lift sebenar ÷ purata SE |', '|---|---|---|---|---|']
    for (reka, pl), r in T.iterrows():
        A.append(f'| {reka} | {pl} | {r.tingkap:.0f} | **{r.palsu:.1%}** | {r.kalibrasi:.2f} |')
    A += ['', 'Kalibrasi > 1 bermaksud SE terlalu kecil (ujian terlalu mudah lulus); < 1 bermaksud konservatif.', '',
          'Bacaan: kluster ikut hari beli (reka bentuk lama) betul HANYA bagi pilihan bebas. Kaedah sebenar sering '
          'membeli saham sama berulang kali atau condong kepada saham meruap, dan di situ ia meluluskan plasebo '
          'berkali ganda melebihi 5%. Padanan tercile ATR membuang pendedahan turun-naik; kluster dua hala '
          '(saham, minggu) menyerap ulangan saham dan pergerakan bersama dalam minggu yang sama.', '']
    os.makedirs(os.path.dirname(MD), exist_ok=True)
    open(MD, 'w', encoding='utf-8').write('\n'.join(A))
    print(T.round(3).to_string())
    print('BAHARU', 'LULUS' if lulus else 'GAGAL')
    return 0 if lulus else 1


if __name__ == '__main__':
    sys.exit(main())
