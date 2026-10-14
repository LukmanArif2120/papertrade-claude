from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M45'
NAMA = 'High 52 Minggu (George & Hwang)'
VARIAN = 'V4 V1 + high 52 minggu dicapai dalam 21 hari'
TMAX = 126
WARM = 252
ADA_HENTI = True
SILANG = True          # ATAS30 = 30% teratas NH merentas semua saham; pra-simulasi 8 slot
PERLU_BAR = 260
SLOT = 8


def _rma_atr(g, n=14):
    c = g.close
    tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def _hari_sejak_max(c, n=252):
    """Bilangan hari sejak kali TERAKHIR tutup menyamai maks 252 hari (termasuk hari ini)."""
    v = c.values.astype(float); out = np.full(len(v), np.nan)
    if len(v) >= n:
        W = np.lib.stride_tricks.sliding_window_view(v, n)[:, ::-1]   # lajur 0 = hari ini
        out[n - 1:] = np.argmax(W == W.max(axis=1, keepdims=True), axis=1)
    return pd.Series(out, c.index)


def _keluar(g, i, sp):
    """Tiru enjin: hari keluar bagi dagangan isyarat i (henti tetap sp, tmax 126, tiada exitc)."""
    o, l = g.open.values, g.low.values; n = len(g)
    j = i + 1
    while j < n:
        if j > i + 1 and o[j] <= sp: return j
        if l[j] <= sp: return j
        if (j - i) >= TMAX: return j
        j += 1
    return n - 1


def _hb(dates):
    """Hari dagangan terakhir setiap bulan dalam kalendar gabungan; bulan terakhir hanya jika tarikh akhir = hari bekerja terakhir bulan."""
    d = pd.DatetimeIndex(dates)
    s = pd.Series(d, index=d); last = s.groupby(d.to_period('M')).max()
    hb = set(last.values[:-1])
    # Andaian saya: bulan terakhir dikira hujung bulan hanya jika tarikh akhir data = hari bekerja terakhir bulan kalendar
    if d[-1] == d[-1] + pd.offsets.BMonthEnd(0): hb.add(d[-1].to_datetime64())
    return sorted(pd.Timestamp(x) for x in hb)


def sedia(fr, idx):
    nh = {}; r126 = {}; baru = {}; stop = {}
    for t, g in fr.items():
        c = g.close
        h252 = c.rolling(252).max()
        nh[t] = c / h252
        r126[t] = c / c.shift(126) - 1
        baru[t] = _hari_sejak_max(c) <= 21
        stop[t] = c - 3 * _rma_atr(g)
        g['_nh'] = nh[t]; g['_baru'] = baru[t]
    NH = pd.DataFrame(nh); R = pd.DataFrame(r126); BA = pd.DataFrame(baru).fillna(False); ST = pd.DataFrame(stop)
    hbs = _hb(NH.index)
    sig = {t: pd.Series(False, g.index) for t, g in fr.items()}
    pos = {t: {d: i for i, d in enumerate(g.index)} for t, g in fr.items()}
    pegang = {}   # ticker -> tarikh keluar
    akhir_keluar = {}
    calon_akhir = []
    for d in hbs:
        nhd = NH.loc[d].dropna()
        if nhd.empty: continue
        k = int(np.floor(0.3 * len(nhd)))
        dfc = pd.DataFrame({'nh': nhd, 'r': R.loc[d].reindex(nhd.index)}).sort_values(['nh', 'r'], ascending=False)
        atas = dfc.index[:k]
        for t, x in list(pegang.items()):
            if x <= d: akhir_keluar[t] = x; del pegang[t]
        kosong = SLOT - len(pegang)
        cal = [t for t in atas if bool(BA.at[d, t])]
        for t in cal:
            if kosong <= 0: break
            if t in pegang: continue
            g = fr[t]
            if d not in pos[t]: continue
            i = pos[t][d]
            if i < WARM: continue
            if akhir_keluar.get(t) == d: continue     # tidak dibeli semula pada hari ia keluar (had enjin)
            sp = ST.at[d, t]
            kosong -= 1
            if i + 1 < len(g) and g.open.values[i + 1] <= sp:
                continue            # langkau; slot dibiar kosong bulan itu
            sig[t].iloc[i] = True
            pegang[t] = g.index[_keluar(g, i, sp)] if i + 1 < len(g) else pd.Timestamp.max
    for t, g in fr.items():
        g['sig'] = sig[t]
        g['stop'] = ST[t].reindex(g.index)
        g['tgt'] = np.nan
        g['exitc'] = False
        g['rank'] = g['_nh'] + 1e-6 * R[t].reindex(g.index).fillna(0).clip(-50, 50)

    # Untuk scan harian: kedudukan NH pada tarikh terakhir (bukan semestinya hujung bulan)
    dl = NH.index[-1]; nhd = NH.loc[dl].dropna(); k = int(np.floor(0.3 * len(nhd)))
    dfc = pd.DataFrame({'nh': nhd, 'r': R.loc[dl].reindex(nhd.index)}).sort_values(['nh', 'r'], ascending=False)
    atas = dfc.index[:k]
    for t, g in fr.items():
        g.attrs['_m45'] = dict(atas30=t in atas, kedudukan=(list(dfc.index).index(t) + 1) if t in dfc.index else None,
                               k=k, hb=bool(dl in hbs), pegang=t in pegang)
    # Pembantu hampir(): susunan calon (30% teratas NH & high baharu dalam 21 hari) yang belum dipegang.
    # Andaian saya: posisi dengan tarikh keluar >= tarikh terakhir dikira masih dipegang (konservatif).
    masih = {t for t, x in pegang.items() if x >= dl}
    calx = [t for t in atas if bool(BA.at[dl, t]) and t not in masih and dl in pos[t] and pos[t][dl] >= WARM]
    for t, g in fr.items():
        g.attrs['_m45'].update(urutan=(calx.index(t) + 1) if t in calx else None,
                               kosong2=SLOT - len(masih), masih=t in masih)


def _hari_ke_hb(d):
    """Hari dagangan (hari bekerja; Andaian saya: cuti umum diabaikan) dari d ke hari bekerja terakhir bulan (> d)."""
    hb = d + pd.offsets.BMonthEnd(0)
    if hb <= d: hb = d + pd.offsets.BMonthEnd(1)
    return len(pd.bdate_range(d + pd.Timedelta(days=1), hb))


def hampir(g, idx):
    """Piawaian ketat. Pencetus KALENDAR (rotasi hujung bulan). Syarat entry V4, N=4:
    1 dalam 30% teratas NH (tutup / maks tutup 252 hari); 2 high 52 minggu dicapai dalam 21 hari;
    3 urutan antara calon layak yang belum dipegang <= slot kosong; 4 PENCETUS: hari dagangan terakhir bulan dalam <= 3 hari."""
    r = g.iloc[-1]; a = g.attrs.get('_m45')
    if bool(r.sig) or not a or np.isnan(r._nh) or len(g) <= WARM:
        return None
    if not (a['atas30'] and bool(r._baru)) or a.get('masih'):
        return None
    if a['hb']:
        return None
    if a.get('urutan') is None or a['urutan'] > a['kosong2'] or a['kosong2'] <= 0:
        return None
    hk = _hari_ke_hb(g.index[-1])
    if hk > 3:
        return None
    return {'sebab': f'NH {r._nh:.3f} (kedudukan {a["kedudukan"]}/{a["k"]}, 30% teratas); high 52 minggu dalam 21 hari; urutan calon {a["urutan"]} <= slot kosong {a["kosong2"]}',
            'syarat_beli': f'Hari dagangan terakhir bulan ({hk} hari lagi): kekal dalam 30% teratas NH, high 52 minggu dalam 21 hari, urutan kekal <= slot kosong; beli buka hari pertama bulan depan; henti tutup − 3 × ATR14 Wilder; pegang 126 hari',
            'pencetus': 'Rotasi hujung bulan', 'paras': None, 'jarak_pct': 0.0,
            'syarat_dipenuhi': '3/4', 'skor': 1.0}
