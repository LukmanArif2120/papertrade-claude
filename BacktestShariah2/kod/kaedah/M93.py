from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M93'
NAMA = 'Bollinger Kaedah II: %b + MFI'
VARIAN = 'V2 V1, keluar LEMAH (%b<0.20 & MFI10<20)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260


def _rma_atr(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _psar(g, step=0.02, mx=0.20):
    # Andaian saya (ikut laporan): PSAR Wilder klasik, mula dalam aliran naik pada hari pertama data.
    h, l = g.high.values.astype(float), g.low.values.astype(float); n = len(h)
    out = np.full(n, np.nan)
    if n < 2: return pd.Series(out, g.index)
    up = True; af = step; ep = h[0]; sar = l[0]; out[0] = sar
    for i in range(1, n):
        sar = sar + af * (ep - sar)
        if up:
            sar = min(sar, l[i - 1], l[i - 2] if i >= 2 else l[i - 1])
            if l[i] < sar:
                up = False; sar = ep; ep = l[i]; af = step
            elif h[i] > ep:
                ep = h[i]; af = min(af + step, mx)
        else:
            sar = max(sar, h[i - 1], h[i - 2] if i >= 2 else h[i - 1])
            if h[i] > sar:
                up = True; sar = ep; ep = h[i]; af = step
            elif l[i] < ep:
                ep = l[i]; af = min(af + step, mx)
        out[i] = sar
    return pd.Series(out, g.index)


def _mfi(g, n=10):
    tp = (g.high + g.low + g.close) / 3; aw = tp * g.volume
    d = tp.diff()
    pos = aw.where(d > 0, 0.0).rolling(n).sum(); neg = aw.where(d < 0, 0.0).rolling(n).sum()
    m = 100 - 100 / (1 + pos / neg)
    return m.where(neg != 0, 100.0).where(pos.notna())


def _pb(c):
    s = c.rolling(20).mean(); sd = c.rolling(20).std(ddof=0)
    ja, jb = s + 2 * sd, s - 2 * sd
    return ((c - jb) / (ja - jb)).where(ja != jb, 0.5).where(s.notna())


def sedia(fr, idx):
    for g in fr.values():
        pb = _pb(g.close); mfi = _mfi(g, 10); ps = _psar(g)
        kuat = (pb > 0.80) & (mfi > 80)
        g['_pb'] = pb; g['_mfi'] = mfi
        g['sig'] = kuat & ~kuat.shift(fill_value=False)
        g['stop'] = np.where(ps < g.close, ps, g.close - 2 * _rma_atr(g))
        g['tgt'] = np.nan
        g['exitc'] = (pb < 0.20) & (mfi < 20)
        g['rank'] = g.close / g.close.shift(63) - 1


def _cari_paras(g, idx, ekor, bawah=-0.05, atas=0.02, vol=None):
    """Tutup esok minimum (dalam julat tutup*(1+bawah)..tutup*(1+atas)) yang menjadikan sig bar esok benar,
    dengan menjalankan sedia() asal pada ekor data + satu bar esok rekaan.
    Andaian saya: bar esok open=high=low=close=C; volum esok = `vol` jika diberi, jika tidak purata volum 10 hari."""
    c0 = float(g.close.iloc[-1])
    asas = g[['open', 'high', 'low', 'close', 'volume', 'turnover']].iloc[-ekor:].astype(float)
    v = float(asas.volume.iloc[-10:].mean()) if vol is None else float(vol)
    esok = asas.index[-1] + pd.offsets.BDay(1)

    def cuba(C):
        b = asas.copy()
        b.loc[esok] = [C, C, C, C, v, C * v]
        d = {'x': b}; sedia(d, {})
        return bool(d['x'].sig.iloc[-1])

    grid = np.round(np.arange(bawah, atas + 1e-9, 0.0025), 6)
    sebelum = None
    for p in grid:
        if cuba(c0 * (1 + p)):
            if sebelum is None:
                return c0 * (1 + p)
            lo, hi = c0 * (1 + sebelum), c0 * (1 + p)
            for _ in range(18):
                m = (lo + hi) / 2
                if cuba(m): hi = m
                else: lo = m
            return hi
        sebelum = p
    return None


def _jarak(paras, tutup):
    # Jarak mentah; pemanggil menolak jarak <= 0 (piawaian: 0 < jarak <= 2.0).
    return (paras - tutup) / tutup * 100


def hampir(g, idx):
    # Syarat entry V2 (= V1, laporan M93): N = 3
    #   1. Belum KUAT pada bar akhir (isyarat = hari PERTAMA KUAT)   2. %b(20,2) > 0.80   3. MFI(10) > 80
    # KUAT = %b > 0.80 DAN MFI10 > 80. Pencetus = syarat yang belum dipenuhi (%b atau MFI); satu lagi MESTI sudah dipenuhi.
    # Andaian saya: volum esok = purata volum 10 hari (MFI bergantung pada volum esok).
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._pb) or np.isnan(r._mfi):
        return None
    a, b = r._pb > 0.80, r._mfi > 80
    if a == b:          # kedua-dua dipenuhi (sudah KUAT, bukan hari pertama) atau kedua-dua belum
        return None
    paras = _cari_paras(g, idx, ekor=60)
    if paras is None:
        return None
    j = _jarak(paras, float(r.close))
    if not (0 < j <= 2.0):
        return None
    if a:
        sudah, pen = f'%b {r._pb:.2f} > 0.80', f'MFI(10) {r._mfi:.0f} naik melebihi 80'
    else:
        sudah, pen = f'MFI(10) {r._mfi:.0f} > 80', f'%b {r._pb:.2f} naik melebihi 0.80'
    return {'sebab': f'Belum KUAT pada bar akhir; {sudah}',
            'syarat_beli': f'Tutup esok > {paras:.2f} supaya {pen} sementara syarat satu lagi kekal (andaian volum esok = purata 10 hari)',
            'pencetus': 'MFI > 80' if a else '%b > 0.80', 'paras': round(float(paras), 2), 'jarak_pct': round(float(j), 2),
            'syarat_dipenuhi': '2/3', 'skor': round(float(1 - j / 2), 3)}
