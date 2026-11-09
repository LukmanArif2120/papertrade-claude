"""Kajian SATELIT — GB02_atau3 × Chandelier 15% akaun di atas teras indeks 35% + tunai.
Pradaftar `REVERSE/SPEC_SATELIT.md` (dikomit sebelum larian).

Enjin keluar, panel harga, topeng isyarat, kos dan peta industri diguna semula daripada
`REVERSE/pembinaan.py`, `REVERSE/step18_nxx.py`, `REVERSE/step22_portfolio_n.py`,
`REVERSE/step24_pegang_slot.py`, `REVERSE/step28_korelasi.py`. Yang baharu: akaun tiga
bahagian (teras diimbang bulanan, satelit berhad berat, tunai), penapis rejim QQQ pada sauh,
had 1 posisi setiap industri, dan ujian asap gabungan masuk+keluar (`--asap`).

Guna: python3 REVERSE/step41_satelit.py [--asap] [--benih 20] [--laporan-sahaja]
Output: REVERSE/satelit.csv, REVERSE/satelit_dagangan.csv, REVERSE/SATELIT.md
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
import REVERSE.pembinaan as PB  # noqa: E402
import REVERSE.step18_nxx as S18  # noqa: E402
import REVERSE.step22_portfolio_n as S22  # noqa: E402
import REVERSE.step24_pegang_slot as S24  # noqa: E402
import REVERSE.step28_korelasi as S28  # noqa: E402
from REVERSE.teras import kos as K  # noqa: E402

KELUAR = AKAR / 'REVERSE'
SPUS_BULANAN = AKAR / 'BacktestShariah2' / 'data' / 'penanda_aras' / 'spus_bulanan.csv'

UJI0, UJI1 = '2020-01-01', '2025-12-31'
LATIH0, LATIH1 = '2012-01-01', '2019-12-31'
W_TERAS, W_SAT, W_TERAS_K1 = 0.35, 0.15, 0.50     # spec §2–3
CAP = 126                                          # had masa SOP
RULE = 'X15'
assert RULE == 'X15', 'keluar X15 sahaja: RSI tidak dibekalkan kepada step24.keluar'
KOS_TERAS = 0.001 + 0.0005                         # komisen + slippage >= USD50j
N_BENIH = 20
SLOT = [8, 10]
MDD_HAD = -10.0

# spec §3 — lengan tetap
LENGAN = {
    'K0': dict(masuk=None, w_teras=W_TERAS, w_sat=0.0, urut=None, rejim=False, had_ind=None),
    'K1': dict(masuk=None, w_teras=W_TERAS_K1, w_sat=0.0, urut=None, rejim=False, had_ind=None),
    'S1': dict(masuk='GB02_atau3', w_teras=W_TERAS, w_sat=W_SAT, urut='U08', rejim=True, had_ind=1),
    'S2': dict(masuk='GB02_atau3', w_teras=W_TERAS, w_sat=W_SAT, urut='U08', rejim=False, had_ind=1),
    'S3': dict(masuk='GB02_atau3', w_teras=W_TERAS, w_sat=W_SAT, urut='U01', rejim=True, had_ind=1),
    'S4': dict(masuk='GB02_atau3', w_teras=W_TERAS, w_sat=W_SAT, urut='U08', rejim=True, had_ind=None),
    'R1': dict(masuk='RAWAK', w_teras=W_TERAS, w_sat=W_SAT, urut='U01', rejim=True, had_ind=1),
    'R2': dict(masuk='RAWAK', w_teras=W_TERAS, w_sat=W_SAT, urut='U08', rejim=True, had_ind=1),
}


# ---------------------------------------------------------------- isyarat
def bina_isyarat():
    """Sama dengan `step22.bina_isyarat` tetapi tanpa merge `pul_kombinasi.parquet`
    (fail itu hanya diperlukan untuk statistik setiap dagangan, bukan untuk topeng)."""
    if S22.SIGF.exists():
        return pd.read_parquet(S22.SIGF)
    import pyarrow.parquet as pq
    rsf = S18.rs_persentil()
    out, t0 = [], time.time()
    kel = S18.kelompok_ticker()
    for i, bk in enumerate(kel):
        P = pq.read_table(S18.PANEL, filters=[('ticker', 'in', set(bk))]).to_pandas()
        P = P.merge(rsf, on=['ticker', 'date'], how='left')
        P = P.sort_values(['ticker', 'date']).reset_index(drop=True)
        T = S18.topeng(P)
        a3 = np.logical_or.reduce([T[k] for k in S22.KOLAM3])
        a4 = np.logical_or.reduce([T[k] for k in S22.KOLAM4])
        sel = a3 | a4
        if sel.any():
            out.append(pd.DataFrame({'ticker': P.ticker.to_numpy()[sel],
                                     'date': P.date.to_numpy()[sel],
                                     'a3': a3[sel], 'a4': a4[sel]}))
        del P, T
        print(f'    [{time.time() - t0:.0f}s] isyarat kelompok {i + 1}/{len(kel)}', flush=True)
    d = pd.concat(out, ignore_index=True)
    S22.CACHE.mkdir(parents=True, exist_ok=True)
    d.to_parquet(S22.SIGF, index=False)
    return d


def calon_gb02(P, S, LAYAK):
    it = {t: i for i, t in enumerate(P.tick)}
    idt = {d: i for i, d in enumerate(P.tarikh)}
    S = S[S.ticker.isin(it) & S.a3]
    ii = S.ticker.map(it).to_numpy()
    jj = np.array([idt.get(d, -1) for d in S.date.to_numpy()])
    ok = jj >= 0
    ii, jj = ii[ok], jj[ok]
    o = np.argsort(jj, kind='stable')
    js, iss = jj[o], ii[o]
    b = np.flatnonzero(np.concatenate([[True], js[1:] != js[:-1], [True]]))
    d = {}
    for s, e in zip(b[:-1], b[1:]):
        aa = int(js[s])
        lay = LAYAK.get(aa)
        if lay is None:
            continue
        v = np.intersect1d(iss[s:e], lay)
        if v.size:
            d[aa] = v.astype('int64')
    return d


# ---------------------------------------------------------------- indeks
def siri_indeks(P, tk):
    """Buka dan tutup indeks `tk` dijajarkan ke P.tarikh (ffill tutup; buka = tutup jika tiada)."""
    ix = pd.read_parquet(PB.CACHE / 'idx.parquet')
    q = ix[ix.ticker == tk].sort_values('date').set_index('date')
    q = q.reindex(pd.DatetimeIndex(P.tarikh))
    assert q.open.notna().all() and q.close.notna().all(), f'{tk}: buka/tutup tiada pada tarikh panel'
    c = q.close.astype('float64')
    o = q.open.astype('float64')
    return o.to_numpy(), c.to_numpy()


def rejim_qqq(P):
    """ON[a] = QQQ tutup > SMA50 DAN SMA10 > SMA20 pada sauh a (SPEC_KAD_SKOR.md)."""
    _, c = siri_indeks(P, 'QQQ')
    s = pd.Series(c)
    on = (s > s.rolling(50).mean()) & (s.rolling(10).mean() > s.rolling(20).mean())
    return on.fillna(False).to_numpy()


# ---------------------------------------------------------------- simulasi
def simulasi(P, ATRP, CAL, IND, TO, TC, cfg, slot, benih, cache, rejim_on, m0, l0, l1):
    """Laluan ekuiti akaun 3 bahagian + rekod setiap dagangan satelit."""
    rng = np.random.default_rng(benih)
    m = len(P.tarikh)
    tunai, prev = 1.0, 1.0
    unit_teras = 0.0
    buka = []                       # (ti, unit, idx_keluar, px_keluar, idx_masuk, belanja, ind)
    ek = np.full(m, np.nan)
    dz = np.full(m, np.nan)
    nb = np.zeros(m, dtype='int32')
    bulan = pd.DatetimeIndex(P.tarikh).to_period('M')
    dag = []
    w_sat, w_teras = cfg['w_sat'], cfg['w_teras']
    cal_all = CAL.get(cfg['masuk']) if cfg['masuk'] else None
    for d in range(1, m):
        a = d - 1
        # 1. keluar satelit pada buka d
        if buka:
            for p in [x for x in buka if x[2] == d]:
                ko = K.kos_sisi(P.N[p[0], d])
                hasil = p[1] * p[3] * (1 - ko)
                tunai += hasil
                dag.append((p[4], d, int(p[0]), hasil / p[5] - 1.0, d - p[4],
                            bool(rejim_on[p[4] - 1])))
                buka.remove(p)
        # 2. imbang teras pada sesi pertama bulan (harga buka d)
        if w_teras > 0 and (d == 1 or bulan[d] != bulan[d - 1]):
            po = float(TO[d])
            if np.isfinite(po) and po > 0:
                nilai_teras = unit_teras * po
                sasar = w_teras * prev
                beza = sasar - nilai_teras
                if beza > 0:
                    beli = min(beza, tunai)
                    unit_teras += beli * (1 - KOS_TERAS) / po
                    tunai -= beli
                elif beza < 0:
                    jual_unit = -beza / po
                    unit_teras -= jual_unit
                    tunai += jual_unit * po * (1 - KOS_TERAS)
        # 3. belian satelit pada buka d bagi isyarat sauh a
        if w_sat > 0 and cal_all is not None and len(buka) < slot and \
                (not cfg['rejim'] or rejim_on[a]):
            cal = cal_all.get(a)
            if cal is not None and cal.size:
                if cfg['urut'] == 'U01':
                    cal = cal[rng.permutation(cal.size)]
                else:
                    cal = cal[np.argsort(np.nan_to_num(ATRP[cal, a], nan=9e9), kind='stable')]
                pegang = {x[0] for x in buka}
                ind_pegang = {x[6] for x in buka}
                for t in cal:
                    if len(buka) >= slot:
                        break
                    ti = int(t)
                    if ti in pegang:
                        continue
                    if cfg['had_ind'] is not None and int(IND[ti]) in ind_pegang:
                        continue
                    belanja = min(w_sat * prev / slot, tunai)
                    if belanja <= 1e-12:
                        break
                    kx, _, pkeluar = S24.keluar(P, None, ti, a, RULE, CAP, cache)
                    # kx <= d mustahil bagi X15; kx - d > CAP = fallback tutup-terakhir step24
                    # (buka bar keluar tiada) yang melanggar had SOP -> langkau (semakan kod 9 Nov)
                    if kx <= d or kx - d > CAP:
                        continue
                    unit = belanja * (1 - K.kos_sisi(P.N[ti, a])) / float(P.O[ti, d])
                    tunai -= belanja
                    buka.append((ti, unit, kx, pkeluar, d, belanja, int(IND[ti])))
                    pegang.add(ti)
                    ind_pegang.add(int(IND[ti]))
        # 4. tanda pada tutup d
        nilai = tunai + unit_teras * float(TC[d])
        sat = 0.0
        for ti, unit, _, _, _, _, _ in buka:
            c = P.C[ti, d]
            if np.isfinite(c):
                sat += unit * float(c)
        nilai += sat
        assert tunai > -1e-9, f'tunai negatif {tunai} pada d={d}'
        assert nilai > 0, f'ekuiti <= 0 pada d={d}'
        ek[d] = prev = nilai
        dz[d] = sat / nilai
        nb[d] = len(buka)
    D = pd.DataFrame(dag, columns=['i_masuk', 'i_keluar', 'ti', 'pul', 'pegang', 'rejim_on'])
    return ek, dz, nb, D


def ukur(ek, hari, i0, i1):
    e = ek[i0:i1]
    return PB.cagr(e, hari[i0:i1]), PB.mdd(e)


def stat_dag(D, i0, i1):
    x = D[(D.i_masuk >= i0) & (D.i_masuk < i1)]
    if x.empty:
        return dict(n=0, pul=np.nan, menang=np.nan, untung=np.nan, rugi=np.nan, payoff=np.nan,
                    tanpa5=np.nan, pegang=np.nan)
    r = x.pul.to_numpy() * 100
    pos, neg = r[r > 0], r[r <= 0]
    k = int(np.ceil(len(r) * 0.05))
    tanpa5 = float(np.sort(r)[:-k].mean()) if k and len(r) > k else np.nan
    return dict(n=len(r), pul=float(r.mean()), menang=float(len(pos) / len(r) * 100),
                untung=float(pos.mean()) if pos.size else np.nan,
                rugi=float(neg.mean()) if neg.size else np.nan,
                payoff=float(pos.mean() / abs(neg.mean())) if pos.size and neg.size else np.nan,
                tanpa5=tanpa5, pegang=float(x.pegang.mean()))


# ---------------------------------------------------------------- ujian asap (spec §6)
def semak_dagangan(P, D):
    """Bilangan pelanggaran integriti: keluar <= masuk, atau pulangan tidak sepadan dengan kiraan
    semula bebas buka->buka ticker SAMA dengan kos penuh."""
    n = 0
    for r in D.itertuples():
        e, kx, ti = int(r.i_masuk), int(r.i_keluar), int(r.ti)
        if kx <= e:
            n += 1
            continue
        kasar = float(P.O[ti, kx]) / float(P.O[ti, e])
        bersih = kasar * (1 - K.kos_sisi(P.N[ti, e - 1])) * (1 - K.kos_sisi(P.N[ti, kx])) - 1
        if abs(bersih - r.pul) > 1e-6:
            n += 1
    return n


def semak_chandelier(P, D):
    """Bilangan dagangan yang keluarnya dicetus pada bar masuk itu sendiri (mod kegagalan X25):
    pegang == 1 selain hujung data, atau paras Chandelier pada bar masuk sudah di atas tutup
    (C[e] < C[e] - 4*ATR[a], hanya mungkin jika ATR rosak/negatif)."""
    akhir = len(P.tarikh) - 1
    n = 0
    for r in D.itertuples():
        e, kx, ti = int(r.i_masuk), int(r.i_keluar), int(r.ti)
        if kx - e == 1 and kx < akhir:
            n += 1
            continue
        c, atr = float(P.C[ti, e]), float(P.A[ti, e - 1])
        if c < c - 4 * atr:
            n += 1
    return n


def asap(P, ATRP, CAL, IND, TO, TC, rejim_on, m0, l0, l1):
    print('UJIAN ASAP (spec §6)', flush=True)
    hari = pd.DatetimeIndex(P.tarikh)
    gagal = []
    # 1. K0 lawan teras-sahaja analitik: unit teras diimbang bulanan tanpa satelit
    cache = {}
    ek, dz, nb, D = simulasi(P, ATRP, CAL, IND, TO, TC, LENGAN['K0'], 8, 0, cache, rejim_on,
                             m0, l0, l1)
    assert D.empty and nb.max() == 0
    # analitik: laluan yang sama dikira semula secara bebas
    tunai, unit, prev = 1.0, 0.0, 1.0
    bulan = hari.to_period('M')
    ek2 = np.full(len(P.tarikh), np.nan)
    for d in range(1, len(P.tarikh)):
        if d == 1 or bulan[d] != bulan[d - 1]:
            sasar = W_TERAS * prev
            beza = sasar - unit * TO[d]
            if beza > 0:
                unit += beza * (1 - KOS_TERAS) / TO[d]; tunai -= beza
            else:
                unit -= -beza / TO[d]; tunai += -beza * (1 - KOS_TERAS)
        ek2[d] = prev = tunai + unit * TC[d]
    beza = np.nanmax(np.abs(ek / ek2 - 1)) * 100
    print(f'  1. K0 lawan analitik: beza maks {beza:.4f}%', flush=True)
    if beza > 0.05:
        gagal.append('asap1')
    # 2–4. S1 slot 8: integriti dagangan dan kekangan
    cache = {}
    ek, dz, nb, D = simulasi(P, ATRP, CAL, IND, TO, TC, LENGAN['S1'], 8, 0, cache, rejim_on,
                             m0, l0, l1)
    assert (D.i_keluar > D.i_masuk).all(), 'keluar <= masuk'
    assert (D.pegang >= 1).all(), 'pegang 0'
    assert nb.max() <= 8, 'posisi > slot'
    assert (D.pegang <= CAP).all(), 'pegang > CAP (fallback tutup-terakhir)'
    # 2. mod kegagalan X25 (keluar dicetus pada bar masuk) atas SEMUA dagangan; bilangan paras
    # Chandelier di atas buka masuk pada bar masuk (tutup melonjak > 4 ATR) dilapor sebagai
    # maklumat sahaja — ia untung terkunci, bukan pepijat (pindaan spec §6.2, 9 Nov 2026)
    n_x25 = semak_chandelier(P, D)
    n_atas = int(sum(float(P.C[int(r.ti), int(r.i_masuk)]) - 4 * float(P.A[int(r.ti), int(r.i_masuk) - 1])
                     >= float(P.O[int(r.ti), int(r.i_masuk)]) for r in D.itertuples()))
    assert all(rejim_on[int(e) - 1] for e in D.i_masuk), 'belian pada sauh OFF dalam lengan rejim'
    print(f'  2. keluar dicetus pada bar masuk (X25): {n_x25}/{len(D)} (mesti 0); keluar <= masuk: 0; '
          f'pegang 0: 0; pegang > {CAP}: 0; [maklumat] paras trailing di atas buka masuk pada bar '
          f'masuk: {n_atas}/{len(D)}', flush=True)
    # 3. SEMUA dagangan dikira semula bebas (buka->buka ticker sama, kos penuh)
    n_salah = semak_dagangan(P, D)
    print(f'  3. {len(D)} dagangan dikira semula bebas: {n_salah} tidak sepadan (mesti 0)', flush=True)
    if n_x25 or n_salah:
        gagal.append('asap2/3')
    # 4. had industri: tiada dua posisi industri sama pada mana-mana hari -> semak semula
    # dengan simulasi ringkas: jejak set industri terbuka
    buka_ind = {}
    langgar = 0
    rows = D.sort_values('i_masuk')
    for r in rows.itertuples():
        # buang yang sudah keluar sebelum/pada masuk ini
        for k in [k for k, v in buka_ind.items() if v <= r.i_masuk]:
            del buka_ind[k]
        g = int(IND[int(r.ti)])
        if g in buka_ind:
            langgar += 1
        buka_ind[g] = int(r.i_keluar)
    print(f'  4. pelanggaran had 1 industri: {langgar} (mesti 0); tunai/ekuiti disemak oleh '
          f'assert dalam simulasi', flush=True)
    if langgar:
        gagal.append('asap4')
    # 5. ujian mesti boleh gagal: rekod rosak (keluar = masuk, pulangan diubah) dan ATR dipaksa
    # negatif (paras Chandelier di atas tutup masuk) mesti dikesan oleh pemeriksa SAMA langkah 2–3
    rosak = D.head(5).copy()
    rosak['i_keluar'] = rosak['i_masuk']
    rosak['pul'] = rosak['pul'] + 0.01
    n1 = semak_dagangan(P, rosak)
    A_asal = P.A.copy()
    P.A[:] = -np.abs(P.A)
    n2 = semak_chandelier(P, D.head(5))
    P.A[:] = A_asal
    print(f'  5. rekod rosak sengaja dikesan: pulangan/keluar {n1}/5, paras di atas masuk {n2}/5 '
          f'(mesti 5 dan 5)', flush=True)
    if n1 < 5 or n2 < 5:
        gagal.append('asap5')
    if gagal:
        print(f'UJIAN ASAP GAGAL: {gagal} — keputusan TIDAK dilaporkan', flush=True)
        return False
    print('UJIAN ASAP LULUS', flush=True)
    return True


# ---------------------------------------------------------------- larian
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--asap', action='store_true', help='ujian asap sahaja')
    ap.add_argument('--benih', type=int, default=N_BENIH)
    ap.add_argument('--laporan-sahaja', action='store_true')
    a = ap.parse_args(argv)
    f = KELUAR / 'satelit.csv'
    fd = KELUAR / 'satelit_dagangan.csv'
    if a.laporan_sahaja and f.exists():
        return laporan(pd.read_csv(f), pd.read_csv(fd, parse_dates=['tarikh_masuk']))

    t0 = time.time()
    print('1/5 isyarat GB02_atau3...', flush=True)
    S = bina_isyarat()
    print(f'  {len(S):,} bar berisyarat  [{time.time() - t0:.0f}s]', flush=True)
    print('2/5 panel harga...', flush=True)
    P = PB.Panel()
    ATRP = P.A / np.where(P.C > 0, P.C, np.nan)
    LAYAK = S22.peta_layak(P)
    CAL = {'RAWAK': LAYAK, 'GB02_atau3': calon_gb02(P, S, LAYAK)}
    IND, n_ind, n_tiada = S28.peta_industri(P)
    TO, TC = siri_indeks(P, 'SPY')
    rejim_on = rejim_qqq(P)
    hari = pd.DatetimeIndex(P.tarikh)
    m0 = int(np.searchsorted(P.tarikh, np.datetime64(UJI0)))
    m1 = int(np.searchsorted(P.tarikh, np.datetime64(UJI1), side='right'))
    l0 = int(np.searchsorted(P.tarikh, np.datetime64(LATIH0)))
    l1 = int(np.searchsorted(P.tarikh, np.datetime64(LATIH1), side='right'))
    print(f'  {len(P.tick):,} ticker x {len(P.tarikh):,} sesi; {n_ind} industri '
          f'({n_tiada} tanpa); rejim ON {rejim_on[m0:m1].mean() * 100:.0f}% sesi tahan, '
          f'{rejim_on[l0:l1].mean() * 100:.0f}% latih; calon GB02 '
          f'{sum(v.size for v in CAL["GB02_atau3"].values()):,}  [{time.time() - t0:.0f}s]',
          flush=True)

    print('3/5 ujian asap...', flush=True)
    if not asap(P, ATRP, CAL, IND, TO, TC, rejim_on, m0, l0, l1):
        return 1
    if a.asap:
        return 0

    print('4/5 simulasi...', flush=True)
    baris, dags = [], []
    cache = {}
    for nama, cfg in LENGAN.items():
        slots = [8] if cfg['w_sat'] == 0 else SLOT
        for slot in slots:
            benih = range(1, a.benih + 1) if cfg['urut'] == 'U01' else [0]
            for bn in benih:
                if len(cache) > 4_000_000:
                    cache.clear()
                ek, dz, nb, D = simulasi(P, ATRP, CAL, IND, TO, TC, cfg, slot, bn, cache,
                                         rejim_on, m0, l0, l1)
                ct, mt = ukur(ek, hari, m0, m1)
                cl, ml = ukur(ek, hari, l0, l1)
                st, sl = stat_dag(D, m0, m1), stat_dag(D, l0, l1)
                tahun = (hari[m1 - 1] - hari[m0]).days / 365.25
                baris.append(dict(lengan=nama, slot=slot, benih=bn, cagr=ct, mdd=mt,
                                  cagr_latih=cl, mdd_latih=ml,
                                  dedah_sat=float(np.nanmean(dz[m0:m1]) * 100),
                                  n_dag=st['n'], pul_dag=st['pul'], menang=st['menang'],
                                  untung=st['untung'], rugi=st['rugi'], payoff=st['payoff'],
                                  tanpa5=st['tanpa5'], pegang=st['pegang'],
                                  pusing=st['n'] / slot / tahun if cfg['w_sat'] else 0.0,
                                  n_dag_latih=sl['n'], pul_dag_latih=sl['pul'],
                                  menang_latih=sl['menang']))
                if cfg['w_sat'] and (cfg['urut'] == 'U08' or bn == 1):
                    D = D.assign(lengan=nama, slot=slot, benih=bn,
                                 tarikh_masuk=hari[D.i_masuk.to_numpy()],
                                 ticker=P.tick[D.ti.to_numpy()])
                    dags.append(D)
            print(f'  {nama} slot {slot}: siap  [{time.time() - t0:.0f}s]', flush=True)
    R = pd.DataFrame(baris)
    R.to_csv(f, index=False, float_format='%.4f')
    DG = pd.concat(dags, ignore_index=True)
    DG.to_csv(fd, index=False, float_format='%.6f')
    print('5/5 laporan...', flush=True)
    return laporan(R, DG)


# ---------------------------------------------------------------- laporan
def _camp_spus(w):
    s = pd.read_csv(SPUS_BULANAN, comment='#')
    s['bulan'] = pd.PeriodIndex(s.bulan, freq='M')
    s = s[(s.bulan >= pd.Period('2019-12')) & (s.bulan <= pd.Period('2025-12'))]
    r = s.tutup.pct_change().dropna().to_numpy() * w
    e = np.concatenate([[1.0], np.cumprod(1 + r)])
    th = len(r) / 12
    return float(((e[-1]) ** (1 / th) - 1) * 100), PB.mdd(e)


def laporan(R, DG):
    g = (R.groupby(['lengan', 'slot'])
          .agg(cagr=('cagr', 'median'), mdd=('mdd', 'median'),
               cagr_p5=('cagr', lambda x: float(np.percentile(x, 5))),
               cagr_p95=('cagr', lambda x: float(np.percentile(x, 95))),
               cagr_latih=('cagr_latih', 'median'), mdd_latih=('mdd_latih', 'median'),
               dedah_sat=('dedah_sat', 'median'), n_dag=('n_dag', 'median'),
               pul_dag=('pul_dag', 'median'), menang=('menang', 'median'),
               untung=('untung', 'median'), rugi=('rugi', 'median'),
               payoff=('payoff', 'median'), tanpa5=('tanpa5', 'median'),
               pegang=('pegang', 'median'), pusing=('pusing', 'median'),
               pul_dag_latih=('pul_dag_latih', 'median'), nb=('benih', 'size'))
          .reset_index())
    g['nisbah'] = g.cagr / g.mdd.abs()
    g['nisbah_latih'] = g.cagr_latih / g.mdd_latih.abs()
    g['pada_mdd10'] = g.cagr * np.minimum(1.0, 10.0 / g.mdd.abs())
    g.to_csv(KELUAR / 'satelit_ringkas.csv', index=False, float_format='%.4f')

    def sel(n, s=8):
        return g[(g.lengan == n) & (g.slot == s)].iloc[0]
    K1 = sel('K1'); K0 = sel('K0')
    gate = {}
    for s in SLOT:
        S1, R1, R2 = sel('S1', s), sel('R1', s), sel('R2', s)
        P1 = (S1.cagr > K1.cagr) and (S1.cagr_latih > K1.cagr_latih)
        P2 = (S1.mdd >= MDD_HAD) and (S1.mdd >= K1.mdd - 1.0) and (S1.mdd_latih >= K1.mdd_latih - 1.0)
        P3 = (S1.cagr > R1.cagr_p95) and (S1.cagr > R2.cagr)
        P4 = (S1.nisbah > K1.nisbah) and (S1.nisbah_latih > K1.nisbah_latih)
        P5 = (S1.pul_dag > 0) and (S1.pul_dag_latih > 0) and (S1.pul_dag > R1.pul_dag)
        gate[s] = dict(P1=bool(P1), P2=bool(P2), P3=bool(P3), P4=bool(P4), P5=bool(P5))
        gate[s]['LULUS'] = all(gate[s].values())
    sp35, sp50 = _camp_spus(0.35), _camp_spus(0.50)

    L = ['# SATELIT — GB02_atau3 × Chandelier 15% akaun di atas teras indeks 35% + tunai', '']
    L.append(f'Dijana {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC oleh `REVERSE/step41_satelit.py`. '
             'Pradaftar `REVERSE/SPEC_SATELIT.md` (dikomit sebelum larian). Alam A02 cair, kos penuh, '
             f'teras SPY (proksi, spec §2), tahan {UJI0[:4]}–{UJI1[:4]}, latih {LATIH0[:4]}–{LATIH1[:4]}. '
             'Rekod analisis sahaja: tiada order, tiada wang sebenar.')
    L.append('')
    v = 'LULUS' if gate[8]['LULUS'] else 'GAGAL'
    L.append(f'## Keputusan sel utama `S1` slot 8: **{v}** — ' +
             ' · '.join(f'{k} {"✓" if x else "✗"}' for k, x in gate[8].items() if k != 'LULUS'))
    L.append(f'Slot 10: ' + ' · '.join(f'{k} {"✓" if x else "✗"}' for k, x in gate[10].items()))
    L.append('')
    L.append('Gate (spec §4): P1 CAGR > `K1` dua tingkap · P2 MDD tahan ≥ -10% dan ≥ `K1` − 1 mata '
             'dua tingkap · P3 CAGR > p95 `R1` dan > `R2` · P4 nisbah > `K1` dua tingkap · '
             'P5 purata dagangan > 0 dua tingkap dan > `R1`.')
    L.append('')
    L.append('## Jadual lengan (median benih; tahan 2020–2025 | latih 2012–2019)')
    L.append('')
    L.append('| Lengan | Slot | Benih | CAGR % | p5–p95 | MDD % | Nisbah | Pada MDD -10% | CAGR latih % | MDD latih % | Dedah satelit % | Dagangan | Pul/dagangan % | Menang % | Untung % | Rugi % | Payoff | tanpa5 % | Pegang bar | Pusing/slot/thn |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for r in g.sort_values(['lengan', 'slot']).itertuples():
        p = f'{r.cagr_p5:+.1f}–{r.cagr_p95:+.1f}' if r.nb > 1 else '–'
        L.append(f'| `{r.lengan}` | {r.slot} | {r.nb} | {r.cagr:+.2f} | {p} | {r.mdd:.2f} | {r.nisbah:.2f} | '
                 f'{r.pada_mdd10:+.2f} | {r.cagr_latih:+.2f} | {r.mdd_latih:.2f} | {r.dedah_sat:.1f} | '
                 f'{r.n_dag:.0f} | {r.pul_dag:+.2f} | {r.menang:.1f} | {r.untung:+.2f} | {r.rugi:+.2f} | '
                 f'{r.payoff:.2f} | {r.tanpa5:+.2f} | {r.pegang:.1f} | {r.pusing:.1f} |')
    L.append('')
    L.append('## Rujukan pasif')
    L.append('')
    L.append(f'- `K0` teras SPY 35% + tunai: CAGR {K0.cagr:+.2f}% / MDD {K0.mdd:.2f}% (tahan); '
             f'{K0.cagr_latih:+.2f}% / {K0.mdd_latih:.2f}% (latih).')
    L.append(f'- `K1` teras SPY 50% + tunai: CAGR {K1.cagr:+.2f}% / MDD {K1.mdd:.2f}% (tahan); '
             f'{K1.cagr_latih:+.2f}% / {K1.mdd_latih:.2f}% (latih).')
    L.append(f'- SPUS bulanan + tunai 2020–2025 (maklumat, konvensyen `SISTEM.md`): 35% → '
             f'{sp35[0]:+.2f}% / {sp35[1]:.2f}%; 50% → {sp50[0]:+.2f}% / {sp50[1]:.2f}%.')
    L.append('')
    # dagangan ikut rejim (S2, slot 8)
    x = DG[(DG.lengan == 'S2') & (DG.slot == 8)]
    if len(x):
        L.append('## Dagangan satelit ikut rejim pada hari masuk (`S2`, tanpa penapis rejim, slot 8, tahan)')
        L.append('')
        L.append('| Rejim | Dagangan | Pul/dagangan % | Menang % | Untung % | Rugi % | Pegang bar |')
        L.append('|---|---|---|---|---|---|---|')
        hari0 = pd.Timestamp(UJI0)
        xt = x[x.tarikh_masuk >= hari0]
        for lab, sub in (('ON', xt[xt.rejim_on]), ('OFF', xt[~xt.rejim_on])):
            if len(sub):
                r = sub.pul.to_numpy() * 100
                pos, neg = r[r > 0], r[r <= 0]
                L.append(f'| {lab} | {len(r)} | {r.mean():+.2f} | {len(pos) / len(r) * 100:.1f} | '
                         f'{pos.mean() if pos.size else np.nan:+.2f} | {neg.mean() if neg.size else np.nan:+.2f} | '
                         f'{sub.pegang.mean():.1f} |')
        L.append('')
    L.append('## Jangkaan priori (spec §7) lawan keputusan')
    L.append('')
    L.append(f'- P2 lulus nipis: **{"betul" if gate[8]["P2"] else "salah"}**; P1 gagal latih: '
             f'**{"betul" if not (sel("S1").cagr_latih > K1.cagr_latih) else "salah"}**; P3 lulus: '
             f'**{"betul" if gate[8]["P3"] else "salah"}**; P5 lulus: **{"betul" if gate[8]["P5"] else "salah"}**; '
             f'keseluruhan GAGAL: **{"betul" if not gate[8]["LULUS"] else "salah"}**.')
    L.append('')
    L.append('## Had')
    L.append('')
    L.append('- Alam A02 tiada saham delist: CAGR satelit condong ke atas. Kolam GB02 dan keluar X15 dipilih '
             'daripada data yang sama. Teras SPY ialah proksi SPUS (SPUS tiada 2012–2019 dan tiada harian dalam repo); '
             'SPUS mengalahkan SPY 2020–2025, jadi alternatif pasif sebenar lebih kuat daripada `K1` di sini. '
             '`CARA` kekal `C01`. Tiada impak pasaran dalam kos. Tiada dakwaan +10%/bulan.')
    (KELUAR / 'SATELIT.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('\n'.join(L[:8]))
    print(g[['lengan', 'slot', 'nb', 'cagr', 'mdd', 'nisbah', 'cagr_latih', 'mdd_latih', 'dedah_sat',
             'n_dag', 'pul_dag', 'menang', 'payoff']].to_string(index=False, float_format=lambda v: f'{v:.2f}'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
