from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M77'
NAMA = 'Undercut & Rally pada Purata Bergerak (MAU&R)'
VARIAN = 'V2 V1 henti=low hari isyarat'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210


def sedia(fr, idx):
    for g in fr.values():
        c = g.close
        P = c.rolling(50).mean(); s200 = c.rolling(200).mean()
        bawah = c < P; atas = c > P
        ada_atas = atas.astype(int).shift(2).rolling(5).sum() > 0      # wujud ATAS dalam i-6..i-2
        tembus = bawah.shift(1, fill_value=False) & ada_atas
        naikp = P > P.shift(10)
        rng = g.high - g.low
        clv = ((c - g.low) / rng).where(rng > 0, 0.0)
        vol20 = g.volume.shift(1).rolling(20).mean()
        stop = g.low.copy()
        langkau = (g.open.shift(-1) <= stop).fillna(False)   # bar terakhir: buka esok belum diketahui
        g['_P'] = P; g['_s200'] = s200; g['_tembus'] = tembus; g['_naikp'] = naikp; g['_clv'] = clv; g['_vol20'] = vol20
        g['sig'] = tembus & atas & naikp & (c > s200) & (clv > 0.60) & (g.volume > vol20) & ~langkau
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = c < P
        g['rank'] = c / c.shift(63) - 1


def hampir(g, idx):
    # Syarat entry V2 (N=4): TEMBUS (tutup hari ini < SMA50 dan ada tutup > SMA50 dalam 5 hari sebelumnya);
    # NAIKP (SMA50 naik 10 hari); tutup > SMA200;
    # PENCETUS = RAMPAS kuat: tutup esok > SMA50 dengan CLV > 0.60 dan volum > purata 20 hari.
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._P) or np.isnan(r._s200) or len(g) < 210:
        return None
    c = g.close.values.astype(float); P = g._P.values.astype(float)
    if not (c[-1] < P[-1]):
        return None                                   # TEMBUS esok perlu BAWAH hari ini
    if not (c[-6:-1] > P[-6:-1]).any():
        return None                                   # ATAS dalam esok−6..esok−2
    if not (P[-1] > P[-11]):
        return None                                   # NAIKP hari ini
    if not (c[-1] > r._s200):
        return None
    s49 = c[-49:].sum()
    amb = {'rampas': s49 / 49,                        # x > SMA50 esok
           'naikp': 50 * P[-10] - s49,                # SMA50 esok > SMA50 (esok−10)
           'sma200': c[-199:].mean()}                 # x > SMA200 esok
    paras = max(amb.values())
    jarak = (paras - c[-1]) / c[-1] * 100
    if not (0 < jarak <= 2.0):
        return None
    vmin = float(g.volume.iloc[-20:].mean())          # VOL20 esok = purata volum 20 hari terakhir
    return {'sebab': f'Tutup > SMA200; SMA50 menaik 10 hari; tutup baru jatuh bawah SMA50 ({P[-1]:.2f}) selepas berada di atasnya dalam 5 hari',
            'syarat_beli': f'Tutup esok > {paras:.2f} (rampas SMA50) dengan CLV > 0.60 (tutup di 40% atas julat) dan volum > {vmin:,.0f} (purata 20 hari); henti = low hari isyarat',
            'pencetus': 'rampas SMA50 + CLV + volum', 'paras': round(paras, 2), 'jarak_pct': round(jarak, 2),
            'syarat_dipenuhi': '3/4', 'skor': round(1 - jarak / 2, 3)}
