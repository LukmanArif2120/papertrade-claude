# Pelan dan pekerja shard A03 (SPEC_A03 §4 peringkat 2): tugasan (kaedah, lorong, kajian 0–7) bagi 10 sistem utama dalam
# hasil_a03/pilihan.json; tala_a03.tala (sistem utama: F + M + 5 slot + had rugi 8%). Pelan = pekerja_a02.rancang.
#   python3 pekerja_a03.py --rancang --percubaan 120 --shard 20 --plan plan_a03.json [--kajian 0-7] [--github-output]
#   python3 pekerja_a03.py --shard 0 --plan plan_a03.json --proses 4 [--had-minit 330]
import os, sys, json, time, argparse
from multiprocessing import get_context

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tala_a03 as T3
import tala_a02 as T2
import tala as T1
import pekerja_a02 as PA
from pekerja import panaskan, _sudah
from gabung_hasil import versi_kod

_G = {}


def _mula(dir_, tamat, n, had, keluar):
    _G.update(dir=dir_, tamat=tamat, n=n, had=had, keluar=keluar)


def _kerja(t):
    nama = T2.nama_tugas(t['kaedah'], t['lorong'])
    if time.time() > _G['tamat'] - 120:
        H = dict(kaedah=nama, id_kaedah=t['kaedah'], lorong=t['lorong'], kajian=t['kajian'], status='RALAT', versi='A03',
                 ralat=['had masa shard: tidak dimulakan'], n_trials=0, masa={},
                 mula=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
        baru = not os.path.exists(PA._f(_G['keluar'], t))
        if baru: T1.simpan(H, _G['keluar'])
        return dict(H, _ditulis=baru)
    H = T3.tala(t['kaedah'], t['lorong'], t['kajian'], T1.Sumber(_G['dir']), _G['eps'], _G['n'], _G['had'],
                tamat=_G['tamat'] - 60, keluar=_G['keluar'])
    R = {k: H.get(k) for k in ('kaedah', 'kajian', 'status', 'n_trials', 'masa', 'rss_mb', 'ralat')}
    R['_ditulis'] = True
    return R


def pekerja(x):
    t0 = time.time(); tamat = t0 + x.had_minit * 60
    P = json.load(open(x.plan)); n = int(P['percubaan'])
    tugas = sorted(P['shard'][x.shard], key=lambda t: -t['kos'])
    if not x.semula:
        tugas = [t for t in tugas if not _sudah(PA._f(x.keluar, t), n, versi_kod(t['kaedah']))]
    dir_ = str(T2.ambil_data(x.cache)); panaskan()
    _G['eps'] = T3.muat_eps(T3.ambil_fundamental(x.fund))      # dikongsi proses anak (fork)
    print(f'A03 shard {x.shard}: {len(tugas)} tugasan, {x.proses} proses, had {x.had_minit} minit', flush=True)
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
    print(f'A03 shard {x.shard} selesai: {siap} SIAP, {ralat} RALAT, {round((time.time() - t0) / 60, 1)} minit')


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument('--rancang', action='store_true'); a.add_argument('--kajian', default='0-7')
    a.add_argument('--percubaan', type=int, default=T2.PERCUBAAN)
    a.add_argument('--pilihan', default=os.path.join(T3.HASIL, 'pilihan.json'))
    a.add_argument('--saringan', default=os.path.join(T3.HASIL, 'saringan.csv'))
    a.add_argument('--github-output', action='store_true')
    a.add_argument('--shard', type=int, default=20); a.add_argument('--plan', default='plan_a03.json')
    a.add_argument('--proses', type=int, default=4); a.add_argument('--had-minit', type=float, default=330)
    a.add_argument('--had-tugas', type=float, default=T2.HAD_MINIT)
    a.add_argument('--cache', default=os.environ.get('AUTOTUNE_CACHE', T3.CACHE))
    a.add_argument('--fund', default=T3.CACHE_F)
    a.add_argument('--keluar', default=T3.KELUAR); a.add_argument('--semula', action='store_true')
    x = a.parse_args(argv)
    if x.rancang:
        P = PA.rancang(x.pilihan, x.saringan, T1.senarai_kajian(x.kajian), x.percubaan, x.shard)
        P['versi'] = 'A03'
        json.dump(P, open(x.plan, 'w'), indent=1)
        b = P['beban']
        print(f"{P['n_tugas']} tugasan, {len(b)} shard; beban min/maks {min(b)}/{max(b)}")
        if x.github_output and os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f: f.write(f"matriks={json.dumps(list(range(len(b))))}\n")
        return
    pekerja(x)


if __name__ == '__main__':
    main()
