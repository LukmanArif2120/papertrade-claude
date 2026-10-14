from enjin import rsi, atr
import pandas as pd, numpy as np
from numpy.lib.stride_tricks import sliding_window_view

ID = 'M94'
NAMA = 'Pecutan Momentum (Chen, Yu & Wang)'
VARIAN = 'V0 Rotasi sumber (bulanan, langkau 21h, pegang 126h)'
TMAX = 126
WARM = 281
ADA_HENTI = False
SILANG = True
PERLU_BAR = 300
N = 252


def _wg(n=N):
    t = np.arange(n, dtype=float)
    X = np.column_stack([np.ones(n), t, t * t])
    return (np.linalg.inv(X.T @ X) @ X.T)[2]   # pekali t^2


def _pecut(c):
    v = c.values.astype(float); out = np.full(len(v), np.nan)
    if len(v) >= N:
        w = sliding_window_view(v, N)
        out[N - 1:] = (w @ _wg()) / w[:, 0]
    return pd.Series(out, c.index)


def sedia(fr, idx):
    P = {}; R = {}
    for t, g in fr.items():
        P[t] = _pecut(g.close); R[t] = g.close / g.close.shift(252) - 1
    P = pd.DataFrame(P); R = pd.DataFrame(R)
    # Andaian saya (ikut laporan): "20% teratas" = persentil pangkat (seri dipurata) > 0.80 antara saham yang ada nilai.
    pem = R.rank(axis=1, pct=True) > 0.80
    Pp = P.where(pem & P.notna())
    atas = (Pp.rank(axis=1, pct=True) > 0.80) & pem
    # Andaian saya (ikut laporan): hujung bulan = hari dagangan terakhir bulan dalam gabungan tarikh semua saham.
    # Pembantu hampir(): kedudukan PECUT (menurun) dalam kalangan saham layak; tidak mengubah isyarat.
    K = Pp.where(atas).rank(axis=1, ascending=False, method='first')
    tarikh = pd.DatetimeIndex(sorted(set().union(*[g.index for g in fr.values()])))
    hb = set(pd.Series(tarikh, tarikh).groupby(tarikh.to_period('M')).max())
    # Tarikh terakhir data hanya dikira hujung bulan jika hari bekerja berikutnya jatuh dalam bulan lain
    # (jika tidak, ia hanya 'tarikh terkini', bukan hujung bulan sebenar). Isyarat bar akhir tidak menjejaskan backtest.
    akhir = tarikh[-1]
    if (akhir + pd.offsets.BDay(1)).month == akhir.month:
        hb.discard(akhir)
    for t, g in fr.items():
        a = atas[t].reindex(g.index).fillna(False).astype(bool)
        p = pem[t].reindex(g.index).fillna(False).astype(bool)
        pc = P[t].reindex(g.index)
        hbs = pd.Series(g.index.isin(list(hb)), g.index)
        g['_atas'] = a; g['_pem'] = p; g['_pecut'] = pc
        g['_kedrot'] = K[t].reindex(g.index)
        g['sig'] = hbs & a.shift(21, fill_value=False) & p.shift(21, fill_value=False)
        g['stop'] = np.nan
        g['tgt'] = np.nan
        g['exitc'] = False
        g['rank'] = pc.shift(21)


def _hari_ke_rotasi(akhir):
    # Andaian saya: hari dagangan terakhir bulan = hari bekerja terakhir bulan (cuti umum tidak diambil kira).
    hb = akhir + pd.offsets.BMonthEnd(0)
    if hb == akhir:
        hb = akhir + pd.offsets.BMonthEnd(1)
    return len(pd.bdate_range(akhir, hb)) - 1, hb


def hampir(g, idx):
    # Syarat entry V0 (rotasi sumber): N = 4
    #   1. PEMENANG (20% teratas ROC252) dinilai 21 hari dagangan sebelum hari rotasi
    #   2. PECUT_ATAS (20% teratas pecutan dalam kalangan PEMENANG) dinilai pada hari yang sama
    #   3. Kedudukan rank (PECUT) <= 8 slot dalam kalangan saham layak
    #   4. PENCETUS kalendar: hari dagangan terakhir bulan, mesti dalam <= 3 hari dagangan
    if len(g) < 22 or bool(g.sig.iloc[-1]):
        return None
    k, hb = _hari_ke_rotasi(g.index[-1])
    if not (1 <= k <= 3):
        return None
    i = len(g) - 1 + k - 21          # bar penilaian bagi hari rotasi (sudah berlaku kerana k < 21)
    if not (bool(g._atas.iloc[i]) and bool(g._pem.iloc[i])):
        return None
    ked = g._kedrot.iloc[i]
    if np.isnan(ked) or ked > 8:
        return None
    return {'sebab': f'PEMENANG dan PECUT_ATAS pada {g.index[i].date()} (21 hari dagangan sebelum rotasi); kedudukan pecutan #{int(ked)} (<= 8 slot)',
            'syarat_beli': f'Beli pada tutup {hb.date()} (hari dagangan terakhir bulan, {k} hari dagangan lagi); pegang 126 hari',
            'pencetus': 'Rotasi hujung bulan', 'paras': None, 'jarak_pct': 0.0,
            'syarat_dipenuhi': '3/4', 'skor': 1.0}
