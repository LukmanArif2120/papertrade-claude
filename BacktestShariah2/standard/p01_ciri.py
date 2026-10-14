#!/usr/bin/env python3
"""P01 — Eksplorasi ciri pada hari isyarat. Kuintil dikira daripada hari rawak 2019–2023 sahaja."""
import sys, numpy as np, pandas as pd

def ciri_saham(g):
    g = g.sort_values("date").reset_index(drop=True)
    c, h, l, v = g.close, g.high, g.low, g.volume
    d = c.diff()
    au = d.clip(lower=0).ewm(alpha=1/14, adjust=False).mean(); ad = (-d.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
    pc = c.shift(); tr = pd.concat([h-l, (h-pc).abs(), (l-pc).abs()], axis=1).max(axis=1)
    upm, dnm = h.diff(), -l.diff()
    pdm = pd.Series(np.where((upm>dnm)&(upm>0), upm, 0.)); ndm = pd.Series(np.where((dnm>upm)&(dnm>0), dnm, 0.))
    atrw = tr.ewm(alpha=1/14, adjust=False).mean()
    pdi = 100*pdm.ewm(alpha=1/14, adjust=False).mean()/atrw; mdi = 100*ndm.ewm(alpha=1/14, adjust=False).mean()/atrw
    dx = 100*(pdi-mdi).abs()/(pdi+mdi)
    sma20, sd20 = c.rolling(20).mean(), c.rolling(20).std(ddof=0)
    return pd.DataFrame(dict(
        ticker=g.ticker, date=g.date,
        rsi=100-100/(1+au/ad),
        roc20=c/c.shift(20)-1, roc63=c/c.shift(63)-1, roc126=c/c.shift(126)-1,
        jarak_ma50=c/c.rolling(50).mean()-1, jarak_ma150=c/c.rolling(150).mean()-1,
        jarak_high252=c/c.rolling(252, min_periods=150).max()-1,
        atr_pct=tr.rolling(22).mean()/c,
        volr=v/v.rolling(20).mean(),
        lebar_bb=4*sd20/sma20,
        adx=dx.ewm(alpha=1/14, adjust=False).mean(),
        nilai_dagangan=(c*v).rolling(20).mean()))

CIRI = ["rsi","roc20","roc63","roc126","jarak_ma50","jarak_ma150","jarak_high252","atr_pct","volr","lebar_bb","adx","nilai_dagangan"]

if __name__ == "__main__":
    kej = pd.read_csv(sys.argv[1], low_memory=False)
    kej = kej[(kej.ufuk_penuh==True)&(kej.gap!=True)].copy()
    # hari isyarat: m1 sahaja → T0; lengkap → T; rawak → T (= hari rawak)
    kej["hari_isyarat"] = np.where(kej.status=="m1 sahaja", kej.t0, pd.to_numeric(kej["T"], errors="coerce"))
    kej = kej[kej.status.isin(["m1 sahaja","lengkap","rawak"])]
    F = pd.concat([ciri_saham(g) for f in sys.argv[2:] for _, g in pd.read_csv(f).groupby("ticker")])
    kej["hari_isyarat"] = kej.hari_isyarat.astype(int)
    m = kej.merge(F, left_on=["ticker","hari_isyarat"], right_on=["ticker","date"], how="left")
    m["tempoh"] = np.where(m.masuk_tarikh//10000 <= 2023, "pen", "pes")
    m["tahun"] = m.masuk_tarikh//10000
    m["berjaya"] = (m.kelas=="Berjaya").astype(float)
    m.to_parquet("/home/claude/hasil/P4/ciri.parquet") if False else m.to_pickle("/home/claude/hasil/P4/ciri.pkl")
    R = m[m.status=="rawak"]; base = {t: R[R.tempoh==t].berjaya.mean() for t in ["pen","pes"]}
    baseE3 = {t: R[R.tempoh==t].E3_untung.mean() for t in ["pen","pes"]}
    out = []
    for f in CIRI:
        q = R[R.tempoh=="pen"][f].quantile([.2,.4,.6,.8]).to_numpy()
        m[f+"_q"] = np.digitize(m[f], q) + 1
        m.loc[m[f].isna(), f+"_q"] = np.nan
        for qq in range(1,6):
            for st in ["rawak","m1 sahaja","lengkap"]:
                r = dict(ciri=f, kuintil=qq, julat=f"{'-inf' if qq==1 else round(q[qq-2],3)} .. {'inf' if qq==5 else round(q[qq-1],3)}", status=st)
                for t in ["pen","pes"]:
                    g = m[(m.status==st)&(m[f+"_q"]==qq)&(m.tempoh==t)]
                    rr = m[(m.status=="rawak")&(m[f+"_q"]==qq)&(m.tempoh==t)]
                    r[f"n_{t}"] = len(g); r[f"berjaya_{t}"] = g.berjaya.mean(); r[f"E3_{t}"] = g.E3_untung.mean()
                    r[f"E0_{t}"] = g.E0_untung.mean(); r[f"gt_{t}"] = (g.kelas=="Gagal teruk").mean()
                    r[f"vs_semua_{t}"] = g.berjaya.mean() - base[t]           # lawan rawak keseluruhan
                    r[f"vs_kuintil_{t}"] = g.berjaya.mean() - rr.berjaya.mean()  # lawan rawak kuintil sama
                    r[f"E3_vs_semua_{t}"] = g.E3_untung.mean() - baseE3[t]
                out.append(r)
    o = pd.DataFrame(out)
    o.to_csv("/home/claude/hasil/P4/ciri_kuintil.csv", index=False)
    print("asas rawak berjaya:", base, "E3:", baseE3)
