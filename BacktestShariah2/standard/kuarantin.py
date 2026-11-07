"""kuarantin.py — kuarantin data harga ticker yang tercemar (7 Nov 2026).

Latar (disahkan 7 Nov 2026): dalam stor harga, bar SUPN 2026-10-21 hingga 2026-11-02 = bar INDV x 0.775910 dengan volum
yang SAMA — yfinance menyajikan data INDV di bawah simbol SUPN (direktori Nasdaq 2026-11-03: INDV `buang`, SUPN
`tukar_nama`). Larian 2026-11-04 05:45 UTC mengesan `anomali` (nisbah 0.846397, serak 3.1%) tetapi
`harga_yf.gabung_satu` tetap MEMADAM bar lama yang bertindih dan menulis bar tercemar. Kemudian dividen palsu yang sama
(D=8.13 P=36.28) menjadi baris faktor `dividen_khas 0.775910` pada KEDUA-DUA INDV dan SUPN, dan faktor itu didarab pada
388 bar SUPN. Akibatnya 51 baris Lejar SUPN dilaras 0.64–0.66 (keluar di luar julat hari itu) dan posisi Papertrade C INDV
M19 menunjukkan +33.9% palsu (harga beli dilaras oleh faktor palsu).

Fail `data/harga/kuarantin.csv` (TAMBAH SAHAJA; satu kuarantin = pasangan ticker + tarikh_mula):
  ticker       simbol gaya repo
  tarikh_mula  YYYY-MM-DD: bar bertarikh pada/selepas ini tidak boleh dipercayai
  sebab        teks bukti
  dicatat      'YYYY-MM-DD HH:MM UTC' masa baris ditulis
  status       'aktif' (kuarantin dibuka) atau 'lepas' (dilepaskan; baris BAHARU, baris aktif tidak dipadam)
Lajur `status` ditambah kepada empat lajur asal supaya pelepasan boleh direkod tanpa menyunting baris lama.

Kesan kuarantin aktif (standard/harga_yf.py gabung, dipanggil `lejar.py stor`):
  - bar stor ticker itu TIDAK ditimpa dan bar baharu TIDAK ditambah (stor dibekukan);
  - ticker itu diminta muat turun SEJARAH PENUH (data/harga/perlu_sejarah.txt -> `harga_yf.py sejarah`, 3 tahun);
  - apabila sejarah segar tiba, ia dibanding dengan bar stor yang DIPERCAYAI (< tarikh_mula): jika nisbahnya seragam DAN
    bar segar >= tarikh_mula tidak berkongsi volum harian dengan ticker lain dalam stor (cap jari data syarikat lain: siri
    vendor yang disambung — 7 Nov 2026 yfinance masih menyajikan bar INDV di bawah SUPN bagi akhir Okt)
    (harga_yf.semak_kuarantin), bar >= tarikh_mula diganti dengan bar segar, bar dipercayai dilaras dengan nisbah itu, dan
    kuarantin DILEPASKAN (baris 'lepas'). Selainnya stor kekal beku dan kuarantin kekal aktif — keputusan manusia
    (`lepas` CLI) jika vendor terus menyajikan data itu.
  Ticker yang sudah tiada dalam direktori Nasdaq (delist, cth. INDV) tidak diminta muat turun semula: tiada data segar.

Untuk statistik: selang tercemar = [tarikh_mula, tarikh dilepaskan] (inklusif; terbuka jika masih aktif). Selang itu
KEKAL selepas pelepasan, kerana bar stor dibaiki tetapi baris Lejar/Papertrade C yang dikira semasa tercemar tidak.
Modul lain:  import kuarantin as KR;  KR.dikuarantin('SUPN', '2026-10-25') -> True;
             KR.tercemar('SUPN', tarikh_beli, tarikh_keluar) -> True jika tempoh pegangan menyentuh selang tercemar;
             KR.topeng(df, 'saham', 'tarikh_beli') / KR.topeng_posisi(df) -> Series bool untuk dikecualikan.

PEMBAIKAN SEMASA (subarahan `baiki`, boleh dijalankan semula; idempoten): SUPN dari 2026-10-21 dan INDV dari 2026-11-03
(delist) ditambah, dan SUPN diminta sejarah penuh. Skrip ini TIDAK menulis semula stor harga, Lejar atau Papertrade C:
  - bar SUPN dalam stor (data/harga/stor/harga_B.csv) mesti dimuat turun semula SEPENUHNYA oleh larian Actions seterusnya
    (harian.yml / harga_harian.yml: `harga_yf.py sejarah`, kemudian `lejar.py stor` membuat semakan konsisten dan
    melepaskan kuarantin jika lulus);
  - baris Lejar SUPN yang dilaras 0.64–0.66 dan posisi C INDV M19 (faktor palsu) kekal tercemar sehingga keputusan
    pengguna (bina semula Lejar / betulkan posisi C); `laporan` menyenaraikannya.

  python3 standard/kuarantin.py senarai
  python3 standard/kuarantin.py baiki [--kering]
  python3 standard/kuarantin.py tambah --ticker T --mula YYYY-MM-DD --sebab "..."
  python3 standard/kuarantin.py lepas  --ticker T --sebab "..."          # keputusan manusia sahaja
  python3 standard/kuarantin.py laporan                                   # baris Lejar / C dalam selang tercemar
"""
import argparse, csv, glob, json, os, sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
HARGA = os.path.join(BS2, 'data', 'harga')
FAIL = os.environ.get('KUARANTIN_FAIL', os.path.join(HARGA, 'kuarantin.csv'))
PERLU = os.path.join(HARGA, 'perlu_sejarah.txt')
BURSA = os.path.join(BS2, 'data', 'senarai_bursa')
PERISTIWA_BURSA = os.path.join(BURSA, 'peristiwa.csv')
SEMASA_BURSA = os.path.join(BURSA, 'semasa.csv')
LAJUR = ['ticker', 'tarikh_mula', 'sebab', 'dicatat', 'status']
JENIS_BURSA = ('tukar_nama', 'buang')     # peristiwa direktori yang menandakan simbol mungkin bertukar pemilik data

# Pembaikan semasa (7 Nov 2026). Bukti disemak semula oleh `baiki` daripada stor (baca sahaja).
BAIKI = [
    dict(ticker='SUPN', tarikh_mula='2026-10-21',
         sebab='tercemar: bar SUPN 2026-10-21..2026-11-02 = bar INDV x 0.775910 dengan volum sama (data INDV di bawah '
               'simbol SUPN); direktori Nasdaq 2026-11-03 SUPN tukar_nama + INDV buang; log_laras 2026-11-04 05:45 '
               'anomali 0.846397 tetapi bar ditimpa (gabung_satu); faktor dividen_khas 2026-11-03 x0.775910 kembar '
               'dengan INDV didarab pada 388 bar'),
    dict(ticker='INDV', tarikh_mula='2026-11-03',
         sebab='delist 2026-11-03 (direktori Nasdaq buang; ambil alih EDGAR 425 umum 2026-10-29); faktor dividen_khas '
               '2026-11-03 x0.775910 kembar dengan SUPN TIDAK SAH (dividen INDV disajikan di bawah dua simbol) — '
               'posisi C INDV yang dilaras faktor itu menunjukkan untung palsu'),
]


def kini():
    return pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M UTC')


def tarikh_teks(x):
    """'YYYY-MM-DD' daripada int YYYYMMDD (termasuk numpy), teks atau Timestamp."""
    s = str(x).strip()
    if s.isdigit() and len(s) == 8:
        return f'{s[:4]}-{s[4:6]}-{s[6:]}'
    return str(pd.Timestamp(s).date())


def tarikh_int(x):
    return int(tarikh_teks(x).replace('-', ''))


# ---------------------------------------------------------------- fail kuarantin
def muat(path=None):
    """Semua baris (DataFrame LAJUR, teks). Fail tiada -> kosong."""
    path = path or FAIL
    if not os.path.exists(path):
        return pd.DataFrame(columns=LAJUR)
    d = pd.read_csv(path, dtype=str, keep_default_na=False).reindex(columns=LAJUR, fill_value='')
    d['status'] = d.status.str.strip().str.lower().replace('', 'aktif')
    return d[d.ticker.str.strip() != ''].reset_index(drop=True)


def _rekod(x):
    return muat(x) if x is None or isinstance(x, str) else x


def keadaan(x=None):
    """{(ticker, tarikh_mula): (status terakhir, dicatat baris terakhir)} mengikut susunan fail."""
    out = {}
    for r in _rekod(x).itertuples():
        out[(r.ticker, r.tarikh_mula)] = (r.status, r.dicatat)
    return out


def aktif(x=None):
    """{ticker: tarikh_mula paling awal yang masih aktif}."""
    out = {}
    for (t, m), (s, _) in keadaan(x).items():
        if s == 'aktif' and (t not in out or m < out[t]):
            out[t] = m
    return out


def selang(x=None):
    """{ticker: [(mula, tamat atau None)]}: tamat = tarikh baris 'lepas' (inklusif); None = masih aktif."""
    out = {}
    for (t, m), (s, d) in keadaan(x).items():
        out.setdefault(t, []).append((m, d[:10] if s == 'lepas' else None))
    return out


def ditangani(x, ticker, tarikh):
    """True jika ada baris (apa-apa status) bagi ticker yang dicatat PADA/SELEPAS `tarikh` — isyarat bertarikh itu sudah
    dikendalikan (kuarantin dibuka selepas isyarat), jadi pengawal tidak membuka kuarantin baharu bagi isyarat sama."""
    d = _rekod(x)
    if not len(d):
        return False
    t = tarikh_teks(tarikh)
    return bool(((d.ticker == ticker) & (d.dicatat.str[:10] >= t)).any())


def _tulis(path, rows):
    if not rows:
        return
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    baru = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, LAJUR)
        if baru:
            w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in LAJUR})
    _CACHE.clear()


def tambah(ticker, tarikh_mula, sebab, path=None, dicatat=None):
    """Buka kuarantin (ticker, tarikh_mula). Idempoten: pasangan yang sudah wujud (aktif ATAU dilepaskan) tidak ditambah
    semula. Pulang True jika baris ditulis."""
    path = path or FAIL
    m = tarikh_teks(tarikh_mula)
    if (ticker, m) in keadaan(path):
        return False
    _tulis(path, [dict(ticker=ticker, tarikh_mula=m, sebab=sebab, dicatat=dicatat or kini(), status='aktif')])
    return True


def lepas(ticker, sebab, path=None, dicatat=None):
    """Lepaskan SEMUA kuarantin aktif ticker (baris 'lepas' baharu). Pulang senarai tarikh_mula yang dilepaskan."""
    path = path or FAIL
    m = sorted(mm for (t, mm), (s, _) in keadaan(path).items() if t == ticker and s == 'aktif')
    _tulis(path, [dict(ticker=ticker, tarikh_mula=x, sebab=sebab, dicatat=dicatat or kini(), status='lepas') for x in m])
    return m


# ---------------------------------------------------------------- pertanyaan statistik
_CACHE = {}


def _selang_cache(path=None):
    path = path or FAIL
    try:
        s = os.stat(path); kunci = (path, s.st_mtime_ns, s.st_size)
    except OSError:
        kunci = (path, None, None)
    if _CACHE.get('kunci') != kunci:
        _CACHE.clear(); _CACHE.update(kunci=kunci, selang=selang(path))
    return _CACHE['selang']


def dikuarantin(ticker, tarikh, path=None):
    """True jika bar/dagangan `ticker` pada `tarikh` jatuh dalam selang tercemar (aktif atau sudah dilepaskan)."""
    d = tarikh_teks(tarikh)
    return any(m <= d and (e is None or d <= e) for m, e in _selang_cache(path).get(str(ticker), ()))


def tercemar(ticker, mula, tamat=None, path=None):
    """True jika tempoh pegangan [mula, tamat] (tamat kosong = masih dipegang) menyentuh selang tercemar ticker."""
    a = tarikh_teks(mula)
    b = tarikh_teks(tamat) if tamat not in (None, '') and not (isinstance(tamat, float) and pd.isna(tamat)) else None
    for m, e in _selang_cache(path).get(str(ticker), ()):
        if (b is None or m <= b) and (e is None or a <= e):
            return True
    return False


def topeng(df, lajur_saham='saham', lajur_tarikh='tarikh_beli', path=None):
    """Series bool (indeks df): baris yang ticker-tarikhnya dikuarantin."""
    s = _selang_cache(path)
    if not s or not len(df):
        return pd.Series(False, index=df.index)
    return pd.Series([str(t) in s and dikuarantin(t, d, path) if str(d) not in ('', 'nan', 'None') else False
                      for t, d in zip(df[lajur_saham], df[lajur_tarikh])], index=df.index)


def topeng_posisi(df, lajur_saham='saham', mula='tarikh_beli', tamat='tarikh_keluar', path=None):
    """Series bool: posisi yang tempoh pegangannya menyentuh selang tercemar (tamat kosong = masih dipegang)."""
    s = _selang_cache(path)
    if not s or not len(df):
        return pd.Series(False, index=df.index)
    tm = df[tamat] if tamat in df else pd.Series('', index=df.index)
    return pd.Series([str(t) in s and str(a) not in ('', 'nan') and tercemar(t, a, b if str(b) not in ('', 'nan') else None, path)
                      for t, a, b in zip(df[lajur_saham], df[mula], tm)], index=df.index)


# ---------------------------------------------------------------- direktori Nasdaq dan permintaan sejarah
def peristiwa_bursa(path=None, jenis=JENIS_BURSA):
    """{simbol: [(tarikh int, peristiwa)]} bagi peristiwa direktori `jenis` (lalai tukar_nama / buang)."""
    path = path or PERISTIWA_BURSA
    if not os.path.exists(path):
        return {}
    p = pd.read_csv(path, dtype=str, keep_default_na=False, usecols=['tarikh', 'simbol', 'peristiwa'])
    p = p[p.peristiwa.isin(jenis)]
    out = {}
    for r in p.itertuples():
        out.setdefault(r.simbol, []).append((tarikh_int(r.tarikh), r.peristiwa))
    return {t: sorted(v) for t, v in out.items()}


def peristiwa_dalam(ev, d0, d1):
    """Peristiwa pertama (tarikh int, jenis) dalam [d0, d1] (int YYYYMMDD), atau None."""
    for x in ev or ():
        if int(d0) <= x[0] <= int(d1):
            return x
    return None


def tersenarai(path=None):
    """Set simbol dalam direktori semasa, atau None jika fail tiada (tidak diketahui)."""
    path = path or SEMASA_BURSA
    if not os.path.exists(path):
        return None
    return set(pd.read_csv(path, dtype=str, keep_default_na=False, usecols=['simbol']).simbol)


def perlu_muat_semula(x=None, semasa=None):
    """Ticker kuarantin aktif yang masih tersenarai (sejarah penuh boleh dimuat turun). semasa None -> semua aktif."""
    a = aktif(x)
    s = tersenarai() if semasa is None else semasa
    return sorted(t for t in a if s is None or t in s)


def minta_sejarah(tickers, path=None):
    """Tambah ticker ke perlu_sejarah.txt (kesatuan dengan isi sedia ada). Pulang ticker yang baru ditambah."""
    path = path or PERLU
    if not tickers:
        return []
    lama = set()
    if os.path.exists(path):
        with open(path) as f:
            lama = {x.strip() for x in f if x.strip()}
    baru = sorted(set(tickers) - lama)
    if baru:
        with open(path, 'w') as f:
            f.write('\n'.join(sorted(lama | set(tickers))) + '\n')
    return baru


# ---------------------------------------------------------------- CLI
def bukti_supn_indv(stor=None):
    """Semakan baca-sahaja: nisbah tutup SUPN/INDV dan volum sama, 2026-10-21..2026-11-02, dalam stor."""
    stor = stor or os.path.join(HARGA, 'stor')
    fr = [pd.read_csv(os.path.join(stor, f)) for f in ('harga_A.csv', 'harga_B.csv') if os.path.exists(os.path.join(stor, f))]
    if not fr:
        return dict(ralat='stor tiada')
    d = pd.concat(fr, ignore_index=True)
    d = d[(d.date >= 20261021) & (d.date <= 20261102)]
    m = d[d.ticker == 'SUPN'].merge(d[d.ticker == 'INDV'], on='date', suffixes=('_s', '_i'))
    if not len(m):
        return dict(bar=0)
    r = m.close_s / m.close_i
    return dict(bar=int(len(m)), nisbah_min=round(float(r.min()), 6), nisbah_maks=round(float(r.max()), 6),
                volum_sama=int((m.volume_s == m.volume_i).sum()))


def _baris_posisi(lejar_dir, papertrade):
    """Semua posisi Lejar (terbuka + tutup) dan Papertrade C sebagai DataFrame teks dengan lajur `sumber_fail`."""
    out = []
    fs = [os.path.join(lejar_dir, 'terbuka.csv')] + sorted(glob.glob(os.path.join(lejar_dir, 'tutup', '*.csv')))
    for f in fs:
        if os.path.exists(f):
            x = pd.read_csv(f, dtype=str, keep_default_na=False)
            out.append(x.assign(sumber_fail=os.path.relpath(f, BS2), kaedah=x['id_kaedah'] if 'id_kaedah' in x else ''))
    for f in sorted(glob.glob(os.path.join(papertrade, 'claude*.csv'))):
        x = pd.read_csv(f, dtype=str, keep_default_na=False)
        for c in ('tidak_dibeli', 'harga_beli'):
            if c not in x:
                x[c] = ''
        x = x[(x.tidak_dibeli != 'True') & (x.harga_beli != '')]
        out.append(x.assign(sumber_fail=os.path.relpath(f, BS2)))
    if not out:
        return pd.DataFrame(columns=['saham', 'tarikh_beli', 'tarikh_keluar', 'sumber_fail'])
    return pd.concat(out, ignore_index=True).fillna('')


def laporan(path=None, lejar_dir=None, papertrade=None):
    """Posisi Lejar / C yang tempoh pegangannya menyentuh selang tercemar (baca sahaja)."""
    lejar_dir = lejar_dir or os.path.join(BS2, 'lejar')
    papertrade = papertrade or os.path.join(BS2, 'papertrade')
    s = selang(path)
    P = _baris_posisi(lejar_dir, papertrade)
    P = P[P.saham.isin(s)]
    if len(P):
        kosong = pd.Series('', index=P.index)
        tamat = [max(a, b) if a and b else (a or b) for a, b in
                 zip(P['tarikh_keluar'] if 'tarikh_keluar' in P else kosong,
                     P['tarikh_keluar_henti'] if 'tarikh_keluar_henti' in P else kosong)]
        P = P.assign(_tamat=tamat)
        P = P[[tercemar(t, a, b or None, path) for t, a, b in zip(P.saham, P.tarikh_beli, P._tamat)]]
    out = dict(selang={t: [list(x) for x in v] for t, v in s.items()}, posisi=int(len(P)))
    if len(P):
        out['ikut_fail'] = {f: int(n) for f, n in P.groupby('sumber_fail').size().items()}
        out['ikut_saham'] = {t: int(n) for t, n in P.groupby('saham').size().items()}
        if 'laras' in P:
            lr = pd.to_numeric(P.laras, errors='coerce').dropna()
            out['lejar_dilaras'] = int(len(lr))
        out['faktor_dalam_nota'] = sorted({f"{r.sumber_fail} {r.saham} {r.kaedah} {r.tarikh_beli}"
                                           for r in P.itertuples() if 'faktor ' in str(getattr(r, 'nota', ''))})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description='Kuarantin data harga tercemar (data/harga/kuarantin.csv)')
    ap.add_argument('--fail', default=None, help='laluan kuarantin.csv (lalai data/harga/kuarantin.csv)')
    sp = ap.add_subparsers(dest='cmd', required=True)
    sp.add_parser('senarai')
    b = sp.add_parser('baiki'); b.add_argument('--kering', action='store_true', help='cetak sahaja, tiada tulis')
    b.add_argument('--perlu', default=None, help='laluan perlu_sejarah.txt (lalai data/harga/perlu_sejarah.txt)')
    t = sp.add_parser('tambah'); t.add_argument('--ticker', required=True); t.add_argument('--mula', required=True)
    t.add_argument('--sebab', required=True)
    x = sp.add_parser('lepas'); x.add_argument('--ticker', required=True); x.add_argument('--sebab', required=True)
    sp.add_parser('laporan')
    a = ap.parse_args(argv)
    path = a.fail or FAIL
    if a.cmd == 'senarai':
        d = muat(path)
        print(d.to_csv(index=False), end='')
        print(json.dumps(dict(aktif=aktif(d)), ensure_ascii=False), file=sys.stderr)
    elif a.cmd == 'baiki':
        bukti = bukti_supn_indv()
        if a.kering:
            print(json.dumps(dict(akan_ditambah=[(r['ticker'], r['tarikh_mula']) for r in BAIKI
                                                  if (r['ticker'], r['tarikh_mula']) not in keadaan(path)],
                                  bukti_stor=bukti), ensure_ascii=False, indent=1))
            return 0
        ditambah = [(r['ticker'], r['tarikh_mula']) for r in BAIKI if tambah(r['ticker'], r['tarikh_mula'], r['sebab'], path)]
        diminta = minta_sejarah(perlu_muat_semula(path), a.perlu)
        print(json.dumps(dict(ditambah=ditambah, aktif=aktif(path), sejarah_diminta=diminta, bukti_stor=bukti,
                              nota='stor/Lejar/Papertrade C TIDAK ditulis; sejarah penuh dimuat turun oleh Actions seterusnya'),
                         ensure_ascii=False, indent=1))
    elif a.cmd == 'tambah':
        ok = tambah(a.ticker, a.mula, a.sebab, path)
        diminta = minta_sejarah(perlu_muat_semula(path)) if ok else []
        print(json.dumps(dict(ditambah=ok, sejarah_diminta=diminta), ensure_ascii=False))
    elif a.cmd == 'lepas':
        print(json.dumps(dict(dilepaskan=lepas(a.ticker, a.sebab, path)), ensure_ascii=False))
    elif a.cmd == 'laporan':
        print(json.dumps(laporan(path), ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
