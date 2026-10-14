from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M87'
NAMA = 'IBD Tapak Menaik'
VARIAN = 'V4 V1 tanpa DAHULU'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260


def _zigzag(h, l):
    """Zigzag 10% tanpa pandang ke hadapan. Pulang senarai (bar_sah, tarikh_puncak_idx, nilai) puncak disahkan."""
    n = len(h); puncak = []
    naik = True; HR = h[0]; tHR = 0; LR = np.nan
    for k in range(n):
        if naik:
            if h[k] > HR: HR = h[k]; tHR = k
            if l[k] <= 0.90 * HR:
                puncak.append((k, tHR, HR)); naik = False; LR = l[k]
        else:
            if l[k] < LR: LR = l[k]
            if h[k] >= 1.10 * LR:
                naik = True; HR = h[k]; tHR = k
    return puncak


def _kira(g):
    h, l, c = g.high.values, g.low.values, g.close.values; n = len(g)
    pk = _zigzag(h, l)
    out = {k: np.full(n, np.nan) for k in ['beli', 'P1', 'P2', 'P3', 'T1', 'T2', 'T3', 'tp1']}
    ok = np.zeros(n, bool)  # TANGGA & DALAM & TEMPOH (persediaan), tanpa DAHULU
    p = 0  # bilangan puncak disahkan sehingga i
    for i in range(n):
        while p < len(pk) and pk[p][0] <= i: p += 1
        if p < 3: continue
        (_, t1, P1), (_, t2, P2), (_, t3, P3) = pk[p - 3], pk[p - 2], pk[p - 1]
        T1 = l[t1:t2 + 1].min(); T2 = l[t2:t3 + 1].min(); T3 = l[t3:i + 1].min()
        out['beli'][i] = P3 + 0.10
        for k, v in [('P1', P1), ('P2', P2), ('P3', P3), ('T1', T1), ('T2', T2), ('T3', T3), ('tp1', t1)]: out[k][i] = v
        D = [1 - T1 / P1, 1 - T2 / P2, 1 - T3 / P3]
        tangga = P1 < P2 < P3 and T1 < T2 < T3
        dalam = all(0.10 <= d <= 0.20 for d in D)
        tempoh = 45 <= (i - t1) <= 80
        ok[i] = tangga and dalam and tempoh
    return ok, out


def sedia(fr, idx):
    for g in fr.values():
        ok, o = _kira(g)
        beli = pd.Series(o['beli'], g.index)
        s50 = g.close.rolling(50).mean()
        pecah = (g.close > beli) & (g.close.shift() <= beli) & (g.close <= 1.05 * beli)
        g['_ok'] = ok; g['_beli'] = beli; g['_s50'] = s50; g['_tp1'] = o['tp1']
        g['_P3'] = o['P3']; g['_T3'] = o['T3']
        g['sig'] = pecah & pd.Series(ok, g.index) & (g.close > s50)
        # henti = 0.92 x buka_masuk (buka hari i+1). Andaian saya: bar terakhir (buka esok belum ada) guna tutup_i
        g['stop'] = 0.92 * g.open.shift(-1).fillna(g.close)
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(63) - 1


def hampir(g, idx):
    """Syarat entry V4 (sig): (1) TANGGA (P1<P2<P3, T1<T2<T3); (2) DALAM (setiap undur 10-20%);
    (3) TEMPOH 45-80 hari dari P1; (4) tutup > SMA50; (5) tutup semalam <= titik beli;
    (6) tutup <= 1.05 x titik beli; (7) tutup > titik beli P3+0.10 (pencetus). N = 7."""
    r = g.iloc[-1]; n = len(g)
    if bool(r.sig) or not bool(r._ok) or np.isnan(r._beli) or np.isnan(r._s50):
        return None
    if not (r.close <= r._beli):            # (5) untuk esok: tutup hari ini <= titik beli
        return None
    if not (r.close > r._s50):              # (4) pada bar terakhir
        return None
    # (3) tempoh esok: (n - tp1) mesti dalam 45-80. Andaian saya: P1-P3 tidak berubah esok (puncak baru hanya disahkan selepas jatuh 10%)
    if not (45 <= (n - r._tp1) <= 80):
        return None
    paras = float(r._beli)
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    return {'sebab': f'Tapak menaik: 3 undur 10-20% dengan puncak & dasar makin tinggi (P3 {r._P3:.2f}, T3 {r._T3:.2f}); tempoh dalam 45-80 hari; tutup > SMA50 ({r._s50:.2f}); tutup belum melepasi titik beli',
            'syarat_beli': f'Tutup esok > {paras:.2f} (P3 + 0.10) dan <= {1.05*paras:.2f}, kekal > SMA50',
            'pencetus': 'Tutup > P3+0.10', 'paras': float(round(paras, 4)), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '6/7', 'skor': float(round(1 - jarak / 2, 2))}
