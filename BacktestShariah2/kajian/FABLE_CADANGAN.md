# Cadangan Bahagian 2 (cadangan sahaja; tiada fail dijana, ambang kad skor atau kod operasi diubah)

> **Status keputusan (kad skor, harga 2026-11-06):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 223 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Ditulis 9 Nov 2026 bersama `FABLE_PENILAIAN.md` (Bahagian 1) dan `REVERSE/SPEC_SATELIT.md` (kajian tunggal Bahagian 2). Tiga perkara di bawah ialah **cadangan untuk keputusan pengguna**; tiada satu pun dilaksanakan dalam kod sehingga diputuskan dan dipradaftar bertarikh.

## 1. Pradaftar peraturan cantas 223 kaedah (atas label Papan Penganalisis dan kad skor)

Tujuan: mengurangkan bilangan kaedah yang dijejak tanpa membuang kaedah yang belum cukup data. Cantas = **berhenti merekod belian baharu** dalam Lejar dan dashboard; sejarah kekal; boleh dipulihkan hanya dengan pradaftar baharu. Semua ambang di bawah dibaca daripada pemalar sedia ada supaya tiada nombor baharu dicipta selepas melihat data.

| Peraturan | Syarat (dinilai selepas larian `analisis.yml`) | Sumber ambang | Kesan dijangka hari ini |
|---|---|---|---|
| C1 struktur hari-0 | ≥ 12 hari beli langsung, ≥ 30 posisi, henti hari-0 ≥ 20% posisi | `G4_HARI0_MAKS = 0` (gate akan gagal secara pasti) | 12 kaedah Mxx (`FABLE_PENILAIAN.md` §8) |
| C2 pantau | Papan Penganalisis BERSARA atau GANTUNG | `penganalisis.PANTAU_P = 0.9`, `PANTAU_DD = 1.5` (sedia ada) | 0 hari ini |
| C3 NEGATIF | kad skor NEGATIF (lift masuk negatif lulus BH-FDR selepas G1) | `G3_Q = 0.05` | menunggu G1 |
| C4 GAGAL | kad skor GAGAL dua larian berturut-turut | gate G2/G3/G5 | menunggu G1 |
| C5 risiko akaun | lorong T4 L1 ≥ 63 sesi (separuh `G6_SESI`), pulangan < SPUS tingkap sama − 5 mata DAN MDD < -10% | `G6_MDD_HAD = -10`; jurang 5 mata ≈ 1.2 sd jalur 16 sesi dinaikkan ke 63 sesi | 0 hari ini (lorong 16 sesi) |

Syarat tambahan: cantas dinilai **sekali sebulan** (sesi pertama bulan) bukan harian, supaya satu minggu buruk tidak mencantas; satu kaedah yang dicantas direkod dalam `koordinator/keputusan.csv` dengan tarikh dan peraturan. Kaedah replika dinilai dengan dagangan replika. Nxx tidak boleh dicantas oleh C1 (tiada henti) dan hanya oleh C3–C5 selepas G1 Nxx.

Cadangan tambahan **[pendapat]**: hadkan Lejar baharu kepada 223 kaedah sedia ada (tiada Mxx atau Nxx baharu) sehingga Spearman Skor Kaedah 8–12 minggu dinilai; setiap tambahan menaikkan ambang ujian berganda (sauh t Bukti 2.80 pada N = 223).

## 2. Senarai semak sebelum wang sebenar

Semua mesti benar pada hari belian pertama; satu gagal = tiada belian.

1. **TERBUKTI**: `laporan/KAD_SKOR.md` menanda sekurang-kurangnya satu kaedah TERBUKTI (G1–G6), dan status itu kekal dua larian berturut-turut.
2. **Rejim**: hari beli dalam kedua-dua rejim sudah ≥ 10 (G1) dan hari itu rejim QQQ ON (belian satelit hanya dalam ON, `FABLE_PENILAIAN.md` §6).
3. **Had risiko akaun ditulis dahulu**: teras SPUS ≤ 35% akaun, satelit ≤ 15% akaun, 8–10 slot, 1 saham setiap industri, saiz = 0.25% akaun ÷ (4 × ATR14%), had rugi akaun **-10% dari puncak = berhenti semua belian satelit dan semak semula** (bukan jual teras). Nombor ini disalin ke `koordinator/keputusan.csv` sebelum order pertama.
4. **Kos broker**: komisen dan yuran platform diketahui dalam peratus setiap sisi; jika > 0.1% setiap sisi, jangkaan kaedah dikira semula dengan kos itu dan G2 mesti masih lulus.
5. **Slippage**: hanya saham dengan nilai dagangan median 20 hari ≥ USD 10 juta (slippage model 0.10%); saham < USD 10 juta (model 0.25%) dikecualikan daripada wang sebenar walaupun Lejar membelinya.
6. **Cukai**: status cukai pelabur asing atas saham AS (dividen dipotong 30% atau kadar perjanjian; untung modal) disemak dengan penasihat; jejak dividen SPUS diambil kira dalam jangkaan teras.
7. **Pelaksanaan**: order pasaran pada buka (C01, satu-satunya cara yang diukur terbaik); tiada limit di bawah, tiada buy-stop, tiada bracket sasaran (`REVERSE/CARA_94.md`).
8. **Data**: saham bukan dalam `data/harga/kuarantin.csv`, bukan `tidak_layak` (ambil alih, tidak cair, kelas berganda), bukan melintas earnings dalam 5 sesi jika kaedah itu tidak diukur melintas earnings.
9. **Rekod**: setiap order sebenar direkod dalam fail baharu `papertrade/sebenar.csv` (skema sama `SKEMA.md` + lajur komisen sebenar, harga isi sebenar) supaya slippage sebenar diukur lawan model selepas 20 dagangan.
10. **Pemerhatian 20 dagangan pertama** dengan saiz separuh (0.125% risiko) sebelum saiz penuh.

## 3. Format ringkasan mingguan 5 baris (untuk `jadual/mingguan.md`, ntfy topik `claude_azim`)

Lima baris tetap, setiap satu ≤ 120 aksara, nombor daripada `kad_skor.json`, `t4_siri.csv`, `portfolio_slot/RINGKASAN.md` dan `spus_harian.csv`; tiada tafsiran bebas:

1. `Kad skor: TERBUKTI n · CALON n · BELUM CUKUP n · GAGAL n · NEGATIF n. Hari beli m (ON a / OFF b). G1 paling awal <tarikh>.`
2. `Rejim QQQ: ON/OFF sejak <tarikh>; QQQ lawan SMA50 ±x%.`
3. `SPUS minggu ini ±x% (MDD sejak 16 Okt y%). Teras 35% + tunai: ±z% minggu ini.`
4. `Lorong T4 teratas (BUKAN pangkat): Mxx ±x% MDD y% persentil jalur p; median 223 lorong ±x%.`
5. `Tindakan: tiada wang sebenar; <satu keputusan tertunda, jika ada, dari koordinator/keputusan.csv>.`

Pelaksanaan **[cadangan]**: fungsi `ringkasan_mingguan()` dalam `standard/koordinator.py` (sudah membaca fail yang sama), dipanggil oleh `jadual/mingguan.md` langkah akhir dan dihantar melalui `amaran_ntfy.yml`. Tiada perubahan kepada gate.
