#!/usr/bin/env python3
"""P01 — Uji peraturan keluar amaran (E5).
Masuk buka T0+1 (MACD hijau). Jika isyarat teras (A1, R1, Q3) belum lengkap dalam N hari selepas T0,
keluar pada buka hari berikutnya. Selepas lengkap, guna keluar asas (E0 / E1 / E3).
MACD merah sebelum lengkap → keluar (sama seperti E0). Henti −8% dipakai untuk asas E1 dan E3 sepanjang masa.
Kawalan: hari rawak yang sama seperti enjin (benih 42), keluar asas yang sama tanpa syarat amaran.
"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/claude")
import enjin_p01 as E

NS = [5, 10, 20]
ASAS = ["E0", "E1", "E3"]


def keluar_e5(ind, t0, e, N, asas):
    o, c, hist = ind["o"], ind["c"], ind["hist"]
    s = ind["sig"]
    masuk = o[e]; henti = masuk * E.P["henti"]; maxc = -np.inf; n = len(c)
    lengkap = all(s[k][t0] for k in E.TERAS_ASAS)  # lengkap pada T0 sendiri
    for k in range(e, n):
        maxc = max(maxc, c[k])
        if not lengkap and all(s[x][k] for x in E.TERAS_ASAS) and s["M1"][k]:
            lengkap = True
        stop = c[k] < henti
        merah = hist[k] < 0
        if asas == "E0":
            x = merah
        elif asas == "E1":
            x = merah or stop
        else:
            x = (c[k] < maxc - E.P["atr_mult"] * ind["atr22"][k]) or stop
        if not lengkap:
            x = x or merah or (k >= t0 + N)
        if x:
            if k + 1 < n:
                return o[k + 1] / masuk - 1, k - e + 1, lengkap
            return c[k] / masuk - 1, k - e + 1, lengkap
    return c[n - 1] / masuk - 1, n - e, lengkap


def jalan(fail_data, fail_kejadian):
    kej = pd.read_csv(fail_kejadian, low_memory=False)
    kej = kej[(kej.ufuk_penuh == True) & (kej.gap != True) & kej.status.isin(["m1 sahaja", "rawak"])]
    from collections import defaultdict
    kunci = defaultdict(list)
    for r in kej.itertuples():
        kunci[r.ticker].append((r.masuk_tarikh, r.status))
    rows = []
    for f in fail_data:
        d = pd.read_csv(f)
        for tk, g in d.groupby("ticker"):
            g = g.sort_values("date").reset_index(drop=True)
            dates = g.date.to_numpy()
            pos = {int(x): i for i, x in enumerate(dates)}
            ind = E.indikator(g, None)
            for md, st in kunci.get(tk, []):
                e = pos.get(int(md))
                if e is None:
                    continue
                t0 = e - 1
                r = dict(ticker=tk, status=st, tahun=int(md) // 10000)
                for N in NS:
                    for a in ASAS:
                        if st == "rawak":
                            # kawalan: keluar asas sahaja (tiada syarat amaran)
                            ks, px, _ = E.keluar(ind, e, a)
                            u = px / ind["o"][e] - 1; h = ks - e + 1
                        else:
                            u, h, _ = keluar_e5(ind, t0, e, N, a)
                        r[f"N{N}_{a}_u"] = u; r[f"N{N}_{a}_h"] = h
                rows.append(r)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = jalan(sys.argv[2:], sys.argv[1])
    df.to_csv("/home/claude/hasil/P4/e5.csv", index=False)
    print(len(df))
