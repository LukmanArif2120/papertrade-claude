from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M11'
NAMA = 'NR7 Breakout + Volume'
VARIAN = 'V3 V1+NR7 hari dalam (NR7-ID)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210


def _nr7id(g):
    R = g.high - g.low
    nr7 = R <= R.rolling(7).min()                         # seri dikira NR7
    dalam = (g.high <= g.high.shift(1)) & (g.low >= g.low.shift(1))
    return nr7 & dalam


def sedia(fr, idx):
    for g in fr.values():
        c, h, l, o, v = g.close, g.high, g.low, g.open, g.volume
        k = _nr7id(g)
        vs20 = v.rolling(20).mean()
        stop = 0.99 * l.rolling(11).min()
        asas = k.shift(1).fillna(False).astype(bool) & (c > h.shift(1)) & (v > vs20)
        sig = asas & ~(o.shift(-1) <= stop)                  # langkau jika buka masuk <= henti
        g['_k'] = k; g['_vs20'] = vs20
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (c < c.rolling(50).mean()).fillna(False)
        g['rank'] = c / c.shift(63) - 1


def hampir(g, idx):
    """Piawaian KETAT. Syarat entry V3 (N=3):
    1 bar semalam (hari ini bagi esok) NR7; 2 bar itu hari dalam (high <= high sebelum, low >= low sebelum);
    3 PENCETUS: tutup > high bar NR7 dengan volum > SMA20 volum."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 25 or not bool(r._k):     # _k = NR7 dan hari dalam (syarat 1 dan 2)
        return None
    paras = float(r.high)
    # Andaian saya: tutup == high hari ini (jarak 0) masih belum pecah, dikira hampir.
    jarak = (paras - r.close) / r.close * 100
    if jarak < 0 or jarak > 2.0:
        return None
    vmin = g.volume.iloc[-19:].sum() / 19          # volum esok > SMA20 esok  <=>  v > jumlah 19 hari terakhir / 19
    return {'sebab': f'Hari ini NR7 (julat tersempit 7 hari) dan hari dalam (high <= {g.high.iloc[-2]:.2f}, low >= {g.low.iloc[-2]:.2f})',
            'syarat_beli': f'Tutup esok > {paras:.2f} (high hari NR7) dengan volum esok > {vmin:,.0f}',
            'pencetus': 'Pecah high NR7 + volum', 'paras': round(paras, 2), 'jarak_pct': round(float(jarak), 2),
            'syarat_dipenuhi': '2/3', 'skor': round(1 - jarak / 2, 2)}
