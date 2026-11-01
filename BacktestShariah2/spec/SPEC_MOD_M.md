# SPEC_MOD_M — pradaftar: tujuh varian SERAGAM merentas semua kaedah Mxx

**Dikomit SEBELUM sebarang keputusan dilihat.** Permintaan pengguna 1 Nov 2026 ("Analisis + tambah
varian baharu"). Bukti yang mencetuskan spec ini: `laporan/MODIFIKASI_KAEDAH.md`
(`standard/modifikasi_kaedah.py`).

Varian di sini **belum dijalankan**. Tiada nombor hasil, tiada dakwaan. Varian aktif setiap kaedah
TIDAK ditukar; papertrade dan Lejar Penuh berjalan seperti biasa.

---

## 1. Mengapa ini bukan ulangan W01

`WFO/laporan/W01_LAPORAN.md` sudah menala henti/keluar/tmax **setiap kaedah setiap suku**
(Optuna 150 percubaan x 16 suku x 132 kaedah) dan hasilnya: versi WFO mengalahkan varian bekunya
sendiri hanya **52/131**, purata delta CAGR **-6.4 mata** (t -3.63, p 0.0004). Sebabnya diukur dalam
§5 laporan itu: menukar bajet carian Optuna mengubah CAGR dengan beza mutlak median 5.4 mata.
**Penalaan per-kaedah ialah hingar.**

Spec ini berbeza secara JENIS, bukan darjah: **satu** peraturan dipakai kepada **semua** kaedah,
tanpa penalaan, tanpa pemilihan. Bilangan keputusan bebas turun daripada 132 x 16 x 4 parameter
kepada **lapan**. Itu satu-satunya bentuk yang sampel ini ada kuasa untuk menyelesaikan.

Arah setiap varian datang daripada tiga ukuran bebas yang **semuanya menunjuk arah sama**:

| Ukuran | Alam | Arah |
|---|---|---|
| W01 WFO pilihan luar sampel, 2,096 pilihan | 423 saham, 2023–2026 | henti lebih LEBAR (ATR 2.887x lawan 2.75x seragam, p 2.0e-06; PCT 10.84% lawan 10.2%, p 7.5e-08); ekori longgar (CHAN4 2.32x terlebih pilih, CHAN2/EMA10 0.13x/0.11x); tmax lebih PANJANG (pangkat 3.681 lawan 3.0, p 4.6e-128) |
| `REVERSE/NXX_KELUAR.md` | 4,420,650 bar, 2020–2025 | tiga keluar terbaik daripada 23 semuanya "pegang sampai momentum habis": `X13` RSI>70 +4.350%, `X15` Chandelier 4xATR +3.706%, `X17` ADX<20 +1.855%; dua terburuk kedua-duanya memotong awal |
| lengkung `pegang` registry | 619,786 dagangan backtest | pegang 60 hari mengalahkan mesin keluar kaedah pada **75/75** kaedah swing, +4.37 mata setiap dagangan |

---

## 2. Varian (awalan `Z` — belum pernah diguna dalam registry; V/P/U/B sudah diambil)

Semua `Z` dibina **atas varian aktif setiap kaedah**, menukar satu perkara sahaja kecuali `Z6`/`Z7`.

| ID | Perubahan | Kaedah terjejas | Asal arah |
|---|---|---|---|
| `Z1a` | buang sasaran **jarak-tetap** (`g['tgt'] = np.nan`) | **1**: `M02` (3R daripada henti) | `NXX_KELUAR` X10 (jarak tetap 2%) menang 94.1% jangkaan -0.023%; `KOMBINASI` X1 (1xATR) -0.281% lawan asas +2.595% |
| `Z1b` | buang sasaran **paras-struktur** | **9**: `M01` SMA30 · `M03` jalur BB atas · `M18` ATH · `M19` tinggi 20h · `M20` paras dikunci · `M26` paras isyarat · `M28` VWAP · `M47` puncak terdahulu · `M100` gerakan terukur | **Lengan berasingan, dan saya jangka ia GAGAL.** Bukti yang menghukum sasaran semuanya mengenai jarak TETAP; keluar berasaskan paras/penunjuk justeru yang TERBAIK (`X13` rsi14>70 +4.350%, `X12` jalur bawah BB +0.961%). Menyatukan `Z1a` dan `Z1b` akan menyembunyikan dapatan. |
| `Z2` | buang had masa (`TMAX = None`) | **33** yang ada tmax | WFO tmax panjang/tiada 81.5% suku |
| `Z3` | ganti syarat keluar dengan ekori Chandelier 4xATR14 (paras hanya naik; `exitc = tutup < tertinggi_sejak_beli − 4×ATR14`) | **semua 134** | CHAN4 mod luar sampel pada 33 kaedah; `X15` +3.706% |
| `Z4` | lebarkan henti satu langkah: pengganda ATR x1.5, peratus x1.5, lookback LOW x2 | **semua 134** (129 ada henti) | ATR p 2.0e-06, PCT p 7.5e-08 |
| `Z5` | ganti syarat keluar dengan `rsi14 > 70` (keluar atas KEKUATAN) | **semua 134** | `X13` ialah keluar TERBAIK daripada 23 (+4.350%) dan **tiada dalam set pilihan W01** — jurang yang belum pernah diuji pada kaedah Mxx |
| `Z6` | `Z1a` + `Z2` + `Z3` serentak (pakej "pegang sampai momentum habis") | **semua 134** | gabungan tiga arah; diuji berasingan supaya interaksi boleh dilihat |
| `Z7` | KAWALAN: entry kaedah tidak berubah, tiada henti, tiada sasaran, tiada syarat keluar, keluar pada bar ke-60 | **semua 134** | siling lengkung `pegang`; memberi nilai maksimum yang boleh dicapai dengan memanjangkan pegangan sahaja |

`Z7` bukan calon dagangan (tiada henti = tiada had kerugian). Ia **penanda aras**: jika `Z6` tidak
menghampiri `Z7`, mesin keluar masih memotong; jika `Z6` ≈ `Z7`, maka seluruh kelebihan ialah masa
pegangan dan tiada peraturan keluar yang perlu dicari.

---

## 3. Alam, tempoh, pecahan

- Alam: set 431 (sama seperti registry) untuk perbandingan terus dengan varian aktif.
- Enjin: v1.2 beku. Kos 0.1% setiap belah. Portfolio 8 slot, konvensyen `enjin.metrik`.
- **LATIH 1 Nov 2019 – 31 Dis 2022** · **TAHAN 1 Jan 2023 – 2 Okt 2026**. Varian aktif dipilih
  dengan melihat 2019–2026, jadi tingkap TAHAN bukan luar sampel tulen untuk ASAS; ia luar sampel
  untuk `Z1`–`Z7` kerana tiada satu pun pernah dilihat. Dinyatakan supaya tidak terlebih dakwa.
- Semakan kedua: AUTOTUNE 2000 saham AS 2013–Sep 2024 (alam dan tempoh yang tidak pernah dilihat).
  Ini yang 0/134 kaedah lulus setakat ini; ia gate paling menuntut.

## 4. Gate (ditetapkan sekarang, tidak boleh dilonggarkan selepas melihat hasil)

| Gate | Syarat | Mengapa |
|---|---|---|
| **0** | **jangkaan mutlak > 0** pada tingkap TAHAN | Pelajaran `NXX.md`: `N16`x`X1` lulus gate lift dan FDR dengan menang 62.4% tetapi jangkaan -0.088% kerana asasnya -0.281%. Lift positif atas asas negatif masih rugi. |
| **1** | median lift atas varian aktif > 0 pada **kedua-dua** LATIH dan TAHAN | satu tingkap ialah satu cabutan |
| **2** | BH-FDR q ≤ 0.05, m = 7 varian x bilangan kaedah terjejas | 8 x 134 = sampai 1,072 ujian; m mesti dikira penuh |
| **3** | jangkaan selepas buang 5% dagangan terbaik **> asas yang sama** | Gate yang membunuh setiap dapatan terdahulu (`SETUP.md` 0/598, `SILANG_GATE_C.md`, `NXX.md`). Dinyatakan sebagai "> asas", bukan "> 0". |
| **4** | portfolio: CAGR > **SPUS 17.95%** DAN MDD ≥ **-26.82%** pada 2020–2025 | `REVERSE/PENANDA_ARAS_SYARIAH.md`. SPY BUKAN penanda aras; repo menapis melalui SPUS. |
| **5** | nisbah `CAGR ÷ abs(MDD)` > **0.669** | `SISTEM.md`: campuran SPUS+tunai memberi nisbah hampir pemalar 0.642–0.669 merentas setiap berat. Perubahan yang hanya menurunkan pulangan dan MDD bersama-sama **tidak** menambah apa-apa. |

**Gate 4 dan 5 adalah yang penting.** Gate 0–3 boleh lulus sambil masih kalah kepada memegang satu
ETF — itu yang berlaku dalam setiap kajian repo setakat ini.

## 5. Jangkaan priori saya

Direkod kerana repo menjejaki ketepatannya, dan rekod itu buruk: **salah pada 2/3 gate dalam
`SPEC_SILANG` §7, `SPEC_SISTEM` §7, `SPEC_NXX` bahagian A, dan salah ke arah BERTENTANGAN dalam
`NXX_KELUAR` bahagian B.** Empat pradaftar, empat kali tersalah. Maka jangkaan di bawah patut
diabaikan memihak kepada ukuran; ia dicatat hanya supaya ia tidak boleh ditulis semula kemudian.

| Gate | Jangkaan |
|---|---|
| 0 | 4–6 daripada 8 lengan lulus (arah disokong tiga ukuran bebas) |
| 1 | 3–5 lulus |
| 2 | 2–4 lulus |
| 3 | **0–1 lulus** — ini ramalan utama saya, dan ia ramalan kegagalan |
| 4 | **0 lulus** |
| 5 | **0 lulus** |

Alasan ramalan kegagalan gate 3–5: `MODIFIKASI_KAEDAH.md` §2 sudah mengukur bahawa kelebihan
pegang-lebih-lama ialah **masa, bukan alfa** — kadar setiap hari +0.1021% (pegang 60) lawan
+0.1047% (mesin kaedah), ujian-t berpasangan p 0.50, dan mesin kaedah sebenarnya sedikit di
HADAPAN. Jika kadar setiap unit masa tidak berubah, pulangan portfolio tidak sepatutnya berubah.
Nombor yang akan memalsukan ramalan itu: `Z6` memberi CAGR portfolio > 17.95% dengan MDD lebih
cetek daripada -26.82%.

## 6. Apa yang memalsukan spec ini sepenuhnya

Jika `Z7` (siling: entry sama, pegang 60 hari, tiada henti) tidak mengalahkan varian aktif pada
jangkaan setiap dagangan, maka lengkung `pegang` dalam registry salah dibaca dan seluruh spec ini
gugur. Itu semakan pertama yang mesti dijalankan, dan ia murah.

## 7. Cara jalan (belum dijalankan)

```
# 1. semakan pemalsuan dahulu (murah): Z7 sahaja
python3 WFO/kod/...  # skrip varian Z belum ditulis
# 2. Z1..Z6 atas set 431, LATIH + TAHAN
# 3. baris keputusan -> kod/registry/<ID>.csv dan data/registry_M_gabung.csv
#    (varian baharu sahaja; jangan tukar varian aktif tanpa keputusan pengguna)
```

**Status: PRADAFTAR SAHAJA. Tiada varian Z dijalankan pada 1 Nov 2026.**
