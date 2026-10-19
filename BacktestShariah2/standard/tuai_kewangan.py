# tuai_kewangan.py — kumpul hasil alat Moomoo (quote_financials_statements, quote_financials_earnings_price_history,
# quote_market_snapshot) daripada transkrip sesi Claude Code (JSONL, termasuk sub-ejen) ke folder mentah
# `gred_kewangan.py simpan`, tanpa menaip semula hasil alat.
#
#   python3 BacktestShariah2/standard/tuai_kewangan.py --transkrip ~/.claude/projects/<projek> --keluar <folder mentah>
#
# Pasangan tool_use -> tool_result dipadan ikut id; parameter panggilan (symbol, statement_type, financial_type, next_key)
# menentukan nama fail. Hasil besar yang disimpan alat ke fail ("Output has been saved to <path>" atau
# "<persisted-output> … Full output saved to: <path>") dibaca daripada fail itu.
# financial_type 10 (suku + tahunan) dipecah ikut financial_type setiap laporan: 7 -> <T>_<jenis>_7_<halaman>.json,
# 1–4 -> <T>_<jenis>_9_<halaman>.json. Snapshot berkelompok dipecah -> <T>_snap.json. Hasil gagal (ret_code lain,
# cth. -11 had kadar; ralat alat) tidak ditulis. ret_code -10 ("no data") = jawapan muktamad: status 'tiada', tiada fail.
# Hasil berulang: yang terkini menang.
# Status: <keluar>/tuai_status.json {T: {"1"|"2"|"3": {"halaman": [...], "has_more": bool, "next_key": str} atau "tiada",
#   "eph": true|"tiada", "snap": true}}.
import argparse, glob, json, os, re

SIMPAN = re.compile(r'(?:Output has been saved to|Full output saved to:) (\S+?\.(?:txt|json))')
TIADA_DATA = -10   # ret_code Moomoo "no data"


def teks(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return ''.join(x.get('text', '') for x in c if isinstance(x, dict))
    return ''


def kandungan(t):
    """Teks tool_result -> objek JSON (inline atau daripada fail yang disimpan alat); {'tiada': True} bagi
    ret_code -10; None jika ralat."""
    m = SIMPAN.search(t[:2000]) if t.startswith(('Error: result (', '<persisted-output>')) else None
    if m:
        if not os.path.exists(m.group(1)):
            return None
        t = open(m.group(1), encoding='utf-8').read()
    try:
        d = json.loads(t)
    except ValueError:
        return None
    if isinstance(d, list) and d and isinstance(d[0], dict) and d[0].get('type') == 'text':
        d = json.loads(d[0]['text'])
    if not isinstance(d, dict):
        return None
    if d.get('ret_code') == TIADA_DATA:
        return {'tiada': True}
    return d if d.get('ret_code') in (None, 0) else None


def pasangan(paths):
    """[(masa, nama_alat, input, objek)] bagi alat Moomoo yang dikenali, ikut masa."""
    guna, hasil = {}, []
    for p in paths:
        for baris in open(p, encoding='utf-8'):
            try:
                d = json.loads(baris)
            except ValueError:
                continue
            c = (d.get('message') or {}).get('content')
            if not isinstance(c, list):
                continue
            for x in c:
                if not isinstance(x, dict):
                    continue
                if x.get('type') == 'tool_use':
                    n = x.get('name') or ''
                    for a in ('quote_financials_statements', 'quote_financials_earnings_price_history', 'quote_market_snapshot'):
                        if n.endswith('__' + a):
                            guna[x['id']] = (a, x.get('input') or {})
                elif x.get('type') == 'tool_result' and x.get('tool_use_id') in guna:
                    a, inp = guna[x['tool_use_id']]
                    obj = kandungan(teks(x.get('content')))
                    if obj is not None:
                        hasil.append((d.get('timestamp') or '', a, inp, obj))
    return sorted(hasil, key=lambda h: h[0])


def ticker(sym):
    return sym.split('.', 1)[1] if sym.startswith('US.') else sym


def halaman(inp):
    k = str(inp.get('next_key') or '')
    return 'p1' if k in ('', '-1') else 'k' + re.sub(r'\W', '', k.split('|')[0])


def tulis(path, obj):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))


def tuai(paths, keluar):
    os.makedirs(keluar, exist_ok=True)
    status = {}
    for _, a, inp, obj in pasangan(paths):
        if obj.get('tiada'):
            t = ticker(str(inp.get('symbol') or ''))
            if t and a == 'quote_financials_earnings_price_history':
                e = status.setdefault(t, {})
                e['eph'] = e.get('eph') or 'tiada'   # data sebenar yang diterima kekal diutamakan
            elif t and a == 'quote_financials_statements' and not halaman(inp).startswith('k'):
                e = status.setdefault(t, {})
                if str(inp.get('statement_type') or '1') not in e:
                    e[str(inp.get('statement_type') or '1')] = 'tiada'
            continue
        if a == 'quote_market_snapshot':
            data = obj.get('data', obj)
            data = data.get('snapshot_list') or data.get('list') or data.get('data') if isinstance(data, dict) else data
            for s in data or []:
                kod = s.get('code') or s.get('symbol') or ''
                if not kod:
                    continue
                t = ticker(kod)
                tulis(os.path.join(keluar, f'{t}_snap.json'), {'ret_code': 0, 'data': [s]})
                status.setdefault(t, {})['snap'] = True
            continue
        t = ticker(str(inp.get('symbol') or ''))
        if not t:
            continue
        if a == 'quote_financials_earnings_price_history':
            tulis(os.path.join(keluar, f'{t}_eph.json'), obj)
            status.setdefault(t, {})['eph'] = True
            continue
        st, ft = str(inp.get('statement_type') or '1'), str(inp.get('financial_type') or '10')
        if st not in ('1', '2', '3') or ft not in ('7', '9', '10'):
            continue
        rl = (obj.get('data') or {}).get('report_list') or []
        hl = halaman(inp)
        kump = {'9': [r for r in rl if r.get('financial_type') in (1, 2, 3, 4)],
                '7': [r for r in rl if r.get('financial_type') == 7]} if ft == '10' else {ft: rl}
        for tp, laporan in kump.items():
            if laporan:
                tulis(os.path.join(keluar, f'{t}_{st}_{tp}_{hl}.json'), {'ret_code': 0, 'data': {'report_list': laporan}})
        pg = obj.get('pagination') or {}
        s = status.setdefault(t, {})
        if not isinstance(s.get(st), dict):   # 'tiada' lama digantikan oleh data sebenar
            s[st] = {'halaman': []}
        e = s[st]
        if hl not in e['halaman']:
            e['halaman'].append(hl)
        if ft == '10':   # halaman terakhir yang diterima menentukan sambungan
            e['has_more'] = bool(pg.get('has_more')); e['next_key'] = pg.get('next_key')
            e['suku'] = e.get('suku', 0) + len(kump['9']); e['tahun'] = e.get('tahun', 0) + len(kump['7'])
    tulis(os.path.join(keluar, 'tuai_status.json'), status)
    return status


def main(argv=None):
    ap = argparse.ArgumentParser(description='Tuai hasil alat Moomoo daripada transkrip sesi ke folder mentah gred_kewangan')
    ap.add_argument('--transkrip', required=True, nargs='+', help='fail .jsonl atau folder (dicari secara rekursif)')
    ap.add_argument('--keluar', required=True)
    a = ap.parse_args(argv)
    paths = []
    for p in a.transkrip:
        paths += sorted(glob.glob(os.path.join(p, '**', '*.jsonl'), recursive=True)) if os.path.isdir(p) else [p]
    st = tuai(paths, a.keluar)
    lengkap = [t for t, e in st.items() if all(k in e for k in ('1', '2', '3', 'eph'))]
    print(f'{len(paths)} transkrip; {len(st)} saham; lengkap (3 penyata + eph) {len(lengkap)}; '
          f'snapshot {sum(1 for e in st.values() if e.get("snap"))}')


if __name__ == '__main__':
    main()
