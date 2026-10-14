# Semakan data papertrade sebelum commit (peraturan dalam papertrade/SKEMA.md)
# Guna:  python3 BacktestShariah2/standard/sahkan.py            -> semak sahaja
#        python3 BacktestShariah2/standard/sahkan.py --betulkan -> susun lajur ikut skema, kemudian semak
# Kod keluar: 0 = lulus, 1 = ada RALAT (jangan push data), 2 = fail tiada / tidak boleh dibaca.
import sys, os, csv, glob, re, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
PT = os.path.join(os.path.dirname(HERE), 'papertrade')

# Susunan lajur rasmi fail posisi (moomoo.csv, claude.csv, claude_N.csv)
POSISI = ['tarikh_beli', 'saham', 'kaedah', 'id_kaedah', 'sektor', 'industri', 'harga_beli', 'unit',
          'harga_terkini', 'untung_pct', 'hari', 'henti', 'sasaran', 'isyarat_keluar', 'keluar',
          'tarikh_keluar', 'harga_keluar', 'untung_akhir_pct', 'sumber', 'kaedah_kongsi', 'tarikh_isyarat',
          'nota', 'dikesan', 'tidak_sah', 'sebab_tidak_sah', 'tidak_dibeli', 'luar_peraturan',
          'harga_buka_rujukan', 'tarikh_beli_dirancang',
          # gred pada hari isyarat (standard/gred.py; tugasan_v3 §8)
          'gred_sektor', 'skor_sektor', 'gred_industri', 'skor_industri', 'rs_rating', 'gred_rs',
          'gred_pemangkin', 'mata_pemangkin', 'pemangkin', 'tarikh_earnings', 'hari_ke_earnings',
          'sumber_earnings', 'gred_qr', 'gred_keseluruhan', 'gred_pada']
LAJUR_GRED = ['gred_sektor', 'gred_industri', 'gred_rs', 'gred_pemangkin', 'gred_qr', 'gred_keseluruhan']
NILAI_GRED = {'', 'A', 'B', 'C', 'D', 'E', '–'}
WAJIB_POSISI = ['tarikh_beli', 'saham', 'kaedah', 'sektor', 'industri', 'harga_beli', 'unit',
                'harga_terkini', 'untung_pct', 'hari', 'isyarat_keluar', 'keluar', 'tarikh_keluar',
                'harga_keluar', 'untung_akhir_pct']
WAJIB_SENARAI = ['saham', 'kaedah', 'sektor', 'industri', 'pct_dipenuhi', 'harga_rujukan', 'henti',
                 'sasaran', 'tarikh_isyarat', 'tarikh_imbasan']
WAJIB_WATCH = ['Saham', 'Kaedah', 'Sektor', 'Industri', '% hampir']

TARIKH = re.compile(r'^\d{4}-\d{2}-\d{2}$')
BENAR = {'true', '1', 'ya'}
TOL = 0.02  # toleransi peratus (pembundaran 2 titik perpuluhan)


def benar(v):
    return str(v or '').strip().lower() in BENAR


def nombor(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def kosong(v):
    return str(v if v is not None else '').strip() in ('', '-', 'nan', 'None')


def baca(p):
    with open(p, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        return list(r.fieldnames or []), list(r)


def tulis(p, lajur, rows):
    with open(p, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=lajur, extrasaction='raise')
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in lajur})


def susun(lajur):
    """Lajur rasmi dahulu (ikut POSISI), lajur tambahan dikekalkan di hujung."""
    return POSISI + [c for c in lajur if c not in POSISI]


def fail_posisi():
    c = sorted(glob.glob(os.path.join(PT, 'claude*.csv')),
               key=lambda p: int(re.search(r'claude_?(\d*)', os.path.basename(p)).group(1) or 1))
    return [os.path.join(PT, 'moomoo.csv')] + c


def semak_gred(nama, rows, ralat):
    for i, r in enumerate(rows, start=2):
        for c in LAJUR_GRED:
            if c in r and (r[c] or '') not in NILAI_GRED:
                ralat.append(f'{nama}:{i}: {c} tidak sah ({r[c]!r}); mesti A–E atau "–"')
        v = nombor(r.get('rs_rating'))
        if not kosong(r.get('rs_rating')) and (v is None or not 1 <= v <= 99):
            ralat.append(f'{nama}:{i}: rs_rating {r.get("rs_rating")!r} di luar 1–99')


def semak_posisi(nama, lajur, rows, ralat, amaran, kunci):
    for c in WAJIB_POSISI:
        if c not in lajur:
            ralat.append(f'{nama}: lajur wajib tiada: {c}')
    if any(c not in lajur for c in WAJIB_POSISI):
        return
    akaun = 'moomoo' if nama == 'moomoo.csv' else 'claude'
    for i, r in enumerate(rows, start=2):
        t = f'{nama}:{i} {r["saham"]} {r["kaedah"]}'
        tdb = benar(r.get('tidak_dibeli'))
        if kosong(r['sektor']) or kosong(r['industri']):
            ralat.append(f'{t}: sektor/industri kosong')
        if not TARIKH.match(r['tarikh_beli'] or '') and not tdb:
            ralat.append(f'{t}: tarikh_beli bukan YYYY-MM-DD ({r["tarikh_beli"]!r})')
        if tdb:
            # Baris TIDAK DIBELI: tiada harga beli, tidak dikemas kini, tidak dikira
            if not kosong(r['harga_beli']):
                ralat.append(f'{t}: tidak_dibeli tetapi harga_beli berisi')
            if r['isyarat_keluar'] != 'TIDAK DIBELI':
                ralat.append(f'{t}: tidak_dibeli tetapi isyarat_keluar bukan "TIDAK DIBELI"')
            if benar(r['keluar']):
                ralat.append(f'{t}: tidak_dibeli tetapi keluar=True')
            continue
        hb, ht, up = nombor(r['harga_beli']), nombor(r['harga_terkini']), nombor(r['untung_pct'])
        if hb is None or hb <= 0:
            ralat.append(f'{t}: harga_beli tidak sah ({r["harga_beli"]!r})')
            continue
        u = nombor(r['unit'])
        if u is None or u <= 0 or u != int(u):
            ralat.append(f'{t}: unit tidak sah ({r["unit"]!r})')
        elif akaun == 'claude' and u != 1:
            ralat.append(f'{t}: Papertrade C mesti 1 unit (dapat {r["unit"]})')
        if ht is not None and up is not None and abs((ht / hb - 1) * 100 - up) > TOL:
            ralat.append(f'{t}: untung_pct {up} != (harga_terkini/harga_beli-1)*100 = {(ht / hb - 1) * 100:.2f}')
        if benar(r['keluar']):
            hk, ua = nombor(r['harga_keluar']), nombor(r['untung_akhir_pct'])
            if not TARIKH.match(r['tarikh_keluar'] or '') or hk is None:
                ralat.append(f'{t}: keluar=True tetapi tarikh_keluar/harga_keluar kosong')
            else:
                if r['tarikh_keluar'] < r['tarikh_beli']:
                    ralat.append(f'{t}: tarikh_keluar {r["tarikh_keluar"]} sebelum tarikh_beli')
                if ua is None or abs((hk / hb - 1) * 100 - ua) > TOL:
                    ralat.append(f'{t}: untung_akhir_pct {ua} != (harga_keluar/harga_beli-1)*100 = {(hk / hb - 1) * 100:.2f}')
        elif not kosong(r['tarikh_keluar']) or not kosong(r['harga_keluar']):
            ralat.append(f'{t}: keluar=False tetapi tarikh_keluar/harga_keluar berisi')
        k = (akaun, r['kaedah'], r['saham'], r['tarikh_beli'])
        if k in kunci:
            ralat.append(f'{t}: bertindih dengan {kunci[k]} (kaedah+saham+tarikh_beli)')
        else:
            kunci[k] = f'{nama}:{i}'


def semak_senarai(p, ralat, amaran):
    nama = os.path.basename(p)
    lajur, rows = baca(p)
    for c in WAJIB_SENARAI:
        if c not in lajur:
            ralat.append(f'{nama}: lajur wajib tiada: {c}')
    for c in ['nota_henti', 'buka_maks']:
        if c not in lajur:
            amaran.append(f'{nama}: lajur {c} tiada (wajib sejak 14 Okt 2026; diisi oleh imbasan 8:02 malam)')
    lihat, lain = set(), 0
    for i, r in enumerate(rows, start=2):
        t = f'{nama}:{i} {r.get("saham")} {r.get("kaedah")}'
        if kosong(r.get('sektor')) or kosong(r.get('industri')):
            ralat.append(f'{t}: sektor/industri kosong')
        if nombor(r.get('pct_dipenuhi')) != 100:
            ralat.append(f'{t}: senarai beli hanya untuk isyarat 100% (dapat {r.get("pct_dipenuhi")})')
        if r.get('destinasi') not in (None, '', 'Claude'):
            lain += 1
        k = (r.get('saham'), r.get('kaedah'), r.get('tarikh_isyarat'))
        if k in lihat:
            ralat.append(f'{t}: baris bertindih (saham+kaedah+tarikh_isyarat)')
        lihat.add(k)
    if lain:
        amaran.append(f'{nama}: {lain} baris destinasi bukan Claude (mod Papertrade C sahaja; belian tetap ke Claude)')


def semak_watch(p, ralat, amaran):
    nama = os.path.basename(p)
    lajur, rows = baca(p)
    for c in WAJIB_WATCH:
        if c not in lajur:
            ralat.append(f'{nama}: lajur wajib tiada: {c}')
    if any(c not in lajur for c in WAJIB_WATCH):
        return
    lihat = set()
    for i, r in enumerate(rows, start=2):
        t = f'{nama}:{i} {r["Saham"]} {r["Kaedah"]}'
        if kosong(r['Sektor']) or kosong(r['Industri']):
            ralat.append(f'{t}: sektor/industri kosong')
        v = nombor(r['% hampir'])
        if v is None or not 90 <= v <= 100:
            ralat.append(f'{t}: % hampir {r["% hampir"]} di luar 90–100 (terkeluar signal mesti dibuang)')
        k = (r['Saham'], r['Kaedah'])
        if k in lihat:
            ralat.append(f'{t}: baris bertindih (saham+kaedah)')
        lihat.add(k)


def main(argv=None):
    global PT
    ap = argparse.ArgumentParser(description='Semak data papertrade ikut SKEMA.md')
    ap.add_argument('--betulkan', action='store_true', help='susun lajur fail posisi ikut skema sebelum semak')
    ap.add_argument('--folder', default=PT, help='folder papertrade (lalai: BacktestShariah2/papertrade)')
    a = ap.parse_args(argv)
    PT = a.folder
    ralat, amaran, kunci = [], [], {}
    for p in fail_posisi():
        if not os.path.exists(p):
            print(f'TIADA: {p}')
            return 2
        lajur, rows = baca(p)
        if a.betulkan:
            baru = susun(lajur)
            if baru != lajur:
                tulis(p, baru, rows)
                print(f'Disusun semula: {os.path.basename(p)} ({len(lajur)} -> {len(baru)} lajur)')
                lajur = baru
        semak_posisi(os.path.basename(p), lajur, rows, ralat, amaran, kunci)
        semak_gred(os.path.basename(p), rows, ralat)
    for nm, fn in [('senarai_beli.csv', semak_senarai), ('watchlist.csv', semak_watch)]:
        p = os.path.join(PT, nm)
        if os.path.exists(p):
            fn(p, ralat, amaran)
            semak_gred(nm, baca(p)[1], ralat)
    for x in amaran[:40]:
        print('AMARAN', x)
    if len(amaran) > 40:
        print(f'AMARAN ... dan {len(amaran) - 40} lagi')
    for x in ralat[:200]:
        print('RALAT', x)
    print(f'Ringkasan: {len(ralat)} ralat, {len(amaran)} amaran, {len(kunci)} posisi dibeli diperiksa.')
    return 1 if ralat else 0


if __name__ == '__main__':
    sys.exit(main())
