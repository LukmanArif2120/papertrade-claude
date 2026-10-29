"""Gate C bagi kombinasi silang-keluarga — pradaftar `REVERSE/SPEC_SILANG.md` §5 Gate C.

Empat kombinasi lulus Gate A (statistik) dan Gate B (superaditif). Gate C menentukan: adakah
portfolio yang dibina atasnya mengalahkan SPUS pada pulangan DAN MDD?

Fasa 2 menunjukkan satu signal boleh bertahan setiap ujian statistik dan tetap gagal di peringkat
portfolio. `SPEC.md` §3 menetapkan kriteria akhir kajian ialah prestasi portfolio, bukan lift.

Pembinaan: lalai TETAP kajian — `REF_jual_hari63`, 8 slot, saiz tetap (`SPEC.md` §3), sama seperti
`KEPEKATAN.md` dan `KEPEKATAN_BENIH.md`. Spec §5 Gate C tidak menamakan rujukan keluar; memilihnya
selepas melihat hasil akan menjadi pemilihan selepas fakta, jadi lalai kajian diguna.

20 benih kerana hingar pemilihan = 17.3 mata peratus setahun (`KEPEKATAN_BENIH.md`).

Guna: python3 REVERSE/step14_silang_portfolio.py [--benih 20] [--laporan-sahaja]
Output: REVERSE/SILANG_GATE_C.md, REVERSE/silang_portfolio.csv
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
from REVERSE import step9_portfolio as S9  # noqa: E402
from REVERSE import step11_sec_nilai as S11  # noqa: E402
from REVERSE import step12_sec_portfolio as S12  # noqa: E402
from REVERSE import step13_silang as SX  # noqa: E402
from REVERSE.teras import stat as ST  # noqa: E402

KELUAR = AKAR / 'REVERSE'
KELUARAN = 'REF_jual_hari63'   # lalai tetap kajian
SLOT = 8                       # SPEC.md §3
UJI0, UJI1 = 2020, 2025        # tingkap keputusan Gate C (SPUS mula Dis 2019)
N_BENIH = 20


def penanda_spus():
    """SPUS pada KEDUA-DUA konvensyen (PEMBINAAN.md): median tahunan dan CAGR tingkap."""
    f = AKAR / 'BacktestShariah2' / 'data' / 'penanda_aras' / 'spus_bulanan.csv'
    s = pd.read_csv(f, comment='#')
    s['bulan'] = pd.PeriodIndex(s.bulan, freq='M')
    pt, mt = [], []
    for y in range(UJI0, UJI1 + 1):
        q = s[(s.bulan >= pd.Period(f'{y - 1}-12'))
              & (s.bulan <= pd.Period(f'{y}-12'))].tutup.to_numpy('float64')
        if len(q) >= 3:
            pt.append((q[-1] / q[0] - 1) * 100)
            mt.append(ST.mdd(q))
    w = s[(s.bulan >= pd.Period(f'{UJI0}-01')) & (s.bulan <= pd.Period(f'{UJI1}-12'))]
    v = w.tutup.to_numpy('float64')
    th = (w.bulan.iloc[-1] - w.bulan.iloc[0]).n / 12.0
    return dict(median_pul=float(np.median(pt)), median_mdd=float(np.median(mt)),
                cagr=float(((v[-1] / v[0]) ** (1 / th) - 1) * 100), mdd_tingkap=ST.mdd(v),
                tahun_terburuk=float(np.min(pt)), mdd_terdalam=float(np.min(mt)))


def entri_signal(d, nama):
    """(ticker, tarikh) bagi satu syarat silang."""
    P, S, X = SX.set_signal(d)
    semua = {**P, **S, **X}
    ada = semua[nama]
    pop = np.isfinite(d.pul_henti2atr.to_numpy())
    for k in SX.lajur_asas(nama):
        pop = pop & d[k].notna().to_numpy()
    e = d.loc[ada & pop, ['saham', 'tarikh']].rename(columns={'saham': 'ticker'})
    return e.drop_duplicates()


def jalan_signal(nama, ent, benih_senarai):
    """Metrik setiap (benih, tahun) bagi satu signal. Data tahun dimuat SEKALI, benih dilingkar."""
    baris = []
    for th in range(UJI0, UJI1 + 1):
        eth = ent[pd.to_datetime(ent.tarikh).dt.year == th]
        if eth.empty:
            continue
        fr, pra, c, o, to, atrp, kal, _ = S12.sedia_tahun(th, eth)
        e2 = eth.assign(tarikh=pd.to_datetime(eth.tarikh))
        for b in benih_senarai:
            rng = np.random.default_rng(b)
            # Hanya SUSUNAN pilihan berubah ikut benih; set entri kekal sama.
            pilihan = {(t, pd.Timestamp(dd)): (float(rng.random()), 0.0, t)
                       for t, dd in zip(eth.ticker, eth.tarikh)}
            siri, dag, info = S9.jalankan(KELUARAN, e2, fr, pra, c, o, to, kal, KELUARAN, None,
                                          pilihan, slot=SLOT)
            if siri.empty:
                continue
            ek = siri.set_index('tarikh').ekuiti
            bl = ek.resample('ME').last().pct_change().dropna() * 100
            baris.append(dict(signal=nama, benih=b, tahun=th,
                              pulangan=round((float(ek.iloc[-1]) - 1) * 100, 3),
                              mdd=round(ST.mdd(ek.to_numpy()), 3),
                              median_bulanan=round(float(bl.median()), 3) if len(bl) else np.nan,
                              pct_bulan_ge10=(round(float((bl >= 10).mean() * 100), 1)
                                              if len(bl) else np.nan),
                              n_masuk=info['n_masuk'],
                              slot_purata=round(float(info['purata_slot_terisi']), 2)))
    return baris


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--benih', type=int, default=N_BENIH)
    ap.add_argument('--laporan-sahaja', action='store_true')
    a = ap.parse_args(argv)
    f = KELUAR / 'silang_portfolio.csv'
    if a.laporan_sahaja and f.exists():
        return laporan(pd.read_csv(f))

    R13 = pd.read_csv(KELUAR / 'silang_ujian.csv')
    lulus = R13[(R13.jenis == 'silang') & R13.gate_a.fillna(False)
                & R13.gate_b.fillna(False)].signal.tolist()
    if not lulus:
        print('TIADA kombinasi lulus Gate A + B; Gate C tidak dijalankan (spec §6).')
        return 0
    print(f'Gate C bagi {len(lulus)} kombinasi: {lulus}', flush=True)

    d = SX.muat()
    if d is None:
        print('tiada data')
        return 1
    d = d[d.tahun >= SX.TAHUN_MIN]
    t0 = time.time()
    baris = []
    for nm in lulus:
        ent = entri_signal(d, nm)
        print(f'  {nm}: {len(ent):,} entri {UJI0}-{UJI1} '
              f'({len(ent[pd.to_datetime(ent.tarikh).dt.year.between(UJI0, UJI1)]):,})',
              flush=True)
        baris += jalan_signal(nm, ent, range(1, a.benih + 1))
        print(f'  [{time.time() - t0:.0f}s] {nm} siap: {len(baris)} baris', flush=True)
    if not baris:
        print('tiada baris portfolio')
        return 1
    R = pd.DataFrame(baris)
    R.to_csv(f, index=False)
    return laporan(R)


def laporan(R):
    sp = penanda_spus()
    # Konvensyen 1 (median tahunan) — sama seperti KEPEKATAN.md / PENANDA_ARAS_SYARIAH.md.
    g1 = R.groupby('signal').agg(
        pul_median=('pulangan', 'median'), mdd_median=('mdd', 'median'),
        bulanan=('median_bulanan', 'median'), ge10=('pct_bulan_ge10', 'median'),
        masuk=('n_masuk', 'median'), slot=('slot_purata', 'median')).reset_index()
    # Konvensyen 2 (CAGR) — kompaun pulangan tahunan setiap benih, kemudian median benih.
    b = []
    for (nm, bn), g in R.groupby(['signal', 'benih']):
        p = g.sort_values('tahun').pulangan.to_numpy('float64') / 100 + 1
        n = len(p)
        b.append(dict(signal=nm, benih=bn, cagr=(p.prod() ** (1 / n) - 1) * 100,
                      mdd_terdalam=float(g.mdd.min())))
    B = pd.DataFrame(b)
    g2 = B.groupby('signal').agg(cagr_median=('cagr', 'median'),
                                 cagr_p10=('cagr', lambda x: x.quantile(0.10)),
                                 cagr_p90=('cagr', lambda x: x.quantile(0.90)),
                                 mdd_terdalam=('mdd_terdalam', 'median')).reset_index()
    G = g1.merge(g2, on='signal')
    # Gate C spec §5: median kalahkan SPUS pada pulangan DAN MDD, pada KEDUA-DUA konvensyen.
    G['c_median'] = (G.pul_median > sp['median_pul']) & (G.mdd_median > sp['median_mdd'])
    G['c_cagr'] = (G.cagr_median > sp['cagr']) & (G.mdd_terdalam > sp['mdd_tingkap'])
    G['gate_c'] = G.c_median & G.c_cagr
    lulus = G[G.gate_c]

    L = ['# Gate C: portfolio daripada kombinasi silang-keluarga', '']
    L.append(f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh '
             '`REVERSE/step14_silang_portfolio.py`. Pradaftar `REVERSE/SPEC_SILANG.md` §5 Gate C.')
    L.append('')
    L.append(f'## Keputusan akhir: **{"DITERIMA" if len(lulus) else "DITOLAK"}**')
    L.append('')
    L.append(f'Pembinaan: `{KELUARAN}`, {SLOT} slot, saiz tetap — lalai TETAP kajian '
             '(`SPEC.md` §3), bukan dipilih selepas melihat hasil. '
             f'{int(R.benih.nunique())} benih × {UJI0}–{UJI1}, kos penuh.')
    L.append('')
    L.append(f'**SPUS {UJI0}–{UJI1}:** median tahunan {sp["median_pul"]:+.2f}% / MDD '
             f'{sp["median_mdd"]:.2f}% · CAGR tingkap {sp["cagr"]:+.2f}% / MDD '
             f'{sp["mdd_tingkap"]:.2f}%. Kedua-dua konvensyen diperlukan (`PEMBINAAN.md`).')
    L.append('')
    L.append('| Kombinasi | Pulangan median | MDD median | CAGR median | p10 | p90 | '
             'MDD terdalam | Masuk/thn | Slot terisi | Gate C |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for _, r in G.sort_values('cagr_median', ascending=False).iterrows():
        L.append(f'| `{r.signal}` | {r.pul_median:+.2f}% | {r.mdd_median:.2f}% | '
                 f'{r.cagr_median:+.2f}% | {r.cagr_p10:+.2f}% | {r.cagr_p90:+.2f}% | '
                 f'{r.mdd_terdalam:.2f}% | {r.masuk:.0f} | {r.slot:.1f} | '
                 f'{"**YA**" if r.gate_c else "tidak"} |')
    L.append(f'| **SPUS** | **{sp["median_pul"]:+.2f}%** | **{sp["median_mdd"]:.2f}%** | '
             f'**{sp["cagr"]:+.2f}%** | — | — | **{sp["mdd_tingkap"]:.2f}%** | 1 | — | — |')
    L.append('')
    return laporan2(L, R, G, lulus, sp)


def laporan2(L, R, G, lulus, sp):
    """Tafsiran — dipisahkan supaya laporan() kekal boleh dibaca."""
    L.append('## Kapasiti slot')
    L.append('')
    L.append('Soalan (c) arahan asal: cukup untuk mengisi portfolio? Fasa 1 mendapati '
             '**kapasiti slot yang mengikat, bukan kadar menang** — rujukan pegang panjang hanya '
             f'membuka 8–16 posisi setahun berbanding ~130 yang diperlukan untuk {SLOT} slot.')
    L.append('')
    for _, r in G.sort_values('masuk', ascending=False).iterrows():
        L.append(f'- `{r.signal}`: **{r.masuk:.0f} masuk/tahun**, slot terisi purata '
                 f'**{r.slot:.1f} daripada {SLOT}**')
    L.append('')
    sl = float(G.slot.max())
    if sl < SLOT * 0.75:
        L.append(f'Slot terisi tertinggi hanya **{sl:.1f} daripada {SLOT}** — portfolio duduk '
                 'dalam tunai sebahagian besar masa. Itu meredam pulangan DAN MDD serentak, '
                 'jadi angka MDD di atas mesti dibaca bersama kadar pengisian, bukan sendiri.')
        L.append('')
    L.append('## Tafsiran')
    L.append('')
    if len(lulus):
        L.append(f'**{len(lulus)} kombinasi lulus ketiga-tiga gate.** Jangkaan priori saya dalam '
                 '`SPEC_SILANG.md` §7 ialah DITOLAK pada Gate B, dan ia **SALAH pada kedua-dua '
                 'kiraan**: maklumat silang-keluarga wujud (Gate B), dan portfolio yang dibina '
                 'atasnya mengalahkan SPUS pada kedua-dua paksi dan kedua-dua konvensyen.')
        L.append('')
        L.append('**Ini tetap backtest.** Langkah seterusnya bukan mempercayainya, tetapi '
                 'menjalankannya ke hadapan sebagai lorong `portfolio_slot/` dengan jalur benih, '
                 'dan membandingkannya dengan SPUS melalui `laporan/BANDING_SPUS.md`. Kuasa '
                 'statistik sudah dikira: kelebihan benar 10 mata/tahun memerlukan ~489 sesi.')
        L.append('')
        L.append('Had yang perlu dinyatakan bersama: `n` kecil (541–751 peristiwa atas 14 tahun), '
                 'jangkaan selepas membuang 5% pemenang teratas kecil (+0.22 hingga +1.17%), dan '
                 'kesemua empat berkongsi syarat SEC yang **sama** — jadi ia bukan empat dapatan '
                 'bebas, ia satu dapatan (PEAD) dilihat melalui empat konteks harga yang '
                 'berkorelasi.')
    else:
        L.append('**Tiada kombinasi lulus Gate C.** Maklumat silang-keluarga **WUJUD** — empat '
                 'kombinasi lulus Gate A dan Gate B, jadi jangkaan priori saya dalam '
                 '`SPEC_SILANG.md` §7 (DITOLAK pada Gate B) ialah **SALAH**. Tetapi ia '
                 '**tidak mencukupi** untuk mengalahkan memegang SPUS.')
        L.append('')
        L.append('Itu hasil yang spec §6 namakan secara khusus: "maklumat silang-keluarga WUJUD '
                 'tetapi tidak mencukupi" — berbeza daripada penolakan penuh, dan mesti '
                 'dinyatakan sebagai begitu.')
        L.append('')
        gagal = []
        if not G.c_median.any():
            gagal.append('konvensyen median tahunan')
        if not G.c_cagr.any():
            gagal.append('konvensyen CAGR')
        if gagal:
            L.append('Gagal pada: ' + ', '.join(gagal) + '.')
            L.append('')
    L.append('## Mengapa kesemua empat berkongsi induk SEC yang sama')
    L.append('')
    L.append('Kesemua empat kombinasi yang lulus Gate A + B ialah konteks harga × '
             '`q5:pecutan_hasil&sejak_earnings_le5` — iaitu **PEAD**, satu-satunya signal yang '
             'bertahan §5.3 fasa 2. Tiada kombinasi dengan `q5:sue`, `q5:tumbuh_hasil` atau '
             '`q5:pecutan_hasil` tanpa tingkap earnings yang lulus.')
    L.append('')
    L.append('Maksudnya maklumat silang itu **bukan sifat umum "fundamental × harga"**. Ia '
             'khusus: kesan PEAD menjadi lebih kuat apabila disaring oleh konteks harga '
             '(cerun MA50 tinggi, jauh di atas MA200, julat/ATR mengembang). Itu konsisten '
             'dengan kesusasteraan PEAD — hanyutan lebih kuat apabila pasaran sedang memberi '
             'perhatian kepada saham itu.')
    L.append('')
    L.append('## Had')
    L.append('')
    L.append(f'- Alam Release `autotune-data-a02`, **bukan** ditapis Syariah; SPUS ditapis. '
             'Tapisan Syariah membuang semua kewangan, jadi perbandingan tidak setara pada '
             'paksi itu.')
    L.append('- Satu rujukan keluar dan satu saiz sahaja. Spec §5 Gate C tidak menamakannya; '
             f'`{KELUARAN}` + saiz tetap diguna sebagai lalai kajian. Menguji beberapa rujukan '
             'dan melaporkan yang terbaik akan menjadi pemilihan selepas fakta.')
    L.append(f'- Tingkap {UJI0}–{UJI1} sahaja (6 tahun) kerana SPUS mula Dis 2019. Itu tempoh '
             'yang pendek dan ia merangkumi satu pasaran menaik yang kuat.')
    L.append('- Pulangan tahunan dikira setiap tahun secara berasingan (mesin fasa 1/2), '
             'kemudian dikompaun untuk CAGR. Posisi tidak dibawa merentas sempadan tahun.')
    L.append('- MDD SPUS daripada tutup **bulanan**, jadi lebih cetek daripada MDD harian yang '
             'benar. Itu menjadikan syarat MDD **lebih sukar** bagi sistem, bukan lebih mudah.')
    L.append('')
    L.append('**Ia tidak mencapai +10%/bulan.** Lihat `SASARAN.md`.')
    L.append('')
    (KELUAR / 'SILANG_GATE_C.md').write_text('\n'.join(L), encoding='utf-8')
    c = ['signal', 'pul_median', 'mdd_median', 'cagr_median', 'mdd_terdalam', 'masuk', 'slot',
         'gate_c']
    print('\n' + G[c].round(2).to_string(index=False))
    print(f'\nSPUS median {sp["median_pul"]:.2f}%/{sp["median_mdd"]:.2f}% | '
          f'CAGR {sp["cagr"]:.2f}%/{sp["mdd_tingkap"]:.2f}% | '
          f'{"DITERIMA: " + ",".join(lulus.signal) if len(lulus) else "GATE C DITOLAK"}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
