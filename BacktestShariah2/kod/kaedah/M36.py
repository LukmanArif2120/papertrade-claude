from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M36'
NAMA = 'Turtle 55/20'
VARIAN = 'V2 V1 keluar tutup<SMA50 + sig tutup>SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

# Kad Spesifikasi Mesin spec/M36_turtle_55_20.md seksyen 8, varian V2:
# sig = PECAH55_i (tutup > H55 dan tutup semalam <= H55 semalam) & tutup > SMA50;
# stop = buka_masuk - 2*N_i (N = JS Wilder 20, benih purata mudah 20 JS pertama, JS bar pertama = high-low);
# exitc = tutup < SMA50; rank ROC63.


def _N(g, n=20):
    h, l, c = g.high.values, g.low.values, g.close.values
    pc = np.r_[np.nan, c[:-1]]
    js = np.nanmax(np.vstack([h - l, np.abs(h - pc), np.abs(l - pc)]), axis=0)
    out = np.full(len(c), np.nan)
    if len(c) < n:
        return pd.Series(out, g.index)
    out[n - 1] = js[:n].mean()
    for i in range(n, len(c)):
        out[i] = (19 * out[i - 1] + js[i]) / 20
    return pd.Series(out, g.index)


def sedia(fr, idx):
    for g in fr.values():
        c, h = g.close, g.high
        h55 = h.shift(1).rolling(55).max()
        s50 = c.rolling(50).mean()
        N = _N(g)
        pecah = (c > h55) & (c.shift() <= h55.shift())
        g['_h55'] = h55; g['_s50'] = s50; g['_N'] = N
        g['sig'] = (pecah & (c > s50)).fillna(False).astype(bool)
        # henti bergantung pada buka hari masuk (i+1); pada bar terakhir belum diketahui -> NaN
        g['stop'] = g.open.shift(-1) - 2 * N
        g['tgt'] = np.nan
        g['exitc'] = (c < s50).fillna(False)
        g['rank'] = c / c.shift(63) - 1


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V2 (3): (1) tutup > SMA50, (2) tutup semalam <= H55 semalam (bagi esok: tutup hari ini
    <= H55 hari ini), (3) PENCETUS tutup > H55 (high tertinggi 55 hari sebelum hari isyarat)."""
    if len(g) < 60:
        return None
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._h55) or np.isnan(r._s50):
        return None
    c = g.close.values.astype(float); c_ = c[-1]
    if not (c_ > r._s50 and c_ <= r._h55):
        return None
    h55_esok = float(g.high.iloc[-55:].max())                   # tetingkap esok: 55 high terakhir hingga hari ini
    paras = max(h55_esok, c[-49:].mean())                       # dan tutup esok > SMA50 esok
    jarak = (paras - c_) / c_ * 100
    if not (0 < jarak <= 2.0):
        return None
    return {'sebab': f'Tutup > SMA50 ({r._s50:.2f}); tutup hari ini belum melepasi high 55 hari',
            'syarat_beli': f'Tutup esok > {paras:.2f} (high 55 hari); beli buka lusa, henti = buka - 2N (2N kini ~{2*r._N:.2f})',
            'pencetus': 'Tutup > high 55 hari', 'paras': float(round(paras, 4)), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '2/3', 'skor': float(round(1 - jarak / 2, 3))}
