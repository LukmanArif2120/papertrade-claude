"""Carian setup CS01 — pemacu (pradaftar `kajian/SPEC_CARIAN_SETUP.md`).

Guna (folder kerja di luar repo; fail perantaraan besar tidak dikomit):
  python3 cs_cari.py panel  <kerja> <set>         bina panel indikator (set: 431 | kunci | A | B)
  python3 cs_cari.py benih  <kerja> <set>         isyarat benih M (asal + 2 varian) dan N pada set cari
  python3 cs_cari.py besar  <kerja> <pusingan>    peringkat besar: semua masuk x henti x keluar (SPEC §6.1)
  python3 cs_cari.py tepat  <kerja> <pusingan>    peringkat tepat + papan 10 teratas + kolam rawak (SPEC §6.2-6.3)
  python3 cs_cari.py kunci  <kerja> <pusingan>    nilai pada Kunci (SPEC §6.4)
Pusingan: CS01 = (set 431, Kunci 1,000 saham); CS02 = (kumpulan A, kumpulan B) Release A02. Satu folder kerja
setiap pusingan.
Laporan: cs_lapor.py.
"""
import contextlib
import glob
import importlib
import json
import multiprocessing as mp
import os
import pickle
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from concurrent.futures.process import BrokenProcessPool

import numpy as np
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
AKAR = os.path.normpath(os.path.join(SINI, '..', '..', '..'))
for _p in (SINI, AKAR, os.path.join(AKAR, 'AUTOTUNE', 'kaedah'), os.path.join(AKAR, 'BacktestShariah2', 'kod')):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import cs_atom as atom  # noqa: E402
import cs_teras as teras  # noqa: E402

LAJUR = ['open', 'high', 'low', 'close', 'volume', 'turnover']
PEKERJA = int(os.environ.get('CS_PEKERJA', '4'))
N_MIN = 100
PUSINGAN = {'CS01': ('431', 'kunci'), 'CS02': ('A', 'B'), 'CS03': ('A', 'B'), 'CS04': ('A', 'B')}      # pusingan -> (set cari, set Kunci)
N_ATAS = 8
N_TEPAT = 2000
N_SENARAI = 200
TEPI = np.round(np.arange(-0.10, 0.1001, 0.001), 4)
A1, A2, OP = teras.peraturan_keluar(len(atom.KELUAR))
NR = len(A1)
K = teras.NH * NR
JENIS = np.zeros(len(atom.KELUAR), np.int64)
PAR = np.zeros(len(atom.KELUAR))
for _a, (_j, _v) in atom.LALUAN.items():
    JENIS[_a] = 1 if _j == 'chand' else 2
    PAR[_a] = _v
_NF = len(atom.PENAPIS)
F1 = np.asarray([-1] + list(range(_NF)) + [a for a in range(_NF) for b in range(a + 1, _NF)], np.int64)
F2 = np.asarray([-1] + [-1] * _NF + [b for a in range(_NF) for b in range(a + 1, _NF)], np.int64)


def log(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)


# ---------- data ----------
def muat_set(set_):
    from AUTOTUNE.teras import data as D
    if set_ == '431':
        fr, idx = D.muat_431()
        return fr, idx, None
    if set_ in ('A', 'B'):                                   # CS02: kumpulan A (cari) / B (Kunci) Release A02
        fr, idx, univ = D.muat('2009-01-01', '2026-12-31', kumpulan=set_, tag='autotune-data-a02')
        return fr, idx, {t: D.topeng(fr[t], t, univ, kumpulan=set_).to_numpy() for t in fr}
    fr_semua, idx, univ = D.muat('2009-01-01', '2026-12-31', tag='autotune-data-a02')
    s431 = set(pd.concat([pd.read_csv(os.path.join(AKAR, 'data_mentah', f'dataset_{s}.csv'), usecols=['ticker'])
                          for s in ('S1', 'S2', 'S3', 'S4')]).ticker)
    lain = sorted(t for t in fr_semua if t not in s431)
    pilih = sorted(np.random.default_rng(atom.BENIH).choice(lain, 1000, replace=False))
    fr = {t: fr_semua[t] for t in pilih}
    return fr, idx, {t: D.topeng(fr[t], t, univ).to_numpy() for t in pilih}


def panel(kerja, set_, bina=False):
    f = os.path.join(kerja, f'panel_{set_}.pkl')
    if os.path.exists(f) and not bina:
        return pickle.load(open(f, 'rb'))
    fr, idx, lt = muat_set(set_)
    pan = atom.bina(fr, idx, set_, lt)
    akhir = pan['mula'][pan['tid'] + 1]
    i = np.arange(len(pan['c']))
    e = np.minimum(i + 1, len(i) - 1)
    pan['sah'] = (pan['layak'] & (pan['tempoh'] >= 0) & (i + teras.TMAX < akhir) & (pan['atr'] > 0)
                  & (pan['o'][e] > 0))
    hari_unik = np.unique(pan['tarikh'])
    pan['hari'] = np.searchsorted(hari_unik, pan['tarikh'])
    pan['hari_unik'] = hari_unik
    pickle.dump(pan, open(f, 'wb'), protocol=4)
    return pan


# ---------- benih M / N ----------
_FR = _IDX = _TICK = None
_KAUSAL = False               # pindaan 16 Nov 2026 (ae) Bahagian C; lalai False = sama seperti pusingan CS01-CS18


@contextlib.contextmanager
def tanpa_intai():
    """Mod "tanpa intai" (pindaan 16 Nov 2026 (ae) Bahagian C). 98 daripada 134 modul kaedah M memakai `open.shift(-1)` (59 terus,
    40 melalui fungsi kongsi `_k145.langkau`)
    untuk membatalkan isyarat apabila harga buka ESOK <= paras stop (atau >= sasaran) -- maklumat yang belum wujud pada
    tutup hari isyarat. Dalam konteks ini `Series` bernama 'open' yang dianjak NEGATIF dipulangkan kosong (NaN), jadi
    pembatalan itu tidak berlaku dan isyarat hanya bergantung pada bar hari itu dan sebelumnya. Modul kaedah tidak diubah.
    HAD: modul yang membaca bar esok melalui indeks tatasusunan (cth. `o[i + 1]`) atau menganjak siri LAIN (hujung
    minggu/bulan) tidak dibetulkan di sini; lihat `cs_audit19.INTAI_LAIN` dan ujian bar terakhir `cs_audit19.py intai`."""
    asal = pd.Series.shift

    def anjak(self, periods=1, *a, **k):
        if isinstance(periods, (int, np.integer)) and periods < 0 and self.name == 'open':
            return pd.Series(np.nan, index=self.index, name=self.name)
        return asal(self, periods, *a, **k)

    pd.Series.shift = anjak
    try:
        yield
    finally:
        pd.Series.shift = asal


def param_varian(pj, mid, v):
    if v == 0:
        return None
    d = pj[(pj.kaedah == mid) & (pj.tala == 'Y')]
    rng = np.random.default_rng([atom.BENIH, v, int(mid[1:])])
    P = {}
    for r in d.itertuples():
        if r.jenis == 'int':
            P[r.nama] = int(rng.integers(int(round(r.bawah)), int(round(r.atas)) + 1))
        else:
            P[r.nama] = float(rng.uniform(r.bawah, r.atas))
    return P


def _jalan_modul(tugas):
    nama, modul, P = tugas
    warnings.filterwarnings('ignore')
    try:
        m = importlib.import_module(modul)
        # Modul yang tidak bergantung pada saham lain dijalankan 100 saham sekali (hasil sama, memori terkawal).
        kump = [_TICK] if getattr(m, 'SILANG', False) else [_TICK[i:i + 100] for i in range(0, len(_TICK), 100)]
        bah = []
        for kt in kump:
            f2 = {t: _FR[t][LAJUR].copy() for t in kt}
            with (tanpa_intai() if _KAUSAL else contextlib.nullcontext()):
                if modul.startswith('kaedah.'):
                    m.sedia(f2, _IDX)
                else:
                    m.sedia(f2, _IDX, P)
            bah += [np.asarray(pd.Series(f2[t]['sig']).fillna(False), dtype=bool) for t in kt]
            del f2
        return nama, np.packbits(np.concatenate(bah)), None
    except Exception as e:                                  # varian yang gagal dicatat dan ditinggalkan
        return nama, None, f'{type(e).__name__}: {str(e)[:120]}'


def senarai_benih():
    pj = pd.read_csv(os.path.join(AKAR, 'AUTOTUNE', 'kaedah', 'param_julat.csv'))
    tugas = []
    for f in sorted(glob.glob(os.path.join(AKAR, 'AUTOTUNE', 'kaedah', 'M*.py'))):
        mid = os.path.basename(f)[:-3]
        for v in (0, 1, 2):
            P = param_varian(pj, mid, v)
            if v and not P:
                continue
            tugas.append((f'{mid}.{v}', mid, P))
    lihat = set()
    for f in sorted(glob.glob(os.path.join(AKAR, 'BacktestShariah2', 'kod', 'kaedah', 'N*.py'))):
        mod = os.path.basename(f)[:-3]
        nid = mod.split('X')[0]
        if nid not in lihat:
            lihat.add(nid)
            tugas.append((nid, f'kaedah.{mod}', None))
    return tugas


def benih(kerja, set_, hanya=None, tugas=None, fail=None, kausal=False):
    """Jalankan modul benih pada set; simpan/kemas kini benih_<set>.pkl = {nama: packbits sig}, ralat = {...}.
    tugas: senarai (nama, modul, P) khas (lalai: senarai_benih()); fail: nama fail keluaran khas.
    kausal=True: mod "tanpa intai" (`tanpa_intai`); WAJIB bagi pusingan baharu (pindaan (ae)); fail keluaran mesti berbeza."""
    global _KAUSAL
    assert not kausal or fail, 'kausal=True memerlukan nama fail keluaran sendiri (jangan campur dengan benih lama)'
    _KAUSAL = bool(kausal)
    try:
        return _benih(kerja, set_, hanya, tugas, fail)
    finally:
        _KAUSAL = False


def _benih(kerja, set_, hanya=None, tugas=None, fail=None):
    global _FR, _IDX, _TICK
    f = os.path.join(kerja, fail or f'benih_{set_}.pkl')
    sedia = pickle.load(open(f, 'rb')) if os.path.exists(f) else {'sig': {}, 'ralat': {}, 'param': {}}
    tugas = [t for t in (senarai_benih() if tugas is None else tugas) if (hanya is None or t[0] in hanya)
             and t[0] not in sedia['sig'] and t[0] not in sedia['ralat']]
    if not tugas:
        return sedia
    _FR, _IDX, _ = muat_set(set_)
    _TICK = sorted(_FR)
    log(f'benih {set_}: {len(tugas)} modul')
    simpan = lambda: (pickle.dump(sedia, open(f + '.tmp', 'wb'), protocol=4), os.replace(f + '.tmp', f))
    with ProcessPoolExecutor(max_workers=PEKERJA, mp_context=mp.get_context('fork')) as ex:
        fut = [ex.submit(_jalan_modul, t) for t in tugas]
        try:
            for k, ft in enumerate(as_completed(fut)):
                nama, bit, ralat = ft.result()
                if ralat:
                    sedia['ralat'][nama] = ralat
                else:
                    sedia['sig'][nama] = bit
                if (k + 1) % 20 == 0:                        # simpan berperingkat: larian boleh disambung
                    log(f'  {k + 1}/{len(tugas)}')
                    simpan()
        except BrokenProcessPool:                            # pekerja dimatikan (memori): jangan tersangkut
            simpan()
            log('pekerja terbunuh; kemajuan disimpan. Jalankan semula (CS_PEKERJA lebih kecil) untuk menyambung.')
            raise SystemExit(1)
    for nama, _, P in tugas:
        sedia['param'][nama] = P
    pickle.dump(sedia, open(f, 'wb'), protocol=4)
    log(f'benih {set_}: ok {len(sedia["sig"])} ralat {len(sedia["ralat"])}')
    return sedia


def pencetus(pan, bn):
    """dict nama -> indeks bar isyarat (hari pertama isyarat, layak, tetingkap lengkap). Satu demi satu: jimat memori."""
    N = len(pan['c'])
    mula = lambda s: np.flatnonzero(atom.mula_isyarat(s, pan['mula']) & pan['sah'])
    out = {n[:3]: mula(pan['P'][n[:3]]) for n in atom.PENCETUS}
    for n, bit in (bn or {}).get('sig', {}).items():
        out[n] = mula(np.unpackbits(bit)[:N].astype(bool))
    return out


def keluarga(nama):
    return nama.split('.')[0]


# ---------- peringkat besar ----------
def besar(kerja, pus='CS01'):
    cari_set = PUSINGAN[pus][0]
    pan = panel(kerja, cari_set)
    bn = pickle.load(open(os.path.join(kerja, f'benih_{cari_set}.pkl'), 'rb'))
    ev_semua = pencetus(pan, bn)
    rng = np.random.default_rng(atom.BENIH)
    o, h, l, c, atr, X = pan['o'], pan['h'], pan['l'], pan['c'], pan['atr'], pan['X']
    fs = os.path.join(kerja, 'besar_semak.pkl')              # titik semak: larian panjang boleh disambung
    if os.path.exists(fs):
        atas, rawak, hist, meta, siap, saat0 = pickle.load(open(fs, 'rb'))
        log(f'sambung dari titik semak: {len(siap)} pencetus siap')
    else:
        atas, rawak, hist, siap, saat0 = [], [], np.zeros(len(TEPI) + 1, np.int64), set(), 0.0
        meta = {'pencetus': len(ev_semua), 'pencetus_cukup': 0, 'masuk_dicuba': 0, 'masuk_diskor': 0, 'K': K}
    t0 = time.time()
    for ti, (nama, ev) in enumerate(ev_semua.items()):
        tp = pan['tempoh'][ev].astype(np.int64)
        cukup = (tp == 0).sum() >= N_MIN and (tp == 1).sum() >= N_MIN
        rw = rng.integers(0, K, len(F1)) if cukup else None  # dicabut walaupun pencetus sudah siap (turutan rng sama)
        if nama in siap:
            continue
        siap.add(nama)
        meta['masuk_dicuba'] += len(F1)
        if cukup:
            meta['pencetus_cukup'] += 1
            Fm = np.ascontiguousarray(pan['F'][:, ev].T)
            S = np.zeros((len(F1), 2, K))
            Q = np.zeros((len(F1), 2, K))
            N2 = np.zeros((len(F1), 2), np.int64)
            for a in range(0, len(ev), 40000):
                Rm = teras.hasil_semua(ev[a:a + 40000], o, h, l, c, atr, X, JENIS, PAR, A1, A2, OP)
                teras.kumpul_tambah(Rm, tp[a:a + 40000], Fm[a:a + 40000], F1, F2, S, Q, N2)
            idx, st, stw, hs = teras.kumpul_skor(S, Q, N2, rw, N_MIN, N_ATAS, TEPI)
            ok = np.flatnonzero((N2[:, 0] >= N_MIN) & (N2[:, 1] >= N_MIN))
            meta['masuk_diskor'] += len(ok)
            hist += hs.sum(axis=0)
            for ci in ok:
                for t in range(N_ATAS):
                    atas.append((nama, F1[ci], F2[ci], idx[ci, t], *st[ci, t], N2[ci, 0], N2[ci, 1]))
                rawak.append((nama, F1[ci], F2[ci], rw[ci], *stw[ci], N2[ci, 0], N2[ci, 1]))
        if (ti + 1) % 25 == 0:
            log(f'  pencetus {ti + 1}/{len(ev_semua)} · masuk diskor {meta["masuk_diskor"]:,} · '
                f'{saat0 + time.time() - t0:.0f}s')
            pickle.dump((atas, rawak, hist, meta, siap, saat0 + time.time() - t0), open(fs + '.tmp', 'wb'), protocol=4)
            os.replace(fs + '.tmp', fs)
    lajur = ['pencetus', 'f1', 'f2', 'lajur', 'skor', 'pur_L', 'sd_L', 'pur_S', 'sd_S', 'n_L', 'n_S']
    pd.DataFrame(atas, columns=lajur).to_pickle(os.path.join(kerja, 'besar_atas.pkl'))
    pd.DataFrame(rawak, columns=lajur).to_pickle(os.path.join(kerja, 'besar_rawak.pkl'))
    meta['kombinasi_diskor'] = int(meta['masuk_diskor']) * K
    meta['kombinasi_dicuba'] = int(meta['masuk_dicuba']) * K
    meta['hist'] = hist.tolist()
    meta['saat'] = round(saat0 + time.time() - t0)
    meta['pusingan'] = pus
    meta['ralat_benih'] = bn['ralat']
    json.dump(meta, open(os.path.join(kerja, 'besar_meta.json'), 'w'))
    log(f"besar siap: {meta['kombinasi_diskor']:,} kombinasi diskor daripada {meta['kombinasi_dicuba']:,} dicuba")


# ---------- penilaian tepat ----------
def _stat(R):
    n = len(R)
    if n == 0:
        return 0, np.nan, np.nan, np.nan
    mu, sd = float(R.mean()), float(R.std())
    return n, mu, sd, mu - 2 * sd / np.sqrt(n)


def nilai(pan, ev, f1, f2, lajur, penuh=False, asas=None):
    """Nilai satu setup dengan peraturan satu posisi setiap saham. Pulangkan dict tempoh -> ukuran."""
    m = np.ones(len(ev), bool)
    for f in (f1, f2):
        if f >= 0:
            m &= pan['F'][f, ev] > 0
    e = ev[m]
    s, r = divmod(int(lajur), NR)
    o, h, l, c, atr = pan['o'], pan['h'], pan['l'], pan['c'], pan['atr']
    R, hp, sk = teras.hasil_satu(e, o, h, l, c, atr, pan['X'], JENIS, PAR, A1, A2, OP, s, r)
    amb = teras.satu_posisi(e, sk, pan['tid'])
    e, R, hp, sk = e[amb], R[amb], hp[amb], sk[amb]
    tp = pan['tempoh'][e]
    out = {}
    for p in range(int(pan['tempoh'].max()) + 1):
        q = tp == p
        n, mu, sd, lb = _stat(R[q])
        d = {'n': n, 'purata': mu, 'sd': sd, 'lb': lb}
        if penuh and n:
            Rp, ep = R[q], e[q]
            d.update(menang=float((Rp > 0).mean()), k10=float((Rp >= 0.10).mean()), k20=float((Rp >= 0.20).mean()),
                     rugi8=float((Rp <= -0.08).mean()),
                     k5m1=float((c[ep + 5] / o[ep + 1] - 1 >= 0.05).mean()), pegang=float(hp[q].mean()))
            d['seminggu'] = d['purata'] / d['pegang'] * 5
            if asas is not None:
                d['lebihan'] = float((Rp - asas[pan['hari'][ep]]).mean())
            bk = teras.buku_harian(ep, Rp, sk[q], hp[q], o, c, pan['hari'], len(pan['hari_unik']))
            eq = np.cumprod(1 + bk)
            d['mdd'] = float((eq / np.maximum.accumulate(eq) - 1).min())
        out[p] = d
    return out


def asas_rawak(pan, lajur):
    """Purata R semua bar layak setiap tarikh isyarat, dengan henti dan keluar yang sama (beli rawak hari sama)."""
    ev = np.flatnonzero(pan['sah'])
    s, r = divmod(int(lajur), NR)
    R = teras.hasil_satu(ev, pan['o'], pan['h'], pan['l'], pan['c'], pan['atr'], pan['X'], JENIS, PAR, A1, A2, OP,
                         s, r)[0]
    nh = len(pan['hari_unik'])
    hr = pan['hari'][ev]
    bil = np.bincount(hr, minlength=nh)
    return np.bincount(hr, R, minlength=nh) / np.maximum(bil, 1)


def skor_tepat(v):
    if v[0]['n'] < N_MIN or v[1]['n'] < N_MIN:
        return np.nan
    return min(v[0]['lb'], v[1]['lb'])


def tepat(kerja, pus='CS01'):
    cari_set = PUSINGAN[pus][0]
    pan = panel(kerja, cari_set)
    bn = pickle.load(open(os.path.join(kerja, f'benih_{cari_set}.pkl'), 'rb'))
    ev_semua = pencetus(pan, bn)
    A = pd.read_pickle(os.path.join(kerja, 'besar_atas.pkl')).sort_values('skor', ascending=False)
    A = A[A.groupby(['pencetus', 'f1', 'f2']).cumcount() < 3].head(N_TEPAT).reset_index(drop=True)
    baris = []
    for r in A.itertuples():
        v = nilai(pan, ev_semua[r.pencetus], r.f1, r.f2, r.lajur)
        baris.append((skor_tepat(v), v[0]['n'], v[0]['purata'], v[1]['n'], v[1]['purata']))
    A[['skor_tepat', 'nt_L', 'purt_L', 'nt_S', 'purt_S']] = baris
    A = A.dropna(subset=['skor_tepat']).sort_values('skor_tepat', ascending=False).reset_index(drop=True)
    A['keluarga'] = A.pencetus.map(keluarga)
    A['peranan'] = ''
    A.loc[A.index < N_SENARAI, 'peranan'] = 'atas200'
    papan = A.drop_duplicates('keluarga').head(10).index
    A.loc[papan, 'peranan'] = 'papan'
    W = pd.read_pickle(os.path.join(kerja, 'besar_rawak.pkl'))
    W = W.sample(N_SENARAI, random_state=atom.BENIH).reset_index(drop=True)
    baris = []
    for r in W.itertuples():
        v = nilai(pan, ev_semua[r.pencetus], r.f1, r.f2, r.lajur)
        baris.append((skor_tepat(v), v[0]['n'], v[0]['purata'], v[1]['n'], v[1]['purata']))
    W[['skor_tepat', 'nt_L', 'purt_L', 'nt_S', 'purt_S']] = baris
    W['keluarga'] = W.pencetus.map(keluarga)
    W['peranan'] = 'rawak'
    P = pd.concat([A[A.peranan != ''], W], ignore_index=True)
    P.to_pickle(os.path.join(kerja, 'pilihan.pkl'))
    A.to_pickle(os.path.join(kerja, 'tepat_semua.pkl'))
    log(f'tepat siap: {len(A)} setup sah; papan {len(papan)}; rawak {len(W)}')


def kunci(kerja, pus='CS01'):
    cari_set, kunci_set = PUSINGAN[pus]
    P = pd.read_pickle(os.path.join(kerja, 'pilihan.pkl'))
    out = {}
    for set_ in (cari_set, kunci_set):
        nama = [t[0] for t in atom.TEMPOH[set_]]
        pan = panel(kerja, set_)
        perlu = {n for n in P.pencetus.unique() if not n.startswith('P')}
        bn = benih(kerja, set_, hanya=perlu) if set_ == kunci_set else pickle.load(
            open(os.path.join(kerja, f'benih_{cari_set}.pkl'), 'rb'))
        ev_semua = pencetus(pan, bn)
        log(f'nilai {set_}: {len(P)} setup')
        for k, r in enumerate(P.itertuples()):
            if r.pencetus not in ev_semua:
                continue
            penuh = r.peranan == 'papan'
            v = nilai(pan, ev_semua[r.pencetus], r.f1, r.f2, r.lajur, penuh=penuh,
                      asas=asas_rawak(pan, r.lajur) if penuh else None)
            for p, n in enumerate(nama):
                out.setdefault(k, {})[n] = v[p]
            if penuh and set_ == cari_set:                   # T1: keempat-empat henti, masuk dan keluar sama
                rr = int(r.lajur) % NR
                out[k]['t1'] = [skor_tepat(nilai(pan, ev_semua[r.pencetus], r.f1, r.f2, s * NR + rr))
                                for s in range(teras.NH)]
        if set_ == kunci_set:
            out['_ralat_benih_kunci'] = bn['ralat']
    pickle.dump(out, open(os.path.join(kerja, 'kunci.pkl'), 'wb'))
    log('kunci siap')


if __name__ == '__main__':
    arahan, kerja = sys.argv[1], sys.argv[2]
    os.makedirs(kerja, exist_ok=True)
    if arahan == 'panel':
        pan = panel(kerja, sys.argv[3], bina=True)
        log(f"panel {sys.argv[3]}: {len(pan['ticker'])} saham, {len(pan['c']):,} bar, {int(pan['sah'].sum()):,} bar sah")
    elif arahan == 'benih':
        benih(kerja, sys.argv[3])
    else:
        {'besar': besar, 'tepat': tepat, 'kunci': kunci}[arahan](kerja, sys.argv[3] if len(sys.argv) > 3 else 'CS01')
