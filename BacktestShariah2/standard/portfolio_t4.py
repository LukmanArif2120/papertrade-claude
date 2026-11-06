"""Lorong T4 satu-kaedah: satu portfolio maya 10 slot bagi SETIAP kaedah dalam Lejar Penuh (Mxx + Nxx).

Keputusan pengguna 6 Nov 2026 (audit dashboard v154, Pilihan B + T4; laporan
`reports/Audit dashboard v154 pilih kaedah.md`). Sebabnya: gate G6 kad skor ("adakah kaedah ini,
sebagai PORTFOLIO, mengalahkan SPUS?") memerlukan 126 sesi data hadapan. Jika lorong itu hanya
dibina SELEPAS kaedah dipilih, G6 tidak boleh dinilai sebelum ~April 2028. Membina satu lorong
bagi setiap kaedah SEKARANG bermakna kaedah yang matang pada Jan 2027 sudah ada ~126 sesi
portfolio pada April 2027. Kosnya kecil: enjin `portfolio_slot.bina` yang sama, dijalankan sekali
bagi setiap kaedah.

Peraturan (sama dengan `portfolio_slot.py` supaya lorong boleh dibanding):
  - 10 slot, saiz = min(tunai, ekuiti semalam x 10%), satu posisi setiap saham, kos 0.1% setiap belah.
  - Calon = posisi Lejar kaedah itu SAHAJA, bermula pada belian pertama kaedah itu (tingkap sendiri).
  - Susunan bila isyarat > slot = `rank` kaedah itu sendiri (tinggi dahulu) - iaitu cara kaedah itu
    memang memilih, bukan rawak dan bukan RS.
  - Dua lorong keluar dikira berasingan:
      L1 = lorong KAEDAH (keluar lorong 1 Lejar). Ini lorong yang G6 nilai, kerana pilihan keluar
           ~12x lebih berpengaruh daripada masuk (`REVERSE/NXX_KELUAR.md`) - bagi Nxx keluar IALAH
           sebahagian kaedah (N19X13 = keluar X13), jadi menukar keluar bermakna menukar kaedah.
      L2 = lorong 2 Chandelier 4xATR14 (maklumat sahaja).
  - Kawalan: 20 cabutan RAWAK_10 atas SELURUH kolam Lejar (semua keluarga), lorong kaedah, dari
    belian pertama Lejar. Setiap lorong dibanding dengan jalur yang DIASAS SEMULA pada tarikh
    mula lorong itu (ekuiti jalur pada tutup sesi sebelumnya = 1.0), kerana setiap lorong
    bermula pada tarikh berbeza (`laporan/BANDING_SPUS.md` peraturan 2: tingkap sendiri).
  - SPUS: asas = BUKA sesi pertama lorong (peraturan 1), MDD termasuk asas 1.0 (peraturan 3).
  - Campuran T4 (teras SPUS + satelit kaedah L1) pada tiga berat 80/20, 70/30, 50/50, diimbang
    semula pada sesi pertama setiap bulan kalendar. Keputusan pengguna: papar ketiga-tiga berat;
    pilihan berat ditangguh sehingga G6 lulus (nisbah CAGR/MDD SPUS+tunai hampir pemalar merentas
    berat, `REVERSE/SISTEM.md`, jadi ia soalan toleransi drawdown, bukan soalan data).

Skrip ini MENGUKUR sahaja. Ambang G6 (sesi >= 126, persentil > 95, MDD >= -26.82%) dikunci dalam
`standard/kad_skor.py`, satu tempat, supaya ia tidak boleh dilonggarkan di sini tanpa ujian gagal.

Rekod sahaja: tiada order, tiada wang sebenar. Jangan ubah fail keluaran secara manual.
  python3 BacktestShariah2/standard/portfolio_t4.py   (dijalankan oleh analisis.yml selepas Lejar)
Keluaran: portfolio_slot/t4_ringkasan.csv, portfolio_slot/t4_siri.csv, laporan/T4_KAEDAH.md
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BS2 = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(BS2, 'kod')); sys.path.insert(0, HERE)
import portfolio_slot as ps  # noqa: E402
from stor import muat, frames_dict  # noqa: E402

STOR = ps.STOR
KELUAR = ps.KELUAR
SPUS = os.environ.get('SPUS_HARIAN', os.path.join(BS2, 'data', 'penanda_aras', 'spus_harian.csv'))
MD = os.environ.get('T4_MD', os.path.join(BS2, 'laporan', 'T4_KAEDAH.md'))
BERAT = (0.8, 0.7, 0.5)          # pecahan SPUS dalam campuran T4
LORONG = {'L1': 'kaedah', 'L2': 'henti'}
N_JALUR = 20


def calon():
    """Semua posisi Lejar yang dibeli (semua keluarga), dengan medan yang bina() perlukan."""
    import lejar
    T, O = lejar.semua_posisi()
    P = pd.concat([T, O], ignore_index=True)
    P = P[(P.tarikh_beli != '') & (P.harga_beli != '')].copy()
    P['harga_beli'] = P.harga_beli.astype(float)
    P['keluar'] = P.keluar_henti.astype(str).str.lower().eq('true') & P.tarikh_keluar_henti.ne('')
    P['harga_keluar_henti'] = pd.to_numeric(P.harga_keluar_henti, errors='coerce')
    P['harga_keluar1'] = pd.to_numeric(P.harga_keluar, errors='coerce')
    P['keluar1'] = P.tarikh_keluar.ne('') & P.harga_keluar1.notna()
    P['rs'] = np.nan
    return P.sort_values(['tarikh_beli', 'saham', 'id_kaedah']).reset_index(drop=True)


def lorong_kaedah(P, mid, lor, hari, tutup):
    """(posisi, ekuiti) lorong satu-kaedah. hari = sesi stor; tingkap bermula belian pertama kaedah."""
    Q = P[P.id_kaedah == mid]
    if Q.empty:
        return None, pd.DataFrame(columns=['tarikh', 'ekuiti', 'tunai', 'bil_posisi'])
    cfg = dict(mula=Q.tarikh_beli.min(), kuota={mid: ps.SLOT}, lorong={mid: lor}, susun='RANK')
    return ps.bina(Q, 'T4', hari, tutup, cfg)


def jalur(P, hari, tutup, n=N_JALUR):
    """{benih: Series ekuiti} - RAWAK_10 atas seluruh kolam, lorong kaedah, kawalan bagi L1."""
    ids = sorted(P.id_kaedah.unique())
    cfg = dict(mula=P.tarikh_beli.min(), kuota={i: ps.SLOT for i in ids}, lorong={i: 'kaedah' for i in ids},
               susun='RAWAK_10')
    out = {}
    for b in range(1, n + 1):
        _, E = ps.bina(P, 'RAWAK_10', hari, tutup, cfg, benih=b)
        if len(E):
            out[b] = pd.Series(E.ekuiti.to_numpy(), index=E.tarikh.to_numpy())
    return out


def asas_semula(s, t0):
    """Ekuiti s diasas semula supaya tutup sesi SEBELUM t0 = 1.0 (lorong bermula pada buka t0)."""
    sebelum = s[s.index < t0]
    b = float(sebelum.iloc[-1]) if len(sebelum) else 1.0
    return s[s.index >= t0] / b


def muat_spus(path=SPUS):
    if not os.path.exists(path):
        return None
    d = pd.read_csv(path, comment='#')
    d['tarikh'] = pd.to_datetime(d.tarikh).dt.strftime('%Y-%m-%d')
    return d.sort_values('tarikh').set_index('tarikh')[['buka', 'tutup']].astype(float)


def siri_spus(S, tarikh):
    """Siri SPUS sepanjang `tarikh` (senarai sesi lorong), asas = BUKA sesi pertama. None jika tiada asas."""
    if S is None or not len(tarikh) or tarikh[0] not in S.index:
        return None
    t = S.tutup.reindex(sorted(set(S.index) | set(tarikh))).ffill().reindex(tarikh)
    return t / float(S.buka.loc[tarikh[0]])


def mdd(x):
    return ps.mdd(np.asarray(x, float)) * 100


def campur(e_l, e_s, w):
    """Ekuiti campuran w SPUS + (1-w) lorong, imbang semula sesi pertama setiap bulan kalendar.

    e_l, e_s: Series berindeks tarikh 'YYYY-MM-DD', kedua-duanya berasas 1.0 pada buka sesi pertama."""
    hs, hl = w, 1.0 - w
    ps_, pl_ = 1.0, 1.0
    bulan = None
    out = []
    for d, vl, vs in zip(e_l.index, e_l.to_numpy(), e_s.to_numpy()):
        m = d[:7]
        if bulan is not None and m != bulan:      # imbang semula pada buka-ish (guna tutup semalam)
            v = hs + hl
            hs, hl = v * w, v * (1.0 - w)
        bulan = m
        hs *= vs / ps_
        hl *= vl / pl_
        ps_, pl_ = vs, vl
        out.append(hs + hl)
    return pd.Series(out, index=e_l.index)


def ukur(E, Sx, J0):
    """Medan ringkasan satu lorong. E: DataFrame ekuiti; Sx: siri SPUS; J0: {benih: Series} jalur (atau None)."""
    if E is None or not len(E):
        return {}
    e = pd.Series(E.ekuiti.to_numpy(), index=E.tarikh.to_numpy())
    d = dict(mula=e.index[0], sesi=int(len(e)), pul=round(100 * (e.iloc[-1] - 1), 4), mdd=round(mdd(e), 4),
             dipegang=int(E.bil_posisi.iloc[-1]), tunai=round(float(E.tunai.iloc[-1]), 4))
    if Sx is not None and len(Sx) and Sx.notna().all():
        d.update(spus=round(100 * (Sx.iloc[-1] - 1), 4), spus_mdd=round(mdd(Sx), 4))
        d['lebih_spus'] = round(d['pul'] - d['spus'], 4)
        for w in BERAT:
            c = campur(e, Sx, w)
            k = f'c{int(round(w * 100))}'
            d[k + '_pul'] = round(100 * (c.iloc[-1] - 1), 4)
            d[k + '_mdd'] = round(mdd(c), 4)
    if J0:
        akhir = np.array([asas_semula(s, e.index[0]).iloc[-1] for s in J0.values()
                          if len(asas_semula(s, e.index[0]))])
        if len(akhir):
            d['jalur_n'] = int(len(akhir))
            d['jalur_p50'] = round(100 * (np.median(akhir) - 1), 4)
            d['jalur_p95'] = round(100 * (np.quantile(akhir, 0.95) - 1), 4)
            d['persentil'] = round(100.0 * float((akhir < e.iloc[-1]).mean()), 1)
    return d


def harga():
    """(senarai sesi 'YYYY-MM-DD', fungsi tutup(saham, tarikh))."""
    fr, idx = frames_dict(muat(STOR))
    ruj = idx.get('SPY')
    if ruj is None:
        return [], None
    hari = [x.strftime('%Y-%m-%d') for x in ruj.index]
    cl = {t: g.close for t, g in fr.items()}
    cache = {}

    def tutup(s, d):
        k = (s, d)
        if k in cache:
            return cache[k]
        c = cl.get(s)
        v = None
        if c is not None:
            x = c.asof(pd.Timestamp(d))
            v = float(x) if pd.notna(x) and x > 0 else None
        cache[k] = v
        return v
    return hari, tutup


def laporan(R, sesi_akhir, n_jalur):
    """Markdown ringkas. Nombor gate dibaca daripada kad_skor (satu tempat), bukan ditulis di sini."""
    import kad_skor as ks
    L1 = R[R.lorong == 'L1']
    A = ['# Lorong T4 satu-kaedah (jejak hadapan; rekod sahaja)', '',
         f'Dijana {pd.Timestamp.now(tz="UTC"):%Y-%m-%d %H:%M} UTC oleh `standard/portfolio_t4.py` '
         '(Actions `analisis.yml`). Tiada order, tiada wang sebenar. Jangan ubah secara manual.', '',
         f'Sesi terakhir {sesi_akhir}. **{L1.id.nunique()} kaedah**, setiap satu dua lorong (L1 = keluar kaedah, '
         f'L2 = Chandelier 4xATR14). Kawalan: {n_jalur} cabutan rawak 10 slot atas seluruh kolam Lejar, '
         'diasas semula pada tarikh mula setiap lorong. Penanda aras: SPUS, asas buka sesi pertama.', '',
         '## Gate G6 (dikunci dalam `standard/kad_skor.py`)', '',
         f'Lorong L1 mesti: sesi >= {ks.G6_SESI}; pulangan > SPUS tingkap sama; pulangan > persentil '
         f'{ks.G6_PERSENTIL} jalur rawak; MDD >= {ks.G6_MDD}%. ']
    lulus = [r for r in L1.to_dict('records') if ks.g6(r)[0]]
    maks = int(L1.sesi.max()) if len(L1) else 0
    A += [f'**{len(lulus)} lulus.** Lorong paling lama ada {maks} sesi; G6 tidak boleh lulus sebelum '
          f'{ks.G6_SESI} sesi (anggaran {ks.tarikh_sesi(sesi_akhir, ks.G6_SESI - maks)}).', '',
          '## 15 lorong L1 teratas ikut pulangan (BUKAN pangkat: semuanya BELUM CUKUP sehingga G6 dinilai)', '',
          '| Kaedah | Mula | Sesi | Pul % | MDD % | SPUS % | Lebih SPUS | Persentil jalur | T4 80/20 % | T4 70/30 % | T4 50/50 % |',
          '|---|---|---|---|---|---|---|---|---|---|---|']

    def f(v, fmt='{:+.2f}'):
        return '–' if v is None or (isinstance(v, float) and np.isnan(v)) else fmt.format(v)
    for r in L1.sort_values('pul', ascending=False).head(15).to_dict('records'):
        A.append(f"| `{r['id']}` | {r['mula']} | {r['sesi']} | {f(r.get('pul'))} | {f(r.get('mdd'), '{:.2f}')} | "
                 f"{f(r.get('spus'))} | {f(r.get('lebih_spus'))} | {f(r.get('persentil'), '{:.0f}')} | "
                 f"{f(r.get('c80_pul'))} | {f(r.get('c70_pul'))} | {f(r.get('c50_pul'))} |")
    A += ['', '## Cara membaca', '',
          '- Pulangan beberapa sesi ialah hingar. `REVERSE/KEPEKATAN_BENIH.md`: SD pemilihan 4.15 mata/tahun pada 8 slot; '
          'kelebihan 20 mata/tahun perlu ~122 sesi untuk dilihat, 10 mata ~489 sesi (`laporan/BANDING_SPUS.md`).',
          '- Lajur T4 = teras SPUS + satelit kaedah, imbang bulanan. Nisbah CAGR/MDD SPUS+tunai hampir pemalar merentas '
          'berat (`REVERSE/SISTEM.md`), jadi berat ialah soalan toleransi drawdown, bukan soalan data.',
          '- Kawalan rawak diambil daripada SELURUH kolam (Mxx + Nxx), jadi kaedah yang dibeli dalam tingkap menaik '
          'dibanding dengan pemilihan rawak dalam tingkap SAMA, bukan dengan sifar.', '']
    return '\n'.join(A) + '\n'


def main():
    if not os.path.exists(os.path.join(ps.LEJAR, 'terbuka.csv')):
        print('portfolio_t4: lejar/terbuka.csv tiada; tiada apa untuk dibina', file=sys.stderr)
        return 0
    P = calon()
    hari, tutup = harga()
    if P.empty or not hari:
        print('portfolio_t4: tiada calon atau sesi stor', file=sys.stderr)
        return 0
    hari = [d for d in hari if d >= P.tarikh_beli.min()]
    S = muat_spus()
    J = jalur(P, hari, tutup)
    baris, siri = [], {}
    for mid in sorted(P.id_kaedah.unique()):
        for kod, lor in LORONG.items():
            R, E = lorong_kaedah(P, mid, lor, hari, tutup)
            if E is None or not len(E):
                continue
            Sx = siri_spus(S, list(E.tarikh))
            d = dict(id=mid, lorong=kod, posisi=int(len(R)), keluar=int((R.status == 'Keluar').sum()))
            d.update(ukur(E, Sx, J if kod == 'L1' else None))
            baris.append(d)
            siri[f'{mid}|{kod}'] = pd.Series(E.ekuiti.round(5).to_numpy(), index=E.tarikh.to_numpy())
    for b, s in J.items():
        siri[f'JALUR_{b:02d}'] = s.round(5)
    R = pd.DataFrame(baris)
    os.makedirs(KELUAR, exist_ok=True)
    R.to_csv(os.path.join(KELUAR, 't4_ringkasan.csv'), index=False)
    W = pd.DataFrame(siri).reindex(hari)
    W.index.name = 'tarikh'
    W.to_csv(os.path.join(KELUAR, 't4_siri.csv'), float_format='%.5f')
    os.makedirs(os.path.dirname(MD), exist_ok=True)
    open(MD, 'w', encoding='utf-8').write(laporan(R, hari[-1], len(J)))
    L1 = R[R.lorong == 'L1']
    print(f'T4_KAEDAH.md | {L1.id.nunique()} kaedah x 2 lorong | jalur {len(J)} | sesi maks {int(L1.sesi.max())}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
