# jalur_jangka.py — jalur jangkaan ke hadapan setiap saham untuk carta kedua helaian posisi.
#
# BUKAN ramalan arah. `REVERSE/SILING_ARAH.md` mengukur siling ramalan arah 5 hari: 51.55% tepat
# luar sampel lawan asas 50.50%, dan pilihan paling yakin memperoleh KURANG (+0.3105%) daripada
# membeli semua bar (+0.3118%). Yang boleh diramal dengan teguh ialah LEBAR, bukan arah:
# atr_pct lawan MFE 21 hari rho +0.270 (positif pada 95.5% daripada 3,499 tarikh) dan lawan |MAE|
# rho +0.346 (98.5%), manakala lawan pulangan terminal rho hanya -0.043 (41.8%).
#
# Maka carta ini memaparkan satu kekerapan bersyarat, bukan satu ramalan:
#   "saham dalam keadaan turun naik yang sama secara sejarah berada antara X% dan Y% selepas N hari"
# dan satu nombor keputusan:
#   P(paras lorong 2 disentuh dalam N hari) daripada taburan MAE kumpulan yang sama.
#
# Dua peringkat:
#   bina_jadual()  — sekali, daripada panel REVERSE (8.5 juta bar, 2012-2025). Keluaran kecil:
#                    data/jalur/jadual.json. Ditanam pada DESIL atr_pct KERATAN RENTAS dalam tarikh,
#                    kerana taburan atr_pct hanyut merentas masa; desil mutlak akan condong ikut era.
#   dokumen()      — setiap malam, daripada stor harga repo: desil semasa setiap posisi -> jalur.
#
# Guna: python3 BacktestShariah2/standard/jalur_jangka.py --bina-jadual
import json
import os
import sys

import numpy as np

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BS2 = os.path.join(AKAR, 'BacktestShariah2')
JADUAL = os.path.join(BS2, 'data', 'jalur', 'jadual.json')

UFUK = (5, 21)
NDESIL = 10
KUANTIL = (10, 25, 50, 75, 90)
# grid MAE untuk menyongsang P(sentuh) pada sebarang jarak paras; dalam PERATUS, menurun
GRID_MAE = [-1, -2, -3, -4, -5, -6, -8, -10, -12, -15, -18, -21, -25, -30, -35, -40, -50]
MIN_SEL = 2000          # minimum bar setiap sel sebelum kuantil dipercayai
# VERSI: naikkan apabila takrif sasaran/p_sentuh berubah supaya cache lama tidak diguna semula.
#   1 = asal · 2 = mae5 asas tutup (fe822a2) · 3 = paras MENAIK + desil pangkat-alam (f637922)
VERSI = 3


# ---------------------------------------------------------------- peringkat 1
def bina_jadual(panel=None, keluar=JADUAL):
    """Kira jadual kuantil daripada panel REVERSE. Perlu REVERSE/.cache/panel_ekor.parquet."""
    import pandas as pd
    import pyarrow.parquet as pq

    panel = panel or os.path.join(AKAR, 'REVERSE', '.cache', 'panel_ekor.parquet')
    if not os.path.exists(panel):
        raise SystemExit(f'panel tiada: {panel}\nbina dengan: python3 REVERSE/step22_ekor.py --panel')

    print('muat panel...', flush=True)
    P = pq.read_table(panel, columns=['ticker', 'date', 'nilai20', 'atr_pct', 'atr14',
                                      'mfe_cl21', 'mae_cl21', 'term21']).to_pandas()
    P = P[P.nilai20.to_numpy() >= 100_000.0]
    th = P.date.dt.year.to_numpy()
    P = P[(th >= 2012) & (th <= 2025)].dropna(subset=['atr_pct'])

    print('kira sasaran 5 hari...', flush=True)
    H5 = _sasaran5(sorted(set(P.ticker)), P)
    P = P.merge(H5, on=['ticker', 'date'], how='left')

    print('simulasi paras MENAIK (lorong 2) setiap ufuk...', flush=True)
    R = P.sort_values(['ticker', 'date']).reset_index(drop=True)
    _tk = R.ticker.to_numpy()
    _o = R.get('buka_mentah')
    if _o is None:
        RAW = _harga_mentah()
        R = R.merge(RAW, on=['ticker', 'date'], how='left')
    _o = R.buka_mentah.to_numpy('float64')
    _c = R.tutup_mentah.to_numpy('float64')
    _a = R.atr14.to_numpy('float64')
    PT_ = {}
    for Hf in UFUK:
        PT_[Hf] = _p_tercetus(R.ticker.to_numpy(), _o, _c, _a, Hf, GRID_MAE)
        print(f'  H={Hf} siap', flush=True)
    R['desil_'] = (R.groupby('date', observed=True).atr_pct
                   .rank(pct=True, method='first').mul(NDESIL).clip(upper=NDESIL - 1e-9)
                   .astype('int8'))

    print('desil atr_pct keratan rentas dalam tarikh...', flush=True)
    P['desil'] = (P.groupby('date', observed=True).atr_pct
                  .rank(pct=True, method='first').mul(NDESIL).clip(upper=NDESIL - 1e-9)
                  .astype('int8'))

    # tepi desil atr_pct: dikira setiap tarikh kemudian dipuratakan (median) merentas tarikh,
    # supaya padanan masa-larian boleh ikut NILAI atr_pct dan bukan pangkat tempatan
    tepi_hari = (P.groupby('date', observed=True).atr_pct
                 .quantile([i / NDESIL for i in range(1, NDESIL)]).unstack())
    tepi = [round(float(v), 4) for v in tepi_hari.median().to_numpy()]

    jad = {'nota': ('Kuantil pulangan hadapan bersyarat desil atr_pct keratan rentas. '
                    'Bukan ramalan arah; lihat REVERSE/SILING_ARAH.md.'),
           'alam': 'autotune-data-a02 2012-2025, bar cair nilai20 >= USD100k',
           'versi': VERSI,
           'ndesil': NDESIL, 'kuantil': list(KUANTIL), 'grid_mae': list(GRID_MAE),
           'atr_pct_tepi': tepi,
           'ufuk': list(UFUK), 'sel': {}}

    for H in UFUK:
        kt, km, kx = (f'term{H}', f'mae{H}', f'mfe{H}') if H == 5 else ('term21', 'mae_cl21', 'mfe_cl21')
        for d in range(NDESIL):
            s = P[P.desil == d]
            t = s[kt].to_numpy('float64'); t = t[np.isfinite(t)]
            m = s[km].to_numpy('float64'); m = m[np.isfinite(m)]
            x = s[kx].to_numpy('float64'); x = x[np.isfinite(x)]
            if t.size < MIN_SEL or m.size < MIN_SEL:
                continue
            jad['sel'][f'{H}|{d}'] = {
                'n': int(t.size),
                'atr_pct_median': round(float(np.median(s.atr_pct)), 3),
                'term': [round(float(np.percentile(t, q) * 100), 3) for q in KUANTIL],
                'mfe50': round(float(np.median(x) * 100), 3),
                'mae50': round(float(np.median(m) * 100), 3),
                # P(MAE <= ambang) bagi setiap ambang grid -> boleh disongsang untuk sebarang jarak
                # P(paras MENAIK tercetus) — peristiwa sebenar lorong 2, bukan halangan tetap
                'p_sentuh': [round(float(PT_[H][gi][(R.desil_ == d).to_numpy()].mean() * 100), 2)
                             for gi in range(len(GRID_MAE))],
                'p_tetap': [round(float((m * 100 <= g).mean() * 100), 2) for g in GRID_MAE],
            }
        print(f'  H={H}: {sum(1 for k in jad["sel"] if k.startswith(f"{H}|"))} desil', flush=True)

    os.makedirs(os.path.dirname(keluar), exist_ok=True)
    with open(keluar, 'w') as f:
        json.dump(jad, f, separators=(',', ':'), sort_keys=True)
    print(f'ditulis {keluar} ({os.path.getsize(keluar):,} bait)')
    return jad


def _p_tercetus(tk, o, c, atr, H, grid):
    """P(paras lorong 2 tercetus dalam H hari) bagi setiap bar, setiap ambang grid.

    Paras lorong 2 MENAIK: paras_j = max(paras_{j-1}, puncak_j - 4 x ATR14_j), puncak = tutup
    tertinggi sejak masuk; tercetus bila tutup < paras. Halangan tetap (P(MAE <= g)) menilai
    peristiwa yang SALAH dan memberi had bawah — diukur 1.68x terlalu rendah pada keadaan
    median posisi langsung, 2.70x pada desil 9.

    Masuk buka t+1; paras awal = buka(t+1) x (1 + g/100) supaya ia sepadan dengan `jarak` langsung.
    Pulangkan array (len(grid), n) boolean.
    """
    n = c.size
    GANDA = 4.0
    out = np.zeros((len(grid), n), dtype=bool)
    if n < H + 1:
        return out
    idx = np.arange(0, n - H)
    j0 = idx + 1
    sah = (tk[j0 + H - 1] == tk[idx]) & np.isfinite(o[j0]) & (o[j0] > 0)
    masuk = np.where(sah, o[j0], np.nan)
    puncak = np.full(idx.size, -np.inf)
    M = np.full(idx.size, -np.inf)           # max sejauh ini bagi (puncak - 4 x ATR)
    paras0 = [masuk * (1.0 + g / 100.0) for g in grid]
    hidup = [sah.copy() for _ in grid]
    tercetus = [np.zeros(idx.size, dtype=bool) for _ in grid]
    for step in range(H):
        jj = j0 + step
        cj, aj = c[jj], atr[jj]
        puncak = np.maximum(puncak, np.where(np.isfinite(cj), cj, -np.inf))
        with np.errstate(invalid='ignore'):
            cand = puncak - GANDA * np.where(np.isfinite(aj), aj, np.inf)
        M = np.maximum(M, cand)
        for gi in range(len(grid)):
            lvl = np.maximum(paras0[gi], M)
            kena = hidup[gi] & ~tercetus[gi] & np.isfinite(cj) & (cj < lvl)
            tercetus[gi] |= kena
    for gi in range(len(grid)):
        out[gi, idx] = tercetus[gi] & sah
    return out


def _sasaran5(tickers, P):
    """term5/mae5/mfe5 daripada stor A02; masuk buka t+1, tetingkap [t+1, t+5] PENUH."""
    import pandas as pd
    # cache dicap VERSI: tanpa cap, larian semula pada checkout lama memulihkan diam-diam
    # nombor asas-rendah yang salah (lihat komit fe822a2)
    cache = os.path.join(AKAR, 'REVERSE', '.cache', f'sasaran5_v{VERSI}.parquet')
    if os.path.exists(cache):
        return pd.read_parquet(cache)
    H = 5
    src = os.path.join(AKAR, 'AUTOTUNE', '.cache_autotune-data-a02')
    bhg = [pd.read_parquet(os.path.join(src, f'harga_{y}.parquet'),
                           columns=['ticker', 'date', 'open', 'high', 'low', 'close'])
           for y in range(2012, 2026) if os.path.exists(os.path.join(src, f'harga_{y}.parquet'))]
    df = pd.concat(bhg, ignore_index=True).sort_values(['ticker', 'date'])
    del bhg
    o, hi, lo, c = (df[k].to_numpy('float64') for k in ('open', 'high', 'low', 'close'))
    tk = df['ticker'].to_numpy()
    n = o.size
    sw = np.lib.stride_tricks.sliding_window_view
    term = np.full(n, np.nan); mae = np.full(n, np.nan); mfe = np.full(n, np.nan)
    if n >= H + 1:
        wc = sw(c, H)
        i = np.arange(0, n - H)
        j = i + 1
        sama = tk[j + H - 1] == tk[i]
        masuk = o[j]
        ok = sama & np.isfinite(masuk) & (masuk > 0)
        with np.errstate(invalid='ignore', divide='ignore'):
            term[i] = np.where(ok, c[j + H - 1] / masuk - 1.0, np.nan)
            # TUTUP, bukan rendah intrabar: peraturan lorong 2 ialah `tutup < paras -> jual buka
            # esok`, jadi MAE mesti sepadan. mae_cl21 dalam panel juga berasaskan tutup; guna
            # rendah di sini akan melambungkan P(sentuh) 5 hari berbanding angka 21 hari.
            mae[i] = np.where(ok, wc[j].min(axis=1) / masuk - 1.0, np.nan)
            mfe[i] = np.where(ok, wc[j].max(axis=1) / masuk - 1.0, np.nan)
    out = pd.DataFrame({'ticker': df.ticker.to_numpy(), 'date': df.date.to_numpy(),
                        'term5': term.astype('float32'), 'mae5': mae.astype('float32'),
                        'mfe5': mfe.astype('float32')})
    out.to_parquet(cache, index=False)
    return out


# ---------------------------------------------------------------- peringkat 2
def _harga_mentah():
    """buka/tutup mentah A02 2012-2025 untuk simulasi paras (panel tidak menyimpannya)."""
    import pandas as pd
    src = os.path.join(AKAR, 'AUTOTUNE', '.cache_autotune-data-a02')
    bhg = [pd.read_parquet(os.path.join(src, f'harga_{y}.parquet'), columns=['ticker', 'date', 'open', 'close'])
           for y in range(2012, 2026) if os.path.exists(os.path.join(src, f'harga_{y}.parquet'))]
    df = pd.concat(bhg, ignore_index=True)
    return df.rename(columns={'open': 'buka_mentah', 'close': 'tutup_mentah'})


def muat_jadual(p=JADUAL):
    with open(p) as f:
        return json.load(f)


def p_sentuh(sel, jarak_pct, grid):
    """Songsang linear P(MAE <= jarak) daripada grid. jarak_pct negatif (cth -16.40)."""
    if jarak_pct is None or not np.isfinite(jarak_pct):
        return None
    if jarak_pct >= 0:
        return 100.0            # tutup sudah di bawah paras: sudah tercetus, bukan 'tidak diketahui'
    g = np.asarray(grid, dtype='float64')       # menurun: -1, -2, ...
    p = np.asarray(sel['p_sentuh'], dtype='float64')
    if jarak_pct >= g[0]:
        return round(float(p[0]), 1)
    if jarak_pct <= g[-1]:
        return round(float(p[-1]), 1)
    # g menurun -> balikkan untuk np.interp
    return round(float(np.interp(jarak_pct, g[::-1], p[::-1])), 1)


def _atr_pct(h, l, c, n=14):
    """atr_pct seperti REVERSE/teras/ind.py (ATR14 Wilder/RMA) dalam % harga.

    SENGAJA berbeza daripada keluar_lorong.atr, yang purata MUDAH 14 bar dan menetapkan paras
    lorong 2 itu sendiri. Padanan desil wajib guna penganggar yang menanam tepi jadual: nisbah
    purata-mudah/Wilder median 1.034 pada posisi langsung, cukup untuk menukar desil 28% baris
    dan menganjak p21 median 4.6 mata. Jangan "selaraskan" dengan keluar_lorong.atr.
    """
    import pandas as pd
    jalan = os.path.join(AKAR, 'REVERSE', 'teras')
    if jalan not in sys.path:
        sys.path.insert(0, jalan)
    from ind import _wilder
    pc = np.r_[np.nan, c[:-1]]
    tr = np.fmax(h - l, np.fmax(np.abs(h - pc), np.abs(l - pc)))
    a = _wilder(pd.Series(tr), n).to_numpy()
    with np.errstate(invalid='ignore', divide='ignore'):
        return a / np.where(c == 0, np.nan, c) * 100.0


def dokumen(H, l2rows, folder=None, jadual=None):
    """Dokumen db posisi/jalur. Hanya posisi yang MASIH DIPEGANG (jalur ke hadapan).

    H       : {saham: DataFrame date/open/high/low/close} seperti trend_status.muat_harga
    l2rows  : rows daripada lorong2_siri.dokumen() — siri digunakan semula, tidak dikira semula

    rows: ["saham|tarikh_beli", {d, atr, jarak, u:{"5":[q10..q90],"21":[...]}, ps:{"5":p,"21":p}}]
    `u`  = kuantil pulangan terminal (%) bagi desil atr_pct yang sama — kekerapan bersyarat.
    `ps` = P(paras lorong 2 disentuh dalam ufuk itu) pada jarak semasa, daripada taburan MAE.
    Desil dikira merentas keratan rentas posisi HARI INI, sepadan dengan cara jadual ditanam.
    """
    jad = jadual or muat_jadual()
    keadaan = {}
    for kunci, A in (l2rows or []):
        if not A:
            continue
        b = A[-1]
        if b[4] in ('jual', 'lepas', 'bawah'):   # sudah keluar, atau isyarat jual sudah tercetus
            continue
        if b[2] is None or not b[1]:       # belum ada paras (sebelum beli)
            continue
        g = H.get(kunci.split('|')[0])
        if g is None or not len(g):
            continue
        hh, ll, cc = (g[k].to_numpy(float) for k in ('high', 'low', 'close'))
        ap = _atr_pct(hh, ll, cc)
        if not len(ap) or not np.isfinite(ap[-1]):
            continue
        keadaan[kunci] = (float(ap[-1]), (b[2] / b[1] - 1.0) * 100.0)
    if not keadaan:
        return dict(rows=[], ndesil=NDESIL, kuantil=list(KUANTIL), ufuk=list(UFUK))
    # Desil mesti dikira dengan cara yang SAMA seperti jadual dibina: pangkat keratan rentas
    # dalam tarikh merentas ALAM, bukan nilai mutlak terhadap tepi (persetujuan hanya 33.3%;
    # pada Mac-April 2020, 96% bar memetakan ke desil 8/9 secara mutlak) dan bukan pangkat
    # antara POSISI (set papertrade condong ke nama bergolak).
    AP = []
    for g in H.values():
        if g is None or len(g) < 20:
            continue
        a = _atr_pct(*(g[k].to_numpy(float) for k in ('high', 'low', 'close')))
        if len(a) and np.isfinite(a[-1]):
            AP.append(float(a[-1]))
    AP = np.sort(np.asarray(AP, dtype='float64'))
    tepi = jad.get('atr_pct_tepi') or []
    rows = []
    for kunci, (ap, jarak) in sorted(keadaan.items()):
        if AP.size:
            d = int(np.searchsorted(AP, ap, side='right') / AP.size * NDESIL)
        else:
            d = int(np.searchsorted(np.asarray(tepi, dtype='float64'), ap, side='right')) if tepi else 0
        d = max(0, min(NDESIL - 1, d))
        u, ps = {}, {}
        for Hf in UFUK:
            sel = jad['sel'].get(f'{Hf}|{d}')
            if not sel:
                continue
            u[str(Hf)] = sel['term']
            pv = p_sentuh(sel, jarak, jad['grid_mae'])
            if pv is not None:
                ps[str(Hf)] = pv
        if u:
            rows.append([kunci, {'d': d, 'atr': round(ap, 2), 'jarak': round(jarak, 2),
                                 'u': u, 'ps': ps}])
    return dict(rows=rows, ndesil=NDESIL, kuantil=list(KUANTIL), ufuk=list(UFUK),
                alam=jad.get('alam', ''),
                definisi=('Kekerapan bersyarat, BUKAN ramalan arah (REVERSE/SILING_ARAH.md: siling '
                          'ketepatan arah 5 hari 51.55% lawan asas 50.50%). u = kuantil '
                          'p10/p25/p50/p75/p90 pulangan terminal bagi bar sejarah dalam desil '
                          'atr_pct keratan rentas yang sama; ps = P(paras lorong 2 disentuh).'))


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--bina-jadual', action='store_true')
    a = ap.parse_args()
    if a.bina_jadual:
        bina_jadual()
    else:
        ap.print_help()
