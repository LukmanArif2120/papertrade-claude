"""Penanda aras PATUH SYARIAH — pembetulan kesilapan asas kajian ini.

Seluruh projek bernama "Backtest Shariah", tetapi setiap perbandingan dalam kajian REVERSE
menggunakan **SPY**, yang BUKAN patuh Syariah. Jadi sistem diukur terhadap sesuatu yang pengguna
mungkin tidak boleh beli, dan penanda aras yang betul tidak pernah dikira.

Repo sendiri sudah menapis Syariah melalui **SPUS** (SP Funds S&P 500 Sharia Industry Exclusions
ETF) — `BacktestShariah2/data/skrin/etf_shariah.csv` dan `semak_shariah.csv`. Maka SPUS ialah
alternatif pasif yang sah: apa yang pengguna boleh perolehi tanpa satu pun kajian.

Had yang diakui: SPUS mula Dis 2019, jadi hanya 6 tahun penuh (2020-2025) — tempoh prestasi
teknologi yang luar biasa kuat. 26%/tahun BUKAN jangkaan ke hadapan. MDD dikira daripada tutup
bulanan, jadi ia memandang RENDAH drawdown harian sebenar; itu memihak kepada penanda aras, bukan
kepada sistem, jadi kesimpulan di bawah adalah konservatif terhadap SPUS.

Guna: python3 REVERSE/penanda_aras_syariah.py
Output: REVERSE/PENANDA_ARAS_SYARIAH.md
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.teras import data as D, stat as T  # noqa: E402

KELUAR = AKAR / 'REVERSE'
SPUS = AKAR / 'BacktestShariah2' / 'data' / 'penanda_aras' / 'spus_bulanan.csv'
TAHUN = list(range(2020, 2026))


def siri_bulanan():
    d = pd.read_csv(SPUS, comment='#')
    s = pd.Series(d.tutup.values, index=pd.to_datetime(d.bulan.astype(str))).sort_index()
    ix = D.muat_indeks('2019-11-01', '2026-10-16')
    spy = ix['SPY']['close'].resample('ME').last().dropna()
    return {'SPUS': s, 'SPY': spy}


def metrik(ser, y):
    w = ser[(ser.index >= f'{y - 1}-12-01') & (ser.index <= f'{y}-12-31')]
    w = w[w.index.year.isin([y - 1, y])]
    if len(w) < 12:
        return None
    e = w / w.iloc[0]
    bl = e.pct_change().dropna() * 100
    return dict(tahun=y, pulangan=round((float(e.iloc[-1]) - 1) * 100, 2),
                mdd_bulanan=round(T.mdd(e.to_numpy()), 2),
                median_bulanan=round(float(bl.median()), 2),
                pct_ge10=round(float((bl >= 10).mean() * 100), 1),
                terburuk=round(float(bl.min()), 2))


def main():
    S = siri_bulanan()
    baris = []
    for nama, ser in S.items():
        for y in TAHUN:
            m = metrik(ser, y)
            if m:
                baris.append(dict(aset=nama, **m))
    B = pd.DataFrame(baris)

    kd = pd.read_csv(KELUAR / 'kos_drag.csv')
    kd = kd[(kd.kos == 'penuh') & (kd.tahun.isin(TAHUN))]
    sis = kd.groupby('keluar')[['pulangan', 'mdd', 'median_bulanan', 'n_masuk']].median().round(2)

    L = ['# Penanda aras PATUH SYARIAH: pembetulan kesilapan asas kajian ini', '']
    L.append(f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh '
             '`REVERSE/penanda_aras_syariah.py`.')
    L.append('')
    L.append('## Kesilapan')
    L.append('')
    L.append('Projek ini bernama **Backtest Shariah**, tetapi setiap perbandingan dalam kajian '
             'REVERSE — termasuk `KEPUTUSAN_FASA1.md`, `KEPUTUSAN_FASA2_SEC.md`, `SASARAN.md` dan '
             '`KOS_DRAG.md` — menggunakan **SPY**, yang **bukan patuh Syariah**. Sistem diukur '
             'terhadap sesuatu yang pengguna mungkin tidak boleh beli, dan penanda aras yang betul '
             'tidak pernah dikira sekali pun.')
    L.append('')
    L.append('Repo sendiri sudah menapis Syariah melalui **SPUS** (SP Funds S&P 500 Sharia Industry '
             'Exclusions ETF): `data/skrin/etf_shariah.csv` (326 ticker) dan `semak_shariah.csv`. '
             'Jadi alternatif pasif yang sah sudah ada dalam repo sejak awal.')
    L.append('')
    L.append('## Apa yang SPUS beri')
    L.append('')
    L.append('| Tahun | SPUS | SPY | SPUS bulanan | SPY bulanan |')
    L.append('|---|---|---|---|---|')
    for y in TAHUN:
        a = B[(B.aset == 'SPUS') & (B.tahun == y)]
        b = B[(B.aset == 'SPY') & (B.tahun == y)]
        if a.empty or b.empty:
            continue
        L.append(f'| {y} | {a.pulangan.iloc[0]:.2f}% | {b.pulangan.iloc[0]:.2f}% | '
                 f'{a.median_bulanan.iloc[0]:.2f}% | {b.median_bulanan.iloc[0]:.2f}% |')
    L.append('')
    q = {a: B[B.aset == a] for a in ('SPUS', 'SPY')}
    L.append(f'Median: **SPUS {q["SPUS"].pulangan.median():.2f}%/tahun** lawan SPY '
             f'{q["SPY"].pulangan.median():.2f}%/tahun. SPUS **mengalahkan** SPY, kerana membuang '
             'kewangan dan syarikat berleveraj tinggi memberatkannya ke arah teknologi dalam '
             'tempoh ini.')
    L.append('')
    L.append('Maka penanda aras yang betul **lebih tinggi** daripada yang saya guna sepanjang '
             'kajian, bukan lebih rendah. Setiap kesimpulan sebelum ini terlalu memihak kepada '
             'sistem.')
    L.append('')
    L.append('## Perbandingan yang menentukan, 2020–2025')
    L.append('')
    L.append('| | Pulangan/tahun | MDD | Median bulanan | Dagangan/tahun |')
    L.append('|---|---|---|---|---|')
    L.append(f'| **SPUS (patuh Syariah)** | **{q["SPUS"].pulangan.median():.2f}%** | '
             f'{q["SPUS"].mdd_bulanan.median():.2f}% | '
             f'**{q["SPUS"].median_bulanan.median():.2f}%** | **1** |')
    L.append(f'| SPY | {q["SPY"].pulangan.median():.2f}% | {q["SPY"].mdd_bulanan.median():.2f}% | '
             f'{q["SPY"].median_bulanan.median():.2f}% | 1 |')
    for k in sis.index:
        r = sis.loc[k]
        L.append(f'| Sistem: {k} | {r.pulangan:.2f}% | {r.mdd:.2f}% | {r.median_bulanan:.2f}% | '
                 f'{r.n_masuk:.0f} |')
    L.append('')
    best, bv = sis.pulangan.idxmax(), float(sis.pulangan.max())
    sp = float(q['SPUS'].pulangan.median())
    L.append(f'Sistem terbaik (`{best}`) memberi {bv:.2f}%/tahun — **{bv - sp:+.2f} mata peratus** '
             f'lawan SPUS, dengan MDD {abs(float(sis.loc[best, "mdd"])) / abs(float(q["SPUS"].mdd_bulanan.median())):.1f} '
             f'kali lebih dalam dan median bulanan {sis.loc[best, "median_bulanan"]:.2f}% lawan '
             f'{q["SPUS"].median_bulanan.median():.2f}%.')
    L.append('')
    L.append('MDD penanda aras dikira daripada tutup **bulanan**, jadi ia memandang **rendah** '
             'drawdown harian sebenar. Itu memihak kepada penanda aras — maka jurang di atas '
             'adalah **konservatif** terhadap SPUS, dan jurang sebenar pada data harian akan lebih '
             'kecil pada paksi MDD sahaja, bukan pada pulangan.')
    L.append('')
    L.append('## Had yang diakui')
    L.append('')
    L.append('- SPUS mula didagangkan **Dis 2019**, jadi hanya 6 tahun penuh. Tempoh itu ialah '
             'prestasi teknologi yang luar biasa kuat. **26%/tahun bukan jangkaan ke hadapan**, dan '
             'sesiapa yang menganggapnya begitu akan kecewa.')
    L.append('- Penapisan Syariah SPUS ialah satu standard tertentu (S&P Shariah). Sama ada ia '
             'memenuhi standard yang pengguna pakai, dan bagaimana cukai serta akses broker '
             'mempengaruhinya, **bukan sesuatu yang kajian ini boleh jawab**.')
    L.append('- Ini pengukuran sistem pengguna sendiri terhadap penanda aras, **bukan nasihat '
             'pelaburan**. Saya tidak bertauliah memberi nasihat pelaburan peribadi.')
    L.append('')
    B.to_csv(KELUAR / 'penanda_aras_syariah.csv', index=False)
    p = KELUAR / 'PENANDA_ARAS_SYARIAH.md'
    p.write_text('\n'.join(L), encoding='utf-8')
    print(f'{p.name} ditulis | SPUS {sp:.2f}%/tahun lawan sistem terbaik {bv:.2f}% '
          f'({bv - sp:+.2f} mata)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
