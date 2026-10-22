# tawaran_edgar.py — lapisan EDGAR bagi sasaran ambil alih bukan tunai (22 Okt 2026; kajian/reports/Pengesanan data tercemar
# yang tinggal.md). Penapis harga terkunci (kod/ambil_alih.py) hanya menangkap tawaran tunai berpremium besar; urus niaga
# pertukaran saham / campuran, tender (sejak 16 Apr 2026 boleh tamat dalam 10 hari perniagaan) dan penswastaan meninggalkan
# jejak pemfailan SEC yang boleh diramal. Skrip ini (GitHub Actions `edgar.yml`, tanpa LLM; sesi Claude tidak boleh capai
# sec.gov) membaca indeks harian EDGAR dan menambah sasaran dalam universe ke `data/ambil_alih.csv` (satu pintu tidak_layak.py).
#
# Peraturan (subject company dalam pengepala pemfailan = sasaran):
#   SC TO-T, SC 14D9, SC 13E3         -> aktif (tender pihak ketiga / lembaga sasaran / penswastaan)
#   425 dengan SATU subject company   -> aktif (komunikasi urus niaga saham/campuran; subject = syarikat yang sekuritinya dicari)
#   425 berbilang subject, PREM14A/DEFM14A -> calon sahaja (data/edgar/calon.csv; peranan sasaran/pembeli tidak pasti)
#   25-NSE (subject dalam senarai aktif) -> tarikh_tamat = tarikh pemfailan (penyahsenaraian; urus niaga selesai)
# SC TO-I (belian balik sendiri) diabaikan. Baris EDGAR: bayaran 'edgar', sumber '<borang> <nombor akses>'.
#
#   python3 standard/tawaran_edgar.py jalan [--mula YYYY-MM-DD] [--hingga YYYY-MM-DD] [--maks-hari 10]
# Persekitaran: SEC_USER_AGENT (wajib oleh SEC: nama + e-mel hubungan; simpan sebagai rahsia repo). Had 10 permintaan/saat.
import argparse, json, os, re, sys, time
from datetime import date, datetime, timedelta, timezone

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
EDGAR = os.path.join(BS2, 'data', 'edgar')
AMBIL = os.path.join(BS2, 'data', 'ambil_alih.csv')
UNIV = os.path.join(BS2, 'data', 'harga', 'univ.txt')
TICKERS = 'https://www.sec.gov/files/company_tickers.json'
INDEKS = 'https://www.sec.gov/Archives/edgar/daily-index/{y}/QTR{q}/form.{d}.idx'
PENGEPALA = 'https://www.sec.gov/Archives/edgar/data/{cik}/{acc_}/{acc}-index-headers.html'
AKTIF = {'SC TO-T', 'SC 14D9', 'SC 13E3', '425'}
CALON = {'PREM14A', 'DEFM14A', 'PREMM14A', 'DEFM14C', 'PREM14C'}
TAMAT = {'25-NSE'}
LAJUR_AMBIL = ['saham', 'tarikh_umum', 'tarikh_tamat', 'pembeli', 'harga_tawaran', 'bayaran', 'sumber']
JEDA = 0.15   # <= ~7 permintaan/saat (had SEC 10)


def ua():
    return os.environ.get('SEC_USER_AGENT') or 'papertrade-claude research github.com/pedagangsenja/papertrade-claude'


def ambil(url, cuba=3):
    import requests
    for n in range(cuba):
        r = requests.get(url, headers={'User-Agent': ua(), 'Accept-Encoding': 'gzip, deflate'}, timeout=30)
        time.sleep(JEDA)
        if r.status_code == 404:
            return None
        if r.status_code == 200:
            return r.text
        time.sleep(2 * (n + 1))
    raise RuntimeError(f'{url}: HTTP {r.status_code}')


# ---------------------------------------------------------------- penghurai (diuji tanpa rangkaian)
BARIS = re.compile(r'^(?P<borang>\S.*?)\s{2,}(?P<nama>\S.*?)\s{2,}(?P<cik>\d{1,10})\s{2,}(?P<tarikh>\d{8}|\d{4}-\d\d-\d\d)\s{2,}'
                   r'(?P<fail>edgar/data/\S+)\s*$')


def hurai_indeks(teks):
    """form.YYYYMMDD.idx -> DataFrame borang, nama, cik (int), tarikh (YYYY-MM-DD), fail, akses."""
    rows = []
    for b in teks.splitlines():
        m = BARIS.match(b)
        if not m:
            continue
        t = m['tarikh'].replace('-', '')
        akses = os.path.basename(m['fail']).replace('.txt', '')
        rows.append(dict(borang=m['borang'].strip(), nama=m['nama'].strip(), cik=int(m['cik']),
                         tarikh=f'{t[:4]}-{t[4:6]}-{t[6:]}', fail=m['fail'], akses=akses))
    return pd.DataFrame(rows, columns=['borang', 'nama', 'cik', 'tarikh', 'fail', 'akses'])


def hurai_pengepala(teks):
    """Pengepala SGML pemfailan -> dict(borang, filer=[cik], subject=[cik])."""
    t = re.sub(r'<[^>]+>', '\n', teks or '')
    borang = re.search(r'CONFORMED SUBMISSION TYPE:\s*(\S[^\n]*)', t)
    out = dict(borang=borang.group(1).strip() if borang else '', filer=[], subject=[])
    for blok in re.split(r'\n\s*(?=(?:FILER|SUBJECT COMPANY|FILED BY|REPORTING-OWNER|ISSUER):)', t):
        k = re.match(r'\s*(FILER|SUBJECT COMPANY|FILED BY|REPORTING-OWNER|ISSUER):', blok)
        if not k:
            continue
        c = re.search(r'CENTRAL INDEX KEY:\s*0*(\d+)', blok)
        if not c:
            continue
        if k.group(1) == 'SUBJECT COMPANY':
            out['subject'].append(int(c.group(1)))
        elif k.group(1) in ('FILER', 'FILED BY'):
            out['filer'].append(int(c.group(1)))
    return out


def peta_ticker(js):
    """company_tickers.json -> {cik: [ticker,...]} (ticker gaya repo: BRK-B -> BRK.B)."""
    out = {}
    for v in (js.values() if isinstance(js, dict) else js):
        out.setdefault(int(v['cik_str']), []).append(str(v['ticker']).upper().replace('-', '.'))
    return out


def putuskan(borang, kepala):
    """(status, cik sasaran) bagi satu pemfailan: 'aktif' | 'calon' | 'tamat' | None."""
    b = borang.upper().replace('/A', '').strip()
    sub = sorted(set(kepala['subject']))
    if b in TAMAT:
        return ('tamat', sub[0]) if sub else (None, None)
    if b == '425':
        if len(sub) == 1:
            return 'aktif', sub[0]
        return ('calon', sub[0]) if sub else (None, None)
    if b in AKTIF:
        if sub:
            return 'aktif', sub[0]
        return ('aktif', kepala['filer'][0]) if b == 'SC 14D9' and kepala['filer'] else (None, None)
    if b in CALON:
        return ('calon', kepala['filer'][0]) if kepala['filer'] else (None, None)
    return None, None


def kemas_ambil(rekod, path=AMBIL):
    """rekod = [dict(status, saham, tarikh, borang, akses, pembeli)] -> tambah baris aktif baharu / tetapkan tarikh_tamat.
    Pulang (ditambah, ditamatkan)."""
    d = pd.read_csv(path, dtype=str, keep_default_na=False) if os.path.exists(path) else pd.DataFrame(columns=LAJUR_AMBIL)
    d = d.reindex(columns=LAJUR_AMBIL).fillna('')
    tambah, tamat = [], []
    for r in sorted(rekod, key=lambda x: x['tarikh']):
        aktif = (d.saham == r['saham']) & (d.tarikh_tamat == '') & (d.bayaran.str.lower() != 'bukan')
        if r['status'] == 'aktif' and not aktif.any():
            d = pd.concat([d, pd.DataFrame([dict(saham=r['saham'], tarikh_umum=r['tarikh'], tarikh_tamat='', pembeli=r.get('pembeli', ''),
                                                 harga_tawaran='', bayaran='edgar', sumber=f"EDGAR {r['borang']} {r['akses']}")])],
                          ignore_index=True)
            tambah.append(r['saham'])
        elif r['status'] == 'tamat' and aktif.any():
            d.loc[aktif & (d.tarikh_umum <= r['tarikh']), 'tarikh_tamat'] = r['tarikh']
            tamat.append(r['saham'])
    if tambah or tamat:
        d.to_csv(path, index=False)
    return tambah, tamat


# ---------------------------------------------------------------- larian
def universe():
    u = {x.strip().replace('US.', '') for x in open(UNIV) if x.strip()} if os.path.exists(UNIV) else set()
    import glob
    for f in glob.glob(os.path.join(BS2, 'papertrade', 'claude*.csv')):
        u |= set(pd.read_csv(f, usecols=['saham'], dtype=str).saham.dropna())
    return u


def muat_peta():
    os.makedirs(EDGAR, exist_ok=True)
    p = os.path.join(EDGAR, 'company_tickers.json')
    if not os.path.exists(p) or time.time() - os.path.getmtime(p) > 7 * 86400:
        teks = ambil(TICKERS)
        if teks:
            open(p, 'w').write(teks)
    return peta_ticker(json.load(open(p)))


def hari_kerja(mula, hingga):
    d = mula
    while d <= hingga:
        if d.weekday() < 5:
            yield d
        d += timedelta(days=1)


def jalan(a):
    os.makedirs(EDGAR, exist_ok=True)
    stp = os.path.join(EDGAR, 'status.json')
    st = json.load(open(stp)) if os.path.exists(stp) else {}
    hingga = date.fromisoformat(a.hingga) if a.hingga else datetime.now(timezone.utc).date()
    mula = date.fromisoformat(a.mula) if a.mula else (date.fromisoformat(st['hari_terakhir']) + timedelta(days=1)
                                                       if st.get('hari_terakhir') else hingga - timedelta(days=3))
    peta = muat_peta()
    tik = {c: [t for t in ts] for c, ts in peta.items()}
    univ = universe()
    rekod, calon, proses, gagal = [], [], [], []
    for d in list(hari_kerja(mula, hingga))[:a.maks_hari]:
        url = INDEKS.format(y=d.year, q=(d.month - 1) // 3 + 1, d=d.strftime('%Y%m%d'))
        try:
            teks = ambil(url)
        except Exception as e:
            gagal.append(f'{d}: {e}'); break
        proses.append(str(d))
        if teks is None:            # cuti / indeks belum terbit
            continue
        ix = hurai_indeks(teks)
        b = ix.borang.str.upper().str.replace('/A', '', regex=False).str.strip()
        dlm_univ = ix.cik.map(lambda c: any(t in univ for t in tik.get(c, ())))
        # tender/425/13E3/25-NSE: semua pengepala diambil (indeks mungkin hanya menyenaraikan pemfail; sasaran = subject
        # company dalam pengepala); proksi merger: hanya pemfail dalam universe
        ix = ix[b.isin(AKTIF | TAMAT) | (b.isin(CALON) & dlm_univ)]
        for akses, g in ix.groupby('akses'):
            r0 = g.iloc[0]
            acc_ = akses.replace('-', '')
            try:
                kepala = hurai_pengepala(ambil(PENGEPALA.format(cik=r0.cik, acc_=acc_, acc=akses)))
            except Exception as e:
                gagal.append(f'{akses}: {e}'); continue
            status, cik = putuskan(r0.borang, kepala)
            if not status:
                continue
            saham = [t for t in tik.get(cik, ()) if t in univ]
            pembeli = ', '.join(sorted({n for c, n in zip(g.cik, g.nama) if c != cik}))
            for t in saham:
                x = dict(status=status, saham=t, tarikh=r0.tarikh, borang=r0.borang, akses=akses, pembeli=pembeli)
                (calon if status == 'calon' else rekod).append(x)
    tambah, tamat = kemas_ambil(rekod)
    if calon:
        p = os.path.join(EDGAR, 'calon.csv')
        lama = pd.read_csv(p, dtype=str) if os.path.exists(p) else pd.DataFrame()
        pd.concat([lama, pd.DataFrame(calon)], ignore_index=True).drop_duplicates(['saham', 'akses']).to_csv(p, index=False)
    if proses:
        st['hari_terakhir'] = proses[-1]
    st.update(dijana=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), hari=proses[-15:], ditambah=tambah, ditamatkan=tamat,
              calon=len(calon), gagal=gagal[:20], ua_rahsia=bool(os.environ.get('SEC_USER_AGENT')))
    json.dump(st, open(stp, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(dict(hari=proses, ditambah=tambah, ditamatkan=tamat, calon=len(calon), gagal=gagal[:5]), ensure_ascii=False))
    return 1 if gagal and not proses else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='Lapisan EDGAR sasaran ambil alih bukan tunai')
    sp = ap.add_subparsers(dest='cmd', required=True)
    j = sp.add_parser('jalan'); j.add_argument('--mula'); j.add_argument('--hingga'); j.add_argument('--maks-hari', type=int, default=10)
    a = ap.parse_args(argv)
    return jalan(a)


if __name__ == '__main__':
    sys.exit(main() or 0)
