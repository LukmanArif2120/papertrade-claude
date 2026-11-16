# cs_trend17.py — pusingan CS17 (SPEC_CARIAN_SETUP.md pindaan 16 Nov 2026 (aa); keputusan pengguna "ya utk semua"): lorong
# "pegang berbulan-bulan" (T, kes MXL) TANPA HAD bilangan. Mengulang untuk lorong T apa yang CS13 buat untuk F: carian pada
# kumpulan A dengan sasaran `besar` (cs_trend8), calon = sehingga 5 peraturan berskor > 0 setiap pencetus, kawalan rawak,
# bacaan dikunci pada kumpulan B, dan kod T13 dst. bagi setiap calon lulus yang bukan kembar. Mekanik = keluar yang diterima
# pengguna bagi lorong ini: pegang 126 sesi + stop loss 6xATR14, tiada indikator keluar. registry_F.csv TIDAK disentuh.
#   python3 cs_trend17.py skor|calon|kunci|lapor <kerja>
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
import cs_cs05 as c5  # noqa: E402
import cs_daftar13 as d13  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_semak11 as s11  # noqa: E402
import cs_tala7 as t7  # noqa: E402
import cs_teras as teras  # noqa: E402
import cs_trend8 as t8  # noqa: E402

PUS = 'CS17'
N_ATAS, N_KAWALAN, BENIH_KAWALAN = 5, 300, 20261117                 # dikunci pindaan (aa)
S_HENTI = t8.HENTI.index('6xATR14')
MIN_BELIAN, MIN_TAHUN = t8.MIN_BELIAN, t8.MIN_TAHUN                  # 200, 8 ("Dipercayai-T" CS08)
ID_MULA, TAMBAH_MIN = 13, 0.01
Q_HASIL = lapis.KUMPULAN.index('QF06 hasil suku terkini tumbuh >= 20%')
KES = ('MXL', 20260301, 20260630)
F_ = lambda kerja, nama: os.path.join(kerja, f'cs17_{nama}.pkl')
HASIL = os.path.join(SINI, 'hasil', PUS)
_J0, _P0, _B0, _XT0 = np.zeros(0, np.int64), np.zeros(0), np.zeros(0, np.int64), np.zeros((1, 1), np.uint8)


# ---------- carian pada kumpulan A ----------
def skor(kerja):
    """Skor setiap pencetus pada kumpulan A (sasaran `besar`) -> cs17_skor.pkl."""
    f = F_(kerja, 'skor')
    siap = pickle.load(open(f, 'rb')) if os.path.exists(f) else {}
    pan = cari.panel(kerja, 'A')
    S8, V, _, _ = t8.label_v(pan)
    ev = {n: e[S8[e]] for n, e in c12.semua_pencetus(kerja, 'A').items()}
    cari.log(f'CS17 skor: {sum(1 for n in ev if n not in siap)} pencetus (sasaran besar; asas {V[S8, 0].mean() * 100:.2f} %)')
    siap = t7.skor_ev(kerja, ev, siap, f, V=V)
    pickle.dump(siap, open(f, 'wb'), protocol=4)
    cari.log(f"CS17 skor siap: {sum(1 for r in siap.values() if r.get('cukup'))} cukup isyarat daripada {len(siap)}")
    return siap


def calon(kerja):
    """Calon = sehingga N_ATAS peraturan berskor > 0 setiap pencetus; kawalan = N_KAWALAN peraturan rawak yang cukup isyarat
    pada A (tetingkap 126 sesi lengkap). -> cs17_calon.pkl"""
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
                              f1=int(f1[j]), f2=int(f2[j])))
    T = pd.DataFrame(R).sort_values(['skor', 'pencetus', 'ke'], ascending=[False, True, True], kind='stable').reset_index(drop=True)
    T.insert(0, 'id', [f'D{i + 1:04d}' for i in range(len(T))])
    pan = cari.panel(kerja, 'A')
    L = lapis.muat(kerja, 'A')
    Lr, S8 = (L['L1'], L['L2']), t8.sah8(pan)
    EV = c12.semua_pencetus(kerja, 'A')
    cukup = sorted(n for n, r in S.items() if r.get('cukup'))
    rng = np.random.default_rng(BENIH_KAWALAN)
    K, cuba = [], 0
    while len(K) < N_KAWALAN and cuba < 200000:
        cuba += 1
        nama = cukup[int(rng.integers(len(cukup)))]
        q, ci = int(rng.integers(c5.NQ)), int(rng.integers(c5.NC))
        if q == 0 and ci == 0:
            continue
        q1, q2, f1, f2 = (int(x[0]) for x in c5.nyah(np.asarray([q * c5.NC + ci])))
        ev = EV[nama]
        ev = ev[S8[ev]]
        tp = pan['tempoh'][ev[c5.topeng(pan, Lr, ev, q1, q2, f1, f2)]]
        if min(int((tp == 0).sum()), int((tp == 1).sum())) < c5.N_MIN:
            continue
        K.append(dict(id=f'R{len(K) + 1:03d}', pencetus=nama, induk=t7.induk(nama), ke=0, skor=np.nan, q1=q1, q2=q2, f1=f1, f2=f2))
    out = {'calon': T, 'kawalan': pd.DataFrame(K), 'n_pencetus': len(S), 'n_cukup': len(cukup), 'cuba_kawalan': cuba}
    pickle.dump(out, open(F_(kerja, 'calon'), 'wb'), protocol=4)
    cari.log(f"CS17 calon: {len(T)} calon berskor > 0 daripada {len(cukup)} pencetus cukup isyarat ({T.pencetus.nunique()} pencetus "
             f"berbeza); kawalan rawak {len(K)} (dicuba {cuba})")
    return out


# ---------- penilaian pada kumpulan B ----------
def pegang(pan, ev):
    """(R, sesi jual) bagi "pegang 126 sesi + stop loss 6xATR14, tiada indikator keluar": kernel cs_trend8.hasil_semua tanpa atom."""
    R, SK = t8.hasil_semua(np.ascontiguousarray(ev, dtype=np.int64), pan['o'], pan['l'], pan['c'], pan['atr'], _XT0, _J0, _P0, _B0,
                           t8.PEGANG_MIN)
    return R[:, S_HENTI, 0].astype(np.float64), SK[:, S_HENTI, 0].astype(np.int64)


def ukur(pan, V, L8, ev):
    """Statistik satu peraturan (satu posisi setiap saham) -> (dict, bar beli). ev sudah ditapis tetingkap 126 sesi."""
    ev = np.ascontiguousarray(ev, dtype=np.int64)
    if not len(ev):
        return dict(n=0, tahun=0), ev
    R, sk = pegang(pan, ev)
    amb = teras.satu_posisi(ev, sk, pan['tid'])
    e, R, sk = ev[amb], R[amb], sk[amb]
    tp = pan['tempoh'][e]
    bs = L8[e, 0] > 0
    d = dict(n=int(len(e)), tahun=int(len(np.unique(pan['tarikh'][e] // 10000))), besar=float(L8[e, 0].mean()),
             a_besar=float(V[e, 1].mean()), besar100=float(L8[e, 1].mean()), a_besar100=float(L8[e, 3].mean()),
             menang=float((R > 0).mean()), rugi15=float((R <= -0.15).mean()), tb=float((R >= t8.TB).mean()), purata=float(R.mean()),
             median=float(np.median(R)), pegang=float(np.median(sk) + 1), R_besar=float(R[bs].mean()) if bs.any() else float('nan'))
    d['kl'] = d['besar'] - d['a_besar']
    for j in range(3):
        q = tp == j
        d[f'n_K{j + 1}'] = int(q.sum())
        d[f'kl_K{j + 1}'] = float((L8[e[q], 0] - V[e[q], 1]).mean()) if q.any() else float('nan')
    return d, e


def kunci(kerja):
    """Nilai setiap calon dan kawalan pada kumpulan B (dan belian pada A untuk semakan kembar), "prasyarat sahaja", kes MXL
    -> cs17_kunci.pkl."""
    C = pickle.load(open(F_(kerja, 'calon'), 'rb'))
    semua = pd.concat([C['calon'], C['kawalan']], ignore_index=True)
    param = t7.param_semua(kerja)
    out, t0 = {'_pra': {}}, time.time()
    for set_ in ('B', 'A'):
        pan = cari.panel(kerja, set_)
        L = lapis.muat(kerja, set_)
        Lr = (L['L1'], L['L2'])
        EV = c12.semua_pencetus(kerja, set_)
        S8, V, L8, _ = t8.label_v(pan)
        tk = np.flatnonzero(pan['ticker'] == KES[0])
        for k, r in enumerate(semua.itertuples(), 1):
            e0 = EV[r.pencetus]
            ev = e0[S8[e0]]
            d, e = ukur(pan, V, L8, ev[c5.topeng(pan, Lr, ev, r.q1, r.q2, r.f1, r.f2)])
            o = out.setdefault(r.id, {})
            o['e_' + set_] = e.astype(np.int32)
            if set_ == 'B':
                o.update(d=d, nama=t7.nama7(r.pencetus, param), prasyarat=d13.teks_pra(r.q1, r.q2), penapis=d13.teks_pen(r.f1, r.f2))
                o['kes'] = []
                if len(tk):                                                 # kes rujukan: termasuk isyarat yang tetingkapnya belum lengkap
                    x = e0[(pan['tid'][e0] == tk[0]) & (pan['tarikh'][e0] >= KES[1]) & (pan['tarikh'][e0] <= KES[2])]
                    x = x[c5.topeng(pan, Lr, x, r.q1, r.q2, r.f1, r.f2)]
                    o['kes'] = [(int(pan['tarikh'][i]), round(float(pan['o'][i + 1]), 2)) for i in x if i + 1 < len(pan['o'])]
            if k % 1000 == 0:
                cari.log(f'  CS17 kunci {set_} {k}/{len(semua)} · {time.time() - t0:.0f}s')
        if set_ == 'B':
            sah = np.flatnonzero(S8)
            for q1, q2 in sorted({(int(a), int(b)) for a, b in zip(C['calon'].q1, C['calon'].q2)} - {(-1, -1)}):
                out['_pra'][(q1, q2)] = ukur(pan, V, L8, sah[c5.topeng(pan, Lr, sah, q1, q2, -1, -1)])[0]
            out['_asas'] = dict(besar=float(L8[sah, 0].mean()), besar100=float(L8[sah, 1].mean()), n=int(len(sah)))
    out['_n'] = {s: len(cari.panel(kerja, s)['c']) for s in ('A', 'B')}
    pickle.dump(out, open(F_(kerja, 'kunci'), 'wb'), protocol=4)
    cari.log(f'CS17 kunci: {len(semua)} peraturan · {len(out["_pra"])} prasyarat sahaja · {time.time() - t0:.0f}s')
    return out


def jadual(C, K):
    """Satu baris setiap calon dan kawalan dengan angka kumpulan B (nama lajur serasi dengan cs_daftar13.bacaan / kembar)."""
    baris = []
    for nm, T in (('calon', C['calon']), ('kawalan', C['kawalan'])):
        for r in T.itertuples():
            o = K[r.id]
            d = o['d']
            kl = [d.get(f'kl_K{j}', np.nan) for j in (1, 2, 3)]
            layak = bool(d['n'] >= MIN_BELIAN and d['tahun'] >= MIN_TAHUN)
            pra = K['_pra'].get((int(r.q1), int(r.q2)))
            b = dict(peranan=nm, id=r.id, pencetus=r.pencetus, induk=r.induk, q1=int(r.q1), q2=int(r.q2), f1=int(r.f1), f2=int(r.f2),
                     skor_A=r.skor, nama=o['nama'], prasyarat=o['prasyarat'], penapis=o['penapis'], layak=layak,
                     lulus=bool(layak and all(x == x and x > 0 for x in kl)), kl_terus_K3=kl[2], setahun=d['n'] / s11.TAHUN,
                     kl_prasyarat=pra['kl'] if pra and pra.get('n') else np.nan, kes=';'.join(f'{t}@{h}' for t, h in o.get('kes', [])))
            b.update({k_: v for k_, v in d.items()})
            b['tambah'] = b.get('kl', np.nan) - b['kl_prasyarat'] if b['kl_prasyarat'] == b['kl_prasyarat'] else np.nan
            baris.append(b)
    return pd.DataFrame(baris)


def semua(kerja):
    """(C, K, T dengan kembar_kepada / id_T / untuk_daftar, bacaan)."""
    C = pickle.load(open(F_(kerja, 'calon'), 'rb'))
    K = pickle.load(open(F_(kerja, 'kunci'), 'rb'))
    T = jadual(C, K)
    B = d13.bacaan(T)
    kb = d13.kembar(T, K)
    T['kembar_kepada'] = [kb.get(i, '') if p == 'calon' else '' for i, p in zip(T.id, T.peranan)]
    T['untuk_daftar'] = bool(B['ya']) & (T.peranan == 'calon') & T.lulus & (T.kembar_kepada == '')
    X = T[T.untuk_daftar].sort_values('skor_A', ascending=False, kind='stable')
    peta = {i: f'T{ID_MULA + k:02d}' for k, i in enumerate(X.id)}
    T['id_T'] = [peta.get(i, '') for i in T.id]
    return C, K, T, B


# ---------- laporan ----------
def _bersih(x):
    if isinstance(x, dict):
        return {str(k): _bersih(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_bersih(v) for v in x]
    if isinstance(x, (float, np.floating)):
        return None if x != x else round(float(x), 6)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, np.bool_):
        return bool(x)
    return x


def lapor_(kerja):
    C, K, T, B = semua(kerja)
    os.makedirs(HASIL, exist_ok=True)
    c, kw = T[T.peranan == 'calon'], T[T.peranan == 'kawalan']
    buang = ['peranan', 'kl_terus_K3']
    c.drop(columns=buang).to_csv(os.path.join(HASIL, 'calon.csv.gz'), index=False, float_format='%.5f')
    kw.drop(columns=buang + ['kembar_kepada', 'id_T', 'untuk_daftar', 'kes']).to_csv(os.path.join(HASIL, 'kawalan.csv'), index=False, float_format='%.5f')
    D = c[c.id_T != ''].sort_values(['besar', 'kl'], ascending=False, kind='stable').copy()
    lajur = ['id_T', 'prasyarat', 'nama', 'penapis', 'n', 'setahun', 'tahun', 'besar', 'a_besar', 'kl', 'kl_K1', 'kl_K2', 'kl_K3', 'n_K3',
             'besar100', 'a_besar100', 'menang', 'purata', 'median', 'rugi15', 'tb', 'pegang', 'R_besar', 'kl_prasyarat', 'tambah', 'kes',
             'skor_A', 'pencetus', 'q1', 'q2', 'f1', 'f2']
    D[lajur].rename(columns={'id_T': 'id'}).to_csv(os.path.join(HASIL, 'senarai_t.csv'), index=False, float_format='%.5f')
    Pr = pd.DataFrame([dict(q1=k[0], q2=k[1], prasyarat=d13.teks_pra(k[0], k[1]), **v) for k, v in K['_pra'].items() if v.get('n')])
    Pr = Pr.sort_values('kl', ascending=False)
    Pr['lulus'] = (Pr.n >= MIN_BELIAN) & (Pr.tahun >= MIN_TAHUN) & (Pr.kl_K1 > 0) & (Pr.kl_K2 > 0) & (Pr.kl_K3 > 0)
    Pr.to_csv(os.path.join(HASIL, 'prasyarat.csv'), index=False, float_format='%.5f')
    L = c[c.lulus]
    md = lambda X, k: float(X[k].median()) if len(X) else float('nan')
    B.update(n_kawalan=int(len(kw)), n_kembar=int((L.kembar_kepada != '').sum()), n_daftar=int(len(D)), asas=K['_asas'],
             hasil_tumbuh_calon=float((c.q2 == Q_HASIL).mean()), hasil_tumbuh_daftar=float((D.q2 == Q_HASIL).mean()) if len(D) else float('nan'),
             tambah_daftar=float((D.tambah >= TAMBAH_MIN).mean()) if len(D) else float('nan'), n_kes=int((D.kes != '').sum()),
             median_daftar={k: md(D, k) for k in ('besar', 'a_besar', 'kl', 'besar100', 'menang', 'purata', 'median', 'rugi15', 'tb', 'n', 'setahun', 'tambah')},
             median_lulus={k: md(L, k) for k in ('besar', 'a_besar', 'kl', 'menang', 'purata', 'rugi15')},
             median_kawalan={k: md(kw[kw.layak], k) for k in ('besar', 'a_besar', 'kl', 'menang', 'purata', 'rugi15')},
             id_akhir=D.id_T.map(lambda x: int(x[1:])).max() if len(D) else None)
    json.dump(_bersih(B), open(os.path.join(HASIL, 'bacaan.json'), 'w'), indent=1)
    open(os.path.join(HASIL, 'SENARAI_T.md'), 'w', encoding='utf-8').write(teks_laporan(T, D, Pr, B))
    cari.log(f"CS17 lapor: calon {B['n_calon']}, layak {B['calon_layak']}, lulus {B['n_lulus']} ({B['lulus_calon']:.0%} lawan kawalan "
             f"{B['lulus_kawalan']:.0%}); K3 {B['k3_calon']:.0%} lawan {B['k3_kawalan']:.0%} -> {'BERHASIL' if B['ya'] else 'TIDAK'}; "
             f"kembar {B['n_kembar']}, didaftar {B['n_daftar']}")
    return B


def teks_laporan(T, D, Pr, B):
    p = lambda x, d=0, tanda=False: '–' if x is None or x != x else f'{x * 100:{"+" if tanda else ""}.{d}f}'
    ya = lambda x: 'ya' if x else 'TIDAK'
    L8 = pd.read_csv(os.path.join(SINI, 'hasil', 'CS08', 'papan.csv'))
    m, mk = B['median_daftar'], B['median_kawalan']
    A = ['# CS17: lorong "pegang berbulan-bulan" (T) tanpa had bilangan (backtest; BUKAN bukti)', '',
         'Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 16 Nov 2026 (aa). Dijana `cs_trend17.py`; jangan sunting.', '',
         '- Lorong ini: beli selepas isyarat, pegang hingga 6 bulan (126 hari dagangan) dengan stop loss longgar (6×ATR14), tiada jualan '
         'lain. "Naik besar" = harga tutup mencapai ≥ +50 % dalam 6 bulan SEBELUM mana-mana tutup ≤ −15 %.',
         f"- Saham rawak (mana-mana hari): {p(B['asas']['besar'], 1)} % naik besar; {p(B['asas']['besar100'], 1)} % capai +100 %.",
         f"- Dicari pada saham carian: {B['n_calon']:,} calon (sehingga {N_ATAS} peraturan setiap isyarat beli, tiada had bilangan); "
         f"{B['n_kawalan']} peraturan rawak sebagai kawalan. Dinilai pada saham yang carian tidak lihat. Tiada tapisan Shariah.", '',
         '## 1. Keputusan (ujian ditetapkan dahulu)', '',
         f"- Lulus = ≥ {MIN_BELIAN} belian, ≥ {MIN_TAHUN} tahun, lebih kerap naik besar daripada saham rawak hari sama dalam ketiga-tiga tempoh "
         f"(2010–19, 2020–24, 2025–26).",
         f"- (B1) calon yang lulus: {B['n_lulus']:,} daripada {B['calon_layak']:,} yang cukup belian = {p(B['lulus_calon'])} %; peraturan rawak: "
         f"{p(B['lulus_kawalan'])} % (perlu beza ≥ 20 mata) → {ya(B['b1'])}.",
         f"- (B2) lebih baik daripada rawak pada 2025–26: calon {p(B['k3_calon'])} %; peraturan rawak {p(B['k3_kawalan'])} % (perlu ≥ 60 % dan "
         f"beza ≥ 10 mata) → {ya(B['b2'])}.",
         f"- **Keputusan: {'LULUS' if B['ya'] else 'GAGAL'}.** " + (
             f"{B['n_lulus']:,} lulus; {B['n_kembar']:,} kembar (belian bertindih ≥ 80 %); **{B['n_daftar']:,} setup baharu diberi kod "
             f"`T{ID_MULA}`–`T{B['id_akhir']}`**. Anggaran bahagian yang lulus kerana nasib: {p(B['nasib'])} %." if B['ya'] else
             'Tiada kod T baharu diberi. Senarai lorong ini kekal `T01`–`T12`.'), '']
    if len(D):
        A += ['## 2. Gambaran setup baharu (nilai tengah; saham yang carian tidak lihat)', '',
              '| | Naik besar % | Saham rawak hari sama % | Menang % | Purata setiap dagangan % | Rugi ≥ 15 % % | Dijual ≥ +30 % % | Belian setahun |',
              '|---|---|---|---|---|---|---|---|',
              f"| Setup baharu ({len(D):,}) | {p(m['besar'], 1)} | {p(m['a_besar'], 1)} | {p(m['menang'])} | {p(m['purata'], 1, True)} | {p(m['rugi15'])} | "
              f"{p(m['tb'])} | {m['setahun']:.0f} |",
              f"| Peraturan rawak (kawalan) | {p(mk['besar'], 1)} | {p(mk['a_besar'], 1)} | {p(mk['menang'])} | {p(mk['purata'], 1, True)} | {p(mk['rugi15'])} | – | – |",
              f"| Papan lama `T01`–`T12` (CS08) | {p(L8.besar.median(), 1)} | {p(L8.a_besar.median(), 1)} | {p(L8.menang.median())} | "
              f"{p(L8.purata.median(), 1, True)} | {p(L8.rugi15.median())} | {p(L8.tb.median())} | {L8.setahun.median():.0f} |", '',
              f"- {p(B['hasil_tumbuh_daftar'])} % setup baharu memakai prasyarat \"hasil suku terkini tumbuh ≥ 20 %\" (calon: {p(B['hasil_tumbuh_calon'])} %).",
              f"- {p(B['tambah_daftar'])} % setup baharu menambah ≥ 1 mata di atas prasyaratnya sahaja (nilai tengah tambahan {p(m['tambah'], 1, True)} mata).",
              f"- Kes MXL (Mac–Jun 2026; satu contoh, bukan bukti): {B['n_kes']:,} setup baharu memberi isyarat beli pada MXL.", '',
              '## 3. Senarai (60 teratas ikut kadar naik besar; penuh dalam `senarai_t.csv`)', '',
              '| ID | Prasyarat | Isyarat beli | Syarat saham | Naik besar % (rawak) | Capai +100 % % | Menang % | Purata % | Rugi ≥ 15 % % | Belian | Lebih baik drpd rawak: 2010–19 / 2020–24 / 2025–26 (mata) | Atas prasyarat (mata) | MXL |',
              '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
        for r in D.head(60).itertuples():
            A.append(f"| `{r.id_T}` | {r.prasyarat or '–'} | {r.nama} | {r.penapis or '–'} | **{p(r.besar, 1)}** ({p(r.a_besar, 1)}) | {p(r.besar100, 1)} | "
                     f"{p(r.menang)} | {p(r.purata, 1, True)} | {p(r.rugi15)} | {r.n:,} | {p(r.kl_K1, 1, True)} / {p(r.kl_K2, 1, True)} / {p(r.kl_K3, 1, True)} | "
                     f"{p(r.tambah, 1, True)} | {r.kes.split(';')[0] if r.kes else '–'} |")
        A.append('')
    A += ['## 4. "Prasyarat sahaja" (tanpa isyarat beli; 12 teratas)', '',
          '| Prasyarat | Naik besar % (rawak) | Lebih baik drpd rawak (mata) | 2010–19 / 2020–24 / 2025–26 | Menang % | Purata % | Rugi ≥ 15 % % | Belian | Lulus |',
          '|---|---|---|---|---|---|---|---|---|']
    for r in Pr.head(12).itertuples():
        A.append(f"| {r.prasyarat} | {p(r.besar, 1)} ({p(r.a_besar, 1)}) | {p(r.kl, 1, True)} | {p(r.kl_K1, 1, True)} / {p(r.kl_K2, 1, True)} / {p(r.kl_K3, 1, True)} | "
                 f"{p(r.menang)} | {p(r.purata, 1, True)} | {p(r.rugi15)} | {r.n:,} | {ya(r.lulus)} |")
    A += ['', '## 5. Kaveat', '',
          '- Tiada saham delist dalam data: bagi pegang 6 bulan, saham yang gagal hilang dan angka condong ke atas lebih daripada lorong swing.',
          '- Lorong ini banyak rugi besar: lihat lajur "Rugi ≥ 15 %". Purata dikuasai sebilangan kecil saham yang naik besar.',
          '- 2025–26 pendek (isyarat hingga awal 2026 sahaja, kerana perlu 6 bulan penuh selepas beli).',
          '- Beribu calon disemak pada saham yang sama, jadi sebahagian lulus kerana nasib (anggaran di atas).',
          '- Semakan kembar lawan `T01`–`T12` tidak dapat dibuat (isyarat varian lama tiada dalam folder kerja).',
          '- Kod T bukan kod F: `registry_F.csv` tidak disentuh. Tiada papertrade tanpa keputusan pengguna.', '']
    return '\n'.join(A)


if __name__ == '__main__':
    langkah, kerja = sys.argv[1], sys.argv[2]
    {'skor': skor, 'calon': calon, 'kunci': kunci, 'lapor': lapor_}[langkah](kerja)
