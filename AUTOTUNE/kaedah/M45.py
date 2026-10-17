# Salinan berparameter (AUTOTUNE) — sumber: BacktestShariah2/kod/kaedah/M45.py
# Dijana oleh AUTOTUNE/kaedah/ekstrak_param.py dan pilih_julat.py; jangan sunting tangan.
import os as _os, sys as _sys
_D = _os.path.dirname(_os.path.abspath(__file__))
for _p in (_os.path.normpath(_os.path.join(_D, '..', '..', 'BacktestShariah2', 'kod')), _D):
    if _p not in _sys.path: _sys.path.insert(0, _p)
from enjin import rsi, atr
import pandas as pd, numpy as np
PARAM = {
    'slot': 8,
    'hari_sejak_max_ambang_21': 21,
    'rma_atr_kali_3': 3,
    'r_kali_1em06': 1e-06,
    'len_kali_0_3': 0.3,
    'rolling_252': 252,
    'shift_126': 126,
    'hari_sejak_max_252': 252,
    'clip_a1_50': 50,
    'rma_atr_14': 14,
    'clip_50': 50,
    'tmax': 126,
}
ID = 'M45'
NAMA = 'High 52 Minggu (George & Hwang)'
VARIAN = 'V4 V1 + high 52 minggu dicapai dalam 21 hari'
TMAX = 126
WARM = 252
ADA_HENTI = True
SILANG = True
PERLU_BAR = 260
SLOT = 8

def _rma_atr(g, n=14, *, P=PARAM):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()

def _hari_sejak_max(c, n=252, *, P=PARAM):
    """Bilangan hari sejak kali TERAKHIR tutup menyamai maks 252 hari (termasuk hari ini)."""
    v = c.values.astype(float)
    out = np.full(len(v), np.nan)
    if len(v) >= n:
        W = np.lib.stride_tricks.sliding_window_view(v, n)[:, ::-1]
        out[n - 1:] = np.argmax(W == W.max(axis=1, keepdims=True), axis=1)
    return pd.Series(out, c.index)

def _keluar(g, i, sp, *, P=PARAM):
    """Tiru enjin: hari keluar bagi dagangan isyarat i (henti tetap sp, tmax 126, tiada exitc)."""
    o, l = (g.open.values, g.low.values)
    n = len(g)
    j = i + 1
    while j < n:
        if j > i + 1 and o[j] <= sp:
            return j
        if l[j] <= sp:
            return j
        if j - i >= TMAX:
            return j
        j += 1
    return n - 1

def _hb(dates, *, P=PARAM):
    """Hari dagangan terakhir setiap bulan dalam kalendar gabungan; bulan terakhir hanya jika tarikh akhir = hari bekerja terakhir bulan."""
    d = pd.DatetimeIndex(dates)
    s = pd.Series(d, index=d)
    last = s.groupby(d.to_period('M')).max()
    hb = set(last.values[:-1])
    if d[-1] == d[-1] + pd.offsets.BMonthEnd(0):
        hb.add(d[-1].to_datetime64())
    return sorted((pd.Timestamp(x) for x in hb))

def sedia(fr, idx, P=None):
    P = {**PARAM, **(P or {})}
    _p_slot = P['slot']
    _p_hari_sejak_max_ambang_21 = P['hari_sejak_max_ambang_21']
    _p_rma_atr_kali_3 = P['rma_atr_kali_3']
    _p_r_kali_1em06 = P['r_kali_1em06']
    _p_rolling_252 = P['rolling_252']
    _p_shift_126 = P['shift_126']
    _p_hari_sejak_max_252 = P['hari_sejak_max_252']
    _p_len_kali_0_3 = P['len_kali_0_3']
    _p_clip_a1_50 = P['clip_a1_50']
    _p_rma_atr_14 = P['rma_atr_14']
    _p_clip_50 = P['clip_50']
    nh = {}
    r126 = {}
    baru = {}
    stop = {}
    for t, g in fr.items():
        c = g.close
        h252 = c.rolling(_p_rolling_252).max()
        nh[t] = c / h252
        r126[t] = c / c.shift(_p_shift_126) - 1
        baru[t] = _hari_sejak_max(c, n=_p_hari_sejak_max_252, P=P) <= _p_hari_sejak_max_ambang_21
        stop[t] = c - _p_rma_atr_kali_3 * _rma_atr(g, n=_p_rma_atr_14, P=P)
        g['_nh'] = nh[t]
        g['_baru'] = baru[t]
    NH = pd.DataFrame(nh)
    R = pd.DataFrame(r126)
    BA = pd.DataFrame(baru).fillna(False)
    ST = pd.DataFrame(stop)
    hbs = _hb(NH.index, P=P)
    sig = {t: pd.Series(False, g.index) for t, g in fr.items()}
    pos = {t: {d: i for i, d in enumerate(g.index)} for t, g in fr.items()}
    pegang = {}
    akhir_keluar = {}
    calon_akhir = []
    for d in hbs:
        nhd = NH.loc[d].dropna()
        if nhd.empty:
            continue
        k = int(np.floor(_p_len_kali_0_3 * len(nhd)))
        dfc = pd.DataFrame({'nh': nhd, 'r': R.loc[d].reindex(nhd.index)}).sort_values(['nh', 'r'], ascending=False)
        atas = dfc.index[:k]
        for t, x in list(pegang.items()):
            if x <= d:
                akhir_keluar[t] = x
                del pegang[t]
        kosong = _p_slot - len(pegang)
        cal = [t for t in atas if bool(BA.at[d, t])]
        for t in cal:
            if kosong <= 0:
                break
            if t in pegang:
                continue
            g = fr[t]
            if d not in pos[t]:
                continue
            i = pos[t][d]
            if i < WARM:
                continue
            if akhir_keluar.get(t) == d:
                continue
            sp = ST.at[d, t]
            kosong -= 1
            if i + 1 < len(g) and g.open.values[i + 1] <= sp:
                continue
            sig[t].iloc[i] = True
            pegang[t] = g.index[_keluar(g, i, sp, P=P)] if i + 1 < len(g) else pd.Timestamp.max
    for t, g in fr.items():
        g['sig'] = sig[t]
        g['stop'] = ST[t].reindex(g.index)
        g['tgt'] = np.nan
        g['exitc'] = False
        g['rank'] = g['_nh'] + _p_r_kali_1em06 * R[t].reindex(g.index).fillna(0).clip(-_p_clip_50, _p_clip_a1_50)
    dl = NH.index[-1]
    nhd = NH.loc[dl].dropna()
    k = int(np.floor(P['len_kali_0_3'] * len(nhd)))
    dfc = pd.DataFrame({'nh': nhd, 'r': R.loc[dl].reindex(nhd.index)}).sort_values(['nh', 'r'], ascending=False)
    atas = dfc.index[:k]
    for t, g in fr.items():
        g.attrs['_m45'] = dict(atas30=t in atas, kedudukan=list(dfc.index).index(t) + 1 if t in dfc.index else None, k=k, hb=bool(dl in hbs), pegang=t in pegang)
    masih = {t for t, x in pegang.items() if x >= dl}
    calx = [t for t in atas if bool(BA.at[dl, t]) and t not in masih and (dl in pos[t]) and (pos[t][dl] >= WARM)]
    for t, g in fr.items():
        g.attrs['_m45'].update(urutan=calx.index(t) + 1 if t in calx else None, kosong2=_p_slot - len(masih), masih=t in masih)

def _hari_ke_hb(d):
    """Hari dagangan (hari bekerja; Andaian saya: cuti umum diabaikan) dari d ke hari bekerja terakhir bulan (> d)."""
    hb = d + pd.offsets.BMonthEnd(0)
    if hb <= d:
        hb = d + pd.offsets.BMonthEnd(1)
    return len(pd.bdate_range(d + pd.Timedelta(days=1), hb))
BELUM_DITALA = False

# --- JULAT/TALA (pilih_julat.py) ---
JULAT = {}
TALA = []
