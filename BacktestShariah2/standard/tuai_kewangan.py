# tuai_kewangan.py — kumpul hasil alat Moomoo (quote_financials_statements, quote_financials_earnings_price_history,
# quote_market_snapshot) daripada transkrip sesi Claude Code (JSONL, termasuk sub-ejen) ke folder mentah
# `gred_kewangan.py simpan`, tanpa menaip semula hasil alat.
#
#   python3 BacktestShariah2/standard/tuai_kewangan.py --transkrip ~/.claude/projects/<projek> --keluar <folder mentah>
#   python3 BacktestShariah2/standard/tuai_kewangan.py perlu [--had 40] [--tarikh YYYY-MM-DD]
#       -> senarai "T:abcd" ("T:abcde" bagi pelapor separuh tahun: e = jenis 1 financial_type 11)
#          saham yang perlu dikumpul (imbasan malam, jadual/imbas_2002.md langkah 5c): saham tanpa fail
#          data/kewangan dahulu (senarai_beli, watchlist, posisi terbuka, kemudian posisi lain), kemudian saham aktif yang
#          suku seterusnya sepatutnya sudah dilapor (akhir suku terakhir + 91 + 45 hari < hari ini) dan fail dikumpul > 7 hari lalu.
#
# Pasangan tool_use -> tool_result dipadan ikut id; parameter panggilan (symbol, statement_type, financial_type, next_key)
# menentukan nama fail. Hasil besar yang disimpan alat ke fail ("Output has been saved to <path>" atau
# "<persisted-output> … Full output saved to: <path>") dibaca daripada fail itu.
# financial_type 10 (suku + tahunan) dipecah ikut financial_type setiap laporan: 7 -> <T>_<jenis>_7_<halaman>.json,
# 1–4 -> <T>_<jenis>_9_<halaman>.json. financial_type 11 (kumulatif) / 5 (Q6 = separuh tahun pertama, H1; sejak
# 23 Okt 2026 untuk pelapor separuh tahun) dipecah: 5 -> <T>_<jenis>_6_c<halaman>.json, 7 -> _7_c<halaman> (Q1/Q9
# kumulatif diabaikan). Snapshot berkelompok dipecah -> <T>_snap.json. Hasil gagal (ret_code lain,
# cth. -11 had kadar; ralat alat) tidak ditulis. ret_code -10 ("no data") = jawapan muktamad: status 'tiada', tiada fail.
# Hasil berulang: yang terkini menang.
# Status: <keluar>/tuai_status.json {T: {"1"|"2"|"3": {"halaman": [...], "has_more": bool, "next_key": str} atau "tiada",
#   "eph": true|"tiada", "snap": true, "separuh": {"1"|"3": {"halaman": [...], "h1": n, ...} atau "tiada"}}}.
import argparse, csv, glob, json, os, re, sys
from datetime import date, timedelta

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
            elif t and a == 'quote_financials_statements' and str(inp.get('financial_type') or '10') in ('5', '11'):
                status.setdefault(t, {}).setdefault('separuh', {}).setdefault(str(inp.get('statement_type') or '1'), 'tiada')
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
        if st not in ('1', '2', '3') or ft not in ('5', '7', '9', '10', '11'):
            continue
        rl = (obj.get('data') or {}).get('report_list') or []
        hl = halaman(inp)
        if ft == '10':
            kump = {'9': [r for r in rl if r.get('financial_type') in (1, 2, 3, 4)],
                    '7': [r for r in rl if r.get('financial_type') == 7]}
        elif ft in ('5', '11'):   # kumulatif: Q6 (H1) dan tahunan sahaja
            kump = {'6': [r for r in rl if r.get('financial_type') == 5],
                    '7': [r for r in rl if r.get('financial_type') == 7]}
        else:
            kump = {ft: rl}
        for tp, laporan in kump.items():
            if laporan:   # kumulatif: awalan 'c' supaya tidak menimpa fail financial_type 10 halaman sama
                nama = f'{t}_{st}_{tp}_{"c" if ft in ("5", "11") else ""}{hl}.json'
                tulis(os.path.join(keluar, nama), {'ret_code': 0, 'data': {'report_list': laporan}})
        pg = obj.get('pagination') or {}
        s = status.setdefault(t, {})
        if ft in ('5', '11'):   # status separuh tahun berasingan: tidak mengubah status suku
            e = s.setdefault('separuh', {}).setdefault(st, {'halaman': []})
            if hl not in e['halaman']:
                e['halaman'].append(hl)
            e['has_more'] = bool(pg.get('has_more')); e['next_key'] = pg.get('next_key')
            e['h1'] = e.get('h1', 0) + len(kump['6'])
            continue
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


BS2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUKU_LAPOR = 91 + 45      # akhir suku terakhir + satu suku + tempoh lapor (hari)
SEGAR = 7                 # jangan ulang kumpul fail yang dikumpul <= 7 hari lalu


def perlu(folder, kewangan, hari_ini, had):
    """[(T, sebab)] saham yang perlu dikumpul: tiada fail dahulu (ikut keutamaan), kemudian suku baharu dijangka."""
    def tk(p, buka_sahaja=False):
        if not os.path.exists(p):
            return []
        out = []
        for r in csv.DictReader(open(p, newline='', encoding='utf-8')):
            t = (r.get('saham') or r.get('Saham') or '').strip()
            if t and (not buka_sahaja or str(r.get('keluar', '')).strip().lower() not in ('true', '1')):
                out.append(t)
        return out
    posisi = sorted(glob.glob(os.path.join(folder, 'claude*.csv')))
    aktif = tk(os.path.join(folder, 'senarai_beli.csv')) + tk(os.path.join(folder, 'watchlist.csv')) + \
        [t for p in posisi for t in tk(p, True)]
    semua = aktif + [t for p in posisi for t in tk(p)]
    urutan = list(dict.fromkeys(semua))
    out = [(t, 'tiada fail') for t in urutan if not os.path.exists(os.path.join(kewangan, f'{t}.json'))]
    for t in dict.fromkeys(aktif):
        p = os.path.join(kewangan, f'{t}.json')
        if not os.path.exists(p):
            continue
        k = json.load(open(p, encoding='utf-8'))
        suku = k.get('suku') or []
        dk = k.get('dikumpul') or '2000-01-01'
        if suku and date.fromisoformat(suku[-1]['tamat']) + timedelta(days=SUKU_LAPOR) < hari_ini \
                and date.fromisoformat(dk) + timedelta(days=SEGAR) < hari_ini:
            out.append((t, f'suku selepas {suku[-1]["label"]} dijangka sudah dilapor'))
    return out[:had]


def separuh_tahun(kewangan, t):
    """Pelapor separuh tahun (v7.1): fail menyimpan 'separuh', atau 4 suku terakhir tanpa penyata pendapatan (Moomoo
    hanya kunci kira-kira pada label Q2/Q4). Panggilan e = statement_type 1, financial_type 11, limit 50."""
    p = os.path.join(kewangan, f'{t}.json')
    if not os.path.exists(p):
        return False
    k = json.load(open(p, encoding='utf-8'))
    suku = (k.get('suku') or [])[-4:]
    return bool(k.get('separuh')) or (len(suku) >= 2 and all(not e.get('pendapatan') for e in suku))


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ['perlu']:
        ap = argparse.ArgumentParser(description='Saham yang perlu dikumpul data kewangannya')
        ap.add_argument('--folder', default=os.path.join(BS2, 'papertrade'))
        ap.add_argument('--kewangan', default=os.path.join(BS2, 'data', 'kewangan'))
        ap.add_argument('--tarikh', default=date.today().isoformat()); ap.add_argument('--had', type=int, default=40)
        a = ap.parse_args(argv[1:])
        senarai = perlu(a.folder, a.kewangan, date.fromisoformat(a.tarikh), a.had)
        for t, sebab in senarai:
            print(f'{t}:{"abcde" if separuh_tahun(a.kewangan, t) else "abcd"}  # {sebab}')
        print(f'{len(senarai)} saham', file=sys.stderr)
        return
    ap = argparse.ArgumentParser(description='Tuai hasil alat Moomoo daripada transkrip sesi ke folder mentah gred_kewangan')
    ap.add_argument('--transkrip', nargs='+', default=[os.path.expanduser('~/.claude/projects')],
                    help='fail .jsonl atau folder (dicari secara rekursif); lalai ~/.claude/projects')
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
