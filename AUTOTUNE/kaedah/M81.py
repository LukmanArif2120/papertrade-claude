# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M81.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
# Dibaiki (pandang ke hadapan): 18 Okt 2026 selepas AUTOTUNE/hasil/AUDIT_M81.md. `_exit_ekor` dahulu menanda
#   exitc[j-1] apabila rendah[j] <= paras henti mengekor (enjin keluar pada buka j dengan pengetahuan hari j).
#   Kini exitc[j] = True apabila tutup[j] <= paras henti mengekor (paras dikira daripada tutup hingga j-1), dan
#   enjin keluar pada buka j+1. Henti awal (stop) tidak berubah. Salinan ini tidak lagi setara bait demi bait
#   dengan BacktestShariah2/kod/kaedah/M81.py (DIBAIKI dalam KESETARAAN.md).
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'a20_kali_3': 3,
    'tt_kali_0_75': 0.75,
    'rma_atr_20': 20,
    'close_ambang_5': 5,
    'nilai20_ambang_50000000': 50000000,
    'rolling_100': 100,
    'rolling_25': 25,
    'rolling_50': 50,
    'rolling_20': 20,
    'shift_200': 200,
}
ID = 'M81'
NAMA = 'Bensdorp Long Trend High Momentum'
VARIAN = 'V4 V1 henti awal 3xATR20'
TMAX = None
WARM = 201
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210

def _rma_atr(g, n=20, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _exit_ekor(g, sig, a20, warm, *, P=PARAM):
    """(Dibaiki 18 Okt 2026: lihat pengepala fail; perenggan asal di bawah tidak lagi tepat bagi exitc.)
    Andaian saya: enjin v1.2 hanya ada henti tetap. Henti mengekor 25% (0.75 x tutup tertinggi sejak masuk,
    TT bermula = buka_masuk) disimulasi di sini mengikut gelung trades() enjin; hari keluar mengekor
    ditandakan sebagai exitc pada hari SEBELUMNYA supaya enjin keluar pada buka hari itu (masa keluar sama,
    harga keluar = buka, bukan paras henti). Henti awal buka_masuk-3xATR20 diserah kepada enjin melalui stop.
    AMARAN: exitc[j-1] bergantung pada rendah_j (pandang ke hadapan 1 hari) — HANYA untuk meniru jujukan
    dagangan backtest (trades_ekor). Lajur sig tidak bergantung padanya dan bebas pandang ke hadapan.
    Enjin v1.2 tidak dapat keluar pada paras henti mengekor yang berubah harian, jadi harga keluar tidak tepat."""
    _p_a20_kali_3 = P['a20_kali_3']
    _p_tt_kali_0_75 = P['tt_kali_0_75']
    o, h, l, c = (g.open.values, g.high.values, g.low.values, g.close.values)
    n = len(g)
    ex = np.zeros(n, bool)
    i = warm
    while i < n - 1:
        if not sig[i]:
            i += 1
            continue
        e = o[i + 1]
        sp0 = e - _p_a20_kali_3 * a20[i]
        if np.isnan(sp0):
            sp0 = -np.inf
        tt = e
        j = i + 1
        jx = n - 1
        while j < n:
            if j > i + 1:
                tt = max(tt, c[j - 1])
            tr = _p_tt_kali_0_75 * tt
            if j > i + 1 and o[j] <= sp0 or l[j] <= sp0:   # henti awal (enjin, lajur stop)
                jx = j
                break
            if c[j] <= tr and j + 1 < n:                     # henti mengekor atas tutup: keluar buka j+1
                ex[j] = True
                jx = j + 1
                break
            j += 1
        i = jx + 1
    return ex

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_rma_atr_20 = P['rma_atr_20']
    _p_close_ambang_5 = P['close_ambang_5']
    _p_nilai20_ambang_50000000 = P['nilai20_ambang_50000000']
    _p_a20_kali_3 = P['a20_kali_3']
    _p_rolling_25 = P['rolling_25']
    _p_rolling_50 = P['rolling_50']
    _p_rolling_20 = P['rolling_20']
    _p_shift_200 = P['shift_200']
    spy = idx['SPY'].close
    pas = spy > spy.rolling(P['rolling_100']).mean()
    for g in fr.values():
        s25 = g.close.rolling(_p_rolling_25).mean()
        s50 = g.close.rolling(_p_rolling_50).mean()
        nilai20 = (g.close * g.volume).rolling(_p_rolling_20).mean()
        cair = (g.close >= _p_close_ambang_5) & (nilai20 > _p_nilai20_ambang_50000000)
        mkt = pas.reindex(g.index, method='ffill').fillna(False).astype(bool)
        sig = (s25 > s50) & cair & mkt
        a20 = _rma_atr(g, _p_rma_atr_20, P=P)
        g['_s25'] = s25
        g['_s50'] = s50
        g['_cair'] = cair
        g['_mkt'] = mkt
        g['sig'] = sig
        g['stop'] = g.close - _p_a20_kali_3 * a20
        g['tgt'] = np.nan
        g['exitc'] = _exit_ekor(g, sig.values, a20.values, WARM, P=P)
        g['rank'] = g.close / g.close.shift(_p_shift_200) - 1
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {
    'a20_kali_3': ('float', 1.5, 4.5),
    'tt_kali_0_75': ('float', 0.375, 0.99),
    'rma_atr_20': ('int', 10, 40),
    'close_ambang_5': ('int', 2, 8),
    'nilai20_ambang_50000000': ('int', 25000000, 75000000),
    'rolling_25': ('int', 12, 50),
    'rolling_50': ('int', 25, 100),
    'rolling_20': ('int', 10, 40),
    'shift_200': ('int', 100, 400),
}
TALA = ['a20_kali_3', 'tt_kali_0_75', 'rma_atr_20', 'close_ambang_5', 'nilai20_ambang_50000000', 'rolling_25']
