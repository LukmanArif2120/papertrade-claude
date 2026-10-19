# Kajian portfolio modal terhad (19 Okt 2026; laporan kajian/KAJIAN_PORTFOLIO.md).
# Soalan: Papertrade C membeli setiap isyarat (~800 sehari). Dengan modal sebenar 10 slot (10% ekuiti setiap satu),
# isyarat mana patut diambil apabila isyarat lebih banyak daripada slot kosong?
# Calon = semua dagangan enjin v1.2 134 kaedah (set 431, data_mentah 2019–2026), dijana oleh kaji_lorong2.py jana.
# Dua cara keluar: L1 = peraturan kaedah (enjin), L2 = Chandelier tutup 4xATR14 paras naik tanpa henti (lorong 2 semasa).
# Semua ukuran pemilihan diambil pada tutup hari isyarat (tiada pandang hadapan), kecuali 'Kaedah statik' (rujukan sahaja).
# Guna (dari akar repo; perlu numba):
#   KAJIAN_LORONG2=<folder> python3 BacktestShariah2/kajian/lorong2/kaji_lorong2.py jana
#   git show origin/kajian-gred:BacktestShariah2/kajian/data/kumpulan_harian.csv.gz > <folder>/kumpulan_harian.csv.gz
#   KAJIAN_LORONG2=<folder> python3 BacktestShariah2/kajian/portfolio/kaji_portfolio.py sedia
#   KAJIAN_LORONG2=<folder> python3 BacktestShariah2/kajian/portfolio/kaji_portfolio.py semak   -> enjin.portfolio = enjin kajian
#   KAJIAN_LORONG2=<folder> python3 BacktestShariah2/kajian/portfolio/kaji_portfolio.py sim
#   KAJIAN_LORONG2=<folder> python3 BacktestShariah2/kajian/portfolio/kaji_portfolio.py ringkas
import argparse, glob, os, pickle, sys
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'lorong2'))
from kaji_lorong2 import AKAR, COST, KOD, OUT, muat, sim, tatasusunan  # noqa: E402

BS2 = os.path.join(AKAR, 'BacktestShariah2')
MULA = pd.Timestamp('2020-11-02')          # 12 bulan sejarah dagangan untuk skor kaedah walk-forward
H1_AKHIR = pd.Timestamp('2023-10-31')
SLOT, W = 10, 0.10
BENIH = 30
JAUH = np.datetime64('2100-01-01')


# ---------------------------------------------------------------- 1. calon + ukuran pada hari isyarat
def skor_industri(path, spy):
    """Gred Industri v2 (standard/gred_kumpulan.py siri) daripada indeks kumpulan harian cawangan kajian-gred."""
    K = pd.read_csv(path); K = K[K.jenis == 'Industri']; K['tarikh'] = pd.to_datetime(K.tarikh)
    I, M1, N = (K.pivot(index='tarikh', columns='nama', values=v) for v in ('indeks', 'm1m', 'n'))
    I = I.ffill(); ok = N >= 3
    rs = I.div(spy.reindex(I.index), axis=0); mrs = rs / rs.rolling(252).mean() - 1; ma = I.rolling(150).mean()
    w1 = (mrs > 0).astype(float).where(mrs.notna())
    w2 = (mrs > mrs.shift(21)).astype(float).where(mrs.notna() & mrs.shift(21).notna())
    w3 = ((I > ma) & (ma > ma.shift(20))).astype(float).where(mrs.notna() & ma.shift(20).notna())
    pk = lambda X: X.where(ok).rank(axis=1, pct=True)
    return 100 * pk((w1 + w2 + w3) / 3 + pk(M1))


def cmd_sedia(a):
    T = pd.concat([pickle.load(open(f, 'rb')) for f in sorted(glob.glob(f'{OUT}/T/*.pkl'))], ignore_index=True)
    T = T[T.ent >= pd.Timestamp('2019-11-01')].reset_index(drop=True)
    fr, idx = muat(); so, sc = idx['SPY'].open, idx['SPY'].close
    n = len(T); print('dagangan', n, 'kaedah', T.mid.nunique(), flush=True)
    F = {k: np.full(n, np.nan) for k in ('buka', 'ret2', 'mom126', 'mutlak12', 'mansfield', 'atrp')}
    ex2 = np.empty(n, 'datetime64[ns]'); akhir2 = np.zeros(n, bool)
    for t, G in T.groupby('ticker'):
        g = fr[t]; dts = g.index; o, h, l, c, A, we, pwc = tatasusunan(g)
        ks = dts.get_indexer(G.ent).astype(np.int64); ss = dts.get_indexer(G.sig); ix = G.index.to_numpy()
        J, X, Wk = sim(o, h, l, c, A['atr14'], we, pwc, ks, np.full(len(ks), np.nan), 6, 4.0, 1)
        F['buka'][ix] = o[ks]; F['ret2'][ix] = X / o[ks] * (1 - COST) / (1 + COST) - 1
        ex2[ix] = dts[J].values; akhir2[ix] = Wk == 2
        cl = g.close; rl = cl / sc.reindex(dts).ffill()
        F['mom126'][ix] = (cl / cl.shift(126) - 1).to_numpy()[ss]
        F['mutlak12'][ix] = (cl / cl.shift(252) - 1).to_numpy()[ss]
        F['mansfield'][ix] = (rl / rl.rolling(252).mean() - 1).to_numpy()[ss]
        pc = cl.shift(1); tr = pd.concat([g.high - g.low, (g.high - pc).abs(), (g.low - pc).abs()], axis=1).max(axis=1)
        F['atrp'][ix] = (tr.rolling(14).mean() / cl).to_numpy()[ss]
    for k, v in F.items(): T[k] = v
    T['ex2'] = ex2; T['akhir2'] = akhir2; T['akhir1'] = T.why.eq('hujung')
    cf = lambda d: sc.reindex(pd.DatetimeIndex(d), method='ffill').to_numpy()
    T['spy1'] = cf(T.ex) / so.reindex(T.ent).to_numpy() - 1
    T['spy2'] = cf(T.ex2) / so.reindex(T.ent).to_numpy() - 1
    T['spy_atas'] = (sc > sc.rolling(200).mean()).reindex(T.sig).to_numpy()
    rs = pd.read_csv(os.path.join(BS2, 'kajian', 'rs', 'rs_pasaran_431.csv.gz'))
    rs['sig'] = pd.to_datetime(rs.date.astype(str)); rs = rs.rename(columns={'rs_pasaran': 'rs'})[['sig', 'ticker', 'rs']]
    T = T.merge(rs, on=['sig', 'ticker'], how='left')
    peta = pd.read_csv(os.path.join(BS2, 'papertrade', 'peta_industri.csv')).drop_duplicates('ticker').set_index('ticker').industri
    S = skor_industri(a.kumpulan, sc).stack().rename('ind_skor').reset_index().rename(columns={'tarikh': 'sig', 'nama': 'industri'})
    T['industri'] = T.ticker.map(peta)
    T = T.merge(S, on=['sig', 'industri'], how='left')
    T['konsensus'] = T.groupby(['ticker', 'sig']).mid.transform('nunique')
    T.drop(columns=['mfe'], errors='ignore').to_pickle(f'{OUT}/calon.pkl')
    print('liputan: rs %.1f%%, industri %.1f%%, mansfield %.1f%%' % tuple(100 * T[k].notna().mean() for k in ('rs', 'ind_skor', 'mansfield')))


# ---------------------------------------------------------------- 2. enjin portfolio slot
def portfolio(ent_i, ex_i, ret, tk, e_open, susun, Cm, slots=SLOT, w=W):
    """Ikut enjin.portfolio v1.2: keluar direalisasi dahulu; masuk ikut susunan skor; satu posisi bagi setiap saham;
    saiz = min(tunai, ekuiti semalam x w). Nilai pasaran = saiz x tutup / buka masuk."""
    nd = Cm.shape[0]; cash = eq = 1.0; pos = []; held = set(); curve = np.empty(nd); npos = np.empty(nd); ambil = []
    for d in range(nd):
        keep = []
        for q, am in pos:
            if ex_i[q] == d: cash += am * (1 + ret[q]); held.discard(tk[q])
            else: keep.append((q, am))
        pos = keep
        for q in susun[d]:
            if len(pos) >= slots: break
            if tk[q] in held: continue
            am = min(cash, eq * w)
            if am <= 1e-12: break
            cash -= am; pos.append((q, am)); held.add(tk[q]); ambil.append(q)
        keep = []
        for q, am in pos:
            if ex_i[q] == d and ent_i[q] == d: cash += am * (1 + ret[q]); held.discard(tk[q])
            else: keep.append((q, am))
        pos = keep
        eq = cash + sum(am * Cm[d, tk[q]] / e_open[q] for q, am in pos); curve[d] = eq; npos[d] = len(pos)
    return curve, npos, np.array(ambil, int)


class Pasar:
    def __init__(self, T, fr, mula=MULA):
        self.hari = pd.DatetimeIndex(sorted(set().union(*[g.index for g in fr.values()])))
        self.hari = self.hari[self.hari >= mula]
        self.tick = sorted(fr); tid = {t: i for i, t in enumerate(self.tick)}
        self.Cm = pd.concat([fr[t].close.rename(t) for t in self.tick], axis=1).reindex(self.hari).ffill().to_numpy()
        self.pilih = (T.ent >= mula).to_numpy(); self.T = T[self.pilih].reset_index(drop=True)
        self.tk = self.T.ticker.map(tid).to_numpy(); self.e_open = self.T.buka.to_numpy()
        self.ent_i = self.hari.get_indexer(self.T.ent)
        cap = lambda d: np.minimum(self.hari.searchsorted(pd.DatetimeIndex(d)), len(self.hari) - 1)
        self.ex_i = {1: cap(self.T.ex), 2: cap(self.T.ex2)}
        self.ret = {1: self.T.ret.to_numpy(float), 2: self.T.ret2.to_numpy(float)}

    def jalan(self, L, skor, tapis=None, benih=0, slots=SLOT, w=W):
        ok = np.ones(len(self.T), bool) if tapis is None else np.asarray(tapis, bool)
        q = np.flatnonzero(ok & (self.ent_i >= 0))
        bunyi = np.random.default_rng(benih).random(len(q))
        q = q[np.lexsort((bunyi, -np.nan_to_num(np.asarray(skor, float)[q], nan=-1e18), self.ent_i[q]))]
        cut = np.searchsorted(self.ent_i[q], np.arange(len(self.hari) + 1))
        susun = [q[cut[d]:cut[d + 1]] for d in range(len(self.hari))]
        cv, npos, ambil = portfolio(self.ent_i, self.ex_i[L], self.ret[L], self.tk, self.e_open, susun, self.Cm, slots, w)
        return pd.Series(cv, self.hari), npos, ambil


def cagr(s):
    y = (s.index[-1] - s.index[0]).days / 365.25; return (s.iloc[-1] / s.iloc[0]) ** (1 / y) - 1


def metrik(cv, npos, P, L, ambil):
    T = P.T.iloc[ambil]; r = P.ret[L][ambil]; ex = r - T[f'spy{L}'].to_numpy()
    h1 = cv[cv.index <= H1_AKHIR]; h2 = cv[cv.index > H1_AKHIR]
    mdd = (cv / cv.cummax() - 1).min(); c = cagr(cv)
    hari = (P.ex_i[L][ambil] - P.ent_i[ambil] + 1)
    return dict(cagr=c, mdd=mdd, mar=c / abs(mdd), h1=cagr(h1), h2=cagr(pd.concat([h1.iloc[-1:], h2])),
                n=len(ambil), menang=(r > 0).mean(), purata=r.mean(), lebih_spy=np.nanmean(ex), hari=hari.mean(),
                slot=npos.mean())


def skor_wf(T, L, hari=365, nmin=10):
    """Purata lebihan SPY dagangan kaedah (cara keluar L) yang sudah keluar dalam 12 bulan sebelum tutup hari isyarat."""
    ex = T[f'ex{L}' if L == 2 else 'ex'].to_numpy('datetime64[ns]').copy(); ex[T[f'akhir{L}'].to_numpy()] = JAUH
    x = (T['ret' if L == 1 else 'ret2'] - T[f'spy{L}']).to_numpy(float); s = T.sig.to_numpy('datetime64[ns]')
    out = np.full(len(T), np.nan)
    for _, ix in T.groupby('mid').indices.items():
        o = np.argsort(ex[ix]); e = ex[ix][o]; cs = np.r_[0.0, np.cumsum(np.nan_to_num(x[ix][o]))]
        hi = np.searchsorted(e, s[ix], 'right'); lo = np.searchsorted(e, s[ix] - np.timedelta64(hari, 'D'), 'right')
        k = hi - lo; v = (cs[hi] - cs[lo]) / np.maximum(k, 1); v[k < nmin] = np.nan; out[ix] = v
    return out


def peraturan(T, L):
    pk = lambda v: pd.Series(v).rank(pct=True).to_numpy()
    wf = skor_wf(T, L)
    x = (T['ret' if L == 1 else 'ret2'] - T[f'spy{L}'])
    statik = T.mid.map(x.groupby(T.mid).mean()).to_numpy()
    rs = T.rs.fillna(50).to_numpy(); ind = T.ind_skor.fillna(50).to_numpy()
    sah = ((T.rs >= 80) & (T.mutlak12 > 0) & (T.mansfield > 0) & T.spy_atas.astype(bool)).to_numpy()
    gab = (pk(np.nan_to_num(wf)) + pk(rs) + pk(ind) + pk(T.konsensus.to_numpy())) / 4
    return {'Konsensus kaedah': T.konsensus.to_numpy(float), 'RS pasaran': rs, 'RS disahkan dahulu': rs + 100 * sah,
            'Industri v2': ind, 'Kaedah walk-forward 12 bulan': np.nan_to_num(wf), 'Momentum 6 bulan': T.mom126.to_numpy(),
            'Volatiliti rendah (ATR%)': -T.atrp.to_numpy(), 'Volatiliti tinggi (ATR%)': T.atrp.to_numpy(),
            'Gabungan (kaedah WF + RS + industri + konsensus)': gab,
            'Kaedah statik (pandang hadapan, rujukan)': statik}


def cmd_semak(a):
    """Enjin kajian lawan enjin.portfolio (8 slot x 12.5%, susun rank) bagi beberapa kaedah: CAGR mesti hampir sama."""
    sys.path.insert(0, KOD); import enjin
    T = pd.read_pickle(f'{OUT}/calon.pkl'); fr, _ = muat()
    for mid in a.kaedah:
        Tm = T[T.mid == mid].reset_index(drop=True)
        ref = enjin.portfolio(Tm.assign(ret=Tm.ret), fr, slots=8, w=0.125)
        P = Pasar(Tm, fr, mula=pd.Timestamp(enjin.START))
        cv, _, _ = P.jalan(1, P.T['rank'].to_numpy(float), slots=8, w=0.125)
        print(mid, 'enjin.portfolio CAGR %.4f | kajian %.4f' % (cagr(ref), cagr(cv)), flush=True)


def cmd_sim(a):
    T = pd.read_pickle(f'{OUT}/calon.pkl'); fr, idx = muat(); P = Pasar(T, fr)
    rejim = P.T.spy_atas.astype(bool).to_numpy(); rows = []; kurva = {}
    for L in (1, 2):
        R = {k: v[P.pilih] for k, v in peraturan(T, L).items()}      # skor walk-forward guna sejarah sebelum MULA
        for rj in (False, True):
            tp = rejim if rj else None
            for b in range(BENIH):
                cv, npos, ambil = P.jalan(L, np.zeros(len(P.T)), tp, benih=b)
                rows.append(dict(peraturan='Rawak', benih=b, L=L, rejim=rj, slot_n=SLOT, **metrik(cv, npos, P, L, ambil)))
            for nama, sk in R.items():
                cv, npos, ambil = P.jalan(L, sk, tp)
                rows.append(dict(peraturan=nama, benih=-1, L=L, rejim=rj, slot_n=SLOT, **metrik(cv, npos, P, L, ambil)))
                kurva[(nama, L, rj)] = cv
            print('L', L, 'rejim', rj, 'siap', flush=True)
        for slots in (5, 20):
            for nama in ('Rawak', 'Kaedah walk-forward 12 bulan', 'Gabungan (kaedah WF + RS + industri + konsensus)', 'RS pasaran'):
                for b in (range(10) if nama == 'Rawak' else [0]):
                    sk = np.zeros(len(P.T)) if nama == 'Rawak' else R[nama]
                    cv, npos, ambil = P.jalan(L, sk, None, benih=b, slots=slots, w=1 / slots)
                    rows.append(dict(peraturan=nama, benih=b if nama == 'Rawak' else -1, L=L, rejim=False, slot_n=slots,
                                     **metrik(cv, npos, P, L, ambil)))
    D = pd.DataFrame(rows); D.to_pickle(f'{OUT}/portfolio.pkl')
    spy = idx['SPY'].close; spy = spy[spy.index >= MULA]; kurva[('SPY', 0, False)] = spy / spy.iloc[0]
    pickle.dump(kurva, open(f'{OUT}/kurva.pkl', 'wb'))


# ---------------------------------------------------------------- 3. ringkasan
def cmd_ringkas(a):
    D = pd.read_pickle(f'{OUT}/portfolio.pkl'); kurva = pickle.load(open(f'{OUT}/kurva.pkl', 'rb'))
    spy = kurva[('SPY', 0, False)]; h1 = spy[spy.index <= H1_AKHIR]
    print('SPY CAGR %.1f%% | H1 %.1f%% | H2 %.1f%% | MDD %.1f%%' % (100 * cagr(spy), 100 * cagr(h1),
          100 * cagr(spy[spy.index >= h1.index[-1]]), 100 * (spy / spy.cummax() - 1).min()))
    pd.set_option('display.width', 250)
    out = os.path.join(BS2, 'kajian', 'portfolio'); B = []
    for (L, rj, sn), G in D.groupby(['L', 'rejim', 'slot_n']):
        r = G[G.peraturan == 'Rawak']
        if r.empty: continue
        lain = G[G.peraturan != 'Rawak'].copy()
        for k in ('cagr', 'mar', 'h1', 'h2'):
            lain[f'{k}_pct_rawak'] = [100 * (r[k] < v).mean() for v in lain[k]]
        rw = r.drop(columns=['peraturan', 'benih']).median(numeric_only=True)
        rw['peraturan'] = f'Rawak (median {len(r)} benih; p5–p95 CAGR {100 * r.cagr.quantile(.05):.1f}–{100 * r.cagr.quantile(.95):.1f}%)'
        X = pd.concat([pd.DataFrame([rw]), lain], ignore_index=True)
        X['L'], X['rejim'], X['slot_n'] = L, rj, sn
        B.append(X)
        cols = ['peraturan', 'cagr', 'mdd', 'mar', 'h1', 'h2', 'n', 'menang', 'purata', 'lebih_spy', 'hari', 'slot', 'cagr_pct_rawak', 'h1_pct_rawak', 'h2_pct_rawak']
        Y = X[[c for c in cols if c in X]].copy()
        for c in ('cagr', 'mdd', 'h1', 'h2', 'menang', 'purata', 'lebih_spy'): Y[c] = 100 * Y[c]
        print(f"\n== Keluar L{L} ({'kaedah' if L == 1 else 'Chandelier'}), rejim SPY>SMA200 {'YA' if rj else 'tidak'}, {sn} slot")
        print(Y.set_index('peraturan').round(2).to_string())
    pd.concat(B, ignore_index=True).to_csv(os.path.join(out, 'keputusan.csv'), index=False, float_format='%.5f')
    th = {}
    for (nama, L, rj), cv in kurva.items():
        if nama == 'SPY' or (not rj and nama in ('Gabungan (kaedah WF + RS + industri + konsensus)', 'Kaedah walk-forward 12 bulan', 'RS pasaran', 'Kaedah statik (pandang hadapan, rujukan)')):
            y = cv.resample('YE').last(); y = pd.concat([cv.iloc[:1], y]).pct_change().dropna()
            th[f'{nama} L{L}' if nama != 'SPY' else 'SPY'] = (100 * y).round(1).set_axis(y.index.year)
    th = pd.DataFrame(th).T; print('\n== Pulangan tahunan % (2020 = Nov–Dis; 2026 hingga Okt)'); print(th.to_string())
    th.to_csv(os.path.join(out, 'tahunan.csv'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); s = ap.add_subparsers(dest='cmd', required=True)
    x = s.add_parser('sedia'); x.add_argument('--kumpulan', default=f'{OUT}/kumpulan_harian.csv.gz'); x.set_defaults(f=cmd_sedia)
    x = s.add_parser('semak'); x.add_argument('--kaedah', nargs='+', default=['M03', 'M27', 'M119']); x.set_defaults(f=cmd_semak)
    s.add_parser('sim').set_defaults(f=cmd_sim); s.add_parser('ringkas').set_defaults(f=cmd_ringkas)
    a = ap.parse_args(); a.f(a)
