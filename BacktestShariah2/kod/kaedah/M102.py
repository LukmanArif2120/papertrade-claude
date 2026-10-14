from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M102'
NAMA = 'Stockbee SLTB'
VARIAN = 'V5 V1 + volum hari ini > semalam'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210


def _asas(g):
    c = g.close
    R = c / c.shift(1) - 1
    ti65 = c.rolling(7).mean() / c.rolling(65).mean()
    minv = g.volume.shift(1).rolling(3).min()
    s50 = c.rolling(50).mean()
    return R, ti65, minv, s50


def sedia(fr, idx):
    for g in fr.values():
        R, ti65, minv, s50 = _asas(g)
        c = g.close
        sltb = (minv >= 100000) & (c >= 3) & (ti65 >= 1.05) & (c > g.open) & (c > c.shift(1)) \
            & (R > R.shift(1)) & (R.shift(1) < 0.02)
        sig = sltb & (c > s50) & (g.volume > g.volume.shift(1))
        stop = g.low.copy()
        # Kad: masuk dilangkau jika buka masuk <= stop
        langkau = (g.open.shift(-1) <= stop).fillna(False)
        g['_ti65'] = ti65; g['_minv'] = minv; g['_s50'] = s50; g['_R'] = R
        g['sig'] = sig & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = c < s50
        # Andaian (laporan): isyarat tanpa ROC63 diberi rank paling rendah
        g['rank'] = (c / c.shift(63) - 1).fillna(-1e9)


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}


def hampir(g, idx):
    # Syarat entry V5 (6): (1) volum min 3 hari (hari ini, semalam, kelmarin) >= 100,000; (2) tutup >= 3; (3) TI65 >= 1.05;
    # (4) R hari ini < 2% (menjadi R semalam bagi esok); (5) tutup > SMA50;
    # (6) PENCETUS (hari esok): tutup > buka, tutup > tutup hari ini, R esok > R hari ini, volum esok > volum hari ini
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 65:
        return None
    c = g.close.values.astype(float)
    if not (g.volume.iloc[-3:].min() >= 100000):                     # 1
        return None
    if not (r.close >= 3):                                           # 2
        return None
    if np.isnan(r._ti65) or not (r._ti65 >= 1.05):                   # 3
        return None
    if np.isnan(r._R) or not (r._R < 0.02):                          # 4
        return None
    if np.isnan(r._s50) or not (r.close > r._s50):                   # 5
        return None
    # Paras tutup esok: kenaikan > R hari ini (dan > 0), TI65 esok >= 1.05, tutup > SMA50 esok, tutup >= 3
    p_r = r.close * (1 + max(r._R, 0.0))
    s6, s64 = c[-6:].sum(), c[-64:].sum()
    p_ti = (1.05 * s64 / 65 - s6 / 7) / (1 / 7 - 1.05 / 65)
    p_s50 = c[-49:].sum() / 49
    paras = max(p_r, p_ti, p_s50, 3.0)
    # Andaian saya: jika R hari ini <= 0, sebarang kenaikan esok memadai; jarak_pct = 0 (paras = tutup hari ini, mesti dilepasi)
    jarak = max(0.0, (paras - r.close) / r.close * 100)
    if jarak > 2.0:
        return None
    return _hasil(f'Volum min 3 hari {int(g.volume.iloc[-3:].min()):,} (>= 100,000); tutup {r.close:.2f} >= 3; TI65 {r._ti65:.3f} (>= 1.05); '
                  f'perubahan hari ini {r._R*100:+.2f}% (< 2%); tutup > SMA50 ({r._s50:.2f})',
                  f'Esok: tutup > {paras:.2f}, tutup > harga buka (lilin hijau), dan volum > {int(r.volume):,} (volum hari ini); '
                  f'henti = low hari isyarat; masuk dibatalkan jika harga buka hari masuk <= henti',
                  'Hari SLTB (pecutan + lilin hijau + volum naik)', paras, jarak, 5, 6)
