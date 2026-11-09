# STRATEGI — satu rancangan, satu baris gilir, peraturan keputusan dipra-komit

**Status keadaan semasa dijana oleh `python3 REVERSE/strategi.py`, bukan daripada ingatan.**
Dokumen ini menetapkan matlamat, syarat berhenti dan pokok keputusan. Skrip membaca CSV
keputusan sebenar dan memberitahu kita berada di cabang mana. Ujian unit
`ujian/test_strategi.py` gagal jika registry menyatakan sesuatu belum diuji sedangkan fail
keputusan sudah mengandunginya — itu tepat pepijat yang membuat `GB08` dan `GB04` disenarai
sebagai "calon" selepas kedua-duanya diuji dan gagal.

## 1. Mengapa kajian ini tidak pernah tamat

Empat sebab struktur, bukan kecuaian:

1. **Tiada takrif siap.** `SASARAN.md` mengukur +10%/bulan = 3.14×/tahun = 8,994,377× atas
   14 tahun, dan SPY sendiri memberi 0% bulan ≥ +10% dalam 13 daripada 14 tahun. Sasaran itu
   **tertutup**. Tetapi tiada sasaran gantian pernah ditulis, jadi setiap keputusan membaca
   "gagal" dan carian tidak boleh berhenti.
2. **Tiada baris gilir.** Eksperimen dipilih reaktif setiap perbualan.
3. **Sumber kebenaran hanyut** daripada keputusan sebenar.
4. **Tiada peraturan keputusan dipra-komit** — setiap keputusan dibincang semula dari kosong.

## 2. Matlamat — bertingkat, boleh diukur, dan satu daripadanya mesti dipilih

Penanda aras ialah **SPUS** (patuh Syariah; `PENANDA_ARAS_SYARIAH.md`), bukan SPY.
Dua konvensyen, **jangan dicampur**: CAGR seluruh tingkap **17.95% / MDD −26.82% /
nisbah 0.669**, atau median setiap tahun **26.09% / MDD −10.14%**. Semua gate di bawah
memakai konvensyen pertama.

| Tingkat | Takrif | Status |
|---|---|---|
| **T0** | +10%/bulan | **TERTUTUP** secara aritmetik. Tidak akan dibuka semula. |
| **T1** | CAGR > 17.95% **DAN** MDD ≥ −26.82% | belum dicapai oleh apa-apa (0 / 413 + 36) |
| **T2** | nisbah `CAGR ÷ \|MDD\|` > 0.669 **DAN** CAGR > 17.95% | belum dicapai |
| **T3** | CAGR ≈ SPUS (≥ 15%) dengan MDD **jauh lebih cetek** (≥ −15%) | belum diuji sebagai sasaran |

**KEPUTUSAN PENGGUNA 31 Okt 2026: sasaran = T1 ATAU T3 (mana-mana satu).** T3 dipilih sebagai
syarat menang penuh, bukan separa, kerana bagi pedagang swing MDD −15% berbanding −27% ialah
kemenangan sebenar walaupun pulangan sama. `strategi.py` menguatkuasakan takrif ini.
| **T4** | Terima SPUS + tunai pada berat pilihan pengguna | **tersedia sekarang, tiada kajian diperlukan** |

T4 bukan kekalahan: `SISTEM.md` mengukur nisbah campuran SPUS+tunai hampir **pemalar
0.642–0.669** merentas setiap berat, jadi berat ialah soalan **toleransi drawdown**, bukan
soalan data. 100% → +17.95%/−26.82%; 60% → +10.87%/−16.62%; 40% → +7.27%/−11.25%.

## 3. Syarat berhenti — dipra-komit, tidak boleh dilonggarkan selepas melihat keputusan

**BERHENTI–MENANG:** mana-mana eksperimen dalam baris gilir §4 melepasi **T1 atau T3**
dengan kawalan rawak dan jalur benih, pada tingkap tahan. Tindakan: bekukan konfigurasi,
tulis spec hadapan, jalankan sebagai lorong `portfolio_slot/` selama ≥ 126 sesi sebelum
sebarang dakwaan.

**BERHENTI–TUTUP** (diterima pengguna 31 Okt 2026)**:** jika **E1 hingga E6 selesai dan
tiada satu pun melepasi T1 atau T3**,
kajian signal/pembinaan **ditutup**. Tindakan: terima **T4**, pengguna pilih berat, dan
sumber dialih sepenuhnya kepada pelaksanaan (kecacatan henti hari-0, kualiti data, jejak
hadapan). **Tiada eksperimen ke-7 ditambah selepas melihat keputusan E1–E6.**

**BERHENTI–SEPARA:** jika sesuatu melepasi **T2** sahaja (nisbah `CAGR ÷ |MDD|` > 0.669
tetapi CAGR di bawah 15%), ia dilaporkan sebagai lorong risiko-rendah dan diuji ke hadapan,
tetapi **tidak** didakwa mengalahkan SPUS dan ia **tidak** menghentikan baris gilir.

Syarat tambahan yang mengikat semua: apa-apa dapatan pada alam `AL01` kekal **bersyarat**
sehingga `E2` menjalankannya pada alam dagangan sebenar.

## 4. Baris gilir — enam eksperimen, berurutan, dengan cabang ditulis dahulu

Urutan dipilih mengikut **nilai jangkaan ÷ kos**, bukan minat. Setiap item menyatakan bukti
repo yang menyebabkan ia wujud, supaya tiada eksperimen "sebab terfikir".

### E1 · PEGANG × SLOT · **SELESAI 31 Okt 2026 — gagal T1/T3 → E2**
Laporan `PEGANG_SLOT.md`. Had pegangan **42 bar** mengalahkan "tiada had" dalam **72/128**
sel, puncaknya **+39.24%** lawan +12.09% — lever tunggal terbesar yang pernah diukur dalam
kajian ini. Tetapi `P1` (29) dan `P2` (24) **tidak bertindih langsung**: setiap tetapan yang
menaikkan pulangan menaikkan MDD lebih banyak. `SZ10` DITOLAK: lengkung slot memuncak pada
80–160 dan merosot; kolam penuh (slot 1280, melepasi kapasiti 753) memberi 9.19–16.71%.
Hingar pemilihan pada sel terbaik ialah **42.8 mata peratus** merentas 20 benih.

Pradaftar `SPEC_PEGANG_SLOT.md`, skrip `step24_pegang_slot.py` (komit `3370a4f`).
**Bukti:** jangkaan/dagangan dan pusingan/tahun bergerak bertentangan dan hanya dua hujung
pernah diukur (`X29` 10 bar +0.294%; `X13` ~85 bar +4.350%); lengkung slot menaik monoton
pada kedua-dua paksi dalam DUA kajian bebas dan tidak pernah dijalankan ke hadnya.
- **JIKA T1/T3 lulus** → BERHENTI–MENANG.
- **JIKA had pegangan menang tetapi masih bawah T1** → bawa had terbaik ke E2–E4 sebagai
  tetapan tetap; jangan ulang paksi ini.
- **JIKA slot tinggi menang hanya kerana isyarat tidak lagi menyumbang** (gate `P3` gagal di
  sana) → itu **struktur indeks**, bukan isyarat; lompat terus ke E3 dan catat dalam §6.
- **JIKA kedua-duanya gagal** → E2.

### E2 · ALAM `AL02` — alam dagangan sebenar
**Bukti:** setiap satu daripada 449 ujian berjalan pada `A01`/A02 yang (a) **tiada saham
delist** = bias survivorship ke atas, dan (b) **bukan** alam yang repo tapis untuk belian.
Ini bukan mencari alfa; ia menentukan sama ada nombor sedia ada bermakna.
**Kos:** rendah (tapis panel sedia ada).
**Had yang mesti ditulis dalam spec:** `data/skrin/etf_shariah.csv` ialah 326 konstituen
**semasa sahaja, tiada tarikh**, jadi ujian ini membawa bias keahlian-ke-belakang. Ia
dijalankan sebagai **semakan kesahan dua arah**, bukan sebagai dakwaan prestasi.
- **JIKA kelebihan mati pada `AL02`** → BERHENTI–TUTUP dipercepat; E3–E6 dibatalkan kerana
  ia semua akan diuji pada alam yang salah.
- **JIKA bertahan** → E3.

**SELESAI 31 Okt 2026 — laporan `ALAM.md`.** Gate (a) **lulus** (46.2% lawan ambang 25%):
kelebihan isyarat **wujud** pada alam dagangan. Gate (b) **gagal** (27.5% lawan 50%): kesan
had pegangan **tidak merentas alam**, kerana `AL02` membekalkan 7.7 isyarat/sesi lawan 105.2
dan memotong pegangan di sana hanya memindahkan modal ke tunai. **Spec §5 tidak meliputi
gabungan (a) lulus + (b) gagal**, dan kod mengira `kekal = (a) and (b)` lalu mencetak MATI —
keputusan yang spec tidak benarkan. Rasional MATI ("kelebihan tidak wujud pada alam yang
kita dagang") **dipalsukan**. Diserahkan kepada pengguna.

**Pembetulan proses:** setiap spec selepas ini mesti menyenaraikan **setiap gabungan**
keputusan gate, bukan hanya "semua lulus" dan "yang utama gagal".

**KEPUTUSAN PENGGUNA 31 Okt 2026: teruskan ke E3, dan jalankan E3–E6 pada `AL02`.**
Sebabnya E2 sendiri: `AL02` ialah alam dagangan sebenar **dan** ia memberi nombor lebih
baik pada kedua-dua paksi (CAGR +2.69 mata, MDD +6.19 mata lebih cetek, 58/80 sel). Had
pegangan **tidak** dibawa sebagai tetapan tetap — gate (b) menunjukkan ia bergantung kepada
ketumpatan isyarat, bukan peraturan am.

### E3 · INSTRUMEN `IS02` — putaran ETF sektor
**Bukti:** prior positif paling kuat dalam seluruh registry. `SETUP.md` mengukur SPY
**+3.356%** dan QQQ **+4.419%** melepasi syarat ekor yang **598 daripada 598** setup saham
gagal, kerana indeks **itulah** kepelbagaian merentas ekor. ETF sektor ialah titik tengah
antara satu saham dan satu indeks, dan ia tidak pernah diuji.
**Kos:** sederhana — repo **tiada** data ETF sektor (A02 = 3,260 saham; `idx.parquet` hanya
SPY + QQQ). Perlu muat turun ~11 ticker SPDR, 2009–2026, ke dalam stor yang sama.
- **JIKA T1/T3 lulus** → BERHENTI–MENANG.
- **JIKA hanya T2** → BERHENTI–SEPARA; baris gilir **diteruskan** ke E4.
- **JIKA gagal** → E4.

**SELESAI 31 Okt 2026 — laporan `INSTRUMEN.md`.** T1 0, T3 0 → **E4**. Pulangan lulus luas
(P1 26/40) dan risiko gagal **sepenuhnya** (P2 **0/40**, paling cetek −31.61% lawan SPUS
−26.82%) — kali **ketiga berturut-turut** corak itu, pada tiga mekanik berbeza.
**Hipotesis `SETUP.md` DISAHKAN**: `tanpa5` bakul positif pada **8/8** sel (+0.55% hingga
**+4.77%**, tertinggi dalam kajian) lawan **0/598** setup saham. Kepelbagaian merentas ekor
memang membetulkan masalah ekor — tetapi masalah **berpindah kepada drawdown**. Hanya `U14`
(momentum 12−1) mengalahkan kawalan rawak (5/8); `U11` dan `U03` Clenow 0/8. `U14` k=1
nisbah 0.75 = **BERHENTI–SEPARA**, baris gilir diteruskan. Memegang bakul Electronic
Technology **sahaja** memberi +32.67%, mengalahkan setiap putaran — dan itu pilihan selepas
melihat keputusan; jalur kawalan `k=1` ialah **17.1 mata**.

### E4 · KELUAR `X31`/`X32` — keluar peringkat PORTFOLIO
**Bukti:** pilihan keluar diukur **12× lebih berpengaruh** daripada masuk (sebaran 4.997
mata lawan lift terbaik 0.392), tetapi **kesemua 23** keluar yang diuji ialah peraturan
setiap posisi. `X31` (gugur daripada 3 teratas pangkat 252 hari) dan `X32` (imbang berkala
sahaja) ialah keluar peringkat portfolio dan menyerang kesesakan yang `PORTFOLIO_N.md`
diagnosis: pusing ganti ~3 kali/slot/tahun.
**Kos:** sederhana — perlu gelung pangkat + imbang dalam enjin `step22`.
- Cabang sama seperti E3.

**SELESAI 31 Okt 2026 — laporan `KELUAR_PORTFOLIO.md`.** T1 0, T3 0 → **E5**. `P2` gagal
pada setiap sel untuk kali **keempat berturut-turut**. **`E4a` LULUS**: keluar peringkat
portfolio mengalahkan keluar setiap posisi terbaik pada alam yang sama (47.44% lawan
21.01%), jadi jangkaan priori saya salah — pada 214 saham kolam pemeringkat cukup besar
untuk pemeringkatan menambah nilai, tidak seperti 11 bakul E3.

**DUA DAPATAN YANG MENGUBAH BACAAN LAPORAN TERDAHULU:**
1. **Isyarat masuk MEROSAKKAN putaran berpangkat.** `RAWAK` (tiada isyarat) +47.44% dan
   lulus `P3`; `GB02_atau3` +24.04% dan **gagal** `P3`. Menapis membuang calon, dan
   pemeringkat memerlukan calon — `SETUP.md` pada paksi baharu.
2. **Pandang ke hadapan keahlian `AL02` menyanjung MDD sebanyak 30.9 mata.** Diagnostik
   pemalsuan `AL04` (N teratas nilai20, **titik-masa kausal**): konfigurasi yang sama
   memberi −37.94% pada `AL02` tetapi **−68.80%** pada 214 teratas titik-masa. Pulangan
   separa bertahan (+34.78%); risiko **tidak**. **Laporan E2 dan E3 mesti dibaca dengan
   pembetulan ini.**

### E5 · KORELASI `KR03` — had bilangan setiap industri
**Bukti:** tidak pernah diukur. 8–10 slot yang semuanya satu industri = berkesan 2–3 slot.
`PORTFOLIO_N.md` mendapati MDD dikawal oleh **urutan**, bukan bilangan slot — had industri
ialah lever kedua pada paksi yang sama.
**Kos:** rendah jika peta ticker→industri wujud; perlu disemak dahulu.
- Cabang sama seperti E3.

**SELESAI 31 Okt 2026 — laporan `KORELASI.md`.** Dijalankan pada **`AL04` titik-masa**
(pembetulan dipaksa oleh E4). T1 0, T3 0 → **E6**. `P2` gagal kali **kelima**. Tetapi
**`E5a` lulus kedua-dua bahagian**, dan jangkaan priori saya #3 salah: had industri **bukan**
pertukaran. Had **1** memperbaiki **kedua-dua** paksi serentak — median **+1.65 mata CAGR
dan +1.60 mata MDD lebih cetek**. Mekanismenya diukur: tanpa had, **6 daripada 8 slot** boleh
berada dalam satu industri, jadi "8 slot" sebenarnya ~3 taruhan. Saiznya kecil — komponen,
bukan penyelesaian. **Dapatan E4 berulang lebih kuat**: `RAWAK` +49.55% lawan `GB02_atau3`
+11.98% pada alam 500, jurang **37.6 mata**. "Jangan tapis dahulu kemudian peringkat" kini
direplikasi pada dua alam bebas.

### E6 · GABUNGAN `GB07` — hierarki merentas paksi
**Bukti:** satu-satunya operator gabungan yang belum diuji yang menggunakan signal pada
**paksi berlainan** (signal A menentukan ALAM, signal B menentukan URUTAN). `GB01` `DAN`,
`GB02` `ATAU`, `GB03` undi, `GB04` agregat pangkat dan `GB08` penapis terbalik **semuanya
sudah diuji**; empat gagal, satu (`GB02`) lulus gate setiap-dagangan tetapi gagal portfolio.
**Kos:** rendah.
- **JIKA gagal** → **BERHENTI–TUTUP.**

**SELESAI 31 Okt 2026 — laporan `HIERARKI.md`. BARIS GILIR DITUTUP: `KEPUTUSAN_AKHIR.md`.**
T1 0, T3 0 → **BERHENTI–TUTUP**. `P2` gagal kali **keenam**. Tetapi **`E6a` LULUS 19/48**:
saringan **berdiri** memperbaiki **kedua-dua** paksi, sedangkan pintu masuk **harian**
memusnahkan pemeringkat. Bezanya **kekerapan**, bukan jenis — pintu harian beri 7.7–21.8
calon/sesi (kolam lebih kecil daripada slot), saringan berdiri beri 102–326 (kolam 13–41×
slot). **Peraturan: kekalkan kolam calon ≥ ~10× bilangan slot.** Itu merekonsiliasi
`SETUP.md` (598/598 penapis merugikan — kesemuanya pencetus jarang) dengan dapatan ini.

## 5. Apa yang TIDAK akan diuji lagi, dan mengapa

Ditulis supaya ia tidak boleh dicadangkan semula tanpa bukti baharu:

- **Peraturan MASUK baharu** — 280 ujian, gate3 **0**. Ruang ditutup.
- **Penapis gaya setup** — 598 setup, lift positif **0**. Gagal kerana **struktur**: menapis
  membuang bar, dan taburan dipandu ekor kanan.
- **Fundamental / SEC / silang-keluarga** — ditutup oleh `KEPUTUSAN_FASA2_SEC.md` dan
  `SILANG_GATE_C.md`.
- **Sasaran untung tetap** — diukur merugikan **lima kali** (`X10` menang 94.1% dengan
  jangkaan −0.023%; `C06` menang 32.9% dengan −0.591%).
- **Penalaan parameter / Optuna** — di luar skop kajian sejak hari pertama.
- **`C07`/`C09`/`C11`** — satu keluarga dengan `C02` yang kalah pada **kedua-dua** paksi.
- **`U06`/`U07`/`U12`** (WorldQuant 101, OpenAP 212, GTJA 191) — tersekat rangkaian:
  `arxiv.org` dan `huggingface.co` disekat DNS/proksi, dan pakej PyPI `alpha101` memberi
  **404** sedangkan `pandas` dan `qlib` memberi 200, jadi ia bukan sekatan proksi — pakej
  itu tiada. Dibuka semula hanya jika sumber sah muncul.
- **PG/IB baki** — dijawab oleh E1; jangan ulang sebagai paksi berasingan.

## 6. Log cabang

Setiap eksperimen menambah satu baris di sini apabila selesai: keputusan, cabang yang
diambil, dan sebabnya. Ini rekod *mengapa* kita berada di langkah semasa.

| # | Eksperimen | Keputusan | Cabang diambil |
|---|---|---|---|
| — | A masuk (280) | 0 lulus gate3 | ruang masuk ditutup |
| — | B keluar (69) | 0 lulus gate3 | keluar setiap-posisi ditutup |
| — | GABUNGAN (14) | 2 lulus gate3 (`GB02` kesatuan) | bawa ke portfolio |
| — | Silang akhir (8) | 8 lulus gate setiap-dagangan | bawa ke portfolio |
| — | PORTFOLIO (36) | **0 lulus P1–P4** | diagnosis: pegang 84.9 bar + ekor |
| — | CARA (6) | 0 lulus; `C01` terbaik | paksi cara ditutup |
| E1 | PEGANG × SLOT (320) | **T1 0 · T3 0 · lulus 0/320** (P1 29, P2 24, P3 101, P4 9) | **E2** |
| E2 | ALAM `AL02` (160) | **T1 0 · T3 0**; gate (a) **lulus 46.2%**, gate (b) **gagal 27.5%** | **spec tidak meliputi kes ini — keputusan pengguna: E3 pada `AL02`** |
| E3 | INSTRUMEN `IS02` (40) | **T1 0 · T3 0**; P1 26/40 tetapi **P2 0/40**; P3 5 (`U14` sahaja); P4 1 | **E4** |
| E4 | KELUAR portfolio `X31`/`X32` (48) | **T1 0 · T3 0**; P1 33, **P2 0**, P3 16, P4 17; **`E4a` LULUS** (47.44% lawan 21.01%) | **E5** |
| E5 | KORELASI `KR03` (96, `AL04` titik-masa) | **T1 0 · T3 0**; P1 23, **P2 0**; **`E5a` LULUS dua-dua** — had 1 beri **+1.65 CAGR DAN +1.60 MDD** | **E6** |
| E6 | GABUNGAN `GB07` (60, `AL04` titik-masa) | **T1 0 · T3 0**; P1 38, **P2 0**; **`E6a` LULUS 19/48** — saringan berdiri perbaiki dua-dua paksi | **BERHENTI–TUTUP** |
| — | **JUMLAH baris gilir** | **724 konfigurasi · 6,994 larian · P1 161 · P2 24 · T1 0 · T3 0** | `KEPUTUSAN_AKHIR.md` |
| SAT | **Kajian TUNGGAL luar baris gilir** (kebenaran pengguna 9 Nov 2026): satelit `GB02_atau3` × `X15` 15% atas teras indeks 35% + tunai, had 1 industri, rejim ON; 14 sel, 90 larian (`SPEC_SATELIT.md`) | **GAGAL P1/P2/P3/P5**: CAGR tahan +6.12% lawan indeks 50% +7.59% dan satelit RAWAK +7.82%; MDD -13.7% (`SATELIT.md`) | satelit kekal 0%; tunai sepenuhnya sehingga TERBUKTI, tiada ETF pasif (keputusan pengguna 9 Nov; `kajian/FABLE_PENILAIAN.md` §9); kebenaran tunggal terbelanja |

## 7. Peraturan proses — supaya kesilapan yang sama tidak berulang

1. **Spec DAN kod dikomit sebelum keputusan dilihat.** Sudah diikut; kekalkan.
2. **Ujian asap mesti meliputi KOMBINASI penuh, bukan komponen.** Lima pepijat terlepas pada
   30 Okt 2026 kerana komponen diuji berasingan.
3. **Setiap larian baharu mesti membawa kawalan regresi** terhadap larian sebelumnya pada
   konfigurasi bertindih (contoh: `step24` had=tiada memberi ekuiti identik `step22`).
4. **Pradaftar mesti mengandungi syarat `jangkaan mutlak > 0`** — lift positif atas asas
   negatif masih merugikan (`N16`×`X1`).
5. **Jangkaan priori ditulis sebelum larian.** Rekod saya: salah pada 2 daripada 3 gate dalam
   tiga pradaftar berturut-turut. Menulisnya menjadikan kesilapan itu boleh dikira.
6. **`strategi.py` dijalankan pada permulaan setiap sesi kajian** sebelum apa-apa dicadangkan.
   Ia, bukan ingatan atau `CLAUDE.md`, yang menyatakan apa yang sudah diuji.
