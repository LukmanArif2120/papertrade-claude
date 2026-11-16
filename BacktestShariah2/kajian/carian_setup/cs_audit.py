"""Carian setup — AUDIT proses menjana F lawan standard dan matlamat (SPEC pindaan 14 Nov 2026 (ad), asalnya (u) di cawangan lama
`claude/dreamy-lovelace-38z7wm`). Dibawa ke `main` 16 Nov 2026; `hasil/AUDIT_*` ialah REKOD 14 Nov 2026 (95 setup berdaftar ketika itu) dan
TIDAK dijana semula; `matriks()` kini meliputi registry semasa.

Bukan pusingan carian: tiada setup baharu, tiada perubahan pada pangkat, `registry_F.csv` atau kohort.
  A  matriks pematuhan setiap baris `registry_F.csv` (senarai semak A1-A11 dikunci dalam pindaan (ad));
  B  ukuran pandang ke hadapan tarikh earnings (`QF01`, `QF04`): varian A (asal), J (berjadual), L (luar jadual), P (ramalan
     daripada masa lalu sahaja);
  C  kebolehpercayaan pangkat: kelebihan `terus` pada dua belahan saham dan dua belahan tahun;
  D  semakan proses (kekonsistenan laporan, kohort).
Guna: python3 cs_audit.py <kerja>   (panel_B, benih_B, lapis_B, asasL_B, siri keluar CS07 sudah ada)
      python3 cs_audit.py --lapor   (tulis semula AUDIT_F.md daripada csv)
Keluaran: hasil/AUDIT_F.md, AUDIT_F.csv, AUDIT_earnings.csv. Jangan sunting keluaran secara manual."""
import hashlib
import json
import os
import re
import sys

import numpy as np
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
HASIL = os.path.join(SINI, 'hasil')
BS2 = os.path.dirname(os.path.dirname(SINI))
REG_F = os.path.join(BS2, 'data', 'registry_F.csv')

TOLERANSI_JADUAL, MIN_SEJARAH, MIN_BELAH, MIN_BERTAHAN = 10, 3, 30, 100     # dikunci pindaan (ad)
HAD_JUAL_AWAL, HAD_POTONG = 0.10, 0.90
MIN_JUAL_IND = 0.10                                                     # penjelasan (ad)-2 (post-hoc)
VARIAN = ('A', 'J', 'L', 'P')
KUNCI = ('K1', 'K2', 'K3')
SEMAK = ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10')


# ---------- Bahagian A: matriks pematuhan (tanpa data harga) ----------
def _bhg(takrif):
    b = str(takrif).split('|')
    return b + [''] * (5 - len(b))


def matriks(reg=None, akhir=None):
    """Satu baris setiap setup F: semakan A1-A11 (True / False / None = tidak boleh dinilai)."""
    reg = pd.read_csv(REG_F, dtype=str).fillna('') if reg is None else reg
    akhir = pd.read_csv(os.path.join(HASIL, 'KEDUDUKAN_AKHIR.csv')) if akhir is None else akhir
    K = akhir.set_index('id')
    with open(os.path.join(BS2, 'jejak_f', 'kohort.json')) as f:
        kohort = {a['id'] for a in json.load(f)['ahli']}
    baris = []
    for r in reg.itertuples():
        pencetus, pen, henti, keluar, pra = _bhg(r.takrif)
        kq = [re.sub(r'@.*', '', k) for k in pra.split('+') if k]
        fs = [re.sub(r'@.*', '', k) for k in pen.split('+') if k]
        # CS01-CS04: prasyarat pasaran wujud sebagai penapis F26/F27/F28 (lajur `prasyarat` registry)
        pra_pasaran = any(k[:2] in ('QA', 'QB', 'QC', 'QG', 'QH') for k in kq) or r.prasyarat not in ('', 'tiada', '–')
        pra_kumpulan = any(k[:2] in ('QD', 'QE', 'QF') for k in kq)
        n_pen = len([f for f in fs if f not in ('F26', 'F27', 'F28')])
        ada = r.id in K.index
        k = K.loc[r.id] if ada else None
        ind = keluar.strip() != 'X00'
        aktif = bool(re.search(r'@(5|10)\b', keluar))
        b = {'id': r.id, 'pusingan': r.pusingan, 'takrif': r.takrif, 'kohort': r.id in kohort,
             'kedudukan': int(k.kedudukan) if ada else None,
             'pra_pasaran': pra_pasaran, 'pra_kumpulan': pra_kumpulan, 'n_penapis': n_pen, 'henti': henti,
             'keluar_aktif_selepas_untung': aktif, 'earnings_hadapan': any(q in ('QF01', 'QF04') for q in kq),
             'A1': pra_pasaran or pra_kumpulan, 'A2': bool(pencetus), 'A3': bool(henti), 'A4': ind, 'A5': True,
             'A6': ada, 'A7': bool(k.dipercayai) if ada else None, 'A8': bool(k.purata > 0) if ada else None,
             'A9': bool(k.jual_awal <= HAD_JUAL_AWAL) if ada else None,
             'A10': (bool(k.R_pelari >= HAD_POTONG * k.R_pelari_x00) if ind else True) if ada else None}
        b['A11'] = not b['earnings_hadapan']
        b['struktur_lengkap'] = bool(b['A1'] and b['A2'] and b['A3'] and b['A4'])
        b['menepati_semua'] = bool(b['struktur_lengkap'] and all(b[x] is True for x in SEMAK[4:]))
        if ada:
            b.update(belian=int(k.belian), terus=float(k.terus), a_terus=float(k.a_terus), tp=float(k.tp),
                     menang=float(k.menang), purata=float(k.purata), rugi8=float(k.rugi8), jual_awal=float(k.jual_awal),
                     R_pelari=float(k.R_pelari), R_pelari_x00=float(k.R_pelari_x00), liputan=float(k.liputan))
        baris.append(b)
    return pd.DataFrame(baris)


# ---------- Bahagian B: varian prasyarat earnings ----------
def ramalan(ev):
    """ev: indeks sesi peristiwa (menaik). Pulangkan ramalan[j], j = 0..len(ev): ramalan peristiwa ke-j daripada peristiwa
    sebelum j sahaja = ev[j-1] + median hingga 4 jarak terakhir; NaN jika kurang MIN_SEJARAH peristiwa terdahulu."""
    out = np.full(len(ev) + 1, np.nan)
    for j in range(MIN_SEJARAH, len(ev) + 1):
        lalu = ev[max(0, j - 5):j]
        out[j] = ev[j - 1] + np.median(np.diff(lalu))
    return out


def kelas(ev):
    """0 = berjadual, 1 = luar jadual, 2 = tiada sejarah, bagi setiap peristiwa."""
    r = ramalan(ev)[:len(ev)]
    return np.where(np.isnan(r), 2, np.where(np.abs(ev - r) <= TOLERANSI_JADUAL, 0, 1))


def peristiwa(pan):
    """Indeks sesi peristiwa 8-K item 2.02 setiap saham; logik `cs_prasyarat.earnings` (lewat = selepas tutup)."""
    e = pd.read_csv(os.path.join(BS2, 'data', 'sec', 'earnings_8k.csv'), usecols=['saham', 'tarikh_fail', 'masa_terima', 'items'])
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


def topeng_satu(ev, T, x1=5, x4=20):
    """Topeng setiap bar satu saham: QF01 dan QF04 di bawah setiap varian. Pulangkan dict kod -> ndarray bool [T]."""
    i = np.arange(T)
    kn = np.searchsorted(ev, i, 'right')                               # peristiwa seterusnya (> i); = bilangan peristiwa <= i
    ada_n = kn < len(ev)
    hingga = np.where(ada_n, ev[np.minimum(kn, len(ev) - 1)] - i, 10 ** 6)
    kl = np.where(ada_n, kelas(ev)[np.minimum(kn, len(ev) - 1)], 9)
    r = ramalan(ev)[kn]                                                # memakai peristiwa <= i sahaja
    rh = np.where(np.isnan(r), -10 ** 6, r - i)
    a1 = (hingga >= 1) & (hingga <= x1)
    return {'QF01_A': a1, 'QF01_J': a1 & (kl == 0), 'QF01_L': a1 & (kl != 0), 'QF01_P': (rh >= 1) & (rh <= x1),
            'QF04_A': ada_n & (hingga > x4), 'QF04_P': ~np.isnan(r) & (rh > x4)}


def topeng_earnings(pan):
    N = len(pan['c'])
    V = {k: np.zeros(N, bool) for k in ('QF01_A', 'QF01_J', 'QF01_L', 'QF01_P', 'QF04_A', 'QF04_P')}
    n_kelas = np.zeros(3, np.int64)
    for t, ev in peristiwa(pan).items():
        a, b = pan['mula'][t], pan['mula'][t + 1]
        for k, m in topeng_satu(ev, b - a).items():
            V[k][a:b] = m
        n_kelas += np.bincount(kelas(ev), minlength=3)
    return V, n_kelas


# ---------- penilaian pada kumpulan B ----------
def nilai(kerja):
    import cs_akhir as ak
    import cs_atom as atom
    import cs_cari as cari
    import cs_cs05 as c5
    import cs_cs07 as c7
    import cs_keluar7 as k7
    import cs_lapis as lapis
    import cs_lengkap as lg
    import cs_pegang as pg
    import cs_portfolio6 as p6
    import cs_tala7 as t7
    import cs_teras as teras
    pan, _, EV, X, L = c5._sedia(kerja, 'B')
    Lr, Tb = (L['L1'], L['L2']), lg.muat_asas(kerja, 'B')
    N, sah, g, ng = len(pan['c']), np.flatnonzero(pan['sah']), Tb['g'], np.maximum(Tb['n'], 1)
    Lb = ak.label2(sah, pan['o'], pan['l'], pan['c'])
    trs, a_trs = np.zeros(N, np.float32), np.zeros(N, np.float32)
    trs[sah] = Lb[:, 1]
    a_trs[sah] = (np.bincount(g[sah], Lb[:, 1], minlength=len(ng)) / ng)[g[sah]]
    XA = k7.siri_set(kerja, 'B')
    V, n_kelas = topeng_earnings(pan)
    kod2 = [x[:4] for x in lapis.KUMPULAN]
    for q in ('QF01', 'QF04'):                                          # pariti: varian A = lapisan yang dipakai carian
        assert np.array_equal(V[f'{q}_A'][sah], Lr[1][kod2.index(q), sah] > 0), q
    # penjelasan (u)-1: kumpulan A/B sendiri ialah belahan md5(ticker), jadi belahan saham memakai md5('audit:' + ticker)
    belah_s = np.asarray([int(hashlib.md5(('audit:' + t).encode()).hexdigest(), 16) % 2 for t in pan['ticker']])[pan['tid']]
    belah_t = (pan['tarikh'] // 10000) % 2
    akhir = pd.read_csv(os.path.join(HASIL, 'KEDUDUKAN_AKHIR.csv')).set_index('id')
    reg = pd.read_csv(REG_F, dtype=str).fillna('')

    def ukur(e0, d, penuh=False):
        St = k7.sedia_pan(pan, XA, e0)
        R, sk = k7.hasil(*St[:7], k7.A1, k7.A2, k7.OP, d['s'], d['kol'])
        amb = teras.satu_posisi(e0, sk, pan['tid'])
        if penuh:                                                       # (u)-2: sesi jual lawan "pegang sahaja" henti sama
            return e0[amb], R[amb], sk[amb], k7.hasil(*St[:7], k7.A1, k7.A2, k7.OP, d['s'], 0)[1][amb]
        return e0[amb], R[amb]

    def ringkas(e, R):
        o = {'belian': len(e)}
        if len(e) == 0:
            return o
        kl = trs[e] - a_trs[e]
        o.update(terus=float(trs[e].mean()), a_terus=float(a_trs[e].mean()), kl=float(kl.mean()),
                 tp=float(((X[e, 0] > 0) & (R >= lg.JADI)).mean()), purata=float(R.mean()), menang=float((R > 0).mean()),
                 rugi8=float((R <= lg.RUGI).mean()), rugi15=float((R <= -0.15).mean()))
        for i, t in enumerate(KUNCI):
            q = pan['tempoh'][e] == i
            o[f'n_{t}'], o[f'kl_{t}'] = int(q.sum()), (float(kl[q].mean()) if q.any() else np.nan)
        o['bertahan'] = bool(len(e) >= MIN_BERTAHAN and all(o[f'kl_{t}'] > 0 for t in KUNCI))
        return o

    baris_e, tambahan = [], []
    for r in reg.itertuples():
        if r.id not in akhir.index:
            continue
        cs07 = r.pusingan == 'CS07'
        if cs07:
            d = c7.dari_takrif7(r.takrif)
            ev = t7.ev_satu(kerja, 'B', d['pencetus'])
        else:
            d = p6.dari_takrif5(r.takrif)
            ev = EV[d['pencetus']]
            d['s'], d['kol'] = pg.lama_ke_baharu(d['lajur'])
        e, R, sk, sk0 = ukur(ev[c5.topeng(pan, Lr, ev, d['q1'], d['q2'], d['f1'], d['f2'])], d, True)
        assert len(e) == int(akhir.loc[r.id, 'belian']), (r.id, len(e))          # pariti dengan kedudukan akhir
        assert abs(float(trs[e].mean()) - float(akhir.loc[r.id, 'terus'])) < 1e-4, r.id
        kl = trs[e] - a_trs[e]
        t = {'id': r.id, 'rugi15': float((R <= -0.15).mean()), 'rugi_terburuk': float(R.min()),
             'jual_indikator': float((sk < sk0).mean()), 'pegang': float(sk.mean() + 1)}
        for nama, bl in (('s', belah_s[e]), ('t', belah_t[e])):
            for h in (0, 1):
                q = bl == h
                t[f'n_{nama}{h}'], t[f'kl_{nama}{h}'] = int(q.sum()), (float(kl[q].mean()) if q.sum() >= MIN_BELAH else np.nan)
        tambahan.append(t)
        q2 = kod2[d['q2']] if d['q2'] >= 0 else ''
        if q2 in ('QF01', 'QF04'):
            asas = c5.topeng(pan, Lr, ev, d['q1'], -1, d['f1'], d['f2'])
            for v in VARIAN:
                if f'{q2}_{v}' not in V:
                    continue
                ev_, Rv = ukur(ev[asas & V[f'{q2}_{v}'][ev]], d)
                if v == 'A':
                    assert np.array_equal(ev_, e), r.id
                baris_e.append({'id': r.id, 'kedudukan': int(akhir.loc[r.id, 'kedudukan']), 'prasyarat': q2, 'varian': v,
                                **ringkas(ev_, Rv)})
    # asas: semua bar layak di bawah setiap varian (kesan earnings itu sendiri, tanpa pencetus)
    for k in sorted(V):
        e = sah[V[k][sah]]
        baris_e.append({'id': 'SEMUA', 'kedudukan': 0, 'prasyarat': k[:4], 'varian': k[5:], 'belian': len(e),
                        'terus': float(trs[e].mean()), 'a_terus': float(a_trs[e].mean()),
                        'kl': float((trs[e] - a_trs[e]).mean()), 'bahagian_bar': len(e) / len(sah)})
    E = pd.DataFrame(baris_e)
    E.to_csv(os.path.join(HASIL, 'AUDIT_earnings.csv'), index=False, float_format='%.5f')
    M = matriks(reg).merge(pd.DataFrame(tambahan), on='id', how='left')
    M['A4b'] = np.where(M.A6 == True, M.A4 & (M.jual_indikator >= MIN_JUAL_IND), None)   # noqa: E712
    M.to_csv(os.path.join(HASIL, 'AUDIT_F.csv'), index=False, float_format='%.5f')
    meta = {'peristiwa': {'berjadual': int(n_kelas[0]), 'luar_jadual': int(n_kelas[1]), 'tiada_sejarah': int(n_kelas[2])},
            'bar_layak': int(len(sah)), 'asas_terus': float(Lb[:, 1].mean()), 'tempoh': [list(map(int, t[1:])) for t in atom.TEMPOH['B']]}
    with open(os.path.join(HASIL, 'AUDIT_meta.json'), 'w') as f:
        json.dump(meta, f, indent=1)
    cari.log(f'audit: {len(M)} setup, {len(E)} baris earnings; peristiwa {meta["peristiwa"]}')


# ---------- laporan ----------
def _spearman(a, b):
    q = a.notna() & b.notna()
    return float(a[q].rank().corr(b[q].rank())), int(q.sum())


def belah(M):
    """Bahagian C: Spearman dan nasib 10 teratas separuh pertama pada separuh kedua, bagi belahan saham dan tahun."""
    out = {}
    for nama in ('s', 't'):
        a, b = M[f'kl_{nama}0'], M[f'kl_{nama}1']
        rho, n = _spearman(a, b)
        q = a.notna() & b.notna()
        atas = M[q].nlargest(10, f'kl_{nama}0')
        atas2 = M[q].nlargest(10, f'kl_{nama}1')
        out[nama] = {'rho': rho, 'n': n, 'median_semua_0': float(a[q].median()), 'median_semua_1': float(b[q].median()),
                     'atas0_pada_0': float(atas[f'kl_{nama}0'].median()), 'atas0_pada_1': float(atas[f'kl_{nama}1'].median()),
                     'atas1_pada_1': float(atas2[f'kl_{nama}1'].median()), 'atas1_pada_0': float(atas2[f'kl_{nama}0'].median()),
                     'positif_dua': int(((a > 0) & (b > 0))[q].sum())}
    return out


def lapor():
    M = pd.read_csv(os.path.join(HASIL, 'AUDIT_F.csv'))
    E = pd.read_csv(os.path.join(HASIL, 'AUDIT_earnings.csv'))
    with open(os.path.join(HASIL, 'AUDIT_meta.json')) as f:
        meta = json.load(f)
    reg = pd.read_csv(REG_F)
    try:
        sys.path.insert(0, os.path.join(BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    b = lambda s: M[s].map({True: True, False: False, 'True': True, 'False': False})
    for k in SEMAK + ('A11', 'A4b', 'struktur_lengkap', 'menepati_semua', 'kohort', 'pra_pasaran', 'pra_kumpulan'):
        M[k] = b(k)
    p = lambda x, k=1, t=False: '–' if x is None or x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')
    ya = lambda x: '–' if x is None or x != x else ('✓' if x else '✗')
    n = len(M)
    D = M[M.A6 == True]                                                 # noqa: E712
    T = D[D.A7 == True]                                                 # noqa: E712
    A = ['# Audit proses menjana F lawan standard dan matlamat (BUKAN keputusan; tiada perubahan pangkat)', '', status, '',
         'Dijana `kajian/carian_setup/cs_audit.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (ad) [asalnya (u) di cawangan lama], dikomit '
         'sebelum dijalankan. **Jangan sunting secara manual.**', '',
         '## 1. Jawapan ringkas', '',
         f'Daripada **{n}** setup F berdaftar:', '',
         '| Semakan | Lulus | Gagal | Tidak dinilai |', '|---|---|---|---|']
    nama = {'A1': 'A1 ada prasyarat (pasaran / kumpulan / syarikat)', 'A2': 'A2 ada syarat saham (pencetus)',
            'A3': 'A3 ada henti rugi', 'A4': 'A4 keluar ialah indikator (bukan `X00`)', 'A5': 'A5 tiada sasaran untung tetap',
            'A6': 'A6 dinilai di bawah kayu ukur akhir + pegang minimum', 'A7': 'A7 "dipercayai"',
            'A8': 'A8 purata setiap dagangan > 0', 'A9': f'A9 dijual sebelum sesi ke-4 ≤ {HAD_JUAL_AWAL * 100:.0f} % dagangan',
            'A10': 'A10 indikator keluar tidak memotong pelari', 'A11': 'A11 tidak bergantung pada tarikh earnings masa hadapan',
            'A4b': f'A4b (post-hoc) indikator keluar benar-benar menjual (≥ {MIN_JUAL_IND * 100:.0f} % dagangan)'}
    for k in SEMAK + ('A11', 'A4b'):
        s = M[k]
        A.append(f'| {nama[k]} | {int((s == True).sum())} | {int((s == False).sum())} | {int(s.isna().sum())} |')   # noqa: E712
    sl, ms = M[M.struktur_lengkap], M[M.menepati_semua]
    mb = ms[ms.A4b == True]                                             # noqa: E712
    A += ['', f'- **Struktur lengkap ikut matlamat** (prasyarat + syarat + henti + keluar INDIKATOR): **{len(sl)}** daripada {n}.',
          f'- **Menepati semua semakan A1–A10:** **{len(ms)}** daripada {n}'
          + (': ' + ', '.join(f'`{i}`' for i in ms.id) if len(ms) else '') + '.',
          f'- **Menepati semua DAN indikator keluarnya benar-benar menjual (A4b):** **{len(mb)}**'
          + (': ' + ', '.join(f'`{i}`' for i in mb.id) if len(mb) else '') + '.',
          f'- Daripada {len(ms)} itu, yang TIDAK bergantung pada tarikh earnings masa hadapan (A11): '
          f'**{int(ms.A11.sum())}**' + (': ' + ', '.join(f'`{i}`' for i in ms[ms.A11].id) if ms.A11.any() else '') + '.',
          f'- 10 teratas `KEDUDUKAN_AKHIR`: {int((D.nsmallest(10, "kedudukan").A4 == False).sum())} tiada indikator keluar (`X00`); '   # noqa: E712
          f'{int(D.nsmallest(10, "kedudukan").earnings_hadapan.sum())} memakai tarikh earnings masa hadapan.',
          f'- Kohort jejak hadapan ({int(M.kohort.sum())} setup): '
          + ', '.join(f"`{r.id}` {'tidak dinilai' if r.A6 != True else ('dipercayai' if r.A7 == True else 'TIDAK dipercayai')}"   # noqa: E712
                      + ('' if r.A6 != True or r.A8 == True else ', purata negatif') for r in M[M.kohort].itertuples()) + '.', '']   # noqa: E712
    # --- matriks
    A += ['## 2. Matriks setiap setup', '',
          'pra = prasyarat (P pasaran, K kumpulan/syarikat) · pen = bilangan penapis saham · jual ind. = % dagangan yang dijual '
          'lebih awal oleh indikator keluar · pegang = purata sesi · awal = % dagangan dijual sebelum sesi ke-4 · r15 = % dagangan '
          'rugi ≥ 15 % · potong = untung terealisasi pada pelari ÷ "pegang sahaja" · E = memakai tarikh earnings masa hadapan.', '',
          '| ID | pus. | ked. | pra | pen | henti | keluar | A4 ind. | jual ind. % | pegang | A6 nilai | A7 perc. | A8 purata % | A9 awal % '
          '| A10 potong | r15 % | E | lengkap | semua |', '|' + '---|' * 19]
    for r in M.itertuples():
        kel = _bhg(r.takrif)[3]
        pot = '–' if r.A6 != True or r.A4 != True or not r.R_pelari_x00 else f'{r.R_pelari / r.R_pelari_x00:.2f}'   # noqa: E712
        A.append(f"| `{r.id}` | {r.pusingan} | {'–' if r.kedudukan != r.kedudukan else int(r.kedudukan)} | "
                 f"{('P' if r.pra_pasaran else '') + ('K' if r.pra_kumpulan else '') or '✗'} | {r.n_penapis} | {r.henti} | {kel} | "
                 f"{ya(r.A4)} | {p(r.jual_indikator) if r.A6 == True else '–'} | "   # noqa: E712
                 f"{f'{r.pegang:.1f}' if r.A6 == True else '–'} | "   # noqa: E712
                 f"{ya(r.A6)} | {ya(r.A7)} | {p(r.purata, 2, True) if r.A6 == True else '–'} | "   # noqa: E712
                 f"{p(r.jual_awal) if r.A6 == True else '–'} | {pot} | {p(r.rugi15) if r.A6 == True else '–'} | "   # noqa: E712
                 f"{'E' if r.earnings_hadapan else ''} | {ya(r.struktur_lengkap)} | {ya(r.menepati_semua)} |")
    # --- Bahagian B
    S = E[E.id == 'SEMUA'].set_index(['prasyarat', 'varian'])
    pe = meta['peristiwa']
    jum = sum(pe.values())
    A += ['', '## 3. Tarikh earnings masa hadapan (`QF01`, `QF04`)', '',
          f'Peristiwa 8-K item 2.02 dalam kumpulan B: {jum:,}; **berjadual** (dalam ±{TOLERANSI_JADUAL} sesi daripada ramalan masa '
          f'lalu) {pe["berjadual"] / jum * 100:.0f} %, **luar jadual** {pe["luar_jadual"] / jum * 100:.0f} %, tiada sejarah '
          f'{pe["tiada_sejarah"] / jum * 100:.0f} %. Asas `terus` mana-mana hari: {meta["asas_terus"] * 100:.1f} %.', '',
          'Semua bar layak (tanpa pencetus): kesan prasyarat itu sendiri.', '',
          '| Prasyarat | Varian | % bar | `terus` % | rawak hari sama % | kelebihan (mata) |', '|---|---|---|---|---|---|']
    ket = {'A': 'A asal (tarikh sebenar)', 'J': 'J berjadual sahaja', 'L': 'L luar jadual / tiada sejarah', 'P': 'P ramalan masa lalu'}
    for (q, v), r in S.iterrows():
        A.append(f'| `{q}` | {ket[v]} | {p(r.bahagian_bar)} | {p(r.terus)} | {p(r.a_terus)} | {p(r.kl, 1, True)} |')
    F = E[E.id != 'SEMUA']
    A += ['', 'Setiap setup kedudukan akhir yang memakainya (masuk, henti, keluar, pegang minimum tidak berubah). "bertahan" = belian '
          f'≥ {MIN_BERTAHAN} DAN kelebihan `terus` > 0 dalam K1, K2 dan K3.', '',
          '| ID | ked. | pra | varian | belian | `terus` % | kelebihan | K1 | K2 | K3 | tangkap penuh % | purata % | rugi ≥ 8 % | bertahan |',
          '|' + '---|' * 14]
    for r in F.sort_values(['kedudukan', 'varian']).itertuples():
        if r.belian == 0 or r.terus != r.terus:
            A.append(f'| `{r.id}` | {r.kedudukan} | `{r.prasyarat}` | {r.varian} | 0 | – | – | – | – | – | – | – | – | ✗ |')
            continue
        A.append(f'| `{r.id}` | {r.kedudukan} | `{r.prasyarat}` | {r.varian} | {int(r.belian):,} | {p(r.terus)} | {p(r.kl, 1, True)} | '
                 f'{p(r.kl_K1, 1, True)} | {p(r.kl_K2, 1, True)} | {p(r.kl_K3, 1, True)} | {p(r.tp)} | {p(r.purata, 2, True)} | '
                 f'{p(r.rugi8)} | {ya(r.bertahan)} |')
    A += ['', '| Varian | setup | bertahan | median belian | median kelebihan (mata) | median purata % |', '|---|---|---|---|---|---|']
    for v in VARIAN:
        x = F[F.varian == v]
        if len(x):
            A.append(f'| {ket[v]} | {len(x)} | {int((x.bertahan == True).sum())} | {x.belian.median():.0f} | '   # noqa: E712
                     f'{p(x.kl.median(), 1, True)} | {p(x.purata.median(), 2, True)} |')
    # --- Bahagian C
    C = belah(M)
    A += ['', '## 4. Kebolehpercayaan pangkat (kelebihan `terus` pada dua belahan)', '',
          '| Belahan | setup | Spearman | setup positif pada kedua-dua | 10 teratas separuh 1: median di separuh 1 → separuh 2 | '
          '10 teratas separuh 2: median di separuh 2 → separuh 1 | median semua (separuh 1 / 2) |', '|---|---|---|---|---|---|---|']
    for nama_, t in (('s', "saham (md5('audit:' + ticker) genap / ganjil)"), ('t', 'tahun (genap / ganjil)')):
        c = C[nama_]
        A.append(f"| {t} | {c['n']} | {c['rho']:+.2f} | {c['positif_dua']} | {p(c['atas0_pada_0'], 1, True)} → "
                 f"{p(c['atas0_pada_1'], 1, True)} | {p(c['atas1_pada_1'], 1, True)} → {p(c['atas1_pada_0'], 1, True)} | "
                 f"{p(c['median_semua_0'], 1, True)} / {p(c['median_semua_1'], 1, True)} |")
    A += ['', f"Bacaan dikunci: Spearman belahan tahun {C['t']['rho']:+.2f} "
          + ('≤ 0.2 → SUSUNAN dalam `KEDUDUKAN_AKHIR` tidak bermakna; hanya "dipercayai" lawan "tidak" yang boleh dibaca.'
             if C['t']['rho'] <= 0.2 else '> 0.2 → susunan membawa sedikit maklumat; baca bersama penyusutan 10 teratas di atas.'), '']
    # --- Bahagian D
    kk = pd.read_csv(os.path.join(HASIL, 'KEDUDUKAN_AKHIR.csv'))
    mm = reg[['id', 'menang']].merge(kk[['id', 'menang']], on='id', suffixes=('_reg', '_akhir'))
    beza = (mm.menang_reg - mm.menang_akhir).abs()
    A += ['## 5. Semakan proses', '',
          f'- Lajur `menang` `registry_F.csv` / `KADAR_MENANG.md` (mekanik pusingan asal) lawan `KEDUDUKAN_AKHIR.csv` (pegang '
          f'minimum): beza mutlak median {beza.median() * 100:.1f} mata, terbesar {beza.max() * 100:.1f} mata '
          f'({int((beza > 0.03).sum())} setup melebihi 3 mata).',
          f'- Setup tidak dinilai di bawah kayu ukur akhir: {int((M.A6 != True).sum())} '   # noqa: E712
          f"({', '.join(f'`{i}`' for i in M[M.A6 != True].id)}).",   # noqa: E712
          f'- "Dipercayai" tetapi purata setiap dagangan ≤ 0: '
          + (', '.join(f'`{i}`' for i in T[T.A8 == False].id) or 'tiada') + '.',   # noqa: E712
          f'- Henti: {int(M.henti.isin(["G7"]).sum())} setup memakai 5×ATR14; rugi ≥ 15 % median '
          f'{p(D.rugi15.median())} % dagangan (terbesar {p(D.rugi15.max())} %, `{D.loc[D.rugi15.idxmax(), "id"]}`). Henti TIDAK '
          f'mengehadkan rugi apabila harga melompat turun semalaman: dagangan terburuk setiap setup median '
          f'{p(D.rugi_terburuk.median())} %, julat {p(D.rugi_terburuk.max())} % hingga {p(D.rugi_terburuk.min())} % '
          '(disemak: kejatuhan sebenar, cth. `IFRX` Jun 2019, `KOD` Feb 2022, `AMLX` Mac 2024; bukan ralat data).',
          '- Urutan pradaftar → hasil: pindaan (a)–(u) cawangan lama [di `main`: (a)–(q), (ac), (ad)] semuanya dikomit SEBELUM hasil masing-masing (disemak daripada sejarah '
          'komit, 13–14 Nov 2026); dua pengecualian dilabel dalam spec sendiri: (g) tambahan kohort post-hoc, (p) peraturan '
          'pegang minimum ditulis selepas analisis (o).',
          '- Kumpulan B ("saham tidak dilihat") sudah dipakai untuk MEMILIH: takrif "dipercayai" dan susunan kedudukan akhir (m), '
          'pendaftaran `F88`–`F95` ((n)-2). (Pilihan masuk, henti dan keluar dibuat pada kumpulan A sahaja.) Angka kumpulan B '
          'bagi setup teratas condong ke atas (lihat §4); ujian bersih yang tinggal hanyalah jejak hadapan.',
          '- Mekanik: jualan pada hari beli mustahil (henti hari beli dijual pada buka esok); had 20 sesi dan pegang minimum 3 sesi '
          'dikuatkuasakan dalam kernel (`cs_keluar7.sedia`) dan penjejak hadapan (`cs_hadapan.simulasi`), diuji '
          '(`ujian/test_carian_setup.py`).', '']
    with open(os.path.join(HASIL, 'AUDIT_F.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(A) + '\n')


if __name__ == '__main__':
    if sys.argv[1] != '--lapor':
        nilai(sys.argv[1])
    lapor()
