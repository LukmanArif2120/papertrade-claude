"""Tulis `data/robot/larian.json`: larian GitHub Actions 4 hari terakhir untuk tab Robot dashboard.

Dijalankan dalam `harian.yml` (sebelum langkah commit, `continue-on-error`) dengan token GITHUB_TOKEN
(`permissions: actions: read`). Sesi berjadual Claude yang menolak db tiada alat GitHub, jadi hanya Actions boleh
membaca senarai larian; fail kecil ini (~30 KB) ialah jambatannya. Dibaca oleh `robot_kerja.py` melalui `jana_db.py`.

Tidak pernah gagal: sebarang ralat dicetak sebagai amaran dan fail lama dikekalkan.

Guna (Actions):  GH_TOKEN=${{ github.token }} python3 BacktestShariah2/standard/robot_larian.py
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

BS2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
KELUAR = os.path.join(BS2, 'data', 'robot', 'larian.json')
HARI = 4


def _get(api, path, token):
    req = urllib.request.Request(api + path, headers={
        'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'papertrade-robot-kerja'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def baris(r):
    return [r.get('path', '').split('/')[-1], r.get('run_started_at') or r.get('created_at'), r.get('updated_at'),
            r.get('status'), r.get('conclusion'), r.get('event')]


def kumpul(api, repo, token, kini=None):
    kini = kini or datetime.now(timezone.utc)
    had = (kini - timedelta(days=HARI)).strftime('%Y-%m-%dT%H:%M:%SZ')
    runs = {}
    for halaman in range(1, 6):
        d = _get(api, f'/repos/{repo}/actions/runs?per_page=100&page={halaman}', token)
        rr = d.get('workflow_runs') or []
        for r in rr:
            runs[r['id']] = r
        if not rr or min((r.get('created_at') or '') for r in rr) < had:
            break
    # larian terakhir setiap workflow robot (yang jarang berjalan: mingguan, Ahad, Sabtu)
    import robot_kerja
    for _, _, _, _, sumber, *_ in robot_kerja.KATALOG:
        if not sumber.startswith('wf:'):
            continue
        try:
            d = _get(api, f'/repos/{repo}/actions/workflows/{sumber[3:]}/runs?per_page=2', token)
            for r in d.get('workflow_runs') or []:
                runs.setdefault(r['id'], r)
        except Exception as e:  # workflow tiada / dinamakan semula: robot itu kekal tanpa larian
            print(f'::warning::robot_larian: {sumber[3:]}: {e}')
    nama = {s[4][3:] for s in robot_kerja.KATALOG if s[4].startswith('wf:')}
    simpan = [baris(r) for r in runs.values() if r.get('path', '').split('/')[-1] in nama]
    # hadkan: semua larian dalam tetingkap + satu terkini setiap workflow di luar tetingkap
    dalam = [b for b in simpan if (b[1] or '') >= had]
    luar = {}
    for b in simpan:
        if (b[1] or '') < had and (b[0] not in luar or b[1] > luar[b[0]][1]):
            luar[b[0]] = b
    akhir = sorted(dalam + list(luar.values()), key=lambda b: (b[1] or '', b[0]))
    return dict(dibina=kini.strftime('%Y-%m-%dT%H:%M:%SZ'), sumber='GitHub Actions API (robot_larian.py)',
                hari=HARI, lajur=['workflow', 'mula', 'akhir', 'status', 'hasil', 'peristiwa'], runs=akhir)


def main():
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY')
    api = os.environ.get('GITHUB_API_URL', 'https://api.github.com')
    if not token or not repo:
        print('::warning::robot_larian: GH_TOKEN/GITHUB_REPOSITORY tiada; fail lama dikekalkan')
        return 0
    try:
        d = kumpul(api, repo, token)
    except Exception as e:
        print(f'::warning::robot_larian gagal ({e}); fail lama dikekalkan')
        return 0
    os.makedirs(os.path.dirname(KELUAR), exist_ok=True)
    with open(KELUAR, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
        f.write('\n')
    print(f'robot_larian: {len(d["runs"])} larian -> {os.path.relpath(KELUAR)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
