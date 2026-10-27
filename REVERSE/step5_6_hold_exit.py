"""STEP 5 (HOLD) dan STEP 6 (EXIT). Semua berlabel CALON sehingga lulus Step 7b.

AMARAN BIAS (arahan Step 5.6 dan 6.6): angka di sini dikira ATAS RUN SAHAJA — sampel yang sudah
terpilih kerana berjaya. Tiada peraturan HOLD atau signal EXIT boleh DITERIMA di sini.

Guna: python3 REVERSE/step5_6_hold_exit.py 2025
Output: REVERSE/hold_exit_<TAHUN>.csv, .cache/kaki_<TAHUN>.csv, .cache/puncak_<TAHUN>.csv
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
from REVERSE.teras import data as D, ind as I, keluar as K, signal as S, stat as T  # noqa: E402
from REVERSE.teras.kos import kos_sisi  # noqa: E402

CACHE = AKAR / 'REVERSE' / '.cache'
KELUAR = AKAR / 'REVERSE'

CALON20 = K.EXIT13 + ['div_rsi', 'div_macd', 'climax_25_15h', 'gap_besar', 'jauh_ma50_2x',
                      'atr_lonjak_15x', 'pullback_amaran']


def _calon_amaran(a, ind, d, med_jauh, med_atr, kelas_pb):
    """7 calon amaran Step 6.2 yang bukan exit tunggal (SPEC §13.6)."""
    c, o = a['c'], a['o']
    out = {}
    h = a['hist']
    r = a['rsi']
    if d >= 10:
        hh = c[d] >= np.nanmax(c[d - 10:d])
        out['div_rsi'] = bool(hh and np.isfinite(r[d]) and r[d] < np.nanmax(r[d - 10:d]))
        out['div_macd'] = bool(hh and np.isfinite(h[d]) and h[d] < np.nanmax(h[d - 10:d]))
    else:
        out['div_rsi'] = out['div_macd'] = False
    out['climax_25_15h'] = bool(d >= 15 and np.isfinite(c[d - 15]) and c[d - 15] > 0
                                and c[d] / c[d - 15] - 1.0 >= 0.25)
    roc20 = ind['roc20'].to_numpy('float64')
    out['gap_besar'] = bool(d > 0 and np.isfinite(o[d]) and o[d] > a['c'][d - 1] * 1.05
                            and np.isfinite(roc20[d]) and roc20[d] >= 20)
    jm = ind['j_ma50'].to_numpy('float64')
    out['jauh_ma50_2x'] = bool(np.isfinite(jm[d]) and np.isfinite(med_jauh) and med_jauh > 0
                               and jm[d] >= 2.0 * med_jauh)
    ap = ind['atr_pct'].to_numpy('float64')
    out['atr_lonjak_15x'] = bool(np.isfinite(ap[d]) and np.isfinite(med_atr) and med_atr > 0
                                 and ap[d] >= 1.5 * med_atr)
    out['pullback_amaran'] = bool(kelas_pb.get(d) == 'AMARAN')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tahun', type=int)
    a_ = ap.parse_args()
    th = a_.tahun
    t0 = time.time()
    runs = pd.read_csv(KELUAR / f'runs_{th}.csv')
    for k in ('tarikh_mula', 'tarikh_sah', 'tarikh_puncak', 'tarikh_tamat'):
        runs[k] = pd.to_datetime(runs[k], errors='coerce')
    runs = runs[(runs.entry_sah == 'ya') & (runs.sebab_kecuali.isna() | (runs.sebab_kecuali == ''))]
    tick = sorted(set(runs.ticker))
    fr = D.muat_harga(tick, f'{th - 2}-06-01', '2026-10-16')
    ix = D.muat_indeks(f'{th - 2}-06-01', '2026-10-16')
    spy, qqq = ix['SPY']['close'], ix['QQQ']['close']
    pas = ((spy > spy.rolling(50, min_periods=50).mean())
           & (spy > spy.rolling(200, min_periods=200).mean())
           & (qqq > qqq.rolling(50, min_periods=50).mean())
           & (qqq > qqq.rolling(200, min_periods=200).mean())
           & (spy.rolling(50, min_periods=50).mean().pct_change(10) > 0))
    spy_jatuh = spy.pct_change(5) < -0.02
    univ = D.universe()
    peta = D.peta_sektor(list(fr))
    si = D.indeks_sektor(fr, peta, univ, spy.index)
    kuin = json.loads((CACHE / f'kuintil_{th}.json').read_text())['sempadan']
    ikonteks = I.kira_indeks({k: v['close'] for k, v in ix.items()})
    print(f'[{time.time()-t0:.0f}s] run dianalisis {len(runs)} | ticker {len(fr)}')

    kaki_rows, puncak_rows, ringkas = [], [], []
    snap_hold, snap_exit = [], []
    for tk, grp in runs.groupby('ticker'):
        g = fr.get(tk)
        if g is None:
            continue
        sek = peta.loc[tk, 'sektor']
        ind = I.kira(g, spy=spy, sektor_idx=si[sek] if sek in si.columns else None)
        ind = ind.join(ikonteks.reindex(ind.index))
        arr = K.sedia(g, ind)
        c = arr['c']
        idx = g.index
        pas_a = pas.reindex(idx).fillna(False).to_numpy()
        jat_a = spy_jatuh.reindex(idx).fillna(False).to_numpy()
        sek_ma = ind['sektor_atas_ma50'].to_numpy('float64')
        ema9 = arr['ema9']; ema21 = arr['ema21']; ma50 = arr['ma50']
        rsi = arr['rsi']; hist = arr['hist']; voln = arr['voln']
        jm = ind['j_ma50'].to_numpy('float64'); apct = ind['atr_pct'].to_numpy('float64')
        adx = ind['adx14'].to_numpy('float64')
        for _, r in grp.iterrows():
            if pd.isna(r.tarikh_sah) or r.tarikh_sah not in idx or r.tarikh_puncak not in idx:
                continue
            i_s = int(idx.get_loc(r.tarikh_sah))
            i_p = int(idx.get_loc(r.tarikh_puncak))
            i_t = int(idx.get_loc(r.tarikh_tamat)) if r.tarikh_tamat in idx else min(i_p + 63,
                                                                                    c.size - 1)
            if i_p <= i_s:
                continue
            seg = slice(i_s, i_p + 1)
            med_jauh = float(np.nanmedian(jm[seg])) if np.isfinite(jm[seg]).any() else np.nan
            med_atr = float(np.nanmedian(apct[seg])) if np.isfinite(apct[seg]).any() else np.nan
            # kaki / pullback dalam tetingkap run
            puncak_sem = c[i_s]
            i_puncak_sem = i_s
            dalam, i_palung, palung = False, -1, np.inf
            palung_lepas = r.rendah_mula
            kelas_pb = {}
            for d in range(i_s + 1, i_t + 1):
                x = c[d]
                if not dalam:
                    if x <= puncak_sem * 0.95:
                        dalam, i_palung, palung = True, d, x
                else:
                    if x < palung:
                        i_palung, palung = d, x
                    if x > puncak_sem:
                        # pullback pulih
                        trend_shm = (np.isfinite(ma50[i_palung]) and c[i_palung] > ma50[i_palung]
                                     and np.isfinite(ind['cerun_ma50'].to_numpy()[i_palung])
                                     and ind['cerun_ma50'].to_numpy()[i_palung] > 0
                                     and palung > palung_lepas)
                        kls = ('PULLBACK SIHAT' if (trend_shm and pas_a[i_palung])
                               else ('PULLBACK PASARAN' if (trend_shm and jat_a[i_palung])
                                     else 'AMARAN'))
                        kelas_pb[i_palung] = kls
                        kaki_rows.append(dict(
                            ticker=tk, tarikh_sah=r.tarikh_sah.date(), kumpulan=r.kumpulan,
                            jenis_kenaikan=r.jenis_kenaikan, tarikh_palung=idx[i_palung].date(),
                            kedalaman_pct=round((palung / puncak_sem - 1) * 100, 2),
                            henti_ema21=int(np.isfinite(ema21[i_palung])
                                            and palung >= ema21[i_palung] * 0.98),
                            henti_ma50=int(np.isfinite(ma50[i_palung])
                                           and palung >= ma50[i_palung] * 0.98),
                            rsi_palung=round(float(rsi[i_palung]), 1)
                            if np.isfinite(rsi[i_palung]) else np.nan,
                            vol_n50_palung=round(float(voln[i_palung]), 2)
                            if np.isfinite(voln[i_palung]) else np.nan,
                            hari_pulih=float(d - i_palung), kelas_pullback=kls,
                            trend_pasaran=int(pas_a[i_palung]),
                            trend_sektor=float(sek_ma[i_palung] > 0.5)
                            if np.isfinite(sek_ma[i_palung]) else np.nan,
                            puncak_baru=1, selepas_puncak_akhir=int(i_palung > i_p)))
                        sh = ind.iloc[i_palung].to_dict()
                        sh.update(ticker=tk, jenis_kenaikan=r.jenis_kenaikan,
                                  puncak_baru=1, selepas_puncak_akhir=int(i_palung > i_p),
                                  tarikh=idx[i_palung])
                        snap_hold.append(sh)
                        if i_palung <= i_p:
                            se = ind.iloc[i_palung].to_dict()
                            se.update(ticker=tk, jenis_kenaikan=r.jenis_kenaikan,
                                      sebelum_puncak_akhir=0, tarikh=idx[i_palung])
                            snap_exit.append(se)
                        palung_lepas = palung
                        dalam, palung = False, np.inf
                if x > puncak_sem:
                    puncak_sem, i_puncak_sem = x, d
            if dalam and i_palung > 0:
                trend_shm = (np.isfinite(ma50[i_palung]) and c[i_palung] > ma50[i_palung])
                kls = ('PULLBACK SIHAT' if (trend_shm and pas_a[i_palung])
                       else ('PULLBACK PASARAN' if (trend_shm and jat_a[i_palung]) else 'AMARAN'))
                kelas_pb[i_palung] = kls
                kaki_rows.append(dict(
                    ticker=tk, tarikh_sah=r.tarikh_sah.date(), kumpulan=r.kumpulan,
                    jenis_kenaikan=r.jenis_kenaikan, tarikh_palung=idx[i_palung].date(),
                    kedalaman_pct=round((palung / puncak_sem - 1) * 100, 2),
                    henti_ema21=int(np.isfinite(ema21[i_palung])
                                    and palung >= ema21[i_palung] * 0.98),
                    henti_ma50=int(np.isfinite(ma50[i_palung]) and palung >= ma50[i_palung] * 0.98),
                    rsi_palung=round(float(rsi[i_palung]), 1)
                    if np.isfinite(rsi[i_palung]) else np.nan,
                    vol_n50_palung=round(float(voln[i_palung]), 2)
                    if np.isfinite(voln[i_palung]) else np.nan,
                    hari_pulih=np.nan, kelas_pullback=kls, trend_pasaran=int(pas_a[i_palung]),
                    trend_sektor=float(sek_ma[i_palung] > 0.5)
                    if np.isfinite(sek_ma[i_palung]) else np.nan,
                    puncak_baru=0, selepas_puncak_akhir=int(i_palung > i_p)))
            if dalam and i_palung > 0:
                sh = ind.iloc[i_palung].to_dict()
                sh.update(ticker=tk, jenis_kenaikan=r.jenis_kenaikan, puncak_baru=0,
                          selepas_puncak_akhir=int(i_palung > i_p), tarikh=idx[i_palung])
                snap_hold.append(sh)
            for d in range(max(i_p - 10, i_s), i_p + 1):
                se = ind.iloc[d].to_dict()
                se.update(ticker=tk, jenis_kenaikan=r.jenis_kenaikan,
                          sebelum_puncak_akhir=1, tarikh=idx[d])
                snap_exit.append(se)
            # ringkasan HOLD per run
            hh = hist[i_s:i_p + 1]
            naik5 = int(np.sum((np.diff(c[i_s:i_p + 1]) / c[i_s:i_p] >= 0.05)
                               & (voln[i_s + 1:i_p + 1] >= 2.0)))
            t3 = max((i_p - i_s) // 3, 1)
            def arah(v):
                a1 = np.nanmean(v[:t3]); a2 = np.nanmean(v[-t3:])
                if not (np.isfinite(a1) and np.isfinite(a2)):
                    return ''
                return 'naik' if a2 > a1 * 1.1 else ('turun' if a2 < a1 * 0.9 else 'mendatar')
            ringkas.append(dict(
                ticker=tk, tarikh_sah=r.tarikh_sah.date(), kumpulan=r.kumpulan,
                jenis_kenaikan=r.jenis_kenaikan, hari_run=int(i_p - i_s),
                pct_atas_ema9=round(float(np.nanmean(c[seg] > ema9[seg]) * 100), 1),
                pct_atas_ema21=round(float(np.nanmean(c[seg] > ema21[seg]) * 100), 1),
                pct_atas_ma50=round(float(np.nanmean(c[seg] > ma50[seg]) * 100), 1),
                rsi_min=round(float(np.nanmin(rsi[seg])), 1), rsi_maks=round(float(np.nanmax(rsi[seg])), 1),
                arah_adx=arah(adx[seg]), arah_atr=arah(apct[seg]),
                n_hist_negatif=int(np.nansum(hh < 0)),
                hist_negatif_lalu_sambung=int(np.nansum(hh < 0) > 0),
                n_hari_naik5_vol2=naik5))
            # EXIT: 20 calon, hari pertama menyala selepas tarikh_sah
            for nm in CALON20:
                i_nyala = -1
                puncak = c[i_s]; p_atr = arr['atr'][i_s]
                for d in range(i_s + 1, i_t + 1):
                    if np.isfinite(c[d]) and c[d] > puncak:
                        puncak, p_atr = c[d], arr['atr'][d]
                    if nm in K.EXIT13:
                        ny = K._nyala(arr, d, nm, puncak, p_atr)
                    else:
                        ny = _calon_amaran(arr, ind, d, med_jauh, med_atr, kelas_pb)[nm]
                    if ny:
                        i_nyala = d
                        break
                if i_nyala < 0:
                    puncak_rows.append(dict(ticker=tk, tarikh_sah=r.tarikh_sah.date(),
                                            kumpulan=r.kumpulan, jenis_kenaikan=r.jenis_kenaikan,
                                            calon=nm, menyala=0))
                    continue
                i_keluar = min(i_nyala + 1, c.size - 1)
                ks = kos_sisi(float((g['close'] * g['volume']).iloc[max(i_s - 20, 0):i_s].median()))
                masuk = arr['o'][i_s + 1] * (1 + ks) if i_s + 1 < c.size else c[i_s]
                harga = arr['o'][i_keluar] * (1 - ks)
                pul = harga / masuk - 1.0
                denom = c[i_p] - c[i_s]
                kekal = ((harga - masuk) / (c[i_p] - masuk) * 100.0
                         if c[i_p] >= 1.02 * c[i_s] and (c[i_p] - masuk) > 0 else np.nan)
                sisa = c[i_keluar:min(i_p + 63, c.size - 1) + 1]
                palsu = int(np.isfinite(sisa).any() and np.nanmax(sisa) >= harga * 1.10)
                puncak_rows.append(dict(
                    ticker=tk, tarikh_sah=r.tarikh_sah.date(), kumpulan=r.kumpulan,
                    jenis_kenaikan=r.jenis_kenaikan, calon=nm, menyala=1,
                    hari_dari_puncak=int(i_nyala - i_p),
                    pulangan_exit=round(float(pul) * 100, 2),
                    pct_kekal=round(float(kekal), 1) if np.isfinite(kekal) else 'tidak_boleh_dikira',
                    exit_palsu=palsu))
    kk = pd.DataFrame(kaki_rows)
    pp = pd.DataFrame(puncak_rows)
    rr = pd.DataFrame(ringkas)
    kk.to_csv(CACHE / f'kaki_{th}.csv', index=False)
    pp.to_csv(CACHE / f'puncak_{th}.csv', index=False)
    rr.to_csv(CACHE / f'ringkas_hold_{th}.csv', index=False)
    print(f'[{time.time()-t0:.0f}s] kaki {len(kk)} | baris calon exit {len(pp)} | run {len(rr)}')

    rows = []
    # STEP 5.3 kelas pullback
    for kls, d in kk.groupby('kelas_pullback'):
        rows.append(dict(fasa='HOLD', jenis='kelas_pullback', nama=kls, n=len(d),
                         pct_sambung_puncak_baru=round(d.puncak_baru.mean() * 100, 1),
                         purata_kedalaman=round(d.kedalaman_pct.mean(), 2),
                         purata_hari_pulih=round(pd.to_numeric(d.hari_pulih,
                                                               errors='coerce').mean(), 1),
                         label='CALON'))
    # STEP 5.5 grid 18 peraturan HOLD (deskriptif atas run)
    for x in K.HOLD_X:
        for y in K.HOLD_Y:
            m = kk.kedalaman_pct >= -float(x)
            kol = 'henti_ema21' if y == 'ema21' else ('henti_ma50' if y == 'ma50' else None)
            mm = m if kol is None else (m | (kk[kol] == 1))
            d = kk[mm]
            rows.append(dict(fasa='HOLD', jenis='peraturan_hold', nama=f'X={x}%,Y={y}',
                             n=len(d),
                             pct_sambung_puncak_baru=round(d.puncak_baru.mean() * 100, 1)
                             if len(d) else '',
                             purata_kedalaman=round(d.kedalaman_pct.mean(), 2) if len(d) else '',
                             purata_hari_pulih=round(pd.to_numeric(
                                 d.hari_pulih, errors='coerce').mean(), 1) if len(d) else '',
                             label='CALON'))
    # STEP 6.3 metrik 20 calon exit
    for nm, d in pp.groupby('calon'):
        ny = d[d.menyala == 1]
        rows.append(dict(fasa='EXIT', jenis='calon_exit', nama=nm, n=len(ny),
                         pct_menyala=round(d.menyala.mean() * 100, 1),
                         median_hari_dari_puncak=round(float(
                             pd.to_numeric(ny.hari_dari_puncak, errors='coerce').median()), 1)
                         if len(ny) else '',
                         median_pulangan_exit=round(float(pd.to_numeric(
                             ny.pulangan_exit, errors='coerce').median()), 2) if len(ny) else '',
                         median_pct_kekal=round(float(pd.to_numeric(
                             ny.pct_kekal, errors='coerce').median()), 1) if len(ny) else '',
                         kadar_exit_palsu=round(float(pd.to_numeric(
                             ny.exit_palsu, errors='coerce').mean()) * 100, 1) if len(ny) else '',
                         label='CALON'))
        for kump in ('SUPER PADU', 'PADU', 'BIASA'):
            dk = ny[ny.kumpulan == kump]
            if len(dk) < 10:
                continue
            rows.append(dict(fasa='EXIT', jenis=f'calon_exit_{kump}', nama=nm, n=len(dk),
                             median_pulangan_exit=round(float(pd.to_numeric(
                                 dk.pulangan_exit, errors='coerce').median()), 2),
                             median_pct_kekal=round(float(pd.to_numeric(
                                 dk.pct_kekal, errors='coerce').median()), 1),
                             kadar_exit_palsu=round(float(pd.to_numeric(
                                 dk.exit_palsu, errors='coerce').mean()) * 100, 1), label='CALON'))
        for jn in ('BERTANGGA', 'LONJAKAN', 'STABIL'):
            dk = ny[ny.jenis_kenaikan == jn]
            if len(dk) < 10:
                continue
            rows.append(dict(fasa='EXIT', jenis=f'calon_exit_{jn}', nama=nm, n=len(dk),
                             median_pulangan_exit=round(float(pd.to_numeric(
                                 dk.pulangan_exit, errors='coerce').median()), 2),
                             median_pct_kekal=round(float(pd.to_numeric(
                                 dk.pct_kekal, errors='coerce').median()), 1),
                             kadar_exit_palsu=round(float(pd.to_numeric(
                                 dk.exit_palsu, errors='coerce').mean()) * 100, 1), label='CALON'))
    # ---- STEP 5.4 dan 6.5: common/unique HOLD dan EXIT (kelas Step 4) ----
    sh = pd.DataFrame(snap_hold)
    se = pd.DataFrame(snap_exit)
    sh.to_csv(CACHE / f'snap_hold_{th}.csv', index=False)
    se.to_csv(CACHE / f'snap_exit_{th}.csv', index=False)
    kosong = np.array([], dtype=bool)
    # HOLD: 31 binari + 5 boolean khusus pullback = 36 signal tunggal
    for subset in ('S1', 'S2'):
        d = sh if subset == 'S1' else sh[sh.jenis_kenaikan == 'BERTANGGA']
        if len(d) < 50:
            continue
        sg = {k: v for k, v in S.bina(d, {}).items() if k.startswith('b:')}
        kd = d['j_ma50'].to_numpy('float64')
        sg['b:pullback_dalam_7pct'] = np.isfinite(kd) & (kd >= -7.0)
        sg['b:atas_ema21'] = (d['tutup'].to_numpy() > d['ema21'].to_numpy())
        sg['b:atas_ma50'] = (d['tutup'].to_numpy() > d['ma50'].to_numpy())
        sg['b:pasaran_naik'] = (d['spy_ma50'].to_numpy() > 0.5) & (d['spy_ma200'].to_numpy() > 0.5)
        sg['b:sektor_naik'] = (d['sektor_atas_ma50'].to_numpy() > 0.5)
        hasil = np.where(d.puncak_baru.to_numpy() == 1, 'PADU', 'GAGAL')
        for nm in sorted(sg):
            mt = T.metrik(hasil, sg[nm], kosong, 'PADU')
            rows.append(dict(fasa='HOLD', jenis='common_unique', nama=nm, subset=subset,
                             n=mt['n'], n_populasi=len(d),
                             K_padu=round(mt['K_padu'], 2), K_gagal=round(mt['K_gagal'], 2),
                             lift=round(mt['lift'], 3) if np.isfinite(mt['lift']) else '',
                             presisi=round(mt['presisi'], 2) if np.isfinite(mt['presisi']) else '',
                             lift_presisi=round(mt['lift_presisi'], 3)
                             if np.isfinite(mt['lift_presisi']) else '',
                             kelas=T.kelas(mt['K_padu'], mt['lift'], mt['n']), label='CALON'))
    # EXIT: hujung kuintil 31 indikator berterusan yang kekal selepas dedup = 62 signal
    for subset in ('S1', 'S2'):
        d = se if subset == 'S1' else se[se.jenis_kenaikan == 'BERTANGGA']
        if len(d) < 50:
            continue
        sg = {k: v for k, v in S.bina(d, kuin).items() if k.startswith(('q1:', 'q5:'))}
        hasil = np.where(d.sebelum_puncak_akhir.to_numpy() == 1, 'PADU', 'GAGAL')
        for nm in sorted(sg):
            mt = T.metrik(hasil, sg[nm], kosong, 'PADU')
            rows.append(dict(fasa='EXIT', jenis='common_unique', nama=nm, subset=subset,
                             n=mt['n'], n_populasi=len(d),
                             K_padu=round(mt['K_padu'], 2), K_gagal=round(mt['K_gagal'], 2),
                             lift=round(mt['lift'], 3) if np.isfinite(mt['lift']) else '',
                             presisi=round(mt['presisi'], 2) if np.isfinite(mt['presisi']) else '',
                             lift_presisi=round(mt['lift_presisi'], 3)
                             if np.isfinite(mt['lift_presisi']) else '',
                             kelas=T.kelas(mt['K_padu'], mt['lift'], mt['n']), label='CALON'))
    out = pd.DataFrame(rows)
    out.to_csv(KELUAR / f'hold_exit_{th}.csv', index=False)
    n_hold = len(out[(out.fasa == 'HOLD') & (out.jenis.isin(['common_unique',
                                                             'peraturan_hold']))])
    n_exit = len(out[(out.fasa == 'EXIT') & (out.jenis.isin(['common_unique', 'calon_exit']))])
    print(f'N keluarga HOLD sebenar = {n_hold} | N keluarga EXIT sebenar = {n_exit}')
    lg = out[['fasa', 'jenis', 'nama', 'n']].copy()
    lg.insert(0, 'tarikh', '2026-10-27')
    lg['subset'] = out.get('subset', '-')
    lg['keterangan'] = 'STEP5/6 ' + out.jenis.astype(str)
    lg['keputusan'] = 'CALON'
    lg[['tarikh', 'fasa', 'subset', 'nama', 'jenis', 'n', 'keterangan', 'keputusan']].to_csv(
        KELUAR / 'log_ujian.csv', mode='a', header=False, index=False)
    print(out[out.jenis == 'kelas_pullback'].to_string(index=False))
    print(out[out.jenis == 'calon_exit'][['nama', 'n', 'pct_menyala', 'median_hari_dari_puncak',
                                          'median_pulangan_exit', 'median_pct_kekal',
                                          'kadar_exit_palsu']].to_string(index=False))
    print(f'[{time.time()-t0:.0f}s] siap — SEMUA berlabel CALON (amaran bias Step 5.6/6.6)')


if __name__ == '__main__':
    main()
