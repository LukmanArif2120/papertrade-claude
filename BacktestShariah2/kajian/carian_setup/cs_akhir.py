"""Carian setup — KEDUDUKAN AKHIR semua setup F (SPEC pindaan 14 Nov 2026 (m)).

Mengukur apa yang belum diukur lawan matlamat pengguna, tanpa carian baharu: corong ikut ayat matlamat (naik >= 5 % minggu
pertama -> naik lagi hingga minggu ke-4), kekerapan dan liputan, sumbangan setiap komponen, mutu pegang, saham Shariah; dan
menyusun SATU jadual semua setup. Guna: python3 cs_akhir.py <kerja>   (panel_B, benih_B, lapis_B, asasL_B sudah ada).
Keluaran: hasil/KEDUDUKAN_AKHIR.md dan KEDUDUKAN_AKHIR.csv. Jangan sunting keluaran secara manual."""
import os
import sys

import numpy as np
import pandas as pd
from numba import njit, prange

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_atom as atom  # noqa: E402
import cs_cari as cari  # noqa: E402
import cs_cs05 as c5  # noqa: E402
import cs_lapor as lapor  # noqa: E402
import cs_lengkap as lg  # noqa: E402
import cs_portfolio6 as p6  # noqa: E402
import cs_ringkas  # noqa: E402
import cs_teras as teras  # noqa: E402

TMAX = teras.TMAX
MIN_BELIAN, MIN_TAHUN, JARAK_EPISOD = 300, 10, 5          # "dipercayai" dan gabungan episod: dikunci pindaan (m)
KUNCI = ('K1', 'K2', 'K3')


@njit(parallel=True, cache=True)
def label2(ev, o, l, c):
    """Lajur: m10 (tutup sesi 5 >= P + 10 %), terus (tutup sesi 5 >= P + 5 % DAN tutup sesi 20 > tutup sesi 5 DAN henti
    -8 % tidak kena dalam 20 sesi), puncak (tutup tertinggi 20 sesi / P - 1). Beli pada buka bar ev + 1."""
    out = np.zeros((ev.shape[0], 3), np.float32)
    for k in prange(ev.shape[0]):
        e = ev[k] + 1
        P = o[e]
        L = P * 0.92
        henti = c[e] <= L
        mx = c[e]
        for d in range(1, TMAX):
            if o[e + d] <= L or l[e + d] <= L:
                henti = True
            if c[e + d] > mx:
                mx = c[e + d]
        out[k, 0] = c[e + 4] >= P * 1.10
        out[k, 1] = (c[e + 4] >= P * 1.05) and (c[e + TMAX - 1] > c[e + 4]) and (not henti)
        out[k, 2] = mx / P - 1.0
    return out


def episod(lab, mula, jarak=JARAK_EPISOD):
    """ID episod pelari setiap bar (-1 = bukan): blok bar berturutan berlabel bagi satu saham; blok yang dipisahkan kurang
    `jarak` bar digabung. Pulangkan (id setiap bar, bilangan episod)."""
    ep = np.full(len(lab), -1, np.int64)
    k = 0
    for t in range(len(mula) - 1):
        a = mula[t]
        idx = np.flatnonzero(lab[a:mula[t + 1]])
        if len(idx):
            ids = k + np.cumsum(np.r_[True, np.diff(idx) > jarak]) - 1
            ep[a + idx] = ids
            k = ids[-1] + 1
    return ep, k


def main(kerja):
    pan, _, EV, X, L = c5._sedia(kerja, 'B')
    Lr, Tb = (L['L1'], L['L2']), lg.muat_asas(kerja, 'B')
    N, sah, g, ng = len(pan['c']), np.flatnonzero(pan['sah']), Tb['g'], np.maximum(Tb['n'], 1)
    Lb = label2(sah, pan['o'], pan['l'], pan['c'])
    Y = np.zeros((N, 5), np.float32)                              # m10, terus, puncak, asas m10, asas terus
    Y[sah, :3] = Lb
    for j in (0, 1):
        Y[sah, 3 + j] = (np.bincount(g[sah], Lb[:, j], minlength=len(ng)) / ng)[g[sah]]
    terus = np.zeros(N, bool)
    terus[sah] = Lb[:, 1] > 0
    ep, n_ep = episod(terus, pan['mula'])
    hu, tm = pan['hari_unik'], atom.TEMPOH['B']
    dlm = (hu >= tm[0][1]) & (hu <= tm[-1][2])
    n_tahun, n_bulan = dlm.sum() / 252, len(np.unique(hu[dlm] // 100))
    shar = set(open(os.path.join(lapor.BS2, 'data', 'harga', 'univ.txt')).read().split())
    shariah = np.asarray([t in shar for t in pan['ticker']])[pan['tid']]
    cari.log(f"kumpulan B: {len(sah):,} bar layak; asas m5 {X[sah, 0].mean() * 100:.1f}% · m10 {Lb[:, 0].mean() * 100:.1f}% · "
             f"terus {Lb[:, 1].mean() * 100:.1f}%; {n_ep:,} episod pelari; saham Shariah {int(np.isin(pan['ticker'], list(shar)).sum())}"
             f" daripada {len(pan['ticker'])}")
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('')
    with open(os.path.join(lapor.BS2, 'jejak_f', 'kohort.json')) as f:
        import json
        kohort = {a['id'] for a in json.load(f)['ahli']}

    def kl(d, ev, buang):
        """Kelebihan `terus` atas rawak hari sama (satu posisi, pegang 20 sesi) selepas membuang satu komponen."""
        q1, q2, f1, f2 = (-1 if buang == k else d[k] for k in ('q1', 'q2', 'f1', 'f2'))
        if buang == 'pencetus':
            x = sah[c5.topeng(pan, Lr, sah, q1, q2, f1, f2)]
        else:
            x = ev[c5.topeng(pan, Lr, ev, q1, q2, f1, f2)]
            x = x[teras.satu_posisi(x, np.full(len(x), TMAX - 1), pan['tid'])]
        return float((Y[x, 1] - Y[x, 4]).mean()) if len(x) >= 100 else np.nan

    # Pindaan (p): SEMUA setup dinilai di bawah pegang minimum (indikator keluar menjual paling awal pada buka sesi ke-4),
    # dengan kernel cs_keluar7; keluar lama dipetakan ke atom yang setara (cs_pegang.lama_ke_baharu, pariti diuji).
    import cs_cs07 as c7
    import cs_keluar7 as k7
    import cs_pegang as pg
    import cs_tala7 as t7
    XA = k7.siri_set(kerja, 'B')
    calon, langkau = [], []
    for r in reg.itertuples():
        cs07 = r.pusingan == 'CS07'
        if not cs07 and ('@' in r.takrif or r.pusingan == 'CS04'):
            langkau.append(r.id)
            continue
        try:
            if cs07:
                d = c7.dari_takrif7(r.takrif)
                ev = t7.ev_satu(kerja, 'B', d['pencetus'])
            else:
                d = p6.dari_takrif5(r.takrif)
                ev = EV[d['pencetus']]
                d['s'], d['kol'] = pg.lama_ke_baharu(d['lajur'])
        except (KeyError, FileNotFoundError):
            langkau.append(r.id)
            continue
        calon.append((r, cs07, d, ev))
    kolom = sorted({(d['s'], d['kol']) for _, _, d, _ in calon})
    TT7 = {c: np.zeros(len(ng)) for c in kolom}                    # asas rawak tangkap penuh di bawah mekanik yang sama
    for a in range(0, len(sah), 150_000):
        evc = sah[a:a + 150_000]
        Sc = k7.sedia_pan(pan, XA, evc)
        m5c = Sc[7][:, 0] > 0
        for c in kolom:
            Rc = k7.hasil(*Sc[:7], k7.A1, k7.A2, k7.OP, c[0], c[1])[0]
            TT7[c] += np.bincount(g[evc], (m5c & (Rc >= lg.JADI)).astype(float), minlength=len(ng))
    baris, tangkap = [], {}
    for r, cs07, d, ev in calon:
        e0 = ev[c5.topeng(pan, Lr, ev, d['q1'], d['q2'], d['f1'], d['f2'])]
        St = k7.sedia_pan(pan, XA, e0)
        R, sk = k7.hasil(*St[:7], k7.A1, k7.A2, k7.OP, d['s'], d['kol'])
        R00 = k7.hasil(*St[:7], k7.A1, k7.A2, k7.OP, d['s'], 0)[0]
        amb = teras.satu_posisi(e0, sk, pan['tid'])
        e, R = e0[amb], R[amb]
        if len(e) < 30:
            langkau.append(r.id)
            continue
        m5, trs = X[e, 0] > 0, Y[e, 1] > 0
        tp, tpd, ms = pan['tempoh'][e], pan['tarikh'][e], shariah[e]
        pen = cs_ringkas.bahagi(r.penapis)[1]
        keluar = f"{c7.HENTI_KOD[d['s']]} · {k7.kod_peraturan(d['kol'])}" if cs07 else c5.kod_keluar(d['lajur'])
        b = {'id': r.id, 'pusingan': r.pusingan, 'prasyarat': r.prasyarat, 'pencetus': cs_ringkas.nama_pendek(r.masuk),
             'penapis': r.syarat if r.syarat else pen, 'keluar': keluar, 'jejak_hadapan': 'ya' if r.id in kohort else '',
             'belian': len(e), 'hari': int(len(np.unique(tpd))), 'm5': m5.mean(), 'a_m5': X[e, 5].mean(), 'm10': Y[e, 0].mean(),
             'a_m10': Y[e, 3].mean(), 'terus': trs.mean(), 'a_terus': Y[e, 4].mean(), 'tp': (m5 & (R >= lg.JADI)).mean(),
             'a_tp': (TT7[(d['s'], d['kol'])][g[e]] / ng[g[e]]).mean(), 'menang': (R > 0).mean(), 'rugi8': (R <= lg.RUGI).mean(),
             'jual_awal': float((sk[amb] < k7.PEGANG_MIN).mean()),
             'purata': R.mean(), 'belian_setahun': len(e) / n_tahun, 'tangkap_setahun': trs.sum() / n_tahun,
             'tahun_aktif': int(len(np.unique(tpd // 10000))), 'bulan_beli': len(np.unique(tpd // 100)) / n_bulan,
             'liputan': len(np.unique(ep[e[trs]])) / n_ep}
        for i, t in enumerate(KUNCI):
            q = tp == i
            b[f'n_{t}'] = int(q.sum())
            b[f'kl_{t}'] = float((Y[e[q], 1] - Y[e[q], 4]).mean()) if q.any() else np.nan
        b['dipercayai'] = bool(b['belian'] >= MIN_BELIAN and b['tahun_aktif'] >= MIN_TAHUN
                               and all(b[f'kl_{t}'] > 0 for t in KUNCI))
        # komponen: kelebihan terus bila satu komponen dibuang
        b['kl_penuh'] = kl(d, ev, None)
        for nama, k in (('pasaran', 'q1'), ('syarikat', 'q2'), ('penapis1', 'f1'), ('penapis2', 'f2')):
            b[f'kl_tanpa_{nama}'] = kl(d, ev, k) if d[k] >= 0 else np.nan
        b['kl_tanpa_pencetus'] = kl(d, ev, 'pencetus')
        # mutu pegang: antara belian yang naik lagi
        k = e[trs]
        b.update(R_pelari=float(R[trs].mean()) if len(k) else np.nan, puncak_pelari=float(Y[k, 2].mean()) if len(k) else np.nan,
                 R_pelari_x00=float(R00[amb][trs].mean()) if len(k) else np.nan)
        # saham Shariah (senarai semasa)
        b.update(n_shariah=int(ms.sum()), terus_shariah=float(trs[ms].mean()) if ms.sum() >= 30 else np.nan,
                 a_terus_shariah=float(Y[e[ms], 4].mean()) if ms.sum() >= 30 else np.nan,
                 tp_shariah=float((m5 & (R >= lg.JADI))[ms].mean()) if ms.sum() >= 30 else np.nan,
                 menang_shariah=float((R[ms] > 0).mean()) if ms.sum() >= 30 else np.nan)
        baris.append({k_: (float(v) if isinstance(v, (np.floating, np.float32)) else v) for k_, v in b.items()})
        tangkap[r.id] = np.unique(ep[e[trs]])
    T = pd.DataFrame(baris).sort_values(['dipercayai', 'terus'], ascending=[False, False]).reset_index(drop=True)
    T.insert(0, 'kedudukan', np.arange(1, len(T) + 1))
    d_ = os.path.join(SINI, 'hasil')
    T.to_csv(os.path.join(d_, 'KEDUDUKAN_AKHIR.csv'), index=False, float_format='%.5f')
    yakin = T[T.dipercayai]
    lip_semua = len(np.unique(np.concatenate([tangkap[i] for i in yakin.id]))) / n_ep if len(yakin) else 0.0
    asas = {'m5': float(X[sah, 0].mean()), 'm10': float(Lb[:, 0].mean()), 'terus': float(Lb[:, 1].mean())}
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    p = lambda x, k=1, t=False: '–' if x is None or x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')
    ya = lambda x: '–' if x != x else ('✓' if x else '✗')
    tx = lambda x: '–' if x in ('', 'tiada') else x
    A = ['# Kedudukan akhir semua setup F (backtest pada saham yang tidak dilihat; BUKAN bukti)', '', status, '',
         'Dijana `kajian/carian_setup/cs_akhir.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (m), dikomit '
         'sebelum dijalankan. **Jangan sunting secara manual.**', '',
         '## 1. Apa yang dicari, dan cara membaca jadual', '',
         'Matlamat: setup lengkap (prasyarat → syarat → pegang → keluar, dengan henti rugi) yang paling kerap menangkap saham yang '
         '**naik ≥ 5 % pada minggu pertama (lebih baik 10 %), kemudian naik lagi hingga minggu ke-4**. Setiap setup dinilai dengan '
         f'henti dan keluarnya sendiri pada kumpulan B (saham yang carian tidak lihat), {tm[0][1]} – {tm[-1][2]}. Lajur corong = '
         'daripada 100 belian, berapa yang sampai ke setiap peringkat; angka dalam kurungan = saham rawak pada hari dan tahap '
         'turun-naik yang sama.', '',
         '- **Pegang minimum (pindaan (p), syarat pengguna 14 Nov 2026):** tiada jualan pada hari beli; indikator keluar hanya '
         'boleh menjual mulai buka sesi ke-4 (beli Isnin → paling awal Khamis); henti rugi kekal aktif sejak sesi ke-2. Semua '
         'angka di bawah dikira dengan peraturan ini. Lajur "jual awal" = belian yang dijual sebelum sesi ke-4 (henti rugi sahaja).',
         f"- Saham rawak (mana-mana hari): naik ≥ 5 % minggu pertama {p(asas['m5'])} %; ≥ 10 % minggu pertama {p(asas['m10'])} %; "
         f"**naik lagi hingga minggu ke-4 {p(asas['terus'])} %**.",
         f'- **Dipercayai** = belian ≥ {MIN_BELIAN} DAN berdagang dalam ≥ {MIN_TAHUN} tahun DAN mengatasi rawak dalam K1 (2010–19), K2 '
         '(2020–24) dan K3 (2025–26). Setup dipercayai disusun dahulu, kemudian ikut lajur "naik lagi".',
         f'- **Liputan** = daripada semua {n_ep:,} episod "naik lagi" dalam kumpulan B, berapa peratus yang dibeli setup itu. '
         'Tangkapan setahun = bilangan belian setahun yang benar-benar naik lagi.', '',
         f'## 2. Kedudukan ({len(T)} setup; {len(yakin)} dipercayai)', '',
         '| # | ID | Prasyarat | Pencetus | Penapis saham | Henti · keluar | Belian (setahun) | Naik ≥ 5 % minggu 1 % | ≥ 10 % minggu 1 % | '
         '**Naik lagi hingga minggu 4 %** | Tangkap penuh % | Menang % | Rugi ≥ 8 % % | Jual awal % | Tangkapan setahun | Tahun aktif | Liputan % | '
         'Dipercayai | Jejak hadapan |', '|---' * 19 + '|']
    for r in T.itertuples():
        A.append(f"| {r.kedudukan} | `{r.id}` | {tx(r.prasyarat)} | {r.pencetus} | {tx(r.penapis)} | {r.keluar} | "
                 f"{r.belian:,} ({r.belian_setahun:.0f}) | {p(r.m5)} ({p(r.a_m5)}) | {p(r.m10)} ({p(r.a_m10)}) | "
                 f"**{p(r.terus)}** ({p(r.a_terus)}) | {p(r.tp)} ({p(r.a_tp)}) | {p(r.menang, 0)} | {p(r.rugi8, 0)} | {p(r.jual_awal)} | "
                 f"{r.tangkap_setahun:.1f} | {r.tahun_aktif} | {p(r.liputan, 2)} | {'**ya**' if r.dipercayai else 'tidak'} | "
                 f"{r.jejak_hadapan} |")
    A += ['', f"Tidak dinilai ({len(langkau)}): {', '.join(langkau)} (anak tala `F31`–`F38`, `F70`–`F87`: memerlukan varian tala; tala "
          'terbukti tidak menolong).', '',
          '## 3. Setup dipercayai: sumbangan setiap komponen, mutu pegang, saham Shariah', '',
          'Komponen: ✓ = membuang komponen itu MENURUNKAN kelebihan "naik lagi" (ia menyumbang); ✗ = tidak; angka = kelebihan setup '
          'penuh → tanpa komponen (mata peratus). Mutu pegang = purata untung setiap belian yang naik lagi: dengan keluar setup / jika '
          'dipegang sahaja 20 sesi / puncak tutup dalam 20 sesi. Shariah = belian pada saham dalam senarai Shariah semasa.', '',
          '| ID | Prasyarat pasaran | Prasyarat syarikat | Penapis 1 | Penapis 2 | Pencetus | Mutu pegang: keluar setup / pegang 20 sesi / '
          'puncak % | Shariah: belian · naik lagi % (rawak) · tangkap penuh % · menang % |', '|---' * 8 + '|']
    komp = lambda r, n: ('–' if getattr(r, f'kl_tanpa_{n}') != getattr(r, f'kl_tanpa_{n}') else
                         f"{ya(getattr(r, f'kl_tanpa_{n}') < r.kl_penuh)} {p(r.kl_penuh, 1, True)} → {p(getattr(r, f'kl_tanpa_{n}'), 1, True)}")
    for r in yakin.itertuples():
        A.append(f"| `{r.id}` | {komp(r, 'pasaran')} | {komp(r, 'syarikat')} | {komp(r, 'penapis1')} | {komp(r, 'penapis2')} | "
                 f"{komp(r, 'pencetus')} | {p(r.R_pelari, 1, True)} / {p(r.R_pelari_x00, 1, True)} / {p(r.puncak_pelari, 1, True)} | "
                 f"{r.n_shariah:,} · {p(r.terus_shariah)} ({p(r.a_terus_shariah)}) · {p(r.tp_shariah)} · {p(r.menang_shariah, 0)} |")
    sumb = {n: (int((yakin[f'kl_tanpa_{n}'] < yakin.kl_penuh).sum()), int(yakin[f'kl_tanpa_{n}'].notna().sum()))
            for n in ('pasaran', 'syarikat', 'penapis1', 'penapis2', 'pencetus')}
    ys = yakin[yakin.terus_shariah.notna()]
    A += ['', '## 4. Bacaan', '',
          f"- Dipercayai: {len(yakin)} daripada {len(T)} setup. Kadar \"naik lagi\" setup dipercayai: {p(yakin.terus.min())} % hingga "
          f"{p(yakin.terus.max())} % (saham rawak mana-mana hari {p(asas['terus'])} %)." if len(yakin) else '- Tiada setup dipercayai.',
          f"- Kekerapan setup dipercayai: median {yakin.belian_setahun.median():.0f} belian setahun, {yakin.tangkap_setahun.median():.1f} "
          f"tangkapan setahun; liputan setiap setup {p(yakin.liputan.min(), 2)}–{p(yakin.liputan.max(), 2)} %; **semua setup dipercayai "
          f"bersama menangkap {p(lip_semua, 1)} % daripada semua episod naik lagi**." if len(yakin) else '',
          '- Komponen yang menyumbang (setup dipercayai): ' + '; '.join(
              f"{n.replace('penapis', 'penapis ').replace('pasaran', 'prasyarat pasaran').replace('syarikat', 'prasyarat syarikat')} "
              f"{a} daripada {b}" for n, (a, b) in sumb.items()) + '.',
          f"- Mutu pegang (median setup dipercayai): keluar setup {p(yakin.R_pelari.median(), 1, True)} % lawan pegang 20 sesi "
          f"{p(yakin.R_pelari_x00.median(), 1, True)} % setiap pelari; puncak {p(yakin.puncak_pelari.median(), 1, True)} %."
          if len(yakin) else '',
          f"- Saham Shariah: {len(ys)} setup dipercayai cukup belian (≥ 30); kadar naik lagi pada saham Shariah mengatasi rawak bagi "
          f"{int((ys.terus_shariah > ys.a_terus_shariah).sum())} daripadanya (median {p(ys.terus_shariah.median())} % lawan rawak "
          f"{p(ys.a_terus_shariah.median())} %)." if len(ys) else '- Saham Shariah: belian tidak cukup untuk dinilai.', '',
          '## 5. Kaveat dan apa yang MASIH belum dibuat', '',
          '- Backtest sahaja; papan ialah pangkat, BUKAN bukti. Kad skor kekal satu-satunya keputusan wang sebenar.',
          '- `F01`–`F10` dicari pada set 431 yang bertindih dengan kumpulan B; kumpulan B sudah dilihat dalam CS05/CS06.',
          '- Tiada saham delist (condong ke atas). Senarai Shariah ialah senarai semasa, bukan titik-masa. Prasyarat earnings memakai '
          'tarikh sebenar.',
          '- Belum dibuat: data saham delist; carian automatik berkala ("mesin sentiasa mencari"); peringkat papertrade bagi setup '
          'baharu (ditangguh atas arahan pengguna 14 Nov 2026).', '']
    open(os.path.join(d_, 'KEDUDUKAN_AKHIR.md'), 'w', encoding='utf-8').write('\n'.join(x for x in A if x is not None))
    cari.log(f"kedudukan akhir: {len(T)} setup, {len(yakin)} dipercayai, {len(langkau)} dilangkau; liputan gabungan {lip_semua * 100:.1f}%")


if __name__ == '__main__':
    main(sys.argv[1])
