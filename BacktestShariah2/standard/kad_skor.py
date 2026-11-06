"""Kad skor keputusan: SATU jawapan kepada "kaedah mana untuk wang sebenar", dengan gate G1-G6 yang
DIPRADAFTAR 6 Nov 2026 (spec `standard/SPEC_KAD_SKOR.md`; keputusan pengguna "Kunci apa adanya").

Mengapa ia wujud (`reports/Audit dashboard v154 pilih kaedah.md`): dashboard v154 memberi tujuh
jawapan "kaedah terbaik" yang tidak bersetuju, kerana setiap panel memakai penyebut berbeza (akaun C
ditutup sahaja, backtest set 431, Lejar matang, skor gabungan...). Kad ini memakai SATU penyebut -
setiap posisi Lejar Penuh lorong 1 (keluar kaedah), yang terbuka ditanda-ke-pasaran, kos 0.2% setiap
pusingan - jadi kesemua 222 kaedah (Mxx + Nxx) dinilai pada paksi sama dan penapisan keluar
(`laporan/KAEDAH_TERBAIK.md` §3a) tidak boleh memilih sampel.

Gate (ambang di bawah ialah PRADAFTAR; `ujian/test_kad_skor.py::TestKunci` gagal jika ia diubah):
  G1 kematangan : hari beli >= G1_HARI_BELI_MIN DAN (posisi ditutup >= n_perlu ATAU hari beli >= hari
                  beli perlu untuk lift G1_LIFT_MATA). n_perlu = ((1.96+0.84) x SD / G1_BEZA_MATA)^2 dan
                  SD dikira SEMULA setiap larian (median SD dalam-kaedah), jadi ambang tidak boleh hanyut.
  G2 jangkaan   : jangkaan semua posisi > 0 DAN had bawah selang keyakinan (1-G2_ALPHA) > 0, SE
                  berkelompok ikut hari beli.
  G3 lift       : lift padan hari beli x baldi hari pegang > 0 DAN lulus BH-FDR q <= G3_Q pada penyebut
                  SEMUA kaedah diuji (`laporan/LIFT_KAEDAH.md`).
  G4 hari-0     : bilangan henti pada hari beli <= G4_HARI0_MAKS (= 0). PINDAAN 6 Nov 2026: versi asal
                  ("0, ATAU jangkaan termasuk hari-0 > 0") tidak pernah mengubah status kerana G2 sudah
                  mewajibkan jangkaan > 0; laporan audit menetapkan "hari-0 = 0 secara struktur".
  G5 pantau     : status pantau Papan Penganalisis bukan GANTUNG/BERSARA, dan kejatuhan kohort
                  p_dd <= p_dd_had jika had wujud.
  G6 portfolio  : lorong T4 L1 kaedah itu (`portfolio_t4.py`) ada >= G6_SESI sesi, pulangan > SPUS
                  tingkap sama, pulangan > persentil G6_PERSENTIL jalur rawak, MDD >= G6_MDD %.
Status (satu kosa kata, keutamaan atas ke bawah):
  NEGATIF     - lift negatif yang bertahan BH-FDR (bukti merugikan, matang atau tidak)
  GAGAL       - G5 gagal, atau G1 lulus tetapi G2/G3/G4 gagal
  BELUM CUKUP - G1 belum lulus
  CALON       - G1-G5 lulus; G6 (portfolio lawan SPUS) belum
  TERBUKTI    - G1-G6 lulus = calon wang sebenar
Lajur maklumat (BUKAN gate, pemilik yang menimbang): menang %, payoff, tanpa5, CVaR, MAE/MFE.
Kadar menang BUKAN maklumat bersendirian (`REVERSE/NXX_KELUAR.md`: X10 menang 94.1% dengan jangkaan
negatif), jadi ia sentiasa dipapar bersebelahan payoff.

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

# ---------- PRADAFTAR 6 Nov 2026 - jangan ubah tanpa keputusan pengguna + pradaftar bertarikh baharu ----------
G1_HARI_BELI_MIN = 20       # PANTAU_G Papan Penganalisis; lantai label pengguna 14 Okt
G1_BEZA_MATA = 1.0          # beza jangkaan yang mesti boleh dilihat (KAEDAH_TERBAIK.md §6)
G1_LIFT_MATA = 2.0          # lift yang mesti boleh dilihat merentas semua kaedah (LIFT_KAEDAH.md)
Z_ALPHA, Z_KUASA = 1.96, 0.84
G2_ALPHA = 0.05             # selang keyakinan 95% dua-hujung; had bawah mesti > 0
G3_Q = 0.05                 # BH-FDR, sama dengan lift_kaedah.Q_FDR
G6_SESI = 126               # ~6 bulan; BANDING_SPUS.md: tanda pertama kelebihan 20 mata/tahun
G6_PERSENTIL = 95           # pulangan lorong > persentil ini dalam jalur rawak tingkap sama
G6_MDD = -26.82             # MDD SPUS 2020-2025 (REVERSE/PENANDA_ARAS_SYARIAH.md, SISTEM.md)
G4_HARI0_MAKS = 0           # PINDAAN 6 Nov 2026 (keputusan pengguna): henti hari-0 mesti sifar secara struktur
STATUS = ('NEGATIF', 'GAGAL', 'BELUM CUKUP', 'CALON', 'TERBUKTI')
# ---------------------------------------------------------------------------------------------------------------

AN = os.path.join(BS2, 'data', 'analisis')
LIFT = os.environ.get('KS_LIFT', os.path.join(AN, 'lift.json'))
PAPAN = os.environ.get('KS_PAPAN', os.path.join(AN, 'papan.json'))
T4 = os.environ.get('KS_T4', os.path.join(BS2, 'portfolio_slot', 't4_ringkasan.csv'))
JSN = os.environ.get('KS_JSON', os.path.join(AN, 'kad_skor.json'))
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


def g1(r, sd_n, perlu_hb):
    hb, tt = r.get('hari_beli') or 0, r.get('tutup') or 0
    if hb < G1_HARI_BELI_MIN:
        return False, f'hari beli {hb}/{G1_HARI_BELI_MIN}'
    lalu_n = sd_n is not None and tt >= sd_n
    lalu_h = perlu_hb is not None and hb >= perlu_hb
    if lalu_n or lalu_h:
        return True, ''
    return False, f'ditutup {tt}/{sd_n} dan hari beli {hb}/{perlu_hb}'


def g2(r):
    if not _ada(r.get('jangkaan')) or not _ada(r.get('ci_bawah')):
        return False, 'tiada selang keyakinan'
    if r['jangkaan'] <= 0:
        return False, f"jangkaan {r['jangkaan']:+.2f}"
    if r['ci_bawah'] <= 0:
        return False, f"had bawah {r['ci_bawah']:+.2f}"
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


def g6(r):
    """r: baris lorong T4 L1 (kunci sesi, pul, spus, jalur_p95, mdd)."""
    s = r.get('sesi') or 0
    if s < G6_SESI:
        return False, f'sesi {s}/{G6_SESI}'
    for k in ('pul', 'spus', 'jalur_p95', 'mdd'):
        if not _ada(r.get(k)):
            return False, f'{k} tiada'
    if r['pul'] <= r['spus']:
        return False, 'tidak mengalahkan SPUS'
    if r['pul'] <= r['jalur_p95']:
        return False, f'dalam jalur rawak (bawah p{G6_PERSENTIL})'
    if r['mdd'] < G6_MDD:
        return False, f"MDD {r['mdd']:.1f} < {G6_MDD}"
    return True, ''


def tentukan(r, sd_n, perlu_hb):
    """Pulang (status, {G1..G6: (lulus, sebab)})."""
    G = {'G1': g1(r, sd_n, perlu_hb), 'G2': g2(r), 'G3': g3(r), 'G4': g4(r), 'G5': g5(r),
         'G6': g6({k[3:]: v for k, v in r.items() if k.startswith('t4_')})}
    if _ada(r.get('lift')) and r['lift'] < 0 and r.get('lift_lulus'):
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


def statistik(g):
    """Lajur setiap kaedah daripada posisi lorong 1 (DataFrame dengan pul, terbuka, tarikh_beli...)."""
    p = g.pul.to_numpy(float)
    n = len(p)
    d = dict(n=n, tutup=int((~g.terbuka).sum()), buka_pct=float(g.terbuka.mean() * 100),
             hari_beli=int(g.tarikh_beli.nunique()), jangkaan=float(p.mean()))
    tt, bk = g.pul[~g.terbuka], g.pul[g.terbuka]
    d['pul_tutup'] = float(tt.mean()) if len(tt) else None
    d['pul_buka'] = float(bk.mean()) if len(bk) else None
    kl = g.groupby('tarikh_beli').pul.mean()
    if len(kl) >= 2 and kl.std(ddof=1) > 0:
        se = float(kl.std(ddof=1)) / np.sqrt(len(kl))
        tc = float(stats.t.ppf(1 - G2_ALPHA / 2, len(kl) - 1))
        d['ci_bawah'], d['ci_atas'] = d['jangkaan'] - tc * se, d['jangkaan'] + tc * se
    else:
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
    P = lk.nilai(lk.posisi(), akhir, idx)
    P['sebab_keluar'] = P.sebab_keluar.fillna('').astype(str)
    nm = lk.nama_kaedah()
    L = muat_json(LIFT)
    lift = {r['id']: r for r in L.get('rows', [])}
    papan = {r['id']: r for r in muat_json(PAPAN).get('rows', [])}
    T = pd.read_csv(T4) if os.path.exists(T4) else pd.DataFrame(columns=['id', 'lorong'])
    t4 = {(r['id'], r['lorong']): r for r in T.to_dict('records')}

    sds = [float(g.pul.std(ddof=1)) for _, g in P.groupby('id_kaedah') if len(g) >= 2]
    sd = float(np.median(sds)) if sds else None
    sd_n = n_perlu(sd)
    perlu_hb = L.get('perlu_2mata')
    perlu_hb = max(int(perlu_hb), G1_HARI_BELI_MIN) if perlu_hb else None
    nhb = int(P.tarikh_beli.nunique())

    rows = []
    for mid, g in P.groupby('id_kaedah'):
        r = dict(id=mid, nama=nm.get(mid, '') or (papan.get(mid) or {}).get('nama', ''),
                 keluarga=mid[:1] if mid[:2] != 'GB' else 'GB', keluar=keluar_kod(mid))
        r.update(statistik(g))
        lr = lift.get(mid) or {}
        r.update(lift=lr.get('lift'), lift_t=lr.get('t'), lift_p=lr.get('p'), lift_bh=lr.get('bh'),
                 lift_lulus=bool(lr.get('lulus')) if lr else None, hari_pegang=lr.get('hari'))
        pr = papan.get(mid) or {}
        r.update(pantau=pr.get('pantau'), p_dd=pr.get('p_dd'), p_dd_had=pr.get('p_dd_had'),
                 lintas_earnings=pr.get('h_lintas_earnings'), bt_hari=pr.get('hari'),
                 semakan=sum(bool(pr.get(k)) for k in ('lulus_subset', 'lulus_wfo', 'lulus_at'))
                 if pr.get('bt_cagr') is not None else None)
        for kod, pre in (('L1', 't4_'), ('L2', 't4b_')):
            x = t4.get((mid, kod)) or {}
            keys = (('sesi', 'pul', 'mdd', 'spus', 'spus_mdd', 'lebih_spus', 'persentil', 'jalur_p95',
                     'c80_pul', 'c80_mdd', 'c70_pul', 'c70_mdd', 'c50_pul', 'c50_mdd', 'mula')
                    if kod == 'L1' else ('sesi', 'pul', 'mdd'))
            for k in keys:
                r[pre + k] = bulat(x.get(k)) if _ada(x.get(k)) else None
        st, G = tentukan(r, sd_n, perlu_hb)
        r['status'] = st
        r['gate'] = {k: bool(v[0]) for k, v in G.items()}
        r['sebab'] = {k: v[1] for k, v in G.items() if v[1]}
        rows.append({k: bulat(v, 4 if k in ('lift_p', 'lift_bh') else 2) for k, v in r.items()})

    kira = {s: sum(r['status'] == s for r in rows) for s in STATUS}
    akhir_sesi = sesi[-1] if sesi else None
    akhir_sesi = f'{akhir_sesi[:4]}-{akhir_sesi[4:6]}-{akhir_sesi[6:]}' if akhir_sesi and '-' not in akhir_sesi else akhir_sesi
    t4_maks = max([r['t4_sesi'] or 0 for r in rows] or [0])
    tarikh_g1 = tarikh_sesi(akhir_sesi, (perlu_hb or G1_HARI_BELI_MIN) - nhb) if perlu_hb else None
    tarikh_g6 = tarikh_sesi(akhir_sesi, G6_SESI - t4_maks)
    if kira['TERBUKTI']:
        tajuk = f"{kira['TERBUKTI']} kaedah TERBUKTI — calon wang sebenar"
    elif kira['CALON']:
        tajuk = (f"{kira['CALON']} CALON (setiap dagangan lulus), belum terbukti sebagai portfolio; "
                 f"G6 paling awal {tarikh_g6}")
    else:
        tajuk = (f"Tiada kaedah lulus. Keputusan paling awal: lift {G1_LIFT_MATA:.0f} mata ~{tarikh_g1}, "
                 f"portfolio lawan SPUS ~{tarikh_g6}")
    # Susunan: status, kemudian berapa gate G1-G5 sudah lulus (paling hampir dahulu), kemudian lift.
    # Ini BUKAN pangkat: dalam BELUM CUKUP, lift ialah hingar sehingga G1 lulus.
    ord_st = {s: i for i, s in enumerate(('TERBUKTI', 'CALON', 'BELUM CUKUP', 'GAGAL', 'NEGATIF'))}
    rows.sort(key=lambda r: (ord_st[r['status']], -sum(r['gate'][k] for k in ('G1', 'G2', 'G3', 'G4', 'G5')),
                             -(r['lift'] if r['lift'] is not None else -99)))
    meta = dict(kini=str(pd.Timestamp.now(tz='UTC').date()), harga_pada=akhir_sesi, hari_beli=nhb,
                posisi=int(len(P)), kaedah=len(rows), sd=bulat(sd), n_perlu=sd_n, hari_beli_perlu=perlu_hb,
                t4_sesi_maks=t4_maks, tarikh_g1=tarikh_g1, tarikh_g6=tarikh_g6, kira=kira, tajuk=tajuk,
                pradaftar='2026-11-06', spec='standard/SPEC_KAD_SKOR.md',
                ambang=dict(G1_HARI_BELI_MIN=G1_HARI_BELI_MIN, G1_BEZA_MATA=G1_BEZA_MATA,
                            G1_LIFT_MATA=G1_LIFT_MATA, G2_ALPHA=G2_ALPHA, G3_Q=G3_Q, G6_SESI=G6_SESI,
                            G6_PERSENTIL=G6_PERSENTIL, G6_MDD=G6_MDD))
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
         f"Dijana {M['kini']} oleh `standard/kad_skor.py` (Actions `analisis.yml`). Gate dipradaftar "
         f"{M['pradaftar']} dalam `{M['spec']}`. Rekod analisis sahaja: tiada order, tiada wang sebenar.", '',
         f"## {M['tajuk']}", '',
         f"Penyebut: {M['posisi']:,} posisi Lejar Penuh lorong 1 merentas {M['kaedah']} kaedah, {M['hari_beli']} hari beli, "
         f"yang terbuka ditanda-ke-pasaran pada tutup {M['harga_pada']}.", '',
         '| Status | Bilangan |', '|---|---|']
    A += [f'| {k} | {v} |' for k, v in M['kira'].items()]
    A += ['', '## Kematangan (G1)', '',
          f"SD setiap posisi (median dalam-kaedah) {f(M['sd'], '{:.2f}')} mata → **{f(M['n_perlu'], '{:,}')}** posisi ditutup "
          f"untuk beza {G1_BEZA_MATA:.0f} mata; ATAU **{f(M['hari_beli_perlu'], '{}')}** hari beli untuk lift "
          f"{G1_LIFT_MATA:.0f} mata (ada {M['hari_beli']}); DAN hari beli ≥ {G1_HARI_BELI_MIN}. "
          f"Lorong T4 paling lama: {M['t4_sesi_maks']} / {G6_SESI} sesi.", '',
          '## 20 kaedah teratas ikut lift (calon, BUKAN pangkat sehingga status berubah)', '',
          '| Kaedah | Status | n / tutup | Hari beli | Jangkaan % [95%] | Lift | Menang % | Payoff | tanpa5 | Hari-0 | T4 sesi | T4 vs SPUS |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
    top = sorted([r for r in rows if r['lift'] is not None], key=lambda r: -r['lift'])[:20]
    for r in top:
        A.append(f"| `{r['id']}` {str(r['nama'])[:28]} | {r['status']} | {r['n']} / {r['tutup']} | {r['hari_beli']} | "
                 f"{f(r['jangkaan'])} [{f(r['ci_bawah'])}, {f(r['ci_atas'])}] | {f(r['lift'])} | {f(r['menang'], '{:.0f}')} | "
                 f"{f(r['payoff'], '{:.2f}')} | {f(r['tanpa5'])} | {r['hari0']} | {f(r['t4_sesi'], '{}')} | {f(r['t4_lebih_spus'])} |")
    A += ['', '## Cara membaca', '',
          '- **Satu status sahaja yang bermakna untuk wang sebenar: TERBUKTI.** CALON bermaksud setiap dagangan lulus tetapi '
          'portfolio belum terbukti mengalahkan SPUS; `REVERSE/KEPUTUSAN_AKHIR.md` mengukur bahawa kohort setiap dagangan '
          'yang lulus pernah gagal 0/36 sebagai portfolio.',
          '- Menang % sentiasa dibaca bersama payoff: `X10` menang 94.1% dengan jangkaan negatif; `X3` menang 30.2% dengan '
          'jangkaan +2.595% (`REVERSE/KOMBINASI.md`).',
          '- `tanpa5` = jangkaan selepas membuang 5% posisi terbaik. Negatif bermaksud kelebihan hidup dalam ekor kanan '
          '(`REVERSE/KOLAM_EKOR.md`) dan memerlukan banyak posisi untuk ditangkap.',
          '- Jangan ubah ambang gate selepas melihat data. Ia dikunci oleh ujian unit.', '']
    return '\n'.join(A) + '\n'


if __name__ == '__main__':
    sys.exit(main())
