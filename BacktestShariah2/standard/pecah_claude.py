# pecah_claude.py — pastikan setiap dokumen db papertrade/claude_N kekal di bawah had saiz (256 KiB = 262,144 bait).
# Dokumen membesar kira-kira 120–130 bait setiap kali posisi keluar (medan keluar diisi), jadi saiz diunjur
# seolah-olah semua posisi terbuka sudah keluar, dan fail dipecah awal.
# Anggaran = JSON padat baris CSV (medan kosong digugurkan, nilai bertaip) + meta dokumen; tepat ±0.1% (16 Okt 2026).
# Guna:
#   python3 BacktestShariah2/standard/pecah_claude.py          -> lapor; kod keluar 1 jika ada unjuran > --had
#   python3 BacktestShariah2/standard/pecah_claude.py --pecah  -> baris hujung fail yang unjurannya > --had dipindah
#        ke fail baharu claude_<N terbesar + 1>.csv sehingga unjuran fail asal <= --sasaran
# Selepas --pecah: tolak SEMUA fail dalam "berubah" ke dokumen db yang sama nama (papertrade/claude_N),
# dalam satu batch ArtifactData (if_version bagi dokumen sedia ada). Halaman dashboard membaca claude_N tanpa had.
import argparse, csv, glob, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PT = os.path.join(os.path.dirname(HERE), 'papertrade')
HAD_DB = 262144          # had keras dokumen db
TUMBUH = 140             # bait tambahan bagi setiap posisi terbuka apabila keluar (diukur 113–128; dibundar ke atas)
TUMBUH_LORONG = 150      # bait tambahan apabila lorong 2 (henti) atau 3 (10%) keluar (keluar_tiga.py; anggaran 125–146)
META = {'claude': 12000}  # meta dokumen (slot, batal, nota_slot) dalam papertrade/claude
META_LAIN = 1000


def nombor_fail(path):
    m = re.fullmatch(r'claude(?:_(\d+))?\.csv', os.path.basename(path))
    return (int(m.group(1)) if m.group(1) else 1) if m else None


def nama_fail(n):
    return 'claude.csv' if n == 1 else f'claude_{n}.csv'


def nilai(v):
    if v in ('True', 'False'):
        return v == 'True'
    try:
        f = float(v)
    except ValueError:
        return v
    return int(f) if f.is_integer() and '.' not in v and 'e' not in v.lower() else f


def saiz_baris(hdr, r):
    d = {k: nilai(v) for k, v in zip(hdr, r) if v != ''}
    return len(json.dumps(d, ensure_ascii=False, separators=(',', ':')).encode('utf-8')) + 1


def terbuka(hdr, r):
    d = dict(zip(hdr, r))
    return str(d.get('keluar', '')).strip().lower() not in ('true', '1') and \
        str(d.get('tidak_dibeli', '')).strip().lower() not in ('true', '1')


def tumbuh(hdr, r):
    """Bait yang akan ditambah pada baris ini apabila semua lorong keluar yang masih terbuka keluar."""
    d = dict(zip(hdr, r))
    if str(d.get('tidak_dibeli', '')).strip().lower() in ('true', '1'):
        return 0
    n = TUMBUH if terbuka(hdr, r) else 0
    if 'tutup_semua' in d:
        n += sum(TUMBUH_LORONG for c in ('keluar_henti', 'keluar_10') if str(d.get(c, '')).strip().lower() != 'true')
    return n


def baca(path):
    rows = list(csv.reader(open(path, encoding='utf-8', newline='')))
    return rows[0], [r for r in rows[1:] if r]


def tulis(path, hdr, rows):
    b = io.StringIO(newline='')
    w = csv.writer(b)
    w.writerow(hdr)
    w.writerows(rows)
    open(path, 'w', encoding='utf-8', newline='').write(b.getvalue())


def ukur(n, hdr, rows):
    meta = META.get('claude' if n == 1 else '', META_LAIN)
    kini = meta + 13 + sum(saiz_baris(hdr, r) for r in rows)
    buka = sum(terbuka(hdr, r) for r in rows)
    return dict(baris=len(rows), terbuka=buka, anggaran=kini, unjuran=kini + sum(tumbuh(hdr, r) for r in rows))


def main(argv=None):
    ap = argparse.ArgumentParser(description='Semak/pecah fail claude*.csv supaya dokumen db kekal di bawah had')
    ap.add_argument('--folder', default=PT)
    ap.add_argument('--had', type=int, default=240000, help='unjuran maksimum (bait) sebelum fail dipecah')
    ap.add_argument('--sasaran', type=int, default=190000, help='unjuran fail asal selepas dipecah (bait)')
    ap.add_argument('--pecah', action='store_true', help='pindah baris hujung ke fail baharu')
    a = ap.parse_args(argv)
    if not a.sasaran < a.had < HAD_DB:
        raise SystemExit('perlu --sasaran < --had < 262144')
    fail = {nombor_fail(p): p for p in glob.glob(os.path.join(a.folder, 'claude*.csv')) if nombor_fail(p)}
    if not fail:
        print('tiada fail claude*.csv', file=sys.stderr)
        return 2
    berubah, dipecah = [], []
    n = 1
    while n <= max(fail):
        if n not in fail:
            n += 1
            continue
        hdr, rows = baca(fail[n])
        u = ukur(n, hdr, rows)
        if a.pecah and u['unjuran'] > a.had and len(rows) > 1:
            k = len(rows)
            unj = u['unjuran'] - sum(saiz_baris(hdr, r) + tumbuh(hdr, r) for r in rows)
            awal = [unj]
            for r in rows:
                awal.append(awal[-1] + saiz_baris(hdr, r) + tumbuh(hdr, r))
            while k > 1 and awal[k] > a.sasaran:
                k -= 1
            baru = max(fail) + 1
            p_baru = os.path.join(a.folder, nama_fail(baru))
            tulis(fail[n], hdr, rows[:k])
            tulis(p_baru, hdr, rows[k:])
            fail[baru] = p_baru
            berubah += [os.path.basename(fail[n]), os.path.basename(p_baru)]
            dipecah.append(dict(dari=os.path.basename(fail[n]), ke=os.path.basename(p_baru),
                                kekal=k, dipindah=len(rows) - k))
            continue  # ukur semula fail ini; fail baharu diperiksa apabila n sampai kepadanya
        n += 1
    lapor, lebih = {}, []
    for m in sorted(fail):
        hdr, rows = baca(fail[m])
        u = ukur(m, hdr, rows)
        lapor[os.path.basename(fail[m])] = u
        if u['unjuran'] > a.had:
            lebih.append(os.path.basename(fail[m]))
    print(json.dumps(dict(had=a.had, sasaran=a.sasaran, fail=lapor, dipecah=dipecah,
                          berubah=sorted(set(berubah), key=lambda s: nombor_fail(s)), melebihi=lebih),
                     ensure_ascii=False, indent=1))
    return 1 if lebih else 0


if __name__ == '__main__':
    sys.exit(main())
