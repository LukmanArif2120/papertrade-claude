from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M80'
NAMA = 'Radge Saluran Purata Bergerak (MAC)'
VARIAN = 'V2 V1 dengan henti tutup-3xATR14'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230


def _rma_atr(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def sedia(fr, idx):
    for g in fr.values():
        ga = g.high.rolling(10).mean()          # garis atas: SMA10 harga tinggi
        gb = g.low.rolling(8).mean()            # garis bawah: SMA8 harga rendah
        atas = (g.low > ga)
        bawah = (g.high < gb)
        n_atas = atas.astype(int).rolling(5).sum()
        masuk5 = (n_atas == 5) & ~atas.shift(5, fill_value=False).astype(bool)
        keluar5 = bawah.astype(int).rolling(5).sum() == 5
        # bilangan bar ATAS berturut-turut sehingga hari ini
        run = atas.astype(int).groupby((~atas).cumsum()).cumsum()
        g['_ga'] = ga; g['_gb'] = gb; g['_run'] = run
        g['sig'] = masuk5
        g['stop'] = g.close - 3 * _rma_atr(g)
        g['tgt'] = np.nan
        g['exitc'] = keluar5
        g['rank'] = g.close / g.close.shift(63) - 1


def hampir(g, idx):
    """Syarat entry V2 (sig): (1) bar i-5 TIDAK di atas saluran; (2)-(6) bar i-4..i masing-masing rendah > SMA10(tinggi).
    N = 6. Pencetus = bar ke-5 berturut-turut di atas saluran (esok)."""
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._ga) or len(g) < 10:
        return None
    if int(r._run) != 4:          # tepat 4 bar sudah di atas saluran dan bar sebelumnya tidak (syarat 1-5)
        return None
    # Garis atas esok = (jumlah 9 tinggi terakhir + tinggi_esok)/10. Rendah_esok > garis atas esok.
    # Andaian saya: andaikan tinggi esok = rendah esok (= tutup) -> rendah_esok > S9/9 (paras minimum).
    s9 = float(g.high.iloc[-9:].sum())
    paras = s9 / 9
    jarak = (paras - r.close) / r.close * 100
    # Andaian saya: pencetus jenis "kekal di atas paras"; jika tutup sudah di atas paras, jarak = 0
    # (tiada pergerakan naik diperlukan, hanya rendah esok tidak jatuh di bawah paras).
    if jarak > 2.0:
        return None
    jarak = max(0.0, jarak)
    return {'sebab': f'Bar sebelum siri tidak di atas saluran; 4 bar berturut-turut rendah > SMA10 tinggi (garis kini {r._ga:.2f})',
            'syarat_beli': f'Rendah esok > {paras:.2f} (garis atas SMA10 tinggi esok, andai tinggi=rendah; jika tinggi esok H, rendah > ({s9:.2f}+H)/10) — bar ke-5 berturut-turut',
            'pencetus': 'Bar ke-5 di atas saluran', 'paras': float(round(paras, 4)), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '5/6', 'skor': float(round(1 - jarak / 2, 2))}
