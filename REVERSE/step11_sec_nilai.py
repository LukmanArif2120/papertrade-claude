"""STEP 11 — penilaian leg SEC fasa 2 (SPEC_FASA2.md §5, §6, §9.3, §9.4).

Peringkat 4 workflow. Dijalankan SEKALI, selepas join (step10) dan liputan lengkap. Set signal,
sasaran, populasi, keluarga FDR dan ambang penerimaan semuanya dikunci dalam §9.4 sebelum skrip ini
pernah dijalankan.

Sasaran: `pul_henti2atr` — masuk buka esok + kos sisi, henti keras -2xATR14, ufuk 63 hari, kos
keluar. Formula sama dengan `step7_false.sedia_hadapan()` fasa 1. Bagi tahun yang ada
`.cache/hadapan_<tahun>.parquet`, nilai itu dibaca terus. Bagi tahun lain ia dikira di sini untuk
peristiwa sah SAHAJA (~14 ribu baris, bukan ~500 ribu hari-ticker) dan `--sahkan` membandingkan
kedua-dua laluan atas tahun bertindih supaya ia terbukti sama.

Guna:
  python3 REVERSE/step11_sec_nilai.py --sahkan 2025      (sahkan laluan ringkas = cache fasa 1)
  python3 REVERSE/step11_sec_nilai.py                    (penilaian penuh)
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR / 'REVERSE'))
from teras import data as D  # noqa: E402
from teras import stat as ST  # noqa: E402
from teras.kos import kos_sisi  # noqa: E402

CACHE = AKAR / 'REVERSE' / '.cache'
KELUAR = AKAR / 'REVERSE'
UFUK = 63                  # ufuk label fasa 1 (SPEC §2)
HENTI_ATR = 2.0            # henti keras fasa 1
LAJUR = ['sue', 'tumbuh_hasil', 'pecutan_hasil']
TINGKAP = 5                # hari dagangan: tingkap PEAD dan tingkap pra-earnings (§9.4)
BASI_MAKS = 120            # §9.6: lajur SEC lebih lama daripada ini = kosong (sama SELANG_MAKS step10)
KELUARGA = 'FASA2_SEC'
MIN_N = 200                # minimum baris untuk Spearman (sama seperti ujian_pangkat.py)
PECAHAN_KONSISTEN = 0.71   # §9.5: ceil(0.71 x 14) = 10, sama dengan §9.3 asal
MIN_TAHUN = 10             # §9.5: kurang daripada ini -> BELUM BOLEH DINILAI
AMBANG_TAHUN = 3000        # §9.7: ambang §4 dikenakan SETIAP TAHUN; tahun di bawahnya dikecualikan


def pulangan_dagang(th, ev):
    """`pul_henti2atr` bagi peristiwa sah tahun `th` sahaja. Formula sama step7_false.sedia_hadapan."""
    tick = sorted(ev.saham.unique())
    fr = D.muat_harga(tick, f'{th - 2}-06-01', '2026-10-16')
    # Tarikh peristiwa setiap ticker sebagai DatetimeIndex[ns]: sec_join.csv datang sebagai
    # datetime64[us] dan np.isin atas senarai Timestamp tidak memadan indeks harga [ns].
    perlu = {t: pd.DatetimeIndex(pd.to_datetime(g).values.astype('datetime64[ns]'))
             for t, g in ev.groupby('saham')['tarikh']}
    out = []
    for tk, g in fr.items():
        c, o = g['close'].to_numpy('float64'), g['open'].to_numpy('float64')
        tr = pd.concat([g['high'] - g['low'], (g['high'] - g['close'].shift(1)).abs(),
                        (g['low'] - g['close'].shift(1)).abs()], axis=1).max(axis=1)
        atr = tr.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean().to_numpy('float64')
        to = (g['close'] * g['volume']).rolling(20, min_periods=10).median().to_numpy('float64')
        idx = g.index
        for i in np.flatnonzero(idx.isin(perlu.get(tk, pd.DatetimeIndex([])))):
            if i + 1 >= c.size:
                continue
            ks = kos_sisi(to[i])
            masuk = o[i + 1] * (1 + ks)
            if not np.isfinite(masuk) or masuk <= 0:
                continue
            b = min(i + UFUK, c.size - 1)
            seg = c[i + 1:b + 1]
            if seg.size == 0 or not np.isfinite(seg).any():
                continue
            hs = masuk - HENTI_ATR * atr[i] if np.isfinite(atr[i]) else np.nan
            i_keluar, sebab = b, 'hujung_63'
            if np.isfinite(hs):
                hit = np.flatnonzero(seg <= hs)
                if hit.size:
                    i_keluar, sebab = min(i + 1 + int(hit[0]) + 1, c.size - 1), 'henti2atr'
            harga = (o[i_keluar] if sebab == 'henti2atr' else c[i_keluar]) * (1 - ks)
            out.append((tk, idx[i], float(harga / masuk - 1.0)))
    return pd.DataFrame(out, columns=['saham', 'tarikh', 'pul_henti2atr'])


def sasaran(th, ev):
    """Pulangan boleh didagangkan: cache fasa 1 jika ada, jika tidak kira laluan ringkas.

    Laluan ringkas dicache ke `.cache/pul_dagang_<th>.csv` supaya step11 boleh disambung jika ia
    gagal separuh jalan: pengiraan 8 tahun baharu (~80 ribu peristiwa) tidak perlu diulang."""
    f = CACHE / f'hadapan_{th}.parquet'
    if f.exists():
        h = pd.read_parquet(f, columns=['ticker', 'tarikh', 'pul_henti2atr'])
        return h.rename(columns={'ticker': 'saham'})
    c = CACHE / f'pul_dagang_{th}.csv'
    if c.exists():
        return pd.read_csv(c, parse_dates=['tarikh'])
    d = pulangan_dagang(th, ev)
    d.to_csv(c, index=False)
    print(f'  pulangan dagangan {th} dikira dan dicache: {len(d)} baris')
    return d


def hasil_label(th):
    """Label PADU/SUPER PADU/BIASA/GAGAL fasa 1 bagi peristiwa sah (step1 menulisnya dalam signals)."""
    s = pd.read_parquet(CACHE / f'signals_{th}.parquet',
                        columns=['ticker', 'tarikh', 'jenis_peristiwa', 'dalam_univ', 'hasil'])
    s = s[(s.jenis_peristiwa != '') & (s.dalam_univ == 1)]
    return s.rename(columns={'ticker': 'saham'})[['saham', 'tarikh', 'hasil']]


def muat(tahun):
    """sec_join.csv + sasaran + label, bagi tahun yang ada cache signals."""
    j = pd.read_csv(KELUAR / 'sec_join.csv', parse_dates=['tarikh', 'hari_tersedia'])
    bhg = []
    for th in tahun:
        if not (CACHE / f'signals_{th}.parquet').exists():
            continue
        e = j[j.tahun == th].copy()
        if e.empty:
            continue
        e['tarikh'] = pd.to_datetime(e.tarikh)
        t = sasaran(th, e)
        t['tarikh'] = pd.to_datetime(t.tarikh)
        e = e.merge(t, on=['saham', 'tarikh'], how='left')
        bhg.append(e)
    if not bhg:
        return None
    d = pd.concat(bhg, ignore_index=True)
    d['bulan'] = d.tarikh.dt.strftime('%Y-%m')
    d['minggu'] = d.tarikh.dt.strftime('%G-W%V')
    # §9.6: pengumuman terakhir lebih lama daripada BASI_MAKS hari -> lajur SEC dianggap kosong.
    # Taburan: p95 = 97 hari (kitaran suku normal), p99 = 952 (saham yang berhenti memfail).
    basi = (d.hari_sejak_earnings > BASI_MAKS) | d.hari_sejak_earnings.isna()
    d['basi'] = basi
    d.loc[basi, LAJUR] = np.nan
    print(f'  §9.6 kebasian: {int(basi.sum())} daripada {len(d)} baris'
          f' ({basi.mean() * 100:.2f}%) lajur SEC dikosongkan')
    return d


def signal_binari(d, batas):
    """Set signal §9.4: 6 kuintil + 2 tingkap earnings + 12 silang = 20. Dikunci."""
    S = {}
    for k in LAJUR:
        if k in batas:
            S[f'q5:{k}'] = (d[k] >= batas[k]['q5']).to_numpy()
            S[f'q1:{k}'] = (d[k] <= batas[k]['q1']).to_numpy()
    S['sejak_earnings_le5'] = (d.hari_sejak_earnings <= TINGKAP).fillna(False).to_numpy()
    S['jangka_earnings_le5'] = ((d.hari_ke_earnings_jangka >= 0)
                                & (d.hari_ke_earnings_jangka <= TINGKAP)).fillna(False).to_numpy()
    kuin = [n for n in S if n.startswith(('q5:', 'q1:'))]
    ting = ['sejak_earnings_le5', 'jangka_earnings_le5']
    for a in kuin:
        for b in ting:
            S[f'{a}&{b}'] = S[a] & S[b]
    return S


def batas_kuintil(d):
    """Sempadan q1/q5 atas populasi kuintil DIBEKUKAN (larian pertama) — §9.4."""
    f = CACHE / 'kuintil_sec.json'
    if f.exists():
        return json.loads(f.read_text())
    out = {}
    for k in LAJUR:
        x = d[k].to_numpy('float64')
        x = x[np.isfinite(x)]
        if x.size >= 100:
            out[k] = dict(q1=float(np.quantile(x, 0.20)), q5=float(np.quantile(x, 0.80)),
                          n=int(x.size))
    f.write_text(json.dumps(out, indent=1))
    print(f'  populasi kuintil DIBEKUKAN -> {f.name} ({len(out)} lajur)')
    return out


def ujian_51(d):
    """§5.1 + §9.3/§9.5: Spearman setiap TAHUN, tanda konsisten >= 71% tahun dinilai (min 10 tahun
    dinilai, jika tidak BELUM BOLEH DINILAI), |rho| purata >= 0.05."""
    rows = []
    th = sorted(d.tahun.unique())
    for k in LAJUR:
        r, kecuali = [], []
        for y in th:
            g = d[d.tahun == y]
            x, v = g[k].to_numpy('float64'), g.pul_henti2atr.to_numpy('float64')
            m = np.isfinite(x) & np.isfinite(v)
            # §9.7: ambang 3,000 setiap tahun; tahun di bawahnya dikecualikan sepenuhnya.
            if m.sum() < AMBANG_TAHUN:
                kecuali.append(y)
                r.append(np.nan)
                continue
            r.append(spearmanr(x[m], v[m])[0] if m.sum() > MIN_N else np.nan)
        ada = [x for x in r if np.isfinite(x)]
        pos, neg = sum(x > 0 for x in ada), sum(x < 0 for x in ada)
        rows.append(dict(lajur=k, n_tahun=len(ada), konsisten=max(pos, neg),
                         tahun_dikecualikan=','.join(str(y) for y in kecuali),
                         rho_purata=round(float(np.mean(ada)), 4) if ada else np.nan,
                         rho_min=round(min(ada), 4) if ada else np.nan,
                         rho_maks=round(max(ada), 4) if ada else np.nan,
                         rho_abs=round(float(np.mean(np.abs(ada))), 4) if ada else np.nan))
    r = pd.DataFrame(rows)
    perlu = np.ceil(PECAHAN_KONSISTEN * r.n_tahun)
    r['perlu_konsisten'] = perlu.astype('Int64')
    r['boleh_dinilai'] = r.n_tahun >= MIN_TAHUN
    r['lulus_51'] = r.boleh_dinilai & (r.konsisten >= perlu) & (r.rho_abs >= 0.05)
    return r


def ujian_52_53(d):
    """§5.2 kehadiran + §5.3 kawalan kebetulan (permutasi, bootstrap blok, BH-FDR FASA2_SEC)."""
    batas = batas_kuintil(d)
    S = signal_binari(d, batas)
    hasil = d.hasil.to_numpy()
    bulan = d.bulan.to_numpy()
    rng = np.random.default_rng(42)
    rows = []
    for nama, ada in S.items():
        pop = np.isfinite(d.pul_henti2atr.to_numpy()) & (
            d[nama.split('&')[0].split(':')[-1]].notna().to_numpy()
            if nama.split('&')[0].startswith(('q5:', 'q1:')) else True)
        ada = ada & pop
        if ada.sum() < 30:
            rows.append(dict(signal=nama, n=int(ada.sum()), nota='n < 30'))
            continue
        rawak = rng.random(ada.size) < (ada.sum() / max(pop.sum(), 1))
        m = ST.metrik(hasil[pop], ada[pop], rawak[pop], keluarga='PADU')
        p, lift_rawak_permutasi = ST.permutasi_lift(hasil[pop], ada[pop], bulan[pop],
                                                    keluarga='PADU', n=1000)
        pul = d.pul_henti2atr.to_numpy('float64')[ada]
        bt_t = ST.bootstrap_blok(pul, d.saham.to_numpy()[ada], n=1000)
        bt_w = ST.bootstrap_blok(pul, d.minggu.to_numpy()[ada], n=1000)
        jang = ST.jangkaan(pul)[0]
        urut = np.sort(pul)[::-1]
        tanpa5 = (ST.jangkaan(urut[int(np.ceil(0.05 * urut.size)):])[0]
                  if urut.size > 20 else np.nan)
        rows.append(dict(signal=nama, n=int(ada.sum()), K_padu=round(m['K_padu'], 2),
                         lift=round(m['lift'], 3), presisi=round(m['presisi'], 2),
                         lift_rawak_permutasi=(round(lift_rawak_permutasi, 3)
                                               if np.isfinite(lift_rawak_permutasi) else np.nan),
                         lift_presisi=round(m['lift_presisi'], 3), p_permutasi=p,
                         pul_purata=round(float(np.nanmean(pul)) * 100, 3),
                         jangkaan=round(jang * 100, 3), jangkaan_tanpa_5pct=round(tanpa5 * 100, 3),
                         p5_blok_ticker=round(bt_t[0] * 100, 3), p5_blok_minggu=round(bt_w[0] * 100, 3),
                         kelas=ST.kelas(m['K_padu'], m['lift'], int(ada.sum()))))
    r = pd.DataFrame(rows)
    ada_p = r.p_permutasi.notna() if 'p_permutasi' in r else pd.Series(False, index=r.index)
    r['lulus_fdr'] = False
    r['ambang_fdr'] = np.nan
    if ada_p.any():
        lulus, amb = ST.bh_fdr(r.loc[ada_p, 'p_permutasi'].to_numpy(), q=0.01)
        r.loc[ada_p, 'lulus_fdr'] = lulus
        r.loc[ada_p, 'ambang_fdr'] = amb
    # §5.3: tolak jika had bawah 95% <= 0 dalam MANA-MANA skema blok, atau jangkaan <= 0 tanpa 5% teratas
    r['lulus_53'] = (r.lulus_fdr & (r.p5_blok_ticker > 0) & (r.p5_blok_minggu > 0)
                     & (r.jangkaan_tanpa_5pct > 0))
    return r


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--sahkan', type=int, default=0,
                    help='sahkan laluan ringkas = cache fasa 1 bagi tahun ini, kemudian keluar')
    ap.add_argument('--tahun-min', type=int, default=2012, help='§9.3: liputan XBRL cukup dari 2012')
    a = ap.parse_args(argv)

    if a.sahkan:
        j = pd.read_csv(KELUAR / 'sec_join.csv', parse_dates=['tarikh'])
        ev = j[j.tahun == a.sahkan]
        kira = pulangan_dagang(a.sahkan, ev)
        cache = pd.read_parquet(CACHE / f'hadapan_{a.sahkan}.parquet',
                                columns=['ticker', 'tarikh', 'pul_henti2atr']).rename(
            columns={'ticker': 'saham'})
        b = kira.merge(cache, on=['saham', 'tarikh'], how='inner', suffixes=('_ringkas', '_cache'))
        d = (b.pul_henti2atr_ringkas - b.pul_henti2atr_cache).abs()
        print(f'SAHKAN {a.sahkan}: {len(b)} baris bertindih | beza maks {d.max():.3e}'
              f' | beza median {d.median():.3e}')
        print('LULUS: laluan ringkas sama dengan cache fasa 1' if d.max() < 1e-9
              else 'GAGAL: laluan ringkas BERBEZA — jangan guna untuk tahun baharu')
        return 0 if d.max() < 1e-9 else 1

    tahun = sorted(int(p.stem.split('_')[1]) for p in CACHE.glob('signals_*.parquet'))
    tahun = [y for y in tahun if y >= a.tahun_min]
    d = muat(tahun)
    if d is None:
        print('tiada data')
        return 1
    d = d.merge(pd.concat([hasil_label(y) for y in tahun], ignore_index=True),
                on=['saham', 'tarikh'], how='left')
    print(f'tahun {tahun[0]}-{tahun[-1]} ({len(tahun)}) | {len(d)} peristiwa'
          f' | pulangan ada {int(d.pul_henti2atr.notna().sum())}'
          f' | SUE ada {int(d.sue.notna().sum())}')

    r51 = ujian_51(d)
    r51.to_csv(KELUAR / 'sec_ujian51.csv', index=False)
    print('\n=== §5.1 PEMANGKATAN (Spearman setiap tahun; §9.3: konsisten >= 10/14, |rho| >= 0.05) ===')
    print(r51.to_string(index=False))

    r = ujian_52_53(d)
    r.to_csv(KELUAR / 'sec_ujian53.csv', index=False)
    print(f'\n=== §5.2 + §5.3 KEHADIRAN + KAWALAN (keluarga {KELUARGA}, {len(r)} ujian, q <= 0.01) ===')
    print(r.to_string(index=False))

    if not r51.boleh_dinilai.all():
        print(f'\nAMARAN §9.5: hanya {int(r51.n_tahun.max())} tahun dinilai (minimum 10).'
              ' Lajur dengan tahun < 10 ialah BELUM BOLEH DINILAI, bukan lulus dan bukan gagal.')
    n51, n53 = int(r51.lulus_51.sum()), int(r.lulus_53.sum())
    # §6 syarat 1 menuntut LAJUR YANG SAMA lulus §5.1 DAN §5.3 -- bukan sekadar "ada yang lulus
    # §5.1" dan "ada yang lulus §5.3". Signal gabungan dikaitkan kembali ke lajur induknya.
    lajur_51 = set(r51.loc[r51.lulus_51, 'lajur'])
    lajur_53 = set()
    for nm in r.loc[r.lulus_53.fillna(False), 'signal']:
        for bhg in nm.split('&'):
            k = bhg.split(':')[-1]
            if k in LAJUR:
                lajur_53.add(k)
    kedua = sorted(lajur_51 & lajur_53)
    print(f'\n§5.1 lulus: {n51}/{len(r51)} lajur | §5.3 lulus: {n53}/{len(r)} signal')
    print(f'\nlajur lulus §5.1: {sorted(lajur_51) or "tiada"}')
    print(f'lajur (induk) lulus §5.3: {sorted(lajur_53) or "tiada"}')
    if kedua:
        print(f'\n§6 SYARAT 1 DIPENUHI oleh {kedua} -> syarat 2-4 masih perlu disahkan.')
    else:
        print('\n§6 SYARAT 1 TIDAK DIPENUHI: tiada lajur lulus §5.1 DAN §5.3.')
        print('KEPUTUSAN: leg SEC fasa 2 DITOLAK.')
        if n53:
            print('§5.4 tetap dijalankan sebagai maklumat magnitud, kerana signal yang bertahan')
            print('tidak gagal ujian kebetulan -- ia gagal ujian pemangkatan lajur induknya.')
            print('Nombornya TIDAK mengubah keputusan §6.')
    json.dump(dict(tahun=tahun, n_peristiwa=int(len(d)), n_lulus_51=n51, n_lulus_53=n53,
                   lajur_lulus_51=sorted(lajur_51), lajur_induk_lulus_53=sorted(lajur_53),
                   lajur_lulus_kedua=kedua, s6_syarat1=bool(kedua),
                   keluarga=KELUARGA, n_ujian=int(len(r))),
              open(KELUAR / 'sec_keputusan.json', 'w'), indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
