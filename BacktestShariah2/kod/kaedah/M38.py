from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M38'
NAMA = 'Darvas Kotak'
VARIAN = 'V4 V1 atas bar mingguan'
TMAX = None
WARM = 265
ADA_HENTI = True
SILANG = False
PERLU_BAR = 280
N_SAH = 3          # pengesahan 3 minggu


def _minggu(g):
    """Bar mingguan Isnin-Jumaat daripada data harian; tarikh = hari dagangan terakhir minggu itu."""
    k = g.index.to_period('W-FRI')
    w = pd.DataFrame({'high': g.high.groupby(k).max(), 'low': g.low.groupby(k).min(),
                      'close': g.close.groupby(k).last(), 'tarikh': pd.Series(g.index, index=g.index).groupby(k).last()})
    return w.reset_index(drop=True)


def _mesin(w):
    """Mesin keadaan A/B/C atas bar mingguan. Pulangkan senarai isyarat (indeks minggu, T, B),
    senarai kotak siap (indeks minggu, B), dan keadaan akhir."""
    h, l, c = w.high.values, w.low.values, w.close.values
    n = len(w)
    h52 = pd.Series(h).rolling(52).max().shift(1).values
    st = 'IDLE'; T = B = np.nan; cnt = 0
    sig = []; kotak = []
    for k in range(n):
        if st == 'IDLE':
            if not np.isnan(h52[k]) and h[k] > h52[k]:
                st, T, cnt = 'A', h[k], 0
            continue
        if st == 'A':
            if h[k] > T: T, cnt = h[k], 0
            else:
                cnt += 1
                if cnt == N_SAH: st, B, cnt = 'B0', np.nan, 0
            continue
        if st == 'B0':                    # hari pertama carian bawah (Andaian laporan: semak high > T juga)
            if h[k] > T: st, T, cnt = 'A', h[k], 0
            else: st, B, cnt = 'B', l[k], 0
            continue
        if st == 'B':
            if h[k] > T: st, T, cnt = 'A', h[k], 0
            elif l[k] < B: B, cnt = l[k], 0
            else:
                cnt += 1
                if cnt == N_SAH: st = 'C'; kotak.append((k, B))
            continue
        if st == 'C':
            if c[k] > T:
                sig.append((k, T, B)); st, T, cnt = 'A', h[k], 0
            elif c[k] < B:
                st = 'IDLE'; T = B = np.nan
    return sig, kotak, dict(st=st, T=T, B=B, cnt=cnt)


def _isi(g):
    w = _minggu(g)
    sigs, kotak, akhir = _mesin(w)
    ix = g.index; n = len(g); pos = {d: i for i, d in enumerate(ix)}
    o, hi, lo = g.open.values, g.high.values, g.low.values
    wk_end = np.zeros(n, bool); wclose = np.full(n, np.nan)
    for d, cc in zip(w.tarikh, w.close): wk_end[pos[d]] = True; wclose[pos[d]] = cc
    kotak_d = [(pos[w.tarikh[k]], b) for k, b in kotak]
    sig = np.zeros(n, bool); stop = np.full(n, np.nan); exitc = np.zeros(n, bool)
    raw = {pos[w.tarikh[k]]: B for k, T, B in sigs}
    for i, B in raw.items(): stop[i] = B
    # Tiru jujukan dagangan enjin supaya exitc ikut B_SEMASA dagangan semasa
    i = WARM
    while i < n - 1:
        if i not in raw or o[i + 1] <= raw[i]:   # langkau jika buka masuk <= B
            i += 1; continue
        sig[i] = True; sp = raw[i]; bs = sp
        j = i + 1; kk = [x for x in kotak_d if x[0] > i]; q = 0; keluar = None
        while j < n:
            while q < len(kk) and kk[q][0] <= j:
                bs = max(bs, kk[q][1]); q += 1
            ex = wk_end[j] and wclose[j] < bs
            if ex: exitc[j] = True
            if j > i + 1 and o[j] <= sp: keluar = j; break
            if lo[j] <= sp: keluar = j; break
            if ex and j + 1 < n: keluar = j + 1; break
            j += 1
        if keluar is None: break
        i = keluar + 1
    # Isyarat pada bar terakhir (untuk scan): buka esok belum diketahui
    # Andaian saya: isyarat bar terakhir hanya jika minggu sudah siap (bar terakhir hari Jumaat)
    if (n - 1) in raw and n - 1 >= WARM and ix[-1].weekday() == 4: sig[n - 1] = True
    return sig, stop, exitc, w, akhir


def sedia(fr, idx):
    for g in fr.values():
        sig, stop, exitc, w, akhir = _isi(g)
        g['sig'] = sig; g['stop'] = stop; g['tgt'] = np.nan; g['exitc'] = exitc
        g['rank'] = g.close / g.close.shift(63) - 1
        g.attrs['_m38'] = akhir


def hampir(g, idx):
    """Piawaian ketat. Syarat entry V4 (mingguan), N=5:
    1 high 52 minggu dipecah (mesin bermula); 2 atas kotak disahkan 3 minggu; 3 bawah kotak disahkan 3 minggu;
    4 kotak utuh (tiada tutup mingguan < bawah); 5 PENCETUS: tutup mingguan > atas kotak."""
    r = g.iloc[-1]
    if bool(r.sig):
        return None
    w = _minggu(g)
    # Andaian saya: jika bar terakhir bukan Jumaat, minggu separa dibuang; keadaan diambil daripada minggu siap sahaja
    if g.index[-1].weekday() != 4:
        w = w.iloc[:-1].reset_index(drop=True)
    _, _, a = _mesin(w)
    if a['st'] != 'C':
        return None
    T, B = float(a['T']), float(a['B'])
    if not (r.close >= B):
        return None
    jarak = (T - r.close) / r.close * 100
    if not (0 < jarak <= 2.0):
        return None
    return {'sebab': f'High 52 minggu dipecah; atas kotak {T:.2f} disahkan 3 minggu; bawah kotak {B:.2f} disahkan 3 minggu; kotak masih utuh',
            'syarat_beli': f'Tutup mingguan (hari dagangan terakhir minggu) > {T:.2f} (atas kotak); batal jika tutup mingguan < {B:.2f}; henti {B:.2f}',
            'pencetus': 'Tutup mingguan > atas kotak', 'paras': round(T, 2), 'jarak_pct': round(jarak, 2),
            'syarat_dipenuhi': '4/5', 'skor': round(1 - jarak / 2, 3)}
