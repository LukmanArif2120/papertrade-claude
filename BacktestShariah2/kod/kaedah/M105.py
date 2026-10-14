from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M105'
NAMA = 'Supertrend tulen'
VARIAN = 'V1 Dikunci (V0 + had henti 12%)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
N, M = 10, 3.0


def _atr_rma(g, n):
    # ATR Wilder (RMA); nilai pertama = purata mudah n julat sebenar pertama (Andaian saya, sama seperti laporan M105/M33)
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1).values
    out = np.full(len(tr), np.nan)
    if len(tr) < n: return out
    out[n - 1] = tr[:n].mean()
    for i in range(n, len(tr)):
        out[i] = (out[i - 1] * (n - 1) + tr[i]) / n
    return out


def _supertrend(g, n=N, m=M):
    a = _atr_rma(g, n); hl2 = ((g.high + g.low) / 2).values; c = g.close.values; L = len(c)
    ba = hl2 + m * a; bb = hl2 - m * a
    ga = np.full(L, np.nan); gb = np.full(L, np.nan); naik = np.zeros(L, bool); st = np.full(L, np.nan)
    s = n - 1
    if L <= s: return ga, gb, naik, st
    ga[s], gb[s], naik[s] = ba[s], bb[s], False   # bar pertama ATR: ARAH = TURUN
    st[s] = ga[s]
    for i in range(s + 1, L):
        gb[i] = bb[i] if (bb[i] > gb[i - 1] or c[i - 1] < gb[i - 1]) else gb[i - 1]
        ga[i] = ba[i] if (ba[i] < ga[i - 1] or c[i - 1] > ga[i - 1]) else ga[i - 1]
        if c[i] > ga[i - 1]: naik[i] = True
        elif c[i] < gb[i - 1]: naik[i] = False
        else: naik[i] = naik[i - 1]
        st[i] = gb[i] if naik[i] else ga[i]
    return ga, gb, naik, st


def sedia(fr, idx):
    for g in fr.values():
        ga, gb, naik, st = _supertrend(g)
        naik_s = pd.Series(naik, g.index)
        pecah = naik_s & ~naik_s.shift(1, fill_value=True)
        stop = np.maximum(pd.Series(st, g.index), g.close * 0.88)
        # Langkau jika buka masuk <= henti (ikut laporan M105). Bar terakhir: buka esok belum diketahui -> isyarat kekal.
        langkau = (g.open.shift(-1) <= stop).fillna(False)
        g['_ga'] = ga; g['_naik'] = naik
        g['sig'] = pecah & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = ~naik_s          # tutup < ST (ARAH bertukar TURUN)
        g['rank'] = g.close / g.close.shift(63) - 1


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}


def hampir(g, idx):
    # Syarat entry V1 (2): (1) Supertrend 10/3 arah TURUN hari ini; (2) PENCETUS: tutup esok > garisan atas (GA) hari ini -> arah bertukar NAIK
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._ga):
        return None
    if bool(r._naik):                                   # 1
        return None
    paras = r._ga
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    return _hasil('Supertrend 10/3 masih merah (arah turun)',
                  f'Tutup esok > {paras:.2f} (garisan Supertrend atas) supaya arah bertukar naik; henti = maks(garisan bawah, 0.88 x tutup); '
                  f'masuk dibatalkan jika harga buka hari masuk <= henti',
                  'Supertrend bertukar hijau', paras, jarak, 1, 2)
