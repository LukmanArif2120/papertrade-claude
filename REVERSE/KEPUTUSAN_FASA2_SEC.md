# KEPUTUSAN FASA 2 — LEG SEC: **DITOLAK**

Dijana 2026-10-28 22:19 UTC daripada output `step10_sec.py` dan `step11_sec_nilai.py`. Spec dipradaftar: `REVERSE/SPEC_FASA2.md` §4.1–§4.4 (data dan masa ketersediaan), §5 (ujian), §6 (ambang penerimaan), §9.3–§9.5 (ufuk, set signal, ambang pecahan). Semua pilihan dikunci sebelum keputusan dilihat.

## 1. Soalan

Fasa 1 mengukur ruang indikator harga sampai habis: 20,640 ujian ENTRY, enam tahun, empat rejim, **kosong**. Fasa 2 leg SEC menanya satu soalan yang berbeza — sama ada data **fundamental titik-masa** (SUE, pecutan hasil, jarak ke earnings) membawa kuasa pemangkatan yang indikator harga tidak ada, atas **populasi peristiwa yang sama**.

Sasaran: pulangan **boleh didagangkan** (`pul_henti2atr`) — masuk buka esok dengan kos sisi, henti keras −2×ATR14, ufuk 63 hari, kos keluar. Bukan puncak run. Kesilapan fasa 1 (lift 10–24 kali atas hasil bersyarat hindsight yang hilang dalam dagangan) tidak diulang.

## 2. Data dan liputan

Tahun dinilai: **2012–2025** (14 tahun). Peristiwa sah: **161,204**.

| tahun | n_peristiwa | n_saham | n_saham_ada_sec | n_sue | pct_sue |
|---|---|---|---|---|---|
| 2012.0 | 7028.0 | 1205.0 | 887.0 | 4557.0 | 64.8 |
| 2013.0 | 7946.0 | 1361.0 | 1100.0 | 6475.0 | 81.5 |
| 2014.0 | 8271.0 | 1487.0 | 1203.0 | 6694.0 | 80.9 |
| 2015.0 | 9497.0 | 1591.0 | 1306.0 | 7783.0 | 82.0 |
| 2016.0 | 9715.0 | 1624.0 | 1348.0 | 8057.0 | 82.9 |
| 2017.0 | 9530.0 | 1745.0 | 1434.0 | 7927.0 | 83.2 |
| 2018.0 | 12030.0 | 1873.0 | 1552.0 | 9975.0 | 82.9 |
| 2019.0 | 11839.0 | 1907.0 | 1586.0 | 9842.0 | 83.1 |
| 2020.0 | 12858.0 | 2045.0 | 1694.0 | 10799.0 | 84.0 |
| 2021.0 | 15259.0 | 2283.0 | 1832.0 | 12615.0 | 82.7 |
| 2022.0 | 15440.0 | 2255.0 | 1823.0 | 12638.0 | 81.9 |
| 2023.0 | 13642.0 | 2202.0 | 1836.0 | 11211.0 | 82.2 |
| 2024.0 | 14151.0 | 2191.0 | 1844.0 | 11938.0 | 84.4 |
| 2025.0 | 13998.0 | 2237.0 | 1862.0 | 11568.0 | 82.6 |


Data SEC ialah **nilai pertama difail** (SEC XBRL), jadi ia titik-masa secara retrospektif sejak 2009 — tidak seperti RS/gred yang dikira harian dan tiada sejarah (`SPEC_FASA2.md` §4.1). Hari ketersediaan = sesi dagangan pertama yang bukanya selepas cap masa pemfailan (§4.2), bukan `tarikh_fail`: 52% earnings 8-K difail selepas tutup 16:00 ET, jadi `tarikh_fail` akan memberi lebih separuh peristiwa maklumat kira-kira satu sesi lebih awal.

## 3. §5.1 Pemangkatan (Spearman setiap tahun)

Ambang §9.3/§9.5: tanda konsisten ≥ 71% tahun dinilai (minimum 10 tahun), |rho| purata ≥ 0.05.

| lajur | n_tahun | konsisten | tahun_dikecualikan | rho_purata | rho_min | rho_maks | rho_abs | perlu_konsisten | boleh_dinilai | lulus_51 |
|---|---|---|---|---|---|---|---|---|---|---|
| sue | 14 | 11 |  | 0.0224 | -0.0247 | 0.0834 | 0.0295 | 10 | True | False |
| tumbuh_hasil | 14 | 11 |  | -0.0411 | -0.1712 | 0.077 | 0.06 | 10 | True | True |
| pecutan_hasil | 14 | 12 |  | 0.0272 | -0.0359 | 0.0859 | 0.0331 | 10 | True | False |


Lulus §5.1: **1 daripada 3** lajur.

Bandingan fasa 1 (`ujian_pangkat.py`): daripada 30 indikator harga, **1 sahaja** konsisten-tanda lawan pulangan boleh didagangkan, dan |rho| tertinggi 0.027. `atr_pct` memberi rank-IC **−0.251** — apa yang memilih pergerakan besar ialah apa yang menghalang kita memegangnya.

## 4. §5.2 + §5.3 Kehadiran dan kawalan kebetulan

Keluarga FDR **FASA2_SEC**, 20 ujian, BH-FDR q ≤ 0.01. Berasingan daripada leg RS/gred dan kelima-lima keluarga fasa 1 — tiada penggabungan kiraan ujian. Permutasi label 1000× (bilangan sama setiap bulan), bootstrap blok 1000× mengikut **ticker** dan mengikut **minggu**.

| signal | n | K_padu | lift | presisi | lift_presisi | p_permutasi | pul_purata | jangkaan | jangkaan_tanpa_5pct | p5_blok_ticker | p5_blok_minggu | kelas | lulus_fdr | lulus_53 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| q1:tumbuh_hasil | 23431 | 22.55 | 1.215 | 47.22 | 1.141 | 0.0009990009990009 | 2.158 | 2.158 | -0.787 | 1.915 | 1.14 | TIDAK BERGUNA | True | False |
| q5:tumbuh_hasil | 23428 | 25.6 | 1.356 | 53.66 | 1.296 | 0.0009990009990009 | 0.785 | 0.785 | -2.559 | 0.477 | 0.077 | TIDAK BERGUNA | True | False |
| q1:pecutan_hasil | 23057 | 22.12 | 1.074 | 46.39 | 1.122 | 0.0009990009990009 | 1.061 | 1.061 | -2.061 | 0.797 | 0.183 | TIDAK BERGUNA | True | False |
| q5:pecutan_hasil | 23051 | 23.04 | 1.243 | 48.42 | 1.171 | 0.0009990009990009 | 1.872 | 1.872 | -1.165 | 1.601 | 1.019 | TIDAK BERGUNA | True | False |
| q5:tumbuh_hasil&sejak_earnings_le5 | 2205 | 2.55 | 1.528 | 56.92 | 1.375 | 0.0009990009990009 | 2.04 | 2.04 | -1.259 | 1.236 | 0.678 | TIDAK BERGUNA | True | False |
| q5:tumbuh_hasil&jangka_earnings_le5 | 1023 | 1.1 | 1.237 | 53.27 | 1.287 | 0.0009990009990009 | 1.222 | 1.222 | -2.312 | 0.052 | -0.916 | TIDAK BERGUNA | True | False |
| q5:pecutan_hasil&sejak_earnings_le5 | 2367 | 2.51 | 1.33 | 51.33 | 1.241 | 0.0009990009990009 | 3.806 | 3.806 | 0.533 | 3.102 | 1.681 | TIDAK BERGUNA | True | True |
| sejak_earnings_le5 | 13505 | 8.48 | 1.006 | 41.19 | 1.009 | 0.0039960039960039 | 1.587 | 1.587 | -0.936 | 1.328 | 0.633 | TIDAK BERGUNA | True | False |
| q5:sue&sejak_earnings_le5 | 2770 | 2.16 | 0.986 | 40.72 | 1.01 | 0.0069930069930069 | 1.687 | 1.687 | -0.776 | 1.163 | 0.77 | TIDAK BERGUNA | False | False |
| q5:pecutan_hasil&jangka_earnings_le5 | 1004 | 1.0 | 1.177 | 48.61 | 1.175 | 0.0079920079920079 | 1.162 | 1.162 | -1.722 | 0.176 | -0.304 | TIDAK BERGUNA | False | False |
| q1:pecutan_hasil&sejak_earnings_le5 | 2057 | 1.97 | 1.069 | 46.33 | 1.12 | 0.0109890109890109 | 0.44 | 0.44 | -2.218 | -0.254 | -0.66 | TIDAK BERGUNA | False | False |
| q1:pecutan_hasil&jangka_earnings_le5 | 1050 | 1.08 | 1.126 | 49.81 | 1.204 | 0.0309690309690309 | 4.358 | 4.358 | 0.117 | 3.033 | 0.572 | TIDAK BERGUNA | False | False |
| q1:sue&sejak_earnings_le5 | 2387 | 2.07 | 1.124 | 45.41 | 1.127 | 0.0619380619380619 | 1.809 | 1.809 | -0.926 | 1.158 | 0.364 | TIDAK BERGUNA | False | False |
| q1:sue&jangka_earnings_le5 | 1178 | 1.04 | 1.181 | 45.76 | 1.135 | 0.1038961038961039 | 2.872 | 2.872 | -0.085 | 1.939 | 0.912 | TIDAK BERGUNA | False | False |
| q1:tumbuh_hasil&sejak_earnings_le5 | 2260 | 2.18 | 1.132 | 46.99 | 1.135 | 0.2167832167832167 | 2.984 | 2.984 | -0.03 | 2.333 | 0.954 | TIDAK BERGUNA | False | False |
| q5:sue | 25984 | 19.54 | 0.917 | 39.16 | 0.971 | 0.3476523476523476 | 1.023 | 1.023 | -1.443 | 0.811 | 0.548 | TIDAK BERGUNA | False | False |
| q1:tumbuh_hasil&jangka_earnings_le5 | 1080 | 1.06 | 1.129 | 47.59 | 1.15 | 0.4475524475524475 | 3.641 | 3.641 | 0.567 | 2.597 | 0.883 | TIDAK BERGUNA | False | False |
| q5:sue&jangka_earnings_le5 | 1061 | 0.76 | 0.862 | 37.42 | 0.928 | 0.5934065934065934 | 0.887 | 0.887 | -1.43 | 0.018 | -0.239 | TIDAK BERGUNA | False | False |
| jangka_earnings_le5 | 5888 | 3.69 | 0.969 | 41.2 | 1.009 | 0.7282717282717283 | 1.822 | 1.822 | -1.027 | 1.426 | 0.5 | TIDAK BERGUNA | False | False |
| q1:sue | 25982 | 21.82 | 1.103 | 44.18 | 1.096 | 0.7862137862137862 | 1.394 | 1.394 | -1.28 | 1.168 | 0.674 | TIDAK BERGUNA | False | False |


Lulus §5.3 (FDR **dan** kedua-dua skema blok > 0 **dan** jangkaan tanpa 5% pemenang teratas > 0): **1 daripada 20**.

## 5. Keputusan

**Leg SEC fasa 2 DITOLAK.**

§6 syarat 1 menuntut **lajur yang sama** lulus §5.1 **dan** §5.3. Itu tidak berlaku: lajur lulus §5.1 = **tumbuh_hasil**, lajur induk lulus §5.3 = **pecutan_hasil**. Persilangannya kosong.

1 daripada 3 lajur lulus §5.1 dan 1 daripada 20 signal lulus §5.3, tetapi bukan lajur yang sama — jadi tiada penemuan yang lulus kedua-dua ujian. Membaca "satu lulus di sini, satu lulus di sana" sebagai penemuan ialah tepat kesilapan yang §6 ditulis untuk menghalang.

Ini **dijangka**, dan dinyatakan sebelum ujian dijalankan (§9.3): PEAD sudah susut sejak ia diketahui umum, dan baki kesannya tertumpu pada saham kecil berspread lebar — sedangkan universe REVERSE ialah 2,000 teratas ikut nilai dagangan, iaitu dengan sengaja membuang bahagian keratan-rentas itu.

## 5b. §5.4 Portfolio 8 slot × 12.5%

**Keputusan §6 sudah ditentukan oleh syarat 1 (lihat §5 di bawah). Nombor di sini ialah maklumat magnitud, bukan kriteria penerimaan.** Ia dijalankan kerana signal yang bertahan §5.3 tidak gagal ujian kebetulan — ia bertahan 1000 permutasi label dan kedua-dua skema bootstrap blok — tetapi lajur induknya gagal ujian pemangkatan §5.1. Nombor ini **tidak** mengubah keputusan DITOLAK.

Kos penuh, tiga rujukan keluar fasa 1, dua saiz (tetap 12.5% dan berskala risiko SPEC_1B k = 4 risiko 1.0%). Nilai di bawah ialah **median merentas tahun**. §6 syarat 3: signal mesti mengalahkan KAWALAN RAWAK pada pulangan **dan** MDD.

| signal | jenis | keluar | saiz | pulangan_tahunan | mdd | median_bulanan | pct_bulan_ge10 | bulan_terburuk |
|---|---|---|---|---|---|---|---|---|
| q5:pecutan_hasil&sejak_earnings_le5 | RAWAK | REF_chandelier_4atr | risiko | 0.72 | -8.7 | 0.53 | 0.0 | -4.82 |
| q5:pecutan_hasil&sejak_earnings_le5 | RAWAK | REF_chandelier_4atr | tetap | 9.16 | -14.66 | 1.0 | 0.0 | -7.6 |
| q5:pecutan_hasil&sejak_earnings_le5 | RAWAK | REF_jual_hari63 | risiko | 2.7 | -9.41 | 0.88 | 0.0 | -4.76 |
| q5:pecutan_hasil&sejak_earnings_le5 | RAWAK | REF_jual_hari63 | tetap | 4.33 | -14.84 | 0.98 | 0.0 | -7.34 |
| q5:pecutan_hasil&sejak_earnings_le5 | RAWAK | REF_pegang_252 | risiko | 9.86 | -10.7 | 1.15 | 0.0 | -5.12 |
| q5:pecutan_hasil&sejak_earnings_le5 | RAWAK | REF_pegang_252 | tetap | 15.3 | -15.76 | 1.37 | 0.0 | -8.66 |
| q5:pecutan_hasil&sejak_earnings_le5 | signal | REF_chandelier_4atr | risiko | 2.97 | -8.56 | 0.72 | 0.0 | -4.62 |
| q5:pecutan_hasil&sejak_earnings_le5 | signal | REF_chandelier_4atr | tetap | 3.0 | -13.98 | 0.58 | 0.0 | -8.38 |
| q5:pecutan_hasil&sejak_earnings_le5 | signal | REF_jual_hari63 | risiko | 9.87 | -9.5 | 0.9 | 0.0 | -4.22 |
| q5:pecutan_hasil&sejak_earnings_le5 | signal | REF_jual_hari63 | tetap | 17.65 | -14.55 | 1.46 | 0.0 | -6.85 |
| q5:pecutan_hasil&sejak_earnings_le5 | signal | REF_pegang_252 | risiko | 3.68 | -11.4 | 0.78 | 0.0 | -5.65 |
| q5:pecutan_hasil&sejak_earnings_le5 | signal | REF_pegang_252 | tetap | 4.95 | -20.36 | 1.07 | 0.0 | -10.98 |


- `REF_chandelier_4atr` / saiz risiko: signal 2.97%/tahun MDD -8.56% lawan rawak 0.72%/tahun MDD -8.70% -> mengalahkan rawak pada pulangan DAN MDD: **YA**
- `REF_chandelier_4atr` / saiz tetap: signal 3.00%/tahun MDD -13.98% lawan rawak 9.16%/tahun MDD -14.66% -> mengalahkan rawak pada pulangan DAN MDD: **TIDAK**
- `REF_jual_hari63` / saiz risiko: signal 9.87%/tahun MDD -9.50% lawan rawak 2.70%/tahun MDD -9.41% -> mengalahkan rawak pada pulangan DAN MDD: **TIDAK**
- `REF_jual_hari63` / saiz tetap: signal 17.65%/tahun MDD -14.55% lawan rawak 4.33%/tahun MDD -14.84% -> mengalahkan rawak pada pulangan DAN MDD: **YA**
- `REF_pegang_252` / saiz risiko: signal 3.68%/tahun MDD -11.40% lawan rawak 9.86%/tahun MDD -10.70% -> mengalahkan rawak pada pulangan DAN MDD: **TIDAK**
- `REF_pegang_252` / saiz tetap: signal 4.95%/tahun MDD -20.36% lawan rawak 15.30%/tahun MDD -15.76% -> mengalahkan rawak pada pulangan DAN MDD: **TIDAK**

Sasaran +10%/bulan dibaca daripada lajur `median_bulanan` dan `pct_bulan_ge10` di atas, tanpa dimaniskan.

## 6. Apa yang leg ini TIDAK menjawab

- Leg **RS/gred** fasa 2 masih menunggu data terkumpul (anggaran ~Okt 2027). Keputusan di atas tidak mendahuluinya.
- Leg SEC berjalan atas universe A02 yang **sama** dengan fasa 1, jadi ia mewarisi sifat survivorship yang sama. Itu **had**, bukan kelebihan (§9.3).
- Lajur SEC hadir pada kira-kira 27–30% peristiwa sah sahaja, kerana SUE memerlukan sejarah suku yang cukup. Peristiwa tanpa lajur dikecualikan, bukan diisi sifar.
- Liputan XBRL berperingkat 2009–2011 (89 saham pada 2009, 253 pada 2010, 482 pada 2011) — sebab ujian bermula 2012, bukan 2009.
