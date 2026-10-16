# Analisis prestasi SEBENAR Papertrade C (semua claude*.csv) lawan jangkaan backtest setiap kaedah.
#   python3 WFO/kod/analisis_sebenar.py   → WFO/laporan/ANALISIS_SEBENAR.md + WFO/data/analisis_sebenar.json
# Jangkaan = baris registry set 431 bagi VARIAN modul (sama seperti scanner.jangkaan()).
# Bias pemilihan: dagangan yang tutup awal kebanyakannya kena henti, yang untung masih terbuka. Oleh itu ujian
# hanya memakai posisi MATANG (dibeli >= 1.5 x hari pegang jangkaan, min 14 hari kalendar, sebelum tarikh data),
# dengan pulangan = untung_akhir_pct jika tutup, untung_pct (harga terkini) jika masih terbuka.
# AMARAN jika posisi matang >= N_MIN dan kadar menang (binomial, z) atau purata (t satu sampel) < -2 vs jangkaan.
import os, sys, glob, json, math, importlib
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(ROOT, '..', '..')
KOD = os.path.join(REPO, 'BacktestShariah2', 'kod'); sys.path.insert(0, KOD)
PT = os.path.join(REPO, 'BacktestShariah2', 'papertrade')
LAPORAN = os.path.join(ROOT, '..', 'laporan', 'ANALISIS_SEBENAR.md')
JSON = os.path.join(ROOT, '..', 'data', 'analisis_sebenar.json')
N_MIN = 10
B = lambda v: str(v).strip().lower() == 'true'


def jangkaan():
    out = {}
    for f in glob.glob(os.path.join(KOD, 'registry', 'M*.csv')):
        mid = os.path.basename(f)[:-4]
        try:
            m = importlib.import_module(f'kaedah.{mid}')
            r = pd.read_csv(f); r = r[(r['set'].astype(str) == '431') & (r.varian == m.VARIAN)]
            if len(r):
                r = r.iloc[0]
                out[mid] = dict(nama=m.NAMA, keputusan=r.keputusan, win=float(r.win), avg=float(r.avg) * 100, days=float(r.days))
        except Exception:
            pass
    return out


def muat():
    d = pd.concat([pd.read_csv(f, dtype=str, keep_default_na=False) for f in sorted(glob.glob(os.path.join(PT, 'claude*.csv')))])
    for k in ('tidak_sah', 'tidak_dibeli', 'keluar'):
        d[k] = d[k].map(B) if k in d else False
    d = d[~d.tidak_sah & ~d.tidak_dibeli & (d.harga_beli != '')]
    for k in ('untung_pct', 'untung_akhir_pct', 'hari'):
        d[k] = pd.to_numeric(d[k], errors='coerce')
    return d


def analisis():
    d = muat(); J = jangkaan(); rows = []
    kini = pd.to_datetime(d.tarikh_beli).max()
    for mid, g in d.groupby('id_kaedah'):
        t = g[g.keluar]; o = g[~g.keluar]; j = J.get(mid, {})
        umur = max(14, 1.5 * j.get('days', 10) * 7 / 5)
        mt = g[pd.to_datetime(g.tarikh_beli) <= kini - pd.Timedelta(days=umur)]
        pul = mt.untung_akhir_pct.where(mt.keluar, mt.untung_pct)
        r = dict(id=mid, nama=j.get('nama', ''), n=len(g), tutup=len(t), terbuka=len(o),
                 win=float((t.untung_akhir_pct > 0).mean()) if len(t) else None,
                 avg=float(t.untung_akhir_pct.mean()) if len(t) else None,
                 hari=float(t.hari.mean()) if len(t) else None,
                 terbuka_avg=float(o.untung_pct.mean()) if len(o) else None,
                 j_win=j.get('win'), j_avg=j.get('avg'), j_hari=j.get('days'), keputusan=j.get('keputusan'),
                 matang=len(mt), m_win=float((pul > 0).mean()) if len(mt) else None, m_avg=float(pul.mean()) if len(mt) else None)
        z = tt = None
        if len(mt) >= N_MIN and r['j_win'] is not None:
            p = r['j_win']; z = (r['m_win'] - p) / math.sqrt(p * (1 - p) / len(mt)) if 0 < p < 1 else None
            sd = pul.std(ddof=1)
            tt = (r['m_avg'] - r['j_avg']) / (sd / math.sqrt(len(mt))) if sd and sd > 0 else None
        r['z_win'], r['t_avg'] = z, tt
        r['status'] = ('DATA BELUM CUKUP' if len(mt) < N_MIN else
                       'AMARAN' if (z is not None and z < -2) or (tt is not None and tt < -2) else 'SELARI')
        rows.append(r)
    return pd.DataFrame(rows), d


def f(v, p=1, pct=False):
    if v is None or (isinstance(v, float) and math.isnan(v)): return ''
    return f'{v * 100:.{p}f}%' if pct else f'{v:.{p}f}'


def main():
    R, d = analisis()
    R = R.sort_values(['status', 'tutup'], ascending=[True, False])
    os.makedirs(os.path.dirname(JSON), exist_ok=True)
    R.to_json(JSON, orient='records', force_ascii=False, indent=1)
    c = R.status.value_counts().to_dict()
    L = ['# Analisis prestasi sebenar Papertrade C lawan jangkaan backtest', '',
         f'Dijana oleh `WFO/kod/analisis_sebenar.py`. Sumber: semua `papertrade/claude*.csv` ({len(d)} posisi sah; '
         f'{int(d.keluar.sum())} tutup, {int((~d.keluar).sum())} terbuka; {d.tarikh_beli.min()} hingga {d.tarikh_beli.max()}). '
         f'Jangkaan = registry set 431 bagi varian modul (dalam sampel bagi M115–M161).', '',
         f'Ujian hanya atas posisi MATANG (dibeli >= 1.5 x hari pegang jangkaan dan >= 14 hari lalu; tutup = untung akhir, terbuka = untung semasa) '
         f'untuk elak bias pemilihan (yang tutup awal kebanyakannya kena henti). Ambang: >= {N_MIN} posisi matang. '
         f'AMARAN = kadar menang (z) atau purata (t) < −2 berbanding jangkaan.', '',
         f"**Ringkasan:** {c.get('AMARAN', 0)} AMARAN, {c.get('SELARI', 0)} SELARI, {c.get('DATA BELUM CUKUP', 0)} data belum cukup.", '',
         '| Kaedah | Status | n | Matang | Menang matang | Menang jangka | Purata matang % | Purata jangka % | Hari jangka | Tutup (awal) | Purata tutup % | Terbuka purata % | z | t |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for _, r in R.iterrows():
        L.append(f"| {r.id} {r.nama} | {r.status} | {r.n} | {r.matang} | {f(r.m_win, 0, True)} | {f(r.j_win, 0, True)} | "
                 f"{f(r.m_avg, 2)} | {f(r.j_avg, 2)} | {f(r.j_hari, 0)} | {r.tutup} | {f(r.avg, 2)} | {f(r.terbuka_avg, 2)} | {f(r.z_win, 1)} | {f(r.t_avg, 1)} |")
    L += ['', 'Nota: lajur "Tutup (awal)" dan "Purata tutup" ialah maklumat sahaja (berat sebelah ke arah kena henti), tidak dipakai dalam ujian.', '']
    open(LAPORAN, 'w').write('\n'.join(L))
    print(f"ditulis {LAPORAN}: {len(R)} kaedah; {c}")


if __name__ == '__main__':
    main()
