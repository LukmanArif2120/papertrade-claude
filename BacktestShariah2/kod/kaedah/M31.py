from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M31'
NAMA = 'Band Walk (BB 20/2)'
VARIAN = 'V0 Peraturan pengguna (henti tutup<LOWER isyarat, keluar MID turun)'
TMAX = None
WARM = 200
ADA_HENTI = True
HENTI_TUTUP = '_lo'   # henti ikut tutup: paras = LOWER BB hari isyarat (paparan & R sahaja; enjin keluar melalui exitc)
SILANG = False
PERLU_BAR = 30

# Logik isyarat disalin daripada finalis_v1.py (KOMPILASI Bahagian 8.3), cabang K=='M31'.


def _bb(c):
    mid = c.rolling(20).mean(); sd = c.rolling(20).std(ddof=0)
    return mid, mid + 2 * sd, mid - 2 * sd


def sedia(fr, idx):
    for g in fr.values():
        c = g.close; n = len(g)
        mid, up, lo = _bb(c); w = up - lo; s10 = c.rolling(10).mean()
        sgs = ((c > up) & (c.shift() <= up.shift()) & (w > w.shift()) & (mid > mid.shift(5)) & (s10 > mid)).fillna(False).values
        dn = (mid < mid.shift(5)).fillna(False).values
        cv_ = c.values; lov = lo.values; exv = np.zeros(n, bool); i = WARM
        # henti ikut TUTUP < LOWER hari isyarat: jejak dagangan sama seperti enjin (seperti kod asal)
        while i < n - 1:
            if not sgs[i]: i += 1; continue
            lv = lov[i]; j = i + 1
            while j < n:
                if (dn[j] or cv_[j] < lv) and j + 1 < n: exv[j] = True; j += 1; break
                j += 1
            else: j = n - 1
            i = j + 1
        g['_mid'] = mid; g['_up'] = up; g['_lo'] = lo; g['_s10'] = s10
        g['sig'] = pd.Series(sgs, g.index)
        g['stop'] = np.nan
        g['tgt'] = np.nan
        g['exitc'] = pd.Series(exv, g.index)
        g['rank'] = c / c.shift(63) - 1


def _bb_esok(c_last19, X):
    # SMA20, SD20 (ddof=0) dan band esok jika tutup esok = X (X boleh tatasusunan)
    X = np.asarray(X, float)
    s = c_last19.sum() + X; s2 = (c_last19 ** 2).sum() + X ** 2
    mid = s / 20; sd = np.sqrt(np.maximum(s2 / 20 - mid ** 2, 0))
    return mid, mid + 2 * sd, mid - 2 * sd


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V0 (5): (1) tutup semalam <= UPPER semalam, (2) lebar band menaik,
    (3) MID > MID 5 hari lepas, (4) MA10 > MID, (5) PENCETUS tutup > UPPER.
    Pencetus = tutup esok > UPPER esok (UPPER bergantung pada tutup esok; diselesaikan dengan carian binari)."""
    if len(g) < 30:
        return None
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._up) or np.isnan(r._mid):
        return None
    c = g.close.values.astype(float)
    # (1) bagi esok, 'semalam' = hari ini: tutup hari ini <= UPPER hari ini
    if not (c[-1] <= r._up):
        return None
    # Andaian saya: syarat (3) dan (4) mesti dipenuhi hari ini DAN pada tutup esok = paras; syarat (2) dinilai pada paras.
    if not (r._mid > g._mid.iloc[-6] and r._s10 > r._mid):
        return None
    c19 = c[-19:]
    # X - UPPER(X) menaik secara monoton dalam X (dUPPER/dX < 1), jadi carian binari sah
    lo_, hi_ = c[-1], c[-1] * 1.5
    for _ in range(60):
        m_ = (lo_ + hi_) / 2
        if m_ > _bb_esok(c19, m_)[1]: hi_ = m_
        else: lo_ = m_
    paras = hi_
    jarak = (paras - c[-1]) / c[-1] * 100
    if not (0 < jarak <= 2.0):
        return None
    mid_e, up_e, lo_e = _bb_esok(c19, paras)
    s10_e = (c[-9:].sum() + paras) / 10
    w_hari_ini = r._up - r._lo
    if not ((up_e - lo_e) > w_hari_ini and mid_e > g._mid.iloc[-5] and s10_e > mid_e):
        return None
    return {'sebab': f'Tutup hari ini ({c[-1]:.2f}) masih <= band atas ({r._up:.2f}); MID SMA20 menaik berbanding 5 hari lepas; '
                     f'MA10 ({r._s10:.2f}) > MID ({r._mid:.2f}); pada tutup {paras:.2f} lebar band akan bertambah',
            'syarat_beli': f'Tutup esok > {paras:.2f} (band atas Bollinger 20/2 esok, dikira dengan tutup esok)',
            'pencetus': 'Tutup > band atas BB', 'paras': float(round(paras, 4)), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '4/5', 'skor': float(round(1 - jarak / 2, 3))}
