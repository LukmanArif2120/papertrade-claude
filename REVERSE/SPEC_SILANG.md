# SPEC SILANG-KELUARGA — pradaftar, 29 Okt 2026

**Dikomit SEBELUM apa-apa keputusan dilihat.** Satu tembakan. Tiada pelarasan selepas melihat hasil.

Keputusan pengguna 29 Okt 2026: uji kombinasi silang-keluarga.

## 1. Soalan

Fasa 1 menguji konteks **harga** sahaja (101 signal tunggal + 120 kombinasi pemicu × konteks
harga = 20,640 ujian ENTRY). Fasa 2 menguji **fundamental SEC** sahaja (20 signal, 12 daripadanya
kombinasi fundamental × masa earnings). **Tiada satu ujian pernah menggabungkan kedua-dua
keluarga.** Itu bahagian tugasan asal yang belum disiapkan.

> **Adakah konteks harga × fundamental SEC membawa maklumat yang TIADA pada mana-mana keluarga
> secara berasingan?**

Hipotesis arahan asal ("maklumat magnitud terletak pada KONTEKS ketika pemicu menyala") telah
**disokong** oleh fasa 1 — konteks membawa maklumat magnitud, pemicu tidak. Yang gagal ialah
**kestabilan**: 0 signal mengekalkan kelas penemuannya dalam kesemua 6 tahun. Ujian ini menanya
sama ada konteks fundamental menstabilkan konteks harga, atau sebaliknya.

**Ini ujian signal TERAKHIR.** Jika ia ditolak, ruang signal ditutup: harga (fasa 1), fundamental
(fasa 2), dan silang (ini) kesemuanya diukur.

## 2. Populasi

- `REVERSE/sec_join.csv` — 161,204 peristiwa sah, 2012–2025, alam Release `autotune-data-a02`.
  Peristiwa sah = tutup ≥ 5% atas rendah 20 hari DAN tutup > EMA21, hari pertama dalam ≤ 10 sesi.
- Lajur SEC sudah dilekatkan secara as-of (titik-masa, had basi 120 hari).
- Lajur harga dikira pada tarikh peristiwa yang SAMA dengan `REVERSE/teras/ind.py kira()`,
  tiada pandang hadapan.
- Ambang liputan §9.7 fasa 2 dikekalkan: tahun dengan < 3,000 peristiwa dikecualikan daripada
  pengangka DAN penyebut kekonsistenan.

## 3. Grid — tepat 48 kombinasi silang

**Konteks harga (6 lajur × 2 hujung = 12).** Keenam-enam ini ialah konteks yang fasa 1 sendiri
kenal pasti sebagai terbaiknya. Ia **tidak dicari semula** di sini:

`atr_pct` · `julat20` · `bb_lebar` · `cerun_ma50` · `j_ma200` · `j_52w_tinggi`

Setiap satu sebagai `q5:` (≥ persentil 80) dan `q1:` (≤ persentil 20).

**Syarat SEC (4).** Keempat-empat ini ialah yang fasa 2 sendiri kenal pasti. Ia **tidak dicari
semula**:

| Syarat | Mengapa ia dalam senarai |
|---|---|
| `q5:pecutan_hasil&sejak_earnings_le5` | satu-satunya yang lulus §5.3 fasa 2 (PEAD, lift 1.330) |
| `q5:pecutan_hasil` | induk tunggal bagi yang di atas |
| `q5:tumbuh_hasil` | satu-satunya yang lulus §5.1 fasa 2 |
| `q5:sue` | lajur ketiga, disertakan supaya keluarga tidak dipilih selepas fakta |

12 × 4 = **48 kombinasi**. Grid ini **tidak akan dilebarkan**. Tiada pengoptimum, tiada carian,
tiada Optuna (`ARAHAN`).

Sempadan kuintil harga **dibekukan pada larian pertama** ke `REVERSE/.cache/kuintil_harga.json`,
sama seperti `kuintil_sec.json` fasa 2 §9.4.

## 4. Keluaran yang dinilai

`pul_henti2atr` fasa 1 tanpa perubahan: masuk pada buka esok + kos sisi, henti keras
−2×ATR14, ufuk 63 sesi, kos sisi keluar. Kos: `REVERSE/teras/kos.py`.

## 5. Gate — ketiga-tiga diperlukan

### Gate A — statistik (sama seperti fasa 2 §5.3, supaya setara)

1. `n` ≥ 200
2. Kekonsistenan tahunan ≥ **71%** tahun dinilai, dengan ≥ **10** tahun dinilai
3. Permutasi label dalam-bulan, 1000 kali → nilai-p
4. **BH-FDR q ≤ 0.01** merentas kesemua 48 (satu keluarga)
5. Jangkaan > 0 **selepas membuang 5% pemenang teratas**
6. Bootstrap blok ikut **ticker** DAN ikut **minggu** kedua-duanya positif

### Gate B — superaditif (ini soalan sebenarnya)

`lift(silang)` > **kedua-dua** `lift(induk harga sahaja)` dan `lift(induk SEC sahaja)`.

Tanpa gate ini, satu kombinasi boleh lulus Gate A hanya kerana induk yang lebih kuat menembusi
— dan itu sudah diukur oleh fasa 1 dan 2. Gate B menguntukkan soalan "maklumat yang TIADA pada
mana-mana keluarga berasingan".

### Gate C — portfolio

Median 20 benih mengalahkan **SPUS** pada **pulangan DAN MDD**, 2020–2025, dengan kos penuh.
Penanda aras SPUS wajib (`PENANDA_ARAS_SYARIAH.md`); SPY rujukan sahaja. Kedua-dua konvensyen
SPUS dilaporkan (median tahunan dan CAGR tingkap) dan keputusan mesti bertahan pada kedua-duanya
(`PEMBINAAN.md`).

20 benih kerana hingar pemilihan = 17.3 mata peratus setahun (`KEPEKATAN_BENIH.md`); satu larian
ialah satu cabutan dan tidak boleh ditafsir.

## 6. Keputusan

**DITERIMA** hanya jika ≥ 1 kombinasi lulus Gate A **dan** Gate B **dan** Gate C.

Jika kombinasi lulus A dan B tetapi gagal C, itu dilaporkan sebagai **maklumat silang-keluarga
WUJUD tetapi tidak mencukupi** — hasil yang berbeza daripada penolakan penuh, dan mesti
dinyatakan sebagai begitu.

Jika tiada kombinasi lulus A: **DITOLAK**, dan ruang signal ditutup sepenuhnya.

Keputusan **tidak** bergantung pada: nisbah pulangan/MDD, Sharpe, lift sahaja, atau apa-apa
ukuran yang tidak disenaraikan.

## 7. Jangkaan priori (ditulis sebelum larian)

Saya menjangka **DITOLAK pada Gate B**, atas empat sebab yang sudah diukur:

1. Fasa 1: tiada konteks harga mengekalkan kelas penemuan dalam kesemua 6 tahun; yang terbaik
   semuanya konteks pengembangan kemeruapan — kohort paling tercemar oleh ketiadaan saham delist.
2. Fasa 2: 1 daripada 20 sahaja bertahan, dan portfolionya memberi 0% bulan ≥ +10%.
3. `KOLAM_EKOR.md`: signal mesti menambah ≥ 1.00 mata sebulan hanya untuk seri dengan SPY, dan
   SPUS lebih tinggi lagi.
4. Interaksi dalam data kewangan biasanya **subaditif**, bukan superaditif: mensyaratkan dua
   keadaan mengecilkan `n` sementara keadaan itu sendiri berkorelasi, jadi lift jarang melebihi
   induk terkuat.

Sebab 4 ialah yang paling kuat dan ia menyasarkan tepat Gate B.

Jangkaan ini direkodkan supaya ia tidak boleh dilaraskan selepas fakta. Jika hasilnya LULUS,
jangkaan saya salah dan itu mesti dinyatakan dengan jelas dan menonjol.

## 8. Apa yang ujian ini TIDAK boleh buktikan

- Ia tidak boleh mencapai **+10%/bulan** (`SASARAN.md`). Soalan itu sudah dijawab.
- LULUS bermakna "kombinasi silang mengalahkan SPUS dalam backtest 2020–2025" — ia **mesti**
  disahkan ke hadapan sebagai lorong `portfolio_slot/` dengan jalur benih sebelum dipercayai.
- Ia tidak menguji kaedah Mxx. REVERSE menguji signal/indikator (`CLAUDE.md`).
