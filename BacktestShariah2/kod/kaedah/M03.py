from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M03'
NAMA = 'BB Break + Divergence RSI'
VARIAN = 'V1 Spesifikasi dikunci'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 240


def _kira(g):
    o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values
    n = len(g)
    bm = g.close.rolling(20).mean(); sd = g.close.rolling(20).std(ddof=0)
    BBL = (bm - 2 * sd).values; BBU = (bm + 2 * sd)
    RS = rsi(g.close, 14).values
    sg = np.zeros(n, bool); st = np.full(n, np.nan); rk = np.zeros(n)
    setup = np.zeros(n, bool); L2v = np.full(n, np.nan)       # divergence terbentuk (tanpa pencetus lilin)
    for i in range(31, n):
        L2 = i - 5 + int(np.argmin(l[i - 5:i + 1]))
        K = [k for k in range(i - 30, i - 5) if c[k] < BBL[k]]
        if not K: continue
        L1 = K[int(np.argmin([l[k] for k in K]))]
        if any(c[q] > BBL[q] for q in range(L1 + 1, L2)) and l[L2] < l[L1] and RS[L2] > RS[L1]:
            setup[i] = True; L2v[i] = l[L2]
            if c[i] > h[i - 1] and c[i] > o[i]:
                sg[i] = True; st[i] = 0.99 * l[L2]; rk[i] = RS[L2] - RS[L1]
    return sg, st, rk, BBU, setup, L2v


def sedia(fr, idx):
    for g in fr.values():
        sg, st, rk, BBU, setup, L2v = _kira(g)
        stop = pd.Series(st, g.index)
        bm = g.open.shift(-1)
        sig = pd.Series(sg, g.index) & ((bm > stop) | bm.isna())   # langkau jika buka_masuk <= henti
        g['_setup'] = setup; g['_l2'] = L2v
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = BBU
        g['exitc'] = False
        g['rank'] = rk



def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def hampir(g, idx):
    """Syarat entry V1 (N=5), dinilai untuk bar esok i: [1] K wujud (tutup < BBL(20,2) pada i-30..i-6)
       [2] tutup kembali > BBL antara L1 dan L2 [3] low_L2 < low_L1 [4] RSI14_L2 > RSI14_L1
       [5] PENCETUS lilin momentum: tutup esok > high hari ini DAN tutup esok > buka esok."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 40:
        return None
    o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values
    n = len(g)                                 # indeks bar esok = n
    bm = g.close.rolling(20).mean(); sd = g.close.rolling(20).std(ddof=0)
    BBL = (bm - 2 * sd).values; RS = rsi(g.close, 14).values
    # Andaian saya: low esok tidak lebih rendah daripada low terendah 5 hari terakhir (L2 kekal dalam n-5..n-1)
    L2 = n - 5 + int(np.argmin(l[n - 5:n]))
    K = [k for k in range(n - 30, n - 5) if c[k] < BBL[k]]
    if not K:
        return None
    L1 = K[int(np.argmin([l[k] for k in K]))]
    if not (any(c[q] > BBL[q] for q in range(L1 + 1, L2)) and l[L2] < l[L1] and RS[L2] > RS[L1]):
        return None
    paras = float(h[-1]); c0 = float(c[-1])
    jarak = (paras - c0) / c0 * 100
    if jarak > 2.0:
        return None
    return _hasil(f'Kaki 1 tutup bawah band bawah BB(20,2) (low {l[L1]:.2f}); kembali ke dalam band; kaki 2 low lebih rendah {l[L2]:.2f} tetapi RSI14 lebih tinggi ({RS[L2]:.1f} > {RS[L1]:.1f})',
                  f'Tutup esok > {paras:.2f} (high hari ini) DAN tutup esok > buka esok; langkau jika buka esok <= henti {0.99*l[L2]:.2f}',
                  'Lilin momentum naik', paras, jarak, 4, 5)
