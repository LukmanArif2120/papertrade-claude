# Rangka R — rangka ranking piawai M162–M167 (spec: SPEC_SEMUA_KAEDAH.md, tanda `FAIL ASAL: spec/RANGKA_R`).
# Sama seperti M114 V4: kolam PCT(F) >= 0.90 atas 431, vol20 >= 100K, SPY > SMA200, henti buka_masuk x 0.88,
# keluar tutup < maks tutup sejak masuk - 3 x ATR22 (atau tutup < henti), rank F. Enjin v1.2 tidak diubah;
# keluar chandelier bergantung pada tarikh masuk, jadi laluan enjin.trades direplika untuk menandakan exitc.
import numpy as np, pandas as pd
from enjin import atr

LAPAN = ['ASST', 'FCEL', 'MTDR', 'OVV', 'PR', 'SM', 'VAL', 'XENE']   # saham bermasalah data (M114 Bahagian 10)


def spy_pada(g, idx, lajur='close'):
    """Siri SPY di-reindex ke tarikh saham (ffill)."""
    return idx['SPY'][lajur].reindex(g.index, method='ffill')


def spy_atas_sma200(g, idx):
    s = idx['SPY'].close
    return (s > s.rolling(200).mean()).reindex(g.index, method='ffill').fillna(False).astype(bool)


def rs12(g, idx):
    rsl = g.close / spy_pada(g, idx)
    return rsl / rsl.shift(251) - 1


def pct(F):
    """F: dict ticker -> Series. Persentil keratan rentas (rank pct) atas semua saham ada nilai pada hari itu."""
    P = pd.DataFrame(F)
    return P.rank(axis=1, pct=True)


def tandai_keluar(g, warm=200, k=3.0, n_atr=22, tmax=None, keluar_lain=None):
    """Replika gelung enjin.trades (v1.2) satu saham: isi g['exitc'] hanya pada hari keluar chandelier.
       g mesti sudah ada sig dan stop (tgt = NaN). keluar_lain: Series bool tambahan (cth. tutup < SMA50) atau None."""
    o, l, c = g.open.values, g.low.values, g.close.values
    sig = g.sig.fillna(False).astype(bool).values; st = g.stop.astype(float).values
    a = atr(g, n_atr).values if k is not None else None
    lain = keluar_lain.fillna(False).astype(bool).values if keluar_lain is not None else None
    n = len(g); ex = np.zeros(n, bool); i = warm
    while i < n - 1:
        if not sig[i]:
            i += 1; continue
        sp = st[i] if not np.isnan(st[i]) else -np.inf
        j = i + 1; mx = -np.inf
        while j < n:
            if j > i + 1 and o[j] <= sp: break
            if l[j] <= sp: break
            mx = max(mx, c[j])
            kena = c[j] < sp
            if k is not None: kena = kena or (not np.isnan(a[j]) and c[j] < mx - k * a[j])
            if lain is not None: kena = kena or lain[j]
            if kena and j + 1 < n:
                ex[j] = True; j += 1; break
            if tmax and (j - i) >= tmax: break
            j += 1
        i = j + 1
    g['exitc'] = ex


def pasang(fr, idx, F, kolam=0.90, penapis_spy=True, P=None, sah=None, exit_sma50=False):
    """Isi sig/stop/tgt/exitc/rank bagi setiap saham ikut Rangka R. F: dict ticker -> Series kunci ranking.
       P: persentil siap (DataFrame) jika sudah dikira; sah: dict ticker -> Series bool syarat tambahan."""
    P = pct(F) if P is None else P
    for t, g in fr.items():
        p = P[t].reindex(g.index) if t in P else pd.Series(np.nan, g.index)
        s = (p >= kolam) & (g.volume.rolling(20).mean() >= 1e5) & F[t].reindex(g.index).notna()
        if penapis_spy: s &= spy_atas_sma200(g, idx)
        if sah is not None: s &= sah[t].reindex(g.index).fillna(False).astype(bool)
        g['sig'] = s.fillna(False).astype(bool)
        g['stop'] = g.open.shift(-1) * 0.88
        g['tgt'] = np.nan
        g['rank'] = F[t].reindex(g.index).astype(float)
        if exit_sma50:
            tandai_keluar(g, k=None, keluar_lain=g.close < g.close.rolling(50).mean())
        else:
            tandai_keluar(g)
