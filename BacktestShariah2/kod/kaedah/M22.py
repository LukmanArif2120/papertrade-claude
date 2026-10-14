from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M22'
NAMA = 'Qullamaggie Episodic Pivot'
VARIAN = 'V0 Sumber tulen (QQQ EMA, jurang>=10%, vol>=3x, henti low hari jurang, keluar<SMA10)'
TMAX = None
WARM = 70
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

ema = lambda s, k: s.ewm(span=k, adjust=False).mean()


def _mkt(idx, index):
    q = idx['QQQ'].close
    e10, e20 = ema(q, 10), ema(q, 20)
    m = (e10 > e20) & (e10 > e10.shift()) & (e20 > e20.shift())
    # Laporan: data QQQ berakhir lebih awal; tarikh tanpa data QQQ dianggap penapis gagal
    return m.reindex(index).fillna(False).astype(bool), (e10 > e20).reindex(index).ffill().fillna(False)


def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c, v = g.open, g.high, g.low, g.close, g.volume
        MK, _ = _mkt(idx, g.index)
        G = o / c.shift() - 1
        VR = v / v.rolling(50).mean().shift(1)
        EP = (G >= 0.10) & (VR >= 3)
        ADRp = (h / l).shift(1).rolling(20).mean() - 1
        RISK = (c - l) / c
        sig = MK & EP & (c >= o) & (RISK <= ADRp)
        lk = (o.shift(-1) <= l).fillna(False)
        g['_ADRp'] = ADRp
        g['sig'] = (sig & ~lk).fillna(False)
        g['stop'] = l
        g['tgt'] = np.nan
        g['exitc'] = c < c.rolling(10).mean()
        g['rank'] = VR


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V0 (kod sedia, PADAN registry), N=5: 1 penapis QQQ (EMA10 > EMA20,
    kedua-dua naik); 2 PENCETUS jurang buka >= 10%; 3 volume >= 3× purata 50 hari; 4 tutup >= buka;
    5 risiko (tutup − low)/tutup <= ADR20.
    Syarat 3–5 hanya wujud pada hari jurang itu sendiri, jadi sebelum jurang paling banyak 1/5 syarat
    dipenuhi — tidak mungkin capai N−1. Mengikut piawaian ketat, tiada calon hampir."""
    return None
