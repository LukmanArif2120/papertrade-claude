# CARA — bagaimana pesanan diisi (paksi CARA, C01–C06)

Pradaftar: `REVERSE/SPEC_PORTFOLIO_N.md` §4 (komit `5ad55ab`, sebelum larian).
Skrip: `REVERSE/step23_cara.py` · Data: `REVERSE/cara.csv`

Masuk `GB02_atau3` (N19 ∪ N37 ∪ N115), keluar `X13` (`rsi14 > 70` → jual buka esok),
ufuk 126 bar, kos penuh dua sisi, alam A02 cair. **195,706 isyarat** tingkap tahan
(2020–2025), **175,322** tingkap latih (2012–2019).

## Keputusan: 0 daripada 5 lulus

| Gate | | |
|---|---|---|
| CARA1 | beza jangkaan setiap SIGNAL > 0 pada kedua-dua tingkap | **0/5** |
| CARA2 | BH-FDR q ≤ 0.05, m = 6 dipradaftar | **0/5** |
| CARA3 | jangkaan mutlak setiap SIGNAL > 0 (tahan) | 4/5 |

**`C01` — "beli pada buka esok", iaitu apa yang repo sudah buat — adalah yang TERBAIK
daripada enam.** Tiada mekanik pengisian mengalahkannya. Setiap nilai p ialah 0.83–1.00
kerana setiap alternatif lebih teruk, bukan kerana ujian tidak berkuasa.

## Tingkap tahan 2020–2025

| cara | kadar isi | **jangkaan /SIGNAL** | jangkaan /isi | menang | tanpa 5% | harga masuk vs C01 | beza |
|---|---:|---:|---:|---:|---:|---:|---:|
| **C01** pasaran buka esok | 100.0% | **+8.540%** | +8.541% | 64.2% | +2.858% | – | – |
| C02 buy-stop `tinggi20×1.002`, 5 bar | 13.3% | +0.682% | +5.119% | 65.8% | −0.180% | +4.20% | −7.86 |
| C03 buy-limit `−1.5%`, 3 bar | 72.2% | +7.227% | **+10.011%** | 64.6% | **+3.945%** | −1.68% | −1.31 |
| C04 buy-limit `−1.0%`, 3 bar | 79.0% | +7.429% | +9.408% | 64.5% | +3.577% | −1.30% | −1.11 |
| C05 OCO `−2%` / `+2%`, 5 bar | 98.0% | +8.044% | +8.208% | 63.7% | +2.563% | +0.42% | −0.50 |
| C06 bracket `+6%` / `−3%` | 100.0% | **−0.591%** | −0.591% | 32.9% | −0.985% | – | −9.13 |

Tingkap latih memberi susunan yang **sama** pada setiap baris (C01 +4.523%, C02 +0.177%,
C03 +3.336%, C04 +3.655%, C05 +4.206%, C06 −0.299%).

## Tiga dapatan

### 1. Menunggu harga lebih baik memberi dagangan lebih baik — dan portfolio lebih teruk

`C03` dan `C04` memang berfungsi seperti yang sepatutnya: harga masuk **1.68%** dan
**1.30%** lebih murah daripada `C01`, jangkaan setiap dagangan terisi **naik** daripada
+8.541% kepada **+10.011%** dan **+9.408%**, dan jangkaan terpangkas-ekor juga naik
(+3.945% lawan +2.858%).

Tetapi kadar isi 72% dan 79%. **21–28% isyarat yang tidak pernah berundur bernilai lebih
daripada potongan harga pada yang berundur.** Jangkaan setiap SIGNAL jatuh kepada +7.227%
dan +7.429%.

Ini pengukuran, bukan tafsiran: kelebihan `GB02_atau3` tertumpu pada isyarat yang **terus
bergerak tanpa menoleh**. Sesiapa yang meletakkan limit di bawah untuk "masuk lebih baik"
secara sistematik terlepas yang itu.

### 2. Pengesahan harga memusnahkan dua kali

`C02` (buy-stop di atas tinggi 20 hari) mengisi hanya **13.3%** isyarat — dan jangkaan
setiap dagangan terisi pun **lebih rendah** (+5.119% lawan +8.541%), dengan
`tanpa5` **negatif**. Harga masuk 4.20% lebih mahal. Jadi ia kalah pada kedua-dua paksi
serentak, bukan menukar kadar isi dengan kualiti.

Jangkaan priori saya untuk `C02` **salah arah**: saya jangka kualiti setiap isian naik dan
hanya kadar isi turun. Kedua-duanya turun.

### 3. Sasaran untung memusnahkan segalanya — kali KELIMA diukur

`C06` (bracket `+6%` / `−3%`) menukar +8.540% menjadi **−0.591%**, dan kadar menang
64.2% → **32.9%**. Ini pengukuran kelima yang sama dalam repo ini: `KOMBINASI.md` sudah
mendapati sasaran 1×ATR menukar asas +2.595% menjadi −0.281%, dan `NXX_KELUAR.md`
mendapati `X10` (sasaran 2% tetap) menang **94.1%** dengan jangkaan **−0.023%**.

## Kecacatan henti hari-0: soalan itu salah tanya

`C06` memberi **65,240 daripada 195,681** dagangan dihentikan pada **bar masuk** = **33.3%**
(tahan) dan 20.0% (latih). `KOLAM_EKOR.md` §4a mengukur **23.8%** pada data hadapan sebenar
(421/1,770 posisi C). Simulator dan data hadapan bersetuju tanpa ditala — pengesahan luaran.

Tetapi dapatan sebenarnya ialah ini: **`X13` tiada henti langsung**, jadi di bawah `X13`
kecacatan hari-0 **tidak wujud** pada `C01` hingga `C05` — sifar, bukan dikurangkan.

Maka kecacatan hari-0 **bukan** disebabkan oleh "beli pada buka esok". Ia disebabkan oleh
**mempunyai henti ketat**. Menukar cara pengisian tidak membetulkannya; membuang henti ketat
membetulkannya sepenuhnya — dan itu tepat apa yang `NXX_KELUAR.md` sudah dapati secara
berasingan ("pegang sampai momentum habis; tiada sasaran untung, tiada henti ketat").

Dua kajian bebas, dua kaedah berbeza, satu kesimpulan yang sama.

## Jangkaan priori lawan keputusan

| | Saya jangka | Berlaku | |
|---|---|---|---|
| `C02` | setiap isian naik, setiap signal rata | setiap isian **turun** juga | **salah** |
| `C03`/`C04` | lebih teruk (beli penurunan yang terus turun) | setiap isian **lebih baik**, setiap signal lebih teruk | salah mekanisme, betul kesimpulan |
| `C06` | jelas lebih teruk | −0.591%, menang 32.9% | **betul** |
| henti hari-0 | ~24% | 33.3% tahan / 20.0% latih | hampir betul |

## Had

- Bersyarat: `GB02_atau3` dan `X13` dipilih daripada data yang sama.
- Tiada bar intrahari: setiap sentuhan stop/limit dianggarkan daripada tinggi/rendah harian.
  Bagi `C05` dan `C06`, apabila kedua-dua paras disentuh dalam bar yang sama, yang
  **merugikan kita** diandaikan berlaku dahulu.
- Alam A02 tiada saham delist.
- `m = 6` dipradaftar walaupun hanya 5 alternatif diuji (`C01` lawan dirinya adalah remeh);
  itu menjadikan ambang BH lebih ketat, bukan longgar.

## Tafsiran — paksi CARA pada 45 masuk produksi

Dijalankan oleh `REVERSE/step35_cara_94.py`, pradaftar `SPEC_PORTFOLIO_94B.md` §6.
Enjin sama (`step23_cara.py`), kolam diarahkan daripada `GB02_atau3` kepada kesatuan 45
masuk produksi. Keluar dikekalkan `X13` untuk MENGASINGKAN paksi CARA, jadi pemindahan
kepada 5 keluar produksi yang lain ialah **anggapan, bukan ukuran**.

### Keputusan: `C01` kekal. CARA1 = 0/5, CARA2 = 0/5.

Tiada mekanik pengisian mengalahkan `C01` (beli buka esok) setiap **isyarat**, pada
KEDUA-DUA tingkap, pada 4.16 juta isyarat tahan / 3.96 juta latih. Itu mengesahkan keputusan
asal `cara.csv` — yang diukur pada `GB02_atau3 × X13`, konfigurasi bersara berpangkat
7/1,496 — kini pada kohort produksi yang sebenar.

### Struktur nyata di dalamnya, konsisten dua tingkap

| Cara | Isi% tahan | /ISYARAT | /ISIAN | tanpa5 |
|---|--:|--:|--:|--:|
| `C01` | 99.9 | **+4.332** | +4.335 | 0.876 |
| `C03` limit −1.5% | 66.1 | +3.438 | **+5.203** | **1.314** |
| `C04` limit −1.0% | 74.8 | +3.635 | **+4.858** | **1.146** |

`C03`/`C04` memberi harga masuk LEBIH BAIK (+0.87 dan +0.52 mata setiap isian) **dan**
tanpa5 lebih baik (+0.44 dan +0.27 mata) — pada kedua-dua tingkap. Mereka kalah **hanya**
kerana 25–34% isyarat tidak pernah berundur untuk diisi.

**Mekanismenya mengikat kepada dapatan terbesar repo.** Isyarat yang limit order terlepas
ialah yang melonjak terus — **ekor kanan**. Jadi limit itu secara sistematik melepaskan
ekor, dan itu menjelaskan KEDUA-DUA arah serentak: `tanpa5` bertambah baik kerana ekor
dibuang daripada pengiraan, sementara jangkaan setiap isyarat jatuh kerana ekor itulah yang
membayar (`SETUP.md`, `KOLAM_EKOR.md` §2). Itu bukan mekanik gagal — ia pertukaran
kapasiti-lawan-ekor, dan `C01` menang kerana ia tidak melepaskan apa-apa.

### `C06` mengesahkan diagnosis henti hari-0 untuk kali ketiga

`C06` (bracket: pasaran + sasaran +6% + henti −3%) memberi **913,298** henti hari-0 tahan
dan **480,950** latih, dengan kadar menang 35.4%/39.2% dan jangkaan **NEGATIF** pada
kedua-dua tingkap (−0.465%/−0.275%). `C01`–`C05` memberi **SIFAR** henti hari-0, kerana 94
kombinasi produksi memakai `stop = NaN`.

Jadi puncanya ialah **mempunyai henti ketat**, bukan "beli pada buka esok" — sama seperti
`CARA.md` asal simpulkan, kini pada kohort produksi. Keputusan membuang henti secara
struktur (`stop = NaN`) disahkan betul.

### Had

Keluar dikunci `X13`, yang memegang 6 daripada 94 slot produksi. `X36` (37 slot) dan `X16`
(26 slot) TIDAK diuji pada paksi CARA. Jadi "C01 terbaik" disahkan untuk `X13` dan
dianggap untuk yang lain.
