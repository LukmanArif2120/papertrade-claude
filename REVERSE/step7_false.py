"""STEP 7 — false signal ENTRY (imbasan ke hadapan seluruh universe, tanpa hindsight).

Laluan sedia (sekali): bagi SETIAP (ticker, hari 2025) kira ciri hadapan yang bebas signal —
jenis kenaikan hadapan, ketulenan trend, pulangan dengan henti keras -2xATR ufuk 63, dan
pengesahan 1-2 tutup. Kemudian metrik Step 7 bagi setiap signal = agregat atas lajur cache.

Guna: python3 REVERSE/step7_false.py 2025
Output: REVERSE/false_signal_<TAHUN>.csv, .cache/hadapan_<TAHUN>.parquet, .cache/lulus7_<TAHUN>.json
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.teras import data as D, signal as S  # noqa: E402
from REVERSE.teras.kos import kos_sisi  # noqa: E402

CACHE = AKAR / 'REVERSE' / '.cache'
KELUAR = AKAR / 'REVERSE'
UFUK_L = 63
BUNYI_KEKERAPAN = 5000
BUNYI_LIFT = 1.5

# Penapis calon Step 7.4 — dipradaftar
PENAPIS = {
    'spy_atas_ma50': lambda d: d.spy_ma50.to_numpy() > 0.5,
    'spy_atas_ma200': lambda d: d.spy_ma200.to_numpy() > 0.5,
    'sektor_atas_ma50': lambda d: d.sektor_atas_ma50.to_numpy() > 0.5,
    'vol_n50_ge_1.5': lambda d: d.vol_n50.to_numpy() >= 1.5,
    'harga_atas_ma50': lambda d: d.j_ma50.to_numpy() >= 0,
    'lapis_ge_3': lambda d: d.lapis.to_numpy() >= 3,
    'pengesahan_1_tutup': lambda d: d.conf1.to_numpy() > 0,
    'pengesahan_2_tutup': lambda d: d.conf2.to_numpy() > 0,
}


def _jenis_hadapan(c, e, i0, i_mfe):
    """Klasifikasi jenis kenaikan (SPEC §5.3) atas laluan hadapan i0 -> i_mfe."""
    if i_mfe <= i0:
        return '', np.nan
    seg = c[i0:i_mfe + 1]
    n = seg.size
    kaki = 0
    palung, puncak_sem, dalam, pk = [], seg[0], False, np.inf
    pecah = False
    for k in range(1, n):
        x = seg[k]
        if not dalam:
            if x <= puncak_sem * 0.95:
                dalam, pk = True, x
        else:
            pk = min(pk, x)
            if x > puncak_sem:
                kaki += 1
                asas = palung[-1] if palung else seg[0]
                if pk <= asas:
                    pecah = True
                palung.append(pk)
                dalam, pk = False, np.inf
        puncak_sem = max(puncak_sem, x)
    dif = np.diff(seg)
    naik2 = np.sort(dif[dif > 0])[-2:].sum() if (dif > 0).any() else 0.0
    jum = seg[-1] - seg[0]
    sumb2 = naik2 / jum if jum > 0 else np.nan
    es = e[i0:i_mfe + 1]
    sah = np.isfinite(es)
    pct = float(np.sum(seg[sah] > es[sah]) / max(sah.sum(), 1) * 100.0) if sah.any() else np.nan
    if np.isfinite(sumb2) and sumb2 >= 0.50:
        return 'LONJAKAN', pct
    if kaki >= 2 and not pecah and np.isfinite(pct) and pct >= 60.0:
        return 'BERTANGGA', pct
    return 'STABIL', pct


def sedia_hadapan(th):
    """Lajur hadapan bebas signal bagi setiap (ticker, hari tahun kajian)."""
    f = CACHE / f'hadapan_{th}.parquet'
    if f.exists():
        return pd.read_parquet(f)
    sig = pd.read_parquet(CACHE / f'signals_{th}.parquet',
                          columns=['ticker', 'tarikh', 'harga_masuk', 'hari_mfe63'])
    tick = sorted(sig.ticker.unique())
    fr = D.muat_harga(tick, f'{th - 2}-06-01', '2026-10-16')
    out = []
    t0 = time.time()
    for n, (tk, g) in enumerate(fr.items()):
        c = g['close'].to_numpy('float64')
        o = g['open'].to_numpy('float64')
        e = g['close'].ewm(span=21, adjust=False, min_periods=21).mean().to_numpy('float64')
        tr = pd.concat([g['high'] - g['low'], (g['high'] - g['close'].shift(1)).abs(),
                        (g['low'] - g['close'].shift(1)).abs()], axis=1).max(axis=1)
        atr = tr.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean().to_numpy('float64')
        to = (g['close'] * g['volume']).rolling(20, min_periods=10).median().to_numpy('float64')
        idx = g.index
        m = (idx >= pd.Timestamp(f'{th}-01-01')) & (idx <= pd.Timestamp(f'{th}-12-31'))
        for i in np.flatnonzero(m):
            if i + 1 >= c.size:
                continue
            ks = kos_sisi(to[i])
            masuk = o[i + 1] * (1 + ks)
            if not np.isfinite(masuk) or masuk <= 0:
                continue
            b = min(i + UFUK_L, c.size - 1)
            seg = c[i + 1:b + 1]
            if seg.size == 0 or not np.isfinite(seg).any():
                continue
            i_mfe = int(np.nanargmax(seg)) + i + 1
            jen, ket = _jenis_hadapan(c, e, i + 1, i_mfe)
            # henti keras -2xATR, ufuk 63
            hs = masuk - 2.0 * atr[i] if np.isfinite(atr[i]) else np.nan
            i_keluar, sebab = b, 'hujung_63'
            if np.isfinite(hs):
                hit = np.flatnonzero(seg <= hs)
                if hit.size:
                    i_keluar, sebab = min(i + 1 + int(hit[0]) + 1, c.size - 1), 'henti2atr'
            harga = (o[i_keluar] if sebab == 'henti2atr' else c[i_keluar]) * (1 - ks)
            out.append((tk, idx[i], jen, ket, float(harga / masuk - 1.0), sebab,
                        int(i_keluar - i), float(c[i + 1] / c[i] - 1.0) if i + 1 < c.size else np.nan,
                        float(c[min(i + 2, c.size - 1)] / c[i] - 1.0)))
        if n % 400 == 0:
            print(f'  sedia hadapan {n}/{len(fr)} [{time.time()-t0:.0f}s]')
    d = pd.DataFrame(out, columns=['ticker', 'tarikh', 'jenis_hadapan', 'ketulenan',
                                   'pul_henti2atr', 'sebab_keluar', 'hari_pegang', 'r1', 'r2'])
    d['conf1'] = (d.r1 > 0).astype('int8')
    d['conf2'] = (d.r2 > 0).astype('int8')
    d.to_parquet(f, index=False)
    print(f'  sedia hadapan siap: {len(d)} baris [{time.time()-t0:.0f}s]')
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tahun', type=int)
    a_ = ap.parse_args()
    th = a_.tahun
    t0 = time.time()
    sig = pd.read_parquet(CACHE / f'signals_{th}.parquet')
    sig = sig[sig.dalam_univ == 1].reset_index(drop=True)
    had = sedia_hadapan(th)
    df = sig.merge(had, on=['ticker', 'tarikh'], how='left')
    kuin = json.loads((CACHE / f'kuintil_{th}.json').read_text())['sempadan']
    corong = json.loads((CACHE / f'corong_{th}.json').read_text())['signal']
    rawak = pd.read_parquet(CACHE / f'rawak_{th}.parquet').merge(had, on=['ticker', 'tarikh'],
                                                                 how='left')
    print(f'[{time.time()-t0:.0f}s] hari universe {len(df)} | signal corong {len(corong)}')

    sg = S.bina(df, kuin)
    asas_tepat = float((rawak.mfe63 >= 0.30).mean() * 100)
    rows = []
    lulus = []
    for nm in corong:
        ada = sg[nm]
        d = df[ada]
        n = len(d)
        if n == 0:
            continue
        tepat = float((d.mfe63 >= 0.30).mean() * 100)
        lift_tepat = tepat / max(asas_tepat, 1e-9)
        bunyi = (n > BUNYI_KEKERAPAN and lift_tepat < BUNYI_LIFT)
        jen = d.jenis_hadapan.fillna('')
        jk, kmn, pmn, pkl = __import__('REVERSE.teras.stat', fromlist=['x']).jangkaan(
            d.pul_henti2atr.to_numpy())
        kapasiti = 'TULANG BELAKANG' if (n >= 130 and np.isfinite(jk) and jk > 0) else 'PELENGKAP'
        pusing = n / 12.0
        baris = dict(
            signal=nm, n_kemunculan=n, kekerapan_setahun=n,
            kadar_tepat_mfe30=round(tepat, 2), kadar_asas_rawak=round(asas_tepat, 2),
            lift_tepat=round(lift_tepat, 3),
            kadar_palsu_bawah10=round(float((d.mfe63 < 0.10).mean() * 100), 2),
            kadar_tepat_bertangga=round(float((jen == 'BERTANGGA').mean() * 100), 2),
            ketulenan_trend_median=round(float(d.ketulenan.median()), 1),
            mfe63_p50=round(float(d.mfe63.quantile(.50)) * 100, 2),
            mfe63_p75=round(float(d.mfe63.quantile(.75)) * 100, 2),
            mfe63_p90=round(float(d.mfe63.quantile(.90)) * 100, 2),
            mfe252_p50=round(float(d.mfe252.quantile(.50)) * 100, 2),
            mfe252_p75=round(float(d.mfe252.quantile(.75)) * 100, 2),
            mfe252_p90=round(float(d.mfe252.quantile(.90)) * 100, 2),
            median_hari_mfe63=round(float(d.hari_mfe63.median()), 1),
            pct_mfe63_ge30=round(float((d.mfe63 >= 0.30).mean() * 100), 2),
            pct_mfe63_ge100=round(float((d.mfe63 >= 1.00).mean() * 100), 2),
            pct_mfe252_ge100=round(float((d.mfe252 >= 1.00).mean() * 100), 2),
            purata_mfe63_selepas_kos=round(float(d.mfe63.mean()) * 100, 2),
            pct_henti7_dahulu=round(float(d.henti7_dahulu.mean() * 100), 2),
            pct_henti2atr_dahulu=round(float(d.henti2atr_dahulu.mean() * 100), 2),
            jangkaan_henti2atr=round(jk * 100, 3) if np.isfinite(jk) else '',
            kadar_menang=round(kmn * 100, 2) if np.isfinite(kmn) else '',
            purata_menang=round(pmn * 100, 2) if np.isfinite(pmn) else '',
            purata_kalah=round(pkl * 100, 2) if np.isfinite(pkl) else '',
            jangkaan_bulanan_anggaran=round(jk * 100 * min(pusing / 11.0, 1.0), 3)
            if np.isfinite(jk) else '',
            pct_terpotong=round(float(d.terpotong.mean() * 100), 1),
            kapasiti=kapasiti, tanda='BUNYI LATAR' if bunyi else '')
        rows.append(baris)
        if not bunyi:
            lulus.append(nm)
        # STEP 7.4 punca false signal + penapis
        benar = d[d.mfe63 >= 0.30]
        palsu = d[d.mfe63 < 0.10]
        for pn, fn in PENAPIS.items():
            try:
                mb, mp = fn(benar), fn(palsu)
            except Exception:
                continue
            if len(benar) == 0 or len(palsu) == 0:
                continue
            buang_palsu = float((~mp).mean() * 100)
            buang_benar = float((~mb).mean() * 100)
            rows.append(dict(signal=f'{nm} | penapis:{pn}', n_kemunculan=int(mb.sum() + mp.sum()),
                             kadar_tepat_mfe30='', buang_palsu_pct=round(buang_palsu, 1),
                             buang_benar_pct=round(buang_benar, 1),
                             tanda='PENAPIS LULUS' if (buang_palsu >= 30 and buang_benar <= 10)
                             else ''))
    out = pd.DataFrame(rows)
    out.to_csv(KELUAR / f'false_signal_{th}.csv', index=False)
    (CACHE / f'lulus7_{th}.json').write_text(json.dumps({'signal': lulus}, indent=1))
    ut = out[~out.signal.str.contains(r'\| penapis:')]
    print(ut[['signal', 'n_kemunculan', 'kadar_tepat_mfe30', 'lift_tepat', 'kadar_palsu_bawah10',
              'mfe63_p90', 'pct_mfe63_ge100', 'jangkaan_henti2atr', 'kapasiti',
              'tanda']].to_string(index=False))
    pl = out[out.tanda == 'PENAPIS LULUS']
    print(f'\npenapis lulus kriteria (buang >= 30% palsu, <= 10% benar): {len(pl)}')
    if len(pl):
        print(pl[['signal', 'buang_palsu_pct', 'buang_benar_pct']].head(20).to_string(index=False))
    print(f'signal lulus Step 7 (bukan BUNYI LATAR): {len(lulus)}')
    print(f'[{time.time()-t0:.0f}s] siap')


if __name__ == '__main__':
    main()
