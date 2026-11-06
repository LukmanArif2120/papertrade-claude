# institusi_13f.py — aliran institusi (13F) setiap saham dan setiap sektor/industri (6 Nov 2026; keputusan pengguna:
# "saham yang institusi beli" + "sektor/industri yang hot", sumber SEC EDGAR, paparan digabung ke tab Sektor).
#
# PAPARAN SAHAJA. 13F ialah pegangan pada AKHIR SUKU, difail sehingga 45 hari kemudian, dan set data SEC diterbitkan
# ~2 minggu selepas tetingkap failnya tamat: data paling segar sudah 2.5–3.5 bulan pada hari ia muncul. Belum diuji
# sebagai peramal (registry N146 `PERLU:data_13f`). Kalibrasi tab Sektor 13 Okt 2026 sudah mendapati skor panas
# harga tidak meramal pulangan 1–3 bulan; jangan jadikan ini penapis belian tanpa pradaftar dan ukuran.
#
# Sumber (percuma, tanpa kunci):
#   www.sec.gov Form 13F data sets — zip setiap tetingkap FAIL 3 bulan (Mac–Mei, Jun–Ogo, Sep–Nov, Dis–Feb).
#     Tetingkap yang bermula pada bulan M membawa kebanyakan laporan tempoh akhir-bulan-M (cth. Jun–Ogo -> 30 Jun);
#     pemfail lewat dan pindaan tempoh itu muncul dalam tetingkap berikutnya, jadi tempoh P dibaca daripada S(P)+S(P+1).
#   api.openfigi.com — CUSIP -> ticker (13F tiada ticker). Cache data/institusi/cusip_ticker.csv; tanpa kunci
#     25 permintaan/min x 10 CUSIP. Pilihan: OPENFIGI_APIKEY (250/min x 100).
#
# Kaedah (tempoh P lawan P-1):
#   * Pemfail = CIK yang memfail 13F-HR bagi KEDUA-DUA tempoh. Pemfail yang hanya ada satu tempoh tidak dikira sebagai
#     "baru" atau "keluar" (kalau tidak, pemfail lewat/baharu disangka aliran).
#   * Pegangan pemfail = laporan asal terakhir ATAU pernyataan semula (RESTATEMENT) terakhir, mana lebih lewat, ditambah
#     pindaan NEW HOLDINGS yang difail selepasnya. Baris SH sahaja, tanpa put/call; dijumlah ikut (CIK, ticker).
#   * Pecahan saham: nisbah median saham P/P-1 pemegang berterusan; jika |log| > log 1.4 dan ia dekat (15%) dengan
#     nisbah pecahan biasa DAN harga bergerak bertentangan, saham P-1 didarab faktor itu.
#   * aliran_usd = (saham_inst − saham_inst_lalu×faktor) × harga P; ubah_saham_pct = perubahan saham institusi (%).
#   * Kumpulan (industri = peta_industri, sektor = SEKTOR_INDUSTRI): aliran_pct = Σaliran ÷ Σnilai lalu (berat nilai,
#     dikuasai saham besar) dan median ubah_saham_pct (berat sama, saham ≥ PEMEGANG_MIN pemegang lalu). skor = purata
#     pangkat persentil kedua-duanya; gred A > 80 … E <= 20 (sama seperti gred_kumpulan). Kumpulan < MIN_SAHAM tiada skor.
#
# Output (data/institusi/): saham.csv · kumpulan.csv (setiap tempoh, ditulis ganti ikut tempoh) · cusip_ticker.csv ·
#   status.json. Set zip dicache dalam --cache (tidak dikomit).
#
#   python3 standard/institusi_13f.py jalan [--suku 1] [--cache /tmp/f13]
#   (Actions: .github/workflows/institusi.yml, mingguan; set baharu muncul sekali setiap suku)
import argparse, json, math, os, re, sys, time, zipfile
from datetime import date, datetime, timedelta, timezone

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
sys.path.insert(0, HERE)

KELUAR = os.path.join(BS2, 'data', 'institusi')
PETA = os.path.join(BS2, 'papertrade', 'peta_industri.csv')
HALAMAN = 'https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets'
FIGI = 'https://api.openfigi.com/v3/mapping'
BULAN = {b: i + 1 for i, b in enumerate(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov',
                                         'dec'])}
PECAHAN = [1 / 50, 1 / 30, 1 / 25, 1 / 20, 1 / 15, 1 / 10, 1 / 8, 1 / 5, 1 / 4, 1 / 3, 1 / 2, 2 / 3, 3 / 2, 2, 3, 4, 5,
           8, 10, 15, 20, 25, 30, 50]
PEMFAIL_MIN = 3      # CUSIP dipetakan hanya jika dipegang >= 3 pemfail (13,000+ CUSIP; selebihnya hingar)
PEMEGANG_MIN = 5     # saham masuk median kumpulan jika pemegang lalu >= 5
MIN_SAHAM = 3
TERATAS = 5
LAJUR_SAHAM = ['tempoh', 'ticker', 'pemegang', 'pemegang_lalu', 'baru', 'keluar', 'bersih', 'saham_inst',
               'saham_inst_lalu', 'ubah_saham_pct', 'harga', 'aliran_usd', 'nilai_inst_usd', 'faktor_pecahan']
LAJUR_KUMP = ['tempoh', 'jenis', 'nama', 'sektor', 'n', 'aliran_usd', 'nilai_lalu_usd', 'aliran_pct',
              'median_ubah_pct', 'pct_bersih_positif', 'baru', 'keluar', 'skor', 'gred', 'teratas', 'dibina']


def ua():
    # Actions: rahsia SEC_USER_AGENT. Sandaran sesi: SEC menolak (403) UA yang mengandungi URL; yang ini diterima.
    return os.environ.get('SEC_USER_AGENT') or 'papertrade-claude research bot'


# ---------------------------------------------------------------- fungsi tulen (diuji ujian/test_institusi_13f.py)

def tempoh_set(nama):
    """'01jun2026-31aug2026_form13f.zip' -> (mula, akhir, tempoh) ; tempoh = akhir bulan mula."""
    m = re.search(r'(\d{2})([a-z]{3})(\d{4})-(\d{2})([a-z]{3})(\d{4})', nama.lower())
    if not m:
        return None
    mula = date(int(m[3]), BULAN[m[2]], int(m[1]))
    akhir = date(int(m[6]), BULAN[m[5]], int(m[4]))
    hujung = (date(mula.year + mula.month // 12, mula.month % 12 + 1, 1) - timedelta(days=1))
    return mula, akhir, hujung


def suku_lalu(t):
    """Akhir suku sebelum t (t sendiri akhir suku)."""
    awal = date(t.year, t.month, 1)
    b = awal - timedelta(days=1)                       # akhir bulan sebelum
    for _ in range(2):
        b = date(b.year, b.month, 1) - timedelta(days=1)
    return b


def pilih_akses(sub):
    """sub: DataFrame satu (CIK, tempoh) dengan akses, tarikh_fail, jenis (13F-HR | 13F-HR/A), pindaan
    ('' | RESTATEMENT | NEW HOLDINGS). Pulang senarai akses yang membentuk pegangan."""
    s = sub.sort_values(['tarikh_fail', 'akses'])
    asas = s[(s.jenis == '13F-HR') | (s.pindaan.str.upper().str.startswith('RESTATE'))]
    if asas.empty:
        return []
    a = asas.iloc[-1]
    tambah = s[(s.jenis == '13F-HR/A') & (s.pindaan.str.upper().str.startswith('NEW')) &
               ((s.tarikh_fail > a.tarikh_fail) | ((s.tarikh_fail == a.tarikh_fail) & (s.akses > a.akses)))]
    return [a.akses] + list(tambah.akses)


def faktor_pecahan(nisbah_saham, nisbah_harga):
    """Nisbah median saham P/P-1 pemegang berterusan dan nisbah harga P/P-1 -> faktor pecahan (1 jika tiada)."""
    if not (nisbah_saham > 0 and math.isfinite(nisbah_saham)) or abs(math.log(nisbah_saham)) <= math.log(1.4):
        return 1.0
    f = min(PECAHAN, key=lambda k: abs(math.log(nisbah_saham / k)))
    if abs(math.log(nisbah_saham / f)) > math.log(1.15):
        return 1.0
    if nisbah_harga > 0 and math.isfinite(nisbah_harga) and not (0.5 <= nisbah_harga * f <= 2.0):
        return 1.0
    return float(f)


def aliran(kini, lalu):
    """kini/lalu: DataFrame cik, ticker, saham, nilai (satu baris setiap pasangan; pemfail sudah dihadkan kepada
    yang ada dalam kedua-dua tempoh). Pulang DataFrame setiap ticker (LAJUR_SAHAM tanpa tempoh)."""
    g = kini.merge(lalu, on=['cik', 'ticker'], how='outer', suffixes=('', '_l')).fillna(0.0)
    hk = kini.groupby('ticker').agg(sk=('saham', 'sum'), nk=('nilai', 'sum'))
    hl = lalu.groupby('ticker').agg(sl=('saham', 'sum'), nl=('nilai', 'sum'))
    harga_k = (hk.nk / hk.sk).replace([np.inf, -np.inf], np.nan)
    harga_l = (hl.nl / hl.sl).replace([np.inf, -np.inf], np.nan)
    teru = g[(g.saham > 0) & (g.saham_l > 0)]
    r_med = (teru.saham / teru.saham_l).groupby(teru.ticker).median()
    ada, ada_l = g.saham > 0, g.saham_l > 0
    d = pd.DataFrame(dict(pemegang=ada, pemegang_lalu=ada_l, baru=ada & ~ada_l, keluar=~ada & ada_l,
                          saham_inst=g.saham, sl=g.saham_l, nilai_inst_usd=g.nilai)).groupby(g.ticker).sum()
    d = d.sort_index()
    nh = (harga_k / harga_l).reindex(d.index)
    d['faktor_pecahan'] = [faktor_pecahan(r_med.get(t, np.nan), nh.get(t, np.nan)) for t in d.index]
    d['saham_inst_lalu'] = d.sl * d.faktor_pecahan
    hrg = harga_k.reindex(d.index)
    d['harga'] = hrg.fillna(harga_l.reindex(d.index) / d.faktor_pecahan)
    d['bersih'] = d.baru - d.keluar
    d['ubah_saham_pct'] = np.where(d.saham_inst_lalu > 0, (d.saham_inst / d.saham_inst_lalu - 1) * 100, np.nan)
    d['aliran_usd'] = (d.saham_inst - d.saham_inst_lalu) * d.harga
    for c in ['pemegang', 'pemegang_lalu', 'baru', 'keluar', 'bersih']:
        d[c] = d[c].astype(int)
    return d.reset_index()[[c for c in LAJUR_SAHAM if c != 'tempoh']]


def doc_db(saham, kump, peta, sektor_industri, ringkas):
    """Dokumen db `institusi/kumpulan` (tab Sektor) bagi tempoh terkini: satu baris setiap sektor/industri dengan
    saham aliran teratas. Kunci pendek supaya dokumen kecil (~170 baris)."""
    tp = ringkas['tempoh']
    s = saham[saham.tempoh.astype(str) == tp].merge(peta[['ticker', 'industri']], on='ticker', how='inner')
    s['sektor'] = s.industri.map(sektor_industri).fillna('Lain-lain')
    s = s[s.pemegang_lalu >= PEMEGANG_MIN].sort_values('aliran_usd', ascending=False)

    def r(v, n=2):
        return None if v is None or (isinstance(v, float) and not math.isfinite(v)) else round(float(v), n)

    rows = []
    for x in kump[kump.tempoh.astype(str) == tp].itertuples():
        kunci = 'industri' if x.jenis == 'Industri' else 'sektor'
        t = s[s[kunci] == x.nama].head(TERATAS)
        rows.append(dict(j=x.jenis[0], n=x.nama, s=x.sektor, c=int(x.n), a=r(x.aliran_pct), m=r(x.median_ubah_pct),
                         b=r(x.pct_bersih_positif, 1), nb=int(x.baru), nk=int(x.keluar), u=r(x.aliran_usd / 1e6, 1),
                         sk=r(x.skor, 1), g=x.gred or None,
                         t=[[y.ticker, r(y.ubah_saham_pct, 1), int(y.bersih), r(y.aliran_usd / 1e6, 1)]
                            for y in t.itertuples()]))
    return dict(dibina=ringkas['dibina'], tempoh=tp, tempoh_lalu=ringkas['tempoh_lalu'],
                pemfail=ringkas['pemfail_dua'], saham=ringkas['saham'],
                nota='13F = pegangan akhir suku, difail sehingga 45 hari kemudian. Paparan sahaja, bukan penapis.',
                rows=rows)


def pangkat_gred(s):
    """Siri skor 0–100 -> gred A–E (sama seperti gred_kumpulan.gred)."""
    return s.map(lambda v: '' if pd.isna(v) else 'A' if v > 80 else 'B' if v > 60 else 'C' if v > 40
                 else 'D' if v > 20 else 'E')


def kumpulan(saham, peta, sektor_industri, dibina=''):
    """saham: output aliran() + tempoh; peta: DataFrame ticker, industri. Pulang LAJUR_KUMP."""
    d = saham.merge(peta[['ticker', 'industri']], on='ticker', how='inner')
    d['sektor'] = d.industri.map(sektor_industri).fillna('Lain-lain')
    keluar = []
    for jenis, kunci in [('Industri', 'industri'), ('Sektor', 'sektor')]:
        for (tp, nama), x in d.groupby(['tempoh', kunci]):
            nl = (x.saham_inst_lalu * x.harga).sum()
            m = x[x.pemegang_lalu >= PEMEGANG_MIN]
            ter = x[x.pemegang_lalu >= PEMEGANG_MIN].sort_values('aliran_usd', ascending=False).head(TERATAS)
            keluar.append(dict(tempoh=tp, jenis=jenis, nama=nama,
                               sektor=x.sektor.iloc[0] if jenis == 'Industri' else nama, n=len(x),
                               aliran_usd=x.aliran_usd.sum(), nilai_lalu_usd=nl,
                               aliran_pct=x.aliran_usd.sum() / nl * 100 if nl > 0 else np.nan,
                               median_ubah_pct=m.ubah_saham_pct.median() if len(m) else np.nan,
                               pct_bersih_positif=(x.bersih > 0).mean() * 100,
                               baru=int(x.baru.sum()), keluar=int(x.keluar.sum()),
                               teratas=' '.join(ter.ticker), dibina=dibina))
    k = pd.DataFrame(keluar, columns=[c for c in LAJUR_KUMP if c not in ('skor', 'gred')])
    k['skor'] = np.nan
    for (tp, j), idx in k.groupby(['tempoh', 'jenis']).groups.items():
        x = k.loc[idx]
        ok = x[(x.n >= MIN_SAHAM) & x.aliran_pct.notna() & x.median_ubah_pct.notna()]
        if len(ok) < 2:
            continue
        r = (ok.aliran_pct.rank(pct=True) + ok.median_ubah_pct.rank(pct=True)) / 2
        k.loc[ok.index, 'skor'] = ((r.rank(pct=True) * 100)).round(1)
    k['gred'] = pangkat_gred(k.skor)
    return k.sort_values(['tempoh', 'jenis', 'skor'], ascending=[True, True, False], na_position='last')[LAJUR_KUMP]


# ---------------------------------------------------------------- I/O

def senarai_set():
    import requests
    r = requests.get(HALAMAN, headers={'User-Agent': ua()}, timeout=60)
    r.raise_for_status()
    sets = {}
    for href in re.findall(r'href="([^"]*form13f\.zip)"', r.text):
        t = tempoh_set(href)
        if t:
            sets[t[2]] = dict(url='https://www.sec.gov' + href if href.startswith('/') else href, mula=t[0],
                              akhir=t[1], nama=os.path.basename(href))
    return sets


def muat_turun(info, cache):
    import requests
    os.makedirs(cache, exist_ok=True)
    p = os.path.join(cache, info['nama'])
    if os.path.exists(p) and zipfile.is_zipfile(p):
        return p
    for n in range(4):
        try:
            with requests.get(info['url'], headers={'User-Agent': ua()}, timeout=600, stream=True) as r:
                r.raise_for_status()
                with open(p + '.tmp', 'wb') as f:
                    for b in r.iter_content(1 << 20):
                        f.write(b)
            os.replace(p + '.tmp', p)
            if zipfile.is_zipfile(p):
                return p
        except Exception as e:  # noqa: BLE001
            print(f'  gagal muat turun {info["nama"]} ({e}); cuba lagi', flush=True)
        time.sleep(10 * (n + 1))
    raise SystemExit(f'tidak dapat memuat turun {info["url"]}')


def _tarikh(s):
    return pd.to_datetime(s, format='%d-%b-%Y', errors='coerce')


def submisi(zips):
    """Gabung SUBMISSION + COVERPAGE semua zip -> akses, cik, tarikh_fail, jenis, tempoh, pindaan, zip."""
    out = []
    for z in zips:
        with zipfile.ZipFile(z) as zf:
            s = pd.read_csv(zf.open('SUBMISSION.tsv'), sep='\t', dtype=str, keep_default_na=False)
            c = pd.read_csv(zf.open('COVERPAGE.tsv'), sep='\t', dtype=str, keep_default_na=False,
                            usecols=['ACCESSION_NUMBER', 'AMENDMENTTYPE'])
        s = s.merge(c, on='ACCESSION_NUMBER', how='left').fillna('')
        s = s[s.SUBMISSIONTYPE.isin(['13F-HR', '13F-HR/A'])]
        out.append(pd.DataFrame(dict(akses=s.ACCESSION_NUMBER, cik=s.CIK.str.lstrip('0'),
                                     tarikh_fail=_tarikh(s.FILING_DATE), jenis=s.SUBMISSIONTYPE,
                                     tempoh=_tarikh(s.PERIODOFREPORT).dt.date, pindaan=s.AMENDMENTTYPE, zip=z)))
    d = pd.concat(out, ignore_index=True)
    return d.drop_duplicates('akses', keep='last')


def akses_tempoh(sub, tp):
    """{akses: zip} bagi tempoh tp; dan set CIK yang memfail."""
    x = sub[sub.tempoh == tp]
    pilih = {}
    for _, g in x.groupby('cik'):
        for a in pilih_akses(g):
            pilih[a] = g.loc[g.akses == a, 'zip'].iloc[0]
    return pilih, set(x[x.akses.isin(pilih)].cik)


def baca_pegangan(pilih, sub):
    """Baris INFOTABLE bagi akses dipilih -> DataFrame cik, cusip, saham, nilai (SH, tanpa put/call)."""
    cik = sub.set_index('akses').cik
    out = []
    for z in sorted(set(pilih.values())):
        mahu = {a for a, zz in pilih.items() if zz == z}
        with zipfile.ZipFile(z) as zf:
            for ch in pd.read_csv(zf.open('INFOTABLE.tsv'), sep='\t', dtype=str, chunksize=500_000,
                                  usecols=['ACCESSION_NUMBER', 'CUSIP', 'VALUE', 'SSHPRNAMT', 'SSHPRNAMTTYPE',
                                           'PUTCALL']):
                ch = ch[ch.ACCESSION_NUMBER.isin(mahu) & (ch.SSHPRNAMTTYPE == 'SH') & ch.PUTCALL.isna()]
                out.append(pd.DataFrame(dict(cik=ch.ACCESSION_NUMBER.map(cik), cusip=ch.CUSIP.str.upper().str.strip(),
                                             saham=pd.to_numeric(ch.SSHPRNAMT, errors='coerce'),
                                             nilai=pd.to_numeric(ch.VALUE, errors='coerce'))))
    d = pd.concat(out, ignore_index=True).dropna()
    d = d[(d.saham > 0) & (d.cusip.str.len() == 9)]
    return d.groupby(['cik', 'cusip'], as_index=False)[['saham', 'nilai']].sum()


def peta_cusip(cusips, laluan, had_masa=None):
    """Kemas kini cache CUSIP -> ticker melalui OpenFIGI. CUSIP tanpa padanan disimpan kosong dan dicuba semula
    selepas 90 hari. Pulang dict cusip -> ticker (format repo: BRK.B)."""
    import requests
    lajur = ['cusip', 'ticker', 'nama', 'jenis', 'dikemas']
    c = pd.read_csv(laluan, dtype=str, keep_default_na=False) if os.path.exists(laluan) else pd.DataFrame(columns=lajur)
    hari = date.today().isoformat()
    lama = (date.today() - timedelta(days=90)).isoformat()
    ada = set(c.cusip[(c.ticker != '') | (c.dikemas >= lama)])
    perlu = sorted(set(cusips) - ada)
    kunci = os.environ.get('OPENFIGI_APIKEY', '')
    saiz, jeda = (100, 0.25) if kunci else (10, 2.45)
    kepala = {'Content-Type': 'application/json', **({'X-OPENFIGI-APIKEY': kunci} if kunci else {})}
    print(f'OpenFIGI: {len(perlu)} CUSIP perlu dipetakan (cache {len(c)})', flush=True)
    baru, mula = [], time.time()
    for i in range(0, len(perlu), saiz):
        if had_masa and time.time() - mula > had_masa:
            print(f'  had masa: berhenti pada {i}/{len(perlu)} (sambung larian seterusnya)', flush=True)
            break
        kump = perlu[i:i + saiz]
        for n in range(5):
            r = requests.post(FIGI, headers=kepala, timeout=60,
                              json=[{'idType': 'ID_CUSIP', 'idValue': x, 'exchCode': 'US'} for x in kump])
            if r.status_code == 429:
                time.sleep(int(r.headers.get('ratelimit-reset', 60)) + 1)
                continue
            r.raise_for_status()
            break
        else:
            raise SystemExit('OpenFIGI: had kadar berulang')
        for x, j in zip(kump, r.json()):
            d = (j.get('data') or [{}])[0]
            baru.append(dict(cusip=x, ticker=(d.get('ticker') or '').replace('/', '.'), nama=d.get('name') or '',
                             jenis=d.get('securityType') or '', dikemas=hari))
        if (i // saiz) % 50 == 0:
            print(f'  {i + len(kump)}/{len(perlu)}', flush=True)
        time.sleep(jeda)
    if baru:
        b = pd.DataFrame(baru, columns=lajur)
        c = pd.concat([c[~c.cusip.isin(b.cusip)], b]).sort_values('cusip')
        os.makedirs(os.path.dirname(laluan), exist_ok=True)
        c.to_csv(laluan, index=False)
    return dict(zip(c.cusip, c.ticker))


def _ganti(laluan, baru, lajur):
    """Tulis ganti baris tempoh yang dikira semula; tempoh lain dikekalkan."""
    if os.path.exists(laluan):
        lama = pd.read_csv(laluan, dtype={'tempoh': str}, keep_default_na=False)
        lama = lama[~lama.tempoh.isin(set(baru.tempoh.astype(str)))]
        baru = pd.concat([lama, baru.astype({'tempoh': str})], ignore_index=True)
    baru[lajur].to_csv(laluan, index=False, float_format='%.6g')


def jalan(a):
    from sektor_pasaran import SEKTOR_INDUSTRI
    sets = senarai_set()
    tempoh = sorted(sets)
    print('set SEC:', ', '.join(f'{t}' for t in tempoh[-4:]), flush=True)
    # tempoh yang boleh dikira: P dan P-1 kedua-duanya ada set
    calon = [t for t in tempoh if suku_lalu(t) in sets][-a.suku:]
    if not calon:
        raise SystemExit('tiada tempoh dengan dua set berturut-turut')
    peta = pd.read_csv(a.peta, dtype=str, keep_default_na=False).drop_duplicates('ticker')
    univ = set(peta.ticker)
    dibina = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M MYT')
    semua_saham, ringkas = [], []
    for P in calon:
        L = suku_lalu(P)
        perlu = [t for t in (L, P, min([t for t in tempoh if t > P], default=None)) if t is not None]
        zips = [muat_turun(sets[t], a.cache) for t in perlu]
        sub = submisi(zips)
        pk, ck = akses_tempoh(sub, P)
        pl, cl = akses_tempoh(sub, L)
        dua = ck & cl
        gk, gl = baca_pegangan(pk, sub), baca_pegangan(pl, sub)
        gk, gl = gk[gk.cik.isin(dua)], gl[gl.cik.isin(dua)]
        n = pd.concat([gk, gl]).groupby('cusip').cik.nunique()
        tick = peta_cusip(list(n[n >= PEMFAIL_MIN].index), a.cusip, a.had_figi)
        f = lambda g: (g.assign(ticker=g.cusip.map(tick)).query('ticker in @univ')  # noqa: E731
                       .groupby(['cik', 'ticker'], as_index=False)[['saham', 'nilai']].sum())
        s = aliran(f(gk), f(gl))
        s.insert(0, 'tempoh', P.isoformat())
        semua_saham.append(s)
        ringkas.append(dict(tempoh=P.isoformat(), tempoh_lalu=L.isoformat(), set=[sets[t]['nama'] for t in perlu],
                            pemfail_kini=len(ck), pemfail_lalu=len(cl), pemfail_dua=len(dua), saham=len(s)))
        print(f'{P}: pemfail {len(ck)}/{len(cl)} (kedua-dua {len(dua)}), saham {len(s)}', flush=True)
    S = pd.concat(semua_saham, ignore_index=True)
    K = kumpulan(S, peta, SEKTOR_INDUSTRI, dibina)
    os.makedirs(a.keluar, exist_ok=True)
    _ganti(os.path.join(a.keluar, 'saham.csv'), S, LAJUR_SAHAM)
    _ganti(os.path.join(a.keluar, 'kumpulan.csv'), K, LAJUR_KUMP)
    st = dict(dibina=dibina, tempoh_terkini=calon[-1].isoformat(), tempoh=ringkas,
              set_terkini=sets[tempoh[-1]]['nama'],
              nota='Pegangan akhir suku 13F; difail sehingga 45 hari selepas suku; paparan sahaja, bukan penapis.')
    with open(os.path.join(a.keluar, 'status.json'), 'w') as fh:
        json.dump(st, fh, ensure_ascii=False, indent=1)
    doc = doc_db(S, K, peta, SEKTOR_INDUSTRI, dict(ringkas[-1], dibina=dibina))
    with open(os.path.join(a.keluar, 'db.json'), 'w') as fh:
        json.dump(doc, fh, ensure_ascii=False, separators=(',', ':'))
    for j in ['Sektor', 'Industri']:
        x = K[(K.tempoh == calon[-1].isoformat()) & (K.jenis == j)]
        print(j, 'teratas:', ', '.join(f'{r.nama} {r.aliran_pct:+.1f}%' for r in x.head(5).itertuples()))


def main(argv=None):
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    j = sp.add_parser('jalan')
    j.add_argument('--suku', type=int, default=1, help='bilangan tempoh terkini dikira (isi sejarah: > 1)')
    j.add_argument('--cache', default=os.path.join('/tmp', 'f13'))
    j.add_argument('--keluar', default=KELUAR)
    j.add_argument('--peta', default=PETA)
    j.add_argument('--cusip', default=os.path.join(KELUAR, 'cusip_ticker.csv'))
    j.add_argument('--had-figi', type=float, default=None, help='had saat pemetaan OpenFIGI setiap larian')
    a = ap.parse_args(argv)
    jalan(a)


if __name__ == '__main__':
    main()
