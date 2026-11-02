"""Daftarkan larian kohort 94 dalam sumber kebenaran `REVERSE/strategi.py`.

CLAUDE.md: *"Jangan baca CLAUDE.md untuk mengetahui apa yang belum diuji — ia hanyut, dan
hanyutan itulah yang menyebabkan eksperimen dicadangkan semula. Sumber kebenaran ialah
`python3 REVERSE/strategi.py`."*

Jadi larian kohort 94 (portfolio A, portfolio B, AL02, CARA) mesti muncul di sana, atau ia
akan hanyut keluar daripada sumber kebenaran dan dicadangkan semula kelak — tepat kitaran
yang nota itu memperingatkan.

## PEMBETULAN kepada versi pertama skrip ini (dikomit 32728d4e, kaedahnya SALAH)

Versi pertama menambah lajur `T1` kepada `portfolio_94.csv`, `portfolio_94b.csv` dan
`portfolio_94_al02.csv`, kemudian mendaftarkan ketiga-tiga fail MENTAH itu sebagai
eksperimen `pf=True`. Itu salah secara JENIS, dan saya dapati sebabnya sebelum melaksanakan:

1. **Fail mentah ialah satu baris setiap BENIH, bukan setiap konfigurasi.** Setiap fail
   `*_ringkas.csv` yang E1–E6 daftarkan sudah meruntuhkan jalur benih (lajur `cagr` =
   median, `cagr_p5`/`cagr_p95` = jalur, `nb` = bilangan benih). `strategi.py`
   mengira "konfigurasi lulus" baris demi baris, jadi mendaftar fail mentah akan mengira
   **cabutan benih** sebagai konfigurasi.
2. Akibatnya boleh diukur, bukan teori: `portfolio_94_al02.csv` ada **121 baris** dengan
   `cagr > SPUS` DAN nisbah > 0.669. Fail mentah akan melaporkan "121 konfigurasi melepasi
   T2" sedangkan ia hanya **4 lengan** (dan lengan AL02 pula, yang laporan sendiri
   mengukur sebagai artifak alam: masuk RAWAK pada AL02 beri median +46.17%).

Jadi skrip ini menjana `REVERSE/portfolio_94_ringkas.csv` mengikut konvensyen E1–E6 —
satu baris setiap lengan, median + jalur + gate — kemudian mendaftar fail ITU.

## Satu pepijat dalam `strategi.py` dibetulkan serentak

`keadaan()` mengenakan `tapis` (cth E2 = `alam` AL02) tetapi jumlah T1/T2/T3 dalam `main()`
memanggil `baca()` terus **tanpa** tapis. Diukur: kad E2 melapor AL02 (T2 = 0) sementara
jumlah global diam-diam mengandungi 5 baris T2 daripada AL01 yang tiada kad melaporkannya.
Hari ini verdict tidak terjejas (T1 = T3 = 0 di mana-mana), tetapi fail ini wujud khusus
untuk menghalang hanyutan senyap seperti itu. Pemilihan baris dipindahkan ke satu fungsi
`baris()` yang KEDUA-DUA laluan guna.

Guna: python3 REVERSE/step37_daftar_94.py
"""
import csv
import sys
from pathlib import Path

import numpy as np

AKAR = Path(__file__).resolve().parents[1]
RV = AKAR / 'REVERSE'
SPUS_CAGR, SPUS_MDD, SPUS_NISBAH = 17.95, -26.82, 0.669
T3_CAGR, T3_MDD = 15.0, -15.0

# fail mentah -> (id larian, alam, cacat)
LARIAN = [
    ('portfolio_94.csv', 'A', 'AL01',
     'U02 pendua bit-identik U14; kawalan RAWAK uji SUSUNAN bukan isyarat; saiz PENUH '
     'berayun 2.7x dengan kepadatan isyarat'),
    ('portfolio_94b.csv', 'B', 'AL01', ''),
    # 'B8' = larian B diulang di bawah syarat SPEC_PORTFOLIO_94B.md §8 (alam AL02).
    ('portfolio_94_al02.csv', 'B8', 'AL02', ''),
]
# Nama lengan kawalan, mengikut keutamaan: RAWAKALAM = kawalan dipadankan (larian B/AL02),
# RAWAK = kawalan susunan sahaja (larian A, sebab itu ia dicatat `cacat`).
KAWALAN = ('RAWAKALAM', 'RAWAK')

KOL = ['larian', 'alam', 'lengan', 'slot', 'urutan', 'cagr', 'mdd', 'cagr_p5', 'cagr_p95',
       'mdd_p5', 'nisbah', 'dedah', 'n_dag', 'nb', 'ctl', 'ctl_p95',
       'P1', 'P2', 'P3', 'P4', 'T1', 'T3', 'lulus', 'cacat']


def ringkas():
    """Satu baris setiap lengan daripada fail mentah — konvensyen E1-E6."""
    out = []
    for fail, lid, alam, cacat in LARIAN:
        p = RV / fail
        if not p.exists():
            print(f'  {fail}: TIADA — dilangkau')
            continue
        R = list(csv.DictReader(open(p, encoding='utf-8')))
        G = {}
        for r in R:
            G.setdefault((r['lengan'], r['slot'], r['urut']), []).append(r)
        # p95 jalur kawalan bagi setiap saiz slot, untuk P3.
        ctl = {}
        for nama in KAWALAN:
            for (ln, sl, _), g in G.items():
                if ln == nama and sl not in ctl:
                    ctl[sl] = (nama, float(np.nanpercentile(
                        [float(x['cagr']) for x in g], 95)))
        for (ln, sl, ur), g in sorted(G.items()):
            v = lambda k: np.asarray([float(x[k]) for x in g])  # noqa: E731
            cg, md = float(np.nanmedian(v('cagr'))), float(np.nanmedian(v('mdd')))
            nis = float(np.nanmedian(v('nisbah')))
            cn, cp = ctl.get(sl, ('', float('nan')))
            p1, p2 = cg > SPUS_CAGR, md >= SPUS_MDD
            p3 = bool(np.isfinite(cp) and cg > cp and ln not in KAWALAN)
            p4 = nis > SPUS_NISBAH
            out.append(dict(
                larian=lid, alam=alam, lengan=ln, slot=sl, urutan=ur,
                cagr=f'{cg:.4f}', mdd=f'{md:.4f}',
                cagr_p5=f'{float(np.nanpercentile(v("cagr"), 5)):.4f}',
                cagr_p95=f'{float(np.nanpercentile(v("cagr"), 95)):.4f}',
                mdd_p5=f'{float(np.nanpercentile(v("mdd"), 5)):.4f}',
                nisbah=f'{nis:.4f}', dedah=f'{float(np.nanmedian(v("dedah"))):.4f}',
                n_dag=f'{float(np.nanmedian(v("n_dag"))):.0f}', nb=len(g),
                ctl=cn, ctl_p95='' if not np.isfinite(cp) else f'{cp:.4f}',
                P1=str(p1), P2=str(p2), P3=str(p3), P4=str(p4),
                T1=str(p1 and p2), T3=str(cg >= T3_CAGR and md >= T3_MDD),
                lulus=str(p1 and p2 and p3 and p4), cacat=cacat))
    q = RV / 'portfolio_94_ringkas.csv'
    with open(q, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=KOL)
        w.writeheader()
        w.writerows(out)
    for lid in ('A', 'B', 'B8'):
        S = [r for r in out if r['larian'] == lid]
        if S:
            print(f'  larian {lid:4s}: {len(S):2d} lengan · T1 '
                  f'{sum(1 for r in S if r["T1"] == "True")} · P3 '
                  f'{sum(1 for r in S if r["P3"] == "True")} · lulus '
                  f'{sum(1 for r in S if r["lulus"] == "True")}')
    print(f'  -> {q.name} ({len(out)} lengan)')
    return len(out)


# --- tampalan `strategi.py` ---------------------------------------------------------

ENTRI = """    # Kohort 94 kombinasi produksi — pradaftar SPEC_PORTFOLIO_94.md + 94B.md, dijana
    # oleh step37_daftar_94.py daripada fail mentah. BUKAN eksperimen ke-7: ia mengukur
    # kohort yang SUDAH dipilih untuk produksi, bukan mencari pembinaan baharu.
    dict(id='P94', nama='Portfolio kohort 94 kombinasi, alam AL01 (249 larian)',
         fail='portfolio_94_ringkas.csv', gate='T1', pf=True,
         tapis=('alam', 'AL01'),
         amaran='Larian A cacat (U02 pendua U14; kawalan RAWAK uji susunan bukan isyarat) '
                '- baca lajur `cacat`. P3 LULUS pada 8 slot dalam larian B: ujian isyarat '
                'pertama dalam repo dengan kawalan benar-benar dipadankan.'),
    dict(id='P94AL', nama='Portfolio kohort 94, alam AL02 (SPUS) - syarat 94B §8',
         fail='portfolio_94_ringkas.csv', gate='T1', pf=True,
         tapis=('alam', 'AL02'),
         amaran='SETIAP nombor pulangan di sini ARTIFAK ALAM: masuk RAWAK pada AL02 beri '
                'median +46.17% (AL01: +2.70%). Keahlian SPUS ialah petikan semasa ditolak '
                'ke belakang; E4 mengukur ia menyanjung MDD 30.9 mata. T2 yang lulus di '
                'sini BUKAN lorong risiko-rendah.'),
    dict(id='CARA94', nama='Paksi CARA pada 45 masuk produksi (6 cara)',
         fail='cara_94.csv', gate='CARA1'),
"""

TAMPAL = [
    # (nama, cari, ganti) — setiap satu mesti unik dalam fail.
    ('fungsi baris()',
     """def keadaan():
    \"\"\"Senarai (eksperimen, status, ringkasan) mengikut urutan baris gilir.\"\"\"
    out = []
    for e in EKSPERIMEN:
        if e['fail'] is None:
            out.append((e, 'BELUM', 'belum dijalankan'))
            continue
        p = RV / e['fail']
        if not p.exists():
            out.append((e, 'BELUM', f'tiada {e["fail"]}'))
            continue
        R = baca(p)
        if e['fail'] == 'cara.csv':
            R = [r for r in R if r.get('tingkap') == 'tahan']
        if e.get('tapis'):
            k_, v_ = e['tapis']
            R = [r for r in R if str(r.get(k_)) == v_]
        n = len(R)""",
     """def baris(e):
    \"\"\"Baris yang eksperimen `e` MILIKI — satu laluan pemilihan, bukan dua.

    Dahulu `keadaan()` mengenakan `tapis` tetapi jumlah T1/T2/T3 dalam `main()` memanggil
    `baca()` terus tanpanya, jadi kad E2 melapor AL02 sementara jumlah global mengandungi
    baris AL01 yang tiada kad melaporkannya. Kedua-dua laluan kini melalui sini.
    \"\"\"
    if e['fail'] is None:
        return None
    p = RV / e['fail']
    if not p.exists():
        return None
    R = baca(p)
    if e['fail'].startswith('cara'):
        R = [r for r in R if r.get('tingkap') == 'tahan']
    if e.get('tapis'):
        k_, v_ = e['tapis']
        R = [r for r in R if str(r.get(k_)) == v_]
    return R


def keadaan():
    \"\"\"Senarai (eksperimen, status, ringkasan) mengikut urutan baris gilir.\"\"\"
    out = []
    for e in EKSPERIMEN:
        R = baris(e)
        if R is None:
            out.append((e, 'BELUM', 'belum dijalankan' if e['fail'] is None
                        else f'tiada {e["fail"]}'))
            continue
        n = len(R)"""),
    ('amaran pada kad',
     """            print(f'  [{tanda}] {e["id"]:5s} {e["nama"]}')
            print(f'        {s}')""",
     """            print(f'  [{tanda}] {e["id"]:5s} {e["nama"]}')
            print(f'        {s}')
            if e.get('amaran'):
                print(f'        AMARAN: {e["amaran"]}')"""),
    ('jumlah guna baris()',
     """    t1 = sum(nilai_tingkat(baca(RV / e['fail']))[0]
             for e, st, _ in K if e.get('pf') and st == 'SELESAI')
    t2 = sum(nilai_tingkat(baca(RV / e['fail']))[1]
             for e, st, _ in K if e.get('pf') and st == 'SELESAI')
    t3 = sum(nilai_tingkat(baca(RV / e['fail']))[2]
             for e, st, _ in K if e.get('pf') and st == 'SELESAI')""",
     """    PF = [(e, nilai_tingkat(baris(e)))
          for e, st, _ in K if e.get('pf') and st == 'SELESAI']
    t1 = sum(v[0] for _, v in PF)
    t2 = sum(v[1] for _, v in PF)
    t3 = sum(v[2] for _, v in PF)"""),
    ('pecahan T2 ikut eksperimen',
     """            if t2:
                print(f'  BERHENTI–SEPARA: {t2} konfigurasi melepasi T2 (nisbah) sahaja — '
                      'dilapor sebagai lorong risiko-rendah, baris gilir diteruskan.')""",
     """            if t2:
                pec = ', '.join(f'{e["id"]} {v[1]}' for e, v in PF if v[1])
                print(f'  BERHENTI–SEPARA: {t2} konfigurasi melepasi T2 (nisbah) sahaja '
                      f'[{pec}] — dilapor sebagai lorong risiko-rendah, baris gilir '
                      'diteruskan.')
                for e, v in PF:
                    if v[1] and e.get('amaran'):
                        print(f'    {e["id"]}: {e["amaran"]}')"""),
]


def daftar():
    p = RV / 'strategi.py'
    s = p.read_text(encoding='utf-8')
    n = 0
    for nama, cari, ganti in TAMPAL:
        if ganti.strip() in s:
            print(f'  tampalan "{nama}": sudah dikenakan')
            continue
        if s.count(cari) != 1:
            raise SystemExit(f'tampalan "{nama}": {s.count(cari)} padanan, dijangka 1')
        s = s.replace(cari, ganti, 1)
        n += 1
        print(f'  tampalan "{nama}": dikenakan')
    if "id='P94'" not in s:
        jangkar = "    dict(id='E1', nama='PEGANG x SLOT (320 konfigurasi)',"
        if s.count(jangkar) != 1:
            raise SystemExit('jangkar E1 tidak unik dalam strategi.py')
        s = s.replace(jangkar, ENTRI + jangkar, 1)
        n += 1
        print('  3 entri (P94, P94AL, CARA94) ditambah sebelum E1')
    else:
        print('  entri 94: sudah didaftar')
    if n:
        p.write_text(s, encoding='utf-8')
    return n


def main():
    print('1/2 jana portfolio_94_ringkas.csv daripada fail mentah...')
    if not ringkas():
        raise SystemExit('tiada lengan dijana — fail mentah tiada?')
    print('2/2 daftar dalam strategi.py...')
    daftar()
    print('\nsemakan hanyut (strategi.py --semak):')
    sys.path.insert(0, str(AKAR))
    import importlib
    import REVERSE.strategi as ST
    importlib.reload(ST)
    return ST.main(['--semak'])


if __name__ == '__main__':
    raise SystemExit(main())
