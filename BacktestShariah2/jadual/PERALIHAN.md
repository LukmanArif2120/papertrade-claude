# Peralihan rutin Claude → GitHub Actions (keputusan pengguna 17 Okt 2026)

Tujuan: jimat token (rutin Claude ~37 juta token sehari) supaya papertrade boleh berjalan pada pelan Pro.
Keputusan pengguna: (1) berjalan selari 3 hari dagangan dahulu; (2) belian kekal sekitar 9:35 NY; (3) data yang hanya
Moomoo/SST boleh beri dikumpul seminggu sekali; (4) dashboard dikemas kini oleh satu sesi Claude ringkas setiap hari.

## Komponen
| Tugas | Dahulu (rutin Claude) | Selepas peralihan |
|---|---|---|
| Kemas kini posisi (harga, keluar 2 lorong, betulkan harga beli, kesahihan) | 6:02 pagi MYT | `harian.yml` 05:07 UTC (+ sandaran 07:07, 09:07, 11:07) → `harian_c.py malam` |
| Imbas 134 kaedah, senarai beli, watchlist, rekod isyarat | 7:47 malam MYT | sama (`harian.yml`, langkah yang sama) |
| Gred S/I/R/Q/P | 7:47 malam MYT | `harian.yml` + `petang.yml` 11:47 UTC (P disegar semula sebelum buka) |
| Beli maya 9:35 NY | rutin 9:35 NY (quote Moomoo) | `beli.yml` 9:40 NY (yfinance; disahkan bar harian keesokannya) |
| Harga | skrin Moomoo + yfinance | yfinance muktamad (tarikan ≥ 05:00 UTC sama dengan Moomoo; lihat log 17 Okt) |
| Lejar Penuh | `lejar.yml` | `lejar.yml` 06:17 UTC (tidak berubah; pengawal data muktamad) |
| Pengawas (6 semakan sehari) | sesi Sonnet | dibuang; sandaran jadual + `jana_db.py` pengawas + e-mel kegagalan GitHub |
| Tolak db dashboard | dalam setiap rutin | `jadual/tolak_db.md` (sesi Claude baharu, Isn–Sab 10:20 NY) |
| Jejak kertas M166 V1 (`uji_kertas/jejak_M166.csv`) | imbas 7:47 langkah 4b | `harian.yml` (mod rasmi sahaja) |
| Universe Shariah, sektor seluruh pasaran, SST, akaun Moomoo | setiap hari | `jadual/mingguan.md` (Ahad) |
| Kewangan Moomoo (gred kewangan v7), peristiwa korporat (rehab Moomoo) | imbas 7:47 langkah 5c; 6:02 langkah 2d | `jadual/mingguan.md` 7b, 7c |
| Saham tidak layak, kaedah replika (R10), belian buka_lewat | 6:02 langkah 2c; beli 9:35 | `harian_c.py` (sudah terbina) |

Mod ditentukan oleh `BacktestShariah2/MOD_ACTIONS`: `bayang` = Actions menulis ke `BacktestShariah2/bayang/` sahaja dan
membanding setiap hari dengan rutin Claude (`bayang/BANDING_<tarikh>.md`); `rasmi` = Actions menulis ke `papertrade/`.

## Bukti sebelum mod selari (ulang tayang 16–17 Okt, `standard/banding_bayang.py`)
- Kemas kini 17 Okt: 2,696/2,696 posisi sama (harga beli termasuk 553 pembetulan, status/tarikh/harga keluar, harga terkini);
  133 keluar (C 125, M 8), 60 menunggu, ANF M153 tidak dibeli — sama tepat dengan log Claude.
- Imbas 16 Okt: dengan isyarat yang sama, senarai beli 847/847 sama (dipegang 184, had 2,473, mingguan 97 sama tepat).
  Isyarat 3,600/3,601 sama; 92 isyarat tambahan Actions daripada 15 saham yang tiada sejarah harga pada larian Claude.
- Beli 16 Okt: 819/820 sama; harga 819/819 = harga rasmi selepas pembetulan Claude. ANF M153 dilangkau terus (Claude:
  direkod kemudian ditanda tidak dibeli). 16 saham "belum didagangkan 9:36" dibeli pada buka rasmi dalam ulang tayang.

## Bukti mod selari 19–21 Okt (bayang/BANDING_*.md; belian sebenar bayang lawan papertrade rasmi selepas semakan kesahihan)
- Workflow: semua larian harian/beli/petang berjaya; jadual GitHub lewat ditampung `penjaga_jadual` (beli 20–21 Okt 10:13 NY).
- Kemas kini: 20 Okt 3,266/3,267 sama (SBH: low data). 21 Okt 3,676/3,750: 74 beza semuanya peraturan baharu selepas rutin Claude
  berjalan (60 penapis ambil alih 21 Okt 15:31 UTC, 14 kaedah replika R10) dan diterapkan ke rasmi kemudian.
- Senarai beli: 603/604, 517/519; 21 Okt bayang 729 lawan Claude 730 (beza ulang tayang = penapis tidak layak/kelas berganda baharu).
- Belian sama: 562, 445, 659; harga sama 562/562 dan 659/659. 20 Okt: 54 harga bayang salah kerana stor dicemari buka sementara
  Moomoo (`lejar.tampal_moomoo`, dibetulkan R1 22 Okt; selepas peralihan tiada buka Moomoo ditulis). Belian Claude sahaja =
  yang Claude sendiri tanda tidak sah esoknya (13, 7, 6), kecuali ADI (tiada bar Yahoo 19 Okt) dan HAFN ×5 (universe harian
  Claude; Actions guna universe mingguan). Belian Actions sahaja = saham belum didagangkan pada masa belian Claude (peraturan
  `buka_lewat` sejak 22 Okt menyamakan kedua-duanya).

## Langkah peralihan (sesi Claude dengan alat claude-code-remote; selepas 3 laporan BANDING lulus dan pengguna setuju)
1. Semak `bayang/BANDING_*.md` 3 hari dagangan: kemas kini ≥ 99% sama (beza hanya data), senarai beli dan belian sama
   kecuali beza data yang dijelaskan, tiada kegagalan workflow (`mcp__github__actions_list`).
2. Pilih masa di antara rutin Claude (bukan semasa rutin sedang berjalan). Tulis `BacktestShariah2/papertrade/status_harian.json`
   = keadaan terakhir rutin Claude: `{"malam": {"sesi": "<sesi yang sudah dikemas kini DAN diimbas>"}, "beli": {"tarikh": "<tarikh belian terakhir>"}}`
   (tinggalkan `malam` jika imbasan sesi terakhir belum dibuat).
3. `echo rasmi > BacktestShariah2/MOD_ACTIONS`; jadual `harga_harian.yml` DIKEKALKAN (dijaga `penjaga_jadual`; dipakai workflow lain sebelum 05:07 UTC);
   `git rm -r BacktestShariah2/bayang/papertrade BacktestShariah2/bayang/pemangkin BacktestShariah2/bayang/isyarat` (laporan BANDING kekal).
4. Matikan tugasan berjadual (`mcp__claude-code-remote__update_trigger`, enabled=false): tiga rutin "Papertrade – Kemas kini 6:02
   pagi / Imbas 7:47 malam / Beli 9:35 NY" (`trig_01R2RcT5GZ4xGkncK5xa1jnH`, `trig_012DQb9KbjfhpKuopsMByNDh`,
   `trig_018pfWtxtyMaC6aaThn7UDCo`; sahkan dengan `list_triggers`) dan pengawas yang masih aktif (`trig_018zyZSoegh4fQWpWGv3wS9m`,
   `trig_01AJf4h6GffXNmHXmQsVzzGF`, `trig_018eaPB3VHoodMscT1s8BiLs`; 22 Okt sudah tiada dalam senarai aktif).
5. Cipta tiga tugasan berjadual baharu (`create_trigger`, `create_new_session_on_fire`=true, model `claude-sonnet-5-5`,
   connectors yang perlu sahaja): tolak db `CRON_TZ=America/New_York 20 10 * * 1-6`, prompt "Ikut BacktestShariah2/jadual/tolak_db.md";
   mingguan `CRON_TZ=Asia/Kuala_Lumpur 47 10 * * 0`, prompt "Ikut BacktestShariah2/jadual/mingguan.md"; notifikasi harian
   `CRON_TZ=Asia/Kuala_Lumpur 17 15 * * 2-6`, prompt "Ikut BacktestShariah2/jadual/notifikasi_harian.md" (permintaan pengguna 24 Okt 2026).
6. Kemas kini `standard/tugasan_v3.md` §2, `jadual/README.md` dan `CLAUDE.md` (rutin harian = Actions); catat dalam log; commit + push.
7. Jika `status_harian.json` tiada `malam` bagi sesi terakhir, tembak `harian.yml` sekali (workflow_dispatch).
