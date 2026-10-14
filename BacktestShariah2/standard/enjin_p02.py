#!/usr/bin/env python3
"""
Enjin Kajian Peristiwa P02 v1.2 (v1.2: betulkan jenis data spy_ok untuk V4; V1–V3, V5 tidak terjejas) — Saham peneraju RS + masa masuk.
Spesifikasi: spec/P02_rs_peneraju.md (Project Backtest Shariah).
Guna semula fungsi indikator, keluar dan ukuran P01 (enjin_p01 v1.1):
  K1 = E1 (MACD merah atau henti −8%), K2 = E2 (tutup < SMA20 atau henti), K3 = E3 (3×ATR22 atau henti).

Guna:
  python3 enjin_p02.py --data data/dataset_S*.csv --bench data/index_benchmark.csv --out hasil/P02 --varian V1
"""
import argparse, os, json, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import enjin_p01 as E

VERSI = "1.2"
BURUK = ["ASST", "FCEL", "MTDR", "OVV", "PR", "SM", "VAL", "XENE"]
Q = dict(kolam=0.80, bawah=0.20, kadar_rawak=0.05, benih=42, panas=252)
E.P["panas"] = 0  # panas dikawal oleh ketersediaan RS (252 hari)


def rs_ukuran(c: pd.Series, spy: pd.Series, varian: str) -> pd.DataFrame:
    rsl = c / spy
    out = pd.DataFrame(index=c.index)
    out["rsl"] = rsl
    if varian == "V3":
        out["rs"] = rsl / rsl.shift(125) - 1
    elif varian == "V5":
        out["rs"] = (2 * rsl / rsl.shift(63) + rsl.shift(63) / rsl.shift(126)
                     + rsl.shift(126) / rsl.shift(189) + rsl.shift(189) / rsl.shift(252))
    else:
        out["rs"] = rsl / rsl.shift(251) - 1
    mx = rsl.rolling(252, min_periods=252).max()
    out["rs_tinggi"] = rsl >= mx                                   # setiap hari di paras tertinggi (V0 / I03)
    out["rsh"] = out["rs_tinggi"] & ~(rsl.shift(1) >= rsl.shift(1).rolling(252, min_periods=252).max())
    out.loc[mx.isna(), ["rs_tinggi", "rsh"]] = False
    return out


def muat(fail_data, fail_bench, sertakan_buruk):
    b = pd.read_csv(fail_bench)
    spy = b[b.ticker == "SPY"].sort_values("date").set_index("date")["close"]
    spy200 = (spy > spy.rolling(200).mean())
    saham = {}
    for f in fail_data:
        sub = os.path.basename(f).replace("dataset_", "").replace(".csv", "")
        d = pd.read_csv(f)
        for tk, g in d.groupby("ticker"):
            if not sertakan_buruk and tk in BURUK:
                continue
            g = g.sort_values("date").reset_index(drop=True)
            saham[tk] = (sub, g)
    return saham, spy, spy200


def jalan(fail_data, fail_bench, varian="V1", out="hasil/P02", sertakan_buruk=False):
    kolam_min = 0.90 if varian == "V2" else Q["kolam"]
    saham, spy, spy200 = muat(fail_data, fail_bench, sertakan_buruk)
    # 1. RS setiap saham, kemudian persentil merentas saham setiap tarikh
    rsd, ind_all = {}, {}
    for tk, (sub, g) in saham.items():
        s = spy.reindex(g.date).ffill().to_numpy()
        r = rs_ukuran(g.close.reset_index(drop=True), pd.Series(s), varian)
        r["date"] = g.date.to_numpy()
        rsd[tk] = r
    panel = pd.DataFrame({tk: r.set_index("date")["rs"] for tk, r in rsd.items()})
    pct = panel.rank(axis=1, pct=True)          # 1.0 = paling kuat
    rng = np.random.default_rng(Q["benih"])
    rows = []
    for tk, (sub, g) in saham.items():
        r = rsd[tk]
        n = len(g)
        dates = g.date.to_numpy()
        p = pct[tk].reindex(dates).to_numpy()
        spy_ok = pd.Series(dates).map(spy200).fillna(False).astype(bool).to_numpy()
        ind = E.indikator(g, None)
        hist = ind["hist"]
        m1 = (hist > 0) & (np.r_[True, hist[:-1] <= 0])
        m1[0] = False
        sah = ~np.isnan(p) & (np.arange(n) < n - 1) & (ind["vol20"] >= E.P["vol_min"])
        if varian == "V4":
            sah &= spy_ok
        kolam = sah & (p >= kolam_min)

        def catat(i, status, isyarat=""):
            e = i + 1
            rec = dict(ticker=tk, subset=sub, varian=varian, status=status, isyarat=isyarat,
                       hari=int(dates[i]), masuk_tarikh=int(dates[e]), masuk_harga=float(ind["o"][e]),
                       pct_rs=float(p[i]), spy_ok=bool(spy_ok[i]),
                       gap=bool(ind["o"][e] / ind["c"][i] - 1 > E.P["gap_max"]))
            E.ukur_masuk(ind, e, rec)
            return rec

        # 2. Isyarat B2 (MACD hijau) dan B3 (RS paras tertinggi baharu), tiada tindih ikut K1 (=E1)
        bil = 0
        for status, mask in [("B2", kolam & m1), ("B3", kolam & r["rsh"].to_numpy())]:
            akhir = -1
            for i in np.nonzero(mask)[0]:
                if i <= akhir:
                    continue
                rec = catat(i, status)
                rows.append(rec)
                bil += 1
                akhir = i + rec["E1_hari"]
        # 3. V0: peraturan I03 tulen — setiap hari di paras tertinggi RS, tanpa kolam, K2 tanpa henti
        if varian == "V1":
            akhir = -1
            v0mask = sah & r["rs_tinggi"].to_numpy()
            for i in np.nonzero(v0mask)[0]:
                if i <= akhir:
                    continue
                e = i + 1
                rec = catat(i, "V0")
                # K2 tanpa henti: tutup < SMA20 sahaja
                k_out = None
                for k in range(e, n):
                    if ind["c"][k] < ind["ma20"][k]:
                        k_out = k
                        break
                if k_out is None or k_out + 1 >= n:
                    kk = n - 1 if k_out is None else k_out
                    rec["V0_untung"], rec["V0_hari"] = ind["c"][kk] / ind["o"][e] - 1, kk - e + 1
                else:
                    rec["V0_untung"], rec["V0_hari"] = ind["o"][k_out + 1] / ind["o"][e] - 1, k_out - e + 1
                rows.append(rec)
                akhir = i + rec["V0_hari"]
        # 4. Kawalan rawak: B1 (kolam), C0 (semua), C1 (20% terbawah).
        #    v1.1: sampel seragam 5% daripada hari layak bagi SETIAP saham (tidak bergantung pada bilangan isyarat),
        #    supaya kawalan mewakili populasi sebenar. (v1.0 mengikat bilangan pada B2+B3 → saham tanpa isyarat
        #    tiada dalam C0/C1, dan saham banyak isyarat terlebih wakil.)
        for status, mask in [("B1", kolam), ("C0", sah), ("C1", sah & (p <= Q["bawah"]))]:
            calon = np.nonzero(mask)[0]
            kira = int(round(Q["kadar_rawak"] * len(calon)))
            if kira:
                for i in sorted(rng.choice(calon, size=kira, replace=False)):
                    rows.append(catat(i, status))
    df = pd.DataFrame(rows)
    df["tahun"] = df.masuk_tarikh // 10000
    df["tempoh"] = np.where(df.tahun <= 2023, "penemuan", "pengesahan")
    df = df.rename(columns={c: c.replace("E1_", "K1_").replace("E2_", "K2_").replace("E3_", "K3_")
                            for c in df.columns})
    os.makedirs(out, exist_ok=True)
    tag = varian + ("_buruk" if sertakan_buruk else "")
    df.to_csv(os.path.join(out, f"kejadian_{tag}.csv"), index=False)
    with open(os.path.join(out, f"parameter_{tag}.json"), "w") as fh:
        json.dump(dict(versi=VERSI, varian=varian, kolam_min=kolam_min, sertakan_buruk=sertakan_buruk,
                       **Q, henti=E.P["henti"], ufuk=E.P["ufuk"]), fh, indent=1)
    return df, pct


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", nargs="+", required=True)
    ap.add_argument("--bench", required=True)
    ap.add_argument("--varian", default="V1")
    ap.add_argument("--out", default="hasil/P02")
    ap.add_argument("--sertakan_buruk", action="store_true")
    a = ap.parse_args()
    df, _ = jalan(a.data, a.bench, a.varian, a.out, a.sertakan_buruk)
    print(a.varian, df.status.value_counts().to_dict())
