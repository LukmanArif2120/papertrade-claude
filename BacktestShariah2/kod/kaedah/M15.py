from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M15'
NAMA = 'Break & Retest + Henti ATR'
VARIAN = 'V2 Ekori SMA20 tanpa sasaran'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = False
PERLU_BAR = 230


def _atrw(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _br(g):
    """Pecah & uji semula (kod M15 kompilasi 8.2). Pulang sig (tanpa langkau), SL, R, T dan b bagi setiap i."""
    O, H, L, C = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close']]
    n = len(g); a14 = _atrw(g).values; s20 = g.close.rolling(20).mean().values
    PH = (g.high == g.high.rolling(7, center=True).max()).values
    lastpv = np.full(n, -1)
    cur = -1
    for t in range(n):
        if PH[t]: cur = t
        lastpv[t] = cur
    sg = np.zeros(n, bool); SL = np.full(n, np.nan); RR_ = np.full(n, np.nan); RZ = np.full(n, np.nan); TT = np.full(n, np.nan)
    for i in range(70, n):
        b = None
        for bb in range(i - 1, i - 16, -1):
            p = lastpv[bb - 4]
            if p >= 0 and C[bb] > H[p] and C[bb - 1] <= H[p]:
                b = bb; R_ = H[p]; tR = p; break
        if b is None: continue
        if C[b:i + 1].min() > L[tR:b + 1].min(): RZ[i] = R_   # trend naik masih sah (tiada tutup < PL)
        if not (C[b:i + 1].min() > L[tR:b + 1].min() and L[i] <= R_ + 0.5 * a14[i] and C[i] >= R_ - 0.5 * a14[i]):
            continue
        cdl = (min(O[i], C[i]) >= H[i] - 0.382 * (H[i] - L[i]) and H[i] > L[i]) or \
              (C[i - 1] < O[i - 1] and C[i] > O[i] and (C[i] - O[i]) > (O[i - 1] - C[i - 1])) or C[i] > H[i - 1]
        T_ = H[i - 60:i].max(); SL_ = L[b:i + 1].min() - a14[i]
        TT[i] = T_; SL[i] = SL_
        if cdl and T_ > C[i] and C[i] > s20[i] and (T_ - C[i]) / (C[i] - SL_) >= 1:
            sg[i] = True
    return sg, SL, RZ, TT, a14


def sedia(fr, idx):
    for g in fr.values():
        sg, SL, RZ, TT, a14 = _br(g)
        idx_ = g.index
        stop = pd.Series(SL, idx_)
        sig = pd.Series(sg, idx_)
        # Laporan: langkau jika buka masuk <= henti (V2 tiada sasaran)
        lk = (g.open.shift(-1) <= stop).fillna(False)
        S20 = g.close.rolling(20).mean()
        g['_R'] = RZ; g['_S20'] = S20; g['_A'] = a14
        g['sig'] = (sig & ~lk).fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = g.close < S20
        g['rank'] = g.close / g.close.shift(63) - 1


def hampir(g, idx):
    """Piawaian ketat (ARAHAN_HAMPIR). Syarat entry V2 (kod _br, PADAN registry), N=8:
    1 tutup pecah pivot high R dalam 15 hari; 2 trend sah (tiada tutup < pivot low sebelum pecah);
    3 low sentuh zon (low <= R + 0.5×ATR14); 4 tutup >= R − 0.5×ATR14; 5 tutup > SMA20;
    6 high 60 hari > tutup; 7 R:R ke high 60 hari >= 1; 8 PENCETUS lilin masuk.
    Syarat 1–7 mesti dipenuhi pada bar terakhir; lilin masuk hari ini gagal.
    Pencetus yang boleh diukur: tutup esok > high hari ini (salah satu bentuk lilin masuk dalam kod)."""
    n = len(g)
    if n < 80: return None
    r = g.iloc[-1]
    if bool(r.sig): return None
    O, H, L, C = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close']]
    a14 = g._A.values; s20 = g._S20.values
    PH = (g.high == g.high.rolling(7, center=True).max()).values
    lastpv = np.full(n, -1); cur = -1
    for t in range(n):
        if PH[t]: cur = t
        lastpv[t] = cur
    i = n - 1
    b = None
    for bb in range(i - 1, i - 16, -1):
        p = lastpv[bb - 4]
        if p >= 0 and C[bb] > H[p] and C[bb - 1] <= H[p]:
            b = bb; R_ = H[p]; tR = p; break
    if b is None or b < n - 15: return None          # 1 (dan pecahan masih dalam tetingkap 15 hari esok)
    if not C[b:i + 1].min() > L[tR:b + 1].min(): return None   # 2
    A = a14[i]
    if not (L[i] <= R_ + 0.5 * A and C[i] >= R_ - 0.5 * A): return None   # 3, 4
    if not C[i] > s20[i]: return None                 # 5
    T_ = H[i - 60:i].max(); SL_ = L[b:i + 1].min() - A
    if not (T_ > C[i] and (T_ - C[i]) / (C[i] - SL_) >= 1): return None   # 6, 7
    # Pencetus esok: tutup > high hari ini. Andaian saya: henti/ATR esok ≈ nilai hari ini; T esok termasuk high hari ini.
    paras = H[i]
    jarak = (paras - C[i]) / C[i] * 100
    if not (0 < jarak <= 2.0): return None
    T1 = H[i - 59:i + 1].max()
    if not (T1 > paras and (T1 - paras) / (paras - SL_) >= 1): return None
    return {'sebab': f'Pecah rintangan {R_:.2f} dalam 15 hari lepas; trend naik sah; low sentuh zon uji semula '
                     f'({R_ - 0.5*A:.2f}–{R_ + 0.5*A:.2f}); tutup > SMA20 ({s20[i]:.2f}); R:R ke high 60 hari ({T_:.2f}) >= 1',
            'syarat_beli': f'Tutup esok > {paras:.2f} (high hari ini, lilin masuk) dengan low esok <= {R_ + 0.5*A:.2f}; '
                           f'R:R ke {T1:.2f} kekal >= 1 (henti ≈ {SL_:.2f}); langkau jika buka masuk <= henti',
            'pencetus': 'Lilin masuk: tutup > high semalam', 'paras': round(float(paras), 2), 'jarak_pct': round(float(jarak), 2),
            'syarat_dipenuhi': '7/8', 'skor': round(1 - jarak / 2, 3)}
