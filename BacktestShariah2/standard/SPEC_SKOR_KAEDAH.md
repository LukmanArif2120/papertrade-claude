# Pradaftar Skor Kaedah 0–100 (pangkat maklumat semua kaedah)

**Dipradaftar 9 Nov 2026** (keputusan pengguna hari yang sama: "setuju semua cadangan, laksana sekarang"), **sebelum
skor pertama dikira** atas penyebut Lejar lorong 1 LANGSUNG. Pelaksana: `standard/skor_kaedah.py`. Kunci:
`ujian/test_skor_kaedah.py::TestKunci` gagal jika mana-mana berat, sauh atau pemalar di bawah berubah. **Mengubahnya
memerlukan keputusan pengguna DAN pradaftar baharu bertarikh dalam fail ini, sebelum data yang terkesan dilihat.**

## Soalan yang dijawab

"Kaedah mana paling baik DARI SEMUA SEGI setakat ini, 100% = unggul semua segi?" — satu nombor setiap kaedah Mxx/Nxx/GB,
dipecah kepada empat tiang (Untung, Tahan, Bukti, Konsisten). Ia **pangkat maklumat**, BUKAN keputusan wang sebenar:
keputusan itu hanya datang daripada status **TERBUKTI** kad skor (`SPEC_KAD_SKOR.md`). Skor ini dipapar bersama baris
status kad skor dan tidak boleh melonggarkan gate.

## Mengapa skor komposit lama dibersarakan dan apa yang berbeza

Skor 0–100 dashboard v97–v154 (Untung 40 / Konsisten 20 / Risiko 25 / Bukti 15) dibersarakan 6 Nov 2026 kerana:
(1) tujuh pangkat atas penyebut berbeza bercanggah; (2) sampel terlalu kecil memberi skor ekstrem; (3) sauh persentil
p5–p95 hanyut dengan data; (4) berat diubah selepas melihat keputusan. Pembetulan dalam spec ini: (1) **satu penyebut**
= baris `data/analisis/kad_skor.json` (Lejar Penuh lorong 1, posisi LANGSUNG, terbuka ditanda-ke-pasaran, kos ditolak)
dan ekuiti lorong T4 L1 `portfolio_slot/t4_siri.csv`; (2) **kecutan ke 50** mengikut hari beli; (3) **sauh tetap**
daripada ambang pakar, bukan persentil; (4) berat dan sauh **dikunci di sini sebelum dikira**, dan kebolehramalan skor
diukur setiap larian (Spearman) sebelum ia dipercayai sebagai pangkat.

## Penyebut (satu sahaja)

Sama dengan kad skor: setiap posisi Lejar Penuh lorong 1 (keluar kaedah itu sendiri) yang direkod LANGSUNG (Mxx sejak
isyarat 2026-10-15; Nxx/GB sejak 2026-11-03), posisi terbuka ditanda-ke-pasaran, kos 0.2 % setiap pusingan, data
dikuarantin dibuang. Papertrade C ialah subset penyebut ini (Lejar merekod setiap isyarat setiap kaedah).

## Konsensus pakar yang menetapkan berat (rujukan)

- Jangkaan per dagangan ialah ukuran kelebihan; kadar menang sahaja bukan maklumat — Van Tharp (*Trade Your Way to
  Financial Freedom*, SQN, ≥ 100 dagangan), Mark Minervini (batting average × nisbah untung/rugi, sasaran 2:1),
  Nick Radge (saiz sampel kecil mengelirukan).
- Pulangan ÷ kejatuhan maksimum (MAR/Calmar) dan Gain-to-Pain ialah ukuran risiko utama — Jack Schwager (*Market Sense
  and Nonsense*), Radge, Curtis Faith; Ulcer Index (Peter Martin) menangkap kedalaman × tempoh, bukan MDD sahaja.
- Sharpe/t-stat mesti mengambil kira sampel kecil dan ujian berganda — Robert Carver (*Systematic Trading*: Sharpe sebenar
  jarang > 1, skew), Harvey & Liu (t = SR × √tahun; t = 2 lemah bila banyak strategi diuji), Bailey & López de Prado
  (Deflated Sharpe Ratio: jangkaan maksimum N normal, E[maks N]).
- Hadapan mesti ≥ 50 % daripada backtest (kecekapan jalan-ke-depan) — Robert Pardo (*The Evaluation and Optimization of
  Trading Strategies*); buang 2–3 % pemenang terbesar dan sistem mesti kekal untung; satu gate gagal = keluar — Kevin
  Davey (*Building Winning Algorithmic Trading Systems*).
- Kelancaran ekuiti (K-ratio) — Lars Kestner (1996/2003).
- Kelebihan mesti bertahan merentas rejim dan parameter — Andreas Clenow (*Stocks on the Move*); dapatan repo: tanda
  kelebihan pemimpin bertukar ikut rejim QQQ 12/17 tahun (7 Nov 2026).
- Jangan bergantung pada satu metrik — konsensus semua di atas.

## Tiang, metrik, berat dan sauh (DIKUNCI)

Setiap metrik dipetakan 0–100 secara linear sekeping-sekeping melalui tiga sauh (x0 → 0, x50 → 50, x100 → 100),
dipotong pada 0 dan 100. Metrik tiada data = 50 (neutral). Tiang = purata berberat metriknya.

| Metrik | Berat | Takrif | Sauh (0 · 50 · 100) |
|---|---|---|---|
| **A Keuntungan** | **35 %** | | |
| A1 | 20 | Jangkaan % setiap posisi (`jangkaan` kad skor) | −2 · 0 · +2 |
| A2 | 10 | Lebihan mata pulangan lorong T4 L1 (potongan LANGSUNG, pindaan (a)) lawan SPUS tingkap sama | −10 · 0 · +10 |
| A3 | 5 | Payoff = untung purata ÷ \|rugi purata\| (`payoff`) | 0.5 · 1.0 · 2.0 |
| **B Ketahanan** | **30 %** | | |
| B1 | 12 | Pulangan ÷ \|MDD\| lorong T4 L1 (potongan LANGSUNG; MDD sifar → nisbah dipotong ±10) | −1 · 0 · +1 |
| B2 | 6 | Ulcer Index % ekuiti T4 L1 = √purata(kejatuhan dari puncak²), puncak termasuk asas 1.0; kecil lebih baik | 10 · 5 · 0 |
| B3 | 6 | CVaR10 = purata 10 % posisi terburuk (`cvar10`) | −24 · −16 · −8 |
| B4 | 6 | `tanpa5` = jangkaan selepas buang 5 % posisi terbaik | −2 · 0 · +2 |
| **C Kebolehpercayaan** | **25 %** | | |
| C1 | 12 | t Newey-West purata buku harian (dipulihkan daripada selang 95 % kad skor); markah = 50 + 50 × t ÷ t_sauh, t_sauh = maks(`C1_T_MIN` = 2.0, E[maks N]) dengan N = bilangan kaedah diskor, E[maks N] = (1−γ)Φ⁻¹(1−1/N) + γΦ⁻¹(1−1/(Ne)), γ = 0.5772 | t = −t_sauh · 0 · +t_sauh |
| C2 | 8 | ½ × log-skala hari beli langsung (penuh `C2_HARI_PENUH` = 60) + ½ × log-skala posisi ditutup (penuh `C2_TUTUP_PENUH` = 100); log-skala(x, p) = 100 × ln(1+x) ÷ ln(1+p) | – |
| C3 | 5 | min(hari beli rejim ON, rejim OFF) ÷ `C3_REJIM_PENUH` = 10 × 100 | – |
| **D Konsistensi & kesahihan** | **10 %** | | |
| D1 | 4 | K-ratio = (cerun regresi log-ekuiti T4 L1 atas masa ÷ ralat piawainya) ÷ √n; n ≥ 5 | −0.2 · 0 · +0.2 |
| D2 | 3 | Lift masuk (`lift`): lulus BH-FDR → 100 jika positif, 0 jika negatif; belum lulus → 50 + 50 × lift ÷ `D2_LIFT_SKALA` (= 4); belum diuji → 50 | – |
| D3 | 3 | Kecekapan jalan-ke-depan = purata harian buku hadapan ÷ (purata backtest setiap dagangan ÷ hari pegang backtest); tiada backtest (Nxx/GB) → 50 | 0 · 0.5 · 1.0 |

Sumber sauh: A1/B4 ±2 % per posisi ≈ jangkaan swing cemerlang/teruk pada pegangan 5–20 hari; A3 Minervini 2:1;
B1 MAR 1.0 "kuat" (Schwager); B2 Ulcer 5 % ≈ setara toleransi MDD −10 % pengguna separuh masa; B3 −16 % ≈ CVaR
tipikal henti 4×ATR; C1 t_sauh deflasi López de Prado; C2 Tharp 100 dagangan; C3 = `G1_REJIM_MIN`; D1 0.2 ≈ Sharpe
tahunan ~1.8 (Carver: jarang > 1); D3 Pardo 50 %.

## Gabungan (DIKUNCI)

1. **Skor mentah** = exp(Σ berat_tiang × ln(maks(tiang, `LANTAI_GEO` = 1))) — min geometri berberat (Untung 0.35,
   Tahan 0.30, Bukti 0.25, Konsisten 0.10). Satu tiang hampir sifar menarik jumlah ke bawah (prinsip Davey).
2. **Kecutan**: skor = 50 + (skor mentah − 50) × h ÷ (h + `KECUT_H` = 20), h = hari beli langsung kaedah itu.
3. **Siling** ikut kad skor / pantau: NEGATIF ≤ 20, GANTUNG/BERSARA ≤ 30, GAGAL ≤ 40. TERBUKTI, CALON, BELUM CUKUP
   tiada siling.
4. Papar lima nombor: Untung · Tahan · Bukti · Konsisten · **Skor**, bersama status kad skor setiap kaedah.

## Pindaan 9 Nov 2026 (a) — metrik T4 dipotong pada mula LANGSUNG

**Dipradaftar 9 Nov 2026, hari yang sama dengan pradaftar asal, selepas semakan semula atas permintaan pengguna
("recheck sekali lagi") dan SEBELUM mana-mana keputusan dibuat dengan skor.** Dapatan semakan: lorong T4
(`portfolio_t4.py`) bermula 2026-10-16 bagi SEMUA kaedah termasuk Nxx/GB, sedangkan posisi Nxx/GB hanya LANGSUNG sejak
2026-11-03; sesi 16 Okt–2 Nov lorong Nxx/GB datang daripada posisi isian bina semula. Ini melanggar penyebut spec ini
("LANGSUNG sahaja"). Contoh: `N50X14` lorong penuh +10.75 % (16 sesi) tetapi hanya +3.18 % atas 4 sesi LANGSUNG.

Pembetulan (`skor_kaedah.lorong_langsung`): metrik A2, B1, B2, D1 dan pulangan T4 dalam sejarah Spearman dikira atas
lorong T4 L1 **dipotong pada sesi LANGSUNG pertama kaedah itu** (≥ `mula_langsung` kad skor), diasas semula supaya
tutup sesi sebelumnya = 1.0, MDD dengan puncak termasuk asas 1.0, SPUS berasas BUKA sesi pertama potongan (peraturan
`BANDING_SPUS.md`). Bagi Mxx (lorong bermula 16 Okt, LANGSUNG sejak isyarat 15 Okt) potongan = lorong penuh, disahkan
0 perbezaan pada 129 kaedah Mxx. Berat, sauh dan pemalar TIDAK berubah. Susulan (keputusan pengguna 9 Nov 2026 "ya"):
`portfolio_t4.py` kini membina lorong daripada posisi LANGSUNG sahaja (`SPEC_KAD_SKOR.md` pindaan 9 Nov 2026), jadi
lorong penuh = potongan LANGSUNG; `lorong_langsung` kekal sebagai pengawal jika lorong pernah mengandungi sesi isian.

## Apa yang sengaja TIDAK dimasukkan

Kadar menang, median, rugi purata, rugi terbesar (pengiraan dua kali dengan A1/A3/B3; `reports/Skor KPI pemilihan
kaedah swing.md`); pangkat backtest (tiada kuasa ramalan terukur, `laporan/KAEDAH_TERBAIK.md`); purata dipangkas sebagai
asas (kelebihan hidup dalam ekor kanan; `tanpa5` kekal metrik B4 sahaja).

## Semakan kebolehramalan (wajib sebelum skor dipercayai)

Setiap larian menyimpan snapshot (tarikh harga, kaedah, skor, pulangan T4 L1) dalam
`data/analisis/skor_kaedah_sejarah.csv`. Laporan mengira Spearman ρ antara skor snapshot terkini yang ≥ `SPEARMAN_HARI`
= 7 hari kalendar lalu dan pulangan lorong T4 L1 sejak snapshot itu, merentas kaedah (n ≥ 10). **Skor hanya dipercayai
sebagai pangkat selepas 8–12 minggu ρ positif yang konsisten**; sehingga itu ia paparan sahaja. Jika ρ tidak positif
selepas tempoh itu, keputusan pengguna diperlukan (ubah berat memerlukan pradaftar baharu).

## Keadaan pada pradaftar (9 Nov 2026, sebelum skor dikira)

223 kaedah, 16 hari beli langsung (rejim ON 1, OFF 15), semua BELUM CUKUP kad skor. Dengan kecutan h = 16, berat data
= 0.44, jadi skor hari ini dijangka dalam julat ~35–65: itu betul, bukan kecacatan.
