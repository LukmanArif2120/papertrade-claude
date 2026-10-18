# Imbasan pandang ke hadapan A02 (SPEC_A02 §4): logik AUTOTUNE/kaedah/semak_hadapan.imbas (peraturan Pindaan 18 Okt
# 2026, tidak berubah) atas parameter AKHIR (k06) dan SEMASA (k07) setiap kaedah-lorong terpilih, data A02, 12 tarikh
# potong 2012–2026. Sampel ticker: N ticker universe A02 (susunan md5 tetap) dengan sejarah sejak 2010.
#   Pekerja: python3 imbas_a02.py --shard 0 --n-shard 10 --proses 4 [--ticker 150] [--keluar DIR]  → DIR/<ID>_<lorong>.json
#   Tulis  : python3 imbas_a02.py --tulis DIR1 [DIR2 ...]  → hasil_a02/PANDANG_HADAPAN.md, hasil_a02/pandang_hadapan.json
import argparse, glob, hashlib, json, os, sys, time, traceback, types
from multiprocessing import get_context
import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
AT = os.path.dirname(SINI)
for p in (os.path.join(AT, 'kaedah'), os.path.join(AT, 'tala'), os.path.join(AT, 'teras')):
    if p not in sys.path: sys.path.insert(0, p)
import semak_hadapan as SH   # noqa: E402
import tala as T1            # noqa: E402
import tala_a02 as T2        # noqa: E402

HASIL = T2.HASIL
POTONG = ('2012-06-29', '2013-09-30', '2014-12-31', '2016-03-31', '2017-06-30', '2018-09-28', '2019-12-31',
          '2021-03-31', '2022-06-30', '2023-09-29', '2024-12-31', '2026-03-31')
MULA = '2010-01-01'
_D = {}


def tugas_pilihan(pilihan=None):
    J = json.load(open(pilihan or os.path.join(HASIL, 'pilihan.json')))
    return list(J['tugas'])


def bungkus(m, P):
    """Modul berparameter → antara muka sedia(fr, idx) yang dipakai semak_hadapan.imbas."""
    return types.SimpleNamespace(sedia=lambda f, i: m.sedia(f, i, dict(P)), SILANG=getattr(m, 'SILANG', False),
                                 PERLU_BAR=getattr(m, 'PERLU_BAR', 0), WARM=getattr(m, 'WARM', 0))


def sampel(dir_, n):
    """n ticker universe (susunan md5) yang ada dalam universe sebelum 2011 dan masih ada pada 2026."""
    u = pd.read_parquet(os.path.join(dir_, 'universe.parquet'), columns=['bulan', 'ticker'])
    awal = set(u.loc[u.bulan <= '2010-12', 'ticker']); akhir = set(u.loc[u.bulan >= '2026-01', 'ticker'])
    c = sorted(awal & akhir, key=lambda t: hashlib.md5(t.encode()).hexdigest())
    return c[:n]


def muat_sampel(dir_, n):
    import data
    tk = set(sampel(dir_, n))
    fr, idx, _ = data.muat(MULA, '2030-12-31', 'AB', dir=dir_)
    return {t: g for t, g in fr.items() if t in tk}, idx


def param_tugas(nama, tala_dir=None):
    """{'AKHIR': P, 'SEMASA': P} (params_penuh) daripada k06/k07; set yang sama digabung ('AKHIR=SEMASA')."""
    d = os.path.join(tala_dir or T2.KELUAR, nama)
    out = {}
    for k, lbl in ((T2.K_AKHIR, 'AKHIR'), (T2.K_SEMASA, 'SEMASA')):
        try: H = json.load(open(os.path.join(d, f'k{k:02d}.json')))
        except Exception: continue
        if H.get('status') == 'SIAP' and H.get('params_penuh') is not None: out[lbl] = H['params_penuh']
    if 'AKHIR' in out and 'SEMASA' in out and out['AKHIR'] == out['SEMASA']:
        out = {'AKHIR=SEMASA': out['AKHIR']}
    return out


def semak(nama):
    t0 = time.time(); mid, lorong = T2.pecah_tugas(nama)
    R = dict(tugas=nama, kaedah=mid, lorong=lorong, set={}, potong=list(POTONG), n_ticker=len(_D['fr']))
    try:
        m = T1.muat_kaedah(mid)
        P = param_tugas(nama, _D.get('tala'))
        if not P: R['ralat'] = 'tiada parameter AKHIR/SEMASA (k06/k07 tidak SIAP)'
        for lbl, Pp in P.items():
            r = SH.imbas(bungkus(m, Pp), _D['fr'], _D['idx'], POTONG)
            R['set'][lbl] = dict(langgar=SH._jsonkan(r['langgar']), dibenar=SH._jsonkan(r['dibenar']))
    except Exception as e:
        R['ralat'] = f'{type(e).__name__}: {e}'[:300]; R['jejak'] = traceback.format_exc()[-800:]
    R['masa'] = round(time.time() - t0, 1)
    return R


def _init(dir_, n, tala_dir):
    import warnings; warnings.filterwarnings('ignore')
    _D['fr'], _D['idx'] = muat_sampel(dir_, n); _D['tala'] = tala_dir


def status(R):
    if R.get('ralat') and not R.get('set'): return 'PANDANG HADAPAN'
    if R.get('ralat'): return 'PANDANG HADAPAN'
    return 'PANDANG HADAPAN' if any(s['langgar'] for s in R['set'].values()) else 'BERSIH'


def pekerja(x):
    ids = tugas_pilihan(x.pilihan)
    ids = [t for j, t in enumerate(ids) if j % x.n_shard == x.shard]
    os.makedirs(x.keluar, exist_ok=True)
    dir_ = str(T2.ambil_data(x.cache))
    print(f'imbas shard {x.shard}: {len(ids)} tugas', flush=True)
    with get_context('fork').Pool(x.proses, initializer=_init, initargs=(dir_, x.ticker, x.tala), maxtasksperchild=4) as p:
        for R in p.imap_unordered(semak, ids):
            json.dump(R, open(os.path.join(x.keluar, R['tugas'] + '.json'), 'w'), ensure_ascii=False)
            print(R['tugas'], status(R), R.get('ralat', '')[:80], R['masa'], flush=True)


def tulis(dirs, keluar=HASIL):
    R = {}
    for d in dirs:
        for f in glob.glob(os.path.join(d, '**', 'M*.json'), recursive=True):
            try: J = json.load(open(f))
            except Exception: continue
            if isinstance(J, dict) and J.get('tugas'): R[J['tugas']] = J
    kunci = lambda t: (int(T2.pecah_tugas(t)[0][1:]) if T2.pecah_tugas(t)[0][1:].isdigit() else 0, t)
    out = {}
    for t in sorted(R, key=kunci):
        r = R[t]
        out[t] = dict(status=status(r), set=sorted(r.get('set', {})), catatan=r.get('ralat', ''),
                      lajur=sorted({k for s in r.get('set', {}).values() for k in s['langgar']}),
                      butiran={lbl: s['langgar'] for lbl, s in r.get('set', {}).items() if s['langgar']})
    os.makedirs(keluar, exist_ok=True)
    json.dump(out, open(os.path.join(keluar, 'pandang_hadapan.json'), 'w'), indent=1, ensure_ascii=False)
    n_ph = sum(v['status'] == 'PANDANG HADAPAN' for v in out.values())
    n_t = next((r.get('n_ticker') for r in R.values()), None)
    L = ['# Imbasan pandang ke hadapan A02', '',
         f'Dijana oleh `AUTOTUNE/sahkan/imbas_a02.py` ({time.strftime("%Y-%m-%d %H:%M")} UTC). Logik `semak_hadapan.imbas` '
         f'(peraturan Pindaan 18 Okt 2026) atas parameter AKHIR (k06) dan SEMASA (k07) setiap kaedah-lorong terpilih; data '
         f'Release `autotune-data-a02`, sampel {n_t} ticker universe (susunan md5, sejarah sejak 2010), {len(POTONG)} tarikh '
         f'potong: {", ".join(POTONG)}.', '',
         f'Kaedah-lorong diimbas: {len(out)}. Bersih: {len(out) - n_ph}. PANDANG HADAPAN (melanggar atau ralat): {n_ph}.', '',
         '| Kaedah-lorong | Status | Set parameter | Lajur dilanggar | Catatan |', '|---|---|---|---|---|']
    for t, v in out.items():
        L.append(f"| {t} | {v['status']} | {', '.join(v['set'])} | {', '.join(v['lajur']) or '—'} | {v['catatan'][:80]} |")
    dib = sorted({f"{k}" for r in R.values() for s in r.get('set', {}).values() for k in s['dibenar']})
    L += ['', f"Kebergantungan hari c yang dibenarkan (buka c+1 sahaja / kewujudan bar c+1) dijumpai pada lajur: "
          f"{', '.join(dib) or 'tiada'}. Imbasan bersifat sampel (ticker dan tarikh potong terhad)."]
    open(os.path.join(keluar, 'PANDANG_HADAPAN.md'), 'w').write('\n'.join(L) + '\n')
    return out


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument('--shard', type=int, default=0); a.add_argument('--n-shard', type=int, default=1)
    a.add_argument('--proses', type=int, default=4); a.add_argument('--ticker', type=int, default=150)
    a.add_argument('--cache', default=os.environ.get('AUTOTUNE_CACHE', T2.CACHE))
    a.add_argument('--pilihan', default=os.path.join(HASIL, 'pilihan.json'))
    a.add_argument('--tala', default=T2.KELUAR)
    a.add_argument('--keluar', default=os.path.join(HASIL, '_imbas'))
    a.add_argument('--tulis', nargs='*')
    x = a.parse_args(argv)
    if x.tulis is not None:
        out = tulis(x.tulis or [x.keluar])
        print(f"imbasan: {len(out)} kaedah-lorong; PANDANG HADAPAN {sum(v['status'] != 'BERSIH' for v in out.values())}")
        return
    pekerja(x)


if __name__ == '__main__':
    main()
