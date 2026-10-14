from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M49'
NAMA = 'Ichimoku (Tutup Atas Awan + Tenkan Silang Kijun)'
VARIAN = 'V4 V1 + awan hadapan hijau (RA>RB)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230


def _ichi(g):
    h, l = g.high, g.low
    ten = (h.rolling(9).max() + l.rolling(9).min()) / 2
    kij = (h.rolling(26).max() + l.rolling(26).min()) / 2
    ra = (ten + kij) / 2
    rb = (h.rolling(52).max() + l.rolling(52).min()) / 2
    atas = pd.concat([ra.shift(26), rb.shift(26)], axis=1).max(axis=1, skipna=False)
    bawah = pd.concat([ra.shift(26), rb.shift(26)], axis=1).min(axis=1, skipna=False)
    return ten, kij, ra, rb, atas, bawah


def sedia(fr, idx):
    for g in fr.values():
        c = g.close
        ten, kij, ra, rb, atas, bawah = _ichi(g)
        keadaan = (c > atas) & (ten > kij) & (c > kij)
        sig = keadaan & ~keadaan.shift(1, fill_value=False) & (ra > rb)   # V4: tapis pada hari isyarat V1
        stop = kij
        bo = g.open.shift(-1)
        g['sig'] = (sig & ~(bo <= stop)).fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = c < bawah
        g['rank'] = c / c.shift(63) - 1
        g['_ten'] = ten; g['_kij'] = kij; g['_ra'] = ra; g['_rb'] = rb; g['_atas'] = atas; g['_keadaan'] = keadaan


def _keadaan_esok(g, C):
    """Nilai KEADAAN dan RA>RB untuk bar esok jika tutup esok = C (andaikan high = low = C)."""
    h = g.high.values; l = g.low.values
    ten = (max(h[-8:].max(), C) + min(l[-8:].min(), C)) / 2
    kij = (max(h[-25:].max(), C) + min(l[-25:].min(), C)) / 2
    rb = (max(h[-51:].max(), C) + min(l[-51:].min(), C)) / 2
    ra = (ten + kij) / 2
    return ten, kij, ra, rb


def hampir(g, idx):
    # Syarat entry V4 (N=3): (1) awan hadapan hijau (Rentang A > Rentang B) pada hari isyarat;
    # (2) KEADAAN palsu pada hari sebelum isyarat (hari pertama); (3) PENCETUS: KEADAAN benar
    # (tutup > tepi atas awan, Tenkan > Kijun, tutup > Kijun).
    # Hampir: (1) benar hari ini, KEADAAN palsu hari ini, dan ada tutup esok C dalam 2% yang
    # menjadikan KEADAAN dan RA > RB benar esok (carian grid atas C; andaian high = low = C).
    r = g.iloc[-1]
    if bool(r.sig) or bool(r._keadaan) or not (r._ra > r._rb) or len(g) < 80:
        return None
    # Tepi atas awan esok = max(RA, RB) 25 hari lalu (sudah diketahui)
    atas_e = float(max(g._ra.iloc[-26], g._rb.iloc[-26]))
    if np.isnan(atas_e):
        return None
    c0 = float(r.close); paras = None
    for C in np.linspace(c0 * 1.00001, c0 * 1.02, 400):
        ten, kij, ra, rb = _keadaan_esok(g, C)
        if C > atas_e and ten > kij and C > kij and ra > rb:
            paras = float(C); break
    if paras is None:
        return None
    jarak = (paras - c0) / c0 * 100
    if not (0 < jarak <= 2.0):
        return None
    ten, kij, ra, rb = _keadaan_esok(g, paras)
    return {'sebab': f'Awan hadapan hijau (Rentang A {r._ra:.2f} > Rentang B {r._rb:.2f}); keadaan Ichimoku belum lengkap hari ini (syarat hari pertama)',
            'syarat_beli': f'Tutup esok > {paras:.2f} supaya tutup > tepi atas awan ({atas_e:.2f}), Tenkan > Kijun (~{kij:.2f}) dan tutup > Kijun; henti Kijun',
            'pencetus': 'Keadaan Ichimoku lengkap (hari pertama)', 'paras': round(paras, 4), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '2/3', 'skor': float(round(1 - jarak / 2, 3))}
