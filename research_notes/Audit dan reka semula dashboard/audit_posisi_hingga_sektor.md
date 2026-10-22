# Audit tab Posisi, Watchlist, Backtest (Keputusan + Butiran), Kaedah, Sektor dan rangka global dashboard (versi 102 / artifact versi 107, 22 Okt 2026)

Konvensyen petikan: `html:N` = `BacktestShariah2/standard/dashboard_v2.html` baris N (490,841 bait, 3,521 baris); `md:N` = `BacktestShariah2/standard/dashboard.md` baris N; `log+:N` = `BacktestShariah2/standard/binaan_v2_log_tambahan.md` baris N. "db langsung" = bacaan ArtifactData (get/list sahaja) pada 22 Okt 2026 daripada https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e; saiz db = JSON padat dikira semula dengan skrip dalam scratchpad (bukan saiz cetak cantik yang dilapor alat). Tiada fail repo, artifact atau db diubah.

## S1. Inventori setiap tab: panel ikut susunan, dokumen db, keadaan lalai, kerumitan (desktop lawan telefon ≤ 760px)

### Takeaway
Lima tab ini sahaja memuatkan kira-kira 20 panel/sub-paparan, dengan tajuk, jalur KPI, tapisan dan kaki tersendiri bagi setiap satu. Jadual paling penting juga sangat besar dalam data langsung: Posisi C 4,240 baris, Keputusan 141 kaedah, Papan penuh sehingga 665 varian dengan 21 lajur, Watchlist 212 baris, Kaedah 134 baris dan Sektor 149 baris. Tab Posisi sendiri mempunyai empat pandangan jadual (8, 19, 11 dan 10 lajur), tiga akaun dan enam kawalan tapisan. Di telefon, semua pandangan itu diganti dengan satu jenis kad lipat.

### Cited Findings

**Tab Posisi** (`renderPos`, [html:1399–1424](../../BacktestShariah2/standard/dashboard_v2.html#L1399))
- Sub-tab akaun **Papertrade C / Moomoo lama / Gabung** dikongsi dengan Prestasi ([html:641–643](../../BacktestShariah2/standard/dashboard_v2.html#L641)). Lalai `c`, dan pilihan disimpan dalam `pbs3_akaun` ([html:646–650](../../BacktestShariah2/standard/dashboard_v2.html#L646)).
- Susunan paparan:
  1. Tajuk ayat ikut akaun ([html:1407–1410](../../BacktestShariah2/standard/dashboard_v2.html#L1407)). M: "Akaun simulasi Moomoo … tiada belian baharu sejak 13 Okt 2026", diikuti jalur "Sumber" (harian / warisan v1 / strategi luar 87 M). C: tarikh mula dan "harga pada".
  2. KPI 4 kad (`ptKpis`, [html:1356–1365](../../BacktestShariah2/standard/dashboard_v2.html#L1356)): Posisi, Purata untung, Purata ikut lorong keluar (Kaedah · Selagi naik) dan Sedang untung.
  3. Panel **Peta portfolio**: treemap sektor → industri bagi posisi dipegang; ketik untuk menapis jadual ([html:2912–2939](../../BacktestShariah2/standard/dashboard_v2.html#L2912)).
  4. Panel **Posisi & keputusan** ([html:1412–1414](../../BacktestShariah2/standard/dashboard_v2.html#L1412)). Kawalan: seg status Semua/Dipegang/Sudah keluar; seg pandangan Ringkas/Penuh/Risiko/Gred (desktop; `pbs3_pandangan`, [html:2940–2945](../../BacktestShariah2/standard/dashboard_v2.html#L2940)); pilih kaedah, sektor dan industri; carian (`ptFilterBar`, [html:1371–1375](../../BacktestShariah2/standard/dashboard_v2.html#L1371)). Susunan lalai ialah Untung % menurun. Desktop mula dengan 25 baris (+100 setiap "Papar lagi", "Papar semua" hanya jika ≤ 400); telefon mula dengan 10 (+25) ([html:1367–1370](../../BacktestShariah2/standard/dashboard_v2.html#L1367)).
  5. Panel **Isyarat tidak dibeli** (C sahaja, 6 lajur, dilipat secara lalai) ([html:1415–1418](../../BacktestShariah2/standard/dashboard_v2.html#L1415); `LIPAT_LALAI` [html:3385](../../BacktestShariah2/standard/dashboard_v2.html#L3385)).
- Bilangan lajur ikut pandangan:
  - Ringkas `posColsR`: 8 ([html:1390–1398](../../BacktestShariah2/standard/dashboard_v2.html#L1390)).
  - Penuh `ptCols`: 12 lajur asas + 7 lajur gred = 19 ([html:1342–1355](../../BacktestShariah2/standard/dashboard_v2.html#L1342), `grCols` [html:1333–1340](../../BacktestShariah2/standard/dashboard_v2.html#L1333)). Lajur asas termasuk Tarikh beli, Saham, Kaedah, Harga beli, Unit, Harga terkini, Untung %, R, carta "Sejak beli", Hari, Keluar kaedah dan Pegang selagi naik.
  - Risiko `posColsP`: 11 (R, Risiko awal, Turun maks, Naik maks, Ke henti kaedah, Lorong 2, …) ([html:2946–2958](../../BacktestShariah2/standard/dashboard_v2.html#L2946)).
  - Gred: 3 + 7 = 10 ([html:2948](../../BacktestShariah2/standard/dashboard_v2.html#L2948)).
- Dokumen db yang dibaca:
  - `papertrade/ringkas_c` (+`_2…_5`, `_kamus_1…3`) dan `ringkas_m` (+`_kamus_1`) melalui `subRingkas`; jika tiada, `claude*`/`moomoo` ([html:3474–3500](../../BacktestShariah2/standard/dashboard_v2.html#L3474)).
  - `prestasi/garis` (carta kecil, cip SPY), `prestasi/mae` dan `prestasi/mfe` (pandangan Risiko).
  - `sektor/snapshot`, untuk "1B kini" dalam sel gred Sektor/Industri (`skPerf`/`grKump`, [html:1299–1306](../../BacktestShariah2/standard/dashboard_v2.html#L1299)).
- Tab sisi (pnav) lalai = "posisi & keputusan" ([html:3406](../../BacktestShariah2/standard/dashboard_v2.html#L3406)). Item rel: Gambaran, Peta portfolio, Posisi & keputusan, Isyarat tidak dibeli (dibina daripada tajuk panel oleh `applyNav`, [html:3413–3435](../../BacktestShariah2/standard/dashboard_v2.html#L3413)).
- Telefon:
  - `lajurOf()` sentiasa memulangkan 'penuh' di skrin kecil ([html:2037](../../BacktestShariah2/standard/dashboard_v2.html#L2037)). Butang Lajur disembunyi (`[data-lajur]{display:none}`, [html:407](../../BacktestShariah2/standard/dashboard_v2.html#L407)) dan pandangan Risiko/Gred dimatikan (`pandOf`, [html:2941](../../BacktestShariah2/standard/dashboard_v2.html#L2941)).
  - Jadual Penuh dipapar sebagai kad lipat: baris tertutup "Saham [akaun] · Kaedah · Nh · Keluar/Tunggu · Gred · Untung %" ([md:3](../../BacktestShariah2/standard/dashboard.md), versi 81). Kad terbuka mempunyai 3 zon (`kadPos`, [html:2073–2079](../../BacktestShariah2/standard/dashboard_v2.html#L2073)) dan butang "Butiran penuh ›".
  - Susunan dibuat melalui menu Susun + butang arah (`.msusun`, [html:684–704](../../BacktestShariah2/standard/dashboard_v2.html#L684)).
- Helaian posisi (`openPos`, [html:2178–2189](../../BacktestShariah2/standard/dashboard_v2.html#L2178)): 8 metrik, carta harga sejak beli, MFE/MAE/SPY/status, kedua-dua lorong, senarai 7 gred dan butang "Lihat kaedah".
- db langsung (`ringkas_c`, 22 Okt):
  - C: 4,289 baris, iaitu 49 tidak dibeli + **4,240 posisi**. Daripadanya, 3,253 masih dipegang dalam lorong kaedah, 987 sudah keluar lorong kaedah dan 132 sudah keluar kedua-dua lorong.
  - 121 kaedah. Tarikh beli antara 8 dan 21 Okt 2026, dengan belian harian 79–819; 697 dibeli pada 21 Okt.
  - M (`ringkas_m`): 208 posisi (101 dipegang, 43 kaedah), dibeli 1–8 Okt ([db langsung](https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e)).

**Tab Watchlist** (`renderWatch`, [html:1202–1253](../../BacktestShariah2/standard/dashboard_v2.html#L1202))
- Susunan:
  1. Tajuk ayat "Hampir Signal (90–100%) …" ([html:1225](../../BacktestShariah2/standard/dashboard_v2.html#L1225)).
  2. KPI 4: Calon, ≥ 99% hampir, Sektor terbanyak, Isyarat lengkap (atau Dibina) ([html:1226–1231](../../BacktestShariah2/standard/dashboard_v2.html#L1226)).
  3. Panel **Hampir Signal** ([html:1232–1246](../../BacktestShariah2/standard/dashboard_v2.html#L1232)). Kawalan: seg lajur, kaedah, sektor, industri dan carian. Ringkas 6 lajur (`watchColsR`, [html:1195–1201](../../BacktestShariah2/standard/dashboard_v2.html#L1195)); Penuh 8 + 7 gred = 15 lajur ([html:1237–1245](../../BacktestShariah2/standard/dashboard_v2.html#L1237)).
  4. Panel **Isyarat lengkap dalam watchlist**: 4 lajur dengan status belian Dibeli / Dilangkau / Menunggu belian / Tidak dibeli (`wBeli`, [html:1186–1193](../../BacktestShariah2/standard/dashboard_v2.html#L1186)); panel ditakrif di [html:1217–1223](../../BacktestShariah2/standard/dashboard_v2.html#L1217) dan diletak selepas panel utama; dilipat secara lalai ([html:3385](../../BacktestShariah2/standard/dashboard_v2.html#L3385)).
- Hanya baris dengan `pct_dipenuhi` 90–100 dipapar ([html:1173](../../BacktestShariah2/standard/dashboard_v2.html#L1173)).
- db: `papertrade/watchlist` dan bahagiannya (`subBhg`, [html:3509](../../BacktestShariah2/standard/dashboard_v2.html#L3509)). Data C dibaca juga untuk status belian.
- Hanya 2 panel peringkat atas, jadi tab sisi tidak aktif (`PNAV_MIN=3`, [html:3403](../../BacktestShariah2/standard/dashboard_v2.html#L3403)). Telefon memakai kad `kadWl` ([html:2119](../../BacktestShariah2/standard/dashboard_v2.html#L2119)).
- db langsung: 212 baris, semuanya dalam julat 90–100%: **88 isyarat lengkap** dan 124 calon hampir, merentas 64 kaedah; tarikh_data 2026-10-21.
- 47 kaedah calon K145+ (M115–M161) tiada `hampir()`, jadi tiada watchlist bagi kaedah-kaedah itu ([00_NOTA_SERAHAN.md:23](../../BacktestShariah2/00_NOTA_SERAHAN.md)).

**Tab Backtest › Keputusan** (`renderKeputusan`, [html:811–847](../../BacktestShariah2/standard/dashboard_v2.html#L811))
- Susunan:
  1. Tajuk ayat ([html:827](../../BacktestShariah2/standard/dashboard_v2.html#L827)).
  2. Podium 3 teratas (`kpPod`, [html:805–810](../../BacktestShariah2/standard/dashboard_v2.html#L805); [html:828](../../BacktestShariah2/standard/dashboard_v2.html#L828)).
  3. Panel **Saringan 7 langkah**: corong yang boleh diketik ([html:829–830](../../BacktestShariah2/standard/dashboard_v2.html#L829); `LANGKAH`/`PERINGKAT` [html:754–762](../../BacktestShariah2/standard/dashboard_v2.html#L754)).
  4. Panel **Semua kaedah** ([html:831–837](../../BacktestShariah2/standard/dashboard_v2.html#L831)): seg Dapat pingat/Semua, cip "Gaya saya: pegang ≤ 40 hari", carian dan jadual 10 lajur (`kpCols`, [html:794–804](../../BacktestShariah2/standard/dashboard_v2.html#L794)).
  5. Jalur "Cara baca" dan kaki ([html:838–840](../../BacktestShariah2/standard/dashboard_v2.html#L838)).
- Lalai: lihat 'pingat'. Desktop memapar semua baris; telefon 10 (`S.kp`, [html:648](../../BacktestShariah2/standard/dashboard_v2.html#L648)). Telefon memakai kad `LP_KP` ([html:2098–2104](../../BacktestShariah2/standard/dashboard_v2.html#L2098)).
- Mata wang: "RM10k → RM…" ([html:765](../../BacktestShariah2/standard/dashboard_v2.html#L765), [html:792](../../BacktestShariah2/standard/dashboard_v2.html#L792), [html:799–800](../../BacktestShariah2/standard/dashboard_v2.html#L799)). Ringkasan masih memakai "USD1,000 setiap belian", manakala Prestasi memakai % sahaja atas permintaan pengguna sejak versi 95 ([md:3](../../BacktestShariah2/standard/dashboard.md)).
- Langkah 2 ialah "Untung lebih daripada SPY" (gate G3) ([html:755–756](../../BacktestShariah2/standard/dashboard_v2.html#L755)). Matlamat projek pula ialah mengalahkan EW semua saham Shariah ([00_NOTA_SERAHAN.md:11](../../BacktestShariah2/00_NOTA_SERAHAN.md)).
- db: `registry/*` (173 dokumen), `autotune/a02_saringan` (Ujian 2), `kaedah/katalog` (varian aktif) dan data C (lajur Papertrade C) ([html:766–786](../../BacktestShariah2/standard/dashboard_v2.html#L766)).
- db langsung (kiraan semula logik `kpM` oleh penyelidik; anggaran): 141 kaedah M. **44 berpingat**: 2 Emas/GUNA, 21 Perak/UJI KERTAS, 21 Gangsa/SIMPAN. Gugur paling banyak di langkah 7 (Ujian 2; 40 kaedah) dan langkah 2 (SPY; 31 kaedah). 134 kaedah aktif, 7 tidak aktif.

**Tab Backtest › Butiran**
- Pemilih set **431 / S1 / S2 / S3 / S4 / 2000 AS** dalam subbar ([html:639](../../BacktestShariah2/standard/dashboard_v2.html#L639), [html:719–720](../../BacktestShariah2/standard/dashboard_v2.html#L719)).
- Bagi 431/S1–S4, seg ketiga ialah "Papan penuh (gate) / Carta & gaya / Banding varian" (`B4`, [html:857–861](../../BacktestShariah2/standard/dashboard_v2.html#L857)).
- Bagi 2000 AS, empat versi AUTOTUNE: "Semua lorong (A/B) / A02 / A03 / A01" (`AT_V`, [html:1940](../../BacktestShariah2/standard/dashboard_v2.html#L1940); `renderAutotune` [html:2020–2027](../../BacktestShariah2/standard/dashboard_v2.html#L2020)).
- Kesemuanya ialah 3 × 5 + 4 = 19 kombinasi paparan dalam 5 seksyen HTML (`v-papan/ringkasan/banding/autotune/keputusan`, [html:610–623](../../BacktestShariah2/standard/dashboard_v2.html#L610)).
- **Carta & gaya** (`renderRingkasan`, [html:863–904](../../BacktestShariah2/standard/dashboard_v2.html#L863)): tajuk, KPI 4 (termasuk "Atasi beli semua" = EW), grid "Gaya anda" (7 lajur) + "Taburan keputusan"/"Skor tertinggi", serakan "Pulangan lawan kejatuhan", jalur "Ingat" dan jalur "Tindakan seterusnya: Pantau dalam papertrade: …" ([html:901](../../BacktestShariah2/standard/dashboard_v2.html#L901)).
- **Papan penuh** (`renderPapan`, [html:945–973](../../BacktestShariah2/standard/dashboard_v2.html#L945)): 21 lajur (Kaedah, Keputusan, 18 `COLS` [html:929–935](../../BacktestShariah2/standard/dashboard_v2.html#L929), Gate gagal). Kawalan: Semua/Kaedah M/Indikator I, Varian terbaik sahaja, Gaya saya, 4 cip keputusan dan carian; "Papar 40 lagi".
- **Banding** (`renderBanding`, [html:1025–1045](../../BacktestShariah2/standard/dashboard_v2.html#L1025)): pilih hingga 3 varian, carta profil pegangan dan jadual ~23 metrik.
- Helaian varian (`openDetail`, [html:978–1006](../../BacktestShariah2/standard/dashboard_v2.html#L978)): gate G1–G6, kad saringan, grid 23 metrik, profil pegangan, konsisten merentas set dan "Tambah ke banding".
- db langsung: registry 665 varian set 431 (141 M + 32 indikator I) dan 271 varian setiap satu untuk S1–S4. Keputusan enjin set 431: 11 GUNA, 48 UJI KERTAS, 128 SIMPAN, 478 DITOLAK. Tarikh ujian terbaharu 2026-10-17. `autotune` = 194 dokumen.

**Tab Kaedah** (`renderKaedah`, [html:1811–1846](../../BacktestShariah2/standard/dashboard_v2.html#L1811))
- Susunan:
  1. Tajuk ayat.
  2. KPI 5: Kaedah aktif, Backtest/papertrade, Ada had masa, "Beli: Buka esok" (teks tetap) dan "Dua lorong keluar" (teks tetap) ([html:1832–1838](../../BacktestShariah2/standard/dashboard_v2.html#L1832)).
  3. Panel **Semua kaedah**: seg lajur, carian, legenda pil (`KAT_LEGENDA`, [html:1799](../../BacktestShariah2/standard/dashboard_v2.html#L1799)) dan jadual ([html:1839–1843](../../BacktestShariah2/standard/dashboard_v2.html#L1839)).
  4. Jalur "Sama untuk semua" dan kaki ([html:1844–1845](../../BacktestShariah2/standard/dashboard_v2.html#L1844)).
- Lajur: Ringkas = 4 (Kaedah, Backtest (set 431), Papertrade C, Asal); Penuh = 7 (ID, Kaedah, Asal, Masuk, Keluar, Pegang, Henti rugi) ([html:1825–1830](../../BacktestShariah2/standard/dashboard_v2.html#L1825)). Lalai 'penuh' ([html:2037](../../BacktestShariah2/standard/dashboard_v2.html#L2037)). Pandangan lalai Penuh tidak menunjukkan langsung bukti backtest atau papertrade.
- db: `kaedah/katalog` + `registry` + data C (`katGabungM`, [html:1801–1804](../../BacktestShariah2/standard/dashboard_v2.html#L1801)).
- Helaian `openKaedah` ([html:2156–2177](../../BacktestShariah2/standard/dashboard_v2.html#L2156)): cara kaedah berfungsi, papertrade (label TERUSKAN/PERHATI/HENTIKAN + skor Untung×Selamat), sebenar lawan backtest, dan pingat + kad saringan.
- db langsung: katalog 134 baris, dibina 2026-10-17.

**Tab Sektor** (`renderSektor`, [html:1089–1164](../../BacktestShariah2/standard/dashboard_v2.html#L1089))
- Susunan:
  1. Tajuk ayat ("Tab ini maklumat sahaja") ([html:1104](../../BacktestShariah2/standard/dashboard_v2.html#L1104)).
  2. KPI 4: Sektor 1M terkuat, Industri 1M terkuat, Breadth pasaran, Fasa sektor ([html:1105–1110](../../BacktestShariah2/standard/dashboard_v2.html#L1105)).
  3. **Peta haba**: seg Sektor/Industri × 1H/1W/1M/3M ([html:1111–1115](../../BacktestShariah2/standard/dashboard_v2.html#L1111)).
  4. **Ranking sektor & industri**: 11 lajur termasuk Fasa, 1H/1W/1M/3M, RS, Breadth, Volum relatif dan Aliran institusi; seg Sektor/Industri, pilih sektor dan carian ([html:1116–1132](../../BacktestShariah2/standard/dashboard_v2.html#L1116)).
  5. Grid: **Fasa rotasi** (carta kuadran) + **Aliran institusi & volum** ([html:1133–1145](../../BacktestShariah2/standard/dashboard_v2.html#L1133)).
  6. **10 industri 1M terkuat** (kad, termasuk calon watchlist dalam industri itu) ([html:1146–1152](../../BacktestShariah2/standard/dashboard_v2.html#L1146)).
  7. Jalur **Nota kalibrasi** dan kaki ([html:1153–1155](../../BacktestShariah2/standard/dashboard_v2.html#L1153)).
- db: `sektor/snapshot` ([html:3510](../../BacktestShariah2/standard/dashboard_v2.html#L3510)) + watchlist.
- db langsung: 11 sektor + 138 industri, `alam` "US penuh", dibina 2026-10-22 06:35 MYT.
- Pada 21 Okt, SST tidak tersedia; breadth, volum luar biasa dan aliran institusi SST membawa nilai 19 Okt ([log+:212](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md)).

### Inferences
- Setiap tab mengulang corak yang sama (tajuk ayat + KPI 4–5 + panel + jalur penerangan + kaki). Hasilnya ialah ~10 blok teks penerangan tetap dalam lima tab ini; penerangan itu boleh dipindah ke Panduan.
- Untuk soalan pengguna "adakah posisi saya OK?", tab Posisi menyusun 4,240 baris ikut Untung % menurun, jadi posisi terbaik dipapar dahulu. Tiada KPI "berapa posisi hampir/kena paras keluar" dalam tab Posisi. Maklumat itu hanya wujud dalam panel Esok di Ringkasan (lihat S2).
- Dengan pertumbuhan ~500–800 belian sehari, baris Posisi C akan melepasi 10,000 dalam beberapa minggu. Jadual satu-baris-satu-posisi tidak lagi sesuai sebagai paparan utama; ringkasan ikut kaedah atau status lebih sesuai.
- Pandangan lalai tab Kaedah (Penuh) menyorok bukti dan hanya menunjukkan peraturan. Peraturan pula bersifat rujukan, bukan bahan keputusan harian.

### Gaps
- Halaman tidak dirender (tiada Playwright dalam audit ini). Ketinggian sebenar di 390px pada versi 102 dan bilangan item rel yang benar-benar terpapar tidak diukur; kiraan diambil daripada kod.
- Kiraan pingat (44) ialah replikasi `kpM` oleh penyelidik dan mungkin berbeza sedikit daripada angka yang dipapar halaman.

## S2. Pertindihan dengan tab lain (termasuk Ringkasan, Analisis, Prestasi)

### Takeaway
Maklumat "setiap kaedah" muncul dalam sekurang-kurangnya lima jadual dan tiga helaian: Backtest Keputusan, Butiran Papan, Kaedah, Analisis dan Prestasi. Setiap satu memakai sistem label sendiri. Ringkasan menyalin podium Keputusan dan status data di pengepala. Panel Esok dalam Ringkasan memakai data yang sama dengan Watchlist (isyarat lengkap) dan Posisi (status keluar). `ptCols()` kini hanya dipakai oleh Posisi, walaupun dokumentasi menyatakan ia dikongsi dengan Prestasi.

### Cited Findings
- **Podium berganda:** Ringkasan "Terbaik ikut backtest" memakai `kpPod` yang sama dengan podium Keputusan ([html:3048–3049](../../BacktestShariah2/standard/dashboard_v2.html#L3048) lawan [html:828](../../BacktestShariah2/standard/dashboard_v2.html#L828)).
- **Status data berganda:** jalur `salStrip()` dalam Ringkasan ([html:3030](../../BacktestShariah2/standard/dashboard_v2.html#L3030), [html:2350](../../BacktestShariah2/standard/dashboard_v2.html#L2350)) ialah 8 cip yang sama dengan butang "Data n/8" di pengepala dan helaiannya ([html:2310–2316](../../BacktestShariah2/standard/dashboard_v2.html#L2310)).
- **Ringkasan Esok lawan Watchlist/Posisi** (`panelEsok`, [html:2319–2333](../../BacktestShariah2/standard/dashboard_v2.html#L2319)):
  - "Dibeli pada buka" = isyarat lengkap watchlist berstatus `tunggu` daripada `wBeli` yang sama dengan panel "Isyarat lengkap dalam watchlist" ([html:2321](../../BacktestShariah2/standard/dashboard_v2.html#L2321)).
  - "Dijual pada buka", "Hampir paras keluar" dan "Earnings ≤ 5 hari" = `statusPos`/`hariKeEarn` daripada posisi C yang sama dengan jadual Posisi.
  - Butang "+n lagi" melompat ke tab `posisi`/`watch` tanpa tapisan ([html:2325](../../BacktestShariah2/standard/dashboard_v2.html#L2325)).
- **Panel Berubah** dalam Ringkasan juga mengira "Masuk Watchlist" dan "Kedudukan Analisis" ([html:2335–2348](../../BacktestShariah2/standard/dashboard_v2.html#L2335)).
- **Jadual per kaedah:**
  - Keputusan "Semua kaedah" (backtest + lajur Papertrade C, `kpPtSel` [html:793](../../BacktestShariah2/standard/dashboard_v2.html#L793)).
  - Butiran Papan penuh (21 metrik backtest).
  - Kaedah (Backtest + Papertrade C dalam lajur Ringkas; `selBt`/`selPt` [html:1806–1810](../../BacktestShariah2/standard/dashboard_v2.html#L1806)).
  - Analisis (Backtest 431, Semakan S1–S4/WFO/2000 AS, Jangkaan, Matang, Lorong 2, C, Skor; [html:3080–3135](../../BacktestShariah2/standard/dashboard_v2.html#L3080)).
  - Prestasi "kedudukan kaedah" dan "Skor kaedah swing" ([md:3](../../BacktestShariah2/standard/dashboard.md), versi 96–102).
- **Helaian kaedah:** `openKaedah` ([html:2156](../../BacktestShariah2/standard/dashboard_v2.html#L2156)), `openDetail` bagi varian backtest ([html:978](../../BacktestShariah2/standard/dashboard_v2.html#L978)) dan helaian baris Analisis (`LP_ANL`, [html:3145](../../BacktestShariah2/standard/dashboard_v2.html#L3145)).
- **Penapis "Gaya saya ≤ 40 hari" di tiga tempat:** Keputusan ([html:835](../../BacktestShariah2/standard/dashboard_v2.html#L835)), Papan penuh ([html:957](../../BacktestShariah2/standard/dashboard_v2.html#L957)) dan jadual "Gaya anda" dalam Carta & gaya ([html:871–885](../../BacktestShariah2/standard/dashboard_v2.html#L871)). Definisi swing dalam Papan Penganalisis pula ialah 3–30 hari (CLAUDE.md, Papan Penganalisis).
- **Semakan luar sampel dirumus dua kali:** langkah 6–7 Keputusan (S1–S4, Ujian 2) dan lajur Semakan ✓✗ dalam Analisis (`anlSem`, [html:3080](../../BacktestShariah2/standard/dashboard_v2.html#L3080)). Butiran set S1–S4/2000 AS memapar data mentahnya.
- **Sistem label berbeza bagi soalan yang sama ("adakah kaedah ini baik?"):**
  - Enjin: GUNA/UJI KERTAS/SIMPAN/DITOLAK → pingat Emas/Perak/Gangsa, "✗ Langkah n", "◌ Belum diuji" ([html:763](../../BacktestShariah2/standard/dashboard_v2.html#L763), [html:788–791](../../BacktestShariah2/standard/dashboard_v2.html#L788)).
  - Prestasi: TERUSKAN/PERHATI/HENTIKAN/BELUM CUKUP DATA (`KPT`, [html:1422](../../BacktestShariah2/standard/dashboard_v2.html#L1422)).
  - Analisis: KUAT/PERHATI/LEMAH/AMARAN/BELUM CUKUP (`ANL_ST`, [html:3077](../../BacktestShariah2/standard/dashboard_v2.html#L3077)).
  - Pantau: OK/AMARAN/GANTUNG/BERSARA (`SKW_HENTI`, [html:2567](../../BacktestShariah2/standard/dashboard_v2.html#L2567)).
  - Skor swing: Teras/Calon/Pantau/Belum layak/Gantung/Bersara (`skwTahap`, [html:2586](../../BacktestShariah2/standard/dashboard_v2.html#L2586)).
  - AUTOTUNE: TINGGI/SEDERHANA/RENDAH/GAGAL/BUKAN SWING/PANDANG HADAPAN/BELUM DITALA, ditambah A02 LULUS/CALON/TIDAK LULUS dan A03 MENANG/HAMPIR/TIDAK ([html:1853–1855](../../BacktestShariah2/standard/dashboard_v2.html#L1853), [html:1941](../../BacktestShariah2/standard/dashboard_v2.html#L1941)).
  - "PERHATI" dan "AMARAN" masing-masing membawa maksud berbeza dalam dua sistem.
- **`ptCols()` hanya dipanggil dalam `renderPos`** ([html:1414](../../BacktestShariah2/standard/dashboard_v2.html#L1414)). `dashboard.md` masih menyatakan "Lajur M, C dan jadual dagangan Prestasi sama … (`ptCols()`)" ([md:28](../../BacktestShariah2/standard/dashboard.md)), jadi dokumentasi sudah usang.
- **Komen kod tidak sepadan dengan kod:** komen menyatakan akaun dikongsi oleh "Prestasi, Posisi, Backtest dan Kaedah" ([html:640](../../BacktestShariah2/standard/dashboard_v2.html#L640)), tetapi Keputusan dan Kaedah sentiasa memakai `prSrc('c')` ([html:786](../../BacktestShariah2/standard/dashboard_v2.html#L786), [html:1805](../../BacktestShariah2/standard/dashboard_v2.html#L1805)).
- **Kebergantungan silang Sektor → Posisi/Watchlist:** sel gred Sektor/Industri memapar "1B kini" daripada `sektor/snapshot` ([html:1299–1306](../../BacktestShariah2/standard/dashboard_v2.html#L1299)). Sektor pula memapar calon watchlist bagi setiap industri ([html:1150](../../BacktestShariah2/standard/dashboard_v2.html#L1150)).

### Inferences
- Pengguna perlu belajar ~7 kosa kata label untuk satu soalan. Ini punca utama papan "sukar difahami". Satu label keputusan tunggal (contohnya daripada Papan Penganalisis/Skor swing) dengan bukti sokongan di helaian akan mengurangkan beban ini.
- Keputusan, Kaedah dan Butiran boleh digabung menjadi satu "Profil kaedah" (helaian/halaman setiap kaedah) dan satu jadual ranking tunggal (Analisis).
- Panel Esok sudah menjawab soalan (2) "apa berlaku hari ini/esok". Ia layak menjadi blok utama. Jadual penuh Watchlist dan Posisi pula boleh menjadi paparan butiran yang dibuka daripada blok itu.

### Gaps
- Prestasi, Ringkasan dan Analisis tidak diaudit mendalam (skop penyelidik lain). Pertindihan dalaman Prestasi (contohnya kedudukan kaedah lawan Skor swing) tidak dinilai di sini.

## S3. Bahagian warisan atau bernilai diragui di bawah peraturan semasa

### Takeaway
Calon terkuat untuk dibuang atau diturunkan ialah:
- akaun Moomoo lama (dimuat dan diberi sub-tab walaupun tiada belian sejak 13 Okt);
- tab Sektor (fasa dan skor panas gagal kalibrasi, tetapi fasa masih dipapar di empat tempat; data SST pun basi);
- Backtest Butiran, iaitu 19 kombinasi paparan backtest mentah termasuk 32 indikator I yang bukan kaedah dagangan;
- 7 lajur gred dalam jadual utama;
- jalur teks yang sudah lapuk.

Lorong 10% sudah tiada dalam kod.

### Cited Findings
- **Moomoo lama:**
  - Peraturan: "Papertrade C … sahaja untuk belian baharu sejak 13 Okt 2026" (CLAUDE.md); keputusan pengguna kerana Moomoo kerap ralat ([log+:19](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md)).
  - Halaman tetap memberi sub-tab M dan Gabung dalam Posisi dan Prestasi ([html:641–643](../../BacktestShariah2/standard/dashboard_v2.html#L641)), tajuk dan jalur "Sumber" warisan v1 / "strategi luar 87 M" ([html:1407–1408](../../BacktestShariah2/standard/dashboard_v2.html#L1407)).
  - `ringkas_m` dilanggan tanpa syarat pada setiap buka ([html:3493](../../BacktestShariah2/standard/dashboard_v2.html#L3493)); saiznya 65.7 KiB (db langsung).
  - Data: 208 posisi, 101 masih dipegang.
- **Tab Sektor:**
  - `dashboard.md` "Kalibrasi tab Sector" menyatakan skor panas, fasa Leading dan kekuatan 1W–12M tidak meramal pulangan 1–3 bulan, dan "TIDAK digunakan sebagai penapis atau keutamaan beli" ([md:21–25](../../BacktestShariah2/standard/dashboard.md)).
  - Tab masih memapar fasa dalam KPI "Fasa sektor", lajur Fasa, carta Fasa rotasi dan pil fasa dalam kad 10 industri ([html:1109](../../BacktestShariah2/standard/dashboard_v2.html#L1109), [html:1122](../../BacktestShariah2/standard/dashboard_v2.html#L1122), [html:1134](../../BacktestShariah2/standard/dashboard_v2.html#L1134), [html:1149](../../BacktestShariah2/standard/dashboard_v2.html#L1149)). Tooltip `skor_panas` masih dalam `TIPS` ([html:3287](../../BacktestShariah2/standard/dashboard_v2.html#L3287)).
  - Gred Sektor/Industri v2 (Weinstein, disahkan kajian; CLAUDE.md; [log+:147](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md)) hanya muncul dalam sel gred Posisi/Watchlist, bukan dalam tab Sektor.
  - Medan SST basi sejak 19 Okt ([log+:212](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md)).
- **Gred A–E:**
  - Tugasan menetapkan "rekod dan uji dahulu, bukan penapis" ([tugasan_v3.md:80](../../BacktestShariah2/standard/tugasan_v3.md)); Panduan: "Gred tidak menapis belian" ([html:2981](../../BacktestShariah2/standard/dashboard_v2.html#L2981)).
  - Namun jadual Penuh Posisi dan Watchlist membawa 7 lajur gred bersel kaya (skor /100, RS, hari ke earnings, teks pemangkin + pautan berita, sub-gred kewangan K/U/T/S) ([html:1333–1340](../../BacktestShariah2/standard/dashboard_v2.html#L1333)).
  - Label QR "Selamat / Berhati-hati / Elak" ([html:1318](../../BacktestShariah2/standard/dashboard_v2.html#L1318)) berbunyi seperti arahan tindakan walaupun bukan penapis.
- **Lorong 10%:** dibuang pada 17 Okt ([log+:143](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md)). `LORONG` dalam kod kini hanya `kaedah` dan `henti` ([html:1267](../../BacktestShariah2/standard/dashboard_v2.html#L1267)), jadi tiada sisa dalam lima tab ini.
- **Isyarat tidak dibeli:** 49 baris, dilipat secara lalai, "tidak dikira dalam Prestasi" ([html:1415](../../BacktestShariah2/standard/dashboard_v2.html#L1415)). Kepentingannya rendah untuk keputusan, tetapi ia rekod audit "kalau tak beli, cakap tak beli" (CLAUDE.md).
- **Backtest Butiran:**
  - 19 kombinasi set × sub-paparan, dengan 4 versi AUTOTUNE yang masing-masing mempunyai kosa kata label sendiri ([html:1940–1941](../../BacktestShariah2/standard/dashboard_v2.html#L1940)).
  - Papan penuh memasukkan 32 indikator I (seg "Indikator I", [html:955](../../BacktestShariah2/standard/dashboard_v2.html#L955)). Dokumen registry I = 224 KiB padat dimuat pada setiap buka.
  - Hasil luar sampel sudah dirumus dalam langkah 6–7 Keputusan dan lajur Semakan Analisis.
- **Teks lapuk:**
  - Jalur "Tindakan seterusnya: Pantau dalam papertrade: <3 kaedah>" ([html:901](../../BacktestShariah2/standard/dashboard_v2.html#L901)), sedangkan Papertrade C membeli semua kaedah aktif ([html:2977](../../BacktestShariah2/standard/dashboard_v2.html#L2977)) dan Lejar Penuh membeli semua isyarat ([tugasan_v3.md:92–93](../../BacktestShariah2/standard/tugasan_v3.md)).
  - KPI teks tetap dalam Kaedah ("Beli: Buka esok", "Dua lorong keluar") ([html:1836–1837](../../BacktestShariah2/standard/dashboard_v2.html#L1836)).
  - Tajuk halaman "Papan Backtest Shariah" ([html:585](../../BacktestShariah2/standard/dashboard_v2.html#L585)) sedangkan tumpuan kini data hadapan.
- **Mata wang dan penanda aras tidak seragam:** Keputusan memakai RM10k dan langkah SPY; Butiran KPI memakai EW ("Atasi beli semua"); Prestasi memakai % (rujukan dalam S1).

### Inferences
- Moomoo lama boleh dijadikan arkib (satu baris pautan, dimuat atas permintaan). Ia tidak menjawab mana-mana daripada empat soalan 10 saat.
- Tab Sektor boleh diturunkan menjadi panel "Konteks pasaran" kecil (breadth + kumpulan terkuat). Paparan fasa boleh dibuang memandangkan kalibrasi gagal, atau digantikan dengan gred kumpulan v2 yang sah.
- Lajur gred lebih sesuai dalam helaian posisi sahaja (sudah ada `gredList`). Ini konsisten dengan status "rekod sahaja" sehingga kajian gred lulus.
- Backtest Butiran boleh menjadi pautan "Data backtest mentah" dalam profil kaedah, bukan sub-tab utama.

### Gaps
- Tiada data penggunaan sebenar (analitik klik) untuk mengesahkan tab mana yang jarang dibuka. Penilaian di atas berdasarkan peraturan dan matlamat dalam repo sahaja.

## S4. Isyarat kesegaran data dan kesihatan sistem: apa yang dipapar dan apa yang tidak

### Takeaway
Halaman memapar dua isyarat:
1. "Kemas kini terakhir" (merah jika > 30 jam, atau 74 jam merentas hujung minggu);
2. butang "Data n/8": 8 saluran dibanding tarikh dengan sesi dijangka, tanpa kalendar cuti NYSE.

Kedua-duanya hanya menguji **tarikh**, bukan **kejayaan**. Medan kesihatan yang sudah ada dalam `harian/status` tidak dipapar langsung: ralat kaedah, bilangan belian direkod/dilangkau, keluar baharu dan gred_pada. Mod `MOD_ACTIONS` (bayang/rasmi), keputusan GitHub Actions, `sahkan.py`, saham tanpa bar dan penjaga jadual juga tidak kelihatan. Oleh itu soalan (4) "adakah sistem berjalan betul" hanya dijawab separuh.

### Cited Findings
- **Pengepala "Kemas kini terakhir"** (`renderData`, [html:740–747](../../BacktestShariah2/standard/dashboard_v2.html#L740)): dibaca daripada `harian/status.dikemaskini`; merah + pil "belum dikemas kini" jika lebih 30 jam (Ahad–Selasa MYT: 74 jam) ([html:729–732](../../BacktestShariah2/standard/dashboard_v2.html#L729)). Tarikh data tutup diambil daripada `harga_tutup_pada`, atau sandaran `harga_pada`/tarikh posisi ([html:735–738](../../BacktestShariah2/standard/dashboard_v2.html#L735)).
- **"Data n/8"** (`saluran`, [html:2300–2307](../../BacktestShariah2/standard/dashboard_v2.html#L2300)): Harga & posisi, Belian 9:35 NY, Watchlist, Harga tinggi/rendah (mae), Lejar Penuh, Penganalisis, Portfolio 10 slot, Sektor (≤ 8 hari).
  - Status ✓ segar / ! lewat 1 sesi / ✗ basi / ? tiada.
  - Helaian menyatakan "cuti NYSE tidak diambil kira" ([html:2313–2316](../../BacktestShariah2/standard/dashboard_v2.html#L2313)).
  - Di telefon, cip "ok" disembunyi dalam jalur Ringkasan ([html:554](../../BacktestShariah2/standard/dashboard_v2.html#L554)).
- **Teks hidup** "Langsung · ujian terkini <tarikh>" memakai tarikh ujian **registry** backtest (kini 2026-10-17), bukan tarikh data harian ([html:3466–3468](../../BacktestShariah2/standard/dashboard_v2.html#L3466)).
- **Ralat lukis tab** dipapar sebagai panel merah dalam tab itu ([html:3165](../../BacktestShariah2/standard/dashboard_v2.html#L3165)).
- **Medan `harian/status` yang ditulis tetapi tidak dibaca halaman:**
  - `jana_db.py` menulis `ralat` (senarai ralat kaedah, ≤ 20), `beli_ringkas {direkod, dilangkau}`, `beli_dirancang`, `kemaskini_pagi_ringkas {C_keluar_baru, M_keluar_baru, menunggu_buka, tidak_dibeli_baru, watchlist_dibuang}`, `senarai_beli {…}`, `gred_pada` dan `sumber` ([jana_db.py:510–520](../../BacktestShariah2/standard/jana_db.py)).
  - Halaman hanya merujuk `S.hst` untuk tarikh dan masa ([html:735](../../BacktestShariah2/standard/dashboard_v2.html#L735), [html:740](../../BacktestShariah2/standard/dashboard_v2.html#L740), [html:2300](../../BacktestShariah2/standard/dashboard_v2.html#L2300)). Carian `beli_ringkas|kemaskini_pagi_ringkas|bayang` dalam HTML: tiada padanan bagi medan ini.
- **Nilai langsung `harian/status` (versi 34, 22 Okt):**
  - dikemaskini 2026-10-22 06:30 MYT; harga_tutup_pada 2026-10-21; beli_pada 2026-10-21 21:41 MYT.
  - beli_dirancang 730, direkod 703, dilangkau 27.
  - C_keluar_baru 112, menunggu_buka 46, tidak_dibeli_baru 6, watchlist_dibuang 73.
  - `ralat: []`; **gred_pada: "" (kosong)**.
  - sumber "GitHub Actions (standard/harian_c.py) + sesi Claude tolak db" ([db langsung](https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e)).
- **Ketinggalan satu sesi pada masa bacaan:** `analisis/papan` harga_pada dan lejar_sesi = 2026-10-20 dan `prestasi/portfolio_slot.sesi_terakhir` = 2026-10-20, sedangkan harga posisi = 2026-10-21 ([db langsung](https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e)). Semua 134 baris Analisis berstatus "BELUM CUKUP" dan medan `pantau` kosong.
- **`MOD_ACTIONS` = `bayang`** ([BacktestShariah2/MOD_ACTIONS](../../BacktestShariah2/MOD_ACTIONS)): dalam mod ini Actions menulis ke `bayang/` sahaja dan rutin Claude kekal rasmi ([tugasan_v3.md:105–106](../../BacktestShariah2/standard/tugasan_v3.md); [PERALIHAN.md](../../BacktestShariah2/jadual/PERALIHAN.md)). Teks `sumber` dalam status ialah rentetan tetap dalam `jana_db.py:513` dan tidak menyatakan mod. Laporan banding harian `bayang/BANDING_<tarikh>.md` juga tidak dipapar.
- **`data/harga/status.json`** (dijana 2026-10-22 06:22 UTC): sesi 20261021, 931 ticker, `tiada_bar_sesi` 4 (ATKR, BLFS, QRVO, WLYB), dividen_baharu 1. Tidak dipapar ([status.json](../../BacktestShariah2/data/harga/status.json)).
- **GitHub Actions:** 31 fail workflow. Jadual utama:
  - `harian.yml` 05:07 UTC + 3 sandaran (Sel–Sab);
  - `beli.yml` 13:40/14:40/16:25/19:25 UTC (Isn–Jum);
  - `lejar.yml` 06:17/10:17;
  - `analisis.yml` dicetus `workflow_run`;
  - `penjaga_jadual.yml` setiap jam pada :23 dan :53;
  - `semak_data.yml` pada push;
  - serta `rs_pasaran`, `gred_kumpulan`, `edgar`, `harga_harian`, `petang` dan `skrin_tv` ([.github/workflows/](../../.github/workflows/)).
  - Tiada keputusan larian (berjaya/gagal) dimasukkan ke db atau dipapar. Penjaga jadual mengawasi 9 workflow dan dicetus dari luar oleh tugasan berjadual Claude (CLAUDE.md).
- **`sahkan.py --betulkan`** mesti keluar 0 sebelum push data (CLAUDE.md). Hasilnya tidak direkod dalam db.

### Inferences
- "Data n/8" boleh menunjukkan ✓ walaupun sesuatu langkah gagal separa, kerana yang diuji hanya tarikh. Contohnya ralat beberapa kaedah, gred yang tidak dikemas kini (`gred_pada` kosong) atau saham tanpa bar.
- Panel "Kesihatan sistem" yang jujur memerlukan satu dokumen ringkas (contohnya `harian/status` dilanjutkan) dengan tiga bahagian:
  - status larian terakhir setiap workflow (berjaya/gagal + masa);
  - kiraan semakan (isyarat, belian direkod/dilangkau/dibatalkan, ralat kaedah, saham tanpa bar, `sahkan.py` lulus);
  - mod (bayang/rasmi) dan sumber data.
  
  Kebanyakan medan sudah ditulis oleh `jana_db.py`; cuma halaman yang tidak membacanya.
- Ketinggalan Lejar/Penganalisis/Portfolio satu sesi adalah normal mengikut jadual (`lejar.yml` 06:17 UTC selepas `harian.yml`). Namun pengguna tidak dapat membezakan "lewat ikut jadual" dengan "gagal".

### Gaps
- Status sebenar larian GitHub Actions hari ini tidak disemak (tiada panggilan API GitHub dalam audit ini).
- Tidak diperhatikan apa yang dipapar butang "Data n/8" pada masa sebenar. Pengiraan bergantung pada jam pelayar (`jangkaSesi`).

## S5. Muatan dan prestasi

### Takeaway
Setiap kali dibuka, halaman melanggan **389 dokumen db, kira-kira 4.0 MiB JSON padat**. Angka ini lebih besar daripada 3.6 MB yang direkod selepas versi 90. Semuanya dimuat tanpa mengira tab yang dibuka: registry 1.31 MiB, posisi C 1.40 MiB dan watchlist 0.29 MiB. HTML pula 491 KB. Dokumen lama `claude*`/`moomoo`/`senarai_beli` (~7.5 MiB) masih ada dalam db tetapi hanya dibaca sebagai sandaran.

### Cited Findings
- **HTML:** 490,841 bait, 3,521 baris (wc pada `dashboard_v2.html`). Format penerbitan tanpa doctype/head, dengan `<style>` sebaris ([md:4](../../BacktestShariah2/standard/dashboard.md)).
- **`connect()` melanggan semua dokumen serentak** ([html:3457–3519](../../BacktestShariah2/standard/dashboard_v2.html#L3457)):
  - koleksi `registry` (had 1000) dan koleksi `autotune` (had 1000);
  - `meta/info`, `ringkas_m*`, `ringkas_c*`, `watchlist*`, `sektor/snapshot`, `harian/status`;
  - `prestasi/mae`, `garis`, `mfe`, `harian_kaedah`, `portfolio_slot`;
  - `analisis/papan`, `kaedah/katalog`.
- **Saiz padat diukur daripada db langsung (22 Okt):**

  | Kumpulan | Dokumen | Saiz |
  |---|---|---|
  | registry | 173 | 1,337.9 KiB (I = 32 dok., 224 KiB) |
  | ringkas_c* | 8 | 1,432.3 KiB |
  | watchlist* | 2 | 300.8 KiB |
  | autotune | 194 | 154.9 KiB |
  | kaedah/katalog | 1 | 149.8 KiB |
  | prestasi/mfe | 1 | 132.4 KiB |
  | prestasi/mae | 1 | 127.9 KiB |
  | analisis/papan | 1 | 119.5 KiB |
  | sektor/snapshot | 1 | 95.1 KiB |
  | prestasi/garis | 1 | 76.5 KiB |
  | ringkas_m* | 2 | 65.7 KiB |
  | prestasi/harian_kaedah | 1 | 64.5 KiB |
  | prestasi/portfolio_slot | 1 | 5.9 KiB |
  | meta/info | 1 | 0.3 KiB |
  | **Jumlah** (+ harian/status) | **388 + 1** | **≈ 3.97 MiB** |

  Sebelum ini: 7.2 → 3.6 MB selepas versi 90 ([md:3](../../BacktestShariah2/standard/dashboard.md)).
- **Dalam db tetapi tidak dilanggan** (melainkan `ringkas_*` tiada): 60 dokumen `papertrade/claude…claude_51`, `moomoo`, `moomoo_peta`, `senarai_beli…_6` dan `log` ≈ 7.46 MiB padat; juga `prestasi/ringkasan` (51 KiB) dan `analisis/sebenar` (32 KiB). Tiada rujukan kepada dua dokumen terakhir dalam HTML (grep 0).
- **Lukisan:**
  - Setiap dokumen yang tiba memanggil `renderSoon` (debounce 30 ms) yang melukis semula tab semasa ([html:671–672](../../BacktestShariah2/standard/dashboard_v2.html#L671)). Dengan ~389 dokumen, lukisan semula berlaku berulang kali semasa memuat.
  - Rangka (skeleton) dipapar sehingga papertrade siap, dengan had 20 s ([html:3461](../../BacktestShariah2/standard/dashboard_v2.html#L3461)).
  - `muatLajur` mengukur dan menyorok lajur selepas setiap lukisan dan ubah saiz ([html:3172–3190](../../BacktestShariah2/standard/dashboard_v2.html#L3172)).
- **Carta dalam lima tab ini:** treemap (Peta portfolio, Peta haba), serakan CAGR–MDD (Carta & gaya), kuadran Fasa rotasi, carta kecil setiap baris Posisi (`sparkPos`) dan profil pegangan (helaian/Banding).
- **Ketinggian halaman 390px pada versi 85** (selepas kad lipat): Prestasi 8,093px, Backtest 3,800px, Kaedah 3,063px, Sektor 5,862px ([log+:201](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md)).

### Inferences
- Memuat malas ikut tab akan mengurangkan muatan awal lebih separuh:
  - registry + autotune (1.5 MiB) hanya untuk Backtest/Kaedah/profil kaedah;
  - sektor hanya untuk konteks pasaran;
  - ringkas_m hanya untuk arkib.
  
  Ini mungkin bertentangan dengan Ringkasan dan Analisis yang mengira daripada registry. Jika ringkasan backtest dipra-kira dalam `analisis/papan` (yang sudah mengandungi `bt_*`), registry tidak perlu dimuat untuk paparan utama.
- `ringkas_c` akan terus membesar (~500–800 posisi/hari). Paparan utama lebih baik dibaca daripada ringkasan pra-kira bagi setiap kaedah/status; baris penuh dimuat atas permintaan sahaja.

### Gaps
- Masa muat sebenar (ms) di telefon dan desktop tidak diukur. Saiz di atas ialah JSON padat, bukan bait rangkaian sebenar selepas mampatan.

## S6. Navigasi dan rangka global (pengepala, Panduan, tab sisi, telefon lawan desktop)

### Takeaway
Navigasi berlapis empat:
1. 8 tab utama;
2. subbar: akaun 3 / Keputusan–Butiran / set 6;
3. seg ketiga Butiran (3 atau 4);
4. tab sisi (rel/cip) di dalam tab, dengan butang togol "Papar senarai / Lipat semua / Buka semua".

Di telefon ≤ 520px, 8 tab dibalut menjadi dua baris dalam pengepala melekit, ditambah subbar dan jalur cip melekit. Ini menggunakan sebahagian besar skrin sebelum kandungan. Panduan pula mengandungi 162 istilah glosari, satu petanda bilangan konsep yang perlu dipelajari.

### Cited Findings
- **Pengepala** ([html:583–607](../../BacktestShariah2/standard/dashboard_v2.html#L583)):
  - tajuk "Papan Backtest Shariah"; "Kemas kini terakhir" + tarikh data tutup; butang "Data n/8"; butang "?" (Panduan); titik + teks sambungan;
  - `nav.tabs` 8 butang: Ringkasan, Analisis, Prestasi, Posisi, Watchlist, Backtest, Kaedah, Sektor ([html:591–599](../../BacktestShariah2/standard/dashboard_v2.html#L591));
  - subbar: sub-tab, "Set saham" + 6 butang set, togol tab sisi, "Lipat semua" dan "Buka semua" ([html:601–607](../../BacktestShariah2/standard/dashboard_v2.html#L601)).
- **Pengepala melekit** (`header.top{position:sticky…}`, [html:34](../../BacktestShariah2/standard/dashboard_v2.html#L34)). ≤ 520px: `nav.tabs{flex-wrap:wrap}`, butang 8×9px ([html:303](../../BacktestShariah2/standard/dashboard_v2.html#L303)). Di telefon, rel tab sisi menjadi jalur cip melekit di bawah pengepala ([html:128–135](../../BacktestShariah2/standard/dashboard_v2.html#L128)).
- **Pautan hash:** 17 kunci (`utama, ringkasan, analisis, penganalisis, keputusan, kedudukan, butiran, papan, banding, sektor, watchlist, posisi, ptm, ptc, prestasi, kaedah, autotune`) ([html:653](../../BacktestShariah2/standard/dashboard_v2.html#L653)).
- **Tab sisi (versi 93–94):**
  - tab dengan ≥ 3 panel peringkat atas memapar satu bahagian pada satu masa;
  - Ringkasan hanya di telefon;
  - lalai Posisi = "posisi & keputusan", Analisis = "kedudukan kaedah", Ringkasan = "3 perkara utama";
  - pilihan disimpan dalam `pbs2_pnav_pilih`; togol `pbs2_pnav` ([html:3396–3455](../../BacktestShariah2/standard/dashboard_v2.html#L3396)).
  - Panel lain dilipat secara lalai: "cara skor dikira, banding dua lorong keluar, prestasi ikut gred, isyarat tidak dibeli, isyarat lengkap dalam watchlist" ([html:3385](../../BacktestShariah2/standard/dashboard_v2.html#L3385)).
- **Storan pelayar:** tab, akaun, sub-tab, set, b4, lajur, pandangan, lipatan dan tab sisi ([html:650–652](../../BacktestShariah2/standard/dashboard_v2.html#L650), [html:724](../../BacktestShariah2/standard/dashboard_v2.html#L724)). Halaman dibuka semula pada tab terakhir, bukan Ringkasan.
- **Panduan** (`openPanduan`, [html:2965–2995](../../BacktestShariah2/standard/dashboard_v2.html#L2965)):
  - "Cara membaca papan ini" 4 langkah: Ringkasan, Analisis, Prestasi, Ketik untuk butiran ([html:2969–2972](../../BacktestShariah2/standard/dashboard_v2.html#L2969));
  - Petunjuk simbol 11 entri (`SIMBOL`, [html:2205–2216](../../BacktestShariah2/standard/dashboard_v2.html#L2205));
  - 7 konsep penting; glosari boleh cari dijana daripada `TIPS` = **162 entri** ([html:3197–3362](../../BacktestShariah2/standard/dashboard_v2.html#L3197)).
  - Tooltip dibuka dengan hover di desktop dan tekan lama di telefon ([md:31](../../BacktestShariah2/standard/dashboard.md)).
- **Lebar telefon:** jadual "Lajur disembunyi kerana skrin tidak cukup lebar: …" (nota `muatLajur`) menyorok lajur kanan di desktop sempit ([html:3172–3190](../../BacktestShariah2/standard/dashboard_v2.html#L3172)). Telefon memakai kad lipat (`LP_KP`, `LP_KAT`, `LP_SK`, `kadPos`, `kadWl`; [html:2073–2121](../../BacktestShariah2/standard/dashboard_v2.html#L2073)).
- **Ketikan untuk maklumat utama di telefon** (dikira daripada kod; Ringkasan tab lalai jika tiada pilihan tersimpan, [html:646](../../BacktestShariah2/standard/dashboard_v2.html#L646)):
  - (2) Esok dibeli/dijual: tab Ringkasan → cip "Esok" (jalur cip; lalai "3 perkara utama") = 1–2 ketik.
  - (3) Posisi bermasalah:
    - tab Posisi (1);
    - seg "Dipegang" (1);
    - menu Susun → Untung % + arah "Rendah dahulu" (2);
    - bermakna ≥ 4 ketik, dan tiada tapisan "hampir paras keluar" dalam Posisi.
    - Alternatif: Ringkasan → Esok → "Hampir paras keluar" (≤ 12 cip di telefon, kemudian "+n lagi" ke Posisi tanpa tapisan) ([html:2324–2332](../../BacktestShariah2/standard/dashboard_v2.html#L2324)).
  - (4) Kesihatan: butang "Data n/8" di pengepala = 1 ketik (tarikh sahaja; lihat S4).
  - (1) Kaedah terbaik: tab Analisis (diaudit penyelidik lain). Dari tab Backtest, pengguna hanya mendapat pingat backtest, bukan bukti hadapan.

### Inferences
- Empat lapis navigasi dan butang "Papar senarai / Lipat semua / Buka semua" adalah tampalan bagi halaman yang terlalu panjang.
- Mengurangkan tab utama kepada sekitar 4 tab akan membolehkan satu baris tab di telefon, iaitu:
  - Hari ini (Esok + Berubah + kesihatan);
  - Kaedah (ranking tunggal + profil);
  - Posisi (ringkasan + jadual);
  - Lagi/Arkib (Backtest mentah, Sektor, Moomoo lama, Panduan).
- Mula pada Ringkasan setiap kali dibuka, bukan tab terakhir yang disimpan, lebih sepadan dengan matlamat "jawapan dalam 10 saat".

### Gaps
- Ketinggian sebenar pengepala melekit di 390px pada versi 102 tidak diukur.

## S7. Sejarah permintaan pengguna di sebalik ciri (untuk dihormati dalam reka semula)

### Takeaway
Hampir setiap ciri dalam lima tab ini lahir daripada permintaan atau kelulusan eksplisit pengguna, kebanyakannya dalam 15–22 Okt 2026. Arah permintaan konsisten:
- mudah difahami pemula (versi 73);
- boleh dibaca di telefon (versi 77–85);
- % bukan USD (versi 95);
- data mesti betul dan lengkap (gred kewangan untuk semua posisi).

Reka semula perlu mengekalkan maksud permintaan ini walaupun bentuknya berubah.

### Cited Findings
- **15 Okt (versi 34):** lajur gred terperinci (Sektor, Industri, RS, Pemangkin + 2 pautan berita, QR Selamat/Berhati-hati/Elak, Gred), masing-masing dengan tooltip ([log+:80–84](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md)).
- **19 Okt:**
  - versi 72: cip Kewangan K/U/T/S "pening" dipermudah ([log+:161](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md));
  - versi 73: "pakai dashboard latest ni sahaja"; disusun semula untuk pemula, 7 tab; Moomoo digabung ke Prestasi/Posisi sebagai pilihan akaun; watchlist "Paras disentuh" + isyarat lengkap berasingan; telefon 10 baris; butang ? Panduan ([log+:163](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md));
  - versi 74–75: lajur "Syarat belum cukup" dan "Pemangkin/Kewangan" diseimbangkan ([log+:166–167](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md));
  - versi 76: kad Portfolio maya 10 slot ([log+:170](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md));
  - `senarai_beli` tidak lagi ditolak ke db ([log+:165](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md)).
- **20 Okt:**
  - versi 77–81: kad telefon Posisi/Watchlist, baris tertutup satu baris ([md:3](../../BacktestShariah2/standard/dashboard.md));
  - versi 82: "kad telefon Posisi sukar dibaca" → kad 3 zon ([log+:200](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md));
  - versi 83–85: kad lipat untuk Backtest/Kaedah/Sektor/Prestasi + menu Susun telefon ([log+:201](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md));
  - versi 87: tab Analisis;
  - versi 89 (pratonton disetujui pengguna): status saluran data "Data n/8", panel Esok, Berubah sejak sesi lalu, ▲▼, BARU, titik status, cip lorong, carta kecil ([md:3](../../BacktestShariah2/standard/dashboard.md));
  - versi 90: kelajuan, `ringkas_c/m`, 7.2 → 3.6 MB;
  - versi 91 (pratonton disetujui): peta portfolio, lajur R, pandangan Ringkas/Penuh/Risiko/Gred ([md:3](../../BacktestShariah2/standard/dashboard.md));
  - gred kewangan untuk semua posisi C atas permintaan ([log+:198](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md)).
- **21 Okt:**
  - versi 92: senarai berikon tab Kaedah (`katPecah`), lajur disembunyi bila tidak muat (`muatLajur`), tajuk jadual melekit;
  - versi 93 (permintaan pengguna): tab sisi panel;
  - versi 94: Ringkasan tab sisi di telefon sahaja ([md:3](../../BacktestShariah2/standard/dashboard.md)).
- **22 Okt:**
  - versi 95: Prestasi dalam % sahaja, bukan USD (permintaan pengguna);
  - versi 96–102: panel Skor kaedah swing, Pantau GANTUNG/BERSARA ([md:3](../../BacktestShariah2/standard/dashboard.md)).
- **Keputusan peraturan yang mempengaruhi paparan:**
  - Moomoo tidak lagi untuk belian ([log+:19](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md));
  - lorong 10% dibuang, 17 Okt ([log+:143](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md));
  - lorong 2 Chandelier, 19 Okt ([log+:154](../../BacktestShariah2/standard/binaan_v2_log_tambahan.md));
  - gred "rekod dan uji dahulu, bukan penapis" ([tugasan_v3.md:80](../../BacktestShariah2/standard/tugasan_v3.md));
  - Sektor maklumat sahaja selepas kalibrasi 13 Okt ([md:21–25](../../BacktestShariah2/standard/dashboard.md)).
- **Peraturan paparan yang dinyatakan:** semua jadual boleh disusun; setiap istilah ada tooltip; kadar menang sentiasa dinamakan asasnya; telefon 10 baris + 25; gaya SST Terminal satu tema gelap ([md:27–36](../../BacktestShariah2/standard/dashboard.md)).

### Inferences
- Permintaan berulang tentang "pening", "sukar dibaca" dan "tidak seimbang" (versi 72, 74, 82) menunjukkan masalah asas ialah kepadatan, bukan susun atur sel. Tampalan setempat sudah mencapai had.
- Reka semula yang membuang lajur gred dari jadual utama perlu mengekalkan akses mudah kepada gred (helaian/kad), kerana pengguna meminta data gred lengkap pada 15 dan 20 Okt.
- Peraturan "% bukan USD" (versi 95) patut diperluas ke Keputusan (RM10k) dan Ringkasan (USD1,000) supaya seragam.

### Gaps
- Fail log tidak merekod reaksi pengguna terhadap tab Sektor, Kaedah atau Butiran selepas versi 85. Tiada bukti sama ada pengguna masih memakainya.
