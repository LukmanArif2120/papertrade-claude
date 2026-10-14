import json, statistics as st
SP = '/tmp/claude-0/-home-claude/1065e185-9b92-5438-9115-e17141ed91ba/scratchpad/'
M = json.load(open(SP + 'out_moomoo.json'))['rows']; C = json.load(open(SP + 'out_claude.json'))['rows']
mae = json.load(open(SP + 'out_mae.json'))['rows']
cl = lambda x: max(0, min(1, x))
def rows(ak, R):
    out = []
    for r in R:
        u = r['untung_akhir_pct'] if r.get('keluar') else r['untung_pct']
        k = f"{ak}|{r['saham']}|{r['kaedah']}|{r['tarikh_beli']}"
        out.append(dict(ak=ak, saham=r['saham'], kaedah=r['kaedah'], u=u, keluar=bool(r.get('keluar')), hari=r.get('hari') or 0,
                        dd=mae.get(k, min(u, 0))))
    return out
def kpi(T):
    us = [t['u'] for t in T]
    w = min(T, key=lambda t: t['u'])
    return dict(dagangan=len(T), kadar_menang=round(100 * sum(u > 0 for u in us) / len(us), 1), untung_purata=round(st.mean(us), 2),
                untung_median=round(st.median(us), 2), rugi_terbesar=round(w['u'], 2), rugi_terbesar_saham=f"{w['saham']} ({w['kaedah']})",
                hari_purata=round(st.mean(t['hari'] for t in T), 1), kaedah=len({t['kaedah'] for t in T}), keluar=sum(t['keluar'] for t in T),
                penurunan_maks_purata=round(st.mean(t['dd'] for t in T), 2))
def kaedah(T):
    g = {}
    for t in T: g.setdefault(t['kaedah'], []).append(t)
    out = []
    for k, a in g.items():
        us = [t['u'] for t in a]; n = len(a); avg = st.mean(us); win = sum(u > 0 for u in us) / n
        dd = st.mean(t['dd'] for t in a); worst = min(us)
        U = 0.6 * cl((avg + 5) / 15) + 0.4 * win; S = 0.6 * cl(1 + dd / 10) + 0.4 * cl(1 + worst / 20)
        sk = 100 * U * S * min(1, n / 5); gagal = 1 - win
        kl = sum(1 for t in a if t['keluar'] and t['u'] < 0)
        kep = 'HENTIKAN' if n >= 5 and (avg <= -3 or gagal >= .75 or sk < 25) else 'TERUSKAN' if n >= 5 and sk >= 55 and avg > 0 else 'PERHATI'
        out.append(dict(kaedah=k, n=n, menang=round(100 * win, 1), purata=round(avg, 2), median=round(st.median(us), 2), terburuk=round(worst, 2),
                        dd=round(dd, 2), gagal=round(100 * gagal, 1), keluar_rugi=kl, skor=round(sk, 1), keputusan=kep))
    return sorted(out, key=lambda x: -x['skor'])
res = {}
for nm, T in [('M', rows('M', M)), ('C', rows('C', C)), ('Combine', rows('M', M) + rows('C', C))]:
    K = kaedah(T)
    res[nm] = dict(kpi=kpi(T), kaedah=K,
                   teruskan=[x['kaedah'] for x in K if x['keputusan'] == 'TERUSKAN'],
                   hentikan=[x['kaedah'] for x in K if x['keputusan'] == 'HENTIKAN'],
                   bil={k: sum(x['keputusan'] == k for x in K) for k in ['TERUSKAN', 'PERHATI', 'HENTIKAN']},
                   teruk_gagal=[(x['kaedah'], x['gagal'], x['n']) for x in sorted([x for x in K if x['n'] >= 3], key=lambda x: -x['gagal'])[:5]],
                   teruk_rugi=[(x['kaedah'], x['terburuk']) for x in sorted(K, key=lambda x: x['terburuk'])[:5]],
                   teruk_keluar_rugi=[(x['kaedah'], x['keluar_rugi']) for x in sorted(K, key=lambda x: -x['keluar_rugi'])[:5]],
                   top=[(x['kaedah'], x['skor'], x['purata'], x['menang'], x['n']) for x in K[:5]])
json.dump(dict(res, dibina='2026-10-13 06:10 MYT', harga_pada='2026-10-12 tutup',
               nota='Dikira semula oleh larian 6:02 MYT dengan peraturan skor & keputusan P4 (sama seperti halaman). Halaman mengira sendiri daripada papertrade/moomoo + claude + prestasi/mae; dokumen ini rekod ringkasan.'),
          open(SP + 'out_prestasi.json', 'w'), ensure_ascii=False, separators=(',', ':'))
for nm in res:
    r = res[nm]; print(nm, r['kpi'], r['bil']); print(' TERUSKAN', r['teruskan']); print(' HENTIKAN', r['hentikan']); print(' top', r['top'])
    print(' teruk', r['teruk_gagal'], r['teruk_rugi'], r['teruk_keluar_rugi'])
