# jana_db.py — dokumen db dashboard daripada fail repo (tanpa LLM), untuk sesi Claude harian yang hanya MENOLAK fail ke db
# (ArtifactData batch dengan file_path; tugasan_v3 §6). Menggantikan JSON yang dibina dengan tangan oleh rutin 6:02 / 7:47 / 9:35.
#
#   python3 BacktestShariah2/standard/jana_db.py --keluar <folder> [--versi versi.json]
#   -> <folder>/<koleksi>/<doc>.json, <folder>/batch_<n>.json (senarai writes ArtifactData; <= 50 tulisan dan < 900 KB
#      setiap batch) dan <folder>/ringkas.json. --versi: {"papertrade/claude": 14, …} (daripada senarai ArtifactData list)
#      supaya setiap tulisan membawa if_version; dokumen tanpa versi = dokumen baharu.
# Dokumen: papertrade/moomoo, papertrade/claude… (1:1 dengan claude*.csv), (senarai_beli tidak ditolak sejak 19 Okt 2026),
# papertrade/watchlist(+_2…), prestasi/ringkasan, prestasi/mae, prestasi/portfolio_slot, harian/status. sektor/snapshot dijana oleh tugasan
# mingguan (data/db/sektor_snapshot.json, jika ada; medan posisi dikemas kini di sini).
import argparse, csv, glob, json, os, re, statistics as stt, sys

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
    """prestasi/portfolio_slot: dua portfolio maya 10 slot (standard/portfolio_slot.py, daripada Lejar Penuh) untuk kad
    Eksperimen dalam tab Ringkasan. None jika fail belum dijana."""
    import portfolio_slot as PS
    out, spy, hari = {}, None, []
    for k, nama in PS.PORTFOLIO.items():
        pe, pp = os.path.join(folder, f'{k}_ekuiti.csv'), os.path.join(folder, f'{k}_posisi.csv')
        if not (os.path.exists(pe) and os.path.exists(pp)):
            return None
        E, R = pd.read_csv(pe), pd.read_csv(pp)
        if E.empty:
            return None
        kel = R[R.status == 'Keluar']
        out[k] = dict(nama=f'{k}: {nama}', pulangan_pct=round(100 * (E.ekuiti.iloc[-1] - 1), 2), mdd_pct=round(100 * PS.mdd(E.ekuiti), 2),
                      dipegang=int((R.status == 'Pegang').sum()), keluar=int(len(kel)),
                      menang_pct=round(100 * float((kel.untung_pct > 0).mean()), 1) if len(kel) else None,
                      ekuiti=[[t, round(float(e), 5)] for t, e in zip(E.tarikh, E.ekuiti)],
                      posisi=json.loads(R.round(4).to_json(orient='records')))
        spy, hari = round(100 * (float(E.spy.iloc[-1]) - 1), 2), list(E.tarikh)
    return dict(dibina=dibina, mula=hari[0], sesi_terakhir=hari[-1], sesi=len(hari), spy_pct=spy, portfolio=out,
                nota='Rekod sahaja (kajian/KAJIAN_PORTFOLIO.md). 10 slot x 10% ekuiti, satu posisi setiap saham, keluar lorong 2; '
                     'RS_10 = RS pasaran tertinggi, RAWAK_10 = kawalan rawak. Dibina semula setiap malam oleh lejar.yml.')


def sesi_stor(path=STATUS_HARGA):
    """Sesi terkini stor harga repo (status.json terkini.sesi, YYYYMMDD) sebagai YYYY-MM-DD; '' jika tiada.
    Sandaran tarikh data apabila status_harian.json tiada dalam folder (mod bayang: Actions menulis ke bayang/ sahaja)."""
    try:
        s = str(json.load(open(path, encoding='utf-8')).get('terkini', {}).get('sesi', ''))
    except (OSError, ValueError, AttributeError):
        return ''
    return f'{s[:4]}-{s[4:6]}-{s[6:8]}' if len(s) == 8 and s.isdigit() else ''


# ---------------------------------------------------------------- utama
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
    wl = baca_csv(os.path.join(a.folder, 'watchlist.csv'))
    docs['papertrade/watchlist'] = dict(
        definisi='Hampir Signal: semua syarat entry selain pencetus dipenuhi; pencetus dalam <=2% (pct_dipenuhi = 100 - jarak_pct, '
                 'maks 99.9). Maks 5 setiap kaedah. Terkeluar signal dibuang serta-merta (tugasan_v3 §3).',
        dibina=malam.get('masa', dibina), gred_pada=st.get('gred', {}).get('tarikh', ''), pemangkin_pada=st.get('gred', {}).get('tarikh', ''),
        tarikh_data=wl[0]['tarikh_data'] if wl else S, rows=[baris_db(r, PETA_WATCH) for r in wl])
    # prestasi
    mae = penurunan_maks(M, C, a.stor)
    docs['prestasi/mae'] = dict(rows=mae, dibina=dibina, harga_hingga=f'{S} tutup',
                                definisi='Penurunan maksimum % = (harga rendah terendah sejak hari beli hingga hari ini, atau sehingga keluar) ÷ harga beli − 1, maksimum 0. Bagi posisi keluar: rendah hari sebelum hari keluar dan harga keluar. Kunci: akaun|saham|kaedah|tarikh_beli (akaun M=Moomoo, C=Claude).')
    docs['prestasi/ringkasan'] = dict(prestasi(M, C, mae), dibina=dibina, harga_pada=f'{S} tutup',
                                      nota='Dikira oleh standard/jana_db.py (GitHub Actions + sesi tolak db) dengan peraturan skor & keputusan P4 (sama seperti halaman).')
    ps = portfolio_slot(dibina)
    if ps:
        docs['prestasi/portfolio_slot'] = ps
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
    # tulis + bahagi + batch
    os.makedirs(a.keluar, exist_ok=True)
    versi = json.load(open(a.versi)) if a.versi else {}
    tulis = []
    for nama, d in docs.items():
        kol, doc = nama.split('/')
        bahagian = bahagi(d, doc, 200000) if doc in ('senarai_beli', 'watchlist') else [(doc, d)]
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
            tulis.append((w, sz))
    batches, cur, size = [], [], 0
    for w, sz in tulis:
        if cur and (size + sz > HAD_BATCH or len(cur) >= 50):
            batches.append(cur); cur, size = [], 0
        cur.append(w); size += sz
    if cur:
        batches.append(cur)
    fail = []
    for i, bt in enumerate(batches):
        p = os.path.join(a.keluar, f'batch_{i}.json'); json.dump(bt, open(p, 'w'), indent=1); fail.append(p)
    ring = dict(dibina=dibina, sesi=S, dokumen=len(tulis), batch=fail, tanpa_versi=[f"{w['collection']}/{w['doc_id']}" for w, _ in tulis if 'if_version' not in w],
                pengawas=pengawas(st, masa))
    json.dump(ring, open(os.path.join(a.keluar, 'ringkas.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(ring, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
