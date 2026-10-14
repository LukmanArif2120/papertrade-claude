from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M25'
NAMA = 'VWAP Wave (proksi harian)'
VARIAN = 'V2 V1 tanpa sasaran'
TMAX = 20
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
N = 20


def _vw(g, n=N):
    tp = (g.high + g.low + g.close) / 3; v = g.volume
    vw = (tp * v).rolling(n).sum() / v.rolling(n).sum()
    TP, V, VW = tp.values, v.values.astype(float), vw.values
    sd = np.full(len(g), np.nan)
    for i in range(n - 1, len(g)):
        w = V[i - n + 1:i + 1]
        if w.sum() > 0:
            sd[i] = np.sqrt((w * (TP[i - n + 1:i + 1] - VW[i]) ** 2).sum() / w.sum())
    return vw, pd.Series(vw.values + sd, g.index)


def _penerimaan(C, UB):
    """Untuk setiap i: indeks A terkini dalam [i-10, i-1] (hari penerimaan) dengan DISC & FIRST masih sah, atau -1."""
    n = len(C); out = np.full(n, -1)
    acc = np.zeros(n, bool)
    for a in range(2, n):
        acc[a] = C[a] > UB[a] and C[a - 1] > UB[a - 1] and C[a - 2] <= UB[a - 2]
    return acc


def sedia(fr, idx):
    for g in fr.values():
        O, H, L, C, V = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close', 'volume']]
        vw, ub = _vw(g); UB = ub.values; VW = vw.values
        vs20 = g.volume.rolling(20).mean().values
        acc = _penerimaan(C, UB)
        n = len(g); sg = np.zeros(n, bool); pers = np.zeros(n, bool)
        for i in range(12, n):
            # A paling terkini dalam 10 hari, dengan DISC (tiada tutup <= UB sejak A) dan FIRST (tiada low <= UB A+1..i-1)
            for A in range(i - 1, i - 11, -1):
                if acc[A]:
                    ok = all(C[t] > UB[t] for t in range(A, i)) and all(L[t] > UB[t] for t in range(A + 1, i))
                    pers[i] = ok
                    sg[i] = ok and L[i] <= UB[i] and C[i] > UB[i] and C[i] > O[i] and V[i] >= 0.7 * vs20[i]
                    break
        # Persediaan untuk ESOK (hampir): A dalam [i-9, i], semua tutup A..i > UB, tiada low <= UB A+1..i
        pe = np.zeros(n, bool)
        for i in range(n - 1, max(n - 2, 11), -1):
            for A in range(i, i - 10, -1):
                if acc[A]:
                    pe[i] = all(C[t] > UB[t] for t in range(A, i + 1)) and all(L[t] > UB[t] for t in range(A + 1, i + 1))
                    break
        stop = 0.99 * g.low
        sig = pd.Series(sg, g.index) & ~(g.open.shift(-1) <= stop)
        g['_pers'] = pe; g['_ub'] = UB
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = pd.Series(C < VW, g.index)
        g['rank'] = g.close / g.close.shift(63) - 1


def hampir(g, idx):
    # Piawaian ketat: syarat entry V2 (= V1) = (1) hari penerimaan A dalam 10 hari (tetingkap esok),
    # (2) DISC: tiada tutup <= UB sejak A, (3) FIRST: tiada low <= UB sejak A+1,
    # (4) PENCETUS ujian pertama: low <= UB, tutup > UB, tutup > buka, volume >= 0.7 x SMA20 volume.
    r = g.iloc[-1]
    if bool(r.sig) or not bool(r._pers):
        return None
    ub = float(r._ub)   # Andaian saya: UB esok dianggarkan = UB hari ini (UB esok bergantung pada bar esok)
    c = float(r.close)
    # Pencetus ialah undur ke paras UB: jarak = (tutup - UB)/tutup x 100 (arah ke bawah)
    jarak = (c - ub) / c * 100
    if not (0 < jarak <= 2.0):
        return None
    v19 = float(g.volume.iloc[-19:].sum())
    vmin = 0.035 * v19 / 0.965   # volume esok >= 0.7 x purata 20 hari (termasuk volume esok)
    return {'sebab': 'Penerimaan atas jalur atas VWAP20 (2 tutup berturut > UB) dalam 10 hari; tiada tutup <= UB sejak itu; tiada ujian semula UB lagi',
            'syarat_beli': f'Esok: low <= {ub:.2f} (UB VWAP20), tutup > {ub:.2f} dan tutup > buka, volume >= {vmin:,.0f}',
            'pencetus': 'ujian pertama UB', 'paras': round(ub, 4), 'jarak_pct': round(jarak, 2),
            'syarat_dipenuhi': '3/4', 'skor': round(1 - jarak / 2, 3)}
