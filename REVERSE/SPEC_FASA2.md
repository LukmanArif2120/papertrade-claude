# SPEC FASA 2 — data titik-masa (RS, gred kumpulan, earnings)

Dikunci **28 Okt 2026**, **sebelum datanya cukup untuk diuji**. Itu tujuannya: ujian dipradaftar
ketika hasilnya masih tidak diketahui, supaya ia tidak boleh dilenturkan kemudian.

Fasa 1 (`SPEC.md`, `KEPUTUSAN_FASA1.md`) dan 1b (`SPEC_1B.md`, `KEPUTUSAN_1B.md`) ditutup dan
tidak disentuh.

## 1. Satu hipotesis

Fasa 1 menguji 77 lajur indikator **harga** merentas enam tahun dan menolaknya. `DIAGNOSIS_FASA1.md`
menunjukkan mengapa: korelasi pangkat indikator harga terhadap **pulangan yang boleh didagangkan**
≈ 0 (1/30 konsisten, −0.027), walaupun terhadap puncak run bersyarat-hindsight ia sampai 0.124.

Hipotesis fasa 2, satu sahaja: **data titik-masa yang dikeluarkan daripada fasa 1 membawa kuasa
pemangkatan yang indikator harga tidak ada.**

## 2. Lajur yang diuji (dikunci; tiada tambahan separuh jalan)

| Kumpulan | Sumber | Liputan data (bukan tarikh mula ambil) |
|---|---|---|
| RS rating lawan seluruh pasaran AS | `BacktestShariah2/data/rs/rs_pasaran.csv` | sejak 2026-09-15 (terkumpul harian) |
| Gred sektor dan industri v2 | `BacktestShariah2/data/kumpulan/gred_kumpulan_sejarah.csv` | sejak 2026-09-25 (terkumpul harian) |
| EPS/hasil suku point-in-time, SUE, pecutan hasil | `BacktestShariah2/data/sec/eps_hasil.csv`, `sue.csv` | **sejak 2009** (`tarikh_fail`; lihat §4.1) |
| Tarikh earnings 8-K Item 2.02 (jarak ke earnings, ±5 hari) | `BacktestShariah2/data/sec/earnings_8k.csv` | **sejak 2004** (`tarikh_fail`; lihat §4.1) |

Tetapan standard sahaja. **Tiada penalaan parameter. Tiada Optuna.** Indikator berterusan diuji
pada dua hujung kuintil, atas populasi kuintil yang dibekukan pada larian pertama, seperti fasa 1.

## 3. Sasaran — pembetulan penting daripada fasa 1

Sasaran utama ialah **pulangan yang boleh didagangkan**: masuk buka esok, kos penuh (SPEC §3.1),
henti dan exit dinyatakan, ufuk dinyatakan. **Bukan** puncak run.

Fasa 1 mengukur lift terhadap hasil run yang bersyarat pada hindsight (hanya 15–18% peristiwa
menjadi run), dan itu menghasilkan lift 10–24 kali yang hilang sepenuhnya dalam dagangan. Fasa 2
tidak mengulangi kesilapan itu: setiap keputusan dibuat atas pulangan selepas kos.

## 4. Ambang data minimum sebelum penilaian PERTAMA (dikunci)

Penilaian **tidak boleh** dijalankan sebelum **kesemua** dipenuhi:

- **≥ 250 hari dagangan** liputan bertindih antara lajur yang diuji dan populasi peristiwa sah ~~dan Lejar Penuh~~ (**dibetulkan §9.1**)
- **≥ 3,000 peristiwa sah** dengan nilai lajur itu tidak kosong
- **≥ 2 suku kalendar penuh** data

Pada 28 Okt 2026: RS ≈ 30 hari dagangan, gred ≈ 23. **Belum cukup.** Anggaran penilaian pertama
bagi kedua-dua lajur itu: sekitar **Okt 2027**.

### 4.1 Pembetulan 28 Okt 2026 — leg SEC TIDAK perlu menunggu

Versi asal spec ini menulis "SEC ≈ 1 hari" dan meletakkan leg SEC dalam kumpulan yang menunggu
Okt 2027. **Itu salah.** Lajur "2026-10-27" dalam §2 ialah tarikh kita **mula mengambil** data, bukan
tarikh liputannya. SEC XBRL `companyfacts` menyimpan **nilai pertama difail**, dan
`standard/fundamental_sec.py` memang mengambil nilai pertama itu (pernyataan semula diabaikan,
lihat komen kepala skrip). Maka data itu **titik-masa secara retrospektif**:

| Fail | Medan masa | Liputan (petikan 28 Okt 2026) | Baris |
|---|---|---|---|
| `data/sec/eps_hasil.csv` | `tarikh_fail` | 2009-04-30 → 2026-10-28 | 80,575 |
| `data/sec/sue.csv` | `tarikh_umum` | 2007-10-25 → 2026-10-28 | 41,179 |
| `data/sec/earnings_8k.csv` | `tarikh_fail` | 2004-08-23 → 2026-10-28 | 54,109 |

Perbezaannya dengan RS/gred: RS dan gred **dikira** oleh kita setiap hari dan tidak boleh dibina
semula ke belakang (input harian tidak disimpan); SEC **diterbitkan** dengan cap masa pemfailan,
jadi sejarahnya memang ada.

Maka leg SEC fasa 2 (SUE, pecutan hasil, jarak ke earnings) boleh dinilai atas 2009–2026 sebaik
liputan ticker cukup, **tanpa menunggu**. Ia juga leg yang paling tidak bertindih dengan fasa 1:
SUE dan pecutan hasil bukan indikator harga, jadi ia bukan ruang yang sudah diukur dan kosong.

**Halangan yang tinggal ialah liputan ticker, bukan masa.** Pada 28 Okt 2026 liputan = 777 ticker
daripada universe `tawaran_edgar.universe()` (911), sedangkan universe REVERSE ≈ 2,300 setahun.
Keputusan pengguna 28 Okt 2026: lebarkan ke **3,260 ticker Release `autotune-data-a02`**
(`BacktestShariah2/data/univ_sec.txt`; kesatuan dengan universe lama = 3,335). Isian awal melalui
`fundamental_sec.yml` (`--maks-fakta`, `--maks-saham`); SEC had 10 permintaan/saat, jeda 0.15s.

Ambang §4 kekal terpakai kepada leg SEC seperti juga RS/gred: ≥ 3,000 peristiwa sah dengan nilai
lajur tidak kosong, dan ≥ 250 hari dagangan bertindih. Bezanya, bagi SEC ambang itu dipenuhi oleh
sejarah, bukan oleh menunggu. Penilaian leg SEC dijalankan **berasingan** daripada leg RS/gred,
dan keluarga FDR-nya dikira berasingan (tiada penggabungan kiraan ujian antara dua leg).

### 4.2 Masa ketersediaan data SEC (dikunci 28 Okt 2026, sebelum sebarang keputusan dilihat)

Data SEC titik-masa pada peringkat **nilai** (§4.1), tetapi itu belum cukup: cap masa pemfailan
mesti ditukar kepada **sesi dagangan** yang betul. Petikan 28 Okt 2026, `data/sec/earnings_8k.csv`
(54,109 baris, `masa_terima` penuh, tiada yang kosong), ditukar ke waktu New York:

| Waktu pemfailan (ET) | Baris | % |
|---|---|---|
| Selepas tutup (≥ 16:00) | 28,161 | **52.0** |
| Pra-buka (< 09:30) | 19,217 | 35.5 |
| Intraday (09:30–15:59) | 6,731 | 12.4 |

Dan 5.2% baris mempunyai `tarikh_fail` **berbeza** daripada tarikh ET `masa_terima`.

Maka menggunakan `tarikh_fail` sebagai tarikh ketersediaan akan memberi **lebih separuh** peristiwa
maklumat kira-kira satu sesi dagangan lebih awal — tepat jenis kelebihan palsu yang fasa 1 dibina
untuk mengelak, dan ia akan muncul sebagai "penemuan" yang hilang sepenuhnya dalam dagangan.

**Peraturan dikunci.** Hari sesuatu nilai SEC boleh digunakan = **sesi dagangan pertama yang
pembukaannya (09:30 ET) jatuh selepas cap masa pemfailan**. Satu peraturan, tiga kes:

| Difail | Tersedia |
|---|---|
| 06:00 ET Selasa | buka Selasa |
| 11:00 ET Selasa | buka Rabu |
| 20:00 ET Selasa | buka Rabu |
| 20:00 ET Jumaat | buka Isnin |

Butiran yang juga dikunci:

- Zon waktu dikira dengan `America/New_York` (`zoneinfo`), **bukan offset tetap**: data merangkumi
  2004–2026, termasuk peraturan waktu musim panas sebelum dan selepas perubahan 2007.
- Kalendar sesi = **tarikh dalam stor harga**, bukan kalendar kalendar: cuti pasaran dilangkau.
- Tepat 09:30 ET dikira **sudah lepas** (sesi berikut), kerana harga buka itu sendiri tidak boleh
  didagangkan atas maklumat yang tiba pada saat yang sama.
- `sue.csv` dengan `sumber_tarikh == 'fail'` (1,914 baris; tiada 8-K Item 2.02 dijumpai, jadi hanya
  tarikh pemfailan 10-Q/10-K diketahui): waktu tidak diketahui, maka **dianggap selepas tutup** pada
  tarikh itu. Pilihan konservatif; ia tidak boleh mencipta kelebihan.
- Nilai `eps_hasil.csv` menggunakan `tarikh_fail` 10-Q/10-K melalui peraturan yang sama.

Pelaksanaan: `REVERSE/teras/sec.py` `hari_tersedia()`; ujian
`BacktestShariah2/ujian/test_reverse_sec.py` (14 ujian, termasuk sempadan waktu musim panas,
peraturan pra-2007, cuti, dan sifat "hari tersedia tidak pernah mendahului tarikh pemfailan" atas
data sebenar). Penilaian leg SEC **tidak boleh** menggunakan `tarikh_fail` secara terus.


### 4.3 "Jarak ke earnings" (dikunci 28 Okt 2026, sebelum sebarang keputusan dilihat)

§2 menulis lajur "Tarikh earnings 8-K Item 2.02 (jarak ke earnings, ±5 hari)" tanpa menyatakan
arah. Keadaan itu tidak boleh dibiar: `data/sec/earnings_8k.csv` hanya mengandungi pemfailan yang
**sudah berlaku**, jadi "jarak ke pengumuman berikut" yang diambil daripada tarikh 8-K berikut
bermakna mengetahui tarikh pemfailan masa hadapan. Itu lookahead, dan ia akan kelihatan sebagai
kesan yang kuat sekitar earnings.

**Peraturan dikunci — dua lajur, bukan satu:**

- `hari_sejak_earnings` — hari dari pengumuman terakhir yang **sudah tersedia** (§4.2) ke hari
  peristiwa. Tepat dan ke belakang sepenuhnya. Ini juga pemboleh ubah yang betul untuk PEAD, kerana
  PEAD ialah drift **selepas** pengumuman.
- `hari_ke_earnings_jangka` — **jangkaan**, dikira daripada median selang pengumuman yang sudah
  tersedia pada masa itu (median bergulir yang hanya melihat ke belakang; selang > 120 hari tidak
  dipercayai dan memberi kosong). Ia menganggarkan apa yang pelabur pada hari itu boleh jangka,
  bukan apa yang sebenarnya berlaku.

**Tarikh pemfailan 8-K yang sebenarnya berikut TIDAK boleh digunakan, dalam apa-apa bentuk.**

Pelaksanaan: `REVERSE/step10_sec.py`. Jangkaan dikira pada jadual SEC (bukan pada jadual peristiwa)
supaya ia mengalir melalui `merge_asof(direction='backward')` dan tidak boleh tersilap mengambil
baris masa hadapan. Ujian `BacktestShariah2/ujian/test_reverse_step10.py` mengunci sifat ini secara
struktur: jangkaan bagi k pengumuman pertama mesti **sama** sama ada baris kemudian ada atau tidak
(`test_hirisan_tidak_berubah_oleh_masa_hadapan`), dan kod tidak boleh mengandungi merge arah
`forward` atau `nearest`.

### 4.4 Status gerbang ambang §4 (28 Okt 2026, kiraan sahaja)

`REVERSE/step10_sec.py` dijalankan atas cache peristiwa sah yang ada (2020–2025). **Kiraan liputan
sahaja; tiada statistik hasil dikira atau dilihat pada peringkat ini.**

| Tahun | Peristiwa sah | Saham | Saham ada SEC | SUE tidak kosong | % |
|---|---|---|---|---|---|
| 2020 | 12,858 | 2,045 | 525 | 3,517 | 27.4 |
| 2021 | 15,259 | 2,283 | 567 | 4,157 | 27.2 |
| 2022 | 15,440 | 2,255 | 572 | 4,221 | 27.3 |
| 2023 | 13,642 | 2,202 | 598 | 3,991 | 29.3 |
| 2024 | 14,151 | 2,191 | 605 | 4,186 | 29.6 |
| 2025 | 13,998 | 2,237 | 615 | 3,996 | 28.5 |

Ambang **≥ 3,000 peristiwa sah dengan lajur tidak kosong: LULUS setiap tahun**, walaupun dengan
liputan 777 ticker yang lama. Ambang ≥ 250 hari dagangan dan ≥ 2 suku: lulus (§4.1).

Tetapi **gerbang ini belum boleh dianggap memuaskan**, dan penilaian §5 belum dijalankan, kerana
dua sebab:

1. **Kecenderungan pemilihan.** Hanya 525–615 daripada ~2,200 saham (≈ 27%) ada data SEC, dan
   universe lama ialah watchlist + posisi C — iaitu nama yang lebih besar dan lebih cair. Sampel itu
   bukan keratan-rentas universe REVERSE. Isian awal 3,335 ticker membetulkannya; itulah sebab
   sebenar melebarkan universe, bukan bilangan baris.
2. **Sejarah masih 6 tahun, bukan 14.** Cache peristiwa sah hanya ada untuk 2020–2025. Liputan SUE
   yang boleh diguna bermula 2012 (§4.1), jadi `step1_run.py` perlu dijalankan untuk 2012–2019
   sebelum kelebihan sejarah panjang itu benar-benar diperoleh.

Penilaian §5 dijalankan selepas (1) dan (2) selesai, atas populasi penuh, sekali sahaja.


## 5. Ujian (dipradaftar)

1. **Pemangkatan** — Spearman antara setiap lajur dan pulangan boleh didagangkan, dikira
   **setiap suku**. Lajur diteruskan hanya jika tandanya konsisten dalam **≥ 4 daripada 6** suku
   pertama dan |rho| purata ≥ 0.05.
2. **Kehadiran** — metrik Step 4 fasa 1 (K_padu, lift, presisi, lift_presisi) atas populasi
   keputusan, dengan KAWALAN RAWAK yang sama.
3. **Kawalan kebetulan** — label rawak 1000×, bootstrap blok 1000× (blok ticker **dan** blok
   minggu), BH-FDR q ≤ 0.01 dalam keluarga **`FASA2`** sendiri. Tolak jika had bawah 95% jangkaan
   ≤ 0 dalam mana-mana skema blok, atau jika jangkaan ≤ 0 tanpa 5% pemenang teratas.
4. **Portfolio** — **8 slot × 12.5%** seperti REVERSE Step 9 ~~10 slot (selari `portfolio_slot/`)~~
   (**dibetulkan §9.1**), kos penuh, dua saiz: tetap 12.5% dan berskala risiko (SPEC_1B, k = 4,
   risiko 1.0%).

## 6. Ambang penerimaan (dikunci sekarang, tidak boleh diubah selepas melihat hasil)

Fasa 2 diterima sebagai penemuan hanya jika lajur yang sama:

1. lulus §5.1 **dan** §5.3; **dan**
2. mengalahkan **asas harga-sahaja** (fungsi pangkat indikator harga terbaik fasa 1, yang
   |rho|-nya ≈ 0) pada pulangan boleh didagangkan; **dan**
3. mengalahkan **KAWALAN RAWAK** dalam portfolio §5.4 pada pulangan **dan** MDD.

Jika tidak: fasa 2 **DITOLAK** dan dilaporkan sebagai ditolak, sama seperti fasa 1 dan 1b.

## 7. Had yang diakui lebih awal

- Tempoh ujian bermula 2026 — **satu rejim pasaran sahaja**. Keputusan tertinggi fasa 2 ialah
  **CALON** sehingga dua tempoh bebas disahkan.
- Lejar Penuh **tiada bias survivorship** (ia jejak hadapan sebenar) — ini **lebih baik** daripada
  data A02 fasa 1, dan satu sebab fasa 2 berbaloi walaupun fasa 1 ditolak.
- Saiz sampel akan kecil pada mulanya; §4 ada untuk mengelak kesimpulan awal.

## 8. Apa yang fasa 2 BUKAN

Bukan percubaan kedua pada indikator harga. Jika seseorang mahu menguji indikator harga lagi,
`KEPUTUSAN_FASA1.md` dan `DIAGNOSIS_FASA1.md` ialah jawapannya: enam tahun, empat rejim,
20,640 ujian ENTRY, 108 ujian 1b — ruang itu kosong.


---

## 9. Pindaan bertarikh

### 9.1 — 28 Okt 2026: populasi peristiwa dan saiz portfolio dibetulkan (bukan Lejar, bukan 10 slot)

**Kesilapan penulis spec, ditemui oleh pengguna.** Draf pertama SPEC_FASA2 menetapkan populasi
ujian sebagai **Lejar Penuh** (§4) dan portfolio **10 slot selari `portfolio_slot/`** (§5.4).
Kedua-duanya salah: Lejar Penuh dan `portfolio_slot/` ialah rekod isyarat **134 kaedah Mxx**.

Arahan asal kajian ini menyatakannya tanpa kekaburan:

> *"Kajian ini menguji signal dan indikator sahaja — BUKAN kaedah Mxx dalam repo, dan BUKAN
> penalaan parameter."*

Menguji RS/gred/earnings atas belian Mxx menjawab soalan yang **berbeza** — sama ada data itu
menambah kuasa pemangkatan **dalam kalangan isyarat kaedah Mxx** — bukan soalan kajian ini, iaitu
sama ada data itu menambah kuasa yang indikator harga tidak ada, atas populasi peristiwa yang sama
seperti fasa 1.

**Dibetulkan:**

| Perkara | Draf pertama (salah) | Dikunci sekarang |
|---|---|---|
| Populasi ujian | belian Lejar Penuh (isyarat Mxx) | **peristiwa sah `SPEC.md` §7**: tutup ≥ 5% di atas rendah terendah 20 hari DAN tutup > EMA21, hari pertama dalam ≤ 10 hari dagangan — kausal, bebas kaedah |
| Portfolio §5.4 | 10 slot × 10% (`portfolio_slot/`) | **8 slot × 12.5%** seperti REVERSE Step 9, supaya setanding fasa 1 |
| Universe | tidak dinyatakan | universe A02 titik-masa, sama seperti fasa 1 |
| Kawalan | tidak dinyatakan | KAWALAN RAWAK dan asas harga-sahaja, sama seperti fasa 1 |

**Mengapa pembetulan ini sah:** pada tarikh ini fasa 2 berada pada **30 / 250** hari dagangan —
**tiada data dinilai, tiada hasil dilihat**. Itulah satu-satunya keadaan di mana spec yang dikunci
boleh dibetulkan tanpa menjejaskan integriti pradaftar. Draf pertama dikekalkan dalam sejarah git.

**Tiada infrastruktur baharu diperlukan.** Peristiwa sah ialah fungsi deterministik stor harga
(`BacktestShariah2/data/harga/stor/`), yang dipelihara setiap hari, dan RS/gred/SEC direkod setiap
hari. Maka join peristiwa × data titik-masa boleh dibuat **secara retrospektif** pada Okt 2027
dengan menjalankan semula pengesan peristiwa REVERSE atas stor. Yang perlu ditunggu ialah **masa**,
bukan kod.

### 9.2 — 28 Okt 2026: lorong `RISIKO_10` bukan ujian ke hadapan fasa 1b

Lorong `RISIKO_10` yang ditambah ke `standard/portfolio_slot.py` pada 28 Okt 2026 pada mulanya
diterangkan sebagai "ujian ke hadapan bagi dapatan fasa 1b". **Itu terlebih-dakwa.**
`portfolio_slot/` membeli daripada Lejar Penuh, iaitu isyarat **kaedah Mxx** — populasi kemasukan
yang sama sekali berbeza daripada signal REVERSE yang menghasilkan dapatan 1b.

Apa yang `RISIKO_10` sebenarnya uji: sama ada saiz berskala risiko memperbaiki drawdown **atas
isyarat Mxx**. Mekanisme saiz itu umum, jadi hasilnya tetap bermaklumat — tetapi ia **bukan**
pengesahan atau penafian dapatan 1b. Ujian ke hadapan yang betul bagi 1b memerlukan lorong yang
kemasukannya daripada peristiwa sah REVERSE, bukan daripada Lejar.

### 9.3 — 28 Okt 2026: §5.1, §6 dan §7 diselaraskan untuk leg SEC (14 tahun, bukan 6 suku)

§5–§7 ditulis ketika spec ini menganggap **semua** lajur fasa 2 bermula 2026 dan populasinya Lejar
Penuh. §4.1 (leg SEC titik-masa sejak 2009) dan §9.1 (populasi = peristiwa sah REVERSE) membatalkan
kedua-dua anggapan itu. Tiga tempat menjadi tidak sah dan diselaraskan di sini, **sebelum sebarang
keputusan leg SEC dilihat**:

**§5.1 — ufuk ujian pemangkatan.** "≥ 4 daripada 6 suku pertama" ditulis untuk data yang baru
terkumpul 6 suku. Leg SEC ada 2012–2025 (14 tahun penuh; 2026 tidak lengkap, dikecualikan seperti
fasa 1). Bagi leg SEC, Spearman dikira **setiap tahun**, dan lajur diteruskan hanya jika tandanya
konsisten dalam **≥ 10 daripada 14 tahun** dan |rho| purata ≥ 0.05. Bar ini bermakna: `ujian_pangkat.py`
fasa 1 mendapati 7 daripada 30 indikator konsisten-tanda lawan puncak hindsight tetapi hanya **1
daripada 30** lawan pulangan boleh didagangkan. §5.1 asal kekal terpakai kepada leg RS/gred.

**§6 — ambang penerimaan, syarat keempat ditambah untuk leg SEC.** Fasa 1 mengajar bahawa satu
tahun tidak bermakna apa-apa: gerbang 8.1 mula-mula menerima `q5:atr_pct`, `q5:julat20` dan
`q5:bb_lebar` pada 2020 dan 2025 secara berasingan, dan tiada satu pun bertahan apabila disyaratkan
lulus gerbang keras dalam ≥ 2 tahun lain (`SPEC.md` §13.12). Maka bagi leg SEC, syarat tambahan:

4. lajur itu mesti lulus gerbang keras dalam **≥ 2 tahun selain tahun ia ditemui**, dengan kelas
   tahun itu sendiri merupakan penemuan (bukan TIDAK BERGUNA) — iaitu gerbang 8.1 `SPEC.md` §13.11
   dan §13.12 yang sama, tanpa pelonggaran.

**§7 — had yang diakui, dua butir dibatalkan untuk leg SEC.**

- ~~"Tempoh ujian bermula 2026 — satu rejim pasaran sahaja. Keputusan tertinggi ialah CALON."~~
  Tidak terpakai: leg SEC merangkumi 2012–2025, termasuk pasaran menaik rendah-meruap 2013–2019,
  pembetulan 2015–2016, keruntuhan dan pemulihan 2020, pasaran menurun 2022. Ia boleh mencapai
  keputusan penuh, bukan CALON, jika §6 (1)–(4) dipenuhi. Had §7 asal kekal bagi leg RS/gred.
- ~~"Lejar Penuh tiada bias survivorship — ini lebih baik daripada data A02 fasa 1, dan satu sebab
  fasa 2 berbaloi walaupun fasa 1 ditolak."~~ Dibatalkan oleh §9.1: populasi bukan Lejar Penuh.
  Leg SEC berjalan atas universe A02 yang **sama** dengan fasa 1, jadi ia mewarisi sifat
  survivorship yang sama. Itu **had**, bukan kelebihan. Sebab leg SEC berbaloi ialah ia sumber
  maklumat yang berbeza (bukan harga), bukan kerana datanya lebih bersih.

Had tambahan leg SEC yang diakui sekarang, bukan selepas keputusan:

- **Liputan XBRL berperingkat.** Mandat SEC berperingkat 2009–2011: 89 saham ada EPS titik-masa pada
  2009, 253 pada 2010, 482 pada 2011. Sebab itu ujian bermula 2012, bukan 2009.
- **PEAD tertumpu pada saham kecil.** Universe REVERSE ialah 2,000 teratas ikut nilai dagangan,
  iaitu dengan sengaja membuang bahagian keratan-rentas di mana PEAD paling kuat didokumenkan.
  Jangkaan priori oleh itu rendah, dan dinyatakan di sini supaya keputusan "tiada kesan" tidak
  dilaporkan sebagai kejutan.
- **Lajur SEC hadir pada kira-kira 27–30% peristiwa sah** (§4.4) walaupun selepas liputan ticker
  dilebarkan, kerana SUE memerlukan sejarah suku yang cukup. Peristiwa tanpa lajur SEC dikecualikan
  daripada ujian pemangkatan lajur itu, bukan diisi sifar.

### 9.4 — 28 Okt 2026: set signal leg SEC dikunci (sebelum sebarang keputusan dilihat)

§5.2 merujuk "metrik Step 4 fasa 1" tetapi tidak menyatakan bagaimana lajur berterusan SEC ditukar
kepada signal binari. Dibiarkan terbuka, pilihan itu boleh dibuat selepas melihat keputusan. Dikunci
sekarang.

**Sasaran (satu sahaja).** Pulangan boleh didagangkan `pul_henti2atr` seperti fasa 1: masuk pada
buka esok dengan kos satu sisi, henti keras −2×ATR14, ufuk 63 hari, kos keluar. Tiada sasaran
hindsight. Bagi 2020–2025 ia dibaca terus daripada `.cache/hadapan_<tahun>.parquet` fasa 1; bagi
tahun lain ia dikira dengan formula yang **sama** dan disahkan mengeluarkan nombor serupa atas
tahun bertindih.

**Set signal (20 ujian, dikunci; had corong fasa 1 = 30).**

Lajur berterusan → dua hujung kuintil, sempadan daripada **populasi kuintil yang dibekukan** pada
larian pertama (peristiwa sah dengan lajur itu tidak kosong), seperti fasa 1:

| # | Signal |
|---|---|
| 1–2 | `q5:sue`, `q1:sue` |
| 3–4 | `q5:tumbuh_hasil`, `q1:tumbuh_hasil` |
| 5–6 | `q5:pecutan_hasil`, `q1:pecutan_hasil` |
| 7 | `sejak_earnings_le5` — peristiwa dalam 5 hari dagangan **selepas** pengumuman tersedia (tingkap PEAD) |
| 8 | `jangka_earnings_le5` — jangkaan pengumuman berikut dalam 5 hari (§4.3; jangkaan, bukan tarikh sebenar) |
| 9–20 | enam signal kuintil × dua signal tingkap earnings (silang, seperti pemicu × konteks fasa 1) |

**Tiada signal ditambah selepas larian pertama.** Jika lajur lain kelihatan menarik selepas melihat
keputusan, ia bukan penemuan kajian ini.

**Populasi.** Peristiwa sah REVERSE (§9.1) yang lajur berkenaan **tidak kosong**. Peristiwa tanpa
lajur SEC dikecualikan daripada ujian lajur itu, tidak diisi sifar (§9.3). Kadar asas dan kawalan
rawak dikira atas populasi yang sama supaya lift tidak dicemari perbezaan liputan.

**Keluarga FDR.** Satu keluarga `FASA2_SEC`, 20 ujian, BH-FDR q ≤ 0.01 (§5.3). Berasingan daripada
leg RS/gred dan daripada kelima-lima keluarga fasa 1 — tiada penggabungan kiraan ujian.

**Keputusan.** Lajur diterima hanya jika §6 (1)–(4) dipenuhi, termasuk syarat §9.3 bahawa ia lulus
gerbang keras dalam ≥ 2 tahun selain tahun ia ditemui. Jika tidak: **DITOLAK**, dilaporkan sebagai
ditolak.

### 9.5 — 28 Okt 2026: §9.3 ambang pemangkatan dinyatakan sebagai PECAHAN (sebelum keputusan dilihat)

§9.3 menulis "konsisten dalam ≥ 10 daripada **14** tahun". Itu mengandaikan kesemua 14 tahun
2012–2025 tersedia. `step1_run.py` sedang dijalankan untuk 2012–2019 dan mungkin tidak semuanya
siap; dengan 12 tahun, peraturan seperti ditulis **tidak boleh dinilai sama sekali**.

Dinyatakan semula sebagai pecahan yang sama, supaya ia terdefinisi bagi apa-apa bilangan tahun:

- tanda konsisten dalam **≥ 71% tahun yang dinilai** (pembundaran ke atas), **dan**
- **≥ 10 tahun dinilai** (jika kurang, lajur itu dilapor **BELUM BOLEH DINILAI**, bukan lulus dan
  bukan gagal), **dan**
- |rho| purata ≥ 0.05.

Pada 14 tahun: ceil(0.71 × 14) = 10 — **sama** dengan §9.3 asal. Ini penyataan semula, bukan
pelonggaran: pecahannya tidak berubah, dan syarat minimum 10 tahun dinilai menghalang keputusan
daripada sampel pendek. Dikunci sebelum sebarang keputusan §5.1 dilihat.

### 9.6 — 28 Okt 2026: had kebasian lajur SEC dikunci (sebelum keputusan dilihat)

`merge_asof` arah ke belakang melekatkan pengumuman **terakhir yang tersedia**, tanpa had berapa
lama dahulu. Taburan `hari_sejak_earnings` dalam `sec_join.csv` (24,871 baris) menunjukkan ia
masalah sebenar walaupun kecil:

| Kuantil | Hari |
|---|---|
| p50 | 47 |
| p75 | 70 |
| p90 | 87 |
| p95 | 97 |
| p99 | **952** |
| maks | **5,241** |

Kitaran suku normal berakhir sekitar p95 = 97 hari. Lonjakan ke 952 pada p99 ialah saham yang
**berhenti memfail** (delist, diambil alih, atau hanya pernah memfail sekali dahulu). SUE dari
14 tahun lalu yang dilekatkan pada peristiwa 2025 ialah hingar, bukan maklumat titik-masa, dan ia
akan masuk ke dalam kuintil seolah-olah ia nilai sah.

**Peraturan dikunci.** Lajur SEC (`sue`, `tumbuh_hasil`, `pecutan_hasil`) digunakan hanya jika
pengumuman terakhir yang tersedia berada dalam **120 hari kalendar**. Lebih lama daripada itu,
ketiga-tiga lajur dianggap **kosong** bagi baris itu (dikecualikan, bukan diisi sifar — §9.3).

- 120 hari = satu kitaran suku + tempoh tenggang, dan ia nilai yang **sama** dengan `SELANG_MAKS`
  yang sudah digunakan untuk jangkaan kitaran dalam `step10_sec.py` (§4.3). Satu ambang, bukan dua.
- Ia menyentuh **585 baris (2.35%)**, jadi ia tidak boleh mengubah kesimpulan secara material. Ia
  dikunci kerana ia betul, bukan kerana ia besar.
- `hari_sejak_earnings` **mentah** kekal dalam `sec_join.csv` supaya penapis ini boleh diaudit.
  Penapis dikenakan dalam `step11_sec_nilai.py`, bukan dalam join.
- Signal `sejak_earnings_le5` (tingkap PEAD, ≤ 5 hari) tidak terjejas: ia sudah lebih ketat.

### 9.7 — 28 Okt 2026: ambang 3,000 dikenakan SETIAP TAHUN (sebelum keputusan dilihat)

§4 menulis "≥ 3,000 peristiwa sah dengan nilai lajur itu tidak kosong" tanpa menyatakan sama ada ia
setahun atau keseluruhan 14 tahun. §4.4 melaporkannya setiap tahun dan menulis "LULUS setiap
tahun", jadi niatnya setahun — tetapi ia tidak pernah dinyatakan sebagai peraturan. Dibiarkan
kabur, pilihan itu boleh dibuat selepas melihat tahun mana yang menyebelahi keputusan.

Liputan selepas `step1` 14 tahun siap dan satu larian isian awal (28 Okt 2026, kiraan sahaja):

| Tahun | Peristiwa | Saham | Ada SEC | SUE tidak kosong | % |
|---|---|---|---|---|---|
| 2012 | 7,028 | 1,205 | 383 | **2,065** | 29.4 |
| 2013 | 7,946 | 1,361 | 456 | **2,895** | 36.4 |
| 2014 | 8,271 | 1,487 | 499 | **2,968** | 35.9 |
| 2015 | 9,497 | 1,591 | 531 | 3,403 | 35.8 |
| 2016 | 9,715 | 1,624 | 544 | 3,413 | 35.1 |
| 2017 | 9,530 | 1,745 | 576 | 3,314 | 34.8 |
| 2018 | 12,030 | 1,873 | 615 | 4,145 | 34.5 |
| 2019 | 11,839 | 1,907 | 630 | 4,072 | 34.4 |
| 2020 | 12,858 | 2,045 | 657 | 4,266 | 33.2 |
| 2021 | 15,259 | 2,283 | 704 | 5,082 | 33.3 |
| 2022 | 15,440 | 2,255 | 714 | 5,167 | 33.5 |
| 2023 | 13,642 | 2,202 | 739 | 4,739 | 34.7 |
| 2024 | 14,151 | 2,191 | 737 | 5,037 | 35.6 |
| 2025 | 13,998 | 2,237 | 752 | 4,832 | 34.5 |

Jumlah: **161,204** peristiwa sah, **55,398** dengan SUE tidak kosong. Tiga tahun pertama berada di
bawah 3,000, kerana mandat XBRL berperingkat 2009–2011 (§9.3) — isian awal yang sedang berjalan
akan menaikkannya, tetapi ia mungkin tidak cukup.

**Peraturan dikunci.** Ambang 3,000 dikenakan **setiap tahun**. Tahun di bawahnya **dikecualikan**
daripada §5.1, dan tidak dikira dalam pembilang mahupun penyebut pecahan §9.5. Jika tahun yang
layak kurang daripada 10, keputusan ialah **BELUM BOLEH DINILAI** (§9.5), bukan lulus dan bukan
gagal.

Ini **tidak** melonggarkan apa-apa: dengan 11 tahun layak, pecahan 71% menuntut 8 tahun konsisten,
dan minimum 10-tahun §9.5 masih terpakai. Ia menutup kekaburan, dan ia dikunci sebelum sebarang
rho pernah dikira.

### 9.8 — 28 Okt 2026: pelaksanaan §5.4 (portfolio) dan dua saiz

`REVERSE/step12_sec_portfolio.py`. Dijalankan **hanya** jika §5.1 dan §5.3 lulus (§6 syarat 1);
jika tidak ia menolak untuk berjalan dan mencetak sebabnya, kerana mencari portfolio daripada signal
yang sudah gagal ujian kebetulan hanya mencari kebetulan yang lebih besar.

- **8 slot × 12.5%**, kos penuh, tiga rujukan keluar fasa 1 (`REF_pegang_252`,
  `REF_chandelier_4atr`, `REF_jual_hari63`).
- **Dua saiz** seperti §5.4 menuntut: tetap 12.5%, dan berskala risiko SPEC_1B —
  (RISIKO × ekuiti) / (k × ATR%), had 2–25%, k = 4, risiko 1.0%. Apabila ATR tidak diketahui, ia
  jatuh balik ke saiz tetap (bukan dilangkau), supaya bilangan posisi kekal setanding.
- **Kawalan rawak** (§6 syarat 3): entri rawak, bilangan sama **setiap bulan**, benih 42 — sama
  seperti fasa 1. Signal mesti mengalahkannya pada pulangan **dan** MDD.
- **Metrik dilaporkan** ialah yang menjadi soalan sebenar pengguna, bukan lift: pulangan tahunan
  terkompaun, MDD, median bulanan, % bulan ≥ +10%, bulan terburuk, median pulangan dagangan.

`step9_portfolio.jalankan()` fasa 1 **diguna semula, bukan difork**, supaya nombor setanding. Satu
parameter `saiz` ditambah padanya; apabila ia tidak diberi, `bhg == BAHAGIAN` dan pemeriksaan
`isfinite` mustahil menolaknya, jadi tingkah laku fasa 1 tidak berubah sama sekali.

### 9.9 — 28 Okt 2026: gerbang §5 menuntut KEDUA-DUA tahun layak DAN isian awal selesai

Pada 16:30 UTC rantaian automatik memulakan `step11` (penilaian §5, sekali sahaja) kerana gerbang
yang saya kodkan dipenuhi: ketiga-tiga lajur mencapai 13 tahun layak, melepasi minimum 10 (§9.7).
**Ia dihentikan sebelum sebarang keputusan ditulis.**

Sebabnya: gerbang itu mengukur perkara yang salah. Liputan ketika itu hanya **1,081 daripada 2,237
ticker (48%)** bagi 2025, dengan **1,530 CIK masih belum diisi**. §4.4 menetapkan penilaian
dijalankan "atas populasi penuh", dan sebab yang dicatat di sana ialah **kecenderungan pemilihan**
— universe lama ialah watchlist dan posisi C, iaitu nama yang lebih besar dan lebih cair. Pada 48%
kecenderungan itu baru separuh dibetulkan.

Bilangan tahun layak dan keterwakilan sampel ialah dua perkara berbeza. Ambang 3,000 setahun (§9.7)
memastikan setiap tahun ada data **cukup banyak**; ia tidak mengatakan apa-apa tentang sama ada
sampel itu **keratan-rentas universe REVERSE**. Gerbang lama hanya menyemak yang pertama.

**Gerbang dikunci (kedua-dua syarat):**

1. ≥ 10 tahun layak bagi setiap lajur SEC (§9.7, §9.5); **dan**
2. isian awal selesai — `belum_diisi = 0` dalam `data/sec/status.json`.

Pengesan dataran (12 kitaran × 10 min = 2 jam tanpa pertambahan **liputan mahupun `belum_diisi`**)
kekal sebagai jaring keselamatan, supaya rantaian tidak tergantung jika isian awal berhenti maju.
Jika ia mencetus, penilaian diteruskan dengan liputan yang ada dan laporan menyatakannya — tetapi
itu keputusan terakhir, bukan pertama.

Dicatat kerana ia hampir menjadi kesilapan yang paling mahal dalam kajian ini: tembakan pradaftar
hanya ada satu, dan membelanjakannya atas sampel yang saya sendiri sudah dokumenkan sebagai berat
sebelah akan menjadikan keputusannya tidak boleh dipercayai — tanpa cara untuk mengulanginya.
