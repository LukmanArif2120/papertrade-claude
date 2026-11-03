#!/usr/bin/env python3
"""audit_mn.py — audit pembezaan M lawan N pada setiap peringkat saluran papertrade.

Setiap baris menjawab satu soalan: adakah peringkat ini melayan Nxx sama seperti Mxx? Jawapan
datang daripada fail KELUARAN sebenar, bukan daripada membaca kod - itulah sebabnya ia menangkap
perkara yang pembacaan kod terlepas. Audit 3 Nov 2026 memakai skrip ini untuk mengesahkan 835
posisi Nxx dilangkau oleh kemas kini malam.

Berbeza daripada pengawal.py: pengawal menjawab "adakah ia berjalan hari ini" dan membetulkan
yang boleh; ini menjawab "adakah kedua-dua keluarga dilayan sama" dan tidak menulis apa-apa.

Guna:
    python3 BacktestShariah2/standard/audit_mn.py <folder papertrade> [folder lejar]

Tanda XX bukan semestinya kegagalan - lihat kolum nota. Kohort baharu yang belum matang
memberi 0 pada peringkat keluar, dan watchlist Nxx memang 0 kerana modul Nxx tidak melaporkan
calon "hampir" (hampir() = None).
"""
import collections
import csv
import glob
import gzip
import json
import os
import sys

PT = sys.argv[1]
LEJAR = sys.argv[2] if len(sys.argv) > 2 else None


def fam(m):
    m = str(m or '')
    return 'N' if m.startswith('N') else 'GB' if m.startswith('GB') else 'M' if m.startswith('M') else '?'


def baris(p):
    with open(p, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def kira(rows, kol, syarat=None):
    c = collections.Counter()
    for r in rows:
        if syarat and not syarat(r):
            continue
        c[fam(r.get(kol))] += 1
    return dict(c)


def lapor(nama, m, n, nota=''):
    ok = 'OK ' if (n > 0) == (m > 0) or n > 0 else 'XX '
    print(f'{ok} {nama:34} M {m:>6}   N {n:>6}   {nota}')


print('=' * 92)
print(f'PAPERTRADE: {PT}')
print('=' * 92)

# 1. posisi dibeli
pos = []
for p in sorted(glob.glob(os.path.join(PT, 'claude*.csv'))):
    pos += baris(p)
dibeli = [r for r in pos if r.get('tarikh_beli') and r.get('harga_beli')
          and r.get('tidak_dibeli') not in ('1', 'ya', 'True', 'benar')]
c = kira(dibeli, 'kaedah')
lapor('1 posisi dibeli', c.get('M', 0), c.get('N', 0))

# 2. harga terkini dikemas kini
c = kira(dibeli, 'kaedah', lambda r: bool(r.get('harga_terkini')))
lapor('2 harga_terkini diisi', c.get('M', 0), c.get('N', 0))

# 3. lorong 1 keluar / menunggu
c = kira(dibeli, 'kaedah', lambda r: r.get('keluar') in ('1', 'ya', 'True', 'benar'))
lapor('3a lorong 1 KELUAR', c.get('M', 0), c.get('N', 0))
c = kira(dibeli, 'kaedah', lambda r: 'menunggu' in (r.get('isyarat_keluar') or ''))
lapor('3b lorong 1 menunggu jual', c.get('M', 0), c.get('N', 0))
c = kira(dibeli, 'kaedah', lambda r: bool((r.get('isyarat_keluar') or '').strip()))
lapor('3c isyarat_keluar ada teks', c.get('M', 0), c.get('N', 0))

# 4. lorong 2 (Chandelier) — lajur bermula 'l2_' atau mengandungi 'henti'
l2 = [k for k in (dibeli[0] if dibeli else {}) if k.startswith('lorong2') or k.endswith('_henti')]
if l2:
    k0 = l2[0]
    c = kira(dibeli, 'kaedah', lambda r: bool(r.get(k0)))
    lapor(f'4 lorong 2 ({k0}) diisi', c.get('M', 0), c.get('N', 0))

# 5. gred
for g in ('gred_keseluruhan', 'rs_rating', 'gred_sektor'):
    if dibeli and g in dibeli[0]:
        c = kira(dibeli, 'kaedah', lambda r, g=g: bool(r.get(g)))
        lapor(f'5 gred diisi: {g}', c.get('M', 0), c.get('N', 0))

# 6. senarai_beli + watchlist
sb = baris(os.path.join(PT, 'senarai_beli.csv'))
c = kira(sb, 'kaedah')
lapor('6a senarai_beli', c.get('M', 0), c.get('N', 0))
wl = baris(os.path.join(PT, 'watchlist.csv'))
kol = next((k for k in (wl[0] if wl else {}) if 'kaedah' in k.lower()), None)
if kol:
    c = kira(wl, kol)
    lapor('6b watchlist', c.get('M', 0), c.get('N', 0), '(N sengaja 0: hampir() = None)')

# 7. isyarat direkod
isy = sorted(glob.glob(os.path.join(os.path.dirname(PT.rstrip('/')), 'isyarat', '*.csv.gz'))) or \
      sorted(glob.glob(os.path.join(PT, '..', 'isyarat', '*.csv.gz')))
if isy:
    with gzip.open(isy[-1], 'rt', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    k = next((x for x in (rows[0] if rows else {}) if 'kaedah' in x.lower()), 'kaedah')
    c = kira(rows, k)
    lapor(f'7 isyarat {os.path.basename(isy[-1])}', c.get('M', 0), c.get('N', 0))

# 8. Lejar Penuh
if LEJAR and os.path.isdir(LEJAR):
    print('-' * 92)
    print(f'LEJAR PENUH: {LEJAR}')
    for nama, f in (('8a terbuka.csv', 'terbuka.csv'), ('8b tunggu.csv', 'tunggu.csv')):
        p = os.path.join(LEJAR, f)
        if os.path.exists(p):
            c = kira(baris(p), 'id_kaedah')
            lapor(nama, c.get('M', 0), c.get('N', 0))
    g = sorted(glob.glob(os.path.join(LEJAR, 'isyarat', '*.csv.gz')))
    if g:
        with gzip.open(g[-1], 'rt', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        c = kira(rows, 'kaedah')
        lapor(f'8c isyarat {os.path.basename(g[-1])}', c.get('M', 0), c.get('N', 0))
    g = sorted(glob.glob(os.path.join(LEJAR, 'tutup', '*.csv*')))
    if g:
        rows = []
        for p in g[-2:]:
            op = gzip.open if p.endswith('.gz') else open
            with op(p, 'rt', encoding='utf-8') as f:
                rows += list(csv.DictReader(f))
        c = kira(rows, 'id_kaedah')
        lapor('8d tutup (2 fail terakhir)', c.get('M', 0), c.get('N', 0))
    p = os.path.join(LEJAR, 'status.json')
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            st = json.load(f)
        print(f'    status: sesi_terakhir={st.get("sesi_terakhir")} ralat={len(st.get("ralat") or [])}')
