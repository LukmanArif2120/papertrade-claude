"""Carian setup — pusingan CS24 (SPEC pindaan 17 Nov 2026 (ak)): kumpulan "SAHAM TENANG".

Alam = bar isyarat dengan `ATR% <= 2.5` (penapis F24). Cara pegang T5 (satu-satunya): beli buka esok (P); puncak = maksimum P dan
setiap tutup sejak hari beli; tutup <= 0.95 x puncak -> jual pada buka sesi berikutnya; had teknikal 252 sesi. Sasaran = label
`t5` (pulangan bersih T5 > 0, "dijual dengan untung") lawan saham tenang rawak pada hari yang sama yang dipegang cara sama.
Ruang, syarat kekerapan mingguan, kawalan dan enjin skor = CS20 (`cs_mingguan20`); isyarat setiap pencetus ditapis kepada alam
tenang (dan dagangan yang selesai dalam data) SEBELUM skor. "Lulus" pada kumpulan B = kelebihan `t5` > 0 dalam K1, K2 dan K3.
Guna: python3 cs_tenang24.py skor|calon|kunci|lapor|daftar <kerja>. Jangan sunting keluaran secara manual."""
import json
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd
from numba import njit, prange

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_atom as atom  # noqa: E402
import cs_cari as cari  # noqa: E402
import cs_cs05 as c5  # noqa: E402
import cs_daftar13 as d13  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_mingguan20 as m20  # noqa: E402
import cs_semak11 as s11  # noqa: E402
import cs_tala7 as t7  # noqa: E402
import cs_teras as teras  # noqa: E402

# ---- pemalar dikunci pindaan (ak); selebihnya = pemalar CS20 ----
PUS, TARIKH = 'CS24', '2026-11-17'
BENIH_KAWALAN = 20261119
JATUH, HAD, KOS = 0.05, 252, teras.KOS
I_TENANG = atom.PENAPIS.index('F24 ATR% <= 2.5')
MIN_BELIAN, MIN_TAHUN, MIN_TAHUN_N = 300, 10, 20
N_PAPAR = 40
F_ = lambda kerja, nama: os.path.join(kerja, f'cs24_{nama}.pkl')
_A24 = {}


@njit(cache=True, parallel=True)
def label_t5(ev, akhir, o, c, jatuh, had, kos):
    """Setiap bar isyarat ev (akhir[k] = bar terakhir saham itu): (pulangan bersih, sesi keluar, selesai?, capai had?).
    Beli pada buka ev + 1; puncak = maks(P, tutup sejak hari beli); tutup <= (1 - jatuh) x puncak -> jual buka esok.
    Sesi keluar mengikut `teras.satu_posisi` (bar keluar = ev + 1 + sk). Dagangan yang belum dijual apabila data saham itu
    tamat, atau yang menyentuh harga tidak sah, ditanda tidak selesai."""
    n = ev.shape[0]
    R = np.zeros(n, np.float64)
    sk = np.zeros(n, np.int64)
    siap = np.zeros(n, np.bool_)
    cap = np.zeros(n, np.bool_)
    for k in prange(n):
        e = ev[k] + 1
        if e > akhir[k]:
            continue
        P = o[e]
        if not (P > 0.0):
            continue
        puncak = P
        for d in range(had):
            b = e + d
            if b > akhir[k]:
                break
            cb = c[b]
            if not (cb > 0.0):
                break
            if cb > puncak:
                puncak = cb
            if cb <= (1.0 - jatuh) * puncak:
                if b + 1 > akhir[k] or not (o[b + 1] > 0.0):
                    break
                R[k], sk[k], siap[k] = o[b + 1] / P - 1.0 - kos, d + 1, True
                break
            if d == had - 1:
                R[k], sk[k], siap[k], cap[k] = cb / P - 1.0 - kos, d, True, True
    return R, sk, siap, cap


def asas24(pan):
    """Label T5 setiap bar tenang layak + asas "saham tenang rawak hari sama" (purata label dan pulangan bar tenang yang selesai
    pada hari itu) dan asas era. S = topeng bar yang dinilai (tenang, layak, dagangan selesai)."""
    N = len(pan['c'])
    idx = np.flatnonzero(pan['F'][I_TENANG].astype(bool) & pan['sah'])
    akhir = (pan['mula'][pan['tid'][idx] + 1] - 1).astype(np.int64)
    R, sk, siap, cap = label_t5(idx.astype(np.int64), akhir, pan['o'], pan['c'], JATUH, HAD, KOS)
    b = idx[siap]
    S = np.zeros(N, np.bool_)
    S[b] = True
    Lab, Ret, SK, Cap = np.zeros(N, np.float32), np.zeros(N), np.zeros(N, np.int64), np.zeros(N, np.bool_)
    Lab[b], Ret[b], SK[b], Cap[b] = (R[siap] > 0).astype(np.float32), R[siap], sk[siap], cap[siap]
    hari = pan['hari'][b]
    bil = np.maximum(np.bincount(hari), 1)
    AsL, AsR, AsE = np.zeros(N, np.float32), np.zeros(N), np.zeros(N, np.float32)
    AsL[b] = (np.bincount(hari, Lab[b]) / bil)[hari]
    AsR[b] = (np.bincount(hari, Ret[b]) / bil)[hari]
    tp = pan['tempoh'][b].astype(np.int64)
    AsE[b] = (np.bincount(tp, Lab[b]) / np.maximum(np.bincount(tp), 1))[tp]
    return dict(S=S, Lab=Lab, Ret=Ret, SK=SK, Cap=Cap, AsL=AsL, AsR=AsR, AsE=AsE, n_tenang=int(len(idx)), n_selesai=int(len(b)))


def a24(kerja, set_):
    if set_ not in _A24:
        _A24[set_] = asas24(cari.panel(kerja, set_))
    return _A24[set_]


def pasang_alam(kerja, set_):
    """Tapis isyarat setiap pencetus kepada alam tenang (dan dagangan selesai) dan letak dalam cache `cs_mingguan20`, supaya skor,
    kekerapan, calon dan kawalan CS20 semuanya berjalan atas alam yang sama."""
    if ('tenang', set_) in _A24:
        return m20._EV[set_]
    S = a24(kerja, set_)['S']
    m20._EV.pop(set_, None)
    mentah = m20.semua_pencetus(kerja, set_)
    m20._EV[set_] = {n: np.ascontiguousarray(ev[S[ev]]) for n, ev in mentah.items()}
    _A24[('tenang', set_)] = True
    return m20._EV[set_]


def v_t5(A):
    V = np.zeros((len(A['S']), 3))
    b = np.flatnonzero(A['S'])
    V[b, 0], V[b, 1], V[b, 2] = A['Lab'][b], A['AsL'][b], A['AsE'][b]
    return V


def ukur24(pan, A, ev):
    """Statistik satu peraturan di bawah T5 (satu posisi setiap saham sehingga dijual)."""
    ev = np.ascontiguousarray(ev[A['S'][ev]], dtype=np.int64)
    e = ev[teras.satu_posisi(ev, A['SK'][ev], pan['tid'])] if len(ev) else ev
    thn = pan['tarikh'][e] // 10000
    d = dict(n=int(len(e)), tahun=int(len(np.unique(thn))), e=e.astype(np.int32))
    if not len(e):
        return d
    lab, ret = A['Lab'][e].astype(float), A['Ret'][e]
    x = lab - A['AsL'][e]
    d.update(menang=float(lab.mean()), a_menang=float(A['AsL'][e].mean()), kl_t5=float(x.mean()), purata=float(ret.mean()),
             a_purata=float(A['AsR'][e].mean()), tengah=float(np.median(ret)), p05=float(np.percentile(ret, 5)),
             hari=float(np.median(A['SK'][e]) + 1), hari_p90=float(np.percentile(A['SK'][e], 90) + 1), had=float(A['Cap'][e].mean()))
    tp = pan['tempoh'][e]
    for p in range(3):
        q = tp == p
        d[f'n_K{p + 1}'] = int(q.sum())
        d[f'kl_t5_K{p + 1}'] = float(x[q].mean()) if q.any() else np.nan
    g = pd.Series(x).groupby(thn).agg(['size', 'mean'])
    g = g[g['size'] >= MIN_TAHUN_N]
    d['tahun_n'], d['tahun_pos'] = int(len(g)), float((g['mean'] > 0).mean()) if len(g) else np.nan
    return d


# ---------- langkah ----------
def skor(kerja):
    A = a24(kerja, 'A')
    pasang_alam(kerja, 'A')
    cari.log(f"CS24 skor: alam tenang A {A['n_tenang']} bar layak, {A['n_selesai']} dagangan selesai; menang rawak "
             f"{A['Lab'][A['S']].mean():.4f}")
    return m20.skor(kerja, V=v_t5(A), F=F_)


def calon(kerja):
    pasang_alam(kerja, 'A')
    return m20.calon(kerja, F=F_, benih=BENIH_KAWALAN, awalan='Z')


def kunci(kerja):
    """Nilai setiap calon dan kawalan pada kumpulan B di bawah T5 (+ kekerapan pada A dan B, ukuran utama `terus` sebagai
    maklumat) -> cs24_kunci.pkl"""
    C = pickle.load(open(F_(kerja, 'calon'), 'rb'))
    semua_ = pd.concat([C['calon'], C['kawalan']], ignore_index=True)
    param = t7.param_semua(kerja)
    out, t0 = {}, time.time()
    for set_ in ('B', 'A'):
        pan = cari.panel(kerja, set_)
        L = lapis.muat(kerja, set_)
        Lr = (L['L1'], L['L2'])
        EV = pasang_alam(kerja, set_)
        M = m20.minggu(pan['hari_unik'], set_)
        A = a24(kerja, set_)
        if set_ == 'B':
            Lab, As = s11.asas(pan)
        for k, r in enumerate(semua_.itertuples(), 1):
            ev = EV[r.pencetus]
            ev = ev[c5.topeng(pan, Lr, ev, r.q1, r.q2, r.f1, r.f2)]
            o = out.setdefault(r.id, {})
            mg, mt, _ = m20.kekerapan(M, pan['hari'][m20.entri(pan, ev)])
            o['mgg_' + set_], o['mgg_min_' + set_] = mg, mt
            if set_ == 'B':
                o['t5'] = ukur24(pan, A, ev)
                o['d'] = s11.ukur_tangkap(pan, Lab, As, ev, m20.S_HENTI)[0]
                o.update(nama=t7.nama7(r.pencetus, param), prasyarat=d13.teks_pra(r.q1, r.q2), penapis=d13.teks_pen(r.f1, r.f2))
            if k % 500 == 0:
                cari.log(f'  CS24 kunci {set_} {k}/{len(semua_)} · {time.time() - t0:.0f}s')
        if set_ == 'B':
            b = np.flatnonzero(A['S'])
            out['_dasar'] = dict(n_tenang=A['n_tenang'], n_selesai=A['n_selesai'], menang=float(A['Lab'][b].mean()),
                                 purata=float(A['Ret'][b].mean()), tengah=float(np.median(A['Ret'][b])),
                                 p05=float(np.percentile(A['Ret'][b], 5)), hari=float(np.median(A['SK'][b]) + 1),
                                 had=float(A['Cap'][b].mean()))
    pickle.dump(out, open(F_(kerja, 'kunci'), 'wb'), protocol=4)
    cari.log(f'CS24 kunci: {len(out) - 1} peraturan · {time.time() - t0:.0f}s')
    return out


L24 = ('n', 'tahun', 'menang', 'a_menang', 'kl_t5', 'kl_t5_K1', 'kl_t5_K2', 'kl_t5_K3', 'purata', 'a_purata', 'tengah', 'p05', 'hari',
       'hari_p90', 'had', 'tahun_n', 'tahun_pos')


def bacaan(T):
    """Bacaan dikunci pindaan (ak) atas peraturan yang cukup belian."""
    c, k = T[(T.peranan == 'calon') & T.layak], T[(T.peranan == 'kawalan') & T.layak]
    f = lambda x: float(x) if len(c) and len(k) else np.nan
    o = dict(n_calon=int((T.peranan == 'calon').sum()), calon_layak=len(c), kawalan_layak=len(k), n_lulus=int(c.lulus.sum()),
             lulus_calon=f(c.lulus.mean()), lulus_kawalan=f(k.lulus.mean()),
             k3_calon=f((c.kl_t5_K3 > 0).mean()), k3_kawalan=f((k.kl_t5_K3 > 0).mean()))
    o['b1'] = bool(o['lulus_calon'] >= o['lulus_kawalan'] + d13.B1_BEZA)
    o['b2'] = bool(o['k3_calon'] >= d13.B2_MIN and o['k3_calon'] >= o['k3_kawalan'] + d13.B2_BEZA)
    o['ya'] = bool(o['b1'] and o['b2'])
    o['nasib'] = float(o['lulus_kawalan'] / o['lulus_calon']) if o['lulus_calon'] and o['lulus_calon'] == o['lulus_calon'] else np.nan
    return o


def kembar(T, K):
    """Calon 'boleh' ikut skor A menurun; yang beliannya (kumpulan B) bertindih Jaccard >= 0.80 dengan calon lebih tinggi yang
    sudah diterima ditanda kembar."""
    terima, kb = [], {}
    for r in T[T.boleh].sort_values('skor', ascending=False, kind='stable').itertuples():
        e = set(K[r.id]['t5']['e'].tolist())
        for i, s in terima:
            u = len(e | s)
            if u and len(e & s) / u >= d13.JACCARD:
                kb[r.id] = i
                break
        else:
            terima.append((r.id, e))
    return kb


def semua(kerja):
    C = pickle.load(open(F_(kerja, 'calon'), 'rb'))
    K = pickle.load(open(F_(kerja, 'kunci'), 'rb'))
    T = pd.concat([C['calon'].assign(peranan='calon'), C['kawalan'].assign(peranan='kawalan')], ignore_index=True)
    for k_ in L24:
        T[k_] = [K[i]['t5'].get(k_, np.nan) for i in T.id]
    for k_ in ('mgg_B', 'mgg_min_B'):
        T[k_] = [K[i].get(k_, np.nan) for i in T.id]
    for k_ in ('nama', 'prasyarat', 'penapis'):
        T[k_] = [K[i].get(k_, '') for i in T.id]
    T['terus'] = [K[i]['d'].get('terus', np.nan) for i in T.id]
    T['a_terus'] = [K[i]['d'].get('a_terus', np.nan) for i in T.id]
    T['kerap_B'] = (T.mgg_B >= m20.MINGGU_MIN) & (T.mgg_min_B >= m20.TAHUN_MIN)
    T['layak'] = (T.n >= MIN_BELIAN) & (T.tahun >= MIN_TAHUN)
    T['lulus'] = T.layak & (T.kl_t5_K1 > 0) & (T.kl_t5_K2 > 0) & (T.kl_t5_K3 > 0)
    B = bacaan(T)
    T['boleh'] = (T.peranan == 'calon') & T.lulus & T.kerap_B & (T.purata > T.a_purata)
    kb = kembar(T, K)
    T['kembar_kepada'] = [kb.get(i, '') for i in T.id]
    T['untuk_daftar'] = T.boleh & (T.kembar_kepada == '')
    B['dasar'] = K['_dasar']
    B['n_boleh'], B['n_untuk_daftar'] = int(T.boleh.sum()), int(T.untuk_daftar.sum())
    return C, K, T, B


def daftar(kerja):
    """Pendaftaran HANYA jika bacaan dikunci lulus (pindaan (ak)). Kod F kumpulan "tenang" ditulis oleh langkah berasingan."""
    _, _, T, B = semua(kerja)
    if not B['ya']:
        cari.log('CS24 daftar: bacaan dikunci TIDAK lulus -> tiada kod F baharu')
        return 0
    cari.log(f"CS24 daftar: bacaan lulus; {int(T.untuk_daftar.sum())} calon untuk didaftarkan (senarai_tenang.csv)")
    return int(T.untuk_daftar.sum())


def lapor_(kerja):
    C, K, T, B = semua(kerja)
    d_ = os.path.join(SINI, 'hasil', PUS)
    os.makedirs(d_, exist_ok=True)
    c, kw = T[T.peranan == 'calon'], T[T.peranan == 'kawalan']
    c.drop(columns=['peranan']).to_csv(os.path.join(d_, 'calon.csv.gz'), index=False, float_format='%.5f')
    kw.drop(columns=['peranan', 'kembar_kepada', 'untuk_daftar', 'boleh']).to_csv(os.path.join(d_, 'kawalan.csv'), index=False,
                                                                                    float_format='%.5f')
    json.dump({k_: (v if not isinstance(v, (np.floating, np.integer)) else float(v)) for k_, v in B.items()},
              open(os.path.join(d_, 'bacaan.json'), 'w'), indent=1, ensure_ascii=False)
    D = c[c.untuk_daftar].sort_values('skor', ascending=False, kind='stable')
    if B['ya']:
        D.drop(columns=['peranan']).to_csv(os.path.join(d_, 'senarai_tenang.csv'), index=False, float_format='%.5f')
    cl, kl = c[c.layak], kw[kw.layak]
    p = lambda x, n=1: '–' if x != x else f'{100 * x:.{n}f} %'
    s = lambda x, n=2: '–' if x != x else f'{100 * x:+.{n}f}'
    med = lambda df, k_: float(df[k_].median()) if len(df) else np.nan
    ds = B['dasar']
    Ls = c[c.lulus]
    baris = [
        f'# CS24 — kumpulan "saham tenang" (pindaan (ak), {TARIKH})',
        '',
        'Dijana `cs_tenang24.py`; jangan sunting. Pangkat backtest, BUKAN bukti dan BUKAN keputusan wang sebenar. Tiada saham delist.',
        '',
        '## Takrif (dikunci sebelum dijalankan)',
        '',
        f'- Alam: bar isyarat dengan ATR14 ÷ tutup ≤ 2.5 %. Cara pegang T5: beli buka esok; jual pada buka selepas tutup pertama ≤ 95 % '
        f'tutup tertinggi sejak beli (termasuk harga beli); had teknikal {HAD} sesi; kos {100 * KOS:.1f} %.',
        '- "Berjaya" = dijual dengan untung. "Rawak" = saham tenang lain yang dibeli pada hari sama dan dipegang cara sama.',
        '',
        '## Saham tenang rawak di bawah T5 (kumpulan B, semua bar layak)',
        '',
        f"- {ds['n_selesai']:,} dagangan selesai daripada {ds['n_tenang']:,} bar tenang layak. Dijual dengan untung {p(ds['menang'])}; purata "
        f"{s(ds['purata'])} %; nilai tengah {s(ds['tengah'])} %; persentil ke-5 {s(ds['p05'])} %; nilai tengah pegang {ds['hari']:.0f} sesi; "
        f"mencapai had {HAD} sesi {p(ds['had'], 2)}.",
        '',
        '## Bacaan dikunci',
        '',
        '| Semakan | Calon | Peraturan rawak | Perlu | Keputusan |',
        '|---|---|---|---|---|',
        f"| B1: lulus (kelebihan > 0 dalam K1, K2, K3) | {p(B['lulus_calon'])} ({B['n_lulus']} / {B['calon_layak']}) | {p(B['lulus_kawalan'])} "
        f"({B['kawalan_layak']} layak) | beza ≥ 20 mata | {'LULUS' if B['b1'] else 'GAGAL'} |",
        f"| B2: lebih baik daripada rawak pada 2025–26 | {p(B['k3_calon'])} | {p(B['k3_kawalan'])} | ≥ 60 % dan beza ≥ 10 mata | "
        f"{'LULUS' if B['b2'] else 'GAGAL'} |",
        '',
        f"**Keputusan: {'LULUS' if B['ya'] else 'GAGAL'}.** " + (f"{B['n_untuk_daftar']} calon untuk didaftarkan ({B['n_boleh']} lulus semua syarat; "
        "selebihnya kembar)." if B['ya'] else 'Tiada kod baharu.'),
        '',
        '## Nilai tengah (peraturan yang cukup belian, kumpulan B)',
        '',
        '| Kumpulan | Bil. | Untung % (rawak) | Kelebihan K1 / K2 / K3 (mata) | Purata % (rawak) | Nilai tengah % | Persentil ke-5 % | Pegang (sesi) | Tahun positif |',
        '|---|---|---|---|---|---|---|---|---|',
    ]
    for nm, df in (('Calon', cl), ('Calon lulus', Ls), ('Peraturan rawak', kl)):
        baris.append(f"| {nm} | {len(df)} | {100 * med(df, 'menang'):.1f} ({100 * med(df, 'a_menang'):.1f}) | {s(med(df, 'kl_t5_K1'))} / "
                     f"{s(med(df, 'kl_t5_K2'))} / {s(med(df, 'kl_t5_K3'))} | {s(med(df, 'purata'))} ({s(med(df, 'a_purata'))}) | "
                     f"{s(med(df, 'tengah'))} | {s(med(df, 'p05'))} | {med(df, 'hari'):.0f} | {p(med(df, 'tahun_pos'), 0)} |" if len(df) else
                     f'| {nm} | 0 | – | – | – | – | – | – | – |')
    atas = (D if B['ya'] else Ls.sort_values('kl_t5', ascending=False, kind='stable')).head(N_PAPAR)
    baris += ['', f"## {'Calon untuk didaftarkan' if B['ya'] else 'Calon lulus teratas ikut kelebihan (REKOD sahaja, tiada kod)'} — {len(atas)} teratas",
              '', '| Id | Isyarat beli | Prasyarat | Syarat saham | Belian | Untung % (rawak) | K1 / K2 / K3 | Purata % (rawak) | Pegang | Minggu ada belian |',
              '|---|---|---|---|---|---|---|---|---|---|']
    for r in atas.itertuples():
        baris.append(f"| {r.id} | {r.nama} | {r.prasyarat or '–'} | {r.penapis or '–'} | {r.n:,} | {100 * r.menang:.1f} ({100 * r.a_menang:.1f}) | "
                     f"{s(r.kl_t5_K1, 1)} / {s(r.kl_t5_K2, 1)} / {s(r.kl_t5_K3, 1)} | {s(r.purata)} ({s(r.a_purata)}) | {r.hari:.0f} | {p(r.mgg_B, 0)} |")
    baris += ['', f"Calon: {len(c)} daripada {C['calon'].pencetus.nunique() if len(C['calon']) else 0} isyarat beli ({C['tinjau']} peraturan ditinjau); "
              f"kawalan {len(kw)} peraturan rawak (benih {BENIH_KAWALAN}). Fail: `calon.csv.gz`, `kawalan.csv`, `bacaan.json`.", '']
    open(os.path.join(d_, 'TENANG.md'), 'w', encoding='utf-8').write('\n'.join(baris))
    cari.log(f"CS24 lapor: B1 {'lulus' if B['b1'] else 'GAGAL'}, B2 {'lulus' if B['b2'] else 'GAGAL'} -> {os.path.join(d_, 'TENANG.md')}")
    return B


if __name__ == '__main__':
    cmd, kerja = sys.argv[1], sys.argv[2]
    {'skor': skor, 'calon': calon, 'kunci': kunci, 'lapor': lapor_, 'daftar': daftar}[cmd](kerja)
