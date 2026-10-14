from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M06'
NAMA = 'Minervini VCP Breakout'
VARIAN = 'V5 V1 tanpa VCP'
TMAX = None
WARM = 252
ADA_HENTI = True
SILANG = True          # persentil RS dikira merentas semua saham
PERLU_BAR = 260


def _rsp(fr):
    cl = pd.DataFrame({t: g.close for t, g in fr.items()})
    rs = 0.4 * (cl / cl.shift(63) - 1) + 0.2 * (cl / cl.shift(126) - 1) + 0.2 * (cl / cl.shift(189) - 1) + 0.2 * (cl / cl.shift(252) - 1)
    return rs.rank(axis=1, pct=True) * 100


def sedia(fr, idx):
    RSP = _rsp(fr)
    for t, g in fr.items():
        o, h, l, c, v = g.open, g.high, g.low, g.close, g.volume
        s50, s150, s200 = c.rolling(50).mean(), c.rolling(150).mean(), c.rolling(200).mean()
        rsp = RSP[t].reindex(g.index)
        TT = (c > s50) & (s50 > s150) & (s150 > s200) & (s200 > s200.shift(21)) & \
             (c >= 1.3 * l.rolling(252).min()) & (c >= 0.75 * h.rolling(252).max()) & (rsp >= 70)
        VOLA = v.rolling(50).mean().shift(1)
        PIV = h.shift(1).rolling(15).max()                 # high tertinggi i-15..i-1 (blok B3)
        LB3 = l.shift(1).rolling(15).min()
        sig = TT & (c > PIV) & (c.shift() <= PIV) & (v >= 1.4 * VOLA)
        bm = o.shift(-1)
        # henti = max(0.99 x low B3, 0.92 x buka_masuk); bar terakhir: buka esok belum diketahui -> 0.99 x low B3
        stop = pd.concat([0.99 * LB3, 0.92 * bm], axis=1).max(axis=1)
        # langkau: buka_masuk <= henti atau buka_masuk > 1.05 x pangsi
        ok = ((bm > stop) & (bm <= 1.05 * PIV)) | bm.isna()
        g['_tt'] = TT.fillna(False); g['_piv'] = PIV; g['_vola'] = VOLA; g['_rsp'] = rsp
        g['sig'] = (sig & ok).fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (c < s50).fillna(False)
        g['rank'] = rsp.fillna(0)



def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def hampir(g, idx):
    """Syarat entry V5 (N=9): Trend Template [1] tutup > SMA50 [2] SMA50 > SMA150 [3] SMA150 > SMA200
       [4] SMA200 naik 21 hari [5] tutup >= 1.3 x low 252 hari [6] tutup >= 0.75 x high 252 hari [7] persentil RS >= 70;
       [8] tutup semalam <= pangsi; [9] PENCETUS: tutup > pangsi (high 15 hari) DENGAN volume >= 1.4 x SMA50 volume (semalam)."""
    r = g.iloc[-1]
    if bool(r.sig) or not bool(r._tt) or np.isnan(r._piv):
        return None
    # Andaian saya: persentil RS esok = persentil RS hari ini (silang saham; tidak boleh dikira untuk satu saham)
    paras = float(g.high.iloc[-15:].max()); c0 = float(r.close)          # pangsi esok = high 15 hari termasuk hari ini
    jarak = (paras - c0) / c0 * 100
    if jarak > 2.0:
        return None
    vmin = 1.4 * float(g.volume.iloc[-50:].mean())
    return _hasil(f'Trend Template lulus (tutup > SMA50 > SMA150 > SMA200, SMA200 menaik, >= 30% atas low 52 minggu, <= 25% bawah high 52 minggu, persentil RS {r._rsp:.0f})',
                  f'Tutup esok > {paras:.2f} (high 15 hari) DAN volume esok >= {vmin:,.0f} (1.4 x SMA50 volume); langkau jika buka esok > {1.05*paras:.2f}',
                  'Pecah pangsi 15 hari + volume', paras, jarak, 8, 9)
