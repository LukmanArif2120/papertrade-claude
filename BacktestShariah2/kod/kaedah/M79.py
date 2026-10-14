from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M79'
NAMA = 'Radge: 20% Flipper'
VARIAN = 'V3 V1 dengan A=0.15 (masuk/keluar/henti 15%)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260     # mesin keadaan bermula hari pertama data; lebih banyak sejarah = keadaan lebih tepat
A = 0.15


def _zigzag(c):
    c = c.values.astype(float); n = len(c)
    flip = np.zeros(n, bool); jatuh = np.zeros(n, bool)
    naik = np.zeros(n, bool); LT = np.full(n, np.nan); HT = np.full(n, np.nan)
    if n == 0: return flip, jatuh, naik, LT, HT
    st = False; lt = c[0]; ht = np.nan
    for i in range(n):
        if not st:
            if i > 0: lt = min(lt, c[i])
            if c[i] >= (1 + A) * lt:
                st = True; ht = c[i]; flip[i] = True
        else:
            ht = max(ht, c[i])
            if c[i] <= (1 - A) * ht:
                st = False; lt = c[i]; jatuh[i] = True
        naik[i] = st; LT[i] = lt; HT[i] = ht
    return flip, jatuh, naik, LT, HT


def sedia(fr, idx):
    for g in fr.values():
        flip, jatuh, naik, LT, HT = _zigzag(g.close)
        g['_naik'] = naik; g['_LT'] = LT; g['_HT'] = HT
        g['sig'] = flip
        g['stop'] = (1 - A) * g.close
        g['tgt'] = np.nan
        g['exitc'] = jatuh
        g['rank'] = g.close / g.close.shift(63) - 1


def hampir(g, idx):
    # Syarat entry V3 (N=2): keadaan TURUN (mesin zigzag 15%); PENCETUS = tutup esok >= 1.15 x titik low tutup (LT).
    r = g.iloc[-1]
    if bool(r.sig) or bool(r._naik) or np.isnan(r._LT):
        return None
    paras = (1 + A) * r._LT
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    return {'sebab': f'Keadaan TURUN; titik low tutup {r._LT:.2f}; harga sudah naik {(r.close / r._LT - 1) * 100:.1f}% dari low',
            'syarat_beli': f'Tutup esok ≥ {paras:.2f} (15% atas titik low tutup); henti 0.85 × tutup isyarat, keluar bila tutup ≤ 0.85 × tutup tertinggi',
            'pencetus': 'tutup ≥ 1.15 × low', 'paras': round(paras, 2), 'jarak_pct': round(jarak, 2),
            'syarat_dipenuhi': '1/2', 'skor': round(1 - jarak / 2, 3)}
