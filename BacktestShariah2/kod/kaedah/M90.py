from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M90'
NAMA = 'Pring KST'
VARIAN = 'V3 V1 + tutup>SMA50, keluar tutup<SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260


def _rma_atr(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _kst(c):
    roc = lambda n: 100 * (c / c.shift(n) - 1)
    kst = (roc(10).rolling(10).mean() + 2 * roc(15).rolling(10).mean()
           + 3 * roc(20).rolling(10).mean() + 4 * roc(30).rolling(15).mean())
    return kst, kst.rolling(9).mean()


def sedia(fr, idx):
    for g in fr.values():
        kst, isy = _kst(g.close)
        s50 = g.close.rolling(50).mean()
        silang = (kst > isy) & (kst.shift() <= isy.shift())
        g['_kst'] = kst; g['_isy'] = isy; g['_s50'] = s50
        g['sig'] = silang & (kst > 0) & (g.close > s50)
        g['stop'] = g.close - 2 * _rma_atr(g)
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
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
    # Syarat entry V3 (laporan M90 "Cara ujian" + V3): N = 3
    #   1. KST > 0   2. tutup > SMA50   3. PENCETUS: KST silang ke atas garis isyarat SMA9
    # Prasyarat pencetus: KST <= isyarat pada bar akhir (jika tidak, silang tidak boleh berlaku esok).
    r = g.iloc[-1]
    if bool(r.sig) or any(np.isnan([r._kst, r._isy, r._s50])):
        return None
    if not (r._kst > 0 and r.close > r._s50 and r._kst <= r._isy):
        return None
    paras = _cari_paras(g, idx, ekor=150)
    if paras is None:
        return None
    j = _jarak(paras, float(r.close))
    if not (0 < j <= 2.0):
        return None
    return {'sebab': f'KST positif ({r._kst:.1f}); tutup di atas SMA50 ({r._s50:.2f}); KST ({r._kst:.1f}) hanya sedikit di bawah garis isyarat ({r._isy:.1f})',
            'syarat_beli': f'Tutup esok > {paras:.2f} supaya KST melintas ke atas garis isyarat SMA9 (KST kekal > 0, tutup kekal > SMA50)',
            'pencetus': 'KST silang isyarat', 'paras': round(float(paras), 2), 'jarak_pct': round(float(j), 2),
            'syarat_dipenuhi': '2/3', 'skor': round(float(1 - j / 2), 3)}
