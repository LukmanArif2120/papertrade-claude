from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M08'
NAMA = 'SMA20 + SMA200'
VARIAN = 'V1 Spesifikasi dikunci'
TMAX = None
WARM = 220
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230


def _asas(g):
    c, h, l, o = g.close, g.high, g.low, g.open
    s20 = c.rolling(20).mean()
    sl20 = s20 / s20.shift(5) - 1
    lonjak = h.shift(1).rolling(10).max()          # max(high i-10..i-1)
    return s20, sl20, lonjak


def sedia(fr, idx):
    for g in fr.values():
        c, h, l, o = g.close, g.high, g.low, g.open
        s20, sl20, lonjak = _asas(g)
        stop = 0.99 * l.rolling(6).min()           # 0.99 x min(low i-5..i)
        asas = (sl20 >= 0.01) & (l <= 1.01 * s20) & (c > s20) & (c > o) & (lonjak >= 1.05 * s20)
        bn = o.shift(-1)
        # Langkau (buka masuk <= henti atau buka masuk > 1.05xSMA20) ialah pembatalan pesanan pada buka i+1.
        # Andaian saya: pada bar terakhir (buka esok belum diketahui) isyarat dikekalkan; semak buka esok secara manual.
        langkau = (bn <= stop) | (bn > 1.05 * s20)
        g['_s20'] = s20; g['_sl20'] = sl20; g['_lonjak'] = lonjak
        g['sig'] = (asas & ~langkau).fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (s20 < s20.shift()).fillna(False)
        g['rank'] = sl20


def hampir(g, idx):
    """Piawaian KETAT (ARAHAN_HAMPIR). Syarat entry V1 (N=4):
    1 SL20 >= 1%; 2 lonjakan: max(high 10 hari sebelum) >= 1.05 x SMA20; 3 tutup > SMA20;
    4 PENCETUS (lilin lantunan): low <= 1.01 x SMA20 dan tutup > SMA20 dan lilin hijau."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 25 or np.isnan(r._s20) or np.isnan(r._sl20):
        return None
    # Syarat selain pencetus mesti dipenuhi hari ini
    if r._sl20 < 0.01 or not (r._lonjak >= 1.05 * r._s20) or not (r.close > r._s20):
        return None
    # Andaian saya: SMA20 esok dianggar dengan tutup esok = tutup hari ini (tetingkap esok = 19 tutup terakhir + esok).
    s20e = (g.close.iloc[-19:].sum() + r.close) / 20
    lonjak_e = g.high.iloc[-10:].max()               # tetingkap lonjakan esok = high hari i-9..i
    if not (lonjak_e >= 1.05 * s20e) or s20e / g._s20.iloc[-5] - 1 < 0.01:
        return None                                  # syarat keadaan tidak kekal esok -> bukan 90-100%
    paras = 1.01 * s20e
    # Andaian saya: pencetus ini undur ke bawah (sentuh SMA20), jadi jarak = (tutup - paras)/tutup x 100;
    # jika tutup sudah <= paras, jarak = 0 (sentuhan hampir pasti, yang tinggal lilin hijau tutup > SMA20).
    jarak = max(0.0, (r.close - paras) / r.close * 100)
    if jarak > 2.0:
        return None
    return {'sebab': f'SMA20 menaik {r._sl20*100:.1f}% (5 hari); ada lonjakan >= 5% atas SMA20 dalam 10 hari; tutup ({r.close:.2f}) > SMA20 ({r._s20:.2f})',
            'syarat_beli': f'Esok low <= {paras:.2f} (1.01 x SMA20 esok ~{s20e:.2f}), lilin hijau dan tutup > {s20e:.2f}; batal jika buka lusa > {1.05*s20e:.2f} (terlanjur) atau <= henti',
            'pencetus': 'Lantunan SMA20 (low sentuh + lilin hijau)', 'paras': round(float(paras), 2), 'jarak_pct': round(float(jarak), 2),
            'syarat_dipenuhi': '3/4', 'skor': round(1 - jarak / 2, 2)}
