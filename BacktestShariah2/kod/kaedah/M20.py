from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M20'
NAMA = 'EMA10/15 Crossover + Sudut'
VARIAN = 'V3 V1 tanpa syarat sudut'
TMAX = 20
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230

ema = lambda s, k: s.ewm(span=k, adjust=False).mean()


def _kunci(g, sig, stop, T, warm, tmax=None, ex=None):
    """Cermin gelung trades() enjin supaya lajur tgt kekal pada nilai hari isyarat sepanjang dagangan
    (laporan M19: sasaran dikunci pada hari isyarat, isian ke hadapan daripada isyarat yang diambil)."""
    o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values
    n = len(g); tg = np.full(n, np.nan); ex = np.zeros(n, bool) if ex is None else ex
    i = warm
    while i < n - 1:
        if not sig[i]: i += 1; continue
        Ti = T[i]; sp = stop[i] if not np.isnan(stop[i]) else -np.inf
        j = i + 1; keluar = False
        while j < n:
            if j > i + 1 and o[j] <= sp: keluar = True; break
            if l[j] <= sp: keluar = True; break
            if not np.isnan(Ti) and j > i + 1 and (o[j] >= Ti or h[j] >= Ti): keluar = True; break
            if ex[j] and j + 1 < n: j += 1; keluar = True; break
            if tmax and (j - i) >= tmax: keluar = True; break
            j += 1
        if not keluar: j = n - 1
        tg[i:j + 1] = Ti
        i = j + 1
    tg[n - 1] = T[n - 1] if sig[n - 1] else tg[n - 1]
    return tg


def _atrw(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def sedia(fr, idx):
    for g in fr.values():
        o, h, l, c = g.open, g.high, g.low, g.close
        E10, E15 = ema(c, 10), ema(c, 15)
        Hi = np.maximum(E10, E15); Lo = np.minimum(E10, E15)
        below = pd.concat([(c.shift(k) < Lo.shift(k)) for k in range(1, 6)], axis=1).any(axis=1)
        S100 = c.rolling(100).mean()
        sig = (c > Hi) & (c.shift() <= Hi.shift()) & below & (c > S100)
        stop = 0.99 * l
        T = c + 2 * (c - stop)
        lk = ((o.shift(-1) <= stop) | (o.shift(-1) >= T)).fillna(False)
        sig = (sig & ~lk).fillna(False)
        SL = (E10 - E10.shift(5)) / _atrw(g)
        g['_Hi'] = Hi; g['_Lo'] = Lo; g['_S100'] = S100; g['_below'] = below
        g['sig'] = sig
        g['stop'] = stop
        g['tgt'] = _kunci(g, sig.values, stop.values.astype(float), T.values.astype(float), WARM, TMAX)
        g['exitc'] = False
        g['rank'] = SL.fillna(-99.0)   # laporan: isyarat tanpa SL paling bawah


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V3 tanpa sudut (kod sedia, PADAN registry), N=3:
    1 tutup < min(EMA10, EMA15) dalam 5 hari lepas; 2 tutup > SMA100; 3 PENCETUS silang:
    tutup naik melepasi max(EMA10, EMA15) (tutup semalam <= max EMA).
    Paras silang esok (algebra): x > EMA10' dan x > EMA15' <=> x > EMA10 hari ini dan x > EMA15 hari ini,
    jadi paras = max(EMA10, EMA15) hari ini (tepat)."""
    if len(g) < 120: return None
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._S100): return None
    if not r.close <= r._Hi: return None                 # belum silang (syarat 'semalam <= max EMA' untuk esok)
    c5 = g.close.iloc[-5:]; Lo5 = g._Lo.iloc[-5:]
    if not (c5 < Lo5).any(): return None                  # 1 (tetingkap esok = hari i-4..i)
    if not r.close > r._S100: return None                 # 2
    paras = r._Hi
    s100_esok = g.close.iloc[-99:].mean()                 # x > SMA100 esok <=> x > purata 99 tutup terakhir
    paras_akhir = max(paras, s100_esok)
    jarak = (paras_akhir - r.close) / r.close * 100
    if not (0 < jarak <= 2.0): return None
    return {'sebab': f'Tutup di bawah EMA10/15 dalam 5 hari lepas; tutup > SMA100 ({r._S100:.2f}); belum silang max EMA',
            'syarat_beli': f'Tutup esok > {paras_akhir:.2f} (max EMA10/EMA15 hari ini = paras silang tepat); '
                           f'henti 0.99 × low esok, sasaran 2R, had 20 hari; langkau jika buka masuk <= henti atau >= sasaran',
            'pencetus': 'Silang tutup > max(EMA10, EMA15)', 'paras': round(float(paras_akhir), 2), 'jarak_pct': round(float(jarak), 2),
            'syarat_dipenuhi': '2/3', 'skor': round(1 - jarak / 2, 3)}
