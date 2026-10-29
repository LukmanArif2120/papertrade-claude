# Jejak hadapan portfolio_slot lawan SPUS

Dijana 2026-10-29 07:03 UTC oleh `standard/banding_spus.py`. Rekod sahaja; tiada order, tiada wang sebenar.

Tempoh: **2026-10-16 hingga 2026-10-27 (8 sesi)**.

## 1. Jawapan pendek

Atas tingkap 8 sesi penuh (16 Oct–27 Oct), SPUS memberi **+0.28%** (MDD -1.87%).

**1 daripada 6 lorong mengalahkan SPUS**: `RAWAK_10`.

**Tetapi 8 sesi tidak boleh membezakan apa-apa.** Bahagian 3 mengira bila ia boleh. Sila baca bahagian itu sebelum menyimpulkan apa-apa daripada jadual di bawah.

## 2. Jadual

Setiap lorong dibanding dengan SPUS atas **tingkapnya sendiri**: lorong gabungan beku bermula 22 Okt, bukan 16 Okt, jadi satu angka SPUS tunggal tidak sah untuk semua.

| Lorong | Sesi | Mula | Pulangan | MDD | SPUS tingkap sama | Lawan SPUS | Persentil jalur |
|---|---|---|---|---|---|---|---|
| `RAWAK_10` | 8 | 10-16 | +0.33% | -2.23% | +0.28% | +0.06 mata | 30 |
| `GABUNGAN_10` | 4 | 10-22 | -0.05% | -1.44% | +1.23% | -1.27 mata | 20 |
| `RISIKO_10` | 8 | 10-16 | -0.38% | -2.10% | +0.28% | -0.66 mata | 15 |
| `TOP1_10` | 4 | 10-22 | -0.43% | -0.43% | +1.23% | -1.66 mata | 20 |
| `RAWAK_KAEDAH_10` | 4 | 10-22 | -0.57% | -1.07% | +1.23% | -1.80 mata | 10 |
| `RS_10` | 8 | 10-16 | -2.15% | -7.74% | +0.28% | -2.42 mata | 0 |

SPY atas tingkap 8 sesi: -0.46% (-0.74 mata lawan SPUS +0.28%). Rujukan sahaja — SPY bukan patuh Syariah.

Jalur rawak (20 cabutan berbenih berbeza, pembinaan sama): min -1.70% · p10 -0.55% · median +1.40% · p90 +3.25% · maks +3.68%, sisihan piawai **1.51 mata**.

Lajur persentil ialah bacaan yang betul, bukan lajur pulangan. Lorong di dalam jalur tidak dapat dibezakan daripada pemilihan rawak.

## 3. Bila perbandingan ini menjadi bermakna

Hingar pemilihan merentas 20 cabutan rawak ialah **1.51 mata** selepas 8 sesi sahaja. Ia berkembang seperti √T manakala kelebihan benar berkembang linear dengan T, jadi tingkap yang cukup panjang akhirnya memisahkan kedua-duanya. Sesi yang diperlukan sebelum kelebihan benar melepasi jalur (satu-hujung 95%):

| Kelebihan benar lawan SPUS | Sesi diperlukan | Lebih kurang |
|---|---|---|
| 20.0 mata/tahun | 122 | 0.5 tahun |
| 10.0 mata/tahun | 489 | 1.9 tahun |
| 5.0 mata/tahun | 1,954 | 7.8 tahun |
| 17.3 mata/tahun | 163 | 0.6 tahun ← hingar pemilihan `KEPEKATAN_BENIH.md` |

Maksudnya: walaupun satu lorong benar-benar mengalahkan SPUS **10 mata setahun**, ia memerlukan kira-kira **1.9 tahun** jejak hadapan sebelum kita boleh mengatakannya dengan yakin. Jurang yang lebih kecil memerlukan lebih lama lagi, mengikut kuasa dua.

Jurang setiap lorong dinyatakan dalam sisihan piawai jalurnya sendiri — itu bacaan yang betul, bukan membandingkan mata dengan mata:

- `RAWAK_10`: +0.06 mata = **+0.04 sd** jalur (persentil 30)
- `RISIKO_10`: -0.66 mata = **-0.44 sd** jalur (persentil 15)
- `RS_10`: -2.42 mata = **-1.61 sd** jalur (persentil 0)

Terbesar ialah **1.61 sd**, di bawah ambang satu-hujung 95% (1.645 sd). Tiada lorong boleh didakwa lebih baik atau lebih buruk daripada SPUS hari ini.

Satu bacaan yang perlu diperhatikan, bukan disimpulkan: `RS_10` berada di bawah **kesemua** 20 cabutan rawak (persentil 0), iaitu nilai-p satu-hujung ≈ 0.048. Itu di sempadan kelaziman — tetapi pada SATU tingkap 8 sesi, dan lorong itu sendiri juga hanya satu cabutan. Ia **tidak** dipradaftar sebagai ujian hadapan dengan peraturan keputusan, jadi ia perkara untuk diperhatikan apabila tingkap memanjang, bukan dapatan.

## 4. Apa yang perlu dibuat

1. **Jangan tukar apa-apa berdasarkan dokumen ini.** Ia terlalu awal; itulah keseluruhan maksudnya.
2. Biarkan `portfolio_slot/` terkumpul. Ia dibina semula setiap malam tanpa kos.
3. Baca semula selepas **6 bulan** (kira-kira 126 sesi) untuk tanda pertama, dan selepas **2 tahun** untuk keyakinan. Jadual bahagian 3 memberi angka tepatnya.
4. Apabila membaca semula, lihat **lajur persentil**, bukan lajur pulangan.

## 5. Had

- SPUS asas = **buka 16 Oct** kerana lorong beli pada buka sesi pertama. Menggunakan tutup hari itu sebagai asas memberi SPUS angka yang jauh berbeza; kesilapan itu lebih besar daripada jurang antara mana-mana dua lorong.
- MDD SPUS daripada tutup harian dalam tingkap ini, jadi ia tidak setara dengan `PENANDA_ARAS_SYARIAH.md` yang menggunakan median MDD tahunan daripada tutup bulanan. Pada tingkap sependek ini kedua-duanya hampir tidak bermakna.
- Lorong tidak membayar kos dagangan; SPUS juga tidak. Pusing ganti lorong jauh lebih tinggi, jadi ketiadaan kos **memihak kepada lorong**.
- `spus_harian.csv` disegarkan secara manual (`--kemas-kini`), bukan oleh workflow malam. Jika tempoh portfolio_slot melepasi liputan fail itu, skrip ini berhenti dan memberitahu, bukan meneka.
