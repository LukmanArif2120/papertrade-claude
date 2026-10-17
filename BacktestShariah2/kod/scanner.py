"""Scan harian Papertrade Shariah — 87 kaedah M.

Subarahan:
  python3 scanner.py harga  --skrin F1 F2 ... [--kline peta.tsv] [--idx SPY=fail QQQ=fail]
  python3 scanner.py scan   --mod malam|tutup --db DIR_DB --out DIR_OUT
  python3 scanner.py rekod  --db DIR_DB --isian isian.json --out DIR_OUT
Data stor: data/harga_A.csv, data/harga_B.csv, data/harga_idx.csv, data/univ.csv
"""
import sys, os, json, argparse, importlib, glob, time, traceback, copy
import pandas as pd, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from stor import *

MAKS_SLOT = 10          # had saham setiap kaedah (arahan pengguna)
MAKS_WATCH = 5          # had saham 'hampir' setiap kaedah
PENUH_SEHARI = 5      # isyarat slot penuh baharu direkod setiap kaedah sehari (ikut kedudukan rank)
PENUH_MAKS = 50       # simpan 50 terkini
TAMAT_WATCH = 10        # hari dagangan sebelum 'hampir' tanpa isyarat dibuang
HARGA_MIN = 10.0        # harga > USD10
FLOAT_MIN = 1e6         # float market cap > USD1 juta
DATA = os.path.join(HERE, 'data')
BERGANTUNG = {'M02','M18','M19','M24','M40','M45','M47','M56','M76','M78','M81','M82','M94','M96','M100'}  # keluar bergantung jujukan dagangan


def kal():
    import exchange_calendars as xc
    return xc.get_calendar('XNYS')


def sesi_terakhir_siap(now=None):
    """Tarikh sesi NYSE terakhir yang sudah tutup (YYYYMMDD)."""
    c = kal(); now = now or pd.Timestamp.now(tz='America/New_York')
    d = now.normalize().tz_localize(None)
    if c.is_session(d) and now.hour * 60 + now.minute >= 16 * 60 + 20:
        return int(d.strftime('%Y%m%d'))
    return int(c.previous_session(d).strftime('%Y%m%d')) if c.is_session(d) else int(c.date_to_session(d, direction='previous').strftime('%Y%m%d'))


def senarai_kaedah():
    out = []
    for f in glob.glob(os.path.join(HERE, 'kaedah', 'M*.py')):
        out.append(os.path.basename(f)[:-3])
    return sorted(out, key=lambda x: int(x[1:]))


def s431():
    return set(pd.read_csv(os.path.join(DATA, 'harga_A.csv'), usecols=['ticker']).ticker)


# ---------------------------------------------------------------- harga
def cmd_harga(a):
    from parse_screen import parse
    fr = muat(DATA)
    tarikh = a.tarikh or sesi_terakhir_siap()
    rows = []
    for f in a.skrin or []:
        o, _ = parse(f); rows += o
    nota = []
    if rows:
        u = pd.DataFrame(rows).drop_duplicates('ticker')
        u.to_csv(os.path.join(DATA, 'univ.csv'), index=False)
        A = set(fr['harga_A.csv'].ticker)
        for nm, sel in [('harga_A.csv', u[u.ticker.isin(A)]), ('harga_B.csv', u[~u.ticker.isin(A)])]:
            d = fr[nm]
            akhir = d.groupby('ticker').date.max()
            ok = sel[sel.ticker.isin(akhir.index)].copy()
            # hanya tambah jika bar sebelumnya ialah sesi sebelum 'tarikh' (tiada jurang)
            c = kal(); prev = int(c.previous_session(pd.Timestamp(str(tarikh))).strftime('%Y%m%d'))
            ok['akhir'] = ok.ticker.map(akhir)
            jur = ok[(ok.akhir < prev)]
            ok = ok[ok.akhir >= prev]
            ok = ok.dropna(subset=['open', 'high', 'low', 'close'])
            baru = pd.DataFrame({'ticker': ok.ticker, 'date': tarikh, 'open': ok.open, 'high': ok.high, 'low': ok.low,
                                 'close': ok.close, 'volume': ok.volume.fillna(0)})
            fr[nm] = pd.concat([d[~((d.ticker.isin(baru.ticker)) & (d.date == tarikh))], baru], ignore_index=True)
            if len(jur): nota.append(f'{nm}: {len(jur)} saham ada jurang data (perlu kline)')
        perlu = sorted(set(u.ticker) - set(fr['harga_A.csv'].ticker) - set(fr['harga_B.csv'].ticker))
        jurang = []
        for nm in ['harga_A.csv', 'harga_B.csv']:
            akhir = fr[nm].groupby('ticker').date.max()
            jurang += [t for t in akhir.index[akhir < tarikh] if t in set(u.ticker)]
        open(os.path.join(DATA, 'perlu_kline.txt'), 'w').write('\n'.join(perlu + sorted(set(jurang))))
        nota.append(f'saham baharu tanpa sejarah: {len(perlu)}; saham dengan jurang: {len(set(jurang))} (senarai dalam data/perlu_kline.txt)')
    for f in a.kline or []:
        for ln in open(f):
            p = ln.rstrip('\n').split('\t')
            if len(p) != 2 or not p[1].startswith('/'): continue
            t, path = p; kl = baca_kline(path)
            nm = 'harga_A.csv' if t in set(fr['harga_A.csv'].ticker) else 'harga_B.csv'
            fr[nm] = gabung_kline(fr[nm], t, kl)
    for spec in a.idx or []:
        t, path = spec.split('=', 1)
        fr['harga_idx.csv'] = gabung_kline(fr['harga_idx.csv'], t, baca_kline(path))
    simpan(DATA, fr)
    for nm, d in fr.items():
        nota.append(f'{nm}: {d.ticker.nunique()} saham, bar terakhir {int(d.date.max())}')
    print(json.dumps({'tarikh': tarikh, 'nota': nota}, ensure_ascii=False, indent=1))


# ---------------------------------------------------------------- belian semula
def terbuka(r):
    """Baris posisi/penuh db masih terbuka (belum keluar, atau keluar menunggu harga)."""
    k = r.get('keluar')
    return not k or bool(k.get('menunggu')) or k.get('harga') is None


def pegangan_c(folder):
    """papertrade/claude*.csv -> (set (kaedah, saham) masih terbuka, Counter (kaedah, saham) bilangan belian).
    Saham yang sudah keluar TIDAK dikecualikan: isyarat baharu = belian ke-2, ke-3 ...
    Sejak 17 Okt 2026 (dua lorong keluar, standard/keluar_lorong.py) posisi kekal terbuka sehingga kedua-dua lorong keluar
    (`tutup_semua` = True). Fail tanpa lajur tutup_semua: ikut `keluar` (lorong 1) seperti dahulu."""
    import csv
    from collections import Counter
    buka, bil = set(), Counter()
    for f in sorted(glob.glob(os.path.join(folder, 'claude*.csv'))):
        rd = csv.DictReader(open(f, newline='', encoding='utf-8'))
        tiga = 'tutup_semua' in (rd.fieldnames or [])
        for r in rd:
            if r.get('tidak_dibeli') == 'True' or not r.get('tarikh_beli'):
                continue
            k = (r.get('kaedah'), r.get('saham'))
            bil[k] += 1
            tutup = r.get('tutup_semua') == 'True' if tiga else r.get('keluar') == 'True'
            if not tutup and r.get('tidak_sah') != 'True':
                buka.add(k)
    return buka, bil


# ---------------------------------------------------------------- db helpers
def baca_db(dirdb):
    """Baca dokumen yang disimpan oleh ArtifactData (out_dir). Pulang dict path->data."""
    out = {}
    for f in glob.glob(os.path.join(dirdb, '**', '*.json'), recursive=True):
        parts = os.path.relpath(f, dirdb)[:-5].replace(os.sep, '/').split('/')
        try:
            d = json.load(open(f))
        except Exception:
            continue
        if len(parts) >= 2 and parts[-2] == 'kumpulan' and isinstance(d, dict):
            for mid, doc in (d.get('kaedah') or {}).items():
                out[f'kaedah/{mid}'] = doc
            continue
        rel = '/'.join(parts[-2:]) if len(parts) >= 2 else parts[0]
        out[rel] = d
    return out


def simpan_isyarat(rows, folder, tdata, mod):
    """Rekod kekal SEMUA isyarat 100% satu imbasan (bukan hanya yang dibeli) untuk analisis kemudian
    (cth. portfolio 8 slot ikut rank). Fail: <folder>/<tdata>_<mod>.csv.gz. Tidak mengubah logik isyarat/belian."""
    os.makedirs(folder, exist_ok=True)
    p = os.path.join(folder, f'{tdata}_{mod}.csv.gz')
    lajur = ['tarikh_data', 'kaedah', 'saham', 'rank', 'henti', 'sasaran', 'tutup', 'sumber', 'dirancang']
    pd.DataFrame(rows, columns=lajur).to_csv(p, index=False, compression={'method': 'gzip', 'mtime': 0})
    return p


def tulis(dirout, rel, data):
    p = os.path.join(dirout, rel + '.json'); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(data, open(p, 'w'), ensure_ascii=False, default=lambda x: None if (isinstance(x, float) and np.isnan(x)) else (x.item() if hasattr(x, 'item') else str(x)))


def bersih(x):
    if isinstance(x, (np.floating, float)):
        return None if np.isnan(x) else round(float(x), 4)
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.bool_,)): return bool(x)
    if isinstance(x, dict): return {k: bersih(v) for k, v in x.items()}
    if isinstance(x, list): return [bersih(v) for v in x]
    return x


def jangkaan():
    """Varian & jangkaan backtest setiap kaedah (daripada registry tempatan)."""
    out = {}
    for f in glob.glob(os.path.join(HERE, 'registry', 'M*.csv')):
        mid = os.path.basename(f)[:-4]
        try:
            m = importlib.import_module(f'kaedah.{mid}')
            r = pd.read_csv(f); r = r[(r['set'].astype(str) == '431') & (r.varian == m.VARIAN)]
            if len(r):
                r = r.iloc[0]
                out[mid] = {'keputusan': r.keputusan, 'avg': float(r.avg), 'win': float(r.win), 'days': float(r.days), 'cagr': float(r.cagr)}
        except Exception:
            pass
    return out


# ---------------------------------------------------------------- keluar ikut peraturan
def keluar_peraturan(g, t_isyarat, e):
    """Tiru gelung enjin.trades untuk satu dagangan. g sudah ada sig/stop/tgt/exitc. e = harga masuk."""
    ix = g.index
    try:
        i = ix.get_loc(pd.Timestamp(str(t_isyarat)))
    except KeyError:
        return None
    o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values
    st = g['stop'].astype(float).values; tg = g['tgt'].astype(float).values
    ex = g['exitc'].fillna(False).astype(bool).values
    n = len(g)
    sp = st[i] if not np.isnan(st[i]) else -np.inf
    j = i + 1
    while j < n:
        tgt = tg[j - 1] if j > i + 1 else np.nan
        if j > i + 1 and o[j] <= sp: return dict(tarikh=str(ix[j].date()), harga=float(o[j]), sebab='henti (buka bawah henti)')
        if l[j] <= sp: return dict(tarikh=str(ix[j].date()), harga=float(sp), sebab='henti')
        if not np.isnan(tgt):
            if j > i + 1 and o[j] >= tgt: return dict(tarikh=str(ix[j].date()), harga=float(o[j]), sebab='sasaran')
            if h[j] >= tgt: return dict(tarikh=str(ix[j].date()), harga=float(tgt), sebab='sasaran')
        if ex[j]:
            if j + 1 < n: return dict(tarikh=str(ix[j + 1].date()), harga=float(o[j + 1]), sebab='isyarat keluar')
            return dict(tarikh=None, harga=None, sebab='isyarat keluar — jual pada buka esok', menunggu=True)
        j += 1
    return None


def jejak(g, row, kunci_harga):
    """Kemas kini harga terkini, tertinggi/terendah dan keluar peraturan bagi satu baris posisi/penuh."""
    e = row.get(kunci_harga)
    ti = row.get('tarikh_isyarat')
    if e is None:  # harga masuk andaian = buka hari selepas isyarat
        try:
            i = g.index.get_loc(pd.Timestamp(str(ti)))
            if i + 1 < len(g):
                e = float(g.open.iloc[i + 1]); row[kunci_harga] = round(e, 4); row['tarikh_masuk'] = str(g.index[i + 1].date())
        except KeyError:
            pass
    if e is None:
        return row
    akhir = float(g.close.iloc[-1]); row['harga_terkini'] = round(akhir, 4); row['harga_pada'] = str(g.index[-1].date())
    row['untung_pct'] = round((akhir / e - 1) * 100, 2)
    tm = row.get('tarikh_masuk')
    if tm:
        s = g[g.index >= pd.Timestamp(tm)]
        if len(s):
            row['tertinggi_pct'] = round((s.high.max() / e - 1) * 100, 2)
            row['terendah_pct'] = round((s.low.min() / e - 1) * 100, 2)
            row['hari'] = int(len(s))
    if not row.get('keluar') or row['keluar'].get('menunggu'):
        k = keluar_peraturan(g, ti, e)
        if k:
            if k.get('harga') is not None:
                k['untung_pct'] = round((k['harga'] / e - 1) * 100, 2)
            row['keluar'] = k
    if row.get('keluar') and row['keluar'].get('untung_pct') is not None:
        row['beza_peraturan_pct'] = round(row['keluar']['untung_pct'] - row['untung_pct'], 2)
    return row


# ---------------------------------------------------------------- scan
def cmd_scan(a):
    t0 = time.time()
    fr0, idx = frames_dict(muat(DATA))
    univ = pd.read_csv(os.path.join(DATA, 'univ.csv')) if os.path.exists(os.path.join(DATA, 'univ.csv')) else None
    layak = set(univ[(univ.close >= HARGA_MIN) & (univ.floatcap > FLOAT_MIN)].ticker) if univ is not None else set(fr0)
    A = s431()
    db = baca_db(a.db) if a.db else {}
    jk = jangkaan()
    tarikh_data = max(g.index[-1] for g in fr0.values())
    tdata = str(tarikh_data.date())
    # saham yang sudah dipegang dalam akaun (semua kaedah + pegangan lama)
    dipegang = set(db.get('meta/akaun', {}).get('saham', []))
    for k, d in db.items():
        if k.startswith('kaedah/'):
            dipegang |= {p['saham'] for p in d.get('posisi', [])}
    buka_c, bil_c = pegangan_c(a.papertrade) if getattr(a, 'papertrade', None) else (set(), {})
    queue = []; ringkas = []; ralat = []; semua_isyarat = []
    kaedah = senarai_kaedah() if not a.hanya else a.hanya.split(',')
    fr_ok = {t: g for t, g in fr0.items() if len(g) >= 60}
    for mid in kaedah:
        tm = time.time()
        try:
            m = importlib.import_module(f'kaedah.{mid}')
        except Exception as e:
            ralat.append(f'{mid}: import gagal {e}'); continue
        doc = copy.deepcopy(db.get(f'kaedah/{mid}', {}))
        doc.setdefault('posisi', []); doc.setdefault('watch', []); doc.setdefault('penuh', [])
        perlu = getattr(m, 'PERLU_BAR', 260)
        fr = {t: g.copy() for t, g in fr_ok.items() if (len(g) >= perlu or m.SILANG)}
        try:
            m.sedia(fr, idx)
        except Exception as e:
            ralat.append(f'{mid}: sedia gagal {type(e).__name__}: {e}'); continue
        # isyarat bar akhir
        sig = []
        for t, g in fr.items():
            if g.index[-1] != tarikh_data or t not in layak: continue
            try:
                if bool(g['sig'].iloc[-1]):
                    sig.append(dict(saham=t, rank=bersih(float(g['rank'].iloc[-1])) if 'rank' in g else None,
                                    henti=bersih(float(g['stop'].iloc[-1])), sasaran=bersih(float(g['tgt'].iloc[-1])),
                                    tutup=round(float(g.close.iloc[-1]), 4), sumber='431' if t in A else 'lain'))
            except Exception:
                pass
        sig.sort(key=lambda x: (x['sumber'] != '431', -(x['rank'] if x['rank'] is not None else -1e9)))
        tulis(a.out, f'semua_sig/{mid}', bersih(sig))
        semua_isyarat += [dict(tarikh_data=tdata, kaedah=mid, **{k: x[k] for k in ('saham', 'rank', 'henti', 'sasaran', 'tutup', 'sumber')})
                          for x in sig]
        # hanya posisi TERBUKA kaedah ini dikecualikan; saham yang sudah keluar layak dibeli semula (belian ke-2, ke-3 ...)
        ada = {p['saham'] for p in doc['posisi'] + doc['penuh'] if terbuka(p) and not getattr(a, 'papertrade', None)} \
            | {t for (k, t) in buka_c if k == mid}
        baru_penuh = 0
        baki = MAKS_SLOT - sum(1 for p in doc['posisi'] if terbuka(p))
        for s in sig:
            if s['saham'] in ada: continue
            s['belian_ke'] = bil_c.get((mid, s['saham']), 0) + 1
            if baki > 0 and a.mod in ('malam', 'tutup'):
                s.update(kaedah=mid, dikongsi=s['saham'] in dipegang, tarikh_isyarat=tdata)
                queue.append(s); baki -= 1; ada.add(s['saham']); dipegang.add(s['saham'])
            elif baru_penuh < PENUH_SEHARI:
                baru_penuh += 1
                doc['penuh'].append(dict(saham=s['saham'], sumber=s['sumber'], tarikh_isyarat=tdata, harga_isyarat=s['tutup'],
                                         henti=s['henti'], harga_masuk_andaian=None, belian_ke=s['belian_ke'],
                                         catatan='Isyarat beli sah tetapi slot kaedah penuh (10/10); dipantau seolah-olah dibeli pada buka esok'))
                ada.add(s['saham'])
        doc['penuh'] = doc['penuh'][-PENUH_MAKS:]
        # hampir -> watchlist
        calon = []
        for t, g in fr.items():
            if g.index[-1] != tarikh_data or t not in layak or t in ada: continue
            try:
                h = m.hampir(g, idx)
            except Exception:
                h = None
            if h:
                calon.append(dict(saham=t, sumber='431' if t in A else 'lain', sebab=str(h.get('sebab', '')),
                                  syarat_beli=str(h.get('syarat_beli', '')), skor=bersih(float(h.get('skor', 0) or 0)),
                                  harga_terkini=round(float(g.close.iloc[-1]), 4),
                                  pencetus=h.get('pencetus'), paras=bersih(h.get('paras')), jarak_pct=bersih(h.get('jarak_pct')),
                                  syarat_dipenuhi=h.get('syarat_dipenuhi')))
        calon.sort(key=lambda x: (x['sumber'] != '431', -(x['skor'] or 0)))
        lama = {w['saham']: w for w in doc['watch']}
        baru = []
        for c in calon:
            w = lama.get(c['saham'])
            if w:
                w.update(sebab=c['sebab'], syarat_beli=c['syarat_beli'], skor=c['skor'], harga_terkini=c['harga_terkini'], pencetus=c['pencetus'], paras=c['paras'], jarak_pct=c['jarak_pct'], syarat_dipenuhi=c['syarat_dipenuhi'])
                w['hari'] = w.get('hari', 0) + (1 if w.get('dikemaskini') != tdata else 0); w['dikemaskini'] = tdata
                baru.append(w)
        for c in calon:
            if len(baru) >= MAKS_WATCH: break
            if c['saham'] in {w['saham'] for w in baru}: continue
            c.update(ditambah=tdata, harga_ditambah=c['harga_terkini'], hari=0, dikemaskini=tdata); baru.append(c)
        for w in baru:
            if w.get('harga_ditambah'): w['ubah_pct'] = round((w['harga_terkini'] / w['harga_ditambah'] - 1) * 100, 2)
        doc['watch'] = [w for w in baru if w.get('hari', 0) <= TAMAT_WATCH][:MAKS_WATCH + 3]
        # jejak posisi & penuh
        for lst, kunci in [(doc['posisi'], 'harga_isian'), (doc['penuh'], 'harga_masuk_andaian')]:
            for r in lst:
                g = fr.get(r['saham'])
                if g is None or 'sig' not in g:
                    continue
                jejak(g, r, kunci)
        info = jk.get(mid, {})
        doc.update(id=mid, nama=m.NAMA, varian=m.VARIAN, keputusan=info.get('keputusan'), jangka_avg=info.get('avg'),
                   jangka_win=info.get('win'), jangka_hari=info.get('days'), bergantung=mid in BERGANTUNG,
                   isyarat_hari_ini=len(sig), kemaskini=pd.Timestamp.now(tz='Asia/Kuala_Lumpur').strftime('%Y-%m-%d %H:%M'),
                   tarikh_data=tdata)
        tulis(a.out, f'kaedah/{mid}', bersih(doc))
        ringkas.append((mid, len(sig), len(doc['posisi']), len(doc['penuh']), len(doc['watch']), round(time.time() - tm, 1)))
        print(mid, round(time.time() - tm, 1), file=sys.stderr, flush=True)
    for k, d in db.items():
        if k.startswith('meta/') and k != 'meta/beli': tulis(a.out, k, d)
    if getattr(a, 'papertrade', None):
        try:
            dir_ = {(q['kaedah'], q['saham']) for q in queue}
            for r in semua_isyarat: r['dirancang'] = (r['kaedah'], r['saham']) in dir_
            simpan_isyarat(semua_isyarat, os.path.join(a.papertrade, '..', 'data', 'isyarat'), tdata, a.mod)
        except Exception as e:
            ralat.append(f'simpan_isyarat gagal {type(e).__name__}: {e}')
    # baris gilir beli (unik saham untuk pesanan sebenar)
    tulis(a.out, 'meta/beli', bersih(dict(tarikh_data=tdata, dibina=pd.Timestamp.now(tz='Asia/Kuala_Lumpur').strftime('%Y-%m-%d %H:%M'),
                                  mod=a.mod, rows=queue)))
    st = json.load(open(a.status)) if a.status and os.path.exists(a.status) else {}
    st.update(tarikh_data=tdata, bil_univ=len(layak), bil_kaedah=len(ringkas))
    st[f'scan_{a.mod}'] = pd.Timestamp.now(tz='Asia/Kuala_Lumpur').strftime('%Y-%m-%d %H:%M')
    st['ralat'] = ralat[-20:]
    st['beli_dirancang'] = len(queue)
    tulis(a.out, 'status', bersih(st))
    print(json.dumps(dict(tarikh_data=tdata, beli_dirancang=len(queue), saham_unik=len({q['saham'] for q in queue}),
                          dikongsi=sum(q['dikongsi'] for q in queue), ralat=ralat, masa_s=round(time.time() - t0),
                          kaedah=[dict(id=x[0], isyarat=x[1], posisi=x[2], penuh=x[3], watch=x[4], s=x[5]) for x in ringkas]),
                     ensure_ascii=False))


# ---------------------------------------------------------------- rekod beli
def cmd_rekod(a):
    """isian.json: [{kaedah, saham, order_id, harga_isian, status('diisi'|'dikongsi'|'langkau'|'gagal'), catatan}]"""
    db = baca_db(a.db); isi = json.load(open(a.isian))
    beli = db.get('meta/beli', {}); qmap = {(q['kaedah'], q['saham']): q for q in beli.get('rows', [])}
    ubah = {}
    for r in isi:
        if r.get('status') not in ('diisi', 'dikongsi'): continue
        mid = r['kaedah']; doc = ubah.get(mid) or copy.deepcopy(db.get(f'kaedah/{mid}', {}))
        doc.setdefault('posisi', []); doc.setdefault('watch', []); doc.setdefault('penuh', [])
        if any(p['saham'] == r['saham'] for p in doc['posisi']): ubah[mid] = doc; continue
        if len(doc['posisi']) >= MAKS_SLOT: ubah[mid] = doc; continue
        q = qmap.get((mid, r['saham']), {})
        doc['posisi'].append(bersih(dict(saham=r['saham'], sumber=q.get('sumber'), tarikh_isyarat=q.get('tarikh_isyarat', beli.get('tarikh_data')),
                                         tarikh_masuk=r.get('tarikh_masuk'), harga_isian=r.get('harga_isian'), henti=q.get('henti'),
                                         sasaran=q.get('sasaran'), order_id=r.get('order_id'), dikongsi=r['status'] == 'dikongsi',
                                         unit=0 if r['status'] == 'dikongsi' else 1, catatan=r.get('catatan', ''))))
        doc['watch'] = [w for w in doc['watch'] if w['saham'] != r['saham']]
        ubah[mid] = doc
    # salin semua dokumen lama ke larian baharu, ganti yang berubah
    for k, d in db.items():
        if k.startswith('kaedah/') and k[7:] not in ubah: tulis(a.out, k, d)
        if k.startswith('meta/'): tulis(a.out, k, d)
    for mid, doc in ubah.items():
        tulis(a.out, f'kaedah/{mid}', bersih(doc))
    tulis(a.out, 'meta/beli', dict(tarikh_data=beli.get('tarikh_data'), rows=[], selesai=pd.Timestamp.now(tz='Asia/Kuala_Lumpur').strftime('%Y-%m-%d %H:%M')))
    st = json.load(open(a.status)) if a.status and os.path.exists(a.status) else {}; st['beli_pada'] = pd.Timestamp.now(tz='Asia/Kuala_Lumpur').strftime('%Y-%m-%d %H:%M')
    st['beli_ringkas'] = {s: sum(1 for r in isi if r.get('status') == s) for s in ['diisi', 'dikongsi', 'langkau', 'gagal']}
    tulis(a.out, 'status', bersih(st))
    print(json.dumps(dict(kaedah_dikemaskini=len(ubah), **st['beli_ringkas']), ensure_ascii=False))


def cmd_batch(a):
    """Bungkus dokumen kaedah ke kumpulan (6 kaedah) dan cetak fail 'writes' untuk ArtifactData batch (dokumen baharu, tanpa if_version)."""
    fs = sorted(glob.glob(os.path.join(a.out, 'kaedah', '*.json')), key=lambda x: int(os.path.basename(x)[1:-5]))
    os.makedirs(os.path.join(a.out, 'kumpulan'), exist_ok=True)
    w = []
    for i in range(0, len(fs), 6):
        pk = {'kaedah': {os.path.basename(f)[:-5]: json.load(open(f)) for f in fs[i:i + 6]}}
        p = os.path.join(a.out, 'kumpulan', f'k{i // 6:02d}.json'); json.dump(pk, open(p, 'w'), ensure_ascii=False)
        w.append({'op': 'set', 'collection': f'larian/{a.run}/kumpulan', 'doc_id': f'k{i // 6:02d}', 'file_path': os.path.abspath(p)})
    for f in sorted(glob.glob(os.path.join(a.out, 'meta', '*.json'))):
        w.append({'op': 'set', 'collection': f'larian/{a.run}/meta', 'doc_id': os.path.basename(f)[:-5], 'file_path': os.path.abspath(f)})
    batches, cur, size = [], [], 0
    for x in w:
        sz = os.path.getsize(x['file_path'])
        if cur and size + sz > 850_000: batches.append(cur); cur, size = [], 0
        cur.append(x); size += sz
    if cur: batches.append(cur)
    for i, bt in enumerate(batches):
        p = os.path.join(a.out, f'batch_{i}.json'); json.dump(bt, open(p, 'w'))
        print(p, len(bt), sum(os.path.getsize(x['file_path']) for x in bt))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); sp = p.add_subparsers(dest='cmd')
    h = sp.add_parser('harga'); h.add_argument('--skrin', nargs='*'); h.add_argument('--kline', nargs='*'); h.add_argument('--idx', nargs='*'); h.add_argument('--tarikh', type=int)
    s = sp.add_parser('scan'); s.add_argument('--mod', default='tutup'); s.add_argument('--db'); s.add_argument('--out', default='out'); s.add_argument('--hanya'); s.add_argument('--status')
    s.add_argument('--papertrade', help='folder papertrade/ (claude*.csv): kecualikan posisi Claude TERBUKA sahaja; isi belian_ke')
    r = sp.add_parser('rekod'); r.add_argument('--db'); r.add_argument('--isian'); r.add_argument('--out', default='out'); r.add_argument('--status')
    b = sp.add_parser('batch'); b.add_argument('--out'); b.add_argument('--run')
    a = p.parse_args()
    {'harga': cmd_harga, 'scan': cmd_scan, 'rekod': cmd_rekod, 'batch': cmd_batch}[a.cmd](a)
