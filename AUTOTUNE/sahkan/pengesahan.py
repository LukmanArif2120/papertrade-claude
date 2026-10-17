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


K_PARAM = ('param', 'params', 'P', 'parameter', 'terbaik.param', 'pilihan.param')
K_NCUBA = ('n_cubaan', 'n_trials', 'cubaan')
K_RALAT = ('ralat', 'error', 'errors')
K_PULANG = ('pulangan_ujian', 'ujian.pulangan', 'pulangan', 'returns', 'test_returns')
K_MUJI = ('metrik_ujian', 'ujian.metrik', 'test', 'metrik.ujian')
KUMP_AB = ('AB', 'A+B', 'gabung', 'semua')


def _kump(blok, g):
    """Ambil sub-blok kumpulan g ('A', 'B', 'AB') daripada dict {A:..., B:..., AB:...}."""
    if not isinstance(blok, dict): return None
    if g == 'AB':
        for k in KUMP_AB:
            if k in blok: return blok[k]
        return None
    return blok.get(g)


def pulangan(d, g):
    return U.siri(_kump(ambil(d, *K_PULANG), g))


def metrik_ujian(d, g):
    return _kump(ambil(d, *K_MUJI), g) or {}


def n_cubaan(d):
    x = ambil(d, *K_NCUBA, lalai=0)
    if isinstance(x, (list, tuple)): return len(x)
    try: return int(x)
    except Exception: return 0


def param(d):
    p = ambil(d, *K_PARAM)
    return p if isinstance(p, dict) else None


def rosak(d, k):
    """True jika kajian k tidak boleh digunakan (tiada parameter pilihan, atau tiada pulangan ujian untuk k ≤ 12)."""
    if not isinstance(d, dict) or param(d) is None: return True
    if k <= U.K_AKHIR:
        bl = ambil(d, *K_PULANG)
        if not isinstance(bl, dict) or not bl: return True
    return False


# ---------- statistik dagangan agregat ----------
def _stat(m):
    n = ambil(m, 'n', 'n_dagangan', 'dagangan', 'trades', 'n_trades', lalai=0) or 0
    h = ambil(m, 'hari', 'purata_hari', 'avg_days', 'days', 'hari_pegang')
    w = ambil(m, 'menang', 'kadar_menang', 'win', 'win_rate', 'wr')
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
def nilai(kid, kaj, spy, N_jumlah, belum_modul=False, nama=''):
    rek = dict(kaedah=kid, nama=nama, catatan='')
    hilang = [k for k in range(U.K_AKHIR + 1) if k not in kaj or rosak(kaj[k], k)]
    catat = []
    if belum_modul: catat.append('modul gagal kesetaraan')
    if hilang: catat.append('kajian tiada/rosak: ' + ','.join(f'k{k:02d}' for k in hilang))
    if U.K_SEMASA not in kaj or rosak(kaj[U.K_SEMASA], U.K_SEMASA): catat.append('SEMASA tiada')
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
    # tempoh kunci (k12, A+B)
    d12 = sah.get(U.K_AKHIR, {})
    rK = pulangan(d12, 'AB') if d12 else pd.Series(dtype=float)
    if d12 and not len(rK): rK = pulangan(d12, 'A')            # tala.py mungkin simpan A+B di bawah kunci lain
    m['cagr_kunci'] = U.cagr(rK); m['mdd_kunci'] = U.mdd(rK); m['spy_kunci'] = spy_cagr(spy, rK.index)
    m['kunci_mula'] = rK.index[0].strftime('%Y-%m-%d') if len(rK) else ''
    m['kunci_akhir'] = rK.index[-1].strftime('%Y-%m-%d') if len(rK) else ''
    # ujian bersih (k00): PARAM asal 2013–2018 A+B
    b = ambil(kaj.get(0, {}), 'bersih')
    if isinstance(b, dict):
        rb = U.siri(ambil(b, 'pulangan', 'returns', 'r'))
        if len(rb):
            m['cagr_bersih'] = U.cagr(rb); m['spy_bersih'] = spy_cagr(spy, rb.index)
        else:
            m['cagr_bersih'] = ambil(b, 'cagr', 'metrik.cagr', lalai=float('nan'))
            m['spy_bersih'] = spy_julat(spy, BERSIH_MULA, BERSIH_AKHIR)
    else:
        m['cagr_bersih'] = float('nan'); m['spy_bersih'] = float('nan')
    # DSR, dataran, PBO
    m['dsr'] = U.dsr(rA, N_jumlah) if len(rA) else float('nan')
    m['dataran'] = _f(ambil(d12, 'dataran', 'nisbah_dataran', 'plateau', 'kepekaan.dataran', 'kepekaan.nisbah'))
    m['pbo'] = _f(ambil(d12, 'pbo', 'PBO', 'pbo.nilai'))
    belum = belum_modul or bool(hilang)
    rek.update(m)
    rek['label'] = U.label(m, belum=belum)
    rek['catatan'] = '; '.join(catat)
    return rek, rA


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
    rek = []
    for k in ids:
        r, _ = nilai(k, semua[k], spy, N, belum_modul=U.belum_ditala_modul(k, kaedah_dir),
                     nama=U.nama_modul(k, kaedah_dir))
        rek.append(r)
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
        n_kaedah=len(df), n_cubaan_jumlah=N, kiraan_label=kira,
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
