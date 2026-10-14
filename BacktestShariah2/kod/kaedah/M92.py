from enjin import rsi, atr
import pandas as pd, numpy as np
from numpy.lib.stride_tricks import sliding_window_view

ID = 'M92'
NAMA = 'CCI-50'
VARIAN = 'V2 V1 isyarat silang atas sifar (NAIK0)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260


def _rma_atr(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _cci(g, n=50):
    tp = ((g.high + g.low + g.close) / 3).values.astype(float)
    out = np.full(len(tp), np.nan)
    if len(tp) >= n:
        w = sliding_window_view(tp, n)
        ma = w.mean(axis=1)
        sp = np.abs(w - ma[:, None]).mean(axis=1)
        with np.errstate(divide='ignore', invalid='ignore'):
            c = np.where(sp == 0, 0.0, (tp[n - 1:] - ma) / (0.015 * sp))
        out[n - 1:] = c
    return pd.Series(out, g.index)


def sedia(fr, idx):
    for g in fr.values():
        cci = _cci(g)
        g['_cci'] = cci
        g['sig'] = (cci > 0) & (cci.shift() <= 0)
        g['stop'] = g.close - 2 * _rma_atr(g)
        g['tgt'] = np.nan
        g['exitc'] = (cci < 100) & (cci.shift() >= 100)
        g['rank'] = g.close / g.close.shift(63) - 1


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
    # Syarat entry V2 (silang atas sifar): N = 2
    #   1. CCI50 <= 0 pada bar akhir (prasyarat silang)   2. PENCETUS: CCI50 esok > 0
    # Algebra: CCI esok > 0  <=>  TP esok > MA50(TP) esok  <=>  TP esok > purata 49 TP terakhir.
    # Andaian saya: high = low = tutup esok, maka TP esok = tutup esok.
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._cci) or r._cci > 0:
        return None
    tp = ((g.high + g.low + g.close) / 3).iloc[-49:]
    if tp.isna().any() or len(tp) < 49:
        return None
    paras = float(tp.mean())
    j = (paras - r.close) / r.close * 100
    if not (0 < j <= 2.0):
        return None
    return {'sebab': f'CCI50 = {r._cci:.0f} (masih <= 0, sedia untuk silang ke atas sifar)',
            'syarat_beli': f'Tutup esok > {paras:.2f} (harga tipikal esok melebihi purata 49 harga tipikal terakhir) supaya CCI50 melintas ke atas 0',
            'pencetus': 'CCI50 silang 0', 'paras': round(float(paras), 2), 'jarak_pct': round(float(j), 2),
            'syarat_dipenuhi': '1/2', 'skor': round(float(1 - j / 2), 3)}
