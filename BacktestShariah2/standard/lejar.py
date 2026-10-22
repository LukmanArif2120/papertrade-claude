"""Lejar Penuh Papertrade (sejak 16 Okt 2026) — SEMUA isyarat SEMUA kaedah dibeli dan dikeluarkan dengan peraturan
yang sama (tiada had 10 sekaedah, tiada keutamaan 431), supaya data setiap kaedah adil dan setanding dengan backtest.
Dijalankan oleh GitHub Actions (`.github/workflows/lejar.yml`) selepas Harga harian; tanpa LLM, tanpa Moomoo.
Papertrade C (claude*.csv) dan tiga rutin harian TIDAK diubah (fasa 1: berjalan selari).

  python3 lejar.py stor                         # gabung data/harga/terkini.csv (+ sejarah.csv saham baharu) ke stor repo
  python3 lejar.py jalan [--mula S] [--hingga S] [--proses 4] [--hanya M01,M02]
                                                # proses setiap sesi belum diproses mengikut urutan (tampung larian terlepas)
  python3 lejar.py ringkas                      # lejar/RINGKASAN.md + ringkasan.json (+ banding Papertrade C)
  python3 lejar.py semak                        # semakan integriti lejar; keluar 1 jika rosak

Peraturan setiap sesi S (data dipotong <= S; modul kaedah = kod/kaedah/Mxx.py, logik dagangan = enjin v1.2):
1. Keluar posisi terbuka, bar demi bar selepas `dinilai_hingga` (gelung enjin.trades): buka <= henti (dari hari kedua)
   -> buka; rendah <= henti -> henti; sasaran (tgt bar sebelum, dari hari kedua): buka >= sasaran -> buka, tinggi >=
   sasaran -> sasaran; isyarat keluar bar j -> jual pada buka bar seterusnya (bar akhir: `keluar_esok`); had masa
   (j - i >= TMAX) -> tutup. Posisi yang keluar dibekukan dalam `tutup/<YYYY-MM>.csv`.
2. Masuk bagi isyarat menunggu (bar i): pada buka bar seterusnya saham itu (i+1), hanya jika sig[i] masih benar apabila
   bar i+1 diketahui (peraturan buka modul: buka_maks, henti ikut buka, isyarat mingguan), bar i+1 ada dagangan
   (buka > 0, volum > 0) dan buka > henti[i] (tugasan_v3 §4). Henti dibekukan = stop[i]. Selainnya -> `langkau/`.
3. Isyarat baharu bar S: saham layak (data/harga/univ.txt, tutup >= USD10), bar >= PERLU_BAR (atau SILANG), indeks
   bar >= WARM. Isyarat semasa kaedah sama memegang saham itu (termasuk hari keluar) diabaikan, seperti enjin.
   Semua isyarat direkod dalam `isyarat/<S>.csv.gz`; yang layak masuk menunggu sesi seterusnya (`tunggu.csv`).
4. Dua lorong keluar (sejak 17 Okt 2026, DUA_LORONG): lorong 1 = peraturan 1; lorong 2 (pegang selagi naik, dipinda 19 Okt
   2026: tutup < tutup tertinggi sejak beli − 4×ATR14, paras hanya naik, tanpa henti kaedah) dikira oleh standard/keluar_lorong.py.
   Posisi kekal dalam terbuka.csv sehingga kedua-dua lorong keluar, tetapi sejak 19 Okt 2026 hanya lorong 1 yang menyekat
   isyarat baharu kaedah+saham sama (lorong 1 lejar = enjin; posisi lorong 2 boleh bertindih). Apabila peraturan
   lorong 2 berubah (keluar_lorong.VERSI lain daripada status.json `lorong2`), `jalan` membina semula lejar dari sesi mula.
5. Saham tidak layak pada sesi S (sejak 21 Okt 2026, kod/tidak_layak.py: diambil alih — corak harga terkunci atau
   data/ambil_alih.csv — atau tidak cair): isyarat direkod (`tidak_layak` = sebab) tetapi tidak masuk menunggu; isyarat
   menunggu dilangkau ('saham <sebab>'). Posisi saham tanpa bar >= tidak_layak.DELIST_SESI sesi (delist) ditutup pada tutup
   bar terakhir (sebab_keluar / lorong 2 'delist'). Peraturan atau senarai berubah (status.json `tidak_layak`) -> bina
   semula seperti peraturan 4.
Harga: stor repo `data/harga/stor/` (format kod/stor.py; yfinance, semakan silang Moomoo oleh rutin 6:02).
Jika harga lama dilaras (split), posisi terbuka dilaras dengan nisbah sama (lajur `laras`).
"""
import os, sys, json, glob, argparse, importlib, time
from multiprocessing import get_context
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
KOD = os.path.join(BS2, 'kod'); sys.path.insert(0, KOD); sys.path.insert(0, HERE)
import enjin  # noqa: E402
from stor import muat, frames_dict, LAJ, tulis_log_laras  # noqa: E402
import keluar_lorong  # noqa: E402
import tidak_layak  # noqa: E402
import dagangan  # noqa: E402

HARGA = os.path.join(BS2, 'data', 'harga')
STOR = os.environ.get('LEJAR_STOR', os.path.join(HARGA, 'stor'))
LEJAR = os.environ.get('LEJAR_DIR', os.path.join(BS2, 'lejar'))
HARGA_MIN = 10.0
TAMAT_TUNGGU = 5      # sesi maksimum isyarat menunggu bar masuk (saham digantung / data lewat)
TOLERANSI_LARAS = 0.003
LIPUTAN_MIN = 0.99   # pecahan saham layak (ada bar sesi sebelum) yang mesti ada bar sesi S sebelum diproses
# Dua lorong keluar (keputusan pengguna 17 Okt 2026; standard/keluar_lorong.py): lorong 1 = peraturan kaedah (enjin, lajur
# tarikh_keluar …), lorong 2 = pegang selagi naik (Chandelier tutup 4×ATR14 sejak 19 Okt 2026). Posisi kekal dalam terbuka.csv
# sehingga kedua-dua lorong keluar; kemudian dipindah ke tutup/. Isyarat baharu kaedah+saham sama disekat selagi lorong 1
# terbuka (termasuk hari lorong 1 keluar), seperti enjin.
# False = tingkah laku enjin asal (posisi tutup apabila lorong 1 keluar); dipakai oleh ujian kesetaraan enjin.
DUA_LORONG = True
# Logik keluar Lejar (kunci bina semula bersama tidak_layak.versi()): 22 Okt 2026 — laluan penuh dari bar isyarat (R2) dan lajur
# kaedah bagi dagangan sendiri untuk modul replika (kod/dagangan.py, R10)
VERSI_KELUAR = 'laluan penuh + dagangan sendiri v1 (22 Okt 2026)'

L_ASAS = ['id_kaedah', 'saham', 'sumber', 'tarikh_isyarat', 'rank', 'tarikh_beli', 'harga_beli', 'henti', 'sasaran',
          'tmax', 'belian_ke', 'dinilai_hingga', 'keluar_esok', 'laras']
L_K1 = ['tarikh_keluar', 'harga_keluar', 'sebab_keluar', 'hari', 'untung_pct', 'pulangan', 'mfe_pct', 'mae_pct']
L_K2 = ['keluar_henti', 'tarikh_keluar_henti', 'harga_keluar_henti', 'untung_henti_pct', 'tutup_semua']
L_POS = L_ASAS + L_K1 + L_K2      # terbuka.csv: lorong 1 boleh sudah keluar sementara lorong 2 masih terbuka
L_TUTUP = L_POS
L_TUNGGU = ['id_kaedah', 'saham', 'sumber', 'tarikh_isyarat', 'rank', 'henti', 'sasaran', 'tutup']
L_LANGKAU = ['id_kaedah', 'saham', 'tarikh_isyarat', 'sesi', 'sebab', 'buka', 'henti']
L_ISYARAT = ['sesi', 'kaedah', 'saham', 'rank', 'henti', 'sasaran', 'tutup', 'sumber', 'dipegang', 'pemanasan', 'tidak_layak']


# ---------------------------------------------------------------- bantu
def tkh(x):
    return str(pd.Timestamp(str(x)).date())


def nombor(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return np.nan
    return v


def r4(x):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) else round(float(x), 4)


def senarai_kaedah():
    f = glob.glob(os.path.join(KOD, 'kaedah', 'M*.py'))
    return sorted((os.path.basename(x)[:-3] for x in f), key=lambda x: int(x[1:]))


def baca(p, lajur):
    if not os.path.exists(p):
        return pd.DataFrame(columns=lajur)
    d = pd.read_csv(p, dtype=str, keep_default_na=False)
    for c in lajur:
        if c not in d: d[c] = ''
    return d[lajur]


def tulis_csv(d, p, lajur):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    pd.DataFrame(d, columns=lajur).to_csv(p, index=False)


def tambah_bulan(rows, folder, kunci, lajur):
    """Tambah baris ke <folder>/<YYYY-MM>.csv mengikut tarikh `kunci` (fail sedia ada tidak ditulis semula selain ditambah)."""
    if not rows: return
    d = pd.DataFrame(rows, columns=lajur)
    for bln, g in d.groupby(d[kunci].str[:7]):
        p = os.path.join(folder, f'{bln}.csv'); os.makedirs(folder, exist_ok=True)
        lama = list(pd.read_csv(p, nrows=0).columns) if os.path.exists(p) else None
        if lama is not None and lama != lajur:   # tajuk lama (sebelum lajur baharu): tulis semula dengan lajur semasa
            x = pd.read_csv(p, dtype=str, keep_default_na=False)
            pd.concat([x.reindex(columns=lajur, fill_value=''), g.astype(object)], ignore_index=True).to_csv(p, index=False)
            continue
        g.to_csv(p, mode='a', header=lama is None, index=False)


def univ_layak():
    p = os.environ.get('LEJAR_UNIV', os.path.join(HARGA, 'univ.txt'))
    return {x.strip().replace('US.', '') for x in open(p) if x.strip()} if os.path.exists(p) else None


UNIV_ARKIB = os.path.join(LEJAR, 'univ_arkib')   # dalam lejar/ supaya di-commit oleh lejar.yml


def univ_sesi(S, semasa, simpan):
    """Universe bagi sesi S (sejak 22 Okt 2026, kajian/KAJIAN_DATA_TERCEMAR.md R8): arkib `lejar/univ_arkib/<S>.txt`
    jika ada, supaya bina semula lejar memakai universe sebenar sesi itu; jika tiada, universe semasa — dan disimpan ke arkib
    apabila S = sesi terkini (larian biasa), tidak semasa bina semula sesi lama."""
    p = os.path.join(UNIV_ARKIB, f"{pd.Timestamp(S).strftime('%Y%m%d')}.txt")
    if os.path.exists(p):
        return {x.strip() for x in open(p) if x.strip()}
    if semasa is not None and simpan:
        os.makedirs(UNIV_ARKIB, exist_ok=True)
        open(p, 'w').write('\n'.join(sorted(semasa)) + '\n')
    return semasa


# ---------------------------------------------------------------- stor harga repo
def tulis_stor(d, p):
    """Format tetap: harga 6 angka bererti (seperti kod/stor.py), volum integer. Pulang True jika fail berubah."""
    d = d[LAJ].copy()
    for c in ('open', 'high', 'low', 'close'): d[c] = pd.to_numeric(d[c], errors='coerce').astype(float)
    d['volume'] = pd.to_numeric(d.volume, errors='coerce').fillna(0).round().astype('int64')
    d['date'] = d.date.astype('int64')
    teks = d.sort_values(['ticker', 'date']).to_csv(index=False, float_format='%.6g')
    if os.path.exists(p) and open(p).read() == teks:
        return False
    open(p, 'w').write(teks)
    return True


def tampal_moomoo(stor):
    """Moomoo menang (tugasan_v3 §6): buka rasmi kline Moomoo yang disahkan rutin 6:02 (claude*.csv, nota bermula
    'buka rasmi') menggantikan buka yfinance jika beza > 0.5%. Entri baharu hanya bagi tarikh selepas sesi terakhir lejar
    (posisi yang sudah direkod tidak berubah); semua entri dalam buka_moomoo.csv dipakai semula setiap larian supaya tidak
    ditimpa yfinance. Sejak 22 Okt 2026 (kajian/KAJIAN_DATA_TERCEMAR.md R1): nota 'buka sementara … (sahkan kline …)' TIDAK
    diterima (buka 9:35 NY belum rasmi), dan nilai disahkan terkini menggantikan entri lama bagi saham+tarikh sama."""
    p = os.path.join(STOR, 'buka_moomoo.csv')
    T = pd.read_csv(p, dtype={'ticker': str}) if os.path.exists(p) else pd.DataFrame(columns=['ticker', 'date', 'open'])
    stp = os.path.join(LEJAR, 'status.json')
    akhir = int(json.load(open(stp)).get('sesi_terakhir', '0').replace('-', '')) if os.path.exists(stp) else 0
    fs = sorted(glob.glob(os.path.join(BS2, 'papertrade', 'claude*.csv')))
    if fs:
        C = pd.concat([pd.read_csv(f, dtype=str, keep_default_na=False) for f in fs])
        C = C[(C.tidak_dibeli != 'True') & (C.harga_beli != '') & C.nota.str.contains(r'^(?:belian ke-\d+; )?buka rasmi', regex=True)]
        C = C.assign(date=C.tarikh_beli.str.replace('-', '').astype(int), open=pd.to_numeric(C.harga_beli, errors='coerce'))
        C = C[C.date > akhir].groupby(['saham', 'date'], as_index=False).open.median().rename(columns={'saham': 'ticker'})
        T = pd.concat([C, T]).drop_duplicates(['ticker', 'date'], keep='first')   # nilai disahkan terkini menang
    T = T.assign(date=T.date.astype('int64'), open=pd.to_numeric(T.open, errors='coerce').astype(float)).dropna(subset=['open'])
    n = 0
    for nm, d in stor.items():
        m = d.reset_index().merge(T, on=['ticker', 'date'], suffixes=('', '_mm'))
        m = m[(m.open_mm / m.open - 1).abs() > 0.005]
        if len(m):
            i = m['index'].values
            d.loc[i, 'open'] = m.open_mm.values
            d.loc[i, 'high'] = np.maximum(d.loc[i, 'high'].values, m.open_mm.values)
            d.loc[i, 'low'] = np.minimum(d.loc[i, 'low'].values, m.open_mm.values)
            n += len(m)
    T.sort_values(['date', 'ticker']).to_csv(p, index=False)
    return n


def cmd_stor(a):
    import harga_yf
    stor = muat(STOR)
    ada = {t: n for d in stor.values() for t, n in d.groupby('ticker').size().items()}
    fail = []
    sj = os.path.join(HARGA, 'sejarah.csv')
    if os.path.exists(sj):   # sejarah hanya bagi saham yang belum cukup sejarah dalam stor
        s = pd.read_csv(sj); s = s[s.ticker.map(lambda t: ada.get(t, 0) < 260)]
        if len(s): fail.append(s)
    tk = os.path.join(HARGA, 'terkini.csv')
    if os.path.exists(tk): fail.append(pd.read_csv(tk))
    if not fail:
        print('tiada fail harga baharu'); return
    baru = pd.concat(fail, ignore_index=True)
    # nisbah laras (split/dividen) dicatat sebelum digabung — logik sama dengan harga_yf.gabung_satu
    laras = {}
    semua = pd.concat(stor.values(), ignore_index=True) if stor else pd.DataFrame(columns=LAJ)
    m = semua.merge(baru, on=['ticker', 'date'], suffixes=('_l', '_k'))
    if len(m):
        r = (m.close_k / m.close_l).groupby(m.ticker).median()
        laras = {t: round(float(v), 6) for t, v in r.items() if abs(v - 1) > TOLERANSI_LARAS}
    # peristiwa besar (kod/peristiwa.py): dividen yfinance >= 2% -> jadual faktor sebelum digabung (guna pada stor larian ini)
    import peristiwa
    sem = pd.concat([d for d in stor.values()] + [baru[LAJ]], ignore_index=True).drop_duplicates(['ticker', 'date'], keep='last')
    fr_sem, _ = frames_dict({'harga_A.csv': sem})
    nota_div = peristiwa.tambah_dari_dividen(fr_sem)
    stor, nota = harga_yf.gabung(stor, baru, STOR)
    nota['log_laras'] = tulis_log_laras(STOR, nota.pop('log_laras'))   # keputusan laras/anomali/faktor (tambah sahaja)
    nota['faktor_dividen'] = [f"{x['saham']} {x['tarikh_ex']} {x['catatan']}" for x in nota_div]
    try:   # calon spin-off / pengagihan (jurang <= −15% tanpa earnings) untuk disahkan rutin 6:02 (Moomoo rehab)
        import penganalisis
        fr_baru, idx_baru = frames_dict(stor)
        nota['faktor_calon'] = [f"{x['saham']} {x['tarikh']} {x['jurang']}" for x in
                                peristiwa.kesan_calon(fr_baru, list(idx_baru['SPY'].index), penganalisis.muat_earnings())]
    except Exception as e:
        nota['faktor_calon'] = f'{type(e).__name__}: {e}'
    nota['moomoo'] = tampal_moomoo(stor)
    ubah = [nm for nm, d in stor.items() if tulis_stor(d, os.path.join(STOR, nm))]
    # saham universe tanpa sejarah mencukupi -> minta sejarah 3 tahun (harga_harian.yml)
    u = univ_layak() or set()
    n = {t: c for d in stor.values() for t, c in d.groupby('ticker').size().items()}
    perlu = sorted(t for t in u if n.get(t, 0) < 60)
    if perlu:
        p = os.path.join(HARGA, 'perlu_sejarah.txt')
        lama = {x.strip() for x in open(p)} if os.path.exists(p) else set()
        open(p, 'w').write('\n'.join(sorted(lama | set(perlu))) + '\n')
    st = dict(dikemaskini=pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M UTC'),
              bar_terakhir=int(max(d.date.max() for d in stor.values())), laras=laras, perlu_sejarah=perlu[:100], **nota)
    if ubah or not os.path.exists(os.path.join(STOR, 'status.json')):   # status hanya ditulis jika stor berubah (elak commit kosong)
        json.dump(st, open(os.path.join(STOR, 'status.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(dict(bar_terakhir=st['bar_terakhir'], fail_berubah=ubah, laras=len(laras), perlu_sejarah=len(perlu))))


# ---------------------------------------------------------------- logik dagangan (enjin v1.2, satu posisi)
def langkah_keluar(g, p, tmax):
    """Nilai posisi p (dict) atas bar g dari bar masuk (laluan penuh setiap sesi, seperti enjin dan harian_c.nilai_keluar).
    Ubah p di tempat (dinilai_hingga, keluar_esok = rekod sahaja). Pulang dict keluar (tarikh_keluar, harga_keluar,
    sebab_keluar, j) atau None jika masih terbuka.
    Sejak 22 Okt 2026 (kajian/KAJIAN_DATA_TERCEMAR.md R2): tidak lagi bermula dari `dinilai_hingga`. Modul yang exitc-nya
    bergantung jujukan dagangan (`_exitc_*`: M19, M20, M31, M38, M40, M41, M76, M78, M81, M82) hanya boleh menanda bar j
    apabila bar j+1 wujud; penilaian tokokan melangkau bar itu selamanya (GEF M76, DELL M81 tidak keluar)."""
    ix = g.index; n = len(g)
    try:
        i = ix.get_loc(pd.Timestamp(p['tarikh_isyarat']))
    except KeyError:
        return None
    k = i + 1
    if k >= n:
        return None
    o, h, l, c = g.open.values, g.high.values, g.low.values, g.close.values
    tg = g['tgt'].astype(float).values; ex = g['exitc'].fillna(False).astype(bool).values
    sp = nombor(p['henti']); sp = -np.inf if np.isnan(sp) else sp
    p['keluar_esok'] = False
    for j in range(k, n):
        tgt = tg[j - 1] if j > i + 1 else np.nan
        if j > i + 1 and o[j] <= sp: return dict(tarikh_keluar=tkh(ix[j]), harga_keluar=float(o[j]), sebab_keluar='henti', j=j)
        if l[j] <= sp: return dict(tarikh_keluar=tkh(ix[j]), harga_keluar=float(sp), sebab_keluar='henti', j=j)
        if not np.isnan(tgt):
            if j > i + 1 and o[j] >= tgt: return dict(tarikh_keluar=tkh(ix[j]), harga_keluar=float(o[j]), sebab_keluar='sasaran', j=j)
            if h[j] >= tgt: return dict(tarikh_keluar=tkh(ix[j]), harga_keluar=float(tgt), sebab_keluar='sasaran', j=j)
        if ex[j]:
            if j + 1 < n: return dict(tarikh_keluar=tkh(ix[j + 1]), harga_keluar=float(o[j + 1]), sebab_keluar='isyarat keluar', j=j + 1)
            p['keluar_esok'] = True; p['dinilai_hingga'] = tkh(ix[j]); return None
        if tmax and (j - i) >= tmax: return dict(tarikh_keluar=tkh(ix[j]), harga_keluar=float(c[j]), sebab_keluar='masa', j=j)
        p['dinilai_hingga'] = tkh(ix[j])
    return None


def tutup_posisi(g, p, k):
    """Lengkapkan baris tutup daripada keputusan langkah_keluar."""
    ix = g.index; i = ix.get_loc(pd.Timestamp(p['tarikh_isyarat'])); j = k['j']; e = float(p['harga_beli']); x = k['harga_keluar']
    r = dict(p); r.update(tarikh_keluar=k['tarikh_keluar'], harga_keluar=r4(x), sebab_keluar=k['sebab_keluar'], hari=int(j - i),
                         untung_pct=r4((x / e - 1) * 100), pulangan=round(x / e * (1 - enjin.COST) / (1 + enjin.COST) - 1, 6),
                         mfe_pct=r4((g.high.values[i + 1:j + 1].max() / e - 1) * 100),
                         mae_pct=r4((g.low.values[i + 1:j + 1].min() / e - 1) * 100), dinilai_hingga=k['tarikh_keluar'],
                         keluar_esok=False)
    return r


def tutup_delist(g, p):
    """Saham tanpa bar >= tidak_layak.DELIST_SESI sesi (delist selepas ambil alih / tiada data): lorong yang masih terbuka
    ditutup pada tutup bar terakhir (anggaran nilai tunai)."""
    ix = g.index; c = float(g.close.iloc[-1]); e = float(p['harga_beli'])
    if not p.get('tarikh_keluar'):
        p = tutup_posisi(g, p, dict(tarikh_keluar=tkh(ix[-1]), harga_keluar=c, sebab_keluar='delist', j=len(g) - 1))
    if DUA_LORONG and not benar(p.get('keluar_henti')):
        p = dict(p); p.update(keluar_henti=True, tarikh_keluar_henti=tkh(ix[-1]), harga_keluar_henti=r4(c),
                              untung_henti_pct=round((c / e - 1) * 100, 2))
    p['tutup_semua'] = True
    return p


def benar(v):
    return str(v).strip().lower() == 'true'


def tarikh_tutup(r):
    """Tarikh posisi tutup sepenuhnya (lorong terakhir keluar); '' jika masih ada lorong terbuka."""
    if not DUA_LORONG:
        return r.get('tarikh_keluar') or ''
    if not (r.get('tarikh_keluar') and benar(r.get('keluar_henti'))):
        return ''
    return max(r['tarikh_keluar'], r['tarikh_keluar_henti'])


def nilai_posisi(g, p, tmax):
    """Nilai semua lorong keluar posisi p atas bar g. Pulang (baris, tutup_sepenuhnya)."""
    if not p.get('tarikh_keluar'):
        k = langkah_keluar(g, p, tmax)
        if k: p = tutup_posisi(g, p, k)
    if not DUA_LORONG:
        return p, bool(p.get('tarikh_keluar'))
    if not benar(p.get('keluar_henti')):
        ix = [tkh(x) for x in g.index]
        L2, _ = keluar_lorong.nilai_baris(ix, g.open.values.astype(float), g.high.values.astype(float), g.low.values.astype(float),
                                          g.close.values.astype(float), p['tarikh_beli'], float(p['harga_beli']))
        if L2 is not None:
            p = dict(p); p.update({c: v for c, v in L2.items() if c in L_K2})
    p['tutup_semua'] = bool(tarikh_tutup(p))
    return p, p['tutup_semua']


# ---------------------------------------------------------------- satu kaedah, satu sesi (proses anak)
FR = {}; IDX = {}


def kerja(arg):
    mid, S, terbuka, tunggu, layak, a431, bil, aa = arg
    t0 = time.time(); St = pd.Timestamp(S)
    try:
        m = importlib.import_module(f'kaedah.{mid}')
    except Exception as e:
        return dict(mid=mid, ralat=f'import: {type(e).__name__}: {e}', terbuka=terbuka, tunggu=tunggu)
    perlu = getattr(m, 'PERLU_BAR', 260); warm = getattr(m, 'WARM', 200) or 0; tmax = m.TMAX or 0
    fr = {}
    for t, g in FR.items():
        if g.index[-1] > St: g = g[g.index <= St]
        if len(g) >= 60 and (len(g) >= perlu or m.SILANG): fr[t] = g.copy()
    idx = {t: (g[g.index <= St].copy() if g.index[-1] > St else g.copy()) for t, g in IDX.items()}
    try:
        m.sedia(fr, idx)
    except Exception as e:
        return dict(mid=mid, ralat=f'sedia: {type(e).__name__}: {e}', terbuka=terbuka, tunggu=tunggu)
    for g in fr.values(): enjin.siap(g)
    sendiri = dagangan.perlu(mid, m)

    def g_dagangan(t, g, ti):
        """Modul replika (kod/dagangan.py): lajur kaedah bagi dagangan yang isyaratnya pada ti; selainnya g."""
        if not sendiri:
            return g
        x = FR[t]
        x = x[x.index <= St] if x.index[-1] > St else x
        h = dagangan.sedia_dagangan(m, t, x, idx, ti)
        return h if h is not None else g
    tutup, kekal, langkau, beli, nota = [], [], [], [], []
    # 1) keluar
    for p in terbuka:
        g = fr.get(p['saham'])
        if g is None:
            kekal.append(p); continue
        g = g_dagangan(p['saham'], g, p['tarikh_isyarat'])
        e = float(p['harga_beli'])
        try:
            ob = float(g.open.loc[pd.Timestamp(p['tarikh_beli'])])
            r = ob / e
            if abs(r - 1) > TOLERANSI_LARAS:   # stor dilaras (split): laras posisi dengan nisbah sama
                for c in ('harga_beli', 'henti', 'sasaran'):
                    v = nombor(p[c]); p[c] = r4(v * r) if not np.isnan(v) else p[c]
                p['laras'] = r4(nombor(p.get('laras')) * r if not np.isnan(nombor(p.get('laras'))) else r)
                nota.append(f"{mid} {p['saham']}: laras x{r:.4f}")
        except KeyError:
            pass
        if pd.Timestamp(p['tarikh_isyarat']) not in g.index:
            nota.append(f"{mid} {p['saham']}: bar isyarat {p['tarikh_isyarat']} tiada dalam stor; keluar tidak dinilai")
        p, habis = nilai_posisi(g, p, tmax)
        if not habis and tidak_layak.sesi_tanpa_bar(g, IDX['SPY'].index if 'SPY' in IDX else [], St) >= tidak_layak.DELIST_SESI:
            p = tutup_delist(g, p); habis = True
        (tutup if habis else kekal).append(p)
    # isyarat kaedah+saham sama disekat selagi lorong 1 terbuka, termasuk hari ia keluar (seperti enjin); lorong 2 tidak menyekat
    pegang = {p['saham'] for p in kekal + tutup if not p.get('tarikh_keluar') or p['tarikh_keluar'] >= str(St.date())}
    # 2) masuk (isyarat menunggu)
    tunggu_baru = []
    for s in tunggu:
        t = s['saham']; g = fr.get(t); ti = pd.Timestamp(s['tarikh_isyarat'])
        jauh = int((IDX['SPY'].index[(IDX['SPY'].index > ti) & (IDX['SPY'].index <= St)]).size) if 'SPY' in IDX else 0
        def lk(sebab, buka=None):
            langkau.append(dict(id_kaedah=mid, saham=t, tarikh_isyarat=s['tarikh_isyarat'], sesi=str(St.date()), sebab=sebab,
                                buka=r4(buka) if buka is not None else None, henti=s.get('henti')))
        if t in pegang:
            lk('dipegang'); continue
        if t in aa:
            lk(f'saham {aa[t]}'); continue
        if g is None or ti not in g.index:
            if jauh >= TAMAT_TUNGGU: lk('tiada data')
            else: tunggu_baru.append(s)
            continue
        i = g.index.get_loc(ti)
        if i + 1 >= len(g):
            if jauh >= TAMAT_TUNGGU: lk('tiada bar masuk')
            else: tunggu_baru.append(s)
            continue
        ob = nombor(g.open.iloc[i + 1]); vb = nombor(g.volume.iloc[i + 1]); sp = nombor(g['stop'].iloc[i])
        if not bool(g['sig'].iloc[i]): lk('isyarat batal pada buka (peraturan kaedah)', ob); continue
        if not (ob > 0) or not (vb > 0): lk('tiada dagangan', ob); continue
        if not np.isnan(sp) and ob <= sp: lk('buka <= henti', ob); continue
        bil[t] = bil.get(t, 0) + 1
        p = dict(id_kaedah=mid, saham=t, sumber=s['sumber'], tarikh_isyarat=s['tarikh_isyarat'], rank=s.get('rank'),
                 tarikh_beli=tkh(g.index[i + 1]), harga_beli=r4(ob), henti=r4(sp) if not np.isnan(sp) else None,
                 sasaran=r4(nombor(g['tgt'].iloc[i])), tmax=tmax, belian_ke=bil[t], dinilai_hingga='', keluar_esok=False, laras='')
        beli.append(p)
        p, habis = nilai_posisi(g_dagangan(t, g, s['tarikh_isyarat']), p, tmax)
        (tutup if habis else kekal).append(p)
        pegang.add(t)
    # 3) isyarat baharu bar S
    isy = []
    for t, g in fr.items():
        if g.index[-1] != St or (layak is not None and t not in layak) or not bool(g['sig'].iloc[-1]): continue
        if float(g.close.iloc[-1]) < HARGA_MIN: continue
        rw = dict(sesi=str(St.date()), kaedah=mid, saham=t, rank=r4(nombor(g['rank'].iloc[-1])), henti=r4(nombor(g['stop'].iloc[-1])),
                  sasaran=r4(nombor(g['tgt'].iloc[-1])), tutup=r4(float(g.close.iloc[-1])), sumber='431' if t in a431 else 'lain',
                  dipegang=t in pegang, pemanasan=len(g) - 1 < warm, tidak_layak=aa.get(t, ''))
        isy.append(rw)
        if not rw['dipegang'] and not rw['pemanasan'] and not rw['tidak_layak']:
            tunggu_baru.append(dict(id_kaedah=mid, saham=t, sumber=rw['sumber'], tarikh_isyarat=rw['sesi'], rank=rw['rank'],
                                    henti=rw['henti'], sasaran=rw['sasaran'], tutup=rw['tutup']))
    return dict(mid=mid, ralat=None, terbuka=kekal, tunggu=tunggu_baru, tutup=tutup, beli=beli, langkau=langkau, isyarat=isy,
                nota=nota, s=round(time.time() - t0, 1))


# ---------------------------------------------------------------- larian
def keadaan():
    st = json.load(open(os.path.join(LEJAR, 'status.json'))) if os.path.exists(os.path.join(LEJAR, 'status.json')) else {}
    T = baca(os.path.join(LEJAR, 'terbuka.csv'), L_POS).to_dict('records')
    W = baca(os.path.join(LEJAR, 'tunggu.csv'), L_TUNGGU).to_dict('records')
    for p in T:
        p['keluar_esok'] = str(p['keluar_esok']).lower() == 'true'
        for c in L_K1 + L_K2:    # medan kosong -> tiada (posisi lama sebelum dua lorong, atau lorong 1 belum keluar)
            if p.get(c) == '': p.pop(c)
    bil = {}
    for f in [os.path.join(LEJAR, 'terbuka.csv')] + sorted(glob.glob(os.path.join(LEJAR, 'tutup', '*.csv'))):
        d = baca(f, ['id_kaedah', 'saham'])
        for (mid, t), n in d.groupby(['id_kaedah', 'saham']).size().items():
            bil.setdefault(mid, {})[t] = bil.get(mid, {}).get(t, 0) + int(n)
    return st, T, W, bil


def bina_semula(st):
    """Peraturan lorong 2 dipinda (keluar_lorong.VERSI lain daripada status.json `lorong2`): lorong 2 menentukan bila posisi
    tutup sepenuhnya (dan sebelum 19 Okt 2026 bila kaedah+saham boleh dibeli semula), jadi lejar dikosongkan dan diproses semula dari sesi mula
    dengan peraturan baharu. Sama apabila penapis saham tidak layak berubah (tidak_layak.versi() lain daripada `tidak_layak`,
    sejak 21 Okt 2026: peraturan atau senarai data/ambil_alih.csv). Pulang status baharu (sesi mula dikekalkan; ditulis segera
    supaya keadaan sentiasa konsisten)."""
    for f in [os.path.join(LEJAR, 'terbuka.csv'), os.path.join(LEJAR, 'tunggu.csv')] + \
            [x for d in ('tutup', 'langkau') for x in glob.glob(os.path.join(LEJAR, d, '*.csv'))] + \
            glob.glob(os.path.join(LEJAR, 'isyarat', '*.csv.gz')):
        os.remove(f)
    if st.get('lorong2') != keluar_lorong.VERSI:
        dari, ke = st.get('lorong2') or '2 tutup turun berturut atau henti', keluar_lorong.VERSI
    elif st.get('tidak_layak') != tidak_layak.versi():
        dari, ke = st.get('tidak_layak') or 'tiada penapis tidak layak', tidak_layak.versi()
    else:
        dari, ke = st.get('keluar') or 'tokokan dari dinilai_hingga', VERSI_KELUAR
    rekod = dict(tarikh=pd.Timestamp.now(tz='Asia/Kuala_Lumpur').strftime('%Y-%m-%d %H:%M MYT'),
                 dari=dari, ke=ke, sesi_terakhir_lama=st.get('sesi_terakhir'))
    print(json.dumps(dict(bina_semula=rekod), ensure_ascii=False), flush=True)
    st = dict(mula=st.get('mula'), lorong2=keluar_lorong.VERSI, tidak_layak=tidak_layak.versi(), keluar=VERSI_KELUAR,
              bina_semula=st.get('bina_semula', []) + [rekod])
    json.dump(st, open(os.path.join(LEJAR, 'status.json'), 'w'), ensure_ascii=False, indent=1)
    return st


def cmd_jalan(a):
    global FR, IDX
    os.makedirs(LEJAR, exist_ok=True)
    st, T, W, bil = keadaan()
    if DUA_LORONG and st.get('sesi_terakhir') and (st.get('lorong2') != keluar_lorong.VERSI
                                                   or st.get('tidak_layak') != tidak_layak.versi()
                                                   or st.get('keluar') != VERSI_KELUAR):
        st = bina_semula(st); T, W, bil = [], [], {}
    st['lorong2'] = keluar_lorong.VERSI; st['tidak_layak'] = tidak_layak.versi(); st['keluar'] = VERSI_KELUAR
    FR, IDX = frames_dict(muat(STOR))
    sesi = [x for x in IDX['SPY'].index]
    akhir = st.get('sesi_terakhir')
    hingga = pd.Timestamp(str(a.hingga)) if a.hingga else sesi[-1]
    if akhir:
        todo = [x for x in sesi if x > pd.Timestamp(akhir) and x <= hingga]
    else:   # larian pertama (atau bina semula): rekod isyarat sesi mula sahaja (tiada posisi lagi)
        mula = a.mula or st.get('mula')
        mula = pd.Timestamp(str(mula)) if mula else hingga
        todo = [x for x in sesi if mula <= x <= hingga]
        st['mula'] = str(todo[0].date()) if todo else None
    if not todo:
        print(json.dumps(dict(sesi_terakhir=akhir, diproses=0))); return
    kaedah = a.hanya.split(',') if a.hanya else senarai_kaedah()
    layak = univ_layak(); a431 = set(muat(STOR).get('harga_A.csv', pd.DataFrame(columns=['ticker'])).ticker)
    ctx = get_context('fork')
    with ctx.Pool(a.proses) as pool:
        for S in todo:
            t0 = time.time()
            layak_s = univ_sesi(S, layak, S == sesi[-1])
            # data sesi S mesti lengkap (Harga harian awal kadang-kadang belum ada bar bagi sebahagian saham);
            # jika tidak, berhenti tanpa memajukan sesi — larian sandaran / esok memproses semula dengan data penuh
            sb = [x for x in sesi if x < S]
            if sb and not getattr(a, 'paksa', False):
                ada = [t for t, g in FR.items() if (layak_s is None or t in layak_s) and sb[-1] in g.index]
                cukup = sum(1 for t in ada if S in FR[t].index) / max(len(ada), 1)
                if cukup < LIPUTAN_MIN:
                    print(json.dumps(dict(sesi=str(S.date()), ditangguh=f'liputan bar {cukup:.1%} < {LIPUTAN_MIN:.0%}')), flush=True)
                    break
                # tarikan yfinance awal (< 00:20 UTC selepas sesi) boleh tersilap harga buka; tunggu data muktamad
                tk = json.load(open(os.path.join(HARGA, 'status.json'))).get('terkini', {}) if os.path.exists(os.path.join(HARGA, 'status.json')) else {}
                if str(tk.get('sesi')) == S.strftime('%Y%m%d') and \
                        pd.Timestamp(tk.get('dijana', '1970-01-01 00:00 UTC').replace(' UTC', '')) < S + pd.Timedelta(hours=24, minutes=20):
                    print(json.dumps(dict(sesi=str(S.date()), ditangguh=f"data yfinance awal ({tk.get('dijana')})")), flush=True)
                    break
            Tm = {}; Wm = {}
            for p in T: Tm.setdefault(p['id_kaedah'], []).append(p)
            for w in W: Wm.setdefault(w['id_kaedah'], []).append(w)
            aa = {t: x['sebab'] for t, x in tidak_layak.tapis(FR, S).items()}   # diambil alih / tidak cair pada S
            args = [(mid, S, Tm.pop(mid, []), Wm.pop(mid, []), layak_s, a431, bil.get(mid, {}), aa) for mid in kaedah]
            hasil = pool.map(kerja, args, chunksize=1)
            T = [p for v in Tm.values() for p in v]; W = [w for v in Wm.values() for w in v]   # kaedah di luar senarai: kekal
            tutup, beli, langkau, isy, ralat, nota = [], [], [], [], [], []
            for h in hasil:
                T += h['terbuka']; W += h['tunggu']
                if h['ralat']: ralat.append(f"{h['mid']}: {h['ralat']}"); continue
                tutup += h['tutup']; beli += h['beli']; langkau += h['langkau']; isy += h['isyarat']; nota += h['nota']
                for p in h['beli']: bil.setdefault(h['mid'], {})[p['saham']] = p['belian_ke']
            tambah_bulan(tutup, os.path.join(LEJAR, 'tutup'), 'tarikh_keluar', L_TUTUP)
            tambah_bulan(langkau, os.path.join(LEJAR, 'langkau'), 'sesi', L_LANGKAU)
            os.makedirs(os.path.join(LEJAR, 'isyarat'), exist_ok=True)
            d = pd.DataFrame(isy, columns=L_ISYARAT); d['_n'] = d.kaedah.str[1:].astype(int)
            d.sort_values(['_n', 'saham']).drop(columns='_n').to_csv(
                os.path.join(LEJAR, 'isyarat', f"{S.strftime('%Y%m%d')}.csv.gz"), index=False, compression={'method': 'gzip', 'mtime': 0})
            T.sort(key=lambda p: (int(p['id_kaedah'][1:]), p['tarikh_beli'], p['saham']))
            W.sort(key=lambda w: (int(w['id_kaedah'][1:]), w['tarikh_isyarat'], w['saham']))
            tulis_csv(T, os.path.join(LEJAR, 'terbuka.csv'), L_POS)
            tulis_csv(W, os.path.join(LEJAR, 'tunggu.csv'), L_TUNGGU)
            ringkas = dict(sesi=str(S.date()), beli=len(beli), tutup=len(tutup), langkau=len(langkau), isyarat=len(isy),
                           terbuka=len(T), tunggu=len(W), kaedah_isyarat=len({r['kaedah'] for r in isy}), ralat=ralat, nota=nota[:50],
                           masa_s=round(time.time() - t0))
            st['sesi_terakhir'] = str(S.date())
            st['kemaskini'] = pd.Timestamp.now(tz='Asia/Kuala_Lumpur').strftime('%Y-%m-%d %H:%M MYT')
            st['bil_kaedah'] = len(kaedah)
            st['larian'] = (st.get('larian', []) + [ringkas])[-60:]
            json.dump(st, open(os.path.join(LEJAR, 'status.json'), 'w'), ensure_ascii=False, indent=1)
            print(json.dumps({k: v for k, v in ringkas.items() if k != 'nota'}, ensure_ascii=False), flush=True)


# ---------------------------------------------------------------- semakan & ringkasan
def semua_posisi():
    t = [baca(f, L_TUTUP) for f in sorted(glob.glob(os.path.join(LEJAR, 'tutup', '*.csv')))]
    T = pd.concat(t, ignore_index=True) if t else pd.DataFrame(columns=L_TUTUP)
    O = baca(os.path.join(LEJAR, 'terbuka.csv'), L_POS)
    return T, O


def cmd_semak(a):
    T, O = semua_posisi(); salah = []
    k = pd.concat([T[['id_kaedah', 'saham', 'tarikh_beli']], O[['id_kaedah', 'saham', 'tarikh_beli']]])
    if k.duplicated().any(): salah.append(f'kunci berganda: {int(k.duplicated().sum())}')
    if O[O.tarikh_keluar == ''].duplicated(['id_kaedah', 'saham']).any(): salah.append('lebih satu posisi lorong 1 terbuka bagi kaedah+saham sama')
    for nm, d in [('tutup', T), ('terbuka', O)]:
        hb = pd.to_numeric(d.harga_beli, errors='coerce')
        if (~(hb > 0)).any(): salah.append(f'{nm}: harga_beli tidak sah ({int((~(hb > 0)).sum())})')
        if (d.tarikh_beli <= d.tarikh_isyarat).any(): salah.append(f'{nm}: tarikh_beli <= tarikh_isyarat')
    if len(T):
        if (T.tarikh_keluar < T.tarikh_beli).any(): salah.append('tutup: tarikh_keluar < tarikh_beli')
        hk = pd.to_numeric(T.harga_keluar, errors='coerce')
        if (~(hk > 0)).any(): salah.append('tutup: harga_keluar tidak sah')
        if ~T.sebab_keluar.isin(['henti', 'sasaran', 'isyarat keluar', 'masa', 'delist']).all(): salah.append('tutup: sebab_keluar tidak dikenali')
        baru = T[T.tutup_semua != '']   # baris sejak dua lorong: mesti tutup sepenuhnya
        if len(baru) and not (baru.tutup_semua.str.lower() == 'true').all(): salah.append('tutup: ada lorong keluar belum keluar (tutup_semua bukan True)')
    for nm, d in [('tutup', T), ('terbuka', O)]:
        for c, t in (('keluar_henti', 'tarikh_keluar_henti'),):
            x = d[d[c].str.lower() == 'true']
            if len(x) and ((x[t] == '') | (x[t] < x.tarikh_beli)).any(): salah.append(f'{nm}: {c}=True tetapi {t} kosong/sebelum beli')
    # setiap posisi mesti bermula daripada isyarat yang direkod
    rek = set()
    for f in glob.glob(os.path.join(LEJAR, 'isyarat', '*.csv.gz')):
        d = pd.read_csv(f, dtype=str, keep_default_na=False); rek |= set(zip(d.kaedah, d.saham, d.sesi))
    tiada = [x for x in zip(pd.concat([T.id_kaedah, O.id_kaedah]), pd.concat([T.saham, O.saham]),
                            pd.concat([T.tarikh_isyarat, O.tarikh_isyarat])) if x not in rek]
    if tiada: salah.append(f'{len(tiada)} posisi tanpa rekod isyarat (cth. {tiada[:3]})')
    print('\n'.join(salah) if salah else f'Lejar sah: {len(T)} tutup, {len(O)} terbuka, {len(rek)} isyarat direkod.')
    sys.exit(1 if salah else 0)


def jangkaan():
    out = {}
    for f in glob.glob(os.path.join(KOD, 'registry', 'M*.csv')):
        mid = os.path.basename(f)[:-4]
        try:
            m = importlib.import_module(f'kaedah.{mid}')
            r = pd.read_csv(f); r = r[(r['set'].astype(str) == '431') & (r.varian == m.VARIAN)]
            if len(r):
                r = r.iloc[0]; out[mid] = dict(nama=m.NAMA, win=float(r.win), avg=float(r.avg) * 100, days=float(r.days))
        except Exception:
            pass
    return out


def cmd_ringkas(a):
    st = json.load(open(os.path.join(LEJAR, 'status.json'))) if os.path.exists(os.path.join(LEJAR, 'status.json')) else {}
    T, O = semua_posisi(); J = jangkaan()
    fr, _ = frames_dict(muat(STOR))
    akhir = {t: float(g.close.iloc[-1]) for t, g in fr.items()}
    P = pd.concat([T, O], ignore_index=True)   # lorong 1 dikira daripada semua posisi (terbuka.csv boleh ada lorong 1 sudah keluar)
    for c in ('untung_pct', 'hari', 'untung_henti_pct'): P[c] = pd.to_numeric(P[c], errors='coerce')
    P['untung_kini'] = [(akhir.get(t, np.nan) / float(h) - 1) * 100 if h else np.nan for t, h in zip(P.saham, P.harga_beli)]
    T, O = P[P.tarikh_keluar != ''], P[P.tarikh_keluar == '']   # T/O di bawah = lorong 1 keluar / masih dipegang
    rows = []
    for mid in senarai_kaedah():
        t = T[T.id_kaedah == mid]; o = O[O.id_kaedah == mid]; j = J.get(mid, {}); a = P[P.id_kaedah == mid]
        t2 = a[a.keluar_henti.str.lower() == 'true']
        rows.append(dict(id=mid, nama=j.get('nama', ''), posisi=len(t) + len(o), tutup=len(t), terbuka=len(o),
                         menang=r4((t.untung_pct > 0).mean() * 100) if len(t) else None, purata=r4(t.untung_pct.mean()) if len(t) else None,
                         hari=r4(t.hari.mean()) if len(t) else None, terbuka_purata=r4(o.untung_kini.mean()) if len(o) else None,
                         tutup_henti=len(t2), purata_henti=r4(t2.untung_henti_pct.mean()) if len(t2) else None,
                         j_menang=r4(j['win'] * 100) if j else None, j_purata=r4(j['avg']) if j else None, j_hari=r4(j['days']) if j else None))
    json.dump(dict(sesi_terakhir=st.get('sesi_terakhir'), mula=st.get('mula'), kaedah=rows), open(os.path.join(LEJAR, 'ringkasan.json'), 'w'),
              ensure_ascii=False, indent=1)
    f = lambda v, p=1: '' if v is None else f'{v:.{p}f}'
    L = ['# Lejar Penuh — ringkasan setiap kaedah', '',
         f"Dijana oleh `standard/lejar.py ringkas`. Lejar bermula {st.get('mula')}; sesi terakhir {st.get('sesi_terakhir')}. "
         f"{len(P)} posisi ({len(T)} tutup lorong 1, {len(O)} terbuka). Semua isyarat setiap kaedah dibeli pada buka rasmi esok "
         'dengan peraturan sama (tiada had sekaedah). Jangkaan = registry set 431 varian modul (dalam sampel).', '',
         'Nota: data awal didominasi posisi yang tutup cepat (kebanyakan kena henti); nilai hanya selepas posisi matang '
         '(lihat `WFO/README.md`, penilaian 15 Jan 2027).', '',
         'Dua lorong keluar (sejak 17 Okt 2026): Tutup/Menang/Purata tutup = lorong 1 (peraturan kaedah); Selagi naik = lorong 2 '
         '(pegang selagi naik, sejak 19 Okt 2026: tutup < tutup tertinggi sejak beli − 4×ATR14, paras hanya naik, tanpa henti kaedah). '
         'n = bilangan keluar.', '',
         '| Kaedah | Posisi | Tutup | Terbuka | Menang % | Purata tutup % | Hari | Purata terbuka % | Selagi naik n | Purata selagi naik % '
         '| Menang jangka % | Purata jangka % | Hari jangka |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in sorted(rows, key=lambda r: -r['posisi']):
        L.append(f"| {r['id']} {r['nama']} | {r['posisi']} | {r['tutup']} | {r['terbuka']} | {f(r['menang'], 0)} | {f(r['purata'], 2)} | "
                 f"{f(r['hari'], 0)} | {f(r['terbuka_purata'], 2)} | {r['tutup_henti']} | {f(r['purata_henti'], 2)} | "
                 f"{f(r['j_menang'], 0)} | {f(r['j_purata'], 2)} | {f(r['j_hari'], 0)} |")
    open(os.path.join(LEJAR, 'RINGKASAN.md'), 'w').write('\n'.join(L) + '\n')
    print(f"ringkasan: {len(rows)} kaedah, {len(T)} tutup, {len(O)} terbuka")


def cmd_banding(a):
    """Fasa 1: banding Papertrade C (claude*.csv, isyarat >= mula lejar) dengan lejar bagi kunci kaedah+saham+tarikh_isyarat
    -> lejar/BANDING_C.md. Beza dijangka: harga (Moomoo lawan yfinance), had 10 sekaedah dan keutamaan 431 dalam C."""
    st = json.load(open(os.path.join(LEJAR, 'status.json'))) if os.path.exists(os.path.join(LEJAR, 'status.json')) else {}
    mula = st.get('mula')
    if not mula:
        print('lejar belum bermula'); return
    C = pd.concat([pd.read_csv(f, dtype=str, keep_default_na=False) for f in sorted(glob.glob(os.path.join(BS2, 'papertrade', 'claude*.csv')))])
    C = C[(C.tidak_dibeli != 'True') & (C.tidak_sah != 'True') & (C.harga_beli != '') & (C.tarikh_isyarat >= mula)]
    T, O = semua_posisi(); P = pd.concat([T, O], ignore_index=True).fillna('')
    lk = pd.concat([baca(f, L_LANGKAU) for f in sorted(glob.glob(os.path.join(LEJAR, 'langkau', '*.csv')))] or [pd.DataFrame(columns=L_LANGKAU)])
    isy = pd.concat([pd.read_csv(f, dtype=str, keep_default_na=False) for f in sorted(glob.glob(os.path.join(LEJAR, 'isyarat', '*.csv.gz')))]
                    or [pd.DataFrame(columns=L_ISYARAT)])
    kc = list(zip(C.id_kaedah, C.saham, C.tarikh_isyarat))
    kp = {k: r for k, r in zip(zip(P.id_kaedah, P.saham, P.tarikh_isyarat), P.to_dict('records'))}
    kl = {k: s for k, s in zip(zip(lk.id_kaedah, lk.saham, lk.tarikh_isyarat), lk.sebab)}
    ki = {k: d for k, d in zip(zip(isy.kaedah, isy.saham, isy.sesi), isy.dipegang)}
    sama, beza_harga, keluar_sama, keluar_beza, tiada = 0, [], 0, [], {}
    for (mid, t, ti), (_, c) in zip(kc, C.iterrows()):
        p = kp.get((mid, t, ti))
        if p is None:
            s = kl.get((mid, t, ti)) or ('isyarat ada, dipegang lejar' if ki.get((mid, t, ti)) == 'True' else
                                         'isyarat ada, belum diproses' if (mid, t, ti) in ki else 'tiada isyarat dalam lejar')
            tiada[s] = tiada.get(s, 0) + 1; continue
        sama += 1
        hb = float(c.harga_beli) / float(p['harga_beli']) - 1
        if abs(hb) > 0.005: beza_harga.append(f"{mid} {t} {ti}: C {c.harga_beli} / lejar {p['harga_beli']} ({hb * 100:+.2f}%)")
        ck = c.keluar == 'True'; pk = bool(p.get('tarikh_keluar'))
        if ck == pk and (not ck or c.tarikh_keluar == p['tarikh_keluar']): keluar_sama += 1
        else: keluar_beza.append(f"{mid} {t} {ti}: C {'keluar ' + c.tarikh_keluar if ck else 'terbuka'} / lejar "
                                 f"{('keluar ' + p['tarikh_keluar'] + ' ' + str(p['sebab_keluar'])) if pk else 'terbuka'}")
    L = ['# Banding Papertrade C dengan Lejar Penuh (fasa 1)', '',
         f"Dijana oleh `standard/lejar.py banding`. Lejar bermula {mula}; sesi terakhir {st.get('sesi_terakhir')}. "
         'Kunci: kaedah + saham + tarikh_isyarat. Beza dijangka: sumber harga (C: Moomoo; lejar: yfinance), had 10 sekaedah dan '
         'keutamaan 431 dalam C (lejar membeli semua isyarat).', '',
         f"- Posisi C (isyarat >= {mula}): {len(C)}; ada dalam lejar: {sama}; tiada: {len(C) - sama} {tiada}",
         f"- Posisi lejar: {len(P)} (C hanya {len(C)}; lejar {len(P) / max(len(C), 1):.1f}×)",
         f"- Harga beli berbeza > 0.5%: {len(beza_harga)} daripada {sama}",
         f"- Status keluar sama: {keluar_sama} daripada {sama}; berbeza: {len(keluar_beza)}", '']
    if beza_harga: L += ['## Harga beli berbeza > 0.5%', ''] + [f'- {x}' for x in beza_harga[:60]] + ['']
    if keluar_beza: L += ['## Status keluar berbeza', ''] + [f'- {x}' for x in keluar_beza[:80]] + ['']
    open(os.path.join(LEJAR, 'BANDING_C.md'), 'w').write('\n'.join(L))
    print(f'banding: C {len(C)}, sama {sama}, harga beza {len(beza_harga)}, keluar beza {len(keluar_beza)}, tiada {tiada}')


def main():
    p = argparse.ArgumentParser(); s = p.add_subparsers(dest='cmd', required=True)
    x = s.add_parser('banding'); x.set_defaults(f=cmd_banding)
    x = s.add_parser('stor'); x.set_defaults(f=cmd_stor)
    x = s.add_parser('jalan'); x.add_argument('--mula'); x.add_argument('--hingga'); x.add_argument('--proses', type=int, default=4)
    x.add_argument('--hanya'); x.add_argument('--paksa', action='store_true', help='proses walaupun liputan bar < LIPUTAN_MIN')
    x.set_defaults(f=cmd_jalan)
    x = s.add_parser('ringkas'); x.set_defaults(f=cmd_ringkas)
    x = s.add_parser('semak'); x.set_defaults(f=cmd_semak)
    a = p.parse_args(); a.f(a)


if __name__ == '__main__':
    main()
