# jana_db.py — dokumen db dashboard daripada fail repo (tanpa LLM), untuk sesi Claude harian yang hanya MENOLAK fail ke db
# (ArtifactData batch dengan file_path; tugasan_v3 §6). Menggantikan JSON yang dibina dengan tangan oleh rutin 6:02 / 7:47 / 9:35.
#
#   python3 BacktestShariah2/standard/jana_db.py --keluar <folder> [--versi versi.json]
#   -> <folder>/<koleksi>/<doc>.json, <folder>/batch_<n>.json (senarai writes ArtifactData; <= 50 tulisan dan < 900 KB
#      setiap batch) dan <folder>/ringkas.json. --versi: {"papertrade/claude": 14, …} (daripada senarai ArtifactData list)
#      supaya setiap tulisan membawa if_version; dokumen tanpa versi = dokumen baharu.
# Dokumen: papertrade/moomoo, papertrade/claude… (1:1 dengan claude*.csv), (senarai_beli tidak ditolak sejak 19 Okt 2026),
# papertrade/watchlist(+_2…), prestasi/ringkasan, prestasi/mae, prestasi/mae_atr (dibahagi), prestasi/harian_kaedah, prestasi/portfolio_slot, analisis/papan, harian/status,
# harian/trend (trend_status.py), harian/stage (stage.py), posisi/lorong2(+_2…; lorong2_siri.py). sektor/snapshot dijana oleh tugasan
# mingguan (data/db/sektor_snapshot.json, jika ada; medan posisi dikemas kini di sini).
import argparse, csv, glob, hashlib, json, os, re, statistics as stt, sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(BS2, 'kod'))
import sahkan as SH  # noqa: E402
from bahagi_db import bahagi, padat, bait, HAD_DB  # noqa: E402
from pecah_claude import nilai, nombor_fail  # noqa: E402

PT = os.path.join(BS2, 'papertrade')
STOR = os.path.join(BS2, 'data', 'harga', 'stor')
MIN_TUTUP = 20
USD_POSISI = 1000
HAD_BATCH = 900_000
STATUS_HARGA = os.path.join(BS2, 'data', 'harga', 'status.json')

PETA_WATCH = {'Saham': 'saham', 'Nama': 'nama', 'Kaedah': 'kaedah', 'Sektor': 'sektor', 'Industri': 'industri',
              'Harga': 'harga_terkini', '% hampir': 'pct_dipenuhi', 'Pencetus': 'pencetus', 'Keadaan semasa': 'sebab',
              'Syarat belum cukup': 'syarat_belum', 'Syarat dipenuhi': 'syarat_dipenuhi', 'Paras pencetus': 'paras',
              'Jarak %': 'jarak_pct', 'Tarikh masuk watchlist': 'ditambah', 'Hari dalam watchlist': 'hari', 'Skor': 'skor',
              'Set': 'set', 'tarikh_data': None, 'dibina': None}


def baris_db(r, peta=None):
    """Baris CSV -> baris db: medan kosong digugurkan, nilai bertaip (sama dengan pecah_claude.nilai)."""
    out = {}
    for k, v in r.items():
        if v in ('', None) or k == 'kewangan_butiran':   # JSON butiran kekal dalam CSV sahaja (had saiz db)
            continue
        if peta is not None:
            if k in peta and peta[k] is None:
                continue
            k = peta.get(k, k)
        out[k] = nilai(v) if k not in ('saham', 'nama', 'kaedah_kongsi', 'tarikh_isyarat', 'tarikh_beli') else v
    return out


def earn_sebenar(db, r, K):
    """Tambah tarikh earnings seterusnya SEBENAR (kalendar gabungan kalendar_earnings.py) kepada baris db (bukan CSV): earn_seb,
    earn_seb_h (hari dagangan dari sesi rujukan), earn_seb_sumber. Sesi rujukan = tarikh QR asal (gred_pada "QR pada X"),
    tarikh_isyarat / tarikh_data, atau hari bekerja sebelum tarikh_beli. Gred QR asal tidak diubah (audit 23 Okt 2026)."""
    from datetime import date, timedelta
    import kalendar_earnings as KE
    m = re.search(r'QR pada (\d{4}-\d\d-\d\d)', r.get('gred_pada') or '')
    t0 = (m.group(1) if m else None) or r.get('tarikh_isyarat') or r.get('tarikh_data')
    if t0:
        D = date.fromisoformat(t0[:10])
    elif r.get('tarikh_beli'):
        D = date.fromisoformat(r['tarikh_beli'][:10]) - timedelta(days=1)
        while D.weekday() > 4:
            D -= timedelta(days=1)
    else:
        return db
    te, sb = KE.seterusnya(K, r.get('saham') or r.get('Saham'), D)
    if te:
        db.update(earn_seb=te.isoformat(), earn_seb_h=int(np.busday_count(D + timedelta(days=1), te + timedelta(days=1))) if te > D else 0,
                  earn_seb_sumber=sb)
    return db


def baca_csv(p):
    return SH.baca(p)[1] if os.path.exists(p) else []


def sah(r):
    return not (SH.benar(r.get('tidak_dibeli')) or SH.benar(r.get('tidak_sah')) or SH.benar(r.get('luar_peraturan')))


# ---------------------------------------------------------------- prestasi (peraturan sama dengan halaman; tugasan_v3 §7)
def prestasi(M, C, mae):
    cl = lambda x: max(0, min(1, x))

    def rows(ak, R):
        out = []
        for r in R:
            if not sah(r) or r.get('harga_beli') in (None, ''):
                continue
            kel = SH.benar(r.get('keluar'))
            u = float(r['untung_akhir_pct'] if kel else r['untung_pct'] or 0)
            k = f"{ak}|{r['saham']}|{r['kaedah']}|{r['tarikh_beli']}"
            out.append(dict(saham=r['saham'], kaedah=r['kaedah'], u=u, keluar=kel, hari=int(float(r.get('hari') or 0)),
                            dd=mae.get(k, min(u, 0))))
        return out

    def kpi(T):
        if not T:
            return {}
        us = [t['u'] for t in T]; w = min(T, key=lambda t: t['u'])
        return dict(dagangan=len(T), kadar_menang=round(100 * sum(u > 0 for u in us) / len(us), 1), untung_purata=round(stt.mean(us), 2),
                    untung_median=round(stt.median(us), 2), rugi_terbesar=round(w['u'], 2), rugi_terbesar_saham=f"{w['saham']} ({w['kaedah']})",
                    hari_purata=round(stt.mean(t['hari'] for t in T), 1), kaedah=len({t['kaedah'] for t in T}), keluar=sum(t['keluar'] for t in T),
                    penurunan_maks_purata=round(stt.mean(t['dd'] for t in T), 2),
                    untung_usd_sama=round(sum(us) / 100 * USD_POSISI, 2), modal_usd_sama=len(T) * USD_POSISI)

    def kaedah(T):
        g = {}
        for t in T:
            g.setdefault(t['kaedah'], []).append(t)
        out = []
        for k, a in g.items():
            us = [t['u'] for t in a]; n = len(a); avg = stt.mean(us); win = sum(u > 0 for u in us) / n
            dd = stt.mean(t['dd'] for t in a); worst = min(us)
            U = 0.6 * cl((avg + 5) / 15) + 0.4 * win; S_ = 0.6 * cl(1 + dd / 10) + 0.4 * cl(1 + worst / 20)
            sk = 100 * U * S_ * min(1, n / 5); gagal = 1 - win
            ntutup = sum(1 for t in a if t['keluar'])
            kep = ('BELUM CUKUP DATA' if ntutup < MIN_TUTUP else
                   'HENTIKAN' if (avg <= -3 or gagal >= .75 or round(sk) < 25) else
                   'TERUSKAN' if round(sk) >= 55 and avg > 0 else 'PERHATI')
            out.append(dict(kaedah=k, n=n, menang=round(100 * win, 1), purata=round(avg, 2), median=round(stt.median(us), 2),
                            terburuk=round(worst, 2), dd=round(dd, 2), gagal=round(100 * gagal, 1),
                            keluar_rugi=sum(1 for t in a if t['keluar'] and t['u'] < 0), tutup=ntutup, skor=round(sk, 1), keputusan=kep))
        return sorted(out, key=lambda x: -x['skor'])

    res = {}
    for nm, T in [('M', rows('M', M)), ('C', rows('C', C)), ('Combine', rows('M', M) + rows('C', C))]:
        K = kaedah(T)
        res[nm] = dict(kpi=kpi(T), kaedah=K, teruskan=[x['kaedah'] for x in K if x['keputusan'] == 'TERUSKAN'],
                       hentikan=[x['kaedah'] for x in K if x['keputusan'] == 'HENTIKAN'],
                       bil={k: sum(x['keputusan'] == k for x in K) for k in ['TERUSKAN', 'PERHATI', 'HENTIKAN', 'BELUM CUKUP DATA']},
                       teruk_gagal=[(x['kaedah'], x['gagal'], x['n']) for x in sorted([x for x in K if x['n'] >= 3], key=lambda x: -x['gagal'])[:5]],
                       teruk_rugi=[(x['kaedah'], x['terburuk']) for x in sorted(K, key=lambda x: x['terburuk'])[:5]],
                       teruk_keluar_rugi=[(x['kaedah'], x['keluar_rugi']) for x in sorted(K, key=lambda x: -x['keluar_rugi'])[:5]],
                       top=[(x['kaedah'], x['skor'], x['purata'], x['menang'], x['n']) for x in K[:5]])
    return res


def penurunan_maks(M, C, stor):
    """prestasi/mae: (rendah terendah sejak hari beli hingga kini, atau hingga sehari sebelum keluar + harga keluar) ÷ harga beli − 1."""
    fr = pd.concat([pd.read_csv(os.path.join(stor, f), usecols=['ticker', 'date', 'low']) for f in ('harga_A.csv', 'harga_B.csv')
                    if os.path.exists(os.path.join(stor, f))])
    L = {t: g.set_index('date')['low'] for t, g in fr.groupby('ticker')}
    out = {}
    for ak, R in (('M', M), ('C', C)):
        for r in R:
            hbv = SH.nombor(r.get('harga_beli'))
            if hbv is None or not hbv or SH.benar(r.get('tidak_dibeli')):
                continue
            k = f"{ak}|{r['saham']}|{r['kaedah']}|{r['tarikh_beli']}"
            b = int(r['tarikh_beli'].replace('-', '')); lo = L.get(r['saham'])
            if lo is None:
                continue
            if SH.benar(r.get('keluar')) and r.get('tarikh_keluar'):
                e = int(r['tarikh_keluar'].replace('-', '')); w = lo[(lo.index >= b) & (lo.index < e)].tolist()
                if SH.nombor(r.get('harga_keluar')) is not None:
                    w.append(float(r['harga_keluar']))
            else:
                w = lo[lo.index >= b].tolist()
            if not w:
                continue
            v = round(min(0.0, (min(w) / hbv - 1) * 100), 2)
            out[k] = min(v, out.get(k, 0.0))
    return out


def atr_isyarat(M, C, stor, n=14):
    """ATR14 % pada bar terakhir sebelum hari beli (hari isyarat) bagi setiap posisi: purata julat benar 14 hari ÷ tutup × 100
    (formula enjin.atr). Dipakai skor kaedah swing v2 untuk MAE ÷ ATR. Kunci sama dengan prestasi/mae."""
    fr = pd.concat([pd.read_csv(os.path.join(stor, f), usecols=['ticker', 'date', 'high', 'low', 'close']) for f in ('harga_A.csv', 'harga_B.csv')
                    if os.path.exists(os.path.join(stor, f))])
    A = {}
    for t, g in fr.groupby('ticker'):
        g = g.drop_duplicates('date', keep='last').sort_values('date').set_index('date'); c = g.close
        tr = pd.concat([g.high - g.low, (g.high - c.shift()).abs(), (g.low - c.shift()).abs()], axis=1).max(axis=1)
        A[t] = (tr.rolling(n).mean() / c * 100).dropna()
    out = {}
    for ak, R in (('M', M), ('C', C)):
        for r in R:
            a = A.get(r.get('saham'))
            if a is None or not r.get('tarikh_beli') or SH.benar(r.get('tidak_dibeli')):
                continue
            s = a[a.index < int(r['tarikh_beli'].replace('-', ''))]
            if len(s):
                out[f"{ak}|{r['saham']}|{r['kaedah']}|{r['tarikh_beli']}"] = round(float(s.iloc[-1]), 3)
    return out


HAD_RINGKAS = 200000


def kod_lajur(R):
    """Baris db -> bentuk padat ikut lajur (dashboard v90): (kolum, jenis, kamus, rows). jenis setiap lajur:
    'b' boolean (0/1), 'k' rentetan berulang (indeks kamus + 1), 'j' senarai/campuran berulang (kamus JSON, indeks + 1),
    '' nilai asal. Medan yang tiada = 0 bagi 'k'/'j', null bagi yang lain. Kamus dikongsi semua bahagian; halaman menyahkod
    kepada objek sama seperti baris_db()."""
    cols = sorted({k for r in R for k in r})
    jenis, kamus, lajur = [], {}, []
    for c in cols:
        v = [r.get(c) for r in R]
        s = [x for x in v if x is not None]
        if s and all(isinstance(x, bool) for x in s):
            jenis.append('b'); lajur.append([None if x is None else int(x) for x in v]); continue
        if s and all(isinstance(x, (str, list)) for x in s):
            js = any(isinstance(x, list) for x in s)
            k = [None if x is None else (json.dumps(x, ensure_ascii=False) if js else x) for x in v]
            u = sorted({x for x in k if x is not None})
            if len(u) < 0.6 * len(R):
                ix = {x: i for i, x in enumerate(u)}; kamus[c] = u
                jenis.append('j' if js else 'k'); lajur.append([0 if x is None else ix[x] + 1 for x in k]); continue
        jenis.append(''); lajur.append(v)
    return cols, jenis, kamus, [list(t) for t in zip(*lajur)]


def ringkas_pt(R, nama, meta, had=HAD_RINGKAS):
    """[(doc_id, dokumen)] padat bagi papertrade/ringkas_c|m (susunan baris dikekalkan):
    <nama> = meta + kolum + jenis + bahagian {id, n, nk} + rows bahagian 1; <nama>_2.._n = {induk, bahagian, rows};
    <nama>_kamus_1.._nk = {induk, kamus: [[lajur, mula, [nilai…]], …]} (senarai panjang dipecah ikut segmen)."""
    cols, jenis, kamus, rows = kod_lajur(R)
    ident = hashlib.sha1(padat(R).encode('utf-8')).hexdigest()[:12]
    asas_kosong = bait(dict(meta, kolum=cols, jenis=jenis, bahagian=dict(id=ident, n=999, nk=999), rows=[]))
    bhg, cur, guna = [], [], asas_kosong
    for r in rows:
        sz = bait(r) + 1
        if cur and guna + sz > had:
            bhg.append(cur); cur, guna = [], 60
        cur.append(r); guna += sz
    bhg.append(cur)
    seg, cur, guna = [], [], 60
    for c, u in kamus.items():
        i = 0
        while i < len(u):
            j, sz = i, 0
            while j < len(u) and (j == i or guna + sz + bait(u[j]) + 1 < had):
                sz += bait(u[j]) + 1; j += 1
            if cur and guna + sz > had:
                seg.append(cur); cur, guna = [], 60
            cur.append([c, i, u[i:j]]); guna += sz + len(c) + 12; i = j
    if cur:
        seg.append(cur)
    out = [(nama, dict(meta, kolum=cols, jenis=jenis, bahagian=dict(id=ident, n=len(bhg), nk=len(seg)), rows=bhg[0]))]
    out += [(f'{nama}_{j}', dict(induk=ident, bahagian=j, rows=b)) for j, b in enumerate(bhg[1:], 2)]
    out += [(f'{nama}_kamus_{j}', dict(induk=ident, kamus=k)) for j, k in enumerate(seg, 1)]
    return out


SESI_GARIS = 60


def garis_harga(M, C, stor):
    """prestasi/garis + prestasi/mfe (pratonton dashboard v3).
    garis: tarikh (<= 60 sesi terakhir stor), tutup setiap saham yang masih ada posisi terbuka atau keluar dalam sesi
    terakhir (carta kecil, harga sesi sebelum)
    dan spy [[tarikh, buka, tutup]] sejak belian terawal (banding pasaran). mfe: [[kunci, kenaikan maks %], …] =
    (tinggi tertinggi sejak hari beli hingga kini, atau hingga sehari sebelum keluar lorong kaedah + harga keluar) ÷ harga beli − 1, minimum 0."""
    fr = pd.concat([pd.read_csv(os.path.join(stor, f), usecols=['ticker', 'date', 'high', 'close']) for f in ('harga_A.csv', 'harga_B.csv')
                    if os.path.exists(os.path.join(stor, f))])
    G = {t: g.set_index('date') for t, g in fr.groupby('ticker')}
    hari = sorted(int(d) for d in fr.date.unique())[-SESI_GARIS:]
    mfe, terbuka, mula, mula_t = {}, set(), None, None
    for ak, R in (('M', M), ('C', C)):
        for r in R:
            hbv = SH.nombor(r.get('harga_beli'))
            if hbv is None or not hbv or SH.benar(r.get('tidak_dibeli')):
                continue
            b = int(r['tarikh_beli'].replace('-', '')); mula = b if mula is None else min(mula, b)
            ts = r.get('tutup_semua')
            akhir = max(r.get('tarikh_keluar') or '', r.get('tarikh_keluar_henti') or '').replace('-', '')
            # posisi terbuka, atau keluar dalam sesi terakhir (masih terbuka pada sesi sebelum: perbandingan "sejak semalam")
            if not SH.benar(ts if ts not in (None, '') else r.get('keluar')) or (akhir.isdigit() and len(hari) > 1 and int(akhir) > hari[-2]):
                terbuka.add(r['saham']); mula_t = b if mula_t is None else min(mula_t, b)
            g = G.get(r['saham'])
            if g is None:
                continue
            if SH.benar(r.get('keluar')) and r.get('tarikh_keluar'):
                e = int(r['tarikh_keluar'].replace('-', '')); w = g.high[(g.index >= b) & (g.index < e)].tolist()
                if SH.nombor(r.get('harga_keluar')) is not None:
                    w.append(float(r['harga_keluar']))
            else:
                w = g.high[g.index >= b].tolist()
            if w:
                k = f"{ak}|{r['saham']}|{r['kaedah']}|{r['tarikh_beli']}"
                mfe[k] = max(round(max(0.0, (max(w) / hbv - 1) * 100), 2), mfe.get(k, 0.0))
    hari = [d for d in hari if mula_t is None or d >= mula_t] or hari[-1:]
    rows = []
    for t in sorted(terbuka):
        g = G.get(t)
        if g is None:
            continue
        c = g.close.reindex(hari)
        if c.notna().any():
            rows.append(dict(s=t, c=[None if pd.isna(x) else round(float(x), 2) for x in c]))
    spy = []
    pi = os.path.join(stor, 'harga_idx.csv')
    if os.path.exists(pi) and mula:
        I = pd.read_csv(pi)
        I = I[(I.ticker == 'SPY') & (I.date >= mula)].sort_values('date')
        spy = [[int(d), round(float(o), 2), round(float(c), 2)] for d, o, c in zip(I.date, I.open, I.close)]
    return dict(tarikh=hari, spy=spy, rows=rows), [[k, v] for k, v in sorted(mfe.items())]


TERKINI = os.path.join(BS2, 'data', 'harga', 'terkini.csv')


def harian_kaedah(M, C, stor, terkini=None):
    """prestasi/harian_kaedah (grid prestasi harian setiap kaedah, tab Prestasi): untung harian % setiap kaedah setiap sesi =
    Σ perubahan nilai ÷ Σ nilai awal hari bagi posisi USD_POSISI yang dipegang hari itu (hari beli: tutup lawan harga beli; hari
    keluar lorong kaedah: harga keluar lawan tutup semalam; tiada bar = harga semalam). j = untung purata % (untung akhir bagi
    yang keluar, semasa bagi yang dipegang; sama dengan Prestasi). ev = [[indeks hari, beli, keluar untung, keluar rugi]].
    Akaun M, C dan G (gabung); k 'Semua' = semua kaedah akaun itu. spy = untung harian % SPY. Harga: stor + terkini.csv
    (bar harian terbaharu; stor repo boleh ketinggalan satu sesi)."""
    fail = [os.path.join(stor, f) for f in ('harga_A.csv', 'harga_B.csv', 'harga_idx.csv')] + ([terkini] if terkini else [])
    fr = pd.concat([pd.read_csv(f, usecols=['ticker', 'date', 'close']) for f in fail if os.path.exists(f)])
    fr['date'] = fr.date.astype(int)
    fr = fr.drop_duplicates(['ticker', 'date'], keep='last')
    P = {t: dict(zip(g.date, g.close.astype(float))) for t, g in fr.groupby('ticker')}
    pos = []
    for ak, R in (('M', M), ('C', C)):
        for r in R:
            hb = SH.nombor(r.get('harga_beli'))
            if not sah(r) or not hb or not r.get('tarikh_beli'):
                continue
            kel = SH.benar(r.get('keluar'))
            hk = SH.nombor(r.get('harga_keluar')) if kel else None
            e = int(r['tarikh_keluar'].replace('-', '')) if kel and hk is not None and r.get('tarikh_keluar') else None
            u = SH.nombor(r.get('untung_akhir_pct') if kel else r.get('untung_pct'))
            pos.append((ak, r['kaedah'], r['saham'], int(r['tarikh_beli'].replace('-', '')), e, hb, hk, u or 0.0))
    if not pos:
        return dict(tarikh=[], spy=[], rows=[])
    mula = min(p[3] for p in pos)
    bil = fr[fr.ticker != 'SPY'].date.value_counts()
    hari = sorted(d for d, n in bil.items() if d >= mula and n >= 0.5 * bil.max())   # sesi separa (stor belum lengkap) diabaikan
    ix = {d: i for i, d in enumerate(hari)}
    sp = sorted(P.get('SPY', {}).items())
    spy = []
    for d in hari:
        lalu = [c for t, c in sp if t < d]
        spy.append(round(100 * (P['SPY'][d] / lalu[-1] - 1), 2) if lalu and d in P.get('SPY', {}) else None)
    agg = {}
    for ak, k, s, b, e, hb, hk, u in pos:
        harga = P.get(s, {})
        kunci = ((ak, k), ('G', k), (ak, 'Semua'), ('G', 'Semua'))
        for kk in kunci:
            x = agg.setdefault(kk, dict(pnl=[0.0] * len(hari), asas=[0.0] * len(hari), n=[0] * len(hari), u=[], ev={}))
            x['u'].append(u)
            if b in ix:
                x['ev'].setdefault(ix[b], [0, 0, 0])[0] += 1
            if e in ix:
                x['ev'].setdefault(ix[e], [0, 0, 0])[1 if hk > hb else 2] += 1
        lalu = hb
        for d in hari:
            if d < b:
                continue
            if e is not None and d > e:
                break
            kini = hk if e is not None and d == e else harga.get(d, lalu)
            i = ix[d]
            for kk in kunci:
                x = agg[kk]
                x['pnl'][i] += USD_POSISI * (kini - lalu) / hb; x['asas'][i] += USD_POSISI * lalu / hb; x['n'][i] += 1
            lalu = kini
    no = lambda k: (-1 if k == 'Semua' else int(k[1:]) if k[1:].isdigit() else 9999, k)
    rows = []
    for (ak, k), x in sorted(agg.items(), key=lambda kv: ('MCG'.index(kv[0][0]), no(kv[0][1]))):
        rows.append(dict(a=ak, k=k, np=len(x['u']), j=round(stt.mean(x['u']), 2),
                         d=[round(100 * p / a, 2) if a > 0 else None for p, a in zip(x['pnl'], x['asas'])], n=x['n'],
                         ev=[[i] + v for i, v in sorted(x['ev'].items())]))
    return dict(tarikh=hari, spy=spy, rows=rows)


def pengawas(st, masa):
    """Larian Actions yang sepatutnya sudah siap tetapi belum (untuk sesi tolak db: tembak workflow sekali).
    harian.yml: sesi NYSE terakhir yang tutup >= 9 jam lalu (data Yahoo muktamad); beli.yml: hari ini NY selepas 9:45."""
    try:
        import exchange_calendars as xc
    except ImportError:
        return {}
    c = xc.get_calendar('XNYS'); ny = masa.tz_convert('America/New_York'); hari = ny.normalize().tz_localize(None)
    sesi = [s for s in c.sessions_in_range(hari - pd.Timedelta(days=10), hari)
            if pd.Timestamp(f'{s.date()} 16:00', tz='America/New_York') + pd.Timedelta(hours=9) <= ny]
    jangka = str(sesi[-1].date()) if sesi else ''
    out = dict(malam_sesi=st.get('malam', {}).get('sesi', ''), malam_jangka=jangka,
               beli_tarikh=st.get('beli', {}).get('tarikh', ''), tembak=[])
    if jangka and out['malam_sesi'] < jangka:
        out['tembak'].append('harian.yml')
    if c.is_session(hari) and ny.hour * 60 + ny.minute >= 9 * 60 + 45 and out['beli_tarikh'] != str(hari.date()):
        out['beli_jangka'] = str(hari.date()); out['tembak'].append('beli.yml')
    return out


def portfolio_slot(dibina, folder=os.path.join(BS2, 'portfolio_slot')):
    """prestasi/portfolio_slot: portfolio maya 10 slot (standard/portfolio_slot.py, daripada Lejar Penuh) untuk kad Eksperimen
    dalam tab Ringkasan dan panel Skor kaedah swing (gabungan beku). Portfolio tanpa fail dilangkau; None jika RS_10 belum dijana.
    Setiap portfolio: mula, sesi dan spy_pct tempoh sama (portfolio beku bermula pada mula_jejak)."""
    import portfolio_slot as PS
    out = {}
    for k, nama in PS.PORTFOLIO.items():
        pe, pp = os.path.join(folder, f'{k}_ekuiti.csv'), os.path.join(folder, f'{k}_posisi.csv')
        if not (os.path.exists(pe) and os.path.exists(pp)):
            continue
        E, R = pd.read_csv(pe), pd.read_csv(pp)
        if E.empty and k not in PS.BEKU_JENIS:
            continue
        kel = R[R.status == 'Keluar']
        out[k] = dict(nama=f'{k}: {nama}', pulangan_pct=round(100 * (E.ekuiti.iloc[-1] - 1), 2) if len(E) else None,
                      mdd_pct=round(100 * PS.mdd(E.ekuiti), 2) if len(E) else None,
                      dipegang=int((R.status == 'Pegang').sum()), keluar=int(len(kel)),
                      menang_pct=round(100 * float((kel.untung_pct > 0).mean()), 1) if len(kel) else None,
                      mula=E.tarikh.iloc[0] if len(E) else None, sesi=int(len(E)),
                      spy_pct=round(100 * (float(E.spy.iloc[-1]) - 1), 2) if len(E) and pd.notna(E.spy.iloc[-1]) else None,
                      ekuiti=[[t, round(float(e), 5)] for t, e in zip(E.tarikh, E.ekuiti)],
                      posisi=json.loads(R.round(4).to_json(orient='records')))
    rs = out.get('RS_10')
    if not rs or not rs['sesi']:
        return None
    beku = None
    try:
        beku = json.load(open(os.path.join(BS2, 'data', 'analisis', 'gabungan_beku.json'), encoding='utf-8'))
    except (OSError, ValueError):
        pass
    return dict(dibina=dibina, mula=rs['mula'], sesi_terakhir=rs['ekuiti'][-1][0], sesi=rs['sesi'], spy_pct=rs['spy_pct'], portfolio=out,
                beku=beku,
                nota='Rekod sahaja (kajian/KAJIAN_PORTFOLIO.md). 10 slot x 10% ekuiti, satu posisi setiap saham. RS_10 = RS pasaran '
                     'tertinggi, RAWAK_10 = kawalan rawak (lorong 2). GABUNGAN_10 / TOP1_10 / RAWAK_KAEDAH_10 = gabungan kaedah beku '
                     '(data/analisis/gabungan_beku.json) lawan #1 sahaja lawan kaedah rawak, sejak mula_jejak. Dibina semula setiap malam oleh lejar.yml.')


def sesi_stor(path=STATUS_HARGA):
    """Sesi terkini stor harga repo (status.json terkini.sesi, YYYYMMDD) sebagai YYYY-MM-DD; '' jika tiada.
    Sandaran tarikh data apabila status_harian.json tiada dalam folder (mod bayang: Actions menulis ke bayang/ sahaja)."""
    try:
        s = str(json.load(open(path, encoding='utf-8')).get('terkini', {}).get('sesi', ''))
    except (OSError, ValueError, AttributeError):
        return ''
    return f'{s[:4]}-{s[4:6]}-{s[6:8]}' if len(s) == 8 and s.isdigit() else ''


def _produksi_n(rd, ff, ii, bl, RV, reg):
    """94 kombinasi masuk x keluar yang DIPILIH untuk produksi.

    STATUS (semak sebelum mendakwa apa-apa): "produksi" di sini bermaksud DIPILIH dan
    SIAP, bukan sedang berjalan. Cetusan `schedule` GitHub Actions sentiasa berjalan dari
    cawangan LALAI, jadi imbasan malam hanya memasukkan kombinasi ini selepas kodnya
    digabung ke `main`. Medan `hidup` di bawah dikira daripada kandungan repo sebenar
    (bilangan fail kod/kaedah/<ID>.py yang ada), bukan ditulis tangan.

    Populasi ini BERBEZA daripada registry Nxx di atas dan tidak boleh dicampur:
    registry = katalog peraturan (263 baris, tidak didagangkan); produksi = kombinasi
    `masuk`+`keluar` yang lulus empat syarat pradaftar SPEC_GRID_PENUH.md pada grid
    penuh 1,495 sel dengan penyebut BH-FDR jujur m=1,495, dan yang kodnya ADA dalam
    kod/kaedah/. Sumber: REVERSE/jejak_semua.csv + REVERSE/grid_penuh.csv.

    Corong dikira daripada CSV, bukan ditulis tangan, supaya ia tidak boleh hanyut.
    PENTING: s1/s2/s3 ialah syarat BEBAS yang mesti lulus SERENTAK. Kiraan bersarang
    (688 -> 313) dan kiraan berasingan (s2 sendiri 461) ialah dua perkara berbeza;
    kedua-duanya dilaporkan supaya bar corong tidak boleh dibaca salah.
    """
    J, G = rd(os.path.join(RV, 'jejak_semua.csv')), rd(os.path.join(RV, 'grid_penuh.csv'))
    if not J or not G:
        return None
    # STATUS DIKIRA, BUKAN DITULIS. Panel pernah mendakwa "diimbas setiap malam sejak
    # 2 Nov 2026" sementara `main` tiada satu pun modul Nxx dan Papertrade C tiada satu
    # pun posisi Nxx. Dakwaan prosa hanyut; kiraan tidak. `kod` = modul yang ADA,
    # `posisi` = posisi Nxx dalam Papertrade C, `lejar` = baris Nxx dalam Lejar Penuh.
    # Halaman menyatakan status daripada ketiga-tiga nombor ini sahaja.
    import glob as _glob
    import re as _re
    hidup = {x['masuk'] + x['keluar'] for x in J}
    kod = sum(1 for i in hidup
              if os.path.exists(os.path.join(BS2, 'kod', 'kaedah', i + '.py')))

    def _kira(pola, medan=('kaedah', 'id')):
        n = 0
        for f in sorted(_glob.glob(os.path.join(BS2, *pola))):
            for r in rd(f):
                k = next((r[m] for m in medan if r.get(m)), '')
                if _re.match(r'^N\d', str(k)):
                    n += 1
        return n

    posisi, lejar_n = _kira(('papertrade', 'claude*.csv')), _kira(('lejar', '*.csv'))
    B = lambda x, k: x.get(k) == 'True'
    n1 = sum(1 for x in G if B(x, 's1_mutlak'))
    n12 = sum(1 for x in G if B(x, 's1_mutlak') and B(x, 's2_lift'))
    n123 = sum(1 for x in G if B(x, 's123'))
    nfdr = sum(1 for x in G if B(x, 'lulus'))
    s2_sendiri = sum(1 for x in G if B(x, 's2_lift'))
    s3_sendiri = sum(1 for x in G if B(x, 's3_n'))
    lulus = [x for x in G if B(x, 'lulus')]
    hidup = {(x['masuk'], x['keluar']) for x in J}
    buang = [x for x in lulus if (x['masuk'], x['keluar']) not in hidup]
    kl_hidup = {x['keluar'] for x in J}
    b_keluar = [x for x in buang if x['keluar'] not in kl_hidup]
    b_rs = [x for x in buang if x['keluar'] in kl_hidup]
    kira = {}
    for x in J:
        kira[x['keluar']] = kira.get(x['keluar'], 0) + 1
    kel = {}
    for x in J:
        kel[x['keluarga']] = kel.get(x['keluarga'], 0) + 1
    # Nama dan peraturan MASUK TIDAK diulang di sini: ia sudah ada sekali dalam `rows`
    # (registry, satu sumber kebenaran standard/registry_n.py) dan dashboard mencarinya
    # ikut `masuk`. Mengulangnya 94 kali menambah ~12 KB pada dokumen yang hadnya 256 KB,
    # dan mewujudkan dua salinan peraturan yang sama yang boleh hanyut berasingan.
    # Lajur `peraturan` dalam jejak_semua.csv ialah peraturan KELUAR, bukan masuk, jadi ia
    # dinamakan `keluar_aturan` supaya tiada sesiapa membacanya sebagai peraturan masuk.
    hil = sorted({x['masuk'] for x in J} - {x['id'] for x in reg})
    baris = [dict(
        pangkat=ii(x.get('pangkat')), id=x['masuk'] + x['keluar'], masuk=x['masuk'],
        keluar=x['keluar'], kel=x.get('keluarga'), keluar_aturan=x.get('peraturan'),
        jangkaan=ff(x.get('jangkaan_tahan')), jangkaan_latih=ff(x.get('jangkaan_latih')),
        lift=ff(x.get('lift_tahan')), lift_latih=ff(x.get('lift_latih')),
        n=ii(x.get('n_tahan')), menang=ff(x.get('menang'), 1),
        untung=ff(x.get('untung'), 2), rugi=ff(x.get('rugi'), 2),
        tanpa5=ff(x.get('tanpa5_tahan')), p=ff(x.get('p'), 6)) for x in J]
    pos = [r for r in baris if (r['tanpa5'] or 0) > 0]
    return dict(
        bil=len(J), sel=len(G), masuk_unik=len({x['masuk'] for x in J}),
        hilang_registry=hil,
        kod=kod, posisi=posisi, lejar=lejar_n,
        berjalan=bool(posisi or lejar_n),
        keluar=sorted(kira.items(), key=lambda kv: -kv[1]),
        keluarga=sorted(kel.items(), key=lambda kv: -kv[1]),
        corong=[dict(g='Sel grid penuh (65 masuk x 23 keluar)', n=len(G), sendiri=None),
                dict(g='S1 jangkaan mutlak > 0 pada KEDUA-DUA tingkap', n=n1, sendiri=n1),
                dict(g='+ S2 lift > 0 pada KEDUA-DUA tingkap', n=n12, sendiri=s2_sendiri),
                dict(g='+ S3 n_tahan >= 200', n=n123, sendiri=s3_sendiri),
                dict(g='+ S4 BH-FDR q <= 0.05, penyebut m = ' + str(len(G)),
                     n=nfdr, sendiri=nfdr),
                dict(g='- keluar yang enjin tidak boleh laksana', n=nfdr - len(b_keluar),
                     sendiri=None),
                dict(g='- masuk yang perlukan RS (N69, N70, N120)',
                     n=nfdr - len(buang), sendiri=None)],
        buang_keluar=len(b_keluar), buang_rs=len(b_rs),
        keluar_buang=sorted({x['keluar'] for x in b_keluar}),
        tanpa5_positif=len(pos),
        tanpa5_x13=sum(1 for r in pos if r['keluar'] == 'X13'),
        baris=baris,
        status=('Modul kod ' + str(kod) + '/' + str(len(J)) + ' ADA dalam repo ini, '
                'tetapi ' + ('ada ' + str(posisi) + ' posisi Papertrade C dan ' +
                             str(lejar_n) + ' baris Lejar'
                             if (posisi or lejar_n) else
                             'SIFAR posisi Papertrade C dan SIFAR baris Lejar Penuh') +
                '. Cetusan `schedule` GitHub Actions sentiasa berjalan dari cawangan '
                'LALAI, jadi kombinasi ini hanya masuk imbasan malam selepas kodnya '
                'DIGABUNG ke cawangan itu. Sehingga jurang itu ditutup, "produksi" '
                'bermaksud DIPILIH dan DISAHKAN hujung-ke-hujung, bukan sedang berjalan '
                '- dan nombor ini dikira daripada kandungan repo, bukan ditulis tangan, '
                'supaya ia tidak boleh hanyut daripada kebenaran.'),
        nota='Setiap ID ialah KOMBINASI masuk+keluar (cth N19X13), bukan kaedah berdiri '
             'sendiri: masuk yang sama dengan keluar berbeza ialah baris berbeza, dan '
             'grid penuh mengukur bahawa keluar yang salah MENYEMBUNYIKAN masuk yang '
             'terbaik - N124 x X15 (+16.127%, sel terbaik dalam seluruh kajian) GAGAL '
             'gate dalam grid jarang kerana N124 hanya pernah diuji pada X1-X4. '
             'Konfigurasi sama bagi kesemua 94: cara C01 beli buka esok, TIADA henti '
             '(stop = NaN, jadi kecacatan henti hari-0 mustahil secara struktur), TIADA '
             'sasaran, TMAX 126 bar, rank U14 momentum 12-1, lorong 2 Chandelier 4xATR14 '
             'kekal automatik seperti semua posisi lain.',
        had='HAD WAJIB. (1) Ini jangkaan SETIAP DAGANGAN pada tingkap TAHAN 2020-2025, '
            'BUKAN prestasi portfolio: ujian portfolio 8/40 slot lawan SPUS memberi 0/36 '
            'lulus (CAGR 9.3-16.1%, MDD -22% hingga -63% lawan SPUS +17.95%/-26.82%), '
            'jadi ini kohort setiap dagangan dan T4 (SPUS + tunai) kekal cadangan modal. '
            '(2) tanpa5 POSITIF hanya pada ' + str(len(pos)) + ' daripada ' +
            str(len(J)) + ', jadi kelebihan yang lain '
            'hidup dalam ekor kanan dan SETUP.md terpakai sepenuhnya kepada mereka. '
            '(3) N124 latih +3.064 lawan tahan +16.127 = jurang 5x; jangan saiz ia '
            'seperti +16%. (4) Alam A02 tiada saham delist. (5) Kohort akan dilabel '
            'BELUM CUKUP 3-6 bulan kerana pegangan median 36-64 hari.',
    )


def kaedah_n(dibina):
    """Dokumen kaedah_n/papan: registry Nxx (262 baris, 11 paksi) + hasil 371 ujian dipradaftar.

    Sumber: data/registry_N.csv (satu sumber kebenaran = standard/registry_n.py) dan empat CSV
    keputusan dalam REVERSE/ (nxx, nxx_keluar, gabungan, silang_akhir). Rekod kajian sahaja;
    bukan isyarat beli. Tab "Kaedah N" dalam dashboard membacanya.
    """
    import csv as _csv
    akar = os.path.dirname(BS2)

    def rd(p_):
        return list(_csv.DictReader(open(p_, encoding='utf-8'))) if os.path.exists(p_) else []

    def ff(x, d=3):
        try:
            return round(float(x), d)
        except (TypeError, ValueError):
            return None

    def ii(x):
        try:
            return int(float(x))
        except (TypeError, ValueError):
            return None

    def bl(x):
        return str(x) == 'True'

    KEL = ['MA', 'RSI', 'BB', 'TREND', 'PECAH', 'VOLUM', 'UNDUR', 'KETAT', 'ADX', 'VWAP',
           'POLA', 'KEKUATAN', 'OSILATOR', 'KALENDAR', 'REJIM', 'LILIN']
    RV = os.path.join(akar, 'REVERSE')
    reg = rd(os.path.join(BS2, 'data', 'registry_N.csv'))
    if not reg:
        return None
    A, B = rd(os.path.join(RV, 'nxx.csv')), rd(os.path.join(RV, 'nxx_keluar.csv'))
    G, X = rd(os.path.join(RV, 'gabungan.csv')), rd(os.path.join(RV, 'silang_akhir.csv'))
    best = {}
    for r in A:
        nm = r.get('masuk', '')
        if nm == 'N01_semak':
            continue
        key = nm[:4] if nm.startswith('N104') else nm
        lt = ff(r.get('lift_tahan'))
        if lt is None:
            continue
        cur = best.get(key)
        if cur is None or lt > cur['lift_tahan']:
            best[key] = dict(keluar=r.get('keluar'), lift_latih=ff(r.get('lift_latih')),
                             lift_tahan=lt, jangkaan=ff(r.get('jangkaan_tahan')),
                             n=ii(r.get('n_tahan')), menang=ff(r.get('menang'), 1),
                             tanpa5=ff(r.get('tanpa5_tahan')), p=ff(r.get('p'), 6),
                             g1=bl(r.get('gate1')), g2=bl(r.get('gate2')))
    rows = []
    for x in reg:
        d = dict(id=x['id'], paksi='MASUK' if x['keluarga'] in KEL else x['keluarga'],
                 kel=x['keluarga'], nama=x['nama'], aturan=x['masuk'] or x['nama'],
                 sumber=x['sumber'], plat=x['platform'], status=x['status'])
        if x['id'] in best:
            d['hasil'] = best[x['id']]
        rows.append(d)
    UJ = _ujian_n(A, B, G, X, rd(os.path.join(RV, 'portfolio_n_ringkas.csv')),
                  rd(os.path.join(RV, 'cara.csv')), ff, ii, bl)
    return dict(
        dibina=dibina,
        nota='TIGA populasi dalam tab ini, unitnya BERBEZA dan ia TIDAK boleh dicampur. '
             '(1) PRODUKSI: 94 kombinasi masuk x keluar yang DIPILIH pada 2 Nov 2026 '
             'daripada grid penuh 1,495 sel dengan penyebut BH-FDR jujur - "produksi" '
             'bermaksud dipilih dan siap, dan ia hanya masuk imbasan malam selepas '
             'kodnya digabung ke cawangan lalai. '
             '(2) REGISTRY: 263 baris merentas 11 paksi (MASUK, KELUAR, CARA, URUTAN, '
             'GABUNGAN, SAIZ, ALAM, PEGANG, IMBANG, KORELASI, INSTRUMEN) - katalog '
             'peraturan, BUKAN isyarat beli. (3) KAJIAN: (a) 413 ujian '
             'setiap-dagangan - NXX.md (280), NXX_KELUAR.md (69), GABUNGAN.md (14), '
             'SILANG_AKHIR.md (8), PORTFOLIO_N.md (36), CARA.md (6), daripadanya 10 lulus '
             'gate akhir; (b) 724 konfigurasi portfolio dalam baris gilir E1-E6 '
             '(PEGANG_SLOT, ALAM, INSTRUMEN, KELUAR_PORTFOLIO, KORELASI, HIERARKI) atas '
             '6,994 larian, daripadanya 161 lulus pulangan, 24 lulus risiko, dan SIFAR '
             'lulus kedua-duanya. Baris gilir ditutup 31 Okt 2026: BERHENTI-TUTUP, lihat '
             'REVERSE/KEPUTUSAN_AKHIR.md. Setiap spec DAN kod dikomit sebelum keputusan '
             'dilihat. Nombor kajian di bawah ialah REKOD KAJIAN, bukan isyarat beli; '
             'hanya 94 kombinasi dalam panel PRODUKSI yang benar-benar membeli.',
        rows=rows,
        gate=dict(A=dict(ujian=280, g1=52, g2=7, g3=0), B=dict(ujian=69, g1=24, g2=0, g3=0),
                  GAB=dict(ujian=14, g1=13, g2=8, g3=2), SX=dict(ujian=8, g1=8, g2=8, g3=8)),
        # Dua pradaftar 31 Okt 2026 dengan gate TERSENDIRI, jadi diasingkan daripada jadual
        # gate1/2/3 di atas (REVERSE/PORTFOLIO_N.md, REVERSE/CARA.md).
        port=dict(ujian=36, larian=264, P1=3, P2=6, P3=15, P4=1, lulus=0,
                  spus_cagr=17.95, spus_mdd=-26.82, spus_nisbah=0.669,
                  baris=[dict(k='GB02_atau4 · 40 slot · X15 · U02', cagr=29.28, mdd=-56.51,
                              nisbah=0.52, dedah=94.4, nb=1, p5=None, p95=None),
                         dict(k='GB02_atau3 · 40 slot · X13 · U01', cagr=13.92, mdd=-38.38,
                              nisbah=0.36, dedah=81.6, nb=20, p5=7.21, p95=21.16),
                         dict(k='GB02_atau3 · 8 slot · X13 · U01', cagr=9.40, mdd=-44.82,
                              nisbah=0.21, dedah=82.8, nb=20, p5=1.14, p95=24.45),
                         dict(k='RAWAK · 8 slot · X15 · U08 (tiada isyarat)', cagr=11.19,
                              mdd=-12.14, nisbah=0.92, dedah=98.9, nb=1, p5=None, p95=None)],
                  diambil=[dict(k='populasi penuh', n=195681, min=8.541, menang=64.2,
                                pegang=None, tanpa5=2.858),
                           dict(k='diambil, 8 slot', n=674, min=8.015, menang=67.1,
                                pegang=84.9, tanpa5=1.558),
                           dict(k='diambil, 40 slot', n=3495, min=7.483, menang=63.5,
                                pegang=81.5, tanpa5=1.140)]),
        cara=dict(ujian=6, C1=0, C2=0, C3=4, lulus=0,
                  baris=[dict(k='C01', n='pasaran buka esok (asas repo)', isi=100.0,
                              sig=8.540, isian=8.541, menang=64.2, tanpa5=2.858, h0=0),
                         dict(k='C02', n='buy-stop tinggi20 x1.002, 5 bar', isi=13.3,
                              sig=0.682, isian=5.119, menang=65.8, tanpa5=-0.180, h0=0),
                         dict(k='C03', n='buy-limit -1.5%, 3 bar', isi=72.2,
                              sig=7.227, isian=10.011, menang=64.6, tanpa5=3.945, h0=0),
                         dict(k='C04', n='buy-limit -1.0%, 3 bar', isi=79.0,
                              sig=7.429, isian=9.408, menang=64.5, tanpa5=3.577, h0=0),
                         dict(k='C05', n='OCO -2% / +2%, 5 bar', isi=98.0,
                              sig=8.044, isian=8.208, menang=63.7, tanpa5=2.563, h0=0),
                         dict(k='C06', n='bracket +6% / -3%', isi=100.0,
                              sig=-0.591, isian=-0.591, menang=32.9, tanpa5=-0.985,
                              h0=65240)]),
        keluar=[dict(keluar=r['keluar'], peraturan=r.get('peraturan'),
                     jangkaan=ff(r.get('jangkaan_tahan')), menang=ff(r.get('menang'), 1),
                     n=ii(r.get('n_tahan'))) for r in B if r.get('masuk') == 'ASAS'],
        gabungan=[dict(konfig=r['konfig'], lift_latih=ff(r.get('lift_latih')),
                       lift_tahan=ff(r.get('lift_tahan')), jangkaan=ff(r.get('jangkaan_tahan')),
                       menang=ff(r.get('menang'), 1), tanpa5=ff(r.get('tanpa5_tahan')),
                       p=ff(r.get('p'), 6), n=ii(r.get('n_tahan')), g3=bl(r.get('gate3')))
                  for r in G],
        silang=[dict(masuk=r['masuk'], keluar=r['keluar'], lift_latih=ff(r.get('lift_latih')),
                     lift_tahan=ff(r.get('lift_tahan')), jangkaan=ff(r.get('jangkaan_tahan')),
                     menang=ff(r.get('menang'), 1), untung=ff(r.get('untung'), 2),
                     rugi=ff(r.get('rugi'), 2), tanpa5=ff(r.get('tanpa5')),
                     asas5=ff(r.get('asas5')), p=ff(r.get('p'), 6), n=ii(r.get('n_tahan')),
                     g3=bl(r.get('gate3'))) for r in X],
        produksi=_produksi_n(rd, ff, ii, bl, RV, reg),
        tarik=TARIK_N,
        ujian=UJ,
        skor=_skor_n(UJ),
        giliran=_giliran(rd, ff, ii),
        akhir=dict(
            status='BERHENTI-TUTUP',
            konfig=724, larian=6994, P1=161, P2=24, P3=215, P4=45, T1=0, T3=0,
            spus_cagr=17.95, spus_mdd=-26.82,
            ayat='Set konfigurasi yang RISIKONYA boleh diterima dan set yang PULANGANNYA '
                 'mencukupi tidak pernah bertindih, dan jurangnya boleh diukur. 24 '
                 'konfigurasi melepasi P2; CAGR tertinggi antara kesemuanya ialah 13.55% '
                 'sedangkan SPUS memerlukan > 17.95% - jurang 4.40 mata. 161 melepasi P1; '
                 'tiada satu pun melepasi P2. Dan 22 daripada 24 yang risikonya boleh '
                 'diterima memakai masuk RAWAK, iaitu tiada isyarat langsung.',
            sebab='Portfolio ekuiti panjang-sahaja yang 100% melabur tidak boleh mempunyai '
                  'MDD lebih cetek daripada indeks ekuiti melainkan ia memegang tunai - '
                  'dan memegang tunai ialah T4. Enam mekanik bebas mengesahkannya.',
            dapatan=[
                'Keluar jauh lebih penting daripada masuk (sebaran 4.997 mata lawan lift '
                'masuk terbaik 0.392), dan keluar peringkat PORTFOLIO lebih penting lagi: '
                '+47.44% lawan +21.01% pada alam sama, kekal +34.78% selepas pembetulan '
                'titik-masa.',
                'Jangan tapis sehingga kolam calon runtuh - tetapi saringan BERDIRI '
                'membantu. Pintu harian (7.7-21.8 calon/sesi) memusnahkan pemeringkat '
                '(jurang 37.6 mata); saringan berdiri (102-326) memperbaiki kedua-dua '
                'paksi. Peraturan: kolam calon >= ~10x bilangan slot.',
                'Had industri ialah lever RISIKO yang hampir percuma. Dakwaan dwi-arah '
                'asal DITARIK BALIK 1 Nov 2026 oleh semakan luar sampel: kaki CAGR tidak '
                'bertahan (+1.65 pada 2020-2025 menjadi -0.19 pada 2012-2019) tetapi kaki '
                'MDD bertahan (+1.60 dan +1.12, mencetek pada 83.3% sel latih). Semakan '
                'semula dengan ujian tanda berpasangan menajamkannya: +1.65 itu TIDAK '
                'PERNAH signifikan walaupun dalam tingkapnya sendiri (16/24 sel, p=0.152), '
                'manakala kaki MDD MELEPASI BH-FDR luar sampel (20/23 sel, p=0.0005). '
                'Tanpa had, 6 daripada 8 slot boleh berada dalam satu industri.',
                'Masalah ekor ialah sifat ALAM, bukan hukum pasaran: 5% teratas membawa '
                '101.67% jumlah pulangan pada alam 3,260 nama, 47.92% pada 214 nama, dan '
                'tanpa5 POSITIF pada 8/8 sel bakul sektor.',
                'Volatiliti rendah ialah lever MDD terbesar dan paling KUKUH dalam '
                'kajian: MDD mencetek pada 12/12 sel dalam KEDUA-DUA tingkap (p=0.0005 '
                'setiap satu, melepasi FDR), +22.09 mata dalam tahan dan +18.62 dalam '
                'latih. Harganya bergantung TINGKAP: kos CAGR -17.47 mata dalam 2020-2025 '
                'tetapi TEPAT NOL dalam 2012-2019 (6/12 sel, p=1.000), jadi "pertukaran '
                'tulen" ialah sifat 2020-2025 sahaja.',
                'SEMAKAN LUAR SAMPEL 1 Nov 2026: saringan berdiri DISAHKAN tetapi '
                'magnitudnya runtuh (A2 +4.26 menjadi +0.64 mata CAGR). Yang bertahan '
                'ialah ARAH dan peraturan kolam, bukan nombor. Setiap kesan MDD dalam '
                'E1-E4 masih tingkap TAHAN sahaja.',
                'AYAT TUNGGAL SELEPAS SEMAKAN LUAR SAMPEL: daripada 28 kesan pembinaan '
                'yang diuji dengan ujian tanda berpasangan, 8 melepasi BH-FDR, 3 '
                'daripadanya luar sampel, dan KESEMUA 3 ialah kesan MDD. SIFAR kesan CAGR '
                'luar sampel melepasi FDR. Lever pembinaan menggerakkan RISIKO, bukan '
                'PULANGAN - dan itu kini benar pada dua tingkap dengan kawalan pelbagai '
                'ujian, bukan satu.'],
            t4=[dict(berat=100, cagr=17.95, mdd=-26.82),
                dict(berat=60, cagr=10.87, mdd=-16.62),
                dict(berat=40, cagr=7.27, mdd=-11.25),
                dict(berat=30, cagr=5.46, mdd=-8.50)],
            t4_nota='SISTEM.md mengukur nisbah CAGR/|MDD| campuran SPUS+tunai hampir '
                    'PEMALAR 0.642-0.669 merentas setiap berat, jadi tiada titik optimum '
                    'untuk dicari. Pilihan berat bukan soalan data - ia soalan toleransi '
                    'drawdown, dan itu keputusan pengguna. Diimbang bulanan; baki dalam '
                    'TUNAI, bukan bon.',
            priori=dict(betul=15, separa=3, salah=13)),
        metrik=METRIK_N,
    )


# Baris gilir E1-E6 (REVERSE/STRATEGI.md §4). Medan naratif ditulis tangan kerana ia
# DAPATAN, bukan agregat; kiraan gate dikira daripada CSV supaya ia tidak boleh hanyut.
GILIRAN = [
    dict(id='E1', nama='PEGANG x SLOT', alam='AL01', fail='pegang_slot_ringkas.csv',
         konfig=320, larian=3360, spec='SPEC_PEGANG_SLOT.md', lap='PEGANG_SLOT.md',
         khusus='Had pegangan 42 bar mengalahkan "tiada had" pada 72/128 sel; '
                'puncak +39.24% lawan +12.09% = +27.15 mata.',
         dapatan='SZ10 DITOLAK: lengkung slot memuncak pada 80-160 dan MEROSOT; kolam '
                 'penuh memberi 9.19-16.71%. Hingar pemilihan pada sel terbaik 42.8 mata '
                 'merentas 20 benih - jalur mengecil kepada 16.3 mata pada 160 slot, jadi '
                 'menambah slot membeli KEBOLEHPERCAYAAN bukan pulangan.', cabang='E2'),
    dict(id='E2', nama='ALAM AL02', alam='AL02', fail='alam_ringkas.csv', tapis='AL02',
         konfig=160, larian=1680, spec='SPEC_ALAM.md', lap='ALAM.md',
         khusus='Gate (a) isyarat > kawalan LULUS 46.2%; gate (b) had pegangan merentas '
                'alam GAGAL 27.5% — gabungan yang spec TIDAK liputi, jadi cabang ke E3 '
                'ialah keputusan pengguna, bukan keputusan yang pradaftar benarkan.',
         dapatan='Masalah EKOR ialah sifat ALAM, bukan hukum pasaran: 5% teratas membawa '
                 '101.67% jumlah pulangan pada alam a02 luas (95% lain NEGATIF bersih) '
                 'lawan 47.92% pada SPUS, dan tanpa5 +2.682% - POSITIF buat kali pertama '
                 'dalam kajian. HAD: keahlian SPUS semasa menghasilkan tepat kesan ini.',
         cabang='E3'),
    dict(id='E3', nama='INSTRUMEN IS02 bakul sektor', alam='AL02',
         fail='instrumen_ringkas.csv', konfig=40, larian=230,
         spec='SPEC_INSTRUMEN.md', lap='INSTRUMEN.md',
         khusus='E3 mengesahkan hipotesis SETUP.md: tanpa5 bakul POSITIF pada 8/8 sel '
                '(+0.55% hingga +4.77%, tertinggi dalam kajian) lawan 0/598 setup saham.',
         dapatan='Kepelbagaian merentas ekor MEMANG membetulkan masalah ekor - tetapi '
                 'masalah BERPINDAH kepada drawdown. Hanya U14 momentum 12-1 mengalahkan '
                 'kawalan (5/8); U11 dan U03 Clenow 0/8. Memegang bakul Electronic '
                 'Technology SAHAJA memberi +32.67%, mengalahkan setiap putaran.',
         cabang='E4'),
    dict(id='E4', nama='KELUAR portfolio X31/X32', alam='AL02',
         fail='keluar_portfolio_ringkas.csv', konfig=48, larian=276,
         spec='SPEC_KELUAR_PORTFOLIO.md', lap='KELUAR_PORTFOLIO.md',
         khusus='E4a LULUS: keluar peringkat portfolio mengalahkan keluar setiap posisi '
                'terbaik pada alam SAMA, +47.44% lawan +21.01%.',
         dapatan='PEMALSUAN: konfigurasi sama memberi +9.65%/-91.50% pada alam penuh dan '
                 '+34.78%/-68.80% pada 214 teratas TITIK-MASA. Pulangan separa bertahan; '
                 'risiko TIDAK - 30.9 mata kelebihan MDD AL02 ialah survivorship. Isyarat '
                 'masuk MEROSAKKAN putaran berpangkat: RAWAK +47.44% lulus P3, '
                 'GB02_atau3 +24.04% GAGAL P3.', cabang='E5'),
    dict(id='E5', nama='KORELASI KR03 had industri', alam='AL04 titik-masa',
         fail='korelasi_ringkas.csv', konfig=96, larian=1008,
         spec='SPEC_KORELASI.md', lap='KORELASI.md',
         khusus='E5a LULUS kedua-dua bahagian: had mencetekkan MDD pada 56.9% sel DAN '
                'menaikkan nisbah pada 52/72 sel.',
         dapatan='Had industri BUKAN pertukaran. Had 1 memperbaiki KEDUA-DUA paksi: '
                 '+1.65 mata CAGR DAN +1.60 mata MDD lebih cetek. Mekanisme: tanpa had, '
                 '6 daripada 8 slot boleh berada dalam SATU industri, jadi "8 slot" '
                 'sebenarnya ~3 taruhan. Dapatan E4 berulang lebih kuat: jurang RAWAK '
                 'lawan GB02 ialah 37.6 mata.', cabang='E6'),
    dict(id='E6', nama='GABUNGAN GB07 hierarki', alam='AL04 titik-masa',
         fail='hierarki_ringkas.csv', konfig=60, larian=440,
         spec='SPEC_HIERARKI.md', lap='HIERARKI.md',
         khusus='E6a LULUS: 19/48 sel saringan BERDIRI mengalahkan asas pada KEDUA-DUA '
                'paksi.',
         dapatan='Menapis tidak buruk - menapis sehingga JARANG yang buruk. Pintu masuk '
                 'HARIAN beri 7.7-21.8 calon/sesi (kolam lebih kecil daripada slot) dan '
                 'memusnahkan pemeringkat; saringan BERDIRI beri 102-326 (kolam 13-41x '
                 'slot) dan memperbaiki kedua-dua paksi. PERATURAN: kekalkan kolam calon '
                 '>= ~10x bilangan slot. A4 separuh ATR% rendah beri lever MDD TERBESAR '
                 'dalam kajian (+22.09 mata) tetapi -17.47 mata CAGR = pertukaran tulen.',
         cabang='BERHENTI-TUTUP'),
]


def _giliran(rd, ff, ii):
    """Satu baris setiap eksperimen baris gilir, kiraan gate dikira daripada CSV."""
    akar = os.path.dirname(BS2)
    out = []
    for g in GILIRAN:
        R = rd(os.path.join(akar, 'REVERSE', g['fail']))
        if g.get('tapis'):
            R = [r for r in R if str(r.get('alam')) == g['tapis']]
        d = dict({k: v for k, v in g.items() if k not in ('fail', 'tapis')},
                 sedia=bool(R))
        if R:
            def kira(k):
                return sum(1 for r in R if str(r.get(k)) == 'True')
            t1 = sum(1 for r in R
                     if (ff(r.get('cagr')) or -9e9) > 17.95
                     and (ff(r.get('mdd')) or -9e9) >= -26.82)
            t3 = sum(1 for r in R
                     if (ff(r.get('cagr')) or -9e9) >= 15.0
                     and (ff(r.get('mdd')) or -9e9) >= -15.0)
            cg = [ff(r.get('cagr')) for r in R if ff(r.get('cagr')) is not None]
            md = [ff(r.get('mdd')) for r in R if ff(r.get('mdd')) is not None]
            d.update(n=len(R), t1=t1, t3=t3, P1=kira('P1'), P2=kira('P2'),
                     P3=kira('P3'), P4=kira('P4'),
                     cagr_maks=max(cg) if cg else None,
                     mdd_cetek=max(md) if md else None)
        out.append(d)
    return out


# Nama tiga lajur metrik bagi setiap pradaftar. Diangkat ke sini, bukan diulang pada
# setiap baris: unitnya berbeza antara pradaftar dan papan mesti menamakannya, tetapi
# mengulang rentetan yang sama 422 kali memakan ~21 KB daripada had dokumen db.
# Penarikan balik 1 Nov 2026 (REVERSE/AUDIT_JEJAK_N.md). Dipaparkan pada panel yang
# menunjukkan nombor yang ditarik, supaya nombor lama tidak boleh dibaca sebagai dakwaan
# hidup. Nombor itu DIKEKALKAN, bukan dibuang: ia rekod apa yang pernah didakwa.
TARIK_N = dict(
    tarikh='1 Nov 2026',
    fail='REVERSE/AUDIT_JEJAK_N.md',
    tajuk='Dakwaan "silang akhir 8/8 lulus semua gate" DITARIK BALIK',
    sebab='Penyebut BH-FDR dalam step21_silang_akhir.py ialah M_PRADAFTAR = 8 sedangkan '
          'step18 guna 358 dan step19 guna 349. Dengan 8 baris, ambang BH = 0.05 x 8/8 = '
          '0.05, iaitu p < 0.05 TANPA sebarang pembetulan pelbagai ujian. Pada panel yang '
          'SAMA, N19 x X13 p=0.003576 direkod gate2 GAGAL (dinilai pada m=349) sementara '
          'GB02_atau3 x X13 p=0.006803 direkod gate2 LULUS (dinilai pada m=8) - p yang '
          'lebih BESAR lulus kerana penyebutnya lebih kecil. gate3 juga dilonggarkan '
          'daripada "tanpa5 > 0" kepada "tanpa5 > asas5" selepas spec ditulis.',
    salah=['"satu-satunya yang lulus gate0-gate3" SALAH: 8 daripada 12 baris lulus.',
           '"satu-satunya dengan tanpa5 positif" SALAH: GB02_atau4 +2.8825 lebih tinggi, '
           'dan ASAS sendiri +0.9118.',
           'GB02_atau3 x X13 berpangkat 7 daripada 1,496 dalam grid penuh dan dikalahkan '
           'oleh DUA kaki tunggalnya sendiri - kesatuan MENCAIRKAN, bukan menambah.',
           'N19 x X13 jangkaan +11.2855% dan p 0.003576 LEBIH BAIK daripada konfigurasi '
           'yang dihantar ke produksi pada 1 Nov.'],
    bersih='Lapisan terjemahan kekal BERSIH: 22 lajur + 20 topeng bit-identik dengan '
           'kajian, tiada kebocoran masa hadapan, dan stop = NaN benar-benar bermakna '
           'tiada henti. Yang cacat ialah PENYEBUT statistik, bukan kodnya.',
    ganti='Digantikan 2 Nov 2026 oleh grid penuh 1,495 sel dengan penyebut jujur '
          'm = 1,495 (REVERSE/SPEC_GRID_PENUH.md, dikomit sebelum larian). Kajian ruang '
          'MASUK tidak memberi sokongan bertahan-FDR kepada MANA-MANA konfigurasi apabila '
          'penyebut merangkumi carian yang menghasilkannya, jadi 94 kombinasi produksi '
          'ialah UJIAN PERTAMA yang jujur - bukan pengesahan kelebihan yang sudah diukur.',
)

METRIK_N = {
    'A': ['lift latih', 'lift tahan', 'jangkaan'],
    'B': ['lift latih', 'lift tahan', 'jangkaan'],
    'GAB': ['lift latih', 'lift tahan', 'jangkaan'],
    'SX': ['lift latih', 'lift tahan', 'jangkaan'],
    'PORT': ['CAGR latih', 'CAGR tahan', 'MDD'],
    'CARA': ['jangkaan/sig latih', 'jangkaan/sig tahan', 'kadar isi %'],
}


def _ujian_n(A, B, G, X, PO, CA, ff, ii, bl):
    """Satu baris bagi SETIAP ujian dipradaftar merentas enam larian.

    Unit BERBEZA antara pradaftar (lift mata lawan CAGR % lawan jangkaan %/signal), jadi
    setiap baris membawa nama metriknya sendiri dan papan memaparkannya dalam sel. Menyusun
    merentas kumpulan pada lajur nilai membandingkan unit berlainan — papan memberi amaran
    dan menyediakan penapis kumpulan.
    """
    def gt(*pasangan):
        return ' '.join(f'{k}{"Y" if v else "N"}' for k, v in pasangan if v is not None)

    U = []
    for r in A:
        m = r.get('masuk', '')
        U.append(dict(pra='A', masuk=m, cara='C01',
                      keluar=r.get('keluar'), urutan=None, slot=None,
                      n=ii(r.get('n_tahan')), m1=ff(r.get('lift_latih')), m2=ff(r.get('lift_tahan')), m3=ff(r.get('jangkaan_tahan')),
                      menang=ff(r.get('menang'), 1), tanpa5=ff(r.get('tanpa5_tahan')),
                      p=ff(r.get('p'), 6),
                      gate=gt(('1', bl(r.get('gate1'))), ('2', bl(r.get('gate2'))),
                              ('3', bl(r.get('gate3')))),
                      lulus=bl(r.get('gate3')), ref=1 if 'semak' in m else 0,
                      nota='semak pemalsuan' if 'semak' in m else ''))
    for r in B:
        asas = r.get('masuk') == 'ASAS'
        U.append(dict(pra='B', masuk=r.get('masuk'), cara='C01', keluar=r.get('keluar'),
                      urutan=None, slot=None, n=ii(r.get('n_tahan')), m1=ff(r.get('lift_latih')), m2=ff(r.get('lift_tahan')), m3=ff(r.get('jangkaan_tahan')),
                      menang=ff(r.get('menang'), 1), tanpa5=ff(r.get('tanpa5_tahan')),
                      p=ff(r.get('p'), 6),
                      gate=gt(('0', bl(r.get('gate0'))), ('1', bl(r.get('gate1'))),
                              ('2', bl(r.get('gate2'))), ('3', bl(r.get('gate3')))),
                      lulus=bl(r.get('gate3')), ref=0,
                      nota='asas tanpa penapis masuk' if asas else r.get('peraturan', '')))
    for r in G:
        asas = r.get('konfig') == 'ASAS'
        U.append(dict(pra='GAB', k=r.get('konfig'), masuk=r.get('konfig'), cara='C01',
                      keluar='X3', urutan=None, slot=None, n=ii(r.get('n_tahan')), m1=ff(r.get('lift_latih')), m2=ff(r.get('lift_tahan')), m3=ff(r.get('jangkaan_tahan')),
                      menang=ff(r.get('menang'), 1), tanpa5=ff(r.get('tanpa5_tahan')),
                      p=ff(r.get('p'), 6),
                      gate=gt(('0', bl(r.get('gate0'))), ('1', bl(r.get('gate1'))),
                              ('2', bl(r.get('gate2'))), ('3', bl(r.get('gate3')))),
                      lulus=bl(r.get('gate3')), ref=1 if asas else 0,
                      nota='asas' if asas else ''))
    for r in X:
        asas = r.get('masuk') == 'ASAS'
        U.append(dict(pra='SX', masuk=r.get('masuk'), cara='C01', keluar=r.get('keluar'),
                      urutan=None, slot=None, n=ii(r.get('n_tahan')), m1=ff(r.get('lift_latih')), m2=ff(r.get('lift_tahan')), m3=ff(r.get('jangkaan_tahan')),
                      menang=ff(r.get('menang'), 1), tanpa5=ff(r.get('tanpa5')),
                      p=ff(r.get('p'), 6),
                      gate=gt(('0', bl(r.get('gate0'))), ('1', bl(r.get('gate1'))),
                              ('2', bl(r.get('gate2'))), ('3', bl(r.get('gate3')))),
                      lulus=bl(r.get('gate3')), ref=1 if asas else 0,
                      nota='asas' if asas else ''))
    for r in PO:
        kaw = r.get('masuk') == 'RAWAK'
        U.append(dict(pra='PORT',
                      masuk=r.get('masuk'), cara='C01', keluar=r.get('keluar'),
                      urutan=r.get('urutan'), slot=ii(r.get('slot')),
                      n=ii(r.get('n')), m1=ff(r.get('cagr_latih')), m2=ff(r.get('cagr')), m3=ff(r.get('mdd')),
                      menang=None, tanpa5=None, p=None,
                      gate=gt(('P1', bl(r.get('P1'))), ('P2', bl(r.get('P2'))),
                              ('P3', bl(r.get('P3'))), ('P4', bl(r.get('P4')))),
                      lulus=bl(r.get('lulus')),
                      nota=('kawalan tanpa isyarat · ' if kaw else '')
                           + f'nisbah {ff(r.get("nisbah"), 2)} · dedah '
                             f'{ff(r.get("dedah"), 0)}% · {ii(r.get("nb"))} benih'))
    # CARA: 6 cara x 2 tingkap dalam CSV -> SATU baris setiap cara, supaya latih dan tahan
    # duduk dalam lajur yang sama seperti setiap pradaftar lain (m1 = latih, m2 = tahan).
    lt = {r.get('cara'): r for r in CA if r.get('tingkap') == 'latih'}
    for r in CA:
        if r.get('tingkap') != 'tahan':
            continue
        c = r.get('cara')
        L = lt.get(c, {})
        h0 = ii(r.get('henti_hari0'))
        U.append(dict(pra='CARA', masuk='GB02_atau3', cara=c, keluar='X13',
                      urutan=None, slot=None, n=ii(r.get('n_isyarat')), m1=ff(L.get('jangkaan_sig')), m2=ff(r.get('jangkaan_sig')), m3=ff(r.get('kadar_isi'), 1),
                      menang=ff(r.get('menang'), 1), tanpa5=ff(r.get('tanpa5')),
                      p=ff(r.get('p'), 6),
                      gate=gt(('1', bl(r.get('CARA1'))), ('2', bl(r.get('CARA2'))),
                              ('3', bl(r.get('CARA3')))),
                      lulus=bl(r.get('CARA1')) and bl(r.get('CARA2')) and bl(r.get('CARA3')),
                      nota=f'jangkaan/isi {ff(r.get("jangkaan_isi"))}%'
                           + (f' · henti hari-0 {h0:,}' if h0 else '')))
    for r in U:
        if not r.get('ref'):
            r.pop('ref', None)   # baris ujian = kebanyakan; jangan bayar bait untuk ref=0
    _pangkat_n(U)
    return U


# Metrik yang menentukan pangkat dalam setiap pradaftar, sebagai indeks ke dalam METRIK_N:
# "jangkaan tahan" bagi pradaftar setiap-dagangan, "CAGR tahan" bagi portfolio. Pangkat
# dikira DALAM kumpulan sendiri sahaja — 2 mata lift dan 9% CAGR bukan unit yang sama.
PANGKAT_N = {'A': 2, 'B': 2, 'GAB': 2, 'SX': 2, 'PORT': 1, 'CARA': 1}


def _pangkat_n(U):
    """Tulis `pangkat` (1 = terbaik) dalam setiap kumpulan pradaftar.

    Baris rujukan (`ref`: asas tanpa penapis, semakan pemalsuan) tidak diberi pangkat —
    ia bukan ujian dipradaftar, jadi memangkatkannya akan mengubah penyebut "3 / 280".
    """
    for pra, i in PANGKAT_N.items():
        g = [r for r in U if r['pra'] == pra and not r.get('ref')]
        kk = ('m1', 'm2', 'm3')[i]
        g.sort(key=lambda r: (r[kk] is None, -(r[kk] or 0.0)))
        for n_, r in enumerate(g, 1):
            r['pangkat'] = n_


def _skor_n(U):
    """Kad skor: kadar lulus setiap pradaftar, dikira daripada senarai ujian YANG SAMA.

    Sengaja diterbitkan daripada `U` dan bukan ditulis tangan: peratus pada kad tidak boleh
    menyimpang daripada baris yang jadual tunjukkan. Baris rujukan dibuang daripada penyebut.
    """
    NAMA = {'A': 'A · ruang MASUK', 'B': 'B · ruang KELUAR', 'GAB': 'Paksi GABUNGAN',
            'SX': 'Silang akhir', 'PORT': 'Portfolio lawan SPUS', 'CARA': 'Paksi CARA'}
    corong, n_uji, n_lulus = [], 0, 0
    for pra in ('A', 'B', 'GAB', 'SX', 'PORT', 'CARA'):
        g = [r for r in U if r['pra'] == pra and not r.get('ref')]
        if not g:
            continue
        tok = []
        for r in g:
            for t in (r.get('gate') or '').split():
                if t[:-1] not in tok:
                    tok.append(t[:-1])
        lulus = sum(1 for r in g if r['lulus'])
        n_uji += len(g); n_lulus += lulus
        corong.append(dict(pra=pra, nama=NAMA[pra], ujian=len(g), lulus=lulus,
                           tahap=[dict(g=k, n=sum(1 for r in g
                                                  if f'{k}Y' in (r.get('gate') or '').split()))
                                  for k in tok],
                           metrik=METRIK_N[pra][PANGKAT_N[pra]]))
    return dict(
        ujian=n_uji, lulus=n_lulus,
        peratus=round(100.0 * n_lulus / n_uji, 2) if n_uji else None,
        corong=corong,
        # "Terbaik" bermaksud terbaik SETIAP DAGANGAN. Nombor portfolio diletak bersebelahan
        # dengan sengaja: ia pradaftar yang sama, dan tanpa lajur itu kad ini akan menipu.
        terbaik=dict(
            k='GB02_atau3 × X13',
            aturan='Masuk: N19 ∪ N37 ∪ N115 (kesatuan ATAU, bukan penapis DAN). '
                   'Keluar: rsi14 > 70 → jual buka esok. Cara: C01 beli pada buka esok.',
            dagangan=8.541, menang=64.2, n=195681, tanpa5=2.858,
            slot=8, cagr=9.40, mdd=-44.82, nisbah=0.21,
            slot2=40, cagr2=13.92, mdd2=-38.38, nisbah2=0.36,
            spus_cagr=17.95, spus_mdd=-26.82, spus_nisbah=0.669,
            verdikt='Lulus KESEMUA gate setiap-dagangan (gate0–gate3) — satu daripada dua '
                    'sahaja dalam 413 ujian yang pernah melepasi gate3 pada paksi GABUNGAN. '
                    'GAGAL sebagai portfolio: 0 daripada 36 konfigurasi melepasi keempat-empat '
                    'gate portfolio, dan CAGR 9.40% berada 8.6 mata di bawah SPUS dengan MDD '
                    '18 mata lebih dalam.',
            sebab='Jurangnya diukur, bukan ditafsir: tempoh pegang 84.9 bar (≈3 pusingan slot '
                  'setahun) dan kelebihan yang hidup dalam ekor — selepas membuang 5% dagangan '
                  'terbaik yang DIAMBIL, purata jatuh kepada +1.558% setiap 4 bulan. Tiada bias '
                  'pemilihan: dagangan yang diambil memberi +8.015% lawan populasi +8.541%.',
            syarat='BERSYARAT: kolam 12 signal GB02 dan keluar X13/X15 dipilih daripada data '
                   'yang SAMA, jadi tiada tingkap bebas tinggal. Alam A02 tiada saham delist '
                   '(setiap CAGR condong ke atas).'))


# ---------------------------------------------------------------- utama
# Dokumen yang dipecah dengan bahagi_db.bahagi() kerana ia melebihi had dokumen db.
# NAMA PENUH `koleksi/doc_id`, BUKAN doc_id. Sebelum 2 Nov 2026 padanan dibuat atas
# `nama.split('/')[1]` sahaja, dan itu pepijat yang menunggu: doc_id `papan` dikongsi oleh
# `analisis/papan` DAN `kaedah_n/papan`. Memecah atas doc_id akan memecah kedua-duanya,
# sedangkan dashboard membaca `kaedah_n/papan` dengan sub() biasa — jadi tab Kombinasi N
# akan kehilangan baris secara SENYAP (KPI "Baris registry 200" sebelah teks "263 baris").
# Setiap nama di sini MESTI dibaca dengan subBhg() dalam dashboard_v2.html.
# SEMBILAN nama pertama ialah terjemahan satu-ke-satu tuple doc_id yang lama; `prestasi/mae`
# dengan SENGAJA TIADA di sini walaupun dashboard membacanya dengan subBhg(), kerana
# `mae.rows` ialah OBJEK (peta kunci->nilai), bukan senarai, jadi bahagi() menolaknya.
PECAH = frozenset((
    'papertrade/senarai_beli', 'papertrade/watchlist', 'prestasi/garis', 'prestasi/mfe',
    'prestasi/mae_atr', 'prestasi/harian_kaedah', 'harian/trend',
    'harian/stage', 'posisi/lorong2',
    # 2 Nov 2026: 274,573 bait pada 228 kaedah (134 Mxx + 94 kombinasi Nxx) = 12,429
    # melebihi HAD_DB. Tanpa pemecahan, jana_db.py SystemExit pada langkah 4 tolak_db.md.
    'analisis/papan',
))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--keluar', required=True); ap.add_argument('--folder', default=PT); ap.add_argument('--stor', default=STOR)
    ap.add_argument('--versi', help='JSON {"koleksi/doc": versi} bagi if_version'); ap.add_argument('--masa')
    a = ap.parse_args(argv)
    masa = (pd.Timestamp(a.masa).tz_localize('Asia/Kuala_Lumpur') if a.masa else pd.Timestamp.now(tz='Asia/Kuala_Lumpur'))
    dibina = masa.strftime('%Y-%m-%d %H:%M') + ' MYT'
    st = json.load(open(os.path.join(a.folder, 'status_harian.json'), encoding='utf-8')) if os.path.exists(os.path.join(a.folder, 'status_harian.json')) else {}
    malam = st.get('malam', {}); beli = st.get('beli', {}); S = malam.get('sesi', '') or sesi_stor()
    harga_pada = f"{S} tutup (bar harian yfinance muktamad; GitHub Actions)" if S else ''
    nota_pos = (f"Dikemas kini oleh GitHub Actions (standard/harian_c.py) {malam.get('masa', '')}: harga tutup {S}; keluar dinilai dengan "
                'enjin rasmi; harga beli sementara dibetulkan kepada buka rasmi bar harian; baris keluar dibekukan; "menunggu" = '
                'isyarat keluar pada tutup terakhir, harga keluar = buka sesi seterusnya.')
    docs = {}
    M = baca_csv(os.path.join(a.folder, 'moomoo.csv'))
    docs['papertrade/moomoo'] = dict(akaun='4135388', dibina=dibina, harga_pada=harga_pada, nota=nota_pos, rows=[baris_db(r) for r in M])
    # dokumen lama (halaman v90+ membaca papertrade/ringkas_m; ini sandaran sahaja): gugurkan medan teks panjang jika melebihi
    # had satu dokumen (23 Okt 2026: medan audit yang diisi menjadikannya 270 KB)
    gugur = []
    for k in ('gred_pada', 'pemangkin_url', 'kewangan_ringkas', 'rs_tanda', 'pemangkin', 'sumber_earnings', 'nota'):
        if bait(docs['papertrade/moomoo']) < HAD_DB - 2000:
            break
        for x in docs['papertrade/moomoo']['rows']:
            x.pop(k, None)
        gugur.append(k)
    if gugur:
        docs['papertrade/moomoo']['medan_digugurkan'] = gugur
    C = []
    fail_c = sorted(glob.glob(os.path.join(a.folder, 'claude*.csv')), key=nombor_fail)
    for p in fail_c:
        R = baca_csv(p); C += R
        n = nombor_fail(p)
        docs[f"papertrade/{'claude' if n == 1 else f'claude_{n}'}"] = dict(dibina=dibina, harga_pada=harga_pada, nota=nota_pos,
                                                                         rows=[baris_db(r) for r in R])
    # slot (panel Papertrade C) dan isyarat dibatalkan pada belian terakhir
    import importlib
    slot = {}
    for r in C:
        if not sah(r):
            continue
        x = slot.setdefault(r['kaedah'], dict(claude_jumlah=0, claude_terbuka=0, moomoo=0, moomoo_termasuk_warisan=0))
        x['claude_jumlah'] += 1
        x['claude_terbuka'] += not SH.benar(r.get('tutup_semua') if r.get('tutup_semua') else r.get('keluar'))
    for r in M:
        x = slot.setdefault(r['kaedah'], dict(claude_jumlah=0, claude_terbuka=0, moomoo=0, moomoo_termasuk_warisan=0))
        x['moomoo_termasuk_warisan'] += 1
        x['moomoo'] += r.get('sumber') == 'harian' and not SH.benar(r.get('keluar'))
    for k, x in slot.items():
        try:
            x['nama'] = importlib.import_module(f'kaedah.{k}').NAMA
        except Exception:
            x['nama'] = ''
    batal = [l.split(': ', 1)[0].split(' ')[::-1] + [l.split(': ', 1)[1]] for l in beli.get('langkau', []) if ': ' in l]
    if 'papertrade/claude' in docs:
        docs['papertrade/claude'].update(slot=dict(sorted(slot.items(), key=lambda kv: int(kv[0][1:]) if kv[0][1:].isdigit() else 9999)),
                                         batal=batal, nota_slot='claude_terbuka = posisi Papertrade C yang belum tutup kedua-dua lorong; '
                                         'moomoo = posisi Moomoo warisan (sumber harian) yang belum keluar.')
    # senarai beli: tidak ditolak ke db sejak 19 Okt 2026 (halaman tidak membacanya); kiraan untuk harian/status sahaja
    sb = baca_csv(os.path.join(a.folder, 'senarai_beli.csv'))
    lihat = {r['saham'] for r in sb}
    # watchlist (dibahagi bawah had saiz)
    import kalendar_earnings as KE
    KAL = KE.muat()   # tarikh earnings sebenar (earn_sebenar) bagi ringkas_c/m dan watchlist
    wl = baca_csv(os.path.join(a.folder, 'watchlist.csv'))
    docs['papertrade/watchlist'] = dict(
        definisi='Hampir Signal: semua syarat entry selain pencetus dipenuhi; pencetus dalam <=2% (pct_dipenuhi = 100 - jarak_pct, '
                 'maks 99.9). Maks 5 setiap kaedah. Terkeluar signal dibuang serta-merta (tugasan_v3 §3).',
        dibina=malam.get('masa', dibina), gred_pada=st.get('gred', {}).get('tarikh', ''), pemangkin_pada=st.get('gred', {}).get('tarikh', ''),
        tarikh_data=wl[0]['tarikh_data'] if wl else S, rows=[earn_sebenar(baris_db(r, PETA_WATCH), r, KAL) for r in wl])
    # prestasi
    mae = penurunan_maks(M, C, a.stor)
    docs['prestasi/mae'] = dict(rows=mae, dibina=dibina, harga_hingga=f'{S} tutup',
                                definisi='Penurunan maksimum % = (harga rendah terendah sejak hari beli hingga hari ini, atau sehingga keluar) ÷ harga beli − 1, maksimum 0. Bagi posisi keluar: rendah hari sebelum hari keluar dan harga keluar. Kunci: akaun|saham|kaedah|tarikh_beli (akaun M=Moomoo, C=Claude). ATR isyarat: prestasi/mae_atr.')
    # 23 Okt 2026: atr dipindah ke dokumen sendiri (dibahagi) kerana mae + atr melebihi had satu dokumen
    docs['prestasi/mae_atr'] = dict(rows=sorted([k, v] for k, v in atr_isyarat(M, C, a.stor).items()), dibina=dibina,
                                    harga_hingga=f'{S} tutup', definisi='ATR14 % pada hari isyarat (bar terakhir sebelum hari beli). '
                                    'rows: [akaun|saham|kaedah|tarikh_beli, %].')
    docs['prestasi/ringkasan'] = dict(prestasi(M, C, mae), dibina=dibina, harga_pada=f'{S} tutup',
                                      nota='Dikira oleh standard/jana_db.py (GitHub Actions + sesi tolak db) dengan peraturan skor & keputusan P4 (sama seperti halaman).')
    # papertrade/ringkas_c, ringkas_m: semua baris dalam bentuk padat (halaman v90 membaca ini sahaja, bukan claude*)
    pra = {}
    dc = docs.get('papertrade/claude', {})
    for kod, R, meta in (('c', [earn_sebenar(baris_db(r), r, KAL) for r in C], {k: dc[k] for k in ('dibina', 'harga_pada', 'nota', 'slot', 'batal') if k in dc}),
                         ('m', [earn_sebenar(baris_db(r), r, KAL) for r in M], {k: v for k, v in docs['papertrade/moomoo'].items() if k not in ('rows', 'medan_digugurkan')})):
        for doc_id, d in ringkas_pt(R, f'ringkas_{kod}', meta):
            pra[f'papertrade/{doc_id}'] = d
    garis, mfe = garis_harga(M, C, a.stor)
    docs['prestasi/garis'] = dict(garis, dibina=dibina, harga_hingga=f'{S} tutup',
                                  definisi='rows: {s: saham, c: tutup sejajar dengan tarikh (null = tiada bar)} bagi saham yang masih ada '
                                           'posisi terbuka; spy: [tarikh, buka, tutup] sejak belian terawal.')
    docs['prestasi/mfe'] = dict(rows=mfe, dibina=dibina, harga_hingga=f'{S} tutup',
                                definisi='Kenaikan maksimum % (MFE) = (harga tinggi tertinggi sejak hari beli hingga hari ini, atau sehingga '
                                         'sehari sebelum keluar lorong kaedah, dan harga keluar) ÷ harga beli − 1, minimum 0. '
                                         'rows: [akaun|saham|kaedah|tarikh_beli, %].')
    docs['prestasi/harian_kaedah'] = dict(harian_kaedah(M, C, a.stor, TERKINI if a.stor == STOR else None), dibina=dibina, harga_hingga=f'{S} tutup',
                                          definisi='rows: {a: akaun M|C|G, k: kaedah, np: jumlah posisi, j: untung purata %, d: untung '
                                                   'harian % sejajar tarikh (null = tiada posisi), n: posisi dipegang, ev: [[indeks hari, beli, keluar untung, '
                                                   'keluar rugi]]}; k Semua = semua kaedah; spy: untung harian % SPY. Untung harian = '
                                                   'Σ perubahan nilai ÷ Σ nilai awal hari (posisi USD sama; keluar ikut lorong kaedah).')
    # harian/trend (pill Trend D10+H2, ATR14% + kuintil, rejim SPY), harian/stage (lajur Stage Analysis mingguan) dan
    # posisi/lorong2 (candlestick + paras lorong 2 setiap saham|tarikh_beli); kegagalan di sini tidak menghalang dokumen lain
    try:
        import trend_status as TS, lorong2_siri as L2, stage as ST
        tk = TERKINI if a.stor == STOR else None
        H, nota_h = TS.muat_harga(a.stor, tk, lajur=('date', 'open', 'high', 'low', 'close', 'volume'))
        I, _ = TS.muat_harga(a.stor, tk, fail=('harga_idx.csv',))
        lama = json.load(open(TS.FAIL, encoding='utf-8')) if a.stor == STOR and os.path.exists(TS.FAIL) else None
        docs['harian/trend'] = dict(TS.bawa_semalam(TS.dokumen(H, TS.alam(a.folder, H), nota_h, I), lama), dibina=dibina)
        docs['posisi/lorong2'] = dict(L2.dokumen(H, a.folder), dibina=dibina, harga_hingga=f'{S} tutup')
        docs['harian/stage'] = dict(ST.dokumen(H, TS.alam(a.folder, H), I), dibina=dibina)
    except Exception as e:  # noqa: BLE001
        print(f'amaran: harian/trend / harian/stage / posisi/lorong2 gagal: {e!r}', file=sys.stderr)
    ps = portfolio_slot(dibina)
    if ps:
        docs['prestasi/portfolio_slot'] = ps
    # analisis/papan: Papan Penganalisis (standard/penganalisis.py, Actions analisis.yml selepas Lejar Penuh) untuk tab Analisis
    pa = os.path.join(BS2, 'data', 'analisis', 'papan.json')
    if os.path.exists(pa):
        docs['analisis/papan'] = json.load(open(pa, encoding='utf-8'))
    # sektor/snapshot (dijana mingguan; medan posisi dikemas kini jika fail ada)
    snap = os.path.join(BS2, 'data', 'db', 'sektor_snapshot.json')
    if os.path.exists(snap):
        docs['sektor/snapshot'] = json.load(open(snap, encoding='utf-8'))
    # harian/status: kesegaran data (halaman: kemaskini_pagi, harga_tutup_pada, tarikh_data_pagi; header "Kemas kini terakhir")
    rk = malam
    docs['harian/status'] = dict(
        dikemaskini=dibina, sumber='GitHub Actions (standard/harian_c.py) + sesi Claude tolak db', harga_tutup_pada=S, tarikh_data_pagi=S,
        kemaskini_pagi=rk.get('masa', ''), tarikh_data=S, scan_malam=rk.get('masa', ''),
        kemaskini_pagi_ringkas=dict(C_keluar_baru=(rk.get('keluar_baru_jumlah') or {}).get('C', 0),
                                    M_keluar_baru=(rk.get('keluar_baru_jumlah') or {}).get('M', 0), menunggu_buka=rk.get('menunggu', 0),
                                    tidak_dibeli_baru=len(rk.get('tidak_dibeli') or []), watchlist_dibuang=rk.get('watchlist_dibuang', 0)),
        senarai_beli=dict(claude=len(sb), jumlah=len(sb), moomoo=0, saham_unik=len(lihat), watchlist=len(wl)),
        beli_dirancang=len(sb), beli_pada=beli.get('masa', ''), beli_ringkas=dict(direkod=beli.get('direkod', 0), dilangkau=beli.get('dilangkau', 0)),
        gred_pada=st.get('gred', {}).get('masa', ''), ralat=(rk.get('ralat_kaedah') or [])[:20])
    kn = kaedah_n(dibina)
    if kn:
        docs['kaedah_n/papan'] = kn
    # tulis + bahagi + batch
    os.makedirs(a.keluar, exist_ok=True)
    versi = json.load(open(a.versi)) if a.versi else {}
    tulis = []
    semua = [(nama.split('/')[0], bahagi(d, nama.split('/')[1], 200000) if nama in PECAH
              else [(nama.split('/')[1], d)]) for nama, d in docs.items()]
    semua += [(nama.split('/')[0], [(nama.split('/')[1], d)]) for nama, d in pra.items()]   # sudah dibahagi (ringkas_pt)
    for kol, bahagian in semua:
        # `kump_id` = kumpulan keatoman: satu bagi setiap operasi bahagi(), supaya SEMUA
        # bahagiannya ditolak dalam satu panggilan. Ia datang daripada operasi pecahan itu
        # sendiri, BUKAN daripada bentuk nama: `papertrade/claude_7` nampak seperti bahagian
        # tetapi ialah dokumen BEBAS daripada pecah_claude.py, dan mengumpulkannya dengan
        # `claude` memaksa 13.6 MB ke satu batch (diuji; ia gagal).
        kump_id = f'{kol}/{bahagian[0][0]}' if len(bahagian) > 1 else None
        for doc_id, dd in bahagian:
            sz = bait(dd)
            if sz >= HAD_DB:
                raise SystemExit(f'{kol}/{doc_id}: {sz} bait melebihi had db {HAD_DB} (jalankan pecah_claude.py --pecah)')
            p = os.path.join(a.keluar, kol, doc_id + '.json'); os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, 'w', encoding='utf-8').write(padat(dd))
            w = dict(op='set', collection=kol, doc_id=doc_id, file_path=os.path.abspath(p))
            v = versi.get(f'{kol}/{doc_id}')
            if v:
                w['if_version'] = int(v)
            tulis.append((w, sz, kump_id or f'{kol}/{doc_id}'))
    # Pembatchan SEDAR-BAHAGIAN. bahagi_db.py mewajibkan semua bahagian satu dokumen
    # ditolak dalam SATU batch, tetapi tolak_db.md langkah 5 membuat satu panggilan
    # ArtifactData bagi SETIAP batch_N.json — jadi bahagian yang jatuh ke fail berbeza
    # ditolak dalam panggilan berbeza, dan antara keduanya halaman melihat dokumen asas
    # yang mengisytiharkan n bahagian sementara bahagian itu belum ada. Kumpulan ialah
    # dokumen asas + semua bahagiannya; ia tidak boleh dipecahkan merentas batch.
    kump, idx = [], {}
    for w, sz, k in tulis:
        if k not in idx:
            idx[k] = len(kump); kump.append([])
        kump[idx[k]].append((w, sz))
    # Satu kumpulan disimpan utuh apabila ia MUAT dalam satu batch. Apabila ia tidak muat
    # (posisi/lorong2 ialah 3.1 MB merentas bahagian, lawan had batch 900 KB), ia dipecahkan
    # seperti dahulu dan DIREKOD dalam ringkas.json, bukan menyebabkan SystemExit: keadaan
    # itu sudah berlaku setiap malam sebelum perubahan ini dan tiada apa yang rosak. Yang
    # membuatnya selamat ialah pengawal kelengkapan dalam subBhg (dashboard_v2.html):
    # halaman tidak merender sehingga setiap bahagian dengan `induk` sepadan tiba, jadi
    # tingkap antara dua panggilan tolakan memapar "Memuatkan…", bukan jadual separa.
    batches, cur, size, terpecah = [], [], 0, []
    for g in kump:
        gs = sum(sz for _, sz in g)
        if gs > HAD_BATCH and len(g) > 1:
            terpecah.append(f'{g[0][0]["collection"]}/{g[0][0]["doc_id"]} ({len(g)} bahagian, {gs} bait)')
        if cur and (size + gs > HAD_BATCH or len(cur) + len(g) > 50):
            batches.append(cur); cur, size = [], 0
        for w, sz in g:
            if cur and (size + sz > HAD_BATCH or len(cur) >= 50):
                batches.append(cur); cur, size = [], 0
            cur.append(w); size += sz
    if cur:
        batches.append(cur)
    fail = []
    for i, bt in enumerate(batches):
        p = os.path.join(a.keluar, f'batch_{i}.json'); json.dump(bt, open(p, 'w'), indent=1); fail.append(p)
    ring = dict(dibina=dibina, sesi=S, dokumen=len(tulis), batch=fail, kumpulan_terpecah=terpecah, tanpa_versi=[f"{w['collection']}/{w['doc_id']}" for w, _, _ in tulis if 'if_version' not in w],
                pengawas=pengawas(st, masa))
    json.dump(ring, open(os.path.join(a.keluar, 'ringkas.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(ring, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
