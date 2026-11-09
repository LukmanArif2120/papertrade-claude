"""Keadaan kajian REVERSE: apa sudah diuji, apa cabang semasa, apa langkah seterusnya.

Dibaca daripada CSV keputusan SEBENAR, bukan daripada ingatan atau `CLAUDE.md`. Rancangan
dan peraturan keputusan ada dalam `REVERSE/STRATEGI.md`; fail ini menguatkuasakannya.

Dua kerja:
  1. Cetak keadaan — eksperimen selesai dengan keputusannya, kedudukan dalam baris gilir,
     langkah seterusnya, dan sama ada syarat BERHENTI sudah tercapai.
  2. `--semak` — gagal (kod 1) jika `data/registry_N.csv` menandakan sesuatu BELUM diuji
     sedangkan fail keputusan sudah mengandunginya. Itu tepat pepijat yang menyebabkan
     `GB04` dan `GB08` disenaraikan sebagai "calon belum diuji" selepas kedua-duanya diuji
     dan gagal (31 Okt 2026).

Guna: python3 REVERSE/strategi.py [--semak]
"""
import argparse
import csv
import re
from pathlib import Path

AKAR = Path(__file__).resolve().parents[1]
RV = AKAR / 'REVERSE'
REG = AKAR / 'BacktestShariah2' / 'data' / 'registry_N.csv'

# SPUS, konvensyen CAGR-seluruh-tingkap (PENANDA_ARAS_SYARIAH.md; jangan campur dengan
# konvensyen median-setiap-tahun 26.09% / -10.14%).
SPUS_CAGR, SPUS_MDD, SPUS_NISBAH = 17.95, -26.82, 0.669
T3_CAGR, T3_MDD = 15.0, -15.0
# Keputusan pengguna 31 Okt 2026: MENANG = T1 ATAU T3. T2 dilapor sebagai diagnostik sahaja
# (BERHENTI-SEPARA) dan tidak menghentikan baris gilir.

# Lajur yang BOLEH mengandungi id paksi. Medan nota sengaja dikecualikan: nota menyebut id
# yang belum diuji secara sah, dan mengimbasnya akan memberi hanyutan palsu.
LAJUR_ID = {'masuk', 'keluar', 'cara', 'urutan', 'konfig', 'pegang', 'alam'}
TOKEN = re.compile(r'\b(?:GB|SZ|AL|PG|IB|KR|IS)\d{2}|\b[NXCU]\d{1,3}\b')

# Had pegangan (bar) -> baris registry PEGANG yang ia uji.
PEGANG_KE_ID = {'10': 'PG02', '21': 'PG03', '63': 'PG04'}

EKSPERIMEN = [
    dict(id='A', nama='Ruang MASUK (280 ujian)', fail='nxx.csv', gate='gate3'),
    dict(id='B', nama='Ruang KELUAR (69 ujian)', fail='nxx_keluar.csv', gate='gate3'),
    dict(id='GAB', nama='Paksi GABUNGAN (14 ujian)', fail='gabungan.csv', gate='gate3'),
    dict(id='SX', nama='Silang akhir (8 ujian)', fail='silang_akhir.csv', gate='gate3'),
    dict(id='PORT', nama='Portfolio lawan SPUS (36 konfigurasi)',
         fail='portfolio_n_ringkas.csv', gate='lulus', pf=True),
    dict(id='CARA', nama='Paksi CARA (6 ujian)', fail='cara.csv', gate='CARA1'),
    # Kohort 94 kombinasi produksi — pradaftar SPEC_PORTFOLIO_94.md + 94B.md, dijana
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
    dict(id='CARA94', nama='Paksi CARA pada 45 masuk produksi (6 cara, keluar X13 sahaja)',
         fail='cara_94.csv', gate='CARA1'),
    # Pradaftar SPEC_CARA_94.md: CARA_94 mengukur cara pada X13 SAHAJA (6/94 slot) dan
    # menyatakan bakinya ANGGAPAN. Entri ini ialah ukurannya: enam keluar, m = 30.
    dict(id='CARAK94', nama='Paksi CARA x enam keluar kohort (6 asas C01 + 30 ujian)',
         fail='cara_keluar_94.csv', gate='MENANG'),
    dict(id='E1', nama='PEGANG x SLOT (320 konfigurasi)',
         fail='pegang_slot_ringkas.csv', gate='lulus', pf=True, giliran=True),
    # `tapis`: alam_ringkas.csv membawa KEDUA-DUA alam (AL01 rujukan + AL02 ujian), jadi
    # tanpa tapisan kad E2 akan melaporkan baris AL01 sebagai keputusannya.
    dict(id='E2', nama='ALAM AL02 - alam dagangan sebenar',
         fail='alam_ringkas.csv', gate='lulus', pf=True, giliran=True,
         tapis=('alam', 'AL02')),
    dict(id='E3', nama='INSTRUMEN IS02 - putaran bakul sektor',
         fail='instrumen_ringkas.csv', gate='T1', pf=True, giliran=True),
    dict(id='E4', nama='KELUAR X31/X32 - keluar peringkat portfolio',
         fail='keluar_portfolio_ringkas.csv', gate='T1', pf=True, giliran=True),
    dict(id='E5', nama='KORELASI KR03 - had setiap industri',
         fail='korelasi_ringkas.csv', gate='T1', pf=True, giliran=True),
    dict(id='E6', nama='GABUNGAN GB07 - hierarki merentas paksi',
         fail='hierarki_ringkas.csv', gate='T1', pf=True, giliran=True),
    # Kajian TUNGGAL di luar baris gilir (kebenaran pengguna 9 Nov 2026; pradaftar SPEC_SATELIT.md):
    # satelit GB02_atau3 x X15 15% akaun atas teras indeks 35% + tunai, dalam toleransi MDD -10%.
    # Gate P1-P5 ialah gate AKAUN (lawan K1 indeks 50% dan satelit rawak), bukan T1/T3 SPUS penuh,
    # jadi T1/T2/T3 di bawah dijangka 0 secara struktur (teras 35%); baca `lulus`.
    dict(id='SAT', nama='SATELIT - GB02_atau3 x Chandelier 15% atas teras indeks 35% + tunai (14 sel)',
         fail='satelit_ringkas.csv', gate='lulus', pf=True,
         amaran='GAGAL P1/P2/P3/P5: CAGR tahan +6.12% lawan indeks 50% +7.59% dan satelit RAWAK +7.82%; '
                'MDD -13.7%. Satelit kekal 0%. Kebenaran kajian tunggal 9 Nov 2026 dianggap terbelanja.'),
]


def baca(p):
    return list(csv.DictReader(open(p, encoding='utf-8'))) if p.exists() else []


def _f(r, k):
    try:
        return float(r[k])
    except (KeyError, TypeError, ValueError):
        return None


def nilai_tingkat(R):
    """(T1, T2, T3, baris terbaik) bagi fail bergaya portfolio (ada cagr dan mdd)."""
    t1 = t2 = t3 = 0
    terbaik, skor = None, -9e9
    for r in R:
        c, m = _f(r, 'cagr'), _f(r, 'mdd')
        if c is None or m is None:
            continue
        nis = c / abs(m) if m else 0.0
        if c > SPUS_CAGR and m >= SPUS_MDD:
            t1 += 1
        if nis > SPUS_NISBAH and c > SPUS_CAGR:
            t2 += 1
        if c >= T3_CAGR and m >= T3_MDD:
            t3 += 1
        if c > skor:
            skor, terbaik = c, (r, c, m, nis)
    return t1, t2, t3, terbaik


def baris(e):
    """Baris yang eksperimen `e` MILIKI — satu laluan pemilihan, bukan dua.

    Dahulu `keadaan()` mengenakan `tapis` tetapi jumlah T1/T2/T3 dalam `main()` memanggil
    `baca()` terus tanpanya, jadi kad E2 melapor AL02 sementara jumlah global mengandungi
    baris AL01 yang tiada kad melaporkannya. Kedua-dua laluan kini melalui sini.
    """
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
    """Senarai (eksperimen, status, ringkasan) mengikut urutan baris gilir."""
    out = []
    for e in EKSPERIMEN:
        R = baris(e)
        if R is None:
            out.append((e, 'BELUM', 'belum dijalankan' if e['fail'] is None
                        else f'tiada {e["fail"]}'))
            continue
        n = len(R)
        lulus = sum(1 for r in R if str(r.get(e['gate'])) == 'True')
        if e.get('pf'):
            t1, t2, t3, tb = nilai_tingkat(R)
            s = (f'{n} konfigurasi · lulus semua gate {lulus} · '
                 f'T1 {t1} · T2 {t2} · T3 {t3}')
            if tb:
                r, c, m, nis = tb
                # `larian`/`lengan` WAJIB di sini: tanpa nama lengan, baris kawalan
                # (RAWAK/RAWAKALAM) boleh dicetak sebagai "terbaik" tanpa menyatakan ia
                # kawalan, bukan konfigurasi isyarat.
                nm = ' '.join(str(r.get(k, '')) for k in
                              ('alam', 'larian', 'lengan', 'masuk', 'slot', 'k', 'imbang',
                               'keluar', 'pegang', 'urutan') if r.get(k))
                s += f'\n        terbaik CAGR: {nm} -> {c:+.2f}% / MDD {m:.2f}% / nisbah {nis:.2f}'
        else:
            s = f'{n} baris · lulus gate akhir {lulus}'
        out.append((e, 'SELESAI', s))
    return out


def hanyut():
    """Id paksi yang muncul dalam fail keputusan tetapi registry kata belum diuji."""
    reg = {r['id']: r['status'] for r in baca(REG)}
    jumpa = {}
    for p in sorted(RV.glob('*.csv')):
        for r in baca(p):
            for k, v in r.items():
                if k not in LAJUR_ID or not v:
                    continue
                ids = set(TOKEN.findall(str(v)))
                if k == 'pegang' and str(v) in PEGANG_KE_ID:
                    ids.add(PEGANG_KE_ID[str(v)])
                for i in ids:
                    jumpa.setdefault(i, set()).add(p.name)
    bad = []
    for i, fail in sorted(jumpa.items()):
        st = reg.get(i)
        if st is not None and st != 'DIUJI':
            bad.append((i, st, sorted(fail)))
    return bad


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--semak', action='store_true',
                    help='kod keluar 1 jika registry hanyut daripada fail keputusan')
    a = ap.parse_args(argv)

    K = keadaan()
    bad = hanyut()

    if not a.semak:
        print('KEADAAN KAJIAN REVERSE — dijana daripada CSV keputusan sebenar')
        print(f'Penanda aras SPUS: CAGR {SPUS_CAGR:.2f}%  MDD {SPUS_MDD:.2f}%  '
              f'nisbah {SPUS_NISBAH:.3f}')
        print()
        for e, st, s in K:
            tanda = 'v' if st == 'SELESAI' else '.'
            print(f'  [{tanda}] {e["id"]:5s} {e["nama"]}')
            print(f'        {s}')
            if e.get('amaran'):
                print(f'        AMARAN: {e["amaran"]}')
        print()

    gil = [(e, st) for e, st, _ in K if e.get('giliran')]
    belum = [e for e, st in gil if st == 'BELUM']
    PF = [(e, nilai_tingkat(baris(e)))
          for e, st, _ in K if e.get('pf') and st == 'SELESAI']
    t1 = sum(v[0] for _, v in PF)
    t2 = sum(v[1] for _, v in PF)
    t3 = sum(v[2] for _, v in PF)

    if not a.semak:
        if t1 or t3:
            print(f'BERHENTI–MENANG: {t1} konfigurasi melepasi T1, {t3} melepasi T3 '
                  f'(T2 diagnostik: {t2}). '
                  'Bekukan konfigurasi dan jalankan ujian hadapan >= 126 sesi.')
        elif not belum:
            print('BERHENTI–TUTUP: baris gilir E1–E6 selesai dan tiada melepasi T1/T3. '
                  'Kajian signal/pembinaan ditutup; terima T4 (SPUS + tunai pada berat '
                  'pilihan pengguna) dan alih sumber kepada pelaksanaan.')
        else:
            print(f'LANGKAH SETERUSNYA: {belum[0]["id"]} — {belum[0]["nama"]}')
            print(f'  tinggal dalam baris gilir: '
                  f'{", ".join(e["id"] for e in belum)}  '
                  f'(selepas E6 tanpa T1/T3 -> BERHENTI–TUTUP)')
            if t2:
                pec = ', '.join(f'{e["id"]} {v[1]}' for e, v in PF if v[1])
                print(f'  BERHENTI–SEPARA: {t2} konfigurasi melepasi T2 (nisbah) sahaja '
                      f'[{pec}] — dilapor sebagai lorong risiko-rendah, baris gilir '
                      'diteruskan.')
                for e, v in PF:
                    if v[1] and e.get('amaran'):
                        print(f'    {e["id"]}: {e["amaran"]}')
        print()

    if bad:
        print('HANYUT registry lawan fail keputusan '
              '(registry kata belum diuji, hasil sudah ada):')
        for i, st, fail in bad:
            print(f'  {i}  registry="{st}"  muncul dalam {", ".join(fail)}')
        return 1
    if not a.semak:
        print('Registry selaras dengan fail keputusan: tiada hanyut.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
