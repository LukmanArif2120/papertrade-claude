# F6 Pengesahan (SPEC §5): OOS-A/OOS-B daripada tetingkap 0–11, tempoh kunci (k12), ujian bersih (k00),
# DSR (N = jumlah percubaan semua kaedah), dataran dan PBO (k12), label.
# Output: AUTOTUNE/hasil/parameter_sedia.csv, AUTOTUNE/hasil/ringkasan.json.
#   python3 AUTOTUNE/sahkan/pengesahan.py [--tala DIR] [--keluar DIR]
import argparse, json, math, os, sys
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umum as U

BERSIH_MULA, BERSIH_AKHIR = '2013-01-01', '2018-12-31'
OOS_MULA, OOS_AKHIR = '2013-01-01', '2024-09-30'
KUNCI_MULA = '2024-10-01'


# ---------- pembaca medan JSON kajian (nama medan ikut AUTOTUNE/tala/tala.py; alias untuk toleransi) ----------
def ambil(d, *nama, lalai=None):
    """Nilai pertama yang wujud antara nama (boleh bertitik, cth. 'ujian.A')."""
    if not isinstance(d, dict): return lalai
    for n in nama:
        x = d
        for k in n.split('.'):
            if isinstance(x, dict) and k in x: x = x[k]
            else: x = None; break
        if x is not None: return x
    return lalai


# Skema AUTOTUNE/tala/tala.py (kNN.json): status 'SIAP'|'RALAT', ralat [..], belum_ditala, n_trials,
# latih [L0, L1], ujian [U0, U1]|None, params (TALA sahaja), params_penuh, latih_A, ujian_A/ujian_B(/ujian_AB k12)
# {cagr, mdd, n, win, avg, days, thn_min, tahunan}, harian_ujian {tarikh: [...], A: [...], B: [...](, AB: [...])},
# k00: bersih_AB, harian_bersih_AB {tarikh, r}; k12: dataran {nisbah, ...}, pbo {pbo, ...}.
def pulangan(d, g):
    """Pulangan harian ujian kumpulan g ('A', 'B', 'AB') daripada harian_ujian."""
    h = d.get('harian_ujian') if isinstance(d, dict) else None
    if not isinstance(h, dict) or g not in h or 'tarikh' not in h: return pd.Series(dtype=float)
    if len(h['tarikh']) != len(h[g]): raise ValueError(f'harian_ujian {g}: panjang tarikh tidak sama')
    return U.siri(dict(tarikh=h['tarikh'], r=h[g]))


def metrik_ujian(d, g):
    return (d.get(f'ujian_{g}') if isinstance(d, dict) else None) or {}


def n_cubaan(d):
    try: return int(d.get('n_trials') or 0)
    except Exception: return 0


def param(d):
    p = d.get('params') if isinstance(d, dict) else None
    return p if isinstance(p, dict) else None


def param_penuh(d):
    p = d.get('params_penuh') if isinstance(d, dict) else None
    return p if isinstance(p, dict) else param(d)


def rosak(d, k):
    """True jika kajian k tidak boleh digunakan: status bukan SIAP, tiada params, atau tiada pulangan ujian
    (A dan B bagi 0–11; AB bagi 12)."""
    if not isinstance(d, dict) or d.get('status') != 'SIAP' or param(d) is None: return True
    perlu = ('A', 'B') if k < U.K_AKHIR else ('AB',) if k == U.K_AKHIR else ()
    h = d.get('harian_ujian') or {}
    return any(g not in h for g in perlu)


def belum_json(kaj):
    return any(bool(d.get('belum_ditala')) for d in kaj.values() if isinstance(d, dict))


# ---------- statistik dagangan agregat ----------
def _stat(m):
    n = m.get('n') or 0; h = m.get('days'); w = m.get('win')
    return float(n), (None if h is None else float(h)), (None if w is None else float(w))


def stat_gabung(senarai_m):
    """Gabung n, purata hari, kadar menang beberapa tetingkap (berpemberat n)."""
    N = 0.0; sh = 0.0; sw = 0.0; nh = 0.0; nw = 0.0
    for m in senarai_m:
        n, h, w = _stat(m)
        N += n
        if h is not None and n > 0 and np.isfinite(h): sh += n * h; nh += n
        if w is not None and n > 0 and np.isfinite(w): sw += n * w; nw += n
    return int(N), (sh / nh if nh else float('nan')), (sw / nw if nw else float('nan'))


def oos(kaj, g):
    """Siri OOS (tetingkap 0–11 bersambung) kumpulan g."""
    return U.sambung([pulangan(kaj[k], g) for k in U.K_WFO if k in kaj])


# ---------- SPY ----------
def muat_spy(data_dir=None):
    """Harga tutup SPY daripada idx.parquet (aset Release autotune-data, via teras/data.ambil)."""
    if data_dir is None:
        sys.path.insert(0, U.AT)
        from teras import data as D
        data_dir = D.ambil()
    return _spy_daripada(pd.read_parquet(os.path.join(str(data_dir), 'idx.parquet')))


def _spy_daripada(x):
    if isinstance(x, pd.Series): return x.sort_index()
    if isinstance(x, dict): x = x['SPY']
    if isinstance(x, pd.DataFrame):
        if 'ticker' in x.columns:
            x = x[x.ticker == 'SPY']
            return pd.Series(x.close.values.astype(float), index=pd.to_datetime(x.date)).sort_index()
        if 'close' in x.columns: return x.close.astype(float).sort_index()
        if 'SPY' in x.columns: return x.SPY.astype(float).sort_index()
    raise ValueError('format idx tidak dikenali')


def spy_cagr(spy, tarikh):
    return U.cagr(U.spy_pulangan(spy, tarikh)) if len(tarikh) else float('nan')


def spy_julat(spy, mula, akhir):
    t = spy.index[(spy.index >= pd.Timestamp(mula)) & (spy.index <= pd.Timestamp(akhir))]
    return spy_cagr(spy, t)


# ---------- penilaian satu kaedah ----------
def nilai(kid, kaj, spy, belum_modul=False, nama=''):
    """Rekod metrik satu kaedah (tanpa DSR, yang memerlukan semua kaedah) dan siri OOS-A."""
    rek = dict(kaedah=kid, nama=nama, catatan='')
    hilang = [k for k in range(U.K_AKHIR + 1) if k not in kaj or rosak(kaj[k], k)]
    belum_j = belum_json(kaj)
    catat = []
    if belum_modul or belum_j: catat.append('modul gagal kesetaraan / tiada salinan berparameter')
    if hilang: catat.append('kajian tiada/rosak: ' + ','.join(f'k{k:02d}' for k in hilang))
    if U.K_SEMASA not in kaj or rosak(kaj[U.K_SEMASA], U.K_SEMASA): catat.append('SEMASA tiada')
    n_had = [k for k, d in kaj.items() if any('had masa' in str(x) for x in (d.get('ralat') or []))]
    if n_had: catat.append('had masa: ' + ','.join(f'k{k:02d}' for k in sorted(n_had)))
    rek['n_cubaan'] = int(sum(n_cubaan(d) for d in kaj.values()))
    rek['param_semasa'] = json.dumps(param(kaj.get(U.K_SEMASA, {})) or {}, sort_keys=True)
    rek['param_akhir'] = json.dumps(param(kaj.get(U.K_AKHIR, {})) or {}, sort_keys=True)
    sah = {k: d for k, d in kaj.items() if not rosak(d, k)}
    rA, rB = oos(sah, 'A'), oos(sah, 'B')
    m = {}
    for g, r in (('a', rA), ('b', rB)):
        m[f'cagr_{g}'] = U.cagr(r); m[f'mdd_{g}'] = U.mdd(r)
        n, h, w = stat_gabung([metrik_ujian(sah[k], g.upper()) for k in U.K_WFO if k in sah])
        m[f'n_{g}'] = n; m[f'hari_{g}'] = h; m[f'menang_{g}'] = w
        m[f'spy_{g}'] = spy_cagr(spy, r.index)
    m['oos_mula'] = rA.index[0].strftime('%Y-%m-%d') if len(rA) else ''
    m['oos_akhir'] = rA.index[-1].strftime('%Y-%m-%d') if len(rA) else ''
    # tempoh kunci (k12, parameter AKHIR, A+B)
    d12 = sah.get(U.K_AKHIR, {})
    rK = pulangan(d12, 'AB')
    m['cagr_kunci'] = U.cagr(rK); m['mdd_kunci'] = U.mdd(rK); m['spy_kunci'] = spy_cagr(spy, rK.index)
    m['kunci_mula'] = rK.index[0].strftime('%Y-%m-%d') if len(rK) else ''
    m['kunci_akhir'] = rK.index[-1].strftime('%Y-%m-%d') if len(rK) else ''
    # ujian bersih (k00): PARAM asal 2013–2018 A+B
    hb = (kaj.get(0) or {}).get('harian_bersih_AB')
    rb = U.siri(hb) if isinstance(hb, dict) else pd.Series(dtype=float)
    m['cagr_bersih'] = U.cagr(rb); m['spy_bersih'] = spy_cagr(spy, rb.index)
    # dataran, PBO (k12)
    m['dataran'] = _f((d12.get('dataran') or {}).get('nisbah'))
    m['pbo'] = _f((d12.get('pbo') or {}).get('pbo'))
    m['dsr'] = float('nan')
    rek.update(m)
    rek['_belum'] = bool(belum_modul or belum_j or hilang)
    rek['catatan'] = '; '.join(catat)
    return rek, rA


def dsr_semua(siri_a, N):
    """DSR setiap kaedah: SR harian OOS-A, SR0 = jangkaan maksimum nasib dengan V = varians SR antara kaedah
    dan N = jumlah percubaan semua kaedah (formula teras/objektif.py = WFO/kod/wfo_laporan.py)."""
    O = _objektif()
    S = {k: O.sharpe(r) for k, r in siri_a.items() if len(r)}
    srs = [v[0] for v in S.values() if not math.isnan(v[0])]
    if len(srs) < 2 or N < 2: return {k: float('nan') for k in siri_a}, float('nan')
    s0 = O.sr0(srs, N)
    out = {}
    for k in siri_a:
        sr, sk, ku, n = S.get(k, (float('nan'),) * 3 + (0,))
        out[k] = float(O.dsr(sr, sk, ku, n, s0)) if not math.isnan(sr) else float('nan')
    return out, s0


def _objektif():
    try:
        sys.path.insert(0, os.path.join(U.AT, 'teras'))
        import objektif
        if all(hasattr(objektif, f) for f in ('sharpe', 'sr0', 'dsr')): return objektif
    except ImportError:
        pass
    return U.ObjektifGanti


def _f(x):
    try: return float(x)
    except Exception: return float('nan')


LAJUR = ['kaedah', 'nama', 'label', 'cagr_a', 'mdd_a', 'n_a', 'hari_a', 'menang_a', 'spy_a',
         'cagr_b', 'mdd_b', 'n_b', 'hari_b', 'menang_b', 'spy_b',
         'cagr_kunci', 'mdd_kunci', 'spy_kunci', 'kunci_mula', 'kunci_akhir',
         'cagr_bersih', 'spy_bersih', 'dsr', 'dataran', 'pbo', 'n_cubaan',
         'param_semasa', 'param_akhir', 'oos_mula', 'oos_akhir', 'catatan']


def jalan(tala=None, keluar=None, spy=None, kaedah=None, kaedah_dir=None):
    tala = tala or U.TALA; keluar = keluar or U.HASIL
    ids = kaedah or sorted({os.path.basename(p) for p in _subdir(tala)} | set(U.senarai_kaedah()),
                           key=lambda s: (len(s), s))
    semua = {k: U.baca_kajian(k, os.path.join(tala, k)) for k in ids}
    N = int(sum(n_cubaan(d) for kaj in semua.values() for d in kaj.values()))
    if spy is None: spy = muat_spy()
    rek = []; rA = {}
    for k in ids:
        r, rA[k] = nilai(k, semua[k], spy, belum_modul=U.belum_ditala_modul(k, kaedah_dir),
                         nama=U.nama_modul(k, kaedah_dir))
        rek.append(r)
    D, s0 = dsr_semua(rA, N)
    for r in rek:
        r['dsr'] = D.get(r['kaedah'], float('nan'))
        r['label'] = U.label(r, belum=r.pop('_belum'))
    df = pd.DataFrame(rek, columns=LAJUR)
    os.makedirs(keluar, exist_ok=True)
    df.to_csv(os.path.join(keluar, 'parameter_sedia.csv'), index=False, float_format='%.6g')
    kira = {l: int((df.label == l).sum()) for l in U.LABEL}
    sah = df[df.label != 'BELUM DITALA'].sort_values('cagr_a', ascending=False)
    top = [U.bersih({c: r[c] for c in ('kaedah', 'nama', 'label', 'cagr_a', 'mdd_a', 'cagr_b', 'mdd_b',
                                          'cagr_kunci', 'spy_kunci', 'spy_a', 'dsr', 'pbo')}, 4)
           for _, r in sah.head(20).iterrows()]
    t_oos = df.oos_mula[df.oos_mula != ''], df.oos_akhir[df.oos_akhir != '']
    t_k = df.kunci_mula[df.kunci_mula != ''], df.kunci_akhir[df.kunci_akhir != '']
    ring = dict(
        dijana=pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%dT%H:%MZ'),
        n_kaedah=len(df), n_cubaan_jumlah=N, sr0_harian=s0, kiraan_label=kira,
        tempoh=dict(oos=[t_oos[0].min() if len(t_oos[0]) else None, t_oos[1].max() if len(t_oos[1]) else None],
                    kunci=[t_k[0].min() if len(t_k[0]) else None, t_k[1].max() if len(t_k[1]) else None],
                    bersih=[BERSIH_MULA, BERSIH_AKHIR],
                    data_akhir=spy.index.max().strftime('%Y-%m-%d') if len(spy) else None),
        spy=U.bersih(dict(oos=spy_julat(spy, OOS_MULA, OOS_AKHIR),
                          bersih=spy_julat(spy, BERSIH_MULA, BERSIH_AKHIR)), 4),
        top20_cagr_a=top,
        belum_ditala=df.kaedah[df.label == 'BELUM DITALA'].tolist())
    U.tulis_json(os.path.join(keluar, 'ringkasan.json'), U.bersih(ring))
    return df, ring


def _subdir(p):
    return [os.path.join(p, x) for x in os.listdir(p) if os.path.isdir(os.path.join(p, x))] if os.path.isdir(p) else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tala', default=None); ap.add_argument('--keluar', default=None)
    a = ap.parse_args()
    df, ring = jalan(a.tala, a.keluar)
    print(f"pengesahan: {len(df)} kaedah, N cubaan = {ring['n_cubaan_jumlah']}")
    print('label: ' + ', '.join(f'{k} {v}' for k, v in ring['kiraan_label'].items()))
    for t in ring['top20_cagr_a'][:5]:
        print(f"  {t['kaedah']:6s} {t['label']:12s} A {t['cagr_a']} B {t['cagr_b']} MDD {t['mdd_a']}")


if __name__ == '__main__':
    main()
