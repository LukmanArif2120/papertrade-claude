"""Grid PENUH: 65 topeng MASUK x 23 keluar = 1,495 sel. Pradaftar `REVERSE/SPEC_GRID_PENUH.md`.

Melengkapkan grid yang jarang. `nxx.csv` ukur 65 masuk x 4 keluar asas; `nxx_keluar.csv` ukur
3 masuk x 23 keluar. Jadi "kombinasi masuk x keluar terbaik" belum pernah dikira, dan 61
daripada 65 masuk tidak pernah diukur pada keluar produksi.

Panel, topeng, keluar, tingkap, ambang cair, MIN_N dan model kos diguna semula daripada
`step18_nxx` + `step19_nxx_keluar` TANPA perubahan. Yang baharu hanyalah:
  (a) gelung masuk 3 -> 65 (topeng boolean; kos hampir sifar), dan
  (b) penyebut BH-FDR JUJUR m = bilangan sel sebenar, bukan m=8 pada satu sudut grid.

Guna: python3 REVERSE/step32_grid_penuh.py
"""
import csv
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
import REVERSE.step18_nxx as S18          # noqa: E402
import REVERSE.step19_nxx_keluar as S19   # noqa: E402

KELUAR = AKAR / 'REVERSE'
MAKS_KELUAR_SETIAP_MASUK = 3              # spec §3, had kepelbagaian
TOP = 40


def topeng_diuji():
    """Topeng MASUK berstatus DIUJI dalam registry, + keluarganya."""
    out = {}
    with (AKAR / 'BacktestShariah2' / 'data' / 'registry_N.csv').open() as fh:
        for r in csv.DictReader(fh):
            i = r['id']
            if i.startswith('N') and i[1:].isdigit() and r['status'].startswith('DIUJI'):
                out[i] = r['keluarga']
    return out


def main():
    t0 = time.time()
    KELG = topeng_diuji()
    kod = [k for k, _ in S19.XSPEC]
    rsf = S18.rs_persentil()
    kel = S18.kelompok_ticker()

    AK, PERHARI = {}, {}
    nama = None
    print(f'1/3 {len(kel)} kelompok x {len(kod)} keluar x ~{len(KELG)} masuk...', flush=True)
    for i, bk in enumerate(kel):
        P = S18._sedia(bk, S18.PUL, rsf)
        T = S18.topeng(P)
        PU = S19.pulangan_keluar(P)
        th = P.date.dt.year.to_numpy()
        hari = P.date.to_numpy().astype('datetime64[D]').astype('int64')
        cair = P.nilai20.to_numpy() >= S19.CAIR
        W = {'latih': (th >= S19.LATIH[0]) & (th <= S19.LATIH[1]) & cair,
             'tahan': (th >= S19.TAHAN[0]) & (th <= S19.TAHAN[1]) & cair}
        if nama is None:
            nama = ['ASAS'] + sorted((k for k in KELG if k in T), key=lambda x: int(x[1:]))
            print(f'  {len(nama) - 1} topeng DIUJI hadir dalam panel '
                  f'-> {(len(nama) - 1) * len(kod):,} sel', flush=True)
        msk = {nm: (np.ones(len(P), bool) if nm == 'ASAS' else np.asarray(T[nm], bool))
               for nm in nama}
        for k in kod:
            pu = PU[k]
            ada = np.isfinite(pu)
            for w, wm in W.items():
                base = wm & ada
                for nm in nama:
                    sel = msk[nm] & base
                    if not sel.any():
                        continue
                    x = pu[sel]
                    ak = AK.setdefault((nm, k, w), [0.0, 0, 0, 0.0, 0.0])
                    ak[0] += float(x.sum()); ak[1] += int(x.size)
                    pos = x > 0
                    ak[2] += int(pos.sum()); ak[3] += float(x[pos].sum())
                    ak[4] += float(x[~pos].sum())
                    if w == 'tahan':                     # SE berkelompok ikut hari beli
                        ph = PERHARI.setdefault((nm, k), {})
                        hh = hari[sel]
                        o = np.argsort(hh, kind='stable')
                        hs, xs = hh[o], x[o]
                        b = np.flatnonzero(np.concatenate(
                            [[True], hs[1:] != hs[:-1], [True]]))
                        sm, cn = np.add.reduceat(xs, b[:-1]), np.diff(b)
                        for d, sv, cv in zip(hs[b[:-1]], sm, cn):
                            e = ph.get(d)
                            if e is None:
                                ph[d] = [sv, int(cv)]
                            else:
                                e[0] += sv; e[1] += int(cv)
        del P, T, PU
        print(f'    [{time.time() - t0:.0f}s] kelompok {i + 1}/{len(kel)}', flush=True)

    from scipy import stats as sps
    asas = {(k, w): AK[('ASAS', k, w)][0] / AK[('ASAS', k, w)][1] * 100
            for k in kod for w in ('latih', 'tahan') if ('ASAS', k, w) in AK}
    baris = []
    for nm in nama:
        if nm == 'ASAS':
            continue
        for k in kod:
            r = dict(masuk=nm, keluarga=KELG.get(nm, ''), keluar=k,
                     peraturan=dict(S19.XSPEC).get(k, ''))
            ok = True
            for w in ('latih', 'tahan'):
                a = AK.get((nm, k, w))
                if a is None or a[1] == 0:
                    ok = False
                    break
                j = a[0] / a[1] * 100
                r[f'jangkaan_{w}'] = j
                r[f'lift_{w}'] = j - asas[(k, w)]
                r[f'n_{w}'] = a[1]
            if not ok:
                continue
            a = AK[(nm, k, 'tahan')]
            r['menang'] = a[2] / a[1] * 100
            r['untung'] = a[3] / a[2] * 100 if a[2] else np.nan
            r['rugi'] = a[4] / (a[1] - a[2]) * 100 if a[1] - a[2] else np.nan
            r['asas_latih'], r['asas_tahan'] = asas[(k, 'latih')], asas[(k, 'tahan')]
            ph = PERHARI.get((nm, k), {})
            if len(ph) >= 30:
                v = np.array([s / c for s, c in ph.values()]) * 100
                r['n_hari'] = len(v)
                r['t'], pp = sps.ttest_1samp(v, 0.0)
                r['p'] = pp / 2 if r['t'] > 0 else 1 - pp / 2
            else:
                r['n_hari'] = len(ph); r['t'] = r['p'] = np.nan
            baris.append(r)

    H = pd.DataFrame(baris)
    M = len(H)                                    # PENYEBUT JUJUR: setiap sel diukur
    H['s1_mutlak'] = (H.jangkaan_latih > 0) & (H.jangkaan_tahan > 0)
    H['s2_lift'] = (H.lift_latih > 0) & (H.lift_tahan > 0)
    H['s3_n'] = H.n_tahan >= S19.MIN_N
    H['s123'] = H.s1_mutlak & H.s2_lift & H.s3_n
    lulus, amb = S18.bh_m(H.p.where(H.s123).to_numpy(), M, 0.05)
    H['s4_fdr'] = lulus
    H['lulus'] = H.s123 & H.s4_fdr
    print(f'\n2/3 pas ekor bagi {int(H.s123.sum())} sel yang lulus syarat 1-3...', flush=True)

    # tanpa5 bagi semua yang lulus s1-s3 (spec §3: lajur, bukan gate)
    hidup = sorted(set(H[H.s123][['masuk', 'keluar']].itertuples(index=False, name=None)))
    kump = {kk: [] for kk in hidup}
    if hidup:
        perlu = sorted({nm for nm, _ in hidup})
        for i, bk in enumerate(kel):
            P = S18._sedia(bk, S18.PUL, rsf)
            T = S18.topeng(P)
            PU = S19.pulangan_keluar(P)
            th = P.date.dt.year.to_numpy()
            wm = ((th >= S19.TAHAN[0]) & (th <= S19.TAHAN[1])
                  & (P.nilai20.to_numpy() >= S19.CAIR))
            msk = {nm: np.asarray(T[nm], bool) for nm in perlu}
            for nm, k in hidup:
                pu = PU[k].astype('float32')
                sel = msk[nm] & wm & np.isfinite(pu)
                if sel.any():
                    kump[(nm, k)].append(pu[sel])
            del P, T, PU
            print(f'    [{time.time() - t0:.0f}s] ekor kelompok {i + 1}/{len(kel)}', flush=True)
    H['tanpa5_tahan'] = np.nan
    for (nm, k), lst in kump.items():
        if lst:
            u = np.sort(np.concatenate(lst))[::-1]
            if u.size > 20:
                H.loc[(H.masuk == nm) & (H.keluar == k), 'tanpa5_tahan'] = float(
                    u[int(np.ceil(0.05 * u.size)):].mean() * 100)

    H = H.sort_values('jangkaan_tahan', ascending=False)
    H.to_csv(KELUAR / 'grid_penuh.csv', index=False, float_format='%.6f')

    # senarai TOP: had 3 keluar setiap masuk (spec §3)
    def pilih(df, label):
        kira, out = {}, []
        for r in df.itertuples():
            if kira.get(r.masuk, 0) >= MAKS_KELUAR_SETIAP_MASUK:
                continue
            kira[r.masuk] = kira.get(r.masuk, 0) + 1
            out.append((r, label))
            if len(out) >= TOP:
                break
        return out

    utama = pilih(H[H.lulus], 'FDR')
    if len(utama) < 30:                            # spec §4
        sisa = H[H.s123 & ~H.lulus]
        kira = {}
        for r, _ in utama:
            kira[r.masuk] = kira.get(r.masuk, 0) + 1
        for r in sisa.itertuples():
            if len(utama) >= 30:
                break
            if kira.get(r.masuk, 0) >= MAKS_KELUAR_SETIAP_MASUK:
                continue
            kira[r.masuk] = kira.get(r.masuk, 0) + 1
            utama.append((r, 'TIADA_FDR'))

    print()
    print('=' * 118)
    print(f'GRID PENUH: {M:,} sel diukur · penyebut BH-FDR JUJUR m = {M:,} '
          f'(ambang {amb:.3e} kalau ada)')
    print(f'  syarat 1 jangkaan mutlak > 0 dua tingkap : {int(H.s1_mutlak.sum()):>5}/{M}')
    print(f'  syarat 2 lift > 0 dua tingkap            : {int(H.s2_lift.sum()):>5}/{M}')
    print(f'  syarat 1+2+3 (n >= {S19.MIN_N})                  : {int(H.s123.sum()):>5}/{M}')
    print(f'  syarat 4 BH-FDR pada m={M}              : {int(H.lulus.sum()):>5}/{M}')
    print('=' * 118)
    print()
    print(f'SENARAI UNTUK PAPERTRADE — {len(utama)} kombinasi '
          f'(maks {MAKS_KELUAR_SETIAP_MASUK} keluar setiap masuk)')
    print(f'{"#":>3} {"masuk":<7}{"kelg":<9}{"keluar":<6}{"jang_lat":>9}{"jang_tah":>9}'
          f'{"lift_lat":>9}{"lift_tah":>9}{"menang":>7}{"untung":>8}{"rugi":>8}'
          f'{"n_tahan":>9}{"p":>9}{"tanpa5":>8}  {"label":<9} peraturan keluar')
    for n, (r, lab) in enumerate(utama, 1):
        t5 = r.tanpa5_tahan
        print(f'{n:>3} {r.masuk:<7}{r.keluarga:<9}{r.keluar:<6}{r.jangkaan_latih:>+9.3f}'
              f'{r.jangkaan_tahan:>+9.3f}{r.lift_latih:>+9.3f}{r.lift_tahan:>+9.3f}'
              f'{r.menang:>7.1f}{r.untung:>+8.2f}{r.rugi:>+8.2f}{int(r.n_tahan):>9,}'
              f'{r.p:>9.5f}{(f"{t5:+8.3f}" if t5 == t5 else "       -")}  {lab:<9} '
              f'{r.peraturan[:34]}')
    pd.DataFrame([{**r._asdict(), 'label': lab} for r, lab in utama]).drop(
        columns=['Index'], errors='ignore').to_csv(
        KELUAR / 'grid_top40.csv', index=False, float_format='%.6f')

    print()
    print('Pecahan KELUAR dalam senarai:')
    kk = pd.Series([r.keluar for r, _ in utama]).value_counts()
    print('  ' + ' · '.join(f'{k} {v}' for k, v in kk.items()))
    print('Pecahan KELUARGA masuk dalam senarai:')
    kg = pd.Series([r.keluarga for r, _ in utama]).value_counts()
    print('  ' + ' · '.join(f'{k} {v}' for k, v in kg.items()))
    print(f'Masuk berbeza: {len({r.masuk for r, _ in utama})}')
    t5 = [r.tanpa5_tahan for r, _ in utama if r.tanpa5_tahan == r.tanpa5_tahan]
    if t5:
        print(f'tanpa5 dalam senarai: {sum(1 for x in t5 if x > 0)}/{len(t5)} POSITIF · '
              f'median {np.median(t5):+.3f}')
    print()
    print('Semakan jangkaan priori spec §5:')
    for nm, k, apa in (('N19', 'X13', 'priori 3: N19xX13 tempat 1 atau 2'),):
        sub = H[(H.masuk == nm) & (H.keluar == k)]
        if len(sub):
            pos = int((H.jangkaan_tahan > float(sub.jangkaan_tahan.iloc[0])).sum()) + 1
            print(f'  {apa} -> pangkat {pos} ({float(sub.jangkaan_tahan.iloc[0]):+.4f}%)')
    print(f'  -> grid_penuh.csv ({M:,} baris) · grid_top40.csv  [{time.time() - t0:.0f}s]')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
