"""Ukur `N16`/`N17`/`N75` terhadap keluar `X13`. Pradaftar `REVERSE/SPEC_JEJAK_N.md` §8b.

`nxx_keluar.csv` hanya menguji `ASAS`, `N19`, `N115` terhadap 23 keluar, jadi tiga topeng
yang melepasi gate2 dalam `nxx.csv` tidak pernah diukur pada keluar yang jejak hadapan
gunakan. Skrip ini mengisi sel itu — enjin, panel, tingkap, kos dan model keluar diguna
semula daripada `step19_nxx_keluar` tanpa perubahan.

Ini BUKAN eksperimen ketujuh. Ruang MASUK kekal DITUTUP (280 ujian, gate3 = 0); ukuran ini
menetapkan jangkaan priori bagi kohort jejak, dan peraturan keputusan (kodkan jika dan hanya
jika keempat-empat: jangkaan_latih > 0, jangkaan_tahan > 0, lift_latih > 0, lift_tahan > 0)
dikomit dalam spec SEBELUM larian ini.

`N115` disertakan sebagai KAWALAN REGRESI: nilainya mesti menghasilkan semula
`nxx_keluar.csv` baris `N115 x X13` dengan tepat, jika tidak laluan kod ini berbeza daripada
yang menghasilkan nombor terbitan dan keputusan tidak boleh dipercayai.

Guna: python3 REVERSE/step30_nxx_x13.py
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
import REVERSE.step18_nxx as S18           # noqa: E402
import REVERSE.step19_nxx_keluar as S19    # noqa: E402

KELUAR = AKAR / 'REVERSE'
TOPENG = ['N16', 'N17', 'N75', 'N115', 'ASAS']   # N115 = kawalan regresi
KOD = 'X13'


def main():
    t0 = time.time()
    rsf = S18.rs_persentil()
    kel = S18.kelompok_ticker()
    AK = {}
    print(f'{len(kel)} kelompok x 1 keluar ({KOD}) x {len(TOPENG)} masuk...', flush=True)
    for i, bk in enumerate(kel):
        P = S18._sedia(bk, S18.PUL, rsf)
        T = S18.topeng(P)
        PU = S19.pulangan_keluar(P)
        th = P.date.dt.year.to_numpy()
        cair = P.nilai20.to_numpy() >= S19.CAIR
        W = {'latih': (th >= S19.LATIH[0]) & (th <= S19.LATIH[1]) & cair,
             'tahan': (th >= S19.TAHAN[0]) & (th <= S19.TAHAN[1]) & cair}
        msk = {nm: (np.ones(len(P), bool) if nm == 'ASAS' else T[nm]) for nm in TOPENG}
        pu = PU[KOD]
        ada = np.isfinite(pu)
        for w, wm in W.items():
            for nm in TOPENG:
                sel = msk[nm] & wm & ada
                if not sel.any():
                    continue
                x = pu[sel]
                ak = AK.setdefault((nm, w), [0.0, 0, 0, 0.0, 0.0])
                ak[0] += float(x.sum()); ak[1] += int(x.size)
                pos = x > 0
                ak[2] += int(pos.sum()); ak[3] += float(x[pos].sum())
                ak[4] += float(x[~pos].sum())
        del P, T, PU
        print(f'    [{time.time() - t0:.0f}s] kelompok {i + 1}/{len(kel)}', flush=True)

    asas = {w: AK[('ASAS', w)][0] / AK[('ASAS', w)][1] * 100 for w in ('latih', 'tahan')}
    baris = []
    for nm in TOPENG:
        if nm == 'ASAS':
            continue
        r = dict(masuk=nm, keluar=KOD)
        for w in ('latih', 'tahan'):
            a = AK.get((nm, w))
            if a is None:
                r[f'jangkaan_{w}'] = r[f'lift_{w}'] = np.nan
                r[f'n_{w}'] = 0
                continue
            j = a[0] / a[1] * 100
            r[f'jangkaan_{w}'] = j
            r[f'lift_{w}'] = j - asas[w]
            r[f'n_{w}'] = a[1]
        a = AK[(nm, 'tahan')]
        r['menang'] = a[2] / a[1] * 100
        r['untung'] = a[3] / a[2] * 100 if a[2] else np.nan
        r['rugi'] = a[4] / (a[1] - a[2]) * 100 if a[1] - a[2] else np.nan
        r['asas_latih'], r['asas_tahan'] = asas['latih'], asas['tahan']
        r['lulus'] = bool(r['jangkaan_latih'] > 0 and r['jangkaan_tahan'] > 0
                          and r['lift_latih'] > 0 and r['lift_tahan'] > 0)
        baris.append(r)
    H = pd.DataFrame(baris)
    H.to_csv(KELUAR / 'nxx_x13.csv', index=False, float_format='%.4f')

    print()
    print('=' * 92)
    print(f'Asas {KOD}: latih {asas["latih"]:+.3f}%  tahan {asas["tahan"]:+.3f}%')
    print('=' * 92)
    lj = ['masuk', 'jangkaan_latih', 'jangkaan_tahan', 'lift_latih', 'lift_tahan',
          'menang', 'untung', 'rugi', 'n_tahan', 'lulus']
    print(H[lj].to_string(index=False, float_format=lambda v: f'{v:+.3f}'))
    print()
    print('KAWALAN REGRESI — N115 x X13 mesti sepadan nxx_keluar.csv:')
    ref = pd.read_csv(KELUAR / 'nxx_keluar.csv')
    ref = ref[(ref.masuk == 'N115') & (ref.keluar == 'X13')]
    got = H[H.masuk == 'N115'].iloc[0]
    ok = True
    for k in ('jangkaan_latih', 'jangkaan_tahan', 'lift_latih', 'lift_tahan', 'menang'):
        if k not in ref.columns:
            continue
        a, b = float(ref.iloc[0][k]), float(got[k])
        d = abs(a - b)
        ok &= d < 0.002
        print(f'  {k:<16} terbitan {a:+9.4f}  kini {b:+9.4f}  |d| {d:.2e}  '
              f'{"OK" if d < 0.002 else "<<< TERPESONG"}')
    print(f'  -> kawalan {"LULUS" if ok else "GAGAL — JANGAN percaya keputusan"}')
    print()
    print('KEPUTUSAN (peraturan spec §8b, dikomit sebelum larian):')
    for r in baris:
        if r['masuk'] == 'N115':
            continue
        print(f"  {r['masuk']:<6} -> {'KODKAN' if r['lulus'] else 'JANGAN KODKAN'}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
