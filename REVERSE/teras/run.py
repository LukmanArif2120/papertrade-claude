"""Pengesanan run dan peristiwa sah (REVERSE SPEC §4, §4.1, §5, §7).

Semua pengesanan peristiwa adalah kausal: hari t hanya guna bar <= t.
Pengesanan run menggunakan tetingkap 63 hari SELEPAS tarikh_mula (UFUK LABEL) — ini maklumat masa
depan dan dipakai HANYA untuk melabel hasil, bukan untuk signal.
"""
import numpy as np
import pandas as pd

TETINGKAP = 63      # hari dagangan selepas tarikh_mula
PANTAU = 63         # hari pemantauan turun selepas tarikh_puncak
LOOKBACK = 20       # rendah terendah 20 hari
HAD_SAH = 10        # tarikh_sah mesti <= 10 hari dagangan selepas tarikh_mula
NAIK_MULA = 0.05    # 5% di atas rendah


def _grid_layak(hari, naik):
    """SPEC §4.7."""
    if hari <= 21:
        return naik >= 10.0
    if hari <= 42:
        return naik >= 20.0
    if hari <= 63:
        return naik >= 30.0
    return False


def kelas_kumpulan(naik):
    if naik >= 100.0:
        return 'SUPER PADU'
    if naik >= 30.0:
        return 'PADU'
    return 'BIASA'


def kelas_laju(hari):
    if hari <= 21:
        return 'PANTAS'
    if hari <= 42:
        return 'SEDANG'
    return 'PERLAHAN'


def bucket_naik(naik):
    for b in (300, 200, 100, 50, 30, 20, 10):
        if naik >= b:
            return f'{b}%+'
    return '<10%'


def bucket_tempoh(hari):
    return '<=21' if hari <= 21 else ('<=42' if hari <= 42 else '<=63')


def kaki_dan_jenis(c, ema21, i_mula, i_sah, i_puncak, rendah_mula):
    """Kaki (pullback-pulih), higher low, sumbangan 2 hari, % hari atas EMA21, jenis kenaikan.

    c, ema21 : array tutup dan EMA21 penuh.
    Dinilai tarikh_mula -> tarikh_puncak (SPEC §5.3).
    """
    seg = c[i_mula:i_puncak + 1]
    n = seg.size
    kaki = 0
    palung = []
    puncak_sem = seg[0]
    dalam_turun = False
    palung_kini = np.inf
    pecah = False
    for k in range(1, n):
        x = seg[k]
        if not dalam_turun:
            if x <= puncak_sem * 0.95:
                dalam_turun = True
                palung_kini = x
        else:
            palung_kini = min(palung_kini, x)
            if x > puncak_sem:
                kaki += 1
                asas = palung[-1] if palung else rendah_mula
                if palung_kini <= asas:
                    pecah = True
                palung.append(palung_kini)
                dalam_turun = False
                palung_kini = np.inf
        puncak_sem = max(puncak_sem, x)
    # sumbangan dua hari kenaikan harga terbesar
    dif = np.diff(seg) if n > 1 else np.array([0.0])
    naik2 = np.sort(dif[dif > 0])[-2:].sum() if (dif > 0).any() else 0.0
    jumlah = c[i_puncak] - rendah_mula
    sumb2 = float(naik2 / jumlah) if jumlah > 0 else np.nan
    # % hari atas EMA21 dari tarikh_sah hingga tarikh_puncak
    a, b = i_sah, i_puncak
    if b >= a:
        e = ema21[a:b + 1]
        cc = c[a:b + 1]
        sah = np.isfinite(e)
        pct = float(np.sum(cc[sah] > e[sah]) / max(sah.sum(), 1) * 100.0) if sah.any() else np.nan
    else:
        pct = np.nan
    if np.isfinite(sumb2) and sumb2 >= 0.50:
        jenis = 'LONJAKAN'
    elif kaki >= 2 and not pecah and np.isfinite(pct) and pct >= 60.0:
        jenis = 'BERTANGGA'
    else:
        jenis = 'STABIL'
    hari_besar = int(np.argmax(dif)) + 1 if dif.size else 0
    return kaki, pecah, sumb2, pct, jenis, hari_besar


def peristiwa_sah(g, ema21):
    """Senarai indeks bar yang merupakan PERISTIWA SAH (kausal; SPEC §7).

    Pulangkan list (i_peristiwa, i_mula, rendah_mula).
    """
    low = g['low'].to_numpy('float64')
    c = g['close'].to_numpy('float64')
    e = ema21.to_numpy('float64')
    n = c.size
    out = []
    lihat = {}   # i_mula -> sudah ada peristiwa
    for t in range(LOOKBACK, n):
        w = low[t - LOOKBACK:t]
        if not np.isfinite(w).any():
            continue
        j = int(np.nanargmin(w)) + (t - LOOKBACK)
        r = low[j]
        if not np.isfinite(r) or r <= 0:
            continue
        if t - j > HAD_SAH:
            continue
        if j in lihat:
            continue
        if c[t] >= r * (1.0 + NAIK_MULA) and np.isfinite(e[t]) and c[t] > e[t]:
            lihat[j] = True
            out.append((t, j, float(r)))
    return out


def jumpa_run(g, ema21):
    """Senarai run (layak dan gagal) bagi satu ticker. SPEC §4.

    Pulangkan (run_layak, gagal) di mana setiap item ialah dict indeks bar.
    """
    low = g['low'].to_numpy('float64')
    c = g['close'].to_numpy('float64')
    e = ema21.to_numpy('float64')
    n = c.size
    layak, gagal = [], []
    batas = 0
    t = LOOKBACK
    while t < n:
        w = low[t - LOOKBACK:t]
        if not np.isfinite(w).any():
            t += 1
            continue
        j = int(np.nanargmin(w)) + (t - LOOKBACK)
        r = low[j]
        if j < batas or not np.isfinite(r) or r <= 0 or c[t] < r * (1.0 + NAIK_MULA):
            t += 1
            continue
        # run bermula di j
        hujung = min(j + TETINGKAP, n - 1)
        if hujung <= j:
            break
        seg = c[j + 1:hujung + 1]
        if not np.isfinite(seg).any():
            batas = j + 1
            t += 1
            continue
        i_pk = int(np.nanargmax(seg)) + j + 1
        hari_pk = i_pk - j
        naik = (c[i_pk] - r) / r * 100.0
        masih = i_pk >= hujung - 2
        # tarikh sah
        i_sah = -1
        for d in range(j + 1, min(j + HAD_SAH, n - 1) + 1):
            if c[d] >= r * (1.0 + NAIK_MULA) and np.isfinite(e[d]) and c[d] > e[d]:
                i_sah = d
                break
        rec = dict(i_mula=j, rendah_mula=float(r), i_puncak=i_pk, hari_ke_puncak=hari_pk,
                   naik_rendah=float(naik), masih_naik=bool(masih), i_sah=i_sah,
                   i_hujung_tetingkap=hujung)
        if not _grid_layak(hari_pk, naik):
            rec['sebab'] = 'terlalu perlahan'
            gagal.append(rec)
            batas = j + 1
            t = max(t + 1, j + 1)
            continue
        # tarikh turun
        hp = c[i_pk]
        i10 = i25 = -1
        akhir_pantau = min(i_pk + PANTAU, n - 1)
        for d in range(i_pk + 1, akhir_pantau + 1):
            if i10 < 0 and c[d] <= hp * 0.90:
                i10 = d
            if c[d] <= hp * 0.75:
                i25 = d
                break
        rec['i_turun_10'] = i10
        rec['i_turun_25'] = i25
        rec['i_tamat'] = i25 if i25 >= 0 else akhir_pantau
        rec['tamat_pemantauan'] = i25 < 0
        layak.append(rec)
        batas = rec['i_tamat']
        t = max(t + 1, rec['i_tamat'])
    return layak, gagal


def baris_run(tk, g, ema21, ma50, ma200, rec, kump_data, sektor, industri, ambil_alih=None):
    """Satu baris runs_<TAHUN>.csv daripada rec jumpa_run()."""
    idx = g.index
    c = g['close'].to_numpy('float64')
    e = ema21.to_numpy('float64')
    j, i_pk, i_sah = rec['i_mula'], rec['i_puncak'], rec['i_sah']
    i_tamat = rec['i_tamat']
    r = rec['rendah_mula']
    naik = rec['naik_rendah']
    kaki, pecah, sumb2, pct_e, jenis, hari_besar = kaki_dan_jenis(
        c, e, j, i_sah if i_sah >= 0 else j, i_pk, r)
    harga_sah = float(c[i_sah]) if i_sah >= 0 else np.nan
    naik_dag = (c[i_pk] - harga_sah) / harga_sah * 100.0 if i_sah >= 0 else np.nan
    m50 = ma50.to_numpy('float64')
    m200 = ma200.to_numpy('float64')
    graf = (np.isfinite(m200[i_pk]) and i_pk >= 20 and np.isfinite(m200[i_pk - 20])
            and c[i_pk] > m50[i_pk] > m200[i_pk] and m200[i_pk] > m200[i_pk - 20])
    sebab = ''
    if ambil_alih is not None and tk in ambil_alih:
        if idx[i_pk] >= ambil_alih[tk]:
            sebab = 'ambil_alih'
    return dict(
        ticker=tk, sektor=sektor, industri=industri,
        bulan_mula=idx[j].strftime('%Y-%m'),
        tarikh_mula=idx[j].date(), rendah_mula=round(r, 4),
        harga_mula=round(float(c[j]), 4),
        tarikh_sah=idx[i_sah].date() if i_sah >= 0 else '',
        harga_sah=round(harga_sah, 4) if i_sah >= 0 else '',
        entry_sah='ya' if i_sah >= 0 else 'tidak',
        tarikh_puncak=idx[i_pk].date(), harga_puncak=round(float(c[i_pk]), 4),
        hari_ke_puncak=rec['hari_ke_puncak'],
        masih_naik='ya' if rec['masih_naik'] else 'tidak',
        tarikh_turun_10=idx[rec['i_turun_10']].date() if rec['i_turun_10'] >= 0 else '',
        tarikh_turun_25=idx[rec['i_turun_25']].date() if rec['i_turun_25'] >= 0 else '',
        tarikh_tamat=idx[i_tamat].date(),
        tamat_pemantauan='ya' if rec['tamat_pemantauan'] else 'tidak',
        harga_tamat=round(float(c[i_tamat]), 4),
        pct_naik_rendah=round(naik, 2),
        pct_naik_dagang=round(naik_dag, 2) if i_sah >= 0 else '',
        bucket_pct=bucket_naik(naik), bucket_tempoh=bucket_tempoh(rec['hari_ke_puncak']),
        kumpulan=kelas_kumpulan(naik), kelas_laju=kelas_laju(rec['hari_ke_puncak']),
        graf_menaik='ya' if graf else 'tidak', kumpulan_data=kump_data,
        sebab_kecuali=sebab, jenis_kenaikan=jenis, bilangan_kaki=kaki,
        higher_low_pecah='ya' if pecah else 'tidak',
        sumbangan_2_hari=round(sumb2, 4) if np.isfinite(sumb2) else '',
        pct_hari_atas_ema21=round(pct_e, 1) if np.isfinite(pct_e) else '',
        hari_kenaikan_terbesar=hari_besar,
        i_mula=j, i_sah=i_sah, i_puncak=i_pk, i_tamat=i_tamat,
    )


def peta_ambil_alih(path):
    """{ticker: Timestamp tarikh_umum}."""
    try:
        d = pd.read_csv(path)
    except Exception:
        return {}
    out = {}
    for _, r in d.iterrows():
        try:
            out[str(r['saham']).strip()] = pd.Timestamp(r['tarikh_umum'])
        except Exception:
            continue
    return out
