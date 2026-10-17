"""Senarai calon AUTOTUNE (SPEC §1): saham biasa NASDAQ/NYSE/AMEX + ticker dataset_S1-S4 -> calon.txt."""
import argparse
import io
import re
import sys
import urllib.request
from pathlib import Path

import pandas as pd

URL_N = 'https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt'
URL_O = 'https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt'
AKAR = Path(__file__).resolve().parents[2]

# Nama yang bukan saham biasa. ADR ("American Depositary Shares") dikekalkan; dana tertutup (Fund) dibuang.
BUANG_NAMA = re.compile(
    r'\bwarrants?\b|\bunits?\b|\brights?\b|\bpreferred\b|\bpreference\b|\bnotes?\b|\bdebentures?\b|'
    r'\bsubordinated\b|acquisition corp|\bfund\b|\betn\b|\bdue \d{4}\b|\bbeneficial interest\b', re.I)
SAH_SIMBOL = re.compile(r'^[A-Z0-9]{1,6}(-[A-Z]{1,2})?$')


def ambil_teks(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode('utf-8', 'replace')


def baca_simbol(teks):
    """Jadual pipe-delimited SymDir tanpa baris 'File Creation Time'."""
    baris = [b for b in teks.splitlines() if b.strip() and not b.startswith('File Creation Time')]
    return pd.read_csv(io.StringIO('\n'.join(baris)), sep='|', dtype=str, keep_default_na=False)


def yahoo(sim):
    """Bentuk Yahoo: '.'->'-'. None jika mengandungi '$' atau aksara pelik."""
    s = sim.strip().upper()
    if '$' in s or not s:
        return None
    s = s.replace('.', '-')
    return s if SAH_SIMBOL.match(s) else None


def tapis(df, kol_sim, kol_etf, kol_uji, kol_nama='Security Name'):
    """Pulangkan senarai simbol Yahoo saham biasa daripada satu jadual SymDir."""
    m = (df[kol_etf].str.upper() != 'Y') & (df[kol_uji].str.upper() != 'Y')
    m &= ~df[kol_nama].str.contains(BUANG_NAMA, na=False)
    out = []
    for s in df.loc[m, kol_sim]:
        y = yahoo(s)
        if y:
            out.append(y)
    return out


def calon_senarai(teks_n, teks_o, akar=AKAR):
    n = baca_simbol(teks_n)
    o = baca_simbol(teks_o)
    sim = tapis(n, 'Symbol', 'ETF', 'Test Issue')
    sim += tapis(o, 'ACT Symbol', 'ETF', 'Test Issue')
    ds = set()
    for f in sorted((akar / 'data_mentah').glob('dataset_S*.csv')):
        ds |= set(pd.read_csv(f, usecols=['ticker'], dtype=str).ticker.dropna().str.strip().str.upper()
                  .str.replace('.', '-', regex=False))
    return sorted(set(sim) | ds), len(set(sim)), len(ds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--keluar', default=str(Path(__file__).parent / 'calon.txt'))
    a = ap.parse_args()
    cal, ns, nd = calon_senarai(ambil_teks(URL_N), ambil_teks(URL_O))
    Path(a.keluar).write_text('\n'.join(cal) + '\n')
    print(f'calon={len(cal)} (saham biasa SymDir={ns}, dataset={nd}) -> {a.keluar}')
    if len(cal) < 3000:
        sys.exit('terlalu sedikit calon; semak sumber')


if __name__ == '__main__':
    main()
