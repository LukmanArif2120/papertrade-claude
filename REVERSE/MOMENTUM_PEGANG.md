# MOMENTUM_PEGANG — Pattern saham high-momentum bawah lorong 2 (pegang selagi naik)

Dijalankan 1 Nov 2026. Pradaftar: `REVERSE/SPEC_MOMENTUM_PEGANG.md`.
Nama asal fail ini ialah `L99` (label daripada salah taip dalam permintaan pengguna); dinamakan semula
1 Nov 2026 mengikut konvensyen REVERSE (nama deskriptif, bukan ID bernombor). `L99` BUKAN ID yang
pernah wujud dalam repo; keluarga `L01`–`L03` ialah ID kaedah, bukan ID kajian (ditulis sebelum keputusan dilihat).
Soalan pengguna: saham yang boleh dipegang 3 hari ke atas atau dipegang selagi naik; pattern apa yang
memaksimumkan keuntungan; khususnya pattern **high momentum**.

Empat keputusan pengguna: sasaran = **peluang jadi trend besar**; keluar = **lorong 2 sahaja**;
alam = **763k dagangan enjin + A02**; keluaran = pradaftar + laporan dalam repo.

---

## 0. Semakan pemalsuan — LULUS 13/13

Simulator lorong 2 MOMENTUM_PEGANG menghasilkan semula setiap nombor terbitan `KAJIAN_LORONG2.md` pada 763,327
dagangan enjin, dalam toleransi pradaftar:

| Ukuran | MOMENTUM_PEGANG | Terbitan |
|---|---|---|
| Lorong 2 purata | **5.10%** | 5.1% |
| Lorong 2 median | −2.75% | −2.8% |
| Lorong 2 p5 | −18.24% | −18.2% |
| Lorong 2 hari | 43.78 | 43.8 |
| Lorong 2 sebulan | 2.45% | 2.4% |
| Lorong 2 lebih SPY sebulan | 1.15% | 1.2% |
| **Lorong 2 TANGKAP (trend besar)** | **25.13%** | 25.1% |
| Lorong 1 purata / hari / TANGKAP | 2.71% / 22.75 / 12.03% | 2.7% / 22.7 / 12.0% |
| Kadar trend besar | 33.01% | 33% |
| Hari p25/50/75 | 20 / 34 / 58 | 20 / 34 / 58 |
| Hari trend besar p25/50/75 | 31 / 54 / 85 | 31 / 54 / 85 |

ATR MOMENTUM_PEGANG dibuktikan sepadan `enjin.atr` dengan `np.allclose`.

**Tetapi semakan pemalsuan ini TIDAK memadai, dan audit kod bebas membuktikannya (§8):**
- Ujian asap SPEC §5 **menyala** (15 ralat dalam P1, 75 dalam P2) dan pipeline **tidak berhenti**, bertentangan
  dengan SPEC §5 yang menetapkan "Gagal → kajian berhenti". Ia mencetak ralat lalu mencetak "PEMALSUAN: LULUS"
  pada baris seterusnya. Saya menyiasat ralat itu secara manual dan mendapati ia bukan pepijat (ambang ±500%
  terlalu ketat bagi pegangan 300 hari dalam saham bergerak 100×; harga keluar disahkan berada dalam julat
  ticker sendiri) — tetapi pengesan yang selalu berbunyi ialah pengesan yang dimatikan.
- **Dua daripada lima ujian asap adalah VAKUM**: `hari < 1` mustahil kerana `hari = J − k + 1` dan `J ≥ k`;
  `(j_keluar == k) & (kod == 1)` mustahil kerana `kod = 1` hanya ditetapkan bersama `J = j+1 > k`. Jadi kelas
  pepijat 2 (henti degenerat hari-masuk) dan kelas pepijat 3 (paras henti di atas harga masuk — pepijat `X25`)
  **tidak pernah benar-benar diuji**. Ujian yang betul ialah `tutup[k] − 4×ATR[k] < buka[k]` pada 100% baris.
- **Satu pepijat MAUT dalam kod saya sendiri** ditemui oleh audit, bukan oleh ujian asap saya:
  `float NaN .astype(bool)` memberi **True** dalam numpy, jadi TANGKAP setiap pattern mengumpul kesemua sauh
  ufuk-terpotong ke dalam kumpulan "trend besar" manakala TANGKAP asas membuangnya dengan betul. Gate 4
  membanding dua takrifan berbeza. Keputusan gate asal dibuang dan dijalankan semula (§3).
- Satu pepijat lain ditangkap sendiri: lajur ufuk `r1`/`r2` bertembung nama dengan lajur pulangan lorong 1 /
  lorong 2 dalam skrip tempoh pegangan, menjadikan "purata lorong 2" dilapor sebagai pulangan 2 hari.

Kedua-dua pepijat itu mengesahkan semula pelajaran 31 Okt 2026 dalam bentuk baharu: **ujian asap pada
komponen tidak menangkap pepijat dalam penggabungan**, dan ujian asap yang tidak boleh gagal tidak menguji apa-apa.

---

## 1. DUA LORONG KELUAR — senarai yang diminta

### 1a. Sejarah (763,327 dagangan, 134 kaedah, masuk Nov 2019 – Okt 2026)

Dua cara mengukur, dan ia memberi **jawapan berbeza**. Audit bebas menunjukkan pradaftar §9.5 saya hanya
melaporkan yang pertama, dan itu memuji artifak tempoh pegangan:

| Ukuran | **Lorong 1** (peraturan kaedah) | **Lorong 2** (Chandelier tutup 4×ATR14) |
|---|---|---|
| Purata **setiap dagangan** | 2.709% | **5.099%** (1.88×) |
| Hari dipegang | 22.7 | 43.8 (1.93×) |
| **Purata setiap BULAN pendedahan** | **2.501%** | 2.446% |
| TANGKAP setiap dagangan (pada dagangan ≥ +30%) | 12.03% | **25.13%** (2.09×) |
| Hari dipegang pada dagangan itu | 34.7 | 62.5 |
| **TANGKAP setiap BULAN pendedahan** | 7.28% | **8.44%** (1.16×) |
| Lebih SPY setiap bulan | — | 1.152% |
| Mengatasi lorong satu lagi | — | 80% kaedah |

Nisbah pulangan (1.88×) hampir **sama** dengan nisbah tempoh pegangan (1.93×). Maka kelebihan per-dagangan
lorong 2 ialah **pendedahan, bukan kelebihan**: pada modal yang sama diputar pada kadar yang sama, lorong 1
memberi 2.501%/bulan dan lorong 2 memberi 2.446%/bulan — lorong 2 **sedikit lebih rendah**.
`KAJIAN_LORONG2.md` sendiri sudah melaporkan 2.5 lawan 2.4 dalam jadualnya; pradaftar saya tidak membacanya.

**Di mana lorong 2 benar-benar menang:** pada dagangan yang MEMANG menjadi trend besar, dan selepas normalisasi
masa — **8.44%/bulan lawan 7.28%/bulan (+1.16 mata)**. Itulah kelebihan sebenar, dan ia lebih kecil daripada
"menggandakan tangkapan" yang angka mentah cadangkan.

Tanpa 15 ticker ekstrem (§1b) kedua-dua jawapan bertambah ketat terhadap lorong 2:

| Tanpa 15 ticker ekstrem | Lorong 1 | Lorong 2 |
|---|---|---|
| Setiap dagangan | 2.177% | 3.409% |
| **Setiap bulan** | **2.009%** | 1.640% |
| TANGKAP setiap dagangan | 10.60% | 20.25% |
| **TANGKAP setiap bulan** | 6.36% | **6.81%** (1.07×) |
| **Lebih SPY setiap bulan** | — | **0.327%** (daripada 1.152%) |

**Ini dapatan MOMENTUM_PEGANG yang paling penting untuk repo, bukan untuk pengguna:** dakwaan teras `KAJIAN_LORONG2.md`
("lebihan SPY sebulan tertinggi = pilihan, 1.2%") jatuh kepada **0.33%** apabila 15 ticker (2.3% dagangan)
dibuang. Pilihan lorong 2 masih boleh dipertahankan — ia menang pada trend besar per unit masa, dan
`KAJIAN_LORONG2.md` §Batasan sudah menyatakan kelebihan tertumpu pada 2020 dan 2025 — tetapi margin
keselamatannya jauh lebih kecil daripada yang direkod.

Teguh terhadap pemotongan hujung data:
- Buang dagangan yang masih terbuka pada bar akhir (`kod==2`): L2 **4.766%** lawan L1 2.667%; TANGKAP 24.43% lawan 11.96%.
- Hanya masuk sebelum 2026 dan sudah ditutup: L2 **5.176%** lawan L1 2.835%; TANGKAP 24.74% lawan 12.06%.

### 1b. Kerapuhan purata lorong 2 — had yang mesti dibaca bersama

| Potongan | n | Purata | TANGKAP |
|---|---|---|---|
| Semua | 763,327 | 5.10% | 25.13% |
| Buang 15 ticker ekstrem | 738,404 | **3.41%** | 20.25% |
| Buang 605 baris (0.08%) dengan pulangan > +500% | 762,722 | 3.79% | 21.20% |
| Winsor 99% (potong pada +115%) | — | 3.14% | — |

- **AXTI seorang menyumbang 15.1% daripada JUMLAH pulangan lorong 2** merentas 134 kaedah; SNDK 5.1%, WDC 3.2%.
  Sepuluh ticker teratas = **33.6% jumlah pulangan daripada 2.3% dagangan**.
- 1% dagangan teratas = **61.1% jumlah pulangan** — replikasi bebas angka 63.7% dalam `KOLAM_EKOR.md`.
- Tahun masuk 2020 + 2025 = **77.5% jumlah pulangan daripada 29% dagangan**.
- Pergerakan itu **BENAR, bukan artifak pecahan**: nisbah tutup-ke-tutup bersebelahan tertinggi dalam seluruh
  sejarah AXTI ialah 1.693 (tiada diskontinuiti pecahan), dan A02 — dataset bebas dengan lajur `faktor_split`
  sendiri — bersetuju pada julat 2025 (1.16–16.38). Dua dataset repo memang **bercanggah** pada tahap harga
  (`data_mentah` dilaras hadapan **termasuk dividen**, A02 pecahan sahaja), dan `data_mentah` mengandungi
  jurang yang kelihatan seperti pecahan songsang tidak dilaras (FCEL 2.27× pada 2019-07-02, ASST 5.56× pada
  2025-05-07; A02 merekod `faktor_split` 0.05 untuk ASST). Arm utama MOMENTUM_PEGANG (§3) menggunakan A02.

### 1c. Data forward (Papertrade C, 8,748 posisi, 8–30 Okt 2026)

| | Lorong 1 | Lorong 2 |
|---|---|---|
| Tutup | 2,404 | 296 |
| Masih pegang | 6,344 | 8,452 |
| Purata (yang tutup) | −3.24% | −13.97% |
| Menang | 18.2% | 2.0% |
| Hari median | **2** | 10 (kalendar) |

**Lorong 2 forward TIDAK BOLEH dibaca sebagai prestasi lorong 2.** Chandelier hanya tercetus selepas jatuh
4×ATR dari puncak, jadi dalam tingkap 3 minggu hanya **yang gagal cepat** yang keluar. 8,452 posisi yang
masih dipegang berada pada purata **+1.50%** (52.8% positif). Had ini ditulis dalam pradaftar §7 sebelum
data dilihat.

**Dapatan forward yang BOLEH dipercayai** — lorong 1 tidak memberi pegangan 3 hari ke atas:

| Tempoh pegangan lorong 1 | n | Purata | Menang |
|---|---|---|---|
| **0 hari** | **491 (20.4%)** | −2.47% | **0.00%** |
| 1 hari | 637 | −2.18% | 27.0% |
| 2 hari | 303 | −3.59% | 14.9% |
| 3–4 hari | 434 | −4.86% | 15.0% |
| 5–9 hari | 435 | −3.73% | 26.9% |
| 10+ hari | 104 | −3.55% | 36.5% |

**59% keluar lorong 1 berlaku dalam 2 hari, dan 491 posisi keluar pada HARI MASUK dengan kadar menang
0.00%** — kecacatan henti hari-0 (`KOLAM_EKOR.md` §4a) direplikasi secara langsung pada data hadapan.
Jika pengguna mahu pegangan ≥ 3 hari, **lorong 1 secara mekanikal tidak boleh memberikannya**; lorong 2 boleh
(ia tidak memakai henti kaedah dan parasnya pada hari masuk ialah `tutup − 4×ATR`, jadi mustahil tercetus
hari masuk).

---

## 2. ARM UTAMA — A02, 8,935,267 sauh, setiap bar cair, tiada kaedah

3,240 ticker, 2010-01 – 2026-10. LATIH 2010–2019 (4,530,580 sauh) / TAHAN 2020–2026 (4,404,687 sauh, selepas
membuang 103,529 baris `kod==2` yang belum pernah keluar — §8b pepijat 2). SE **berkelompok dua hala**
(bulan masuk × ticker, Cameron-Gelbach-Miller), lebih ketat daripada pradaftar §8 yang hanya menetapkan kelompok
tarikh, kerana pegangan 44 hari bermakna dagangan **bertindih** merentas ticker yang sama. Nilai p daripada
taburan-t, df = kelompok−1. **86 pattern × 3 sasaran = 258 ujian dalam kiraan BH-FDR** (lebih daripada 176 yang
dipradaftar, jadi ambang lebih ketat). `G1 sektor atas MA50` dan `G2 rejim SPY` tidak diuji dalam larian terbetul
kerana lajurnya tidak disimpan ke parquet (§8b pepijat 6); nilainya daripada larian tidak terbetul menunjukkan
kedua-duanya gagal.

**Asas lorong 2 tanpa apa-apa isyarat masuk (beli SETIAP bar cair):**

| | LATIH | TAHAN |
|---|---|---|
| Pulangan setiap dagangan | 1.929% | 1.884% |
| **Pulangan setiap bulan pendedahan** | 0.823% | **0.900%** |
| Hari dipegang | 49.2 | 44.0 |
| Menang | 42.4% | 38.8% |
| P(trend besar) mutlak | 20.16% | 31.15% |
| P(trend besar) dinormal | 25.00% | 24.68% |
| TANGKAP / setiap bulan | 19.44% / 5.65% | 20.41% / 6.83% |
| **Pulangan selepas buang 5% teratas** | −0.916% | **−2.579%** |

### 2a. Keputusan gate (dua sasaran, kedua-duanya dengan G3 dan G4 dinormal masa)

| Gate | Sasaran MUTLAK | Sasaran DINORMAL |
|---|---|---|
| G0 n ≥ 2,000 dua tingkap | 86 / 86 | 86 / 86 |
| G1 ΔP(TB) > 0 DAN lift R2 > 0 dua tingkap | 6 | 21 |
| G2 BH-FDR q ≤ 0.05 (atas 258) | 68 | 70 |
| G3 pulangan/bulan > asas | 50 | 50 |
| G4 TANGKAP/bulan ≥ asas | 32 | 35 |
| **LULUS KESEMUA** | **5** | **3** |

**Sasaran MUTLAK — 5 lulus:**

| Pattern | n | ΔP(TB) | Q | Pulangan | lift | /bulan | TANGKAP/bulan | R2(−5%) |
|---|---|---|---|---|---|---|---|---|
| **S3 RS SPY 6 bulan, desil teratas** | 441,412 | **+15.78** | <0.0001 | **3.041%** | **+1.286** | **1.484%** | **8.02%** | −3.61% |
| **H1 Qullamaggie anggaran** | 178,414 | +16.08 | <0.0001 | 2.988% | +1.151 | 1.442% | 7.71% | −3.26% |
| D1 `vol_n50 ≥ 1.5` | 547,891 | +3.00 | 0.008 | 2.551% | +0.762 | 1.182% | 7.46% | −2.64% |
| S4 hampir tinggi 52w **D8** (bukan D10) | 440,392 | +5.97 | <0.0001 | 2.315% | +0.479 | 1.110% | 7.05% | −2.66% |
| H2 Minervini anggaran | 808,654 | +5.30 | <0.0001 | 2.237% | +0.433 | 1.072% | 6.88% | −2.56% |

**Sasaran DINORMAL — 3 lulus:** `S3 RS SPY 6b D10` (ΔP(TBn) +4.08, Q<0.0001) · `H2 Minervini` (+5.52) ·
`A2 RS SPY 6b&12b > 0` (+2.40, tetapi lift pulangan hanya +0.059 = tidak bermakna).

**Satu pattern lulus KEDUA-DUA sasaran, KEDUA-DUA arm, dan kesemua gate: `S3` = desil teratas kekuatan
relatif 6 bulan lawan SPY, disusun silang-keratan setiap sesi.** Pulangan 3.041% lawan asas 1.884%
(**+62%**), setiap bulan 1.484% lawan 0.900% (**+65%**), pada 441,412 sauh.

Takrif pattern yang lulus:
- `S3` = pangkat persentil ≥ 0.90 bagi `rs_spy_6b` (pulangan 126 hari saham − pulangan 126 hari SPY) dalam
  keratan rentas sesi itu.
- `H1 Qullamaggie anggaran` = `roc60` desil teratas **DAN** `atr_pct ≥ 3` **DAN** dalam 25% tinggi 52 minggu
  **DAN** median nilai dagang 20 bar ≥ USD 10 juta.
- `H2 Minervini anggaran` = tutup > MA50 > MA150 > MA200 **DAN** dalam 25% tinggi 52w **DAN** ≥ 30% atas rendah
  52w **DAN** `roc60` kuartil teratas.

### 2b. Had yang paling penting bagi kelima-lima

`R2(−5%)` — jangkaan selepas membuang 5% dagangan terbaik — ialah **−2.56% hingga −3.61%** bagi kesemua lima,
berbanding asas **−2.579%**. **`S3` dan `H1` lebih BURUK daripada asas pada ukuran ini.** Maknanya kelebihan
mereka bukan sahaja hidup dalam ekor kanan, ia **lebih tertumpu pada ekor** daripada asas. Pattern ini
menjadikan taburan lebih berat ke kanan, bukan lebih baik secara seragam. Dengan 8–10 slot, kebarangkalian
menangkap ekor itu rendah — itulah sebabnya diagnostik portfolio (§4) gagal walaupun gate lulus.

### 2c. Pembetulan sasaran mutlak lawan dinormal

Sasaran +30% mutlak **mengukur volatiliti**. Buktinya muktamad: `C1 ATR% tertile teratas` memberi ΔP(TB)
**+23.72 mata** — kesan terbesar dalam seluruh kajian — dan `C2 ATR% tertile terbawah` memberi **−23.90 mata**,
hampir simetri sempurna. Dengan sasaran dinormal (`mx120 ÷ ATR% ≥ 10`, kadar asas ditala supaya hampir sama):

| Pattern | ΔP(TB) mutlak | ΔP(TB) dinormal |
|---|---|---|
| C1 ATR% tertile teratas | **+23.72** | **−3.26** |
| C2 ATR% tertile terbawah | −23.90 | **+3.11** |
| E4 julat10 tertile terbawah | −19.37 | +3.13 |
| S4 hampir tinggi 52w D10 | **+19.83** | **−3.86** |
| B1 dalam 5% tinggi 52w | −11.02 | +5.18 |
| B2 susunan MA (lapis) | −6.71 | +5.83 |
| S2 roc60/ATR% (Clenow) D10 | +3.26 | **+5.88** |

Lapan daripada lapan menukar tanda atau berubah besar. **Volatiliti mentah bukan pattern; ia unit ukuran.**
Ini kegagalan reka bentuk pradaftar, bukan dapatan terpilih — kedua-dua set keputusan dilapor.

### 2d. URUTAN mengalahkan PENAPIS — jangkaan priori #3 BETUL

Purata lift pulangan pada TAHAN: **urutan D10 +0.520** · penapis +0.034 · kesatuan +0.015 (larian tidak
terbetul; arahnya tidak berubah dalam larian terbetul kerana pembetulan menjejaskan semua jenis sama rata).
Ini mengesahkan mekanisme yang `SETUP.md` dan `SISTEM.md` ukur: menapis membuang bar pada ekor, menyusun tidak
membuang apa-apa. Berbeza dengan `GABUNGAN.md`, **kesatuan tidak membantu di sini** — `GABUNGAN.md` menyatukan
12 signal yang sudah terbukti ada lift, manakala kesatuan MOMENTUM_PEGANG dibentuk daripada keluarga pattern mentah.

### 2e. Bentuk desil — di mana wang sebenarnya berada

`S1 roc60`, TAHAN: `P(TB)` berbentuk **U** (D1 42.5%, D5 25.6%, D10 43.8% — kedua-dua hujung ialah volatiliti)
tetapi pulangan **monotonik menaik** (0.77% → 2.72%). Momentum membayar pada purata pulangan, bukan pada
kebarangkalian ekor.

`S4 hampir tinggi 52w`: `P(TB)` monotonik menaik (24.3% → 49.0%) tetapi pulangan **memuncak pada desil 8**
(2.54%) dan **jatuh pada desil 10** (1.26%, di bawah asas). Membeli **pada** tinggi 52 minggu memberi peluang
tertinggi untuk bergerak +30% dan pulangan terendah. Itulah sebabnya **D8 yang lulus gate, bukan D10**:
**hampir tinggi, belum pecah.**

### 2f. PERANGKAP PANGKAT #1 — dan ia hanya pada momentum mentah

Pulangan lorong 2 mengikut pangkat harian tepat, TAHAN terbetul (asas 1.884% = 0.900%/bulan):

| Pangkat harian | `roc60` mentah | `roc60÷ATR%` (Clenow) | RS SPY 6 bulan |
|---|---|---|---|
| **#1** | **−10.26%** (−6.21%/bln) | −2.58% | **+4.68%** (+2.23%/bln) |
| #2–8 | +2.71% | +2.32% | −0.48% |
| **#9–40** | **+3.00%** (1.54%/bln) | **+3.26%** (1.66%/bln) | +2.43% |
| #41–100 | +2.31% | +2.72% | +2.99% |
| #101–400 | +2.58% | +2.21% | **+3.08%** (1.47%/bln) |
| #401+ | +1.76% | +1.80% | +1.69% |

**Saham dengan `roc60` paling tinggi setiap hari ialah dagangan terburuk dalam keseluruhan taburan**
(−10.26%, n = 1,704 sesi) walaupun `P(TB)`-nya 52.4%. Ia mencapai +30% lebih kerap daripada hampir mana-mana
kumpulan dan tetap merugikan: lorong 2 keluar selepas kejatuhan 4×ATR dan ATR nama itu sangat besar.

**Tetapi perangkap ini TIDAK universal.** Dengan RS 6 bulan, pangkat #1 ialah yang **terbaik** (+4.68%).
Jadi dakwaan yang sah ialah: perangkap itu khusus kepada **pecutan harga jangka pendek** (`roc60`), bukan
kepada kekuatan relatif jangka sederhana. `n = 1,704` bagi setiap baris #1 jadi ketiga-tiga angka itu bising;
yang **teguh** merentas ketiga-tiga skor ialah **pangkat #9–40 dan #101–400**, kedua-duanya mengalahkan asas
dengan 0.3–0.75 mata sebulan.

Hujung ekstrem (0.2% teratas) setiap skor: `S1` −0.86%, `S3` −1.51%, `S5` −0.73%, `S4` +0.28% — semuanya
runtuh daripada nilai D10. Hanya **dua** bertahan: `S2` roc60÷ATR% **+1.26%** dan `S6` gabungan pangkat
**+1.30%**. Normalkan dengan volatiliti dan hujung ekstrem berhenti menjadi perangkap.

### 2g. ALAM mengalahkan PATTERN — dan ia bias

Arm P1 (dagangan enjin, set 431) memberi **12 daripada 85 lulus** pada sasaran mutlak, lebih banyak daripada
5/86 pada A02, dan dengan lift jauh lebih besar (`A3` lift +13.0 mata lawan maksimum +1.29 pada A02). Punca
diasingkan dengan menjalankan pattern A02 **terhad kepada 431 ticker yang sama**, tiada kaedah terlibat, 2023–2026:

| | Alam penuh A02 (3,240 ticker) | Terhad kepada set 431 |
|---|---|---|
| Asas pulangan lorong 2 | 1.884% | **3.773%** |
| Asas TANGKAP | 20.41% | **22.53%** |
| `A3`, `C1`, `A1`, `F1`, `H1` lulus G4? | tidak | **ya** (TANGKAP `A3` 31.14%) |

Jadi lift besar P1 bukan kaedah dan bukan pattern — ia **alam**. Memilih alam 431 nama berbaloi **+1.89 mata
peratus setiap dagangan**, lebih besar daripada lift mana-mana pattern pada alam penuh (maksimum +1.29).
Tetapi set 431 dipilih **selepas melihat data**, jadi nombor itu **bukan boleh didagangkan** — ia ukuran saiz
bias pemilihan alam. Ini mengisi paksi `AL02` dalam registry dengan angka: **pemilihan alam lebih berkuasa
daripada mana-mana signal yang pernah diukur dalam repo ini, dan ia juga paling mudah menipu diri sendiri.**

## 3. POST-HOC (BUKAN pradaftar, tiada dakwaan gate) — pattern paling kuat bukan pada masuk

706,649 dagangan enjin ufuk penuh, selepas membuang `kod==2`. Asas: P(TB) 34.05%, pulangan 5.261%
(**2.477%/bulan**), TANGKAP 24.77%, hari 44.6.

| Peraturan selepas masuk | n | % dagangan | P(TB) | Pulangan | **/bulan** | TANGKAP | Hari |
|---|---|---|---|---|---|---|---|
| Asas (semua) | 706,649 | 100% | 34.05% | 5.261% | **2.477%** | 24.77% | 44.6 |
| Selepas 3 hari masih ≤ 0 | 346,333 | 49.0% | 29.50% | 1.628% | **0.793%** | 21.78% | 43.1 |
| Selepas 3 hari > 0 | 360,316 | 51.0% | 38.43% | 8.753% | 3.995% | 26.97% | 46.0 |
| Selepas 3 hari > +3% | 142,647 | 20.2% | 51.15% | 14.805% | 6.502% | 31.24% | 47.8 |
| **Selepas 3 hari > +5%** | **73,695** | **10.4%** | **60.16%** | **21.066%** | **8.997%** | **36.73%** | 49.2 |
| Selepas 5 hari > +5% | 113,446 | 16.1% | 58.65% | 20.157% | 8.407% | 35.11% | 50.4 |
| **Selepas 10 hari > +10%** | **76,598** | **10.8%** | **73.70%** | **33.263%** | **12.591%** | **44.43%** | 55.5 |

Desil pulangan 3 hari: P(TB) 27.0% pada desil tengah naik ke **60.8%** pada desil teratas.

**Pattern yang paling kuat meramal trend besar bukanlah apa-apa pada carta sebelum masuk — ia kelakuan saham itu
sendiri dalam 3 hari pertama selepas masuk.** +5% dalam 3 hari menaikkan P(TB) daripada 34% ke 60% dan pulangan
lorong 2 daripada 5.26% ke 21.07%. Kelebihan ini **bertahan normalisasi pendedahan**, yang membezakannya daripada
kelebihan per-dagangan lorong 2 (§1a): 8.997%/bulan lawan 2.477%/bulan = **3.6×**, dan 12.591% lawan 2.477% =
**5.1×** bagi peraturan 10 hari. Tiada pattern masuk yang pernah diukur dalam repo ini (598 setup, 280 NXX,
48 kombinasi silang, 86 MOMENTUM_PEGANG) menghampiri magnitud ini.

Ini **bukan** penapis masuk dan tidak boleh digunakan untuk memilih belian. Ia peraturan **paksi PEGANG**
(`PG01–PG06` dalam registry, belum pernah diuji): tambah kepada yang berfungsi, potong yang tidak. Ia memerlukan
pradaftar sendiri — khususnya (a) ia dikira pada populasi dagangan kaedah Mxx pada set 431, bukan alam A02;
(b) sebahagian daripadanya mungkin momentum jangka pendek yang dilabel semula; (c) kos tambahan daripada
menambah saiz posisi di tengah dagangan belum dimodelkan.

## 4. Diagnostik portfolio (pradaftar SPEC_MOMENTUM_PEGANG §8) — 8 dan 40 slot lawan SPUS

Alam A02, 2020-01 – 2026-10, keluar lorong 2, berat sama rata, satu posisi setiap ticker.
Penanda aras: **SPUS 17.95%/tahun** (CAGR seluruh tingkap, `PEMBINAAN.md`).

| Lorong | 8 slot | 40 slot |
|---|---|---|
| **RAWAK (median 20 benih)** | **+10.39%** | **+9.52%** |
| S2 roc60÷ATR% (Clenow) | +1.67% | +6.06% |
| S6 gabungan pangkat | −18.13% | +4.35% |
| S1 roc60 | −13.98% | +2.57% |
| S3 RS SPY 6b | −14.39% | +1.55% |

**Masuk RAWAK mengalahkan setiap lorong momentum tersusun**, dan kedua-duanya kalah kepada SPUS. Sebabnya
ialah §2e: dengan 8 slot anda membeli berhampiran pangkat #1–8 setiap hari, iaitu kawasan terburuk dalam
taburan. Hanya lorong Clenow (dinormal volatiliti) tidak runtuh — konsisten dengan §2e.

**Had:** siri ekuiti saya menilai posisi terbuka pada **kos**, jadi MDD daripada simulasi ini **tidak sah**
dan tidak dilaporkan. Hanya CAGR dilapor. Pembetulan yang diperlukan: nilai posisi terbuka pada tutup harian.

---

## 5. Jangkaan priori saya (pradaftar SPEC_MOMENTUM_PEGANG §9) — 3 betul, 2 salah

| # | Jangkaan | Keputusan |
|---|---|---|
| 1 | 10–20 daripada 88 lulus G1 | **SALAH.** 6/86 (mutlak) dan 21/86 (dinormal) pada A02 |
| 2 | G3 ialah pengikat, ≤ 5 lulus | **SEPARUH BETUL.** Bilangan betul (5 dan 3) tetapi sebab salah: G3 lulus 50/86; **G1 dan G4** yang mengikat |
| 3 | Urutan > kesatuan > penapis | **BETUL.** +0.520 / +0.015 / +0.034 (kesatuan jatuh ke bawah penapis) |
| 4 | Tiada portfolio mengalahkan SPUS | **BETUL.** Terbaik +10.39% lawan 17.95%; masuk rawak mengalahkan setiap lorong tersusun |
| 5 | TANGKAP ialah nombor paling berguna, bukan pattern | **SEPARUH BETUL.** Betul bahawa ia bukan pattern, tetapi nombor yang paling berguna ternyata **parameter keluar** (§8d: sebaran 1.049 mata/bulan, 1.8× lift masuk terbaik), dan TANGKAP mentah memuji artifak pendedahan (§1a: 1.16× bukan 2.09×) |

Corak kesilapan saya berubah. Dalam tiga pradaftar terdahulu saya memandang **rendah** struktur statistik dalam
ruang belum diukur. Kali ini kesilapan utama bukan arah tetapi **reka bentuk**: saya tidak menormalkan sasaran
ikut volatiliti (§2c), tidak menormalkan perbandingan lorong ikut pendedahan (§1a), dan menulis dua ujian asap
yang tidak boleh gagal (§8a). Ketiga-tiganya ditemui oleh ukuran atau audit, bukan oleh intuisi saya. Saya juga
tidak meramalkan perangkap pangkat #1 (§2f) dan tidak meramalkan bahawa pemilihan **alam** akan mengalahkan
setiap pattern dalam magnitud (§2g).

---

## 6. Jawapan kepada soalan pengguna

Selepas audit enam agen dan tiga larian semula, mengikut urutan magnitud yang DIUKUR dan BERTAHAN:

**1. Parameter KELUAR, bukan pattern masuk — dan repo sudah betul.** Sapuan ganda ATR tanpa apa-apa pattern
memberi sebaran **1.049 mata sebulan** (1.5× → 1.397%, 3× → 1.689%, **4× → 2.446% = puncak**, 12× → 2.350%),
lawan **0.584 mata sebulan** bagi lift pattern masuk terbaik. Parameter keluar **1.8× lebih berpengaruh** dan
lorong 2 repo sudah berada pada puncaknya. Cliff sebenar di bawah 3×; **jangan ketatkan ekor di bawah 3×ATR**.

**2. Jangan potong awal.** 491 posisi Papertrade C keluar lorong 1 pada **hari masuk** dengan menang **0.00%**;
59% keluar dalam 2 hari. Pegangan ≥ 3 hari yang anda mahu **tidak boleh** datang daripada lorong 1 — ia mesti
datang daripada lorong 2, yang secara struktur tidak boleh keluar pada hari masuk. Syarat "≥ 3 hari" sendiri
tidak mengikat apa-apa: **100% dagangan lorong 2 sudah ≥ 3 hari** (median 34 hari).

**3. Lorong mana, dengan syarat.** Per dagangan lorong 2 menangkap 25.13% daripada trend besar lawan 12.03%
(2.09×). Per unit modal-masa ia **8.44%/bulan lawan 7.28%/bulan (1.16×)**, dan 6.81% lawan 6.36% (1.07×) tanpa
15 ticker ekstrem. Jadi **lorong 2 menang jika slot bukan kekangan anda**. Jika anda sentiasa ada lebih banyak
isyarat daripada slot, lorong 1 memutar modal 1.93× lebih cepat dan jurangnya hampir tertutup.

**4. Peraturan selepas masuk — paling kuat setakat ini, tetapi POST-HOC.** +5% dalam 3 hari menaikkan
P(trend besar) 34.1% → **60.2%** dan pulangan lorong 2 5.26% → **21.07%** (**8.997%/bulan lawan 2.477%**).
+10% dalam 10 hari → 73.7% dan 33.3% (12.591%/bulan). Ia **bertahan normalisasi pendedahan**, yang
membezakannya daripada kelebihan per-dagangan lorong 2. Tiada pattern masuk yang pernah diukur dalam repo
(598 setup, 280 NXX, 48 silang, 86 MOMENTUM_PEGANG) menghampiri magnitud ini. **Belum dipradaftar.**

**5. Satu pattern masuk sahaja bertahan setiap ujian: desil teratas kekuatan relatif 6 bulan lawan SPY.**
Pulangan 3.04% lawan asas 1.88% (**+62%**), 1.484%/bulan lawan 0.900% (**+65%**), n 441,412, ΔP(trend besar)
**+15.78 mata**. Ia satu-satunya yang lulus kedua-dua sasaran, kedua-dua arm, **dan** kedua-dua ujian
teguh-tindihan (bootstrap blok CI95 [+0.297, +2.544]; subsampel tak-bertindih p = 0.011).
Empat yang lain (`Qullamaggie`, `vol_n50 ≥ 1.5`, hampir-tinggi-52w D8, `Minervini`) lulus gate pradaftar tetapi
**gagal sekurang-kurangnya satu ujian teguh-tindihan**; `Minervini` gagal kedua-dua.

**6. Susun, jangan tapis; dan jangan beli yang paling panas.** Urutan memberi lift 15× penapis. Pangkat
**#9–40** dan **#101–400** harian mengalahkan asas dengan 0.3–0.75 mata sebulan merentas ketiga-tiga skor.
Pangkat **#1** pada `roc60` memberi **−10.26%** — tetapi pangkat #1 pada RS 6 bulan memberi **+4.68%**, jadi
perangkap itu khusus kepada **pecutan harga jangka pendek**, bukan kekuatan relatif.
Dan **beli hampir tinggi 52 minggu, bukan pada tinggi**: desil 8 memberi lift +0.479, desil 10 memberi
**−0.902** dengan ΔP(TB) +19.83.

### Apa yang jawapan ini TIDAK beri

- **Gate mengukur desil (10% alam = 441,412 sauh); anda ada 8–10 slot (~0.3% ekstrem setiap hari).** Di
  kawasan ekstrem itu urutan momentum **kalah kepada rawak** (§2f, §4). Lima pemenang per-dagangan **belum**
  diuji pada "N teratas setiap tarikh" bagi N = 8.
- **Selepas buang 5% dagangan terbaik**, keempat daripada lima pemenang **lebih buruk daripada asas**
  (−2.56% hingga −3.61% lawan −2.579%). Kelebihan mereka bukan sahaja hidup dalam ekor — ia **lebih tertumpu**
  di sana.
- **Diagnostik portfolio:** 8 slot, masuk **rawak** +10.39%/tahun mengalahkan setiap lorong momentum tersusun,
  dan semuanya kalah kepada **SPUS 17.95%**.
- **74.3% keuntungan dalam data kajian datang daripada saham DI LUAR alam dagangan Syariah anda**, dan repo
  tiada keahlian SPUS titik-masa untuk membetulkannya (paksi `AL02`).
- **Sasaran "trend besar" bukan ekor.** Kadar asasnya 31–34% = median-atas. Ekor sebenar ~1.3%, dan peringkat
  pattern pada dua sasaran itu berbeza sampai 4×.
- **n berkesan 8,700–18,500**, bukan 9 juta.

### Pengesahan silang data forward

Antara posisi Papertrade C yang dipegang ≥ 3 hari, 10% terbaik mengandungi **gred RS A pada 34.6% berbanding
19.9% keseluruhan (1.74×)**; median `rs_rating` 81 lawan 76. Itu sejajar dengan `S3` — satu-satunya pattern
yang bertahan setiap ujian pada 17 tahun data. Sebaliknya **gred industri A kurang terwakili (24.5% lawan
40.1%)** dan median `skor_industri` pemenang **59 lawan 69.6**. n = 503, tingkap 3 minggu: kewarasan arah,
bukan bukti — tetapi dua sumber bebas menunjuk arah sama pada feature yang sama.

### Satu ayat

Saham high-momentum yang boleh dipegang ialah yang **kuat relatif kepada pasaran selama 6 bulan** (itu
satu-satunya pattern masuk yang bertahan setiap ujian), dibeli **hampir — bukan pada — tinggi 52 minggu** dan
**bukan pada pangkat #1**; tetapi wang itu datang daripada **memegangnya 6–9 minggu dengan ekor 4×ATR**
(parameter yang repo sudah tetapkan pada optimum, dan 1.8× lebih berpengaruh daripada pattern itu sendiri),
dan **anda perlu banyak slot** kerana pada 8 slot pemilihan momentum kalah kepada rawak.

## 7. Had

- **Bias penyintas A02**: 88.5% ticker mempunyai bar terakhir pada/selepas 2026-09-01 (11.5% berakhir lebih
  awal). Nama yang mati tidak boleh mencapai +30%, dan pattern momentum memilih populasi yang kadar delistnya
  paling tinggi, jadi setiap `P(TB)` dan setiap ΔP(TB) ialah **had ATAS** yang saiznya tidak diketahui.
  Pengesahan pada alam yang mengandungi delist belum dijalankan dan itu ujian paling penting yang tinggal.
- Set 431 (§1, §2f) dipilih selepas melihat data; ia semakan pemalsuan, bukan pengesahan.
- A02 berakhir 16 Okt 2026; 3.7% sauh mempunyai ufuk TB terpotong dan **dibuang** daripada pengiraan P(TB).
- Paksi CARA kekal `C01` (beli pada buka esok); paksi SAIZ, IMBANG dan KORELASI tidak diuji.
- MDD portfolio tidak sah (§4): posisi terbuka dinilai pada kos, jadi MDD terkurang. Hanya CAGR dilapor.
- Tingkap LATIH/TAHAN memisahkan tarikh MASUK tetapi bukan tarikh HASIL, jadi ia bukan dua replikasi bebas
  sepenuhnya (tindihan maksimum 120 bar + tempoh pegangan).
- `G1 sektor atas MA50` dan `G2 rejim SPY` tidak diuji dalam larian terbetul (§8b pepijat 6).
- Enam pepijat dalam kod MOMENTUM_PEGANG sendiri ditemui dan dibetulkan; dua daripadanya hanya ditemui oleh audit bebas,
  bukan oleh ujian asap saya (§8).
- Peta sektor bukan titik-masa.
- Ambang dinormal (10×ATR) dipilih supaya kadar asas sepadan sasaran mutlak; ia pilihan, bukan terbitan.
- Lihat §8 untuk audit kod bebas dan senarai penuh pembetulan.

---

## 7b. FASA 2 — tiga jurang ditutup (1 Nov 2026)

Jurang **A**, **C** dan **D** dalam §8f telah ditutup: `REVERSE/SPEC_MOMENTUM_PEGANG_2.md` (pradaftar) dan
`REVERSE/MOMENTUM_PEGANG_2.md` (keputusan). Ringkasan yang mengubah syor fasa 1:

| Leg | Keputusan | Kesan pada §6 |
|---|---|---|
| **A** top-N bukan desil | **0 / 28 lulus.** `S3` RS 6b runtuh pada 8 slot (0.090%/bulan lawan rawak 0.934%); hanya pakej `Minervini` dan `Qullamaggie` melepasi jalur rawak pada setiap N dalam kedua-dua tingkap; **tiada** lorong boleh dibezakan daripada rawak (CI95 0/28). Risiko ekor kiri pemilihan momentum **8–20× lebih tinggi** daripada rawak | §6 butir 5 **DIPINDA**: jangan guna RS 6 bulan tunggal pada 8–10 slot |
| **C** paksi PEGANG | **0 / 4 lulus; signifikan MERUGIKAN dalam LATIH** (CI95 mengecualikan sifar pada sisi negatif). Statistik bersyarat §3 betul tetapi bukan strategi: cabang pegang +9.807% hanya 6.7% dagangan, cabang potong 93.3% pada −0.617% | §6 butir 4 **DITOLAK** |
| **D** grid pattern × keluar | D1 lulus pada anggaran titik, **D2 dan D3 gagal**. Tiada interaksi: pilih pattern dan ganda secara berasingan. Pada A02 ganda 4× dan 6× **tidak boleh dibezakan**; yang pasti ialah jangan ke bawah 3× | §8d **DIBETULKAN**: 4× ialah plato, bukan puncak |

Satu kesan pattern signifikan dalam seluruh fasa 2: `S3` RS 6 bulan pada ganda 4, TAHAN,
**+0.627 mata/bulan, CI95 [+0.140, +1.121]** — tidak berulang dalam LATIH dan runtuh pada slot kecil.

---

## 8. Audit kod bebas — enam agen, enam pepijat dalam kod MOMENTUM_PEGANG sendiri

Enam agen bebas mengaudit MOMENTUM_PEGANG tanpa melihat keputusan satu sama lain: tiga lensa kod (pandang ke hadapan ·
pengindeksan dan bias penyintas · statistik), satu penerbitan bebas, satu semakan integriti data luaran, dan
satu kritik kelengkapan. 1.28 juta token, 217 panggilan alat. **Setiap dakwaan disahkan sendiri sebelum
diterima; tiga dakwaan ditolak atau dikecilkan.**

### 8a. Yang BERSIH (diuji dan lulus)

- **Tiada pandang ke hadapan** dalam mana-mana daripada 40 feature. Setiap lajur diperiksa satu demi satu:
  `donchian20/55` dan `breakout_asas` guna `.shift(1)`, `atas_awan` guna `.shift(26)` ke belakang,
  `pocket_pivot` tidak memasukkan volum turunnya sendiri. `REVERSE/semak_hadapan.py` meliputi **semua** lajur
  dengan 12–14 tarikh potong dan lulus bagi 2020–2025.
- **Penjajaran masa betul**: `G.ent = G.sig + 1 bar` bagi **763,327 / 763,327** dagangan, 0 pengecualian.
- **Kalendar SPY ialah superset ketat** bagi kesemua 3,252 kalendar ticker; kadar NaN feature P2 = 0.000%.
- **Tiada pepijat pengindeksan**: topeng `t+1` jajaran tepat; `J` selalu dalam `[k, n−1]`; hanyutan `cumsum`
  ATR maksimum 1.8e-9 mata; `del fr[t]` selamat.
- **PENERBITAN BEBAS LULUS.** Satu agen menulis simulator lorong 2 dari sifar, **dua kali** (gelung Python dan
  pandas tervektor), tanpa melihat `teras.py`. Ia menghasilkan semula **setiap** nilai terbitan
  `KAJIAN_LORONG2.md` atas kesemua 134 kaedah (n = 763,327): purata 5.099 · median −2.751 · p5 −18.240 ·
  hari 43.780 · sebulan 2.446 · TANGKAP 25.128 · TB 33.007 · hari p25/50/75 20/34/58 · hari TB 31/54/85 ·
  lorong 1 2.709/22.745/12.029. Dua pelaksanaannya sepadan **400/400** baris dengan saya.
  **Simulator bukan masalahnya.** Invarian `paras_k < tutup[k]` lulus **763,327 / 763,327**.
- **Ujian asap SEBENAR** (menggantikan dua ujian vakum) pada 942,443 sauh, liputan 100% baris: kelas 1
  (harga keluar di luar julat ticker sendiri) **0**; kelas 2 (keluar peraturan pada bar masuk) **0**; kelas 3
  (paras Chandelier ≥ tutup masuk) **0** pada populasi yang diukur. Satu-satunya pelanggaran (1,726 baris,
  ATR = 0 pada bar beku/pra-penyenaraian sintetik A02) **kesemuanya dibuang oleh tapisan cair**: dalam
  9,038,796 sauh P2, baris dengan `atr_pct ≤ 0` = **0**.
- **INTEGRITI DATA: hipotesis artifak pecahan DITOLAK bagi ketiga-tiga ticker**, disahkan bar demi bar
  terhadap Alpha Vantage raw, senarai pecahan bebas dan pemfailan SEC/Nasdaq:
  **AXTI BENAR** (raw tinggi Mei 2026 = 143.16 lawan A02 tutup maks 140.83; Okt 2026 raw 50.57–88.36
  merangkumi kedua-dua nilai A02); **FCEL BENAR** (tutup awal 204.01 ialah pelarasan ke belakang yang betul —
  raw Jan 2019 = USD0.567 = 204.01 ÷ 360, dan 360 = 12 × 30 daripada dua pecahan songsang kemudian; Alpha
  Vantage memberi faktor 360 yang sama secara bebas); **ASST BENAR** (jurang 5.56× disertai volum
  9,829 → 15,791,971 saham = **1,606×**, dan pelarasan pecahan tidak boleh mengubah volum).

### 8b. Pepijat yang ditemui dan dibetulkan (keputusan gate asal DIBUANG)

| # | Pepijat | Kesan diukur | Pembetulan |
|---|---|---|---|
| 1 | `float NaN .astype(bool)` memberi **True** dalam numpy, jadi TANGKAP setiap pattern memasukkan semua sauh ufuk-terpotong sebagai "trend besar" manakala TANGKAP asas membuangnya | **MAUT.** Gate 4 membanding dua takrifan. `A1` dilapor 17.92% (GAGAL) lawan nilai betul 21.94% (LULUS). Penjana **negatif-palsu** — cermin kepada pepijat `X25` | `nan_to_num(...)>0.5` pada kedua-dua pihak |
| 2 | Penyensoran hujung data `kod==2` (posisi belum pernah keluar) tidak dibuang, dan **asimetri**: LATIH 0.00%, TAHAN 2.30% | **MAUT.** Purata `r2` baris itu +9.011% lawan +1.884%. Asas TAHAN dilapor 2.047% lawan nilai betul **1.884%** | Semua baris `kod==2` dibuang |
| 3 | Baris yang **feature**-nya NaN masuk kumpulan KAWALAN, bukan dibuang | **MAUT.** Purata `r2` baris itu +41.3% dalam satu kes (ticker sejarah pendek = IPO meluru); ia menerbalikkan tanda Gate 1 bagi `A2` (−0.581 → +0.096). Artifak 0.50–0.68 mata **lebih besar daripada `N01` +0.392**, kelebihan masuk terbesar yang pernah bertahan dalam repo | Topeng 3-keadaan; baris NaN dibuang daripada KEDUA-DUA kumpulan |
| 4 | `TANGKAP` dan purata per-dagangan tidak dinormalkan ikut pendedahan | **MAUT untuk tafsiran.** Nisbah pulangan L2/L1 1.88× ≈ nisbah tempoh pegangan 1.93×; per bulan L2 2.446% lawan L1 **2.501%** | Lajur `sebulan` pada setiap baris; §1a ditulis semula |
| 5 | Kunci kelompok dua hala sebagai rentetan `U24`+`U24` → 192 bait/elemen | **SERIUS (OOM).** Larian P2 pertama **terbunuh**; RSS puncak 4.58 GB sebelum pengiraan | Kod integer (8 bait); lajur terhad; satu proses setiap tingkap |
| 6 | `G1 sektor atas MA50` **lesap senyap** (lajur tidak disimpan); dalam P1 juga `G2` dan `H1` | **SERIUS.** 1 daripada 24 penapis pradaftar tidak pernah diuji dalam P2 | Dilapor eksplisit; dibuang daripada kiraan FDR |

### 8c. TINDIHAN BERSIRI — kecacatan dalam PRADAFTAR, bukan dalam kod

Ini dapatan audit yang paling menentukan. Pradaftar §8 menetapkan SE berkelompok **ikut tarikh masuk**.
Itu salah: ufuk hasil (120 bar bagi TB, 44 hari bagi R2) **lebih panjang daripada blok masa**, jadi faktor
pasaran yang sama menyelesaikan ribuan dagangan serentak. Ukuran saya sendiri bagi `S3 RS SPY 6b D10`
(lift R2 = +1.286 mata, tetap merentas semua skema):

| Kelompok | SE | t | p |
|---|---|---|---|
| tarikh × ticker (**pradaftar**) | 0.429 | 3.00 | 0.0027 |
| bulan × ticker (**dilaksanakan**) | 0.630 | 2.04 | 0.0446 |
| kuartal × ticker | 0.804 | 1.60 | 0.122 |
| semester × ticker | 0.739 | 1.74 | 0.105 |
| tahun × ticker | 0.835 | 1.54 | 0.174 |

Jadi **pradaftar seperti ditulis akan menghasilkan dapatan palsu**: audit mengira semula BH-FDR bagi 87 pattern
dan mendapat, pada sasaran R2, **62/87 "signifikan" dengan kelompok tarikh → 5/87 dengan bulan × ticker →
0/87 dengan semester atau tahun**. Pada sasaran TB ia kukuh (80 → 68 → 59 → 56), tetapi gate yang 59/87 calon
lepasi bukan gate.

**Saya tidak menerima kesimpulan "0/87" itu sepenuhnya**, kerana kelompok dua hala dengan G = 13 (semester)
atau G = 7 (tahun) terkenal tidak boleh dipercayai. Dua kaedah tak-berparameter yang **bebas daripada andaian
kelompok** dijalankan sendiri, dan kedua-duanya menolak sifar bagi `S3`:

| Kaedah teguh-tindihan | `S3` lift R2 | Keputusan |
|---|---|---|
| Subsampel **tak-bertindih** (10 fasa, jarak 120 sesi) | min +1.297, sd merentas fasa 1.283 | t = 3.20, **p = 0.011** |
| **Bootstrap blok-bergerak** 120 sesi (300 cabutan) | min +1.337, sd 0.610 | CI95 **[+0.297, +2.544]**, sifar di luar |

Diuji atas kelima-lima pemenang — **hanya `S3` lulus KEDUA-DUA ujian teguh-tindihan:**

| Pattern | lift R2 | CI95 bootstrap blok | p subsampel fasa | Keputusan |
|---|---|---|---|---|
| **`S3` RS SPY 6b D10** | **+1.286** | **[+0.297, +2.544]** | **0.011** | **LULUS kedua-dua** |
| `H1` Qullamaggie | +1.151 | [−1.104, +3.603] | 0.014 | separuh (fasa ya, bootstrap tidak) |
| `D1` `vol_n50 ≥ 1.5` | +0.762 | [+0.057, +1.271] | 0.063 | separuh (bootstrap ya, fasa tidak) |
| `S4` hampir tinggi 52w D8 | +0.479 | [−0.223, +1.177] | 0.009 | separuh (fasa ya, bootstrap tidak) |
| `H2` Minervini | +0.433 | [−0.331, +1.908] | 0.216 | **GAGAL kedua-dua** |

Perbezaan penting: kesan **TB** (keahlian ekor) teguh bagi **kelima-lima** — CI95 bootstrap `d_TB` tidak
merangkumi sifar dalam setiap kes. Yang **tidak** teguh ialah lift **PULANGAN**. Jadi pattern ini memang
memilih saham yang lebih kerap bergerak besar; apa yang tidak boleh dibuktikan ialah bahawa lorong 2
mengeluarkan lebih banyak wang daripadanya, kecuali bagi `S3`.

Pengesahan sampingan dalam ujian yang sama: `S4` desil **10** memberi lift pulangan **−0.902** dengan
ΔP(TB) **+19.83** — pengukuran paling bersih bagi §2e. Membeli **pada** tinggi 52 minggu memaksimumkan
peluang bergerak +30% dan **merugikan** berbanding asas.

**n berkesan** bukan 9 juta: audit mengira **8,700 (TB) hingga 18,500 (R2)** pemerhatian berkesan. Itu nombor
yang betul untuk dibaca.

### 8d. SAPUAN PARAMETER KELUAR — kritik kelengkapan menemui yang paling berguna

MOMENTUM_PEGANG membelanjakan 258 ujian pada paksi **MASUK** (yang `NXX.md`, `SETUP.md` dan `SILANG.md` ukur hampir kosong)
sambil **membekukan** paksi KELUAR pada satu nilai (`ganda = 4`) tanpa mengukurnya. Saya sapu sendiri pada
763,327 dagangan, **tanpa apa-apa pattern masuk**:

| Ganda ATR | Purata/dagangan | Hari | **SEBULAN** | Median | Menang | p5 |
|---|---|---|---|---|---|---|
| 1.5× | 0.909% | 13.7 | 1.397% | −1.60% | 40.3% | −11.3% |
| 2× | 1.365% | 18.5 | 1.546% | −1.87% | 40.6% | −12.8% |
| 3× | 2.411% | 30.0 | 1.689% | −2.41% | 40.9% | −15.7% |
| **4× (yang repo guna)** | 5.099% | 43.8 | **2.446%** ← maks | −2.75% | 41.7% | −18.2% |
| 5× | 6.474% | 59.6 | 2.283% | −3.04% | 42.3% | −20.7% |
| 6× | 8.615% | 78.2 | 2.314% | −3.08% | 43.2% | −23.0% |
| 8× | 12.627% | 116.1 | 2.283% | −3.15% | 44.4% | −26.9% |
| 12× | 22.777% | 203.5 | 2.350% | −2.62% | 46.4% | −33.4% |

**Sebaran 1.049 mata sebulan daripada SATU parameter keluar**, lawan **0.584 mata sebulan** bagi lift pattern
masuk terbaik (`S3`). Parameter keluar **1.8× lebih berpengaruh daripada pattern masuk terbaik** — dan
**repo sudah berada pada puncaknya**. Cliff sebenar berada **di bawah 3×** (1.40–1.69%); 4× hingga 12× ialah
plato rata (2.28–2.45%), jadi 4× ialah pilihan yang betul tetapi bukan puncak tajam.

### 8e. Dakwaan audit yang DITOLAK atau DIKECILKAN

- **"A02 tiada delist sama sekali"** — ditolak sebahagian. Ukuran saya pada populasi sauh sebenar: **88.5%**
  ticker mempunyai bar terakhir pada/selepas 2026-09-01, jadi **11.5% memang berakhir lebih awal**. Bias
  penyintas tetap besar tetapi bukan mutlak. **Set 431 pula memang mutlak**: audit mengukur kesemua 431 ticker
  mempunyai bar terakhir pada **tepat** 2026-10-02 (sifar delist dalam 7.75 tahun, sedangkan kadar susut saham
  AS ~4–7%/tahun), dan **80 daripada 431 (18.6%) bermula selepas 2019-01-02** (IPO/spin-off). Ini mengesahkan
  dan menajamkan §2g.
- **"SE terlalu kecil 5.5–8.4×"** — dikecilkan. Benar bagi `d_tb` pattern tertentu (`A1`: 0.236 → 1.743 = 7.4×)
  tetapi bagi lift R2 `S3` ia hanya 1.9× (tarikh → tahun) dan 1.32× (bulan → tahun). Magnitudnya
  bergantung pattern dan sasaran, bukan universal.
- **"Pepijat `erfc` dalam nilai p"** — tidak terpakai. `ukur.beza_kelompok` dan `ukur.p2sisi` ialah **kod mati**
  (tiada pemanggil); setiap nombor yang dilaporkan guna `scipy.stats.t`. Formula sandwich kelompok-teguh dan
  Cameron-Gelbach-Miller kedua-duanya **disahkan BETUL** oleh audit, begitu juga `bh_fdr` dalam
  `REVERSE/teras/stat.py`.

### 8f. Jurang yang audit namakan dan MOMENTUM_PEGANG TIDAK tutup

| Keutamaan | Jurang | Ujian yang akan menyelesaikannya |
|---|---|---|
| Tinggi | **Gate mengukur DESIL (10% alam) tetapi 8 slot membeli puncak skor** (~0.3% ekstrem), dan §2f menunjukkan ekstrem itulah tempat urutan KALAH | Ukur semula kelima-lima calon pada "N teratas setiap tarikh" bagi N = 8, 10, 20, 40, bukan pada desil |
| Tinggi | **TB bukan ekor.** Kadar asas 31–34% = median-atas, bukan ekor; duit ada dalam peristiwa ~1.3%. Peringkat pattern pada dua sasaran berbeza sampai 4× | Jalankan semula 86 topeng dengan sasaran `r2 ≥ +100%` dan keahlian 1% teratas; bandingkan rho Spearman |
| Tinggi | **74.3% keuntungan datang daripada saham DI LUAR alam dagangan Syariah**, dan repo tiada keahlian SPUS titik-masa | Jalankan semula gate pada A02 ∩ SPUS dan lapor kedua-dua set bersebelahan |
| Tinggi | `r2_potong5` sepatutnya menjadi **gate**: 4 daripada 5 pemenang lebih buruk daripada asas | Tambah gate `r2_potong5 ≥ asas` (jangkaan: hanya `H2` bertahan, margin 0.018 mata) |
| Tinggi | **Paksi KELUAR tidak disapu bersama pattern** walaupun §8d menunjukkan ia lebih berpengaruh | Grid 86 topeng × ganda {2,3,4,6} × satu keluar bukan-ekor, FDR atas keseluruhan grid |
| Sederhana | Label TB (120 bar) dan hasil R2 (tempoh pegangan sebenar) atas **tingkap berbeza**; 73% keuntungan datang daripada 3.93% dagangan yang keluar **selepas** tingkap label | Had tempoh pegangan pada 120 bar, atau takrif TB atas tingkap pegangan sebenar |
| Sederhana | **Lantai hingar topeng rawak tidak diukur pada P2.** Pada P1 dengan topeng blok-tarikh (lift benar = 0): `d_r2` sd 3.963 mata, p95 \|lift\| 7.232 — margin pemenang 0.43–1.29 mata berada **di bawah** lantai itu. (Bootstrap P2 saya memberi sd 0.61 bagi `S3`, jadi lantai P2 jauh lebih rendah — tetapi ujian null blok-tarikh pada P2 belum dijalankan) | 86 topeng NULL blok-tarikh dipadankan n dan kepersisten; ambang gate pada persentil 95 |

### 8g. Had audit

Satu kelemahan reka bentuk yang audit kenal pasti dan **tidak** diperbaiki: tingkap LATIH dan TAHAN memisahkan
tarikh **MASUK** tetapi bukan tarikh **HASIL**, jadi dagangan yang masuk Dis 2019 menyelesaikan dirinya dalam
2020. Tindihan maksimum ialah 120 bar + tempoh pegangan, jadi kedua-dua tingkap **bukan** dua replikasi bebas.
