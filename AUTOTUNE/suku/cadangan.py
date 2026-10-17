# AUTOTUNE F8: CADANGAN tala semula suku tahun. Bandingkan parameter SEMASA baharu (hasil/suku/<Q>/tala/Mxx/k13.json)
# dengan k13 lama (hasil/tala/Mxx/k13.json; jika tiada, param_semasa dalam hasil/parameter_sedia.csv).
# Output: hasil/suku/<Q>/CADANGAN.md (≤120 baris) dan cadangan.json. TIDAK mengubah papertrade atau fail lain.
# Guna: python3 AUTOTUNE/suku/cadangan.py --suku 2026-Q4 [--hasil AUTOTUNE/hasil]
import os, re, csv, json, math, argparse, glob

AKAR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HASIL = os.path.join(AKAR, 'AUTOTUNE', 'hasil')
MAKS_BARIS = 120
POLA = re.compile(r'^20\d\d-Q[1-4]$')


def _baca(f):
    try:
        with open(f) as fh: return json.load(fh)
    except (OSError, ValueError): return None


def _angka(x): return isinstance(x, (int, float)) and not isinstance(x, bool)


def _sama(a, b):
    if _angka(a) and _angka(b): return math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-12)
    return a == b


def beza_param(lama, baru):
    """{p: [lama, baru]} bagi parameter yang berubah; parameter tiada di satu pihak ditanda None."""
    out = {}
    for p in sorted(set(lama) | set(baru)):
        a, b = lama.get(p), baru.get(p)
        if a is None or b is None or not _sama(a, b): out[p] = [a, b]
    return out


def _met(H, kunci):
    m = (H or {}).get(kunci) or {}
    c, d = m.get('cagr'), m.get('mdd')
    return (c if _angka(c) else None), (d if _angka(d) else None)


def muat_sedia(f):
    """{kaedah: {label, param}} daripada parameter_sedia.csv (kosong jika tiada)."""
    out = {}
    try:
        with open(f, newline='') as fh:
            for r in csv.DictReader(fh):
                try: p = json.loads(r.get('param_semasa') or '{}')
                except ValueError: p = {}
                out[r['kaedah']] = dict(label=r.get('label') or '', param=p if isinstance(p, dict) else {})
    except OSError: pass
    return out


def satu(mid, baru, lama, sedia):
    """Rekod cadangan bagi satu kaedah. baru/lama: kandungan k13.json (atau None); sedia: baris parameter_sedia atau None."""
    r = dict(kaedah=mid, label=(sedia or {}).get('label', ''), status=(baru or {}).get('status'))
    if not baru:
        r.update(tindakan='TIADA HASIL', param_baru=None, param_lama=None, ubah={}, sumber_lama=None,
                 cagr_rujuk=None, mdd_rujuk=None, rujuk='-', delta_cagr=None)
        return r
    r['belum_ditala'] = bool(baru.get('belum_ditala')); r['ada_lulus'] = baru.get('ada_lulus')
    pb = baru.get('params') or {}
    if lama and lama.get('status') == 'SIAP' and isinstance(lama.get('params'), dict): pl, sl = lama['params'], 'k13'
    elif sedia and sedia.get('param'): pl, sl = sedia['param'], 'parameter_sedia'
    else: pl, sl = None, None
    r.update(param_baru=pb, param_lama=pl, sumber_lama=sl)
    r['cagr_baru'], r['mdd_baru'] = _met(baru, 'latih_A')
    r['cagr_lama'], r['mdd_lama'] = _met(lama, 'latih_A') if sl == 'k13' else (None, None)
    r['cagr_asal'], r['mdd_asal'] = _met(baru, 'latih_A_asal')   # PARAM asal pada tetingkap baharu
    r['ubah'] = beza_param(pl, pb) if pl is not None else {}
    if baru.get('status') != 'SIAP': r['tindakan'] = 'GAGAL'
    elif r['belum_ditala'] or not baru.get('tala'): r['tindakan'] = 'BELUM DITALA'
    elif pl is None: r['tindakan'] = 'TIADA ASAS'
    elif not r['ubah']: r['tindakan'] = 'KEKAL'
    elif baru.get('ada_lulus') is False: r['tindakan'] = 'KEKAL (tiada calon lulus)'
    else: r['tindakan'] = 'UBAH'
    if r['cagr_lama'] is not None: r['cagr_rujuk'], r['mdd_rujuk'], r['rujuk'] = r['cagr_lama'], r['mdd_lama'], 'k13'
    elif r['cagr_asal'] is not None: r['cagr_rujuk'], r['mdd_rujuk'], r['rujuk'] = r['cagr_asal'], r['mdd_asal'], 'asal'
    else: r['cagr_rujuk'], r['mdd_rujuk'], r['rujuk'] = None, None, '-'
    r['delta_cagr'] = (r['cagr_baru'] - r['cagr_rujuk']) if (r['cagr_baru'] is not None and r['cagr_rujuk'] is not None) else None
    return r


def jana(suku, hasil=HASIL):
    if not POLA.match(suku): raise ValueError(f'label suku tidak sah: {suku!r}')
    dbaru = os.path.join(hasil, 'suku', suku, 'tala')
    sedia = muat_sedia(os.path.join(hasil, 'parameter_sedia.csv'))
    ids = sorted({os.path.basename(os.path.dirname(f)) for f in glob.glob(os.path.join(dbaru, 'M*', 'k13.json'))},
                 key=lambda x: int(x[1:]) if x[1:].isdigit() else 0)
    R = [satu(m, _baca(os.path.join(dbaru, m, 'k13.json')), _baca(os.path.join(hasil, 'tala', m, 'k13.json')), sedia.get(m))
         for m in ids]
    kira = {}
    for r in R: kira[r['tindakan']] = kira.get(r['tindakan'], 0) + 1
    return dict(suku=suku, kajian=13, nota='cadangan sahaja; perlu kelulusan pengguna', n_kaedah=len(R), kira=kira, kaedah=R)


def _pct(x): return '-' if x is None else f'{x * 100:.1f}%'
def _v(x): return 'tiada' if x is None else (f'{x:.4g}' if isinstance(x, float) else str(x))


def tulis_md(C):
    R = C['kaedah']
    ub = sorted([r for r in R if r['tindakan'] == 'UBAH'], key=lambda r: -(r['delta_cagr'] if r['delta_cagr'] is not None else -9))
    L = [f"# CADANGAN tala semula {C['suku']} (kajian 13 SEMASA)", '',
         '**Cadangan sahaja; perlu kelulusan pengguna.** Tiada fail papertrade, kaedah atau parameter semasa diubah. '
         'Semua angka ialah backtest latih (3 tahun terkini); tiada order, tiada wang sebenar.', '',
         f"- Kaedah dinilai: {C['n_kaedah']}. Ringkasan: " + (', '.join(f'{k} {v}' for k, v in sorted(C['kira'].items())) or 'tiada'),
         '- Rujukan CAGR/MDD: `k13` = k13 lama pada tetingkap lamanya; `asal` = PARAM asal kaedah pada tetingkap baharu '
         '(digunakan jika k13 lama tiada). Tetingkap berbeza: banding secara kasar sahaja.', '',
         '## Cadangan ubah parameter (disusun ikut kenaikan CAGR latih)', '']
    if not ub: L.append('Tiada cadangan ubah.')
    else:
        L += ['| Kaedah | Label | Param berubah (lama → baru) | CAGR rujuk | CAGR baru | MDD rujuk | MDD baru | Rujuk |',
              '|---|---|---|---|---|---|---|---|']
        baki = max(MAKS_BARIS - len(L) - 12, 0)
        for r in ub[:baki]:
            p = '; '.join(f'{k} {_v(a)}→{_v(b)}' for k, (a, b) in list(r['ubah'].items())[:4])
            if len(r['ubah']) > 4: p += f"; +{len(r['ubah']) - 4}"
            L.append(f"| {r['kaedah']} | {r['label'] or '-'} | {p[:90]} | {_pct(r['cagr_rujuk'])} | {_pct(r['cagr_baru'])} | "
                     f"{_pct(r['mdd_rujuk'])} | {_pct(r['mdd_baru'])} | {r['rujuk']} |")
        if len(ub) > baki: L.append(f'| ... | | {len(ub) - baki} kaedah lagi: lihat `cadangan.json` | | | | | |')
    sk = [r['kaedah'] for r in R if r['tindakan'] in ('GAGAL', 'TIADA HASIL')]
    ta = [r['kaedah'] for r in R if r['tindakan'] == 'TIADA ASAS']
    L += ['', '## Perlu perhatian', '',
          f"- Gagal/tiada hasil ({len(sk)}): " + ((', '.join(sk[:30]) + (' ...' if len(sk) > 30 else '')) if sk else 'tiada'),
          f"- Tiada asas perbandingan ({len(ta)}): " + ((', '.join(ta[:30]) + (' ...' if len(ta) > 30 else '')) if ta else 'tiada'),
          '', '## Langkah seterusnya', '',
          'Pengguna menyemak jadual, kemudian memutuskan sama ada menggantikan parameter semasa. Jalankan semula '
          '`autotune_sahkan.yml` (F6) sebelum sebarang perubahan diterima pakai. Fail ini tidak menukar apa-apa secara automatik.']
    return '\n'.join(L[:MAKS_BARIS]) + '\n'


def main(argv=None):
    a = argparse.ArgumentParser(); a.add_argument('--suku', required=True); a.add_argument('--hasil', default=HASIL)
    x = a.parse_args(argv)
    C = jana(x.suku, x.hasil); d = os.path.join(x.hasil, 'suku', x.suku); os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'cadangan.json'), 'w') as f: json.dump(C, f, indent=1)
    with open(os.path.join(d, 'CADANGAN.md'), 'w') as f: f.write(tulis_md(C))
    print(f"{C['suku']}: {C['n_kaedah']} kaedah; " + ', '.join(f'{k} {v}' for k, v in sorted(C['kira'].items())))


if __name__ == '__main__':
    main()
