import json, glob, csv, re, collections
import numpy as np

HARI_INI = '2026-10-12'
HARGA_PADA = '2026-10-12 ~13:30 NY (intraday, Moomoo)'
DIBINA = '2026-10-12 17:45 UTC (P2)'

def bdays(a, b):
    """hari dagangan dari a hingga b (a=hari 0)."""
    if not a or not b: return None
    return int(np.busday_count(a, b))

# ---------- sektor ----------
SEK = {k: tuple(v) for k, v in json.load(open('sektor_sedia.json')).items()}
for f in ['sektor_b0.csv', 'sektor_b1.csv', 'sektor_b2.csv']:
    for r in csv.DictReader(open(f)):
        SEK[r['saham'].strip()] = (r['sektor'].strip(), r['industri'].strip())
SEK['AXSM'] = ('Healthcare', SEK['AXSM'][1]); SEK['BMRN'] = ('Healthcare', SEK['BMRN'][1])
SEK['CHWY'] = ('Consumer', SEK['CHWY'][1])

# ---------- data ----------
peta = json.load(open('papertrade/moomoo_peta.json'))['rows']
log = json.load(open('papertrade/log.json'))['rows']
MM = {p['symbol']: p for p in json.load(open('moomoo_pos.json'))['data']['positions']}
SNAP = {s['code'][3:]: s for s in json.load(open('snap.json'))['data']['snapshot_list']}
OHLC = collections.defaultdict(list)
for o in sorted(csv.DictReader(open('ohlc_8_9.csv')), key=lambda o: o['tarikh']):
    OHLC[o['saham']].append({'tarikh': o['tarikh'], 'buka': float(o['buka']), 'rendah': float(o['rendah'])})
POS, PEN, SLOT, NAMA = {}, [], {}, {}
for f in sorted(glob.glob('larian/*/kumpulan/*.json')):
    for m, v in json.load(open(f))['kaedah'].items():
        NAMA[m] = v.get('nama')
        SLOT[m] = len(v['posisi'])
        for p in v['posisi']: POS.setdefault((m, p['saham']), p)
        for p in v['penuh']: PEN.append((m, p))

def r2(x, n=2):
    return None if x is None else round(float(x), n)

def keluar_dari_enjin(k, harga_beli, saham):
    """k = dict keluar daripada larian. pulangkan (tarikh, harga, teks) atau None."""
    if not k: return None
    if k.get('menunggu'):
        s = SNAP.get(saham)
        if s and s.get('open_price'):
            return (HARI_INI, float(s['open_price']), 'Keluar: isyarat keluar (jual pada buka 12 Okt)')
        return None
    sebab = k.get('sebab') or 'isyarat'
    teks = {'henti': 'Keluar: kena henti', 'sasaran': 'Keluar: capai sasaran',
            'isyarat keluar': 'Keluar: isyarat keluar kaedah'}.get(sebab, 'Keluar: ' + sebab)
    return (k['tarikh'], float(k['harga']), teks)

def baris(tarikh_beli, saham, kaedah, kongsi, harga_beli, unit, harga_kini, kel, id_kaedah, sumber, henti=None, sasaran=None, nota=''):
    sek, ind = SEK.get(saham, ('Lain-lain', 'Tidak diketahui'))
    r = dict(tarikh_beli=tarikh_beli, saham=saham, kaedah=kaedah, kaedah_kongsi=kongsi, sektor=sek, industri=ind,
             harga_beli=r2(harga_beli, 4), unit=unit, id_kaedah=id_kaedah, sumber=sumber,
             henti=r2(henti, 4), sasaran=r2(sasaran, 4), nota=nota)
    if kel:
        tk, hk, teks = kel
        u = (hk / harga_beli - 1) * 100
        r.update(harga_terkini=r2(hk, 4), untung_pct=r2(u), hari=bdays(tarikh_beli, tk), isyarat_keluar=teks,
                 keluar=True, tarikh_keluar=tk, harga_keluar=r2(hk, 4), untung_akhir_pct=r2(u))
    else:
        u = (harga_kini / harga_beli - 1) * 100 if harga_kini else None
        teks = 'Pegang'
        if henti: teks += f' (henti {henti:.2f}'+(f', sasaran {sasaran:.2f})' if sasaran else ')')
        elif sasaran: teks += f' (sasaran {sasaran:.2f})'
        r.update(harga_terkini=r2(harga_kini, 4), untung_pct=r2(u), hari=bdays(tarikh_beli, HARI_INI), isyarat_keluar=teks,
                 keluar=False, tarikh_keluar=None, harga_keluar=None, untung_akhir_pct=None)
    return r

# ---------- MOOMOO ----------
BULAN = {'Okt': '10', 'Sep': '09'}
def tarikh_status(st):
    m = re.search(r'(\d+) Okt', st or '')
    return f'2026-10-{int(m.group(1)):02d}' if m else None

moomoo = []
for p in peta:
    s = p['saham']; mm = MM[s]
    hb = float(mm['cost_price']); unit = int(float(mm['qty'])); kini = float(mm['cur_price'])
    raw = p['kaedah']
    ids = re.findall(r'M\d+', raw)
    if p['sumber_peta'] == 'harian':
        kaedah, kongsi, sumber = raw, p.get('kaedah_kongsi') or [], 'harian'
        ps = POS[(raw, s)]
        kel = keluar_dari_enjin(ps.get('keluar'), hb, s)
        r = baris(p['tarikh_beli'], s, kaedah, kongsi, hb, unit, kini, kel, kaedah, sumber, ps.get('henti'), ps.get('sasaran'))
    elif ids and p['sumber_peta'] == 'log_v1':
        kaedah = ids[0]; kongsi = sorted(set(ids[1:] + (p.get('kaedah_kongsi') or [])))
        # padan log
        cand = [l for l in log if l['saham'] == s and l['teknik'] == raw] or [l for l in log if l['saham'] == s and kaedah in l['teknik']] or [l for l in log if l['saham'] == s]
        lg = None
        if cand:
            terb = [l for l in cand if l['status'].startswith('terbuka')]
            lg = (terb or cand)[0]
        kel = None; henti = lg.get('henti') if lg else None
        nota = 'Pegangan warisan v1 (log 7 Okt).'
        if lg and not lg['status'].startswith('terbuka') and lg.get('harga_keluar'):
            tk = tarikh_status(lg['status'])
            if 'keluar buka' in lg['status'] or 'keluar pada buka' in lg['status']:
                m2 = re.findall(r'(\d+) Okt', lg['status']); tk = f'2026-10-{int(m2[-1]):02d}'
            kel = (tk, float(lg['harga_keluar']), 'Keluar: ' + lg['status'])
        elif lg and not lg['status'].startswith('terbuka'):
            kel = None; nota += ' Status log: ' + lg['status']
        # kaedah lama tanpa id M dalam POS? semak enjin harian juga
        ps = POS.get((kaedah, s))
        if not kel and ps and ps.get('keluar'):
            kel = keluar_dari_enjin(ps['keluar'], hb, s)
        if not kel and henti:
            for o in OHLC.get(s, []):
                if o['buka'] <= henti:
                    kel = (o['tarikh'], o['buka'], f"Keluar: kena henti {o['tarikh'][8:]} Okt (buka {o['buka']:.2f} di bawah henti)"); break
                if o['rendah'] <= henti:
                    kel = (o['tarikh'], henti, f"Keluar: kena henti {o['tarikh'][8:]} Okt (keluar pada harga henti)"); break
        r = baris(p['tarikh_beli'], s, kaedah, kongsi, hb, unit, kini, kel, kaedah, 'log_v1', henti, None, nota)
        if not kel: r['isyarat_keluar'] = 'Pegang (warisan v1)' + (f' (henti {henti:.2f})' if henti else '')
    else:
        nm = raw.split(' (')[0]
        r = baris(p['tarikh_beli'], s, nm, [], hb, unit, kini, None, None, 'luar', None, None,
                  'Strategi luar 87 M; tidak dikira dalam slot kaedah M; tiada peraturan keluar M.')
        r['isyarat_keluar'] = 'Pegang (luar M)'
    moomoo.append(r)

# ---------- CLAUDE ----------
claude, batal = [], []
for m, p in PEN:
    s = p['saham']; snap = SNAP.get(s)
    if 'tarikh_masuk' in p:
        hb = p['harga_masuk_andaian']; tb = p['tarikh_masuk']
        kel = keluar_dari_enjin(p.get('keluar'), hb, s)
        kini = float(snap['last_price']) if snap and snap.get('last_price') else p.get('harga_terkini')
        sumber = 'penuh_v1'
    else:
        tb = HARI_INI
        if not snap or not snap.get('open_price'):
            batal.append((m, s, 'tiada harga buka')); continue
        hb = float(snap['open_price'])
        if p.get('henti') and hb <= p['henti']:
            batal.append((m, s, f'buka {hb} <= henti {p["henti"]}')); continue
        kel = None; kini = float(snap['last_price']); sumber = 'penuh_20261012'
    r = baris(tb, s, m, [], hb, 1, kini, kel, m, sumber, p.get('henti'), p.get('sasaran'),
              f"Maya: isyarat {p['tarikh_isyarat']} ketika slot Moomoo penuh; harga beli = buka sebenar hari masuk.")
    r['tarikh_isyarat'] = p['tarikh_isyarat']
    claude.append(r)

# slot
slot_c = collections.Counter(r['kaedah'] for r in claude if not r['keluar'])
slot_c_all = collections.Counter(r['kaedah'] for r in claude)
slot = {m: {'moomoo': SLOT.get(m, 0), 'claude_terbuka': slot_c.get(m, 0), 'claude_jumlah': slot_c_all.get(m, 0), 'nama': NAMA.get(m)} for m in sorted(SLOT)}

print('moomoo', len(moomoo), collections.Counter(r['keluar'] for r in moomoo), collections.Counter(r['sumber'] for r in moomoo))
print('claude', len(claude), collections.Counter(r['keluar'] for r in claude), collections.Counter(r['sumber'] for r in claude))
print('batal', batal)
print('tiada sektor', [r['saham'] for r in moomoo + claude if r['sektor'] == 'Lain-lain'])
print('penuh10', sum(1 for v in slot.values() if v['moomoo'] >= 10))

COLS = ['tarikh_beli', 'saham', 'kaedah', 'sektor', 'industri', 'harga_beli', 'unit', 'harga_terkini', 'untung_pct', 'hari',
        'isyarat_keluar', 'tarikh_keluar', 'harga_keluar', 'untung_akhir_pct', 'id_kaedah', 'sumber', 'kaedah_kongsi', 'henti', 'sasaran', 'keluar', 'nota']
def tulis_csv(fn, rows, extra=()):
    with open(fn, 'w', newline='') as fh:
        w = csv.writer(fh); cols = COLS + list(extra); w.writerow(cols)
        for r in sorted(rows, key=lambda r: (r['tarikh_beli'], r['kaedah'], r['saham'])):
            w.writerow(['+'.join(r.get(c) or []) if c == 'kaedah_kongsi' else ('' if r.get(c) is None else r.get(c)) for c in cols])
tulis_csv('moomoo.csv', moomoo)
tulis_csv('claude.csv', claude, ['tarikh_isyarat'])
json.dump({'rows': moomoo, 'harga_pada': HARGA_PADA, 'akaun': '4135388', 'dibina': DIBINA,
           'nota': 'P2: 208 posisi akaun simulasi Moomoo. Isyarat keluar daripada enjin harian (data tutup 9 Okt) + log v1 (7 Okt); isyarat "jual pada buka esok" diisi harga buka 12 Okt. Baris keluar dibekukan; posisi TIDAK dijual. Harga terkini = Moomoo intraday 12 Okt.'},
          open('out_moomoo.json', 'w'))
json.dump({'rows': claude, 'slot': slot, 'harga_pada': HARGA_PADA, 'dibina': DIBINA, 'batal': [list(b) for b in batal],
           'nota': 'P2: posisi maya Claude Papertrade (1 unit). 276 rekod slot penuh lama (isyarat 7–8 Okt, masuk buka 8–9 Okt) + isyarat 9 Okt masuk buka 12 Okt. Harga terkini = Moomoo snapshot intraday 12 Okt.'},
          open('out_claude.json', 'w'))
