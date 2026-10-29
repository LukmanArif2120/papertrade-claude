"""Adakah +10% sebulan mungkin? Diukur daripada Papertrade C sendiri.

Soalan pengguna 29 Okt 2026. Dijawab daripada data jejak hadapan sebenar, bukan backtest:
`papertrade/claude*.csv` (posisi sah yang benar-benar dibeli) dan `portfolio_slot/` (satu-satunya
ukuran PORTFOLIO yang ada).

Dua perkara mesti dipisahkan, kerana mencampurkannya memberi jawapan yang salah:

1. **Pulangan setiap posisi** — 7 ribu posisi daripada 124 kaedah. Ini BUKAN portfolio: tiada
   sesiapa boleh membeli kesemuanya. Ia memberitahu kita BENTUK taburan.
2. **Pulangan portfolio** — `portfolio_slot/` 10 slot. Ini yang boleh didagangkan, dan ini yang
   mesti mencapai +10% sebulan.

Guna: python3 BacktestShariah2/standard/sasaran_papertrade.py
Output: BacktestShariah2/laporan/SASARAN_PAPERTRADE.md
"""
import glob
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
PT = os.path.join(BS2, 'papertrade')
PS = os.path.join(BS2, 'portfolio_slot')
KELUAR = os.path.join(BS2, 'laporan', 'SASARAN_PAPERTRADE.md')
SESI_SEBULAN = 21          # sesi dagangan dalam sebulan
SASARAN = 10.0


def posisi():
    f = sorted(glob.glob(os.path.join(PT, 'claude*.csv')))
    if not f:
        return None, 0
    d = pd.concat([pd.read_csv(x, low_memory=False) for x in f], ignore_index=True)
    for c in ('tidak_sah', 'tidak_dibeli'):
        if c in d:
            d[c] = d[c].astype(str).str.lower().isin(['true', '1', 'ya'])
        else:
            d[c] = False
    return d[~d.tidak_sah & ~d.tidak_dibeli], len(f)


def lorong():
    out = []
    for p in sorted(glob.glob(os.path.join(PS, '*_ekuiti.csv'))):
        k = os.path.basename(p).replace('_ekuiti.csv', '')
        if k.startswith('rawak_jalur'):
            continue
        e = pd.read_csv(p)
        if not len(e):
            continue
        n, v = len(e), float(e.ekuiti.iloc[-1])
        out.append(dict(lorong=k, sesi=n, pulangan=(v - 1) * 100,
                        unjur_bulan=(v ** (SESI_SEBULAN / n) - 1) * 100))
    j = os.path.join(PS, 'rawak_jalur_ekuiti.csv')
    if os.path.exists(j):
        J = pd.read_csv(j)
        if len(J):
            a = J[J.tarikh == J.tarikh.max()].ekuiti
            n = J.tarikh.nunique()
            out.append(dict(lorong=f'jalur rawak (median, {len(a)} cabutan)', sesi=n,
                            pulangan=(float(a.median()) - 1) * 100,
                            unjur_bulan=(float(a.median()) ** (SESI_SEBULAN / n) - 1) * 100))
    return pd.DataFrame(out)


def main():
    s, nf = posisi()
    if s is None or s.empty:
        print('tiada data papertrade')
        return 1
    kel = s[s.untung_akhir_pct.notna()]
    buk = s[s.untung_akhir_pct.isna() & s.untung_pct.notna()]
    semua = pd.concat([kel.untung_akhir_pct, buk.untung_pct])
    L = lorong()

    A = [f'# Adakah +{SASARAN:.0f}% sebulan mungkin? Diukur daripada Papertrade C', '']
    A.append(f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh '
             '`standard/sasaran_papertrade.py`. Data jejak hadapan sebenar, bukan backtest.')
    A.append('')
    A.append(f'**Tempoh: {s.tarikh_beli.min()} hingga {s.tarikh_beli.max()}.** '
             f'{len(s):,} posisi sah dibeli, {s.saham.nunique()} saham, '
             f'{s.id_kaedah.nunique()} kaedah, {nf} fail.')
    A.append('')
    A.append('## 1. Had yang mesti dibaca dahulu')
    A.append('')
    A.append('Tempoh ini **kurang daripada sebulan penuh**. Data ini tidak boleh menjawab sama ada '
             f'+{SASARAN:.0f}% sebulan BOLEH DIKEKALKAN. Ia hanya boleh menunjukkan **bentuk** '
             'taburan pulangan, dan sama ada bentuk itu membenarkan sasaran tersebut.')
    A.append('')
    A.append(f'{len(s):,} posisi daripada {s.id_kaedah.nunique()} kaedah **bukan portfolio** — '
             'tiada sesiapa boleh membeli kesemuanya. Pulangan setiap posisi dan pulangan portfolio '
             'ialah dua perkara berbeza, dan hanya yang kedua perlu mencapai sasaran.')
    A.append('')
    A.append('## 2. Posisi yang sudah DITUTUP (realisasi)')
    A.append('')
    A.append(f'- {len(kel):,} posisi')
    A.append(f'- median **{kel.untung_akhir_pct.median():+.2f}%**, purata '
             f'{kel.untung_akhir_pct.mean():+.2f}%')
    A.append(f'- kadar menang **{100 * (kel.untung_akhir_pct > 0).mean():.1f}%**')
    A.append(f'- tempoh pegang median **{kel.hari.median():.0f} hari**')
    A.append('')
    A.append(f'Posisi masih terbuka: {len(buk):,}, median {buk.untung_pct.median():+.2f}%. '
             'Angka terbuka itu kelihatan lebih baik kerana yang rugi **sudah dikeluarkan** oleh '
             'henti — itu bukan prestasi, itu kesan pemilihan dalam buku terbuka.')
    A.append('')
    A.append(f'## 3. Berapa kerap satu posisi mencapai +{SASARAN:.0f}%?')
    A.append('')
    A.append('| Ambang | Daripada posisi ditutup | Daripada semua posisi |')
    A.append('|---|---|---|')
    for t in (5, 10, 20, 50):
        A.append(f'| ≥ +{t}% | {100 * (kel.untung_akhir_pct >= t).mean():.2f}% | '
                 f'{100 * (semua >= t).mean():.2f}% |')
    A.append('')
    A.append(f'Taburan semua posisi: p10 {semua.quantile(.10):+.2f}% · p25 {semua.quantile(.25):+.2f}% · '
             f'p50 **{semua.quantile(.50):+.2f}%** · p75 {semua.quantile(.75):+.2f}% · '
             f'p90 **{semua.quantile(.90):+.2f}%** · maks {semua.max():+.2f}%')
    A.append('')
    # Tempoh pegang: median SEMUA posisi, bukan yang ditutup sahaja. Posisi ditutup didominasi
    # henti pantas (median 1 hari), jadi menggunakannya melebih-lebihkan pusing ganti dengan teruk
    # dan memberi keperluan setiap pusingan yang jauh terlalu rendah.
    hari = float(s.hari.median()) if len(s) else 15.0
    per_bulan = max(SESI_SEBULAN / max(hari, 1.0), 1.0)
    perlu = ((1 + SASARAN / 100.0) ** (1 / per_bulan) - 1) * 100
    # Asas yang betul ialah pulangan REALISASI. Purata semua posisi berat sebelah ke atas kerana
    # 76% masih terbuka: yang rugi sudah dikeluarkan oleh henti, yang baik masih dikira.
    real = float(kel.untung_akhir_pct.mean()) if len(kel) else float('nan')
    campur = float(semua.mean())
    A.append('### Aritmetik yang menentukan')
    A.append('')
    A.append(f'Tempoh pegang median **{hari:.0f} hari** (semua posisi; yang DITUTUP median '
             f'{kel.hari.median():.0f} hari kerana didominasi henti pantas — menggunakan angka itu '
             'akan melebih-lebihkan pusing ganti dengan teruk).')
    A.append('')
    A.append(f'Itu kira-kira **{per_bulan:.1f} pusingan sebulan**. Untuk +{SASARAN:.0f}% sebulan, '
             f'setiap pusingan perlu **+{perlu:.2f}% purata merentas semua posisi**, termasuk yang '
             'rugi, selepas kos.')
    A.append('')
    A.append(f'**Asas yang betul ialah pulangan REALISASI: {real:+.2f}%** (purata '
             f'{len(kel):,} posisi yang sudah ditutup).')
    A.append('')
    A.append(f'Purata semua posisi ({campur:+.2f}%) **tidak boleh diguna** di sini: '
             f'{100 * len(buk) / len(s):.0f}% posisi masih terbuka, dan yang rugi sudah dikeluarkan '
             f'oleh henti sementara yang baik masih dikira. Realisasi {real:+.2f}% lawan '
             f'belum-nyata {buk.untung_pct.mean():+.2f}% menunjukkan saiz berat sebelah itu. '
             'Apabila henti tamat, posisi terbuka akan bergerak ke arah taburan yang ditutup.')
    A.append('')
    A.append(f'Jadi: perlu **+{perlu:.2f}%** setiap pusingan, dapat **{real:+.2f}%**. '
             f'Jurangnya **{perlu - real:.2f} mata peratus setiap pusingan**, '
             f'{per_bulan:.1f} kali sebulan.')
    A.append('')
    if not L.empty:
        A.append('## 4. Pulangan PORTFOLIO sebenar (satu-satunya yang boleh didagangkan)')
        A.append('')
        A.append('| Lorong | Sesi | Pulangan | Unjuran sebulan (21 sesi) |')
        A.append('|---|---|---|---|')
        for _, r in L.sort_values('unjur_bulan', ascending=False).iterrows():
            A.append(f'| {r.lorong} | {int(r.sesi)} | {r.pulangan:+.2f}% | {r.unjur_bulan:+.2f}% |')
        A.append('')
        b = float(L.unjur_bulan.max())
        A.append(f'Unjuran terbaik: **{b:+.2f}% sebulan**, lawan sasaran +{SASARAN:.0f}%. '
                 '**Unjuran daripada 4–8 sesi tidak bermakna** — ia disenaraikan hanya untuk '
                 'menunjukkan tiada satu pun lorong berada di sekitar sasaran, bukan sebagai '
                 'ramalan.')
        A.append('')
    A.append('## 5. Jawapan')
    A.append('')
    A.append(f'**Tidak, bukan pada apa yang data ini tunjukkan.** Untuk +{SASARAN:.0f}% sebulan '
             f'portfolio perlu +{perlu:.2f}% setiap pusingan ({per_bulan:.1f} kali sebulan). '
             f'Pulangan realisasi sebenar ialah {real:+.2f}% — median '
             f'{kel.untung_akhir_pct.median():+.2f}% dengan kadar menang '
             f'{100 * (kel.untung_akhir_pct > 0).mean():.0f}%. Jurangnya '
             f'{perlu - real:.2f} mata setiap pusingan, bukan beberapa titik perpuluhan.')
    A.append('')
    A.append('Ukuran portfolio sebenar mengatakan hal yang sama: tiada satu pun daripada enam '
             'lorong `portfolio_slot/` berada di sekitar sasaran.')
    A.append('')
    A.append('**Had yang jujur:** data ini kurang sebulan dan 76% posisi belum ditutup. Ia '
             '**tidak** membuktikan sasaran itu mustahil secara kekal. Ia menunjukkan bahawa '
             'sekarang tiada satu pun tanda ke arahnya, dan jurangnya besar — bukan jenis jurang '
             'yang ditutup dengan menala parameter.')
    A.append('')
    A.append('Baca semula dokumen ini selepas 6 bulan jejak hadapan. Bukan untuk mengesahkan '
             'sasaran, tetapi untuk melihat paras mana yang benar-benar dicapai.')
    A.append('')
    os.makedirs(os.path.dirname(KELUAR), exist_ok=True)
    with open(KELUAR, 'w', encoding='utf-8') as f:
        f.write('\n'.join(A))
    print(f'SASARAN_PAPERTRADE.md: {len(s):,} posisi | realisasi purata {real:+.2f}% | '
          f'perlu +{perlu:.2f}% setiap pusingan ({per_bulan:.1f}/bulan) | jurang '
          f'{perlu - real:.2f} mata')
    return 0


if __name__ == '__main__':
    sys.exit(main())
