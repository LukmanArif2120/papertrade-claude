# kod/ — kod teras papertrade (sumber kebenaran)

Salinan tepat aset kod dashboard (id `4663135cc115bb60b40a6d93983f1456`, diambil 14 Okt 2026; 185 fail, disahkan sama bait demi bait).
Mulai 14 Okt 2026 **repo ini sumber kebenaran**. Aset dalam dashboard hanya salinan untuk larian.

- `enjin.py` — enjin backtest v1.2 (BEKU, jangan ubah logik).
- `stor.py` — stor harga harian (harga_A/B/idx.csv).
- `ambil_alih.py` — penapis saham sedang diambil alih (isyarat palsu; sejak 21 Okt 2026): `tapis()` dipakai scanner.py, standard/harian_c.py dan standard/lejar.py; senarai sah `data/ambil_alih.csv`.
- `scanner.py`, `pasang.py`, `parse_screen.py`, `beli_alat.py`, `tambahan.py` — imbasan harian dan alat larian.
- `uji_kaedah.py` — semak modul kaedah lawan registry.
- `kaedah/Mxx.py` — modul isyarat 134 kaedah M: M01–M111 (87) + calon K145+ M115–M161 (47, sejak 16 Okt 2026; pembantu `kaedah/_k145.py`; entry daripada `WFO/kaedah_baru/`, stop/exit/tmax pilihan WFO 2026S4 dibekukan; `hampir()` belum ditakrif) (antara muka: `ANTARAMUKA.md`; takrif hampir: `ARAHAN_HAMPIR.md`).
- `registry/Mxx.csv` — registry asal yang dipakai oleh modul kaedah untuk memilih varian.

## Mengubah kod
1. Ubah fail di sini, commit dengan mesej yang jelas.
2. Bungkus: `python3 BacktestShariah2/standard/bungkus_kod.py /tmp/kod.json --banding <aset_lama.json>`.
3. Muat naik `/tmp/kod.json` sebagai aset dashboard (Artifact publish `asset: true`), kemas kini `harian/status` → `harga_aset.kod` dengan id baharu.
4. Catat id aset baharu dalam log harian.

Jangan ubah aset kod terus dalam dashboard tanpa mengemas kini folder ini.
