from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M101'
NAMA = 'Bulkowski: Tiga lembah menaik'
VARIAN = 'V3 V1 + corak sambungan (tutup_a>tutup_a-63)'
TMAX = None
WARM = 260
ADA_HENTI = True
SILANG = False
PERLU_BAR = 320
P = 5


def _corak(g, P=P):
    """Per hari i: syarat persediaan (NAIK3, JARAK, sambungan), PUNCAK_i, PUNCAK lama (a sama, high a..i-2), low_c."""
    lo = g.low.values.astype(float); hi = g.high.values.astype(float); c = g.close.values.astype(float)
    n = len(g)
    piv = (g.low == g.low.rolling(2 * P + 1, center=True).min()).values  # seri: kedua-duanya pangsi
    sedia_ = np.zeros(n, bool); pk = np.full(n, np.nan); pk_lama = np.full(n, np.nan); lc = np.full(n, np.nan)
    sam = np.zeros(n, bool)
    kp = np.nonzero(piv)[0]
    ptr = 0
    for i in range(1, n):
        # pangsi disahkan: k + P <= i - 1
        while ptr < len(kp) and kp[ptr] + P <= i - 1:
            ptr += 1
        if ptr < 3:
            continue
        a, b, cc = kp[ptr - 3], kp[ptr - 2], kp[ptr - 1]
        naik3 = lo[a] < lo[b] < lo[cc] and lo[cc + 1:i + 1].min() > lo[cc]
        jarak = 5 <= b - a <= 60 and 5 <= cc - b <= 60 and i - a <= 126
        if not (naik3 and jarak):
            continue
        sedia_[i] = True
        pk[i] = hi[a:i].max()
        pk_lama[i] = hi[a:i - 1].max() if i - 1 > a else np.nan
        lc[i] = lo[cc]
        sam[i] = a - 63 >= 0 and c[a] > c[a - 63]
    idx = g.index
    return (pd.Series(sedia_, idx), pd.Series(pk, idx), pd.Series(pk_lama, idx), pd.Series(lc, idx), pd.Series(sam, idx))


def sedia(fr, idx):
    for g in fr.values():
        sd, pk, pkl, lc, sam = _corak(g)
        s50 = g.close.rolling(50).mean()
        sah = (g.close > pk) & (g.close.shift(1) <= pkl)
        stop = 0.99 * lc
        sig = sd & sah & sam & (g.close > s50)
        # Kad: masuk dilangkau jika buka masuk <= stop
        langkau = (g.open.shift(-1) <= stop).fillna(False)
        g['_sd'] = sd & sam; g['_pk'] = pk; g['_lc'] = lc; g['_s50'] = s50
        g['sig'] = sig & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(63) - 1


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}


def hampir(g, idx):
    # Syarat entry V3 (6): (1) tiga lembah menaik NAIK3; (2) JARAK lembah 5-60 hari & corak <= 126 hari; (3) corak sambungan tutup_a > tutup_{a-63};
    # (4) tutup hari ini <= puncak corak (pecahan kali pertama); (5) tutup > SMA50; (6) PENCETUS: tutup esok > puncak tertinggi corak
    r = g.iloc[-1]
    if bool(r.sig):
        return None
    lo = g.low.values.astype(float); hi = g.high.values.astype(float); c = g.close.values.astype(float)
    n = len(g); i = n
    piv = (g.low == g.low.rolling(2 * P + 1, center=True).min()).values
    kp = np.nonzero(piv)[0]; kp = kp[kp + P <= i - 1]
    if len(kp) < 3:
        return None
    a, b, cc = kp[-3], kp[-2], kp[-1]
    # Andaian saya: low esok belum diketahui; syarat min(low c+1..i) > low_c disemak hingga hari ini sahaja
    if not (lo[a] < lo[b] < lo[cc] and lo[cc + 1:i].min() > lo[cc]):          # 1
        return None
    if not (5 <= b - a <= 60 and 5 <= cc - b <= 60 and i - a <= 126):          # 2
        return None
    if not (a - 63 >= 0 and c[a] > c[a - 63]):                                 # 3
        return None
    pk = hi[a:i].max(); pk_lama = hi[a:i - 1].max() if i - 1 > a else np.nan
    if np.isnan(pk_lama) or not (c[-1] <= pk_lama):                            # 4
        return None
    if np.isnan(r._s50) or not (r.close > r._s50):                             # 5
        return None
    s50_min = c[-49:].sum() / 49                                               # tutup esok > SMA50 esok
    paras = max(pk, s50_min)
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    return _hasil(f'Tiga lembah menaik ({lo[a]:.2f} < {lo[b]:.2f} < {lo[cc]:.2f}), jarak lembah sah, aliran 63 hari sebelum corak menaik; tutup > SMA50 ({r._s50:.2f})',
                  f'Tutup esok > {paras:.2f} (puncak tertinggi corak {pk:.2f}) dan low esok kekal > {lo[cc]:.2f}; henti {0.99*lo[cc]:.2f}; '
                  f'masuk dibatalkan jika harga buka hari masuk <= henti',
                  'Pecah puncak corak', paras, jarak, 5, 6)
