from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M78'
NAMA = 'Alvarez Pecahan Mingguan DTAYS'
VARIAN = 'V2 V1 henti mengekor 5xATR100'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210
K_ATR = 5


def _rma_atr(g, n):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _hm(g):
    ix = g.index
    minggu = ix.to_period('W-SUN')          # minggu kalendar Isnin–Ahad
    hm = pd.Series(minggu[:-1] != minggu[1:], index=ix[:-1]).reindex(ix)
    # Andaian saya: bar terakhir data dianggap hujung minggu jika ia hari Jumaat (untuk scan; tiada kesan pada backtest
    # kerana enjin tidak masuk pada isyarat bar terakhir)
    hm.iloc[-1] = ix[-1].weekday() == 4
    return hm.astype(bool)


def _exitc_ekor(g, warm):
    """Replika urutan dagangan enjin untuk henti mengekor bergantung dagangan: tutup_j < TT_j - K x ATR100_j."""
    o, l, c = g.open.values, g.low.values, g.close.values
    sig = g.sig.fillna(False).astype(bool).values; st = g.stop.astype(float).values
    a = g._atr100.values; n = len(g); ex = np.zeros(n, bool); i = warm
    while i < n - 1:
        if not sig[i]: i += 1; continue
        sp = st[i] if not np.isnan(st[i]) else -np.inf
        j = i + 1; tt = -np.inf; keluar = n - 1
        while j < n:
            if j > i + 1 and o[j] <= sp: keluar = j; break
            if l[j] <= sp: keluar = j; break
            tt = max(tt, c[j])
            if c[j] < tt - K_ATR * a[j] and j + 1 < n:
                ex[j] = True; keluar = j + 1; break
            j += 1
        i = keluar + 1
    return ex


def sedia(fr, idx):
    spy = idx['SPY'].close
    mkt_spy = spy > spy.rolling(100).mean()
    for g in fr.values():
        c = g.close
        hm = _hm(g)
        tm = c[hm]                                     # tutup mingguan (hari terakhir setiap minggu)
        high20 = tm >= tm.shift(1).rolling(19).max()
        ret20 = tm / tm.shift(20) - 1
        H20 = high20.reindex(g.index).fillna(False).astype(bool)
        R20 = ret20.reindex(g.index)
        dv21 = (c * g.volume).rolling(21).mean()
        mkt = mkt_spy.reindex(g.index, method='ffill').fillna(False).astype(bool)
        g['_hm'] = hm; g['_ret20'] = R20; g['_dv21'] = dv21; g['_mkt'] = mkt
        g['_atr100'] = _rma_atr(g, 100)
        g['sig'] = hm & H20 & (R20 > 0.30) & (dv21 > 15e6) & mkt
        # Henti keras 0.92 x buka masuk (buka i+1). Pada bar terakhir buka esok belum diketahui -> NaN (scan: henti = 0.92 x harga masuk sebenar)
        g['stop'] = 0.92 * g.open.shift(-1)
        g['tgt'] = np.nan
        g['rank'] = R20.fillna(0.0)
        g['exitc'] = _exitc_ekor(g, WARM)
        # Andaian saya: untuk papertrade, keluar = tutup < (tutup tertinggi sejak masuk - 5 x ATR100 Wilder), jual buka esok


def hampir(g, idx):
    # Syarat entry V2 (N=4): pulangan 20 minggu > 30%; purata nilai dagangan 21 hari > USD15 juta; SPY > SMA100;
    # PENCETUS = tutup hari terakhir minggu >= high tutup mingguan 19 minggu sebelumnya (pecahan high 20 minggu).
    # Minggu sasaran: jika hari ini hujung minggu -> minggu depan; jika tidak -> minggu semasa.
    r = g.iloc[-1]
    if bool(r.sig) or not bool(r._mkt) or not (r._dv21 > 15e6):
        return None
    c = g.close
    tm = c[g._hm.astype(bool)]                       # tutup mingguan minggu yang SUDAH tamat
    if len(tm) < 21:
        return None
    paras_high = float(tm.iloc[-19:].max())         # 19 minggu tamat sebelum minggu sasaran
    base = float(tm.iloc[-20])                      # tutup minggu sasaran−20
    ret = r.close / base - 1
    if not (ret > 0.30):
        return None                                  # pulangan 20 minggu (pada tutup semasa) belum > 30%
    paras = max(paras_high, 1.30 * base)
    jarak = (paras - r.close) / r.close * 100
    # Andaian saya: baki hari dagangan minggu ini dikira ikut hari bekerja (Isnin–Jumaat), tanpa cuti.
    baki = 5 if bool(r._hm) else 4 - g.index[-1].weekday()
    if jarak <= 0:
        # Pencetus kalendar: paras sudah dilepasi, menunggu tutup hujung minggu (mesti ≤ 3 hari dagangan)
        if bool(r._hm) or baki > 3:
            return None
        return {'sebab': f'Pulangan 20 minggu {ret*100:.0f}% > 30%; nilai dagangan > USD15 juta; SPY > SMA100; tutup sudah ≥ {paras:.2f}',
                'syarat_beli': f'Tutup hari terakhir minggu ini (dalam {baki} hari dagangan) kekal ≥ {paras:.2f}; henti 8% bawah harga masuk, ekor 5 × ATR100',
                'pencetus': 'tutup hujung minggu', 'paras': round(paras, 2), 'jarak_pct': 0.0,
                'syarat_dipenuhi': '3/4', 'skor': 1.0}
    if not (jarak <= 2.0):
        return None
    bila = 'minggu depan' if bool(r._hm) else f'minggu ini (dalam {baki} hari dagangan)'
    return {'sebab': f'Pulangan 20 minggu {ret*100:.0f}% > 30%; nilai dagangan > USD15 juta; SPY > SMA100',
            'syarat_beli': f'Tutup hari terakhir {bila} ≥ {paras:.2f} (high tutup mingguan 20 minggu, pulangan kekal > 30%); henti 8% bawah harga masuk, ekor 5 × ATR100',
            'pencetus': 'pecahan high tutup 20 minggu', 'paras': round(paras, 2), 'jarak_pct': round(jarak, 2),
            'syarat_dipenuhi': '3/4', 'skor': round(1 - jarak / 2, 3)}
