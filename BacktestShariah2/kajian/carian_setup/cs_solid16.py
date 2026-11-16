# cs_solid16.py — pusingan CS16 "UJIAN SOLID" (SPEC_CARIAN_SETUP.md pindaan 16 Nov 2026 (z); permintaan pengguna: "beberapa
# methods F yang betul betul solid ... 5 % seminggu, 10 % seminggu, 10 % dua minggu"; "abaikan dahulu saham shariah").
# Bukan carian: peraturan masuk tidak diubah, tiada kod F baharu. Setiap setup dinilai pada kumpulan B dengan mekanik senarai
# utama (satu posisi setiap saham, jual hari ke-20, stop loss 4xATR14, asas = saham rawak hari sama x tercile ATR):
#   tiga angka pengguna (m5, m10, m10d) + takrif SOLID S1-S7 + "boleh dibuat" S8 (tarikh laporan kewangan DITEKA) + senarai
#   pendek yang berbeza S9; kawalan rawak K1 dan "kawalan laporan kewangan" K2; "prasyarat sahaja" sebagai rujukan.
#   python3 cs_solid16.py kira <kerja>   -> <kerja>/cs16_solid.pkl
#   python3 cs_solid16.py lapor <kerja>  -> hasil/CS16/SOLID.md, solid.csv.gz, kawalan.csv, prasyarat.csv, bacaan.json
import json
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd
from numba import njit, prange

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_cari as cari  # noqa: E402
import cs_cari12 as c12  # noqa: E402
import cs_cs05 as c5  # noqa: E402
import cs_keluar7 as k7  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_prasyarat as pr  # noqa: E402
import cs_semak11 as s11  # noqa: E402
import cs_tala7 as t7  # noqa: E402
import cs_teras as teras  # noqa: E402

PUS = 'CS16'
S_HENTI = k7.HENTI.index('4xATR14')
LABEL = ('m5', 'terus', 'm10', 'm10d', 'p5', 'p10', 'p10d')         # p* = "pernah capai" (maklumat)
MIN_N, MIN_TAHUN, MIN_K3 = 300, 10, 20                              # S1
KL_MIN = 0.03                                                       # S2
THN_MIN_N, THN_MIN_BIL, THN_BAHAGIAN = 15, 8, 0.70                  # S3
BUANG_HARI, KL_BAKI = 10, 0.01                                      # S5
ADIK_MAKS, ADIK_MIN_N, ADIK_MIN_BIL, ADIK_BAHAGIAN = 30, 100, 3, 0.60   # S6
TAMBAH_MIN = 0.01                                                   # S7
RAMAL_TAHUN, RAMAL_SUKU, S8_BAHAGIAN = 364, 91, 0.5                 # S8
JACCARD = 0.50                                                      # S9
B1_MAKS, B2_BEZA = 0.05, 0.10                                       # bacaan dikunci
Q_F01 = lapis.KUMPULAN.index('QF01 earnings dalam 1-5 sesi akan datang')
Q_F04 = lapis.KUMPULAN.index('QF04 tiada earnings dalam 20 sesi akan datang')
Q_TARIKH = (Q_F01, Q_F04)                                           # prasyarat yang memakai tarikh laporan AKAN DATANG
F_ = lambda kerja: os.path.join(kerja, 'cs16_solid.pkl')
HASIL = os.path.join(SINI, 'hasil', PUS)
CS13 = os.path.join(SINI, 'hasil', 'CS13')


# ---------- label dan asas ----------
@njit(parallel=True, cache=True)
def label15(ev, o, c):
    """[m10, m10d, p5, p10, p10d] setiap isyarat (P = buka sesi 1): tutup sesi 5 >= +10 %; tutup sesi 10 >= +10 %;
    mana-mana tutup sesi 1-5 >= +5 %; sesi 1-5 >= +10 %; sesi 1-10 >= +10 %."""
    out = np.zeros((ev.shape[0], 5), np.float32)
    for k in prange(ev.shape[0]):
        e = ev[k] + 1
        P = o[e]
        m5 = c[e]
        for d in range(1, 5):
            if c[e + d] > m5:
                m5 = c[e + d]
        m10 = m5
        for d in range(5, 10):
            if c[e + d] > m10:
                m10 = c[e + d]
        if c[e + 4] >= P * 1.10:
            out[k, 0] = 1.0
        if c[e + 9] >= P * 1.10:
            out[k, 1] = 1.0
        if m5 >= P * 1.05:
            out[k, 2] = 1.0
        if m5 >= P * 1.10:
            out[k, 3] = 1.0
        if m10 >= P * 1.10:
            out[k, 4] = 1.0
    return out


def asas15(pan):
    """(Lab[bar, 7], As[bar, 7]) susunan LABEL: m5 dan terus daripada cs_semak11.asas (sama seperti senarai utama), lima label
    baharu dengan asas yang sama (hari x tercile ATR % antara bar layak)."""
    L11, A11 = s11.asas(pan)
    sah = np.flatnonzero(pan['sah'])
    Lb = label15(sah, pan['o'], pan['c'])
    hari = pan['hari'][sah]
    pct = pd.Series(pan['atr'][sah] / pan['c'][sah]).groupby(hari).rank(pct=True).to_numpy()
    g = hari * 3 + np.minimum((pct * 3).astype(np.int64), 2)
    bil = np.maximum(np.bincount(g), 1)
    N = len(pan['c'])
    Lab, As = np.zeros((N, 7), np.float32), np.zeros((N, 7), np.float32)
    Lab[:, :2], As[:, :2] = L11[:, :2], A11[:, :2]
    Lab[sah, 2:] = Lb
    As[sah, 2:] = np.stack([np.bincount(g, Lb[:, j]) / bil for j in range(5)], 1)[g]
    return Lab, As


def ukur15(pan, Lab, As, ev):
    """Statistik belian satu peraturan (satu posisi setiap saham, jual hari ke-20 + stop loss 4xATR14) -> (dict, bar beli)."""
    ev = np.ascontiguousarray(ev, dtype=np.int64)
    if not len(ev):
        return dict(n=0, tahun=0), ev
    R, sk, st = s11.jual20(ev, pan['o'], pan['l'], pan['c'], pan['atr'], S_HENTI)
    amb = teras.satu_posisi(ev, sk, pan['tid'])
    e, R = ev[amb], R[amb]
    tp, thn, hari = pan['tempoh'][e], pan['tarikh'][e] // 10000, pan['hari'][e]
    d = dict(n=int(len(e)), tahun=int(len(np.unique(thn))), menang=float((R > 0).mean()), purata=float(R.mean()),
             rugi8=float((R <= -0.08).mean()))
    for j, nm in enumerate(LABEL):
        d[nm], d['a_' + nm] = float(Lab[e, j].mean()), float(As[e, j].mean())
        d['kl_' + nm] = d[nm] - d['a_' + nm]
    x = (Lab[e, 1] - As[e, 1]).astype(np.float64)                     # sumbangan setiap belian kepada kelebihan `terus`
    for p in range(3):
        q = tp == p
        d[f'n_K{p + 1}'] = int(q.sum())
        d[f'kl_K{p + 1}'] = float((Lab[e[q], 1] - As[e[q], 1]).mean()) if q.any() else float('nan')
    _, inv = np.unique(thn, return_inverse=True)
    bil, jum = np.bincount(inv), np.bincount(inv, x)
    cukup = bil >= THN_MIN_N
    d['thn_bil'], d['thn_pos'] = int(cukup.sum()), int((jum[cukup] > 0).sum())
    _, invh = np.unique(hari, return_inverse=True)
    bh, jh = np.bincount(invh), np.bincount(invh, x)
    buang = np.argsort(-jh, kind='stable')[:BUANG_HARI]
    baki = len(e) - int(bh[buang].sum())
    d['kl_baki'] = float((x.sum() - jh[buang].sum()) / baki) if baki > 0 else float('nan')
    return d, e


def syarat(d):
    """S1-S5 daripada statistik satu peraturan (NaN = gagal)."""
    g = lambda k: d.get(k, float('nan'))
    pos = lambda v: v == v and v > 0
    s1 = bool(d.get('n', 0) >= MIN_N and d.get('tahun', 0) >= MIN_TAHUN and d.get('n_K3', 0) >= MIN_K3)
    s2 = bool(g('kl_terus') == g('kl_terus') and g('kl_terus') >= KL_MIN and all(pos(g(f'kl_K{p}')) for p in (1, 2, 3)))
    s3 = bool(d.get('thn_bil', 0) >= THN_MIN_BIL and d.get('thn_pos', 0) >= THN_BAHAGIAN * d.get('thn_bil', 0))
    s4 = bool(pos(g('kl_m5')) and pos(g('kl_m10')) and pos(g('kl_m10d')))
    s5 = bool(g('kl_baki') == g('kl_baki') and g('kl_baki') >= KL_BAKI)
    return dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5)


# ---------- tarikh laporan kewangan yang diteka (S8) ----------
def peristiwa_earnings(pan):
    """dict indeks saham -> indeks bar (dalam saham) setiap laporan kewangan; logik sama seperti cs_prasyarat.earnings."""
    e = pd.read_csv(os.path.join(pr.BS2, 'data', 'sec', 'earnings_8k.csv'), usecols=['saham', 'tarikh_fail', 'masa_terima', 'items'])
    e = e[e['items'].astype(str).str.contains('2.02', regex=False)]
    e['d'] = e.tarikh_fail.str.replace('-', '').astype(int)
    e['lewat'] = pd.to_datetime(e.masa_terima, errors='coerce', utc=True).dt.hour >= 20
    eg = dict(tuple(e.groupby('saham')))
    out = {}
    for t, nama in enumerate(pan['ticker']):
        if nama not in eg:
            continue
        a, b = pan['mula'][t], pan['mula'][t + 1]
        d, g = pan['tarikh'][a:b], eg[nama]
        ev = np.where(g.lewat.to_numpy(), np.searchsorted(d, g.d.to_numpy(), 'right'), np.searchsorted(d, g.d.to_numpy(), 'left'))
        ev = np.unique(ev[(ev > 0) & (ev < b - a)])
        if len(ev):
            out[t] = ev
    return out


def ramal_indeks(d, ev):
    """Indeks bar yang DITEKA bagi setiap laporan (−1 = tiada tekaan): laporan suku sama tahun lepas + 364 hari; jika belum
    ada empat laporan terdahulu, laporan terakhir + 91 hari. Hanya maklumat sebelum laporan itu dipakai."""
    hari = pd.to_datetime(pd.Series(d[ev].astype(str)), format='%Y%m%d')
    p = np.full(len(ev), -1, np.int64)
    for k in range(1, len(ev)):
        t = hari.iloc[k - 4] + pd.Timedelta(days=RAMAL_TAHUN) if k >= 4 else hari.iloc[k - 1] + pd.Timedelta(days=RAMAL_SUKU)
        p[k] = np.searchsorted(d, int(t.strftime('%Y%m%d')), 'left')
    return p


def ramal_earnings(pan):
    """(baris tekaan {Q_F01: bool[N], Q_F04: bool[N]}, baris sebenar yang dibina semula {…}, ketepatan)."""
    N = len(pan['c'])
    R = {Q_F01: np.zeros(N, bool), Q_F04: np.zeros(N, bool)}
    S = {Q_F01: np.zeros(N, bool), Q_F04: np.zeros(N, bool)}
    beza = []
    for t, ev in peristiwa_earnings(pan).items():
        a, b = pan['mula'][t], pan['mula'][t + 1]
        T, d = b - a, pan['tarikh'][a:b]
        i = np.arange(T)
        kn = np.searchsorted(ev, i, 'right')
        ada_n = kn < len(ev)
        kk = np.minimum(kn, len(ev) - 1)
        hingga = np.where(ada_n, ev[kk] - i, 10 ** 6)
        S[Q_F01][a:b] = (hingga >= 1) & (hingga <= 5)
        S[Q_F04][a:b] = ada_n & (hingga > 20)
        p = ramal_indeks(d, ev)
        ada_p = ada_n & (p[kk] >= 0)
        hr = np.where(ada_p, p[kk] - i, 10 ** 6)
        R[Q_F01][a:b] = ada_p & (hr >= 1) & (hr <= 5)
        R[Q_F04][a:b] = ada_p & (hr > 20) & (hr < 10 ** 6)
        beza.append((p - ev)[p >= 0])
    z = np.concatenate(beza) if beza else np.zeros(0)
    s1, r1 = S[Q_F01] & pan['sah'], R[Q_F01] & pan['sah']
    tepat = dict(n=int(len(z)), dalam2=float((np.abs(z) <= 2).mean()) if len(z) else float('nan'),
                 dalam5=float((np.abs(z) <= 5).mean()) if len(z) else float('nan'),
                 ingat=float((s1 & r1).sum() / max(s1.sum(), 1)), tepat=float((s1 & r1).sum() / max(r1.sum(), 1)))
    return R, S, tepat


# ---------- peraturan ----------
class Konteks:
    def __init__(self, kerja):
        self.kerja, self.pan = kerja, cari.panel(kerja, 'B')
        L = lapis.muat(kerja, 'B')
        self.Lr = (L['L1'], L['L2'])
        self.EV = c12.semua_pencetus(kerja, 'B')
        self.Lab, self.As = asas15(self.pan)
        self.ramal, sebenar, self.tepat = ramal_earnings(self.pan)
        for q in Q_TARIKH:                                            # pariti: peristiwa yang dibina semula = lapisan yang dipakai carian
            assert (sebenar[q] == (self.Lr[1][q] > 0)).all(), f'baris prasyarat {q} tidak sepadan dengan lapis_B.pkl'
        self.asas_nama = {}
        for n in self.EV:
            self.asas_nama.setdefault(n.split('.')[0], []).append(n)
        self._bare = {}

    def topeng(self, ev, q1, q2, f1, f2, ramal=False):
        m = np.ones(len(ev), bool)
        if q1 >= 0:
            m &= self.Lr[0][q1, ev] > 0
        if q2 >= 0:
            m &= self.ramal[q2][ev] if (ramal and q2 in Q_TARIKH) else (self.Lr[1][q2, ev] > 0)
        for f in (f1, f2):
            if f >= 0:
                m &= self.pan['F'][f, ev] > 0
        return m

    def ukur(self, ev):
        return ukur15(self.pan, self.Lab, self.As, ev)

    def prasyarat_sahaja(self, q1, q2):
        """Kelebihan `terus` dan statistik "prasyarat sahaja" (semua bar layak; tiada isyarat beli, tiada syarat saham)."""
        k = (int(q1), int(q2))
        if k not in self._bare:
            ev = np.flatnonzero(self.pan['sah'])
            self._bare[k] = self.ukur(ev[self.topeng(ev, k[0], k[1], -1, -1)])[0] if k != (-1, -1) else None
        return self._bare[k]

    def adik(self, pencetus, q1, q2, f1, f2):
        """S6: (bilangan adik-beradik >= ADIK_MIN_N belian, bilangan dengan kelebihan `terus` > 0)."""
        lain = sorted(n for n in self.asas_nama.get(pencetus.split('.')[0], []) if n != pencetus)
        if len(lain) > ADIK_MAKS:
            lain = [lain[i] for i in sorted(set(np.linspace(0, len(lain) - 1, ADIK_MAKS).round().astype(int)))]
        bil = pos = 0
        for n in lain:
            ev = self.EV[n]
            d, _ = self.ukur(ev[self.topeng(ev, q1, q2, f1, f2)])
            if d['n'] >= ADIK_MIN_N:
                bil += 1
                pos += d['kl_terus'] > 0
        return bil, int(pos)


def peraturan(kerja, K):
    """Senarai semua peraturan yang dinilai: calon CS13, setup lama dipercayai, kawalan K1, kawalan laporan kewangan K2."""
    C = pickle.load(open(os.path.join(kerja, 'cs13_calon.pkl'), 'rb'))
    idf = pd.read_csv(os.path.join(CS13, 'calon.csv.gz'), usecols=['id', 'id_F']).set_index('id').id_F
    U = pd.read_csv(os.path.join(CS13, 'senarai_utama.csv'))
    utama = set(U.id)
    out = []
    for r in C['calon'].itertuples():
        f = idf.get(r.id)
        f = f if isinstance(f, str) and f in utama else ''
        out.append(dict(id=r.id, jenis='calon', id_F=f, pencetus=r.pencetus, q1=int(r.q1), q2=int(r.q2), f1=int(r.f1), f2=int(r.f2), ev=None))
    for r in C['kawalan'].itertuples():
        asas = dict(pencetus=r.pencetus, q1=int(r.q1), f1=int(r.f1), f2=int(r.f2), ev=None, id_F='')
        out.append(dict(asas, id=r.id, jenis='K1', q2=int(r.q2)))
        out.append(dict(asas, id=r.id + 'E', jenis='K2', q2=Q_F01))
    lama = set(U.id[U.asal == 'lama'])
    for x in lama_takrif(kerja, K):
        if x['id'] in lama:
            out.append(dict(x, jenis='lama', id_F=x['id']))
    assert sum(1 for x in out if x['id_F']) == len(U), 'senarai utama tidak lengkap'
    return out


def lama_takrif(kerja, K):
    """Setup F lama (kedudukan akhir): isyarat seperti cs_semak11.setup_f + pencetus dan indeks prasyarat / syarat saham."""
    import cs_cs07 as c7
    import cs_lapor as lapor
    import cs_portfolio6 as p6
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('').set_index('id')
    KA = pd.read_csv(os.path.join(SINI, 'hasil', 'KEDUDUKAN_AKHIR.csv')).set_index('id')
    EVa = t7.semua_ev(kerja, 'B', 'asal')
    out = []
    for i in KA.index:
        r = reg.loc[i]
        if r.pusingan == 'CS07':
            d = c7.dari_takrif7(r.takrif)
            ev = t7.ev_satu(kerja, 'B', d['pencetus'])
        else:
            d = p6.dari_takrif5(r.takrif)
            ev = EVa[d['pencetus']]
        q1, q2, f1, f2 = int(d['q1']), int(d['q2']), int(d['f1']), int(d['f2'])
        out.append(dict(id=i, pencetus=d['pencetus'], q1=q1, q2=q2, f1=f1, f2=f2, ev=ev[c5.topeng(K.pan, K.Lr, ev, q1, q2, f1, f2)]))
    return out


def kira(kerja):
    """Nilai semua peraturan -> cs16_solid.pkl {baris: DataFrame, beli: {id_F: bar beli}, prasyarat: DataFrame, tepat}."""
    t0 = time.time()
    K = Konteks(kerja)
    P = peraturan(kerja, K)
    cari.log(f'CS16: {len(P)} peraturan · konteks siap · {time.time() - t0:.0f}s')
    baris, beli = [], {}
    for j, x in enumerate(P, 1):
        ev = x['ev']
        if ev is None:
            e0 = K.EV[x['pencetus']]
            ev = e0[K.topeng(e0, x['q1'], x['q2'], x['f1'], x['f2'])]
        d, e = K.ukur(ev)
        b = dict(id=x['id'], jenis=x['jenis'], id_F=x['id_F'], pencetus=x['pencetus'], q1=x['q1'], q2=x['q2'], f1=x['f1'], f2=x['f2'])
        b.update(d)
        b.update(syarat(d))
        pra = K.prasyarat_sahaja(x['q1'], x['q2'])
        b['kl_prasyarat'] = pra['kl_terus'] if pra and pra.get('n', 0) else float('nan')
        b['tambah'] = d.get('kl_terus', float('nan')) - b['kl_prasyarat'] if pra else float('nan')
        b['s7'] = bool(pra is None or (b['tambah'] == b['tambah'] and b['tambah'] >= TAMBAH_MIN))
        b['adik_bil'] = b['adik_pos'] = -1
        if all(b[f's{i}'] for i in (1, 2, 3, 4, 5, 7)) and x['pencetus'] in K.EV:      # S6 hanya bagi yang lulus syarat lain
            b['adik_bil'], b['adik_pos'] = K.adik(x['pencetus'], x['q1'], x['q2'], x['f1'], x['f2'])
        b['s6'] = 'tidak diuji' if b['adik_bil'] < ADIK_MIN_BIL else ('lulus' if b['adik_pos'] >= ADIK_BAHAGIAN * b['adik_bil'] else 'gagal')
        b['solid'] = bool(all(b[f's{i}'] for i in (1, 2, 3, 4, 5, 7)) and b['s6'] != 'gagal')
        b['tarikh'] = bool(x['q2'] in Q_TARIKH)
        b['kl_ramal'] = b['n_ramal'] = float('nan')
        if b['tarikh'] and x['jenis'] in ('calon', 'lama') and x['pencetus'] in K.EV:
            e0 = K.EV[x['pencetus']]
            dr, _ = K.ukur(e0[K.topeng(e0, x['q1'], x['q2'], x['f1'], x['f2'], ramal=True)])
            b['n_ramal'], b['kl_ramal'] = dr['n'], dr.get('kl_terus', float('nan'))
        b['s8'] = bool(b['tarikh'] and b['kl_ramal'] == b['kl_ramal'] and b['kl_ramal'] > 0
                       and b['kl_ramal'] >= S8_BAHAGIAN * d.get('kl_terus', float('nan')))
        b['boleh_dibuat'] = bool((not b['tarikh']) or b['s8'])
        baris.append(b)
        if x['id_F']:
            beli[x['id_F']] = e.astype(np.int32)
        if j % 1000 == 0:
            cari.log(f'  CS16 {j}/{len(P)} · {time.time() - t0:.0f}s')
    T = pd.DataFrame(baris)
    pras = pd.DataFrame([dict(q1=k[0], q2=k[1], prasyarat=c5.buang_kod(c5.tk_pra(k[0], k[1])).replace(' DAN ', ' + '), **v, **syarat(v))
                         for k, v in K._bare.items() if v])
    pickle.dump(dict(baris=T, beli=beli, prasyarat=pras, tepat=K.tepat), open(F_(kerja), 'wb'), protocol=4)
    cari.log(f'CS16 kira: {len(T)} peraturan · solid {int(T.solid.sum())} · {time.time() - t0:.0f}s')
    return T


# ---------- senarai pendek, bacaan, laporan ----------
def wakil(U, beli):
    """S9: antara setup SOLID senarai utama ("boleh dibuat" dahulu, kemudian kadar `terus`), buang yang beliannya bertindih
    (Jaccard >= JACCARD) dengan setup yang sudah dipilih. Pulangkan dict id -> '' (wakil) atau ID setup yang serupa."""
    S = U[U.solid].sort_values(['boleh_dibuat', 'terus', 'kl_terus'], ascending=False, kind='stable')
    pilih, out = [], {}
    for i in S.id_F:
        a = beli[i]
        serupa = ''
        for j in pilih:
            b = beli[j]
            sama = len(np.intersect1d(a, b, assume_unique=True))
            if sama / (len(a) + len(b) - sama) >= JACCARD:
                serupa = j
                break
        out[i] = serupa
        if not serupa:
            pilih.append(i)
    return out


def bacaan(T):
    kadar = lambda X: float(X.solid.mean()) if len(X) else float('nan')
    c, k1, k2 = T[T.jenis == 'calon'], T[T.jenis == 'K1'], T[T.jenis == 'K2']
    ce = c[c.q2 == Q_F01]
    B = dict(n_calon=int(len(c)), solid_calon=int(c.solid.sum()), kadar_calon=kadar(c), n_K1=int(len(k1)), solid_K1=int(k1.solid.sum()),
             kadar_K1=kadar(k1), n_K2=int(len(k2)), solid_K2=int(k2.solid.sum()), kadar_K2=kadar(k2),
             n_calon_earnings=int(len(ce)), solid_calon_earnings=int(ce.solid.sum()), kadar_calon_earnings=kadar(ce))
    B['b1'] = bool(B['kadar_K1'] <= B1_MAKS)
    B['nasib'] = B['kadar_K1'] / B['kadar_calon'] if B['kadar_calon'] > 0 else float('nan')
    B['b2'] = bool(B['kadar_calon_earnings'] >= B['kadar_K2'] + B2_BEZA)
    for s in ('s1', 's2', 's3', 's4', 's5', 's7'):
        B['lulus_' + s] = {nm: float(X[s].mean()) for nm, X in (('calon', c), ('K1', k1), ('K2', k2))}
    return B


def pariti(U):
    """Angka CS16 lawan senarai_utama.csv (beza terbesar)."""
    S = pd.read_csv(os.path.join(CS13, 'senarai_utama.csv')).set_index('id').loc[U.id_F]
    f = lambda a, b: float(np.nanmax(np.abs(U[a].to_numpy(float) - S[b].to_numpy(float))))
    return dict(n=f('n', 'n'), terus=f('terus', 'terus'), a_terus=f('a_terus', 'a_terus'), m5=f('m5', 'm5'),
                kl_K1=f('kl_K1', 'kl_terus_K1'), kl_K3=f('kl_K3', 'kl_terus_K3'))


def lapor_(kerja):
    D = pickle.load(open(F_(kerja), 'rb'))
    T = D['baris']
    U = T[T.id_F != ''].copy()
    par = pariti(U)
    assert par['n'] == 0 and max(v for k, v in par.items() if k != 'n') < 2e-5, f'pariti gagal: {par}'
    S13 = pd.read_csv(os.path.join(CS13, 'senarai_utama.csv')).set_index('id')
    for k in ('asal', 'prasyarat', 'nama', 'penapis', 'pilihan', 'menang_B', 'purata_B', 'kedudukan'):
        U[k] = S13.loc[U.id_F, k].to_numpy()
    w = wakil(U, D['beli'])
    U['serupa_dengan'] = [w.get(i, '') for i in U.id_F]
    U['wakil'] = [bool(s and w.get(i, 'x') == '') for i, s in zip(U.id_F, U.solid)]
    U = U.sort_values(['solid', 'wakil', 'boleh_dibuat', 'terus'], ascending=False, kind='stable').reset_index(drop=True)
    B = bacaan(T)
    B.update(pariti=par, tepat=D['tepat'], n_utama=int(len(U)), solid_utama=int(U.solid.sum()), wakil=int(U.wakil.sum()),
             solid_boleh=int((U.solid & U.boleh_dibuat).sum()), wakil_boleh=int((U.wakil & U.boleh_dibuat).sum()),
             solid_lama=int((U.solid & (U.asal == 'lama')).sum()), solid_tarikh=int((U.solid & U.tarikh).sum()))
    X = U[U.tarikh & U.kl_ramal.notna()]
    B['ramal'] = dict(n=int(len(X)), kl_sebenar=float(X.kl_terus.median()), kl_ramal=float(X.kl_ramal.median()),
                      positif=float((X.kl_ramal > 0).mean()), s8=float(X.s8.mean()))
    os.makedirs(HASIL, exist_ok=True)
    lajur = (['id_F', 'asal', 'solid', 'wakil', 'serupa_dengan', 'boleh_dibuat', 'prasyarat', 'nama', 'penapis', 'n', 'tahun', 'n_K3']
             + [a + nm for nm in LABEL for a in ('', 'a_')] + ['kl_terus', 'kl_m5', 'kl_m10', 'kl_m10d', 'kl_K1', 'kl_K2', 'kl_K3', 'thn_bil',
             'thn_pos', 'kl_baki', 'adik_bil', 'adik_pos', 'kl_prasyarat', 'tambah', 'tarikh', 'n_ramal', 'kl_ramal', 'menang', 'purata', 'rugi8',
             's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 'pilihan'])
    U[lajur].rename(columns={'id_F': 'id'}).to_csv(os.path.join(HASIL, 'solid.csv.gz'), index=False, float_format='%.4f')
    kk = ['id', 'jenis', 'pencetus', 'q1', 'q2', 'f1', 'f2', 'n', 'tahun', 'n_K3', 'terus', 'a_terus', 'kl_terus', 'kl_K1', 'kl_K2', 'kl_K3',
          'thn_bil', 'thn_pos', 'kl_baki', 'kl_m5', 'kl_m10', 'kl_m10d', 'kl_prasyarat', 'tambah', 'adik_bil', 'adik_pos', 's1', 's2', 's3', 's4',
          's5', 's6', 's7', 'solid']
    T[T.jenis.isin(['K1', 'K2'])][kk].to_csv(os.path.join(HASIL, 'kawalan.csv'), index=False, float_format='%.5f')
    Pr = D['prasyarat'].sort_values('kl_terus', ascending=False)
    Pr['solid_s1_s5'] = Pr[['s1', 's2', 's3', 's4', 's5']].all(axis=1)
    Pr[['q1', 'q2', 'prasyarat', 'n', 'tahun', 'n_K3', 'm5', 'a_m5', 'm10', 'a_m10', 'm10d', 'a_m10d', 'terus', 'a_terus', 'kl_terus', 'kl_K1',
        'kl_K2', 'kl_K3', 'thn_bil', 'thn_pos', 'kl_baki', 'menang', 'purata', 'rugi8', 's1', 's2', 's3', 's4', 's5', 'solid_s1_s5']].to_csv(
        os.path.join(HASIL, 'prasyarat.csv'), index=False, float_format='%.5f')
    B['prasyarat_solid'] = int(Pr.solid_s1_s5.sum())
    json.dump(_bersih(B), open(os.path.join(HASIL, 'bacaan.json'), 'w'), indent=1)
    open(os.path.join(HASIL, 'SOLID.md'), 'w', encoding='utf-8').write(teks_laporan(U, B, Pr))
    cari.log(f"CS16 lapor: solid {B['solid_utama']} daripada {B['n_utama']} · wakil {B['wakil']} · kawalan K1 {B['kadar_K1']:.3f} · K2 {B['kadar_K2']:.3f}")
    return B


def _bersih(x):
    if isinstance(x, dict):
        return {k: _bersih(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_bersih(v) for v in x]
    if isinstance(x, (float, np.floating)):
        return None if x != x else round(float(x), 6)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, np.bool_):
        return bool(x)
    return x


def teks_laporan(U, B, Pr):
    p = lambda x, d=0, tanda=False: '–' if x is None or x != x else f'{x * 100:{"+" if tanda else ""}.{d}f}'
    ya = lambda x: 'ya' if x else 'TIDAK'
    t = B['tepat']
    A = ['# CS16: "ujian solid" bagi setup F (backtest; BUKAN bukti)', '',
         'Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 16 Nov 2026 (z). Dijana `cs_solid16.py`; jangan sunting.', '',
         '- Permintaan pengguna 16 Nov 2026: beberapa setup F yang betul-betul solid, diukur dengan "5 % seminggu, 10 % seminggu, 10 % dua '
         'minggu". Tiada tapisan saham Shariah dalam pusingan ini (arahan pengguna).',
         f"- Dinilai pada saham yang carian tidak lihat: {B['n_calon']:,} calon CS13, setup lama yang dipercayai, {B['n_K1']} peraturan rawak "
         f"(kawalan), {B['n_K2']} peraturan rawak dengan prasyarat \"laporan kewangan dalam 1–5 hari\", dan setiap prasyarat tanpa isyarat beli.",
         f"- Semakan pariti: angka sama dengan senarai utama (beza terbesar {max(v for k, v in B['pariti'].items() if k != 'n'):.6f}).", '',
         '## 1. Takrif SOLID (semua mesti benar)', '',
         f'- S1 cukup belian: ≥ {MIN_N} belian, ≥ {MIN_TAHUN} tahun, ≥ {MIN_K3} belian pada 2025–26.',
         f'- S2 kelebihan jelas: kadar tangkap melebihi saham rawak hari sama sebanyak ≥ {KL_MIN * 100:.0f} mata, dan positif dalam ketiga-tiga tempoh.',
         f'- S3 tahun demi tahun: lebih baik daripada rawak dalam ≥ {THN_BAHAGIAN * 100:.0f} % tahun (tahun dengan ≥ {THN_MIN_N} belian; sekurang-kurangnya {THN_MIN_BIL} tahun).',
         '- S4 tiga angka pengguna: lebih baik daripada rawak bagi 5 % seminggu, 10 % seminggu DAN 10 % dua minggu.',
         f'- S5 tidak bergantung pada beberapa hari: selepas {BUANG_HARI} hari terbaik dibuang, masih ≥ +{KL_BAKI * 100:.0f} mata.',
         f'- S6 tahan ubah parameter: ≥ {ADIK_BAHAGIAN * 100:.0f} % varian parameter lain bagi isyarat beli yang sama masih lebih baik daripada rawak.',
         f'- S7 isyarat beli menambah: ≥ +{TAMBAH_MIN * 100:.0f} mata di atas "prasyarat sahaja".', '',
         '## 2. Keputusan', '',
         f"- **SOLID: {B['solid_utama']:,} daripada {B['n_utama']:,} setup senarai utama** ({B['solid_lama']} setup lama). Selepas membuang yang "
         f"serupa (belian bertindih ≥ {JACCARD * 100:.0f} %): **{B['wakil']:,} setup berbeza**.",
         f"- **Boleh dibuat tanpa mengetahui tarikh laporan dengan tepat: {B['solid_boleh']:,} daripada {B['solid_utama']:,} yang solid** "
         f"({B['wakil_boleh']:,} berbeza); {B['solid_tarikh']:,} setup solid bergantung pada tarikh laporan kewangan akan datang.",
         f"- Ujian (B1) takrif boleh dipercayai: peraturan rawak yang lulus SOLID = {B['solid_K1']} daripada {B['n_K1']} ({p(B['kadar_K1'], 1)} %; perlu "
         f"≤ {B1_MAKS * 100:.0f} %) → {ya(B['b1'])}. Calon yang lulus: {p(B['kadar_calon'], 1)} %; anggaran bahagian nasib {p(B['nasib'])} %.",
         f"- Ujian (B2) isyarat beli menambah di atas prasyarat laporan kewangan: calon ber-prasyarat itu lulus {p(B['kadar_calon_earnings'], 1)} %; "
         f"peraturan rawak dengan prasyarat yang sama lulus {p(B['kadar_K2'], 1)} % (perlu beza ≥ {B2_BEZA * 100:.0f} mata) → {ya(B['b2'])}."
         + ('' if B['b2'] else ' **Yang solid ialah PRASYARAT itu, bukan setiap setup secara berasingan.**'),
         '- Berapa peratus lulus setiap syarat (calon · peraturan rawak · rawak + laporan kewangan): '
         + '; '.join(f"{s.upper()} {p(B['lulus_' + s]['calon'])} · {p(B['lulus_' + s]['K1'])} · {p(B['lulus_' + s]['K2'])}" for s in ('s1', 's2', 's3', 's4', 's5', 's7')) + '.', '',
         '## 3. Tarikh laporan kewangan: sebenar lawan diteka', '',
         f"- Tekaan = tarikh laporan suku sama tahun lepas + {RAMAL_TAHUN} hari. Daripada {t['n']:,} laporan: {p(t['dalam2'])} % diteka dalam ±2 hari "
         f"dagangan, {p(t['dalam5'])} % dalam ±5. Hari \"1–5 hari sebelum laporan\" yang sebenar ditangkap oleh tekaan: {p(t['ingat'])} %; tekaan yang betul: {p(t['tepat'])} %.",
         f"- {B['ramal']['n']:,} setup senarai utama memakai tarikh akan datang. Nilai tengah kelebihan kadar tangkap: tarikh sebenar "
         f"{p(B['ramal']['kl_sebenar'], 1, True)} mata → tarikh diteka {p(B['ramal']['kl_ramal'], 1, True)} mata; {p(B['ramal']['positif'])} % masih positif; "
         f"{p(B['ramal']['s8'])} % mengekalkan sekurang-kurangnya separuh.",
         '- Ini ujian paling keras (tanpa kalendar). Dalam dunia sebenar kebanyakan syarikat mengumumkan tarikh lebih awal, jadi keadaan sebenar '
         'berada di antara dua angka itu.', '']
    kepala = ('| ID | Prasyarat | Isyarat beli | Syarat saham | 5 % seminggu (rawak) | 10 % seminggu (rawak) | 10 % dua minggu (rawak) | '
              'Naik lagi hingga minggu 4 (rawak) | Tahun lebih baik | Menang % | Purata % | Rugi ≥ 8 % % | Belian | Boleh dibuat | Tarikh diteka: kelebihan |\n'
              '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')

    def baris(r):
        f = lambda a: f'**{p(getattr(r, a))}** ({p(getattr(r, "a_" + a))})'
        return (f"| `{r.id_F}` | {r.prasyarat if isinstance(r.prasyarat, str) and r.prasyarat else '–'} | {r.nama} | "
                f"{r.penapis if isinstance(r.penapis, str) and r.penapis else '–'} | {f('m5')} | {f('m10')} | {f('m10d')} | {f('terus')} | "
                f"{r.thn_pos}/{r.thn_bil} | {p(r.menang)} | {p(r.purata, 1, True)} | {p(r.rugi8)} | {r.n:,} | {ya(r.boleh_dibuat)} | "
                f"{p(r.kl_ramal, 1, True) if r.tarikh else 'tidak berkenaan'} |")

    W = U[U.wakil]
    A += [f'## 4. Senarai pendek: {len(W):,} setup SOLID yang berbeza (daripada 100 belian; dalam kurungan = saham rawak hari sama)', '', kepala]
    A += [baris(r) for r in W.head(60).itertuples()]
    if len(W) > 60:
        A.append(f'| … | {len(W) - 60} lagi dalam `solid.csv.gz` | | | | | | | | | | | | | |')
    S = U[U.solid & ~U.wakil]
    A += ['', f'## 5. Setup SOLID lain yang serupa dengan wakil di atas: {len(S):,}', '',
          'Senarai penuh dalam `solid.csv.gz` (lajur `serupa_dengan`).', '',
          '## 6. "Prasyarat sahaja" (tanpa isyarat beli; rujukan)', '',
          '| Prasyarat | 5 % seminggu (rawak) | 10 % seminggu (rawak) | 10 % dua minggu (rawak) | Naik lagi hingga minggu 4 (rawak) | Kelebihan (mata) | Tahun lebih baik | Belian | Lulus S1–S5 |',
          '|---|---|---|---|---|---|---|---|---|']
    for r in Pr.head(15).itertuples():
        A.append(f"| {r.prasyarat} | {p(r.m5)} ({p(r.a_m5)}) | {p(r.m10)} ({p(r.a_m10)}) | {p(r.m10d)} ({p(r.a_m10d)}) | {p(r.terus)} ({p(r.a_terus)}) | "
                 f"{p(r.kl_terus, 1, True)} | {r.thn_pos}/{r.thn_bil} | {r.n:,} | {ya(r.solid_s1_s5)} |")
    A += ['', '## 7. Kaveat', '',
          '- Senarai utama sudah dipilih dengan saham yang sama, jadi "solid" bermaksud "paling tahan uji dalam backtest", BUKAN bukti.',
          '- Semua ambang ditetapkan oleh Claude sebelum hasil dilihat. Tiada saham delist. Tiada tapisan Shariah (arahan pengguna).',
          '- "Boleh dibuat" diukur dengan tekaan tarikh yang kasar; kalendar sebenar lebih tepat.',
          '- Registry, kohort dan susunan senarai utama tidak diubah. Bukti hanya datang daripada papertrade (keputusan pengguna).', '']
    return '\n'.join(A)


if __name__ == '__main__':
    langkah, kerja = sys.argv[1], sys.argv[2]
    {'kira': kira, 'lapor': lapor_}[langkah](kerja)
