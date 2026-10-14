from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M64'
NAMA = "O'Neil Tiga Minggu Ketat"
VARIAN = 'V5 V1 henti 0.92xPIVOT'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
KETAT, SAH = 0.015, 15


def _mingguan(g):
    # Bar mingguan Isnin-Ahad; e = kedudukan hari dagangan terakhir minggu itu dalam g
    pos = pd.Series(np.arange(len(g)), g.index)
    wk = g.index.to_period('W-SUN')
    w = pd.DataFrame({'c': g.close.groupby(wk).last(), 'h': g.high.groupby(wk).max(),
                      'l': g.low.groupby(wk).min(), 'e': pos.groupby(wk).last()})
    c = w.c
    ketat = ((c.shift(1) / c.shift(2) - 1).abs() <= KETAT) & ((c / c.shift(1) - 1).abs() <= KETAT)
    naik = c.shift(2) / c.shift(10) - 1 >= 0.20
    w['corak'] = ketat & naik
    w['pv'] = pd.concat([w.h, w.h.shift(1), w.h.shift(2)], axis=1).max(axis=1) + 0.10
    w['lowc'] = pd.concat([w.l, w.l.shift(1), w.l.shift(2)], axis=1).min(axis=1)
    return w


def sedia(fr, idx):
    for g in fr.values():
        n = len(g); cl = g.close.values
        w = _mingguan(g)
        # Andaian saya: minggu terakhir data (mungkin belum lengkap) dianggap lengkap pada hari terakhirnya;
        # corak minggu itu hanya mempengaruhi hari selepas e_w, maka tiada kesan pada isyarat sedia ada.
        cw = w[w.corak]
        ev = cw.e.values.astype(int); pv = cw.pv.values
        piv = np.full(n, np.nan); eact = np.full(n, -1)
        k = -1
        for i in range(n):
            while k + 1 < len(ev) and ev[k + 1] < i:
                k += 1
            if k >= 0 and 1 <= i - ev[k] <= SAH:
                piv[i] = pv[k]; eact[i] = ev[k]
        sig = np.zeros(n, bool)
        for i in range(n):
            if eact[i] < 0 or not cl[i] > piv[i]:
                continue
            e = eact[i]
            if (cl[e + 1:i] > piv[i]).any():
                continue
            sig[i] = True
        s50 = g.close.rolling(50).mean()
        g['_piv'] = piv; g['_e'] = eact
        g['sig'] = pd.Series(sig, g.index) & (g.close > s50)
        g['stop'] = 0.92 * g['_piv']
        g['tgt'] = np.nan
        g['exitc'] = g.close < s50
        g['rank'] = g.close / g.close.shift(63) - 1


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def hampir(g, idx):
    """Syarat entry V5 (N=6) untuk isyarat esok (i = esok):
       [1] corak tiga minggu ketat (dua perubahan tutup mingguan berturut-turut <= 1.5%) [2] naik >= 20% dalam 8 minggu sebelum corak
       [3] esok masih dalam 15 hari dagangan selepas minggu corak [4] pecahan pertama (tiada tutup > titik beli sejak corak)
       [5] tutup > SMA50 (keadaan hari ini; esok mesti kekal) [6] PENCETUS: tutup esok > titik beli (high 3 minggu + 0.10).
       Corak aktif esok = corak terkini dengan hari akhir minggu e < esok (termasuk minggu semasa jika berakhir hari ini)."""
    r = g.iloc[-1]; n = len(g)
    if bool(r.sig) or n < PERLU_BAR:
        return None
    # Andaian saya: minggu terakhir data dianggap lengkap (sama seperti sedia()).
    w = _mingguan(g)
    cw = w[w.corak & (w.e <= n - 1)]
    if cw.empty:
        return None
    e = int(cw.e.iloc[-1]); piv = float(cw.pv.iloc[-1])
    if not (1 <= n - e <= SAH):                       # [3]
        return None
    cl = g.close.values
    if (cl[e + 1:] > piv).any():                      # [4]
        return None
    s50 = cl[-50:].mean()
    if not cl[-1] > s50:                              # [5]
        return None
    s50_min = cl[-49:].mean()
    paras = max(piv, s50_min)
    jarak = (paras - r.close) / r.close * 100
    if jarak <= 0 or jarak > 2.0:
        return None
    baki = SAH - (n - e)
    return _hasil(f'Tiga minggu ketat (tutup mingguan dalam 1.5%) selepas naik >= 20%; belum pecah titik beli; tutup > SMA50 ({s50:.2f}); corak sah {baki} hari lagi selepas esok',
                  f'Tutup esok > {paras:.2f} (titik beli {piv:.2f}); henti 0.92 x titik beli = {0.92*piv:.2f}',
                  'Tutup > titik beli', paras, jarak, 5, 6)
