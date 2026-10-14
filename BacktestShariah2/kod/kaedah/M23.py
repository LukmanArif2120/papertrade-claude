from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M23'
NAMA = 'Breitstein Kapitulasi + Kesinambungan'
VARIAN = 'V5 V4 keluar close<SMA20'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210


def sedia(fr, idx):
    for g in fr.values():
        o, h, c, v = g.open, g.high, g.close, g.volume
        R = h.shift(1).rolling(126).max()
        VS50 = v.rolling(50).mean()            # laporan/kod 8.2: purata 50 hari termasuk hari i
        sig = (c > R) & (c.shift() <= R.shift()) & (v >= 1.5 * VS50)
        # Andaian saya (laporan M23): langkau jika buka masuk <= henti R
        lk = (o.shift(-1) <= R).fillna(False)
        g['_R'] = R; g['_VS50'] = VS50
        g['sig'] = (sig & ~lk).fillna(False)
        g['stop'] = R
        g['tgt'] = np.nan
        g['exitc'] = c < c.rolling(20).mean()
        g['rank'] = v / VS50


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V5 (kod sedia, PADAN registry), N=3:
    1 tutup hari ini <= high tertinggi 126 hari sebelumnya (pecahan esok kali pertama);
    2 PENCETUS: tutup esok > high tertinggi 126 hari (termasuk high hari ini);
    3 volume esok >= 1.5× purata 50 hari (termasuk esok) — pencetus volum, dinyatakan sebagai minimum."""
    if len(g) < 140: return None
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._R): return None
    if not r.close <= r._R: return None                    # 1
    paras = g.high.iloc[-126:].max()                       # R esok = max high hari i-125..i
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0): return None
    # v >= 1.5 × (S49 + v)/50  <=>  v >= 0.03 × S49 / 0.97 (tepat)
    vmin = 0.03 * g.volume.iloc[-49:].sum() / 0.97
    return {'sebab': f'Tutup hari ini belum melepasi high 126 hari; harga {jarak:.2f}% di bawah paras {paras:.2f}',
            'syarat_beli': f'Tutup esok > {paras:.2f} (high 126 hari) dengan volume >= {vmin:,.0f} (1.5× purata 50 hari); '
                           f'henti {paras:.2f}; langkau jika buka masuk <= henti; keluar tutup < SMA20',
            'pencetus': 'Pecah high 126 hari + volume', 'paras': round(float(paras), 2), 'jarak_pct': round(float(jarak), 2),
            'syarat_dipenuhi': '2/3', 'skor': round(1 - jarak / 2, 3)}
