# Inventori tab operasi dashboard v154: `utama` (Ringkasan), `posisi`, `watch` (Watchlist)

Skop: audit dalaman repo `/home/user/papertrade-claude` pada 6 Nov 2026 (manifes terbit `nombor` 185 = v154, `bait` 683,519). Sumber utama: `BacktestShariah2/standard/dashboard_v2.html` (5,352 baris; disingkat **H**), `BacktestShariah2/standard/jana_db.py` (disingkat **J**), `papertrade/*.csv`, `standard/dashboard.md`, `standard/tugasan_v3.md`, dua audit terdahulu dalam `reports/`. Semua kiraan baris/lajur dikira daripada fail, bukan dianggar. Matlamat pemilik yang dipakai pada setiap penilaian: **SATU kaedah untuk wang sebenar; papertrade banyak kaedah untuk memilih yang paling menguntungkan (rugi kecil, untung besar)** — jadi setiap panel ditanya: (a) bantu pilih kaedah? (b) bantu laksana beli/jual hari ini bagi kaedah terpilih? (c) tiada kedua-duanya?

Kod penilaian: **ESENSIAL** · **REDUNDAN** (sama di tempat lain, dinamakan) · **MATI/TAK DIPAKAI** · **PAPARAN-SAHAJA** (nilai ramalan diukur sifar, dokumen dinamakan) · **HILANG**.

---

## Soalan 1 — Rangka tab: id, paparan, laluan hash, langganan db yang tab ini baca

### Takeaway
Dashboard mempunyai 9 tab (bukan 4 seperti cadangan audit 2); `utama`, `posisi`, `watch` dirender oleh `renderUtama`, `renderPos`, `renderWatch` ke dalam `#v-utama`, `#v-pos`, `#v-watch`. Posisi membaca Papertrade C melalui dokumen PADAT `papertrade/ringkas_c` (bukan `papertrade/claude*` seperti yang `dashboard.md` tulis), dan ketiga-tiga tab bergantung pada 6–10 dokumen db lain (trend, stage, lorong2, garis, harian_kaedah, portfolio_slot, analisis/papan).

### Cited Findings
- 9 butang tab dalam urutan: Ringkasan (`utama`), Analisis, Prestasi, Posisi (`posisi`), Watchlist (`watch`), Backtest, Kaedah, Kombinasi N, Sektor — [H:1060–1068](../../BacktestShariah2/standard/dashboard_v2.html#L1060). Seksyen paparan `#v-utama`, `#v-watch`, `#v-pos` — [H:1079,1086,1087](../../BacktestShariah2/standard/dashboard_v2.html#L1079).
- Peta hash: `#utama`/`#ringkasan` → utama; `#watchlist` → watch; `#posisi`/`#ptm`/`#ptc` → posisi (`#ptm` set akaun `m`, `#ptc` set akaun `cm`) — [H:1136](../../BacktestShariah2/standard/dashboard_v2.html#L1136).
- Pemetaan render: `const R={utama:renderUtama,…,watch:renderWatch,pos…}` — [H:4780](../../BacktestShariah2/standard/dashboard_v2.html#L4780). Fungsi: `renderUtama` [H:4314](../../BacktestShariah2/standard/dashboard_v2.html#L4314), `renderPos` [H:1907](../../BacktestShariah2/standard/dashboard_v2.html#L1907), `renderWatch` [H:1690](../../BacktestShariah2/standard/dashboard_v2.html#L1690).
- Keadaan lalai: `S.tab='utama'`, `S.akaun='cm'` (Papertrade C · Mxx), `S.pos.st='semua'`; tab terakhir dipulihkan daripada `localStorage pbs3_tab` — [H:1128–1132](../../BacktestShariah2/standard/dashboard_v2.html#L1128). Segmen akaun (sub-tab) Posisi: `['cm','Papertrade C · M'],['cn','Papertrade C · N'],['m','Moomoo lama'],['gab','Gabung']` — [H:1116](../../BacktestShariah2/standard/dashboard_v2.html#L1116); `kelN=/^N\d/` jadi `GB02` dikumpul bersama Mxx — [H:1124](../../BacktestShariah2/standard/dashboard_v2.html#L1124).
- Langganan db (fungsi `connect`): `papertrade/ringkas_c` → sandaran `papertrade/claude`, `claude_2`, `claude_3`… tanpa had [H:5325–5331](../../BacktestShariah2/standard/dashboard_v2.html#L5325); `papertrade/ringkas_m` → sandaran `papertrade/moomoo` + `moomoo_peta` [H:5324]; `papertrade/watchlist` (dibahagi) → tab watch & sektor [H:5332]; `harian/status` → `S.hst` [H:5334]; `prestasi/garis` → utama, ptc, prestasi, watch; `prestasi/harian_kaedah` → utama, prestasi, analisis; `posisi/lorong2` → ptc; `posisi/jalur` → ptc; `harian/trend` dan `harian/stage` → ptc, watch [H:5336]; `prestasi/portfolio_slot` → utama, prestasi [H:5337]; `analisis/papan` → analisis (tetapi dibaca oleh Ringkasan melalui `S.anl` dalam `anlSt`, `panelBerubah`, `saluran`) [H:5343]; `kaedah/katalog` → `S.kat` dipakai Ringkasan untuk nama kaedah [H:5345].
- `jana_db.py` menulis dokumen: `papertrade/moomoo`, `papertrade/claude[_N]` (satu dokumen setiap fail CSV), `papertrade/watchlist` (dipetakan daripada tajuk CSV melalui `PETA_WATCH`: `'% hampir'→pct_dipenuhi`, `'Keadaan semasa'→sebab`, `'Syarat belum cukup'→syarat_belum`, `'Paras pencetus'→paras`, `'Jarak %'→jarak_pct`, `'Tarikh masuk watchlist'→ditambah`, `'Hari dalam watchlist'→hari`) [J:31–35](../../BacktestShariah2/standard/jana_db.py#L31), [J:1297–1301]; `prestasi/mae`, `mae_atr`, `ringkasan`, `garis`, `mfe`, `harian_kaedah`, `portfolio_slot`; `harian/trend`, `harian/stage`, `harian/status`; `posisi/lorong2`, `posisi/jalur`; `analisis/papan`, `analisis/lift`; `kaedah_n/papan`; `sektor/snapshot` — senarai nama [J:1152–1381]. `papertrade/senarai_beli` **tidak ditolak ke db sejak 19 Okt 2026** ("halaman tidak membacanya") [J:1293–1294](../../BacktestShariah2/standard/jana_db.py#L1293).
- Dokumen yang dipecah (`PECAH`): watchlist, garis, mfe, mae_atr, harian_kaedah, trend, stage, lorong2, jalur, mae, analisis/papan, kaedah_n/papan, moomoo — [J:1150–1180](../../BacktestShariah2/standard/jana_db.py#L1150).

### Inferences
- `dashboard.md` jadual "Struktur tab" menyatakan Posisi membaca `papertrade/moomoo`, `papertrade/claude*` — laluan sebenar ialah `ringkas_c/m` dahulu; dokumen `claude*` hanya sandaran. Dokumen peraturan sudah hanyut daripada kod (lihat Soalan 9).
- Ringkasan bergantung pada `analisis/papan` (status KUAT/PERHATI dsb.) walaupun langganannya hanya memicu lukis semula tab `analisis`; jika `analisis/papan` tiba selepas Ringkasan dilukis, label status Ringkasan hanya dikemas kini pada lukisan seterusnya (tidak disahkan secara runtime — inferens daripada `subBhg('analisis/papan','anl',['analisis'])`).

### Gaps
- Tidak dapat menjalankan halaman (tiada Chromium dalam sesi ini) untuk mengesahkan susunan render sebenar; susunan di bawah ialah susunan rentetan `innerHTML` dalam kod.

---

## Soalan 2 — Tab `utama` (Ringkasan): senarai panel dalam urutan render, sumber, soalan yang dijawab, penilaian

### Takeaway
Ringkasan merender 11 blok dalam urutan tetap; semuanya Papertrade C (Mxx + Nxx digabung melalui `prSrc('c')`). Hanya DUA blok membantu pelaksanaan harian (Esok; Berubah) dan SATU blok menyentuh "kaedah mana" (Terbaik ikut papertrade, tetapi ia purata mentah ≥20 selesai tanpa pembetulan pelbagai ujian dan tanpa paksi Nxx-vs-Mxx yang adil). Angka hero/KPI mencampur untung belum direalisasi dengan selesai — kiraan semula atas CSV menunjukkan Mxx **−1.27%/posisi** (selesai −4.82%, menang 15%) dan Nxx **−5.17%**; jumlah **−14,390 mata** (Mxx) dan **−17,625 mata** (Nxx), iaitu −USD143,898 dan −USD176,250 pada USD1,000 setiap posisi.

### Cited Findings (urutan render `renderUtama`, [H:4336–4373](../../BacktestShariah2/standard/dashboard_v2.html#L4336))
1. **Hero "Purata setiap belian · Papertrade C"** (`heroUtama`, [H:4305–4313]): angka besar = purata `hasil` semua posisi C (selesai = untung akhir, dipegang = semasa); delta sejak sesi lalu (`semalam()`); "SPY tempoh sama" = purata `spyPos` [H:2879]; "USD1,000 setiap belian" = jumlah mata ×10 [H:4320,4309]; ayat bilangan belian/kaedah/dipegang/keluar; sparkline terkumpul daripada `prestasi/harian_kaedah` baris `a='C',k='Semua'` (`hkSemua`, [H:2980]). Soalan dijawab: "berapa purata setiap belian setakat ini?" — **tidak** menjawab "kaedah mana". Penilaian: **REDUNDAN** dengan kad KPI "Keseluruhan" tepat di bawahnya (angka dan sparkline `kum` yang sama, [H:4347]) dan dengan tab Prestasi; penanda aras SPY bercanggah dengan CLAUDE.md "Guna SPUS, bukan SPY" dan `REVERSE/PENANDA_ARAS_SYARIAH.md`.
2. **Jalur status data `salStrip`** ([H:3318]; takrif `saluran()` [H:3261–3279]): 8 cip — Harga & posisi (`harian/status.harga_tutup_pada`), Belian 9:35 NY (`beli_pada`), Watchlist (`tarikh_data`), Harga tinggi/rendah (`prestasi/mae.harga_hingga`), Lejar Penuh (`analisis/papan.lejar_sesi`), Penganalisis (`harga_pada`), Portfolio 10 slot (`sesi_terakhir`), Sektor mingguan (`sektor/snapshot.dibina`); ambang 39.5 jam / 16 jam (v147). Penilaian: **ESENSIAL untuk pelaksanaan** (tahu data basi sebelum bertindak) tetapi **REDUNDAN** dengan butang kepala "Data n/8" (`renderSal`, [H:3279]) yang membaca `saluran()` yang sama — maklumat yang sama dipaparkan dua kali pada skrin pertama.
3. **"Peluang teratas ikut sektor"** (`panelPeluang`, [H:2953–2978]): 5 sektor × (1 kad + 3 baris) posisi terbuka paling untung; cip bulat = `rs_rating`; sparkline sejak beli (`prestasi/garis`). Nota kaki panel sendiri: "Ini paparan — bukan cadangan beli atau jual" [H:2977]. Penilaian: **PAPARAN-SAHAJA** (RS rating: `kajian/rs/RINGKASAN.md` §22 — gred A lebihan 63 hari +1.24 mata CI95 [0.29, 2.18], B +0.23 tidak signifikan, C–E ≤ 0; tugasan_v3 §8 "RS tidak dikira dalam gred keseluruhan"); tidak membantu memilih kaedah (susunan ikut saham/sektor, bukan kaedah).
4. **"3 perkara utama"** ([H:4330–4334, 4342–4343]) + `blokExplainer` ([H:2599–2611]): ayat 1 = purata selesai/menang/dipegang; ayat 2 = sebab keluar teratas + median hari + amaran "dagangan rugi keluar dahulu"; ayat 3 = bilangan kaedah ≥ 20 selesai + kiraan status Papan Penganalisis (KUAT/PERHATI/AMARAN/LEMAH/BELUM CUKUP) + "terlalu awal". `blokExplainer` = 4 bar "Selesai untung / Selesai rugi / Dipegang untung / Dipegang rugi" dalam **mata** dan Jumlah. Penilaian: **ESENSIAL (sebahagian)** — `blokExplainer` ialah satu-satunya tempat dalam 3 tab yang menjawab "berapa rugi lawan untung" secara dipecah; ayat 1–2 **REDUNDAN** dengan kad KPI; ayat 3 **REDUNDAN** dengan panel "Terbaik ikut papertrade" (kiraan status yang sama `cnt` dipaparkan dua kali [H:4334 dan H:4353]).
5. **4 kad KPI** ([H:4344–4349]): Dagangan selesai (purata, delta, spark `kum`, menang, n), Masih dipegang (purata, spark `n`), Keseluruhan (purata, spark `kum`, menang (semua), USD1,000), Aktiviti terkini (dibeli/keluar pada tarikh terkini, spark `beli`). Penilaian: **REDUNDAN** dengan hero (Keseluruhan = angka hero; spark `kum` dilukis TIGA kali: hero, kad 1, kad 3) dan dengan `ptKpis` tab Posisi [H:1852–1860]. Tiada kad menamakan kaedah.
6. **"Esok · buka <tarikh>"** (`panelEsok`, [H:3288–3303]): 4 blok cip — Dijual pada buka (`statusPos`[0]==='m' = isyarat "menunggu" lorong 1 atau 2 [H:2893–2896]), Dibeli pada buka (watchlist `wLengkap` && `wBeli().k==='tunggu'` [H:3290]), Hampir paras keluar (`statusPos` 'h': lorong 2 < 25% julat atas paras ATAU henti kaedah < 2% bawah harga [H:2897–2899]), Earnings ≤ 10 hari dagangan (`hariKeEarn`). Had telefon 12 cip, desktop 24 [H:3293]. Penilaian: **ESENSIAL untuk pelaksanaan** — satu-satunya panel yang menjawab "apa dijual/dibeli esok"; tetapi ia merentas SEMUA 222 kaedah (tiada tapisan kaedah), jadi bagi "kaedah terpilih" pemilik perlu mengecam ID dalam cip.
7. **"Berubah sejak sesi lalu"** (`panelBerubah`, [H:3304–3317]): dibeli, keluar lorong kaedah, keluar selagi naik, masuk watchlist, perubahan kedudukan Analisis (6 teratas, `kedudukan_sebelum`). Penilaian: **ESENSIAL (ringan)**; separuh REDUNDAN dengan kad "Aktiviti terkini" (nombor dibeli/keluar sama).
8. **"Terbaik ikut papertrade"** ([H:4352–4357]): senarai kaedah dengan ≥ `PR_MIN_TUTUP` (20) dagangan selesai, disusun purata menurun; pil status Papan Penganalisis; `awalPill` "terlalu awal"; blok `adilH` "Bila label boleh dipercayai"; "Paling hampir dinilai". Sumber: `prStats(prSrc('c'))` (semua C termasuk Nxx) + `S.anl`. Penilaian: **satu-satunya panel 'kaedah mana' dalam 3 tab — tetapi lemah**: purata mentah (tiada SE berkelompok hari beli, tiada BH-FDR) sedangkan `laporan/KAEDAH_TERBAIK.md` (CLAUDE.md) mendapati "25 terbukti NEGATIF, 0 terbukti positif" dan "jangan pilih kaedah ikut pangkat papan"; ia REDUNDAN dengan tab Analisis (Kedudukan + panel Lift v154) yang mengira dengan betul. Pautan "Lihat tab Analisis" disediakan [H:4357].
9. **"Untung lawan risiko"** scatter (`drawPrScatter`, [H:4358, 2144]) + `legendKpt` (bentuk = status Papan). Penilaian: **REDUNDAN** — scatter yang sama dilukis dalam tab Prestasi (`drawPrScatter` dipanggil di [H:2193] kawasan Prestasi); audit 1 sudah mengesyorkan BUANG.
10. **"Terbaik ikut backtest"** podium 3 kaedah berpingat (`kpData`, `kpPod` [H:1290, 4360–4361]). Sumber: `registry/*` set 431 + `kaedah/katalog`. Penilaian: **REDUNDAN** dengan tab Backtest › Keputusan dan **menyesatkan untuk 'kaedah mana'**: CLAUDE.md KAEDAH_TERBAIK (4) "AUTOTUNE 2000 saham AS 0/134 … ≥ 2 daripada 3: 0" dan (1) "pangkat backtest tiada kuasa ramalan yang boleh diukur (rho +0.16, p 0.105)".
11. **"Eksperimen"** ([H:4362–4371]): (a) Dua lorong keluar — purata lorong kaedah `L1` lawan selagi naik `L2`, ayat "Lebih untung setakat ini" jika kedua-dua ≥ 20 keluar; (b) Gred saham: `gredRingkas` [H:2663–2670] A lawan gred terendah cukup data bagi Industri/RS/Pemangkin/QR (Sektor dikecualikan); (c) `pslotKad` [H:2654–2662] RS_10 lawan RAWAK_10 lawan SPY daripada `prestasi/portfolio_slot`. Penilaian: (a) **ESENSIAL untuk reka bentuk keluar** tetapi REDUNDAN dengan `ptKpis` Posisi kad 3 "Purata ikut lorong keluar" dan panel Prestasi "Banding dua lorong" [H:2107]; (b) **PAPARAN-SAHAJA/eksperimen** (gred belum terbukti; tugasan_v3 §8 "rekod dan uji dahulu"); (c) **tidak menjawab soalan pemilik** — `pslotKad` hanya memapar RS_10 & RAWAK_10 (`ks=['RS_10','RAWAK_10']`) walaupun `portfolio_slot/` ada 6 lorong + jalur 20 benih; CLAUDE.md: "Baca persentil jalur, bukan beza antara dua lorong" — panel ini memaparkan tepat beza dua lorong yang CLAUDE.md kata tidak bermakna.
12. **Strip "Cara baca"** [H:4372] dan **kaki Moomoo** [H:4373]: teks tetap + pautan Panduan. Penilaian: **REDUNDAN** dengan butang "?" Panduan.

### Inferences
- Kiraan audit atas `claude*.csv` (6 Nov 2026, baris dibeli & sah): Mxx+GB purata **−1.27%** (n 11,308), selesai **−4.82%** (n 5,745, menang 15%), dipegang **+2.39%** (n 5,563); jumlah **−14,390 mata** = **−USD143,898** pada USD1,000/posisi. Nxx purata **−5.17%** (n 3,412), selesai **−4.61%** (n 476, menang 20%), dipegang **−5.26%** (n 2,936); jumlah **−17,625 mata** = **−USD176,250**. Angka hero lalai menggabungkan kedua-dua keluarga (`prSrc('c')`) sedangkan sub-tab Posisi/Prestasi memisahkannya — Ringkasan tidak ada pemisah Mxx/Nxx.
- Dua panel memaparkan status Papan Penganalisis yang sama (ayat 3 "3 perkara utama" dan tajuk "Terbaik ikut papertrade"); sparkline `kum` dilukis 3 kali; purata selesai/dipegang muncul 3 kali (hero ayat, ayat 1, kad KPI). Skrin pertama di telefon (2 kad sebaris, hero 2.5rem [H:276,489]) dihabiskan oleh nombor yang sama.
- Tiada panel Ringkasan menyebut SPUS, matlamat 10%/bulan, atau Lift (v154 meletakkan Lift di tab Analisis sahaja).

### Gaps
- `spyPos` (SPY tempoh sama) bergantung pada `prestasi/garis.spy`; tidak disahkan sama ada nilainya tersedia bagi semua posisi (jika tiada, "beza" dibiarkan kosong — kod menangani, tetapi liputannya tidak diukur).

---

## Soalan 3 — Tab `posisi`: panel, 4 pandangan jadual dan lajurnya, sumber, penilaian

### Takeaway
Posisi = 1 headline + 4 kad KPI + Peta portfolio (treemap posisi, bukan saham) + jadual "Posisi & keputusan" (baris rejim, kad "Perlu perhatian", segmen Semua/Dipegang/Sudah keluar, 4 pandangan Ringkas/Penuh/Risiko/Gred, tapis kaedah/sektor/industri/carian) + panel "Isyarat tidak dibeli". Pada akaun lalai `cm` jadual "Semua" memuatkan **11,441** baris Mxx (5,571 dipegang lorong 1), `cn` **3,419** Nxx (2,936 dipegang). KPI dan Peta **tidak** mengikut tapisan kaedah — cadangan audit 1 belum dilaksanakan. Setiap pandangan (termasuk Ringkas) membawa 3–4 lajur PAPARAN-SAHAJA (Trend, Risiko ATR, 52w, Stage) di hadapan lajur keputusan.

### Cited Findings (urutan render `renderPos`, [H:1907–1935](../../BacktestShariah2/standard/dashboard_v2.html#L1907))
1. **Headline akaun** [H:1915–1918]: teks tetap ikut `S.akaun` (cm/cn/m/gab) + `harga_pada`. Penilaian: ESENSIAL (konteks) tetapi panjang di telefon.
2. **4 kad KPI `ptKpis(all,…)`** [H:1852–1860]: Posisi (n sah, bilangan kaedah, kena isyarat keluar, n tidak sah/tidak dibeli), Purata untung, Purata ikut lorong keluar (kaedah · selagi naik; keluar n · n; tutup semua n), Sedang untung n/N. **Dikira atas `all` (semua akaun), bukan `fb.apply(base)`** [H:1921] — tapisan kaedah tidak mengubah KPI. Penilaian: **REDUNDAN** dengan kad KPI Ringkasan (purata sama) dan **tidak membantu pilih kaedah** kerana tidak mengikut tapisan.
3. **Peta portfolio `panelPeta`** [H:3794–3801] + `blokKomposisi` + `blokKepekatan` [H:2585–2597] + treemap `drawPeta` [H:3781]: "saiz = bilangan [posisi], warna = untung purata"; ketik kotak menapis jadual (`pilihPeta`). Kepekatan: ambang sektor ≥ 25%, saham dalam ≥ 8 kaedah, kaedah ≥ 8% portfolio. Penilaian: **tidak menjawab kedua-dua soalan** — ia mengukur pertindihan isyarat (kiraan audit: 5,571 posisi Mxx dipegang hanya **654 saham unik**; LFST 41 posisi, EXLS 40, SBH 39; Nxx 2,936 posisi dalam 407 saham; SWK/XNCR/EXPD 50–51 posisi) bukan pendedahan portfolio sebenar; audit 1 ([reports/Audit dashboard tab demi tab.md:125](../../reports/Audit%20dashboard%20tab%20demi%20tab.md)) sudah menyatakan "Peta mengira posisi, bukan saham" — belum dibetulkan.
4. **Panel "Posisi & keputusan"** [H:1922]: sub "n posisi · ketik baris · ketik tajuk". Di dalamnya:
   - `rejimHtml()` [H:4279]: "Rejim pasaran: SPY <Bullish/Neutral/Bearish> · RV21 n% (Biasa/Tenang/Tertekan)" daripada `harian/trend.rejim` (nilai 6 Nov: `spy_s` 0, `rv21` 19.9, label Biasa — `data/trend/status.json`). Penilaian: **PAPARAN-SAHAJA** (laporan trend §"Jangan papar": Bullish tidak bermaksud selamat dalam rejim tertekan; tiada peraturan beli/jual terikat).
   - `panelPerhatian(peg)` [H:3016–3045]: kad per kategori Jual pada buka / Hampir paras keluar / Earnings hampir / Tidak sah, 1 kad + 3 baris setiap satu, cip RS. Penilaian: **ESENSIAL untuk pelaksanaan** tetapi **REDUNDAN** dengan `panelEsok` Ringkasan (sumber `statusPos` dan `hariKeEarn` yang sama).
   - Komen v152 [H:1924]: blok "Gred sekali pandang" **dibuang sementara** daripada Posisi (kekal di Watchlist).
   - Segmen status `posSt`: Semua (n) / Dipegang (n) / Sudah keluar (n) [H:1926]; "Dipegang" = `!r.keluar` iaitu **lorong 1 sahaja** [H:1909] — posisi yang lorong 2 masih buka tetapi lorong 1 keluar jatuh ke "Sudah keluar" (kiraan audit: Mxx lorong 2 masih buka **9,498** lawan lorong 1 **5,571**; Nxx 3,409 lawan 2,936).
   - Telefon: `lajurSeg('pos')` Ringkas/Penuh; desktop: `pandSeg()` Ringkas/Penuh/Risiko/Gred [H:1926, 3811]; pilihan disimpan `localStorage pbs3_pandangan`.
   - Bar tapis `ptFilterBar` [H:1877–1880]: `<select>` kaedah, `selSI` sektor/industri, carian saham/sektor/industri. Tapisan **hanya** mengubah jadual.
   - `sortTable` susunan lalai `untung_pct` **menurun** [H:1927] (bukan ikut risiko/tindakan). Had baris: telefon 10 awal +25 setiap "Papar lagi", desktop 25 +100; "Papar semua" hanya jika ≤ 400 baris [H:1862–1865].
5. **Panel "Isyarat tidak dibeli"** [H:1929–1933]: baris `tidak_dibeli` ikut keluarga akaun; lajur Tarikh, Saham, Kaedah, Harga buka, Henti, Sebab. Kiraan: **101** baris `tidak_dibeli` dalam `claude*.csv`. Penilaian: **ESENSIAL untuk pilih kaedah** (kadar isyarat tidak boleh dilaksana ialah sifat kaedah) tetapi tidak diagregat ikut kaedah; audit 1 mencadangkan pindah ke "Sistem" — kekal di sini.

**Lajur setiap pandangan** (lajur dengan `v:`/`f:` dikira; `MKAD`/`BTN_PENUH` ialah sel kad telefon, bukan lajur desktop):
- **Ringkas `posColsR`** [H:1897–1906] — 11 lajur: Saham (+titik status, pil akaun, cip earnings/keluar) · **Trend `TRC`** · **Risiko `RSC`** · **52w `J52C`** · **Stage `STC`** · Untung % (+harga beli→kini, cip SPY) · Sejak beli (sparkline) · Kaedah · Tarikh beli · Hari (`hariSel` bar had masa) · Gred (`gred_keseluruhan`) · Keluar kaedah (`lorongRingkas`: Pegang/Tunggu/Keluar + sebab). 4 daripada 12 sel ialah PAPARAN-SAHAJA dan diletakkan SEBELUM Untung %.
- **Penuh `ptCols`** [H:1837–1851] — 16 lajur + 5 gred = 21 (desktop tidak padat): Tarikh beli · Saham · Kaedah (+kongsi) · **Trend+ATR `TRCA`** · **52w** · **Stage** · Harga beli · Unit · Harga terkini · Untung % · R (`kp-lo`) · Sejak beli (`kp-lo`) · Hari pegang (KK) · Keluar kaedah · Hari pegang (PSN) (`kp-hi`) · Pegang selagi naik (`kp-hi`) · `grCols()` 5 lajur: Sektor (`kp-lo`) · Industri (`kp-hi`) · RS (`kp-hi`) · QR (`kp-lo`) · Gred [H:1829–1835]. Pemangkin dan Kewangan dibuang daripada jadual 28 Okt 2026 (v122) tetapi kekal dalam helaian [H:1834 komen].
- **Risiko `posColsP('risiko')`** [H:3815–3829] — 13 lajur: Saham(+kaedah) · Untung % · **Trend** · **Risiko** · **52w** · **Stage** · R · Risiko awal (henti) · Turun maks (`prestasi/mae`) · Naik maks (`prestasi/mfe`) · Ke henti kaedah (jarak %) · Lorong 2 (bar + paras) · Hari · Keluar kaedah.
- **Gred `posColsP('gred')`** [H:3818] — 12 lajur: Saham · Untung % · Trend · Risiko · 52w · Stage · Tarikh beli · Sektor · Industri · RS · QR · Gred.
- Helaian butiran `openPos` [H:2806–2835]: pil Trend/Stage/ATR, verdict `pdVerdikt`, KPI, "Di mana harga berdiri" tangga, carta sejak beli / ulang tayang lorong 2 (`rpPos`, `posisi/lorong2`), "Jalur jangkaan ke hadapan" (`jlPos`, `posisi/jalur`; `standard/jalur_jangka.py` dan `REVERSE/SILING_ARAH.md` kini ADA dalam repo), Dua lorong keluar, kecekapan, gred penuh, nombor mentah, Trend & Stage penuh.

### Inferences
- Lajur **input keputusan** (bantu laksana jual/pegang kaedah terpilih): Keluar kaedah (status lorong 1 + sebab), Pegang selagi naik / Lorong 2 (paras Chandelier), Ke henti kaedah, Risiko awal (henti), Hari pegang (KK) lawan had masa, Tarikh beli, Kaedah, Untung %, cip earnings. Lajur **PAPARAN-SAHAJA** (lihat Soalan 4): Trend, Risiko ATR (ukuran risiko sah tetapi "bukan isyarat jual"), 52w, Stage, Sektor, Industri, RS, QR, Gred keseluruhan, cip RS dalam kad, Rejim.
- Dalam pandangan **Ringkas** — pandangan yang dimaksudkan untuk telefon/laju — 4 daripada 11 lajur (36%) ialah PAPARAN-SAHAJA dan 1 lagi (Gred) belum terbukti; hanya 3 lajur (Untung %, Hari, Keluar kaedah) ialah input tindakan harian.
- Lorong 2 (Chandelier 4×ATR14) ialah dapatan terkuat repo untuk "untung besar" (`kajian/KAJIAN_LORONG2.md`: purata +5.1% lawan lorong 1 +2.7%, trend besar 25.1% lawan 12.0%, atasi lorong 1 dalam 80% kaedah) tetapi dalam pandangan Ringkas paras lorong 2 **tiada** (hanya dalam Penuh/Risiko dan helaian) — lajur yang paling bernilai untuk keputusan "pegang" disembunyikan di belakang 4 lajur hiasan.

### Gaps
- `pdVerdikt` (teks verdict helaian) tidak dibaca penuh; tidak dinilai sama ada ia memakai takrif "hampir keluar" yang sama dengan `statusPos`.
- Tidak disahkan secara runtime berapa lajur `muatLajur` sembunyikan pada 1,400px bagi pandangan Penuh (bergantung lebar fon); hanya logik keutamaan (`kp-lo` dahulu, `kp-hi` akhir) dibaca.

---

## Soalan 4 — Lajur PAPARAN-SAHAJA lawan input keputusan: bukti repo bagi setiap satu

### Takeaway
Repo sendiri sudah mengukur dan melabel sifar/kecil nilai ramalan bagi Trend D10H2, Stage, 52W, Sektor, Gred keseluruhan, skor panas/fasa sektor; RS dan Industri mempunyai kesan kecil tetapi signifikan (RS A +1.24 mata/63 hari; Industri A +0.03 … E −1.21 relatif) dan **sengaja bukan penapis** (keputusan pengguna). Tiada satu pun daripada lajur ini menjawab "kaedah mana" — semuanya sifat SAHAM pada hari isyarat, bukan sifat KAEDAH.

### Cited Findings
- **Trend (D10H2-r2)** — `reports/Penentuan status trend saham mendalam.md:126`: "tidak boleh meramal pulangan 3–30 hari secara stabil, tidak menambah maklumat risiko yang boleh dipercayai melebihi ATR%, tidak memberi masa jual yang lebih baik daripada lorong 1 atau lorong 2 … tidak boleh dipakai untuk menyusun Watchlist"; §5: beza Bullish−Bearish 21 sesi −1.19 mata (IS, t −1.3) lawan +1.54 (OOS, t 2.2) — tanda bertukar. `data/trend/status.json.takrif`: "Rekod sejarah, bukan isyarat jual" (947 baris, tarikh 20261105). CLAUDE.md: "Paparan sahaja (kajian 23 Okt 2026: tidak meramal pulangan 3–30 hari; bukan penapis atau peraturan jual)". Lajur: `TRC` [H:4157], `TRCA` [H:4165] — dipakai dalam SEMUA 4 pandangan Posisi dan 2 pandangan Watchlist.
- **Risiko ATR14% + kuintil** — tooltip `atr_risiko` [H:4846]: "ukuran risiko yang lulus ujian luar sampel … Maklumat, bukan peraturan saiz posisi atau isyarat jual"; laporan trend §29 "Risiko yang boleh diukur datang daripada ATR, lorong 2 dan earnings". Penilaian: **ukuran risiko sah** tetapi paparan — ia tidak dipakai dalam saiz posisi (1 unit setiap posisi, tugasan_v3 §4) kecuali lorong RISIKO_10 portfolio maya.
- **52w (`J52C`)** — komen kod [H:4167–4174] dan `REVERSE/JARAK_52W.md` (10,468,053 bar 2012–2025): "sebagai PENAPIS ia GAGAL (band 0%…−2% lift −1.34 mata pada 21 sesi dan −5.76 pada 126 sesi, tingkap tahan)"; sebagai urutan IC +0.032…+0.116, "kelebihan HABIS kira-kira −10%"; kod: "PAPARAN SAHAJA: bukan penapis belian, bukan isyarat jual". Ditambah v150 (4 Nov 2026) atas permintaan pengguna.
- **Stage (`STC`)** — `data/stage/status.json.takrif`: "Paparan sahaja: bukan penapis belian, bukan isyarat jual"; CLAUDE.md: "belum diuji sebagai peramal"; 947 baris, kiraan 6 Nov: Stage 2 226, 4 242, 1/3 164, 4A 104 …
- **Sektor (`gred_sektor`)** — `kajian/KAJIAN_GRED_KUMPULAN.md:52`: "tidak membantu memilih saham (semua definisi t < 2 atau bertukar arah H1/H2) … Gred Sektor v2 = % > SMA200, paparan sahaja"; tugasan_v3 §8.2: "paparan sahaja … tidak dikira dalam gred_keseluruhan". Kelas tajuk `kp-lo` (disembunyi dahulu) [H:1830].
- **Industri (`gred_industri`)** — tugasan_v3 §8.1: "A +0.03%, B −0.18%, C −0.40%, D −0.89%, E −1.21%; A dan E signifikan, B–D hampir neutral"; "Tidak terpakai bagi 15 kaedah pantulan". Kesan kecil, direkod bukan penapis.
- **RS rating / gred RS** — `kajian/rs/RINGKASAN.md` §22 (skema `gred.py`, 63 hari): A (90+) lebihan ikut tarikh **+1.24** [CI95 +0.29, +2.18], t 2.57; B +0.23 [−0.24, +0.69]; C −0.07; D −0.21; E −0.29; §24: A 90–94 disahkan +1.53 lawan tidak disahkan +0.68 (t 0.87). tugasan_v3 §8: "RS tidak dikira [dalam gred keseluruhan]". Cip RS muncul dalam kad Peluang [H:2963], Perhatian [H:3029], Watchlist kad [H:3058] dan lajur RS (`kp-hi`).
- **QR (hari ke earnings)** — tooltip `g_q` [H:4974]: risiko lompat henti E 5.7×, D 3.8× … lawan > 30 hari — ukuran RISIKO peristiwa (kajian 659k dagangan). Penilaian: input pelaksanaan yang sah (bila TIDAK memegang merentas earnings) — tetapi sebagai gred ia "direkod untuk diuji".
- **Gred keseluruhan** — tooltip `gred` [H:4975]: "Direkod untuk diuji, belum terbukti meramal dan bukan penapis belian"; `papertrade/SKEMA.md`: "paparan sahaja; belum diuji".
- **Pemangkin, Kewangan** — dibuang daripada jadual v122 (28 Okt 2026), kekal dalam helaian `pdGred`/`gredList` [H:2612]; Pemangkin v3 "bukti lemah" (SKEMA.md).
- **Rejim pasaran** (`rejimHtml`) — `harian/trend.rejim`; laporan trend: "menjual kerana Bearish paling merugikan dalam rejim [tertekan]" — baris teks dipaparkan atas jadual Posisi dan Watchlist tanpa peraturan terikat.
- **Skor panas / fasa sektor** — `dashboard.md` "Kalibrasi tab Sector": "skor panas dan fasa TIDAK digunakan sebagai penapis atau keutamaan beli"; tidak dipaparkan dalam 3 tab ini (hanya tab Sektor).
- **Input keputusan sah** (bukti repo): lorong 2 Chandelier (`kajian/KAJIAN_LORONG2.md` jadual: dipilih +5.1% purata, lebihan SPY sebulan +1.2%, atasi lorong 1 pada 80% kaedah), henti kaedah/`Ke henti kaedah`, `hari` lawan had masa (katalog), `isyarat_keluar` lorong 1, `tarikh_isyarat`/`tarikh_beli`, earnings ≤ 10 hari (`hariKeEarn`), `tidak_dibeli`/`tidak_sah`.

### Inferences
- Dalam Ringkas Posisi dan Ringkas Watchlist, susunan lajur meletakkan 4 lajur paparan (Trend, Risiko, 52w, Stage) tepat selepas Saham, sebelum Untung %/% hampir — iaitu kedudukan paling berharga pada skrin sempit diberi kepada data yang repo sendiri labelkan "bukan isyarat". Satu-satunya lajur paparan dengan ukuran risiko yang lulus luar sampel ialah ATR (tooltip `atr_risiko`).
- Kesemua lajur gred/trend/stage/52w ialah **sifat saham**, bukan sifat kaedah; ia tidak boleh membantu memilih kaedah melainkan diagregat ikut kaedah (tiada agregat sedemikian dalam 3 tab).

### Gaps
- Kajian "Prestasi ikut gred" (adakah gred A lebih untung) belum matang — `gredRingkas` menunjukkan "belum cukup data" apabila < 20 dagangan tertutup gred A; nilai sebenar pada 6 Nov tidak dikira dalam audit ini.

---

## Soalan 5 — Berapa posisi dipaparkan; kebolehgunaan telefon; tapisan dan susunan

### Takeaway
Fail `claude*.csv` (154 fail, 14,961 baris, 61 lajur) memberi Posisi lalai (`cm`) **11,441 baris** "Semua" / **5,571** "Dipegang" / **5,870** "Sudah keluar"; sub-tab `cn` **3,419 / 2,936 / 483**; Moomoo lama 208 (48 belum keluar). Di telefon jadual menjadi kad 10 baris + "Papar lagi" 25 (tiada "Papar semua" kerana > 400), tanpa skrol mendatar (dibuang v113); jadual desktop 11–21 lajur bergantung pandangan, dengan `muatLajur` menyembunyikan lajur `kp-lo` dahulu dan nota "Lajur disembunyi…". Tapisan: kaedah (select), sektor, industri, carian; susunan: klik tajuk, lalai untung menurun.

### Cited Findings
- Kiraan CSV (6 Nov 2026): 154 fail `claude*.csv`, 14,961 baris, 61 lajur (`tarikh_beli … kewangan_butiran`); `tidak_dibeli` 101; `tidak_sah` (dibeli) 140; dibeli 14,860. Mxx+GB: 11,441 dibeli (lorong 1 belum keluar 5,571; `tutup_semua` belum 9,662; 129 kaedah; 857 saham); Nxx: 3,419 dibeli (2,936; 3,409; 94 kaedah; 428 saham). `moomoo.csv` 208 baris, 48 belum keluar. (Kiraan sendiri dengan `csv.DictReader`; CLAUDE.md menyebut 1,641 posisi Nxx pada 4 Nov — kini 3,419 selepas dua sesi lagi.)
- `status_harian.json.malam` (sesi 2026-11-05): `menunggu` 605 (isyarat keluar menunggu buka esok), `keluar_baru_jumlah` C 1,102 (henti 641, isyarat 413, masa 26, sasaran 22), `keluar_keluarga` M 848 / N 254, `menunggu_keluarga` M 251 / N 349.
- `posRows(a)` menapis `tidak_dibeli` sahaja; `tidak_sah` kekal dalam "Semua" (KPI pakai `sahSahaja`) — [H:1888–1892, 1852].
- Had baris: `LAGI=TELEFON?25:100, AWAL=TELEFON?10:25`; "Papar semua" hanya `t<=400` — [H:1862–1865]. Pada 5,571 baris Dipegang di telefon: 10 kad, kemudian +25 setiap ketik, "Papar semua" tiada.
- Telefon (≤ 760px): `thead` menjadi deretan butang susun; setiap `tbody tr` menjadi kad grid 2 lajur dengan label `::before` (`data-label`) — [H:473–488]; jadual bergred `tw-grd` kad grid 6 lajur, sel Saham span 3 bersaiz 1.12rem — [H:609–616]. `TELEFON`/`skrinKecil` = `max-width:760px` [H:1127, 2491]. Kad telefon pandangan Penuh = `MKAD` (`kadPos` [H:2528–2532]: saham, kaedah · hari, untung %, harga beli→kini, unit, tarikh, sparkline 300×64, pil tidak sah, dua lorong `mkLorong`, gred `mkGred`, nota).
- Skrol mendatar dibuang v113 (28 Okt 2026) kerana tajuk melekit timbul di tengah; v110 lalai jadual bergred = semua lajur boleh skrol; v112 permintaan pengguna "saya takmau scroll ke kanan" — `dashboard.md` fragmen versi 110–113. Logik `muatLajur` [H:4803–4830]: lajur disembunyi kanan→kiri kecuali lajur pertama/`frz`/`m0`/`tk`/`utg`; keutamaan `kp-lo` (R, Sejak beli, QR, Sektor) dahulu, `kp-hi` (Industri, RS, Pegang selagi naik, Hari PSN) akhir; nota "Lajur disembunyi kerana skrin tidak cukup lebar: …".
- Bilangan lajur (dikira daripada definisi): Posisi Ringkas 11 · Penuh 21 (16 + 5 gred; 3 lajur harga/unit disembunyi dalam mod `padat`) · Risiko 13 · Gred 12; Watchlist Ringkas 10 · Penuh 17. Semua melebihi 6 lajur.
- Saiz teks telefon: `@media (max-width:520px) … th,td{padding:7px 10px} table{font-size:.86rem}`; `.kpis` 2 lajur, `.kpi .v` 1.3rem [H:462, 489]; hero 2.5rem [H:276].
- Tapisan Posisi: `ptFilterBar` kaedah/sektor/industri/carian [H:1877–1880]; tapis Peta ketik kotak [H:3802–3805]; segmen status; pandangan. Susunan lalai `untung_pct` menurun [H:1927]; `sortTable` boleh susun mana-mana lajur (`dashboard.md` "Semua jadual boleh disusun").
- v151 (5 Nov 2026): Ringkasan dan Posisi memakai "senarai bahagian" (rel kiri desktop / jalur cip melekit telefon) — satu panel dipaparkan pada satu masa; lalai Posisi = "posisi & keputusan", Ringkasan = Gambaran — [H:5063–5071].
- v153 (5 Nov 2026): "Papar lagi" tidak melompat ke atas (`kekalSkrol`) — [H:1866–1876].

### Inferences
- Jadual 5,571 (atau 11,441) baris dengan 10 kad awal + 25 setiap ketik memerlukan ~220 ketikan untuk sampai ke hujung di telefon; tanpa tapis kaedah ia tidak boleh dibaca. Dengan tapis kaedah tunggal (contoh 1 daripada 129), purata ~43 posisi Mxx (5,571/129) — boleh dibaca, tetapi KPI/Peta di atasnya tidak berubah, jadi pemilik tidak mendapat ringkasan kaedah yang ditapis.
- Pandangan Risiko/Gred tidak tersedia di telefon (`pandOf()` pulang '' bila `skrinKecil()` [H:3810]); telefon hanya Ringkas/Penuh. Lajur `Lorong 2` (paras Chandelier) hanya dalam Risiko/Penuh → di telefon ia hanya kelihatan dalam kad Penuh (`mkLorong`) atau helaian.
- Nama lajur panjang ("Hari pegang (KK)", "Hari pegang (PSN)", "Pegang selagi naik", "Keluar kaedah") menjadi label `::before` 0.64rem huruf besar dalam kad — boleh dibaca tetapi padat.

### Gaps
- Tiada ukuran runtime (ketinggian kad, bilangan skrol) — `ujian/semak_dashboard.js` menyokong lebar tersuai tetapi tidak dijalankan dalam audit ini.

---

## Soalan 6 — Blok KPI `utama`: kad, lampu Data n/8, SPUS/SPY; adakah ia menjawab "kaedah mana" atau "berapa rugi lawan untung"

### Takeaway
Blok KPI (hero + 4 kad) menjawab "purata setiap belian" dan "aktiviti"; tiada kad menamakan kaedah dan tiada kad SPUS (hanya SPY tempoh sama). "Berapa rugi lawan untung" dijawab separa oleh `blokExplainer` (4 bar mata + Jumlah) dan oleh "USD1,000 setiap belian" — tetapi angka itu menggabungkan 222 kaedah; nilai 6 Nov ialah negatif besar (Mxx −14,390 mata; Nxx −17,625 mata) dan bergantung 46% (Mxx) / 86% (Nxx) pada posisi masih terbuka.

### Cited Findings
- Hero: label "Purata setiap belian · Papertrade C", angka `a=avgOf(src.map(r=>r.hasil))`, "SPY tempoh sama", "beza", "USD1,000 setiap belian" — [H:4305–4312]. Ayat: "Angka besar di atas ialah untung purata setiap belian, bukan pulangan portfolio" [H:4311].
- Kad KPI 1–4 dan isinya — [H:4344–4349]; `delta()` sejak sesi lalu daripada `semalam(src)` [H:4328].
- `blokExplainer`: E = Selesai untung / Selesai rugi / Dipegang untung / Dipegang rugi (jumlah mata) + Jumlah; "Purata setiap belian = jumlah ÷ n posisi" — [H:2599–2611].
- Lampu "Data n/8": `renderSal` di kepala (`#salH`) [H:3279–3282] + `salStrip` dalam Ringkasan [H:3318]; 8 saluran dinamakan di [H:3272–3276]. Ia menguji TARIKH, bukan kejayaan larian (audit 2 §"Lampu Data n/8 menguji tarikh") — v147 hanya menukar ambang kepada 39.5/16 jam [H:3262–3271].
- Penanda aras: `spyPos` memakai `prestasi/garis.spy` [H:2879]; perkataan "SPUS" tidak muncul dalam `renderUtama`/`heroUtama` (hanya SPY). CLAUDE.md: "Guna SPUS, bukan SPY, dalam apa-apa perbandingan pulangan selepas ini"; `laporan/BANDING_SPUS.md` wujud sebagai laporan, bukan panel.
- Kiraan audit CSV (lihat Soalan 2 Inferences): Mxx jumlah −14,390 mata (selesai −27,685, dipegang +13,296); Nxx −17,625 (selesai −2,193, dipegang −15,432).
- "Terbaik ikut papertrade" ialah satu-satunya tempat kaedah dinamakan dalam Ringkasan [H:4352–4357]; "Terbaik ikut backtest" menamakan 3 kaedah berpingat backtest [H:4360].

### Inferences
- Tiada kad KPI Ringkasan membezakan Mxx daripada Nxx walaupun sub-tab Posisi/Prestasi memisahkannya sejak 3 Nov 2026; purata gabungan (≈ −2.2% atas 14,720 posisi sah) menyembunyikan bahawa kohort Nxx 3 hari (−5.17%, 86% terbuka) sedang menarik purata ke bawah.
- Soalan pemilik "rugi kecil, untung besar" memerlukan taburan (untung purata lawan rugi purata, ekor) setiap KAEDAH; Ringkasan hanya memberi purata agregat dan kadar menang (yang `REVERSE/KOMBINASI.md` dalam CLAUDE.md labelkan "Kadar menang bukan maklumat").

### Gaps
- Nilai `spyPos` purata dan "beza" pada 6 Nov tidak dikira (perlu `prestasi/garis.spy`, iaitu output `jana_db.py` yang tidak dijalankan dalam audit ini).

---

## Soalan 7 — Watchlist: sumber, pencetus kemasukan, panel/lajur, pertindihan dengan Posisi

### Takeaway
Watchlist membaca `papertrade/watchlist` (daripada `watchlist.csv`, 488 baris pada 6 Nov, `tarikh_data` 2026-11-05, 45 lajur) ditapis 90–100% `pct_dipenuhi`; 297 daripada 488 baris ialah kaedah Nxx; 244 baris ≥ 99%; 0 "isyarat lengkap" (panel itu tidak dirender bila kosong). Ia memaparkan 4 KPI, kad "calon paling hampir ikut sektor", "Gred sekali pandang", penapis dan jadual 10/17 lajur; 9 daripada 17 lajur penuh (Trend, Risiko, 52w, Stage, 5 gred) ialah salinan tepat lajur Posisi — maklumat saham yang sama, bukan maklumat kaedah.

### Cited Findings
- Sumber dan kemasukan: tugasan_v3 §3 "Watchlist (Hampir Signal) = 90–99% dipenuhi (semua syarat kecuali pencetus; pencetus dalam ≤ 2%; pencetus kalendar ≤ 3 hari dagangan). Maks 5 setiap kaedah … Terkeluar signal → BUANG serta-merta. Calon baharu hanya ditambah pada imbasan malam"; §10 "calon tanpa `jarak_pct` tidak dimasukkan"; 47 kaedah K145+ (M115–M161) "tiada `hampir()` → tiada watchlist" (§3). `watchlist.csv` ditulis imbasan malam, tajuk lajur dikekalkan "dipakai oleh dashboard" (`papertrade/SKEMA.md` §watchlist.csv).
- `jana_db.py` dokumen `papertrade/watchlist`: `definisi`, `dibina`, `gred_pada`, `tarikh_data`, `rows=[earn_sebenar(baris_db(r,PETA_WATCH),…)]` — [J:1297–1301]; dibahagi (`PECAH`).
- Kiraan `watchlist.csv` (6 Nov): 488 baris semuanya 90.0–99.9% (`% hampir`), 115 kaedah unik, 215 saham unik, 297 baris kaedah `N*`, 244 ≥ 99%, 0 baris "Tiada (isyarat sah)"; sektor teratas Healthcare 93, Technology 88, Materials 51; 488/488 ada `rs_rating`; `gred_kewangan` ada 488 (SKEMA: butiran kewangan hanya dalam senarai_beli/watchlist, tidak ke db). `senarai_beli.csv` 1,262 baris (tidak ditolak ke db).
- Render `renderWatch` [H:1690–1763] urutan: (1) headline teks tetap [H:1715]; (2) 4 KPI: Calon (n, saham unik, kaedah), ≥ 99% hampir (`n99` + "n paras sudah disentuh"), Sektor terbanyak (3 teratas), Isyarat lengkap ATAU Dibina [H:1716–1721]; (3) panel "Hampir Signal": `rejimHtml` · `panelWatchKad(all)` 5 sektor × (kad + 3 baris, cip RS, sparkline 30 tutup) [H:3047–3066] · `blokGredGrid(rows)` 10 baris teratas × 6 dimensi gred + Gred + Untung [H:2574–2582] · penapis (`lajurSeg`, kaedah, sektor/industri, carian) [H:1725–1727] · `sortTable` lalai `pct_dipenuhi` menurun [H:1728]; (4) panel "Isyarat lengkap dalam watchlist" (hanya jika `lengkap.length`) dengan lajur Saham, Kaedah, Status belian (`wBeli`: Dibeli / Dilangkau / Menunggu belian / Tidak dibeli), Catatan [H:1705–1713].
- Lajur Penuh (17): Saham(+nama) · Kaedah · **Trend** · **Risiko** · **52w** · **Stage** · Harga · % hampir (`wPill`: "Isyarat lengkap"/"Paras disentuh"/n.n%) · Syarat belum cukup (pencetus + dipenuhi + sebab + syarat_belum) · Paras pencetus (+jarak) · Tarikh masuk watchlist · Hari dalam watchlist · Sektor · Industri · RS · QR · Gred — [H:1729–1740]. Ringkas (10) `watchColsR` [H:1682–1689]: Saham · Kaedah · Trend · Risiko · 52w · Stage · % hampir · Harga(+paras) · Gred · Syarat belum cukup.
- `wPill` menulis 100 → "Paras disentuh" dan had 99.9 — [H:1665–1666] (cadangan audit 1 dilaksanakan). `n99` masih mengira baris disentuh (`pct>=99`) tetapi menambah "n paras sudah disentuh" dalam sub [H:1703, 1718].
- Helaian `openWatch` [H:2836–2845]: status belian, 6 medan (% hampir, harga, paras, jarak, tarikh masuk, hari), syarat belum cukup, Trend, Stage, Gred (`gredList` 7 baris termasuk Pemangkin & Kewangan).
- Kad telefon `kadWl` [H:2563–2566]: saham, kaedah · hari, pil % hampir, nama, harga, pencetus/dipenuhi/paras, jarak, syarat belum, gred, nota.

### Inferences
- Watchlist ialah alat **pelaksanaan "esok beli apa"** — tetapi senarai beli sebenar (`senarai_beli.csv`, 1,262 baris) tidak dipaparkan di mana-mana dalam dashboard (tidak ditolak ke db sejak 19 Okt); pemilik hanya melihat "isyarat lengkap dalam watchlist" (0 pada 6 Nov) dan cip "Dibeli pada buka" dalam `panelEsok`, yang bersumber watchlist juga. Jadi **HILANG**: paparan senarai beli esok yang sebenar (dengan `henti`, `buka_maks`, `sasaran`, `belian_ke`) — tugasan_v3 §3 mewajibkan medan itu dalam senarai beli, bukan watchlist.
- 9 lajur Watchlist (Trend, Risiko, 52w, Stage, Sektor, Industri, RS, QR, Gred) ialah lajur yang sama dengan Posisi — **REDUNDAN** antara tab dan **PAPARAN-SAHAJA** (Soalan 4). Lajur khas Watchlist yang berguna: % hampir, Syarat belum cukup, Paras pencetus/jarak, Hari dalam watchlist.
- Dengan 297/488 baris Nxx dan 115 kaedah, Watchlist tanpa tapis kaedah ialah senarai 488 calon untuk 115 kaedah — tiada nilai untuk "kaedah terpilih" sehingga pemilik menapis; `select` kaedah 115 pilihan di telefon ialah dropdown panjang.
- KPI "Sektor terbanyak" tidak membantu kedua-dua soalan (audit 1 cadangan BUANG, kekal).

### Gaps
- `TAMAT_WATCH`/umur maksimum dalam `kod/scanner.py` tidak disemak dalam audit ini; nilai `hari` maksimum dalam `watchlist.csv` tidak dikira.

---

## Soalan 8 — Status pelaksanaan cadangan dua audit terdahulu (v102/v103) pada v154

### Takeaway
Daripada ~30 cadangan khusus untuk tiga tab ini, **5 dilaksanakan** (label TERUSKAN/PERHATI/HENTIKAN bersara; Pemangkin/Kewangan keluar dari jadual; 100 → "Paras disentuh"/99.9; "Papar lagi" kekal skrol; MOD_ACTIONS rasmi), **4 separa** (Esok+Berubah bersebelahan tetapi tidak digabung; "Gred sekali pandang" dibuang dari Posisi sahaja; KPI ≥99% menambah nota disentuh; kad Perhatian = satu takrif status), dan **≥ 20 tidak** — termasuk semua perubahan struktur (4 tab, lampu tunggal, KPI ikut tapisan, Peta ikut saham, lalai Dipegang, EW/SPUS hadapan, buang USD1,000, buang scatter/podium, pindah lajur gred/trend ke helaian). Arah bertentangan juga berlaku: lajur **52W** DITAMBAH ke setiap pandangan (v150) walaupun kedua-dua audit mencadangkan mengurangkan lajur paparan.

### Cited Findings
Audit 1 = `reports/Audit dashboard tab demi tab.md` (§"Keputusan setiap bahagian", baris 182–268); Audit 2 = `reports/Audit dan reka semula dashboard.md` (jadual baris 120–182; D1–D9 baris 206–222). Status disemak terhadap kod v154:

| Cadangan (sumber) | Status v154 | Bukti |
|---|---|---|
| Ringkasan: satu lampu sistem ganti jalur 8 cip + "Kemas kini terakhir" (A1 ¶Ringkasan; A2 Global) | TIDAK | `salStrip` 8 cip [H:3318] + `renderSal` kepala [H:3279] kedua-duanya kekal; v147 hanya ubah ambang |
| Banner fasa bukti ganti "3 perkara utama" (A1) | TIDAK | "3 perkara utama" kekal [H:4342] |
| KPI matang sahaja; buang USD1,000 (A1; A2 D1) | TIDAK | USD1,000 dalam hero [H:4309] dan kad 3 [H:4347] |
| Esok + Berubah digabung satu blok (A1) | SEPARA | kedua-dua wujud bersebelahan `grid2 eq` [H:4350], tidak digabung |
| BUANG "Terbaik ikut papertrade" & scatter "Untung lawan risiko" (A1; A2 D1) | TIDAK | [H:4352–4358] |
| PINDAH podium backtest ke Lagi (A1, A2) | TIDAK | [H:4360] |
| Portfolio 10 slot → "Posisi saya"/Lawan matlamat (A1, A2 D5) | TIDAK | masih `pslotKad` dalam Eksperimen [H:4371], hanya RS_10/RAWAK_10 |
| Label TERUSKAN/PERHATI/HENTIKAN + Skor U×S bersara (A2 D1) | **YA** | komen [H:1939–1941] "29 Okt 2026 … dibuang"; satu sistem label = status Papan |
| EW/SPUS hadapan ganti SPY (A2 §EW) | TIDAK | hero/kad masih SPY; SPUS hanya `laporan/BANDING_SPUS.md` |
| Sasaran 10%/bulan dipapar (A2 D9) | TIDAK | tiada dalam 3 tab |
| Posisi: KPI ikut tapisan; asing direalisasi/belum (A1 ¶Posisi 22) | TIDAK | `ptKpis(all,…)` [H:1921] |
| Ringkasan kaedah ditapis (n, matang, lorong, SPY, henti, dilangkau) (A1 22) | TIDAK | tiada fungsi sedemikian |
| Lalai "Dipegang", susun ikut risiko (A1 24; A2) | TIDAK | `S.pos.st='semua'` [H:1131]; lalai `untung_pct` menurun [H:1927] |
| Satu takrif "hampir keluar" dalam unit ATR (A1 24) | SEPARA | `statusPos` guna 2 takrif (25% julat L2; henti < 2%) [H:2897–2899]; `l2Cip` ATR hanya helaian [H:4287] |
| Gred/Trend/Pemangkin/Kewangan ke helaian (A1 24; A2 D7) | SEPARA/TERBALIK | Pemangkin+Kewangan keluar v122; Gred 5 lajur kekal; Trend/Risiko/Stage kekal dalam semua pandangan; **52W ditambah v150** [H:4167] |
| Peta mengira saham + pegangan lorong 2 (A1 24) | TIDAK | `panelPeta` "saiz = bilangan [posisi]" [H:3796]; `peg=!r.keluar` lorong 1 |
| "Isyarat tidak dibeli" ke Sistem + langkauan 9:35 (A1 14; A2) | TIDAK | kekal dalam Posisi [H:1929]; hanya baris `tidak_dibeli` (101) |
| Bendera kualiti data (bar sintetik, beli ≠ buka) (A1 24) | TIDAK dikesan | tiada lajur sedemikian dalam `posColsP`/`ptCols` |
| Buang akaun Gabung; arkib Moomoo (A2 D6) | TIDAK | `AKAUN` termasuk `gab`, `m` [H:1116] |
| "Gred sekali pandang" (A2 D7 arah) | SEPARA | dibuang daripada Posisi v152 [H:1924], kekal Watchlist [H:1724] |
| Watchlist: 100 → 99.9 / "disentuh" (A1 25) | **YA** | `wPill` [H:1665–1666] |
| KPI ≥99% dipisah daripada disentuh (A1) | SEPARA | `n99` masih termasuk; sub tambah "n paras sudah disentuh" [H:1718] |
| Buang KPI "Sektor terbanyak" (A1) | TIDAK | [H:1719] |
| Lajur status/kedudukan Analisis dalam Watchlist (A1 25) | TIDAK | tiada dalam `watchColsR`/penuh |
| Tanda "tiada watchlist" bagi K145+ (A1) | TIDAK | tiada |
| Isyarat lengkap → "Beli pada buka" Hari Ini (A1, A2) | SEPARA | `panelEsok` blok "Dibeli pada buka" [H:3298] membaca `wLengkap`; panel Watchlist kekal |
| Watchlist pindah ke Hari Ini (A2) | TIDAK | tab kekal [H:1064] |
| 4 tab, tiada tab sisi, sentiasa buka Hari Ini (A2 D7, Global) | TIDAK | 9 tab [H:1060–1068]; v142 rel kiri; `pbs3_tab` dipulihkan [H:1132] |
| MOD_ACTIONS → rasmi (A2 D8) | **YA** | CLAUDE.md "GitHub Actions RASMI sejak 27 Okt 2026" |
| "Papar lagi" tidak melompat (bukan cadangan audit; permintaan pengguna) | YA v153 | [H:1866] |

- Pencetus perubahan sebenar v103–v154 (sumber `dashboard.md` fragmen "versi 1xx", komen kod): v104 lajur Stage; v105–v131 (28–29 Okt) ~27 versi penjajaran/padat/lajur Posisi atas permintaan pengguna; v132 Kombinasi N; v135 paksi %; v138 hero; v139 Perbandingan setara/snow/kepekatan; v142 rel kiri; v144–v148 pembaikan langganan db; v150 52W; v151 senarai bahagian; v152 buang Gred sekali pandang; v153 skrol; v154 Lift (tab Analisis).

### Inferences
- Perubahan v103–v154 pada tiga tab ini hampir semuanya **kosmetik atau tambahan lajur** (28 Okt: 27 versi dalam sehari menjajarkan sel gred) — tiada satu pun cadangan struktur kedua-dua audit yang menyentuh "kaedah mana" dilaksanakan dalam tab operasi; jawapan "kaedah mana" (Lift v154) diletakkan dalam tab Analisis, bukan Ringkasan.
- `dashboard.md` menyatakan "Versi semasa = versi 132 (artifact versi 164; 2 Nov 2026)" sementara manifes `data/dashboard_terbit.json` ialah `nombor` 185 / v154 — dokumen peraturan tertinggal 22 versi, jadi ia tidak boleh dipakai untuk menyemak "apa yang WAJIB dipaparkan" bagi v133–v154.

### Gaps
- Status "bendera kualiti data" dan "`gred_pada` diisi tarikh data" tidak disahkan sepenuhnya (perlu baca `gred.py`); dilabel "TIDAK dikesan".

---

## Soalan 9 — Apa yang `dashboard.md` dan `tugasan_v3.md` WAJIBKAN tab ini paparkan

### Takeaway
`tugasan_v3.md` tidak menetapkan panel; ia menetapkan **data** (dua lorong keluar direkod berasingan, baris tidak sah/tidak dibeli tidak dikira, gred direkod bukan penapis, label kaedah ≥ 20 dagangan tertutup, USD1,000 sama berat untuk metrik portfolio, Watchlist 90–99% maks 5 setiap kaedah). `dashboard.md` menetapkan susunan lajur Posisi (`ptCols` 14 nama), peraturan baris merah, tooltip, had baris telefon, dan jadual kandungan setiap tab — tetapi ia pada versi 132 dan jadual kandungannya tidak lagi memadankan kod (contoh: tiada sebutan Trend/Risiko/52w/Stage/Peta/Perhatian/Peluang/Esok/Berubah dalam baris Ringkasan/Posisi/Watchlist).

### Cited Findings
- `dashboard.md` jadual Struktur tab: Ringkasan = "3 perkara utama, KPI selesai/dipegang/keseluruhan/aktiviti, Terbaik ikut papertrade (label + sebab + Terlalu awal), untung lawan risiko, Terbaik ikut backtest (podium), Eksperimen (dua lorong, gred, portfolio 10 slot RS_10 lawan RAWAK_10)"; Posisi = "Semua/Dipegang/Sudah keluar, lajur ringkas atau penuh, tapis kaedah/sektor/industri/carian; helaian saham; Isyarat tidak dibeli (dilipat)"; Watchlist = "Hampir Signal (90–100%; Paras disentuh; 99.9) … Isyarat lengkap dalam watchlist (dilipat) dengan status belian" — [dashboard.md:§Struktur tab](../../BacktestShariah2/standard/dashboard.md).
- `dashboard.md` Peraturan paparan: "Lajur M, C dan jadual dagangan Prestasi sama dan sama susunan (`ptCols()`): Tarikh beli, Saham, Kaedah, Sektor, Industri, Harga beli, Unit, Harga terkini, Untung %, Hari dipegang, Isyarat keluar, Tarikh keluar, Harga keluar, Untung akhir %" — kod `ptCols` sebenar [H:1837–1851] berbeza (Trend/52w/Stage/R/Sejak beli/Hari PSN/Pegang selagi naik/5 gred; Sektor & Industri hanya sebagai gred). "`keluar=true` → baris merah" (kod: merah hanya bila `tutup_semua` [H:1836 `rclsPT`]). "Telefon ≤ 760px: jadual bermula 10 baris, Papar lagi +25; desktop 25 dan +100" — sepadan kod. "Kadar menang sentiasa dinamakan asasnya" — sepadan. "Versi semasa = versi 132" — tidak sepadan manifes 185.
- `tugasan_v3.md` §3 Watchlist (90–99%, maks 5, buang serta-merta); §5.3a dua lorong direkod berasingan; §5.4 baris `tidak_dibeli`/`tidak_sah` tidak dikira dalam prestasi; §7 "Papertrade M, C, Combine; KPI, untung purata setiap kaedah, kadar menang, penurunan maksimum, Paling Teruk, skor Untung×Selamat" dan label ≥ 20 dagangan tertutup ("BELUM CUKUP DATA"), "USD1,000 sama berat"; §8 "Gred tidak menapis belian sehingga pengguna memutuskan berdasarkan data papertrade"; §11 Papan Penganalisis "rekod analisis sahaja, tidak menapis belian".
- `dashboard.md` "Semakan render: `jana_db.py --keluar /tmp/db` kemudian `node ujian/semak_dashboard.js /tmp/db [lebar…]` … mengaudit jadual Posisi (Penuh, Ringkas, Risiko, Gred)".

### Inferences
- Tiada dokumen peraturan yang MEWAJIBKAN Trend, Stage, 52W, Rejim, Peta, Peluang, Perhatian, Kepekatan — semuanya ditambah atas permintaan pengguna ad hoc (komen kod "permintaan pengguna") tanpa dimasukkan ke `dashboard.md`. Oleh itu membuangnya tidak melanggar mana-mana peraturan bertulis; yang wajib dikekalkan ialah data dua lorong, pengecualian tidak sah/tidak dibeli, Watchlist 90–99% dan label ≥ 20.
- `tugasan_v3 §7` masih menyebut "skor Untung×Selamat" dan label TERUSKAN/PERHATI/HENTIKAN yang kod sudah buang (29 Okt 2026) — peraturan dan kod bercanggah; audit 2 D1 mencadangkan "§7 ditulis semula" dan itu belum dibuat.

### Gaps
- `standard/binaan_v2_log.md` tidak mengandungi entri "versi 1xx" bagi ketiga-tiga tab (grep kosong); sejarah hanya ada dalam `dashboard.md` baris 3 (hingga v132) dan komen kod.

---

## Soalan 10 — Penilaian keseluruhan setiap panel terhadap matlamat pemilik + perkara HILANG

### Takeaway
Dalam 3 tab operasi: **ESENSIAL untuk pelaksanaan harian** = Esok, Berubah, Perhatian, jadual Posisi (lajur Keluar kaedah / Lorong 2 / Hari / Untung / Kaedah / Tarikh), Isyarat tidak dibeli, Watchlist (% hampir, syarat, paras), jalur status data; **ESENSIAL untuk pilih kaedah** = TIADA panel yang mencukupi (Terbaik ikut papertrade ialah purata mentah yang repo sendiri labelkan tidak boleh dipakai); **REDUNDAN** = hero↔KPI↔3 perkara, salStrip↔Data n/8, scatter, podium, KPI Posisi↔KPI Ringkasan, Perhatian↔Esok, 9 lajur saham Watchlist↔Posisi; **PAPARAN-SAHAJA** = Trend, 52w, Stage, Sektor, Gred keseluruhan, Rejim, cip RS, Peluang ikut sektor, Peta/Kepekatan (mengira posisi); **MATI/TAK DIPAKAI** = tiada laluan mati dikesan dalam 3 tab ini (semua panel bersyarat data; "Isyarat lengkap" dan "Gred sekali pandang" hanya tidak dirender bila data < had).

### Cited Findings
- Senarai panel dan sumber: Soalan 2, 3, 7 di atas (dengan baris kod).
- Panel bersyarat (dirender hanya bila data ada, bukan mati): `panelPeluang` (`buka.length`) [H:2955]; `panelPerhatian` (`L.length`) [H:3019]; `lengkapH` (`lengkap.length`) [H:1705]; `blokGredGrid` (`L.length<3`) [H:2576]; `blokKepekatan` (`peg.length<20`) [H:2586]; `adilH`; `kpiSpark` (`H[k].length<3`) [H:4303]; `jlPos` (`posisi/jalur` ada) [H:4007].
- `prestasi/ringkasan` ditulis `jana_db.py` [J:1313] tetapi **tidak dilanggan** oleh halaman (tiada `sub('prestasi/ringkasan'` dalam `connect`, [H:5320–5348]) — dokumen db yang ditulis setiap hari tanpa pembaca (MATI di sisi data, bukan di tab).
- `papertrade/senarai_beli`: tidak ditolak dan tidak dibaca [J:1293–1294] — tetapi `dashboard.md` §6 tugasan_v3 masih menyenaraikannya sebagai dokumen dashboard.
- CLAUDE.md (KAEDAH_TERBAIK 29 Okt 2026): "jangan pilih kaedah ikut pangkat papan"; "25 terbukti NEGATIF, 0 terbukti positif"; "membezakan dua kaedah yang berbeza 1 mata perlu ~77 posisi ditutup setiap kaedah (sekarang median 10)"; "Betulkan kecacatan henti hari-0 dahulu kerana ia mencemari setiap pangkat". Nota manifes v154: "17 kaedah positif lawan sifar, 0 selepas hari beli dipadankan" (`data/dashboard_terbit.json.nota`).
- `REVERSE/KOLAM_EKOR.md` §4 (CLAUDE.md): 421 daripada 1,770 posisi C ditutup dibeli dan dihentikan pada HARI MASUK dengan kadar menang 0.00% — kecacatan mekanikal yang mencemari purata setiap kaedah; tiada lajur/penanda dalam Posisi menandakan keluar hari-0.

### Inferences — HILANG (apa yang pemilik perlukan tetapi tiada dalam 3 tab)
1. **Satu paparan "kaedah terpilih"**: tiada mod/tapisan global "kaedah saya" yang mengikat Esok, Posisi (KPI + Peta + jadual), Watchlist dan senarai beli kepada SATU ID; tapisan kaedah wujud secara berasingan dalam Posisi dan Watchlist sahaja dan tidak mengubah KPI.
2. **Senarai beli esok yang sebenar** (`senarai_beli.csv`, 1,262 baris, dengan `henti`, `buka_maks`, `sasaran`, `belian_ke`) — tidak ditolak ke db dan tidak dipaparkan; pemilik yang mahu melaksanakan belian kaedah terpilih dengan wang sebenar tidak nampak paras henti/buka_maks sebelum buka pasaran.
3. **Pecahan untung/rugi setiap kaedah dalam wang** (jumlah mata/USD, untung purata lawan rugi purata, ekor 5% teratas) — hanya purata dan kadar menang; "rugi kecil, untung besar" memerlukan nisbah untung purata ÷ rugi purata dan `tanpa5` setiap kaedah (ukuran yang REVERSE pakai) — tiada dalam 3 tab.
4. **Penanda aras SPUS** (bukan SPY) dan **jurang ke matlamat 10%/bulan** — tiada.
5. **Pemisahan Mxx/Nxx dalam Ringkasan** — Posisi/Prestasi memisah, Ringkasan menggabung.
6. **Penanda keluar hari-0 / kecacatan henti** pada baris Posisi dan agregat ikut kaedah (kadar kena henti hari masuk) — tiada, walaupun CLAUDE.md menyatakan ia "mencemari setiap pangkat".
7. **Langkauan belian 9:35 yang tidak direkod sebagai baris** (audit 1: ~159 langkauan lawan 64 baris) — `status_harian.json.beli.langkau` dibaca `jana_db.py` ke `papertrade/claude.batal` [J:1283–1288] tetapi tiada panel memaparkannya dalam Posisi/Ringkasan (tidak disahkan; grep `batal` dalam render tidak dibuat).
8. **Lift (v154)** — ukuran "kaedah mana" yang paling jujur dalam repo berada di tab Analisis, bukan di Ringkasan; Ringkasan masih memaparkan tiga "terbaik" yang bercanggah (papertrade mentah, backtest podium, status Papan).

### Gaps
- Tidak dapat mengesahkan sama ada `papertrade/claude.batal` dipaparkan di mana-mana (tidak di-grep dalam masa audit).
- Prestasi ikut gred dan dua lorong pada data 6 Nov tidak dikira semula (bergantung kiraan halaman).

---

## Ringkasan berangka untuk penulis laporan

| Perkara | Nilai | Sumber |
|---|---|---|
| Tab | 9; operasi 3 (`utama`, `posisi`, `watch`) | H:1060–1068 |
| Panel Ringkasan (urutan) | 12 blok: hero · salStrip (8 cip) · Peluang ikut sektor · 3 perkara utama (+explainer 4 bar) · 4 KPI · Esok (4 blok) · Berubah (5 baris) · Terbaik ikut papertrade · Untung lawan risiko · Terbaik ikut backtest · Eksperimen (3) · Cara baca + kaki | H:4336–4373 |
| Panel Posisi | headline · 4 KPI · Peta (komposisi, kepekatan, treemap) · Posisi & keputusan (rejim, Perhatian ≤ 4 kad, segmen 3, pandangan 4, tapis 4, jadual) · Isyarat tidak dibeli | H:1907–1935 |
| Lajur Posisi | Ringkas 11 · Penuh 21 · Risiko 13 · Gred 12; PAPARAN-SAHAJA dalam Ringkas: 4 (+Gred) | H:1897, 1837, 3815 |
| Panel Watchlist | headline · 4 KPI · Hampir Signal (rejim, kad sektor 5, Gred sekali pandang 10, tapis 4, jadual) · Isyarat lengkap (0 pada 6 Nov) | H:1690–1763 |
| Lajur Watchlist | Ringkas 10 · Penuh 17; 9 lajur sama dengan Posisi | H:1682, 1729 |
| Baris Posisi lalai `cm` | Semua 11,441 · Dipegang 5,571 · Keluar 5,870 · tidak sah 133 · lorong 2 buka 9,498 · saham unik dipegang 654 | kiraan `claude*.csv` |
| Baris Posisi `cn` | 3,419 · 2,936 · 483 · 7 · 3,409 · 407 | kiraan |
| Untung/rugi (sah) | Mxx −1.27%/posisi, −14,390 mata (−USD143,898); Nxx −5.17%, −17,625 mata (−USD176,250) | kiraan |
| Watchlist | 488 baris, 115 kaedah, 215 saham, 297 Nxx, 244 ≥ 99%, 0 lengkap, `tarikh_data` 2026-11-05 | kiraan `watchlist.csv` |
| Telefon | ≤ 760px kad; 10 baris + 25; "Papar semua" hanya ≤ 400; tiada skrol mendatar (v113); KPI 2 lajur ≤ 520px; Risiko/Gred tiada di telefon | H:473–491, 1862, 3810 |
| Cadangan audit terdahulu dilaksanakan | 5 YA · 4 SEPARA · ≥ 20 TIDAK; 1 arah terbalik (52W ditambah) | Soalan 8 |
| Dokumen peraturan | `dashboard.md` pada v132 lawan terbitan v154 (nombor 185) | dashboard.md; data/dashboard_terbit.json |
