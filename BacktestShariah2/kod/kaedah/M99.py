from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M99'
NAMA = 'Three Line Break'
VARIAN = 'V4 V1 + close>SMA200'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
N_BALIK = 3


def _tlb(c, N=N_BALIK):
    """Bina carta Three Line Break hari demi hari (Kad Spesifikasi Mesin).
    Pulangkan per hari: tembus3, dasar (stop), hitambalik, h3_akhir, paras (maks ATAS N garisan terakhir selepas hari i)."""
    n = len(c)
    atas, bawah, warna = [], [], []          # warna: 1 PUTIH, -1 HITAM
    tembus = np.zeros(n, bool); hb = np.zeros(n, bool)
    dasar = np.full(n, np.nan); h3a = np.zeros(n, int); paras = np.full(n, np.nan)
    asas = c[0] if n else np.nan
    for i in range(n):
        x = c[i]
        if np.isnan(x):
            continue
        if not warna:
            if np.isnan(asas):
                asas = x
            elif x > asas:
                atas.append(x); bawah.append(asas); warna.append(1)
            elif x < asas:
                atas.append(asas); bawah.append(x); warna.append(-1)
        else:
            w = warna[-1]
            k = min(N, len(warna))
            if w == 1:
                if x > atas[-1]:
                    bawah.append(atas[-1]); atas.append(x); warna.append(1)
                elif x < min(bawah[-k:]):
                    atas.append(bawah[-1]); bawah.append(x); warna.append(-1); hb[i] = True
            else:
                if x < bawah[-1]:
                    atas.append(bawah[-1]); bawah.append(x); warna.append(-1)
                elif x > max(atas[-k:]):
                    # H3 = bilangan HITAM berturut-turut sejurus sebelum garisan ini
                    h = 0
                    for ww in reversed(warna):
                        if ww == -1: h += 1
                        else: break
                    if h >= 3 and x > max(atas[-3:]):
                        tembus[i] = True
                        dasar[i] = bawah[-1]   # BAWAH garisan HITAM terakhir sebelum hari i
                    bawah.append(atas[-1]); atas.append(x); warna.append(1)
        # keadaan selepas hari i (untuk hampir)
        h = 0
        for ww in reversed(warna):
            if ww == -1: h += 1
            else: break
        h3a[i] = h
        if warna:
            k = min(N, len(warna))
            paras[i] = max(atas[-k:]) if warna[-1] == -1 else np.nan
    return tembus, dasar, hb, h3a, paras


def sedia(fr, idx):
    for g in fr.values():
        c = g.close.values.astype(float)
        tembus, dasar, hb, h3a, paras = _tlb(c)
        s200 = g.close.rolling(200).mean()
        g['_h3'] = h3a; g['_paras'] = paras; g['_s200'] = s200
        stop = pd.Series(dasar, g.index)
        sig = pd.Series(tembus, g.index) & (g.close > s200)
        # Kad: masuk dilangkau jika buka masuk <= henti (buka hari i+1; pada bar akhir tidak diketahui -> isyarat kekal)
        langkau = (g.open.shift(-1) <= stop).fillna(False)
        g['sig'] = sig & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = pd.Series(hb, g.index)
        g['rank'] = g.close / g.close.shift(63) - 1


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}


def hampir(g, idx):
    # Syarat entry V4 (3): (1) >= 3 garisan HITAM berturut-turut; (2) tutup > SMA200; (3) PENCETUS: tutup > maks ATAS tiga garisan HITAM terakhir
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 200:
        return None
    if r._h3 < 3 or np.isnan(r._paras):                      # syarat 1
        return None
    if np.isnan(r._s200) or not (r.close > r._s200):          # syarat 2 (hari ini)
        return None
    c = g.close.values.astype(float)
    s200_min = c[-199:].sum() / 199                           # tutup esok > SMA200 esok  <=>  x > jumlah199/199
    paras = max(r._paras, s200_min)
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    return _hasil(f'{int(r._h3)} garisan HITAM berturut-turut dalam carta Three Line Break; tutup {r.close:.2f} di atas SMA200 ({r._s200:.2f})',
                  f'Tutup esok > {paras:.2f} (ATAS tertinggi tiga garisan HITAM terakhir = {r._paras:.2f}; tutup juga mesti kekal > SMA200 esok). '
                  f'Masuk dibatalkan jika harga buka hari masuk <= dasar garisan HITAM terakhir',
                  'Garisan PUTIH pembalikan (tembus 3 garisan)', paras, jarak, 2, 3)
