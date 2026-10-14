#!/usr/bin/env python3
"""Laporan P01 Peringkat 3 — bandingkan varian V0–V5 dengan hari rawak yang ditapis sama."""
import sys
import pandas as pd


def pct(x):
    return "–" if pd.isna(x) else f"{100 * x:.0f}%"


def sg(x):
    return "–" if pd.isna(x) else f"{100 * x:+.1f}%"


def jadual(hdr, rows):
    s = "| " + " | ".join(hdr) + " |\n|" + "---|" * len(hdr) + "\n"
    return s + "".join("| " + " | ".join(map(str, r)) + " |\n" for r in rows)


def muat(f):
    d = pd.read_csv(f, low_memory=False)
    d = d[(d.ufuk_penuh == True) & (d.gap != True)].copy()
    d["tahun"] = d.masuk_tarikh // 10000
    return d


def v0(d):
    """Turutan asal pengguna: tiada isyarat teras 'pra'; MA10>MA20 menyala dahulu (atau serentak)
    sebelum RSI>50 dan squeeze hijau."""
    L = d[d.status == "lengkap"].copy()
    a, r, q = (pd.to_numeric(L[f"rel_{k}"], errors="coerce") for k in ["A1", "R1", "Q3"])
    m = (a >= 0) & (r >= 0) & (q >= 0) & (a <= r) & (a <= q)
    return pd.concat([L[m], d[d.status != "lengkap"]])


def nilai(nama, d):
    L, R, M = d[d.status == "lengkap"], d[d.status == "rawak"], d[d.status == "m1 sahaja"]
    bL, bR, bM = (x.kelas.eq("Berjaya").mean() for x in (L, R, M))
    tL, tR = L.kelas.eq("Gagal teruk").mean(), R.kelas.eq("Gagal teruk").mean()
    per = {}
    for t in ["penemuan", "pengesahan"]:
        per[t] = (L[L.tempoh == t].kelas.eq("Berjaya").mean(), R[R.tempoh == t].kelas.eq("Berjaya").mean())
    sub = sum(1 for s in ["S1", "S2", "S3", "S4"]
              if L[L.subset == s].kelas.eq("Berjaya").mean() - R[R.subset == s].kelas.eq("Berjaya").mean() >= 0.05)
    nt = L[L.tahun != 2020]; rt = R[R.tahun != 2020]
    g1 = len(L) >= 100
    g2 = bL - bR >= 0.05
    g3 = tL < tR - 0.005
    g4 = all(a - b >= 0.05 for a, b in per.values())
    g5 = sub >= 3
    lulus = all([g1, g2, g3, g4, g5])
    return dict(
        ringkas=[nama, len(L), pct(bL), pct(bR), f"{100 * (bL - bR):+.1f}", pct(tL), pct(tR), pct(bM),
                 sg(L.E0_untung.mean()), sg(L.E0_untung.median()), sg(L.naik_maks.median())],
        stabil=[nama, f"{pct(per['penemuan'][0])} / {pct(per['penemuan'][1])}",
                f"{pct(per['pengesahan'][0])} / {pct(per['pengesahan'][1])}",
                f"{sub}/4", f"{pct(nt.kelas.eq('Berjaya').mean())} / {pct(rt.kelas.eq('Berjaya').mean())}"],
        gate=[nama] + ["✅" if g else "❌" for g in (g1, g2, g3, g4, g5)] + ["**LULUS**" if lulus else "GAGAL"],
        lulus=lulus)


def lapor(fail_v1, fail_lain):
    d1 = muat(fail_v1)
    sets = [("V0 Turutan asal (MA10>MA20 dahulu)", v0(d1)), ("V1 Asas (20 hari)", d1)]
    nama = {"V2": "V2 Lengkap dalam 10 hari", "V3": "V3 Tambah +DI>−DI", "V4": "V4 SPY > MA200",
            "V5": "V5 Harga > MA150"}
    for f in fail_lain:
        v = f.split("_")[-1].replace(".csv", "")
        sets.append((nama.get(v, v), muat(f)))
    hasil = [nilai(n, d) for n, d in sets]
    out = ["# P01 — Peringkat 3: Varian V0–V5 (431 saham)\n",
           "Setiap varian dibandingkan dengan **hari rawak yang ditapis dengan syarat yang sama** "
           "(contoh V4: hari rawak semasa SPY > MA200). Ufuk 60 hari penuh; tanpa gap > 15%.\n"]
    out.append("## 1. Ringkasan\n" + jadual(
        ["Varian", "Bil. lengkap", "Berjaya", "Berjaya rawak", "Beza (mata)", "Gagal teruk", "Gagal teruk rawak",
         "Berjaya MACD sahaja", "Purata E0", "Median E0", "Median naik maks"], [h["ringkas"] for h in hasil]))
    out.append("## 2. Kestabilan (% Berjaya: varian / rawak)\n" + jadual(
        ["Varian", "2019–2023", "2024–2026", "Subset ≥ +5 mata", "Tanpa 2020"], [h["stabil"] for h in hasil]))
    out.append("## 3. Gate\n" + jadual(
        ["Varian", "≥100 kejadian", "≥ +5 mata vs rawak", "Gagal teruk < rawak", "+5 mata dalam kedua-dua tempoh",
         "≥ 3/4 subset", "Keputusan"], [h["gate"] for h in hasil]))
    # Calon dari peringkat 1 dalam setiap varian
    rows = []
    for n, d in sets:
        L = d[(d.status == "lengkap") & (d.turutan == "M1 → A1 → R1+Q3")]
        R = d[d.status == "rawak"]
        rows.append([n, len(L), pct(L.kelas.eq("Berjaya").mean()), pct(R.kelas.eq("Berjaya").mean()),
                     pct(L.kelas.eq("Gagal teruk").mean())])
    out.append("## 4. Semakan calon Peringkat 1: turutan `M1 → A1 → R1+Q3`\n" + jadual(
        ["Varian", "Bil.", "Berjaya", "Berjaya rawak", "Gagal teruk"], rows))
    return "\n".join(out), hasil


if __name__ == "__main__":
    teks, _ = lapor(sys.argv[1], sys.argv[2:])
    print(teks)
