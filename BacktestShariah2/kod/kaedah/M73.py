from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M73'
NAMA = 'ADX(5) > 40 + Julat Terkecil 6 Hari'
VARIAN = 'V0 Sumber tulen (ADX5>40 + NR6; tiada henti; keluar tutup>high semalam)'
TMAX = None
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 60


def _rma(x, n):
    """Wilder RMA disemai purata mudah n nilai sah pertama (seperti kad)."""
    v = x.values.astype(float); out = np.full(len(v), np.nan)
    ok = np.where(~np.isnan(v))[0]
    if len(ok) < n: return pd.Series(out, x.index)
    s = ok[0]; e = s + n - 1
    if np.isnan(v[s:e + 1]).any(): return pd.Series(out, x.index)
    out[e] = v[s:e + 1].mean()
    for k in range(e + 1, len(v)):
        out[k] = out[k - 1] + (v[k] - out[k - 1]) / n
    return pd.Series(out, x.index)


def _adx(g, n=5):
    c = g.close; pc = c.shift()
    tr = pd.concat([g.high - g.low, (g.high - pc).abs(), (g.low - pc).abs()], axis=1).max(axis=1)
    tr[pc.isna()] = np.nan
    nd = g.high - g.high.shift(); td = g.low.shift() - g.low
    pdm = pd.Series(np.where((nd > td) & (nd > 0), nd, 0.0), g.index); pdm[nd.isna()] = np.nan
    mdm = pd.Series(np.where((td > nd) & (td > 0), td, 0.0), g.index); mdm[td.isna()] = np.nan
    rtr = _rma(tr, n)
    pdi = 100 * _rma(pdm, n) / rtr; mdi = 100 * _rma(mdm, n) / rtr
    den = pdi + mdi
    dx = (100 * (pdi - mdi).abs() / den).where(den != 0, 0.0).where(den.notna())
    return _rma(dx, n), pdi, mdi


def sedia(fr, idx):
    for g in fr.values():
        adx, pdi, mdi = _adx(g, 5)
        jul = g.high - g.low
        nr6 = jul < jul.shift(1).rolling(5).min()
        g['_adx5'] = adx; g['_nr6'] = nr6; g['_pdi'] = pdi; g['_mdi'] = mdi
        g['sig'] = (adx > 40) & nr6
        g['stop'] = np.nan
        g['tgt'] = np.nan
        g['exitc'] = g.close > g.high.shift()
        g['rank'] = g.close / g.close.shift(63) - 1


def hampir(g, idx):
    # Syarat entry V0 (N=2): ADX(5) > 40; julat hari terkecil 6 hari NR6 (PENCETUS).
    # Pencetus corak satu hari (julat sempit) -> tiada paras harga, jarak_pct = None.
    r = g.iloc[-1]
    if bool(r.sig) or not (r._adx5 > 40):
        return None
    jul = (g.high - g.low)
    jmin = float(jul.iloc[-5:].min())      # esok: julat < min julat 5 hari terakhir (termasuk hari ini)
    if not (jmin > 0):
        return None
    # Andaian saya: semak ADX(5) esok kekal > 40 dengan bar esok sempit (julat 0.99 x jmin) berpusat pada tutup hari ini.
    t = g[['open', 'high', 'low', 'close']].iloc[-260:].copy()
    h = 0.99 * jmin / 2
    t.loc[t.index[-1] + pd.Timedelta(days=1)] = [r.close, r.close + h, r.close - h, r.close]
    adx_esok = float(_adx(t, 5)[0].iloc[-1])
    if not (adx_esok > 40):
        return None
    return {'sebab': f'ADX(5) = {r._adx5:.1f} > 40 (aliran sangat kuat); julat hari ini belum terkecil 6 hari',
            'syarat_beli': f'Julat esok (high − low) < {jmin:.2f} (terkecil 6 hari) dengan ADX(5) kekal > 40 '
                           f'(anggaran esok {adx_esok:.1f}); beli buka lusa, jual bila tutup > high semalam',
            'pencetus': 'NR6 (julat terkecil 6 hari)', 'paras': None, 'jarak_pct': None,
            'syarat_dipenuhi': '1/2', 'skor': 0.9}
