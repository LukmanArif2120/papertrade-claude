# Kajian lorong 2 "pegang selagi naik" (19 Okt 2026)

Keputusan pengguna 19 Okt 2026: lorong 2 = **Chandelier tutup 4×ATR14, paras hanya naik, tanpa henti kaedah**. Paras keluar = tutup tertinggi sejak beli − 4 × ATR14 (`enjin.atr`); paras tidak pernah turun; tutup < paras → jual pada buka esok. Henti kaedah kekal dalam lorong 1 sahaja. Menggantikan "2 tutup turun berturut atau kena henti kaedah" (17–18 Okt 2026).
Pelaksanaan: `standard/keluar_lorong.py` (`VERSI = chandelier_tutup_4xATR14`; baris peraturan lama dikira semula sekali secara automatik), `standard/lejar.py` (lejar dibina semula dari sesi mula apabila `VERSI` berubah), ujian `ujian/test_keluar_lorong.py`, `ujian/test_lejar.py`. Skrip kajian: `kajian/lorong2/kaji_lorong2.py` (`jana`, `sim`, `ringkas`).

## Data dan kaedah
- 763,327 dagangan enjin v1.2 bagi 134 kaedah (set 431, `data_mentah`, masuk 1 Nov 2019 – 2 Okt 2026). Bilangan dan purata setiap kaedah sama dengan `data/registry_M_gabung.csv`. Kos 0.1% setiap belah.
- Setiap calon dinilai dari harga beli yang sama: isyarat pada tutup → jual pada buka esok; henti kaedah (jika dipakai) seperti `keluar_lorong.py` (rendah ≤ henti → henti; buka ≤ henti dari hari kedua → buka). Posisi yang belum keluar pada 2 Okt 2026 dinilai pada tutup terakhir.
- Lebihan SPY = pulangan dagangan − pulangan SPY dalam tempoh pegangan yang sama. "Sebulan" = purata pulangan ÷ purata hari × 21.
- Trend besar = tutup tertinggi dalam 120 hari ≥ +30% dari harga beli (33% dagangan; purata kenaikan maksimum 70%). Semikon 2026 = 16 saham semikonduktor, masuk 25 Mac – 15 Mei 2026 (1,023 dagangan).
- Lebih 30 calon: N tutup turun (2–4), Chandelier tinggi/tutup 2–5×ATR14/22 (dengan dan tanpa paras hanya naik), trailing 8–25% dari puncak, tutup < MA20/MA50, 2 tutup < MA20, tutup < rendah 10/20 hari, mingguan (1–2 minggu tutup turun, tutup < rendah minggu lepas), henti sahaja; setiap satu dengan dan tanpa henti kaedah.

## Keputusan utama
| Peraturan | Purata % | Median % | 5% terburuk % | Hari | Sebulan % | Lebihan SPY sebulan % | Trend besar % | Semikon 2026 % | Atasi lorong 1 (% kaedah) |
|---|---|---|---|---|---|---|---|---|---|
| Lama: 2 tutup turun + henti kaedah | 0.2 | −1.2 | −8.1 | 6.7 | 0.6 | −0.4 | 2.6 | 11.5 | 2 |
| Lorong 1 (peraturan kaedah) | 2.7 | – | – | 22.7 | 2.5 | – | 12.0 | 21.4 | – |
| **Chandelier tutup 4×ATR14 paras naik, tanpa henti (dipilih)** | **5.1** | **−2.8** | **−18.2** | **43.8** | **2.4** | **1.2** | **25.1** | **27.7** | **80** |
| Sama, dengan henti kaedah | 3.6 | −3.1 | −13.9 | 32.2 | 2.4 | 1.1 | 18.4 | 22.2 | 66 |
| Chandelier tutup 4×ATR14 (paras boleh turun), tanpa henti | 6.1 | −3.0 | −19.8 | 54.1 | 2.4 | 1.0 | 29.4 | 27.6 | 84 |
| Chandelier tinggi 4×ATR14, tanpa henti | 4.8 | −2.8 | −18.0 | 44.3 | 2.3 | 1.0 | 24.2 | 28.3 | 82 |
| Tutup < rendah 20 hari, tanpa henti | 4.2 | −3.5 | −17.0 | 41.4 | 2.1 | 0.9 | 22.1 | 24.9 | 79 |
| Tutup < MA50, tanpa henti | 2.2 | −1.8 | −12.4 | 23.4 | 2.0 | 0.9 | 12.2 | 26.7 | 61 |
| 2 minggu tutup turun, tanpa henti | 3.0 | −1.8 | −17.7 | 32.1 | 2.0 | 0.7 | 16.6 | 43.7 | 59 |
| Trailing 15% dari puncak, tanpa henti | 4.9 | −4.0 | −18.7 | 87.3 | 1.2 | −0.1 | 24.1 | 36.7 | 78 |
| Trailing 20% dari puncak, tanpa henti | 9.1 | −4.4 | −23.0 | 145.2 | 1.3 | −0.1 | 35.8 | 33.0 | 88 |

- Peraturan lama paling lemah antara semua calon: keluar purata selepas 7 hari, hampir tiada bahagian trend besar.
- Lebihan SPY sebulan pegangan tertinggi = pilihan (1.2%). Trailing % tetap tidak mengatasi SPY selepas pegangan panjang; MA20/MA50 keluar serta-merta bagi kaedah pantulan (beli bawah purata).
- Kestabilan: lebihan SPY setiap dagangan positif bagi kaedah momentum (+2.4%) dan pantulan (+2.4%); plato 4–5×ATR (4× tertinggi; 3.5× ke bawah jauh lebih rendah); ATR22 hampir sama.
- Henti kaedah dalam lorong 2 memotong 33% trend besar sebelum trend berkembang. Tanpa henti kaedah, hasil lebih baik atau sama dalam semua ukuran kecuali 5% terburuk (−18.2% lawan −13.9%).

## Berapa lama pegang (pilihan)
- Semua dagangan: hari dagangan p25/median/p75 = 20 / 34 / 58.
- Trend besar: 31 / 54 / 85 hari (~6 / 11 / 17 minggu). Semikon 2026: purata 51 hari (~10 minggu).

## Belian semula (keputusan pengguna 19 Okt 2026)
Dengan peraturan belian semula 17 Okt (kaedah+saham sama hanya selepas kedua-dua lorong keluar), lorong 2 baharu menyekat 39.5% dagangan enjin (peraturan lama 5.5%), jadi lorong 1 Papertrade C dan Lejar tidak lagi mewakili kaedah. Sejak 19 Okt 2026 hanya lorong 1 menyekat belian semula (`kod/scanner.py pegangan_c`, `standard/lejar.py`); dagangan lorong 1 lejar = enjin (diuji), posisi lorong 2 boleh bertindih.

## Batasan
- Lebihan tertumpu pada tahun trend kuat: lebihan SPY ikut tahun masuk 2020 +7.1%, 2021 −0.7, 2022 +1.3, 2023 −0.2, 2024 −1.1, 2025 +10.9, 2026 −1.6 (masih terbuka). Tanpa 2020 dan 2025 semua varian Chandelier 3–5×ATR sedikit bawah SPY (pilihan −0.2% sebulan).
- Median dagangan negatif; untung daripada sebilangan kecil trend besar — perlu ikut semua isyarat.
- Saham yang dinyahsenarai tiada (bias penyintas; menyebelahi pegangan panjang). Keputusan dalam sampel (data sama seperti registry).
- Ujian awal titik masuk proksi breakout (tutup = tinggi 20 hari, atas MA50 naik; 13,306 dagangan, 431 saham) memberi susunan sama: peraturan lama terendah, Chandelier 4×ATR paling cekap.
