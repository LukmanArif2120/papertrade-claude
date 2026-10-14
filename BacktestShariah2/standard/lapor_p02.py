#!/usr/bin/env python3
"""Laporan P02 v1.0 — kesan pilihan saham (RS) dan kesan masa masuk."""
import sys
import numpy as np
import pandas as pd

KELAS = ["Berjaya", "Sederhana", "Gagal", "Gagal teruk"]
NAMA = {"C0": "C0 Rawak, semua saham", "B1": "B1 Rawak, RS teratas", "B2": "B2 MACD hijau, RS teratas",
        "B3": "B3 RS paras tertinggi baharu", "C1": "C1 Rawak, RS terbawah"}
URUT = ["C0", "B1", "B2", "B3", "C1"]


def pct(x): return "–" if pd.isna(x) else f"{100 * x:.0f}%"
def sg(x): return "–" if pd.isna(x) else f"{100 * x:+.1f}%"
def bj(g): return g.kelas.eq("Berjaya").mean()
def gt(g): return g.kelas.eq("Gagal teruk").mean()


def jadual(h, rows):
    return "| " + " | ".join(h) + " |\n|" + "---|" * len(h) + "\n" + "".join(
        "| " + " | ".join(map(str, r)) + " |\n" for r in rows)


def muat(f):
    d = pd.read_csv(f, low_memory=False)
    return d[(d.ufuk_penuh == True) & (d.gap != True)].copy()


def lapor(f, tajuk="V1"):
    d = muat(f)
    G = {s: d[d.status == s] for s in URUT}
    out = [f"# P02 — Laporan {tajuk}\n",
           "Ufuk 60 hari penuh; tanpa gap > 15%. K1 = MACD merah, K2 = tutup < SMA20, K3 = 3×ATR22; semua dengan henti −8%.\n"]
    rows = []
    for s in URUT:
        g = G[s]
        rows.append([NAMA[s], len(g)] + [pct(g.kelas.eq(k).mean()) for k in KELAS] +
                    [sg(g.naik_maks.median()), sg(g.K1_untung.mean()), sg(g.K2_untung.mean()), sg(g.K3_untung.mean()),
                     pct((g.K3_untung >= .10).mean()), f"{g.K3_hari.median():.0f}"])
    out.append("## 1. Kumpulan (ufuk 60 hari)\n" + jadual(
        ["Kumpulan", "Bil.", "Berjaya ≥20%", "Sederhana", "Gagal <10%", "Gagal teruk", "Median naik maks",
         "Purata K1", "Purata K2", "Purata K3", "% K3 ≥ +10%", "Median hari K3"], rows))

    rows = []
    for s in ["B1", "B2", "B3"]:
        for k in ["K1", "K2", "K3"]:
            u = G[s][f"{k}_untung"]
            rows.append([NAMA[s], k, sg(u.mean()), sg(u.median()), pct((u > 0).mean()), pct((u >= .10).mean()),
                         pct((u <= -.08).mean()), f"{G[s][f'{k}_hari'].median():.0f}"])
    out.append("## 2. Cara keluar\n" + jadual(
        ["Kumpulan", "Keluar", "Purata", "Median", "% untung", "% ≥ +10%", "% rugi ≤ −8%", "Median hari"], rows))

    # Kestabilan
    def baris(nama, f):
        g = {s: f(G[s]) for s in URUT}
        return [nama, len(g["B1"])] + [pct(bj(g[s])) for s in URUT] + [sg(g[s].K3_untung.mean()) for s in ["C0", "B1", "B3"]]
    rows = [baris(f"Tempoh: {t}", lambda x, t=t: x[x.tempoh == t]) for t in ["penemuan", "pengesahan"]]
    rows += [baris(f"Subset: {s}", lambda x, s=s: x[x.subset == s]) for s in ["S1", "S2", "S3", "S4"]]
    rows += [baris(f"Tahun: {y}", lambda x, y=y: x[x.tahun == y]) for y in sorted(d.tahun.unique())]
    rows += [baris("Hingga Dis 2025", lambda x: x[x.tahun <= 2025]), baris("Tanpa 2020", lambda x: x[x.tahun != 2020])]
    out.append("## 3. Kestabilan (% Berjaya; purata K3)\n" + jadual(
        ["Kumpulan", "Bil. B1"] + URUT + ["K3 C0", "K3 B1", "K3 B3"], rows))

    # Kriteria
    def dua(f):
        return [f(G, t) for t in ["penemuan", "pengesahan"]]
    T = lambda g, t: g[g.tempoh == t]
    L1a = dua(lambda G, t: bj(T(G["B1"], t)) - bj(T(G["C0"], t)))
    L1b = dua(lambda G, t: T(G["B1"], t).K3_untung.mean() - T(G["C0"], t).K3_untung.mean())
    L1 = all(x >= .05 for x in L1a) and all(x > 0 for x in L1b)
    rows = [["L1 Pilihan saham: B1 − C0 ≥ 5 mata DAN purata K3 lebih tinggi, kedua-dua tempoh",
             f"{100*L1a[0]:+.1f} / {100*L1a[1]:+.1f} mata; K3 {sg(L1b[0])} / {sg(L1b[1])}", "✅" if L1 else "❌"]]
    for s in ["B2", "B3"]:
        e = dua(lambda G, t, s=s: bj(T(G[s], t)) - bj(T(G["B1"], t)))
        sub = sum(1 for q in ["S1", "S2", "S3", "S4"]
                  if bj(G[s][G[s].subset == q]) - bj(G["B1"][G["B1"].subset == q]) >= .05)
        ok = all(x >= .05 for x in e) and sub >= 3
        rows.append([f"L2 Masa masuk {s}: {s} − B1 ≥ 5 mata kedua-dua tempoh & ≥ 3/4 subset",
                     f"{100*e[0]:+.1f} / {100*e[1]:+.1f} mata; subset {sub}/4", "✅" if ok else "❌"])
    for s in ["B1", "B3"]:
        rows.append([f"L3 Gagal teruk {s} < C0", f"{pct(gt(G[s]))} vs {pct(gt(G['C0']))}",
                     "✅" if gt(G[s]) < gt(G["C0"]) - .005 else "❌"])
    for nama, f in [("hingga Dis 2025", lambda x: x[x.tahun <= 2025]), ("tanpa 2020", lambda x: x[x.tahun != 2020])]:
        a = bj(f(G["B1"])) - bj(f(G["C0"]))
        rows.append([f"L4 Arah B1 > C0 kekal {nama}", f"{100*a:+.1f} mata", "✅" if a > 0 else "❌"])
    rows.append(["L5 C1 lebih lemah daripada B1", f"{pct(bj(G['C1']))} vs {pct(bj(G['B1']))}",
                 "✅" if bj(G["C1"]) < bj(G["B1"]) else "❌"])
    out.append("## 4. Kriteria lulus\n" + jadual(["Kriteria", "Nilai", "Lulus"], rows))

    v0 = d[d.status == "V0"]
    if len(v0):
        out.append("## 5. V0 — peraturan I03 tulen (RS di paras tertinggi setiap hari, keluar tutup < SMA20 tanpa henti)\n" +
                   jadual(["Bil.", "Purata untung", "Median", "% ≥ +10%", "% rugi ≤ −8%", "Median hari", "Berjaya (60 hari)"],
                          [[len(v0), sg(v0.V0_untung.mean()), sg(v0.V0_untung.median()), pct((v0.V0_untung >= .1).mean()),
                            pct((v0.V0_untung <= -.08).mean()), f"{v0.V0_hari.median():.0f}", pct(bj(v0))]]))
    return "\n".join(out)


if __name__ == "__main__":
    print(lapor(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "V1"))
