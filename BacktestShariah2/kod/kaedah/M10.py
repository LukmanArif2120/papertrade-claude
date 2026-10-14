from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M10'
NAMA = 'EMA3 + CCI + MACD'
VARIAN = 'V4 V1 pencetus CCI>+100'
TMAX = None
WARM = 260
ADA_HENTI = True
SILANG = False
PERLU_BAR = 300


def _cci(g, n=20):
    tp = (g.high + g.low + g.close) / 3
    md = tp.rolling(n).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
    return (tp - tp.rolling(n).mean()) / (0.015 * md)


def sedia(fr, idx):
    for g in fr.values():
        c, l, o = g.close, g.low, g.open
        e60 = c.ewm(span=60, adjust=False).mean(); e125 = c.ewm(span=125, adjust=False).mean(); e250 = c.ewm(span=250, adjust=False).mean()
        cci = _cci(g)
        susun = (c > e250) & (e60 > e125) & (e125 > e250)
        sentuh = (l - e60).rolling(11).min() <= 0            # tetingkap i-10..i (11 hari, ikut kod 8.3)
        lemah = cci.rolling(11).min() < -100
        stop = 0.99 * e125
        asas = susun & sentuh & lemah & (cci.shift() <= 100) & (cci > 100) & (c > e60)
        sig = asas & ~(o.shift(-1) <= stop)                    # langkau jika buka masuk <= henti
        g['_susun'] = susun; g['_sentuh'] = sentuh; g['_lemah'] = lemah; g['_cci'] = cci; g['_e60'] = e60
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (c < e125).fillna(False)
        g['rank'] = c / e250 - 1


def hampir(g, idx):
    """Piawaian KETAT. Syarat entry V4 (N=5):
    1 tutup > EMA250 dan EMA60 > EMA125 > EMA250; 2 low sentuh EMA60 dalam tetingkap 11 hari;
    3 CCI20 < -100 dalam tetingkap 11 hari; 4 tutup > EMA60; 5 PENCETUS: CCI20 silang atas +100 (semalam <= 100 < hari ini)."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 300 or np.isnan(r._cci) or r._cci > 100:
        return None
    if not bool(r._susun) or not (r.close > r._e60):
        return None
    # Tetingkap esok = hari i-9..i (10 bar terakhir) + esok; bar esok (tutup > EMA60, CCI > 100) tidak menyumbang sentuhan/CCI<-100.
    if not ((g.low.iloc[-10:] - g._e60.iloc[-10:]).min() <= 0) or not (g._cci.iloc[-10:].min() < -100):
        return None
    # Andaian saya: harga esok high = low = tutup = x; cari x terkecil (dalam +2%) yang memberi CCI20 > 100 dan x > EMA60 esok.
    tp = ((g.high + g.low + g.close) / 3).values[-19:].astype(float)
    xs = r.close * (1 + np.linspace(0.0001, 0.02, 400))
    W = np.concatenate([np.tile(tp, (len(xs), 1)), xs[:, None]], axis=1)
    m = W.mean(axis=1); md = np.abs(W - m[:, None]).mean(axis=1)
    cci = (xs - m) / (0.015 * md)
    e60e = r._e60 + (xs - r._e60) * 2 / 61
    ok = (cci > 100) & (xs > e60e)
    if not ok.any():
        return None
    paras = xs[np.argmax(ok)]
    jarak = (paras - r.close) / r.close * 100
    return {'sebab': f'EMA60 > EMA125 > EMA250 dan tutup > EMA250; low sentuh EMA60 dan CCI20 < -100 dalam 10 hari terakhir; tutup > EMA60 ({r._e60:.2f}); CCI20 kini {r._cci:.0f}',
            'syarat_beli': f'Tutup esok >= {paras:.2f} supaya CCI20 silang atas +100 (anggaran high = low = tutup)',
            'pencetus': 'CCI20 silang atas +100', 'paras': round(float(paras), 2), 'jarak_pct': round(float(jarak), 2),
            'syarat_dipenuhi': '4/5', 'skor': round(1 - jarak / 2, 2)}
