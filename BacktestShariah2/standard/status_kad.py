"""Satu baris status kad skor untuk diletakkan di atas SETIAP laporan (audit 7 Nov 2026: lima laporan memberi lima
jawapan berbeza — KAD_SKOR 0 lulus, LIFT 5, KAEDAH_TERBAIK "1 lulus", PENGANALISIS "M153 +5.22% sebulan" lawan SPY).

Laporan lain boleh terus mengukur perkara masing-masing, tetapi mesti menyatakan bahawa keputusan wang sebenar hanya
datang daripada kad skor (`standard/kad_skor.py`, `laporan/KAD_SKOR.md`). Membaca `data/analisis/kad_skor.json`
(larian malam sebelumnya jika laporan ini dijana dahulu); tidak pernah gagal — jika fail tiada, ia berkata begitu.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
KS = os.environ.get('KS_JSON', os.path.join(BS2, 'data', 'analisis', 'kad_skor.json'))
TERTIB = ('TERBUKTI', 'CALON', 'BELUM CUKUP', 'GAGAL', 'NEGATIF')


def baris(path=None):
    """Satu perenggan Markdown: bilangan status, tarikh data, dan peraturan wang sebenar."""
    try:
        with open(path or KS, encoding='utf-8') as f:
            M = json.load(f)
    except (OSError, ValueError):
        return ('> **Status keputusan:** kad skor belum dijana (`standard/kad_skor.py`). Hanya status TERBUKTI '
                'dalam `laporan/KAD_SKOR.md` layak untuk wang sebenar; laporan ini BUKAN keputusan.')
    k = M.get('kira') or {}
    s = ' · '.join(f'{x} {k.get(x, 0)}' for x in TERTIB)
    rj = M.get('rejim') or {}
    r = f" Rejim QQQ {rj.get('label')} sejak {rj.get('sejak')}." if rj.get('label') else ''
    return (f"> **Status keputusan (kad skor, harga {M.get('harga_pada', '–')}):** {s}.{r} Hanya **TERBUKTI** "
            'layak untuk wang sebenar (`laporan/KAD_SKOR.md`); nombor dalam laporan ini BUKAN keputusan dan tidak '
            'boleh dibaca sebagai pangkat untuk wang sebenar.')
