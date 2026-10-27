"""Bateri signal EXIT dan peraturan HOLD (REVERSE SPEC §6/§7b).

Konvensyen: signal menyala pada tutup hari d -> JUAL pada BUKA hari d+1 (sama seperti lorong 2 repo).
Jika d+1 tiada, dagangan ditutup pada tutup bar terakhir dan ditanda terpotong.

13 signal EXIT dalam grid SISTEM (SPEC pindaan §13.6). 7 calon amaran Step 6 yang lain tidak boleh
menjadi exit tunggal (ia mungkin tidak menyala sama sekali) dan dilapor sebagai CALON sahaja.
"""
import numpy as np

EXIT13 = ['bawah_ema9', 'bawah_ema21', 'bawah_ma50', 'rsi_70_60', 'macd_bawah', 'hist_neg3',
          'hari_agihan', 'trail_2atr', 'trail_3atr', 'chandelier_4atr', 'trail_8pct',
          'trail_10pct', 'trail_15pct']

HOLD_X = [5, 7, 10, 12, 15, 20]
HOLD_Y = ['ema9', 'ema21', 'ma50']
HOLD18 = [(x, y) for x in HOLD_X for y in HOLD_Y]


def sedia(g, ind):
    """Array yang diperlukan oleh signal exit. Pulangkan dict array numpy."""
    a = dict(
        c=g['close'].to_numpy('float64'), o=g['open'].to_numpy('float64'),
        v=g['volume'].to_numpy('float64'),
        ema9=ind['ema9'].to_numpy('float64'), ema21=ind['ema21'].to_numpy('float64'),
        ma50=ind['ma50'].to_numpy('float64'), atr=ind['atr14'].to_numpy('float64'),
        rsi=ind['rsi14'].to_numpy('float64'), hist=ind['macd_hist'].to_numpy('float64'),
        cerun50=ind['cerun_ma50'].to_numpy('float64'),
        voln=ind['vol_n50'].to_numpy('float64'),
    )
    return a


def _nyala(a, d, nama, puncak, puncak_atr):
    """Adakah signal `nama` menyala pada tutup hari d?"""
    c = a['c']
    if nama == 'bawah_ema9':
        return np.isfinite(a['ema9'][d]) and c[d] < a['ema9'][d]
    if nama == 'bawah_ema21':
        return np.isfinite(a['ema21'][d]) and c[d] < a['ema21'][d]
    if nama == 'bawah_ma50':
        return np.isfinite(a['ma50'][d]) and c[d] < a['ma50'][d]
    if nama == 'rsi_70_60':
        r = a['rsi']
        if not np.isfinite(r[d]) or r[d] >= 60:
            return False
        lo = max(d - 20, 0)
        seg = r[lo:d]
        return np.isfinite(seg).any() and np.nanmax(seg) > 70
    if nama == 'macd_bawah':
        h = a['hist']
        return (d > 0 and np.isfinite(h[d]) and np.isfinite(h[d - 1])
                and h[d] < 0 <= h[d - 1])
    if nama == 'hist_neg3':
        h = a['hist']
        return d >= 2 and np.all(np.isfinite(h[d - 2:d + 1])) and np.all(h[d - 2:d + 1] < 0)
    if nama == 'hari_agihan':
        return (d > 0 and c[d] < c[d - 1] and np.isfinite(a['voln'][d]) and a['voln'][d] >= 2.0)
    if nama == 'trail_2atr':
        return np.isfinite(puncak_atr) and c[d] <= puncak - 2.0 * puncak_atr
    if nama == 'trail_3atr':
        return np.isfinite(puncak_atr) and c[d] <= puncak - 3.0 * puncak_atr
    if nama == 'chandelier_4atr':
        return np.isfinite(puncak_atr) and c[d] <= puncak - 4.0 * puncak_atr
    if nama == 'trail_8pct':
        return c[d] <= puncak * 0.92
    if nama == 'trail_10pct':
        return c[d] <= puncak * 0.90
    if nama == 'trail_15pct':
        return c[d] <= puncak * 0.85
    raise KeyError(nama)


def hold_ok(a, d, puncak, x_pct, y_ma, pasaran_naik):
    """Peraturan HOLD: veto exit jika pullback masih kecil DAN trend saham + pasaran masih naik.

    SPEC §13.7: "Selagi trend saham dan pasaran naik, pullback <= X% atau <= paras MA Y boleh
    di-hold". Operasi: veto sah hanya jika SEMUA benar —
      (1) pullback dari tutup tertinggi sejak masuk <= X%
      (2) tutup >= paras MA Y
      (3) trend saham: tutup > MA50 dan cerun MA50 > 0
      (4) trend pasaran: SPY > MA50 dan SPY > MA200 (hari itu)
    """
    c = a['c']
    if puncak <= 0 or (c[d] / puncak - 1.0) * 100.0 < -float(x_pct):
        return False
    lvl = a[y_ma][d]
    if not np.isfinite(lvl) or c[d] < lvl:
        return False
    if not (np.isfinite(a['ma50'][d]) and c[d] > a['ma50'][d]):
        return False
    if not (np.isfinite(a['cerun50'][d]) and a['cerun50'][d] > 0):
        return False
    return bool(pasaran_naik[d])


def jalan(a, i_masuk, ufuk, exit_nama, hold=None, pasaran_naik=None):
    """Jalankan satu dagangan. Pulangkan dict.

    i_masuk  : indeks hari isyarat; masuk pada BUKA i_masuk+1.
    exit_nama: nama dalam EXIT13, atau None = pegang sampai hujung ufuk.
    hold     : (X, Y) peraturan HOLD sebagai veto, atau None.
    """
    c, o, atr = a['c'], a['o'], a['atr']
    n = c.size
    i0 = i_masuk + 1
    if i0 >= n:
        return None
    masuk = o[i0]
    if not np.isfinite(masuk) or masuk <= 0:
        return None
    hadir = min(i_masuk + ufuk, n - 1)
    puncak = c[i0] if np.isfinite(c[i0]) else masuk
    puncak_atr = atr[i0]
    i_sig = -1
    for d in range(i0, hadir + 1):
        if np.isfinite(c[d]) and c[d] > puncak:
            puncak = c[d]
            puncak_atr = atr[d]
        if exit_nama is None:
            continue
        if _nyala(a, d, exit_nama, puncak, puncak_atr):
            if hold is not None and pasaran_naik is not None and hold_ok(
                    a, d, puncak, hold[0], hold[1], pasaran_naik):
                continue
            i_sig = d
            break
    if i_sig >= 0 and i_sig + 1 <= n - 1:
        i_keluar = i_sig + 1
        harga = o[i_keluar]
        sebab = exit_nama
        terbuka = False
    else:
        i_keluar = hadir
        harga = c[i_keluar]
        sebab = 'hujung_ufuk' if i_sig < 0 else 'hujung_data'
        terbuka = i_sig < 0
    if not np.isfinite(harga) or harga <= 0:
        return None
    seg = c[i0:i_keluar + 1]
    mfe = float(np.nanmax(seg) / masuk - 1.0) if np.isfinite(seg).any() else np.nan
    mae = float(np.nanmin(seg) / masuk - 1.0) if np.isfinite(seg).any() else np.nan
    # naik >= 10% selepas keluar? (exit terlalu awal)
    sisa = c[i_keluar:min(i_masuk + ufuk, n - 1) + 1]
    awal = bool(np.isfinite(sisa).any() and np.nanmax(sisa) >= harga * 1.10)
    return dict(i_masuk=i_masuk, i_keluar=i_keluar, masuk_kasar=float(masuk),
                keluar_kasar=float(harga), hari_pegang=int(i_keluar - i0 + 1),
                sebab=sebab, terbuka=terbuka, mfe=mfe, mae=mae, exit_awal=awal,
                terpotong=bool(i_keluar >= n - 1 and i_masuk + ufuk > n - 1))
