# Pradaftar B — betulkan tiga kecacatan, tambah jalur benih, ukur paksi CARA

**Dikomit sebelum sebarang keputusan dilihat.** 2 Nov 2026.
Pindaan kepada `REVERSE/SPEC_PORTFOLIO_94.md`; keputusan larian A ada dalam
`REVERSE/PORTFOLIO_94.md` dan **tidak** ditarik balik — gate P2/P4/T1 di sana ditutup
dengan bersih. Yang dibetulkan di sini ialah tiga lengan yang pelaksanaannya tidak sepadan
dengan spec A.

Kod: `REVERSE/step34_portfolio_94b.py`. Keluaran: `REVERSE/PORTFOLIO_94B.md`,
`REVERSE/portfolio_94b.csv`.

## 1. Apa yang larian A tetapkan, dan kekal

- **P2 = 0/8**, MDD −39.31% hingga −75.69% lawan SPUS −26.82%, pendedahan 90–100%.
- **P4 = 0/8**, nisbah terbaik 0.31 lawan ambang 0.669.
- **T1 = 0.** Kohort 94 bukan peruntukan modal — diukur pada kohort yang SEBENARNYA
  dijalankan, bukan diwarisi daripada `GB02_atau3` yang bersara.
- Hingar susunan pada 8 slot = **30 mata peratus** (jalur p5 −10.01%, p95 +20.30%).
- Kolam median **8,476** pasangan/hari = **1,060×** bilangan slot pada 8.

Larian B tidak boleh membatalkan mana-mana daripada itu. Ia hanya menambah lengan yang
hilang.

## 2. Tiga pembetulan

**(a) `U02` ialah pendua `U14`.** Cabang `U02` memakai matriks momentum 12−1 yang sama;
barisnya bit-identik. Pembetulan: bina matriks momentum **6−1** yang sebenar
(`C[t-21] / C[t-147] − 1`) sebagai `U02`, berbeza secara angka daripada `U14`
(`C[t-21] / C[t-252] − 1`). Semakan wajib sebelum larian: korelasi Spearman antara dua
matriks itu mesti **< 0.99** pada sampel, jika tidak ia pendua lagi dan lengan dibuang.

**(b) `RAWAK` menguji susunan, bukan isyarat.** Pembetulan: lengan `RAWAKALAM` baharu —
masuk dicabut rawak daripada **alam cair** (`nilai20 ≥ 100,000`, harga buka esok sah),
bilangan calon setiap hari **dipadankan** dengan `P94` hari itu, keluar diberi dengan
mengambil sampel taburan keluar `P94` yang sama (`X36` 37 · `X16` 26 · `X17` 10 · `X14` 10
· `X13` 6 · `X15` 5). Jadi satu-satunya perbezaan antara `P94` dan `RAWAKALAM` ialah
**isyarat masuk**; kolam, kiraan, keluar dan pemeringkat dipadankan.

Ini soalan yang sepatutnya ditanya dari awal, dan **tiada** keputusan portfolio terdahulu
dalam repo menjawabnya: kawalan di E1–E6, `PORTFOLIO_N` dan larian A semuanya susunan
rawak atau masuk rawak dengan kolam yang TIDAK dipadankan.

**(c) `PENUH` bukan berat sama rata.** Saiz = ekuiti ÷ bilangan calon hari itu, berayun
2.7×. Pembetulan: pecahan **TETAP** `1/N_TETAP` dengan `N_TETAP = 200`, dan posisi baharu
dilangkau bila tunai habis. Itu ujian `SZ10` yang sah: berat sama rata, had tersirat oleh
tunai, bukan oleh kepadatan isyarat.

## 3. Jalur benih pada SETIAP lengan urutan

Larian A menjalankan `U14`, `U08`, `U01`, `U02` pada **satu** benih, lalu larian itu sendiri
mengukur hingar susunan 30 mata. Jadi "`U08` kalahkan `U14` 30 mata MDD" ialah satu
cabutan dalam jalur 30 mata — tidak boleh ditindaklanjuti.

Pembetulan: setiap urutan dijalankan pada **20 benih**. Untuk pemeringkat determinan
(`U14`, `U02`, `U08`) benih menjejaskan hanya pemecah seri, jadi jalurnya dijangka sempit;
itu sendiri maklumat. `U01` kekal jalur penuh.

Keputusan urutan dibuat pada **median** dan jalur p5–p95, bukan satu larian.

## 4. Grid B

| Lengan | Kolam | Slot | Urutan | Benih |
|---|---|---|---|---|
| `P94` | 94 kombinasi | 8, 40 | U14, U02, U08, U01 | 20 setiap satu |
| `RAWAKALAM` | masuk rawak, kolam/kiraan/keluar dipadankan | 8, 40 | U14 | 20 |
| `PENUH` | 94 kombinasi, pecahan tetap 1/200 | — | U14 | 1 |

= 2×4×20 + 2×20 + 1 = **201 larian**.

## 5. Gate — sama seperti spec A, tiada pelonggaran

P1 CAGR > 17.95% · P2 MDD ≥ −26.82% · P3 **median `P94` > p95 `RAWAKALAM` pada slot yang
sama** · P4 nisbah > 0.669 · T1 = P1 DAN P2 · T3 = CAGR ≥ 15% dengan MDD ≥ −15%.

`P3` kini bermakna apa yang spec A niatkan: **isyarat mengalahkan masuk rawak**, bukan
pemeringkat mengalahkan susunan rawak. Dinilai median-lawan-p95, bukan cabutan tunggal.

## 6. Paksi CARA pada 94 — dijalankan berasingan

`REVERSE/cara.csv` mengukur 6 cara pada `GB02_atau3 × X13` sahaja, dan di situ `C03`/`C04`
(buy-limit −1.5%/−1.0%) memberi jangkaan setiap **isian** LEBIH BAIK (+10.01%/+9.41% lawan
C01 +8.54%) dan `tanpa5` lebih baik (+3.94/+3.58 lawan +2.86) — tetapi kadar isi hanya
72.2%/79.0%, jadi jangkaan setiap **isyarat** lebih rendah.

`REVERSE/step23_cara.py` diarahkan semula kepada kesatuan 45 masuk produksi. Gate kekal
seperti `SPEC_CARA`: CARA1 beza > 0 dua tingkap · CARA2 BH-FDR · CARA3 jangkaan mutlak > 0.
Keputusan dilaporkan setiap **isyarat** DAN setiap **isian**, kerana kedua-duanya unit yang
sah dan memilih satu sahaja menyembunyikan pertukaran.

## 7. Jangkaan priori — direkod sebelum larian

Rekod saya dalam sesi ini: priori #2 dan #3 betul, #1 separa, #6 **salah**, #4 tidak dapat
diselesaikan, #5 tidak sah kerana kecacatan saya sendiri. Jadi:

1. **`P3` GAGAL** — isyarat tidak mengalahkan masuk rawak yang dipadankan. Sebabnya kolam
   1,060× slot: pada kadar pemilihan 0.09%, pemeringkat melakukan hampir semua kerja dan
   isyarat hanya menetapkan kolam. Ini jangkaan yang paling saya yakin dalam spec ini.
2. **`U08` kekal mengalahkan `U14` pada MDD** dengan jalur benih, kerana ATR% songsang
   memilih nama kurang turun naik secara mekanikal — itu kesan struktur bukan cabutan.
   Tetapi jurangnya akan **lebih kecil** daripada 30 mata.
3. **Jalur benih pemeringkat determinan sempit** (< 3 mata), jadi perbandingan urutan
   boleh dipercayai walaupun perbandingan CAGR mutlak tidak.
4. **`PENUH` pecahan tetap masih GAGAL P1**, dan lebih rendah daripada 40 slot.
5. **CARA: `C03`/`C04` mengalahkan `C01` setiap ISIAN tetapi kalah setiap ISYARAT**, jadi
   CARA1 lulus pada satu unit dan gagal pada satu lagi — dan itu sebabnya kedua-duanya
   mesti dilaporkan.

## 8. Syarat BERHENTI

Jika `P3` gagal pada kedua-dua slot: **ruang isyarat masuk untuk portfolio ditutup secara
muktamad**, bukan dengan inferens tetapi dengan kawalan yang dipadankan. Kohort 94 kekal
sah sebagai kohort setiap dagangan dan tiada larian portfolio lanjut dijalankan untuk Nxx.

Jika `P3` lulus: ia mesti diulang pada alam `AL02` sebelum sebarang dakwaan, kerana E4
mengukur `AL02` menyanjung MDD sebanyak 30.9 mata berbanding `AL04` titik-masa.
