from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M34'
NAMA = 'Carter TTM Squeeze'
VARIAN = 'V2 V1 keluar close<SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 80

# Kad Spesifikasi Mesin spec/M34_ttm_squeeze.md seksyen 7, varian V2:
# sig = LEPAS_i & MOM_i > 0 & MOM_i > MOM_{i-1} & ALIRAN_i; stop = min(low i-9..i); exitc close < SMA50.
# Tiada peraturan langkau (laporan M34). ATR20 Wilder = ewm alpha 1/20 dari julat sebenar hari pertama (laporan M34).

_X = np.arange(20, dtype=float); _XM = _X.mean(); _SXX = ((_X - _XM) ** 2).sum()


def _linreg_end(s, n=20):
    # nilai garis regresi kuasa dua terkecil pada titik akhir tetingkap n (vektor; setara polyfit)
    y = s.values.astype(float); out = np.full(len(y), np.nan)
    if len(y) >= n:
        w = np.lib.stride_tricks.sliding_window_view(y, n)
        ym = w.mean(axis=1); b = ((w - ym[:, None]) * (_X - _XM)).sum(axis=1) / _SXX
        out[n - 1:] = ym + b * (n - 1 - _XM)
    return pd.Series(out, s.index)


def _komponen(g):
    h, l, c = g.high, g.low, g.close
    s20 = c.rolling(20).mean(); sd = c.rolling(20).std(ddof=0)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    a20 = tr.ewm(alpha=1 / 20, adjust=False).mean()
    bba, bbb = s20 + 2 * sd, s20 - 2 * sd
    kca, kcb = s20 + 1.5 * a20, s20 - 1.5 * a20
    himpit = (bba < kca) & (bbb > kcb)
    dm = (h.rolling(20).max() + l.rolling(20).min()) / 2
    d = c - (dm + s20) / 2
    mom = _linreg_end(d)
    s50 = c.rolling(50).mean()
    aliran = (c > s50) & (s50 > s50.shift(5))
    return himpit, mom, s50, aliran


def sedia(fr, idx):
    for g in fr.values():
        himpit, mom, s50, aliran = _komponen(g)
        lepas = himpit.shift(1, fill_value=False) & ~himpit
        sig = lepas & (mom > 0) & (mom > mom.shift()) & aliran
        g['_himpit'] = himpit; g['_mom'] = mom; g['_s50'] = s50; g['_aliran'] = aliran
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = g.low.rolling(10).min()
        g['tgt'] = np.nan
        g['exitc'] = (g.close < s50).fillna(False)
        g['rank'] = g.close / g.close.shift(63) - 1


def _esok(g, X):
    """Nilai indikator TTM esok bagi tatasusunan tutup esok X.
    Andaian saya: high = low = tutup esok = X untuk tetingkap high/low 20 hari; tetapi julat sebenar esok diandaikan
    = max(ATR20 hari ini, |X - tutup hari ini|) supaya ATR tidak mengecut secara buatan (andaian konservatif)."""
    X = np.asarray(X, float)
    h, l, c = g.high.values.astype(float), g.low.values.astype(float), g.close.values.astype(float)
    c19 = c[-19:]
    s20 = (c19.sum() + X) / 20
    sd = np.sqrt(np.maximum(((c19 ** 2).sum() + X ** 2) / 20 - s20 ** 2, 0))
    tr = pd.concat([g.high - g.low, (g.high - g.close.shift()).abs(), (g.low - g.close.shift()).abs()], axis=1).max(axis=1)
    a20_hi = float(tr.ewm(alpha=1 / 20, adjust=False).mean().iloc[-1])
    a20 = a20_hi * 19 / 20 + np.maximum(a20_hi, np.abs(X - c[-1])) / 20
    himpit = (s20 + 2 * sd < s20 + 1.5 * a20) & (s20 - 2 * sd > s20 - 1.5 * a20)
    hh = np.maximum(h[-19:].max(), X); ll = np.minimum(l[-19:].min(), X)
    d_new = X - ((hh + ll) / 2 + s20) / 2
    # d bagi 19 hari terakhir (sama seperti _komponen)
    s20s = g.close.rolling(20).mean(); dm = (g.high.rolling(20).max() + g.low.rolling(20).min()) / 2
    d_old = (g.close - (dm + s20s) / 2).values[-19:]
    W = np.concatenate([np.broadcast_to(d_old, (len(X), 19)), d_new[:, None]], axis=1)
    ym = W.mean(axis=1); b = ((W - ym[:, None]) * (_X - _XM)).sum(axis=1) / _SXX
    mom = ym + b * (19 - _XM)
    s50 = (c[-49:].sum() + X) / 50
    s50_5 = g.close.rolling(50).mean().values[-5]                 # SMA50 lima hari sebelum esok
    aliran = (X > s50) & (s50 > s50_5)
    return himpit, mom, aliran


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V2 (5): (1) himpitan hidup semalam (= hari ini bagi isyarat esok), (2) ALIRAN tutup > SMA50
    dan SMA50 > SMA50 5 hari lepas, (3) MOM > 0, (4) MOM > MOM semalam, (5) PENCETUS: himpitan terlepas.
    (2)-(4) mesti dipenuhi hari ini; tutup esok minimum yang menjadikan (2)-(5) benar serentak dicari atas grid 0.01%."""
    if len(g) < 80:
        return None
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._mom):
        return None
    # Andaian saya: 'MOM > 0' dan 'aliran' mesti benar hari ini; 'MOM menaik' hanya bermakna untuk bar esok.
    if not (bool(r._himpit) and bool(r._aliran) and r._mom > 0):
        return None
    c_ = float(r.close)
    X = c_ * (1 + np.arange(1, 201) / 10000.0)                  # +0.01% .. +2.00%
    hp, mom, al = _esok(g, X)
    ok = (~hp) & (mom > 0) & (mom > r._mom) & al
    if not ok.any():
        return None
    k = int(np.argmax(ok)); paras = float(X[k])
    jarak = (paras - c_) / c_ * 100
    if not (0 < jarak <= 2.0):
        return None
    pjg = 0
    for x in g._himpit.values[::-1]:
        if not x: break
        pjg += 1
    return {'sebab': f'Himpitan TTM hidup {pjg} hari; tutup > SMA50 ({r._s50:.2f}) yang menaik; MOM positif ({r._mom:.3f})',
            'syarat_beli': f'Tutup esok >= {paras:.2f} (pada paras ini Bollinger keluar daripada Keltner, MOM > 0 dan menaik); '
                           f'henti = low terendah 10 hari',
            'pencetus': 'Himpitan terlepas', 'paras': float(round(paras, 4)), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '4/5', 'skor': float(round(1 - jarak / 2, 3))}
