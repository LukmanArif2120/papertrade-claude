from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M41'
NAMA = 'FW Penyatuan Mingguan'
VARIAN = 'V0 Sumber sahaja (tanpa had julat 25%)'
TMAX = None
WARM = 300
ADA_HENTI = True
SILANG = False
PERLU_BAR = 320


def _ema_sma(x, n):
    """EMA dimulakan dengan purata mudah n nilai pertama yang sah (kad)."""
    x = pd.Series(x, dtype=float); out = np.full(len(x), np.nan)
    v = x.values; ok = np.flatnonzero(~np.isnan(v))
    if len(ok) < n: return pd.Series(out, x.index)
    s = ok[0]; a = 2 / (n + 1)
    out[s + n - 1] = v[s:s + n].mean()
    for k in range(s + n, len(v)): out[k] = a * v[k] + (1 - a) * out[k - 1]
    return pd.Series(out, x.index)


def _minggu(g):
    k = g.index.to_period('W-SUN')        # minggu kalendar Isnin-Ahad
    gr = g.groupby(k)
    w = pd.DataFrame({'open': gr.open.first(), 'high': gr.high.max(), 'low': gr.low.min(),
                      'close': gr.close.last(), 'volume': gr.volume.sum(),
                      'tarikh': pd.Series(g.index, index=g.index).groupby(k).last()}).reset_index(drop=True)
    c = w.close
    w['sma20'] = c.rolling(20).mean()
    w['macd'] = _ema_sma(c, 12) - _ema_sma(c, 26)
    w['isy'] = _ema_sma(w.macd, 9)
    w['rint'] = w.high.rolling(6).max().shift(1); w['sok'] = w.low.rolling(6).min().shift(1)
    saiz = c / c.shift() - 1
    t10 = c > c.rolling(10).max().shift(1)
    jul = w.high - w.low
    sumbu = np.where(jul > 0, (w.high - np.maximum(w.open, c)) / jul.replace(0, np.nan), 1.0)
    w['henti'] = (w.rint + w.sok) / 2
    jarak = (c - w.henti) / c < 0.20
    volok = w.volume >= 1.3 * w.volume.shift()
    w['sig'] = ((c > w.sma20) & (w.macd > w.isy) & (c > w.rint) & (saiz >= 0.05) & (saiz <= 0.20)
                & t10 & (pd.Series(sumbu) < 0.5) & volok & jarak)   # V0: tanpa SATU (julat <= 25%)
    w['turun'] = (w.macd < w.isy) & (w.macd.shift() >= w.isy.shift())
    return w


def sedia(fr, idx):
    for g in fr.values():
        w = _minggu(g)
        ix = g.index; n = len(g); pos = {d: i for i, d in enumerate(ix)}
        o, lo, c = g.open.values, g.low.values, g.close.values
        wk_of_day = np.searchsorted(w.tarikh.values, ix.values)   # indeks minggu bagi setiap hari
        sig = np.zeros(n, bool); stop = np.full(n, np.nan); exitc = np.zeros(n, bool)
        raw = {}
        for k in np.flatnonzero(w.sig.values):
            raw[pos[w.tarikh[k]]] = (k, w.henti[k])
        for i, (k, h) in raw.items(): stop[i] = h
        turun = w.turun.values
        i = WARM
        while i < n - 1:
            if i not in raw or o[i + 1] <= raw[i][1]:
                i += 1; continue
            wk, sp = raw[i]; sig[i] = True
            xs = np.flatnonzero(turun[wk + 1:])
            paras = None; mula = None
            if len(xs):
                x = wk + 1 + xs[0]; paras = w.low[x]; mula = pos[w.tarikh[x]] + 1
            j = i + 1; keluar = None
            while j < n:
                ex = paras is not None and j >= mula and c[j] < paras
                if ex: exitc[j] = True
                if j > i + 1 and o[j] <= sp: keluar = j; break
                if lo[j] <= sp: keluar = j; break
                if ex and j + 1 < n: keluar = j + 1; break
                j += 1
            if keluar is None: break
            i = keluar + 1
        # Bar terakhir: buka esok belum diketahui. Andaian saya: minggu dianggap siap jika bar terakhir hari Jumaat;
        # jika minggu belum siap (scan pertengahan minggu), tiada isyarat.
        siap = ix[-1].weekday() == 4
        if (n - 1) in raw and n - 1 >= WARM and siap: sig[n - 1] = True
        g['sig'] = sig; g['stop'] = stop; g['tgt'] = np.nan; g['exitc'] = exitc
        g['rank'] = g.close / g.close.shift(63) - 1
        # Minggu 'semasa' untuk persediaan: minggu depan jika minggu ini sudah siap, atau minggu ini jika belum siap
        b = len(w) if siap else len(w) - 1          # indeks minggu yang belum ditutup
        ws = w.iloc[:b]                              # minggu siap
        g.attrs['_m41'] = dict(siap=siap, close=float(ws.close.iloc[-1]), sma20=float(ws.sma20.iloc[-1]),
                               macd=float(ws.macd.iloc[-1]), isy=float(ws.isy.iloc[-1]),
                               rint=float(ws.high.iloc[-6:].max()), sok=float(ws.low.iloc[-6:].min()),
                               tutup10=float(ws.close.iloc[-10:].max()), vol_lalu=float(ws.volume.iloc[-1]),
                               tutup_lalu=float(ws.close.iloc[-1]))


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V0 (mingguan), N=4:
    1 tutup minggu > SMA20 minggu; 2 MACD(12,26) > garis isyarat(9); 3 jarak henti (tutup − (rintangan+sokongan)/2)/tutup < 20%;
    4 PENCETUS = lilin pecahan mingguan: tutup > high 6 minggu & > tutup maks 10 minggu, kenaikan 5–20%,
      sumbu atas < 50% julat, volum >= 1.3 x minggu lalu.
    Syarat 1–3 mesti benar pada minggu siap terakhir DAN pada tutup minggu hipotesis = paras pencetus."""
    r = g.iloc[-1]; a = g.attrs.get('_m41')
    if bool(r.sig) or not a or np.isnan(a['sma20']) or np.isnan(a['isy']):
        return None
    if not (a['close'] > a['sma20'] and a['macd'] > a['isy']):
        return None
    rint, sok, tl = a['rint'], a['sok'], a['tutup_lalu']
    paras = max(rint, a['tutup10'], 1.05 * tl)
    hmax = 1.20 * tl
    if paras > hmax:
        return None
    henti = (rint + sok) / 2
    if not ((paras - henti) / paras < 0.20):
        return None
    # Semak SMA20 & MACD pada tutup minggu hipotesis = paras
    w = _minggu(g)
    ws = w.close.iloc[:len(w) if a['siap'] else len(w) - 1]
    cc = pd.concat([ws, pd.Series([paras])], ignore_index=True)
    s20 = cc.rolling(20).mean().iloc[-1]
    mc = _ema_sma(cc, 12) - _ema_sma(cc, 26); isy = _ema_sma(mc, 9)
    if not (paras > s20 and mc.iloc[-1] > isy.iloc[-1]):
        return None
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    bila = 'minggu ini' if not a['siap'] else 'minggu depan'
    return {'sebab': f'Mingguan: tutup > SMA20 minggu ({a["sma20"]:.2f}); MACD > garis isyarat; jarak henti {henti:.2f} < 20%',
            'syarat_beli': f'Tutup {bila} (hari dagangan terakhir minggu) > {paras:.2f} dan <= {hmax:.2f}, sumbu atas < 50% julat minggu, volum minggu >= {1.3*a["vol_lalu"]:,.0f}; beli buka hari berikutnya; henti {henti:.2f}',
            'pencetus': 'Lilin pecahan mingguan', 'paras': round(paras, 2), 'jarak_pct': round(jarak, 2),
            'syarat_dipenuhi': '3/4', 'skor': round(1 - jarak / 2, 3)}
