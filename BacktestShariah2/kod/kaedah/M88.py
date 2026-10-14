from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M88'
NAMA = "O'Neil Shakeout +3"
VARIAN = 'V1 Dikunci (BELI 1.10xL1; vol>VOL50; henti max(L2;0.92x masuk); keluar tutup<low20)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260


def _argmin_baru(a):
    """indeks minimum; jika seri, yang paling baharu"""
    return len(a) - 1 - int(np.argmin(a[::-1]))


def _w(g):
    h, l = g.high.values, g.low.values; n = len(g)
    L1 = np.full(n, np.nan); L2 = np.full(n, np.nan); TG = np.full(n, np.nan)
    for i in range(16, n):
        a = i - 15
        d2 = a + _argmin_baru(l[a:i])
        s, e = d2 - 40, d2 - 5
        if s < 0 or e < s: continue
        d1 = s + _argmin_baru(l[s:e + 1])
        L1[i] = l[d1]; L2[i] = l[d2]
        TG[i] = h[d1 + 1:d2].max() if d2 - d1 > 1 else np.nan
    return L1, L2, TG


def sedia(fr, idx):
    for g in fr.values():
        L1, L2, TG = _w(g)
        L1 = pd.Series(L1, g.index); L2 = pd.Series(L2, g.index); TG = pd.Series(TG, g.index)
        bentuk = (L2 < L1) & (L2 >= 0.90 * L1) & (TG >= 1.10 * L1)
        beli = 1.10 * L1
        naik = (g.close > beli) & (g.close.shift() <= beli)       # Andaian (laporan): BELI hari i untuk i-1 juga
        vol50 = g.volume.rolling(50).mean().shift(1)
        g['_bentuk'] = bentuk; g['_beli'] = beli; g['_L1'] = L1; g['_L2'] = L2; g['_tg'] = TG; g['_v50'] = vol50
        g['sig'] = bentuk & naik & (g.volume > vol50)
        bm = g.open.shift(-1).fillna(g.close)   # buka_masuk; Andaian saya: bar terakhir guna tutup_i
        st = np.maximum(L2, 0.92 * bm)
        g['stop'] = st.where(bm > L2, 0.92 * bm)
        g['tgt'] = np.nan
        g['exitc'] = g.close < g.low.rolling(20).min().shift(1)
        g['rank'] = g.close / g.close.shift(63) - 1


def hampir(g, idx):
    """Syarat entry V1 (sig), dikira dengan tetingkap ESOK: (1) L2 < L1; (2) L2 >= 0.90 x L1; (3) puncak tengah >= 1.10 x L1;
    (4) tutup hari ini <= BELI esok; (5) tutup esok > BELI (1.10 x L1) DENGAN volum esok > VOL50 (pencetus). N = 5."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 60:
        return None
    h, l = g.high.values, g.low.values; n = len(g)
    i = n                                   # bar esok (hipotesis); tetingkap l[i-15:i] sudah diketahui hari ini
    a = i - 15; d2 = a + _argmin_baru(l[a:i]); s, e = d2 - 40, d2 - 5
    if s < 0 or e < s:
        return None
    d1 = s + _argmin_baru(l[s:e + 1]); L1, L2 = l[d1], l[d2]
    if d2 - d1 <= 1:
        return None
    TG = h[d1 + 1:d2].max()
    if not (L2 < L1 and L2 >= 0.90 * L1 and TG >= 1.10 * L1):
        return None
    beli = 1.10 * L1
    if not (r.close <= beli):
        return None
    jarak = (beli - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    v50 = float(g.volume.iloc[-50:].mean())   # VOL50 esok = purata 50 hari berakhir hari ini
    return {'sebab': f'Bentuk W: dasar kedua {L2:.2f} menembusi dasar pertama {L1:.2f} tidak lebih 10%; puncak tengah {TG:.2f} >= 1.10 x L1; tutup belum melepasi titik beli',
            'syarat_beli': f'Tutup esok > {beli:.2f} (1.10 x L1) dengan volum esok > {v50:,.0f} (purata 50 hari)',
            'pencetus': 'Tutup > 1.10xL1 + volum', 'paras': float(round(beli, 4)), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '4/5', 'skor': float(round(1 - jarak / 2, 2))}
