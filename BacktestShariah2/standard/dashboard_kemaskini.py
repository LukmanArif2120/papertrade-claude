# dashboard_kemaskini.py — tukar registry/<ID>.csv kepada dokumen JSON untuk pangkalan data dashboard
# "Papan Backtest Shariah". Guna:  python3 dashboard_kemaskini.py registry_M112.csv  ->  M112.json
# Kemudian: ArtifactData action "set", collection "registry", doc_id "<ID>", file_path "<ID>.json"
# (sertakan if_version jika dokumen sudah wujud — baca dahulu dengan action "get").
# Papertrade: python3 dashboard_kemaskini.py --papertrade log.csv TARIKH_HARGA LAJUR_HARGA -> _papertrade.json
#   lalu ArtifactData "set" collection "papertrade", doc_id "log".
#   Lajur pilihan dalam log.csv (sejak 8 Okt 2026): harga_keluar, untung_jika_pegang_pct, beza_peraturan_pct
#   -> medan harga_keluar, untung_pegang_pct, beza_peraturan_pct (null jika kosong / kedudukan masih terbuka).
import csv, json, os, sys

NUM = {'skor','cagr','mdd','mar','h1','h2','thn_kalah_spy','n','dagangan_setahun','win','avg','avgwin','avgloss',
       'pf','days','hit10','ret10','terburuk','ew_cagr','bulan_untung','bulan10','days_median','spy_cagr','qqq_cagr',
       'ew_mdd','skor_tanpa_gate'}
BOOL = {'ada_henti','menang_ew','menang_qqq','gate_lulus_kecuali_G1'}
DROP = {'enjin'}

def baris(path):
    rows = list(csv.reader(open(path, encoding='utf-8')))
    hdr = rows[0]; nc = len(hdr); ci = hdr.index('catatan'); out = []
    for r in rows[1:]:
        if not r: continue
        if len(r) > nc:  # koma tanpa petikan dalam catatan: cantum semula
            ex = len(r) - nc; r = r[:ci] + [','.join(r[ci:ci + ex + 1])] + r[ci + ex + 1:]
        if len(r) != nc: raise SystemExit(f'{path}: baris rosak ({len(r)} lajur)')
        d = {}
        for k, v in zip(hdr, r):
            if k in DROP: continue
            if k in NUM: d[k] = float(v) if v not in ('', 'nan') else None
            elif k in BOOL: d[k] = v == 'True'
            elif k in ('pegang', 'skor_pecahan'):
                o = {}
                for p in v.split('|'):
                    if ':' in p:
                        a, b = p.split(':', 1)
                        try: o[a] = float(b)
                        except ValueError: pass
                d[k] = o
            else: d[k] = v
        out.append(d)
    return out

def dokumen(path):
    rec = baris(path); mid = rec[0]['id']
    return mid, {'id': mid, 'jenis': mid[0], 'kaedah': rec[0]['kaedah'], 'tarikh': rec[0]['tarikh'], 'rows': rec}

def _f(v):
    try: return float(v)
    except (TypeError, ValueError): return None

def papertrade(path, tarikh, lajur):
    rows = []
    for r in csv.DictReader(open(path, encoding='utf-8')):
        rows.append({'tarikh_masuk': r['tarikh_masuk'], 'teknik': r['teknik'], 'saham': r['saham'], 'unit': float(r['unit']),
                     'harga_isian': float(r['harga_isian']), 'henti': _f(r['henti']),
                     'harga_terkini': float(r[lajur]), 'untung_pct': float(r['untung_pct']), 'status': r['status'],
                     'harga_keluar': _f(r.get('harga_keluar')),
                     'untung_pegang_pct': _f(r.get('untung_jika_pegang_pct')),
                     'beza_peraturan_pct': _f(r.get('beza_peraturan_pct'))})
    return {'rows': rows, 'harga_pada': tarikh, 'sumber': 'uji_kertas/log.csv'}

if __name__ == '__main__':
    if sys.argv[1] == '--papertrade':
        json.dump(papertrade(sys.argv[2], sys.argv[3], sys.argv[4]), open('_papertrade.json', 'w'), ensure_ascii=False)
        print('_papertrade.json')
    else:
        for f in sys.argv[1:]:
            mid, doc = dokumen(f)
            json.dump(doc, open(f'{mid}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
            print(f'{mid}.json', len(doc['rows']), 'baris')
