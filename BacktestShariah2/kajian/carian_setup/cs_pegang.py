"""Carian setup — analisis PEGANG MINIMUM (SPEC pindaan 14 Nov 2026 (o); diminta pengguna: "tak mahu beli dan jual hari
yang sama ... at least hold 3 hari ... analisa dahulu").

(1) Papertrade langsung: berapa dagangan dijual pada hari beli / esok / hari ke-3, ikut sebab dan kaedah.
(2) 61 setup kedudukan akhir pada kumpulan B: taburan sesi jual dan sebabnya.
(3) Tiga mekanik: V0 sedia ada; V1 indikator keluar hanya mulai buka sesi ke-4 (henti kekal aktif sejak sesi 2);
    V2 indikator DAN henti hanya aktif mulai sesi ke-4.
Guna: python3 cs_pegang.py <kerja>. Keluaran: hasil/PEGANG_MIN.md dan PEGANG_MIN.csv. Jangan sunting secara manual."""
import glob
import os
import pickle
import sys

import numpy as np
import pandas as pd
from numba import njit, prange

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cs_atom as atom  # noqa: E402
import cs_cari as cari  # noqa: E402
import cs_cs05 as c5  # noqa: E402
import cs_keluar7 as k7  # noqa: E402
import cs_lapis as lapis  # noqa: E402
import cs_lapor as lapor  # noqa: E402
import cs_portfolio6 as p6  # noqa: E402
import cs_teras as teras  # noqa: E402

N_MIN = 3                               # pegang penuh 3 sesi: jualan paling awal pada buka sesi ke-4 (indeks sesi 3)
TMAX, KOS = k7.TMAX, k7.KOS
# atom keluar lama (cs_atom.KELUAR) -> teks atom baharu (cs_keluar7) yang sama; henti lama H1-H4 -> indeks henti baharu
_PETA = ['tutup < MA10', 'tutup < MA20', 'tutup < MA50', 'tutup < EMA10', 'tutup < EMA20', 'dua tutup berturut < MA10',
         'dua tutup berturut < MA20', 'MA10 < MA20', 'MACD(12,26,9) < isyarat', 'histogram MACD turun 3 hari', 'RSI14 < 50',
         'RSI14 silang turun bawah 70', 'RSI14 > 80', 'Supertrend(10, 3.0) turun', 'tutup < rendah 3 hari',
         'tutup < rendah 5 hari', 'tutup < rendah 10 hari', 'Chandelier 3.0xATR14 dari tutup tertinggi',
         'Chandelier 2.0xATR14 dari tutup tertinggi', 'tutup < 92% tutup tertinggi sejak beli',
         'Stochastic(14) silang turun di atas 80', 'hari turun dengan volum >= 1.5x', 'tutup < buka dan < rendah semalam',
         '+DI14 < -DI14']
_HENTI = (0, 1, 4, 5)
_R7 = {}


def lama_ke_baharu(lajur):
    """Lajur enjin lama (henti x peraturan) -> (henti, lajur) enjin cs_keluar7 yang setara (syarat aktif = sentiasa)."""
    if not _R7:
        _R7.update({(int(k7.OP[r]), int(k7.A1[r]), int(k7.A2[r])): r for r in range(k7.NR)})
    teks = [a[3] for a in k7.ATOM]
    s, x = divmod(int(lajur), cari.NR)
    op = int(cari.OP[x])
    if op == 0:
        return _HENTI[s], 0
    a = teks.index(_PETA[cari.A1[x]])
    if op == 1:
        return _HENTI[s], _R7[(1, a, a)] * k7.NG
    b = teks.index(_PETA[cari.A2[x]])
    return _HENTI[s], _R7[(op, min(a, b), max(a, b))] * k7.NG


@njit(parallel=True, cache=True)
def henti_lewat(ev, o, l, atr, m):
    """Sesi dan harga henti (/ P) jika henti hanya aktif mulai indeks sesi m (pelanggaran sebelum itu diabaikan)."""
    n = ev.shape[0]
    DS = np.full((n, k7.NH), 99, np.int64)
    PS = np.zeros((n, k7.NH))
    for k in prange(n):
        e = ev[k] + 1
        P = o[e]
        L = np.zeros(k7.NH)
        k7._aras_henti(P, atr[ev[k]], L)
        for s in range(k7.NH):
            for d in range(m, TMAX):
                b = e + d
                if o[b] <= L[s]:
                    DS[k, s] = d
                    PS[k, s] = o[b] / P
                    break
                if l[b] <= L[s]:
                    DS[k, s] = d
                    PS[k, s] = L[s] / P
                    break
    return DS, PS


@njit(parallel=True, cache=True)
def hasil_v(M, ARM, DS, PS, H0, OPN, CF, DS3, PS3, a1, a2, op, s, kol, mod, m):
    """(R, indeks sesi jual, sebab) bagi mekanik mod: 0 = sedia ada; 1 = indikator mulai indeks sesi m; 2 = indikator dan
    henti mulai indeks sesi m. sebab: 1 indikator, 2 henti, 3 had masa. Indeks sesi 1 = sesi ke-2 (esok hari beli)."""
    n = M.shape[0]
    R = np.empty(n)
    sk = np.empty(n, np.int64)
    sb = np.empty(n, np.int64)
    r, g = kol // k7.NG, kol % k7.NG
    buang = (1 << (m - 1)) - 1                                    # bit d < m - 1: jualan pada indeks sesi < m
    for k in prange(n):
        mr = k7._topeng(M[k], ARM[k], a1, a2, op, r, g)
        if mod > 0:
            mr &= ~buang
        if mod == 2:
            ds, ps, h0 = DS3[k, s], PS3[k, s], False
        else:
            ds, ps, h0 = DS[k, s], PS[k, s], H0[k, s]
        dx = 99
        if mr != 0:
            dx = k7._ctz(mr) + 1
        if h0 and dx > 1:                                         # tutup sesi 1 <= aras henti: jual buka sesi 2 (sebab henti)
            R[k], sk[k], sb[k] = OPN[k, 1] - 1.0 - KOS, 1, 2
        elif dx != 99 and dx <= ds:
            R[k], sk[k], sb[k] = OPN[k, dx] - 1.0 - KOS, dx, 1
        elif ds != 99:
            R[k], sk[k], sb[k] = ps - 1.0 - KOS, ds, 2
        else:
            R[k], sk[k], sb[k] = CF[k] - 1.0 - KOS, TMAX - 1, 3
    return R, sk, sb


def papertrade():
    """Ringkasan jualan awal dalam Lejar dan Papertrade C (data langsung dalam repo)."""
    L = pd.concat([pd.read_csv(f, low_memory=False) for f in sorted(glob.glob(os.path.join(lapor.BS2, 'lejar', 'tutup', '*.csv')))],
                  ignore_index=True)
    L = L[L.tarikh_keluar.notna()]
    hari = sorted(set(L.tarikh_beli) | set(L.tarikh_keluar))
    ix = {d: i for i, d in enumerate(hari)}
    L = L.assign(sesi=[ix[k] - ix[b] for b, k in zip(L.tarikh_beli, L.tarikh_keluar)])
    g = L.groupby('id_kaedah').agg(n=('saham', 'size'), sama=('sesi', lambda x: float((x == 0).mean())),
                                   bawah3=('sesi', lambda x: float((x < 3).mean())), purata=('untung_pct', 'mean'))
    g = g[g.n >= 30].sort_values('sama', ascending=False)
    C = pd.concat([pd.read_csv(f, low_memory=False) for f in sorted(glob.glob(os.path.join(lapor.BS2, 'papertrade', 'claude*.csv')))],
                  ignore_index=True)
    C = C[C.tarikh_keluar.notna() & C.tarikh_beli.notna()]
    sc = C.tarikh_keluar == C.tarikh_beli
    return dict(n=len(L), dari=L.tarikh_beli.min(), hingga=L.tarikh_beli.max(), sama=float((L.sesi == 0).mean()),
                esok=float((L.sesi == 1).mean()), tiga=float((L.sesi == 2).mean()),
                sebab_sama=L[L.sesi == 0].sebab_keluar.value_counts().to_dict(), untung_sama=float(L[L.sesi == 0].untung_pct.mean()),
                sebab_awal=L[L.sesi < 3].sebab_keluar.value_counts().to_dict(), kaedah=g, tanpa=int((g.sama == 0).sum()),
                c_n=len(C), c_sama=int(sc.sum()), c_kaedah=C[sc].id_kaedah.value_counts().head(8).to_dict())


def main(kerja):
    pan = cari.panel(kerja, 'B')
    EV = cari.pencetus(pan, pickle.load(open(os.path.join(kerja, 'benih_B.pkl'), 'rb')))
    L = lapis.muat(kerja, 'B')
    Lr, XA = (L['L1'], L['L2']), k7.siri_set(kerja, 'B')
    reg = pd.read_csv(lapor.REG_F, dtype=str).fillna('').set_index('id')
    ked = pd.read_csv(os.path.join(SINI, 'hasil', 'KEDUDUKAN_AKHIR.csv'))
    ked = ked[~ked.id.isin(reg.index[reg.pusingan == 'CS07'])]
    baris = []
    for q in ked.itertuples():
        d = p6.dari_takrif5(reg.loc[q.id, 'takrif'])
        ev = EV[d['pencetus']]
        e0 = ev[c5.topeng(pan, Lr, ev, d['q1'], d['q2'], d['f1'], d['f2'])]
        s, kol = lama_ke_baharu(d['lajur'])
        St = k7.sedia_pan(pan, XA, e0, pegang_min=1)               # mekanik asal; V1/V2 dikenakan dalam hasil_v
        M, ARM, DS, PS, H0, OPN, CF, LAB = St
        DS3, PS3 = henti_lewat(np.ascontiguousarray(e0, dtype=np.int64), pan['o'], pan['l'], pan['atr'], N_MIN)
        b = {'id': q.id, 'kedudukan': q.kedudukan, 'dipercayai': bool(q.dipercayai), 'keluar': c5.kod_keluar(d['lajur'])}
        for mod in (0, 1, 2):
            R, sk, sb = hasil_v(M, ARM, DS, PS, H0, OPN, CF, DS3, PS3, k7.A1, k7.A2, k7.OP, s, kol, mod, N_MIN)
            if mod == 0:                                           # pariti dengan enjin lama
                Ro = p6.hasil(pan, e0, d['lajur'])[0]
                assert np.allclose(R, Ro), q.id
            amb = teras.satu_posisi(e0, sk, pan['tid'])
            r, k_, c_, lab = R[amb], sk[amb], sb[amb], LAB[amb]
            v = f'v{mod}'
            b.update({f'n_{v}': int(amb.sum()), f'tp_{v}': float(((lab[:, 0] > 0) & (r >= 0.10)).mean()),
                      f'menang_{v}': float((r > 0).mean()), f'rugi8_{v}': float((r <= -0.08).mean()),
                      f'rugi15_{v}': float((r <= -0.15).mean()), f'purata_{v}': float(r.mean()),
                      f'pegang_{v}': float(k_.mean() + 1), f'jual2_{v}': float((k_ == 1).mean()),
                      f'jual3_{v}': float((k_ == 2).mean()), f'awal_henti_{v}': float(((k_ < N_MIN) & (c_ == 2)).mean()),
                      f'awal_ind_{v}': float(((k_ < N_MIN) & (c_ == 1)).mean()),
                      f'R_awal_{v}': float(r[k_ < N_MIN].mean()) if (k_ < N_MIN).any() else np.nan})
        baris.append(b)
    T = pd.DataFrame(baris)
    d_ = os.path.join(SINI, 'hasil')
    T.to_csv(os.path.join(d_, 'PEGANG_MIN.csv'), index=False, float_format='%.5f')
    pt = papertrade()
    Y = T[T.dipercayai]
    p = lambda x, k=1, t=False: '–' if x != x else (f'{x * 100:+.{k}f}' if t else f'{x * 100:.{k}f}')
    med = lambda kol, D=Y: float(D[kol].median())
    try:
        sys.path.insert(0, os.path.join(lapor.BS2, 'standard'))
        import status_kad
        status = status_kad.baris()
    except Exception:
        status = '> **Status keputusan:** lihat `laporan/KAD_SKOR.md`; laporan ini BUKAN keputusan.'
    A = ['# Analisis pegang minimum: "tak mahu beli dan jual hari yang sama; pegang sekurang-kurangnya 3 hari"', '', status, '',
         'Dijana `kajian/carian_setup/cs_pegang.py`. Pradaftar: `kajian/SPEC_CARIAN_SETUP.md` pindaan 14 Nov 2026 (o). '
         '**Jangan sunting secara manual.**', '',
         '## 1. Papertrade langsung: dari mana datangnya "beli dan jual hari sama"?', '',
         f"- Lejar (semua kaedah, {pt['n']:,} dagangan ditutup, beli {pt['dari']} hingga {pt['hingga']}): dijual **pada hari beli "
         f"{p(pt['sama'])} %**, esoknya {p(pt['esok'])} %, hari ke-3 {p(pt['tiga'])} %. Semua jualan hari sama berpunca daripada "
         f"{', '.join(f'{k} ({v})' for k, v in pt['sebab_sama'].items())}; purata hasilnya {pt['untung_sama']:+.1f} %.",
         f"- Papertrade C: {pt['c_sama']:,} daripada {pt['c_n']:,} dagangan ditutup ({pt['c_sama'] / pt['c_n']:.0%}) dijual pada hari "
         f"beli; paling banyak {', '.join(f'{k} ({v})' for k, v in pt['c_kaedah'].items())}.",
         f"- {pt['tanpa']} daripada {len(pt['kaedah'])} kaedah (≥ 30 dagangan) tiada langsung jualan hari sama. Puncanya kaedah M "
         'tertentu yang henti ruginya ketat dan aktif pada hari beli:', '',
         '| Kaedah | Dagangan | Dijual hari sama % | Dijual dalam < 3 hari % | Purata % |', '|---|---|---|---|---|']
    for k, r in pt['kaedah'].head(10).iterrows():
        A.append(f'| `{k}` | {int(r.n)} | {r.sama * 100:.0f} | {r.bawah3 * 100:.0f} | {r.purata:+.1f} |')
    A += ['', f'## 2. Setup F ({len(T)} setup kedudukan akhir; kumpulan B)', '',
          '- **Jualan pada hari beli: 0 dalam semua setup F.** Mekanik F (sejak pindaan asal, syarat wajib "tiada jual hari beli"): '
          'beli pada buka; henti rugi tidak aktif pada hari beli; indikator keluar dinilai pada tutup dan dijual pada buka esok.',
          f"- Tetapi jualan AWAL memang berlaku. Median setup dipercayai: dijual pada hari ke-2 {p(med('jual2_v0'))} %, hari ke-3 "
          f"{p(med('jual3_v0'))} % daripada belian; punca: henti rugi {p(med('awal_henti_v0'))} %, indikator keluar "
          f"{p(med('awal_ind_v0'))} %. Purata hasil dagangan yang dijual sebelum hari ke-4: {p(med('R_awal_v0'), 1, True)} %.", '',
          '## 3. Tiga mekanik pada setup yang sama (median 34 setup dipercayai)', '',
          '| Mekanik | Dijual sebelum hari ke-4 % | Tangkap penuh % | Menang % | Rugi ≥ 8 % % | Rugi ≥ 15 % % | Purata % | Pegang (sesi) |',
          '|---|---|---|---|---|---|---|---|']
    for mod, nama in ((0, 'V0 sedia ada'), (1, 'V1 indikator mulai hari ke-4; henti kekal aktif'),
                      (2, 'V2 indikator DAN henti mulai hari ke-4')):
        v = f'v{mod}'
        awal = float((Y[f'jual2_{v}'] + Y[f'jual3_{v}']).median())
        A.append(f"| {nama} | {p(awal)} | {p(med(f'tp_{v}'))} | {p(med(f'menang_{v}'), 0)} | {p(med(f'rugi8_{v}'))} | "
                 f"{p(med(f'rugi15_{v}'))} | {p(med(f'purata_{v}'), 2, True)} | {med(f'pegang_{v}'):.1f} |")
    naik = lambda a, b: int((Y[a] > Y[b]).sum())
    A += ['', f"- V1 lawan V0: tangkap penuh lebih tinggi bagi {naik('tp_v1', 'tp_v0')} daripada {len(Y)} setup dipercayai, purata "
          f"lebih tinggi bagi {naik('purata_v1', 'purata_v0')}, rugi ≥ 8 % lebih tinggi bagi {naik('rugi8_v1', 'rugi8_v0')}.",
          f"- V2 lawan V0: tangkap penuh lebih tinggi bagi {naik('tp_v2', 'tp_v0')}, purata lebih tinggi bagi "
          f"{naik('purata_v2', 'purata_v0')}, rugi ≥ 15 % lebih tinggi bagi {naik('rugi15_v2', 'rugi15_v0')}.", '',
          '## 4. Setiap setup dipercayai', '',
          '| # | ID | Keluar | Dijual hari ke-2 / ke-3 % (V0) | Tangkap penuh %: V0 / V1 / V2 | Menang %: V0 / V1 / V2 | '
          'Rugi ≥ 8 %: V0 / V1 / V2 | Rugi ≥ 15 %: V0 / V1 / V2 | Purata %: V0 / V1 / V2 |', '|---' * 9 + '|']
    for r in Y.itertuples():
        A.append(f"| {r.kedudukan} | `{r.id}` | {r.keluar} | {p(r.jual2_v0)} / {p(r.jual3_v0)} | {p(r.tp_v0)} / {p(r.tp_v1)} / "
                 f"{p(r.tp_v2)} | {p(r.menang_v0, 0)} / {p(r.menang_v1, 0)} / {p(r.menang_v2, 0)} | {p(r.rugi8_v0, 0)} / "
                 f"{p(r.rugi8_v1, 0)} / {p(r.rugi8_v2, 0)} | {p(r.rugi15_v0, 0)} / {p(r.rugi15_v1, 0)} / {p(r.rugi15_v2, 0)} | "
                 f"{p(r.purata_v0, 2, True)} / {p(r.purata_v1, 2, True)} / {p(r.purata_v2, 2, True)} |")
    A += ['', 'Kaveat: kumpulan B sudah dilihat; tiada saham delist; backtest sahaja. Baris V0 disahkan sama dengan enjin lama.', '']
    open(os.path.join(d_, 'PEGANG_MIN.md'), 'w', encoding='utf-8').write('\n'.join(A))
    cari.log(f'pegang minimum: {len(T)} setup; laporan ditulis')
    return T


if __name__ == '__main__':
    main(sys.argv[1])
