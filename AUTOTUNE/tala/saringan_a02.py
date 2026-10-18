# Saringan A02 (SPEC_A02 §3 peringkat 1): semua kaedah × 2 lorong, PARAM asal, 2013-01-01 – 2018-12-31,
# kumpulan A dan B. Skor = min(lebihan A, lebihan B) atas SPY tempoh sama. Pilih 20 teratas setiap lorong.
# Pekerja (satu shard; satu proses baharu setiap kaedah; sedia() sekali, 2 lorong × 2 kumpulan):
#   python3 saringan_a02.py --shard 0 --n-shard 20 --proses 4 [--cache AUTOTUNE/.cache_a02] [--keluar DIR]
#   → DIR/<ID>.json (satu fail setiap kaedah; rekod kedua-dua lorong)
# Gabung: python3 saringan_a02.py --gabung DIR1 [DIR2 ...] [--pilih 20]
#   → AUTOTUNE/hasil_a02/saringan.csv, AUTOTUNE/hasil_a02/pilihan.json
import os, sys, json, time, math, argparse, glob, traceback, warnings
from multiprocessing import get_context
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tala_a02 as T2
import tala as T1
from tala import E, O

KELUAR_J = os.path.join(T2.HASIL, 'saringan')
CSV = os.path.join(T2.HASIL, 'saringan.csv')
PILIHAN = os.path.join(T2.HASIL, 'pilihan.json')
N_PILIH = 20
LAJUR = ['kaedah', 'lorong', 'skor', 'lebihan_A', 'lebihan_B', 'cagr_A', 'cagr_B', 'spy_A', 'spy_B', 'mdd_A', 'mdd_B',
         'spy_mdd_A', 'spy_mdd_B', 'n_A', 'n_B', 'hari_A', 'hari_B', 'menang_A', 'menang_B', 'sr_lebih_A', 'sr_lebih_B',
         'hari_siri', 'tmax_asal', 'n_tala', 'silang', 'panas_hari', 'status', 'ralat', 'saat']
_G = {}


def sr_lebih(rh, spy_r):
    """SR harian pulangan berlebihan (strategi − SPY), tarikh sama."""
    x = (rh - spy_r.reindex(rh.index).fillna(0.0)).dropna()
    if len(x) < 30 or x.std() == 0: return float('nan')
    return float(x.mean() / x.std())


def saring(mid, sumber, mula=T2.SARING[0], akhir=T2.SARING[1]):
    """Rekod {lorong: baris} bagi satu kaedah (PARAM asal)."""
    t0 = time.time(); B0, B1 = pd.Timestamp(mula), pd.Timestamp(akhir)
    out = {}
    asas = dict(kaedah=mid, status='RALAT', ralat='')
    try:
        m = T1.muat_kaedah(mid)
        panas = pd.Timedelta(days=O.panas_a02(m))
        asas.update(tmax_asal=m.TMAX, n_tala=len(m.TALA), silang=bool(m.SILANG), panas_hari=int(panas.days))
        fr, idx, univ = sumber.muat(B0 - panas, B1, 'AB')
        pn = T2.Penilai02(m, fr, idx, univ, sumber, B0, B1, ['A', 'B'])
        hs = pn.jalan02({}, ['A', 'B'], T2.LORONG, harian=True)
        for lo in T2.LORONG:
            r = dict(asas, lorong=lo, status='SIAP')
            for g in ('A', 'B'):
                mt, rh, _ = hs[(lo, g)]
                r.update({f'lebihan_{g}': mt['lebihan'], f'cagr_{g}': mt['cagr'], f'spy_{g}': mt['spy_cagr'],
                          f'mdd_{g}': mt['mdd'], f'spy_mdd_{g}': mt['spy_mdd'], f'n_{g}': mt['n'], f'hari_{g}': mt['days'],
                          f'menang_{g}': mt['win'], f'sr_lebih_{g}': sr_lebih(rh, pn.spy_r)})
                r['hari_siri'] = len(rh)
            r['skor'] = min(r['lebihan_A'], r['lebihan_B'])
            out[lo] = r
    except Exception as e:
        for lo in T2.LORONG:
            out[lo] = dict(asas, lorong=lo, ralat=f'{type(e).__name__}: {e}'[:300], jejak=traceback.format_exc()[-800:])
    for r in out.values(): r['saat'] = round(time.time() - t0, 1)
    return out


def _mula(dir_, keluar):
    _G.update(dir=dir_, keluar=keluar)


def _kerja(mid):
    warnings.filterwarnings('ignore')
    R = saring(mid, T1.Sumber(_G['dir']))
    f = os.path.join(_G['keluar'], f'{mid}.json')
    tmp = f'{f}.{os.getpid()}.tmp'
    with open(tmp, 'w') as fh: json.dump(T1._bulat(R), fh, separators=(',', ':'))
    os.replace(tmp, f)
    return mid, {lo: (r.get('status'), r.get('skor'), r.get('ralat', '')[:80]) for lo, r in R.items()}, R['had60'].get('saat')


def shard(ids, i, n):
    """Pembahagian tetap: kaedah ke-j (susunan nombor) ke shard j mod n."""
    return [m for j, m in enumerate(ids) if j % n == i]


def pekerja(x):
    import pekerja as PK
    ids = shard(T1.semua_kaedah(), x.shard, x.n_shard)
    os.makedirs(x.keluar, exist_ok=True)
    dir_ = str(T2.ambil_data(x.cache)); PK.panaskan()
    print(f'saringan shard {x.shard}: {len(ids)} kaedah', flush=True)
    with get_context('fork').Pool(x.proses, initializer=_mula, initargs=(dir_, x.keluar), maxtasksperchild=1) as p:
        for mid, s, saat in p.imap_unordered(_kerja, ids):
            print(mid, s, f'{saat}s', flush=True)


def pilih(D, n=N_PILIH):
    """{lorong: [ID ...]} — n teratas setiap lorong ikut skor, antara baris SIAP yang ada parameter TALA."""
    out = {}
    for lo in T2.LORONG:
        d = D[(D.lorong == lo) & (D.status == 'SIAP') & (D.n_tala > 0)].dropna(subset=['skor'])
        out[lo] = d.sort_values(['skor', 'kaedah'], ascending=[False, True]).kaedah.head(n).tolist()
    return out


def gabung(dirs, n=N_PILIH, csv=CSV, pilihan=PILIHAN):
    R = []
    for d in dirs:
        for f in sorted(glob.glob(os.path.join(d, '**', 'M*.json'), recursive=True)):
            try: J = json.load(open(f))
            except Exception: continue
            R += [r for r in J.values() if isinstance(r, dict)]
    D = pd.DataFrame(R)
    for c in LAJUR:
        if c not in D: D[c] = np.nan
    D = D[LAJUR].drop_duplicates(['kaedah', 'lorong'], keep='last')
    D['_n'] = pd.to_numeric(D.kaedah.str[1:], errors='coerce')
    D = D.sort_values(['_n', 'lorong']).drop(columns='_n')
    os.makedirs(os.path.dirname(csv), exist_ok=True)
    D.to_csv(csv, index=False, float_format='%.6g')
    P = pilih(D, n)
    J = dict(dicipta=pd.Timestamp.now('UTC').strftime('%Y-%m-%dT%H:%M:%SZ'), n_pilih=n, tempoh=list(T2.SARING),
             peraturan='skor = min(lebihan A, lebihan B) atas SPY tempoh sama; PARAM asal; SIAP dan ada parameter TALA',
             n_saringan=int(len(D)), n_siap=int((D.status == 'SIAP').sum()), pilihan=P,
             tugas=[T2.nama_tugas(m, lo) for lo in T2.LORONG for m in P[lo]])
    with open(pilihan, 'w') as fh: json.dump(J, fh, indent=1)
    return D, J


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument('--shard', type=int); a.add_argument('--n-shard', type=int, default=20)
    a.add_argument('--proses', type=int, default=4)
    a.add_argument('--cache', default=os.environ.get('AUTOTUNE_CACHE', T2.CACHE))
    a.add_argument('--keluar', default=KELUAR_J)
    a.add_argument('--gabung', nargs='*'); a.add_argument('--pilih', type=int, default=N_PILIH)
    x = a.parse_args(argv)
    if x.gabung is not None:
        D, J = gabung(x.gabung or [KELUAR_J], x.pilih)
        print(f"saringan: {len(D)} baris, SIAP {J['n_siap']}; pilihan: " +
              '; '.join(f"{lo} {len(v)}: {','.join(v)}" for lo, v in J['pilihan'].items()))
        return
    pekerja(x)


if __name__ == '__main__':
    main()
