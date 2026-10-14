from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M67'
NAMA = 'Rayner Teo: Ujian Ketiga pada Purata 50'
VARIAN = 'V6 Versi Financial Wisdom: zon EMA20-EMA50, henti 2xATR'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
BIL_SYARAT = lambda b: b == 3   # V6 = V1 (ujian ketiga tepat) dengan zon EMA20-EMA50


def _rma_atr(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _kira(g):
    c, lo = g.close.values, g.low.values
    e20 = g.close.ewm(span=20, adjust=False).mean(); e50 = g.close.ewm(span=50, adjust=False).mean()
    s200 = g.close.rolling(200).mean()
    naik = ((g.close > s200) & (e50 > e50.shift(10)) & (e20 > e50)).values
    E20, P = e20.values, e50.values
    n = len(g)
    uji = (lo <= E20) & (c >= P)
    atas = lo > E20
    mula = np.zeros(n, bool)
    mula[3:] = uji[3:] & atas[2:-1] & atas[1:-2] & atas[:-3]
    reset = ~naik | (c < P)
    reset[:WARM] = True                      # Andaian laporan: hari pemanasan dianggap set semula
    bil = np.zeros(n, int); b = 0
    for k in range(n):
        if reset[k]: b = 0
        elif mula[k]: b += 1
        bil[k] = b
    # PANTUL: isyarat pertama bagi setiap episod
    pantul = np.zeros(n, bool); kidx = np.full(n, -1)
    sudah = set()
    for i in range(1, n):
        if not (c[i] > c[i - 1] and c[i] > P[i]):
            continue
        for k in range(i - 1, max(i - 6, -1), -1):   # k terkini dahulu
            if mula[k] and (c[k:i + 1] >= P[k:i + 1]).all():
                if k not in sudah:
                    pantul[i] = True; kidx[i] = k; sudah.add(k)
                break
    return naik, mula, bil, pantul, kidx, e20, e50, reset


def sedia(fr, idx):
    for g in fr.values():
        naik, mula, bil, pantul, kidx, e20, e50, reset = _kira(g)
        bk = np.where(kidx >= 0, bil[np.clip(kidx, 0, None)], 0)
        sig = naik & pantul & np.array([BIL_SYARAT(x) for x in bk])
        a = _rma_atr(g)
        # stop = buka_masuk - 2xATR14_i (buka hari i+1). Bar akhir: buka esok belum diketahui -> guna tutup_i (anggaran).
        bm = g.open.shift(-1).fillna(g.close)
        g['_naik'] = naik; g['_bil'] = bil; g['_e20'] = e20; g['_e50'] = e50; g['_mula'] = mula
        g['sig'] = sig   # langkau jika buka_masuk <= stop tidak pernah berlaku kerana stop = buka_masuk - 2xATR
        g['stop'] = bm - 2 * a
        g['tgt'] = np.nan
        g['exitc'] = g.close < e50
        g['rank'] = g.close / g.close.shift(63) - 1


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def hampir(g, idx):
    """Syarat entry V6 (N=8) untuk isyarat esok (i = esok):
       [1] tutup > SMA200 [2] EMA50 > EMA50 10 hari dahulu [3] EMA20 > EMA50  (NAIK, disemak dengan tutup esok = paras)
       [4] ujian zon (MULA: low <= EMA20, tutup >= EMA50, 3 hari sebelumnya low > EMA20) dalam 5 hari terakhir
       [5] ujian itu ialah ujian ketiga (bil = 3) [6] tutup >= EMA50 sejak ujian hingga hari ini
       [7] episod ujian belum menghasilkan pantulan
       [8] PENCETUS: tutup esok > tutup hari ini dan > EMA50 esok."""
    r = g.iloc[-1]; n = len(g)
    if bool(r.sig) or n < PERLU_BAR:
        return None
    naik, mula, bil, pantul, kidx, e20, e50, reset = _kira(g)
    c = g.close.values; P = e50.values
    sudah = set(int(k) for k in kidx if k >= 0)
    k_ = None
    for k in range(n - 1, n - 6, -1):                 # k terkini dahulu (i-1..i-5), sama seperti _kira
        if mula[k] and (c[k:] >= P[k:]).all():
            k_ = k; break
    if k_ is None or k_ in sudah or bil[k_] != 3:    # [4][6][7][5]
        return None
    c0 = float(c[-1])
    paras = max(c0, float(P[-1]))                     # tutup x > EMA50 esok <=> x > EMA50 hari ini
    x = paras * (1 + 1e-6)
    a20, a50 = 2 / 21, 2 / 51
    e20x = e20.values[-1] + a20 * (x - e20.values[-1]); e50x = P[-1] + a50 * (x - P[-1])
    s200x = (c[-199:].sum() + x) / 200
    if not (x > s200x and e50x > P[-10] and e20x > e50x):   # [1][2][3] esok
        return None
    jarak = (paras - c0) / c0 * 100
    # Andaian saya: paras = tutup hari ini, maka jarak_pct = 0 (sebarang kenaikan tutup esok mencetuskan isyarat).
    if jarak < 0 or jarak > 2.0:
        return None
    return _hasil(f'Aliran naik (tutup > SMA200; EMA50 menaik; EMA20 > EMA50); ujian ketiga zon EMA20 ({e20.values[-1]:.2f}) - EMA50 ({P[-1]:.2f}) '
                  f'{n - 1 - k_} hari lalu; tutup kekal >= EMA50; belum ada pantulan',
                  f'Tutup esok > {paras:.2f} (tutup hari ini) dan > EMA50; henti = buka masuk - 2 x ATR14',
                  'Tutup lebih tinggi selepas ujian ketiga', paras, jarak, 7, 8)
