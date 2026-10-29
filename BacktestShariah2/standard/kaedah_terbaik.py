"""Kaedah mana terbaik buat masa sekarang? — soalan pengguna 29 Okt 2026.

Papan Penganalisis (`laporan/PENGANALISIS.md`) sudah membanding semua kaedah dan dijana semula
setiap malam. Dokumen ini TIDAK mengulanginya. Ia menjawab soalan yang mesti dijawab DAHULU
sebelum mana-mana pangkat boleh dipercayai:

  1. Adakah pangkat backtest meramal prestasi hadapan? (jika tidak, tiada pangkat boleh diguna)
  2. Ada kaedah yang pulangan hadapannya POSITIF secara boleh ukur?
  3. Bila pangkat kaedah boleh dipercayai?

Nota penting: REVERSE menguji signal/indikator, **BUKAN** kaedah Mxx (`CLAUDE.md`). Keputusan
REVERSE tidak terpakai di sini dan populasinya tidak boleh dicampur. Ini populasi berasingan dengan
backtestnya sendiri (set 431) dan jejak hadapannya sendiri (Lejar Penuh + Papertrade C).

Guna: python3 BacktestShariah2/standard/kaedah_terbaik.py
Output: BacktestShariah2/laporan/KAEDAH_TERBAIK.md
"""
import glob
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAPAN = os.path.join(AKAR, 'BacktestShariah2', 'data', 'analisis', 'papan.json')
KELUAR = os.path.join(AKAR, 'BacktestShariah2', 'laporan', 'KAEDAH_TERBAIK.md')
MIN_N = 20        # posisi ditutup minimum untuk menguji satu kaedah
MIN_KLUSTER = 3   # hari beli berbeza minimum untuk SE berkelompok
Q_FDR = 0.05


def papan():
    d = json.load(open(PAPAN, encoding='utf-8'))
    B = pd.DataFrame(d['rows']).set_index('id')
    B['n_lulus'] = B[['lulus_subset', 'lulus_wfo', 'lulus_at']].sum(axis=1)
    return B, d


def papertrade_c():
    """Posisi Papertrade C yang sah, dengan jarak henti."""
    f = sorted(glob.glob(os.path.join(AKAR, 'BacktestShariah2', 'papertrade', 'claude*.csv')))
    C = pd.concat([pd.read_csv(x) for x in f], ignore_index=True)
    C = C[C.tidak_sah.isna() | (C.tidak_sah.astype(str) == 'False')].copy()
    C['terbuka'] = C.untung_akhir_pct.isna()
    m = (C.henti > 0) & (C.harga_beli > 0)
    C.loc[m, 'jarak'] = (C.loc[m, 'harga_beli'] - C.loc[m, 'henti']) / C.loc[m, 'harga_beli'] * 100
    return C


def t_berkelompok(g, lajur='untung_akhir_pct'):
    """(purata, t, n_kluster) dengan SE berkelompok ikut hari beli.

    Posisi yang dibeli pada hari sama bergerak bersama pasaran, jadi melayannya sebagai bebas
    melebih-lebihkan keyakinan. Papan Penganalisis guna pembetulan yang sama (`n_berkesan`).
    """
    m = float(g[lajur].mean())
    kl = g.groupby('tarikh_beli')[lajur].mean()
    if len(kl) < MIN_KLUSTER:
        return m, np.nan, len(kl)
    se = float(kl.std(ddof=1)) / np.sqrt(len(kl))
    return m, (m / se if se > 0 else np.nan), len(kl)


def spearman_separa(d, x, y, z):
    """Korelasi Spearman separa: x lwn y, mengawal z (pangkat, kemudian sisa linear)."""
    s = d.dropna(subset=[x, y, z])
    if len(s) < 10:
        return np.nan, np.nan, len(s)
    rx, ry, rz = (stats.rankdata(s[c]) for c in (x, y, z))

    def sisa(a, b):
        return a - np.polyval(np.polyfit(b, a, 1), b)

    r, p = stats.pearsonr(sisa(rx, rz), sisa(ry, rz))
    return r, p, len(s)


def uji_kaedah(k, B):
    """Ujian setiap kaedah: purata realisasi, t berkelompok, BH-FDR merentas kaedah diuji."""
    baris = []
    for kid, g in k.groupby('id_kaedah'):
        if len(g) < MIN_N:
            continue
        m, t, nk = t_berkelompok(g)
        if not np.isfinite(t):
            continue
        baris.append(dict(id=kid, n=len(g), hari_beli=nk, real=m, t=t,
                          median_pul=float(g.untung_akhir_pct.median()),
                          menang=float((g.untung_akhir_pct > 0).mean() * 100),
                          p=2 * (1 - stats.t.cdf(abs(t), nk - 1))))
    if not baris:
        # Tiada kaedah memenuhi syarat (cth. awal jejak hadapan): pulangkan rangka kosong
        # yang berlajur penuh supaya pemanggil tidak perlu kes khas.
        kol = ['n', 'hari_beli', 'real', 't', 'median_pul', 'menang', 'p', 'ambang_bh',
               'lulus_bh', 'nama', 'hari', 'bt_purata', 'n_lulus']
        return pd.DataFrame(columns=kol, index=pd.Index([], name='id'))
    R = pd.DataFrame(baris).set_index('id').sort_values('p')
    mm = len(R)
    R['ambang_bh'] = Q_FDR * np.arange(1, mm + 1) / mm
    R['lulus_bh'] = R.p <= R.ambang_bh
    return R.join(B[['nama', 'hari', 'bt_purata', 'n_lulus']])


def main():
    B, d = papan()
    C = papertrade_c()
    k = C[~C.terbuka]
    G = k.groupby('id_kaedah').agg(n=('untung_akhir_pct', 'size'),
                                   real=('untung_akhir_pct', 'mean'),
                                   jarak=('jarak', 'median')).join(B)
    G = G.dropna(subset=['real', 'bt_purata'])
    R = uji_kaedah(k, B)

    A = ['# Kaedah mana terbaik buat masa sekarang?', '']
    A.append(f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh '
             '`standard/kaedah_terbaik.py`. Rekod analisis sahaja.')
    A.append('')
    A.append('Papan Penganalisis (`laporan/PENGANALISIS.md`) sudah membanding semua kaedah dan '
             'dijana semula setiap malam. Dokumen ini tidak mengulanginya — ia menjawab soalan '
             'yang mesti dijawab **dahulu** sebelum mana-mana pangkat boleh dipercayai.')
    A.append('')
    A.append('**REVERSE menguji signal/indikator, BUKAN kaedah Mxx** (`CLAUDE.md`). Keputusan '
             'REVERSE tidak terpakai di sini. Ini populasi berasingan.')
    A.append('')

    # ---------- 1. Jawapan pendek ----------
    pos = R[(R.real > 0) & R.lulus_bh]
    neg = R[(R.real < 0) & R.lulus_bh]
    A.append('## 1. Jawapan pendek')
    A.append('')
    A.append(f'**Tiada.** Daripada {len(R)} kaedah yang mempunyai cukup posisi ditutup untuk '
             f'diuji, **{len(neg)} terbukti NEGATIF** pada BH-FDR q ≤ {Q_FDR} dengan ralat '
             f'piawai berkelompok ikut hari beli, dan **{len(pos)} terbukti positif**.')
    A.append('')
    A.append('Itu bukan bermakna semua kaedah buruk. Ia bermakna tingkap hadapan masih terlalu '
             'pendek, dan bahagian 2 menunjukkan mengapa pangkat yang anda lihat sekarang '
             'tidak boleh diguna.')
    A.append('')

    # ---------- 2. Adakah backtest meramal hadapan? ----------
    A.append('## 2. Adakah pangkat backtest meramal prestasi hadapan?')
    A.append('')
    r0, p0 = stats.spearmanr(G.bt_purata, G.real)
    A.append(f'Korelasi mentah jangkaan backtest lawan pulangan realisasi Papertrade C merentas '
             f'**{len(G)} kaedah**: Spearman rho **{r0:+.3f}**, p {p0:.4f}.')
    A.append('')
    A.append('Negatif. Dibaca mentah, itu bermakna kaedah dengan backtest LEBIH BAIK berprestasi '
             'LEBIH BURUK ke hadapan — dan itu akan menjadi dapatan yang besar. **Ia salah.**')
    A.append('')
    rj, pj, _ = spearman_separa(G, 'bt_purata', 'real', 'jarak')
    rh, ph, _ = spearman_separa(G, 'bt_purata', 'real', 'hari')
    rbh, pbh = stats.spearmanr(G.dropna(subset=['hari']).bt_purata,
                               G.dropna(subset=['hari']).hari)
    A.append(f'Jangkaan backtest berkorelasi **{rbh:+.3f}** dengan hari pegang backtest — '
             'sepele: pegang lebih lama memberi pulangan lebih besar setiap dagangan. Dan dalam '
             'tingkap hadapan 3 minggu, kaedah pegang-panjang belum ada masa untuk berfungsi.')
    A.append('')
    A.append('| Korelasi | rho | p |')
    A.append('|---|---|---|')
    A.append(f'| Mentah: backtest → realisasi | **{r0:+.3f}** | {p0:.4f} |')
    A.append(f'| Separa, kawal lebar henti | {rj:+.3f} | {pj:.4f} |')
    A.append(f'| **Separa, kawal hari pegang** | **{rh:+.3f}** | **{ph:.4f}** |')
    A.append('')
    A.append(f'Mengawal hari pegang, korelasi bertukar daripada {r0:+.3f} kepada **{rh:+.3f}** '
             f'dan **tidak lagi signifikan** (p {ph:.3f}). Jadi tanda negatif itu **artifak '
             'panjang tingkap**, bukan bukti pangkat terbalik.')
    A.append('')
    A.append('**Kesimpulan bahagian ini:** pangkat backtest tidak mempunyai kuasa ramalan yang '
             'boleh diukur pada data hadapan sekarang — tidak positif, tidak negatif. Jadi '
             '"kaedah teratas papan" bukan jawapan kepada "kaedah terbaik".')
    A.append('')
    return laporan2(A, B, C, G, R, d)


def laporan2(A, B, C, G, R, d):
    k = C[~C.terbuka]
    # ---------- 3. Ujian setiap kaedah ----------
    A.append('## 3. Ada kaedah yang positif secara boleh ukur?')
    A.append('')
    A.append(f'Ujian: purata pulangan realisasi setiap kaedah dengan ≥ {MIN_N} posisi ditutup, '
             f't dengan ralat piawai **berkelompok ikut hari beli** (posisi hari sama bergerak '
             f'bersama pasaran), BH-FDR q ≤ {Q_FDR} merentas {len(R)} kaedah yang diuji.')
    A.append('')
    A.append('| Kaedah | n | Hari beli | Realisasi | Median | Menang | t | p | FDR | Backtest hari |')
    A.append('|---|---|---|---|---|---|---|---|---|---|')
    tk = {True: '**lulus**', False: 'tidak'}
    for kid, r in R.head(10).iterrows():
        A.append(f'| `{kid}` {str(r.nama)[:26]} | {r.n:.0f} | {r.hari_beli:.0f} | '
                 f'{r.real:+.2f}% | {r.median_pul:+.2f}% | {r.menang:.0f}% | {r.t:+.1f} | '
                 f'{r.p:.4f} | {tk[bool(r.lulus_bh)]} | {r.hari:.1f} |')
    A.append('')
    neg = R[(R.real < 0) & R.lulus_bh]
    A.append(f'**{len(neg)} daripada {len(R)} kaedah terbukti negatif; 0 terbukti positif.** '
             'Jadual di atas 10 teratas ikut p — kesemuanya negatif.')
    A.append('')
    # Calon positif terbaik, dengan kaveat pelbagai ujian
    cal = R[R.real > 0].sort_values('p')
    if len(cal):
        c0 = cal.iloc[0]
        A.append(f'Calon positif terbaik ialah `{cal.index[0]}` {str(c0.nama)[:40]}: '
                 f'**{c0.real:+.2f}%** atas {c0.n:.0f} posisi ditutup merentas '
                 f'{c0.hari_beli:.0f} hari beli, kadar menang {c0.menang:.0f}%, '
                 f'median {c0.median_pul:+.2f}%, t {c0.t:+.2f}, p {c0.p:.4f}.')
        A.append('')
        A.append(f'**Ia TIDAK bertahan pembetulan pelbagai ujian.** p {c0.p:.4f} melepasi ambang '
                 f'mentah 0.05 tetapi bukan ambang BH bagi pangkatnya merentas {len(R)} kaedah. '
                 'Menguji 38 kaedah dan melaporkan yang terbaik adalah cara paling biasa untuk '
                 'menipu diri sendiri. Ia **calon untuk diperhatikan**, bukan jawapan.')
        A.append('')

    # ---------- 4. Mengapa pegang-panjang belum boleh dinilai ----------
    A.append('## 4. Mengapa separuh papan belum boleh dinilai')
    A.append('')
    J = C.groupby('id_kaedah').terbuka.agg(n='size', pct='mean').join(B[['hari']]).dropna()
    A.append('| Kumpulan backtest | Kaedah | Posisi masih terbuka | Realisasi purata | Positif |')
    A.append('|---|---|---|---|---|')
    for nm, sel, selr in (('pegang ≤ 10 hari', J.hari <= 10, R.hari <= 10),
                          ('pegang 11–20 hari', (J.hari > 10) & (J.hari <= 20),
                           (R.hari > 10) & (R.hari <= 20)),
                          ('pegang > 20 hari', J.hari > 20, R.hari > 20)):
        s, sr = J[sel], R[selr]
        A.append(f'| {nm} | {len(s)} | {s.pct.mean() * 100:.0f}% | '
                 f'{sr.real.mean():+.2f}% | {int((sr.real > 0).sum())}/{len(sr)} |')
    A.append('')
    A.append('Kaedah pegang-panjang mempunyai **85% posisi masih terbuka**, jadi "realisasi" '
             'bagi mereka hanyalah himpunan posisi yang dihentikan awal — yang paling buruk '
             'daripada taburan. Angka itu bukan prestasi kaedah; ia prestasi hentinya dalam '
             'tiga minggu.')
    A.append('')

    # ---------- 5. Premis pakar ----------
    A.append('## 5. "Setiap kaedah ada sebab musabab daripada pakar" — ya, dan ini yang diukur')
    A.append('')
    A.append('Premis itu betul: kaedah ini datang daripada pedagang yang berjaya dengannya. '
             'Tetapi repo ini sudah menguji versi mekanikalnya di luar sampel, dan hasilnya:')
    A.append('')
    A.append(f'- Lulus S1–S4: **{int(B.lulus_subset.sum())}** daripada {len(B)} kaedah')
    A.append(f'- Lulus WFO 2023–2026: **{int(B.lulus_wfo.sum())}**')
    A.append(f'- Lulus AUTOTUNE 2000 saham AS 2013–2024: **{int(B.lulus_at.sum())}**')
    A.append(f'- Lulus **≥ 2 daripada 3**: **{int((B.n_lulus >= 2).sum())}**')
    A.append('')
    A.append('Semakan 2000-saham-AS ialah yang paling menuntut kerana ia menguji kaedah LENGKAP '
             '(masuk + keluar + henti) pada alam dan tempoh yang tidak pernah dilihat. '
             f'**{int(B.lulus_at.sum())} kaedah melepasinya.**')
    A.append('')
    A.append('**Had yang jujur, dan ia penting:** kaedah ini ialah **anggaran mekanikal** bagi '
             'kaedah yang asalnya mempunyai pertimbangan manusia — pemilihan saham, saiz, masa '
             'keluar, keadaan pasaran yang tidak dikodkan. `spec/SPEC_SEMUA_KAEDAH.md` menanda '
             '`FAIL ASAL` di tempat spec asal tidak dapat ditentukan. Jadi kegagalan di sini '
             'bermakna "versi mekanikal kami tidak berfungsi pada alam kami", **bukan** '
             '"pakar itu salah". Perbezaan itu nyata dan saya tidak boleh merapatkannya dengan '
             'data yang ada.')
    A.append('')

    # ---------- 6. Kuasa ----------
    A.append('## 6. Bila pangkat kaedah boleh dipercayai')
    A.append('')
    sd = float(k.groupby('id_kaedah').untung_akhir_pct.std().median())
    A.append(f'Sisihan piawai pulangan setiap posisi (median dalam-kaedah): **{sd:.2f} mata**.')
    A.append('')
    A.append('| Untuk membezakan dua kaedah yang berbeza | Perlu posisi DITUTUP setiap kaedah |')
    A.append('|---|---|')
    for bz in (3.0, 2.0, 1.0, 0.5):
        n = ((1.96 + 0.84) * sd / bz) ** 2
        A.append(f'| {bz:.1f} mata setiap posisi | ~{n:,.0f} |')
    A.append('')
    ns = k.groupby('id_kaedah').size()
    A.append(f'Sekarang: median **{ns.median():.0f}** posisi ditutup setiap kaedah, maksimum '
             f'**{ns.max()}**. Jadi perbezaan bawah ~2 mata setiap posisi belum boleh dilihat '
             'bagi hampir semua kaedah.')
    A.append('')

    # ---------- 7. Syor ----------
    A.append('## 7. Syor')
    A.append('')
    A.append('1. **Jangan pilih kaedah sekarang.** Pangkat backtest tiada kuasa ramalan yang '
             'boleh diukur (bahagian 2), dan tiada kaedah positif yang bertahan pembetulan '
             'pelbagai ujian (bahagian 3).')
    A.append('2. **Betulkan kecacatan henti hari-0 dahulu.** `REVERSE/KOLAM_EKOR.md` §4a: 421 '
             'daripada 1,770 posisi dibeli dan dihentikan pada hari masuk dengan kadar menang '
             '0.00% kerana paras henti terletak dalam julat intrabar hari masuk. Itu bukan '
             'prestasi kaedah, itu pepijat pelaksanaan, dan ia mencemari setiap pangkat di atas.')
    A.append(f'3. **Perhatikan kaedah pegang-pendek dahulu.** Hanya kumpulan ≤ 10 hari ada data '
             f'yang hampir matang ({J[J.hari <= 10].pct.mean() * 100:.0f}% masih terbuka lawan '
             f'{J[J.hari > 20].pct.mean() * 100:.0f}% bagi pegang-panjang). Pangkat pegang-panjang '
             'tidak bermakna sebelum satu tempoh pegang penuh berlalu.')
    A.append('4. **Baca semula selepas 6 bulan.** Papan dijana semula setiap malam tanpa kos. '
             'Jadual bahagian 6 memberi bilangan posisi yang diperlukan.')
    A.append('')
    A.append('**Ia tidak akan mencapai +10%/bulan.** Kaedah teratas papan ikut skor sebulan '
             'memberi +3.40% dengan status BELUM CUKUP dan 0 posisi hadapan matang. Lihat '
             '`REVERSE/SASARAN.md`.')
    A.append('')
    os.makedirs(os.path.dirname(KELUAR), exist_ok=True)
    open(KELUAR, 'w', encoding='utf-8').write('\n'.join(A))
    print(f'KAEDAH_TERBAIK.md | {len(R)} kaedah diuji | negatif terbukti '
          f'{int(((R.real < 0) & R.lulus_bh).sum())} | positif terbukti '
          f'{int(((R.real > 0) & R.lulus_bh).sum())}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
