# SPEC_CARIAN_SETUP — pradaftar carian setup berterusan (pusingan CS01)

**Dipradaftar 13 Nov 2026**, dikomit **sebelum** mana-mana keputusan carian dilihat. Kod: `kajian/carian_setup/`.
Keputusan pengguna 13 Nov 2026 (`koordinator/keputusan.csv`): carian kombinasi indikator dan penalaan dari benih M/N
dibenarkan **berterusan dan tanpa had bilangan**; **backtest dahulu, papertrade kemudian**. Ini pengecualian kedua kepada
"jangan cadang carian kombinasi lagi pada data lama" (`CLAUDE.md`).

## 1. Apa yang dicari (requirement pengguna, disahkan 13 Nov 2026)

Satu setup lengkap — bila masuk, bagaimana pegang, bila keluar — yang menangkap saham ketika ia mula naik kuat
(≥ 5 % minggu pertama, lebih baik ≥ 10 %, kemudian naik lagi 2–4 minggu) dan memegangnya selagi ia naik.

Peraturan WAJIB setiap setup (bukan pilihan carian):

| Perkara | Peraturan |
|---|---|
| Swing | tiada jual pada hari beli; pegang paling lama 20 sesi (4 minggu), sesi 1 = hari beli |
| Henti rugi | wajib, longgar sahaja: `H1` −8 % · `H2` −10 % · `H3` 3×ATR14 · `H4` 4×ATR14 di bawah harga beli |
| Sasaran untung | tiada sasaran tetap (10 % ialah matlamat, bukan paras jual) |
| Keluar | ikut indikator atau kombinasi dua indikator |

## 2. Apa ini, dan apa ia BUKAN

- Hasil ialah **papan pangkat backtest**, bukan bukti. `laporan/KAD_SKOR.md` kekal satu-satunya keputusan wang sebenar.
- Dapatan lama tidak dibatalkan: tinjauan ~1.35 juta gabungan (`KAJIAN_ISYARAT_KOMBINASI.md`) mendapati yang "terbaik"
  tidak mengatasi pilihan rawak pada saham lain. Sebab itu angka papan dilaporkan pada saham dan tahun yang carian
  **tidak pernah lihat** (§5 Kunci), bersebelahan dengan setup yang dipilih **rawak** daripada ruang yang sama.
- Tiada setup masuk papertrade daripada kajian ini tanpa keputusan pengguna yang berasingan.

## 3. Data dan tempoh

| Peranan | Saham | Tarikh isyarat |
|---|---|---|
| **Latih** (cari) | set 431 `data_mentah/dataset_S1–S4.csv` | 2020-01-02 … 2023-06-30 |
| **Sah** (pilih) | set 431 | 2023-07-03 … 2026-08-28 |
| **Kunci K1** (lapor) | 1,000 saham dipilih rawak (benih 20261113) daripada saham Release `autotune-data-a02` yang TIADA dalam set 431 | 2010-01-04 … 2019-12-31 |
| **Kunci K2** (lapor) | 1,000 saham yang sama | 2020-01-02 … 2026-08-28 |

Layak pada bar isyarat: ≥ 252 bar sejarah; set 431: tutup ≥ USD 10 dan purata 20 hari (tutup × volum) ≥ USD 1 juta;
Kunci: saham dalam universe bulanan titik-masa A02 (`teras/data.topeng`). Kaveat kekal: tiada saham delist dalam
kedua-dua set (angka condong ke atas); K2 berkongsi tahun dengan Latih/Sah (saham berbeza, pasaran sama).

## 4. Mekanik dagangan (dikunci)

- Isyarat dikira pada TUTUP bar *i* (data ≤ *i*); beli pada BUKA bar *i*+1, harga `P`. Pencetus = hari pertama isyarat
  (benar hari ini, palsu semalam).
- Henti: paras ditetapkan semasa beli (`H3`/`H4` guna ATR14 bar *i*). Aktif intrahari **mulai sesi 2**: buka ≤ paras →
  jual pada buka; rendah ≤ paras → jual pada paras. Sesi 1 (hari beli): jika TUTUP ≤ paras → jual pada buka esok.
- Keluar indikator: syarat dinilai pada tutup sesi 1…19 → jual pada BUKA sesi berikutnya.
- Tiada keluar hingga sesi 20 → jual pada TUTUP sesi 20.
- Kos 0.5 % pusingan. `R` = harga jual ÷ `P` − 1 − 0.005.
- Saham yang tiada 20 sesi selepas beli tidak dikira.

## 5. Ruang carian

**Masuk** = satu pencetus DAN 0, 1 atau 2 penapis.

- Pencetus indikator: senarai `PENCETUS` dalam `carian_setup/cs_atom.py` (silang MA, MACD, RSI, pecah tinggi N hari,
  Keltner/Bollinger, squeeze, Supertrend, ADX, Ichimoku, Stochastic, gap/lonjakan volum, tapak, undur dalam trend).
- Benih M: lajur `sig` setiap modul `AUTOTUNE/kaedah/Mxx.py` dengan parameter asal, **dan dua varian parameter** setiap
  kaedah: setiap parameter `tala = Y` diambil seragam dalam [`bawah`, `atas`] `param_julat.csv` (benih 20261113 + nombor
  varian). Varian yang gagal dijalankan dicatat dan ditinggalkan.
- Benih N: lajur `sig` setiap masuk N unik dalam `kod/kaedah/N*.py`.
- Penapis (keadaan): senarai `PENAPIS` (trend MA, RSI, MACD, ADX, Supertrend, kekuatan relatif, jarak puncak 52 minggu,
  volum, ATR %, squeeze, rejim QQQ, SPY > SMA200, bentuk lilin).

**Henti** = `H1`–`H4`. **Keluar** = senarai `KELUAR` (24 atom indikator) secara tunggal, pasangan ATAU (mana-mana satu
menyala), pasangan DAN (kedua-dua menyala), dan `X00` (tiada keluar indikator: henti dan had 20 sesi sahaja).

Setiap (masuk × henti × keluar) dinilai. Tiada had bilangan; bilangan sebenar dilaporkan.

## 6. Ukuran dan pemilihan (dikunci)

Setiap setup, setiap tempoh: `n`, purata `R`, sisihan piawai, **had bawah** `LB` = purata − 2 × sd ÷ √n.

1. **Peringkat besar** (semua kombinasi; isyarat bertindih pada saham sama dibenarkan): syarat `n` ≥ 100 dalam Latih
   DAN Sah. `skor` = min(`LB` Latih, `LB` Sah). Simpan 8 (henti × keluar) terbaik setiap peraturan masuk, dan satu
   (henti × keluar) rawak setiap peraturan masuk (kolam rawak).
2. **Peringkat tepat**: 2,000 teratas ikut `skor` (paling banyak 3 setiap peraturan masuk) dinilai semula dengan
   peraturan **satu posisi setiap saham** (isyarat semasa saham masih dipegang diabaikan). `skor tepat` dikira sama;
   syarat `n` ≥ 100 kekal.
3. **Papan 10 teratas** = susun `skor tepat` menurun; setiap benih muncul sekali sahaja (keluarga = ID kaedah M
   termasuk variannya, ID masuk N, atau ID pencetus indikator).
4. **Kunci**: 10 teratas, 200 teratas `skor tepat`, dan 200 setup rawak (benih 20261113, daripada kolam rawak) dinilai
   pada K1 dan K2 dengan peraturan satu posisi setiap saham. **Kunci tidak mengubah pangkat**; ia hanya dilaporkan.

Peratus yang dipaparkan bagi setiap setup papan (Latih, Sah, K1, K2):
bilangan dagangan · purata `R` · % menang · **% dagangan ≥ +10 %** · **% ≥ +20 %** · % rugi ≤ −8 % ·
% saham naik ≥ 5 % pada tutup sesi 5 (tanpa kos; sifat masuk) · purata sesi pegang · purata seminggu
(= purata `R` ÷ sesi pegang × 5) · lebihan atas beli rawak hari sama (purata `R` setup − purata `R` semua bar layak
pada tarikh isyarat yang sama dengan henti dan keluar yang sama) · MDD buku harian (semua posisi sama berat).

Tiga tapis (lajur ✓/✗, maklumat untuk keputusan papertrade kemudian):

| Tapis | Lulus jika |
|---|---|
| T1 tahan | `skor tepat` > 0 pada keempat-empat pilihan henti dengan masuk dan keluar yang sama |
| T2 tidak dilihat | purata `R` > 0 dalam K1 DAN K2 |
| T3 kalahkan rawak | purata `R` Kunci (K1+K2) > persentil ke-95 purata `R` Kunci 200 setup rawak |

Semakan kejujuran yang dilaporkan bersama: Spearman antara `skor tepat` dan purata `R` Kunci merentas 200 teratas
(adakah pangkat carian meramal hasil pada saham yang tidak dilihat), dan kedudukan median 10 teratas dalam taburan
rawak.

## 7. Keluaran

`kajian/CARIAN_SETUP.md` (dijana `carian_setup/cs_lapor.py`), `kajian/carian_setup/hasil/*.csv`. Fail perantaraan besar
ditulis ke folder kerja di luar repo. Jangan sunting keluaran secara manual.

### Pindaan 13 Nov 2026 (a) — keluarga F (sebelum carian dijalankan; tiada keputusan dilihat)

Keputusan pengguna 13 Nov 2026: kaedah baharu daripada carian ini didaftarkan dengan nombor bermula **`Fxx`**.
Setiap setup papan mendapat ID `F01`, `F02`, … mengikut kedudukan papan, dalam `data/registry_F.csv` (dijana
`carian_setup/cs_lapor.py`). ID **kekal**: takrif (`pencetus|penapis|henti|keluar`) yang sudah berdaftar mengekalkan
ID-nya pada pusingan berikutnya; takrif baharu mendapat nombor seterusnya. Lajur `status` = `BACKTEST` bermaksud belum
papertrade: tiada modul `kod/kaedah/Fxx.py`, tiada dalam Lejar atau kad skor. Pendaftaran tidak mengubah pemilihan
atau pangkat (§6).

### Pindaan 13 Nov 2026 (b) — pusingan CS02: dua era pada set 2000 (sebelum CS02 dijalankan)

**Apa yang sudah dilihat:** keputusan CS01 (`carian_setup/hasil/CS01/LAPORAN.md`). Setup teratas CS01 mengatasi setup
rawak pada saham lain dalam tahun yang sama (K2 2020–2026: median +2.05 % lawan −0.30 %) tetapi **tidak** pada tahun
lain (K1 2010–2019: −0.26 % lawan −0.23 %; Spearman −0.25). Keputusan pengguna 13 Nov 2026: jalankan pusingan kedua
pada set 2000 dengan syarat pemenang mesti untung dalam **dua era**. Tiada keputusan CS02 dilihat sebelum pindaan ini.

Yang berubah berbanding CS01 hanyalah data dan tempoh; mekanik (§4), ruang carian (§5: pencetus, penapis, henti,
keluar, benih M asal + varian 1 dan 2 yang sama, benih N) dan pemilihan (§6) **tidak berubah**.

| Peranan | Saham (Release `autotune-data-a02`, universe bulanan titik-masa) | Tarikh isyarat |
|---|---|---|
| **Cari E1** | kumpulan A | 2010-01-04 … 2019-12-31 |
| **Cari E2** | kumpulan A | 2020-01-02 … 2024-12-31 |
| **Kunci K1** | kumpulan B (saham yang carian tidak lihat) | 2010-01-04 … 2019-12-31 |
| **Kunci K2** | kumpulan B | 2020-01-02 … 2024-12-31 |
| **Kunci K3** | kumpulan B | 2025-01-02 … 2026-08-28 (**tahun yang tidak dipakai carian**) |

- Kumpulan A/B ialah pembahagian md5 sedia ada dalam `universe.parquet` (`SPEC_A02.md`); semua saham setiap kumpulan
  dipakai (tiada subsampel).
- `skor` = min(`LB` E1, `LB` E2), `n` ≥ 100 dalam E1 DAN E2: pemenang mesti mempunyai had bawah positif dalam **kedua-dua
  era**. Peringkat tepat, papan 10 teratas (satu setiap keluarga), 200 teratas dan 200 rawak seperti §6.
- Keputusan pengguna menyebut era 2020–2026; E2 dipendekkan ke 2024 supaya 2025 – Ogo 2026 kekal sebagai tempoh yang
  tidak pernah dilihat pemilihan (K3). Ini mengetatkan ujian, bukan melonggarkannya.
- Tapis: T1 seperti §6 (pada set cari). **T2** = purata `R` > 0 dalam K1, K2 **dan** K3. **T3** = purata `R` Kunci
  (K1+K2+K3) > persentil ke-95 purata Kunci 200 setup rawak. Laporan memecahkan semakan kejujuran mengikut setiap
  tempoh Kunci; **K3 ialah ujian sebenar**, kerana K1 dan K2 berkongsi tahun dengan carian.
- Kaveat tambahan: set 2000 bukan tapisan Shariah dan tiada saham delist. Kumpulan A dan B merangkumi saham set 431
  dan saham Kunci CS01, dan K3 bertindih dengan tempoh Sah CS01; maka K3 bersih bagi pemilihan CS02 sahaja, dan reka
  bentuk dua era ini sendiri dipilih selepas melihat CS01.
- Keluaran setiap pusingan diarkib dalam `carian_setup/hasil/<pusingan>/`; `kajian/CARIAN_SETUP.md` memaparkan pusingan
  terkini. ID keluarga F bersambung (takrif yang sama mengekalkan ID; ukurannya dikemas kini ke pusingan terkini).

### Pindaan 13 Nov 2026 (c) — semakan portfolio pada had MDD −10 % (sebelum dijalankan)

Keputusan pengguna 13 Nov 2026: Claude menentukan langkah seterusnya ke arah matlamat (untung bersih dengan MDD akaun
−10 %) dengan token sesedikit mungkin. Purata setiap dagangan bukan matlamat itu; semakan ini mengukurnya terus.
Tiada keputusan semakan ini dilihat sebelum pindaan ditulis; pangkat CS02 tidak berubah.

- Setup: 10 papan CS02 (`F11`–`F20`) satu demi satu, dan gabungan tujuh yang lulus tiga tapis.
- Data: kumpulan B (saham yang carian tidak lihat), isyarat 2010-01-04 … 2026-08-28, mekanik §4.
- Portfolio: 10 slot × 10 % ekuiti; isyarat dibeli pada buka esok jika ada slot kosong dan saham itu tidak sedang
  dipegang; slot kosong semula sehari selepas hari jual; lebih isyarat daripada slot → dipilih rawak (benih 20261113);
  pulangan harian = jumlah pulangan harian posisi terbuka ÷ 10; tunai 0 %.
- Ukuran: CAGR, MDD, purata pendedahan; kemudian **pada MDD −10 %**: pendedahan didarab `w` = min(1, 10 % ÷ |MDD|)
  (baki tunai) dan CAGR dikira semula. Juga dilaporkan untuk K3 sahaja (2025 – Ogo 2026).
- Kayu ukur tempoh sama: SPY beli-dan-pegang dengan skala yang sama (SPUS tiada sejarah sebelum Dis 2019).
- Bacaan: setup yang CAGR-nya pada MDD −10 % tidak melebihi SPY pada MDD −10 % tidak mendekatkan matlamat, walaupun
  purata setiap dagangannya positif. Keluaran: `carian_setup/hasil/CS02/PORTFOLIO.md` dan `portfolio.csv`
  (`cs_portfolio.py`). Maklumat sahaja; kad skor kekal satu-satunya keputusan wang sebenar.

### Pindaan 13 Nov 2026 (d) — pusingan CS03: pangkat ikut KADAR TANGKAP (sebelum dijalankan)

**Pembetulan arah.** Requirement yang disahkan pengguna (§1) ialah setup yang **paling kerap menangkap saham yang mula
naik kuat** (≥ 5 % minggu pertama, ≥ 10 %, kemudian naik lagi 2–4 minggu). CS01/CS02 memangkatkan ikut purata `R` setiap
dagangan, lalu memilih "beli ketika pasaran jatuh"; pindaan (c) pula mengukur lawan indeks, yang bukan soalan pengguna.
CS03 memangkatkan ikut apa yang dicari. Tiada keputusan CS03 dilihat sebelum pindaan ini. Data, tempoh, ruang masuk
(§5) dan mekanik (§4) sama seperti CS02 (cari kumpulan A: E1, E2; Kunci kumpulan B: K1, K2, K3).

Label setiap isyarat (beli pada buka esok, harga `P`; tetingkap 20 sesi; bebas daripada peraturan keluar):

| Label | Takrif |
|---|---|
| `m5` | tutup sesi 5 ≥ `P` + 5 % |
| `t10` | tutup mencapai ≥ `P` + 10 % **sebelum** henti −8 % kena (henti ikut mekanik §4 `H1`) |
| `t20` | sama, ≥ `P` + 20 % |
| `gagal` | henti −8 % kena sebelum `t10` |
| **`lari`** | `m5` DAN `t10` DAN tutup sesi 20 ≥ `P` + 10 % (naik minggu pertama, capai 10 %, dan masih di atas pada minggu ke-4) |

- **Asas rawak** setiap label = kadar label itu antara semua bar layak pada **hari yang sama dan tercile ATR % yang
  sama** (reka bentuk `standard/lift_kaedah.py`): menolak kesan hari pasaran dan kesan saham meruap. **Kelebihan** =
  kadar setup − asas.
- Peringkat besar: setiap peraturan masuk (pencetus × 0–2 penapis), `n` ≥ 100 dalam E1 DAN E2.
  `skor` = min merentas E1, E2 bagi [kelebihan `lari` − 2 × √(p(1−p)/n)].
- Peringkat tepat: 2,000 teratas dinilai semula dengan satu posisi setiap saham (pegang 20 sesi); papan 10 teratas
  (satu setiap keluarga), 200 teratas dan 200 peraturan rawak (benih 20261113) dinilai pada K1, K2, K3.
- Pegang/keluar bagi setiap masuk papan: (henti × keluar) dengan min(`LB` E1, `LB` E2) purata `R` tertinggi (§6.1),
  dilaporkan pada Kunci. Ini tidak mengubah pangkat masuk.
- Lajur ✓/✗: `T1` kelebihan `t10` > 0 dalam K1, K2 dan K3 · `T2` kelebihan `lari` > 0 dalam K1, K2 dan K3 · `T3`
  kelebihan `lari` Kunci (gabungan) > persentil ke-95 peraturan rawak. K3 ialah ujian sebenar.
- Keluaran `carian_setup/hasil/CS03/` (`cs_tangkap.py`); setup papan didaftarkan dalam keluarga F.

### Pindaan 13 Nov 2026 (e) — pusingan CS04: tala parameter di sekitar pemenang CS03 (sebelum dijalankan)

Matlamat tidak berubah: setup yang paling kerap menangkap saham "lari" (pindaan (d)). CS03 memilih 10 masuk terbaik
dengan tetapan tetap; CS04 **menala parameternya** ("tala dari benih"). Data, label, asas rawak dan `skor` sama seperti
CS03. Tiada keputusan CS04 dilihat sebelum pindaan ini.

- **Induk:** 10 setup papan CS03 (`F21`–`F30`).
- **Pencetus:** induk berasaskan kaedah M → 24 varian baharu; setiap parameter `tala = Y` diambil seragam dalam ±25 %
  nilai induk (dipotong pada [`bawah`, `atas`] `param_julat.csv`; integer dibundarkan; benih 20261113). Induk N dan
  indikator P tidak mempunyai parameter boleh tala dalam modulnya: pencetus kekal.
- **Penapis:** jenis penapis induk kekal; ambang penapis berambang ditala pada grid: RS ≥ {50, 60, 70, 80, 90, 95};
  ATR % ≥ {2, 3, 4, 5, 6, 8}; ≥ {20, 30, 40, 50, 60} % di bawah puncak 52 minggu. Penapis lain (rejim QQQ, Supertrend,
  SPY > SMA200, tutup > MA200) kekal.
- **Dataran, bukan puncak:** markah satu sel (varian × ambang) = **median** `skor` sel itu dan jiran ambangnya (grid
  3 × 3, sekurang-kurangnya 4 sel cukup isyarat; bila hanya satu ambang ditala: 3 sel sebaris, sekurang-kurangnya 2).
  Anak = sel bermarkah dataran tertinggi bagi setiap induk; jika sel induk sendiri yang tertinggi, induk kekal.
  Penilaian dengan satu posisi setiap saham; `n` ≥ 100 dalam E1 dan E2.
- **Ujian:** anak dan induk dinilai pada kumpulan B (K1, K2, K3). Laporan menyatakan berapa anak yang kelebihan
  `lari`-nya melebihi induk pada saham yang tidak dilihat, dan pada K3. Jika penalaan tidak menambah baik pada
  kumpulan B, itu dilaporkan sebagaimana adanya.
- Pegang/keluar anak: seperti pindaan (d). Anak didaftarkan dalam keluarga F (ID baharu, dengan catatan induknya).
  Keluaran `carian_setup/hasil/CS04/` (`cs_tala.py`).

### Pindaan 13 Nov 2026 (f) — kohort jejak hadapan F (ditulis sebelum keputusan CS04 dilihat)

Keputusan pengguna 13 Nov 2026: siapkan semuanya malam ini, termasuk papertrade bagi setup yang lulus; penentuan
diserahkan kepada Claude. Peraturan pemilihan dikunci di sini **sebelum** keputusan CS04 dibaca:

1. Bagi setiap induk CS03 (`F21`–`F30`): calon = **anak** CS04 jika induk itu ditala DAN kelebihan `lari` anak melebihi
   induk pada kumpulan B (gabungan K1+K2+K3) DAN pada K3; selainnya calon = **induk**.
2. Calon masuk kohort hanya jika `T1` dan `T2` benar baginya (kelebihan `t10` dan `lari` positif dalam K1, K2 dan K3).
3. Setiap ahli kohort dijejak dengan cara pegang dan keluar terbaiknya (pindaan (d)), mekanik §4 tanpa perubahan.

Jejak hadapan ialah **penjejak berasingan** (`carian_setup/cs_hadapan.py`, folder `BacktestShariah2/jejak_f/`), bukan
Lejar: mekanik §4 (henti ikut harga beli, tiada jual hari beli, keluar bergantung laluan) tidak sama dengan enjin v1.2,
dan ukuran yang dijejak ialah kadar tangkap. Ia tidak menyentuh Lejar, Papertrade C, kad skor atau dashboard. Alam =
stor harga (senarai Shariah semasa); layak seperti set 431. Hanya isyarat pada atau selepas **2026-11-13** dikira
(tiada isian ke belakang). Kad skor kekal satu-satunya keputusan wang sebenar: setup F yang terbukti dalam jejak ini
masih perlu keputusan pengguna dan integrasi Lejar sebelum boleh dinilai kad skor.

### Pindaan 13 Nov 2026 (g) — tambahan kohort selepas hasil dilihat (POST-HOC, dilabel begitu)

Semakan semula lawan matlamat pengguna (menangkap saham yang naik kuat **dan untung**): peraturan (f) memilih anak `F34`
menggantikan induk `F24` kerana kadar tangkapnya lebih tinggi, tetapi dengan cara pegang terbaik masing-masing induk
`F24` positif setiap dagangan dalam K1, K2 dan K3 (+0.79 / +1.19 / +0.50 %) manakala `F34` tidak (+0.07 / −0.77 / −0.83 %).
`F24` juga lulus `T1`, `T2` dan `T3`. Maka **`F24` ditambah ke kohort** supaya kedua-dua versi dijejak ke hadapan.
Ini keputusan selepas melihat hasil, bukan pradaftar; ia hanya MENAMBAH satu ahli dan tidak membuang mana-mana ahli
peraturan (f). Tiada tambahan lain.

### Pindaan 14 Nov 2026 (h) — tinjauan PRASYARAT (isyarat bukan daripada harga saham itu sendiri; sebelum dijalankan)

Permintaan pengguna 14 Nov 2026: prasyarat setup F setakat ini hanya rejim QQQ dan SPY > SMA200; selidik prasyarat lain
(earnings, sektor, industri, keadaan pasaran) "secara kreatif". Ini **tinjauan pengukuran**, bukan pemilihan setup: ia
mengukur sama ada setiap prasyarat mengubah kadar saham "lari" (pindaan (d)). Tiada hasil dilihat sebelum senarai ini
ditulis. Senarai dan takrif tepat: `carian_setup/cs_prasyarat.py` (`PRASYARAT`).

| Kumpulan | Prasyarat |
|---|---|
| A. Arah pasaran | QQQ ON / OFF · SPY atas / bawah SMA200 · QQQ dalam 3 % dari puncak 52 minggu · QQQ ≥ 10 % / ≥ 20 % di bawah puncak · rejim ON baharu (≤ 10 sesi) · rejim OFF baharu (≤ 10 sesi) · QQQ RSI14 < 35 · QQQ naik ≥ 3 % dalam 5 sesi |
| B. Turun-naik pasaran | turun-naik SPY 21 hari ≥ 25 % setahun · ≤ 10 % · sedang menurun (21 hari < 63 hari) |
| C. Keluasan pasaran (semua saham set 2000 yang layak) | ≥ 60 % saham di atas MA50 · ≤ 30 % · keluasan naik ≥ 10 mata dalam 10 sesi · ≥ 60 % di atas MA200 · ≥ 15 % saham dalam 5 % dari puncak 52 minggu |
| D. Sektor saham itu (11 sektor) | sektor 3 teratas ikut pulangan 63 sesi · 3 terbawah · ≥ 60 % saham sektor di atas MA50 |
| E. Industri saham itu (≥ 5 saham layak) | industri 20 % teratas ikut pulangan 63 sesi · 20 % teratas ikut 21 sesi · 20 % terbawah (63 sesi) · ≥ 60 % saham industri di atas MA50 · ada saham LAIN dalam industri sama yang naik ≥ 20 % dalam 20 sesi |
| F. Earnings syarikat (8-K item 2.02; `data/sec/`) | earnings dalam 1–5 sesi akan datang · 0–4 sesi selepas earnings · 5–19 sesi selepas · tiada earnings dalam 20 sesi akan datang · kejutan untung terkini positif (SUE > 0) · hasil suku terkini tumbuh ≥ 20 % · harga melompat ≥ 5 % pada hari earnings (dalam 20 sesi lalu) |
| G. Kalendar | Nov–Apr · Mei–Okt · 7 hari pertama bulan · Januari |

- Ukuran: kadar `lari`, `t10`, `gagal` antara bar layak bila prasyarat BENAR lawan PALSU, dalam lima kepingan: kumpulan A
  (E1, E2) dan kumpulan B (K1, K2, K3). Prasyarat "konsisten" jika kadar `lari` BENAR > PALSU dalam kelima-lima kepingan.
  Ukuran yang sama bagi isyarat lapan setup kohort (gabungan), satu posisi setiap saham.
- Kaveat dikunci: prasyarat pasaran berubah ikut HARI, jadi bilangan pemerhatian bebasnya kecil walaupun bar banyak;
  "earnings akan datang" memakai tarikh sebenar (syarikat biasanya mengumumkan tarikh lebih awal, tetapi ini pandang ke
  hadapan yang ringan); peta sektor/industri ialah peta semasa; tiada saham delist.
- Hasil hanya maklumat. Prasyarat yang konsisten boleh dimasukkan sebagai penapis baharu dalam pusingan carian seterusnya
  (pindaan berasingan). Keluaran: `carian_setup/hasil/PRASYARAT/`.

### Pindaan 14 Nov 2026 (i) — pusingan CS05: PRASYARAT + SYARAT bagi SEMUA kaedah (sebelum dijalankan)

Keputusan pengguna 14 Nov 2026: CS01–CS04 ialah pusingan "syarat sahaja"; jalankan carian sekali lagi untuk **semua**
kaedah (M, N dan indikator, bukan 50 teratas) dengan **prasyarat, kemudian syarat**, dan tunjukkan bagi setiap kaedah
hasil syarat sahaja lawan hasil dengan prasyarat. Butiran teknikal diserahkan kepada Claude. Matlamat tidak berubah (§1,
pindaan (d)): setup yang paling kerap menangkap saham "lari".

**Apa yang sudah dilihat sebelum pindaan ini:** CS01–CS04 dan tinjauan (h), termasuk kadar lari bila setiap satu daripada
38 prasyarat (h) benar/palsu pada kumpulan A DAN B (semua bar layak dan isyarat kohort F). Maka kesan utama 38 prasyarat
itu bukan lagi "tidak dilihat" pada kumpulan B; yang belum dilihat ialah gabungannya dengan setiap pencetus, prasyarat
takrif pakar (`QH`), dan mana-mana hasil CS05. Supaya tiada pemilihan selepas melihat, **kesemua 38 prasyarat (h)
dimasukkan** (yang membantu dan yang tidak). Kod: `carian_setup/cs_lapis.py` (prasyarat) dan `cs_cs05.py` (carian, laporan).
Data, tempoh, mekanik (§4), label dan 500 pencetus sama seperti CS02–CS03 (cari kumpulan A: E1, E2; Kunci kumpulan B: K1,
K2, K3).

**1. Ruang carian.** Peraturan masuk = [0–1 prasyarat PASARAN] DAN [0–1 prasyarat KUMPULAN/SYARIKAT] DAN satu pencetus
DAN [0–2 penapis SAHAM].

- Pencetus: kesemua 500 (49 indikator, benih M asal + 2 varian, benih N); tidak berubah.
- Penapis saham: 27 = `PENAPIS` tanpa `F26`, `F27`, `F28` (ketiga-tiganya berpindah ke lapisan prasyarat); 379 gabungan.
- Prasyarat PASARAN (33; sama bagi semua saham pada hari itu): `QA01`–`QA11`, `QB01`–`QB03`, `QC01`–`QC05`,
  `QG01`–`QG04` = prasyarat A, B, C, G pindaan (h) dengan takrif `cs_prasyarat.py` yang sama, dan sepuluh takrif pakar
  `QH01`–`QH10` di bawah.
- Prasyarat KUMPULAN/SYARIKAT (15; bukan harga saham itu sendiri tetapi berbeza antara saham): `QD01`–`QD03` (sektor),
  `QE01`–`QE05` (industri), `QF01`–`QF07` (earnings) = prasyarat D, E, F pindaan (h), takrif sama. Tanpa data → PALSU.
- Bilangan: 34 × 16 × 500 × 379 = **103,088,000** peraturan masuk. Tiada had bilangan; bilangan sebenar dilaporkan.

| ID | Prasyarat takrif pakar (dikunci; data ≤ hari itu; "saham layak" = bar layak kedua-dua kumpulan) |
|---|---|
| `QH01` | **Follow-through day aktif (O'Neil), pada QQQ.** Hari rendah = rendah hari itu ialah rendah terendah 20 sesi (termasuk hari itu) DAN tutup ≤ 0.93 × tutup tertinggi 252 sesi. FTD = sesi ke-4 hingga ke-12 selepas hari rendah terkini, tutup naik ≥ 1.5 % berbanding semalam, volum > volum semalam. BENAR dari hari FTD selama 20 sesi; terbatal sebaik QQQ tutup di bawah rendah hari rendah itu atau hari rendah baharu muncul |
| `QH02` | Distribution day QQQ (tutup turun ≥ 0.2 % dengan volum > semalam) **≤ 2** dalam 25 sesi terkini |
| `QH03` | Distribution day QQQ **≥ 5** dalam 25 sesi terkini |
| `QH04` | **Breadth thrust (Zweig) aktif.** Nisbah = saham naik ÷ (naik + turun); EMA 10 hari nisbah > 0.615 hari ini dan < 0.40 pada sekurang-kurangnya satu daripada 10 sesi sebelumnya. BENAR 20 sesi dari hari itu |
| `QH05` | **Nisbah 4 % (Stockbee) > 2**: jumlah 10 hari bilangan saham tutup naik ≥ 4 % ÷ jumlah 10 hari turun ≥ 4 % |
| `QH06` | Nisbah 4 % **< 0.5** |
| `QH07` | **Regangan turun-naik (Connors; PROKSI, tiada VIX dalam repo).** Sisihan piawai pulangan harian SPY 10 sesi ≥ 1.05 × purata 10 sesinya selama 3 sesi berturut, DAN SPY > SMA200 |
| `QH08` | QQQ SMA10 > SMA20 (Qullamaggie) |
| `QH09` | **Peringkat 2 Weinstein, indeks**: SPY > SMA150 DAN SMA150 > SMA150 20 sesi lalu |
| `QH10` | **Hari 90 % (Lowry; kiraan saham, bukan volum).** Hari ≥ 90 % saham turun, kemudian dalam 10 sesi: satu hari ≥ 90 % naik atau dua hari berturut ≥ 80 % naik. BENAR 20 sesi dari hari naik itu |

**2. Dua skor (kedua-duanya kadar tangkap; `n` ≥ 100 dalam E1 DAN E2; formula pindaan (d)).**

- `skor_pilih` = min merentas E1, E2 bagi [kelebihan `lari` atas saham rawak **hari sama** × tercile ATR % sama − 2 ralat
  piawai]. Ini kayu ukur pindaan (d) tanpa perubahan: kemahiran MEMILIH saham. Prasyarat pasaran menaikkan saham rawak
  hari itu juga, jadi ia hanya menambah skor ini jika pencetus memilih lebih baik pada hari begitu.
- `skor_jumlah` = formula sama, tetapi asas = kadar `lari` semua bar layak dalam **era yang sama** × tercile ATR % sama
  (tercile dikira dalam hari). Ia memasukkan kesan BILA membeli, iaitu sumbangan prasyarat pasaran. Hari isyarat
  berkelompok, jadi ralat piawainya terlalu kecil; sebab itu papan skor ini wajib dibaca bersama plasebo (butir 5c) dan
  bilangan hari isyarat berbeza.

**3. Peringkat tepat, papan dan Kunci (bagi setiap skor secara berasingan).** 2,000 peraturan teratas dinilai semula dengan
satu posisi setiap saham (pegang 20 sesi). **Papan 10 teratas** ikut skor tepat: satu setiap keluarga pencetus; setiap
prasyarat muncul paling banyak 3 kali; setup tanpa prasyarat paling banyak 3. Papan, 200 teratas dan 200 peraturan rawak
(dicabut seragam daripada semua peraturan yang diskor, benih 20261113) dinilai pada K1, K2, K3. Henti × keluar setiap
setup papan dipilih seperti pindaan (d). Lajur ✓/✗ (kelebihan ikut asas papan itu): `T1` `t10` > 0 dalam K1, K2, K3 · `T2`
`lari` > 0 dalam K1, K2, K3 · `T3` `lari` Kunci > persentil ke-95 peraturan rawak · **`T4`** (setup berprasyarat sahaja)
kelebihan `lari` Kunci (gabungan) DAN K3 melebihi versi yang sama TANPA prasyarat (pencetus dan penapis saham sama).

**4. Keluarga F.** Setup kedua-dua papan didaftarkan (`F39` dan seterusnya). `data/registry_F.csv` mendapat lajur
`prasyarat` dan `syarat` (diisi juga bagi `F01`–`F38`); takrif setup berprasyarat = `pencetus|penapis|henti|keluar|prasyarat`.
Status kekal `BACKTEST`. **Kohort jejak hadapan TIDAK berubah** dalam pindaan ini; penukaran kohort ialah keputusan
pengguna yang berasingan.

**5. Banding wajib dalam laporan.**

- (a) **Setiap pencetus (500), syarat sahaja lawan dengan prasyarat.** Pada kumpulan A, bagi setiap skor dan setiap
  kelas — `S` tiada prasyarat · `P` sekurang-kurangnya satu prasyarat · `PL` sekurang-kurangnya satu prasyarat plasebo
  (5c) — 5 peraturan teratas dinilai tepat dan yang terbaik dipilih. Ketiga-tiganya kemudian dinilai pada kumpulan B:
  kadar `lari` (mutlak), asas, kelebihan, kadar kena henti. Laporan: `hasil/CS05/SEMUA_PENCETUS.md|csv`.
- (b) **Padanan jenis setup × prasyarat.** Kelas pencetus dikunci secara mekanikal sebelum hasil dilihat: **IKUT TREND**
  jika ≥ 50 % isyaratnya (kumpulan A, bar sah) mempunyai RSI14 > 50 pada bar isyarat; selainnya **PANTULAN**. Bagi
  setiap prasyarat tunggal (48), tanpa penapis: beza kelebihan `lari` dan beza kadar kena henti antara isyarat pencetus
  bila prasyarat benar dan semua isyarat pencetus itu, pada kumpulan B; median setiap kelas, dengan plasebo di sebelah.
- (c) **Plasebo.** Keseluruhan carian diulang dengan prasyarat yang sama **dianjak masa**: siri prasyarat pasaran dianjak
  437 sesi secara membulat atas senarai hari panel; siri prasyarat kumpulan/syarikat dianjak 437 bar secara membulat dalam
  setiap saham. Anjakan mengekalkan peratus masa benar dan kelompok hari, dan memutuskan kaitan dengan keadaan sebenar.
- (d) Kadar kena henti (`gagal`) dipaparkan di sebelah kadar `lari` di mana-mana kadar lari dipaparkan.
- (e) Rujukan "prasyarat sahaja": kadar `lari` semua bar layak bila setiap prasyarat benar/palsu (kumpulan B).

**6. Bacaan dikunci.** "Prasyarat menolong" hanya jika, pada kumpulan B, median merentas pencetus bagi (kelebihan `P` −
kelebihan `S`) positif DAN melebihi median (kelebihan `PL` − kelebihan `S`); dilaporkan bagi kumpulan B gabungan dan K3
sahaja (**K3 ialah ujian sebenar**), bagi setiap skor. Jika prasyarat tidak mengatasi plasebo, itu dilaporkan
sebagaimana adanya. Papan ialah pangkat backtest, BUKAN bukti; kad skor kekal satu-satunya keputusan wang sebenar.

**7. Kaveat dikunci.** `QF01`/`QF04` memakai tarikh earnings sebenar (pandang ke hadapan ringan; papertrade memerlukan
kalendar earnings); peta sektor/industri ialah peta semasa; tiada saham delist; set 2000 bukan tapisan Shariah; prasyarat
pasaran berubah ikut HARI (pemerhatian bebas sedikit); `QH07` ialah proksi; lebih 100 juta peraturan dicuba, jadi yang
teratas pada kumpulan A sebahagiannya nasib (sebab itu angka dilaporkan pada kumpulan B, bersebelahan rawak dan plasebo).
Keluaran: `carian_setup/hasil/CS05/`; `kajian/CARIAN_SETUP.md` memaparkan pusingan terkini.

**Tambahan (i), 14 Nov 2026 — ditulis sebelum larian penuh.** Apa yang dilihat: ujian kod hujung-ke-hujung pada 49
pencetus indikator sahaja (tanpa benih M/N), ditulis ke folder ujian di luar repo. Ujian itu mendedahkan kecacatan
prosedur butir 3: 2,000 teratas sejagat hampir semuanya berkongsi satu prasyarat, jadi had kepelbagaian (setiap prasyarat
paling banyak 3 kali) tidak dapat mengisi 10 baris papan. Pembetulan, dikunci sebelum larian penuh: **kolam calon papan**
= 2,000 teratas sejagat DAN, bagi setiap satu daripada 544 pasangan prasyarat, 20 peraturan teratas ikut skor merentas
pencetus (terbaik setiap pencetus); semuanya dinilai tepat dan papan dipilih daripada gabungan itu dengan peraturan butir 3
yang sama. "200 teratas" kekal 200 teratas daripada 2,000 sejagat. Tiada perubahan lain. Dicatat tanpa perubahan: `QH03`
benar kira-kira dua pertiga masa kerana takrif di sini tiada peraturan luput IBD (kenaikan 5 %); ia kekal seperti
dipradaftar.

### Pindaan 14 Nov 2026 (j) — CS05 peringkat LENGKAP: pegang + keluar + henti ikut kadar tangkap (sebelum dijalankan)

Pengguna 14 Nov 2026 (selepas hasil (i)): "jangan mula jejak hadapan lagi; sudah selesai ke, prasyarat dan syarat? Check
betul-betul matlamat backtest ini; tak boleh tersasar". Semakan lawan §1 menemui tiga kecacatan pada bahagian
pegang/keluar pindaan (d) dan (i); bahagian masuk (prasyarat → syarat) tidak terjejas:

1. (henti × keluar) dipilih ikut had bawah PURATA `R`, sedangkan kayu ukur pengguna ialah kadar tangkap.
2. Label `lari` memakai henti −8 % tetap, sedangkan henti setup itu sendiri boleh `H2`–`H4`.
3. Pegang/keluar hanya dikira bagi setup papan, bukan bagi setiap kaedah.

**Apa yang sudah dilihat:** semua hasil (i), termasuk purata `R`, tempoh pegang dan peratus dagangan ≥ +10 % bagi 19
setup papan dengan (henti × keluar) yang dipilih ikut purata (cth. `F48`: pegang 5.4 sesi, 12 % dagangan ≥ +10 %).
Tiada hasil peringkat ini dilihat sebelum pindaan ditulis. Peraturan masuk, papan dan pangkat (i) TIDAK berubah.

**Ukuran setup lengkap** (setiap dagangan, dengan henti dan peraturan keluar setup itu sendiri; mekanik §4; kos ditolak):

| Ukuran | Takrif |
|---|---|
| **`jadi`** | dagangan DIJUAL dengan `R` ≥ +10 % ("menangkap dan memegang": kadar tangkap yang direalisasi) |
| `rugi8` | dagangan dijual dengan `R` ≤ −8 % |
| `pelari dipegang` | antara belian yang sahamnya `lari` (label (d)), bahagian yang `jadi` |
| pegang | purata sesi dipegang |

- **Pemilihan (kumpulan A):** bagi setiap peraturan masuk, (henti × keluar) daripada 4 × 577 dengan
  min merentas E1, E2 bagi [kadar `jadi` − 2 ralat piawai] tertinggi (`n` ≥ 100 setiap era; isyarat bertindih dibenarkan
  pada langkah ini, seperti §6.1). Kemudian dinilai dengan satu posisi setiap saham.
- **Diliputi:** 19 setup papan (i), dan bagi SETIAP pencetus peraturan masuk terbaik kelas `S` (syarat sahaja) dan `P`
  (dengan prasyarat) bagi kedua-dua kayu ukur (butir 5a pindaan (i)). Semuanya dilaporkan pada kumpulan B.
- **Asas rawak:** kadar `jadi` dan `rugi8` semua bar layak pada hari sama × tercile ATR % sama (papan pilih) atau era
  sama × tercile (papan jumlah), dengan henti dan keluar YANG SAMA.
- **Banding wajib:** (a) `jadi` dengan keluar terpilih lawan **tanpa keluar indikator** (`X00`, henti sama): adakah
  indikator keluar menambah; (b) lawan (henti × keluar) lama yang dipilih ikut purata; (c) `rugi8` dan purata `R` di
  sebelah `jadi` (maklumat, bukan kayu ukur).
- Lajur ✓/✗ setup papan: `L1` kelebihan `jadi` atas rawak positif dalam K1, K2 dan K3 · `L2` `jadi` (kumpulan B) dengan
  keluar terpilih ≥ `X00`.
- **Keluarga F:** `F39`–`F57` didaftarkan beberapa jam sebelum ini pada branch kerja yang sama, belum digabung ke `main`
  dan tidak dipakai mana-mana penjejak. ID-nya kekal pada peraturan MASUK yang sama; `henti`, `keluar`, `takrif` dan
  ukurannya diganti dengan pilihan pindaan ini (pusingan kekal `CS05`). Ini satu-satunya kali takrif F diganti; selepas
  digabung ke `main`, ID kekal seperti pindaan (a).
- Tambahan laporan (tiada pemilihan baharu): senarai 50 peraturan masuk teratas setiap kayu ukur TANPA had kepelbagaian
  papan (`hasil/CS05/TOP50.md`), kerana had itu memaksa setup yang lebih lemah naik ke papan.
- **Jejak hadapan:** tiada setup CS05 masuk jejak hadapan (keputusan pengguna 14 Nov 2026). Kohort 13 Nov tidak berubah.
- Kod `carian_setup/cs_lengkap.py`; keluaran `hasil/CS05/` (`LENGKAP` dalam `LAPORAN.md`, `SEMUA_PENCETUS_LENGKAP.md`).

### Pindaan 14 Nov 2026 (k) — pusingan CS06: pangkat masuk ikut TANGKAP PENUH, dan tala bersama prasyarat (sebelum dijalankan)

Keputusan pengguna 14 Nov 2026 ("ya untuk tiga-tiga"): sambung backtest dengan (A) memangkatkan peraturan masuk terus
ikut tangkap penuh setup lengkap, bukan label `lari`; (B) menala parameter BERSAMA prasyarat. Tiada setup CS05/CS06
masuk jejak hadapan. Kod: `carian_setup/cs_cs05.py` (pusingan `CS06`), `cs_lengkap.py`, `cs_tala6.py`.

**Apa yang sudah dilihat:** semua hasil (i) dan (j) pada kumpulan A dan B; reka bentuk ini dipilih selepasnya, jadi
kumpulan B bukan lagi "tidak dilihat" bagi keluarga setup ini (K3 kekal ujian paling ketat, dengan kaveat itu). Kadar
asas semua bar layak kumpulan A (bukan hasil carian): `lari` 5.22 %, tangkap penuh piawai 5.12 %; 95 % bar `lari` juga
tangkap penuh dan 97 % sebaliknya. Maka pangkat (A) DIJANGKA hampir sama dengan CS05; ini diukur, bukan diandaikan.

**A. Pangkat masuk ikut tangkap penuh.**

- Label sasaran **`tp`** = tutup sesi 5 ≥ `P` + 5 % DAN dagangan dengan **pegang piawai** dijual dengan `R` ≥ +10 %.
  Pegang piawai = henti `H4` (4×ATR14), tiada keluar indikator (`X00`), jual pada tutup sesi 20: cara pegang yang paling
  kerap terpilih dalam (j). `tp` menggantikan `lari` (yang memakai henti −8 % tetap) sebagai sasaran pangkat; label lain
  kekal untuk laporan.
- Ruang carian (103,088,000 peraturan masuk), dua kayu ukur (pilih = lawan rawak hari sama × tercile ATR %; jumlah =
  lawan rawak era sama × tercile; asasnya kadar `tp`), `n` ≥ 100 setiap era, peringkat tepat, kolam calon papan, papan 10
  teratas dengan had kepelbagaian, Kunci, larian plasebo, banding setiap pencetus (`S`/`P`/`PL`) dan padanan: semuanya
  seperti (i) + tambahan (i), dengan `tp` di tempat `lari`.
- Setup lengkap papan: (henti × keluar) dipilih seperti (j), tetapi ikut kadar tangkap penuh DENGAN henti dan keluar
  setup itu sendiri (tutup sesi 5 ≥ `P` + 5 % DAN `R` ≥ +10 %); asas rawak dengan henti dan keluar yang sama.
- Banding wajib dengan CS05: Spearman antara skor CS05 (`lari`) dan skor CS06 (`tp`) bagi peraturan yang dinilai tepat
  dalam kedua-duanya, dan bilangan setup papan yang peraturan masuknya sama.
- Keluarga F: peraturan masuk papan CS06 yang sudah berdaftar (`F39`–`F57`) mengekalkan ID dan barisnya; hanya peraturan
  masuk baharu mendapat ID baharu (pusingan `CS06`).

**B. Tala bersama prasyarat.** Induk = setup papan CS06 (kedua-dua papan). Tiga paksi ditala serentak:

- Pencetus: induk berasaskan kaedah M → 24 varian baharu, setiap parameter `tala = Y` seragam dalam ±25 % nilai induk
  (dipotong pada [`bawah`, `atas`] `param_julat.csv`; benih 20261113), seperti (e). Induk N dan indikator P kekal.
- Penapis saham berambang (grid (e)): RS ≥ {50, 60, 70, 80, 90, 95}; ATR % ≥ {2, 3, 4, 5, 6, 8}; ≥ {20, 30, 40, 50, 60} %
  di bawah puncak 52 minggu. Penapis lain kekal.
- Prasyarat berambang (jadual di bawah). Prasyarat tanpa ambang (`QA01`–`QA04`, `QB03`, `QG01`, `QG02`, `QG04`, `QH07`,
  `QH08`, `QH09`, `QF05`) kekal.

| Prasyarat | Grid ambang (nilai induk dalam kurungan) |
|---|---|
| `QA05` QQQ dalam x % dari puncak | 1, 2, (3), 5, 7 |
| `QA06` / `QA07` QQQ ≥ x % di bawah puncak | 5, 7.5, (10), 15, (20), 25 |
| `QA08` / `QA09` rejim baharu ≤ n sesi | 5, (10), 15, 20, 30 |
| `QA10` QQQ RSI14 < x | 30, (35), 40, 45 |
| `QA11` QQQ naik ≥ x % dalam 5 sesi | 2, (3), 4, 5 |
| `QB01` turun-naik SPY 21 hari ≥ x % | 20, (25), 30, 35, 40 |
| `QB02` turun-naik SPY 21 hari ≤ x % | 8, (10), 12, 15 |
| `QC01` ≥ x % saham di atas MA50 | 50, (60), 70, 80 |
| `QC02` ≤ x % saham di atas MA50 | 15, 20, (30), 40 |
| `QC03` keluasan naik ≥ x mata dalam 10 sesi | 5, (10), 15, 20 |
| `QC04` ≥ x % saham di atas MA200 | 50, (60), 70 |
| `QC05` ≥ x % saham dalam 5 % dari puncak | 10, (15), 20, 30 |
| `QG03` x hari pertama bulan | 5, (7), 10 |
| `QH01`, `QH04`, `QH10` tempoh aktif n sesi | 10, (20), 30 |
| `QH02` distribution day ≤ n | 1, (2), 3 |
| `QH03` distribution day ≥ n | 4, (5), 6, 7 |
| `QH05` nisbah 4 % > x | 1.5, (2), 3 |
| `QH06` nisbah 4 % < x | 0.33, (0.5), 0.67 |
| `QD01` / `QD02` sektor n teratas / terbawah | 2, (3), 4 |
| `QD03`, `QE04` ≥ x % saham sektor / industri di atas MA50 | 50, (60), 70 |
| `QE01`, `QE02`, `QE03` industri x % teratas / terbawah | 10, (20), 30 |
| `QE05` saham lain industri sama naik ≥ x % dalam 20 sesi | 15, (20), 30 |
| `QF01` earnings dalam 1–k sesi akan datang | 2, 3, (5), 7, 10 |
| `QF02` 0–k sesi selepas earnings | 2, (4), 7 |
| `QF03` 5–k sesi selepas earnings | 14, (19), 29 |
| `QF04` tiada earnings dalam k sesi akan datang | 10, (20), 30 |
| `QF06` hasil suku terkini tumbuh ≥ x % | 10, (20), 30, 50 |
| `QF07` harga melompat ≥ x % pada hari earnings | 3, (5), 8 |

- Skor sel = skor tepat CS06 mengikut kayu ukur papan induk (satu posisi setiap saham; `n` ≥ 100 dalam E1 dan E2).
- **Dataran, bukan puncak:** markah sel = median skor sel itu dan jirannya ±1 langkah pada setiap ambang yang ditala
  (kotak 3^k); perlu sekurang-kurangnya separuh sel kotak (paling kurang 2) cukup isyarat. Varian pencetus tidak
  berjiran. Anak = sel bermarkah dataran tertinggi; jika sel induk sendiri tertinggi, induk kekal.
- **Ujian:** anak dan induk dinilai pada kumpulan B. **Bacaan dikunci:** "tala menolong" hanya jika lebih separuh anak
  (tidak termasuk induk kekal) mengatasi induknya dalam kelebihan `tp` pada kumpulan B gabungan DAN pada K3. Jika tidak,
  itu dilaporkan sebagaimana adanya.
- Cara pegang anak dipilih seperti A; anak didaftarkan dalam keluarga F (ID baharu, catatan induk dalam laporan).

Keluaran `carian_setup/hasil/CS06/`; `kajian/CARIAN_SETUP.md` memaparkan pusingan terkini. Kaveat (i) dan (j) kekal.

### Pindaan 14 Nov 2026 (l) — simulasi portfolio 10 slot bagi setup berprasyarat (sebelum dijalankan)

Langkah backtest seterusnya yang dicadangkan kepada pengguna pada akhir CS06 (pengguna 14 Nov 2026: "boleh continue?").
Soalan: hari isyarat setup berprasyarat berkelompok; **adakah satu akaun 10 slot sempat mengambil belian itu, dan adakah
kadar tangkapnya kekal pada belian yang benar-benar diambil?** Tiada jejak hadapan. Kod `carian_setup/cs_portfolio6.py`.

**Apa yang sudah dilihat:** semua hasil (i), (j), (k), termasuk taburan belian mengikut tahun dan kadar menang. Empat setup
di bawah dinamakan kepada pengguna SEBELUM simulasi ini ditulis atau dijalankan; tiada hasil portfolio dilihat.

- **Setup** (takrif `data/registry_F.csv`, dengan henti dan keluar masing-masing): `F39`, `F40`, `F58` (papan pilih; berdagang
  setiap tahun) dan `F49` (papan jumlah). Gabungan: `PILIH3` = `F39` + `F40` + `F58`; `SEMUA4` = keempat-empatnya.
- **Data:** kumpulan B, isyarat 2010-01-04 … 2026-08-28; mekanik §4 (kos 0.5 % pusingan).
- **Portfolio** (seperti pindaan (c)): 10 slot × 10 % ekuiti; isyarat dibeli pada buka esok jika ada slot kosong dan saham
  itu tidak sedang dipegang; slot kosong semula sehari selepas hari jual; lebih isyarat daripada slot → dipilih rawak;
  pulangan harian = jumlah pulangan harian posisi ÷ 10; tunai 0 %. Pilihan rawak diulang **200 kali** (benih 20261113 + i);
  dilaporkan median.
- **Ukuran:** (1) bahagian isyarat yang sempat diambil, dagangan setahun, bahagian bulan tanpa belian; (2) pada dagangan
  yang DIAMBIL: tangkap penuh (tutup sesi 5 ≥ `P` + 5 % DAN `R` ≥ +10 %), `jadi`, menang, `rugi8`, purata `R`; (3) akaun:
  CAGR, MDD, pendedahan purata, **CAGR pada MDD −10 %** (pendedahan × min(1, 10 % ÷ |MDD|)), bilangan tahun kalendar
  positif dan tahun terburuk; (4) K3 sahaja.
- **Jalur rawak (kawalan):** setiap isyarat diganti dengan saham rawak yang layak pada hari yang sama dan tercile ATR %
  yang sama, dengan henti dan keluar yang sama; portfolio yang sama; 200 cabutan. Dilaporkan median dan persentil ke-5/95
  jalur, dan persentil kedudukan setup dalam jalur.
- **Bacaan dikunci:** setup "menambah di peringkat akaun" hanya jika CAGR pada MDD −10 % positif DAN melebihi persentil
  ke-95 jalur rawaknya. SPY beli-dan-pegang pada skala yang sama dipaparkan sebagai MAKLUMAT sahaja (kayu ukur pengguna
  ialah kadar tangkap, bukan indeks; SPUS tiada sejarah sebelum Dis 2019).
- Kaveat dikunci: tiada saham delist; set 2000 bukan tapisan Shariah; `QF01` memakai tarikh earnings sebenar; kumpulan B
  sudah dilihat dalam (i)–(k); satu akaun 10 slot ialah satu cara membina portfolio, bukan satu-satunya.
- Keluaran: `carian_setup/hasil/CS06/PORTFOLIO.md` dan `portfolio.csv`.

### Pindaan 14 Nov 2026 (m) — semakan lawan matlamat kali kedua: ukuran yang belum dibuat, dan satu kedudukan akhir (sebelum dijalankan)

Pengguna 14 Nov 2026 (selepas Claude melaporkan "backtest sudah lengkap"): "anda pasti ke sudah lengkap semua proses kita?
cuba baca balik matlamat saya; rasanya masih ada yang belum complete". Bacaan semula §1 baris demi baris mendapati
bahagian masuk, henti, kadar menang dan portfolio sudah diukur, tetapi ENAM perkara belum:

1. **Peringkat ketiga corak** ("kemudian naik lagi 2–4 minggu") hanya diukur sebagai "masih ≥ 10 % pada minggu ke-4",
   bukan "naik lagi selepas minggu pertama"; dan "lebih baik 10 % minggu pertama" tidak dipaparkan.
2. **Kekerapan dan liputan.** Semua pangkat setakat ini ialah KETEPATAN (daripada belian, berapa yang jadi). "Paling kerap
   menangkap" juga bermaksud berapa banyak pelari ditangkap: belian dan tangkapan setahun, dan bahagian semua pelari
   pasaran yang ditangkap. Belum dilaporkan.
3. **Sumbangan setiap komponen** setup (prasyarat pasaran, prasyarat syarikat, setiap penapis, pencetus) belum diuji satu
   demi satu; hanya "buang semua prasyarat" dan "buang pencetus".
4. **Mutu pegang** ("selagi naik; 10 % bukan paras jual"): keluar dipilih ikut ukuran ya/tidak (≥ +10 %), yang tidak
   membezakan menjual pada +10 % daripada memegang hingga +40 %.
5. **Saham Shariah.** Semua angka CS daripada set 2000 yang bukan tapisan Shariah; belum disemak pada saham yang pengguna
   boleh beli.
6. **Satu kedudukan akhir.** Peratus bertaburan dalam beberapa laporan dan dua papan; tiada satu jadual semua setup.

**Apa yang sudah dilihat:** semua hasil (i)–(l). Pindaan ini MENGUKUR dan MENYUSUN sahaja: tiada carian, penalaan atau
setup baharu. Kod `carian_setup/cs_akhir.py`; keluaran `carian_setup/hasil/KEDUDUKAN_AKHIR.md|csv`.

- **Setup:** setiap setup F yang takrifnya boleh dinilai seragam pada kumpulan B: `F01`–`F30` dan `F39`–`F69` (61). Tidak
  termasuk anak tala `F31`–`F38` dan `F70`–`F87` (memerlukan varian tala; tala terbukti tidak menolong). `F01`–`F10` dicari
  pada set 431 yang bertindih dengan kumpulan B (dicatat). Data: kumpulan B, 2010-01-04 … 2026-08-28; mekanik §4; setiap
  setup dengan henti dan keluarnya sendiri; satu posisi setiap saham.
- **Corong ikut ayat matlamat** (laluan harga selepas beli pada `P`; henti −8 % seperti label (d)): `m5` tutup sesi 5 ≥
  `P` + 5 % · `m10` tutup sesi 5 ≥ `P` + 10 % · **`terus`** = `m5` DAN tutup sesi 20 > tutup sesi 5 DAN henti −8 % tidak
  kena dalam 20 sesi ("naik ≥ 5 % minggu pertama, kemudian naik lagi hingga minggu ke-4") · `tp` tangkap penuh dengan henti
  dan keluar setup sendiri (pindaan (k)). Asas rawak: hari sama × tercile ATR % sama.
- **Kekerapan:** belian setahun, tangkapan `terus` setahun, tahun dengan belian, bahagian bulan dengan belian.
  **Liputan:** episod pelari = blok bar berturutan berlabel `terus` bagi satu saham (blok yang dipisahkan kurang 5 bar
  digabung); liputan = episod yang dibeli setup ÷ semua episod kumpulan B. Juga bagi gabungan semua setup yang dipercayai.
- **Komponen:** kelebihan `terus` (lawan rawak hari sama) setup penuh lawan setup tanpa SATU komponen (prasyarat pasaran;
  prasyarat syarikat; penapis 1; penapis 2; pencetus). Komponen "menyumbang" jika membuangnya menurunkan kelebihan.
- **Mutu pegang:** antara belian berlabel `terus`: purata `R` direalisasi (keluar sendiri), purata `R` jika dipegang 20
  sesi dengan henti yang sama (`X00`), dan purata puncak tutup dalam 20 sesi.
- **Shariah:** ukuran yang sama pada saham kumpulan B yang ada dalam `data/harga/univ.txt` (senarai Shariah semasa; bukan
  titik-masa).
- **Kedudukan akhir (dikunci):** "dipercayai" = belian ≥ 300 DAN tahun dengan belian ≥ 10 DAN kelebihan `terus` positif
  dalam K1, K2 dan K3. Susunan: setup dipercayai dahulu, kemudian kadar `terus` menurun. Lajur: corong, rawak, tangkap
  penuh, menang, rugi ≥ 8 %, kekerapan, liputan, komponen, Shariah.
- Kaveat (i)–(l) kekal. Yang TIDAK ditutup oleh pindaan ini: data saham delist; carian automatik berkala ("mesin sentiasa
  mencari"); peringkat papertrade (ditangguh atas arahan pengguna).

### Pindaan 14 Nov 2026 (n) — pusingan CS07: tala parameter SEMUA kaedah, cari + tala KELUAR, dan mesin berkala (sebelum dijalankan)

Sebab: semakan 12 item matlamat (`SERAHAN_CARIAN_SETUP.md` §1a) menunjukkan item 2 (parameter), item 4 (indikator keluar yang
mengesan kenaikan tamat) dan item 7 (mesin sentiasa mencari dan menala) belum capai. Keputusan pengguna 14 Nov 2026: "ya, mula
sekarang", ikut susunan (a) tala parameter semua kaedah M, N dan indikator; (b) cari dan tala indikator keluar; (c) mesin
berkala. Tiada jejak hadapan, tiada order.

**Kayu ukur (tidak berubah keluarga):** kadar tangkap. Label masuk = `terus` (pindaan (m): tutup sesi 5 ≥ P + 5 % DAN tutup
sesi 20 > tutup sesi 5 DAN henti −8 % tidak kena dalam 20 sesi), lawan saham rawak hari sama × tercile ATR % ("pilih").
`lari` dan `tp` turut dilaporkan. Skor peraturan masuk = min dua era carian (E1, E2) bagi [kelebihan − 2 ralat piawai],
n ≥ 100 setiap era (sama seperti (i)). Carian pada kumpulan A sahaja; kumpulan B (K1, K2, K3) hanya untuk laporan.

**(a) Tala parameter masuk** (`carian_setup/cs_tala7.py`, `cs_param.py`):
- Kaedah M (134): varian lalai (v0) dan dua varian sedia ada (v1, v2), ditambah 8 varian rawak julat penuh `param_julat.csv`
  (v3–v10, `cari.param_varian`); kemudian bagi 50 kaedah M dengan skor A terbaik, 8 varian setempat ±25 % di sekitar varian
  terbaiknya (benih `[20261113, 7, id, v]`).
- Indikator dan kaedah N: 25 keluarga berparameter `K01`–`K25` dengan grid penuh (≈ 630 varian): RSI(n) < x; RSI silang naik;
  bawah/masuk semula/atas jalur Bollinger(n, k); k tutup turun berturut; tutup silang MA/EMA(n); MA(f) silang MA(s);
  MACD(f, s, g); pecah tinggi n hari (± volum); Supertrend(n, m); ADX(n) silang x; Stochastic(n); lonjakan (r, volum);
  gap; gap-and-go; undur ke MA(n) yang naik; jatuh y % dalam x hari; Keltner; squeeze lepas; NR-k; Holy Grail; RS silang x;
  bar pembalikan; pecah julat sempit. Ahli yang parameternya sama dengan takrif `P`/`N` asal ditanda `asal` (= induk).
  Corak kompleks berbilang syarat (cth. VCP, Qullamaggie, Ichimoku, pocket pivot, Stage 1→2) TIDAK ditala dalam pusingan ini;
  ia kekal pada takrif asal dan disenaraikan dalam laporan sebagai baki bagi mesin.
- Setiap varian diskor dengan enjin (i): terbaik atas [0–1 prasyarat pasaran] × [0–1 prasyarat syarikat] × [0–2 penapis saham].
- Pilihan: bagi setiap induk (kaedah M / keluarga K), anak = varian dengan skor A tertinggi. Induk = v0 (M) atau ahli `asal`.
- Bacaan dikunci: "tala menolong" jika pada kumpulan B kelebihan `terus` anak > induk bagi lebih separuh pasangan DAN median
  beza > 0 dalam K3. Turut dilaporkan: 20 setup teratas ikut skor A dengan dan tanpa varian baharu, dinilai pada B.

**(b) Keluar** (`carian_setup/cs_keluar7.py`; kernel sendiri, enjin lama tidak disentuh supaya pariti jejak F kekal):
- Atom keluar berparameter (≈ 97): tutup < SMA/EMA(n); dua tutup < SMA(n); SMA(f) < SMA(s); MACD(f, s, g) < isyarat;
  histogram MACD turun k hari; RSI(n) < x; RSI(n) silang turun x; RSI(n) > x; Supertrend(n, m) turun; tutup < rendah k hari;
  Stochastic silang turun; hari turun bervolum; bar pembalikan; k tutup turun; +DI < −DI; Chandelier k × ATR14
  (k 1.5–5); ekor p × tutup tertinggi (p 0.85–0.97); "tiada kemajuan" (selepas d sesi, tutup < harga beli).
- Peraturan: `X00`, tunggal, pasangan ATAU/DAN; setiap satu dengan **syarat aktif** {sentiasa, selepas tutup tertinggi ≥ +5 %,
  selepas ≥ +10 %} ("pegang selagi naik; indikator keluar hanya bekerja selepas saham sudah naik"). Henti: −8 %, −10 %, −12 %,
  −15 %, 3×, 4×, 5× ATR14 dan min(−10 %, 4×ATR14). Had 20 sesi kekal.
- Ukuran dikunci: `tp` = naik ≥ 5 % minggu pertama DAN dijual dengan untung ≥ +10 % (pindaan (k)), dengan SYARAT "tidak jual
  awal": purata untung terealisasi pada belian berlabel `terus` ≥ 90 % daripada "pegang sahaja" (henti yang sama, `X00`).
  Turut dilaporkan: kekurangan dari puncak (puncak tutup 20 sesi − untung terealisasi), menang, rugi ≥ 8 %, purata.
- Pilihan dua peringkat pada kumpulan A (elak padanan lampau atas ratusan ribu calon): (1) **keluar sejagat**: purata merentas
  setup bagi [min dua era (tp − tp `X00` henti sama)], 30 teratas yang lulus syarat; (2) setiap setup memilih antara `X00`
  (semua henti) dan 30 keluar sejagat itu. Setup = 61 setup kedudukan akhir (m) + setup papan baharu (a).
- Bacaan dikunci: "keluar menolong" jika pada kumpulan B, tp keluar terpilih > tp `X00` (henti sama) DAN > tp keluar lama
  bagi lebih separuh setup, syarat "tidak jual awal" kekal pada B, dan median rugi ≥ 8 % tidak naik lebih 1 mata.

**(c) Mesin berkala** (`carian_setup/cs_mesin.py`, workflow `mesin_carian.yml`): setiap larian menarik kelompok varian BAHARU
(benih = nombor larian: varian rawak kaedah M, parameter rawak keluarga K, termasuk di luar grid), menskor pada A dengan
peraturan (a), menilai yang terbaik pada B, dan MENAMBAH ke papan terkumpul (`hasil/MESIN/papan.csv`, tambah-sahaja) serta
laporan `hasil/MESIN/LAPORAN.md`. Peraturan mesin dikunci di sini; larian mesin tidak memerlukan pindaan baharu selagi ruang,
skor dan bacaan tidak berubah. Papan disusun ikut skor A; lajur B ialah semakan, bukan kunci susunan. Mesin TIDAK mendaftar
setup ke papertrade dan tidak menyentuh Lejar, kad skor atau kohort jejak F.

**Pendaftaran:** setup lengkap terbaik CS07 (masuk (a) + henti/keluar (b)) didaftarkan `F88` dan seterusnya (pusingan `CS07`,
status `BACKTEST`). Kedudukan akhir dijana semula dengan takrif "dipercayai" (m) yang sama.

**Penjelasan (n)-1 (14 Nov 2026, ditulis sebelum mana-mana hasil B bagi CS07 dilihat):** grid keluarga K menghasilkan 656
varian. Statistik keluar pada peringkat cari dan BACAAN "keluar menolong" dikira atas SEMUA isyarat masuk setup itu (set
isyarat yang sama bagi keluar terpilih, `X00` dan keluar lama: perbandingan berpasangan); angka "satu posisi setiap saham"
dilaporkan bersama sebagai angka praktikal. Syarat "tidak jual awal" pada peringkat sejagat dikira atas jumlah merentas setup.

**Penjelasan (n)-2 (14 Nov 2026, sebelum hasil B larian penuh dilihat; diputuskan Claude di bawah serahan pengguna: "anda sendiri
tahu kan matlamat kita?"):** kod F baharu didaftarkan HANYA bagi setup papan CS07 yang lulus takrif "dipercayai" pindaan (m)
(belian ≥ 300, ≥ 10 tahun aktif, kelebihan `terus` > 0 dalam K1, K2 dan K3, dengan henti dan keluar terpilihnya). Setup papan
yang tidak lulus direkod dalam laporan CS07 sahaja, tanpa kod F. Setup F lama (`F01`–`F87`) tidak diubah dan tidak dibuang.
Sebab: pengguna bimbang senarai F bertambah dengan kod yang tidak berguna.

**Kaveat dikunci:** kumpulan B sudah dilihat dalam CS02–CS06 dan (m) (bukan lagi tahanan bersih, hanya tidak dipakai untuk
memilih); lebih banyak varian dicuba = skor A terbaik lebih melambung, jadi angka B dan K3 yang dibaca; tiada saham delist;
tiga pusingan tala terdahulu (CS04, (j), CS06) tidak menunjukkan faedah luar sampel — pusingan ini mengukur semula dengan
ruang yang jauh lebih luas, bukan menjanjikan hasil.

### Pindaan 14 Nov 2026 (o) — analisis PEGANG MINIMUM (diminta pengguna; sebelum dijalankan)

Pengguna 14 Nov 2026: "saya tak mahu saham itu dibeli hari tu dan dijual hari tu juga ... at least hold 3 hari ... analisa
dahulu". Ini analisis, bukan carian: tiada setup dipilih daripadanya. Kod `carian_setup/cs_pegang.py`, keluaran
`hasil/PEGANG_MIN.md|csv`.

- (1) Papertrade langsung (Lejar `lejar/tutup/*.csv`, Papertrade C): berapa dagangan dijual pada hari beli, esoknya dan hari
  ke-3, ikut sebab dan kaedah.
- (2) 61 setup kedudukan akhir (m), kumpulan B, henti dan keluar sendiri, satu posisi setiap saham: taburan sesi jual dan
  sebabnya (henti / indikator / had masa). Mekanik sedia ada: beli pada buka sesi 1; tiada jualan pada sesi 1.
- (3) Tiga mekanik dibandingkan pada setup yang sama: **V0** sedia ada; **V1** indikator keluar hanya boleh menjual mulai
  buka sesi ke-4 (pegang penuh 3 sesi), henti rugi kekal aktif sejak sesi 2; **V2** indikator DAN henti rugi hanya aktif
  mulai sesi ke-4 (pelanggaran henti sebelum itu diabaikan). Ukuran: tangkap penuh, menang, rugi ≥ 8 %, rugi ≥ 15 %,
  purata, sesi pegang.
- Tiada bacaan lulus/gagal: pegang minimum ialah SYARAT pengguna, bukan pengoptimuman. Analisis ini mengukur kosnya dan
  memilih cara melaksanakannya (V1 atau V2); keputusan dicatat sebagai pindaan sebelum enjin diubah.

### Pindaan 14 Nov 2026 (p) — SYARAT WAJIB baharu: pegang minimum 3 sesi (selepas analisis (o); sebelum hasil keluar CS07 dilihat)

Syarat pengguna 14 Nov 2026: tiada beli dan jual pada hari yang sama; pegang sekurang-kurangnya 3 hari. Analisis (o)
(`hasil/PEGANG_MIN.md`): setup F tidak pernah menjual pada hari beli; jualan sebelum hari ke-4 hanya ~2.5 % belian (median
setup dipercayai), hampir semuanya henti rugi; tiga mekanik memberi angka yang hampir sama.

- **Peraturan (V1), berkuat kuasa bagi semua setup F mulai sekarang:** indikator keluar hanya boleh menjual mulai BUKA SESI
  KE-4 (beli Isnin → jualan indikator paling awal Khamis). Henti rugi kekal aktif sejak sesi ke-2 sebagai perlindungan
  kecemasan (henti rugi wajib, item 5); tiada apa-apa jualan pada hari beli. Diputuskan Claude di bawah serahan pengguna;
  pilihan V2 (henti juga ditangguh) direkod dalam analisis dan boleh dipilih pengguna.
- Pelaksanaan: `cs_keluar7.PEGANG_MIN = 3` (carian dan penilaian keluar CS07 dijalankan SEMULA di bawah peraturan ini; hasil
  A tanpa peraturan dibuang sebelum hasil B dilihat); kedudukan akhir dijana semula bagi SEMUA setup di bawah peraturan ini;
  penjejak hadapan kohort F (`cs_hadapan.py`) memakai peraturan yang sama (belum ada posisi ditutup; kohort tidak berubah).
- Mesin (c) tidak terkesan: ia menskor masuk sahaja.

### Pindaan 14 Nov 2026 (q) — pusingan CS08: LORONG KEDUA "beli selepas pengesahan uptrend, pegang sampai trend tamat" (sebelum dijalankan)

Permintaan pengguna 14 Nov 2026 (kes MXL): "beli di tengah atau lewat sedikit dari start uptrend ... tunggu confirmation untuk
big uptrend, then baru beli, then continue hold sampai habis trend". Ini lorong BERASINGAN daripada swing ≤ 20 sesi: syarat
wajib "swing ≤ 20 sesi" TIDAK terpakai di sini; semua syarat lain kekal (henti rugi wajib, tiada jual hari beli, pegang
minimum 3 sesi (p), tiada sasaran untung tetap, keluar ikut indikator, backtest dahulu). Kod `carian_setup/cs_trend8.py`;
keluaran `hasil/CS08/`. Tiada jejak hadapan, tiada order.

- **Had pegang:** 126 sesi (≈ 6 bulan). Isyarat hanya dikira jika tetingkap 126 sesi lengkap dalam data.
- **Label masuk (bebas daripada keluar):** `besar` = tutup mencapai ≥ P + 50 % dalam 126 sesi SEBELUM mana-mana tutup
  ≤ P − 15 % (P = harga beli pada buka esok). Dilaporkan bersama: `besar100` (≥ +100 % sebelum −15 %) dan puncak tutup.
- **Kayu ukur:** kadar tangkap `besar` lawan saham rawak hari sama × tercile ATR % ("pilih"); skor = min dua era carian
  bagi [kelebihan − 2 ralat piawai], n ≥ 100 setiap era; carian pada kumpulan A, laporan pada kumpulan B (K1, K2, K3).
- **Ruang masuk:** SEMUA pencetus sedia ada (500 asal + 656 varian keluarga K + varian kaedah M CS07) × [0–1 prasyarat
  pasaran] × [0–1 prasyarat syarikat] × [0–2 penapis saham] — enjin (i). Pengesahan uptrend (pecah puncak 52 minggu, pecah
  tinggi + volum, gap, templat Minervini, Supertrend, ADX, RS) sudah berada dalam ruang ini; carian yang menentukan mana yang
  benar-benar mendahului pelari besar.
- **Papan:** 12 setup teratas ikut skor A (maks 2 setiap induk, 3 setiap pasangan prasyarat), ID `T01`–`T12` (lorong trend;
  BUKAN kod F). "Dipercayai-T" = belian B ≥ 200, ≥ 8 tahun aktif, kelebihan `besar` > 0 dalam K1, K2 DAN K3.
- **Keluar (trend tamat):** 38 atom (tutup < MA20/50/100; dua tutup < MA20/50; MA20 < MA50; MA50 menurun; EMA20/50;
  Supertrend; tutup < rendah 10/20/50 hari; MACD perlahan; RSI14 < 40/45/50; Chandelier 3–8 × ATR14; ekor 70–90 % tutup
  tertinggi; tiada kemajuan selepas 20/40 sesi) × syarat aktif {sentiasa, selepas +10 %, selepas +20 %} × henti {−10 %,
  −15 %, −20 %, 4×ATR14, 6×ATR14, min(−15 %, 5×ATR14)}, serta `X00` (henti + 126 sesi). Ukuran `tb` = dijual dengan untung
  ≥ +30 %. Pilihan dua peringkat pada A seperti (n)(b): 10 keluar sejagat teratas (purata merentas setup papan bagi min dua
  era [tb − tb `X00` henti sama]), kemudian setiap setup memilih antara `X00` dan 10 itu ikut min dua era tb.
- **Bacaan dikunci:** lorong trend "ada kelebihan" jika sekurang-kurangnya separuh setup papan Dipercayai-T; keluar
  "menolong" jika pada B tb keluar terpilih > tb `X00` (henti sama) bagi lebih separuh setup papan.
- Dilaporkan bagi setiap setup: belian setahun; daripada 100 belian berapa `besar` / `besar100` (rawak); dijual ≥ +30 %;
  menang; rugi ≥ 15 %; purata; sesi pegang; dan sama ada isyarat April 2026 MXL termasuk (kes rujukan pengguna, maklumat).
- **Kaveat dikunci:** tiada saham delist — bagi pegang 6 bulan biasnya LEBIH besar daripada lorong swing; K3 pendek
  (tetingkap 126 sesi berakhir ~April 2026); kumpulan B sudah dilihat untuk label lain; satu kes (MXL) bukan bukti.

### Pindaan 15 Nov 2026 (r) — pusingan CS09: KELUAR daripada maklumat yang BELUM dicuba (sebelum dijalankan)

Sebab: item 4 matlamat ("keluar: indikator yang memberitahu kenaikan sudah tamat") ialah satu-satunya item yang belum capai
selepas CS07 (`SERAHAN_CARIAN_SETUP.md` §1a). CS07 mencari 225,840 cara keluar setiap setup, tetapi SEMUA 97 atomnya dibina
daripada harga/volum harian saham itu sendiri. Keputusan pengguna 15 Nov 2026: "Cari keluar cara baharu". Pusingan ini menguji
kelas maklumat keluar yang belum dicuba. Tiada jejak hadapan, tiada order, tiada perubahan registry atau kohort.

Kod `carian_setup/cs_keluar9.py` (topeng, henti dan statistik `cs_keluar7` dipakai semula; hanya peringkat `sedia` diperluas
dengan jenis atom baharu, pariti dengan `cs_keluar7` diuji pada atom lama); keluaran `hasil/CS09/KELUAR.md`, `keluar.csv`.

**Tidak berubah daripada (n)(b) dan (p):** mekanik (isyarat pada tutup → beli buka esok; atom dinilai pada tutup sesi d → jual
buka sesi d + 1; henti intrahari; had 20 sesi; kos 0.5 %); pegang minimum 3 sesi (indikator keluar menjual paling awal pada
buka sesi ke-4, henti kekal aktif); 8 henti; 3 syarat aktif {sentiasa, selepas tutup tertinggi ≥ +5 %, selepas ≥ +10 %};
ukuran `tp` (naik ≥ 5 % minggu pertama DAN dijual dengan untung ≥ +10 %); syarat "tidak jual awal" (nisbah simpan ≥ 0.90);
statistik atas SEMUA isyarat masuk setup (perbandingan berpasangan, penjelasan (n)-1); carian pada kumpulan A sahaja.

**80 atom baharu dalam enam kelas** (tiada satu pun dalam 97 atom CS07):
- **P — pasaran (22; sama bagi semua saham pada hari itu):** daripada lapisan (i): QQQ OFF (`QA02`); SPY < SMA200 (`QA04`);
  QQQ ≥ 10 % di bawah puncak (`QA06`); rejim OFF baharu ≤ 10 sesi (`QA09`); QQQ RSI14 < 35 (`QA10`); turun-naik SPY 21 hari
  ≥ 25 % (`QB01`); ≤ 30 % saham di atas MA50 (`QC02`); distribution day QQQ ≥ 5 dalam 25 sesi (`QH03`); nisbah 4 % < 0.5
  (`QH06`); BUKAN `QH08` (QQQ SMA10 ≤ SMA20); BUKAN `QB03` (turun-naik SPY 21 hari ≥ 63 hari). Siri QQQ harian baharu: tutup <
  SMA10 / SMA20 / SMA50; tutup < rendah 5 / 10 hari sebelumnya; pulangan sehari ≤ −1.5 % / ≤ −2.5 %; pulangan 5 sesi ≤ −3 % /
  ≤ −5 %; 3 tutup menurun berturut; keluasan (% saham layak A + B di atas MA50) turun ≥ 10 mata dalam 10 sesi.
- **S — sektor/industri (2):** sektor 3 terbawah pulangan 63 sesi (`QD02`); industri 20 % terbawah pulangan 63 sesi (`QE03`).
- **E — peristiwa earnings (10; kalendar 8-K item 2.02 yang sama dengan prasyarat `QF`):** earnings pada sesi berikutnya
  (jual sebelum laporan); reaksi earnings terakhir (0–5 sesi lalu; reaksi = tutup hari reaksi ÷ tutup sebelumnya − 1) ≤ −5 % /
  ≤ −3 % / ≤ 0 % / < +3 %; hari reaksi itu (0–5 sesi lalu) tutup < buka; 0–10 sesi selepas reaksi DAN tutup < tutup sebelum
  earnings; k hingga 10 sesi selepas reaksi, k ∈ {1, 3, 5}.
- **R — relatif kepada pasaran (5):** pulangan k sesi saham − pulangan k sesi QQQ ≤ −x: (5, 5 %), (5, 10 %), (10, 10 %),
  (10, 15 %); RS < 70.
- **K — kemuncak / terlalu panas (17; saham sendiri tetapi tiada dalam CS07):** (tutup − SMA20) ÷ ATR14 ≥ 3 / 4 / 5 / 6;
  tutup ≥ 10 % / 15 % / 20 % di atas SMA10; tutup > jalur atas Bollinger(20, 2.5) / (20, 3.0); 4 / 5 / 6 tutup naik berturut;
  gap naik ≥ 2 % / ≥ 4 % DAN tutup < buka; julat hari ≥ 2.5 × ATR14 DAN tutup dalam separuh bawah julat; naik ≥ 2 × ATR14
  sehari dengan volum ≥ 2 × purata 50; ekor atas ≥ 60 % julat dengan volum ≥ 1.5 ×.
- **L — keadaan laluan sejak beli (24):** tiada tutup tertinggi baharu selama k sesi, k ∈ {3, 5, 7, 10}; pulang ≥ f daripada
  untung puncak (tutup ≤ P + (1 − f) × (tutup tertinggi − P), tutup tertinggi > P), f ∈ {1/3, 1/2, 2/3}; gagal corak (selepas
  d sesi, tutup < P × (1 + x)): (5, +3 %), (5, +5 %), (8, +5 %), (10, +5 %), (10, +10 %); lantai untung (selepas tutup tertinggi
  ≥ +a, tutup < +b): (5 %, 0 %), (10 %, 3 %), (10 %, 5 %), (15 %, 8 %), (20 %, 10 %); tutup < rendah bar tutup tertinggi;
  distribution day saham sejak beli ≥ k (tutup turun, volum > semalam DAN ≥ purata 50), k ∈ {2, 3, 4}; Chandelier yang
  mengetat ikut masa (k0 × ATR14 hingga sesi 10, kemudian k1): (4 → 2), (5 → 2.5), (3 → 1.5).

**Peraturan:** `X00`; 80 atom baharu tunggal; pasangan baharu × baharu (ATAU, DAN); pasangan baharu × lama (80 × 97; ATAU,
DAN — termasuk "indikator saham hanya dikira bila pasaran lemah"); dan SATU peraturan lama sebagai penanda aras: keluar
sejagat terbaik CS07 (`Y08.10 ATAU Y09.4`). ≈ 21,900 peraturan × 3 syarat aktif × 8 henti ≈ 526,000 cara keluar setiap
setup. Pasangan lama × lama tidak diulang (sudah dicari dalam CS07). **Setup** = 69 setup kedudukan akhir semasa.

**Pilihan pada kumpulan A (dua peringkat, seperti (n)(b)), dua senarai sejagat:**
- Senarai T ("tangkap"): 30 teratas ikut purata merentas setup bagi [min dua era (tp − tp `X00` henti sama)], lulus nisbah
  simpan ≥ 0.90 (jumlah merentas setup). Setiap setup memilih antara `X00` (8 henti) dan 30 itu (lulus simpan setup itu) ikut
  min dua era tp, seri dipecah ikut rugi ≥ 8 % terendah. Penanda aras CS07 sentiasa calon.
- Senarai R ("sisi rugi"): 30 teratas ikut purata merentas setup bagi [min dua era (purata dagangan − purata `X00` henti
  sama)], lulus nisbah simpan ≥ 0.90 DAN purata merentas setup [min dua era (tp − tp `X00`)] ≥ 0. Setiap setup memilih antara
  `X00` (8 henti) dan 30 itu (lulus simpan setup itu dan tp min dua era ≥ tp `X00` henti sama) ikut min dua era purata.

**Bacaan dikunci (kumpulan B):**
1. **Item 4, "keluar baharu MENOLONG"** jika (i) tp keluar terpilih-T > tp `X00` (henti sama) DAN > tp keluar terbaik CS07
   setup itu (`hasil/CS07/keluar.csv`; bagi `F88`–`F95`, keluar dalam registry), bagi lebih separuh setup; (ii) median nisbah
   simpan ≥ 0.90; (iii) median beza rugi ≥ 8 % lawan keluar terbaik CS07 ≤ +1 mata; (iv) dalam K3 (2025–26, tahun yang carian
   tidak lihat), median merentas setup (isyarat K3 ≥ 30) bagi [tp terpilih-T − tp `X00` henti sama] > 0.
2. **Sisi rugi (BUKAN item 4; untuk item 5 dan matlamat akaun "untung bersih melebihi rugi"), "potong rugi MENOLONG"** jika
   bagi lebih separuh setup: purata terpilih-R > purata `X00` (henti sama) DAN rugi ≥ 8 % terpilih-R < `X00` DAN tp terpilih-R
   ≥ tp `X00` − 0.5 mata; median nisbah simpan ≥ 0.90; dan dalam K3 median [purata terpilih-R − purata `X00`] > 0.
   Kayu ukur keluarga F kekal kadar tangkap; bacaan 2 hanya menjawab "adakah keluar baharu mengurangkan rugi tanpa menjual
   pelari".

**Dilaporkan sebagai maklumat (bukan bacaan):** bagi setiap kelas (P, S, E, R, K, L) peraturan atom tunggal terbaik pada A
dan nilainya pada B dan K3; komposisi kelas dalam kedua-dua senarai sejagat; **plasebo** bagi kelas P, S, E (siri yang sama
dianjak 437 sesi/bar secara membulat, seperti (i)): atom tunggal sebenar lawan plasebo; menang, rugi ≥ 8 %, purata,
kekurangan dari puncak, sesi pegang.

**Kaveat dikunci:** kumpulan B berkongsi HARI yang sama dengan kumpulan A — bagi keluar ikut pasaran (kelas P) saham B bukan
ujian bebas; hanya K3 yang tidak dilihat dari segi masa, dan K3 pendek. Kumpulan B sudah dilihat dalam pusingan terdahulu.
Lebih banyak calon = skor A terbaik lebih melambung. Tarikh earnings = tarikh pemfailan 8-K sebenar; "earnings pada sesi
berikutnya" mengandaikan tarikh diumumkan lebih awal (andaian sama seperti `QF01`). Tiada saham delist. Lima pusingan terdahulu
(CS04, (j), CS06, CS07 masuk, CS07 keluar) tidak menemui keluar yang mengatasi "pegang 20 sesi": pusingan ini mengukur kelas
maklumat baharu, bukan menjanjikan hasil.

**Selepas bacaan:** registry F, kedudukan akhir dan kohort jejak TIDAK diubah oleh pusingan ini. Jika bacaan 1 atau 2
"MENOLONG", penukaran keluar mana-mana setup memerlukan keputusan pengguna dan pindaan bertarikh berasingan.

### Pindaan 15 Nov 2026 (s) — pusingan CS10: keluar daripada maklumat baharu pada LORONG TREND `T01`–`T12` (sebelum dijalankan)

Sebab: CS08 (q) mencari "trend tamat" dengan 38 atom TUNGGAL daripada harga saham itu sendiri sahaja (0 daripada 12 menolong;
33–50 % dagangan rugi ≥ 15 %). CS09 (r) menunjukkan kelas maklumat baharu tidak menolong dalam bingkai 4 minggu; bagi pegangan
6 bulan keluar ikut pasaran dan peristiwa lebih munasabah dan BELUM diukur. Keputusan pengguna 15 Nov 2026: "ya" (uji jenis
keluar baharu pada lorong trend). Tiada jejak hadapan, tiada order, tiada perubahan papan `T01`–`T12`, registry atau kohort.

Kod `carian_setup/cs_keluar10.py`; keluaran `hasil/CS10/KELUAR.md`, `keluar.csv`, `sejagat.csv`. Setup = 12 setup papan CS08
seperti direkod dalam `hasil/CS08/papan.csv` (pencetus, prasyarat, penapis dibaca semula daripada fail itu; pariti dengan angka
CS08 disemak sebelum hasil keluar dibaca).

**Tidak berubah daripada (q) dan (p):** had pegang 126 sesi (tetingkap lengkap); mekanik (atom pada tutup sesi d → jual buka
sesi d + 1; henti intrahari; kos 0.5 %); pegang minimum 3 sesi; 6 henti {−10 %, −15 %, −20 %, 4×ATR14, 6×ATR14,
min(−15 %, 5×ATR14)}; 3 syarat aktif {sentiasa, selepas tutup tertinggi ≥ +10 %, selepas ≥ +20 %}; ukuran `tb` = dijual dengan
untung ≥ +30 %; label `besar` (tutup ≥ +50 % sebelum tutup ≤ −15 %); statistik atas SEMUA isyarat setup (berpasangan); carian
pada kumpulan A sahaja. Kernel baharu (topeng bit 125 sesi supaya pasangan boleh dinilai); pariti dengan `cs_trend8` pada
atom tunggal lama diuji.

**90 atom baharu dalam enam kelas, diskala untuk pegangan 6 bulan:**
- **P — pasaran (22):** sama seperti (r).
- **S — sektor/industri (2):** sama seperti (r).
- **E — peristiwa syarikat (10):** earnings pada sesi berikutnya; reaksi earnings terakhir (0–5 sesi lalu) ≤ −10 % / ≤ −5 % /
  ≤ 0 %; hari reaksi (0–5 sesi lalu) tutup < buka; 0–10 sesi selepas reaksi DAN tutup < tutup sebelum earnings; **premis masuk
  hilang:** hasil suku terkini (diumumkan sebelum hari itu) tumbuh < 20 % / < 10 % / < 0 %; kejutan untung terkini negatif
  (SUE < 0).
- **R — relatif kepada pasaran (6):** pulangan k sesi saham − QQQ ≤ −x: (20, 10 %), (20, 20 %), (60, 15 %), (60, 30 %);
  RS < 70; RS < 90.
- **K — kemuncak / terlalu panas (24):** 17 atom (r) ditambah tutup ≥ 30 % / 50 % / 70 % di atas SMA50; (tutup − SMA50) ÷
  ATR14 ≥ 6 / 8 / 10; tutup ≥ 100 % di atas SMA200.
- **L — keadaan laluan/saham (26):** tiada tutup tertinggi baharu selama k sesi, k ∈ {20, 40, 60}; pulang ≥ f daripada untung
  puncak, f ∈ {1/3, 1/2, 2/3}; gagal corak (selepas d sesi, tutup < P × (1 + x)): (20, +5 %), (40, +10 %), (60, +10 %),
  (60, +20 %), (90, +20 %); lantai untung (selepas tutup tertinggi ≥ +a, tutup < +b): (20 %, 5 %), (30 %, 10 %), (50 %, 20 %),
  (50 %, 30 %), (100 %, 50 %); tutup < rendah bar tutup tertinggi; Chandelier mengetat ikut masa (k0 × ATR14 hingga sesi 60,
  kemudian k1): (8 → 4), (6 → 3), (5 → 3); Chandelier mengetat ikut untung (k0 hingga tutup tertinggi ≥ +a, kemudian k1):
  (8 → 4, +50 %), (6 → 3, +50 %), (8 → 5, +30 %); distribution day saham ≥ k dalam 25 sesi, k ∈ {4, 5, 6}.

**Peraturan:** `X00`; setiap atom tunggal (38 lama + 90 baharu); SEMUA pasangan (ATAU, DAN) antara 128 atom, termasuk lama ×
lama (CS08 hanya menguji atom tunggal). 16,385 peraturan × 3 syarat aktif × 6 henti = 294,930 cara keluar setiap setup.

**Pilihan pada kumpulan A (dua peringkat, 10 sejagat seperti (q)), dua senarai, dengan syarat "tidak jual awal" BAHARU bagi
lorong ini:** nisbah simpan = jumlah untung terealisasi pada belian berlabel `besar` ÷ jumlah yang sama bagi `X00` (henti sama)
≥ 0.90.
- Senarai T: 10 teratas ikut purata merentas 12 setup bagi [min dua era (tb − tb `X00` henti sama)], lulus simpan (jumlah
  merentas setup). Setiap setup memilih antara `X00` (6 henti) dan 10 itu (lulus simpan setup itu) ikut min dua era tb, seri
  dipecah ikut rugi ≥ 15 % terendah.
- Senarai R ("sisi rugi"): 10 teratas ikut purata merentas setup bagi [min dua era (purata dagangan − purata `X00` henti
  sama)], lulus simpan DAN purata merentas setup [min dua era (tb − tb `X00`)] ≥ 0. Setiap setup memilih antara `X00` dan 10
  itu (lulus simpan setup itu dan tb min dua era ≥ tb `X00` henti sama) ikut min dua era purata.

**Bacaan dikunci (kumpulan B, 12 setup):**
1. **Keluar lorong trend (item 14), "keluar baharu MENOLONG"** jika (i) tb terpilih-T > tb `X00` (henti sama) DAN > tb keluar
   CS08 setup itu (`papan.csv`: semuanya `X00` pada henti terpilih CS08), bagi lebih separuh setup; (ii) median nisbah simpan
   ≥ 0.90; (iii) median beza rugi ≥ 15 % lawan keluar CS08 ≤ +1 mata; (iv) dalam K3 (isyarat 2025–26, digabung merentas 12
   setup kerana sedikit): tb terpilih-T − tb `X00` (henti sama) > 0.
2. **Sisi rugi, "potong rugi MENOLONG"** jika bagi lebih separuh setup: purata terpilih-R > purata `X00` (henti sama) DAN rugi
   ≥ 15 % terpilih-R < `X00` DAN tb terpilih-R ≥ tb `X00` − 0.5 mata; median nisbah simpan ≥ 0.90; dan dalam K3 (digabung)
   purata terpilih-R − purata `X00` > 0.

**Dilaporkan sebagai maklumat:** atom tunggal terbaik setiap kelas (A, B, K3) dan plasebo kelas P, S, E (anjak 437
sesi/bar); komposisi kelas kedua-dua senarai; keluar sejagat pada B; bagi setiap setup: tb, menang, rugi ≥ 15 %, purata,
median, sesi pegang, untung pada pelari besar.

**Kaveat dikunci:** 12 setup sahaja (bacaan "lebih separuh" = ≥ 7) dan beberapa berkongsi pencetus/prasyarat (bukan 12 ujian
bebas); kumpulan B berkongsi HARI yang sama dengan A (kelas P bukan ujian bebas; K3 pendek, tetingkap 126 sesi berakhir ~April
2026); tiada saham delist — bias LEBIH besar bagi pegangan 6 bulan; kumpulan B sudah dilihat; ratusan ribu calon atas beberapa
ratus isyarat setiap setup = risiko padanan lampau tinggi, sebab itu pilihan dua peringkat dan bacaan pada B.

**Selepas bacaan:** papan `T01`–`T12` tidak diubah; penukaran keluar memerlukan keputusan pengguna dan pindaan berasingan.

### Keputusan pengguna 15 Nov 2026 (selepas CS09 dan CS10) — prinsip keluar diterima; carian keluar manual dihentikan

Selepas enam pusingan dengan arah yang sama (CS04, (j), CS06, CS07, CS09, CS10) pengguna memutuskan ("1.ya 2.x 3.ya"):
- **Keluar yang diterima bagi kedua-dua lorong = pegang hingga had masa (20 sesi swing; 126 sesi trend) + henti rugi
  longgar.** Item 4 matlamat ("indikator yang memberitahu kenaikan sudah tamat") DITUTUP sebagai "dicari, tiada yang
  menolong" — bukan sebagai "capai".
- **Keluar `T01`–`T12` TIDAK ditukar** kepada "terlalu panas selepas untung ≥ 20 %": bacaan 1 (s) lulus, tetapi purata
  dagangan tidak naik dan pelari besar dijual awal.
- Pusingan CS baharu khusus untuk KELUAR dihentikan. Mesin berkala boleh mencuba keluar jika diperluas (perlu pindaan
  bertarikh kerana ruang mesin (n)(c) berubah). Pusingan keluar manual baharu hanya dengan sebab baharu (cth. data baharu)
  dan keputusan pengguna.
- Tiada perubahan pada registry F, kedudukan akhir, papan T atau kohort jejak: setup sedia ada kekal dengan keluar yang
  didaftarkan. Tiada jejak hadapan atau papertrade tanpa keputusan pengguna berasingan.

### Pindaan 15 Nov 2026 (t) — pusingan CS11: semak semula SEMUA setup F dengan ukuran longgar pengguna, pegang selepas 4 minggu, kekerapan, dan banding M / N / F (sebelum dijalankan)

Sebab (kata pengguna 15 Nov 2026, selepas menyemak 42 setup satu demi satu): "saya tak nak beli hari ni jual hari ni. at
least saham itu makin naik dan naik. 0.1% naik daily pun still ok lagi bagi saya. atau mungkin 1% daily. turun sikit bagi
saya still ok as long as trendnya adalah menaik. so just hold je. tak boleh la terlalu strict sangat sampai nak beli apa pun
susah, n asyik nak jual je"; "method F sepatutnya lagi better and far more better than M dan N"; "mungkin ada benda yang anda
miss". Tiga perkara yang Claude terlepas pandang: (1) ukuran `terus` (naik ≥ 5 % minggu pertama) lebih ketat daripada
kehendak pengguna; (2) setiap setup DIPAKSA jual pada sesi 20 walaupun saham masih naik; (3) kekerapan belian tidak pernah
dijadikan syarat. Keputusan pengguna ("1.C 2.B 3.B"): tunjuk KEDUA-DUA ukuran; selepas 4 minggu terus pegang sehingga trend
patah atau kena stop loss (diuji dahulu); F patut membeli sekurang-kurangnya beberapa kali sebulan pada senarai saham
pengguna. Keputusan 2.B ialah sebab baharu yang membuka semula soalan pegang/keluar (keputusan "carian keluar manual
dihentikan" kekal bagi carian luas; di sini hanya enam peraturan trend mudah yang diisytihar di bawah). Tiada jejak hadapan,
tiada order, tiada perubahan registry atau kohort. Kod `carian_setup/cs_semak11.py`; keluaran `hasil/CS11/`.

**Label (P = harga beli pada buka esok; sesi 1 = hari beli; bebas daripada cara jual):**
- `terus` (ketat, tidak berubah): tutup sesi 5 ≥ P + 5 % DAN tutup sesi 20 > tutup sesi 5 DAN −8 % tidak tersentuh.
- `naik` (longgar, BAHARU): tutup sesi 20 ≥ P + 2 % (≈ 0.1 % sehari) DAN tutup sesi 20 > purata tutup sesi 1–20 (trend masih
  naik) DAN tiada tutup ≤ P − 10 % dalam sesi 1–20 ("turun sikit" dibenarkan). Dilaporkan bersama: `naik10` (naik DAN tutup
  sesi 20 ≥ P + 10 %) dan `naik20` (≥ P + 20 %, ≈ 1 % sehari).
- Asas bagi kedua-dua label = saham rawak pada hari sama × tercile ATR % (seperti (d)); kelebihan dilaporkan setiap tempoh
  K1, K2, K3 pada kumpulan B.

**Cara pegang yang dibandingkan (stop loss setup kekal aktif sejak sesi 2; tiada jualan hari beli; had 126 sesi; hanya
isyarat dengan tetingkap 126 sesi lengkap; perbandingan berpasangan atas SEMUA isyarat):**
- `J20`: jual pada tutup sesi 20 (cara sekarang).
- Enam cara "pegang selagi trend naik": pegang sahaja hingga sesi 20; mulai tutup sesi 20, jual pada buka sesi berikutnya
  selepas tutup pertama yang memenuhi peraturan trend patah: `P-MA20` tutup < SMA20; `P-MA20x2` dua tutup berturut < SMA20;
  `P-MA50` tutup < SMA50; `P-R10` tutup < rendah 10 hari sebelumnya; `P-CH4` tutup < tutup tertinggi sejak beli − 4 × ATR14;
  `P-126` tiada peraturan trend (stop loss + 126 sesi; rujukan).
- Pilihan (kumpulan A sahaja): cara dengan purata merentas setup bagi [purata untung − purata untung `J20`] tertinggi.
- Bacaan dikunci (kumpulan B): "pegang selepas 4 minggu MENOLONG" jika bagi lebih separuh setup purata untung cara terpilih >
  `J20`, DAN median beza kadar menang ≥ −2 mata, DAN median beza rugi ≥ 15 % ≤ +2 mata. Dilaporkan bagi setiap cara: purata,
  menang, rugi ≥ 15 %, median sesi pegang, dan untung pada saham berlabel `naik`.

**Kekerapan:** belian setahun pada senarai Shariah semasa (`data/harga/univ.txt`; saham Shariah dalam kumpulan A dan B, satu
posisi setiap saham, 2010 – Ogos 2026), bagi setiap setup dan bagi senarai gabungan. Tafsiran Claude bagi "beberapa kali
sebulan": ≥ 24 belian setahun; dilaporkan setiap setup (maklumat) dan bagi gabungan setup yang lulus (syarat).

**Setup yang disemak:** semua setup F yang isyaratnya boleh dijana semula (69 setup kedudukan akhir), dengan stop loss
berdaftar masing-masing dan cara pegang di atas (isyarat jual berdaftar lama tidak dipakai: keputusan pengguna 15 Nov, keluar
= pegang + stop loss longgar). **Banding M / N / F:** isyarat asal setiap kaedah M (parameter lalai) dan setiap kaedah N,
tanpa prasyarat atau penapis, dengan cara pegang yang sama (`J20`, stop loss 4 × ATR14) — median dan lima teratas setiap
kumpulan pada `terus`, `naik`, menang dan kekerapan; rekod jualan hari sama kaedah M diambil daripada `hasil/PEGANG_MIN.md`.

**"Menepati semua" (takrif dikunci bagi pusingan ini):** ada prasyarat; tiada jualan hari beli dan jualan sebelum sesi 4 hanya
kerana stop loss; belian B ≥ 300 dan ≥ 10 tahun aktif; kelebihan `naik` > 0 dalam K1, K2 DAN K3. Kelebihan `terus` dilaporkan
di sebelahnya (ukuran ketat, "C: tunjuk kedua-dua").

**Kaveat dikunci:** setup F dipilih dahulu ikut ukuran ketat; menilai semula ikut `naik` bukan carian baharu — carian yang
dipangkatkan ikut `naik` (semua pencetus × prasyarat × penapis) ialah langkah berikutnya dan perlu pindaan sendiri. Kumpulan B
sudah dilihat; tiada saham delist; tetingkap 126 sesi mengurangkan isyarat 2026.

### Pindaan 15 Nov 2026 (u) — pusingan CS12: CARIAN BAHARU dipangkatkan ikut ukuran longgar `naik`, dengan cara pegang pilihan pengguna (sebelum dijalankan)

Keputusan pengguna 15 Nov 2026 selepas CS11 ("ya dan B"): (1) buat carian baharu yang mencari setup ikut ukuran longgar
(semua kaedah, prasyarat dan syarat); (2) **cara pegang B**: pegang sahaja (stop loss aktif) hingga hari ke-20, kemudian jual
pada buka selepas tutup pertama di bawah purata 20 hari (`P-MA20`), had 126 sesi. Cara B dipilih PENGGUNA selepas melihat
jadual CS11 pada saham yang tidak dilihat (purata +2.7 % lawan +2.1 %, kadar menang 51 % lawan 54 %); ia TIDAK lulus ujian
yang ditetapkan dahulu dalam (t) dan direkod begitu. Tiada papertrade, tiada order, tiada perubahan registry atau kohort
dalam pusingan ini. Kod `carian_setup/cs_cari12.py`; keluaran `hasil/CS12/`.

- **Sasaran:** label `naik` pindaan (t) (tutup sesi 20 ≥ P + 2 %, di atas purata tutup sesi 1–20, tiada tutup ≤ P − 10 %).
- **Pencetus:** semua 500 pencetus asal (kaedah M lalai + 2 varian, kaedah N, indikator P) + 656 varian keluarga indikator
  `K01`–`K25` + varian M CS07 yang sudah dijana. (1,472 varian M CS07 yang lain tidak dijana semula dalam pusingan ini.)
- **Ruang masuk:** enjin (i): [0–1 prasyarat pasaran (33)] × [0–1 prasyarat kumpulan/syarikat (15)] × [0–2 penapis saham
  (27)] bagi setiap pencetus.
- **Skor (kumpulan A sahaja):** min dua era bagi [kelebihan `naik` atas saham rawak hari sama × tercile ATR % − 2 ralat
  piawai], n ≥ 100 setiap era (enjin `cs_tala7.skor_ev`).
- **Calon:** bagi SETIAP pencetus, sehingga 5 peraturan masuk dengan skor tertinggi; semua yang skornya > 0. Tiada had
  bilangan dan tiada had kepelbagaian.
- **Setup lengkap setiap calon:** beli pada buka esok; stop loss 4 × ATR14 dari harga beli (aktif sejak sesi 2; tiada
  jualan hari beli); cara pegang B di atas.
- **Semakan pada kumpulan B, "lulus":** belian ≥ 300 (satu posisi setiap saham), ≥ 10 tahun aktif, kelebihan `naik` > 0
  dalam K1, K2 DAN K3 (takrif (t)). Dilaporkan: `naik` dan `terus` (rawak), naik ≥ 10 % / ≥ 20 % selepas 4 minggu, kadar
  menang dan purata di bawah cara pegang B dan di bawah "jual hari ke-20", rugi ≥ 15 %, median hari pegang, belian setahun
  pada senarai Shariah.
- **Kawalan rawak:** 300 peraturan masuk dipilih rawak daripada ruang yang sama (pencetus rawak × prasyarat × penapis
  rawak; n ≥ 100 setiap era pada A; benih 20261115) dinilai pada B dengan takrif "lulus" yang sama.
- **Bacaan dikunci, "carian ikut ukuran longgar BERHASIL"** jika bagi 100 calon dengan skor A tertinggi: lebih separuh lulus
  pada B, DAN kadar lulusnya ≥ kadar lulus kawalan rawak + 20 mata, DAN median kelebihan `naik` pada B ≥ +2 mata.
- **Susunan laporan:** ikut skor A (kriteria pilihan), bukan ikut angka B. Calon yang lulus ialah SENARAI untuk keputusan
  pengguna (pendaftaran kod F tanpa had bilangan = keputusan berasingan).
- **Kaveat dikunci:** beratus-ratus calon disemak pada B, jadi sebahagian lulus kerana nasib — sebab itu kawalan rawak
  dilaporkan di sebelahnya; kumpulan B sudah dilihat; tiada saham delist (bias lebih besar bagi pegangan hingga 6 bulan);
  kelebihan lawan rawak hari sama mengukur PILIHAN saham, manakala kadar mentah turut mengandungi kesan BILA membeli.

### Pindaan 15 Nov 2026 (v) — pusingan CS13: daftar SEMUA setup "naik laju" yang lulus (tanpa had bilangan), dan senarai utama F + cara pegang B (sebelum dijalankan)

Keputusan pengguna 15 Nov 2026 selepas CS12 ("1. ya 2.ya 3.A"): **(1)** senarai utama = setup F (saham naik laju, ukuran
ketat `terus`) dengan cara pegang B; **(2)** daftarkan SEMUA setup naik laju yang lulus, termasuk semakan 2025–26, tanpa had
bilangan (teguran pengguna: had 10–12 kod setiap papan ialah had Claude, bukan kehendak pengguna); **(3)** pilihan A: 1,368
calon ukuran longgar CS12 kekal REKOD sahaja dan carian "naik perlahan" dihentikan di situ (dibuka semula hanya dengan
keputusan pengguna atau sebab baharu, cth. data baharu). `F01`–`F95` TIDAK diubah (ID dan takrif kekal); kod baharu bermula
`F96`. Tiada papertrade (ditangguh pengguna), tiada order, kohort jejak hadapan tidak berubah. Kod
`carian_setup/cs_daftar13.py`; keluaran `hasil/CS13/`.

- **Sasaran:** label `terus` (tutup sesi 5 ≥ P + 5 %, tutup sesi 20 > tutup sesi 5, −8 % tidak disentuh; takrif (m)/(t)).
- **Pencetus, ruang masuk dan skor:** sama seperti (u) (1,169 pencetus yang sudah dijana; [0–1 prasyarat pasaran (33)] ×
  [0–1 prasyarat kumpulan/syarikat (15)] × [0–2 penapis saham (27)]; skor pada kumpulan A = min dua era bagi [kelebihan
  `terus` atas saham rawak hari sama × tercile ATR % − 2 ralat piawai], n ≥ 100 setiap era). Hanya label yang ditukar.
- **Calon:** bagi SETIAP pencetus, sehingga 5 peraturan masuk dengan skor tertinggi; semua yang skornya > 0. Tiada had
  bilangan.
- **Setup lengkap setiap calon:** beli pada buka esok; stop loss 4 × ATR14 (aktif sejak sesi 2; tiada jualan hari beli);
  cara pegang B (pegang hingga hari ke-20, kemudian jual pada buka selepas tutup pertama di bawah purata 20 hari; had 126
  sesi).
- **"Lulus" (kumpulan B):** belian ≥ 300 (satu posisi setiap saham, jual hari ke-20), ≥ 10 tahun aktif, kelebihan `terus` > 0
  dalam K1 (2010–19), K2 (2020–24) DAN K3 (2025–26). "Layak dinilai" = dua syarat pertama sahaja.
- **Kawalan rawak:** 300 peraturan masuk dipilih rawak daripada ruang yang sama (n ≥ 100 setiap era pada A; benih
  20261116), dinilai pada B dengan takrif yang sama.
- **Bacaan dikunci, "carian naik laju BERHASIL"** jika, antara peraturan yang layak dinilai: **(B1)** kadar lulus calon ≥
  kadar lulus kawalan + 20 mata, DAN **(B2)** bahagian calon dengan kelebihan `terus` > 0 pada 2025–26 (tahun yang carian
  tidak lihat) ≥ 60 % dan ≥ bahagian kawalan + 10 mata. **Pendaftaran kod F dibuat HANYA jika bacaan ini lulus**; jika gagal,
  tiada kod baharu dan hasilnya dilaporkan kepada pengguna.
- **Kembar (bukan had bilangan):** dua setup yang membeli saham yang sama pada hari yang sama bukan dua setup berlainan.
  Calon lulus disemak ikut susunan skor A; calon ialah "kembar" jika belian satu posisinya (kumpulan A + B) bertindih dengan
  satu setup yang sudah diterima pada Jaccard ≥ 0.80 (persilangan ÷ kesatuan). 69 setup F sedia ada yang dinilai dalam
  kedudukan akhir dikira sudah diterima. Kembar TIDAK diberi kod baharu; ia direkod dalam `hasil/CS13/calon.csv.gz` dengan
  ID setup yang diwakilinya. Setiap calon lulus yang bukan kembar diberi kod F — tiada had.
- **Pendaftaran:** kod `F96` dan seterusnya ikut susunan skor A; `pusingan = CS13`; status `BACKTEST`; takrif
  `pencetus|penapis|G6|PB|prasyarat` (`G6` = stop loss 4 × ATR14, `PB` = cara pegang B; pembetulan label sebelum
  dijalankan: kod stop loss 4 × ATR14 dalam `cs_keluar7.HENTI` ialah `G6`, bukan `G4` — peraturan tidak berubah). Lajur `n_K*`, `purata_K*`, `k10_K*`
  dan `menang_K*` = dagangan setup LENGKAP (stop loss 4 × ATR14 + cara pegang B, satu posisi setiap saham, tetingkap 126 sesi
  lengkap) pada kumpulan B.
- **Senarai utama (keputusan (1)):** `hasil/CS13/SENARAI_UTAMA.md` — 42 setup F lama yang dipercayai (takrif (m)) + semua
  kod baharu, SEMUA dinilai seragam dengan peraturan masuk masing-masing + stop loss 4 × ATR14 + cara pegang B. Disusun ikut
  kadar tangkap `terus` pada kumpulan B (seperti kedudukan akhir), dengan saham rawak hari sama, naik ≥ 5 % minggu pertama,
  ukuran longgar `naik`, kadar menang, purata setiap dagangan, rugi ≥ 15 %, median hari pegang, belian setahun pada senarai
  Shariah dan kelebihan 2025–26 di sebelahnya. `KEDUDUKAN_AKHIR.md` (69 setup dengan keluar asal) kekal rekod dan tidak
  dijana semula; keluar berdaftar `F01`–`F95` tidak diubah.
- **Kaveat dikunci:** beribu calon disemak pada kumpulan B, jadi sebahagian lulus kerana nasib — anggaran bahagian nasib
  (kadar lulus kawalan ÷ kadar lulus calon) dilaporkan; kumpulan B sudah dilihat berkali-kali; 2025–26 pendek dan belian di
  dalamnya sedikit; tiada saham delist; kelebihan lawan rawak hari sama mengukur PILIHAN saham, kadar mentah turut mengandungi
  kesan BILA membeli. Pangkat backtest, BUKAN bukti; kad skor kekal satu-satunya keputusan wang sebenar.

### Keputusan pengguna 16 Nov 2026 selepas CS13 ("ya 1,2,3") — susunan senarai utama; kembar; gabung ke `main`

1. CS11, CS12, CS13 dan tinjauan (w) digabung ke `main` melalui PR.
2. **Senarai utama memaparkan DAHULU setup "pilihan"**: kadar menang ≥ 50 % DAN purata setiap dagangan ≥ +2 % (cara pegang
   B, satu posisi setiap saham, kumpulan B); dalam setiap kumpulan susunan kekal ikut kadar tangkap `terus`. Tiada setup
   dibuang dan tiada kod F berubah; ini susunan paparan.
3. Calon lulus yang kembar (pertindihan ≥ 80 %) kekal TANPA kod F.

**Kaveat dikunci bagi (2):** tapisan "pilihan" dibuat SELEPAS melihat hasil pada kumpulan B, jadi angka menang dan purata
kumpulan itu condong ke atas. **Semakan ikut masa (ditulis sebelum dikira; dilaporkan sahaja, bukan syarat):** setup yang
menepati tapisan pada 2010–2024 SAHAJA (K1 + K2, berwajaran bilangan dagangan) dibandingkan dengan setup lain pada 2025–26
(K3): nilai tengah kadar menang dan purata, serta bahagian yang masih menang ≥ 50 % dan bahagian dengan purata > 0. Setup
dengan kurang 20 dagangan pada K3 dikecualikan daripada semakan itu.

### Pindaan 16 Nov 2026 (w) — tinjauan JENIS dan TEMPOH trend menaik setiap saham (deskriptif; sebelum dijalankan)

Permintaan pengguna 16 Nov 2026: "berapa jenis trend menaik ... utk satu satu saham? dan berapa lama ianya naik, ada table
tak? boleh research tak". Tinjauan DESKRIPTIF: bukan carian setup dan bukan pemilihan; tiada perubahan registry, senarai
utama atau kohort. Kod `carian_setup/cs_jenis_trend.py`; keluaran `hasil/TREND/`.

- **Data:** semua 3,260 saham (kumpulan A + B), tempoh panel carian, harga tutup harian.
- **Takrif "satu trend menaik" (zigzag ATR):** dari satu dasar ke satu puncak. Trend disahkan bermula apabila harga tutup
  naik ≥ k × ATR14 di atas tutup terendah sejak puncak lalu (dasar = tutup terendah itu), dan disahkan tamat apabila harga
  tutup jatuh ≥ k × ATR14 di bawah tutup tertinggi sejak dasar (puncak = tutup tertinggi itu). ATR14 pada hari semasa.
- **Tiga saiz ikut toleransi turun** (sepadan dengan tiga trend Teori Dow: kecil, sederhana, utama): k = 2; k = 4 (sama
  seperti lorong Chandelier projek); k = 8.
- **Yang dikira:** hanya trend lengkap dengan dasar pada bar layak (`sah`); ayunan pertama setiap saham (dasarnya terpotong)
  dan trend yang belum tamat pada hujung data dibuang dan bilangannya dilaporkan. "Lonjakan" = tempoh < 5 sesi (dilaporkan
  berasingan); "trend" = ≥ 5 sesi.
- **Ukuran setiap trend:** tempoh (sesi, dasar → puncak); kenaikan (tutup puncak ÷ tutup dasar − 1); kelajuan = kadar harian
  terkompaun dasar → puncak; turun paling dalam di tengah jalan (dari tutup tertinggi berjalan, tidak termasuk kejatuhan
  penamat). Bahagian yang boleh dikenal SEMASA berlaku: dari bar pengesahan naik hingga bar pengesahan tamat (tempoh dan
  perubahan harga tutup, tanpa kos).
- **Jenis ikut kelajuan** (ambang daripada angka pengguna sendiri: 0.1 % sehari; 1 % sehari ≈ 5 % seminggu): sangat perlahan
  < 0.25 % sehari; perlahan 0.25–0.5 %; sederhana 0.5–1 %; laju ≥ 1 % sehari.
- **Jadual:** (1) setiap saiz: bilangan setiap saham setahun, tempoh (median dan 25 %–75 %), kenaikan, taburan tempoh (< 1
  bulan, 1–3 bulan, 3–6 bulan, > 6 bulan; 21 sesi = 1 bulan); (2) saiz × jenis kelajuan: bahagian, tempoh, kenaikan, turun
  di tengah jalan; (3) "sudah naik N sesi → berapa peratus sampai 2N, dan median baki"; (4) bahagian yang boleh dikenal
  semasa berlaku; (5) kestabilan median tempoh ikut tahun.
- **Kaveat dikunci:** dasar dan puncak hanya diketahui SELEPAS berlaku — ini gambaran, bukan isyarat beli atau jual; kelajuan
  dasar → puncak melebihi apa yang dagangan sebenar boleh tangkap; tiada saham delist; angka bergantung pada takrif (sebab
  itu tiga saiz ditunjuk).

## 8. Apa yang TIDAK dibuat dalam CS01

Penalaan Optuna penuh 1,303 parameter kaedah M (hanya dua varian rawak setiap kaedah), gabungan ≥ 3 penapis, gabungan
≥ 3 indikator keluar, carian pada set 2000 penuh (dirancang melalui Actions selepas keputusan pengguna), dan simulasi
portfolio berslot. Pusingan seterusnya memerlukan pindaan bertarikh pada fail ini **sebelum** dijalankan.
