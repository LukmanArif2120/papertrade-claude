# Bungkus folder kod/ menjadi satu fail JSON {laluan: kod} untuk dimuat naik sebagai aset kod dashboard
# (status `harian/status` -> `harga_aset.kod`). Repo ialah sumber kebenaran; aset hanya salinan.
# Guna: python3 BacktestShariah2/standard/bungkus_kod.py OUT.json [--banding ASET_LAMA.json]
import sys, os, json, argparse

KOD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'kod')


def bungkus():
    out = {}
    for akar, dirs, fail in os.walk(KOD):
        dirs[:] = sorted(d for d in dirs if d != '__pycache__')
        for f in sorted(fail):
            if f.endswith('.pyc') or f == 'README.md':
                continue
            p = os.path.join(akar, f)
            out[os.path.relpath(p, KOD).replace(os.sep, '/')] = open(p, encoding='utf-8').read()
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--banding', help='aset kod lama (JSON) untuk senarai perbezaan')
    a = ap.parse_args(argv)
    d = bungkus()
    json.dump(d, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(f'{len(d)} fail -> {a.out}')
    if a.banding:
        lama = json.load(open(a.banding, encoding='utf-8'))
        for k in sorted(set(d) | set(lama)):
            if k not in lama: print('BAHARU ', k)
            elif k not in d: print('DIBUANG', k)
            elif d[k] != lama[k]: print('BERUBAH', k)
        print('Sama sepenuhnya.' if d == lama else 'Ada perbezaan (lihat di atas).')


if __name__ == '__main__':
    main()
