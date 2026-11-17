"""Carian setup — pusingan CS20 (SPEC pindaan 17 Nov 2026 (ag)): setup "sepanjang tahun" (membeli hampir setiap minggu).

Mengapa: CS12 / CS13 menyimpan 5 peraturan masuk terbaik setiap isyarat beli, dan prasyarat "laporan kewangan dalam 1-5 sesi"
hampir sentiasa mengisi kelima-limanya; peraturan sepanjang tahun tersisih sebelum dinilai. Pusingan ini mengulang carian yang
SAMA (enjin skor CS13, sasaran `terus` = kadar tangkap) dengan dua had: (1) prasyarat yang bergantung pada tarikh laporan
kewangan atau pada kalendar TIDAK dibenarkan; (2) peraturan mesti membeli dalam >= 80 % minggu (dan >= 50 % minggu pada tahun
paling teruk) pada separuh alam. Isyarat beli = bahagian `asal` (dijana dalam mod tanpa intai) + `K`.
Guna: python3 cs_mingguan20.py skor|calon|kunci|lapor|daftar <kerja>. Jangan sunting keluaran secara manual."""
import json
import multiprocessing as mp
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_cari as cari  # noqa: E402
import cs_cs05 as c5  # noqa: E402
import cs_daftar13 as d13  # noqa: E402
import cs_keluar7 as k7  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_semak11 as s11  # noqa: E402
import cs_tala7 as t7  # noqa: E402
import cs_teras as teras  # noqa: E402

N_ATAS, N_TINJAU, N_KAWALAN, BENIH_KAWALAN, CUBA_KAWALAN = 5, 200, 300, 20261117, 400000     # dikunci pindaan (ag)
MINGGU_MIN, TAHUN_MIN = 0.80, 0.50
BAHAGIAN = ('asal', 'K')
LARANG_PASARAN = ('QG01', 'QG02', 'QG03', 'QG04')                    # kalendar
LARANG_KUMPULAN = ('QF01', 'QF02', 'QF03', 'QF04', 'QF07')           # bergantung pada TARIKH laporan kewangan
JULAT = {'A': (20100104, 20241231, 2010, 2024), 'B': (20100104, 20260828, 2010, 2025)}   # mula, akhir, tahun penuh pertama / akhir
TAHUN_SET = {'A': 15.0, 'B': s11.TAHUN}
MIN_TAHUN_N = 20                                                     # belian minimum setahun bagi semakan ikut tahun
S_HENTI = d13.S_HENTI
PUS, ID_MULA, TARIKH_DAFTAR = 'CS20', 2055, '2026-11-17'
N_PAPAR = 60
AUDIT = ('j5', 'a_j5', 'arah', 'arah_K1', 'arah_K2', 'arah_K3', 'n_B', 'menang_B', 'a_menang_B', 'purata_B', 'a_purata_B', 'rugi15_B',
         'a_rugi15_B', 'menangx_K3', 'puratax_K3')
F_ = lambda kerja, nama: os.path.join(kerja, f'cs20_{nama}.pkl')
_EV = {}


def semua_pencetus(kerja, set_):
    if set_ not in _EV:
        ev = {}
        for bhg in BAHAGIAN:
            ev.update(t7.semua_ev(kerja, set_, bhg))
        _EV[set_] = ev
    return _EV[set_]


def dibenar():
    """bool[NQ]: gabungan (prasyarat pasaran, prasyarat kumpulan / syarikat) yang dibenarkan pusingan ini."""
    l1 = [i for i, x in enumerate(lapis.PASARAN) if x[:4] in LARANG_PASARAN]
    l2 = [i for i, x in enumerate(lapis.KUMPULAN) if x[:4] in LARANG_KUMPULAN]
    assert len(l1) == len(LARANG_PASARAN) and len(l2) == len(LARANG_KUMPULAN)
    q = np.arange(c5.NQ)
    return ~(np.isin(q // c5.NQ2 - 1, l1) | np.isin(q % c5.NQ2 - 1, l2))


def larang_q(q1, q2):
    return (q1 >= 0 and lapis.PASARAN[q1][:4] in LARANG_PASARAN) or (q2 >= 0 and lapis.KUMPULAN[q2][:4] in LARANG_KUMPULAN)


# ---------- kekerapan mingguan ----------
def minggu(hari_unik, set_):
    """Minggu kalendar (Isnin-Jumaat) dalam julat set: idx = indeks minggu setiap HARI (-1 di luar julat), kunci = tarikh Isnin
    setiap minggu, thn = tahun (ikut Isnin), penuh = tahun kalendar penuh."""
    a, z, y0, y1 = JULAT[set_]
    hu = np.asarray(hari_unik)
    d = pd.to_datetime(pd.Series(hu).astype(str))
    isnin = (d - pd.to_timedelta(d.dt.weekday, unit='D')).dt.strftime('%Y%m%d').astype(int).to_numpy()
    dalam = (hu >= a) & (hu <= z)
    kunci, inv = np.unique(isnin[dalam], return_inverse=True)
    idx = np.full(len(hu), -1, np.int64)
    idx[dalam] = inv
    return dict(idx=idx, kunci=kunci, thn=kunci // 10000, n=len(kunci), penuh=list(range(y0, y1 + 1)))


def kekerapan(M, hari_e):
    """(bahagian minggu yang ada belian, bahagian pada tahun penuh paling teruk, kunci minggu yang ada belian)."""
    w = np.unique(M['idx'][np.asarray(hari_e, np.int64)])
    w = w[w >= 0]
    ada = np.zeros(M['n'], bool)
    ada[w] = True
    return float(ada.mean()), float(min(ada[M['thn'] == y].mean() for y in M['penuh'])), M['kunci'][w]


def kerap(mg, mt):
    return bool(mg >= MINGGU_MIN and mt >= TAHUN_MIN)


def entri(pan, ev):
    """Belian satu posisi setiap saham (pegang 20 sesi + stop loss), seperti `s11.ukur_tangkap`."""
    ev = np.ascontiguousarray(ev, dtype=np.int64)
    _, sk, _ = s11.jual20(ev, pan['o'], pan['l'], pan['c'], pan['atr'], S_HENTI)
    return ev[teras.satu_posisi(ev, sk, pan['tid'])]


# ---------- skor (kumpulan A) ----------
def _skor_satu(nama):
    pan, ev = c5._G['pan'], c5._G['ev'][nama]
    tp = pan['tempoh'][ev].astype(np.int64)
    out = {'n_ev': (int((tp == 0).sum()), int((tp == 1).sum()))}
    if min(out['n_ev']) < c5.N_MIN:
        return nama, dict(out, cukup=False)
    V = np.ascontiguousarray(c5._G['V'][ev])
    Acc = np.zeros((c5.NQ, c5.NC, 2, 4))
    c5.kumpul5(tp, V, np.ascontiguousarray(c5._G['FS'][:, ev].T), np.ascontiguousarray(c5._G['L1'][:, ev].T),
               np.ascontiguousarray(c5._G['L2'][:, ev].T), c5.PASANG, Acc)
    ok, sp, _ = c5.skor_acc(Acc)
    n = Acc[..., 0].sum(-1)
    with np.errstate(invalid='ignore'):
        boleh = ok & c5._G['dibenar'][:, None] & (n >= c5._G['n_min']) & (sp > 0)
    sm = np.where(boleh, sp, -np.inf)
    out.update(cukup=True, n_ok=int(ok.sum()), n_boleh=int(boleh.sum()), atas=c5._atas(sm, N_TINJAU),
               skor0=float(sp[0, 0]) if ok[0, 0] else np.nan)
    return nama, out


def skor(kerja):
    """Skor setiap isyarat beli pada kumpulan A (sasaran `terus`); simpan sehingga N_TINJAU peraturan DIBENARKAN berskor > 0
    yang cukup isyarat untuk syarat kekerapan -> cs20_skor.pkl."""
    f = F_(kerja, 'skor')
    siap = pickle.load(open(f, 'rb')) if os.path.exists(f) else {}
    ev = semua_pencetus(kerja, 'A')
    tugas = sorted([n for n in ev if n not in siap], key=lambda n: -len(ev[n]))
    pan = cari.panel(kerja, 'A')
    M = minggu(pan['hari_unik'], 'A')
    cari.log(f"CS20 skor: {len(tugas)} isyarat beli (siap {len(siap)}); minggu A {M['n']}; gabungan prasyarat dibenarkan "
             f"{int(dibenar().sum())} daripada {c5.NQ}")
    if tugas:
        L = lapis.muat(kerja, 'A')
        c5._G.update(pan=pan, ev=ev, V=t7.label_terus(pan), FS=np.ascontiguousarray(pan['F'][c5.SAHAM]), L1=L['L1'], L2=L['L2'],
                     dibenar=dibenar(), n_min=int(np.ceil(MINGGU_MIN * M['n'])))
        c5.kumpul5(np.zeros(1, np.int64), np.zeros((1, 3)), np.zeros((1, c5.NS), np.uint8), np.zeros((1, lapis.N1), np.uint8),
                   np.zeros((1, lapis.N2), np.uint8), c5.PASANG, np.zeros((c5.NQ, c5.NC, 2, 4)))       # kompil sebelum fork
        t0 = time.time()
        with mp.get_context('fork').Pool(cari.PEKERJA) as pool:
            for k, (n, r) in enumerate(pool.imap_unordered(_skor_satu, tugas), 1):
                siap[n] = r
                if k % 100 == 0:
                    cari.log(f'  {k}/{len(tugas)} · {time.time() - t0:.0f}s')
                    pickle.dump(siap, open(f + '.tmp', 'wb'), protocol=4)
                    os.replace(f + '.tmp', f)
    pickle.dump(siap, open(f, 'wb'), protocol=4)
    cukup = [r for r in siap.values() if r.get('cukup')]
    cari.log(f"CS20 skor siap: {len(cukup)} cukup isyarat daripada {len(siap)}; {sum(1 for r in cukup if len(r['atas'][0]))} ada "
             'peraturan dibenarkan berskor > 0')
    return siap


# ---------- calon dan kawalan (kumpulan A) ----------
def calon(kerja):
    """Calon = sehingga N_ATAS peraturan berskor > 0 tertinggi setiap isyarat beli antara yang dibenarkan DAN menepati syarat
    kekerapan pada A; kawalan = N_KAWALAN peraturan rawak daripada ruang yang sama yang menepati syarat yang sama.
    -> cs20_calon.pkl"""
    S = pickle.load(open(F_(kerja, 'skor'), 'rb'))
    pan = cari.panel(kerja, 'A')
    L = lapis.muat(kerja, 'A')
    Lr = (L['L1'], L['L2'])
    EV = semua_pencetus(kerja, 'A')
    M = minggu(pan['hari_unik'], 'A')
    n_min = int(np.ceil(MINGGU_MIN * M['n']))
    R, tinjau, t0 = [], 0, time.time()
    for k, (nama, r) in enumerate(sorted(S.items()), 1):
        if not r.get('cukup') or not len(r['atas'][0]):
            continue
        idx, sk = r['atas']
        q1, q2, f1, f2 = c5.nyah(idx)
        ev, dapat = EV[nama], 0
        for j in range(len(idx)):
            if dapat >= N_ATAS:
                break
            tinjau += 1
            e = entri(pan, ev[c5.topeng(pan, Lr, ev, int(q1[j]), int(q2[j]), int(f1[j]), int(f2[j]))])
            mg, mt, _ = kekerapan(M, pan['hari'][e])
            if kerap(mg, mt):
                dapat += 1
                R.append(dict(pencetus=nama, induk=t7.induk(nama), ke=dapat, kedudukan_skor=j + 1, skor=float(sk[j]), q1=int(q1[j]),
                              q2=int(q2[j]), f1=int(f1[j]), f2=int(f2[j]), skor0=r['skor0'], n_E1=r['n_ev'][0], n_E2=r['n_ev'][1],
                              mgg_A=mg, mgg_min_A=mt))
        if k % 200 == 0:
            cari.log(f'  CS20 calon {k}/{len(S)} · {len(R)} calon · {tinjau} peraturan ditinjau · {time.time() - t0:.0f}s')
    T = pd.DataFrame(R).sort_values(['skor', 'pencetus', 'ke'], ascending=[False, True, True], kind='stable').reset_index(drop=True)
    T.insert(0, 'id', [f'W{i + 1:04d}' for i in range(len(T))])
    cukup = sorted(n for n, r in S.items() if r.get('cukup'))
    q_boleh = np.flatnonzero(dibenar())
    rng = np.random.default_rng(BENIH_KAWALAN)
    K, cuba = [], 0
    while len(K) < N_KAWALAN and cuba < CUBA_KAWALAN:
        cuba += 1
        nama = cukup[int(rng.integers(len(cukup)))]
        q = int(q_boleh[int(rng.integers(len(q_boleh)))])
        ci = int(rng.integers(c5.NC))
        if q == 0 and ci == 0:
            continue
        q1, q2, f1, f2 = (int(x[0]) for x in c5.nyah(np.asarray([q * c5.NC + ci])))
        ev = EV[nama]
        ev = ev[c5.topeng(pan, Lr, ev, q1, q2, f1, f2)]
        if len(ev) < n_min:
            continue
        tp = pan['tempoh'][ev]
        if min(int((tp == 0).sum()), int((tp == 1).sum())) < c5.N_MIN:
            continue
        mg, mt, _ = kekerapan(M, pan['hari'][entri(pan, ev)])
        if not kerap(mg, mt):
            continue
        K.append(dict(id=f'R{len(K) + 1:03d}', pencetus=nama, induk=t7.induk(nama), ke=0, kedudukan_skor=0, skor=np.nan, q1=q1, q2=q2,
                      f1=f1, f2=f2, skor0=np.nan, n_E1=int((tp == 0).sum()), n_E2=int((tp == 1).sum()), mgg_A=mg, mgg_min_A=mt))
    out = {'calon': T, 'kawalan': pd.DataFrame(K), 'n_pencetus': len(S), 'n_cukup': len(cukup), 'cuba_kawalan': cuba, 'tinjau': tinjau,
           'n_ada_boleh': sum(1 for r in S.values() if r.get('cukup') and len(r['atas'][0]))}
    pickle.dump(out, open(F_(kerja, 'calon'), 'wb'), protocol=4)
    cari.log(f"CS20 calon: {len(T)} calon daripada {T.pencetus.nunique() if len(T) else 0} isyarat beli ({tinjau} peraturan ditinjau); "
             f"kawalan rawak {len(K)} (dicuba {cuba})")
    return out


# ---------- semakan pada kumpulan B ----------
def f_sedia(kerja, set_, pan, EV, Lr):
    """Kod F sedia ada yang boleh menjadi kembar setup sepanjang tahun: (id, isyarat, nama, prasyarat, penapis). Setup lama
    kedudukan akhir (takrif pusingan masing-masing) + kod CS13 tanpa prasyarat yang dilarang. Yang isyaratnya tiada dalam folder
    kerja (varian M CS07) dilangkau."""
    import cs_cs07 as c7
    import cs_lapor as lapor
    import cs_portfolio6 as p6
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('').set_index('id')
    KA = pd.read_csv(os.path.join(SINI, 'hasil', 'KEDUDUKAN_AKHIR.csv')).set_index('id')
    kq1, kq2 = [x[:4] for x in lapis.PASARAN], [x[:4] for x in lapis.KUMPULAN]
    out, langkau = [], []
    for i in KA.index:
        r = reg.loc[i]
        try:
            d = c7.dari_takrif7(r.takrif) if r.pusingan == 'CS07' else p6.dari_takrif5(r.takrif)
            ev = EV[d['pencetus']]
        except Exception:
            langkau.append(i)
            continue
        if larang_q(int(d['q1']), int(d['q2'])):
            continue
        pra = KA.loc[i, 'prasyarat']
        pen = str(KA.loc[i, 'penapis']).strip()
        out.append((i, ev[c5.topeng(pan, Lr, ev, d['q1'], d['q2'], d['f1'], d['f2'])], str(KA.loc[i, 'pencetus']),
                    pra if isinstance(pra, str) and pra.strip() not in ('', '–') else '', '' if pen in ('', '–', 'nan') else pen))
    for i, r in reg[reg.pusingan == 'CS13'].iterrows():
        b = r.takrif.split('|')
        kod = [x for x in b[4].split('+') if x] if len(b) > 4 else []
        q1 = next((kq1.index(x) for x in kod if x in kq1), -1)
        q2 = next((kq2.index(x) for x in kod if x in kq2), -1)
        if larang_q(q1, q2):
            continue
        if b[0] not in EV:
            langkau.append(i)
            continue
        fs = [int(x[1:]) - 1 for x in b[1].split('+') if x] + [-1, -1]
        ev = EV[b[0]]
        out.append((i, ev[c5.topeng(pan, Lr, ev, q1, q2, fs[0], fs[1])], r.masuk, r.prasyarat if r.prasyarat != 'tiada' else '', r.syarat))
    return out, langkau


def kunci(kerja):
    """Nilai setiap calon, setiap kawalan dan kod F sepanjang tahun sedia ada dengan setup lengkap yang SAMA pada kumpulan B
    (+ belian dan kekerapan pada A) -> cs20_kunci.pkl"""
    import cs_audit19 as a19
    C = pickle.load(open(F_(kerja, 'calon'), 'rb'))
    semua_ = pd.concat([C['calon'], C['kawalan']], ignore_index=True)
    param = t7.param_semua(kerja)
    out, t0, langkau = {}, time.time(), []
    kosong = np.zeros(0, np.int32)
    for set_ in ('B', 'A'):
        pan = cari.panel(kerja, set_)
        L = lapis.muat(kerja, set_)
        Lr = (L['L1'], L['L2'])
        EV = semua_pencetus(kerja, set_)
        Lab, As = s11.asas(pan)
        M = minggu(pan['hari_unik'], set_)
        Bt = A19 = None
        if set_ == 'B':
            Bt = s11.siri_trend(pan)
            df, _, A19 = a19.bina_bebas()
            assert len(pan['c']) == len(df) and (pan['tarikh'] == A19['tarikh']).all()
            del df

        def nilai(idn, ev):
            d, e = s11.ukur_tangkap(pan, Lab, As, ev, S_HENTI)
            o = out.setdefault(idn, {})
            mg, mt, w = kekerapan(M, pan['hari'][e])
            o['e_' + set_], o['es_' + set_], o['w_' + set_] = e.astype(np.int32), kosong, w.astype(np.int32)
            o['mgg_' + set_], o['mgg_min_' + set_] = mg, mt
            if set_ == 'B':
                x = Lab[e, 1].astype(float) - As[e, 1]
                g = pd.Series(x).groupby(pan['tarikh'][e] // 10000).agg(['size', 'mean'])
                g = g[g['size'] >= MIN_TAHUN_N]
                da = a19.ukur(A19, np.ascontiguousarray(ev[A19['sah'][ev]], dtype=np.int64))[0]
                o.update(d=d, L=d13.lengkap(pan, Bt, ev), tahun_n=int(len(g)), tahun_pos=float((g['mean'] > 0).mean()) if len(g) else np.nan,
                         audit={k_: da.get(k_, np.nan) for k_ in AUDIT})
            return o

        for k, r in enumerate(semua_.itertuples(), 1):
            ev = EV[r.pencetus]
            o = nilai(r.id, ev[c5.topeng(pan, Lr, ev, r.q1, r.q2, r.f1, r.f2)])
            if set_ == 'B':
                o.update(nama=t7.nama7(r.pencetus, param), prasyarat=d13.teks_pra(r.q1, r.q2), penapis=d13.teks_pen(r.f1, r.f2))
            if k % 500 == 0:
                cari.log(f'  CS20 kunci {set_} {k}/{len(semua_)} · {time.time() - t0:.0f}s')
        F, lk = f_sedia(kerja, set_, pan, EV, Lr)
        langkau = sorted(set(langkau) | set(lk))
        for idn, ev, nama, pra, pen in F:
            o = nilai(idn, ev)
            if set_ == 'B':
                o.update(nama=nama, prasyarat=pra, penapis=pen)
    out['_n'] = {s: len(cari.panel(kerja, s)['c']) for s in ('A', 'B')}
    out['_langkau'] = langkau
    pickle.dump(out, open(F_(kerja, 'kunci'), 'wb'), protocol=4)
    cari.log(f"CS20 kunci: {len(out) - 2} peraturan · kod F sedia ada dilangkau (isyarat tiada) {len(langkau)} · {time.time() - t0:.0f}s")
    return out


def semua(kerja):
    """(C, K, T, bacaan). T = satu baris setiap calon, kawalan dan kod F sepanjang tahun sedia ada (angka kumpulan B) + lajur
    kekerapan, semakan ikut tahun, ukuran audit, kembar, takrif dan kod F."""
    import cs_lapor as lapor
    C = pickle.load(open(F_(kerja, 'calon'), 'rb'))
    K = pickle.load(open(F_(kerja, 'kunci'), 'rb'))
    Kd = {k_: v for k_, v in K.items() if not k_.startswith('_')}
    T = d13.jadual(C, Kd).drop(columns=['shariah_setahun', 'menang_B', 'purata_B', 'rugi15_B', 'n_B'])
    g = lambda k_: [Kd[i].get(k_, np.nan) for i in T.id]
    for k_ in ('mgg_A', 'mgg_min_A', 'mgg_B', 'mgg_min_B', 'tahun_n', 'tahun_pos'):
        T[k_] = g(k_)
    for k_ in AUDIT:
        T[k_] = [Kd[i]['audit'].get(k_, np.nan) for i in T.id]
    n_w = len(minggu_kunci('A'))                                  # minggu 2010-2024: kekerapan pada SEMUA saham (A + B)
    w15 = lambda i: len(np.union1d(Kd[i]['w_A'], Kd[i]['w_B'][Kd[i]['w_B'] <= JULAT['A'][1]])) / n_w
    T['mgg_semua'] = [w15(i) for i in T.id]
    T['setahun_semua'] = [len(Kd[i]['e_A']) / TAHUN_SET['A'] + len(Kd[i]['e_B']) / TAHUN_SET['B'] for i in T.id]
    T['kerap_B'] = (T.mgg_B >= MINGGU_MIN) & (T.mgg_min_B >= TAHUN_MIN)
    B = d13.bacaan(T)
    c = T[(T.peranan == 'calon') & T.layak]
    kw = T[(T.peranan == 'kawalan') & T.layak]
    B.update(tahun_pos_lulus=float(c[c.lulus].tahun_pos.median()) if c.lulus.any() else np.nan,
             tahun_pos_kawalan=float(kw.tahun_pos.median()) if len(kw) else np.nan,
             kerap_B_lulus=float(c[c.lulus].kerap_B.mean()) if c.lulus.any() else np.nan)
    T2 = T.copy()
    T2['lulus'] = T2.lulus & T2.kerap_B
    kb = d13.kembar(T2, K)
    T['kembar_kepada'] = [kb.get(i, '') if p == 'calon' else '' for i, p in zip(T.id, T.peranan)]
    T['takrif'] = [d13.takrif13(r.pencetus, int(r.q1), int(r.q2), int(r.f1), int(r.f2)) if r.peranan == 'calon' else '' for r in T.itertuples()]
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('')
    peta = dict(zip(reg.takrif[reg.pusingan == PUS], reg.id[reg.pusingan == PUS]))
    T['id_F'] = [peta.get(t, '') if p == 'calon' else (i if p == 'F' else '') for t, p, i in zip(T.takrif, T.peranan, T.id)]
    T['untuk_daftar'] = (T.peranan == 'calon') & T.lulus & T.kerap_B & (T.kembar_kepada == '')
    return C, K, T, B


_MK = {}


def minggu_kunci(set_):
    """Kunci minggu (tarikh Isnin) dalam julat set, daripada kalendar hari bekerja (tanpa panel): untuk penyebut kekerapan
    gabungan A + B."""
    if set_ not in _MK:
        a, z = JULAT[set_][:2]
        d = pd.bdate_range(str(a), str(z))
        _MK[set_] = np.unique((d - pd.to_timedelta(d.weekday, unit='D')).strftime('%Y%m%d').astype(int))
    return _MK[set_]


# ---------- pendaftaran ----------
def daftar(kerja):
    """Daftar setiap calon lulus yang menepati syarat kekerapan pada B dan bukan kembar ke data/registry_F.csv (kod F2055 dst.,
    ikut susunan skor A). HANYA jika bacaan dikunci lulus. Baris sedia ada tidak disentuh. Pulangkan bilangan kod baharu."""
    import cs_lapor as lapor
    C, K, T, B = semua(kerja)
    if not B['ya']:
        cari.log('CS20 daftar: bacaan dikunci TIDAK lulus -> tiada kod F baharu')
        return 0
    param = t7.param_semua(kerja)
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('').reindex(columns=lapor.LAJUR_F, fill_value='')
    ada, seterusnya, baharu = set(reg.takrif), max(int(x[1:]) for x in reg.id) + 1, []
    assert seterusnya >= ID_MULA
    for r in T[T.untuk_daftar].sort_values('skor_A', ascending=False, kind='stable').itertuples():
        if r.takrif in ada:
            continue
        q1, q2, f1, f2 = int(r.q1), int(r.q2), int(r.f1), int(r.f2)
        masuk = t7.nama7(r.pencetus, param)
        P = param.get(r.pencetus) if r.pencetus[0] in 'MN' else dict(t7._GRID[r.pencetus][1]) if r.pencetus[0] == 'K' else None
        b = dict.fromkeys(lapor.LAJUR_F, '')
        b.update(id=f'F{seterusnya:02d}', keluarga='F', pusingan=PUS, tarikh_daftar=TARIKH_DAFTAR, takrif=r.takrif,
                 param=json.dumps({a: (round(x, 6) if isinstance(x, float) else x) for a, x in P.items()}, sort_keys=True) if P else '',
                 masuk=masuk, penapis=c5.tk_pen(f1, f2), henti=f'{d13.KOD_HENTI} {k7.HENTI[S_HENTI]}',
                 keluar=d13.TEKS_PEGANG, skor_tepat=f'{r.skor_A:.5f}', status='BACKTEST',
                 prasyarat=c5.buang_kod(c5.tk_pra(q1, q2)).replace(' DAN ', ' + '),
                 syarat=c5.buang_kod(c5.tk_pen(f1, f2)).replace(' DAN ', ' + '))
        jum = bil = 0.0
        for j, t in enumerate(('K1', 'K2', 'K3'), 1):
            n = int(getattr(r, f'n_B_K{j}'))
            b[f'n_{t}'] = str(n)
            if n:
                m = float(getattr(r, f'menang_B_K{j}'))
                b.update({f'purata_{t}': f"{getattr(r, f'purata_B_K{j}'):.5f}", f'k10_{t}': f"{getattr(r, f'k10_B_K{j}'):.4f}",
                          f'menang_{t}': f'{m:.4f}'})
                jum, bil = jum + n * float(f'{m:.4f}'), bil + n
        b['menang'] = f'{jum / bil:.4f}' if bil else ''
        baharu.append(b)
        ada.add(r.takrif)
        seterusnya += 1
    if baharu:
        reg = pd.concat([reg, pd.DataFrame(baharu)[lapor.LAJUR_F].astype(str)], ignore_index=True)
        reg['_n'] = reg.id.str[1:].astype(int)
        reg.sort_values('_n').drop(columns='_n').to_csv(lapor.REG_F, index=False)
    cari.log(f"CS20 daftar: {len(baharu)} kod F baharu ({baharu[0]['id']}–{baharu[-1]['id']})" if baharu else 'CS20 daftar: tiada yang baharu')
    return len(baharu)


# ---------- laporan ----------
def lapor_(kerja):
    import cs_lapor as lapor
    C, K, T, B = semua(kerja)
    d_ = os.path.join(SINI, 'hasil', PUS)
    os.makedirs(d_, exist_ok=True)
    c, kw, fl = T[T.peranan == 'calon'], T[T.peranan == 'kawalan'], T[T.peranan == 'F']
    c.drop(columns=['peranan']).to_csv(os.path.join(d_, 'calon.csv.gz'), index=False, float_format='%.5f')
    kw.drop(columns=['peranan', 'kembar_kepada', 'takrif', 'id_F', 'untuk_daftar']).to_csv(os.path.join(d_, 'kawalan.csv'), index=False,
                                                                                         float_format='%.5f')
    L = c[c.lulus]
    LK = L[L.kerap_B]
    D = c[c.untuk_daftar]
    U = c[c.id_F != ''].sort_values(['kl_terus', 'terus'], ascending=False, kind='stable').reset_index(drop=True)
    U.insert(0, 'kedudukan', np.arange(1, len(U) + 1))
    lajur_u = ['kedudukan', 'id_F', 'prasyarat', 'nama', 'penapis', 'n', 'tahun', 'setahun_semua', 'mgg_semua', 'mgg_B', 'mgg_min_B',
               'terus', 'a_terus', 'kl_terus', 'kl_terus_K1', 'kl_terus_K2', 'kl_terus_K3', 'tahun_pos', 'tahun_n', 'm5', 'a_m5', 'j5',
               'a_j5', 'arah', 'n_B', 'menang_B', 'a_menang_B', 'purata_B', 'a_purata_B', 'rugi15_B', 'a_rugi15_B', 'menangx_K3',
               'puratax_K3', 'hari_B', 'jual_hari_beli', 'skor_A', 'takrif']
    U[lajur_u].rename(columns={'id_F': 'id'}).to_csv(os.path.join(d_, 'mingguan.csv'), index=False, float_format='%.5f')
    bersih = lambda v: None if isinstance(v, float) and v != v else v
    json.dump({k_: bersih(v) for k_, v in dict(
        B, n_isyarat=C['n_pencetus'], n_cukup=C['n_cukup'], n_ada_boleh=C['n_ada_boleh'], tinjau=C['tinjau'], cuba_kawalan=C['cuba_kawalan'],
        n_kawalan=len(kw), n_lulus_kerap=len(LK), n_kembar=int((LK.kembar_kepada != '').sum()), n_untuk_daftar=len(D), n_berdaftar=len(U),
        n_f_sedia=len(fl), f_dilangkau=len(K.get('_langkau', [])), minggu_min=MINGGU_MIN, tahun_min=TAHUN_MIN).items()},
        open(os.path.join(d_, 'bacaan.json'), 'w'), indent=1, sort_keys=True)
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    p = lambda x, k=0, t=False: '–' if x is None or x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')
    tx = lambda s: s if isinstance(s, str) and s.strip() else '–'
    idf = sorted(U.id_F, key=lambda x: int(x[1:]))
    A = ['# CS20: setup "sepanjang tahun" — membeli hampir setiap minggu (backtest; BUKAN bukti)', '', status, '',
         'Dijana `kajian/carian_setup/cs_mingguan20.py`. Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 17 Nov 2026 (ag). '
         '**Jangan sunting secara manual.**', '',
         '## 1. Apa yang dibuat', '',
         '- Carian yang sama dengan CS13 (kayu ukur = KADAR TANGKAP: naik ≥ 5 % minggu pertama, naik lagi hingga minggu ke-4, −8 % tidak '
         'disentuh), dengan dua had: prasyarat yang bergantung pada tarikh laporan kewangan atau pada kalendar TIDAK dibenarkan, dan setiap '
         f"setup mesti membeli dalam ≥ {MINGGU_MIN:.0%} minggu (≥ {TAHUN_MIN:.0%} minggu pada tahun paling teruk), diukur pada separuh saham.",
         f"- {C['n_pencetus']:,} isyarat beli (kaedah M dan N dalam mod tanpa intai, indikator dan variannya; {C['n_cukup']:,} cukup isyarat) × "
         f"prasyarat yang dibenarkan × penapis saham. {C['tinjau']:,} peraturan ditinjau mengikut susunan skor; **{B['n_calon']:,} calon** "
         f"(sehingga {N_ATAS} setiap isyarat beli) menepati syarat kekerapan pada saham carian.",
         '- Setup lengkap: beli pada buka esok; stop loss 4xATR14; pegang sekurang-kurangnya 20 hari, kemudian jual bila tutup di bawah purata '
         '20 hari; paling lama 6 bulan (cara pegang B).',
         '- "Lulus" = pada saham yang carian tidak lihat: belian ≥ 300, ≥ 10 tahun aktif, dan kadar tangkap melebihi saham rawak hari sama '
         'dalam KETIGA-TIGA tempoh (2010–19, 2020–24, 2025–26).', '',
         '## 2. Ujian (ditetapkan dahulu)', '',
         f"- Kawalan = {len(kw)} peraturan rawak daripada ruang yang SAMA yang juga membeli hampir setiap minggu (dicuba {C['cuba_kawalan']:,}).",
         f"- **B1** kadar lulus: calon **{p(B['lulus_calon'])} %** lawan kawalan {p(B['lulus_kawalan'])} % (perlu beza ≥ 20 mata) → "
         f"{'lulus' if B['b1'] else 'GAGAL'}.",
         f"- **B2** lebih baik daripada rawak pada 2025–26: calon **{p(B['k3_calon'])} %** lawan kawalan {p(B['k3_kawalan'])} % (perlu ≥ 60 % "
         f"dan beza ≥ 10 mata) → {'lulus' if B['b2'] else 'GAGAL'}.",
         f"- **Keputusan: carian setup sepanjang tahun {'BERHASIL — kod F didaftarkan' if B['ya'] else 'TIDAK berhasil — tiada kod F baharu'}.**",
         f"- Semakan ikut tahun (dilaporkan, bukan syarat): calon lulus lebih baik daripada rawak dalam {p(B['tahun_pos_lulus'])} % tahun "
         f"(nilai tengah); kawalan {p(B['tahun_pos_kawalan'])} %.", '',
         '## 3. Berapa yang lulus dan didaftarkan', '',
         f"- Lulus: **{len(L):,}** daripada {B['n_calon']:,} calon; {len(LK):,} daripadanya juga membeli hampir setiap minggu pada saham yang "
         'carian tidak lihat.',
         f"- Kembar setup lain (pertindihan belian ≥ {d13.JACCARD:.0%}; termasuk kembar kod F sedia ada): {int((LK.kembar_kepada != '').sum()):,} "
         f"({int(LK.kembar_kepada.str.startswith('F').sum())} kembar kod F sedia ada) — tidak diberi kod.",
         f"- **Setup berlainan yang lulus: {len(D):,}**" + (f" → didaftarkan sebagai **`{idf[0]}`–`{idf[-1]}`** ({len(idf):,} kod baharu)."
                                                            if idf else ' (belum / tidak didaftarkan).'),
         f"- Anggaran bahagian yang lulus kerana nasib (kadar lulus kawalan ÷ kadar lulus calon): kira-kira {p(B['nasib'])} %.", '',
         '## 4. Ikut tempoh (peraturan yang cukup belian; saham yang carian tidak lihat)', '',
         '| Kumpulan | Bilangan | Lebih baik daripada rawak: 2010–19 | 2020–24 | **2025–26** | Median kelebihan tangkap 2010–19 / 2020–24 / 2025–26 '
         '(mata) | Lulus |', '|---' * 7 + '|']
    for nm, X in (('Calon', c), ('Kawalan rawak (ruang sama)', kw), ('Kod F sepanjang tahun sedia ada', fl), ('Kod baharu', U)):
        e = X[X.layak]
        if len(e):
            A.append(f"| {nm} | {len(e):,} | {(e.kl_terus_K1 > 0).mean():.0%} | {(e.kl_terus_K2 > 0).mean():.0%} | **{(e.kl_terus_K3 > 0).mean():.0%}** | "
                     f"{p(e.kl_terus_K1.median(), 1, True)} / {p(e.kl_terus_K2.median(), 1, True)} / {p(e.kl_terus_K3.median(), 1, True)} | {e.lulus.mean():.0%} |")
    A += ['', '## 5. Mutu (nilai tengah setiap kumpulan; saham yang carian tidak lihat; kurungan = saham rawak hari sama)', '',
          '| Kumpulan | Bilangan | Tangkap % | Naik ≥ 5 % minggu 1 | JATUH ≥ 5 % minggu 1 | Menang % cara B (rawak dipegang sama) | Purata % cara B '
          '(rawak dipegang sama) | Rugi ≥ 15 % | Minggu ada belian |', '|---' * 9 + '|']
    for nm, X in (('Kod baharu', U), ('Calon lulus', L), ('Kawalan rawak (ruang sama)', kw[kw.layak]), ('Kod F sepanjang tahun sedia ada', fl[fl.layak])):
        if len(X):
            g = X.median(numeric_only=True)
            A.append(f"| {nm} | {len(X):,} | {p(g.terus, 1)} ({p(g.a_terus, 1)}) | {p(g.m5)} ({p(g.a_m5)}) | {p(g.j5)} ({p(g.a_j5)}) | "
                     f"{p(g.menang_B)} ({p(g.a_menang_B)}) | {p(g.purata_B, 1, True)} ({p(g.a_purata_B, 1, True)}) | {p(g.rugi15_B)} ({p(g.a_rugi15_B)}) | "
                     f"{p(g.mgg_B)} % |")
    if len(U):
        A += ['', '## 6. Kod baharu: pecahan', '',
              f"- Dengan prasyarat pasaran: {int((U.q1 >= 0).sum()):,}; dengan prasyarat kumpulan / syarikat: {int((U.q2 >= 0).sum()):,}; tanpa "
              f"apa-apa prasyarat: {int(((U.q1 < 0) & (U.q2 < 0)).sum()):,}.",
              '- Prasyarat paling kerap: ' + '; '.join(f'{k_ or "tiada"} ({v})' for k_, v in U.prasyarat.value_counts().head(8).items()) + '.',
              '- Penapis saham paling kerap: ' + '; '.join(f'{k_ or "tiada"} ({v})' for k_, v in U.penapis.value_counts().head(8).items()) + '.',
              f"- Isyarat beli: {U.induk.nunique()} kaedah / keluarga berbeza; paling kerap " +
              ', '.join(f'{k_} ({v})' for k_, v in U.induk.value_counts().head(8).items()) + '.',
              f"- Kelebihan tangkap > 0 pada 2025–26: {int((U.kl_terus_K3 > 0).sum()):,} daripada {len(U):,} (syarat lulus, jadi bukan bukti di "
              'luar sampel).',
              f"- `arah` > 0 (tambahan naik melebihi tambahan jatuh): {int((U.arah > 0).sum()):,} daripada {len(U):,}; menang cara B melebihi "
              f"saham rawak yang dipegang sama: {int((U.menang_B > U.a_menang_B).sum()):,}; purata melebihi: {int((U.purata_B > U.a_purata_B).sum()):,}.",
              f"- Jualan pada hari beli: {int(U.jual_hari_beli.sum())} (mesti 0).", '',
              f'## 7. Kod baharu (teratas {min(N_PAPAR, len(U))} ikut kelebihan tangkap; senarai penuh `mingguan.csv`)', '',
              '| # | ID | Prasyarat | Isyarat beli | Penapis saham | Beli setahun (semua saham) | Minggu ada belian | **Tangkap %** (rawak) | '
              'Naik ≥ 5 % (rawak) | Jatuh ≥ 5 % (rawak) | Menang % (rawak) | Purata % (rawak) | 2025–26 |', '|---' * 13 + '|']
        for r in U.head(N_PAPAR).itertuples():
            A.append(f"| {r.kedudukan} | `{r.id_F}` | {tx(r.prasyarat)} | {r.nama} | {tx(r.penapis)} | {r.setahun_semua:.0f} | {p(r.mgg_semua)} % | "
                     f"**{p(r.terus, 1)}** ({p(r.a_terus, 1)}) | {p(r.m5)} ({p(r.a_m5)}) | {p(r.j5)} ({p(r.a_j5)}) | {p(r.menang_B)} ({p(r.a_menang_B)}) | "
                     f"{p(r.purata_B, 1, True)} ({p(r.a_purata_B, 1, True)}) | {p(r.kl_terus_K3, 1, True)} |")
    A += ['', '## 8. Kaveat', '',
          '- Kelebihan setup sepanjang tahun kecil berbanding setup "laporan kewangan" (senarai utama CS13: tangkap kira-kira dua kali rawak).',
          '- 2025–26 ialah syarat lulus, bukan tempoh di luar sampel; bukti bersih hanya papertrade.',
          '- Beribu calon disemak pada saham yang sama, jadi sebahagian lulus kerana nasib (anggaran di §3).',
          '- "Minggu ada belian" pada lajur jadual §7 = semua saham (2010–2024); syarat kekerapan diukur pada separuh saham.',
          '- Tiada saham delist dalam data (condong ke atas). Backtest sahaja; tiada papertrade tanpa keputusan pengguna; kad skor kekal '
          'satu-satunya keputusan wang sebenar.', '']
    open(os.path.join(d_, 'MINGGUAN.md'), 'w', encoding='utf-8').write('\n'.join(A))
    cari.log(f"CS20 lapor: calon {B['n_calon']}, layak {B['calon_layak']}, lulus {B['n_lulus']} ({B['lulus_calon']:.0%} lawan kawalan "
             f"{B['lulus_kawalan']:.0%}); K3 {B['k3_calon']:.0%} lawan {B['k3_kawalan']:.0%} -> {'BERHASIL' if B['ya'] else 'TIDAK'}; lulus + kerap "
             f"{len(LK)}, kembar {int((LK.kembar_kepada != '').sum())}, untuk daftar {len(D)}, berdaftar {len(U)}")
    return T, B, U


if __name__ == '__main__':
    cmd, kerja = sys.argv[1], sys.argv[2]
    if cmd == 'skor':
        skor(kerja)
    elif cmd == 'calon':
        calon(kerja)
    elif cmd == 'kunci':
        kunci(kerja)
    elif cmd == 'lapor':
        lapor_(kerja)
    elif cmd == 'daftar':
        daftar(kerja)
    else:
        raise SystemExit(f'arahan tidak dikenali: {cmd}')
