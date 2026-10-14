#!/usr/bin/env python3
"""Laporan P01 Peringkat 2 — MACD hijau sahaja vs tunggu isyarat lengkap vs hari rawak."""
import sys
import numpy as np
import pandas as pd

KELAS = ["Berjaya", "Sederhana", "Gagal", "Gagal teruk"]


def pct(x):
    return "–" if pd.isna(x) else f"{100 * x:.0f}%"


def sg(x):
    return "–" if pd.isna(x) else f"{100 * x:+.1f}%"


def jadual(hdr, rows):
    s = "| " + " | ".join(hdr) + " |\n|" + "---|" * len(hdr) + "\n"
    return s + "".join("| " + " | ".join(map(str, r)) + " |\n" for r in rows)


def ringkas(nama, g):
    return [nama, len(g)] + [pct((g.kelas == k).mean()) for k in KELAS] + \
           [sg(g.naik_maks.median()), sg(g.E0_untung.median()), sg(g.E0_untung.mean()),
            pct((g.E0_untung >= 0.10).mean()), f"{g.E0_hari.median():.0f}"]


def lapor(fail):
    d = pd.read_csv(fail, low_memory=False)
    d = d[(d.ufuk_penuh == True) & (d.gap != True)].copy()
    d["tahun"] = d.masuk_tarikh // 10000
    L = d[d.status == "lengkap"]
    M = d[d.status == "m1 sahaja"]
    R = d[d.status == "rawak"]
    TL = d[d.status == "tidak lengkap"]
    Mk = M[M.lengkap_kemudian == True]
    Mt = M[M.lengkap_kemudian == False]
    out = ["# P01 — Peringkat 2: MACD hijau sahaja vs tunggu isyarat lengkap\n",
           f"MACD hijau (semua T0): {len(M)} · isyarat lengkap: {len(L)} · hari rawak: {len(R)} · "
           "ufuk 60 hari penuh, tanpa gap > 15%.\n"]
    H = ["Kumpulan", "Bil.", "Berjaya ≥20%", "Sederhana", "Gagal <10%", "Gagal teruk",
         "Median naik maks", "Median untung E0", "Purata untung E0", "% E0 ≥ +10%", "Median hari E0"]
    rows = [ringkas("A. Masuk terus bila MACD hijau (semua)", M),
            ringkas("B. Tunggu isyarat lengkap", L),
            ringkas("C. Hari rawak", R),
            ringkas("A1. MACD hijau → kemudian lengkap", Mk),
            ringkas("A2. MACD hijau → tidak lengkap", Mt)]
    out.append("## 1. Perbandingan utama (ufuk 60 hari)\n" + jadual(H, rows))

    # Berpasangan: kejadian yang kemudian lengkap — masuk awal vs tunggu
    a = Mk.set_index(["ticker", "t0"])
    b = L.set_index(["ticker", "t0"])
    k = a.index.intersection(b.index)
    a, b = a.loc[k], b.loc[k]
    kos = b.masuk_harga / a.masuk_harga - 1
    rows = [["Bilangan pasangan", len(k), ""],
            ["Harga masuk: tunggu berbanding masuk awal (median)", sg(kos.median()), "Harga lebih tinggi = kos menunggu"],
            ["% Berjaya: masuk awal / tunggu", f"{pct((a.kelas == 'Berjaya').mean())} / {pct((b.kelas == 'Berjaya').mean())}", ""],
            ["% Gagal teruk: masuk awal / tunggu", f"{pct((a.kelas == 'Gagal teruk').mean())} / {pct((b.kelas == 'Gagal teruk').mean())}", ""],
            ["Median untung E0: masuk awal / tunggu", f"{sg(a.E0_untung.median())} / {sg(b.E0_untung.median())}", ""],
            ["Purata untung E0: masuk awal / tunggu", f"{sg(a.E0_untung.mean())} / {sg(b.E0_untung.mean())}", ""],
            ["% pasangan di mana tunggu memberi untung E0 lebih tinggi", pct((b.E0_untung > a.E0_untung).mean()), ""],
            ["Median hari dari MACD hijau ke lengkap", f"{pd.to_numeric(b.hari_ke_lengkap, errors='coerce').median():.0f}", ""]]
    out.append("## 2. Kejadian yang sama: masuk awal vs tunggu (hanya yang kemudian lengkap)\n" +
               jadual(["Ukuran", "Nilai", "Nota"], rows))

    # Cara keluar bagi A dan B
    rows = []
    for nama, g in [("A. MACD hijau sahaja", M), ("B. Tunggu lengkap", L)]:
        for e in ["E0", "E1", "E2", "E3", "E4"]:
            u = g[f"{e}_untung"]
            rows.append([nama, e, sg(u.mean()), sg(u.median()), pct((u > 0).mean()), pct((u >= 0.10).mean()),
                         f"{g[f'{e}_hari'].median():.0f}"])
    out.append("## 3. Cara keluar\n" + jadual(
        ["Kumpulan", "Keluar", "Purata untung", "Median untung", "% untung", "% ≥ +10%", "Median hari"], rows))

    # Kestabilan
    rows = []
    for nama, col in [("Tempoh", "tempoh"), ("Subset", "subset"), ("Tahun", "tahun")]:
        for v in sorted(d[col].dropna().unique()):
            m, l, r = M[M[col] == v], L[L[col] == v], R[R[col] == v]
            rows.append([f"{nama}: {v}", len(m), pct((m.kelas == "Berjaya").mean()), pct((l.kelas == "Berjaya").mean()),
                         pct((r.kelas == "Berjaya").mean()), sg(m.E0_untung.mean()), sg(l.E0_untung.mean())])
    for nama, f in [("Tanpa 2020", lambda x: x[x.tahun != 2020])]:
        m, l, r = f(M), f(L), f(R)
        rows.append([nama, len(m), pct((m.kelas == "Berjaya").mean()), pct((l.kelas == "Berjaya").mean()),
                     pct((r.kelas == "Berjaya").mean()), sg(m.E0_untung.mean()), sg(l.E0_untung.mean())])
    out.append("## 4. Kestabilan (% Berjaya)\n" + jadual(
        ["Kumpulan", "Bil. MACD hijau", "A. MACD sahaja", "B. Tunggu lengkap", "C. Rawak",
         "Purata E0 (A)", "Purata E0 (B)"], rows))

    # Kriteria
    bm, bl, br = (M.kelas == "Berjaya").mean(), (L.kelas == "Berjaya").mean(), (R.kelas == "Berjaya").mean()
    tm, tl, tr = (M.kelas == "Gagal teruk").mean(), (L.kelas == "Gagal teruk").mean(), (R.kelas == "Gagal teruk").mean()
    rows = [["A. MACD sahaja lebih baik daripada rawak ≥ 5 mata (Berjaya)", f"{100 * (bm - br):+.1f} mata", "✅" if bm - br >= .05 else "❌"],
            ["A. Gagal teruk lebih rendah daripada rawak", f"{pct(tm)} vs {pct(tr)}", "✅" if tm < tr else "❌"],
            ["B. Tunggu lengkap lebih baik daripada A ≥ 5 mata (Berjaya)", f"{100 * (bl - bm):+.1f} mata", "✅" if bl - bm >= .05 else "❌"],
            ["B. Gagal teruk lebih rendah daripada A", f"{pct(tl)} vs {pct(tm)}", "✅" if tl < tm else "❌"]]
    out.append("## 5. Kriteria\n" + jadual(["Kriteria", "Nilai", "Lulus"], rows))
    return "\n".join(out)


if __name__ == "__main__":
    print(lapor(sys.argv[1]))
