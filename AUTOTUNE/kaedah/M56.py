# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M56.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'shift_21': 21,
    'shift_252': 252,
    'max_16': 16,
    'open_kali_0_8': 0.8,
    'range_4': 4,
    'len_ambang_252': 252,
    'p_ambang_252': 252,
    'len_kali_0_1': 0.1,
    'nilai_8': 8,
}
ID = 'M56'
NAMA = 'Gray & Vogel Momentum Lancar (FIP)'
VARIAN = 'V4 V1 tanpa FIP (8 MOM tertinggi)'
TMAX = None
WARM = 253
ADA_HENTI = True
SILANG = True
PERLU_BAR = 253
BULAN = (2, 5, 8, 11)

def _hari_imbang(fr, *, P=PARAM):
    tarikh = pd.DatetimeIndex(sorted(set().union(*[g.index for g in fr.values()])))
    s = pd.Series(tarikh, tarikh)
    akhir = s.groupby([tarikh.year, tarikh.month]).last()
    hari = set((d for d in akhir.values if pd.Timestamp(d).month in BULAN))
    d_akhir = tarikh[-1]
    if d_akhir.month in BULAN and d_akhir != d_akhir + pd.offsets.BMonthEnd(0):
        hari.discard(np.datetime64(d_akhir))
        hari.discard(d_akhir)
    return sorted((pd.Timestamp(d) for d in hari))

def _mom(g, *, P=PARAM):
    return g.close.shift(P['shift_21']) / g.close.shift(P['shift_252']) - 1

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_max_16 = P['max_16']
    _p_open_kali_0_8 = P['open_kali_0_8']
    _p_range_4 = P['range_4']
    _p_len_ambang_252 = P['len_ambang_252']
    _p_p_ambang_252 = P['p_ambang_252']
    _p_len_kali_0_1 = P['len_kali_0_1']
    _p_nilai_8 = P['nilai_8']
    hari = _hari_imbang(fr, P=P)
    mom = {t: _mom(g, P=P) for t, g in fr.items()}
    pilih = {}
    atas = {}
    for t_ in hari:
        nilai = {}
        for t, g in fr.items():
            if t_ in g.index:
                p = g.index.get_loc(t_)
                if p >= _p_p_ambang_252:
                    v = mom[t].iloc[p]
                    if not np.isnan(v):
                        nilai[t] = v
        if not nilai:
            continue
        s = pd.Series(nilai).sort_values(ascending=False)
        n10 = max(_p_max_16, int(np.floor(_p_len_kali_0_1 * len(s))))
        atas[t_] = s.iloc[:n10]
        pilih[t_] = set(s.iloc[:_p_nilai_8].index)
    hs = pd.DatetimeIndex(list(pilih.keys()))
    for t, g in fr.items():
        ada = g.index.isin(hs)
        sig = np.zeros(len(g), bool)
        ex = np.zeros(len(g), bool)
        for i in np.where(ada)[0]:
            if t in pilih[g.index[i]]:
                sig[i] = True
            else:
                ex[i] = True
        g['sig'] = sig
        g['stop'] = _p_open_kali_0_8 * g.open.shift(-1)
        g['tgt'] = np.nan
        g['exitc'] = ex
        g['rank'] = mom[t]
        g['_mom'] = mom[t]
    akhir = {}
    for t, g in fr.items():
        if len(g) > _p_len_ambang_252 and (not np.isnan(g._mom.iloc[-1])):
            akhir[t] = (g.index[-1], g._mom.iloc[-1])
    if akhir:
        dmax = max((d for d, _ in akhir.values()))
        s = pd.Series({t: v for t, (d, v) in akhir.items() if d == dmax}).sort_values(ascending=False)
        kd = {t: k + 1 for k, t in enumerate(s.index)}
        for t, g in fr.items():
            g['_kd'] = np.nan
            g['_nuniv'] = len(s)
            if t in kd:
                g.loc[g.index[-1], '_kd'] = kd[t]
        nxt = None
        d = dmax
        for _ in range(_p_range_4):
            cand = d + pd.offsets.BMonthEnd(1)
            if cand.month in BULAN:
                nxt = cand
                break
            d = cand
        for g in fr.values():
            g.attrs['m56_imbang_seterusnya'] = nxt

def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus, 'paras': None if paras is None else round(float(paras), 4), 'jarak_pct': None if jarak is None else round(float(jarak), 2), 'syarat_dipenuhi': f'{n}/{N}', 'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []
