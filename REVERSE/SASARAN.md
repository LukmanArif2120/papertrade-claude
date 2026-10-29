# SASARAN: apa yang TERUKUR boleh dicapai

Dijana 2026-10-29 00:22 UTC oleh `REVERSE/sasaran_terukur.py` daripada data yang sudah ada. **Tiada parameter ditala, tiada signal dipilih, tiada ujian baharu dijalankan.** Ia hanya meletakkan sasaran +10%/bulan bersebelahan dengan asas yang paling mudah.

## 1. Aritmetik sasaran itu sendiri

+10% sebulan, dikompaun, bermakna:

- **3.14× setahun** (+214%/tahun)
- **8,994,377× atas 14 tahun** — tempoh yang sama dengan kajian ini
- USD 10,000 menjadi **USD 89,943,774,035**

Tiada strategi dalam sejarah pasaran yang pernah mengekalkan kadar itu atas 14 tahun. Ini bukan pendapat tentang kaedah; ia sifat pengkompaunan.

## 2. Asas paling mudah: beli-dan-pegang SPY, 2012-2025

| Tahun | Pulangan | MDD | Median bulanan | % bulan ≥ +10% | Bulan terburuk |
|---|---|---|---|---|---|
| 2012 | 14.17% | -9.69% | 1.18% | 0.0% | -6.01% |
| 2013 | 29.00% | -5.55% | 2.59% | 0.0% | -3.00% |
| 2014 | 14.56% | -7.27% | 2.06% | 0.0% | -1.38% |
| 2015 | 1.29% | -11.91% | 0.37% | 0.0% | -6.10% |
| 2016 | 13.59% | -9.19% | 0.39% | 0.0% | -1.73% |
| 2017 | 20.78% | -2.61% | 1.41% | 0.0% | 0.13% |
| 2018 | -5.25% | -19.35% | 0.58% | 0.0% | -8.80% |
| 2019 | 31.09% | -6.62% | 2.21% | 0.0% | -6.38% |
| 2020 | 17.24% | -33.72% | 3.70% | 18.2% | -12.49% |
| 2021 | 30.51% | -5.11% | 2.78% | 0.0% | -4.66% |
| 2022 | -18.65% | -24.50% | -2.95% | 0.0% | -9.24% |
| 2023 | 26.71% | -9.97% | 1.60% | 0.0% | -4.74% |
| 2024 | 25.59% | -8.41% | 2.34% | 0.0% | -4.03% |
| 2025 | 18.01% | -18.76% | 2.05% | 0.0% | -5.57% |

**Median: pulangan 17.62%/tahun, MDD -9.44%, bulanan 1.82%.** Bulan yang mencapai +10%: **0% dalam 13 daripada 14 tahun** — satu-satunya pengecualian ialah tahun pemulihan selepas kejatuhan.

Sasaran +10%/bulan ialah kira-kira **5.5 kali** median bulanan indeks, dan indeks itu sendiri melepasinya hanya dalam satu tahun daripada 14.

## 3. Apa yang kajian ini hasilkan, bersebelahan

Portfolio leg SEC (§5.4, median merentas 14 tahun). Kesemua enam konfigurasi dipradaftar ditunjukkan — **bukan yang terbaik sahaja** — kerana memilih sel terbaik selepas melihat jadual bukan dapatan.

| Keluar | Saiz | Pulangan | MDD | Median bulanan | % bulan ≥ +10% |
|---|---|---|---|---|---|
| REF_jual_hari63 | tetap | 17.65% | -14.55% | 1.46% | 0.0% |
| REF_jual_hari63 | risiko | 9.87% | -9.50% | 0.90% | 0.0% |
| REF_pegang_252 | tetap | 4.95% | -20.36% | 1.07% | 0.0% |
| REF_pegang_252 | risiko | 3.68% | -11.40% | 0.78% | 0.0% |
| REF_chandelier_4atr | tetap | 3.00% | -13.98% | 0.58% | 0.0% |
| REF_chandelier_4atr | risiko | 2.97% | -8.56% | 0.72% | 0.0% |

Konfigurasi terbaik (REF_jual_hari63, saiz tetap) memberi **17.65%/tahun pada MDD -14.55%**. SPY beli-dan-pegang memberi **17.62%/tahun pada MDD -9.44%** atas tempoh yang sama.

Mengalahkan SPY pada pulangan **dan** MDD: **TIDAK**. Median bulanannya 1.46% lawan 1.82% bagi SPY.

## 4. Apa yang ini bermakna untuk keputusan

Selepas 20,640 ujian indikator harga (fasa 1), 108 ujian saiz posisi (fasa 1b), 20 ujian fundamental titik-masa (fasa 2 leg SEC), dan 38,400 konfigurasi Optuna (AUTOTUNE A02 — LULUS 0), **tiada satu pun mengalahkan beli-dan-pegang SPY pada pulangan dan MDD serentak** atas tempoh yang sama.

Itu bukan kegagalan mencari. Ia pengukuran: ruang yang boleh dicapai dengan data harga harian dan fundamental suku, pada universe 2,000 saham AS paling cair, sudah diukur dan hadnya kira-kira pulangan indeks.

Keputusan yang tinggal adalah milik pengguna, dan ia bukan keputusan teknikal:

1. **Kekalkan sasaran +10%/bulan** dan terima bahawa tiada kerja yang boleh dicadangkan secara jujur akan mencapainya. Setiap kajian seterusnya akan ditolak seperti tiga yang sudah.
2. **Tetapkan sasaran pada apa yang terukur** — kira-kira pulangan indeks, dengan MDD yang boleh ditanggung — dan alihkan usaha daripada mencari kelebihan kepada mengurangkan kos, cukai, dan kesilapan pelaksanaan. Itu lever yang belum pernah diukur dalam repo ini.
3. **Terima risiko lebih tinggi secara sengaja** (leveraj, kepekatan) untuk pulangan lebih tinggi. Itu keputusan risiko, bukan penemuan signal, dan ia membawa risiko kehabisan modal yang kajian ini tidak mengukur.

Saya tidak boleh memilih antara ketiga-tiganya untuk pengguna: ia bergantung pada berapa banyak modal boleh hilang tanpa mengubah hidupnya, dan itu bukan nombor yang ada dalam repo ini.
