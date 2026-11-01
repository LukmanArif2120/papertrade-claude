# SPEC_GRID_PENUH — grid penuh MASUK × KELUAR, dan senarai TOP-40 untuk papertrade

**Dikomit SEBELUM larian.** Permintaan pengguna: "entry hold dan exit yang terbaik —
mungkin top 30 ke, atau top 40 ke."

## 1. Mengapa ini perlu dan mengapa ia bukan eksperimen baharu

Grid yang diukur sampai sekarang **jarang**, dan itu punca setiap masalah yang
`AUDIT_JEJAK_N.md` temui:

| sudah diukur | bentuk | sel |
|---|---|---:|
| `nxx.csv` | 65 masuk × 4 keluar asas (`X1`–`X4`) | 260 |
| `nxx_keluar.csv` | 3 masuk × 23 keluar | 69 |
| `nxx_x13.csv` | 4 masuk × 1 keluar | 4 |
| `silang_akhir.csv` | 2 masuk × 4 keluar | 8 |

Jadi **"kombinasi masuk×keluar yang terbaik" belum pernah dikira.** `X13` ialah keluar
terbaik yang diukur, tetapi hanya 4 daripada 65 masuk pernah diuji dengannya — dan
**61 daripada 65 masuk tidak pernah diukur pada keluar produksi sama sekali.**

Ini **bukan** eksperimen ketujuh dan bukan ruang baharu. Ia **melengkapkan grid yang sama**
dengan topeng yang sama, keluar yang sama, panel yang sama, tingkap yang sama dan model kos
yang sama. Kosnya hampir percuma kerana `pulangan_keluar()` sudah mengira kesemua 23 keluar
serentak setiap kelompok; menukar 3 masuk kepada 65 hanya menambah topeng boolean.

**Dan ia membetulkan kecacatan fatal audit secara langsung:** satu penyebut BH-FDR yang
jujur merentas **kesemua 1,495 sel**, bukan m=8 pada satu sudut grid.

## 2. Apa yang diukur

**1,495 sel** = 65 topeng MASUK berstatus `DIUJI` × 23 keluar `XSPEC`.
Panel, tingkap (LATIH 2012–2019 / TAHAN 2020–2025), ambang cair (`nilai20 ≥ 100k`),
`MIN_N = 200` dan model kos `teras/kos.py` **tidak berubah**.

Setiap sel: `jangkaan_latih`, `jangkaan_tahan`, `lift_latih`, `lift_tahan`, `menang`,
`untung`, `rugi`, `n`, `t`, `p` (SE berkelompok ikut hari beli), `tanpa5_tahan`.

**Nota tentang PEGANG:** paksi pegang **sebahagiannya sudah dalam** 23 keluar itu — `X29`
pegang tetap 10 bar, `X33` keluar pada tutup sesi masuk, dan setiap keluar bersyarat dihadkan
pada ufuk `IMBAS = 126` bar. Larian ini **tidak** menguji `TMAX` sebagai paksi berasingan;
itu larian kedua kalau diperlukan. Saya nyatakan ini supaya tiada dakwaan berlebihan.

## 3. Syarat WAJIB — ditetapkan sebelum melihat keputusan

Sel masuk senarai hanya jika **kesemua empat** benar:

1. **`jangkaan_latih > 0` DAN `jangkaan_tahan > 0`** — menguntungkan secara **mutlak** pada
   kedua-dua tingkap. Ini perangkap yang `CLAUDE.md` catat: `N16 × X1` ada lift +0.193 dan
   menang 62.4% tetapi jangkaan **−0.088%** kerana asasnya sendiri negatif.
2. **`lift_latih > 0` DAN `lift_tahan > 0`** — mengalahkan beli-setiap-bar pada kedua-dua
   tingkap.
3. **`n_tahan ≥ 200`** — sama seperti `MIN_N` kajian.
4. **`p` melepasi BH-FDR q ≤ 0.05 pada penyebut BERKUMPUL `m = 1,495`** — penyebut yang
   **jujur**, iaitu tepat apa yang `step21` gagal lakukan dengan m=8.

**Susunan: `jangkaan_tahan` menurun.**

**Had kepelbagaian:** maksimum **3 keluar setiap topeng masuk** dalam senarai akhir, supaya
40 slot tidak menjadi 2 masuk × 20 keluar. Sekurang-kurangnya **14 masuk berbeza** terjamin.

**`tanpa5_tahan` dilaporkan sebagai LAJUR, bukan gate.** Sebabnya audit: `gate3` menjadi
pemutus de-facto sedangkan ia anggaran titik telanjang tanpa ralat piawai, tanpa nilai p dan
tanpa kawalan pelbagai ujian. Ia maklumat penting — jadi ia dipapar pada setiap baris dan
disebut dalam keputusan — tetapi ia **tidak** menapis senarai secara senyap.

## 4. Kalau kurang daripada 30 lulus

Dilaporkan **tepat berapa yang lulus**, dan senarai diisi kepada 30 dengan **menggugurkan
syarat 4 (FDR) sahaja**, mengikut susunan `jangkaan_tahan`, dan setiap baris tambahan
**dilabel `TIADA_FDR`**. Syarat 1–3 **tidak pernah** digugurkan. Kalau kurang daripada 30
lulus syarat 1–3, senarai lebih pendek daripada 30 dan saya katakan begitu.

## 5. Jangkaan priori

1. **Antara 15 dan 60 sel** akan lulus kesemua empat syarat. Penyebut 1,495 jauh lebih ketat
   daripada m=8, tetapi `X13`/`X15`/`X17` pada masuk pembalikan min memberi p yang sangat
   kecil (`N19 × X13` p = 0.0036), jadi sebahagian akan bertahan.
2. **Keluar akan mendominasi senarai, bukan masuk.** Saya jangka `X13`, `X15`, `X17` memegang
   > 60% slot, kerana sebaran keluar 4.997 mata lawan lift masuk terbaik 0.392 mata.
3. **`N19 × X13` akan menduduki tempat pertama atau kedua** (+11.2855% sudah diukur).
4. **`GB02_atau3 × X13` TIDAK akan berada dalam 10 teratas** — +8.5413% lebih rendah daripada
   `N19` sendirian, jadi konfigurasi yang saya hantar ke produksi akan kelihatan sederhana.
5. **Keluarga RSI dan BB akan mendominasi**; `MA`, `TREND`, `KEKUATAN` akan hampir tiada.
6. **`tanpa5_tahan` akan NEGATIF pada majoriti senarai**, termasuk sebahagian daripada 10
   teratas. Kalau ia positif secara meluas, itu bercanggah dengan `SETUP.md` dan saya mesti
   mencari pepijat sebelum mempercayainya.

## 6. Apa yang larian ini TIDAK akan buktikan

- Prestasi **portfolio**. Ini jangkaan setiap dagangan. `KEPUTUSAN_AKHIR.md` sudah mengukur
  724 konfigurasi portfolio dengan T1 = 0.
- Alam kajian = `a02` tanpa delist; alam dagangan ditapis SPUS. Berbeza.
- 65 topeng itu dipilih daripada 147 oleh `status = DIUJI`, dan status itu ditetapkan oleh
  larian terdahulu. Jadi senarai ini **bersyarat** kepada pilihan itu.
- `p` berpemberat hari sama rata manakala `lift` berpemberat dagangan — audit menunjukkan
  tandanya boleh bertentangan. Kedua-dua lajur dipapar; jangan campur.
