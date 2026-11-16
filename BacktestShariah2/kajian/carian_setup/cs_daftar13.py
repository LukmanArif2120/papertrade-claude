"""Carian setup — pusingan CS13 (SPEC pindaan 15 Nov 2026 (v)): daftar SEMUA setup "naik laju" yang lulus, tanpa had
bilangan, dan senarai utama F + cara pegang B.

Sasaran = label ketat `terus` (naik >= 5 % minggu pertama, naik lagi hingga minggu ke-4, -8 % tidak disentuh). Ruang masuk dan
skor = enjin CS12 dengan label ditukar. Setiap calon berskor > 0 disemak pada kumpulan B (termasuk 2025-26) lawan kawalan
rawak; jika bacaan dikunci lulus, setiap calon lulus yang bukan kembar setup lain diberi kod F baharu (F96 dst.). Setup
lengkap: stop loss 4xATR14 + cara pegang B (pegang hingga hari ke-20, kemudian jual selepas tutup di bawah purata 20 hari).
Guna: python3 cs_daftar13.py skor|calon|kunci|lapor|daftar <kerja>. Jangan sunting keluaran secara manual."""
import json
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_atom as atom  # noqa: E402
import cs_cari as cari  # noqa: E402
import cs_cari12 as c12  # noqa: E402
import cs_cs05 as c5  # noqa: E402
import cs_keluar7 as k7  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_semak11 as s11  # noqa: E402
import cs_tala7 as t7  # noqa: E402
import cs_teras as teras  # noqa: E402

N_ATAS, N_KAWALAN, BENIH_KAWALAN = 5, 300, 20261116                  # dikunci pindaan (v)
JACCARD, B1_BEZA, B2_MIN, B2_BEZA = 0.80, 0.20, 0.60, 0.10
MENANG_PILIH, PURATA_PILIH, MIN_K3, N_LAIN = 0.50, 0.02, 20, 50      # susunan paparan: keputusan pengguna 16 Nov 2026
S_HENTI = k7.HENTI.index('4xATR14')
CARA_B = s11.CARA.index('P-MA20')
KOD_HENTI, KOD_PEGANG = f'G{S_HENTI + 1}', 'PB'
TEKS_PEGANG = 'PB pegang hingga hari ke-20, kemudian jual selepas tutup pertama di bawah purata 20 hari (had 126 sesi)'
PUS = 'CS13'
ID_MULA = 96
F_ = lambda kerja, nama: os.path.join(kerja, f'cs13_{nama}.pkl')


# ---------- skor (kumpulan A) dan calon ----------
def skor(kerja):
    """Skor setiap pencetus pada kumpulan A (sasaran `terus`, label lalai enjin) -> cs13_skor.pkl."""
    f = F_(kerja, 'skor')
    siap = pickle.load(open(f, 'rb')) if os.path.exists(f) else {}
    ev = c12.semua_pencetus(kerja, 'A')
    cari.log(f'CS13 skor: {sum(1 for n in ev if n not in siap)} pencetus (sasaran terus)')
    siap = t7.skor_ev(kerja, ev, siap, f)
    pickle.dump(siap, open(f, 'wb'), protocol=4)
    cari.log(f"CS13 skor siap: {sum(1 for r in siap.values() if r.get('cukup'))} cukup isyarat daripada {len(siap)}")
    return siap


def calon(kerja):
    """Calon = sehingga N_ATAS peraturan masuk berskor > 0 bagi setiap pencetus (tiada had bilangan); kawalan = N_KAWALAN
    peraturan rawak dengan n >= 100 setiap era pada A. -> cs13_calon.pkl"""
    S = pickle.load(open(F_(kerja, 'skor'), 'rb'))
    R = []
    for nama, r in S.items():
        if not r.get('cukup') or not len(r['atas'][0]):
            continue
        idx, sk = r['atas']
        q1, q2, f1, f2 = c5.nyah(idx)
        for j in range(min(N_ATAS, len(idx))):
            if np.isfinite(sk[j]) and sk[j] > 0:
                R.append(dict(pencetus=nama, induk=t7.induk(nama), ke=j + 1, skor=float(sk[j]), q1=int(q1[j]), q2=int(q2[j]),
                              f1=int(f1[j]), f2=int(f2[j]), skor0=r['skor0'], n_E1=r['n_ev'][0], n_E2=r['n_ev'][1]))
    T = pd.DataFrame(R).sort_values(['skor', 'pencetus', 'ke'], ascending=[False, True, True], kind='stable').reset_index(drop=True)
    T.insert(0, 'id', [f'C{i + 1:04d}' for i in range(len(T))])
    pan = cari.panel(kerja, 'A')
    L = lapis.muat(kerja, 'A')
    Lr = (L['L1'], L['L2'])
    EV = c12.semua_pencetus(kerja, 'A')
    cukup = sorted(n for n, r in S.items() if r.get('cukup'))
    rng = np.random.default_rng(BENIH_KAWALAN)
    K, cuba = [], 0
    while len(K) < N_KAWALAN and cuba < 200000:
        cuba += 1
        nama = cukup[int(rng.integers(len(cukup)))]
        q = int(rng.integers(c5.NQ))
        ci = int(rng.integers(c5.NC))
        if q == 0 and ci == 0:
            continue
        q1, q2, f1, f2 = (int(x[0]) for x in c5.nyah(np.asarray([q * c5.NC + ci])))
        ev = EV[nama]
        tp = pan['tempoh'][ev[c5.topeng(pan, Lr, ev, q1, q2, f1, f2)]]
        if min(int((tp == 0).sum()), int((tp == 1).sum())) < c5.N_MIN:
            continue
        K.append(dict(id=f'R{len(K) + 1:03d}', pencetus=nama, induk=t7.induk(nama), ke=0, skor=np.nan, q1=q1, q2=q2, f1=f1, f2=f2,
                      skor0=np.nan, n_E1=int((tp == 0).sum()), n_E2=int((tp == 1).sum())))
    out = {'calon': T, 'kawalan': pd.DataFrame(K), 'n_pencetus': len(S), 'n_cukup': len(cukup), 'cuba_kawalan': cuba}
    pickle.dump(out, open(F_(kerja, 'calon'), 'wb'), protocol=4)
    cari.log(f"CS13 calon: {len(T)} calon berskor > 0 daripada {len(cukup)} pencetus cukup isyarat ({T.pencetus.nunique()} pencetus berbeza); "
             f"kawalan rawak {len(K)} (dicuba {cuba})")
    return out


# ---------- semakan pada kumpulan B ----------
def teks_pra(q1, q2):
    """Teks prasyarat tanpa kod; '' jika tiada prasyarat (prasyarat "tiada earnings ..." dikekalkan sepenuhnya)."""
    return '' if q1 < 0 and q2 < 0 else c5.buang_kod(c5.tk_pra(int(q1), int(q2))).replace(' DAN ', ' + ')


def teks_pen(f1, f2):
    return '' if f1 < 0 and f2 < 0 else c5.buang_kod(c5.tk_pen(int(f1), int(f2))).replace(' DAN ', ' + ')


def lengkap(pan, Bt, ev):
    """Dagangan setup LENGKAP (stop loss 4xATR14 + cara pegang B) atas isyarat dengan tetingkap 126 sesi lengkap: statistik
    satu posisi setiap saham (keseluruhan dan setiap tempoh) + statistik semua isyarat bagi "jual hari ke-20" dan cara B."""
    ev = np.ascontiguousarray(ev[s11.sah126(pan)[ev]], dtype=np.int64)
    if len(ev) < 30:
        return None
    R, SK = s11.pegang(ev, pan['o'], pan['l'], pan['c'], pan['atr'], Bt, S_HENTI)
    out = dict(n_semua=len(ev), purata_semua=float(R[:, CARA_B].mean()), menang_semua=float((R[:, CARA_B] > 0).mean()),
               purata_J20_semua=float(R[:, 0].mean()), menang_J20_semua=float((R[:, 0] > 0).mean()))
    amb = teras.satu_posisi(ev, SK[:, CARA_B], pan['tid'])
    e, r, sk = ev[amb], R[amb, CARA_B], SK[amb, CARA_B]
    tp = pan['tempoh'][e]
    st = lambda x: dict(n=int(len(x)), purata=float(x.mean()) if len(x) else np.nan, menang=float((x > 0).mean()) if len(x) else np.nan,
                        k10=float((x >= 0.10).mean()) if len(x) else np.nan)
    out.update(st(r), rugi15=float((r <= -0.15).mean()), sesi=float(np.median(sk) + 1), jual_hari_beli=int((sk == 0).sum()),
               K=[st(r[tp == j]) for j in range(3)])
    return out


def kunci(kerja):
    """Nilai setiap calon, setiap kawalan dan 69 setup F sedia ada dengan setup lengkap yang SAMA pada kumpulan B (dan kira
    belian pada kumpulan A bagi semakan kembar dan kekerapan Shariah) -> cs13_kunci.pkl."""
    import cs_lapor as lapor
    C = pickle.load(open(F_(kerja, 'calon'), 'rb'))
    semua = pd.concat([C['calon'], C['kawalan']], ignore_index=True)
    shar = set(open(os.path.join(lapor.BS2, 'data', 'harga', 'univ.txt')).read().split())
    param = t7.param_semua(kerja)
    out, t0 = {}, time.time()
    for set_ in ('B', 'A'):
        pan = cari.panel(kerja, set_)
        L = lapis.muat(kerja, set_)
        Lr = (L['L1'], L['L2'])
        EV = c12.semua_pencetus(kerja, set_)
        Lab, As = s11.asas(pan)
        Bt = s11.siri_trend(pan) if set_ == 'B' else None
        sh = np.asarray([t in shar for t in pan['ticker']])

        def nilai(idn, ev):
            d, e = s11.ukur_tangkap(pan, Lab, As, ev, S_HENTI)
            o = out.setdefault(idn, {})
            es = e[sh[pan['tid'][e]]]
            o['e_' + set_], o['es_' + set_] = e.astype(np.int32), es.astype(np.int32)
            o['ms_' + set_] = (pan['tarikh'][es + 1] // 100).astype(np.int32)
            if set_ == 'B':
                o.update(d=d, L=lengkap(pan, Bt, ev))
            return o

        for k, r in enumerate(semua.itertuples(), 1):
            ev = EV[r.pencetus]
            o = nilai(r.id, ev[c5.topeng(pan, Lr, ev, r.q1, r.q2, r.f1, r.f2)])
            if set_ == 'B':
                o.update(nama=t7.nama7(r.pencetus, param), prasyarat=teks_pra(r.q1, r.q2), penapis=teks_pen(r.f1, r.f2))
            if k % 500 == 0:
                cari.log(f'  CS13 kunci {set_} {k}/{len(semua)} · {time.time() - t0:.0f}s')
        for x in s11.setup_f(kerja, set_, pan, t7.semua_ev(kerja, set_, 'asal'), Lr):
            o = nilai(x['id'], x['ev'])
            if set_ == 'B':
                o.update(nama=x['pencetus'], prasyarat=x['prasyarat'], penapis='' if str(x['penapis']).strip() in ('', '–', 'nan') else x['penapis'])
    out['_n'] = {s: len(cari.panel(kerja, s)['c']) for s in ('A', 'B')}
    pickle.dump(out, open(F_(kerja, 'kunci'), 'wb'), protocol=4)
    cari.log(f'CS13 kunci: {len(out) - 1} peraturan · {time.time() - t0:.0f}s')
    return out


def _baris(peranan, idn, o, **lain):
    d, L = o['d'], o['L'] or {}
    kl = [d[f'kl_terus_K{j}'] for j in (1, 2, 3)]
    layak = bool(d['n'] >= s11.MIN_BELIAN and d['tahun'] >= s11.MIN_TAHUN)
    g = lambda k_: L.get(k_, np.nan)
    b = dict(peranan=peranan, id=idn, nama=o['nama'], prasyarat=o['prasyarat'], penapis=o['penapis'], n=d['n'], tahun=d['tahun'],
             setahun=d['n'] / s11.TAHUN, shariah_setahun=(len(o['es_A']) + len(o['es_B'])) / s11.TAHUN,
             m5=d['m5'], a_m5=d['a_m5'], terus=d['terus'], a_terus=d['a_terus'], kl_terus=d['terus'] - d['a_terus'],
             kl_terus_K1=kl[0], kl_terus_K2=kl[1], kl_terus_K3=kl[2], naik=d['naik'], a_naik=d['a_naik'],
             menang_J20=d['menang'], purata_J20=d['purata'], rugi8_J20=d['rugi8'], stop_J20=d['stop'],
             n_B=L.get('n', 0), menang_B=g('menang'), purata_B=g('purata'), k10_B=g('k10'), rugi15_B=g('rugi15'), hari_B=g('sesi'),
             jual_hari_beli=d['jual_hari_beli'] + L.get('jual_hari_beli', 0), layak=layak,
             lulus=bool(layak and all(x == x and x > 0 for x in kl)))
    for j in range(3):
        v = L['K'][j] if L else {}
        b.update({f'n_B_K{j + 1}': v.get('n', 0), f'purata_B_K{j + 1}': v.get('purata', np.nan),
                  f'menang_B_K{j + 1}': v.get('menang', np.nan), f'k10_B_K{j + 1}': v.get('k10', np.nan)})
    b.update(lain)
    return b


def jadual(C, K):
    """Satu baris setiap calon, setiap kawalan dan setiap setup F sedia ada, dengan angka kumpulan B."""
    baris = []
    for nm, T in (('calon', C['calon']), ('kawalan', C['kawalan'])):
        for r in T.itertuples():
            baris.append(_baris(nm, r.id, K[r.id], pencetus=r.pencetus, induk=r.induk, q1=r.q1, q2=r.q2, f1=r.f1, f2=r.f2, skor_A=r.skor,
                                prasyarat=teks_pra(r.q1, r.q2), penapis=teks_pen(r.f1, r.f2)))
    for i in sorted((i for i in K if i[0] == 'F'), key=lambda x: int(x[1:])):
        baris.append(_baris('F', i, K[i], pencetus='', induk='', q1=np.nan, q2=np.nan, f1=np.nan, f2=np.nan, skor_A=np.nan))
    return pd.DataFrame(baris)


def bacaan(T):
    """Bacaan dikunci pindaan (v), atas peraturan yang layak dinilai (belian B >= 300 dan >= 10 tahun aktif)."""
    c, k = T[(T.peranan == 'calon') & T.layak], T[(T.peranan == 'kawalan') & T.layak]
    f = lambda x: float(x) if len(c) and len(k) else np.nan
    o = dict(n_calon=int((T.peranan == 'calon').sum()), calon_layak=len(c), kawalan_layak=len(k), n_lulus=int(c.lulus.sum()),
             lulus_calon=f(c.lulus.mean()), lulus_kawalan=f(k.lulus.mean()),
             k3_calon=f((c.kl_terus_K3 > 0).mean()), k3_kawalan=f((k.kl_terus_K3 > 0).mean()))
    o['b1'] = bool(o['lulus_calon'] >= o['lulus_kawalan'] + B1_BEZA)
    o['b2'] = bool(o['k3_calon'] >= B2_MIN and o['k3_calon'] >= o['k3_kawalan'] + B2_BEZA)
    o['ya'] = bool(o['b1'] and o['b2'])
    o['nasib'] = float(o['lulus_kawalan'] / o['lulus_calon']) if o['lulus_calon'] and o['lulus_calon'] == o['lulus_calon'] else np.nan
    return o


def kembar(T, K):
    """Semakan kembar pindaan (v): calon lulus ikut susunan skor A; kembar jika Jaccard belian satu posisi (A + B) >= JACCARD
    dengan setup yang sudah diterima (69 setup F sedia ada dikira sudah diterima). Pulangkan dict id calon -> id wakil ('' =
    bukan kembar)."""
    from scipy import sparse
    lama = T[T.peranan == 'F'].id.tolist()
    baru = T[(T.peranan == 'calon') & T.lulus].sort_values('skor_A', ascending=False, kind='stable').id.tolist()
    ids = lama + baru
    if not baru:
        return {}
    nB = K['_n']['B']
    baris_, lajur_ = [], []
    for i, idn in enumerate(ids):
        x = np.concatenate([K[idn]['e_B'].astype(np.int64), K[idn]['e_A'].astype(np.int64) + nB])
        baris_.append(np.full(len(x), i, np.int64))
        lajur_.append(x)
    lj = np.concatenate(lajur_)
    _, lj = np.unique(lj, return_inverse=True)
    M = sparse.csr_matrix((np.ones(len(lj), np.int32), (np.concatenate(baris_), lj)), shape=(len(ids), int(lj.max()) + 1))
    X = (M @ M.T).tocsr()
    saiz = np.asarray(M.sum(1)).ravel()
    terima = np.zeros(len(ids), bool)
    terima[:len(lama)] = True
    out = {}
    for i in range(len(lama), len(ids)):
        a, b = X.indptr[i], X.indptr[i + 1]
        j, x = X.indices[a:b], X.data[a:b]
        m = terima[j] & (j != i)
        jac = x[m] / (saiz[i] + saiz[j[m]] - x[m])
        if len(jac) and jac.max() >= JACCARD:
            out[ids[i]] = ids[int(j[m][int(np.argmax(jac))])]
        else:
            out[ids[i]] = ''
            terima[i] = True
    return out


def takrif13(pencetus, q1, q2, f1, f2):
    pen = '+'.join(atom.PENAPIS[f][:3] for f in (f1, f2) if f >= 0)
    return f'{pencetus}|{pen}|{KOD_HENTI}|{KOD_PEGANG}|{c5.tk_pra(q1, q2, kod=True)}'


def semua(kerja):
    """(C, K, T dengan lajur kembar_kepada / takrif / id_F, bacaan)."""
    import cs_lapor as lapor
    C = pickle.load(open(F_(kerja, 'calon'), 'rb'))
    K = pickle.load(open(F_(kerja, 'kunci'), 'rb'))
    T = jadual(C, K)
    B = bacaan(T)
    kb = kembar(T, K)
    T['kembar_kepada'] = [kb.get(i, '') if p == 'calon' else '' for i, p in zip(T.id, T.peranan)]
    T['takrif'] = [takrif13(r.pencetus, int(r.q1), int(r.q2), int(r.f1), int(r.f2)) if r.peranan == 'calon' else '' for r in T.itertuples()]
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('')
    peta = dict(zip(reg.takrif[reg.pusingan == PUS], reg.id[reg.pusingan == PUS]))
    T['id_F'] = [peta.get(t, '') if p == 'calon' else (i if p == 'F' else '') for t, p, i in zip(T.takrif, T.peranan, T.id)]
    T['untuk_daftar'] = (T.peranan == 'calon') & T.lulus & (T.kembar_kepada == '')
    return C, K, T, B


# ---------- pendaftaran ----------
def daftar(kerja):
    """Daftar setiap calon lulus yang bukan kembar ke data/registry_F.csv (kod F96 dst., ikut susunan skor A). HANYA jika
    bacaan dikunci lulus. F01-F95 tidak disentuh. Pulangkan bilangan kod baharu."""
    import cs_lapor as lapor
    C, K, T, B = semua(kerja)
    if not B['ya']:
        cari.log('CS13 daftar: bacaan dikunci TIDAK lulus -> tiada kod F baharu')
        return 0
    param = t7.param_semua(kerja)
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('').reindex(columns=lapor.LAJUR_F, fill_value='')
    ada, seterusnya, baharu = set(reg.takrif), max(int(x[1:]) for x in reg.id) + 1, []
    assert seterusnya >= ID_MULA
    X = T[T.untuk_daftar].sort_values('skor_A', ascending=False, kind='stable')
    for r in X.itertuples():
        if r.takrif in ada:
            continue
        q1, q2, f1, f2 = int(r.q1), int(r.q2), int(r.f1), int(r.f2)
        masuk = t7.nama7(r.pencetus, param)
        P = param.get(r.pencetus) if r.pencetus[0] == 'M' else dict(t7._GRID[r.pencetus][1]) if r.pencetus[0] == 'K' else None
        b = dict.fromkeys(lapor.LAJUR_F, '')
        b.update(id=f'F{seterusnya:02d}', keluarga='F', pusingan=PUS, tarikh_daftar='2026-11-15', takrif=r.takrif,
                 param=json.dumps({a: (round(x, 6) if isinstance(x, float) else x) for a, x in P.items()}, sort_keys=True) if P else '',
                 masuk=masuk, penapis=c5.tk_pen(f1, f2), henti=f'{KOD_HENTI} {k7.HENTI[S_HENTI]}', keluar=TEKS_PEGANG,
                 skor_tepat=f'{r.skor_A:.5f}', status='BACKTEST',
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
        b['menang'] = f'{jum / bil:.4f}'
        baharu.append(b)
        ada.add(r.takrif)
        seterusnya += 1
    if baharu:
        reg = pd.concat([reg, pd.DataFrame(baharu)[lapor.LAJUR_F].astype(str)], ignore_index=True)
        reg['_n'] = reg.id.str[1:].astype(int)
        reg.sort_values('_n').drop(columns='_n').to_csv(lapor.REG_F, index=False)
    cari.log(f"CS13 daftar: {len(baharu)} kod F baharu ({baharu[0]['id']}–{baharu[-1]['id']})" if baharu else 'CS13 daftar: tiada yang baharu')
    return len(baharu)


# ---------- laporan ----------
def gabung(K, ids):
    """Belian (saham-hari berbeza) setahun dan bahagian bulan yang ada belian, pada senarai Shariah, bagi gabungan setup."""
    if not len(ids):
        return 0.0, 0.0
    n = sum(len(np.unique(np.concatenate([K[i]['es_' + s] for i in ids]))) for s in ('A', 'B'))
    bulan = np.unique(np.concatenate([K[i]['ms_' + s] for i in ids for s in ('A', 'B')]))
    return n / s11.TAHUN, len(bulan) / (s11.TAHUN * 12)


def senarai_utama(T):
    """Senarai utama keputusan (1): setup F lama yang dipercayai (takrif (m)) + kod baharu CS13, disusun ikut kadar tangkap."""
    KA = pd.read_csv(os.path.join(SINI, 'hasil', 'KEDUDUKAN_AKHIR.csv'))
    yakin = set(KA.id[KA.dipercayai.astype(bool)])
    U = T[((T.peranan == 'F') & T.id.isin(yakin)) | ((T.peranan == 'calon') & (T.id_F != ''))].copy()
    U['asal'] = np.where(U.peranan == 'F', 'lama', 'baharu')
    U['pilihan'] = (U.menang_B >= MENANG_PILIH) & (U.purata_B >= PURATA_PILIH)
    U = U.sort_values(['pilihan', 'terus', 'kl_terus'], ascending=False, kind='stable').reset_index(drop=True)
    U.insert(0, 'kedudukan', np.arange(1, len(U) + 1))
    return U


def semak_masa(U):
    """Semakan ikut masa bagi tapisan "pilihan" (keputusan 16 Nov 2026): setup yang menepati tapisan pada K1 + K2 sahaja lawan
    setup lain, diukur pada K3 (>= MIN_K3 dagangan). Dilaporkan sahaja."""
    n12 = (U.n_B_K1 + U.n_B_K2).replace(0, np.nan)
    w = lambda kol: (U.n_B_K1 * U[f'{kol}_B_K1'].fillna(0) + U.n_B_K2 * U[f'{kol}_B_K2'].fillna(0)) / n12
    pil = (w('menang') >= MENANG_PILIH) & (w('purata') >= PURATA_PILIH)
    ok = U.n_B_K3 >= MIN_K3
    out = {}
    for nm, X in (('pilih', U[ok & pil]), ('lain', U[ok & ~pil])):
        out[nm] = dict(n=int(len(X)), menang=float(X.menang_B_K3.median()), purata=float(X.purata_B_K3.median()),
                       menang50=float((X.menang_B_K3 >= MENANG_PILIH).mean()), positif=float((X.purata_B_K3 > 0).mean()))
    return out


def lapor_(kerja):
    import cs_lapor as lapor
    C, K, T, B = semua(kerja)
    d_ = os.path.join(SINI, 'hasil', PUS)
    os.makedirs(d_, exist_ok=True)
    c, kw = T[T.peranan == 'calon'], T[T.peranan == 'kawalan']
    buang = ['peranan']
    c.drop(columns=buang).to_csv(os.path.join(d_, 'calon.csv.gz'), index=False, float_format='%.5f')
    kw.drop(columns=buang + ['kembar_kepada', 'takrif', 'id_F', 'untuk_daftar']).to_csv(os.path.join(d_, 'kawalan.csv'), index=False, float_format='%.5f')
    L = c[c.lulus]
    D = c[c.untuk_daftar]
    U = senarai_utama(T)
    lajur_u = ['kedudukan', 'id_F', 'asal', 'prasyarat', 'nama', 'penapis', 'n', 'tahun', 'setahun', 'shariah_setahun', 'm5', 'a_m5', 'terus',
               'a_terus', 'kl_terus', 'kl_terus_K1', 'kl_terus_K2', 'kl_terus_K3', 'naik', 'a_naik', 'menang_J20', 'purata_J20',
               'n_B', 'menang_B', 'purata_B', 'k10_B', 'rugi15_B', 'hari_B', 'jual_hari_beli', 'skor_A', 'takrif', 'pilihan']
    SM = semak_masa(U)
    U[lajur_u].rename(columns={'id_F': 'id'}).to_csv(os.path.join(d_, 'senarai_utama.csv'), index=False, float_format='%.5f')
    json.dump({k_: (None if isinstance(v, float) and v != v else v) for k_, v in dict(
        B, n_kembar=int((L.kembar_kepada != '').sum()), n_untuk_daftar=len(D), n_berdaftar=int((c.id_F != '').sum()),
        n_utama=len(U), n_utama_lama=int((U.asal == 'lama').sum()), n_pilihan=int(U.pilihan.sum()), semak_masa=SM).items()},
        open(os.path.join(d_, 'bacaan.json'), 'w'), indent=1, sort_keys=True)
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    p = lambda x, k=0, t=False: '–' if x is None or x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')
    daftar_ = c[c.id_F != '']
    idf = sorted(daftar_.id_F, key=lambda x: int(x[1:]))
    A = ['# CS13: semua setup "naik laju" yang lulus didaftarkan sebagai kod F (backtest; BUKAN bukti)', '', status, '',
         'Dijana `kajian/carian_setup/cs_daftar13.py`. Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 15 Nov 2026 (v). '
         '**Jangan sunting secara manual.**', '',
         '## 1. Apa yang dibuat', '',
         '- **Ukuran ketat ("naik laju")**: saham naik ≥ 5 % pada minggu pertama, naik lagi hingga minggu ke-4, dan tidak menyentuh −8 %.',
         f"- {C['n_pencetus']:,} isyarat beli (kaedah M, kaedah N, indikator dan variannya) × prasyarat pasaran × prasyarat syarikat × penapis "
         f"saham; skor dikira pada saham carian sahaja. **{B['n_calon']:,} calon** berskor positif (sehingga {N_ATAS} peraturan terbaik setiap "
         'isyarat beli; tiada had bilangan).',
         '- Setup lengkap setiap calon: beli pada buka esok; stop loss 4xATR14; pegang sekurang-kurangnya hingga hari ke-20; selepas itu jual '
         'bila harga tutup di bawah purata 20 hari; paling lama 6 bulan (cara pegang B pilihan pengguna).',
         '- "Lulus" = pada saham yang carian tidak lihat: belian ≥ 300, ≥ 10 tahun aktif, dan lebih kerap menangkap saham naik laju daripada '
         'saham rawak pada hari yang sama dalam KETIGA-TIGA tempoh (2010–19, 2020–24, 2025–26).', '',
         '## 2. Ujian (ditetapkan dahulu)', '',
         f"- Peraturan yang cukup belian untuk dinilai: {B['calon_layak']:,} calon dan {B['kawalan_layak']} kawalan rawak.",
         f"- **B1** kadar lulus: calon **{p(B['lulus_calon'])} %** lawan kawalan rawak {p(B['lulus_kawalan'])} % (perlu beza ≥ 20 mata) → "
         f"{'lulus' if B['b1'] else 'GAGAL'}.",
         f"- **B2** lebih baik daripada rawak pada 2025–26 (tahun yang carian tidak lihat): calon **{p(B['k3_calon'])} %** lawan kawalan "
         f"{p(B['k3_kawalan'])} % (perlu ≥ 60 % dan beza ≥ 10 mata) → {'lulus' if B['b2'] else 'GAGAL'}.",
         f"- **Keputusan: carian naik laju {'BERHASIL — kod F didaftarkan' if B['ya'] else 'TIDAK berhasil — tiada kod F baharu'}.**", '',
         '## 3. Berapa yang lulus dan didaftarkan', '',
         f"- Lulus: **{len(L):,}** daripada {B['n_calon']:,} calon.",
         f"- Daripada yang lulus, {int((L.kembar_kepada != '').sum()):,} ialah kembar setup lain (membeli saham yang sama pada hari yang sama, "
         f"pertindihan ≥ {JACCARD:.0%}; {int(L.kembar_kepada.str.startswith('F').sum())} daripadanya kembar setup F lama) dan tidak diberi kod "
         'sendiri; ia direkod dalam `calon.csv.gz` (lajur `kembar_kepada`).',
         f"- **Setup berlainan yang lulus: {len(D):,}**" + (f" → didaftarkan sebagai **`{idf[0]}`–`{idf[-1]}`** ({len(idf):,} kod baharu; "
                                                            '`F01`–`F95` tidak diubah).' if idf else ' (belum didaftarkan).'),
         f"- Anggaran bahagian yang lulus kerana nasib (kadar lulus kawalan ÷ kadar lulus calon): kira-kira {p(B['nasib'])} %.", '',
         '## 4. Ikut tempoh (peraturan yang cukup belian; saham yang carian tidak lihat)', '',
         '| Kumpulan | Bilangan | Lebih baik daripada rawak: 2010–19 | 2020–24 | **2025–26** | Median kelebihan 2010–19 / 2020–24 / 2025–26 (mata) | Lulus |',
         '|---' * 7 + '|']
    for nm, X in (('Calon carian', c), ('Kawalan rawak', kw), ('Calon tanpa prasyarat pasaran', c[c.q1 < 0]),
                  ('Setup F lama (69)', T[T.peranan == 'F']), ('Kod baharu', daftar_)):
        e = X[X.layak]
        if len(e):
            A.append(f"| {nm} | {len(e):,} | {(e.kl_terus_K1 > 0).mean():.0%} | {(e.kl_terus_K2 > 0).mean():.0%} | **{(e.kl_terus_K3 > 0).mean():.0%}** | "
                     f"{p(e.kl_terus_K1.median(), 1, True)} / {p(e.kl_terus_K2.median(), 1, True)} / {p(e.kl_terus_K3.median(), 1, True)} | {e.lulus.mean():.0%} |")
    A += ['', '## 5. Banding (nilai tengah setiap kumpulan; saham yang carian tidak lihat)', '',
          '| Kumpulan | Bilangan | Naik ≥ 5 % minggu 1 % (rawak) | Naik laju % (rawak) | Jual hari ke-20: menang · purata | Cara pegang B: menang · purata · rugi ≥ 15 % · hari |',
          '|---' * 6 + '|']
    for nm, X in (('Setup F lama yang dipercayai', U[U.asal == 'lama']), ('Kod baharu', U[U.asal == 'baharu']), ('Kawalan rawak', kw[kw.layak])):
        if len(X):
            g = X.median(numeric_only=True)
            A.append(f"| {nm} | {len(X):,} | {p(g.m5)} ({p(g.a_m5)}) | {p(g.terus)} ({p(g.a_terus)}) | {p(g.menang_J20)} % · {p(g.purata_J20, 1, True)} % | "
                     f"{p(g.menang_B)} % · {p(g.purata_B, 1, True)} % · {p(g.rugi15_B)} % · {g.hari_B:.0f} |")
    if len(daftar_):
        ada_pas, ada_sy = (daftar_.q1 >= 0), (daftar_.q2 >= 0)
        g30, b30 = gabung(K, U.id.head(30).tolist())
        gs, bs = gabung(K, U.id.tolist())
        A += ['', '## 6. Kod baharu: pecahan', '',
              f"- Dengan prasyarat pasaran: {int(ada_pas.sum()):,}; dengan prasyarat syarikat/kumpulan: {int(ada_sy.sum()):,}; tanpa apa-apa prasyarat: "
              f"{int((~ada_pas & ~ada_sy).sum()):,}.",
              '- Prasyarat paling kerap: ' + '; '.join(f'{k_ or "tiada"} ({v})' for k_, v in daftar_.prasyarat.value_counts().head(8).items()) + '.',
              f"- Isyarat beli: {daftar_.induk.nunique()} kaedah/keluarga berbeza; paling kerap " +
              ', '.join(f'{k_} ({v})' for k_, v in daftar_.induk.value_counts().head(8).items()) + '.',
              f"- Kekerapan pada senarai Shariah: 30 setup teratas senarai utama digabung = {g30:.0f} belian setahun (ada belian dalam {b30:.0%} "
              f"bulan); semua {len(U):,} setup senarai utama = {gs:.0f} setahun ({bs:.0%} bulan).",
              f"- Jualan pada hari beli: {int(U.jual_hari_beli.sum())} (mesti 0).", '']
    if len(daftar_):
        ern = daftar_.prasyarat.fillna('').str.contains('earnings dalam 1-')
        A += ['## 6b. Sifat kod baharu (analisis SELEPAS hasil; bukan ditetapkan dahulu)', '',
              f"- **{int(ern.sum()):,} daripada {len(daftar_):,} kod baharu memakai SATU prasyarat yang sama: laporan kewangan (earnings) dalam 1–5 hari akan "
              'datang.** Harga bergerak besar selepas laporan kewangan, jadi belian begini lebih kerap menangkap saham naik laju — dan juga '
              'lebih kerap jatuh.',
              '- Kadar tangkap kod baharu kira-kira dua kali saham rawak, tetapi **kadar menang dan purata setiap dagangan hampir sama dengan '
              'peraturan rawak** (jadual di bawah). Setup F lama yang dipercayai mempunyai purata yang jauh lebih tinggi.', '',
              '| Kumpulan | Bilangan | Tangkap % (rawak) | Cara pegang B: menang % | Purata % | Rugi ≥ 15 % % | Beli setahun (nilai tengah) |',
              '|---' * 7 + '|']
        for nm, X in (('Kod baharu: laporan kewangan dalam 1–5 hari', daftar_[ern]), ('Kod baharu: prasyarat lain', daftar_[~ern]),
                      ('Setup F lama yang dipercayai', U[U.asal == 'lama']), ('Kawalan rawak', kw[kw.layak])):
            if len(X):
                g = X.median(numeric_only=True)
                A.append(f"| {nm} | {len(X):,} | {p(g.terus)} ({p(g.a_terus)}) | {p(g.menang_B)} | {p(g.purata_B, 1, True)} | {p(g.rugi15_B)} | {g.setahun:.0f} |")
        m50, p2 = U.menang_B >= 0.5, U.purata_B >= 0.02
        A += ['', f"- Dalam senarai utama ({len(U):,} setup): {int(m50.sum()):,} menang ≥ 50 %; {int(p2.sum()):,} purata ≥ +2 % setiap dagangan; "
              f"**{int((m50 & p2).sum()):,} kedua-duanya** ({int((m50 & p2 & (U.asal == 'lama')).sum())} lama, "
              f"{int((m50 & p2 & (U.asal == 'baharu')).sum())} baharu). Ini paparan pada saham yang sudah dilihat, bukan pemilihan.", '']
    A += ['', '## 7. Kaveat', '',
          '- Beribu calon disemak pada saham yang tidak dilihat, jadi sebahagian lulus kerana nasib (anggaran di §3); kumpulan saham itu sudah '
          'digunakan dalam pusingan terdahulu.',
          '- 2025–26 pendek (kira-kira 20 bulan) dan belian di dalamnya sedikit bagi kebanyakan setup.',
          '- "Lebih baik daripada rawak hari sama" mengukur PILIHAN saham; kadar mentah turut mengandungi kesan BILA membeli (keadaan pasaran).',
          '- Tiada saham delist dalam data (condong ke atas, lebih-lebih lagi bagi pegangan hingga 6 bulan). Backtest sahaja; tiada papertrade '
          'tanpa keputusan pengguna; kad skor kekal satu-satunya keputusan wang sebenar.', '']
    open(os.path.join(d_, 'DAFTAR.md'), 'w', encoding='utf-8').write('\n'.join(A))
    tx = lambda s: s if isinstance(s, str) and s.strip() else '–'
    Up, Ul = U[U.pilihan], U[~U.pilihan]
    S = ['# Senarai utama: setup F (saham naik laju) dengan cara pegang B (backtest; BUKAN bukti)', '', status, '',
         'Dijana `kajian/carian_setup/cs_daftar13.py` (pindaan 15 Nov 2026 (v), keputusan pengguna (1)). **Jangan sunting secara manual.**', '',
         f"{len(U):,} setup: {int((U.asal == 'lama').sum())} setup F lama yang dipercayai + {int((U.asal == 'baharu').sum()):,} kod baharu CS13. "
         'Semua dinilai dengan cara yang SAMA pada saham yang carian tidak lihat: peraturan beli masing-masing; stop loss 4xATR14; pegang '
         'sekurang-kurangnya hingga hari ke-20, kemudian jual bila harga tutup di bawah purata 20 hari; paling lama 6 bulan. Tiada jualan pada '
         'hari beli.', '',
         '- **Tangkap** = daripada 100 belian, berapa yang naik ≥ 5 % minggu pertama DAN naik lagi hingga minggu ke-4 (kurungan = saham rawak '
         'pada hari yang sama).',
         '- **Menang** dan **purata** = daripada semua dagangan dengan cara pegang di atas (selepas kos 0.5 %).',
         '- Lajur "2025–26" = kelebihan atas saham rawak pada tahun yang carian tidak lihat (mata peratus).',
         f"- **Susunan (keputusan pengguna 16 Nov 2026):** dahulu setup \"pilihan\" — menang ≥ {MENANG_PILIH:.0%} DAN purata ≥ +{PURATA_PILIH:.0%} "
         'setiap dagangan — kemudian yang lain; dalam setiap kumpulan ikut kadar tangkap.', '']
    kepala = ['| # | ID | Prasyarat | Isyarat beli | Penapis saham | Beli setahun (senarai Shariah) | **Tangkap %** (rawak) | Naik ≥ 5 % minggu 1 % | '
              '**Menang %** | Purata % | Rugi ≥ 15 % % | Hari pegang | 2025–26 |', '|---' * 13 + '|']
    baris_u = lambda r: (f"| {r.kedudukan} | `{r.id_F}` | {tx(r.prasyarat)} | {r.nama} | {tx(r.penapis)} | {r.setahun:.0f} ({r.shariah_setahun:.0f}) | "
                         f"**{p(r.terus)}** ({p(r.a_terus)}) | {p(r.m5)} | **{p(r.menang_B)}** | {p(r.purata_B, 1, True)} | {p(r.rugi15_B)} | "
                         f"{r.hari_B:.0f} | {p(r.kl_terus_K3, 1, True)} |")
    S += [f"## 1. Setup pilihan: {len(Up):,} ({int((Up.asal == 'lama').sum())} lama, {int((Up.asal == 'baharu').sum())} baharu)", '',
          '**Baca dahulu:** tapisan ini dibuat SELEPAS melihat hasil pada saham yang sama, jadi angka menang dan purata kumpulan ini condong ke '
          'atas. Semakan ikut masa (ditulis sebelum dikira): setup yang menepati tapisan pada 2010–2024 sahaja, diukur pada 2025–26 '
          f"(≥ {MIN_K3} dagangan):", '',
          '| Kumpulan (ikut 2010–2024) | Bilangan | Menang 2025–26 (nilai tengah) | Purata 2025–26 (nilai tengah) | Masih menang ≥ 50 % | Purata masih positif |',
          '|---' * 6 + '|']
    for kk, nm in (('pilih', 'Menepati tapisan'), ('lain', 'Tidak menepati')):
        v = SM[kk]
        S.append(f"| {nm} | {v['n']:,} | {p(v['menang'])} % | {p(v['purata'], 1, True)} % | {p(v['menang50'])} % | {p(v['positif'])} % |")
    S += [''] + kepala + [baris_u(r) for r in Up.itertuples()]
    S += ['', f'## 2. Setup lain: {len(Ul):,} (jadual memaparkan {min(N_LAIN, len(Ul))} teratas ikut kadar tangkap)', ''] + kepala
    S += [baris_u(r) for r in Ul.head(N_LAIN).itertuples()]
    S += ['', f'Senarai penuh {len(U):,} setup (lajur `pilihan`): '
          '`hasil/CS13/senarai_utama.csv`. Keluar berdaftar `F01`–`F95` (lajur `keluar` dalam `data/registry_F.csv`) tidak diubah; angka di '
          'sini ialah peraturan beli mereka dengan cara pegang B.', '',
          '- Pangkat backtest pada saham yang sudah dilihat berkali-kali; tiada saham delist. Papertrade hanya dengan keputusan pengguna.', '']
    open(os.path.join(d_, 'SENARAI_UTAMA.md'), 'w', encoding='utf-8').write('\n'.join(S))
    cari.log(f"CS13 lapor: calon {B['n_calon']}, layak {B['calon_layak']}, lulus {B['n_lulus']} ({B['lulus_calon']:.0%} lawan kawalan "
             f"{B['lulus_kawalan']:.0%}); K3 {B['k3_calon']:.0%} lawan {B['k3_kawalan']:.0%} -> {'BERHASIL' if B['ya'] else 'TIDAK'}; "
             f"kembar {int((L.kembar_kepada != '').sum())}, untuk daftar {len(D)}, berdaftar {len(idf)}; senarai utama {len(U)}")
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
