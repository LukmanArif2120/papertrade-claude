# SPEC — Jarak ke tinggi 52 minggu (pradaftar)

Status: **PRADAFTAR**. Spec dan kod (`REVERSE/step40_52w.py`) dikomit **sebelum** sebarang
keputusan dilihat. Permintaan pengguna 4 Nov 2026: "Near 52WK high, perlu kita add dalam posisi
ke? sejauh mana sebelum 52wk high? dalam table format tu."

Keputusan pengguna pada soalan penjelasan (4 Nov 2026):
1. Yang diminta ialah **lajur dashboard sahaja** (paparan), bukan peraturan beli, bukan piramid.
2. Skop data **A02 penuh 2012–2025**.
3. Paksi ujian: **band + urutan** (bukan penapis `DAN` sahaja).

## 1. Hipotesis

`j52` = jarak tutup dari tinggi 252 sesi sebelumnya membawa maklumat tentang pulangan hadapan,
sebagai (a) **band mutlak** (sejauh mana di bawah tinggi 52w) dan (b) **urutan keratan rentas**
(susun calon ikut `j52`).

Sebab ia layak diuji walaupun `SETUP.md` sudah ukur 0/598 penapis dengan lift positif: paksi
URUTAN **tidak** membuang bar, dan `SISTEM.md` ukur bahawa urutan ikut skor berterusan ada
sebaran benih 0.00 mata. Yang sudah diuji dan GAGAL ialah bentuk penapis keras: `N35`
(`breakout_52w`, lift −0.097/−0.223), `N66` (tutup > 1.01×tinggi_52w, −0.184/−0.308), `N65`
(gap + hampir 52w, −0.008/−0.110), `N120` (Minervini termasuk ≥0.75×tinggi_52w, −0.087/−0.097).
Tiada satu pun daripada empat itu mengukur **band berperingkat**, jadi soalan "sejauh mana"
belum pernah dijawab.

## 2. Data

- Harga: Release `autotune-data-a02` (`AUTOTUNE/.cache_autotune-data-a02/harga_YYYY.parquet`),
  3,260 ticker. Lookback dimuat dari 2009.
- Tingkap: **LATIH 2012–2019**, **TAHAN 2020–2025** (sama seperti step17/step18).
- Bar cair sahaja: median nilai dagangan 20 hari ≥ USD100,000 (`CAIR`, sama seperti step18).
- Kos: komisen 0.1% + slippage ikut `REVERSE/teras/kos.py`, kedua-dua sisi.

**KAVEAT ALAM (mengikat setiap nombor):** alam A02 **tiada saham delist** dan `KEPUTUSAN_AKHIR.md`
§(4) ukur 0 daripada 3,180 ticker panel tamat sebelum 2025-12-01. Band "jauh di bawah tinggi 52w"
ialah band yang paling terjejas oleh bias ini kerana saham yang jatuh 40% dan kemudian mati
tiada dalam alam. Maka **bias menyanjung band jauh**, bukan band hampir. Kesimpulan yang
menyebelahi band jauh tidak boleh dipercayai; kesimpulan yang menyebelahi band hampir tidak
dilemahkan oleh bias ini.

## 3. Penunjuk (dikunci)

- `tinggi_52w = high.rolling(252, min_periods=200).max().shift(1)` — **sama baris** seperti
  `REVERSE/step18_nxx.py:61` supaya nombor boleh dibanding terus dengan `N35`/`N65`/`N66`/`N120`.
- `j52 = (tutup / tinggi_52w − 1) × 100`. Positif = di atas tinggi 52w lama.
- Varian kekukuhan `j52c` = `ind.py` `j_52w_tinggi` (tinggi 252 sesi atas **tutup**, termasuk hari
  ini, jadi selalu ≤ 0). Dilaporkan sebagai lajur kedua supaya kesimpulan tidak bergantung
  pada konvensyen.
- **Ujian pariti wajib**: `tinggi_52w` saya mesti bit-identik dengan `step18_nxx.tambahan()` dan
  `j52c` dengan `ind.kira()` pada sampel ticker. Jika gagal, larian dibatalkan.

## 4. Band (dikunci, 8)

`[0, ∞)` · `[−2, 0)` · `[−5, −2)` · `[−10, −5)` · `[−15, −10)` · `[−25, −15)` · `[−40, −25)` ·
`(−∞, −40)`

Asas = **semua bar cair** dalam tingkap yang sama dengan keluar yang sama (bukan band mana-mana).

## 5. Keluar (dikunci, 5)

| Kod | Peraturan |
|---|---|
| `H21` | pegang 21 sesi, jual buka; tiada henti, tiada sasaran |
| `H63` | pegang 63 sesi, jual buka |
| `H126` | pegang 126 sesi, jual buka (= ufuk `IMBAS` kajian) |
| `X13` | `rsi14 > 70` → jual buka esok; TMAX 126; **tiada henti** (lorong 1 produksi) |
| `X15` | Chandelier: tutup < tutup tertinggi sejak beli − 4×ATR14 → jual buka esok; TMAX 126 (lorong 2 produksi) |

Masuk pada **buka esok** (`C01`) pada setiap bar yang jatuh dalam band. `stop = NaN` pada
kesemua lima, jadi kecacatan henti hari-0 (`KOLAM_EKOR.md` §4a) **tidak** hadir.

## 6. Metrik

`n` · `menang%` · `untung` · `rugi` · `jangkaan` (min) · `tanpa5` (min selepas buang 5% teratas)
· `lift` = `jangkaan(band) − jangkaan(asas)` · `lift_tanpa5` = `tanpa5(band) − tanpa5(asas)`.

## 7. Gate (dipradaftar; TAHAN yang memutuskan)

- **gate0** `n ≥ 200` dalam kedua-dua tingkap.
- **gate1** `lift > 0` dalam **kedua-dua** LATIH dan TAHAN.
- **gate2** `p` satu hujung bagi (band − asas) dengan SE **berkelompok ikut hari beli**, lulus
  BH-FDR `q = 0.05` dengan penyebut **dipradaftar `m = 40`** (8 band × 5 keluar). Penyebut jujur
  ditulis di sini supaya kecacatan `m=8` yang `AUDIT_JEJAK_N.md` dedahkan tidak berulang.
- **gate3** `jangkaan` mutlak > 0 dalam TAHAN **DAN** `lift_tanpa5 > 0` dalam TAHAN. Dua-dua,
  kerana `NXX.md` tangkap `N16×X1` lulus lift atas asas NEGATIF (merugikan walaupun lift positif).
- **gate4 (urutan)** min IC harian (Spearman `j52` lawan pulangan hadapan) bertanda **sama**
  dan `|t| ≥ 2` dalam kedua-dua tingkap, DAN kemonotonan desil `|rho| ≥ 0.7`.

Gate1–gate3 menilai band; gate4 menilai urutan. Kedua-duanya dilaporkan walau apa pun hasil.

## 8. Keputusan lajur dashboard

Lajur `jarak 52w` dalam jadual Posisi/Watchlist diterbitkan **tanpa mengira** hasil gate (ia
paparan, keputusan pengguna). Tetapi laporan mesti menyatakan hasil ukuran, dan jika gate gagal
lajur itu dilabel **paparan sahaja — bukan peramal**, sama seperti lajur Trend dan Stage.

## 9. Jangkaan priori saya (ditulis sebelum larian)

Rekod: jangkaan priori saya SALAH pada 2/3 gate dalam tiga pradaftar berturut-turut
(`SPEC_SILANG` §7, `SPEC_SISTEM` §7, `SPEC_NXX` §7).

1. Band **tidak** monoton. Saya jangka band `[0, ∞)` dan `[−2, 0)` **tidak** terbaik pada
   jangkaan mutlak 126 sesi.
2. Band jauh (`[−40, −25)`, `(−∞, −40)`) menunjukkan jangkaan mutlak **tertinggi** tetapi
   `tanpa5` paling negatif — iaitu kelebihan hidup dalam ekor kanan, dan sebahagiannya artifak
   tiada-delist (§2).
3. IC harian **positif tetapi kecil** (`|IC| < 0.02`) dan tidak stabil merentas dua tingkap.
4. Ramalan berangka: **0 daripada 40 sel lulus kesemua gate0–gate3**, dan **gate4 gagal**.

## 10. Apa yang akan menukar verdict

Jika band `[0, ∞)` atau `[−2, 0)` menunjukkan `lift > 0` pada **kedua-dua** tingkap DAN
`lift_tanpa5 > 0` pada TAHAN, itu ialah struktur sebelah MASUK yang **pertama** bertahan ujian
ekor dalam seluruh kajian, dan jarak 52w layak didaftar sebagai paksi **URUTAN** (`U13`+),
bukan penapis. Jika hanya gate4 lulus, ia paksi urutan tanpa band — lajur dashboard kekal
paparan dan `REVERSE/strategi.py` dikemas dengan satu baris gilir urutan.

## 11. Syarat BERHENTI

Satu larian. Tiada penalaan band, tiada penambahan keluar selepas keputusan dilihat. Jika
ujian pariti §3 gagal, larian dibatalkan dan tiada nombor dilaporkan.
