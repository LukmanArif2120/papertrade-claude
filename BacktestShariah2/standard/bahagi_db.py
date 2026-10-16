# bahagi_db.py — bahagi dokumen db dashboard yang besar (papertrade/watchlist, papertrade/senarai_beli) kepada
# beberapa dokumen di bawah had saiz db (262,144 bait JSON padat). Halaman menggabungkan semula baris:
#   <nama>      : semua medan meta + bahagian = {id, n} + rows bahagian 1
#   <nama>_2 …  : {induk: id, bahagian: k, rows}
# Halaman hanya menggabungkan bahagian 2..n yang `induk`-nya sama dengan `bahagian.id` dokumen asas, jadi bahagian
# lama daripada larian terdahulu diabaikan dan tidak perlu dipadam. Dokumen tanpa `bahagian` dibaca seperti biasa.
# Guna:
#   python3 BacktestShariah2/standard/bahagi_db.py --json <dokumen penuh.json> --nama watchlist --keluar <folder>
#   -> <folder>/watchlist.json, <folder>/watchlist_2.json, … ; senarai fail dicetak (JSON).
#   Tolak SEMUA fail yang dicetak dalam SATU batch ArtifactData (collection papertrade; if_version bagi dokumen
#   yang sudah wujud, tiada if_version bagi dokumen baharu).
import argparse, hashlib, json, os, sys

HAD_DB = 262144


def padat(x):
    return json.dumps(x, ensure_ascii=False, separators=(',', ':'))


def bait(x):
    return len(padat(x).encode('utf-8'))


def bahagi(doc, nama, had):
    """doc: dokumen penuh {meta…, rows:[…]}. Pulangkan [(doc_id, dokumen), …] setiap satu <= had bait."""
    if 'rows' not in doc and isinstance(doc.get('data'), dict):
        doc = doc['data']
    rows = doc.get('rows')
    if not isinstance(rows, list):
        raise SystemExit('dokumen tiada senarai "rows"')
    meta = {k: v for k, v in doc.items() if k not in ('rows', 'bahagian', 'induk')}
    ident = hashlib.sha1(padat(doc).encode('utf-8')).hexdigest()[:12]
    saiz = [bait(r) + 1 for r in rows]  # +1 = koma pemisah
    if any(s > had - 200 for s in saiz):
        raise SystemExit('satu baris melebihi had dokumen')
    kosong_asas = bait(dict(meta, bahagian={'id': ident, 'n': 999}, rows=[]))
    kosong_bhg = bait({'induk': ident, 'bahagian': 999, 'rows': []})
    kump, kini, guna = [[]], kosong_asas, kosong_asas
    for r, s in zip(rows, saiz):
        if kump[-1] and guna + s > had:
            kump.append([])
            guna = kosong_bhg
        kump[-1].append(r)
        guna += s
    n = len(kump)
    out = [(nama, dict(meta, bahagian={'id': ident, 'n': n}, rows=kump[0]))]
    for k in range(2, n + 1):
        out.append((f'{nama}_{k}', {'induk': ident, 'bahagian': k, 'rows': kump[k - 1]}))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description='Bahagi dokumen db besar kepada beberapa dokumen di bawah had saiz')
    ap.add_argument('--json', required=True, help='dokumen penuh (JSON) seperti yang akan ditulis ke db')
    ap.add_argument('--nama', required=True, help='doc_id asas, cth. watchlist atau senarai_beli')
    ap.add_argument('--keluar', required=True, help='folder fail JSON hasil')
    ap.add_argument('--had', type=int, default=200000, help='saiz maksimum setiap dokumen (bait JSON padat)')
    a = ap.parse_args(argv)
    if not 1000 < a.had < HAD_DB:
        raise SystemExit('perlu 1000 < --had < 262144')
    doc = json.load(open(a.json, encoding='utf-8'))
    hasil = bahagi(doc, a.nama, a.had)
    os.makedirs(a.keluar, exist_ok=True)
    fail = []
    for doc_id, d in hasil:
        p = os.path.join(a.keluar, doc_id + '.json')
        open(p, 'w', encoding='utf-8').write(padat(d))
        fail.append(dict(doc=doc_id, fail=p, baris=len(d['rows']), bait=bait(d)))
    print(json.dumps(dict(id=hasil[0][1]['bahagian']['id'], n=len(hasil), fail=fail), ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
