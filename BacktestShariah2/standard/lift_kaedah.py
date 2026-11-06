"""Lift setiap kaedah atas kolam Lejar Penuh — ukuran yang tidak dicemari penapisan keluar.

Soalan pengguna 6 Nov 2026: "ada banyak method, perlukan satu mechanism yang measure setiap
method ni one by one dan compare each other". Mekanisme itu sudah ada tiga lapis (Lejar Penuh =
setiap isyarat setiap kaedah dibeli dengan peraturan sama; `laporan/PENGANALISIS.md` = pangkat
gabungan; `laporan/KAEDAH_TERBAIK.md` = ujian statistik setiap kaedah). Skrip ini menambah lapisan
yang tiada, dan sebabnya ialah DUA kecacatan ukuran yang diukur pada 6 Nov 2026:

1. PENAPISAN KELUAR. `KAEDAH_TERBAIK.md` menguji posisi DITUTUP sahaja, tetapi peraturan keluar
   itu sendiri memilih posisi mana ditutup dahulu, jadi sampel "ditutup" bukan sampel rawak bagi
   dagangan kaedah — dan arah biasnya BERTENTANGAN antara dua jenis keluar:
     M82 sasaran 10%      ditutup 122 +4.19% (menang 61%)  | terbuka 359 -0.57%
     M15 henti ATR ketat  ditutup 108 -4.18% (menang 6.5%) | terbuka 130 +9.48%
     M33 Supertrend+SMA10 ditutup  23 -10.27% (menang 4.3%)| terbuka 133 +7.66%
   Kaedah bersasaran keluar awal bila MENANG; kaedah berhenti ketat keluar awal bila RUGI. Jadi
   purata-ditutup memberi tanda yang salah pada kedua-dua hujung. Ubatnya: nilai SEMUA posisi,
   dengan yang terbuka ditanda-ke-pasaran pada tutup terakhir stor.

2. ARAH PASARAN. Purata tanda-ke-pasaran lawan SIFAR hanya memberitahu ke mana pasaran bergerak
   dalam tingkap itu: pada 6 Nov 2026 ia menunjukkan 17 daripada 180 kaedah "positif", dan
   KESEMUANYA hilang sebaik hari beli dipadankan. Ubatnya: lift atas kolam, dipadan ikut
   (hari beli x baldi hari pegang) — hari beli membuang arah pasaran, baldi hari pegang membuang
   kesan lebar henti (kaedah berhenti lebar memegang lebih lama, jadi dalam pasaran menaik ia
   mengumpul lebih banyak pulangan tanpa apa-apa kemahiran memilih saham).

Asas lift dikira TINGGAL-SATU-KAEDAH-KELUAR: baris kaedah itu sendiri dibuang daripada purata
selnya. Tanpa itu kaedah besar mencairkan asasnya sendiri dan liftnya ditarik ke sifar secara
mekanikal (kesan sel degenerat yang sama seperti `REVERSE/SEMAKAN_LATIH.md` dapati pada A3xU02).

Berbeza daripada Papan Penganalisis: papan memberi SKOR (backtest + hadapan) dan hanya boleh
memangkat Mxx kerana Nxx tiada backtest set 431. Skrip ini tidak memakai backtest sama sekali,
jadi ia memangkat kesemua 222 kaedah (Mxx + Nxx + GBxx) atas data hadapan sahaja, pada paksi yang
sama. Ia TIDAK menggantikan papan; ia menjawab soalan berbeza.

HAD YANG MESTI DIBACA BERSAMA SETIAP NOMBOR: Lejar bermula 15 Okt 2026. SD lift setiap hari beli
~3.3 mata, jadi membanding ~180 kaedah serentak perlukan ~224 hari beli (~11 bulan) untuk melihat
lift 1 mata, ~56 (~3 bulan) untuk 2 mata. Sebelum itu jadual ini ialah SENARAI CALON, bukan
pangkat. Lajur `status` mengira ini sendiri supaya ia tidak boleh hanyut dalam teks.

Guna: python3 BacktestShariah2/standard/lift_kaedah.py
Keluaran: BacktestShariah2/laporan/LIFT_KAEDAH.md, BacktestShariah2/data/analisis/lift.json
          (= dokumen db dashboard `analisis/lift`)
"""
import glob
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy import stats

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BS2 = os.path.join(AKAR, 'BacktestShariah2')
LEJAR = os.environ.get('LEJAR_DIR', os.path.join(BS2, 'lejar'))
STOR = os.environ.get('LEJAR_STOR', os.path.join(BS2, 'data', 'harga', 'stor'))
MD = os.path.join(BS2, 'laporan', 'LIFT_KAEDAH.md')
JSN = os.path.join(BS2, 'data', 'analisis', 'lift.json')

KOS = 0.2          # 0.1% setiap belah, sama seperti Papan Penganalisis
MIN_N = 30         # posisi minimum sebelum satu kaedah diuji
MIN_KLUSTER = 5    # hari beli berbeza minimum (kluster bagi SE)
Q_FDR = 0.05
BALDI = ([-1, 2, 5, 9, 14, 10**6], ['0-2', '3-5', '6-9', '10-14', '15+'])
# Kuasa: z bagi alpha 5% dua-hujung selepas pembetulan Bonferroni merentas kaedah diuji (anggaran
# konservatif bagi BH), dan z bagi kuasa 80%.
Z_KUASA = 0.8416


def posisi():
    """Semua posisi Lejar Penuh (terbuka.csv + tutup/*.csv). Lorong 1."""
    f = [os.path.join(LEJAR, 'terbuka.csv')] + sorted(glob.glob(os.path.join(LEJAR, 'tutup', '*.csv')))
    P = pd.concat([pd.read_csv(x) for x in f if os.path.exists(x)], ignore_index=True)
    P['tarikh_keluar'] = P.tarikh_keluar.fillna('').astype(str)
    return P


def harga_akhir():
    """(tutup terakhir setiap ticker, indeks sesi stor)."""
    f = [os.path.join(STOR, x) for x in ('harga_A.csv', 'harga_B.csv')]
    H = pd.concat([pd.read_csv(x, usecols=['ticker', 'date', 'close'])
                   for x in f if os.path.exists(x)], ignore_index=True)
    H['date'] = H.date.astype(str)
    sesi = sorted(H.date.unique())
    return H.sort_values('date').groupby('ticker').close.last(), {d: i for i, d in enumerate(sesi)}, sesi


def nilai(P, akhir, idx):
    """Pulangan setiap posisi: tutup = untung akhir, terbuka = ditanda-ke-pasaran. Tolak kos."""
    P = P.copy()
    P['untung_pct'] = pd.to_numeric(P.untung_pct, errors='coerce')
    P['hari'] = pd.to_numeric(P.hari, errors='coerce')
    P['terbuka'] = P.tarikh_keluar == ''
    beli = pd.to_numeric(P.harga_beli, errors='coerce')
    kini = (P.saham.map(akhir) / beli - 1) * 100
    P['pul'] = np.where(P.terbuka, kini, P.untung_pct) - KOS
    hb = P.tarikh_beli.astype(str).str.replace('-', '', regex=False).map(idx)
    P['hari_pegang'] = np.where(P.terbuka, max(idx.values()) - hb, P.hari).astype(float)
    P = P.dropna(subset=['pul', 'hari_pegang']).copy()
    P['baldi'] = pd.cut(P.hari_pegang, BALDI[0], labels=BALDI[1])
    return P


def lift_tsk(P, kunci):
    """Lift tinggal-satu-kaedah-keluar: pul - purata sel TANPA baris kaedah itu sendiri.

    Tanpa pengecualian itu, kaedah yang menguasai selnya mencairkan asasnya sendiri dan liftnya
    ditarik ke sifar secara mekanikal, bukan kerana ia tiada kelebihan.
    """
    g = P.groupby(kunci, observed=True).pul
    jum_sel, bil_sel = g.transform('sum'), g.transform('size')
    gm = P.groupby(kunci + ['id_kaedah'], observed=True).pul
    jum_km, bil_km = gm.transform('sum'), gm.transform('size')
    baki = bil_sel - bil_km
    return np.where(baki > 0, P.pul - (jum_sel - jum_km) / baki.replace(0, np.nan), np.nan)


def uji(P, kunci):
    """Satu baris setiap kaedah: lift, t berkelompok ikut hari beli, BH-FDR."""
    D = P.assign(lift=lift_tsk(P, kunci)).dropna(subset=['lift'])
    baris = []
    for mid, g in D.groupby('id_kaedah'):
        if len(g) < MIN_N:
            continue
        kl = g.groupby('tarikh_beli').lift.mean()
        if len(kl) < MIN_KLUSTER:
            continue
        m = float(g.lift.mean())
        se = float(kl.std(ddof=1)) / np.sqrt(len(kl))
        if not se > 0:
            continue
        t = m / se
        hp = float(g.hari_pegang[g.hari_pegang > 0].median())
        baris.append(dict(id=mid, n=len(g), tutup=int((~g.terbuka).sum()),
                          buka_pct=float(g.terbuka.mean() * 100), hari_beli=len(kl),
                          pul=float(g.pul.mean()), lift=m, hari=hp,
                          sebulan=(m / hp * 21) if hp and hp > 0 else np.nan,
                          menang=float((g.pul > 0).mean() * 100), t=t,
                          p=float(2 * (1 - stats.t.cdf(abs(t), len(kl) - 1)))))
    if not baris:
        return pd.DataFrame(columns=['n', 'tutup', 'buka_pct', 'hari_beli', 'pul', 'lift', 'hari',
                                     'sebulan', 'menang', 't', 'p', 'bh', 'lulus'],
                            index=pd.Index([], name='id'))
    R = pd.DataFrame(baris).set_index('id').sort_values('p')
    R['bh'] = Q_FDR * np.arange(1, len(R) + 1) / len(R)
    R['lulus'] = R.p <= R.bh
    return R


def hari_perlu(sd, m, lift):
    """Hari beli berbeza untuk melihat `lift` mata pada kuasa 80%, Bonferroni merentas m kaedah."""
    z = stats.norm.ppf(1 - Q_FDR / max(m, 1) / 2)
    return float(np.ceil((z + Z_KUASA) ** 2 * sd * sd / lift / lift))


def nama_kaedah():
    """Nama setiap ID. Mxx daripada ringkasan Lejar; Nxx/GBxx dibina `masuk → keluar` daripada
    `data/registry_N.csv`, kerana ringkasan Lejar meninggalkan namanya kosong (Nxx tiada
    backtest set 431, jadi `lejar.jangkaan()` tidak menemuinya)."""
    out = {}
    f = os.path.join(LEJAR, 'ringkasan.json')
    if os.path.exists(f):
        out = {r['id']: (r.get('nama') or '')
               for r in json.load(open(f, encoding='utf-8')).get('kaedah', [])}
    reg = os.path.join(BS2, 'data', 'registry_N.csv')
    if os.path.exists(reg):
        import csv
        N = {r['id']: (r.get('nama') or '') for r in csv.DictReader(open(reg, encoding='utf-8'))}
        for mid in list(out):
            if out[mid]:
                continue
            m = re.fullmatch(r'(N\d+|GB\d+\w*?)(X\d+)', mid)
            if m and N.get(m.group(1)):
                out[mid] = f'{N[m.group(1)]} → {N.get(m.group(2), m.group(2))}'
            elif N.get(mid):
                out[mid] = N[mid]
    return out


def status(hari_beli, perlu2):
    return 'BELUM CUKUP' if hari_beli < perlu2 else 'BOLEH DIBACA'


def main():
    if not os.path.exists(os.path.join(LEJAR, 'terbuka.csv')):
        print('lift_kaedah: lejar/terbuka.csv tiada; tiada apa untuk diukur', file=sys.stderr)
        return 0
    akhir, idx, sesi = harga_akhir()
    P = nilai(posisi(), akhir, idx)
    nm = nama_kaedah()
    st = json.load(open(os.path.join(LEJAR, 'status.json'), encoding='utf-8')) \
        if os.path.exists(os.path.join(LEJAR, 'status.json')) else {}

    RA = uji(P, ['tarikh_beli'])                   # padan hari beli sahaja
    RB = uji(P, ['tarikh_beli', 'baldi'])          # + baldi hari pegang (utama)
    # SD lift setiap hari beli, untuk jadual kuasa
    D = P.assign(lift=lift_tsk(P, ['tarikh_beli', 'baldi'])).dropna(subset=['lift'])
    sds = [float(g.groupby('tarikh_beli').lift.mean().std(ddof=1))
           for _, g in D.groupby('id_kaedah') if g.tarikh_beli.nunique() >= MIN_KLUSTER]
    sd = float(np.median(sds)) if sds else float('nan')
    nhb = int(P.tarikh_beli.nunique())
    perlu2 = hari_perlu(sd, len(RB), 2.0) if sds and len(RB) else float('inf')
    RB = RB.assign(status=[status(h, perlu2) for h in RB.hari_beli])

    posB = RB[(RB.lift > 0) & RB.lulus]
    negB = RB[(RB.lift < 0) & RB.lulus]
    # Lawan sifar: untuk menunjukkan berapa banyak yang hilang sebaik hari beli dipadankan
    nol = []
    for mid, g in P.groupby('id_kaedah'):
        if len(g) < MIN_N or g.tarikh_beli.nunique() < MIN_KLUSTER:
            continue
        kl = g.groupby('tarikh_beli').pul.mean()
        se = float(kl.std(ddof=1)) / np.sqrt(len(kl))
        if se > 0:
            t = float(g.pul.mean()) / se
            nol.append((mid, float(g.pul.mean()), float(2 * (1 - stats.t.cdf(abs(t), len(kl) - 1)))))
    N0 = pd.DataFrame(nol, columns=['id', 'pul', 'p']).set_index('id').sort_values('p')
    if len(N0):
        N0['bh'] = Q_FDR * np.arange(1, len(N0) + 1) / len(N0)
        N0['lulus'] = N0.p <= N0.bh
        nol_pos = int(((N0.pul > 0) & N0.lulus).sum())
    else:
        nol_pos = 0

    A = ['# Lift setiap kaedah atas kolam Lejar Penuh', '']
    A.append(f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh '
             '`standard/lift_kaedah.py` (Actions `analisis.yml`, selepas Lejar Penuh). '
             'Rekod analisis sahaja: tiada order, tiada wang sebenar.')
    A.append('')
    A.append(f'Lejar bermula {st.get("mula")}; sesi terakhir {st.get("sesi_terakhir")} '
             f'({nhb} hari beli berbeza). **{len(P):,} posisi** merentas '
             f'**{P.id_kaedah.nunique()} kaedah** (Mxx + Nxx), '
             f'{int((~P.terbuka).sum()):,} tutup lorong 1 dan {int(P.terbuka.sum()):,} terbuka '
             f'ditanda-ke-pasaran pada tutup {sesi[-1]}. Kos {KOS}% setiap pusingan ditolak.')
    A.append('')
    A.append('## Mengapa ukuran ini ada')
    A.append('')
    A.append('`laporan/KAEDAH_TERBAIK.md` menguji posisi **DITUTUP** sahaja, dan peraturan keluar '
             'itu sendiri memilih posisi mana ditutup dahulu — jadi arah biasnya bertentangan '
             'antara dua jenis keluar: kaedah ber**sasaran untung** keluar awal bila MENANG '
             '(purata ditutup terlebih tinggi), kaedah ber**henti ketat** keluar awal bila RUGI '
             '(terlebih rendah). Ukuran di sini menilai SEMUA posisi, jadi penapisan itu hilang.')
    A.append('')
    A.append('Tetapi purata tanda-ke-pasaran lawan **sifar** hanya mengukur arah pasaran dalam '
             f'tingkap itu: **{nol_pos} daripada {len(N0)}** kaedah kelihatan positif pada ujian '
             'itu. Jadi lajur utama di bawah ialah **lift atas kolam**, dipadan ikut '
             '**hari beli × baldi hari pegang** — hari beli membuang arah pasaran, baldi hari '
             'pegang membuang kesan lebar henti. Asas setiap sel dikira '
             '**tinggal-satu-kaedah-keluar** supaya kaedah besar tidak mencairkan asasnya sendiri.')
    A.append('')
    A.append('## Keputusan')
    A.append('')
    A.append('| Ujian | Diuji | Lift positif bertahan BH-FDR | Lift negatif bertahan |')
    A.append('|---|---|---|---|')
    A.append(f'| Lawan sifar (tiada padanan) | {len(N0)} | {nol_pos} | '
             f'{int(((N0.pul < 0) & N0.lulus).sum()) if len(N0) else 0} |')
    A.append(f'| Lift, padan hari beli | {len(RA)} | {int(((RA.lift > 0) & RA.lulus).sum())} | '
             f'{int(((RA.lift < 0) & RA.lulus).sum())} |')
    A.append(f'| **Lift, padan hari beli × baldi hari pegang** | **{len(RB)}** | '
             f'**{len(posB)}** | **{len(negB)}** |')
    A.append('')
    if len(posB):
        A.append(f'**{len(posB)} kaedah mempunyai lift positif yang bertahan BH-FDR** pada ujian '
                 'utama. Senarai penuh di bawah; baca lajur `% terbuka` sebelum mempercayainya.')
    else:
        A.append('**Tiada kaedah mempunyai lift positif yang bertahan BH-FDR** pada ujian utama. '
                 'Jadual di bawah ialah senarai CALON, bukan pangkat yang boleh dipilih.')
    A.append('')

    A.append('## 20 calon teratas ikut lift (padan hari beli × baldi hari pegang)')
    A.append('')
    A.append('| # | Kaedah | n | % terbuka | Hari beli | Pul % | **Lift mata** | Lift/bulan % | '
             'Hari | Menang % | t | p | Ambang BH | BH | Status |')
    A.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for i, (mid, r) in enumerate(RB[RB.n >= 50].sort_values('lift', ascending=False).head(20).iterrows(), 1):
        A.append(f'| {i} | `{mid}` {str(nm.get(mid, ""))[:34]} | {r.n:.0f} | {r.buka_pct:.0f}% | '
                 f'{r.hari_beli:.0f} | {r.pul:+.2f} | **{r.lift:+.2f}** | {r.sebulan:+.1f} | '
                 f'{r.hari:.0f} | {r.menang:.0f} | {r.t:+.2f} | {r.p:.4f} | {r.bh:.4f} | '
                 f'{"lulus" if r.lulus else "tidak"} | {r.status} |')
    A.append('')
    A.append(f'Disekat kepada n ≥ 50 posisi. `Lift/bulan` = lift ÷ hari pegang × 21, iaitu lift '
             'setiap posisi jika modal dipusing penuh — ia **bukan** pulangan portfolio, dan '
             'setiap kali repo ini menukar jangkaan setiap-dagangan kepada portfolio sebenar ia '
             'jatuh ke bawah indeks (`REVERSE/KEPUTUSAN_AKHIR.md`: 0/24 lulus).')
    A.append('')

    if len(negB):
        A.append('## Lift NEGATIF yang bertahan BH-FDR')
        A.append('')
        A.append('| Kaedah | n | % terbuka | Lift mata | Hari | Menang % | t | p |')
        A.append('|---|---|---|---|---|---|---|---|')
        for mid, r in negB.sort_values('lift').iterrows():
            A.append(f'| `{mid}` {str(nm.get(mid, ""))[:34]} | {r.n:.0f} | {r.buka_pct:.0f}% | '
                     f'{r.lift:+.2f} | {r.hari:.0f} | {r.menang:.0f} | {r.t:+.2f} | {r.p:.4f} |')
        A.append('')
        A.append('Ini lebih berguna daripada senarai positif: `GB08` (penapis terbalik) ialah '
                 'paksi yang memerlukan senarai buang, dan senarai ini dibina daripada data '
                 'hadapan, bukan backtest.')
        A.append('')

    A.append('## Bila jadual ini boleh dipercayai')
    A.append('')
    A.append(f'SD lift setiap hari beli (median dalam-kaedah): **{sd:.2f} mata**. Membanding '
             f'{len(RB)} kaedah serentak (Bonferroni, anggaran konservatif bagi BH):')
    A.append('')
    A.append('| Lift benar | Hari beli diperlukan | Setara bulan dagangan |')
    A.append('|---|---|---|')
    for d in (1.0, 2.0, 3.0, 4.0):
        h = hari_perlu(sd, len(RB), d)
        A.append(f'| {d:.0f} mata | {h:,.0f} | ~{np.ceil(h / 21):.0f} |')
    A.append('')
    A.append(f'**Sekarang ada {nhb} hari beli.** Lajur `status` menanda `BELUM CUKUP` bagi '
             f'kaedah dengan hari beli di bawah {perlu2:,.0f} (ambang lift 2 mata). Angka ini '
             'dikira setiap larian supaya ia tidak boleh hanyut dalam teks.')
    A.append('')
    A.append('## Had')
    A.append('')
    A.append('- Tingkap Lejar pendek, dan kaedah pegang-panjang mempunyai majoriti posisi masih '
             'terbuka. Lift mereka ialah untung kertas, bukan hasil.')
    A.append('- Paksi CARA dikunci `C01` (beli pada buka esok), jadi kecacatan henti hari-0 '
             '(`REVERSE/KOLAM_EKOR.md` §4a) hadir dalam setiap nombor.')
    A.append('- Alam Lejar tiada saham delist sebelum tingkap ini, jadi ia bukan alam '
             'titik-masa yang kausal (`REVERSE/ALAM.md`).')
    A.append('- Lift diukur atas kolam Lejar, bukan atas SPUS. Penanda aras pulangan yang sah '
             'ialah SPUS (`REVERSE/PENANDA_ARAS_SYARIAH.md`), dan itu perbandingan portfolio '
             '(`laporan/BANDING_SPUS.md`), bukan perbandingan setiap dagangan.')
    A.append('- Sasaran +10%/bulan: lihat `REVERSE/SASARAN.md`. Ia tidak dicapai oleh mana-mana '
             'baris di atas, dan lajur `Lift/bulan` tidak boleh dibaca sebagai pulangan bulanan.')
    A.append('')

    os.makedirs(os.path.dirname(MD), exist_ok=True)
    open(MD, 'w', encoding='utf-8').write('\n'.join(A))

    kol = ['n', 'tutup', 'buka_pct', 'hari_beli', 'pul', 'lift', 'hari', 'sebulan', 'menang',
           't', 'p', 'bh', 'lulus', 'status']
    rows = []
    for mid, r in RB.sort_values('lift', ascending=False).iterrows():
        d = dict(id=mid, nama=nm.get(mid, ''))
        for c in kol:
            v = r[c]
            d[c] = (bool(v) if c == 'lulus' else v if isinstance(v, str) else
                    (None if pd.isna(v) else round(float(v), 4)))
        rows.append(d)
    os.makedirs(os.path.dirname(JSN), exist_ok=True)
    json.dump(dict(kini=str(pd.Timestamp.now(tz='UTC').date()), mula=st.get('mula'),
                   sesi_terakhir=st.get('sesi_terakhir'), harga_pada=sesi[-1],
                   posisi=int(len(P)), kaedah=int(P.id_kaedah.nunique()), hari_beli=nhb,
                   kos=KOS, sd_lift=round(sd, 4), perlu_2mata=None if not np.isfinite(perlu2) else int(perlu2),
                   diuji=int(len(RB)), positif=int(len(posB)), negatif=int(len(negB)),
                   positif_lawan_sifar=nol_pos, rows=rows),
              open(JSN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'LIFT_KAEDAH.md | {len(P)} posisi | {len(RB)} kaedah diuji | lift positif {len(posB)} | '
          f'negatif {len(negB)} | lawan sifar positif {nol_pos} | {nhb} hari beli')
    return 0


if __name__ == '__main__':
    sys.exit(main())
