# senarai_bursa.py — petikan harian direktori simbol Nasdaq Trader (nasdaqlisted.txt + otherlisted.txt; 27 Okt 2026,
# senarai alat #74). Fail rasmi hanya memberi senarai SEMASA; dengan menyimpan perubahan setiap hari, sejarah
# point-in-time saham tersenarai terbina mulai hari ini (saham yang hilang = delist / tukar simbol) untuk universe
# backtest bebas bias survivorship. Sejarah sebelum hari ini: Alpha Vantage LISTING_STATUS (connector claude.ai).
# GitHub Actions `senarai_bursa.yml` sahaja (sesi Claude tidak boleh capai nasdaqtrader.com).
#
# Output (BacktestShariah2/data/senarai_bursa/):
#   semasa.csv     simbol, nama, bursa, etf, biasa, pertama_dilihat   (senarai terkini; Test Issue dibuang)
#   peristiwa.csv  tarikh, simbol, peristiwa (asas|tambah|buang|tukar_nama), nama, bursa, etf, biasa
#                  'asas' = senarai pada larian pertama (bukan penyenaraian baharu).
#   status.json    tarikh fail sumber, bilangan, larian terakhir
# biasa = 1 jika saham biasa/ADR (bukan ETF, waran, unit, hak, keutamaan, nota, dana, SPAC; peraturan
# AUTOTUNE/data/senarai_calon.py). Simbol gaya repo: kelas dengan '.' (BRK.B).
# Pengawal: jika senarai baharu < 80% daripada semasa (fail rosak/separa), tiada perubahan ditulis dan keluar 1.
#
#   python3 standard/senarai_bursa.py jalan [--n FAIL --o FAIL]   (fail tempatan untuk ujian; lalai = muat turun)
import argparse, io, json, os, re, sys
from datetime import datetime, timezone

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
OUT = os.path.join(BS2, 'data', 'senarai_bursa')
URL_N = 'https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt'
URL_O = 'https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt'
BURSA_O = {'A': 'NYSE American', 'N': 'NYSE', 'P': 'NYSE Arca', 'Z': 'Cboe BZX', 'V': 'IEX'}
BUANG_NAMA = re.compile(
    r'\bwarrants?\b|\bunits?\b|\brights?\b|\bpreferred\b|\bpreference\b|\bnotes?\b|\bdebentures?\b|'
    r'\bsubordinated\b|acquisition corp|\bfund\b|\betn\b|\bdue \d{4}\b|\bbeneficial interest\b', re.I)
LAJUR = ['simbol', 'nama', 'bursa', 'etf', 'biasa']
NISBAH_MIN = 0.8


def ambil_teks(url):
    import urllib.request
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (papertrade-claude)'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode('utf-8', 'replace')


# ---------------------------------------------------------------- penghurai (diuji tanpa rangkaian)
def hurai(teks):
    """Jadual SymDir (pipe) -> (DataFrame, masa fail 'File Creation Time' atau '')."""
    masa = ''
    baris = []
    for b in teks.splitlines():
        if b.startswith('File Creation Time'):
            masa = b.split(':', 1)[1].strip().strip('|').strip()
        elif b.strip():
            baris.append(b)
    if not baris:
        return pd.DataFrame(), masa
    return pd.read_csv(io.StringIO('\n'.join(baris)), sep='|', dtype=str, keep_default_na=False), masa


def senarai(teks_n, teks_o):
    """Dua fail SymDir -> (DataFrame LAJUR satu baris setiap simbol, [masa fail])."""
    n, mn = hurai(teks_n)
    o, mo = hurai(teks_o)
    bah = []
    if len(n):
        n = n[n['Test Issue'].str.upper() != 'Y']
        bah.append(pd.DataFrame(dict(simbol=n['Symbol'], nama=n['Security Name'], bursa='NASDAQ', etf=n['ETF'])))
    if len(o):
        o = o[o['Test Issue'].str.upper() != 'Y']
        bah.append(pd.DataFrame(dict(simbol=o['ACT Symbol'], nama=o['Security Name'],
                                     bursa=o['Exchange'].map(BURSA_O).fillna(o['Exchange']), etf=o['ETF'])))
    if not bah:
        return pd.DataFrame(columns=LAJUR), [mn, mo]
    d = pd.concat(bah, ignore_index=True)
    d['simbol'] = d.simbol.str.strip().str.upper()
    d = d[d.simbol.ne('') & ~d.simbol.str.contains(r'\$', regex=True)]
    d['etf'] = (d.etf.str.upper() == 'Y').astype(int)
    d['biasa'] = ((d.etf == 0) & ~d.nama.str.contains(BUANG_NAMA, na=False)).astype(int)
    return d.drop_duplicates('simbol')[LAJUR].sort_values('simbol').reset_index(drop=True), [mn, mo]


def banding(lama, baru, tarikh):
    """semasa lama vs senarai baharu -> (semasa baharu, DataFrame peristiwa)."""
    if lama.empty:
        sem = baru.assign(pertama_dilihat=tarikh)
        return sem, baru.assign(tarikh=tarikh, peristiwa='asas')
    l, b = lama.set_index('simbol'), baru.set_index('simbol')
    tambah = b.loc[b.index.difference(l.index)].reset_index().assign(tarikh=tarikh, peristiwa='tambah')
    buang = l.loc[l.index.difference(b.index)].reset_index()[['simbol'] + LAJUR[1:]].assign(tarikh=tarikh, peristiwa='buang')
    sama = b.index.intersection(l.index)
    tukar = b.loc[sama][b.loc[sama, 'nama'] != l.loc[sama, 'nama']].reset_index().assign(tarikh=tarikh, peristiwa='tukar_nama')
    pertama = l['pertama_dilihat'] if 'pertama_dilihat' in l else pd.Series(dtype=str)
    sem = b.reset_index()
    sem['pertama_dilihat'] = sem.simbol.map(pertama).fillna(tarikh)
    return sem, pd.concat([tambah, buang, tukar], ignore_index=True)


# ---------------------------------------------------------------- larian
def jalan(a):
    os.makedirs(OUT, exist_ok=True)
    teks_n = open(a.n).read() if a.n else ambil_teks(URL_N)
    teks_o = open(a.o).read() if a.o else ambil_teks(URL_O)
    baru, masa = senarai(teks_n, teks_o)
    p_sem, p_per, p_st = (os.path.join(OUT, f) for f in ('semasa.csv', 'peristiwa.csv', 'status.json'))
    lama = pd.read_csv(p_sem, dtype=str, keep_default_na=False) if os.path.exists(p_sem) else pd.DataFrame()
    if len(lama):
        lama[['etf', 'biasa']] = lama[['etf', 'biasa']].astype(int)
    if len(lama) and len(baru) < NISBAH_MIN * len(lama):
        print(json.dumps(dict(ralat=f'senarai baharu {len(baru)} < {NISBAH_MIN:.0%} daripada semasa {len(lama)}; tiada perubahan')))
        return 1
    tarikh = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    sem, per = banding(lama, baru, tarikh)
    sem[LAJUR + ['pertama_dilihat']].to_csv(p_sem, index=False)
    if len(per):
        per = per[['tarikh', 'simbol', 'peristiwa'] + LAJUR[1:]]
        lama_per = pd.read_csv(p_per, dtype=str, keep_default_na=False) if os.path.exists(p_per) else pd.DataFrame()
        pd.concat([lama_per, per.astype(str)], ignore_index=True).to_csv(p_per, index=False)
    kira = per.peristiwa.value_counts().to_dict() if len(per) else {}
    st = dict(larian=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), masa_fail=masa, simbol=len(sem),
              saham_biasa=int(sem.biasa.sum()), peristiwa=kira)
    json.dump(st, open(p_st, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(st, ensure_ascii=False))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('perintah', choices=['jalan'])
    ap.add_argument('--n', default='', help='fail nasdaqlisted.txt tempatan (ujian)')
    ap.add_argument('--o', default='', help='fail otherlisted.txt tempatan (ujian)')
    return jalan(ap.parse_args(argv))


if __name__ == '__main__':
    sys.exit(main())
