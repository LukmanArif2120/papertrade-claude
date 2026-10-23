# Peraturan praktikal status trend papan (D10+H2): spesifikasi tepat, contoh saham sebenar 22 Okt 2026, kes tepi, banding SST dan paparan

Disediakan 23 Okt 2026 (sambungan larian yang terhenti akibat container dimulakan semula; semua skrip dijalankan semula atas data yang sama). Data harga: stor repo hingga bar 21 Okt 2026 + `data/harga/terkini.csv` hingga 22 Okt 2026. Alam saham: posisi Papertrade C yang masih terbuka dan sah (`BacktestShariah2/papertrade/claude*.csv`, 60 fail) dan `papertrade/watchlist.csv`, iaitu 701 saham. Takrif yang diperincikan ialah cadangan laporan [Penentuan status trend saham](../../reports/Penentuan%20status%20trend%20saham.md) (selepas ini "LAP"). Tiada fail repo lain diubah, dan tiada artifact atau db disentuh.

Semua skrip dan output berada di `SP = /tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/trend6/`. Folder ini sementara: angka penting disalin ke nota ini.
- `trend.py`: pelaksanaan rujukan (versi `D10H2-r2`). Arahan: `python3 trend.py dokumen` dan `python3 trend.py garis TICKER --mula YYYYMMDD`. Larian penuh mengambil 5.9 s dengan RSS maksimum 157 MB.
- `papar.py`: penjana teks pill, tooltip dan berita.
- `analisis.py`, `tambahan.py`, `tambahan2.py`, `tambahan3.py`: statistik alam sebenar. Output dalam `*_out.txt`, `ringkasan.csv` dan `jurang.csv`.
- `sahkan_s.py`: semakan stor lawan sejarah penuh dataset S1–S4.
- `sst_banding.py`: banding dengan SST.
- `garis_<TICKER>.txt`: garis masa silang dan perubahan status.
- `trend_doc.json`: dokumen db contoh.
- `jadual_wakil.md`: jadual wakil.

Rujukan sumber dalam nota: [AN] = `SP/analisis_out.txt`; [T1] = `SP/tambahan_out.txt`; [T2] = `SP/tambahan2_out.txt`; [T3] = `SP/tambahan3_out.txt`; [SAH] = `SP/sahkan_s_out.txt`; [SST] = pemerhatian alat `mcp__SST_Terminal__technical_analysis`, 23 Okt 2026 03:52 UTC, dan `SP/sst_banding_out.txt`; [G-X] = `SP/garis_X.txt`; [PAP] = `SP/papar_out.txt`; [PENG] = [sumber_pengamal_disahkan.md §8](sumber_pengamal_disahkan.md).

## 1. Spesifikasi algoritma tepat: siri harga, mesin keadaan, medan beku dan skema dokumen db

### Takeaway
Status dikira semula sepenuhnya setiap malam daripada siri terlaras stor. Mesin pengesahan 2 tutup **menyegerak sendiri**: selepas mana-mana dua `mentah` berturut yang sama, status sudah ditentukan tanpa mengira titik mula sejarah. Akibatnya, sejarah stor bergolek 520 bar memberi status dan tarikh_sah yang sama dengan sejarah penuh (382/382 saham sepadan). Tarikh_sah, tutup pertama, `dari`, `sebab` dan titik mula hanya bergantung pada bar ≤ tarikh_sah, jadi semuanya beku secara automatik. Pengecualian hanya apabila (a) sejarah dilaras semula, atau (b) tarikh_sah terkeluar daripada tetingkap 520 bar; kes (b) dibawa daripada dokumen semalam. Dokumen db untuk 701 saham bersaiz 95,414 bait (≈ 136 bait sesaham), jadi 800 saham ≈ 109 KB, jauh di bawah 256 KB.

### Cited Findings
**Siri harga dan konvensyen laras**
- Stor = `data/harga/stor/harga_A.csv` + `harga_B.csv`, dipotong kepada 520 bar terakhir setiap ticker (`kod/stor.py`: `SIMPAN_BAR = 520`, `groupby('ticker').tail(SIMPAN_BAR)`). `status.json`: dikemas kini 2026-10-22 14:30 UTC, `bar_terakhir` 20261021, `laras` RMR 1.025181 — [kod/stor.py baris 7, 32; data/harga/stor/status.json](/home/user/papertrade-claude/BacktestShariah2/kod/stor.py)
- Konvensyen ([CLAUDE.md "Stor harga"](/home/user/papertrade-claude/CLAUDE.md)):
  - bar sebelum ~2 Okt 2026 dilaras hadapan termasuk dividen; selepas itu yfinance, pecahan sahaja;
  - sejarah dilaras hanya jika nisbah bar bertindih seragam (`nisbah_laras`: |r − 1| ≤ 0.3% = sama; laras jika serak ≤ 0.2% dan sekurang-kurangnya 3 bar atau nisbah pecahan lazim; selain itu "anomali", tiada laras);
  - peristiwa besar melalui `data/harga/faktor.csv`. Fail ini kini memuatkan HMY 9 Okt ×0.972625 dan RMR 19 Okt ×0.975437 (dividen khas) — [kod/stor.py nisbah_laras](/home/user/papertrade-claude/BacktestShariah2/kod/stor.py); [data/harga/faktor.csv](/home/user/papertrade-claude/BacktestShariah2/data/harga/faktor.csv)
- `terkini.csv` mengandungi 928 ticker hingga 21 Okt, tetapi hanya **833** ticker bagi 22 Okt. Akibatnya **63 daripada 701** saham alam berhenti pada 21 Okt — [T3]
- `trend.muat_harga` hanya menyambung bar `terkini.csv` yang **lebih baharu** daripada bar akhir stor. Bar bertindih terakhir dibanding: jika nisbah tutup berbeza > 0.3%, stor sahaja dipakai dan status ditanda "semak data". Hari ini tiada penolakan. RMR hanya bernota (bar lama `terkini.csv` berbeza dengan nisbah median 1.0252 kerana belum dilaras dividen, tetapi bar akhir sepadan) — [SP/trend.py; T3 nota]
- Tutup stor lawan dataset S1–S4 (382 saham pada 2 Okt 2026): nisbah median 1.0, p1–p99 0.9997–1.0, dan hanya 3/382 berbeza > 0.3% — [SAH]

**Pseudo-kod (dilaksana tepat dalam `SP/trend.py`, fungsi `mentah`, `mesin`, `titik_mula`, `sebab`, `kira`)**
```
INPUT  bar harian sendiri (tarikh, O, H, L, C) menaik; siri terlaras stor + bar terkini.csv lebih baharu
PARAM  50/150/200; BAHARU = 20; LAMA = 60; W_TITIK = 63; N_ATR = 14
1  SMA_k[t] = purata mudah C[t−k+1..t] atas BAR (bukan hari kalendar; hari tanpa bar tidak wujud)
2  mentah[t] = +1 jika C > S50 > S150 > S200 (semua ketat); −1 jika C < S50 < S150 < S200; 0 selainnya;
              tiada jika S200 belum wujud (t < 199). Kesamaan (=) di mana-mana → 0 (Neutral)
3  mesin, t = 1..n−1 (langkau jika mentah[t] atau mentah[t−1] tiada):
     status belum ada: jika mentah[t] = mentah[t−1] → status = mentah[t]; i_mula = t   (TERSENSOR)
     selainnya:        jika mentah[t] = mentah[t−1] = X ≠ status → peristiwa(isyarat = t−1, sah = t, dari = status, ke = X);
                       status = X
4  ada peristiwa: i_sah = sah terakhir; tepat = 1.  Tiada: i_sah = i_mula; tepat = 0; dari = tiada
5  umur = n − i_sah (bar tarikh_sah = 1); pct_sejak = C[n−1] / C[i_sah] − 1
6  sub = "baharu" jika tepat dan umur ≤ 20; "lama" jika umur > 60; kosong selainnya
7  amaran = (status = −1 dan umur > 60)
8  titik mula (status ±1 dan tepat): a = max(0, i_sah − 62)
     Bullish: j = indeks L minimum dalam [a, i_sah]; Bearish: H maksimum; seri → bar PALING AKHIR
     tembus = tarikh pertama selepas i_sah dengan L < titik (Bullish) / H > titik (Bearish); kekal selepas diset
9  sebab (kod 'C50', '50_150', '150_200', digabung '+'):
     hilang X (X ≠ 0 → lain): syarat X yang gagal pada tutup pertama
     jadi X (0 → X): syarat X yang gagal pada bar sebelum tutup pertama (syarat yang baru dipenuhi)
10 calon = mentah[n−1] jika ≠ status (tutup pertama hari ini; tidak mengubah status)
11 ATR14% = purata mudah 14 TR ÷ C[n−1] × 100; TR = maks(H−L, |H−C₋₁|, |L−C₋₁|)  (= enjin.atr / keluar_lorong.atr)
12 prasyarat: n ≥ 201 bar (SMA200 + dua tutup); jika tidak → "Tiada status" (ATR% tetap dikira jika n > 14)
```
- Pertukaran terus Bullish↔Bearish dibenarkan oleh mesin, tetapi berlaku **0 kali** dalam 6,132 pertukaran disahkan (alam 701 saham, liputan status ≤ 1.27 tahun setiap saham). Kesemua pertukaran melalui Neutral — [T2: senarai sebab hanya mengandungi Bearish→Neutral, Bullish→Neutral, Neutral→Bearish, Neutral→Bullish]

**Sifat penyegerakan dan pembekuan (disahkan)**
- Status yang dikira daripada stor (≤ 520 bar) sama dengan status daripada sejarah penuh dataset S1–S4 (sejak 2019) pada 2 Okt 2026 bagi **382/382** saham alam. `tarikh_sah` sama bagi semua yang `tepat`, dan **0** titik mula berbeza — [SAH]
- Liputan status = n − 200 bar. Saham `harga_A` (520 bar) mempunyai ~320 sesi sejarah status. Saham yang sejarahnya bermula 17 Apr 2025 (cth. AMSC 381 bar, AVY 380 bar) hanya ~180 sesi — [T3: n_bar median 521, p5 380; stor bar pertama AMSC 20250417]
- Hari ini **5** saham tersensor, semuanya Neutral: AMSC ≥ 181, AVY ≥ 180, ELVR ≥ 86, PARK ≥ 22 dan VSNT ≥ 15 sesi. Dataset S1–S4 tiada sejarah lebih awal bagi kelima-limanya — [T3; SP/sensor_out.txt]
- `trend.bawa_semalam`: jika kiraan baharu tersensor tetapi dokumen semalam `tepat` dengan status sama, kekalkan `sah, tepat, dari, sebab, isyarat, titik_*, tembus, c_sah` semalam dan tambah umur +1 bagi setiap bar baharu. Jika kedua-duanya `tepat` tetapi `sah` berbeza tanpa pertukaran, pakai kiraan baharu dan tulis nota "sejarah stor berubah" — [SP/trend.py]

**Skema dokumen db (cadangan nama `harian/trend`, sama seperti pratonton `bina_trend.py`)**
- Peringkat dokumen: `tarikh` (int YYYYMMDD, bar terbaru merentas saham), `versi` ("D10H2-r2"), `lajur` (senarai nama), `takrif` (teks), `nota` {saham: teks}, `rows` (senarai baris) — [SP/trend_doc.json]
- Baris (22 medan, susunan `lajur`). Contoh nilai daripada MSM pada 22 Okt — [SP/trend_doc.json]

| Medan | Jenis | Makna | Contoh MSM |
|---|---|---|---|
| saham | teks | ticker | "MSM" |
| s | 1/0/−1/null | status (null = tiada status) | 1 |
| sub | teks | "baharu"/"lama"/"" | "baharu" |
| sah | int | tarikh tutup kedua (beku) | 20260929 |
| umur | int | sesi sejak sah (sah = 1) | 18 |
| tepat | 0/1 | 0 = tersensor (umur ialah had bawah) | 1 |
| pct_sejak | nombor 2 tp | C kini ÷ C pada sah − 1 (%) | −9.73 |
| dari | 1/0/−1/null | status sebelum | 0 |
| sebab | teks | kod syarat pertukaran | "C50" |
| isyarat | int | tarikh tutup pertama (audit, tidak dipapar) | 20260928 |
| titik_tarikh, titik_harga | int, nombor | titik mula (beku) | 20260902, 115.73 |
| pct_titik | nombor | C kini ÷ titik − 1 (%) | −2.85 |
| tembus | int/null | tarikh titik mula pertama kali ditembusi | 20261022 |
| atr_pct | nombor | ATR14% | 3.98 |
| mentah | 1/0/−1 | susunan pada tutup terakhir | 0 |
| calon | 1/0/−1/null | tutup pertama keadaan lain hari ini | 0 |
| susun | teks 3 aksara | tanda C−S50, S50−S150, S150−S200 | "-++" |
| jarak | [3 nombor] | % C/S50, S50/S150, S150/S200 | [−8.92, 8.2, 6.04] |
| c, c_sah | nombor | tutup kini, tutup pada sah | 112.43, 124.55 |
| tarikh_data | int | bar terakhir saham ini | 20261022 |

- Saiz: 701 baris = **95,414 bait**. Versi r1 tanpa `sebab`/`isyarat` = 84,052 bait — [SP/trend_doc.json; larian `trend.py dokumen`]

**Perbezaan dengan pratonton `scratchpad/asal/bina_trend.py`**
- Pratonton membina siri dengan `drop_duplicates(keep='last')` atas stor + `terkini.csv`, jadi bar `terkini.csv` yang belum dilaras menimpa bar stor (kes RMR). Ia juga menetapkan status awal tanpa pengesahan pada bar 199, mengira umur dari **tutup pertama**, memasukkan `moomoo.csv` serta semua baris claude (termasuk yang sudah ditutup atau `tidak_sah`), dan melangkau saham < 205 bar secara senyap — [scratchpad/asal/bina_trend.py](/tmp/claude-0/-home-user-papertrade-claude/a40a74c5-2874-5b77-8397-3036eb71ebfc/scratchpad/asal/bina_trend.py)
- Atas data hingga 21 Okt, status pratonton sama dengan rujukan bagi **700/700** saham, tetapi umur pratonton = umur rujukan **+1** bagi kesemua 700 (kiraan dari tutup pertama) — [T1]

### Inferences
- **Bekukan tarikh, bukan harga.** Simpan `sah`, `isyarat`, `titik_tarikh` sebagai kunci beku. Harga titik dan C pada sah pula dibaca semula daripada siri terlaras semasa setiap malam (seperti `kira` sekarang), supaya % kekal betul selepas pecahan atau faktor dividen. Bagi baris yang dibawa oleh `bawa_semalam`, darabkan `titik_harga` dan `c_sah` dengan faktor dalam `faktor_diguna.csv`/`log_laras.csv` jika laras berlaku selepas dokumen semalam. Pelaksanaan rujukan belum membuat pendaraban ini.
- Takrif umur mesti kekal "sejak pertukaran disahkan terakhir", tanpa menyambung keadaan sama yang terputus ≤ 5 sesi. Sebabnya, kontras "Bearish > 60 sesi" dalam LAP diukur dengan takrif ini. Kesannya nyata: TTD sekarang 116 sesi, tetapi 207 sesi jika jeda 4 sesi pada Mei disambung (lihat §4).
- Medan `sebab` murah (≈ 5 bait) dan cukup untuk teks berita tanpa membaca SMA. Medan `isyarat` disimpan untuk audit sahaja.
- Pemecahan dokumen hanya perlu jika alam melebihi ~1,800 saham (256 KB ÷ 136 bait). Cadangan pecahan: `harian/trend_A` (A–L) dan `harian/trend_B` (M–Z).
- Jika lajur `peristiwa` (3 pertukaran terakhir, ~45 bait) ditambah untuk paparan sejarah ringkas, 800 saham kekal ≈ 145 KB.

### Gaps
- `bawa_semalam` belum diuji atas larian berbilang malam sebenar, kerana hanya satu tarikh data tersedia dalam sesi ini.
- Pendaraban faktor bagi medan yang dibawa belum dilaksanakan atau diuji.
- Kesamaan tepat (C = SMA50 dan seumpamanya) tidak dikira kekerapannya. Peraturan ditetapkan (→ Neutral), tetapi kesannya tidak diukur.

## 2. Status hari ini bagi posisi dan watchlist sebenar (bar 22 Okt 2026)

### Takeaway
Daripada 701 saham, 25.5% Bullish, 63.9% Neutral, 10.4% Bearish dan 1 tiada status. **Bearish lama hanya 3 saham** (BLDR, ROL, TTD), jadi amaran itu jarang dan tidak bising. Sebaliknya **54 saham** mempunyai tutup pertama keadaan lain pada 22 Okt. Mengikut sejarah, ~74% daripadanya akan disahkan esok, jadi papan perlu jelas bahawa status hanya bertukar pada tutup kedua. Titik mula hampir tidak pernah ditembusi selepas pengesahan: 1 daripada 252, iaitu MSM pada 22 Okt.

### Cited Findings
**Taburan (peringkat saham; satu saham boleh berada dalam lebih daripada satu sumber)** — [AN]
- P1 = sekurang-kurangnya satu baris dengan lorong kaedah masih terbuka (`keluar` = False).
- P2 = baris dengan lorong kaedah sudah keluar tetapi lorong 2 masih terbuka (`tutup_semua` = False).
- W = watchlist.
- Baris `tidak_sah`, `tidak_dibeli` dan `tutup_semua` dikecualikan.

| Status | Semua (701) | P1 (570) | P2 (486) | W (120) |
|---|---|---|---|---|
| Bullish baharu (≤ 20 sesi) | 117 | 114 | 83 | 30 |
| Bullish (21–60) | 34 | 32 | 27 | 9 |
| Bullish lama (> 60) | 28 | 26 | 23 | 5 |
| **Jumlah Bullish** | **179 (25.5%)** | 172 (30.2%) | 133 (27.4%) | 44 (36.7%) |
| **Jumlah Neutral** | **448 (63.9%)** | 348 (61.1%) | 306 (63.0%) | 65 (54.2%) |
| Bearish baharu (≤ 20) | 39 | 25 | 25 | 5 |
| Bearish (21–60) | 31 | 23 | 19 | 4 |
| Bearish lama (> 60, amaran) | 3 | 1 | 3 | 2 |
| **Jumlah Bearish** | **73 (10.4%)** | 49 (8.6%) | 47 (9.7%) | 11 (9.2%) |
| Tiada status | 1 (HQ) | 1 | 0 | 0 |

- Umur Neutral (semua): ≤ 20 sesi 166, 21–60 sesi 126, > 60 sesi 151, tersensor 5. Neutral **dari Bullish 282**, **dari Bearish 161**, tidak diketahui 5 — [AN]
- Umur median: Bullish 11 sesi, Neutral 32, Bearish 20 — [AN]
- ATR14% median (p25–p75): Bullish 3.10% (2.41–3.74), Neutral 3.37% (2.67–4.53), Bearish 3.47% (2.69–4.17) — [AN]
- Calon (tutup pertama keadaan lain pada 22 Okt), 54 saham: Neutral→Bullish 19, Bullish→Neutral 15, Bearish→Neutral 12, Neutral→Bearish 8 — [AN]
- Titik mula: dari 252 saham Bullish/Bearish (semuanya `tepat`), hanya **1** sudah ditembusi (MSM, 22 Okt) — [AN; T3]
  - Bullish: median titik terletak 54 sesi sebelum sah (p25–p75 30–60), dan harga pada sah median +18.7% di atasnya (13.1% hingga 32.0%).
  - Bearish: median 45 sesi sebelum sah (24–56), dan harga pada sah −20.6% (−26.9% hingga −15.6%) di bawahnya.
  - Sumber: [SP/ringkasan.csv, dikira dalam sesi ini]
- Data basi: 63 saham dengan bar terakhir 21 Okt, contohnya ABM, ACA, AGCO, AGX, AORT, ATO, AVY, COR dan CRC — [T3]

**Jadual wakil (19 saham sebenar)** — [SP/jadual_wakil.md]

Petunjuk lajur:
- Sumber: P1/P2/W seperti di atas.
- Sebab: kod pada tutup pertama (C50 = tutup lawan SMA50; 50_150 = SMA50 lawan SMA150; 150_200 = SMA150 lawan SMA200).
- Susunan: tanda C−S50 / S50−S150 / S150−S200 dengan jarak % pada 22 Okt.

| Saham | Sumber | Status | Umur | Sejak (tutup ke-2) | % sejak | Sebelum | Sebab | Titik mula | % dari titik | ATR14% | Susunan [jarak %] | Tutup 22 Okt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| VRTX | P2+P1+W | Bullish baharu | 1 | 22 Okt 2026 | +0.0 | Neutral | C50 | 4 Ogo 2026 @ 465.51 | +15.0 | 2.56 | +++ [2.41, 8.95, 0.52] | sama |
| EMR | P2+P1+W | Bullish baharu | 1 | 22 Okt 2026 | +0.0 | Neutral | 150_200 | 16 Sep 2026 @ 144.40 | +11.0 | 2.64 | +++ [2.5, 7.15, 0.15] | sama |
| RIGL | P2+P1 | Bullish baharu | 7 | 14 Okt 2026 | +4.4 | Neutral | 150_200 | 24 Jul 2026 @ 35.01 | +39.6 | 3.77 | +++ [4.22, 24.19, 2.36] | sama |
| MSM | P2 | Bullish baharu | 18 | 29 Sep 2026 | −9.7 | Neutral | C50 | 2 Sep 2026 @ 115.73, **ditembusi 22 Okt** | −2.9 | 3.98 | −++ [−8.92, 8.2, 6.04] | Neutral (tutup pertama) |
| JCI | P2+P1 | Bullish | 23 | 22 Sep 2026 | −2.4 | Neutral | C50 | 14 Sep 2026 @ 135.41 | +5.6 | 3.35 | −++ [−2.64, 2.75, 2.65] | Neutral (tutup pertama) |
| ASC | P2+P1 | Bullish | 60 | 30 Jul 2026 | +17.5 | Neutral | C50 | 1 Jul 2026 @ 13.19 | +46.6 | 4.53 | +++ [5.64, 10.64, 6.12] | sama |
| PSX | P2+P1 | Bullish lama | 79 | 2 Jul 2026 | +62.2 | Neutral | C50 | 17 Apr 2026 @ 151.67 | +87.7 | 3.21 | +++ [8.88, 26.04, 7.26] | sama |
| MATX | P2+P1 | Bullish lama | 142 | 1 Apr 2026 | +38.5 | Neutral | C50 | 2 Jan 2026 @ 121.61 | +87.1 | 3.10 | +++ [0.38, 12.82, 5.95] | sama |
| HBB | P2+P1+W | Neutral | 1 | 22 Okt 2026 | +0.0 | Bullish | C50 | – | – | 4.81 | −++ [−0.44, 33.75, 7.37] | sama |
| NEM | P2+P1+W | Neutral | 20 | 25 Sep 2026 | −6.0 | Bullish | 150_200 | – | – | 3.21 | −+− [−6.23, 10.35, −1.61] | sama |
| CTAS | P2+P1+W | Neutral | 79 | 2 Jul 2026 | +23.9 | Bearish | C50 | – | – | 1.74 | ++− [10.79, 8.06, −0.87] | sama |
| VSNT | P1 | Neutral (tersensor) | ≥ 15 | tidak diketahui | +4.4 | tidak diketahui | – | – | – | 2.49 | −−+ [−8.22, −4.99, 3.66] | sama |
| AGCO | P2+P1 | Bearish baharu | 10 | 8 Okt 2026 | −2.7 | Neutral | C50 | 4 Sep 2026 @ 135.17 | −22.2 | 3.68 | −−− [−7.1, −0.64, −1.79] | **data 21 Okt** |
| PRIM | P2 | Bearish baharu | 5 | 16 Okt 2026 | −8.6 | Neutral | C50 | 5 Ogo 2026 @ 92.15 | −27.4 | 6.85 | −−− [−12.44, −26.84, −9.36] | sama |
| DHI | P2 | Bearish | 32 | 9 Sep 2026 | +6.3 | Neutral | 50_150 | 25 Jun 2026 @ 170.28 | −13.3 | 2.99 | +−− [4.64, −2.97, −1.24] | Neutral (tutup pertama) |
| ROL | P2+P1+W | **Bearish lama** | 86 | 23 Jun 2026 | −20.5 | Neutral | 150_200 | 23 Apr 2026 @ 56.97 | −38.0 | 3.07 | +−− [4.62, −21.92, −8.81] | Neutral (tutup pertama) |
| TTD | P2+W | **Bearish lama** | 116 | 8 Mei 2026 | −43.0 | Neutral | C50 | 5 Mac 2026 @ 32.90 | −60.0 | 3.91 | −−− [−0.43, −26.51, −13.56] | sama |
| HQ | P1 | Tiada status (150 bar sejak 20 Mac 2026) | – | – | – | – | – | – | – | 8.74 | – | – |
| BRZE | P2+P1 | (dikira: Bullish baharu 10, +57.8%) → **Diambil alih** | 10 | 9 Okt 2026 | +57.8 | Neutral | 150_200 | 23 Jul 2026 @ 20.93 | +119.1 | 5.04 | +++ [56.76, 16.37, 4.22] | sama |

- BRZE tersenarai dalam `data/ambil_alih.csv` (diumumkan 2026-10-20, Salesforce, tunai) dan melonjak +51.7% pada 20 Okt — [data/ambil_alih.csv](/home/user/papertrade-claude/BacktestShariah2/data/ambil_alih.csv); [T3 semakan lompatan]

### Inferences
- Bullish baharu mendominasi Bullish (117/179) kerana larian status pendek (median 12 sesi antara pertukaran, semua status; §4). Sub-label "baharu" akan kerap muncul; ia deskriptif, bukan isyarat.
- Saham watchlist lebih kerap Bullish (36.7%) berbanding P1 (30.2%), konsisten dengan imbasan kaedah yang memilih saham kuat. Ini pemerhatian satu hari sahaja.
- CTAS (Neutral 79 sesi dari Bearish, harga +23.9%, C 10.8% atas SMA50) menunjukkan kelemahan D10: selepas kejatuhan panjang, SMA150 kekal di bawah SMA200 lama selepas harga pulih. Sebab itu "dari Bearish" dan umur perlu dipaparkan.
- AGCO dan 62 saham lain berstatus berdasarkan bar 21 Okt. Paparan mesti menunjukkan "data 21 Okt" supaya status lewat sehari tidak disangka semasa.

### Gaps
- Taburan ialah gambaran satu hari (22 Okt 2026) dan tidak mewakili kitaran pasaran lain.
- Punca 95 ticker tiada bar 22 Okt dalam `terkini.csv` tidak disiasat; mungkin lewat kemas kini atau tiada sebut harga.

## 3. Garis masa terperinci: tarikh silang C/SMA50/SMA150/SMA200 dan perubahan status

### Takeaway
Enam kes sebenar menunjukkan semua corak penting:
- **Bullish segar** (VRTX): sah 22 Okt, tetapi SMA150 hanya +0.52% di atas SMA200.
- **Bullish lama** (MATX): 142 sesi tanpa satu pun silang selepas 1 Apr, kini C hanya +0.38% di atas SMA50.
- **Neutral dari Bullish** (NEM): Bullish hilang selepas 7 sesi kerana SMA150 jatuh 0.05% bawah SMA200, walaupun C masih 5.7% di atas SMA50.
- **Bearish lama** (TTD): dua lintasan satu hari ke atas SMA50 ditapis oleh H2.
- **Whipsaw** (JCI): 20 pertukaran dalam 2026.
- **Hari jurang besar** (PRIM): −50.1% sehari; status bertukar ke Neutral sesi berikutnya, dan Bearish hanya 73 sesi kemudian.

### Cited Findings
**A. VRTX: Bullish segar (P1+P2+W)** — [G-VRTX; T3]

| Tarikh | Peristiwa | C | SMA50 | SMA150 | SMA200 | Status selepas |
|---|---|---|---|---|---|---|
| 7 Jan 2026 | SMA50 naik atas SMA200 | 484.15 | – | – | – | – |
| 27 Mac – 11 Jun | C melintasi SMA150/SMA200 berulang kali (≥ 20 silang); SMA50 bawah SMA200 5 Jun, naik semula 29 Jun | – | – | – | – | Neutral |
| 15 Jul | SMA50 naik atas SMA150 → mentah Bullish | 477.08 | – | – | – | Neutral (tutup pertama) |
| 16 Jul | tutup kedua | 486.03 | – | – | – | **Bullish** |
| 18 Sep | C jatuh bawah SMA50 | 508.34 | 510.60 | 473.82 | 470.15 | Bullish (tutup pertama Neutral) |
| 21 Sep | tutup kedua | 510.72 | 511.10 | 473.95 | 470.54 | **Neutral** |
| 22 Sep | C naik atas SMA50 | 514.99 | 511.80 | 474.20 | 470.80 | Neutral |
| 23 Sep | tutup kedua | 516.34 | 512.60 | 474.51 | 471.10 | **Bullish** |
| 1 Okt | C jatuh bawah SMA50 | 506.74 | 517.57 | 476.20 | 473.37 | Bullish |
| 2 Okt | tutup kedua | 504.73 | 518.20 | 476.26 | 473.62 | **Neutral** |
| 21 Okt | C naik atas SMA50 | 524.52 | 522.37 | 479.12 | 476.84 | Neutral |
| 22 Okt | tutup kedua | 535.17 | 522.56 | 479.63 | 477.17 | **Bullish baharu, 1 sesi** |

- Titik mula 4 Ogo @ 465.51 (56 sesi sebelum sah), harga +15.0%. ATR 2.56%. Tujuh pertukaran dalam 1.27 tahun liputan — [T3]

**B. MATX: Bullish lama (P1+P2)** — [G-MATX; T3]

| Tarikh | Peristiwa | C | SMA50 | SMA150 | SMA200 | Status selepas |
|---|---|---|---|---|---|---|
| 5 Nov 2025 | C naik atas SMA50 | 108.79 | – | – | – | (SMA200 belum wujud; stor bermula 17 Apr 2025) |
| 25 Nov 2025 | C naik atas SMA150 | 108.53 | – | – | – | – |
| 22 Dis 2025 | SMA50 naik atas SMA150 | 122.38 | – | – | – | – |
| 4 Feb 2026 | status pertama diketahui | 161.95 | – | – | – | Bullish (tersensor) |
| 12 Mac | C bawah SMA50 | 148.67 | 152.88 | 121.07 | 118.22 | Bullish |
| 13 Mac | tutup kedua | 149.17 | 153.39 | 121.34 | 118.42 | **Neutral** |
| 18 Mac | C atas SMA50 | 155.50 | 155.18 | 122.30 | 119.06 | Neutral |
| 19 Mac | tutup kedua | 157.56 | 155.76 | 122.63 | 119.30 | **Bullish** |
| 20 Mac → 23 Mac | bawah SMA50 satu tutup (154.48), kemudian atas (159.33) | – | – | – | – | Bullish (ditapis H2) |
| 27 Mac | C bawah SMA50 | 157.43 | 159.29 | 124.90 | 120.74 | Bullish |
| 30 Mac | tutup kedua | 156.76 | 159.53 | 125.24 | 120.96 | **Neutral** |
| 31 Mac | C atas SMA50 | 163.32 | 159.89 | 125.64 | 121.21 | Neutral |
| 1 Apr | tutup kedua | 164.28 | 160.30 | 126.05 | 121.48 | **Bullish** |
| 1 Apr – 22 Okt | tiada silang langsung bagi mana-mana pasangan | – | – | – | – | Bullish |
| 22 Okt | – | 227.48 | 226.61 | 200.85 | 189.58 | **Bullish lama, 142 sesi, +38.5%** |

- Titik mula 2 Jan 2026 @ 121.61, 61 sesi sebelum sah. Harga pada sah +35.1% di atasnya, kini +87.1%. ATR 3.10%. Empat pertukaran dalam 0.71 tahun liputan — [T3]

**C. NEM: Neutral dari Bullish (P1+P2+W)** — [G-NEM; T3]

| Tarikh | Peristiwa | C | SMA50 | SMA150 | SMA200 | Status selepas |
|---|---|---|---|---|---|---|
| 5 Mac – 18 Mei 2026 | 9 pertukaran Bullish↔Neutral di sekitar SMA50 (whipsaw) | – | – | – | – | Neutral (18 Mei) |
| 5 Jun | C jatuh bawah SMA150 dan SMA200 | 99.50 | – | – | – | Neutral |
| 25 Jun / 16 Jul | SMA50 jatuh bawah SMA150 / bawah SMA200 | 95.15 / 90.64 | – | – | – | Neutral |
| 5 Ogo | C naik atas SMA50 dan SMA200; 7 Ogo atas SMA150 | 104.07 | – | – | – | Neutral |
| 10 Sep | SMA50 naik atas SMA200 | 126.14 | – | – | – | Neutral |
| 15 Sep | SMA50 naik atas SMA150 → mentah Bullish | 124.19 | 110.63 | 110.35 | 109.27 | Neutral |
| 16 Sep | tutup kedua | 121.76 | 111.17 | 110.36 | 109.43 | **Bullish** |
| 24 Sep | **SMA150 jatuh bawah SMA200** (110.40 < 110.45) → mentah Neutral; C masih 5.7% atas SMA50 | 121.30 | 114.73 | 110.40 | 110.45 | Bullish |
| 25 Sep | tutup kedua | 121.43 | 115.34 | 110.40 | 110.61 | **Neutral (dari Bullish)** |
| 30 Sep / 14 Okt / 15 Okt | C bawah SMA50 / bawah SMA200 / atas SMA200 semula | 115.34 / 111.56 / 115.79 | – | – | – | Neutral |
| 22 Okt | – | 114.11 | 121.69 | 110.28 | 112.09 | **Neutral, 20 sesi, −6.0%** |

- Ringkasan: 15 pertukaran dalam 1.27 tahun liputan. ATR 3.21%. Sebab kehilangan Bullish ialah `150_200`, bukan harga — [T3]

**D. TTD: Bearish lama (P2+W)** — [G-TTD; T3]

| Tarikh | Peristiwa | C | SMA50 | SMA150 | SMA200 | Status selepas |
|---|---|---|---|---|---|---|
| 16 Jul 2025 | status pertama diketahui | 81.13 | – | – | – | Neutral (tersensor) |
| 8 Ogo → 11 Ogo 2025 | C bawah SMA50 dan SMA150 → disahkan | 54.23 → 53.18 | – | – | – | **Bearish** |
| Sep – Dis 2025 | 6 pertukaran lagi (silang SMA50/SMA150 dan SMA150/SMA200); 24 Dis SMA150 bawah SMA200 → 26 Dis | 38.12 → 38.31 | – | – | – | **Bearish** |
| 29 Apr → 30 Apr 2026 | atas SMA50 satu tutup (24.37), kemudian bawah (23.59) | – | – | – | – | Bearish (ditapis) |
| 1 Mei → 4 Mei | atas SMA50 dua tutup | 24.24 → 24.10 | 23.82 → 23.80 | 34.92 → 34.76 | 41.59 → 41.31 | **Neutral** |
| 7 Mei | C bawah SMA50 | 23.49 | 23.76 | 34.26 | 40.46 | Neutral |
| 8 Mei | tutup kedua | 23.08 | 23.74 | 34.07 | 40.15 | **Bearish** |
| 1 Jun → 2 Jun | atas SMA50 satu tutup (23.22), kemudian bawah (21.10) | – | – | – | – | Bearish (ditapis) |
| 4 Ogo → 5 Ogo | atas SMA50 satu tutup (19.34), kemudian bawah (18.96) | – | – | – | – | Bearish (ditapis) |
| 22 Okt | – | 13.16 | 13.22 | 17.98 | 20.81 | **Bearish lama, 116 sesi, −43.0%, amaran** |

- Titik mula 5 Mac @ 32.90, 45 sesi sebelum sah. Harga pada sah −29.8%, kini −60.0%. ATR 3.91%. C kini hanya −0.43% bawah SMA50 — [T3]
- Larian semasa didahului jeda Neutral 4–7 Mei. Jika jeda itu disambung, Bearish bermula 26 Dis 2025, iaitu 207 sesi — [T2 senarai "jambatan"]

**E. JCI: whipsaw (P1+P2)** — [G-JCI; T3; AN]
- Sebanyak **32 pertukaran dalam 1.27 tahun** (25.2 setahun; tertinggi dalam alam bersama SILC), dengan 19 corak X→Y(≤ 5 sesi)→X. Dua puluh pertukaran berlaku dalam 2026, dan 13 daripadanya sejak 1 Jun.

| Pertukaran sejak 1 Jun 2026 (tarikh sah) | Arah |
|---|---|
| 3 Jun, 1 Jul, 13 Jul, 22 Jul, 31 Jul, 8 Sep, 22 Sep | Neutral → Bullish |
| 29 Jun, 8 Jul, 17 Jul, 29 Jul, 20 Ogo, 15 Sep | Bullish → Neutral |

- Contoh nilai pertukaran:
  - 14 Sep: C 137.38 < SMA50 144.31 dan < SMA150 140.70 → 15 Sep **Neutral** (137.90).
  - 21 Sep: C 145.18 > SMA50 144.34 → 22 Sep **Bullish** (146.44; SMA150 140.84; SMA200 135.51).
  - Lintasan satu tutup bawah SMA50 pada 16 Okt (145.47) dan atas semula pada 19 Okt (148.22) ditapis.
  - Pada 22 Okt, C 143.00 < SMA50 146.88 (−5.3% sehari) menjadi **tutup pertama Neutral**. Papan masih Bullish 23 sesi (−2.4%).
  - ATR 3.35%. Jarak SMA50/SMA150 dan SMA150/SMA200 masing-masing hanya 2.75% dan 2.65%.

**F. PRIM: hari jurang besar (P2)** — [G-PRIM; T3; SP/jurang.csv; bar stor]

| Tarikh | Peristiwa | Buka | C | SMA50 | SMA150 | SMA200 | Status selepas |
|---|---|---|---|---|---|---|---|
| 7 → 8 Apr 2026 | C atas SMA50, disahkan | – | 148.67 → 156.29 | – | – | – | **Bullish** |
| 5 Mei | – | 194.36 | 202.54 | – | – | – | Bullish |
| 6 Mei | **jurang −36.7%, hari −50.1%**, volum 13.17 juta (5 Mei: 2.40 juta); C bawah ketiga-tiga SMA → mentah Neutral | 128.15 | 101.04 | 152.45 | 142.18 | 134.92 | Bullish (tutup pertama) |
| 7 Mei | tutup kedua | 101.87 | 107.78 | 151.54 | 141.97 | 135.02 | **Neutral** |
| 15 / 17 Jun | SMA50 bawah SMA150 / bawah SMA200 | – | 101.15 / 101.47 | – | – | – | Neutral |
| 23 Jun | jurang −38.8%, hari −21.6% | 66.12 | 84.79 | – | – | – | Neutral (tiada perubahan) |
| 19 Ogo | SMA150 bawah SMA200 → mentah Bearish | – | 79.84 | 89.05 | 126.58 | 126.62 | Neutral |
| 20 Ogo | tutup kedua (73 sesi selepas 6 Mei) | – | 79.15 | 88.56 | 126.19 | 126.31 | **Bearish** |
| 2 → 5 Okt | C atas SMA50, disahkan | – | 79.08 → 80.57 | 77.92 → 77.80 | – | – | **Neutral** |
| 15 → 16 Okt | C bawah SMA50, disahkan | – | 73.75 → 73.21 | 77.40 → 77.26 | – | – | **Bearish** |
| 22 Okt | – | – | 66.94 | 76.45 | 104.50 | 115.28 | **Bearish baharu, 5 sesi, −8.6%** |

- Tutup 4–8 Mei dalam dataset backtest S1–S4 sama dengan stor (185.1977, 202.5347, 101.0378, 107.7750, 104.6010). Data ini konsisten antara dua sumber repo, tetapi punca berita tidak disemak — [bar dataset S1–S4]
- Titik mula 5 Ogo @ 92.15 (51 sesi sebelum sah). Harga pada sah −20.6%, kini −27.4%. ATR 6.85% — [T3]

### Inferences
- Tiga daripada enam kes sedang berada di ambang: MATX (C +0.38% atas SMA50), TTD (−0.43% bawah SMA50) dan VRTX (SMA150 +0.52% atas SMA200). Satu tutup biasa (ATR 3–4%) cukup untuk mencetus tutup pertama. Kesimpulannya, Bullish lama tidak bermakna "jauh dari kehilangan status".
- H2 benar-benar menapis lintasan satu hari: MATX 20–23 Mac, TTD 29–30 Apr, 1–2 Jun dan 4–5 Ogo, JCI 16–19 Okt. Namun ia tidak menghalang whipsaw dua hari (JCI, NEM).
- PRIM menunjukkan label struktur MA tidak sesuai menandakan kejatuhan mengejut. Selepas −50% sehari, label hanya menjadi Neutral (sesi berikutnya), dan Bearish penuh tiba 73 sesi kemudian. Risiko kejatuhan seperti ini terpapar melalui ATR14% (6.85% sekarang), bukan label.

### Gaps
- Garis masa hanya meliputi tetingkap stor. Tarikh silang sebelum ~Apr 2025 (MATX) atau sebelum SMA200 wujud tidak dapat ditentukan, jadi "tiada data".
- Punca peristiwa PRIM 6 Mei dan 23 Jun (berita atau earnings) tidak disahkan dalam sesi ini.

## 4. Kes tepi: kekerapan tukar, whipsaw, hari jurang, sejarah pendek, data bermasalah

### Takeaway
Dengan H2, saham alam bertukar status median **8.4 kali setahun** (p10–p90 4.2–14.0). Sebanyak **30%** larian status berakhir dalam ≤ 5 sesi, dan whipsaw X→Y→X berlaku 2.34 kali bagi setiap saham setahun. H1 (tanpa pengesahan) hampir menggandakan bilangan pertukaran (median 14.1), manakala H3 hanya mengurangkannya kepada 6.3. Kira-kira 93% kehilangan Bullish dan 92% kehilangan Bearish dicetus oleh tutup melintasi SMA50. Pada hari jurang ≥ 10%, status tidak pernah bertukar pada hari jurang itu sendiri kecuali jika hari itu tutup kedua; kelewatan tepat satu sesi.

### Cited Findings
**Kekerapan pertukaran**
- H2, 697 saham dengan liputan ≥ 0.25 tahun: median 8.4 setahun, purata 8.69, p10–p90 4.2–14.0, maksimum 25.2 (JCI 32 pertukaran/1.27 tahun; SILC 18/0.71). Seterusnya NPO dan ASND 21.0; ITT, ZWS, WWW, RPM, PPIH dan MSM ≈ 18.2 — [AN]
- Saham ≥ 260 bar: H1 median 14.1 (purata 15.0), larian ≤ 5 sesi 57%; **H2 8.4 (8.7), 30%**; H3 6.3 (6.8), 17% — [T2]
- Panjang larian antara pertukaran (H2): median 12 sesi, p10 2. Daripada 5,438 larian, 1,658 (30%) ≤ 5 sesi dan 2,558 (47%) ≤ 10 sesi — [AN]
- Tutup pertama yang disahkan esok: 6,132/8,299 (74%). Mengikut arah: Bearish→Neutral 75%, Neutral→Bearish 73%, Neutral→Bullish 76%, Bullish→Neutral 72% — [AN]

**Whipsaw (X → Y bertahan ≤ 5 sesi → X)**
- 1,656 corak dalam 707.1 saham-tahun = **2.34 setiap saham setahun**: Bullish→Neutral→Bullish 562, Neutral→Bullish→Neutral 557, Neutral→Bearish→Neutral 312, Bearish→Neutral→Bearish 225. Sebanyak 148 daripada 700 saham tiada whipsaw. Terbanyak: JCI 19, SILC 12, ARLO 12, ADBE 10, TT 10, NPO 10, BIIB 9, LAUR 9 — [T1]
- Contoh daripada data:
  - SSNC: Neutral 19 Dis 2025 → Bullish 23 Dis 2025 (2 sesi);
  - PR: Neutral 7 Jan 2026 → Bullish 9 Jan 2026 (2 sesi);
  - CTAS: Bearish 5 Jan 2026 → Neutral 7 Jan 2026 (2 sesi);
  - MTDR: Bullish 22 Jul 2026 → Neutral 24 Jul 2026 (2 sesi).
  - Sumber: [AN]
- Larian semasa yang didahului jeda ≤ 5 sesi daripada keadaan sama: Bullish 31 (14 akan bertukar sub-label jika disambung), Bearish 9 (7), Neutral 124 (43). Contoh: TTD 116 → 207 sesi; DINO Bullish 83 → 163 sesi — [T2]

**Sebab pertukaran (syarat pada tutup pertama, 6,132 pertukaran)** — [T2]

| Pertukaran | C/SMA50 sahaja | SMA150/SMA200 | SMA50/SMA150 | Gabungan | Jumlah |
|---|---|---|---|---|---|
| Bullish → Neutral | 1,901 (92.8%) | 70 | 57 | 21 | 2,049 |
| Neutral → Bullish | 1,508 (74.3%) | 314 (15.5%) | 190 (9.4%) | 17 | 2,029 |
| Neutral → Bearish | 710 (70.1%) | 175 (17.3%) | 120 (11.8%) | 8 | 1,013 |
| Bearish → Neutral | 952 (91.5%) | 42 | 38 | 9 | 1,041 |

- Hari ini, `sebab` bagi status semasa: C50 563, 150_200 72, 50_150 53, gabungan 7, tiada 6 (tersensor/tiada status) — [SP/trend_doc.json]

**Hari jurang besar (|buka ÷ tutup semalam − 1| ≥ 10%, 120 sesi terakhir)**
- Terdapat 320 jurang (131 turun, 189 naik). Jadual di bawah meliputi 314 jurang yang ada data hari berikutnya — [AN; T1]

| Jurang | Status sebelum | n | Mentah berubah pada hari jurang | Status berubah pada hari jurang | Status berubah selewat-lewatnya esok |
|---|---|---|---|---|---|
| Naik | Bearish | 11 | 10 (semua → Neutral) | 1 | 10 |
| Naik | Neutral | 121 | 17 (→ Bullish) | 2 | 16 |
| Naik | Bullish | 57 | 1 | 0 | 0 |
| Turun | Bearish | 14 | 0 | 0 | 0 |
| Turun | Neutral | 79 | 15 (14 → Bearish, 1 → Bullish) | 4 | 15 |
| Turun | Bullish | 32 | 15 (→ Neutral) | 1 | 14 |

- Jurang terbesar dalam alam: PRIM 23 Jun −38.8% dan 6 Mei −36.7%, ZUMZ 5 Jun −35.7%, PSIX 12 Mei −34.2%, GLUE 31 Jul −31.8%. Jurang naik terbesar: BRZE 20 Okt +51.6% (ambil alih), AAON 7 Mei +45.5%, AXTI 31 Jul +42.1% — [AN]
- MSM pada 22 Okt jatuh −15.4% dengan jurang −5.1%; volum 2.40 juta lawan purata 20 hari 0.87 juta (SST `relativeVolume` 3.03; `volumeSurge` true). Ia menjadi tutup pertama Neutral, dan titik mula ditembusi — [SP/sst_banding_out2.txt; SST]

**Sejarah pendek (IPO, spin-off, ticker baharu)**
- n_bar dalam alam: minimum 150, p5 380, median 521. Hanya 1 saham < 201 bar (HQ, 150 bar sejak 20 Mac 2026 → Tiada status) dan 4 saham < 260 bar — [T3]
- Selain HQ, saham sejarah pendek yang tersensor ialah VSNT (215 bar sejak 15 Dis 2025, ≥ 15 sesi Neutral), PARK (223 bar sejak 3 Dis 2025, ≥ 22) dan ELVR (287 bar sejak 2 Sep 2025, ≥ 86). BLLN (241 bar sejak 6 Nov 2025) sudah mempunyai pertukaran disahkan — [T3; bar pertama stor]

**Data bermasalah**
- Lompatan > 40% sehari dalam 60 sesi, ditanda `semak data`:
  - BRZE: +51.7% pada 20 Okt; diambil alih.
  - SVRN: +41.5% pada 21 Okt; ATR 24.08%; % sejak Neutral +314.7%.
  - IOVA: +43.1% pada 6 Ogo.
  - TANH: +181.8% pada 22 Okt; ATR 14.50%; Bearish dengan % sejak +66.2%.
  - OESX: +54.4% pada 5 Ogo.
  - Sumber: [AN; semakan lompatan dalam sesi ini; T3]
- Hari tanpa bar (gantung dagangan) tidak wujud dalam siri. SMA dan umur dikira atas bar saham itu sendiri. Saham tanpa bar ≥ 10 sesi ditutup oleh `kod/tidak_layak.py posisi` (sebab_keluar `delist`) — [CLAUDE.md; SP/trend.py]

### Inferences
- **Jangan tambah tutup ketiga.** H3 hanya mengurangkan pertukaran dari 8.4 kepada 6.3 setahun dengan kelewatan sesi tambahan, dan LAP tidak menguji pemisahan H3. H2 kekal sebagai titik imbang yang diuji.
- **Whipsaw tidak boleh dihapuskan tanpa mengubah takrif yang diuji.** Paparan yang jujur ialah menunjukkan umur kecil ("1 sesi", "baharu"), dan bagi posisi, menyatakan dalam tooltip berapa kali status bertukar dalam 60 sesi terakhir (pilihan; medan belum dibina).
- Pada hari jurang turun dari Bullish, papan masih memaparkan Bullish pada hari itu. ATR14% di sebelah pill dan baris tooltip "Tutup [tarikh] sudah Neutral" ialah cara memberitahu tanpa melanggar peraturan pengesahan.
- Saham diambil alih (BRZE) dan saham ber-`semak data` (TANH, SVRN) menghasilkan status yang mengelirukan. Status saham diambil alih mesti digantikan dengan label "Diambil alih". Lompatan > 40% pula perlu tanda "semak data" dalam tooltip. Tanda ini tidak boleh mengubah status, kerana sebahagian lompatan itu sebenar.

### Gaps
- Kesahihan lompatan TANH +181.8% dan SVRN tidak dapat disahkan dengan sumber luar dalam sesi ini, kerana kedua-dua saham tidak disemak dengan Moomoo atau SST.
- Kekerapan pertukaran diukur atas ~1.27 tahun liputan (2025–2026) sahaja, rejim yang kebanyakannya pasaran naik.

## 5. Perbandingan dengan label SST Terminal

### Takeaway
Bagi 10 saham alam yang ada dalam SST, label SST dapat dihasilkan semula 10/10 dengan peraturan yang dinyahkod dalam [PENG] (kumulatif 33/33 pemerhatian). Label papan "sepadan" dengan SST bagi 6/10 saham. Tiga beza ialah kelewatan pengesahan 2 tutup pada hari yang sama (JCI, MSM, ROL bertukar mentah pada 22 Okt). Satu lagi beza struktur: CTAS ialah Uptrend dalam SST tetapi Neutral di papan kerana SMA150 < SMA200. Harga tutup sama tepat. SMA50 hampir sama, manakala SMA200 SST lebih tinggi 0.2–0.7% bagi saham yang membayar dividen. Ini konsisten dengan stor repo yang dilaras dividen.

### Cited Findings
- Kesegaran SST: lapisan `technicals` dikemas kini 2026-10-23 03:45 UTC. PRIM, BLDR, ARQT dan HBB memulangkan "Stock not found" — [SST `get_data_freshness`, `technical_analysis`]

| Saham | Papan (D10+H2) | Susunan papan | SST `trend` | `trendTemplate` | C lawan SMA50 / SMA200 (SST, %) | Sepadan? | Sebab beza |
|---|---|---|---|---|---|---|---|
| MATX | Bullish lama (142) | +++ | Uptrend | true | +0.38 / +19.74 | ya | – |
| PSX | Bullish lama (79) | +++ | Uptrend | true | +8.85 / +46.14 | ya | – |
| EMR | Bullish baharu (1) | +++ | Uptrend | true | +2.49 / +9.47 | ya | – |
| VRTX | Bullish baharu (1) | +++ | Constructive | false | +2.41 / +12.15 | ya (Constructive ⊃ C > SMA50 dan SMA200) | templat SST gagal walaupun syarat Minervini yang kelihatan lulus (lihat bawah) |
| NEM | Neutral (20, dari Bullish) | −+− | Neutral | false | −6.29 / +1.48 | ya | – |
| TTD | Bearish lama (116) | −−− | Downtrend | false | −0.43 / −36.75 | ya | – |
| JCI | Bullish (23; tutup pertama Neutral 22 Okt) | −++ | Neutral | false | −2.78 / +2.22 | tidak | papan menunggu tutup kedua |
| MSM | Bullish baharu (18; tutup pertama Neutral) | −++ | Neutral | false | −8.92 / +3.79 | tidak | sama; −15.4% pada 22 Okt |
| ROL | Bearish lama (86; tutup pertama Neutral) | +−− | Neutral | false | +4.62 / −25.98 | tidak | sama; +5.6% pada 22 Okt |
| CTAS | Neutral (79, dari Bearish) | ++− | Uptrend | true | +10.79 / +18.27 | tidak | struktur: SMA150 −0.87% bawah SMA200 (data repo), tetapi templat SST true |

Sumber jadual: [SST; SP/sst_banding_out.txt]

- Peraturan SST daripada [PENG] menghasilkan label SST yang sama bagi kesemua 10 saham, sama ada dikira atas nilai SST atau atas nilai repo — [SP/sst_banding_out.txt]
  - Uptrend ⇔ `trendTemplate` true;
  - Constructive ⇔ C > SMA50 dan C > SMA200 tetapi templat gagal;
  - Neutral ⇔ di antara;
  - Downtrend ⇔ C < SMA50 dan C < SMA200.
- Beza nilai (SST ÷ repo − 1):
  - tutup 0.00% bagi semua 10;
  - SMA50 0.00–0.14%;
  - SMA200 0.00% bagi VRTX dan TTD; +0.21% MATX; +0.32% NEM; +0.34% CTAS; +0.45% JCI; +0.48% EMR; +0.64% ROL; +0.68% MSM; +0.73% PSX.
  - Sumber: [SP/sst_banding_out.txt]
- VRTX atas data repo memenuhi semua syarat Minervini yang boleh disemak, tetapi `trendTemplate` SST = false — [SP/sst_banding_out2.txt; SST]
  - C > SMA150 > SMA200, dengan SMA50 di atas kedua-duanya;
  - SMA200 naik 107 sesi berturut (+1.29% dalam 21 sesi);
  - +30.7% atas tutup terendah 52 minggu (+32.7% atas rendah intrahari);
  - −4% dari tinggi 52 minggu;
  - RS SST 78.46.
- CTAS ialah sebaliknya: SMA150 (187.13) < SMA200 (188.78) dalam data repo, tetapi `trendTemplate` SST = true. SST tidak memaparkan SMA150 — [SP/sst_banding_out.txt; SST]
- Contoh dari [PENG] yang konsisten: INTC dan LRCX = Downtrend SST (C bawah SMA50 dan SMA200, tetapi SMA50 > SMA200) dan akan menjadi Neutral di papan — [PENG]

### Inferences
- Beza SMA200 hanya pada saham berdividen, dan saiznya sepadan dengan magnitud laras dividen ~1 tahun. Ini menunjukkan SST memakai harga laras pecahan sahaja, manakala stor repo dilaras dividen sebelum ~2 Okt 2026. Kesannya kecil, tetapi boleh mengubah label apabila SMA150 dan SMA200 hampir sama (VRTX +0.52%, EMR +0.15%).
- Tiga beza utama papan lawan SST ialah reka bentuk, bukan ralat:
  - SST bertindak pada tutup yang sama, manakala papan menunggu tutup kedua;
  - SST hanya melihat kedudukan harga berbanding SMA50/SMA200, manakala papan memerlukan susunan penuh termasuk SMA150 > SMA200;
  - Downtrend SST (C bawah dua MA) lebih longgar daripada Bearish papan (susunan terbalik penuh).
- Templat SST bukan templat Minervini 8 syarat yang setia: VRTX dan PFE gagal walaupun lulus, CTAS lulus walaupun SMA150 < SMA200. Oleh itu label SST tidak sesuai dijadikan rujukan kebenaran atau pengganti papan.

### Gaps
- Komponen tepat `trendTemplate` SST tidak diketahui, dan SST tidak mendokumenkannya.
- Hanya 10 saham alam dibanding pada satu hari, dan 4 saham alam tiada dalam SST.

## 6. Peraturan paparan: teks pill, tooltip, warna, larangan dan penerangan ringkas

### Takeaway
Pill memaparkan satu daripada 9 teks tetap: Bullish/Bearish dengan sub-label baharu atau lama, Neutral tanpa sub-label, Tiada status dan Diambil alih. Warna sentiasa dalam bentuk garis (outline), kecuali **Bearish lama** yang diisi penuh merah sebagai satu-satunya amaran. Baris kedua memaparkan umur, tarikh sah, % sejak (atau "dari X" bagi Neutral), titik mula dan ATR14%. Tooltip menerangkan takrif, tarikh tutup pertama dan kedua, sebab pertukaran, serta tutup pertama hari ini jika ada. Teks contoh di bawah dijana terus daripada data oleh `SP/papar.py`.

### Cited Findings
**Teks pill dan warna (dilaksana dalam `papar.py`)** — [SP/papar.py; PAP]

| Keadaan | Teks pill | Warna |
|---|---|---|
| s = 1, umur ≤ 20 | `Bullish baharu` | hijau, garis |
| s = 1, 21–60 | `Bullish` | hijau, garis |
| s = 1, > 60 | `Bullish lama` | hijau, garis |
| s = 0 (semua umur) | `Neutral` | ambar, garis |
| s = −1, ≤ 20 | `Bearish baharu` | merah, garis |
| s = −1, 21–60 | `Bearish` | merah, garis |
| s = −1, > 60 | `Bearish lama` | **merah, isi penuh (amaran)** |
| s = null | `Tiada status` | kelabu |
| saham dalam `data/ambil_alih.csv` (tarikh_umum ≤ tarikh_data) | `Diambil alih` | kelabu |

**Baris kedua (format tepat)** — [PAP]
- Bullish/Bearish: `{umur} sesi · sejak {D Mmm} ({±x.x}%) · titik mula {D Mmm} @ {harga} ({±x}%) · ATR {x.x}%`
- Neutral: `{umur} sesi · sejak {D Mmm} (dari Bullish|Bearish) · ATR {x.x}%`
- Tersensor: `≥ {umur} sesi · sejak sebelum liputan data (tarikh tepat tidak diketahui) · ATR {x.x}%`
- Titik mula ditembusi: `titik mula {D Mmm} @ {harga} ditembusi {D Mmm}`
- Data basi (tarikh_data < tarikh dokumen): tambah ` · data {D Mmm}`
- Bulan: `Jan Feb Mac Apr Mei Jun Jul Ogo Sep Okt Nov Dis`, sama dengan senarai bulan dalam kod `standard/` repo — [grep standard/ dan kod/]
- Contoh sebenar — [PAP]
  - `VRTX [Bullish baharu | hijau] 1 sesi · sejak 22 Okt (+0.0%) · titik mula 4 Ogo @ 465.51 (+15%) · ATR 2.6%`
  - `MSM [Bullish baharu | hijau] 18 sesi · sejak 29 Sep (-9.7%) · titik mula 2 Sep @ 115.73 ditembusi 22 Okt · ATR 4.0%`
  - `NEM [Neutral | ambar] 20 sesi · sejak 25 Sep (dari Bullish) · ATR 3.2%`
  - `CTAS [Neutral | ambar] 79 sesi · sejak 2 Jul (dari Bearish) · ATR 1.7%`
  - `AGCO [Bearish baharu | merah] 10 sesi · sejak 8 Okt (-2.7%) · titik mula 4 Sep @ 135.17 (-22%) · ATR 3.7% · data 21 Okt`
  - `TTD [Bearish lama | merah isi penuh] 116 sesi · sejak 8 Mei (-43.0%) · titik mula 5 Mac @ 32.90 (-60%) · ATR 3.9%`
  - `HQ [Tiada status | kelabu] sejarah < 201 sesi · ATR 8.7%`
  - `BRZE [Diambil alih | kelabu] status trend tidak bermakna (harga terkunci pada tawaran)`

**Tooltip (teks tetap + baris dinamik)** — [SP/papar.py; PAP]
- Teks tetap (semua pill): "Ringkasan susunan purata 50/150/200 hari: Bullish = tutup > SMA50 > SMA150 > SMA200, Bearish = susunan terbalik, Neutral = selain itu; bertukar hanya selepas dua tutup berturut. Dalam ujian 2020–2026 status ini tidak meramal pulangan; Bearish menandakan saham lebih meruap. Bukan isyarat jual; keluar ikut lorong 1/lorong 2."
- Baris pengesahan: "Disahkan pada tutup {D Mmm YYYY} (tutup pertama {D Mmm}); sebab: {frasa}." Frasa daripada `sebab`:
  - C50: "tutup jatuh bawah SMA50" atau "tutup naik atas SMA50";
  - 50_150: "SMA50 jatuh bawah/naik atas SMA150";
  - 150_200: "SMA150 jatuh bawah/naik atas SMA200";
  - gabungan disambung dengan "dan".
- Bearish lama: "Bearish lebih 60 sesi: dalam ujian 2020–2026 kumpulan ini lebih kerap jatuh > 8% dalam 10 sesi berbanding Bearish yang lebih muda. Maklumat risiko, bukan isyarat jual."
- Calon: "Tutup {D Mmm} sudah {Neutral|Bullish|Bearish}; status bertukar jika tutup seterusnya sama." Contoh hari ini: JCI, MSM, ROL dan DHI.
- Nota data: "Nota data: diambil alih (diumum 20261020): status trend tidak bermakna" atau "pergerakan > 40% sehari dalam 60 sesi: semak data".

**Berita (posisi terbuka, pada hari pertukaran disahkan)** — [PAP]
- Hilang: `Hilang Bullish 25 Sep → Neutral; SMA150 jatuh bawah SMA200. Maklumat, bukan isyarat jual; keluar ikut lorong 1/lorong 2.`
- Jadi: `Jadi Bullish 22 Okt (dari Neutral); tutup naik atas SMA50. Maklumat, bukan isyarat jual; keluar ikut lorong 1/lorong 2.` dan `Jadi Bearish 16 Okt (dari Neutral); tutup jatuh bawah SMA50. …`

**Asas bukti bagi pilihan paparan (daripada LAP)** — [LAP](../../reports/Penentuan%20status%20trend%20saham.md)
- Label tidak meramal pulangan: |t| ≤ 1.2 (IS) dan ≤ 1.5 (OOS) bagi 37 takrif.
- Beza risiko Bullish−Bearish hilang selepas kawalan ATR14%.
- Bearish > 60 sesi: +11.3 mata (IS) dan +12.5 mata (OOS) P(jatuh > 8%/10 sesi), dan kekal +3.9/+6.5 selepas kawalan turun naik.
- Bearish ≤ 20 sesi kurang berisiko.
- 43/43 peraturan jual berasaskan status merugikan.
- Bagi kaedah pantulan, Bearish ialah syarat masuk.

**Jangan papar**
- Calon (tutup pertama) sebagai status atau perubahan warna; ia hanya boleh muncul dalam tooltip (74% disahkan, 26% tidak) — [AN]
- Tarikh "sejak" yang tepat bagi saham tersensor; papar "≥ N sesi" — [T3]
- Sub-label "baharu/lama" bagi Neutral (tidak diuji dalam LAP).
- Tarikh atau titik mula yang dikira semula; "Mula naik/Mula turun"; skema 4–5 keadaan; amaran jual atau jualan automatik; kebarangkalian risiko mutlak; skor kekuatan; warna amaran bagi Bearish baharu atau Bearish pada posisi pantulan — [LAP]
- Status trend saham diambil alih — [data/ambil_alih.csv; CLAUDE.md]
- Tarikh tutup pertama (`isyarat`) di baris utama (audit sahaja).

### Inferences
- Gaya garis bagi semua status kecuali Bearish lama memenuhi syarat LAP "jangan warnakan Bearish pada posisi pantulan sebagai amaran" tanpa kes khas bagi kaedah pantulan (`kod/jenis_kaedah.csv`, 15 baris `pantulan`). Satu peraturan warna sudah cukup.
- Neutral tidak diberi % sejak di baris utama kerana arah tiada makna bagi Neutral. Nilai itu tetap disimpan dalam `pct_sejak` untuk tooltip atau analisis.
- Bearish lama hari ini hanya 3/701 saham (0.4%), jadi warna isi penuh akan jarang muncul dan tidak menjadi hingar.
- **Penerangan ringkas (cadangan teks bantuan papan):** "Status trend meringkaskan susunan harga dan tiga purata bergerak (50, 150 dan 200 hari). Bullish bermaksud harga di atas purata 50 hari, dan purata 50 > 150 > 200; Bearish bermaksud sebaliknya; selain itu Neutral. Status hanya bertukar selepas dua hari tutup berturut-turut memberi susunan baharu, supaya pergerakan sehari tidak mengubahnya. 'Sejak' ialah hari tutup kedua itu, dan umur dikira dalam hari dagangan. 'Baharu' bermaksud 20 hari atau kurang; 'lama' bermaksud lebih 60 hari. Titik mula ialah harga terendah (atau tertinggi bagi Bearish) dalam kira-kira tiga bulan sebelum status disahkan, dan tidak berubah selepas itu. Status ini menerangkan keadaan, bukan meramal: dalam ujian 2020–2026 ia tidak meramal pulangan, dan risiko sebenar lebih jelas dilihat pada ATR% di sebelahnya. Satu-satunya amaran ialah Bearish lama, kumpulan yang lebih kerap jatuh tajam. Status bukan isyarat jual; jualan tetap ikut lorong 1 dan lorong 2."

### Gaps
- Kontras warna (hijau, ambar dan merah garis atas latar terang/gelap) belum disemak untuk aksesibiliti.
- Kefahaman pengguna terhadap teks belum diuji.
- Kesan "Neutral lama" dan "Bullish lama" ke atas risiko hanya diuji secara lemah dalam LAP (Bullish > 60: +2.7 mata, t 1.7 IS / 2.5 OOS) dan tidak pernah bagi Neutral. Oleh itu kedua-duanya tidak diberi warna atau teks risiko.
- Medan "bilangan pertukaran dalam 60 sesi" untuk tooltip whipsaw belum dibina atau diuji.
