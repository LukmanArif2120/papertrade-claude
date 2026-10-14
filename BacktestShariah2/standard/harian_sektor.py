# Harian (6:02 MYT) — bina snapshot sektor/industri (papertrade/sektor.csv + db sektor/snapshot)
# Diadaptasi daripada standard/bina_p3_sektor.py: stor harga kini termasuk bar tutup terkini, SST = tutup sesi sama.
# Input: sst_us.csv (SST screen_stocks US), sst_raw.json (breadth/institusi/volum), af/<aset harga>.csv, db2/papertrade/*.json
import csv, json, statistics as st, collections, sys, os
SP = os.path.dirname(os.path.abspath(__file__)) + '/'
A = SP + 'af/'
F = lambda x: float(x) if x not in ('', None) else None
raw = json.load(open(SP + 'sst_raw.json'))
sst = {r['ticker']: r for r in csv.DictReader(open(SP + 'sst_us.csv'))}
peta = {}
for f in ['claude', 'moomoo', 'senarai_beli', 'watchlist']:
    d = json.load(open(SP + 'db2/papertrade/%s.json' % f)); d = d.get('data', d)
    for r in d['rows']:
        if r.get('sektor') and r.get('industri'): peta[r['saham']] = (r['sektor'], r['industri'], r.get('nama') or '')
def heat(key):
    g = collections.defaultdict(list)
    for r in sst.values(): g[r[key]].append(r)
    out = {}
    for k, a in g.items():
        ch = [F(r['changePercent']) for r in a if F(r['changePercent']) is not None]
        rs = [F(r['rsRating']) for r in a if F(r['rsRating']) is not None]
        sc = [F(r['sstScore']) for r in a if F(r['sstScore']) is not None]
        out[k] = dict(avgChangePct=st.mean(ch) if ch else None, avgRsRating=st.mean(rs) if rs else None, avgSstScore=st.mean(sc) if sc else None,
                      advancersCount=sum(x > 0 for x in ch), declinersCount=sum(x < 0 for x in ch), marketCap=sum(F(r['marketCap']) or 0 for r in a))
    return out
heatS, heatI = heat('sector'), heat('industry')
sek_sst = set(heatS)
H = collections.defaultdict(list)
for fn in ['c0ea371042d455671d97fd203f9e6014.csv', 'd1c8189cd2a79685005cbb7462bfeaf3.csv']:
    for r in csv.DictReader(open(A + fn)):
        c = F(r['close'])
        if c: H[r['ticker']].append((r['date'], c, F(r['volume']) or 0))
for t in H: H[t].sort()
univ = {r['ticker']: r for r in csv.DictReader(open(A + '067c3ee5895f4689140eb94f6074fd26.csv'))}
TARIKH = max(h[-1][0] for h in H.values() if h)
def ret(cl, kini, n):
    return (kini / cl[-n] - 1) * 100 if len(cl) >= n and cl[-n] else None
saham = []
for t in set(H) | set(sst):
    s = sst.get(t)
    if s: sek, ind, nama = s['sector'], s['industry'], s['company']; sumber = 'SST'
    elif t in peta:
        sek, ind, nama = peta[t]; sumber = 'peta'
        if sek not in sek_sst: continue
        if ind not in heatI: ind = None
    else: continue
    h = [x for x in H.get(t, []) if x[0] <= TARIKH]
    cl = [x[1] for x in h]; vo = [x[2] for x in h]
    harga_sst = F(s['price']) if s else None
    kini = harga_sst or (cl[-1] if cl else None)
    # stor kini mengandungi bar sesi terakhir; harga SST = tutup sesi sama -> rujukan 5/21/63 sesi lalu = cl[-6]/[-22]/[-64]
    n1w, n1m, n3m = 6, 22, 64
    r1w = ret(cl, kini, n1w) if cl else None
    r1m = ret(cl, kini, n1m) if cl else None
    r3m = ret(cl, kini, n3m) if cl else None
    sma50 = st.mean(cl[-50:]) if len(cl) >= 50 else None
    atas50 = (kini > sma50) if (sma50 and kini) else None
    rv = (st.mean(vo[-5:]) / st.mean(vo[-50:])) if len(vo) >= 50 and st.mean(vo[-50:]) > 0 else None
    saham.append(dict(t=t, nama=nama, sek=sek, ind=ind, sumber=sumber, kini=kini, d1=F(s['changePercent']) if s else None,
                      r1w=r1w, r1m=r1m, r3m=r3m, atas50=atas50, rv=rv, rs=F(s['rsRating']) if s else None,
                      sst=F(s['sstScore']) if s else None, mcap=F(s['marketCap']) if s else (F(univ[t]['floatcap']) if t in univ else None),
                      ada_harga=bool(cl)))
beli = {r['ticker'] for r in raw['inst_buy']}; jual = {r['ticker'] for r in raw['inst_sell']}
uv = {r['ticker'] for r in raw['unusual']}
def kump(jenis, key, heat):
    g = collections.defaultdict(list)
    for s in saham:
        if s[key]: g[s[key]].append(s)
    out = []
    for nama, a in g.items():
        hp = [s for s in a if s['ada_harga']]
        m = lambda k: (st.median([s[k] for s in hp if s[k] is not None]) if any(s[k] is not None for s in hp) else None)
        ab = [s['atas50'] for s in hp if s['atas50'] is not None]
        hm = heat.get(nama, {})
        rs = hm.get('avgRsRating')
        if rs is None:
            v = [s['rs'] for s in a if s['rs'] is not None]; rs = st.mean(v) if v else None
        nb = sum(s['t'] in beli for s in a); nj = sum(s['t'] in jual for s in a)
        top = sorted([s for s in a if s['r1m'] is not None], key=lambda s: -s['r1m'])[:3]
        out.append(dict(nama=nama, jenis=jenis, sektor=(a[0]['sek'] if jenis == 'Industri' else nama),
            n=len(a), n_harga=len(hp),
            prestasi_1d=hm.get('avgChangePct', m('d1')), prestasi_1w=m('r1w'), prestasi_1m=m('r1m'), prestasi_3m=m('r3m'),
            rs=rs, breadth=(sum(ab) / len(ab) * 100 if ab else None), volum_relatif=m('rv'),
            aliran_beli=nb, aliran_jual=nj, aliran_institusi=nb - nj, volum_luar_biasa=sum(s['t'] in uv for s in a),
            naik=hm.get('advancersCount'), turun=hm.get('declinersCount'), sst=hm.get('avgSstScore'),
            mcap=hm.get('marketCap') or sum(s['mcap'] or 0 for s in a),
            teratas=[dict(saham=s['t'], nama=s['nama'], r1m=round(s['r1m'], 2), r1w=None if s['r1w'] is None else round(s['r1w'], 2),
                          sst=s['sst'], rs=s['rs']) for s in top]))
    return out
S = kump('Sektor', 'sek', heatS); I = kump('Industri', 'ind', heatI)
hp = [s for s in saham if s['ada_harga']]
mk = {k: st.median([s[k] for s in hp if s[k] is not None]) for k in ['r1w', 'r1m', 'r3m']}
def pr(vals, v):
    vs = sorted(x for x in vals if x is not None)
    if v is None or not vs: return 50.0
    return 100.0 * sum(x < v for x in vs) / max(1, len(vs) - 1) if len(vs) > 1 else 50.0
W = dict(prestasi_1m=.25, prestasi_1w=.15, prestasi_3m=.15, breadth=.15, rs=.15, volum_relatif=.10, aliran_institusi=.05)
for grp, minn in ((S, 1), (I, 3)):
    ok = [g for g in grp if g['n_harga'] >= minn]
    for g in grp:
        g['skor_panas'] = round(sum(w * pr([x[k] for x in ok], g[k]) for k, w in W.items()), 1) if g['n_harga'] >= minn else None
        x = None if g['prestasi_3m'] is None else g['prestasi_3m'] - mk['r3m']
        y = None if g['prestasi_1m'] is None else g['prestasi_1m'] - mk['r1m']
        g['rel_3m'], g['rel_1m'] = x, y
        g['fasa'] = None if x is None or y is None else ('Leading' if x > 0 and y > 0 else 'Weakening' if x > 0 else 'Improving' if y > 0 else 'Lagging')
        g['sampel_kecil'] = g['n_harga'] < 3
        for k in list(g):
            if isinstance(g[k], float): g[k] = round(g[k], 2)
rows = sorted(S, key=lambda g: -(g['skor_panas'] or -1)) + sorted(I, key=lambda g: -(g['skor_panas'] or -1))
br = raw['breadth']
doc = dict(rows=rows, dibina=sys.argv[1], tarikh_harga=TARIKH, harga_kini='SST Terminal tutup ' + TARIKH + ' (dikemas kini selepas tutup); selain itu tutup Moomoo ' + TARIKH,
           sumber='SST Terminal: screen_stocks (heatmap sektor & industri dikira semula), institutional_flow (BUYING/SELLING), unusual_volume (≥2×), market_breadth; sejarah harga harian stor dashboard (harga_A/B, termasuk tutup terkini Moomoo)',
           pasaran=dict(r1w=round(mk['r1w'], 2), r1m=round(mk['r1m'], 2), r3m=round(mk['r3m'], 2), naik=br['advancers'], turun=br['decliners'], adr=round(br['adr'], 2),
                        atas_sma50=round(br['pctAboveSma50'], 1), atas_sma200=round(br['pctAboveSma200'], 1), rsi=round(br['avgRsi'], 1), net_tinggi52=br['netNewHighs'],
                        n_saham=len(saham), n_harga=len(hp)),
           institusi_beli=[dict(saham=r['ticker'], nama=r['companyName'], ubah=round(r['holderPctChange'], 2)) for r in raw['inst_buy'][:10]],
           institusi_jual=[dict(saham=r['ticker'], nama=r['companyName'], ubah=round(r['holderPctChange'], 2)) for r in raw['inst_sell'][:10]],
           volum_luar_biasa=[dict(saham=r['ticker'], nama=r['companyName'], rv=round(r['relativeVolume'], 2), ubah=round(r['changePct'], 2)) for r in raw['unusual']],
           pemberat=W, definisi_fasa='Leading: 3M & 1M atasi pasaran; Weakening: 3M atasi tetapi 1M kalah; Improving: 3M kalah tetapi 1M atasi; Lagging: kedua-dua kalah. Pasaran = purata sama rata semua saham berharga.')
json.dump(doc, open(SP + 'sektor_snapshot.json', 'w'), ensure_ascii=False, separators=(',', ':'))
K = ['jenis', 'nama', 'sektor', 'n', 'n_harga', 'prestasi_1d', 'prestasi_1w', 'prestasi_1m', 'prestasi_3m', 'rs', 'breadth', 'volum_relatif', 'aliran_beli', 'aliran_jual',
     'aliran_institusi', 'volum_luar_biasa', 'rel_3m', 'rel_1m', 'fasa', 'skor_panas', 'teratas']
with open(SP + 'sektor.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(K + ['dibina'])
    for g in rows: w.writerow([' '.join(f"{x['saham']}({x['r1m']:+.1f}%)" for x in g['teratas']) if k == 'teratas' else g[k] for k in K] + [sys.argv[1]])
print(len(S), len(I), len(saham), len(hp), TARIKH, mk, len(json.dumps(doc, separators=(',', ':'))))
for g in rows[:12]: print(g['jenis'], g['nama'], g['skor_panas'], g['fasa'], g['prestasi_1w'], g['prestasi_1m'], g['breadth'], g['n_harga'])
for g in [x for x in rows if x['jenis'] == 'Industri'][:10]: print(g['nama'], g['skor_panas'], g['n_harga'], [x['saham'] for x in g['teratas']])
