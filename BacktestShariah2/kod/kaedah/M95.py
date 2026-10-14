from enjin import rsi, atr
import pandas as pd, numpy as np
from numpy.lib.stride_tricks import sliding_window_view

ID = 'M95'
NAMA = 'Nisbah Kebaharuan High 52 Minggu (Bhootra & Hur)'
VARIAN = 'V1 Dikunci: PECAH20+PTH>=0.85+HSHP<=21+tutup>SMA50'
TMAX = None
WARM = 260
ADA_HENTI = True
SILANG = False
PERLU_BAR = 280


def _rma_atr(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _hsh(h, n=252):
    v = h.values.astype(float); out = np.full(len(v), np.nan)
    if len(v) >= n:
        w = sliding_window_view(v, n)[:, ::-1]
        out[n - 1:] = w.argmax(axis=1)      # seri -> hari paling baharu
    return pd.Series(out, h.index)


def sedia(fr, idx):
    for g in fr.values():
        h252 = g.high.rolling(252).max()
        hsh = _hsh(g.high)
        hshp = hsh.shift(1); rrp = 1 - hshp / 252
        pth = g.close / h252
        s50 = g.close.rolling(50).mean()
        hh20 = g.high.rolling(20).max().shift(1)
        g['_pth'] = pth; g['_hshp'] = hshp; g['_hh20'] = hh20; g['_s50'] = s50; g['_hsh'] = hsh
        g['sig'] = (g.close > hh20) & (pth >= 0.85) & (hshp <= 21) & (g.close > s50)
        g['stop'] = g.close - 2 * _rma_atr(g)
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        roc = (g.close / g.close.shift(63) - 1).clip(-1, 30)
        # Andaian saya (ikut laporan): ROC63 hanya pemecah seri.
        g['rank'] = rrp + 0.00001 * roc


def _cari_paras(g, idx, ekor, bawah=-0.05, atas=0.02, vol=None):
    """Tutup esok minimum (dalam julat tutup*(1+bawah)..tutup*(1+atas)) yang menjadikan sig bar esok benar,
    dengan menjalankan sedia() asal pada ekor data + satu bar esok rekaan.
    Andaian saya: bar esok open=high=low=close=C; volum esok = `vol` jika diberi, jika tidak purata volum 10 hari."""
    c0 = float(g.close.iloc[-1])
    asas = g[['open', 'high', 'low', 'close', 'volume', 'turnover']].iloc[-ekor:].astype(float)
    v = float(asas.volume.iloc[-10:].mean()) if vol is None else float(vol)
    esok = asas.index[-1] + pd.offsets.BDay(1)

    def cuba(C):
        b = asas.copy()
        b.loc[esok] = [C, C, C, C, v, C * v]
        d = {'x': b}; sedia(d, {})
        return bool(d['x'].sig.iloc[-1])

    grid = np.round(np.arange(bawah, atas + 1e-9, 0.0025), 6)
    sebelum = None
    for p in grid:
        if cuba(c0 * (1 + p)):
            if sebelum is None:
                return c0 * (1 + p)
            lo, hi = c0 * (1 + sebelum), c0 * (1 + p)
            for _ in range(18):
                m = (lo + hi) / 2
                if cuba(m): hi = m
                else: lo = m
            return hi
        sebelum = p
    return None


def _jarak(paras, tutup):
    # Jarak mentah; pemanggil menolak jarak <= 0 (piawaian: 0 < jarak <= 2.0).
    return (paras - tutup) / tutup * 100


def hampir(g, idx):
    # Syarat entry V1 (dikunci): N = 4
    #   1. PTH = tutup / high 252 hari >= 0.85   2. HSHP (hari sejak high 52 minggu, bar sebelum) <= 21
    #   3. tutup > SMA50   4. PENCETUS: tutup > high tertinggi 20 hari lepas
    # Syarat 2 untuk esok: HSHP esok = HSH hari ini, maka HSH hari ini <= 21.
    r = g.iloc[-1]
    if bool(r.sig) or any(np.isnan([r._pth, r._hsh, r._hh20, r._s50])):
        return None
    if not (r._hsh <= 21 and r._pth >= 0.85 and r.close > r._s50):
        return None
    hh20_esok = float(g.high.iloc[-20:].max())
    if not (0 < (hh20_esok - r.close) / r.close * 100 <= 2.0):
        return None
    paras = _cari_paras(g, idx, ekor=300, bawah=0.0)
    if paras is None:
        return None
    j = _jarak(paras, float(r.close))
    if not (0 < j <= 2.0):
        return None
    return {'sebab': f'High 52 minggu dicapai {int(r._hsh)} hari dagangan lalu (<= 21); tutup {r._pth*100:.0f}% daripada high 52 minggu (>= 85%); tutup di atas SMA50 ({r._s50:.2f})',
            'syarat_beli': f'Tutup esok > {paras:.2f} (high 20 hari {hh20_esok:.2f})',
            'pencetus': 'Pecah HH20', 'paras': round(float(paras), 2), 'jarak_pct': round(float(j), 2),
            'syarat_dipenuhi': '3/4', 'skor': round(float(1 - j / 2), 3)}
