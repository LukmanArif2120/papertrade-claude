# Gred calon dan posisi papertrade: Sektor, Industri, RS, Pemangkin, QR (jarak ke laporan suku/earnings).
# Peraturan dan bukti: standard/tugasan_v3.md §8. Gred direkod pada hari isyarat; prestasi setiap gred dinilai
# selepas >= 20 dagangan tertutup (dashboard Prestasi > Prestasi ikut gred).
#
# Guna (imbasan 8:02 malam):
#   python3 gred.py tambah --csv papertrade/senarai_beli.csv --harga <folder harga_A/B.csv> \
#       --kumpulan data/kumpulan/gred_kumpulan.csv --peta papertrade/peta_industri.csv \
#       --acara <market_events.json> --pemangkin <pemangkin.json> --tarikh YYYY-MM-DD
#   (Sektor/Industri v2 sejak 19 Okt 2026: standard/gred_kumpulan.py; tanpa --kumpulan = v1 skor panas, --sektor wajib)
#   (ulang untuk papertrade/watchlist.csv; --pemangkin pilihan)
#   python3 gred.py kumpul --folder <fail mentah alat> --csv papertrade/senarai_beli.csv papertrade/watchlist.csv \
#       --keluar papertrade/pemangkin.json --tarikh YYYY-MM-DD      (berita untuk veto/pautan pemangkin v3)
#   Sumber percuma (Actions, pemangkin_actions.py): `kumpul --yahoo data/pemangkin/yahoo.json --nasdaq
#   data/pemangkin/earnings_nasdaq.json` (--folder pilihan; data Moomoo hari ini diutamakan) dan `tambah --nasdaq …`
#   (tarikh earnings kedua selepas SST; reaksi earnings lalu dikira daripada stor harga).
import sys, os, re, csv, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datetime import date, datetime, timedelta, timezone

import numpy as np
import pandas as pd

GRED = ['A', 'B', 'C', 'D', 'E']
MATA = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
TIADA = '–'
HERE_GRED = os.path.dirname(os.path.abspath(__file__))
LAJUR = ['sektor_us', 'industri_us', 'gred_sektor', 'skor_sektor', 'gred_industri', 'skor_industri', 'rs_rating', 'gred_rs',
         'rs_sah', 'rs_tanda', 'rs_industri', 'rs_sumber', 'gred_pemangkin', 'mata_pemangkin', 'pemangkin', 'pemangkin_url', 'tarikh_earnings', 'hari_ke_earnings', 'sumber_earnings', 'gred_qr',
         'gred_keseluruhan', 'gred_pada']


# ---------- RS rating (gaya IBD, 1–99) ----------
# Skema 18 Okt 2026 (kajian 3,830 saham AS 2005–2026: kajian/rs/RINGKASAN.md; tugasan_v3.md §8):
#   RS dipangkat berbanding SELURUH pasaran AS (data/rs/rs_pasaran.csv, Actions rs_pasaran.yml); sandaran stor harga.
#   Kelebihan RS hanya sah jika "disahkan": saham naik dalam 12 bulan, SPY > SMA200, Mansfield > 0 (RS line atas purata 52 minggu).
#   Lebihan 63 hari atas pasaran: A +1.5% (CI95 +0.8..+2.3), RS 95+ +1.9% tetapi median ≈ 0 (ditanda), B +0.6%, C ≈ 0, D −0.2..−0.4%.
#   RS >= 80 yang tidak disahkan ≈ 0 (pasaran lemah: RS tinggi kalah kepada pasaran) -> C.
RS_SAH = ('mutlak12', 'mansfield', 'spy_atas200')


def skor_rs(close):
    """close: DataFrame (index tarikh, lajur ticker). Skor IBD pada bar terakhir: 40% pulangan 63 hari terkini + 20% setiap
    satu daripada tiga suku sebelumnya. Saham dengan < 253 bar atau tiada harga 252 hari lalu tiada skor."""
    c = close.sort_index()
    if len(c) < 253:
        return pd.Series(dtype=float)
    a = c.iloc[-1]
    q = [c.iloc[-64], c.iloc[-127], c.iloc[-190], c.iloc[-253]]
    skor = 0.4 * (a / q[0] - 1) + 0.2 * (q[0] / q[1] - 1) + 0.2 * (q[1] / q[2] - 1) + 0.2 * (q[2] / q[3] - 1)
    return skor.replace([np.inf, -np.inf], np.nan).dropna()


def rs_rating(close, harga_min=5.0):
    """Pangkat persentil 1–99 skor RS berbanding semua saham dalam `close` dengan tutup terakhir >= harga_min."""
    skor = skor_rs(close)
    if skor.empty:
        return skor
    akhir = close.sort_index().iloc[-1].reindex(skor.index)
    skor = skor[akhir >= harga_min] if harga_min else skor
    return (skor.rank(pct=True) * 98 + 1).round().astype(int).clip(1, 99)


def sah_rs(close, spy):
    """Pengesahan pada bar terakhir: DataFrame (ticker) mutlak12 (% 252 hari), mansfield (% RS line atas purata 252 hari),
    dan skalar spy_atas200. close dan spy (Series) berindeks tarikh sama."""
    c = close.sort_index()
    s = spy.reindex(c.index).ffill()
    out = pd.DataFrame(index=c.columns, dtype=float)
    out['mutlak12'] = ((c.iloc[-1] / c.iloc[-253] - 1) * 100) if len(c) >= 253 else np.nan
    rl = c.div(s, axis=0)
    out['mansfield'] = ((rl.iloc[-1] / rl.iloc[-252:].mean() - 1) * 100) if len(c) >= 252 else np.nan
    atas = bool(s.iloc[-1] > s.iloc[-200:].mean()) if len(s.dropna()) >= 200 else None
    return out, atas


def disahkan(mutlak12, mansfield, spy_atas200):
    """True/False, atau None jika data pengesahan tiada."""
    v = [mutlak12, mansfield, spy_atas200]
    if any(x is None or (isinstance(x, float) and np.isnan(x)) for x in v):
        return None
    return bool(mutlak12 > 0 and mansfield > 0 and spy_atas200)


def gred_rs(rs, sah=None):
    """A: RS 90–99 disahkan; B: 80–89 disahkan; C: 70–79, atau >= 80 tidak/belum disahkan; D: < 70."""
    if rs is None or (isinstance(rs, float) and np.isnan(rs)):
        return TIADA
    if rs < 70:
        return 'D'
    if rs < 80 or not sah:
        return 'C'
    return 'A' if rs >= 90 else 'B'


def tanda_rs(rs, mutlak12=None, mansfield=None, spy_atas200=None):
    """Teks amaran bagi paparan: sebab RS >= 80 tidak disahkan, atau risiko RS 95+."""
    if rs is None or (isinstance(rs, float) and np.isnan(rs)) or rs < 80:
        return ''
    sah = disahkan(mutlak12, mansfield, spy_atas200)
    if sah is None:
        return 'pengesahan tiada data'
    if not sah:
        s = [x for x, b in (('pasaran lemah (SPY < SMA200)', not spy_atas200), ('saham turun 12 bulan', mutlak12 <= 0),
                            ('Mansfield < 0', mansfield <= 0)) if b]
        return 'tidak disahkan: ' + ', '.join(s)
    return 'RS 95+: purata tertinggi tetapi berisiko (median ≈ 0)' if rs >= 95 else ''


def baca_rs_pasaran(folder, sesi):
    """data/rs/rs_pasaran.csv -> DataFrame (ticker) bagi `sesi` (YYYY-MM-DD) dan spy_atas200; (None, None) jika tiada."""
    f = os.path.join(folder, 'rs_pasaran.csv') if folder else None
    st = os.path.join(folder, 'status.json') if folder else None
    if not f or not os.path.exists(f) or not os.path.exists(st):
        return None, None
    d = pd.read_csv(f, dtype={'tarikh': str})
    d = d[d.tarikh == sesi]
    spy = (json.load(open(st, encoding='utf-8')).get('spy_atas200') or {}).get(sesi)
    if d.empty or spy is None:
        return None, None
    return d.set_index('ticker'), bool(spy)


def muat_spy(folder):
    p = os.path.join(folder, 'harga_idx.csv')
    if not os.path.exists(p):
        return None
    d = pd.read_csv(p, usecols=['ticker', 'date', 'close'])
    d = d[d.ticker == 'SPY']
    return pd.Series(d.close.values, index=pd.to_datetime(d.date.astype(str))).sort_index()


def rs_semua(c, spy, folder_rs=None):
    """RS dan pengesahan bagi bar terakhir `c`: utama seluruh pasaran (rs_pasaran.csv sesi sama), sandaran stor harga.
    Pulang (DataFrame ticker: rs, mutlak12, mansfield, rs_industri, rs_sumber; spy_atas200)."""
    sesi = str(c.index[-1].date())
    pas, atas = baca_rs_pasaran(folder_rs, sesi)
    st = pd.DataFrame({'rs': rs_rating(c)})
    if spy is not None:
        sh, atas_st = sah_rs(c, spy)
        st = st.join(sh, how='outer')
        atas = atas_st if atas is None else atas
    st['rs_industri'] = np.nan
    st['rs_sumber'] = 'stor'
    if pas is not None:
        p = pas.reindex(columns=['rs', 'mutlak12', 'mansfield', 'rs_industri']).copy()
        p['rs_sumber'] = 'pasaran'
        st = pd.concat([p, st[~st.index.isin(p.index)]])
    return st, atas


# ---------- Sektor / Industri v2 (sejak 19 Okt 2026; standard/gred_kumpulan.py) ----------
HARI_KUMPULAN = 7   # data/kumpulan/gred_kumpulan.csv lebih lama daripada ini (hari kalendar) -> gred "–"


def peta_kumpulan(path_csv, hari_ini):
    """data/kumpulan/gred_kumpulan.csv -> ({sektor: (skor, gred)}, {industri: (skor, gred)}, tarikh) atau
    ({}, {}, tarikh/None) jika fail tiada atau basi (> HARI_KUMPULAN hari sebelum hari_ini)."""
    if not path_csv or not os.path.exists(path_csv):
        return {}, {}, None
    rows = list(csv.DictReader(open(path_csv, newline='', encoding='utf-8')))
    if not rows:
        return {}, {}, None
    t = max(r['tarikh'] for r in rows)
    if (hari_ini - date.fromisoformat(t)).days > HARI_KUMPULAN:
        return {}, {}, t
    sek, ind = {}, {}
    for r in rows:
        if r['tarikh'] == t and r['gred'] in GRED:
            (sek if r['jenis'] == 'Sektor' else ind)[r['nama']] = (float(r['skor']), r['gred'])
    return sek, ind, t


def peta_jenis_kaedah(path_csv=None):
    """kod/jenis_kaedah.csv -> {kaedah: 'momentum'|'pantulan'} (pulangan median 20 hari sebelum isyarat > 0 = momentum)."""
    path_csv = path_csv or os.path.join(os.path.dirname(HERE_GRED), 'kod', 'jenis_kaedah.csv')
    if not os.path.exists(path_csv):
        return {}
    return {r['kaedah']: r['jenis'] for r in csv.DictReader(open(path_csv, newline='', encoding='utf-8'))}


def id_kaedah(teks):
    m = re.match(r'\s*(M\d+)', str(teks or ''))
    return m.group(1) if m else ''


# ---------- Sektor / Industri v1 (skor panas, 0–100; dipakai hanya jika --kumpulan tidak diberi) ----------
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


def gred_qr(hari, sejak=None):
    """Risiko jurang QR semasa pegang (kajian 18 Okt 2026: 659k dagangan isyarat 134 kaedah, 2019–2026; lompat
    henti dan rugi <= -15% lawan beli > 30 hari sebelum QR; sempadan disahkan segmentasi optimum + bootstrap).
    hari = hari dagangan ke QR seterusnya; None = tiada dalam tetingkap 30/35 hari kalendar (> ~21) -> A.
    sejak = hari dagangan sejak QR lalu: 0–1 -> sekurang-kurangnya C, 2–3 -> sekurang-kurangnya B (volatiliti
    selepas pengumuman belum reda). Gred akhir = yang lebih buruk."""
    g = 'A' if hari is None or hari > 21 else 'B' if hari > 15 else 'C' if hari > 10 else 'D' if hari > 5 else 'E'
    if sejak is not None and sejak <= 3:
        g = max(g, 'C' if sejak <= 1 else 'B')
    return g


def sejak_qr(lalu, hari_ini):
    """Tarikh QR lalu (sebelum hari ini) -> hari dagangan sejak; None jika tiada atau bukan sebelum hari ini."""
    return hari_dagangan(lalu, hari_ini) if lalu and lalu < hari_ini else None


def tanda_pasca_qr(sumber, sejak):
    """Catatan pada sumber_earnings apabila QR lalu <= 3 hari dagangan (paparan dashboard)."""
    return f'{sumber}; QR lalu {sejak} hari' if sejak is not None and sejak <= 3 else sumber


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


# ---------- Pemangkin v3 (sejak 18 Okt 2026) ----------
# Kajian 18 Okt 2026 (pandangan pakar + data sejarah data/pemangkin/sejarah/: 945 saham semasa, 2012–2026; AR21 = masuk
# buka esok, 21 hari, lawan purata sama berat saham cair). Hanya komponen yang lulus luar sampel (latih 2012–2018,
# uji 2019–2026) diberi mata — lihat `nilai_pemangkin`. Kalibrasi gred (AR21 latih / uji): A +1.7 / +1.4%,
# B +0.38 / +0.35%, C +0.24 / +0.20%, D −0.11 / −0.01% (menurun A→D dalam kedua-dua tempoh). Bias survivorship: alam
# saham semasa sahaja.
#  K1 premium pengumuman: earnings dijadualkan 6–21 hari dagangan lagi +2 (AR21 +0.38% / +0.35%, t 3.4 luar sampel),
#     1–5 hari lagi +1 (+0.24% / +0.20%).
#  K2 reaksi earnings melampau: hari reaksi >= +20% lawan pasaran, umur <= 10 hari dagangan +4, 11–20 hari +3
#     (AR21 +1.7% / +1.4%; ~640 peristiwa, t < 2 — bukti lemah). Reaksi 3–20% dan reaksi negatif: 0.
#  Diuji dan dibuang: mata tajuk berita, bilangan berita, tindakan analisis (termasuk 'disahkan pasaran'),
#     volum, penalti perhatian. Belum diuji (data SEC gagal): orang dalam. Institusi: tiada data.
#  Veto (bukti pakar sahaja): tawaran saham/pencairan atau peristiwa binari FDA/klinikal <= 20 hari dagangan
#     -> had C; sasaran ambil alih -> had D.
#  Gred: A >= 3, B 2, C 1, D 0 (tiada pemangkin). E tidak dipakai (tiada isyarat negatif sahih dalam data).
# Pengelas tajuk (KELAS) dan peristiwa analisis kekal untuk veto, pautan dan paparan sahaja.
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


def hari_reaksi(close, vol, tarikh, selepas_tutup=None):
    """Reaksi earnings: `pengesahan` pada hari reaksi. selepas_tutup None (masa pengumuman tidak diketahui, cth.
    kalendar Nasdaq 'time-not-supplied'): hari reaksi = hari volum lebih tinggi antara hari pengumuman dan hari
    dagangan berikutnya (disahkan pada data sejarah: volum memuncak pada hari itu); None jika hari berikutnya
    belum ada dalam stor harga."""
    if selepas_tutup is not None:
        return pengesahan(close, vol, tarikh, selepas_tutup)
    a, b = pengesahan(close, vol, tarikh, False), pengesahan(close, vol, tarikh, True)
    return None if not a or not b else a if a['volum_x'] >= b['volum_x'] else b


def reaksi_earnings(close, vol, tarikh, selepas_tutup=None):
    """Gerak % hari reaksi earnings (tutup hari reaksi lawan tutup sebelumnya); lihat `hari_reaksi`."""
    s = hari_reaksi(close, vol, tarikh, selepas_tutup)
    return s['gerak_pct'] if s else None


VETO = [  # (had gred, sebab, corak tajuk) — bukti pakar; tidak diuji pada data repo
    ('D', 'sasaran ambil alih (harga terkunci pada tawaran)',
     r'to be acquired|agrees? to be (bought|acquired)|definitive (merger )?agreement to be acquired|\bto go private|take[- ]private'),
    ('C', 'tawaran saham (pencairan)', KELAS[0][2]),
    ('C', 'peristiwa binari FDA/klinikal',
     r'\bpdufa\b|advisory committee|\badcom\b|fda (decision|action date)|target action date'),  # keputusan akan datang
]
BUKAN_PENCAIRAN = r'selling (share|stock)holders?|by (a |the )?selling|secondary (public )?offering .*\bby\b'
HARI_VETO = 28  # 20 hari dagangan ~ 28 hari kalendar


def veto_tajuk(tajuk):
    """Tajuk berita -> (had gred, sebab) atau None."""
    t = bersih(tajuk).lower()
    for had, sebab, corak in VETO:
        if re.search(corak, t) and not (sebab.startswith('tawaran') and re.search(BUKAN_PENCAIRAN, t)):
            return had, sebab
    return None


def nilai_pemangkin(p, hari_ini, hari_ke_earnings=None, close=None, vol=None, pasaran=None):
    """Pemangkin v3 -> (mata, gred, ringkasan). Ringkasan bermula '🔥 PANAS · ' jika K2 aktif dan tiada veto.
    p: entri pemangkin.json (boleh {}), dengan earnings_lalu_tarikh / earnings_selepas_tutup (Nasdaq) atau
       earnings_gerak_pct / earnings_lalu_hari (Moomoo) dan berita [{tajuk, tarikh, hari_lalu}] untuk veto.
    hari_ke_earnings: hari dagangan ke earnings seterusnya (sama seperti QR). close, vol: Series satu saham;
    pasaran: Series tutup SPY (pelarasan reaksi). Umur reaksi = hari dagangan dalam stor selepas hari reaksi."""
    p = p or {}
    mata, ring = 0, []
    g = umur = None
    if p.get('earnings_lalu_tarikh') and close is not None and vol is not None:
        s = hari_reaksi(close, vol, p['earnings_lalu_tarikh'], p.get('earnings_selepas_tutup'))
        if s:
            g, t = s['gerak_pct'], pd.Timestamp(s['hari'])
            ps = pasaran.dropna().sort_index() if pasaran is not None else None
            if ps is not None and t in ps.index and ps.index.get_loc(t) > 0:
                k = ps.index.get_loc(t)
                g = round(g - (float(ps.iloc[k]) / float(ps.iloc[k - 1]) - 1) * 100, 2)
            umur = int((close.dropna().index > t).sum())
    if g is None and p.get('earnings_gerak_pct') is not None and p.get('earnings_lalu_hari') is not None:
        g, umur = p['earnings_gerak_pct'], p['earnings_lalu_hari']   # Moomoo: belum dilaras pasaran
    panas = g is not None and g >= 20 and umur is not None and umur <= 20
    if panas:
        k2 = 4 if umur <= 10 else 3
        mata += k2; ring.append(f'reaksi earnings {g:+.1f}% lawan pasaran ({umur} hari lalu) +{k2}')
    h = hari_ke_earnings
    if h is not None and 1 <= h <= 21:
        k1 = 2 if h >= 6 else 1
        mata += k1; ring.append(f'earnings {h} hari dagangan lagi (premium pengumuman) +{k1}')
    gred = gred_pemangkin(mata)
    for b in p.get('berita') or []:
        hl = _hari_lalu(b, hari_ini)
        v = veto_tajuk(b.get('tajuk')) if hl is not None and 0 <= hl <= HARI_VETO else None
        if v and GRED.index(gred) < GRED.index(v[0]):
            gred = v[0]; ring.append(f'had {v[0]}: {v[1]} ({hl} hari lalu)')
    teks = '; '.join(ring) or 'tiada pemangkin'
    return mata, gred, ('🔥 PANAS · ' + teks) if panas and gred == 'A' else teks   # veto membuang tanda PANAS


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
    """Pemangkin v3: A >= 3 (K2), B 2 (earnings 6–21 hari lagi), C 1 (1–5 hari lagi), D 0 (tiada); E < 0 (tidak dipakai)."""
    if mata is None:
        return TIADA
    return 'A' if mata >= 3 else 'B' if mata >= 2 else 'C' if mata >= 1 else 'D' if mata >= 0 else 'E'


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
            u = round(sl / sp - 1, 6)
            kat = ('naik_sasaran_besar' if u >= 0.10 else 'naik_sasaran' if u > 0 else
                   'potong_sasaran' if u < 0 else None)
        if not kat:
            continue
        out.append({'kategori': kat, 'mata': mata_analisis(kat, sl, sp), 'firma': firma, 'tarikh': tk, 'hari_lalu': h,
                    'sasaran': sl, 'url': L.get('rating_url') or ''})
    return out


def mata_analisis(kat, sl=None, sp=None):
    if kat == 'potong_sasaran':
        return -2 if sl and sp and round(sl / sp - 1, 6) <= -0.10 else -1
    return {'naik_taraf': 2, 'mula_beli': 2, 'naik_sasaran_besar': 2, 'naik_sasaran': 1, 'turun_taraf': -2, 'mula_jual': -2}[kat]


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
        e = {'dikumpul': hari_ini.isoformat(), 'sumber_pemangkin': 'moomoo', 'berita': [], 'analisis': [], 'orang_dalam': {}}
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


# ---------- Sumber percuma: GitHub Actions (pemangkin_actions.py -> data/pemangkin/) ----------
GRED_BELI = re.compile(r'\b(strong buy|buy|outperform|overweight|positive|accumulate|add)\b', re.I)
GRED_JUAL = re.compile(r'\b(sell|underperform|underweight|negative|reduce)\b', re.I)


def berita_yahoo(lst, ticker, nama, hari_ini):
    """yahoo.json saham[T].berita [{tajuk, masa (saat UTC), url}] -> format berita_moomoo (ditapis relevan)."""
    out = []
    for r in lst or []:
        if not isinstance(r, dict) or not r.get('masa') or not relevan(r.get('tajuk'), ticker, nama):
            continue
        tk, st = masa_ny(float(r['masa']))
        out.append({'tajuk': bersih(r.get('tajuk'))[:200], 'tarikh': tk, 'selepas_tutup': st,
                    'hari_lalu': max((hari_ini - date.fromisoformat(tk)).days, 0), 'url': r.get('url') or '',
                    'sumber': 'yahoo'})
    return out


def analisis_yahoo(lst, hari_ini, hari_maks=10):
    """yahoo.json saham[T].analisis (yfinance upgrades_downgrades) -> format analisis_moomoo. Tindakan terkini
    setiap firma (<= 10 hari): up/down = naik/turun taraf; init = mula liputan Beli/Jual (Tahan diabaikan);
    selainnya (main/reit) ubah sasaran berbanding sasaran sebelumnya."""
    out, dilihat = [], set()
    sah = [x for x in lst or [] if isinstance(x, dict) and TARIKH_ISO.match(str(x.get('tarikh') or ''))]
    for x in sorted(sah, key=lambda x: x['tarikh'], reverse=True):
        firma = x.get('firma') or ''
        if firma in dilihat:
            continue
        dilihat.add(firma)
        h = (hari_ini - date.fromisoformat(x['tarikh'])).days
        if h > hari_maks or h < 0:
            continue
        tin, ke, sl, sp = str(x.get('tindakan') or '').lower(), str(x.get('ke') or ''), x.get('sasaran'), x.get('sasaran_lalu')
        kat = None
        if tin == 'up':
            kat = 'naik_taraf'
        elif tin == 'down':
            kat = 'turun_taraf'
        elif tin == 'init':
            kat = 'mula_jual' if GRED_JUAL.search(ke) else 'mula_beli' if GRED_BELI.search(ke) else None
        elif sl and sp:
            u = round(sl / sp - 1, 6)
            kat = 'naik_sasaran_besar' if u >= 0.10 else 'naik_sasaran' if u > 0 else 'potong_sasaran' if u < 0 else None
        if kat:
            out.append({'kategori': kat, 'mata': mata_analisis(kat, sl, sp), 'firma': firma, 'tarikh': x['tarikh'],
                        'hari_lalu': h, 'sasaran': sl, 'url': ''})
    return out


def orang_dalam_yahoo(lst, hari_ini, hari_maks=30):
    """yahoo.json saham[T].orang_dalam (belian sahaja) -> {bilangan orang dalam berbeza, tarikh terkini}."""
    nama, akhir = set(), None
    for r in lst or []:
        t = str(r.get('tarikh') or '')[:10]
        if (r.get('saham') or 0) <= 0 or not TARIKH_ISO.match(t) or not 0 <= (hari_ini - date.fromisoformat(t)).days <= hari_maks:
            continue
        nama.add(r.get('nama') or '?'); akhir = max(akhir or t, t)
    return {'bilangan': len(nama), 'tarikh': akhir} if nama else {}


def _tarikh(x):
    try:
        return date.fromisoformat(str(x or '')[:10])
    except ValueError:
        return None


def baca_nasdaq(path, hari_ini, hari_maks=4):
    """earnings_nasdaq.json -> (saham {T: {lalu, lalu_masa, seterusnya, seterusnya_masa}}, lengkap tanpa ralat hari)
    atau (None, False) jika fail tiada atau bukan bertarikh 0–4 hari sebelum hari_ini."""
    if not path or not os.path.exists(path):
        return None, False
    try:
        d = baca_json(path)
    except ValueError:
        d = None
    t = _tarikh(d.get('tarikh') or d.get('dijana')) if isinstance(d, dict) else None
    if t is None or not 0 <= (hari_ini - t).days <= hari_maks:
        print(f'AMARAN {path} bertarikh {t}; diabaikan (mesti 0–{hari_maks} hari sebelum {hari_ini})')
        return None, False
    return d.get('saham') or {}, d.get('hari_ralat') == 0


def earnings_nasdaq(e, hari_ini):
    """Entri Nasdaq satu saham -> (medan earnings lalu untuk pemangkin, tarikh earnings >= hari_ini atau None).
    Masa 'time-not-supplied' -> earnings_selepas_tutup None (hari reaksi ditentukan oleh volum; reaksi_earnings)."""
    lalu, seter = _tarikh((e or {}).get('lalu')), _tarikh((e or {}).get('seterusnya'))
    out = {}
    if lalu and lalu < hari_ini:
        masa = e.get('lalu_masa') or ''
        out = {'earnings_lalu_tarikh': lalu.isoformat(), 'earnings_lalu_hari': hari_dagangan(lalu, hari_ini),
               'earnings_selepas_tutup': True if masa == 'time-after-hours' else False if masa == 'time-pre-market' else None,
               'earnings_anggaran': (lalu + timedelta(days=91)).isoformat(), 'earnings_gerak_pct': None}
    return out, next((x for x in (lalu, seter) if x and x >= hari_ini), None)


def pemangkin_yahoo(d, hari_ini, nama=None, tickers=None, institusi=None, nas=None, sejak=None):
    """yahoo.json -> ({ticker: entri format kumpul_pemangkin, sumber_pemangkin 'yahoo'}, {'ralat': [...], 'lama': [...]}).
    Hanya fail bertarikh hari_ini (MYT) dan entri yang diambil selepas 6:00 petang MYT hari itu (berita pra-pasaran
    New York sesi imbasan); ticker beralat atau lama tidak dimasukkan (kumpul melalui Moomoo atau '–').
    sejak (saat UTC): sempadan lain bagi saluran Actions (standard/harian_c.py: selepas sesi isyarat tutup)."""
    out, buang = {}, {'ralat': [], 'lama': []}
    if not isinstance(d, dict) or str(d.get('tarikh')) != hari_ini.isoformat():
        return out, buang
    sempadan = sejak if sejak is not None else datetime(hari_ini.year, hari_ini.month, hari_ini.day, 10, tzinfo=timezone.utc).timestamp()
    for t, y in (d.get('saham') or {}).items():
        if tickers is not None and t not in tickers:
            continue
        if y.get('ralat') or (y.get('diambil') or 0) < sempadan:
            buang['ralat' if y.get('ralat') else 'lama'].append(t)
            continue
        e = {'dikumpul': hari_ini.isoformat(), 'sumber_pemangkin': 'yahoo',
             'berita': berita_yahoo(y.get('berita'), t, (nama or {}).get(t, ''), hari_ini),
             'analisis': analisis_yahoo(y.get('analisis'), hari_ini),
             'orang_dalam': orang_dalam_yahoo(y.get('orang_dalam'), hari_ini), 'institusi': (institusi or {}).get(t)}
        if nas is not None:
            e.update(earnings_nasdaq(nas.get(t), hari_ini)[0])
        out[t] = e
    return out, buang


def gred_keseluruhan(gred):
    """Purata mata gred yang ada (A=4 … E=0) -> huruf. Belum diuji; untuk paparan sahaja. Sejak 18 Okt 2026 RS tidak
    dimasukkan (gred RS sudah menggabung pengesahan pasaran; dinilai berasingan)."""
    v = [MATA[g] for g in gred if g in MATA]
    if not v:
        return TIADA
    x = sum(v) / len(v)
    return 'A' if x >= 3.5 else 'B' if x >= 2.5 else 'C' if x >= 1.5 else 'D' if x >= 0.5 else 'E'


def isi_rs(r, x, spy_atas):
    """Isi lajur RS satu baris daripada satu baris `rs_semua` (atau None)."""
    nil = lambda k: None if x is None or k not in x or pd.isna(x[k]) else float(x[k])
    rs = nil('rs')
    rs = None if rs is None else int(rs)
    m12, mf, ri = nil('mutlak12'), nil('mansfield'), nil('rs_industri')
    sah = disahkan(m12, mf, spy_atas)
    r['rs_rating'] = '' if rs is None else rs
    r['gred_rs'] = gred_rs(rs, sah)
    r['rs_sah'] = '' if rs is None or sah is None else 'ya' if sah else 'tidak'
    r['rs_tanda'] = tanda_rs(rs, m12, mf, spy_atas)
    r['rs_industri'] = '' if ri is None else int(ri)
    r['rs_sumber'] = '' if rs is None else x['rs_sumber']


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
    nama, semua = {}, set()
    for f in a.csv or []:
        for r in csv.DictReader(open(f, newline='', encoding='utf-8')):
            t, n = ambil(r, 'saham', 'Saham'), ambil(r, 'nama', 'Nama')
            if t:
                semua.add(t)
            if t and n:
                nama[t] = n
    ins = json.load(open(a.institusi, encoding='utf-8')) if a.institusi else {}
    nas = baca_nasdaq(a.nasdaq, hari_ini)[0] if getattr(a, 'nasdaq', None) else None
    if a.folder and not os.path.isdir(a.folder):
        print(f'AMARAN folder {a.folder} tiada; fail mentah Moomoo dilangkau')
    baru = kumpul_pemangkin(a.folder, nama, hari_ini, ins) if a.folder and os.path.isdir(a.folder) else {}
    if nas is not None:
        for t, e in baru.items():
            if 'earnings_lalu_tarikh' not in e:
                e.update(earnings_nasdaq(nas.get(t), hari_ini)[0])
    lama = json.load(open(a.keluar, encoding='utf-8')) if os.path.exists(a.keluar) else {}
    n_mm, n_yh, yh_buang = len(baru), 0, {}
    if getattr(a, 'yahoo', None):
        try:
            d = baca_json(a.yahoo) if os.path.exists(a.yahoo) else {}
        except ValueError:
            d = {}
        if not isinstance(d, dict) or str(d.get('tarikh')) != a.tarikh:
            print(f'AMARAN {a.yahoo} tiada / bukan bertarikh {a.tarikh}: data Yahoo tidak dipakai')
            d = {}
        sejak = datetime.fromisoformat(a.sejak.replace('Z', '+00:00')).timestamp() if getattr(a, 'sejak', None) else None
        yh, yh_buang = pemangkin_yahoo(d, hari_ini, nama, semua if a.csv else None, ins, nas, sejak)
        for t, e in yh.items():
            l = lama.get(t) or {}
            # data Moomoo (dikumpul khusus bagi saham itu) hari ini diutamakan; Yahoo hanya mengisi yang belum ada
            if t in baru or (l.get('dikumpul') == a.tarikh and l.get('sumber_pemangkin', 'moomoo') != 'yahoo'):
                continue
            baru[t] = e; n_yh += 1
    # gabung: entri baharu menggantikan; entri lama > 5 hari dagangan dibuang
    gab = {t: e for t, e in lama.items() if segar(e, hari_ini, 5)}
    gab.update(baru)
    with open(a.keluar, 'w', encoding='utf-8') as f:
        json.dump(dict(sorted(gab.items())), f, ensure_ascii=False, indent=1)
    tanpa_nama = sorted(t for t in baru if t not in nama)
    print(f'{len(baru)} saham dikumpul ({n_mm} Moomoo, {n_yh} Yahoo); {sum(1 for e in baru.values() if e["berita"])} ada berita relevan; '
          f'{sum(1 for e in baru.values() if e["analisis"])} ada tindakan analisis; jumlah dalam fail {len(gab)}')
    if a.csv:
        hari = sorted(t for t in semua if (gab.get(t) or {}).get('dikumpul') != a.tarikh)
        print(f'{len(hari)} saham CSV belum ada entri hari ini' + (': ' + ' '.join(hari) if hari else ''))
    for k, v in yh_buang.items():
        if v:
            print(f'{len(v)} saham Yahoo tidak dipakai ({k}):', ' '.join(sorted(v)))
    if tanpa_nama:
        print('AMARAN tiada nama syarikat (tapisan relevan guna ticker sahaja):', ' '.join(tanpa_nama))


def tambah(a):
    rows = list(csv.DictReader(open(a.csv, newline='', encoding='utf-8')))
    lajur = list(rows[0].keys()) if rows else []
    hari_ini = date.fromisoformat(a.tarikh)
    c, v = muat_harga(a.harga)
    spy = muat_spy(a.harga)
    rsd, spy_atas = rs_semua(c, spy, getattr(a, 'rs', None))
    from sektor_pasaran import SEKTOR_INDUSTRI
    v2 = bool(getattr(a, 'kumpulan', None))
    pind = {}
    if a.peta and os.path.exists(a.peta):
        pind = {r['ticker']: r['industri'] for r in csv.DictReader(open(a.peta, newline='', encoding='utf-8'))}
    if v2:
        # v2 (sejak 19 Okt 2026): Weinstein + 1 bulan (industri), % > SMA200 (sektor); fail basi/tiada -> "–"
        ksek, kind, ktarikh = peta_kumpulan(a.kumpulan, hari_ini)
        if not kind:
            print(f'AMARAN: gred_kumpulan tiada atau basi (tarikh {ktarikh}); gred sektor/industri "–"')
    else:
        sek, ind = peta_sektor(a.sektor)
        pusek, puind = {}, {}
        if a.pasaran and pind and os.path.exists(a.pasaran):
            pusek, puind = peta_pasaran(a.pasaran)
    jenis = peta_jenis_kaedah()
    ear = peta_earnings(a.acara, hari_ini) if a.acara else None
    nas, nas_lengkap = baca_nasdaq(a.nasdaq, hari_ini) if getattr(a, 'nasdaq', None) else (None, False)
    pem = json.load(open(a.pemangkin, encoding='utf-8')) if a.pemangkin else {}
    for r in rows:
        t = ambil(r, 'saham', 'Saham')
        iu = pind.get(t); su = SEKTOR_INDUSTRI.get(iu) if iu else None
        r['industri_us'] = iu or ''; r['sektor_us'] = su or ''
        if v2:
            s1, g1 = ksek.get(su, (None, TIADA)); s2, g2 = kind.get(iu, (None, TIADA))
        else:
            s1 = pusek.get(su) if su in pusek else sek.get(ambil(r, 'sektor', 'Sektor'))
            s2 = puind.get(iu) if iu in puind else ind.get(ambil(r, 'industri', 'Industri'))
            g1, g2 = gred_kumpulan(s1), gred_kumpulan(s2)
        r['skor_sektor'] = '' if s1 is None else round(s1, 1); r['gred_sektor'] = g1
        r['skor_industri'] = '' if s2 is None else round(s2, 1); r['gred_industri'] = g2
        isi_rs(r, rsd.loc[t] if t in rsd.index else None, spy_atas)
        te, sumber = (ear or {}).get(t), 'SST'
        if te is None and nas is not None:
            d = earnings_nasdaq(nas.get(t), hari_ini)[1]
            if d:
                te, sumber = d, 'Nasdaq'
        if te is None and (pem.get(t) or {}).get('earnings_anggaran'):
            te, sumber = date.fromisoformat(pem[t]['earnings_anggaran']), 'anggaran'
            if te < hari_ini:
                te = None
        # Nasdaq tanpa ralat dan saham itu ada earnings lalu dalam kalendar -> ketiadaan tarikh hadapan boleh dipercayai
        liput_nas = nas is not None and nas_lengkap and bool((nas.get(t) or {}).get('lalu'))
        h = None
        if te is None and ear is None and not liput_nas:
            r['tarikh_earnings'] = ''; r['hari_ke_earnings'] = ''; r['sumber_earnings'] = 'tiada data'; r['gred_qr'] = TIADA
        else:
            h = hari_dagangan(hari_ini, te) if te else None
            lalu = [_tarikh(((nas or {}).get(t) or {}).get('lalu')), _tarikh((pem.get(t) or {}).get('earnings_lalu_tarikh'))]
            sj = sejak_qr(max((d for d in lalu if d and d < hari_ini), default=None), hari_ini)
            r['tarikh_earnings'] = te.isoformat() if te else ''
            r['hari_ke_earnings'] = '' if h is None else h
            r['sumber_earnings'] = tanda_pasca_qr(sumber if te else 'tiada dalam 30 hari (SST)' if ear is not None
                                                  else 'tiada dalam 35 hari (Nasdaq)', sj)
            r['gred_qr'] = gred_qr(h, sj)
        # Pemangkin v3: K1 (earnings seterusnya, sama seperti QR) dan K2 (reaksi earnings lalu daripada stor harga)
        # tidak memerlukan pemangkin.json; berita (veto dan pautan) hanya jika entri segar ada.
        p = dict(pem[t]) if t in pem and segar(pem[t], hari_ini) else {}
        if nas is not None and 'earnings_lalu_tarikh' not in p:
            p.update(earnings_nasdaq(nas.get(t), hari_ini)[0])
        if r['gred_qr'] == TIADA and not p.get('earnings_lalu_tarikh') and not p.get('berita'):
            r['mata_pemangkin'] = ''; r['pemangkin'] = 'belum dikumpul'; r['gred_pemangkin'] = TIADA
            r['pemangkin_url'] = ''
        else:
            ada = t in c.columns
            m, g, ring = nilai_pemangkin(p, hari_ini, h, c[t] if ada else None, v[t] if ada else None, spy)
            r['mata_pemangkin'] = m; r['pemangkin'] = ring; r['gred_pemangkin'] = g
            r['pemangkin_url'] = pautan_berita(p.get('berita'), hari_ini=hari_ini)
        if v2:
            # v2: Sektor paparan sahaja; Industri tidak terpakai bagi kaedah pantulan (kajian 18 Okt 2026)
            gi = TIADA if jenis.get(id_kaedah(ambil(r, 'kaedah', 'Kaedah'))) == 'pantulan' else r['gred_industri']
            r['gred_keseluruhan'] = gred_keseluruhan([gi, r['gred_pemangkin'], r['gred_qr']])
        else:
            r['gred_keseluruhan'] = gred_keseluruhan([r['gred_sektor'], r['gred_industri'], r['gred_pemangkin'], r['gred_qr']])
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
    t.add_argument('--kumpulan', help='data/kumpulan/gred_kumpulan.csv (v2, utama sejak 19 Okt 2026; Actions gred_kumpulan.yml)')
    t.add_argument('--sektor', help='papertrade/sektor.csv (v1, hanya jika --kumpulan tidak diberi)')
    t.add_argument('--pasaran', help='papertrade/sektor_pasaran.csv (utama: seluruh pasaran AS)')
    t.add_argument('--peta', help='papertrade/peta_industri.csv (ticker -> industri Moomoo)')
    t.add_argument('--acara', help='JSON SST market_events (daysLookahead 30)')
    t.add_argument('--pemangkin', help='papertrade/pemangkin.json (hasil `gred.py kumpul`)')
    t.add_argument('--nasdaq', help='data/pemangkin/earnings_nasdaq.json (Actions): tarikh earnings kedua selepas SST')
    t.add_argument('--rs', default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'rs'),
                   help='folder rs_pasaran.csv + status.json (RS seluruh pasaran AS; sandaran stor harga)')
    t.add_argument('--tarikh', required=True, help='tarikh imbasan YYYY-MM-DD')
    k = sp.add_parser('kumpul', help='fail mentah alat (berita/analisis/orangdalam/earnings/sst_<T>.json) -> pemangkin.json')
    k.add_argument('--folder', help='folder fail mentah alat Moomoo/SST (pilihan jika --yahoo diberi)')
    k.add_argument('--yahoo', help='data/pemangkin/yahoo.json (Actions; dipakai jika bertarikh --tarikh)')
    k.add_argument('--nasdaq', help='data/pemangkin/earnings_nasdaq.json (Actions; earnings lalu bagi saham tanpa fail earnings_)')
    k.add_argument('--csv', nargs='*', help='senarai_beli.csv / watchlist.csv (nama syarikat untuk tapisan relevan)')
    k.add_argument('--institusi', help='JSON {ticker: "kumpul"|"agih"} daripada SST institutional_flow')
    k.add_argument('--keluar', required=True, help='papertrade/pemangkin.json (digabung dengan entri sedia ada)')
    k.add_argument('--tarikh', required=True)
    k.add_argument('--sejak', help='ISO UTC: entri Yahoo yang diambil selepas masa ini dipakai (lalai 10:00 UTC --tarikh)')
    e = sp.add_parser('earnings', help='ringkas fail Moomoo earnings_price_history -> JSON')
    e.add_argument('fail'); e.add_argument('--tarikh', required=True)
    a = ap.parse_args(argv)
    if a.cmd == 'tambah':
        if not a.kumpulan and not a.sektor:
            ap.error('tambah memerlukan --kumpulan (v2) atau --sektor (v1)')
        tambah(a)
    elif a.cmd == 'kumpul':
        if not a.folder and not a.yahoo:
            ap.error('kumpul memerlukan --folder atau --yahoo')
        kumpul(a)
    elif a.cmd == 'earnings':
        print(json.dumps(ringkas_earnings(a.fail, date.fromisoformat(a.tarikh))))


if __name__ == '__main__':
    main()
