from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M89'
NAMA = 'Chande 65sma-3cc'
VARIAN = 'V5 V1+SMA65 naik (>SMA65 10h lalu)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 220


def _rma_atr(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def sedia(fr, idx):
    for g in fr.values():
        c = g.close
        s65 = c.rolling(65).mean()
        atas = c > s65
        tiga = atas & atas.shift(1, fill_value=False) & atas.shift(2, fill_value=False) & (c.shift(3) <= s65.shift(3))
        naik = s65 > s65.shift(10)
        g['_s65'] = s65; g['_naik'] = naik
        g['sig'] = tiga & naik
        g['stop'] = c - 2 * _rma_atr(g)
        g['tgt'] = np.nan
        g['exitc'] = c < g.low.rolling(14).min().shift(1)
        g['rank'] = c / c.shift(63) - 1


def hampir(g, idx):
    """Syarat entry V5 (sig): (1) tutup i-3 <= SMA65; (2) tutup i-2 > SMA65; (3) tutup i-1 > SMA65;
    (4) SMA65_i > SMA65_{i-10}; (5) tutup i > SMA65 (pencetus = tutup ketiga di atas). N = 5."""
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._s65) or len(g) < 75:
        return None
    c = g.close.values; s = g._s65.values
    # untuk isyarat esok: hari ini & semalam di atas SMA65, kelmarin <= SMA65
    if not (c[-1] > s[-1] and c[-2] > s[-2] and c[-3] <= s[-3]):
        return None
    # tutup esok > SMA65 esok: c > (S64 + c)/65  ->  c > S64/64
    s64 = float(c[-64:].sum()); paras = s64 / 64
    jarak = (paras - c[-1]) / c[-1] * 100
    # Andaian saya: pencetus jenis "kekal di atas paras"; tutup sudah di atas -> jarak = 0
    if jarak > 2.0:
        return None
    jarak = max(0.0, jarak)
    # SMA65 esok (pada tutup = maks(paras, tutup kini)) mesti > SMA65 10 hari sebelum esok
    s65_esok = (s64 + max(paras, c[-1])) / 65
    if not (s65_esok > s[-10]):
        return None
    return {'sebab': f'Tutup kelmarin <= SMA65; 2 tutup berturut-turut > SMA65 ({r._s65:.2f}); SMA65 menaik (> nilai 10 hari lalu)',
            'syarat_beli': f'Tutup esok > {paras:.2f} (SMA65 esok) — tutup ketiga berturut-turut di atas SMA65',
            'pencetus': 'Tutup ke-3 > SMA65', 'paras': float(round(paras, 4)), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '4/5', 'skor': float(round(1 - jarak / 2, 2))}
