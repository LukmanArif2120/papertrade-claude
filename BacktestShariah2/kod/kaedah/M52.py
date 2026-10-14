from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M52'
NAMA = 'Radge Weekend Trend Trader'
VARIAN = 'V3 V1 keluar tutup<SMA50 harian'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230


def _idx_mingguan(idx):
    s = idx['SPY'].close
    wk = s.index.to_period('W-SUN')
    tms = s.groupby(wk).last()
    return tms > tms.rolling(10).mean()


def sedia(fr, idx):
    IDX = _idx_mingguan(idx)
    for g in fr.values():
        c = g.close
        wk = g.index.to_period('W-SUN')
        ws = pd.Series(wk, g.index)
        akhir = ws != ws.shift(-1)       # bar terakhir saham dalam minggu itu
        tm = c.groupby(wk).last()
        t20 = tm >= tm.rolling(20).max()
        roc = tm / tm.shift(20) - 1
        # Andaian saya: minggu tanpa data SPY (minggu terakhir) guna keadaan SPY terakhir (ffill)
        idxw = IDX.reindex(tm.index).ffill().fillna(False).astype(bool)
        sw = (t20 & (roc >= 0.30) & idxw)
        s50 = c.rolling(50).mean()
        sigw = sw.reindex(wk).values
        sig = pd.Series(sigw, g.index).fillna(False).astype(bool) & akhir & (c > s50)
        g['sig'] = sig
        bo = g.open.shift(-1)
        g['stop'] = (0.60 * bo).fillna(0.60 * c)     # henti keras 0.60 x buka masuk
        g['tgt'] = np.nan
        g['exitc'] = c < s50
        g['rank'] = pd.Series(roc.reindex(wk).values, g.index)
        g['_t20'] = pd.Series(t20.reindex(wk).values, g.index)
        g['_roc'] = g['rank']; g['_idx'] = pd.Series(idxw.reindex(wk).values, g.index)
        g['_s50'] = s50; g['_akhir'] = akhir


def hampir(g, idx):
    # Syarat entry V3 (N=4), dinilai pada tutup hari dagangan terakhir minggu: (1) SPY mingguan > purata
    # 10 minggu; (2) ROC 20 minggu >= 30%; (3) tutup > SMA50 harian; (4) PENCETUS (paras + kalendar):
    # tutup mingguan >= tutup mingguan tertinggi 20 minggu.
    # Hampir: minggu belum tamat dan baki <= 3 hari dagangan ke Jumaat; (1)-(3) benar dengan tutup hari ini
    # sebagai tutup mingguan sementara; pencetus sama ada sudah dipenuhi sementara (jarak 0) atau <= 2%.
    # Andaian saya: minggu tamat hari Jumaat (tiada cuti); baki hari = 4 - hari minggu (Isnin = 0).
    r = g.iloc[-1]
    hari = g.index[-1].dayofweek
    baki = 4 - hari
    if bool(r.sig) or baki < 1 or baki > 3:
        return None
    if not bool(r._idx) or not (r.close > r._s50):
        return None
    wk = g.index.to_period('W-SUN')
    tm = g.close.groupby(wk).last()
    if len(tm) < 21:
        return None
    roc = tm.iloc[-1] / tm.iloc[-21] - 1
    if roc < 0.30:
        return None
    paras = float(tm.iloc[-20:-1].max())
    c0 = float(r.close)
    jarak = max(0.0, (paras - c0) / c0 * 100)
    if jarak > 2.0:
        return None
    roc_min = 1.30 * float(tm.iloc[-21])
    return {'sebab': f'SPY di atas purata 10 minggu; ROC 20 minggu {roc*100:.0f}% (>= 30%); tutup > SMA50 ({r._s50:.2f}); minggu tamat dalam {baki} hari dagangan',
            'syarat_beli': f'Tutup hari terakhir minggu ini >= {paras:.2f} (tutup mingguan tertinggi 20 minggu) dan >= {roc_min:.2f} (ROC 30%), atas SMA50; beli buka minggu depan',
            'pencetus': 'Tutup mingguan tertinggi 20 minggu (hujung minggu)', 'paras': round(paras, 4), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '3/4', 'skor': float(round(1 - jarak / 2, 3))}
