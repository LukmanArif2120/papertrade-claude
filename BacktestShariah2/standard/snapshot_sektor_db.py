# Bina dokumen db dashboard `sektor/snapshot` daripada kekuatan SELURUH pasaran AS (sektor_pasaran.py),
# dengan medan SST (aliran institusi, volum relatif, RS, institusi_beli/jual, volum_luar_biasa) disalin daripada
# snapshot lama jika nama kumpulan sama, dan pendedahan posisi aktif sah (Paper Trade M, Papertrade C).
#
# Guna: python3 snapshot_sektor_db.py --pasaran sektor_pasaran.json --lama snapshot_lama.json \
#           --peta papertrade/peta_industri.csv --papertrade papertrade --dibina "YYYY-MM-DD HH:MM MYT" --out baru.json
import os, sys, csv, glob, json, argparse
from statistics import mean

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sektor_pasaran import SEKTOR_INDUSTRI  # noqa: E402

SST_MEDAN = ['rs', 'sst', 'volum_relatif', 'aliran_institusi', 'aliran_beli', 'aliran_jual', 'volum_luar_biasa']


def benar(v):
    return str(v or '').strip().lower() in ('true', '1')


def posisi_aktif(folder):
    out = []
    for f in [os.path.join(folder, 'moomoo.csv')] + sorted(glob.glob(os.path.join(folder, 'claude*.csv'))):
        ak = 'm' if f.endswith('moomoo.csv') else 'c'
        for r in csv.DictReader(open(f, newline='', encoding='utf-8')):
            if benar(r.get('keluar')) or benar(r.get('tidak_sah')) or benar(r.get('tidak_dibeli')):
                continue
            try:
                u = float(r['untung_pct'])
            except (TypeError, ValueError, KeyError):
                continue
            out.append((ak, r['saham'], u))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--pasaran', required=True)
    ap.add_argument('--lama', help='dokumen sektor/snapshot semasa (JSON) untuk medan SST')
    ap.add_argument('--peta', required=True)
    ap.add_argument('--papertrade', required=True)
    ap.add_argument('--dibina', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args(argv)
    P = json.load(open(a.pasaran, encoding='utf-8'))
    L = {}
    if a.lama and os.path.exists(a.lama):
        L = json.load(open(a.lama, encoding='utf-8'))
        L = L.get('data', L)
    lama = {(r.get('jenis'), r.get('nama')): r for r in L.get('rows', [])}
    peta = {r['ticker']: r['industri'] for r in csv.DictReader(open(a.peta, newline='', encoding='utf-8'))}
    pos = posisi_aktif(a.papertrade)
    kum = {}
    for ak, t, u in pos:
        i = peta.get(t)
        if not i:
            continue
        for key in [('Industri', i), ('Sektor', SEKTOR_INDUSTRI.get(i))]:
            kum.setdefault(key, {'m': [], 'c': []})[ak].append(u)
    rows = []
    for r in P['rows']:
        o = {k: r.get(k) for k in ['jenis', 'nama', 'sektor', 'n', 'prestasi_1w', 'prestasi_1m', 'prestasi_3m', 'breadth',
                                    'rel_1m', 'rel_3m', 'fasa', 'skor_panas']}
        o['n_harga'] = o['n']
        o['mcap'] = (r.get('mcap_bilion') or 0) * 1e9
        o['sampel_kecil'] = (o['n'] or 0) < 5
        o['prestasi_1d'] = None
        o['teratas'] = r.get('teratas_senarai') or []
        x = lama.get((o['jenis'], o['nama'])) or {}
        for k in SST_MEDAN:
            o[k] = x.get(k)
        k = kum.get((o['jenis'], o['nama']), {'m': [], 'c': []})
        o['posisi_m'], o['posisi_c'] = len(k['m']), len(k['c'])
        o['untung_m'] = round(mean(k['m']), 2) if k['m'] else None
        o['untung_c'] = round(mean(k['c']), 2) if k['c'] else None
        al = k['m'] + k['c']
        o['untung_purata_posisi'] = round(mean(al), 2) if al else None
        rows.append(o)
    pas = dict(L.get('pasaran') or {})
    pp = P['pasaran']
    pas.update(n_saham=pp['n'], n_harga=pp['n'], breadth_1m=pp['breadth'], median_1w=round(pp['r1w'], 2),
               median_1m=round(pp['r1m'], 2), median_3m=round(pp['r3m'], 2))
    doc = {k: L[k] for k in ['institusi_beli', 'institusi_jual', 'volum_luar_biasa', 'definisi_fasa'] if k in L}
    doc.update(rows=rows, pasaran=pas, alam='US penuh', dibina=a.dibina, tarikh_harga=P['tarikh'].replace('-', ''),
               harga_kini='tutup ' + P['tarikh'],
               sumber='Seluruh pasaran AS (screener Moomoo, harga >= USD5) + industri Moomoo (peta_industri.csv); '
                      'sektor = 11 sektor Morningstar. Aliran institusi, RS dan volum relatif daripada SST Terminal jika ada.',
               pemberat={'prestasi_1m': 0.30, 'prestasi_3m': 0.25, 'prestasi_1w': 0.15, 'breadth': 0.30})
    json.dump(doc, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(f"{len(rows)} baris · {sum(1 for r in rows if r['posisi_m'] or r['posisi_c'])} kumpulan berposisi · "
          f"{os.path.getsize(a.out) // 1024} KB")


if __name__ == '__main__':
    main()
