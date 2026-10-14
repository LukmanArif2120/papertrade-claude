# Tugasan v2 — Dashboard & Papertrade (diluluskan 12 Okt 2026)

> **TERBATAL (14 Okt 2026).** Diganti oleh `standard/tugasan_v3.md` dan `jadual/`. Dikekalkan untuk sejarah sahaja; jangan ikut peraturan di bawah.


Dokumen rujukan untuk SEMUA tugasan berjadual v2. Baca ini dahulu, kemudian `standard/dashboard.md` dan `standard/papertrade_harian.md` (v1). Jika bercanggah, dokumen ini menang.

## Dashboard
- Artifact sedia ada: "Papan Backtest Shariah" https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e — kemas kini di URL ini (baca dahulu dengan Artifact action read, kekalkan db sedia ada). Jangan cipta artifact baharu.
- Struktur tab (ikut gambar pengguna):
  1. Backtest → sub-tab: Ringkasan | Papan Kedudukan | Banding (kekalkan kandungan sedia ada)
  2. Sector → heatmap sektor & industri (prestasi 1M/W, RS, breadth, aliran dana/institusi, volum relatif, ranking "panas"). Sumber: SST Terminal (sector_rotation, industry_rotation, market_heatmap, institutional_flow, unusual_volume).
  3. Watchlist → Hampir Signal sahaja (90–100% dekat isyarat entry, setiap kaedah; nyatakan kaedah, syarat yang belum cukup, paras pencetus, sektor, industri).
  4. Paper Trade M → Moomoo Papertrade (posisi + keputusan dalam SATU tab)
  5. Papertrade C → Claude Papertrade (maya)
  6. Prestasi → sub-tab: Papertrade M | Papertrade C | Combine
- Buang tab Panduan istilah; ganti dengan tooltip hover pada setiap istilah/lajur.
- Lajur jadual Paper Trade M, Papertrade C dan Prestasi DISELARASKAN (lajur sama, susunan sama): Tarikh beli, Saham, Kaedah, Sektor, Industri, Harga beli, Unit, Harga terkini, Untung %, Hari dipegang, Isyarat keluar (status), Tarikh keluar, Harga keluar, Untung akhir %.
- Setiap saham WAJIB ada Sektor dan Industri.
- Semua jadual boleh disusun (klik tajuk lajur, naik/turun).
- Saham yang sudah kena isyarat keluar ikut kaedahnya: baris diserlah MERAH, harga dibekukan pada tarikh/harga keluar, tidak dikemas kini lagi. Posisi Moomoo TIDAK dijual (tanda merah sahaja) dan slotnya kekal dikira.
- Prestasi: matlamat = cari kaedah paling untung DAN paling selamat untuk swing. Paparan: carta bar untung purata/kaedah, kadar menang (donut/bar), scatter untung vs penurunan maksimum (risiko), ranking "Paling Teruk" (kadar gagal, kerugian terbesar, isyarat keluar rugi), skor gabungan Untung×Selamat. Mudah dibaca, label BM baku.
- Gaya: SST Terminal — latar gelap navy (#0b1220/#0f172a), kad #111a2e, sempadan halus, teks kelabu muda, hijau #22c55e untung, merah #ef4444 rugi, ungu/teal untuk bar skor, lencana pil kecil (BUY/HOLD), fon sans moden (Inter), angka tabular, jadual padat. Mesra telefon.

## Peraturan papertrade
- Kaedah: 87 kaedah M (varian terbaik dalam registry, seperti v1).
- Skop imbasan: SEMUA saham AS harga > USD10 (Shariah atau tidak); senarai 431 diimbas dahulu.
- Beli hanya apabila isyarat entry kaedah dipenuhi 90–100%. 1 unit setiap saham.
- Keutamaan: Moomoo papertrade (akaun simulasi) dahulu — maksimum 10 saham SETIAP KAEDAH. Jika kaedah itu sudah 10/10 di Moomoo → beli maya dalam Claude Papertrade (1 unit, harga buka sebenar, rekod sama seperti Moomoo).
- Watchlist hanya calon Hampir Signal; apabila larian seterusnya isyarat lengkap → beli (Moomoo dahulu, kemudian Claude).
- Keluar: kira ikut peraturan keluar kaedah masing-masing; tanda merah; tiada jualan Moomoo.
- Wang sebenar: TIDAK SEKALI-KALI tanpa kelulusan pengguna.
- Hanya pada hari pasaran AS dibuka (semak kalendar NYSE; cuti = berhenti).

## Stor data (Project)
- `papertrade/moomoo.csv`, `papertrade/claude.csv` (lajur seperti di atas + id_kaedah, sumber), `papertrade/watchlist.csv`, `papertrade/sektor.csv` (snapshot heatmap). Juga tolak ke db dashboard (ArtifactData) supaya halaman terus papar.
- Log kemajuan binaan malam 13 Okt: `standard/binaan_v2_log.md` — setiap peringkat baca log ini dahulu dan tambah catatan di akhir.

## Jadual
- Binaan sekali (13 Okt MYT): P1 00:01 audit & struktur | P2 01:15 Papertrade M & C | P3 02:30 Watchlist & Sector | P4 03:45 Prestasi & gaya SST | P5 05:00 QA & publish (siap < 06:00).
- Harian: 8:02 malam MYT Isnin–Jumaat imbas & watchlist | 9:35 pagi New York Isnin–Jumaat beli | 6:02 pagi MYT Selasa–Sabtu kemas kini M, C, Prestasi.
