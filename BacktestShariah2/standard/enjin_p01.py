#!/usr/bin/env python3
"""
Enjin Kajian Peristiwa P01 v1.1 (v1.1: tambah kumpulan "m1 sahaja" untuk Peringkat 2) — Corak isyarat selepas MACD hijau.
Spesifikasi: spec/P01_corak_isyarat_macd.md (Project Backtest Shariah).

Bukan enjin portfolio. Setiap kejadian (T0 = histogram MACD bertukar hijau) direkod:
hari setiap isyarat menyala, turutan, hasil ke depan, dan hasil 5 cara keluar (E0–E4).

Guna:
  python3 enjin_p01.py --data data/dataset_S1.csv data/dataset_S2.csv ... \
      --bench data/index_benchmark.csv --out hasil/V1 --varian V1
"""
import argparse, os, json
import numpy as np
import pandas as pd

VERSI = "1.1"

# ---------------- Parameter (dibekukan) ----------------
P = dict(
    tetingkap=20,        # hari selepas T0 untuk isyarat lengkap
    ufuk=60,             # ufuk tetap untuk kenaikan maksimum & kelas hasil
    henti=0.92,          # henti rugi −8%
    atr_mult=3.0,        # E3 chandelier
    panas=200,           # hari pertama dibuang setiap saham
    vol_min=100_000,     # volum purata 20 hari minimum
    gap_max=0.15,        # gap > 15% pada hari masuk → ditanda "gap"
    n_rawak=3,           # hari rawak bagi setiap kejadian lengkap
    benih=42,
)
TERAS_ASAS = ["A1", "R1", "Q3"]            # M1 ialah titik mula
REKOD = ["D1", "Q1", "A2", "A3", "V1"]      # direkod sahaja
SEMUA = ["M1"] + TERAS_ASAS + REKOD
KELUAR = ["E0", "E1", "E2", "E3", "E4"]


# ---------------- Indikator ----------------
def indikator(g: pd.DataFrame, spy_ok: pd.Series | None) -> dict:
    o, h, l, c, v = (g[k].to_numpy(float) for k in ["open", "high", "low", "close", "volume"])
    cs = pd.Series(c)
    e12 = cs.ewm(span=12, adjust=False).mean()
    e26 = cs.ewm(span=26, adjust=False).mean()
    dif = e12 - e26
    hist = (dif - dif.ewm(span=9, adjust=False).mean()).to_numpy()

    ma = {n: cs.rolling(n).mean().to_numpy() for n in (10, 20, 50, 150)}

    d = cs.diff()
    au = d.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean()
    ad = (-d.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
    rsi = (100 - 100 / (1 + au / ad)).to_numpy()

    hs, ls = pd.Series(h), pd.Series(l)
    pc = cs.shift()
    tr = pd.concat([hs - ls, (hs - pc).abs(), (ls - pc).abs()], axis=1).max(axis=1)
    upm, dnm = hs.diff(), -ls.diff()
    pdm = pd.Series(np.where((upm > dnm) & (upm > 0), upm, 0.0))
    ndm = pd.Series(np.where((dnm > upm) & (dnm > 0), dnm, 0.0))
    atrw = tr.ewm(alpha=1 / 14, adjust=False).mean()
    pdi = (100 * pdm.ewm(alpha=1 / 14, adjust=False).mean() / atrw).to_numpy()
    mdi = (100 * ndm.ewm(alpha=1 / 14, adjust=False).mean() / atrw).to_numpy()

    # Squeeze (LazyBear): BB 20/2 di dalam KC 20/1.5 (julat = TR, SMA)
    sma20 = cs.rolling(20).mean()
    sd20 = cs.rolling(20).std(ddof=0)
    rng20 = tr.rolling(20).mean()
    sqz_on = ((sma20 - 2 * sd20) > (sma20 - 1.5 * rng20)) & ((sma20 + 2 * sd20) < (sma20 + 1.5 * rng20))
    x = cs - ((hs.rolling(20).max() + ls.rolling(20).min()) / 2 + sma20) / 2
    mom = linreg_akhir(x.to_numpy(), 20)

    atr22 = tr.rolling(22).mean().to_numpy()
    volr = (pd.Series(v) / pd.Series(v).rolling(20).mean()).to_numpy()
    vol20 = pd.Series(v).rolling(20).mean().to_numpy()

    with np.errstate(invalid="ignore"):
        sig = {
            "M1": hist > 0,
            "A1": ma[10] > ma[20],
            "R1": rsi > 50,
            "Q3": mom > 0,
            "D1": pdi > mdi,
            "Q1": sqz_on.to_numpy(),
            "A2": c > ma[50],
            "A3": c > ma[150],
            "V1": volr > 1.5,
        }
    return dict(o=o, h=h, l=l, c=c, hist=hist, ma10=ma[10], ma20=ma[20], ma150=ma[150],
                atr22=atr22, vol20=vol20, sig=sig, spy_ok=spy_ok)


def linreg_akhir(x: np.ndarray, n: int) -> np.ndarray:
    """Nilai garis regresi linear pada titik terakhir tetingkap n (sama seperti linreg(x,n,0))."""
    out = np.full(len(x), np.nan)
    if len(x) < n:
        return out
    t = np.arange(n, dtype=float)
    tb = t.mean()
    w = (t - tb) / ((t - tb) ** 2).sum()
    win = np.lib.stride_tricks.sliding_window_view(x, n)
    slope = win @ w
    out[n - 1:] = win.mean(axis=1) + slope * (n - 1 - tb)
    return out


# ---------------- Keluar ----------------
def keluar(ind, e: int, cara: str):
    """Masuk pada buka hari e. Kembalikan (hari_isyarat, harga_keluar, terbuka?)."""
    o, c, hist = ind["o"], ind["c"], ind["hist"]
    masuk = o[e]
    henti = masuk * P["henti"]
    maxc = -np.inf
    n = len(c)
    for k in range(e, n):
        maxc = max(maxc, c[k])
        macd_merah = hist[k] < 0
        stop = c[k] < henti
        if cara == "E0":
            x = macd_merah
        elif cara == "E1":
            x = macd_merah or stop
        elif cara == "E2":
            x = (c[k] < ind["ma20"][k]) or stop
        elif cara == "E3":
            x = (c[k] < maxc - P["atr_mult"] * ind["atr22"][k]) or stop
        elif cara == "E4":
            x = (macd_merah and c[k] < ind["ma10"][k]) or stop
        else:
            raise ValueError(cara)
        if x:
            if k + 1 < n:
                return k, o[k + 1], False
            return k, c[k], True
    return n - 1, c[n - 1], True


def hasil_ke_depan(ind, e: int):
    """Kenaikan maks, kejatuhan maks, hari ke puncak, kelas — ufuk tetap P['ufuk']."""
    o, c = ind["o"], ind["c"]
    masuk = o[e]
    akhir = min(len(c), e + P["ufuk"])
    seg = c[e:akhir] / masuk - 1
    if len(seg) == 0:
        return dict(naik_maks=np.nan, jatuh_maks=np.nan, hari_puncak=np.nan, kelas="tiada_data", ufuk_penuh=False)
    naik = float(seg.max())
    jatuh = float(seg.min())
    hp = int(seg.argmax())
    # Gagal teruk: −10% dicapai sebelum +10%
    i_up = np.argmax(seg >= 0.10) if (seg >= 0.10).any() else None
    i_dn = np.argmax(seg <= -0.10) if (seg <= -0.10).any() else None
    if i_dn is not None and (i_up is None or i_dn < i_up):
        kelas = "Gagal teruk"
    elif naik >= 0.20:
        kelas = "Berjaya"
    elif naik >= 0.10:
        kelas = "Sederhana"
    else:
        kelas = "Gagal"
    return dict(naik_maks=naik, jatuh_maks=jatuh, hari_puncak=hp, kelas=kelas,
                ufuk_penuh=(e + P["ufuk"] <= len(c)))


def ukur_masuk(ind, e: int, rec: dict):
    rec.update(hasil_ke_depan(ind, e))
    masuk = ind["o"][e]
    for k in KELUAR:
        ks, px, terbuka = keluar(ind, e, k)
        rec[f"{k}_untung"] = px / masuk - 1
        rec[f"{k}_hari"] = ks - e + 1
        rec[f"{k}_terbuka"] = terbuka
        seg = ind["c"][e:ks + 1]
        rec[f"{k}_naik_dlm_pegang"] = float(seg.max() / masuk - 1)
    return rec


# ---------------- Kejadian ----------------
def label_turutan(rel: dict, teras: list) -> str:
    """rel: kod → hari relatif (−1 = sudah aktif sebelum T0). M1 = 0."""
    pra = [k for k in teras if rel[k] == -1]
    kump = {}
    kump.setdefault(0, ["M1"])
    for k in teras:
        if rel[k] >= 0:
            kump.setdefault(rel[k], []).append(k)
    badan = " → ".join("+".join(kump[d]) for d in sorted(kump))
    return (f"pra:{'+'.join(pra)} ; " if pra else "") + badan


def proses_saham(tk: str, g: pd.DataFrame, teras: list, varian: str, rng, spy_map):
    g = g.sort_values("date").reset_index(drop=True)
    spy_ok = g["date"].map(spy_map).fillna(False).to_numpy() if spy_map is not None else None
    ind = indikator(g, spy_ok)
    s = ind["sig"]
    n = len(g)
    dates = g["date"].to_numpy()
    W = P["tetingkap"]
    keluar_ = []
    i = max(P["panas"], 1)
    akhir_dagangan = -1
    while i < n - 1:
        if not (s["M1"][i] and not s["M1"][i - 1]) or i <= akhir_dagangan:
            i += 1
            continue
        t0 = i
        T, putus = None, None
        for j in range(t0, min(n - 1, t0 + W + 1)):
            if not s["M1"][j]:
                putus = j
                break
            if all(s[k][j] for k in teras):
                T = j
                break
        rec = dict(ticker=tk, varian=varian, t0=int(dates[t0]))
        # hari relatif setiap isyarat
        hujung = T if T is not None else (putus - 1 if putus is not None else min(n - 2, t0 + W))
        rel = {}
        for k in teras + [r for r in REKOD if r not in teras]:
            if s[k][t0] and s[k][t0 - 1]:
                rel[k] = -1
            else:
                hit = np.nonzero(s[k][t0:hujung + 1])[0]
                rel[k] = int(hit[0]) if len(hit) else None
            rec[f"rel_{k}"] = rel[k] if rel[k] is not None else ""
        if T is not None:
            e = T + 1
            rec.update(status="lengkap", T=int(dates[T]), hari_ke_lengkap=T - t0,
                       turutan=label_turutan(rel, teras))
            rec["sihat"] = (all(rel[k] >= 0 for k in teras)
                            and rel["A1"] >= max(rel[k] for k in teras if k != "A1"))
            for r in REKOD:
                rec[f"diT_{r}"] = bool(s[r][T])
            rec["gap"] = bool(ind["o"][e] / ind["c"][T] - 1 > P["gap_max"])
            rec["vol_ok"] = bool(ind["vol20"][T] >= P["vol_min"])
            rec["atas_ma150"] = bool(ind["c"][T] > ind["ma150"][T]) if not np.isnan(ind["ma150"][T]) else False
            rec["spy_ok"] = bool(spy_ok[T]) if spy_ok is not None else ""
        else:
            e = t0 + 1
            rec.update(status="tidak lengkap", T="", hari_ke_lengkap="", turutan="tidak lengkap", sihat="")
            rec["gap"] = False
            rec["vol_ok"] = bool(ind["vol20"][t0] >= P["vol_min"])
            rec["atas_ma150"] = bool(ind["c"][t0] > ind["ma150"][t0]) if not np.isnan(ind["ma150"][t0]) else False
            rec["spy_ok"] = bool(spy_ok[t0]) if spy_ok is not None else ""
        rec["masuk_tarikh"] = int(dates[e])
        rec["masuk_harga"] = float(ind["o"][e])
        ukur_masuk(ind, e, rec)
        keluar_.append(rec)
        # Peringkat 2: MACD hijau sahaja — masuk buka T0+1 untuk SETIAP T0 (lengkap atau tidak)
        e1 = t0 + 1
        m1 = dict(ticker=tk, varian=varian, t0=int(dates[t0]), status="m1 sahaja",
                  T="", turutan="MACD hijau sahaja", sihat="",
                  lengkap_kemudian=(T is not None), hari_ke_lengkap=rec.get("hari_ke_lengkap", ""),
                  gap=bool(ind["o"][e1] / ind["c"][t0] - 1 > P["gap_max"]),
                  vol_ok=bool(ind["vol20"][t0] >= P["vol_min"]),
                  atas_ma150=bool(ind["c"][t0] > ind["ma150"][t0]) if not np.isnan(ind["ma150"][t0]) else False,
                  spy_ok=bool(spy_ok[t0]) if spy_ok is not None else "",
                  masuk_tarikh=int(dates[e1]), masuk_harga=float(ind["o"][e1]))
        ukur_masuk(ind, e1, m1)
        keluar_.append(m1)
        rec["lengkap_kemudian"] = (T is not None)
        # tiada tindih: kejadian seterusnya selepas E0 keluar
        akhir_dagangan = e + int(rec["E0_hari"]) - 1
        i = max(i + 1, akhir_dagangan + 1)

    # Kawalan C1: hari rawak (bilangan = n_rawak × kejadian lengkap)
    n_lengkap = sum(1 for r in keluar_ if r["status"] == "lengkap")
    calon = np.arange(P["panas"], n - 2)
    rawak = []
    if n_lengkap and len(calon):
        pilih = rng.choice(calon, size=min(len(calon), P["n_rawak"] * n_lengkap), replace=False)
        for r in sorted(pilih):
            e = r + 1
            rec = dict(ticker=tk, varian=varian, t0=int(dates[r]), status="rawak", T=int(dates[r]),
                       turutan="hari rawak", sihat="", gap=bool(ind["o"][e] / ind["c"][r] - 1 > P["gap_max"]),
                       vol_ok=bool(ind["vol20"][r] >= P["vol_min"]),
                       atas_ma150=bool(ind["c"][r] > ind["ma150"][r]) if not np.isnan(ind["ma150"][r]) else False,
                       spy_ok=bool(spy_ok[r]) if spy_ok is not None else "",
                       masuk_tarikh=int(dates[e]), masuk_harga=float(ind["o"][e]))
            ukur_masuk(ind, e, rec)
            rawak.append(rec)
    return keluar_ + rawak


def jalan(fail_data, fail_bench, varian="V1", out="hasil", subset_dari_fail=True, panas=None):
    if panas is not None:
        P["panas"] = panas
    teras = list(TERAS_ASAS)
    if varian == "V2":
        P["tetingkap"] = 10
    if varian == "V3":
        teras = teras + ["D1"]
    spy_map = None
    if fail_bench:
        b = pd.read_csv(fail_bench)
        b = b[b.ticker == "SPY"].sort_values("date")
        b["ok"] = b.close > b.close.rolling(200).mean()
        spy_map = dict(zip(b.date, b.ok))
    rng = np.random.default_rng(P["benih"])
    semua = []
    for f in fail_data:
        d = pd.read_csv(f)
        sub = os.path.basename(f).replace("dataset_", "").replace(".csv", "")
        for tk, g in d.groupby("ticker"):
            if len(g) < P["panas"] + 30:
                continue
            for r in proses_saham(tk, g, teras, varian, rng, spy_map):
                r["subset"] = sub
                semua.append(r)
    df = pd.DataFrame(semua)
    if df.empty:
        return df
    # Penapis varian (dikenakan pada semua baris, termasuk rawak, supaya setara)
    df["tahun"] = df["masuk_tarikh"] // 10000
    df["tempoh"] = np.where(df["tahun"] <= 2023, "penemuan", "pengesahan")
    df = df[df["vol_ok"]]
    if varian == "V4":
        df = df[df["spy_ok"] == True]
    if varian == "V5":
        df = df[df["atas_ma150"] == True]
    os.makedirs(out, exist_ok=True)
    df.to_csv(os.path.join(out, f"kejadian_{varian}.csv"), index=False)
    with open(os.path.join(out, f"parameter_{varian}.json"), "w") as fh:
        json.dump(dict(versi=VERSI, varian=varian, teras=["M1"] + teras, **P), fh, indent=1)
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", nargs="+", required=True)
    ap.add_argument("--bench", default=None)
    ap.add_argument("--varian", default="V1")
    ap.add_argument("--out", default="hasil")
    ap.add_argument("--panas", type=int, default=None)
    a = ap.parse_args()
    df = jalan(a.data, a.bench, a.varian, a.out, panas=a.panas)
    print(f"Varian {a.varian}: {len(df)} baris; lengkap={int((df.status=='lengkap').sum())}, "
          f"tidak lengkap={int((df.status=='tidak lengkap').sum())}, rawak={int((df.status=='rawak').sum())}")
