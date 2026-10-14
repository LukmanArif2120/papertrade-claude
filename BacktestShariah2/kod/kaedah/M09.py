from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M09'
NAMA = 'Volumatic VIDYA Pivot Retest'
VARIAN = 'V2 V1 tanpa sasaran'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 300   # ATR200 Wilder + VIDYA perlu pemanasan panjang


def _atrw(g, n):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _kira(g):
    O, H, L, C, V = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close', 'volume']]
    n = len(g); c = g.close
    dl = c.diff(); up = dl.clip(lower=0).rolling(20).sum(); dn = (-dl.clip(upper=0)).rolling(20).sum()
    CMO = ((up - dn) / (up + dn) * 100).abs().fillna(0).values; a = 2 / 11; Vr = np.zeros(n)
    for t in range(1, n): Vr[t] = a * CMO[t] / 100 * C[t] + (1 - a * CMO[t] / 100) * Vr[t - 1]
    VID = pd.Series(Vr).rolling(15).mean().values; A200 = _atrw(g, 200).values
    UB = VID + 2 * A200; LB = VID - 2 * A200
    upT = np.zeros(n, bool); chg = np.zeros(n, bool)
    for t in range(1, n):
        upT[t] = upT[t - 1]
        if not np.isnan(UB[t]) and C[t] > UB[t] and C[t - 1] <= UB[t - 1]: upT[t] = True
        if not np.isnan(LB[t]) and C[t] < LB[t] and C[t - 1] >= LB[t - 1]: upT[t] = False
        chg[t] = upT[t] != upT[t - 1]
    buy = sell = 0.0; DL = np.zeros(n)
    for t in range(1, n):
        if chg[t] or chg[t - 1]: buy = sell = 0.0
        elif C[t] > O[t]: buy += V[t]
        elif C[t] < O[t]: sell += V[t]
        av = (buy + sell) / 2; DL[t] = (buy - sell) / av * 100 if av > 0 else 0
    line = np.where(upT, LB, UB)
    a14 = _atrw(g, 14).values
    sg = np.zeros(n, bool); st = np.full(n, np.nan)
    levA = np.full(n, np.nan)          # paras aktif (belum disentuh) pada penghujung hari t
    ageA = np.full(n, np.nan)          # umur paras aktif (pembantu hampir)
    pendB = np.zeros(n, bool)          # hari t = sentuhan merah tutup >= paras -> B boleh pada t+1
    levB = np.full(n, np.nan)
    lev = np.nan; age = 0; touched = False; pb = -1; pblev = np.nan
    for i in range(7, n):
        cc = i - 3
        if upT[i] and C[cc] == C[cc - 3:cc + 4].min() and L[cc] > line[cc]:
            lev = L[cc]; age = 0; touched = False
        if not upT[i]: lev = np.nan
        # Persediaan B (ikut laporan: kad diutamakan): semalam sentuh+merah+tutup>=paras, hari ini hijau.
        # Andaian saya (disahkan padan registry): B sah hanya jika paras itu masih paras semasa (tidak diganti pivot baharu hari ini).
        if pb == i - 1 and upT[i] and not np.isnan(lev) and lev == pblev:
            if C[i] > O[i] and C[i] >= pblev and DL[i] >= 30:
                sg[i] = True; st[i] = min(L[i - 1], L[i]) - 0.5 * a14[i]
        if np.isnan(lev): continue
        age += 1
        if age > 50 or touched: continue
        if L[i] <= lev:
            touched = True
            if C[i] >= lev and C[i] > O[i] and DL[i] >= 30:
                sg[i] = True; st[i] = L[i] - 0.5 * a14[i]
            elif C[i] < O[i] and C[i] >= lev:
                pb = i; pblev = lev; pendB[i] = True; levB[i] = lev
        else:
            levA[i] = lev; ageA[i] = age
    return sg, st, upT, DL, levA, pendB, levB, ageA


def sedia(fr, idx):
    for g in fr.values():
        sg, st, upT, DL, levA, pendB, levB, ageA = _kira(g)
        stop = pd.Series(st, g.index)
        sig = pd.Series(sg, g.index) & ~(g.open.shift(-1) <= stop)   # langkau jika buka masuk <= henti
        g['_up'] = upT; g['_dl'] = DL; g['_lev'] = levA; g['_pb'] = pendB; g['_levb'] = levB; g['_age'] = ageA
        g['sig'] = sig.fillna(False).astype(bool)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = ~pd.Series(upT, g.index)
        g['rank'] = DL


def hampir(g, idx):
    """Piawaian KETAT. Syarat entry V2 (N=4):
    A: 1 trend VIDYA Naik; 2 Delta >= 30; 3 paras pivot aktif (umur <= 50, belum disentuh); 4 PENCETUS: low <= L, tutup >= L, lilin hijau.
    B: 1 Naik; 2 Delta >= 30; 3 semalam sentuh L, merah, tutup >= L; 4 PENCETUS: lilin hijau dengan tutup >= L."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 60 or not bool(r._up) or not (r._dl >= 30):
        return None
    # Andaian saya: lilin hijau esok hanya menambah volum beli, jadi Delta >= 30 hari ini kekal >= 30 esok;
    # andaian paras L tidak diganti oleh pivot baharu esok.
    if bool(r._pb):
        L = float(r._levb)
        return {'sebab': f'Trend VIDYA naik; Delta {r._dl:.0f}% (>= 30); hari ini lilin merah menyentuh paras pivot {L:.2f} dan tutup di atasnya (Persediaan B)',
                'syarat_beli': f'Esok lilin hijau (tutup > buka) dengan tutup >= {L:.2f}',
                'pencetus': 'Lilin hijau selepas sentuhan merah (B)', 'paras': round(L, 2), 'jarak_pct': None,
                'syarat_dipenuhi': '3/4', 'skor': 0.9}
    L = r._lev
    if np.isnan(L) or np.isnan(r._age) or r._age + 1 > 50:
        return None
    # Pencetus undur ke bawah: jarak = (tutup - L)/tutup x 100
    jarak = (r.close - L) / r.close * 100
    if jarak <= 0 or jarak > 2.0:
        return None
    return {'sebab': f'Trend VIDYA naik; Delta {r._dl:.0f}% (>= 30); paras pivot low {L:.2f} aktif (umur {int(r._age)} hari, belum disentuh)',
            'syarat_beli': f'Esok low <= {L:.2f}, tutup >= {L:.2f} dan lilin hijau (Persediaan A)',
            'pencetus': 'Sentuh paras pivot + lilin hijau (A)', 'paras': round(float(L), 2), 'jarak_pct': round(float(jarak), 2),
            'syarat_dipenuhi': '3/4', 'skor': round(1 - jarak / 2, 2)}
