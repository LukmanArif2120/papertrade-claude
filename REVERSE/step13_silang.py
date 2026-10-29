"""Kombinasi silang-keluarga: konteks HARGA x fundamental SEC — pradaftar `REVERSE/SPEC_SILANG.md`.

Fasa 1 menguji konteks harga sahaja; fasa 2 fundamental SEC sahaja. Tiada ujian pernah
menggabungkan kedua-duanya. Ini ujian signal TERAKHIR: jika ditolak, ruang signal ditutup.

Mesin fasa 2 (`step11_sec_nilai`) diguna semula bulat-bulat supaya Gate A setara, bukan ujian
baharu yang tidak boleh dibanding. Yang ditambah: lajur harga pada tarikh peristiwa yang sama
(sudah ada dalam cache `signals_*.parquet`, dikira step1 tanpa pandang hadapan), sempadan kuintil
harga yang dibekukan, dan **Gate B superaditif** — soalan sebenarnya.

Guna: python3 REVERSE/step13_silang.py [--laporan-sahaja]
Output: REVERSE/SILANG.md, REVERSE/silang_ujian.csv, REVERSE/silang_portfolio.csv
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE import step11_sec_nilai as S11  # noqa: E402
from REVERSE.teras import stat as ST  # noqa: E402

KELUAR = AKAR / 'REVERSE'
CACHE = S11.CACHE

# Grid TETAP (spec §3). Jangan lebarkan.
HARGA = ['atr_pct', 'julat20', 'bb_lebar', 'cerun_ma50', 'j_ma200', 'j_52w_tinggi']
SEC = ['q5:pecutan_hasil&sejak_earnings_le5', 'q5:pecutan_hasil', 'q5:tumbuh_hasil', 'q5:sue']
KELUARGA = 'FASA2_SILANG'
MIN_N = 200                 # spec §5 Gate A1
PECAHAN_KONSISTEN = 0.71    # Gate A2
MIN_TAHUN = 10              # Gate A2
AMBANG_TAHUN = 3000         # §9.7 fasa 2 dikekalkan


TAHUN_MIN = 2012            # §9.3 fasa 2: liputan XBRL cukup dari 2012. Kekalkan supaya setara.


def muat():
    """Peristiwa sah + lajur SEC (as-of) + label hasil + lajur HARGA (pada tarikh peristiwa).

    `S11.muat()` TIDAK melekatkan lajur `hasil`; fasa 2 melakukannya dengan gabungan berasingan
    dalam `main()`-nya. Diulang di sini supaya populasi dan label betul-betul sama.
    """
    tahun = sorted(int(p.stem.split('_')[1]) for p in CACHE.glob('signals_*.parquet'))
    tahun = [y for y in tahun if y >= TAHUN_MIN]
    d = S11.muat(tahun)
    if d is None or d.empty:
        return None
    bhg = []
    for th in tahun:
        p = CACHE / f'signals_{th}.parquet'
        if not p.exists():
            continue
        s = pd.read_parquet(p, columns=['ticker', 'tarikh', 'jenis_peristiwa', 'dalam_univ']
                            + HARGA)
        s = s[(s.jenis_peristiwa != '') & (s.dalam_univ == 1)]
        bhg.append(s.rename(columns={'ticker': 'saham'})[['saham', 'tarikh'] + HARGA])
    H = pd.concat(bhg, ignore_index=True)
    H['tarikh'] = pd.to_datetime(H.tarikh)
    H = H.drop_duplicates(['saham', 'tarikh'])
    n0 = len(d)
    d = d.merge(H, on=['saham', 'tarikh'], how='left')
    lab = pd.concat([S11.hasil_label(y) for y in tahun], ignore_index=True)
    lab['tarikh'] = pd.to_datetime(lab.tarikh)
    d = d.merge(lab.drop_duplicates(['saham', 'tarikh']), on=['saham', 'tarikh'], how='left')
    ada = d[HARGA].notna().all(axis=1).mean()
    print(f'  lajur harga dilekatkan: {n0:,} baris, {ada * 100:.1f}% lengkap | '
          f'label hasil ada {int(d.hasil.notna().sum()):,}')
    return d


def batas_harga(d):
    """Sempadan q1/q5 konteks harga, DIBEKUKAN pada larian pertama (spec §3)."""
    f = CACHE / 'kuintil_harga.json'
    if f.exists():
        return json.loads(f.read_text())
    out = {}
    for k in HARGA:
        x = d[k].to_numpy('float64')
        x = x[np.isfinite(x)]
        if x.size >= 100:
            out[k] = dict(q1=float(np.quantile(x, 0.20)), q5=float(np.quantile(x, 0.80)),
                          n=int(x.size))
    f.write_text(json.dumps(out, indent=1))
    print(f'  sempadan kuintil HARGA DIBEKUKAN -> {f.name} ({len(out)} lajur)')
    return out


def set_signal(d):
    """{nama: topeng} bagi 12 induk harga, 4 induk SEC, dan 48 silang. Dikunci oleh spec §3."""
    bh = batas_harga(d)
    bs = S11.batas_kuintil(d)
    P, S = {}, {}
    for k in HARGA:
        if k in bh:
            P[f'q5:{k}'] = (d[k] >= bh[k]['q5']).fillna(False).to_numpy()
            P[f'q1:{k}'] = (d[k] <= bh[k]['q1']).fillna(False).to_numpy()
    semua_sec = S11.signal_binari(d, bs)
    for nm in SEC:
        if nm in semua_sec:
            S[nm] = semua_sec[nm]
    X = {f'{a}+{b}': P[a] & S[b] for a in P for b in S}
    return P, S, X


def lajur_asas(nama):
    """Lajur data yang mesti bukan-NA supaya satu syarat bermakna (populasi sah)."""
    out = []
    for bhg in nama.replace('+', '&').split('&'):
        k = bhg.split(':')[-1]
        if k in HARGA or k in S11.LAJUR:
            out.append(k)
    return out


def nilai_satu(d, nama, ada, hasil, bulan, rng):
    """Gate A bagi satu syarat. Populasi = baris dengan pulangan sah DAN lajur asas bukan-NA."""
    pop = np.isfinite(d.pul_henti2atr.to_numpy())
    for k in lajur_asas(nama):
        pop = pop & d[k].notna().to_numpy()
    ada = ada & pop
    if ada.sum() < 30:
        return dict(signal=nama, n=int(ada.sum()), nota='n < 30')
    rawak = rng.random(ada.size) < (ada.sum() / max(pop.sum(), 1))
    m = ST.metrik(hasil[pop], ada[pop], rawak[pop], keluarga='PADU')
    p, _ = ST.permutasi_lift(hasil[pop], ada[pop], bulan[pop], keluarga='PADU', n=1000)
    pul = d.pul_henti2atr.to_numpy('float64')[ada]
    bt_t = ST.bootstrap_blok(pul, d.saham.to_numpy()[ada], n=1000)
    bt_w = ST.bootstrap_blok(pul, d.minggu.to_numpy()[ada], n=1000)
    urut = np.sort(pul)[::-1]
    tanpa5 = ST.jangkaan(urut[int(np.ceil(0.05 * urut.size)):])[0] if urut.size > 20 else np.nan
    # Gate A2: kekonsistenan tahunan pada tahun yang melepasi ambang liputan (§9.7 fasa 2).
    th = d.tahun.to_numpy()
    kon, dinilai = 0, 0
    for y in np.unique(th):
        my = th == y
        if my.sum() < AMBANG_TAHUN:
            continue
        ay = ada & my
        if ay.sum() < 20:
            continue
        dinilai += 1
        py = d.pul_henti2atr.to_numpy('float64')[ay]
        if np.nanmean(py) > np.nanmean(d.pul_henti2atr.to_numpy('float64')[my & pop]):
            kon += 1
    return dict(signal=nama, n=int(ada.sum()), lift=round(m['lift'], 3),
                presisi=round(m['presisi'], 2), p_permutasi=p,
                pul_purata=round(float(np.nanmean(pul)) * 100, 3),
                jangkaan_tanpa_5pct=round(tanpa5 * 100, 3),
                p5_blok_ticker=round(bt_t[0] * 100, 3),
                p5_blok_minggu=round(bt_w[0] * 100, 3),
                tahun_konsisten=kon, tahun_dinilai=dinilai,
                pecahan_konsisten=round(kon / dinilai, 3) if dinilai else np.nan)


def jalankan(d):
    """Nilai 12 induk harga + 4 induk SEC + 48 silang. FDR hanya atas 48 silang (spec §5 A4)."""
    P, S, X = set_signal(d)
    hasil = d.hasil.to_numpy()
    bulan = d.bulan.to_numpy()
    rng = np.random.default_rng(42)
    baris = []
    for jenis, kump in (('induk_harga', P), ('induk_sec', S), ('silang', X)):
        for nama, ada in kump.items():
            r = nilai_satu(d, nama, ada, hasil, bulan, rng)
            r['jenis'] = jenis
            baris.append(r)
        print(f'  {jenis}: {len(kump)} syarat dinilai', flush=True)
    R = pd.DataFrame(baris)

    # Gate A4: BH-FDR q <= 0.01 merentas 48 silang SAHAJA (satu keluarga).
    R['lulus_fdr'] = False
    R['ambang_fdr'] = np.nan
    m = (R.jenis == 'silang') & R.p_permutasi.notna()
    if m.any():
        lulus, amb = ST.bh_fdr(R.loc[m, 'p_permutasi'].to_numpy(), q=0.01)
        R.loc[m, 'lulus_fdr'] = lulus
        R.loc[m, 'ambang_fdr'] = amb
    R['gate_a'] = (R.lulus_fdr & (R.n >= MIN_N) & (R.p5_blok_ticker > 0)
                   & (R.p5_blok_minggu > 0) & (R.jangkaan_tanpa_5pct > 0)
                   & (R.tahun_dinilai >= MIN_TAHUN)
                   & (R.pecahan_konsisten >= PECAHAN_KONSISTEN)).fillna(False)

    # Gate B: superaditif — lift silang > KEDUA-DUA induknya.
    lift = dict(zip(R.signal, R.lift))
    ib, lb = [], []
    for _, r in R.iterrows():
        if r.jenis != 'silang':
            ib.append(np.nan)
            lb.append(False)
            continue
        a, b = r.signal.split('+', 1)
        la, lsb = lift.get(a, np.nan), lift.get(b, np.nan)
        mx = np.nanmax([la, lsb])
        ib.append(round(float(mx), 3) if np.isfinite(mx) else np.nan)
        lb.append(bool(np.isfinite(r.lift) and np.isfinite(mx) and r.lift > mx))
    R['lift_induk_maks'] = ib
    R['gate_b'] = lb
    return R


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--laporan-sahaja', action='store_true')
    a = ap.parse_args(argv)
    f = KELUAR / 'silang_ujian.csv'
    if a.laporan_sahaja and f.exists():
        return laporan(pd.read_csv(f))
    print('memuat peristiwa sah + lajur SEC + lajur harga...', flush=True)
    d = muat()
    if d is None:
        print('tiada data')
        return 1
    print(f'  {len(d):,} peristiwa, {d.tahun.nunique()} tahun', flush=True)
    R = jalankan(d)
    R.to_csv(f, index=False)
    return laporan(R)


def laporan(R):
    X = R[R.jenis == 'silang']
    a = X[X.gate_a]
    ab = X[X.gate_a & X.gate_b]
    L = ['# Kombinasi silang-keluarga: konteks harga × fundamental SEC', '']
    L.append(f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh '
             '`REVERSE/step13_silang.py`. Pradaftar: `REVERSE/SPEC_SILANG.md` (dikomit sebelum '
             'larian ini). **Ujian signal terakhir.**')
    L.append('')
    if len(ab):
        kpts = 'LULUS GATE A + B — Gate C diperlukan'
    elif len(a):
        kpts = 'DITOLAK pada Gate B (superaditif)'
    else:
        kpts = 'DITOLAK pada Gate A (statistik)'
    L.append(f'## Keputusan: **{kpts}**')
    L.append('')
    L.append(f'{len(X)} kombinasi silang diuji (12 konteks harga × 4 syarat SEC). '
             f'**Gate A lulus: {len(a)}. Gate A + B lulus: {len(ab)}.**')
    L.append('')
    L.append('## Gate A — statistik (sama seperti fasa 2 §5.3)')
    L.append('')
    L.append(f'`n` ≥ {MIN_N} · konsisten ≥ {PECAHAN_KONSISTEN:.0%} daripada ≥ {MIN_TAHUN} tahun '
             'dinilai · BH-FDR q ≤ 0.01 merentas 48 · jangkaan > 0 selepas buang 5% teratas · '
             'dua bootstrap blok positif.')
    L.append('')
    pecah = dict(FDR=int(X.lulus_fdr.sum()), n=int((X.n >= MIN_N).sum()),
                 konsisten=int((X.pecahan_konsisten >= PECAHAN_KONSISTEN).fillna(False).sum()),
                 tanpa5=int((X.jangkaan_tanpa_5pct > 0).fillna(False).sum()),
                 blok=int(((X.p5_blok_ticker > 0) & (X.p5_blok_minggu > 0)).fillna(False).sum()))
    for k, v in pecah.items():
        L.append(f'- lulus `{k}`: **{v}** daripada {len(X)}')
    L.append('')
    L.append('## Gate B — superaditif (soalan sebenarnya)')
    L.append('')
    L.append('`lift(silang)` mesti melebihi **kedua-dua** induknya. Tanpa gate ini satu '
             'kombinasi boleh lulus Gate A hanya kerana induk yang lebih kuat menembusi — dan '
             'itu sudah diukur oleh fasa 1 dan 2.')
    L.append('')
    sa = int(X.gate_b.sum())
    L.append(f'**{sa} daripada {len(X)} kombinasi superaditif** '
             f'({sa / max(len(X), 1) * 100:.0f}%).')
    L.append('')
    bz = (X.lift - X.lift_induk_maks).dropna()
    if len(bz):
        L.append(f'Beza `lift(silang) − lift(induk terkuat)`: median **{bz.median():+.3f}**, '
                 f'min {bz.min():+.3f}, maks {bz.max():+.3f}. Nilai negatif = **subaditif**: '
                 'mensyaratkan dua keadaan memberi lift LEBIH RENDAH daripada syarat terkuat '
                 'sendiri.')
        L.append('')
    L.append('## 10 kombinasi silang dengan lift tertinggi')
    L.append('')
    L.append('| Kombinasi | n | lift | lift induk maks | Beza | Gate A | Gate B |')
    L.append('|---|---|---|---|---|---|---|')
    tk = {True: 'ya', False: 'tidak'}
    for _, r in X.sort_values('lift', ascending=False).head(10).iterrows():
        bb = (r.lift - r.lift_induk_maks) if np.isfinite(r.lift_induk_maks) else np.nan
        L.append(f'| `{r.signal}` | {r.n:,.0f} | {r.lift:.3f} | {r.lift_induk_maks:.3f} | '
                 f'{bb:+.3f} | {tk[bool(r.gate_a)]} | {tk[bool(r.gate_b)]} |')
    L.append('')
    L.append('## Induk, sebagai rujukan')
    L.append('')
    L.append('| Syarat | Jenis | n | lift |')
    L.append('|---|---|---|---|')
    for _, r in R[R.jenis != 'silang'].sort_values('lift', ascending=False).iterrows():
        L.append(f'| `{r.signal}` | {r.jenis.replace("induk_", "")} | {r.n:,.0f} | {r.lift:.3f} |')
    L.append('')
    return laporan2(L, R, X, a, ab, bz)


def laporan2(L, R, X, a, ab, bz):
    """Tafsiran dan keputusan — dipisahkan supaya laporan() kekal boleh dibaca."""
    L.append('## Tafsiran')
    L.append('')
    if len(ab):
        L.append(f'**{len(ab)} kombinasi lulus Gate A dan Gate B.** Jangkaan priori saya dalam '
                 'spec §7 ialah DITOLAK pada Gate B, dan ia **SALAH**. Maklumat silang-keluarga '
                 'wujud: kombinasi ini membawa lift yang melebihi kedua-dua induknya dan '
                 'bertahan setiap kawalan kebetulan.')
        L.append('')
        for _, r in ab.iterrows():
            L.append(f'- `{r.signal}`: n {r.n:,.0f}, lift {r.lift:.3f} lawan induk terkuat '
                     f'{r.lift_induk_maks:.3f}, p {r.p_permutasi:.4f}, konsisten '
                     f'{r.tahun_konsisten:.0f}/{r.tahun_dinilai:.0f} tahun')
        L.append('')
        L.append('**Gate C belum dinilai dan ia menentukan.** Spec §6: DITERIMA hanya jika '
                 'portfolio median 20 benih mengalahkan SPUS pada pulangan DAN MDD. Fasa 2 '
                 'menunjukkan satu signal boleh bertahan setiap ujian statistik dan tetap gagal '
                 'di peringkat portfolio.')
    elif len(a):
        L.append(f'**{len(a)} kombinasi lulus Gate A tetapi 0 lulus Gate B.** Jangkaan priori '
                 'saya dalam spec §7 ialah tepat ini.')
        L.append('')
        L.append('Maksudnya: kombinasi itu signifikan secara statistik, tetapi liftnya **tidak '
                 'melebihi** induk terkuatnya. Ia adalah induk yang menembusi, bukan maklumat '
                 'baharu. Fasa 1 dan 2 sudah mengukur induk-induk itu.')
    else:
        L.append('**0 kombinasi lulus Gate A.** Tiada kombinasi silang-keluarga bertahan '
                 'kawalan kebetulan yang sama yang dipakai fasa 2.')
    L.append('')
    if len(bz) and bz.median() < 0:
        L.append(f'Dapatan struktur: beza lift median **{bz.median():+.3f}** — interaksi di '
                 f'sini **subaditif secara majoriti** ({int((~X.gate_b).sum())} daripada '
                 f'{len(X)}). Mensyaratkan dua keadaan mengecilkan `n` sementara keadaan itu '
                 'sendiri berkorelasi, jadi lift biasanya jatuh di bawah syarat terkuat.')
        L.append('')
        L.append(f'**Rujukan antara dua kenyataan di atas:** sebab 4 dalam spec §7 betul sebagai '
                 f'**kecenderungan** — majoriti kombinasi memang subaditif. Ia salah sebagai '
                 f'**dakwaan menyeluruh**: {int(X.gate_b.sum())} daripada {len(X)} superaditif, '
                 f'dan {len(ab)} daripadanya juga bertahan setiap kawalan kebetulan. Saya '
                 'menggunakan kecenderungan itu untuk meramal tiada pengecualian, dan itu '
                 'kesilapan penaakulan, bukan kesilapan ukuran.')
        L.append('')
    if not len(ab):
        L.append('## Ruang signal ditutup')
        L.append('')
        L.append('Spec §1: ini ujian signal terakhir. Ketiga-tiga keluarga kini diukur dengan '
                 'kawalan kebetulan yang sama:')
        L.append('')
        L.append('| Keluarga | Apa yang diuji | Keputusan |')
        L.append('|---|---|---|')
        L.append('| Harga (fasa 1) | 101 tunggal + 120 kombinasi, 20,640 ujian ENTRY | DITOLAK |')
        L.append('| Fundamental SEC (fasa 2) | 20 signal, 12 kombinasi | DITOLAK (1 lulus '
                 '§5.3, gagal §6) |')
        L.append(f'| Silang (ini) | {len(X)} kombinasi harga × SEC | DITOLAK |')
        L.append('')
        L.append('Tambah `PEMBINAAN.md` (pembinaan portfolio tanpa pemicu: DITOLAK) dan '
                 'kedua-dua paksi yang ada — **apa yang dibeli** dan **bagaimana ia dipegang** — '
                 'telah diukur terhadap SPUS dan kedua-duanya kalah.')
        L.append('')
        L.append('Yang tinggal bukan kajian: biarkan `portfolio_slot/` terkumpul dan banding '
                 'dengan SPUS (`laporan/BANDING_SPUS.md`). Kuasa statistiknya sudah dikira — '
                 'kelebihan benar 10 mata/tahun memerlukan ~489 sesi.')
        L.append('')
    L.append('## Had')
    L.append('')
    L.append('- Alam Release `autotune-data-a02`, **bukan** ditapis Syariah; SPUS ditapis.')
    L.append('- Lajur harga diambil daripada cache `signals_*.parquet` fasa 1 (dikira step1 '
             'tanpa pandang hadapan), jadi ia tepat lajur yang sama yang fasa 1 nilai.')
    L.append('- Sempadan kuintil harga dibekukan pada larian pertama; ia **tidak** ditala.')
    L.append('- Grid 48 ditetapkan dalam spec §3 sebelum larian dan tidak dilebarkan.')
    L.append('- Konteks harga terbaik fasa 1 ialah konteks pengembangan kemeruapan, iaitu '
             'kohort yang paling tercemar oleh ketiadaan saham delist dalam stor. Bias itu '
             '**memihak** kepada kombinasi, bukan terhadapnya.')
    L.append('')
    L.append('**Ia tidak mencapai +10%/bulan.** Lihat `SASARAN.md`.')
    L.append('')
    (KELUAR / 'SILANG.md').write_text('\n'.join(L), encoding='utf-8')
    c = ['signal', 'n', 'lift', 'lift_induk_maks', 'gate_a', 'gate_b']
    print('\n' + X.sort_values('lift', ascending=False).head(12)[c].to_string(index=False))
    print(f'\nGate A: {len(a)}/{len(X)} | Gate A+B: {len(ab)}/{len(X)} | '
          f'beza lift median {bz.median():+.3f}' if len(bz) else '')
    return 0


if __name__ == '__main__':
    sys.exit(main())
