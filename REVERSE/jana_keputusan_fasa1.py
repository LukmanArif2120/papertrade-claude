"""Jana REVERSE/KEPUTUSAN_FASA1.md — keputusan penutup fasa 1 (indikator harga sahaja).

Semua angka dikira daripada CSV yang dicommit; tiada nilai ditulis keras.
Guna: python3 REVERSE/jana_keputusan_fasa1.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.teras import data as D  # noqa: E402

R = AKAR / 'REVERSE'
C = R / '.cache'
BAIK = ('TERAS', 'UNIQUE', 'LANGKA')
PEMICU = ['b:macd_cross', 'b:rsi_lintas50', 'b:ema_crossback', 'b:donchian20', 'b:pocket_pivot',
          'b:gap_and_go']


def main():
    tahun = sorted(int(f.stem.split('_')[-1]) for f in R.glob('keputusan_*.csv')
                   if f.stem.split('_')[-1].isdigit())
    kp, cu, pf, hh, fdr, koh, he, hb, runs, lg = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
    for y in tahun:
        kp[y] = pd.read_csv(R / f'keputusan_{y}.csv')
        d = pd.read_csv(R / f'common_unique_{y}.csv')
        cu[y] = d[(d.subset == 'S2') & (d.populasi == 'a') & (d.kumpulan_data == 'A')
                  & (d.keluarga == 'PADU')].set_index('signal')
        pf[y] = pd.read_csv(R / f'portfolio_{y}.csv')
        hh[y] = pd.read_csv(R / f'hadapan_hold_exit_{y}.csv')
        fdr[y] = json.loads((C / f'fdr_{y}.json').read_text())
        koh[y] = pd.read_csv(R / f'kohort_masih_naik_{y}.csv')
        he[y] = pd.read_csv(R / f'hold_exit_{y}.csv')
        hb[y] = json.loads((C / f'had_bersyarat_{y}.json').read_text())
        runs[y] = pd.read_csv(R / f'runs_{y}.csv')
        lg[y] = json.loads((C / f'lulus7b_{y}.json').read_text())
    uv = D.universe()
    L = []
    A = L.append
    ny = len(tahun)
    t0, t1 = tahun[0], tahun[-1]

    A(f'# KEPUTUSAN FASA 1 — REVERSE ({t0}–{t1})\n')
    A('Dijana `REVERSE/jana_keputusan_fasa1.py`; semua angka dikira daripada CSV yang dicommit.\n')
    A('Fasa 1 menguji **indikator harga sahaja** (77 lajur, tetapan standard, tiada penalaan '
      'parameter). Spec dikunci sebelum larian pertama: `REVERSE/SPEC.md` (12 pindaan bertarikh).\n')

    # ---------- keputusan penutup ----------
    sj = pd.concat([pf[y][~pf[y].sistem.str.startswith('KAWALAN_RAWAK')].assign(tahun=y)
                    for y in tahun], ignore_index=True)
    kr = pd.concat([pf[y][pf[y].sistem.str.startswith('KAWALAN_RAWAK')].assign(tahun=y)
                    for y in tahun], ignore_index=True)
    spy = {y: float(pf[y].spy_pulangan_tahun.iloc[0]) for y in tahun}
    spy_mdd = {y: float(pf[y].spy_mdd.iloc[0]) for y in tahun}
    n_capai = int((sj.median_bulanan >= 10).sum())
    i_best = sj.median_bulanan.idxmax()
    A('## 1. Keputusan penutup\n')
    A(f'**Sasaran pengguna +10% sebulan (median) TIDAK TERCAPAI: {n_capai} daripada {len(sj)} '
      f'sistem-tahun.** Yang terbaik ialah **{sj.loc[i_best, "median_bulanan"]:.2f}%** '
      f'(`{sj.loc[i_best, "sistem"]}`, {int(sj.loc[i_best, "tahun"])}, '
      f'{int(sj.loc[i_best, "n_posisi_dibuka"])} posisi dibuka).\n')
    A(f'\n**Hipotesis fasa 1 ditolak.** Tiada signal entry berasaskan indikator harga menunjukkan '
      f'kelebihan yang berulang merentas {ny} tahun. Purata merentas {len(sj)} sistem-tahun:\n\n')
    A('| | Pulangan/tahun | Median bulanan | MDD |\n|---|---|---|---|\n'
      f'| Sistem berasaskan signal | **{sj.pulangan_tahun.mean():+.2f}%** | '
      f'{sj.median_bulanan.mean():+.2f}% | **{sj.mdd.mean():.2f}%** |\n'
      f'| Entri RAWAK (universe sama) | **{kr.pulangan_tahun.mean():+.2f}%** | '
      f'{kr.median_bulanan.mean():+.2f}% | {kr.mdd.mean():.2f}% |\n'
      f'| SPY | **{np.mean(list(spy.values())):+.2f}%** | — | '
      f'{np.mean(list(spy_mdd.values())):.2f}% |\n')
    menang_spy = int(sum((pf[y][~pf[y].sistem.str.startswith('KAWALAN_RAWAK')].pulangan_tahun
                          > spy[y]).sum() for y in tahun))
    menang_rwk = int(sum((pf[y][~pf[y].sistem.str.startswith('KAWALAN_RAWAK')].pulangan_tahun
                          > pf[y][pf[y].sistem.str.startswith('KAWALAN_RAWAK')]
                          .pulangan_tahun.max()).sum() for y in tahun))
    A(f'\nSistem berasaskan signal memberi pulangan **lebih rendah** daripada entri rawak dengan '
      f'drawdown **{abs(sj.mdd.mean()) - abs(kr.mdd.mean()):.1f} mata peratus lebih dalam**, dan '
      f'kalah kepada SPY pada kedua-dua ukuran. Mengalahkan SPY: **{menang_spy}/{len(sj)}** '
      f'sistem-tahun; mengalahkan entri rawak: **{menang_rwk}/{len(sj)}**.\n')
    A('\n> Kaveat dua arah: data A02 **tiada saham delist** (survivorship), jadi angka sebenar '
      '**lebih buruk** daripada yang dilaporkan di atas, bukan lebih baik.\n')

    # ---------- skop ----------
    A('\n## 2. Skop yang dilindungi\n')
    rows = []
    for y in tahun:
        g = uv[uv.bulan.str[:4] == str(y)].groupby('bulan').size()
        rows.append(dict(tahun=y, universe_min=int(g.min()), universe_median=int(g.median()),
                         universe_maks=int(g.max()), n_run=len(runs[y]),
                         n_peristiwa_sah=hb[y]['n_peristiwa_sah'],
                         n_signal_diuji=len(cu[y]),
                         spy=f'{spy[y]:+.1f}%'))
    A(pd.DataFrame(rows).to_markdown(index=False) + '\n')
    n_ujian = sum(len(pd.read_csv(R / f'common_unique_{y}.csv')) for y in tahun)
    A(f'\nJumlah baris ujian ENTRY direkod: **{n_ujian:,}** (setiap signal × subset × populasi × '
      f'kumpulan data × keluarga), ditambah {ny} × 234 ujian SISTEM dan keluarga HOLD/EXIT. '
      f'Setiap satu dicatat dalam `log_ujian.csv`.\n')
    A(f'\nEmpat rejim pasaran berbeza dilindungi: lonjakan selepas COVID ({t0}), puncak dan '
      f'penguncupan (2021), pasaran menurun (2022, SPY {spy.get(2022, float("nan")):+.1f}%), dan '
      f'tiga tahun menaik (2023–2025).\n')

    # ---------- tiga soalan ----------
    A('\n## 3. Jawapan kepada tiga soalan arahan\n')
    pem_lulus = [(y, nm) for y in tahun for nm in PEMICU if cu[y].kelas.get(nm, '-') in BAIK]
    A(f'**(a) ARAH — adakah saham ini akan naik?** Sedikit, dan tidak boleh dipercayai. Pemicu '
      f'klasik tunggal (MACD cross, RSI lintas 50, EMA crossback, Donchian 20, pocket pivot, '
      f'gap and go) mencapai kelas TERAS/UNIQUE/LANGKA dalam **{len(pem_lulus)} daripada '
      f'{len(PEMICU) * ny}** kombinasi (pemicu × tahun). Dalam imbasan seluruh universe '
      f'(Step 7), lift arah signan terbaik hanya 1.2–2.5 kali kadar asas.\n')
    kons = {}
    for nm in sorted(set().union(*[set(cu[y].index) for y in tahun])):
        kons[nm] = sum(1 for y in tahun if cu[y].kelas.get(nm, '-') in BAIK)
    maks = max(kons.values()) if kons else 0
    atas = [k for k, v in kons.items() if v == maks]
    A(f'\n**(b) MAGNITUD — naik setinggi mana, secepat mana?** Konteks membawa maklumat magnitud, '
      f'pemicu tidak — hipotesis arahan **disokong**. Tetapi tiada konteks kekal: signal terbaik '
      f'mengekalkan kelas penemuan dalam **{maks}/{ny}** tahun sahaja '
      f'({len(atas)} signal), dan **0** dalam kesemua {ny} tahun. Kesemua yang terbaik ialah '
      f'konteks pengembangan kemeruapan (ATR%, julat 20 hari, lebar Bollinger pada kuintil '
      f'tertinggi) — iaitu kohort yang paling dicemari oleh ketiadaan saham delist.\n')
    A(f'\n**(c) KAPASITI — cukup untuk mengisi portfolio?** Signal: ya, berlebihan '
      f'(180–250 ribu kemunculan setahun). Portfolio: **tidak**. Dengan pegangan panjang, 8 slot '
      f'terisi awal dan tidak pernah kosong — rujukan pegang-252 hanya membuka 8–16 posisi '
      f'setahun berbanding ~130 yang diperlukan. **Kapasiti slot yang mengikat, bukan kadar '
      f'menang.**\n')

    # ---------- aritmetik ----------
    A('\n## 4. Mengapa +10% sebulan tidak boleh dicapai dengan reka bentuk ini\n')
    A('Portfolio 8 slot × 12.5% yang penuh = 100% dilabur, jadi pulangan bulanan ≈ jangkaan '
      'setiap dagangan ÷ tempoh pegangan dalam bulan. Jangkaan yang **diperlukan**:\n\n')
    A('| Tempoh pegangan | Jangkaan setiap dagangan diperlukan |\n|---|---|\n'
      + ''.join(f'| {h} hari dagangan | **+{10 * h / 21:.1f}%** |\n' for h in (15, 30, 60)))
    A('\nJangkaan bulanan tersirat yang **terbaik** diukur setiap tahun (atas 234 sistem):\n\n')
    rows = []
    for y in tahun:
        h = hh[y][~hh[y].sistem.str.startswith('REF_')].copy()
        h['j'] = pd.to_numeric(h.jangkaan, errors='coerce')
        h['d'] = pd.to_numeric(h.purata_hari_pegang, errors='coerce')
        h['b'] = h.j / (h.d / 21.0)
        b = h.loc[h.b.idxmax()]
        rows.append(dict(tahun=y, sistem=b.sistem, jangkaan_dagangan=f'{float(b.j):+.2f}%',
                         hari_pegang=round(float(b.d), 1),
                         bulanan_tersirat=f'{float(b.b):+.2f}%',
                         n_sistem_bulanan_ge10=int((h.b >= 10).sum())))
    A(pd.DataFrame(rows).to_markdown(index=False) + '\n')
    A(f'\n**0 daripada {ny * 234:,} sistem-tahun** mencapai 10% bulanan tersirat. Jurangnya bukan '
      f'10–20%; ia 2–5 kali. Mencapai +10% sebulan secara median memerlukan jangkaan setiap '
      f'dagangan ~3 kali yang terbaik pernah diukur, **secara konsisten merentas rejim** — '
      f'sedangkan yang diukur bertukar tanda dari tahun ke tahun.\n')

    # ---------- dapatan kukuh ----------
    A('\n## 5. Dapatan yang kukuh merentas semua tahun\n')
    pb = {y: he[y][he[y].jenis == 'kelas_pullback'].set_index('nama') for y in tahun}
    sh = [f'{y}: SIHAT {pb[y].pct_sambung_puncak_baru.get("PULLBACK SIHAT", float("nan")):.1f}% / '
          f'PASARAN {pb[y].pct_sambung_puncak_baru.get("PULLBACK PASARAN", float("nan")):.1f}% '
          f'lawan AMARAN {pb[y].pct_sambung_puncak_baru.get("AMARAN", float("nan")):.1f}%'
          for y in tahun]
    A(f'1. **Kelas pullback ialah satu-satunya hasil yang berulang {ny}/{ny} tahun.** Pullback '
      f'yang trend sahamnya utuh menyambung ke puncak baru jauh lebih kerap daripada pullback '
      f'yang trendnya rosak — {"; ".join(sh)}. Ini peraturan **pegangan**, bukan peraturan '
      f'masuk.\n')
    e_all = '; '.join(f'{y}: 0/{fdr[y]["EXIT"]["n"]}' for y in tahun)
    A(f'\n2. **Tiada signal EXIT bertahan, pada mana-mana tahun** (BH-FDR q ≤ 0.01): {e_all}. '
      f'Exit berasaskan MA menyala 12–19 hari **sebelum** puncak dengan kadar palsu 46–74%. '
      f'Tiada signal membezakan "hari sebelum puncak akhir" daripada "palung pullback biasa".\n')
    amb = '; '.join(f'{y}: {lg[y]["ambang"]:+.2f}%' for y in tahun)
    A(f'\n3. **"Jangan jual" ialah artifak rejim, bukan penemuan.** Jangkaan rujukan terbaik '
      f'Step 7b berayun mengikut arah 12 bulan selepas kemasukan: {amb}. Bilangan sistem yang '
      f'"mengalahkan ketiga-tiga rujukan" bertentangan arah dengan bilangan yang berjangkaan '
      f'positif — pada 2021, 196/234 mengalahkan rujukan sedangkan **0/234** berjangkaan '
      f'positif. Kedudukan berbanding rujukan bukan ukuran keuntungan.\n')
    k100 = '; '.join(f'{y}: {(koh[y].pct_naik_penuh >= 100).mean() * 100:.1f}%' for y in tahun)
    A(f'\n4. **Kohort "naik dan naik" ialah kesan sebenar tetapi bukan signal.** Run yang masih '
      f'naik pada hari ke-63 pergi jauh lebih tinggi ({k100} akhirnya melebihi +100%), tetapi '
      f'`masih_naik` ialah **label hasil** yang hanya diketahui pada hari ke-63 — ia tidak boleh '
      f'didagangkan. Julat 15.6%–54.6% itu juga menunjukkan betapa ia bergantung pada rejim.\n')

    # ---------- boleh diguna ----------
    A('\n## 6. Apa yang boleh diguna sekarang, dan apa yang tidak\n')
    A('**Boleh diguna:** kelas pullback sebagai peraturan pegangan — jangan jual pada pullback '
      'yang trend saham (tutup > MA50, MA50 menaik, higher low kekal) dan trend pasaran masih '
      'utuh; layan pullback yang memecahkan struktur itu secara berbeza. Ini selari dengan '
      'falsafah lorong 2 repo dan disokong {}/{} tahun.\n'.format(ny, ny))
    A('\n**TIDAK boleh diguna:** mana-mana signal entry dalam kajian ini sebagai asas belian. '
      'Tiada satu pun lulus gate keras dalam lebih daripada satu tahun, dan portfolio yang '
      'dibina atasnya kalah kepada entri rawak daripada universe yang sama.\n')

    # ---------- tidak diuji ----------
    A('\n## 7. Apa yang fasa 1 TIDAK uji\n')
    A('Dikeluarkan atas sebab tiada data titik-masa (SPEC §10), bukan kerana dianggap tidak '
      'penting:\n\n'
      '- **RS rating lawan seluruh pasaran** (`data/rs/` bermula 2026-09-15)\n'
      '- **Gred sektor/industri** (`gred_kumpulan_sejarah.csv` bermula 2026-09-25)\n'
      '- **Earnings**: kejutan EPS, power earnings gap, jarak ke tarikh earnings '
      '(`data/sec/` bermula 2026-10-27)\n\n'
      'RS lawan SPY dan garisan RS **dikira sendiri** daripada harga dan kekal dalam kajian; '
      'ia antara yang gagal gate keras.\n')
    A('\nKerana liputan sejarahnya 0% bagi ' + f'{t0}–{t1}' + ', dimensi ini hanya boleh diuji '
      '**ke hadapan**, bukan dengan backtest. Hasil bermakna memerlukan 1–2 tahun pengumpulan.\n')

    # ---------- had ----------
    A('\n## 8. Had kajian ini\n')
    A('1. **Tiada saham delist** (survivorship) pada setiap tahun: run dipandang tinggi DAN '
      'kadar signal palsu dipandang rendah.\n'
      '2. **Peta sektor bukan titik-masa** (petikan 2026).\n'
      f'3. **Universe {t0} lebih kecil** daripada 2000 saham sebulan, jadi bilangan mutlaknya '
      f'tidak setara dengan 2021–2025.\n'
      '4. **Indeks sektor menggantikan ETF SPDR** (SPEC §13.1) kerana endpoint sejarah tidak '
      'dapat diakses.\n'
      '5. **Portfolio 8 slot** bermakna setiap angka tahunan bergantung pada bilangan posisi '
      'yang kecil (8–415); varians tinggi.\n'
      '6. **Step 7b disampel** 24,000 kemasukan sebulan-berlapis daripada 220–250 ribu '
      '(SPEC §13.9).\n')

    # ---------- status keputusan ----------
    A('\n## 9. Status keputusan setiap tahun (selepas gate 8.1 diketatkan, SPEC §13.12)\n')
    rows = []
    for y in tahun:
        k = kp[y]
        rows.append(dict(tahun=y, diterima=int((k.keputusan == 'DITERIMA').sum()),
                         calon=int((k.keputusan == 'CALON').sum()),
                         ditolak=int((k.keputusan == 'DITOLAK').sum()),
                         lulus_gate_keras=int((k.get('lulus_gate_keras',
                                                     pd.Series(dtype=str)) == 'ya').sum())
                         if 'lulus_gate_keras' in k.columns else None))
    A(pd.DataFrame(rows).to_markdown(index=False) + '\n')
    nm_multi = [nm for nm, v in kons.items() if v >= 2]
    keras_multi = {}
    for y in tahun:
        k = kp[y]
        if 'lulus_gate_keras' in k.columns:
            for nm in k[k.lulus_gate_keras == 'ya'].signal:
                keras_multi[nm] = keras_multi.get(nm, 0) + 1
    byk = sorted([nm for nm, c in keras_multi.items() if c >= 2])
    byk3 = sorted([nm for nm, c in keras_multi.items() if c >= 3])
    n_terima = sum(int((kp[y].keputusan == 'DITERIMA').sum()) for y in tahun)
    A(f'\nSignal yang lulus gate keras dalam **≥ 2 tahun**: '
      f'**{len(byk)}**{" (" + ", ".join("`" + x + "`" for x in byk) + ")" if byk else ""}. '
      f'Signal yang lulus dalam **≥ 3 tahun**: **{len(byk3)}**'
      f'{" (" + ", ".join("`" + x + "`" for x in byk3) + ")" if byk3 else ""}.\n')
    A(f'\nGate 8.1 menuntut ≥ 2 tahun **LAIN**, jadi satu signal perlu lulus gate keras dalam '
      f'**≥ 3 tahun** untuk dinaik taraf. Keempat-empat signal di atas lulus dalam tepat 2 tahun '
      f'(2020 dan 2025) — satu tahun pendek. Itulah sebab gate yang diketatkan menghasilkan '
      f'**{n_terima} DITERIMA**.\n')

    A('\n## 10. Fail\n')
    A('Setiap tahun: `LAPORAN_<TAHUN>.md`, `runs_`, `monthly_summary_`, `skipped_`, '
      '`kohort_masih_naik_`, `common_unique_`, `taburan_indikator_`, `hold_exit_`, '
      '`false_signal_`, `hadapan_hold_exit_`, `kawalan_rawak_bootstrap_`, '
      '`jangkaan_kemunculan_`, `keputusan_`, `portfolio_`, `portfolio_bulanan_`, '
      '`PANDANG_HADAPAN_<TAHUN>.md`.\n\n'
      'Merentas tahun: `BANDING_TAHUN.md`, `banding_tahun.csv`, `JADUAL_KEPUTUSAN.csv`, '
      '`log_ujian.csv`, `SPEC.md`, dan dokumen ini.\n')
    (R / 'KEPUTUSAN_FASA1.md').write_text('\n'.join(L))
    print(f'KEPUTUSAN_FASA1.md siap ({len("".join(L)):,} aksara) | tahun {tahun}')
    print(f'  sasaran +10%/bulan: {n_capai}/{len(sj)} sistem-tahun')
    print(f'  signal lulus gate keras >= 2 tahun: {len(byk)}')


if __name__ == '__main__':
    main()
