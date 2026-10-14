from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M14'
NAMA = 'Walking with the Whales'
VARIAN = 'V3 V1 pegang ikut SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210


def sedia(fr, idx):
    for g in fr.values():
        c, h, l, o = g.close, g.high, g.low, g.open
        s50 = c.rolling(50).mean()
        Lhi = np.maximum(l.shift(1), l.shift(2)); Llo = np.minimum(l.shift(1), l.shift(2))
        Hhi = np.maximum(h.shift(1), h.shift(2))
        stop = np.minimum(l, Llo)
        asas = (l <= Lhi) & (c > Llo) & (c > s50)
        sig = asas & ~(o.shift(-1) <= stop)                  # langkau hanya jika buka masuk <= henti (kod finalis)
        g['_s50'] = s50
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (c < s50).fillna(False)
        g['rank'] = (Hhi - c) / (c - stop)


def hampir(g, idx):
    """Piawaian KETAT. Syarat entry V3 (N=2):
    1 tutup > SMA50 (trend); 2 PENCETUS kotak 2 hari: low <= L_hi dan tutup > L_lo (L dari low 2 hari sebelumnya)."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 55 or np.isnan(r._s50) or not (r.close > r._s50):
        return None
    lhi = max(r.low, g.low.iloc[-2]); llo = min(r.low, g.low.iloc[-2])     # kotak esok = low hari ini dan semalam
    s50e = (g.close.iloc[-49:].sum() + r.close) / 50   # Andaian saya: SMA50 esok dianggar dengan tutup esok = tutup hari ini
    tmin = max(llo, s50e)
    # Andaian saya: pencetus undur ke bawah; jarak = (tutup - L_hi)/tutup x 100, 0 jika tutup sudah <= L_hi.
    jarak = max(0.0, (r.close - lhi) / r.close * 100)
    if jarak > 2.0:
        return None
    return {'sebab': f'Tutup ({r.close:.2f}) > SMA50 ({r._s50:.2f}); kotak 2 hari: L_hi {lhi:.2f}, L_lo {llo:.2f}',
            'syarat_beli': f'Esok low <= {lhi:.2f} dan tutup > {tmin:.2f} (max L_lo, SMA50 esok); henti {min(llo, lhi):.2f} atau low esok jika lebih rendah',
            'pencetus': 'Sentuh paras bawah kotak 2 hari', 'paras': round(float(lhi), 2), 'jarak_pct': round(float(jarak), 2),
            'syarat_dipenuhi': '1/2', 'skor': round(1 - jarak / 2, 2)}
