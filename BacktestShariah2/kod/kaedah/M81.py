from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M81'
NAMA = 'Bensdorp Long Trend High Momentum'
VARIAN = 'V4 V1 henti awal 3xATR20'
TMAX = None
WARM = 201
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210


def _rma_atr(g, n=20):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _exit_ekor(g, sig, a20, warm):
    """Andaian saya: enjin v1.2 hanya ada henti tetap. Henti mengekor 25% (0.75 x tutup tertinggi sejak masuk,
    TT bermula = buka_masuk) disimulasi di sini mengikut gelung trades() enjin; hari keluar mengekor
    ditandakan sebagai exitc pada hari SEBELUMNYA supaya enjin keluar pada buka hari itu (masa keluar sama,
    harga keluar = buka, bukan paras henti). Henti awal buka_masuk-3xATR20 diserah kepada enjin melalui stop.
    AMARAN: exitc[j-1] bergantung pada rendah_j (pandang ke hadapan 1 hari) — HANYA untuk meniru jujukan
    dagangan backtest (trades_ekor). Lajur sig tidak bergantung padanya dan bebas pandang ke hadapan.
    Enjin v1.2 tidak dapat keluar pada paras henti mengekor yang berubah harian, jadi harga keluar tidak tepat."""
    o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values
    n = len(g); ex = np.zeros(n, bool); i = warm
    while i < n - 1:
        if not sig[i]: i += 1; continue
        e = o[i + 1]; sp0 = e - 3 * a20[i]
        if np.isnan(sp0): sp0 = -np.inf
        tt = e; j = i + 1; jx = n - 1
        while j < n:
            if j > i + 1: tt = max(tt, c[j - 1])
            tr = 0.75 * tt
            sp = max(sp0, tr)
            if (j > i + 1 and o[j] <= sp) or l[j] <= sp:
                if tr > sp0 and j > i + 1:
                    ex[j - 1] = True          # trailing exit -> engine exits at open j
                jx = j; break
            j += 1
        i = jx + 1
    return ex


def sedia(fr, idx):
    spy = idx['SPY'].close
    pas = spy > spy.rolling(100).mean()
    for g in fr.values():
        s25 = g.close.rolling(25).mean(); s50 = g.close.rolling(50).mean()
        nilai20 = (g.close * g.volume).rolling(20).mean()
        cair = (g.close >= 5) & (nilai20 > 50_000_000)
        mkt = pas.reindex(g.index, method='ffill').fillna(False).astype(bool)
        sig = (s25 > s50) & cair & mkt
        a20 = _rma_atr(g, 20)
        g['_s25'] = s25; g['_s50'] = s50; g['_cair'] = cair; g['_mkt'] = mkt
        g['sig'] = sig
        # Henti awal = buka_masuk - 3xATR20; buka_masuk belum diketahui pada hari isyarat.
        # Andaian saya: enjin guna stop[i] tetap -> guna tutup_i - 3xATR20_i sebagai anggaran (lihat _exit_ekor)
        g['stop'] = g.close - 3 * a20
        g['tgt'] = np.nan
        g['exitc'] = _exit_ekor(g, sig.values, a20.values, WARM)
        g['rank'] = g.close / g.close.shift(200) - 1


def hampir(g, idx):
    """Syarat entry V4 (sig): (1) SPY > SMA100; (2) tutup >= 5; (3) purata nilai dagangan 20h > 50 juta;
    (4) SMA25 > SMA50 (pencetus). N = 4."""
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._s50) or len(g) < 50:
        return None
    if not (bool(r._cair) and bool(r._mkt)):
        return None
    # SMA25 esok > SMA50 esok: (A24 + c)/25 > (A49 + c)/50  ->  c > A49 - 2*A24
    a24 = float(g.close.iloc[-24:].sum()); a49 = float(g.close.iloc[-49:].sum())
    paras = a49 - 2 * a24
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    return {'sebab': f'SPY > SMA100; tutup >= 5; nilai dagangan 20h > 50 juta; SMA25 ({r._s25:.2f}) di bawah SMA50 ({r._s50:.2f})',
            'syarat_beli': f'Tutup esok > {paras:.2f} supaya SMA25 menyilang ke atas SMA50 (SPY kekal > SMA100)',
            'pencetus': 'Silang SMA25 > SMA50', 'paras': float(round(paras, 4)), 'jarak_pct': float(round(jarak, 2)),
            'syarat_dipenuhi': '3/4', 'skor': float(round(1 - jarak / 2, 2))}
