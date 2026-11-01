# MOMENTUM_PEGANG fasa 2 — top-N, paksi PEGANG, grid pattern × keluar

Dijalankan 1 Nov 2026. Pradaftar: `REVERSE/SPEC_MOMENTUM_PEGANG_2.md` (ditulis dan dikomit sebelum apa-apa
keputusan dilihat). Permintaan pengguna: tutup jurang **A**, **C**, **D** dalam `MOMENTUM_PEGANG.md` §8f.

Alam: A02, **9,038,796 sauh** (8,935,267 selepas membuang `kod==2`), 3,240 ticker, LATIH 2010–2019 /
TAHAN 2020–2026. Enam pembetulan audit fasa 1 diwarisi. Ujian signifikan utama ialah **bootstrap blok-bergerak
120 sesi** (300 cabutan, CI95), bukan SE berkelompok.

**Semakan integriti sebelum apa-apa pengukuran:** kiraan sauh fasa 2 = **9,038,796**, sepadan **tepat** dengan
fasa 1; merge `(ticker, tarikh)` 9,038,796 → 9,038,796 tanpa kehilangan baris; kunci unik dalam kedua-dua set;
invarian leg C diuji (baris tidak dipotong kekal sama tepat).

---

## Keputusan ringkas

| Leg | Soalan | Gate | Keputusan |
|---|---|---|---|
| **A** | Adakah 5 pemenang fasa 1 berfungsi pada 8–10 slot, bukan desil? | 0 / 28 | **TIDAK** |
| **C** | Adakah peraturan PEGANG (+5% dalam 3 hari) berfungsi sebagai strategi? | 0 / 4 | **TIDAK — ia merugikan** |
| **D** | Adakah ada interaksi pattern × parameter keluar? | D1 ya, **D2 tidak, D3 tidak** | **TIDAK** |

Satu pengecualian yang bertahan: **`S3` RS 6 bulan pada ganda 4 memberi +0.627 mata/bulan atas asas dalam
tingkap TAHAN dengan CI95 [+0.140, +1.121]** — satu-satunya kesan pattern yang signifikan dalam seluruh fasa 2.
Ia **tidak** berulang dalam LATIH dan ia **runtuh** pada slot kecil (§1).

---

## 1. LEG A — N teratas setiap hari lawan jalur RAWAK

Jalur `RAWAK` = 20 benih urutan rawak pada `N` yang sama; ambang A1 ialah **persentil 95 jalur itu**, bukan
beza dua titik (sebab: `KEPEKATAN_BENIH.md` mengukur hingar pemilihan 17.3 mata/tahun pada 8 slot).

### Pulangan per bulan pendedahan (LATIH | TAHAN)

| Lorong | N=8 | N=10 | N=20 | N=40 | A1 setiap N? |
|---|---|---|---|---|---|
| **H2 Minervini** | 1.534 \| 1.423 | 1.489 \| 1.644 | 1.475 \| 1.634 | 1.274 \| 1.641 | **YA** |
| **H1 Qullamaggie** | 1.222 \| 1.463 | 1.154 \| 1.511 | 1.100 \| 1.587 | 1.006 \| 1.470 | **YA** |
| S2 Clenow | 1.004 \| 0.903 | 0.957 \| 1.220 | 0.819 \| 1.462 | 0.797 \| 1.509 | tidak |
| D1 `vol_n50 ≥ 1.5` | 1.035 \| 0.790 | 1.041 \| 0.781 | 0.996 \| 0.885 | 1.013 \| 1.046 | tidak |
| S1 roc60 | 0.809 \| 0.600 | 0.760 \| 0.943 | 0.889 \| 1.409 | 0.935 \| 1.363 | tidak |
| **S3 RS SPY 6b** | **0.851 \| 0.090** | 0.996 \| 0.232 | 1.275 \| 0.338 | 1.145 \| 1.035 | tidak |
| S6 gabungan pangkat | 0.204 \| 1.498 | 0.363 \| 1.507 | 0.535 \| 1.474 | 0.801 \| 1.622 | tidak |
| *RAWAK (jalur p95)* | *0.909 \| 1.081* | *0.916 \| 1.092* | *0.929 \| 1.026* | *0.908 \| 0.966* | — |

| Gate | Lulus |
|---|---|
| A0 n ≥ 1,000 setiap sel | 28 / 28 |
| A1 > jalur p95 RAWAK pada KEDUA tingkap | 12 / 28 |
| **A2 CI95 bootstrap kecuali sifar (TAHAN)** | **0 / 28** ← pengikat |
| A3 `TANGKAP` per bulan ≥ RAWAK | 28 / 28 |
| **LULUS KESEMUA** | **0 / 28** |

### 1a. Dapatan: pemenang fasa 1 runtuh pada slot kecil

`S3` RS 6 bulan — satu-satunya pattern yang bertahan setiap ujian fasa 1 — memberi **0.090%/bulan** pada
TAHAN N=8, lawan jalur RAWAK **0.934%** (median). Ia meningkat **monotonik** dengan `N`
(0.090 → 0.232 → 0.338 → 1.035) dan hanya melepasi jalur pada N=40.

Maka `S3` ialah signal yang **bergantung kepada kepelbagaian**, bukan signal **pemilihan**. Kelebihan desil
fasa 1 (+1.286 mata/dagangan atas 441,412 sauh) ialah pernyataan tentang **taburan 10% alam**, bukan tentang
8 nama teratas. Perkara sama berlaku pada `S1`, `S2` dan `S6`: semuanya bertambah baik dengan `N`.

### 1b. Dapatan: pakej berbilang syarat menang di mana skor tunggal gagal

Hanya **dua** lorong melepasi jalur RAWAK pada **setiap** `N` dalam **kedua-dua** tingkap, dan kedua-duanya
ialah **penapis berbilang syarat**, bukan satu skor momentum:

| Lorong | Syarat | LATIH | TAHAN |
|---|---|---|---|
| `H2` Minervini | tutup > MA50 > MA150 > MA200 **DAN** dalam 25% tinggi 52w **DAN** ≥ 30% atas rendah 52w **DAN** `roc60` kuartil teratas | 1.274–1.534 | 1.423–1.644 |
| `H1` Qullamaggie | `roc60` desil teratas **DAN** `atr_pct ≥ 3` **DAN** dalam 25% tinggi 52w **DAN** nilai dagang ≥ $10j | 1.006–1.222 | 1.463–1.587 |

Perbezaan struktur: skor tunggal menyusun **seluruh** alam dan menolak pemilihan ke hujung ekstrem, di mana
fasa 1 §2f mengukur kemerosotan. Pakej berbilang syarat **membuang** hujung ekstrem itu dahulu (had ATR,
had jarak dari tinggi 52w, had kecairan), kemudian menyusun dalam baki yang lebih jinak.

### 1c. Dapatan: harga risiko pemilihan momentum, diukur

Diagnostik TAHAN N=8 (bukan gate):

| Lorong | %/bulan | Rugi > 50% | Persentil 5 | Menang |
|---|---|---|---|---|
| **RAWAK** | 0.75 | **0.23%** | **−22.67%** | 37.98% |
| H1 Qullamaggie | 1.46 | 1.88% | −40.33% | 33.38% |
| D1 `vol_n50 ≥ 1.5` | 0.79 | 2.49% | −40.58% | 35.79% |
| S2 Clenow | 0.90 | 2.61% | −42.36% | 31.92% |
| S6 gabungan | 1.50 | 2.72% | −42.92% | 31.57% |
| H2 Minervini | 1.42 | 2.78% | −44.25% | 33.32% |
| S3 RS SPY 6b | 0.09 | 3.02% | −45.03% | 29.37% |
| **S1 roc60** | 0.60 | **4.60%** | **−49.06%** | 31.14% |

Memilih nama momentum pada 8 slot **menggandakan** kerugian persentil-5 dan menaikkan kekerapan rugi > 50%
sebanyak **8–20×** berbanding cabutan rawak — manakala kelebihan puratanya **tidak** boleh dibezakan daripada
rawak (A2 = 0/28). Satu ukuran yang memihak kepada momentum: `TANGKAP` per bulan 8.5–11.5% lawan RAWAK 6.78%,
lulus 28/28. Jadi momentum **memang** menangkap trend besar lebih baik; ia juga membayar lebih banyak ekor kiri.

---

## 2. LEG C — paksi PEGANG sebagai STRATEGI: DITOLAK

Fasa 1 §3 mengukur `P(trend besar)` **BERSYARAT** pada pulangan 3 hari pertama. Fasa 2 menukarnya kepada
strategi penuh: cabang "potong" **merealisasikan** kerugiannya (jual pada buka hari ke-4).

| Tingkap | Peraturan | Dipotong | %/dagangan | **%/bulan** | Asas %/bulan | `TANGKAP`/bln | CI95 bootstrap |
|---|---|---|---|---|---|---|---|
| LATIH | `hari3 ≤ 0%` | 47.9% | 0.951 | **0.706** | 0.823 | 5.27 (asas 5.65) | **[−0.153, −0.073]** |
| LATIH | `hari3 ≤ +3%` | 84.9% | 0.253 | **0.486** | 0.823 | 5.20 | **[−0.479, −0.213]** |
| LATIH | `hari3 ≤ +5%` | 93.3% | 0.086 | **0.256** | 0.823 | 5.20 | **[−0.764, −0.396]** |
| LATIH | `hari5 ≤ +5%` | 88.2% | 0.266 | **0.507** | 0.823 | 5.30 | **[−0.501, −0.154]** |
| TAHAN | `hari3 ≤ 0%` | 49.8% | 0.938 | 0.795 | 0.900 | 6.35 (asas 6.83) | **[−0.170, −0.034]** |
| TAHAN | `hari3 ≤ +3%` | 79.1% | 0.518 | 0.854 | 0.900 | 6.55 | [−0.341, +0.163] |
| TAHAN | `hari3 ≤ +5%` | 88.5% | 0.334 | 0.797 | 0.900 | 6.73 | [−0.498, +0.208] |
| TAHAN | `hari5 ≤ +5%` | 82.6% | 0.568 | 0.922 | 0.900 | 6.72 | [−0.272, +0.266] |

**Gate C: 0 / 4 lulus.** Tujuh daripada lapan sel berada **di bawah** asas; dalam LATIH kesemua empat
mempunyai CI95 yang **mengecualikan sifar pada sisi negatif** = peraturan itu **signifikan merugikan**.
Kesemua lapan gagal C4 (`TANGKAP` rosak). Satu sel sahaja melepasi C1 (`hari5 ≤ +5%` pada TAHAN, 0.922 lawan
0.900) dan CI-nya merangkumi sifar.

### 2a. Mengapa statistik bersyarat fasa 1 menipu

Pecahan cabang menjelaskannya sepenuhnya (LATIH, ambang +5%):

| Cabang | n | % | Purata | Hari | `P(TB)` |
|---|---|---|---|---|---|
| **Potong** | 4,225,268 | **93.3%** | **−0.617%** | 4.0 | 18.27% |
| **Pegang** | 305,312 | 6.7% | **+9.807%** | 48.8 | **46.26%** |

Cabang pegang **memang** sebaik yang fasa 1 lapor. Tetapi untuk memilikinya anda mesti **membayar** 93.3%
dagangan yang dipotong pada kerugian. Henti lebar 4×ATR lorong 2 wujud **tepat** untuk mengelak jualan ke
dalam kelemahan itu, dan memperkenalkan semula potongan awal membatalkan sebab lorong 2 berfungsi.

**Pelajaran kaedah, bukan pelajaran pasaran:** `P(X | Y)` yang tinggi tidak bermakna "tapis dengan Y".
Ia hanya bermakna sesuatu jika `Y` diketahui **sebelum** komitmen modal. Di sini `Y` diketahui hari ke-3,
selepas modal dikomit, jadi penapis itu ialah **keputusan jual**, dan keputusan jual mesti dinilai bersama
kos jualannya. Fasa 1 §3 sudah menandakannya POST-HOC; fasa 2 menunjukkan mengapa tanda itu penting.

---

## 3. LEG D — grid pattern × parameter keluar

### Pulangan per bulan, 24 sel

| Baris | ganda 2 | ganda 3 | ganda 4 | ganda 6 |
|---|---|---|---|---|
| **LATIH** | | | | |
| ASAS (tiada pattern) | 0.674 | 0.769 | 0.823 | **0.906** |
| S3 RS SPY 6b D10 | 0.691 | 0.951 | 0.966 | **0.966** |
| H1 Qullamaggie | 0.467 | 0.745 | **0.915** | 0.767 |
| D1 `vol_n50 ≥ 1.5` | 0.777 | 0.824 | 0.869 | **0.947** |
| S4 hampir tinggi 52w D8 | 0.719 | 0.779 | 0.863 | **0.950** |
| H2 Minervini | 0.620 | 0.815 | 0.888 | **0.952** |
| **TAHAN** | | | | |
| ASAS (tiada pattern) | 0.602 | 0.831 | 0.900 | **1.011** |
| S3 RS SPY 6b D10 | 1.146 | 1.389 | **1.492** | 1.366 |
| H1 Qullamaggie | 1.344 | 1.136 | **1.476** | 1.332 |
| D1 `vol_n50 ≥ 1.5` | 0.916 | 1.198 | 1.182 | **1.267** |
| S4 hampir tinggi 52w D8 | 0.655 | 1.072 | 1.109 | **1.125** |
| H2 Minervini | 0.738 | 0.914 | 1.084 | **1.130** |

### 3a. Pembetulan kepada dapatan fasa 1 §8d

Fasa 1 menyapu ganda pada **763,327 dagangan enjin (set 431)** dan mendapati **4× ialah puncak**
(2.446%/bulan, dengan 6× pada 2.314%). Pada **alam A02 penuh** arahnya **berbeza**: pulangan per bulan naik
monotonik 2 → 3 → 4 → 6 bagi baris `ASAS` dalam **kedua-dua** tingkap, jadi anggaran titik memihak **6×**.

Tetapi perbezaan itu **tidak signifikan**: CI95 bootstrap bagi `ASAS g6 − ASAS g4` ialah
**[−0.081, +0.299]** (LATIH) dan **[−0.269, +0.344]** (TAHAN) — sifar di dalam kedua-duanya.

**Jadi pernyataan yang betul ialah:** ganda 4× dan 6× **tidak boleh dibezakan** pada A02; apa yang
**boleh** dibezakan ialah bahawa ganda **di bawah 3×** jauh lebih buruk (0.60–0.77 lawan 0.90–1.01).
Syor "kekalkan 4×" kekal sah, tetapi sebabnya ialah **plato**, bukan puncak. Ganda > 6 **tidak diuji** pada
A02 — itu jurang yang tinggal.

### 3b. Gate D

| Gate | Keputusan |
|---|---|
| D0 setiap sel ≥ 50,000 sauh | lulus |
| D1 ada (pattern, ganda) > sel `ASAS` terbaik pada kedua tingkap | **lulus** — `S3`@4: 0.966 > 0.906 (LATIH), 1.492 > 1.011 (TAHAN) |
| **D2 CI95 bootstrap kecuali sifar** | **GAGAL** |
| **D3 interaksi: ganda optimum pattern ≠ ganda optimum `ASAS`, bertahan dua tingkap** | **GAGAL** |

CI95 bootstrap bagi sel utama:

| Perbandingan | LATIH | TAHAN |
|---|---|---|
| `S3` g4 − `ASAS` g4 | +0.135 [−0.175, +0.418] | **+0.627 [+0.140, +1.121]** ← sifar di luar |
| `S3` g6 − `ASAS` g6 | +0.074 [−0.217, +0.369] | **+0.383 [+0.033, +0.756]** ← sifar di luar |
| `H1` g4 − `ASAS` g4 | +0.077 [−0.549, +0.742] | +0.573 [−0.345, +1.451] |
| `S3` g4 − `ASAS` g6 | +0.019 [−0.424, +0.375] | +0.575 [−0.060, +1.238] |
| `H1` g4 − `H1` g6 | +0.096 [−0.285, +0.453] | +0.213 [−0.304, +0.704] |

`H1` ialah satu-satunya baris yang ganda optimumnya 4× dalam **kedua-dua** tingkap manakala `ASAS` memilih 6×
dalam kedua-duanya — itu kelihatan seperti interaksi. Tetapi `H1 g4 − H1 g6` mempunyai CI yang merangkumi
sifar dalam kedua-dua tingkap, jadi ia **artifak anggaran titik**. **Tiada interaksi yang boleh dibuktikan:
pilih pattern dan pilih ganda secara berasingan.**

### 3c. Satu kesan pattern yang signifikan dalam seluruh fasa 2

`S3` RS 6 bulan pada ganda 4, tingkap TAHAN: **+0.627 mata/bulan atas asas, CI95 [+0.140, +1.121]**.
Had: ia tidak berulang dalam LATIH (+0.135, CI merangkumi sifar), dan leg A menunjukkan ia runtuh pada
8–10 slot. Jadi ia dapatan tentang **memegang 10% alam secara luas dalam tingkap 2020–2026**, bukan tentang
skrin yang boleh dijalankan dengan 8 slot.

---

## 4. Jangkaan priori saya (pradaftar §1–§3) — 1 betul, 2 salah

| Leg | Jangkaan | Keputusan |
|---|---|---|
| A | Tiada lorong lulus A1 pada N=8; sekurang-kurangnya satu lulus pada N=40 | **SEPARUH SALAH.** 4 lorong lulus A1 pada N=8 LATIH. Tetapi saya betul bahawa `S3` gagal di situ, dan betul tentang N=40 |
| C | C1 lulus tetapi C4 gagal | **SALAH, dan ke arah lebih buruk.** C1 sendiri gagal; dalam LATIH peraturan itu **signifikan merugikan** |
| D | D1 lulus tetapi D3 gagal | **BETUL.** D1 lulus pada anggaran titik, D3 gagal. Saya tidak meramalkan D2 juga gagal |

Corak kesilapan: dalam fasa 1 kesilapan saya ialah **reka bentuk** (tidak menormalkan volatiliti dan masa).
Dalam fasa 2 kesilapan saya ialah **terlalu optimistik tentang ruang yang sudah diukur kosong** — saya masih
menjangka peraturan PEGANG akan memperbaiki purata, walaupun `KOLAM_EKOR.md` sudah mengukur bahawa memotong
awal merosakkan ekor dan ekor itulah yang membayar.

---

## 5. Kiraan FDR

Leg A 28 ujian + Leg C 4 + Leg D 20 = **52 ujian**. Oleh kerana gate pengikat setiap leg ialah CI95 bootstrap
dan jumlah yang melepasinya ialah **1 daripada 52** (`S3`@g4 TAHAN), pembetulan BH-FDR tidak mengubah apa-apa:
pada 52 ujian, satu dapatan pada `p` ≈ 0.02 memberi `q` ≈ 1.0. **Tiada dakwaan signifikan dibuat selepas
pembetulan pelbagai ujian.**

---

## 6. Apa yang fasa 2 ubah dalam syor

| Syor fasa 1 | Status selepas fasa 2 |
|---|---|
| Susun watchlist ikut RS 6 bulan, ambil pangkat #9–40 | **DIPINDA.** RS 6 bulan runtuh pada 8–10 slot (0.090%/bulan lawan rawak 0.934%). Guna **pakej Minervini atau Qullamaggie** pada slot kecil |
| Kekalkan lorong 2 pada 4×ATR | **KEKAL**, tetapi sebabnya dibetulkan: 4× dan 6× tidak boleh dibezakan; yang pasti ialah **jangan** ke bawah 3× |
| Pradaftar ujian peraturan PEGANG (+5% dalam 3 hari) | **SELESAI dan DITOLAK.** Ia signifikan merugikan dalam LATIH |
| Jangan harap 8 slot menewaskan SPUS | **DIPERKUAT.** Pada 8 slot tiada lorong boleh dibezakan daripada rawak, dan risiko ekor kiri 8–20× lebih tinggi |

---

## 7. Had

- Bias penyintas A02 kekal (88.5% ticker hidup hingga hujung data).
- **74.3% keuntungan datang daripada saham di luar alam Syariah** (fasa 1); fasa 2 **tidak** membetulkannya.
- Leg A memodelkan **pemilihan slot**, bukan portfolio penuh: tiada had tunai, had korelasi atau imbangan semula.
  Ia menjawab "adakah N teratas lebih baik daripada rawak", bukan "berapa CAGR".
- Anggaran titik dalam §3b (jadual CI) dikira dengan **pemberat blok bertindih**, jadi ia berbeza sedikit
  daripada min sampel dalam jadual 24 sel. Perbezaan itu sebahagian besarnya hapus dalam **beza**, yang
  merupakan kuantiti yang CI diukur.
- Ganda > 6 tidak diuji pada A02.
- `S4` dikeluarkan daripada leg A (baldi tengah; "N teratas" tidak tertakrif) — sebab ditulis dalam pradaftar.
- Paksi CARA kekal `C01`; paksi SAIZ, IMBANG dan KORELASI masih tidak diuji.
- Leg C memodelkan kos 0.1% setiap belah tetapi bukan slippage; cabang potong menambah satu dagangan.
