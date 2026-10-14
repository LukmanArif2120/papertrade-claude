from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M84'
NAMA = 'Jarak purata bergerak MAD 21/200'
VARIAN = 'V5 V1 + SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = True          # desil MAD merentas semua saham
PERLU_BAR = 210


def _rma_atr(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _hb(dates):
    """Hujung bulan daripada kalendar dagangan gabungan: hari berikutnya dalam bulan lain.
    Andaian saya: bagi tarikh terakhir data (hari esok belum diketahui), guna hari bekerja berikutnya (BDay,
    tanpa cuti umum) untuk menentukan sama ada hari ini hari dagangan terakhir bulan."""
    d = pd.DatetimeIndex(sorted(dates))
    nxt = pd.Series(d[1:].tolist() + [d[-1] + pd.offsets.BDay(1)], index=d)
    return pd.Series(nxt.dt.month.values != d.month, index=d)


def sedia(fr, idx):
    dates = sorted(set().union(*[g.index for g in fr.values()]))
    hb = _hb(dates)
    mad = {}
    for t, g in fr.items():
        m = g.close.rolling(21).mean() / g.close.rolling(200).mean()
        mad[t] = m.where(g.close >= 5)
    M = pd.DataFrame(mad)
    P = M.rank(axis=1, pct=True) * 100
    for t, g in fr.items():
        s50 = g.close.rolling(50).mean()
        des = (P[t].reindex(g.index) >= 90).fillna(False)
        h = hb.reindex(g.index).fillna(False).astype(bool)
        m = g.close.rolling(21).mean() / g.close.rolling(200).mean()
        g['_mad'] = m; g['_pmad'] = P[t].reindex(g.index); g['_s50'] = s50; g['_hb'] = h
        g['sig'] = h & des & (g.close > s50)
        g['stop'] = g.close - 3 * _rma_atr(g)
        g['tgt'] = np.nan
        g['exitc'] = (h & ~des) | (g.close < s50)
        g['rank'] = m
    # lajur pembantu: kedudukan MAD dalam kalangan calon (DESIL & tutup>SMA50) setiap hari (1 = MAD tertinggi)
    C = pd.DataFrame({t: g._mad.where((g._pmad >= 90) & (g.close > g._s50)) for t, g in fr.items()})
    K = C.rank(axis=1, ascending=False, method='first')
    for t, g in fr.items():
        g['_kd'] = K[t].reindex(g.index)


def hampir(g, idx):
    """Syarat entry V5 (sig): (1) DESIL (persentil MAD21/200 >= 90, tutup >= 5); (2) tutup > SMA50;
    (3) hari dagangan terakhir bulan (pencetus kalendar). N = 3.
    Penapis tambahan watchlist: kedudukan MAD dalam calon (DESIL & tutup>SMA50) <= 8 slot portfolio."""
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._mad) or np.isnan(r._pmad) or bool(r._hb):
        return None
    if not (r._pmad >= 90 and r.close > r._s50):
        return None
    if np.isnan(r._kd) or r._kd > 8:
        return None
    # Andaian saya: hari dagangan = hari bekerja (BDay, tanpa cuti umum), sama seperti _hb()
    d = g.index[-1]
    hb = (d + pd.offsets.BMonthEnd(0)) if d != d + pd.offsets.BMonthEnd(0) else d
    baki = len(pd.bdate_range(d + pd.offsets.BDay(1), hb))
    if baki > 3:
        return None
    return {'sebab': f'MAD21/200 = {r._mad:.3f} dalam desil teratas (persentil {r._pmad:.0f}); tutup > SMA50 ({r._s50:.2f}); kedudukan MAD {int(r._kd)} daripada 8 slot',
            'syarat_beli': f'Kekal dalam desil teratas dan tutup > SMA50 pada {hb.date()} (hari dagangan terakhir bulan, {baki} hari lagi)',
            'pencetus': 'Rotasi hujung bulan', 'paras': None, 'jarak_pct': 0.0,
            'syarat_dipenuhi': '2/3', 'skor': 1.0}
