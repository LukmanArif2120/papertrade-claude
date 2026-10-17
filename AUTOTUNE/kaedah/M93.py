# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M93.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'high_bahagi_3': 3,
    'pos_tolak_100': 100,
    'pos_bahagi_100': 100,
    'where_a1_100_0': 100.0,
    'rolling_20': 20,
    'sd_kali_2': 2,
    'where_a1_0_5': 0.5,
    'n_ambang_2': 2,
    'i_ambang_2': 2,
    'i_tolak_2': 2,
    'mfi_10': 10,
    'psar_step_0_02': 0.02,
    'psar_mx_0_2': 0.2,
    'pb_ambang_0_8': 0.8,
    'mfi_ambang_80': 80,
    'pb_ambang_0_2': 0.2,
    'mfi_ambang_20': 20,
    'rma_atr_kali_2': 2,
    'shift_63': 63,
    'rma_atr_14': 14,
}
ID = 'M93'
NAMA = 'Bollinger Kaedah II: %b + MFI'
VARIAN = 'V2 V1, keluar LEMAH (%b<0.20 & MFI10<20)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260

def _rma_atr(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _psar(g, step=0.02, mx=0.2, *, P=PARAM):
    _p_i_ambang_2 = P['i_ambang_2']
    _p_i_tolak_2 = P['i_tolak_2']
    h, l = (g.high.values.astype(float), g.low.values.astype(float))
    n = len(h)
    out = np.full(n, np.nan)
    if n < P['n_ambang_2']:
        return pd.Series(out, g.index)
    up = True
    af = step
    ep = h[0]
    sar = l[0]
    out[0] = sar
    for i in range(1, n):
        sar = sar + af * (ep - sar)
        if up:
            sar = min(sar, l[i - 1], l[i - _p_i_tolak_2] if i >= _p_i_ambang_2 else l[i - 1])
            if l[i] < sar:
                up = False
                sar = ep
                ep = l[i]
                af = step
            elif h[i] > ep:
                ep = h[i]
                af = min(af + step, mx)
        else:
            sar = max(sar, h[i - 1], h[i - _p_i_tolak_2] if i >= _p_i_ambang_2 else h[i - 1])
            if h[i] > sar:
                up = True
                sar = ep
                ep = h[i]
                af = step
            elif l[i] < ep:
                ep = l[i]
                af = min(af + step, mx)
        out[i] = sar
    return pd.Series(out, g.index)

def _mfi(g, n=10, *, P=PARAM):
    tp = (g.high + g.low + g.close) / P['high_bahagi_3']
    aw = tp * g.volume
    d = tp.diff()
    pos = aw.where(d > 0, 0.0).rolling(n).sum()
    neg = aw.where(d < 0, 0.0).rolling(n).sum()
    m = P['pos_tolak_100'] - P['pos_bahagi_100'] / (1 + pos / neg)
    return m.where(neg != 0, P['where_a1_100_0']).where(pos.notna())

def _pb(c, *, P=PARAM):
    s = c.rolling(P['rolling_20']).mean()
    sd = c.rolling(P['rolling_20']).std(ddof=0)
    ja, jb = (s + P['sd_kali_2'] * sd, s - P['sd_kali_2'] * sd)
    return ((c - jb) / (ja - jb)).where(ja != jb, P['where_a1_0_5']).where(s.notna())

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_mfi_10 = P['mfi_10']
    _p_psar_step_0_02 = P['psar_step_0_02']
    _p_psar_mx_0_2 = P['psar_mx_0_2']
    _p_pb_ambang_0_8 = P['pb_ambang_0_8']
    _p_mfi_ambang_80 = P['mfi_ambang_80']
    _p_pb_ambang_0_2 = P['pb_ambang_0_2']
    _p_mfi_ambang_20 = P['mfi_ambang_20']
    _p_rma_atr_kali_2 = P['rma_atr_kali_2']
    _p_shift_63 = P['shift_63']
    _p_rma_atr_14 = P['rma_atr_14']
    for g in fr.values():
        pb = _pb(g.close, P=P)
        mfi = _mfi(g, _p_mfi_10, P=P)
        ps = _psar(g, step=_p_psar_step_0_02, mx=_p_psar_mx_0_2, P=P)
        kuat = (pb > _p_pb_ambang_0_8) & (mfi > _p_mfi_ambang_80)
        g['_pb'] = pb
        g['_mfi'] = mfi
        g['sig'] = kuat & ~kuat.shift(fill_value=False)
        g['stop'] = np.where(ps < g.close, ps, g.close - _p_rma_atr_kali_2 * _rma_atr(g, n=_p_rma_atr_14, P=P))
        g['tgt'] = np.nan
        g['exitc'] = (pb < _p_pb_ambang_0_2) & (mfi < _p_mfi_ambang_20)
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

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
        d = {'x': b}
        sedia(d, {})
        return bool(d['x'].sig.iloc[-1])
    grid = np.round(np.arange(bawah, atas + 1e-09, 0.0025), 6)
    sebelum = None
    for p in grid:
        if cuba(c0 * (1 + p)):
            if sebelum is None:
                return c0 * (1 + p)
            lo, hi = (c0 * (1 + sebelum), c0 * (1 + p))
            for _ in range(18):
                m = (lo + hi) / 2
                if cuba(m):
                    hi = m
                else:
                    lo = m
            return hi
        sebelum = p
    return None

def _jarak(paras, tutup):
    return (paras - tutup) / tutup * 100
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'rolling_20': ('int', 10, 40),
    'sd_kali_2': ('float', 1.0, 3.0),
    'where_a1_0_5': ('float', 0.25, 0.75),
    'mfi_10': ('int', 5, 20),
    'psar_step_0_02': ('float', 0.01, 0.03),
    'psar_mx_0_2': ('float', 0.1, 0.3),
    'pb_ambang_0_8': ('float', 0.4, 0.99),
    'mfi_ambang_80': ('int', 40, 99),
    'pb_ambang_0_2': ('float', 0.1, 0.3),
    'mfi_ambang_20': ('int', 10, 30),
    'rma_atr_kali_2': ('int', 2, 4),
    'shift_63': ('int', 32, 126),
    'rma_atr_14': ('int', 7, 28),
}
TALA = ['psar_step_0_02', 'psar_mx_0_2', 'pb_ambang_0_2', 'mfi_ambang_20', 'rolling_20', 'sd_kali_2']
