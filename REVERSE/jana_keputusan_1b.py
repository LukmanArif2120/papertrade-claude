"""Nilai fasa 1b terhadap ambang yang dipradaftar (SPEC_1B §3) dan jana KEPUTUSAN_1B.md.

Ambang: satu konfigurasi mesti mengalahkan asas fasa 1 DAN kawalan rawak bersaiz sama DAN SPY,
pada pulangan tahunan DAN MDD, dalam >= 4 daripada 6 tahun.

SPEC_1B §3 tidak menyatakan baris fasa 1 yang mana menjadi "asas". Dua bacaan dilaporkan supaya
pilihan itu tidak menentukan keputusan:
  (i) KETAT  — baris fasa 1 berpulangan tertinggi tahun itu
  (ii) MEDIAN — median pulangan dan median MDD semua baris signal fasa 1 tahun itu
Guna: python3 REVERSE/jana_keputusan_1b.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
R = AKAR / 'REVERSE'


def main():
    tahun = sorted(int(f.stem.split('_')[-1]) for f in R.glob('portfolio_1b_*.csv')
                   if f.stem.split('_')[-1].isdigit())
    if not tahun:
        print('tiada tahun 1b siap')
        return
    L, A = [], None
    L.append(f'# KEPUTUSAN FASA 1B — saiz dan henti berskala kemeruapan ({tahun[0]}–{tahun[-1]})\n')
    L.append('Dijana `REVERSE/jana_keputusan_1b.py`. Spec dikunci sebelum larian: `SPEC_1B.md`.\n')
    L.append('> Had diakui lebih awal (SPEC_1B §4): 1b menggunakan enam tahun yang **sama** '
             'seperti fasa 1 dan ideanya dipilih **selepas** melihat hasil fasa 1. Keputusan '
             'tertinggi 1b ialah **CALON**.\n')
    b1, bm, konf = {}, {}, None
    rows1b, bands = [], []
    for y in tahun:
        d1b = pd.read_csv(R / f'portfolio_1b_{y}.csv')
        p1 = pd.read_csv(R / f'portfolio_{y}.csv')
        sj = p1[~p1.sistem.str.startswith('KAWALAN_RAWAK')]
        b1[y] = dict(pul=float(sj.pulangan_tahun.max()),
                     mdd=float(sj.loc[sj.pulangan_tahun.idxmax(), 'mdd']),
                     sistem=sj.loc[sj.pulangan_tahun.idxmax(), 'sistem'])
        bm[y] = dict(pul=float(sj.pulangan_tahun.median()), mdd=float(sj.mdd.median()))
        kr = d1b[d1b.jenis == 'kawalan_rawak']
        spy = float(d1b.spy_pulangan_tahun.iloc[0])
        spy_mdd = float(d1b.spy_mdd.iloc[0])
        bands.append(dict(tahun=y, asas_ketat_sistem=b1[y]['sistem'],
                          asas_ketat_pul=round(b1[y]['pul'], 2),
                          asas_ketat_mdd=round(b1[y]['mdd'], 2),
                          asas_median_pul=round(bm[y]['pul'], 2),
                          asas_median_mdd=round(bm[y]['mdd'], 2),
                          rawak1b_pul=round(float(kr.pulangan_tahun.max()), 2),
                          rawak1b_mdd=round(float(kr.loc[kr.pulangan_tahun.idxmax(), 'mdd']), 2),
                          spy_pul=round(spy, 2), spy_mdd=round(spy_mdd, 2)))
        for _, r in d1b[d1b.jenis == ' 1b'.strip()].iterrows():
            rows1b.append(dict(tahun=y, sistem=r.sistem, pul=float(r.pulangan_tahun),
                               mdd=float(r.mdd), med=float(r.median_bulanan),
                               rawak_pul=float(kr.pulangan_tahun.max()),
                               rawak_mdd=float(kr.loc[kr.pulangan_tahun.idxmax(), 'mdd']),
                               spy_pul=spy, spy_mdd=spy_mdd))
    bd = pd.DataFrame(bands)
    L.append('\n## 1. Asas perbandingan setiap tahun\n')
    L.append(bd.to_markdown(index=False) + '\n')
    d = pd.DataFrame(rows1b)
    L.append('\n## 2. Keputusan ambang dipradaftar\n')
    hasil = []
    for bacaan, asas in (('KETAT', b1), ('MEDIAN', bm)):
        d2 = d.copy()
        d2['asas_pul'] = d2.tahun.map(lambda y: asas[y]['pul'])
        d2['asas_mdd'] = d2.tahun.map(lambda y: asas[y]['mdd'])
        d2['lulus'] = ((d2.pul > d2.asas_pul) & (d2.mdd > d2.asas_mdd)
                       & (d2.pul > d2.rawak_pul) & (d2.mdd > d2.rawak_mdd)
                       & (d2.pul > d2.spy_pul) & (d2.mdd > d2.spy_mdd))
        g = d2.groupby('sistem').lulus.sum().sort_values(ascending=False)
        n_terbaik = int(g.iloc[0]) if len(g) else 0
        lulus_amb = n_terbaik >= 4
        hasil.append((bacaan, n_terbaik, g.index[0] if len(g) else '-', lulus_amb))
        L.append(f'\n**Bacaan {bacaan}** — konfigurasi terbaik `{g.index[0] if len(g) else "-"}` '
                 f'mengalahkan ketiga-tiga asas dalam **{n_terbaik} daripada {len(tahun)}** tahun '
                 f'(perlu ≥ 4). → **{"LULUS" if lulus_amb else "GAGAL"}**\n')
        L.append('\n' + g.head(6).rename('tahun_lulus').reset_index().to_markdown(index=False)
                 + '\n')
    terima = any(h[3] for h in hasil)
    L.append(f'\n## 3. Keputusan 1b\n')
    L.append(f'**{"CALON" if terima else "DITOLAK"}** — ambang dipradaftar '
             f'{"dipenuhi" if terima else "TIDAK dipenuhi"} pada '
             f'{sum(1 for h in hasil if h[3])}/2 bacaan asas.\n')
    L.append('\n## 4. Kesan sebenar saiz berskala risiko (di luar ambang)\n')
    for y in tahun:
        d1b = pd.read_csv(R / f'portfolio_1b_{y}.csv')
        s = d1b[d1b.jenis == '1b']
        p1 = pd.read_csv(R / f'portfolio_{y}.csv')
        sj = p1[~p1.sistem.str.startswith('KAWALAN_RAWAK')]
        L.append(f'- **{y}**: MDD fasa 1 {sj.mdd.min():.1f}% … {sj.mdd.max():.1f}% → '
                 f'1b {s.mdd.min():.1f}% … {s.mdd.max():.1f}%; pulangan fasa 1 '
                 f'{sj.pulangan_tahun.min():.1f}% … {sj.pulangan_tahun.max():.1f}% → '
                 f'1b {s.pulangan_tahun.min():.1f}% … {s.pulangan_tahun.max():.1f}%; '
                 f'median bulanan 1b terbaik {s.median_bulanan.max():.2f}%\n')
    semua = pd.concat([pd.read_csv(R / f'portfolio_1b_{y}.csv').assign(tahun=y)
                       for y in tahun], ignore_index=True)
    s1b = semua[semua.jenis == '1b']
    L.append(f'\nMerentas {len(tahun)} tahun, {len(s1b)} konfigurasi-tahun 1b: purata pulangan '
             f'**{s1b.pulangan_tahun.mean():+.2f}%**, purata MDD **{s1b.mdd.mean():.2f}%**, '
             f'purata median bulanan **{s1b.median_bulanan.mean():+.2f}%**; '
             f'**{int((s1b.median_bulanan >= 10).sum())}** mencapai median ≥ +10% sebulan.\n')
    # Apa yang 1b BERJAYA buat, berbanding apa yang ia tidak buat
    p1_all = pd.concat([pd.read_csv(R / f'portfolio_{y}.csv').assign(tahun=y) for y in tahun],
                       ignore_index=True)
    sj_all = p1_all[~p1_all.sistem.str.startswith('KAWALAN_RAWAK')]
    mdd_terbaik_1b = s1b.groupby('tahun').mdd.max()
    mdd_terbaik_p1 = sj_all.groupby('tahun').mdd.max()
    lebih_baik = int((mdd_terbaik_1b > mdd_terbaik_p1).sum())
    L.append('\n## 5. Apa yang 1b berjaya buat, dan apa yang tidak\n')
    L.append(f'**Berjaya: kawalan risiko.** MDD terbaik setiap tahun bertambah baik dalam '
             f'**{lebih_baik} daripada {len(tahun)}** tahun. Contoh paling jelas: '
             + '; '.join(f'{y} {mdd_terbaik_p1[y]:.1f}% → {mdd_terbaik_1b[y]:.1f}%'
                         for y in tahun) + '. Menyamakan risiko setiap dagangan memang '
             'mengecilkan drawdown seperti yang dijangka — purata MDD jatuh daripada '
             f'{sj_all.mdd.mean():.2f}% (fasa 1) ke {s1b.mdd.mean():.2f}% (1b).\n')
    L.append(f'\n**Tidak berjaya: pulangan.** Purata pulangan tahunan '
             f'{sj_all.pulangan_tahun.mean():+.2f}% (fasa 1) → '
             f'{s1b.pulangan_tahun.mean():+.2f}% (1b), dan median bulanan '
             f'{sj_all.median_bulanan.mean():+.2f}% → {s1b.median_bulanan.mean():+.2f}%. '
             f'{int((s1b.median_bulanan >= 10).sum())} daripada {len(s1b)} konfigurasi-tahun '
             f'mencapai sasaran +10% sebulan.\n')
    L.append('\n**Maknanya.** Saiz berskala risiko membetulkan **drawdown**, bukan **alpha**. '
             'Ia mengurangkan kerugian apabila signal salah, tetapi ia tidak boleh mencipta '
             'kelebihan yang tidak ada. Digabung dengan diagnosis fasa 1 — jangkaan setiap '
             'dagangan yang diperlukan 2–5 kali apa yang pernah diukur, dan korelasi pangkat '
             'terhadap pulangan boleh didagangkan ≈ 0 — ini mengukuhkan kesimpulan fasa 1 dan '
             'tidak melemahkannya: **tiada alpha untuk dipungut daripada indikator harga sahaja '
             'dalam reka bentuk ini.** Kawalan risiko yang lebih baik ialah penambahbaikan yang '
             'sah dan berguna, tetapi ia bukan jalan ke +10% sebulan.\n')
    (R / 'KEPUTUSAN_1B.md').write_text('\n'.join(L))
    print('\n'.join(L[-6:]))
    print(f'\nKEPUTUSAN_1B.md siap | tahun {tahun} | keputusan '
          f'{"CALON" if terima else "DITOLAK"}')


if __name__ == '__main__':
    main()
