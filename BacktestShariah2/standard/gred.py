# Gred calon dan posisi papertrade: Sektor, Industri, RS, Pemangkin, QR (jarak ke laporan suku/earnings).
# Peraturan dan bukti: standard/tugasan_v3.md §8. Gred direkod pada hari isyarat; prestasi setiap gred dinilai
# selepas >= 20 dagangan tertutup (dashboard Prestasi > Prestasi ikut gred).
#
# Guna (imbasan 8:02 malam):
#   python3 gred.py tambah --csv papertrade/senarai_beli.csv --harga <folder harga_A/B.csv> \
#       --sektor papertrade/sektor.csv --acara <market_events.json> --pemangkin <pemangkin.json> --tarikh YYYY-MM-DD
#   (ulang untuk papertrade/watchlist.csv; --pemangkin pilihan)
#   python3 gred.py kumpul --folder <fail mentah alat> --csv papertrade/senarai_beli.csv papertrade/watchlist.csv \
#       --keluar papertrade/pemangkin.json --tarikh YYYY-MM-DD      (Berita Panas; lihat jadual/imbas_2002.md)
import sys, os, re, csv, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datetime import date, timedelta

import numpy as np
import pandas as pd

GRED = ['A', 'B', 'C', 'D', 'E']
MATA = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
TIADA = '–'
LAJUR = ['sektor_us', 'industri_us', 'gred_sektor', 'skor_sektor', 'gred_industri', 'skor_industri', 'rs_rating', 'gred_rs',
         'gred_pemangkin', 'mata_pemangkin', 'pemangkin', 'pemangkin_url', 'tarikh_earnings', 'hari_ke_earnings', 'sumber_earnings', 'gred_qr',
         'gred_keseluruhan', 'gred_pada']


# ---------- RS rating (gaya IBD, 1–99) ----------
def rs_rating(close):
    """close: DataFrame (index tarikh, lajur ticker). Pulangkan Series RS 1–99 pada bar terakhir.
    Skor = 40% pulangan 63 hari terkini + 20% setiap satu daripada tiga suku sebelumnya; pangkat persentil
    berbanding semua saham dalam stor harga. Saham dengan < 253 bar tiada RS."""
    c = close.sort_index()
    if len(c) < 253:
        return pd.Series(dtype=float)
    a = c.iloc[-1]
    q = [c.iloc[-64], c.iloc[-127], c.iloc[-190], c.iloc[-253]]
    skor = 0.4 * (a / q[0] - 1) + 0.2 * (q[0] / q[1] - 1) + 0.2 * (q[1] / q[2] - 1) + 0.2 * (q[2] / q[3] - 1)
    skor = skor.replace([np.inf, -np.inf], np.nan).dropna()
    return (skor.rank(pct=True) * 98 + 1).round().astype(int).clip(1, 99)


def gred_rs(rs):
    """Ujian 2019–2026 (431 saham, pulangan 21 hari): RS 90+ purata +4.2% lawan +1.6–2.2% bagi gred lain,
    dan mendahului setiap tahun. Sempadan ikut ujian itu."""
    if rs is None or (isinstance(rs, float) and np.isnan(rs)):
        return TIADA
    return 'A' if rs >= 90 else 'B' if rs >= 80 else 'C' if rs >= 60 else 'D' if rs >= 40 else 'E'


# ---------- Sektor / Industri (skor panas SST, 0–100) ----------
def gred_kumpulan(skor):
    """Ujian 13 Okt 2026: skor panas/fasa sektor TIDAK meramal pulangan 1–3 bulan. Gred direkod untuk diuji
    semula dalam papertrade, bukan penapis."""
    if skor is None or (isinstance(skor, float) and np.isnan(skor)):
        return TIADA
    return 'A' if skor >= 80 else 'B' if skor >= 60 else 'C' if skor >= 40 else 'D' if skor >= 20 else 'E'


def peta_pasaran(path_csv):
    """sektor_pasaran.csv (seluruh pasaran AS) -> ({sektor: skor}, {industri: skor}) snapshot terkini."""
    return peta_sektor(path_csv)


def peta_sektor(path_csv):
    """sektor.csv -> ({sektor: skor_panas}, {industri: skor_panas}) bagi snapshot terkini."""
    rows = list(csv.DictReader(open(path_csv, newline='', encoding='utf-8')))
    if not rows:
        return {}, {}
    akhir = max(r['tarikh'] for r in rows)
    sek, ind = {}, {}
    for r in rows:
        if r['tarikh'] != akhir:
            continue
        try:
            v = float(r['skor_panas'])
        except (TypeError, ValueError):
            continue
        (sek if r['jenis'] == 'Sektor' else ind)[r['nama']] = v
    return sek, ind


# ---------- QR: jarak ke laporan suku (earnings) ----------
def hari_dagangan(dari, ke):
    """Bilangan hari bekerja (Isn–Jum) selepas `dari` hingga `ke` (anggaran hari dagangan; cuti diabaikan)."""
    if ke <= dari:
        return 0
    return int(np.busday_count(dari + timedelta(days=1), ke + timedelta(days=1)))


def gred_qr(hari):
    """Pegangan swing ~20 hari dagangan: makin jauh earnings, makin kecil risiko jurang harga semasa pegang.
    hari=None bermaksud tiada earnings dalam tetingkap 30 hari kalendar (≈ 21 hari dagangan) -> A."""
    if hari is None:
        return 'A'
    return 'A' if hari > 21 else 'B' if hari > 15 else 'C' if hari > 10 else 'D' if hari > 5 else 'E'


def peta_earnings(path_json, hari_ini):
    """Fail keputusan SST market_events (daysLookahead 30) -> {ticker: tarikh earnings terdekat >= hari ini}."""
    d = json.load(open(path_json, encoding='utf-8'))
    if isinstance(d, list) and d and isinstance(d[0], dict) and 'text' in d[0]:
        d = json.loads(d[0]['text'])
    rows = d.get('data', {}).get('data', []) if isinstance(d, dict) else d
    out = {}
    for r in rows:
        if r.get('eventType') != 'EARNINGS':
            continue
        try:
            t = date.fromisoformat(r['eventDate'][:10])
        except (KeyError, ValueError):
            continue
        k = r.get('ticker')
        if k and t >= hari_ini and (k not in out or t < out[k]):
            out[k] = t
    return out


def ringkas_earnings(path_json, hari_ini):
    """Fail Moomoo quote_financials_earnings_price_history -> dict:
       earnings_lalu_tarikh, earnings_lalu_hari (hari dagangan sejak), earnings_gerak_pct (reaksi tutup hari
       pertama selepas pengumuman lawan tutup sebelumnya), earnings_anggaran (lalu + 91 hari)."""
    d = json.load(open(path_json, encoding='utf-8'))
    if isinstance(d, list) and d and isinstance(d[0], dict) and 'text' in d[0]:
        d = json.loads(d[0]['text'])
    rec = d.get('data', {}).get('records', [])
    lalu = [r for r in rec if r.get('pub_trading_day_str') and r['pub_trading_day_str'] <= hari_ini.isoformat()]
    if not lalu:
        return {}
    pub = max(r['pub_trading_day_str'] for r in lalu)
    hari = {r['trading_day_str']: r for r in rec if r.get('pub_trading_day_str') == pub and r.get('trading_day_str')}
    jenis = next((r.get('pub_type') for r in hari.values()), None)
    # pub_type 2 = selepas tutup: reaksi pada hari dagangan berikutnya; selainnya pada hari pengumuman
    selepas = sorted(t for t in hari if (t > pub if jenis == 2 else t >= pub))
    out = {'earnings_lalu_tarikh': pub, 'earnings_lalu_hari': hari_dagangan(date.fromisoformat(pub), hari_ini),
           'earnings_anggaran': (date.fromisoformat(pub) + timedelta(days=91)).isoformat(), 'earnings_gerak_pct': None}
    if selepas:
        r = hari[selepas[0]]
        sebelum = r.get('last_close_price')
        if sebelum and r.get('close_price'):
            out['earnings_gerak_pct'] = round((r['close_price'] / sebelum - 1) * 100, 2)
    return out


# ---------- Pemangkin: Berita Panas (sebab orang terus membeli) ----------
# Tiga lapis (belum diuji; paparan sahaja):
#  1. Kumpul: berita Moomoo (+ SST jika ada) yang benar-benar tentang saham itu, tindakan analisis berstruktur
#     (Moomoo quote_research_rating_summary) dan belian orang dalam (Form 4). Lihat `kumpul_pemangkin`.
#  2. Kelaskan ikut kuasa pemangkin: Tier 1 +3, Tier 2 +2, Tier 3 +1, negatif -1 hingga -3; susutan masa
#     0–3 hari penuh, 4–10 hari separuh, > 10 hari diabaikan.
#  3. Pengesahan pasaran bagi pemangkin terkuat: hari reaksi naik, volum >= 2x purata 20 hari, dan harga kini
#     masih di atas tutup sebelum berita -> +2 dan tanda PANAS; pasaran menolak (turun / jurang ditutup) -> -1.
KELAS = [  # (kategori, mata, corak); disemak mengikut susunan, negatif dahulu
    ('offering', -3, r'(public|secondary|registered direct|follow-on|at-the-market|atm|stock|share|equity|convertible) (notes )?offering'
                     r'|\bdilut|\bprices? .*\boffering|\bfiles? .*\bshelf'),
    ('turun_taraf', -2, r'\bdowngrade'),
    ('mula_jual', -2, r'initiates?.*\b(sell|underperform|underweight|negative)\b'),
    ('potong_sasaran', -2, r'\b(cuts?|lowers?|reduces?|slashes?) (its |the )?(price )?target'),
    ('potong_panduan', -2, r'\b(cuts?|lowers?|reduces?|slashes?|withdraws?) (its |the |fy|full-year |annual |\d{4} )*(guidance|outlook|forecast)'),
    ('gagal_earnings', -2, r'\bmiss(es|ed)?\b'),
    ('risiko', -1, r'\blawsuit|\bprobe\b|\binvestigation|\brecall\b|\bsubpoena|\bshort (seller|report)|\bdelist'),
    ('beat_naik_panduan', 3, r'\bbeats?\b.*\b(raises?|boosts?|lifts?|hikes?)\b|\b(raises?|boosts?|lifts?|hikes?)\b.*\bbeats?\b'),
    ('naik_panduan', 3, r'\b(raises?|boosts?|lifts?|hikes?|increases?) (its |the |fy|full-year |annual |\d{4} )*(guidance|outlook|forecast)'),
    ('fda', 3, r'\bfda (approv|clear|grant)|\bapproval\b.*\bfda\b|\bfda\b.*\bapproval\b'),
    ('indeks', 3, r'\b(added|add|join|joins|to join|set to join|inclusion|included|enter|enters) .*s&p (500|midcap 400|smallcap 600)'
                  r'|s&p (500|midcap 400|smallcap 600)\b.*\b(addition|inclusion|to add)'),
    ('ambil_alih', 3, r'to be acquired|agrees? to be (bought|acquired)|\b(takeover|buyout|acquisition) (bid|offer|proposal)'),
    ('kontrak_besar', 3, r'\$[\d.,]+ ?(million|billion|bn|m|b)\b.*\b(contract|order|award)|\b(contract|order|award)\b.*\$[\d.,]+ ?(million|billion|bn)'
                         r'|\b(partnership|collaboration|agreement|deal|contract) with (nvidia|microsoft|amazon|aws|google|alphabet|apple|meta|openai'
                         r'|tesla|oracle|the pentagon|pentagon|u\.s\. (army|navy|air force)|department of (defense|energy|war))'),
    ('naik_taraf', 2, r'\bupgrade'),
    ('mula_beli', 2, r'initiates?.*\b(buy|outperform|overweight|strong buy|positive)\b'),
    ('beat', 2, r'\bbeats?\b|\btops? (estimates|expectations|views)|\brecord (revenue|quarter|sales|results)'),
    ('buyback', 2, r'\bbuyback|\brepurchase'),
    ('naik_sasaran', 1, r'\b(raises?|boosts?|lifts?) (its |the )?(price )?target'),
    ('positif', 1, r'\bwins?\b.*\b(contract|order|award)|\bawarded\b|\bpartnership\b|\bapproval\b'),
]
LABEL = {'offering': 'tawaran saham (pencairan)', 'turun_taraf': 'turun taraf', 'mula_jual': 'mula liputan Jual',
         'potong_sasaran': 'potong sasaran', 'potong_panduan': 'potong panduan', 'gagal_earnings': 'earnings gagal',
         'risiko': 'risiko undang-undang/siasatan', 'beat_naik_panduan': 'earnings atasi + naik panduan',
         'naik_panduan': 'naik panduan', 'fda': 'kelulusan FDA', 'indeks': 'masuk indeks S&P',
         'ambil_alih': 'tawaran ambil alih', 'kontrak_besar': 'kontrak/rakan kongsi besar', 'naik_taraf': 'naik taraf',
         'mula_beli': 'mula liputan Beli', 'beat': 'earnings atasi', 'buyback': 'beli balik saham',
         'naik_sasaran_besar': 'naik sasaran ≥ 10%', 'naik_sasaran': 'naik sasaran', 'positif': 'berita positif',
         'orang_dalam_beli': 'orang dalam beli'}
ANALISIS_KAT = {'naik_taraf', 'turun_taraf', 'mula_beli', 'mula_jual', 'naik_sasaran', 'naik_sasaran_besar', 'potong_sasaran'}
HUJUNG_NAMA = {'inc', 'corp', 'corporation', 'holdings', 'holding', 'ltd', 'limited', 'plc', 'co', 'company', 'group',
               'nv', 'sa', 'ag', 'se', 'lp', 'llc', 'class', 'a', 'b', 'c', 'adr', 'ads', 'the', 'common', 'stock', 'shares'}
NAMA_UMUM = {'united', 'american', 'first', 'general', 'national', 'global', 'international', 'new', 'north', 'south',
             'west', 'east', 'advanced', 'applied', 'digital', 'energy', 'capital', 'pacific', 'atlantic', 'western',
             'eastern', 'central', 'royal', 'standard', 'universal', 'micro', 'super', 'smart', 'data', 'bio'}
SUSUT = [(3, 1.0), (10, 0.5)]


def bersih(tajuk):
    return re.sub(r'<[^>]+>', '', str(tajuk or '')).replace('&amp;', '&').strip()


def kelas_tajuk(tajuk):
    """Tajuk -> (kategori, mata) atau (None, 0)."""
    t = bersih(tajuk).lower()
    for k, m, p in KELAS:
        if re.search(p, t):
            return k, m
    return None, 0


def nilai_tajuk(tajuk):
    m = kelas_tajuk(tajuk)[1]
    return (m > 0) - (m < 0)


def nama_teras(nama):
    """'CF Industries Holdings, Inc.' -> 'CF Industries'; 'Infleqtion' -> 'Infleqtion'."""
    w = [x for x in re.split(r'[\s,]+', re.sub(r'[.()]', '', str(nama or ''))) if x and x.lower() not in HUJUNG_NAMA]
    if not w:
        return ''
    return w[0] if len(w[0]) >= 4 and w[0].lower() not in NAMA_UMUM or len(w) == 1 else ' '.join(w[:2])


def relevan(tajuk, ticker, nama=''):
    """Berita benar-benar tentang saham itu? Carian Moomoo ialah kata kunci ('CF' juga memulangkan berita
    cystic fibrosis), jadi tajuk mesti menyebut nama syarikat, '(TICKER)'/'$TICKER'/'NYSE: TICKER',
    atau ticker >= 4 huruf sebagai perkataan penuh."""
    t, tk = bersih(tajuk), str(ticker or '').upper()
    teras = nama_teras(nama)
    if teras and re.search(r'(?<![A-Za-z])' + re.escape(teras) + r'(?![A-Za-z])', t, re.I):
        return True
    if tk and re.search(r'(\(|\$|:\s?)' + re.escape(tk) + r'\b', t):
        return True
    return bool(tk) and len(tk) >= 4 and re.search(r'(?<![A-Za-z])' + re.escape(tk) + r'(?![A-Za-z])', t) is not None


def susut(hari):
    if hari is None:
        return 0.5
    for had, f in SUSUT:
        if hari <= had:
            return f
    return 0.0


def _hari_lalu(x, hari_ini):
    if hari_ini is not None and x.get('tarikh'):
        try:
            return (hari_ini - date.fromisoformat(str(x['tarikh'])[:10])).days
        except ValueError:
            pass
    return x.get('hari_lalu')


def peristiwa(p, hari_ini=None):
    """Senarai pemangkin (kategori, mata, hari_lalu, tarikh, selepas_tutup, tajuk, url, w = mata x susutan)
    daripada berita, analisis dan orang dalam, tanpa pendua (kategori + tarikh)."""
    ev, kunci = [], set()
    for a in p.get('analisis') or []:
        h = _hari_lalu(a, hari_ini)
        k = (a.get('kategori'), a.get('tarikh'), a.get('firma'))
        if a.get('kategori') not in LABEL or susut(h) == 0 or k in kunci:
            continue
        kunci.add(k)
        ev.append({**a, 'hari_lalu': h, 'w': a['mata'] * susut(h), 'tajuk': f"{a.get('firma') or 'Analisis'}: {LABEL[a['kategori']]}"
                   + (f" (sasaran ${a['sasaran']:g})" if a.get('sasaran') else '')})
    dari_analisis = {('naik_sasaran' if a['kategori'] == 'naik_sasaran_besar' else a['kategori'], a.get('tarikh')) for a in ev}
    for b in p.get('berita') or []:
        h = _hari_lalu(b, hari_ini)
        kat, m = kelas_tajuk(b.get('tajuk'))
        if not kat or susut(h) == 0:
            continue
        k = (kat, b.get('tarikh') if b.get('tarikh') else h)
        if k in kunci or (kat in ANALISIS_KAT and (kat, b.get('tarikh')) in dari_analisis):
            continue
        kunci.add(k)
        ev.append({'kategori': kat, 'mata': m, 'hari_lalu': h, 'tarikh': b.get('tarikh'), 'w': m * susut(h),
                   'selepas_tutup': b.get('selepas_tutup'), 'tajuk': bersih(b.get('tajuk')), 'url': b.get('url')})
    od = p.get('orang_dalam') or {}
    if od.get('bilangan'):
        h = _hari_lalu(od, hari_ini)
        if h is None or h <= 30:
            m = 2 if od['bilangan'] >= 2 else 1
            ev.append({'kategori': 'orang_dalam_beli', 'mata': m, 'hari_lalu': h, 'tarikh': od.get('tarikh'), 'w': m,
                       'tajuk': f"{od['bilangan']} orang dalam beli (30 hari)"})
    return ev


def terkuat(ev):
    pos = [e for e in ev if e['w'] > 0 and e['kategori'] != 'orang_dalam_beli' and e.get('tarikh')]
    return max(pos, key=lambda e: (e['w'], -(e['hari_lalu'] or 0))) if pos else None


def pengesahan(close, vol, tarikh, selepas_tutup=False):
    """Reaksi pasaran pada hari pertama selepas berita. close, vol: Series (index tarikh) satu saham.
    Pulangkan {hari, gerak_pct, volum_x, kekal} atau None jika data tidak cukup."""
    c, v = close.dropna(), vol.reindex(close.index)
    c = c.sort_index(); v = v.reindex(c.index)
    t = pd.Timestamp(tarikh)
    idx = c.index[c.index > t] if selepas_tutup else c.index[c.index >= t]
    if not len(idx):
        return None
    i = c.index.get_loc(idx[0])
    if i < 10:
        return None
    sebelum = float(c.iloc[i - 1])
    purata = float(v.iloc[max(0, i - 20):i].mean())
    if not sebelum or not purata or np.isnan(purata):
        return None
    return {'hari': idx[0].date().isoformat(), 'gerak_pct': round((float(c.iloc[i]) / sebelum - 1) * 100, 2),
            'volum_x': round(float(v.iloc[i]) / purata, 2), 'kekal': bool(float(c.iloc[-1]) > sebelum)}


def mata_pemangkin(p, hari_ini=None):
    """p: dict satu saham (papertrade/pemangkin.json; dibina oleh `gred.py kumpul`):
         berita: [{tajuk, tarikh (New York), selepas_tutup, hari_lalu, url}]   (sudah ditapis relevan)
         analisis: [{kategori, mata, firma, tarikh, sasaran, url}]           (Moomoo rating_summary)
         orang_dalam: {bilangan, tarikh}                                      (Form 4 belian, 30 hari)
         earnings_lalu_hari, earnings_gerak_pct; institusi: 'kumpul'|'agih'|None
         pengesahan: hasil `pengesahan` bagi pemangkin terkuat (diisi oleh `tambah`)
         volum_nisbah (volum 5 hari / purata 50), naik_5h (%)
       Pulangkan (mata, ringkasan). Ringkasan bermula '🔥 PANAS · ' jika pemangkin Tier 1/2 disahkan pasaran."""
    ev = peristiwa(p, hari_ini)
    pos = sorted([e for e in ev if e['w'] > 0], key=lambda e: -e['w'])
    neg = sorted([e for e in ev if e['w'] < 0], key=lambda e: e['w'])
    m = min(sum(e['w'] for e in pos), 6) + max(sum(e['w'] for e in neg), -6)
    ring = [f"{LABEL[e['kategori']]}" + (f" ({e['hari_lalu']} hari)" if e.get('hari_lalu') is not None else '') for e in pos[:3]]
    panas = False
    top, sah = terkuat(ev), p.get('pengesahan')
    if top and sah:
        if sah['gerak_pct'] > 0 and sah['volum_x'] >= 2 and sah['kekal']:
            m += 2; panas = top['mata'] >= 2
            ring.append(f"disahkan pasaran {sah['gerak_pct']:+.1f}%, volum {sah['volum_x']:.1f}×")
        elif sah['gerak_pct'] < 0 or not sah['kekal']:
            m -= 1; ring.append(f"pasaran tolak ({sah['gerak_pct']:+.1f}%{'' if sah['kekal'] else ', jurang ditutup'})")
    berita = [b for b in (p.get('berita') or []) if 0 < susut(_hari_lalu(b, hari_ini))]
    if len(berita) >= 3:
        m += 1; ring.append(f'{len(berita)} berita/10 hari')
    eh, eg = p.get('earnings_lalu_hari'), p.get('earnings_gerak_pct')
    if eh is not None and eh <= 30 and eg is not None:
        if eg >= 3: m += 2; ring.append(f'earnings {eh} hari lalu +{eg:.1f}%')
        elif eg <= -3: m -= 2; ring.append(f'earnings {eh} hari lalu {eg:.1f}%')
    vn, n5 = p.get('volum_nisbah'), p.get('naik_5h')
    if not sah and vn is not None and vn >= 2 and (n5 or 0) > 0:
        m += 1; ring.append(f'volum {vn:.1f}× naik')
    ins = p.get('institusi')
    if ins == 'kumpul': m += 1; ring.append('institusi kumpul')
    elif ins == 'agih': m -= 1; ring.append('institusi agih')
    ring += [LABEL[e['kategori']] + (f" ({e['hari_lalu']} hari)" if e.get('hari_lalu') is not None else '') for e in neg[:2]]
    m = round(m, 1)
    m = int(m) if m == int(m) else m
    teks = '; '.join(ring) or 'tiada pemangkin dikesan'
    return m, ('🔥 PANAS · ' + teks) if panas else teks


def pautan_berita(berita, maks=2, hari_ini=None):
    """Pautan untuk dashboard: pemangkin terkuat dahulu (mata), kemudian terkini; hanya URL https, <= 10 hari.
    Pulangkan JSON [{"tajuk", "url"}] (maks 2) atau '' jika tiada."""
    b = []
    for x in berita or []:
        h = _hari_lalu(x, hari_ini)
        if str(x.get('url') or '').startswith('https://') and (h is None or h <= 10):
            b.append((-(x['mata'] if 'mata' in x else kelas_tajuk(x.get('tajuk'))[1]), h if h is not None else 99, x))
    b.sort(key=lambda z: (z[0], z[1]))
    out = [{'tajuk': bersih(x.get('tajuk'))[:140], 'url': x['url']} for _, _, x in b[:maks]]
    return json.dumps(out, ensure_ascii=False) if out else ''


def gred_pemangkin(mata):
    if mata is None:
        return TIADA
    return 'A' if mata >= 5 else 'B' if mata >= 3 else 'C' if mata >= 1 else 'D' if mata >= 0 else 'E'


# ---------- Kumpul: fail mentah alat -> papertrade/pemangkin.json ----------
def baca_json(path):
    with open(path, encoding='utf-8') as f:
        d = json.load(f)
    if isinstance(d, list) and d and isinstance(d[0], dict) and 'text' in d[0] and len(d[0]) <= 3:
        d = json.loads(d[0]['text'])
    return d


def masa_ny(ms_atau_s):
    """Cap masa (saat atau ms, UTC) -> (tarikh New York ISO, selepas_tutup >= 16:00)."""
    s = ms_atau_s / 1000 if ms_atau_s > 1e11 else ms_atau_s
    from datetime import datetime, timezone
    try:
        from zoneinfo import ZoneInfo
        t = datetime.fromtimestamp(s, ZoneInfo('America/New_York'))
    except Exception:
        t = datetime.fromtimestamp(s, timezone.utc) - timedelta(hours=4)
    return t.date().isoformat(), t.hour >= 16


def berita_moomoo(d, ticker, nama, hari_ini):
    out = []
    for r in (d.get('data') if isinstance(d, dict) else d) or []:
        if not isinstance(r, dict) or not r.get('publish_time') or not relevan(r.get('title'), ticker, nama):
            continue
        tk, st = masa_ny(float(r['publish_time']))
        out.append({'tajuk': bersih(r.get('title'))[:200], 'tarikh': tk, 'selepas_tutup': st,
                    'hari_lalu': (hari_ini - date.fromisoformat(tk)).days, 'url': r.get('url') or '', 'sumber': 'moomoo'})
    return out


def berita_sst(d, ticker, nama, hari_ini):
    """Format SST search_news tidak tetap: cari senarai rekod yang ada tajuk dan tarikh."""
    def senarai(x):
        if isinstance(x, list):
            return x
        if isinstance(x, dict):
            for k in ('data', 'results', 'items', 'news', 'records'):
                if k in x:
                    return senarai(x[k])
        return []
    out = []
    for r in senarai(d):
        if not isinstance(r, dict):
            continue
        tj = r.get('title') or r.get('headline') or r.get('summary')
        tt = str(r.get('publishedAt') or r.get('published_at') or r.get('date') or r.get('eventDate') or '')[:10]
        if not tj or not TARIKH_ISO.match(tt) or not relevan(tj, ticker, nama) and r.get('ticker') != ticker:
            continue
        out.append({'tajuk': bersih(tj)[:200], 'tarikh': tt, 'selepas_tutup': False,
                    'hari_lalu': (hari_ini - date.fromisoformat(tt)).days, 'url': r.get('url') or r.get('link') or '', 'sumber': 'sst'})
    return out


TARIKH_ISO = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def analisis_moomoo(d, hari_ini, hari_maks=10):
    """Moomoo quote_research_rating_summary -> tindakan analisis terkini setiap institusi (<= 10 hari):
    naik/turun taraf (rating berbanding rekod sebelumnya institusi sama), mula liputan, ubah sasaran.
    Skala rating Moomoo: 3+ = Beli, 2 = Tahan, 1 = Jual."""
    out = []
    lst = (d.get('data') or {}).get('inst_rating_summary_list') or [] if isinstance(d, dict) else []
    for inst in lst:
        firma = ((inst.get('institution_info') or {}).get('institution_en_name')
                 or (inst.get('institution_info') or {}).get('institution_name') or '')
        it = sorted([x for x in inst.get('rating_item_list') or [] if x.get('recommendation_date')],
                    key=lambda x: -x['recommendation_date'])
        if not it:
            continue
        L, P = it[0], (it[1] if len(it) > 1 else None)
        tk, _ = masa_ny(float(L['recommendation_date']))
        h = (hari_ini - date.fromisoformat(tk)).days
        if h > hari_maks or h < 0:
            continue
        rl, rp = L.get('rating'), (P or {}).get('rating')
        sl, sp = L.get('target_price'), (P or {}).get('target_price')
        kat = None
        if rl is not None and rp is not None and rl != rp:
            kat = 'naik_taraf' if rl > rp else 'turun_taraf'
        elif P is None and rl is not None:
            kat = 'mula_beli' if rl >= 3 else 'mula_jual' if rl <= 1 else None
        elif sl and sp:
            u = sl / sp - 1
            kat = ('naik_sasaran_besar' if u >= 0.10 else 'naik_sasaran' if u > 0 else
                   'potong_sasaran' if u < 0 else None)
        if not kat:
            continue
        m = {'naik_taraf': 2, 'mula_beli': 2, 'naik_sasaran_besar': 2, 'naik_sasaran': 1, 'turun_taraf': -2,
             'mula_jual': -2, 'potong_sasaran': -2 if sl and sp and sl / sp - 1 <= -0.10 else -1}[kat]
        out.append({'kategori': kat, 'mata': m, 'firma': firma, 'tarikh': tk, 'hari_lalu': h,
                    'sasaran': sl, 'url': L.get('rating_url') or ''})
    return out


def orang_dalam_moomoo(d, hari_ini, hari_maks=30):
    """Moomoo quote_insider_trade_list -> {bilangan orang dalam berbeza yang BELI di pasaran (Form 4), tarikh}."""
    nama, akhir = set(), None
    for r in ((d.get('data') or {}).get('trades') or []) if isinstance(d, dict) else []:
        jenis = str(r.get('transaction_type') or '')
        if not re.search(r'purchase|\bbuy', jenis, re.I) or (r.get('trade_shares') or 0) <= 0:
            continue
        t = str(r.get('max_trade_date_str') or '')[:10]
        if not TARIKH_ISO.match(t) or not 0 <= (hari_ini - date.fromisoformat(t)).days <= hari_maks:
            continue
        nama.add(r.get('name') or r.get('holder_id')); akhir = max(akhir or t, t)
    return {'bilangan': len(nama), 'tarikh': akhir} if nama else {}


def kumpul_pemangkin(folder, nama, hari_ini, institusi=None):
    """Bina {ticker: entri} daripada fail mentah dalam `folder` (simpan hasil alat SEBIJI, jangan diubah):
       berita_<T>.json (Moomoo quote_news_search), analisis_<T>.json (quote_research_rating_summary),
       orangdalam_<T>.json (quote_insider_trade_list), earnings_<T>.json (quote_financials_earnings_price_history),
       sst_<T>.json (SST search_news, pilihan). nama: {ticker: nama syarikat} untuk tapisan relevan."""
    out = {}
    tickers = sorted({re.match(r'^[a-z]+_(.+)\.json$', f).group(1) for f in os.listdir(folder)
                      if re.match(r'^(berita|analisis|orangdalam|earnings|sst)_.+\.json$', f)})
    for t in tickers:
        f = lambda jenis: os.path.join(folder, f'{jenis}_{t}.json')
        e = {'dikumpul': hari_ini.isoformat(), 'berita': [], 'analisis': [], 'orang_dalam': {}}
        if os.path.exists(f('berita')):
            e['berita'] += berita_moomoo(baca_json(f('berita')), t, nama.get(t, ''), hari_ini)
        if os.path.exists(f('sst')):
            lama = {b['tajuk'].lower() for b in e['berita']}
            e['berita'] += [b for b in berita_sst(baca_json(f('sst')), t, nama.get(t, ''), hari_ini) if b['tajuk'].lower() not in lama]
        if os.path.exists(f('analisis')):
            e['analisis'] = analisis_moomoo(baca_json(f('analisis')), hari_ini)
        if os.path.exists(f('orangdalam')):
            e['orang_dalam'] = orang_dalam_moomoo(baca_json(f('orangdalam')), hari_ini)
        if os.path.exists(f('earnings')):
            e.update(ringkas_earnings(f('earnings'), hari_ini))
        e['institusi'] = (institusi or {}).get(t)
        out[t] = e
    return out


def gred_keseluruhan(gred):
    """Purata mata gred yang ada (A=4 … E=0) -> huruf. Belum diuji; untuk paparan sahaja."""
    v = [MATA[g] for g in gred if g in MATA]
    if not v:
        return TIADA
    x = sum(v) / len(v)
    return 'A' if x >= 3.5 else 'B' if x >= 2.5 else 'C' if x >= 1.5 else 'D' if x >= 0.5 else 'E'


# ---------- CLI ----------
def muat_harga(folder):
    fr = []
    for nm in ['harga_A.csv', 'harga_B.csv']:
        p = os.path.join(folder, nm)
        if os.path.exists(p):
            fr.append(pd.read_csv(p, usecols=['ticker', 'date', 'close', 'volume']))
    if not fr:
        raise SystemExit(f'Tiada harga_A.csv/harga_B.csv dalam {folder}')
    d = pd.concat(fr).drop_duplicates(['ticker', 'date'], keep='last')
    d['date'] = pd.to_datetime(d['date'].astype(str))
    c = d.pivot(index='date', columns='ticker', values='close').sort_index()
    v = d.pivot(index='date', columns='ticker', values='volume').sort_index()
    return c, v


def ambil(r, *k):
    for x in k:
        if x in r and r[x] not in (None, ''):
            return r[x]
    return None


def segar(e, hari_ini, hari_maks=2):
    """Entri pemangkin.json dikumpul <= 2 hari dagangan lalu (tanpa 'dikumpul' = dianggap segar)."""
    try:
        return hari_dagangan(date.fromisoformat(e['dikumpul']), hari_ini) <= hari_maks
    except (KeyError, TypeError, ValueError):
        return True


def kumpul(a):
    hari_ini = date.fromisoformat(a.tarikh)
    nama = {}
    for f in a.csv or []:
        for r in csv.DictReader(open(f, newline='', encoding='utf-8')):
            t, n = ambil(r, 'saham', 'Saham'), ambil(r, 'nama', 'Nama')
            if t and n:
                nama[t] = n
    ins = json.load(open(a.institusi, encoding='utf-8')) if a.institusi else {}
    baru = kumpul_pemangkin(a.folder, nama, hari_ini, ins)
    lama = json.load(open(a.keluar, encoding='utf-8')) if os.path.exists(a.keluar) else {}
    # gabung: entri baharu menggantikan; entri lama > 5 hari dagangan dibuang
    gab = {t: e for t, e in lama.items() if segar(e, hari_ini, 5)}
    gab.update(baru)
    with open(a.keluar, 'w', encoding='utf-8') as f:
        json.dump(dict(sorted(gab.items())), f, ensure_ascii=False, indent=1)
    tanpa_nama = sorted(t for t in baru if t not in nama)
    print(f'{len(baru)} saham dikumpul; {sum(1 for e in baru.values() if e["berita"])} ada berita relevan; '
          f'{sum(1 for e in baru.values() if e["analisis"])} ada tindakan analisis; jumlah dalam fail {len(gab)}')
    if tanpa_nama:
        print('AMARAN tiada nama syarikat (tapisan relevan guna ticker sahaja):', ' '.join(tanpa_nama))


def tambah(a):
    rows = list(csv.DictReader(open(a.csv, newline='', encoding='utf-8')))
    lajur = list(rows[0].keys()) if rows else []
    hari_ini = date.fromisoformat(a.tarikh)
    c, v = muat_harga(a.harga)
    rs = rs_rating(c)
    vn = (v.iloc[-5:].mean() / v.iloc[-50:].mean()) if len(v) >= 50 else pd.Series(dtype=float)
    n5 = (c.iloc[-1] / c.iloc[-6] - 1) * 100 if len(c) >= 6 else pd.Series(dtype=float)
    sek, ind = peta_sektor(a.sektor)
    # Utama: kekuatan seluruh pasaran AS (sektor_pasaran.py) dengan industri Moomoo setiap saham
    pusek, puind, pind = {}, {}, {}
    if a.pasaran and a.peta and os.path.exists(a.pasaran) and os.path.exists(a.peta):
        from sektor_pasaran import SEKTOR_INDUSTRI
        pusek, puind = peta_pasaran(a.pasaran)
        pind = {r['ticker']: r['industri'] for r in csv.DictReader(open(a.peta, newline='', encoding='utf-8'))}
    ear = peta_earnings(a.acara, hari_ini) if a.acara else None
    pem = json.load(open(a.pemangkin, encoding='utf-8')) if a.pemangkin else {}
    for r in rows:
        t = ambil(r, 'saham', 'Saham')
        iu = pind.get(t); su = SEKTOR_INDUSTRI.get(iu) if iu else None
        r['industri_us'] = iu or ''; r['sektor_us'] = su or ''
        s1 = pusek.get(su) if su in pusek else sek.get(ambil(r, 'sektor', 'Sektor'))
        s2 = puind.get(iu) if iu in puind else ind.get(ambil(r, 'industri', 'Industri'))
        r['skor_sektor'] = '' if s1 is None else round(s1, 1); r['gred_sektor'] = gred_kumpulan(s1)
        r['skor_industri'] = '' if s2 is None else round(s2, 1); r['gred_industri'] = gred_kumpulan(s2)
        x = int(rs[t]) if t in rs.index else None
        r['rs_rating'] = '' if x is None else x; r['gred_rs'] = gred_rs(x)
        te, sumber = (ear or {}).get(t), 'SST'
        if te is None and (pem.get(t) or {}).get('earnings_anggaran'):
            te, sumber = date.fromisoformat(pem[t]['earnings_anggaran']), 'anggaran'
            if te < hari_ini:
                te = None
        if te is None and ear is None:
            r['tarikh_earnings'] = ''; r['hari_ke_earnings'] = ''; r['sumber_earnings'] = 'tiada data'; r['gred_qr'] = TIADA
        else:
            h = hari_dagangan(hari_ini, te) if te else None
            r['tarikh_earnings'] = te.isoformat() if te else ''
            r['hari_ke_earnings'] = '' if h is None else h
            r['sumber_earnings'] = sumber if te else 'tiada dalam 30 hari (SST)'
            r['gred_qr'] = gred_qr(h)
        if t in pem and segar(pem[t], hari_ini):
            p = dict(pem[t])
            p.setdefault('volum_nisbah', None if t not in vn.index or pd.isna(vn[t]) else float(vn[t]))
            p.setdefault('naik_5h', None if t not in n5.index or pd.isna(n5[t]) else float(n5[t]))
            top = terkuat(peristiwa(p, hari_ini))
            if top and 'pengesahan' not in p and t in c.columns:
                p['pengesahan'] = pengesahan(c[t], v[t], top['tarikh'], top.get('selepas_tutup'))
            m, ring = mata_pemangkin(p, hari_ini)
            r['mata_pemangkin'] = m; r['pemangkin'] = ring; r['gred_pemangkin'] = gred_pemangkin(m)
            r['pemangkin_url'] = pautan_berita(peristiwa(p, hari_ini) + list(p.get('berita') or []), hari_ini=hari_ini)
        else:
            r['mata_pemangkin'] = ''; r['pemangkin'] = 'belum dikumpul'; r['gred_pemangkin'] = TIADA
            r['pemangkin_url'] = ''
        r['gred_keseluruhan'] = gred_keseluruhan([r['gred_sektor'], r['gred_industri'], r['gred_rs'],
                                                  r['gred_pemangkin'], r['gred_qr']])
        r['gred_pada'] = a.tarikh
    out = lajur + [k for k in LAJUR if k not in lajur]
    with open(a.csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=out)
        w.writeheader(); w.writerows(rows)
    from collections import Counter
    for k in ['gred_sektor', 'gred_industri', 'gred_rs', 'gred_pemangkin', 'gred_qr', 'gred_keseluruhan']:
        print(k, dict(sorted(Counter(r[k] for r in rows).items())))


def main(argv=None):
    ap = argparse.ArgumentParser(description='Tambah lajur gred ke CSV calon (senarai_beli / watchlist)')
    sp = ap.add_subparsers(dest='cmd', required=True)
    t = sp.add_parser('tambah')
    t.add_argument('--csv', required=True)
    t.add_argument('--harga', required=True, help='folder harga_A.csv / harga_B.csv (stor harga dashboard)')
    t.add_argument('--sektor', required=True, help='papertrade/sektor.csv (sandaran: snapshot SST)')
    t.add_argument('--pasaran', help='papertrade/sektor_pasaran.csv (utama: seluruh pasaran AS)')
    t.add_argument('--peta', help='papertrade/peta_industri.csv (ticker -> industri Moomoo)')
    t.add_argument('--acara', help='JSON SST market_events (daysLookahead 30)')
    t.add_argument('--pemangkin', help='papertrade/pemangkin.json (hasil `gred.py kumpul`)')
    t.add_argument('--tarikh', required=True, help='tarikh imbasan YYYY-MM-DD')
    k = sp.add_parser('kumpul', help='fail mentah alat (berita/analisis/orangdalam/earnings/sst_<T>.json) -> pemangkin.json')
    k.add_argument('--folder', required=True)
    k.add_argument('--csv', nargs='*', help='senarai_beli.csv / watchlist.csv (nama syarikat untuk tapisan relevan)')
    k.add_argument('--institusi', help='JSON {ticker: "kumpul"|"agih"} daripada SST institutional_flow')
    k.add_argument('--keluar', required=True, help='papertrade/pemangkin.json (digabung dengan entri sedia ada)')
    k.add_argument('--tarikh', required=True)
    e = sp.add_parser('earnings', help='ringkas fail Moomoo earnings_price_history -> JSON')
    e.add_argument('fail'); e.add_argument('--tarikh', required=True)
    a = ap.parse_args(argv)
    if a.cmd == 'tambah':
        tambah(a)
    elif a.cmd == 'kumpul':
        kumpul(a)
    elif a.cmd == 'earnings':
        print(json.dumps(ringkas_earnings(a.fail, date.fromisoformat(a.tarikh))))


if __name__ == '__main__':
    main()
