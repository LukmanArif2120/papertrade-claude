"""STEP 4 — common & unique signal (ENTRY).

Carian atas S1 dan S2, kumpulan data A dan B, dua populasi peristiwa:
  (a) mula_run + tiada_run  -> KEPUTUSAN ikut ini
  (b) semua peristiwa       -> semakan kekukuhan
Dua keluarga: PADU (lift ikut K_padu) dan SUPER PADU (lift ikut K_super), FDR berasingan.

Guna: python3 REVERSE/step4_common.py 2025
Output: REVERSE/common_unique_<TAHUN>.csv, .cache/corong_<TAHUN>.json, log_ujian.csv
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
from REVERSE.teras import signal as S, stat as T  # noqa: E402

CACHE = AKAR / 'REVERSE' / '.cache'
KELUAR = AKAR / 'REVERSE'
HAD_CORONG = 30


def subset_topeng(ev, subset):
    """Topeng baris populasi bagi subset (SPEC §5.6, pindaan §13.8)."""
    if subset == 'S1':
        return np.ones(len(ev), dtype=bool)
    # S2: hasil BERTANGGA sahaja + kegagalan bersih (tiada_run)
    return ((ev.run_jenis.to_numpy() == 'BERTANGGA') | (ev.hasil.to_numpy() == 'GAGAL'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tahun', type=int)
    a = ap.parse_args()
    th = a.tahun
    t0 = time.time()
    sig = pd.read_parquet(CACHE / f'signals_{th}.parquet')
    kuin = json.loads((CACHE / f'kuintil_{th}.json').read_text())['sempadan']
    rawak = pd.read_parquet(CACHE / f'rawak_{th}.parquet')
    ev = sig[(sig.jenis_peristiwa != '') & (sig.dalam_univ == 1)].reset_index(drop=True)
    sg = S.bina(ev, kuin)
    sg_rawak = S.bina(rawak, kuin)
    nama = sorted(sg)
    print(f'peristiwa sah {len(ev)} | signal {len(nama)} | rawak {len(rawak)}')

    minggu = ev.tarikh.dt.strftime('%G-W%V').to_numpy()
    industri = ev.industri.to_numpy()
    hasil_all = ev.hasil.to_numpy()
    rows = []
    for subset in ('S1', 'S2'):
        ms = subset_topeng(ev, subset)
        for pop_nama, mp in (('a', ev.jenis_peristiwa.isin(['mula_run', 'tiada_run']).to_numpy()),
                             ('b', np.ones(len(ev), dtype=bool))):
            for kd in ('A', 'B'):
                mk = (ev.kumpulan_data.to_numpy() == kd)
                m = ms & mp & mk
                if m.sum() < 50:
                    continue
                mr = (rawak.kumpulan_data.to_numpy() == kd)
                hasil = hasil_all[m]
                for keluarga in ('PADU', 'SUPER PADU'):
                    for nm in nama:
                        ada = sg[nm][m]
                        mt = T.metrik(hasil, ada, sg_rawak[nm][mr], keluarga)
                        k_utama = mt['K_super'] if keluarga == 'SUPER PADU' else mt['K_padu']
                        kls = T.kelas(k_utama, mt['lift'], mt['n'])
                        sub_ada = ada
                        ind_a = industri[m][sub_ada]
                        mg_a = minggu[m][sub_ada]
                        tema = ''
                        if ind_a.size:
                            vc = pd.Series(ind_a).value_counts(normalize=True)
                            if float(vc.iloc[0]) >= 0.5:
                                tema = 'BERGANTUNG PADA TEMA'
                        jen = ev.run_jenis.to_numpy()[m][sub_ada]
                        jen = jen[jen != '']
                        pb = float((jen == 'BERTANGGA').mean() * 100) if jen.size else np.nan
                        pl = float((jen == 'LONJAKAN').mean() * 100) if jen.size else np.nan
                        ps = float((jen == 'STABIL').mean() * 100) if jen.size else np.nan
                        tanda = []
                        if mt['n'] < 20:
                            tanda.append('SAMPEL KECIL')
                        if tema:
                            tanda.append(tema)
                        if np.isfinite(pl) and pl >= 50:
                            tanda.append('LONJAKAN BERITA')
                        rows.append(dict(
                            subset=subset, populasi=pop_nama, kumpulan_data=kd,
                            keluarga=keluarga, fasa='ENTRY', signal=nm,
                            K_super=round(mt['K_super'], 2), K_padu=round(mt['K_padu'], 2),
                            K_biasa=round(mt['K_biasa'], 2), K_gagal=round(mt['K_gagal'], 2),
                            K_rawak=round(mt['K_rawak'], 2),
                            lift=round(mt['lift'], 3) if np.isfinite(mt['lift']) else '',
                            lift_rawak=round(mt['lift_rawak'], 3)
                            if np.isfinite(mt['lift_rawak']) else '',
                            presisi=round(mt['presisi'], 2) if np.isfinite(mt['presisi']) else '',
                            kadar_asas_padu=round(mt['kadar_asas_padu'], 2),
                            lift_presisi=round(mt['lift_presisi'], 3)
                            if np.isfinite(mt['lift_presisi']) else '',
                            kelas=kls, n=mt['n'], n_populasi=int(m.sum()),
                            n_industri=int(pd.unique(ind_a).size), n_minggu=int(pd.unique(mg_a).size),
                            purata_pct_naik_rendah=round(float(np.nanmean(
                                ev.run_naik.to_numpy()[m][sub_ada])), 2) if sub_ada.any() else '',
                            purata_pct_naik_dagang=round(float(np.nanmean(
                                ev.run_dagang.to_numpy()[m][sub_ada])), 2) if sub_ada.any() else '',
                            purata_hari_ke_puncak=round(float(np.nanmean(
                                ev.run_hari.to_numpy()[m][sub_ada])), 1) if sub_ada.any() else '',
                            pct_bertangga=round(pb, 1) if np.isfinite(pb) else '',
                            pct_lonjakan=round(pl, 1) if np.isfinite(pl) else '',
                            pct_stabil=round(ps, 1) if np.isfinite(ps) else '',
                            tanda='; '.join(tanda)))
    out = pd.DataFrame(rows)
    out.to_csv(KELUAR / f'common_unique_{th}.csv', index=False)
    print(f'baris common_unique: {len(out)} | N ujian ENTRY (signal x subset x keluarga, '
          f'populasi a, kumpulan A) = '
          f'{len(out[(out.populasi=="a")&(out.kumpulan_data=="A")])}')

    # corong: keputusan utama = S2, populasi a, kumpulan A, keluarga PADU
    ut = out[(out.subset == 'S2') & (out.populasi == 'a') & (out.kumpulan_data == 'A')
             & (out.keluarga == 'PADU')].copy()
    ut['lift_presisi_n'] = pd.to_numeric(ut.lift_presisi, errors='coerce')
    layak = ut[(ut.kelas.isin(['TERAS', 'UNIQUE', 'LANGKA']))
               | ((ut.lift_presisi_n >= 3) & (ut.n >= 30))]
    layak = layak.sort_values('lift_presisi_n', ascending=False).head(HAD_CORONG)
    (CACHE / f'corong_{th}.json').write_text(json.dumps(
        dict(had=HAD_CORONG, n_layak_sebelum_had=int(len(ut[(ut.kelas.isin(
            ['TERAS', 'UNIQUE', 'LANGKA'])) | ((ut.lift_presisi_n >= 3) & (ut.n >= 30))])),
            signal=layak.signal.tolist()), indent=1))
    print('kelas (S2, populasi a, kumpulan A, keluarga PADU):')
    print(ut.kelas.value_counts().to_string())
    print(f'corong: {len(layak)} signal diteruskan ke Step 7')
    for _, r in layak.head(12).iterrows():
        print(f"  {r.signal:38s} kelas {r.kelas:12s} lift {r.lift} "
              f"lift_presisi {r.lift_presisi} n {r.n}")
    # log ujian
    lg = out[(out.populasi == 'a') & (out.kumpulan_data == 'A')][
        ['subset', 'fasa', 'signal', 'keluarga', 'n', 'kelas']].copy()
    lg.insert(0, 'tarikh', '2026-10-27')
    lg = lg.rename(columns={'keluarga': 'jenis', 'kelas': 'keputusan'})
    lg['keterangan'] = 'STEP4 ENTRY'
    lg[['tarikh', 'fasa', 'subset', 'signal', 'jenis', 'n', 'keterangan', 'keputusan']].to_csv(
        KELUAR / 'log_ujian.csv', mode='a', header=False, index=False)
    print(f'[{time.time()-t0:.0f}s] siap')


if __name__ == '__main__':
    main()
