"""Diagnostik POST-HOC bagi `REVERSE/JARAK_52W.md` — BUKAN gate, BUKAN hipotesis pradaftar.

Dijalankan selepas keputusan §2–§4 dilihat, untuk menerangkan percanggahan antara MIN dan
MEDIAN yang muncul dalam jadual desil. Tiada dakwaan statistik dibuat di sini; ia huraian.

Guna: python3 REVERSE/step40b_52w_diag.py
Output: REVERSE/JARAK_52W_DIAG.md, REVERSE/jarak_52w_diag.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE.step40_52w import (BAND, CAIR, LATIH, NAMA_BAND, PANEL, TAHAN, UFUK,  # noqa: E402
                                XK, t_nw)

KELUAR = AKAR / 'REVERSE'


def main():
    P = pd.read_parquet(PANEL)
    P['date'] = pd.to_datetime(P['date'])
    th = P.date.dt.year.to_numpy()
    cair = P.nilai20.to_numpy() >= CAIR
    j52 = P.j52.to_numpy('float64')
    asas_m = cair & np.isfinite(j52) & (th >= LATIH[0]) & (th <= TAHAN[1])
    L, baris = [], []
    L += ['# Jarak 52w — diagnostik POST-HOC', '',
          '**Bukan gate, bukan pradaftar.** Dijalankan selepas `REVERSE/JARAK_52W.md` dilihat,',
          'semata-mata untuk menerangkan mengapa MIN dan MEDIAN memberi arah BERTENTANGAN.',
          'Tiada dakwaan statistik baharu; `REVERSE/SPEC_52W.md` §11 melarang penalaan band.', '']

    # ---- 1. median setiap band (metrik ini TIADA dalam spec §6) ----
    L += ['## 1. Median setiap band (metrik POST-HOC)', '']
    for kod in ('H126', 'X13'):
        pul = P[f'pul_{kod}'].to_numpy('float64')
        L += [f'### `{kod}`', '',
              '| Band | n tahan | Min tahan | **Median tahan** | Min latih | **Median latih** |',
              '|---|---|---|---|---|---|']
        for kodb, b0, b1 in BAND:
            r = {}
            for w, (y0, y1) in (('latih', LATIH), ('tahan', TAHAN)):
                m = (cair & np.isfinite(j52) & (j52 >= b0) & (j52 < b1)
                     & (th >= y0) & (th <= y1))
                x = pul[m]
                x = x[np.isfinite(x)]
                r[w] = (x.size, x.mean() * 100 if x.size else np.nan,
                        np.median(x) * 100 if x.size else np.nan)
            baris.append(dict(jenis='band_median', keluar=kod, band=kodb,
                              n_tahan=r['tahan'][0], min_tahan=r['tahan'][1],
                              median_tahan=r['tahan'][2], min_latih=r['latih'][1],
                              median_latih=r['latih'][2]))
            L.append(f'| `{kodb}` {NAMA_BAND[kodb]} | {r["tahan"][0]:,} | '
                     f'{r["tahan"][1]:+.2f}% | **{r["tahan"][2]:+.2f}%** | '
                     f'{r["latih"][1]:+.2f}% | **{r["latih"][2]:+.2f}%** |')
        L.append('')

    # ---- 2. setiap tahun: IC, median desil, min desil ----
    L += ['## 2. Setiap tahun (ufuk 126 sesi) — stabiliti', '',
          '| Tahun | IC min | % hari IC > 0 | Median D1 | Median D9 | Median D10 | '
          'Min D1 | Min D10 | Beza median D9−D1 |', '|---|---|---|---|---|---|---|---|---|']
    kol = 'pul_H126'
    for y in range(LATIH[0], TAHAN[1] + 1):
        m = cair & np.isfinite(j52) & (th == y) & np.isfinite(P[kol].to_numpy('float64'))
        S = pd.DataFrame({'date': P.date.to_numpy()[m], 'j52': j52[m],
                          'r': P[kol].to_numpy('float64')[m]})
        g = S.groupby('date', sort=False)
        n_h = g.size()
        S = S[S.date.isin(n_h[n_h >= 20].index)]
        g = S.groupby('date', sort=False)
        rj = g.j52.rank(pct=True).to_numpy()
        rr = g.r.rank(pct=True).to_numpy()
        A = pd.DataFrame({'date': S.date.to_numpy(), 'x': rj, 'y': rr})
        A['xy'] = A.x * A.y
        A['xx'] = A.x * A.x
        A['yy'] = A.y * A.y
        gg = A.groupby('date', sort=True)
        n = gg.size().to_numpy('float64')
        mx, my = gg.x.sum().to_numpy() / n, gg.y.sum().to_numpy() / n
        cov = gg.xy.sum().to_numpy() / n - mx * my
        vx = np.maximum(gg.xx.sum().to_numpy() / n - mx * mx, 0)
        vy = np.maximum(gg.yy.sum().to_numpy() / n - my * my, 0)
        with np.errstate(invalid='ignore', divide='ignore'):
            ic = cov / np.sqrt(vx * vy)
        des = np.minimum((rj * 10).astype(int), 9) + 1
        S = S.assign(desil=des)
        dd = S.groupby('desil').r.agg(['mean', 'median'])
        gm = lambda k, c: float(dd.loc[k, c] * 100) if k in dd.index else np.nan  # noqa: E731
        baris.append(dict(jenis='tahunan', tahun=y, ic_min=float(np.nanmean(ic)),
                          ic_positif=float(np.nanmean(ic > 0) * 100),
                          med_d1=gm(1, 'median'), med_d9=gm(9, 'median'),
                          med_d10=gm(10, 'median'), min_d1=gm(1, 'mean'),
                          min_d10=gm(10, 'mean')))
        L.append(f'| {y} | {np.nanmean(ic):+.4f} | {np.nanmean(ic > 0)*100:.0f}% | '
                 f'{gm(1,"median"):+.2f}% | {gm(9,"median"):+.2f}% | {gm(10,"median"):+.2f}% | '
                 f'{gm(1,"mean"):+.2f}% | {gm(10,"mean"):+.2f}% | '
                 f'{gm(9,"median")-gm(1,"median"):+.2f} |')
    L.append('')

    # ---- 3. sumbangan 2020 kepada kesan MIN ----
    L += ['## 3. Adakah kesan MIN pada band jauh didorong 2020?', '',
          '| Tingkap | Min `B7` (bawah −40%) | Min asas | Lift min |', '|---|---|---|---|']
    pul = P['pul_H126'].to_numpy('float64')
    for nama, m in (('tahan penuh 2020–2025', (th >= 2020) & (th <= 2025)),
                    ('tahan tanpa 2020', (th >= 2021) & (th <= 2025)),
                    ('2020 sahaja', th == 2020),
                    ('latih 2012–2019', (th >= 2012) & (th <= 2019))):
        base = pul[cair & np.isfinite(j52) & m]
        base = base[np.isfinite(base)]
        b7 = pul[cair & np.isfinite(j52) & (j52 < -40.0) & m]
        b7 = b7[np.isfinite(b7)]
        if not base.size or not b7.size:
            continue
        baris.append(dict(jenis='b7_tahun', tingkap=nama, min_b7=float(b7.mean() * 100),
                          min_asas=float(base.mean() * 100),
                          lift=float((b7.mean() - base.mean()) * 100)))
        L.append(f'| {nama} | {b7.mean()*100:+.2f}% | {base.mean()*100:+.2f}% | '
                 f'{(b7.mean()-base.mean())*100:+.2f} |')
    L.append('')

    # ---- 4. rumusan: mengapa MIN dan MEDIAN bertentangan ----
    R = pd.read_csv(KELUAR / 'jarak_52w.csv')
    I2 = pd.read_csv(KELUAR / 'jarak_52w_ic.csv')
    T = R[(R.varian == 'j52') & (R.band != 'ASAS') & (R.tingkap == 'tahan')]
    n_semua = int((T.gate0 & T.gate1 & T.gate2 & T.gate3).sum())
    ic_ok = []
    for N in UFUK:
        a2 = I2[(I2.tingkap == 'latih') & (I2.ufuk == N)]
        b2 = I2[(I2.tingkap == 'tahan') & (I2.ufuk == N)]
        if not len(a2) or not len(b2):
            continue
        a2, b2 = a2.iloc[0], b2.iloc[0]
        sama = np.sign(a2.ic_min) == np.sign(b2.ic_min)
        ic_ok.append((N, sama, abs(a2.t_nw) >= 2, abs(b2.t_nw) >= 2,
                      float(a2.ic_min), float(b2.ic_min)))
    L += ['## 4. Rumusan diagnostik', '',
          f'Lulus kesemua gate band (gate0–gate3): **{n_semua}/40**. Satu-satunya yang lulus '
          'ialah `B7×X13`, dan §3 menunjukkan liftnya **+8.82 mata dengan 2020 di dalam, +0.80 '
          'tanpa 2020, +0.16 dalam latih** — iaitu ia peristiwa SATU TAHUN, bukan kesan berulang. '
          'Pada 2020 sahaja `B7` memberi +84.30% lawan asas +41.84%. Tambah kaveat alam '
          '(`SPEC_52W.md` §2: tiada delist, jadi saham yang jatuh 40% dan mati tiada dalam '
          'alam), dan dakwaan "beli jauh di bawah tinggi 52w" **tidak boleh dibuat**.', '',
          '**Punca percanggahan MIN lawan MEDIAN (tidak dijangka dalam spec):** `j52` berkorelasi '
          'dengan KEDUDUKAN PASARAN dalam kitarannya, bukan hanya dengan saham. Pada Mac 2020 '
          'hampir setiap saham berada > 40% di bawah tinggi 52w, jadi band mutlak `B7` '
          'mengumpulkan bar yang bertarikh pada DASAR pasaran — pulangan hadapannya tinggi untuk '
          'SEMUA nama, bukan kerana pemilihan saham. Jadual band §2 oleh itu mengukur '
          '**pemasaan pasaran**, bukan pemilihan saham. Desil (§4 laporan utama) dikira '
          '**dalam hari yang sama**, jadi ia bebas daripada confound itu — dan di sana arahnya '
          'BERTENTANGAN: nama yang lebih HAMPIR tinggi 52w memberi median lebih tinggi.', '']
    L += ['| Ufuk | IC latih | IC tahan | Tanda sama | t≥2 latih | t≥2 tahan |',
          '|---|---|---|---|---|---|']
    for N, sama, ta, tb, ia, ib in ic_ok:
        L.append(f'| {N} | {ia:+.4f} | {ib:+.4f} | {"ya" if sama else "tidak"} | '
                 f'{"ya" if ta else "tidak"} | {"ya" if tb else "tidak"} |')
    L += ['', '`gate4` seperti ditulis dalam spec **GAGAL**, kerana kaki kemonotonan '
          'dipradaftar atas **MIN** desil dan min desil bertukar tanda antara tingkap '
          '(rho +0.92 latih → −0.96 tahan pada 63 sesi). Kaki IC **LULUS** pada 21 dan 63 '
          'sesi: tanda sama dan |t| ≥ 2 dalam kedua-dua tingkap. Itu kesilapan spec saya, '
          'bukan penemuan: saya sepatutnya menulis kaki kemonotonan atas MEDIAN kerana min '
          'desil mewarisi masalah ekor yang kajian ini sudah tahu ada.', '',
          '**Jangkaan priori §9 saya: SALAH pada 2 daripada 4.** Betul: (1) band tidak '
          'monoton; (2) band jauh min tertinggi. Salah: (3) saya ramal `|IC| < 0.02` dan tidak '
          'stabil — IC sebenarnya **+0.032 hingga +0.116**, bertanda sama dalam dua tingkap, '
          'positif dalam **10 daripada 14 tahun**; (4) saya ramal 0/40 lulus — 1/40 lulus. '
          'Kali KEEMPAT berturut-turut jangkaan priori saya salah pada ruang belum diukur.', '']
    pd.DataFrame(baris).to_csv(KELUAR / 'jarak_52w_diag.csv', index=False)
    (KELUAR / 'JARAK_52W_DIAG.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('siap: REVERSE/JARAK_52W_DIAG.md')
    _ = (UFUK, XK, t_nw, asas_m)


if __name__ == '__main__':
    main()
