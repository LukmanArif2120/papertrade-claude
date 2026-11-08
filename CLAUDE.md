# Papertrade Claude (Backtest Shariah 2)

Stor utama projek "Backtest Shariah 2" sejak 14 Okt 2026. Baca dahulu `BacktestShariah2/00_NOTA_SERAHAN.md` (latar) dan `BacktestShariah2/standard/tugasan_v3.md` (peraturan harian). `tugasan_v2.md` dan `papertrade_harian.md` TERBATAL. **Sejarah penuh kajian, keputusan dan pelajaran (CLAUDE.md asal 76 KB, verbatim) ada dalam `BacktestShariah2/SEJARAH_KAJIAN.md` — baca bahagian berkaitan sebelum mencadangkan kajian baharu.** Fail ini sengaja ringkas: ia dimuat dalam setiap sesi, dan nombor yang disalin ke sini hanyut.

## WAJIB DALAM SETIAP CHAT REPO INI (keputusan pengguna 8 Nov 2026 — STRICT, tiada pengecualian)
Terpakai pada SETIAP sesi/chat baharu yang melibatkan repo ini (Claude Code web, app, desktop, CLI), bukan satu chat sahaja.
1. **Notifikasi telefon pada SETIAP jawapan:** pada akhir setiap giliran, muatkan `select:PushNotification` (ToolSearch) dan hantar satu baris < 200 aksara, status "proactive": hasil giliran itu + apa yang pengguna perlu putuskan. Abaikan jika keputusan alat "not sent". (Hanya tugasan berjadual `tolak_db.md` dan `mingguan.md` dikecualikan: ntfy sahaja.)
2. **Jawapan pendek, Bahasa Melayu mudah** — pengguna pening membaca jawapan panjang. Butiran teknikal hanya jika diminta.
3. **Jadual di jawapan TERAKHIR sahaja:** jawapan terakhir yang menutup sesuatu permintaan (kerja siap, atau berhenti menunggu keputusan pengguna) MESTI berakhir dengan SATU jadual tiga lajur: **Selesai** · **Tertangguh** (dengan sebab ringkas) · **Perlu keputusan anda** (soalan ya/tidak atau pilihan, dengan cadangan). Tulis "–" jika tiada. Jawapan perantaraan (kemas kini status, menunggu CI, notis latar belakang) TIDAK perlu jadual. Jangan letak keputusan yang perlu dibuat di tempat lain selain jadual itu.

## Matlamat pengguna (7 Nov 2026)
Cari kaedah swing yang **untung bersih melebihi rugi** (jangkaan positif; kadar menang sahaja bukan ukuran), dengan toleransi **MDD akaun -10%**. Sasaran asal +10%/bulan sudah diukur tidak boleh dicapai (`REVERSE/SASARAN.md`). Tiada wang sebenar sehingga kad skor menanda **TERBUKTI**.

## Sumber kebenaran — baca fail, JANGAN petik nombor daripada CLAUDE.md
| Soalan | Fail |
|---|---|
| Kaedah mana boleh guna wang sebenar? (satu jawapan) | `BacktestShariah2/laporan/KAD_SKOR.md` (`standard/kad_skor.py`) |
| Gate G1–G6, ambang terkunci, pindaan | `BacktestShariah2/standard/SPEC_KAD_SKOR.md` (pindaan 7 Nov 2026 berkuat kuasa) |
| Gate kemahiran sah? | `BacktestShariah2/laporan/PLASEBO_GATE.md` (`standard/plasebo_gate.py`; peraturan: lulus palsu ≤ 5%) |
| Lift masuk setiap kaedah | `BacktestShariah2/laporan/LIFT_KAEDAH.md` |
| Portfolio setiap kaedah lawan SPUS pada MDD -10% | `BacktestShariah2/laporan/T4_KAEDAH.md` |
| Kajian REVERSE: apa yang sudah diuji / tinggal | `python3 REVERSE/strategi.py` + `REVERSE/STRATEGI.md`, `REVERSE/KEPUTUSAN_AKHIR.md` |
| Keadaan repo, keputusan terbuka, kesegaran data | `KOORDINATOR.md` (dijana; jangan sunting) |
| Penanda aras | SPUS, bukan SPY (`REVERSE/PENANDA_ARAS_SYARIAH.md`, `laporan/BANDING_SPUS.md`) |

Peraturan tetap: laporan lain (PENGANALISIS, KAEDAH_TERBAIK, RINGKASAN portfolio, T4) memaparkan baris status kad skor (`standard/status_kad.py`) dan BUKAN keputusan.

## Struktur
- `BacktestShariah2/standard/` — skrip harian, penjana laporan, `sahkan.py`, sumber dashboard `dashboard_v2.html` (`dashboard.md`).
- `BacktestShariah2/kod/` — kod teras (enjin, `kaedah/Mxx.py`, `Nxx*.py`, `GB*.py`); sumber kebenaran kod kaedah.
- `BacktestShariah2/jadual/` — prosedur tugasan berjadual Claude: aktif `tolak_db.md` (Isn–Sab 10:20 NY) dan `mingguan.md` (Ahad); rutin lama 6:02 / 7:47 / 9:35 dimatikan (rujukan).
- `BacktestShariah2/ujian/` — `python3 -m unittest discover -s BacktestShariah2/ujian`.
- `BacktestShariah2/papertrade/` — Papertrade C (`claude*.csv`, `senarai_beli.csv`, `watchlist.csv`); skema `papertrade/SKEMA.md`.
- `BacktestShariah2/lejar/` — Lejar Penuh: setiap isyarat setiap kaedah, `lejar.yml` (`standard/lejar.py`). Jangan ubah manual. Bina semula memadam fail di bawah lejar/.
- `BacktestShariah2/data/konteks/` — konteks isyarat DIBEKUKAN (rejim QQQ/SPY, ATR%, jarak 52w, RS, sektor, earnings), tambah-sahaja (`standard/konteks_isyarat.py`, sejak 7 Nov 2026).
- `BacktestShariah2/data/harga/` — stor harga (`stor/`), faktor peristiwa, **kuarantin data tercemar** (`kuarantin.csv`, `standard/kuarantin.py`; SUPN/INDV 7 Nov 2026).
- `BacktestShariah2/portfolio_slot/` — portfolio maya 10 slot + jalur rawak + lorong T4; baca persentil jalur, bukan beza dua lorong.
- `BacktestShariah2/data/` lain — `rs/` (RS harian), `kumpulan/` (gred sektor/industri, `gred_kumpulan.yml`), `trend/`, `stage/` (paparan sahaja), `sec/` (EPS titik-masa), `senarai_bursa/` (direktori Nasdaq titik-masa), `institusi/` (13F, paparan sahaja), `analisis/` (output kad skor/lift/papan).
- `BacktestShariah2/spec/` — spec kaedah (`SPEC_SEMUA_KAEDAH.md`, `SPEC_SEMUA_N.md`); registry Nxx satu sumber `standard/registry_n.py`.
- `REVERSE/` — kajian signal/pembinaan (BUKAN kaedah Mxx; populasi berbeza). `AUTOTUNE/`, `WFO/` — backtest luar sampel; `data_mentah/` — dataset S1–S4 backtest; `requirements-kajian.txt` — pustaka sesi kajian sahaja (bukan workflow malam).
- Kaedah Mxx baharu: skrip `WFO/kaedah_baru/step2_<ID>.py`, tambah `kod/registry/<ID>.csv`, baris `data/registry_M_gabung.csv`, db `registry/<ID>` (`standard/dashboard_kemaskini.py`), baris `standard/katalog_kaedah.json`, jana semula papan.
- `KOORDINATOR.md` — dijana `standard/koordinator.py`; hanya `BacktestShariah2/koordinator/keputusan.csv` disunting manual.

## Dapatan yang sudah diukur — jangan ulangi tanpa sebab baharu
- Ruang signal masuk berasaskan indikator harga, penapis setup, fundamental dan silang **sudah diukur kosong**; baris gilir E1–E6 DITUTUP (`REVERSE/KEPUTUSAN_AKHIR.md`). Jangan tambah eksperimen ke-7 atau baris MASUK Nxx baharu.
- Keluar lebih berpengaruh daripada masuk (~12×); henti ketat (1–2×ATR) merugikan; sasaran untung merugikan; kadar menang bukan maklumat (`REVERSE/NXX_KELUAR.md`, `KOMBINASI.md`).
- Tiada sistem mengalahkan SPUS + tunai pada pendedahan sama; nisbah CAGR÷|MDD| campuran SPUS+tunai ~0.65 tetap — lever sebenar ialah BERAT (`REVERSE/SISTEM.md`).
- Kelebihan relatif saham pemimpin bertukar tanda ikut rejim QQQ (12/17 tahun, kajian 7 Nov 2026) — sebab G1 mewajibkan data dalam kedua-dua rejim.
- Ujian statistik setiap kaedah: SE berkelompok ikut hari beli meluluskan plasebo sehingga 45%; gunakan reka bentuk dalam `standard/lift_kaedah.py` (dua hala saham+minggu, asas hari × tercile ATR).
- Alam kajian A02 tiada saham delist (bias survivorship); setiap CAGR kajian condong ke atas.

## Peraturan
- **Dashboard:** artifact sedia ada https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e (db melalui ArtifactData); jangan cipta artifact baharu. Selepas SETIAP terbitan: `python3 BacktestShariah2/standard/semak_terbit.py --kemas --versi <version id> --nombor <n>` dan komit `data/dashboard_terbit.json` bersama `dashboard_v2.html` (`semak_data.yml` gagal tanpanya; `jadual/tolak_db.md` langkah 7 menyemak arah terbit-tanpa-komit). Jika penerbitan ditolak kerana versi lebih baharu hidup: GABUNG ke atas HTML hidup, jangan tulis ganti. Butiran: `standard/dashboard.md`.
- **Tiga jaring (4 Nov 2026):** `sandaran.yml` (sandaran mingguan data tidak boleh ganti ke Release, diuji setiap kali), `koordinator.py --semak` dalam `harian.yml` (tripwire data tidak bergerak, ambang 5 hari), `standard/saiz_repo.py` (ukur pertumbuhan git SEBELUM mencadangkan pembaikan saiz).
- Papertrade C (maya) sahaja untuk belian baharu sejak 13 Okt 2026. **Tiada order Moomoo, tiada wang sebenar.** "Kalau tak beli, cakap tak beli." Data mesti betul; jangan reka.
- Dua lorong keluar: kaedah, dan Chandelier tutup (tutup < tutup tertinggi sejak beli − 4×ATR14 → jual buka esok); direkod berasingan (`standard/keluar_lorong.py`, `papertrade/SKEMA.md`). Belian semula kaedah+saham sama dibenarkan selepas lorong kaedah keluar.
- Saham tidak layak, satu pintu `kod/tidak_layak.py`: diambil alih (`kod/ambil_alih.py`, `data/ambil_alih.csv`, `edgar.yml`), tidak cair, kelas berganda (`data/kelas_berganda.csv`). **Delist hanya jika direktori Nasdaq menandakan `buang`, tiada dalam `semasa.csv`, atau ambil alih selesai** (`tidak_layak.sah_delist`, 7 Nov 2026). Rahsia `SEC_USER_AGENT` diperlukan.
- Kaedah replika (M02, M19, M20, M26, M31, M38, M41, M47, M76, M78, M81, M82, M100): posisi hadapan dinilai dengan dagangan replika (`kod/dagangan.py`).
- Stor harga: konvensyen data backtest; sejarah dilaras hanya jika nisbah bar bertindih seragam (`kod/stor.py`, `log_laras.csv`); peristiwa besar melalui `kod/peristiwa.py` + `data/harga/faktor.csv`. **Anomali tidak boleh menimpa bar** — ticker dikuarantin dan dilepas hanya selepas semakan (`kuarantin.py lepas` = keputusan manusia). Versi pustaka dipin `kekangan.txt`.
- Penerangan teknikal dalam Bahasa Melayu baku.
- Larian berjadual: `git pull --rebase` dahulu, tulis di repo ini, commit dan push ke `main`. Jangan tulis ke Project claude.ai (dibekukan 14 Okt 2026). Sebelum push data: `python3 BacktestShariah2/standard/sahkan.py --betulkan` mesti keluar 0.
- **Kad skor:** ambang dikunci `ujian/test_kad_skor.py::TestKunci`; mengubahnya memerlukan keputusan pengguna + pradaftar bertarikh dalam `SPEC_KAD_SKOR.md` SEBELUM data terkesan dilihat, dan gate kemahiran mesti lulus `plasebo_gate.py`. Hanya hari beli LANGSUNG dikira (Mxx sejak isyarat 2026-10-15; Nxx/GB sejak 2026-11-03).
- Automasi: `.claude/settings.json` menyekat semua alat order (hook PreToolUse) dan memasang `requirements.txt` (SessionStart); `semak_data.yml` menjalankan ujian + `sahkan.py` pada setiap push ke `main` dan setiap PR; `penjaga_jadual.yml` (`standard/penjaga_jadual.py`) mencetus semula workflow berjadual yang hilang/lewat > 30 minit (tambah workflow berjadual baharu ke `JAGA`), juga dicetus oleh tugasan berjadual Claude `trig_01N3Qx1S6bRhf9h5BEKk85bQ` ke sesi Sonnet `session_018zpLxNRJ3rxZBvGT9yztVT`. Jangan buang atau longgarkan.
- GitHub Actions RASMI sejak 27 Okt 2026: `harian.yml`, `beli.yml`, `petang.yml`, `lejar.yml` → `analisis.yml` (hanya selepas Lejar berjaya). `BacktestShariah2/MOD_ACTIONS` = `rasmi`. Berpatah balik: `jadual/PERALIHAN.md`. Notifikasi ntfy topik `claude_azim` (`standard/notifikasi.py`; `amaran_ntfy.yml`). Rutin Claude 6:02 / 7:47 / 9:35 dimatikan — jangan hidupkan tanpa keputusan pengguna.
- Tugasan berjadual Claude (tolak db, mingguan) guna model Sonnet 5.5 sahaja; repo sudah dilampirkan (jangan `add_repo`). Alat Moomoo/SST mungkin berawalan lain: cari dengan ToolSearch nama alat. Larangan order terpakai tanpa mengira awalan.
- Plugin Superpowers: untuk sesi kerja bersama pengguna sahaja; rutin berjadual ikut `jadual/` terus tanpa skill brainstorming/soalan menunggu jawapan.
- Papan Penganalisis (`standard/penganalisis.py`, `analisis.yml`): skor gabungan backtest + hadapan dan label pantau (BERSARA/GANTUNG/AMARAN/OK/BELUM CUKUP) — maklumat dan input G5, bukan keputusan.
- Fail output dijana (papan, lift, kad skor, T4, KOORDINATOR, gred kumpulan, RS, trend, stage, institusi, SEC, senarai bursa) — jangan ubah secara manual; ubah penjananya.
