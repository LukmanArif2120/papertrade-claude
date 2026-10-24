# Ketepatan data dan kiraan papan pratonton v104 (kiraan semula bebas)

> **Kaedah dan bukti.** Audit ini baca sahaja, dibuat pada 24 Okt 2026 dengan data tutup Jumaat 23 Okt 2026. Halaman `terbit_v104_uji.html` dijalankan dalam Chromium (Playwright) melalui salinan yang ditambah satu baris `window.__ev` untuk membaca keadaan dalaman: [salinan.html](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/salinan.html). Teks halaman dan baris yang dinyahkod disimpan dalam [halaman.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/halaman.json).
>
> Setiap angka dikira semula dalam Python (pandas, scipy) terus daripada CSV `papertrade/claude*.csv`, stor harga, `terkini.csv`, `watchlist.csv`, `senarai_beli.csv` dan CSV `portfolio_slot`, semuanya di cawangan `pratonton-audit`. Skrip: [kira.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/kira.py), [esok.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/esok.py), [masa.js](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/masa.js) (simulasi jam bagi lampu) dan [ambil.js](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/ambil.js).
>
> Rujukan baris:
> - `H:n` ialah [dashboard_v2.html di worktree](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), yang sudah mengandungi blok v104.
> - `B:n` ialah [blok_audit.js](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/laman/blok_audit.js).
>
> WebFetch gagal (DNS disekat), jadi sumber luar dipetik daripada ringkasan hasil carian.

## 1. Adakah kiraan dan purata yang dipaparkan sepadan dengan kiraan semula bebas?

### Takeaway
Ya. Setiap nombor KPI yang diminta dapat dihasilkan semula dengan tepat. Db dan CSV juga sama medan demi medan: 5,711 baris, 0 beza pada 12 medan. Masalahnya bukan aritmetik, tetapi **takrif, populasi dan kesesuaian statistik** (bahagian 2–4). Dua kaunter hulu dalam `harian/status` (761 direkod dan 186 keluar baharu) berbeza daripada nombor halaman. Bezanya dapat diterangkan, dan nombor halaman ialah yang betul.

### Cited Findings

**Integriti db lawan CSV**
- `ringkas_c` yang dinyahkod halaman mengandungi 5,711 baris dengan susunan yang sama dengan `claude.csv`, `claude_2.csv` hingga `claude_72.csv`. Medan berikut memberi 0 beza: harga_beli, harga_terkini, untung_pct, untung_akhir_pct, untung_henti_pct, henti, keluar, keluar_henti, tidak_sah, tutup_semua, status_henti dan isyarat_keluar — [kira.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/kira.py), [papertrade/](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/papertrade/)

**Hari Ini › Aktiviti terkini** ("760 dibeli · 175 keluar · 9 dilangkau")
- **760 dibeli**: CSV mempunyai tepat 760 baris sah dengan `tarikh_beli` 2026-10-23 (`tidak_sah` 0). `harian/status.beli_ringkas.direkod` pula 761. Baris ke-761 ialah PEGA M153, yang kemudian ditanda `tidak_dibeli` ("sedia() sig=False pada 2026-10-22, disemak dengan bar hingga 2026-10-23") — [kpiAktiviti H:3513](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [claude*.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/papertrade/)
- **175 keluar**: 175 keluar lorong kaedah pada 23 Okt bagi posisi sah. Jika baris tidak sah dikira, jumlahnya 176 (LNTH M03 ditutup sebagai `tidak_sah`). Kaunter hulu `kemaskini_pagi_ringkas.C_keluar_baru` = 186 sama dengan bilangan baris yang `dikesan` = "2026-10-24 06:02 MYT". Bilangan ini termasuk 176 keluar lorong 1, 8 penutupan ACA bertarikh 22 Okt, dan 2 baris lain. Jadi 186 menggunakan takrif "dikesan pagi ini", bukan "keluar pada sesi 23 Okt" — [db harian/status](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/harian/status.json), [kira.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/kira.py)
- **9 dilangkau**: 9 baris `papertrade/langkau` bertarikh 23 Okt. Ini sama dengan `beli_ringkas.dilangkau` = 9 dan `liputan["2026-10-23"].bil_log` = 9. Senarai beli 770 = 761 + 9 — [db papertrade/langkau](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/papertrade/langkau.json)

**Hari Ini › Posisi C matang** ("+0.02%, 95% −18.76 … +18.80, 2 hari beli; menang 46% (28–65%); 24 matang; 8% masih terbuka; 5,492 belum matang")
- Kiraan semula memberi n = 24 dan purata 0.0171%. SE berkelompok 1.4780 dengan G = 2, dan t(1) = 12.706, jadi selang 95% ialah −18.76 hingga +18.80. Menang 11/24 dengan Wilson 27.9%–64.9%. Masih terbuka 2/24 (8.3%), dan 5,516 − 24 = 5,492 belum matang. Semua sepadan dengan paparan — [matangC B:95](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/laman/blok_audit.js), [kira.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/kira.py)
- Komposisi 24 posisi itu:
  - M20: 5 dibeli 8 Okt + 5 dibeli 9 Okt.
  - M73: 5 dibeli 8 Okt + 4 dibeli 9 Okt.
  - M27: 5 dibeli 8 Okt.
  - Purata hari beli: 8 Okt −1.17% (n = 15), 9 Okt +1.99% (n = 9). Ada 23 saham unik, kerana PTEN muncul dua kali.
  - Sumber: [kira.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/kira.py)

**Hari Ini › Bukti hadapan** ("10 / 9,810")
- 9,810 = `lejar_posisi` 8,528 + `c_pra_lejar` 1,620 − `lejar_tindih` 338, iaitu Σ`h_posisi` merentas 134 kaedah. 10 = Σ`h_matang`, iaitu M20 5 + M73 5 (dibeli 8 Okt, data Lejar 22 Okt) — [db analisis/papan](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/analisis/papan.json)

**Hari Ini › Portfolio gabungan beku** ("−0.72% · rawak kaedah +0.19% · SPY −0.31% · 1 sesi hingga 22 Okt")
- `GABUNGAN_10_ekuiti.csv` 22 Okt: ekuiti 0.992759 (−0.72%), dan spy 0.996855 (−0.31%). `RAWAK_KAEDAH_10_ekuiti.csv`: 1.001878 (+0.19%) — [GABUNGAN_10_ekuiti.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/portfolio_slot/GABUNGAN_10_ekuiti.csv), [RAWAK_KAEDAH_10_ekuiti.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/portfolio_slot/RAWAK_KAEDAH_10_ekuiti.csv)
- SPY −0.31% ialah buka 22 Okt 766.37 → tutup 763.96, selaras dengan belian pada buka. `portfolio_slot.py` membahagi dengan harga buka hari pertama — [portfolio_slot.py:240–244](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/portfolio_slot.py), [harga_idx.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/data/harga/stor/harga_idx.csv)

**Hari Ini › Esok** ("Dijual 63 · Dibeli 92 · Hampir ≤ 1 ATR 240 · Earnings ≤ 10 hari 507")
- **Dijual 63**: 51 lorong kaedah "menunggu" + 12 lorong 2 "menunggu" (47 saham, termasuk 1 baris tidak sah). `harian/status.menunggu_buka` = 55, dan angka ini tidak dapat dihasilkan semula daripada CSV, yang hanya mempunyai 51 `isyarat_keluar` "menunggu" — [panelEsok H:2240](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [esok.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/esok.py)
- **Dibeli 92**: 92/173 baris watchlist dengan "tiada (isyarat sah)" dan `wBeli` = "tunggu". Daripada 92 itu, 0 sudah dibeli 23 Okt bagi saham+kaedah yang sama. Watchlist pratonton dibina 24 Okt 06:20 MYT atas data 23 Okt, jadi isyaratnya bukan isyarat semalam — [watchlist.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/papertrade/watchlist.csv), [esok.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/esok.py)
- **Hampir 240 (144 saham)**: dikira semula dengan ATR14 bebas, iaitu purata mudah julat sebenar 14 bar daripada stor + `terkini.csv`.
  - ATR% sama bagi 744/744 saham (beza ≤ 0.05), dan status setiap baris memberi 0 beza.
  - Jarak memberi 0 beza > 0.01 ATR.
  - Tiada jarak negatif (harga sudah di bawah paras).
  - Sumber: [jarakAtr H:3675](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [esok.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/esok.py)
- **Earnings 507**: 507 **saham** unik (3,804 posisi) dengan `earn_kini_h` ≤ 10, daripada 726 saham yang masih aktif. `earn_kini_h` sama dengan `hariKeEarn` halaman bagi 688/688 saham — [hariKeEarn H:3687](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [jana_db.py:92–110](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/jana_db.py)

**Posisi** ("Dipegang 4,150 · Belum direalisasi +3.28% · Dua lorong +3.28% / +3.28%")
- Dipegang = sah dan lorong kaedah belum keluar = 4,150. Purata untung_pct 3.2850%, dengan 73.8% > 0.
- Dua lorong (segmen Dipegang): kaedah 3.2850, selagi naik 3.2793, beza −0.0056. Halaman memaparkan "+3.28% · +3.28%, beza −0.01%".
- Sumber: [ptKpis2 H:3724](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [kiraan](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/halaman.json)
- Panel Hari Ini "selagi naik − kaedah +0.08% ± 0.13 SE (5,516 posisi, 12 hari beli)": kiraan semula memberi purata 0.0813, SE 0.1295, G = 12, dan selang −0.204 hingga +0.366 — [bezaLorong H:3498](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html)

**Monte Carlo Penganalisis**
- Σ`p_top5` bagi 75 kaedah swing = 4.998 dan Σ`p_top1` = 1.002. Ini konsisten dengan 5 tempat dan 1 juara (cabutan 20,000) — [db analisis/papan](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/analisis/papan.json)

### Inferences
- Lapisan paparan v104 boleh dipercayai dari segi aritmetik. Setiap ralat yang tinggal ialah soal takrif, populasi, kelewatan data atau ketidaksesuaian statistik.
- Kaunter `harian/status` (761, 186, 55) menggunakan takrif rutin yang berbeza. Ia tidak patut dipaparkan bersebelahan nombor halaman tanpa label.

### Gaps
- Kaunter `menunggu_buka` = 55 tidak dapat dihasilkan semula daripada CSV, yang hanya mempunyai 51 baris "menunggu" lorong kaedah dan 12 lorong 2. Kaunter ini mungkin termasuk akaun Moomoo atau dikira sebelum langkah lain dalam rutin 6:02. Kod rutin tidak disemak.

## 2. Adakah takrif konsisten merentas panel? Adakah pengiraan berganda yang mengelirukan?

### Takeaway
Tidak konsisten. "Dipegang", "hampir keluar", "matang" dan unit kiraan Esok bermaksud perkara berbeza dalam panel yang berbeza. Panel Esok turut mengira posisi `tidak_sah`. Purata posisi pula didominasi isyarat yang dikongsi banyak kaedah: purata +3.28% ikut posisi menjadi **+0.96% ikut saham**.

### Cited Findings

**Takrif "dipegang"**
- 4,150 dalam Posisi ialah posisi sah yang lorong kaedahnya masih terbuka. Ada lagi **1,268 posisi** sah yang masih dipegang dalam lorong 2 selepas lorong kaedah keluar, dan 6 posisi yang lorong 2nya sudah keluar ketika lorong 1 masih terbuka. Jumlah posisi sah yang aktif dalam mana-mana lorong ialah 5,418 (719 saham) — [ptKpis2 H:3724](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [kiraan](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/kira.py)
- Bilangan `tidak_sah` dalam `posRows('c')` kini 131, berbanding 122 dalam audit v103. Sembilan baris ini sepadan dengan 8 posisi ACA (kini `tidak_sah` dan `tutup_semua` pada 22 Okt @149.15) dan LNTH M03 (ditutup 23 Okt @99.80) — [claude*.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/papertrade/), [Audit dashboard tab demi tab.md](/home/user/papertrade-claude/reports/Audit%20dashboard%20tab%20demi%20tab.md)

**Populasi panel Esok lawan Posisi**
- `panelEsok` memakai `posRows('c').filter(r=>!r.tidak_dibeli)`, yang **tidak** menapis `tidak_sah`. `statusPos` dan `jarakAtr` juga tidak menyemak `tidak_sah` — [H:2240](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [H:3675–3685](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html)
- Kesannya kepada setiap panel:
  - "Dijual" termasuk SENEB M11, yang tidak cair (median nilai $10,352).
  - "Hampir" termasuk FEDU M31, juga tidak cair.
  - "Earnings" termasuk 20 posisi tidak sah, dan 3 saham muncul hanya kerana posisi tidak sah.
  - Sumber: [esok.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/esok.py)
- "Hampir paras keluar (≤ 1 ATR)" memberi tiga nilai bergantung pada panel, walaupun TIPS `jarak_atr` menyebut "satu takrif":
  - Hari Ini: 240 (144 saham), iaitu 166 lorong kaedah + 73 lorong 2 sahaja + 1 tidak sah.
  - Posisi › Dipegang: 166 titik oren.
  - Posisi › Semua: 239.
  - Sumber: [B:484](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/laman/blok_audit.js), [esok.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/esok.py)
- Unit dalam satu panel bercampur:
  - "Dijual 63" dan "Hampir 240" ialah **posisi**, dengan sublabel "47 saham" dan "144 saham".
  - "Earnings 507" ialah **saham** (`new Map(...[r.saham,r])`), sedangkan bilangan posisi ialah 3,804.
  - "Dibeli 92" ialah baris watchlist, iaitu saham+kaedah.
  - Sumber: [panelEsok H:2240–2255](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html)

**Panel "Dibeli pada buka 92" bukan senarai beli sebenar**
- Watchlist hanya meliputi 57 daripada 122 kaedah C. Belian sebenar setiap hari: 571 (19 Okt), 484 (20 Okt), 697 (21 Okt), 647 (22 Okt) dan 760 (23 Okt). Pada 23 Okt hanya 402 daripada 760 belian datang daripada kaedah yang ada watchlist — [watchlist.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/papertrade/watchlist.csv), [claude*.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/papertrade/)
- Senarai beli sebenar (`senarai_beli.csv`, 770 baris bagi 23 Okt) dijana oleh imbasan 7:47 malam MYT pada hari belian (`tarikh_imbasan` 2026-10-23, `tarikh_isyarat` 2026-10-22) — [senarai_beli.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/papertrade/senarai_beli.csv)

**Takrif "matang": KPI 24 lawan Lejar 10**
- Kedua-dua angka memakai takrif umur yang sama: kalendar ≥ `h_umur` = maks(14, ⌈1.5 × hari pegang backtest × 7/5⌉). Bezanya ialah tarikh data dan populasi:
  - KPI C dikira pada data 23 Okt.
  - Penganalisis dikira pada 22 Okt.
  - Pada 22 Okt hanya M20 dan M73 (dibeli 8 Okt) yang matang, iaitu 10 posisi, dan kiraan semula C pada 22 Okt juga memberi 10.
  - 14 tambahan pada 23 Okt ialah belian 9 Okt M20/M73 dan M27 8 Okt (`h_umur` 15).
  - Sumber: [penganalisis.py:128–131](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/penganalisis.py), [umurMatang H:3486](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [kira.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/kira.py)

**Pengiraan berganda (satu saham dibeli banyak kaedah)**
- 4,150 posisi dipegang hanya dalam **603 saham** dan 1,953 pasangan saham+hari beli. Saham dengan posisi terbanyak: BIIB 34, NOW 32, EXLS 32, CTSH 32 dan ANF 31 — [kiraan](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/kira.py)
- Purata belum direalisasi berubah mengikut unit: **+3.28%** ikut posisi, **+3.05%** ikut saham+hari beli, dan **+0.96%** ikut saham (setiap saham sekali) — [kiraan](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/kira.py)
- KPI "Posisi C matang" terdiri daripada 3 kaedah sahaja (M20, M73, M27), iaitu kaedah dengan `h_umur` ≤ 15 hari. Ia bukan sampel wakil Papertrade C — [kira.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/kira.py)

**Rujukan kedudukan dalam teks**
- Banner fasa menulis "M20 #56", dan nota gabungan menulis "#35/#41/#52 dalam ranking ini (M70/M03/M18)". Kedua-duanya memakai `kedudukan` Penganalisis (susunan `skor_bulan`). Jadual Kaedah pula disusun ikut `lb_bulan`, dan dalam jadual itu M20 berada di baris 67, manakala M70/M03/M18 di baris 65/66/63 daripada 75. "Status sebenar 5 teratas semasa: 21 Dis 2026 – 18 Okt 2027" merujuk 5 teratas ikut `kedudukan` (M21, M140, M144, M32, M84), bukan 5 baris teratas jadual — [bannerFasa H:3479](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [rankRows H:3532](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [db analisis/papan](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/analisis/papan.json)

**Portfolio 10 slot**
- Jadual slot memaparkan satu baris SPY sahaja, "−1.20% sejak 16 Okt" (buka 16 Okt 773.24 → tutup 22 Okt 763.96). Baris ini hanya sah bagi RS_10 dan RAWAK_10. Tiga portfolio beku bermula 22 Okt, dan SPY bagi tempoh itu ialah −0.31% — [jadualSlot H:3545](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [harga_idx.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/data/harga/stor/harga_idx.csv)

### Inferences
- **Pembaikan: penapis.** Tambah `&&!r.tidak_sah` pada `pos` dalam `panelEsok` (H:2240), supaya Esok sama populasi dengan KPI Posisi.
- **Pembaikan: label panel Esok.**
  - Setiap blok dilabel "n posisi · m saham".
  - "Hampir" dipecah kepada "lorong kaedah 166 · lorong 2 sahaja 73".
- **Pembaikan: blok "Dibeli pada buka".** Namakan semula sebagai "Isyarat lengkap dalam watchlist (57 kaedah)". Tambah nota: "senarai beli penuh dijana 7:47 malam MYT; purata 5 hari lalu ≈ 630 belian". Tanpa nota ini, peniaga swing akan menjangka kira-kira 92 belian Isnin, sedangkan sejarah menunjukkan 480–760.
- **Pembaikan: purata ikut saham.** Paparkan purata "ikut saham" atau "ikut saham+hari" di sebelah purata posisi dalam KPI Posisi. Purata posisi kini memberi berat 34× kepada BIIB.
- **Pembaikan: rujukan kedudukan.** Sama ada semua rujukan "#n" memakai susunan jadual yang dipapar, atau label ditukar kepada "kedudukan skor #56 (baris jadual 67)".
- **Pembaikan: baris SPY.** Jadual slot memerlukan SPY bagi setiap baris, ikut tarikh `mula` portfolio itu.

### Gaps
- Audit ini tidak mengesahkan sama ada `petaSaham` (pandangan Risiko) mengira 719 saham. Kiraan bebas memberi 719 saham sah yang aktif (tidak `tutup_semua`), tetapi teks panel Risiko tidak dirakam.

## 3. Adakah formula statistik dilaksanakan dengan betul, dan sesuaikah ia apabila G = 2?

### Takeaway
Formula yang dilaksanakan betul dari segi matematik: SE berkelompok CR1 untuk purata, t(G−1), dan Wilson. Tetapi formula ini **tidak bermakna apabila G = 2**. Selang ±18.8 mata (Hari Ini) dan −81.9 … +65.1 (Posisi › Dipegang) ialah hingar yang dipaparkan sebagai KPI. Wilson pula mengabaikan pengelompokan, jadi ia tidak konsisten dengan selang purata. `bezaLorong` mencampur pulangan direalisasi dengan yang belum direalisasi, dan menyembunyikan bahawa apabila kedua-dua lorong sudah ditutup, lorong 2 lebih buruk **−9.34 mata**.

### Cited Findings

**Formula (betul)**
- `selangK`: se = √(G/(G−1) · Σ_g(Σ_{i∈g}(x_i − x̄))²) / n, dengan nilai kritikal `tKrit(G−1)`. Ini penganggar Liang–Zeger dengan pelarasan sampel kecil G/(G−1) bagi purata. Jadual `T975` bagi df ≤ 30 betul (12.706, 4.303, …), dan anggaran 1.96 + 2.4/df bagi df > 30 hampir tepat — [H:3491](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [T975/tKrit H:2514–2515](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html)
- `wilson2` melaksanakan formula skor Wilson yang standard (pusat (p + z²/2n)/(1 + z²/n)). 11/24 memberi 27.9%–64.9%, sepadan dengan kiraan bebas — [H:3494](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [kira.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/kira.py)

**Kesesuaian apabila G = 2**
- Dengan G = 2, t(1) = 12.706, jadi selang 95% ialah ±12.7 SE. KPI Posisi › Dipegang › Matang memaparkan −8.44% dengan n = 2 (SNPS −14.22 dan HP −2.65, dua hari beli) dan selang −81.94 … +65.07 — [ptKpis2 H:3724](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [halaman.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/halaman.json)
- Cameron & Miller (2015) menyatakan bahawa SE berkelompok bergantung pada bilangan kelompok yang besar, bukan bilangan cerapan — [Cameron & Miller, JHR 50(2):317](https://jhr.uwpress.org/content/50/2/317)
- Ujian asimptotik juga terlebih tolak dengan 5–30 kelompok — [Cameron, Gelbach & Miller, NBER t0344](https://www.nber.org/papers/t0344.pdf)
- Kajian terkini (10–200 kelompok) mendapati nilai kritikal normal terlebih tolak, dan t(G−1) hanya separuh membaikinya — [Refined Cluster Robust Inference, arXiv 2603.24786](https://arxiv.org/pdf/2603.24786)
- Penganalisis sendiri hanya memberi status sebenar selepas ≥ 10 hari beli matang (`n_hari_min` 10, `hari_kluster_min` 5), tetapi KPI Hari Ini memaparkan selang pada G = 2 — [db analisis/papan parameter](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/analisis/papan.json)

**Wilson tanpa pengelompokan**
- `wTxt` memanggil `wilson2(k, n)` dengan n = 24 posisi, sedangkan purata di sebelahnya dikelompokkan ikut 2 hari beli. Posisi pada hari beli yang sama bergerak bersama: purata hari 8 Okt −1.17%, hari 9 Okt +1.99%. Jadi selang 28–65% terlalu sempit — [wTxt H:3496](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [kira.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/kira.py)

**`bezaLorong` (selagi naik − kaedah)**
- Daripada 5,516 posisi:
  - 4,147 memberi beza tepat 0, kerana kedua-dua lorong masih terbuka dan `hasilL` memulangkan `untung_pct` yang sama.
  - 1,268 membanding lorong 1 yang **sudah direalisasi** dengan lorong 2 yang **belum direalisasi** (`semasaL2` = tutup terkini ÷ harga beli). Purata beza bukan sifar ialah +0.327.
  - 95 posisi sudah ditutup dalam kedua-dua lorong. Purata beza bagi kumpulan ini ialah **−9.34 mata**, iaitu lorong 2 jauh lebih buruk.
  - 6 posisi hanya lorong 2nya yang keluar.
  - Sumber: [bezaLorong H:3498](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [hasilL H:1389](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [semasaL2 H:2179](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [kiraan](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/kira.py)

**Medan Monte Carlo**
- Kebarangkalian dijumlah dengan betul (Σ`p_top5` = 4.998, Σ`p_top1` = 1.002). Namun `kedudukan` jatuh di luar selang pangkat 90% MC bagi M132 (#68 lawan 13–67) dan M44 (#73 lawan 15–66). M22 (swing, `sampel_kecil`) tiada `kedudukan` dan tiada `p_top5`, tetapi masih disenaraikan tanpa bendera — [db analisis/papan](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/analisis/papan.json)

### Inferences
- **Pembaikan KPI matang.** Dalam `kpiMatang` (H:3519) dan `ptKpis2` (H:3724), jika G < 10 (selaras `n_hari_min`), paparkan "belum cukup: 2/10 hari beli · 24 posisi daripada 3 kaedah (M20, M27, M73)" dan bukan purata dengan selang. Sembunyikan KPI Matang dalam segmen "Dipegang", kerana segmen itu ialah subset terselamat (survivor).
- **Pembaikan kadar menang.** Kira kadar menang dengan n berkesan (kesan reka bentuk) atau bootstrap kelompok, bukan Wilson atas n mentah.
- **Pembaikan `bezaLorong`.** Kira beza hanya atas posisi matang, atau atas posisi yang kedua-dua lorongnya sudah ditutup. Paparkan tiga komponen secara berasingan: sifar, direalisasi lawan belum direalisasi, dan kedua-duanya direalisasi. Label "belum signifikan +0.08%" kini memberi gambaran neutral, sedangkan satu-satunya bukti direalisasi (n = 95) berat sebelah ke lorong kaedah. Bukti itu juga terdedah kepada bias pemilihan, kerana yang kedua-duanya keluar ialah posisi yang jatuh.

### Gaps
- Bootstrap kelompok tidak dijalankan untuk memberi selang alternatif. Dengan G = 2, kaedah apa pun tidak memberi inferens yang bermakna.
- Teks penuh Cameron & Miller tentang "few clusters" tidak dapat dibaca kerana WebFetch disekat.

## 4. Logik kesegaran lampu: cuti, tamat DST dan hujung minggu

### Takeaway
Kalendar NYSE 2026–2027 dan peralihan DST dikendalikan dengan betul. Namun ada dua kecacatan:
1. Lampu kini kuning dengan tajuk **"Ada data lewat"** walaupun 13/13 saluran segar, kerana `lampuTahap` menyamakan **amaran** saiz db dengan "lewat".
2. Jangkaan Lejar/Analisis/Slot (07:00 UTC hari berikutnya) lebih awal daripada masa db sebenarnya ditolak (rutin 6:02 MYT, ≈ 22:30 UTC). Akibatnya Lejar, Penganalisis dan Portfolio 10 slot berstatus "lewat" palsu sepanjang hujung minggu, dan kira-kira 15.5 jam setiap hari kerja.

### Cited Findings

**Senarai cuti**
- `cutiNyse` menyenaraikan 2026: 1 Jan, 19 Jan, 16 Feb, 3 Apr, 25 Mei, 19 Jun, 3 Jul, 7 Sep, 26 Nov, 25 Dis. Bagi 2027: 1 Jan, 18 Jan, 15 Feb, 26 Mac, 31 Mei, 18 Jun, 5 Jul, 6 Sep, 25 Nov, 24 Dis — [cutiNyse H:3426](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html)
- Pengumuman NYSE (23 Dis 2025) mengesahkan tarikh berikut:
  - Thanksgiving: 26 Nov 2026 dan 25 Nov 2027, dengan tutup awal 13:00 pada 27 Nov 2026.
  - Good Friday: 3 Apr 2026 dan 26 Mac 2027.
  - Juneteenth: 19 Jun 2026, dan 18 Jun 2027 (diperhati).
  - Independence Day: 3 Jul 2026 dan 5 Jul 2027.
  - Krismas: 25 Dis 2026, dan 24 Dis 2027 (diperhati).
  - Presidents' Day: 16 Feb 2026 dan 15 Feb 2027.
  - Pengumuman itu juga meliputi 2028.
  - Sumber: [NYSE Group via BusinessWire](https://www.businesswire.com/news/home/20251223981478/en/NYSE-Group-Announces-2026-2027-and-2028-Holiday-and-Early-Closings-Calendar), [ICE IR](https://ir.theice.com/press/news-details/2025/NYSE-Group-Announces-2026-2027-and-2028-Holiday-and-Early-Closings-Calendar/default.aspx)

**DST**
- DST AS tamat Ahad 1 Nov 2026 dan bermula semula 14 Mac 2027 — [Almanac](https://www.almanac.com/daylight-saving-time-ends), [Time Out](https://www.timeout.com/usa/news/when-do-the-clocks-go-back-in-2026-heres-when-daylight-saving-time-officially-ends-100626)
- `nyUtc` membaca offset `America/New_York` bagi setiap tarikh melalui `Intl` — [H:3430](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html)

**Simulasi jam (data snapshot 23 Okt)** — [masa.js](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/masa.js)
- **DST**:
  - 2 Nov 2026 15:00Z (10:00 EST): belian dijangka = 30 Okt ✓.
  - 2 Nov 16:00Z: belian dijangka = 2 Nov ✓, dengan 10:51 EST = 15:51Z.
  - 30 Okt 14:55Z (10:55 EDT): 30 Okt ✓.
  - 15 Mac 2027 14:30Z (10:30 EDT): 12 Mac ✓.
- **Cuti**:
  - 26 Nov 23:30Z: sesi dijangka 25 Nov ✓ (Thanksgiving dilangkau).
  - 27 Nov 23:30Z: 27 Nov ✓.
  - 25 Dis 23:30Z: 24 Dis ✓.
  - 1 Jan 2027 08:00Z: 31 Dis ✓.
  - 26 Mac 2027 23:30Z: 25 Mac ✓ (Good Friday).
- **Hujung minggu**: Ahad 25 Okt 12:00Z memberi sesi harga dijangka 23 Okt ✓.
- **Lampu sekarang**: pada 24 Okt 04:40Z, lampu = "lewat". Senarai saluran: semua ✓ atau "menunggu jadual" (Lejar, Penganalisis, Slot). Satu-satunya sebab ialah amaran `papertrade/moomoo 238646 bait = 91% had db` dalam `harian/status.ralat`.
  - `lampuTahap` memulangkan 'lewat' jika `amaranOf(...).length`, dan `lampuHtml` menterjemah 'lewat' sebagai "Ada data lewat".
  - Sumber: [lampuTahap H:3455](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [B:62–65](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/laman/blok_audit.js), [db harian/status](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/harian/status.json)
- **Lejar, Penganalisis dan Slot**: `jl = jangkaSesi(31)`, iaitu sesi D dijangka siap pada D + 31 jam = 07:00 UTC esoknya.
  - Simulasi pada Sab 24 Okt 08:00Z, Ahad 25 Okt 12:00Z dan Isn 26 Okt 12:00Z memberi ketiga-tiganya "lewat" dan lampu kuning.
  - Audit v103 merekod bahawa `analisis/papan` dan `portfolio_slot` hanya ditolak bersama db harian oleh rutin 6:02 MYT (≈ 22:30 UTC). Cron Lejar juga tiba 2.5–6 jam lewat, jadi sesi 23 Okt hanya sampai ke db pada Selasa 27 Okt 06:02 MYT.
  - Sumber: [saluran B:46–59](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/laman/blok_audit.js), [Audit dashboard tab demi tab.md](/home/user/papertrade-claude/reports/Audit%20dashboard%20tab%20demi%20tab.md), [masa.js](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/masa.js)
- **Saluran tanpa jadual**: "Sektor (mingguan)" dan "SST" dinilai "ok" jika ≤ 8 hari. SST bertarikh 20 Okt dikira segar pada 24 Okt — [B:58](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/laman/blok_audit.js)
- **Lampu tidak menangkap kelewatan separa.** Sebanyak 46 saham tiada bar yfinance 23 Okt (`trend.tarikh_data` 20261022). Ini menjejaskan 187 baris dan 148 posisi lorong kaedah yang dipegang. Namun saluran "Trend" dan "Lorong 2" dinilai "segar" ikut tarikh dokumen — [db harian/trend](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/harian/trend.json), [esok.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/esok.py)
- **Hari dagangan bagi earnings**: `hariAntara` di halaman dan `np.busday_count` dalam `jana_db.earn_kini` mengira hari Isnin–Jumaat tanpa cuti NYSE. Bilangan "hari dagangan" akan terlebih 1 apabila Thanksgiving atau Krismas jatuh dalam tetingkap — [hariAntara H:1392](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [jana_db.py:105](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/jana_db.py)

### Inferences
- **Pembaikan 1: amaran.** `lampuTahap` perlu memulangkan tahap berasingan, contohnya 'amaran' dengan teks "Data segar · 1 amaran sistem", atau mengekalkan 'ok' dan memaparkan amaran sebagai cip sahaja.
- **Pembaikan 2: jangkaan Lejar.** Gantikan `jl = jangkaSesi(31)` dengan jangkaan "satu sesi di belakang data harga", iaitu `jl = hariKerjaSebelum(js)`. Status "lewat" hanya bila v < `hariKerjaSebelum(js)`, dan "menunggu jadual" bila v = `hariKerjaSebelum(js)` < js. Cara ini mengikut masa tolakan db sebenar, dan menghapuskan amaran palsu pada hujung minggu dan siang hari kerja.
- **Pembaikan 3: kelewatan separa.** Tambah saluran "Liputan harga 23 Okt: 698/744 saham", atau cip kuning apabila `trend.rows` mempunyai `tarikh_data` < D.
- **Pembaikan 4: kalendar.** Tambah cuti 2028 (sudah diumumkan NYSE). Gunakan senarai cuti yang sama dalam `hariAntara` dan dalam `np.busday_count(..., holidays=...)`.

### Gaps
- Waktu sebenar tolakan db oleh rutin 9:35 NY bagi `harian/status.beli_pada` tidak disahkan dengan log commit. Simulasi Isn 26 Okt 22:00Z hanya menunjukkan status "lewat" kerana snapshot data adalah statik.

## 5. Adakah ralat data yang diketahui (DAC, ACA, LNTH, VIAV/LITE) sudah dibetulkan, dan adakah ralat baharu?

### Takeaway
Keempat-empat ralat lama sudah dibetulkan dalam CSV pratonton. Ralat ikon earnings v103 (FRD, GRAL, CRSR, PSO) juga sudah betul. Ditemui dua masalah data baharu:
1. Saham dengan earnings **pada** tarikh data (23 Okt, sudah dilapor sebelum buka) dipaparkan sebagai "0h / hari ini" dan dikira dalam "≤ 10 hari".
2. Sebanyak 46 saham tanpa bar yfinance 23 Okt menyebabkan ATR, trend dan harga lorong 2 bercampur tarikh (22 lawan 23 Okt).

### Cited Findings

**Ralat lama yang sudah dibetulkan**
- **DAC M80/M90**: harga_beli kini 170.19, sama dengan buka stor 12 Okt (170.19). Untung akhir M80 −7.66% dan M90 −5.32%, sepadan dengan nilai betul dalam audit v103 — [claude*.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/papertrade/), [harga_B.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/data/harga/stor/harga_B.csv)
- **ACA**: kesemua 8 posisi kini `tidak_sah`, dengan sebab "isyarat palsu: saham diambil alih (umum 2026-06-22, CRH, tawaran $150.00; senarai)". Kesemuanya `tutup_semua`, keluar 22 Okt @149.15 — [claude*.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/papertrade/)
- **LNTH M03** (dibeli 21 Okt @100.28): `tidak_sah`, dengan sebab "diambil alih (umum 2026-08-03, Curium, tawaran $102.50)". Ditutup 23 Okt @99.80 (−0.48%) — [claude*.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/papertrade/)
- **VIAV dan LITE** (Moomoo, S04V2): VIAV keluar lorong 2 pada 15 Okt @36.88 (−19.98%), dan LITE pada 16 Okt @853.485 (−18.19%). Kedua-duanya sepadan dengan kiraan semula audit v103 — [moomoo.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/papertrade/moomoo.csv)
- **Ikon earnings**: `earn_kini` kini FRD 4 Nov, GRAL 4 Nov, CRSR 5 Nov dan PSO 25 Feb 2027 (Khamis). Tiada `earn_kini` yang jatuh pada hujung minggu (0/688) — [db ringkas_c](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/papertrade/ringkas_c.json)

**Masalah baharu 1: earnings "0h"**
- Enam saham mempunyai `earn_kini` = 2026-10-23 = tarikh data, dengan `earn_kini_h` 0: GNTX, SLB, BCPC, RDY, INFY dan E. Panel memaparkan "23 Okt · 0h", dan ikon 📅 menulis "hari ini". Ini kerana `seterusnya()` menerima tarikh **pada atau selepas** sesi data — [jana_db.py:92–105](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/jana_db.py), [kalendar_earnings.py:71–79](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/kalendar_earnings.py), [earnH H:3688](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html)
- SLB mengeluarkan keputusan suku ketiga 2026 pada 23 Okt 2026 jam 7:00 pagi ET, iaitu sebelum pasaran dibuka, dengan panggilan pada 9:30 pagi ET. Reaksi harga itu sudah termasuk dalam tutup 23 Okt — [SLB press release](https://www.slb.com/newsroom/press-release/2026/pr-2026-0928-q3-earnings-call-announcement), [SEC 8-K SLB](https://www.sec.gov/Archives/edgar/data/0000087347/000119312526429435/d151271dex99.htm)
- Sebanyak 53 saham aktif (daripada 726) tiada `earn_kini`, dan disingkirkan daripada panel tanpa tanda. Contohnya SAIH, ANL, TANH dan SVRN (tiada data), manakala SSNC, BE dan DOV sudah melapor 22 Okt — [db ringkas_c](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/papertrade/ringkas_c.json)

**Masalah baharu 2: harga bercampur tarikh**
- `terkini.csv` tiada bar 23 Okt bagi 46 saham dalam alam posisi, termasuk WAT, SRE, FTV, BURL, CNX dan VAL. Bagi saham ini, `harian/trend` (ATR%, tutup c) masih bertarikh 22 Okt, sedangkan `harga_terkini` CSV ialah tutup 23 Okt daripada Moomoo. Beza harga paling besar: KFRC +9.0%, NE +8.5%, XPRO +8.1%, SDRL +6.4% dan VAL +5.6% — [terkini.csv](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/data/harga/terkini.csv), [esok.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/esok.py)
- Kesannya kepada setiap fungsi:
  - `jarakAtr` mencampur ATR 22 Okt (`t.atr_pct × t.c`) dengan harga 23 Okt.
  - `l2Info` dan `semasaL2` memakai `tutupAkhir` (garis), iaitu tutup 22 Okt, bagi 36 pegangan lorong 2 sahaja dalam saham ini.
  - Sumber: [jarakAtr H:3675](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [l2Info H:2190](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [tutupAkhir H:2178](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html)
- Bendera kualiti `bar_moomoo` sudah ditanda bagi 187/187 baris saham ini (2 juga `bar_sintetik`), jadi barisnya diberi amaran ⚠ data. Kesan pada kiraan "Hampir" kecil, iaitu 2 daripada 240 baris — [db ringkas_c kualiti](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/papertrade/ringkas_c.json), [esok.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/esok.py)

### Inferences
- **Pembaikan earnings.** Dalam `earn_kini`, anggap tarikh = S sebagai "lalu" (ikon "baru lapor") kecuali sumber menyatakan selepas tutup (AMC). Dalam panel Esok, kecualikan `hariKeEarn` = 0, atau labelkannya "23 Okt (sudah dilapor)". Tambah "n saham tanpa tarikh earnings" di bawah panel.
- **Pembaikan harga bercampur.** Bagi saham dengan `trend.tarikh_data` < D:
  - Guna `harga_terkini` untuk `l2Info` dan `semasaL2`, atau tanda jarak sebagai "ATR 22 Okt".
  - Isi bar 23 Okt daripada Moomoo ke dalam stor kerja `jana_db`, supaya trend, ATR dan garis sama tarikh.

### Gaps
- Tarikh earnings lima saham "0h" yang lain (GNTX, BCPC, RDY, INFY dan E) tidak disahkan dengan sumber luar. Hanya SLB yang disahkan (dikeluarkan sebelum buka).
- Sebab yfinance tiada bar 23 Okt bagi saham besar seperti WAT, SRE dan FTV tidak disiasat.

## 6. Medan ranking dalam tab Kaedah dan "Calon teratas"

### Takeaway
Susunan lalai `lb_bulan` (had bawah julat sebulan) pada dasarnya ialah **susunan ikut hari pegang**: Spearman ρ = 0.93 dengan `hari`, dan ρ = −0.73 dengan P(5 teratas). Akibatnya "Calon teratas" Hari Ini (M111, M55, M100) mempunyai P(5 teratas) hanya 2%, 5% dan 0.4%. Kaedah #1 Penganalisis (M21, P(#1) 29%) pula jatuh ke baris 74/75. Semua 75 had bawah adalah negatif.

### Cited Findings

**Punca dalam kod**
- `lb_bulan = sebulan(lo)`, dengan `sebulan(x) = x ÷ hari × 21`. `rankRows` menyusun kaedah swing ikut `lb_bulan` secara menurun — [penganalisis.py:784–785](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/penganalisis.py), [rankRows H:3532](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html)

**Kesan pada susunan**
- Semua 75 kaedah swing mempunyai `lb_bulan` < 0. Spearman(`lb_bulan`, `hari`) = 0.93, Spearman(`lb_bulan`, `p_top5`) = −0.73, dan Spearman(`skor_bulan`, `hari`) = 0.31. Sepuluh baris teratas mempunyai hari pegang 29.9, 28.2, 29.5, 28.0, 29.7, 25.5, 27.6, 28.5, 29.2 dan 18.2, berbanding median 17.3 bagi semua kaedah swing — [kiraan](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/halaman.json), [db analisis/papan](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/analisis/papan.json)
- Tiga calon teratas yang dipapar:

  | Calon | lb_bulan | P(5 teratas) | Pangkat 90% | Kedudukan skor | Catatan |
  |---|---|---|---|---|---|
  | M111 | −2.233 | 2.0% | 8–63 | #10 | |
  | M55 | −2.533 | 4.7% | 6–64 | #7 | |
  | M100 | −2.560 | 0.4% | 14–65 | #61 | ⚑ DITOLAK |

  Sumber: [panelCalon H:3537](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [halaman.json](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/ketepatan/halaman.json)
- M21 (kedudukan #1, `p_top1` 0.289, `p_top5` 0.449) berada di baris 74/75 dalam susunan lalai jadual. M73 (#74, `hari` 4.8) pula mempunyai `p_top5` 12.8%, iaitu enam kali ganda M111 — [db analisis/papan](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/analisis/papan.json)

**Kestabilan kedudukan**
- Kedudukan skor rapat: IQR `skor_bulan` swing ialah 0.27–0.52. M73 jatuh 35 tempat (#39 → #74) kerana 5 posisi matang daripada 1 hari beli (`h_purata` −5.83, nb = 1). Panel "Berubah" memaparkannya sebagai "M73 ▼35", dengan nota bahawa gerakan dalam julat 90% bukan isyarat — [panelBerubah H:2256](/home/user/papertrade-claude/.claude/worktrees/pratonton/BacktestShariah2/standard/dashboard_v2.html), [db analisis/papan](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/analisis/papan.json)

**Medan bukti**
- "Bukti 0/10 hari beli" bagi tiga calon betul (`g_matang` 0). M20 dan M73 mempunyai `g_matang` 1, `tarikh_sebenar` 2026-11-04 dan `matang_20` 26–27 Okt, selaras dengan banner "status sebenar pertama ±4 Nov 2026" — [db analisis/papan](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/pratonton_audit/db/analisis/papan.json)

### Inferences
- **Mengapa susunan ini berat sebelah.** Dalam fasa bukti 0 (100% backtest dipotong), had bawah per dagangan didominasi oleh SD backtest. Membahagi had bawah negatif dengan `hari` mengecutkan kerugian sebulan bagi kaedah pegang lama. Jadi susunan lalai memberi ganjaran kepada tempoh pegang, bukan kepada bukti.
- **Pembaikan susunan lalai.** Pilihan:
  - Susun ikut P(5 teratas) (MC sendiri).
  - Susun ikut `skor_bulan` dengan julat.
  - Kekalkan `lb_bulan` hanya selepas `g_matang` ≥ 10, atau kira had bawah dalam unit yang tidak bergantung pada hari pegang.
- **Pembaikan "Calon teratas".** Jangan menamakan senarai `lb_bulan` sebagai "Calon teratas" selagi semua had bawah < 0. Paparkan "Tiada calon: semua julat merangkumi rugi".
- **Pembaikan pembulatan.** Selaraskan semua rujukan "#n" (banner fasa, nota gabungan, panel Berubah) dengan susunan yang dipapar. Bendera M22 (`sampel_kecil`, tiada `p_top5`) juga perlu ditambah.

### Gaps
- Sebab `kedudukan` M132 dan M44 jatuh di luar selang pangkat MC 90% tidak disiasat dalam `penganalisis.py`. Kemungkinan selang MC dikira atas skor per dagangan, sedangkan `kedudukan` dikira atas `skor_bulan`, tetapi ini belum disahkan.

## Ringkasan: dipapar lawan dijangka (kiraan semula)

| Item | Dipapar | Kiraan semula | Status |
|---|---|---|---|
| Aktiviti: dibeli / keluar / dilangkau | 760 / 175 / 9 | 760 / 175 / 9 (status hulu: 761 / 186) | ✓ (kaunter hulu beza takrif) |
| C matang: purata, selang 95% | +0.02%, −18.76…+18.80 | 0.0171, −18.76…+18.80 (G = 2, t = 12.706) | ✓ tetapi tidak bermakna; 3 kaedah sahaja |
| C matang: menang (Wilson) | 46% (28–65%) | 11/24, 27.9–64.9 | ✓ formula; abaikan pengelompokan |
| Bukti hadapan | 10 / 9,810 | 10 / (8,528 + 1,620 − 338) | ✓ (data 22 Okt) |
| Portfolio beku / rawak / SPY | −0.72 / +0.19 / −0.31 | −0.72 / +0.19 / −0.31 | ✓ (1 sesi; baris SPY jadual slot −1.20 bagi tempoh lain) |
| Esok: dijual | 63 (47 saham) | 51 L1 + 12 L2; 1 tidak sah | ✓ kiraan; populasi termasuk tidak sah |
| Esok: dibeli | 92 | 92 isyarat watchlist (57 kaedah) | ✓ kiraan; bukan senarai beli (biasa 480–760) |
| Esok: hampir ≤ 1 ATR | 240 (144 saham) | 240; Posisi Dipegang 166; Semua 239 | ✓ kiraan; populasi berbeza |
| Esok: earnings ≤ 10 hari | 507 | 507 saham (3,804 posisi); 6 saham "0h" sudah dilapor | ✓ kiraan; unit dan "0h" mengelirukan |
| Posisi: dipegang, belum direalisasi | 4,150; +3.28%; 74% | 4,150; 3.285; 73.8% | ✓; ikut saham +0.96% |
| Posisi: dua lorong | +3.28 / +3.28, beza −0.01 | 3.285 / 3.279, −0.006 | ✓ |
| Hari Ini: beza lorong | +0.08 ± 0.13, G 12 | 0.0813 ± 0.1295, G 12 | ✓ kiraan; campur direalisasi dan belum; kedua-dua keluar −9.34 (n = 95) |
| Lampu | "Ada data lewat" | 13/13 segar + 1 amaran | ✗ label |
| Calon teratas | M111, M55, M100 | P(5 teratas) 2% / 5% / 0.4% | ✗ susunan berat sebelah hari pegang |
