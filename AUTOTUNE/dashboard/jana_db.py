# F7 Dashboard: dokumen db koleksi `autotune` (tab AUTOTUNE dashboard sedia ada) daripada output F5/F6.
#   python3 AUTOTUNE/dashboard/jana_db.py [--hasil AUTOTUNE/hasil] [--keluar AUTOTUNE/dashboard/db] [--versi versi.json]
# Input (mana-mana yang wujud): <hasil>/ringkasan.json, gabungan.json, papan.json (laporan.py, gabungan.py,
# pengesahan.py) dan <hasil>/tala/Mxx/kNN.json (kemajuan tala). Tanpa fail F6, hanya `autotune/status` ditulis.
# Output: <keluar>/autotune/<doc_id>.json (satu fail setiap dokumen, JSON padat, < 262,144 bait),
#   <keluar>/_indeks.json [{collection, doc_id, path (relatif repo), bait}] dan <keluar>/_batch_<n>.json (writes
#   ArtifactData `batch`: op set + file_path mutlak; ≤ 50 tulisan dan < 900 KB setiap batch; if_version jika --versi).
# Dokumen: autotune/status (sentiasa), autotune/ringkasan, autotune/gabungan, autotune/kaedah_<ID> (satu setiap kaedah).
# Setiap dokumen membawa `dibina` yang sama; tab hanya memapar kaedah_<ID> yang tersenarai dalam ringkasan.kaedah_doc
# dan sama `dibina` (dokumen lama diabaikan, tidak perlu dipadam).
# A02 (ringkasan/papan.json `versi` = 'A02', cth. --hasil AUTOTUNE/hasil_a02 --keluar AUTOTUNE/dashboard/db_a02): doc_id
# berawalan `a02_` (A01 tidak ditindih), label A02 daripada ringkasan.label, kajian_penuh 8, setiap dokumen `versi: A02`.
import argparse, csv, glob, json, math, os, sys
from datetime import datetime, timezone

DIR = os.path.dirname(os.path.abspath(__file__))
AT = os.path.dirname(DIR)
REPO = os.path.dirname(AT)
KOL = 'autotune'
HAD_DB = 262144          # had dokumen db dashboard (BacktestShariah2/standard/dashboard.md §6)
HAD_SELAMAT = 240000     # sasaran dokumen ini
HAD_BATCH = 900_000      # sama seperti BacktestShariah2/standard/jana_db.py
MAKS_TULIS = 50
LABEL = ['TINGGI', 'SEDERHANA', 'RENDAH', 'GAGAL', 'BUKAN SWING', 'PANDANG HADAPAN', 'BELUM DITALA']
KAVEAT = 'Had atas: data tanpa saham delist (yfinance); hasil backtest, bukan jaminan.'


def padat(x):
    return json.dumps(x, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def bait(x):
    return len(padat(x).encode('utf-8'))


def bersih(x):
    """NaN/inf → None supaya JSON sah."""
    if isinstance(x, dict): return {k: bersih(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [bersih(v) for v in x]
    if isinstance(x, float) and not math.isfinite(x): return None
    return x


def baca(p):
    try:
        with open(p, encoding='utf-8') as f: return json.load(f)
    except (OSError, ValueError):
        return None


def _rel(p):
    a = os.path.abspath(p)
    return os.path.relpath(a, REPO) if a.startswith(REPO + os.sep) else a


# ---------- dokumen ----------
def doc_status(hasil, dibina, kajian_penuh=14):
    """Kemajuan tala daripada <hasil>/tala/Mxx/kNN.json (medan kecil sahaja; tidak bergantung pada F6)."""
    kaedah = {}
    for p in sorted(glob.glob(os.path.join(hasil, 'tala', '*', 'k*.json'))):
        kid = os.path.basename(os.path.dirname(p)); k = os.path.basename(p)[1:-5]
        if not k.isdigit(): continue
        d = baca(p) or {}
        o = kaedah.setdefault(kid, dict(siap=[], tidak_siap=[], percubaan=0))
        if d.get('status') == 'SIAP': o['siap'].append(int(k))
        else: o['tidak_siap'].append(int(k))
        o['percubaan'] += int(d.get('n_trials') or 0)
        if d.get('belum_ditala'): o['belum_ditala'] = True
    for o in kaedah.values():
        o['siap'].sort(); o['tidak_siap'].sort()
    masa = None
    mp = os.path.join(hasil, 'tala', '_masa.csv')
    if os.path.exists(mp):
        with open(mp, encoding='utf-8') as f:
            masa = max((r.get('mula') or '' for r in csv.DictReader(f)), default=None) or None
    ada = {f: os.path.exists(os.path.join(hasil, f)) for f in ('ringkasan.json', 'gabungan.json', 'papan.json')}
    return dict(dibina=dibina, kaedah=kaedah, n_kaedah=len(kaedah),
                n_kajian_siap=sum(len(o['siap']) for o in kaedah.values()),
                n_percubaan=sum(o['percubaan'] for o in kaedah.values()), tala_terakhir=masa, fail_f6=ada,
                kajian_penuh=kajian_penuh)


def doc_ringkasan(ring, papan, gab, dibina, contoh, kaedah_doc, label=LABEL):
    ring = ring or {}
    kira = ring.get('kiraan_label')
    if not kira and papan:
        kira = {l: sum(1 for r in papan.get('kaedah', []) if r.get('label') == l) for l in label}
    return dict(dibina=dibina, contoh=contoh, dijana=ring.get('dijana') or (papan or {}).get('dijana'),
                n_kaedah=ring.get('n_kaedah', len((papan or {}).get('kaedah', []))),
                n_cubaan_jumlah=ring.get('n_cubaan_jumlah'), sr0_harian=ring.get('sr0_harian'),
                kiraan_label={l: int((kira or {}).get(l, 0)) for l in label},
                tempoh=ring.get('tempoh') or (papan or {}).get('tempoh') or {},
                spy=ring.get('spy') or {}, belum_ditala=ring.get('belum_ditala', []),
                gabungan=(gab or {}).get('terpilih') or (papan or {}).get('gabungan') or [],
                kaedah_doc=kaedah_doc, kaveat=KAVEAT)


def doc_gabungan(gab, dibina, contoh):
    g = dict(gab or {})
    g.pop('param_semasa_penuh', None)       # besar; param_semasa (yang ditala) mencukupi untuk paparan
    g['log'] = (g.get('log') or [])[:25]
    g['gagal_jana'] = {k: str(v)[:160] for k, v in list((g.get('gagal_jana') or {}).items())[:40]}
    g.update(dibina=dibina, contoh=contoh)
    # had saiz: buang butiran yang paling kurang penting dahulu
    for buang in ('gagal_jana', 'semakan_satu_kaedah', 'param_akhir', 'log'):
        if bait(g) < HAD_SELAMAT: break
        g.pop(buang, None)
    if bait(g) >= HAD_SELAMAT and isinstance(g.get('ekuiti_bulanan'), dict):
        g['ekuiti_bulanan'] = {k: v[::3] for k, v in g['ekuiti_bulanan'].items()}  # suku tahunan
    return g


def doc_kaedah(r, dibina):
    d = dict(r); d['dibina'] = dibina
    while bait(d) > 4096:  # laporan.py sudah ≤ 2 KB; jaga-jaga
        if d.get('catatan'): d['catatan'] = ''
        elif d.get('param'): d['param'].pop(next(iter(d['param'])))
        else: break
    return d


def bina(hasil, dibina=None, contoh=None):
    dibina = dibina or datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    if contoh is None: contoh = os.path.basename(os.path.normpath(hasil)) == 'contoh'
    ring, gab, papan = (bersih(baca(os.path.join(hasil, f))) for f in ('ringkasan.json', 'gabungan.json', 'papan.json'))
    a02 = 'A02' in ((ring or {}).get('versi'), (papan or {}).get('versi'))
    awal = 'a02_' if a02 else ''
    label = (ring or {}).get('label') or LABEL
    docs = {awal + 'status': doc_status(hasil, dibina, 8 if a02 else 14)}
    kaedah_doc = []
    for r in (papan or {}).get('kaedah', []):
        if not r.get('id'): continue
        did = awal + 'kaedah_' + str(r['id'])
        docs[did] = doc_kaedah(r, dibina); kaedah_doc.append(did)
    if ring or papan:
        docs[awal + 'ringkasan'] = doc_ringkasan(ring, papan, gab, dibina, contoh, kaedah_doc, label)
    if gab:
        docs[awal + 'gabungan'] = doc_gabungan(gab, dibina, contoh)
    if a02:
        for d in docs.values(): d['versi'] = 'A02'
    return {k: bersih(v) for k, v in docs.items()}


def tulis(docs, keluar, versi=None):
    versi = versi or {}
    dk = os.path.join(keluar, KOL); os.makedirs(dk, exist_ok=True)
    for p in glob.glob(os.path.join(dk, '*.json')) + glob.glob(os.path.join(keluar, '_batch_*.json')):
        os.remove(p)                       # folder ini milik skrip; buang dokumen larian lama
    indeks, tulisan = [], []
    for did, d in docs.items():
        sz = bait(d)
        if sz >= HAD_DB: raise SystemExit(f'{KOL}/{did}: {sz} bait melebihi had db {HAD_DB}')
        p = os.path.join(dk, did + '.json')
        with open(p, 'w', encoding='utf-8') as f: f.write(padat(d))
        indeks.append(dict(collection=KOL, doc_id=did, path=_rel(p), bait=sz))
        w = dict(op='set', collection=KOL, doc_id=did, file_path=os.path.abspath(p))
        v = versi.get(f'{KOL}/{did}')
        if v: w['if_version'] = int(v)
        tulisan.append((w, sz))
    batches, cur, size = [], [], 0
    for w, sz in tulisan:
        if cur and (size + sz > HAD_BATCH or len(cur) >= MAKS_TULIS):
            batches.append(cur); cur, size = [], 0
        cur.append(w); size += sz
    if cur: batches.append(cur)
    fail = []
    for i, bt in enumerate(batches):
        p = os.path.join(keluar, f'_batch_{i}.json')
        with open(p, 'w', encoding='utf-8') as f: json.dump(bt, f, indent=1)
        fail.append(_rel(p))
    with open(os.path.join(keluar, '_indeks.json'), 'w', encoding='utf-8') as f:
        json.dump(dict(dibina=next(iter(docs.values()))['dibina'], dokumen=indeks, batch=fail), f, ensure_ascii=False, indent=1)
    return indeks, fail


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--hasil', default=os.path.join(AT, 'hasil'))
    ap.add_argument('--keluar', default=os.path.join(DIR, 'db'))
    ap.add_argument('--versi', help='JSON {"autotune/<doc_id>": versi} daripada ArtifactData list (if_version)')
    ap.add_argument('--dibina', help='cap masa tetap (ujian)')
    a = ap.parse_args(argv)
    versi = baca(a.versi) if a.versi else {}
    docs = bina(a.hasil, a.dibina)
    indeks, fail = tulis(docs, a.keluar, versi)
    st = docs.get('status') or docs['a02_status']
    print(f"autotune db: {len(indeks)} dokumen ({', '.join(i['doc_id'] for i in indeks[:6])}{' …' if len(indeks) > 6 else ''}); "
          f"terbesar {max(i['bait'] for i in indeks)} B; batch {len(fail)}")
    print(f"  tala: {st['n_kaedah']} kaedah, {st['n_kajian_siap']} kajian siap; fail F6: "
          + (', '.join(k for k, v in st['fail_f6'].items() if v) or 'tiada'))
    return indeks


if __name__ == '__main__':
    main()
