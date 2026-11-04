# Jarak 52w — diagnostik POST-HOC

**Bukan gate, bukan pradaftar.** Dijalankan selepas `REVERSE/JARAK_52W.md` dilihat,
semata-mata untuk menerangkan mengapa MIN dan MEDIAN memberi arah BERTENTANGAN.
Tiada dakwaan statistik baharu; `REVERSE/SPEC_52W.md` §11 melarang penalaan band.

## 1. Median setiap band (metrik POST-HOC)

### `H126`

| Band | n tahan | Min tahan | **Median tahan** | Min latih | **Median latih** |
|---|---|---|---|---|---|
| `B0` di atas tinggi 52w | 82,029 | +6.37% | **+2.55%** | +5.62% | **+4.41%** |
| `B1` -2% .. 0% | 181,169 | +4.64% | **+2.89%** | +5.19% | **+4.77%** |
| `B2` -5% .. -2% | 321,907 | +5.12% | **+3.19%** | +5.72% | **+5.19%** |
| `B3` -10% .. -5% | 507,005 | +6.10% | **+3.42%** | +5.98% | **+5.23%** |
| `B4` -15% .. -10% | 443,431 | +6.63% | **+3.44%** | +5.99% | **+5.07%** |
| `B5` -25% .. -15% | 718,332 | +8.03% | **+4.03%** | +5.53% | **+4.23%** |
| `B6` -40% .. -25% | 731,729 | +10.77% | **+4.62%** | +4.32% | **+1.84%** |
| `B7` bawah -40% | 944,513 | +19.22% | **-1.52%** | +5.69% | **-2.48%** |

### `X13`

| Band | n tahan | Min tahan | **Median tahan** | Min latih | **Median latih** |
|---|---|---|---|---|---|
| `B0` di atas tinggi 52w | 90,046 | +0.53% | **+0.61%** | +0.46% | **+0.42%** |
| `B1` -2% .. 0% | 195,231 | +1.00% | **+1.70%** | +1.28% | **+1.77%** |
| `B2` -5% .. -2% | 342,134 | +1.89% | **+4.13%** | +2.29% | **+4.09%** |
| `B3` -10% .. -5% | 534,033 | +2.90% | **+5.82%** | +2.86% | **+5.27%** |
| `B4` -15% .. -10% | 464,876 | +3.44% | **+6.31%** | +2.98% | **+5.79%** |
| `B5` -25% .. -15% | 751,068 | +4.21% | **+7.40%** | +2.84% | **+6.23%** |
| `B6` -40% .. -25% | 763,240 | +5.61% | **+9.47%** | +2.50% | **+7.12%** |
| `B7` bawah -40% | 977,795 | +9.58% | **+12.03%** | +4.41% | **+9.66%** |

## 2. Setiap tahun (ufuk 126 sesi) — stabiliti

| Tahun | IC min | % hari IC > 0 | Median D1 | Median D9 | Median D10 | Min D1 | Min D10 | Beza median D9−D1 |
|---|---|---|---|---|---|---|---|---|
| 2012 | +0.0672 | 63% | +2.83% | +9.71% | +8.95% | +8.73% | +10.56% | +6.88 |
| 2013 | -0.0128 | 45% | +7.53% | +9.41% | +9.03% | +20.15% | +11.55% | +1.88 |
| 2014 | +0.0748 | 90% | -4.50% | +5.06% | +4.71% | +1.36% | +4.94% | +9.56 |
| 2015 | +0.1962 | 96% | -17.40% | -0.67% | -0.88% | -9.59% | -0.90% | +16.74 |
| 2016 | -0.0547 | 32% | +11.11% | +8.47% | +7.89% | +18.83% | +9.68% | -2.64 |
| 2017 | +0.0401 | 66% | +4.02% | +7.25% | +7.38% | +15.32% | +8.89% | +3.23 |
| 2018 | +0.0912 | 90% | -8.06% | +0.82% | +1.86% | +1.31% | +2.68% | +8.88 |
| 2019 | +0.1443 | 89% | -16.09% | +1.36% | +2.04% | -5.01% | -0.43% | +17.45 |
| 2020 | -0.1893 | 17% | +47.23% | +16.04% | +14.31% | +132.50% | +21.79% | -31.19 |
| 2021 | +0.2495 | 97% | -33.75% | +0.24% | -0.83% | -22.56% | -0.31% | +33.99 |
| 2022 | +0.1430 | 81% | -19.22% | -1.23% | -2.90% | -6.25% | -1.75% | +18.00 |
| 2023 | +0.1229 | 96% | -8.74% | +6.85% | +7.46% | +8.90% | +8.46% | +15.59 |
| 2024 | +0.1486 | 100% | -10.63% | +4.67% | +4.64% | +21.98% | +5.98% | +15.30 |
| 2025 | -0.0743 | 29% | +15.13% | +5.31% | +5.20% | +51.91% | +8.01% | -9.82 |

## 3. Adakah kesan MIN pada band jauh didorong 2020?

| Tingkap | Min `B7` (bawah −40%) | Min asas | Lift min |
|---|---|---|---|
| tahan penuh 2020–2025 | +19.22% | +10.39% | +8.82 |
| tahan tanpa 2020 | +5.05% | +4.26% | +0.80 |
| 2020 sahaja | +84.30% | +41.84% | +42.46 |
| latih 2012–2019 | +5.69% | +5.53% | +0.16 |

## 4. Rumusan diagnostik

Lulus kesemua gate band (gate0–gate3): **1/40**. Satu-satunya yang lulus ialah `B7×X13`, dan §3 menunjukkan liftnya **+8.82 mata dengan 2020 di dalam, +0.80 tanpa 2020, +0.16 dalam latih** — iaitu ia peristiwa SATU TAHUN, bukan kesan berulang. Pada 2020 sahaja `B7` memberi +84.30% lawan asas +41.84%. Tambah kaveat alam (`SPEC_52W.md` §2: tiada delist, jadi saham yang jatuh 40% dan mati tiada dalam alam), dan dakwaan "beli jauh di bawah tinggi 52w" **tidak boleh dibuat**.

**Punca percanggahan MIN lawan MEDIAN (tidak dijangka dalam spec):** `j52` berkorelasi dengan KEDUDUKAN PASARAN dalam kitarannya, bukan hanya dengan saham. Pada Mac 2020 hampir setiap saham berada > 40% di bawah tinggi 52w, jadi band mutlak `B7` mengumpulkan bar yang bertarikh pada DASAR pasaran — pulangan hadapannya tinggi untuk SEMUA nama, bukan kerana pemilihan saham. Jadual band §2 oleh itu mengukur **pemasaan pasaran**, bukan pemilihan saham. Desil (§4 laporan utama) dikira **dalam hari yang sama**, jadi ia bebas daripada confound itu — dan di sana arahnya BERTENTANGAN: nama yang lebih HAMPIR tinggi 52w memberi median lebih tinggi.

| Ufuk | IC latih | IC tahan | Tanda sama | t≥2 latih | t≥2 tahan |
|---|---|---|---|---|---|
| 21 | +0.0315 | +0.0551 | ya | ya | ya |
| 63 | +0.0557 | +0.0654 | ya | ya | ya |
| 126 | +0.0683 | +0.0796 | ya | ya | tidak |

`gate4` seperti ditulis dalam spec **GAGAL**, kerana kaki kemonotonan dipradaftar atas **MIN** desil dan min desil bertukar tanda antara tingkap (rho +0.92 latih → −0.96 tahan pada 63 sesi). Kaki IC **LULUS** pada 21 dan 63 sesi: tanda sama dan |t| ≥ 2 dalam kedua-dua tingkap. Itu kesilapan spec saya, bukan penemuan: saya sepatutnya menulis kaki kemonotonan atas MEDIAN kerana min desil mewarisi masalah ekor yang kajian ini sudah tahu ada.

**Jangkaan priori §9 saya: SALAH pada 2 daripada 4.** Betul: (1) band tidak monoton; (2) band jauh min tertinggi. Salah: (3) saya ramal `|IC| < 0.02` dan tidak stabil — IC sebenarnya **+0.032 hingga +0.116**, bertanda sama dalam dua tingkap, positif dalam **10 daripada 14 tahun**; (4) saya ramal 0/40 lulus — 1/40 lulus. Kali KEEMPAT berturut-turut jangkaan priori saya salah pada ruang belum diukur.

