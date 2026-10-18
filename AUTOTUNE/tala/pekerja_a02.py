# Pelan dan pekerja shard A02 (SPEC_A02 §3 peringkat 2). Tugasan = (kaedah, lorong, kajian 0–7) bagi kaedah-lorong
# dalam hasil_a02/pilihan.json. Kos anggaran = saat saringan kaedah (saringan.csv) × (percubaan + 3); LPT.
#   python3 pekerja_a02.py --rancang --percubaan 120 --shard 20 --keluar plan_a02.json [--kajian 0-7] [--github-output]
#   python3 pekerja_a02.py --shard 0 --plan plan_a02.json --proses 4 [--had-minit 330]
# Setiap tugasan: proses baharu (maxtasksperchild=1) → hasil_a02/tala/<ID>_<lorong>/kNN.json. Senarai fail yang ditulis:
# <keluar>/_ditulis_shard<i>.txt (hanya fail ini dimuat naik sebagai artifak; peraturan gabung_hasil.py).
import os, sys, json, time, argparse
from multiprocessing import get_context
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tala_a02 as T2
import tala as T1
from rancang import lpt
from pekerja import panaskan, _sudah
from gabung_hasil import versi_kod

_G = {}


def rancang(pilihan, saringan_csv, kajian, percubaan, n_shard):
    J = json.load(open(pilihan))
    try: S = pd.read_csv(saringan_csv).groupby('kaedah').saat.max().to_dict()
    except Exception: S = {}
    tugas = []
    for lo, ids in J['pilihan'].items():
        for mid in ids:
            s = float(S.get(mid) or 60.0)
            for k in kajian:
                f = 1.6 if k == T2.K_AKHIR else (0.6 if k == T2.K_SEMASA else 1.0)   # ujian AKHIR 7+ tahun A+B
                tugas.append(dict(kaedah=mid, lorong=lo, kajian=k, kos=round(s * f * (percubaan + 3) / 4, 1)))
    n_shard = max(1, min(n_shard, len(tugas)))
    Sh = lpt(tugas, n_shard)
    return dict(dicipta=pd.Timestamp.now('UTC').strftime('%Y-%m-%dT%H:%M:%SZ'), percubaan=percubaan, kajian=kajian,
                n_tugas=len(tugas), shard=Sh, beban=[round(sum(t['kos'] for t in s), 1) for s in Sh])


def _mula(dir_, tamat, n, had, keluar):
    _G.update(dir=dir_, tamat=tamat, n=n, had=had, keluar=keluar)


def _f(keluar, t):
    return os.path.join(keluar, T2.nama_tugas(t['kaedah'], t['lorong']), f"k{int(t['kajian']):02d}.json")


def _kerja(t):
    nama = T2.nama_tugas(t['kaedah'], t['lorong'])
    if time.time() > _G['tamat'] - 120:
        H = dict(kaedah=nama, id_kaedah=t['kaedah'], lorong=t['lorong'], kajian=t['kajian'], status='RALAT',
                 ralat=['had masa shard: tidak dimulakan'], n_trials=0, masa={},
                 mula=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
        baru = not os.path.exists(_f(_G['keluar'], t))
        if baru: T1.simpan(H, _G['keluar'])
        return dict(H, _ditulis=baru)
    H = T2.tala(t['kaedah'], t['lorong'], t['kajian'], T1.Sumber(_G['dir']), _G['n'], _G['had'],
                tamat=_G['tamat'] - 60, keluar=_G['keluar'])
    R = {k: H.get(k) for k in ('kaedah', 'kajian', 'status', 'n_trials', 'masa', 'rss_mb', 'ralat')}
    R['_ditulis'] = True
    return R


def pekerja(x):
    t0 = time.time(); tamat = t0 + x.had_minit * 60
    P = json.load(open(x.plan)); n = int(P['percubaan'])
    tugas = sorted(P['shard'][x.shard], key=lambda t: -t['kos'])
    if not x.semula:
        tugas = [t for t in tugas if not _sudah(_f(x.keluar, t), n, versi_kod(t['kaedah']))]
    dir_ = str(T2.ambil_data(x.cache)); panaskan()
    print(f'shard {x.shard}: {len(tugas)} tugasan, {x.proses} proses, had {x.had_minit} minit', flush=True)
    os.makedirs(x.keluar, exist_ok=True)
    siap = ralat = 0
    with open(os.path.join(x.keluar, f'_ditulis_shard{x.shard}.txt'), 'w') as senarai, \
            get_context('fork').Pool(x.proses, initializer=_mula, initargs=(dir_, tamat, n, x.had_tugas, x.keluar),
                                     maxtasksperchild=1) as p:
        for H in p.imap_unordered(_kerja, tugas):
            if H.get('_ditulis'):
                senarai.write(f"{H['kaedah']}/k{int(H['kajian']):02d}.json\n"); senarai.flush()
            siap += H.get('status') == 'SIAP'; ralat += H.get('status') != 'SIAP'
            m = H.get('masa') or {}
            print(f"{H['kaedah']} k{H['kajian']:02d} {H.get('status')} n={H.get('n_trials')} s/cuba={m.get('s_percubaan')} "
                  f"jumlah={m.get('jumlah')} rss={H.get('rss_mb')}MB {(H.get('ralat') or [''])[0][:80]}", flush=True)
    print(f'shard {x.shard} selesai: {siap} SIAP, {ralat} RALAT, {round((time.time() - t0) / 60, 1)} minit')


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument('--rancang', action='store_true'); a.add_argument('--kajian', default='0-7')
    a.add_argument('--percubaan', type=int, default=T2.PERCUBAAN)
    a.add_argument('--pilihan', default=os.path.join(T2.HASIL, 'pilihan.json'))
    a.add_argument('--saringan', default=os.path.join(T2.HASIL, 'saringan.csv'))
    a.add_argument('--github-output', action='store_true')
    a.add_argument('--shard', type=int, default=20); a.add_argument('--plan', default='plan_a02.json')
    a.add_argument('--proses', type=int, default=4); a.add_argument('--had-minit', type=float, default=330)
    a.add_argument('--had-tugas', type=float, default=T2.HAD_MINIT)
    a.add_argument('--cache', default=os.environ.get('AUTOTUNE_CACHE', T2.CACHE))
    a.add_argument('--keluar', default=T2.KELUAR); a.add_argument('--semula', action='store_true')
    x = a.parse_args(argv)
    if x.rancang:
        P = rancang(x.pilihan, x.saringan, T1.senarai_kajian(x.kajian), x.percubaan, x.shard)
        json.dump(P, open(x.plan, 'w'), indent=1)
        b = P['beban']
        print(f"{P['n_tugas']} tugasan, {len(b)} shard; beban min/maks {min(b)}/{max(b)}")
        if x.github_output and os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f: f.write(f"matriks={json.dumps(list(range(len(b))))}\n")
        return
    pekerja(x)


if __name__ == '__main__':
    main()
