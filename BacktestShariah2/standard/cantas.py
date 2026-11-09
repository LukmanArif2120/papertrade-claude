"""CANTAS — label maklumat bulanan: kaedah mana calon untuk berhenti direkod. Pradaftar `standard/SPEC_CANTAS.md`.

Membaca `data/analisis/kad_skor.json` (penyebut kad skor, LANGSUNG sahaja) dan `cantas.json` larian lalu (untuk C4 dan
`bulan_berturut`). Menulis `laporan/CANTAS.md` + `data/analisis/cantas.json`. TIDAK mengubah Lejar atau kad skor:
cantas sebenar ialah keputusan pengguna dalam `koordinator/keputusan.csv`.

  python3 BacktestShariah2/standard/cantas.py
"""
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
KS = os.environ.get('KS_JSON', os.path.join(BS2, 'data', 'analisis', 'kad_skor.json'))
OUT_JSON = os.environ.get('CANTAS_JSON', os.path.join(BS2, 'data', 'analisis', 'cantas.json'))
OUT_MD = os.environ.get('CANTAS_MD', os.path.join(BS2, 'laporan', 'CANTAS.md'))
sys.path.insert(0, HERE)

# Ambang DIKUNCI (SPEC_CANTAS.md; ujian/test_cantas.py::TestKunci)
C1_HARI_BELI, C1_POSISI, C1_HARI0_PCT = 12, 30, 20.0
C2_PANTAU = ('BERSARA', 'GANTUNG')
C4_LARIAN = 2
C5_SESI, C5_JURANG, C5_MDD = 63, 5.0, -10.0
BULAN_CADANG = 2


def _f(x, lalai=float('nan')):
    try:
        return float(x)
    except (TypeError, ValueError):
        return lalai


def nilai(r, lama=None):
    """Senarai (kod, sebab) peraturan yang dipenuhi oleh satu baris kad skor; `lama` = rekod larian lalu."""
    k = []
    if r.get('keluarga') == 'M' and _f(r.get('hari_beli'), 0) >= C1_HARI_BELI and \
            _f(r.get('n'), 0) >= C1_POSISI and _f(r.get('hari0_pct'), 0) >= C1_HARI0_PCT:
        k.append(('C1', f"henti hari-0 {_f(r.get('hari0_pct')):.0f}% daripada {int(_f(r.get('n')))} posisi"))
    if r.get('pantau') in C2_PANTAU:
        k.append(('C2', f"pantau {r.get('pantau')}"))
    if r.get('status') == 'NEGATIF':
        k.append(('C3', 'kad skor NEGATIF'))
    if r.get('status') == 'GAGAL' and lama and lama.get('status') == 'GAGAL':
        k.append(('C4', f'GAGAL {C4_LARIAN} larian berturut'))
    sesi, pul, spus, mdd = (_f(r.get('t4_sesi'), 0), _f(r.get('t4_pul')), _f(r.get('t4_spus')),
                            _f(r.get('t4_mdd')))
    if sesi >= C5_SESI and pul == pul and spus == spus and pul <= spus - C5_JURANG and mdd <= C5_MDD:
        k.append(('C5', f'T4 {pul:+.1f}% lawan SPUS {spus:+.1f}% atas {int(sesi)} sesi, MDD {mdd:.1f}%'))
    return k


def kira(M, lama):
    rows = [dict(zip(M['kol'], r)) for r in M['rows']] if 'kol' in M else M['rows']
    L = {x['id']: x for x in (lama or {}).get('kaedah', [])}
    bulan_kini = str(M.get('harga_pada', ''))[:7]
    out = []
    for r in rows:
        k = nilai(r, L.get(r['id']))
        lm = L.get(r['id'])
        if k:
            bb = int(lm.get('bulan_berturut', 0)) if lm and lm.get('kod') else 0
            if lm and lm.get('bulan') == bulan_kini:
                bb = max(bb, 1)
            else:
                bb += 1
        else:
            bb = 0
        out.append(dict(id=r['id'], nama=r.get('nama', ''), keluarga=r.get('keluarga', ''),
                        status=r.get('status'), kod=[c for c, _ in k], sebab='; '.join(s for _, s in k),
                        bulan=bulan_kini, bulan_berturut=bb))
    return out


def laporan(M, out):
    from status_kad import baris
    calon = [x for x in out if x['kod']]
    cad = [x for x in calon if x['bulan_berturut'] >= BULAN_CADANG]
    L = ['# CANTAS — calon berhenti direkod (label maklumat bulanan; bukan tindakan)', '']
    L.append(f'Dijana {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC oleh `standard/cantas.py` atas `kad_skor.json` harga '
             f'{M.get("harga_pada", "–")}. Pradaftar `standard/SPEC_CANTAS.md`. **Tiada Lejar atau kad skor diubah**; '
             'cantas sebenar = keputusan pengguna dalam `koordinator/keputusan.csv`.')
    L.append('')
    L.append(baris())
    L.append('')
    L.append(f'**Calon cantas: {len(calon)} daripada {len(out)} kaedah.** Dicadangkan untuk keputusan (calon '
             f'≥ {BULAN_CADANG} bulan berturut): **{len(cad)}** — ' + (', '.join(f"`{x['id']}`" for x in cad) or 'tiada') + '.')
    L.append('')
    kira_kod = {}
    for x in calon:
        for c in x['kod']:
            kira_kod[c] = kira_kod.get(c, 0) + 1
    L.append('| Peraturan | Bilangan |')
    L.append('|---|---|')
    for c in ('C1', 'C2', 'C3', 'C4', 'C5'):
        L.append(f'| {c} | {kira_kod.get(c, 0)} |')
    L.append('')
    L.append('| Kaedah | Status kad | Peraturan | Sebab | Bulan berturut |')
    L.append('|---|---|---|---|---|')
    for x in sorted(calon, key=lambda z: (-z['bulan_berturut'], z['id'])):
        L.append(f"| `{x['id']}` {str(x['nama'])[:30]} | {x['status']} | {', '.join(x['kod'])} | {x['sebab']} | "
                 f"{x['bulan_berturut']} |")
    L.append('')
    L.append('Peraturan: C1 henti hari-0 struktur (G4 pasti gagal) · C2 pantau BERSARA/GANTUNG · C3 NEGATIF · '
             'C4 GAGAL dua larian · C5 lorong T4 ≥ 63 sesi kalah SPUS ≥ 5 mata dengan MDD ≤ -10%. Nxx dikecualikan C1.')
    return '\n'.join(L) + '\n'


def main():
    try:
        M = json.load(open(KS, encoding='utf-8'))
    except (OSError, ValueError) as e:
        print(f'kad_skor.json tiada/rosak: {e}', file=sys.stderr)
        return 1
    lama = None
    try:
        lama = json.load(open(OUT_JSON, encoding='utf-8'))
    except (OSError, ValueError):
        pass
    out = kira(M, lama)
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(dict(kini=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M'), harga_pada=M.get('harga_pada'),
                       ambang=dict(C1=[C1_HARI_BELI, C1_POSISI, C1_HARI0_PCT], C2=list(C2_PANTAU), C4=C4_LARIAN,
                                   C5=[C5_SESI, C5_JURANG, C5_MDD]), kaedah=out), f, ensure_ascii=False)
    with open(OUT_MD, 'w', encoding='utf-8') as f:
        f.write(laporan(M, out))
    n = sum(1 for x in out if x['kod'])
    print(f'CANTAS: {n}/{len(out)} calon; {OUT_MD}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
