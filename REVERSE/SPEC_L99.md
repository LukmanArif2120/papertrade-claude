# SPEC L99 — Pradaftar: pattern MASUK yang memaksimumkan tangkapan bawah lorong 2

Ditulis 1 Nov 2026, **sebelum** apa-apa keputusan L99 dilihat. Permintaan pengguna: "saham yang boleh pegang 3 hari
dan ke atas, atau pegang selagi naik; pattern saham macam mana yang memaksimumkan keuntungan; high momentum stocks
pattern". Empat keputusan pengguna dalam sesi ini: sasaran = **peluang jadi trend besar**; keluar = **lorong 2 sahaja**;
alam = **763k dagangan enjin + A02**; keluaran = **pradaftar + laporan dalam repo**.

## 1. Mengapa soalan ini BUKAN ulangan ruang yang sudah ditutup

`SETUP.md` (0/598 penapis lift positif), `NXX.md` (gate3 0/280) dan `SILANG.md` mengukur **lift pada PURATA pulangan**.
L99 mengukur **fungsi berbeza**: `P(dagangan menjadi ekor kanan)`. `KOLAM_EKOR.md` ukur 5% teratas = 63.7% jumlah
pulangan, dan `SETUP.md` menjelaskan mengapa penapis gagal — ia membuang bar pada ekor. Jika itu mekanismenya, maka
pemboleh ubah sasaran yang betul ialah **keahlian ekor**, bukan min. Hubungan antara kedua-duanya tidak tertutup oleh
mana-mana ujian terdahulu: satu pattern boleh menaikkan `P(ekor)` dan tetap menurunkan min (lebih banyak kalah kecil),
atau sebaliknya. Ini paksi sasaran, bukan paksi signal.

Kedua: lorong 2 **imun** kepada kecacatan henti hari-0 (`KOLAM_EKOR.md` §4a) kerana ia tidak memakai henti kaedah dan
parasnya pada hari masuk ialah `tutup[k] − 4×ATR < tutup[k]`, jadi tidak boleh tercetus hari masuk. Setiap nombor
dalam kajian Mxx tercemar oleh kecacatan itu; L99 tidak.

## 2. Takrif sasaran (dibekukan)

Masuk: isyarat pada tutup bar `t` → beli pada **buka bar t+1** (= paksi `C01`, sama seperti seluruh repo).

- **TB (utama)** = `1` jika `max(tutup[k .. k+119]) / buka[k] − 1 >= 0.30`, di mana `k` = bar masuk.
  Takrif ini **sama tepat** dengan `kajian/lorong2/kaji_lorong2.py` (`mx120`, `besar = mx120 >= 0.30`) supaya L99
  boleh dibanding terus dengan `KAJIAN_LORONG2.md`. Guna **tutup tertinggi**, bukan tinggi tertinggi.
- **R2 (sekunder)** = pulangan lorong 2 terealisasi: Chandelier tutup, paras keluar = `max(tutup sejak masuk) − 4×ATR14`,
  paras hanya naik, tiada henti kaedah, `tutup < paras` → jual pada **buka esok**; posisi belum keluar pada bar akhir
  data ditutup pada tutup akhir dan ditanda terpotong. Kos 0.1% setiap belah (sama seperti `kaji_lorong2.py`).
- **TANGKAP** = purata `R2` bagi dagangan yang `TB = 1`. Ini nombor yang paling dekat dengan soalan pengguna:
  antara saham yang MEMANG bergerak, berapa banyak yang lorong 2 tangkap.
- **SEBULAN** = `purata R2 ÷ purata hari × 21`.

## 3. Populasi

| ID | Alam | Tingkap | Peranan |
|---|---|---|---|
| P1 | 763k dagangan enjin v1.2, 134 kaedah, set 431 (`data_mentah`) | masuk 1 Nov 2019 – 2 Okt 2026 | Semakan pemalsuan + pattern dalam konteks isyarat kaedah |
| P2L | A02, setiap bar cair, kumpulan AB | 2009-11 – 2019-12 (**LATIH**) | Jana/ukur |
| P2T | A02, setiap bar cair, kumpulan AB | 2020-01 – 2026-10 (**TAHAN**) | Pengesahan luar sampel |
| P3 | Papertrade C 8,748 posisi + Lejar Penuh 16,629 | 8 Okt – 30 Okt 2026 | **Deskriptif sahaja** — lihat §7 |

Tapisan cair P2 (sama seperti `SETUP.md`): median nilai dagang 20 bar ≥ USD100 ribu, tutup ≥ USD5, bar ≥ 260.

## 4. Semakan pemalsuan WAJIB (gate sifar untuk seluruh kajian)

Sebelum apa-apa pattern dilaporkan, simulator lorong 2 saya mesti menghasilkan semula nombor terbitan
`KAJIAN_LORONG2.md` pada P1, dalam toleransi 0.2 mata peratus / 0.5 hari:

| Ukuran | Sasaran terbitan |
|---|---|
| Lorong 2 purata | 5.1% |
| Lorong 2 median | −2.8% |
| Lorong 2 5% terburuk | −18.2% |
| Lorong 2 hari | 43.8 |
| Lorong 2 sebulan | 2.4% |
| **Lorong 2 TANGKAP (trend besar)** | **25.1%** |
| Lorong 1 purata / hari / TANGKAP | 2.7% / 22.7 / 12.0% |
| Kadar TB pada P1 | 33% |
| Hari pegangan p25/50/75 | 20 / 34 / 58 |
| Hari pegangan trend besar p25/50/75 | 31 / 54 / 85 |

Gagal → kajian berhenti dan pepijat dibetulkan dahulu. **Tiada nombor pattern dilaporkan sebelum jadual ini lulus.**

## 5. Kelas pepijat yang mesti diuji asap (daripada lima pepijat 31 Okt 2026)

1. **Harga keluar merentas ticker** — `o[kk+1]` diindeks pada tatasusunan ticker salah. Ujian: tiada `R2` di luar
   [−100%, +500%]; harga keluar mesti dalam julat [min low, max high] ticker itu dalam tempoh pegangan.
2. **Keluar degenerat hari masuk** — Ujian: `hari_pegang >= 1` bagi 100% dagangan, dan kadar keluar hari-0 = 0%.
3. **Paras henti di atas harga masuk** — Ujian: paras Chandelier pada hari masuk mesti `< buka masuk` bagi 100% baris.
4. **Penapis dipakai sebelum topeng** — setiap feature dikira daripada data hingga tutup `t` sahaja; dijalankan
   melalui `REVERSE/semak_hadapan.py` bagi SEMUA feature baharu. Lag eksplisit: keputusan guna baris `t`, hasil guna `t+1`.
5. **Ujian asap mesti pada KOMBINASI** (pattern × lorong 2), bukan komponen — kerana `X25` lulus semua gate sebagai
   komponen yang kelihatan waras.
6. **OOM** — P2 diproses ticker demi ticker; tiada tatasusunan penuh `anchor × 120` dibina.

## 6. Pattern yang diuji (dibekukan sebelum keputusan)

Setiap pattern = topeng pada bar `t`. Dua jenis operasi diuji berasingan kerana `SETUP.md` dan `GABUNGAN.md` mengukur
bahawa jenis operasi itulah yang menentukan, bukan signal:

**(a) PENAPIS (`DAN`)** — 24 topeng, dijangka gagal secara struktur tetapi diperlukan sebagai asas banding:
A1 `roc60` desil teratas (silang-keratan setiap tarikh) · A2 `rs_spy_6b>0 & rs_spy_12b>0` · A3 `roc20` desil teratas ·
B1 `j_52w_tinggi >= −5` · B2 `lapis` (susunan MA 50>150>200 + harga atas) · B3 `breakout_52w` · B4 `j_ma50>=0 & cerun_ma50>0` ·
C1 `atr_pct` tertile teratas · C2 `atr_pct` tertile terbawah · D1 `vol_n50>=1.5` · D2 `pocket_pivot` ·
E1 `vcp` · E2 `bb_squeeze` · E3 `nr7` · E4 `julat10` tertile terbawah · F1 `gap_and_go` · F2 `donchian20` ·
F3 `adx14>=25 & pdi>mdi` · G1 `sektor_atas_ma50` · G2 rejim SPY atas MA50 dan MA200 ·
H1 Qullamaggie anggaran (`roc60` desil teratas & `atr_pct>=3` & `j_52w_tinggi>=−25` & nilai dagang >= $10j) ·
H2 Minervini anggaran (`lapis` & `j_52w_tinggi>=−25` & `j_52w_rendah>=30` & `roc60` kuartil teratas) ·
H3 `ad_tinggi_baru` · H4 `garis_rs_tinggi`

**(b) KESATUAN (`ATAU`)** — 4 topeng, kerana `GABUNGAN.md` ialah satu-satunya dapatan yang pernah lulus keempat gate
dan mekanismenya ialah kesatuan MENAMBAH bar: U_A `A1 ∪ B1 ∪ F1` · U_B `A1 ∪ E1 ∪ D2` · U_C `B2 ∪ B3 ∪ F3` ·
U_D keempat keluarga `A1 ∪ B1 ∪ E1 ∪ D2`

**(c) URUTAN (skor berterusan)** — 6 skor, kerana `SISTEM.md` ukur urutan skor berterusan ada sebaran benih 0.00 mata
lawan 17.3 mata/tahun hingar pemilihan: S1 `roc60` · S2 `roc60/atr_pct` (Clenow-ish) · S3 `rs_spy_6b` ·
S4 `−j_52w_tinggi` · S5 `adx14` · S6 skor gabungan pangkat S1–S4. Diukur sebagai `P(TB)` dan `R2` setiap desil,
**tiada bar dibuang**.

Bilangan ujian untuk FDR: 24 penapis + 4 kesatuan + 6 urutan × 10 desil = **88 ujian setiap sasaran**, dan
dua sasaran berasingan (`TB`, `R2`) = **176**. BH-FDR dikira atas 176.

## 7. Had P3 (data forward) — ditulis sebelum ia digunakan

Papertrade C/Lejar **tidak boleh** menjawab soalan TB dan tidak akan digunakan untuk itu:
- Tingkap 8–30 Okt 2026 = maksimum 15 hari dagangan. `TB` memerlukan ufuk 120 hari. Mustahil.
- Lorong 2 yang sudah keluar dalam tingkap itu ialah **sampel terpilih yang rosak**: Chandelier hanya tercetus
  selepas jatuh 4×ATR dari puncak, jadi dalam 3 minggu hanya **yang gagal cepat** yang keluar (296 keluar, purata
  −13.97%, menang 2.0%), manakala 8,452 masih terbuka pada purata +1.50%. Mengira prestasi lorong 2 daripada 296
  baris itu ialah kesilapan bentuk yang sama seperti melaporkan kaedah pegang-panjang daripada posisi yang
  dihentikan awal (`KAEDAH_TERBAIK.md` §3).
- Peranan P3 dalam L99: **(i)** senarai dua lorong seperti yang pengguna minta, dengan had dinyatakan; **(ii)** taburan
  feature pada isyarat sebenar (RS, gred sektor/industri, pemangkin, ATR%) supaya pattern yang menang dalam P2 boleh
  diterjemah kepada skrin yang benar-benar boleh dijalankan; **(iii)** semakan kewarasan arah, bukan bukti.

## 8. Gate (dibekukan)

- **Gate 0** `n >= 2,000` sauh dalam SETIAP tingkap (P2L dan P2T).
- **Gate 1** `ΔP(TB) > 0` pada KEDUA-DUA tingkap, **dan** lift `R2` > 0 pada kedua-dua tingkap.
- **Gate 2** BH-FDR `q <= 0.05` atas 176 ujian, pada tingkap TAHAN, dengan `p` daripada SE **berkelompok ikut tarikh
  masuk** (sauh pada tarikh sama berkorelasi; SE tidak berkelompok akan terlalu kecil).
- **Gate 3** `R2` mutlak bagi pattern `> 0` **dan** `> R2` asas. Syarat ini ditambah kerana `N16×X1` lulus gate1+gate2
  dengan lift +0.193 dan menang 62.4% tetapi jangkaan mutlak −0.088% = merugikan (`NXX.md`).
- **Gate 4** `TANGKAP` pattern `>=` `TANGKAP` asas pada tingkap TAHAN. Pattern yang menaikkan `P(TB)` tetapi
  menurunkan tangkapan tidak berguna.
- **Diagnostik (BUKAN gate, dilapor tanpa dakwaan):** `R2` selepas buang 5% teratas; MDD dan CAGR portfolio 8 dan 40
  slot lawan **SPUS** (`PENANDA_ARAS_SYARIAH.md`: 17.95%/tahun, MDD −26.82% bagi 2020–2025 CAGR seluruh tingkap);
  sebaran benih merentas 20 benih; hari pegangan.

## 9. Jangkaan priori saya (direkod supaya boleh disalahkan)

Jangkaan priori saya **salah pada 2 daripada 3 gate dalam tiga pradaftar berturut-turut** (SPEC_SILANG §7,
SPEC_SISTEM §7, SPEC_NXX). Corak kesilapan: saya memandang **rendah** struktur statistik dalam ruang belum diukur
dan memandang **tinggi** keupayaannya bertahan syarat ekor. Maka:

1. **Gate 1 akan dilepasi oleh BANYAK pattern** (tekaan: 10–20 daripada 88). `P(TB)` ialah pemboleh ubah yang jauh
   lebih kasar daripada min pulangan, dan momentum-meramal-momentum ialah kesan yang paling banyak direplikasi
   dalam kesusasteraan akademik. Saya menjangka `roc60` desil teratas (A1) dan `j_52w_tinggi >= −5` (B1) akan
   menggandakan `P(TB)`.
2. **Gate 3 ialah pengikat sebenar.** Tekaan: ≤ 5 daripada 88 lulus. Mekanismenya: pattern momentum menaikkan
   `P(TB)` DAN menaikkan `P(kerugian besar)` serentak, kerana kedua-duanya kesan volatiliti.
3. **Urutan (c) akan mengalahkan penapis (a)** pada setiap ukuran, dan kesatuan (b) akan berada di antara keduanya.
4. **Tiada pattern akan memberi portfolio yang mengalahkan SPUS pada KEDUA-DUA pulangan dan MDD.** Saya menjangka
   diagnostik portfolio gagal walaupun gate 1–4 lulus, kerana `PEMBINAAN.md` dan `SISTEM.md` kedua-duanya mendarat
   di bawah garis SPUS+tunai dan nisbah `CAGR÷|MDD|` campuran hampir pemalar 0.642–0.669.
5. Nombor tunggal yang paling berguna daripada L99 dijangka ialah **TANGKAP**, bukan pattern: 25.1% lawan 12.0%
   bermakna pilihan keluar sudah menggandakan tangkapan pada dagangan yang penting, dan itu diperoleh **tanpa**
   apa-apa pattern masuk.

## 10. Had yang diketahui (ditulis awal)

- **A02 tiada saham delist** = bias penyintas, dan ia menyebelahi pegangan panjang secara khusus. Setiap nombor P2
  ialah had ATAS.
- **P1 set 431** dipilih daripada data sama = keputusan dalam sampel; ia semakan pemalsuan, bukan pengesahan.
- Peta sektor bukan titik-masa (petikan 2026).
- Paksi CARA kekal `C01`; paksi SAIZ dan IMBANG tidak diuji di sini.
- A02 berakhir 16 Okt 2026, jadi sauh selepas ~April 2026 ada ufuk TB terpotong; sauh dengan ufuk < 120 bar
  **dibuang** daripada pengiraan `TB` (dan bilangannya dilapor).
