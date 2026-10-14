from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M39'
NAMA = 'Radge Pecahan Bollinger 100 hari'
VARIAN = 'V4 V1 jalur atas 2 SD'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 205


def _jalur(g):
    c = g.close
    m = c.rolling(100).mean(); sd = c.rolling(100).std(ddof=0)   # SD populasi (spec)
    return m, sd


def sedia(fr, idx):
    for g in fr.values():
        c = g.close
        m, sd = _jalur(g)
        atas2 = m + 2 * sd; bawah = m - sd
        lintas = (c > atas2) & (c.shift() <= atas2.shift())
        g['_atas2'] = atas2; g['_bawah'] = bawah
        stop = np.maximum(bawah, 0.85 * c)
        # Langkau jika buka hari masuk <= henti (spec). Bar terakhir: buka esok belum diketahui -> isyarat kekal
        g['sig'] = lintas & ~(g.open.shift(-1) <= stop)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = c < bawah
        g['rank'] = c / c.shift(63) - 1


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V4, N=2:
    1 tutup hari ini <= ATAS2 hari ini (syarat 'tutup semalam <= jalur' bagi lintasan esok);
    2 PENCETUS: tutup esok > ATAS2 esok (SMA100 + 2 SD populasi, tetingkap 100 hari termasuk tutup esok)."""
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._atas2) or len(g) < 100:
        return None
    if not (r.close <= r._atas2):
        return None
    w99 = g.close.values[-99:].astype(float)
    def f(x):
        v = np.append(w99, x); return x - (v.mean() + 2 * v.std())
    lo, hi = float(r.close), float(r.close) * 1.5
    if f(hi) <= 0:
        return None
    for _ in range(60):                      # carian binari: tutup esok minimum untuk lintasan
        m = (lo + hi) / 2
        if f(m) > 0: hi = m
        else: lo = m
    paras = hi
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    return {'sebab': f'Tutup {r.close:.2f} masih di bawah jalur atas SMA100 + 2 SD ({r._atas2:.2f}); persediaan lintasan',
            'syarat_beli': f'Tutup esok > {paras:.2f} (jalur SMA100 + 2 SD esok, termasuk tutup esok); beli buka lusa; henti maks(SMA100 − 1 SD; 0.85 × tutup)',
            'pencetus': 'Tutup lintas atas SMA100+2SD', 'paras': round(paras, 2), 'jarak_pct': round(jarak, 2),
            'syarat_dipenuhi': '1/2', 'skor': round(1 - jarak / 2, 3)}
