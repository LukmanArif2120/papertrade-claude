# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M49.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'h_bahagi_2': 2,
    'ten_bahagi_2': 2,
    'rolling_9': 9,
    'rolling_26': 26,
    'rolling_52': 52,
    'shift_26': 26,
    'shift_63': 63,
}
ID = 'M49'
NAMA = 'Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun)'
VARIAN = 'V4 V1 + awan hadapan hijau (RA>RB)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230

def _ichi(g, *, P=PARAM):
    h, l = (g.high, g.low)
    ten = (h.rolling(P['rolling_9']).max() + l.rolling(P['rolling_9']).min()) / P['h_bahagi_2']
    kij = (h.rolling(P['rolling_26']).max() + l.rolling(P['rolling_26']).min()) / P['h_bahagi_2']
    ra = (ten + kij) / P['ten_bahagi_2']
    rb = (h.rolling(P['rolling_52']).max() + l.rolling(P['rolling_52']).min()) / P['h_bahagi_2']
    atas = pd.concat([ra.shift(P['shift_26']), rb.shift(P['shift_26'])], axis=1).max(axis=1, skipna=False)
    bawah = pd.concat([ra.shift(P['shift_26']), rb.shift(P['shift_26'])], axis=1).min(axis=1, skipna=False)
    return (ten, kij, ra, rb, atas, bawah)

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_shift_63 = P['shift_63']
    for g in fr.values():
        c = g.close
        ten, kij, ra, rb, atas, bawah = _ichi(g, P=P)
        keadaan = (c > atas) & (ten > kij) & (c > kij)
        sig = keadaan & ~keadaan.shift(1, fill_value=False) & (ra > rb)
        stop = kij
        bo = g.open.shift(-1)
        g['sig'] = (sig & ~(bo <= stop)).fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = c < bawah
        g['rank'] = c / c.shift(_p_shift_63) - 1
        g['_ten'] = ten
        g['_kij'] = kij
        g['_ra'] = ra
        g['_rb'] = rb
        g['_atas'] = atas
        g['_keadaan'] = keadaan

def _keadaan_esok(g, C):
    """Nilai KEADAAN dan RA>RB untuk bar esok jika tutup esok = C (andaikan high = low = C)."""
    h = g.high.values
    l = g.low.values
    ten = (max(h[-8:].max(), C) + min(l[-8:].min(), C)) / 2
    kij = (max(h[-25:].max(), C) + min(l[-25:].min(), C)) / 2
    rb = (max(h[-51:].max(), C) + min(l[-51:].min(), C)) / 2
    ra = (ten + kij) / 2
    return (ten, kij, ra, rb)
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []
