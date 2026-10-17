# AUTOTUNE F8: pembungkus tala semula suku tahun (kajian 13 SEMASA sahaja) → direktori output berasingan.
# tala.py/pekerja.py/rancang.py TIDAK diubah; pekerja.py sudah ada --keluar, rancang.py hanya membaca _masa.csv.
#   label    : cetak (dan tulis ke GITHUB_OUTPUT) label suku YYYY-Qn, cth. 2026-Q4
#   rancang  : pelan shard (semua kaedah, kajian 13) → plan.json
#   pekerja  : jalankan satu shard; hasil → AUTOTUNE/hasil/suku/<YYYY-Qn>/tala/Mxx/k13.json
# Guna: python3 AUTOTUNE/suku/jalan.py label [--suku 2026-Q4] [--github-output]
import os, sys, re, argparse, datetime

AKAR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HASIL = os.path.join(AKAR, 'AUTOTUNE', 'hasil')
KAJIAN = '13'
POLA = re.compile(r'^(20\d\d)-Q([1-4])$')


def label_suku(tarikh=None):
    t = tarikh or datetime.datetime.now(datetime.timezone.utc).date()
    return f'{t.year}-Q{(t.month - 1) // 3 + 1}'


def sah_label(s):
    if not POLA.match(s or ''): raise ValueError(f'label suku tidak sah: {s!r} (format YYYY-Qn)')
    return s


def dir_suku(label, hasil=HASIL):
    return os.path.join(hasil, 'suku', sah_label(label))


def dir_tala(label, hasil=HASIL):
    return os.path.join(dir_suku(label, hasil), 'tala')


def _tala_laluan():
    p = os.path.join(AKAR, 'AUTOTUNE', 'tala')
    if p not in sys.path: sys.path.insert(0, p)


def main(argv=None):
    a = argparse.ArgumentParser()
    s = a.add_subparsers(dest='cmd', required=True)
    p = s.add_parser('label'); p.add_argument('--suku', default=''); p.add_argument('--github-output', action='store_true')
    p = s.add_parser('rancang'); p.add_argument('--percubaan', type=int, default=120)
    p.add_argument('--shard', type=int, default=20); p.add_argument('--keluar', default='plan.json')
    p.add_argument('--ukur', action='store_true'); p.add_argument('--github-output', action='store_true')
    p = s.add_parser('pekerja'); p.add_argument('--suku', required=True); p.add_argument('--shard', type=int, required=True)
    p.add_argument('--plan', default='plan.json'); p.add_argument('--proses', type=int, default=4)
    p.add_argument('--had-minit', type=float, default=330)
    x = a.parse_args(argv)
    if x.cmd == 'label':
        lab = sah_label(x.suku.strip()) if x.suku.strip() else label_suku()
        print(lab)
        if x.github_output and os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'], 'a') as f: f.write(f'suku={lab}\n')
    elif x.cmd == 'rancang':
        _tala_laluan(); import rancang
        args = ['--kaedah', 'semua', '--kajian', KAJIAN, '--percubaan', str(x.percubaan), '--shard', str(x.shard),
                '--keluar', x.keluar]
        if x.ukur: args.append('--ukur')
        if x.github_output: args.append('--github-output')
        rancang.main(args)
    else:
        _tala_laluan(); import pekerja
        d = dir_tala(x.suku); os.makedirs(d, exist_ok=True)
        pekerja.main(['--shard', str(x.shard), '--plan', x.plan, '--proses', str(x.proses),
                      '--had-minit', str(x.had_minit), '--keluar', d])


if __name__ == '__main__':
    main()
