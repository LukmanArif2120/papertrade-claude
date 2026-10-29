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
        L.append('Bandingkan dengan apa yang kajian ini hasilkan selepas 20,640 ujian indikator '
                 'harga, 108 ujian saiz, 20 ujian fundamental dan 38,400 konfigurasi Optuna: '
                 '**tiada kelebihan yang bertahan sama sekali**. Drag kos ialah nombor yang pasti, '
                 'boleh dikurangkan, dan tidak memerlukan satu pun penemuan untuk dituntut.')
        L.append('')
    L.append('## Apa yang boleh dibuat dengannya')
    L.append('')
    L.append('Drag ini bukan satu nombor tetap — ia hasil **bilangan dagangan × kos setiap sisi**. '
             'Kedua-duanya boleh dikurangkan tanpa mencari apa-apa signal:')
    L.append('')
    L.append('- **Kurangkan pusing ganti.** `REF_pegang_252` memegang jauh lebih lama daripada '
             '`REF_jual_hari63`; jadual di atas menunjukkan kos yang dibayar setiap satu. '
             'Memanjangkan tempoh pegangan mengurangkan drag secara terus.')
    L.append('- **Elak tingkat slippage tertinggi.** Model mengenakan 0.25% pada nama dengan median '
             'nilai dagangan < USD10 juta berbanding 0.05% pada ≥ USD50 juta — **lima kali** '
             'bezanya. Menapis kecairan sebelum masuk memotong kos tanpa menyentuh signal.')
    L.append('- **Komisen ialah terma broker**, bukan sifat pasaran. 0.1% setiap sisi yang dimodel '
             'di sini jauh lebih tinggi daripada broker kos rendah; itu rundingan, bukan kajian.')
    L.append('')
    L.append('Tiga perkara di atas ialah pulangan yang pasti. Setiap kajian signal dalam repo ini '
             'ialah pulangan yang berkemungkinan — dan setakat ini, berkemungkinan sifar.')
    L.append('')
    (KELUAR / 'KOS_DRAG.md').write_text('\n'.join(L), encoding='utf-8')
    print(f'\nKOS_DRAG.md ditulis | drag terbesar: {best[0] if best else "?"} '
          f'{best[1]:.2f} mata' if best else 'KOS_DRAG.md ditulis')
    return 0


if __name__ == '__main__':
    sys.exit(main())
