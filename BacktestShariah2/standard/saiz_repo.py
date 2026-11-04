#!/usr/bin/env python3
"""saiz_repo.py — ke mana pertumbuhan git sebenarnya pergi, dan tripwire supaya ia tidak hanyut.

Guna:
  python3 BacktestShariah2/standard/saiz_repo.py                 -> laporan JSON (kod keluar 0)
  python3 BacktestShariah2/standard/saiz_repo.py --hari 14       -> tingkap lain (lalai 14)
  python3 BacktestShariah2/standard/saiz_repo.py --had-mb-hari 12 -> kod keluar 1 jika melebihi
  python3 BacktestShariah2/standard/saiz_repo.py --teks          -> jadual untuk manusia

MENGAPA FAIL INI WUJUD (4 Nov 2026). Pengguna bimbang repo akan "crash atau lembap". Audit
pertama saya menganggar puncanya `lejar/terbuka.csv` kerana ia ditulis semula penuh setiap
malam. Apabila akhirnya DIUKUR, terbuka.csv ialah **1.9%** daripada pertumbuhan; data SEC
ialah 33% dan dua artifak kajian hampir menyamai keseluruhan lejar. Anggaran itu salah pada
hampir setiap paksi, dan tiada apa-apa dalam repo yang boleh menyangkalnya.

Jadi nilai fail ini bukan nombornya — ia menjadikan soalan "apa yang membesarkan repo?"
BOLEH DIJAWAB tanpa meneka. Jalankan ia sebelum mencadangkan apa-apa pembaikan saiz.

CARA IA MENGUKUR, dan HADNYA. Ia menjumlahkan `objectsize:disk` (saiz SELEPAS mampatan dan
delta) bagi setiap blob unik yang diperkenalkan dalam tingkap, dikumpul ikut laluan. Dua had
yang mesti difahami sebelum mempercayai nombornya:

  1. Ia mengukur pek TEMPATAN. `git repack -ad --window=250` menurunkan jumlah ~35% (diukur
     4 Nov: 8.68 -> 5.64 MB/hari) kerana objek baharu belum dipek-delta dengan baik. GitHub
     pek sendiri mengikut jadualnya, jadi angka di sini ialah had ATAS, bukan saiz di GitHub.
  2. Repack TEMPATAN tidak mengubah ID objek, jadi tiada apa-apa untuk ditolak — ia TIDAK
     mengecilkan repo di GitHub. Jangan cadangkan repack sebagai pembetulan saiz jauh.

Saiz sebenar di GitHub: `gh api repos/<owner>/<repo> --jq .size` (KB).
"""
import argparse
import collections
import json
import os
import subprocess
import sys

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _git(*a, **kw):
    return subprocess.run(['git', '-C', AKAR, *a], capture_output=True, text=True, **kw)


def cetek():
    """True jika klon cetek — nombor tingkap tidak boleh dipercayai di sana."""
    return _git('rev-parse', '--is-shallow-repository').stdout.strip() == 'true'


KOSONG = '0' * 40   # oid "tiada" bagi fail yang baru ditambah


def blob_tingkap(hari):
    """{(oid, laluan)} bagi setiap blob yang muncul dalam commit `hari` terakhir.

    `git log --raw` dan BUKAN `git diff-tree <banyak rev>`: diff-tree dengan beberapa rev
    membandingkan pokok-pokok itu ANTARA SATU SAMA LAIN, bukan setiap commit dengan induknya,
    jadi ia memulangkan hampir tiada apa-apa. Versi pertama fail ini membuat kesilapan itu dan
    melaporkan 0.00 MB/hari pada repo yang sedang tumbuh — kegagalan senyap yang kelihatan
    seperti berita baik, iaitu jenis yang paling berbahaya bagi tripwire.

    `-m` membuka commit gabungan terhadap setiap induk supaya data yang masuk melalui
    gabungan tidak terlepas kira.
    """
    r = _git('log', f'--since={hari} days ago', '-m', '--raw', '--no-abbrev',
             '--no-renames', '--format=', 'HEAD')
    pasangan = set()
    for ln in r.stdout.splitlines():
        # baris mentah: :<mod_lama> <mod_baru> <oid_lama> <oid_baru> <status>\t<laluan>
        if not ln.startswith(':') or '\t' not in ln:
            continue
        kepala, _, laluan = ln.partition('\t')
        b = kepala.split()
        if len(b) < 5 or not laluan or laluan.startswith('.'):
            continue
        oid = b[3]
        if oid != KOSONG:          # langkau padaman
            pasangan.add((oid, laluan))
    return pasangan


def saiz_cakera(oids):
    """{oid: bait pada cakera} — saiz SELEPAS delta dan zlib."""
    if not oids:
        return {}
    p = subprocess.run(['git', '-C', AKAR, 'cat-file', '--batch-check=%(objectname) %(objectsize:disk)'],
                       input='\n'.join(oids), capture_output=True, text=True)
    out = {}
    for ln in p.stdout.splitlines():
        b = ln.split()
        if len(b) == 2 and b[1].isdigit():
            out[b[0]] = int(b[1])
    return out


def kumpul(hari):
    pasangan = blob_tingkap(hari)
    sz = saiz_cakera({o for o, _ in pasangan})
    bait = collections.Counter()
    versi = collections.Counter()
    for o, laluan in pasangan:
        if o in sz:
            bait[laluan] += sz[o]
            versi[laluan] += 1
    return bait, versi


def folder(laluan, dalam=2):
    b = laluan.split('/')
    return '/'.join(b[:dalam]) if len(b) > dalam else laluan


def laporan(hari, atas):
    bait, versi = kumpul(hari)
    jum = sum(bait.values())
    fail = [dict(laluan=p, mb=round(v / 1e6, 3), peratus=round(100 * v / jum, 2) if jum else 0,
                 versi=versi[p], mb_setiap_versi=round(v / 1e6 / versi[p], 4))
            for p, v in bait.most_common(atas)]
    fol = collections.Counter()
    for p, v in bait.items():
        fol[folder(p)] += v
    return dict(
        hari=hari, cetek=cetek(), jumlah_mb=round(jum / 1e6, 2),
        mb_sehari=round(jum / 1e6 / hari, 3) if hari else 0,
        nota='saiz pek TEMPATAN; GitHub pek sendiri jadi ini had ATAS',
        fail=fail,
        folder=[dict(laluan=p, mb=round(v / 1e6, 2), peratus=round(100 * v / jum, 1) if jum else 0)
                for p, v in fol.most_common(10)])


def teks(d):
    b = [f"Pertumbuhan git {d['hari']} hari: {d['jumlah_mb']:,.1f} MB = {d['mb_sehari']:.2f} MB/hari",
         f"({d['nota']})", '']
    if d['cetek']:
        b.append('AMARAN: klon CETEK — tingkap tidak lengkap, nombor ini tidak boleh dipercayai.')
        b.append('')
    b.append(f"{'laluan':<54}{'MB':>8}{'%':>7}{'versi':>7}{'MB/versi':>10}")
    for f in d['fail']:
        b.append(f"  {f['laluan'][:52]:<52}{f['mb']:>8.1f}{f['peratus']:>6.1f}%"
                 f"{f['versi']:>7}{f['mb_setiap_versi']:>10.3f}")
    b += ['', 'ikut folder:']
    for f in d['folder']:
        b.append(f"  {f['laluan'][:52]:<52}{f['mb']:>8.1f}{f['peratus']:>6.1f}%")
    return '\n'.join(b)


def main(argv=None):
    global AKAR
    ap = argparse.ArgumentParser(description='Pertumbuhan git ikut laluan, dan tripwire kadar')
    ap.add_argument('--hari', type=int, default=14)
    ap.add_argument('--atas', type=int, default=20, help='bilangan laluan teratas dilaporkan')
    ap.add_argument('--had-mb-hari', type=float, default=None, dest='had',
                    help='kod keluar 1 jika MB/hari melebihi nilai ini')
    ap.add_argument('--teks', action='store_true', help='jadual untuk manusia, bukan JSON')
    # `--akar` wujud supaya skrip ini BOLEH DIUJI. Tanpa ia, AKAR dikira daripada __file__ dan
    # subproses sentiasa mengukur repo sebenar, apa pun cwd - jadi ujian yang menetapkan AKAR
    # dalam proses tidak menjejaskan subproses langsung. Dua ujian saya membuat kesilapan itu:
    # ia lulus pada klon penuh dan GAGAL dalam CI, yang mengklon cetek, kerana tripwire memang
    # dilangkau pada klon cetek dengan sengaja. Ujian itu menguji persekitaran, bukan kod.
    ap.add_argument('--akar', default=None, help='repo yang diukur (lalai: repo skrip ini)')
    a = ap.parse_args(argv)
    if a.akar:
        AKAR = os.path.abspath(a.akar)
    if a.hari < 1:
        raise SystemExit('--hari mesti >= 1')
    d = laporan(a.hari, a.atas)
    print(teks(d) if a.teks else json.dumps(d, ensure_ascii=False, indent=1))
    if a.had is not None and not d['cetek'] and d['mb_sehari'] > a.had:
        print(f"\nMELEBIHI: {d['mb_sehari']:.2f} MB/hari > had {a.had} MB/hari. "
              f"Laluan teratas: {d['fail'][0]['laluan'] if d['fail'] else '-'}", file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
