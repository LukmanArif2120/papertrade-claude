"""Siling ramalan ARAH 5 hari — berapa tepat ia BOLEH jadi, di luar sampel.

Bukan pradaftar kajian; ini ukuran SILING. Soalan pengguna: ramal setiap hari selepas tutup,
ufuk 5 hari, kebarangkalian naik/turun, dan tala setiap hari sehingga hampir 100% tepat.

Yang diukur di sini:
  1. kadar asas (berapa % bar naik dalam 5 hari) — tanda aras yang mesti dikalahkan
  2. ketepatan + AUC luar sampel model penggalak kecerunan atas 21 peramal
  3. KALIBRASI — bila model kata 60%, adakah ia berlaku 60%? Ini yang penting, bukan ketepatan.
  4. keruntuhan masa — adakah kelebihan LATIH bertahan ke TAHAN

LATIH 2012-2019, TAHAN 2020-2025. Tiada penalaan pada TAHAN.

Guna: python3 REVERSE/step23_siling_arah.py
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))

HARGA = AKAR / 'AUTOTUNE' / '.cache_autotune-data-a02'
PANEL = AKAR / 'REVERSE' / '.cache' / 'panel_ekor.parquet'
FWD = AKAR / 'REVERSE' / '.cache' / 'fwd5.parquet'

H = 5
CAIR = 100_000.0
LATIH, TAHAN = (2012, 2019), (2020, 2025)

PERAMAL = ['atr_pct', 'sd20_pct', 'julat10', 'julat20', 'bb_lebar', 'vol63_pct', 'gap_abs20',
           'mfe63_lalu', 'larian_maks252', 'skew60', 'kurt60',
           'mom63', 'mom126', 'mom252', 'j_ma200', 'cerun_ma50', 'adx14', 'rsi14',
           'log_nilai20', 'log_tutup', 'vol_n50']


def bina_fwd5():
    """fwd5 = tutup[t+H] / buka[t+1] - 1, setiap ticker, tetingkap PENUH sahaja."""
    if FWD.exists():
        return
    t0 = time.time()
    bhg = []
    for y in range(LATIH[0], TAHAN[1] + 1):
        p = HARGA / f'harga_{y}.parquet'
        if p.exists():
            bhg.append(pd.read_parquet(p, columns=['ticker', 'date', 'open', 'close']))
    df = pd.concat(bhg, ignore_index=True).sort_values(['ticker', 'date'])
    del bhg
    o = df['open'].to_numpy('float64')
    c = df['close'].to_numpy('float64')
    tk = df['ticker'].to_numpy()
    n = o.size
    # buka[t+1] dan tutup[t+H], tetapi hanya jika kekal dalam ticker yang SAMA
    masuk = np.full(n, np.nan)
    keluar = np.full(n, np.nan)
    masuk[:n - 1] = o[1:]
    keluar[:n - H] = c[H:]
    sama1 = np.zeros(n, dtype=bool)
    sama1[:n - 1] = tk[1:] == tk[:-1]
    samaH = np.zeros(n, dtype=bool)
    samaH[:n - H] = tk[H:] == tk[:-H]
    sah = sama1 & samaH & np.isfinite(masuk) & (masuk > 0) & np.isfinite(keluar)
    with np.errstate(invalid='ignore', divide='ignore'):
        fwd = np.where(sah, keluar / masuk - 1.0, np.nan)
    out = pd.DataFrame({'ticker': df['ticker'].to_numpy(), 'date': df['date'].to_numpy(),
                        'fwd5': fwd.astype('float32')})
    out.to_parquet(FWD, index=False)
    print(f'  [{time.time()-t0:.0f}s] fwd5: {np.isfinite(fwd).sum():,} sah / {n:,} bar', flush=True)


def main():
    t0 = time.time()
    print('1/4 bina sasaran 5 hari...', flush=True)
    bina_fwd5()

    print('2/4 muat panel + cantum...', flush=True)
    import pyarrow.parquet as pq
    P = pq.read_table(PANEL, columns=['ticker', 'date', 'nilai20'] + PERAMAL).to_pandas()
    P = P[P.nilai20.to_numpy() >= CAIR].drop(columns='nilai20')
    th = P.date.dt.year.to_numpy()
    P = P[(th >= LATIH[0]) & (th <= TAHAN[1])]
    F = pd.read_parquet(FWD)
    P = P.merge(F, on=['ticker', 'date'], how='inner')
    del F
    P = P.dropna(subset=['fwd5'])
    th = P.date.dt.year.to_numpy()
    P['naik'] = (P.fwd5.to_numpy() > 0).astype('int8')
    print(f'  [{time.time()-t0:.0f}s] {len(P):,} bar cair dengan sasaran 5 hari', flush=True)

    tr = (th >= LATIH[0]) & (th <= LATIH[1])
    te = (th >= TAHAN[0]) & (th <= TAHAN[1])
    print(f'\n--- KADAR ASAS (tanda aras yang mesti dikalahkan) ---')
    print(f'  LATIH {LATIH[0]}-{LATIH[1]}: naik {P.naik[tr].mean()*100:.2f}%  (n {tr.sum():,})')
    print(f'  TAHAN {TAHAN[0]}-{TAHAN[1]}: naik {P.naik[te].mean()*100:.2f}%  (n {te.sum():,})')
    print(f'  teka "sentiasa naik" pada TAHAN = {P.naik[te].mean()*100:.2f}% tepat')

    print('\n3/4 latih penggalak kecerunan (LATIH sahaja)...', flush=True)
    import lightgbm as lgb
    from sklearn.metrics import roc_auc_score, brier_score_loss
    Xtr = P.loc[tr, PERAMAL].to_numpy('float32')
    ytr = P.naik[tr].to_numpy()
    Xte = P.loc[te, PERAMAL].to_numpy('float32')
    yte = P.naik[te].to_numpy()
    # subsampel latih untuk kelajuan; 2 juta baris jauh melebihi keperluan statistik
    rng = np.random.default_rng(0)
    if len(ytr) > 2_000_000:
        idx = rng.choice(len(ytr), 2_000_000, replace=False)
        Xtr, ytr = Xtr[idx], ytr[idx]
    m = lgb.LGBMClassifier(n_estimators=400, learning_rate=0.05, num_leaves=63,
                           min_child_samples=500, subsample=0.8, subsample_freq=1,
                           colsample_bytree=0.8, n_jobs=4, verbose=-1, random_state=0)
    m.fit(Xtr, ytr)
    print(f'  [{time.time()-t0:.0f}s] siap', flush=True)

    print('\n4/4 nilai pada TAHAN (tidak pernah dilihat)...', flush=True)
    ptr = m.predict_proba(Xtr)[:, 1]
    pte = m.predict_proba(Xte)[:, 1]
    print(f'  LATIH  AUC {roc_auc_score(ytr, ptr):.4f} | tepat {( (ptr>0.5)==ytr ).mean()*100:.2f}%')
    print(f'  TAHAN  AUC {roc_auc_score(yte, pte):.4f} | tepat {( (pte>0.5)==yte ).mean()*100:.2f}%')
    print(f'  TAHAN  asas (sentiasa naik) {max(yte.mean(), 1-yte.mean())*100:.2f}%')
    print(f'  TAHAN  Brier {brier_score_loss(yte, pte):.5f} | '
          f'Brier asas {brier_score_loss(yte, np.full(yte.size, ytr.mean())):.5f}')

    print('\n--- KALIBRASI TAHAN (bila model kata X%, berapa kerap ia berlaku?) ---')
    bins = np.array([0, .40, .45, .475, .50, .525, .55, .60, 1.01])
    gi = np.digitize(pte, bins) - 1
    for i in range(len(bins) - 1):
        s = gi == i
        if s.sum() < 500:
            continue
        print(f'  model kata {bins[i]*100:4.1f}-{bins[i+1]*100:4.1f}% : '
              f'sebenar {yte[s].mean()*100:5.2f}%  (n {s.sum():>9,})')

    print('\n--- KEYAKINAN TERTINGGI: adakah ia lebih tepat? ---')
    for q in (0.01, 0.05, 0.10, 0.25):
        k = int(len(pte) * q)
        top = np.argsort(pte)[::-1][:k]
        print(f'  {q*100:>4.0f}% paling yakin NAIK : tepat {yte[top].mean()*100:5.2f}%  '
              f'(asas {yte.mean()*100:.2f}%, n {k:,})')

    print('\n--- KEPENTINGAN CIRI ---')
    imp = sorted(zip(PERAMAL, m.feature_importances_), key=lambda x: -x[1])
    print('  ' + ' · '.join(f'{k} {v}' for k, v in imp[:8]))


if __name__ == '__main__':
    main()
