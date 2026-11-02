"""Daftarkan larian 94 dalam sumber kebenaran `REVERSE/strategi.py`.

CLAUDE.md: *"Jangan baca CLAUDE.md untuk mengetahui apa yang belum diuji — ia hanyut, dan
hanyutan itulah yang menyebabkan eksperimen dicadangkan semula. Sumber kebenaran ialah
`python3 REVERSE/strategi.py`."*

Jadi empat larian kohort 94 (portfolio A, portfolio B, CARA, AL02) mesti muncul di sana,
atau ia akan hanyut keluar daripada sumber kebenaran dan dicadangkan semula kelak — tepat
kitaran yang nota itu memperingatkan.

`strategi.py` memerlukan lajur gate boolean setiap fail. CSV portfolio menyimpan
`cagr`/`mdd` tetapi gate dikira dalam laporan, bukan disimpan. Skrip ini menambah lajur
`T1` (= P1 DAN P2 = CAGR > SPUS DAN MDD >= SPUS) kepada setiap CSV portfolio supaya gate
boleh dibaca semula tanpa mengira ulang di tempat lain, kemudian menambah empat entri
`EKSPERIMEN`.

Guna: python3 REVERSE/step37_daftar_94.py
"""
import csv
import io
import sys
from pathlib import Path

AKAR = Path(__file__).resolve().parents[1]
RV = AKAR / 'REVERSE'
SPUS_CAGR, SPUS_MDD = 17.95, -26.82

FAIL = ['portfolio_94.csv', 'portfolio_94b.csv', 'portfolio_94_al02.csv']

ENTRI = """    # Kohort 94 kombinasi produksi — pradaftar SPEC_PORTFOLIO_94.md dan 94B.md. Didaftar
    # di sini supaya ia tidak hanyut keluar daripada sumber kebenaran dan dicadangkan semula.
    dict(id='P94A', nama='Portfolio 94 kombinasi (50 larian; 3 lengan cacat)',
         fail='portfolio_94.csv', gate='T1', pf=True),
    dict(id='P94B', nama='Portfolio 94 - kecacatan dibetulkan + jalur benih (201 larian)',
         fail='portfolio_94b.csv', gate='T1', pf=True),
    dict(id='P94AL', nama='Portfolio 94 pada alam AL02 (SPUS) - syarat 94B §8',
         fail='portfolio_94_al02.csv', gate='T1', pf=True),
    dict(id='CARA94', nama='Paksi CARA pada 45 masuk produksi (6 cara)',
         fail='cara_94.csv', gate='CARA1'),
"""


def tambah_t1():
    n = 0
    for nama in FAIL:
        p = RV / nama
        if not p.exists():
            print(f'  {nama}: TIADA — dilangkau')
            continue
        R = list(csv.DictReader(open(p, encoding='utf-8')))
        if not R:
            print(f'  {nama}: kosong — dilangkau')
            continue
        for r in R:
            try:
                c, m = float(r['cagr']), float(r['mdd'])
                r['T1'] = str(c > SPUS_CAGR and m >= SPUS_MDD)
            except (KeyError, TypeError, ValueError):
                r['T1'] = 'False'
        kol = [k for k in R[0] if k != 'T1'] + ['T1']
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=kol)
        w.writeheader()
        w.writerows(R)
        p.write_text(buf.getvalue(), encoding='utf-8')
        lulus = sum(1 for r in R if r['T1'] == 'True')
        print(f'  {nama}: {len(R)} baris, T1 lulus {lulus}')
        n += 1
    return n


def daftar():
    p = RV / 'strategi.py'
    s = p.read_text(encoding='utf-8')
    if "id='P94A'" in s:
        print('  strategi.py: sudah didaftar')
        return False
    jangkar = "    dict(id='E1', nama='PEGANG x SLOT (320 konfigurasi)',"
    if jangkar not in s:
        raise SystemExit('jangkar E1 tidak dijumpai dalam strategi.py')
    s = s.replace(jangkar, ENTRI + jangkar, 1)
    p.write_text(s, encoding='utf-8')
    print('  strategi.py: 4 entri ditambah sebelum E1')
    return True


def main():
    print('1/2 tambah lajur T1 kepada CSV portfolio...')
    tambah_t1()
    print('2/2 daftar dalam strategi.py...')
    daftar()
    print('\nsemakan hanyut:')
    sys.path.insert(0, str(AKAR))
    import REVERSE.strategi as ST
    import importlib
    importlib.reload(ST)
    return ST.main(['--semak'])


if __name__ == '__main__':
    raise SystemExit(main())
