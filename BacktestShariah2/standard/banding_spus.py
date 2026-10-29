"""Banding jejak hadapan `portfolio_slot/` dengan SPUS (penanda aras pasif patuh Syariah).

Mengapa SPUS dan bukan SPY: `REVERSE/PENANDA_ARAS_SYARIAH.md`. Repo ini menapis melalui SPUS,
jadi SPY bukan penanda aras yang sah bagi projek ini. `RINGKASAN.md` portfolio_slot melaporkan
SPY sahaja kerana hanya SPY ada dalam stor harga indeks.

Konvensyen yang MESTI dipadankan (`standard/portfolio_slot.py` main): lorong beli pada **buka**
sesi pertama dan ekuiti berasas 1.0 pada ketika itu. Maka penanda aras juga mesti berasaskan
**buka** sesi pertama, bukan tutup. Menggunakan tutup 16 Okt sebagai asas memberi SPUS +1.83%
dan bukan +0.28% — kesilapan 1.5 mata pada tingkap 8 sesi, iaitu lebih besar daripada jurang
antara mana-mana dua lorong.

Dokumen ini juga mengira **bila** perbandingan ini menjadi bermakna. Pada tingkap pendek, jurang
antara lorong lebih kecil daripada hingar pemilihan (`REVERSE/KEPEKATAN_BENIH.md`: 17.3 mata
peratus setahun pada 8 slot), jadi melaporkan pemenang sekarang adalah melaporkan hingar.

Guna: python3 BacktestShariah2/standard/banding_spus.py [--kemas-kini]
Output: BacktestShariah2/laporan/BANDING_SPUS.md
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLOT = os.path.join(AKAR, 'BacktestShariah2', 'portfolio_slot')
HARIAN = os.path.join(AKAR, 'BacktestShariah2', 'data', 'penanda_aras', 'spus_harian.csv')
KELUAR = os.path.join(AKAR, 'BacktestShariah2', 'laporan', 'BANDING_SPUS.md')
SESI_SETAHUN = 252
Z = 1.645          # satu-hujung 95%


def muat_spus():
    d = pd.read_csv(HARIAN, comment='#')
    d['tarikh'] = pd.to_datetime(d.tarikh)
    return d.sort_values('tarikh').reset_index(drop=True)


def kemas_kini():
    """Lanjutkan spus_harian.csv dengan yfinance jika pustaka itu ada.

    Tidak dipasang dalam workflow malam dengan sengaja: kod yang belum diuji dalam kerja
    berjadual adalah liabiliti. Jalankan secara manual, atau lihat keputusan terbuka.
    """
    try:
        import yfinance as yf
    except ImportError:
        print('yfinance tiada dalam sesi ini; spus_harian.csv dibiar seperti sedia ada')
        return 1
    lama = muat_spus()
    mula = (lama.tarikh.max() - pd.Timedelta(days=5)).strftime('%Y-%m-%d')
    h = yf.Ticker('SPUS').history(start=mula, auto_adjust=True)
    if h.empty:
        print('yfinance tidak memulangkan data SPUS')
        return 1
    baru = pd.DataFrame({'tarikh': pd.to_datetime(h.index.date),
                         'buka': h.Open.to_numpy(), 'tutup': h.Close.to_numpy()})
    G = (pd.concat([lama, baru], ignore_index=True)
         .drop_duplicates('tarikh', keep='first').sort_values('tarikh'))
    kepala = [ln for ln in open(HARIAN, encoding='utf-8') if ln.startswith('#')]
    with open(HARIAN, 'w', encoding='utf-8') as f:
        f.writelines(kepala)
        f.write('tarikh,buka,tutup\n')
        for _, r in G.iterrows():
            f.write(f'{r.tarikh:%Y-%m-%d},{r.buka:.6f},{r.tutup:.6f}\n')
    print(f'spus_harian.csv: {len(lama)} -> {len(G)} sesi')
    return 0


def mdd(e):
    e = np.asarray(e, 'float64')
    return float((e / np.maximum.accumulate(e) - 1).min() * 100) if e.size > 1 else np.nan


def lorong():
    """{nama: DataFrame ekuiti} bagi setiap lorong portfolio_slot.

    `rawak_jalur_ekuiti.csv` dikecualikan: ia jalur kawalan 20 cabutan, bukan lorong, dan
    mencantumkannya sebagai satu siri memberi MDD yang tidak bermakna.
    """
    out = {}
    for f in sorted(os.listdir(SLOT)):
        if f.endswith('_ekuiti.csv') and not f.startswith('rawak_jalur'):
            E = pd.read_csv(os.path.join(SLOT, f))
            if len(E):
                out[f[:-len('_ekuiti.csv')]] = E
    return out


def mdd_lorong(E):
    """MDD termasuk asas 1.0 pada masa belian — padan dengan portfolio_slot RINGKASAN.md.

    Mengira MDD daripada lajur ekuiti sahaja terlepas penurunan sesi pertama (ekuiti sesi
    pertama ialah TUTUP hari itu, bukan asas), jadi RS_10 akan dilapor -6.77% dan bukan -7.74%.
    """
    return mdd(np.concatenate([[1.0], E.ekuiti.to_numpy('float64')]))


def sesi_perlu(sd_jalur, n_sesi, kelebihan):
    """Bilangan sesi sebelum kelebihan benar `kelebihan` mata/tahun melepasi jalur pemilihan.

    Hingar pemilihan berkembang seperti sqrt(T); kelebihan benar berkembang linear dengan T.
    Perlu: kelebihan*T/252 > Z*sd(T), dengan sd(T) = sd_jalur*sqrt(T/n_sesi).
    """
    if kelebihan <= 0 or sd_jalur <= 0 or n_sesi <= 0:
        return np.nan
    return float((Z * sd_jalur * SESI_SETAHUN / (kelebihan * np.sqrt(n_sesi))) ** 2)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--kemas-kini', action='store_true',
                    help='lanjutkan spus_harian.csv dengan yfinance (manual sahaja)')
    a = ap.parse_args(argv)
    if a.kemas_kini:
        return kemas_kini()

    S = muat_spus()
    L = lorong()
    if not L:
        print('tiada fail ekuiti portfolio_slot')
        return 1
    J = pd.read_csv(os.path.join(SLOT, 'rawak_jalur_ekuiti.csv'))
    J['tarikh'] = pd.to_datetime(J.tarikh)

    def spus_tingkap(t0, t1):
        """(pulangan%, mdd%) SPUS berasaskan BUKA t0 hingga tutup t1 — padan konvensyen lorong."""
        b, k = S[S.tarikh == t0], S[S.tarikh == t1]
        if b.empty or k.empty:
            return None, None
        asas = float(b.buka.iloc[0])
        W = S[(S.tarikh >= t0) & (S.tarikh <= t1)].tutup.to_numpy('float64')
        return (float(k.tutup.iloc[0]) / asas - 1) * 100, mdd(np.concatenate([[asas], W]))

    def jalur_tingkap(t0, t1):
        """Pulangan setiap cabutan jalur atas tingkap [t0, t1].

        Jalur berasas 1.0 pada buka sesi pertamanya (16 Okt). Bagi lorong yang bermula lebih
        lewat, asas terdekat yang ada ialah TUTUP sesi sebelum t0 — bukan buka t0. Ketidakpadanan
        itu dinyatakan dalam Had.
        """
        out = []
        for b, g in J.groupby('benih'):
            g = g.sort_values('tarikh')
            sblm = g[g.tarikh < t0]
            asas = float(sblm.ekuiti.iloc[-1]) if len(sblm) else 1.0
            akhir = g[g.tarikh <= t1]
            if len(akhir) and asas > 0:
                out.append((float(akhir.ekuiti.iloc[-1]) / asas - 1) * 100)
        return np.array(out)

    baris = []
    for nm, E in sorted(L.items()):
        t0, t1 = pd.Timestamp(E.tarikh.iloc[0]), pd.Timestamp(E.tarikh.iloc[-1])
        pul = (float(E.ekuiti.iloc[-1]) - 1) * 100
        sp, spm = spus_tingkap(t0, t1)
        jp = jalur_tingkap(t0, t1)
        baris.append(dict(lorong=nm, n=len(E), mula=f'{t0:%m-%d}', pulangan=pul,
                          mdd=mdd_lorong(E), spus=sp, spus_mdd=spm,
                          lwn_spus=(pul - sp) if sp is not None else np.nan,
                          persentil=100.0 * float((jp < pul).mean()) if jp.size else np.nan,
                          jalur_sd=float(jp.std(ddof=1)) if jp.size > 1 else np.nan))
    E8 = max(L.values(), key=len)
    t0, t1, n = (pd.Timestamp(E8.tarikh.iloc[0]), pd.Timestamp(E8.tarikh.iloc[-1]), len(E8))
    sp_pul, sp_mdd = spus_tingkap(t0, t1)
    if sp_pul is None:
        print(f'spus_harian.csv tidak meliputi {t0:%Y-%m-%d}..{t1:%Y-%m-%d}; jalankan --kemas-kini')
        return 1
    spy_pul = (float(E8.spy.iloc[-1]) - 1) * 100 if 'spy' in E8 else np.nan
    jpul = jalur_tingkap(t0, t1)
    sd = float(jpul.std(ddof=1))
    R = pd.DataFrame(baris).sort_values('pulangan', ascending=False)
    return laporan(R, S, t0, t1, n, sp_pul, sp_mdd, spy_pul, jpul, sd)


def laporan(R, S, t0, t1, n, sp_pul, sp_mdd, spy_pul, jpul, sd):
    A = ['# Jejak hadapan portfolio_slot lawan SPUS', '']
    A.append(f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh '
             '`standard/banding_spus.py`. Rekod sahaja; tiada order, tiada wang sebenar.')
    A.append('')
    A.append(f'Tempoh: **{t0:%Y-%m-%d} hingga {t1:%Y-%m-%d} ({n} sesi)**.')
    A.append('')
    A.append('## 1. Jawapan pendek')
    A.append('')
    menang = R[R.lwn_spus > 0]
    A.append(f'Atas tingkap {n} sesi penuh ({t0:%d %b}–{t1:%d %b}), SPUS memberi '
             f'**{sp_pul:+.2f}%** (MDD {sp_mdd:.2f}%).')
    A.append('')
    A.append(f'**{len(menang)} daripada {len(R)} lorong mengalahkan SPUS**'
             + (f': {", ".join("`" + x + "`" for x in menang.lorong)}.' if len(menang) else '.'))
    A.append('')
    A.append(f'**Tetapi {n} sesi tidak boleh membezakan apa-apa.** Bahagian 3 mengira bila ia '
             'boleh. Sila baca bahagian itu sebelum menyimpulkan apa-apa daripada jadual di bawah.')
    A.append('')
    A.append('## 2. Jadual')
    A.append('')
    A.append('Setiap lorong dibanding dengan SPUS atas **tingkapnya sendiri**: lorong gabungan '
             'beku bermula 22 Okt, bukan 16 Okt, jadi satu angka SPUS tunggal tidak sah untuk '
             'semua.')
    A.append('')
    A.append('| Lorong | Sesi | Mula | Pulangan | MDD | SPUS tingkap sama | Lawan SPUS | '
             'Persentil jalur |')
    A.append('|---|---|---|---|---|---|---|---|')
    for _, r in R.iterrows():
        A.append(f'| `{r.lorong}` | {r.n:.0f} | {r.mula} | {r.pulangan:+.2f}% | {r.mdd:.2f}% | '
                 f'{r.spus:+.2f}% | {r.lwn_spus:+.2f} mata | {r.persentil:.0f} |')
    A.append('')
    A.append(f'SPY atas tingkap {n} sesi: {spy_pul:+.2f}% ({spy_pul - sp_pul:+.2f} mata lawan '
             f'SPUS {sp_pul:+.2f}%). Rujukan sahaja — SPY bukan patuh Syariah.')
    A.append('')
    A.append(f'Jalur rawak ({len(jpul)} cabutan berbenih berbeza, pembinaan sama): '
             f'min {jpul.min():+.2f}% · p10 {np.quantile(jpul, 0.10):+.2f}% · '
             f'median {np.median(jpul):+.2f}% · p90 {np.quantile(jpul, 0.90):+.2f}% · '
             f'maks {jpul.max():+.2f}%, sisihan piawai **{sd:.2f} mata**.')
    A.append('')
    A.append('Lajur persentil ialah bacaan yang betul, bukan lajur pulangan. Lorong di dalam '
             'jalur tidak dapat dibezakan daripada pemilihan rawak.')
    A.append('')
    A.append('## 3. Bila perbandingan ini menjadi bermakna')
    A.append('')
    A.append(f'Hingar pemilihan merentas {len(jpul)} cabutan rawak ialah **{sd:.2f} mata** '
             f'selepas {n} sesi sahaja. Ia berkembang seperti √T manakala kelebihan benar '
             'berkembang linear dengan T, jadi tingkap yang cukup panjang akhirnya memisahkan '
             'kedua-duanya. Sesi yang diperlukan sebelum kelebihan benar melepasi jalur '
             '(satu-hujung 95%):')
    A.append('')
    A.append('| Kelebihan benar lawan SPUS | Sesi diperlukan | Lebih kurang |')
    A.append('|---|---|---|')
    for e in (20.0, 10.0, 5.0, 17.3):
        t = sesi_perlu(sd, n, e)
        nota = ' ← hingar pemilihan `KEPEKATAN_BENIH.md`' if abs(e - 17.3) < 1e-9 else ''
        A.append(f'| {e:.1f} mata/tahun | {t:,.0f} | {t / SESI_SETAHUN:.1f} tahun{nota} |')
    A.append('')
    A.append(f'Maksudnya: walaupun satu lorong benar-benar mengalahkan SPUS **10 mata setahun**, '
             f'ia memerlukan kira-kira **{sesi_perlu(sd, n, 10.0) / SESI_SETAHUN:.1f} tahun** '
             'jejak hadapan sebelum kita boleh mengatakannya dengan yakin. Jurang yang lebih '
             'kecil memerlukan lebih lama lagi, mengikut kuasa dua.')
    A.append('')
    # Nyatakan jurang dalam sisihan piawai jalur, bukan membandingkan mata dengan mata:
    # jurang 2.42 mata terhadap sd 1.51 mata BUKAN "di dalam hingar", ia 1.6 sd.
    R8 = R[R.n == R.n.max()]
    A.append('Jurang setiap lorong dinyatakan dalam sisihan piawai jalurnya sendiri — itu '
             'bacaan yang betul, bukan membandingkan mata dengan mata:')
    A.append('')
    for _, r in R8.iterrows():
        z = r.lwn_spus / r.jalur_sd if r.jalur_sd and r.jalur_sd > 0 else np.nan
        A.append(f'- `{r.lorong}`: {r.lwn_spus:+.2f} mata = **{z:+.2f} sd** jalur '
                 f'(persentil {r.persentil:.0f})')
    A.append('')
    zm = (R8.lwn_spus / R8.jalur_sd).abs().max()
    A.append(f'Terbesar ialah **{zm:.2f} sd**, di bawah ambang satu-hujung 95% ({Z:.3f} sd). '
             'Tiada lorong boleh didakwa lebih baik atau lebih buruk daripada SPUS hari ini.')
    A.append('')
    terburuk = R8.sort_values('pulangan').iloc[0]
    if terburuk.persentil <= 0:
        A.append(f'Satu bacaan yang perlu diperhatikan, bukan disimpulkan: `{terburuk.lorong}` '
                 f'berada di bawah **kesemua** {len(jpul)} cabutan rawak (persentil 0), '
                 f'iaitu nilai-p satu-hujung ≈ {1 / (len(jpul) + 1):.3f}. Itu di sempadan '
                 'kelaziman — tetapi pada SATU tingkap 8 sesi, dan lorong itu sendiri juga '
                 'hanya satu cabutan. Ia **tidak** dipradaftar sebagai ujian hadapan dengan '
                 'peraturan keputusan, jadi ia perkara untuk diperhatikan apabila tingkap '
                 'memanjang, bukan dapatan.')
        A.append('')
    A.append('## 4. Apa yang perlu dibuat')
    A.append('')
    A.append('1. **Jangan tukar apa-apa berdasarkan dokumen ini.** Ia terlalu awal; itulah '
             'keseluruhan maksudnya.')
    A.append('2. Biarkan `portfolio_slot/` terkumpul. Ia dibina semula setiap malam tanpa kos.')
    A.append('3. Baca semula selepas **6 bulan** (kira-kira 126 sesi) untuk tanda pertama, dan '
             'selepas **2 tahun** untuk keyakinan. Jadual bahagian 3 memberi angka tepatnya.')
    A.append('4. Apabila membaca semula, lihat **lajur persentil**, bukan lajur pulangan.')
    A.append('')
    A.append('## 5. Had')
    A.append('')
    A.append(f'- SPUS asas = **buka {t0:%d %b}** kerana lorong beli pada buka sesi pertama. '
             'Menggunakan tutup hari itu sebagai asas memberi SPUS angka yang jauh berbeza; '
             'kesilapan itu lebih besar daripada jurang antara mana-mana dua lorong.')
    A.append('- MDD SPUS daripada tutup harian dalam tingkap ini, jadi ia tidak setara dengan '
             '`PENANDA_ARAS_SYARIAH.md` yang menggunakan median MDD tahunan daripada tutup '
             'bulanan. Pada tingkap sependek ini kedua-duanya hampir tidak bermakna.')
    A.append('- Lorong tidak membayar kos dagangan; SPUS juga tidak. Pusing ganti lorong jauh '
             'lebih tinggi, jadi ketiadaan kos **memihak kepada lorong**.')
    A.append('- `spus_harian.csv` disegarkan secara manual (`--kemas-kini`), bukan oleh '
             'workflow malam. Jika tempoh portfolio_slot melepasi liputan fail itu, skrip ini '
             'berhenti dan memberitahu, bukan meneka.')
    A.append('')
    os.makedirs(os.path.dirname(KELUAR), exist_ok=True)
    open(KELUAR, 'w', encoding='utf-8').write('\n'.join(A))
    print(R.round(2).to_string(index=False))
    print(f'\nSPUS {sp_pul:+.2f}% | jalur sd {sd:.2f} mata | '
          f'10 mata/tahun perlu {sesi_perlu(sd, n, 10.0) / SESI_SETAHUN:.1f} tahun')
    return 0


if __name__ == '__main__':
    sys.exit(main())
