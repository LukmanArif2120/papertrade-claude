from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M50'
NAMA = 'Elder Triple Screen'
VARIAN = 'V2 V1 keluar tutup<SMA50 + tutup>SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260


def _arus(g):
    """ARUS_i = HISTM minggu siap w(i) > HISTM minggu sebelumnya (MACD 12/26/9 mingguan).
    Minggu kalendar Isnin-Ahad; tutup mingguan = tutup hari dagangan terakhir minggu itu."""
    wk = g.index.to_period('W-SUN')
    akhir = pd.Series(wk, g.index) != pd.Series(wk, g.index).shift(-1)
    # Andaian saya (seperti laporan): bar terakhir data dikira hujung minggu siap
    # hanya jika ia hari Jumaat; untuk scan harian bar lain pada hari terakhir dianggap belum siap.
    akhir.iloc[-1] = g.index[-1].dayofweek == 4
    tm = g.close.groupby(wk).last()
    macd = tm.ewm(span=12, adjust=False).mean() - tm.ewm(span=26, adjust=False).mean()
    hist = macd - macd.ewm(span=9, adjust=False).mean()
    naik = hist > hist.shift(1)
    pos = pd.Series(np.arange(len(tm)), tm.index)
    wpos = pos.reindex(wk).values
    wsiap = np.where(akhir.values, wpos, wpos - 1)
    nv = naik.values
    arus = np.array([bool(nv[k]) if k >= 0 else False for k in wsiap])
    return pd.Series(arus, g.index), akhir


def sedia(fr, idx):
    for g in fr.values():
        c = g.close
        arus, akhir = _arus(g)
        fi2 = ((c - c.shift()) * g.volume).ewm(span=2, adjust=False).mean()
        undur = fi2.shift() < 0
        pecah = g.high > g.high.shift()
        s50 = c.rolling(50).mean()
        sig = arus & undur & pecah & (c > s50)
        stop = pd.concat([g.low, g.low.shift()], axis=1).min(axis=1)
        bo = g.open.shift(-1)
        g['sig'] = (sig & ~(bo <= stop)).fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = c < s50
        g['rank'] = c / c.shift(63) - 1
        g['_arus'] = arus; g['_fi2'] = fi2; g['_s50'] = s50


def hampir(g, idx):
    # Syarat entry V2 (N=4): (1) ARUS: histogram MACD mingguan (minggu siap) naik; (2) UNDUR: Force Index
    # EMA2 semalam < 0; (3) tutup hari isyarat > SMA50; (4) PENCETUS: high hari isyarat > high semalam.
    # Hampir: ARUS benar hari ini, FI2 hari ini < 0, tutup hari ini > SMA50; pencetus esok: high > high hari ini.
    # Andaian saya: ARUS esok = ARUS hari ini (berubah hanya jika esok Jumaat, kerana minggu semasa
    # dikira siap pada Jumaat dan bergantung pada tutup esok).
    r = g.iloc[-1]
    if bool(r.sig) or not bool(r._arus) or not (r._fi2 < 0) or not (r.close > r._s50):
        return None
    paras = float(r.high)
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    s50_esok = float(g.close.iloc[-49:].mean())
    henti = float(r.low)
    return {'sebab': f'Histogram MACD mingguan naik; Force Index 2 hari {r._fi2:,.0f} < 0 (undur); tutup > SMA50 ({r._s50:.2f})',
            'syarat_beli': f'High esok > {paras:.2f} (high hari ini) dan tutup esok > {s50_esok:.2f} (SMA50 esok); beli buka lusa; henti min(low esok, {henti:.2f})',
            'pencetus': 'High > high semalam', 'paras': round(paras, 4), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '3/4', 'skor': float(round(1 - jarak / 2, 3))}
