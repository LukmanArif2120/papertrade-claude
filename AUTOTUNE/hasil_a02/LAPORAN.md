# LAPORAN AUTOTUNE A02

Dijana oleh `AUTOTUNE/sahkan/sahkan_a02.py` (2026-10-18 11:33 UTC). Spec: `AUTOTUNE/SPEC_A02.md`. A01 (`AUTOTUNE/hasil/`) kekal tidak diubah. Parameter SEMASA ialah cadangan sahaja; tiada dagangan wang sebenar.

## Kaveat data

- Release `autotune-data-a02` (yfinance auto_adjust + faktor_split; 2009-01-02 – 2026-10-16; 3260 ticker pernah dalam universe; QC bar titik masa, 1373 lonjakan berbalik dibuang; `AUTOTUNE/data/QC_A02.md`).
- Tiada saham delist (bias survivorship): semua angka ialah had atas. Universe 2010–2013 hanya ~1000–1300 saham.
- Data bermula 2009-01-02: pemanasan kajian 0 (latih 2010) terhad kepada ~1 tahun bagi kaedah bertetingkap panjang.
- Harga backtest dilaras dividen; universe ikut harga tidak dilaras split (masih dilaras dividen).

## Pembetulan audit yang diterapkan

- #1–#3 data: harga tidak dilaras split untuk penapis USD10/nilai dagangan; QC peringkat bar (tiada ticker dibuang kerana kemeruapan).
- #7: n, hari pegang dan kadar menang daripada dagangan yang benar-benar dipegang portfolio 8 × 12.5%.
- #8: objektif = CAGR − CAGR SPY tempoh sama; kekangan MDD ≥ MDD SPY − 10 mata, ≥ 30 dagangan dipegang.
- #17: pemanasan = maks(400 hari, 1.6 × (tetingkap terpanjang julat atas + WARM)) hari kalendar.
- #12: reka bentuk bersih 2010–2018 (saringan 2013–2018; walk-forward 2013–2018); 2019–kini = pengesahan sahaja.
- Dua lorong: `had60` (had pegang 60 hari, seperti A01) dan `asal` (tiada had enjin; TMAX asal).

## Saringan (peringkat 1)

268 kaedah-lorong (PARAM asal, 2013–2018, A dan B); SIAP 268. Skor = min(lebihan A, lebihan B).
- had60: skor > 0 pada 1/134; dipilih 20: M30, M82, M04, M149, M33, M121, M161, M93, M136, M37, M80, M11, M38, M118, M59, M147, M135, M29, M105, M95
- asal: skor > 0 pada 1/134; dipilih 20: M131, M30, M121, M125, M04, M37, M78, M161, M80, M29, M136, M38, M130, M117, M105, M10, M95, M34, M100, M142

## Tala (peringkat 2)

320/320 tugasan SIAP; 38400 percubaan. Kajian 0–5 = ujian 2013…2018 (latih 3 tahun sebelum), 6 = AKHIR (latih 2016–2018, pengesahan 2019-01-01 – hujung), 7 = SEMASA.

## Label

LULUS: lebihan OOS bersih > 0 (A dan B), lebihan pengesahan > 0, MDD OOS (terburuk A/B) ≥ MDD SPY − 10 mata, DSR ≥ 0.9 (N = 268, pulangan berlebihan harian OOS A), imbasan bersih. CALON: tiga syarat pertama. 

| Lorong | LULUS | CALON | TIDAK LULUS | PANDANG HADAPAN |
|---|---|---|---|---|
| had60 | 0 | 0 | 20 | 0 |
| asal | 0 | 0 | 20 | 0 |

SR0 (jangkaan SR maksimum nasib, harian) = 0.0907 daripada 268 SR saringan.

## 10 teratas ikut lebihan OOS bersih (min A, B)

| # | Kaedah-lorong | Label | Lebihan A | Lebihan B | SPY OOS | Pengesahan (lebihan; CAGR / SPY) | MDD OOS / SPY | Dag. A | DSR | Imbasan |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M10_asal | TIDAK LULUS | 3.5% | 2.3% | 12.0% | -0.6% (16.5% / 17.1%) | -23.6% / -19.3% | 197 | 0.00 | BERSIH |
| 2 | M121_had60 | TIDAK LULUS | 6.1% | 0.7% | 12.0% | -12.7% (4.4% / 17.1%) | -21.5% / -19.3% | 237 | 0.01 | BERSIH |
| 3 | M30_had60 | TIDAK LULUS | -0.1% | 4.3% | 12.0% | -17.2% (-0.1% / 17.1%) | -26.8% / -19.3% | 345 | 0.00 | BERSIH |
| 4 | M95_asal | TIDAK LULUS | 0.1% | -1.2% | 12.0% | -23.5% (-6.4% / 17.1%) | -25.4% / -19.3% | 290 | 0.00 | BERSIH |
| 5 | M147_had60 | TIDAK LULUS | -1.8% | 1.4% | 12.0% | -13.8% (3.3% / 17.1%) | -28.2% / -19.3% | 277 | 0.00 | BERSIH |
| 6 | M161_asal | TIDAK LULUS | -2.6% | 3.3% | 12.0% | -9.3% (7.8% / 17.1%) | -36.2% / -19.3% | 551 | 0.00 | BERSIH |
| 7 | M38_had60 | TIDAK LULUS | -2.6% | -0.9% | 12.0% | -8.9% (8.2% / 17.1%) | -28.3% / -19.3% | 201 | 0.00 | BERSIH |
| 8 | M04_had60 | TIDAK LULUS | 5.3% | -2.6% | 12.0% | -15.5% (1.6% / 17.1%) | -27.8% / -19.3% | 344 | 0.00 | BERSIH |
| 9 | M37_asal | TIDAK LULUS | -3.4% | 5.2% | 12.0% | -24.2% (-7.1% / 17.1%) | -28.5% / -19.3% | 270 | 0.00 | BERSIH |
| 10 | M135_had60 | TIDAK LULUS | -3.2% | -3.9% | 12.0% | -19.0% (-1.9% / 17.1%) | -32.2% / -19.3% | 296 | 0.00 | BERSIH |

## Portfolio gabungan

tiada kaedah LULUS atau CALON

## Perbandingan A01 lwn A02

- A01: objektif CAGR mutlak (MDD ≥ −30%), had 60 hari, metrik daripada semua isyarat (bukan dagangan dipegang), walk-forward 2013–2024 atas data dengan universe harga dilaras dan ticker meruap dibuang.
- A01 (semua kaedah): TINGGI 0, SEDERHANA 0, RENDAH 70, GAGAL 64.
- A02 (kaedah-lorong terpilih): LULUS 0, CALON 0, TIDAK LULUS 40, PANDANG HADAPAN 0.

| Kaedah-lorong | Label A01 | Label A02 | Lebihan A (A02) |
|---|---|---|---|
| M121_had60 | RENDAH | TIDAK LULUS | 6.1% |
| M04_had60 | RENDAH | TIDAK LULUS | 5.3% |
| M11_had60 | GAGAL | TIDAK LULUS | 4.7% |
| M10_asal | RENDAH | TIDAK LULUS | 3.5% |
| M04_asal | RENDAH | TIDAK LULUS | 3.0% |
| M95_asal | RENDAH | TIDAK LULUS | 0.1% |
| M30_had60 | RENDAH | TIDAK LULUS | -0.1% |
| M147_had60 | RENDAH | TIDAK LULUS | -1.8% |
| M80_had60 | RENDAH | TIDAK LULUS | -1.9% |
| M29_asal | RENDAH | TIDAK LULUS | -2.5% |
| M161_asal | RENDAH | TIDAK LULUS | -2.6% |
| M38_had60 | RENDAH | TIDAK LULUS | -2.6% |
| M135_had60 | RENDAH | TIDAK LULUS | -3.2% |
| M37_asal | GAGAL | TIDAK LULUS | -3.4% |
| M59_had60 | RENDAH | TIDAK LULUS | -3.9% |
| M130_asal | RENDAH | TIDAK LULUS | -4.0% |
| M82_had60 | RENDAH | TIDAK LULUS | -4.0% |
| M33_had60 | RENDAH | TIDAK LULUS | -4.4% |
| M142_asal | RENDAH | TIDAK LULUS | -5.2% |
| M95_had60 | RENDAH | TIDAK LULUS | -5.4% |

## Imbasan pandang ke hadapan

40 kaedah-lorong diimbas (AKHIR dan SEMASA, 12 tarikh potong 2012–2026); PANDANG HADAPAN: 0. Butiran: [PANDANG_HADAPAN.md](PANDANG_HADAPAN.md).

Fail: `parameter_sedia.csv` (semua kaedah-lorong terpilih, param AKHIR/SEMASA), `gabungan.json`, `saringan.csv`, `pilihan.json`, `tala/<ID>_<lorong>/kNN.json`. Holdout sebenar: ujian ke hadapan sejak 16 Okt 2026 (tidak dinilai).
