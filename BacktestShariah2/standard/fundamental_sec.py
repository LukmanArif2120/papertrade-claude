# fundamental_sec.py — EPS dan hasil suku point-in-time daripada SEC XBRL + tarikh pengumuman earnings daripada 8-K
# (27 Okt 2026; senarai alat #56/#57). Asas kaedah PEAD (drift selepas kejutan earnings) dan penapis fundamental AUTOTUNE
# A04. GitHub Actions `fundamental_sec.yml` sahaja (tanpa LLM; sesi Claude tidak boleh capai sec.gov).
#
# Sumber (percuma, tanpa kunci; User-Agent wajib = rahsia SEC_USER_AGENT; had SEC 10 permintaan/saat):
#   data.sec.gov/submissions/CIK##########.json   -> pemfailan; 8-K Item 2.02 = pengumuman keputusan (earnings)
#   data.sec.gov/api/xbrl/companyfacts/CIK…json  -> EPS (cair) dan hasil setiap tempoh, dengan tarikh fail
#
# Point-in-time: bagi setiap (saham, metrik, akhir tempoh) hanya nilai yang PERTAMA difailkan disimpan (nilai yang
# diketahui pada masa itu; pernyataan semula kemudian diabaikan). Suku = tempoh 80–100 hari. Q4 tiada dalam 10-Q:
# diterbitkan = tahunan (10-K, 350–380 hari) − 3 suku tahun fiskal sama (terbitan=1; EPS Q4 terbitan ialah anggaran
# kerana bilangan saham berubah).
#
# Output (BacktestShariah2/data/sec/):
#   eps_hasil.csv   saham, cik, metrik (eps|hasil), mula, akhir, nilai, tarikh_fail, borang, akses, terbitan
#   earnings_8k.csv saham, cik, tarikh_fail, masa_terima, akses, items   (8-K mengandungi Item 2.02)
#   sue.csv         saham, akhir, eps, eps_lalu, sue, hasil, tumbuh_hasil, pecutan_hasil, tarikh_umum, sumber_tarikh
#                   SUE = (EPS_t − EPS_t−4) / maks(sisihan piawai perbezaan sama 8 suku sebelumnya (min 4), USD0.01);
#                   EPS_t−4 = angka perbandingan dalam pemfailan suku t (dilaras pecahan saham); SUE kosong jika |EPS|
#                   > 20 × median |EPS| saham + 1 (ralat unit XBRL). tarikh_umum =
#                   8-K Item 2.02 pertama dalam (akhir, tarikh_fail]; jika tiada, tarikh_fail 10-Q/10-K (sumber_tarikh).
#                   tumbuh_hasil = hasil_t / hasil_t−4 − 1; pecutan_hasil = tumbuh_t − tumbuh_t−1.
#   status.json     akses terakhir setiap CIK (larian tambahan: companyfacts hanya diambil semula jika ada 10-Q/10-K baharu)
#
#   python3 standard/fundamental_sec.py jalan [--maks-fakta 300] [--maks-saham 0] [--saham AAPL,MSFT]
#
# Universe (28 Okt 2026): data/univ_sec.txt (3260 ticker A02) U tawaran_edgar.universe(). Dilebarkan daripada 911
# supaya leg fundamental REVERSE fasa 2 diuji atas populasi yang sama dengan fasa 1 (SEC XBRL nilai pertama difail
# = titik-masa secara retrospektif sejak 2009, jadi leg ini tidak perlu menunggu Okt 2027).
import argparse, json, os, sys
from datetime import date, datetime, timezone

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tawaran_edgar as TE  # noqa: E402  (ua, ambil, peta_ticker, universe, muat_peta)

BS2 = os.path.dirname(HERE)
SEC = os.path.join(BS2, 'data', 'sec')
UNIV_SEC = os.path.join(BS2, 'data', 'univ_sec.txt')
SUBMISSIONS = 'https://data.sec.gov/submissions/CIK{cik:010d}.json'
SUBMISSIONS_LAMA = 'https://data.sec.gov/submissions/{nama}'
FAKTA = 'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json'
TAG_EPS = ['EarningsPerShareDiluted', 'EarningsPerShareBasicAndDiluted', 'EarningsPerShareBasic']
TAG_HASIL = ['Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax', 'SalesRevenueNet',
             'RevenueFromContractWithCustomerIncludingAssessedTax', 'RevenuesNetOfInterestExpense']
BORANG_LAPOR = {'10-Q', '10-K', '10-Q/A', '10-K/A', '10-KT', '20-F', '40-F'}
VERSI = 3           # naikkan bila kiraan berubah: semua companyfacts diambil semula (v2: perbandingan pemfailan sama +
                    # penyebut minimum; v3: penapis kewarasan EPS)
EPS_GANDA_MAKS = 20  # |EPS| > 20 × median |EPS| saham + 1 = ralat unit XBRL (cth. DXCM −40000): SUE dikosongkan
SUE_MIN_SP = 0.01   # penyebut minimum SUE (USD 1 sen): elak SUE meletup bila EPS hampir malar
LAJUR_EH = ['saham', 'cik', 'metrik', 'mula', 'akhir', 'nilai', 'tarikh_fail', 'borang', 'akses', 'terbitan']
LAJUR_8K = ['saham', 'cik', 'tarikh_fail', 'masa_terima', 'akses', 'items']
LAJUR_SUE = ['saham', 'akhir', 'eps', 'eps_lalu', 'sue', 'hasil', 'tumbuh_hasil', 'pecutan_hasil', 'tarikh_umum',
             'sumber_tarikh']


def univ_sec():
    """Universe SEC = data/univ_sec.txt (3260 ticker A02, untuk leg fundamental REVERSE fasa 2) DALAM KESATUAN
    dengan tawaran_edgar.universe() (univ.txt + posisi claude*.csv). Kesatuan supaya liputan tidak susut dan
    edgar.yml (pengesan ambil alih) kekal pada universe-nya sendiri."""
    u = set(TE.universe())
    if os.path.exists(UNIV_SEC):
        with open(UNIV_SEC, encoding='utf-8') as f:
            u |= {x.strip().replace('US.', '') for x in f if x.strip() and not x.lstrip().startswith('#')}
    return u


def putaran(pasangan, kursor, maks):
    """Sublist `maks` pasangan (cik, ticker) bermula selepas `kursor` (ticker), berputar. maks <= 0 = semua.

    Larian terhad masih menulis kemajuan (`_ganti` hanya menggantikan baris ticker yang disentuh), jadi isian
    awal 3260 ticker boleh dipecahkan merentas beberapa larian tanpa melebihi had masa workflow."""
    if maks <= 0 or maks >= len(pasangan):
        return pasangan, ''
    mula = next((i for i, (_, t) in enumerate(pasangan) if t > kursor), 0) if kursor else 0
    pilih = [pasangan[(mula + i) % len(pasangan)] for i in range(maks)]
    return pilih, pilih[-1][1]


# ---------------------------------------------------------------- penghurai (diuji tanpa rangkaian)
def _hari(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days


def hurai_fakta(js, tags, unit):
    """companyfacts -> DataFrame mula, akhir, nilai, tarikh_fail, borang, akses, fy, tempoh_hari (semua tag, unit tertentu).
    Tag awal dalam senarai didahulukan bagi akhir tempoh yang sama."""
    rows = []
    gaap = (js.get('facts') or {}).get('us-gaap') or {}
    for keutamaan, tag in enumerate(tags):
        for x in ((gaap.get(tag) or {}).get('units') or {}).get(unit, []):
            if not x.get('start') or not x.get('end') or x.get('val') is None:
                continue
            rows.append(dict(mula=x['start'], akhir=x['end'], nilai=float(x['val']), tarikh_fail=x.get('filed', ''),
                             borang=x.get('form', ''), akses=x.get('accn', ''), fy=x.get('fy'),
                             tempoh_hari=_hari(x['start'], x['end']), keutamaan=keutamaan))
    return pd.DataFrame(rows, columns=['mula', 'akhir', 'nilai', 'tarikh_fail', 'borang', 'akses', 'fy', 'tempoh_hari',
                                       'keutamaan'])


def pertama_difail(df):
    """Satu baris setiap (akhir, tempoh): tag keutamaan tertinggi, kemudian fail paling awal (point-in-time)."""
    if df.empty:
        return df
    df = df.sort_values(['akhir', 'tempoh_hari', 'keutamaan', 'tarikh_fail'])
    return df.drop_duplicates(['akhir', 'tempoh_hari'], keep='first')


def suku(df):
    """Nilai suku (80–100 hari) + Q4 terbitan = tahunan (350–380 hari) − 3 suku dalam tempoh tahunan itu."""
    df = pertama_difail(df)
    if df.empty:
        return pd.DataFrame(columns=['mula', 'akhir', 'nilai', 'tarikh_fail', 'borang', 'akses', 'terbitan'])
    q = df[df.tempoh_hari.between(80, 100)].copy()
    q['terbitan'] = 0
    out = [q]
    qm, qa = pd.to_datetime(q.mula), pd.to_datetime(q.akhir)
    for _, t in df[df.tempoh_hari.between(350, 380)].iterrows():
        if (q.akhir == t.akhir).any():
            continue                                    # suku keempat sudah dilapor terus
        tm, ta = pd.Timestamp(t.mula), pd.Timestamp(t.akhir)
        dlm = q[(qm >= tm - pd.Timedelta(days=7)) & (qa < ta)]
        if len(dlm) != 3:
            continue
        mula4 = (pd.Timestamp(dlm.akhir.max()) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        out.append(pd.DataFrame([dict(mula=mula4, akhir=t.akhir, nilai=t.nilai - dlm.nilai.sum(), tarikh_fail=t.tarikh_fail,
                                      borang=t.borang, akses=t.akses, terbitan=1)]))
    r = pd.concat(out, ignore_index=True)
    r = r.sort_values(['akhir', 'terbitan']).drop_duplicates('akhir', keep='first')
    return r[['mula', 'akhir', 'nilai', 'tarikh_fail', 'borang', 'akses', 'terbitan']].reset_index(drop=True)


def hurai_8k(js):
    """submissions (blok 'recent' atau fail lama) -> DataFrame tarikh_fail, masa_terima, akses, items bagi 8-K Item 2.02."""
    r = js.get('filings', {}).get('recent', js) if isinstance(js, dict) else {}
    borang = r.get('form') or []
    rows = []
    for i, f in enumerate(borang):
        if f not in ('8-K', '8-K/A'):
            continue
        items = (r.get('items') or [''] * len(borang))[i] or ''
        if '2.02' not in items.split(','):
            continue
        rows.append(dict(tarikh_fail=r['filingDate'][i], masa_terima=(r.get('acceptanceDateTime') or [''] * len(borang))[i],
                         akses=r['accessionNumber'][i], items=items))
    return pd.DataFrame(rows, columns=['tarikh_fail', 'masa_terima', 'akses', 'items'])


def akses_lapor_terkini(js):
    """Nombor akses 10-Q/10-K terkini dalam submissions (penanda: perlu ambil companyfacts semula?)."""
    r = js.get('filings', {}).get('recent', {})
    for f, a in zip(r.get('form') or [], r.get('accessionNumber') or []):
        if f in BORANG_LAPOR:
            return a
    return None


def nilai_banding(mentah, q):
    """Bagi setiap suku dilapor terus (terbitan=0): nilai suku setahun lebih awal seperti tercetak dalam pemfailan YANG SAMA
    (angka perbandingan; sudah dilaras pecahan saham dan masih point-in-time). Siri akhir -> nilai."""
    out = {}
    if mentah.empty or q.empty:
        return pd.Series(out, dtype=float)
    m = mentah[mentah.tempoh_hari.between(80, 100)].copy()
    m['akhir_dt'] = pd.to_datetime(m.akhir)
    for _, x in q[q.terbitan == 0].iterrows():
        t = pd.Timestamp(x.akhir)
        c = m[(m.akses == x.akses) & (m.akhir_dt >= t - pd.Timedelta(days=390)) & (m.akhir_dt <= t - pd.Timedelta(days=340))]
        if len(c):
            out[x.akhir] = float(c.sort_values('keutamaan').nilai.iloc[0])
    return pd.Series(out, dtype=float)


def kira_sue(eps, hasil, k8, banding=None):
    """eps/hasil: DataFrame suku (akhir, nilai, tarikh_fail); k8: DataFrame 8-K (tarikh_fail); banding: siri akhir -> EPS
    setahun lebih awal daripada pemfailan sama (nilai_banding; jika tiada, nilai pertama difail) -> DataFrame LAJUR_SUE."""
    if eps.empty:
        return pd.DataFrame(columns=LAJUR_SUE[1:])
    e = eps.sort_values('akhir').reset_index(drop=True)
    akhir = pd.to_datetime(e.akhir)
    rows = []
    hs = hasil.set_index('akhir').nilai if not hasil.empty else pd.Series(dtype=float)
    hs_dt = pd.Series(hs.values, index=pd.to_datetime(hs.index)).sort_index() if len(hs) else hs
    k8d = sorted(pd.to_datetime(k8.tarikh_fail)) if not k8.empty else []

    def lalu(siri_dt, t):            # nilai ~ setahun sebelum t (±25 hari)
        if not len(siri_dt):
            return np.nan
        c = siri_dt[(siri_dt.index >= t - pd.Timedelta(days=390)) & (siri_dt.index <= t - pd.Timedelta(days=340))]
        return float(c.iloc[-1]) if len(c) else np.nan

    eps_dt = pd.Series(e.nilai.values, index=akhir)
    sifar = e.nilai.abs()[e.nilai.abs() > 0]
    batas = EPS_GANDA_MAKS * (float(sifar.median()) if len(sifar) else 0.0) + 1.0
    beza = []
    for i, r in e.iterrows():
        t = akhir[i]
        el = float(banding[r.akhir]) if banding is not None and r.akhir in banding.index else lalu(eps_dt, t)
        d = r.nilai - el if not np.isnan(el) else np.nan
        sejarah = [x for x in beza[-8:] if not np.isnan(x)]
        waras = abs(r.nilai) <= batas and (np.isnan(el) or abs(el) <= batas)
        if not waras:
            d = np.nan                                  # tidak masuk sejarah perbezaan juga
        sue = d / max(np.std(sejarah, ddof=1), SUE_MIN_SP) if not np.isnan(d) and len(sejarah) >= 4 else np.nan
        beza.append(d)
        h = float(hs_dt.get(t, np.nan)) if len(hs_dt) else np.nan
        hl = lalu(hs_dt, t)
        tumbuh = h / hl - 1 if not np.isnan(h) and not np.isnan(hl) and hl > 0 else np.nan
        fail = pd.Timestamp(r.tarikh_fail)
        umum = [d8 for d8 in k8d if t < d8 <= fail]
        rows.append(dict(akhir=r.akhir, eps=r.nilai, eps_lalu=el, sue=sue, hasil=h, tumbuh_hasil=tumbuh,
                         tarikh_umum=(umum[0] if umum else fail).strftime('%Y-%m-%d'),
                         sumber_tarikh='8k' if umum else 'fail'))
    out = pd.DataFrame(rows)
    out['pecutan_hasil'] = out.tumbuh_hasil.diff()
    return out[LAJUR_SUE[1:]]


# ---------------------------------------------------------------- larian
def _baca(nama, lajur):
    p = os.path.join(SEC, nama)
    return pd.read_csv(p, dtype={'cik': 'Int64'}) if os.path.exists(p) else pd.DataFrame(columns=lajur)


def _ganti(lama, baru, saham):
    return pd.concat([lama[~lama.saham.isin(saham)], baru], ignore_index=True)


def jalan(a):
    os.makedirs(SEC, exist_ok=True)
    stp = os.path.join(SEC, 'status.json')
    st = json.load(open(stp)) if os.path.exists(stp) else {}
    if not os.environ.get('SEC_USER_AGENT'):
        print(json.dumps(dict(langkau='rahsia SEC_USER_AGENT belum ditetapkan (nama + e-mel hubungan; SEC wajibkan)'), ensure_ascii=False))
        return 0
    peta = TE.muat_peta()
    univ = set(a.saham.split(',')) if a.saham else univ_sec()
    cik_saham = {}
    for c, ts in peta.items():
        for t in ts:
            if t in univ:
                cik_saham.setdefault(c, t)          # satu ticker bagi setiap CIK (kelas pertama dalam senarai SEC)
    akses = st.get('akses', {}) if st.get('versi') == VERSI else {}   # versi kiraan berubah -> isi semula
    sej8k = set(st.get('sejarah_8k', [])) | (set(st.get('akses', {})) if 'sejarah_8k' not in st else set())
    eh, k8, sue = _baca('eps_hasil.csv', LAJUR_EH), _baca('earnings_8k.csv', LAJUR_8K), _baca('sue.csv', LAJUR_SUE)
    if st.get('versi') != VERSI:                # tiada campuran baris kiraan lama dan baharu
        eh, sue = pd.DataFrame(columns=LAJUR_EH), pd.DataFrame(columns=LAJUR_SUE)
    baru_eh, baru_k8, baru_sue, dikemas, gagal, fakta_n = [], [], [], [], [], 0
    pilih, kursor = putaran(sorted(cik_saham.items(), key=lambda kv: kv[1]), st.get('kursor', ''), a.maks_saham)
    for cik, t in pilih:
        try:
            sub = json.loads(TE.ambil(SUBMISSIONS.format(cik=cik)) or '{}')
        except Exception as e:
            gagal.append(f'{t} submissions: {e}'); continue
        kk = hurai_8k(sub)
        if str(cik) not in sej8k:                   # kali pertama: halaman 8-K lama juga (sekali sahaja setiap CIK)
            lengkap = True
            for f in (sub.get('filings', {}).get('files') or []):
                try:
                    kk = pd.concat([kk, hurai_8k(json.loads(TE.ambil(SUBMISSIONS_LAMA.format(nama=f['name'])) or '{}'))])
                except Exception as e:
                    gagal.append(f'{t} {f.get("name")}: {e}'); lengkap = False
            if lengkap:
                sej8k.add(str(cik))
        lama8 = k8[k8.saham == t][['tarikh_fail', 'masa_terima', 'akses', 'items']]
        kk = pd.concat([lama8, kk], ignore_index=True).drop_duplicates('akses')   # sejarah 8-K lama dikekalkan
        lapor = akses_lapor_terkini(sub)
        if not lapor:
            # Tiada 10-Q/10-K/20-F dalam submissions (ETF, dana, syarikat dorman): tiada companyfacts
            # suku untuk diambil, SELAMANYA. Tanda siap supaya `belum_diisi` tidak dikira kekal > 0
            # dan isian awal boleh dilaporkan selesai. '' tidak akan sama dengan mana-mana `lapor`
            # sebenar, jadi ia tidak menghalang pengambilan jika pemfailan muncul kemudian.
            akses.setdefault(str(cik), '')
        perlu = lapor and akses.get(str(cik)) != lapor
        if perlu and fakta_n < a.maks_fakta:
            try:
                js = json.loads(TE.ambil(FAKTA.format(cik=cik)) or '{}')
            except Exception as e:
                gagal.append(f'{t} companyfacts: {e}'); continue
            fakta_n += 1
            me = hurai_fakta(js, TAG_EPS, 'USD/shares')
            qe = suku(me)
            qh = suku(hurai_fakta(js, TAG_HASIL, 'USD'))
            for m, q in (('eps', qe), ('hasil', qh)):
                if not q.empty:
                    baru_eh.append(q.assign(saham=t, cik=cik, metrik=m)[LAJUR_EH])
            s = kira_sue(qe, qh, kk, nilai_banding(me, qe))
            if not s.empty:
                baru_sue.append(s.assign(saham=t)[LAJUR_SUE])
            akses[str(cik)] = lapor
            dikemas.append(t)
        if not kk.empty:
            baru_k8.append(kk.assign(saham=t, cik=cik)[LAJUR_8K])
    if baru_eh:
        eh = _ganti(eh, pd.concat(baru_eh), dikemas)
    if baru_sue:
        sue = _ganti(sue, pd.concat(baru_sue), dikemas)
    if baru_k8:
        b8 = pd.concat(baru_k8)
        k8 = _ganti(k8, b8, set(b8.saham))
    eh.sort_values(['saham', 'metrik', 'akhir']).to_csv(os.path.join(SEC, 'eps_hasil.csv'), index=False, float_format='%.10g')
    k8.sort_values(['saham', 'tarikh_fail']).to_csv(os.path.join(SEC, 'earnings_8k.csv'), index=False)
    sue.sort_values(['saham', 'akhir']).to_csv(os.path.join(SEC, 'sue.csv'), index=False, float_format='%.6g')
    baki = sum(1 for c in cik_saham if str(c) not in akses)
    st.update(versi=VERSI, akses=akses, sejarah_8k=sorted(sej8k), dijana=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), saham_universe=len(cik_saham),
              companyfacts_diambil=fakta_n, belum_diisi=baki, gagal=gagal[:20], kursor=kursor,
              saham_disentuh=len(pilih))
    json.dump(st, open(stp, 'w'), ensure_ascii=False, indent=1, sort_keys=True)
    print(json.dumps(dict(saham=len(cik_saham), disentuh=len(pilih), kursor=kursor, companyfacts=fakta_n, belum_diisi=baki, baris_sue=len(sue),
                          baris_8k=len(k8), gagal=len(gagal), contoh_gagal=gagal[:3]), ensure_ascii=False))
    return 1 if gagal and not dikemas and not baru_k8 else 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('perintah', choices=['jalan'])
    ap.add_argument('--maks-fakta', type=int, default=300, help='companyfacts maksimum setiap larian (isian awal berperingkat)')
    ap.add_argument('--maks-saham', type=int, default=0, help='ticker maksimum disentuh setiap larian (0 = semua; berputar ikut kursor status.json)')
    ap.add_argument('--saham', default='', help='senarai ticker (ujian); kosong = universe')
    a = ap.parse_args(argv)
    return jalan(a)


if __name__ == '__main__':
    sys.exit(main())
