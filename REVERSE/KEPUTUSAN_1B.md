# KEPUTUSAN FASA 1B — saiz dan henti berskala kemeruapan (2020–2025)

Dijana `REVERSE/jana_keputusan_1b.py`. Spec dikunci sebelum larian: `SPEC_1B.md`.

> Had diakui lebih awal (SPEC_1B §4): 1b menggunakan enam tahun yang **sama** seperti fasa 1 dan ideanya dipilih **selepas** melihat hasil fasa 1. Keputusan tertinggi 1b ialah **CALON**.


## 1. Asas perbandingan setiap tahun

|   tahun | asas_ketat_sistem        |   asas_ketat_pul |   asas_ketat_mdd |   asas_median_pul |   asas_median_mdd |   rawak1b_pul |   rawak1b_mdd |   spy_pul |   spy_mdd |
|--------:|:-------------------------|-----------------:|-----------------:|------------------:|------------------:|--------------:|--------------:|----------:|----------:|
|    2020 | hari_agihan|X=15%,Y=ma50 |            93.71 |           -40.63 |             67.5  |            -40.63 |         49.28 |        -30.52 |     17.24 |    -33.72 |
|    2021 | REF_pegang_252           |            12.28 |           -22.16 |            -18.5  |            -46.05 |          3.39 |         -9.67 |     30.51 |     -5.11 |
|    2022 | REF_chandelier_4atr      |            -5.26 |           -37.88 |             -5.65 |            -34.22 |        -21.07 |        -22.69 |    -18.65 |    -24.5  |
|    2023 | REF_chandelier_4atr      |            56.37 |           -21.52 |             33.53 |            -19.61 |         16.05 |        -28.37 |     26.71 |     -9.97 |
|    2024 | hari_agihan|X=5%,Y=ema9  |            10.98 |           -29.4  |             -0.07 |            -30.48 |          9.9  |         -7.85 |     25.59 |     -8.41 |
|    2025 | REF_pegang_252           |           128.93 |           -38.71 |             -4.32 |            -41.05 |         16.58 |        -24.81 |     18.01 |    -18.76 |


## 2. Keputusan ambang dipradaftar


**Bacaan KETAT** — konfigurasi terbaik `1b|V1_maks8|risiko1.0%|k4` mengalahkan ketiga-tiga asas dalam **1 daripada 6** tahun (perlu ≥ 4). → **GAGAL**


| sistem                    |   tahun_lulus |
|:--------------------------|--------------:|
| 1b|V1_maks8|risiko1.0%|k4 |             1 |
| 1b|V1_maks8|risiko0.5%|k4 |             1 |
| 1b|V1_maks8|risiko0.5%|k3 |             0 |
| 1b|V1_maks8|risiko0.5%|k2 |             0 |
| 1b|V1_maks8|risiko1.0%|k2 |             0 |
| 1b|V1_maks8|risiko1.0%|k3 |             0 |


**Bacaan MEDIAN** — konfigurasi terbaik `1b|V1_maks8|risiko1.0%|k4` mengalahkan ketiga-tiga asas dalam **1 daripada 6** tahun (perlu ≥ 4). → **GAGAL**


| sistem                    |   tahun_lulus |
|:--------------------------|--------------:|
| 1b|V1_maks8|risiko1.0%|k4 |             1 |
| 1b|V1_maks8|risiko0.5%|k4 |             1 |
| 1b|V1_maks8|risiko0.5%|k3 |             0 |
| 1b|V1_maks8|risiko0.5%|k2 |             0 |
| 1b|V1_maks8|risiko1.0%|k2 |             0 |
| 1b|V1_maks8|risiko1.0%|k3 |             0 |


## 3. Keputusan 1b

**DITOLAK** — ambang dipradaftar TIDAK dipenuhi pada 0/2 bacaan asas.


## 4. Kesan sebenar saiz berskala risiko (di luar ambang)

- **2020**: MDD fasa 1 -54.3% … -29.4% → 1b -50.6% … -9.6%; pulangan fasa 1 30.8% … 93.7% → 1b -1.6% … 122.3%; median bulanan 1b terbaik 8.42%

- **2021**: MDD fasa 1 -52.6% … -22.2% → 1b -57.7% … -7.9%; pulangan fasa 1 -34.8% … 12.3% → 1b -50.0% … 14.9%; median bulanan 1b terbaik 1.13%

- **2022**: MDD fasa 1 -37.9% … -25.0% → 1b -45.7% … -9.0%; pulangan fasa 1 -20.0% … -5.3% → 1b -38.0% … -3.4%; median bulanan 1b terbaik 1.21%

- **2023**: MDD fasa 1 -21.8% … -17.2% → 1b -28.7% … -6.4%; pulangan fasa 1 21.1% … 56.4% → 1b 4.0% … 52.8%; median bulanan 1b terbaik 5.08%

- **2024**: MDD fasa 1 -50.3% … -25.3% → 1b -52.9% … -10.6%; pulangan fasa 1 -46.7% … 11.0% → 1b -48.5% … 7.7%; median bulanan 1b terbaik -0.93%

- **2025**: MDD fasa 1 -47.7% … -27.0% → 1b -41.2% … -9.2%; pulangan fasa 1 -31.8% … 128.9% → 1b -20.6% … 24.2%; median bulanan 1b terbaik 1.80%


Merentas 6 tahun, 108 konfigurasi-tahun 1b: purata pulangan **+2.83%**, purata MDD **-29.01%**, purata median bulanan **-0.06%**; **0** mencapai median ≥ +10% sebulan.


## 5. Apa yang 1b berjaya buat, dan apa yang tidak

**Berjaya: kawalan risiko.** MDD terbaik setiap tahun bertambah baik dalam **6 daripada 6** tahun. Contoh paling jelas: 2020 -29.4% → -9.6%; 2021 -22.2% → -7.9%; 2022 -25.0% → -9.0%; 2023 -17.2% → -6.4%; 2024 -25.3% → -10.6%; 2025 -27.0% → -9.2%. Menyamakan risiko setiap dagangan memang mengecilkan drawdown seperti yang dijangka — purata MDD jatuh daripada -35.12% (fasa 1) ke -29.01% (1b).


**Tidak berjaya: pulangan.** Purata pulangan tahunan +12.76% (fasa 1) → +2.83% (1b), dan median bulanan +0.91% → -0.06%. 0 daripada 108 konfigurasi-tahun mencapai sasaran +10% sebulan.


**Maknanya.** Saiz berskala risiko membetulkan **drawdown**, bukan **alpha**. Ia mengurangkan kerugian apabila signal salah, tetapi ia tidak boleh mencipta kelebihan yang tidak ada. Digabung dengan diagnosis fasa 1 — jangkaan setiap dagangan yang diperlukan 2–5 kali apa yang pernah diukur, dan korelasi pangkat terhadap pulangan boleh didagangkan ≈ 0 — ini mengukuhkan kesimpulan fasa 1 dan tidak melemahkannya: **tiada alpha untuk dipungut daripada indikator harga sahaja dalam reka bentuk ini.** Kawalan risiko yang lebih baik ialah penambahbaikan yang sah dan berguna, tetapi ia bukan jalan ke +10% sebulan.
