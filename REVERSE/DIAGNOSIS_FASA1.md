# DIAGNOSIS FASA 1 — di mana maklumat itu hilang

Dijana oleh `REVERSE/siling_pandangan_sempurna.py` dan `REVERSE/ujian_pangkat.py`, 28 Okt 2026.
Dua ujian ini **bukan** bahagian arahan v10. Ia ditambah selepas fasa 1 ditutup untuk menjawab
soalan pengguna: "macam mana nak cari signal yang saya nak?"

## 1. Siling pandangan sempurna — sasaran +10%/bulan ada dalam julat, tetapi hanya baru

```
Siling pandangan sempurna, portfolio 8 slot x 12.5%, kos penuh dua sisi

 tahun  n_dagangan  pulangan_tahun  median_bulanan  purata_bulanan  pct_bulan_ge10  bulan_terburuk  n_calon_setahun
  2020          50           597.6           11.20           19.12            50.0            1.34             2735
  2021          44           825.9           17.96           22.39            66.7            0.00             3309
  2022          52           373.8           10.96           14.38            50.0            0.07             3654
  2023          49           301.9            9.90           12.61            50.0            3.07             3093
  2024          48           367.2            9.27           14.32            50.0            1.09             3011
  2025          47           504.3           18.04           16.76            66.7            1.26             3091

Purata siling: pulangan 495.1%/tahun, median bulanan 12.89%
Tahun yang siling mencapai median >= +10%/bulan: 4/6
```

Portfolio 8 slot yang memilih **dengan sempurna** (antara run yang tarikh_sahnya hari itu, pilih
yang %_naik_dagang tertinggi; keluar tepat pada puncak) memberi median bulanan **9.3%–18.0%**,
purata **12.89%**. Jadi +10%/bulan **bukan** mustahil secara aritmetik — tetapi ia duduk hampir
pada siling itu sendiri. Step 9 sebenar mencapai purata median bulanan **0.91%**, iaitu kira-kira
**7% daripada nilai pemilihan yang ada**. Untuk +10%/bulan, 78% daripada siling perlu ditangkap.

## 2. Ujian pemangkatan — maklumat itu ADA, tetapi tidak boleh dipungut

```
n baris: (A) peristiwa yang menjadi run  vs  (B) semua peristiwa sah
  2020: A= 2135  B= 12858  (A ialah 17% daripada B)
  2021: A= 2213  B= 15259  (A ialah 15% daripada B)
  2022: A= 2732  B= 15440  (A ialah 18% daripada B)
  2023: A= 2350  B= 13642  (A ialah 17% daripada B)
  2024: A= 2088  B= 14151  (A ialah 15% daripada B)
  2025: A= 2306  B= 13998  (A ialah 16% daripada B)

(A) sasaran = puncak run induk (HINDSIGHT)
 indikator  rho_purata  rho_min  rho_maks konsisten
   stoch_k      -0.124   -0.209    -0.056        ya
   stoch_d      -0.112   -0.163    -0.078        ya
     cci20      -0.109   -0.167    -0.041        ya
 rs_spy_6b       0.079    0.022     0.163        ya
   j_ema21      -0.078   -0.139    -0.045        ya
     adx14      -0.074   -0.115     0.029     tidak
vol_n50_5h      -0.074   -0.184     0.009     tidak
nisbah_atr      -0.074   -0.208     0.024     tidak
  tanda konsisten 6/6 tahun: 7/30 | |rho| purata tertinggi: 0.124
  konsisten: stoch_k (-0.124), stoch_d (-0.112), cci20 (-0.109), rs_spy_6b (+0.079), j_ema21 (-0.078), vol_n50 (-0.066), pdi (-0.065)

(B) sasaran = pulangan boleh didagangkan (KAUSAL)
   indikator  rho_purata  rho_min  rho_maks konsisten
     atr_pct      -0.251   -0.445     0.096     tidak
     julat20      -0.211   -0.378     0.074     tidak
    bb_lebar      -0.182   -0.326     0.072     tidak
j_52w_tinggi       0.137   -0.072     0.257     tidak
      j_ema9      -0.096   -0.200     0.025     tidak
     stoch_d       0.052   -0.035     0.087     tidak
     stoch_k       0.051   -0.054     0.098     tidak
       cci20       0.049   -0.042     0.084     tidak
  tanda konsisten 6/6 tahun: 1/30 | |rho| purata tertinggi: 0.251
  konsisten: j_ema21 (-0.027)
```

Kajian REVERSE menguji **kehadiran** signal (nyala/tidak). Ia tidak pernah menguji
**pemangkatan**: antara ~14,000 peristiwa sah setahun, yang mana 8 untuk slot? Ujian ini
menanya soalan itu dengan korelasi pangkat Spearman, terhadap dua sasaran berbeza.

**Sasaran (A) puncak run induk** — hanya 15–18% peristiwa yang memang menjadi run, jadi
pengiraan ini bersyarat pada hindsight. Di sini **7 daripada 30** indikator mempunyai tanda yang
konsisten kesemua enam tahun, dengan arah yang masuk akal: `stoch_k` (−0.124), `stoch_d`
(−0.112), `cci20` (−0.109), `j_ema21` (−0.078), `vol_n50` (−0.066), `pdi` (−0.065) semuanya
**negatif**, dan `rs_spy_6b` (+0.079) **positif**. Maknanya: antara calon yang sudah mencetus,
pilih yang **paling belum terlanjur** (stokastik rendah, dekat EMA21, tanpa lonjakan volum)
tetapi yang kekuatan relatif 6 bulannya kuat. Itu bertentangan dengan mengejar.

**Sasaran (B) pulangan yang boleh didagangkan** — semua peristiwa sah, henti −2×ATR dan kos
dikenakan. Di sini hanya **1 daripada 30** konsisten, dan nilainya −0.027 (bersamaan sifar).

### Mengapa (A) dan (B) berbeza — dan itulah jawapannya

Lihat `atr_pct` dalam (B): rho purata **−0.251**, julat −0.445 hingga +0.096. Dalam Step 4,
kuintil ATR% tertinggi ialah signal berlift tertinggi bagi hasil PADU — ia memang memilih saham
yang bergerak besar. Tetapi terhadap pulangan yang boleh didagangkan, ia berkorelasi **negatif
dengan kuat**: dengan henti −2×ATR dan slippage, nama berkemeruapan tinggi dihentikan lebih
kerap dan membayar kos lebih tinggi.

**Perkara yang memilih pergerakan besar ialah perkara yang sama yang menghalang anda memegangnya
sampai habis.** Itu menjelaskan sepenuhnya mengapa setiap portfolio yang dibina atas
`q5:atr_pct` dan `q5:julat20` kalah kepada entri rawak walaupun lift Step 4-nya 10–24 kali.

## 3. Implikasi untuk langkah seterusnya

Kekangan yang mengikat **bukan** kekurangan signal. Ia pembinaan dagangan di sekeliling signal:
saiz posisi tetap 12.5% dan henti tetap −2×ATR dikenakan sama rata kepada nama berkemeruapan
4% dan 15% sehari. Tiga perkara yang fasa 1 **tidak pernah** uji:

1. **Saiz posisi berskala kemeruapan** — slot lebih kecil + henti lebih luas untuk nama ATR
   tinggi, supaya risiko setiap dagangan sama. Boleh diuji dengan data yang sudah ada.
2. **Pengurusan pendedahan** — portfolio Step 9 terisi 7.8–7.9/8 slot **setiap tahun termasuk
   2022**. Tidak pernah ke tunai.
3. **Data titik-masa fasa 2** — RS rating, gred kumpulan, earnings/SEC (liputan sejarah 0%).
