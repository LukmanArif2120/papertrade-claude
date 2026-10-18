# Saringan A03 (SPEC_A03 §4 peringkat 1): 20 kaedah × 2 lorong × 4 sistem (utama + 3 ablasi), PARAM asal,
# 2013-01-01 – 2018-12-31, kumpulan A dan B. skor = min(lebihan A, lebihan B) atas SPY (rujukan); skor_menang =
# min(kadar menang A, kadar menang B). Pemilihan (SPEC_A03 §6): 10 sistem utama teratas ikut skor_menang di kalangan
# sistem dengan CAGR A dan B > 0 (kedua-dua lorong dikumpul); ablasi dilaporkan sahaja.
#   Pekerja: python3 saringan_a03.py --shard 0 --n-shard 10 --proses 2 [--cache ...] [--fund ...] [--keluar DIR]
#   Gabung : python3 saringan_a03.py --gabung DIR1 [DIR2 ...] [--pilih 10]  → hasil_a03/saringan.csv, pilihan.json
import os, sys, json, time, argparse, glob, traceback, warnings
from multiprocessing import get_context
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tala_a03 as T3
import tala_a02 as T2
import tala as T1
import saringan_a02 as S2
from tala import O

KELUAR_J = os.path.join(T3.HASIL, 'saringan')
CSV = os.path.join(T3.HASIL, 'saringan.csv')
PILIHAN = os.path.join(T3.HASIL, 'pilihan.json')
STAT = ('menang', 'pf', 'purata_untung', 'purata_rugi', 'jangkaan')
LAJUR = (['kaedah', 'lorong', 'varian', 'pakar', 'skor_menang', 'skor', 'lebihan_A', 'lebihan_B', 'cagr_A', 'cagr_B',
          'spy_A', 'spy_B', 'mdd_A', 'mdd_B', 'spy_mdd_A', 'spy_mdd_B', 'n_A', 'n_B', 'hari_A']
         + [f'{k}_{g}' for k in STAT for g in 'AB'] + ['sr_lebih_A', 'sr_lebih_B', 'tmax_asal', 'n_tala', 'panas_hari',
                                                       'status', 'ralat', 'saat'])
_G = {}


def saring(mid, sumber, eps, mula=T2.SARING[0], akhir=T2.SARING[1], varian=tuple(T3.SISTEM)):
    """Senarai baris (lorong × varian) bagi satu kaedah, PARAM asal."""
    t0 = time.time(); B0, B1 = pd.Timestamp(mula), pd.Timestamp(akhir)
    asas = dict(kaedah=mid, pakar=mid in T3.PAKAR, status='RALAT', ralat='')
    out = []
    try:
        m = T1.muat_kaedah(mid)
        panas = pd.Timedelta(days=O.panas_a02(m))
        asas.update(tmax_asal=m.TMAX, n_tala=len(m.TALA), panas_hari=int(panas.days))
        fr, idx, univ = sumber.muat(B0 - panas, B1, 'AB')
        pn = T3.Penilai03(m, fr, idx, univ, sumber, B0, B1, ['A', 'B'], eps=eps)
        hs = pn.jalan03({}, ['A', 'B'], T2.LORONG, varian, harian=True)
        for lo in T2.LORONG:
            for v in varian:
                r = dict(asas, lorong=lo, varian=v, status='SIAP')
                for g in ('A', 'B'):
                    mt, rh, _ = hs[(lo, g, v)]
                    r.update({f'lebihan_{g}': mt['lebihan'], f'cagr_{g}': mt['cagr'], f'spy_{g}': mt['spy_cagr'],
                              f'mdd_{g}': mt['mdd'], f'spy_mdd_{g}': mt['spy_mdd'], f'n_{g}': mt['n'],
                              f'sr_lebih_{g}': S2.sr_lebih(rh, pn.spy_r)})
                    st = T3.terbitan(mt['n_menang'], mt['n_kalah'], mt['jumlah_untung'], mt['jumlah_rugi'])
                    r.update({f'{k}_{g}': st[k] for k in STAT})
                    if g == 'A': r.update(hari_A=mt['days'])
                r['skor'] = min(r['lebihan_A'], r['lebihan_B'])
                r['skor_menang'] = min(r['menang_A'] if r['menang_A'] is not None else -1.0,
                                       r['menang_B'] if r['menang_B'] is not None else -1.0)
                out.append(r)
    except Exception as e:
        out = [dict(asas, lorong=lo, varian=v, ralat=f'{type(e).__name__}: {e}'[:300], jejak=traceback.format_exc()[-800:])
               for lo in T2.LORONG for v in varian]
    for r in out: r['saat'] = round(time.time() - t0, 1)
    return out


def _mula(dir_, keluar):
    _G.update(dir=dir_, keluar=keluar)


def _kerja(mid):
    warnings.filterwarnings('ignore')
    R = saring(mid, T1.Sumber(_G['dir']), _G['eps'])
    f = os.path.join(_G['keluar'], f'{mid}.json')
    with open(f + '.tmp', 'w') as fh: json.dump(T1._bulat(R), fh, separators=(',', ':'))
    os.replace(f + '.tmp', f)
    return mid, [(r['lorong'], r['varian'], r.get('status'), r.get('skor'), r.get('ralat', '')[:60]) for r in R], R[0].get('saat')


def pekerja(x):
    import pekerja as PK
    ids = S2.shard(T3.senarai_kaedah(), x.shard, x.n_shard)
    os.makedirs(x.keluar, exist_ok=True)
    dir_ = str(T2.ambil_data(x.cache)); PK.panaskan()
    _G['eps'] = T3.muat_eps(T3.ambil_fundamental(x.fund))      # dikongsi proses anak (fork)
    print(f'saringan A03 shard {x.shard}: {len(ids)} kaedah: {ids}', flush=True)
    with get_context('fork').Pool(x.proses, initializer=_mula, initargs=(dir_, x.keluar), maxtasksperchild=1) as p:
        for mid, s, saat in p.imap_unordered(_kerja, ids):
            print(mid, s, f'{saat}s', flush=True)


def pilih(D, n=T3.N_TALA):
    """10 sistem utama teratas (kaedah-lorong) ikut skor_menang = min(kadar menang A, B), di kalangan sistem dengan
    CAGR A dan B > 0; SIAP dan ada parameter TALA (SPEC_A03 §6). Seri: skor (lebihan)."""
    d = D[(D.varian == T3.UTAMA) & (D.status == 'SIAP') & (D.n_tala > 0) & (D.cagr_A > 0) & (D.cagr_B > 0)]
    d = d.dropna(subset=['skor_menang'])
    d = d.sort_values(['skor_menang', 'skor', 'kaedah', 'lorong'], ascending=[False, False, True, True]).head(n)
    return [T2.nama_tugas(r.kaedah, r.lorong) for r in d.itertuples()]


def ringkas_varian(D):
    """{varian: {lorong: dict(n, skor_pos, a_b_pos, median_skor, median_lebihan_A)}} — perbandingan utama lwn ablasi."""
    out = {}
    for v in T3.SISTEM:
        for lo in T2.LORONG:
            d = D[(D.varian == v) & (D.lorong == lo) & (D.status == 'SIAP')]
            out.setdefault(v, {})[lo] = dict(n=int(len(d)), skor_pos=int((d.skor > 0).sum()),
                                             cagr_pos=int(((d.cagr_A > 0) & (d.cagr_B > 0)).sum()),
                                             median_skor=float(d.skor.median()) if len(d) else None,
                                             median_menang_A=float(d.menang_A.median()) if len(d) else None,
                                             median_n_A=float(d.n_A.median()) if len(d) else None)
    return out


def gabung(dirs, n=T3.N_TALA, csv=CSV, pilihan=PILIHAN):
    R = []
    for d in dirs:
        for f in sorted(glob.glob(os.path.join(d, '**', 'M*.json'), recursive=True)):
            try: J = json.load(open(f))
            except Exception: continue
            R += [r for r in J if isinstance(r, dict)] if isinstance(J, list) else []
    D = pd.DataFrame(R)
    for c in LAJUR:
        if c not in D: D[c] = np.nan
    D = D[LAJUR].drop_duplicates(['kaedah', 'lorong', 'varian'], keep='last')
    D['_n'] = pd.to_numeric(D.kaedah.str[1:], errors='coerce')
    D['_v'] = D.varian.map({v: i for i, v in enumerate(T3.SISTEM)})
    D = D.sort_values(['_n', 'lorong', '_v']).drop(columns=['_n', '_v'])
    os.makedirs(os.path.dirname(csv), exist_ok=True)
    D.to_csv(csv, index=False, float_format='%.6g')
    tugas = pilih(D, n)
    P = {lo: [T2.pecah_tugas(t)[0] for t in tugas if T2.pecah_tugas(t)[1] == lo] for lo in T2.LORONG}
    J = dict(versi='A03', dicipta=pd.Timestamp.now('UTC').strftime('%Y-%m-%dT%H:%M:%SZ'), n_pilih=n,
             tempoh=list(T2.SARING), kaedah=T3.senarai_kaedah(), pakar=T3.PAKAR, lain=T3.kaedah_lain(),
             sistem=T3.keterangan_sistem(), ablasi=list(T3.ABLASI),
             peraturan='skor_menang = min(kadar menang A, B) di kalangan CAGR A dan B > 0 (SPEC_A03 §6); PARAM asal; '
                       'sistem utama sahaja; SIAP dan ada TALA',
             n_saringan=int(len(D)), n_siap=int((D.status == 'SIAP').sum()), pilihan=P, tugas=tugas,
             varian=ringkas_varian(D))
    with open(pilihan, 'w') as fh: json.dump(T1._bulat(J), fh, indent=1)
    return D, J


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument('--shard', type=int); a.add_argument('--n-shard', type=int, default=10)
    a.add_argument('--proses', type=int, default=2)
    a.add_argument('--cache', default=os.environ.get('AUTOTUNE_CACHE', T3.CACHE))
    a.add_argument('--fund', default=T3.CACHE_F)
    a.add_argument('--keluar', default=KELUAR_J)
    a.add_argument('--gabung', nargs='*'); a.add_argument('--pilih', type=int, default=T3.N_TALA)
    x = a.parse_args(argv)
    if x.gabung is not None:
        D, J = gabung(x.gabung or [KELUAR_J], x.pilih)
        print(f"saringan A03: {len(D)} baris, SIAP {J['n_siap']}; pilihan {len(J['tugas'])}: {', '.join(J['tugas'])}")
        return
    pekerja(x)


if __name__ == '__main__':
    main()
