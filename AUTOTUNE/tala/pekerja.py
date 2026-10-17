# Pekerja shard: jalankan tugasan satu shard daripada plan.json dalam kolam proses (maxtasksperchild=1:
# setiap tugasan proses baharu, memori dibebaskan). Setiap tugasan menulis AUTOTUNE/hasil/tala/Mxx/kNN.json.
# Guna: python3 pekerja.py --shard 0 --plan plan.json --proses 4 [--had-minit 335] [--cache AUTOTUNE/.cache]
import os, sys, json, time, argparse
from multiprocessing import get_context

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tala

_G = {}


def _mula(dir_, tamat, n, had_tugas, keluar):
    _G.update(dir=dir_, tamat=tamat, n=n, had=had_tugas, keluar=keluar)


def _kerja(t):
    if time.time() > _G['tamat'] - 120:
        H = dict(kaedah=t['kaedah'], kajian=t['kajian'], status='RALAT', ralat=['had masa shard: tidak dimulakan'],
                 n_trials=0, masa={})
        tala.simpan(H, _G['keluar']); return H
    H = tala.tala(t['kaedah'], t['kajian'], tala.Sumber(_G['dir']), _G['n'], _G['had'], tamat=_G['tamat'] - 60,
                  keluar=_G['keluar'])
    return {k: H.get(k) for k in ('kaedah', 'kajian', 'status', 'n_trials', 'masa', 'rss_mb', 'ralat')}


def _sudah(f, n):
    try:
        H = json.load(open(f))
        return (H.get('status') == 'SIAP' and H.get('n_trials_diminta', 0) >= n
                and H.get('n_trials', 0) >= H.get('n_sasaran', n))
    except Exception: return False


def panaskan():
    """Kompil numba sekali dalam induk (cache=True) supaya proses anak tidak mengkompil serentak."""
    import numpy as np, pandas as pd
    import enjin_at as E
    ix = pd.bdate_range('2020-01-01', periods=30)
    g = pd.DataFrame(dict(open=1.0, high=1.1, low=0.9, close=1.0, volume=1e6, sig=False, stop=np.nan, tgt=np.nan,
                          exitc=False, rank=0.0), index=ix)
    g.iloc[5, g.columns.get_loc('sig')] = True
    T = E.trades({'X': g}, None, 2, mula=ix[1], akhir=ix[-1]); E.portfolio(T, {'X': g}, mula=ix[0], akhir=ix[-1])


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument('--shard', type=int, required=True); a.add_argument('--plan', default='plan.json')
    a.add_argument('--proses', type=int, default=4); a.add_argument('--had-minit', type=float, default=335)
    a.add_argument('--had-tugas', type=float, default=tala.HAD_MINIT)
    a.add_argument('--cache', default=os.environ.get('AUTOTUNE_CACHE', 'AUTOTUNE/.cache'))
    a.add_argument('--keluar', default=tala.KELUAR); a.add_argument('--semula', action='store_true')
    x = a.parse_args(argv)
    t0 = time.time(); tamat = t0 + x.had_minit * 60
    P = json.load(open(x.plan)); n = int(P['percubaan'])
    tugas = sorted(P['shard'][x.shard], key=lambda t: -t['kos'])
    if not x.semula:
        tugas = [t for t in tugas if not _sudah(os.path.join(x.keluar, t['kaedah'], f"k{t['kajian']:02d}.json"), n)]
    import data
    dir_ = str(data.ambil(x.cache))
    panaskan()
    print(f'shard {x.shard}: {len(tugas)} tugasan, {x.proses} proses, had {x.had_minit} minit', flush=True)
    siap = ralat = 0; R = []
    ctx = get_context('fork')
    with ctx.Pool(x.proses, initializer=_mula, initargs=(dir_, tamat, n, x.had_tugas, x.keluar), maxtasksperchild=1) as p:
        for H in p.imap_unordered(_kerja, tugas):
            R.append(H)
            if H.get('status') == 'SIAP': siap += 1
            else: ralat += 1
            m = H.get('masa') or {}
            print(f"{H['kaedah']} k{H['kajian']:02d} {H.get('status')} n={H.get('n_trials')} "
                  f"s/cuba={m.get('s_percubaan')} jumlah={m.get('jumlah')} rss={H.get('rss_mb')}MB "
                  f"{(H.get('ralat') or [''])[0][:80]}", flush=True)
    print(f'shard {x.shard} selesai: {siap} SIAP, {ralat} RALAT, {round((time.time() - t0) / 60, 1)} minit')


if __name__ == '__main__':
    main()
