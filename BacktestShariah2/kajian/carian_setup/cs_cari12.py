"""Carian setup — pusingan CS12 (SPEC pindaan 15 Nov 2026 (u)): carian baharu dipangkatkan ikut ukuran longgar `naik`.

Sasaran = label `naik` (cs_semak11): selepas 4 minggu harga >= 2 % di atas harga beli, masih di atas purata 20 harinya, dan
tidak pernah tutup 10 % di bawah harga beli. Ruang masuk = enjin CS05 (prasyarat pasaran x prasyarat syarikat x penapis saham)
bagi setiap pencetus; skor pada kumpulan A; semakan pada kumpulan B dengan kawalan rawak. Setup lengkap setiap calon: stop
loss 4xATR14 dan cara pegang B pilihan pengguna (pegang hingga tutup di bawah purata 20 hari selepas hari ke-20).
Guna: python3 cs_cari12.py skor|calon|kunci|lapor <kerja>. Jangan sunting keluaran secara manual."""
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
import cs_keluar7 as k7  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_semak11 as s11  # noqa: E402
import cs_tala7 as t7  # noqa: E402

N_ATAS, N_KAWALAN, BENIH_KAWALAN, N_BACA = 5, 300, 20261115, 100     # dikunci pindaan (u)
S_HENTI = k7.HENTI.index('4xATR14')
CARA_B = s11.CARA.index('P-MA20')
BAHAGIAN = ('asal', 'K', 'M1', 'M2')
PUS = 'CS12'


def v_naik(pan):
    """V[bar] = (naik, asas hari sama x tercile ATR %, asas era x tercile) bagi bar layak (bentuk yang diterima skor_ev)."""
    sah = np.flatnonzero(pan['sah'])
    lb = s11.label11(sah, pan['o'], pan['l'], pan['c'])[:, 2].astype(np.float64)
    hari = pan['hari'][sah]
    pct = pd.Series(pan['atr'][sah] / pan['c'][sah]).groupby(hari).rank(pct=True).to_numpy()
    terc = np.minimum((pct * 3).astype(np.int64), 2)
    V = np.zeros((len(pan['c']), 3))
    V[sah, 0] = lb
    for a, g in ((1, hari * 3 + terc), (2, pan['tempoh'][sah].astype(np.int64) * 3 + terc)):
        V[sah, a] = (np.bincount(g, lb) / np.maximum(np.bincount(g), 1))[g]
    return V


def semua_pencetus(kerja, set_):
    ev = {}
    for bhg in BAHAGIAN:
        try:
            ev.update(t7.semua_ev(kerja, set_, bhg))
        except FileNotFoundError:
            pass
    return ev


def skor(kerja):
    """Skor setiap pencetus pada kumpulan A (sasaran `naik`) -> cs12_skor.pkl."""
    f = os.path.join(kerja, 'cs12_skor.pkl')
    siap = pickle.load(open(f, 'rb')) if os.path.exists(f) else {}
    pan = cari.panel(kerja, 'A')
    ev = semua_pencetus(kerja, 'A')
    V = v_naik(pan)
    cari.log(f"CS12 skor: {sum(1 for n in ev if n not in siap)} pencetus; asas naik {V[pan['sah'], 0].mean() * 100:.1f}%")
    siap = t7.skor_ev(kerja, ev, siap, f, V=V)
    pickle.dump(siap, open(f, 'wb'), protocol=4)
    cari.log(f"CS12 skor siap: {sum(1 for r in siap.values() if r.get('cukup'))} cukup isyarat daripada {len(siap)}")
    return siap


def calon(kerja):
    """Calon = sehingga N_ATAS peraturan masuk berskor > 0 bagi setiap pencetus; kawalan = N_KAWALAN peraturan rawak dengan
    n >= 100 setiap era pada A. -> cs12_calon.pkl"""
    S = pickle.load(open(os.path.join(kerja, 'cs12_skor.pkl'), 'rb'))
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
    T.insert(0, 'id', [f'L{i + 1:04d}' for i in range(len(T))])
    pan = cari.panel(kerja, 'A')
    L = lapis.muat(kerja, 'A')
    Lr = (L['L1'], L['L2'])
    EV = semua_pencetus(kerja, 'A')
    cukup = sorted(n for n, r in S.items() if r.get('cukup'))
    rng = np.random.default_rng(BENIH_KAWALAN)
    K, cuba = [], 0
    while len(K) < N_KAWALAN and cuba < 200000:
        cuba += 1
        nama = cukup[int(rng.integers(len(cukup)))]
        q = int(rng.integers(c5.NQ))
        ci = int(rng.integers(c5.NC))
        q1, q2, f1, f2 = (int(x[0]) for x in c5.nyah(np.asarray([q * c5.NC + ci])))
        if q == 0 and ci == 0:
            continue
        ev = EV[nama]
        e = ev[c5.topeng(pan, Lr, ev, q1, q2, f1, f2)]
        tp = pan['tempoh'][e]
        if min(int((tp == 0).sum()), int((tp == 1).sum())) < c5.N_MIN:
            continue
        K.append(dict(id=f'R{len(K) + 1:03d}', pencetus=nama, induk=t7.induk(nama), ke=0, skor=np.nan, q1=q1, q2=q2, f1=f1, f2=f2,
                      skor0=np.nan, n_E1=int((tp == 0).sum()), n_E2=int((tp == 1).sum())))
    out = {'calon': T, 'kawalan': pd.DataFrame(K), 'n_pencetus': len(S), 'n_cukup': len(cukup), 'cuba_kawalan': cuba}
    pickle.dump(out, open(os.path.join(kerja, 'cs12_calon.pkl'), 'wb'), protocol=4)
    cari.log(f"CS12 calon: {len(T)} calon berskor > 0 daripada {len(cukup)} pencetus cukup isyarat ({T.pencetus.nunique()} pencetus berbeza); "
             f"kawalan rawak {len(K)} (dicuba {cuba})")
    return out


def _nilai(pan, Lab, As, Bt, Lr, EV, sh, r):
    """Statistik satu peraturan masuk pada satu set: tangkapan (satu posisi, jual hari ke-20) + cara pegang (semua isyarat)."""
    ev = EV[r.pencetus]
    ev = ev[c5.topeng(pan, Lr, ev, r.q1, r.q2, r.f1, r.f2)]
    d, e = s11.ukur_tangkap(pan, Lab, As, ev, S_HENTI)
    p = s11.ukur_pegang(pan, Lab, Bt, ev, S_HENTI)
    beli = set(zip(pan['ticker'][pan['tid'][e]][sh[pan['tid'][e]]].tolist(), pan['tarikh'][e + 1][sh[pan['tid'][e]]].tolist()))
    return d, p, beli


def kunci(kerja):
    """Nilai setiap calon dan setiap kawalan pada kumpulan B (dan kira belian Shariah pada A + B) -> cs12_kunci.pkl."""
    import cs_lapor as lapor
    C = pickle.load(open(os.path.join(kerja, 'cs12_calon.pkl'), 'rb'))
    semua = pd.concat([C['calon'], C['kawalan']], ignore_index=True)
    shar = set(open(os.path.join(lapor.BS2, 'data', 'harga', 'univ.txt')).read().split())
    param = t7.param_semua(kerja)
    out = {i: {} for i in semua.id}
    t0 = time.time()
    for set_ in ('B', 'A'):
        pan = cari.panel(kerja, set_)
        L = lapis.muat(kerja, set_)
        Lr = (L['L1'], L['L2'])
        EV = semua_pencetus(kerja, set_)
        Lab, As = s11.asas(pan)
        Bt = s11.siri_trend(pan)
        sh = np.asarray([t in shar for t in pan['ticker']])
        for k, r in enumerate(semua.itertuples(), 1):
            d, p, beli = _nilai(pan, Lab, As, Bt, Lr, EV, sh, r)
            o = out[r.id]
            o['beli_' + set_] = beli
            if set_ == 'B':
                o.update(d=d, p=p, nama=t7.nama7(r.pencetus, param),
                         prasyarat=c5.buang_kod(c5.tk_pra(r.q1, r.q2)).replace(' DAN ', ' + ').replace('tiada', ''),
                         penapis=c5.buang_kod(c5.tk_pen(r.f1, r.f2)).replace(' DAN ', ' + ').replace('tiada', ''))
            if k % 500 == 0:
                cari.log(f'  CS12 kunci {set_} {k}/{len(semua)} · {time.time() - t0:.0f}s')
    pickle.dump(out, open(os.path.join(kerja, 'cs12_kunci.pkl'), 'wb'), protocol=4)
    cari.log(f'CS12 kunci: {len(out)} peraturan · {time.time() - t0:.0f}s')
    return out


def _teks(fn, a, b):
    """Teks prasyarat / penapis tanpa kod; '' jika tiada (prasyarat "tiada earnings ..." dikekalkan sepenuhnya)."""
    return '' if a < 0 and b < 0 else c5.buang_kod(fn(int(a), int(b))).replace(' DAN ', ' + ')


def jadual(C, K):
    """Satu baris setiap calon dan setiap kawalan dengan angka kumpulan B."""
    baris = []
    for nm, T in (('calon', C['calon']), ('kawalan', C['kawalan'])):
        for r in T.itertuples():
            o = K[r.id]
            d, p = o['d'], o['p']
            kl = [d[f'kl_naik_K{j}'] for j in (1, 2, 3)]
            lulus = bool(d['n'] >= s11.MIN_BELIAN and d['tahun'] >= s11.MIN_TAHUN and all(x == x and x > 0 for x in kl))
            g = lambda kunci_, m: float(p[kunci_][m]) if p else np.nan
            baris.append(dict(
                peranan=nm, id=r.id, pencetus=r.pencetus, induk=r.induk, nama=o['nama'], prasyarat=_teks(c5.tk_pra, r.q1, r.q2),
                penapis=_teks(c5.tk_pen, r.f1, r.f2),
                q1=r.q1, q2=r.q2, f1=r.f1, f2=r.f2, skor_A=r.skor, n=d['n'], tahun=d['tahun'], setahun=d['n'] / s11.TAHUN,
                shariah_setahun=(len(o['beli_A']) + len(o['beli_B'])) / s11.TAHUN,
                m5=d['m5'], terus=d['terus'], a_terus=d['a_terus'], naik=d['naik'], a_naik=d['a_naik'], naik10=d['naik10'], naik20=d['naik20'],
                kl_naik=d['naik'] - d['a_naik'], kl_naik_K1=kl[0], kl_naik_K2=kl[1], kl_naik_K3=kl[2],
                menang_J20=d['menang'], purata_J20=d['purata'], rugi8_J20=d['rugi8'], stop_J20=d['stop'],
                n_pegang=p['n'] if p else 0, purata_B=g('purata', CARA_B), menang_B=g('menang', CARA_B), rugi15_B=g('rugi15', CARA_B),
                hari_B=g('sesi', CARA_B), purata_J20_semua=g('purata', 0), menang_J20_semua=g('menang', 0), lulus=lulus))
    return pd.DataFrame(baris)


def bacaan(T):
    """Bacaan dikunci pindaan (u)."""
    c = T[T.peranan == 'calon'].sort_values('skor_A', ascending=False, kind='stable')
    a, k = c.head(N_BACA), T[T.peranan == 'kawalan']
    o = dict(n_calon=len(c), n_lulus=int(c.lulus.sum()), atas=len(a), atas_lulus=float(a.lulus.mean()) if len(a) else np.nan,
             kawalan=len(k), kawalan_lulus=float(k.lulus.mean()) if len(k) else np.nan,
             atas_kl=float(a.kl_naik.median()) if len(a) else np.nan, kawalan_kl=float(k.kl_naik.median()) if len(k) else np.nan)
    o['ya'] = bool(o['atas_lulus'] > 0.5 and o['atas_lulus'] >= o['kawalan_lulus'] + 0.20 and o['atas_kl'] >= 0.02)
    return o


def gabung(K, ids):
    semua = set()
    for i in ids:
        semua |= K[i]['beli_A'] | K[i]['beli_B']
    bulan = {t // 100 for _, t in semua}
    return len(semua) / s11.TAHUN, len(bulan) / (s11.TAHUN * 12)


def lapor_(kerja):
    import cs_lapor as lapor
    C = pickle.load(open(os.path.join(kerja, 'cs12_calon.pkl'), 'rb'))
    K = pickle.load(open(os.path.join(kerja, 'cs12_kunci.pkl'), 'rb'))
    T = jadual(C, K)
    B = bacaan(T)
    d_ = os.path.join(SINI, 'hasil', PUS)
    os.makedirs(d_, exist_ok=True)
    T[T.peranan == 'calon'].drop(columns='peranan').to_csv(os.path.join(d_, 'calon.csv.gz'), index=False, float_format='%.5f')
    T[T.peranan == 'kawalan'].drop(columns='peranan').to_csv(os.path.join(d_, 'kawalan.csv'), index=False, float_format='%.5f')
    c = T[T.peranan == 'calon']
    L = c[c.lulus]
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    p = lambda x, k=0, t=False: '–' if x is None or x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')
    f11 = os.path.join(SINI, 'hasil', 'CS11', 'semak_f.csv')
    G = pd.read_csv(f11).groupby('kump')[['m5', 'terus', 'a_terus', 'naik', 'a_naik', 'naik10', 'menang', 'purata']].median() if os.path.exists(f11) else None
    g30, b30 = gabung(K, L.id.head(30).tolist()) if len(L) else (0.0, 0.0)
    gs, bs = gabung(K, L.id.tolist()) if len(L) else (0.0, 0.0)
    A = ['# CS12: carian baharu ikut ukuran longgar — setup yang menangkap saham yang naik berterusan, walaupun perlahan (backtest; BUKAN bukti)',
         '', status, '',
         'Dijana `kajian/carian_setup/cs_cari12.py`. Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 15 Nov 2026 (u). '
         '**Jangan sunting secara manual.**', '',
         '## 1. Apa yang dicari', '',
         '- **Ukuran longgar ("naik")**: selepas 4 minggu harga ≥ 2 % di atas harga beli (kira-kira 0.1 % sehari), masih di atas purata 20 '
         'harinya (trend naik), dan tidak pernah tutup 10 % di bawah harga beli.',
         f"- {C['n_pencetus']:,} isyarat beli (kaedah M, kaedah N, indikator dan variannya), setiap satu digabung dengan prasyarat pasaran, prasyarat "
         f"syarikat dan penapis saham; {C['n_cukup']:,} cukup isyarat untuk diskor. Skor dikira pada saham carian sahaja.",
         f"- **{B['n_calon']:,} calon** berskor positif (sehingga {N_ATAS} peraturan terbaik setiap isyarat beli; tiada had bilangan).",
         '- Setup lengkap setiap calon: beli pada buka esok; stop loss 4xATR14; pegang sekurang-kurangnya hingga hari ke-20; selepas itu jual bila '
         'harga tutup di bawah purata 20 hari; paling lama 6 bulan.', '',
         '## 2. Ujian (ditetapkan dahulu; pada saham yang carian tidak lihat)', '',
         f"- 100 calon teratas ikut skor: **{p(B['atas_lulus'])} % lulus** (perlu > 50 %); kawalan rawak ({B['kawalan']} peraturan dipilih rambang daripada "
         f"ruang yang sama): {p(B['kawalan_lulus'])} % lulus (perlu beza ≥ 20 mata).",
         f"- Median kelebihan atas saham rawak hari sama: 100 teratas {p(B['atas_kl'], 1, True)} mata (perlu ≥ +2); kawalan {p(B['kawalan_kl'], 1, True)} mata.",
         f"- Semua calon: {B['n_lulus']:,} daripada {B['n_calon']:,} lulus.",
         f"- **Keputusan: carian ikut ukuran longgar {'BERHASIL' if B['ya'] else 'TIDAK berhasil'}.**", '',
         '"Lulus" = belian ≥ 300, ≥ 10 tahun aktif, dan lebih baik daripada saham rawak hari sama dalam ketiga-tiga tempoh (2010–19, 2020–24, 2025–26).', '',
         '## 3. Banding (nilai tengah setiap kumpulan; saham yang carian tidak lihat; jual hari ke-20)', '',
         '| Kumpulan | Bilangan | Naik ≥ 5 % minggu 1 % | Ukuran ketat % (rawak) | Ukuran longgar % (rawak) | Naik ≥ 10 % selepas 4 minggu % | Menang % | Purata % |',
         '|---' * 8 + '|']
    if G is not None:
        for kk, nm in (('M asal', 'Kaedah M asal'), ('N asal', 'Kaedah N asal'), ('F', 'Setup F sedia ada')):
            if kk in G.index:
                g = G.loc[kk]
                A.append(f"| {nm} | {int((pd.read_csv(f11).kump == kk).sum())} | {p(g.m5)} | {p(g.terus)} ({p(g.a_terus)}) | {p(g.naik)} ({p(g.a_naik)}) | {p(g.naik10)} | {p(g.menang)} | {p(g.purata, 1, True)} |")
    for nm, X in (('Calon baharu yang lulus', L), ('30 calon lulus teratas', L.head(30)), ('Kawalan rawak', T[T.peranan == 'kawalan'])):
        if len(X):
            g = X.median(numeric_only=True)
            A.append(f"| {nm} | {len(X)} | {p(g.m5)} | {p(g.terus)} ({p(g.a_terus)}) | {p(g.naik)} ({p(g.a_naik)}) | {p(g.naik10)} | {p(g.menang_J20)} | {p(g.purata_J20, 1, True)} |")
    A += ['', '## 4. Kekerapan belian pada senarai Shariah', '',
          f"- 30 calon lulus teratas digabung: {g30:.0f} belian (saham-hari berbeza) setahun; ada belian dalam {b30:.0%} bulan.",
          f"- Semua {len(L)} calon lulus digabung: {gs:.0f} setahun; ada belian dalam {bs:.0%} bulan.", '',
          '## 5. 50 calon lulus teratas (disusun ikut skor pada saham carian; angka pada saham yang carian tidak lihat)', '',
          'Naik = ukuran longgar; kurungan = saham rawak pada hari yang sama. "Cara pegang B" = pegang hingga harga tutup di bawah purata 20 hari '
          '(selepas hari ke-20).', '',
          '| ID | Prasyarat | Isyarat beli | Penapis saham | Beli setahun (senarai Shariah) | Naik % (rawak) | Naik ≥ 10 % / ≥ 20 % | Ketat % (rawak) | Jual hari ke-20: menang · purata | Cara pegang B: menang · purata · rugi ≥ 15 % · hari |',
          '|---' * 10 + '|']
    for r in L.head(50).itertuples():
        A.append(f"| `{r.id}` | {r.prasyarat or 'Tiada'} | {r.nama} | {r.penapis or '–'} | {r.setahun:.0f} ({r.shariah_setahun:.0f}) | **{p(r.naik)}** ({p(r.a_naik)}) | "
                 f"{p(r.naik10)} / {p(r.naik20)} | {p(r.terus)} ({p(r.a_terus)}) | {p(r.menang_J20)} % · {p(r.purata_J20, 1, True)} % | "
                 f"{p(r.menang_B)} % · {p(r.purata_B, 1, True)} % · {p(r.rugi15_B)} % · {r.hari_B:.0f} |")
    A += ['', f'Senarai penuh {len(c):,} calon (lulus dan tidak): `hasil/CS12/calon.csv.gz`; kawalan rawak: `kawalan.csv`.', '',
          '## 6. Mengapa ujian gagal: tahun yang carian tidak lihat (analisis SELEPAS hasil; bukan ditetapkan dahulu)', '',
          'Saham yang tidak dilihat berkongsi TAHUN yang sama dengan saham carian bagi 2010–2024; hanya 2025–26 yang benar-benar tidak dilihat dari '
          'segi masa. Peraturan dengan belian ≥ 300 dan ≥ 10 tahun aktif:', '',
          '| Kumpulan | Bilangan | Lebih baik daripada rawak: 2010–19 | 2020–24 | **2025–26** | Median kelebihan 2010–19 / 2020–24 / 2025–26 (mata) |',
          '|---' * 6 + '|']
    kw = T[T.peranan == 'kawalan']
    for nm, X in (('Calon carian', c), ('Kawalan rawak', kw), ('Calon tanpa prasyarat pasaran', c[c.q1 < 0])):
        e = X[(X.n >= s11.MIN_BELIAN) & (X.tahun >= s11.MIN_TAHUN)]
        if len(e):
            A.append(f"| {nm} | {len(e):,} | {(e.kl_naik_K1 > 0).mean():.0%} | {(e.kl_naik_K2 > 0).mean():.0%} | **{(e.kl_naik_K3 > 0).mean():.0%}** | "
                     f"{p(e.kl_naik_K1.median(), 1, True)} / {p(e.kl_naik_K2.median(), 1, True)} / {p(e.kl_naik_K3.median(), 1, True)} |")
    if G is not None:
        Fx = pd.read_csv(f11)
        Fx = Fx[(Fx.kump == 'F') & (Fx.n >= s11.MIN_BELIAN) & (Fx.tahun >= s11.MIN_TAHUN)]
        A.append(f"| Setup F sedia ada, ukuran KETAT | {len(Fx)} | {(Fx.kl_terus_K1 > 0).mean():.0%} | {(Fx.kl_terus_K2 > 0).mean():.0%} | **{(Fx.kl_terus_K3 > 0).mean():.0%}** | "
                 f"{p(Fx.kl_terus_K1.median(), 1, True)} / {p(Fx.kl_terus_K2.median(), 1, True)} / {p(Fx.kl_terus_K3.median(), 1, True)} |")
    cp = c[(c.n >= s11.MIN_BELIAN) & (c.tahun >= s11.MIN_TAHUN)]
    A += ['', f"- {int((c.q1 >= 0).sum()):,} daripada {len(c):,} calon memakai prasyarat pasaran: kelebihan ukuran longgar pada 2010–2024 hampir semuanya datang "
          'daripada BILA membeli (keadaan pasaran dan kalendar), dan ia tidak berulang pada 2025–26.',
          '- Prasyarat pasaran paling kerap antara calon, dengan median kelebihan 2025–26: '
          + '; '.join(f"{lapis.PASARAN[int(q)][5:]} ({len(g_)} calon, {p(g_.kl_naik_K3.median(), 1, True)})"
                      for q, g_ in sorted(cp[cp.q1 >= 0].groupby('q1'), key=lambda x: -len(x[1]))[:8]) + '.', '',
          '## 7. Kaveat', '',
          '- Beratus-ratus calon disemak pada saham yang tidak dilihat, jadi sebahagian lulus kerana nasib: bandingkan dengan kadar lulus kawalan rawak.',
          '- "Lebih baik daripada rawak hari sama" mengukur PILIHAN saham; angka naik mentah turut mengandungi kesan BILA membeli (keadaan pasaran).',
          '- Saham yang tidak dilihat sudah digunakan dalam pusingan terdahulu; tiada saham delist (lebih penting bagi pegangan hingga 6 bulan). '
          'Belum didaftarkan sebagai kod F: itu keputusan pengguna. Backtest sahaja; kad skor kekal satu-satunya keputusan wang sebenar.', '']
    open(os.path.join(d_, 'CARIAN.md'), 'w', encoding='utf-8').write('\n'.join(A))
    cari.log(f"CS12 lapor: calon {B['n_calon']}, lulus {B['n_lulus']}; 100 teratas lulus {B['atas_lulus']:.0%} lawan kawalan {B['kawalan_lulus']:.0%}; "
             f"median kelebihan {B['atas_kl'] * 100:+.1f} -> {'BERHASIL' if B['ya'] else 'TIDAK'}")
    return T, B


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
    else:
        raise SystemExit(f'arahan tidak dikenali: {cmd}')
