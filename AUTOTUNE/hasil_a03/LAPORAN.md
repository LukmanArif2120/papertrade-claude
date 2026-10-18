# LAPORAN AUTOTUNE A03

Dijana oleh `AUTOTUNE/sahkan/sahkan_a03.py` (2026-10-18 13:57 UTC). Spec: `AUTOTUNE/SPEC_A03.md` (termasuk pindaan §6). A01/A02 kekal tidak diubah. Parameter SEMASA ialah cadangan sahaja; tiada dagangan wang sebenar.

## Sistem

- Utama: F (EPS suku terkini tersedia > 0 dan pertumbuhan tahun ke tahun ≥ 25%; tiada data → tidak layak) ∧ M (SPY > SMA50 dan SMA50 > SMA200) pada hari isyarat; 5 slot × 20%; henti = maks(henti kaedah, 0.92 × harga masuk) mulai hari masuk + 1 (peraturan gap dan rendah hari masuk tidak berubah). Lain-lain seperti A02 (kos, slippage, gap, topeng universe, lorong).
- Ablasi (dilaporkan sahaja): F sahaja, M sahaja, tanpa F/M — semuanya 5 slot dan had rugi 8%.
- Tala: objektif lebihan atas SPY, kekangan SPEC_A02 §2 + kadar menang latih ≥ 50% (pelanggar: penalti SPEC_A02 tolak kekurangan kadar menang).

## Kaveat data

- Harga/universe: Release `autotune-data-a02`. EPS: Release `autotune-fundamental-a03` (Yahoo; EPS dilaporkan/dilaras penganalisis, bukan GAAP). Titik masa: sebelum buka → hari laporan; selainnya → hari dagangan berikutnya.
- Liputan EPS ("ada", `AUTOTUNE/fundamental/LIPUTAN.md`) 2013–2018: 2013 94%, 2014 94%, 2015 93%, 2016 94%, 2017 94%, 2018 94%; semua ≥ 70%.
- Tiada saham delist (bias survivorship): angka ialah had atas. Pemangkin, pegangan institusi, pyramiding tidak dimodelkan.

## Pengurangan skop

- Tiada: 20 kaedah × 2 lorong, 10 sistem ditala, 8 kajian, 120 percubaan (skop penuh).

## Kesimpulan

- Label MENANG (SPEC_A03 §6): MENANG 0, HAMPIR 0, TIDAK 10 daripada 10 sistem ditala. Tiada sistem MENANG; kalau tak beli, cakap tak beli.
- 0/10 mengatasi SPY atas OOS bersih (A dan B); 0/10 dalam pengesahan. Label SPEC_A02 (rujukan): LULUS 0, CALON 0, TIDAK LULUS 10, PANDANG HADAPAN 0.

## Saringan (peringkat 1): utama lwn ablasi

160 baris = 20 kaedah × 2 lorong × 4 sistem (PARAM asal, 2013–2018, A dan B); SIAP 160.

| Sistem | Lorong | n | CAGR A&B > 0 | Lebihan A&B > 0 | Median menang A / B | Median PF A | Median lebihan A | Median MDD A | Median dag. A |
|---|---|---|---|---|---|---|---|---|---|
| utama (pemilihan) | had60 | 20 | 15 | 0 | 36.9% / 36.9% | 1.32 | -8.9% | -24.8% | 161 |
| utama (pemilihan) | asal | 20 | 15 | 0 | 35.3% / 34.1% | 1.47 | -6.9% | -25.4% | 126 |
| f_sahaja | had60 | 20 | 17 | 1 | 37.5% / 39.0% | 1.26 | -7.8% | -28.6% | 195 |
| f_sahaja | asal | 20 | 16 | 0 | 36.1% / 34.6% | 1.33 | -7.0% | -28.9% | 157 |
| m_sahaja | had60 | 20 | 7 | 0 | 32.8% / 30.9% | 1.01 | -12.5% | -40.1% | 196 |
| m_sahaja | asal | 20 | 6 | 0 | 32.6% / 32.5% | 1.16 | -9.5% | -36.7% | 160 |
| tanpa | had60 | 20 | 8 | 1 | 34.9% / 33.2% | 1.08 | -11.2% | -37.1% | 250 |
| tanpa | asal | 20 | 12 | 0 | 33.5% / 34.0% | 1.28 | -4.7% | -33.2% | 185 |

Kaedah: pakar M06, M28, M35, M37, M38, M44, M51, M54, M64, M66, M74, M87, M88, M104; lain (saringan A02 `asal` teratas) M131, M30, M121, M125, M04, M78. Ditala (min kadar menang A/B teratas, CAGR A dan B > 0): M37_had60, M38_had60, M121_asal, M88_had60, M121_had60, M37_asal, M88_asal, M78_had60, M51_asal, M04_had60.

## Tala (peringkat 2)

80/80 tugasan SIAP; 9600 percubaan. Kajian 0–5 = ujian 2013…2018 (latih 3 tahun sebelum), 6 = AKHIR (latih 2016–2018; pengesahan 2019-01-01 – hujung), 7 = SEMASA.

## Label

MENANG: menang ≥ 55% (A dan B), CAGR > 0 dan PF ≥ 1.3 (A dan B), MDD OOS ≥ −35%, pengesahan menang ≥ 55% dan CAGR > 0, ≥ 100 dagangan OOS (A dan B), imbasan bersih — 11 syarat; HAMPIR = tepat satu gagal; TIDAK selainnya. Label SPEC_A02 (rujukan): DSR N = 308 atas pulangan berlebihan.

| Lorong | MENANG | HAMPIR | TIDAK | A02: LULUS | A02: CALON | A02: TIDAK LULUS | A02: PANDANG HADAPAN |
|---|---|---|---|---|---|---|---|
| had60 | 0 | 0 | 6 | 0 | 0 | 6 | 0 |
| asal | 0 | 0 | 4 | 0 | 0 | 4 | 0 |

SR0 = 0.0908 (harian, 308 SR saringan A02 + A03 utama).

## Sistem ditala: dagangan (OOS bersih A / B; pengesahan P = A+B)

| # | Sistem | Label (gagal) | Label A02 | Menang % A / B / P | Kalah % A | Purata untung / rugi A | Jangkaan A / B / P | PF A / B / P | Dag. A / B / P |
|---|---|---|---|---|---|---|---|---|---|
| 1 | M121_had60 | TIDAK (3 syarat) | TIDAK LULUS | 53% / 49% / 36% | 47% | 9.9% / -7.1% | 1.97% / 2.08% / 0.71% | 1.60 / 1.53 / 1.14 | 146 / 142 / 188 |
| 2 | M04_had60 | TIDAK (3 syarat) | TIDAK LULUS | 45% / 45% / 31% | 55% | 10.9% / -5.2% | 1.92% / 1.21% / 0.93% | 1.66 / 1.39 / 1.20 | 191 / 197 / 251 |
| 3 | M37_had60 | TIDAK (3 syarat) | TIDAK LULUS | 44% / 49% / 32% | 56% | 13.0% / -6.7% | 2.04% / 1.83% / 1.18% | 1.55 / 1.52 / 1.24 | 147 / 145 / 194 |
| 4 | M121_asal | TIDAK (4 syarat) | TIDAK LULUS | 43% / 44% / 38% | 57% | 11.4% / -7.5% | 0.54% / 1.71% / 1.31% | 1.12 / 1.42 / 1.25 | 150 / 142 / 183 |
| 5 | M51_asal | TIDAK (4 syarat) | TIDAK LULUS | 43% / 42% / 35% | 57% | 15.5% / -6.7% | 2.91% / 1.95% / 2.18% | 1.76 / 1.52 / 1.43 | 90 / 83 / 117 |
| 6 | M38_had60 | TIDAK (4 syarat) | TIDAK LULUS | 52% / 40% / 38% | 48% | 11.2% / -8.0% | 1.95% / 0.25% / 1.28% | 1.51 / 1.06 / 1.25 | 127 / 136 / 164 |
| 7 | M37_asal | TIDAK (4 syarat) | TIDAK LULUS | 40% / 43% / 32% | 60% | 12.8% / -6.5% | 1.26% / 1.26% / -0.06% | 1.32 / 1.35 / 0.99 | 147 / 149 / 170 |
| 8 | M78_had60 | TIDAK (5 syarat) | TIDAK LULUS | 42% / 39% / 20% | 58% | 16.3% / -7.6% | 2.46% / 1.15% / -0.92% | 1.56 / 1.26 / 0.86 | 157 / 153 / 277 |
| 9 | M88_asal | TIDAK (5 syarat) | TIDAK LULUS | 38% / 35% / 0% | 62% | 19.4% / -7.3% | 2.80% / 1.18% / -6.39% | 1.62 / 1.26 / 0.00 | 108 / 101 / 3 |
| 10 | M88_had60 | TIDAK (9 syarat) | TIDAK LULUS | 35% / 33% / 0% | 65% | 12.9% / -6.5% | 0.20% / -0.83% / -7.30% | 1.05 / 0.83 / 0.00 | 84 / 81 / 5 |

## Sistem ditala: pulangan lwn SPY

| # | Sistem | CAGR A / B | Lebihan A / B (SPY OOS) | Pengesahan CAGR (lebihan; SPY) | MDD OOS / SPY | MDD peng. / SPY | DSR | Imbasan |
|---|---|---|---|---|---|---|---|---|
| 1 | M121_had60 | 8.4% / 9.2% | -3.7% / -2.9% (12.0%) | 2.6% (-14.5%; 17.1%) | -19.5% / -19.3% | -31.1% / -33.7% | 0.00 | BERSIH |
| 2 | M04_had60 | 11.4% / 7.1% | -0.6% / -5.0% (12.0%) | 3.3% (-13.8%; 17.1%) | -34.7% / -19.3% | -48.0% / -33.7% | 0.00 | BERSIH |
| 3 | M37_had60 | 9.3% / 8.6% | -2.7% / -3.4% (12.0%) | 4.4% (-12.7%; 17.1%) | -19.1% / -19.3% | -39.9% / -33.7% | 0.00 | BERSIH |
| 4 | M121_asal | 1.7% / 7.2% | -10.4% / -4.8% (12.0%) | 4.9% (-12.2%; 17.1%) | -24.4% / -19.3% | -25.8% / -33.7% | 0.00 | BERSIH |
| 5 | M51_asal | 7.3% / 5.0% | -4.7% / -7.0% (12.0%) | 4.9% (-12.2%; 17.1%) | -16.8% / -19.3% | -35.9% / -33.7% | 0.00 | BERSIH |
| 6 | M38_had60 | 7.7% / 0.2% | -4.4% / -11.8% (12.0%) | 3.4% (-13.7%; 17.1%) | -30.6% / -19.3% | -27.7% / -33.7% | 0.00 | BERSIH |
| 7 | M37_asal | 6.1% / 5.1% | -5.9% / -6.9% (12.0%) | -1.8% (-18.9%; 17.1%) | -20.0% / -19.3% | -35.3% / -33.7% | 0.00 | BERSIH |
| 8 | M78_had60 | 11.6% / 4.1% | -0.4% / -7.9% (12.0%) | -10.5% (-27.6%; 17.1%) | -22.2% / -19.3% | -64.1% / -33.7% | 0.00 | BERSIH |
| 9 | M88_asal | 8.2% / 2.8% | -3.8% / -9.3% (12.0%) | -0.5% (-17.6%; 17.1%) | -33.7% / -19.3% | -5.0% / -33.7% | 0.00 | BERSIH |
| 10 | M88_had60 | -0.0% / -2.2% | -12.1% / -14.3% (12.0%) | -0.9% (-18.1%; 17.1%) | -24.9% / -19.3% | -7.6% / -33.7% | 0.00 | BERSIH |

## Portfolio gabungan

tiada sistem MENANG atau HAMPIR; tiada gabungan

## Kriteria MENANG atas 40 kaedah-lorong A02 (rujukan, `menang_a02.csv`)

Dagangan dipegang A02 (8 slot × 12.5%, tanpa F/M) dijana semula dengan parameter setiap kajian: MENANG 0, HAMPIR 1, TIDAK 39. Beza kadar menang A berbanding rekod A02: maks 2.4% (dagangan dijana semula atas data tetingkap A+B; susunan seri rank boleh berbeza). Lima teratas ikut min kadar menang A/B:

| Kaedah-lorong | Label | Menang A / B / P | PF A / B | CAGR A / B / P | MDD OOS | Gagal |
|---|---|---|---|---|---|---|
| M38_had60 | HAMPIR | 55% / 64% / 51% | 1.44 / 2.14 | 9.4% / 11.2% / 8.2% | -28.3% | menang pengesahan ≥ 55% |
| M121_had60 | TIDAK | 53% / 58% / 50% | 1.73 / 1.72 | 18.1% / 12.7% / 4.4% | -21.5% | menang A ≥ 55%; menang pengesahan ≥ 55% |
| M121_asal | TIDAK | 53% / 56% / 51% | 1.25 / 1.35 | 0.4% / 7.7% / 1.9% | -32.0% | menang A ≥ 55%; PF A ≥ 1.3; menang pengesahan ≥ 55% |
| M147_had60 | TIDAK | 50% / 54% / 43% | 1.49 / 1.63 | 10.2% / 13.4% / 3.3% | -28.2% | menang A ≥ 55%; menang B ≥ 55%; menang pengesahan ≥ 55% |
| M82_had60 | TIDAK | 49% / 50% / 46% | 1.40 / 1.03 | 8.1% / -1.1% / -3.6% | -44.5% | menang A ≥ 55%; menang B ≥ 55%; CAGR B > 0; PF B ≥ 1.3; MDD OOS ≥ −35%; menang pengesahan  |

## Perbandingan dengan A02 (kaedah-lorong sama)

| Sistem | Skor saringan A02 / A03 (min lebihan) | Label A02 (rekod) | Label MENANG A02 | Menang A A02 / A03 | PF A A02 / A03 | Lebihan A A02 / A03 | Label A03 |
|---|---|---|---|---|---|---|---|
| M121_had60 | -4.2% / -5.3% | TIDAK LULUS | TIDAK | 53.2% / 53.4% | 1.73 / 1.60 | 6.1% / -3.7% | TIDAK |
| M04_had60 | -1.8% / -1.4% | TIDAK LULUS | TIDAK | 45.6% / 44.5% | 1.74 / 1.66 | 5.3% / -0.6% | TIDAK |
| M37_had60 | -5.0% / -6.3% | TIDAK LULUS | TIDAK | 41.3% / 44.2% | 1.13 / 1.55 | -10.2% / -2.7% | TIDAK |
| M121_asal | -1.4% / -7.7% | TIDAK LULUS | TIDAK | 53.1% / 42.7% | 1.25 / 1.12 | -11.6% / -10.4% | TIDAK |
| M51_asal | -6.2% / -8.7% | tidak ditala | — | — / 43.3% | — / 1.76 | — / -4.7% | TIDAK |
| M38_had60 | -6.5% / -10.2% | TIDAK LULUS | HAMPIR | 55.1% / 52.0% | 1.44 / 1.51 | -2.6% / -4.4% | TIDAK |
| M37_asal | -1.9% / -10.0% | TIDAK LULUS | TIDAK | 45.9% / 40.1% | 1.43 / 1.32 | -3.4% / -5.9% | TIDAK |
| M78_had60 | -11.6% / -8.2% | tidak ditala | — | — / 42.0% | — / 1.56 | — / -0.4% | TIDAK |
| M88_asal | -12.0% / -5.2% | tidak ditala | — | — / 38.0% | — / 1.62 | — / -3.8% | TIDAK |
| M88_had60 | -13.8% / -4.3% | tidak ditala | — | — / 34.5% | — / 1.05 | — / -12.1% | TIDAK |

## Imbasan pandang ke hadapan

10 sistem diimbas (AKHIR dan SEMASA, 12 tarikh potong; isyarat termasuk topeng F dan M; F dikira daripada EPS yang sudah dilaporkan pada setiap tarikh potong); PANDANG HADAPAN: 0. Butiran: [PANDANG_HADAPAN.md](PANDANG_HADAPAN.md).

Fail: `saringan.csv`, `pilihan.json`, `parameter_sedia.csv`, `menang_a02.csv`, `gabungan.json`, `tala/<ID>_<lorong>/kNN.json`. Holdout sebenar: ujian ke hadapan sejak 16 Okt 2026 (tidak dinilai).
