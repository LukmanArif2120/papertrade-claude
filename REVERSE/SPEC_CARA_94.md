# Pradaftar — paksi CARA pada KESEMUA keluar kohort 94

**Dikomit sebelum sebarang keputusan dilihat.** Tarikh: 2 Nov 2026.

## 1. Mengapa larian ini WAJIB, dan mengapa ia bukan eksperimen baharu

`REVERSE/cara.csv` mengukur 6 cara pengisian pada `GB02_atau3 × X13`. `REVERSE/cara_94.csv`
(`step35_cara_94.py`) membetulkan separuh daripada masalah itu: ia mengarahkan kolam masuk
kepada **45 masuk produksi**. Tetapi keluarnya kekal `X13`, dan `X13` memegang **6 daripada
94** slot produksi. Laporan `CARA_94.md` menyatakan had itu sendiri:

> *"keputusan ini menjawab 'cara mana terbaik DIBERI X13', bukan 'diberi setiap kombinasi
> dengan keluarnya sendiri'. `X13` memegang 6 daripada 94 slot produksi, jadi pemindahan
> kepada 5 keluar yang lain ialah ANGGAPAN, bukan ukuran."*

Pengguna meminta kombinasi N yang **lengkap**. Satu paksi yang diukur pada 6% kohort dan
**dianggap** merentas 94% yang lain bukan lengkap. Larian ini menukar anggapan itu menjadi
ukuran: 6 cara × **6 keluar** × dua tingkap.

Ini **bukan** "eksperimen ke-7" yang dilarang. Larangan itu dipersetujui sebelum E1 dan
terpakai kepada **mencari** pembinaan portfolio yang mengalahkan SPUS. Di sini tiada carian:
kohort sudah dipilih, keluarnya sudah ditetapkan oleh `jejak_semua.csv`, dan satu-satunya
soalan ialah sama ada mekanik pengisian yang produksi SUDAH guna (`C01`) ialah pilihan yang
betul bagi keluar yang produksi SUDAH guna. Ia menutup jurang ukuran dalam kohort yang
dihantar, bukan membuka ruang carian baharu.

**Dapatan yang mencetuskannya:** `REVERSE/NXX_KELUAR.md` mengukur sebaran pilihan keluar
sebanyak **4.997 mata peratus** — ~12× lebih berpengaruh daripada pilihan masuk. Jika keluar
sebegitu berpengaruh, tiada alasan menganggap interaksi cara×keluar boleh dipindahkan.

## 2. Reka bentuk

| Paksi | Nilai |
|---|---|
| Keluar | `X13` `X14` `X15` `X16` `X17` `X36` — kesemua enam yang muncul dalam `jejak_semua.csv` |
| Cara | `C01`–`C06`, tiada perubahan daripada `step23_cara.py` |
| Masuk | **setiap keluar memakai masuk yang BERPASANGAN dengannya dalam produksi** (kesatuan `ATAU`) |
| Tingkap | LATIH 2012–2019 · TAHAN 2020–2025 |
| Alam | `AL01` (`autotune-data-a02`), cair `nilai20 ≥ USD100k` |
| Ufuk | 126 bar, kos penuh (komisen + slippage ikut `nilai20`) |

Bilangan masuk setiap keluar (daripada `jejak_semua.csv`, bukan tangan):
`X36` 37 · `X16` 26 · `X17` 10 · `X14` 10 · `X13` 6 · `X15` 5.

### 2.1 Satu enjin, bukan dua

`step23_cara.py` dijadikan boleh-tukar-keluar (`KELUAR_ID`) dan peraturan keluar
**diterjemahkan daripada `step33_portfolio_94.hari_keluar()`**, bukan ditulis semula daripada
ingatan. Tiada enjin CARA kedua. Lalai `X13` mesti kekal **bit-identik**: semakan md5
`cara.csv` dijalankan dan dilaporkan sebelum larian ini ditafsir. Jika md5 berbeza, larian
ini DIBATALKAN dan tampalan ditarik.

### 2.2 ATR `X15` diambil pada bar ISYARAT

`X15` ialah satu-satunya keluar dengan keadaan setiap posisi (puncak bergerak). Puncak
bermula pada bar **pengisian** (berbeza setiap cara, itu memang paksi yang dikaji) tetapi
lebar ekor `4×ATR14` diambil pada bar **isyarat** (sama merentas enam cara). Jika ATR
diambil pada bar pengisian, cara dan lebar henti bergerak serentak dan keputusan
mengelirukan kedua-duanya.

### 2.3 Had yang kekal, dinyatakan di awal

- `X15` dalam produksi ialah **lorong 2** (selari, tidak menyekat lorong 1), manakala di sini
  ia diuji sebagai lorong tunggal. Jadi baris `X15` menjawab "jika X15 ialah satu-satunya
  keluar", bukan "lorong 2 seperti dalam produksi".
- Masuk digabung dengan `ATAU` dalam setiap keluar. Itu menjadikan setiap sel = kolam bar
  yang kohort akan beli dengan keluar itu, tetapi ia **bukan** 94 ujian berasingan: ia 6.
- `C06` (bracket) mengandungi henti −3%, jadi `henti_hari0` dilapor dan baris itu mewarisi
  kecacatan henti hari-0 `KOLAM_EKOR.md` §4a dengan sengaja — itulah yang diukur.

## 3. Gate (ditetapkan SEBELUM keputusan)

Gate diwarisi daripada `SPEC_PORTFOLIO_N.md` §4.3 **seperti yang dikodkan dalam
`step23_cara.laporan()`**, tanpa satu pun definisi disentuh. Saya menyalinnya daripada kod,
bukan daripada ingatan, kerana menukar definisi gate selepas satu larian sudah dilihat ialah
tepat kecacatan yang audit `gate2` dedahkan (`AUDIT_JEJAK_N.md`):

- **CARA1** — `beza > 0` pada **kedua-dua** tingkap, di mana `beza` = purata pulangan setiap
  **ISYARAT** cara tolak `C01` (bar yang tidak terisi dikira **0**, bukan dibuang). Ini
  ukuran yang betul kerana ia tidak memberi kredit kepada cara yang hanya terisi pada bar
  yang menguntungkan.
- **CARA2** — `beza` lulus BH-FDR dengan t berkelompok ikut hari isyarat.
- **CARA3** — `jangkaan_sig > 0` (jangkaan MUTLAK setiap isyarat positif). Gate ini wujud
  kerana `SPEC_NXX` mendapati `N16×X1` lulus lift tetapi jangkaan mutlak −0.088% = merugikan.
- **MENANG** = CARA1 **DAN** CARA2 **DAN** CARA3 pada keluar yang sama.

**Satu-satunya perubahan: penyebut BH-FDR `m = 6` → `m = 30`.** Lima cara dibanding merentas
enam keluar = 30 perbandingan, jadi penyebut mesti mengikut ruang carian. Ini pembetulan ke
arah yang **LEBIH KETAT**, ditulis sebelum sebarang keputusan dilihat, dan ia bergerak ke
arah bertentangan dengan `m = 8` yang audit dedahkan (di sana penyebut dikecilkan sehingga
ambang menjadi p < 0.05 tanpa pembetulan).

`tanpa5` dilapor dalam setiap baris sebagai diagnostik ekor tetapi **bukan gate**, kerana ia
bukan gate dalam spec asal dan menambahnya sekarang akan menjadikan keputusan tidak boleh
dibanding dengan `cara.csv` dan `cara_94.csv`.

Perangkap yang gate mesti elak, direkod daripada pelajaran terdahulu:

- **Kadar isian bukan maklumat.** `C03`/`C04` (buy-limit) hanya diisi apabila harga jatuh,
  jadi `jangkaan_isi` tinggi boleh datang daripada **pemilihan** bar, bukan kelebihan. Itu
  sebab `jangkaan_sig` (setiap ISYARAT, bar tidak terisi = 0) dilapor bersebelahan, dan
  `CARA1` dinilai pada `jangkaan_isi` hanya kerana spec asal menetapkannya — mana-mana
  dakwaan produksi mesti menyebut **kedua-duanya**.
- **Kadar menang bukan maklumat** (`KOMBINASI.md`: 61.1% menang pada jangkaan −0.281%).

## 4. Jangkaan priori — ditulis sebelum larian

Rekod jujur: jangkaan priori saya SALAH pada 2/3 gate dalam tiga pradaftar berturut-turut
(SPEC_SILANG §7, SPEC_SISTEM §7, SPEC_NXX §7), dan SALAH pada jangkaan yang paling saya
yakin dalam SPEC_PORTFOLIO_94B §7. Jadi ini direkod sebagai kalibrasi, bukan ramalan.

1. **`C01` kekal menang atau seri pada majoriti keluar.** Kajian `X13` memberi 0/5 lulus
   `CARA1`. Keyakinan: sederhana.
2. **`C03`/`C04` kekal lebih baik setiap ISIAN tetapi gagal `CARA2` pada `m = 30`.** Mereka
   lulus `CARA1` setiap-isian dalam `cara_94` tetapi gagal keseluruhan; penyebut lebih ketat
   sepatutnya mengekalkan kegagalan itu. Keyakinan: tinggi.
3. **Interaksi cara×keluar WUJUD dan terbesar pada `X36`/`X16`.** Kedua-duanya keluar
   ikut-trend yang pegang lebih lama; pengisian lebih murah sepatutnya penting lebih sedikit
   apabila pegangan panjang. Jadi saya jangka sebaran cara MENGECIL pada `X36`/`X16`
   berbanding `X13`. Keyakinan: rendah — ini jangkaan yang paling mungkin salah.
4. **`C06` (bracket) terburuk pada setiap keluar**, kerana henti −3% memotong ekor kanan
   dan `KOLAM_EKOR.md` mengukur henti −2×ATR merugikan 9.79 mata/tahun. Keyakinan: tinggi.

## 5. Syarat BERHENTI

- Jika **tiada** cara lulus ketiga-tiga gate pada mana-mana keluar: paksi CARA **DITUTUP**.
  `C01` kekal dalam produksi atas sebab yang diukur merentas kesemua enam keluar kohort,
  bukan atas anggapan daripada satu keluar. Jangan daftar cara ke-7; jangan uji semula
  `C02`–`C06` pada varian lain.
- Jika satu cara lulus ketiga-tiganya pada ≥ 2 keluar yang **bersama-sama memegang ≥ 50
  slot**: itu cadangan perubahan produksi, dan ia mesti melalui jejak hadapan ≥ 126 sesi
  sebelum ditukar — bukan ditukar atas larian belakang ini.
- Jika satu cara lulus pada satu keluar sahaja: dilapor sebagai **BERSYARAT kepada keluar
  itu** dan tidak ditindaklanjuti, kerana dengan `m = 30` satu sel tunggal ialah tepat jenis
  dapatan yang pembetulan pelbagai ujian wujud untuk menolak.

## 6. Keluaran

`REVERSE/CARA_KELUAR_94.md` (laporan) + `REVERSE/cara_keluar_94.csv` (keputusan mentah, satu
baris setiap cara × keluar × tingkap). Kedua-duanya dijana oleh
`REVERSE/step38_cara_94.py`; jangan sunting dengan tangan.
