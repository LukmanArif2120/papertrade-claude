# CS22: setup sepanjang tahun yang dicari ikut ukuran kedua — "+10 % sebelum −8 %" (backtest; BUKAN bukti)

> **Status keputusan (kad skor, harga 2026-11-13):** TERBUKTI 0 · CALON 0 · BELUM CUKUP 226 · GAGAL 0 · NEGATIF 0. Rejim QQQ OFF sejak 2026-10-16. Hanya **TERBUKTI** layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak boleh dibaca sebagai pangkat untuk wang sebenar.

Dijana `kajian/carian_setup/cs_capai22.py`. Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 17 Nov 2026 (ai). **Jangan sunting secara manual.**

## 1. Apa yang dibuat

- Carian CS20 diulang dengan satu perubahan: setup dipangkatkan ikut **"kena"** — selepas beli, harga TUTUP ≥ +10% sebelum menyentuh −8%, dalam 63 sesi (≈ 3 bulan) — bukan ikut "naik ≥ 5 % dalam minggu pertama". Prasyarat tarikh laporan kewangan / kalendar tetap tidak dibenarkan dan setiap setup tetap mesti membeli hampir setiap minggu.
- 1,156 isyarat beli (1,116 cukup isyarat); 102,675 peraturan ditinjau; **783 calon**. Kawalan = 300 peraturan rawak daripada ruang yang sama.
- "Lulus" = pada saham yang carian tidak lihat: belian ≥ 300, ≥ 10 tahun aktif, dan "kena" lebih kerap daripada saham rawak hari sama dalam KETIGA-TIGA tempoh (2010–19, 2020–24, 2025–26).

## 2. Ujian (ditetapkan dahulu)

- **B1** kadar lulus: calon **42 %** lawan kawalan 6 % (perlu beza ≥ 20 mata) → lulus.
- **B2** lebih baik daripada rawak pada 2025–26: calon **50 %** lawan kawalan 50 % (perlu ≥ 60 % dan beza ≥ 10 mata) → GAGAL.
- **Keputusan: carian ikut ukuran kedua TIDAK berhasil — tiada kod F baharu.**
- Dilaporkan sahaja: calon lulus lebih baik daripada rawak dalam 71 % tahun (kawalan 41 %); "kena" bertambah lebih daripada "jatuh dahulu" bagi 93 % calon lulus (kawalan 29 %).

## 3. Berapa yang lulus

- Lulus: **332** daripada 783 calon; juga membeli hampir setiap minggu pada saham tidak dilihat: 314; dan "kena" bertambah lebih daripada "jatuh dahulu": **290**.
- Daripada 290 itu: 20 sama atau kembar dengan kod F sedia ada (11 kod berbeza — "kod sedia ada yang juga lulus ukuran kedua"); 105 kembar calon lain.
- **Setup baharu: 165** (belum / tidak didaftarkan).
- Anggaran lulus kerana nasib (kadar lulus kawalan ÷ kadar lulus calon): kira-kira 15 %.

## 4. Mutu (nilai tengah setiap kumpulan; saham yang carian tidak lihat; kurungan = saham rawak hari sama)

| Kumpulan | Bilangan | **Kena %** | Jatuh dahulu % | Terus naik % (sesi ke-63 masih ≥ +10 %) | Tangkap % (ukuran utama) | Menang % cara B (rawak dipegang sama) | Purata % cara B | Minggu ada belian |
|---|---|---|---|---|---|---|---|---|
| Kod sedia ada yang juga lulus | 11 | **42.4** (40.9) | 52.9 (52.9) | 33.7 (31.9) | 8.4 (7.0) | 47 (45) | +0.9 (+0.3) | 95 % |
| Calon lulus (semua) | 332 | **41.8** (40.2) | 51.8 (52.3) | 32.8 (31.1) | 7.8 (7.0) | 47 (45) | +0.7 (+0.3) | 94 % |
| Kawalan rawak (ruang sama) | 300 | **38.8** (39.1) | 48.8 (48.3) | 29.7 (29.6) | 5.6 (5.5) | 46 (45) | +0.3 (+0.3) | 96 % |

## 7. Kod sedia ada yang juga lulus ukuran kedua (11 kod; teratas 11)

| # | ID | Prasyarat | Isyarat beli | Penapis saham | Beli setahun | **Kena %** (rawak) | Beza 2010–19 / 2020–24 / 2025–26 | Jatuh dahulu % (rawak) | Terus naik % (rawak) | Tangkap % (rawak) | Menang % (rawak) | Purata % (rawak) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `F2276` | hasil suku terkini tumbuh >= 20% | K01.064 RSI(5) < 30 + atas MA200 | – | 1018 | **43.0** (40.9) | +2.8 / +2.0 / +0.3 | 51.9 (52.7) | 34.5 (32.3) | 8.4 (7.6) | 47 (45) | +1.0 (+0.3) |
| 2 | `F2366` | hasil suku terkini tumbuh >= 20% | K16.001 gap-and-go (buka > tinggi semalam + 0.0%) | MACD > isyarat + ADX < 20 | 714 | **41.8** (39.9) | +3.1 / +1.4 / +0.6 | 52.7 (53.1) | 33.7 (31.3) | 8.6 (7.0) | 47 (45) | +0.8 (+0.2) |
| 3 | `F2270` | >= 60% saham sektor di atas MA50 | K17.019 undur ke ema20 yang naik (tol 1.0%) | RS >= 90 + dalam 15% dari puncak 52 minggu | 616 | **41.7** (39.9) | +2.1 / +1.2 / +2.1 | 53.8 (52.9) | 33.5 (30.9) | 8.0 (6.6) | 45 (44) | +0.5 (+0.1) |
| 4 | `F2091` | >= 60% saham sektor di atas MA50 | K17.015 undur ke ema20 yang naik (tol 0.0%) | RS >= 90 + dalam 15% dari puncak 52 minggu | 462 | **41.9** (40.1) | +1.7 / +1.8 / +2.6 | 54.1 (53.5) | 33.9 (31.1) | 8.5 (7.0) | 45 (44) | +0.4 (+0.1) |
| 5 | `F2770` | hasil suku terkini tumbuh >= 20% | N56 RSI>50 + ADX>20 (benih N) | MA50 > MA200 + MACD > 0 | 632 | **41.1** (39.5) | +2.9 / +0.2 / +2.1 | 52.5 (52.6) | 33.2 (30.9) | 7.8 (6.5) | 46 (45) | +0.7 (+0.1) |
| 6 | `F2616` | – | K01.067 RSI(7) < 20 | volum 10 hari > volum 50 hari + ATR% >= 4 | 841 | **43.8** (42.3) | +0.5 / +1.7 / +3.1 | 55.4 (56.6) | 42.5 (42.1) | 13.4 (12.0) | 49 (47) | +1.8 (+1.3) |
| 7 | `F2796` | hasil suku terkini tumbuh >= 20% | N56 RSI>50 + ADX>20 (benih N) | tutup > MA200 + MA50 naik (lawan 20 bar lalu) | 742 | **41.1** (39.8) | +2.5 / +0.1 / +1.7 | 52.9 (52.7) | 32.9 (31.0) | 7.7 (6.7) | 47 (45) | +0.7 (+0.1) |
| 8 | `F2793` | – | K09.005 MACD(8,17,9) silang naik bawah sifar | ADX < 20 + hari naik (tutup > buka) | 2923 | **42.5** (41.3) | +1.2 / +1.3 / +0.7 | 47.8 (48.3) | 32.9 (31.9) | 6.9 (6.6) | 48 (47) | +1.0 (+0.7) |
| 9 | `F2629` | – | K03.026 tutup < jalur bawah BB(20, 1.5) + RSI14 < 30 | >= 30% di bawah puncak 52 minggu + volum 10 hari > volum 50 hari | 846 | **44.3** (43.3) | +0.7 / +1.3 / +0.9 | 54.3 (55.0) | 43.5 (42.3) | 13.0 (11.6) | 49 (48) | +1.6 (+1.8) |
| 10 | `F2794` | – | K09.011 MACD(6,19,6) silang naik bawah sifar | ADX < 20 | 3920 | **42.4** (41.5) | +0.7 / +1.2 / +0.1 | 48.2 (48.6) | 32.8 (32.3) | 7.0 (6.6) | 47 (47) | +0.9 (+0.7) |
| 11 | `F2603` | – | K03.014 tutup < jalur bawah BB(15, 1.5) + RSI14 < 30 | >= 30% di bawah puncak 52 minggu + volum 10 hari > volum 50 hari | 856 | **43.7** (43.0) | +0.4 / +0.9 / +1.2 | 54.9 (55.4) | 43.6 (42.5) | 12.9 (11.5) | 49 (48) | +1.7 (+1.6) |

## 8. Kaveat

- Saham rawak sendiri "kena" kira-kira 40 daripada 100 kali dalam 3 bulan; yang bermakna hanya beza lawan rawak, dan beza itu kecil.
- 2025–26 ialah syarat lulus, bukan tempoh di luar sampel; ukuran longgar pernah gagal pada tahun tidak dilihat (CS12).
- Ukuran kedua tidak bergantung pada cara pegang; angka menang dan purata di sini memakai cara pegang B seperti kod lain.
- Tiada saham delist dalam data ("kena" condong ke atas bagi semua, termasuk saham rawak). Backtest sahaja; tiada papertrade tanpa keputusan pengguna; kad skor kekal satu-satunya keputusan wang sebenar.
