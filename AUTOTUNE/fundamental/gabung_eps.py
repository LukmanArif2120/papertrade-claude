"""AUTOTUNE A03 §1: gabung shard EPS -> eps_a03.parquet + manifest + LIPUTAN.md.

eps_a03.parquet (satu baris setiap ticker + suku, tersusun ticker, tarikh_laporan):
  ticker, tarikh_laporan (America/New_York), tarikh (tarikh laporan, tanpa zon), masa, eps_sebenar, eps_anggaran, sumber,
  tersedia (hari dagangan pertama angka boleh digunakan), eps_yoy, eps_yoy_sebelum.
Titik masa: 'sebelum' -> hari dagangan pertama >= tarikh (hari yang sama jika hari dagangan); selainnya ('selepas',
'tidak diketahui') -> hari dagangan pertama > tarikh. Hari dagangan = tarikh bar SPY dalam idx.parquet Release A02.
eps_yoy = (eps - eps empat suku lalu) / eps empat suku lalu, hanya jika eps itu > 0 DAN jarak tarikh ~1 tahun (300-430 hari).
Guna: python3 AUTOTUNE/fundamental/gabung_eps.py --masuk shards --universe universe.parquet --idx idx.parquet --keluar keluar
"""
import argparse
import glob
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

NY = 'America/New_York'
AKAR = Path(__file__).resolve().parents[2]
RUMPUN_HARI = 40            # laporan dalam tempoh ini selepas laporan terdahulu dianggap pendua suku sama
USIA_MAKS = 135             # suku terkini dianggap "boleh guna" jika dilaporkan <= 135 hari sebelum
JARAK_TAHUN = (300, 430)    # jarak hari dibenarkan antara suku dan suku empat kedudukan lalu
JARAK_SUKU = (50, 140)      # jarak hari dibenarkan antara suku dan suku sebelumnya (eps_yoy_sebelum)
TAHUN_LIPUTAN = range(2010, 2027)


def hari_dagangan(idx):
    """Array datetime64[D] tersusun hari dagangan SPY daripada DataFrame idx (lajur ticker, date)."""
    d = idx[idx['ticker'] == 'SPY']['date']
    return np.sort(pd.DatetimeIndex(d).normalize().unique().values).astype('datetime64[D]')


def hitung_tersedia(tarikh, masa, hari):
    """Hari dagangan pertama angka boleh digunakan. NaT jika melepasi hari dagangan terakhir yang diketahui."""
    t = pd.DatetimeIndex(tarikh).values.astype('datetime64[D]')
    sebelum = np.asarray(masa) == 'sebelum'
    kiri = np.searchsorted(hari, t, side='left')     # hari >= tarikh
    kanan = np.searchsorted(hari, t, side='right')   # hari > tarikh
    pos = np.where(sebelum, kiri, kanan)
    ok = pos < len(hari)
    out = np.full(len(t), np.datetime64('NaT', 'ns'), dtype='datetime64[ns]')
    out[ok] = hari[pos[ok]].astype('datetime64[ns]')
    return pd.DatetimeIndex(out)


def nyahpendua(d):
    """Satu baris setiap suku: laporan dalam RUMPUN_HARI selepas baris yang dikekalkan (ticker sama) dibuang;
    baris terawal dikekalkan (selamat titik-masa). d tersusun ticker, tarikh_laporan."""
    kekal = np.ones(len(d), bool)
    tick = d['ticker'].to_numpy()
    tgl = pd.DatetimeIndex(d['tarikh']).values.astype('datetime64[D]').astype('int64')
    akhir_t, akhir_tgl = None, 0
    for i in range(len(d)):
        if tick[i] == akhir_t and tgl[i] - akhir_tgl <= RUMPUN_HARI:
            kekal[i] = False
        else:
            akhir_t, akhir_tgl = tick[i], tgl[i]
    return d[kekal]


def tambah_yoy(d):
    """Tambah eps_yoy dan eps_yoy_sebelum (d tersusun ticker, tarikh; satu baris setiap suku)."""
    eps = d['eps_sebenar'].to_numpy(float)
    tgl = pd.DatetimeIndex(d['tarikh']).values.astype('datetime64[D]').astype('int64')
    tick = d['ticker'].to_numpy()
    n = len(d)
    yoy = np.full(n, np.nan)
    sebelum = np.full(n, np.nan)
    if n > 4:
        lalu, jarak = eps[:-4], tgl[4:] - tgl[:-4]
        ok = (tick[4:] == tick[:-4]) & (lalu > 0) & (jarak >= JARAK_TAHUN[0]) & (jarak <= JARAK_TAHUN[1])
        yoy[4:][ok] = (eps[4:][ok] - lalu[ok]) / lalu[ok]
    if n > 1:
        jarak = tgl[1:] - tgl[:-1]
        ok = (tick[1:] == tick[:-1]) & (jarak >= JARAK_SUKU[0]) & (jarak <= JARAK_SUKU[1])
        sebelum[1:][ok] = yoy[:-1][ok]
    out = d.copy()
    out['eps_yoy'] = yoy
    out['eps_yoy_sebelum'] = sebelum
    return out


def bina(mentah, hari):
    """mentah: DataFrame lajur ticker, tarikh_laporan (ISO), masa, eps_sebenar, eps_anggaran, sumber -> jadual akhir."""
    d = mentah.copy()
    d['tarikh_laporan'] = pd.to_datetime(d['tarikh_laporan'], utc=True).dt.tz_convert(NY)
    d['tarikh'] = d['tarikh_laporan'].dt.tz_localize(None).dt.normalize()
    d['eps_sebenar'] = pd.to_numeric(d['eps_sebenar'], errors='coerce')
    d['eps_anggaran'] = pd.to_numeric(d['eps_anggaran'], errors='coerce')
    d = d[d['eps_sebenar'].notna()]
    d = d.sort_values(['ticker', 'tarikh_laporan', 'sumber']).drop_duplicates(['ticker', 'tarikh_laporan'])
    d = nyahpendua(d.reset_index(drop=True)).reset_index(drop=True)
    d = tambah_yoy(d)
    d['tersedia'] = hitung_tersedia(d['tarikh'], d['masa'], hari)
    return d[['ticker', 'tarikh_laporan', 'tarikh', 'masa', 'eps_sebenar', 'eps_anggaran', 'sumber',
              'tersedia', 'eps_yoy', 'eps_yoy_sebelum']]


def baca_shard(masuk):
    fail = sorted(glob.glob(str(Path(masuk) / '**' / 'eps_shard_*.csv'), recursive=True))
    if not fail:
        raise SystemExit(f'tiada eps_shard_*.csv di {masuk}')
    mentah = pd.concat([pd.read_csv(f, dtype={'ticker': str, 'masa': str, 'sumber': str}) for f in fail], ignore_index=True)
    gagal = []
    for f in sorted(glob.glob(str(Path(masuk) / '**' / 'gagal_*.txt'), recursive=True)):
        gagal += [x for x in Path(f).read_text().splitlines() if x and not x.startswith('#')]
    return mentah, gagal, len(fail)


def liputan(eps, univ, hari, ambang=0.25):
    """DataFrame per tahun: peratus baris (ticker-bulan) universe dengan suku terkini boleh guna pada hari dagangan
    terakhir bulan itu (tersedia <= hari itu, dilaporkan <= USIA_MAKS hari sebelum)."""
    u = univ[['bulan', 'ticker', 'kumpulan']].copy()
    awal = pd.to_datetime(u['bulan'] + '-01')
    hari_idx = pd.DatetimeIndex(hari.astype('datetime64[ns]'))
    u = u[awal <= hari_idx[-1]].copy()
    bln = pd.PeriodIndex(u['bulan'], freq='M')
    akhir_bulan = pd.Series(hari_idx, index=hari_idx).groupby(hari_idx.to_period('M')).max()
    u['nilai'] = akhir_bulan.reindex(bln).to_numpy()
    u = u[u['nilai'].notna()].sort_values('nilai').reset_index(drop=True)
    e = eps[eps['tersedia'].notna()][['ticker', 'tersedia', 'tarikh', 'eps_sebenar', 'eps_yoy']].sort_values('tersedia')
    m = pd.merge_asof(u, e, left_on='nilai', right_on='tersedia', by='ticker', direction='backward')
    usia = (m['nilai'] - m['tarikh']).dt.days
    m['ada'] = m['tarikh'].notna() & (usia <= USIA_MAKS)
    m['yoy'] = m['ada'] & m['eps_yoy'].notna()
    m['f'] = m['yoy'] & (m['eps_sebenar'] > 0) & (m['eps_yoy'] >= ambang)
    m['tahun'] = m['nilai'].dt.year
    return m


def ringkas_liputan(m):
    g = m.groupby('tahun')
    r = pd.DataFrame({'baris': g.size(), 'ada': g['ada'].mean() * 100, 'yoy': g['yoy'].mean() * 100, 'f': g['f'].mean() * 100})
    r['ada_A'] = m[m['kumpulan'] == 'A'].groupby('tahun')['ada'].mean() * 100
    r['ada_B'] = m[m['kumpulan'] == 'B'].groupby('tahun')['ada'].mean() * 100
    return r.reindex([y for y in TAHUN_LIPUTAN if y in r.index])


def tulis_liputan(laluan, eps, univ, m, gagal, n_shard, tarikan):
    r = ringkas_liputan(m)
    tick_univ = set(univ['ticker'])
    tick_eps = set(eps['ticker'])
    tiada = sorted(tick_univ - tick_eps)
    rendah = [int(y) for y in r.index if 2013 <= y <= 2018 and r.loc[y, 'ada'] < 70]
    jenis = {}
    for x in gagal:
        p = x.split('\t')
        k = (p[1] if len(p) > 1 else '?').split(':')[0]
        ganti = p[2].replace('ganti=', '') if len(p) > 2 else '?'
        jenis[(k, ganti)] = jenis.get((k, ganti), 0) + 1
    L = ['# Liputan EPS A03 (Yahoo `get_earnings_dates`)', '',
         f'Dijana {tarikan}. Shard {n_shard}. Spesifikasi: `AUTOTUNE/SPEC_A03.md` §1.', '',
         '## Ringkasan',
         f'- Ticker universe A02: {len(tick_univ)}; ticker dengan sekurang-kurangnya satu EPS: {len(tick_eps)} '
         f'({100 * len(tick_eps) / max(len(tick_univ), 1):.1f}%); tanpa EPS: {len(tiada)}.',
         f'- Baris suku (selepas nyahpendua): {len(eps)}; sumber yahoo {int((eps["sumber"] == "yahoo").sum())}, '
         f'repo (benih eps.csv) {int((eps["sumber"] == "repo").sum())}; laporan {eps["tarikh"].min().date()} hingga {eps["tarikh"].max().date()}.',
         f'- Masa: ' + ', '.join(f'{k} {v}' for k, v in eps['masa'].value_counts().items()) + '.',
         f'- eps_yoy sah (EPS suku lalu > 0 dan jarak ~1 tahun): {int(eps["eps_yoy"].notna().sum())} baris.',
         '', '## Liputan setiap tahun',
         f'Peratus baris ticker-bulan universe pada hari dagangan terakhir bulan yang suku terkininya tersedia (titik masa) '
         f'dan dilaporkan <= {USIA_MAKS} hari sebelum ("ada"); "yoy" = ada dan eps_yoy sah; "F" = yoy dan EPS > 0 dan yoy >= 25%.', '',
         '| Tahun | Baris | ada % | ada A % | ada B % | yoy % | F % |', '|---|---|---|---|---|---|---|']
    for y, x in r.iterrows():
        L.append(f'| {y} | {int(x.baris)} | {x.ada:.1f} | {x.ada_A:.1f} | {x.ada_B:.1f} | {x.yoy:.1f} | {x.f:.1f} |')
    L += ['', f'Tanda SPEC §1: liputan < 70% bagi tahun 2013-2018 -> **{"liputan rendah: " + ", ".join(map(str, rendah)) if rendah else "tiada (semua >= 70%)"}**.',
          '', '## Kegagalan',
          f'- Ticker gagal/kosong pada Yahoo: {len(gagal)}.']
    for (k, ganti), v in sorted(jenis.items(), key=lambda z: -z[1]):
        L.append(f'  - {k} (sumber ganti: {ganti}): {v}')
    L += [f'- Ticker universe tanpa sebarang EPS: {len(tiada)}' + (f'; contoh: {", ".join(tiada[:30])}' if tiada else '') + '.', '',
          '## Kaveat', '- EPS Yahoo ialah EPS dilaporkan/dilaras penganalisis, bukan GAAP; sejarah awal tidak lengkap; tiada saham delist.',
          '- Masa laporan 09:30-15:59 dan 00:00 = "tidak diketahui" (guna hari dagangan berikutnya).', '']
    Path(laluan).write_text('\n'.join(L))
    return r, tiada


def _sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def gabung(masuk, universe, idx, keluar, repo_dir):
    keluar, repo_dir = Path(keluar), Path(repo_dir)
    keluar.mkdir(parents=True, exist_ok=True)
    repo_dir.mkdir(parents=True, exist_ok=True)
    mentah, gagal, n_shard = baca_shard(masuk)
    univ = pd.read_parquet(universe)
    hari = hari_dagangan(pd.read_parquet(idx, columns=['ticker', 'date']))
    eps = bina(mentah, hari)
    p = keluar / 'eps_a03.parquet'
    eps.to_parquet(p, index=False)
    tarikan = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    m = liputan(eps, univ, hari)
    r, tiada = tulis_liputan(repo_dir / 'LIPUTAN.md', eps, univ, m, gagal, n_shard, tarikan)
    manifest = {
        'tag': 'autotune-fundamental-a03', 'tarikan': tarikan, 'n_ticker_universe': int(univ['ticker'].nunique()),
        'n_ticker_eps': int(eps['ticker'].nunique()), 'n_baris': int(len(eps)),
        'tarikh_laporan_min': str(eps['tarikh'].min().date()), 'tarikh_laporan_maks': str(eps['tarikh'].max().date()),
        'hari_dagangan_akhir': str(hari[-1]), 'n_gagal': len(gagal), 'n_shard': n_shard,
        'liputan_ada_pct': {int(y): round(float(x), 1) for y, x in r['ada'].items()},
        'fail': [{'nama': p.name, 'bait': p.stat().st_size, 'sha256': _sha256(p)}],
    }
    (keluar / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    (repo_dir / 'manifest_a03.json').write_text(json.dumps(manifest, indent=1))
    print(json.dumps({k: v for k, v in manifest.items() if k not in ('fail', 'liputan_ada_pct')}))
    print(r.round(1).to_string())
    return eps, manifest


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--masuk', default='shards')
    ap.add_argument('--universe', default='universe.parquet')
    ap.add_argument('--idx', default='idx.parquet')
    ap.add_argument('--keluar', default='keluar')
    ap.add_argument('--repo-dir', default=str(AKAR / 'AUTOTUNE' / 'fundamental'))
    a = ap.parse_args(argv)
    gabung(a.masuk, a.universe, a.idx, a.keluar, a.repo_dir)
    return 0


if __name__ == '__main__':
    sys.exit(main())
