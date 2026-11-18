# Papertrade Claude (Backtest Shariah 2)

Fail ini sengaja ringkas kerana dimuat dalam setiap chat (keputusan pengguna 18 Nov 2026). **Butiran penuh (matlamat, sumber kebenaran setiap kajian CS01–CS24, dapatan, peraturan lanjut) ada dalam `BacktestShariah2/RUJUKAN_CLAUDE.md`. Baca bahagian yang perlu sahaja (grep tajuk / kod CS), bukan seluruh fail.** Latar: `BacktestShariah2/00_NOTA_SERAHAN.md`; peraturan harian: `BacktestShariah2/standard/tugasan_v3.md`; sejarah lama: `BacktestShariah2/SEJARAH_KAJIAN.md`. Jangan petik nombor daripada fail ini; baca fail sumber.

## WAJIB DALAM SETIAP CHAT REPO INI (keputusan pengguna — STRICT)
1. **Jimat token = peraturan PALING UTAMA (18 Nov 2026).** Pilih cara paling murah: baca bahagian fail yang perlu sahaja (grep / `sed -n`); jangan baca semula fail atau ulang fakta; gabung panggilan alat selari; elak subagen / workflow kecuali jelas lebih murah; jangan cuba langkah yang mungkin disekat (cth. push terus ke `main` — guna PR); jawapan pendek. Sejurus SELEPAS jadual jawapan terakhir, tulis satu baris `Jimat token: ...` — nyatakan penjimatan yang BOLEH DIUKUR (cth. "tidak membaca fail X, 40 KB"); jika tidak diukur, tulis "tidak diukur". Jangan reka peratus.
2. **Notifikasi telefon HANYA bila kerja siap atau perlu keputusan pengguna:** muatkan `select:PushNotification` (ToolSearch), satu baris < 200 aksara, status "proactive". Abaikan jika "not sent". (Tugasan berjadual `tolak_db.md`: ntfy sahaja.)
3. **Jawapan pendek, Bahasa Melayu mudah, perkataan biasa** — bukan istilah dalaman (tulis "papertrade" bukan "jejak hadapan/kohort"; "saham yang carian tidak pernah lihat" bukan "kumpulan B"; "peraturan ditulis dahulu sebelum diuji" bukan "pradaftar/pindaan"; "ujian lulus/gagal" bukan "bacaan dikunci"); kod / nama fail hanya sebagai rujukan di hujung. **Jika tidak faham kehendak pengguna, TANYA soalan pendek — jangan teka.** Keputusan teknikal diserahkan kepada Claude.
4. **Jadual di jawapan TERAKHIR sahaja:** SATU jadual tiga lajur **Selesai** · **Tertangguh** (sebab ringkas) · **Perlu keputusan anda** (ya/tidak atau pilihan, dengan cadangan); "–" jika tiada. Jawapan perantaraan tanpa jadual. Keputusan hanya diletak dalam jadual itu.

## Matlamat pengguna (ringkas; penuh: `RUJUKAN_CLAUDE.md` § Matlamat pengguna)
- Cari setup swing lengkap terbaik (prasyarat → syarat → pegang → keluar, stop loss) yang paling kerap menangkap saham naik ≥ 5 % seminggu kemudian naik lagi 2–4 minggu. **Kayu ukur = KADAR TANGKAP** (dipapar bersama kadar menang dan purata). BUKAN indeks, untung/MDD akaun, atau purata setiap dagangan.
- **Senarai kerja rasmi = Top 100 "Setiap minggu"** (`BacktestShariah2/kajian/carian_setup/hasil/CS23/TOP100.md` §5); §6 musim laporan kewangan = tambahan bermusim. Tunjuk setup setiap minggu dahulu.
- Peraturan setup: swing; tiada beli-jual hari sama; pegang ≥ 3 hari; stop loss wajib tetapi longgar (saham laju: 4×ATR14 dari harga beli — jangan tukar); pegang selagi naik.
- **Dihentikan / dijeda atas keputusan pengguna — jangan cadang kecuali diminta:** papertrade (`jejak_f2/JEDA`); kumpulan saham tenang / jual 5 % dari puncak (CS24); carian keluar manual; carian ikut ukuran longgar (CS12, CS22); carian kombinasi indikator pada data lama. Tiada tapisan Shariah buat masa ini pada setup F.
- **Larangan:** jangan nilai/tolak/cadang berhenti kerja CS ikut indeks, untung akaun atau MDD; jangan cadang ukuran akaun, pembekuan, had calon atau kerja sampingan. Langkah selepas backtest = papertrade setup terbaik, hanya dengan keputusan pengguna.
- **Sebelum melaporkan setup F atau T**, baca ayat "WAJIB sebut" bagi pusingan berkaitan dalam `RUJUKAN_CLAUDE.md` § Dapatan (grep kod CS). Sebelum menyambung kerja CS: `BacktestShariah2/kajian/SERAHAN_CARIAN_SETUP.md`.

## Sumber kebenaran utama (senarai penuh: `RUJUKAN_CLAUDE.md` § Sumber kebenaran)
- Wang sebenar? `BacktestShariah2/laporan/KAD_SKOR.md` · gate: `standard/SPEC_KAD_SKOR.md` · keadaan repo: `KOORDINATOR.md` (dijana) · apa yang sudah diuji: `python3 REVERSE/strategi.py` · penanda aras SPUS, bukan SPY.
- Setup F: `kajian/carian_setup/hasil/CS13/SENARAI_UTAMA.md`, `CS20/MINGGUAN.md`, `CS23/TOP100.md`; lorong T: `CS17/SENARAI_T.md`, `CS18/SOLID_T.md`; registry `data/registry_F.csv`.

## Peraturan kritikal (lanjut: `RUJUKAN_CLAUDE.md` § Peraturan, § Struktur)
- **Tiada order Moomoo, tiada wang sebenar.** Data mesti betul; jangan reka.
- **Dashboard:** artifact sedia ada https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e; jangan cipta baharu. Selepas setiap terbitan: `python3 BacktestShariah2/standard/semak_terbit.py --kemas --versi <id> --nombor <n>` dan komit `data/dashboard_terbit.json` bersama `dashboard_v2.html`. Jika ditolak kerana versi lebih baharu: gabung atas HTML hidup. Butiran `standard/dashboard.md`.
- Pusingan carian baharu perlu peraturan bertarikh dalam spec dahulu (`kajian/SPEC_CARIAN_SETUP.md`); pusingan / penjejak baharu WAJIB `kausal=True`.
- Fail dijana (papan, lift, kad skor, KOORDINATOR, `jejak_f*/`, `lejar/` dll.) — jangan ubah manual; ubah penjana. Ambang kad skor dikunci ujian; ubah hanya dengan keputusan pengguna.
- Sebelum push data: `python3 BacktestShariah2/standard/sahkan.py --betulkan` keluar 0. Ujian: `python3 -m unittest discover -s BacktestShariah2/ujian`.
- Larian berjadual: `git pull --rebase`, komit dan push ke `main`; model Sonnet 5.5; repo sudah dilampirkan.
- Jangan buang atau longgarkan automasi (`.claude/settings.json` sekat order, `semak_data.yml`, `penjaga_jadual.yml`, `sandaran.yml`). Rutin Claude lama 6:02 / 7:47 / 9:35 kekal mati.
- Penerangan teknikal dalam fail: Bahasa Melayu baku.
