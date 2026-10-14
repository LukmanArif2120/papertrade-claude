from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M33'
NAMA = 'Supertrend + SMA10'
VARIAN = 'V5 V1 + volum>VOL20'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60

# Kad Spesifikasi Mesin spec/M33_supertrend_ma.md seksyen 8, varian V5:
# sig = PECAH_i & TAPAK_i (julat 20h sebelum <= 25%) & volum_i > purata volum i-20..i-1;
# stop = ST_i (GB_i) tetap; exitc tutup < ST (ARAH TURUN); langkau jika buka i+1 <= stop.


def _atr_wilder(g, n=10):
    c = g.close.values; h = g.high.values; l = g.low.values
    pc = np.r_[np.nan, c[:-1]]
    tr = np.nanmax(np.vstack([h - l, np.abs(h - pc), np.abs(l - pc)]), axis=0)
    a = np.full(len(c), np.nan)
    if len(c) <= n:
        return a
    # Andaian (laporan M33): nilai pertama = purata mudah 10 julat sebenar pertama (bar pertama TR = high-low)
    a[n - 1] = tr[:n].mean()
    for i in range(n, len(c)):
        a[i] = (a[i - 1] * (n - 1) + tr[i]) / n
    return a


def _supertrend(g, n=10, k=3.0):
    h = g.high.values; l = g.low.values; c = g.close.values; N = len(c)
    a = _atr_wilder(g, n)
    hl2 = (h + l) / 2; ba = hl2 + k * a; bb = hl2 - k * a
    GA = np.full(N, np.nan); GB = np.full(N, np.nan); up = np.zeros(N, bool)
    s = n - 1
    if N <= s:
        return GA, GB, up, np.full(N, np.nan)
    GA[s] = ba[s]; GB[s] = bb[s]; up[s] = False
    for i in range(s + 1, N):
        GB[i] = bb[i] if (bb[i] > GB[i - 1] or c[i - 1] < GB[i - 1]) else GB[i - 1]
        GA[i] = ba[i] if (ba[i] < GA[i - 1] or c[i - 1] > GA[i - 1]) else GA[i - 1]
        if c[i] > GA[i - 1]: up[i] = True
        elif c[i] < GB[i - 1]: up[i] = False
        else: up[i] = up[i - 1]
    st = np.where(up, GB, GA)
    return GA, GB, up, st


def sedia(fr, idx):
    for g in fr.values():
        GA, GB, up, st = _supertrend(g)
        upS = pd.Series(up, g.index); stS = pd.Series(st, g.index)
        pecah = upS & ~upS.shift(1, fill_value=True)
        tapak = g.high.shift(1).rolling(20).max() / g.low.shift(1).rolling(20).min() - 1 <= 0.25
        vol20 = g.volume.shift(1).rolling(20).mean()
        sig = pecah & tapak & (g.volume > vol20)
        bk = g.open.shift(-1)
        # langkau jika buka masuk <= henti; Andaian saya: bar terakhir (buka esok belum diketahui) isyarat dikekalkan
        sig = sig & ((bk > stS) | bk.isna())
        g['_up'] = upS; g['_GA'] = pd.Series(GA, g.index); g['_vol20'] = vol20; g['_tapak'] = tapak
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stS.where(upS)
        g['tgt'] = np.nan
        g['exitc'] = ~upS
        g['rank'] = g.close / g.close.shift(63) - 1


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V5 (3): (1) Supertrend(10,3) TURUN hari ini (supaya esok berlaku pertukaran arah),
    (2) TAPAK: julat 20 hari sebelum hari isyarat <= 25%, (3) PENCETUS: tutup esok > garisan atas Supertrend hari ini (GA)
    dengan volum esok > purata volum 20 hari (pencetus harga + volum serentak)."""
    if len(g) < 40:
        return None
    r = g.iloc[-1]
    if bool(r.sig) or bool(r._up) or np.isnan(r._GA):
        return None
    tp = g.high.iloc[-20:].max() / g.low.iloc[-20:].min() - 1     # tapak untuk esok = julat 20 hari hingga hari ini
    if not (tp <= 0.25):
        return None
    c_ = float(r.close); paras = float(r._GA)                    # pertukaran ke NAIK esok jika tutup esok > GA hari ini
    jarak = (paras - c_) / c_ * 100
    if not (0 < jarak <= 2.0):
        return None
    vol20 = float(g.volume.iloc[-20:].mean())                    # purata volum 20 hari yang digunakan esok
    return {'sebab': f'Supertrend(10,3) masih turun; tapak 20 hari mendatar (julat {tp*100:.1f}% <= 25%)',
            'syarat_beli': f'Tutup esok > {paras:.2f} (garisan atas Supertrend) dengan volum esok > {int(vol20):,} (purata 20 hari); '
                           f'beli buka lusa jika buka > garisan Supertrend baharu',
            'pencetus': 'Tutup > Supertrend + volum', 'paras': float(round(paras, 4)), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '2/3', 'skor': float(round(1 - jarak / 2, 3))}
