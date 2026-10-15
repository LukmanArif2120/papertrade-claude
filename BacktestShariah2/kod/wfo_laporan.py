# Jana laporan Fasa C W01 daripada data/wfo/hasil/*.json → laporan/W01_LAPORAN.md
import os, json, math
from statistics import NormalDist
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
HASIL = os.path.join(ROOT, '..', 'data', 'wfo', 'hasil')
LAPORAN = os.path.join(ROOT, '..', 'laporan', 'W01_LAPORAN.md')
N = NormalDist()
p = lambda x: '' if x is None or (isinstance(x, float) and math.isnan(x)) else f'{x * 100:.1f}%'


def muat():
    out = {}
    for f in sorted(os.listdir(HASIL)):
        if f.endswith('.json'):
            h = json.load(open(os.path.join(HASIL, f)))
            if 'menang_ew_subset' in h: h['menang_ew_subset'] = int(h['menang_ew_subset'])
            out[f[:-5]] = h
    return out

def sharpe(mid):
    f = os.path.join(HASIL, mid + '_ekuiti.csv')
    if not os.path.exists(f): return np.nan, np.nan, np.nan, 0
    r = pd.read_csv(f, index_col=0).iloc[:, 0].pct_change().dropna()
    if len(r) < 30 or r.std() == 0: return np.nan, np.nan, np.nan, len(r)
    return r.mean() / r.std(), float(r.skew()), float(r.kurt() + 3), len(r)

def dsr(sr, sk, ku, n, sr0):
    """Deflated Sharpe ratio (Bailey & López de Prado 2014), SR harian."""
    d = math.sqrt(max(1e-12, 1 - sk * sr + (ku - 1) / 4 * sr ** 2))
    return N.cdf((sr - sr0) * math.sqrt(n - 1) / d)

def lulus(h, m96, ewc):
    o = h['oos']
    if o.get('n', 0) == 0: return False, 'tiada dagangan'
    gagal = []
    if not o['cagr'] > m96: gagal.append('≤M96')
    if not o['cagr'] > ewc: gagal.append('≤EW')
    if o['mdd'] < -0.35: gagal.append('MDD')
    if o['n'] < 60: gagal.append('n<60')
    if h['menang_ew_subset'] < 3: gagal.append(f"subset {h['menang_ew_subset']}/4")
    if (o.get('tumpuan_maks') or 0) > 0.25: gagal.append('tumpuan')
    return not gagal, ' '.join(gagal)

def mod(mid, col):
    f = os.path.join(HASIL, mid + '_pilihan.csv')
    try: s = pd.read_csv(f)[col].astype(str)
    except Exception: return ''
    v = s.value_counts(); return f'{v.index[0]} ({v.iloc[0]}/{len(s)})'


def main():
    H = muat(); K = {k: v for k, v in H.items() if k.startswith('M')}
    siap = {k: v for k, v in K.items() if v.get('status') == 'SIAP'}
    tl = {k: v for k, v in K.items() if v.get('status') == 'TIDAK LAYAK'}
    ra = {k: v for k, v in K.items() if v.get('status') == 'RALAT'}
    if not siap: print('tiada hasil'); return
    any_ = next(iter(siap.values()))
    ewc, spy, qqq = any_['ew']['cagr'], any_['spy']['cagr'], any_['qqq']['cagr']
    m96 = siap['M96']['beku']['cagr'] if 'M96' in siap else float('nan')

    S = {k: sharpe(k) for k in siap}
    srs = [s[0] for s in S.values() if not math.isnan(s[0])]
    nk = len(srs); v = np.var(srs) if nk > 1 else 0
    g = 0.5772156649
    sr0 = math.sqrt(v) * ((1 - g) * N.inv_cdf(1 - 1 / nk) + g * N.inv_cdf(1 - 1 / (nk * math.e))) if nk > 1 else 0

    rows = []
    for k, h in siap.items():
        o, b = h['oos'], h['beku']; ok, why = lulus(h, m96, ewc); sr, sk, ku, n = S[k]
        rows.append(dict(id=k, nama=h['nama'], cagr=o.get('cagr'), mdd=o.get('mdd'), win=o.get('win'), hit10=o.get('hit10'),
                         n=o.get('n', 0), hari=o.get('hari'), bcagr=b.get('cagr'), bmdd=b.get('mdd'),
                         subw=h['menang_ew_subset'], dsr=dsr(sr, sk, ku, n, sr0) if not math.isnan(sr) else np.nan,
                         lulus=ok, gagal=why))
    R = pd.DataFrame(rows).sort_values('cagr', ascending=False).reset_index(drop=True)

    L = [f'# Laporan W01 — WFO stop/exit/tempoh pegangan bagi setiap kaedah (Fasa C)', '',
         f'Spec: `spec/SPEC_WFO_SISTEM_SWING.md`. Enjin v1.2 (beku). Alam 423 saham. Luar sampel: 1 Jan 2023 – 2 Okt 2026 (16 suku). '
         f'Optuna {any_.get("percubaan")} percubaan setiap suku, latih 3 tahun. Objektif: CAGR maks, MDD ≥ −35%.', '',
         '## 1. Ringkasan', '',
         f'- Kaedah diuji: {len(siap)} siap; {len(tl)} tidak layak; {len(ra)} ralat.',
         f'- Penanda aras luar sampel: EW 423 {p(ewc)}, SPY {p(spy)}, QQQ {p(qqq)}, M96 V1 beku {p(m96)}.',
         f'- Versi WFO mengalahkan varian beku sendiri: {int((R.cagr > R.bcagr).sum())}/{len(R)} kaedah.',
         f'- LULUS semua kriteria §7: {int(R.lulus.sum())} kaedah' + (f" ({', '.join(R.id[R.lulus])})." if R.lulus.any() else '.'),
         f'- Deflated Sharpe: SR* (jangkaan maksimum nasib, {nk} kaedah) = {sr0 * math.sqrt(252):.2f} tahunan. DSR ≥ 0.95 = kebarangkalian tinggi bukan nasib.', '']
    if 'W01' in H and H['W01'].get('status') == 'SIAP':
        w = H['W01']; o = w['oos']; ok, why = lulus(w, m96, ewc)
        L += ['## 2. W01 gabungan (entry turut dipilih)', '',
              f"Entry calon: {', '.join(w['entry'])}. CAGR {p(o.get('cagr'))}, MDD {p(o.get('mdd'))}, menang {p(o.get('win'))}, "
              f"Hit10 {p(o.get('hit10'))}, n {o.get('n')}, subset {w['menang_ew_subset']}/4. **{'LULUS' if ok else 'DITOLAK'}** {why}", '',
              f"Pilihan paling kerap: entry {mod('W01', 'entry')}, stop {mod('W01', 'stop')}, exit {mod('W01', 'exit')}, tmax {mod('W01', 'tmax')}.", '']
    L += ['## 3. Semua kaedah (luar sampel, susun ikut CAGR WFO)', '',
          '| # | ID | Kaedah | CAGR WFO | MDD | Menang | Hit10 | n | Hari | CAGR beku | MDD beku | Subset | DSR | Keputusan |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for i, r in R.iterrows():
        L.append(f"| {i + 1} | {r.id} | {r.nama} | {p(r.cagr)} | {p(r.mdd)} | {p(r.win)} | {p(r.hit10)} | {r.n} | "
                 f"{'' if pd.isna(r.hari) else round(r.hari)} | {p(r.bcagr)} | {p(r.bmdd)} | {r.subw}/4 | "
                 f"{'' if pd.isna(r.dsr) else f'{r.dsr:.2f}'} | {'LULUS' if r.lulus else 'DITOLAK: ' + r.gagal} |")
    L += ['', '## 4. Gabungan paling kerap dipilih (10 teratas)', '', '| ID | Stop | Exit | Tmax |', '|---|---|---|---|']
    for k in R.id[:10]:
        L.append(f"| {k} | {mod(k, 'stop')} | {mod(k, 'exit')} | {mod(k, 'tmax')} |")
    if tl or ra:
        L += ['', '## 5. Tidak layak / ralat', '']
        L += [f"- {k}: {v.get('sebab', '')}" for k, v in tl.items()]
        L += [f"- {k}: RALAT — {v.get('sebab', '').strip().splitlines()[-1] if v.get('sebab') else ''}" for k, v in ra.items()]
    L += ['', '## 6. Nota tafsiran', '',
          '- CAGR beku = varian registry dengan stop/exit asal, dagangan masuk ≥ 1 Jan 2023, portfolio sama. Ia BUKAN luar sampel tulen (varian dipilih dengan melihat data 2019–2026).',
          '- CAGR WFO ialah luar sampel tulen: setiap suku memakai gabungan yang dipilih atas 3 tahun sebelumnya sahaja.',
          '- Subset: gabungan terpilih yang sama dinilai atas S1–S4 (tidak ditala semula); bilangan subset yang mengalahkan EW subset.',
          '- Kriteria LULUS (§7): CAGR > M96 V1 beku dan > EW; MDD ≥ −35%; n ≥ 60; subset ≥ 3/4; tiada saham > 25% keuntungan.', '']
    open(LAPORAN, 'w').write('\n'.join(L))
    print('ditulis', LAPORAN, len(R), 'kaedah')


if __name__ == '__main__':
    main()
