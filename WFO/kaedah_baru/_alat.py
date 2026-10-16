# Alat indikator bersama modul calon K145+ (WFO sahaja; bukan dalam imbasan harian).
# Konvensyen: pencetus "beli tembus paras X" dimodelkan sebagai TUTUP hari i > X (masuk buka hari i+1),
# selaras kriteria saringan "mekanikal pada tutup harian". Semua nilai hari i guna data <= i sahaja.
import numpy as np, pandas as pd

sma = lambda s, n: s.rolling(n).mean()
ema = lambda s, n: s.ewm(span=n, adjust=False).mean()

def stoch_k(g, n, d=3):
    """%K perlahan: %K pantas (n) dilicinkan SMA d."""
    lo, hi = g.low.rolling(n).min(), g.high.rolling(n).max()
    k = 100 * (g.close - lo) / (hi - lo)
    return k.rolling(d).mean()

def macd_hist(c, a=12, b=26, s=9):
    m = ema(c, a) - ema(c, b)
    return m - ema(m, s)

def cci(h, l, c, n=20):
    tp = (h + l + c) / 3; ma = tp.rolling(n).mean()
    md = tp.rolling(n).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
    return (tp - ma) / (0.015 * md)

def mingguan_lalu(g, fungsi):
    """Nilai minggu kalendar LEPAS (Isnin–Jumaat) yang sudah lengkap, dipetakan ke setiap hari minggu ini."""
    wk = g.index.to_period('W-FRI')
    nilai = fungsi(g.groupby(wk))                       # Series diindeks minggu
    return pd.Series(wk.map(lambda p: nilai.get(p - 1, np.nan)), g.index, dtype=float)

def cci_mingguan_lalu(g, n=20):
    wk = g.index.to_period('W-FRI')
    w = g.groupby(wk).agg(high=('high', 'max'), low=('low', 'min'), close=('close', 'last'))
    cw = cci(w.high, w.low, w.close, n)
    return pd.Series(wk.map(lambda p: cw.get(p - 1, np.nan)), g.index, dtype=float)

def langkau(g, stop):
    """Langkau jika buka esok <= henti (konvensyen projek)."""
    return (g.open.shift(-1) <= stop).fillna(False)

def siap_lajur(g, sig, stop, exitc=None, tgt=None):
    g['sig'] = sig.fillna(False).astype(bool)
    g['stop'] = stop
    g['tgt'] = np.nan if tgt is None else tgt
    g['exitc'] = False if exitc is None else exitc.fillna(False).astype(bool)
    g['rank'] = g.close / g.close.shift(63) - 1          # ROC63, kunci keutamaan slot (konvensyen projek)
