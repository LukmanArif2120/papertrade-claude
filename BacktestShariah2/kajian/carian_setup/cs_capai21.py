"""Carian setup — pusingan CS21 (SPEC pindaan 17 Nov 2026 (ah)): ukuran KEDUA "mencapai +10 % sebelum jatuh 8 %".

Label `c10`: selepas beli pada buka sesi berikutnya (harga P), dalam 63 sesi ada TUTUP >= 1.10 x P sebelum harga menyentuh
0.92 x P. Tiada syarat minggu pertama dan tiada cara pegang. Diukur lawan saham rawak hari sama x tercile ATR % bagi:
(1) setiap isyarat beli asal M / N / P sahaja, (2) setup senarai utama F, (3) setup sepanjang tahun CS20, (4) kawalan rawak
CS20 — semuanya pada kumpulan B (saham yang carian tidak lihat). Pusingan UKURAN: tiada pemilihan, tiada kod baharu.
Guna: python3 cs_capai21.py ukur|lapor <kerja>. Jangan sunting keluaran secara manual."""
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
import cs_cs05 as c5  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_tala7 as t7  # noqa: E402
import cs_teras as teras  # noqa: E402

NAIK, JATUH, HAD = 0.10, 0.08, 63                             # dikunci pindaan (ah)
MIN_BELIAN, MIN_TAHUN_N = 300, 20                             # unit < 300 belian dilaporkan tetapi tidak masuk nilai tengah kumpulan
LABEL = ('c10', 'j8', 'k10')
PUS = 'CS21'
N_PAPAR = 25
F_ = lambda kerja, nama: os.path.join(kerja, f'cs21_{nama}.pkl')


@njit(cache=True, parallel=True)
def label21(ev, o, l, c, naik, jatuh, had):
    """Setiap bar isyarat ev (tetingkap `had` sesi lengkap): [c10, j8, k10] dan sesi keputusan (0 = hari beli). Sentuhan
    -8 % diperiksa dahulu daripada tutup hari yang sama; pada hari beli hanya tutup yang dikira."""
    n = ev.shape[0]
    out = np.zeros((n, 3), np.float32)
    sk = np.zeros(n, np.int64)
    for k in prange(n):
        e = ev[k] + 1
        P = o[e]
        hi, lo = P * (1.0 + naik), P * (1.0 - jatuh)
        res, dk = 0, had - 1
        for d in range(had):
            b = e + d
            if d == 0:
                if c[b] <= lo:
                    res = -1
                elif c[b] >= hi:
                    res = 1
            elif o[b] <= lo or l[b] <= lo:
                res = -1
            elif c[b] >= hi:
                res = 1
            if res != 0:
                dk = d
                break
        out[k, 0] = 1.0 if res == 1 else 0.0
        out[k, 1] = 1.0 if res == -1 else 0.0
        out[k, 2] = 1.0 if c[e + had - 1] >= hi else 0.0
        sk[k] = dk
    return out, sk


def sah63(pan):
    i = np.arange(len(pan['c']))
    return pan['sah'] & (i + HAD < pan['mula'][pan['tid'] + 1])


def asas21(pan):
    """(Lab[bar, 3], As[bar, 3], SK[bar], S63[bar]): label setiap bar layak, asas rawak hari sama x tercile ATR %, sesi
    keputusan, dan topeng bar yang dinilai."""
    S63 = sah63(pan)
    sah = np.flatnonzero(S63)
    Lb, sk = label21(sah, pan['o'], pan['l'], pan['c'], NAIK, JATUH, HAD)
    hari = pan['hari'][sah]
    pct = pd.Series(pan['atr'][sah] / pan['c'][sah]).groupby(hari).rank(pct=True).to_numpy()
    g = hari * 3 + np.minimum((pct * 3).astype(np.int64), 2)
    bil = np.maximum(np.bincount(g), 1)
    N = len(pan['c'])
    Lab, As, SK = np.zeros((N, 3), np.float32), np.zeros((N, 3), np.float32), np.zeros(N, np.int64)
    Lab[sah] = Lb
    As[sah] = np.stack([np.bincount(g, Lb[:, j]) / bil for j in range(3)], 1)[g]
    SK[sah] = sk
    return Lab, As, SK, S63


def ukur21(pan, Lab, As, SK, S63, ev):
    """Statistik satu unit (satu posisi setiap saham sehingga keputusan diketahui)."""
    ev = np.ascontiguousarray(ev[S63[ev]], dtype=np.int64)
    e = ev[teras.satu_posisi(ev, SK[ev], pan['tid'])] if len(ev) else ev
    thn = pan['tarikh'][e] // 10000
    d = dict(n=int(len(e)), tahun=int(len(np.unique(thn))))
    if not len(e):
        return d
    for j, nm in enumerate(LABEL):
        d[nm], d['a_' + nm] = float(Lab[e, j].mean()), float(As[e, j].mean())
    x = Lab[e, 0].astype(float) - As[e, 0]
    y = Lab[e, 1].astype(float) - As[e, 1]
    d['kl_c10'], d['arah10'], d['sesi'] = float(x.mean()), float((x - y).mean()), float(np.median(SK[e]) + 1)
    tp = pan['tempoh'][e]
    for p in range(3):
        q = tp == p
        d[f'n_K{p + 1}'] = int(q.sum())
        d[f'kl_c10_K{p + 1}'] = float(x[q].mean()) if q.any() else np.nan
    g = pd.Series(x).groupby(thn).agg(['size', 'mean'])
    g = g[g['size'] >= MIN_TAHUN_N]
    d['tahun_n'], d['tahun_pos'] = int(len(g)), float((g['mean'] > 0).mean()) if len(g) else np.nan
    return d


def _ev_f(reg, EV, pan, Lr):
    """(id, isyarat, laporan?) bagi setiap baris registry F yang takrifnya boleh dibaca dan isyaratnya ada."""
    import cs_cs07 as c7
    import cs_portfolio6 as p6
    kq1, kq2 = [x[:4] for x in lapis.PASARAN], [x[:4] for x in lapis.KUMPULAN]
    out, langkau = [], []
    for i, r in reg.iterrows():
        try:
            if r.pusingan in ('CS13', 'CS20'):
                b = r.takrif.split('|')
                kod = [x for x in b[4].split('+') if x] if len(b) > 4 else []
                q1 = next((kq1.index(x) for x in kod if x in kq1), -1)
                q2 = next((kq2.index(x) for x in kod if x in kq2), -1)
                fs = [int(x[1:]) - 1 for x in b[1].split('+') if x] + [-1, -1]
                d = dict(pencetus=b[0], q1=q1, q2=q2, f1=fs[0], f2=fs[1])
            else:
                d = c7.dari_takrif7(r.takrif) if r.pusingan == 'CS07' else p6.dari_takrif5(r.takrif)
            ev = EV[d['pencetus']]
        except Exception:
            langkau.append(i)
            continue
        lap = int(d['q2']) >= 0 and lapis.KUMPULAN[int(d['q2'])][:4] == 'QF01'
        out.append((i, ev[c5.topeng(pan, Lr, ev, d['q1'], d['q2'], d['f1'], d['f2'])], bool(lap)))
    return out, langkau


def ukur(kerja):
    """Ukur setiap unit pada kumpulan B -> cs21_unit.pkl (DataFrame) + asas keseluruhan."""
    import cs_lapor as lapor
    import cs_mingguan20 as m20
    t0 = time.time()
    pan = cari.panel(kerja, 'B')
    L = lapis.muat(kerja, 'B')
    Lr = (L['L1'], L['L2'])
    Lab, As, SK, S63 = asas21(pan)
    asal = t7.semua_ev(kerja, 'B', 'asal')
    EV = dict(asal)
    EV.update(t7.semua_ev(kerja, 'B', 'K'))
    param = t7.param_semua(kerja)
    sah = np.flatnonzero(S63)
    tp = pan['tempoh'][sah]
    dasar = dict(bar=int(len(sah)), c10=float(Lab[sah, 0].mean()), j8=float(Lab[sah, 1].mean()), k10=float(Lab[sah, 2].mean()),
                 sesi=float(np.median(SK[sah]) + 1), akhir=int(pan['tarikh'][sah].max()),
                 **{f'c10_K{p + 1}': float(Lab[sah[tp == p], 0].mean()) for p in range(3)})
    cari.log(f"CS21: bar dinilai {dasar['bar']:,} (hingga {dasar['akhir']}); saham rawak: kena {dasar['c10']:.1%}, jatuh dahulu "
             f"{dasar['j8']:.1%}, tiada {1 - dasar['c10'] - dasar['j8']:.1%}")
    R = []

    def tambah(kump, idn, ev, **lain):
        d = ukur21(pan, Lab, As, SK, S63, ev)
        d.update(kumpulan=kump, id=idn, **lain)
        R.append(d)

    # (1) isyarat beli asal sahaja
    for nama in sorted(asal):
        kump = {'M': 'isyarat M sahaja', 'N': 'isyarat N sahaja'}.get(nama[0], 'isyarat indikator (P) sahaja')
        tambah(kump, nama, asal[nama], nama=t7.nama7(nama, param), prasyarat='', penapis='')
    cari.log(f'CS21: isyarat asal {len(asal)} · {time.time() - t0:.0f}s')
    # (2) senarai utama F
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('').set_index('id')
    U = pd.read_csv(os.path.join(SINI, 'hasil', 'CS13', 'senarai_utama.csv')).set_index('id')
    F, langkau = _ev_f(reg.loc[[i for i in U.index if i in reg.index]], EV, pan, Lr)
    for idn, ev, lap in F:
        u = U.loc[idn]
        tambah('F senarai utama: laporan kewangan' if lap else 'F senarai utama: bukan laporan', idn, ev, nama=str(u['nama']),
               prasyarat='' if u['prasyarat'] != u['prasyarat'] else str(u['prasyarat']),
               penapis='' if u['penapis'] != u['penapis'] else str(u['penapis']), terus=float(u['terus']), a_terus=float(u['a_terus']))
    cari.log(f'CS21: senarai utama {len(F)} (dilangkau {len(langkau)}) · {time.time() - t0:.0f}s')
    # (3) + (4) CS20
    n20 = 0
    if os.path.exists(m20.F_(kerja, 'kunci')):
        _, _, T, B20 = m20.semua(kerja)
        for r in T[T.peranan.isin(['calon', 'kawalan'])].itertuples():
            if r.peranan == 'calon' and not r.lulus:
                continue
            kump = 'kawalan rawak sepanjang tahun (CS20)' if r.peranan == 'kawalan' else \
                ('F sepanjang tahun CS20: kod berdaftar' if r.id_F else 'F sepanjang tahun CS20: lulus, tiada kod')
            ev = EV[r.pencetus]
            tambah(kump, r.id_F or r.id, ev[c5.topeng(pan, Lr, ev, int(r.q1), int(r.q2), int(r.f1), int(r.f2))], nama=r.nama,
                   prasyarat=r.prasyarat, penapis=r.penapis, terus=float(r.terus), a_terus=float(r.a_terus), mgg_semua=float(r.mgg_semua))
            n20 += 1
    T21 = pd.DataFrame(R)
    T21['layak'] = T21.n >= MIN_BELIAN
    pickle.dump({'T': T21, 'dasar': dasar, 'langkau': langkau, 'n20': n20}, open(F_(kerja, 'unit'), 'wb'), protocol=4)
    cari.log(f'CS21 ukur: {len(T21)} unit ({n20} daripada CS20) · {time.time() - t0:.0f}s')
    return T21


def kumpulan(T):
    """Satu baris setiap kumpulan (unit layak sahaja): nilai tengah dan bahagian unit yang lebih baik daripada rawak."""
    out = []
    for k, g in T[T.layak].groupby('kumpulan', sort=False):
        m = g.median(numeric_only=True)
        tiga = (g.kl_c10_K1 > 0) & (g.kl_c10_K2 > 0) & (g.kl_c10_K3 > 0)
        out.append(dict(kumpulan=k, unit=len(g), belian=float(m.n), c10=m.c10, a_c10=m.a_c10, kl_c10=m.kl_c10, j8=m.j8, a_j8=m.a_j8, k10=m.k10,
                        a_k10=m.a_k10, arah10=m.arah10, pos=float((g.kl_c10 > 0).mean()), pos_K1=float((g.kl_c10_K1 > 0).mean()),
                        pos_K2=float((g.kl_c10_K2 > 0).mean()), pos_K3=float((g.kl_c10_K3 > 0).mean()), pos_tiga=float(tiga.mean()),
                        kl_K1=m.kl_c10_K1, kl_K2=m.kl_c10_K2, kl_K3=m.kl_c10_K3, arah_pos=float((g.arah10 > 0).mean()),
                        tahun_pos=m.tahun_pos, terus=m.get('terus', np.nan), a_terus=m.get('a_terus', np.nan)))
    return pd.DataFrame(out)


def lapor_(kerja):
    import cs_lapor as lapor
    Z = pickle.load(open(F_(kerja, 'unit'), 'rb'))
    T, D = Z['T'], Z['dasar']
    G = kumpulan(T)
    d_ = os.path.join(SINI, 'hasil', PUS)
    os.makedirs(d_, exist_ok=True)
    lajur = ['kumpulan', 'id', 'nama', 'prasyarat', 'penapis', 'n', 'tahun', 'layak', 'c10', 'a_c10', 'kl_c10', 'kl_c10_K1', 'kl_c10_K2',
             'kl_c10_K3', 'j8', 'a_j8', 'arah10', 'k10', 'a_k10', 'sesi', 'tahun_n', 'tahun_pos', 'n_K1', 'n_K2', 'n_K3', 'terus', 'a_terus',
             'mgg_semua']
    T.reindex(columns=lajur).to_csv(os.path.join(d_, 'unit.csv.gz'), index=False, float_format='%.5f')
    G.to_csv(os.path.join(d_, 'kumpulan.csv'), index=False, float_format='%.5f')
    bersih = lambda v: None if isinstance(v, float) and v != v else v
    json.dump({'naik': NAIK, 'jatuh': JATUH, 'had': HAD, 'min_belian': MIN_BELIAN, 'dasar': {k: bersih(v) for k, v in D.items()},
               'n_unit': int(len(T)), 'n_layak': int(T.layak.sum()), 'f_dilangkau': len(Z['langkau']), 'n_cs20': Z['n20'],
               'kumpulan': {r['kumpulan']: {k: bersih(v) for k, v in r.items() if k != 'kumpulan'} for r in G.to_dict('records')}},
              open(os.path.join(d_, 'bacaan.json'), 'w'), indent=1, sort_keys=True)
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    p = lambda x, k=0, t=False: '–' if x is None or x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')
    tx = lambda s: s if isinstance(s, str) and s.strip() else '–'
    A = ['# CS21: ukuran kedua — "mencapai +10 % sebelum jatuh 8 %" dalam 3 bulan (backtest; BUKAN bukti)', '', status, '',
         'Dijana `kajian/carian_setup/cs_capai21.py`. Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 17 Nov 2026 (ah). '
         '**Jangan sunting secara manual.** Pusingan UKURAN: tiada pemilihan dan tiada kod baharu.', '',
         '## 1. Ukuran', '',
         f"- **Kena** = selepas beli pada buka esok, dalam {HAD} sesi (≈ 3 bulan) ada harga TUTUP ≥ +{NAIK:.0%} sebelum harga menyentuh −{JATUH:.0%}. "
         'Tiada syarat "mesti naik dalam minggu pertama" dan tiada cara pegang.',
         f"- **Jatuh dahulu** = menyentuh −{JATUH:.0%} sebelum mencapai +{NAIK:.0%}. **Terus naik** (maklumat) = tutup sesi ke-{HAD} masih ≥ +{NAIK:.0%}.",
         '- Semua angka pada saham yang carian tidak lihat; kurungan = saham rawak yang dibeli pada hari yang sama (tercile ATR % sama).',
         f"- **Saham rawak (semua {D['bar']:,} bar layak hingga {D['akhir']}):** kena {p(D['c10'], 1)} %, jatuh dahulu {p(D['j8'], 1)} %, "
         f"tiada kedua-duanya {p(1 - D['c10'] - D['j8'], 1)} %; terus naik {p(D['k10'], 1)} %. Jadi angka mentah \"kena\" tinggi bagi SEMUA "
         'unit; yang bermakna hanya beza lawan rawak.', '',
         f'## 2. Setiap kumpulan (nilai tengah unit dengan ≥ {MIN_BELIAN} belian)', '',
         '| Kumpulan | Unit | **Kena %** (rawak) | Beza (mata) | Jatuh dahulu % (rawak) | Terus naik % (rawak) | Unit lebih baik daripada rawak | '
         '…dalam 2010–19 / 2020–24 / 2025–26 | …ketiga-tiga tempoh | Tangkap % ukuran utama (rawak) |', '|---' * 10 + '|']
    for r in G.itertuples():
        A.append(f"| {r.kumpulan} | {r.unit:,} | **{p(r.c10, 1)}** ({p(r.a_c10, 1)}) | {p(r.kl_c10, 1, True)} | {p(r.j8, 1)} ({p(r.a_j8, 1)}) | "
                 f"{p(r.k10, 1)} ({p(r.a_k10, 1)}) | {p(r.pos)} % | {p(r.pos_K1)} / {p(r.pos_K2)} / {p(r.pos_K3)} % | {p(r.pos_tiga)} % | "
                 f"{p(r.terus, 1)} ({p(r.a_terus, 1)}) |")
    A += ['', '- "Beza" positif tetapi "jatuh dahulu" juga lebih tinggi daripada rawak = unit itu memilih saham yang lebih bergerak (naik DAN '
          'jatuh), bukan saham yang lebih kerap naik.', '']
    kepala = ['| ID | Isyarat beli | Prasyarat | Penapis saham | Belian | **Kena %** (rawak) | Beza 2010–19 / 2020–24 / 2025–26 (mata) | '
              'Jatuh dahulu % (rawak) | Terus naik % (rawak) |', '|---' * 9 + '|']
    baris = lambda r: (f"| `{r.id}` | {tx(r.nama)} | {tx(r.prasyarat)} | {tx(r.penapis)} | {r.n:,} | **{p(r.c10, 1)}** ({p(r.a_c10, 1)}) | "
                       f"{p(r.kl_c10_K1, 1, True)} / {p(r.kl_c10_K2, 1, True)} / {p(r.kl_c10_K3, 1, True)} | {p(r.j8, 1)} ({p(r.a_j8, 1)}) | "
                       f"{p(r.k10, 1)} ({p(r.a_k10, 1)}) |")
    bhg = 3
    for tajuk, kumps in (('Isyarat beli M dan N sahaja (tanpa syarat, tanpa prasyarat)', ['isyarat M sahaja', 'isyarat N sahaja']),
                         ('Setup F sepanjang tahun (CS20, kod berdaftar)', ['F sepanjang tahun CS20: kod berdaftar']),
                         ('Setup F senarai utama: bukan laporan kewangan', ['F senarai utama: bukan laporan']),
                         ('Setup F senarai utama: laporan kewangan', ['F senarai utama: laporan kewangan'])):
        X = T[T.kumpulan.isin(kumps) & T.layak]
        if not len(X):
            continue
        tiga = X[(X.kl_c10_K1 > 0) & (X.kl_c10_K2 > 0) & (X.kl_c10_K3 > 0)]
        A += [f'## {bhg}. {tajuk}', '',
              f"- {len(X):,} unit dengan ≥ {MIN_BELIAN} belian; lebih baik daripada rawak dalam ketiga-tiga tempoh: **{len(tiga):,}**; daripadanya "
              f"\"jatuh dahulu\" tidak melebihi rawak: {int((tiga.j8 <= tiga.a_j8).sum()):,}.",
              f"- {min(N_PAPAR, len(tiga))} teratas antara yang lebih baik dalam ketiga-tiga tempoh, ikut beza lawan rawak (susunan SELEPAS melihat "
              'hasil; bukan pemilihan):', ''] + kepala + [baris(r) for r in tiga.sort_values('kl_c10', ascending=False).head(N_PAPAR).itertuples()] + ['']
        bhg += 1
    A += [f'## {bhg}. Kaveat', '',
          '- Ukuran ini lebih longgar daripada ukuran utama; pelajaran CS12: carian ikut ukuran longgar lulus pada saham tidak dilihat tetapi '
          'gagal pada 2025–26. Lajur 2025–26 di sini wajib dibaca.',
          '- Isyarat M / N di sini ialah isyarat beli sahaja (mod tanpa intai), bukan kaedah penuh dengan keluar masing-masing.',
          '- Tiada saham delist dalam data: "kena" condong ke atas dan "jatuh dahulu" condong ke bawah bagi semua unit, termasuk saham rawak.',
          '- Jadual teratas disusun selepas melihat hasil pada saham yang sama; sebahagian kedudukan ialah nasib. Senarai penuh: `unit.csv.gz`.',
          '- Backtest sahaja; tiada papertrade tanpa keputusan pengguna; kad skor kekal satu-satunya keputusan wang sebenar.', '']
    open(os.path.join(d_, 'CAPAI10.md'), 'w', encoding='utf-8').write('\n'.join(A))
    cari.log(f"CS21 lapor: {len(T)} unit, {int(T.layak.sum())} layak, {len(G)} kumpulan")
    return T, G


if __name__ == '__main__':
    cmd, kerja = sys.argv[1], sys.argv[2]
    if cmd == 'ukur':
        ukur(kerja)
    elif cmd == 'lapor':
        lapor_(kerja)
    else:
        raise SystemExit(f'arahan tidak dikenali: {cmd}')
