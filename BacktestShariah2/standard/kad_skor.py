"""Kad skor keputusan: SATU jawapan kepada "kaedah mana untuk wang sebenar", dengan gate G1-G6 yang
DIPRADAFTAR 6 Nov 2026 dan DIPINDA 7 Nov 2026 (spec `standard/SPEC_KAD_SKOR.md`, bahagian "Pindaan 7 Nov
2026": gate disahkan plasebo dan diselaraskan dengan toleransi MDD pengguna -10%).

Mengapa ia wujud (`reports/Audit dashboard v154 pilih kaedah.md`): dashboard v154 memberi tujuh jawapan
"kaedah terbaik" yang tidak bersetuju. Kad ini memakai SATU penyebut - setiap posisi Lejar Penuh lorong 1
yang direkod LANGSUNG (`lift_kaedah.MULA_LANGSUNG`) - jadi kesemua kaedah dinilai pada paksi sama.

Gate (ambang di bawah ialah PRADAFTAR; `ujian/test_kad_skor.py::TestKunci` gagal jika ia diubah):
  G1 kematangan : hari beli langsung >= maks(G1_HARI_BELI_MIN, hari beli perlu untuk lift G1_LIFT_MATA)
                  DAN >= G1_REJIM_MIN hari beli dalam rejim ON DAN >= G1_REJIM_MIN dalam rejim OFF
                  (ON = QQQ > SMA50 DAN SMA10 > SMA20 pada tarikh isyarat).
  G2 jangkaan   : BUKU kaedah (berat sama setiap posisi, keluar lorong 1, kos 0.2%/pusingan, ditanda
                  setiap hari): purata pulangan harian > 0 DAN had bawah 95% > 0, SE Newey-West lag
                  G2_NW_LAG. (SE ikut hari beli dibuang: posisi terbuka semua hari beli berkongsi satu tanda.)
  G3 lift masuk : `lift_kaedah.py` - ufuk tetap 10 sesi, asas hari x tercile ATR, SE dua hala, BH-FDR q G3_Q.
  G4 hari-0     : bilangan henti pada hari beli <= G4_HARI0_MAKS (= 0).
  G5 pantau     : status pantau Papan Penganalisis bukan GANTUNG/BERSARA, dan kejatuhan kohort
                  p_dd <= p_dd_had jika had wujud.
  G6 portfolio  : lorong T4 L1 (`portfolio_t4.py`): sesi >= G6_SESI DAN pulangan > 0 DAN pulangan pada MDD
                  G6_MDD_HAD > SPUS pada MDD sama DAN nisbah pulangan/|MDD| > maksimum jalur rawak.
Status (satu kosa kata, keutamaan atas ke bawah):
  NEGATIF     - G1 lulus DAN lift masuk negatif yang bertahan BH-FDR
  GAGAL       - G5 gagal, atau G1 lulus tetapi G2/G3/G4 gagal
  BELUM CUKUP - G1 belum lulus
  CALON       - G1-G5 lulus; G6 (portfolio lawan SPUS pada MDD -10%) belum
  TERBUKTI    - G1-G6 lulus = calon wang sebenar
Lajur maklumat (BUKAN gate): menang %, payoff, tanpa5, CVaR, MAE/MFE.

Rekod analisis sahaja: tiada order, tiada wang sebenar.
  python3 BacktestShariah2/standard/kad_skor.py   (analisis.yml, selepas lift_kaedah + portfolio_t4)
Keluaran: data/analisis/kad_skor.json (= db dashboard `analisis/kad_skor`), laporan/KAD_SKOR.md
"""
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
sys.path.insert(0, HERE)

# ---------- PRADAFTAR 6 Nov 2026, PINDAAN 7 Nov 2026 - jangan ubah tanpa keputusan pengguna + pradaftar bertarikh ----------
G1_HARI_BELI_MIN = 20       # PANTAU_G Papan Penganalisis; lantai label pengguna 14 Okt
G1_BEZA_MATA = 1.0          # maklumat sahaja sejak 7 Nov (laluan "posisi ditutup" dibuang daripada G1)
G1_LIFT_MATA = 2.0          # lift yang mesti boleh dilihat merentas semua kaedah (LIFT_KAEDAH.md)
G1_REJIM_MIN = 10           # PINDAAN 7 Nov: hari beli langsung minimum dalam SETIAP rejim (ON dan OFF)
Z_ALPHA, Z_KUASA = 1.96, 0.84
G2_ALPHA = 0.05             # selang keyakinan 95% dua-hujung; had bawah mesti > 0
G2_NW_LAG = 5               # PINDAAN 7 Nov: SE Newey-West buku harian
G3_Q = 0.05                 # BH-FDR, sama dengan lift_kaedah.Q_FDR
G6_SESI = 126               # ~6 bulan; BANDING_SPUS.md: tanda pertama kelebihan 20 mata/tahun
G6_MDD_HAD = -10.0          # PINDAAN 7 Nov: toleransi MDD akaun pengguna; bandingan pada MDD sama
G4_HARI0_MAKS = 0           # PINDAAN 6 Nov 2026 (keputusan pengguna): henti hari-0 mesti sifar secara struktur
STATUS = ('NEGATIF', 'GAGAL', 'BELUM CUKUP', 'CALON', 'TERBUKTI')
# ---------------------------------------------------------------------------------------------------------------

AN = os.path.join(BS2, 'data', 'analisis')
LIFT = os.environ.get('KS_LIFT', os.path.join(AN, 'lift.json'))
PAPAN = os.environ.get('KS_PAPAN', os.path.join(AN, 'papan.json'))
T4 = os.environ.get('KS_T4', os.path.join(BS2, 'portfolio_slot', 't4_ringkasan.csv'))
JSN = os.environ.get('KS_JSON', os.path.join(AN, 'kad_skor.json'))
SPEC_SEMUA = os.path.join(BS2, 'spec', 'SPEC_SEMUA_KAEDAH.md')


def bendera_kaedah():
    """(set REPLIKA, {id: fail spec asal}) - asal-usul kaedah untuk tab Kaedah (audit v154: 13 REPLIKA dan
    penanda `FAIL ASAL` tidak dipapar di mana-mana). REPLIKA = keluar/sasaran dinilai dengan dagangan replika
    enjin (`kod/dagangan.py`); FAIL ASAL = bahagian spec yang disatukan daripada fail spec asal tersendiri."""
    try:
        sys.path.insert(0, os.path.join(BS2, 'kod'))
        from dagangan import REPLIKA
    except Exception:
        REPLIKA = set()
    asal = {}
    if os.path.exists(SPEC_SEMUA):
        for m in re.finditer(r'<!-- FAIL ASAL: (spec/(M\d+)_[^ ]+?\.md) -->', open(SPEC_SEMUA, encoding='utf-8').read()):
            asal.setdefault(m.group(2), m.group(1))
    return set(REPLIKA), asal
MD = os.environ.get('KS_MD', os.path.join(BS2, 'laporan', 'KAD_SKOR.md'))


def n_perlu(sd, beza=G1_BEZA_MATA):
    """Posisi ditutup untuk melihat beza `beza` mata pada kuasa 80% (formula KAEDAH_TERBAIK.md §6)."""
    if sd is None or not np.isfinite(sd) or sd <= 0:
        return None
    return int(math.ceil(((Z_ALPHA + Z_KUASA) * sd / beza) ** 2))


def tarikh_sesi(dari, n):
    """Anggaran tarikh selepas n sesi dagangan (hari bekerja; cuti AS tidak ditolak)."""
    if not dari:
        return None
    n = max(int(n), 0)
    return str((pd.Timestamp(dari) + pd.offsets.BDay(n)).date())


def _ada(v):
    return v is not None and not (isinstance(v, float) and np.isnan(v))


def g1(r, perlu_hb):
    """Hari beli LANGSUNG >= maks(G1_HARI_BELI_MIN, perlu_hb) DAN >= G1_REJIM_MIN dalam setiap rejim."""
    hb = r.get('hari_beli') or 0
    on, off = r.get('hari_on') or 0, r.get('hari_off') or 0
    perlu = max(G1_HARI_BELI_MIN, perlu_hb) if perlu_hb else None
    sebab = []
    if perlu is None:
        sebab.append(f'hari beli {hb}; kuasa lift belum boleh dianggar')
    elif hb < perlu:
        sebab.append(f'hari beli {hb}/{perlu}')
    if on < G1_REJIM_MIN or off < G1_REJIM_MIN:
        sebab.append(f'rejim ON {on}/{G1_REJIM_MIN}, OFF {off}/{G1_REJIM_MIN}')
    return (not sebab), '; '.join(sebab)


def g2(r):
    """Buku harian: purata > 0 DAN had bawah 95% Newey-West > 0."""
    if not _ada(r.get('buku_harian')) or not _ada(r.get('buku_ci_bawah')):
        return False, 'buku harian belum cukup sesi'
    if r['buku_harian'] <= 0:
        return False, f"buku harian {r['buku_harian']:+.3f}%"
    if r['buku_ci_bawah'] <= 0:
        return False, f"had bawah buku {r['buku_ci_bawah']:+.3f}%"
    return True, ''


def g3(r):
    if not _ada(r.get('lift')):
        return False, 'lift belum diuji'
    if r['lift'] <= 0:
        return False, f"lift {r['lift']:+.2f}"
    if not r.get('lift_lulus'):
        return False, 'tidak lulus BH-FDR'
    return True, ''


def g4(r):
    n = int(r.get('hari0') or 0)
    if n <= G4_HARI0_MAKS:
        return True, ''
    return False, f"{n} henti hari-0 (mesti {G4_HARI0_MAKS})"


def g5(r):
    if r.get('pantau') in ('GANTUNG', 'BERSARA'):
        return False, r['pantau']
    if _ada(r.get('p_dd')) and _ada(r.get('p_dd_had')) and r['p_dd'] > r['p_dd_had']:
        return False, f"kejatuhan kohort {r['p_dd']:.1f} > had {r['p_dd_had']:.1f}"
    return True, ''


def pada_mdd(pul, mdd, had=G6_MDD_HAD):
    """Pulangan jika pendedahan diskala supaya MDD = `had` (baki tunai): pul x min(1, |had| / |MDD|)."""
    if not _ada(pul) or not _ada(mdd):
        return None
    return float(pul) * (1.0 if mdd >= 0 or abs(mdd) <= abs(had) else abs(had) / abs(mdd))


def g6(r):
    """r: baris lorong T4 L1 (kunci sesi, pul, mdd, spus, spus_mdd, jalur_nisbah_maks)."""
    s = r.get('sesi') or 0
    if s < G6_SESI:
        return False, f'sesi {s}/{G6_SESI}'
    for k in ('pul', 'mdd', 'spus', 'spus_mdd', 'jalur_nisbah_maks'):
        if not _ada(r.get(k)):
            return False, f'{k} tiada'
    if r['pul'] <= 0:
        return False, f"pulangan {r['pul']:+.2f}"
    a, b = pada_mdd(r['pul'], r['mdd']), pada_mdd(r['spus'], r['spus_mdd'])
    if a <= b:
        return False, f'pada MDD {G6_MDD_HAD:.0f}%: {a:+.2f} tidak mengalahkan SPUS {b:+.2f}'
    nis = r['pul'] / abs(r['mdd']) if r['mdd'] < 0 else float('inf')
    if nis <= r['jalur_nisbah_maks']:
        return False, f"nisbah {nis:.2f} tidak melepasi maksimum jalur rawak {r['jalur_nisbah_maks']:.2f}"
    return True, ''


def tentukan(r, perlu_hb):
    """Pulang (status, {G1..G6: (lulus, sebab)})."""
    G = {'G1': g1(r, perlu_hb), 'G2': g2(r), 'G3': g3(r), 'G4': g4(r), 'G5': g5(r),
         'G6': g6({k[3:]: v for k, v in r.items() if k.startswith('t4_')})}
    if G['G1'][0] and _ada(r.get('lift')) and r['lift'] < 0 and r.get('lift_lulus'):
        st = 'NEGATIF'
    elif not G['G5'][0]:
        st = 'GAGAL'
    elif not G['G1'][0]:
        st = 'BELUM CUKUP'
    elif not (G['G2'][0] and G['G3'][0] and G['G4'][0]):
        st = 'GAGAL'
    elif not G['G6'][0]:
        st = 'CALON'
    else:
        st = 'TERBUKTI'
    return st, G


def nw_se(x, lag=G2_NW_LAG):
    """SE purata siri x, Newey-West (Bartlett) dengan `lag`."""
    x = np.asarray(x, float)
    T = len(x)
    e = x - x.mean()
    v = float((e * e).sum() / T)
    for k in range(1, min(lag, T - 1) + 1):
        v += 2 * (1 - k / (lag + 1)) * float((e[k:] * e[:-k]).sum() / T)
    return float(np.sqrt(max(v, 0.0) / T))


def buku_harian(P, sesi, C, kos=0.1):
    """{id_kaedah: Series pulangan harian % buku berat sama}. Setiap posisi = 1 unit modal pada buka hari beli;
    ditanda pada tutup setiap sesi; keluar lorong 1 pada untung akhir (kasar). kos % setiap belah.
    Hari tanpa posisi dipegang tidak dikira (modal tidak digunakan)."""
    si = {d: i for i, d in enumerate(sesi)}
    L = len(sesi) - 1
    X = P[['id_kaedah', 'saham', 'tarikh_beli', 'harga_beli', 'tarikh_keluar', 'untung_pct']].copy()
    X['p0'] = pd.to_numeric(X.harga_beli, errors='coerce')
    X['ut'] = pd.to_numeric(X.untung_pct, errors='coerce')
    X['b'] = X.tarikh_beli.astype(str).str.replace('-', '', regex=False).map(si)
    tk = X.tarikh_keluar.fillna('').astype(str)
    X['tutup'] = tk != ''
    X['e'] = np.where(X.tutup, tk.str.replace('-', '', regex=False).map(si), L)
    X = X[X.p0.notna() & X.b.notna() & X.e.notna() & X.saham.isin(C.index) & (~X.tutup | X.ut.notna())]
    X = X[X.e >= X.b]
    if X.empty:
        return {}
    b, e = X.b.to_numpy(int), X.e.to_numpy(int)
    n = e - b + 1
    pos = np.repeat(np.arange(len(X)), n)
    awal = np.repeat(np.cumsum(n) - n, n)
    t = np.repeat(b, n) + (np.arange(n.sum()) - awal)
    ri = np.repeat(C.index.get_indexer(X.saham), n)
    v = C.to_numpy()[ri, t] / np.repeat(X.p0.to_numpy(), n)
    akhir = np.cumsum(n) - 1
    tut = X.tutup.to_numpy()
    v[akhir[tut]] = 1 + X.ut.to_numpy()[tut] / 100
    v = np.where(np.isfinite(v), v, np.nan)
    v = pd.Series(v).groupby(pos).ffill().fillna(1.0).to_numpy()   # tiada bar: guna nilai semalam
    vp = np.empty_like(v)
    vp[1:] = v[:-1]
    vp[np.r_[True, np.diff(pos) != 0]] = 1.0          # nilai sebelum hari beli = modal 1 unit
    pnl = v - vp
    pnl[np.r_[True, np.diff(pos) != 0]] -= kos / 100
    pnl[akhir[tut]] -= kos / 100 * v[akhir[tut]]
    kod, ids = pd.factorize(X.id_kaedah.to_numpy())
    key = np.repeat(kod, n) * (L + 1) + t
    num = np.bincount(key, weights=pnl, minlength=len(ids) * (L + 1)).reshape(len(ids), L + 1)
    den = np.bincount(key, weights=vp, minlength=len(ids) * (L + 1)).reshape(len(ids), L + 1)
    out = {}
    for i, mid in enumerate(ids):
        ok = den[i] > 0
        out[mid] = pd.Series(num[i][ok] / den[i][ok] * 100, index=np.asarray(sesi)[ok])
    return out


def statistik_buku(r):
    """(purata harian %, had bawah, had atas, bilangan sesi) bagi siri buku r."""
    if r is None or len(r) < 2:
        return None, None, None, int(0 if r is None else len(r))
    m = float(r.mean())
    se = nw_se(r.to_numpy())
    tc = float(stats.t.ppf(1 - G2_ALPHA / 2, len(r) - 1))
    return m, m - tc * se, m + tc * se, int(len(r))


def statistik(g):
    """Lajur setiap kaedah daripada posisi lorong 1 (DataFrame dengan pul, terbuka, tarikh_beli...)."""
    p = g.pul.to_numpy(float)
    n = len(p)
    d = dict(n=n, tutup=int((~g.terbuka).sum()), buka_pct=float(g.terbuka.mean() * 100),
             hari_beli=int(g.tarikh_beli.nunique()), jangkaan=float(p.mean()))
    tt, bk = g.pul[~g.terbuka], g.pul[g.terbuka]
    d['pul_tutup'] = float(tt.mean()) if len(tt) else None
    d['pul_buka'] = float(bk.mean()) if len(bk) else None
    # Selang keyakinan setiap-posisi DIBUANG 7 Nov 2026: posisi terbuka semua hari beli berkongsi satu tanda
    # pasaran, jadi SE ikut hari beli terlalu sempit. Ketidakpastian dibawa oleh buku harian (G2).
    d['ci_bawah'] = d['ci_atas'] = None
    m, r = p[p > 0], p[p < 0]
    d['menang'] = float((p > 0).mean() * 100)
    d['untung_purata'] = float(m.mean()) if len(m) else None
    d['rugi_purata'] = float(r.mean()) if len(r) else None
    d['payoff'] = (d['untung_purata'] / abs(d['rugi_purata'])
                   if d['untung_purata'] is not None and d['rugi_purata'] else None)
    s = np.sort(p)
    k10 = max(1, int(math.ceil(0.10 * n)))
    d['cvar10'] = float(s[:k10].mean())
    d['terburuk'] = float(s[0])
    k5 = int(math.ceil(0.05 * n))
    d['tanpa5'] = float(s[:n - k5].mean()) if n - k5 > 0 else None
    for c in ('mae_pct', 'mfe_pct'):
        v = pd.to_numeric(g.get(c), errors='coerce').dropna() if c in g else pd.Series(dtype=float)
        d[c[:3]] = float(v.median()) if len(v) else None
    h0 = (~g.terbuka) & (g.tarikh_keluar == g.tarikh_beli.astype(str)) & (g.sebab_keluar.astype(str) == 'henti')
    d['hari0'] = int(h0.sum())
    d['hari0_pct'] = float(h0.mean() * 100)
    return d


def muat_json(p):
    try:
        return json.load(open(p, encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def bulat(v, k=2):
    if isinstance(v, (bool, np.bool_)):
        return bool(v)
    if isinstance(v, (int, np.integer)):
        return int(v)
    if isinstance(v, (float, np.floating)):
        return None if np.isnan(v) else round(float(v), k)
    return v


def keluar_kod(mid):
    m = re.search(r'(X\d+)$', mid)
    return m.group(1) if m else ''


def main():
    import lift_kaedah as lk
    if not os.path.exists(os.path.join(lk.LEJAR, 'terbuka.csv')):
        print('kad_skor: lejar/terbuka.csv tiada', file=sys.stderr)
        return 0
    akhir, idx, sesi = lk.harga_akhir()
    P0 = lk.nilai(lk.posisi(), akhir, idx)
    P0['sebab_keluar'] = P0.sebab_keluar.fillna('').astype(str)
    P = P0[lk.langsung(P0)].copy()                       # penyebut: posisi LANGSUNG sahaja (pindaan 7 Nov)
    try:                                                 # data harga tercemar (standard/kuarantin.py, 7 Nov 2026)
        import kuarantin as KR
        cemar = KR.topeng_posisi(P).to_numpy()
    except Exception:
        cemar = np.zeros(len(P), bool)
    n_cemar = int(cemar.sum())
    P = P[~cemar].copy()
    sesi_h, C, _ = lk.panel_harga()
    buku = buku_harian(P, sesi_h, C)
    rj = lk.rejim_qqq()
    P['on'] = P.tarikh_isyarat.astype(str).str.replace('-', '', regex=False).map(rj)
    nm = lk.nama_kaedah()
    L = muat_json(LIFT)
    sl = lk.sesi_lejar()
    if sl and (L.get('sesi_terakhir') or '').replace('-', '') != sl:
        # Audit 7 Nov 2026: kad skor pernah membaca lift.json larian lalu tanpa amaran (continue-on-error).
        raise SystemExit(f"lift.json basi: sesi {L.get('sesi_terakhir')} lawan Lejar {sl}; jalankan lift_kaedah.py dahulu")
    lift = {r['id']: r for r in L.get('rows', [])}
    papan = {r['id']: r for r in muat_json(PAPAN).get('rows', [])}
    T = pd.read_csv(T4) if os.path.exists(T4) else pd.DataFrame(columns=['id', 'lorong'])
    t4 = {(r['id'], r['lorong']): r for r in T.to_dict('records')}

    sds = [float(g.pul.std(ddof=1)) for _, g in P.groupby('id_kaedah') if len(g) >= 2]
    sd = float(np.median(sds)) if sds else None
    perlu_hb = L.get('perlu_2mata')
    perlu_hb = max(int(perlu_hb), G1_HARI_BELI_MIN) if perlu_hb else None
    nhb = int(P.tarikh_beli.nunique())
    hb_on = int(P[P.on == True].tarikh_beli.nunique())    # noqa: E712
    hb_off = int(P[P.on == False].tarikh_beli.nunique())  # noqa: E712

    replika, spec_asal = bendera_kaedah()
    rows = []
    for mid, g in P.groupby('id_kaedah'):
        r = dict(id=mid, nama=nm.get(mid, '') or (papan.get(mid) or {}).get('nama', ''),
                 keluarga=mid[:1] if mid[:2] != 'GB' else 'GB', keluar=keluar_kod(mid),
                 mula_langsung=lk.mula_langsung(mid))
        r.update(statistik(g))
        r['hari_on'] = int(g[g.on == True].tarikh_beli.nunique())    # noqa: E712
        r['hari_off'] = int(g[g.on == False].tarikh_beli.nunique())  # noqa: E712
        bm, bb, ba, bn = statistik_buku(buku.get(mid))
        r.update(buku_harian=bm, buku_ci_bawah=bb, buku_ci_atas=ba, buku_sesi=bn)
        lr = lift.get(mid) or {}
        r.update(lift=lr.get('lift'), lift_t=lr.get('t'), lift_p=lr.get('p'), lift_bh=lr.get('bh'),
                 lift_lulus=bool(lr.get('lulus')) if lr else None, lift_n=lr.get('n'), hari_pegang=lr.get('hari'))
        pr = papan.get(mid) or {}
        r.update(pantau=pr.get('pantau'), p_dd=pr.get('p_dd'), p_dd_had=pr.get('p_dd_had'),
                 lintas_earnings=pr.get('h_lintas_earnings'), bt_hari=pr.get('hari'),
                 # Backtest | Hadapan bersebelahan (audit v154, corak LEAN): purata setiap dagangan set 431
                 bt_purata=pr.get('bt_purata'), bt_menang=pr.get('bt_menang'),
                 replika=mid in replika, spec_asal=spec_asal.get(mid),
                 semakan=sum(bool(pr.get(k)) for k in ('lulus_subset', 'lulus_wfo', 'lulus_at'))
                 if pr.get('bt_cagr') is not None else None)
        for kod, pre in (('L1', 't4_'), ('L2', 't4b_')):
            x = t4.get((mid, kod)) or {}
            keys = (('sesi', 'pul', 'mdd', 'spus', 'spus_mdd', 'lebih_spus', 'persentil', 'jalur_p95',
                     'jalur_nisbah_maks', 'nisbah', 'w10', 'r10', 'spus_r10',
                     'c80_pul', 'c80_mdd', 'c70_pul', 'c70_mdd', 'c50_pul', 'c50_mdd', 'mula')
                    if kod == 'L1' else ('sesi', 'pul', 'mdd'))
            for k in keys:
                r[pre + k] = bulat(x.get(k)) if _ada(x.get(k)) else None
        st, G = tentukan(r, perlu_hb)
        r['status'] = st
        r['gate'] = {k: bool(v[0]) for k, v in G.items()}
        r['sebab'] = {k: v[1] for k, v in G.items() if v[1]}
        rows.append({k: bulat(v, 4 if k in ('lift_p', 'lift_bh', 'buku_harian', 'buku_ci_bawah', 'buku_ci_atas')
                              else 2) for k, v in r.items()})

    kira = {s: sum(r['status'] == s for r in rows) for s in STATUS}
    akhir_sesi = sesi[-1] if sesi else None
    akhir_sesi = f'{akhir_sesi[:4]}-{akhir_sesi[4:6]}-{akhir_sesi[6:]}' if akhir_sesi and '-' not in akhir_sesi else akhir_sesi
    t4_maks = max([r['t4_sesi'] or 0 for r in rows] or [0])
    perlu_g1 = perlu_hb or G1_HARI_BELI_MIN
    tarikh_g1 = tarikh_sesi(akhir_sesi, perlu_g1 - nhb)
    tarikh_g6 = tarikh_sesi(akhir_sesi, G6_SESI - t4_maks)
    syarat_rejim = (f'dan ≥ {G1_REJIM_MIN} hari beli dalam setiap rejim (kini ON {hb_on}, OFF {hb_off}; '
                    'bergantung pasaran)')
    if kira['TERBUKTI']:
        tajuk = f"{kira['TERBUKTI']} kaedah TERBUKTI — calon wang sebenar"
    elif kira['CALON']:
        tajuk = (f"{kira['CALON']} CALON (setiap dagangan lulus), belum terbukti sebagai portfolio pada MDD "
                 f"{G6_MDD_HAD:.0f}%; G6 paling awal {tarikh_g6}")
    else:
        tajuk = (f"Tiada kaedah lulus. Kematangan paling awal ~{tarikh_g1} {syarat_rejim}; "
                 f"portfolio lawan SPUS pada MDD {G6_MDD_HAD:.0f}% ~{tarikh_g6}")
    # Susunan: status, kemudian berapa gate G1-G5 sudah lulus (paling hampir dahulu), kemudian lift.
    # Ini BUKAN pangkat: dalam BELUM CUKUP, lift ialah hingar sehingga G1 lulus.
    ord_st = {s: i for i, s in enumerate(('TERBUKTI', 'CALON', 'BELUM CUKUP', 'GAGAL', 'NEGATIF'))}
    rows.sort(key=lambda r: (ord_st[r['status']], -sum(r['gate'][k] for k in ('G1', 'G2', 'G3', 'G4', 'G5')),
                             -(r['lift'] if r['lift'] is not None else -99)))
    meta = dict(kini=str(pd.Timestamp.now(tz='UTC').date()), harga_pada=akhir_sesi, hari_beli=nhb,
                hari_on=hb_on, hari_off=hb_off, posisi=int(len(P)), posisi_isian=int(len(P0) - len(P) - n_cemar),
                posisi_tercemar=n_cemar,
                kaedah=len(rows), sd=bulat(sd), n_perlu=n_perlu(sd), hari_beli_perlu=perlu_g1,
                t4_sesi_maks=t4_maks, tarikh_g1=tarikh_g1, tarikh_g6=tarikh_g6, kira=kira, tajuk=tajuk,
                pradaftar='2026-11-06; pindaan 2026-11-07', spec='standard/SPEC_KAD_SKOR.md',
                mula_langsung=lk.MULA_LANGSUNG,
                ambang=dict(G1_HARI_BELI_MIN=G1_HARI_BELI_MIN, G1_LIFT_MATA=G1_LIFT_MATA, G1_REJIM_MIN=G1_REJIM_MIN,
                            G2_ALPHA=G2_ALPHA, G2_NW_LAG=G2_NW_LAG, G3_Q=G3_Q, G3_UFUK=lk.UFUK,
                            G6_SESI=G6_SESI, G6_MDD_HAD=G6_MDD_HAD, G4_HARI0_MAKS=G4_HARI0_MAKS))
    tulis_json(JSN, meta, rows)
    os.makedirs(os.path.dirname(MD), exist_ok=True)
    open(MD, 'w', encoding='utf-8').write(laporan(meta, rows))
    print(f'KAD_SKOR | {len(rows)} kaedah | ' + ' '.join(f'{k} {v}' for k, v in kira.items()) + f' | {tajuk}')
    return 0


KOL_GATE = ('G1', 'G2', 'G3', 'G4', 'G5', 'G6')


def tulis_json(path, meta, rows):
    """Bentuk lajur (`kol` + senarai baris) supaya dokumen db kekal jauh di bawah had 262,144 bait:
    nama medan tidak diulang 222 kali. Satu baris kaedah setiap baris fail supaya delta git kecil.
    `gate` = rentetan 6 aksara '1'/'0' bagi G1..G6; `sebab` = {gate: sebab} bagi yang gagal sahaja."""
    kol = [k for k in rows[0] if k not in ('gate', 'sebab')] + ['gate', 'sebab'] if rows else []
    out = []
    for r in rows:
        v = [r.get(k) for k in kol[:-2]]
        v.append(''.join('1' if r['gate'][g] else '0' for g in KOL_GATE))
        v.append(r['sebab'])
        out.append(json.dumps(v, ensure_ascii=False, separators=(',', ':')))
    head = json.dumps(dict(meta, kol=kol), ensure_ascii=False, separators=(',', ':'))[:-1]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(head + ',"rows":[\n' + ',\n'.join(out) + '\n]}\n')


def baca_json(path):
    """Kebalikan tulis_json: (meta, [dict baris])."""
    with open(path, encoding='utf-8') as f:
        A = json.load(f)
    kol = A.pop('kol')
    rows = []
    for v in A.pop('rows'):
        r = dict(zip(kol, v))
        r['gate'] = {g: c == '1' for g, c in zip(KOL_GATE, r['gate'])}
        rows.append(r)
    return A, rows


def laporan(M, rows):
    def f(v, fmt='{:+.2f}'):
        return '–' if v is None else fmt.format(v)
    A = ['# Kad skor keputusan (satu jawapan)', '',
         f"Dijana {M['kini']} oleh `standard/kad_skor.py` (Actions `analisis.yml`). Gate: `{M['spec']}` "
         f"(pradaftar {M['pradaftar']}). Rekod analisis sahaja: tiada order, tiada wang sebenar.", '',
         f"## {M['tajuk']}", '',
         f"Penyebut: **{M['posisi']:,} posisi LANGSUNG** Lejar Penuh lorong 1 merentas {M['kaedah']} kaedah, "
         f"{M['hari_beli']} hari beli (rejim ON {M['hari_on']}, OFF {M['hari_off']}); {M['posisi_isian']:,} posisi "
         f"isian bina semula dan {M.get('posisi_tercemar', 0):,} posisi dengan data harga dikuarantin tidak dikira (Mxx sejak isyarat {M['mula_langsung']['M']}, Nxx/GB sejak "
         f"{M['mula_langsung']['N']}). Harga pada tutup {M['harga_pada']}.", '',
         '| Status | Bilangan |', '|---|---|']
    A += [f'| {k} | {v} |' for k, v in M['kira'].items()]
    A += ['', '## Bila keputusan boleh dibuat', '',
          f"- **G1 kematangan:** ≥ {M['hari_beli_perlu']} hari beli langsung (ada {M['hari_beli']}) **dan** ≥ "
          f"{G1_REJIM_MIN} dalam rejim ON (ada {M['hari_on']}) **dan** ≥ {G1_REJIM_MIN} dalam rejim OFF "
          f"(ada {M['hari_off']}). Rejim ON = QQQ > SMA50 dan SMA10 > SMA20. Paling awal ~{M['tarikh_g1']} "
          'jika rejim ON muncul cukup lama; jika pasaran kekal OFF, G1 menunggu.',
          f"- **G6 portfolio:** {G6_SESI} sesi lorong T4 (paling lama {M['t4_sesi_maks']}); ~{M['tarikh_g6']}. "
          f"Dibanding dengan SPUS **pada MDD {G6_MDD_HAD:.0f}%** (toleransi anda), bukan pada MDD SPUS penuh.",
          '', '## 20 kaedah teratas ikut lift masuk (calon, BUKAN pangkat sehingga status berubah)', '',
          '| Kaedah | Status | Posisi / tutup | Hari beli (ON/OFF) | Jangkaan % | Buku harian % [95%] | Lift masuk | '
          'Menang % | Payoff | tanpa5 | Hari-0 | T4 sesi | T4 pada MDD -10% vs SPUS |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    top = sorted(rows, key=lambda r: -(r['lift'] if r['lift'] is not None else -99))[:20]
    for r in top:
        t4 = ('–' if r.get('t4_r10') is None else f"{r['t4_r10']:+.2f} vs {f(r.get('t4_spus_r10'))}")
        A.append(f"| `{r['id']}` {str(r['nama'])[:28]} | {r['status']} | {r['n']} / {r['tutup']} | "
                 f"{r['hari_beli']} ({r['hari_on']}/{r['hari_off']}) | {f(r['jangkaan'])} | "
                 f"{f(r['buku_harian'], '{:+.3f}')} [{f(r['buku_ci_bawah'], '{:+.3f}')}, {f(r['buku_ci_atas'], '{:+.3f}')}] | "
                 f"{f(r['lift'])} | {f(r['menang'], '{:.0f}')} | {f(r['payoff'], '{:.2f}')} | {f(r['tanpa5'])} | "
                 f"{r['hari0']} | {f(r['t4_sesi'], '{}')} | {t4} |")
    A += ['', '## Cara membaca', '',
          '- **Satu status sahaja yang bermakna untuk wang sebenar: TERBUKTI.**',
          '- **Lift masuk** = adakah kaedah memilih saham lebih baik daripada saham lain yang Lejar beli pada hari sama '
          'dan tahap turun-naik sama, diukur 10 sesi (bebas peraturan keluar). Disahkan plasebo: '
          '`laporan/PLASEBO_GATE.md`.',
          '- **Buku harian** = pulangan harian purata jika setiap isyarat kaedah itu diberi modal sama dan keluar ikut '
          'peraturannya sendiri. Selang 95% Newey-West mengambil kira bahawa semua posisi bergerak bersama pasaran.',
          '- Menang % sentiasa dibaca bersama payoff: `X10` menang 94.1% dengan jangkaan negatif.',
          '- `tanpa5` = jangkaan selepas membuang 5% posisi terbaik. Negatif bermaksud kelebihan hidup dalam ekor kanan.',
          '- Jangan ubah ambang gate selepas melihat data. Ia dikunci oleh ujian unit.', '']
    return '\n'.join(A) + '\n'


if __name__ == '__main__':
    sys.exit(main())
