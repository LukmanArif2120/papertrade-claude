# Adakah +10% sebulan mungkin? Diukur daripada Papertrade C

Dijana 2026-10-29 06:00 UTC oleh `standard/sasaran_papertrade.py`. Data jejak hadapan sebenar, bukan backtest.

**Tempoh: 2026-10-08 hingga 2026-10-28.** 7,377 posisi sah dibeli, 786 saham, 124 kaedah, 92 fail.

## 1. Had yang mesti dibaca dahulu

Tempoh ini **kurang daripada sebulan penuh**. Data ini tidak boleh menjawab sama ada +10% sebulan BOLEH DIKEKALKAN. Ia hanya boleh menunjukkan **bentuk** taburan pulangan, dan sama ada bentuk itu membenarkan sasaran tersebut.

7,377 posisi daripada 124 kaedah **bukan portfolio** — tiada sesiapa boleh membeli kesemuanya. Pulangan setiap posisi dan pulangan portfolio ialah dua perkara berbeza, dan hanya yang kedua perlu mencapai sasaran.

## 2. Posisi yang sudah DITUTUP (realisasi)

- 1,770 posisi
- median **-2.67%**, purata -3.01%
- kadar menang **16.8%**
- tempoh pegang median **1 hari**

Posisi masih terbuka: 5,607, median +1.05%. Angka terbuka itu kelihatan lebih baik kerana yang rugi **sudah dikeluarkan** oleh henti — itu bukan prestasi, itu kesan pemilihan dalam buku terbuka.

## 3. Berapa kerap satu posisi mencapai +10%?

| Ambang | Daripada posisi ditutup | Daripada semua posisi |
|---|---|---|
| ≥ +5% | 4.41% | 15.63% |
| ≥ +10% | 1.41% | 4.83% |
| ≥ +20% | 0.45% | 0.94% |
| ≥ +50% | 0.00% | 0.07% |

Taburan semua posisi: p10 -4.57% · p25 -1.70% · p50 **+0.00%** · p75 +3.29% · p90 **+7.04%** · maks +59.40%

### Aritmetik yang menentukan

Tempoh pegang median **3 hari** (semua posisi; yang DITUTUP median 1 hari kerana didominasi henti pantas — menggunakan angka itu akan melebih-lebihkan pusing ganti dengan teruk).

Itu kira-kira **7.0 pusingan sebulan**. Untuk +10% sebulan, setiap pusingan perlu **+1.37% purata merentas semua posisi**, termasuk yang rugi, selepas kos.

**Asas yang betul ialah pulangan REALISASI: -3.01%** (purata 1,770 posisi yang sudah ditutup).

Purata semua posisi (+0.95%) **tidak boleh diguna** di sini: 76% posisi masih terbuka, dan yang rugi sudah dikeluarkan oleh henti sementara yang baik masih dikira. Realisasi -3.01% lawan belum-nyata +2.20% menunjukkan saiz berat sebelah itu. Apabila henti tamat, posisi terbuka akan bergerak ke arah taburan yang ditutup.

Jadi: perlu **+1.37%** setiap pusingan, dapat **-3.01%**. Jurangnya **4.38 mata peratus setiap pusingan**, 7.0 kali sebulan.

## 4. Pulangan PORTFOLIO sebenar (satu-satunya yang boleh didagangkan)

| Lorong | Sesi | Pulangan | Unjuran sebulan (21 sesi) |
|---|---|---|---|
| jalur rawak (median, 20 cabutan) | 8 | +1.40% | +3.70% |
| RAWAK_10 | 8 | +0.33% | +0.88% |
| GABUNGAN_10 | 4 | -0.05% | -0.24% |
| RISIKO_10 | 8 | -0.38% | -0.99% |
| TOP1_10 | 4 | -0.43% | -2.26% |
| RAWAK_KAEDAH_10 | 4 | -0.57% | -2.96% |
| RS_10 | 8 | -2.15% | -5.54% |

Unjuran terbaik: **+3.70% sebulan**, lawan sasaran +10%. **Unjuran daripada 4–8 sesi tidak bermakna** — ia disenaraikan hanya untuk menunjukkan tiada satu pun lorong berada di sekitar sasaran, bukan sebagai ramalan.

## 5. Jawapan

**Tidak, bukan pada apa yang data ini tunjukkan.** Untuk +10% sebulan portfolio perlu +1.37% setiap pusingan (7.0 kali sebulan). Pulangan realisasi sebenar ialah -3.01% — median -2.67% dengan kadar menang 17%. Jurangnya 4.38 mata setiap pusingan, bukan beberapa titik perpuluhan.

Ukuran portfolio sebenar mengatakan hal yang sama: tiada satu pun daripada enam lorong `portfolio_slot/` berada di sekitar sasaran.

**Had yang jujur:** data ini kurang sebulan dan 76% posisi belum ditutup. Ia **tidak** membuktikan sasaran itu mustahil secara kekal. Ia menunjukkan bahawa sekarang tiada satu pun tanda ke arahnya, dan jurangnya besar — bukan jenis jurang yang ditutup dengan menala parameter.

Baca semula dokumen ini selepas 6 bulan jejak hadapan. Bukan untuk mengesahkan sasaran, tetapi untuk melihat paras mana yang benar-benar dicapai.
