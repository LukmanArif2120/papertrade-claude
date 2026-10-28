# Penjaga jadual GitHub Actions (`.github/workflows/penjaga_jadual.yml`): jadual cron GitHub boleh lewat 2–4 jam atau
# digugurkan (17–19 Okt 2026: beli.yml dan petang.yml tidak pernah dicetus). Bagi setiap workflow berjadual di JAGA,
# cetusan cron terkini yang sudah lewat LEWAT_MIN minit dan masih dalam had masa dicari; jika tiada larian (apa-apa
# event/status) dicipta sejak cetusan itu, workflow_dispatch dicetus. Semua workflow dijaga idempoten dan ada
# concurrency, jadi larian berganda (jadual lewat tiba selepas dispatch) selamat. Tanpa LLM; tiada fail repo ditulis.
#
# Had masa (elak data salah):
#   buka  = sebelum 13:00 UTC seterusnya (sebelum buka AS; harga/RS/gred kumpulan/skrin tanpa bar separa)
#   petang < 9:15 NY (petang.yml dispatch memintas gerbang 9:20 NY miliknya), beli < 16:45 NY (gerbang beli 9:31–17:00 NY)
#
# Guna:
#   python3 penjaga_jadual.py [--cuba]      (GITHUB_TOKEN, GITHUB_REPOSITORY; --cuba = cetak keputusan, tiada dispatch)
import argparse, json, os, re, sys, urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

NY = ZoneInfo('America/New_York')
LEWAT_MIN = 30           # minit selepas cetusan sebelum penjaga bertindak (beri peluang jadual GitHub yang lewat)
TINJAU_JAM = 16          # cetusan lebih lama daripada ini diabaikan
AWAL_MIN = 2             # larian dicipta sedikit sebelum cetusan masih dikira
JAGA = {
    'harga_harian.yml': 'buka', 'skrin_tv.yml': 'buka', 'rs_pasaran.yml': 'buka', 'gred_kumpulan.yml': 'buka',
    'lejar.yml': 'buka', 'harian.yml': 'buka', 'petang.yml': ('ny', 9, 15), 'beli.yml': ('ny', 16, 45),
    'edgar.yml': 'buka', 'fundamental_sec.yml': 'buka', 'senarai_bursa.yml': 'buka',
    'autotune_suku.yml': 'buka',   # suku-tahunan; pintu workflow menapis hari > 7 (termasuk dispatch penjaga)
}


def medan(teks, lo, hi):
    """Satu medan cron -> set nilai (sokong *, a-b, a,b, */n, a-b/n)."""
    nilai = set()
    for bah in teks.split(','):
        bah, _, langkah = bah.partition('/')
        langkah = int(langkah) if langkah else 1
        if bah == '*':
            a, b = lo, hi
        elif '-' in bah:
            a, b = (int(x) for x in bah.split('-'))
        else:
            a = b = int(bah)
        nilai.update(range(a, b + 1, langkah))
    return nilai


def cetusan(cron, mula, akhir):
    """Senarai masa UTC (mula < t <= akhir) yang dipadankan cron 5 medan (semantik ATAU dom/dow seperti cron)."""
    mi, ja, dom, bul, dow = cron.split()
    M, J, B = medan(mi, 0, 59), medan(ja, 0, 23), medan(bul, 1, 12)
    D, W = medan(dom, 1, 31), {x % 7 for x in medan(dow, 0, 7)}
    hasil = []
    hari = mula.replace(hour=0, minute=0, second=0, microsecond=0)
    while hari <= akhir:
        cw = (hari.weekday() + 1) % 7
        if dom == '*' or dow == '*':
            ok = hari.day in D and cw in W
        else:
            ok = hari.day in D or cw in W
        if ok and hari.month in B:
            for j in sorted(J):
                for m in sorted(M):
                    t = hari.replace(hour=j, minute=m)
                    if mula < t <= akhir:
                        hasil.append(t)
        hari += timedelta(days=1)
    return hasil


def had_masa(jenis, t):
    """Masa UTC selepasnya cetusan t tidak lagi wajar didispatch."""
    if jenis == 'buka':
        h = t.replace(hour=13, minute=0, second=0, microsecond=0)
        return h if h > t else h + timedelta(days=1)
    _, jam, minit = jenis
    return t.astimezone(NY).replace(hour=jam, minute=minit, second=0, microsecond=0).astimezone(timezone.utc)


def baca_cron(laluan):
    with open(laluan, encoding='utf-8') as f:
        return re.findall(r"""^\s*-\s*cron:\s*['"]([^'"]+)['"]""", f.read(), re.M)


def sasaran(crons, jenis, kini):
    """Cetusan terkini yang perlu dipastikan berlaku (sudah lewat LEWAT_MIN, masih dalam had), atau None."""
    calon = [t for c in crons for t in cetusan(c, kini - timedelta(hours=TINJAU_JAM), kini - timedelta(minutes=LEWAT_MIN))
             if kini < had_masa(jenis, t)]
    return max(calon) if calon else None


def keputusan(crons, jenis, dicipta, kini):
    """dicipta: masa cipta larian workflow itu (UTC). Pulang (cetusan, perlu_dispatch)."""
    t = sasaran(crons, jenis, kini)
    if t is None:
        return None, False
    return t, not any(d >= t - timedelta(minutes=AWAL_MIN) for d in dicipta)


def api(kaedah, url, token, data=None):
    req = urllib.request.Request(url, method=kaedah, data=json.dumps(data).encode() if data is not None else None,
                                 headers={'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json',
                                          'X-GitHub-Api-Version': '2022-11-28'})
    with urllib.request.urlopen(req, timeout=30) as r:
        teks = r.read()
        return json.loads(teks) if teks else None


def masa(s):
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cuba', action='store_true', help='cetak keputusan sahaja, tiada dispatch')
    ap.add_argument('--folder', default='.github/workflows')
    ap.add_argument('--ref', default='main')
    a = ap.parse_args()
    token, repo = os.environ['GITHUB_TOKEN'], os.environ['GITHUB_REPOSITORY']
    asas = f'https://api.github.com/repos/{repo}/actions/workflows'
    kini = datetime.now(timezone.utc)
    ralat = 0
    for fail, jenis in JAGA.items():
        crons = baca_cron(os.path.join(a.folder, fail))
        t = sasaran(crons, jenis, kini)
        if t is None:
            print(json.dumps(dict(workflow=fail, status='tiada cetusan perlu disemak')))
            continue
        try:
            dari = (t - timedelta(minutes=AWAL_MIN)).strftime('%Y-%m-%dT%H:%M:%SZ')
            runs = api('GET', f'{asas}/{fail}/runs?per_page=30&created=%3E%3D{dari}', token)['workflow_runs']
            _, perlu = keputusan(crons, jenis, [masa(r['created_at']) for r in runs], kini)
            rekod = dict(workflow=fail, cetusan=t.strftime('%Y-%m-%d %H:%M UTC'), larian_sejak=len(runs))
            if perlu and not a.cuba:
                api('POST', f'{asas}/{fail}/dispatches', token, {'ref': a.ref})
                rekod['status'] = 'DISPATCH (jadual GitHub tidak dicetus)'
            else:
                rekod['status'] = ('perlu dispatch (cuba)' if perlu else 'ok')
            print(json.dumps(rekod))
        except Exception as e:      # satu workflow gagal tidak menghalang yang lain
            ralat += 1
            print(json.dumps(dict(workflow=fail, ralat=str(e))))
    sys.exit(1 if ralat else 0)


if __name__ == '__main__':
    main()
