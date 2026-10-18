# Pengesahan, label, portfolio gabungan dan laporan A03 (SPEC_A03 §4; peraturan label SPEC_A02 §4). A01/A02 tidak berubah:
# fungsi label/nilai/tamak dipakai semula daripada sahkan_a02; dagangan gabungan dijana semula dengan sistem utama A03
# (topeng universe ∧ F ∧ M, had rugi 8%, 5 slot × 20%).
#   python3 AUTOTUNE/sahkan/sahkan_a03.py [--cache ...] [--fund ...] [--proses 4] [--maks 6] [--calon-maks 10] [--skop ...]
# Input : hasil_a03/{pilihan.json, saringan.csv, pandang_hadapan.json, tala/<ID>_<lorong>/kNN.json}, hasil_a02/saringan.csv,
#         hasil_a02/parameter_sedia.csv (perbandingan), AUTOTUNE/fundamental/LIPUTAN.md (kaveat liputan).
# Output: hasil_a03/parameter_sedia.csv, ringkasan.json, gabungan.json, papan.json, LAPORAN.md (≤ 150 baris).
import argparse, json, math, os, re, sys, time
import numpy as np, pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
AT = os.path.dirname(SINI)
for p in (SINI, os.path.join(AT, 'tala'), os.path.join(AT, 'teras')):
    if p not in sys.path: sys.path.insert(0, p)
import umum as U            # noqa: E402
import tala as T1           # noqa: E402
import tala_a02 as T2       # noqa: E402
import tala_a03 as T3       # noqa: E402
import sahkan_a02 as S2     # noqa: E402
import menang_a03 as MA     # noqa: E402
from tala import E, O       # noqa: E402

HASIL = T3.HASIL
TALA = T3.KELUAR
N_DSR = 308                 # 268 A02 + 40 A03 (kumulatif, SPEC_A03 §4)
LABEL = MA.LABEL            # label utama A03 (SPEC_A03 §6); label SPEC_A02 §4 = lajur label_a02 (rujukan)
MAKS, CALON_MAKS = S2.MAKS, 10
LIPUTAN = os.path.join(AT, 'fundamental', 'LIPUTAN.md')
LIPUTAN_MIN = 0.70


def sr0_kumulatif(csv_a02, csv_a03):
    """SR0 daripada SR harian pulangan berlebihan A: saringan A02 (SIAP, 268) + sistem utama A03 (SIAP, 40); N = 308."""
    srs = []
    try:
        D = pd.read_csv(csv_a02); srs += D.loc[D.status == 'SIAP', 'sr_lebih_A'].dropna().tolist()
    except Exception: pass
    try:
        D = pd.read_csv(csv_a03); srs += D.loc[(D.status == 'SIAP') & (D.varian == T3.UTAMA), 'sr_lebih_A'].dropna().tolist()
    except Exception: pass
    return (O.sr0(srs, N_DSR) if srs else float('nan')), len(srs)


def liputan(f=LIPUTAN):
    """{tahun: pecahan 'ada'} daripada jadual LIPUTAN.md (| Tahun | Baris | ada % | ada A % | ada B % | yoy % | F % |)."""
    out = {}
    try: L = open(f, encoding='utf-8').read().splitlines()
    except OSError: return out
    for x in L:
        c = [s.strip() for s in x.strip().strip('|').split('|')]
        if len(c) >= 3 and re.fullmatch(r'20\d\d', c[0]):
            try: out[int(c[0])] = float(c[2].rstrip('%')) / 100
            except ValueError: pass
    return out


def liputan_rendah(lp):
    return sorted(y for y, v in lp.items() if 2013 <= y <= 2018 and v < LIPUTAN_MIN)


def nilai(nama, kaj, sr0, hadapan, skor_saring=None):
    """S2.nilai (metrik dan label SPEC_A02 → label_a02) + statistik dagangan OOS A/B dan pengesahan + label MENANG."""
    m = S2.nilai(nama, kaj, sr0, hadapan, skor_saring)
    m['label_a02'] = m.pop('label')
    MA.tambah_stat(m, 'a', MA.agregat(kaj, 'A', T2.K_WFO)); MA.tambah_stat(m, 'b', MA.agregat(kaj, 'B', T2.K_WFO))
    MA.tambah_stat(m, 'peng', MA.agregat(kaj, 'AB', [T2.K_AKHIR]))
    if len([k for k in m['kajian_siap'] if int(k) <= T2.K_AKHIR]) < 7:
        m['label'], g = 'TIDAK', ['kajian tidak lengkap']
    else:
        m['label'], g = MA.label(m)
    m['gagal'] = '; '.join(g)
    return m


# ---------- gabungan (sistem A03) ----------
_PJ = {}


def _jana(arg):
    nama, P = arg
    try:
        d = _PJ['d']; mid, lorong = T2.pecah_tugas(nama)
        m = T1.muat_kaedah(mid); Pp = dict(m.PARAM); Pp.update(P or {})
        fr = T1.salin(d['fr']); m.sedia(fr, d['idx'], Pp)
        tmax = Pp['tmax'] if 'tmax' in Pp else m.TMAX
        S = E.Susun(fr)
        out = {}
        for g in d['kum']:
            T = S.dengan_topeng(d['tp'][g]).dagangan(tmax, m.WARM, d['U0'], d['U1'], had60=E.had60_lorong(lorong),
                                                     had_rugi=T3.HAD_RUGI)
            out[g] = T[['ticker', 'ent', 'ex', 'ret', 'days', 'rank']].copy()
        return nama, out, None
    except Exception as e:
        return nama, None, f'{type(e).__name__}: {e}'[:300]


class Gabung03(S2.Gabung):
    """S2.Gabung dengan topeng universe ∧ F ∧ M, had rugi dan 5 slot × 20%."""
    def __init__(self, kaj, calon, data_dir, eps, proses=4):
        super().__init__(kaj, calon, data_dir, proses); self.eps = eps

    def sedia(self):
        from multiprocessing import get_context
        for k in T2.K_WFO + [T2.K_AKHIR]:
            H0 = self.kaj[self.calon[0]][k]
            U0, U1 = pd.Timestamp(H0['ujian'][0]), pd.Timestamp(H0['ujian'][1])
            fr, idx, univ = self.S.muat(U0 - self.panas, U1, 'AB')
            kum = ['AB'] if k == T2.K_AKHIR else ['A', 'B']
            F = T3.lajur_f(fr, self.eps); M = T3.topeng_m(fr, idx)
            tp = {}
            for g in kum:
                u = self.S.topeng(fr, univ, g)
                tp[g] = {t: (u[t].reindex(fr[t].index).fillna(False).astype(bool)
                             & F.get(t, pd.Series(False, index=fr[t].index)).reindex(fr[t].index).fillna(False).astype(bool)
                             & M[t]) for t in fr}
            _PJ['d'] = dict(fr=fr, idx=idx, U0=U0, U1=U1, kum=kum, tp=tp)
            tugas = [(c, self.kaj[c][k].get('params') or {}) for c in self.calon if c not in self.gagal]
            with get_context('fork').Pool(min(self.proses, len(tugas)), maxtasksperchild=2) as p:
                for nama, out, e in p.imap_unordered(_jana, tugas):
                    if e: self.gagal[nama] = f'k{k:02d}: {e}'; continue
                    for g, T in out.items(): self.T[(nama, k, g)] = S2.persentil(T)
            self.ps[k] = E.Pasaran(fr, U0, U1)
            self.spy[k] = O.spy_lengkung(idx['SPY']['close'], self.ps[k].tarikh)
            del fr; self.S._fr.clear(); _PJ.clear()
            print(f'gabungan A03: kajian {k} siap, gagal {len(self.gagal)}', flush=True)
        return [c for c in self.calon if c not in self.gagal]

    def pulangan(self, ids, bah):
        ks = [(T2.K_AKHIR, 'AB')] if bah == 'P' else [(k, bah) for k in T2.K_WFO]
        r, s = [], []
        for k, g in ks:
            cv = self.ps[k].lengkung(S2.kongsi([self.T[(i, k, g)] for i in ids]), T3.SLOT, T3.W)
            r.append(E.pulangan_harian(cv)); s.append(E.pulangan_harian(self.spy[k]))
        return U.sambung(r), U.sambung(s)


def gabungan(D, semua_kaj, data_dir, eps, proses=4, maks=MAKS, calon_maks=CALON_MAKS):
    asas = 'MENANG' if (D.label == 'MENANG').any() else 'HAMPIR'
    C = D[D.label == asas].sort_values('lebihan_a', ascending=False)
    out = dict(versi='A03', asas_calon=asas, n_calon=int(len(C)), terpilih=[], log=[])
    if not len(C): out['catatan'] = 'tiada sistem MENANG atau HAMPIR; tiada gabungan'; return out
    calon = C.tugas.tolist()[:calon_maks]
    out['calon_dinilai'] = calon
    G = Gabung03({c: semua_kaj[c] for c in calon}, calon, data_dir, eps, proses)
    ok = G.sedia(); out['gagal_jana'] = G.gagal
    if not ok: out['catatan'] = 'semua calon gagal dijana'; return out
    r_ind = {c: S2.oos(semua_kaj[c], 'A')[0] for c in ok}
    had = float(C.spy_mdd_oos.dropna().iloc[0]) - S2.MDD_LONGGAR if C.spy_mdd_oos.notna().any() else -0.30
    cache = {}

    def nilai_fn(ids):
        k = tuple(ids)
        if k not in cache:
            r, s = G.pulangan(ids, 'A'); cache[k] = (S2.lebihan(r, s), U.mdd(r))
        return cache[k]
    pilih, log, _ = S2.pilih_tamak(ok, r_ind, nilai_fn, had, maks)
    out.update(terpilih=pilih, log=U.bersih(log, 4), had_mdd=round(had, 4))
    ek = {}
    for bah, nm in (('A', 'oos_A'), ('B', 'oos_B'), ('P', 'pengesahan')):
        r, s = G.pulangan(pilih, bah); out[nm] = S2.metrik(r, s); ek[nm] = U.ekuiti_bulanan(r)
    out['ekuiti_bulanan'] = ek
    out['param_semasa'] = {c: (semua_kaj[c].get(T2.K_SEMASA) or {}).get('params') for c in pilih}
    out['param_akhir'] = {c: (semua_kaj[c].get(T2.K_AKHIR) or {}).get('params') for c in pilih}
    return out


# ---------- laporan ----------
pc = S2.pc


def nb(x, nd=2):
    try:
        x = float(x)
        return '—' if math.isnan(x) else ('∞' if math.isinf(x) else f'{x:.{nd}f}')
    except (TypeError, ValueError): return '—'


def jadual_varian(saring):
    """Sistem utama lwn ablasi (saringan, PARAM asal, 2013–2018)."""
    L = ['| Sistem | Lorong | n | CAGR A&B > 0 | Lebihan A&B > 0 | Median menang A / B | Median PF A | Median lebihan A | Median MDD A | Median dag. A |',
         '|---|---|---|---|---|---|---|---|---|---|']
    perlu = ['cagr_A', 'cagr_B', 'lebihan_A', 'lebihan_B', 'menang_A', 'menang_B', 'pf_A', 'mdd_A', 'n_A']
    saring = saring.reindex(columns=list(dict.fromkeys(list(saring.columns) + perlu)))
    for v in T3.SISTEM:
        for lo in T2.LORONG:
            d = saring[(saring.varian == v) & (saring.lorong == lo) & (saring.status == 'SIAP')]
            if not len(d): continue
            L.append(f"| {v}{' (pemilihan)' if v == T3.UTAMA else ''} | {lo} | {len(d)} | {int(((d.cagr_A > 0) & (d.cagr_B > 0)).sum())} | "
                     f"{int(((d.lebihan_A > 0) & (d.lebihan_B > 0)).sum())} | {pc(d.menang_A.median())} / {pc(d.menang_B.median())} | "
                     f"{nb(d.pf_A.median())} | {pc(d.lebihan_A.median())} | {pc(d.mdd_A.median())} | {nb(d.n_A.median(), 0)} |")
    return L


def banding_a02(D, saring, a02_saring, a02_param, a02_menang):
    """Sistem ditala lwn A02 bagi kaedah-lorong yang sama."""
    L = ['| Sistem | Skor saringan A02 / A03 (min lebihan) | Label A02 (rekod) | Label MENANG A02 | Menang A A02 / A03 | PF A A02 / A03 | Lebihan A A02 / A03 | Label A03 |',
         '|---|---|---|---|---|---|---|---|']
    s2 = {(r.kaedah, r.lorong): r.skor for r in a02_saring.itertuples()} if len(a02_saring) else {}
    s3 = {(r.kaedah, r.lorong): r.skor for r in saring[saring.varian == T3.UTAMA].itertuples()} if len(saring) else {}
    p2 = {r.tugas: r for r in a02_param.itertuples()} if len(a02_param) else {}
    m2 = {r.tugas: r for r in a02_menang.itertuples()} if len(a02_menang) else {}
    for r in D.itertuples():
        a, b = p2.get(r.tugas), m2.get(r.tugas)
        L.append(f"| {r.tugas} | {pc(s2.get((r.kaedah, r.lorong)))} / {pc(s3.get((r.kaedah, r.lorong)))} | "
                 f"{a.label if a is not None else 'tidak ditala'} | {b.label if b is not None else '—'} | "
                 f"{pc(getattr(b, 'menang_a', None))} / {pc(r.menang_a)} | {nb(getattr(b, 'pf_a', None))} / {nb(r.pf_a)} | "
                 f"{pc(getattr(a, 'lebihan_a', None))} / {pc(r.lebihan_a)} | {r.label} |")
    return L


def _gagal_ringkas(r):
    g = str(r.gagal or '') if not (isinstance(r.gagal, float) and math.isnan(r.gagal)) else ''
    if not g: return ''
    n = len(g.split('; '))
    return f' ({g})' if n == 1 else f' ({n} syarat)'


def laporan(D, ring, gab, saring, pilihan, hadapan, skop, a02_saring, a02_param, a02_menang, lp, keluar=HASIL):
    rendah = liputan_rendah(lp)
    L = ['# LAPORAN AUTOTUNE A03', '',
         f"Dijana oleh `AUTOTUNE/sahkan/sahkan_a03.py` ({ring['dijana']}). Spec: `AUTOTUNE/SPEC_A03.md` (termasuk pindaan §6). "
         'A01/A02 kekal tidak diubah. Parameter SEMASA ialah cadangan sahaja; tiada dagangan wang sebenar.', '',
         '## Sistem', '',
         '- Utama: F (EPS suku terkini tersedia > 0 dan pertumbuhan tahun ke tahun ≥ 25%; tiada data → tidak layak) ∧ M (SPY > SMA50 '
         'dan SMA50 > SMA200) pada hari isyarat; 5 slot × 20%; henti = maks(henti kaedah, 0.92 × harga masuk) mulai hari masuk + 1 '
         '(peraturan gap dan rendah hari masuk tidak berubah). Lain-lain seperti A02 (kos, slippage, gap, topeng universe, lorong).',
         '- Ablasi (dilaporkan sahaja): F sahaja, M sahaja, tanpa F/M — semuanya 5 slot dan had rugi 8%.',
         '- Tala: objektif lebihan atas SPY, kekangan SPEC_A02 §2 + kadar menang latih ≥ 50% (pelanggar: penalti SPEC_A02 '
         'tolak kekurangan kadar menang).', '',
         '## Kaveat data', '',
         '- Harga/universe: Release `autotune-data-a02`. EPS: Release `autotune-fundamental-a03` (Yahoo; EPS dilaporkan/dilaras '
         'penganalisis, bukan GAAP). Titik masa: sebelum buka → hari laporan; selainnya → hari dagangan berikutnya.']
    if lp:
        L.append('- Liputan EPS ("ada", `AUTOTUNE/fundamental/LIPUTAN.md`) 2013–2018: ' +
                 ', '.join(f'{y} {pc(v, 0)}' for y, v in sorted(lp.items()) if 2013 <= y <= 2018) +
                 ('; semua ≥ 70%.' if not rendah else f'; **LIPUTAN RENDAH** (< 70%) bagi {", ".join(map(str, rendah))}: '
                  'semua keputusan sistem dengan F ditanda "liputan rendah".'))
    else:
        L.append('- Liputan EPS: `AUTOTUNE/fundamental/LIPUTAN.md` tidak dapat dibaca; keputusan F dianggap "liputan rendah".')
    L += ['- Tiada saham delist (bias survivorship): angka ialah had atas. Pemangkin, pegangan institusi, pyramiding tidak dimodelkan.', '']
    L += ['## Pengurangan skop', ''] + ([f'- {s}' for s in skop] if skop else
                                        ['- Tiada: 20 kaedah × 2 lorong, 10 sistem ditala, 8 kajian, 120 percubaan (skop penuh).']) + ['']
    k = {l: int((D.label == l).sum()) for l in LABEL}
    L += ['## Kesimpulan', '',
          f"- Label MENANG (SPEC_A03 §6): MENANG {k['MENANG']}, HAMPIR {k['HAMPIR']}, TIDAK {k['TIDAK']} daripada {len(D)} sistem ditala"
          + (' (liputan rendah)' if rendah or not lp else '') + '. ' +
          ('Tiada sistem MENANG; kalau tak beli, cakap tak beli.' if not k['MENANG'] else 'Lihat portfolio gabungan.'),
          f"- {int(((D.lebihan_a > 0) & (D.lebihan_b > 0)).sum())}/{len(D)} mengatasi SPY atas OOS bersih (A dan B); "
          f"{int((D.lebihan_peng > 0).sum())}/{len(D)} dalam pengesahan. Label SPEC_A02 (rujukan): "
          + ', '.join(f"{l} {int((D.label_a02 == l).sum())}" for l in S2.LABEL) + '.', '']
    n_s = int((saring.status == 'SIAP').sum()) if len(saring) else 0
    L += ['## Saringan (peringkat 1): utama lwn ablasi', '',
          f"{len(saring)} baris = 20 kaedah × 2 lorong × 4 sistem (PARAM asal, 2013–2018, A dan B); SIAP {n_s}.", ''] + jadual_varian(saring)
    L += ['', f"Kaedah: pakar {', '.join(pilihan.get('pakar', []))}; lain (saringan A02 `asal` teratas) {', '.join(pilihan.get('lain', []))}. "
          f"Ditala (min kadar menang A/B teratas, CAGR A dan B > 0): {', '.join(pilihan.get('tugas', []))}.", '',
          '## Tala (peringkat 2)', '',
          f"{ring['n_tugas_siap']}/{ring['n_tugas']} tugasan SIAP; {ring['n_cubaan_jumlah']} percubaan. Kajian 0–5 = ujian 2013…2018 "
          '(latih 3 tahun sebelum), 6 = AKHIR (latih 2016–2018; pengesahan 2019-01-01 – hujung), 7 = SEMASA.', '',
          '## Label', '',
          'MENANG: menang ≥ 55% (A dan B), CAGR > 0 dan PF ≥ 1.3 (A dan B), MDD OOS ≥ −35%, pengesahan menang ≥ 55% dan CAGR > 0, '
          '≥ 100 dagangan OOS (A dan B), imbasan bersih — 11 syarat; HAMPIR = tepat satu gagal; TIDAK selainnya. Label SPEC_A02 '
          f'(rujukan): DSR N = {N_DSR} atas pulangan berlebihan.', '',
          '| Lorong | ' + ' | '.join(LABEL) + ' | ' + ' | '.join(f'A02: {l}' for l in S2.LABEL) + ' |',
          '|---|' + '---|' * (len(LABEL) + len(S2.LABEL))]
    for lo in T2.LORONG:
        d = D[D.lorong == lo]
        L.append(f'| {lo} | ' + ' | '.join(str(int((d.label == l).sum())) for l in LABEL) + ' | '
                 + ' | '.join(str(int((d.label_a02 == l).sum())) for l in S2.LABEL) + ' |')
    if ring.get('sr0_harian') is not None and not math.isnan(ring['sr0_harian']):
        L += ['', f"SR0 = {ring['sr0_harian']:.4f} (harian, {ring['n_sr_saringan']} SR saringan A02 + A03 utama)."]
    T = D.assign(_m=D[['menang_a', 'menang_b']].min(axis=1)).sort_values(['_m', 'lebihan_a'], ascending=False)
    L += ['', '## Sistem ditala: dagangan (OOS bersih A / B; pengesahan P = A+B)', '',
          '| # | Sistem | Label (gagal) | Label A02 | Menang % A / B / P | Kalah % A | Purata untung / rugi A | Jangkaan A / B / P | PF A / B / P | Dag. A / B / P |',
          '|---|---|---|---|---|---|---|---|---|---|']
    for i, r in enumerate(T.itertuples(), 1):
        L.append(f"| {i} | {r.tugas} | {r.label}{_gagal_ringkas(r)} | "
                 f"{r.label_a02} | {pc(r.menang_a, 0)} / {pc(r.menang_b, 0)} / {pc(r.menang_peng, 0)} | {pc(r.kalah_a, 0)} | "
                 f"{pc(r.purata_untung_a)} / {pc(r.purata_rugi_a)} | {pc(r.jangkaan_a, 2)} / {pc(r.jangkaan_b, 2)} / {pc(r.jangkaan_peng, 2)} | "
                 f"{nb(r.pf_a)} / {nb(r.pf_b)} / {nb(r.pf_peng)} | {r.n_a} / {r.n_b} / {r.n_peng} |")
    L += ['', '## Sistem ditala: pulangan lwn SPY', '',
          '| # | Sistem | CAGR A / B | Lebihan A / B (SPY OOS) | Pengesahan CAGR (lebihan; SPY) | MDD OOS / SPY | MDD peng. / SPY | DSR | Imbasan |',
          '|---|---|---|---|---|---|---|---|---|']
    for i, r in enumerate(T.itertuples(), 1):
        L.append(f"| {i} | {r.tugas} | {pc(r.cagr_a)} / {pc(r.cagr_b)} | {pc(r.lebihan_a)} / {pc(r.lebihan_b)} ({pc(r.spy_oos)}) | "
                 f"{pc(r.cagr_peng)} ({pc(r.lebihan_peng)}; {pc(r.spy_peng)}) | {pc(r.mdd_oos)} / {pc(r.spy_mdd_oos)} | "
                 f"{pc(r.mdd_peng)} / {pc(r.spy_mdd_peng)} | {'—' if pd.isna(r.dsr) else f'{r.dsr:.2f}'} | {r.imbasan} |")
    L += ['', '## Portfolio gabungan', '']
    if gab.get('terpilih'):
        L.append(f"Calon: {gab['asas_calon']} ({gab['n_calon']}; {len(gab.get('calon_dinilai', []))} dinilai). "
                 f"Terpilih: {', '.join(gab['terpilih'])}. Had MDD {pc(gab.get('had_mdd'))}. 5 slot × 20%.")
        for nm, t in (('oos_A', 'OOS bersih A'), ('oos_B', 'OOS bersih B'), ('pengesahan', 'Pengesahan A+B')):
            x = gab.get(nm) or {}
            L.append(f"- {t} ({x.get('mula')} – {x.get('akhir')}): CAGR {pc(x.get('cagr'))} lwn SPY {pc(x.get('spy'))} "
                     f"(lebihan {pc(x.get('lebihan'))}); MDD {pc(x.get('mdd'))} lwn SPY {pc(x.get('spy_mdd'))}")
    else:
        L.append(gab.get('catatan', 'tiada gabungan'))
    L += ['', '## Kriteria MENANG atas 40 kaedah-lorong A02 (rujukan, `menang_a02.csv`)', '']
    if len(a02_menang):
        k2 = {l: int((a02_menang.label == l).sum()) for l in LABEL}
        L.append(f"Dagangan dipegang A02 (8 slot × 12.5%, tanpa F/M) dijana semula dengan parameter setiap kajian: MENANG {k2['MENANG']}, "
                 f"HAMPIR {k2['HAMPIR']}, TIDAK {k2['TIDAK']}. Beza kadar menang A berbanding rekod A02: maks "
                 f"{pc((a02_menang.menang_a - a02_menang.menang_a_a02).abs().max())} (dagangan dijana semula atas data "
                 "tetingkap A+B; susunan seri rank boleh berbeza). Lima teratas ikut min kadar menang A/B:")
        T2_ = a02_menang.assign(_m=a02_menang[['menang_a', 'menang_b']].min(axis=1)).sort_values('_m', ascending=False).head(5)
        L += ['', '| Kaedah-lorong | Label | Menang A / B / P | PF A / B | CAGR A / B / P | MDD OOS | Gagal |', '|---|---|---|---|---|---|---|']
        for r in T2_.itertuples():
            L.append(f"| {r.tugas} | {r.label} | {pc(r.menang_a, 0)} / {pc(r.menang_b, 0)} / {pc(r.menang_peng, 0)} | {nb(r.pf_a)} / {nb(r.pf_b)} | "
                     f"{pc(r.cagr_a)} / {pc(r.cagr_b)} / {pc(r.cagr_peng)} | {pc(r.mdd_oos)} | {str(r.gagal)[:90]} |")
    else:
        L.append('`hasil_a03/menang_a02.csv` tiada (aliran kerja `autotune_menang_a03` belum dijalankan).')
    L += ['', '## Perbandingan dengan A02 (kaedah-lorong sama)', ''] + banding_a02(T, saring, a02_saring, a02_param, a02_menang)
    nph = sum(v.get('status') == 'PANDANG HADAPAN' for v in hadapan.values())
    L += ['', '## Imbasan pandang ke hadapan', '',
          f'{len(hadapan)} sistem diimbas (AKHIR dan SEMASA, 12 tarikh potong; isyarat termasuk topeng F dan M; F dikira daripada EPS '
          f'yang sudah dilaporkan pada setiap tarikh potong); PANDANG HADAPAN: {nph}. Butiran: [PANDANG_HADAPAN.md](PANDANG_HADAPAN.md).', '',
          'Fail: `saringan.csv`, `pilihan.json`, `parameter_sedia.csv`, `menang_a02.csv`, `gabungan.json`, `tala/<ID>_<lorong>/kNN.json`. '
          'Holdout sebenar: ujian ke hadapan sejak 16 Okt 2026 (tidak dinilai).']
    L = [x for i, x in enumerate(L) if not (x == '' and i and L[i - 1] == '')]
    if len(L) > 150: L = L[:149] + ['(dipotong pada 150 baris)']
    open(os.path.join(keluar, 'LAPORAN.md'), 'w').write('\n'.join(L) + '\n')
    return len(L)


def rekod_papan(r, rendah):
    d = S2.rekod_papan(r); d['versi'] = 'A03'; d['sistem'] = 'F+M, 5×20%, had rugi 8%'
    d['label_a02'] = r.get('label_a02'); d['gagal'] = r.get('gagal')
    for k in MA.STAT:
        for ak in ('a', 'b', 'peng'): d[f'{k}_{ak}'] = r.get(f'{k}_{ak}')
    d = U.bersih(d, 4)
    if rendah: d['catatan'] = ('liputan rendah; ' + (d.get('catatan') or '')).strip('; ')
    return d


def jalan(data_dir=None, eps=None, proses=4, maks=MAKS, calon_maks=CALON_MAKS, tanpa_gabungan=False, keluar=HASIL, tala=TALA,
          skop=(), a02=os.path.join(AT, 'hasil_a02'), liputan_md=LIPUTAN):
    pilihan = json.load(open(os.path.join(keluar, 'pilihan.json')))
    try: saring = pd.read_csv(os.path.join(keluar, 'saringan.csv'))
    except Exception: saring = pd.DataFrame(columns=['kaedah', 'lorong', 'varian', 'status', 'skor'])
    hadapan = {}
    try: hadapan = json.load(open(os.path.join(keluar, 'pandang_hadapan.json')))
    except Exception: pass
    sr0, n_sr = sr0_kumulatif(os.path.join(a02, 'saringan.csv'), os.path.join(keluar, 'saringan.csv'))
    sk = {(r.kaedah, r.lorong): r.skor for r in saring[saring.varian == T3.UTAMA].itertuples()} if len(saring) else {}
    semua, R = {}, []
    for nama in pilihan['tugas']:
        kaj = S2.baca_kajian(nama, tala); semua[nama] = kaj
        R.append(nilai(nama, kaj, sr0, hadapan, sk.get(T2.pecah_tugas(nama))))
    D = pd.DataFrame(R)
    lp = liputan(liputan_md); rendah = bool(liputan_rendah(lp)) or not lp
    if len(D):
        D['liputan_rendah'] = rendah
        D.to_csv(os.path.join(keluar, 'parameter_sedia.csv'), index=False, float_format='%.6g')
    gab = dict(versi='A03', terpilih=[], catatan='gabungan tidak dijalankan')
    if not tanpa_gabungan and len(D):
        gab = gabungan(D, semua, data_dir, eps, proses, maks, calon_maks)
    U.tulis_json(os.path.join(keluar, 'gabungan.json'), U.bersih(gab))
    try: a02_menang = pd.read_csv(os.path.join(keluar, 'menang_a02.csv'))
    except Exception: a02_menang = pd.DataFrame(columns=['tugas', 'label', 'menang_a', 'menang_b'])
    ring = dict(versi='A03', dijana=time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime()), n_kaedah=len(D),
                n_tugas=8 * len(pilihan['tugas']),
                n_tugas_siap=int(sum(len(str(x)) for x in D.kajian_siap)) if len(D) else 0,
                n_cubaan_jumlah=int(D.n_cubaan.sum()) if len(D) else 0, sr0_harian=sr0, n_sr_saringan=n_sr, n_dsr=N_DSR,
                kiraan_label={l: int((D.label == l).sum()) if len(D) else 0 for l in LABEL},
                kiraan_label_a02={l: int((D.label_a02 == l).sum()) if len(D) else 0 for l in S2.LABEL},
                kiraan_label_lorong={lo: {l: int(((D.lorong == lo) & (D.label == l)).sum()) if len(D) else 0 for l in LABEL}
                                     for lo in T2.LORONG},
                menang_a02={l: int((a02_menang.label == l).sum()) for l in LABEL} if len(a02_menang) else None,
                tempoh=dict(saringan=list(T2.SARING), oos=['2013-01-01', '2018-12-31'], pengesahan=['2019-01-01', None]),
                spy=dict(oos=D.spy_oos.dropna().iloc[0] if len(D) and D.spy_oos.notna().any() else None,
                         pengesahan=D.spy_peng.dropna().iloc[0] if len(D) and D.spy_peng.notna().any() else None),
                liputan={str(k): v for k, v in lp.items()}, liputan_rendah=rendah, sistem=T3.keterangan_sistem(),
                varian=pilihan.get('varian'), belum_ditala=[], skop=list(skop), label=LABEL)
    U.tulis_json(os.path.join(keluar, 'ringkasan.json'), U.bersih(ring))
    U.tulis_json(os.path.join(keluar, 'papan.json'), dict(versi='A03', dijana=ring['dijana'], tempoh=ring['tempoh'],
                                                         kaedah=[rekod_papan(r, rendah) for r in R], gabungan=gab.get('terpilih', [])))
    try: a02_saring = pd.read_csv(os.path.join(a02, 'saringan.csv'))
    except Exception: a02_saring = pd.DataFrame(columns=['kaedah', 'lorong', 'skor'])
    try: a02_param = pd.read_csv(os.path.join(a02, 'parameter_sedia.csv'))
    except Exception: a02_param = pd.DataFrame(columns=['tugas', 'label', 'lebihan_a'])
    n = laporan(D, ring, gab, saring, pilihan, hadapan, list(skop), a02_saring, a02_param, a02_menang, lp, keluar) if len(D) else 0
    return D, gab, ring, n


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--data', default=None); a.add_argument('--cache', default=os.environ.get('AUTOTUNE_CACHE', T3.CACHE))
    a.add_argument('--fund', default=T3.CACHE_F)
    a.add_argument('--proses', type=int, default=4); a.add_argument('--maks', type=int, default=MAKS)
    a.add_argument('--calon-maks', type=int, default=CALON_MAKS); a.add_argument('--tanpa-gabungan', action='store_true')
    a.add_argument('--skop', action='append', default=[], help='catatan pengurangan skop (boleh berulang)')
    x = a.parse_args()
    dd = x.data or (None if x.tanpa_gabungan else str(T2.ambil_data(x.cache)))
    eps = None if x.tanpa_gabungan else T3.muat_eps(T3.ambil_fundamental(x.fund))
    D, gab, ring, n = jalan(dd, eps, x.proses, x.maks, x.calon_maks, x.tanpa_gabungan, skop=x.skop)
    print(f"A03: {len(D)} sistem; label {ring['kiraan_label']}; gabungan {gab.get('terpilih')}; LAPORAN {n} baris")


if __name__ == '__main__':
    main()
