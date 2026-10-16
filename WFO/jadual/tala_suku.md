# Penalaan semula suku tahunan (1 Jan/Apr/Jul/Okt, 9:49 pagi MYT)

Automatik; jangan tanya soalan. Tiada order. MENGHASILKAN CADANGAN SAHAJA — tetapan Papertrade C TIDAK diubah
sehingga pengguna meluluskan (`tala_semula.py guna`). Label = tahun + suku yang baru tamat, cth. `2026S4`.

1. `git pull --rebase origin main`. Pastikan `pip install -q -r requirements.txt` (numba, optuna).
2. Stor harga: baca `harian/status` (ArtifactData) → `harga_aset` A, B, idx. Muat turun setiap aset (`Artifact` action read, `path` = id aset) ke satu folder sebagai `harga_A.csv`, `harga_B.csv`, `harga_idx.csv`.
3. `python3 WFO/kod/tala_semula.py data <folder>`; catat bar baharu dan ticker yang tidak disambung.
4. Bagi setiap benih 42, 1042, 2042: `python3 WFO/kod/tala_semula.py jalan <label> <benih>` dengan Bash run_in_background (timeout 7200000). Satu larian berhenti melancar selepas ~70 minit; ulang arahan yang sama sehingga tiada BELUM (hasil disambung). Jalankan satu benih pada satu masa.
5. `python3 WFO/kod/tala_semula.py cadang <label>` → `WFO/cadangan/<label>.md` + `.json`.
6. Commit `Tala semula <label>: <n> cadangan lulus pengawal` (fail cadangan sahaja; `WFO/data/tala/` diabaikan git) dan push ke `main`.
7. PushNotification: "Cadangan tala <label>: <n> kaedah lulus pengawal. Semak WFO/cadangan/<label>.md dan balas kaedah yang diluluskan."

Selepas pengguna meluluskan (sesi berasingan): `python3 WFO/kod/tala_semula.py guna <label> Mxx ...` (M115–M161 sahaja),
kemudian `registry_baru.py`, ujian unit, `sahkan.py --betulkan`, commit + push `main`, bungkus dan muat naik aset kod dashboard
(`kod/README.md`), kemas kini `harian/status` → `harga_aset.kod`, catat dalam log.
