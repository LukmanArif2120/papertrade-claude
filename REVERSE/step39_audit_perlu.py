"""Jana `REVERSE/AUDIT_PERLU.md` daripada `REVERSE/audit_perlu.json`.

Status `PERLU:<x>` dalam registry N ialah teks yang DITAIP TANGAN semasa baris didaftar. Ia
tidak dikira daripada apa yang repo ada, dan `ujian/test_registry_n.py` hanya menyemak
bentuk rentetan (`test_status_sah`, `test_perlu_ada_nama_indikator`) — **tiada apa-apa yang
menyemak sama ada indikator itu benar-benar tiada**. Jadi label itu satu DAKWAAN, bukan
ukuran, dan audit ini mengukurnya.

`audit_perlu.json` = keluaran mentah audit 2 Nov 2026: 18 agen (9 pengelas + 9 penyangkal
adversarial), 2.77 juta token, 454 panggilan alat, setiap dakwaan "boleh diuji dengan apa
yang repo sudah ada" diserang oleh agen kedua yang cuba menolaknya. 12 daripada 47 dakwaan
DITOLAK dan dikelas semula.

Jadual di bawah dijana, bukan ditaip — supaya ia tidak boleh hanyut daripada JSON itu.

Guna: python3 REVERSE/step39_audit_perlu.py
"""
import collections
import csv
import json
from pathlib import Path

AKAR = Path(__file__).resolve().parents[1]
RV = AKAR / 'REVERSE'
REG = AKAR / 'BacktestShariah2' / 'data' / 'registry_N.csv'

KELAS = [
    ('KOD_SAHAJA', 'Hanya KOD yang belum ditulis',
     'Fungsi tulen bagi data yang repo SUDAH ada (OHLCV harian 3,260 ticker, atau 67 lajur '
     'panel). Tiada halangan data langsung.'),
    ('SUDAH_ADA', 'Label SALAH — datanya ADA dalam repo',
     'Data wujud dan dijejak git. Yang tiada hanyalah paip yang menyambungkannya ke panel.'),
    ('DATA_LUAR', 'Benar-benar disekat data luar',
     'Perlukan sumber yang repo tiada dan tidak boleh diterbitkan daripada apa yang ada.'),
    ('BUKAN_INDIKATOR', 'Bukan indikator masuk langsung',
     'Paksi lain (saiz, urutan, pembinaan portfolio) atau halangan sumber. Label `PERLU` '
     'pada lajur yang sama membuatnya kelihatan seperti masalah data sedangkan bukan.'),
]


def main():
    A = json.loads((RV / 'audit_perlu.json').read_text(encoding='utf-8'))
    T = A['token']
    R = list(csv.DictReader(open(REG, encoding='utf-8')))
    nb = collections.Counter(r['status'].split(':', 1)[1]
                             for r in R if r['status'].startswith('PERLU:'))
    baris = {}
    for r in R:
        if r['status'].startswith('PERLU:'):
            baris.setdefault(r['status'].split(':', 1)[1], []).append(r['id'])

    n_reg = len(R)
    n_perlu = sum(nb.values())
    kira_baris = collections.Counter()
    for t in T:
        kira_baris[t['kelas_akhir']] += nb[t['token']]

    L = [f'# Audit status `PERLU` registry N — {len(T)} token, {n_perlu} baris', '',
         'Dijana oleh `REVERSE/step39_audit_perlu.py` daripada `REVERSE/audit_perlu.json`; '
         'jangan sunting dengan tangan.', '',
         '## Mengapa audit ini wujud', '',
         'Status `PERLU:<x>` **ditaip tangan** dalam jadual tuple '
         '`BacktestShariah2/standard/registry_n.py` semasa baris itu didaftar. Ia **tidak '
         'dikira** daripada apa yang repo sebenarnya ada, dan `ujian/test_registry_n.py` '
         'hanya menyemak **bentuk** rentetan itu:', '',
         '- `test_status_sah` — mesti `DIUJI`, `SEDIA`, atau bermula `PERLU:`',
         '- `test_perlu_ada_nama_indikator` — mesti ada teks selepas titik bertindih', '',
         '**Tiada satu pun ujian menyemak sama ada indikator itu benar-benar tiada.** Jadi '
         'setiap label `PERLU` ialah dakwaan yang tidak pernah disemak sejak hari ia ditaip.',
         '',
         f'Audit: 18 agen (9 pengelas + 9 **penyangkal adversarial**), '
         f'{A["meta"]["token_subagen"]:,} token, {A["meta"]["panggilan_alat"]} panggilan '
         'alat. Setiap dakwaan "boleh diuji dengan apa yang repo sudah ada" diserang oleh '
         'agen kedua yang diarah **menolaknya**, dengan lalai `ditolak=true` jika ia tidak '
         f'dapat disahkan. **{sum(1 for t in T if t.get("ditolak"))} dakwaan DITOLAK** dan '
         'dikelas semula.', '',
         '## Keputusan', '',
         '| Kelas | Token | Baris registry |', '|---|--:|--:|']
    for k, nama, _ in KELAS:
        g = [t for t in T if t['kelas_akhir'] == k]
        L.append(f'| **{nama}** (`{k}`) | {len(g)} | **{kira_baris[k]}** |')
    L += [f'| | **{len(T)}** | **{n_perlu}** |', '',
          f'Registry penuh: {n_reg} baris '
          f'({sum(1 for r in R if r["status"] == "DIUJI")} DIUJI · {n_perlu} PERLU · '
          f'{sum(1 for r in R if r["status"] == "SEDIA")} SEDIA).', '']

    for k, nama, cerita in KELAS:
        g = sorted([t for t in T if t['kelas_akhir'] == k],
                   key=lambda x: (-nb[x['token']], -x.get('baris_kod', 0)))
        if not g:
            continue
        L += [f'## {nama} — {len(g)} token, {kira_baris[k]} baris', '', cerita, '',
              '| Token | Baris | ID | ~baris kod | Yakin | Nota |',
              '|---|--:|---|--:|:-:|---|']
        for t in g:
            y = {'tinggi': 'T', 'sederhana': 'S', 'rendah': 'R'}.get(t.get('keyakinan'), '?')
            tol = ' **[dikelas semula oleh penyangkal]**' if t.get('ditolak') else ''
            ids = ' '.join(baris.get(t['token'], []))
            bk = t.get('baris_kod', 0)
            L.append(f'| `{t["token"]}` | {nb[t["token"]]} | {ids} | '
                     f'{bk if bk else "–"} | {y} | {t["sebab"].strip()}{tol} |')
        L.append('')

    tol = [t for t in T if t.get('ditolak')]
    if tol:
        L += ['## Dakwaan yang penyangkal TOLAK', '',
              'Setiap satu ialah kes di mana pengelas berkata "boleh diuji" dan penyangkal '
              'membuktikan sebaliknya. Ini bahagian audit yang paling bernilai: tanpa '
              'pusingan kedua, kesemua ini akan masuk sebagai kerja yang kelihatan murah.',
              '']
        for t in sorted(tol, key=lambda x: x['token']):
            L += [f'### `{t["token"]}` — {t["kelas"]} → **{t["kelas_akhir"]}**', '',
                  t.get('hujah_penyangkal', '').strip(), '']

    (RV / 'AUDIT_PERLU.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print(f'AUDIT_PERLU.md: {len(T)} token, {n_perlu} baris, '
          f'{dict(kira_baris)}, {len(tol)} ditolak')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
