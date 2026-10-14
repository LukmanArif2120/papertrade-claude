from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M35'
NAMA = 'Pocket Pivot Morales & Kacher'
VARIAN = 'V3 V1 DEKAT10 sahaja'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210

# Kad Spesifikasi Mesin spec/M35_pocket_pivot.md seksyen 7, varian V3:
# sig = PP_i & close>SMA50 & close>SMA200 & DEKAT10_i (low <= 1.02*SMA10 dan close > SMA10);
# stop = low_i; langkau jika buka i+1 <= low_i; exitc = LANGGAR10_j (close_{j-1}<SMA10_{j-1} dan low_j<low_{j-1}).


def _vt10(c, v):
    turun = c < c.shift()
    vt = v.where(turun, 0.0)
    return vt.shift(1).rolling(10, min_periods=1).max().fillna(0.0)


def sedia(fr, idx):
    for g in fr.values():
        c, l, v = g.close, g.low, g.volume
        s10, s50, s200 = c.rolling(10).mean(), c.rolling(50).mean(), c.rolling(200).mean()
        vt10 = _vt10(c, v)
        pp = (c > c.shift()) & (v > vt10)
        dekat10 = (l <= 1.02 * s10) & (c > s10)
        sig = pp & (c > s50) & (c > s200) & dekat10
        bk = g.open.shift(-1)
        # langkau jika buka masuk <= henti; Andaian saya: bar terakhir (buka esok belum diketahui) isyarat dikekalkan
        sig = sig & ((bk > l) | bk.isna())
        g['_s10'] = s10; g['_s50'] = s50; g['_s200'] = s200; g['_vt10'] = vt10
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = l
        g['tgt'] = np.nan
        g['exitc'] = ((c.shift() < s10.shift()) & (l < l.shift())).fillna(False)
        g['rank'] = c / c.shift(63) - 1


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V3 (4): (1) tutup > SMA50, (2) tutup > SMA200, (3) DEKAT10: low <= 1.02 x SMA10 dan tutup > SMA10,
    (4) PENCETUS Pocket Pivot: tutup naik berbanding semalam dengan volum > volum hari turun tertinggi 10 hari.
    (1)-(3) mesti dipenuhi hari ini; paras = tutup esok minimum supaya naik dan kekal di atas SMA10/50/200 esok."""
    if len(g) < 205:
        return None
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._s200):
        return None
    if not (r.close > r._s50 and r.close > r._s200 and r.low <= 1.02 * r._s10 and r.close > r._s10):
        return None
    c = g.close.values.astype(float); c_ = c[-1]
    # tutup esok X > SMAn esok <=> X > purata (n-1) tutup terakhir
    # Andaian saya: 'tutup naik' = sekurang-kurangnya satu sen di atas tutup hari ini.
    paras = max(c_ + 0.01, c[-9:].mean(), c[-49:].mean(), c[-199:].mean())
    jarak = (paras - c_) / c_ * 100
    if not (0 < jarak <= 2.0):
        return None
    turun = (g.close < g.close.shift()).iloc[-10:]
    vt = float(g.volume.iloc[-10:][turun].max()) if turun.any() else 0.0
    s10_e = (c[-9:].sum() + paras) / 10
    return {'sebab': f'Tutup > SMA50 ({r._s50:.2f}) dan SMA200 ({r._s200:.2f}); berehat dekat SMA10 (low {r.low:.2f} <= 1.02 x SMA10 {r._s10:.2f}, tutup > SMA10)',
            'syarat_beli': f'Tutup esok >= {paras:.2f} (naik daripada hari ini) dengan volum > {int(vt):,} (volum hari turun tertinggi 10 hari), '
                           f'dan low esok <= ~{1.02*s10_e:.2f} (1.02 x SMA10 esok); beli buka lusa jika buka > low esok',
            'pencetus': 'Pocket Pivot (naik + volum)', 'paras': float(round(paras, 4)), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '3/4', 'skor': float(round(1 - jarak / 2, 3))}
