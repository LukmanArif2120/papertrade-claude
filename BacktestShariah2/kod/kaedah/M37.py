from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M37'
NAMA = 'Weinstein Peringkat 2'
VARIAN = 'V2 V1 keluar tutup harian<SMA50 + tutup>SMA50'
TMAX = None
WARM = 400
ADA_HENTI = True
SILANG = False
PERLU_BAR = 420

# Kad Spesifikasi Mesin spec/M37_weinstein_peringkat2.md seksyen 7, varian V2:
# Bar mingguan Isnin-Jumaat daripada data harian; isyarat dinilai pada hari dagangan terakhir minggu w:
#   MA_OK (tutup>SMA30, SMA30>=SMA30[w-4], SMA10>SMA10[w-1]) & PECAH (tutup>R26 & tutup[w-1]<=R26[w-1])
#   & VOL_OK (vol>=2*purata vol w-4..w-1) & KR_OK (RP/purata52(RP)-1>0, RP = tutup saham / tutup SPY hari sama)
#   & tutup harian > SMA50 harian.
# stop = low terendah 4 minggu (w-3..w); langkau jika buka masuk <= stop; exitc = tutup harian < SMA50 (setiap hari).
# Andaian saya: bagi minggu semasa yang belum lengkap (bar akhir data bukan Jumaat), bar akhir dianggap tutup minggu
# sementara, jadi isyarat bar akhir boleh berubah sebelum minggu tamat.


def _mingguan(g, spy):
    wk = g.index.to_period('W-FRI')
    grp = pd.Series(g.index, index=g.index).groupby(wk)
    akhir = grp.transform('max')                       # tarikh hari dagangan terakhir minggu itu
    W = pd.DataFrame({'high': g.high.groupby(wk).max(), 'low': g.low.groupby(wk).min(),
                      'close': g.close.groupby(wk).last(), 'volume': g.volume.groupby(wk).sum(),
                      'tarikh': grp.max()})
    sp = spy.reindex(g.index).ffill()
    W['spy'] = sp.groupby(wk).last().values
    return W, akhir


def _isyarat_mingguan(W):
    c = W.close
    s30 = c.rolling(30).mean(); s10 = c.rolling(10).mean()
    ma_ok = (c > s30) & (s30 >= s30.shift(4)) & (s10 > s10.shift(1))
    r26 = W.high.shift(1).rolling(26).max()
    pecah = (c > r26) & (c.shift(1) <= r26.shift(1))
    vol4 = W.volume.shift(1).rolling(4).mean()
    vol_ok = W.volume >= 2 * vol4
    rp = c / W.spy
    kr = rp / rp.rolling(52).mean() - 1
    kr_ok = kr > 0
    stop = W.low.rolling(4).min()
    return dict(s30=s30, s10=s10, ma_ok=ma_ok, r26=r26, pecah=pecah, vol4=vol4, vol_ok=vol_ok, kr=kr, kr_ok=kr_ok, stop=stop)


def sedia(fr, idx):
    spy = idx['SPY'].close
    for g in fr.values():
        W, akhir = _mingguan(g, spy)
        k = _isyarat_mingguan(W)
        sigw = (k['ma_ok'] & k['pecah'] & k['vol_ok'] & k['kr_ok']).fillna(False)
        tarikh = W.tarikh.values
        sig = pd.Series(False, g.index); stop = pd.Series(np.nan, g.index)
        sig.loc[tarikh] = sigw.values
        stop.loc[tarikh] = k['stop'].values
        s50 = g.close.rolling(50).mean()
        sig = sig & (g.close > s50)
        bk = g.open.shift(-1)
        # langkau jika buka masuk <= henti; Andaian saya: bar terakhir (buka esok belum diketahui) isyarat dikekalkan
        sig = sig & ((bk > stop) | bk.isna())
        g['_s50'] = s50
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (g.close < s50).fillna(False)
        g['rank'] = g.close / g.close.shift(63) - 1


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V2 (5): (1) MA_OK mingguan, (2) KR_OK (kekuatan relatif lawan SPY > 0),
    (3) tutup harian > SMA50, (4) tutup minggu sebelum isyarat <= R26 minggu itu, (5) PENCETUS tutup mingguan > R26
    dengan volum minggu >= 2 x purata 4 minggu sebelumnya.
    (1)-(4) mesti dipenuhi pada bar terakhir; paras = R26 yang akan digunakan pada bar isyarat seterusnya."""
    if len(g) < 300:
        return None
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._s50) or not (r.close > r._s50):
        return None
    W, _ = _mingguan(g[['open', 'high', 'low', 'close', 'volume']], idx['SPY'].close)
    k = _isyarat_mingguan(W)
    if not (bool(k['ma_ok'].iloc[-1]) and bool(k['kr_ok'].iloc[-1])):
        return None
    # Andaian saya: bar terakhir hari Jumaat = minggu lengkap, jadi bar isyarat seterusnya ialah minggu depan;
    # jika bukan Jumaat, minggu semasa masih berjalan dan isyarat boleh berlaku pada mana-mana hari baki minggu ini.
    lengkap = g.index[-1].dayofweek == 4
    if lengkap:
        if not (W.close.iloc[-1] <= k['r26'].iloc[-1]):
            return None
        paras = float(W.high.iloc[-26:].max()); vmin = 2 * float(W.volume.iloc[-4:].mean()); vsudah = 0.0
        bila = 'minggu depan'
    else:
        if not (W.close.iloc[-2] <= k['r26'].iloc[-2]):
            return None
        paras = float(k['r26'].iloc[-1]); vmin = 2 * float(k['vol4'].iloc[-1]); vsudah = float(W.volume.iloc[-1])
        bila = 'minggu ini'
    c_ = float(r.close)
    paras = max(paras, g.close.values[-49:].mean())
    jarak = (paras - c_) / c_ * 100
    if np.isnan(jarak) or not (0 < jarak <= 2.0):
        return None
    return {'sebab': f'Peringkat 2: tutup mingguan > SMA30 (mendatar/naik), SMA10 mingguan naik; kekuatan relatif lawan SPY positif; '
                     f'tutup harian > SMA50 ({r._s50:.2f}); belum pecah high 26 minggu',
            'syarat_beli': f'Tutup mingguan {bila} > {paras:.2f} (high 26 minggu) dengan volum minggu >= {int(vmin):,} '
                           f'(2 x purata 4 minggu' + (f'; terkumpul setakat ini {int(vsudah):,})' if vsudah else ')') + f'; tutup harian > SMA50; beli buka hari dagangan berikutnya',
            'pencetus': 'Tutup mingguan > R26 + volum 2x', 'paras': float(round(paras, 4)), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '4/5', 'skor': float(round(1 - jarak / 2, 3))}
