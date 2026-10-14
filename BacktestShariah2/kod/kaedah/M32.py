from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M32'
NAMA = 'Momentum Burst'
VARIAN = 'V2 V1 keluar close<SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

# Kad Spesifikasi Mesin spec/M32_momentum_burst.md seksyen 7, varian V2:
# sig = BURST & SEMPIT & BUKAN3 & REHAT & ALIRAN & CLV>=0.75 & close>SMA50; stop low_i; exitc close<SMA50;
# langkau jika buka_masuk <= stop.


def _komponen(g):
    o, h, l, c, v = g.open, g.high, g.low, g.close, g.volume
    R = c / c.shift() - 1
    adr = (h / l).rolling(20).mean() - 1
    rng = (h - l)
    clv = ((c - l) / rng).where(rng > 0, 0.0)
    s50 = c.rolling(50).mean()
    burst = (R >= 0.04) & (v > v.shift())
    sempit = R.shift(1) < 0.02
    bukan3 = ~((R.shift(1) > 0) & (R.shift(2) > 0))
    a1 = adr.shift(1)
    rehat = (R.shift(1).abs() < a1) & (R.shift(2).abs() < a1) & (R.shift(3).abs() < a1) & \
            (l.shift(1).rolling(3).min() >= 0.80 * h.shift(1).rolling(20).max())
    aliran = (c.shift(1) > s50.shift(1)) & (s50.shift(1) > s50.shift(6)) & (c.shift(1) / c.shift(64) - 1 > 0)
    return dict(R=R, clv=clv, s50=s50, burst=burst, sempit=sempit, bukan3=bukan3, rehat=rehat, aliran=aliran)


def sedia(fr, idx):
    for g in fr.values():
        k = _komponen(g)
        sig = k['burst'] & k['sempit'] & k['bukan3'] & k['rehat'] & k['aliran'] & (k['clv'] >= 0.75) & (g.close > k['s50'])
        stop = g.low
        bk = g.open.shift(-1)
        # Langkau jika buka hari masuk <= henti. Andaian saya: pada bar terakhir (buka esok belum diketahui) isyarat dikekalkan;
        # enjin tidak pernah masuk pada bar terakhir, jadi backtest tidak terjejas.
        sig = sig & ((bk > stop) | bk.isna())
        for nm in ('sempit', 'bukan3', 'rehat', 'aliran'):
            g['_' + nm] = k[nm]
        g['_s50'] = k['s50']
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (g.close < k['s50']).fillna(False)
        g['rank'] = g.close / g.close.shift(63) - 1


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V2 (8): SEMPIT, BUKAN3, REHAT, ALIRAN (dinilai atas data hingga semalam hari lonjakan),
    tutup > SMA50, volum > volum semalam, CLV >= 0.75, PENCETUS pulangan harian >= 4%.
    Pencetus ialah paras harga = tutup hari ini x 1.04 (atau SMA50 jika lebih tinggi), jadi jarak sentiasa >= 4%
    dan melebihi had 2.0%: mengikut piawaian, kaedah ini tidak pernah menghasilkan calon 'hampir'."""
    if len(g) < 70:
        return None
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._s50):
        return None
    c, h, l, v = g.close, g.high, g.low, g.volume
    R = c / c.shift() - 1
    adr = float(((h / l).rolling(20).mean() - 1).iloc[-1])
    if np.isnan(adr):
        return None
    sempit = R.iloc[-1] < 0.02
    bukan3 = not (R.iloc[-1] > 0 and R.iloc[-2] > 0)
    rehat = all(abs(R.iloc[-k]) < adr for k in (1, 2, 3)) and l.iloc[-3:].min() >= 0.80 * h.iloc[-20:].max()
    aliran = c.iloc[-1] > r._s50 and r._s50 > g._s50.iloc[-6] and c.iloc[-1] / c.iloc[-64] - 1 > 0
    if not (sempit and bukan3 and rehat and aliran):
        return None
    c_ = float(c.iloc[-1])
    paras = max(c_ * 1.04, (c.iloc[-49:].sum()) / 49)   # tutup esok > SMA50 esok <=> X > purata 49 tutup terakhir
    jarak = (paras - c_) / c_ * 100
    if not (0 < jarak <= 2.0):
        return None   # sentiasa berlaku kerana jarak >= 4%
    return {'sebab': 'Rehat ketat 3 hari; aliran naik; hari ini sempit dan bukan 2 hari naik berturut',
            'syarat_beli': f'Tutup esok >= {paras:.2f}, volum > {int(v.iloc[-1]):,}, CLV >= 0.75',
            'pencetus': 'Lonjakan >= 4%', 'paras': float(round(paras, 4)), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '7/8', 'skor': float(round(1 - jarak / 2, 3))}
