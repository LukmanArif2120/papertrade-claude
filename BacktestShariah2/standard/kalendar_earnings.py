# kalendar_earnings.py — kalendar tarikh earnings gabungan (audit 23 Okt 2026) bagi isi semula QR dan tarikh earnings sebenar.
# Sumber (keutamaan menurun, tarikh sama digabung):
#   1. Nasdaq: data/pemangkin/tarikh_pendapatan.csv (sejarah) + earnings_nasdaq.json (lalu/seterusnya)
#   2. yfinance: data/pemangkin/sejarah/eps.csv (tarikh; eps_sebenar ada = sudah dilapor)
#   3. Tambahan disahkan (FMP / Moomoo / laman IR syarikat): data/pemangkin/tarikh_pendapatan_tambahan.csv
#      (ticker,tarikh,sumber,catatan) bagi saham yang tidak diliputi 1–2 (kebanyakan ADR dan syarikat kecil asing)
# Tarikh seterusnya dipercayai jika <= DEKAT hari selepas rujukan, atau siri berterusan (jarak laporan lalu -> seterusnya
# <= 1.25 × jarak laporan terpanjang syarikat dalam 3 tahun; suku tahunan ~91 hari, separuh tahunan sehingga ~215 hari).
import csv, json, os
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
PEMANGKIN = os.path.join(BS2, 'data', 'pemangkin')
SELANG_MAKS = 200
DEKAT = 80          # laporan seterusnya <= 80 hari selepas rujukan: tiada laporan suku lain mungkin di antaranya


def _d(x):
    try:
        return date.fromisoformat(str(x)[:10])
    except (TypeError, ValueError):
        return None


def muat(folder=PEMANGKIN):
    """-> {ticker: {date: sumber}}"""
    K = {}

    def tambah(t, d, s):
        if t and d:
            K.setdefault(t, {}).setdefault(d, s)
    p = os.path.join(folder, 'tarikh_pendapatan.csv')
    if os.path.exists(p):
        with open(p, newline='', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                tambah(r['ticker'], _d(r['d0']), 'Nasdaq')
    p = os.path.join(folder, 'earnings_nasdaq.json')
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            nas = json.load(f)
        for t, e in (nas.get('saham') or {}).items():
            for k in ('lalu', 'seterusnya'):
                tambah(t, _d(e.get(k)), 'Nasdaq')
    p = os.path.join(folder, 'sejarah', 'eps.csv')
    if os.path.exists(p):
        with open(p, newline='', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                tambah(r['ticker'], _d(r['tarikh']), 'yfinance')
    p = os.path.join(folder, 'tarikh_pendapatan_tambahan.csv')
    if os.path.exists(p):
        with open(p, newline='', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                tambah(r['ticker'], _d(r['tarikh']), r.get('sumber') or 'tambahan')
    return K


def lalu(K, t, D):
    """Earnings terakhir sebelum D -> (date, sumber) atau (None, None)."""
    x = sorted(d for d in K.get(t, {}) if d < D)
    return (x[-1], K[t][x[-1]]) if x else (None, None)


def kitaran(K, t, D):
    """Jarak laporan TERPANJANG (> 40 hari) dalam 3 tahun sebelum D (separuh tahun: Jul -> Feb ~215 hari); None jika < 2 jarak."""
    x = sorted(d for d in K.get(t, {}) if D - timedelta(days=3 * 366) < d < D)
    j = [(b - a).days for a, b in zip(x, x[1:]) if (b - a).days > 40]
    return max(j) if len(j) >= 2 else None


def seterusnya(K, t, D):
    """Earnings pertama pada/selepas D yang boleh dipercayai -> (date, sumber) atau (None, sebab).
    Diterima jika (a) dalam DEKAT hari selepas D (tiada ruang untuk laporan lain di antaranya), atau (b) siri berterusan:
    laporan lalu ada dan jarak laporan lalu -> seterusnya <= 1.25 × jarak terpanjang syarikat 3 tahun (tiada sejarah: SELANG_MAKS)."""
    akan = sorted(d for d in K.get(t, {}) if d >= D)
    if not akan:
        return None, 'tiada tarikh akan datang dalam sumber'
    if (akan[0] - D).days <= DEKAT:
        return akan[0], K[t][akan[0]]
    sb, _ = lalu(K, t, D)
    kt = kitaran(K, t, D)
    had = int(1.25 * kt) if kt else SELANG_MAKS
    if sb is None or (akan[0] - sb).days > had:
        return None, f'siri tidak berterusan (laporan lalu tiada / jarak > {had} hari)'
    return akan[0], K[t][akan[0]]
