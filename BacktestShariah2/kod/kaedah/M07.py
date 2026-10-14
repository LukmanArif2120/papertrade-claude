from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M07'
NAMA = 'Qullamaggie Breakout'
VARIAN = 'V11 V7 keluar close<SMA20'
TMAX = None
WARM = 130
ADA_HENTI = True
SILANG = False
PERLU_BAR = 140


def _atrw(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _mkt(idx, ix):
    q = idx['QQQ'].close
    q10, q20 = q.rolling(10).mean(), q.rolling(20).mean()
    m = (q10 > q20) & ((q10 > q10.shift()) | (q20 > q20.shift()))
    # Andaian saya: tiada ffill — hari tanpa data QQQ = tiada isyarat (laporan M07: isyarat selepas 28 Sep tidak dijana)
    return m.reindex(ix).fillna(False).astype(bool).values


def _kira(g, MKT):
    h, l, c, o = g.high.values, g.low.values, g.close.values, g.open.values
    n = len(g)
    s10 = g.close.rolling(10).mean().values; s20 = g.close.rolling(20).mean().values; s50 = g.close.rolling(50).mean().values
    a14 = _atrw(g).values; ADR = ((g.high / g.low).rolling(20).mean() - 1).values
    sg = np.zeros(n, bool); setup = np.zeros(n, bool); RHv = np.full(n, np.nan)
    for i in range(132, n):
        k = i - 126 + int(np.argmax(h[i - 126:i - 4]))
        if k - 63 < 0: continue
        RUN = h[k] / l[k - 63:k + 1].min() - 1
        RH = h[i - 5:i].max(); RL = l[i - 5:i].min(); RHp = h[i - 6:i - 1].max()
        SURF = any(l[t] <= 1.01 * s10[t] and c[t] >= s50[t] for t in range(i - 10, i))
        HL = RL > l[i - 10:i - 5].min()
        base = RUN >= 0.30 and s10[i] > s20[i] and s20[i] > s20[i - 5] and SURF and HL \
            and ADR[i] >= 0.04 and (RH - RL) / RL <= 3 * ADR[i] and c[i] > s50[i]
        if base and MKT[i] and c[i] > RH and c[i - 1] <= RHp and (c[i] - l[i]) <= a14[i]:
            sg[i] = True
        # persediaan untuk esok (tetingkap julat 5 hari termasuk hari ini)
        if i == n - 1:
            RH2 = h[i - 4:i + 1].max(); RL2 = l[i - 4:i + 1].min()
            SURF2 = any(l[t] <= 1.01 * s10[t] and c[t] >= s50[t] for t in range(i - 9, i + 1))
            HL2 = RL2 > l[i - 9:i - 4].min()
            setup[i] = RUN >= 0.30 and s10[i] > s20[i] and SURF2 and HL2 and ADR[i] >= 0.04 \
                and (RH2 - RL2) / RL2 <= 3 * ADR[i] and c[i] > s50[i] and c[i] <= RH2
            RHv[i] = RH2
    return sg, setup, RHv, ADR, a14


def sedia(fr, idx):
    for g in fr.values():
        MKT = _mkt(idx, g.index)
        sg, setup, RHv, ADR, a14 = _kira(g, MKT)
        stop = g.low.copy()
        bm = g.open.shift(-1)
        sig = pd.Series(sg, g.index) & ((bm > stop) | bm.isna())    # langkau jika buka_masuk <= henti
        g['_setup'] = setup; g['_rh'] = RHv; g['_mkt'] = MKT
        g['sig'] = sig.fillna(False)
        g['stop'] = stop
        g['tgt'] = np.nan
        g['exitc'] = (g.close < g.close.rolling(20).mean()).fillna(False)
        g['rank'] = g.close / g.close.shift(126) - 1



def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def hampir(g, idx):
    """Syarat entry V11 (N=11), untuk bar esok i: [1] pasaran QQQ SMA10 > SMA20 dan salah satu menaik
       [2] RUN >= 30% [3] SMA10 > SMA20 [4] SMA20 > SMA20 5 hari lalu [5] SURF (low <= 1.01 x SMA10, tutup >= SMA50, 10 hari)
       [6] low makin tinggi (HL) [7] ADR20 >= 4% [8] julat 5 hari <= 3 x ADR [9] tutup > SMA50
       [10] tutup semalam <= high 5 hari semalam [11] PENCETUS: tutup > high 5 hari (RH) dengan (tutup - low) <= ATR14 Wilder."""
    r = g.iloc[-1]
    n = len(g)
    if bool(r.sig) or n < 140:
        return None
    h, l, c = g.high.values, g.low.values, g.close.values
    # [1] Andaian saya: penapis pasaran dinilai pada bar QQQ terakhir yang ada (bar esok belum wujud)
    q = idx['QQQ'].close; q10, q20 = q.rolling(10).mean(), q.rolling(20).mean()
    if not (q10.iloc[-1] > q20.iloc[-1] and (q10.iloc[-1] > q10.iloc[-2] or q20.iloc[-1] > q20.iloc[-2])):
        return None
    s10 = g.close.rolling(10).mean().values; s20 = g.close.rolling(20).mean().values; s50 = g.close.rolling(50).mean().values
    if not (s10[-1] > s20[-1] and c[-1] > s50[-1]):      # syarat trend mesti lulus hari ini juga
        return None
    i = n
    k = i - 126 + int(np.argmax(h[i - 126:i - 4]))
    if k - 63 < 0:
        return None
    RUN = h[k] / l[k - 63:k + 1].min() - 1
    RH = h[i - 5:i].max(); RL = l[i - 5:i].min(); RHp = h[i - 6:i - 1].max()
    SURF = any(l[t] <= 1.01 * s10[t] and c[t] >= s50[t] for t in range(i - 10, i))
    HL = RL > l[i - 10:i - 5].min()
    # [7][8] Andaian saya: ADR20 esok = ADR20 hari ini (julat bar esok belum diketahui)
    ADR = float((g.high / g.low).iloc[-20:].mean() - 1)
    if not (RUN >= 0.30 and SURF and HL and ADR >= 0.04 and (RH - RL) / RL <= 3 * ADR and c[-1] <= RHp):
        return None
    c0 = float(c[-1]); paras = float(RH)
    jarak = (paras - c0) / c0 * 100
    if jarak > 2.0:
        return None
    x = paras * (1 + 1e-9)
    s10x = np.append(c[-9:], x).mean(); s20x = np.append(c[-19:], x).mean(); s50x = np.append(c[-49:], x).mean()
    if not (s10x > s20x and s20x > s20[i - 5] and x > s50x):
        return None
    tr = pd.concat([g.high - g.low, (g.high - g.close.shift()).abs(), (g.low - g.close.shift()).abs()], axis=1).max(axis=1)
    a14 = float(tr.ewm(alpha=1 / 14, adjust=False).mean().iloc[-1])
    return _hasil(f'QQQ SMA10 > SMA20 dan menaik; lonjakan {RUN:.0%} dalam 6 bulan; SMA10 > SMA20, SMA20 menaik; meluncur dekat SMA10; low makin tinggi; julat 5 hari ketat (ADR20 {ADR:.1%}); tutup > SMA50',
                  f'Tutup esok > {paras:.2f} (high 5 hari) DAN (tutup esok - low esok) <= ~{a14:.2f} (ATR14 Wilder); henti = low esok',
                  'Pecah high 5 hari', paras, jarak, 10, 11)
