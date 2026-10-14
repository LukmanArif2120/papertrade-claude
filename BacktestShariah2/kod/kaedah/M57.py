from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M57'
NAMA = 'Landry Trend Knockout (TKO)'
VARIAN = 'V1 Dikunci (keluar tutup<SMA50)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260


def _aliran(g, s50, lag):
    c, h = g.close, g.high
    a = (c > s50) & (s50 > s50.shift(10)) & (c / c.shift(63) - 1 >= 0.15) & \
        (h.rolling(10).max() >= h.rolling(63).max())
    return a.shift(lag).fillna(False).astype(bool)


def sedia(fr, idx):
    for g in fr.values():
        s50 = g.close.rolling(50).mean()
        lo = g.low
        ko = lo < np.minimum(lo.shift(1), lo.shift(2))
        ko1 = ko.shift(1).fillna(False).astype(bool)
        aliran = _aliran(g, s50, 2)            # dinilai pada i-2
        sah = ko1 & (g.high > g.high.shift(1))
        stop = np.minimum(lo.shift(1), lo)
        sig = aliran & sah & (g.close > s50)
        # Langkau jika buka_masuk <= stop (bar akhir: buka esok belum diketahui -> isyarat dikekalkan)
        # Andaian saya: dilaksana dengan buka hari i+1 kerana enjin tiada pilihan langkau; ini bukan pandang ke hadapan untuk scan hari terakhir.
        langkau = (g.open.shift(-1) <= stop)
        g['_aliran1'] = _aliran(g, s50, 1)
        g['_ko'] = ko & (g.close > s50)
        g['sig'] = sig & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(63) - 1


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def hampir(g, idx):
    """Syarat entry V1 (N=7) untuk isyarat esok (i = esok):
       ALIRAN dinilai pada i-2 = semalam: [1] tutup > SMA50 [2] SMA50 > SMA50 10 hari dahulu [3] ROC63 >= 15%
       [4] high 10 hari >= high 63 hari; [5] bar tumbang (KO) pada i-1 = hari ini (low < dua low sebelumnya);
       [6] tutup > SMA50 (dinilai hari ini sebagai keadaan semasa; esok mesti kekal);
       [7] PENCETUS: high esok > high bar tumbang (hari ini).
       Paras = max(high hari ini, tutup minimum esok supaya tutup > SMA50 esok)."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < PERLU_BAR:
        return None
    if not (bool(r._aliran1) and bool(r._ko)):      # [1]-[4] semalam, [5] KO hari ini dan [6] tutup > SMA50 hari ini
        return None
    c = g.close.values
    s50_min = c[-49:].mean()        # tutup esok x > (sum49 + x)/50  <=>  x > purata 49 tutup terakhir
    paras = max(float(r.high), float(s50_min))
    jarak = (paras - r.close) / r.close * 100
    if jarak <= 0 or jarak > 2.0:
        return None
    st = min(r.low, g.low.iloc[-2])
    syarat = f'High esok > {r.high:.2f} (high bar tumbang)'
    if s50_min > r.high:
        syarat += f' dan tutup esok > {s50_min:.2f} (SMA50)'
    else:
        syarat += f'; tutup esok kekal > {s50_min:.2f} (SMA50)'
    return _hasil('Aliran kuat semalam (tutup > SMA50; SMA50 menaik 10 hari; ROC63 >= 15%; high 10 hari = high 63 hari); '
                  'hari ini bar tumbang (low di bawah dua low sebelumnya) dan tutup > SMA50',
                  syarat + f'; henti = {st:.2f}', 'High > high bar tumbang', paras, jarak, 6, 7)
