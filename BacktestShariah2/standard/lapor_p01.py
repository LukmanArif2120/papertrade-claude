#!/usr/bin/env python3
"""Penjana laporan P01 v1.0 — baca kejadian_Vx.csv, tulis jadual ringkasan (Markdown)."""
import sys
import numpy as np
import pandas as pd

KELAS = ["Berjaya", "Sederhana", "Gagal", "Gagal teruk"]
KELUAR = ["E0", "E1", "E2", "E3", "E4"]
ISY = ["A1", "R1", "Q3", "D1", "Q1", "A2", "A3", "V1"]
NAMA = dict(M1="MACD hijau", A1="MA10>MA20", R1="RSI>50", Q3="Squeeze hijau", D1="+DI>−DI",
            Q1="Squeeze ON", A2="Atas MA50", A3="Atas MA150", V1="Volum tinggi")


def pct(x):
    return f"{100 * x:.0f}%"


def baris_kelas(g):
    n = len(g)
    r = [str(n)] + [pct((g.kelas == k).mean()) if n else "–" for k in KELAS]
    r += [f"{100 * g.naik_maks.median():+.1f}%", f"{100 * g.E0_untung.median():+.1f}%",
          f"{g.E0_hari.median():.0f}"]
    return r


def jadual(hdr, rows):
    s = "| " + " | ".join(hdr) + " |\n|" + "---|" * len(hdr) + "\n"
    for r in rows:
        s += "| " + " | ".join(map(str, r)) + " |\n"
    return s


def lapor(fail, varian="V1", top=10):
    d = pd.read_csv(fail)
    d = d[d.ufuk_penuh == True]          # ufuk 60 hari mesti penuh
    gapn = int(((d.status == "lengkap") & (d.gap == True)).sum())
    d = d[d.gap != True]
    L = d[d.status == "lengkap"]
    TL = d[d.status == "tidak lengkap"]
    R = d[d.status == "rawak"]
    out = [f"# P01 — Laporan kajian corak ({varian})\n",
           f"Kejadian lengkap: **{len(L)}** · tidak lengkap: {len(TL)} · hari rawak: {len(R)} · "
           f"dibuang (gap > 15%): {gapn} · hanya kejadian dengan ufuk 60 hari penuh.\n"]

    H = ["Turutan", "Bil.", "Berjaya ≥20%", "Sederhana", "Gagal <10%", "Gagal teruk",
         "Median naik maks", "Median untung E0", "Median hari E0"]
    rows = []
    for t, g in L.groupby("turutan"):
        rows.append([t] + baris_kelas(g))
    rows.sort(key=lambda r: -int(r[1]))
    rows = rows[:top]
    rows.append(["**Semua lengkap**"] + baris_kelas(L))
    rows.append(["Sihat (A1 terakhir)"] + baris_kelas(L[L.sihat == True]))
    rows.append(["Tidak sihat"] + baris_kelas(L[L.sihat == False]))
    rows.append(["Tidak lengkap"] + baris_kelas(TL))
    rows.append(["**Hari rawak (kawalan)**"] + baris_kelas(R))
    out.append("## 1. Turutan dan hasil (ufuk 60 hari)\n" + jadual(H, rows))

    # U2: hari relatif
    rows = []
    for k in ISY:
        col = pd.to_numeric(L[f"rel_{k}"], errors="coerce")
        aktif = (col == -1).mean()
        tiada = col.isna().mean()
        v = col[col >= 0]
        rows.append([f"{k} {NAMA[k]}", pct(aktif), pct(tiada),
                     f"{v.median():.0f}" if len(v) else "–",
                     f"{v.quantile(.25):.0f}–{v.quantile(.75):.0f}" if len(v) else "–"])
    out.append("## 2. Bila isyarat menyala selepas MACD hijau (kejadian lengkap)\n" +
               jadual(["Isyarat", "Sudah aktif sebelum", "Tidak menyala", "Median hari", "Julat 25–75%"], rows))

    # U3: matriks A sebelum B
    core = ["A1", "R1", "Q3", "D1", "Q1"]
    rows = []
    for a in core:
        ra = pd.to_numeric(L[f"rel_{a}"], errors="coerce")
        r = [a]
        for b in core:
            if a == b:
                r.append("–")
                continue
            rb = pd.to_numeric(L[f"rel_{b}"], errors="coerce")
            m = ra.notna() & rb.notna()
            r.append(pct((ra[m] < rb[m]).mean()) if m.any() else "–")
        rows.append(r)
    out.append("## 3. Peratus A menyala lebih awal daripada B (baris = A)\n" + jadual(["A \\ B"] + core, rows))

    # U6/U7: cara keluar
    rows = []
    for nama, g in [("Kejadian lengkap", L), ("Hari rawak", R)]:
        for k in KELUAR:
            u = g[f"{k}_untung"]
            nk = g[f"{k}_naik_dlm_pegang"]
            simp = (u / nk)[nk > 0.02].clip(-2, 1)
            rows.append([nama, k, f"{100 * u.mean():+.1f}%", f"{100 * u.median():+.1f}%", pct((u > 0).mean()),
                         pct((u >= 0.10).mean()), f"{simp.median():.2f}", f"{g[f'{k}_hari'].median():.0f}"])
    out.append("## 4. Cara keluar\n" + jadual(
        ["Kumpulan", "Keluar", "Purata untung", "Median untung", "% untung", "% ≥ +10%", "Nisbah simpanan", "Median hari"],
        rows))

    # U9: isyarat rekod pada hari T
    rows = []
    B = L[L.kelas == "Berjaya"]
    G = L[L.kelas.isin(["Gagal", "Gagal teruk"])]
    for r in ["D1", "Q1", "A2", "A3", "V1"]:
        c = f"diT_{r}"
        pb, pg = B[c].astype(bool).mean(), G[c].astype(bool).mean()
        rows.append([f"{r} {NAMA[r]}", pct(pb), pct(pg), f"{pb - pg:+.0%}"])
    out.append("## 5. Isyarat tambahan pada hari T: Berjaya vs Gagal\n" +
               jadual(["Isyarat", "% dalam Berjaya", "% dalam Gagal", "Beza"], rows))

    # Kestabilan
    rows = []
    L = L.assign(semua="semua"); R = R.assign(semua="semua")
    L["tanpa2020"] = np.where(L.tahun == 2020, "2020 sahaja", "tanpa 2020")
    R["tanpa2020"] = np.where(R.tahun == 2020, "2020 sahaja", "tanpa 2020")
    for nama, col in [("Tempoh", "tempoh"), ("Subset", "subset"), ("Tahun", "tahun"), ("2020", "tanpa2020")]:
        for v, g in L.groupby(col):
            rr = R[R[col] == v]
            rows.append([f"{nama}: {v}", len(g), pct((g.kelas == "Berjaya").mean()),
                         pct((rr.kelas == "Berjaya").mean()) if len(rr) else "–",
                         pct((g.kelas == "Gagal teruk").mean()),
                         pct((rr.kelas == "Gagal teruk").mean()) if len(rr) else "–"])
    out.append("## 6. Kestabilan\n" + jadual(
        ["Kumpulan", "Bil. lengkap", "Berjaya (lengkap)", "Berjaya (rawak)", "Gagal teruk (lengkap)",
         "Gagal teruk (rawak)"], rows))

    # Kriteria lulus
    besar = [(t, g) for t, g in L.groupby("turutan") if len(g) >= 100]
    t_best, g_best = max(besar, key=lambda x: (x[1].kelas == "Berjaya").mean()) if besar else ("–", L.iloc[:0])
    pb_best = (g_best.kelas == "Berjaya").mean() if len(g_best) else np.nan
    pb_r = (R.kelas == "Berjaya").mean()
    gt_l, gt_r = (L.kelas == "Gagal teruk").mean(), (R.kelas == "Gagal teruk").mean()
    pen = L[L.tempoh == "penemuan"]; pes = L[L.tempoh == "pengesahan"]
    rows = [["≥ 100 kejadian lengkap", len(L), "✅" if len(L) >= 100 else "❌"],
            [f"% Berjaya turutan terbaik (≥100 kejadian: {t_best}) ≥ 1.5 × rawak", f"{pct(pb_best)} vs {pct(pb_r)}",
             "✅" if pb_best >= 1.5 * pb_r else "❌"],
            ["% Berjaya semua lengkap melebihi rawak ≥ 5 mata",
             f"{100 * ((L.kelas == 'Berjaya').mean() - pb_r):+.1f} mata",
             "✅" if (L.kelas == 'Berjaya').mean() - pb_r >= 0.05 else "❌"],
            ["% Gagal teruk < rawak", f"{pct(gt_l)} vs {pct(gt_r)}", "✅" if gt_l < gt_r else "❌"],
            ["% Berjaya > rawak dalam penemuan DAN pengesahan",
             f"{pct((pen.kelas == 'Berjaya').mean())} / {pct((pes.kelas == 'Berjaya').mean())}",
             "✅" if ((pen.kelas == 'Berjaya').mean() > pb_r and (pes.kelas == 'Berjaya').mean() > pb_r) else "❌"]]
    out.append("## 7. Kriteria lulus\n" + jadual(["Kriteria", "Nilai", "Lulus"], rows))
    return "\n".join(out)


if __name__ == "__main__":
    print(lapor(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "V1"))
