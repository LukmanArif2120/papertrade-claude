"""Adakah angka 8-slot kajian ini cabutan bertuah?

`step9_portfolio.jalankan()` menyusun calon dengan `pilihan.get((t, hari), (0.0, 0.0, t))` dan
`reverse=True`. Apabila tiada pemeringkatan signal, tuple itu pemalar, jadi susunan menjadi **ticker
menurun ikut abjad**. Maka "8 slot" bermakna 8 calon terakhir ikut abjad setiap hari — satu subset
sewenang-wenang yang TETAP, bukan sampel neutral.

`REVERSE/KEPEKATAN.md` menunjukkan 8 slot = 19.31%/tahun tetapi 60 slot = 13.34%. Oleh kerana 60
slot mengambil hampir semua calon, 13.34% menghampiri min populasi. Jadi 19.31% itu mungkin cuma
cabutan bertuah — dan jika benar, setiap angka 8-slot dalam kajian ini melambung.

Ujian: 8 slot, populasi/keluar/kos SAMA, hanya susunan pemilihan ditukar kepada rawak dengan
beberapa benih. Jika sebarannya luas, angka 8-slot ialah hingar.

Guna: python3 REVERSE/kepekatan_benih.py [--benih 1,2,3,4,5]
Output: REVERSE/KEPEKATAN_BENIH.md, REVERSE/kepekatan_benih.csv
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
KELUARAN = 'REF_jual_hari63'
SLOT = 8


def jalan_tahun(th, eth, benih):
    """benih None = susunan abjad asal (seperti seluruh kajian); jika tidak, susunan rawak."""
    fr, pra, c, o, to, atrp, kal, _ = S12.sedia_tahun(th, eth)
    if benih is None:
        pilihan = {(t, pd.Timestamp(d)): (0.0, 0.0, t) for t, d in zip(eth.ticker, eth.tarikh)}
    else:
        rng = np.random.default_rng(benih)
        pilihan = {(t, pd.Timestamp(d)): (float(rng.random()), 0.0, t)
                   for t, d in zip(eth.ticker, eth.tarikh)}
    e2 = eth.assign(tarikh=pd.to_datetime(eth.tarikh))
    siri, dag, info = S9.jalankan(KELUARAN, e2, fr, pra, c, o, to, kal, KELUARAN, None, pilihan,
                                  slot=SLOT)
    if siri.empty:
        return None
    ek = siri.set_index('tarikh').ekuiti
    bl = ek.resample('ME').last().pct_change().dropna() * 100
    return dict(tahun=th, benih=('abjad' if benih is None else str(benih)),
                pulangan=round((float(ek.iloc[-1]) - 1) * 100, 2),
                mdd=round(T.mdd(ek.to_numpy()), 2),
                median_bulanan=round(float(bl.median()), 2) if len(bl) else np.nan,
                n_masuk=info['n_masuk'])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--benih', default='1,2,3,4,5')
    ap.add_argument('--laporan-sahaja', action='store_true',
                    help='jana laporan daripada kepekatan_benih.csv tanpa mengira ulang')
    a = ap.parse_args(argv)
    benih = [None] + [int(x) for x in a.benih.split(',')]

    if a.laporan_sahaja and (KELUAR / 'kepekatan_benih.csv').exists():
        return laporan(pd.read_csv(KELUAR / 'kepekatan_benih.csv'))
    j = pd.read_csv(KELUAR / 'sec_join.csv', parse_dates=['tarikh'])
    ent = j[['saham', 'tarikh']].rename(columns={'saham': 'ticker'}).drop_duplicates()
    baris = []
    for th in sorted(j.tahun.unique()):
        eth = ent[pd.to_datetime(ent.tarikh).dt.year == th]
        if eth.empty:
            continue
        for b in benih:
            r = jalan_tahun(th, eth, b)
            if r:
                baris.append(r)
        print(f'  {th}: {len(baris)} baris')
    R = pd.DataFrame(baris)
    R.to_csv(KELUAR / 'kepekatan_benih.csv', index=False)
    return laporan(R)


def laporan(R):
    g = R.groupby('benih')[['pulangan', 'mdd', 'median_bulanan']].median().round(2)
    rw = g.drop(index='abjad', errors='ignore')
    L = ['# Adakah angka 8-slot kajian ini cabutan bertuah?', '']
    L.append(f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh '
             '`REVERSE/kepekatan_benih.py`.')
    L.append('')
    L.append('`step9_portfolio.jalankan()` menyusun calon dengan tuple `(0.0, 0.0, ticker)` dan '
             '`reverse=True`. Tanpa pemeringkatan signal, tuple itu **pemalar**, jadi susunan '
             'menjadi **ticker menurun ikut abjad**. "8 slot" bermakna 8 calon terakhir ikut abjad '
             'setiap hari — subset sewenang-wenang yang TETAP, bukan sampel neutral.')
    L.append('')
    L.append('`KEPEKATAN.md` menunjukkan 8 slot = 19.31%/tahun tetapi 60 slot = 13.34%. Oleh kerana '
             '60 slot mengambil hampir semua calon, 13.34% menghampiri min populasi. Jadi 19.31% '
             'mungkin cabutan bertuah.')
    L.append('')
    L.append('Ujian: 8 slot, populasi/keluar/kos **sama**, hanya susunan pemilihan ditukar kepada '
             'rawak dengan beberapa benih.')
    L.append('')
    L.append('| Susunan | Pulangan/tahun | MDD | Median bulanan |')
    L.append('|---|---|---|---|')
    for b in g.index:
        r = g.loc[b]
        tanda = ' **(yang diguna seluruh kajian)**' if b == 'abjad' else ''
        L.append(f'| {b}{tanda} | {r.pulangan:.2f}% | {r.mdd:.2f}% | {r.median_bulanan:.2f}% |')
    L.append('')
    if not rw.empty:
        lo, hi, md = float(rw.pulangan.min()), float(rw.pulangan.max()), float(rw.pulangan.median())
        ab = float(g.loc['abjad', 'pulangan']) if 'abjad' in g.index else np.nan
        L.append(f'Susunan rawak: median **{md:.2f}%**, julat {lo:.2f}% hingga {hi:.2f}% '
                 f'({len(rw)} benih). Susunan abjad yang diguna seluruh kajian: **{ab:.2f}%**.')
        L.append('')
        n_bawah = int((rw.pulangan < ab).sum())
        pval = (len(rw) - n_bawah + 1) / (len(rw) + 1)
        sd = float(rw.pulangan.std())
        L.append(f'Susunan abjad melebihi **{n_bawah} daripada {len(rw)}** benih rawak; nilai-p '
                 f'satu-hujung **{pval:.3f}**.')
        L.append('')
        if pval <= 0.05:
            L.append('Itu melepasi ambang kelaziman: susunan abjad ialah subset bertuah, dan angka '
                     '8-slot kajian ini melambung.')
        else:
            L.append(f'Itu **tidak** melepasi ambang kelaziman (p = {pval:.3f} > 0.05). Susunan '
                     f'abjad berada pada hujung tinggi taburan tetapi **tidak boleh didakwa '
                     f'bertuah secara pasti** — sekurang-kurangnya satu benih rawak '
                     f'({rw.pulangan.max():.2f}%) mengalahkannya.')
        L.append('')
        L.append('**Dapatan yang menentukan bukan nilai-p itu, tetapi SEBARANNYA.**')
        L.append('')
        L.append(f'- Median susunan neutral: **{md:.2f}%/tahun** — ini anggaran pusat yang betul '
                 f'bagi sistem pada 8 slot, bukan {ab:.2f}%.')
        L.append(f'- Julat: {lo:.2f}% hingga {hi:.2f}%, sisihan piawai **{sd:.2f} mata**.')
        L.append(f'- Maka apa-apa perbandingan sistem yang bezanya lebih kecil daripada kira-kira '
                 f'**{hi - lo:.1f} mata** adalah dalam hingar pemilihan, bukan dapatan.')
        L.append('')
        L.append(f'Nombor {ab:.2f}% yang dilaporkan sepanjang kajian ialah **satu cabutan** '
                 f'daripada taburan ini, dan cabutan itu berada di hujung tinggi (persentil '
                 f'{100 * n_bawah / len(rw):.0f}). Anggaran yang betul ialah medianya, '
                 f'{md:.2f}%/tahun pada MDD {float(rw.mdd.median()):.2f}%.')
        L.append('')
    (KELUAR / 'KEPEKATAN_BENIH.md').write_text('\n'.join(L), encoding='utf-8')
    print('\n' + g.to_string())
    return 0


if __name__ == '__main__':
    sys.exit(main())
