from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M21'
NAMA = 'Marius 3 Persediaan (Pecahan+Jurang+Kesinambungan)'
VARIAN = 'V5 V1 keluar close<SMA20'
TMAX = None
WARM = 260
ADA_HENTI = True
SILANG = False
PERLU_BAR = 300


def _persediaan(g, spy):
    O, H, L, C, V = [g[k].values.astype(float) for k in ['open', 'high', 'low', 'close', 'volume']]
    n = len(g); c, v = g.close, g.volume
    a14 = atr(g, 14).values                       # kad: atr() enjin (purata mudah)
    ADR = ((g.high / g.low).rolling(20).mean() - 1).values
    U = ((c > 1) & (pd.Series(ADR, g.index) >= 0.05) & ((c * v).rolling(20).mean() >= 1e6)).values
    VOL50 = v.rolling(50).mean().shift(1).values
    s10 = c.rolling(10).mean().values; s20 = c.rolling(20).mean().values; s50 = c.rolling(50).mean().values
    sp = spy.reindex(g.index).ffill().values
    BOk = np.zeros(n, bool); EPk = np.zeros(n, bool); MCk = np.zeros(n, bool)
    for i in range(70, n):
        if not U[i]: continue
        k = i - 63 + int(np.argmax(H[i - 63:i - 2])); hk = H[k]
        RUN = hk / L[max(0, k - 63):k + 1].min() - 1
        RH = H[i - 10:i].max(); RL = L[i - 10:i].min()
        BO = RUN >= 0.30 and s10[i] > s20[i] and C[i] > RH and C[i - 1] <= H[i - 11:i - 1].max() and (C[i] - L[i]) <= a14[i]
        BOk[i] = BO and (RH - RL) / RL <= 2.5 * ADR[i] and C[i] > s50[i] and RL >= 0.75 * hk
        H63 = H[i - 63:i].max()
        EP = O[i] / C[i - 1] - 1 >= 0.05 and V[i] >= 3 * VOL50[i] and O[i] > H63
        EPk[i] = EP and C[i] > H63
        MC = sp[i] < sp[i - 1] and C[i] / C[i - 1] - 1 >= max(0.04, ADR[i]) and V[i] >= 2 * VOL50[i] and C[i] > H[i - 20:i].max()
        MCk[i] = MC and H[i] > L[i] and (C[i] - L[i]) / (H[i] - L[i]) >= 0.75
    return BOk, EPk, MCk, U, ADR


def sedia(fr, idx):
    spy = idx['SPY'].close
    for g in fr.values():
        BOk, EPk, MCk, U, ADR = _persediaan(g, spy)
        sig = pd.Series(BOk | EPk | MCk, g.index)
        lk = (g.open.shift(-1) <= g.low).fillna(False)      # kad: langkau jika buka masuk <= henti
        sig = (sig & ~lk).fillna(False)
        S20 = g.close.rolling(20).mean()
        RED1 = sig.shift(1, fill_value=False) & (g.close < g.open)
        g['_U'] = U; g['_ADR'] = ADR
        g['sig'] = sig
        g['stop'] = g.low
        g['tgt'] = np.nan
        g['exitc'] = (g.close < S20) | RED1
        g['rank'] = g.volume.rolling(40).mean() / g.volume.rolling(252).mean()


def hampir(g, idx):
    """Piawaian ketat. Isyarat = BO | EP | MC. Hanya persediaan pecahan (BO) ada fasa 'hampir';
    jurang EP dan kesinambungan MC ialah peristiwa satu hari tanpa persediaan -> tidak dipantau.
    Syarat BO (kod _persediaan, PADAN registry), N=7, dinilai untuk esok:
    1 alam U (harga > 1, ADR20 >= 5%, purata nilai dagangan 20 hari >= 1 juta); 2 larian >= 30% ke puncak 3 bulan;
    3 SMA10 > SMA20; 4 tutup > SMA50; 5 julat 10 hari <= 2.5×ADR; 6 low julat >= 0.75×puncak;
    7 PENCETUS: tutup > high 10 hari (kali pertama) dengan (tutup − low) <= ATR14."""
    if len(g) < 80: return None
    r = g.iloc[-1]
    if bool(r.sig) or not bool(r._U): return None                         # 1
    H, L, C = g.high.values, g.low.values, g.close.values
    i = len(g)                                  # indeks esok: tetingkap berakhir hari ini
    k = i - 63 + int(np.argmax(H[i - 63:i - 2])); hk = H[k]
    RUN = hk / L[max(0, k - 63):k + 1].min() - 1
    RH = H[i - 10:i].max(); RL = L[i - 10:i].min()
    if not C[-1] <= H[i - 11:i - 1].max(): return None                    # kali pertama (tutup hari ini belum pecah)
    adr = r._ADR
    paras = RH
    # Andaian saya: SMA esok dinilai dengan tutup esok = paras pencetus.
    s10 = (C[-9:].sum() + paras) / 10; s20 = (C[-19:].sum() + paras) / 20; s50 = (C[-49:].sum() + paras) / 50
    if not (RUN >= 0.30 and s10 > s20 and paras > s50 and (RH - RL) / RL <= 2.5 * adr and RL >= 0.75 * hk):
        return None                                                        # 2–6
    jarak = (paras - C[-1]) / C[-1] * 100
    if not (0 < jarak <= 2.0): return None
    a14 = atr(g, 14).iloc[-1]
    return {'sebab': f'Alam U lulus; larian {RUN*100:.0f}% ke puncak 3 bulan; SMA10 > SMA20; atas SMA50; '
                     f'julat 10 hari ketat ({(RH-RL)/RL*100:.1f}% <= 2.5×ADR); low julat >= 0.75×puncak',
            'syarat_beli': f'Tutup esok > {paras:.2f} (high 10 hari) dengan (tutup − low) <= ATR14 (≈ {a14:.2f}); '
                           f'henti = low hari isyarat; keluar tutup < SMA20 atau hari masuk merah',
            'pencetus': 'Pecahan tutup > high 10 hari', 'paras': round(float(paras), 2), 'jarak_pct': round(float(jarak), 2),
            'syarat_dipenuhi': '6/7', 'skor': round(1 - jarak / 2, 3)}
