"""Metrik, kelas dan kawalan statistik REVERSE (SPEC §11.5, §11.6, Step 8)."""
import numpy as np
import pandas as pd


def metrik(hasil, ada, rawak_ada, keluarga='PADU'):
    """Metrik KEHADIRAN + PRESISI bagi satu signal.

    hasil     : array label ('SUPER PADU','PADU','BIASA','GAGAL') bagi populasi peristiwa
    ada       : array boolean kemunculan signal, sejajar hasil
    rawak_ada : array boolean kemunculan signal atas KAWALAN RAWAK
    keluarga  : 'PADU' (lift ikut K_padu) atau 'SUPER PADU' (lift ikut K_super)
    """
    n_pop = hasil.size
    out = {}
    for lab, kunci in (('SUPER PADU', 'K_super'), ('PADU', 'K_padu'), ('BIASA', 'K_biasa'),
                       ('GAGAL', 'K_gagal')):
        m = hasil == lab
        out[kunci] = float(ada[m].mean() * 100.0) if m.any() else np.nan
    out['K_rawak'] = float(rawak_ada.mean() * 100.0) if rawak_ada.size else np.nan
    utama = out['K_super'] if keluarga == 'SUPER PADU' else out['K_padu']
    asas = max([x for x in (out['K_biasa'], out['K_gagal'], 100.0 / max(n_pop, 1))
                if np.isfinite(x)] or [np.nan])
    out['lift'] = float(utama / asas) if (np.isfinite(utama) and asas and asas > 0) else np.nan
    ar = max(out['K_rawak'] if np.isfinite(out['K_rawak']) else 0.0, 100.0 / max(n_pop, 1))
    out['lift_rawak'] = float(utama / ar) if (np.isfinite(utama) and ar > 0) else np.nan
    sasar = np.isin(hasil, ['PADU', 'SUPER PADU'])
    n_ada = int(ada.sum())
    out['n'] = n_ada
    out['presisi'] = float(sasar[ada].mean() * 100.0) if n_ada else np.nan
    out['kadar_asas_padu'] = float(sasar.mean() * 100.0) if n_pop else np.nan
    out['lift_presisi'] = (float(out['presisi'] / out['kadar_asas_padu'])
                           if (np.isfinite(out['presisi']) and out['kadar_asas_padu'] > 0)
                           else np.nan)
    return out


def kelas(k_utama, lift, n):
    """SPEC §11.6."""
    if not (np.isfinite(k_utama) and np.isfinite(lift)):
        return 'TIDAK BERGUNA'
    if k_utama >= 50 and lift >= 2:
        return 'TERAS'
    if 15 <= k_utama < 50 and lift >= 3:
        return 'UNIQUE'
    if 3 <= k_utama < 15 and lift >= 5 and n >= 30:
        return 'LANGKA'
    if (k_utama >= 50 and 1.5 <= lift < 2.0) or (15 <= k_utama < 50 and 2.0 <= lift < 3.0):
        return 'SEDERHANA'
    if k_utama >= 50 and lift < 1.5:
        return 'COMMON BIASA'
    return 'TIDAK BERGUNA'


def bh_fdr(p, q=0.01):
    """Benjamini-Hochberg. Pulangkan (lulus boolean array, ambang)."""
    p = np.asarray(p, dtype='float64')
    ok = np.isfinite(p)
    lulus = np.zeros(p.size, dtype=bool)
    if not ok.any():
        return lulus, np.nan
    idx = np.flatnonzero(ok)
    srt = idx[np.argsort(p[idx])]
    m = srt.size
    amb = np.nan
    for i in range(m - 1, -1, -1):
        if p[srt[i]] <= q * (i + 1) / m:
            amb = p[srt[i]]
            lulus[srt[:i + 1]] = True
            break
    return lulus, amb


def permutasi_lift(hasil, ada, bulan, keluarga='PADU', n=1000, benih=42):
    """Nilai-p label rawak: tukar label hasil secara rawak, bilangan sama SETIAP BULAN.

    Pulangkan (nilai_p, purata_lift_rawak).
    """
    rng = np.random.default_rng(benih)
    asal = metrik(hasil, ada, np.array([], dtype=bool), keluarga)['lift']
    if not np.isfinite(asal):
        return np.nan, np.nan
    kump = {}
    for b in np.unique(bulan):
        kump[b] = np.flatnonzero(bulan == b)
    lifts = np.empty(n)
    h = hasil.copy()
    for k in range(n):
        for b, ix in kump.items():
            h[ix] = rng.permutation(hasil[ix])
        lifts[k] = metrik(h, ada, np.array([], dtype=bool), keluarga)['lift']
    baik = np.isfinite(lifts)
    if not baik.any():
        return np.nan, np.nan
    p = float((lifts[baik] >= asal).sum() + 1) / float(baik.sum() + 1)
    return p, float(np.nanmean(lifts[baik]))


def bootstrap_blok(nilai, blok, n=1000, benih=42, stat='mean'):
    """Bootstrap blok (sampel blok dengan penggantian). Pulangkan (p5, p50, p95)."""
    rng = np.random.default_rng(benih)
    nilai = np.asarray(nilai, dtype='float64')
    ok = np.isfinite(nilai)
    nilai, blok = nilai[ok], np.asarray(blok)[ok]
    if nilai.size == 0:
        return (np.nan,) * 3
    unik, inv = np.unique(blok, return_inverse=True)
    peta = [np.flatnonzero(inv == i) for i in range(unik.size)]
    out = np.empty(n)
    for k in range(n):
        pilih = rng.integers(0, unik.size, unik.size)
        ix = np.concatenate([peta[j] for j in pilih])
        v = nilai[ix]
        out[k] = np.mean(v) if stat == 'mean' else np.median(v)
    return (float(np.quantile(out, 0.05)), float(np.quantile(out, 0.50)),
            float(np.quantile(out, 0.95)))


def bootstrap_lift_blok(hasil, ada, blok, keluarga='PADU', n=1000, benih=42):
    """Had bawah 95% bagi lift, bootstrap blok."""
    rng = np.random.default_rng(benih)
    unik, inv = np.unique(np.asarray(blok), return_inverse=True)
    peta = [np.flatnonzero(inv == i) for i in range(unik.size)]
    out = np.full(n, np.nan)
    kosong = np.array([], dtype=bool)
    for k in range(n):
        pilih = rng.integers(0, unik.size, unik.size)
        ix = np.concatenate([peta[j] for j in pilih])
        out[k] = metrik(hasil[ix], ada[ix], kosong, keluarga)['lift']
    baik = np.isfinite(out)
    if not baik.any():
        return np.nan
    return float(np.quantile(out[baik], 0.05))


def jangkaan(pulangan):
    """(kadar menang x purata menang) - (kadar kalah x purata kalah)."""
    r = np.asarray(pulangan, dtype='float64')
    r = r[np.isfinite(r)]
    if r.size == 0:
        return np.nan, np.nan, np.nan, np.nan
    menang, kalah = r[r > 0], r[r <= 0]
    km = menang.size / r.size
    pm = float(menang.mean()) if menang.size else 0.0
    pk = float(-kalah.mean()) if kalah.size else 0.0
    return float(km * pm - (1 - km) * pk), float(km), pm, pk


def siri_kalah_terpanjang(pulangan):
    r = np.asarray(pulangan, dtype='float64')
    best = cur = 0
    for x in r:
        if np.isfinite(x) and x <= 0:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return int(best)


def mdd(ekuiti):
    e = np.asarray(ekuiti, dtype='float64')
    if e.size == 0:
        return np.nan
    puncak = np.maximum.accumulate(e)
    return float(np.min(e / puncak - 1.0) * 100.0)
