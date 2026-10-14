from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M96'
NAMA = 'Momo India: Ranking Sharpe 3/6/12 bulan'
VARIAN = 'V1 Dikunci (+henti tutup-3xATR14)'
TMAX = None
WARM = 260
ADA_HENTI = True
SILANG = True
PERLU_BAR = 270


def _skor(c):
    r = c.pct_change()
    s = 0
    for n in (252, 126, 63):
        s = s + (c / c.shift(n) - 1) / (r.rolling(n).std() * np.sqrt(252))
    return s / 3


def sedia(fr, idx):
    S = {}; L = {}
    for t, g in fr.items():
        c = g.close
        # Andaian saya (ikut laporan): puncak = tutup tertinggi sejak mula data.
        lulus = (c >= 0.75 * c.cummax()) & (c > c.rolling(200).mean()) & (c / c.shift(252) - 1 > 0.05)
        S[t] = _skor(c); L[t] = lulus
    S = pd.DataFrame(S); L = pd.DataFrame(L).fillna(False).astype(bool)
    Sl = S.where(L & S.notna())
    ked = Sl.rank(axis=1, ascending=False, method='first')
    tarikh = pd.DatetimeIndex(sorted(set().union(*[g.index for g in fr.values()])))
    hb = set(pd.Series(tarikh, tarikh).groupby(tarikh.to_period('M')).max())
    # Tarikh terakhir data dikira hujung bulan hanya jika hari bekerja berikutnya dalam bulan lain.
    akhir = tarikh[-1]
    if (akhir + pd.offsets.BDay(1)).month == akhir.month:
        hb.discard(akhir)
    for t, g in fr.items():
        k = ked[t].reindex(g.index)
        lu = L[t].reindex(g.index).fillna(False).astype(bool)
        hbs = pd.Series(g.index.isin(list(hb)), g.index)
        g['_ked'] = k; g['_lulus'] = lu; g['_skor'] = S[t].reindex(g.index)
        g['sig'] = hbs & lu & (k <= 8)
        g['stop'] = g.close - 3 * atr(g)          # ATR purata mudah enjin (ikut catatan registry)
        g['tgt'] = np.nan
        g['exitc'] = hbs & (~lu | k.isna() | (k > 20))
        g['rank'] = g['_skor']


def _hari_ke_rotasi(akhir):
    # Andaian saya: hari dagangan terakhir bulan = hari bekerja terakhir bulan (cuti umum tidak diambil kira).
    hb = akhir + pd.offsets.BMonthEnd(0)
    if hb == akhir:
        hb = akhir + pd.offsets.BMonthEnd(1)
    return len(pd.bdate_range(akhir, hb)) - 1, hb


def hampir(g, idx):
    # Syarat entry V1 (dikunci): N = 5
    #   1. tutup >= 75% puncak tutup   2. tutup > SMA200   3. ROC252 > 5%   4. kedudukan SKOR <= 8
    #   5. PENCETUS kalendar: hari dagangan terakhir bulan, mesti dalam <= 3 hari dagangan
    r = g.iloc[-1]
    if bool(r.sig) or not bool(r._lulus) or np.isnan(r._ked) or r._ked > 8:
        return None
    k, hb = _hari_ke_rotasi(g.index[-1])
    if not (1 <= k <= 3):
        return None
    return {'sebab': f'Lulus penapis (>= 75% puncak, > SMA200, pulangan 12 bulan > 5%); kedudukan skor Sharpe #{int(r._ked)} (<= 8)',
            'syarat_beli': f'Beli pada tutup {hb.date()} (hari dagangan terakhir bulan, {k} hari dagangan lagi) jika kekal lulus dan kedudukan <= 8; henti tutup - 3xATR14',
            'pencetus': 'Rotasi hujung bulan', 'paras': None, 'jarak_pct': 0.0,
            'syarat_dipenuhi': '4/5', 'skor': 1.0}
