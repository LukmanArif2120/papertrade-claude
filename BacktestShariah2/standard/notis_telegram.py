# notis_telegram.py — notifikasi Telegram daripada GitHub Actions (.github/workflows/notis.yml).
# Rahsia repo: TELEGRAM_TOKEN (token bot daripada @BotFather) dan TELEGRAM_TO (chat id anda). Jika tiada, skrip
# hanya mencetak mesej dan keluar 0 (tiada kegagalan workflow).
# Subarahan:
#   komit     : baca peristiwa push (GITHUB_EVENT_PATH); hantar baris pertama commit rutin (6:02, imbas, beli, log)
#   gagal     : workflow_run gagal -> amaran (nama workflow, pautan larian)
#   pengawas  : --jenis pagi|imbas|beli --mula HH:MM (UTC) ; jika hari dagangan NYSE dan tiada commit rutin sejak
#               masa mula itu -> amaran (sauh tetap, jadi kelewatan jadual GitHub tidak menyebabkan amaran palsu)
#   hantar    : --teks "…" (ujian)
import argparse, json, os, re, subprocess, sys, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

DASHBOARD = 'https://claude.ai/code/artifact/12bb853e-34ef-4d6c-885d-10f46984437e'
RUTIN = [('pagi', re.compile(r'^(Kemas kini 6:02 pagi|Log 6:02 pagi)')),
         ('imbas', re.compile(r'^Imbas\b')),
         ('beli', re.compile(r'^Beli 9:35 NY'))]
LABEL = {'pagi': 'Kemas kini 6:02 pagi MYT', 'imbas': 'Imbas 7:47 malam MYT', 'beli': 'Beli maya 9:35 NY'}
HAD = 4000  # had Telegram 4096 aksara


def jenis_rutin(mesej):
    baris = (mesej or '').strip().splitlines()[0] if (mesej or '').strip() else ''
    for j, rx in RUTIN:
        if rx.search(baris):
            return j, baris
    return None, baris


def mesej_komit(event):
    out = []
    for c in event.get('commits') or []:
        j, baris = jenis_rutin(c.get('message'))
        if j:
            out.append(f'• {baris}')
    if not out:
        return None
    teks = 'Papertrade C (maya) — kemas kini repo\n' + '\n'.join(out) + f'\n\nDashboard: {DASHBOARD}'
    return teks[:HAD]


def mesej_gagal(event):
    wr = event.get('workflow_run') or {}
    if wr.get('conclusion') not in ('failure', 'timed_out', 'startup_failure'):
        return None
    _, komit = jenis_rutin((wr.get('head_commit') or {}).get('message'))
    return (f"⚠️ Workflow GAGAL: {wr.get('name', '?')} ({wr.get('conclusion')})\n"
            f"Cabang {wr.get('head_branch', '?')} · {komit[:150]}\n"
            f"{wr.get('html_url', '')}")[:HAD]


def hari_dagangan_ny(tarikh):
    try:
        import exchange_calendars as xc
        return bool(xc.get_calendar('XNYS').is_session(tarikh.strftime('%Y-%m-%d')))
    except ImportError:
        return tarikh.weekday() < 5


def sauh(mula, sekarang):
    """Masa mula rutin terkini (UTC) bagi 'HH:MM': hari ini jika sudah lepas, selainnya semalam.
    Jadual GitHub boleh lewat beberapa jam; sauh tetap memastikan commit rutin tetap dijumpai."""
    jam, minit = (int(x) for x in mula.split(':'))
    t = sekarang.replace(hour=jam, minute=minit, second=0, microsecond=0)
    return t if t <= sekarang else t - timedelta(days=1)


def ada_komit(jenis, sejak, repo='.'):
    log = subprocess.run(['git', '-C', repo, 'log', f"--since={sejak.strftime('%Y-%m-%dT%H:%M:%SZ')}", '--format=%s'],
                         capture_output=True, text=True, check=False).stdout
    rx = dict(RUTIN)[jenis]
    return any(rx.search(b) for b in log.splitlines())


def mesej_pengawas(jenis, mula, sekarang=None, repo='.', semak_komit=None):
    sekarang = sekarang or datetime.now(timezone.utc)
    s = sauh(mula, sekarang)
    # tarikh sesi NYSE yang berkaitan = tarikh New York pada masa sauh (sauh dipilih jauh dari tengah malam NY)
    if not hari_dagangan_ny((s - timedelta(hours=4)).date()):
        return None
    if (semak_komit or ada_komit)(jenis, s, repo):
        return None
    return (f"⚠️ {LABEL[jenis]}: tiada commit rutin sejak {s.strftime('%d %b %H:%M')} UTC.\n"
            f"Semak sesi rutin dan connector (Moomoo/SST) di claude.ai.\nDashboard: {DASHBOARD}")


def hantar(teks):
    token, ke = os.environ.get('TELEGRAM_TOKEN', '').strip(), os.environ.get('TELEGRAM_TO', '').strip()
    if not teks:
        print('tiada mesej')
        return 0
    if not token or not ke:
        print('Telegram belum disediakan (TELEGRAM_TOKEN / TELEGRAM_TO tiada). Mesej:\n' + teks)
        return 0
    data = urllib.parse.urlencode({'chat_id': ke, 'text': teks, 'disable_web_page_preview': 'true'}).encode()
    req = urllib.request.Request(f'https://api.telegram.org/bot{token}/sendMessage', data=data, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            ok = json.load(r).get('ok')
    except Exception as e:
        print(f'gagal hantar Telegram: {type(e).__name__}', file=sys.stderr)
        return 1
    print('dihantar' if ok else 'Telegram menolak mesej')
    return 0 if ok else 1


def baca_event():
    p = os.environ.get('GITHUB_EVENT_PATH')
    return json.load(open(p, encoding='utf-8')) if p and os.path.exists(p) else {}


def main(argv=None):
    ap = argparse.ArgumentParser(description='Notifikasi Telegram untuk rutin papertrade')
    sp = ap.add_subparsers(dest='cmd', required=True)
    sp.add_parser('komit')
    sp.add_parser('gagal')
    g = sp.add_parser('pengawas')
    g.add_argument('--jenis', required=True, choices=['pagi', 'imbas', 'beli'])
    g.add_argument('--mula', required=True, help='masa mula rutin (UTC, HH:MM); commit dicari sejak masa ini')
    h = sp.add_parser('hantar')
    h.add_argument('--teks', required=True)
    a = ap.parse_args(argv)
    if a.cmd == 'komit':
        return hantar(mesej_komit(baca_event()))
    if a.cmd == 'gagal':
        return hantar(mesej_gagal(baca_event()))
    if a.cmd == 'pengawas':
        return hantar(mesej_pengawas(a.jenis, a.mula))
    return hantar(a.teks)


if __name__ == '__main__':
    sys.exit(main())
