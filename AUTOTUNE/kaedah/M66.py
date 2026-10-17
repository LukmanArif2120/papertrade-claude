# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M66.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'akhir_999': 999,
    's50_kali_1_02': 1.02,
    'shift_10': 10,
    'rolling_50': 50,
    'i_ambang_10': 10,
    'rolling_4': 4,
    'shift_63': 63,
}
ID = 'M66'
NAMA = 'IBD Undur Pertama ke Purata 50 Hari'
VARIAN = 'V0 Sumber tulen (UNDUR+NAIK50+PUSING+BARU; tanpa PERTAMA/HIGHBARU/NIPIS)'
TMAX = None
WARM = 292
ADA_HENTI = True
SILANG = False
PERLU_BAR = 300

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_akhir_999 = P['akhir_999']
    _p_s50_kali_1_02 = P['s50_kali_1_02']
    _p_shift_10 = P['shift_10']
    _p_rolling_50 = P['rolling_50']
    _p_i_ambang_10 = P['i_ambang_10']
    _p_rolling_4 = P['rolling_4']
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        s50 = g.close.rolling(_p_rolling_50).mean()
        sentuh = g.low <= _p_s50_kali_1_02 * s50
        undur = sentuh.astype(int).rolling(_p_rolling_4, min_periods=1).max() > 0
        naik50 = s50 > s50.shift(_p_shift_10)
        pusing = (g.close > g.high.shift(1)) & (g.close > g.open) & (g.close > s50)
        calon = (undur & naik50 & pusing).values
        sig = np.zeros(len(g), bool)
        akhir = -_p_akhir_999
        for i in range(len(g)):
            if calon[i] and i - akhir > _p_i_ambang_10:
                sig[i] = True
                akhir = i
        g['_undur'] = undur
        g['_naik50'] = naik50
        g['_s50'] = s50
        g['sig'] = sig
        g['stop'] = g.low.rolling(_p_rolling_4).min()
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(_p_shift_63) - 1

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'akhir_999': ('int', 500, 1998),
    's50_kali_1_02': ('float', 0.51, 1.53),
    'shift_10': ('int', 5, 20),
    'rolling_50': ('int', 25, 100),
    'rolling_4': ('int', 2, 8),
    'shift_63': ('int', 32, 126),
}
TALA = ['rolling_4', 'rolling_50', 'akhir_999', 's50_kali_1_02', 'shift_10']
