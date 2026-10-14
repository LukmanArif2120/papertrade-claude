"""Pemasangan sesi berjadual.
  python3 pasang.py kod FAIL_KOD.json DEST          -> tulis semua fail kod ke DEST
  python3 pasang.py aset STATUS.json DIR_ASET DEST  -> salin aset harga ke DEST/data/
  python3 pasang.py status --scan OUT/status.json --lama STATUS_LAMA.json --run RUN [--aset A=id ...] --out STATUS_BARU.json
  python3 pasang.py lama STATUS.json                -> cetak run lama untuk dipadam (simpan 8 terkini)
"""
import json, os, sys, shutil, glob

NAMA = {'A': 'harga_A.csv', 'B': 'harga_B.csv', 'idx': 'harga_idx.csv', 'univ': 'univ.csv'}


def kod(src, dest):
    f = json.load(open(src))
    for p, c in f.items():
        q = os.path.join(dest, p); os.makedirs(os.path.dirname(q) or '.', exist_ok=True); open(q, 'w').write(c)
    os.makedirs(os.path.join(dest, 'data'), exist_ok=True)
    print(len(f), 'fail ditulis ke', dest)


def aset(st, d, dest):
    s = json.load(open(st)); a = s.get('harga_aset', {})
    os.makedirs(os.path.join(dest, 'data'), exist_ok=True)
    for k, nm in NAMA.items():
        if k not in a: print('TIADA aset', k); continue
        f = glob.glob(os.path.join(d, a[k] + '*'))
        if not f: print('TIADA fail untuk', k, a[k]); continue
        shutil.copy(f[0], os.path.join(dest, 'data', nm)); print(k, '->', nm)


def status(args):
    import argparse
    p = argparse.ArgumentParser(); p.add_argument('--scan'); p.add_argument('--lama'); p.add_argument('--run'); p.add_argument('--aset', nargs='*', default=[]); p.add_argument('--out')
    a = p.parse_args(args)
    lama = json.load(open(a.lama)) if a.lama and os.path.exists(a.lama) else {}
    baru = json.load(open(a.scan)) if a.scan and os.path.exists(a.scan) else {}
    lama.update(baru)
    if a.run:
        runs = [r for r in lama.get('runs', []) if r != a.run] + [a.run]
        lama['runs'] = runs[-12:]; lama['run_terkini'] = a.run
    ha = lama.get('harga_aset', {})
    for x in a.aset:
        k, v = x.split('=', 1); ha[k] = v
    lama['harga_aset'] = ha
    json.dump(lama, open(a.out, 'w'), ensure_ascii=False, indent=1); print(json.dumps({k: lama[k] for k in ['run_terkini', 'harga_aset'] if k in lama}))


def lama_run(st):
    s = json.load(open(st)); runs = s.get('runs', [])
    print(json.dumps(runs[:-8]))


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'kod': kod(sys.argv[2], sys.argv[3])
    elif c == 'aset': aset(sys.argv[2], sys.argv[3], sys.argv[4])
    elif c == 'status': status(sys.argv[2:])
    elif c == 'lama': lama_run(sys.argv[2])
