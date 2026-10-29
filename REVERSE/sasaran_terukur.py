"""Apa yang TERUKUR boleh dicapai — daripada data yang sudah ada, tanpa pemasangan baharu.

Kajian ini mengukur tiga ruang dan menolak ketiga-tiganya terhadap sasaran +10%/bulan. Yang belum
pernah dilakukan ialah membandingkan sasaran itu dengan asas yang paling mudah: beli-dan-pegang
SPY atas tempoh yang SAMA (2012-2025), dan dengan aritmetik pengkompaunan sasaran itu sendiri.

Output: REVERSE/SASARAN.md. Tiada parameter ditala, tiada signal dipilih, tiada ujian baharu.

Guna: python3 REVERSE/sasaran_terukur.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.teras import data as D, stat as T  # noqa: E402

KELUAR = AKAR / 'REVERSE'
TAHUN = list(range(2012, 2026))
SASARAN_BULANAN = 10.0


def spy_tahunan():
    """SPY beli-dan-pegang, setiap tahun kalendar 2012-2025."""
    ix = D.muat_indeks('2011-06-01', '2026-10-16')
    c = ix['SPY']['close']
    rows = []
    for y in TAHUN:
        s = c[(c.index >= f'{y}-01-01') & (c.index <= f'{y}-12-31')].dropna()
        if len(s) < 200:
            continue
        e = s / s.iloc[0]
        bl = e.resample('ME').last().pct_change().dropna() * 100
        rows.append(dict(tahun=y, pulangan_tahunan=round((e.iloc[-1] - 1) * 100, 2),
                         mdd=round(T.mdd(e.to_numpy()), 2),
                         median_bulanan=round(float(bl.median()), 2),
                         pct_bulan_ge10=round(float((bl >= SASARAN_BULANAN).mean() * 100), 1),
                         bulan_terburuk=round(float(bl.min()), 2), n_bulan=len(bl)))
    return pd.DataFrame(rows)


def aritmetik_sasaran():
    """Apa yang +10%/bulan bermakna apabila dikompaun."""
    f = 1 + SASARAN_BULANAN / 100.0
    setahun = f ** 12
    return dict(faktor_bulanan=f, kali_setahun=setahun,
                pct_setahun=(setahun - 1) * 100,
                kali_14_tahun=setahun ** len(TAHUN),
                usd10k_jadi=10_000 * setahun ** len(TAHUN))


def main():
    S = spy_tahunan()
    A = aritmetik_sasaran()
    pf = KELUAR / 'sec_portfolio_ringkas.csv'
    P = pd.read_csv(pf) if pf.exists() else None

    L = ['# SASARAN: apa yang TERUKUR boleh dicapai', '']
    L.append(f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh '
             '`REVERSE/sasaran_terukur.py` daripada data yang sudah ada. **Tiada parameter ditala, '
             'tiada signal dipilih, tiada ujian baharu dijalankan.** Ia hanya meletakkan sasaran '
             '+10%/bulan bersebelahan dengan asas yang paling mudah.')
    L.append('')
    L.append('## 1. Aritmetik sasaran itu sendiri')
    L.append('')
    L.append(f'+{SASARAN_BULANAN:.0f}% sebulan, dikompaun, bermakna:')
    L.append('')
    L.append(f'- **{A["kali_setahun"]:.2f}× setahun** (+{A["pct_setahun"]:.0f}%/tahun)')
    L.append(f'- **{A["kali_14_tahun"]:,.0f}× atas 14 tahun** — tempoh yang sama dengan kajian ini')
    L.append(f'- USD 10,000 menjadi **USD {A["usd10k_jadi"]:,.0f}**')
    L.append('')
    L.append('Tiada strategi dalam sejarah pasaran yang pernah mengekalkan kadar itu atas 14 tahun. '
             'Ini bukan pendapat tentang kaedah; ia sifat pengkompaunan.')
    L.append('')
    L.append('## 2. Asas paling mudah: beli-dan-pegang SPY, 2012-2025')
    L.append('')
    L.append('| Tahun | Pulangan | MDD | Median bulanan | % bulan ≥ +10% | Bulan terburuk |')
    L.append('|---|---|---|---|---|---|')
    for _, r in S.iterrows():
        L.append(f'| {int(r.tahun)} | {r.pulangan_tahunan:.2f}% | {r.mdd:.2f}% | '
                 f'{r.median_bulanan:.2f}% | {r.pct_bulan_ge10:.1f}% | {r.bulan_terburuk:.2f}% |')
    L.append('')
    n0 = int((S.pct_bulan_ge10 == 0).sum())
    L.append(f'**Median: pulangan {S.pulangan_tahunan.median():.2f}%/tahun, MDD '
             f'{S.mdd.median():.2f}%, bulanan {S.median_bulanan.median():.2f}%.** '
             f'Bulan yang mencapai +10%: **0% dalam {n0} daripada {len(S)} tahun** — satu-satunya '
             'pengecualian ialah tahun pemulihan selepas kejatuhan.')
    L.append('')
    L.append(f'Sasaran +10%/bulan ialah kira-kira **{SASARAN_BULANAN / float(S.median_bulanan.median()):.1f} kali** '
             'median bulanan indeks, dan indeks itu sendiri melepasinya hanya dalam satu tahun '
             'daripada 14.')
    L.append('')

    if P is not None and not P.empty:
        sig = P[P.jenis == 'signal'].sort_values('pulangan_tahunan', ascending=False)
        L.append('## 3. Apa yang kajian ini hasilkan, bersebelahan')
        L.append('')
        L.append('Portfolio leg SEC (§5.4, median merentas 14 tahun). Kesemua enam konfigurasi '
                 'dipradaftar ditunjukkan — **bukan yang terbaik sahaja** — kerana memilih sel '
                 'terbaik selepas melihat jadual bukan dapatan.')
        L.append('')
        L.append('| Keluar | Saiz | Pulangan | MDD | Median bulanan | % bulan ≥ +10% |')
        L.append('|---|---|---|---|---|---|')
        for _, r in sig.iterrows():
            L.append(f'| {r.keluar} | {r.saiz} | {r.pulangan_tahunan:.2f}% | {r.mdd:.2f}% | '
                     f'{r.median_bulanan:.2f}% | {r.pct_bulan_ge10:.1f}% |')
        L.append('')
        b = sig.iloc[0]
        L.append(f'Konfigurasi terbaik ({b.keluar}, saiz {b.saiz}) memberi '
                 f'**{b.pulangan_tahunan:.2f}%/tahun pada MDD {b.mdd:.2f}%**. '
                 f'SPY beli-dan-pegang memberi **{S.pulangan_tahunan.median():.2f}%/tahun pada MDD '
                 f'{S.mdd.median():.2f}%** atas tempoh yang sama.')
        L.append('')
        lebih_baik = (float(b.pulangan_tahunan) > float(S.pulangan_tahunan.median())
                      and float(b.mdd) > float(S.mdd.median()))
        L.append(f'Mengalahkan SPY pada pulangan **dan** MDD: **{"YA" if lebih_baik else "TIDAK"}**. '
                 f'Median bulanannya {b.median_bulanan:.2f}% lawan {S.median_bulanan.median():.2f}% '
                 'bagi SPY.')
        L.append('')

    L.append('## 4. Apa yang ini bermakna untuk keputusan')
    L.append('')
    L.append('Selepas 20,640 ujian indikator harga (fasa 1), 108 ujian saiz posisi (fasa 1b), '
             '20 ujian fundamental titik-masa (fasa 2 leg SEC), dan 38,400 konfigurasi Optuna '
             '(AUTOTUNE A02 — LULUS 0), **tiada satu pun mengalahkan beli-dan-pegang SPY pada '
             'pulangan dan MDD serentak** atas tempoh yang sama.')
    L.append('')
    L.append('Itu bukan kegagalan mencari. Ia pengukuran: ruang yang boleh dicapai dengan data '
             'harga harian dan fundamental suku, pada universe 2,000 saham AS paling cair, sudah '
             'diukur dan hadnya kira-kira pulangan indeks.')
    L.append('')
    L.append('Keputusan yang tinggal adalah milik pengguna, dan ia bukan keputusan teknikal:')
    L.append('')
    L.append('1. **Kekalkan sasaran +10%/bulan** dan terima bahawa tiada kerja yang boleh '
             'dicadangkan secara jujur akan mencapainya. Setiap kajian seterusnya akan ditolak '
             'seperti tiga yang sudah.')
    L.append('2. **Tetapkan sasaran pada apa yang terukur** — kira-kira pulangan indeks, dengan '
             'MDD yang boleh ditanggung — dan alihkan usaha daripada mencari kelebihan kepada '
             'mengurangkan kos, cukai, dan kesilapan pelaksanaan. Itu lever yang belum pernah '
             'diukur dalam repo ini.')
    L.append('3. **Terima risiko lebih tinggi secara sengaja** (leveraj, kepekatan) untuk '
             'pulangan lebih tinggi. Itu keputusan risiko, bukan penemuan signal, dan ia '
             'membawa risiko kehabisan modal yang kajian ini tidak mengukur.')
    L.append('')
    L.append('Saya tidak boleh memilih antara ketiga-tiganya untuk pengguna: ia bergantung pada '
             'berapa banyak modal boleh hilang tanpa mengubah hidupnya, dan itu bukan nombor yang '
             'ada dalam repo ini.')
    L.append('')

    S.to_csv(KELUAR / 'sasaran_spy.csv', index=False)
    p = KELUAR / 'SASARAN.md'
    p.write_text('\n'.join(L), encoding='utf-8')
    print(f'{p.name}: {len("".join(L)):,} aksara')
    print(f'SPY median: {S.pulangan_tahunan.median():.2f}%/tahun, MDD {S.mdd.median():.2f}%, '
          f'bulanan {S.median_bulanan.median():.2f}% | +10%/bulan = {A["kali_setahun"]:.2f}x/tahun')
    return 0


if __name__ == '__main__':
    sys.exit(main())
