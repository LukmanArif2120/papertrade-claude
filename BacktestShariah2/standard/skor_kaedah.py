"""Skor Kaedah 0-100: PANGKAT maklumat semua kaedah Mxx/Nxx/GB atas SATU penyebut (Lejar Penuh lorong 1
LANGSUNG — penyebut yang sama dengan kad skor), dipradaftar 9 Nov 2026 (`standard/SPEC_SKOR_KAEDAH.md`).

BUKAN keputusan wang sebenar: keputusan itu hanya datang daripada status TERBUKTI kad skor
(`standard/kad_skor.py`). Skor ini menjawab "kaedah mana paling baik DARI SEMUA SEGI setakat ini" dan
diukur kebolehramalannya setiap larian (Spearman skor lalu lawan pulangan lorong T4 selepasnya).

Empat tiang (berat ikut konsensus pakar — Tharp, Minervini, Schwager, Radge, Carver, Harvey-Liu,
López de Prado, Pardo, Davey, Kestner, Martin, Clenow; rujukan dalam spec):
  A Keuntungan 35 : A1 jangkaan per posisi 20 · A2 lebihan T4 lawan SPUS 10 · A3 payoff 5
  B Ketahanan  30 : B1 pulangan/|MDD| T4 12 · B2 Ulcer Index 6 · B3 CVaR10 6 · B4 tanpa5 6
  C Bukti      25 : C1 t Newey-West buku harian, dideflasi N ujian 12 · C2 saiz sampel 8 · C3 liputan rejim 5
  D Konsisten  10 : D1 K-ratio ekuiti T4 4 · D2 lift masuk 3 · D3 kecekapan jalan-ke-depan 3
Setiap metrik dipetakan 0-100 dengan SAUH TETAP (bukan persentil data: persentil hanyut). Tiang = purata
berberat metriknya (metrik tiada data = 50, neutral). Jumlah = min geometri berberat empat tiang (satu tiang
hampir sifar menarik jumlah ke bawah). Kecutan ke 50: skor = 50 + (jumlah - 50) x h/(h + KECUT_H), h = hari
beli langsung. Siling ikut kad skor: NEGATIF <= 20, GANTUNG/BERSARA <= 30, GAGAL <= 40.

Input : data/analisis/kad_skor.json (semua statistik setiap kaedah), portfolio_slot/t4_siri.csv (ekuiti T4).
Output: data/analisis/skor_kaedah.json, laporan/SKOR_KAEDAH.md, data/analisis/skor_kaedah_sejarah.csv
        (snapshot skor setiap sesi, untuk semakan Spearman).
  python3 BacktestShariah2/standard/skor_kaedah.py   (analisis.yml, selepas kad_skor.py)
Rekod analisis sahaja: tiada order, tiada wang sebenar.
"""
import json
import math
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
sys.path.insert(0, HERE)

# ---------- PRADAFTAR 9 Nov 2026 (keputusan pengguna) - jangan ubah tanpa keputusan pengguna + pradaftar bertarikh ----------
BERAT_TIANG = {'A': 0.35, 'B': 0.30, 'C': 0.25, 'D': 0.10}
# metrik: (tiang, berat dalam tiang)
BERAT_METRIK = {'A1': ('A', 20), 'A2': ('A', 10), 'A3': ('A', 5),
                'B1': ('B', 12), 'B2': ('B', 6), 'B3': ('B', 6), 'B4': ('B', 6),
                'C1': ('C', 12), 'C2': ('C', 8), 'C3': ('C', 5),
                'D1': ('D', 4), 'D2': ('D', 3), 'D3': ('D', 3)}
# sauh (x0 -> 0, x50 -> 50, x100 -> 100; linear sekeping-sekeping, dipotong 0..100)
SAUH = {'A1': (-2.0, 0.0, 2.0),      # jangkaan % setiap posisi, ditanda-ke-pasaran, kos ditolak
        'A2': (-10.0, 0.0, 10.0),    # lebihan mata lorong T4 L1 lawan SPUS, tingkap sama
        'A3': (0.5, 1.0, 2.0),       # payoff untung purata / |rugi purata| (Minervini 2:1)
        'B1': (-1.0, 0.0, 1.0),      # pulangan / |MDD| lorong T4 L1 (MAR; Schwager, Radge, Faith)
        'B2': (10.0, 5.0, 0.0),      # Ulcer Index ekuiti T4 L1 (% ; Martin) - lebih kecil lebih baik
        'B3': (-24.0, -16.0, -8.0),  # CVaR10 % setiap posisi
        'B4': (-2.0, 0.0, 2.0),      # tanpa5: jangkaan selepas buang 5% posisi terbaik (Davey)
        'D1': (-0.2, 0.0, 0.2),      # K-ratio = t cerun log-ekuiti / sqrt(n) (Kestner; 0.2 ~ Sharpe tahunan 1.8)
        'D3': (0.0, 0.5, 1.0)}       # kecekapan jalan-ke-depan = purata harian hadapan / purata harian backtest (Pardo 50%)
C1_T_MIN = 2.0                       # sauh t minimum; dinaikkan ke E[maks N] bila N kaedah besar (López de Prado)
C2_HARI_PENUH = 60                   # hari beli yang memberi markah penuh (skala log)
C2_TUTUP_PENUH = 100                 # posisi ditutup yang memberi markah penuh (Tharp: 100 dagangan)
C3_REJIM_PENUH = 10                  # hari beli dalam SETIAP rejim untuk markah penuh (= G1_REJIM_MIN)
D2_LIFT_SKALA = 4.0                  # lift mata: -4 -> 0, +4 -> 100; lulus BH-FDR positif -> 100, negatif -> 0
KECUT_H = 20                         # kecutan ke 50: berat data = h / (h + KECUT_H), h = hari beli langsung
SILING = {'NEGATIF': 20.0, 'GANTUNG': 30.0, 'BERSARA': 30.0, 'GAGAL': 40.0}
LANTAI_GEO = 1.0                     # lantai tiang dalam min geometri (elak log 0)
SPEARMAN_HARI = 7                    # semakan kebolehramalan: skor >= 7 hari kalendar lalu lawan pulangan T4 selepasnya
NEUTRAL = 50.0
# ---------------------------------------------------------------------------------------------------------------------

AN = os.path.join(BS2, 'data', 'analisis')
KS_JSON = os.environ.get('KS_JSON', os.path.join(AN, 'kad_skor.json'))
T4_SIRI = os.environ.get('SK_T4_SIRI', os.path.join(BS2, 'portfolio_slot', 't4_siri.csv'))
SPUS_HARIAN = os.environ.get('SPUS_HARIAN', os.path.join(BS2, 'data', 'penanda_aras', 'spus_harian.csv'))
JSN = os.environ.get('SK_JSON', os.path.join(AN, 'skor_kaedah.json'))
MD = os.environ.get('SK_MD', os.path.join(BS2, 'laporan', 'SKOR_KAEDAH.md'))
SEJARAH = os.environ.get('SK_SEJARAH', os.path.join(AN, 'skor_kaedah_sejarah.csv'))
SPEC = 'standard/SPEC_SKOR_KAEDAH.md'
PRADAFTAR = '2026-11-09'
TIANG_NAMA = {'A': 'Untung', 'B': 'Tahan', 'C': 'Bukti', 'D': 'Konsisten'}


def _ada(v):
    return v is not None and not (isinstance(v, float) and (math.isnan(v) or math.isinf(v)))


def peta(x, sauh):
    """Petakan x ke 0..100 dengan sauh (x0, x50, x100): linear sekeping-sekeping, dipotong. None -> NEUTRAL."""
    if not _ada(x):
        return NEUTRAL
    x0, x50, x100 = sauh
    x = float(x)
    if x100 > x0:                       # lebih besar lebih baik
        if x <= x50:
            v = 50.0 * (x - x0) / (x50 - x0)
        else:
            v = 50.0 + 50.0 * (x - x50) / (x100 - x50)
    else:                               # lebih kecil lebih baik
        if x >= x50:
            v = 50.0 * (x0 - x) / (x0 - x50)
        else:
            v = 50.0 + 50.0 * (x50 - x) / (x50 - x100)
    return float(min(100.0, max(0.0, v)))


def e_maks(n, gamma=0.5772156649):
    """Jangkaan maksimum n normal piawai (López de Prado, Deflated Sharpe Ratio): deflasi untuk n ujian."""
    n = int(n)
    if n < 2:
        return 0.0
    return float((1 - gamma) * stats.norm.ppf(1 - 1 / n) + gamma * stats.norm.ppf(1 - 1 / (n * math.e)))


def t_sauh(n_kaedah):
    return max(C1_T_MIN, e_maks(n_kaedah))


def t_buku(r):
    """t Newey-West purata buku harian, dipulihkan daripada selang 95% kad skor (purata, had bawah/atas, sesi)."""
    m, lo, hi, n = r.get('buku_harian'), r.get('buku_ci_bawah'), r.get('buku_ci_atas'), r.get('buku_sesi')
    if not (_ada(m) and _ada(lo) and _ada(hi)) or not n or n < 3 or hi <= lo:
        return None
    tc = float(stats.t.ppf(0.975, int(n) - 1))
    se = (hi - lo) / 2 / tc
    return float(m / se) if se > 0 else None


def skala_log(x, penuh):
    """0 -> 0, penuh -> 100 pada skala log(1 + x); dipotong 100."""
    if not _ada(x) or x <= 0:
        return 0.0
    return float(min(100.0, 100.0 * math.log1p(float(x)) / math.log1p(penuh)))


def ulcer(ekuiti):
    """Ulcer Index (%) = punca purata kuasa dua kejatuhan daripada puncak (puncak termasuk asas 1.0)."""
    e = np.asarray([v for v in ekuiti if _ada(v)], float)
    if len(e) < 2:
        return None
    puncak = np.maximum.accumulate(np.r_[1.0, e])[1:]
    dd = (e / puncak - 1.0) * 100
    return float(np.sqrt(np.mean(dd ** 2)))


def k_ratio(ekuiti):
    """K-ratio (Kestner, bebas panjang sampel): t cerun regresi log-ekuiti atas masa / sqrt(n)."""
    e = np.asarray([v for v in ekuiti if _ada(v) and v > 0], float)
    n = len(e)
    if n < 5:
        return None
    y, x = np.log(e), np.arange(n, dtype=float)
    res = stats.linregress(x, y)
    if not np.isfinite(res.stderr) or not np.isfinite(res.slope):
        return None
    if res.stderr == 0:                       # garis lurus sempurna: t tak terhingga
        return 0.0 if res.slope == 0 else math.copysign(1e3, res.slope)
    return float(res.slope / res.stderr / math.sqrt(n))


def skor_d2(r):
    """Lift masuk: tiada ujian -> neutral; lulus BH-FDR positif -> 100, negatif -> 0; selain itu skala linear."""
    lift = r.get('lift')
    if not _ada(lift):
        return NEUTRAL
    if r.get('lift_lulus'):
        return 100.0 if lift > 0 else 0.0
    return float(min(100.0, max(0.0, 50.0 + 50.0 * lift / D2_LIFT_SKALA)))


def wfe(r):
    """Kecekapan jalan-ke-depan: purata harian buku hadapan / (purata backtest setiap dagangan / hari pegang backtest).
    None jika tiada backtest (Nxx/GB) atau backtest tidak positif."""
    bm, bp, bh = r.get('buku_harian'), r.get('bt_purata'), r.get('bt_hari')
    if not (_ada(bm) and _ada(bp) and _ada(bh)) or bp <= 0 or bh <= 0:
        return None
    return float(bm / (bp / bh))


def mdd_asas(e):
    """MDD % dengan puncak termasuk asas 1.0 (peraturan 3 BANDING_SPUS.md)."""
    e = np.asarray(e, float)
    puncak = np.maximum.accumulate(np.r_[1.0, e])[1:]
    return float((e / puncak - 1.0).min() * 100)


def lorong_langsung(T4, spus, mid, mula):
    """Lorong T4 L1 kaedah `mid` DIPOTONG pada sesi LANGSUNG pertama (>= `mula`) dan diasas semula supaya tutup
    sesi sebelumnya = 1.0 (sama seperti lorong yang bermula pada buka hari itu). SPUS: asas = BUKA sesi pertama
    potongan (peraturan 1 BANDING_SPUS.md). Pindaan 9 Nov 2026 (a): lorong Nxx/GB bermula 16 Okt dengan posisi
    isian bina semula; penyebut skor ialah LANGSUNG sahaja, jadi sesi sebelum mula LANGSUNG dibuang.
    -> dict(sesi, pul, mdd, nisbah, spus, lebih_spus, ekuiti) atau None."""
    kol = f'{mid}|L1'
    if T4 is None or kol not in T4.columns:
        return None
    e = pd.to_numeric(T4[kol], errors='coerce').dropna()
    if not len(e):
        return None
    mula = str(mula or '')
    sebelum = e[e.index < mula]
    e2 = e[e.index >= mula]
    if not len(e2):
        return None
    ek = e2 / (float(sebelum.iloc[-1]) if len(sebelum) else 1.0)
    pul = float(100 * (ek.iloc[-1] - 1))
    md = mdd_asas(ek.to_numpy())
    nis = pul / abs(md) if md < 0 else math.copysign(10.0, pul) if pul else 0.0
    out = dict(sesi=int(len(ek)), pul=pul, mdd=md, nisbah=float(min(10.0, max(-10.0, nis))), spus=None,
               lebih_spus=None, ekuiti=ek.tolist())
    t0 = ek.index[0]
    if spus is not None and t0 in spus.index and _ada(spus.buka.get(t0)) and spus.buka.loc[t0] > 0:
        tt = spus.tutup.reindex(sorted(set(spus.index) | set(ek.index))).ffill().reindex(ek.index)
        if tt.notna().all():
            sp = float(100 * (tt.iloc[-1] / float(spus.buka.loc[t0]) - 1))
            out.update(spus=sp, lebih_spus=pul - sp)
    return out


def muat_t4(path=None):
    """DataFrame ekuiti lorong T4, indeks tarikh 'YYYY-MM-DD' (lajur 'ID|L1'/'ID|L2'); None jika fail tiada."""
    path = path or T4_SIRI
    if not os.path.exists(path):
        return None
    t = pd.read_csv(path, dtype={'tarikh': str})
    return t.set_index('tarikh').sort_index()


def muat_spus(path=None):
    path = path or SPUS_HARIAN
    if not os.path.exists(path):
        return None
    d = pd.read_csv(path, comment='#')
    d['tarikh'] = pd.to_datetime(d.tarikh).dt.strftime('%Y-%m-%d')
    return d.sort_values('tarikh').set_index('tarikh')[['buka', 'tutup']].astype(float)


def metrik(r, siri_t4, n_kaedah):
    """Nilai mentah dan markah 0-100 setiap metrik bagi satu baris kad skor. siri_t4: {id: dict lorong_langsung}."""
    L = siri_t4.get(r['id']) or {}
    ek = L.get('ekuiti')
    ui = ulcer(ek) if ek is not None else None
    kr = k_ratio(ek) if ek is not None else None
    tb = t_buku(r)
    ts = t_sauh(n_kaedah)
    ef = wfe(r)
    mentah = dict(A1=r.get('jangkaan'), A2=L.get('lebih_spus'), A3=r.get('payoff'),
                  B1=L.get('nisbah'), B2=ui, B3=r.get('cvar10'), B4=r.get('tanpa5'),
                  C1=tb, C2=None, C3=min(r.get('hari_on') or 0, r.get('hari_off') or 0),
                  D1=kr, D2=r.get('lift'), D3=ef)
    markah = {k: peta(mentah[k], SAUH[k]) for k in SAUH}
    markah['C1'] = NEUTRAL if tb is None else float(min(100.0, max(0.0, 50.0 + 50.0 * tb / ts)))
    markah['C2'] = 0.5 * skala_log(r.get('hari_beli'), C2_HARI_PENUH) + 0.5 * skala_log(r.get('tutup'), C2_TUTUP_PENUH)
    markah['C3'] = float(min(100.0, 100.0 * mentah['C3'] / C3_REJIM_PENUH))
    markah['D2'] = skor_d2(r)
    mentah['T4_sesi'] = L.get('sesi')
    mentah['T4_pul'] = L.get('pul')
    mentah['T4_mdd'] = L.get('mdd')
    return mentah, markah, ts


def tiang(markah):
    """Purata berberat metrik dalam setiap tiang."""
    out = {}
    for t in BERAT_TIANG:
        w = [(markah[k], b) for k, (tt, b) in BERAT_METRIK.items() if tt == t]
        out[t] = float(sum(v * b for v, b in w) / sum(b for _, b in w))
    return out


def geometri(T):
    """Min geometri berberat empat tiang, lantai LANTAI_GEO."""
    return float(math.exp(sum(BERAT_TIANG[t] * math.log(max(T[t], LANTAI_GEO)) for t in BERAT_TIANG)))


def kecut(g, hari_beli):
    h = max(float(hari_beli or 0), 0.0)
    w = h / (h + KECUT_H)
    return float(NEUTRAL + (g - NEUTRAL) * w), float(w)


def siling(skor, r):
    for k in (r.get('status'), r.get('pantau')):
        if k in SILING:
            skor = min(skor, SILING[k])
    return float(skor)


def skor_baris(r, siri_t4, n_kaedah):
    mentah, markah, ts = metrik(r, siri_t4, n_kaedah)
    T = tiang(markah)
    g = geometri(T)
    s, w = kecut(g, r.get('hari_beli'))
    s2 = siling(s, r)
    return dict(id=r['id'], nama=r.get('nama', ''), keluarga=r.get('keluarga', ''), status=r.get('status'),
                pantau=r.get('pantau'), hari_beli=r.get('hari_beli'), n=r.get('n'), tutup=r.get('tutup'),
                skor=round(s2, 1), skor_mentah=round(g, 1), berat_data=round(w, 3), siling=(s2 < s - 1e-9),
                untung=round(T['A'], 1), tahan=round(T['B'], 1), bukti=round(T['C'], 1), konsisten=round(T['D'], 1),
                markah={k: round(v, 1) for k, v in markah.items()},
                mentah={k: (round(v, 4) if isinstance(v, float) else v) for k, v in mentah.items() if _ada(v)},
                t_sauh=round(ts, 2))


def muat_siri_t4(kad, path=None, spus_path=None):
    """{id: lorong_langsung(...)} bagi setiap baris kad skor (lorong T4 L1 dipotong pada mula LANGSUNG kaedah itu).
    Laluan dibaca pada masa panggilan (bukan masa takrif) supaya ujian boleh menukar T4_SIRI/SPUS_HARIAN."""
    T4, S = muat_t4(path or T4_SIRI), muat_spus(spus_path or SPUS_HARIAN)
    out = {}
    for r in kad:
        L = lorong_langsung(T4, S, r['id'], r.get('mula_langsung'))
        if L:
            out[r['id']] = L
    return out


def baca_kad(path=KS_JSON):
    import kad_skor as KS
    return KS.baca_json(path)


# ---------------------------------------------------------------- sejarah + Spearman
def kemas_sejarah(path, harga_pada, rows, kad):
    """Tambah snapshot (tarikh harga, id, skor, t4_pul = pulangan lorong T4 L1 LANGSUNG) jika tarikh itu belum ada.
    Pulangkan DataFrame penuh."""
    t4 = {r['id']: r['mentah'].get('T4_pul') for r in rows}
    baru = pd.DataFrame(dict(tarikh=harga_pada, id=[r['id'] for r in rows], skor=[r['skor'] for r in rows],
                             t4_pul=[t4.get(r['id']) for r in rows]))
    if os.path.exists(path):
        lama = pd.read_csv(path, dtype={'tarikh': str})
        if harga_pada in set(lama.tarikh):
            return lama
        S = pd.concat([lama, baru], ignore_index=True)
    else:
        S = baru
    os.makedirs(os.path.dirname(path), exist_ok=True)
    S.to_csv(path, index=False, float_format='%.4g')
    return S


def spearman(S, harga_pada, rows, kad, hari=SPEARMAN_HARI):
    """Skor snapshot terkini yang >= `hari` kalendar sebelum harga_pada lawan pulangan T4 L1 sejak snapshot itu.
    Pulangan sejak = (1 + t4_pul_kini) / (1 + t4_pul_dulu) - 1. None jika belum ada snapshot cukup lama."""
    if S is None or not len(S):
        return None
    had = str((pd.Timestamp(harga_pada) - pd.Timedelta(days=hari)).date())
    calon = sorted(t for t in set(S.tarikh) if t <= had)
    if not calon:
        return None
    t0 = calon[-1]
    dulu = S[S.tarikh == t0].set_index('id')
    kini = {r['id']: r['mentah'].get('T4_pul') for r in rows}
    x, y = [], []
    for mid, r in dulu.iterrows():
        a, b = r.get('t4_pul'), kini.get(mid)
        if _ada(a) and _ada(b) and _ada(r.get('skor')):
            x.append(float(r['skor']))
            y.append((1 + b / 100) / (1 + a / 100) - 1)
    if len(x) < 10:
        return dict(tarikh=t0, n=len(x), rho=None, p=None)
    res = stats.spearmanr(x, y)
    return dict(tarikh=t0, n=len(x), rho=round(float(res.statistic), 3), p=round(float(res.pvalue), 4))


# ---------------------------------------------------------------- keluaran
def tulis_json(path, meta, rows):
    kol = [k for k in rows[0]] if rows else []
    out = [json.dumps([r.get(k) for k in kol], ensure_ascii=False, separators=(',', ':')) for r in rows]
    head = json.dumps(dict(meta, kol=kol), ensure_ascii=False, separators=(',', ':'))[:-1]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(head + ',"rows":[\n' + ',\n'.join(out) + '\n]}\n')


def baca_json(path):
    with open(path, encoding='utf-8') as f:
        A = json.load(f)
    kol = A.pop('kol')
    return A, [dict(zip(kol, v)) for v in A.pop('rows')]


def sama_isi(path, meta, rows):
    """Benar jika fail sedia ada mempunyai baris dan tarikh harga yang sama (hanya cap masa 'kini' berbeza)."""
    try:
        M, R = baca_json(path)
    except (OSError, ValueError, KeyError):
        return False
    return M.get('harga_pada') == meta.get('harga_pada') and R == json.loads(json.dumps(rows))


def laporan(M, rows):
    import status_kad

    def f(v, fmt='{:.1f}'):
        return '–' if not _ada(v) else fmt.format(v)
    sp = M.get('spearman')
    if sp is None:
        sp_t = (f'belum ada snapshot skor ≥ {SPEARMAN_HARI} hari lalu (sejarah bermula {M["harga_pada"]}); '
                'skor dipercayai sebagai pangkat hanya selepas 8–12 minggu semakan positif.')
    elif sp.get('rho') is None:
        sp_t = f"snapshot {sp['tarikh']}: hanya {sp['n']} kaedah berpasangan; belum boleh dikira."
    else:
        sp_t = (f"skor pada {sp['tarikh']} lawan pulangan lorong T4 sejak itu, {sp['n']} kaedah: Spearman ρ = "
                f"{sp['rho']:+.3f} (p = {sp['p']:.3f}). " +
                ('Positif dan p < 0.05: skor meramal pangkat.' if sp['rho'] > 0 and sp['p'] < 0.05 else
                 'Belum ada bukti skor meramal pangkat; jangan pilih kaedah dengannya.'))
    A = ['# Skor Kaedah 0–100 (pangkat maklumat, BUKAN keputusan)', '', status_kad.baris(), '',
         f"Dijana {M['kini']} oleh `standard/skor_kaedah.py` (Actions `analisis.yml`, selepas kad skor). Harga pada "
         f"tutup {M['harga_pada']}; {M['kaedah']} kaedah; {M['hari_beli']} hari beli langsung (rejim ON {M['hari_on']}, "
         f"OFF {M['hari_off']}). Pradaftar {M['pradaftar']}: `{M['spec']}` (berat dan sauh dikunci "
         '`ujian/test_skor_kaedah.py::TestKunci`). Rekod analisis sahaja: tiada order, tiada wang sebenar.', '',
         '## Cara membaca', '',
         f"- **Skor** = min geometri berberat empat tiang (Untung {int(BERAT_TIANG['A']*100)} · Tahan "
         f"{int(BERAT_TIANG['B']*100)} · Bukti {int(BERAT_TIANG['C']*100)} · Konsisten {int(BERAT_TIANG['D']*100)}), "
         f"dikecut ke 50 mengikut data: berat data = hari beli ÷ (hari beli + {KECUT_H}). Kaedah dengan 2 hari beli "
         'tidak boleh menjauhi 50. 100 = unggul semua segi; 50 = neutral/tiada bukti; < 50 = lebih buruk daripada neutral.',
         '- **Siling** ikut kad skor: NEGATIF ≤ 20, GANTUNG/BERSARA ≤ 30, GAGAL ≤ 40. Tanda ⌈ = siling terpakai.',
         '- **Satu-satunya status yang membenarkan wang sebenar ialah TERBUKTI dalam `laporan/KAD_SKOR.md`.** Skor '
         'tinggi dengan status BELUM CUKUP bermaksud "paling menjanjikan setakat ini", bukan "selamat".',
         f"- Deflasi ujian berganda (López de Prado): sauh t Bukti C1 = maks({C1_T_MIN}, E[maks {M['kaedah']} normal]) = "
         f"{M['t_sauh']:.2f}.",
         f'- **Semakan kebolehramalan:** {sp_t}',
         '- Metrik T4 (A2, B1, B2, D1) dikira atas lorong T4 L1 **dipotong pada sesi LANGSUNG pertama** kaedah itu '
         '(Mxx 2026-10-16, Nxx/GB 2026-11-03) dan diasas semula; sesi isian bina semula tidak dikira (pindaan 9 Nov 2026 (a)). '
         'Lajur "T4 sesi/pul" di bawah ialah potongan itu, bukan lorong penuh `T4_KAEDAH.md`.', '',
         '## Semua kaedah, susun ikut Skor', '',
         '| # | Kaedah | Skor | Untung | Tahan | Bukti | Konsisten | Status kad | Hari beli | Posisi/tutup | '
         'Jangkaan % | T4 sesi | T4 pul % | T4 pul/|MDD| | Ulcer | t buku | Lift | WFE |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for i, r in enumerate(rows, 1):
        m = r['mentah']
        A.append(f"| {i} | `{r['id']}` {str(r['nama'])[:30]} | **{r['skor']:.1f}**{'⌈' if r['siling'] else ''} | "
                 f"{r['untung']:.0f} | {r['tahan']:.0f} | {r['bukti']:.0f} | {r['konsisten']:.0f} | {r['status']} | "
                 f"{r['hari_beli']} | {r['n']}/{r['tutup']} | {f(m.get('A1'), '{:+.2f}')} | {f(m.get('T4_sesi'), '{}')} | "
                 f"{f(m.get('T4_pul'), '{:+.2f}')} | {f(m.get('B1'), '{:+.2f}')} | "
                 f"{f(m.get('B2'))} | {f(m.get('C1'), '{:+.2f}')} | {f(m.get('D2'), '{:+.2f}')} | {f(m.get('D3'), '{:.2f}')} |")
    A += ['', '## Metrik dan sauh (0 · 50 · 100)', '',
          '| Metrik | Berat | Apa | Sauh | Pakar |', '|---|---|---|---|---|',
          f"| A1 | 20 | Jangkaan % setiap posisi, ditanda-ke-pasaran, kos ditolak | {SAUH['A1']} | Tharp, Minervini, Radge |",
          f"| A2 | 10 | Lebihan mata lorong T4 L1 (potongan LANGSUNG) lawan SPUS, tingkap sama | {SAUH['A2']} | Penanda aras SPUS (repo) |",
          f"| A3 | 5 | Payoff untung purata ÷ rugi purata | {SAUH['A3']} | Minervini 2:1 |",
          f"| B1 | 12 | Pulangan ÷ |MDD| lorong T4 L1 (MAR) | {SAUH['B1']} | Schwager, Radge, Faith |",
          f"| B2 | 6 | Ulcer Index ekuiti T4 L1 (%) — kecil lebih baik | {SAUH['B2']} | Martin |",
          f"| B3 | 6 | CVaR10: purata 10% posisi terburuk (%) | {SAUH['B3']} | Ekor kiri |",
          f"| B4 | 6 | tanpa5: jangkaan tanpa 5% posisi terbaik | {SAUH['B4']} | Davey (buang pemenang terbesar) |",
          f"| C1 | 12 | t Newey-West buku harian ÷ sauh t (≥ {C1_T_MIN}, dideflasi N ujian) | 0 → 50, sauh → 100 | Carver, Harvey-Liu, López de Prado |",
          f"| C2 | 8 | ½ log-skala hari beli (penuh {C2_HARI_PENUH}) + ½ log-skala posisi ditutup (penuh {C2_TUTUP_PENUH}) | – | Tharp 100 dagangan, Radge |",
          f"| C3 | 5 | min(hari beli ON, OFF) ÷ {C3_REJIM_PENUH} | – | Clenow; rejim QQQ (repo) |",
          f"| D1 | 4 | K-ratio: t cerun log-ekuiti T4 ÷ √n | {SAUH['D1']} | Kestner |",
          f"| D2 | 3 | Lift masuk (lulus BH-FDR → 100/0; selain itu ±{D2_LIFT_SKALA:.0f} mata) | – | Plasebo gate (repo) |",
          f"| D3 | 3 | Kecekapan jalan-ke-depan: purata harian hadapan ÷ backtest | {SAUH['D3']} | Pardo ≥ 50%, Davey |",
          '', 'Metrik tiada data = 50 (neutral). Kadar menang, median, rugi purata dan rugi terbesar sengaja TIDAK '
          'dimasukkan (pengiraan dua kali; pelajaran laporan KPI lama). Jangan ubah berat atau sauh selepas melihat '
          'data: dikunci oleh ujian unit dan memerlukan pradaftar bertarikh baharu.', '']
    return '\n'.join(A) + '\n'


def main():
    if not os.path.exists(KS_JSON):
        print('skor_kaedah: kad_skor.json tiada; jalankan kad_skor.py dahulu', file=sys.stderr)
        return 1
    M, kad = baca_kad(KS_JSON)
    siri = muat_siri_t4(kad)
    n = len(kad)
    rows = [skor_baris(r, siri, n) for r in kad]
    rows.sort(key=lambda r: (-r['skor'], -r['skor_mentah'], r['id']))
    harga_pada = M.get('harga_pada')
    S = kemas_sejarah(SEJARAH, harga_pada, rows, kad)
    sp = spearman(S, harga_pada, rows, kad)
    meta = dict(kini=str(pd.Timestamp.now(tz='UTC').date()), harga_pada=harga_pada, kaedah=n,
                hari_beli=M.get('hari_beli'), hari_on=M.get('hari_on'), hari_off=M.get('hari_off'),
                t_sauh=round(t_sauh(n), 3), spearman=sp, pradaftar=PRADAFTAR, spec=SPEC,
                berat_tiang=BERAT_TIANG, berat_metrik={k: v[1] for k, v in BERAT_METRIK.items()}, sauh=SAUH,
                kecut_h=KECUT_H, siling=SILING, kad_skor_kini=M.get('kini'),
                tajuk=(f"Teratas: {rows[0]['id']} {rows[0]['nama']} skor {rows[0]['skor']:.1f} "
                       f"(status kad {rows[0]['status']}) — pangkat maklumat, bukan keputusan") if rows else 'Tiada kaedah')
    if sama_isi(JSN, meta, rows):
        print(f'SKOR_KAEDAH | tiada perubahan (harga {harga_pada})')
        return 0
    tulis_json(JSN, meta, rows)
    os.makedirs(os.path.dirname(MD), exist_ok=True)
    open(MD, 'w', encoding='utf-8').write(laporan(meta, rows))
    print(f"SKOR_KAEDAH | {n} kaedah | {meta['tajuk']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
