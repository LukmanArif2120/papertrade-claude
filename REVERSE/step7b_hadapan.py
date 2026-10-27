"""STEP 7b — ujian ke hadapan HOLD dan EXIT sebagai SISTEM lengkap (ufuk terbuka, had 252 hari).

Set kemasukan = gabungan kemunculan SEMUA signal yang lulus Step 7 (termasuk yang GAGAL),
didedup ikut (ticker, tarikh). Grid 18 peraturan HOLD x 13 signal EXIT = 234 ujian, ditambah TIGA
rujukan wajib: (a) jual hari ke-63, (b) Chandelier 4xATR14 tanpa veto, (c) pegang hingga hari 252.

Semua 234 sistem dinilai serentak bagi setiap kemasukan dengan satu laluan vektor: matriks
(13 exit x 18 hold x W hari) menentukan hari exit pertama setiap pasangan.

Guna: python3 REVERSE/step7b_hadapan.py 2025
Output: REVERSE/hadapan_hold_exit_<TAHUN>.csv, .cache/dagangan7b_<TAHUN>.npz
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.teras import data as D, keluar as K, signal as S, stat as T  # noqa: E402
from REVERSE.teras.kos import kos_sisi  # noqa: E402

CACHE = AKAR / 'REVERSE' / '.cache'
KELUAR = AKAR / 'REVERSE'
UFUK = 252
PRA = ['bawah_ema9', 'bawah_ema21', 'bawah_ma50', 'rsi_70_60', 'macd_bawah', 'hist_neg3',
       'hari_agihan']
TRAIL = {'trail_2atr': ('atr', 2.0), 'trail_3atr': ('atr', 3.0), 'chandelier_4atr': ('atr', 4.0),
         'trail_8pct': ('pct', 0.92), 'trail_10pct': ('pct', 0.90), 'trail_15pct': ('pct', 0.85)}
NAMA = [f'{e}|X={x}%,Y={y}' for e in K.EXIT13 for (x, y) in K.HOLD18]
RUJ = ['REF_jual_hari63', 'REF_chandelier_4atr', 'REF_pegang_252']


def _pra_siri(g, spy_naik):
    c, h, l, v = g['close'], g['high'], g['low'], g['volume']
    ema9 = c.ewm(span=9, adjust=False, min_periods=9).mean()
    ema21 = c.ewm(span=21, adjust=False, min_periods=21).mean()
    ma50 = c.rolling(50, min_periods=50).mean()
    tr = pd.concat([h - l, (h - c.shift(1)).abs(), (l - c.shift(1)).abs()], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    d = c.diff()
    nw = d.clip(lower=0).ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    tw = (-d).clip(lower=0).ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    rsi = 100 - 100 / (1 + nw / (tw + 1e-12))
    macd = (c.ewm(span=12, adjust=False, min_periods=12).mean()
            - c.ewm(span=26, adjust=False, min_periods=26).mean())
    hist = macd - macd.ewm(span=9, adjust=False, min_periods=9).mean()
    voln = v / (v.rolling(50, min_periods=50).mean() + 1e-12)
    pra = {
        'bawah_ema9': (c < ema9).to_numpy(), 'bawah_ema21': (c < ema21).to_numpy(),
        'bawah_ma50': (c < ma50).to_numpy(),
        'rsi_70_60': ((rsi < 60) & (rsi.rolling(20, min_periods=1).max().shift(1) > 70)).to_numpy(),
        'macd_bawah': ((hist < 0) & (hist.shift(1) >= 0)).to_numpy(),
        'hist_neg3': ((hist < 0) & (hist.shift(1) < 0) & (hist.shift(2) < 0)).to_numpy(),
        'hari_agihan': ((c < c.shift(1)) & (voln >= 2.0)).to_numpy()}
    asas = ((c > ma50) & (ma50.pct_change(10) > 0)).to_numpy() & spy_naik
    lv = dict(ema9=ema9.to_numpy('float64'), ema21=ema21.to_numpy('float64'),
              ma50=ma50.to_numpy('float64'), atr=atr.to_numpy('float64'))
    return pra, asas, lv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tahun', type=int)
    ap.add_argument('--had-kemunculan', type=int, default=24000)
    a_ = ap.parse_args()
    th = a_.tahun
    t0 = time.time()
    sig = pd.read_parquet(CACHE / f'signals_{th}.parquet')
    sig = sig[sig.dalam_univ == 1].reset_index(drop=True)
    kuin = json.loads((CACHE / f'kuintil_{th}.json').read_text())['sempadan']
    lulus = json.loads((CACHE / f'lulus7_{th}.json').read_text())['signal']
    sg = S.bina(sig, kuin)
    mana = np.zeros(len(sig), dtype=bool)
    for nm in lulus:
        mana |= sg[nm]
    ent = sig.loc[mana, ['ticker', 'tarikh']].drop_duplicates().reset_index(drop=True)
    n_unik = len(ent)
    print(f'signal lulus Step 7: {len(lulus)} | kemunculan unik (ticker,tarikh): {n_unik}')
    disampel = False
    if len(ent) > a_.had_kemunculan:
        ent['bulan'] = ent.tarikh.dt.strftime('%Y-%m')
        n_b = a_.had_kemunculan // 12
        ent = (ent.groupby('bulan', group_keys=False)[['ticker', 'tarikh']]
               .apply(lambda d: d.sample(n=min(n_b, len(d)), random_state=42))
               .reset_index(drop=True))
        disampel = True
        print(f'  disampel berlapis ikut bulan (benih 42) -> {len(ent)} kemunculan')
    tick = sorted(ent.ticker.unique())
    fr = D.muat_harga(tick, f'{th - 2}-06-01', '2026-10-16')
    ix = D.muat_indeks(f'{th - 2}-06-01', '2026-10-16')
    spy = ix['SPY']['close']
    spy_n = ((spy > spy.rolling(50, min_periods=50).mean())
             & (spy > spy.rolling(200, min_periods=200).mean()))

    N = len(ent)
    P = len(NAMA) + 3
    pul = np.full((N, P), np.nan, 'float32')
    hari = np.zeros((N, P), 'int16')
    terbuka = np.zeros((N, P), bool)
    mae = np.full((N, P), np.nan, 'float32')
    awal = np.zeros((N, P), bool)
    terpotong = np.zeros((N, P), bool)
    meta_tk = np.empty(N, object)
    meta_mg = np.empty(N, object)
    meta_bl = np.empty(N, object)
    sah = np.zeros(N, bool)
    pos = {(t, d): k for k, (t, d) in enumerate(zip(ent.ticker, ent.tarikh))}
    ix_ch = K.EXIT13.index('chandelier_4atr')
    for tk, grp in ent.groupby('ticker'):
        g = fr.get(tk)
        if g is None or len(g) < 260:
            continue
        sn = spy_n.reindex(g.index).fillna(False).to_numpy()
        pra, asas, lv = _pra_siri(g, sn)
        c = g['close'].to_numpy('float64')
        o = g['open'].to_numpy('float64')
        to = (g['close'] * g['volume']).rolling(20, min_periods=10).median().to_numpy('float64')
        idx = g.index
        n = c.size
        for tgl in grp.tarikh:
            if tgl not in idx:
                continue
            k = pos[(tk, tgl)]
            i = int(idx.get_loc(tgl))
            i0 = i + 1
            if i0 >= n:
                continue
            ks = kos_sisi(to[i])
            masuk = o[i0] * (1 + ks)
            if not np.isfinite(masuk) or masuk <= 0:
                continue
            b = min(i + UFUK, n - 1)
            W = b - i0 + 1
            if W < 2:
                continue
            cw = c[i0:b + 1]
            ow = o[i0:b + 1]
            puncak = np.maximum.accumulate(np.where(np.isfinite(cw), cw, -np.inf))
            baru = cw >= puncak
            ipk = np.maximum.accumulate(np.where(baru, np.arange(W), 0))
            atr_pk = lv['atr'][i0:b + 1][ipk]
            fire = np.empty((13, W), bool)
            for q, e in enumerate(K.EXIT13):
                if e in pra:
                    fire[q] = pra[e][i0:b + 1]
                else:
                    jen, p = TRAIL[e]
                    fire[q] = (cw <= puncak - p * atr_pk) if jen == 'atr' else (cw <= puncak * p)
            dd = (cw / np.where(puncak > 0, puncak, np.nan) - 1.0) * 100.0
            ddok = np.stack([(dd >= -float(x)) for x in K.HOLD_X])            # (6,W)
            maok = np.stack([(cw >= lv[y][i0:b + 1]) for y in K.HOLD_Y])      # (3,W)
            veto = (ddok[:, None, :] & maok[None, :, :] & asas[i0:b + 1])     # (6,3,W)
            veto = veto.reshape(18, W)
            eff = fire[:, None, :] & ~veto[None, :, :]                        # (13,18,W)
            ada = eff.any(-1)
            j = eff.argmax(-1)
            cmin = np.minimum.accumulate(np.where(np.isfinite(cw), cw, np.inf))
            rmax = np.maximum.accumulate(np.where(np.isfinite(cw), cw, -np.inf)[::-1])[::-1]
            i_kel = np.where(ada, np.minimum(i0 + j + 1, n - 1), b)
            rel = np.clip(i_kel - i0, 0, W - 1)
            kasar = np.where(ada, o[i_kel], c[b])
            kasar = np.where(np.isfinite(kasar) & (kasar > 0), kasar, c[b])
            p_ = kasar * (1 - ks) / masuk - 1.0
            fl = slice(0, 234)
            pul[k, fl] = p_.reshape(-1)
            hari[k, fl] = (rel + 1).reshape(-1)
            terbuka[k, fl] = (~ada).reshape(-1)
            mae[k, fl] = (cmin[rel] / masuk - 1.0).reshape(-1)
            awal[k, fl] = (rmax[rel] >= kasar * 1.10).reshape(-1)
            terpotong[k, fl] = bool(b < i + UFUK)
            # rujukan
            b63 = min(i + 63, n - 1)
            r63 = max(min(b63 - i0, W - 1), 0)
            pul[k, 234] = c[b63] * (1 - ks) / masuk - 1.0
            hari[k, 234] = r63 + 1
            mae[k, 234] = cmin[r63] / masuk - 1.0
            awal[k, 234] = rmax[r63] >= c[b63] * 1.10
            terpotong[k, 234] = b63 < i + 63
            q = ix_ch
            pul[k, 235] = pul[k, q * 18 + 17] if False else np.nan
            fch = fire[q]
            if fch.any():
                jj = int(np.argmax(fch))
                ik = min(i0 + jj + 1, n - 1)
                rr = min(max(ik - i0, 0), W - 1)
                kg = o[ik] if np.isfinite(o[ik]) and o[ik] > 0 else c[b]
                pul[k, 235] = kg * (1 - ks) / masuk - 1.0
                hari[k, 235] = rr + 1
                mae[k, 235] = cmin[rr] / masuk - 1.0
                awal[k, 235] = rmax[rr] >= kg * 1.10
            else:
                pul[k, 235] = c[b] * (1 - ks) / masuk - 1.0
                hari[k, 235] = W
                mae[k, 235] = cmin[W - 1] / masuk - 1.0
                terbuka[k, 235] = True
            terpotong[k, 235] = b < i + UFUK
            pul[k, 236] = c[b] * (1 - ks) / masuk - 1.0
            hari[k, 236] = W
            terbuka[k, 236] = True
            mae[k, 236] = cmin[W - 1] / masuk - 1.0
            terpotong[k, 236] = b < i + UFUK
            meta_tk[k], meta_mg[k] = tk, tgl.strftime('%G-W%V')
            meta_bl[k] = tgl.strftime('%Y-%m')
            sah[k] = True
    print(f'[{time.time()-t0:.0f}s] kemasukan sah {int(sah.sum())} x {P} sistem')
    nama_semua = NAMA + RUJ
    np.savez_compressed(CACHE / f'dagangan7b_{th}.npz', pul=pul[sah], hari=hari[sah],
                        terbuka=terbuka[sah], mae=mae[sah], awal=awal[sah],
                        terpotong=terpotong[sah], ticker=meta_tk[sah].astype(str),
                        minggu=meta_mg[sah].astype(str), bulan=meta_bl[sah].astype(str),
                        sistem=np.array(nama_semua))
    rows = []
    for q, nm in enumerate(nama_semua):
        v = pul[sah, q]
        ok = np.isfinite(v)
        if ok.sum() < 20:
            continue
        jk, km, pm, pk = T.jangkaan(v[ok])
        rows.append(dict(sistem=nm, n=int(ok.sum()),
                         median_pulangan=round(float(np.median(v[ok])) * 100, 2),
                         purata_pulangan=round(float(np.mean(v[ok])) * 100, 2),
                         jangkaan=round(jk * 100, 3), kadar_menang=round(km * 100, 2),
                         purata_menang=round(pm * 100, 2), purata_kalah=round(pk * 100, 2),
                         purata_hari_pegang=round(float(hari[sah, q][ok].mean()), 1),
                         mae_median=round(float(np.nanmedian(mae[sah, q][ok])) * 100, 2),
                         pct_exit_terlalu_awal=round(float(awal[sah, q][ok].mean()) * 100, 1),
                         pct_terbuka_hari252=round(float(terbuka[sah, q][ok].mean()) * 100, 1),
                         pct_terpotong_data=round(float(terpotong[sah, q][ok].mean()) * 100, 1),
                         siri_kalah_terpanjang=T.siri_kalah_terpanjang(v[ok])))
    out = pd.DataFrame(rows)
    out['jangkaan_n'] = pd.to_numeric(out.jangkaan, errors='coerce')
    out = out.sort_values('jangkaan_n', ascending=False)
    out.drop(columns=['jangkaan_n']).to_csv(KELUAR / f'hadapan_hold_exit_{th}.csv', index=False)
    ruj = out[out.sistem.isin(RUJ)]
    print('TIGA RUJUKAN WAJIB:')
    print(ruj[['sistem', 'n', 'median_pulangan', 'purata_pulangan', 'jangkaan', 'kadar_menang',
               'purata_hari_pegang', 'pct_exit_terlalu_awal',
               'pct_terbuka_hari252']].to_string(index=False))
    perlu = float(ruj.jangkaan_n.max())
    sis = out[~out.sistem.isin(RUJ)]
    menang = sis[sis.jangkaan_n > perlu]
    print(f'\nambang (jangkaan rujukan TERBAIK) = {perlu:.3f}%')
    print(f'sistem mengalahkan KETIGA-TIGA rujukan: {len(menang)} / {len(sis)}'
          f'{"  (kemasukan disampel)" if disampel else ""}')
    print(sis.head(12)[['sistem', 'n', 'median_pulangan', 'jangkaan', 'kadar_menang',
                        'purata_hari_pegang', 'pct_terbuka_hari252',
                        'pct_exit_terlalu_awal']].to_string(index=False))
    (CACHE / f'lulus7b_{th}.json').write_text(json.dumps(
        dict(ambang=perlu, rujukan={r.sistem: float(r.jangkaan_n) for _, r in ruj.iterrows()},
             sistem=menang.sistem.tolist(), disampel=disampel, n_kemunculan_unik=n_unik,
             n_kemasukan_diuji=int(sah.sum()), n_sistem=len(sis)), indent=1))
    print(f'[{time.time()-t0:.0f}s] siap')


if __name__ == '__main__':
    main()
