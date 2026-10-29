"""Ukur KOS sebagai lever — satu-satunya yang tidak bergantung pada sasaran pulangan.

`REVERSE/SASARAN.md` memberi tiga pilihan, dan dua daripadanya bergantung pada selera risiko
pengguna. Yang ketiga tidak: apa-apa sasaran yang dipilih, wang yang tinggal lebih banyak kalau kos
lebih rendah. Repo ini mengukur signal, saiz dan fundamental, tetapi tidak pernah mengukur berapa
banyak pulangan yang dimakan oleh kos itu sendiri.

Kaedah: jalankan portfolio §5.4 yang SAMA dua kali — sekali dengan model kos penuh (komisen 0.1%
setiap sisi + slippage bertingkat), sekali dengan kos SIFAR — dan banding. Bezanya ialah drag.
Tiada signal baharu, tiada parameter ditala, tiada pradaftar dibelanjakan.

Guna: python3 REVERSE/kos_drag.py
Output: REVERSE/KOS_DRAG.md, REVERSE/kos_drag.csv
"""
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
RUJUKAN = S12.RUJUKAN


def _tanpa_kos(_median_nilai20):
    return 0.0


def jalan_tahun(th, eth, kos_sifar):
    """Satu tahun, satu tetapan kos. Pulang baris metrik bagi setiap rujukan keluar."""
    mod = [m for m in (S9, S12) if hasattr(m, 'kos_sisi')]
    asal = {id(m): m.kos_sisi for m in mod}
    if kos_sifar:
        for m in mod:
            m.kos_sisi = _tanpa_kos
    try:
        fr, pra, c, o, to, atrp, kal, _ = S12.sedia_tahun(th, eth)
        pilihan = {(t, pd.Timestamp(d)): (0.0, 0.0, t) for t, d in zip(eth.ticker, eth.tarikh)}
        e2 = eth.assign(tarikh=pd.to_datetime(eth.tarikh))
        out = []
        for ref in RUJUKAN:
            siri, dag, info = S9.jalankan(ref, e2, fr, pra, c, o, to, kal, ref, None, pilihan)
            if siri.empty:
                continue
            ek = siri.set_index('tarikh').ekuiti
            bl = ek.resample('ME').last().pct_change().dropna() * 100
            out.append(dict(tahun=th, keluar=ref, kos=('sifar' if kos_sifar else 'penuh'),
                            pulangan=round((float(ek.iloc[-1]) - 1) * 100, 3),
                            mdd=round(T.mdd(ek.to_numpy()), 2),
                            median_bulanan=round(float(bl.median()), 3) if len(bl) else np.nan,
                            n_masuk=info['n_masuk'], n_tutup=info['n_tutup'],
                            slot_purata=info['purata_slot_terisi']))
        return out
    finally:
        for m in mod:
            m.kos_sisi = asal[id(m)]


def main():
    if '--laporan-sahaja' in sys.argv and (KELUAR / 'kos_drag.csv').exists():
        return laporan(pd.read_csv(KELUAR / 'kos_drag.csv'))
    j = pd.read_csv(KELUAR / 'sec_join.csv', parse_dates=['tarikh'])
    # Populasi = SEMUA peristiwa sah (bukan signal terpilih): drag kos ialah sifat dagangan,
    # bukan sifat signal, jadi ia diukur atas populasi penuh supaya tiada pemilihan masuk.
    ent = j[['saham', 'tarikh']].rename(columns={'saham': 'ticker'}).drop_duplicates()
    baris = []
    for th in sorted(j.tahun.unique()):
        eth = ent[pd.to_datetime(ent.tarikh).dt.year == th]
        if eth.empty:
            continue
        for sifar in (False, True):
            baris += jalan_tahun(th, eth, sifar)
        print(f'  {th}: {len(baris)} baris')
    R = pd.DataFrame(baris)
    R.to_csv(KELUAR / 'kos_drag.csv', index=False)
    return laporan(R)


def laporan(R):
    p = R.pivot_table(index='keluar', columns='kos',
                      values=['pulangan', 'mdd', 'median_bulanan', 'n_masuk'], aggfunc='median')
    L = ['# KOS sebagai lever: berapa banyak pulangan dimakan oleh kos dagangan', '']
    L.append(f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh `REVERSE/kos_drag.py`.')
    L.append('')
    L.append('`REVERSE/SASARAN.md` memberi tiga pilihan dan dua bergantung pada selera risiko '
             'pengguna. Yang ketiga tidak: **apa-apa sasaran yang dipilih, wang yang tinggal lebih '
             'banyak kalau kos lebih rendah.** Repo ini mengukur signal, saiz dan fundamental, '
             'tetapi tidak pernah mengukur kos itu sendiri. Ini mengukurnya.')
    L.append('')
    L.append('Kaedah: portfolio §5.4 yang **sama** dijalankan dua kali atas **semua** peristiwa sah '
             '2012–2025 — sekali dengan model kos penuh (komisen 0.1% setiap sisi + slippage '
             'bertingkat 0.05/0.10/0.25%), sekali dengan kos **sifar**. Populasi penuh dan bukan '
             'signal terpilih, kerana drag kos ialah sifat dagangan dan bukan sifat signal.')
    L.append('')
    L.append('| Keluar | Pulangan (kos penuh) | Pulangan (kos sifar) | Drag | Dagangan/tahun |')
    L.append('|---|---|---|---|---|')
    for ref in RUJUKAN:
        if ref not in p.index:
            continue
        pp, ps = p.loc[ref, ('pulangan', 'penuh')], p.loc[ref, ('pulangan', 'sifar')]
        nm = p.loc[ref, ('n_masuk', 'penuh')]
        L.append(f'| {ref} | {pp:.2f}% | {ps:.2f}% | **{ps - pp:.2f} mata** | {nm:.0f} |')
    L.append('')
    L.append('Nilai ialah **median merentas 14 tahun**. "Drag" = berapa mata peratus setahun yang '
             'hilang kepada komisen dan slippage.')
    L.append('')
    best = None
    for ref in RUJUKAN:
        if ref in p.index:
            d = float(p.loc[ref, ('pulangan', 'sifar')] - p.loc[ref, ('pulangan', 'penuh')])
            if best is None or d > best[1]:
                best = (ref, d)
    if best:
        L.append(f'Drag terbesar: **{best[0]}, {best[1]:.2f} mata peratus setahun**.')
        L.append('')
    L.append('## Apa nombor ini sebenarnya berkata')
    L.append('')
    L.append('**Saya menulis bahagian ini selepas melihat nombor, dan ia bertentangan dengan apa '
             'yang saya jangka.** Saya memilih mengukur kos kerana ia lever yang pasti dan tidak '
             'bergantung pada sasaran. Ukurannya menunjukkan lever itu lebih kecil daripada '
             'rupanya, dan sebahagiannya mengalahkan diri sendiri.')
    L.append('')
    pen = R[R.kos == 'penuh'].groupby('keluar')[['pulangan', 'mdd', 'median_bulanan', 'n_masuk']].median()
    sif = R[R.kos == 'sifar'].groupby('keluar')['pulangan'].median()
    panjang, pendek = 'REF_pegang_252', 'REF_jual_hari63'
    if panjang in pen.index and pendek in pen.index:
        dp = float(sif[pendek] - pen.loc[pendek, 'pulangan'])
        dl = float(sif[panjang] - pen.loc[panjang, 'pulangan'])
        L.append(f'Mengurangkan pusing ganti **memang** memotong kos: `{panjang}` membayar hanya '
                 f'{dl:.2f} mata drag dengan {pen.loc[panjang, "n_masuk"]:.0f} dagangan setahun, '
                 f'berbanding {dp:.2f} mata dengan {pen.loc[pendek, "n_masuk"]:.0f} dagangan.')
        L.append('')
        L.append(f'Tetapi pulangan **bersihnya** lebih rendah: {pen.loc[panjang, "pulangan"]:.2f}% '
                 f'lawan {pen.loc[pendek, "pulangan"]:.2f}%. Menjimatkan {dp - dl:.2f} mata kos '
                 f'mengorbankan {pen.loc[pendek, "pulangan"] - pen.loc[panjang, "pulangan"]:.2f} '
                 'mata pulangan. **Pusing ganti yang tinggi itu membayar kosnya sendiri.**')
        L.append('')
        L.append(f'Drag terbesar, {dp:.2f} mata, ialah '
                 f'{dp / float(pen.loc[pendek, "pulangan"]) * 100:.0f}% daripada pulangan '
                 'konfigurasi itu. Itu wang sebenar dan patut dikurangkan di tempat yang boleh '
                 '— komisen ialah terma broker, bukan sifat pasaran, dan slippage 0.25% pada nama '
                 '< USD10 juta lawan 0.05% pada ≥ USD50 juta ialah lima kali bezanya, ditapis '
                 'sebelum masuk tanpa menyentuh signal. Tetapi ia **tidak** mengubah gambaran '
                 'strategik.')
    L.append('')
    L.append('Bandingan yang menentukan, kos penuh, median 14 tahun:')
    L.append('')
    L.append('| | Pulangan | MDD | Median bulanan | Dagangan/tahun |')
    L.append('|---|---|---|---|---|')
    for k in R.keluar.unique():
        r = pen.loc[k]
        L.append(f'| {k} | {r.pulangan:.2f}% | {r.mdd:.2f}% | {r.median_bulanan:.2f}% | '
                 f'{r.n_masuk:.0f} |')
    L.append('| **SPY beli-dan-pegang** | **17.62%** | **−9.44%** | **1.82%** | **1** |')
    L.append('')
    if pendek in pen.index:
        r = pen.loc[pendek]
        L.append(f'Konfigurasi terbaik mengalahkan SPY pada pulangan ({r.pulangan:.2f}% lawan '
                 f'17.62%) tetapi dengan MDD {abs(r.mdd) / 9.44:.1f} kali lebih dalam '
                 f'({r.mdd:.2f}% lawan −9.44%) dan median bulanan lebih rendah '
                 f'({r.median_bulanan:.2f}% lawan 1.82%). Walaupun kos **dihapuskan sepenuhnya** '
                 f'— mustahil — ia menjadi {sif[pendek]:.2f}% pada MDD yang sama.')
        L.append('')
    L.append('Maka kesimpulannya: **kos bukan masalahnya.** Ia 13% daripada pulangan dan patut '
             'dikurangkan, tetapi menghapuskannya sepenuhnya pun tidak membawa sistem ini kepada '
             'sasaran +10%/bulan, dan tidak menjadikan drawdownnya setanding SPY.')
    L.append('')
    L.append('Saya mengukurnya kerana ia satu-satunya lever yang tinggal yang tidak memerlukan '
             'keputusan anda. Hasilnya menutup lever itu juga. Yang tinggal sekarang benar-benar '
             'hanya keputusan sasaran, dan ia milik anda.')
    L.append('')
    (KELUAR / 'KOS_DRAG.md').write_text('\n'.join(L), encoding='utf-8')
    print(f'\nKOS_DRAG.md ditulis | drag terbesar: {best[0] if best else "?"} '
          f'{best[1]:.2f} mata' if best else 'KOS_DRAG.md ditulis')
    return 0


if __name__ == '__main__':
    sys.exit(main())
