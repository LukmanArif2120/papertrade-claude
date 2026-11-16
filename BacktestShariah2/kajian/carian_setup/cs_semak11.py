"""Carian setup — pusingan CS11 (SPEC pindaan 15 Nov 2026 (t)): semak semula semua setup F dengan ukuran longgar pengguna.

Tiga perkara yang disemak, ikut kata pengguna ("naik perlahan pun ok asalkan trend naik; just hold; jangan terlalu strict"):
1. dua ukuran sebelah-menyebelah: `terus` (ketat) dan `naik` (longgar);
2. cara pegang: jual pada sesi 20 (J20) lawan enam cara "pegang selagi trend naik" (had 126 sesi);
3. kekerapan belian pada senarai Shariah; dan banding kaedah M asal, N asal dan setup F pada ukuran yang sama.
Guna: python3 cs_semak11.py semak|lapor <kerja>. Jangan sunting keluaran secara manual."""
import os
import pickle
import sys

import numpy as np
import pandas as pd
from numba import njit, prange

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_atom as atom  # noqa: E402
import cs_cari as cari  # noqa: E402
import cs_keluar7 as k7  # noqa: E402
import cs_keluar10 as k10  # noqa: E402
import cs_teras as teras  # noqa: E402

T20, H, KOS, HENTI = 20, 126, teras.KOS, k7.HENTI
CARA = ['J20', 'P-MA20', 'P-MA20x2', 'P-MA50', 'P-R10', 'P-CH4', 'P-126']
CARA_TEKS = {'J20': 'jual pada hari ke-20 (cara sekarang)', 'P-MA20': 'pegang hingga tutup di bawah purata 20 hari',
             'P-MA20x2': 'pegang hingga dua tutup berturut di bawah purata 20 hari',
             'P-MA50': 'pegang hingga tutup di bawah purata 50 hari', 'P-R10': 'pegang hingga tutup di bawah paras terendah 10 hari',
             'P-CH4': 'pegang hingga jatuh 4xATR14 dari tutup tertinggi', 'P-126': 'pegang 6 bulan (stop loss sahaja)'}
NC = len(CARA)
NAIK_MIN, NAIK_LANTAI = 0.02, 0.10                      # dikunci pindaan (t): +2 % (~0.1 % sehari); tiada tutup <= -10 %
MIN_BELIAN, MIN_TAHUN, MIN_SETAHUN = 300, 10, 24        # "menepati semua" dan tafsiran "beberapa kali sebulan"
S_ASAL = HENTI.index('4xATR14')                         # stop loss bagi banding M / N asal
LABEL = ('m5', 'terus', 'naik', 'naik10', 'naik20')
TAHUN = (pd.Timestamp('2026-08-28') - pd.Timestamp('2010-01-04')).days / 365.25
PUS = 'CS11'


@njit(cache=True)
def _aras(P, a, s):
    if s == 0:
        return P * 0.92
    if s == 1:
        return P * 0.90
    if s == 2:
        return P * 0.88
    if s == 3:
        return P * 0.85
    if s == 4:
        return P - 3.0 * a
    if s == 5:
        return P - 4.0 * a
    if s == 6:
        return P - 5.0 * a
    return min(P * 0.90, P - 4.0 * a)


@njit(parallel=True, cache=True)
def label11(ev, o, l, c):
    """[m5, terus, naik, naik10, naik20] setiap isyarat (P = buka sesi 1; sesi 1-20). Lihat pindaan (t)."""
    out = np.zeros((ev.shape[0], 5), np.float32)
    for k in prange(ev.shape[0]):
        e = ev[k] + 1
        P = o[e]
        h8 = c[e] <= P * 0.92
        jum, mn = 0.0, c[e]
        for d in range(T20):
            b = e + d
            jum += c[b]
            if c[b] < mn:
                mn = c[b]
            if d >= 1 and (o[b] <= P * 0.92 or l[b] <= P * 0.92):
                h8 = True
        c5, c20 = c[e + 4], c[e + T20 - 1]
        if c5 >= P * 1.05:
            out[k, 0] = 1.0
            if c20 > c5 and not h8:
                out[k, 1] = 1.0
        if c20 >= P * (1.0 + NAIK_MIN) and c20 > jum / T20 and mn > P * (1.0 - NAIK_LANTAI):
            out[k, 2] = 1.0
            if c20 >= P * 1.10:
                out[k, 3] = 1.0
            if c20 >= P * 1.20:
                out[k, 4] = 1.0
    return out


@njit(parallel=True, cache=True)
def jual20(ev, o, l, c, atr, s):
    """(R, sesi jual, kena stop) bagi "pegang 20 hari + stop loss s". Mekanik sama seperti cs_keluar7 (X00)."""
    n = ev.shape[0]
    R, sk, st = np.empty(n), np.empty(n, np.int64), np.zeros(n, np.bool_)
    for k in prange(n):
        i = ev[k]
        e = i + 1
        P = o[e]
        Ls = _aras(P, atr[i], s)
        R[k], sk[k] = c[e + T20 - 1] / P - 1.0 - KOS, T20 - 1
        if c[e] <= Ls:
            R[k], sk[k], st[k] = o[e + 1] / P - 1.0 - KOS, 1, True
            continue
        for d in range(1, T20):
            b = e + d
            if o[b] <= Ls:
                R[k], sk[k], st[k] = o[b] / P - 1.0 - KOS, d, True
                break
            if l[b] <= Ls:
                R[k], sk[k], st[k] = Ls / P - 1.0 - KOS, d, True
                break
    return R, sk, st


@njit(parallel=True, cache=True)
def pegang(ev, o, l, c, atr, B, s):
    """R[isyarat, cara] dan sesi jual SK[isyarat, cara] bagi 7 cara pegang (CARA). B = uint8 [4, bar]: tutup < SMA20; dua
    tutup berturut < SMA20; tutup < SMA50; tutup < rendah 10 hari sebelumnya. Peraturan trend hanya dinilai mulai tutup sesi
    20 (indeks 19) -> jual buka sesi berikutnya; stop loss aktif sejak sesi 2; had 126 sesi (tetingkap mesti lengkap)."""
    n = ev.shape[0]
    R = np.zeros((n, NC))
    SK = np.zeros((n, NC), np.int64)
    for k in prange(n):
        i = ev[k]
        e = i + 1
        P = o[e]
        Ls = _aras(P, atr[i], s)
        h0 = c[e] <= Ls
        ds, ps = 999, 0.0
        for d in range(1, H):
            b = e + d
            if o[b] <= Ls:
                ds, ps = d, o[b]
                break
            if l[b] <= Ls:
                ds, ps = d, Ls
                break
        dx = np.full(5, 999, np.int64)
        hc = c[e]
        for d in range(H - 1):
            b = e + d
            if c[b] > hc:
                hc = c[b]
            if d < T20 - 1:
                continue
            for j in range(4):
                if dx[j] == 999 and B[j, b] != 0:
                    dx[j] = d + 1
            if dx[4] == 999 and c[b] < hc - 4.0 * atr[b]:
                dx[4] = d + 1
        for m in range(NC):
            if h0:
                R[k, m], SK[k, m] = o[e + 1] / P - 1.0 - KOS, 1
            elif m == 0:
                if ds <= T20 - 1:
                    R[k, m], SK[k, m] = ps / P - 1.0 - KOS, ds
                else:
                    R[k, m], SK[k, m] = c[e + T20 - 1] / P - 1.0 - KOS, T20 - 1
            else:
                x = dx[m - 1] if m <= 5 else 999
                if x != 999 and x <= ds:
                    R[k, m], SK[k, m] = o[e + x] / P - 1.0 - KOS, x
                elif ds != 999:
                    R[k, m], SK[k, m] = ps / P - 1.0 - KOS, ds
                else:
                    R[k, m], SK[k, m] = c[e + H - 1] / P - 1.0 - KOS, H - 1
    return R, SK


def siri_trend(pan):
    """Matriks uint8 [4, bar]: tutup < SMA20; dua tutup berturut < SMA20; tutup < SMA50; tutup < rendah 10 hari sebelumnya."""
    c, tid = pan['c'], pan['tid']
    with np.errstate(invalid='ignore'):
        b20 = c < k10.sma_panel(pan, 20)
        b50 = c < k10.sma_panel(pan, 50)
        i = np.arange(len(c))
        sama = np.concatenate([[False], tid[1:] == tid[:-1]])
        b20x2 = b20 & np.concatenate([[False], b20[:-1]]) & sama
        ll = pd.Series(pan['l']).groupby(tid).transform(lambda s: s.rolling(10).min().shift(1)).to_numpy()
        r10 = c < ll
    return np.stack([b20, b20x2, b50, r10]).astype(np.uint8)


def sah126(pan):
    i = np.arange(len(pan['c']))
    return pan['sah'] & (i + H < pan['mula'][pan['tid'] + 1])


def asas(pan):
    """(Lab[bar, 5], As[bar, 5]): label setiap bar layak dan asas rawak hari sama x tercile ATR %."""
    sah = np.flatnonzero(pan['sah'])
    Lb = label11(sah, pan['o'], pan['l'], pan['c'])
    hari = pan['hari'][sah]
    pct = pd.Series(pan['atr'][sah] / pan['c'][sah]).groupby(hari).rank(pct=True).to_numpy()
    g = hari * 3 + np.minimum((pct * 3).astype(np.int64), 2)
    bil = np.maximum(np.bincount(g), 1)
    N = len(pan['c'])
    Lab, As = np.zeros((N, 5), np.float32), np.zeros((N, 5), np.float32)
    Lab[sah] = Lb
    As[sah] = np.stack([np.bincount(g, Lb[:, j]) / bil for j in range(5)], 1)[g]
    return Lab, As


def setup_f(kerja, set_, pan, EV, Lr):
    """Senarai (id, ev, henti, prasyarat) bagi 69 setup kedudukan akhir pada set itu (semua isyarat masuk)."""
    import cs_cs05 as c5
    import cs_cs07 as c7
    import cs_lapor as lapor
    import cs_pegang as pg
    import cs_portfolio6 as p6
    import cs_tala7 as t7
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('').set_index('id')
    KA = pd.read_csv(os.path.join(SINI, 'hasil', 'KEDUDUKAN_AKHIR.csv')).set_index('id')
    out = []
    for i in KA.index:
        r = reg.loc[i]
        if r.pusingan == 'CS07':
            d = c7.dari_takrif7(r.takrif)
            ev, s = t7.ev_satu(kerja, set_, d['pencetus']), d['s']
        else:
            d = p6.dari_takrif5(r.takrif)
            ev, s = EV[d['pencetus']], pg.lama_ke_baharu(d['lajur'])[0]
        pra = KA.loc[i, 'prasyarat']
        out.append(dict(id=i, kump='F', ev=ev[c5.topeng(pan, Lr, ev, d['q1'], d['q2'], d['f1'], d['f2'])], s=int(s),
                        prasyarat=pra if isinstance(pra, str) and pra.strip() not in ('', '–') else '',
                        pencetus=KA.loc[i, 'pencetus'], penapis=KA.loc[i, 'penapis'], kedudukan=int(KA.loc[i, 'kedudukan'])))
    return out


def asal_mn(EV):
    """Kaedah M asal (parameter lalai) dan N asal: isyarat tanpa prasyarat atau penapis, stop loss 4xATR14."""
    out = []
    for nama, ev in EV.items():
        kump = 'M asal' if (nama[0] == 'M' and nama.endswith('.0')) else 'N asal' if nama[0] == 'N' else None
        if kump:
            out.append(dict(id=nama.replace('.0', ''), kump=kump, ev=ev, s=S_ASAL, prasyarat='', pencetus=nama, penapis='', kedudukan=0))
    return out


def ukur_tangkap(pan, Lab, As, ev, s):
    """Statistik belian (satu posisi setiap saham, jual hari ke-20 + stop loss s) pada satu set."""
    R, sk, st = jual20(np.ascontiguousarray(ev, dtype=np.int64), pan['o'], pan['l'], pan['c'], pan['atr'], s)
    amb = teras.satu_posisi(ev, sk, pan['tid'])
    e, R, sk, st = ev[amb], R[amb], sk[amb], st[amb]
    tp = pan['tempoh'][e]
    d = dict(n=len(e), tahun=int(len(np.unique(pan['tarikh'][e] // 10000))) if len(e) else 0, menang=float((R > 0).mean()) if len(e) else np.nan,
             purata=float(R.mean()) if len(e) else np.nan, rugi8=float((R <= -0.08).mean()) if len(e) else np.nan,
             stop=float(st.mean()) if len(e) else np.nan, jual_hari_beli=int((sk == 0).sum()), awal_bukan_stop=int(((sk < 3) & ~st).sum()))
    for j, nm in enumerate(LABEL):
        d[nm] = float(Lab[e, j].mean()) if len(e) else np.nan
        d['a_' + nm] = float(As[e, j].mean()) if len(e) else np.nan
    for nm, j in (('terus', 1), ('naik', 2)):
        for p in range(3):
            q = tp == p
            d[f'kl_{nm}_K{p + 1}'] = float((Lab[e[q], j] - As[e[q], j]).mean()) if q.any() else np.nan
    return d, e


def ukur_pegang(pan, Lab, B, ev, s):
    """Statistik setiap cara pegang atas SEMUA isyarat dengan tetingkap 126 sesi lengkap (berpasangan)."""
    ev = np.ascontiguousarray(ev[sah126(pan)[ev]], dtype=np.int64)
    if len(ev) < 30:
        return None
    R, SK = pegang(ev, pan['o'], pan['l'], pan['c'], pan['atr'], B, s)
    nk = Lab[ev, 2] > 0
    return dict(n=len(ev), purata=R.mean(0), menang=(R > 0).mean(0), rugi15=(R <= -0.15).mean(0), sesi=np.median(SK, 0) + 1,
                R_naik=R[nk].mean(0) if nk.any() else np.full(NC, np.nan), n_naik=int(nk.sum()))


def semak(kerja):
    """Kira semua -> kerja/cs11_semak.pkl."""
    import cs_lapis as lapis
    import cs_lapor as lapor
    shar = set(open(os.path.join(lapor.BS2, 'data', 'harga', 'univ.txt')).read().split())
    D = {}
    for set_ in ('B', 'A'):
        pan = cari.panel(kerja, set_)
        EV = cari.pencetus(pan, pickle.load(open(os.path.join(kerja, f'benih_{set_}.pkl'), 'rb')))
        L = lapis.muat(kerja, set_)
        Lab, As = asas(pan)
        B = siri_trend(pan)
        sh = np.asarray([t in shar for t in pan['ticker']])
        cari.log(f"CS11 {set_}: saham {len(pan['ticker'])}, Shariah {int(sh.sum())}; asas terus {Lab[pan['sah'], 1].mean() * 100:.1f}% "
                 f"naik {Lab[pan['sah'], 2].mean() * 100:.1f}% naik10 {Lab[pan['sah'], 3].mean() * 100:.1f}% naik20 {Lab[pan['sah'], 4].mean() * 100:.1f}%")
        for x in setup_f(kerja, set_, pan, EV, (L['L1'], L['L2'])) + asal_mn(EV):
            d, e = ukur_tangkap(pan, Lab, As, x['ev'], x['s'])
            r = D.setdefault(x['id'], {k: x[k] for k in ('id', 'kump', 's', 'prasyarat', 'pencetus', 'penapis', 'kedudukan')})
            r[set_] = d
            r['pegang_' + set_] = ukur_pegang(pan, Lab, B, x['ev'], x['s'])
            r['shariah_' + set_] = int(sh[pan['tid'][e]].sum())
            r['beli_' + set_] = set(zip(pan['ticker'][pan['tid'][e]][sh[pan['tid'][e]]].tolist(), pan['tarikh'][e + 1][sh[pan['tid'][e]]].tolist()))
        D['_asas_' + set_] = {nm: float(Lab[pan['sah'], j].mean()) for j, nm in enumerate(LABEL)}
        D['_shariah_' + set_] = int(sh.sum())
    pickle.dump(D, open(os.path.join(kerja, 'cs11_semak.pkl'), 'wb'), protocol=4)
    return D


def jadual(D):
    """Satu baris setiap setup / kaedah: ukuran pada kumpulan B, kekerapan Shariah pada A + B, takrif "menepati semua"."""
    baris = []
    for i, r in D.items():
        if i.startswith('_'):
            continue
        b = r['B']
        kl = [b[f'kl_naik_K{p}'] for p in (1, 2, 3)]
        klt = [b[f'kl_terus_K{p}'] for p in (1, 2, 3)]
        dipercayai = bool(b['n'] >= MIN_BELIAN and b['tahun'] >= MIN_TAHUN and all(x == x and x > 0 for x in kl))
        swing = bool(b['jual_hari_beli'] == 0 and b['awal_bukan_stop'] == 0)
        baris.append(dict(
            id=i, kump=r['kump'], kedudukan=r['kedudukan'], prasyarat=r['prasyarat'], pencetus=r['pencetus'], penapis=r['penapis'],
            henti=HENTI[r['s']], n=b['n'], tahun=b['tahun'], setahun=b['n'] / TAHUN,
            shariah_setahun=(r['shariah_A'] + r['shariah_B']) / TAHUN,
            m5=b['m5'], terus=b['terus'], a_terus=b['a_terus'], naik=b['naik'], a_naik=b['a_naik'], naik10=b['naik10'], a_naik10=b['a_naik10'],
            naik20=b['naik20'], a_naik20=b['a_naik20'], kl_naik_K1=kl[0], kl_naik_K2=kl[1], kl_naik_K3=kl[2],
            kl_terus_K1=klt[0], kl_terus_K2=klt[1], kl_terus_K3=klt[2], menang=b['menang'], purata=b['purata'], rugi8=b['rugi8'], stop=b['stop'],
            swing=swing, lulus_naik=dipercayai, lulus_terus=bool(b['n'] >= MIN_BELIAN and b['tahun'] >= MIN_TAHUN and all(x == x and x > 0 for x in klt)),
            menepati=bool(r['kump'] == 'F' and r['prasyarat'] != '' and swing and dipercayai)))
    T = pd.DataFrame(baris)
    return T.sort_values(['kump', 'menepati', 'naik'], ascending=[True, False, False]).reset_index(drop=True)


def jadual_pegang(D):
    """Setiap setup F x cara pegang pada A dan B, cara terpilih (A) dan bacaan dikunci (B)."""
    ids = [i for i, r in D.items() if not i.startswith('_') and r['kump'] == 'F' and r['pegang_A'] and r['pegang_B']]
    dA = np.mean([D[i]['pegang_A']['purata'] - D[i]['pegang_A']['purata'][0] for i in ids], axis=0)
    pilih = int(np.argmax(dA[1:])) + 1
    baris = []
    for i in ids:
        for st in ('A', 'B'):
            p = D[i]['pegang_' + st]
            for m in range(NC):
                baris.append(dict(id=i, set=st, cara=CARA[m], n=p['n'], purata=p['purata'][m], menang=p['menang'][m], rugi15=p['rugi15'][m],
                                  sesi=p['sesi'][m], R_naik=p['R_naik'][m]))
    P = pd.DataFrame(baris)
    b = P[P.set == 'B'].pivot(index='id', columns='cara')
    c0, c1 = 'J20', CARA[pilih]
    baca = dict(pilih=c1, dA=[float(x) for x in dA], n=len(ids), lebih=int((b['purata'][c1] > b['purata'][c0]).sum()),
                d_menang=float((b['menang'][c1] - b['menang'][c0]).median()), d_rugi15=float((b['rugi15'][c1] - b['rugi15'][c0]).median()))
    baca['ya'] = bool(baca['lebih'] > baca['n'] / 2 and baca['d_menang'] >= -0.02 and baca['d_rugi15'] <= 0.02)
    return P, baca


def gabung(D, ids):
    """Belian setahun pada senarai Shariah bagi gabungan setup: (jumlah belian, belian saham-hari berbeza, % bulan ada belian)."""
    semua, bil = set(), 0
    for i in ids:
        for st in ('A', 'B'):
            semua |= D[i]['beli_' + st]
            bil += len(D[i]['beli_' + st])
    bulan = {t // 100 for _, t in semua}
    return bil / TAHUN, len(semua) / TAHUN, len(bulan) / (TAHUN * 12)


def lapor_(kerja):
    import cs_lapor as lapor
    D = pickle.load(open(os.path.join(kerja, 'cs11_semak.pkl'), 'rb'))
    T = jadual(D)
    P, baca = jadual_pegang(D)
    d_ = os.path.join(SINI, 'hasil', PUS)
    os.makedirs(d_, exist_ok=True)
    T.to_csv(os.path.join(d_, 'semak_f.csv'), index=False, float_format='%.5f')
    P.to_csv(os.path.join(d_, 'pegang.csv'), index=False, float_format='%.5f')
    F = T[T.kump == 'F']
    lulus = F[F.menepati]
    g_semua, g_beza, g_bulan = gabung(D, lulus.id.tolist()) if len(lulus) else (0.0, 0.0, 0.0)
    G = T.groupby('kump')[['n', 'setahun', 'shariah_setahun', 'm5', 'terus', 'a_terus', 'naik', 'a_naik', 'naik10', 'naik20', 'menang', 'purata', 'rugi8']].median()
    G['bil'] = T.groupby('kump').size()
    G['lulus_naik'] = T.groupby('kump').lulus_naik.sum()
    G.to_csv(os.path.join(d_, 'banding.csv'), float_format='%.5f')
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    p = lambda x, k=0, t=False: '–' if x is None or x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')
    ab = D['_asas_B']
    A = ['# CS11: semak semula setup F dengan ukuran longgar ("naik perlahan pun kira"), pegang selepas 4 minggu, kekerapan, dan banding M / N / F (backtest; BUKAN bukti)',
         '', status, '',
         'Dijana `kajian/carian_setup/cs_semak11.py`. Peraturan ditulis dahulu: `kajian/SPEC_CARIAN_SETUP.md` pindaan 15 Nov 2026 (t). '
         '**Jangan sunting secara manual.**', '',
         '## 1. Dua ukuran', '',
         '- **Ketat (`terus`)**: naik ≥ 5 % dalam minggu pertama DAN naik lagi hingga minggu ke-4.',
         '- **Longgar (`naik`)**: selepas 4 minggu harga ≥ 2 % di atas harga beli (kira-kira 0.1 % sehari), masih di atas purata 20 harinya '
         '(trend naik), dan tidak pernah tutup 10 % di bawah harga beli.',
         f'- Saham rawak pada mana-mana hari (saham yang carian tidak lihat): ketat {p(ab["terus"], 1)} %, longgar {p(ab["naik"], 1)} % '
         f'(naik ≥ 10 %: {p(ab["naik10"], 1)} %; naik ≥ 20 %: {p(ab["naik20"], 1)} %).', '',
         '## 2. Banding kaedah M asal, N asal dan setup F (ukuran sama, cara pegang sama; median setiap kumpulan)', '',
         '| Kumpulan | Bilangan | Beli setahun | Naik ≥ 5 % minggu 1 % | Ketat % (rawak) | Longgar % (rawak) | Naik ≥ 10 % selepas 4 minggu % | Menang % | Purata % | Lulus ukuran longgar |',
         '|---' * 10 + '|']
    for k in ('M asal', 'N asal', 'F'):
        if k in G.index:
            g = G.loc[k]
            A.append(f"| {k} | {int(g.bil)} | {g.setahun:.0f} | {p(g.m5)} | {p(g.terus)} ({p(g.a_terus)}) | {p(g.naik)} ({p(g.a_naik)}) | {p(g.naik10)} | "
                     f"{p(g.menang)} | {p(g.purata, 1, True)} | {int(g.lulus_naik)} daripada {int(g.bil)} |")
    g = lulus.median(numeric_only=True) if len(lulus) else None
    if g is not None:
        A.append(f"| F yang menepati semua | {len(lulus)} | {g.setahun:.0f} | {p(g.m5)} | {p(g.terus)} ({p(g.a_terus)}) | {p(g.naik)} ({p(g.a_naik)}) | {p(g.naik10)} | "
                 f"{p(g.menang)} | {p(g.purata, 1, True)} | {len(lulus)} daripada {len(lulus)} |")
    A += ['', '"Lulus ukuran longgar" = belian ≥ 300, ≥ 10 tahun aktif dan lebih baik daripada saham rawak hari sama dalam ketiga-tiga tempoh '
          '(2010–19, 2020–24, 2025–26). Kaedah M dan N asal dipegang dengan cara yang sama (20 hari, stop loss 4xATR14) supaya adil; '
          'dalam papertrade sebenar kaedah M menjual 11 % dagangan pada hari beli (`hasil/PEGANG_MIN.md`), setup F tiada.', '',
          '## 3. Pegang selepas 4 minggu (semua isyarat dengan data 6 bulan lengkap; berpasangan)', '',
          f'Cara terpilih pada saham carian: **{baca["pilih"]}** ({CARA_TEKS[baca["pilih"]]}).', '',
          '| Cara pegang | Saham carian: tambahan purata lawan jual hari ke-20 (mata) | Saham tidak dilihat: purata % | Menang % | Rugi ≥ 15 % % | Median hari pegang | Untung pada saham yang naik % |',
          '|---' * 7 + '|']
    b = P[P.set == 'B'].groupby('cara')[['purata', 'menang', 'rugi15', 'sesi', 'R_naik']].median()
    for m, cr in enumerate(CARA):
        x = b.loc[cr]
        A.append(f"| {cr}: {CARA_TEKS[cr]} | {p(baca['dA'][m], 2, True)} | {p(x.purata, 1, True)} | {p(x.menang)} | {p(x.rugi15)} | {x.sesi:.0f} | {p(x.R_naik, 1, True)} |")
    A += ['', f"- Ujian (ditetapkan dahulu): purata untung cara terpilih lebih tinggi daripada jual hari ke-20 bagi **{baca['lebih']} daripada {baca['n']}** setup "
          f"(perlu lebih separuh); beza kadar menang {p(baca['d_menang'], 1, True)} mata (perlu ≥ −2); beza rugi ≥ 15 % {p(baca['d_rugi15'], 1, True)} mata (perlu ≤ +2).",
          f"- **Keputusan: pegang selepas 4 minggu {'MENOLONG' if baca['ya'] else 'TIDAK menolong'}.**", '',
          '## 4. Kekerapan belian pada senarai Shariah', '',
          f"- Saham Shariah dalam data: {D['_shariah_A'] + D['_shariah_B']} (senarai semasa).",
          f"- {len(lulus)} setup F yang menepati semua, digabung: **{g_semua:.0f} belian setahun** ({g_beza:.0f} saham-hari berbeza; ada belian dalam "
          f"{g_bulan:.0%} bulan). Tafsiran \"beberapa kali sebulan\" = ≥ {MIN_SETAHUN} setahun: **{'LULUS' if g_beza >= MIN_SETAHUN else 'TIDAK'}**.",
          f"- Setiap setup sendirian: {int((lulus.shariah_setahun >= MIN_SETAHUN).sum())} daripada {len(lulus)} membeli ≥ {MIN_SETAHUN} kali setahun pada senarai Shariah.", '',
          '## 5. Setiap setup F (saham yang carian tidak lihat; jual hari ke-20 + stop loss sendiri)', '',
          '| ID | Prasyarat | Stop loss | Beli setahun (senarai Shariah) | Ketat % (rawak) | Longgar % (rawak) | Naik ≥ 10 % / ≥ 20 % selepas 4 minggu | Menang · purata | Menepati semua? | Kekurangan |',
          '|---' * 10 + '|']
    for r in F.sort_values(['menepati', 'naik'], ascending=[False, False]).itertuples():
        kur = []
        if not r.prasyarat:
            kur.append('tiada prasyarat')
        if not r.lulus_naik:
            kur.append('tidak lulus ukuran longgar' if r.n >= MIN_BELIAN else 'belian < 300')
        if r.shariah_setahun < 6:
            kur.append('jarang beli')
        A.append(f"| `{r.id}` | {r.prasyarat or 'Tiada'} | {r.henti} | {r.setahun:.0f} ({r.shariah_setahun:.0f}) | {p(r.terus)} ({p(r.a_terus)}) | "
                 f"**{p(r.naik)}** ({p(r.a_naik)}) | {p(r.naik10)} / {p(r.naik20)} | {p(r.menang)} % · {p(r.purata, 1, True)} % | "
                 f"{'**Ya**' if r.menepati else 'Belum'} | {'; '.join(kur) or '–'} |")
    A += ['', '## 6. Kaveat', '',
          '- Setup F dipilih dahulu ikut ukuran ketat; ini penilaian semula, bukan carian baharu ikut ukuran longgar.',
          '- Saham yang carian tidak lihat sudah digunakan dalam pusingan terdahulu; tiada saham delist; backtest sahaja. '
          'Kad skor kekal satu-satunya keputusan wang sebenar.', '']
    open(os.path.join(d_, 'SEMAK_F.md'), 'w', encoding='utf-8').write('\n'.join(A))
    cari.log(f"CS11 lapor: F {len(F)}, menepati {len(lulus)}; lulus naik {int(F.lulus_naik.sum())}, lulus terus {int(F.lulus_terus.sum())}; pegang {baca['pilih']} "
             f"{baca['lebih']}/{baca['n']} -> {'MENOLONG' if baca['ya'] else 'TIDAK'}; gabungan Shariah {g_beza:.0f}/tahun")
    return T, P, baca


if __name__ == '__main__':
    cmd, kerja = sys.argv[1], sys.argv[2]
    if cmd == 'semak':
        semak(kerja)
    elif cmd == 'lapor':
        lapor_(kerja)
    else:
        raise SystemExit(f'arahan tidak dikenali: {cmd}')
