"""KEPEKATAN portfolio — satu-satunya parameter struktur yang ditetapkan secara fiat dan tidak
pernah diukur.

`SPEC.md` §3 menetapkan **8 slot × 12.5%** sebagai kriteria akhir kajian, dan setiap fasa memakainya
tanpa pernah menyoalnya. Fasa 1b menguji **saiz** posisi (RISIKO, k) tetapi bukan **bilangan**
posisi. Namun lihat di mana sistem kalah kepada penanda aras pasif:

    SPUS (300+ saham)          26.09%/tahun   MDD -10.14%
    Sistem terbaik (8 saham)   18.12%/tahun   MDD -28.42%

Kalah sedikit pada pulangan, kalah hampir **tiga kali** pada drawdown. Itu tandatangan kepekatan,
bukan tandatangan signal yang lemah: 8 posisi daripada populasi peristiwa sah ialah sampel kecil
daripada min populasi, jadi variansnya tinggi walaupun minnya positif.

Ujian: populasi, keluar dan kos yang SAMA; hanya bilangan slot berubah. Ekuiti dibahagi sama rata
(1/slot) supaya pendedahan penuh kekal 100% dan hanya kepekatan berubah. Tiada signal baharu, tiada
parameter ditala, tiada pradaftar dibelanjakan — ini soalan pembinaan portfolio, bukan soalan signal.

Guna: python3 REVERSE/kepekatan.py [--slot 8,16,24,40,60]
Output: REVERSE/KEPEKATAN.md, REVERSE/kepekatan.csv
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE import step9_portfolio as S9  # noqa: E402
from REVERSE import step12_sec_portfolio as S12  # noqa: E402
from REVERSE.teras import stat as T  # noqa: E402

KELUAR = AKAR / 'REVERSE'
# Satu rujukan keluar sahaja: yang terbaik dalam ukuran kos (REF_jual_hari63). Menguji ketiga-tiga
# x lima slot x 14 tahun ialah 210 simulasi tanpa menambah apa-apa kepada soalan kepekatan.
KELUARAN = 'REF_jual_hari63'
SLOT_LALAI = [8, 16, 24, 40, 60]


def jalan_tahun(th, eth, slot):
    fr, pra, c, o, to, atrp, kal, _ = S12.sedia_tahun(th, eth)
    pilihan = {(t, pd.Timestamp(d)): (0.0, 0.0, t) for t, d in zip(eth.ticker, eth.tarikh)}
    e2 = eth.assign(tarikh=pd.to_datetime(eth.tarikh))
    siri, dag, info = S9.jalankan(KELUARAN, e2, fr, pra, c, o, to, kal, KELUARAN, None, pilihan,
                                  slot=slot)
    if siri.empty:
        return None
    ek = siri.set_index('tarikh').ekuiti
    bl = ek.resample('ME').last().pct_change().dropna() * 100
    return dict(tahun=th, slot=slot, pulangan=round((float(ek.iloc[-1]) - 1) * 100, 2),
                mdd=round(T.mdd(ek.to_numpy()), 2),
                median_bulanan=round(float(bl.median()), 2) if len(bl) else np.nan,
                pct_bulan_ge10=round(float((bl >= 10).mean() * 100), 1) if len(bl) else np.nan,
                bulan_terburuk=round(float(bl.min()), 2) if len(bl) else np.nan,
                n_masuk=info['n_masuk'], slot_purata=info['purata_slot_terisi'])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--slot', default=','.join(str(x) for x in SLOT_LALAI))
    a = ap.parse_args(argv)
    slots = [int(x) for x in a.slot.split(',')]

    j = pd.read_csv(KELUAR / 'sec_join.csv', parse_dates=['tarikh'])
    ent = j[['saham', 'tarikh']].rename(columns={'saham': 'ticker'}).drop_duplicates()
    baris = []
    for th in sorted(j.tahun.unique()):
        eth = ent[pd.to_datetime(ent.tarikh).dt.year == th]
        if eth.empty:
            continue
        for sl in slots:
            r = jalan_tahun(th, eth, sl)
            if r:
                baris.append(r)
        print(f'  {th}: {len(baris)} baris')
    R = pd.DataFrame(baris)
    R.to_csv(KELUAR / 'kepekatan.csv', index=False)

    p = R.groupby('slot')[['pulangan', 'mdd', 'median_bulanan', 'pct_bulan_ge10',
                           'bulan_terburuk', 'n_masuk']].median().round(2)
    L = ['# KEPEKATAN portfolio: parameter yang ditetapkan secara fiat, tidak pernah diukur', '']
    L.append(f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh `REVERSE/kepekatan.py`.')
    L.append('')
    L.append('`SPEC.md` §3 menetapkan **8 slot × 12.5%** dan setiap fasa memakainya tanpa pernah '
             'menyoalnya. Fasa 1b menguji **saiz** posisi, bukan **bilangan**. Tetapi sistem kalah '
             'kepada penanda aras pasif terutamanya pada **drawdown** (−28.42% lawan −10.14%), dan '
             'itu tandatangan kepekatan, bukan signal lemah: 8 posisi ialah sampel kecil daripada '
             'min populasi, jadi variansnya tinggi walaupun minnya positif.')
    L.append('')
    L.append(f'Populasi, keluar (`{KELUARAN}`) dan kos **sama**; hanya bilangan slot berubah. '
             'Ekuiti dibahagi sama rata (1/slot) supaya pendedahan kekal 100%.')
    L.append('')
    L.append('| Slot | Pulangan/tahun | MDD | Median bulanan | % bulan ≥ +10% | Bulan terburuk | Dagangan/tahun |')
    L.append('|---|---|---|---|---|---|---|')
    for sl in p.index:
        r = p.loc[sl]
        L.append(f'| {sl} | {r.pulangan:.2f}% | {r.mdd:.2f}% | {r.median_bulanan:.2f}% | '
                 f'{r.pct_bulan_ge10:.1f}% | {r.bulan_terburuk:.2f}% | {r.n_masuk:.0f} |')
    L.append('| **SPUS (penanda aras)** | **26.09%** | **−10.14%** | **2.59%** | 0.0% | — | **1** |')
    L.append('')
    L.append('Nilai ialah **median merentas 14 tahun (2012–2025)**. SPUS hanya 6 tahun '
             '(2020–2025) dan MDD-nya daripada tutup bulanan — lihat `PENANDA_ARAS_SYARIAH.md` '
             'untuk had itu.')
    L.append('')
    asas, maks = int(p.index.min()), int(p.index.max())
    da = float(p.loc[maks, 'mdd']) - float(p.loc[asas, 'mdd'])
    dp = float(p.loc[maks, 'pulangan']) - float(p.loc[asas, 'pulangan'])
    L.append(f'Daripada {asas} slot ke {maks} slot: MDD berubah **{da:+.2f} mata** dan pulangan '
             f'**{dp:+.2f} mata**.')
    L.append('')
    # Terbaik pada paksi risiko-laras mudah: pulangan / |MDD|
    p2 = p.copy()
    p2['pulangan_per_mdd'] = (p2.pulangan / p2.mdd.abs()).round(3)
    bs = int(p2.pulangan_per_mdd.idxmax())
    L.append('Nisbah mudah pulangan ÷ |MDD| bagi setiap kepekatan:')
    L.append('')
    for sl in p2.index:
        L.append(f'- {sl} slot: {p2.loc[sl, "pulangan_per_mdd"]:.3f}')
    L.append('')
    L.append(f'Terbaik: **{bs} slot**. Nisbah itu bukan kriteria yang dipradaftar dan tidak boleh '
             'dijadikan dapatan — ia hanya menunjukkan arah. Apa-apa pilihan slot yang dibuat '
             'selepas melihat jadual ini adalah pemilihan selepas fakta, dan mesti disahkan ke '
             'hadapan sebelum dipercayai.')
    L.append('')
    p.to_csv(KELUAR / 'kepekatan_ringkas.csv')
    (KELUAR / 'KEPEKATAN.md').write_text('\n'.join(L), encoding='utf-8')
    print(f'\nKEPEKATAN.md ditulis | {asas}->{maks} slot: MDD {da:+.2f} mata, pulangan {dp:+.2f} mata')
    return 0


if __name__ == '__main__':
    sys.exit(main())
