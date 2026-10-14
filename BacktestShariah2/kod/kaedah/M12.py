from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M12'
NAMA = 'Parabolic SAR'
VARIAN = 'V5 V1 keluar close<SMA50'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 210


def _psar(g, a0=0.02, da=0.02, amax=0.2):
    H, L = g.high.values.astype(float), g.low.values.astype(float); n = len(g)
    UP = np.zeros(n, bool); SAR = np.zeros(n); upt = True; s_ = L[0]; ep = H[0]; af = a0; UP[0] = True; SAR[0] = s_
    EP = np.zeros(n); AF = np.zeros(n); EP[0] = ep; AF[0] = af
    for t in range(1, n):
        if upt:
            s_ = min(s_ + af * (ep - s_), L[t - 1], L[max(t - 2, 0)])
            if L[t] <= s_: upt = False; s_ = ep; ep = L[t]; af = a0
            elif H[t] > ep: ep = H[t]; af = min(af + da, amax)
        else:
            s_ = max(s_ - af * (s_ - ep), H[t - 1], H[max(t - 2, 0)])
            if H[t] >= s_: upt = True; s_ = ep; ep = H[t]; af = a0
            elif L[t] < ep: ep = L[t]; af = min(af + da, amax)
        UP[t] = upt; SAR[t] = s_; EP[t] = ep; AF[t] = af
    _psar.ep = pd.Series(EP, g.index); _psar.af = pd.Series(AF, g.index)   # pembantu hampir
    return pd.Series(UP, g.index), pd.Series(SAR, g.index)


def sedia(fr, idx):
    for g in fr.values():
        c, o = g.close, g.open
        up, sar = _psar(g)
        s50 = c.rolling(50).mean()
        asas = up & ~up.shift(1, fill_value=True) & (c > s50)
        sig = asas & ~(o.shift(-1) <= sar)                  # langkau jika buka masuk <= henti
        g['_up'] = up; g['_sar'] = sar; g['_s50'] = s50; g['_ep'] = _psar.ep; g['_af'] = _psar.af
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = sar
        g['tgt'] = np.nan
        g['exitc'] = (c < s50).fillna(False)
        g['rank'] = c / c.shift(63) - 1


def hampir(g, idx):
    """Piawaian KETAT. Syarat entry V5 (N=3):
    1 PSAR trend turun semalam (hari ini bagi esok); 2 tutup > SMA50; 3 PENCETUS: PSAR berbalik naik (high esok >= SAR esok)."""
    r = g.iloc[-1]
    if bool(r.sig) or bool(r._up) or len(g) < 55 or np.isnan(r._s50) or not (r.close > r._s50):
        return None
    # SAR esok (Wilder, trend turun): max(SAR - AF x (SAR - EP), high hari ini, high semalam)
    sar_e = max(r._sar - r._af * (r._sar - r._ep), r.high, g.high.iloc[-2])
    s50e = (g.close.iloc[-49:].sum() + r.close) / 50   # Andaian saya: SMA50 esok dengan tutup esok = tutup hari ini
    # Andaian saya: jarak diukur pada high esok = tutup (pencetus sebenar ialah high esok >= SAR esok).
    jarak = (sar_e - r.close) / r.close * 100
    if jarak <= 0 or jarak > 2.0:
        return None
    return {'sebab': f'PSAR masih trend turun (SAR {r._sar:.2f}); tutup ({r.close:.2f}) > SMA50 ({r._s50:.2f})',
            'syarat_beli': f'High esok >= {sar_e:.2f} (SAR esok) supaya PSAR berbalik naik, dengan tutup esok > {s50e:.2f} (SMA50); henti = SAR baharu (low terendah trend turun {r._ep:.2f})',
            'pencetus': 'PSAR berbalik naik', 'paras': round(float(sar_e), 2), 'jarak_pct': round(float(jarak), 2),
            'syarat_dipenuhi': '2/3', 'skor': round(1 - jarak / 2, 2)}
