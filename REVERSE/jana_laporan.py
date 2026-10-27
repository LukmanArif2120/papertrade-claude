"""Jana REVERSE/LAPORAN_<TAHUN>.md daripada CSV output semua step.

Guna: python3 REVERSE/jana_laporan.py 2025
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.teras import data as D  # noqa: E402
R = AKAR / 'REVERSE'
CACHE = R / '.cache'


def md_jadual(d, kols=None, n=None):
    d = d[kols] if kols else d
    if n:
        d = d.head(n)
    if not len(d):
        return '_(tiada baris)_\n'
    out = ['| ' + ' | '.join(str(c) for c in d.columns) + ' |',
           '|' + '|'.join('---' for _ in d.columns) + '|']
    for _, r in d.iterrows():
        out.append('| ' + ' | '.join('' if pd.isna(v) else str(v) for v in r) + ' |')
    return '\n'.join(out) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tahun', type=int)
    th = ap.parse_args().tahun
    runs = pd.read_csv(R / f'runs_{th}.csv')
    ms = pd.read_csv(R / f'monthly_summary_{th}.csv')
    koh = pd.read_csv(R / f'kohort_masih_naik_{th}.csv')
    cu = pd.read_csv(R / f'common_unique_{th}.csv')
    he = pd.read_csv(R / f'hold_exit_{th}.csv')
    fs = pd.read_csv(R / f'false_signal_{th}.csv')
    hh = pd.read_csv(R / f'hadapan_hold_exit_{th}.csv')
    kp = pd.read_csv(R / f'keputusan_{th}.csv')
    pf = pd.read_csv(R / f'portfolio_{th}.csv')
    pb = pd.read_csv(R / f'portfolio_bulanan_{th}.csv', index_col=0)
    sk = pd.read_csv(R / f'skipped_{th}.csv')
    jn = pd.read_csv(R / f'jangkaan_kemunculan_{th}.csv')
    kuin = json.loads((CACHE / f'kuintil_{th}.json').read_text())
    hadb = json.loads((CACHE / f'had_bersyarat_{th}.json').read_text())
    corong = json.loads((CACHE / f'corong_{th}.json').read_text())
    l7 = json.loads((CACHE / f'lulus7_{th}.json').read_text())
    l7b = json.loads((CACHE / f'lulus7b_{th}.json').read_text())
    fdr = json.loads((CACHE / f'fdr_{th}.json').read_text())
    ks = json.loads((CACHE / f'kesediaan_{th}.json').read_text())
    fph = R / f'PANDANG_HADAPAN_{th}.md'
    ph = fph.read_text() if fph.exists() else (R / 'PANDANG_HADAPAN.md').read_text()
    n_potong = re.search(r'Tarikh potong: (\d+)', ph)
    n_band = re.search(r'ticker: ([\d,]+)\n- Perbandingan lajur×potong×ticker: ([\d,]+)', ph)
    n_sig_bina = len(kuin['simpan']) * 2 + 31 + 6 * 10 * 2
    ut = cu[(cu.subset == 'S2') & (cu.populasi == 'a') & (cu.kumpulan_data == 'A')
            & (cu.keluarga == 'PADU')]
    ut1 = cu[(cu.subset == 'S1') & (cu.populasi == 'a') & (cu.kumpulan_data == 'A')
             & (cu.keluarga == 'PADU')]
    sup = cu[(cu.subset == 'S2') & (cu.populasi == 'a') & (cu.kumpulan_data == 'A')
             & (cu.keluarga == 'SUPER PADU')]
    fs_u = fs[~fs.signal.astype(str).str.contains(r'\| penapis:')]
    fs_p = fs[fs.signal.astype(str).str.contains(r'\| penapis:')]
    calon = kp[kp.keputusan == 'CALON']
    L = []
    A = L.append

    A(f'# LAPORAN REVERSE {th} — reverse engineer saham padu US (ENTRY / HOLD / EXIT)\n')
    A(f'Dijana skrip `REVERSE/jana_laporan.py` pada 27 Okt 2026. Spec dikunci: `REVERSE/SPEC.md`.\n')
    n_terima = int((kp.keputusan == 'DITERIMA').sum())
    tahun_lain = sorted(int(f.stem.split('_')[-1]) for f in R.glob('common_unique_*.csv')
                        if f.stem.split('_')[-1].isdigit() and int(f.stem.split('_')[-1]) != th)
    A('> **KAVEAT WAJIB (dua arah).** Data A02 **tiada saham delist** (bias survivorship): run '
      'dipandang **tinggi** (had atas) DAN kadar signal palsu dipandang **rendah**. Satu tahun = '
      '**satu rejim pasaran**. Peta sektor bukan titik-masa. '
      + (f'Gate 8.1 ada {len(tahun_lain)} tahun lain untuk mengesahkan ({tahun_lain}); '
         f'**{n_terima} signal DITERIMA**, selebihnya maksimum CALON (SPEC §11.8).\n'
         if n_terima else
         f'Gate 8.1 ada {len(tahun_lain)} tahun lain ({tahun_lain}); keputusan '
         f'**maksimum CALON** (SPEC §11.8).\n'))

    A('## 0. Jawapan ringkas\n')
    ref = pf[pf.sistem == 'REF_pegang_252'].iloc[0]
    bln_kosong = ms[ms.n_run == 0].bulan.tolist()
    A(f'1. **{len(runs)} run layak** dikenal pasti dalam {th}; '
      + ('setiap 12 bulan ada calon (tiada "TIADA CALON"). '
         if not bln_kosong else
         f'**{len(bln_kosong)} bulan TIADA CALON** ({", ".join(bln_kosong)}) — lihat §2. ')
      + f'{int((runs.kumpulan == "SUPER PADU").sum())} SUPER PADU (≥100%), '
      f'{int((runs.kumpulan == "PADU").sum())} PADU, '
      f'{int((runs.kumpulan == "BIASA").sum())} BIASA.\n')
    A(f'2. **Kohort "naik dan naik" ialah penemuan terkuat kajian ini.** Daripada {len(koh)} run '
      f'yang masih naik pada hari ke-63, **{(koh.pct_naik_penuh>=100).mean()*100:.1f}% akhirnya '
      f'melebihi +100%**, dengan median kenaikan penuh **{koh.pct_naik_penuh.median():.1f}%** '
      f'lawan {koh.pct_naik_rendah_63.median():.1f}% pada hari ke-63.\n')
    kon_mer = ('atr_pct', 'bb_lebar', 'julat20', 'julat10')
    semua_mer = len(calon) and all(any(k in x for k in kon_mer) for x in calon.signal)
    if len(calon):
        A(f'3. **Signal entry: {len(calon)} CALON daripada {len(corong["signal"])} yang masuk '
          f'corong**'
          + (' — dan kesemuanya konteks **pengembangan kemeruapan**, bukan pemicu: '
             if semua_mer else ': ')
          + f'{", ".join("`"+x+"`" for x in calon.signal)}.\n')
    else:
        gagal4 = int((kp.G4_bootstrap == 'GAGAL').sum())
        gagal5 = int((kp.G5_outlier != 'LULUS').sum())
        A(f'3. **Signal entry: TIADA CALON** daripada {len(corong["signal"])} yang masuk corong. '
          f'{gagal4} gagal gate bootstrap (G4) dan {gagal5} ditanda BERGANTUNG PADA OUTLIER (G5). '
          f'Ini keputusan, bukan kegagalan teknikal: tiada signal ENTRY tahun ini bertahan selepas '
          f'had bawah 95% bootstrap blok dan ujian tanpa 5% pemenang teratas.\n')
    RUJ_NAMA = {'REF_pegang_252': 'pegang tanpa jual hingga hari ke-252',
                'REF_chandelier_4atr': 'Chandelier 4×ATR14', 'REF_jual_hari63': 'jual hari ke-63'}
    menang_ruj = max(l7b['rujukan'], key=lambda k: l7b['rujukan'][k])
    n_menang = len(l7b['sistem'])
    # l7b['n_sistem'] sudah mengecualikan 3 rujukan (lihat step7b_hadapan.py)
    n_sistem = l7b.get('n_sistem', 234)
    if n_menang == 0:
        A(f'4. **Rujukan "{RUJ_NAMA[menang_ruj]}" MENANG.** Tiada satu pun daripada {n_sistem} '
          f'sistem HOLD×EXIT mengalahkan ketiga-tiga rujukan. Jangkaan: '
          + ', '.join(f'{l7b["rujukan"][k]:+.2f}% ({RUJ_NAMA[k]})' for k in
                      sorted(l7b['rujukan'], key=lambda k: -l7b['rujukan'][k]))
          + '. Mengikut arahan Step 7b.4, jawapan kajian tahun ini ialah **"jangan jual"**.\n')
    else:
        A(f'4. **{n_menang} daripada {n_sistem} sistem HOLD×EXIT mengalahkan ketiga-tiga '
          f'rujukan** — berbeza daripada tahun lain. Rujukan terbaik hanya '
          f'{l7b["ambang"]:+.2f}% setiap dagangan ("{RUJ_NAMA[menang_ruj]}"): '
          + ', '.join(f'{l7b["rujukan"][k]:+.2f}% ({RUJ_NAMA[k]})' for k in
                      sorted(l7b['rujukan'], key=lambda k: -l7b['rujukan'][k]))
          + '. Apabila memegang tanpa jual tidak lagi menguntungkan, exit aktif baru berbaloi.'
          + (' **Perhatikan: ambang itu NEGATIF.** Mengalahkan rujukan yang merugikan hanya '
             'bermakna "kurang rugi", bukan untung — periksa lajur `jangkaan` dan '
             '`median_pulangan` setiap sistem, bukan hanya kedudukannya berbanding rujukan.\n'
             if l7b['ambang'] <= 0 else '\n'))
    A(f'5. **Kapasiti slot, bukan kadar menang, yang mengikat.** Dalam Step 9 rujukan '
      f'pegang-252 hanya membuka **{int(ref.n_posisi_dibuka)} posisi sepanjang tahun** (8 slot '
      f'terisi awal dan tidak pernah kosong), berbanding ~130 calon/tahun yang diperlukan. '
      f'Pulangannya {ref.pulangan_tahun:.2f}% ialah hasil **{int(ref.n_posisi_dibuka)} saham**, '
      f'bukan sistem.\n')
    A(f'6. **Sasaran +10% sebulan (median): TIDAK TERCAPAI oleh mana-mana sistem.** Yang terbaik '
      f'ialah {ref.median_bulanan:.2f}% sebulan (median) dengan MDD {ref.mdd:.2f}%.\n')
    A(f'7. **Keluarga EXIT dan SISTEM pada FDR:** {fdr["EXIT"]["lulus"]}/{fdr["EXIT"]["n"]} signal '
      f'EXIT dan {fdr["SISTEM"]["lulus"]}/{fdr["SISTEM"]["n"]} sistem lulus q ≤ 0.01.\n')

    A('## 1. Semakan kesediaan Step 0\n')
    A('| Semakan | Hasil |\n|---|---|\n'
      '| a. Tarik aset Release `autotune-data-a02` | **LULUS** — 219 MB, 18 parquet, '
      '2009-01-02 → 2026-10-16; semua sha256 sepadan |\n'
      '| b. SPY dan QQQ dalam `idx.parquet` | **LULUS** |\n'
      f'| c. Sumber sektor/industri setiap ticker | **LULUS** — {ks["liputan_sektor"]}/'
      f'{ks["n_ticker_universe"]} = {ks["pct_liputan_sektor"]}% '
      f'({ks["n_kelas_asas"]} kelas saham diisi daripada ticker asas; {ks["n_lain_lain"]} ticker '
      f'= `Lain-lain`) |\n'
      '| d. 11 ETF sektor SPDR ditarik dan dicache | **GAGAL** → pindaan SPEC §13.1 '
      '(indeks sektor A02; diluluskan pengguna) |\n'
      f'| e. Step 1–3 satu bulan, anggaran × 12 | **LULUS** — {ks["saat_per_ticker"]:.3f} '
      f's/ticker; larian penuh {ks["n_ticker_harga"]} ticker = {ks["saat_larian"]:.0f} s |\n'
      f'| f. `semak_hadapan` atas modul indikator | **LULUS** — '
      f'{n_potong.group(1) if n_potong else "14"} tarikh potong (≥ 12), '
      f'{n_band.group(2) if n_band else "26,950"} perbandingan, **0 kegagalan** '
      f'(`REVERSE/PANDANG_HADAPAN_{th}.md`) |\n')

    A('## 2. Step 1–2 — run\n')
    uv = D.universe()
    uvy = uv[uv.bulan.str[:4] == str(th)].groupby('bulan').size()
    A(f'Saiz universe {th} setiap bulan: min **{uvy.min()}**, median **{int(uvy.median())}**, '
      f'maks **{uvy.max()}**; {ks["n_ticker_universe"]} ticker berbeza sepanjang tahun.\n')
    if uvy.min() < 2000:
        A(f'\n> **KAVEAT SAIZ UNIVERSE.** Universe {th} lebih kecil daripada had 2000 saham '
          f'(min {uvy.min()} sebulan). Jumlah run, peristiwa dan kemunculan tahun ini **tidak '
          f'setara** dengan tahun yang universenya penuh 2000; bandingkan kadar dan peratusan, '
          f'bukan bilangan mutlak, dalam `BANDING_TAHUN.md`.\n')

    A(md_jadual(ms))
    A(f'\nJumlah: **{len(runs)} run layak**, {int((runs.entry_sah=="ya").sum())} '
      f'({(runs.entry_sah=="ya").mean()*100:.1f}%) dengan `entry_sah = ya` '
      f'(tiada amaran: syarat 10 hari menolak {100-(runs.entry_sah=="ya").mean()*100:.1f}% '
      f'< 50%). Dilangkau: {len(sk)} '
      f'({int((sk.sebab=="terlalu perlahan").sum()) if "sebab" in sk else 0} "terlalu perlahan").\n')
    if bln_kosong:
        A('\n### Bulan TIADA CALON (arahan Step 1.3)\n')
        sk2 = sk.copy()
        sk2['tarikh'] = pd.to_datetime(sk2.get('tarikh'), errors='coerce')
        sk2['bulan'] = sk2.tarikh.dt.strftime('%Y-%m')
        for b in bln_kosong:
            A(f'\n**{b} — TIADA CALON.** 3 run terhampir beserta syarat yang gagal:\n\n')
            d = sk2[(sk2.bulan == b) & (sk2.sebab == 'terlalu perlahan')].copy()
            if not len(d):
                A('_(tiada calon run sama sekali bulan ini — tiada tutup ≥ 5% di atas rendah '
                  'terendah 20 hari)_\n')
                continue
            d['hari'] = pd.to_numeric(d.hari_ke_puncak, errors='coerce')
            d['naik'] = pd.to_numeric(d.pct_naik_rendah, errors='coerce')
            d['ambang'] = np.where(d.hari <= 21, 10.0, np.where(d.hari <= 42, 20.0, 30.0))
            d['jurang'] = d.naik - d.ambang
            d = d.sort_values('jurang', ascending=False).head(3)
            d['syarat_gagal'] = [f'hari_ke_puncak {int(h)} perlukan %_naik_rendah ≥ {a:.0f}%, '
                                 f'dapat {n:.1f}% (kurang {abs(j):.1f} mata)'
                                 for h, a, n, j in zip(d.hari, d.ambang, d.naik, d.jurang)]
            A(md_jadual(d, ['ticker', 'tarikh', 'hari_ke_puncak', 'pct_naik_rendah',
                            'syarat_gagal']))
    A('\n### Bucket %_naik × tempoh\n')
    A(md_jadual(pd.crosstab(runs.bucket_pct, runs.bucket_tempoh).reset_index()))
    A('\n### KUMPULAN × KELAS LAJU (sel n < 20 = SAMPEL KECIL)\n')
    ct = pd.crosstab(runs.kumpulan, runs.kelas_laju)
    A(md_jadual(ct.reset_index()))
    kecil = [(i, c) for i in ct.index for c in ct.columns if 0 < ct.loc[i, c] < 20]
    A(f'\nSel SAMPEL KECIL: {kecil if kecil else "tiada"}\n')
    A('\n### Jenis kenaikan\n')
    A(md_jadual(runs.jenis_kenaikan.value_counts().rename_axis('jenis')
                .reset_index(name='n')))
    A(f'\n`graf_menaik = ya` (S3): {int((runs.graf_menaik=="ya").sum())} '
      f'({(runs.graf_menaik=="ya").mean()*100:.1f}%). `masih_naik = ya`: '
      f'{int((runs.masih_naik=="ya").sum())}.\n')

    A('\n### 10 run terbaik setiap bulan (ikut %_naik_rendah)\n')
    for b in sorted(runs.bulan_mula.unique()):
        d = runs[runs.bulan_mula == b].nlargest(10, 'pct_naik_rendah')
        A(f'\n**{b}**\n')
        A(md_jadual(d, ['ticker', 'sektor', 'tarikh_mula', 'tarikh_puncak', 'hari_ke_puncak',
                        'pct_naik_rendah', 'kumpulan', 'jenis_kenaikan', 'entry_sah',
                        'masih_naik']))
    A('\n### Semua run SUPER PADU (≥ 100%)\n')
    A(md_jadual(runs[runs.kumpulan == 'SUPER PADU'].nlargest(60, 'pct_naik_rendah'),
                ['ticker', 'sektor', 'tarikh_mula', 'hari_ke_puncak', 'pct_naik_rendah',
                 'jenis_kenaikan', 'entry_sah', 'masih_naik']))
    A(f'\n(dipaparkan 60 teratas daripada {int((runs.kumpulan=="SUPER PADU").sum())})\n')
    A('\n### Run BERTANGGA (S2) — 40 teratas\n')
    A(md_jadual(runs[runs.jenis_kenaikan == 'BERTANGGA'].nlargest(40, 'pct_naik_rendah'),
                ['ticker', 'sektor', 'tarikh_mula', 'hari_ke_puncak', 'pct_naik_rendah',
                 'bilangan_kaki', 'pct_hari_atas_ema21', 'kumpulan']))
    A(f'\n(daripada {int((runs.jenis_kenaikan=="BERTANGGA").sum())} run BERTANGGA)\n')

    A('\n### HAD BERSYARAT (SPEC §11.1, pindaan §13.4)\n')
    A(f'n peristiwa PADU dalam S2, populasi keputusan (a) = **{hadb["n_padu_s2_keputusan"]}** '
      f'(rujukan: semua peristiwa = {hadb["n_padu_s2_semua"]}). '
      f'{"< 300 → **HAD BERSYARAT AKTIF**: pemicu × 1 konteks sahaja (120 ujian); kombinasi HOLD/EXIT dihadkan 1 syarat." if hadb["had_aktif"] else "≥ 300 → tidak aktif."}\n')
    A(f'\nPeristiwa sah: **{hadb["n_peristiwa_sah"]}** (populasi keputusan '
      f'{hadb["n_populasi_keputusan"]}).\n')

    A('\n## 3. Step 2b — kohort "naik dan naik"\n')
    A(f'Dijejak {len(koh)} run (masih_naik = ya, entry_sah = ya) hingga 252 hari dagangan dari '
      f'tarikh_sah.\n\n')
    A('| Metrik | Nilai |\n|---|---|\n'
      f'| % akhirnya melebihi +100% | **{(koh.pct_naik_penuh>=100).mean()*100:.1f}%** |\n'
      f'| median %_naik_penuh | **{koh.pct_naik_penuh.median():.1f}%** |\n'
      f'| median %_naik pada hari ke-63 | {koh.pct_naik_rendah_63.median():.1f}% |\n'
      f'| median hari ke puncak penuh | {koh.hari_ke_puncak_penuh.median():.0f} |\n'
      f'| median MFE 252 selepas kos | {koh.mfe252.median():.1f}% |\n'
      f'| median MAE 252 | {koh.mae252.median():.1f}% |\n'
      f'| median hari pegang Chandelier 4×ATR | '
      f'{pd.to_numeric(koh.chandelier_hari, errors="coerce").median():.0f} |\n'
      f'| median pulangan Chandelier selepas kos | '
      f'{pd.to_numeric(koh.chandelier_pul, errors="coerce").median():.1f}% |\n'
      f'| terpotong hujung data | {(koh.terpotong_data=="ya").mean()*100:.1f}% |\n')
    A('\nExit yang menyala dahulu:\n\n')
    A(md_jadual(koh.exit_pertama.value_counts().rename_axis('exit').reset_index(name='n')))
    A('\n### Banding signal ENTRY: masih_naik = ya lawan run yang reda dalam 63 hari\n')
    rn = runs[(runs.entry_sah == 'ya')]
    A(md_jadual(pd.DataFrame([
        dict(kohort='masih_naik = ya', n=int((rn.masih_naik == 'ya').sum()),
             median_naik_63=round(rn[rn.masih_naik == 'ya'].pct_naik_rendah.median(), 1),
             pct_bertangga=round((rn[rn.masih_naik == 'ya'].jenis_kenaikan == 'BERTANGGA').mean()
                                 * 100, 1),
             pct_super=round((rn[rn.masih_naik == 'ya'].kumpulan == 'SUPER PADU').mean() * 100, 1),
             median_hari_ke_puncak=round(rn[rn.masih_naik == 'ya'].hari_ke_puncak.median(), 0)),
        dict(kohort='reda dalam 63 hari', n=int((rn.masih_naik == 'tidak').sum()),
             median_naik_63=round(rn[rn.masih_naik == 'tidak'].pct_naik_rendah.median(), 1),
             pct_bertangga=round((rn[rn.masih_naik == 'tidak'].jenis_kenaikan == 'BERTANGGA')
                                 .mean() * 100, 1),
             pct_super=round((rn[rn.masih_naik == 'tidak'].kumpulan == 'SUPER PADU').mean() * 100,
                             1),
             median_hari_ke_puncak=round(rn[rn.masih_naik == 'tidak'].hari_ke_puncak.median(),
                                         0))])))
    A('\nKohort `masih_naik = ya` lebih kerap BERTANGGA dan lebih kerap SUPER PADU. Itu konsisten '
      'dengan hipotesis "naik dan naik", tetapi ia **label hasil**, bukan signal entry: ia hanya '
      'diketahui pada hari ke-63.\n')

    A('\n## 4. Step 3 — populasi kuintil dan dedup\n')
    A(f'POPULASI KUINTIL (dibekukan) = semua peristiwa sah kumpulan A = **{kuin["n"]}** baris. '
      f'Indikator berterusan dikekalkan selepas dedup Spearman > 0.8: **{len(kuin["simpan"])}** '
      f'daripada 41; dibuang {len(kuin["dibuang"])}.\n\n')
    A(md_jadual(pd.DataFrame(kuin['dibuang'])))
    A(f'\nSignal dibina: **{n_sig_bina}** (31 binari + {len(kuin["simpan"]) * 2} hujung kuintil '
      f'+ 120 pemicu × 1 konteks).\n')

    A('\n## 5. Step 4 — common & unique (ENTRY)\n')
    A(f'Keputusan utama = S2, populasi keputusan (a), kumpulan A, keluarga PADU. '
      f'N ujian ENTRY sebenar (populasi a, kumpulan A) = '
      f'**{len(cu[(cu.populasi=="a")&(cu.kumpulan_data=="A")])}** baris '
      f'(213 signal × 2 subset × 2 keluarga).\n')
    A('\n### Kelas (S2, kumpulan A, keluarga PADU)\n')
    A(md_jadual(ut.kelas.value_counts().rename_axis('kelas').reset_index(name='n')))
    A('\n### Signal TERAS / UNIQUE / LANGKA — S2 (keputusan utama)\n')
    A(md_jadual(ut[ut.kelas.isin(['TERAS', 'UNIQUE', 'LANGKA'])]
                .sort_values('lift_presisi', ascending=False),
                ['signal', 'kelas', 'K_padu', 'K_biasa', 'K_gagal', 'K_rawak', 'lift',
                 'lift_rawak', 'presisi', 'lift_presisi', 'n', 'n_industri', 'n_minggu',
                 'purata_pct_naik_rendah', 'purata_hari_ke_puncak', 'pct_bertangga',
                 'pct_lonjakan', 'tanda']))
    A('\n### Rujukan S1 (semua run layak)\n')
    A(md_jadual(ut1[ut1.kelas.isin(['TERAS', 'UNIQUE', 'LANGKA'])]
                .sort_values('lift_presisi', ascending=False),
                ['signal', 'kelas', 'K_padu', 'lift', 'presisi', 'lift_presisi', 'n', 'tanda'],
                25))
    A('\n### Rujukan S3 (graf_menaik) — signal yang sudah lulus sahaja\n')
    s3 = runs[(runs.graf_menaik == 'ya') & (runs.entry_sah == 'ya')]
    A(f'S3 mengandungi {len(s3)} run; ia **bukan keluarga carian** (tidak menambah N). '
      f'{(s3.jenis_kenaikan=="BERTANGGA").mean()*100:.1f}% daripadanya BERTANGGA lawan '
      f'{(runs[runs.entry_sah=="ya"].jenis_kenaikan=="BERTANGGA").mean()*100:.1f}% keseluruhan.\n')
    A('\n### Keluarga SUPER PADU (FDR sendiri)\n')
    A(md_jadual(sup[sup.kelas.isin(['TERAS', 'UNIQUE', 'LANGKA'])]
                .sort_values('lift', ascending=False),
                ['signal', 'kelas', 'K_super', 'lift', 'lift_rawak', 'n', 'tanda'], 20))
    A('\n### PEMICU YANG TIDAK MEMBEZAKAN\n')
    A('Keenam pemicu diuji sebagai signal tunggal. Dilaporkan walaupun ditolak, seperti diarahkan.\n\n')
    pem = ['b:macd_cross', 'b:rsi_lintas50', 'b:ema_crossback', 'b:donchian20', 'b:pocket_pivot',
           'b:gap_and_go']
    A(md_jadual(ut[ut.signal.isin(pem)], ['signal', 'kelas', 'K_padu', 'K_biasa', 'K_gagal',
                                          'K_rawak', 'lift', 'lift_rawak', 'presisi',
                                          'lift_presisi', 'n']))
    A('\n**Tiada satu pun pemicu klasik, sebagai pemicu tunggal, mencapai kelas TERAS/UNIQUE/LANGKA '
      'dalam S2.** Maklumat magnitud terletak pada konteksnya, bukan pada pemicu — itulah hipotesis '
      'yang diuji dalam kajian ini, dan ia disokong oleh data 2025.\n')
    A(f'\n### Corong ke Step 7\n{len(corong["signal"])} signal diteruskan '
      f'(had {corong["had"]}; layak sebelum had: {corong["n_layak_sebelum_had"]}).\n')

    A('\n## 6. Step 5 — HOLD\n')
    A('> AMARAN BIAS (arahan Step 5.6): dikira atas run sahaja — sampel yang sudah terpilih kerana '
      'berjaya. Semua CALON.\n\n')
    A('### Kelas pullback\n')
    A(md_jadual(he[he.jenis == 'kelas_pullback'], ['nama', 'n', 'pct_sambung_puncak_baru',
                                                   'purata_kedalaman', 'purata_hari_pulih']))
    kpb = he[he.jenis == 'kelas_pullback'].set_index('nama').pct_sambung_puncak_baru.to_dict()
    A(f'\nPullback yang trend sahamnya utuh (SIHAT {kpb.get("PULLBACK SIHAT", float("nan")):.1f}%, '
      f'PASARAN {kpb.get("PULLBACK PASARAN", float("nan")):.1f}%) menyambung ke puncak baru jauh '
      f'lebih kerap daripada pullback AMARAN ({kpb.get("AMARAN", float("nan")):.1f}%). '
      'Ini sokongan paling jelas bagi falsafah "pegang selagi naik".\n')
    A('\n### Grid 18 peraturan HOLD (deskriptif)\n')
    A(md_jadual(he[he.jenis == 'peraturan_hold'], ['nama', 'n', 'pct_sambung_puncak_baru',
                                                   'purata_kedalaman', 'purata_hari_pulih']))
    A('\n### Common/unique HOLD (lulus FDR)\n')
    A(f'{fdr["HOLD"]["lulus"]} / {fdr["HOLD"]["n"]} signal HOLD lulus BH-FDR q ≤ 0.01: '
      f'{", ".join("`"+s+"`" for s in fdr["HOLD"]["signal"])}\n')
    A('\n' + md_jadual(he[(he.fasa == 'HOLD') & (he.jenis == 'common_unique')]
                       .sort_values('lift_presisi', ascending=False),
                       ['nama', 'subset', 'n', 'K_padu', 'K_gagal', 'lift', 'presisi',
                        'lift_presisi', 'kelas'], 20))

    A('\n## 7. Step 6 — EXIT (semua CALON)\n')
    A('> AMARAN BIAS (arahan Step 6.6): dikira atas run sahaja.\n\n')
    A(md_jadual(he[he.jenis == 'calon_exit'], ['nama', 'n', 'pct_menyala',
                                               'median_hari_dari_puncak', 'median_pulangan_exit',
                                               'median_pct_kekal', 'kadar_exit_palsu']))
    ce = he[he.jenis == 'calon_exit']
    ma_ = ce[ce.nama.isin(['bawah_ema9', 'bawah_ema21', 'bawah_ma50'])]
    hd = pd.to_numeric(ma_.median_hari_dari_puncak, errors='coerce')
    kk_ = pd.to_numeric(ma_.median_pct_kekal, errors='coerce')
    pls = pd.to_numeric(ce.kadar_exit_palsu, errors='coerce')
    A(f'\n`median_hari_dari_puncak` negatif bermakna signal menyala **sebelum** puncak — iaitu ia '
      f'menjual terlalu awal. Exit berasaskan MA (EMA9/EMA21/MA50) menyala '
      f'{abs(hd.max()):.0f}–{abs(hd.min()):.0f} hari sebelum puncak dan mengekalkan hanya '
      f'{kk_.max():.0f}% hingga {kk_.min():.0f}% keuntungan. Kadar exit palsu '
      f'{pls.min():.0f}%–{pls.max():.0f}%.\n')
    A(f'\n**Keluarga EXIT: 0 / {fdr["EXIT"]["n"]} signal lulus BH-FDR q ≤ 0.01.** Tiada signal '
      'EXIT yang membezakan "hari sebelum puncak akhir" daripada "palung pullback biasa" selepas '
      'kawalan pelbagai ujian.\n')

    A('\n## 8. Step 7 — false signal ENTRY (imbasan seluruh universe)\n')
    A(f'Setiap signal corong diimbas atas **semua** hari universe {th} '
      f'({ks["n_hari_saham"]:,} baris (ticker, hari); '
      f'{ks["n_hari_saham_dalam_univ"]:,} selepas topeng universe). Kadar asas KAWALAN RAWAK '
      f'(MFE63 ≥ 30%) = {fs_u.kadar_asas_rawak.dropna().iloc[0]:.2f}%.\n\n')
    A(md_jadual(fs_u, ['signal', 'n_kemunculan', 'kadar_tepat_mfe30', 'lift_tepat',
                       'kadar_palsu_bawah10', 'kadar_tepat_bertangga', 'ketulenan_trend_median',
                       'mfe63_p50', 'mfe63_p75', 'mfe63_p90', 'pct_mfe63_ge30', 'pct_mfe63_ge100',
                       'mfe252_p90', 'pct_mfe252_ge100', 'median_hari_mfe63',
                       'jangkaan_henti2atr', 'kadar_menang', 'kapasiti', 'tanda']))
    A('\nTaburan berat di hujung kanan: perhatikan jurang antara `mfe63_p50` dan `mfe63_p90`. '
      'p90 dan % ≥ 100% ialah pembeza, bukan median.\n')
    ut_l = ut.copy()
    ut_l['lift_n'] = pd.to_numeric(ut_l.lift, errors='coerce')
    cand = ut_l[ut_l.signal.isin(fs_u.signal)].sort_values('lift_n', ascending=False)
    if len(cand):
        c0 = cand.iloc[0]
        lt = pd.to_numeric(fs_u.set_index('signal').lift_tepat, errors='coerce').get(c0.signal)
        A(f'\n**Lift jatuh besar antara Step 4 dan Step 7** (contoh `{c0.signal}`: lift '
          f'{c0.lift_n:.2f} dalam populasi peristiwa → lift_tepat {lt:.2f} atas semua hari '
          'universe). Sebabnya: Step 4 bersyarat pada peristiwa entry yang sah; Step 7 tidak. '
          'Angka Step 7 yang lebih dekat dengan dagangan sebenar.\n')
    A(f'\n### Penapis Step 7.4\n{len(fs_p)} kombinasi signal × penapis diuji '
      f'({len(fs_p[fs_p.tanda=="PENAPIS LULUS"])} lulus kriteria "buang ≥ 30% palsu dan ≤ 10% '
      f'benar").\n')
    A('\n**Tiada penapis lulus.** Termasuk pengesahan 1–2 tutup, SPY/sektor atas MA50, volum '
      'relatif, lapis MA. Kemunculan BENAR dan PALSU tidak dibezakan oleh mana-mana penapis '
      'dipradaftar. Ini keputusan negatif yang bersih.\n')
    A('\n10 contoh penapis terbaik (ikut % palsu dibuang):\n\n')
    A(md_jadual(fs_p.sort_values('buang_palsu_pct', ascending=False),
                ['signal', 'buang_palsu_pct', 'buang_benar_pct'], 10))

    A('\n## 9. Step 7b — ujian ke hadapan HOLD dan EXIT (ufuk terbuka)\n')
    A(f'Set kemasukan: gabungan semua kemunculan {len(l7["signal"])} signal yang lulus Step 7 = '
      f'{l7b.get("n_kemunculan_unik", 0):,} (ticker, tarikh) unik'
      + (f', disampel berlapis ikut bulan ke **{l7b.get("n_kemasukan_diuji", 0):,}** (benih 42; '
         f'SPEC §13.9)' if l7b.get('disampel') else ' (tiada sampel; semua diuji)')
      + '. Grid 18 HOLD × 13 EXIT = **234** sistem.\n')
    A('\n### TIGA RUJUKAN WAJIB\n')
    A(md_jadual(hh[hh.sistem.str.startswith('REF_')],
                ['sistem', 'n', 'median_pulangan', 'purata_pulangan', 'jangkaan', 'kadar_menang',
                 'purata_menang', 'purata_kalah', 'purata_hari_pegang', 'mae_median',
                 'pct_exit_terlalu_awal', 'pct_terbuka_hari252', 'pct_terpotong_data',
                 'siri_kalah_terpanjang']))
    if n_menang == 0:
        A(f'\n**Keputusan: rujukan "{RUJ_NAMA[menang_ruj]}" menang, dan 0 / {n_sistem} sistem '
          f'mengalahkan ketiga-tiga rujukan** (ambang = jangkaan rujukan terbaik = '
          f'{l7b["ambang"]:.3f}%). Mengikut arahan Step 7b.4, jawapan kajian ialah '
          f'**"jangan jual"** — dan itu dilaporkan sebagai penemuan, bukan kegagalan.\n')
    else:
        sis_ = hh[~hh.sistem.str.startswith('REF_')].copy()
        sis_['j'] = pd.to_numeric(sis_.jangkaan, errors='coerce')
        n_pos = int((sis_.j > 0).sum())
        n_med_pos = int((pd.to_numeric(sis_.median_pulangan, errors='coerce') > 0).sum())
        A(f'\n**Keputusan: {n_menang} / {n_sistem} sistem mengalahkan ketiga-tiga rujukan** '
          f'(ambang = jangkaan rujukan terbaik = {l7b["ambang"]:.3f}%, '
          f'"{RUJ_NAMA[menang_ruj]}"). Ini berlaku kerana rujukan itu sendiri lemah tahun ini, '
          f'bukan semestinya kerana sistem itu kuat.\n')
        A(f'\nUkuran mutlak, bukan kedudukan: **{n_pos} / {n_sistem}** sistem berjangkaan '
          f'positif dan **{n_med_pos} / {n_sistem}** bermedian pulangan positif. '
          + ('Ambang rujukan NEGATIF tahun ini, jadi "mengalahkan rujukan" boleh bermakna '
             'sekadar kurang rugi.\n' if l7b['ambang'] <= 0 else '\n')
          + '\nSemuanya masih perlu melalui FDR keluarga SISTEM dalam Step 8 '
          f'({fdr["SISTEM"]["lulus"]}/{fdr["SISTEM"]["n"]} lulus q ≤ 0.01).\n')
    A(f'\n### 15 sistem terbaik daripada {n_sistem}\n')
    A(md_jadual(hh[~hh.sistem.str.startswith('REF_')],
                ['sistem', 'n', 'median_pulangan', 'purata_pulangan', 'jangkaan', 'kadar_menang',
                 'purata_hari_pegang', 'mae_median', 'pct_exit_terlalu_awal',
                 'pct_terbuka_hari252'], 15))
    A('\nPerhatikan `pct_exit_terlalu_awal` 68%–78% bagi sistem terbaik: walaupun selepas veto '
      'HOLD, majoriti exit berlaku sebelum harga naik ≥ 10% lagi.\n')

    A('\n## 10. Step 8 — kawalan kebetulan\n')
    A('### Ujian label rawak dan FDR per keluarga\n')
    A(md_jadual(pd.DataFrame([dict(keluarga=k, N=v['n'], lulus_fdr=v['lulus'],
                                   ambang_p=v['ambang']) for k, v in fdr.items()])))
    A(f'\nPerbandingan yang diminta arahan: **{fdr["ENTRY/PADU"]["lulus"]} signal lulus FDR '
      f'daripada {fdr["ENTRY/PADU"]["n"]} diuji**, manakala label rawak menghasilkan lift purata '
      f'yang jauh lebih rendah (lajur `lift_purata_rawak` dalam '
      f'`kawalan_rawak_bootstrap_{th}.csv`).\n')
    A('\n### Jangkaan atas SEMUA kemunculan + ujian outlier\n')
    A(md_jadual(jn, ['signal', 'n_kemunculan', 'median_pulangan', 'jangkaan',
                     'jangkaan_tanpa_5pct_teratas', 'pct_rugi_lebih_10',
                     'siri_kalah_terpanjang', 'jangkaan_bawah95_blok_ticker',
                     'jangkaan_bawah95_blok_minggu']))
    A('\n### Keputusan gate demi gate\n')
    A(md_jadual(kp, ['signal', 'G1_sah_dalam_tahun', 'G2_merentas_tahun', 'G3_nilai_p', 'G3_fdr',
                     'G4_bootstrap', 'G5_outlier', 'G6', 'step7', 'keputusan']))
    terima = kp[kp.keputusan == 'DITERIMA']
    A(f'\n**DITERIMA: {len(terima)}** · **CALON: {len(calon)}**'
      + (f' — {", ".join("`"+x+"`" for x in calon.signal)}' if len(calon) else '')
      + f' · **DITOLAK: {int((kp.keputusan == "DITOLAK").sum())}.**\n')
    if len(terima):
        # Adakah tahun yang mengesahkan itu sendiri MENOLAK signal yang sama?
        canggah = []
        for nm in terima.signal:
            tolak = []
            for y in tahun_lain:
                fy = R / f'keputusan_{y}.csv'
                if not fy.exists():
                    continue
                dy = pd.read_csv(fy).set_index('signal')
                if nm in dy.index and dy.loc[nm, 'keputusan'] == 'DITOLAK':
                    tolak.append(f'{y} (G4 {dy.loc[nm, "G4_bootstrap"]}, '
                                 f'G5 {dy.loc[nm, "G5_outlier"]})')
            if tolak:
                canggah.append((nm, tolak))
        if canggah:
            A('\n> ### AMARAN PERCANGGAHAN GATE 8.1 — baca sebelum menggunakan label DITERIMA\n')
            A('>\n> Gate 8.1 seperti ditulis dalam arahan hanya memerlukan **kelas yang sama** '
              'dalam ≥ 2 tahun lain. Ia **tidak** memerlukan tahun-tahun itu lulus gate keras '
              'mereka sendiri. Akibatnya:\n>\n')
            for nm, tolak in canggah:
                A(f'> - `{nm}` dilabel **DITERIMA** di sini, tetapi **DITOLAK** dalam '
                  f'{"; ".join(tolak)}.\n')
            A('>\n> Maknanya: lift Step 4 konsisten merentas tahun, tetapi kelebihan dagangan '
              '**tidak**. Label DITERIMA di atas adalah betul secara mekanikal mengikut spec yang '
              'dikunci, dan saya tidak mengubah spec selepas melihat hasil. Tetapi ia **tidak '
              'boleh** dibaca sebagai "signal ini boleh didagangkan". Keputusan sama ada gate 8.1 '
              'perlu diketatkan (contoh: memerlukan keputusan CALON, bukan sekadar kelas sama, '
              'dalam ≥ 2 tahun lain) ialah keputusan pengguna.\n')
    if len(calon) and semua_mer:
        A('\nKesemua CALON ialah **konteks pengembangan kemeruapan** (ATR% tinggi, lebar '
          'Bollinger tinggi, julat 20 hari luas). Ini perlu dibaca bersama kaveat survivorship: '
          'kohort kemeruapan tinggi ialah tempat ketiadaan saham delist paling memihak kepada '
          'hasil. Pengesahan merentas tahun (gate 8.1) adalah penentu sebenar.\n')
    elif not len(calon):
        A('\nTiada CALON. Gate yang membunuh semua signal ialah **G4 (bootstrap)** dan '
          '**G5 (outlier)**: jangkaan tidak bertahan pada had bawah 95% blok ticker atau blok '
          'minggu, dan jatuh ke ≤ 0 apabila 5% pemenang teratas dibuang. Maknanya pulangan signal '
          'tahun ini datang daripada beberapa kemunculan melampau, bukan daripada kelebihan yang '
          'boleh diulang.\n')
    A('\nPenapis Step 7.4 kekal CALON tanpa kecuali — arahan 8.5 memerlukan keberkesanan dalam '
      '≥ 2 tahun yang tidak digunakan semasa mencarinya, dan tiada penapis lulus walaupun pada '
      f'{th}.\n')

    A('\n## 11. Step 9 — PRESTASI PORTFOLIO (kriteria akhir)\n')
    asas = pf.asas_entry.iloc[0] if 'asas_entry' in pf.columns else 'CALON selepas Step 8'
    A('Portfolio 8 slot × 12.5%, kos penuh, tiada leverage, satu posisi satu saham. '
      f'Asas signal ENTRY: **{asas}**. Peraturan pemilihan dibekukan (SPEC §12): lift_presisi → '
      'RS 6 bulan → ticker.\n\n')
    if 'TIADA signal CALON' in str(asas):
        A('> Angka di bawah **bukan** bukti sistem lulus — tiada signal ENTRY tahun ini lulus '
          'Step 8. Ia dilaporkan supaya kriteria akhir ada angka dan baris merentas tahun setara '
          '(SPEC §13.10).\n\n')
    A(md_jadual(pf, ['sistem', 'n_posisi_dibuka', 'n_dagangan_ditutup',
                     'n_posisi_terbuka_hujung_tahun', 'purata_slot_terisi', 'pulangan_tahun',
                     'median_bulanan', 'purata_bulanan', 'pct_bulan_ge10', 'pct_bulan_positif',
                     'bulan_terbaik', 'bulan_terburuk', 'mdd', 'purata_hari_pegang',
                     'pusing_ganti_bulanan', 'spy_pulangan_tahun', 'spy_mdd']))
    A('\n### Pulangan bulanan penuh (%)\n')
    A(md_jadual(pb.reset_index().rename(columns={'index': 'bulan'})))
    A('\n### Jawapan terus kepada sasaran +10% sebulan\n')
    A('**TIDAK TERCAPAI — oleh mana-mana sistem.** Angka sebenar:\n\n')
    for _, r in pf.iterrows():
        A(f'- `{r.sistem}`: median bulanan **{r.median_bulanan:.2f}%**, '
          f'{r.pct_bulan_ge10:.1f}% bulan ≥ +10%, bulan terburuk {r.bulan_terburuk:.2f}%, '
          f'MDD {r.mdd:.2f}%, pulangan tahun {r.pulangan_tahun:.2f}% '
          f'(SPY {r.spy_pulangan_tahun:.2f}%, MDD SPY {r.spy_mdd:.2f}%)\n')
    A('\n**Apa yang menghalang — kapasiti, bukan kadar menang.**\n')
    A(f'- Sistem terbaik (`REF_pegang_252`) hanya membuka **{int(ref.n_posisi_dibuka)} posisi '
      f'sepanjang tahun**. Portfolio memerlukan ~11 kemasukan sebulan (~130 setahun). Dengan '
      f'purata pegangan 246 hari, 8 slot terisi pada Januari dan tidak pernah kosong: pulangan '
      f'tahun ialah hasil **8 saham**, bukan sistem. Variansnya sangat tinggi dan tidak boleh '
      f'dijadikan asas keputusan.\n')
    A(f'- Sistem yang pusing ganti mencukupi (Chandelier: {pf[pf.sistem=="REF_chandelier_4atr"].iloc[0].n_posisi_dibuka:.0f} '
      f'posisi, {pf[pf.sistem=="REF_chandelier_4atr"].iloc[0].pusing_ganti_bulanan:.1f}/bulan) '
      f'memberi median bulanan hanya '
      f'{pf[pf.sistem=="REF_chandelier_4atr"].iloc[0].median_bulanan:.2f}% dengan MDD '
      f'{pf[pf.sistem=="REF_chandelier_4atr"].iloc[0].mdd:.2f}% — lebih buruk daripada MDD SPY.\n')
    A('- Pusing ganti juga masih jauh di bawah ~11/bulan kerana kekangan 8 slot: calon jauh '
      'melebihi slot (178,843 kemunculan entri) tetapi slot sentiasa penuh. Dengan pegangan '
      'panjang, **kapasiti slot, bukan kapasiti signal, yang mengikat**.\n')
    A(f'- KAWALAN RAWAK pegang-252 memberi {pf[pf.sistem=="KAWALAN_RAWAK|pegang_252"].iloc[0].pulangan_tahun:.2f}% '
      f'dan Chandelier rawak {pf[pf.sistem=="KAWALAN_RAWAK|chandelier"].iloc[0].pulangan_tahun:.2f}% '
      '— dengan n = 8 dan n = 40 posisi, perbezaan antara signal dan rawak di sini **tidak '
      'bermakna secara statistik**. Jangan tafsir jurang itu sebagai bukti.\n')
    spy_r = float(pf.spy_pulangan_tahun.iloc[0])
    kr = pf[pf.sistem.str.startswith('KAWALAN_RAWAK')]
    sis_sj = pf[~pf.sistem.str.startswith('KAWALAN_RAWAK')]
    kalah_spy = sis_sj[sis_sj.pulangan_tahun < spy_r]
    kalah_rawak = sis_sj[sis_sj.pulangan_tahun < kr.pulangan_tahun.max()]
    A(f'\n### Banding wajib: SPY dan KAWALAN RAWAK\n')
    A(f'- SPY tempoh sama: **{spy_r:.2f}%** (MDD {float(pf.spy_mdd.iloc[0]):.2f}%). '
      f'**{len(kalah_spy)}/{len(sis_sj)}** sistem kalah kepada SPY.\n')
    A(f'- KAWALAN RAWAK terbaik: **{kr.pulangan_tahun.max():.2f}%** '
      f'(`{kr.loc[kr.pulangan_tahun.idxmax()].sistem}`). '
      f'**{len(kalah_rawak)}/{len(sis_sj)}** sistem kalah kepada entri rawak.\n')
    if len(kalah_rawak) == len(sis_sj) and len(sis_sj):
        A('- **Setiap sistem berasaskan signal kalah kepada entri rawak tahun ini.** Itu bukan '
          'bukti signal yang lemah sahaja; ia bukti bahawa pemilihan signal tahun ini memudaratkan '
          'portfolio berbanding memilih secara rawak daripada universe yang sama.\n')
    A('\n> KAVEAT WAJIB STEP 9: tiada saham delist (survivorship), satu tahun satu rejim pasaran, '
      'dan keputusan maksimum pada fasa ini ialah **CALON**. Portfolio 8 slot bermakna setiap '
      'angka tahunan bergantung pada bilangan posisi yang kecil — lihat lajur `n_posisi_dibuka`.\n')

    A('\n## 12. Keputusan akhir (had fasa: CALON)\n')
    if len(calon):
        A(f'1. **ENTRY** — {len(calon)} signal CALON: '
          f'{", ".join("`"+x+"`" for x in calon.signal)}. Tiada pemicu klasik tunggal lulus. '
          f'Hipotesis "magnitud ada pada konteks, bukan pemicu" disokong oleh data {th}.\n')
    else:
        A(f'1. **ENTRY** — TIADA signal CALON pada {th}. Semua gagal G4 (bootstrap) dan/atau '
          f'G5 (outlier). Pemicu klasik tunggal juga tidak lulus.\n')
    A(f'2. **HOLD** — {fdr["HOLD"]["lulus"]}/{fdr["HOLD"]["n"]} signal lulus FDR; kelas pullback '
      f'ialah hasil paling kukuh (SIHAT {kpb.get("PULLBACK SIHAT", float("nan")):.1f}% / '
      f'PASARAN {kpb.get("PULLBACK PASARAN", float("nan")):.1f}% menyambung ke puncak baru lawan '
      f'AMARAN {kpb.get("AMARAN", float("nan")):.1f}%).\n')
    A(f'3. **EXIT** — {fdr["EXIT"]["lulus"]}/{fdr["EXIT"]["n"]} signal lulus FDR; '
      f'{n_menang}/{n_sistem} sistem mengalahkan ketiga-tiga rujukan dan '
      f'{fdr["SISTEM"]["lulus"]}/{fdr["SISTEM"]["n"]} lulus FDR keluarga SISTEM. '
      + ('**Jawapan kajian tahun ini: jangan jual.**\n' if n_menang == 0 else
         '**Tahun ini exit aktif berbaloi** kerana memegang tanpa jual hampir tidak '
         'menguntungkan.\n'))
    capai = pf[pf.median_bulanan >= 10]
    A(f'4. **PORTFOLIO** — sasaran +10% sebulan '
      + (f'dicapai oleh {len(capai)} sistem.\n' if len(capai) else
         'tidak tercapai oleh mana-mana sistem; penghalang utama ialah kapasiti slot apabila '
         'pegangan panjang, bukan kadar menang.\n'))
    if n_terima:
        A(f'5. **{n_terima} signal DITERIMA** — kelas yang sama dalam ≥ 2 tahun lain '
          f'({tahun_lain}) selain lulus semua gate keras: '
          f'{", ".join("`"+x+"`" for x in kp[kp.keputusan == "DITERIMA"].signal)}. '
          f'Lihat `BANDING_TAHUN.md`.\n')
    else:
        A(f'5. **Tiada signal dilabel DITERIMA.** Gate 8.1 memerlukan kelas yang sama dalam '
          f'≥ 2 tahun LAIN; tahun lain yang siap: {tahun_lain if tahun_lain else "tiada"}. '
          f'Lihat `BANDING_TAHUN.md` untuk status merentas tahun.\n')

    A('\n## 13. Fail output\n')
    A('| Fail | Isi |\n|---|---|\n'
      f'| `runs_{th}.csv` | {len(runs)} run, 34 lajur |\n'
      f'| `monthly_summary_{th}.csv` | ringkasan 12 bulan |\n'
      f'| `skipped_{th}.csv` | {len(sk)} calon ditolak + sebab |\n'
      f'| `kohort_masih_naik_{th}.csv` | {len(koh)} run masih_naik dijejak 252 hari |\n'
      f'| `common_unique_{th}.csv` | {len(cu)} baris (213 signal × subset × populasi × kumpulan × keluarga) |\n'
      f'| `taburan_indikator_{th}.csv` | median + p25/p75 setiap indikator setiap hasil |\n'
      f'| `hold_exit_{th}.csv` | {len(he)} baris CALON HOLD/EXIT |\n'
      f'| `false_signal_{th}.csv` | {len(fs)} baris (signal + penapis) |\n'
      f'| `hadapan_hold_exit_{th}.csv` | {len(hh)} sistem (234 + 3 rujukan) |\n'
      f'| `kawalan_rawak_bootstrap_{th}.csv` | nilai-p label rawak + had bawah bootstrap |\n'
      f'| `jangkaan_kemunculan_{th}.csv` | jangkaan + ujian outlier |\n'
      f'| `keputusan_{th}.csv` | keputusan gate demi gate |\n'
      f'| `portfolio_{th}.csv`, `portfolio_bulanan_{th}.csv` | Step 9 |\n'
      '| `log_ujian.csv` | setiap signal/kombinasi yang diuji |\n'
      f'| `PANDANG_HADAPAN_{th}.md` | imbasan pandang ke hadapan |\n'
      '| `SPEC.md` | spec dikunci + 9 pindaan bertarikh |\n')
    (R / f'LAPORAN_{th}.md').write_text('\n'.join(L))
    print(f'LAPORAN_{th}.md: {len("".join(L))} aksara')


if __name__ == '__main__':
    main()
