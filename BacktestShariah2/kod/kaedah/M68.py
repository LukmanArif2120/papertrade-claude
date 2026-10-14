from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M68'
NAMA = "Kell Base n' Break"
VARIAN = 'V3 V1 keluar close<SMA50 (+tutup>SMA50)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
N = 10


def _syarat(g):
    c = g.close
    e10 = c.ewm(span=10, adjust=False).mean(); e20 = c.ewm(span=20, adjust=False).mean()
    s50 = c.rolling(50).mean()
    pangsi = g.high.rolling(N).max().shift(1)
    lowt = g.low.rolling(N).min().shift(1)
    ketat = pangsi / lowt - 1 <= 0.12
    sokong = ((c >= e20).astype(int).rolling(N).sum().shift(1) == N) & (e10.shift(1) > e20.shift(1))
    baharu = pangsi >= g.high.rolling(63).max().shift(1)
    naikdulu = pangsi / g.low.rolling(30).min().shift(N + 1) - 1 >= 0.20
    return pangsi, lowt, ketat, sokong, baharu, naikdulu, s50, e20


def sedia(fr, idx):
    for g in fr.values():
        pangsi, lowt, ketat, sokong, baharu, naikdulu, s50, e20 = _syarat(g)
        sig = (g.close > pangsi) & ketat & sokong & baharu & naikdulu & (g.close > s50)
        # Langkau jika buka_masuk (buka i+1) <= stop; bar akhir: buka esok belum diketahui -> isyarat dikekalkan.
        langkau = g.open.shift(-1) <= lowt
        g['sig'] = sig & ~langkau
        g['stop'] = lowt
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(63) - 1


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def hampir(g, idx):
    """Syarat entry V3 (N=7) untuk isyarat esok; tapak = 10 hari terakhir termasuk hari ini:
       [1] KETAT: high tapak / low tapak - 1 <= 12% [2] SOKONG: tutup >= EMA20 setiap hari tapak
       [3] EMA10 > EMA20 hari ini [4] BAHARU: pangsi (high tapak) >= high 63 hari [5] NAIK: pangsi / low 30 hari sebelum tapak - 1 >= 20%
       [6] tutup > SMA50 (keadaan hari ini; esok mesti kekal) [7] PENCETUS: tutup esok > pangsi."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < PERLU_BAR:
        return None
    c = g.close
    e10 = c.ewm(span=10, adjust=False).mean(); e20 = c.ewm(span=20, adjust=False).mean()
    s50 = c.iloc[-50:].mean()
    pangsi = g.high.iloc[-N:].max(); lowt = g.low.iloc[-N:].min()
    if pangsi / lowt - 1 > 0.12: return None                                   # [1]
    if not (c.iloc[-N:] >= e20.iloc[-N:]).all(): return None                   # [2]
    if not e10.iloc[-1] > e20.iloc[-1]: return None                            # [3]
    if pangsi < g.high.iloc[-63:].max(): return None                           # [4]
    if pangsi / g.low.iloc[-N - 30:-N].min() - 1 < 0.20: return None          # [5]
    if not r.close > s50: return None                                          # [6]
    paras = max(float(pangsi), float(c.iloc[-49:].mean()))
    jarak = (paras - r.close) / r.close * 100
    if jarak <= 0 or jarak > 2.0: return None
    return _hasil(f'Tapak {N} hari ketat ({(pangsi/lowt-1)*100:.1f}%); tutup >= EMA20 sepanjang tapak; EMA10 > EMA20; pangsi = high 63 hari; '
                  f'naik >= 20% sebelum tapak; tutup > SMA50 ({s50:.2f})',
                  f'Tutup esok > {paras:.2f} (pangsi); henti = low tapak {lowt:.2f}', 'Tutup > pangsi', paras, jarak, 6, 7)
