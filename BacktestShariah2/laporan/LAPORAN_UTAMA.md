<!-- FAIL ASAL: laporan/M114.md -->
# M114 — Keputusan Backtest Shariah: RS Peneraju Semasa Pasaran Menaik (enjin v1.2)

**Tarikh:** 10 Okt 2026 · **Data:** dataset_S1–S4 (431 saham) + index_benchmark (SPY, QQQ) · **Tempoh:** 1 Nov 2019 – 2 Okt 2026 · **Portfolio:** 8 slot × 12.5% · **Registry:** `registry/M114.csv` (26 baris)

**Verdict ringkas:** V4 (kolam 10% teratas) lulus semua syarat LAYAK di set 431 (GUNA, skor 77.4, CAGR 49.6%, 4/4 subset). **Tetapi selepas 8 saham bermasalah dibuang, V4 jatuh ke UJI KERTAS (31.1%, skor 64.4)**, kerana satu dagangan FCEL (+780%) mengangkat keputusan asal. Lihat Bahagian 10.

## 1. Cara ujian
| Perkara | V1 (spec dikunci) |
|---|---|
| Isyarat | Persentil RS12 (garis RS = tutup ÷ SPY) ≥ 0.80 merentas 431 saham, SPY > SMA200, purata volum 20 hari ≥ 100K, ≥ 252 hari data RS. Isyarat setiap hari dalam kolam |
| Masuk | Buka hari i+1 |
| Henti | −12% daripada harga masuk (tetap) |
| Keluar | Tutup < (tutup tertinggi sejak masuk − 3×ATR22); jual buka esok |
| Had masa / sasaran | Tiada |
| Ranking | RS12 tertinggi |

| Varian | Beza daripada V1 |
|---|---|
| V0 | I03 tulen: RSL paras tertinggi 252 hari, keluar tutup < SMA20, tiada henti |
| V2 | Keluar tutup < SMA50 |
| V3 | Henti −8% |
| V4 | Kolam 10% teratas (PCT ≥ 0.90) |
| V5 | Tanpa penapis SPY > SMA200 |

**Andaian saya:**
- Henti disentuh intrahari (cara enjin), bukan "tutup < henti".
- Keluar chandelier bergantung pada tarikh masuk. Laluan enjin direplika untuk menandakan hari keluar tepat (`exitc` benar hanya pada hari keluar). Semakan 300 dagangan rawak: 0 ralat.
- V0 mengekalkan penapis volum 20 hari.
- Persentil dikira atas 431 saham (ikut spec), termasuk bagi subset.

## 2. Semua varian, set 431
| Varian | Keputusan | Skor | CAGR | MDD | Separuh 1/2 | Dagangan | Menang | Tutup ≥+10% | > Sama rata? | Gate gagal |
|---|---|---|---|---|---|---|---|---|---|---|
| V0 I03 tulen | DITOLAK | – | 32.5% | −37.0% | 6.5% / 60.1% | 4215 | 39.0% | 13.9% | Ya | G1 |
| V1 Dikunci | SIMPAN | 44.2 | 23.3% | −35.5% | 9.5% / 38.1% | 4719 | 38.6% | 21.2% | Ya | – |
| V2 Keluar SMA50 | UJI KERTAS | 64.1 | 37.3% | −37.7% | 31.7% / 42.8% | 12568 | 40.9% | 6.3% | Ya | – |
| V3 Henti 8% | SIMPAN | 43.8 | 19.7% | −34.6% | 22.6% / 18.1% | 5427 | 33.9% | 18.7% | Tidak | – |
| **V4 Kolam 10%** | **GUNA** | **77.4** | **49.6%** | −38.8% | 35.9% / 64.7% | 2619 | 38.1% | 22.3% | Ya | – |
| V5 Tanpa SPY | UJI KERTAS | 67.9 | 39.8% | −43.9% | 16.5% / 66.1% | 5303 | 41.0% | 23.7% | Ya | – |
| QQQ | | | 21.7% | −35.1% | 10.4% / 32.4% | | | | | |
| SPY | | | 15.9% | −33.7% | 9.1% / 22.1% | | | | | |
| Sama rata 431 | | | 21.9% | −40.3% | 16.4% / 27.4% | | | | | |
| I03 (registry) | DITOLAK | | 32.1% | −37.0% | | | | | | G1 |

CAGR hingga Dis 2025: V0 20.3%, V1 9.6%, V2 31.9%, V3 18.0%, V4 44.2%, V5 22.3% (SPY 15.6%, QQQ 20.9%).

## 3. Ujian konsisten S1–S4 (V4)
| Set | Keputusan | CAGR | MDD | Sama rata set | Gate gagal |
|---|---|---|---|---|---|
| S1 | SIMPAN (56.7) | 25.2% | −31.9% | 18.9% | – |
| S2 | UJI KERTAS (73.1) | 34.2% | −43.2% | 27.9% | – |
| S3 | GUNA (84.9) | 35.5% | −30.1% | 21.8% | – |
| S4 | SIMPAN (50.5) | 21.7% | −31.0% | 17.4% | – |
| **Lulus** | **4/4** | | | | |

V1, V2, V3, V5 juga lulus gate di 431 dan diuji di S1–S4 (dalam registry). V1 3/4, V2 1/4, V3 3/4, V5 4/4.

## 4. Berapa lama pegang (V4, 431)
| Hari | 5 | 10 | 15 | 20 | 30 | 40 | 60 |
|---|---|---|---|---|---|---|---|
| Purata % | 1.0 | 1.6 | 2.4 | 3.4 | 4.7 | 6.8 | 10.7 |

Purata pegangan sebenar 28.8 hari. Sebab keluar: chandelier 65.3%, henti 32.8%, hujung data 1.9%. Purata pertama kali ≥ +10% pada hari ke-60.

## 5. Sasaran bulanan (V4, 431)
Bulan untung 57.8%; bulan ≥ +10% 24.1%.

## 6. Gate G1–G6 (V4, 431)
| Gate | Syarat | Nilai | |
|---|---|---|---|
| G1 | Ada henti, purata rugi ≥ −12% | −9.5% | ✅ |
| G2 | ≥ 100 dagangan | 2619 | ✅ |
| G3 | CAGR > SPY | 49.6% > 15.9% | ✅ |
| G4 | MDD ≥ −45% | −38.8% | ✅ |
| G5 | Kedua-dua separuh positif | 35.9% / 64.7% | ✅ |
| G6 | Long, mekanikal | Ya | ✅ |

## 7. Semakan kewarasan (V4, 431)
| Semakan | Hasil |
|---|---|
| Isyarat setahun | ~379 |
| Slot purata terisi | 6.73 / 8 |
| 5 terbaik | FCEL +780%, IREN +454%, VRT +449%, AXTI +423%, APP +354% |
| 5 terburuk | GRAL −46.6%, TGTX −43.9%, KGC −25.9%, DV −21.3%, TTD −21.3% |
| Pulangan tahunan | 2020 +78.5%, 2021 +51.1%, 2022 −2.3%, 2023 +61.6%, 2024 +99.8%, 2025 +12.3%, 2026 (separa) +70.1% |
| V0 lawan I03 | 32.5% lawan 32.1% (beza kecil kerana penapis volum) |

## 8. Penemuan penting
1. Kolam 10% teratas (V4) jauh lebih baik daripada 20% (V1: 23.3%, kalah QQQ hingga Dis 2025).
2. Satu dagangan FCEL (+780%), salah satu saham bermasalah data, menyumbang banyak kepada CAGR V4.
3. V4 menewaskan SPY dalam 5/6 tahun penuh; hanya 2022 negatif.
4. Henti −8% (V3) lebih teruk daripada −12%, selaras corak Project.
5. Kadar menang ~38%; untung datang daripada beberapa pemenang besar.

## 9. Verdict (set 431)
**V4 LAYAK di set 431: lulus semua gate (GUNA 77.4), menewaskan sama rata 431 (49.6% lawan 21.9%), lulus gate 4/4 subset. Namun angka ini tidak tahan apabila saham bermasalah dibuang (Bahagian 10).**

## 10. Semakan ketahanan: tanpa 8 saham bermasalah (10 Okt 2026)
Saham dibuang: ASST, FCEL, MTDR, OVV, PR, SM, VAL, XENE (peristiwa korporat tidak terlaras, seperti dalam spec). Alam ujian 423 saham. Semakan maklumat sahaja; tidak masuk registry.

| Cara | Keputusan | Skor | CAGR | MDD | Separuh 1/2 | Hingga Dis 2025 |
|---|---|---|---|---|---|---|
| 431 asal | GUNA | 77.4 | 49.6% | −38.8% | 35.9% / 64.7% | 44.2% |
| Tapis dagangan sahaja (persentil kekal atas 431) | UJI KERTAS | 66.2 | 36.7% | −39.7% | 11.3% / 65.0% | – |
| **Persentil dikira semula atas 423** | **UJI KERTAS** | **64.4** | **31.1%** | −34.2% | 16.8% / 46.5% | 24.2% |
| Sama rata 423 | | | 21.8% | | | |

Varian lain tanpa 8 saham (tapis dagangan sahaja): V0 31.7%, V1 27.6%, V2 29.0% (SIMPAN 49.3), V3 20.7%, V5 39.9% (UJI KERTAS 65.7).

**Kesimpulan:** M114 V4 sensitif kepada beberapa saham sahaja. Selepas pembersihan ia masih menewaskan SPY dan sama rata, tetapi turun ke UJI KERTAS dan di bawah M96 V1.

## 11. Batasan
- Senarai Shariah ialah senarai hari ini (bias kemandirian); tinggi bagi kaedah RS yang memburu pemenang.
- Harga terlaras; 8 saham ada peristiwa korporat tidak terlaras.
- Persentil atas 431 bagi subset (ikut spec; peraturan skill biasa mengira semula dalam subset).
- Henti intrahari, bukan tutup.
- Tahun 2026 separa (hingga 2 Okt 2026).

registry/M114.csv disimpan (26 baris). Perbandingan merentas kaedah: `laporan/SEMAKAN_TANPA_8_SAHAM.md`.


---

<!-- FAIL ASAL: laporan/P01_peringkat1.md -->
# P01 — Peringkat 1: Ujian utama V1 (431 saham)

**Tarikh:** 10 Okt 2026 · **Enjin:** `standard/enjin_p01.py` v1.0 · **Data:** dataset_S1–S4 (431 saham Shariah), 2019–2026 · **Spesifikasi:** `spec/P01_corak_isyarat_macd.md`

**Verdict: GAGAL di peringkat 1.** Secara keseluruhan, kejadian "semua isyarat lengkap" (MACD hijau + MA10>MA20 + RSI>50 + squeeze hijau) **tidak lebih baik daripada masuk pada hari rawak** dalam saham yang sama: naik ≥20% dalam 60 hari 27% berbanding 28% rawak; gagal teruk 39% berbanding 38%. Keputusan sama dalam kedua-dua tempoh dan keempat-empat subset.

| Penemuan | Bukti |
|---|---|
| Isyarat lengkap ≈ rawak | 27% vs 28% berjaya; stabil di S1–S4 dan 2019–2023 / 2024–2026 |
| Turutan "sihat" tiada kelebihan | 27% (sihat) = 27% (tidak sihat) |
| MACD bukan isyarat pertama | RSI>50 sudah ON sebelum MACD hijau dalam 56% kejadian; MA10>MA20 dalam 36% |
| MACD hijau yang TIDAK disusuli isyarat lain = amaran | 13% berjaya, 63% gagal teruk (rawak: 28% / 38%) |
| Calon untuk diperhati (belum terbukti) | Turutan `M1 → A1 → R1+Q3`: 155 kejadian, 38% berjaya (penemuan 34%, pengesahan 45%; S1–S4 34–45%). Lulus syarat ≥5 mata, gagal syarat 1.5×. Kemungkinan kebetulan tinggi kerana ~40 turutan dibandingkan |
| Cara keluar | E0 (MACD merah) median −1.3%, 10 hari. E3 (3×ATR) % ≥+10% tertinggi (18%) tetapi median −3.4% |
| 2020 | Semua kumpulan lebih tinggi (37–39%); tanpa 2020 keputusan sama (25% vs 26%) |

Data penuh kejadian (88,966 baris, 38 MB) tidak disimpan dalam Project kerana had ruang. Ringkasan agregat: `registry/P01_V1_ringkasan.csv` (status × turutan × tempoh × subset).

---

# P01 — Laporan kajian corak (V1)

Kejadian lengkap: **19863** · tidak lengkap: 6317 · hari rawak: 59536 · dibuang (gap > 15%): 15 · hanya kejadian dengan ufuk 60 hari penuh.

## 1. Turutan dan hasil (ufuk 60 hari)
| Turutan | Bil. | Berjaya ≥20% | Sederhana | Gagal <10% | Gagal teruk | Median naik maks | Median untung E0 | Median hari E0 |
|---|---|---|---|---|---|---|---|---|
| pra:A1+R1+Q3 ; M1 | 5713 | 25% | 23% | 14% | 38% | +11.3% | -1.1% | 6 |
| pra:R1 ; M1 → A1+Q3 | 1367 | 28% | 23% | 12% | 38% | +12.7% | -1.4% | 10 |
| pra:R1 ; M1 → Q3 → A1 | 1306 | 26% | 25% | 11% | 38% | +12.5% | -1.2% | 10 |
| M1 → R1 → Q3 → A1 | 1240 | 29% | 20% | 11% | 40% | +12.9% | -1.5% | 14 |
| M1 → R1 → A1+Q3 | 1160 | 27% | 20% | 11% | 42% | +12.1% | -2.1% | 14 |
| M1+R1 → Q3 → A1 | 1156 | 27% | 22% | 12% | 39% | +12.3% | -1.6% | 12 |
| M1+R1 → A1+Q3 | 904 | 26% | 24% | 11% | 39% | +11.6% | -2.1% | 12 |
| pra:R1 ; M1 → A1 → Q3 | 836 | 28% | 24% | 11% | 38% | +12.8% | -1.5% | 8 |
| M1 → R1 → A1 → Q3 | 604 | 26% | 25% | 8% | 41% | +13.2% | -1.3% | 13 |
| pra:A1+Q3 ; M1+R1 | 601 | 33% | 22% | 10% | 35% | +14.9% | -1.4% | 9 |
| **Semua lengkap** | 19863 | 27% | 23% | 12% | 39% | +12.3% | -1.3% | 10 |
| Sihat (A1 terakhir) | 5329 | 27% | 22% | 11% | 40% | +12.3% | -1.8% | 13 |
| Tidak sihat | 14534 | 27% | 23% | 12% | 38% | +12.3% | -1.2% | 9 |
| Tidak lengkap | 6317 | 13% | 14% | 10% | 63% | +7.5% | -4.9% | 4 |
| **Hari rawak (kawalan)** | 59536 | 28% | 23% | 11% | 38% | +12.8% | -0.3% | 2 |

## 2. Bila isyarat menyala selepas MACD hijau (kejadian lengkap)
| Isyarat | Sudah aktif sebelum | Tidak menyala | Median hari | Julat 25–75% |
|---|---|---|---|---|
| A1 MA10>MA20 | 36% | 0% | 4 | 2–6 |
| R1 RSI>50 | 56% | 0% | 1 | 0–4 |
| Q3 Squeeze hijau | 36% | 0% | 3 | 2–5 |
| D1 +DI>−DI | 52% | 6% | 1 | 0–4 |
| Q1 Squeeze ON | 22% | 61% | 3 | 1–6 |
| A2 Atas MA50 | 54% | 18% | 1 | 0–4 |
| A3 Atas MA150 | 60% | 27% | 1 | 0–3 |
| V1 Volum tinggi | 5% | 67% | 1 | 0–3 |

## 3. Peratus A menyala lebih awal daripada B (baris = A)
| A \ B | A1 | R1 | Q3 | D1 | Q1 |
|---|---|---|---|---|---|
| A1 | – | 9% | 19% | 9% | 9% |
| R1 | 56% | – | 54% | 18% | 19% |
| Q3 | 28% | 9% | – | 10% | 7% |
| D1 | 55% | 10% | 53% | – | 20% |
| Q1 | 58% | 36% | 63% | 37% | – |

## 4. Cara keluar
| Kumpulan | Keluar | Purata untung | Median untung | % untung | % ≥ +10% | Nisbah simpanan | Median hari |
|---|---|---|---|---|---|---|---|
| Kejadian lengkap | E0 | +1.0% | -1.3% | 40% | 13% | 0.31 | 10 |
| Kejadian lengkap | E1 | +0.8% | -1.4% | 39% | 12% | 0.30 | 10 |
| Kejadian lengkap | E2 | +1.1% | -1.9% | 36% | 12% | 0.18 | 11 |
| Kejadian lengkap | E3 | +2.3% | -3.4% | 38% | 18% | 0.06 | 22 |
| Kejadian lengkap | E4 | +0.8% | -1.5% | 39% | 13% | 0.29 | 10 |
| Hari rawak | E0 | +0.8% | -0.3% | 45% | 7% | 0.44 | 2 |
| Hari rawak | E1 | +0.7% | -0.4% | 45% | 7% | 0.44 | 2 |
| Hari rawak | E2 | +0.7% | -0.7% | 41% | 7% | 0.29 | 2 |
| Hari rawak | E3 | +2.6% | -3.1% | 39% | 19% | 0.06 | 23 |
| Hari rawak | E4 | +0.7% | -0.7% | 41% | 8% | 0.33 | 4 |

## 5. Isyarat tambahan pada hari T: Berjaya vs Gagal
| Isyarat | % dalam Berjaya | % dalam Gagal | Beza |
|---|---|---|---|
| D1 +DI>−DI | 90% | 90% | +0% |
| Q1 Squeeze ON | 28% | 28% | -0% |
| A2 Atas MA50 | 77% | 79% | -2% |
| A3 Atas MA150 | 69% | 73% | -4% |
| V1 Volum tinggi | 18% | 16% | +2% |

## 6. Kestabilan
| Kumpulan | Bil. lengkap | Berjaya (lengkap) | Berjaya (rawak) | Gagal teruk (lengkap) | Gagal teruk (rawak) |
|---|---|---|---|---|---|
| Tempoh: penemuan | 11926 | 27% | 28% | 39% | 38% |
| Tempoh: pengesahan | 7937 | 27% | 28% | 39% | 37% |
| Subset: S1 | 4939 | 26% | 27% | 39% | 38% |
| Subset: S2 | 5011 | 28% | 30% | 40% | 39% |
| Subset: S3 | 5177 | 26% | 27% | 37% | 37% |
| Subset: S4 | 4736 | 26% | 28% | 39% | 38% |
| Tahun: 2019 | 577 | 21% | 25% | 34% | 32% |
| Tahun: 2020 | 2692 | 37% | 39% | 35% | 36% |
| Tahun: 2021 | 3065 | 24% | 25% | 37% | 35% |
| Tahun: 2022 | 2522 | 25% | 25% | 49% | 47% |
| Tahun: 2023 | 3070 | 22% | 24% | 36% | 35% |
| Tahun: 2024 | 3048 | 21% | 22% | 37% | 35% |
| Tahun: 2025 | 3210 | 29% | 30% | 39% | 37% |
| Tahun: 2026 | 1679 | 33% | 33% | 43% | 42% |
| 2020: 2020 sahaja | 2692 | 37% | 39% | 35% | 36% |
| 2020: tanpa 2020 | 17171 | 25% | 26% | 39% | 38% |

## 7. Kriteria lulus
| Kriteria | Nilai | Lulus |
|---|---|---|
| ≥ 100 kejadian lengkap | 19863 | ✅ |
| % Berjaya turutan terbaik (≥100 kejadian: M1 → A1 → R1+Q3) ≥ 1.5 × rawak | 38% vs 28% | ❌ |
| % Berjaya semua lengkap melebihi rawak ≥ 5 mata | -1.4 mata | ❌ |
| % Gagal teruk < rawak | 39% vs 38% | ❌ |
| % Berjaya > rawak dalam penemuan DAN pengesahan | 27% / 27% | ❌ |



---

<!-- FAIL ASAL: laporan/P01_peringkat2.md -->
# P01 — Peringkat 2: MACD hijau sahaja vs tunggu isyarat lengkap (431 saham)

**Tarikh:** 10 Okt 2026 · **Enjin:** `standard/enjin_p01.py` v1.1 · **Laporan:** `standard/lapor_p01_p2.py` · **Data:** dataset_S1–S4, 2019–2026

**Verdict: GAGAL.** Masuk terus apabila MACD hijau (A) dan menunggu semua isyarat lengkap (B) kedua-duanya **sama dengan hari rawak**: naik ≥20% dalam 60 hari 28% (A) dan 27% (B) berbanding 28% (rawak). Menunggu isyarat lain tidak menambah nilai. Keputusan sama dalam kedua-dua tempoh, keempat-empat subset dan tanpa 2020.

| Penemuan | Bukti |
|---|---|
| MACD hijau sahaja ≈ rawak | 28% vs 28%; gagal teruk 39% vs 38% |
| Menunggu isyarat lengkap tiada kelebihan | 27% (tunggu) vs 28% (terus) |
| Kos menunggu kecil | Harga masuk median hanya +0.3% lebih tinggi; median 3 hari dari MACD hijau ke lengkap |
| AMARAN tafsiran Bahagian 2 | Perbandingan berpasangan dan baris A1/A2 menggunakan maklumat masa depan (sama ada isyarat akan lengkap kemudian). Kejadian A1 terselamat kerana MACD tidak merah sebelum lengkap, jadi A1 (32%) kelihatan lebih baik secara palsu. Ini **tidak boleh** didagangkan. Hanya A, B dan C sah untuk dibandingkan |
| Isyarat amaran (dari Peringkat 1, disahkan) | MACD hijau yang tidak disusuli isyarat lain: 13% berjaya, 63% gagal teruk, purata E0 −5.4% |
| Kriteria "B gagal teruk < A" | Ditanda ✅ oleh skrip kerana beza pecahan kecil; kedua-duanya 39%. Tidak bermakna |

---

# P01 — Peringkat 2: MACD hijau sahaja vs tunggu isyarat lengkap

MACD hijau (semua T0): 26250 · isyarat lengkap: 19863 · hari rawak: 59536 · ufuk 60 hari penuh, tanpa gap > 15%.

## 1. Perbandingan utama (ufuk 60 hari)
| Kumpulan | Bil. | Berjaya ≥20% | Sederhana | Gagal <10% | Gagal teruk | Median naik maks | Median untung E0 | Purata untung E0 | % E0 ≥ +10% | Median hari E0 |
|---|---|---|---|---|---|---|---|---|---|---|
| A. Masuk terus bila MACD hijau (semua) | 26250 | 28% | 22% | 11% | 39% | +12.6% | -1.5% | +1.2% | 14% | 11 |
| B. Tunggu isyarat lengkap | 19863 | 27% | 23% | 12% | 39% | +12.3% | -1.3% | +1.0% | 13% | 10 |
| C. Hari rawak | 59536 | 28% | 23% | 11% | 38% | +12.8% | -0.3% | +0.8% | 7% | 2 |
| A1. MACD hijau → kemudian lengkap | 19935 | 32% | 25% | 12% | 31% | +14.2% | -0.1% | +3.4% | 18% | 13 |
| A2. MACD hijau → tidak lengkap | 6315 | 13% | 14% | 10% | 63% | +7.5% | -4.9% | -5.4% | 1% | 4 |

## 2. Kejadian yang sama: masuk awal vs tunggu (hanya yang kemudian lengkap)
| Ukuran | Nilai | Nota |
|---|---|---|
| Bilangan pasangan | 19850 |  |
| Harga masuk: tunggu berbanding masuk awal (median) | +0.3% | Harga lebih tinggi = kos menunggu |
| % Berjaya: masuk awal / tunggu | 32% / 27% |  |
| % Gagal teruk: masuk awal / tunggu | 31% / 39% |  |
| Median untung E0: masuk awal / tunggu | -0.1% / -1.3% |  |
| Purata untung E0: masuk awal / tunggu | +3.3% / +1.0% |  |
| % pasangan di mana tunggu memberi untung E0 lebih tinggi | 12% |  |
| Median hari dari MACD hijau ke lengkap | 3 |  |

## 3. Cara keluar
| Kumpulan | Keluar | Purata untung | Median untung | % untung | % ≥ +10% | Median hari |
|---|---|---|---|---|---|---|
| A. MACD hijau sahaja | E0 | +1.2% | -1.5% | 39% | 14% | 11 |
| A. MACD hijau sahaja | E1 | +1.0% | -1.7% | 38% | 13% | 10 |
| A. MACD hijau sahaja | E2 | +0.7% | -1.2% | 36% | 9% | 5 |
| A. MACD hijau sahaja | E3 | +2.4% | -3.3% | 38% | 19% | 22 |
| A. MACD hijau sahaja | E4 | +1.0% | -1.8% | 38% | 14% | 11 |
| B. Tunggu lengkap | E0 | +1.0% | -1.3% | 40% | 13% | 10 |
| B. Tunggu lengkap | E1 | +0.8% | -1.4% | 39% | 12% | 10 |
| B. Tunggu lengkap | E2 | +1.1% | -1.9% | 36% | 12% | 11 |
| B. Tunggu lengkap | E3 | +2.3% | -3.4% | 38% | 18% | 22 |
| B. Tunggu lengkap | E4 | +0.8% | -1.5% | 39% | 13% | 10 |

## 4. Kestabilan (% Berjaya)
| Kumpulan | Bil. MACD hijau | A. MACD sahaja | B. Tunggu lengkap | C. Rawak | Purata E0 (A) | Purata E0 (B) |
|---|---|---|---|---|---|---|
| Tempoh: penemuan | 15652 | 27% | 27% | 28% | +1.4% | +1.1% |
| Tempoh: pengesahan | 10598 | 28% | 27% | 28% | +1.0% | +0.8% |
| Subset: S1 | 6566 | 27% | 26% | 27% | +1.1% | +0.8% |
| Subset: S2 | 6659 | 29% | 28% | 30% | +1.5% | +1.3% |
| Subset: S3 | 6749 | 27% | 26% | 27% | +1.2% | +0.9% |
| Subset: S4 | 6276 | 27% | 26% | 28% | +1.2% | +0.8% |
| Tahun: 2019 | 683 | 25% | 21% | 25% | +2.7% | +2.0% |
| Tahun: 2020 | 3327 | 38% | 37% | 39% | +3.8% | +2.5% |
| Tahun: 2021 | 3952 | 24% | 24% | 25% | +0.8% | +0.6% |
| Tahun: 2022 | 3714 | 25% | 25% | 25% | -0.2% | -0.0% |
| Tahun: 2023 | 3976 | 24% | 22% | 24% | +1.4% | +1.1% |
| Tahun: 2024 | 4010 | 22% | 21% | 22% | +0.6% | +0.2% |
| Tahun: 2025 | 4320 | 29% | 29% | 30% | +0.8% | +0.7% |
| Tahun: 2026 | 2268 | 34% | 33% | 33% | +1.9% | +1.9% |
| Tanpa 2020 | 22923 | 26% | 25% | 26% | +0.9% | +0.7% |

## 5. Kriteria
| Kriteria | Nilai | Lulus |
|---|---|---|
| A. MACD sahaja lebih baik daripada rawak ≥ 5 mata (Berjaya) | -0.5 mata | ❌ |
| A. Gagal teruk lebih rendah daripada rawak | 39% vs 38% | ❌ |
| B. Tunggu lengkap lebih baik daripada A ≥ 5 mata (Berjaya) | -0.9 mata | ❌ |
| B. Gagal teruk lebih rendah daripada A | 39% vs 39% | ✅ |



---

<!-- FAIL ASAL: laporan/P01_peringkat3.md -->
# P01 — Peringkat 3: Varian V0–V5 (431 saham)

**Tarikh:** 10 Okt 2026 · **Enjin:** `standard/enjin_p01.py` v1.1 · **Laporan:** `standard/lapor_p01_p3.py` · **Data:** dataset_S1–S4, 2019–2026

**Verdict: SEMUA 6 VARIAN GAGAL. Peringkat 4 tidak diperlukan.** Tiada varian yang mengatasi hari rawak (ditapis dengan syarat yang sama) walaupun 5 mata. Beza terbaik ialah V0 (turutan asal pengguna, MA10>MA20 menyala dahulu): +1.7 mata (30% vs 28%), jauh di bawah ambang +5 mata. Penapis pasaran (SPY > MA200) dan trend (> MA150) tidak membantu; kedua-duanya sedikit lebih rendah daripada rawak.

| Penemuan | Bukti |
|---|---|
| Tiada keadaan di mana corak ini berkesan | Beza semua varian −1.7 hingga +1.7 mata; 0/4 subset mencapai +5 mata |
| V0 (turutan asal) paling baik tetapi tidak cukup | 30% vs 28%; gagal teruk 39% vs 38% |
| Calon `M1 → A1 → R1+Q3` | 38% dalam V1/V2 (155 kejadian), tetapi 31% dalam V4 dan gagal teruk hanya 36% vs 38% rawak. **Tidak disahkan**; kemungkinan kebetulan. (V3: 0 kerana label turutan berubah apabila D1 dimasukkan) |
| Definisi V0 | Tiada isyarat teras sudah aktif sebelum MACD hijau; MA10>MA20 menyala sebelum atau serentak dengan RSI>50 dan squeeze hijau |

**Kesimpulan P01 (Peringkat 1–3):** Gabungan MACD hijau, MA10>MA20, RSI>50 dan squeeze hijau **tidak memberi kelebihan masuk** berbanding hari rawak dalam 431 saham Shariah, dalam mana-mana turutan, tetingkap, atau keadaan pasaran yang diuji. Satu-satunya penemuan berguna ialah isyarat amaran: MACD hijau yang tidak disusuli isyarat lain dalam 20 hari (13% berjaya, 63% gagal teruk).

---

# P01 — Peringkat 3: Varian V0–V5 (431 saham)

Setiap varian dibandingkan dengan **hari rawak yang ditapis dengan syarat yang sama** (contoh V4: hari rawak semasa SPY > MA200). Ufuk 60 hari penuh; tanpa gap > 15%.

## 1. Ringkasan
| Varian | Bil. lengkap | Berjaya | Berjaya rawak | Beza (mata) | Gagal teruk | Gagal teruk rawak | Berjaya MACD sahaja | Purata E0 | Median E0 | Median naik maks |
|---|---|---|---|---|---|---|---|---|---|---|
| V0 Turutan asal (MA10>MA20 dahulu) | 1285 | 30% | 28% | +1.7 | 39% | 38% | 28% | +1.7% | -1.0% | +14.9% |
| V1 Asas (20 hari) | 19863 | 27% | 28% | -1.4 | 39% | 38% | 28% | +1.0% | -1.3% | +12.3% |
| V2 Lengkap dalam 10 hari | 18968 | 27% | 28% | -1.7 | 39% | 38% | 28% | +0.9% | -1.3% | +12.2% |
| V3 Tambah +DI>−DI | 19333 | 27% | 28% | -1.6 | 39% | 38% | 28% | +1.0% | -1.3% | +12.3% |
| V4 SPY > MA200 | 16680 | 25% | 27% | -1.3 | 39% | 38% | 26% | +0.6% | -1.4% | +11.6% |
| V5 Harga > MA150 | 14281 | 26% | 27% | -0.8 | 39% | 37% | 26% | +0.8% | -1.3% | +11.7% |

## 2. Kestabilan (% Berjaya: varian / rawak)
| Varian | 2019–2023 | 2024–2026 | Subset ≥ +5 mata | Tanpa 2020 |
|---|---|---|---|---|
| V0 Turutan asal (MA10>MA20 dahulu) | 30% / 28% | 30% / 28% | 0/4 | 27% / 26% |
| V1 Asas (20 hari) | 27% / 28% | 27% / 28% | 0/4 | 25% / 26% |
| V2 Lengkap dalam 10 hari | 26% / 28% | 27% / 28% | 0/4 | 25% / 26% |
| V3 Tambah +DI>−DI | 27% / 28% | 27% / 28% | 0/4 | 25% / 26% |
| V4 SPY > MA200 | 25% / 26% | 26% / 27% | 0/4 | 24% / 26% |
| V5 Harga > MA150 | 26% / 26% | 26% / 27% | 0/4 | 24% / 25% |

## 3. Gate
| Varian | ≥100 kejadian | ≥ +5 mata vs rawak | Gagal teruk < rawak | +5 mata dalam kedua-dua tempoh | ≥ 3/4 subset | Keputusan |
|---|---|---|---|---|---|---|
| V0 Turutan asal (MA10>MA20 dahulu) | ✅ | ❌ | ❌ | ❌ | ❌ | GAGAL |
| V1 Asas (20 hari) | ✅ | ❌ | ❌ | ❌ | ❌ | GAGAL |
| V2 Lengkap dalam 10 hari | ✅ | ❌ | ❌ | ❌ | ❌ | GAGAL |
| V3 Tambah +DI>−DI | ✅ | ❌ | ❌ | ❌ | ❌ | GAGAL |
| V4 SPY > MA200 | ✅ | ❌ | ❌ | ❌ | ❌ | GAGAL |
| V5 Harga > MA150 | ✅ | ❌ | ❌ | ❌ | ❌ | GAGAL |

## 4. Semakan calon Peringkat 1: turutan `M1 → A1 → R1+Q3`
| Varian | Bil. | Berjaya | Berjaya rawak | Gagal teruk |
|---|---|---|---|---|
| V0 Turutan asal (MA10>MA20 dahulu) | 155 | 38% | 28% | 36% |
| V1 Asas (20 hari) | 155 | 38% | 28% | 36% |
| V2 Lengkap dalam 10 hari | 151 | 38% | 28% | 36% |
| V3 Tambah +DI>−DI | 0 | – | 28% | – |
| V4 SPY > MA200 | 102 | 31% | 27% | 41% |
| V5 Harga > MA150 | 34 | 41% | 27% | 18% |



---

<!-- FAIL ASAL: laporan/P01_peringkat4_eksplorasi.md -->
# P01 — Eksplorasi: peraturan keluar amaran + carian isyarat tambahan (431 saham)

**Tarikh:** 10 Okt 2026 · **Skrip:** `standard/p01_e5.py`, `standard/p01_ciri.py` (guna `standard/enjin_p01.py` v1.1) · **Data:** dataset_S1–S4, 2019–2026 · **Status:** EKSPLORASI (bukan ujian dikunci awal; semua penemuan perlu disahkan semula)

**Verdict: TIADA isyarat yang boleh digunakan.** (1) Peraturan keluar amaran mengurangkan untung, bukan menambah. (2) Daripada 12 ciri × 5 kuintil × 2 jenis isyarat (118 sel), isyarat MACD tidak mengatasi hari rawak dalam kuintil yang sama; satu-satunya sel yang lulus (pantulan selepas jatuh 20 hari) bergantung pada 2020 dan hilang tanpa 2020. (3) Perbezaan hasil yang besar datang daripada **kemeruapan saham** (ATR%), bukan daripada masa masuk, dan ia rapuh.

## 1. Peraturan keluar amaran (E5)
Masuk buka hari selepas MACD hijau. Keluar jika A1, R1, Q3 belum lengkap dalam N hari; selepas lengkap, keluar asas. Henti −8% untuk E1/E3.

| N | Asas | Purata untung | Median | % ≥ +10% | % rugi ≤ −8% | Median hari | Tanpa amaran (purata) | Rawak (purata) |
|---|---|---|---|---|---|---|---|---|
| 5 | E0 | +0.6% | −1.1% | 9% | 8% | 5 | +1.3% | +0.8% |
| 10 | E0 | +1.1% | −1.4% | 13% | 10% | 10 | +1.3% | +0.8% |
| 20 | E0 | +1.2% | −1.5% | 14% | 11% | 11 | +1.3% | +0.8% |
| 5 | E3 | +1.5% | −1.9% | 13% | 16% | 9 | +2.4% | +2.6% |
| 10 | E3 | +2.1% | −2.7% | 17% | 19% | 16 | +2.4% | +2.6% |
| 20 | E3 | +2.1% | −3.0% | 17% | 20% | 18 | +2.4% | +2.6% |

Amaran memotong pemenang lebih banyak daripada ia mengelak kerugian. Semua kombinasi ≤ versi tanpa amaran. **GAGAL.**

## 2. Ciri pada hari isyarat (kuintil daripada hari rawak 2019–2023)
Ciri: RSI, ROC 20/63/126 hari, jarak MA50, jarak MA150, jarak high 52 minggu, ATR%, nisbah volum, lebar BB, ADX, nilai dagangan 20 hari.

| Soalan | Jawapan |
|---|---|
| Adakah MACD hijau / isyarat lengkap lebih baik daripada rawak dalam kuintil yang sama? | ❌ Median beza −0.6 mata (2019–23) dan −0.1 mata (2024–26). 1 daripada 118 sel lulus ≥ +5 mata dalam kedua-dua tempoh, iaitu jumlah yang dijangka berlaku secara kebetulan |
| Sel yang lulus: isyarat lengkap selepas harga jatuh > 7% dalam 20 hari | 182 kejadian, 45% vs 35% rawak; tetapi 65 kejadian dalam 2020. **Tanpa 2020: 39% vs 34%, purata E3 +3.9% vs +3.0%, gagal teruk lebih tinggi (42% vs 39%). DITOLAK** |
| Ciri mana yang benar-benar mengubah hasil? | Kemeruapan. ATR% kuintil 5 (> 5%): 46% naik ≥20%, tetapi gagal teruk juga 41%. Lebar BB dan ROC ekstrem (kedua-dua hujung) menunjukkan kesan sama: saham yang bergerak besar bergerak besar ke **kedua-dua** arah |

## 3. Kemeruapan + keluar 3×ATR (hari rawak, tanpa isyarat)
| Kuintil ATR% | Purata untung E3 | Median | % ≥ +10% | % rugi ≤ −8% |
|---|---|---|---|---|
| 1 (< 2.3%) | +0.7% | −1.9% | 13% | 8% |
| 3 | +1.6% | −3.4% | 19% | 27% |
| 5 (> 5%) | +7.2% (+6.6% tanpa saham bermasalah data) | −5.9% | 26% | 40% |

Rapuh: tanpa 2020 hanya +4.4%; 2022 −0.8%, 2024 +1.1%; median sentiasa negatif (sebahagian besar dagangan rugi, beberapa pemenang besar menarik purata). Bias kemandirian memihak saham meruap (yang muflis tiada dalam senarai). **Bukan isyarat masuk; tidak disyorkan tanpa ujian portfolio penuh.**

## 4. Isu data ditemui
Saham dengan lonjakan harian > +100% atau < −60% (kemungkinan peristiwa korporat tidak terlaras): ASST, FCEL, MTDR, OVV, PR, SM, VAL, XENE. VAL melonjak +7,082% pada 3 Mei 2021 (penyenaraian semula selepas muflis). Keputusan P01 Peringkat 1–3 disemak semula tanpa saham ini: **tiada perubahan** (contoh: berjaya MACD sahaja 27.6% → 27.4%; rawak 28.1% → 28.0%).

## Kesimpulan keseluruhan P01
MACD, MA10/MA20, RSI, squeeze, DMI dan 12 ciri tambahan **tidak memberi kelebihan masa masuk** dalam set 431 saham Shariah. Masa masuk berasaskan indikator ini setara dengan masuk rawak. Perbezaan hasil ditentukan terutamanya oleh **pemilihan saham (kemeruapan)** dan **cara keluar**, bukan isyarat masuk.


---

<!-- FAIL ASAL: laporan/P02_peringkat1.md -->
# P02 — Peringkat 1: V1 saham peneraju RS + masa masuk (431 saham)

**Tarikh:** 10 Okt 2026 · **Enjin:** `standard/enjin_p02.py` v1.1 · **Laporan:** `standard/lapor_p02.py` · **Data:** dataset_S1–S4 (423 saham; 8 saham bermasalah data dibuang), Dis 2019–2026 · **Spesifikasi:** `spec/P02_rs_peneraju.md`

**Verdict: GAGAL (L1, L2, L3 gagal; L4, L5 lulus).** Saham RS 20% teratas kelihatan lebih kerap naik ≥20% (34% vs 28% semua saham), tetapi **hampir semua kelebihan itu datang daripada kemeruapan**: saham RS teratas dan terbawah kedua-duanya lebih meruap. Selepas diselaraskan ikut ATR%, RS teratas hanya +2 mata (30% vs 28%) dan purata untung K3 **sama** (+2.5% vs +2.5%). Masa masuk (MACD hijau, RS paras tertinggi baharu) tidak menambah nilai dalam kolam RS teratas.

| Penemuan | Bukti |
|---|---|
| Kesan pilihan saham (mentah) | B1 − C0 = +4.8 / +6.6 mata (penemuan / pengesahan); purata K3 +0.6 / +0.7 mata. Hampir lulus L1 |
| Kesan pilihan saham (selaras ATR%) | B1 30% vs C0 28%; purata K3 +2.5% vs +2.5%. **Tiada kelebihan untung** |
| Mengapa? | 28% kejadian B1 dalam kuintil ATR% tertinggi (C0: 20%). C1 (RS terbawah) juga 32% berjaya mentah kerana 34% dalam kuintil ATR% tertinggi |
| Masa masuk dalam kolam | B2 (MACD) −1.9 / −1.9 mata vs B1; B3 (RS paras tertinggi baharu) −1.8 / −1.0 mata; 0/4 subset. **Tiada nilai tambah** |
| Gagal teruk | B1 40%, B3 40% vs C0 38% (lebih teruk) |
| **Penemuan berguna: elak RS terbawah** | Selepas selaras ATR%, C1 (20% terbawah) purata K3 +1.3% vs C0 +2.4%; lebih rendah dalam 7/8 hirisan (kedua-dua tempoh, hingga 2025, tanpa 2020, S1–S3; S4 hampir sama). Ini penapis **elak**, bukan isyarat beli |
| V0 (I03 tulen, tanpa henti, tanpa portfolio) | 4,173 dagangan (I03: 4,220), purata +1.5%, median −1.5%, 13% ≥ +10%. CAGR 32% I03 datang daripada ranking portfolio dan 2025–2026, bukan daripada purata isyarat |
| Sensitiviti 8 saham bermasalah | Disertakan semula: tiada perubahan arah (B1 33.7%, C0 28.1%) |

**Pembetulan kaedah (didedahkan):** v1.0 mengikat bilangan hari rawak kepada bilangan isyarat setiap saham, jadi saham tanpa isyarat tiada dalam C0/C1 dan saham banyak isyarat terlebih wakil (C0 = 34%). v1.1 mengambil sampel seragam 5% daripada hari layak setiap saham. Ini pembetulan pensampelan, bukan perubahan peraturan; laporan di bawah ialah v1.1.

**Pelarasan ATR%:** purata berwajaran ikut taburan kuintil ATR% (22 hari, pada hari isyarat) kumpulan C0; analisis tambahan, bukan sebahagian kriteria dikunci.

---

# P02 — Laporan V1

Ufuk 60 hari penuh; tanpa gap > 15%. K1 = MACD merah, K2 = tutup < SMA20, K3 = 3×ATR22; semua dengan henti −8%.

## 1. Kumpulan (ufuk 60 hari)
| Kumpulan | Bil. | Berjaya ≥20% | Sederhana | Gagal <10% | Gagal teruk | Median naik maks | Purata K1 | Purata K2 | Purata K3 | % K3 ≥ +10% | Median hari K3 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 Rawak, semua saham | 31368 | 28% | 22% | 11% | 38% | +12.7% | +0.6% | +0.6% | +2.5% | 19% | 22 |
| B1 Rawak, RS teratas | 6325 | 34% | 20% | 6% | 40% | +15.7% | +0.7% | +1.2% | +3.1% | 21% | 21 |
| B2 MACD hijau, RS teratas | 5200 | 32% | 19% | 6% | 43% | +14.8% | +1.2% | +1.2% | +2.5% | 20% | 20 |
| B3 RS paras tertinggi baharu | 3822 | 32% | 22% | 7% | 40% | +15.0% | +0.7% | +1.3% | +2.6% | 20% | 21 |
| C1 Rawak, RS terbawah | 6225 | 32% | 19% | 7% | 43% | +14.9% | +0.6% | +0.2% | +2.1% | 19% | 20 |

## 2. Cara keluar
| Kumpulan | Keluar | Purata | Median | % untung | % ≥ +10% | % rugi ≤ −8% | Median hari |
|---|---|---|---|---|---|---|---|
| B1 Rawak, RS teratas | K1 | +0.7% | -0.4% | 45% | 7% | 7% | 2 |
| B1 Rawak, RS teratas | K2 | +1.2% | -1.0% | 39% | 9% | 8% | 4 |
| B1 Rawak, RS teratas | K3 | +3.1% | -4.1% | 38% | 21% | 31% | 21 |
| B2 MACD hijau, RS teratas | K1 | +1.2% | -1.8% | 37% | 14% | 13% | 8 |
| B2 MACD hijau, RS teratas | K2 | +1.2% | -2.0% | 35% | 12% | 11% | 8 |
| B2 MACD hijau, RS teratas | K3 | +2.5% | -4.6% | 36% | 20% | 33% | 20 |
| B3 RS paras tertinggi baharu | K1 | +0.7% | -0.9% | 42% | 10% | 11% | 6 |
| B3 RS paras tertinggi baharu | K2 | +1.3% | -2.0% | 37% | 15% | 15% | 11 |
| B3 RS paras tertinggi baharu | K3 | +2.6% | -3.9% | 37% | 20% | 30% | 21 |

## 3. Kestabilan (% Berjaya; purata K3)
| Kumpulan | Bil. B1 | C0 | B1 | B2 | B3 | C1 | K3 C0 | K3 B1 | K3 B3 |
|---|---|---|---|---|---|---|---|---|---|
| Tempoh: penemuan | 3720 | 28% | 33% | 31% | 31% | 32% | +2.2% | +2.8% | +2.8% |
| Tempoh: pengesahan | 2605 | 28% | 34% | 32% | 33% | 32% | +2.8% | +3.5% | +2.2% |
| Subset: S1 | 1466 | 28% | 30% | 31% | 29% | 32% | +2.6% | +3.3% | +4.4% |
| Subset: S2 | 1818 | 29% | 35% | 32% | 31% | 33% | +2.4% | +2.6% | +1.0% |
| Subset: S3 | 1621 | 26% | 35% | 32% | 35% | 28% | +2.1% | +3.1% | +2.1% |
| Subset: S4 | 1420 | 28% | 34% | 32% | 33% | 34% | +2.9% | +3.5% | +3.4% |
| Tahun: 2020 | 884 | 40% | 43% | 40% | 41% | 42% | +6.7% | +5.9% | +6.3% |
| Tahun: 2021 | 905 | 26% | 28% | 27% | 23% | 25% | +1.7% | +1.0% | -1.2% |
| Tahun: 2022 | 926 | 24% | 31% | 29% | 30% | 31% | -1.1% | -0.0% | +0.5% |
| Tahun: 2023 | 1005 | 23% | 30% | 29% | 27% | 30% | +2.0% | +4.2% | +5.1% |
| Tahun: 2024 | 1026 | 23% | 27% | 26% | 23% | 28% | +0.9% | +1.1% | +1.7% |
| Tahun: 2025 | 1031 | 30% | 41% | 37% | 39% | 35% | +4.4% | +7.0% | +3.1% |
| Tahun: 2026 | 548 | 33% | 36% | 35% | 39% | 34% | +3.5% | +1.3% | +1.5% |
| Hingga Dis 2025 | 5777 | 28% | 33% | 31% | 31% | 32% | +2.4% | +3.2% | +2.7% |
| Tanpa 2020 | 5441 | 26% | 32% | 30% | 30% | 30% | +1.8% | +2.6% | +1.8% |

## 4. Kriteria lulus
| Kriteria | Nilai | Lulus |
|---|---|---|
| L1 Pilihan saham: B1 − C0 ≥ 5 mata DAN purata K3 lebih tinggi, kedua-dua tempoh | +4.8 / +6.6 mata; K3 +0.6% / +0.7% | ❌ |
| L2 Masa masuk B2: B2 − B1 ≥ 5 mata kedua-dua tempoh & ≥ 3/4 subset | -1.9 / -1.9 mata; subset 0/4 | ❌ |
| L2 Masa masuk B3: B3 − B1 ≥ 5 mata kedua-dua tempoh & ≥ 3/4 subset | -1.8 / -1.0 mata; subset 0/4 | ❌ |
| L3 Gagal teruk B1 < C0 | 40% vs 38% | ❌ |
| L3 Gagal teruk B3 < C0 | 40% vs 38% | ❌ |
| L4 Arah B1 > C0 kekal hingga Dis 2025 | +5.7 mata | ✅ |
| L4 Arah B1 > C0 kekal tanpa 2020 | +6.0 mata | ✅ |
| L5 C1 lebih lemah daripada B1 | 32% vs 34% | ✅ |

## 5. V0 — peraturan I03 tulen (RS di paras tertinggi setiap hari, keluar tutup < SMA20 tanpa henti)
| Bil. | Purata untung | Median | % ≥ +10% | % rugi ≤ −8% | Median hari | Berjaya (60 hari) |
|---|---|---|---|---|---|---|
| 4173 | +1.5% | -1.5% | 13% | 12% | 12 | 29% |



---

<!-- FAIL ASAL: laporan/P02_varian_V2-V5.md -->
# P02 — Varian V2–V5 (431 saham)

**Tarikh:** 10 Okt 2026 · **Enjin:** `standard/enjin_p02.py` v1.2 · **Semakan selaras ATR%:** `standard/p02_selaras.py` · **Data:** dataset_S1–S4 (423 saham; 8 bermasalah dibuang), Dis 2019–2026

**Verdict: SEMUA VARIAN GAGAL ikut kriteria dikunci.** V2 (10% teratas) dan V4 (SPY > MA200) lulus L1 secara mentah, tetapi semua varian gagal L2 (masa masuk tidak menambah nilai) dan L3 (gagal teruk lebih tinggi daripada C0). Selepas diselaraskan ikut kemeruapan, kelebihan pilihan saham RS tinggal **+0.3 hingga +0.4 mata peratus untung setiap dagangan** pada varian terbaik, dan +3 hingga +4 mata kadar naik ≥ 20% (di bawah ambang +5).

## 1. Keputusan mentah (ufuk 60 hari)
| Varian | Bil. B1 | Berjaya B1 / C0 (mentah) | Gagal teruk B1 / C0 | Purata K3 B1 / C0 | Berjaya B3 | Keputusan (kriteria dikunci) |
|---|---|---|---|---|---|---|
| V1 Asas (RS12, 20% teratas) | 6325 | 34% / 28% | 40% / 38% | +3.1% / +2.5% | 32% | GAGAL (L1 L2 L3) |
| V2 10% teratas | 3140 | 38% / 28% | 40% / 38% | +3.9% / +2.6% | 36% | GAGAL (L2 L3) |
| V3 RS 6 bulan | 6836 | 33% / 28% | 40% / 38% | +2.6% / +2.5% | 31% | GAGAL (L1 L2 L3) |
| V4 SPY > MA200 | 5046 | 34% / 26% | 40% / 38% | +2.9% / +1.9% | 32% | GAGAL (L2 L3) |
| V5 RS berpemberat | 6313 | 34% / 28% | 41% / 38% | +2.9% / +2.3% | 32% | GAGAL (L1 L2 L3) |

## 2. Selepas diselaraskan ikut kuintil ATR% (taburan C0)
| Varian | Potongan | Berjaya B1 sel. / C0 | Purata K3 B1 sel. / C0 | Purata K3 C1 sel. | Subset K3 B1 > C0 |
|---|---|---|---|---|---|
| V1 | semua | 30% / 28% | +2.5% / +2.5% | +1.3% | 3/4 |
| V1 | penemuan | 30% / 28% | +2.2% / +2.2% | +1.3% | 3/4 |
| V1 | pengesahan | 30% / 28% | +2.7% / +2.8% | +1.2% | 2/4 |
| V1 | tanpa2020 | 29% / 26% | +2.1% / +1.8% | +0.8% | 3/4 |
| V2 | semua | 32% / 28% | +2.9% / +2.6% | +1.7% | 3/4 |
| V2 | penemuan | 31% / 29% | +2.4% / +2.5% | +1.9% | 2/4 |
| V2 | pengesahan | 36% / 28% | +4.0% / +2.6% | +1.3% | 1/4 |
| V2 | tanpa2020 | 32% / 26% | +3.1% / +1.9% | +1.1% | 3/4 |
| V3 | semua | 29% / 28% | +2.1% / +2.5% | +1.0% | 1/4 |
| V3 | penemuan | 28% / 28% | +1.7% / +2.3% | +1.2% | 0/4 |
| V3 | pengesahan | 31% / 28% | +2.9% / +2.7% | +1.0% | 3/4 |
| V3 | tanpa2020 | 28% / 26% | +1.5% / +1.8% | +0.8% | 1/4 |
| V4 | semua | 30% / 26% | +2.3% / +1.9% | +1.3% | 4/4 |
| V4 | penemuan | 30% / 25% | +2.4% / +1.6% | +1.6% | 4/4 |
| V4 | pengesahan | 31% / 28% | +2.2% / +2.2% | +0.9% | 2/4 |
| V4 | tanpa2020 | 29% / 25% | +2.1% / +1.7% | +1.0% | 4/4 |
| V5 | semua | 30% / 28% | +2.0% / +2.3% | +1.6% | 1/4 |
| V5 | penemuan | 29% / 28% | +1.3% / +2.2% | +2.0% | 1/4 |
| V5 | pengesahan | 31% / 28% | +2.9% / +2.6% | +1.1% | 2/4 |
| V5 | tanpa2020 | 29% / 26% | +1.8% / +1.7% | +1.3% | 2/4 |

## 3. Tafsiran
| Penemuan | Bukti | Status |
|---|---|---|
| Varian paling konsisten: **V4 (RS 20% teratas + SPY > MA200)** | Selaras ATR: berjaya 30% vs 26%; K3 +2.3% vs +1.9%; kedua-dua tempoh positif (+4.5 / +3.0 mata); 4/4 subset K3 lebih tinggi; tanpa 2020 +4.0 mata | Kelebihan kecil, konsisten, **di bawah ambang +5 mata**; gagal teruk sama (38%) |
| V2 (10% teratas) | Selaras ATR: berjaya 32% vs 28%, K3 +2.9% vs +2.6%; tetapi tempoh penemuan hampir tiada (+2 mata, K3 −0.1%) dan pengesahan besar (+8.5 mata) | Tidak konsisten ikut masa |
| V3 (RS 6 bulan), V5 (berpemberat) | Selaras ATR: K3 ≤ C0; 1/4 subset | Tiada kelebihan |
| Masa masuk (B2 MACD, B3 RS paras tertinggi baharu) | Lebih rendah daripada rawak dalam kolam dalam **semua** varian | Ditolak |
| **Elak RS 20% terbawah (C1)** | Selaras ATR: K3 C1 lebih rendah daripada C0 dalam **20/20** potongan (beza terkecil V4 penemuan); purata +0.8% hingga +2.0% vs +1.6% hingga +2.8% | **Penemuan paling teguh P02** — penapis elak, bukan isyarat beli |

**Pembetulan:** v1.2 membetulkan ralat jenis data `spy_ok` yang menyebabkan V4 gagal dijalankan; varian lain tidak terjejas.

## 4. Kesimpulan P02
Pilihan saham RS memberi kelebihan **kecil** dan sebahagian besarnya ialah kesan kemeruapan. Gabungan "RS 20% teratas semasa pasaran menaik" (V4) paling konsisten, tetapi tidak mencapai ambang yang dikunci. Masa masuk dalam kolam RS tidak membantu. Peraturan paling berguna: **jangan beli saham dalam 20% RS terbawah.**


---

<!-- FAIL ASAL: laporan/RINGKASAN_I01-I32.md -->
# Ringkasan Backtest Indikator I01–I32 (enjin v1.2)

Tarikh ringkasan: 2026-10-07 · Sumber: `registry/I01.csv`–`registry/I32.csv` dan `laporan/I01.md`–`laporan/I32.md` · Tiada pengiraan semula; semua angka disalin daripada fail sedia ada.

## 0. Status fail

- **32/32 kod lengkap.** Setiap kod ada fail registry dan laporan, dan setiap satu ialah larian V0 penuh atas set 431 + S1–S4. Tiada kod yang tertinggal atau gagal dijalankan.
- Satu-satunya kes "hampir kosong" ialah **I28 (proksi VCP)**. Ia berjalan dengan betul tetapi hanya memberi 3 dagangan di 431, dan 0 dagangan di S2 dan S4. Laporan menyebut sebabnya: syarat ATR10/ATR50 < 0.6 hampir tidak pernah berlaku serentak dengan hari pecahan bervolum tinggi.
- **Semua 32 indikator DITOLAK secara rasmi.** Puncanya G1: exit seragam tiada henti rugi harga. Oleh itu lajur `skor` rasmi kosong bagi semua kod. Papan kedudukan di bawah disusun mengikut **`skor_tanpa_gate`**, iaitu skor v1.2 dengan gate diabaikan, seperti yang tercatat dalam registry.

Takrif lajur (semua angka set 431):

- **Pegang** ialah purata hari pegangan.
- **>SB** bermaksud CAGR mengatasi penanda aras sama berat 431 (21.9%).
- **Konsisten** bermaksud lulus G2–G6 (G1 diabaikan) di keempat-empat S1–S4. Kurungan menunjukkan berapa subset lulus.
- **Dagangan** ialah semua dagangan calon (konvensyen enjin), bukan hanya yang diisi slot.

## a. Papan kedudukan

| # | Kod | Indikator | Dagangan | % Menang | % capai +10% | Pegang (h) | CAGR | Max DD | >SB? | Konsisten? | Skor |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | I12 | MACD lintas isyarat (MACD>0) | 9,608 | 33.8 | 28.5 | 14.2 | 35.1% | −33.6% | Ya | Tidak (1/4) | 66.4 |
| 2 | I22 | Parabolic SAR | 27,113 | 34.4 | 20.9 | 9.9 | 28.8% | −32.2% | Ya | Tidak (1/4) | 58.4 |
| 3 | I03 | Garis RS vs SPY (tinggi 252h) | 4,220 | 39.0 | 32.9 | 15.7 | 32.1% | −36.9% | Ya | Tidak (3/4) | 56.8 |
| 4 | I32 | Volum relatif RVOL ≥2× | 9,218 | 39.5 | 24.5 | 11.1 | 29.4% | −35.6% | Ya | Tidak (2/4) | 56.7 |
| 5 | I16 | Williams %R lintas −20 | 23,174 | 33.5 | 29.1 | 13.9 | 27.0% | −27.7% | Ya | Tidak (1/4) | 56.5 |
| 6 | I29 | OBV tinggi 63h | 12,229 | 35.9 | 27.1 | 13.7 | 31.1% | −37.4% | Ya | Tidak (2/4) | 54.9 |
| 7 | I14 | RSI14 lintas 60 | 16,253 | 36.0 | 31.8 | 15.7 | 26.7% | −34.6% | Ya | Tidak (2/4) | 54.8 |
| 8 | I27 | TTM Squeeze | 8,461 | 36.7 | 29.4 | 14.6 | 24.1% | −38.5% | Ya | **Ya (4/4)** | 40.4 |
| 9 | I10 | Trend Template (MA) | 9,819 | 35.5 | 20.2 | 10.1 | 21.8% | −36.3% | Tidak | Tidak (1/4) | 39.6 |
| 10 | I26 | Saluran Keltner | 10,386 | 39.5 | 34.6 | 18.0 | 19.2% | −41.1% | Tidak | Tidak (1/4) | 39.3 |
| 11 | I18 | ADX + DI | 6,256 | 39.2 | 31.7 | 16.8 | 12.5% | −31.0% | Tidak | Tidak (0/4) | 32.7 |
| 12 | I31 | MFI lintas 50 | 28,466 | 35.6 | 19.8 | 9.3 | 22.7% | −43.1% | Ya | Tidak (0/4) | 32.2 |
| 13 | I07 | SMA10 × SMA20 | 18,207 | 35.2 | 26.6 | 12.6 | 18.2% | −36.7% | Tidak | Tidak (0/4) | 30.6 |
| 14 | I06 | Clenow cerun × R² | 1,853 | 36.1 | 25.5 | 11.1 | 13.1% | −35.8% | Tidak | Tidak (0/4) | 30.6 |
| 15 | I01 | Pulangan 12-1 bulan | 2,790 | 40.5 | 18.9 | 7.7 | 16.1% | −26.8% | Tidak | Tidak (0/4) | 30.1 |
| 16 | I23 | Donchian 20 | 14,009 | 37.8 | 33.4 | 16.8 | 17.9% | −32.8% | Tidak | Tidak (1/4) | 29.0 |
| 17 | I17 | Elder Impulse | 42,082 | 32.1 | 18.9 | 8.8 | 18.4% | −37.9% | Tidak | Tidak (1/4) | 27.5 |
| 18 | I02 | Dekat tinggi 52 minggu | 9,314 | 35.2 | 25.9 | 13.4 | 10.1% | −24.2% | Tidak | Tidak (1/4) | 27.2 |
| 19 | I08 | EMA20 × EMA50 | 6,526 | 38.4 | 32.2 | 15.7 | 16.9% | −41.2% | Tidak | Tidak (1/4) | 27.0 |
| 20 | I30 | CMF lintas +0.1 | 18,498 | 36.9 | 22.4 | 10.8 | 10.7% | −44.2% | Tidak | Tidak (0/4) | 26.6 |
| 21 | I25 | Bollinger pecah selepas sempit | 2,347 | 33.2 | 28.7 | 14.5 | 11.2% | −36.6% | Tidak | Tidak (0/4) | 25.9 |
| 22 | I11 | Peringkat 2 Weinstein | 5,719 | 39.0 | 19.4 | 9.4 | 17.5% | −35.6% | Tidak | Tidak (3/4) | 25.8 |
| 23 | I13 | Histogram MACD berbalik | 33,210 | 40.7 | 10.1 | 5.0 | 20.1% | −59.3% | Tidak | Tidak (0/4) | 25.7 |
| 24 | I20 | Supertrend (10,3) | 10,278 | 37.2 | 33.7 | 16.5 | 11.4% | −52.5% | Tidak | Tidak (1/4) | 25.6 |
| 25 | I19 | Aroon (25) | 14,489 | 36.2 | 26.5 | 13.0 | 17.9% | −44.6% | Tidak | Tidak (1/4) | 25.3 |
| 26 | I04 | Mansfield RS | 7,421 | 38.3 | 22.4 | 11.2 | 9.7% | −45.2% | Tidak | Tidak (0/4) | 25.0 |
| 27 | I24 | Kotak Darvas | 2,369 | 34.5 | 29.1 | 16.1 | 12.0% | −35.2% | Tidak | Tidak (0/4) | 24.7 |
| 28 | I21 | Ichimoku | 7,280 | 37.1 | 29.0 | 14.7 | 2.3% | −39.9% | Tidak | Tidak (0/4) | 18.6 |
| 29 | I09 | Golden Cross 50/200 | 2,160 | 34.9 | 20.6 | 11.0 | 3.2% | −51.6% | Tidak | Tidak (0/4) | 11.3 |
| 30 | I05 | ROC63 lintas +20% | 9,088 | 36.2 | 23.3 | 11.7 | 1.3% | −49.0% | Tidak | Tidak (0/4) | 9.2 |
| 31 | I28 | VCP (proksi) | 3 | 0.0 | 0.0 | 8.7 | −0.1% | −0.7% | Tidak | Tidak (0/4) | 7.5 |
| 32 | I15 | Stochastic <20 | 21,189 | 47.9 | 4.8 | 2.4 | −3.3% | −59.8% | Tidak | Tidak (0/4) | 3.1 |

I07 dan I06 seri pada 30.6; I07 diletakkan di atas kerana CAGRnya lebih tinggi. Penanda aras dalam tempoh yang sama: SPY 15.9%, QQQ 21.7%, sama berat 431 21.9% (MDD −40.3%).

**Hakikat utama:**

- Tiada satu indikator pun mencapai skor 60 (ambang UJI KERTAS) walaupun G1 diabaikan, kecuali I12 (66.4).
- Hanya 9/32 mengalahkan sama berat 431.
- Hanya I27 lulus G2–G6 di keempat-empat subset.

## b. 5 teratas — gate demi gate (set 431)

| Gate | I12 MACD | I22 PSAR | I03 RS | I32 RVOL | I16 %R |
|---|---|---|---|---|---|
| G1 henti rugi harga | ❌ | ❌ | ❌ | ❌ | ❌ |
| G2 ≥100 dagangan | ✅ 9,608 | ✅ 27,113 | ✅ 4,220 | ✅ 9,218 | ✅ 23,174 |
| G3 CAGR > SPY 15.9% | ✅ 35.1% | ✅ 28.8% | ✅ 32.1% | ✅ 29.4% | ✅ 27.0% |
| G4 MDD ≥ −45% | ✅ −33.6% | ✅ −32.2% | ✅ −36.9% | ✅ −35.6% | ✅ −27.7% |
| G5 dua separuh positif | ✅ 23.1/46.5 | ✅ 23.9/33.4 | ✅ 6.5/59.1 | ✅ 19.6/38.4 | ✅ 19.0/34.6 |
| G6 long & mekanikal | ✅ | ✅ | ✅ | ✅ | ✅ |
| Subset lulus (tanpa G1) | 1/4 | 1/4 | 3/4 | 2/4 | 1/4 |
| Subset kalahkan SB set sendiri | 0/4 | 1/4 | 1/4 | 1/4 | 0/4 |
| Skor (tanpa gate) | 66.4 | 58.4 | 56.8 | 56.7 | 56.5 |

Kelemahan setiap satu, menurut laporan masing-masing:

- **I12 MACD:** paling kuat di 431, tetapi 10 dagangan terbaik menyumbang ≈61% untung. CAGR subset jatuh ke 7.7%–15.9%, dan setiap subset kalah sama berat setnya.
- **I22 PSAR:** apabila ranking dirawakkan, CAGR median hanya 13.9%. Kelebihannya datang daripada ranking ROC63, bukan daripada isyarat SAR. Median pegangan 5 hari, dan 35% dagangan keluar dalam ≤ 2 hari.
- **I03 RS:** CAGR hingga Dis 2025 hanya 19.9%, kerana 2026 YTD (+124%) mendominasi. Separuh 1 hanya 6.5%.
- **I32 RVOL:** paling stabil mengikut masa; CAGR hingga Dis 2025 sudah 26.0%. Tetapi subset S1 dan S4 gagal G5, dan S1/S4 juga gagal G4 atau G3.
- **I16 %R:** MDD terendah dalam 5 teratas (−27.7%) dan tiada tahun rugi. Tanpa APP, IREN dan AEHR, CAGR turun ke 21.8%, iaitu setara sama berat.

## c. Indikator yang gagal teruk

| Kod | Masalah utama |
|---|---|
| I15 Stochastic | CAGR −3.3%, MDD −59.8%. 95.8% dagangan keluar dalam ≤ 2 hari kerana isyarat oversold sentiasa di bawah SMA20. Gagal G1/G3/G4/G5. |
| I28 VCP proksi | Hanya 3 dagangan dalam ~7 tahun, semuanya rugi. Syarat proksi saling bercanggah. |
| I05 ROC63 +20% | CAGR 1.3%, MDD −49.0%. Ranking ROC63 terbalik. CAGR hingga 2025 −3.1%. |
| I09 Golden Cross | CAGR 3.2%, MDD −51.6%. Rugi 5/6 tahun penuh. Isyarat terlalu lewat. |
| I21 Ichimoku | CAGR 2.3%. Hampir tiada kelebihan isyarat. |
| I13 Histogram MACD | MDD −59.3%, dengan 4 tahun di bawah air. 70% isyarat sudah di bawah SMA20. |
| I04 Mansfield RS | CAGR 9.7%, MDD −45.2% (gagal G4). Menangkap saham yang baru pulih, bukan peneraju. |

Corak yang sama dalam semua kes ini: isyarat jenis **pembalikan/oversold** atau **lintasan lewat** bertembung dengan exit tutup<SMA20. Dagangan dijual dalam 2–3 hari sebelum isyarat sempat bekerja.

## d. Pemerhatian mengikut kumpulan

Purata skor dikira daripada nilai `skor_tanpa_gate` dalam registry.

| Kumpulan | Kod | Purata skor | Kalahkan SB | Pegangan tipikal |
|---|---|---|---|---|
| Volum | I29–I32 | 42.6 | 3/4 | 9–14 hari |
| Osilator | I12–I17 | 39.0 | 3/6 | 2–16 hari (bercampur) |
| Trend | I18–I22 | 32.1 | 1/5 | 10–17 hari |
| Kekuatan relatif / momentum | I01–I06 | 29.8 | 1/6 | 8–16 hari |
| Breakout / volatiliti | I23–I28 | 27.8 | 1/6 | 14–18 hari |
| Purata bergerak | I07–I11 | 26.9 | 0/5 | 9–16 hari |

Untuk matlamat "naik dan kekal naik beberapa minggu, sasaran +10%":

1. **Isyarat pengesahan momentum mengatasi isyarat pembalikan.** Contohnya RSI>60, %R>−20, MACD>0, garis RS di paras tinggi, dan volum 2× dengan tutup kuat. Isyarat ini berlaku ketika harga sudah di atas SMA20, jadi exit membiarkan dagangan berjalan: median 10–13 hari, dan 29–33% dagangan sempat capai +10%. Isyarat oversold (I13, I15) dan lintasan lewat (I04, I09, I11) dijual dalam 2–3 hari.
2. **Kumpulan volum (khususnya I32) dan osilator momentum (I12, I14, I16) paling sesuai.** Kekuatan relatif hanya bagus melalui I03. Purata bergerak ialah kumpulan paling lemah; tiada satu pun yang mengalahkan sama berat.
3. **Breakout harga (I23 Donchian, I26 Keltner, I20 Supertrend) memberi % capai +10% tertinggi (33–35%) dan pegangan terpanjang (16–18 hari).** Tetapi CAGR kalah sama berat. Isyaratnya baik untuk "kekal naik", tetapi tidak cukup tajam untuk memilih pemenang.
4. **Tiada indikator yang purata pulangannya mencecah +10% dalam 60 hari pegangan tetap** (kecuali I28, yang sampelnya hanya 2–3 dagangan). Sasaran +10% sebulan tercapai hanya dalam 10–20% bulan, walaupun bagi 5 teratas. Exit SMA20 tidak sepadan dengan matlamat pegangan sebulan.
5. **Hampir semua kelebihan di 431 bergantung pada kolam besar dan ranking ROC63.** Dalam subset (≈108 saham), hampir semua indikator kalah sama berat setnya. Beberapa keputusan bergantung pada satu dagangan (ASST bagi I27 dan I29) atau pada tahun 2026 (I03, I31, I07, I08, I19, I23, I26).

## e. Cadangan langkah seterusnya

1. **Tambah henti rugi harga dalam exit seragam** (contohnya −8% atau 2×ATR di bawah harga masuk). Tanpanya tiada kaedah boleh lulus G1, jadi semua perbandingan kekal "maklumat sahaja".
2. **Uji gabungan 2 indikator** (isyarat = kedua-dua benar dalam tetingkap 1–3 hari):
   - **I32 RVOL + I03 RS tinggi 252h:** lonjakan volum pada saham peneraju relatif. I32 paling stabil mengikut masa; I03 paling konsisten antara 5 teratas (3/4 subset).
   - **I32 RVOL + I12 MACD>0:** menapis isyarat MACD yang bising dengan pengesahan volum.
   - **I14 RSI>60 atau I16 %R + I03 RS:** pengesahan momentum hanya pada saham RS tinggi.
3. **Kurangkan kekerapan isyarat.** Isyarat 5 teratas berjumlah 600–3,900 setahun; S6 hanya mendapat 5/10 kerana melebihi 150 setahun. Tapis dengan syarat trend (tutup > SMA50) atau ranking RS sebelum masuk.
4. **Tambah penapis kecairan** (contohnya nilai dagangan purata 20 hari minimum) supaya dagangan seperti ASST tidak mengherotkan keputusan.
5. **Laporkan CAGR hingga Dis 2025 dan ujian ranking rawak sebagai lajur tetap dalam registry,** supaya kebergantungan pada 2026 atau pada ranking kelihatan terus dalam papan kedudukan.
6. **Selepas exit seragam ditetapkan,** uji varian exit (contohnya SMA50 atau trailing ATR) pada calon gabungan terbaik. Data pegangan tetap menunjukkan pulangan terus meningkat hingga 60 hari.

## Batasan

- Semua angka diambil terus daripada registry dan laporan; tiada pengiraan semula backtest. Purata skor kumpulan ialah purata aritmetik nilai `skor_tanpa_gate` dalam registry.
- Bias kemandirian (senarai Shariah hari ini) dan peristiwa korporat yang tidak terlaras (SNX, ASST) ada dalam semua ujian, seperti dicatat dalam setiap laporan.
- "Dagangan" ialah dagangan calon. Portfolio 8 slot hanya mengisi sebahagian (contohnya I22 diisi 1,368 daripada 27,113).


---

<!-- FAIL ASAL: laporan/SEMAKAN_TANPA_8_SAHAM.md -->
# Semakan Ketahanan: Kaedah GUNA Tanpa 8 Saham Bermasalah

**Tarikh:** 10 Okt 2026 · **Enjin:** v1.2 (tidak diubah) · **Data:** dataset_S1–S4 + index_benchmark · **Portfolio:** 8 slot × 12.5%

**Tujuan:** Menguji sama ada empat kaedah GUNA di set 431 (M96, M114, M30, M79) masih kuat apabila 8 saham dengan peristiwa korporat tidak terlaras dibuang: **ASST, FCEL, MTDR, OVV, PR, SM, VAL, XENE**. Alam ujian menjadi 423 saham. Kaedah merentas saham (M96, M114) mengira semula kedudukan/persentil dalam 423 saham.

Semakan maklumat sahaja: registry kaedah tidak diubah.

## 1. Keputusan
| Kaedah | 431 penuh | Tanpa 8 saham | Keputusan baharu | Skor | MDD baharu | Hingga Dis 2025 | Subset lulus (registry) |
|---|---|---|---|---|---|---|---|
| M30 V3 (BB 20/2) | 52.7% | **54.6%** | GUNA | 76.5 | −35.7% | 38.8% | ❌ 2/4 |
| **M96 V1** (Sharpe 3/6/12) | 40.0% | **39.9%** | **GUNA** | **79.8** | −42.1% | 31.4% | ✅ 4/4 |
| M96 V5 (puncak 52 minggu) | 36.2% | 33.8% | GUNA | 78.1 | −42.0% | 25.6% | ✅ 4/4 |
| M79 V3 (Flipper 15%) | 35.5% | 34.6% | UJI KERTAS | 71.3 | −37.2% | 33.4% | ✅ 3/4 |
| M114 V4 (RS 10% teratas) | 49.6% | 31.1% | UJI KERTAS | 64.4 | −34.2% | 24.2% | ✅ 4/4 |
| SPY | 15.9% | | | | | 15.6% | |
| QQQ | 21.7% | | | | | 20.9% | |
| Sama rata | 21.9% (431) | 21.8% (423) | | | | | |

## 2. Semakan kod
| Kaedah | Hasil semula set 431 lawan registry |
|---|---|
| M96 V1 | Tepat: 40.0%, skor 80.3, 294 dagangan |
| M79 V3 | Tepat: 35.5%, skor 75.9, 7146 dagangan |
| M114 V4 | Tepat (dikira dalam sesi yang sama) |
| M30 V3 | Bilangan dagangan tepat (3859); CAGR 52.7% lawan 52.0% registry, skor 76.4 lawan 76.2. Beza kecil, mungkin butiran pengiraan persentil himpitan; tidak mengubah kesimpulan |

## 3. Penemuan
1. **M96 V1 hampir tidak terjejas** (−0.1 mata peratus). Ia hanya memegang 7 dagangan saham bermasalah, dengan sumbangan kecil.
2. **M114 V4 paling terjejas** (−18.5 mata peratus). Satu dagangan FCEL +780% mengangkat keputusan asal; ketiadaannya mengubah dagangan yang mengisi slot selepas itu.
3. **M30 V3 naik** apabila 8 saham dibuang, kerana slot diisi dagangan lain. Masalah asalnya kekal: bergantung pada AXTI (+3,215%); tanpa AXTI 36.5%, tanpa 10 dagangan terbaik 11.1% (laporan/M30.md), dan hanya lulus 2/4 subset.
4. **M79 V3** hampir tidak berubah (−0.9 mata peratus), tetapi skor turun di bawah 75 → UJI KERTAS. ASST (+958%) sebelum ini dagangan terbaiknya.

## 4. Papan kedudukan selepas pembersihan
| # | Kaedah | Status | Sebab |
|---|---|---|---|
| 1 | **M96 V1** | GUNA, LAYAK | Satu-satunya yang kekal GUNA dan lulus 4/4 subset |
| 2 | M79 V3 | UJI KERTAS, layak tetapi rapuh | 3/4 subset; bergantung pada ranking ROC63 |
| 3 | M114 V4 | UJI KERTAS | 4/4 subset, tetapi CAGR jatuh banyak |
| – | M30 V3 | TIDAK LAYAK | 2/4 subset; bergantung pada satu saham (AXTI) |

**Verdict: M96 V1 disahkan sebagai kaedah terbaik setakat ini: lulus gate, lulus 4/4 subset, dan tidak terjejas oleh saham bermasalah.**

## 5. Peringatan untuk semua kaedah di atas
- Purata dagangan memerlukan ~60 hari untuk mencecah +10% (M96, M114, M79); M30 ~97 hari. Tiada kaedah memenuhi sasaran +10% dalam sebulan; semuanya kaedah pegangan 2–3 bulan.
- Senarai Shariah ialah senarai hari ini (bias kemandirian), amat ketara bagi kaedah momentum.
- Keputusan bergantung pada segelintir pemenang besar (M96: MOD, WDC, NVDA).

## 6. Keputusan pengguna yang belum dibuat
Terima pegangan 2–3 bulan dengan M96 V1 sebagai kaedah utama, atau terus mencari kaedah +10% sebulan.
