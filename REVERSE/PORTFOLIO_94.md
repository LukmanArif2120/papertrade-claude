# Portfolio 94 kombinasi produksi lawan SPUS

Pradaftar `REVERSE/SPEC_PORTFOLIO_94.md` — dikomit sebelum keputusan dilihat.
Penanda aras SPUS: CAGR +17.95%  MDD -26.82%  nisbah 0.669

## Keputusan

| Lengan | Slot | Urutan | CAGR | MDD | Nisbah | Dedah | Dagangan | P1 | P2 | P3 | P4 | T1 |
|---|---|---|--:|--:|--:|--:|--:|:-:|:-:|:-:|:-:|:-:|
| P94 | 8 | U14 | +11.65% | -69.41% | 0.17 | 90% | 1337 | ✗ | ✗ | ✗ | ✗ | ✗ |
| P36 | 8 | U14 | +2.58% | -73.47% | 0.04 | 92% | 1379 | ✗ | ✗ | ✗ | ✗ | ✗ |
| P94 | 40 | U14 | +16.46% | -75.69% | 0.22 | 96% | 10064 | ✗ | ✗ | ✗ | ✗ | ✗ |
| P36 | 40 | U14 | +18.26% | -73.22% | 0.25 | 97% | 10297 | ✓ | ✗ | ✗ | ✗ | ✗ |
| PENUH | penuh | U14 | +2.99% | -41.04% | 0.07 | 100% | 2991935 | ✗ | ✗ | ✗ | ✗ | ✗ |
| UKAWAL | 8 | U01 | +9.11% | -46.54% | 0.20 | 98% | 915 | ✗ | ✗ | ✗ | ✗ | ✗ |
| UKAWAL | 8 | U02 | +11.65% | -69.41% | 0.17 | 90% | 1337 | ✗ | ✗ | ✗ | ✗ | ✗ |
| UKAWAL | 8 | U08 | +12.17% | -39.31% | 0.31 | 98% | 1061 | ✗ | ✗ | ✗ | ✗ | ✗ |

## Jalur kawalan RAWAK (20 benih)

| Slot | p5 | median | p95 |
|---|--:|--:|--:|
| 8 | -10.01% | +7.72% | +20.30% |
| 40 | +5.07% | +10.02% | +25.62% |

## TIGA KECACATAN PELAKSANAAN — dibaca SEBELUM mana-mana nombor di atas

Pelaksanaan tidak sepadan dengan spec saya sendiri pada tiga tempat. Ini ditulis sebelum
sebarang tafsiran supaya tiada dakwaan dibuat atas lengan yang cacat.

**1. `UKAWAL U02` BUKAN kawalan.** Cabang `U02` dalam `simulasi()` jatuh ke matriks
momentum yang SAMA seperti `U14`. Buktinya dalam jadual: barisnya **bit-identik** dengan
`P94 8 U14` — +11.65% / −69.41% / 0.17 / 90% / 1337 dagangan. Komen kod berkata "proksi RS
= momentum 6 bulan" tetapi tiada matriks RS 6 bulan pernah dibina. Baris itu mesti dibuang,
bukan ditafsir.

**2. `RAWAK` ialah kawalan URUTAN, bukan kawalan ISYARAT.** Spec §4 berkata "masuk rawak".
Pelaksanaan menghantar kolam calon `C94` yang SAMA dengan susunan rawak (`U01`). Jadi `P3`
seperti dilaksanakan menguji sama ada `U14` mengalahkan susunan rawak **daripada kolam
isyarat yang sama** — ia TIDAK menguji sama ada isyarat mengalahkan masuk rawak daripada
alam. Soalan isyarat-lawan-rawak kekal **TIDAK DIUKUR** oleh larian ini.

**3. `PENUH` bukan berat sama rata.** Saiz posisi = ekuiti ÷ bilangan calon **hari itu**,
yang berjulat 4,082–14,372 (median 8,476) — ayunan 2.7× daripada kepadatan isyarat semata-
mata, dan ia membelanja hampir seluruh ekuiti pada kolam hari pertama lalu kebuluran.
`+2.99%` itu **bukan** ujian `SZ10` dan tidak boleh dibaca sebagai menyangkalnya.

## Apa yang larian ini TETAP tetapkan dengan bersih

**P2 = 0 daripada 8, dengan margin besar.** MDD −39.31% (terbaik) hingga −75.69%
(terburuk) lawan SPUS **−26.82%**. Pendedahan 90–100% pada setiap lengan, jadi MDD dalam
ini **bukan** artifak pendedahan — ia benar-benar diambil. Bandingkan Sistem B Clenow, yang
MDD cetek HANYA kerana ia melabur 35.4%.

**P4 = 0 daripada 8.** Nisbah terbaik **0.31** lawan ambang **0.669**. Jadi campuran
SPUS+tunai mengalahkan setiap lengan pada paksi nisbah, pada pendedahan yang sama.

**T1 = 0.** Akibat P2. Kohort 94 ialah kohort **setiap dagangan**, bukan peruntukan modal —
dan kini itu diukur pada kohort yang SEBENARNYA dijalankan, bukan diwarisi daripada
`GB02_atau3` yang sudah bersara. Itu membetulkan kesilapan logik yang menyebabkan larian ini
wujud.

**`U14` — pemeringkat yang saya pilih TANPA ujian — dikalahkan oleh `U08` pada KEDUA-DUA
paksi.** `U08` (ATR% songsang) beri +12.17% / −39.31% / nisbah **0.31**; `U14` beri +11.65%
/ −69.41% / nisbah **0.17**. Bukan sedikit: MDD 30 mata lebih cetek pada CAGR yang lebih
tinggi. `U01` susunan rawak juga mengalahkan `U14` pada MDD (−46.54%). Jangkaan priori saya
#6 SALAH, dan ini dapatan yang boleh terus diguna.

**Hingar susunan pada 8 slot ialah 30 mata peratus.** Jalur rawak 20 benih: p5 −10.01%,
median +7.72%, p95 +20.30%. **Setiap** CAGR lengan jatuh DALAM jalur itu. Jadi pada 8 slot,
CAGR kohort ini tidak dapat dibezakan daripada hingar susunan pemilihan — pelajaran
`KEPEKATAN_BENIH.md` pada skala lebih besar. Itu sebabnya `P36` lawan `P94` (+2.58% lawan
+11.65% pada 8 slot; +18.26% lawan +16.46% pada 40) **tidak dapat diselesaikan** oleh larian
ini: jurang 9 mata duduk dalam jalur 30 mata.

**Kolam calon ialah median 8,476 pasangan (saham, keluar) setiap hari.** Dengan 8 slot itu
kadar pemilihan **0.09%** — kolam **1,060×** bilangan slot. Dapatan `KEPUTUSAN_AKHIR` (2)
memberi peraturan "kolam ≥ ~10× slot" untuk mengelak pemeringkat runtuh; di sini kita 100×
di seberang hujung itu. Pada saiz slot ini, **pemilihan slot menentukan portfolio, bukan
isyarat masuk**.

## Langkah seterusnya yang larian ini wajibkan

1. Buang baris `UKAWAL U02`; bina matriks RS 6 bulan yang sebenar jika kawalan itu mahu.
2. Tambah lengan `RAWAK-ALAM` yang benar: masuk rawak daripada alam cair, bilangan/hari
   dipadankan — supaya soalan isyarat-lawan-rawak akhirnya diukur.
3. Betulkan saiz `PENUH` kepada pecahan TETAP bagi ujian `SZ10` yang sah.
4. `U08` lawan `U14` patut diulang dengan jalur benih, kerana jurang 30 mata MDD itu lebih
   besar daripada apa-apa yang pernah diukur pada paksi urutan dan ia mungkin nyata.
