# Pradaftar — SATELIT: GB02_atau3 × Chandelier di atas teras indeks + tunai, dalam toleransi MDD -10%

Ditulis dan dikomit **sebelum** sebarang keputusan dilihat. Skrip: `REVERSE/step41_satelit.py`
(dikomit dalam komit yang sama). Keluaran: `REVERSE/SATELIT.md`, `REVERSE/satelit.csv`,
`REVERSE/satelit_dagangan.csv`. Kebenaran: keputusan pengguna 9 Nov 2026 untuk SATU kajian
gabungan baharu walaupun baris gilir E1–E6 ditutup; pilihan B dalam
`BacktestShariah2/kajian/FABLE_PENILAIAN.md` §10 (pengguna menyerahkan pilihan kepada penilai).

## 1. Soalan (satu)

Pelan yang disokong data dalam `FABLE_PENILAIAN.md` §9 ialah teras indeks 35% + tunai 65%
(MDD -10% pada 2020–2025). Soalan: **adakah satelit kaedah sebanyak 15% akaun — masuk
`GB02_atau3`, keluar Chandelier 4×ATR14, urutan ATR% menaik, had 1 saham setiap industri,
belian baharu hanya dalam rejim QQQ ON — menambah pulangan berbanding membelanjakan 15% itu
pada indeks, tanpa memperdalam MDD akaun melebihi -10%?**

Ini belum pernah diukur. Yang sudah diukur dan TIDAK diulang: had pegang 10 sesi
(`PEGANG_SLOT.md`: terburuk pada setiap slot), portfolio satelit 100% pendedahan
(`PORTFOLIO_N.md`, `PORTFOLIO_94B.md`: MDD -38% hingga -83%), penapis RS (pemimpin rugi paling
teruk dalam OFF, `FABLE_PENILAIAN.md` §5).

## 2. Peraturan (dikunci)

Alam `AL01` (A02 cair, nilai20 ≥ USD100k), cara `C01` (beli buka esok), kos penuh dua sisi
(komisen 0.1% + slippage 0.05/0.10/0.25% ikut nilai20), tiada margin, satu posisi setiap ticker,
sauh HARIAN. Enjin keluar dan panel diguna semula daripada `step22_portfolio_n.py` /
`step24_pegang_slot.py` / `pembinaan.py`; tiada enjin kedua. Yang baharu: akaun tiga bahagian
(teras, satelit, tunai), penapis rejim, had industri.

**Akaun.**
- Teras = indeks berat `W_TERAS = 0.35` ekuiti, diimbang pada **sesi pertama setiap bulan** pada
  harga buka, kos 0.15% setiap sisi (komisen 0.1% + slippage 0.05%).
- Satelit = sasaran `W_SAT = 0.15` ekuiti: setiap belian = `W_SAT × ekuiti_semalam ÷ slot`,
  dihadkan oleh tunai; tiada belian jika posisi satelit terbuka ≥ slot. Tiada imbang paksa
  posisi satelit.
- Tunai = baki, tiada faedah (tiada riba).
- **Instrumen teras = SPY harian (A02 `idx.parquet`)**, bukan SPUS, kerana SPUS tiada sejarah
  2012–2019 dan repo tiada SPUS harian 2020–2025 (hanya bulanan `spus_bulanan.csv`; sumber luar
  tidak boleh dicapai dari sesi ini — direkod). Ini proksi yang **memihak kepada satelit**? Tidak
  semestinya: SPUS mengalahkan SPY 2020–2025 (+26.1% lawan +21.6% median tahunan), jadi
  alternatif pasif yang sebenar lebih kuat daripada yang disimulasi. Jadual maklumat §5 melapor
  campuran SPUS bulanan + tunai 2020–2025 sebagai rujukan.

**Satelit.**
- MASUK `GB02_atau3` = `N19` ∪ `N37` ∪ `N115` (takrif `step18_nxx.topeng`, tidak diubah);
  kawalan `RAWAK` = semua calon layak.
- KELUAR `X15` Chandelier: tutup < tutup tertinggi sejak masuk − 4 × ATR14 (ATR pada sauh) →
  jual buka esok; had masa `CAP = 126` bar (SOP). Tiada sasaran, tiada henti peratus.
- URUTAN `U08` ATR% menaik (tentu); ablasi `U01` rawak 20 benih.
- HAD INDUSTRI 1: tiada belian jika sudah ada posisi satelit dalam industri sama
  (`step28_korelasi.peta_industri`, TradingView `tv_us.csv`; tanpa industri = satu kumpulan).
- REJIM: belian baharu hanya jika pada sauh `a` QQQ tutup > SMA50 **dan** SMA10 > SMA20
  (takrif `SPEC_KAD_SKOR.md`). Posisi sedia ada tidak dijual kerana rejim.
- SLOT 8 (utama) dan 10 (sekunder).

## 3. Lengan (tepat; tiada penambahan selepas melihat keputusan)

| Lengan | Teras | Satelit | Urutan | Rejim | Had industri | Benih |
|---|---|---|---|---|---|---|
| `K0` | 35% | tiada (tunai 65%) | – | – | – | 1 |
| `K1` | **50%** | tiada (tunai 50%) — "belanja 15% itu pada indeks" | – | – | – | 1 |
| `S1` **utama** | 35% | GB02_atau3 15% | U08 | ON sahaja | 1 | 1 |
| `S2` ablasi rejim | 35% | GB02_atau3 15% | U08 | tiada | 1 | 1 |
| `S3` ablasi urutan | 35% | GB02_atau3 15% | U01 | ON sahaja | 1 | 20 |
| `S4` ablasi industri | 35% | GB02_atau3 15% | U08 | ON sahaja | tiada | 1 |
| `R1` kawalan | 35% | RAWAK 15% | U01 | ON sahaja | 1 | 20 |
| `R2` kawalan tentu | 35% | RAWAK 15% | U08 | ON sahaja | 1 | 1 |

Setiap lengan satelit dijalankan pada slot 8 dan 10. Jumlah: 2 + 6 × 2 lengan-slot = 14 sel,
90 larian simulasi. Satu laluan ekuiti 2011–2025 setiap larian; tingkap **TAHAN 2020–2025**
(keputusan) dan **LATIH 2012–2019** (semakan) diukur sebagai segmen laluan itu, diasas semula
pada sesi pertama segmen.

## 4. Gate — ditetapkan sekarang (sel utama `S1` slot 8; median benih bila ada benih)

- **P1 nilai tambah:** CAGR `S1` > CAGR `K1` pada **kedua-dua** tingkap.
- **P2 risiko:** MDD `S1` tahan ≥ **-10.0%** DAN MDD `S1` ≥ MDD `K1` − 1.0 mata pada kedua-dua
  tingkap.
- **P3 lawan rawak:** CAGR `S1` tahan > persentil-95 CAGR `R1` (20 benih) DAN > CAGR `R2`.
- **P4 nisbah:** CAGR ÷ |MDD| `S1` > `K1` pada kedua-dua tingkap.
- **P5 setiap dagangan:** purata pulangan bersih dagangan satelit `S1` > 0 pada kedua-dua tingkap
  DAN > median benih purata dagangan `R1` (tahan).
- **LULUS** = P1–P5 kesemuanya pada slot 8. Slot 10 dilapor; "kukuh" jika lulus juga.

Jika LULUS: daftar untuk jejak langsung mengikut prosedur `CLAUDE.md` (skrip
`WFO/kaedah_baru/step2_<ID>.py`, `kod/registry/<ID>.csv`, baris `registry_M_gabung.csv`, db,
katalog), **selepas** semakan kod oleh sub-agen konteks baharu. Jika GAGAL: satelit kekal 0%,
pelan §9 `FABLE_PENILAIAN.md` tidak berubah, dan kebenaran kajian tunggal ini dianggap
terbelanja.

## 5. Diagnostik yang direkod (bukan gate)

Pendedahan satelit purata, bilangan dagangan, pusingan setiap slot setahun, kos setahun, pulangan
setiap dagangan ikut rejim pada hari masuk (ON/OFF, daripada `S2`), kadar menang bersama untung
purata dan rugi purata dan payoff, `tanpa5`, hari pegang, pulangan `S1` dikecilkan ke MDD -10%
(pendedahan × min(1, 10 ÷ |MDD|)), campuran SPUS bulanan + tunai 2020–2025 (35% dan 50%).

## 6. Ujian asap WAJIB sebelum keputusan dibaca (`--asap`)

1. `K0` dengan `W_SAT = 0` memberi laluan yang sama dengan teras-sahaja analitik (beza < 0.05%).
2. Setiap dagangan satelit: indeks keluar > indeks masuk; harga keluar diambil daripada ticker
   yang SAMA (`P.O[ti, k]`), bukan ticker lain; paras Chandelier pada bar masuk < harga masuk
   pada 100% dagangan (pepijat `X25`); tiada dagangan dengan hari pegang 0.
3. 50 dagangan rawak dikira semula secara bebas daripada panel harga mentah (buka→buka, kos
   penuh) dan mesti sepadan dengan rekod (beza < 1e-6).
4. Tunai tidak pernah negatif; ekuiti tidak pernah ≤ 0; bilangan posisi satelit ≤ slot setiap
   hari; tiada dua posisi dalam industri sama bila had = 1; tiada belian satelit pada sauh rejim
   OFF bagi lengan rejim.
5. Ujian asap mesti BOLEH gagal: skrip menyemak dengan sengaja satu kes rosak (paras henti dipaksa
   di atas harga masuk) dan mesti melaporkannya sebagai gagal.
Mana-mana ujian gagal → keputusan tidak dilaporkan; kod dibetulkan dan larian diulang.

## 7. Jangkaan priori — ditulis sebelum larian (rekod: salah majoriti pada ruang belum diukur)

1. **P2 lulus** pada tahan: satelit 15% dengan MDD satelit ~-40% menyumbang ~-6 mata, tetapi
   rejim ON memotong pendedahan dalam 2022; MDD akaun -9% hingga -12%. Saya jangka **lulus nipis**.
2. **P1 gagal pada latih, lulus pada tahan**: SPY 2012–2019 kuat dan satelit 2012–2019
   (`cagr_latih` `PEGANG_SLOT.md` ~10–13%) tidak mengalahkannya pada 15% berat selepas kos.
3. **P3 lulus** (isyarat GB02 mengalahkan rawak pada 8 slot dalam setiap ujian repo).
4. **P5 lulus** (jangkaan setiap dagangan GB02 × X15 +6.9% tahan).
5. **Keputusan keseluruhan: GAGAL pada P1 latih**; pelan §9 tidak berubah.

## 8. Apa yang larian ini tidak boleh buktikan

Alam A02 tiada saham delist (CAGR satelit condong ke atas); kolam GB02 dan X15 dipilih daripada
data yang sama; proksi teras SPY bukan SPUS; `CARA` kekal `C01`; tiada impak pasaran dalam kos;
tingkap tahan satu rejim teknologi dominan. Tiada dakwaan +10%/bulan.
