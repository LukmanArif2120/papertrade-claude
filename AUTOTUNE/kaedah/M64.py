# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M64.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'ketat': 0.015,
    'c_ambang_0_2': 0.2,
    'concat_tambah_0_1': 0.1,
    'shift_2': 2,
    'shift_10': 10,
    'sah': 15,
    'piv_kali_0_92': 0.92,
    'rolling_50': 50,
    'shift_63': 63,
}
ID = 'M64'
NAMA = "O'Neil Tiga Minggu Ketat"
VARIAN = 'V5 V1 henti 0.92xPIVOT'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
KETAT, SAH = (0.015, 15)

def _mingguan(g, *, P=PARAM):
    pos = pd.Series(np.arange(len(g)), g.index)
    wk = g.index.to_period('W-SUN')
    w = pd.DataFrame({'c': g.close.groupby(wk).last(), 'h': g.high.groupby(wk).max(), 'l': g.low.groupby(wk).min(), 'e': pos.groupby(wk).last()})
    c = w.c
    ketat = ((c.shift(1) / c.shift(P['shift_2']) - 1).abs() <= P['ketat']) & ((c / c.shift(1) - 1).abs() <= P['ketat'])
    naik = c.shift(P['shift_2']) / c.shift(P['shift_10']) - 1 >= P['c_ambang_0_2']
    w['corak'] = ketat & naik
    w['pv'] = pd.concat([w.h, w.h.shift(1), w.h.shift(P['shift_2'])], axis=1).max(axis=1) + P['concat_tambah_0_1']
    w['lowc'] = pd.concat([w.l, w.l.shift(1), w.l.shift(P['shift_2'])], axis=1).min(axis=1)
    return w

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_sah = P['sah']
    _p_piv_kali_0_92 = P['piv_kali_0_92']
    _p_rolling_50 = P['rolling_50']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        n = len(g)
        cl = g.close.values
        w = _mingguan(g, P=P)
        cw = w[w.corak]
        ev = cw.e.values.astype(int)
        pv = cw.pv.values
        piv = np.full(n, np.nan)
        eact = np.full(n, -1)
        k = -1
        for i in range(n):
            while k + 1 < len(ev) and ev[k + 1] < i:
                k += 1
            if k >= 0 and 1 <= i - ev[k] <= _p_sah:
                piv[i] = pv[k]
                eact[i] = ev[k]
        sig = np.zeros(n, bool)
        for i in range(n):
            if eact[i] < 0 or not cl[i] > piv[i]:
                continue
            e = eact[i]
            if (cl[e + 1:i] > piv[i]).any():
                continue
            sig[i] = True
        s50 = g.close.rolling(_p_rolling_50).mean()
        g['_piv'] = piv
        g['_e'] = eact
        g['sig'] = pd.Series(sig, g.index) & (g.close > s50)
        g['stop'] = _p_piv_kali_0_92 * g['_piv']
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []
