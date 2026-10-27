"""STEP 1-2 + cache indikator: kenal pasti run, peristiwa sah, dan snapshot indikator.

Satu laluan atas semua ticker universe tahun kajian:
  - indikator 77 lajur (REVERSE/teras/ind.py)
  - run layak + gagal (SPEC §4)       -> runs_<TAHUN>.csv, skipped_<TAHUN>.csv
  - peristiwa sah kausal (SPEC §7)
  - metrik hadapan dua ufuk (SPEC §3.2) -> .cache/signals_<TAHUN>.parquet

Guna: python3 REVERSE/step1_run.py 2025 [--ticker N]
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
from REVERSE.teras import data as D, ind as I, run as R  # noqa: E402
from REVERSE.teras.kos import kos_sisi  # noqa: E402

KELUAR = AKAR / 'REVERSE'
CACHE = KELUAR / '.cache'
UFUK_LABEL = 63
UFUK_NILAI = 252


def _maju(c, i, ufuk, masuk):
    """(mfe, mae, hari_mfe, pulangan_akhir, terpotong) berasaskan tutup selepas hari masuk."""
    n = c.size
    a = i + 1
    b = min(i + ufuk, n - 1)
    if a > b or not np.isfinite(masuk) or masuk <= 0:
        return (np.nan,) * 4 + (True,)
    seg = c[a:b + 1]
    if not np.isfinite(seg).any():
        return (np.nan,) * 4 + (True,)
    mx = np.nanmax(seg)
    mn = np.nanmin(seg)
    return (float(mx / masuk - 1.0), float(mn / masuk - 1.0),
            int(np.nanargmax(seg) + 1), float(seg[-1] / masuk - 1.0), bool(b < i + ufuk))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tahun', type=int)
    ap.add_argument('--ticker', type=int, default=0, help='hadkan bilangan ticker (ujian)')
    a = ap.parse_args()
    th = a.tahun
    t0 = time.time()

    univ = D.universe()
    tick = D.tickers_tahun(th, univ)
    if a.ticker:
        tick = tick[:a.ticker]
    mula_muat = f'{th - 2}-06-01'
    akhir_muat = '2026-10-16'
    fr = D.muat_harga(tick, mula_muat, akhir_muat)
    ix = D.muat_indeks(mula_muat, akhir_muat)
    spy = ix['SPY']['close']
    kal = spy.index
    peta = D.peta_sektor(list(fr))
    si = D.indeks_sektor(fr, peta, univ, kal)
    ikonteks = I.kira_indeks({k: v['close'] for k, v in ix.items()})
    ahli = D.topeng_bulan(univ)
    kump = univ.drop_duplicates('ticker').set_index('ticker')['kumpulan']
    aa = R.peta_ambil_alih(AKAR / 'BacktestShariah2' / 'data' / 'ambil_alih.csv')
    print(f'[{time.time()-t0:.0f}s] ticker {len(fr)} | bar kalendar {len(kal)} | sektor {si.shape[1]}')
    liputan = int((peta.sumber_sektor != 'tiada').sum())
    kesediaan = dict(n_ticker_universe=len(tick), n_ticker_harga=len(fr), n_bar_kalendar=len(kal),
                     n_sektor=int(si.shape[1]), liputan_sektor=liputan,
                     pct_liputan_sektor=round(liputan / max(len(tick), 1) * 100, 1),
                     n_lain_lain=int((peta.sektor == 'Lain-lain').sum()),
                     n_kelas_asas=int((peta.sumber_sektor == 'kelas_asas').sum()),
                     mula_muat=mula_muat, akhir_muat=akhir_muat)

    t_awal = pd.Timestamp(f'{th}-01-01')
    t_akhir = pd.Timestamp(f'{th}-12-31')
    baris_r, baris_s, blok = [], [], []
    IND = None
    for tk, g in fr.items():
        if len(g) < 260:
            baris_s.append(dict(ticker=tk, tarikh='', sebab='bar tidak cukup (< 260)'))
            continue
        sek = peta.loc[tk, 'sektor']
        ind = I.kira(g, spy=spy, sektor_idx=si[sek] if sek in si.columns else None)
        if IND is None:
            IND = [c for c in ind.columns if c not in ('tutup', 'buka')]
        ema21, ma50, ma200 = ind['ema21'], ind['ma50'], ind['ma200']
        kd = kump.get(tk, '?')
        layak, gagal = R.jumpa_run(g, ema21)
        idx = g.index
        for rec in layak:
            tm = idx[rec['i_mula']]
            if not (t_awal <= tm <= t_akhir):
                continue
            if (tk, tm.year * 100 + tm.month) not in ahli:
                baris_s.append(dict(ticker=tk, tarikh=tm.date(), sebab='luar universe bulan itu'))
                continue
            baris_r.append(R.baris_run(tk, g, ema21, ma50, ma200, rec, kd,
                                       sek, peta.loc[tk, 'industri'], aa))
        for rec in gagal:
            tm = idx[rec['i_mula']]
            if t_awal <= tm <= t_akhir:
                baris_s.append(dict(ticker=tk, tarikh=tm.date(), sebab=rec['sebab'],
                                    hari_ke_puncak=rec['hari_ke_puncak'],
                                    pct_naik_rendah=round(rec['naik_rendah'], 2)))
        # peristiwa sah kausal
        per = {p[0]: p for p in R.peristiwa_sah(g, ema21)}
        # pemetaan hari -> run
        hari_sah = {rec['i_sah']: rec for rec in layak if rec['i_sah'] >= 0}
        julat_run = [(rec['i_mula'], rec['i_tamat'], rec) for rec in layak]
        # blok baris tahun kajian
        m = (idx >= t_awal) & (idx <= t_akhir)
        pos = np.flatnonzero(m)
        if pos.size == 0:
            continue
        c = g['close'].to_numpy('float64')
        o = g['open'].to_numpy('float64')
        to = (g['close'] * g['volume']).rolling(20, min_periods=10).median().to_numpy('float64')
        atr = ind['atr14'].to_numpy('float64')
        sub = ind.iloc[pos].copy()
        sub.insert(0, 'ticker', tk)
        sub.insert(1, 'tarikh', idx[pos])
        ym = idx[pos].year * 100 + idx[pos].month
        sub['dalam_univ'] = [1.0 if (tk, int(x)) in ahli else 0.0 for x in ym]
        sub['kumpulan_data'] = kd
        sub['sektor'] = sek
        sub['industri'] = peta.loc[tk, 'industri']
        # peristiwa + hasil
        jen, hasil, pk_naik, pk_hari, pk_jenis, pk_dag = [], [], [], [], [], []
        for i in pos:
            if i not in per:
                jen.append(''), hasil.append(''), pk_naik.append(np.nan)
                pk_hari.append(np.nan), pk_jenis.append(''), pk_dag.append(np.nan)
                continue
            if i in hari_sah:
                rec = hari_sah[i]
                jen.append('mula_run')
            else:
                rec = None
                for i0, i1, rr in julat_run:
                    if i0 <= i <= i1:
                        rec = rr
                        break
                jen.append('dalam_run' if rec is not None else 'tiada_run')
            if rec is None:
                hasil.append('GAGAL'), pk_naik.append(np.nan)
                pk_hari.append(np.nan), pk_jenis.append(''), pk_dag.append(np.nan)
            else:
                hasil.append(R.kelas_kumpulan(rec['naik_rendah']))
                pk_naik.append(rec['naik_rendah'])
                pk_hari.append(rec['hari_ke_puncak'])
                kk = R.kaki_dan_jenis(c, ind['ema21'].to_numpy('float64'), rec['i_mula'],
                                      rec['i_sah'] if rec['i_sah'] >= 0 else rec['i_mula'],
                                      rec['i_puncak'], rec['rendah_mula'])
                pk_jenis.append(kk[4])
                pk_dag.append((c[rec['i_puncak']] - c[rec['i_sah']]) / c[rec['i_sah']] * 100.0
                              if rec['i_sah'] >= 0 else np.nan)
        sub['jenis_peristiwa'] = jen
        sub['hasil'] = hasil
        sub['run_naik'] = pk_naik
        sub['run_hari'] = pk_hari
        sub['run_jenis'] = pk_jenis
        sub['run_dagang'] = pk_dag
        # metrik hadapan (masuk buka esok, kos sisi beli)
        kol = {k: [] for k in ('harga_masuk', 'mfe63', 'mae63', 'hari_mfe63', 'pul63',
                               'mfe252', 'mae252', 'hari_mfe252', 'pul252', 'terpotong',
                               'henti7_dahulu', 'henti2atr_dahulu', 'kos_sisi')}
        for i in pos:
            if i + 1 >= c.size:
                for k in kol:
                    kol[k].append(np.nan)
                continue
            ks = kos_sisi(to[i])
            masuk = o[i + 1] * (1.0 + ks)
            l63 = _maju(c, i, UFUK_LABEL, masuk)
            l252 = _maju(c, i, UFUK_NILAI, masuk)
            kol['harga_masuk'].append(masuk)
            kol['kos_sisi'].append(ks)
            kol['mfe63'].append(l63[0]), kol['mae63'].append(l63[1])
            kol['hari_mfe63'].append(l63[2]), kol['pul63'].append(l63[3])
            kol['mfe252'].append(l252[0]), kol['mae252'].append(l252[1])
            kol['hari_mfe252'].append(l252[2]), kol['pul252'].append(l252[3])
            kol['terpotong'].append(1.0 if l252[4] else 0.0)
            # henti dahulu atau +20% dahulu (ufuk 252)
            h7 = masuk * 0.93
            h2 = masuk - 2.0 * atr[i] if np.isfinite(atr[i]) else np.nan
            tgt = masuk * 1.20
            a7 = a2 = at = -1
            for d in range(i + 1, min(i + UFUK_NILAI, c.size - 1) + 1):
                if a7 < 0 and c[d] <= h7:
                    a7 = d
                if a2 < 0 and np.isfinite(h2) and c[d] <= h2:
                    a2 = d
                if at < 0 and c[d] >= tgt:
                    at = d
                if a7 >= 0 and a2 >= 0 and at >= 0:
                    break
            kol['henti7_dahulu'].append(1.0 if (a7 >= 0 and (at < 0 or a7 < at)) else 0.0)
            kol['henti2atr_dahulu'].append(1.0 if (a2 >= 0 and (at < 0 or a2 < at)) else 0.0)
        for k, v in kol.items():
            sub[k] = v
        blok.append(sub.reset_index(drop=True))
    print(f'[{time.time()-t0:.0f}s] indikator + run siap')

    sig = pd.concat(blok, ignore_index=True)
    sig = sig.join(ikonteks.reindex(sig['tarikh']).reset_index(drop=True))
    for c in sig.columns:
        if sig[c].dtype == 'float64':
            sig[c] = sig[c].astype('float32')
    CACHE.mkdir(parents=True, exist_ok=True)
    sig.to_parquet(CACHE / f'signals_{th}.parquet', index=False)
    (CACHE / f'lajur_ind_{th}.json').write_text(json.dumps(IND))
    kesediaan['n_hari_saham'] = int(len(sig))
    kesediaan['n_hari_saham_dalam_univ'] = int((sig.dalam_univ == 1).sum())
    kesediaan['saat_larian'] = round(time.time() - t0, 1)
    kesediaan['saat_per_ticker'] = round((time.time() - t0) / max(len(fr), 1), 4)
    (CACHE / f'kesediaan_{th}.json').write_text(json.dumps(kesediaan, indent=1))

    runs = pd.DataFrame(baris_r)
    if len(runs):
        runs = runs.sort_values(['tarikh_mula', 'ticker'])
        runs.drop(columns=['i_mula', 'i_sah', 'i_puncak', 'i_tamat']).to_csv(
            KELUAR / f'runs_{th}.csv', index=False)
    pd.DataFrame(baris_s).to_csv(KELUAR / f'skipped_{th}.csv', index=False)

    # ringkasan bulanan
    rows = []
    for b in [f'{th}-{m:02d}' for m in range(1, 13)]:
        r = runs[runs.bulan_mula == b] if len(runs) else runs
        pk = sig[(sig.tarikh.dt.strftime('%Y-%m') == b) & (sig.jenis_peristiwa != '')
                 & (sig.dalam_univ == 1)]
        rows.append(dict(bulan=b, n_run=len(r),
                         n_super=int((r.kumpulan == 'SUPER PADU').sum()) if len(r) else 0,
                         n_padu=int((r.kumpulan == 'PADU').sum()) if len(r) else 0,
                         n_biasa=int((r.kumpulan == 'BIASA').sum()) if len(r) else 0,
                         n_bertangga=int((r.jenis_kenaikan == 'BERTANGGA').sum()) if len(r) else 0,
                         n_lonjakan=int((r.jenis_kenaikan == 'LONJAKAN').sum()) if len(r) else 0,
                         n_stabil=int((r.jenis_kenaikan == 'STABIL').sum()) if len(r) else 0,
                         n_entry_sah=int((r.entry_sah == 'ya').sum()) if len(r) else 0,
                         n_masih_naik=int((r.masih_naik == 'ya').sum()) if len(r) else 0,
                         n_peristiwa=len(pk),
                         med_naik=round(float(r.pct_naik_rendah.median()), 1) if len(r) else 0.0))
    ms = pd.DataFrame(rows)
    ms.to_csv(KELUAR / f'monthly_summary_{th}.csv', index=False)

    n_s2 = int(((runs.jenis_kenaikan == 'BERTANGGA')).sum()) if len(runs) else 0
    # Peristiwa SAH = syarat tarikh sah DAN ticker dalam universe bulan itu (SPEC §7).
    ev = sig[(sig.jenis_peristiwa != '') & (sig.dalam_univ == 1)]
    # HAD BERSYARAT dinilai atas POPULASI KEPUTUSAN (a) mula_run + tiada_run (SPEC §11.1, pindaan
    # §13.4): kuasa statistik keputusan Step 4 ditentukan oleh populasi yang keputusan dibuat atas.
    dec = ev[ev.jenis_peristiwa.isin(['mula_run', 'tiada_run'])]
    ev_s2 = dec[(dec.run_jenis == 'BERTANGGA') & (dec.hasil == 'PADU')]
    had = len(ev_s2) < 300
    print(ms.to_string(index=False))
    print(f'RUN {len(runs)} | entry_sah ya {int((runs.entry_sah=="ya").sum()) if len(runs) else 0}'
          f' ({(runs.entry_sah=="ya").mean()*100 if len(runs) else 0:.1f}%)'
          f' | BERTANGGA {n_s2} | peristiwa sah {len(ev)}')
    print(f'n peristiwa PADU dalam S2 (populasi keputusan a) = {len(ev_s2)} -> HAD BERSYARAT '
          f'{"AKTIF (pemicu x 1 konteks sahaja)" if had else "TIDAK AKTIF"}')
    (CACHE / f'had_bersyarat_{th}.json').write_text(json.dumps(
        {'n_padu_s2_keputusan': int(len(ev_s2)),
         'n_padu_s2_semua': int(((ev.run_jenis == 'BERTANGGA') & (ev.hasil == 'PADU')).sum()),
         'n_peristiwa_sah': int(len(ev)), 'n_populasi_keputusan': int(len(dec)),
         'had_aktif': bool(had)}))
    print(f'[{time.time()-t0:.0f}s] siap')


if __name__ == '__main__':
    main()
