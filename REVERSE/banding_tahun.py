"""Perbandingan merentas tahun (aliran kerja langkah 5).

Signal ENTRY / HOLD / EXIT yang KEKAL konsisten lawan yang hanya berkesan pada tahun tertentu;
status gate 8.1 (naik taraf CALON -> DITERIMA perlu kelas sama dalam >= 2 tahun LAIN);
Step 7b dan Step 9 merentas tahun.

Guna: python3 REVERSE/banding_tahun.py
Output: REVERSE/BANDING_TAHUN.md, REVERSE/banding_tahun.csv
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
R = AKAR / 'REVERSE'
CACHE = R / '.cache'
BAIK = ('TERAS', 'UNIQUE', 'LANGKA')


def md(d, kols=None, n=None):
    d = d[kols] if kols else d
    if n:
        d = d.head(n)
    if not len(d):
        return '_(tiada baris)_\n'
    o = ['| ' + ' | '.join(str(c) for c in d.columns) + ' |',
         '|' + '|'.join('---' for _ in d.columns) + '|']
    for _, r in d.iterrows():
        o.append('| ' + ' | '.join('' if pd.isna(v) else str(v) for v in r) + ' |')
    return '\n'.join(o) + '\n'


def main():
    tahun = sorted(int(f.stem.split('_')[-1]) for f in R.glob('keputusan_*.csv')
                   if f.stem.split('_')[-1].isdigit())
    if len(tahun) < 2:
        print(f'Perlu >= 2 tahun siap; ada: {tahun}')
        return
    runs, cu, kp, pf, hh, fdr, hadb, koh, he = {}, {}, {}, {}, {}, {}, {}, {}, {}
    for y in tahun:
        runs[y] = pd.read_csv(R / f'runs_{y}.csv')
        d = pd.read_csv(R / f'common_unique_{y}.csv')
        cu[y] = d[(d.subset == 'S2') & (d.populasi == 'a') & (d.kumpulan_data == 'A')
                  & (d.keluarga == 'PADU')].set_index('signal')
        kp[y] = pd.read_csv(R / f'keputusan_{y}.csv').set_index('signal')
        pf[y] = pd.read_csv(R / f'portfolio_{y}.csv')
        hh[y] = pd.read_csv(R / f'hadapan_hold_exit_{y}.csv')
        fdr[y] = json.loads((CACHE / f'fdr_{y}.json').read_text())
        hadb[y] = json.loads((CACHE / f'had_bersyarat_{y}.json').read_text())
        koh[y] = pd.read_csv(R / f'kohort_masih_naik_{y}.csv')
        he[y] = pd.read_csv(R / f'hold_exit_{y}.csv')
    L = []
    A = L.append
    A(f'# BANDING MERENTAS TAHUN — REVERSE ({", ".join(str(y) for y in tahun)})\n')
    A('Dijana `REVERSE/banding_tahun.py`. Kod dan parameter **sama tanpa ubah** bagi setiap tahun; '
      'universe ikut bulan tahun berkenaan. Spec: `REVERSE/SPEC.md`.\n')
    A('> **KAVEAT.** Tiada saham delist (survivorship) dalam mana-mana tahun. Gate 8.1 memerlukan '
      f'kelas yang sama dalam **≥ 2 tahun LAIN**; dengan {len(tahun)} tahun siap, setiap tahun '
      f'hanya mempunyai {len(tahun) - 1} tahun lain, jadi **tiada signal boleh dinaik taraf ke '
      'DITERIMA**. Had kekal CALON.\n')

    A('## 1. Run dan peristiwa\n')
    rows = []
    for y in tahun:
        r = runs[y]
        rows.append(dict(tahun=y, n_run=len(r),
                         n_super=int((r.kumpulan == 'SUPER PADU').sum()),
                         n_padu=int((r.kumpulan == 'PADU').sum()),
                         n_biasa=int((r.kumpulan == 'BIASA').sum()),
                         pct_bertangga=round((r.jenis_kenaikan == 'BERTANGGA').mean() * 100, 1),
                         pct_lonjakan=round((r.jenis_kenaikan == 'LONJAKAN').mean() * 100, 1),
                         pct_stabil=round((r.jenis_kenaikan == 'STABIL').mean() * 100, 1),
                         pct_entry_sah=round((r.entry_sah == 'ya').mean() * 100, 1),
                         pct_graf_menaik=round((r.graf_menaik == 'ya').mean() * 100, 1),
                         n_masih_naik=int((r.masih_naik == 'ya').sum()),
                         median_naik=round(r.pct_naik_rendah.median(), 1),
                         n_peristiwa_sah=hadb[y]['n_peristiwa_sah'],
                         n_padu_s2_keputusan=hadb[y]['n_padu_s2_keputusan'],
                         had_bersyarat='AKTIF' if hadb[y]['had_aktif'] else 'tidak'))
    A(md(pd.DataFrame(rows)))

    A('\n## 2. Kohort "naik dan naik" (Step 2b)\n')
    rows = []
    for y in tahun:
        k = koh[y]
        rows.append(dict(tahun=y, n_kohort=len(k),
                         pct_melebihi_100=round((k.pct_naik_penuh >= 100).mean() * 100, 1),
                         median_naik_penuh=round(k.pct_naik_penuh.median(), 1),
                         median_naik_hari63=round(k.pct_naik_rendah_63.median(), 1),
                         median_hari_chandelier=round(pd.to_numeric(
                             k.chandelier_hari, errors='coerce').median(), 0),
                         median_pul_chandelier=round(pd.to_numeric(
                             k.chandelier_pul, errors='coerce').median(), 1),
                         pct_terpotong=round((k.terpotong_data == 'ya').mean() * 100, 1)))
    A(md(pd.DataFrame(rows)))
    A('\nKohort ini lebih kuat pada 2025 daripada 2024, tetapi arahnya sama pada kedua-dua tahun: '
      'run yang masih naik pada hari ke-63 pergi jauh lebih tinggi daripada yang reda.\n')

    A('\n## 3. Signal ENTRY — kekal konsisten lawan tahun tertentu\n')
    semua_sig = sorted(set().union(*[set(cu[y].index) for y in tahun]))
    rows = []
    for nm in semua_sig:
        rec = dict(signal=nm)
        kelas, lifts, lp, ns = [], [], [], []
        for y in tahun:
            k = cu[y].kelas.get(nm, '-')
            rec[f'kelas_{y}'] = k
            rec[f'lift_{y}'] = cu[y].lift.get(nm, '')
            rec[f'lift_presisi_{y}'] = cu[y].lift_presisi.get(nm, '')
            rec[f'n_{y}'] = cu[y].n.get(nm, '')
            rec[f'keputusan_{y}'] = kp[y].keputusan.get(nm, '-')
            kelas.append(k)
            ns.append(cu[y].n.get(nm, 0))
        n_baik = sum(1 for k in kelas if k in BAIK)
        rec['n_tahun_kelas_baik'] = n_baik
        rec['kelas_sama_semua_tahun'] = 'ya' if len(set(kelas)) == 1 and kelas[0] != '-' else 'tidak'
        rec['status'] = ('KEKAL' if n_baik == len(tahun)
                         else ('SEBAHAGIAN' if n_baik >= 1 else 'TIDAK PERNAH'))
        rec['n_tahun_calon'] = sum(1 for y in tahun if kp[y].keputusan.get(nm, '-') == 'CALON')
        rows.append(rec)
    bt = pd.DataFrame(rows)
    bt.to_csv(R / 'banding_tahun.csv', index=False)
    kekal = bt[bt.status == 'KEKAL'].sort_values('n_tahun_calon', ascending=False)
    A(f'\n### KEKAL — kelas TERAS/UNIQUE/LANGKA dalam **semua** {len(tahun)} tahun '
      f'({len(kekal)} signal)\n')
    A(md(kekal, ['signal'] + [c for y in tahun for c in (f'kelas_{y}', f'lift_{y}',
                                                         f'lift_presisi_{y}', f'n_{y}',
                                                         f'keputusan_{y}')]))
    seb = bt[(bt.status == 'SEBAHAGIAN') & (bt.n_tahun_kelas_baik >= 1)]
    A(f'\n### TAHUN TERTENTU — kelas baik dalam sebahagian tahun sahaja ({len(seb)} signal)\n')
    A(md(seb.sort_values('n_tahun_kelas_baik', ascending=False),
         ['signal'] + [c for y in tahun for c in (f'kelas_{y}', f'lift_{y}', f'keputusan_{y}')],
         25))
    calon_semua = bt[bt.n_tahun_calon == len(tahun)]
    A(f'\n### Signal berstatus CALON dalam SEMUA tahun ({len(calon_semua)})\n')
    A(md(calon_semua, ['signal'] + [f'keputusan_{y}' for y in tahun]
         + [f'lift_presisi_{y}' for y in tahun]))
    A('\nInilah satu-satunya senarai yang layak diteruskan ke tahun berikutnya. Gate 8.1 '
      f'memerlukan ≥ 2 tahun LAIN; selepas satu tahun lagi (2023) senarai ini boleh dinaik taraf '
      'ke DITERIMA jika kelasnya kekal.\n')

    A('\n## 4. HOLD, EXIT dan SISTEM merentas tahun\n')
    rows = []
    for y in tahun:
        f = fdr[y]
        rows.append(dict(tahun=y,
                         entry_padu=f'{f["ENTRY/PADU"]["lulus"]}/{f["ENTRY/PADU"]["n"]}',
                         entry_super=f'{f["ENTRY/SUPER PADU"]["lulus"]}/'
                                     f'{f["ENTRY/SUPER PADU"]["n"]}',
                         hold=f'{f["HOLD"]["lulus"]}/{f["HOLD"]["n"]}',
                         exit=f'{f["EXIT"]["lulus"]}/{f["EXIT"]["n"]}',
                         sistem=f'{f["SISTEM"]["lulus"]}/{f["SISTEM"]["n"]}'))
    A(md(pd.DataFrame(rows)))
    A('\nLulus BH-FDR q ≤ 0.01. **Keluarga EXIT dan SISTEM kosong pada setiap tahun.**\n')
    A('\n### Kelas pullback (Step 5) — stabil merentas tahun\n')
    rows = []
    for y in tahun:
        d = he[y][he[y].jenis == 'kelas_pullback'].set_index('nama')
        rec = dict(tahun=y)
        for kls in ('PULLBACK SIHAT', 'PULLBACK PASARAN', 'AMARAN'):
            rec[kls] = d.pct_sambung_puncak_baru.get(kls, np.nan)
            rec[f'n_{kls}'] = d.n.get(kls, np.nan)
        rows.append(rec)
    A(md(pd.DataFrame(rows)))
    A('\nPerbezaan SIHAT/PASARAN lawan AMARAN kekal besar pada kedua-dua tahun. Ini hasil HOLD '
      'yang paling boleh dipercayai dalam kajian ini.\n')
    A('\n### HOLD yang lulus FDR dalam semua tahun\n')
    sh = [set(fdr[y]['HOLD']['signal']) for y in tahun]
    kekal_h = sorted(set.intersection(*sh)) if sh else []
    A(f'{len(kekal_h)} signal: {", ".join("`"+s+"`" for s in kekal_h) if kekal_h else "tiada"}\n')

    A('\n## 5. Step 7b — tiga rujukan wajib merentas tahun\n')
    rows = []
    for y in tahun:
        d = hh[y][hh[y].sistem.str.startswith('REF_')].set_index('sistem')
        l7b = json.loads((CACHE / f'lulus7b_{y}.json').read_text())
        rec = dict(tahun=y)
        for s_ in ('REF_pegang_252', 'REF_chandelier_4atr', 'REF_jual_hari63'):
            rec[f'{s_}_jangkaan'] = d.jangkaan.get(s_, np.nan)
            rec[f'{s_}_median'] = d.median_pulangan.get(s_, np.nan)
        rec['rujukan_menang'] = max(
            ('REF_pegang_252', 'REF_chandelier_4atr', 'REF_jual_hari63'),
            key=lambda k: float(d.jangkaan.get(k, -1e9)))
        rec['n_sistem_mengalahkan_semua'] = len(l7b['sistem'])
        rows.append(rec)
    A(md(pd.DataFrame(rows)))
    A('\n**Rujukan (c) "pegang tanpa jual" menang pada kedua-dua tahun, dan 0/234 sistem '
      'mengalahkan ketiga-tiga rujukan pada kedua-dua tahun.** Tetapi perhatikan medianya: '
      'positif pada 2025, negatif pada 2024 — jangkaan positif itu dipacu hujung kanan taburan, '
      'bukan dagangan biasa.\n')

    A('\n## 6. Step 9 — prestasi portfolio merentas tahun\n')
    pfa = pd.concat([pf[y].assign(tahun=y) for y in tahun], ignore_index=True)
    A(md(pfa, ['tahun', 'sistem', 'n_posisi_dibuka', 'n_dagangan_ditutup', 'purata_slot_terisi',
               'pulangan_tahun', 'median_bulanan', 'pct_bulan_ge10', 'pct_bulan_positif',
               'bulan_terburuk', 'mdd', 'pusing_ganti_bulanan', 'spy_pulangan_tahun', 'spy_mdd']))
    A('\n### Sasaran +10% sebulan (median) merentas tahun\n')
    capai = pfa[pfa.median_bulanan >= 10]
    A(f'**{len(capai)} daripada {len(pfa)} kombinasi (sistem × tahun) mencapai median +10% '
      f'sebulan.**\n')
    for y in tahun:
        d = pf[y]
        b = d.loc[d.median_bulanan.idxmax()]
        A(f'- {y}: terbaik `{b.sistem}` median bulanan **{b.median_bulanan:.2f}%**, '
          f'MDD {b.mdd:.2f}%, {int(b.n_posisi_dibuka)} posisi dibuka '
          f'(SPY {b.spy_pulangan_tahun:.2f}%)\n')

    A('\n## 7. Kesimpulan merentas tahun\n')
    A(f'1. **Kelas kekal, keputusan tidak.** {len(kekal)} signal mengekalkan kelas '
      f'TERAS/UNIQUE/LANGKA pada kedua-dua tahun — kesemuanya konteks pengembangan kemeruapan '
      f'(ATR%, julat 20 hari, lebar Bollinger pada kuintil tertinggi): '
      f'{", ".join("`"+x+"`" for x in kekal.signal)}. **Tetapi {len(calon_semua)} berstatus CALON '
      f'dalam kedua-dua tahun.** Kelas Step 4 (lift atas populasi peristiwa) terus konsisten; '
      f'gate yang keras (G4 bootstrap, G5 outlier) tidak. Itulah jurang yang paling penting dalam '
      f'perbandingan ini: kekonsistenan lift **bukan** kekonsistenan kelebihan dagangan.\n')
    A('2. **Konsisten:** tiada pemicu klasik tunggal lulus pada mana-mana tahun. Hipotesis '
      '"magnitud ada pada konteks, bukan pemicu" disokong dua kali.\n')
    A('3. **Konsisten:** keluarga EXIT dan SISTEM kosong pada FDR kedua-dua tahun; rujukan '
      '"jangan jual" menang kedua-dua tahun.\n')
    A('4. **Konsisten:** kelas pullback (trend saham utuh lawan rosak) membezakan sambungan ke '
      'puncak baru dengan margin besar kedua-dua tahun.\n')
    A('5. **Tidak konsisten:** magnitud mutlak. Median pulangan rujukan pegang-252 +10.1% (2025) '
      'lawan −2.0% (2024); kohort masih_naik 39.8% melebihi +100% (2025) lawan 22.7% (2024). '
      'Tahun berbeza = rejim berbeza; angka 2025 bukan jangkaan.\n')
    A('6. **Paling penting untuk keputusan dagangan: portfolio berasaskan signal kalah kepada '
      'entri rawak pada KEDUA-DUA tahun.**\n')
    for y in tahun:
        d = pf[y]
        kr = d[d.sistem.str.startswith('KAWALAN_RAWAK')]
        sj = d[~d.sistem.str.startswith('KAWALAN_RAWAK')]
        spy_r = float(d.spy_pulangan_tahun.iloc[0])
        k_spy = int((sj.pulangan_tahun < spy_r).sum())
        k_rwk = int((sj.pulangan_tahun < kr.pulangan_tahun.max()).sum())
        lebih = sj[sj.pulangan_tahun >= kr.pulangan_tahun.max()]
        nota = ''
        if len(lebih):
            b = lebih.loc[lebih.pulangan_tahun.idxmax()]
            nota = (f' Satu-satunya yang mengalahkan rawak ialah `{b.sistem}` '
                    f'({b.pulangan_tahun:.2f}%) dengan hanya {int(b.n_posisi_dibuka)} posisi '
                    f'dibuka — saiz sampel yang tidak boleh dijadikan asas keputusan.')
        A(f'   - {y}: SPY {spy_r:+.2f}%, rawak terbaik {kr.pulangan_tahun.max():+.2f}%; '
          f'**{k_spy}/{len(sj)}** sistem kalah kepada SPY dan **{k_rwk}/{len(sj)}** kalah kepada '
          f'entri rawak.{nota}\n')
    A('   Tiada bukti kelebihan yang boleh diulang. Portfolio 8 slot bermakna setiap angka '
      'tahunan bergantung pada bilangan posisi yang kecil.\n')
    A('7. **Had kekal CALON.** Gate 8.1 memerlukan kelas sama dalam ≥ 2 tahun lain. Dengan dua '
      'tahun siap, setiap tahun hanya mempunyai satu tahun lain. Perlu sekurang-kurangnya satu '
      'tahun lagi (2023) sebelum sebarang signal boleh dilabel DITERIMA — dan atas bukti 2024, '
      'tahun tambahan lebih berkemungkinan menolak daripada menerima.\n')
    (R / 'BANDING_TAHUN.md').write_text('\n'.join(L))
    print(f'BANDING_TAHUN.md siap | tahun {tahun} | KEKAL {len(kekal)} | '
          f'CALON semua tahun {len(calon_semua)}')
    print(md(kekal, ['signal'] + [f'kelas_{y}' for y in tahun]
             + [f'keputusan_{y}' for y in tahun]))


if __name__ == '__main__':
    main()
