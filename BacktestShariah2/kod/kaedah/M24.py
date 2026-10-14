from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M24'
NAMA = 'Rotasi Momentum ROC12 + SMA200'
VARIAN = 'V0 Sumber tulen (K=2, tiada henti)'
TMAX = None
WARM = 260
ADA_HENTI = False
SILANG = True
PERLU_BAR = 260
K = 2
# Nota: backtest V0 memakai portfolio 2 slot x 50% (slot = K). uji_kaedah.py memakai 8 x 12.5%,
# jadi CAGR semakan tidak setanding; isyarat (n) sepatutnya sama.


def sedia(fr, idx):
    cl = pd.DataFrame({t: g.close for t, g in fr.items()}).sort_index()
    dts = cl.index
    nxt = pd.Series(dts, index=dts).shift(-1)
    me = pd.Series([pd.notna(nxt.iloc[k]) and dts[k].month != nxt.iloc[k].month for k in range(len(dts))], index=dts)
    # Andaian saya: bar terakhir gabungan dianggap akhir bulan jika hari bekerja berikutnya jatuh dalam bulan lain
    if len(dts):
        last = dts[-1]
        me.iloc[-1] = (last + pd.offsets.BDay(1)).month != last.month
    roc12 = pd.DataFrame({t: g.close / g.close.shift(252) - 1 for t, g in fr.items()}).reindex(dts)
    s200 = pd.DataFrame({t: g.close.rolling(200).mean() for t, g in fr.items()}).reindex(dts)
    atas = cl > s200
    lay = atas & roc12.notna() & pd.DataFrame({t: me for t in cl.columns})
    rk = roc12.where(lay).rank(axis=1, ascending=False)
    # Kedudukan semasa (setiap hari, bukan hanya akhir bulan) untuk hampir()
    rk_hari = roc12.where(atas & roc12.notna()).rank(axis=1, ascending=False)
    for t, g in fr.items():
        L = lay[t].reindex(g.index).fillna(False).astype(bool)
        top = (rk[t].reindex(g.index) <= K).fillna(False)
        m = me.reindex(g.index).fillna(False).astype(bool)
        g['sig'] = L & top
        g['stop'] = np.nan
        g['tgt'] = np.nan
        g['exitc'] = m & (~L | ~top)
        g['rank'] = roc12[t].reindex(g.index)
        g['_rkh'] = rk_hari[t].reindex(g.index)
        g['_me'] = m


def hampir(g, idx):
    # Piawaian ketat: syarat entry V0 = (1) close > SMA200, (2) ROC12 wujud, (3) kedudukan ROC12 <= K,
    # (4) PENCETUS kalendar: hari dagangan terakhir bulan. Calon hanya jika 1-3 dipenuhi hari ini
    # dan rotasi seterusnya <= 3 hari dagangan lagi.
    r = g.iloc[-1]
    if bool(r.sig) or pd.isna(r._rkh) or r._rkh > K:
        return None
    last = g.index[-1]
    akhir = last + pd.offsets.BMonthEnd(0)
    # Andaian saya: hari dagangan = hari bekerja Isnin-Jumaat (cuti umum AS tidak ditolak)
    baki = len(pd.bdate_range(last + pd.Timedelta(days=1), akhir))
    if baki < 1 or baki > 3:
        return None
    return {'sebab': f'Tutup > SMA200; ROC12 {r["rank"]*100:.0f}% wujud; kedudukan ROC12 #{int(r._rkh)} (dalam {K} teratas) hari ini',
            'syarat_beli': f'Kekal > SMA200 dan dalam {K} teratas ROC12 pada tutup {akhir:%d %b %Y} (hari dagangan terakhir bulan, {baki} hari lagi); beli pada buka hari pertama bulan baharu',
            'pencetus': 'rotasi akhir bulan', 'paras': None, 'jarak_pct': 0.0,
            'syarat_dipenuhi': '3/4', 'skor': 1.0}
