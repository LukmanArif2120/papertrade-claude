# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M18.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'ema_a1_9': 9,
    'ema_a1_21': 21,
    'rr_ambang_2': 2,
}
ID = 'M18'
NAMA = 'EMA9/21 Pullback'
VARIAN = 'V2 V1 Model A sahaja'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230
ema = lambda s, k, *, P=PARAM: s.ewm(span=k, adjust=False).mean()

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_ema_a1_9 = P['ema_a1_9']
    _p_ema_a1_21 = P['ema_a1_21']
    _p_rr_ambang_2 = P['rr_ambang_2']
    for g in fr.values():
        o, h, l, c = (g.open, g.high, g.low, g.close)
        E9, E21 = (ema(c, _p_ema_a1_9), ema(c, _p_ema_a1_21))
        ATH = h.cummax().shift(1)
        A = (l < l.shift()) & (c > l.shift())
        RR = (ATH - c) / (c - l)
        sig = (c > E21) & (l <= E9) & A & (ATH > c) & (E9 > E21) & (c > o) & (RR >= _p_rr_ambang_2)
        lk = ((o.shift(-1) <= l) | (o.shift(-1) >= ATH)).fillna(False)
        g['_E9'] = E9
        g['_E21'] = E21
        g['_ATH'] = ATH
        g['sig'] = (sig & ~lk).fillna(False)
        g['stop'] = l
        g['tgt'] = ATH
        g['exitc'] = c < E21
        g['rank'] = RR
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'ema_a1_9': ('int', 4, 18),
    'ema_a1_21': ('int', 10, 42),
    'rr_ambang_2': ('int', 1, 3),
}
TALA = ['ema_a1_21', 'ema_a1_9', 'rr_ambang_2']
