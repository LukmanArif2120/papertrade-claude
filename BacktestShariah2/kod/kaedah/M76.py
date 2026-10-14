from enjin import rsi, atr
import pandas as pd, numpy as np
from numpy.lib.stride_tricks import sliding_window_view as _swv

ID = 'M76'
NAMA = 'Undercut & Rally pada Low Penting'
VARIAN = 'V1 Dikunci (UR + CLV>0.60 + tutup>SMA200)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210
N = 40


def _ur(g):
    lo = g.low.values.astype(float); hi = g.high.values.astype(float); c = g.close.values.astype(float); n = len(g)
    RP = np.full(n, np.nan); sah = np.zeros(n, bool)
    W = N - 2                                   # tetingkap i-N..i-3 = 38 bar
    if n >= N + 1:
        wl = _swv(lo, W)                        # wl[s] = lo[s..s+W-1]; bagi i, s = i-N
        for i in range(N, n):
            w = wl[i - N]
            rp = w.min(); RP[i] = rp
            kk = np.where(w == rp)[0][-1]       # hari paling akhir
            k = i - N + kk
            if k <= i - 8:
                seg = hi[k + 1:i - 2]           # k+1..i-3
                if len(seg) and seg.max() > 1.05 * rp: sah[i] = True
    RP = pd.Series(RP, g.index)
    LT = g.low.rolling(3).min()
    tembus = LT < RP
    rampas = (g.close > RP) & ((g.close.shift() <= RP) | (g.low < RP))
    ur = pd.Series(sah, g.index) & tembus & rampas
    return ur, RP, LT


def _exitc_berjaga(g, warm):
    """Replika urutan dagangan enjin (tmax None) untuk mengisi exitc = BERJAGA & tutup<SMA20."""
    o, l, c = g.open.values, g.low.values, g.close.values
    sig = g.sig.fillna(False).astype(bool).values; st = g.stop.astype(float).values
    atas = (g.close > g._s20).values; bawah = (g.close < g._s20).values
    n = len(g); ex = np.zeros(n, bool); i = warm
    while i < n - 1:
        if not sig[i]: i += 1; continue
        sp = st[i] if not np.isnan(st[i]) else -np.inf
        jaga = bool(atas[i]); j = i + 1; keluar = n - 1
        while j < n:
            if j > i + 1 and o[j] <= sp: keluar = j; break
            if l[j] <= sp: keluar = j; break
            if jaga and bawah[j] and j + 1 < n:
                ex[j] = True; keluar = j + 1; break
            if atas[j]: jaga = True
            j += 1
        i = keluar + 1
    return ex


def sedia(fr, idx):
    for g in fr.values():
        c = g.close
        ur, RP, LT = _ur(g)
        rng = g.high - g.low
        clv = ((c - g.low) / rng).where(rng > 0, 0.0)
        s20 = c.rolling(20).mean(); s200 = c.rolling(200).mean()
        stop = LT
        langkau = (g.open.shift(-1) <= stop).fillna(False)   # bar terakhir: buka esok belum diketahui
        g['_RP'] = RP; g['_LT'] = LT; g['_clv'] = clv; g['_s20'] = s20; g['_s200'] = s200; g['_ur'] = ur
        g['sig'] = ur & (clv > 0.60) & (c > s200) & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['rank'] = c / c.shift(63) - 1
        g['exitc'] = _exitc_berjaga(g, WARM)
        # Andaian saya: untuk scan/papertrade, keluar sebenar = sudah pernah tutup > SMA20 sejak isyarat DAN tutup < SMA20


def hampir(g, idx):
    # Syarat entry V1 (N=4): LOWSAH (low penting sah); TEMBUS (low 3 hari < RP); tutup > SMA200;
    # PENCETUS = RAMPAS dengan CLV > 0.60 (tutup > RP dan tutup di 40% atas julat hari).
    # Semua syarat dinilai bagi tetingkap ESOK (i+1) menggunakan data yang sudah diketahui.
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._s200) or len(g) < N + 2:
        return None
    lo = g.low.values.astype(float); hi = g.high.values.astype(float); c = g.close.values.astype(float)
    n = len(g); j = n                        # indeks esok
    w = lo[j - N:j - 2]                      # rendah esok−40 .. esok−3
    rp = w.min(); k = j - N + np.where(w == rp)[0][-1]
    if not (k <= j - 8 and hi[k + 1:j - 2].max() > 1.05 * rp):
        return None                          # LOWSAH esok gagal
    lt_kini = min(lo[-2], lo[-1])            # low tembusan esok = min(low hari ini, semalam, esok)
    if not (lt_kini < rp):
        return None                          # TEMBUS belum berlaku (Andaian saya: tidak bergantung pada low esok)
    if not (r.close > r._s200):
        return None
    p200 = c[-199:].mean()                   # tutup esok > SMA200 esok
    paras = max(rp, p200)
    if r.close <= rp:
        jarak = (paras - r.close) / r.close * 100
        if not (0 < jarak <= 2.0):
            return None
        syarat = (f'Tutup esok > {paras:.2f} (rampas semula low penting {rp:.2f}) dengan CLV > 0.60 '
                  f'(tutup di 40% atas julat esok); henti {min(lt_kini, rp):.2f} atau low esok jika lebih rendah')
        return {'sebab': f'Low penting {rp:.2f} sah (40 hari, naik > 5% selepasnya); sudah ditembusi (low {lt_kini:.2f}); tutup atas SMA200',
                'syarat_beli': syarat, 'pencetus': 'rampas low penting + CLV > 0.60', 'paras': round(paras, 2),
                'jarak_pct': round(jarak, 2), 'syarat_dipenuhi': '3/4', 'skor': round(1 - jarak / 2, 3)}
    # Tutup hari ini sudah atas RP: RAMPAS esok memerlukan low esok < RP lalu tutup semula > RP (corak satu hari)
    return {'sebab': f'Low penting {rp:.2f} sah (40 hari, naik > 5% selepasnya); sudah ditembusi (low {lt_kini:.2f}); tutup atas SMA200; tutup hari ini sudah atas low penting',
            'syarat_beli': f'Esok low < {rp:.2f} lalu tutup > {paras:.2f} dengan CLV > 0.60 (tembus semula intrahari dan rampas kuat); henti = low tembusan',
            'pencetus': 'tembus intrahari + rampas + CLV > 0.60', 'paras': None, 'jarak_pct': None,
            'syarat_dipenuhi': '3/4', 'skor': 0.9}
