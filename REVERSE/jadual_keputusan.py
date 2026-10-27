"""Jadual keputusan ringkas merentas semua tahun yang siap.

Satu baris setiap tahun: saiz run, HAD BERSYARAT, keputusan ENTRY, FDR setiap keluarga, keputusan
Step 7b (termasuk bilangan sistem berjangkaan POSITIF, bukan hanya yang mengalahkan rujukan), dan
prestasi portfolio Step 9 berbanding SPY dan KAWALAN RAWAK.

Guna: python3 REVERSE/jadual_keputusan.py
Output: REVERSE/JADUAL_KEPUTUSAN.csv
"""
import json
import sys
from pathlib import Path

import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
R = AKAR / 'REVERSE'
C = R / '.cache'


def main():
    tahun = sorted(int(f.stem.split('_')[-1]) for f in R.glob('keputusan_*.csv')
                   if f.stem.split('_')[-1].isdigit())
    if not tahun:
        print('tiada tahun siap')
        return
    rows = []
    for y in tahun:
        k = pd.read_csv(R / f'keputusan_{y}.csv')
        f = json.loads((C / f'fdr_{y}.json').read_text())
        l = json.loads((C / f'lulus7b_{y}.json').read_text())
        hb = json.loads((C / f'had_bersyarat_{y}.json').read_text())
        ks = json.loads((C / f'kesediaan_{y}.json').read_text())
        runs = pd.read_csv(R / f'runs_{y}.csv')
        koh = pd.read_csv(R / f'kohort_masih_naik_{y}.csv')
        pf = pd.read_csv(R / f'portfolio_{y}.csv')
        hh = pd.read_csv(R / f'hadapan_hold_exit_{y}.csv')
        h = hh[~hh.sistem.str.startswith('REF_')].copy()
        h['j'] = pd.to_numeric(h.jangkaan, errors='coerce')
        kr = pf[pf.sistem.str.startswith('KAWALAN_RAWAK')]
        sj = pf[~pf.sistem.str.startswith('KAWALAN_RAWAK')]
        spy = float(pf.spy_pulangan_tahun.iloc[0])
        rows.append(dict(
            tahun=y, n_ticker_universe=ks['n_ticker_universe'], n_run=len(runs),
            pct_entry_sah=round((runs.entry_sah == 'ya').mean() * 100, 1),
            n_bertangga=int((runs.jenis_kenaikan == 'BERTANGGA').sum()),
            n_peristiwa_sah=hb['n_peristiwa_sah'],
            n_padu_s2_keputusan=hb['n_padu_s2_keputusan'],
            had_bersyarat='AKTIF' if hb['had_aktif'] else '-',
            pct_kohort_melebihi_100=round((koh.pct_naik_penuh >= 100).mean() * 100, 1),
            n_corong=len(k), diterima=int((k.keputusan == 'DITERIMA').sum()),
            calon=int((k.keputusan == 'CALON').sum()),
            ditolak=int((k.keputusan == 'DITOLAK').sum()),
            fdr_entry=f'{f["ENTRY/PADU"]["lulus"]}/{f["ENTRY/PADU"]["n"]}',
            fdr_hold=f'{f["HOLD"]["lulus"]}/{f["HOLD"]["n"]}',
            fdr_exit=f'{f["EXIT"]["lulus"]}/{f["EXIT"]["n"]}',
            fdr_sistem=f'{f["SISTEM"]["lulus"]}/{f["SISTEM"]["n"]}',
            rujukan_7b_menang=max(l['rujukan'], key=lambda x: l['rujukan'][x]).replace('REF_', ''),
            ambang_jangkaan_rujukan=round(l['ambang'], 2),
            n_sistem_mengalahkan_3_rujukan=len(l['sistem']),
            n_sistem_jangkaan_positif=int((h.j > 0).sum()), n_sistem=len(h),
            spy_pulangan=round(spy, 1),
            rawak_terbaik=round(float(kr.pulangan_tahun.max()), 1),
            sistem_signal_terbaik=round(float(sj.pulangan_tahun.max()), 1),
            kalah_kepada_spy=f'{int((sj.pulangan_tahun < spy).sum())}/{len(sj)}',
            kalah_kepada_rawak=f'{int((sj.pulangan_tahun < kr.pulangan_tahun.max()).sum())}'
                               f'/{len(sj)}',
            n_sistem_median_bulanan_ge10=int((pf.median_bulanan >= 10).sum()),
            asas_entry_step9=pf.asas_entry.iloc[0] if 'asas_entry' in pf.columns else '',
        ))
    d = pd.DataFrame(rows)
    d.to_csv(R / 'JADUAL_KEPUTUSAN.csv', index=False)
    pd.set_option('display.width', 250)
    print(d.drop(columns=['asas_entry_step9']).to_string(index=False))
    print(f'\nJADUAL_KEPUTUSAN.csv: {len(d)} tahun')


if __name__ == '__main__':
    main()
