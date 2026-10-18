# Imbasan pandang ke hadapan A03 (SPEC_A03 §4): logik semak_hadapan.imbas (tidak berubah) atas parameter AKHIR (k06) dan
# SEMASA (k07) setiap sistem ditala, 12 tarikh potong 2012–2026 (imbas_a02.POTONG), data A02 + EPS A03. Isyarat yang
# diimbas = sig kaedah ∧ F ∧ M; dalam larian dipotong pada c, F dikira daripada EPS yang SUDAH DILAPORKAN pada c
# (tarikh < c, atau tarikh = c dan masa 'sebelum'), jadi sebarang kebocoran laporan selepas c ke hari <= c dikesan.
# Semakan tambahan F (lajur 'F'): F(data dan EPS dipotong pada c) mesti sama dengan F(penuh) bagi semua hari <= c,
# dan peraturan `tersedia` (sebelum buka → hari laporan; selainnya → hari dagangan berikutnya) disemak atas semua baris.
#   Pekerja: python3 imbas_a03.py --shard 0 --n-shard 5 --proses 2 [--ticker 150] [--keluar DIR]
#   Tulis  : python3 imbas_a03.py --tulis DIR1 [DIR2 ...]  → hasil_a03/PANDANG_HADAPAN.md, pandang_hadapan.json
import argparse, glob, json, os, sys, time, traceback, types
from multiprocessing import get_context
import numpy as np, pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
AT = os.path.dirname(SINI)
for p in (SINI, os.path.join(AT, 'kaedah'), os.path.join(AT, 'tala'), os.path.join(AT, 'teras')):
    if p not in sys.path: sys.path.insert(0, p)
import semak_hadapan as SH   # noqa: E402
import imbas_a02 as IA       # noqa: E402
import tala as T1            # noqa: E402
import tala_a02 as T2        # noqa: E402
import tala_a03 as T3        # noqa: E402

HASIL = T3.HASIL
POTONG = IA.POTONG
_D = {}


def eps_pada(eps, c):
    """Baris EPS yang sudah dilaporkan pada hari c: tarikh < c, atau tarikh = c dan masa 'sebelum' (sebelum buka)."""
    if eps is None: return None
    c = pd.Timestamp(c).normalize(); t = pd.to_datetime(eps['tarikh']).dt.normalize()
    return eps[(t < c) | ((t == c) & (eps['masa'] == 'sebelum'))]


def semak_tersedia(eps):
    """Bilangan baris yang melanggar peraturan titik masa `tersedia` (lebih awal daripada dibenarkan)."""
    if eps is None or not len(eps): return dict(baris=0, langgar=0)
    d = eps[eps['tersedia'].notna()]
    t = pd.to_datetime(d['tarikh']).dt.normalize(); s = pd.to_datetime(d['tersedia']).dt.normalize()
    bad = (s < t) | ((d['masa'] != 'sebelum') & (s <= t))
    return dict(baris=int(len(d)), langgar=int(bad.sum()), contoh=d.loc[bad, 'ticker'].head(5).tolist())


def bungkus(m, P, eps):
    """Modul berparameter: sedia(f, idx) = sedia kaedah, kemudian sig &= F (EPS yang dilaporkan pada hari terakhir f) & M."""
    def sedia(f, i):
        m.sedia(f, i, dict(P))
        if not f: return
        c = max(g.index.max() for g in f.values())
        F = T3.lajur_f(f, eps_pada(eps, c)); M = T3.topeng_m(f, i)
        for t, g in f.items():
            if 'sig' not in g: continue
            g['sig'] = g['sig'].fillna(False).astype(bool) & F[t].reindex(g.index).fillna(False).values & M[t].values
    return types.SimpleNamespace(sedia=sedia, SILANG=getattr(m, 'SILANG', False), PERLU_BAR=getattr(m, 'PERLU_BAR', 0),
                                 WARM=getattr(m, 'WARM', 0))


def semak_f(fr, eps, potong_=POTONG):
    """{'langgar': {...}} jika F(dipotong pada c) ≠ F(penuh) bagi mana-mana hari <= c."""
    if eps is None: return {}
    penuh = T3.lajur_f(fr, eps); out = {}
    for c in potong_:
        C = pd.Timestamp(c)
        fc = {t: g[g.index <= C] for t, g in fr.items()}; fc = {t: g for t, g in fc.items() if len(g)}
        F = T3.lajur_f(fc, eps_pada(eps, C))
        for t, s in F.items():
            b = s.values != penuh[t].reindex(s.index).values
            if b.any():
                e = out.setdefault('F', {'ticker': set(), 'hari': set(), 'sifat': {'F bergantung EPS dilaporkan selepas c'}})
                e['ticker'].add(t); e['hari'].update(str(x.date()) for x in s.index[b])
    return out


def semak(nama):
    t0 = time.time(); mid, lorong = T2.pecah_tugas(nama)
    R = dict(tugas=nama, kaedah=mid, lorong=lorong, set={}, potong=list(POTONG), n_ticker=len(_D['fr']))
    try:
        m = T1.muat_kaedah(mid)
        P = IA.param_tugas(nama, _D.get('tala'))
        if not P: R['ralat'] = 'tiada parameter AKHIR/SEMASA (k06/k07 tidak SIAP)'
        for lbl, Pp in P.items():
            r = SH.imbas(bungkus(m, Pp, _D['eps']), _D['fr'], _D['idx'], POTONG)
            R['set'][lbl] = dict(langgar=SH._jsonkan(r['langgar']), dibenar=SH._jsonkan(r['dibenar']))
        if P:
            fl = semak_f(_D['fr'], _D['eps'])
            R['set']['F'] = dict(langgar=SH._jsonkan(fl), dibenar={})
            ts = semak_tersedia(_D['eps'])
            R['tersedia'] = ts
            if ts['langgar']:
                R['set']['F']['langgar']['tersedia'] = dict(ticker=ts['langgar'], hari=0, sifat=['tersedia lebih awal'],
                                                            contoh=ts['contoh'], contoh_hari=[])
    except Exception as e:
        R['ralat'] = f'{type(e).__name__}: {e}'[:300]; R['jejak'] = traceback.format_exc()[-800:]
    R['masa'] = round(time.time() - t0, 1)
    return R


def _init(dir_, n, tala_dir, eps):
    import warnings; warnings.filterwarnings('ignore')
    _D['fr'], _D['idx'] = IA.muat_sampel(dir_, n); _D['tala'] = tala_dir
    _D['eps'] = eps[eps.ticker.isin(set(_D['fr']))] if eps is not None else None


def pekerja(x):
    ids = IA.tugas_pilihan(x.pilihan)
    ids = [t for j, t in enumerate(ids) if j % x.n_shard == x.shard]
    os.makedirs(x.keluar, exist_ok=True)
    dir_ = str(T2.ambil_data(x.cache))
    eps = T3.muat_eps(T3.ambil_fundamental(x.fund))
    print(f'imbas A03 shard {x.shard}: {len(ids)} tugas', flush=True)
    with get_context('fork').Pool(x.proses, initializer=_init, initargs=(dir_, x.ticker, x.tala, eps), maxtasksperchild=4) as p:
        for R in p.imap_unordered(semak, ids):
            json.dump(R, open(os.path.join(x.keluar, R['tugas'] + '.json'), 'w'), ensure_ascii=False)
            print(R['tugas'], IA.status(R), R.get('ralat', '')[:80], R['masa'], flush=True)


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
        out[t] = dict(status=IA.status(r), set=sorted(r.get('set', {})), catatan=r.get('ralat', ''),
                      lajur=sorted({k for s in r.get('set', {}).values() for k in s['langgar']}),
                      butiran={lbl: s['langgar'] for lbl, s in r.get('set', {}).items() if s['langgar']},
                      tersedia=r.get('tersedia'))
    os.makedirs(keluar, exist_ok=True)
    json.dump(out, open(os.path.join(keluar, 'pandang_hadapan.json'), 'w'), indent=1, ensure_ascii=False)
    n_ph = sum(v['status'] == 'PANDANG HADAPAN' for v in out.values())
    n_t = next((r.get('n_ticker') for r in R.values()), None)
    ts = next((r.get('tersedia') for r in R.values() if r.get('tersedia')), None) or {}
    L = ['# Imbasan pandang ke hadapan A03', '',
         f'Dijana oleh `AUTOTUNE/sahkan/imbas_a03.py` ({time.strftime("%Y-%m-%d %H:%M")} UTC). Logik `semak_hadapan.imbas` '
         f'atas parameter AKHIR (k06) dan SEMASA (k07) setiap sistem ditala; isyarat = sig kaedah ∧ F ∧ M, dengan F dalam '
         f'larian dipotong dikira daripada EPS yang sudah dilaporkan pada tarikh potong. Sampel {n_t} ticker universe A02 '
         f'(susunan md5, sejarah sejak 2010), {len(POTONG)} tarikh potong: {", ".join(POTONG)}.', '',
         f'Semakan F (set `F`): F(data dan EPS dipotong pada c) = F(penuh) bagi semua hari <= c; peraturan `tersedia` atas '
         f'{ts.get("baris", 0)} baris EPS sampel: {ts.get("langgar", 0)} melanggar.', '',
         f'Sistem diimbas: {len(out)}. Bersih: {len(out) - n_ph}. PANDANG HADAPAN (melanggar atau ralat): {n_ph}.', '',
         '| Sistem | Status | Set parameter | Lajur dilanggar | Catatan |', '|---|---|---|---|---|']
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
    a.add_argument('--proses', type=int, default=2); a.add_argument('--ticker', type=int, default=150)
    a.add_argument('--cache', default=os.environ.get('AUTOTUNE_CACHE', T3.CACHE)); a.add_argument('--fund', default=T3.CACHE_F)
    a.add_argument('--pilihan', default=os.path.join(HASIL, 'pilihan.json'))
    a.add_argument('--tala', default=T3.KELUAR)
    a.add_argument('--keluar', default=os.path.join(HASIL, '_imbas'))
    a.add_argument('--tulis', nargs='*')
    x = a.parse_args(argv)
    if x.tulis is not None:
        out = tulis(x.tulis or [x.keluar])
        print(f"imbasan A03: {len(out)} sistem; PANDANG HADAPAN {sum(v['status'] != 'BERSIH' for v in out.values())}")
        return
    pekerja(x)


if __name__ == '__main__':
    main()
