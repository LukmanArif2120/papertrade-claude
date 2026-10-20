# penganalisis.py — Papan Penganalisis: satu jadual banding semua kaedah aktif, menggabungkan bukti backtest dan data hadapan
# (keputusan pengguna 20 Okt 2026). Tanpa LLM; dijalankan oleh GitHub Actions `analisis.yml` sebaik `lejar.yml` siap.
#
#   python3 BacktestShariah2/standard/penganalisis.py [--kini YYYY-MM-DD]
#   -> BacktestShariah2/laporan/PENGANALISIS.md, BacktestShariah2/data/analisis/papan.json (= dokumen db dashboard analisis/papan)
#
# Sumber bukti setiap kaedah (varian aktif = katalog_kaedah.json varian_kod):
#   1. Backtest dalam sampel set 431 (data/registry_M_gabung.csv): asas jangkaan, DIPOTONG kerana dipilih atas data sama.
#   2. Tiga semakan luar sampel, setiap satu yang lulus menambah 25% kepercayaan pada angka backtest (asas 25%):
#      S1–S4 (registry; varian sama atasi EW dalam >= 3/4 subset), WFO W01 (WFO/data/hasil; luar sampel 2023–2026, CAGR > EW
#      423 tempoh sama) dan AUTOTUNE A01 (AUTOTUNE/hasil/papan.json; 2000 saham AS, luar sampel 2013–2024, CAGR > SPY dalam
#      kumpulan A dan B).
#   3. Data hadapan: Lejar Penuh (semua isyarat, seluruh alam Shariah) + kohort Papertrade C sebelum Lejar bermula (tidak
#      bertindih). Hanya posisi MATANG dikira (dibeli >= maks(14 hari, 1.5 x hari pegang backtest) lalu; tutup = untung akhir,
#      terbuka = untung semasa) supaya bias "tutup awal kebanyakannya kena henti" tidak masuk (sama seperti WFO/kod/analisis_sebenar.py).
#      Papertrade C selepas Lejar bermula = isyarat sama dengan Lejar, jadi dipapar sebagai semakan sahaja (tidak dikira dua kali).
# Skor (purata pulangan bersih setiap dagangan, %) = (n0 x jangkaan backtest dipotong + n x purata matang) / (n0 + n); julat 95%
# = skor ± 1.96 x SD / sqrt(n0 + n), n0 = 1 / (1/N0 + 1/n backtest) (backtest kecil diberi berat kurang). Skor sebulan = skor / hari pegang backtest x 21. Swing = purata pegang backtest 3–30 hari.
import argparse, glob, json, math, os, re
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
REPO = os.path.dirname(BS2)
KATALOG = os.path.join(HERE, 'katalog_kaedah.json')
REGISTRY = os.path.join(BS2, 'data', 'registry_M_gabung.csv')
WFO_HASIL = os.path.join(REPO, 'WFO', 'data', 'hasil')
WFO_LAPORAN = os.path.join(REPO, 'WFO', 'laporan', 'W01_LAPORAN.md')
AUTOTUNE = os.path.join(REPO, 'AUTOTUNE', 'hasil', 'papan.json')
LEJAR = os.path.join(BS2, 'lejar')
PT = os.path.join(BS2, 'papertrade')
TERKINI = os.path.join(BS2, 'data', 'harga', 'terkini.csv')
INDEKS = os.path.join(REPO, 'data_mentah', 'index_benchmark.csv')
SLOT = os.path.join(BS2, 'portfolio_slot')
OUT_MD = os.path.join(BS2, 'laporan', 'PENGANALISIS.md')
OUT_JSON = os.path.join(BS2, 'data', 'analisis', 'papan.json')

N0 = 30                 # berat maksimum backtest = 30 dagangan hadapan setara (dikurangkan jika dagangan backtest sedikit)
ASAS_KEKAL = 0.25       # pecahan jangkaan backtest dalam sampel yang dikekalkan tanpa semakan luar sampel lulus
TAMBAH_KEKAL = 0.25     # tambahan bagi setiap semakan luar sampel yang lulus (3 semakan -> 100%)
SWING = (3, 30)         # purata hari pegang backtest bagi kaedah swing (keputusan pengguna 20 Okt 2026)
N_MIN = 20              # posisi matang minimum sebelum status dinilai (tugasan_v3 §7: 20 dagangan)
N_AMARAN = 10           # posisi matang minimum bagi AMARAN awal
N_BT_MIN = 100          # dagangan backtest minimum untuk diberi nombor kedudukan (sampel kecil disusun di hujung)
UMUR_MIN = 14           # hari kalendar minimum sebelum posisi dikira matang
SD_MIN = 5.0            # SD minimum setiap dagangan (%)
KOS = 0.001             # kos enjin v1.2 setiap belah
HARI_BULAN = 21
TEMPOH_IS = ('2019-11-01', '2026-10-02')
STATUS = ['KUAT', 'PERHATI', 'LEMAH', 'AMARAN', 'BELUM CUKUP']
B = lambda v: str(v).strip().lower() == 'true'


def nombor(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) or math.isinf(v) else v


def bulat(x, p=2):
    v = nombor(x)
    return None if v is None else round(v, p)


def bersih(untung_pct):
    """Untung kasar % -> pulangan bersih % dengan kos enjin v1.2 (0.1% setiap belah), sama seperti registry."""
    return ((1 + untung_pct / 100) * (1 - KOS) / (1 + KOS) - 1) * 100


def umur_matang(hari_bt):
    """Hari kalendar sebelum posisi dikira matang: maks(14, 1.5 x hari dagangan pegang backtest x 7/5)."""
    h = nombor(hari_bt) or 10
    return max(UMUR_MIN, int(math.ceil(1.5 * h * 7 / 5)))


# ---------------------------------------------------------------- backtest
def muat_katalog(path=KATALOG):
    return [(r['id'], r.get('nama', ''), r.get('varian_kod') or r.get('varian', '')) for r in json.load(open(path, encoding='utf-8'))['rows']]


def muat_registry(varian, path=REGISTRY):
    """{id: dict(baris 431 varian aktif + subset_menang)}; subset_menang = bil. subset S1–S4 (varian sama) yang atasi EW."""
    r = pd.read_csv(path)
    r = r[[varian.get(i) == v for i, v in zip(r['id'], r['varian'])]]
    out = {}
    for mid, g in r.groupby('id'):
        a = g[g['set'].astype(str) == '431']
        if not len(a):
            continue
        x = a.iloc[0]
        s = g[g['set'].astype(str).isin(['S1', 'S2', 'S3', 'S4'])]
        out[mid] = dict(keputusan=x['keputusan'], skor=nombor(x['skor']), cagr=nombor(x['cagr']), mdd=nombor(x['mdd']),
                        win=nombor(x['win']), avg=nombor(x['avg']), avgwin=nombor(x['avgwin']), avgloss=nombor(x['avgloss']),
                        days=nombor(x['days']), n=int(x['n']) if nombor(x['n']) is not None else 0, hit10=nombor(x['hit10']),
                        setahun=nombor(x['dagangan_setahun']),
                        ew=nombor(x['ew_cagr']), subset_n=int(len(s)),
                        subset_menang=int(sum(B(v) for v in s['menang_ew'])))
    return out


def sd_backtest(r):
    """SD pulangan setiap dagangan (%) daripada kadar menang, purata menang dan purata rugi (anggaran bawah; min SD_MIN)."""
    w, aw, al, av = (r.get(k) for k in ('win', 'avgwin', 'avgloss', 'avg'))
    if None in (w, aw, al, av):
        return SD_MIN
    v = w * aw ** 2 + (1 - w) * al ** 2 - av ** 2
    return max(SD_MIN, math.sqrt(max(v, 0)) * 100)


def muat_wfo(hasil=WFO_HASIL, laporan=WFO_LAPORAN):
    """{id: dict(cagr, mdd, win, avg, hari, n, ew, dsr, keputusan)} — WFO luar sampel 2023–2026 (W01)."""
    lap = {}
    if os.path.exists(laporan):
        for l in open(laporan, encoding='utf-8'):
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            if len(c) == 14 and c[0].isdigit() and re.fullmatch(r'M\d+', c[1]):
                lap[c[1]] = dict(dsr=nombor(c[12]), keputusan=c[13])
    out = {}
    for f in glob.glob(os.path.join(hasil, 'M*.json')):
        h = json.load(open(f, encoding='utf-8'))
        if h.get('status') != 'SIAP':
            continue
        o = h.get('oos') or {}
        out[h['id']] = dict(cagr=nombor(o.get('cagr')), mdd=nombor(o.get('mdd')), win=nombor(o.get('win')), avg=nombor(o.get('avg')),
                            hari=nombor(o.get('hari')), n=int(o.get('n') or 0), ew=nombor((h.get('ew') or {}).get('cagr')),
                            spy=nombor((h.get('spy') or {}).get('cagr')), **lap.get(h['id'], dict(dsr=None, keputusan='')))
    return out


def muat_autotune(path=AUTOTUNE):
    """{id: dict(label, cagr_a, spy_a, cagr_b, spy_b, cagr_kunci, spy_kunci, dsr, pbo)} — 2000 saham AS (A01)."""
    if not os.path.exists(path):
        return {}
    k = ('label', 'cagr_a', 'spy_a', 'mdd_a', 'cagr_b', 'spy_b', 'cagr_kunci', 'spy_kunci', 'dsr', 'pbo')
    return {r['id']: {x: r.get(x) for x in k} for r in json.load(open(path, encoding='utf-8')).get('kaedah', [])}


def semakan(reg, wfo, at):
    """Tiga semakan luar sampel: (subset, wfo, autotune) masing-masing True/False/None (tiada data)."""
    s = (reg['subset_menang'] >= 3) if reg and reg.get('subset_n') else None
    w = (wfo['cagr'] > wfo['ew']) if wfo and wfo.get('cagr') is not None and wfo.get('ew') is not None else None
    a = None
    if at and None not in (nombor(at.get('cagr_a')), nombor(at.get('spy_a')), nombor(at.get('cagr_b')), nombor(at.get('spy_b'))):
        a = at['cagr_a'] > at['spy_a'] and at['cagr_b'] > at['spy_b']
    return s, w, a


# ---------------------------------------------------------------- hadapan
def harga_akhir(path=TERKINI):
    """{ticker: tutup terakhir} dan tarikh data terkini (YYYY-MM-DD) daripada data/harga/terkini.csv."""
    if not os.path.exists(path):
        return {}, None
    d = pd.read_csv(path, usecols=['ticker', 'date', 'close'], dtype={'date': str})
    d = d.sort_values(['ticker', 'date'])
    akhir = d.groupby('ticker').tail(1)
    t = d['date'].max()
    return dict(zip(akhir.ticker, akhir.close.astype(float))), f'{t[:4]}-{t[4:6]}-{t[6:8]}'


def muat_lejar(akhir, lejar=LEJAR):
    """Posisi Lejar Penuh: id, saham, tarikh_isyarat, tarikh_beli, tutup1, hasil1 (bersih %), hasil2 (lorong 2, kasar %)."""
    f = sorted(glob.glob(os.path.join(lejar, 'tutup', '*.csv'))) + [os.path.join(lejar, 'terbuka.csv')]
    d = [pd.read_csv(p, dtype=str, keep_default_na=False) for p in f if os.path.exists(p)]
    if not d:
        return pd.DataFrame(columns=['id', 'saham', 'tarikh_isyarat', 'tarikh_beli', 'tutup1', 'hasil1', 'hasil2', 'sumber'])
    d = pd.concat(d, ignore_index=True)
    rows = []
    for r in d.itertuples(index=False):
        hb = nombor(r.harga_beli)
        kini = akhir.get(r.saham)
        semasa = (kini / hb - 1) * 100 if hb and kini else None
        t1 = r.tarikh_keluar != ''
        h1 = (nombor(r.pulangan) * 100 if nombor(r.pulangan) is not None else bersih(nombor(r.untung_pct))) if t1 else \
            (bersih(semasa) if semasa is not None else None)
        h2 = nombor(r.untung_henti_pct) if B(r.keluar_henti) else semasa
        rows.append(dict(id=r.id_kaedah, saham=r.saham, tarikh_isyarat=r.tarikh_isyarat, tarikh_beli=r.tarikh_beli, tutup1=t1,
                         hasil1=h1, hasil2=h2, sumber='lejar'))
    return pd.DataFrame(rows)


def muat_c(pt=PT):
    """Posisi sah Papertrade C (semua claude*.csv): id, saham, tarikh_isyarat, tarikh_beli, tutup1, hasil1 (bersih %), hasil2."""
    f = sorted(glob.glob(os.path.join(pt, 'claude*.csv')))
    if not f:
        return pd.DataFrame(columns=['id', 'saham', 'tarikh_isyarat', 'tarikh_beli', 'tutup1', 'hasil1', 'hasil2', 'sumber'])
    d = pd.concat([pd.read_csv(p, dtype=str, keep_default_na=False) for p in f], ignore_index=True)
    for k in ('tidak_sah', 'tidak_dibeli', 'keluar_henti'):
        d[k] = d[k].map(B) if k in d else False
    d = d[~d.tidak_sah & ~d.tidak_dibeli & (d.harga_beli != '') & (d.tarikh_beli != '')]
    rows = []
    for r in d.itertuples(index=False):
        t1 = B(r.keluar)
        g = nombor(r.untung_akhir_pct) if t1 else nombor(r.untung_pct)
        h2 = nombor(getattr(r, 'untung_henti_pct', None)) if r.keluar_henti else nombor(r.untung_pct)
        rows.append(dict(id=r.id_kaedah or r.kaedah, saham=r.saham, tarikh_isyarat=getattr(r, 'tarikh_isyarat', ''), tarikh_beli=r.tarikh_beli,
                         tutup1=t1, hasil1=bersih(g) if g is not None else None, hasil2=h2, sumber='C'))
    return pd.DataFrame(rows)


def gabung_hadapan(L, C):
    """Bukti hadapan = Lejar Penuh + kohort C sebelum belian pertama Lejar (C selepas itu = isyarat sama; semakan sahaja)."""
    mula = L.tarikh_beli.min() if len(L) else None
    pra = C[C.tarikh_beli < mula] if mula else C
    return pd.concat([L, pra], ignore_index=True), mula


def ringkas_hadapan(P, hari_bt, kini):
    """Statistik hadapan satu kaedah: semua posisi, posisi matang (bukti), lorong 2 matang dan tarikh 20 posisi matang."""
    umur = umur_matang(hari_bt)
    out = dict(posisi=int(len(P)), tutup=int(P.tutup1.sum()) if len(P) else 0, umur_hari=umur,
               matang=0, purata=None, menang=None, sd=None, purata_l2=None, matang_mula=None, matang_20=None)
    if not len(P):
        return out
    tb = pd.to_datetime(P.tarikh_beli)
    had = pd.Timestamp(kini) - pd.Timedelta(days=umur)
    M = P[(tb <= had).values & P.hasil1.notna().values]
    s = sorted(tb)
    out['matang_mula'] = str((s[0] + pd.Timedelta(days=umur)).date())
    if len(s) >= N_MIN:
        out['matang_20'] = str((s[N_MIN - 1] + pd.Timedelta(days=umur)).date())
    if len(M):
        x = M.hasil1.astype(float)
        out.update(matang=int(len(M)), purata=float(x.mean()), menang=float((x > 0).mean()),
                   sd=float(x.std(ddof=1)) if len(M) > 1 else None)
        y = M.hasil2.dropna().astype(float)
        out['purata_l2'] = float(y.mean()) if len(y) else None
    return out


# ---------------------------------------------------------------- skor
def berat_backtest(n_bt):
    """n0 = 1 / (1/N0 + 1/n backtest): varians jangkaan = ketidakpastian model (N0) + ralat sampel backtest (n backtest)."""
    return N0 * n_bt / (N0 + n_bt) if n_bt and n_bt > 0 else 1.0


def skor(mu0, sd0, n, xbar, sdf, n0=N0):
    """Pengecutan normal–normal: (n0 x mu0 + n x xbar) / (n0 + n); SD = SD hadapan jika n >= N_MIN, jika tidak SD backtest."""
    s = sdf if (n >= N_MIN and sdf) else sd0
    s = max(SD_MIN, s or SD_MIN)
    mu = mu0 if not n else (n0 * mu0 + n * xbar) / (n0 + n)
    se = s / math.sqrt(n0 + n)
    return mu, mu - 1.96 * se, mu + 1.96 * se


def status_kaedah(n, xbar, sdf, mu0, lo, hi):
    """AMARAN: >= 10 matang dan purata matang di bawah jangkaan (t < -2). BELUM CUKUP: < 20 matang.
    KUAT: julat 95% skor > 0. LEMAH: julat 95% skor < 0. Selainnya PERHATI."""
    if n >= N_AMARAN and sdf and sdf > 0 and (xbar - mu0) / (sdf / math.sqrt(n)) < -2:
        return 'AMARAN'
    if n < N_MIN:
        return 'BELUM CUKUP'
    return 'KUAT' if lo > 0 else 'LEMAH' if hi < 0 else 'PERHATI'


def analisis(kini=None):
    kat = muat_katalog()
    REG = muat_registry({i: v for i, _, v in kat})
    WF, AT = muat_wfo(), muat_autotune()
    akhir, tarikh_harga = harga_akhir()
    kini = kini or tarikh_harga or datetime.now(timezone.utc).strftime('%Y-%m-%d')
    L, C = muat_lejar(akhir), muat_c()
    H, mula_lejar = gabung_hadapan(L, C)
    Hg = dict(tuple(H.groupby('id'))) if len(H) else {}
    Cg = dict(tuple(C.groupby('id'))) if len(C) else {}
    rows = []
    for mid, nama, var in kat:
        r = REG.get(mid) or {}
        w, a = WF.get(mid), AT.get(mid)
        s_sub, s_wfo, s_at = semakan(r, w, a)
        lulus = sum(bool(x) for x in (s_sub, s_wfo, s_at))
        kekal = ASAS_KEKAL + TAMBAH_KEKAL * lulus
        hari = r.get('days')
        avg_bt = r['avg'] * 100 if r.get('avg') is not None else None
        mu0 = avg_bt * kekal if avg_bt is not None else 0.0
        sd0 = sd_backtest(r)
        hd = ringkas_hadapan(Hg.get(mid, H.iloc[:0]), hari, kini)
        n0 = berat_backtest(r.get('n'))
        mu, lo, hi = skor(mu0, sd0, hd['matang'], hd['purata'] or 0.0, hd['sd'], n0)
        st = status_kaedah(hd['matang'], hd['purata'] or 0.0, hd['sd'], mu0, lo, hi)
        c = Cg.get(mid)
        sebulan = (lambda v: v / hari * HARI_BULAN) if hari else (lambda v: None)
        rows.append(dict(
            id=mid, nama=nama, varian=var, swing=bool(hari is not None and SWING[0] <= hari <= SWING[1]),
            hari=bulat(hari, 1), bt_keputusan=r.get('keputusan'), bt_skor=bulat(r.get('skor'), 1), bt_cagr=bulat(r.get('cagr'), 4),
            bt_mdd=bulat(r.get('mdd'), 4), bt_menang=bulat(r.get('win'), 4), bt_purata=bulat(avg_bt, 2), bt_n=r.get('n'),
            bt_setahun=bulat(r.get('setahun'), 1), n0=bulat(n0, 1),
            subset=f"{r.get('subset_menang', 0)}/{r.get('subset_n', 0)}" if r else None, lulus_subset=s_sub,
            wfo_cagr=bulat(w and w['cagr'], 4), wfo_ew=bulat(w and w['ew'], 4), wfo_mdd=bulat(w and w['mdd'], 4),
            wfo_dsr=bulat(w and w['dsr'], 2), lulus_wfo=s_wfo,
            at_label=a and a.get('label'), at_cagr_a=bulat(a and a.get('cagr_a'), 4), at_cagr_b=bulat(a and a.get('cagr_b'), 4),
            at_spy=bulat(a and a.get('spy_a'), 4), lulus_at=s_at, lulus=lulus, kekal=kekal, jangkaan=bulat(mu0, 2),
            h_posisi=hd['posisi'], h_tutup=hd['tutup'], h_matang=hd['matang'], h_purata=bulat(hd['purata'], 2),
            h_menang=bulat(hd['menang'], 4), h_purata_l2=bulat(hd['purata_l2'], 2), h_umur=hd['umur_hari'],
            matang_mula=hd['matang_mula'], matang_20=hd['matang_20'],
            c_posisi=int(len(c)) if c is not None else 0,
            c_purata=bulat(c.hasil1.dropna().mean(), 2) if c is not None and c.hasil1.notna().any() else None,
            skor=bulat(mu, 2), skor_bawah=bulat(lo, 2), skor_atas=bulat(hi, 2),
            skor_bulan=bulat(sebulan(mu), 2), skor_bulan_bawah=bulat(sebulan(lo), 2), skor_bulan_atas=bulat(sebulan(hi), 2),
            status=st))
    # kedudukan: swing dengan >= N_BT_MIN dagangan backtest (ikut skor sebulan), swing sampel kecil, kemudian bukan swing
    k = lambda r: (-(r['skor_bulan'] if r['skor_bulan'] is not None else -1e9))
    for r in rows:
        r['sampel_kecil'] = (r['bt_n'] or 0) < N_BT_MIN
    sw = sorted([r for r in rows if r['swing'] and not r['sampel_kecil']], key=k)
    kecil = sorted([r for r in rows if r['swing'] and r['sampel_kecil']], key=k)
    lain = sorted([r for r in rows if not r['swing']], key=k)
    for i, r in enumerate(sw, 1):
        r['kedudukan'] = i
    for r in kecil + lain:
        r['kedudukan'] = None
    sw += kecil
    meta = dict(kini=kini, harga_pada=tarikh_harga, mula_lejar=mula_lejar,
                lejar_posisi=int(len(L)), c_posisi=int(len(C)),
                c_pra_lejar=int((C.tarikh_beli < mula_lejar).sum()) if mula_lejar and len(C) else int(len(C)),
                lejar_sesi=_lejar_sesi())
    return sw + lain, meta


def _lejar_sesi():
    try:
        return json.load(open(os.path.join(LEJAR, 'status.json'), encoding='utf-8')).get('sesi_terakhir')
    except (OSError, ValueError):
        return None


# ---------------------------------------------------------------- rujukan
def cagr_indeks(ticker='SPY', mula=TEMPOH_IS[0], akhir=TEMPOH_IS[1], path=INDEKS):
    if not os.path.exists(path):
        return None
    d = pd.read_csv(path, usecols=['ticker', 'date', 'close'], dtype={'date': str})
    d = d[(d.ticker == ticker) & (d.date >= mula.replace('-', '')) & (d.date <= akhir.replace('-', ''))].sort_values('date')
    if len(d) < 2:
        return None
    t = (pd.Timestamp(d.date.iloc[-1]) - pd.Timestamp(d.date.iloc[0])).days / 365.25
    return float((d.close.iloc[-1] / d.close.iloc[0]) ** (1 / t) - 1)


def rujukan(rows, WF=None):
    reg = pd.read_csv(REGISTRY, usecols=['set', 'ew_cagr'])
    ew = reg[reg['set'].astype(str) == '431'].ew_cagr.dropna()
    w = next((r for r in rows if r.get('wfo_ew') is not None), None)
    at = next((r for r in rows if r.get('at_spy') is not None), None)
    out = dict(is_tempoh='1 Nov 2019 – 2 Okt 2026', is_ew=bulat(ew.iloc[0], 4) if len(ew) else None, is_spy=bulat(cagr_indeks(), 4),
               wfo_tempoh='1 Jan 2023 – 2 Okt 2026', wfo_ew=w and w['wfo_ew'], wfo_spy=None,
               at_tempoh='2013 – Sep 2024 (2000 saham AS)', at_spy=at and at['at_spy'], slot=None)
    WF = WF if WF is not None else muat_wfo()
    sp = next((v['spy'] for v in WF.values() if v.get('spy') is not None), None)
    out['wfo_spy'] = bulat(sp, 4)
    try:
        s = {}
        for k in ('RS_10', 'RAWAK_10'):
            e = pd.read_csv(os.path.join(SLOT, f'{k}_ekuiti.csv'))
            s[k] = bulat((e.ekuiti.iloc[-1] - 1) * 100, 2)
            s['spy'] = bulat((e.spy.iloc[-1] - 1) * 100, 2)
            s['mula'], s['akhir'], s['sesi'] = str(e.tarikh.iloc[0]), str(e.tarikh.iloc[-1]), int(len(e))
        out['slot'] = s
    except (OSError, ValueError, KeyError, IndexError):
        pass
    return out


# ---------------------------------------------------------------- penemuan + output
def p(x, d=1):
    return '–' if x is None else f'{x * 100:.{d}f}%'


def sg(x, d=2):
    return '–' if x is None else f'{x:+.{d}f}%'


def tarikh_ms(t):
    if not t:
        return '–'
    d = datetime.strptime(t, '%Y-%m-%d')
    return f"{d.day} {['Jan', 'Feb', 'Mac', 'Apr', 'Mei', 'Jun', 'Jul', 'Ogo', 'Sep', 'Okt', 'Nov', 'Dis'][d.month - 1]} {d.year}"


def penemuan(rows, meta, ruj):
    sw = [r for r in rows if r['swing'] and r['kedudukan']]
    out = []
    if sw:
        t = sw[0]
        out.append(f"Swing teratas ikut skor gabungan: {t['id']} {t['nama']} — {sg(t['skor_bulan'])} sebulan "
                   f"setiap posisi (julat {sg(t['skor_bulan_bawah'])} hingga {sg(t['skor_bulan_atas'])}), {t['lulus']}/3 semakan luar sampel, "
                   f"status {t['status']}; CAGR backtest bersendirian {p(t['bt_cagr'])} ({t['bt_setahun']} dagangan setahun). "
                   'Tiga seterusnya: ' + ', '.join(r['id'] for r in sw[1:4]) + '.')
    dinilai = [r for r in rows if r['h_matang'] >= N_MIN]
    m20 = sorted(r['matang_20'] for r in rows if r['matang_20'])
    if dinilai:
        kuat = [r['id'] for r in dinilai if r['status'] == 'KUAT']
        amaran = [r['id'] for r in rows if r['status'] == 'AMARAN']
        out.append(f"{len(dinilai)} kaedah ada ≥ {N_MIN} posisi hadapan matang; KUAT ({len(kuat)}): {senarai(kuat)}; "
                   f"AMARAN, jauh di bawah jangkaan ({len(amaran)}): {senarai(amaran)}.")
    else:
        mt = sum(r['h_matang'] for r in rows)
        out.append(f"Data hadapan belum matang: {mt} posisi matang daripada {sum(r['h_posisi'] for r in rows)} "
                   f"(Lejar sejak {tarikh_ms(meta['mula_lejar'])}, Papertrade C sejak 8 Okt 2026). Kedudukan kini = backtest dipotong. "
                   f"Kaedah pertama dengan {N_MIN} posisi matang dijangka {tarikh_ms(m20[0]) if m20 else '–'}.")
    n = {k: sum(1 for r in rows if r[f'lulus_{k}']) for k in ('subset', 'wfo', 'at')}
    dua = [r['id'] for r in rows if r['lulus'] >= 2]
    s = ruj.get('slot') or {}
    out.append(f"Ketahanan backtest lemah: lulus S1–S4 {n['subset']}, WFO {n['wfo']}, 2000 saham AS {n['at']} kaedah; "
               f"≥ 2 daripada 3 semakan: {', '.join(dua) if dua else 'tiada'}. "
               + (f"Portfolio 10 slot sejak {tarikh_ms(s.get('mula'))}: RS_10 {sg(s.get('RS_10'))}, RAWAK_10 {sg(s.get('RAWAK_10'))}, "
                  f"SPY {sg(s.get('spy'))}." if s else ''))
    return out


def senarai(ids, had=8):
    return 'tiada' if not ids else ', '.join(ids[:had]) + (f' dan {len(ids) - had} lagi' if len(ids) > had else '')


def tanda(v):
    return '–' if v is None else ('✓' if v else '✗')


def jana_md(rows, meta, ruj, pen, dibina):
    L = ['# Papan Penganalisis — banding semua kaedah (backtest + papertrade)', '',
         f"Dijana {dibina} oleh `standard/penganalisis.py` (GitHub Actions `analisis.yml`, selepas Lejar Penuh). Data harga hingga "
         f"{tarikh_ms(meta['harga_pada'])}; Lejar sesi terakhir {tarikh_ms(meta['lejar_sesi'])}. Rekod analisis sahaja: tiada order, "
         'tiada wang sebenar. Dashboard: tab Analisis (db `analisis/papan`).', '',
         '## 3 penemuan utama', ''] + [f'{i}. {x}' for i, x in enumerate(pen, 1)] + ['',
         '## Cara skor dikira', '',
         f'- Jangkaan backtest = purata pulangan bersih setiap dagangan, set 431 dalam sampel (varian aktif), dikekalkan '
         f'{int(ASAS_KEKAL * 100)}% + {int(TAMBAH_KEKAL * 100)}% bagi setiap semakan luar sampel yang lulus: S1–S4 (atasi EW dalam ≥ 3/4 '
         'subset), WFO (CAGR luar sampel 2023–2026 > EW 423 tempoh sama) dan 2000 saham AS (AUTOTUNE A01: CAGR > SPY dalam kumpulan A dan B).',
         f'- Bukti hadapan = posisi matang Lejar Penuh + kohort Papertrade C sebelum Lejar bermula ({meta["c_pra_lejar"]} posisi). Matang = '
         f'dibeli ≥ maks({UMUR_MIN} hari, 1.5 × hari pegang backtest) lalu; tutup = untung akhir, terbuka = untung semasa (bersih kos 0.1% '
         'setiap belah). Papertrade C selepas Lejar bermula = isyarat sama dengan Lejar: lajur semakan sahaja.',
         f'- Skor = (n0 × jangkaan + n × purata matang) ÷ (n0 + n), n0 = berat backtest (maks {N0}; kurang jika dagangan backtest sedikit). '
         f'Julat 95% = skor ± 1.96 × SD ÷ √(n0 + n). Skor sebulan = skor ÷ hari pegang backtest × {HARI_BULAN}, iaitu untung setiap '
         'posisi jika modal dipusing semula sebaik keluar. Makin banyak posisi matang, makin data sebenar menguasai skor.',
         f'- Status: AMARAN = ≥ {N_AMARAN} matang dan purata matang jauh di bawah jangkaan (t < −2); BELUM CUKUP = < {N_MIN} matang; '
         'KUAT = julat 95% di atas 0; LEMAH = julat 95% di bawah 0; selainnya PERHATI.',
         f'- Swing = purata pegang backtest {SWING[0]}–{SWING[1]} hari dagangan. Kaedah swing dengan < {N_BT_MIN} dagangan backtest '
         '(sampel kecil) tiada nombor kedudukan dan disusun di hujung jadual swing. Kaedah lain disenarai berasingan.', '',
         '## Rujukan', '',
         f"- Backtest dalam sampel ({ruj['is_tempoh']}): EW 431 {p(ruj['is_ew'])}, SPY {p(ruj['is_spy'])} setahun.",
         f"- WFO luar sampel ({ruj['wfo_tempoh']}): EW 423 {p(ruj['wfo_ew'])}, SPY {p(ruj['wfo_spy'])} setahun.",
         f"- AUTOTUNE luar sampel ({ruj['at_tempoh']}): SPY {p(ruj['at_spy'])} setahun."]
    s = ruj.get('slot')
    if s:
        L.append(f"- Portfolio maya 10 slot ({tarikh_ms(s['mula'])} – {tarikh_ms(s['akhir'])}, {s['sesi']} sesi): RS_10 {sg(s['RS_10'])}, "
                 f"RAWAK_10 {sg(s['RAWAK_10'])}, SPY {sg(s['spy'])}. Kajian portfolio: memilih ikut RS pasaran mengatasi memilih ikut kaedah "
                 '(`kajian/KAJIAN_PORTFOLIO.md`).')
    hd = ('| # | Kaedah | Hari | Dagangan/tahun | Backtest 431: CAGR · MDD · menang · purata | S1–S4 · WFO · 2000 AS | Jangkaan % | '
          'Hadapan: posisi · matang · purata · menang | Lorong 2 % | C: posisi · purata | Skor % [julat 95%] | Skor sebulan % | Status | 20 matang |')
    sep = '|' + '---|' * 14

    def baris(r):
        return (f"| {r['kedudukan'] or '–'} | {r['id']} {r['nama']} | {r['hari'] if r['hari'] is not None else '–'} | "
                f"{r['bt_setahun'] if r['bt_setahun'] is not None else '–'} | "
                f"{p(r['bt_cagr'])} · {p(r['bt_mdd'])} · {p(r['bt_menang'], 0)} · {sg(r['bt_purata'])} | "
                f"{tanda(r['lulus_subset'])} {r['subset'] or ''} · {tanda(r['lulus_wfo'])} {p(r['wfo_cagr'])} · {tanda(r['lulus_at'])} "
                f"{p(r['at_cagr_a'])}/{p(r['at_cagr_b'])} | {sg(r['jangkaan'])} | {r['h_posisi']} · {r['h_matang']} · {sg(r['h_purata'])} · "
                f"{p(r['h_menang'], 0)} | {sg(r['h_purata_l2'])} | {r['c_posisi']} · {sg(r['c_purata'])} | "
                f"{sg(r['skor'])} [{sg(r['skor_bawah'])}, {sg(r['skor_atas'])}] | {sg(r['skor_bulan'])} | {r['status']} | "
                f"{tarikh_ms(r['matang_20'])} |")
    sw = [r for r in rows if r['swing']]
    lain = [r for r in rows if not r['swing']]
    L += ['', f'## Kaedah swing ({SWING[0]}–{SWING[1]} hari), susun ikut skor sebulan ({len(sw)} kaedah)', '', hd, sep] + [baris(r) for r in sw]
    L += ['', f'## Bukan swing (pegang < {SWING[0]} atau > {SWING[1]} hari; {len(lain)} kaedah)', '', hd, sep] + [baris(r) for r in lain]
    L += ['', '## Batasan', '',
          '- Set 431 ialah senarai Shariah hari ini (bias kemandirian); kaedah dibina dan ditapis atas data 2019–2026. Sebab itu jangkaan '
          'backtest dipotong dan semakan 2000 saham AS diberi berat.',
          '- SD backtest dianggar daripada kadar menang, purata menang dan purata rugi (anggaran bawah), jadi julat sebelum data hadapan '
          'matang lebih sempit daripada sebenar.',
          '- Skor sebulan menganggap modal dipusing semula sebaik keluar; kaedah dengan isyarat jarang tidak menggunakan modal sepenuhnya '
          '(lihat CAGR backtest).',
          '- Moomoo lama (1–8 Okt 2026, varian v1) tidak dikira.']
    return '\n'.join(L) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--kini', help='tarikh data (YYYY-MM-DD); lalai = tarikh harga terkini')
    ap.add_argument('--md', default=OUT_MD); ap.add_argument('--json', default=OUT_JSON)
    a = ap.parse_args(argv)
    rows, meta = analisis(a.kini)
    ruj = rujukan(rows)
    pen = penemuan(rows, meta, ruj)
    dibina = (datetime.now(timezone.utc) + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M') + ' MYT'
    os.makedirs(os.path.dirname(a.json), exist_ok=True)
    doc = dict(dibina=dibina, **meta, parameter=dict(n0_maks=N0, asas_kekal=ASAS_KEKAL, tambah_kekal=TAMBAH_KEKAL, swing=list(SWING),
                                                    n_min=N_MIN, n_amaran=N_AMARAN, umur_min=UMUR_MIN, hari_bulan=HARI_BULAN),
               penemuan=pen, rujukan=ruj, rows=rows,
               nota='Papan Penganalisis (standard/penganalisis.py). Skor = purata pulangan bersih setiap dagangan (%) gabungan backtest '
                    'dipotong dan posisi hadapan matang. Rekod analisis sahaja.')
    try:   # kandungan sama (hanya masa dibina berbeza) -> fail tidak ditulis semula, jadi tiada commit
        lama = json.load(open(a.json, encoding='utf-8'))
        if {k: v for k, v in lama.items() if k != 'dibina'} == json.loads(json.dumps({k: v for k, v in doc.items() if k != 'dibina'})) \
                and os.path.exists(a.md):
            print(f"penganalisis: tiada perubahan sejak {lama.get('dibina')}"); return
    except (OSError, ValueError):
        pass
    open(a.json, 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False, separators=(',', ':')))
    open(a.md, 'w', encoding='utf-8').write(jana_md(rows, meta, ruj, pen, dibina))
    print(f"penganalisis: {len(rows)} kaedah ({sum(r['swing'] for r in rows)} swing), "
          f"{sum(r['h_matang'] for r in rows)} posisi matang; {a.md}, {a.json} ({os.path.getsize(a.json)} bait)")


if __name__ == '__main__':
    main()
