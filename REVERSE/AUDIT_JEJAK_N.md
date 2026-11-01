# AUDIT_JEJAK_N — audit bebas jejak Nxx, 1 Nov 2026

Dijalankan sebagai workflow 6-lensa; setiap agen membaca CSV/kod sumber, **bukan** dokumen
yang ditulis oleh pembantu yang dinilai. Setiap dapatan disangkal oleh 3 skeptik dari sudut
berbeza; hanya yang bertahan ≥ 2/3 undi disenaraikan. **17 bertahan · 19 disangkal.**
119 agen dirancang, 58 siap — 61 gagal pada had penggunaan 5 jam, jadi lensa `proses`,
`tolak` dan `terima` tiada penyangkalan dan sintesis/hakim tidak berjalan. Dapatan lensa itu
disenaraikan di bawah sebagai **BELUM DISANGKAL**, bukan sebagai disahkan.

Keluaran mentah setiap lensa: `REVERSE/audit_mentah/`.

## FATAL — disahkan sendiri terhadap fail sumber

**F1. Penyebut BH-FDR dikecilkan kepada 8 pada ujian yang memutuskan.**
`M_PRADAFTAR` = 358 (step18) · 349 (step19) · 14 (step20) · **8** (step21:24). Dengan 8 baris
dan m=8, ambang BH pada pangkat 8 = 0.05×8/8 = 0.05 → gate2 setara **p < 0.05 tanpa
pembetulan**; 8/8 lulus. Mengumpul ujian pada panel yang sama (≈346 unik selepas membuang 2
pendua `gabungan`↔`silang_akhir`) meletakkan p = 0.006803 pada pangkat 32, ambang BH 0.00462
→ **GAGAL**; ambang step-up berkumpul ialah p ≤ 0.00261. Nota penyangkal: verdict ini
**tidak monoton** dengan saiz kolam — step19+20+21 sahaja (68 ujian) masih lulus; yang
mematahkannya ialah memasukkan 280 ujian MASUK step18.

**F2. Asimetri yang tidak boleh dipertahankan.** Panel, tingkap, keluar, penganggar sama:
`N19 × X13` p = 0.003576 → `gate2 False` (m=349); `GB02_atau3 × X13` p = 0.006803 →
`gate2 True` (m=8).

**F3. gate3 dilonggarkan pada langkah yang sama.** step18:492 dan step19:274 =
`gate2 & (tanpa5_tahan > 0)`; step21:126 = `gate2 & (tanpa5 > asas5)`.

**F4. "satu-satunya yang lulus gate0–gate3" salah.** 8 daripada 12 baris `silang_akhir.csv`.

**F5. "satu-satunya dengan tanpa5 positif" salah tiga kali.** `GB02_atau4 × X13` = +2.8825 >
+2.8577 yang dipetik; `ASAS × X13` = +0.9118 (positif); dan `tanpa5` pada X13 hanya dikira
untuk 3 baris, jadi `N19 × X13` (jangkaan +11.2855, p 0.003576 — kedua-duanya lebih baik)
**tidak pernah diukur untuk ekor**.

**F6. 15 daripada 20 kohort tiada ujian pariti dalam CI.** `test_topeng_identik` meliputi
`N19 N20 N37 N115 GB02 X13` sahaja. Audit menyemak 15 yang lain sendiri dan mendapati
**betul** — jadi ini jurang liputan ujian, bukan pepijat ketepatan.

## MAJOR

**M1. Lorong 2 produksi BUKAN `X15` kajian.** `keluar_lorong.atr()` = purata mudah bergulir;
kajian = Wilder. Produksi mengira ATR semula setiap bar; kajian membekukannya pada bar
isyarat. Dakwaan "bit untuk bit" ditarik balik.

**M2. `N16`/`N17`/`N75` dinaikkan tanpa ujian signifikan atau ekor.** `nxx_x13.csv` tiada
lajur `p`, `gate` atau `tanpa5`. Pada setiap keluar yang ekornya pernah diukur, ketiga-tiganya
**gagal** gate3.

**M3. Model kos produksi ≈ 1/3 kos kajian**, dan alam produksi lebih sempit — jadi +8.541%
tidak boleh dibandingkan terus dengan lejar.

**M4. Justifikasi pemeringkat `U14` salah.** "Setiap pemenang E6a memakainya": sebenarnya
U14 = 11, **U01 (rawak) = 8**, U02 = 0 daripada 19 sel. Dan perbandingan "16.12 lawan 11.93"
membandingkan **dua masuk berbeza**; `U14` tiada dalam `portfolio_n_ringkas.csv` sama sekali.

**M5. `N75` bukan jangkaan mutlak tertinggi** — ia **ke-7** daripada 65 (N124 9.66 · N19 6.21
· N37 4.69 · N50 4.47 · N115 4.34 · N20 4.21 · N75 4.18).

**M6. Jangkaan priori #4 sudah dipalsukan sebelum ditulis.** `N19` (bb<0 **DAN** rsi14<30)
lift +3.6179 lawan `N73` (bb<0 sahaja) +0.8891 — penapis menambah **+2.73 mata**, bukan
merugikan.

**M7. Jangkaan priori #3 sudah dipalsukan sebelum ditulis.** `GB02_atau3 × X13` +8.5413 <
purata kaki pada X13 (9.3975).

**M8. Julat portfolio salah dan membingkaikan semula.** "CAGR 9.3–16.1%": julat sebenar
24 baris GB02 ialah **+2.76% hingga +29.28%**, dan `GB02_atau4,40,X15,U02` = **+29.28%**,
**di atas** SPUS 17.95%. Nombor yang dipetik ialah subset X13 sahaja (8.83–16.12).

**M9. "P3 lulus 4/6 sel" salah** — ia 5/6 (10 daripada 12 baris).

**M10. "21 positif / 44 negatif" ialah lajur X3 sahaja**, dipakai sebagai sifat 65 topeng.
Pada mana-mana keluar: 25 positif / 40 negatif. Pada keluar produksi X13, **61 daripada 65
topeng tidak pernah diukur**.

**M11. Seksyen kos bercanggah ~2.3× dengan dirinya sendiri** (70/215/267 MB lawan aritmetik
30.0/78.0/97.5 MB daripada input yang sama; §12c kemudian beri 31 MB).

**M12. `bertindih_kelompok.csv` yang dikomit tidak boleh dihasilkan pada ambang 0.5 yang
didokumenkan** — ia sepadan ambang ≈0.6 (55 kelompok, bukan 52).

## MINOR / KOD

- `_nxx.pasang()` memanggil `indikator()` **kali kedua** — menggandakan kos CPU termahal.
- `rank = -9e9` ditulis ke `isyarat/*.csv` sebagai **data**, bukan nilai hilang.
- `test_nxx_sepadan.py` menjalankan **9 daripada 11** ujian bila dijalankan terus —
  `unittest.main()` diletak sebelum kelas kedua ditakrif.
- Kawalan regresi "|Δ| = 0.00e+00" tidak boleh dihasilkan daripada artifak dikomit (deltanya
  1e-6…2.2e-5) kerana `nxx_x13.csv` ditulis `float_format='%.4f'`.
- `N62` membandingkan `julat20` (**peratus**) dengan `0.08 × harga dolar` — ambangnya
  bergantung harga saham. (Setia kepada topeng kajian, tetapi bermakna kawalan itu penapis
  paras harga.)
- Lift kawalan negatif yang dipetik ialah nilai X3 = keluar **terburuk** setiap kawalan; pada
  X1 susunan terbalik dan `N62` menjadi **terbaik**.
- `N118` dan `N15` melepasi gate1 **hanya** pada sel yang jangkaan mutlaknya negatif — tepat
  peraturan pengecualian yang dipakai untuk membuang `N16 × X1`.
- `kelompokkan()` bukan pautan-lengkap; ia penutup klik tamak bergantung susunan input.
- `u14()` tidak mengapit indeks seperti `step27.skor_pangkat` (`max(0, a-252)`), jadi 252 bar
  pertama = −9e9.
- Komposisi §12 tidak menjumlah: 4+4+7 = **15** "berbukti", bukan 16.
- `N124` bukan paling jarang antara 65 (`N65` = 6,537 < 12,728).
- Syarat TARIK BALIK §5 masih merujuk **"lima kohort"** selepas skala naik ke 20.
- `strategi.py` — sumber kebenaran keadaan dan penjaga hanyutan CI — tiada **satu** rujukan
  kepada step30, step31, `nxx_x13.csv` atau spec ini, dan `--semak` keluar 0.
- `CLAUDE.md` hanyut dalam jam yang sama ia ditulis: menamakan **5** modul Nxx; 20 wujud.
- Nombor ujian asap dan larian sandbox tiada artifak dikomit — hanya teks dalam .md.

## Yang audit SAHKAN sebagai betul

- Lapisan terjemahan **bersih**: 22 lajur indikator + 20 topeng bit-identik dengan
  `REVERSE/teras/ind.py` + `step18_nxx.tambahan()`, maks |Δ| < 1e-9, 0 bar berbeza.
  Disemak **sendiri** oleh audit, lebih luas daripada ujian repo.
- **Tiada kebocoran masa hadapan.** `stop = NaN` benar-benar menjadikan henti mustahil
  (`enjin.py:31` `sp = -inf`).
- `hampir()` selamat pada setiap panjang bingkai 1–253; 0 pengecualian pada 20 modul.
- Disiplin pradaftar **mekanikal** dipegang: spec tambah-sahaja (0 baris dibuang), peraturan
  keputusan dikomit 03:58:31, kod ukuran 03:59:13, keputusan 04:23:51; `step30` tidak disunting
  selepas komit pradaftarnya; §10 **membatalkan** dakwaan pembantu sendiri tentang kependuaan.
- Kebanyakan transkripsi terus CSV tepat, termasuk kesemua 10 metrik §3, kesemua 36 nilai §9,
  "598/598 setup negatif", dan "52/65 · 42/65".

## Had audit ini

61 daripada 119 agen gagal pada had penggunaan. Lensa `proses` (16 dapatan), `tolak` dan
`terima` tiada penyangkalan — dapatannya di atas ditanda dari `proses` dan **belum disangkal**.
Sintesis 3-framing dan hakim akhir tidak berjalan. Audit perlu dijalankan semula selepas had
ditetapkan semula untuk melengkapkan tiga lensa itu.
