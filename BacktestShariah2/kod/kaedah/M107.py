from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M107'
NAMA = 'Golden Cross SMA50/200'
VARIAN = 'V5 V1 + SPY>SMA200'
TMAX = None
WARM = 201
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260


def _rma_atr(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _spy_ok(idx, index):
    s = idx['SPY'].close
    ok = s > s.rolling(200).mean()
    return ok.reindex(index, method='ffill').fillna(False).astype(bool)


def sedia(fr, idx):
    for g in fr.values():
        s50 = g.close.rolling(50).mean(); s200 = g.close.rolling(200).mean()
        emas = (s50 > s200) & (s50.shift() <= s200.shift())
        spy = _spy_ok(idx, g.index)
        g['_s50'] = s50; g['_s200'] = s200; g['_spy'] = spy
        g['sig'] = emas & spy
        g['stop'] = g.close - 3 * _rma_atr(g)
        g['tgt'] = np.nan
        g['exitc'] = s50 < s200
        g['rank'] = g.close / g.close.shift(63) - 1


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}


def hampir(g, idx):
    # Syarat entry V5 (3): (1) SMA50 <= SMA200 hari ini (belum silang); (2) SPY > SMA200 SPY;
    # (3) PENCETUS: SMA50 memotong ke atas SMA200 pada tutup esok
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 201 or np.isnan(r._s200) or np.isnan(r._s50):
        return None
    if not (r._s50 <= r._s200):                         # 1
        return None
    if not bool(r._spy):                                # 2
        return None
    c = g.close.values.astype(float)
    a50 = c[-49:].sum() / 50; a200 = c[-199:].sum() / 200
    paras = (a200 - a50) / (1 / 50 - 1 / 200)           # tutup esok minimum untuk SMA50 esok > SMA200 esok
    # Andaian saya: jika paras <= tutup hari ini, silang berlaku walaupun harga tidak naik; jarak_pct = 0
    jarak = max(0.0, (paras - r.close) / r.close * 100)
    if jarak > 2.0:
        return None
    return _hasil(f'SMA50 ({r._s50:.2f}) hanya {(r._s200/r._s50-1)*100:.2f}% di bawah SMA200 ({r._s200:.2f}); SPY di atas SMA200',
                  f'Tutup esok > {max(paras, 0):.2f} supaya SMA50 memotong ke atas SMA200; SPY kekal di atas SMA200',
                  'Golden Cross SMA50/200', max(paras, 0.0), jarak, 2, 3)
