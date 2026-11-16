# cs_solid18.py — pusingan CS18 "UJIAN SOLID" bagi lorong "pegang berbulan-bulan" (T) (SPEC_CARIAN_SETUP.md pindaan 16 Nov
# 2026 (ab); keputusan pengguna "ya untuk 1 dan 2"). Bukan carian: peraturan masuk tidak diubah, tiada kod T baharu, tiada
# tapisan Shariah. Takrif sama bentuk dengan CS16 (cs_solid16.py); sasaran dan mekanik lorong T:
#   satu posisi setiap saham, pegang 126 sesi + stop loss 6xATR14, asas = saham rawak hari sama x tercile ATR;
#   tiga angka lorong (besar, besar100, tb) + takrif SOLID-T S1-S7 + "boleh dibuat" S8 + senarai pendek S9;
#   kawalan rawak K1 dan "kawalan hasil tumbuh" K2; "prasyarat sahaja"; papan lama T01-T12 dipadankan semula daripada teks.
#   python3 cs_solid18.py kira <kerja>   -> <kerja>/cs18_solid.pkl
#   python3 cs_solid18.py lapor <kerja>  -> hasil/CS18/SOLID_T.md, solid_t.csv.gz, kawalan.csv, prasyarat.csv, bacaan.json
import json
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_cari as cari  # noqa: E402
import cs_cari12 as c12  # noqa: E402
import cs_daftar13 as d13  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_solid16 as s16  # noqa: E402
import cs_tala7 as t7  # noqa: E402
import cs_teras as teras  # noqa: E402
import cs_trend17 as t17  # noqa: E402
import cs_trend8 as t8  # noqa: E402

PUS = 'CS18'
LABEL = ('besar', 'besar100', 'tb')                                 # tiga angka lorong (S4)
MAKLUMAT = ('menang', 'rugi15', 'purata')                           # lawan saham rawak hari sama; BUKAN syarat
MIN_N, MIN_TAHUN, MIN_K3 = 300, 10, 20                              # S1
KL_MIN = 0.03                                                       # S2
THN_MIN_N, THN_MIN_BIL, THN_BAHAGIAN = 15, 8, 0.70                  # S3
BUANG_HARI, KL_BAKI = 10, 0.01                                      # S5
ADIK_MAKS, ADIK_MIN_N, ADIK_MIN_BIL, ADIK_BAHAGIAN = 30, 100, 3, 0.60   # S6
TAMBAH_MIN = 0.01                                                   # S7
S8_BAHAGIAN = 0.5                                                   # S8
JACCARD = 0.50                                                      # S9
B1_MAKS, B2_BEZA = 0.05, 0.10                                       # bacaan dikunci
RUGI = 0.15
Q_HASIL = t17.Q_HASIL
Q_TARIKH = s16.Q_TARIKH                                             # prasyarat yang memakai tarikh laporan AKAN DATANG
F_ = lambda kerja: os.path.join(kerja, 'cs18_solid.pkl')
HASIL = os.path.join(SINI, 'hasil', PUS)
CS17 = os.path.join(SINI, 'hasil', 'CS17')
CS08 = os.path.join(SINI, 'hasil', 'CS08')


# ---------- label dan asas ----------
def pegang_h(pan, ev, h):
    """(R, sesi jual) bagi "pegang 126 sesi + stop loss HENTI[h], tiada indikator keluar"."""
    R, SK = t8.hasil_semua(np.ascontiguousarray(ev, dtype=np.int64), pan['o'], pan['l'], pan['c'], pan['atr'], t17._XT0, t17._J0,
                           t17._P0, t17._B0, t8.PEGANG_MIN)
    return R[:, h, 0].astype(np.float64), SK[:, h, 0].astype(np.int64)


def asas18(pan):
    """(S8, Lab[bar, 3], As[bar, 3], Mk[bar, 3], Am[bar, 3], SK[bar]). Lab/As susunan LABEL: label dan asas (saham rawak hari
    sama x tercile ATR %); Mk/Am susunan MAKLUMAT: hasil dagangan jika SETIAP bar layak dibeli dan dipegang dengan mekanik
    lorong, dan puratanya dalam kumpulan hari x tercile yang sama; SK = sesi jual."""
    S8, V, L8, G = t8.label_v(pan)
    sah = np.flatnonzero(S8)
    R, sk = pegang_h(pan, sah, t17.S_HENTI)
    g = G[sah]
    bil = np.maximum(np.bincount(g), 1)
    kump = lambda x: (np.bincount(g, x) / bil)[g]
    N = len(pan['c'])
    Lab, As, Mk, Am = np.zeros((N, 3)), np.zeros((N, 3)), np.zeros((N, 3)), np.zeros((N, 3))
    Lab[:, 0], As[:, 0] = L8[:, 0], V[:, 1]
    Lab[:, 1], As[:, 1] = L8[:, 1], L8[:, 3]
    tb = (R >= t8.TB).astype(np.float64)
    Lab[sah, 2], As[sah, 2] = tb, kump(tb)
    for j, x in enumerate(((R > 0).astype(np.float64), (R <= -RUGI).astype(np.float64), R)):
        Mk[sah, j], Am[sah, j] = x, kump(x)
    SK = np.zeros(N, np.int64)
    SK[sah] = sk
    return S8, Lab, As, Mk, Am, SK


def ukur18(pan, A, ev):
    """Statistik belian satu peraturan (satu posisi setiap saham; ev sudah ditapis tetingkap 126 sesi) -> (dict, bar beli)."""
    _, Lab, As, Mk, Am, SK = A
    ev = np.ascontiguousarray(ev, dtype=np.int64)
    if not len(ev):
        return dict(n=0, tahun=0), ev
    e = ev[teras.satu_posisi(ev, SK[ev], pan['tid'])]
    tp, thn, hari = pan['tempoh'][e], pan['tarikh'][e] // 10000, pan['hari'][e]
    d = dict(n=int(len(e)), tahun=int(len(np.unique(thn))), median=float(np.median(Mk[e, 2])), pegang=float(np.median(SK[e]) + 1))
    for j, nm in enumerate(LABEL):
        d[nm], d['a_' + nm] = float(Lab[e, j].mean()), float(As[e, j].mean())
        d['kl_' + nm] = d[nm] - d['a_' + nm]
    for j, nm in enumerate(MAKLUMAT):
        d[nm], d['a_' + nm] = float(Mk[e, j].mean()), float(Am[e, j].mean())
    x = Lab[e, 0] - As[e, 0]                                          # sumbangan setiap belian kepada kelebihan `besar`
    for p in range(3):
        q = tp == p
        d[f'n_K{p + 1}'] = int(q.sum())
        d[f'kl_K{p + 1}'] = float(x[q].mean()) if q.any() else float('nan')
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
    s2 = bool(g('kl_besar') == g('kl_besar') and g('kl_besar') >= KL_MIN and all(pos(g(f'kl_K{p}')) for p in (1, 2, 3)))
    s3 = bool(d.get('thn_bil', 0) >= THN_MIN_BIL and d.get('thn_pos', 0) >= THN_BAHAGIAN * d.get('thn_bil', 0))
    s4 = bool(pos(g('kl_besar')) and pos(g('kl_besar100')) and pos(g('kl_tb')))
    s5 = bool(g('kl_baki') == g('kl_baki') and g('kl_baki') >= KL_BAKI)
    return dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5)


# ---------- peraturan ----------
class Konteks:
    def __init__(self, kerja):
        self.kerja, self.pan = kerja, cari.panel(kerja, 'B')
        L = lapis.muat(kerja, 'B')
        self.Lr = (L['L1'], L['L2'])
        self.EV = c12.semua_pencetus(kerja, 'B')
        self.A = asas18(self.pan)
        self.S8 = self.A[0]
        self.sah = np.flatnonzero(self.S8)
        self.ramal, sebenar, self.tepat = s16.ramal_earnings(self.pan)
        for q in Q_TARIKH:                                            # pariti: peristiwa yang dibina semula = lapisan yang dipakai carian
            assert (sebenar[q] == (self.Lr[1][q] > 0)).all(), f'baris prasyarat {q} tidak sepadan dengan lapis_B.pkl'
        self.asas_nama = {}
        for n in self.EV:
            self.asas_nama.setdefault(n.split('.')[0], []).append(n)
        self._bare = {}

    def isyarat(self, pencetus):
        e0 = self.EV[pencetus]
        return e0[self.S8[e0]]

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
        return ukur18(self.pan, self.A, ev)

    def prasyarat_sahaja(self, q1, q2):
        """Statistik "prasyarat sahaja" (semua bar layak; tiada isyarat beli, tiada syarat saham); None jika tiada prasyarat."""
        k = (int(q1), int(q2))
        if k not in self._bare:
            self._bare[k] = self.ukur(self.sah[self.topeng(self.sah, k[0], k[1], -1, -1)])[0] if k != (-1, -1) else None
        return self._bare[k]

    def adik(self, pencetus, q1, q2, f1, f2):
        """S6: (bilangan adik-beradik >= ADIK_MIN_N belian, bilangan dengan kelebihan `besar` > 0)."""
        lain = sorted(n for n in self.asas_nama.get(pencetus.split('.')[0], []) if n != pencetus)
        if len(lain) > ADIK_MAKS:
            lain = [lain[i] for i in sorted(set(np.linspace(0, len(lain) - 1, ADIK_MAKS).round().astype(int)))]
        bil = pos = 0
        for n in lain:
            ev = self.isyarat(n)
            d, _ = self.ukur(ev[self.topeng(ev, q1, q2, f1, f2)])
            if d['n'] >= ADIK_MIN_N:
                bil += 1
                pos += d['kl_besar'] > 0
        return bil, int(pos)


def lama_takrif(kerja, K):
    """Papan lama T01-T12: peraturan dipadankan semula daripada teks hasil/CS08/papan.csv. Pariti disemak dengan stop loss
    papan itu sendiri (bilangan belian dan kadar `besar` mesti sama); yang tidak sepadan ditinggalkan. -> (senarai, gagal)."""
    P = pd.read_csv(os.path.join(CS08, 'papan.csv'))
    param = t7.param_semua(kerja)
    nama, pra, pen = {}, {}, {}
    for n in K.EV:
        nama.setdefault(t7.nama7(n, param), []).append(n)
    for q1 in range(-1, len(lapis.PASARAN)):
        for q2 in range(-1, len(lapis.KUMPULAN)):
            pra.setdefault(d13.teks_pra(q1, q2), []).append((q1, q2))
    for f1 in range(-1, K.pan['F'].shape[0]):
        for f2 in range(-1, K.pan['F'].shape[0]):
            pen.setdefault(d13.teks_pen(f1, f2), []).append((f1, f2))
    teks = lambda x: x if isinstance(x, str) else ''
    out, gagal = [], []
    for r in P.itertuples():
        a, b, c = nama.get(r.pencetus, []), pra.get(teks(r.prasyarat), []), pen.get(teks(r.penapis), [])
        if len(a) != 1 or len(b) != 1 or not c or r.henti not in t8.HENTI:
            gagal.append(r.id)
            continue
        (q1, q2), (f1, f2) = b[0], c[0]
        ev = K.isyarat(a[0])
        ev = np.ascontiguousarray(ev[K.topeng(ev, q1, q2, f1, f2)], dtype=np.int64)
        _, sk = pegang_h(K.pan, ev, t8.HENTI.index(r.henti))
        e = ev[teras.satu_posisi(ev, sk, K.pan['tid'])]
        if len(e) != int(r.n) or abs(float(K.A[1][e, 0].mean()) - float(r.besar)) > 2e-5:
            gagal.append(r.id)
            continue
        out.append(dict(id=r.id, pencetus=a[0], q1=int(q1), q2=int(q2), f1=int(f1), f2=int(f2), henti_papan=r.henti))
    return out, gagal


def peraturan(kerja, K):
    """Semua peraturan yang dinilai: calon CS17, papan lama T01-T12, kawalan K1, "kawalan hasil tumbuh" K2. -> (senarai, gagal)."""
    C = pickle.load(open(t17.F_(kerja, 'calon'), 'rb'))
    idt = pd.read_csv(os.path.join(CS17, 'calon.csv.gz'), usecols=['id', 'id_T']).set_index('id').id_T
    out = []
    for r in C['calon'].itertuples():
        f = idt.get(r.id)
        out.append(dict(id=r.id, jenis='calon', id_T=f if isinstance(f, str) else '', pencetus=r.pencetus, q1=int(r.q1), q2=int(r.q2),
                        f1=int(r.f1), f2=int(r.f2)))
    for r in C['kawalan'].itertuples():
        asas = dict(pencetus=r.pencetus, q1=int(r.q1), f1=int(r.f1), f2=int(r.f2), id_T='')
        out.append(dict(asas, id=r.id, jenis='K1', q2=int(r.q2)))
        out.append(dict(asas, id=r.id + 'H', jenis='K2', q2=Q_HASIL))
    lama, gagal = lama_takrif(kerja, K)
    for x in lama:
        out.append(dict(id=x['id'], jenis='lama', id_T=x['id'], pencetus=x['pencetus'], q1=x['q1'], q2=x['q2'], f1=x['f1'], f2=x['f2']))
    return out, gagal


def nilai(K, x):
    """Satu baris hasil bagi satu peraturan (S1-S8) + bar beli."""
    e0 = K.isyarat(x['pencetus'])
    d, e = K.ukur(e0[K.topeng(e0, x['q1'], x['q2'], x['f1'], x['f2'])])
    b = dict(id=x['id'], jenis=x['jenis'], id_T=x['id_T'], pencetus=x['pencetus'], q1=x['q1'], q2=x['q2'], f1=x['f1'], f2=x['f2'])
    b.update(d)
    b.update(syarat(d))
    pra = K.prasyarat_sahaja(x['q1'], x['q2'])
    b['kl_prasyarat'] = pra['kl_besar'] if pra and pra.get('n', 0) else float('nan')
    b['tambah'] = d.get('kl_besar', float('nan')) - b['kl_prasyarat'] if pra else float('nan')
    b['s7'] = bool(pra is None or (b['tambah'] == b['tambah'] and b['tambah'] >= TAMBAH_MIN))
    b['adik_bil'] = b['adik_pos'] = -1
    if all(b[f's{i}'] for i in (1, 2, 3, 4, 5, 7)):                   # S6 hanya bagi yang lulus syarat lain
        b['adik_bil'], b['adik_pos'] = K.adik(x['pencetus'], x['q1'], x['q2'], x['f1'], x['f2'])
    b['s6'] = 'tidak diuji' if b['adik_bil'] < ADIK_MIN_BIL else ('lulus' if b['adik_pos'] >= ADIK_BAHAGIAN * b['adik_bil'] else 'gagal')
    b['solid'] = bool(all(b[f's{i}'] for i in (1, 2, 3, 4, 5, 7)) and b['s6'] != 'gagal')
    b['tarikh'] = bool(x['q2'] in Q_TARIKH)
    b['kl_ramal'] = b['n_ramal'] = float('nan')
    if b['tarikh'] and x['jenis'] in ('calon', 'lama'):
        dr, _ = K.ukur(e0[K.topeng(e0, x['q1'], x['q2'], x['f1'], x['f2'], ramal=True)])
        b['n_ramal'], b['kl_ramal'] = dr['n'], dr.get('kl_besar', float('nan'))
    b['s8'] = bool(b['tarikh'] and b['kl_ramal'] == b['kl_ramal'] and b['kl_ramal'] > 0
                   and b['kl_ramal'] >= S8_BAHAGIAN * d.get('kl_besar', float('nan')))
    b['boleh_dibuat'] = bool((not b['tarikh']) or b['s8'])
    b['rugi_ok'] = bool(d.get('n', 0) > 0 and d['rugi15'] <= d['a_rugi15'])
    return b, e


def kira(kerja):
    """Nilai semua peraturan -> cs18_solid.pkl {baris, beli: {id_T: bar beli}, prasyarat, tepat, lama_gagal}."""
    t0 = time.time()
    K = Konteks(kerja)
    P, gagal = peraturan(kerja, K)
    cari.log(f'CS18: {len(P)} peraturan · papan lama tidak sepadan: {gagal or "tiada"} · konteks siap · {time.time() - t0:.0f}s')
    baris, beli = [], {}
    for j, x in enumerate(P, 1):
        b, e = nilai(K, x)
        baris.append(b)
        if x['id_T']:
            beli[x['id_T']] = e.astype(np.int32)
        if j % 1000 == 0:
            cari.log(f'  CS18 {j}/{len(P)} · {time.time() - t0:.0f}s')
    T = pd.DataFrame(baris)
    pras = pd.DataFrame([dict(q1=k[0], q2=k[1], prasyarat=d13.teks_pra(k[0], k[1]), **v, **syarat(v)) for k, v in K._bare.items() if v])
    pickle.dump(dict(baris=T, beli=beli, prasyarat=pras, tepat=K.tepat, lama_gagal=gagal), open(F_(kerja), 'wb'), protocol=4)
    cari.log(f'CS18 kira: {len(T)} peraturan · solid {int(T.solid.sum())} · {time.time() - t0:.0f}s')
    return T


# ---------- senarai pendek, bacaan, laporan ----------
def wakil(U, beli):
    """S9: antara setup SOLID-T berkod T ("boleh dibuat" dahulu, kemudian kadar `besar`), buang yang beliannya bertindih
    (Jaccard >= JACCARD) dengan setup yang sudah dipilih. Pulangkan dict id -> '' (wakil) atau ID setup yang serupa."""
    S = U[U.solid].sort_values(['boleh_dibuat', 'besar', 'kl_besar'], ascending=False, kind='stable')
    pilih, out = [], {}
    for i in S.id_T:
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
    ch = c[c.q2 == Q_HASIL]
    B = dict(n_calon=int(len(c)), solid_calon=int(c.solid.sum()), kadar_calon=kadar(c), n_K1=int(len(k1)), solid_K1=int(k1.solid.sum()),
             kadar_K1=kadar(k1), n_K2=int(len(k2)), solid_K2=int(k2.solid.sum()), kadar_K2=kadar(k2),
             n_calon_hasil=int(len(ch)), solid_calon_hasil=int(ch.solid.sum()), kadar_calon_hasil=kadar(ch))
    B['b1'] = bool(B['kadar_K1'] <= B1_MAKS)
    B['nasib'] = B['kadar_K1'] / B['kadar_calon'] if B['kadar_calon'] > 0 else float('nan')
    B['b2'] = bool(B['kadar_calon_hasil'] >= B['kadar_K2'] + B2_BEZA)
    for s in ('s1', 's2', 's3', 's4', 's5', 's7'):
        B['lulus_' + s] = {nm: float(X[s].mean()) for nm, X in (('calon', c), ('K1', k1), ('K2', k2))}
    return B


def pariti(T):
    """Angka CS18 lawan hasil/CS17/calon.csv.gz (beza terbesar; fail itu 5 titik perpuluhan)."""
    S = pd.read_csv(os.path.join(CS17, 'calon.csv.gz')).set_index('id')
    c = T[T.jenis == 'calon'].set_index('id').loc[S.index]
    f = lambda a, b: float(np.nanmax(np.abs(c[a].to_numpy(float) - S[b].to_numpy(float))))
    return dict(n=f('n', 'n'), besar=f('besar', 'besar'), a_besar=f('a_besar', 'a_besar'), besar100=f('besar100', 'besar100'),
                tb=f('tb', 'tb'), menang=f('menang', 'menang'), purata=f('purata', 'purata'), rugi15=f('rugi15', 'rugi15'),
                kl_K1=f('kl_K1', 'kl_K1'), kl_K3=f('kl_K3', 'kl_K3'))


def lapor_(kerja):
    D = pickle.load(open(F_(kerja), 'rb'))
    T = D['baris']
    par = pariti(T)
    assert par['n'] == 0 and max(v for k, v in par.items() if k != 'n') < 2e-5, f'pariti gagal: {par}'
    U = T[T.id_T != ''].copy()
    S17 = pd.read_csv(os.path.join(CS17, 'senarai_t.csv')).set_index('id')
    P8 = pd.read_csv(os.path.join(CS08, 'papan.csv')).set_index('id')
    assert set(U.id_T[U.jenis == 'calon']) == set(S17.index), 'senarai T CS17 tidak lengkap'
    teks = lambda x: x if isinstance(x, str) else ''
    U['asal'] = np.where(U.jenis == 'lama', 'lama', 'baharu')
    U['prasyarat'] = [teks(P8.prasyarat[i] if a == 'lama' else S17.prasyarat[i]) for i, a in zip(U.id_T, U.asal)]
    U['nama'] = [P8.pencetus[i] if a == 'lama' else S17.nama[i] for i, a in zip(U.id_T, U.asal)]
    U['penapis'] = [teks(P8.penapis[i] if a == 'lama' else S17.penapis[i]) for i, a in zip(U.id_T, U.asal)]
    U['kes'] = [teks(P8.mxl[i]).replace(' ', '') if a == 'lama' else teks(S17.kes[i]) for i, a in zip(U.id_T, U.asal)]
    w = wakil(U, D['beli'])
    U['serupa_dengan'] = [w.get(i, '') for i in U.id_T]
    U['wakil'] = [bool(s and w.get(i, 'x') == '') for i, s in zip(U.id_T, U.solid)]
    U = U.sort_values(['solid', 'wakil', 'boleh_dibuat', 'besar'], ascending=False, kind='stable').reset_index(drop=True)
    B = bacaan(T)
    W, So = U[U.wakil], U[U.solid]
    md = lambda X, k: float(X[k].median()) if len(X) else float('nan')
    kunci_md = ('besar', 'a_besar', 'kl_besar', 'besar100', 'a_besar100', 'tb', 'a_tb', 'menang', 'a_menang', 'purata', 'a_purata',
                'rugi15', 'a_rugi15', 'median', 'n', 'tambah')
    B.update(pariti=par, tepat=D['tepat'], lama_gagal=list(D['lama_gagal']), n_t=int(len(U)), n_baharu=int((U.asal == 'baharu').sum()),
             n_lama=int((U.asal == 'lama').sum()), solid_t=int(U.solid.sum()), wakil=int(U.wakil.sum()),
             solid_boleh=int((U.solid & U.boleh_dibuat).sum()), wakil_boleh=int((U.wakil & U.boleh_dibuat).sum()),
             solid_lama=int((U.solid & (U.asal == 'lama')).sum()), id_solid_lama=sorted(U.id_T[U.solid & (U.asal == 'lama')]),
             solid_tarikh=int((U.solid & U.tarikh).sum()), solid_rugi_ok=int((U.solid & U.rugi_ok).sum()),
             wakil_rugi_ok=int((U.wakil & U.rugi_ok).sum()), solid_menang50=int((U.solid & (U.menang >= 0.5)).sum()),
             wakil_menang50=int((U.wakil & (U.menang >= 0.5)).sum()), solid_tidak_diuji_s6=int((U.solid & (U.s6 == 'tidak diuji')).sum()),
             solid_hasil=int((U.solid & (U.q2 == Q_HASIL)).sum()), solid_kes=int((U.solid & (U.kes != '')).sum()),
             thn_wakil=float((W.thn_pos / W.thn_bil).median()) if len(W) else float('nan'),
             median_wakil={k: md(W, k) for k in kunci_md}, median_solid={k: md(So, k) for k in kunci_md},
             median_semua={k: md(U, k) for k in kunci_md}, median_tidak_solid={k: md(U[~U.solid], k) for k in kunci_md},
             gagal_syarat={s: int((~U[s]).sum()) for s in ('s1', 's2', 's3', 's4', 's5', 's7')}, gagal_s6=int((U.s6 == 'gagal').sum()))
    X = U[U.tarikh & U.kl_ramal.notna()]
    B['ramal'] = dict(n=int(len(X)), kl_sebenar=md(X, 'kl_besar'), kl_ramal=md(X, 'kl_ramal'),
                      positif=float((X.kl_ramal > 0).mean()) if len(X) else float('nan'), s8=float(X.s8.mean()) if len(X) else float('nan'))
    os.makedirs(HASIL, exist_ok=True)
    angka = [a + nm for nm in LABEL for a in ('', 'a_', 'kl_')] + [a + nm for nm in MAKLUMAT for a in ('', 'a_')]
    lajur = (['id_T', 'asal', 'solid', 'wakil', 'serupa_dengan', 'boleh_dibuat', 'rugi_ok', 'prasyarat', 'nama', 'penapis', 'n', 'tahun', 'n_K3']
             + angka + ['median', 'pegang', 'kl_K1', 'kl_K2', 'kl_K3', 'thn_bil', 'thn_pos', 'kl_baki', 'adik_bil', 'adik_pos', 'kl_prasyarat',
                        'tambah', 'tarikh', 'n_ramal', 'kl_ramal', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 'kes', 'pencetus', 'q1', 'q2',
                        'f1', 'f2'])
    U[lajur].rename(columns={'id_T': 'id'}).to_csv(os.path.join(HASIL, 'solid_t.csv.gz'), index=False, float_format='%.4f')
    kk = (['id', 'jenis', 'pencetus', 'q1', 'q2', 'f1', 'f2', 'n', 'tahun', 'n_K3'] + angka
          + ['kl_K1', 'kl_K2', 'kl_K3', 'thn_bil', 'thn_pos', 'kl_baki', 'kl_prasyarat', 'tambah', 'adik_bil', 'adik_pos', 's1', 's2', 's3', 's4',
             's5', 's6', 's7', 'solid'])
    T[T.jenis.isin(['K1', 'K2'])][kk].to_csv(os.path.join(HASIL, 'kawalan.csv'), index=False, float_format='%.5f')
    Pr = D['prasyarat'].sort_values('kl_besar', ascending=False)
    Pr['solid_s1_s5'] = Pr[['s1', 's2', 's3', 's4', 's5']].all(axis=1)
    Pr[['q1', 'q2', 'prasyarat', 'n', 'tahun', 'n_K3'] + angka + ['kl_K1', 'kl_K2', 'kl_K3', 'thn_bil', 'thn_pos', 'kl_baki', 's1', 's2', 's3',
                                                                 's4', 's5', 'solid_s1_s5']].to_csv(
        os.path.join(HASIL, 'prasyarat.csv'), index=False, float_format='%.5f')
    B['prasyarat_solid'] = int(Pr.solid_s1_s5.sum())
    json.dump(s16._bersih(B), open(os.path.join(HASIL, 'bacaan.json'), 'w'), indent=1)
    open(os.path.join(HASIL, 'SOLID_T.md'), 'w', encoding='utf-8').write(teks_laporan(U, B, Pr))
    cari.log(f"CS18 lapor: solid {B['solid_t']} daripada {B['n_t']} · wakil {B['wakil']} · kawalan K1 {B['kadar_K1']:.3f} · K2 {B['kadar_K2']:.3f}"
             f" · B1 {B['b1']} · B2 {B['b2']}")
    return B


def teks_laporan(U, B, Pr):
    p = lambda x, d=0, tanda=False: '–' if x is None or x != x else f'{x * 100:{"+" if tanda else ""}.{d}f}'
    ya = lambda x: 'ya' if x else 'TIDAK'
    mw, ms, mt = B['median_wakil'], B['median_semua'], B['median_tidak_solid']
    g = B['gagal_syarat']
    A = ['# CS18: "ujian solid" bagi lorong "pegang berbulan-bulan" (T) (backtest; BUKAN bukti)', '',
         'Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 16 Nov 2026 (ab). Dijana `cs_solid18.py`; jangan sunting.', '',
         '- Lorong ini: beli selepas isyarat, pegang hingga 6 bulan (126 hari dagangan) dengan stop loss longgar (6×ATR14), tiada jualan lain. '
         'Tiada tapisan saham Shariah (arahan pengguna).',
         f"- Dinilai pada saham yang carian tidak lihat: {B['n_calon']:,} calon CS17 ({B['n_baharu']:,} berkod `T13`–`T2576`), {B['n_lama']} setup "
         f"papan lama, {B['n_K1']} peraturan rawak (kawalan), {B['n_K2']} peraturan rawak dengan prasyarat \"hasil suku tumbuh ≥ 20 %\", dan "
         'setiap prasyarat tanpa isyarat beli.',
         f"- Semakan pariti: angka sama dengan `hasil/CS17/calon.csv.gz` (beza terbesar {max(v for k, v in B['pariti'].items() if k != 'n'):.6f}). "
         + (f"Papan lama yang tidak dapat dipadankan semula: {', '.join(B['lama_gagal'])}." if B['lama_gagal'] else
            'Kesemua 12 setup papan lama dipadankan semula (bilangan belian dan kadar naik besar sama dengan papan CS08).'), '',
         '## 1. Takrif SOLID (semua mesti benar; sama bentuk dengan ujian solid setup F)', '',
         f'- S1 cukup belian: ≥ {MIN_N} belian, ≥ {MIN_TAHUN} tahun, ≥ {MIN_K3} belian pada 2025–26.',
         f'- S2 kelebihan jelas: kadar naik besar melebihi saham rawak hari sama sebanyak ≥ {KL_MIN * 100:.0f} mata, dan positif dalam ketiga-tiga tempoh.',
         f'- S3 tahun demi tahun: lebih baik daripada rawak dalam ≥ {THN_BAHAGIAN * 100:.0f} % tahun (tahun dengan ≥ {THN_MIN_N} belian; sekurang-kurangnya {THN_MIN_BIL} tahun).',
         '- S4 tiga angka lorong: lebih baik daripada rawak bagi naik besar (≥ +50 % sebelum −15 %), capai +100 % DAN dijual dengan untung ≥ +30 %.',
         f'- S5 tidak bergantung pada beberapa hari: selepas {BUANG_HARI} hari terbaik dibuang, masih ≥ +{KL_BAKI * 100:.0f} mata.',
         f'- S6 tahan ubah parameter: ≥ {ADIK_BAHAGIAN * 100:.0f} % varian parameter lain bagi isyarat beli yang sama masih lebih baik daripada rawak.',
         f'- S7 isyarat beli menambah: ≥ +{TAMBAH_MIN * 100:.0f} mata di atas "prasyarat sahaja".', '',
         '## 2. Keputusan', '',
         f"- **SOLID: {B['solid_t']:,} daripada {B['n_t']:,} setup lorong ini** ({B['solid_lama']} daripada {B['n_lama']} setup papan lama"
         + (f": {', '.join('`' + i + '`' for i in B['id_solid_lama'])}" if B['id_solid_lama'] else '') + '). Selepas membuang yang serupa (belian '
         f"bertindih ≥ {JACCARD * 100:.0f} %): **{B['wakil']:,} setup berbeza**.",
         f"- Ujian (B1) takrif boleh dipercayai: peraturan rawak yang lulus SOLID = {B['solid_K1']} daripada {B['n_K1']} ({p(B['kadar_K1'], 1)} %; perlu "
         f"≤ {B1_MAKS * 100:.0f} %) → {ya(B['b1'])}. Calon yang lulus: {p(B['kadar_calon'], 1)} %; anggaran bahagian nasib {p(B['nasib'])} %.",
         f"- Ujian (B2) isyarat beli menambah di atas prasyarat \"hasil suku tumbuh ≥ 20 %\": calon ber-prasyarat itu lulus {p(B['kadar_calon_hasil'], 1)} %; "
         f"peraturan rawak dengan prasyarat yang sama lulus {p(B['kadar_K2'], 1)} % (perlu beza ≥ {B2_BEZA * 100:.0f} mata) → {ya(B['b2'])}."
         + ('' if B['b2'] else ' **Sebahagian besar kelebihan datang daripada PRASYARAT itu, bukan daripada setiap setup secara berasingan.**'),
         '- Berapa peratus lulus setiap syarat (calon · peraturan rawak · rawak + hasil tumbuh): '
         + '; '.join(f"{s.upper()} {p(B['lulus_' + s]['calon'])} · {p(B['lulus_' + s]['K1'])} · {p(B['lulus_' + s]['K2'])}" for s in ('s1', 's2', 's3', 's4', 's5', 's7')) + '.',
         f"- Antara {B['n_t']:,} setup berkod T, bilangan yang GAGAL setiap syarat: S1 {g['s1']:,}; S2 {g['s2']:,}; S3 {g['s3']:,}; S4 {g['s4']:,}; "
         f"S5 {g['s5']:,}; S7 {g['s7']:,}; S6 {B['gagal_s6']:,} (antara yang lulus syarat lain). {B['solid_tidak_diuji_s6']:,} setup solid tidak "
         'dapat diuji S6 (kurang daripada 3 varian lain).',
         f"- {B['solid_hasil']:,} daripada {B['solid_t']:,} setup solid memakai prasyarat \"hasil suku tumbuh ≥ 20 %\". "
         f"{B['solid_tarikh']:,} bergantung pada tarikh laporan kewangan akan datang; boleh dibuat tanpa tarikh tepat: {B['solid_boleh']:,} "
         f"({B['wakil_boleh']:,} berbeza).",
         f"- Kes MXL (Mac–Jun 2026; satu contoh): {B['solid_kes']:,} setup solid memberi isyarat beli pada MXL.", '',
         '## 3. Gambaran (nilai tengah; daripada 100 belian; dalam kurungan = saham rawak hari sama yang dipegang dengan cara sama)', '',
         '| | Naik besar | Capai +100 % | Dijual ≥ +30 % | Menang % | Purata setiap dagangan % | Rugi ≥ 15 % % | Dagangan biasa (nilai tengah) % | Belian |',
         '|---|---|---|---|---|---|---|---|---|']
    for nm, m in ((f"Solid yang berbeza ({B['wakil']:,})", mw), (f"Semua solid ({B['solid_t']:,})", B['median_solid']),
                  (f"Tidak solid ({B['n_t'] - B['solid_t']:,})", mt), (f"Semua setup lorong ini ({B['n_t']:,})", ms)):
        A.append(f"| {nm} | {p(m['besar'], 1)} ({p(m['a_besar'], 1)}) | {p(m['besar100'], 1)} ({p(m['a_besar100'], 1)}) | {p(m['tb'], 1)} ({p(m['a_tb'], 1)}) | "
                 f"{p(m['menang'])} ({p(m['a_menang'])}) | {p(m['purata'], 1, True)} ({p(m['a_purata'], 1, True)}) | {p(m['rugi15'])} ({p(m['a_rugi15'])}) | "
                 f"{p(m['median'], 1, True)} | {m['n']:,.0f} |")
    A += ['',
          f"- Solid yang berbeza: lebih baik daripada rawak dalam {p(B['thn_wakil'])} % tahun (nilai tengah).",
          f"- **Rugi besar:** {B['solid_rugi_ok']:,} daripada {B['solid_t']:,} setup solid ({B['wakil_rugi_ok']:,} daripada {B['wakil']:,} yang berbeza) "
          'rugi ≥ 15 % TIDAK lebih kerap daripada saham rawak hari sama (lajur `rugi_ok`). '
          f"Menang ≥ 50 %: {B['solid_menang50']:,} solid ({B['wakil_menang50']:,} berbeza). Dua lajur ini maklumat, bukan syarat SOLID.", '']
    kepala = ('| ID | Prasyarat | Isyarat beli | Syarat saham | Naik besar (rawak) | Capai +100 % (rawak) | Dijual ≥ +30 % (rawak) | Tahun lebih baik | '
              'Menang % (rawak) | Purata % (rawak) | Rugi ≥ 15 % % (rawak) | Belian | Boleh dibuat | MXL |\n'
              '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')

    def baris(r):
        f = lambda a, d=1: f'**{p(getattr(r, a), d)}** ({p(getattr(r, "a_" + a), d)})'
        return (f"| `{r.id_T}` | {r.prasyarat or '–'} | {r.nama} | {r.penapis or '–'} | {f('besar')} | {f('besar100')} | {f('tb')} | "
                f"{r.thn_pos}/{r.thn_bil} | {p(r.menang)} ({p(r.a_menang)}) | {p(r.purata, 1, True)} ({p(r.a_purata, 1, True)}) | "
                f"{p(r.rugi15)} ({p(r.a_rugi15)}) | {r.n:,} | {ya(r.boleh_dibuat)} | {r.kes.split(';')[0].split('@')[0] if r.kes else '–'} |")

    W = U[U.wakil]
    A += [f'## 4. Senarai pendek: {len(W):,} setup SOLID yang berbeza', '', kepala]
    A += [baris(r) for r in W.head(60).itertuples()]
    if len(W) > 60:
        A.append(f'| … | {len(W) - 60} lagi dalam `solid_t.csv.gz` | | | | | | | | | | | | |')
    S = U[U.solid & ~U.wakil]
    L = U[U.asal == 'lama'].sort_values('id_T', key=lambda s: s.str[1:].astype(int))
    A += ['', f'## 5. Setup SOLID lain yang serupa dengan wakil di atas: {len(S):,}', '',
          'Senarai penuh dalam `solid_t.csv.gz` (lajur `serupa_dengan`).', '',
          '## 6. Papan lama `T01`–`T12` (dinilai dengan mekanik yang sama)', '',
          '| ID | Solid | Gagal syarat | Naik besar (rawak) | Tahun lebih baik | Menang % (rawak) | Rugi ≥ 15 % % (rawak) | Belian | Belian 2025–26 |',
          '|---|---|---|---|---|---|---|---|---|']
    for r in L.itertuples():
        gagal = [s.upper() for s in ('s1', 's2', 's3', 's4', 's5', 's7') if not getattr(r, s)] + (['S6'] if r.s6 == 'gagal' else [])
        A.append(f"| `{r.id_T}` | {ya(r.solid)} | {', '.join(gagal) or '–'} | {p(r.besar, 1)} ({p(r.a_besar, 1)}) | {r.thn_pos}/{r.thn_bil} | "
                 f"{p(r.menang)} ({p(r.a_menang)}) | {p(r.rugi15)} ({p(r.a_rugi15)}) | {r.n:,} | {r.n_K3} |")
    A += ['', '## 7. "Prasyarat sahaja" (tanpa isyarat beli; rujukan)', '',
          '| Prasyarat | Naik besar (rawak) | Kelebihan (mata) | Capai +100 % (rawak) | Dijual ≥ +30 % (rawak) | Tahun lebih baik | Menang % (rawak) | Rugi ≥ 15 % % (rawak) | Belian | Lulus S1–S5 |',
          '|---|---|---|---|---|---|---|---|---|---|']
    for r in Pr.head(15).itertuples():
        A.append(f"| {r.prasyarat} | {p(r.besar, 1)} ({p(r.a_besar, 1)}) | {p(r.kl_besar, 1, True)} | {p(r.besar100, 1)} ({p(r.a_besar100, 1)}) | "
                 f"{p(r.tb, 1)} ({p(r.a_tb, 1)}) | {r.thn_pos}/{r.thn_bil} | {p(r.menang)} ({p(r.a_menang)}) | {p(r.rugi15)} ({p(r.a_rugi15)}) | "
                 f"{r.n:,} | {ya(r.solid_s1_s5)} |")
    A += ['', f"{B['prasyarat_solid']} daripada {len(Pr)} gabungan prasyarat lulus S1–S5 tanpa isyarat beli (penuh dalam `prasyarat.csv`).", '',
          '## 8. Kaveat', '',
          '- Senarai lorong ini sudah dipilih dengan saham yang sama, jadi "solid" bermaksud "paling tahan uji dalam backtest", BUKAN bukti.',
          '- Ambang disalin daripada ujian solid setup F dan ditetapkan sebelum hasil dilihat. Tiada tapisan Shariah (arahan pengguna).',
          '- Tiada saham delist dalam data: bagi pegang 6 bulan, saham yang gagal hilang dan angka condong ke atas lebih daripada lorong swing.',
          '- 2025–26 pendek (isyarat hingga awal 2026 sahaja, kerana perlu 6 bulan penuh selepas beli).',
          '- "Saham rawak hari sama" bagi menang, purata dan rugi = setiap saham layak pada hari dan kelas turun-naik yang sama, dibeli dan '
          'dipegang dengan cara yang sama (tanpa peraturan satu posisi).',
          '- Kod T, `hasil/CS17/`, papan CS08, registry F dan kohort tidak diubah. Bukti hanya datang daripada papertrade (keputusan pengguna).', '']
    return '\n'.join(A)


if __name__ == '__main__':
    langkah, kerja = sys.argv[1], sys.argv[2]
    {'kira': kira, 'lapor': lapor_}[langkah](kerja)
