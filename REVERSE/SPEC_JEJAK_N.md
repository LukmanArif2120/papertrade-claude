# SPEC_JEJAK_N — pradaftar JEJAK HADAPAN kaedah Nxx dalam Papertrade C

**Dikomit SEBELUM mana-mana isyarat Nxx dibeli.** Ini bukan eksperimen ketujuh: baris gilir
E1–E6 ditutup (`KEPUTUSAN_AKHIR.md`) dan tiada gate baharu dibuka. Ini **pelaksanaan** —
memindahkan konfigurasi yang sudah diukur ke dalam saluran produksi supaya ia menghasilkan
data ke hadapan, iaitu langkah yang `STRATEGI.md` §3 sebut selepas `BERHENTI–TUTUP`.

## 1. Pembetulan kepada jawapan saya sendiri

Dalam dua giliran sebelum ini saya menjawab "belum sedia untuk papertrade" dengan memakai
gate **kajian** (kalahkan SPUS pada CAGR dan MDD) kepada soalan **operasi** (boleh dijejak
atau tidak). Itu salah secara struktur. Papertrade C maya dan tidak melibatkan wang; ia
sudah menjejak 134 kaedah Mxx yang **25 terbukti NEGATIF** pada BH-FDR dan **0 terbukti
positif** (`KAEDAH_TERBAIK.md`), dan `portfolio_slot/` sudah menjalankan lorong `RAWAK_10`
yang rawak tulen sebagai kawalan. Bar kemasukan ke Papertrade C dalam repo ini ialah
**direkod dengan jujur dan dilabel**, bukan **terbukti mengalahkan penanda aras**.

## 2. Konfigurasi, tepat

| paksi | pilihan | sebab |
|---|---|---|
| MASUK | `GB02_atau3` = `N19` ∪ `N37` ∪ `N115` | satu-satunya yang lulus gate0–gate3 |
| CARA | `C01` beli pada BUKA esok | satu-satunya yang dilaksanakan; `o[i+1]` enjin v1.2 |
| KELUAR lorong 1 | `X13` — `rsi14 > 70` → jual buka esok | keluar terbaik diukur (asas +4.350%) |
| KELUAR lorong 2 | `X15` Chandelier tutup 4×ATR14 | sudah dalam produksi; berjalan automatik |
| HENTI | **tiada** (`stop = NaN`) | kecacatan hari-0 mustahil secara struktur |
| SASARAN | **tiada** (`tgt = NaN`) | sasaran 1×ATR menukar asas +2.595% → −0.281% |
| TMAX | 126 bar | = `IMBAS` kajian; tiada dagangan melebihi yang diukur |
| URUTAN | `U14` momentum 12−1 bulan sebagai `rank` | lihat §2a |

Empat kaki dijejak **berasingan** juga (`N19`, `N20`, `N37`, `N115`) supaya sumbangan setiap
satu boleh dibaca, dan kerana `N20` ialah kaki keempat `GB02_atau4` yang hampir sama baik.

### 2a. Mengapa `rank` bukan 0

`harian_c.MAKS_KAEDAH = 10` mengehadkan **10 isyarat baharu setiap kaedah setiap imbasan**
dan memilih antara isyarat ikut lajur `rank`. Ujian asap mengukur `GB02` memberi ~30
isyarat/sesi, jadi had itu **mengikat**. Dengan `rank = 0` pemilihan antara 30 isyarat
menjadi **sewenang-wenang**, dan `KEPEKATAN_BENIH.md` mengukur hingar pemilihan merentas
susunan sewenang-wenang pada **17.3 mata peratus setahun** pada 8 slot. Itu lebih besar
daripada apa-apa kelebihan yang kajian ini pernah ukur, jadi `rank = 0` akan menenggelamkan
isyarat dalam hingar pelaksanaan.

`SISTEM.md` mengukur penyelesaiannya: sistem yang memeringkat ikut **skor objektif
berterusan** mempunyai sebaran benih **0.00 mata**. Jadi `rank` = `U14` momentum 12−1 bulan
(`C[-21] / C[-252] − 1`, formula `step27_keluar_portfolio.skor_pangkat` verbatim).

`U14` dipilih kerana ia pemeringkat terbaik dalam E6 (setiap pemenang `E6a` memakainya) DAN
boleh dikira daripada harga sahaja. `U02` (RS pasaran) sebenarnya lebih baik untuk
`GB02 × X13` dalam `portfolio_n_ringkas.csv` (CAGR 16.12 lawan 11.93 pada 8 slot), tetapi
`sedia(fr, idx)` hanya menerima harga — RS ditulis oleh workflow berasingan dan tidak
tersedia di dalam modul. Jadi ini pilihan **terbaik yang boleh dilaksanakan**, bukan
terbaik mutlak, dan itu had yang direkod.

**Dua lorong keluar repo memberi `X13` dan `X15` terukur bersebelahan tanpa kod tambahan.**
Itu kebetulan yang berguna: lorong 2 repo *ialah* `X15` kajian, bit untuk bit.

## 3. Apa yang DITETAPKAN dan apa yang TIDAK

**Ditetapkan** (`REVERSE/silang_akhir.csv`, dua tingkap, BH-FDR, gate0–gate3 lulus):
`GB02_atau3 × X13` memberi jangkaan **+8.541%** setiap dagangan (tahan) dan **+4.523%**
(latih), lift **+4.191 / +1.818**, menang **64.2%**, untung purata +25.68%, rugi purata
−22.14%, n **195,681**, p **0.0068**, dan `tanpa5` = **+2.858%**.

`tanpa5` positif ialah sebab utama konfigurasi ini dipilih. Halangan yang menjatuhkan hampir
setiap dapatan lain dalam kajian ialah "kelebihan hidup sepenuhnya dalam ekor kanan" —
`SETUP.md` mendapati **598/598** setup negatif selepas membuang 5% pemenang teratas. Buang
5% teratas daripada konfigurasi ini dan ia masih **+2.86%** setiap dagangan, lawan asas X13
**+0.912%**. Kelebihannya **tidak** bergantung kepada ekor.

**TIDAK ditetapkan:** prestasi portfolio. `portfolio_n_ringkas.csv` memberi CAGR **9.3–16.1%**
dengan MDD **−22% hingga −63%** lawan SPUS **+17.95% / −26.82%**; **0 daripada 36**
konfigurasi lulus. Jadi ini dijejak sebagai **kohort setiap dagangan**, BUKAN sebagai
peruntukan modal, dan **tidak** menggantikan `T4` (SPUS + tunai) sebagai cadangan modal.

**Satu pembetulan kepada `KEPUTUSAN_AKHIR.md` dapatan (2):** "isyarat masuk memusnahkan
pemeringkat" diukur pada keluar `X15` dan `X32`. Dengan keluar **`X13`**, isyarat
**mengalahkan** kawalan rawak dalam setiap sel: 16.12 lawan 14.23 (8 slot, U02), 14.74 lawan
4.30 (40 slot, U02), 13.92 lawan 9.23 (40 slot, U01). `P3` LULUS pada 4 daripada 6 sel X13.
Dapatan asal kekal benar bagi X15/X32; ia **tidak** am merentas keluar.

## 4. Jangkaan PRIORI (ditulis sebelum isyarat pertama)

1. Jangkaan setiap dagangan ke hadapan akan **lebih rendah** daripada +8.541%, kerana
   tingkap ujian dipilih selepas melihat data dan alam kajian tiada saham delist.
   Saya jangka **+2% hingga +5%** setiap dagangan ditutup pada 50 dagangan pertama.
2. Kadar menang akan **lebih dekat kepada 55–65%** daripada 64.2%.
3. **Kohort akan dilabel `BELUM CUKUP` untuk 3–6 bulan.** Ujian asap mengukur tempoh pegang
   median **50–64 hari** bagi `N19`/`N20`/`N115` dan **4 hari** bagi `N37`. Papan
   Penganalisis memerlukan ≥ 10 hari beli berbeza, dan `KAEDAH_TERBAIK.md` mengukur
   ~**77 posisi ditutup** diperlukan untuk membezakan dua kaedah yang berbeza 1 mata. Jadi
   jangan baca nombor kohort ini sebelum itu.
4. `N37` (gap-and-go, pegang 4 hari) akan matang **jauh lebih awal** daripada tiga yang lain
   dan akan menjadi satu-satunya yang boleh dibaca dalam bulan pertama.
5. Lorong 2 (`X15`) akan memberi kadar menang **lebih rendah** tetapi untung purata **lebih
   tinggi** daripada lorong 1 (`X13`) — kajian mengukur 42.8% / +36.95% lawan 64.2% /
   +25.68%. Kalau ke hadapan menunjukkan sebaliknya, salah satu lorong tersalah pasang.

Rekod priori saya: **15 betul · 3 separa · 13 salah** merentas enam pradaftar. Jangkaan di
atas tidak patut dipercayai tanpa ukuran; ia ditulis supaya boleh disemak.

## 5. Syarat TARIK BALIK (ditetapkan sekarang)

Jejak ini dihentikan dan dilaporkan sebagai gagal jika, pada ≥ **77 posisi ditutup** setiap
kohort dengan SE berkelompok ikut hari beli:

- **R1** jangkaan `GB02` **≤ 0** pada BH-FDR q ≤ 0.05 merentas lima kohort; **atau**
- **R2** `GB02` tidak mengalahkan purata lima kaedah Mxx rawak atas tingkap yang sama; **atau**
- **R3** kadar henti hari-0 > 1% (bermakna henti telah masuk semula secara tidak sengaja).

Lulus **tidak** bermakna sedia untuk wang sebenar; ia bermakna layak untuk ujian seterusnya.

## 6. Had

- Alam jejak = alam imbasan produksi (ditapis SPUS + `tidak_layak.py`), **bukan** alam `a02`
  kajian. Ini perbezaan yang `AL02` kenal pasti sebagai jurang penting, dan ia bermakna
  nombor ke hadapan tidak boleh dibandingkan terus dengan `silang_akhir.csv`.
- Kolam 12 signal `GABUNGAN.md` dipilih daripada data yang sama, jadi `GB02` **bersyarat**.
- Teks `Street Smarts` belum dibaca; `N115` daripada ringkasan pihak ketiga = SATU versi.
- `TMAX = 126` mengikat 4–15% dagangan dalam ujian asap, jadi ia bukan kekangan kosong.
- Jejak ini tidak menguji **saiz**, **slot** atau **imbang**. Paksi **urutan** dikunci
  `U14` (§2a) dan tidak diuji — ia dipilih untuk menghapuskan hingar pemilihan, bukan
  untuk diukur.
- `U02` (RS) lebih baik tetapi tidak boleh dicapai dari dalam `sedia()`. Kalau RS
  disediakan kepada modul kemudian, `U14` patut ditukar dan jejak dimulakan semula.

## 7. Pengesahan yang SUDAH dibuat sebelum spec ini dikomit

1. **Formula indikator bit-identik.** `kod/kaedah/_nxx.py` lawan `REVERSE/teras/ind.py` +
   `step18_nxx.tambahan` pada **30,828 bar × 60 ticker**: maks |Δ| = **0.000e+00** bagi
   `rsi14`, `adx14`, `bb_pctb`, `vol_n50`, `ema20`; **0 bar** berbeza bagi `sentuh_ema20`
   dan `gap_and_go`. Ini penting kerana `enjin.rsi` guna `ewm(alpha=1/n)` tanpa benih
   purata-n dan `enjin.atr` guna purata mudah — kedua-duanya **berbeza** daripada `_wilder`
   kajian. Memakai pembantu enjin akan menjejak peraturan yang bukan peraturan yang dikaji.
2. **Topeng bit-identik.** `N19`, `N20`, `N37`, `N115`, `GB02`, `X13`: **0 bar** berbeza
   merentas 30,828 bar (408 / 106 / 159 / 603 / 1,164 / 2,408 isyarat rujukan).
3. **Ujian asap merangkumi KOMBINASI masuk+keluar**, bukan komponen — itu pelajaran pepijat
   `X25` (`GABUNGAN.md`: `X25` pada asas memberi +2.273% yang kelihatan waras, tetapi pada
   `N19` ia artifak +18.52%). Keputusan asap pada stor repo (925 ticker, 2024-09…2026-10):
   `N19` menang 65.6% jangkaan +6.14% · `N20` 66.9% / +6.82% · `N37` 64.2% / +3.00% ·
   `N115` 67.1% / +6.21%.
4. **Henti hari-0 = 0 pada setiap modul**, dan dagangan ≤ 1 hari = 0.0–1.2%. Kecacatan
   `KOLAM_EKOR.md` §4a tidak hadir, mengikut binaan.
5. **Larian hujung-ke-hujung saluran produksi ke folder sandbox**, bukan ke
   `papertrade/`. Larian pertama mendedahkan pepijat yang kesemua ujian unit saya
   **terlepas**: pemuat produksi meletakkan `kod/` pada `sys.path` dan memanggil
   `importlib.import_module('kaedah.N19')`, jadi `kod/kaedah/` **tidak** pada path dan
   `import _nxx` gagal dengan `ModuleNotFoundError` pada kesemua lima kaedah — ujian saya
   lulus kerana ia meletakkan `kod/kaedah/` pada path sendiri. Dibetulkan dengan pola
   `try: from kaedah import _nxx / except ImportError: import _nxx` (preseden `_k145.py`),
   dan `test_import_seperti_produksi` kini mengimport melalui subproses dengan path yang
   **tepat** seperti produksi supaya kelas pepijat itu tidak boleh kembali.

   **Pelajaran kaedah, kedua dalam kajian ini:** `GABUNGAN.md` sudah menetapkan "ujian asap
   mesti merangkumi KOMBINASI masuk+keluar, bukan komponen". Tambahan sekarang: **ujian mesti
   merangkumi LALUAN IMPORT produksi, bukan laluan import ujian.** Ujian yang menyiapkan
   persekitarannya sendiri boleh lulus sambil produksi gagal sepenuhnya.

---

## 8. TAMBAHAN 1 Nov 2026 — tiga peraturan yang saya terlepas pandang

Pengguna bertanya mengapa hanya 5 daripada 147 boleh diguna. Semakan menunjukkan **pilihan
saya terlalu konservatif, bukan data yang terhad.** `REVERSE/nxx.csv` mengandungi **empat**
topeng MASUK yang melepasi gate2 (BH-FDR) DAN mempunyai jangkaan mutlak positif pada
kedua-dua tingkap — dan saya hanya mengodkan satu daripadanya (`N115`):

| topeng | peraturan | keluar | lift latih/tahan | jangkaan latih/tahan | n tahan |
|---|---|---|---:|---:|---:|
| `N75` | `rsi14 < 40` | `X3` | +0.647 / +1.587 | +1.851 / **+4.181** | 861,071 |
| `N17` | `rsi14` silang naik 30 | `X2` | +0.870 / +1.264 | +1.351 / +2.216 | 54,073 |
| `N16` | `rsi2 < 10` | `X2` | +0.211 / +0.305 | +0.692 / +1.257 | 567,422 |
| `N115` | Holy Grail | `X2` | +0.590 / +1.464 | +1.071 / +2.416 | 104,014 |

`N75` melepasi FDR pada **tiga** keluar (`X2`, `X3`, `X4`) dan mempunyai jangkaan mutlak
tertinggi antara kesemua topeng MASUK tunggal. Ketiga-tiga yang tertinggal ialah keluarga
**RSI** — sejajar dengan dapatan `NXX.md` bahawa `RSI` 18/28 dan `BB` 12/24 berbanding `MA`
0/20 dan `TREND` 0/24, iaitu pembalikan min berfungsi dan ikut-trend tidak.

Satu-satunya yang kekal **dikecualikan** ialah `N16 × X1`: lift +0.193 dan menang 62.4%
tetapi jangkaan mutlak **−0.088%** kerana asas `X1` sendiri −0.281%. Lift positif atas asas
negatif masih rugi; itu perangkap yang `CLAUDE.md` sudah catat.

### 8a. Masalah: ketiga-tiganya TIDAK pernah diuji terhadap `X13`

`nxx_keluar.csv` hanya menguji `ASAS`, `N19` dan `N115` terhadap 23 keluar. Jadi nombor
`N75`/`N17`/`N16` di atas ialah keluar `X2`/`X3`, bukan `X13` yang jejak ini gunakan.

Bukti bahawa `X13` mendominasi memang kukuh — pada **setiap** masuk yang pernah diukur
dengannya, `X13` memberi jangkaan tertinggi (`N19`: X13 **+11.285** lawan X15 +8.459 lawan
X17 +7.561; `N115`: X13 **+7.509** lawan X15 +6.060 lawan X17 +5.826; asas X13 +4.350 lawan
X15 +3.706 lawan X17 +1.855) — tetapi itu **ekstrapolasi**, bukan ukuran.

### 8b. Peraturan keputusan, dikomit SEBELUM mengukur

Saya akan mengukur `N16 × X13`, `N17 × X13`, `N75 × X13` pada panel, tingkap dan model kos
yang **sama**, kemudian:

**KODKAN** peraturan itu jika dan hanya jika **kesemua empat** benar:
1. `jangkaan_latih > 0`
2. `jangkaan_tahan > 0`
3. `lift_latih > 0`
4. `lift_tahan > 0`

**JANGAN kodkan** jika mana-mana satu gagal, tidak kira betapa baik nombor lain kelihatan.
Tiada kesatuan baharu dibina (itu akan menjadi eksperimen ke-7, yang dilarang). Ukuran ini
untuk menetapkan **jangkaan priori jejak**, bukan sebagai gate kajian baharu — ruang MASUK
kekal DITUTUP.

**Jangkaan priori saya: ketiga-tiganya LULUS**, kerana (a) ketiga-tiganya sudah mempunyai
jangkaan mutlak positif pada keluar yang lebih lemah, dan (b) `X13` mendominasi setiap keluar
lain pada setiap masuk yang diukur. Kalau mana-mana satu GAGAL, itu bermakna `X13` berinteraksi
dengan pembalikan min secara berbeza daripada yang saya jangka, dan itu dapatan yang lebih
berguna daripada tiga kohort tambahan.

### 8c. Had yang kekal

Mengodkan 8 daripada 147 **bukan** bermakna 139 yang lain belum sempat. 69 daripadanya
berstatus `PERLU` — ia memerlukan ~56 indikator atau sumber data berbeza yang repo tiada
(`harmonik`, `td_seq`, `talib_cdl`, `strat_bar`, `gmma`, `data_putcall`, `data_13f` …), jadi
ia **belum pernah diuji**. Mengodkannya bermakna meletakkan peraturan **tidak diuji** ke dalam
produksi, yang berbeza secara jenis daripada melaksanakan peraturan yang sudah diukur. Itu
keputusan pengguna, bukan keputusan saya. Baki ~70 diuji dan **gagal** — ia tidak patut
dikodkan.
