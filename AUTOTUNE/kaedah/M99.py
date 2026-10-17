# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M99.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'h_ambang_3': 3,
    'nilai_3': 3,
    'n_balik': 3,
    'rolling_200': 200,
    'shift_63': 63,
}
ID = 'M99'
NAMA = 'Three Line Break'
VARIAN = 'V4 V1 + close>SMA200'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
N_BALIK = 3

def _tlb(c, N=N_BALIK, *, P=PARAM):
    """Bina carta Three Line Break hari demi hari (Kad Spesifikasi Mesin).
    Pulangkan per hari: tembus3, dasar (stop), hitambalik, h3_akhir, paras (maks ATAS N garisan terakhir selepas hari i)."""
    _p_h_ambang_3 = P['h_ambang_3']
    _p_nilai_3 = P['nilai_3']
    n = len(c)
    atas, bawah, warna = ([], [], [])
    tembus = np.zeros(n, bool)
    hb = np.zeros(n, bool)
    dasar = np.full(n, np.nan)
    h3a = np.zeros(n, int)
    paras = np.full(n, np.nan)
    asas = c[0] if n else np.nan
    for i in range(n):
        x = c[i]
        if np.isnan(x):
            continue
        if not warna:
            if np.isnan(asas):
                asas = x
            elif x > asas:
                atas.append(x)
                bawah.append(asas)
                warna.append(1)
            elif x < asas:
                atas.append(asas)
                bawah.append(x)
                warna.append(-1)
        else:
            w = warna[-1]
            k = min(N, len(warna))
            if w == 1:
                if x > atas[-1]:
                    bawah.append(atas[-1])
                    atas.append(x)
                    warna.append(1)
                elif x < min(bawah[-k:]):
                    atas.append(bawah[-1])
                    bawah.append(x)
                    warna.append(-1)
                    hb[i] = True
            elif x < bawah[-1]:
                atas.append(bawah[-1])
                bawah.append(x)
                warna.append(-1)
            elif x > max(atas[-k:]):
                h = 0
                for ww in reversed(warna):
                    if ww == -1:
                        h += 1
                    else:
                        break
                if h >= _p_h_ambang_3 and x > max(atas[-_p_nilai_3:]):
                    tembus[i] = True
                    dasar[i] = bawah[-1]
                bawah.append(atas[-1])
                atas.append(x)
                warna.append(1)
        h = 0
        for ww in reversed(warna):
            if ww == -1:
                h += 1
            else:
                break
        h3a[i] = h
        if warna:
            k = min(N, len(warna))
            paras[i] = max(atas[-k:]) if warna[-1] == -1 else np.nan
    return (tembus, dasar, hb, h3a, paras)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_n_balik = P['n_balik']
    _p_rolling_200 = P['rolling_200']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        c = g.close.values.astype(float)
        tembus, dasar, hb, h3a, paras = _tlb(c, N=_p_n_balik, P=P)
        s200 = g.close.rolling(_p_rolling_200).mean()
        g['_h3'] = h3a
        g['_paras'] = paras
        g['_s200'] = s200
        stop = pd.Series(dasar, g.index)
        sig = pd.Series(tembus, g.index) & (g.close > s200)
        langkau = (g.open.shift(-1) <= stop).fillna(False)
        g['sig'] = sig & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = pd.Series(hb, g.index)
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []
