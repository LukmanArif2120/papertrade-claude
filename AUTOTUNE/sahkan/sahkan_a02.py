# Pengesahan, label, portfolio gabungan dan laporan A02 (SPEC_A02 §4–§5). A01 (pengesahan.py, gabungan.py,
# laporan.py) tidak berubah.
#   python3 AUTOTUNE/sahkan/sahkan_a02.py [--data DIR] [--proses 4] [--maks 6] [--calon-maks 12] [--tanpa-gabungan]
# Input : hasil_a02/tala/<ID>_<lorong>/kNN.json, saringan.csv, pilihan.json, pandang_hadapan.json (imbas_a02.py).
# Output: hasil_a02/parameter_sedia.csv, ringkasan.json, gabungan.json, papan.json, LAPORAN.md (≤ 150 baris).
import argparse, glob, json, math, os, sys, time
import numpy as np, pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
AT = os.path.dirname(SINI)
for p in (SINI, os.path.join(AT, 'tala'), os.path.join(AT, 'teras')):
    if p not in sys.path: sys.path.insert(0, p)
import umum as U            # noqa: E402
import tala as T1           # noqa: E402
import tala_a02 as T2       # noqa: E402
from tala import E, O       # noqa: E402

HASIL = T2.HASIL
TALA = T2.KELUAR
N_DSR = 268                 # bilangan kaedah-lorong dalam saringan (SPEC_A02 §4)
DSR_MIN = 0.90
MDD_LONGGAR = O.MDD_LONGGAR_A02
LABEL = ['LULUS', 'CALON', 'TIDAK LULUS', 'PANDANG HADAPAN']
HAD_KOR, MAKS = 0.7, 6
CALON_MAKS = 12             # calon gabungan teratas (ikut lebihan OOS A) yang dagangannya dijana semula


# ---------- siri ----------
def siri(H, g):
    h = (H or {}).get('harian_ujian') or {}
    if g not in h or 'tarikh' not in h: return pd.Series(dtype=float)
    return pd.Series(np.asarray(h[g], float), index=pd.to_datetime(h['tarikh']))


def sah(H):
    return isinstance(H, dict) and H.get('status') == 'SIAP'


def baca_kajian(nama, tala=TALA):
    out = {}
    for f in glob.glob(os.path.join(tala, nama, 'k*.json')):
        try: out[int(os.path.basename(f)[1:3])] = json.load(open(f))
        except Exception: pass
    return out


def oos(kaj, g):
    """(siri strategi, siri SPY) gabungan tetingkap 0–5 (SIAP sahaja)."""
    r = [siri(kaj[k], g) for k in T2.K_WFO if sah(kaj.get(k))]
    s = [siri(kaj[k], 'SPY') for k in T2.K_WFO if sah(kaj.get(k))]
    return U.sambung(r), U.sambung(s)


def lebihan(r, s):
    return U.cagr(r) - U.cagr(s) if len(r) and len(s) else float('nan')


def _stat(kaj, g, ks):
    M = [kaj[k].get(f'ujian_{g}') for k in ks if sah(kaj.get(k)) and kaj[k].get(f'ujian_{g}')]
    n = sum(int(m.get('n') or 0) for m in M)
    if not n: return 0, None, None
    hari = sum((m.get('days') or 0) * (m.get('n') or 0) for m in M) / n
    win = sum((m.get('win') or 0) * (m.get('n') or 0) for m in M) / n
    return n, hari, win


def sr0_saringan(csv):
    """Jangkaan SR maksimum nasib: varians SR harian pulangan berlebihan A (saringan, semua baris SIAP), N = 268."""
    try: D = pd.read_csv(csv)
    except Exception: return float('nan'), 0
    srs = D.loc[D.status == 'SIAP', 'sr_lebih_A'].dropna().tolist()
    return O.sr0(srs, N_DSR), len(srs)


def label(m):
    """SPEC_A02 §4. m: lebihan_a, lebihan_b, lebihan_peng, mdd_oos, spy_mdd_oos, dsr, imbasan."""
    if m.get('imbasan') == 'PANDANG HADAPAN': return 'PANDANG HADAPAN'
    pos = lambda x: x is not None and not (isinstance(x, float) and math.isnan(x)) and x > 0
    tiga = pos(m.get('lebihan_a')) and pos(m.get('lebihan_b')) and pos(m.get('lebihan_peng'))
    if not tiga: return 'TIDAK LULUS'
    mdd_ok = U._ge(m.get('mdd_oos'), (m.get('spy_mdd_oos') or 0) - MDD_LONGGAR) if m.get('spy_mdd_oos') is not None else False
    if mdd_ok and U._ge(m.get('dsr'), DSR_MIN) and m.get('imbasan') == 'BERSIH': return 'LULUS'
    return 'CALON'


def nilai(nama, kaj, sr0, hadapan, skor_saring=None):
    mid, lorong = T2.pecah_tugas(nama)
    rA, sA = oos(kaj, 'A'); rB, sB = oos(kaj, 'B')
    nA, hA, wA = _stat(kaj, 'A', T2.K_WFO); nB, hB, wB = _stat(kaj, 'B', T2.K_WFO)
    H6, H7 = kaj.get(T2.K_AKHIR), kaj.get(T2.K_SEMASA)
    rP = siri(H6, 'AB') if sah(H6) else pd.Series(dtype=float); sP = siri(H6, 'SPY') if sah(H6) else pd.Series(dtype=float)
    siap = sorted(k for k, H in kaj.items() if sah(H))
    x = (rA - sA.reindex(rA.index).fillna(0.0)) if len(rA) else pd.Series(dtype=float)
    sr, sk, ku, n = O.sharpe(x)
    d = O.dsr(sr, sk, ku, n, sr0) if n >= 30 and not math.isnan(sr) and not math.isnan(sr0) else float('nan')
    m = dict(tugas=nama, kaedah=mid, lorong=lorong, nama=U.nama_modul(mid),
             lebihan_a=lebihan(rA, sA), lebihan_b=lebihan(rB, sB), cagr_a=U.cagr(rA), cagr_b=U.cagr(rB), spy_oos=U.cagr(sA),
             mdd_a=U.mdd(rA), mdd_b=U.mdd(rB), spy_mdd_oos=U.mdd(sA) if len(sA) else None,
             n_a=nA, n_b=nB, hari_a=hA, menang_a=wA, hari_b=hB,
             lebihan_peng=lebihan(rP, sP), cagr_peng=U.cagr(rP), spy_peng=U.cagr(sP), mdd_peng=U.mdd(rP),
             spy_mdd_peng=U.mdd(sP) if len(sP) else None, n_peng=((H6 or {}).get('ujian_AB') or {}).get('n'),
             peng_mula=str(rP.index[0].date()) if len(rP) else None, peng_akhir=str(rP.index[-1].date()) if len(rP) else None,
             oos_mula=str(rA.index[0].date()) if len(rA) else None, oos_akhir=str(rA.index[-1].date()) if len(rA) else None,
             sr_lebih=sr, dsr=d, pbo=((H6 or {}).get('pbo') or {}).get('pbo'), skor_saringan=skor_saring,
             imbasan=(hadapan.get(nama) or {}).get('status', 'TIDAK DIIMBAS'),
             kajian_siap=''.join(str(k) for k in siap), n_cubaan=sum(int((H or {}).get('n_trials') or 0) for H in kaj.values()),
             param_akhir=json.dumps((H6 or {}).get('params') or {}, sort_keys=True) if sah(H6) else '',
             param_semasa=json.dumps((H7 or {}).get('params') or {}, sort_keys=True) if sah(H7) else '')
    m['mdd_oos'] = min(m['mdd_a'], m['mdd_b']) if len(rA) and len(rB) else float('nan')
    cat = []
    if len(siap) < 8: cat.append(f'kajian tidak lengkap ({m["kajian_siap"] or "tiada"})')
    if m['imbasan'] == 'TIDAK DIIMBAS': cat.append('tidak diimbas')
    m['label'] = label(m) if len([k for k in siap if k <= T2.K_AKHIR]) == 7 else (
        'PANDANG HADAPAN' if m['imbasan'] == 'PANDANG HADAPAN' else 'TIDAK LULUS')
    m['catatan'] = '; '.join(cat)
    return m


# ---------- portfolio gabungan ----------
def persentil(T):
    if not len(T): return T
    T = T.copy(); T['rank'] = T.groupby('ent')['rank'].rank(pct=True, method='average'); return T


def kongsi(senarai):
    s = [t for t in senarai if t is not None and len(t)]
    if not s: return pd.DataFrame(columns=['ticker', 'ent', 'ex', 'ret', 'rank', 'days'])
    return pd.concat(s, ignore_index=True).sort_values(['ent', 'rank'], ascending=[True, False], kind='stable')


def korelasi(a, b):
    x = pd.concat([a, b], axis=1, join='inner').dropna()
    if len(x) < 20 or x.iloc[:, 0].std() == 0 or x.iloc[:, 1].std() == 0: return 0.0
    return float(x.iloc[:, 0].corr(x.iloc[:, 1]))


def pilih_tamak(calon, r_ind, nilai_fn, had_mdd, maks=MAKS, had_kor=HAD_KOR):
    """A01 §6 diadaptasi: mula lebihan OOS A tertinggi; tambah jika lebihan gabungan naik dan MDD ≥ had_mdd;
    langkau korelasi > 0.7; maks 6. nilai_fn(ids) → (lebihan, mdd)."""
    log = []
    if not calon: return [], log, (float('nan'), float('nan'))
    pilih = [calon[0]]; c0, d0 = nilai_fn(pilih)
    log.append(dict(kaedah=calon[0], tindakan='mula', lebihan=c0, mdd=d0))
    for k in calon[1:]:
        if len(pilih) >= maks: break
        kor = {s: korelasi(r_ind[k], r_ind[s]) for s in pilih}
        km = max(kor.values())
        if km > had_kor:
            log.append(dict(kaedah=k, tindakan='langkau: korelasi', korelasi=km, dengan=max(kor, key=kor.get))); continue
        c, d = nilai_fn(pilih + [k])
        if c > c0 and d >= had_mdd:
            pilih.append(k); c0, d0 = c, d; log.append(dict(kaedah=k, tindakan='tambah', lebihan=c, mdd=d, korelasi=km))
        else:
            log.append(dict(kaedah=k, tindakan='tolak: ' + ('lebihan tidak naik' if not c > c0 else 'MDD melepasi had'),
                            lebihan=c, mdd=d, korelasi=km))
    return pilih, log, (c0, d0)


_PJ = {}


def _jana(arg):
    """Proses anak (fork): dagangan semua kumpulan bagi (tugas, kajian) atas data tetingkap yang dikongsi."""
    nama, P = arg
    try:
        d = _PJ['d']; mid, lorong = T2.pecah_tugas(nama)
        m = T1.muat_kaedah(mid); Pp = dict(m.PARAM); Pp.update(P or {})
        fr = T1.salin(d['fr']); m.sedia(fr, d['idx'], Pp)
        tmax = Pp['tmax'] if 'tmax' in Pp else m.TMAX
        S = E.Susun(fr)
        out = {}
        for g in d['kum']:
            T = S.dengan_topeng(d['tp'][g]).dagangan(tmax, m.WARM, d['U0'], d['U1'], had60=E.had60_lorong(lorong))
            out[g] = T[['ticker', 'ent', 'ex', 'ret', 'days', 'rank']].copy()
        return nama, out, None
    except Exception as e:
        return nama, None, f'{type(e).__name__}: {e}'[:300]


class Gabung:
    """Dagangan setiap calon setiap tetingkap (0–5: A, B; 6: AB) dijana semula dengan parameter kajian itu."""
    def __init__(self, kaj, calon, data_dir, proses=4):
        self.kaj, self.calon, self.proses = kaj, calon, proses
        self.S = data_dir if isinstance(data_dir, T1.Sumber) else T1.Sumber(data_dir); self.T = {}; self.ps = {}; self.spy = {}; self.gagal = {}
        self.panas = pd.Timedelta(days=max(O.panas_a02(T1.muat_kaedah(T2.pecah_tugas(c)[0])) for c in calon))

    def sedia(self):
        from multiprocessing import get_context
        for k in T2.K_WFO + [T2.K_AKHIR]:
            H0 = self.kaj[self.calon[0]][k]
            U0, U1 = pd.Timestamp(H0['ujian'][0]), pd.Timestamp(H0['ujian'][1])
            fr, idx, univ = self.S.muat(U0 - self.panas, U1, 'AB')
            kum = ['AB'] if k == T2.K_AKHIR else ['A', 'B']
            _PJ['d'] = dict(fr=fr, idx=idx, U0=U0, U1=U1, kum=kum, tp={g: self.S.topeng(fr, univ, g) for g in kum})
            tugas = [(c, self.kaj[c][k].get('params') or {}) for c in self.calon if c not in self.gagal]
            with get_context('fork').Pool(min(self.proses, len(tugas)), maxtasksperchild=2) as p:
                for nama, out, e in p.imap_unordered(_jana, tugas):
                    if e: self.gagal[nama] = f'k{k:02d}: {e}'; continue
                    for g, T in out.items(): self.T[(nama, k, g)] = persentil(T)
            self.ps[k] = E.Pasaran(fr, U0, U1)
            self.spy[k] = O.spy_lengkung(idx['SPY']['close'], self.ps[k].tarikh)
            del fr; self.S._fr.clear(); _PJ.clear()
            print(f'gabungan: kajian {k} siap, gagal {len(self.gagal)}', flush=True)
        return [c for c in self.calon if c not in self.gagal]

    def pulangan(self, ids, bah):
        ks = [(T2.K_AKHIR, 'AB')] if bah == 'P' else [(k, bah) for k in T2.K_WFO]
        r, s = [], []
        for k, g in ks:
            cv = self.ps[k].lengkung(kongsi([self.T[(i, k, g)] for i in ids]))
            r.append(E.pulangan_harian(cv)); s.append(E.pulangan_harian(self.spy[k]))
        return U.sambung(r), U.sambung(s)


def metrik(r, s):
    return U.bersih(dict(cagr=U.cagr(r), spy=U.cagr(s), lebihan=lebihan(r, s), mdd=U.mdd(r), spy_mdd=U.mdd(s),
                         mula=str(r.index[0].date()) if len(r) else None, akhir=str(r.index[-1].date()) if len(r) else None), 4)


def gabungan(D, semua_kaj, data_dir, proses=4, maks=MAKS, calon_maks=CALON_MAKS):
    asas = 'LULUS' if (D.label == 'LULUS').any() else 'CALON'
    C = D[D.label == asas].sort_values('lebihan_a', ascending=False)
    out = dict(versi='A02', asas_calon=asas, n_calon=int(len(C)), terpilih=[], log=[])
    if not len(C): out['catatan'] = 'tiada kaedah LULUS atau CALON'; return out
    calon = C.tugas.tolist()[:calon_maks]
    out['calon_dinilai'] = calon
    G = Gabung({c: semua_kaj[c] for c in calon}, calon, data_dir, proses)
    ok = G.sedia(); out['gagal_jana'] = G.gagal
    r_ind = {c: oos(semua_kaj[c], 'A')[0] for c in ok}
    had = float(C.spy_mdd_oos.dropna().iloc[0]) - MDD_LONGGAR if C.spy_mdd_oos.notna().any() else -0.30
    cache = {}

    def nilai_fn(ids):
        k = tuple(ids)
        if k not in cache:
            r, s = G.pulangan(ids, 'A'); cache[k] = (lebihan(r, s), U.mdd(r))
        return cache[k]
    pilih, log, _ = pilih_tamak(ok, r_ind, nilai_fn, had, maks)
    out.update(terpilih=pilih, log=U.bersih(log, 4), had_mdd=round(had, 4))
    ek = {}
    for bah, nm in (('A', 'oos_A'), ('B', 'oos_B'), ('P', 'pengesahan')):
        r, s = G.pulangan(pilih, bah); out[nm] = metrik(r, s); ek[nm] = U.ekuiti_bulanan(r)
    out['ekuiti_bulanan'] = ek
    out['param_semasa'] = {c: (semua_kaj[c].get(T2.K_SEMASA) or {}).get('params') for c in pilih}
    out['param_akhir'] = {c: (semua_kaj[c].get(T2.K_AKHIR) or {}).get('params') for c in pilih}
    return out


# ---------- laporan ----------
def pc(x, nd=1):
    try:
        x = float(x)
        return '—' if math.isnan(x) else f'{x * 100:.{nd}f}%'
    except (TypeError, ValueError): return '—'


def a01_label():
    try: A = pd.read_csv(os.path.join(AT, 'hasil', 'parameter_sedia.csv'))
    except Exception: return {}
    return dict(zip(A.kaedah, A.label))


def laporan(D, ring, gab, saring, pilihan, hadapan, skop, keluar=HASIL):
    L = ['# LAPORAN AUTOTUNE A02', '',
         f"Dijana oleh `AUTOTUNE/sahkan/sahkan_a02.py` ({ring['dijana']}). Spec: `AUTOTUNE/SPEC_A02.md`. "
         'A01 (`AUTOTUNE/hasil/`) kekal tidak diubah. Parameter SEMASA ialah cadangan sahaja; tiada dagangan wang sebenar.', '',
         '## Kaveat data', '',
         '- Release `autotune-data-a02` (yfinance auto_adjust + faktor_split; 2009-01-02 – 2026-10-16; 3260 ticker pernah '
         'dalam universe; QC bar titik masa, 1373 lonjakan berbalik dibuang; `AUTOTUNE/data/QC_A02.md`).',
         '- Tiada saham delist (bias survivorship): semua angka ialah had atas. Universe 2010–2013 hanya ~1000–1300 saham.',
         '- Data bermula 2009-01-02: pemanasan kajian 0 (latih 2010) terhad kepada ~1 tahun bagi kaedah bertetingkap panjang.',
         '- Harga backtest dilaras dividen; universe ikut harga tidak dilaras split (masih dilaras dividen).', '',
         '## Pembetulan audit yang diterapkan', '',
         '- #1–#3 data: harga tidak dilaras split untuk penapis USD10/nilai dagangan; QC peringkat bar (tiada ticker dibuang '
         'kerana kemeruapan).',
         '- #7: n, hari pegang dan kadar menang daripada dagangan yang benar-benar dipegang portfolio 8 × 12.5%.',
         '- #8: objektif = CAGR − CAGR SPY tempoh sama; kekangan MDD ≥ MDD SPY − 10 mata, ≥ 30 dagangan dipegang.',
         '- #17: pemanasan = maks(400 hari, 1.6 × (tetingkap terpanjang julat atas + WARM)) hari kalendar.',
         '- #12: reka bentuk bersih 2010–2018 (saringan 2013–2018; walk-forward 2013–2018); 2019–kini = pengesahan sahaja.',
         '- Dua lorong: `had60` (had pegang 60 hari, seperti A01) dan `asal` (tiada had enjin; TMAX asal).', '']
    L += ['## Pengurangan skop', ''] + ([f'- {s}' for s in skop] if skop else
                                        ['- Tiada: 20 kaedah setiap lorong, 120 percubaan setiap kajian, 8 kajian (skop penuh SPEC_A02).']) + ['']
    pos2 = int(((D.lebihan_a > 0) & (D.lebihan_b > 0)).sum()) if len(D) else 0
    posp = int((D.lebihan_peng > 0).sum()) if len(D) else 0
    L += ['## Kesimpulan', '',
          f'- {pos2}/{len(D)} kaedah-lorong mengatasi SPY atas OOS bersih 2013–2018 pada A dan B; {posp}/{len(D)} mengatasi SPY '
          'dalam pengesahan 2019 – hujung data (parameter AKHIR, A+B).',
          f"- LULUS {int((D.label == 'LULUS').sum())}, CALON {int((D.label == 'CALON').sum())}: "
          + ('tiada kaedah yang boleh dicadangkan; kalau tak beli, cakap tak beli.' if not ((D.label == 'LULUS') | (D.label == 'CALON')).any()
             else 'lihat portfolio gabungan di bawah.'), '']
    n_s = int((saring.status == 'SIAP').sum()) if len(saring) else 0
    L += ['## Saringan (peringkat 1)', '',
          f"{len(saring)} kaedah-lorong (PARAM asal, 2013–2018, A dan B); SIAP {n_s}. Skor = min(lebihan A, lebihan B)."]
    for lo in T2.LORONG:
        d = saring[(saring.lorong == lo) & (saring.status == 'SIAP')]
        L.append(f"- {lo}: skor > 0 pada {int((d.skor > 0).sum())}/{len(d)}; dipilih {len(pilihan['pilihan'].get(lo, []))}: "
                 f"{', '.join(pilihan['pilihan'].get(lo, []))}")
    L += ['', '## Tala (peringkat 2)', '',
          f"{ring['n_tugas_siap']}/{ring['n_tugas']} tugasan SIAP; {ring['n_cubaan_jumlah']} percubaan. Kajian 0–5 = ujian "
          '2013…2018 (latih 3 tahun sebelum), 6 = AKHIR (latih 2016–2018, pengesahan 2019-01-01 – hujung), 7 = SEMASA.', '',
          '## Label', '',
          'LULUS: lebihan OOS bersih > 0 (A dan B), lebihan pengesahan > 0, MDD OOS (terburuk A/B) ≥ MDD SPY − 10 mata, '
          f'DSR ≥ {DSR_MIN} (N = {N_DSR}, pulangan berlebihan harian OOS A), imbasan bersih. CALON: tiga syarat pertama. ', '',
          '| Lorong | ' + ' | '.join(LABEL) + ' |', '|---|' + '---|' * len(LABEL)]
    for lo in T2.LORONG:
        d = D[D.lorong == lo]
        L.append(f'| {lo} | ' + ' | '.join(str(int((d.label == l).sum())) for l in LABEL) + ' |')
    L += ['', f"SR0 (jangkaan SR maksimum nasib, harian) = {ring['sr0_harian']:.4f} daripada {ring['n_sr_saringan']} SR saringan."
          if ring.get('sr0_harian') is not None and not math.isnan(ring['sr0_harian']) else '', '',
          '## 10 teratas ikut lebihan OOS bersih (min A, B)', '',
          '| # | Kaedah-lorong | Label | Lebihan A | Lebihan B | SPY OOS | Pengesahan (lebihan; CAGR / SPY) | MDD OOS / SPY | Dag. A | DSR | Imbasan |',
          '|---|---|---|---|---|---|---|---|---|---|---|']
    T = D.assign(_m=D[['lebihan_a', 'lebihan_b']].min(axis=1)).sort_values('_m', ascending=False).head(10)
    for i, r in enumerate(T.itertuples(), 1):
        L.append(f"| {i} | {r.tugas} | {r.label} | {pc(r.lebihan_a)} | {pc(r.lebihan_b)} | {pc(r.spy_oos)} | "
                 f"{pc(r.lebihan_peng)} ({pc(r.cagr_peng)} / {pc(r.spy_peng)}) | {pc(r.mdd_oos)} / {pc(r.spy_mdd_oos)} | "
                 f"{r.n_a} | {'—' if pd.isna(r.dsr) else f'{r.dsr:.2f}'} | {r.imbasan} |")
    L += ['', '## Portfolio gabungan', '']
    if gab.get('terpilih'):
        L.append(f"Calon: {gab['asas_calon']} ({gab['n_calon']}; {len(gab.get('calon_dinilai', []))} teratas dinilai). "
                 f"Terpilih: {', '.join(gab['terpilih'])}. Had MDD {pc(gab.get('had_mdd'))}.")
        for nm, t in (('oos_A', 'OOS bersih A'), ('oos_B', 'OOS bersih B'), ('pengesahan', 'Pengesahan A+B')):
            x = gab.get(nm) or {}
            L.append(f"- {t} ({x.get('mula')} – {x.get('akhir')}): CAGR {pc(x.get('cagr'))} lwn SPY {pc(x.get('spy'))} "
                     f"(lebihan {pc(x.get('lebihan'))}); MDD {pc(x.get('mdd'))} lwn SPY {pc(x.get('spy_mdd'))}")
    else:
        L.append(gab.get('catatan', 'tiada gabungan'))
    a1 = a01_label()
    L += ['', '## Perbandingan A01 lwn A02', '',
          '- A01: objektif CAGR mutlak (MDD ≥ −30%), had 60 hari, metrik daripada semua isyarat (bukan dagangan dipegang), '
          'walk-forward 2013–2024 atas data dengan universe harga dilaras dan ticker meruap dibuang.',
          f"- A01 (semua kaedah): TINGGI {sum(v == 'TINGGI' for v in a1.values())}, SEDERHANA "
          f"{sum(v == 'SEDERHANA' for v in a1.values())}, RENDAH {sum(v == 'RENDAH' for v in a1.values())}, "
          f"GAGAL {sum(v == 'GAGAL' for v in a1.values())}.",
          '- A02 (kaedah-lorong terpilih): ' + ', '.join(f"{l} {int((D.label == l).sum())}" for l in LABEL) + '.', '',
          '| Kaedah-lorong | Label A01 | Label A02 | Lebihan A (A02) |', '|---|---|---|---|']
    for r in D.sort_values('lebihan_a', ascending=False).head(20).itertuples():
        L.append(f'| {r.tugas} | {a1.get(r.kaedah, "—")} | {r.label} | {pc(r.lebihan_a)} |')
    nph = sum(v.get('status') == 'PANDANG HADAPAN' for v in hadapan.values())
    L += ['', '## Imbasan pandang ke hadapan', '',
          f'{len(hadapan)} kaedah-lorong diimbas (AKHIR dan SEMASA, 12 tarikh potong 2012–2026); PANDANG HADAPAN: {nph}. '
          'Butiran: [PANDANG_HADAPAN.md](PANDANG_HADAPAN.md).', '',
          'Fail: `parameter_sedia.csv` (semua kaedah-lorong terpilih, param AKHIR/SEMASA), `gabungan.json`, `saringan.csv`, '
          '`pilihan.json`, `tala/<ID>_<lorong>/kNN.json`. Holdout sebenar: ujian ke hadapan sejak 16 Okt 2026 (tidak dinilai).']
    L = [x for i, x in enumerate(L) if not (x == '' and i and L[i - 1] == '')]
    if len(L) > 150: L = L[:149] + ['(dipotong pada 150 baris)']
    open(os.path.join(keluar, 'LAPORAN.md'), 'w').write('\n'.join(L) + '\n')
    return len(L)


def rekod_papan(r):
    return U.bersih(dict(id=r['tugas'], kaedah=r['kaedah'], lorong=r['lorong'], nama=r['nama'], label=r['label'],
                         lebihan_a=r['lebihan_a'], lebihan_b=r['lebihan_b'], lebihan_peng=r['lebihan_peng'],
                         cagr_a=r['cagr_a'], cagr_b=r['cagr_b'], spy_oos=r['spy_oos'], cagr_peng=r['cagr_peng'],
                         spy_peng=r['spy_peng'], mdd_oos=r['mdd_oos'], spy_mdd_oos=r['spy_mdd_oos'], n_a=r['n_a'],
                         hari_a=r['hari_a'], dsr=r['dsr'], pbo=r['pbo'], imbasan=r['imbasan'],
                         param=json.loads(r['param_semasa'] or '{}'), catatan=r['catatan'], versi='A02'), 4)


def jalan(data_dir=None, proses=4, maks=MAKS, calon_maks=CALON_MAKS, tanpa_gabungan=False, keluar=HASIL, tala=TALA, skop=()):
    pilihan = json.load(open(os.path.join(keluar, 'pilihan.json')))
    try: saring = pd.read_csv(os.path.join(keluar, 'saringan.csv'))
    except Exception: saring = pd.DataFrame(columns=['kaedah', 'lorong', 'status', 'skor'])
    hadapan = {}
    try: hadapan = json.load(open(os.path.join(keluar, 'pandang_hadapan.json')))
    except Exception: pass
    sr0, n_sr = sr0_saringan(os.path.join(keluar, 'saringan.csv'))
    sk = {(r.kaedah, r.lorong): r.skor for r in saring.itertuples()} if len(saring) else {}
    semua, R = {}, []
    for nama in pilihan['tugas']:
        kaj = baca_kajian(nama, tala); semua[nama] = kaj
        R.append(nilai(nama, kaj, sr0, hadapan, sk.get(T2.pecah_tugas(nama))))
    D = pd.DataFrame(R)
    D.to_csv(os.path.join(keluar, 'parameter_sedia.csv'), index=False, float_format='%.6g')
    gab = dict(versi='A02', terpilih=[], catatan='gabungan tidak dijalankan')
    if not tanpa_gabungan:
        gab = gabungan(D, semua, data_dir, proses, maks, calon_maks)
    U.tulis_json(os.path.join(keluar, 'gabungan.json'), U.bersih(gab))
    n_tugas = 8 * len(pilihan['tugas'])
    ring = dict(versi='A02', dijana=time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime()), n_kaedah=len(D),
                n_tugas=n_tugas, n_tugas_siap=int(sum(len(str(x)) for x in D.kajian_siap)) if len(D) else 0,
                n_cubaan_jumlah=int(D.n_cubaan.sum()) if len(D) else 0, sr0_harian=sr0, n_sr_saringan=n_sr, n_dsr=N_DSR,
                kiraan_label={l: int((D.label == l).sum()) for l in LABEL},
                kiraan_label_lorong={lo: {l: int(((D.lorong == lo) & (D.label == l)).sum()) for l in LABEL} for lo in T2.LORONG},
                tempoh=dict(saringan=list(T2.SARING), oos=['2013-01-01', '2018-12-31'], pengesahan=['2019-01-01', None]),
                spy=dict(oos=D.spy_oos.dropna().iloc[0] if len(D) and D.spy_oos.notna().any() else None,
                         pengesahan=D.spy_peng.dropna().iloc[0] if len(D) and D.spy_peng.notna().any() else None),
                belum_ditala=[], skop=list(skop), label=LABEL)
    U.tulis_json(os.path.join(keluar, 'ringkasan.json'), U.bersih(ring))
    U.tulis_json(os.path.join(keluar, 'papan.json'), dict(versi='A02', dijana=ring['dijana'], tempoh=ring['tempoh'],
                                                         kaedah=[rekod_papan(r) for r in R], gabungan=gab.get('terpilih', [])))
    n = laporan(D, ring, gab, saring, pilihan, hadapan, list(skop), keluar)
    return D, gab, ring, n


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--data', default=None); a.add_argument('--cache', default=os.environ.get('AUTOTUNE_CACHE', T2.CACHE))
    a.add_argument('--proses', type=int, default=4); a.add_argument('--maks', type=int, default=MAKS)
    a.add_argument('--calon-maks', type=int, default=CALON_MAKS); a.add_argument('--tanpa-gabungan', action='store_true')
    a.add_argument('--skop', action='append', default=[], help='catatan pengurangan skop (boleh berulang)')
    x = a.parse_args()
    dd = x.data or (None if x.tanpa_gabungan else str(T2.ambil_data(x.cache)))
    D, gab, ring, n = jalan(dd, x.proses, x.maks, x.calon_maks, x.tanpa_gabungan, skop=x.skop)
    print(f"A02: {len(D)} kaedah-lorong; label {ring['kiraan_label']}; gabungan {gab.get('terpilih')}; LAPORAN {n} baris")


if __name__ == '__main__':
    main()
