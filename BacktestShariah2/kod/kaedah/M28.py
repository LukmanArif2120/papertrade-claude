from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M28'
NAMA = 'VWAP Separator + Kiss Pivot'
VARIAN = 'V2 Pemisahan ≥3 ATR'
TMAX = 10
WARM = 60
ADA_HENTI = True
SILANG = False
PERLU_BAR = 60
AMBANG = 3.0


def _atrw(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c, v = g.open, g.high, g.low, g.close, g.volume
        tp = (h + l + c) / 3
        vw = (tp * v).rolling(20).sum() / v.rolling(20).sum()
        a = _atrw(g)
        sepdn = (vw - l) / a
        lvl = l <= 1.01 * l.shift(1).rolling(20).min()
        jw = ((np.minimum(o, c) - l) >= 2 * (c - o).abs()) & ((c - l) >= 0.6 * (h - l))
        eg = (c > o) & (c.shift() < o.shift()) & (c >= o.shift()) & (o <= c.shift())
        pt = ((o.shift() - c.shift()) >= a.shift()) & (c >= (o.shift() + c.shift()) / 2)
        rev = jw | eg | pt
        stop = 0.99 * l
        on = o.shift(-1)
        sig = (sepdn >= AMBANG) & lvl & rev & (c < vw)
        sig = sig & ~(on <= stop) & ~(on >= vw)
        g['_sepdn'] = sepdn; g['_lvl'] = lvl.fillna(False); g['_vw'] = vw; g['_rev'] = rev.fillna(False)
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = vw            # sasaran VWAP bergerak (enjin baca nilai hari sebelumnya)
        g['exitc'] = False
        g['rank'] = sepdn


def hampir(g, idx):
    # Piawaian ketat: syarat entry V2 = (1) SEPDN >= 3 ATR, (2) LVL: low <= 1.01 x low 20 hari,
    # (3) tutup < VWAP20, (4) PENCETUS lilin pembalikan menaik (John Wick / telan menaik / Power of Tower).
    # Pencetus corak satu hari -> jarak_pct = None. Syarat 1-3 mesti dipenuhi pada bar terakhir.
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._sepdn):
        return None
    if not (r._sepdn >= AMBANG and bool(r._lvl) and r.close < r._vw) or bool(r._rev):
        return None
    o, c = float(r.open), float(r.close)
    a = float(_atrw(g).iloc[-1])
    # Andaian saya: VWAP20 dan ATR14 esok dianggarkan = nilai hari ini
    p_lvl = 1.01 * float(g.low.iloc[-20:].min())
    p_sep = float(r._vw) - AMBANG * a
    plow = min(p_lvl, p_sep)
    corak = ['John Wick (sumbu bawah >= 2x badan, tutup di 60% atas julat)']
    if c < o:
        corak.append(f'telan menaik (tutup > buka, tutup >= {o:.2f}, buka <= {c:.2f})')
    if (o - c) >= a:
        corak.append(f'Power of Tower (tutup >= {(o + c) / 2:.2f})')
    return {'sebab': f'Terpisah {r._sepdn:.1f}xATR14 di bawah VWAP20 ({r._vw:.2f}); low di paras low 20 hari; tutup < VWAP20',
            'syarat_beli': f'Esok: low <= {plow:.2f} (kekal di paras low 20 hari dan pemisahan >= 3 ATR), tutup < {float(r._vw):.2f}, dan lilin pembalikan menaik: ' + ' / '.join(corak),
            'pencetus': 'lilin pembalikan', 'paras': None, 'jarak_pct': None,
            'syarat_dipenuhi': '3/4', 'skor': 0.9}
