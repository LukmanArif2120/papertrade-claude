# Kriteria MENANG A03 (SPEC_A03 §6, pindaan 18 Okt 2026) dan pengiraan semula atas 40 kaedah-lorong A02 yang ditala.
#   Syarat (setiap satu dikira berasingan; HAMPIR = tepat satu gagal; TIDAK = dua atau lebih gagal):
#     menang_a, menang_b >= 55% (dagangan portfolio dipegang, OOS bersih 2013–2018); cagr_a, cagr_b > 0; pf_a, pf_b >= 1.3;
#     mdd_oos (terburuk A/B) >= −35%; menang_peng >= 55% dan cagr_peng > 0 (pengesahan 2019 – hujung, A+B);
#     dagangan OOS min(n_a, n_b) >= 100; imbasan pandang ke hadapan BERSIH.
#   python3 AUTOTUNE/sahkan/menang_a03.py --a02 [--cache AUTOTUNE/.cache_a02] [--proses 4]
#     → hasil_a03/menang_a02.csv: trades A02 dijana semula (parameter setiap kajian, sistem A02: 8 slot × 12.5%, tanpa F/M)
#       hanya untuk statistik dagangan; CAGR/MDD/lebihan/label A02 dibaca daripada hasil_a02/parameter_sedia.csv (rekod).
import argparse, json, math, os, sys
import numpy as np, pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
AT = os.path.dirname(SINI)
for p in (SINI, os.path.join(AT, 'tala'), os.path.join(AT, 'teras')):
    if p not in sys.path: sys.path.insert(0, p)
import tala as T1           # noqa: E402
import tala_a02 as T2       # noqa: E402
import tala_a03 as T3       # noqa: E402
import sahkan_a02 as S2     # noqa: E402

LABEL = ['MENANG', 'HAMPIR', 'TIDAK']
MENANG_MIN, PF_MIN, MDD_MIN, N_MIN = 0.55, 1.3, -0.35, 100
A02 = os.path.join(AT, 'hasil_a02')
CSV_A02 = os.path.join(T3.HASIL, 'menang_a02.csv')
STAT = ('menang', 'kalah', 'purata_untung', 'purata_rugi', 'jangkaan', 'pf')
ASAS = ('n_menang', 'n_kalah', 'jumlah_untung', 'jumlah_rugi')


def _ok(x, f):
    try:
        x = float(x)
    except (TypeError, ValueError): return False
    return not math.isnan(x) and f(x)


def syarat(m):
    """{nama syarat: lulus?} bagi dict m (kunci *_a, *_b, *_peng, mdd_oos, n_a, n_b, imbasan)."""
    return {'menang A ≥ 55%': _ok(m.get('menang_a'), lambda x: x >= MENANG_MIN),
            'menang B ≥ 55%': _ok(m.get('menang_b'), lambda x: x >= MENANG_MIN),
            'CAGR A > 0': _ok(m.get('cagr_a'), lambda x: x > 0), 'CAGR B > 0': _ok(m.get('cagr_b'), lambda x: x > 0),
            'PF A ≥ 1.3': _ok(m.get('pf_a'), lambda x: x >= PF_MIN), 'PF B ≥ 1.3': _ok(m.get('pf_b'), lambda x: x >= PF_MIN),
            'MDD OOS ≥ −35%': _ok(m.get('mdd_oos'), lambda x: x >= MDD_MIN),
            'menang pengesahan ≥ 55%': _ok(m.get('menang_peng'), lambda x: x >= MENANG_MIN),
            'CAGR pengesahan > 0': _ok(m.get('cagr_peng'), lambda x: x > 0),
            'dagangan OOS ≥ 100': _ok(min(m.get('n_a') or 0, m.get('n_b') or 0), lambda x: x >= N_MIN),
            'imbasan bersih': m.get('imbasan') == 'BERSIH'}


def label(m):
    """(label, senarai syarat gagal)."""
    g = [k for k, v in syarat(m).items() if not v]
    return ('MENANG' if not g else 'HAMPIR' if len(g) == 1 else 'TIDAK'), g


def tambah_stat(m, akhiran, asas):
    """m[f'{stat}_{akhiran}'] daripada jumlah asas (n_menang, n_kalah, jumlah_untung, jumlah_rugi)."""
    st = T3.terbitan(*[asas.get(k, 0) or 0 for k in ASAS])
    for k in STAT: m[f'{k}_{akhiran}'] = st[k]
    return m


def agregat(kaj, g, ks):
    """Jumlah asas statistik dagangan merentas kajian ks (ujian_<g> dalam kNN.json A03)."""
    out = dict.fromkeys(ASAS, 0)
    for k in ks:
        H = kaj.get(k) or {}
        u = H.get(f'ujian_{g}') if H.get('status') == 'SIAP' else None
        if not u: continue
        for a in ASAS: out[a] += u.get(a) or 0
    return out


def agregat_trades(Ts):
    s = [T3.statistik(T) for T in Ts if T is not None]
    return {a: sum(x[a] for x in s) for a in ASAS}


def kira_a02(data_dir, proses=4, a02=A02, keluar=CSV_A02):
    """Statistik dagangan dan label MENANG bagi kaedah-lorong A02 yang ditala (dagangan dipegang dijana semula)."""
    P = pd.read_csv(os.path.join(a02, 'parameter_sedia.csv'))
    hd = {}
    try: hd = json.load(open(os.path.join(a02, 'pandang_hadapan.json')))
    except Exception: pass
    tugas = P.tugas.tolist(); tala = os.path.join(a02, 'tala')
    kaj = {t: S2.baca_kajian(t, tala) for t in tugas}
    G = S2.Gabung(kaj, tugas, data_dir, proses)
    ok = set(G.sedia())
    R = []
    for r in P.itertuples():
        m = dict(tugas=r.tugas, kaedah=r.kaedah, lorong=r.lorong, label_a02=r.label, lebihan_a=r.lebihan_a,
                 lebihan_b=r.lebihan_b, lebihan_peng=r.lebihan_peng, cagr_a=r.cagr_a, cagr_b=r.cagr_b, cagr_peng=r.cagr_peng,
                 mdd_oos=r.mdd_oos, mdd_peng=r.mdd_peng, imbasan=(hd.get(r.tugas) or {}).get('status', r.imbasan),
                 menang_a_a02=r.menang_a, n_a_a02=r.n_a)
        if r.tugas in ok:
            for g, ks, ak in (('A', T2.K_WFO, 'a'), ('B', T2.K_WFO, 'b'), ('AB', [T2.K_AKHIR], 'peng')):
                Ts = [G.ps[k].lengkung(G.T[(r.tugas, k, g)], pegang=True)[1] for k in ks]
                tambah_stat(m, ak, agregat_trades(Ts))
                m[f'n_{ak}'] = sum(len(T) for T in Ts)
        else:
            m['catatan'] = f'gagal jana: {G.gagal.get(r.tugas, "")}'[:200]
        m['label'], gagal = label(m); m['gagal'] = '; '.join(gagal)
        R.append(m)
    D = pd.DataFrame(R)
    os.makedirs(os.path.dirname(keluar), exist_ok=True)
    D.to_csv(keluar, index=False, float_format='%.6g')
    return D


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--a02', action='store_true'); a.add_argument('--cache', default=os.environ.get('AUTOTUNE_CACHE', T3.CACHE))
    a.add_argument('--proses', type=int, default=4); a.add_argument('--keluar', default=CSV_A02)
    x = a.parse_args()
    if x.a02:
        D = kira_a02(str(T2.ambil_data(x.cache)), x.proses, keluar=x.keluar)
        print(f"A02 dikira semula: {len(D)}; label {D.label.value_counts().to_dict()}; "
              f"beza kadar menang A (jana semula − rekod) maks {np.nanmax(np.abs(D.menang_a - D.menang_a_a02)):.4f}")


if __name__ == '__main__':
    main()
