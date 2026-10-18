# F6 Laporan: AUTOTUNE/hasil/LAPORAN.md (≤ 150 baris) dan AUTOTUNE/hasil/papan.json (rekod ringkas setiap
# kaedah, ≤ 2 KB setiap satu, untuk db dashboard). Input: parameter_sedia.csv, ringkasan.json, gabungan.json.
#   python3 AUTOTUNE/sahkan/laporan.py [--keluar DIR]
import argparse, json, math, os, sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umum as U

HAD_BARIS = 150
HAD_REKOD = 2048


def pc(x, nd=1):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return '–'
    return '–' if not math.isfinite(x) else f'{x * 100:.{nd}f}%'


def nb(x, nd=2):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return '–'
    return '–' if not math.isfinite(x) else f'{x:.{nd}f}'


def _param(s):
    try:
        p = json.loads(s) if isinstance(s, str) and s else {}
    except ValueError:
        p = {}
    return ', '.join(f'{k}={_v(v)}' for k, v in p.items()) or '–'


def _v(v):
    return f'{v:.4g}' if isinstance(v, float) else str(v)


def _baca(p, lalai=None):
    try:
        with open(p, encoding='utf-8') as f: return json.load(f)
    except (OSError, ValueError):
        return lalai


def jana(keluar=None):
    keluar = keluar or U.HASIL
    df = pd.read_csv(os.path.join(keluar, 'parameter_sedia.csv'), keep_default_na=True)
    ring = _baca(os.path.join(keluar, 'ringkasan.json'), {})
    gab = _baca(os.path.join(keluar, 'gabungan.json'), {})
    man = _baca(os.path.join(U.AT, 'data', 'manifest.json'), {})
    t = ring.get('tempoh', {})
    L = ['# LAPORAN AUTOTUNE (A01)', '',
         f"Dijana {ring.get('dijana', '')} oleh `AUTOTUNE/sahkan/laporan.py`. Peraturan: `AUTOTUNE/SPEC.md` §5–§7. "
         'Semua angka ialah backtest; tiada order, tiada wang sebenar.', '',
         '## Data dan kaveat',
         f"- Harga yfinance (`auto_adjust`), universe bulanan 2000 saham AS (harga > USD10, nilai dagangan ≥ USD1 juta), "
         f"tanpa penapis Shariah. Data {man.get('tarikh_mula', '2009')} hingga {t.get('data_akhir') or man.get('tarikh_akhir', '–')}"
         f" (tarikan {man.get('tarikan', '–')}; {man.get('n_ticker', '–')} ticker pernah dalam universe).",
         '- Universe kurang daripada 2000 saham sebelum 2021 (kira-kira 1100–1800 sebulan pada 2013–2020; lihat QC.md).',
         '- Bias survivorship: saham delist tiada dalam data; semua keputusan ialah HAD ATAS.',
         '- yfinance percuma: pelarasan dan bar boleh tersilap; ticker dengan > 5 hari |pulangan| > 50% dibuang (QC.md).',
         f"- OOS: {_jul(t.get('oos'))} (12 tetingkap walk-forward, parameter setiap tetingkap sendiri). "
         f"Kumpulan A = tala, B = semakan merentas saham. Tempoh kunci: {_jul(t.get('kunci'))} (parameter AKHIR, A+B, dibuka sekali). "
         f"Ujian bersih: {_jul(t.get('bersih'))} (PARAM asal, A+B).",
         f"- SPY pada tarikh yang sama: OOS {pc(ring.get('spy', {}).get('oos'))}, bersih {pc(ring.get('spy', {}).get('bersih'))} setahun.",
         '', '## Kiraan label', '', '| Label | Bilangan |', '|---|---|']
    for l in U.LABEL:
        L.append(f"| {l} | {ring.get('kiraan_label', {}).get(l, int((df.label == l).sum()))} |")
    L += ['', f"Jumlah {len(df)} kaedah; N percubaan (DSR) = {ring.get('n_cubaan_jumlah', '–')}.", '']
    L += seksyen_hadapan(keluar)
    L += ['## 20 kaedah teratas (CAGR OOS-A)', '',
          '| # | Kaedah | Label | A CAGR | A MDD | B CAGR | B MDD | SPY OOS | Kunci | SPY kunci | DSR | PBO |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
    top = df[~df.label.isin(U.BUKAN_CALON)].sort_values('cagr_a', ascending=False).head(20)
    for i, (_, r) in enumerate(top.iterrows(), 1):
        L.append(f"| {i} | {r.kaedah} {_pendek(r.nama)} | {r.label} | {pc(r.cagr_a)} | {pc(r.mdd_a)} | {pc(r.cagr_b)} | "
                 f"{pc(r.mdd_b)} | {pc(r.spy_a)} | {pc(r.cagr_kunci)} | {pc(r.spy_kunci)} | {nb(r.dsr)} | {nb(r.pbo)} |")
    L += ['', '## Portfolio gabungan (8 slot × 12.5%)', '']
    if gab.get('terpilih'):
        m = gab['metrik']
        L += [f"Terpilih (urutan tamak atas OOS-A): {', '.join(gab['terpilih'])}.", '',
              '| Bahagian | CAGR | MDD | SPY | Tempoh |', '|---|---|---|---|---|']
        for b, n in (('A', 'OOS-A'), ('B', 'OOS-B'), ('kunci', 'Tempoh kunci')):
            x = m.get(b, {})
            L.append(f"| {n} | {pc(x.get('cagr'))} | {pc(x.get('mdd'))} | {pc(x.get('spy'))} | {x.get('mula')} – {x.get('akhir')} |")
        kalah = [n for b, n in (('A', 'OOS-A'), ('B', 'OOS-B'), ('kunci', 'tempoh kunci'))
                 if not (_f(m.get(b, {}).get('cagr')) > _f(m.get(b, {}).get('spy')))]
        if kalah: L += ['', f"**Amaran: gabungan TIDAK mengatasi SPY pada {', '.join(kalah)}.**"]
        L += ['', 'Parameter SEMASA (untuk cadangan dagangan; parameter lain = PARAM asal):', '']
        for k in gab['terpilih']:
            p = gab.get('param_semasa', {}).get(k, {})
            L.append(f"- **{k}**: " + (', '.join(f'{a}={_v(v)}' for a, v in p.items()) or 'PARAM asal'))
        L += ['', 'Log pemilihan:', '']
        for s in gab.get('log', [])[:25]:
            L.append(f"- {s.get('kaedah')}: {s.get('tindakan')}"
                     + (f" (CAGR {pc(s.get('cagr'))}, MDD {pc(s.get('mdd'))})" if s.get('cagr') is not None else '')
                     + (f", korelasi {nb(s.get('korelasi'))}" if s.get('korelasi') is not None else ''))
        sm = gab.get('semakan_satu_kaedah', {})
        if sm:
            L += ['', 'Semakan jana semula (satu kaedah vs JSON tala, beza pulangan harian maksimum): '
                  + ', '.join(f"{k} {nb(v.get('beza_maks'), 6)}" for k, v in sm.items()) + '.']
    else:
        L += [gab.get('penjelasan', 'gabungan.json tiada.'), '']
        for r in gab.get('terbaik3_oos_a', []):
            L.append(f"- {r.get('kaedah')} ({r.get('label')}): OOS-A {pc(r.get('cagr_a'))}, MDD {pc(r.get('mdd_a'))}, "
                     f"OOS-B {pc(r.get('cagr_b'))}, kunci {pc(r.get('cagr_kunci'))}")
    L += ['', '## Nota DSR dan PBO',
          '- DSR (Bailey & López de Prado): Sharpe harian OOS-A dideflasi dengan N = jumlah semua percubaan semua kaedah; '
          f"V[SR] = varians SR OOS-A antara kaedah (formula teras/objektif.py). SR0 = {nb(_ann(ring.get('sr0_harian')))} "
          'setahun. TINGGI memerlukan DSR ≥ 0.95.',
          '- PBO (CSCV, 8 blok, 50 percubaan teratas kajian AKHIR, pulangan latih): kebarangkalian pilihan terbaik dalam '
          'sampel jatuh di bawah median luar sampel. TINGGI memerlukan PBO ≤ 0.30.',
          '- Nisbah dataran (±10%, ±25% setiap parameter TALA): < 0.5 bermakna pilihan berada di puncak sempit.',
          '- Label tidak menjamin prestasi masa depan; tempoh kunci ialah semakan sekali sahaja.']
    belum = df[df.label == 'BELUM DITALA']
    L += ['', f'## BELUM DITALA ({len(belum)})', '']
    if len(belum):
        baris = [f"{r.kaedah} ({r.catatan})" if isinstance(r.catatan, str) and r.catatan else r.kaedah
                 for _, r in belum.iterrows()]
        L.append('; '.join(baris)[:3000])
    else:
        L.append('Tiada.')
    if len(L) > HAD_BARIS: L = L[:HAD_BARIS - 1] + ['(dipotong pada 150 baris)']
    with open(os.path.join(keluar, 'LAPORAN.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    papan = [rekod_papan(r) for _, r in df.iterrows()]
    U.tulis_json(os.path.join(keluar, 'papan.json'), dict(dijana=ring.get('dijana'), tempoh=t,
                 gabungan=gab.get('terpilih', []), kaedah=papan))
    return L, papan


def seksyen_hadapan(keluar):
    """Ringkasan imbasan pandang ke hadapan dan audit M81 (Pindaan 18 Okt 2026)."""
    ph = U.pandang_hadapan(os.path.join(keluar, 'pandang_hadapan.json'))
    baiki = sorted((k for k, e in ph.items() if e.get('status') == 'DIBAIKI'), key=lambda s: (len(s), s))
    kecuali = sorted((k for k, e in ph.items() if e.get('status') == 'PANDANG HADAPAN'), key=lambda s: (len(s), s))
    L = ['## Imbasan pandang ke hadapan (Pindaan 18 Okt 2026)', '',
         '- Audit [M81](AUDIT_M81.md): hasil asal ialah ARTIFAK — `_exit_ekor` menanda `exitc[j-1]` daripada rendah hari j, '
         'jadi enjin keluar pada buka j dengan pengetahuan hari j.',
         '- Semua 134 salinan diimbas (`AUTOTUNE/kaedah/semak_hadapan.py`, data 431, PARAM asal, potong 2021-06-30, 2023-03-31, '
         '2025-06-30): `exitc/stop/tgt` mesti sama hingga hari potong; `sig/rank` hingga hari sebelumnya, dan pada hari '
         'potong hanya boleh bergantung pada buka esok. Butiran: [PANDANG_HADAPAN.md](PANDANG_HADAPAN.md).',
         f"- Dibaiki dan ditala semula ({len(baiki)}): " + (', '.join(f"{k} ({', '.join(ph[k].get('lajur') or [])})" for k in baiki) or 'tiada') + '.',
         f"- Dikecualikan, label PANDANG HADAPAN, bukan calon gabungan ({len(kecuali)}): "
         + (', '.join(f"{k} ({', '.join(ph[k].get('lajur') or [])})" for k in kecuali) or 'tiada') + '.', '']
    return L


def _f(x):
    try: return float(x)
    except (TypeError, ValueError): return float('nan')


def _ann(x):
    try: return float(x) * math.sqrt(252)
    except (TypeError, ValueError): return None


def _jul(x):
    return f'{x[0]} – {x[1]}' if isinstance(x, (list, tuple)) and len(x) == 2 and x[0] else '–'


def _pendek(s, n=28):
    if not isinstance(s, str) or not s: return ''
    return '(' + (s if len(s) <= n else s[:n - 1] + '…') + ')'


MEDAN_PAPAN = ['cagr_a', 'mdd_a', 'n_a', 'hari_a', 'menang_a', 'spy_a', 'cagr_b', 'mdd_b', 'spy_b',
               'cagr_kunci', 'mdd_kunci', 'spy_kunci', 'cagr_bersih', 'spy_bersih', 'dsr', 'dataran', 'pbo', 'n_cubaan']


def rekod_papan(r):
    d = dict(id=r.kaedah, nama=(r.nama if isinstance(r.nama, str) else '')[:60], label=r.label)
    d.update(U.bersih({k: r[k] for k in MEDAN_PAPAN if k in r}, 4))
    try:
        d['param'] = json.loads(r.param_semasa) if isinstance(r.param_semasa, str) else {}
    except ValueError:
        d['param'] = {}
    d['param'] = U.bersih(d['param'], 5)
    d['catatan'] = (r.catatan if isinstance(r.catatan, str) else '')[:200]
    while len(json.dumps(d, ensure_ascii=False, separators=(',', ':')).encode()) > HAD_REKOD:
        if d['catatan']: d['catatan'] = ''
        elif d['param']: d['param'].pop(next(iter(d['param'])))
        else: d['nama'] = d['nama'][:20]; break
    return d


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--keluar', default=None)
    L, papan = jana(ap.parse_args().keluar)
    print(f'laporan: LAPORAN.md {len(L)} baris, papan.json {len(papan)} rekod')


if __name__ == '__main__':
    main()
