from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M40'
NAMA = 'Clenow Stocks on the Move'
VARIAN = 'V4 V1 tanpa penapis pasaran'
TMAX = None
WARM = 200
ADA_HENTI = True
SILANG = True          # TOP20 merentas semua saham + pra-simulasi 8 slot rotasi mingguan
PERLU_BAR = 210
SLOT = 8
START = pd.Timestamp('2019-11-01')


def _rma_atr(g, n):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _skor(c, n=90):
    y = np.log(c.values.astype(float)); out = np.full(len(y), np.nan)
    if len(y) >= n:
        W = np.lib.stride_tricks.sliding_window_view(y, n)
        x = np.arange(n) - (n - 1) / 2; sxx = (x ** 2).sum()
        ym = W.mean(axis=1, keepdims=True); d = W - ym
        b = (d * x).sum(axis=1) / sxx
        sst = (d ** 2).sum(axis=1); ssr = b ** 2 * sxx
        r2 = np.where(sst > 0, ssr / sst, 0.0)
        out[n - 1:] = (np.exp(b * 252) - 1) * r2
    return pd.Series(out, c.index)


def _hari_r(dates):
    d = pd.DatetimeIndex(sorted(dates))
    rab = (d - pd.to_timedelta((d.weekday - 2) % 7, unit='D'))   # Rabu minggu itu (atau sebelumnya)
    rab = rab.where(d.weekday >= 2, d + pd.to_timedelta(2 - d.weekday, unit='D'))
    s = pd.Series(d, index=d)
    # hari R = hari dagangan pertama >= Rabu minggu itu
    out = s[d >= rab].groupby(rab[d >= rab]).min()
    return pd.DatetimeIndex(out.values)


def _keluar(g, i, sp, ex):
    o, l = g.open.values, g.low.values; n = len(g); j = i + 1
    while j < n:
        if j > i + 1 and o[j] <= sp: return j
        if l[j] <= sp: return j
        if ex[j] and j + 1 < n: return j + 1
        j += 1
    return n - 1


def sedia(fr, idx):
    sk = {}; lay = {}; st = {}
    for t, g in fr.items():
        c = g.close
        sk[t] = _skor(c)
        jur = (c.pct_change().abs() >= 0.15).astype(float).rolling(90, min_periods=1).max().astype(bool)
        s100 = c.rolling(100).mean()
        lay[t] = (c > s100) & ~jur
        st[t] = c - 3 * _rma_atr(g, 20)
        g['_skor'] = sk[t]; g['_lay'] = lay[t]; g['_s100'] = s100
    SK = pd.DataFrame(sk); LY = pd.DataFrame(lay).fillna(False).astype(bool); ST = pd.DataFrame(st)
    RK = SK.rank(axis=1, ascending=False, method='first')
    NB = SK.notna().sum(axis=1)
    TOP = RK.le(np.floor(0.2 * NB), axis=0)
    hr = _hari_r(SK.index)
    hrset = set(hr)
    # exitc: hari R sahaja: bukan TOP20 atau tutup<SMA100 atau JURANG (= bukan LAYAK)
    EX = (~TOP | ~LY)
    for t, g in fr.items():
        m = g.index.isin(hr)
        g['exitc'] = pd.Series(m, g.index) & EX[t].reindex(g.index).fillna(True)
    pos = {t: {d: i for i, d in enumerate(g.index)} for t, g in fr.items()}
    sig = {t: np.zeros(len(g), bool) for t, g in fr.items()}
    pegang = {}; keluar_hari = {}
    for d in hr:
        nx = SK.index[SK.index.get_loc(d) + 1] if SK.index.get_loc(d) + 1 < len(SK.index) else None
        if nx is not None and nx < START: continue
        for t, x in list(pegang.items()):
            if nx is not None and x <= nx: keluar_hari[t] = x; del pegang[t]   # keluar pada buka hari masuk membebaskan slot (enjin v1.2)
        kosong = SLOT - len(pegang)
        if kosong <= 0: continue
        cal = SK.loc[d][TOP.loc[d] & LY.loc[d]].dropna().sort_values(ascending=False).index
        for t in cal:
            if kosong <= 0: break
            if t in pegang or keluar_hari.get(t) == nx or d not in pos[t]: continue
            g = fr[t]; i = pos[t][d]
            if i < WARM: continue
            sp = ST.at[d, t]
            kosong -= 1
            if i + 1 < len(g) and g.open.values[i + 1] <= sp: continue   # Andaian laporan: langkau
            sig[t][i] = True
            pegang[t] = g.index[_keluar(g, i, sp, g['exitc'].values)] if i + 1 < len(g) else pd.Timestamp.max
    dl = SK.index[-1]
    for t, g in fr.items():
        g['sig'] = sig[t]; g['stop'] = ST[t].reindex(g.index); g['tgt'] = np.nan
        g['rank'] = g['_skor']
        g.attrs['_m40'] = dict(hr=dl in hrset, top=bool(TOP.at[dl, t]) if t in TOP else False,
                               kd=int(RK.at[dl, t]) if not np.isnan(RK.at[dl, t]) else None,
                               k=int(np.floor(0.2 * NB.loc[dl])), pegang=t in pegang,
                               slot_kosong=SLOT - len(pegang))
    # Pembantu hampir(): susunan calon LAYAK yang belum dipegang pada tarikh terakhir.
    # Andaian saya: posisi dengan tarikh keluar >= tarikh terakhir dikira masih dipegang (konservatif).
    masih = {t for t, x in pegang.items() if x >= dl}
    calx = [t for t in SK.loc[dl][TOP.loc[dl] & LY.loc[dl]].dropna().sort_values(ascending=False).index
            if t not in masih and dl in pos[t] and pos[t][dl] >= WARM]
    for t, g in fr.items():
        g.attrs['_m40'].update(urutan=(calx.index(t) + 1) if t in calx else None,
                               kosong2=SLOT - len(masih), masih=t in masih)


def _hari_ke_R(d):
    """Bilangan hari dagangan (hari bekerja; Andaian saya: cuti umum diabaikan) dari d ke hari R seterusnya (Rabu, > d)."""
    k = 0; x = d
    while True:
        x = x + pd.offsets.BDay(1); k += 1
        if x.weekday() == 2: return k


def hampir(g, idx):
    """Piawaian ketat. Pencetus KALENDAR (rotasi mingguan hari R = Rabu). Syarat entry V4, N=5:
    1 dalam 20% teratas SKOR Clenow; 2 tutup > SMA100; 3 tiada jurang >= 15% dalam 90 hari;
    4 kedudukan antara calon layak yang belum dipegang <= slot kosong; 5 PENCETUS: hari R dalam <= 3 hari dagangan."""
    r = g.iloc[-1]; a = g.attrs.get('_m40')
    if bool(r.sig) or not a or np.isnan(r._skor) or len(g) <= WARM:
        return None
    if not (a['top'] and bool(r._lay)) or a.get('masih'):
        return None
    if a.get('urutan') is None or a['urutan'] > a['kosong2'] or a['kosong2'] <= 0:
        return None
    if g.index[-1].weekday() == 2:      # hari ini hari R dan tidak dipilih
        return None
    hk = _hari_ke_R(g.index[-1])
    if hk > 3:
        return None
    return {'sebab': f'SKOR Clenow {r._skor:.2f} (kedudukan {a["kd"]}/{a["k"]}, 20% teratas); tutup > SMA100 ({r._s100:.2f}); tiada jurang >= 15% dalam 90 hari; urutan calon {a["urutan"]} <= slot kosong {a["kosong2"]}',
            'syarat_beli': f'Hari R (Rabu, {hk} hari dagangan lagi): kekal dalam 20% teratas SKOR, tutup > SMA100, tiada jurang 15%, urutan calon kekal <= slot kosong; beli buka hari selepas hari R; henti tutup − 3 × ATR20 Wilder',
            'pencetus': 'Rotasi mingguan (Rabu)', 'paras': None, 'jarak_pct': 0.0,
            'syarat_dipenuhi': '4/5', 'skor': 1.0}
