from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M111'
NAMA = 'Sistem Volatiliti Wilder'
VARIAN = 'V5 V1 henti maks(tutup-3xATR7; 0.88xtutup)'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 260
N, M = 7, 3.0


def _rma_atr(g, n):
    # ATR Wilder: EWM alpha=1/n, adjust=False, bermula daripada julat sebenar pertama (ikut laporan M111)
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _sistem(c, a, mula=199, m=M):
    L = len(c); naik = np.zeros(L, bool); sic = np.full(L, np.nan); henti = np.full(L, np.nan)
    if L <= mula: return naik, sic, henti
    sic[mula] = c[mula]   # Permulaan: ARAH = TURUN, SIC = tutup hari pemanasan terakhir (indeks 199)
    for i in range(mula + 1, L):
        if not naik[i - 1]:
            henti[i] = sic[i - 1] + m * a[i - 1]
            if c[i] > henti[i]: naik[i] = True; sic[i] = c[i]
            else: sic[i] = min(sic[i - 1], c[i])
        else:
            henti[i] = sic[i - 1] - m * a[i - 1]
            if c[i] < henti[i]: naik[i] = False; sic[i] = c[i]
            else: naik[i] = True; sic[i] = max(sic[i - 1], c[i])
    return naik, sic, henti


def sedia(fr, idx):
    for g in fr.values():
        a = _rma_atr(g, N); c = g.close.values
        naik, sic, henti = _sistem(c, a.values)
        naik_s = pd.Series(naik, g.index)
        pusing = naik_s & ~naik_s.shift(1, fill_value=True)
        sma50 = g.close.rolling(50).mean()
        g['_naik'] = naik; g['_sic'] = sic; g['_atr'] = a; g['_sma50'] = sma50
        g['sig'] = pusing & (g.close > sma50)
        g['stop'] = np.maximum(g.close - M * a, 0.88 * g.close)
        g['tgt'] = np.nan
        g['exitc'] = ~naik_s & naik_s.shift(1, fill_value=False)   # ARAH bertukar TURUN
        g['rank'] = g.close / g.close.shift(63) - 1


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(1 - float(jarak) / 2, 3)}


def hampir(g, idx):
    # Syarat entry V5 (3): (1) Sistem Volatiliti arah TURUN hari ini; (2) tutup > SMA50;
    # (3) PENCETUS: tutup esok > SIC + 3 x ATR7 (arah pusing NAIK)
    r = g.iloc[-1]
    if bool(r.sig) or np.isnan(r._sic) or np.isnan(r._atr):
        return None
    if bool(r._naik):                                   # 1
        return None
    if np.isnan(r._sma50) or not (r.close > r._sma50):  # 2
        return None
    c = g.close.values.astype(float)
    henti = r._sic + M * r._atr
    paras = max(henti, c[-49:].sum() / 49)              # tutup esok juga mesti > SMA50 esok
    jarak = (paras - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    return _hasil(f'Sistem Volatiliti Wilder dalam arah turun; tutup {r.close:.2f} di atas SMA50 ({r._sma50:.2f})',
                  f'Tutup esok > {paras:.2f} (paras pusing naik SIC {r._sic:.2f} + 3 x ATR7); henti = maks(tutup - 3 x ATR7, 0.88 x tutup)',
                  'Pusing naik Sistem Volatiliti', paras, jarak, 2, 3)
