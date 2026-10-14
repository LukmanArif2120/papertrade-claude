from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M44'
NAMA = 'Tapak Rata IBD'
VARIAN = 'V3 V1 tanpa syarat volum'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210


def _tapak(g):
    c = g.close
    T = g.high.rolling(25).max().shift(1)          # high i-25..i-1
    R = g.low.rolling(25).min().shift(1)
    dalam = (T - R) / T <= 0.15
    # AWAL: kejadian TERAKHIR T bukan dalam i-9..i-1 (laporan: Andaian)
    awal = g.high.rolling(9).max().shift(1) < T
    tb = T + 0.10
    dahulu = c.shift(26) / c.shift(89) - 1 >= 0.20
    s50 = c.rolling(50).mean()
    return T, R, dalam, awal, tb, dahulu, s50


def sedia(fr, idx):
    for g in fr.values():
        c = g.close
        T, R, dalam, awal, tb, dahulu, s50 = _tapak(g)
        pecah = (c > tb) & (c.shift() <= tb)
        dekat = c <= 1.05 * tb
        g['sig'] = dalam & awal & pecah & dahulu & dekat & (c > s50)
        # Henti 0.92 x buka hari masuk (i+1). Bar terakhir: buka esok belum diketahui -> anggaran 0.92 x tutup
        # Andaian saya: anggaran bar terakhir hanya untuk paparan scan; tidak menjejaskan backtest.
        st = 0.92 * g.open.shift(-1)
        st.iloc[-1] = 0.92 * c.iloc[-1]
        g['stop'] = st
        g['tgt'] = np.nan
        g['exitc'] = c < s50
        g['rank'] = c / c.shift(63) - 1
        g['_T'] = T; g['_R'] = R; g['_dalam'] = dalam; g['_awal'] = awal; g['_dahulu'] = dahulu; g['_s50'] = s50


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V3 (tanpa volum), N=5, dinilai untuk isyarat esok:
    1 DALAM: tapak 25 hari (high/low i-24..i) sedalam <= 15%; 2 AWAL: high tapak tiada dalam 9 hari terakhir;
    3 DAHULU: kenaikan >= 20% (tutup i-25 berbanding i-88); 4 tutup > SMA50;
    5 PENCETUS: tutup esok > high tapak + 0.10 (dan <= 1.05 x paras), dengan tutup hari ini <= paras."""
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._T) or len(g) < 90:
        return None
    h = g.high.iloc[-25:]; l = g.low.iloc[-25:]
    T = h.max(); R = l.min()
    if (T - R) / T > 0.15:
        return None
    if g.high.iloc[-9:].max() >= T:
        return None
    c = g.close
    naik = c.iloc[-26] / c.iloc[-89] - 1
    if naik < 0.20:
        return None
    # Andaian saya: syarat tutup > SMA50 disemak pada tutup hari ini (SMA50 hari ini)
    if not (r.close > r._s50):
        return None
    tb = T + 0.10
    jarak = (tb - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    return {'sebab': f'Tapak rata 25 hari sedalam {(T-R)/T*100:.1f}% (<= 15%); high tapak di luar 9 hari terakhir; kenaikan terdahulu {naik*100:.0f}% (>= 20%); tutup > SMA50 ({r._s50:.2f})',
            'syarat_beli': f'Tutup esok > {tb:.2f} (high tapak + 0.10) dan <= {1.05*tb:.2f}, tutup kekal > SMA50; beli buka lusa; henti 8% bawah harga masuk',
            'pencetus': 'Pecah high tapak + 0.10', 'paras': round(tb, 2), 'jarak_pct': round(jarak, 2),
            'syarat_dipenuhi': '4/5', 'skor': round(1 - jarak / 2, 3)}
