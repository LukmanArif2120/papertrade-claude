"""Carian setup — pusingan CS23 (SPEC pindaan 17 Nov 2026 (aj)): MARKAH 0-100 setiap setup F ikut matlamat pengguna + "Top 100".

Lima bahagian (berat dipersetujui pengguna): A menangkap saham yang naik 35 · B naik melebihi jatuh 15 · C boleh dipakai setiap
minggu 20 · D tahan uji 20 · E hasil dagangan 10. Semua ukuran dikira SEMULA dengan satu cara pada kumpulan B (saham yang carian
tidak lihat), isyarat beli dalam mod tanpa intai, stop loss 4xATR14 + cara pegang B. Setup yang serupa (belian bertindih >= 50 %
dengan setup bermarkah lebih tinggi) dibuang; 100 pertama = Top 100. Penyusunan atas data yang sudah dilihat: BUKAN bukti.
Guna: python3 cs_skor23.py ukur|lapor <kerja>. Jangan sunting keluaran secara manual."""
import json
import os
import pickle
import re
import sys
import time

import numpy as np
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_cari as cari  # noqa: E402
import cs_lapis as lapis  # noqa: E402

BERAT = {'A': 35, 'B': 15, 'C': 20, 'D': 20, 'E': 10}                # dikunci pindaan (aj)
# (markah penuh, mula, sasaran markah penuh) bagi kriteria berkadar
A1, A2A, A2B, A3 = (20, 0.0, 0.05), (5, 0.0, 0.08), (5, 0.0, 0.04), (5, 0.0, 0.03)
B1, B2 = (10, 0.0, 0.04), (5, 0.0, 0.05)
C1 = (20, 0.25, 0.80)
D1 = (2, 2, 4)                                                       # K1, K2, K3 > 0
D2, D2_MIN_TAHUN = (6, 0.50, 0.85), 8
D3A, D3B, BAKI_MIN, ADIK_MIN_BIL, ADIK_BAHAGIAN = 3, 3, 0.01, 3, 0.60
E1, E2 = (5, 0.0, 0.03), (5, 0.0, 0.015)
MIN_BELIAN, MIN_TAHUN = 300, 10
JACCARD, N_TOP = 0.50, 100
RASMI = 'Setiap minggu'                                               # senarai kerja rasmi (keputusan pengguna 17 Nov 2026, pindaan (aj))
TAMBAHAN = 'Musim laporan kewangan'                                   # tambahan bermusim
MINGGU_KERAP = 0.80
GUNA = ('Setiap minggu', 'Musim laporan kewangan', 'Keadaan tertentu', 'Lain-lain')
PUS = 'CS23'
BHG = ('mA', 'mB', 'mC', 'mD', 'mE')
KRIT = ('A1', 'A2', 'A3', 'B1', 'B2', 'C1', 'D1', 'D2', 'D3', 'E1', 'E2')
F_ = lambda kerja: os.path.join(kerja, 'cs23_ukur.pkl')
HASIL = os.path.join(SINI, 'hasil', PUS)
_LAIN = re.compile(r'earnings|Nov-Apr|Mei-Okt|Januari|hari pertama bulan')


def lin(x, a, b):
    """0 jika x <= a, 1 jika x >= b, berkadar di antaranya; NaN -> 0."""
    if x is None or x != x:
        return 0.0
    return float(min(1.0, max(0.0, (x - a) / (b - a))))


def markah(u):
    """Markah setiap kriteria, setiap bahagian dan jumlah bagi satu setup. u: dict ukuran (pecahan, bukan peratus):
    kl_terus, kl_m5, kl_m10, kl_c10, arah, kl_rugi15, minggu, kl_K1..kl_K3, thn_pos, thn_bil, kl_baki, adik_bil, adik_pos,
    kl_menang, kl_purata. Ukuran yang tiada (NaN) = 0 markah bagi kriteria itu."""
    g = lambda k: u.get(k, float('nan'))
    pos = lambda v: v == v and v > 0
    m = {'A1': A1[0] * lin(g('kl_terus'), *A1[1:]),
         'A2': A2A[0] * lin(g('kl_m5'), *A2A[1:]) + A2B[0] * lin(g('kl_m10'), *A2B[1:]),
         'A3': A3[0] * lin(g('kl_c10'), *A3[1:]),
         'B1': B1[0] * lin(g('arah'), *B1[1:]),
         'B2': B2[0] * (1.0 - lin(g('kl_rugi15'), *B2[1:])) if g('kl_rugi15') == g('kl_rugi15') else 0.0,
         'C1': C1[0] * lin(g('minggu'), *C1[1:]),
         'D1': sum(w for w, k in zip(D1, ('kl_K1', 'kl_K2', 'kl_K3')) if pos(g(k)))}
    tb = g('thn_bil')
    m['D2'] = D2[0] * lin(g('thn_pos') / tb, *D2[1:]) if tb == tb and tb >= D2_MIN_TAHUN else 0.0
    ab, ap = g('adik_bil'), g('adik_pos')
    m['D3'] = (D3A if g('kl_baki') == g('kl_baki') and g('kl_baki') >= BAKI_MIN else 0) + \
              (D3B if ab == ab and ab >= ADIK_MIN_BIL and ap >= ADIK_BAHAGIAN * ab else 0)
    m['E1'] = E1[0] * lin(g('kl_menang'), *E1[1:])
    m['E2'] = E2[0] * lin(g('kl_purata'), *E2[1:])
    m['mA'], m['mB'], m['mC'] = m['A1'] + m['A2'] + m['A3'], m['B1'] + m['B2'], m['C1']
    m['mD'], m['mE'] = m['D1'] + m['D2'] + m['D3'], m['E1'] + m['E2']
    m['markah'] = round(sum(m[k] for k in BHG), 1)
    return m


def kegunaan(prasyarat, minggu):
    """Label "Kegunaan bila?" (indeks GUNA) daripada teks prasyarat dan bahagian minggu yang ada belian (kumpulan B)."""
    p = prasyarat if isinstance(prasyarat, str) else ''
    if 'earnings dalam 1-' in p:
        return 1
    if _LAIN.search(p):
        return 3
    return 0 if (minggu == minggu and minggu >= MINGGU_KERAP) else 2


# ---------- senarai setup dan ukuran ----------
def senarai():
    """Setiap baris senarai dashboard: 2,001 setup senarai utama (CS13) + kod sepanjang tahun CS20, dengan takrif terurai."""
    import cs_cs07 as c7
    import cs_lapor as lapor
    import cs_portfolio6 as p6
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('').set_index('id')
    U = pd.read_csv(os.path.join(SINI, 'hasil', 'CS13', 'senarai_utama.csv')).fillna({'prasyarat': '', 'penapis': ''}).set_index('id')
    M = pd.read_csv(os.path.join(SINI, 'hasil', 'CS20', 'mingguan.csv')).fillna({'prasyarat': '', 'penapis': ''}).set_index('id')
    kq1, kq2 = [x[:4] for x in lapis.PASARAN], [x[:4] for x in lapis.KUMPULAN]
    out = []
    for kump, T in (('senarai utama', U), ('sepanjang tahun CS20', M)):
        for i, u in T.iterrows():
            r = reg.loc[i]
            b = dict(id=i, kumpulan=kump, nama=str(u['nama']), prasyarat=str(u['prasyarat']), penapis=str(u['penapis']), pencetus='', q1=-1, q2=-1,
                     f1=-1, f2=-1)
            try:
                if r.pusingan in ('CS13', 'CS20'):
                    t = r.takrif.split('|')
                    kod = [x for x in t[4].split('+') if x] if len(t) > 4 else []
                    fs = [int(x[1:]) - 1 for x in t[1].split('+') if x] + [-1, -1]
                    b.update(pencetus=t[0], q1=next((kq1.index(x) for x in kod if x in kq1), -1), q2=next((kq2.index(x) for x in kod if x in kq2), -1),
                             f1=fs[0], f2=fs[1])
                else:
                    d = c7.dari_takrif7(r.takrif) if r.pusingan == 'CS07' else p6.dari_takrif5(r.takrif)
                    b.update(pencetus=d['pencetus'], q1=int(d['q1']), q2=int(d['q2']), f1=int(d['f1']), f2=int(d['f2']))
            except Exception:
                pass
            out.append(b)
    return out


def ukur(kerja):
    """Kira semula setiap ukuran setiap setup pada kumpulan B (mod tanpa intai) -> cs23_ukur.pkl {T, beli, n_bar}."""
    import cs_audit19 as a19
    import cs_capai21 as c21
    import cs_mingguan20 as m20
    import cs_solid16 as s16
    t0 = time.time()
    K = s16.Konteks(kerja)
    pan = K.pan
    df, _, A19 = a19.bina_bebas()
    assert len(pan['c']) == len(df) and (pan['tarikh'] == A19['tarikh']).all()
    del df
    Lab, As, SK, S63 = c21.asas21(pan)
    M = m20.minggu(pan['hari_unik'], 'B')
    cari.log(f'CS23 ukur: konteks siap · {time.time() - t0:.0f}s')
    S = senarai()
    baris, beli = [], {}
    for j, x in enumerate(S, 1):
        b = {k: x[k] for k in ('id', 'kumpulan', 'nama', 'prasyarat', 'penapis', 'pencetus')}
        ev0 = K.EV.get(x['pencetus'])
        if ev0 is None:
            b.update(ada=False, n=0, tahun=0)
            baris.append(b)
            continue
        ev = np.ascontiguousarray(ev0[K.topeng(ev0, x['q1'], x['q2'], x['f1'], x['f2'])], dtype=np.int64)
        d, e = K.ukur(ev)
        b.update(ada=True, n=d['n'], tahun=d['tahun'])
        if d['n']:
            da = a19.ukur(A19, ev[A19['sah'][ev]])[0]
            d2 = c21.ukur21(pan, Lab, As, SK, S63, ev)
            mg = m20.kekerapan(M, pan['hari'][e])[0]
            ab, ap = K.adik(x['pencetus'], x['q1'], x['q2'], x['f1'], x['f2'])
            g = lambda dd, k: float(dd.get(k, float('nan')))
            b.update(terus=d['terus'], a_terus=d['a_terus'], kl_terus=d['kl_terus'], m5=d['m5'], a_m5=d['a_m5'], kl_m5=d['kl_m5'], m10=d['m10'],
                     a_m10=d['a_m10'], kl_m10=d['kl_m10'], kl_K1=d['kl_K1'], kl_K2=d['kl_K2'], kl_K3=d['kl_K3'], n_K3=d['n_K3'], thn_bil=d['thn_bil'],
                     thn_pos=d['thn_pos'], kl_baki=d['kl_baki'], adik_bil=ab, adik_pos=ap, minggu=mg,
                     c10=g(d2, 'c10'), a_c10=g(d2, 'a_c10'), kl_c10=g(d2, 'kl_c10'), j8=g(d2, 'j8'), a_j8=g(d2, 'a_j8'),
                     j5=g(da, 'j5'), a_j5=g(da, 'a_j5'), arah=g(da, 'arah'), menang_B=g(da, 'menang_B'), a_menang_B=g(da, 'a_menang_B'),
                     purata_B=g(da, 'purata_B'), a_purata_B=g(da, 'a_purata_B'), rugi15_B=g(da, 'rugi15_B'), a_rugi15_B=g(da, 'a_rugi15_B'))
            b.update(kl_menang=b['menang_B'] - b['a_menang_B'], kl_purata=b['purata_B'] - b['a_purata_B'], kl_rugi15=b['rugi15_B'] - b['a_rugi15_B'])
            beli[x['id']] = e.astype(np.int32)
        baris.append(b)
        if j % 300 == 0:
            cari.log(f'  CS23 ukur {j}/{len(S)} · {time.time() - t0:.0f}s')
    T = pd.DataFrame(baris)
    pickle.dump({'T': T, 'beli': beli, 'n_bar': int(len(pan['c']))}, open(F_(kerja), 'wb'), protocol=4)
    cari.log(f"CS23 ukur: {len(T)} setup · isyarat ada {int(T.ada.sum())} · {time.time() - t0:.0f}s")
    return T


# ---------- markah, buang yang serupa, Top 100 ----------
def nilai(T):
    """Tambah lajur markah, syarat wajib dan label "Kegunaan bila?" kepada jadual ukuran."""
    T = T.copy()
    T['dinilai'] = T.ada.astype(bool) & (T.n >= MIN_BELIAN) & (T.tahun >= MIN_TAHUN)
    T['sebab'] = np.where(~T.ada.astype(bool), 'isyarat tidak dapat dijana', np.where(T.dinilai, '', 'belian tidak cukup'))
    M = pd.DataFrame([markah(r) if r.get('dinilai') else {} for r in T.to_dict('records')], index=T.index)
    for k in KRIT + BHG + ('markah',):
        T[k] = M[k] if k in M else np.nan
    T['kegunaan'] = [GUNA[kegunaan(p, m)] for p, m in zip(T.prasyarat, T.get('minggu', pd.Series(np.nan, index=T.index)))]
    return T


def buang_serupa(T, beli, n_bar):
    """Ikut susunan markah: 'serupa' jika Jaccard belian (kumpulan B) >= JACCARD dengan setup bermarkah lebih tinggi yang sudah
    disimpan. Pulangkan (susunan id yang dinilai, dict id -> wakil ('' = disimpan))."""
    from scipy import sparse
    D = T[T.dinilai].sort_values(['markah', 'kl_terus', 'id'], ascending=[False, False, True], kind='stable')
    ids = D.id.tolist()
    if not ids:
        return ids, {}
    r_, c_ = [], []
    for i, idn in enumerate(ids):
        x = beli[idn].astype(np.int64)
        r_.append(np.full(len(x), i, np.int64))
        c_.append(x)
    Mx = sparse.csr_matrix((np.ones(sum(len(x) for x in c_), np.int32), (np.concatenate(r_), np.concatenate(c_))), shape=(len(ids), n_bar))
    X = (Mx @ Mx.T).tocsr()
    saiz = np.asarray(Mx.sum(1)).ravel()
    simpan = np.zeros(len(ids), bool)
    out = {}
    for i in range(len(ids)):
        a, b = X.indptr[i], X.indptr[i + 1]
        j, x = X.indices[a:b], X.data[a:b]
        m = simpan[j] & (j < i)
        jac = x[m] / (saiz[i] + saiz[j[m]] - x[m])
        if len(jac) and jac.max() >= JACCARD:
            out[ids[i]] = ids[int(j[m][int(np.argmax(jac))])]
        else:
            out[ids[i]] = ''
            simpan[i] = True
    return ids, out


def semua(kerja):
    Z = pickle.load(open(F_(kerja), 'rb'))
    T = nilai(Z['T'])
    ids, sr = buang_serupa(T, Z['beli'], Z['n_bar'])
    T['serupa_dengan'] = [sr.get(i, '') for i in T.id]
    T['disimpan'] = T.dinilai & (T.serupa_dengan == '')
    ked = {i: k for k, i in enumerate([i for i in ids if sr[i] == ''], 1)}
    T['kedudukan'] = [ked.get(i, 0) for i in T.id]
    T['top'] = np.where((T.kedudukan > 0) & (T.kedudukan <= N_TOP), T.kedudukan, 0)
    # tambahan (aj) selepas hasil: kedudukan dalam kumpulan "Kegunaan bila?" masing-masing (markah sama; paparan sahaja)
    kg = np.zeros(len(T), int)
    for g in GUNA:
        m = ((T.kedudukan > 0) & (T.kegunaan == g)).to_numpy()
        kg[m] = T.kedudukan[m].rank(method='first').astype(int).to_numpy()
    T['kedudukan_guna'] = kg
    T['top_guna'] = np.where((kg > 0) & (kg <= N_TOP), kg, 0)
    return T.sort_values(['kedudukan', 'markah'], ascending=[True, False], kind='stable').reset_index(drop=True)


def _ringkas(X):
    """Nilai tengah satu senarai (bagi laporan dan dashboard)."""
    r4 = lambda x: None if x != x else round(float(x), 4)
    md = lambda k: r4(X[k].median())
    return dict(n=int(len(X)), markah_maks=r4(X.markah.max()), markah_tengah=md('markah'), markah_min=r4(X.markah.min()),
                terus=md('terus'), a_terus=md('a_terus'), m5=md('m5'), a_m5=md('a_m5'), j5=md('j5'), a_j5=md('a_j5'),
                c10=md('c10'), a_c10=md('a_c10'), menang=md('menang_B'), a_menang=md('a_menang_B'), purata=md('purata_B'),
                a_purata=md('a_purata_B'), minggu=md('minggu'), k3=md('kl_K3'), n_belian=md('n'),
                bahagian={k: r4(X[k].median()) for k in BHG})


def lapor_(kerja):
    import cs_lapor as lapor
    T = semua(kerja)
    os.makedirs(HASIL, exist_ok=True)
    lajur = ['id', 'kumpulan', 'kegunaan', 'dinilai', 'sebab', 'markah', 'kedudukan', 'top', 'kedudukan_guna', 'top_guna', 'serupa_dengan'] + list(BHG) + list(KRIT) + \
        ['nama', 'prasyarat', 'penapis', 'n', 'tahun', 'minggu', 'terus', 'a_terus', 'kl_terus', 'kl_K1', 'kl_K2', 'kl_K3', 'm5', 'a_m5', 'kl_m5', 'm10',
         'a_m10', 'kl_m10', 'c10', 'a_c10', 'kl_c10', 'j5', 'a_j5', 'arah', 'rugi15_B', 'a_rugi15_B', 'kl_rugi15', 'thn_pos', 'thn_bil', 'kl_baki',
         'adik_bil', 'adik_pos', 'menang_B', 'a_menang_B', 'kl_menang', 'purata_B', 'a_purata_B', 'kl_purata']
    X = T.sort_values(['dinilai', 'markah', 'id'], ascending=[False, False, True], kind='stable')
    X.reindex(columns=lajur).to_csv(os.path.join(HASIL, 'skor.csv.gz'), index=False, float_format='%.5f')
    D, S, P = T[T.dinilai], T[T.disimpan], T[T.top > 0].sort_values('top')
    r4 = lambda x: None if x != x else round(float(x), 4)
    B = dict(n=int(len(T)), dinilai=int(len(D)), tidak_dijana=int((T.sebab == 'isyarat tidak dapat dijana').sum()),
             belian_tidak_cukup=int((T.sebab == 'belian tidak cukup').sum()), serupa=int((D.serupa_dengan != '').sum()), disimpan=int(len(S)),
             n_top=int(len(P)), berat=BERAT, markah_maks=r4(D.markah.max()), markah_tengah=r4(D.markah.median()),
             top_min=r4(P.markah.min()), top_tengah=r4(P.markah.median()),
             top_kegunaan={k: int((P.kegunaan == k).sum()) for k in GUNA}, top_kumpulan=P.kumpulan.value_counts().to_dict(),
             semua_kegunaan={k: int((D.kegunaan == k).sum()) for k in GUNA},
             tengah_bahagian={g_: {k: r4(X_[k].median()) for k in BHG} for g_, X_ in (('top', P), ('dinilai', D))},
             tengah_kegunaan={k: r4(D[D.kegunaan == k].markah.median()) for k in GUNA if (D.kegunaan == k).any()},
             disimpan_kegunaan={k: int((S.kegunaan == k).sum()) for k in GUNA}, senarai_rasmi=RASMI, senarai_tambahan=TAMBAHAN,
             top_guna={k: _ringkas(T[(T.kegunaan == k) & (T.top_guna > 0)]) for k in GUNA if ((T.kegunaan == k) & (T.top_guna > 0)).any()})
    json.dump(B, open(os.path.join(HASIL, 'bacaan.json'), 'w'), indent=1, sort_keys=True, ensure_ascii=False)
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    p = lambda x, k=0, t=False: '–' if x is None or x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')
    tx = lambda s: s if isinstance(s, str) and s.strip() else '–'
    A = ['# CS23: markah 0–100 setiap setup F ikut matlamat pengguna, dan Top 100 (backtest; BUKAN bukti)', '', status, '',
         'Dijana `kajian/carian_setup/cs_skor23.py`. Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 17 Nov 2026 (aj). '
         '**Jangan sunting secara manual.** Markah ialah PENYUSUNAN mengikut kehendak pengguna atas data yang sudah dilihat; ia bukan ujian.', '',
         f'**Senarai kerja rasmi (keputusan pengguna 17 Nov 2026): Top {N_TOP} "{RASMI}" — §5.** Top {N_TOP} "{TAMBAHAN}" (§6) ialah tambahan '
         f'bermusim; Top {N_TOP} keseluruhan (§4) kekal rekod sahaja. Ini bukan keputusan papertrade.', '',
         '## 1. Cara markah', '',
         f"- **A. Menangkap saham yang naik — {BERAT['A']}:** tangkap (20; penuh pada +5 mata lawan saham rawak), naik ≥ 5 % dan ≥ 10 % seminggu "
         '(10; penuh pada +8 dan +4 mata), mencapai +10 % sebelum jatuh 8 % dalam 3 bulan (5; penuh pada +3 mata).',
         f"- **B. Naik melebihi jatuh — {BERAT['B']}:** tambahan naik tolak tambahan jatuh (10; penuh pada +4 mata), rugi ≥ 15 % tidak lebih kerap "
         'daripada saham rawak (5; kosong pada +5 mata).',
         f"- **C. Boleh dipakai setiap minggu — {BERAT['C']}:** bahagian minggu yang ada belian, diukur pada separuh saham (kosong pada 25 %, penuh "
         'pada 80 %).',
         f"- **D. Tahan uji — {BERAT['D']}:** lebih baik daripada rawak dalam 2010–19 (2), 2020–24 (2), 2025–26 (4); bahagian tahun yang lebih baik "
         '(6; kosong pada 50 %, penuh pada 85 %); masih baik selepas 10 hari terbaik dibuang (3) dan bila parameter diubah sedikit (3).',
         f"- **E. Hasil dagangan — {BERAT['E']}:** kadar menang (5; penuh pada +3 mata) dan purata setiap dagangan (5; penuh pada +1.5 %), "
         'lawan saham rawak yang dibeli hari sama dan dipegang dengan cara sama.',
         '- Semua ukuran dikira semula pada saham yang carian tidak lihat, dengan isyarat beli yang tidak mengintai harga esok, stop loss 4×ATR14 '
         'dan cara pegang B. Sama dengan saham rawak = 0 markah bagi kriteria itu.', '',
         '## 2. Berapa yang dinilai', '',
         f"- Setup dalam senarai: {B['n']:,}. Dinilai: **{B['dinilai']:,}**; tidak dinilai: {B['tidak_dijana']} (isyarat varian lama tidak dapat "
         f"dijana semula) + {B['belian_tidak_cukup']} (kurang 300 belian atau 10 tahun dalam mod tanpa intai).",
         f"- Serupa dengan setup bermarkah lebih tinggi (belian bertindih ≥ {JACCARD:.0%}): {B['serupa']:,} — dibuang. Setup berbeza: "
         f"**{B['disimpan']:,}**; {B['n_top']} teratas = Top 100.",
         f"- Markah tertinggi {B['markah_maks']:.1f}; nilai tengah semua yang dinilai {B['markah_tengah']:.1f}; Top 100: paling rendah "
         f"{B['top_min']:.1f}, nilai tengah {B['top_tengah']:.1f}.",
         '- Top 100 ikut "Kegunaan bila?": ' + ' · '.join(f"{k} {v}" for k, v in B['top_kegunaan'].items()) + '.',
         '- Nilai tengah markah ikut kegunaan (semua yang dinilai): ' + ' · '.join(f"{k} {v:.1f}" for k, v in B['tengah_kegunaan'].items()) + '.', '',
         '## 3. Nilai tengah markah setiap bahagian', '',
         '| Kumpulan | A (35) | B (15) | C (20) | D (20) | E (10) |', '|---' * 6 + '|']
    for nm, X_ in (('Top 100', P), ('Semua yang dinilai', D)) + tuple((k, D[D.kegunaan == k]) for k in GUNA):
        if len(X_):
            A.append(f"| {nm} ({len(X_):,}) | " + ' | '.join(f'{X_[k].median():.1f}' for k in BHG) + ' |')
    A += ['', '## 4. Top 100', '',
          '| # | ID | **Markah** | A · B · C · D · E | Kegunaan bila? | Prasyarat | Isyarat beli | Penapis saham | Tangkap % (rawak) | Minggu ada belian | '
          'Menang % (rawak) | Purata % (rawak) | 2025–26 |', '|---' * 13 + '|']
    for r in P.itertuples():
        A.append(f"| {r.top} | `{r.id}` | **{r.markah:.1f}** | {r.mA:.0f} · {r.mB:.0f} · {r.mC:.0f} · {r.mD:.0f} · {r.mE:.0f} | {r.kegunaan} | "
                 f"{tx(r.prasyarat)} | {r.nama} | {tx(r.penapis)} | {p(r.terus, 1)} ({p(r.a_terus, 1)}) | {p(r.minggu)} % | {p(r.menang_B)} "
                 f"({p(r.a_menang_B)}) | {p(r.purata_B, 1, True)} ({p(r.a_purata_B, 1, True)}) | {p(r.kl_K3, 1, True)} |")
    kepala = ['| # | ID | **Markah** | A · B · C · D · E | Prasyarat | Isyarat beli | Penapis saham | Tangkap % (rawak) | Minggu ada belian | '
              'Menang % (rawak) | Purata % (rawak) | 2025–26 | # keseluruhan |', '|---' * 13 + '|']
    for no, g in ((5, 'Setiap minggu'), (6, 'Musim laporan kewangan')):
        G = T[(T.kegunaan == g) & (T.top_guna > 0)].sort_values('top_guna')
        if not len(G):
            continue
        z = B['top_guna'][g]
        A += ['', f'## {no}. Top {len(G)} "{g}" (markah yang sama, dalam kumpulan itu sahaja)' +
              (' — SENARAI KERJA RASMI' if g == RASMI else ' — tambahan bermusim' if g == TAMBAHAN else ''), '',
              f"Tambahan selepas hasil dilihat (paparan sahaja, lihat pindaan (aj)). Setup berbeza dalam kumpulan ini: "
              f"{B['disimpan_kegunaan'][g]:,}. Markah {z['markah_maks']:.1f} hingga {z['markah_min']:.1f} (nilai tengah {z['markah_tengah']:.1f}). "
              f"Nilai tengah: tangkap {p(z['terus'], 1)} lawan saham rawak {p(z['a_terus'], 1)}; naik ≥ 5 % seminggu {p(z['m5'], 1)} lawan "
              f"{p(z['a_m5'], 1)}; jatuh ≥ 5 % {p(z['j5'], 1)} lawan {p(z['a_j5'], 1)}; menang {p(z['menang'], 1)} % lawan {p(z['a_menang'], 1)} %; "
              f"purata {p(z['purata'], 1, True)} % lawan {p(z['a_purata'], 1, True)} %; minggu ada belian {p(z['minggu'])} %.", ''] + kepala
        for r in G.itertuples():
            A.append(f"| {r.top_guna} | `{r.id}` | **{r.markah:.1f}** | {r.mA:.0f} · {r.mB:.0f} · {r.mC:.0f} · {r.mD:.0f} · {r.mE:.0f} | "
                     f"{tx(r.prasyarat)} | {r.nama} | {tx(r.penapis)} | {p(r.terus, 1)} ({p(r.a_terus, 1)}) | {p(r.minggu)} % | {p(r.menang_B)} "
                     f"({p(r.a_menang_B)}) | {p(r.purata_B, 1, True)} ({p(r.a_purata_B, 1, True)}) | {p(r.kl_K3, 1, True)} | {r.kedudukan} |")
    A += ['', '## 7. Kaveat', '',
          '- Jangkaan yang ditulis dahulu salah pada dua perkara: markah tertinggi dijangka 55–70, dan Top 100 dijangka bercampur. '
          'Top 100 keseluruhan hampir semuanya setup laporan kewangan kerana bahagian C hanya 20 markah.',
          '- Berat dan sasaran markah penuh dipilih selepas melihat hasil; markah menyusun, ia tidak membuktikan apa-apa. Beza beberapa markah '
          'antara dua setup tidak bermakna (kedudukan tidak stabil antara tempoh).',
          '- "Minggu ada belian" diukur pada separuh saham; pada semua saham ia lebih tinggi.',
          '- Angka di sini dikira semula dalam mod tanpa intai dan boleh berbeza sedikit daripada angka berdaftar di dashboard.',
          '- Tiada saham delist dalam data. Backtest sahaja; Top 100 BUKAN keputusan papertrade atau wang sebenar.', '',
          'Senarai penuh dengan markah setiap kriteria: `skor.csv.gz`.', '']
    open(os.path.join(HASIL, 'TOP100.md'), 'w', encoding='utf-8').write('\n'.join(A))
    cari.log(f"CS23 lapor: dinilai {B['dinilai']}, serupa {B['serupa']}, disimpan {B['disimpan']}, top {B['n_top']}; markah maks {B['markah_maks']}, "
             f"top min {B['top_min']}; top ikut kegunaan {B['top_kegunaan']}; disimpan ikut kegunaan {B['disimpan_kegunaan']}")
    return T, B


if __name__ == '__main__':
    cmd, kerja = sys.argv[1], sys.argv[2]
    if cmd == 'ukur':
        ukur(kerja)
    elif cmd == 'lapor':
        lapor_(kerja)
    else:
        raise SystemExit(f'arahan tidak dikenali: {cmd}')
