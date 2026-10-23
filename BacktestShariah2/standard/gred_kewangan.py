# Gred kewangan v7 (A–E): kekukuhan (K), keuntungan (U), pertumbuhan (T), arah suku terkini (S),
# bendera forensik (F), label peringkat, penunjuk keyakinan, jarak Syariah. Spec: spec/GRED_KEWANGAN_v7.md.
# Semua nisbah dikira sendiri daripada penyata mentah Moomoo (suku tunggal); nisbah siap Moomoo tidak dipakai.
# v7.1 (23 Okt 2026, keputusan pengguna "Penuh"; spec §11–13): sambungan HANYA di tempat peraturan v7 tidak dapat
# mengira (nilai None) — tempoh separuh tahun (pelapor asing: H1 = Q6 kumulatif, H2 = tahunan − H1) dan tahunan,
# sejarah pendek (4–7 suku, keyakinan rendah), peralihan tahun kewangan, aliran tunai lewat/tahunan, median sektor,
# asas EPS/hasil <= 0, tetingkap 5 tahun dipendekkan (>= 2 tahun); model berasingan bank / insurans / REIT. Semakan
# yang dikira melalui sambungan disenaraikan dalam butiran 'semakan_ganti' dan tidak menaikkan liputan keyakinan.
#
# Guna:
#   python3 gred_kewangan.py simpan --folder <fail mentah alat> --keluar BacktestShariah2/data/kewangan
#       fail mentah: <T>_<jenis>_<tempoh>[_pN].json (jenis 1 pendapatan / 2 kunci kira-kira / 3 aliran tunai;
#       tempoh 9 = suku tunggal, 7 = tahunan, 6 = separuh tahun pertama kumulatif Q6), <T>_eph.json
#       (quote_financials_earnings_price_history), <T>_snap.json (quote_market_snapshot, pilihan: issued_shares)
#   python3 gred_kewangan.py kira --kewangan BacktestShariah2/data/kewangan --harga <stor harga> --tarikh YYYY-MM-DD T [T ...]
import sys, os, re, csv, json, glob, math, argparse
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
MAKS_SUKU, MAKS_TAHUN, MAKS_SEPARUH = 60, 15, 15   # had simpanan cache
MEDAN = {   # medan yang dipakai (selainnya dibuang semasa simpan)
    'pendapatan': {'Total Operating Revenue', 'Total Revenue as Reported', 'Cost of Revenue', 'Gross Profit',
                   'Operating Expense', 'Selling and Admin Expenses', 'Research & Development', 'Operating Profit',
                   'Non-Operating Interest Expense', 'Non-Operating Interest Income', 'Other Income (Expense)',
                   'Special Income (Charges)', 'Pretax Profit', 'Tax', 'Net Profit', 'Net Income to Parent Company',
                   'Net Income to Common Stockholders', 'Diluted EPS',
                   # v7.1: susut nilai dalam penyata pendapatan (sandaran D&A), REIT (FFO), bank, insurans
                   'Depreciation & Amortization & Depletion', 'Gain on Sale of Security', 'Asset Impairment Loss',
                   'Net Interest Income', '-Interest Income', '-Interest Expense', 'Non-Interest Income',
                   'Credit Losses Provision', 'Non-Interest Expense', 'Total Premiums Earned', '-Net Premiums Written',
                   'Net Investment Income', 'Total Expenses', 'Loss Adjustment Expense', 'Policy Acquisition Expense',
                   'Underwriting Expenses', '-Interest Expense Non-Operating'},
    'kunci': {'Total Assets', 'Total Current Assets', 'Total Current Liabilities', 'Total Non-Current Liabilities',
              'Total Liabilities', 'Cash and Cash Equivalents & Short-Term Investments',
              'Short-Term Debt and Capital Lease Obligation', 'Long Term Debt and Capital Lease Obligation',
              '-Current Debt', '-Long Term Debt', 'Total Equity', "Stockholders' Equity", 'Minority Interests',
              'Retained Earnings', 'Receivables', 'Inventory', 'Net PPE',
              # v7.1: bank / insurans
              'Net Loan', '-Gross Loan', '-Allowance for Loans and Lease Losses', 'Total Deposits',
              'Cash, Cash Equivalents & Federal Funds Sold', 'Securities Investment',
              'Goodwill and Other Intangible Assets', '-Preferred Stock', 'Total Investments',
              'Policy Holders Liabilities'},
    'tunai': {'Operating Cash Flow', 'Change in Working Capital', 'Depreciation & Depletion & Amortization',
              'Free Cash Flow', 'Net Common Stock Issuance', 'Net Income from Continuing Operations',
              'Cash Dividends Paid'}}
JENIS = {'1': P, '2': K, '3': T}
VERSI = '7.1'
GAP = {4: (70, 125), 2: (150, 220), 1: (330, 400)}   # jarak hari antara akhir tempoh berturut (suku/separuh/tahun)
PERALIHAN = 160          # v7.1: satu jarak suku 126–160 hari dibenarkan jika label melangkau (peralihan tahun kewangan)
BASI = {4: 200, 2: 290, 1: 475}   # tempoh terakhir tamat > N hari lalu -> data basi (tempoh + ~110 hari lapor)
LEWAT_SEPARUH = 90       # H1 separuh tahun tanpa rekod siaran: akhir tempoh + 90 hari (andaian; laporan 6-K)
TUNAI_TAHUNAN = 275      # aliran tunai tahunan sebagai ganti TTM: tamat <= 275 hari sebelum akhir tetingkap
NAMA_TEMPOH = {4: 'suku', 2: 'separuh tahun', 1: 'tahun'}


# ---------- normalisasi data mentah Moomoo ----------
def tamat_tempoh(ms):
    """date_time Moomoo = tengah malam UTC+8 pada tarikh akhir tempoh."""
    return (datetime.fromtimestamp(ms / 1000, tz=timezone.utc) + timedelta(hours=8)).date()


def baca_json_alat(path):
    """Hasil alat MCP: JSON mentah, atau pembungkus [{"type": "text", "text": "<json>"}]."""
    d = json.load(open(path, encoding='utf-8'))
    if isinstance(d, list) and d and isinstance(d[0], dict) and d[0].get('type') == 'text':
        d = json.loads(d[0]['text'])
    return d


def baca_laporan(path):
    d = baca_json_alat(path)
    if d.get('ret_code') not in (None, 0):
        return []
    d = d.get('data', d)
    out = []
    for r in d.get('report_list') or []:
        out.append({'tamat': tamat_tempoh(r['date_time']).isoformat(), 'label': r.get('period_text', ''),
                    'mata_wang': r.get('currency_code') or '', 'struktur': r.get('structure_name') or '',
                    'medan': {it['display_name']: it['data'] for it in r.get('item_list') or []
                              if isinstance(it.get('data'), (int, float))}})
    return out


def kunci_tempoh(ix, r):
    """Kunci gabungan tempoh = label (tarikh akhir boleh berbeza 1 hari antara penyata). v7.1: label sama dengan
    tarikh akhir berbeza > 20 hari (peralihan tahun kewangan, cth. FERG '2025/Q4' Jul dan Dis) = tempoh berasingan."""
    k = r['label'] or r['tamat']
    o = ix.get(k)
    if o is not None and abs((tarikh(o['tamat']) - tarikh(r['tamat'])).days) > 20:
        return f"{k}@{r['tamat']}"
    return k


def gabung_tempoh(senarai):
    """{tamat: {'tamat','label', P:{}, K:{}, T:{}}} -> senarai menaik ikut tarikh akhir."""
    ix = {}
    for bahagian, laporan in senarai:
        for r in laporan:
            e = ix.setdefault(kunci_tempoh(ix, r), {'tamat': r['tamat'], 'label': r['label'], P: {}, K: {}, T: {}})
            e[bahagian].update({n: v for n, v in r['medan'].items() if n in MEDAN[bahagian]})
            if r.get('mata_wang'):
                e['mata_wang'] = r['mata_wang']
    return sorted(ix.values(), key=lambda e: e['tamat'])


def baca_terbit(path):
    """quote_financials_earnings_price_history -> {label: {'pub': 'YYYY-MM-DD', 'jenis': 0|1|2}} (tanpa is_current)."""
    d = baca_json_alat(path)
    d = d.get('data', d)
    out = {}
    for r in d.get('records') or []:
        if r.get('is_current') or not r.get('period_text') or not r.get('pub_trading_day_str'):
            continue
        out.setdefault(r['period_text'], {'pub': r['pub_trading_day_str'][:10], 'jenis': int(r.get('pub_type') or 0)})
    return out


def simpan(folder, keluar, tarikh):
    os.makedirs(keluar, exist_ok=True)
    fail = glob.glob(os.path.join(folder, '*_[123]_[679]*.json'))
    tickers = sorted({os.path.basename(f).split('_')[0] for f in fail})
    for t in tickers:
        suku, tahun, separuh, struktur = [], [], [], []
        for f in sorted(glob.glob(os.path.join(folder, f'{t}_[123]_[679]*.json'))):
            m = re.match(rf'{re.escape(t)}_([123])_([679])', os.path.basename(f))
            lap = baca_laporan(f)
            {'9': suku, '7': tahun, '6': separuh}[m.group(2)].append((JENIS[m.group(1)], lap))
            if m.group(2) == '9':
                struktur += [(r['tamat'], r['struktur']) for r in lap if r.get('struktur')]
        p = os.path.join(keluar, f'{t}.json')
        lama = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
        k = {'ticker': t, 'dikumpul': tarikh,
             'suku': gabung_lama(lama.get('suku'), gabung_tempoh(suku))[-MAKS_SUKU:],
             'tahunan': gabung_lama(lama.get('tahunan'), gabung_tempoh(tahun))[-MAKS_TAHUN:],
             'terbit': dict(lama.get('terbit') or {}), 'saham_terbit': lama.get('saham_terbit')}
        if separuh or lama.get('separuh'):   # v7.1: separuh tahun pertama kumulatif (Q6) pelapor separuh tahun
            k['separuh'] = gabung_lama(lama.get('separuh'), gabung_tempoh(separuh))[-MAKS_SEPARUH:]
        if struktur or lama.get('struktur'):   # format penyata Moomoo terkini (NORMAL/BANK/INSURANCE_MSTAR)
            k['struktur'] = max(struktur)[1] if struktur else lama.get('struktur')
        pe = os.path.join(folder, f'{t}_eph.json')
        if os.path.exists(pe):
            k['terbit'].update(baca_terbit(pe))
        ps = os.path.join(folder, f'{t}_snap.json')
        if os.path.exists(ps):
            s = baca_json_alat(ps)
            s = s.get('data', s) if isinstance(s, dict) else s
            s = s[0] if isinstance(s, list) and s else s
            v = (s or {}).get('issued_shares') if isinstance(s, dict) else None
            if v:
                k['saham_terbit'] = float(v)
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(k, f, ensure_ascii=False, separators=(',', ':'))
        print(f'{t}: {len(k["suku"])} suku, {len(k["tahunan"])} tahun, {len(k.get("separuh") or [])} separuh, '
              f'{len(k["terbit"])} tarikh terbit')
    return tickers


def gabung_lama(lama, baru):
    ix = {}
    for e in lama or []:
        ix[kunci_tempoh(ix, e)] = e
    for e in baru:
        kk = kunci_tempoh(ix, e)
        o = ix.get(kk)
        if o:   # data baharu menimpa medan sama (penyata semula), medan lain dikekalkan
            for b in (P, K, T):
                o.setdefault(b, {}).update(e[b])
        else:
            ix[kk] = e
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
    """Tempoh dianggap diketahui pasaran: tarikh siaran (+1 hari jika selepas tutup), sandaran akhir + 45/60 hari
    (v7.1 separuh tahun: H1 + 90 hari; H2 = tahunan − H1, sama seperti tahunan + 60 hari)."""
    t = (terbit or {}).get(e['label'])
    p = tarikh(t['pub']) if t else None
    # rekod Moomoo kadang tersalah label (cth. FAST 2025/Q4 -> 2027-01-19): hanya dipercayai jika 1–120 hari selepas akhir tempoh
    if p and 0 < (p - tarikh(e['tamat'])).days <= 120:
        d = p + timedelta(days=1 if t.get('jenis') == 2 else 0)
    elif e.get('separuh') and not e['label'].endswith('Q4'):
        d = tarikh(e['tamat']) + timedelta(days=LEWAT_SEPARUH)
    else:
        d = tarikh(e['tamat']) + timedelta(days=60 if e['label'].endswith(('Q4', 'FY')) else 45)
    return d <= hari_ini


def label_seterus(lbl):
    """'2025/Q3' -> '2025/Q4'; '2025/Q4' -> '2026/Q1'; selainnya None."""
    m = re.match(r'(\d{4})/Q([1-4])$', lbl or '')
    if not m:
        return None
    y, q = int(m.group(1)), int(m.group(2))
    return f'{y}/Q{q + 1}' if q < 4 else f'{y + 1}/Q1'


def suku_berturut(suku, n=4, lanjut=False):
    """Rantaian tempoh berturut di hujung senarai. Suku (n=4): jarak 70–125 hari (suku 16 minggu dan tahun 52/53
    minggu); v7.1 (lanjut): satu jarak 126–160 hari dibenarkan jika label tidak bersambung (peralihan tahun kewangan,
    cth. GEF Okt -> Sep 2025). Separuh tahun (n=2): 150–220 hari. Tahunan (n=1): 330–400 hari."""
    lo, hi = GAP[n]
    out, peralihan = [], False
    for e in reversed(suku):
        if out:
            d = (tarikh(out[-1]['tamat']) - tarikh(e['tamat'])).days
            if not lo <= d <= hi:
                if lanjut and n == 4 and not peralihan and hi < d <= PERALIHAN \
                        and label_seterus(e['label']) != out[-1]['label']:
                    peralihan = True
                else:
                    break
        out.append(e)
    return list(reversed(out))


def ada_peralihan(qs, n=4):
    lo, hi = GAP[n]
    return any(not lo <= (tarikh(b['tamat']) - tarikh(a['tamat'])).days <= hi for a, b in zip(qs, qs[1:]))


def tempoh_separuh(k):
    """v7.1: tempoh separuh tahun bagi pelapor separuh tahun (penyata pendapatan/aliran tunai suku tiada). H1 =
    laporan kumulatif Q6; H2 = tahunan − H1 (medan aliran yang ada dalam kedua-duanya; EPS H2 = EPS tahunan − EPS H1,
    anggaran). Kunci kira-kira daripada suku/tahunan yang tamat pada tarikh sama (± 7 hari). Label 'YYYY/Q2' (H1) dan
    'YYYY/Q4' (H2), sepadan dengan rekod tarikh siaran Moomoo."""
    h1s = {e['label'][:4]: e for e in k.get('separuh') or [] if e['label'].endswith('Q6')}
    fy = {e['label'][:4]: e for e in k.get('tahunan') or [] if e['label'].endswith('FY')}
    kk = [x for x in (k.get('suku') or []) + (k.get('tahunan') or []) if x.get(K)]

    def kunci_pada(tamat):
        x = next((x for x in kk if abs((tarikh(x['tamat']) - tarikh(tamat)).days) <= 7), None)
        return dict(x[K]) if x else {}
    out = []
    for y in sorted(h1s):
        h1, f = h1s[y], fy.get(y)
        out.append({'tamat': h1['tamat'], 'label': f'{y}/Q2', 'separuh': True, 'mata_wang': h1.get('mata_wang', ''),
                    P: dict(h1.get(P) or {}), K: kunci_pada(h1['tamat']), T: dict(h1.get(T) or {})})
        if f and tarikh(f['tamat']) > tarikh(h1['tamat']):
            h2 = {'tamat': f['tamat'], 'label': f'{y}/Q4', 'separuh': True, 'mata_wang': f.get('mata_wang', ''),
                  K: kunci_pada(f['tamat'])}
            for b in (P, T):
                a, c = f.get(b) or {}, h1.get(b) or {}
                h2[b] = {n: a[n] - c[n] for n in a if n in c}
            out.append(h2)
    return out


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


def tunai_ganti(q, semua, n, tah):
    """v7.1: aliran tunai tetingkap TTM tiada (10-Q/10-K belum difailkan, atau pelapor asing tanpa aliran tunai suku):
    (a) tetingkap n tempoh berturut terkini yang lengkap, lewat <= 2 tempoh; (b) tahunan terkini (point-in-time) yang
    tamat <= TUNAI_TAHUNAN hari sebelum akhir tetingkap. Untung bersih tetingkap ganti dipulangkan (ni_tunai) supaya
    perbandingan OCF > untung dan akruan memakai tempoh yang sama."""
    ocf = lambda e: nilai(e, T, 'Operating Cash Flow')
    i = next((j for j, e in enumerate(semua) if e is q[-1]), None)
    if i is not None:
        for s in (1, 2):
            j = i - s
            w = semua[j - n + 1:j + 1] if j - n + 1 >= 0 else []
            if len(w) == n and len(suku_berturut(w, n)) == n and all(ocf(e) is not None for e in w):
                return {'ocf': jumlah(w, ocf), 'dwc': jumlah(w, lambda e: nilai(e, T, 'Change in Working Capital')),
                        'fcf': jumlah(w, lambda e: nilai(e, T, 'Free Cash Flow')),
                        'da': jumlah(w, lambda e: nilai(e, T, 'Depreciation & Depletion & Amortization')),
                        'ni_tunai': jumlah(w, untung_teras), 'sumber': f'lewat_{s}_tempoh', 'tamat': w[-1]['tamat']}
    akhir = tarikh(q[-1]['tamat'])
    for e in reversed(tah or []):
        d = (akhir - tarikh(e['tamat'])).days
        if 0 <= d <= TUNAI_TAHUNAN and ocf(e) is not None:
            return {'ocf': ocf(e), 'dwc': nilai(e, T, 'Change in Working Capital'), 'fcf': nilai(e, T, 'Free Cash Flow'),
                    'da': nilai(e, T, 'Depreciation & Depletion & Amortization'), 'ni_tunai': untung_teras(e),
                    'sumber': 'tahunan', 'tamat': e['tamat']}
    return None


def ttm(qs, semua, n=4, tah=None, lanjut=False):
    """Metrik 12 bulan daripada n tempoh berturut terakhir qs (n = 4 suku, 2 separuh tahun, 1 tahun). semua = senarai
    tempoh penuh (semakan Q4 dan aliran tunai ganti); tah = tahunan point-in-time; lanjut = sambungan v7.1."""
    q = qs[-n:]
    ragu = False
    if n == 4:
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
    # v7.1: aliran tunai tetingkap tiada -> ganti (lewat <= 2 tempoh, atau tahunan); D&A tiada -> D&A penyata pendapatan
    m['ni_tunai'], m['tunai_ganti'] = m['ni'], None
    if lanjut and (m['ocf'] is None or m['da'] is None):
        g = tunai_ganti(q, semua, n, tah)
        if m['ocf'] is None and g:
            m.update(ocf=g['ocf'], dwc=g['dwc'], fcf=g['fcf'], ni_tunai=g['ni_tunai'])
            m['tunai_ganti'] = g['sumber']
        if m['da'] is None:
            m['da'] = jumlah(q, lambda e: nilai(e, P, 'Depreciation & Amortization & Depletion'))
            if m['da'] is None and g and g['da'] is not None:
                m['da'] = g['da']; m['tunai_ganti'] = m['tunai_ganti'] or g['sumber']
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


def yoy_suku(qs, i, f, n=4):
    """Pertumbuhan YoY tempoh ke-i (indeks negatif) berbanding n tempoh sebelumnya (setahun lalu)."""
    if len(qs) < n - i + 1 or len(qs) + i - n < 0:
        return None
    return tumbuh(f(qs[i]), f(qs[i - n]))


def pasangan_yoy(qs, i, f, n=4):
    """(nilai tempoh ke-i, nilai setahun lalu) atau (None, None)."""
    if len(qs) < n - i + 1 or len(qs) + i - n < 0:
        return None, None
    return f(qs[i]), f(qs[i - n])


def lulus_tumbuh(baru, lama, ambang):
    """v7.1 (asas <= 0, v7 tidak dikira): asas <= 0 -> lulus hanya jika nilai semasa > 0 (pusing untung / hasil
    pertama); selainnya pertumbuhan >= ambang. None jika mana-mana nilai tiada."""
    if baru is None or lama is None:
        return None
    if lama <= 0:
        return baru > 0
    return baru / lama - 1 >= ambang


def tahunan_tersedia(tahunan, terbit, hari_ini):
    out = []
    for e in tahunan:
        lbl = e['label'].replace('/FY', '/Q4')
        if tersedia({'label': lbl if lbl in (terbit or {}) else e['label'], 'tamat': e['tamat']}, terbit, hari_ini):
            out.append(e)
    return out


def isi_tahunan(tah, suku, lanjut=False):
    """Kunci kira-kira tahunan yang tiada diisi daripada suku yang tamat pada tarikh sama (± 7 hari). v7.1 (lanjut):
    penyata pendapatan / aliran tunai tahunan yang tiada (cth. AMR, ASST 2025/FY) = jumlah 4 suku tahun kewangan sama
    (label YYYY/Q1–Q4, Q4 tamat ± 7 hari daripada akhir tahun; medan yang ada dalam keempat-empat suku)."""
    out = []
    for e in tah:
        if not e.get(K):
            q = next((x for x in suku if abs((tarikh(x['tamat']) - tarikh(e['tamat'])).days) <= 7 and x.get(K)), None)
            if q:
                e = dict(e); e[K] = q[K]
        if lanjut and (not e.get(P) or not e.get(T)):
            fy = e['label'][:4]
            qs = [next((x for x in suku if x['label'] == f'{fy}/Q{i}'), None) for i in (1, 2, 3, 4)]
            if all(qs) and abs((tarikh(qs[3]['tamat']) - tarikh(e['tamat'])).days) <= 7:
                e = dict(e)
                for b in (P, T):
                    if not e.get(b):
                        nama = set.intersection(*(set(x.get(b) or {}) for x in qs))
                        e[b] = {n: sum(x[b][n] for x in qs) for n in nama}
                e['dijumlah_suku'] = True
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
    """Sektor kewangan / hartanah ikut label (v7: semua '–'). v7.1: penghala sebenar ialah jenis_model()."""
    s = f'{sektor} {industri}'.lower()
    return any(k in s for k in ('bank', 'insurance', 'reit', 'financial services', 'capital markets', 'credit services'))


def format_industri(k):
    """Penyata format syarikat biasa (Moomoo NORMAL_MSTAR): aset semasa atau untung operasi wujud dalam 4 suku
    terakhir atau tahunan terakhir."""
    for e in (k.get('suku') or [])[-4:] + (k.get('tahunan') or [])[-1:] + (k.get('separuh') or [])[-1:]:
        if 'Total Current Assets' in (e.get(K) or {}) or 'Operating Profit' in (e.get(P) or {}):
            return True
    return False


def jenis_model(k, sektor, industri):
    """v7.1: 'bank' | 'insurans' | 'reit' | 'standard' | 'tidak_dikenali'. Format penyata Moomoo (structure_name
    BANK_MSTAR / INSURANCE_MSTAR, atau medan khas) diutamakan; label industri sebagai sandaran. Sektor kewangan lain
    (pengurusan aset, pasaran modal, data kewangan, syarikat cangkerang) dengan penyata format biasa -> standard."""
    st = (k.get('struktur') or '').upper()
    akhir = (k.get('suku') or [{}])[-1]
    p_, k_ = akhir.get(P) or {}, akhir.get(K) or {}
    ind = (industri or '').lower()
    if 'BANK' in st or 'Net Interest Income' in p_ or 'Total Deposits' in k_ or ind.startswith('banks'):
        return 'bank'
    if 'INSURANCE' in st or 'Total Premiums Earned' in p_ or 'Policy Holders Liabilities' in k_ or \
            (ind.startswith('insurance') and 'broker' not in ind):
        return 'insurans'
    if 'reit' in ind:
        return 'reit'
    if kewangan_bank(sektor, industri) and not format_industri(k):
        return 'tidak_dikenali'
    return 'standard'


def median_pakai(med, nama, ganti=None, kod='', lanjut=False):
    """Median industri (v7); v7.1 (lanjut): industri < PEER_MIN rakan -> median sektor, kemudian median semua saham
    dalam data/kewangan (semakan ditanda ganti)."""
    v = (med or {}).get(nama)
    for aras in (('sektor', 'semua') if lanjut else ()):
        if v is not None:
            break
        v = ((med or {}).get(aras) or {}).get(nama)
        if v is not None and ganti is not None:
            ganti.add(kod)
    return v


def sub_gred(qs, semua, tah, med, sektor, industri, n=4, lanjut=False, pendek=False):
    """Kira K, U, T, S dan bahan bantu bagi tempoh berturut qs (point-in-time). Tanpa pasaran. n = tempoh setahun
    (4 suku; v7.1: 2 separuh tahun, 1 tahun). lanjut=False: peraturan v7 tepat. lanjut=True: sambungan v7.1 di tempat
    v7 tidak dapat mengira; 'ganti' = semakan yang dikira melalui sambungan. pendek (sejarah < 2 tahun, v7.1):
    minimum 3 semakan boleh dikira bagi setiap sub-gred (bukan 4) dan >= 2 perbandingan hasil YoY."""
    minimum = 3 if pendek else 4
    m = ttm(qs, semua, n, tah, lanjut)
    m4 = ttm(qs[:-n], semua, n, tah, lanjut) if len(qs) >= 2 * n else None
    m20 = ttm(qs[:-5 * n], semua, n, tah, lanjut) if len(qs) >= 6 * n else None
    b, b4 = imbangan(qs[-1]), imbangan(qs[-(n + 1)]) if len(qs) >= n + 1 else None
    b20 = imbangan(qs[-(5 * n + 1)]) if len(qs) >= 5 * n + 1 else None
    # v7.1: sejarah < 5 tahun -> tetingkap terpanjang dalam tahun penuh (>= 2 tahun)
    Lm = 5 if m20 or not lanjut else len(qs) // n - 1
    mL = m20 if m20 or not lanjut else (ttm(qs[:-Lm * n], semua, n, tah, lanjut) if Lm >= 2 else None)
    bLm = b20 if m20 or not lanjut else (imbangan(qs[-(Lm * n + 1)]) if Lm >= 2 else None)
    Lb = 5 if b20 or not lanjut else (len(qs) - 1) // n
    bL = b20 if b20 or not lanjut else (imbangan(qs[-(Lb * n + 1)]) if Lb >= 2 else None)
    ganti = set()
    ut = {}   # butiran
    nota = []
    if m['satu_kali']:
        nota.append('untung_luar_biasa')
    if m['q4_ragu']:
        nota.append('q4_ragu')
    if m['tunai_ganti']:
        nota.append('aliran_tunai_' + m['tunai_ganti'])
    utiliti = 'utilit' in f'{sektor} {industri}'.lower()
    hasil_g = tumbuh(m['hasil'], m4['hasil']) if m4 else None
    margin_op = bahagi(m['ebit'], m['hasil'])
    aset = b['aset'] or None

    # --- peringkat (Damodaran / Lynch): median industri v7 sahaja (sandaran sektor tidak mengubah peringkat) ---
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
    # utiliti (dikawal selia): jadual S&P low volatility; selainnya standard volatility
    jalur_de = (2.0, 4.0, 5.0, 6.0) if utiliti else (1.5, 3.0, 4.0, 5.0)
    jalur_ffo = (0.35, 0.13, 0.09, 0.06) if utiliti else (0.60, 0.30, 0.20, 0.12)
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

    def he_tidak_naik(bb):
        if bb is None or not b['ekuiti'] or not bb['ekuiti'] or b['ekuiti'] <= 0 or bb['ekuiti'] <= 0:
            return None
        return b['hutang'] / b['ekuiti'] <= bb['hutang'] / bb['ekuiti'] + 1e-9
    he = he_tidak_naik(b20)
    if lanjut and he is None and b20 is None and bL is not None:
        he = he_tidak_naik(bL)
        if he is not None:
            ganti.add('K:hutang/ekuiti_tidak_naik_5thn')
    sws = {'aset_semasa>liabiliti_semasa': None if None in (b['ca'], b['cl']) else b['ca'] > b['cl'],
           'aset_semasa>liabiliti_panjang': None if None in (b['ca'], b['ncl']) else b['ca'] > b['ncl'],
           'hutang/ekuiti_tidak_naik_5thn': he,
           'ebit>5x_faedah': True if tiada_hutang else (None if ic is None else ic >= 5)}
    gagal_sws = [n_ for n_, v in sws.items() if v is False]
    if len(gagal_sws) >= 2 and not utiliti:   # utiliti dikawal selia gagal semakan kecairan secara struktur
        k = turun(k)
    z = None
    if aset and b['liabiliti'] and None not in (b['ca'], b['cl'], b['ut'], b['ekuiti'], m['ebit']):
        z = 6.56 * (b['ca'] - b['cl']) / aset + 3.26 * b['ut'] / aset + 6.72 * m['ebit'] / aset + 1.05 * b['ekuiti'] / b['liabiliti']
        if z < 1.10:   # semakan silang sahaja: had D dikenakan dalam kira() jika distance-to-default juga < 2
            nota.append('altman_z2<1.1')
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
        n_ok = sum(1 for x in lepas if x['roe'] >= 0.15 and x['fcf_hasil'] >= 0.05)
        mampan = n_ok >= (5 if len(lepas) >= 10 else math.ceil(len(lepas) / 2))
    elif lanjut and len(lepas) >= 3:   # v7.1: 3–4 tahun -> >= separuh
        mampan = sum(1 for x in lepas if x['roe'] >= 0.15 and x['fcf_hasil'] >= 0.05) >= math.ceil(len(lepas) / 2)
        ganti.add('U:mampan_5_daripada_10_thn')
    mo5 = tah_m[-6]['margin_op'] if len(tah_m) >= 6 else None
    mo5_ganti = False
    if lanjut and mo5 is None and 3 <= len(tah_m) < 6:   # v7.1: margin tahun terawal (>= 2 tahun lalu)
        mo5, mo5_ganti = tah_m[0]['margin_op'], True
    gm = set()
    med_mo = median_pakai(med, 'margin_op', gm, 'U:margin_op>median_industri_dan_tidak_turun', lanjut)
    if peringkat == 'kitaran' and len(tah_m) >= 5:   # purata merentas kitaran (5 tahun)
        mos = [x['margin_op'] for x in tah_m[-5:] if x['margin_op'] is not None]
        roes = [x['roe'] for x in tah_m[-5:] if x['roe'] is not None]
        margin_u = sum(mos) / len(mos) if mos else None
        roe_u = sum(roes) / len(roes) if roes else None
    else:
        margin_u, roe_u = margin_op, roe
    u_roic = None if roic is None else roic > KOS_MODAL
    if lanjut and u_roic is None and m['nopat'] is not None and ic_avg is not None and m['nopat'] <= 0:
        u_roic = False; ganti.add('U:roic>kos_modal')   # v7.1: NOPAT <= 0 dengan modal dilabur <= 0
    u_roe = None if roe_u is None or roa is None else (roe_u >= 0.15 and roa >= 0.06)
    if lanjut and u_roe is None and roe_u is None and roa is not None and \
            ((b['ekuiti'] is not None and b['ekuiti'] <= 0) or (eq_avg is not None and eq_avg <= 0)):
        u_roe = roa >= 0.06; ganti.add('U:roe>=15%_dan_roa>=6%')   # v7.1: ekuiti <= 0 -> ROA sahaja
    u_mo = None if margin_u is None or med_mo is None or mo5 is None else (margin_u > med_mo and margin_u >= mo5)
    if u_mo is not None and (mo5_ganti or gm):
        ganti.add('U:margin_op>median_industri_dan_tidak_turun')
    gv = set()
    med_vol_u = median_pakai(med, 'vol_eps', gv, 'U:eps_stabil', lanjut)
    u_vol = None if vol_eps is None or med_vol_u is None else vol_eps <= med_vol_u
    if u_vol is not None and gv:
        ganti.add('U:eps_stabil')
    if lanjut and u_vol is None and vol_eps is None:   # v7.1 (Graham): EPS tahunan <= 0 dalam 5 tahun -> tidak stabil
        e5 = [x['eps'] for x in tah_m[-5:] if x['eps'] is not None]
        if len(e5) >= 3 and any(x <= 0 for x in e5):
            u_vol = False; ganti.add('U:eps_stabil')
    u_ocf = None if m['ocf'] is None or m['ni_tunai'] is None else m['ocf'] > m['ni_tunai']
    if u_ocf is not None and m['tunai_ganti']:
        ganti.add('U:ocf>untung_bersih')
    u = {'roic>kos_modal': u_roic, 'roe>=15%_dan_roa>=6%': u_roe, 'mampan_5_daripada_10_thn': mampan,
         'margin_op>median_industri_dan_tidak_turun': u_mo, 'eps_stabil': u_vol, 'ocf>untung_bersih': u_ocf}
    if peringkat == 'muda':
        mk, mk4 = bahagi(m['untung_kasar'], m['hasil']), bahagi(m4['untung_kasar'], m4['hasil']) if m4 else None
        gk_ = set()
        med_mk = median_pakai(med, 'margin_kasar', gk_, 'U:margin_kasar>median_industri', lanjut)
        u = {'larian>=1thn_atau_fcf+': True if (m['fcf'] or 0) >= 0 else (None if not m['fcf'] else b['tunai'] / -m['fcf'] >= 1),
             'margin_kasar_naik': None if None in (mk, mk4) else mk > mk4,
             'margin_kasar>median_industri': None if None in (mk, med_mk) else mk > med_mk,
             'ocf>untung_bersih': u['ocf>untung_bersih']}
        ganti = {x for x in ganti if not x.startswith('U:')} | \
            ({'U:margin_kasar>median_industri'} if gk_ and u['margin_kasar>median_industri'] is not None else set()) | \
            ({'U:ocf>untung_bersih', 'U:larian>=1thn_atau_fcf+'} if m['tunai_ganti'] else set())
    g_u = gred_semakan(u, minimum)

    # --- T: pertumbuhan ---
    eps4 = m4['eps'] if m4 else None
    eps20 = m20['eps'] if m20 else None
    g1, g5 = tumbuh(m['eps'], eps4), tumbuh(m['eps'], eps20)
    g5a = None if g5 is None or 1 + g5 <= 0 else (1 + g5) ** 0.2 - 1
    roic_t = None
    if m20 and b20 and m['nopat'] is not None and m20['nopat'] is not None:
        dic = (modal_dilabur(b) or 0) - (modal_dilabur(b20) or 0)
        if modal_dilabur(b) is not None and modal_dilabur(b20) is not None and dic > 0:
            roic_t = (m['nopat'] - m20['nopat']) / dic
    naik8 = None
    if len(qs) >= 3 * n:
        v = [yoy_suku(qs, -i, hasil, n) for i in range(1, 2 * n + 1)]
        naik8 = None if any(x is None for x in v) else sum(x > 0 for x in v) >= 1.5 * n   # 6/8 suku
    eps_q = yoy_suku(qs, -1, eps_teras, n)
    hasil_q = yoy_suku(qs, -1, hasil, n)
    t1 = None if eps20 is None or eps20 <= 0 or m['eps'] is None else m['eps'] > eps20
    if lanjut and t1 is None and m['eps'] is not None and mL is not None and mL['eps'] is not None:
        t1 = m['eps'] > max(mL['eps'], 0.0); ganti.add('T:eps_ttm>eps_5thn_lalu')   # asas <= 0 / tetingkap pendek
    t2 = None if roic_t is None else roic_t > KOS_MODAL
    if lanjut and t2 is None and mL is not None and bLm is not None and m['nopat'] is not None \
            and mL['nopat'] is not None:
        a1, a0 = modal_dilabur(b), modal_dilabur(bLm)
        if a1 is not None and a0 is not None:
            dn, dic = m['nopat'] - mL['nopat'], a1 - a0
            t2 = (dn / dic > KOS_MODAL) if dic > 0 else dn > 0   # modal tidak bertambah: untung mesti naik
            ganti.add('T:roic_tambahan_5thn>kos_modal')
    t3 = None if g1 is None or g5a is None else g1 > g5a
    if lanjut and t3 is None and m['eps'] is not None:
        if m['eps'] <= 0:
            t3 = False
        elif eps4 is not None and eps4 <= 0:
            t3 = True    # pusing untung dalam 12 bulan = pecutan
        elif g1 is not None and mL is not None and mL is not m20 and (mL['eps'] or 0) > 0:
            gL = m['eps'] / mL['eps']
            t3 = g1 > gL ** (1 / Lm) - 1
        if t3 is not None:
            ganti.add('T:eps_1thn>purata_5thn')
    t4 = None if eps_q is None else eps_q >= 0.18
    if lanjut and t4 is None:
        t4 = lulus_tumbuh(*pasangan_yoy(qs, -1, eps_teras, n), 0.18)
        if t4 is not None:
            ganti.add('T:eps_suku_yoy>=18%')
    t5 = None if hasil_q is None else hasil_q >= 0.20
    if lanjut and t5 is None:
        t5 = lulus_tumbuh(*pasangan_yoy(qs, -1, hasil, n), 0.20)
        if t5 is not None:
            ganti.add('T:jualan_suku_yoy>=20%')
    if lanjut and naik8 is None:   # v7.1: asas <= 0 (hasil pertama = naik) atau sejarah < 3 tahun (>= n perbandingan, >= 75%)
        kk = min(2 * n, len(qs) - n)
        if kk >= (2 if pendek else n):
            pp = [pasangan_yoy(qs, -i, hasil, n) for i in range(1, kk + 1)]
            if all(a is not None and c is not None for a, c in pp):
                naik8 = sum((a > 0) if c <= 0 else (a / c - 1 > 0) for a, c in pp) >= 0.75 * kk
                ganti.add('T:jualan_naik_6_daripada_8_suku')
    t = {'eps_ttm>eps_5thn_lalu': t1, 'roic_tambahan_5thn>kos_modal': t2, 'eps_1thn>purata_5thn': t3,
         'eps_suku_yoy>=18%': t4, 'jualan_suku_yoy>=20%': t5, 'jualan_naik_6_daripada_8_suku': naik8}
    ut.update(eps_suku_yoy=eps_q, jualan_suku_yoy=hasil_q, roic_tambahan=roic_t)
    if (mL is not None and mL is not m20) or (bL is not None and bL is not b20):
        ut['tetingkap_tahun'] = min(x for x in (Lm if mL is not None and mL is not m20 else 5,
                                                Lb if bL is not None and bL is not b20 else 5))
    g_t = gred_semakan(t, minimum)

    # --- S: arah suku terkini (YoY) ---
    s = {}
    if len(qs) >= n + 1:
        e, e4 = qs[-1], qs[-(n + 1)]
        mk = lambda x: bahagi(nilai(x, P, 'Gross Profit'), hasil(x))
        mo = lambda x: bahagi(nilai(x, P, 'Operating Profit'), hasil(x))
        cr = lambda x: bahagi(nilai(x, K, 'Total Current Assets'), nilai(x, K, 'Total Current Liabilities'))
        da = lambda x: bahagi(hutang(x), nilai(x, K, 'Total Assets'))
        s = {'margin_kasar_naik': None if None in (mk(e), mk(e4)) else mk(e) > mk(e4),
             'margin_op_naik': None if None in (mo(e), mo(e4)) else mo(e) > mo(e4),
             'hutang/aset_tidak_naik': None if None in (da(e), da(e4)) else da(e) <= da(e4) + 1e-12,
             'nisbah_semasa_naik': None if None in (cr(e), cr(e4)) else cr(e) > cr(e4),
             'tiada_terbitan_saham_bersih': None if m['terbitan'] is None else m['terbitan'] <= 0,
             'code33_3_suku_memecut': code33(qs, n)}
    g_s = gred_semakan(s, minimum)

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
    if None not in (m['ni_tunai'], m['ocf'], aa) and aa > 0 and (m['ni_tunai'] - m['ocf']) / aa > 0.10:
        f.append('akruan_tinggi')
    # aliran tunai ganti (tempoh berbeza): Beneish dan OCF/EBITDA tidak dinilai (seperti v7, nilai tiada)
    bm = beneish(m, m4, b, b4) if not (m['tunai_ganti'] or (m4 or {}).get('tunai_ganti')) else None
    ut['beneish_m'] = bm
    if bm is not None and bm > -1.78:
        f.append('beneish')
    if not m['tunai_ganti'] and (m['ebitda'] or 0) > 0 and m['ocf'] is not None and m['ocf'] / m['ebitda'] < 0.5:
        f.append('ocf<50%_ebitda')
    if hasil_g is not None and hasil_g > 0.20 and roic is not None and roic < KOS_MODAL:
        f.append('tumbuh_bakar_nilai')
    ganti = {x for x in ganti if r_semak_ada(x, {'K': sws, 'U': u, 'T': t, 'S': s})}
    return {'K': k, 'U': g_u, 'T': g_t, 'S': g_s, 'semak': {'K': sws, 'U': u, 'T': t, 'S': s}, 'F': f,
            'peringkat': peringkat, 'nota': nota, 'butiran': ut, 'm': m, 'b': b,
            'k_asas': {'hutang_ebitda': g_de, 'ffo_hutang': g_ffo}, 'ganti': sorted(ganti)}


def r_semak_ada(kod, semak):
    """Kod ganti 'X:nama' sah hanya jika semakan itu wujud dan bernilai (bukan None)."""
    x, _, nama = kod.partition(':')
    return semak.get(x, {}).get(nama) is not None


def code33(qs, n=4):
    """Minervini: EPS YoY, jualan YoY dan margin bersih memecut 3 suku berturut."""
    if len(qs) < n + 3:
        return None
    eps = [yoy_suku(qs, -i, eps_teras, n) for i in (3, 2, 1)]
    jual = [yoy_suku(qs, -i, hasil, n) for i in (3, 2, 1)]
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


# ---------- v7.1: model bank / insurans / REIT (spec §13) ----------
def jalur(v, had, naik=True):
    """Huruf daripada ambang: naik=True -> v >= had[0] A, >= had[1] B, ...; naik=False -> v <= had[0] A, ..."""
    if v is None:
        return TIADA
    for g, h in zip('ABCD', had):
        if (v >= h if naik else v <= h):
            return g
    return 'E'


def ttm_f(qs, f, n):
    return jumlah(qs[-n:], f) if len(qs) >= n else None


def da_e(e):
    return nilai(e, T, 'Depreciation & Depletion & Amortization') if nilai(e, T, 'Depreciation & Depletion & Amortization') \
        is not None else nilai(e, P, 'Depreciation & Amortization & Depletion')


def ffo_e(e):
    """FFO anggaran (Nareit 2018): untung bersih induk + susut nilai/pelunasan − untung jualan harta/sekuriti −
    item khas (caj rosot nilai ditambah balik). None jika untung atau D&A tiada."""
    ni, da = untung_induk(e), da_e(e)
    if ni is None or da is None:
        return None
    return ni + da - (nilai(e, P, 'Gain on Sale of Security') or 0.0) - (nilai(e, P, 'Special Income (Charges)') or 0.0)


def roe_mampan(tah, ambang=0.10):
    """ROE tahunan >= ambang dalam >= separuh daripada <= 5 tahun terakhir (minimum 3 tahun)."""
    r = []
    for i in range(max(1, len(tah) - 5), len(tah)):
        ni, eq, eq0 = untung_induk(tah[i]), ekuiti_induk(tah[i]), ekuiti_induk(tah[i - 1])
        ea = purata(eq, eq0)
        if ni is not None and ea and ea > 0:
            r.append(ni / ea)
    return None if len(r) < 3 else sum(x >= ambang for x in r) >= math.ceil(len(r) / 2)


def t_kewangan(qs, n, f_utama, nama, ambang_q, ambang_h, ekuiti=True):
    """Semakan T model kewangan: nilai utama (EPS / FFO) TTM lawan L tahun lalu (L = 5, atau terpanjang >= 2),
    pertumbuhan 1 tahun > purata L tahun, tempoh terkini YoY >= ambang_q, hasil tempoh terkini YoY >= ambang_h,
    hasil naik YoY dalam >= 75% daripada <= 2n tempoh, nilai buku (ekuiti induk) tumbuh YoY."""
    u = ttm_f(qs, f_utama, n)
    u4 = ttm_f(qs[:-n], f_utama, n) if len(qs) >= 2 * n else None
    L = min(5, len(qs) // n - 1)
    uL = ttm_f(qs[:-L * n], f_utama, n) if L >= 2 else None
    t1 = None if u is None or uL is None else u > max(uL, 0.0)
    t3 = None
    if u is not None and u4 is not None:
        if u <= 0:
            t3 = False
        elif u4 <= 0:
            t3 = True
        elif uL is not None and uL > 0:
            t3 = u / u4 - 1 > (u / uL) ** (1 / L) - 1
    kk = min(2 * n, len(qs) - n)
    naik = None
    if kk >= n:
        pp = [pasangan_yoy(qs, -i, hasil, n) for i in range(1, kk + 1)]
        if all(a is not None and c is not None for a, c in pp):
            naik = sum((a > 0) if c <= 0 else a > c for a, c in pp) >= 0.75 * kk
    t = {f'{nama}_ttm>{nama}_5thn_lalu': t1, f'{nama}_1thn>purata_5thn': t3,
         f'{nama}_tempoh_yoy>={round(ambang_q * 100)}%': lulus_tumbuh(*pasangan_yoy(qs, -1, f_utama, n), ambang_q),
         f'hasil_tempoh_yoy>={round(ambang_h * 100)}%': lulus_tumbuh(*pasangan_yoy(qs, -1, hasil, n), ambang_h),
         'hasil_naik_75%_tempoh': naik}
    if ekuiti:
        a, c = pasangan_yoy(qs, -1, ekuiti_induk, n)
        t['nilai_buku_tumbuh_yoy'] = None if a is None or c is None else a > c
    return t, (L if L < 5 else None)


def sub_gred_kewangan(model, qs, semua, tah, n=4):
    """Model bank / insurans / REIT (sub-gred K/U/T/S setara; spec §13). Ambang daripada rujukan piawai (Basel III,
    FDIC PCA, Moody's/S&P, Nareit, perjanjian bon REIT) — senarai sumber dan andaian dalam spec."""
    e = qs[-1]
    e4 = qs[-(n + 1)] if len(qs) >= n + 1 else None
    b = imbangan(e)
    b4 = imbangan(e4) if e4 else None
    nota, ut, f = [], {}, []
    ni = ttm_f(qs, untung_induk, n)
    ni4 = ttm_f(qs[:-n], untung_induk, n) if len(qs) >= 2 * n else None
    rev = ttm_f(qs, hasil, n)
    aset_avg = purata(b['aset'], b4['aset'] if b4 else None)
    eq_avg = purata(b['ekuiti'], b4['ekuiti'] if b4 else None)
    roa = bahagi(ni, aset_avg)
    roe = None if ni is None or not eq_avg or eq_avg <= 0 else ni / eq_avg
    terbitan = ttm_f(qs, lambda x: nilai(x, T, 'Net Common Stock Issuance') or 0.0, n)
    tiada_terbitan = None if terbitan is None else terbitan <= 0
    ttm_p = lambda nama, qq=qs: ttm_f(qq, lambda x: nilai(x, P, nama), n)
    m = {'hasil': rev, 'pend_faedah': 0.0}
    k_asas = {}
    if model == 'bank':
        gw = lambda x: nilai(x, K, 'Goodwill and Other Intangible Assets') or 0.0
        pref = lambda x: nilai(x, K, '-Preferred Stock') or 0.0

        def tce(x):
            a, q_ = nilai(x, K, 'Total Assets'), ekuiti_induk(x)
            return None if a is None or q_ is None or a - gw(x) <= 0 else (q_ - pref(x) - gw(x)) / (a - gw(x))
        ldr = lambda x: bahagi(nilai(x, K, 'Net Loan'), nilai(x, K, 'Total Deposits'))

        def kec(qq):   # nisbah kecekapan: belanja bukan faedah / (pendapatan faedah bersih + bukan faedah)
            nie, nii, non = (jumlah(qq, lambda x: nilai(x, P, nm)) for nm in
                             ('Non-Interest Expense', 'Net Interest Income', 'Non-Interest Income'))
            return bahagi(nie, (nii or 0.0) + (non or 0.0)) if nie is not None and nii is not None else None

        def kos(qq, xa, xb):   # kos kredit: peruntukan (Moomoo: negatif = belanja) / purata pinjaman
            pv = jumlah(qq, lambda x: nilai(x, P, 'Credit Losses Provision'))
            pj = purata(nilai(xa, K, 'Net Loan'), nilai(xb, K, 'Net Loan') if xb else None)
            return None if pv is None or not pj else -pv / pj
        k_asas = {'tce_aset': jalur(tce(e), (0.09, 0.07, 0.05, 0.04)),
                  'pinjaman_deposit': jalur(ldr(e), (0.80, 0.90, 1.00, 1.10), naik=False)}
        kecq, kos_t = kec(qs[-n:]), kos(qs[-n:], e, e4)
        ut.update(tce_aset=tce(e), pinjaman_deposit=ldr(e), kecekapan=kecq, kos_kredit=kos_t)
        u = {'roa>=1%': None if roa is None else roa >= 0.01, 'roe>=10%': None if roe is None else roe >= 0.10,
             'kecekapan<=60%': None if kecq is None else kecq <= 0.60,
             'kos_kredit<=1%': None if kos_t is None else kos_t <= 0.01, 'roe_mampan': roe_mampan(tah)}
        s = {}
        if e4:
            ra = lambda x: bahagi(untung_induk(x), nilai(x, K, 'Total Assets'))
            k1, k0 = kec([e]), kec([e4])
            c1 = kos([e], e, None)
            c0 = kos([e4], e4, None)
            s = {'roa_naik': None if None in (ra(e), ra(e4)) else ra(e) > ra(e4),
                 'kecekapan_bertambah_baik': None if None in (k1, k0) else k1 < k0,
                 'tce_tidak_turun': None if None in (tce(e), tce(e4)) else tce(e) >= tce(e4) - 1e-12,
                 'kos_kredit_tidak_naik': None if None in (c1, c0) else c1 <= c0 + 1e-12,
                 'deposit_tumbuh': None if None in (nilai(e, K, 'Total Deposits'), nilai(e4, K, 'Total Deposits'))
                 else nilai(e, K, 'Total Deposits') > nilai(e4, K, 'Total Deposits'),
                 'tiada_terbitan_saham_bersih': tiada_terbitan}
        t, L = t_kewangan(qs, n, eps_teras, 'eps', 0.10, 0.10)
        m['pend_faedah'] = ttm_p('-Interest Income') or 0.0
        tunai = nilai(e, K, 'Cash, Cash Equivalents & Federal Funds Sold', 'Cash and Cash Equivalents & Short-Term Investments')
        b['tunai'] = tunai or 0.0
    elif model == 'insurans':
        hut = b['hutang']
        lev = None if b['ekuiti'] is None or hut + b['ekuiti'] <= 0 else hut / (hut + b['ekuiti'])
        faedah = ttm_p('-Interest Expense Non-Operating') or ttm_p('Non-Operating Interest Expense')
        pretax = ttm_p('Pretax Profit')
        tiada_hutang = b['aset'] is not None and hut <= 0.01 * b['aset']
        ic = None if not faedah or faedah <= 0 or pretax is None else min((pretax + faedah) / faedah, HAD_IC)

        def cr(qq):   # nisbah gabungan (P&C): (kerugian + perolehan polisi + underwriting) / premium diperoleh
            pr, ls = (jumlah(qq, lambda x: nilai(x, P, nm)) for nm in ('Total Premiums Earned', 'Loss Adjustment Expense'))
            if not pr or ls is None:
                return None
            lain = sum(jumlah(qq, lambda x: nilai(x, P, nm)) or 0.0 for nm in ('Policy Acquisition Expense', 'Underwriting Expenses'))
            return (ls + lain) / pr
        k_asas = {'leverage_kewangan': 'A' if tiada_hutang else jalur(lev, (0.15, 0.25, 0.35, 0.45), naik=False),
                  'liputan_faedah': 'A' if tiada_hutang else jalur(ic, (12.0, 8.0, 4.0, 2.0))}
        crq = cr(qs[-n:])
        ocf = ttm_f(qs, lambda x: nilai(x, T, 'Operating Cash Flow'), n)
        mp = lambda qq: bahagi(jumlah(qq, lambda x: nilai(x, P, 'Pretax Profit')), jumlah(qq, hasil))
        ut.update(leverage_kewangan=lev, liputan_faedah=ic, nisbah_gabungan=crq, margin_pretax=mp(qs[-n:]))
        u = {'roe>=10%': None if roe is None else roe >= 0.10, 'roa>=1%': None if roa is None else roa >= 0.01,
             'nisbah_gabungan<100%': None if crq is None else crq < 1.0,
             'margin_pretax>=10%': None if mp(qs[-n:]) is None else mp(qs[-n:]) >= 0.10,
             'roe_mampan': roe_mampan(tah), 'ocf>untung_bersih': None if ocf is None or ni is None else ocf > ni}
        s = {}
        if e4:
            lv = lambda bb: None if bb['ekuiti'] is None or bb['hutang'] + bb['ekuiti'] <= 0 else bb['hutang'] / (bb['hutang'] + bb['ekuiti'])
            c1, c0 = cr([e]), cr([e4])
            m1, m0 = mp([e]), mp([e4])
            p1, p0 = nilai(e, P, 'Total Premiums Earned'), nilai(e4, P, 'Total Premiums Earned')
            roe4 = None
            if len(qs) >= 2 * n + 1 and ni4 is not None:
                ea4 = purata(ekuiti_induk(qs[-(n + 1)]), ekuiti_induk(qs[-(2 * n + 1)]))
                roe4 = ni4 / ea4 if ea4 and ea4 > 0 else None
            s = {'nisbah_gabungan_turun': None if None in (c1, c0) else c1 < c0,
                 'margin_pretax_naik': None if None in (m1, m0) else m1 > m0,
                 'leverage_tidak_naik': None if None in (lv(b), lv(b4)) else lv(b) <= lv(b4) + 1e-12,
                 'premium_tumbuh': None if None in (p1, p0) else p1 > p0,
                 'roe_naik': None if None in (roe, roe4) else roe > roe4,
                 'tiada_terbitan_saham_bersih': tiada_terbitan}
        t, L = t_kewangan(qs, n, eps_teras, 'eps', 0.10, 0.10)
        m['pend_faedah'] = ttm_p('Net Investment Income') or 0.0
    else:   # REIT
        ffo = ttm_f(qs, ffo_e, n)
        ebit = ttm_p('Operating Profit')
        da = ttm_f(qs, da_e, n)
        ebitda = None if ebit is None or da is None else ebit + da
        faedah = ttm_p('Non-Operating Interest Expense')
        hut, aset = b['hutang'], b['aset']
        ha = bahagi(hut, aset)
        icr = None if not faedah or faedah <= 0 or ebitda is None else min(ebitda / faedah, HAD_IC)
        nde = None if ebitda is None else ((hut - b['tunai']) / ebitda if ebitda > 0 else math.inf)
        k_asas = {'hutang_aset': jalur(ha, (0.35, 0.45, 0.55, 0.60), naik=False),
                  'liputan_faedah': 'A' if hut <= 0.01 * (aset or 0) and aset else jalur(icr, (5.0, 4.0, 3.0, 1.5)),
                  'hutang_bersih_ebitda': jalur(nde, (5.5, 6.5, 7.5, 9.0), naik=False)}
        div = ttm_f(qs, lambda x: nilai(x, T, 'Cash Dividends Paid'), n)
        div = None if div is None else abs(div)
        ocf = ttm_f(qs, lambda x: nilai(x, T, 'Operating Cash Flow'), n)
        ut.update(ffo=ffo, hutang_aset=ha, liputan_faedah=icr, hutang_bersih_ebitda=None if nde == math.inf else nde)
        u = {'margin_ffo>=30%': None if ffo is None or not rev else ffo / rev >= 0.30,
             'ffo/ekuiti>=8%': None if ffo is None or not eq_avg or eq_avg <= 0 else ffo / eq_avg >= 0.08,
             'dividen<=90%_ffo': None if ffo is None or div is None else (ffo > 0 and div <= 0.90 * ffo),
             'ocf>=dividen': None if ocf is None or div is None else ocf >= div,
             'margin_ebitda>=50%': None if ebitda is None or not rev else ebitda / rev >= 0.50}
        s = {}
        if e4:
            me = lambda x: None if hasil(x) in (None, 0) or nilai(x, P, 'Operating Profit') is None or da_e(x) is None \
                else (nilai(x, P, 'Operating Profit') + da_e(x)) / hasil(x)
            li = lambda x: None if not nilai(x, P, 'Non-Operating Interest Expense') or nilai(x, P, 'Operating Profit') is None \
                or da_e(x) is None else (nilai(x, P, 'Operating Profit') + da_e(x)) / nilai(x, P, 'Non-Operating Interest Expense')
            cr_ = lambda x: bahagi(nilai(x, K, 'Total Current Assets'), nilai(x, K, 'Total Current Liabilities'))
            da_ = lambda x: bahagi(hutang(x), nilai(x, K, 'Total Assets'))
            f1, f0 = ffo_e(e), ffo_e(e4)
            s = {'hutang/aset_tidak_naik': None if None in (da_(e), da_(e4)) else da_(e) <= da_(e4) + 1e-12,
                 'margin_ebitda_naik': None if None in (me(e), me(e4)) else me(e) > me(e4),
                 'liputan_faedah_naik': None if None in (li(e), li(e4)) else li(e) > li(e4),
                 'ffo_tempoh_naik_yoy': None if None in (f1, f0) else f1 > f0,
                 'tiada_terbitan_saham_bersih': tiada_terbitan,
                 'nisbah_semasa_naik': None if None in (cr_(e), cr_(e4)) else cr_(e) > cr_(e4)}
        t, L = t_kewangan(qs, n, ffo_e, 'ffo', 0.10, 0.10, ekuiti=False)
        m['pend_faedah'] = ttm_p('Non-Operating Interest Income') or 0.0
    gk = [g for g in k_asas.values() if g != TIADA]
    k = max(gk, key=GRED.index) if gk else TIADA
    if L is not None:
        ut['tetingkap_tahun'] = L
    ut.update(roa=roa, roe=roe)
    return {'K': k, 'U': gred_semakan(u), 'T': gred_semakan(t), 'S': gred_semakan(s),
            'semak': {'K': {}, 'U': u, 'T': t, 'S': s}, 'F': f, 'peringkat': {'reit': 'REIT'}.get(model, model),
            'nota': nota, 'butiran': ut, 'm': m, 'b': b, 'k_asas': k_asas, 'ganti': []}


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


def pilih_tempoh(k, hari_ini, lanjut=True):
    """Pilih siri tempoh (point-in-time). v7: suku >= 8 berturut. v7.1 (lanjut; hanya jika v7 tidak dapat mengira):
    suku tanpa penyata pendapatan diabaikan (rantaian putus di situ); calon: separuh tahun (>= 4), suku pendek (4–7;
    keyakinan rendah), separuh pendek (2–3), tahunan (>= 2). Calon hanya sah jika tempoh terakhirnya ialah data terkini
    yang ada (tidak mengabaikan tempoh lebih baharu, cth. tahunan Dis 2025 tidak dipakai jika suku Mac 2026 ada); calon
    pertama yang tidak basi dipilih (tiada: calon sah pertama, kemudian ditolak sebagai basi).
    -> (calon | None, tahunan point-in-time, sebab jika tiada calon)."""
    terbit = k.get('terbit') or {}
    suku = [e for e in k.get('suku') or [] if tersedia(e, terbit, hari_ini)]
    tah = isi_tahunan(tahunan_tersedia(k.get('tahunan') or [], terbit, hari_ini), k.get('suku') or [], lanjut)
    if not lanjut:
        qs = suku_berturut(suku, 4)
        return (dict(jenis='suku', n=4, qs=qs, semua=suku, pendek=False, minimum=8) if len(qs) >= 8 else None), \
            tah, f'{len(qs)} suku berturut (< 8)'
    tanpa_p = [e['label'] for e in suku[-8:] if not e.get(P)]
    suku = [e for e in suku if e.get(P)]
    qs = suku_berturut(suku, 4, True)
    sep = [e for e in tempoh_separuh(k) if tersedia(e, terbit, hari_ini) and e.get(P)] if k.get('separuh') else []
    hs = suku_berturut(sep, 2) if sep else []
    tp = [e for e in tah if e.get(P)]
    ys = suku_berturut(tp, 1) if tp else []
    terkini = max((tarikh(e['tamat']) for e in suku + sep + tp), default=None)
    calon = [dict(jenis='suku', n=4, qs=qs, semua=suku, pendek=False, minimum=8),
             dict(jenis='separuh', n=2, qs=hs, semua=sep, pendek=False, minimum=4),
             dict(jenis='suku', n=4, qs=qs, semua=suku, pendek=True, minimum=4),
             dict(jenis='separuh', n=2, qs=hs, semua=sep, pendek=True, minimum=2),
             dict(jenis='tahunan', n=1, qs=ys, semua=tp, pendek=False, minimum=2)]
    sah = [c for c in calon if len(c['qs']) >= c['minimum']
           and (tarikh(c['qs'][-1]['tamat']) - terkini).days >= -7]
    segar = [c for c in sah if (hari_ini - tarikh(c['qs'][-1]['tamat'])).days <= BASI[c['n']]]
    lama = lambda c: len(c) and terkini and (tarikh(c[-1]['tamat']) - terkini).days < -7
    sebab = f'{len(qs)} suku berturut (< 4)' + \
        (f'; suku tanpa penyata pendapatan: {", ".join(tanpa_p)}' if tanpa_p else '') + \
        (f'; {len(hs)} separuh tahun ' + ('(bukan data terkini)' if lama(hs) and len(hs) >= 2 else '(< 2)')
         if k.get('separuh') else '') + \
        f'; {len(ys)} tahun ' + ('(bukan data terkini)' if lama(ys) and len(ys) >= 2 else '(< 2)')
    return (segar or sah or [None])[0], tah, sebab


def kira(k, harga=None, hari_ini=None, med=None, sektor='', industri=''):
    """k = kandungan data/kewangan/<T>.json. harga = pd.Series harga tutup (indeks tarikh). med = median industri
    (median_industri()[industri]; v7.1: termasuk sandaran 'sektor').
    v7.1: peraturan v7 dahulu (hasil sama seperti v7 apabila v7 memberi gred); hanya jika v7 memberi '–', pengiraan
    diulang dengan sambungan v7.1 (model bank/insurans/REIT, separuh tahun/tahunan, sejarah pendek, ganti semakan)."""
    hari_ini = hari_ini or date.today()
    if kewangan_bank(sektor, industri):
        sebab_v7 = 'bank/insurans/REIT: model lain diperlukan'
    else:
        r = kira_teras(k, harga, hari_ini, med, sektor, industri, 'standard', False)
        if r['gred'] != TIADA:
            return r
        sebab_v7 = r['butiran'].get('sebab') or r['ringkas']
    r = kira_teras(k, harga, hari_ini, med, sektor, industri, jenis_model(k, sektor, industri), True)
    r['butiran']['sebab_v7'] = sebab_v7
    return r


def kira_teras(k, harga, hari_ini, med, sektor, industri, model, lanjut):
    """Satu laluan pengiraan: lanjut=False -> peraturan v7 tepat (model standard, suku >= 8); lanjut=True ->
    sambungan v7.1."""
    if model == 'tidak_dikenali':
        return hasil_kosong('kewangan: penyata bukan format syarikat biasa/bank/insurans (kumpul semula)')
    pil, tah, sebab = pilih_tempoh(k, hari_ini, lanjut)
    if pil is None:
        return hasil_kosong(sebab)
    qs, semua, n, pendek, jenis = pil['qs'], pil['semua'], pil['n'], pil['pendek'], pil['jenis']
    if (hari_ini - tarikh(qs[-1]['tamat'])).days > BASI[n]:
        return hasil_kosong('suku terakhir tamat > 200 hari lalu (data basi)' if n == 4
                            else f'{NAMA_TEMPOH[n]} terakhir tamat > {BASI[n]} hari lalu (data basi)')
    if model == 'standard':
        kira_sub = lambda q, tq: sub_gred(q, semua, tq, med, sektor, industri, n, lanjut, pendek)
    else:
        kira_sub = lambda q, tq: sub_gred_kewangan(model, q, semua, tq, n)
    # urutan 3 tempoh untuk histerisis (point-in-time setiap tempoh)
    urutan = []
    for j in (2, 1, 0):
        q = qs[:len(qs) - j]
        if len(q) >= (n if pendek else 2 * n):
            tq = [e for e in tah if tarikh(e['tamat']) <= tarikh(q[-1]['tamat'])]
            urutan.append(gabung(kira_sub(q, tq)))
    r = kira_sub(qs, tah)
    g_mentah = gabung(r)
    g = histerisis(urutan) if g_mentah != TIADA else TIADA
    # pasaran: distance-to-default naif (had semasa, selepas histerisis; model standard sahaja)
    hp = None
    mw = {e.get('mata_wang') for e in qs[-2 * n:] if e.get('mata_wang')}
    if mw - {'USD'}:   # penyata bukan USD: nisbah berasaskan harga (USD) tidak dikira
        r['nota'].append('mata_wang_' + '/'.join(sorted(mw)))
        harga = None
    if harga is not None:
        import pandas as pd
        hp = harga[harga.index <= pd.Timestamp(hari_ini)].dropna()
    saham = k.get('saham_terbit')
    dd = jarak_mungkir(hp, saham, r['b']) if hp is not None and model == 'standard' else None
    r['butiran']['jarak_mungkir'] = None if dd is None else (999.0 if dd == math.inf else round(dd, 2))
    if dd is not None and dd != math.inf:
        if dd < 0:
            g = had_atas(g, 'E'); r['K'] = had_atas(r['K'], 'E')
        elif dd < 1 or (dd < 2 and 'altman_z2<1.1' in r['nota']):
            g = had_atas(g, 'D'); r['K'] = had_atas(r['K'], 'D')
    sy = syariah(r['b'], r['m'], hp, saham)
    if sy['status'] == 'gagal':
        g = 'E' if g != TIADA else g
    # keyakinan: semakan 'ganti' (sambungan v7.1) tidak dikira dalam liputan
    ganti = set(r.get('ganti') or [])
    semua_semak = [(x, nm, v) for x, d in r['semak'].items() for nm, v in d.items()]
    liputan = sum(v is not None and f'{x}:{nm}' not in ganti for x, nm, v in semua_semak) / max(1, len(semua_semak))
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
    if tidak_sepadan(k, hari_ini):
        r['nota'].append('suku_tidak_sepadan_tahunan'); tahap -= 1
    # v7.1: data separuh tahun / tahunan dan aliran tunai ganti -> turun satu tahap; sejarah pendek -> rendah
    if jenis != 'suku':
        r['nota'].append('data_separuh_tahun' if jenis == 'separuh' else 'data_tahunan'); tahap -= 1
    if (r.get('m') or {}).get('tunai_ganti'):
        tahap -= 1
    if n == 4 and ada_peralihan(qs, 4):
        r['nota'].append('peralihan_tahun_kewangan')
    if pendek:
        r['nota'].append('sejarah_pendek'); tahap = 0
    yakin = ['rendah', 'sederhana', 'tinggi'][max(0, tahap)]
    bil_semak = sum(len(d) for d in r['semak'].values())
    sy_teks = {'lulus': 'lulus', 'hampir_had': 'hampir had', 'gagal_sebahagian': 'gagal sebahagian', 'gagal': 'gagal'}.get(sy['status'])
    tanda = (f' · data {NAMA_TEMPOH[n]}' if jenis != 'suku' else '') + (' · sejarah pendek' if pendek else '')
    ring = (f'{g} (K:{r["K"]} U:{r["U"]} T:{r["T"]} S:{r["S"]}) · {r["peringkat"]} · F:{len(r["F"])} · keyakinan {yakin}'
            + tanda + (f' · Syariah {sy_teks}' if sy_teks else '')
            if g != TIADA else f'– ({len(qs)} {NAMA_TEMPOH[n]}; sub K:{r["K"]} U:{r["U"]} T:{r["T"]} S:{r["S"]})')
    gagal = {x: [n_ for n_, v in r['semak'][x].items() if v is False] for x in 'KUTS'}
    butiran = {'tempoh': qs[-1]['label'], 'tamat': qs[-1]['tamat'], 'gred_mentah': g_mentah, 'urutan': urutan,
               'gagal': gagal, 'bendera': r['F'], 'nota': r['nota'], 'syariah': sy, 'liputan_semakan': round(liputan, 2),
               'k_asas': r['k_asas'], 'nisbah': {a: (None if v is None else round(v, 4) if abs(v) != math.inf else 999.0)
                                                 for a, v in r['butiran'].items()}, 'bil_semakan': bil_semak,
               'versi': VERSI if lanjut else '7'}
    if model != 'standard':
        butiran['model'] = model
    if jenis != 'suku':
        butiran['tempoh_data'] = jenis
    if pendek:
        butiran['sejarah_pendek'] = True
    if ganti:
        butiran['semakan_ganti'] = sorted(ganti)
    if g == TIADA:   # sebab tepat: sub-gred yang tidak dapat dikira
        kurang = []
        for x in 'KUTS':
            if r[x] != TIADA:
                continue
            d = r['semak'][x]
            if x == 'K':
                kurang.append('K (nisbah hutang/EBITDA dan FFO/hutang tidak dapat dikira: EBITDA, D&A atau aliran tunai '
                              'operasi tiada dalam penyata)' if model == 'standard' else
                              'K (nisbah modal/kecairan tidak dapat dikira: medan penyata tiada)')
            else:
                kurang.append(f'{x} ({sum(v is not None for v in d.values())}/{len(d)} semakan boleh dikira)')
        butiran['sebab'] = 'sub-gred tidak cukup: ' + '; '.join(kurang)
    return {'gred': g, 'K': r['K'], 'U': r['U'], 'T': r['T'], 'S': r['S'], 'peringkat': r['peringkat'],
            'bendera': r['F'], 'keyakinan': yakin, 'syariah': sy['status'], 'ringkas': ring,
            'tempoh': qs[-1]['label'], 'butiran': butiran, 'model': model, 'tempoh_data': jenis}


def tidak_sepadan(k, hari_ini, tahun=5, had=0.02):
    """Jumlah 4 suku != angka tahunan (> 2%) dalam 5 tahun kewangan terakhir: penyataan semula
    (operasi dihentikan) atau penukaran mata wang; perbandingan YoY mungkin bercampur asas."""
    suku = k.get('suku') or []
    for a in [x for x in k.get('tahunan') or [] if tarikh(x['tamat']) <= hari_ini][-tahun:]:
        fy = a['label'][:4]
        qs = [e for e in suku if e['label'][:4] == fy and e['label'][5:] in ('Q1', 'Q2', 'Q3', 'Q4')]
        if len(qs) != 4:
            continue
        for f in ('Total Operating Revenue', 'Net Profit'):
            v = (a.get(P) or {}).get(f)
            s = [e[P].get(f) for e in qs]
            if v and None not in s and abs(sum(s) - v) > had * abs(v) + 1.0:
                return True
    return False


def hasil_kosong(sebab):
    return {'gred': TIADA, 'K': TIADA, 'U': TIADA, 'T': TIADA, 'S': TIADA, 'peringkat': '', 'bendera': [],
            'keyakinan': '', 'syariah': TIADA, 'ringkas': f'– ({sebab})', 'tempoh': '', 'butiran': {'sebab': sebab}}


def median_industri(folder, industri_saham, hari_ini):
    """Median margin operasi TTM, margin kasar TTM dan kemeruapan EPS bagi setiap industri (>= PEER_MIN rakan);
    v7.1: 'sektor' = median sektor yang sama (sandaran semakan apabila industri < PEER_MIN rakan)."""
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
    med = lambda v: sorted(v)[len(v) // 2] if len(v) >= PEER_MIN else None
    # v7.1: median sektor (pemetaan industri -> sektor sektor_pasaran.SEKTOR_INDUSTRI) sebagai sandaran semakan
    try:
        from sektor_pasaran import SEKTOR_INDUSTRI
    except ImportError:
        SEKTOR_INDUSTRI = {}
    sek = {}
    for ind, d in kumpul.items():
        x = sek.setdefault(SEKTOR_INDUSTRI.get(ind), {'margin_op': [], 'margin_kasar': [], 'vol_eps': []})
        for nm, v in d.items():
            x[nm] += v
    semua = {nm: med([x for d in kumpul.values() for x in d[nm]]) for nm in ('margin_op', 'margin_kasar', 'vol_eps')}
    out = {}
    kosong = {'margin_op': [], 'margin_kasar': [], 'vol_eps': []}
    for ind in set(kumpul) | {x for x in industri_saham.values() if x}:   # industri tanpa rakan: sandaran sahaja
        d = kumpul.get(ind, kosong)
        out[ind] = {nm: med(v) for nm, v in d.items()}
        sk = SEKTOR_INDUSTRI.get(ind)
        out[ind]['sektor'] = {nm: med(v) for nm, v in sek[sk].items()} if sk in sek else {}
        out[ind]['semua'] = semua
    return out


LAJUR_KEW = ['gred_kewangan', 'kewangan_ringkas', 'kewangan_tempoh', 'kewangan_butiran']


def isi(folder, kew, harga):
    """Isi lajur kewangan SAHAJA bagi baris bergred dalam fail posisi claude*, senarai_beli dan watchlist, pada tarikh asal
    (peraturan sama dengan gred_kira_semula.py): sesi rujukan D = tarikh_isyarat / tarikh_data / sesi sebelum
    tarikh_beli; hari imbasan = tarikh gred_pada asal (selainnya sesi selepas D). Harga <= D; penyata yang diterbitkan
    <= hari imbasan. Lajur lain tidak disentuh; fail posisi tidak menerima kewangan_butiran."""
    import pandas as pd
    import gred as G
    from gred_isi_semula import fail_posisi
    from sektor_pasaran import SEKTOR_INDUSTRI
    c, _ = G.muat_harga(harga)
    sesi = list(c.index)
    peta = os.path.join(folder, 'peta_industri.csv')
    pind = {r['ticker']: r['industri'] for r in csv.DictReader(open(peta, newline='', encoding='utf-8'))} \
        if os.path.exists(peta) else {}
    data, med, kira_n = {}, {}, {}

    def muat(t):
        if t not in data:
            p = os.path.join(kew, f'{t}.json')
            data[t] = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None
        return data[t]

    # moomoo.csv (akaun Moomoo lama) dikecualikan: dokumen db papertrade/moomoo akan melepasi had 256 KiB (20 Okt 2026)
    for p in [x for x in fail_posisi(folder) if os.path.basename(x) != 'moomoo.csv'] + \
            [os.path.join(folder, f) for f in ('senarai_beli.csv', 'watchlist.csv')]:
        if not os.path.exists(p):
            continue
        posisi = os.path.basename(p) not in ('senarai_beli.csv', 'watchlist.csv')
        with open(p, newline='', encoding='utf-8') as f:
            rd = csv.DictReader(f); lajur = list(rd.fieldnames or []); rows = list(rd)
        if 'gred_keseluruhan' not in lajur:
            continue
        ubah = 0
        for r in rows:
            if not r.get('gred_pada'):
                continue
            ti = r.get('tarikh_isyarat') or r.get('tarikh_data') or ''
            if not ti and r.get('tarikh_beli'):
                sb = [x for x in sesi if x < pd.Timestamp(r['tarikh_beli'])]
                ti = str(sb[-1].date()) if sb else ''
            D = max([x for x in sesi if x <= pd.Timestamp(ti)], default=None) if ti else None
            if D is None:
                kira_n['tiada tarikh/harga rujukan'] = kira_n.get('tiada tarikh/harga rujukan', 0) + 1
                continue
            gp = G._tarikh((r.get('gred_pada') or '')[:10])
            sl = [x for x in sesi if x > D]
            hi = gp if gp and gp >= D.date() else sl[0].date() if sl else (D + pd.offsets.BDay(1)).date()
            t = G.ambil(r, 'saham', 'Saham')
            k = muat(t)
            if k is None:
                rk = hasil_kosong('tiada data kewangan')
            else:
                iu = r.get('industri_us') or pind.get(t) or G.ambil(r, 'industri', 'Industri') or ''
                su = r.get('sektor_us') or SEKTOR_INDUSTRI.get(iu) or G.ambil(r, 'sektor', 'Sektor') or ''
                if hi not in med:
                    med[hi] = median_industri(kew, pind, hi)
                h = c[t][c.index <= D].dropna() if t in c.columns else None
                try:
                    rk = kira(k, h, hi, med[hi].get(iu), su, iu)
                except Exception as ex:   # data rosak tidak boleh menghentikan pengisian fail lain
                    rk = hasil_kosong(f'ralat {type(ex).__name__}: {ex}'[:120])
            r['gred_kewangan'] = rk['gred']; r['kewangan_ringkas'] = rk['ringkas']; r['kewangan_tempoh'] = rk['tempoh']
            if not posisi:
                r['kewangan_butiran'] = json.dumps(rk['butiran'], ensure_ascii=False, separators=(',', ':'))
            nama = os.path.basename(p) if not posisi else 'posisi'
            kira_n[f'{nama} {rk["gred"]}'] = kira_n.get(f'{nama} {rk["gred"]}', 0) + 1
            ubah += 1
        if ubah:
            lajur += [x for x in (LAJUR_KEW[:3] if posisi else LAJUR_KEW) if x not in lajur]
            with open(p, 'w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=lajur); w.writeheader()
                for r in rows:
                    w.writerow({x: r.get(x, '') for x in lajur})
    print(json.dumps(dict(sorted(kira_n.items())), ensure_ascii=False))
    return kira_n


def main(argv=None):
    ap = argparse.ArgumentParser(description='Gred kewangan v7')
    sp = ap.add_subparsers(dest='cmd', required=True)
    s = sp.add_parser('simpan', help='fail mentah alat Moomoo -> data/kewangan/<T>.json')
    s.add_argument('--folder', required=True); s.add_argument('--keluar', required=True)
    s.add_argument('--tarikh', default=date.today().isoformat())
    i = sp.add_parser('isi', help='isi lajur kewangan sahaja dalam fail posisi, senarai_beli dan watchlist (tarikh asal)')
    i.add_argument('--folder', required=True, help='folder papertrade'); i.add_argument('--kewangan', required=True)
    i.add_argument('--harga', required=True, help='folder stor harga (harga_A/B.csv)')
    k = sp.add_parser('kira', help='cetak gred kewangan bagi ticker')
    k.add_argument('--kewangan', required=True); k.add_argument('--harga')
    k.add_argument('--tarikh', default=date.today().isoformat()); k.add_argument('ticker', nargs='+')
    a = ap.parse_args(argv)
    if a.cmd == 'simpan':
        simpan(a.folder, a.keluar, a.tarikh)
        return
    if a.cmd == 'isi':
        isi(a.folder, a.kewangan, a.harga)
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
