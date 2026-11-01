# SPEC MOMENTUM_PEGANG fasa 2 — Pradaftar: top-N, paksi PEGANG, grid pattern × keluar

Ditulis 1 Nov 2026, **sebelum** apa-apa keputusan fasa 2 dilihat. Permintaan pengguna selepas membaca
`REVERSE/MOMENTUM_PEGANG.md` §8f: tutup jurang **A**, **C** dan **D**.

Fasa 1 (`MOMENTUM_PEGANG.md`) mendapati 5 pattern lulus gate pada **desil** (10% alam), tetapi audit menunjukkan
tiga lubang yang menjadikan dapatan itu belum boleh didagangkan. Fasa 2 menutup tiga lubang itu.

## 0. Pembetulan yang DIWARISI daripada fasa 1 (wajib, bukan pilihan)

Setiap larian fasa 2 mesti memakai kesemua enam pembetulan audit fasa 1:
1. `TANGKAP` guna `nan_to_num(...)>0.5`, **jangan** `.astype(bool)` pada float ber-NaN.
2. Baris `kod==2` (posisi belum pernah keluar pada hujung data) **dibuang** daripada semua `r2`/`hari`/`TANGKAP`.
3. Baris yang **feature**-nya NaN dibuang daripada **kedua-dua** kumpulan (topeng 3-keadaan 1/0/NaN).
4. Setiap ukuran dilapor **per dagangan DAN per bulan pendedahan**. Dakwaan hanya dibuat atas per-bulan.
5. Sauh ufuk TB terpotong (`bar_ufuk<120`) dibuang daripada pengiraan `P(TB)`.
6. Kiraan FDR dilapor eksplisit; pattern bertopeng kosong dilapor, bukan lesap senyap.

Tambahan fasa 2: **ujian signifikan utama ialah bootstrap blok-bergerak 120 sesi** (300 cabutan, CI95), bukan
SE berkelompok. Sebab: fasa 1 §8c mengukur bahawa kelompok bulan × ticker memberi SE terlalu kecil kerana ufuk
hasil melebihi blok masa. SE berkelompok dua hala dilapor sebagai rujukan sahaja.

## 1. LEG A — top-N setiap hari, bukan desil

**Masalah:** gate fasa 1 mengukur desil = 441,412 sauh = 10% alam. Pengguna ada 8–10 slot, jadi yang dibeli
ialah ~8 sauh **teratas** setiap tarikh = ~0.3% ekstrem. Fasa 1 §2f mengukur bahawa di kawasan ekstrem itu
urutan momentum **kalah kepada rawak** (pangkat #1 `roc60` = −10.26% lawan asas +1.884%). Jadi lulus gate pada
desil **tidak** bermakna boleh didagangkan.

**Reka bentuk:** bagi setiap lorong di bawah, susun sauh dalam setiap tarikh mengikut skor yang dinyatakan,
ambil **N teratas**, dan ukur. `N ∈ {8, 10, 20, 40}`.

| Lorong | Skor susunan (dibekukan) |
|---|---|
| `S3` RS SPY 6b | `rs_spy_6b` menurun |
| `H1` Qullamaggie | antara sauh yang memenuhi syarat, `roc60` menurun |
| `H2` Minervini | antara sauh yang memenuhi syarat, `roc60` menurun |
| `D1` `vol_n50 ≥ 1.5` | antara sauh yang memenuhi syarat, `vol_n50` menurun |
| `S1` roc60 (rujukan) | `roc60` menurun |
| `S2` roc60÷ATR% Clenow (rujukan) | `roc60/atr_pct` menurun |
| `S6` gabungan pangkat (rujukan) | skor gabungan menurun |
| **`RAWAK` (kawalan)** | **urutan rawak, 20 benih** |

`S4` hampir-tinggi-52w **D8 DIKELUARKAN daripada leg A** dan sebabnya ditulis awal: D8 ialah baldi **tengah**
(persentil 0.70–0.80), jadi "N teratas" tidak tertakrif untuknya. Memaksa takrif (cth N terdekat kepada
persentil 0.75) akan menjadi ukuran yang direka selepas melihat data. Ia kekal sebagai dapatan desil sahaja.

**Gate A (dibekukan):**
- **A0** Setiap lorong mesti ada ≥ 1,000 dagangan pada setiap `N` dalam setiap tingkap.
- **A1** Pulangan **per bulan** lorong > **persentil 95** jalur `RAWAK` 20 benih pada `N` yang **sama**, pada
  **kedua-dua** tingkap. Ambang jalur (bukan beza dua titik) kerana `KEPEKATAN_BENIH.md` mengukur hingar
  pemilihan 17.3 mata peratus setahun pada 8 slot.
- **A2** CI95 bootstrap blok bagi (lorong − purata RAWAK) tidak merangkumi sifar pada tingkap TAHAN.
- **A3** `TANGKAP` per bulan ≥ `TANGKAP` per bulan `RAWAK` pada `N` yang sama.
- **Diagnostik (bukan gate):** median, `p5`, pecahan dagangan `r2 < −50%`, `P(TB)`, hari.

**Jangkaan priori saya:** **tiada lorong lulus A1 pada N = 8**, dan sekurang-kurangnya satu lulus pada N = 40.
Sebabnya struktur: fasa 1 §2f menunjukkan kemerosotan monotonik ke arah pangkat #1, dan N kecil mendedahkan
lebih banyak kepada hujung itu. Jika `S3` lulus pada N = 8 saya salah, dan itu akan jadi dapatan paling boleh
guna dalam seluruh kajian.

## 2. LEG C — paksi PEGANG: peraturan selepas masuk

**Masalah:** fasa 1 §3 mengukur `P(TB)` dan pulangan **BERSYARAT** pada pulangan 3 hari pertama (+5% dalam
3 hari → `P(TB)` 34% → 60%). Itu **bukan strategi** — ia statistik bersyarat yang memerlukan pengetahuan masa
hadapan untuk dilaksanakan sebagai penapis masuk. Fasa 2 menukarnya kepada **strategi penuh** di mana cabang
"potong" benar-benar merealisasikan kerugiannya.

**Reka bentuk (dibekukan).** Masuk pada `o[k]` seperti biasa. Pada **tutup bar k+2** (hari dagangan ke-3):
- Jika `c[k+2]/o[k] − 1 <= ambang` → **jual pada `o[k+3]`**. Pulangan = `o[k+3]/o[k]×(1−kos)/(1+kos) − 1`, hari = 4.
- Jika `> ambang` → **teruskan** sampai keluar lorong 2 biasa.
- Jika lorong 2 **sudah** keluar pada atau sebelum `k+2` (`j_keluar <= k+2`), peraturan tidak terpakai dan
  hasil lorong 2 digunakan seperti adanya. Bilangan kes ini dilapor.

Ambang: `{0%, +3%, +5%}`. Juga satu varian tempoh: semakan pada **k+4** (hari ke-5) dengan ambang `+5%`.
Asas pembanding: **pegang semua** (lorong 2 tulen, tiada peraturan).

**Gate C (dibekukan):**
- **C0** ≥ 100,000 sauh setiap sel dalam setiap tingkap.
- **C1** Pulangan **per bulan** strategi komposit > pulangan per bulan asas, pada **kedua-dua** tingkap.
- **C2** CI95 bootstrap blok bagi (komposit − asas) tidak merangkumi sifar pada TAHAN.
- **C3** Pulangan mutlak komposit **> 0**.
- **C4** `TANGKAP` per bulan komposit ≥ asas (peraturan tidak boleh memotong trend besar).
- **Diagnostik:** pecahan dagangan dipotong, pulangan purata cabang potong, pulangan purata cabang pegang,
  `P(TB)` setiap cabang, kos tambahan (potong = satu dagangan tambahan, 0.2% pulangan perjalanan).

**Jangkaan priori saya:** **C1 lulus tetapi C4 gagal.** Mekanismenya: memotong pada hari ke-3 membuang
dagangan yang akhirnya jadi trend besar tetapi bermula perlahan, dan `KOLAM_EKOR.md` mengukur bahawa 5%
teratas membawa 63.7% pulangan. Saya menjangka purata bertambah baik dan ekor rosak. Jika kedua-duanya lulus,
ini akan jadi perubahan paling besar yang pernah diukur dalam repo.

## 3. LEG D — grid pattern × parameter keluar

**Masalah:** fasa 1 membelanjakan 258 ujian pada paksi MASUK sambil membekukan paksi KELUAR pada `ganda = 4`,
dan §8d kemudian mengukur bahawa parameter keluar **1.8× lebih berpengaruh** daripada pattern masuk terbaik.
Paksi yang lebih berkuasa tidak pernah disapu bersama pattern, jadi **interaksi** tidak diketahui.

**Reka bentuk:** 5 pemenang fasa 1 + `ASAS` (tiada pattern) × `ganda ∈ {2, 3, 4, 6}` = **24 sel**, pada alam
A02 penuh, dua tingkap. Soalan utama bukan sel mana terbaik, tetapi **adakah ada interaksi**: apakah ganda
optimum bagi setiap pattern sama dengan ganda optimum asas (4×)?

**Gate D (dibekukan):**
- **D0** Setiap sel ≥ 50,000 sauh setiap tingkap.
- **D1** Terdapat sekurang-kurangnya satu (pattern, ganda) dengan pulangan per bulan > **sel terbaik baris
  `ASAS`** pada **kedua-dua** tingkap.
- **D2** CI95 bootstrap blok bagi (sel terbaik − `ASAS` pada ganda yang sama) tidak merangkumi sifar.
- **D3 (interaksi)** Ganda optimum bagi sekurang-kurangnya satu pattern **berbeza** daripada ganda optimum
  `ASAS`, dan perbezaannya bertahan pada kedua-dua tingkap.
- **Diagnostik:** matriks penuh 24 sel per-bulan dan per-dagangan; hari dipegang setiap sel.

**Jangkaan priori saya:** **D1 lulus (trivial, kerana pattern menambah lift pada mana-mana ganda) tetapi D3
GAGAL** — saya menjangka ganda optimum ialah 4× bagi setiap pattern, kerana ganda mengawal **bila** keluar
manakala pattern mengawal **apa** dibeli, dan tiada mekanisme yang saya boleh namakan untuk menjadikan kedua-dua
pilihan bergantung. Jika D3 lulus, ia bermakna ekor pattern berbeza bentuk daripada ekor asas, dan itu akan
mengubah cara repo menala lorong 2.

## 4. Kiraan FDR

Leg A: 7 lorong × 4 nilai `N` = 28. Leg C: 4 peraturan = 4. Leg D: 6 baris × 4 ganda = 24, tolak 4 sel `ASAS`
yang menjadi pembanding = 20 ujian. **Jumlah 52 ujian**, dan BH-FDR dikira atas 52 merentas ketiga-tiga leg
bersama (bukan setiap leg berasingan).

## 5. Had yang diketahui (ditulis awal)

- Bias penyintas A02 kekal (88.5% ticker hidup hingga hujung data); setiap nombor ialah had ATAS.
- Alam kajian ≠ alam dagangan Syariah; fasa 1 mengukur **74.3%** keuntungan datang daripada saham di luar
  alam SPUS. Leg A–D **tidak** membetulkan ini, dan ia **bukan** jurang yang pengguna pilih untuk ditutup.
- Leg A memodelkan pemilihan slot tetapi **bukan** portfolio penuh: tiada had tunai, tiada had korelasi,
  tiada imbangan semula. Ia menjawab "adakah N teratas lebih baik daripada rawak", bukan "berapa CAGR".
- Paksi CARA kekal `C01` (beli pada buka esok).
- Leg C menambah satu dagangan bagi cabang potong; kos 0.1% setiap belah dimodelkan, slippage tidak.
- `S4` dikeluarkan daripada leg A (§1) dengan sebab bertulis.
