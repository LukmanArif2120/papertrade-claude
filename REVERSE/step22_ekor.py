"""Paksi EKOR — bolehkah magnitud kenaikan (MFE) diramal? Pradaftar `REVERSE/SPEC_EKOR_RAMAL.md`.

Soalan LOKASI ("adakah purata naik?") sudah ditutup oleh fasa 1 / SETUP / NXX / SILANG.
Spec ini menanya soalan SKALA ("sejauh mana ia naik?") dengan sasaran MFE, dan memisahkan
ramalan VOLATILITI (simetri, kosong) daripada ramalan ASIMETRI (berguna).

Takrif indikator datang daripada `REVERSE/teras/ind.py` — satu sumber kebenaran, tiada
transkripsi semula (kelas pepijat yang menghasilkan artifak X25).

Guna:
  python3 REVERSE/step22_ekor.py --panel     # bina panel (lama; cache)
  python3 REVERSE/step22_ekor.py --gate0     # ujian asap kombinasi
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.teras import data as D  # noqa: E402
from REVERSE.teras import ind as I  # noqa: E402

KELUAR = AKAR / 'REVERSE'
CACHE = KELUAR / '.cache'
HARGA = AKAR / 'AUTOTUNE' / '.cache_autotune-data-a02'
PANEL = CACHE / 'panel_ekor.parquet'
BHGN = CACHE / 'panel_ekor_parts'

TH0, TH1 = 2012, 2025
PANAS = 2009                      # pemanasan indikator
UFUK = (21, 63)
CAIR = 100_000.0
MIN_BAR = 320

# lajur ind.kira yang spec §5 perlukan (sahaja — panel kekal nipis)
DARI_IND = ['atr14', 'atr_pct', 'bb_lebar', 'julat10', 'julat20', 'ma50', 'ma200',
            'j_ma200', 'cerun_ma50', 'adx14', 'rsi14', 'vol_n50', 'rs_spy_6b']


def tambahan(g):
    """Peramal spec §5 yang ind.py tidak sediakan + sasaran §4. Semua guna data <= tutup t."""
    o, h, l, c, v = g['open'], g['high'], g['low'], g['close'], g['volume']
    d = pd.DataFrame(index=g.index)
    pul = c.pct_change()

    # --- SKALA ---
    d['sd20_pct'] = c.rolling(20, min_periods=20).std(ddof=1) / c * 100.0
    d['vol63_pct'] = pul.rolling(63, min_periods=63).std(ddof=1) * 100.0
    d['gap_abs20'] = (o / c.shift(1) - 1.0).abs().rolling(20, min_periods=20).mean() * 100.0

    # --- SEJARAH-EKOR ---
    # larian terbesar yang DICAPAI dalam 63 hari lalu, relatif kepada tutup hari itu
    d['mfe63_lalu'] = (c.rolling(63, min_periods=63).max() / c - 1.0) * 100.0
    # larian 63-hari terbaik dalam 252 hari lalu (kemuncak keupayaan saham ini)
    naik63 = c / c.shift(63) - 1.0
    d['larian_maks252'] = naik63.rolling(252, min_periods=200).max() * 100.0
    d['skew60'] = pul.rolling(60, min_periods=60).skew()
    d['kurt60'] = pul.rolling(60, min_periods=60).kurt()

    # --- TREND ---
    for n in (63, 126, 252):
        d[f'mom{n}'] = (c / c.shift(n) - 1.0) * 100.0

    # --- CAIR/SAIZ ---
    d['nilai20'] = (c * v).rolling(20, min_periods=10).median()
    d['log_nilai20'] = np.log(d['nilai20'].clip(lower=1.0))
    d['log_tutup'] = np.log(c.clip(lower=0.01))

    # --- SASARAN §4: masuk pada BUKA t+1, tetingkap [t+1, t+H] PENUH sahaja ---
    oa, ha, la, ca = (x.to_numpy('float64') for x in (o, h, l, c))
    n = ca.size
    for H in UFUK:
        mfe_hi = np.full(n, np.nan); mfe_cl = np.full(n, np.nan)
        mae_lo = np.full(n, np.nan); mae_cl = np.full(n, np.nan)
        term = np.full(n, np.nan)
        if n >= H + 1:
            sw = np.lib.stride_tricks.sliding_window_view
            wh, wl, wc = sw(ha, H), sw(la, H), sw(ca, H)
            # bar i -> tetingkap bermula i+1; sah bila i+1 <= n-H
            hi = np.arange(0, n - H)          # indeks bar i yang sah
            j = hi + 1                        # permulaan tetingkap
            masuk = oa[j]
            sah = np.isfinite(masuk) & (masuk > 0)
            mx_h, mx_c = wh[j].max(axis=1), wc[j].max(axis=1)
            mn_l, mn_c = wl[j].min(axis=1), wc[j].min(axis=1)
            akhir = ca[j + H - 1]
            with np.errstate(invalid='ignore', divide='ignore'):
                mfe_hi[hi] = np.where(sah, mx_h / masuk - 1.0, np.nan)
                mfe_cl[hi] = np.where(sah, mx_c / masuk - 1.0, np.nan)
                mae_lo[hi] = np.where(sah, mn_l / masuk - 1.0, np.nan)
                mae_cl[hi] = np.where(sah, mn_c / masuk - 1.0, np.nan)
                term[hi] = np.where(sah, akhir / masuk - 1.0, np.nan)
        d[f'mfe_hi{H}'] = mfe_hi
        d[f'mfe_cl{H}'] = mfe_cl
        d[f'mae_lo{H}'] = mae_lo
        d[f'mae_cl{H}'] = mae_cl
        d[f'term{H}'] = term
        d[f'asim{H}'] = mfe_cl + mae_cl
    return d


def _tulis(buf, j):
    R = pd.concat(buf, ignore_index=True)
    for c in R.columns:
        if R[c].dtype == 'float64':
            R[c] = R[c].astype('float32')
        elif R[c].dtype == 'bool':
            R[c] = R[c].astype('int8')
    R.to_parquet(BHGN / f'p{j:03d}.parquet', index=False)
    return len(R)


def bina_panel():
    if PANEL.exists():
        print(f'panel sudah ada: {PANEL}')
        return
    t0 = time.time()
    bhg = []
    for y in range(PANAS, TH1 + 1):
        p = HARGA / f'harga_{y}.parquet'
        if p.exists():
            bhg.append(pd.read_parquet(
                p, columns=['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']))
    df = pd.concat(bhg, ignore_index=True)
    del bhg
    df = df[df.date <= pd.Timestamp(f'{TH1}-12-31')].sort_values(['ticker', 'date'])
    print(f'  [{time.time()-t0:.0f}s] bar mentah {len(df):,} | ticker {df.ticker.nunique():,}',
          flush=True)

    ix = pd.read_parquet(HARGA / 'idx.parquet')
    spy = ix[ix.ticker == 'SPY'].sort_values('date').set_index('date')['close'].astype('float64')
    print(f'  [{time.time()-t0:.0f}s] SPY {len(spy):,} bar', flush=True)

    CACHE.mkdir(exist_ok=True)
    BHGN.mkdir(parents=True, exist_ok=True)
    for old in BHGN.glob('*.parquet'):
        old.unlink()

    out, n, j, jum = [], 0, 0, 0
    for tk, g in df.groupby('ticker', sort=False):
        if len(g) < MIN_BAR:
            continue
        g = g.set_index('date')
        # sektor_idx=None: spec §5 tidak guna lajur sektor; rs_spy_6b perlu spy sahaja
        ind = I.kira(g, spy=spy.reindex(g.index).ffill(), sektor_idx=None)
        a = ind[[c for c in DARI_IND if c in ind.columns]]
        b = tambahan(g)
        r = pd.concat([a, b], axis=1)
        r.insert(0, 'date', g.index)
        r.insert(0, 'ticker', tk)
        out.append(r.reset_index(drop=True))
        n += 1
        if len(out) >= 400:
            jum += _tulis(out, j)
            out, j = [], j + 1
            print(f'    [{time.time()-t0:.0f}s] {n} ticker | {jum:,} bar', flush=True)
    if out:
        jum += _tulis(out, j)
    del df

    # gabung berperingkat (elak OOM 13.97 GB seperti larian GABUNGAN)
    import pyarrow.parquet as pq
    import pyarrow as pa
    bahagi = sorted(BHGN.glob('*.parquet'))
    wtr = None
    for p in bahagi:
        t = pq.read_table(p)
        if wtr is None:
            wtr = pq.ParquetWriter(PANEL, t.schema, compression='zstd')
        wtr.write_table(t)
        del t
    if wtr is not None:
        wtr.close()
    for p in bahagi:
        p.unlink()
    BHGN.rmdir()
    md = pq.read_metadata(PANEL)
    print(f'  [{time.time()-t0:.0f}s] panel: {md.num_rows:,} bar x {md.num_columns} lajur -> {PANEL}',
          flush=True)


def gate0():
    """Ujian asap §6 gate0. Dijalankan SEBELUM apa-apa nombor dilapor."""
    import pyarrow.parquet as pq
    print('gate0 — ujian asap kombinasi')
    md = pq.read_metadata(PANEL)
    print(f'  panel {md.num_rows:,} bar x {md.num_columns} lajur')
    P = pq.read_table(PANEL, filters=[('ticker', 'in', {'AAPL', 'MSFT', 'XOM', 'JNJ', 'KO'})]
                      ).to_pandas().sort_values(['ticker', 'date'])
    gagal = []

    # (3) ketaksamaan identiti: mfe_cl >= term >= mae_cl bagi SETIAP bar
    for H in UFUK:
        m = P[[f'mfe_cl{H}', f'term{H}', f'mae_cl{H}']].dropna()
        b1 = (m[f'mfe_cl{H}'] < m[f'term{H}'] - 1e-9).sum()
        b2 = (m[f'term{H}'] < m[f'mae_cl{H}'] - 1e-9).sum()
        print(f'  H={H}: n={len(m):,} | langgar mfe>=term {b1} | langgar term>=mae {b2}')
        if b1 or b2:
            gagal.append(f'ketaksamaan identiti H={H}')

    # (1) tetingkap tidak melintas ticker: bar H terakhir setiap ticker mesti NaN
    for H in UFUK:
        buruk = 0
        for tk, g in P.groupby('ticker'):
            ekor = g[f'mfe_cl{H}'].to_numpy()[-H:]
            buruk += int(np.isfinite(ekor).sum())
        print(f'  H={H}: sasaran bukan-NaN dalam {H} bar terakhir setiap ticker = {buruk} (jangka 0)')
        if buruk:
            gagal.append(f'tetingkap melintas ticker H={H}')

    # (2) sasaran mesti sepadan dengan pengiraan tangan pada sampel rawak-tetap
    g = P[P.ticker == 'AAPL'].reset_index(drop=True)
    raw = pd.read_parquet(HARGA / 'harga_2015.parquet')
    raw = raw[raw.ticker == 'AAPL'].sort_values('date').reset_index(drop=True)
    cocok = g.merge(raw[['date', 'open', 'high', 'low', 'close']], on='date', how='inner')
    H = 21
    ok = 0; cek = 0
    for i in range(50, min(150, len(cocok) - H - 1)):
        j0 = i + 1
        masuk = cocok.open.iloc[j0]
        jangka = cocok.close.iloc[j0:j0 + H].max() / masuk - 1.0
        dapat = cocok[f'mfe_cl{H}'].iloc[i]
        if np.isfinite(dapat):
            cek += 1
            ok += abs(jangka - dapat) < 2e-4
    print(f'  pengiraan tangan AAPL 2015 H=21: {ok}/{cek} sepadan')
    if cek and ok < cek:
        gagal.append('sasaran tidak sepadan pengiraan tangan')

    print('  GATE0 ' + ('GAGAL: ' + '; '.join(gagal) if gagal else 'LULUS'))
    return not gagal


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--panel', action='store_true')
    ap.add_argument('--gate0', action='store_true')
    a = ap.parse_args(argv)
    if a.panel:
        bina_panel()
    if a.gate0:
        gate0()


if __name__ == '__main__':
    main()


# ======================================================================
# ANALISIS — gate1/2/3 (spec §6). Fama-MacBeth Spearman keratan rentas.
# ======================================================================

SKALA = ['atr_pct', 'sd20_pct', 'julat10', 'julat20', 'bb_lebar', 'nisbah_julat',
         'vol63_pct', 'gap_abs20']
EKOR_LALU = ['mfe63_lalu', 'larian_maks252', 'skew60', 'kurt60']
TREND = ['mom63', 'mom126', 'mom252', 'j_ma200', 'cerun_ma50', 'adx14']
SAIZ = ['log_nilai20', 'log_tutup', 'vol_n50']
PERAMAL = SKALA + EKOR_LALU + TREND + SAIZ
KELUARGA = ({p: 'SKALA' for p in SKALA} | {p: 'EKOR_LALU' for p in EKOR_LALU}
            | {p: 'TREND' for p in TREND} | {p: 'SAIZ' for p in SAIZ})
SASARAN = ['mfe_cl', 'mae_cl', 'asim']
MIN_NAMA = 30          # minimum saham cair dalam satu tarikh untuk rho keratan rentas


def muat_analisis():
    """Panel analisis: bar cair 2012-2025, lajur yang perlu sahaja."""
    import pyarrow.parquet as pq
    perlu = (['ticker', 'date', 'nilai20', 'julat10', 'julat20']
             + [p for p in PERAMAL if p not in ('nisbah_julat', 'julat10', 'julat20')]
             + [f'{s}{H}' for s in ('mfe_cl', 'mae_cl', 'asim') for H in UFUK])
    ada = set(pq.read_schema(PANEL).names)
    perlu = [c for c in dict.fromkeys(perlu) if c in ada]
    P = pq.read_table(PANEL, columns=perlu).to_pandas()
    P = P[P.nilai20.to_numpy() >= CAIR]
    th = P.date.dt.year.to_numpy()
    P = P[(th >= TH0) & (th <= TH1)]
    with np.errstate(invalid='ignore', divide='ignore'):
        P['nisbah_julat'] = (P.julat10.to_numpy('float64')
                             / np.where(P.julat20.to_numpy('float64') == 0, np.nan,
                                        P.julat20.to_numpy('float64')))
    return P.sort_values('date').reset_index(drop=True)


def _rank(a):
    """Pangkat purata (tie = purata), NaN kekal NaN."""
    from scipy.stats import rankdata
    out = np.full(a.shape, np.nan)
    ok = np.isfinite(a)
    if ok.sum() > 1:
        out[ok] = rankdata(a[ok])
    return out


def rho_harian(P, H):
    """rho Spearman dalam tarikh bagi setiap (peramal, sasaran). Pulangkan dict -> (tarikh, rho)."""
    tar = {s: P[f'{s}{H}'].to_numpy('float64') for s in SASARAN}
    pre = {p: P[p].to_numpy('float64') for p in PERAMAL}
    dt = P.date.to_numpy().astype('datetime64[D]').astype('int64')
    sempadan = np.flatnonzero(np.concatenate([[True], dt[1:] != dt[:-1], [True]]))
    hasil = {(p, s): ([], []) for p in PERAMAL for s in SASARAN}
    for b0, b1 in zip(sempadan[:-1], sempadan[1:]):
        hari = dt[b0]
        for s in SASARAN:
            y = tar[s][b0:b1]
            oky = np.isfinite(y)
            if oky.sum() < MIN_NAMA:
                continue
            yr_full = _rank(np.where(oky, y, np.nan))
            for p in PERAMAL:
                x = pre[p][b0:b1]
                m = oky & np.isfinite(x)
                if m.sum() < MIN_NAMA:
                    continue
                xr = _rank(np.where(m, x, np.nan))[m]
                yr = (_rank(np.where(m, y, np.nan))[m] if m.sum() != oky.sum()
                      else yr_full[m])
                xc, yc = xr - xr.mean(), yr - yr.mean()
                den = np.sqrt((xc * xc).sum() * (yc * yc).sum())
                if den > 0:
                    hasil[(p, s)][0].append(hari)
                    hasil[(p, s)][1].append(float((xc * yc).sum() / den))
    return {k: (np.asarray(v[0]), np.asarray(v[1])) for k, v in hasil.items()}


def nw_se(x, lag):
    """SE Newey-West bagi min siri x (autokorelasi hingga `lag`)."""
    x = np.asarray(x, dtype='float64')
    n = x.size
    if n < lag + 5:
        return np.nan
    e = x - x.mean()
    g0 = float((e * e).sum() / n)
    s = g0
    for k in range(1, lag + 1):
        gk = float((e[k:] * e[:-k]).sum() / n)
        s += 2.0 * (1.0 - k / (lag + 1.0)) * gk
    return float(np.sqrt(max(s, 0.0) / n)) if s > 0 else np.nan
