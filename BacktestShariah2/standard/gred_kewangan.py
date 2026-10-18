# Gred kewangan v7 (A–E): kekukuhan (K), keuntungan (U), pertumbuhan (T), arah suku terkini (S),
# bendera forensik (F), label peringkat, penunjuk keyakinan, jarak Syariah. Spec: spec/GRED_KEWANGAN_v7.md.
# Semua nisbah dikira sendiri daripada penyata mentah Moomoo (suku tunggal); nisbah siap Moomoo tidak dipakai.
#
# Guna:
#   python3 gred_kewangan.py simpan --folder <fail mentah alat> --keluar BacktestShariah2/data/kewangan
#       fail mentah: <T>_<jenis>_<tempoh>[_pN].json (jenis 1 pendapatan / 2 kunci kira-kira / 3 aliran tunai;
#       tempoh 9 = suku tunggal, 7 = tahunan), <T>_eph.json (quote_financials_earnings_price_history),
#       <T>_snap.json (quote_market_snapshot, pilihan: issued_shares)
#   python3 gred_kewangan.py kira --kewangan BacktestShariah2/data/kewangan --harga <stor harga> --tarikh YYYY-MM-DD T [T ...]
import sys, os, re, json, glob, math, argparse
from datetime import date, datetime, timedelta, timezone

GRED = ['A', 'B', 'C', 'D', 'E']
MATA = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
TIADA = '–'
KOS_MODAL = 0.09          # anggaran kos modal (andaian; julat Enron 7–9%)
HAD_IC = 100.0            # had liputan faedah
PEER_MIN = 5              # bilangan rakan industri minimum untuk median
MCAP_HAD = 0.30           # had hutang/tunai berbanding purata nilai pasaran (DJIM 2026; S&P)
ASET_HAD = 0.33           # had hutang/tunai berbanding jumlah aset (MSCI/FTSE/SC)
PENDAPATAN_HAD = 0.05     # pendapatan faedah / hasil (AAOIFI)

P, K, T = 'pendapatan', 'kunci', 'tunai'   # bahagian penyata
JENIS = {'1': P, '2': K, '3': T}


# ---------- normalisasi data mentah Moomoo ----------
def tamat_tempoh(ms):
    """date_time Moomoo = tengah malam UTC+8 pada tarikh akhir tempoh."""
    return (datetime.fromtimestamp(ms / 1000, tz=timezone.utc) + timedelta(hours=8)).date()


def baca_laporan(path):
    d = json.load(open(path, encoding='utf-8'))
    d = d.get('data', d)
    out = []
    for r in d.get('report_list') or []:
        out.append({'tamat': tamat_tempoh(r['date_time']).isoformat(), 'label': r.get('period_text', ''),
                    'medan': {it['display_name']: it['data'] for it in r.get('item_list') or []
                              if isinstance(it.get('data'), (int, float))}})
    return out


def gabung_tempoh(senarai):
    """{tamat: {'tamat','label', P:{}, K:{}, T:{}}} -> senarai menaik ikut tarikh akhir."""
    ix = {}
    for bahagian, laporan in senarai:
        for r in laporan:   # kunci = label tempoh (tarikh akhir boleh berbeza 1 hari antara penyata)
            e = ix.setdefault(r['label'] or r['tamat'], {'tamat': r['tamat'], 'label': r['label'], P: {}, K: {}, T: {}})
            e[bahagian].update(r['medan'])
    return sorted(ix.values(), key=lambda e: e['tamat'])


def baca_terbit(path):
    """quote_financials_earnings_price_history -> {label: {'pub': 'YYYY-MM-DD', 'jenis': 0|1|2}} (tanpa is_current)."""
    d = json.load(open(path, encoding='utf-8'))
    d = d.get('data', d)
    out = {}
    for r in d.get('records') or []:
        if r.get('is_current') or not r.get('period_text') or not r.get('pub_trading_day_str'):
            continue
        out.setdefault(r['period_text'], {'pub': r['pub_trading_day_str'][:10], 'jenis': int(r.get('pub_type') or 0)})
    return out


def simpan(folder, keluar, tarikh):
    os.makedirs(keluar, exist_ok=True)
    fail = glob.glob(os.path.join(folder, '*_[123]_[79]*.json'))
    tickers = sorted({os.path.basename(f).split('_')[0] for f in fail})
    for t in tickers:
        suku, tahun = [], []
        for f in sorted(glob.glob(os.path.join(folder, f'{t}_[123]_[79]*.json'))):
            m = re.match(rf'{re.escape(t)}_([123])_([79])', os.path.basename(f))
            (suku if m.group(2) == '9' else tahun).append((JENIS[m.group(1)], baca_laporan(f)))
        p = os.path.join(keluar, f'{t}.json')
        lama = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
        k = {'ticker': t, 'dikumpul': tarikh,
             'suku': gabung_lama(lama.get('suku'), gabung_tempoh(suku)),
             'tahunan': gabung_lama(lama.get('tahunan'), gabung_tempoh(tahun)),
             'terbit': dict(lama.get('terbit') or {}), 'saham_terbit': lama.get('saham_terbit')}
        pe = os.path.join(folder, f'{t}_eph.json')
        if os.path.exists(pe):
            k['terbit'].update(baca_terbit(pe))
        ps = os.path.join(folder, f'{t}_snap.json')
        if os.path.exists(ps):
            s = json.load(open(ps, encoding='utf-8'))
            s = s.get('data', s)
            s = s[0] if isinstance(s, list) and s else s
            v = (s or {}).get('issued_shares') if isinstance(s, dict) else None
            if v:
                k['saham_terbit'] = float(v)
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(k, f, ensure_ascii=False, separators=(',', ':'))
        print(f'{t}: {len(k["suku"])} suku, {len(k["tahunan"])} tahun, {len(k["terbit"])} tarikh terbit')
    return tickers


def gabung_lama(lama, baru):
    ix = {e['label'] or e['tamat']: e for e in lama or []}
    for e in baru:
        o = ix.get(e['label'] or e['tamat'])
        if o:   # data baharu menimpa medan sama (penyata semula), medan lain dikekalkan
            for b in (P, K, T):
                o.setdefault(b, {}).update(e[b])
        else:
            ix[e['label'] or e['tamat']] = e
    return sorted(ix.values(), key=lambda e: e['tamat'])


# ---------- pembantu ----------
def nilai(e, bahagian, *nama):
    for n in nama:
        v = (e.get(bahagian) or {}).get(n)
        if v is not None:
            return float(v)
    return None


def hasil(e):
    return nilai(e, P, 'Total Operating Revenue', 'Total Revenue as Reported')


def untung_induk(e):
    return nilai(e, P, 'Net Income to Parent Company', 'Net Income to Common Stockholders', 'Net Profit')


def item_luar_biasa(e):
    """Jumlah pendapatan lain + khas bagi suku bertanda satu_kali (0 jika tidak bertanda)."""
    if not satu_kali(e):
        return 0.0
    return (nilai(e, P, 'Other Income (Expense)') or 0.0) + (nilai(e, P, 'Special Income (Charges)') or 0.0)


def untung_teras(e):
    """Untung bersih induk tolak item luar biasa selepas cukai (kadar cukai suku, had 0–35%)."""
    ni = untung_induk(e)
    x = item_luar_biasa(e)
    if ni is None or not x:
        return ni
    kadar = bahagi(nilai(e, P, 'Tax'), nilai(e, P, 'Pretax Profit'))
    kadar = 0.21 if kadar is None or kadar < 0 else min(kadar, 0.35)
    return ni - x * (1 - kadar)


def eps_teras(e):
    eps, ni = nilai(e, P, 'Diluted EPS'), untung_induk(e)
    nt = untung_teras(e)
    if eps is None or ni is None or nt is None or nt == ni or ni <= 0:
        return eps
    return eps * nt / ni


def hutang(e):
    st = nilai(e, K, 'Short-Term Debt and Capital Lease Obligation') or 0.0
    lt = nilai(e, K, 'Long Term Debt and Capital Lease Obligation') or 0.0
    return st + lt


def hutang_berfaedah(e):
    """Hutang tanpa liabiliti pajakan (untuk saringan Syariah); sandaran: jumlah hutang."""
    cd, ld = nilai(e, K, '-Current Debt'), nilai(e, K, '-Long Term Debt')
    if cd is None and ld is None:
        return hutang(e)
    return (cd or 0.0) + (ld or 0.0)


def ekuiti_induk(e):
    v = nilai(e, K, "Stockholders' Equity")
    if v is not None:
        return v
    te = nilai(e, K, 'Total Equity')
    return None if te is None else te - (nilai(e, K, 'Minority Interests') or 0.0)


def bahagi(a, b):
    if a is None or b is None or b == 0:
        return None
    return a / b


def tarikh(s):
    return date.fromisoformat(s) if isinstance(s, str) else s


def tersedia(e, terbit, hari_ini):
    """Tempoh dianggap diketahui pasaran: tarikh siaran (+1 hari jika selepas tutup), sandaran akhir + 45/60 hari."""
    t = (terbit or {}).get(e['label'])
    if t:
        d = tarikh(t['pub']) + timedelta(days=1 if t.get('jenis') == 2 else 0)
    else:
        d = tarikh(e['tamat']) + timedelta(days=60 if e['label'].endswith(('Q4', 'FY')) else 45)
    return d <= hari_ini


def suku_berturut(suku):
    """Rantaian suku berturut di hujung senarai (jarak 75–110 hari)."""
    out = []
    for e in reversed(suku):
        if out and not 75 <= (tarikh(out[-1]['tamat']) - tarikh(e['tamat'])).days <= 110:
            break
        out.append(e)
    return list(reversed(out))


def jumlah(qs, f):
    v = [f(e) for e in qs]
    return None if not v or any(x is None for x in v) else sum(v)


def huruf(mata):
    return 'A' if mata >= 3.5 else 'B' if mata >= 2.5 else 'C' if mata >= 1.5 else 'D' if mata >= 0.5 else 'E'


def turun(g, n=1):
    return g if g == TIADA else GRED[min(4, GRED.index(g) + n)]


def had_atas(g, had):
    """g tidak boleh lebih baik daripada had."""
    if g == TIADA or had == TIADA:
        return g
    return GRED[max(GRED.index(g), GRED.index(had))]


def gred_semakan(semak, minimum=4):
    """semak: {nama: True/False/None}. 6/6 = A, >= 5/6 B, >= 3/6 C, >= 2/6 D, selainnya E (berkadar)."""
    v = [x for x in semak.values() if x is not None]
    if len(v) < minimum:
        return TIADA
    f = sum(v) / len(v) + 1e-9
    return 'A' if f >= 1 else 'B' if f >= 5 / 6 else 'C' if f >= 0.5 else 'D' if f >= 2 / 6 else 'E'


def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


# ---------- metrik TTM ----------
def satu_kali(e):
    """Suku dengan pendapatan lain/khas besar: > 5% hasil atau > 20% untung sebelum cukai."""
    r, pt = hasil(e), nilai(e, P, 'Pretax Profit')
    for n in ('Other Income (Expense)', 'Special Income (Charges)'):
        v = nilai(e, P, n)
        if v is None or v == 0:
            continue
        if (r and abs(v) > 0.05 * abs(r)) or (pt and abs(v) > 0.20 * abs(pt)):
            return True
    return False


def q4_ragu(e, sebelum):
    """Q4 Moomoo = tahunan − 9 bulan: tanda jika baris kos negatif, belanja > 2x purata Q1–Q3,
    atau caj khas bertentangan tanda dengan Q1–Q3."""
    if not e['label'].endswith('Q4'):
        return False
    for n in ('Cost of Revenue', 'Research & Development', 'Selling and Admin Expenses'):
        v = nilai(e, P, n)
        if v is not None and v < 0:
            return True
    lain = [x for x in sebelum if x['label'][:4] == e['label'][:4]][-3:]
    ox = [nilai(x, P, 'Operating Expense') for x in lain]
    o = nilai(e, P, 'Operating Expense')
    if o is not None and ox and all(v is not None for v in ox) and o > 2 * (sum(ox) / len(ox)) > 0:
        return True
    sp = nilai(e, P, 'Special Income (Charges)')
    sl = [nilai(x, P, 'Special Income (Charges)') for x in lain]
    sl = sum(v for v in sl if v is not None)
    r = hasil(e)
    if sp and sl and sp * sl < 0 and r and abs(sp) > 0.05 * abs(r):
        return True
    return False


def ttm(qs, semua):
    """Metrik 12 bulan daripada 4 suku berturut (qs). semua = senarai suku penuh (untuk semakan Q4)."""
    q = qs[-4:]
    i0 = semua.index(q[0])
    ragu = any(q4_ragu(e, semua[max(0, i0 + j - 3):i0 + j]) for j, e in enumerate(q))
    m = {'hasil': jumlah(q, hasil), 'untung_kasar': jumlah(q, lambda e: nilai(e, P, 'Gross Profit')),
         'op': jumlah(q, lambda e: nilai(e, P, 'Operating Profit')),
         'pretax': jumlah(q, lambda e: nilai(e, P, 'Pretax Profit')),
         'cukai': jumlah(q, lambda e: nilai(e, P, 'Tax')),
         'ni': jumlah(q, untung_teras), 'ni_lapor': jumlah(q, untung_induk),
         'ni_satu': jumlah(q, lambda e: (nilai(e, P, 'Net Profit') or 0.0) - ((untung_induk(e) or 0.0) - (untung_teras(e) or 0.0))),
         'ni_cont': jumlah(q, lambda e: nilai(e, T, 'Net Income from Continuing Operations') or untung_induk(e)),
         'eps': jumlah(q, eps_teras),
         'da': jumlah(q, lambda e: nilai(e, T, 'Depreciation & Depletion & Amortization')),
         'ocf': jumlah(q, lambda e: nilai(e, T, 'Operating Cash Flow')),
         'dwc': jumlah(q, lambda e: nilai(e, T, 'Change in Working Capital')),
         'fcf': jumlah(q, lambda e: nilai(e, T, 'Free Cash Flow')),
         'terbitan': jumlah(q, lambda e: nilai(e, T, 'Net Common Stock Issuance') or 0.0),
         'sga': jumlah(q, lambda e: nilai(e, P, 'Selling and Admin Expenses')),
         'pend_faedah': jumlah(q, lambda e: nilai(e, P, 'Non-Operating Interest Income') or 0.0),
         'q4_ragu': ragu, 'satu_kali': any(satu_kali(e) for e in q)}
    fa = [nilai(e, P, 'Non-Operating Interest Expense') for e in q]
    m['faedah'] = None if any(v is None for v in fa) else sum(fa)
    # EBIT teras: untung operasi; tetingkap Q4 ragu -> untung sebelum cukai + faedah
    if ragu and m['pretax'] is not None:
        m['ebit'] = m['pretax'] + (m['faedah'] or 0.0)
    else:
        m['ebit'] = m['op']
    m['ebitda'] = None if m['ebit'] is None or m['da'] is None else m['ebit'] + m['da']
    m['ffo'] = None if m['ocf'] is None else m['ocf'] - (m['dwc'] or 0.0)
    kadar = bahagi(m['cukai'], m['pretax']) if (m['pretax'] or 0) > 0 else None
    m['kadar_cukai'] = 0.21 if kadar is None else min(max(kadar, 0.0), 0.35)
    m['nopat'] = None if m['ebit'] is None else m['ebit'] * (1 - m['kadar_cukai'])
    return m


def imbangan(e):
    ca, cl = nilai(e, K, 'Total Current Assets'), nilai(e, K, 'Total Current Liabilities')
    return {'aset': nilai(e, K, 'Total Assets'), 'liabiliti': nilai(e, K, 'Total Liabilities'), 'ca': ca, 'cl': cl,
            'ncl': nilai(e, K, 'Total Non-Current Liabilities'), 'tunai': nilai(e, K, 'Cash and Cash Equivalents & Short-Term Investments') or 0.0,
            'hutang': hutang(e), 'hutang_pendek': nilai(e, K, 'Short-Term Debt and Capital Lease Obligation') or 0.0,
            'hutang_panjang': nilai(e, K, 'Long Term Debt and Capital Lease Obligation') or 0.0,
            'ekuiti': ekuiti_induk(e), 'ekuiti_jumlah': nilai(e, K, 'Total Equity'), 'ut': nilai(e, K, 'Retained Earnings'),
            'hutang_berfaedah': hutang_berfaedah(e),
            'terima': nilai(e, K, 'Receivables'), 'inventori': nilai(e, K, 'Inventory'),
            'ppe': nilai(e, K, 'Net PPE')}


def modal_dilabur(b):
    """Ekuiti jumlah (termasuk minoriti, selari EBIT disatukan) + hutang − tunai."""
    eq = b['ekuiti_jumlah'] if b['ekuiti_jumlah'] is not None else b['ekuiti']
    if eq is None:
        return None
    return eq + b['hutang'] - b['tunai']


def purata(a, b):
    v = [x for x in (a, b) if x is not None]
    return sum(v) / len(v) if v else None


# ---------- pertumbuhan & tahunan ----------
def tumbuh(baru, lama):
    if baru is None or lama is None or lama <= 0:
        return None
    return baru / lama - 1


def yoy_suku(qs, i, f):
    """Pertumbuhan YoY suku ke-i (indeks negatif) berbanding 4 suku sebelumnya."""
    if len(qs) < 4 - i + 1 or len(qs) + i - 4 < 0:
        return None
    return tumbuh(f(qs[i]), f(qs[i - 4]))


def tahunan_tersedia(tahunan, terbit, hari_ini):
    out = []
    for e in tahunan:
        lbl = e['label'].replace('/FY', '/Q4')
        if tersedia({'label': lbl if lbl in (terbit or {}) else e['label'], 'tamat': e['tamat']}, terbit, hari_ini):
            out.append(e)
    return out


def isi_tahunan(tah, suku):
    """Kunci kira-kira tahunan yang tiada diisi daripada suku yang tamat pada tarikh sama (± 7 hari)."""
    out = []
    for e in tah:
        if not e.get(K):
            q = next((x for x in suku if abs((tarikh(x['tamat']) - tarikh(e['tamat'])).days) <= 7 and x.get(K)), None)
            if q:
                e = dict(e); e[K] = q[K]
        out.append(e)
    return out


def metrik_tahunan(e, e0=None):
    r = hasil(e)
    ni = untung_induk(e)
    eq = ekuiti_induk(e)
    eq0 = ekuiti_induk(e0) if e0 else None
    eqa = purata(eq, eq0)
    return {'hasil': r, 'op': nilai(e, P, 'Operating Profit'), 'eps': nilai(e, P, 'Diluted EPS'), 'ni': ni,
            'roe': None if eqa is None or eqa <= 0 or ni is None else ni / eqa,
            'fcf_hasil': bahagi(nilai(e, T, 'Free Cash Flow'), r),
            'margin_op': bahagi(nilai(e, P, 'Operating Profit'), r)}


def kemeruapan_eps(tah):
    """Sisihan piawai pertumbuhan EPS YoY tahunan (5 tahun terakhir; asas positif sahaja)."""
    g = [tumbuh(tah[i]['eps'], tah[i - 1]['eps']) for i in range(max(1, len(tah) - 5), len(tah))]
    g = [x for x in g if x is not None]
    if len(g) < 4:
        return None
    m = sum(g) / len(g)
    return math.sqrt(sum((x - m) ** 2 for x in g) / (len(g) - 1))


# ---------- pasaran (distance-to-default naif, purata nilai pasaran) ----------
def jarak_mungkir(harga, saham, b):
    """Bharath & Shumway (2008) naif: F = hutang pendek + 0.5 hutang panjang, sigma_D = 0.05 + 0.25 sigma_E, T = 1."""
    if harga is None or saham is None or len(harga) < 200:
        return None
    E = float(harga.iloc[-1]) * saham
    F = b['hutang_pendek'] + 0.5 * b['hutang_panjang']
    if F <= 0:
        return math.inf
    r = harga.iloc[-253:].pct_change().dropna()
    sE = float(r.std() * math.sqrt(252))
    mu = float(harga.iloc[-1] / harga.iloc[-min(253, len(harga))] - 1)
    sD = 0.05 + 0.25 * sE
    sV = E / (E + F) * sE + F / (E + F) * sD
    if sV <= 0:
        return None
    return (math.log((E + F) / F) + (mu - 0.5 * sV ** 2)) / sV


def purata_mcap(harga, saham, bulan):
    if harga is None or saham is None or len(harga) < 21 * bulan * 0.8:
        return None
    return float(harga.iloc[-21 * bulan:].mean()) * saham


# ---------- pengiraan utama ----------
def kewangan_bank(sektor, industri):
    s = f'{sektor} {industri}'.lower()
    return any(k in s for k in ('bank', 'insurance', 'reit', 'financial services', 'capital markets', 'credit services'))


def sub_gred(qs, semua, tah, med, sektor, industri):
    """Kira K, U, T, S dan bahan bantu bagi suku berturut qs (point-in-time). Tanpa pasaran."""
    m = ttm(qs, semua)
    m4 = ttm(qs[:-4], semua) if len(qs) >= 8 else None
    m20 = ttm(qs[:-20], semua) if len(qs) >= 24 else None
    b, b4 = imbangan(qs[-1]), imbangan(qs[-5]) if len(qs) >= 5 else None
    b20 = imbangan(qs[-21]) if len(qs) >= 21 else None
    ut = {}   # butiran
    nota = []
    if m['satu_kali']:
        nota.append('untung_luar_biasa')
    if m['q4_ragu']:
        nota.append('q4_ragu')
    utiliti = 'utilit' in f'{sektor} {industri}'.lower()
    hasil_g = tumbuh(m['hasil'], m4['hasil']) if m4 else None
    margin_op = bahagi(m['ebit'], m['hasil'])
    aset = b['aset'] or None

    # --- peringkat (Damodaran / Lynch) ---
    tah_m = [metrik_tahunan(tah[i], tah[i - 1] if i else None) for i in range(len(tah))]
    vol_eps = kemeruapan_eps(tah_m)
    peringkat = 'lain'
    hasil_turun2 = len(tah_m) >= 3 and all(tah_m[-k]['hasil'] is not None and tah_m[-k - 1]['hasil'] is not None
                                           and tah_m[-k]['hasil'] < tah_m[-k - 1]['hasil'] for k in (1, 2))
    margin_turun = len(tah_m) >= 3 and None not in (tah_m[-1]['margin_op'], tah_m[-3]['margin_op']) \
        and tah_m[-1]['margin_op'] < tah_m[-3]['margin_op']
    med_vol = (med or {}).get('vol_eps')
    if hasil_g is not None and hasil_g > 0.20 and margin_op is not None and margin_op < 0.05:
        peringkat = 'muda'
    elif hasil_turun2 and margin_turun:
        peringkat = 'merosot'
    elif (vol_eps is not None and med_vol is not None and vol_eps > med_vol) or \
            (med_vol is None and str(sektor) in ('Energy', 'Basic Materials')):
        peringkat = 'kitaran'
    elif hasil_g is not None and hasil_g >= 0.15 and (margin_op or 0) > 0:
        peringkat = 'tumbuh laju'
    elif hasil_g is not None and hasil_g < 0.10 and (m['fcf'] or 0) > 0:
        peringkat = 'matang'

    # --- K: kekukuhan (S&P standard / medial untuk utiliti) ---
    jalur_de = (1.75, 3.5, 4.5, 5.5) if utiliti else (1.5, 3.0, 4.0, 5.0)
    jalur_ffo = (0.50, 0.23, 0.13, 0.09) if utiliti else (0.60, 0.30, 0.20, 0.12)
    tiada_hutang = aset is not None and b['hutang'] <= 0.01 * aset
    hutang_bersih = b['hutang'] - b['tunai']   # S&P: hutang diselaras tolak tunai
    ut['hutang_bersih'] = hutang_bersih
    larian = None
    if tiada_hutang or (aset is not None and hutang_bersih <= 0.01 * aset):
        g_de = g_ffo = 'A'
    else:
        de = bahagi(hutang_bersih, m['ebitda']) if (m['ebitda'] or 0) > 0 else None
        ffo = bahagi(m['ffo'], hutang_bersih)
        ut['hutang_ebitda'] = de; ut['ffo_hutang'] = ffo
        g_de = TIADA if m['ebitda'] is None else 'E' if de is None else \
            next((g for g, h in zip('ABCD', jalur_de) if de < h), 'E')
        g_ffo = TIADA if ffo is None else next((g for g, h in zip('ABCD', jalur_ffo) if ffo > h), 'E')
    gk = [g for g in (g_de, g_ffo) if g != TIADA]
    k = max(gk, key=GRED.index) if gk else TIADA
    # EBITDA negatif: tempoh tunai bertahan (Simply Wall St)
    if (m['ebitda'] or 0) <= 0 and m['ebitda'] is not None and (m['fcf'] or 0) < 0:
        larian = b['tunai'] / -m['fcf']
        ut['larian_tahun'] = larian
        k = 'D' if larian >= 1 else 'E'
    ic = None
    if m['faedah'] is not None and m['faedah'] > 0 and m['ebit'] is not None:
        ic = min(m['ebit'] / m['faedah'], HAD_IC)
    ut['liputan_faedah'] = ic
    sws = {'aset_semasa>liabiliti_semasa': None if None in (b['ca'], b['cl']) else b['ca'] > b['cl'],
           'aset_semasa>liabiliti_panjang': None if None in (b['ca'], b['ncl']) else b['ca'] > b['ncl'],
           'hutang/ekuiti_tidak_naik_5thn': None if b20 is None or not b['ekuiti'] or not b20['ekuiti'] or b['ekuiti'] <= 0 or b20['ekuiti'] <= 0
           else b['hutang'] / b['ekuiti'] <= b20['hutang'] / b20['ekuiti'] + 1e-9,
           'ebit>5x_faedah': True if tiada_hutang else (None if ic is None else ic >= 5)}
    gagal_sws = [n for n, v in sws.items() if v is False]
    if len(gagal_sws) >= 2:
        k = turun(k)
    z = None
    if aset and b['liabiliti'] and None not in (b['ca'], b['cl'], b['ut'], b['ekuiti'], m['ebit']):
        z = 6.56 * (b['ca'] - b['cl']) / aset + 3.26 * b['ut'] / aset + 6.72 * m['ebit'] / aset + 1.05 * b['ekuiti'] / b['liabiliti']
        if z < 1.10:
            k = had_atas(k, 'D')
    ut['altman_z2'] = z

    # --- U: keuntungan ---
    ic_avg = purata(modal_dilabur(b), modal_dilabur(b4) if b4 else None)
    roic = None if m['nopat'] is None or ic_avg is None else (math.inf if ic_avg <= 0 < m['nopat'] else m['nopat'] / ic_avg if ic_avg > 0 else None)
    eq_avg = purata(b['ekuiti'], b4['ekuiti'] if b4 else None)
    roe = None if m['ni'] is None or eq_avg is None or eq_avg <= 0 or (b['ekuiti'] or 0) <= 0 else m['ni'] / eq_avg
    roa = bahagi(m['ni_satu'], purata(b['aset'], b4['aset'] if b4 else None))   # untung disatukan / aset disatukan
    ut.update(roic=roic, roe=roe, roa=roa, margin_op=margin_op)
    lepas = [x for x in tah_m[-10:] if x['roe'] is not None and x['fcf_hasil'] is not None]
    mampan = None
    if len(lepas) >= 5:
        n = sum(1 for x in lepas if x['roe'] >= 0.15 and x['fcf_hasil'] >= 0.05)
        mampan = n >= (5 if len(lepas) >= 10 else math.ceil(len(lepas) / 2))
    mo5 = tah_m[-6]['margin_op'] if len(tah_m) >= 6 else None
    med_mo = (med or {}).get('margin_op')
    if peringkat == 'kitaran' and len(tah_m) >= 5:   # purata merentas kitaran (5 tahun)
        mos = [x['margin_op'] for x in tah_m[-5:] if x['margin_op'] is not None]
        roes = [x['roe'] for x in tah_m[-5:] if x['roe'] is not None]
        margin_u = sum(mos) / len(mos) if mos else None
        roe_u = sum(roes) / len(roes) if roes else None
    else:
        margin_u, roe_u = margin_op, roe
    u = {'roic>kos_modal': None if roic is None else roic > KOS_MODAL,
         'roe>=15%_dan_roa>=6%': None if roe_u is None or roa is None else (roe_u >= 0.15 and roa >= 0.06),
         'mampan_5_daripada_10_thn': mampan,
         'margin_op>median_industri_dan_tidak_turun': None if margin_u is None or med_mo is None or mo5 is None
         else (margin_u > med_mo and margin_u >= mo5),
         'eps_stabil': None if vol_eps is None or med_vol is None else vol_eps <= med_vol,
         'ocf>untung_bersih': None if m['ocf'] is None or m['ni'] is None else m['ocf'] > m['ni']}
    if peringkat == 'muda':
        mk, mk4 = bahagi(m['untung_kasar'], m['hasil']), bahagi(m4['untung_kasar'], m4['hasil']) if m4 else None
        med_mk = (med or {}).get('margin_kasar')
        u = {'larian>=1thn_atau_fcf+': True if (m['fcf'] or 0) >= 0 else (None if not m['fcf'] else b['tunai'] / -m['fcf'] >= 1),
             'margin_kasar_naik': None if None in (mk, mk4) else mk > mk4,
             'margin_kasar>median_industri': None if None in (mk, med_mk) else mk > med_mk,
             'ocf>untung_bersih': u['ocf>untung_bersih']}
    g_u = gred_semakan(u)

    # --- T: pertumbuhan ---
    eps4 = m4['eps'] if m4 else None
    eps20 = m20['eps'] if m20 else None
    g1, g5 = tumbuh(m['eps'], eps4), tumbuh(m['eps'], eps20)
    g5a = None if g5 is None else (1 + g5) ** 0.2 - 1
    roic_t = None
    if m20 and b20 and m['nopat'] is not None and m20['nopat'] is not None:
        dic = (modal_dilabur(b) or 0) - (modal_dilabur(b20) or 0)
        if modal_dilabur(b) is not None and modal_dilabur(b20) is not None and dic > 0:
            roic_t = (m['nopat'] - m20['nopat']) / dic
    naik8 = None
    if len(qs) >= 12:
        v = [yoy_suku(qs, -i, hasil) for i in range(1, 9)]
        naik8 = None if any(x is None for x in v) else sum(x > 0 for x in v) >= 6
    eps_q = yoy_suku(qs, -1, eps_teras)
    hasil_q = yoy_suku(qs, -1, hasil)
    t = {'eps_ttm>eps_5thn_lalu': None if eps20 is None or eps20 <= 0 or m['eps'] is None else m['eps'] > eps20,
         'roic_tambahan_5thn>kos_modal': None if roic_t is None else roic_t > KOS_MODAL,
         'eps_1thn>purata_5thn': None if g1 is None or g5a is None else g1 > g5a,
         'eps_suku_yoy>=18%': None if eps_q is None else eps_q >= 0.18,
         'jualan_suku_yoy>=20%': None if hasil_q is None else hasil_q >= 0.20,
         'jualan_naik_6_daripada_8_suku': naik8}
    ut.update(eps_suku_yoy=eps_q, jualan_suku_yoy=hasil_q, roic_tambahan=roic_t)
    g_t = gred_semakan(t)

    # --- S: arah suku terkini (YoY) ---
    s = {}
    if len(qs) >= 5:
        e, e4 = qs[-1], qs[-5]
        mk = lambda x: bahagi(nilai(x, P, 'Gross Profit'), hasil(x))
        mo = lambda x: bahagi(nilai(x, P, 'Operating Profit'), hasil(x))
        cr = lambda x: bahagi(nilai(x, K, 'Total Current Assets'), nilai(x, K, 'Total Current Liabilities'))
        da = lambda x: bahagi(hutang(x), nilai(x, K, 'Total Assets'))
        s = {'margin_kasar_naik': None if None in (mk(e), mk(e4)) else mk(e) > mk(e4),
             'margin_op_naik': None if None in (mo(e), mo(e4)) else mo(e) > mo(e4),
             'hutang/aset_tidak_naik': None if None in (da(e), da(e4)) else da(e) <= da(e4) + 1e-12,
             'nisbah_semasa_naik': None if None in (cr(e), cr(e4)) else cr(e) > cr(e4),
             'tiada_terbitan_saham_bersih': None if m['terbitan'] is None else m['terbitan'] <= 0,
             'code33_3_suku_memecut': code33(qs)}
    g_s = gred_semakan(s)

    # --- F: bendera forensik (menurunkan keyakinan sahaja) ---
    f = []
    if b4 and m4 and hasil_g is not None:
        gt = tumbuh(b['terima'], b4['terima'])
        if gt is not None and gt > hasil_g + 0.10:
            f.append('belum_terima>jualan')
        gi = tumbuh(b['inventori'], b4['inventori'])
        if gi is not None and gi > hasil_g + 0.10:
            f.append('inventori>jualan')
    aa = purata(b['aset'], b4['aset'] if b4 else None)
    if None not in (m['ni'], m['ocf'], aa) and aa > 0 and (m['ni'] - m['ocf']) / aa > 0.10:
        f.append('akruan_tinggi')
    bm = beneish(m, m4, b, b4)
    ut['beneish_m'] = bm
    if bm is not None and bm > -1.78:
        f.append('beneish')
    if (m['ebitda'] or 0) > 0 and m['ocf'] is not None and m['ocf'] / m['ebitda'] < 0.5:
        f.append('ocf<50%_ebitda')
    if hasil_g is not None and hasil_g > 0.20 and roic is not None and roic < KOS_MODAL:
        f.append('tumbuh_bakar_nilai')
    return {'K': k, 'U': g_u, 'T': g_t, 'S': g_s, 'semak': {'K': sws, 'U': u, 'T': t, 'S': s}, 'F': f,
            'peringkat': peringkat, 'nota': nota, 'butiran': ut, 'm': m, 'b': b,
            'k_asas': {'hutang_ebitda': g_de, 'ffo_hutang': g_ffo}}


def code33(qs):
    """Minervini: EPS YoY, jualan YoY dan margin bersih memecut 3 suku berturut."""
    if len(qs) < 7:
        return None
    eps = [yoy_suku(qs, -i, eps_teras) for i in (3, 2, 1)]
    jual = [yoy_suku(qs, -i, hasil) for i in (3, 2, 1)]
    mb = [bahagi(untung_induk(qs[-i]), hasil(qs[-i])) for i in (3, 2, 1)]
    if any(x is None for x in eps + jual + mb):
        return None
    return eps[0] < eps[1] < eps[2] and jual[0] < jual[1] < jual[2] and mb[0] < mb[1] < mb[2]


def beneish(m, m4, b, b4):
    """Beneish (1999) 8 pembolehubah, TTM lawan TTM tahun lalu."""
    try:
        r, r0 = m['hasil'], m4['hasil']
        gm, gm0 = m['untung_kasar'] / r, m4['untung_kasar'] / r0
        dsri = (b['terima'] / r) / (b4['terima'] / r0)
        gmi = gm0 / gm
        aqi = (1 - (b['ca'] + b['ppe']) / b['aset']) / (1 - (b4['ca'] + b4['ppe']) / b4['aset'])
        sgi = r / r0
        depi = (m4['da'] / (m4['da'] + b4['ppe'])) / (m['da'] / (m['da'] + b['ppe']))
        sgai = (m['sga'] / r) / (m4['sga'] / r0)
        lvgi = ((b['cl'] + b['hutang_panjang']) / b['aset']) / ((b4['cl'] + b4['hutang_panjang']) / b4['aset'])
        tata = (m['ni_cont'] - m['ocf']) / b['aset']
    except (TypeError, ZeroDivisionError, KeyError):
        return None
    return -4.84 + 0.92 * dsri + 0.528 * gmi + 0.404 * aqi + 0.892 * sgi + 0.115 * depi - 0.172 * sgai + 4.679 * tata - 0.327 * lvgi


def gabung(r):
    """Purata mata K,U,T,S -> huruf; had keseluruhan <= K + 1 huruf."""
    v = [MATA[r[x]] for x in 'KUTS' if r[x] in MATA]
    if r['K'] not in MATA or len(v) < 3:
        return TIADA
    g = huruf(sum(v) / len(v))
    return had_atas(g, GRED[max(0, GRED.index(r['K']) - 1)])


def histerisis(urutan):
    """Ubah 1 huruf hanya jika 2 tempoh berturut menunjuk arah sama; ubah >= 2 huruf terus berlaku."""
    urutan = [g for g in urutan if g in MATA]
    if not urutan:
        return TIADA
    pub, tangguh = urutan[0], 0
    for g in urutan[1:]:
        d = MATA[g] - MATA[pub]
        if abs(d) >= 2:
            pub, tangguh = g, 0
        elif d:
            if tangguh and (tangguh > 0) == (d > 0):
                pub, tangguh = g, 0
            else:
                tangguh = d
        else:
            tangguh = 0
    return pub


def syariah(b, m, harga, saham):
    """Jarak ke had (nilai positif = ruang di bawah had, mata peratus)."""
    out = {}
    aset = b['aset']
    hb = b['hutang_berfaedah']
    if aset:
        out['hutang/aset'] = hb / aset
        out['tunai/aset'] = b['tunai'] / aset
    for bln in (24, 36):
        mc = purata_mcap(harga, saham, bln)
        if mc:
            out[f'hutang/mcap{bln}b'] = hb / mc
            out[f'tunai/mcap{bln}b'] = b['tunai'] / mc
    if m['hasil']:
        out['faedah/hasil'] = (m['pend_faedah'] or 0) / m['hasil']
    jarak = {}
    for k_, v in out.items():
        had = PENDAPATAN_HAD if k_ == 'faedah/hasil' else ASET_HAD if 'aset' in k_ else MCAP_HAD
        jarak[k_] = round((had - v) * 100, 1)
    kaedah = {'aset': [k_ for k_ in jarak if 'aset' in k_], 'mcap24': [k_ for k_ in jarak if 'mcap24' in k_],
              'mcap36': [k_ for k_ in jarak if 'mcap36' in k_]}
    # tunai: Moomoo tidak membezakan deposit Islam/konvensional -> pelanggaran tunai hanya 'gagal_sebahagian'
    faedah_gagal = jarak.get('faedah/hasil', 1) < 0
    gagal = [n for n, ks in kaedah.items() if ks and (faedah_gagal or any(jarak[k_] < 0 for k_ in ks if 'hutang' in k_))]
    gagal_tunai = [n for n, ks in kaedah.items() if ks and any(jarak[k_] < 0 for k_ in ks if 'tunai' in k_)]
    ada = [n for n, ks in kaedah.items() if ks]
    if not ada:
        status = TIADA
    elif len(ada) >= 2 and len(gagal) == len(ada):
        status = 'gagal'
    elif gagal or gagal_tunai:
        status = 'gagal_sebahagian'
    elif any(0 <= v < 2 for v in jarak.values()):
        status = 'hampir_had'
    else:
        status = 'lulus'
    return {'status': status, 'jarak_pp': jarak, 'gagal_kaedah': sorted(set(gagal + gagal_tunai))}


def kira(k, harga=None, hari_ini=None, med=None, sektor='', industri=''):
    """k = kandungan data/kewangan/<T>.json. harga = pd.Series harga tutup (indeks tarikh). med = median industri."""
    hari_ini = hari_ini or date.today()
    if kewangan_bank(sektor, industri):
        return hasil_kosong('bank/insurans/REIT: model lain diperlukan')
    terbit = k.get('terbit') or {}
    suku = [e for e in k.get('suku') or [] if tersedia(e, terbit, hari_ini)]
    qs = suku_berturut(suku)
    if len(qs) < 8:
        return hasil_kosong(f'{len(qs)} suku berturut (< 8)')
    tah = isi_tahunan(tahunan_tersedia(k.get('tahunan') or [], terbit, hari_ini), k.get('suku') or [])
    if (hari_ini - tarikh(qs[-1]['tamat'])).days > 200:
        return hasil_kosong('suku terakhir tamat > 200 hari lalu (data basi)')
    # urutan 3 tempoh untuk histerisis (point-in-time setiap suku)
    urutan = []
    for j in (2, 1, 0):
        q = qs[:len(qs) - j]
        if len(q) >= 8:
            tq = [e for e in tah if tarikh(e['tamat']) <= tarikh(q[-1]['tamat'])]
            rr = sub_gred(q, suku, tq, med, sektor, industri)
            urutan.append(gabung(rr))
    r = sub_gred(qs, suku, tah, med, sektor, industri)
    g_mentah = gabung(r)
    g = histerisis(urutan) if g_mentah != TIADA else TIADA
    # pasaran: distance-to-default naif (had semasa, selepas histerisis)
    hp = None
    if harga is not None:
        import pandas as pd
        hp = harga[harga.index <= pd.Timestamp(hari_ini)].dropna()
    saham = k.get('saham_terbit')
    dd = jarak_mungkir(hp, saham, r['b']) if hp is not None else None
    r['butiran']['jarak_mungkir'] = None if dd is None else (999.0 if dd == math.inf else round(dd, 2))
    if dd is not None and dd != math.inf:
        if dd < 0:
            g = had_atas(g, 'E'); r['K'] = had_atas(r['K'], 'E')
        elif dd < 1:
            g = had_atas(g, 'D'); r['K'] = had_atas(r['K'], 'D')
    sy = syariah(r['b'], r['m'], hp, saham)
    if sy['status'] == 'gagal':
        g = 'E' if g != TIADA else g
    # keyakinan
    semua_semak = [v for d in r['semak'].values() for v in d.values()]
    liputan = sum(v is not None for v in semua_semak) / max(1, len(semua_semak))
    sub = [r[x] for x in 'KUTS' if r[x] in MATA]
    jurang = (max(MATA[x] for x in sub) - min(MATA[x] for x in sub)) if sub else 0
    tahap = 2 if liputan >= 0.9 and jurang <= 2 else 0 if liputan < 0.7 or ('A' in sub and 'E' in sub) else 1
    if r['F']:
        tahap -= 1
    sbc = 'software' in industri.lower() or 'internet' in industri.lower()
    if sbc:
        r['nota'].append('fcf_belum_tolak_sbc'); tahap -= 1
    if sy['status'] in ('gagal_sebahagian', 'hampir_had'):
        tahap -= 1
    yakin = ['rendah', 'sederhana', 'tinggi'][max(0, tahap)]
    bil_semak = sum(len(d) for d in r['semak'].values())
    ring = (f'{g} (K:{r["K"]} U:{r["U"]} T:{r["T"]} S:{r["S"]}) · {r["peringkat"]} · F:{len(r["F"])} · keyakinan {yakin}'
            if g != TIADA else f'– ({len(qs)} suku; sub K:{r["K"]} U:{r["U"]} T:{r["T"]} S:{r["S"]})')
    gagal = {x: [n for n, v in r['semak'][x].items() if v is False] for x in 'KUTS'}
    butiran = {'tempoh': qs[-1]['label'], 'tamat': qs[-1]['tamat'], 'gred_mentah': g_mentah, 'urutan': urutan,
               'gagal': gagal, 'bendera': r['F'], 'nota': r['nota'], 'syariah': sy, 'liputan_semakan': round(liputan, 2),
               'k_asas': r['k_asas'], 'nisbah': {a: (None if v is None else round(v, 4) if abs(v) != math.inf else 999.0)
                                                 for a, v in r['butiran'].items()}, 'bil_semakan': bil_semak}
    return {'gred': g, 'K': r['K'], 'U': r['U'], 'T': r['T'], 'S': r['S'], 'peringkat': r['peringkat'],
            'bendera': r['F'], 'keyakinan': yakin, 'syariah': sy['status'], 'ringkas': ring,
            'tempoh': qs[-1]['label'], 'butiran': butiran}


def hasil_kosong(sebab):
    return {'gred': TIADA, 'K': TIADA, 'U': TIADA, 'T': TIADA, 'S': TIADA, 'peringkat': '', 'bendera': [],
            'keyakinan': '', 'syariah': TIADA, 'ringkas': f'– ({sebab})', 'tempoh': '', 'butiran': {'sebab': sebab}}


def median_industri(folder, industri_saham, hari_ini):
    """Median margin operasi TTM, margin kasar TTM dan kemeruapan EPS bagi setiap industri (>= PEER_MIN rakan)."""
    kumpul = {}
    for t, ind in industri_saham.items():
        p = os.path.join(folder, f'{t}.json')
        if not ind or not os.path.exists(p):
            continue
        k = json.load(open(p, encoding='utf-8'))
        terbit = k.get('terbit') or {}
        suku = [e for e in k.get('suku') or [] if tersedia(e, terbit, hari_ini)]
        qs = suku_berturut(suku)
        if len(qs) < 4:
            continue
        m = ttm(qs, suku)
        tah = isi_tahunan(tahunan_tersedia(k.get('tahunan') or [], terbit, hari_ini), k.get('suku') or [])
        tah_m = [metrik_tahunan(tah[i], tah[i - 1] if i else None) for i in range(len(tah))]
        d = kumpul.setdefault(ind, {'margin_op': [], 'margin_kasar': [], 'vol_eps': []})
        for nm, v in (('margin_op', bahagi(m['ebit'], m['hasil'])), ('margin_kasar', bahagi(m['untung_kasar'], m['hasil'])),
                      ('vol_eps', kemeruapan_eps(tah_m))):
            if v is not None:
                d[nm].append(v)
    out = {}
    for ind, d in kumpul.items():
        out[ind] = {nm: (sorted(v)[len(v) // 2] if len(v) >= PEER_MIN else None) for nm, v in d.items()}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description='Gred kewangan v7')
    sp = ap.add_subparsers(dest='cmd', required=True)
    s = sp.add_parser('simpan', help='fail mentah alat Moomoo -> data/kewangan/<T>.json')
    s.add_argument('--folder', required=True); s.add_argument('--keluar', required=True)
    s.add_argument('--tarikh', default=date.today().isoformat())
    k = sp.add_parser('kira', help='cetak gred kewangan bagi ticker')
    k.add_argument('--kewangan', required=True); k.add_argument('--harga')
    k.add_argument('--tarikh', default=date.today().isoformat()); k.add_argument('ticker', nargs='+')
    a = ap.parse_args(argv)
    if a.cmd == 'simpan':
        simpan(a.folder, a.keluar, a.tarikh)
        return
    hari_ini = date.fromisoformat(a.tarikh)
    c = None
    if a.harga:
        import gred as G
        c, _ = G.muat_harga(a.harga)
    for t in a.ticker:
        p = os.path.join(a.kewangan, f'{t}.json')
        if not os.path.exists(p):
            print(t, '– (tiada data kewangan)'); continue
        h = c[t].dropna() if c is not None and t in c.columns else None
        r = kira(json.load(open(p, encoding='utf-8')), h, hari_ini)
        print(t, r['ringkas'])
        print(json.dumps(r['butiran'], ensure_ascii=False))


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
