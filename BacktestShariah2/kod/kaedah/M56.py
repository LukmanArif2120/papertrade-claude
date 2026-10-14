from enjin import rsi, atr
import pandas as pd, numpy as np

ID = 'M56'
NAMA = 'Gray & Vogel Momentum Lancar (FIP)'
VARIAN = 'V4 V1 tanpa FIP (8 MOM tertinggi)'
TMAX = None
WARM = 253
ADA_HENTI = True
SILANG = True
PERLU_BAR = 253
BULAN = (2, 5, 8, 11)


def _hari_imbang(fr):
    tarikh = pd.DatetimeIndex(sorted(set().union(*[g.index for g in fr.values()])))
    s = pd.Series(tarikh, tarikh)
    akhir = s.groupby([tarikh.year, tarikh.month]).last()
    hari = set(d for d in akhir.values if pd.Timestamp(d).month in BULAN)
    # Bulan terakhir data: hari terakhir hanya dikira hari imbang semula jika ia hari perniagaan terakhir bulan itu.
    # Andaian saya (scan langsung): guna kalendar hari bekerja Isnin-Jumaat (tanpa cuti umum).
    d_akhir = tarikh[-1]
    if d_akhir.month in BULAN and d_akhir != (d_akhir + pd.offsets.BMonthEnd(0)):
        hari.discard(np.datetime64(d_akhir)); hari.discard(d_akhir)
    return sorted(pd.Timestamp(d) for d in hari)


def _mom(g):
    return g.close.shift(21) / g.close.shift(252) - 1


def sedia(fr, idx):
    hari = _hari_imbang(fr)
    mom = {t: _mom(g) for t, g in fr.items()}
    pilih = {}; atas = {}
    for t_ in hari:
        nilai = {}
        for t, g in fr.items():
            if t_ in g.index:
                p = g.index.get_loc(t_)
                if p >= 252:
                    v = mom[t].iloc[p]
                    if not np.isnan(v): nilai[t] = v
        if not nilai: continue
        s = pd.Series(nilai).sort_values(ascending=False)
        n10 = max(16, int(np.floor(0.10 * len(s))))
        atas[t_] = s.iloc[:n10]
        pilih[t_] = set(s.iloc[:8].index)
    hs = pd.DatetimeIndex(list(pilih.keys()))
    for t, g in fr.items():
        ada = g.index.isin(hs)
        sig = np.zeros(len(g), bool); ex = np.zeros(len(g), bool)
        for i in np.where(ada)[0]:
            if t in pilih[g.index[i]]: sig[i] = True
            else: ex[i] = True
        g['sig'] = sig
        g['stop'] = 0.80 * g.open.shift(-1)          # 0.80 x buka masuk (buka i+1)
        g['tgt'] = np.nan
        g['exitc'] = ex
        g['rank'] = mom[t]
        g['_mom'] = mom[t]
    # simpan maklumat untuk hampir(): kedudukan MOM semasa pada bar terakhir
    akhir = {}
    for t, g in fr.items():
        if len(g) > 252 and not np.isnan(g._mom.iloc[-1]):
            akhir[t] = (g.index[-1], g._mom.iloc[-1])
    if akhir:
        dmax = max(d for d, _ in akhir.values())
        s = pd.Series({t: v for t, (d, v) in akhir.items() if d == dmax}).sort_values(ascending=False)
        kd = {t: k + 1 for k, t in enumerate(s.index)}
        for t, g in fr.items():
            g['_kd'] = np.nan; g['_nuniv'] = len(s)
            if t in kd: g.loc[g.index[-1], '_kd'] = kd[t]
        # tarikh imbang semula seterusnya
        nxt = None; d = dmax
        for _ in range(4):
            cand = (d + pd.offsets.BMonthEnd(1))
            if cand.month in BULAN: nxt = cand; break
            d = cand
        for g in fr.values(): g.attrs['m56_imbang_seterusnya'] = nxt


def _hasil(sebab, syarat, pencetus, paras, jarak, n, N):
    return {'sebab': sebab, 'syarat_beli': syarat, 'pencetus': pencetus,
            'paras': None if paras is None else round(float(paras), 4),
            'jarak_pct': None if jarak is None else round(float(jarak), 2),
            'syarat_dipenuhi': f'{n}/{N}',
            'skor': 0.9 if jarak is None else round(float(1 - jarak / 2), 3)}

def hampir(g, idx):
    """Syarat entry V4 (N=3): [1] MOM12-1 sah (>= 253 bar data) [2] MOM12-1 dalam 8 teratas alam saham
       [3] PENCETUS kalendar: tutup hari imbang semula (hari dagangan terakhir Feb/Mei/Ogos/Nov).
       Masuk watchlist hanya jika [1][2] dipenuhi hari ini dan hari imbang semula seterusnya <= 3 hari dagangan."""
    r = g.iloc[-1]
    if bool(r.sig) or '_kd' not in g or np.isnan(r._kd) or np.isnan(r._mom):
        return None
    kd = int(r._kd)
    if kd > 8:
        return None
    nxt = g.attrs.get('m56_imbang_seterusnya')
    if nxt is None:
        return None
    # Andaian saya: hari dagangan dikira dengan kalendar Isnin-Jumaat (tanpa cuti umum), sama seperti sedia().
    baki = len(pd.bdate_range(g.index[-1] + pd.Timedelta(days=1), nxt))
    if baki > 3:
        return None
    return _hasil(f'MOM12-1 = {r._mom*100:.1f}%; kedudukan {kd} daripada {int(r._nuniv)} saham (dalam 8 teratas)',
                  f'Kekal dalam 8 MOM12-1 tertinggi pada tutup hari imbang semula {nxt.strftime("%d %b %Y")} ({baki} hari dagangan lagi); beli pada buka hari berikutnya, henti 0.80 x buka masuk',
                  'Rotasi suku tahunan', None, 0.0, 2, 3)
