# Penalaan semula berkala (suku tahunan): data terkini → WFO 3 benih → CADANGAN (tidak diguna tanpa kelulusan).
#
#   1) python3 WFO/kod/tala_semula.py data <folder stor harga>      # harga_A.csv + harga_idx.csv (aset dashboard)
#        → WFO/data/mentah_terkini/ (data_mentah + bar baharu; diabaikan git)
#   2) python3 WFO/kod/tala_semula.py jalan <label> <benih>          # WFO semua kaedah, boleh disambung; 3 kali: benih 42, 1042, 2042
#        → WFO/data/tala/<label>/b<benih>/hasil/
#   3) python3 WFO/kod/tala_semula.py cadang <label>                 # → WFO/cadangan/<label>.md + .json
#   4) python3 WFO/kod/tala_semula.py guna <label> M119 M137 ...     # HANYA selepas pengguna lulus; kaedah K145+ (M115–M161)
#
# Pengawal cadangan (semua mesti benar): gabungan suku terkini sama dalam >= 2/3 benih; CAGR luar sampel WFO (median benih)
# > CAGR luar sampel tetapan semasa; MDD luar sampel WFO >= −35%; >= 30 dagangan luar sampel.
import os, sys, json, glob, subprocess
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.join(ROOT, '..', '..')
MENTAH = os.path.join(REPO, 'data_mentah'); TERKINI = os.path.join(ROOT, '..', 'data', 'mentah_terkini')
TALA = os.path.join(ROOT, '..', 'data', 'tala'); CADANGAN = os.path.join(ROOT, '..', 'cadangan')
KAEDAH_PROD = os.path.join(REPO, 'BacktestShariah2', 'kod', 'kaedah')
BENIH = [42, 1042, 2042]


# ---------- 1) data ----------
def data(stor):
    """Sambung data_mentah dengan bar stor harga (tarikh > bar terakhir). Ticker yang harga bar bertindih
    berbeza > 0.5% (pelarasan split/dividen berbeza) TIDAK disambung dan dilaporkan."""
    os.makedirs(TERKINI, exist_ok=True)
    A = pd.concat([pd.read_csv(os.path.join(stor, f)) for f in ('harga_A.csv', 'harga_B.csv') if os.path.exists(os.path.join(stor, f))])
    I = pd.read_csv(os.path.join(stor, 'harga_idx.csv'))
    langkau = []; tambah = 0
    def sambung(lama, baru):
        nonlocal tambah
        out = []
        for t, g in lama.groupby('ticker', sort=False):
            b = baru[baru.ticker == t]
            z = g.date.max(); bt = b[b.date == z]
            if len(b) and len(bt) and abs(float(bt.close.iloc[0]) / float(g[g.date == z].close.iloc[0]) - 1) > 0.005:
                langkau.append(t); out.append(g); continue
            n = b[b.date > z].copy()
            if len(n):
                n['turnover'] = (n.close * n.volume).round(0); tambah += len(n)
            out.append(pd.concat([g, n[g.columns]]) if len(n) else g)
        return pd.concat(out)
    for i in range(1, 5):
        d = pd.read_csv(os.path.join(MENTAH, f'dataset_S{i}.csv'))
        sambung(d, A).to_csv(os.path.join(TERKINI, f'dataset_S{i}.csv'), index=False)
    ix = pd.read_csv(os.path.join(MENTAH, 'index_benchmark.csv'))
    sambung(ix, I).to_csv(os.path.join(TERKINI, 'index_benchmark.csv'), index=False)
    print(f'{tambah} bar baharu ditambah; {len(langkau)} ticker tidak disambung (harga bertindih berbeza): {" ".join(langkau[:30])}')


# ---------- 2) jalan ----------
def jalan(label, benih, proses=4):
    out = os.path.join(TALA, label, f'b{benih}')
    env = dict(os.environ, WFO_DATA=TERKINI if os.path.exists(os.path.join(TERKINI, 'dataset_S1.csv')) else MENTAH,
               WFO_KELUAR=out, WFO_BENIH=str(benih), WFO_PERCUBAAN=os.environ.get('WFO_PERCUBAAN', '150'))
    subprocess.run([sys.executable, os.path.join(ROOT, 'wfo.py'), 'kelompok', str(proses)], env=env, check=False)
    st = json.loads(subprocess.run([sys.executable, os.path.join(ROOT, 'wfo.py'), 'senarai'], env=env, capture_output=True,
                                   text=True).stdout.splitlines()[0])
    print(label, benih, {v: list(st.values()).count(v) for v in set(st.values())})


# ---------- 3) cadang ----------
def semasa(mid):
    """Tetapan semasa dalam Papertrade C: (henti, keluar, tmax). Kaedah asal = ASAL/ASAL/TMAX modul."""
    p = os.path.join(KAEDAH_PROD, mid + '.py'); src = open(p).read() if os.path.exists(p) else ''
    g = lambda k: (src.split(f"{k} = '")[1].split("'")[0] if f"{k} = '" in src else None)
    tm = src.split('\nTMAX = ')[1].split('\n')[0].strip() if '\nTMAX = ' in src else 'None'
    return (g('HENTI_KOD') or 'ASAL', g('KELUAR_KOD') or 'ASAL', 0 if tm == 'None' else int(tm.split()[0]))


def cadang(label):
    dirs = {b: os.path.join(TALA, label, f'b{b}', 'hasil') for b in BENIH}
    mids = sorted({os.path.basename(f)[:-5] for d in dirs.values() for f in glob.glob(os.path.join(d, 'M*.json'))},
                  key=lambda x: int(x[1:]))
    rows = []
    for mid in mids:
        H = {}; P = {}
        for b, d in dirs.items():
            try:
                h = json.load(open(os.path.join(d, mid + '.json')))
                if h.get('status') != 'SIAP': continue
                H[b] = h; pl = pd.read_csv(os.path.join(d, mid + '_pilihan.csv')); pl = pl[pl.stop.notna()]
                if len(pl): r = pl.iloc[-1]; P[b] = (r.stop, r.exit, int(r.tmax))
            except Exception:
                pass
        if not H: continue
        undi = pd.Series([str(v) for v in P.values()]).value_counts()
        stabil = len(undi) and undi.iloc[0] >= 2
        pilih = eval(undi.index[0]) if len(undi) else None
        cagr = float(np.median([h['oos'].get('cagr', np.nan) for h in H.values()]))
        mdd = float(np.median([h['oos'].get('mdd', np.nan) for h in H.values()]))
        n = int(np.median([h['oos'].get('n', 0) for h in H.values()]))
        h0 = next(iter(H.values())); beku = h0.get('semasa') or h0.get('beku', {})   # semasa = tetapan Papertrade C (K145+)
        kini = semasa(mid)
        lulus = bool(stabil and pilih is not None and tuple(pilih) != kini and cagr > (beku.get('cagr') or -1)
                     and mdd >= -0.35 and n >= 30)
        rows.append(dict(id=mid, nama=next(iter(H.values())).get('nama', ''), semasa=list(kini), cadangan=list(pilih) if pilih else None,
                         stabil=f'{int(undi.iloc[0]) if len(undi) else 0}/{len(BENIH)}', oos_cagr=cagr, oos_mdd=mdd, oos_n=n,
                         beku_cagr=beku.get('cagr'), beku_mdd=beku.get('mdd'), lulus=lulus,
                         boleh_guna=lulus and 115 <= int(mid[1:]) <= 161))
    os.makedirs(CADANGAN, exist_ok=True)
    json.dump(rows, open(os.path.join(CADANGAN, label + '.json'), 'w'), indent=1, ensure_ascii=False, default=float)
    p = lambda v: '' if v is None or v != v else f'{v * 100:.1f}%'
    L = [f'# Cadangan penalaan semula {label}', '',
         'Dijana oleh `WFO/kod/tala_semula.py cadang`. **Tiada perubahan dibuat sehingga pengguna meluluskan** '
         f'(`tala_semula.py guna {label} Mxx ...`, kaedah M115–M161 sahaja; kaedah asal M01–M111 memerlukan varian baharu secara manual).', '',
         'Pengawal: gabungan suku terkini sama dalam >= 2/3 benih; CAGR luar sampel WFO (median) > CAGR tetapan semasa (beku) dalam tempoh sama; '
         'MDD WFO >= −35%; >= 30 dagangan luar sampel; dan gabungan berbeza daripada tetapan semasa.', '',
         f"**Lulus pengawal: {sum(r['lulus'] for r in rows)} kaedah** "
         f"({sum(r['boleh_guna'] for r in rows)} boleh diguna automatik selepas kelulusan).", '',
         '| Kaedah | Semasa (henti/keluar/tmax) | Cadangan | Stabil | CAGR WFO | MDD WFO | CAGR semasa | n | Lulus |', '|---|---|---|---|---|---|---|---|---|']
    for r in sorted(rows, key=lambda r: (not r['lulus'], -(r['oos_cagr'] or -9))):
        L.append(f"| {r['id']} {r['nama']} | {'/'.join(map(str, r['semasa']))} | {'/'.join(map(str, r['cadangan'])) if r['cadangan'] else ''} | "
                 f"{r['stabil']} | {p(r['oos_cagr'])} | {p(r['oos_mdd'])} | {p(r['beku_cagr'])} | {r['oos_n']} | {'YA' if r['lulus'] else ''} |")
    open(os.path.join(CADANGAN, label + '.md'), 'w').write('\n'.join(L) + '\n')
    print(f"{len(rows)} kaedah; lulus {sum(r['lulus'] for r in rows)} → {os.path.join(CADANGAN, label + '.md')}")


# ---------- 4) guna (selepas kelulusan) ----------
def guna(label, mids):
    sys.path.insert(0, ROOT); import bina_pengeluaran
    rows = {r['id']: r for r in json.load(open(os.path.join(CADANGAN, label + '.json')))}
    for mid in mids:
        r = rows.get(mid)
        if not r or not r['lulus']: print(mid, 'TIDAK LULUS pengawal / tiada dalam cadangan — langkau'); continue
        if not 115 <= int(mid[1:]) <= 161: print(mid, 'kaedah asal: perlu varian baharu secara manual — langkau'); continue
        s, e, x = r['cadangan']
        print(*bina_pengeluaran.bina(mid, (s, e, int(x), f'cadangan {label} diluluskan pengguna')))
    print('Seterusnya: python3 WFO/kod/registry_baru.py <kaedah> ; ujian; sahkan.py; commit + push main; bungkus aset kod dashboard.')


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'data': data(a[1])
    elif a[0] == 'jalan': jalan(a[1], int(a[2]))
    elif a[0] == 'cadang': cadang(a[1])
    elif a[0] == 'guna': guna(a[1], a[2:])
