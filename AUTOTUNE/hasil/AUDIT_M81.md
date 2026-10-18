# AUDIT M81 — Bensdorp Long Trend High Momentum (AUTOTUNE A01)

Diaudit 18 Okt 2026. Skop: hasil luar biasa M81 dalam `LAPORAN.md` (OOS-A 66.6%, OOS-B 48.2%, tempoh kunci 192.2% lwn SPY 16.3%). Tiada kod atau hasil diubah; skrip audit dijalankan di luar repo atas data Release `autotune-data` (manifest sha256 sah).

## Keputusan: ARTIFAK

Prestasi M81 berpunca daripada **pandang ke hadapan dalam lajur `exitc`** (henti mengekor disimulasi dalam `_exit_ekor`). Data harga adalah betul; enjin mengira dengan betul mengikut input yang diberi; tetapi input `exitc` menggunakan harga rendah hari esok. Penala (Optuna) menolak `tt_kali_0_75` dari 0.75 ke 0.94–0.95 (henti mengekor ~5%), iaitu kawasan di mana kecacatan ini memberi untung paling besar. Apabila kecacatan dibuang, CAGR tempoh kunci jatuh daripada 192.6% kepada −25.6% (henti pada paras) atau 17.4% (keluar buka esok selepas tutup ≤ paras), iaitu ≈ SPY.

## 1. Jana semula dagangan (parameter `k12.json`, A+B, 2024-10-01 – 2026-10-16)
- Enjin: 26 278 dagangan calon (sama dengan `ujian_AB.n`), CAGR 192.6%, MDD −37.7% (laporan 192.2%/−37.7%; beza kecil = kaedah tahunan). Portfolio memegang 688 dagangan: 646 `isyarat keluar` (henti mengekor), 28 henti, 12 hujung, 2 masa. Menang 55.4%, purata +2.94%, median +1.07%.
- Sumbangan (amaun × pulangan, unit ekuiti awal): untung bersih 7.94. **5 teratas = 24.5% untung bersih** (9.9% untung kasar); 15 teratas = 54.7%. Semua 15 teratas berlaku pada 2026 (ekuiti sudah besar → kesan kompaun), jadi bukan satu dua dagangan bertuah yang menerangkan hasil.
- OOS k10 (2023) dan k11 (2024 Jan–Sep) juga dijana semula: k10 A 61.8% (JSON 61.6%), B 20.4%; k11 A 84.4% (JSON 84.0%), B 91.8%.

## 2. Integriti data — 8 dagangan teratas lwn Moomoo (`quote_history_kline`, hari, autype 1)

| # | Ticker | Masuk (buka) | Keluar (buka) | Hari | Pulangan enjin | Nisbah data kita | Nisbah Moomoo | Rendah hari keluar | Paras ekor | Pulangan jujur* |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SNDK | 2026-07-28 1173.60 | 2026-09-24 1785.47 | 42 | +51.7% | 1.5214 | 1.5214 | 1726.39 | 1787.74 | +51.7% |
| 2 | AXTI | 2026-04-27 71.91 | 2026-05-06 110.20 | 8 | +52.8% | 1.5325 | 1.5325 | 92.85 | 101.89 | +41.3% |
| 3 | SNDK | 2026-03-05 594.385 | 2026-04-14 964.02 | 28 | +61.7% | 1.6219 | 1.6219 | 902.00 | 902.38 | +51.4% |
| 4 | MRNA | 2026-09-11 137.905 | 2026-09-30 186.55 | 14 | +34.9% | 1.3527 | 1.3527 | 184.58 | 192.75 | +34.9% |
| 5 | SNDK | 2026-05-19 1289.75 | 2026-06-04 1741.31 | 12 | +34.6% | 1.3501 | 1.3501 | 1725.08 | 1735.13 | +34.1% |
| 6 | AXTI | 2026-09-14 59.68 | 2026-09-22 76.64 | 7 | +28.0% | 1.2842 | 1.2841 (76.635) | 74.90 | 75.72 | +26.5% |
| 7 | AXTI | 2026-02-05 17.61 | 2026-02-10 26.63 | 4 | +50.8% | 1.5122 | 1.5122 | 23.60 | 26.31 | +49.0% |
| 8 | AAOI | 2026-06-01 149.25 | 2026-06-03 200.50 | 3 | +33.9% | 1.3434 | 1.3434 | 180.55 | 191.72 | +28.1% |

\* keluar pada min(buka, paras ekor) pada hari yang sama, selepas kos.
- 9–15: AG 02-17→03-02 +43.4%; FRO 09-24→10-14 +25.7%; WDC 06-09→06-23 +23.9%; SNDK 01-26→02-04 +36.8%; ROIV 06-04→07-13 +22.0%; PL 03-03→04-13 +30.7%; AAOI 04-23→05-04 +26.7% (semua 2026, semua `isyarat keluar`).
- Harga buka/rendah kita sama dengan Moomoo hingga 2 titik perpuluhan (beza 0.005 pada AXTI = float32). Tiada artifak split/split songsang: |pulangan harian| maksimum sekitar dagangan 0.11–0.26 (saham momentum sebenar), volum Moomoo konsisten. **Ketidakpadanan data: 0/8.**

## 3. Pandang ke hadapan — ADA
- Kod: `AUTOTUNE/kaedah/M81.py::_exit_ekor` menanda `ex[j-1] = True` apabila `l[j] <= sp` (rendah hari j menembusi paras ekor); enjin (`enjin_at._trades`) lalu keluar pada **buka hari j**. Keputusan keluar pada buka j bergantung pada rendah j yang belum diketahui. Docstring asal sendiri menulis "AMARAN: exitc[j-1] bergantung pada rendah_j (pandang ke hadapan 1 hari)". Kesannya: setiap henti mengekor dijual pada buka (biasanya jauh di atas paras), bukan pada paras henti.
- Ujian potong (sedia() atas data dipotong lwn data penuh, parameter k12): `sig`, `stop`, `rank` = 0 beza pada ketiga-tiga tarikh. `exitc` berbeza pada tarikh potong itu sendiri: 2025-03-31 → 2 saham (HALO, JNJ), 2025-09-30 → 51, 2026-03-31 → 10 (benar dalam data penuh, palsu bila dipotong). Bukti langsung pandang ke hadapan.
- `rank` = ROC200 setiap saham (`close/close.shift(200)-1`), bukan merentas saham, tiada data masa depan. Tiada `shift(-…)` atau `center=True` dalam M81.

Simulasi semula (numba, isyarat/stop/topeng/kos sama dengan enjin; CAGR, MDD):

| Tetingkap | Kump. | Enjin | Tiruan pandang ke hadapan | Jujur: henti pada paras | Jujur: tutup ≤ paras → buka esok |
|---|---|---|---|---|---|
| k12 tala (tt 0.947) | AB | 192.6%, −37.7% | 199.6%, −18.6% | −25.6%, −56.4% | 17.4%, −43.4% |
| k12 tala | A / B | 120.7% / 40.9% | 143.1% / 107.1% | −16.7% / −35.7% | 16.6% / 29.7% |
| k10 tala (tt 0.939) | A / B | 61.8% / 20.4% | 68.3% / 11.1% | 7.4% / −29.4% | 3.2% / −7.2% |
| k11 tala (tt 0.946) | A / B | 84.4% / 91.8% | 80.9% / 68.0% | −20.3% / −32.6% | −4.5% / −10.1% |
| k12 PARAM asal (tt 0.75) | AB | 10.6%, −39.1% | 14.0% | −3.9% | 16.3% |

Purata pulangan dagangan k12 AB: enjin +1.99%, tiruan +1.85%, jujur paras −0.14%. Seluruh kelebihan = jurang buka − paras henti pada hari keluar. Tiruan tidak sama bait demi bait dengan enjin kerana jujukan dagangan `_exit_ekor` berjalan sejak WARM tanpa topeng universe/kumpulan dan memakai henti awal buka_masuk−k×ATR, manakala enjin memakai tutup_isyarat−k×ATR (jujukan boleh tidak segerak).

## 4. Semakan enjin (manual dari bar)
Tiga dagangan (AXTI 04-27, SNDK 03-05, AAOI 06-01): masuk = buka hari selepas isyarat, keluar = buka hari selepas `exitc`, kos 0.15% setiap sisi (komisen 0.1% + slip 0.05%, medv20 ≥ USD50 juta). Manual +52.79%, +61.70%, +33.94% = enjin tepat. Enjin betul; kecacatan dalam input `exitc`.

## 5. Tetapan asal (registry 431, `registry_M_gabung.csv`, enjin v1.2, 2019-11 → 2026-10)
M81 V4 (henti awal 3×ATR20 + ekor 25%): CAGR 27.97%, MDD −40.7%, 3630 dagangan, menang 31.9%, purata 105 hari pegang (SIMPAN). V1 24.6%/−45.8% (DITOLAK). Dengan ekor 25% kesan pandang ke hadapan kecil (k12 asal: enjin 10.6% lwn jujur-tutup 16.3%); kesan menjadi besar hanya selepas penalaan mengetatkan ekor ke ~5%.

## 6. Portfolio
Lengkung portfolio Python bebas = enjin (beza maksimum 0.0). Posisi serentak maksimum 8; tunai minimum 0.000000 (tidak pernah negatif); satu posisi setiap ticker. Tiada pendedahan mustahil.

## Pembetulan yang diperlukan (belum dibuat)
1. `AUTOTUNE/kaedah/M81.py` (dan sumber `BacktestShariah2/kod/kaedah/M81.py`): buang tanda `ex[j-1]` berasaskan `l[j]`. Pilihan A (setia buku, henti intrahari): tambah sokongan henti mengekor dalam `enjin_at._trades` — parameter `ekor` (cth. 0.947): `sp = max(st[i], ekor × max(e, c[i+1..j-1]))`; jika `o[j] <= sp` keluar `o[j]`, jika `l[j] <= sp` keluar `sp`. Pilihan B (tanpa ubah enjin): `ex[j] = True` jika `c[j] <= paras ekor` (keluar buka j+1).
2. Tala semula M81 (k00–k13) selepas pembetulan; jana semula `LAPORAN.md`, `gabungan.json`, `parameter_sedia.csv`. Sehingga itu M81 = ARTIFAK, keluarkan daripada portfolio gabungan dan parameter SEMASA (`tt_kali_0_75=0.9259`) TIDAK boleh diguna.
3. Tambah ujian unit potong-data untuk semua 134 kaedah: `sedia()` atas data dipotong pada beberapa tarikh mesti memberi `sig/stop/tgt/exitc/rank` sama dengan data penuh hingga tarikh potong. Kaedah lain yang memakai `shift(-1)` (cth. `bm = open.shift(-1)` dalam M02–M10 dll.) perlu lulus ujian ini.
4. Hadkan JULAT `tt_kali_0_75` (kini sehingga 0.99) atau tandakan kaedah yang mensimulasikan dagangan sendiri dalam `sedia()` sebagai berisiko pandang ke hadapan.
