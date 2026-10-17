# L02 — Keputusan Ujian: Meta-label (penapis model kedua atas isyarat kaedah)

**Tarikh:** 17 Okt 2026 · **Data:** `data_mentah/dataset_S1–S4` (431 saham) + `index_benchmark` · **Luar sampel:** 1 Jan 2023 – 2 Okt 2026 (16 suku) · **Portfolio:** 8 slot × 12.5% (enjin v1.2) · **Spec:** `SPEC_SEMUA_KAEDAH.md` (`FAIL ASAL: spec/L02`) · **Skrip:** `WFO/kaedah_baru/step2_L02.py` · **Output:** `WFO/data/hasil/L02_ringkasan.csv`, `L02_isyarat.csv.gz` (p setiap hari isyarat luar sampel), `L02_label.csv.gz` (label latihan). Tidak masuk `registry_M_gabung.csv`.

**Verdict ringkas:** DITOLAK. Kriteria memerlukan ≥ 4/6 kaedah; V1 dan V3 masing-masing hanya lulus 1/6, V2 dan V4 0/6. Penapis menaikkan Hit10 bagi beberapa kaedah tetapi biasanya menurunkan CAGR portfolio.

## 1. Cara ujian
| Perkara | Takrif |
|---|---|
| Model utama | M96 V1, M30 V3, M79 V3, M111 V5, M114 V4 (Rangka R), M81 V4. Semua dagangan `trades()` enjin v1.2 sebelum had slot (26,374 isyarat-dagangan sejak 2019) |
| Label y | 1 jika high ≥ buka_masuk × 1.10 dalam ≤ 20 hari dagangan dari hari masuk SEBELUM low ≤ henti kaedah; kedua-duanya pada hari sama = 0 |
| Ciri (tutup hari isyarat) | PCT RS12, PCT RS1 (431), ATR14 ÷ C, C ÷ SMA50 − 1, C ÷ SMA200 − 1, C ÷ maks 252 − 1, vol20 ÷ vol252, SPY 252 hari, SPY ÷ SMA200 − 1, turun naik SPY 21 hari, PCT_ind(IR6) (0.5 jika industri < 3 ahli), ID kaedah (satu-panas) |
| Latihan | Awal setiap suku; isyarat dengan tarikh masuk < awal suku − 25 hari dagangan (purge 20 + embargo 5); piawaian min/SD set latihan; satu model gabungan semua kaedah |
| V1 | Regresi logistik L2 (λ = 1, numpy Newton); sig_L = sig DAN p ≥ median p set latihan |
| V2 | Tiada penapis; rank = p |
| V3 | HistGradientBoosting (scikit-learn, lalai, random_state 0); penapis seperti V1 |
| V4 | Label = pulangan akhir dagangan ≥ +10%; logistik; penapis seperti V1 |
| Penilaian | Isyarat sebelum 1 Jan 2023 dimatikan bagi asas dan semua versi; CAGR/MDD dikira atas lengkung ekuiti dari 1 Jan 2023. Penapis dikenakan pada `sig` (hari isyarat sebenar), kemudian `trades()` dijalankan semula (exitc M114 dan M81 dikira semula kerana bergantung pada sig) |
| Kriteria (ditetapkan sebelum ujian) | Bagi ≥ 4/6 kaedah: Hit10 dagangan lulus − Hit10 semua ≥ +5 mata DAN CAGR ≥ asas; DSR ≥ 0.95 bagi sekurang-kurangnya satu kaedah |

**Andaian saya:** Hit10 = pecahan dagangan portfolio yang MFE ≥ +10% (takrif registry), bukan label y; henti bagi label = `stop` kaedah pada hari isyarat (M81: henti awal tutup − 3×ATR20, bukan henti mengekor); DSR cara W01 (Bailey & López de Prado) atas 24 percubaan berpenapis, SR* = 0.54 tahunan; V2 tidak boleh menaikkan Hit10 (isyarat sama), jadi gagal kriteria Hit10 secara takrif; subset S1–S4 tidak dinilai (spec: dinilai ikut kriteria W01, bukan gate registry); `cari()` enjin dihalakan ke `data_mentah/`, enjin tidak diubah; `scikit-learn` ditambah ke `requirements.txt` untuk V3.

## 2. Hasil luar sampel (1 Jan 2023 – 2 Okt 2026)
| Kaedah | Versi | Dagangan | Hit10 | ΔHit10 | Menang | CAGR | ΔCAGR | MDD | DSR | Lulus |
|---|---|---|---|---|---|---|---|---|---|---|
| M96 V1 | asas | 161 | 59.0% | – | 46.0% | 37.3% | – | -42.0% | – | – |
| M96 V1 | V1 | 158 | 59.5% | +0.5 | 46.2% | 37.5% | +0.2 | -42.0% | 0.81 | Tidak |
| M96 V1 | V2 | 161 | 59.0% | +0.0 | 46.0% | 53.8% | +16.5 | -42.2% | 0.90 | Tidak |
| M96 V1 | V3 | 120 | 68.3% | +9.3 | 48.3% | 58.9% | +21.6 | -42.1% | 0.93 | Ya |
| M96 V1 | V4 | 156 | 57.7% | -1.3 | 44.9% | 39.6% | +2.3 | -41.8% | 0.82 | Tidak |
| M30 V3 | asas | 2298 | 44.2% | – | 36.6% | 67.3% | – | -36.7% | – | – |
| M30 V3 | V1 | 617 | 55.6% | +11.4 | 37.8% | 44.6% | -22.7 | -32.3% | 0.90 | Tidak |
| M30 V3 | V2 | 2298 | 44.2% | +0.0 | 36.6% | 33.4% | -33.9 | -33.5% | 0.83 | Tidak |
| M30 V3 | V3 | 729 | 54.9% | +10.7 | 38.7% | 45.9% | -21.4 | -36.8% | 0.91 | Tidak |
| M30 V3 | V4 | 187 | 40.1% | -4.1 | 27.8% | 30.0% | -37.3 | -26.1% | 0.82 | Tidak |
| M79 V3 | asas | 3616 | 62.9% | – | 41.1% | 48.8% | – | -20.1% | – | – |
| M79 V3 | V1 | 2277 | 63.5% | +0.6 | 41.5% | 49.3% | +0.5 | -26.0% | 0.95 | Tidak |
| M79 V3 | V2 | 3616 | 62.9% | +0.0 | 41.1% | 87.2% | +38.5 | -23.8% | 1.00 | Tidak |
| M79 V3 | V3 | 2023 | 61.7% | -1.2 | 39.8% | 50.5% | +1.8 | -37.0% | 0.90 | Tidak |
| M79 V3 | V4 | 2906 | 62.9% | +0.0 | 40.6% | 71.1% | +22.4 | -22.8% | 1.00 | Tidak |
| M111 V5 | asas | 4939 | 43.4% | – | 37.5% | 62.0% | – | -36.2% | – | – |
| M111 V5 | V1 | 1197 | 55.6% | +12.2 | 40.5% | 65.6% | +3.7 | -40.2% | 0.91 | Ya |
| M111 V5 | V2 | 4939 | 43.4% | +0.0 | 37.5% | 82.8% | +20.8 | -34.4% | 0.98 | Tidak |
| M111 V5 | V3 | 1570 | 50.4% | +7.1 | 37.6% | 46.2% | -15.8 | -29.7% | 0.93 | Tidak |
| M111 V5 | V4 | 1047 | 47.7% | +4.3 | 39.0% | 43.1% | -18.9 | -39.2% | 0.80 | Tidak |
| M114 V4 | asas | 1654 | 56.7% | – | 39.3% | 66.0% | – | -38.8% | – | – |
| M114 V4 | V1 | 1364 | 58.2% | +1.5 | 37.6% | 50.3% | -15.7 | -35.3% | 0.90 | Tidak |
| M114 V4 | V2 | 1654 | 56.7% | +0.0 | 39.3% | 72.9% | +6.9 | -38.1% | 0.97 | Tidak |
| M114 V4 | V3 | 1485 | 57.2% | +0.5 | 38.2% | 37.9% | -28.1 | -35.2% | 0.84 | Tidak |
| M114 V4 | V4 | 1273 | 54.9% | -1.8 | 35.8% | 21.8% | -44.2 | -38.5% | 0.61 | Tidak |
| M81 V4 | asas | 2452 | 57.3% | – | 34.5% | 37.9% | – | -14.4% | – | – |
| M81 V4 | V1 | 1374 | 61.1% | +3.8 | 37.9% | 42.8% | +4.9 | -21.8% | 0.92 | Tidak |
| M81 V4 | V2 | 2452 | 57.3% | +0.0 | 34.5% | 22.7% | -15.1 | -27.5% | 0.75 | Tidak |
| M81 V4 | V3 | 2063 | 58.7% | +1.4 | 35.6% | 49.4% | +11.5 | -18.4% | 0.98 | Tidak |
| M81 V4 | V4 | 2398 | 56.5% | -0.8 | 33.6% | 32.4% | -5.5 | -19.8% | 0.88 | Tidak |

Lulus mengikut versi: V1 1/6 (M111), V2 0/6, V3 1/6 (M96), V4 0/6. Syarat DSR ≥ 0.95 dipenuhi (cth. M79 V2 1.00, M111 V2 0.98), tetapi syarat utama ≥ 4/6 gagal.

## 3. Ambang V1 setiap suku
| Suku | Isyarat latihan | Kadar y | Ambang V1 |
|---|---|---|---|
| 2023-01-01 | 11417 | 43.1% | 0.406 |
| 2023-04-01 | 12303 | 42.9% | 0.405 |
| 2023-07-01 | 13166 | 42.3% | 0.397 |
| 2023-10-01 | 14059 | 41.7% | 0.390 |
| 2024-01-01 | 14907 | 41.4% | 0.386 |
| 2024-04-01 | 15827 | 41.3% | 0.386 |
| 2024-07-01 | 16648 | 41.1% | 0.383 |
| 2024-10-01 | 17699 | 40.6% | 0.379 |
| 2025-01-01 | 18694 | 40.3% | 0.376 |
| 2025-04-01 | 19607 | 39.8% | 0.370 |
| 2025-07-01 | 20647 | 39.7% | 0.369 |
| 2025-10-01 | 21675 | 39.5% | 0.367 |
| 2026-01-01 | 22525 | 39.5% | 0.367 |
| 2026-04-01 | 23546 | 39.9% | 0.371 |
| 2026-07-01 | 24624 | 40.3% | 0.376 |
| 2026-10-01 | 26059 | 40.6% | 0.379 |

## 4. Penemuan penting
1. Penapis menaikkan Hit10 bagi M30 (+11.4 mata), M111 (+12.2) dan M96 V3 (+9.3), tetapi memotong dagangan sehingga separuh, dan CAGR M30 turun 22.7 mata. Ketepatan lebih tinggi tidak menjadi untung portfolio kerana pemenang besar turut ditapis.
2. V2 (tiada penapis, rank = p) menaikkan CAGR bagi 4/6 kaedah: M79 +38.5, M111 +20.8, M96 +16.5, M114 +6.9 mata; tetapi M30 −33.9 dan M81 −15.1. Ia tidak memenuhi kriteria pra-daftar (Hit10 tidak berubah) dan tidak konsisten; ia hanya calon untuk ujian baharu dengan kriteria baharu, bukan diterima.
3. V4 (label pulangan akhir ≥ 10%) paling lemah: M114 −44.2 dan M30 −37.3 mata.
4. DSR tinggi kebanyakannya mencerminkan kekuatan kaedah asas sejak 2023 (pasaran naik), bukan nilai tambah penapis.
5. Risiko lebih padan tinggi: 6 kaedah × 4 versi; luar sampel hanya satu rejim (2023–2026).

## 5. Verdict
**L02 DITOLAK: hanya 1/6 kaedah lulus bagi V1 dan V3 (perlu ≥ 4/6), 0/6 bagi V2 dan V4. Tiada perubahan pada rutin harian atau Papertrade C. Pemerhatian V2 (rank = p menaikkan CAGR 4/6) dicatat untuk keputusan pengguna; ia memerlukan ujian berasingan dengan kriteria yang ditetapkan dahulu.**

## 6. Batasan
- Saiz posisi ikut p tidak boleh diuji (`portfolio()` beku).
- Luar sampel bermula 2023: tiada H1; satu rejim pasaran.
- Bias kemandirian (senarai Shariah hari ini); harga terlaras; 8 saham bermasalah tidak dibuang.
- Klasifikasi industri snapshot Okt 2026 dipakai untuk semua tarikh.
- Andaian dalam Bahagian 1.
