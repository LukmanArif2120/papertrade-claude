# Pelan shard: senarai tugasan (kaedah × kajian) dibahagi kepada N shard seimbang kos (LPT).
# Kos = saat setiap percubaan × (percubaan + penilaian tambahan). Saat setiap percubaan: AUTOTUNE/hasil/tala/_masa.csv
# (median kaedah) jika ada; jika tidak, --ukur: masa sedia() atas 100 saham data 431 (× 2 bagi SILANG); jika tidak, 1.
# Guna: python3 rancang.py --kaedah semua --kajian 0-13 --percubaan 120 --shard 20 --keluar plan.json [--ukur] [--github-output]
import os, sys, json, time, argparse
from multiprocessing import Pool
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tala

MASA = os.path.join(tala.KELUAR, '_masa.csv')
SKALA_431 = 12.0   # anggaran nisbah masa percubaan sebenar (≈1000 saham × 5 tahun) lawan sedia 100 saham 431


def tambahan(k, n_tala):
    """Bilangan penilaian setara percubaan selain Optuna (ujian, dataran, bersih)."""
    return (3 if k != 13 else 0) + (4 * n_tala + 2 if k == 12 else 0) + (6 if k == 0 else 0)


def lpt(tugas, n):
    """Longest Processing Time: tugasan kos menurun → shard paling ringan."""
    S = [[] for _ in range(n)]; beban = [0.0] * n
    for t in sorted(tugas, key=lambda t: -t['kos']):
        i = int(np.argmin(beban)); S[i].append(t); beban[i] += t['kos']
    return S


_FR = {}
def _ukur(mid):
    import data, warnings
    warnings.filterwarnings('ignore')
    if 'fr' not in _FR:
        fr, idx = data.muat_431(); _FR['fr'] = {t: fr[t] for t in sorted(fr)[:100]}; _FR['idx'] = idx
    try:
        m = tala.muat_kaedah(mid); f = tala.salin(_FR['fr']); t = time.time(); m.sedia(f, _FR['idx'], dict(m.PARAM))
        return mid, time.time() - t, None
    except Exception as e:
        return mid, None, f'{type(e).__name__}: {e}'[:200]


def info_kaedah(mid):
    try:
        m = tala.muat_kaedah(mid)
        return dict(n_tala=len(m.TALA), silang=bool(m.SILANG), belum=bool(m.BELUM_DITALA) or not m.TALA)
    except Exception as e:
        return dict(n_tala=0, silang=False, belum=True, ralat=f'{type(e).__name__}: {e}'[:200])


def rancang(kaedah, kajian, percubaan, n_shard, ukur=False, proses=4):
    ids = tala.semua_kaedah() if kaedah in ('semua', '', None) else [x.strip() for x in kaedah.split(',') if x.strip()]
    ks = tala.senarai_kajian(kajian)
    info = {m: info_kaedah(m) for m in ids}
    sp = {}
    if os.path.exists(MASA):
        try:
            M = pd.read_csv(MASA).dropna(subset=['s_percubaan'])
            sp = M.groupby('kaedah').s_percubaan.median().to_dict()
        except Exception: sp = {}
    diukur = {}
    if ukur:
        perlu = [m for m in ids if m not in sp]
        if perlu:
            with Pool(proses, maxtasksperchild=20) as p:
                for mid, s, e in p.imap_unordered(_ukur, perlu): diukur[mid] = s
    tugas = []
    for m in ids:
        i = info[m]
        if m in sp: s = float(sp[m]); sumber = 'masa'
        elif diukur.get(m) is not None: s = diukur[m] * SKALA_431 * (2 if i['silang'] else 1); sumber = 'ukur'
        else: s = 1.0 * (2 if i['silang'] else 1); sumber = 'lalai'
        n = 1 if i['belum'] else percubaan
        for k in ks:
            tugas.append(dict(kaedah=m, kajian=k, kos=round(s * (n + tambahan(k, i['n_tala'])), 2), sumber=sumber))
    n_shard = max(1, min(n_shard, len(tugas)))
    S = lpt(tugas, n_shard)
    return dict(dicipta=pd.Timestamp.now('UTC').strftime('%Y-%m-%dT%H:%M:%SZ'), percubaan=percubaan, kajian=ks,
                kaedah=ids, n_tugas=len(tugas), shard=S, beban=[round(sum(t['kos'] for t in s), 1) for s in S],
                belum_ditala=[m for m in ids if info[m]['belum']])


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument('--kaedah', default='semua'); a.add_argument('--kajian', default='0-13')
    a.add_argument('--percubaan', type=int, default=tala.PERCUBAAN); a.add_argument('--shard', type=int, default=20)
    a.add_argument('--keluar', default='plan.json'); a.add_argument('--ukur', action='store_true')
    a.add_argument('--github-output', action='store_true')
    x = a.parse_args(argv)
    P = rancang(x.kaedah, x.kajian, x.percubaan, x.shard, x.ukur)
    json.dump(P, open(x.keluar, 'w'), indent=1)
    b = P['beban']
    print(f"{P['n_tugas']} tugasan, {len(P['kaedah'])} kaedah, {len(b)} shard; beban min/maks {min(b)}/{max(b)}; "
          f"belum ditala {len(P['belum_ditala'])}")
    if x.github_output and os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f: f.write(f"matriks={json.dumps(list(range(len(b))))}\n")


if __name__ == '__main__':
    main()
