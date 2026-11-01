"""Kesatuan N19 u N37 u N115 (GB02_atau3) — kaedah Nxx (kombinasi indikator REVERSE). Jejak hadapan, bukan dakwaan.

Pradaftar jejak: `REVERSE/SPEC_JEJAK_N.md`. Peraturan dan nombor: `REVERSE/registry_N.csv`
dan `REVERSE/silang_akhir.csv`. Formula indikator: `kaedah/_nxx.py` (salinan verbatim
`REVERSE/teras/ind.py`, disahkan bit-identik oleh `ujian/test_nxx_sepadan.py`).

MASUK  : N19 ATAU N37 ATAU N115 — KESATUAN, bukan penapis
CARA   : C01 — beli pada BUKA esok (enjin v1.2 `o[i+1]`)
KELUAR : lorong 1 = X13 (rsi14 > 70 -> jual buka esok) · lorong 2 = X15 Chandelier 4xATR14
HENTI  : TIADA dengan sengaja — `KOLAM_EKOR.md` §4a mengukur henti ketat menghasilkan 421
         daripada 1,770 posisi C yang dibeli DAN dihentikan pada hari masuk dengan kadar
         menang 0.00%. `stop = NaN` menjadikan kecacatan itu mustahil secara struktur.
SASARAN: TIADA — `KOMBINASI.md` mengukur sasaran 1xATR menukar asas +2.595% jadi -0.281%.
TMAX   : 126 bar = ufuk keluar `IMBAS` kajian, jadi tiada dagangan melebihi apa yang diukur.

KONFIGURASI UTAMA. `REVERSE/silang_akhir.csv`: dengan keluar X13 ia memberi
jangkaan tahan +8.541% setiap dagangan, lift +4.191 tahan / +1.818 latih, menang
64.2%, untung purata +25.68%, rugi purata -22.14%, n 195,681, p 0.0068, dan
tanpa5 = +2.858% — POSITIF secara mutlak, lawan asas X13 +0.912%. Itu satu-satunya
konfigurasi dalam seluruh kajian yang kelebihannya BERTAHAN selepas membuang 5%
pemenang teratas, iaitu halangan yang `SETUP.md` dapati 598/598 setup gagal.
Gate0-gate3 LULUS kesemuanya pada kedua-dua tingkap.

HAD YANG MESTI DIBACA BERSAMA: pada peringkat PORTFOLIO ia TIDAK mengalahkan
SPUS — `portfolio_n_ringkas.csv` memberi CAGR 9.3-16.1% dengan MDD -22% hingga
-63% lawan SPUS +17.95% / -26.82%, dan 0 daripada 36 konfigurasi lulus. Jadi ini
dijejak sebagai KOHORT Papertrade C (jangkaan setiap dagangan), BUKAN sebagai
peruntukan modal. Ia mengalahkan kawalan RAWAK dengan keluar X13 (16.12 lawan
14.23 pada 8 slot; 14.74 lawan 4.30 pada 40 slot) — dapatan "isyarat memburukkan"
dalam E4/E5 khusus kepada keluar X15/X32, bukan X13.
Alam kajian = a02 tanpa saham delist; kolam signal dipilih daripada data yang sama,
jadi keputusannya BERSYARAT.
"""
try:                                  # pemuat produksi letak kod/ pada path,
    from kaedah import _nxx as NX     # bukan kod/kaedah/ — ikut preseden _k145
except ImportError:
    import _nxx as NX

ID = 'GB02'
NAMA = 'Kesatuan N19 u N37 u N115 (GB02_atau3)'
VARIAN = 'V1 Nxx pradaftar'
TMAX = NX.IMBAS
WARM = 200
ADA_HENTI = False
SILANG = False
PERLU_BAR = 240


def sedia(fr, idx):
    for g in fr.values():
        f = NX.indikator(g)
        NX.pasang(g, NX.gb02_atau3(f, g))
        g['_rsi14'] = f.rsi14
        g['_bb'] = f.bb_pctb
        g['_adx'] = f.adx14
        g['_vol'] = f.vol_n50


def hampir(g, idx):
    """Kesatuan: "hampir" = tiada kaki tercetus tetapi satu kaki hampir.
    Dilaporkan sebagai kaki yang paling hampir antara N19 / N37 / N115."""
    r = g.iloc[-1]
    if bool(r.sig) or len(g) < 60 or not (r._rsi14 == r._rsi14):
        return None
    kaki = []
    if r._bb == r._bb:
        kaki.append(('N19 (bb_pctb<0 DAN rsi14<30)',
                     max(abs(float(r._bb)) if r._bb >= 0 else 0.0,
                         float(r._rsi14) - 30.0 if r._rsi14 >= 30 else 0.0)))
    if r._vol == r._vol:
        kaki.append(('N37 (gap and go)', (1.5 - float(r._vol)) * 10.0 if r._vol < 1.5 else 0.0))
    if r._adx == r._adx:
        kaki.append(('N115 (Holy Grail)', 30.0 - float(r._adx) if r._adx <= 30 else 0.0))
    kaki = [(n, d) for n, d in kaki if d > 0]
    if not kaki:
        return None
    n, d = min(kaki, key=lambda x: x[1])
    return {'sebab': 'tiada kaki kesatuan tercetus; paling hampir ' + n,
            'syarat_beli': 'N19 ATAU N37 ATAU N115',
            'pencetus': n, 'paras': None, 'jarak_pct': round(float(d), 2),
            'syarat_dipenuhi': '0/1 kaki',
            'skor': round(float(max(0.0, 1.0 - d / 20.0)), 3)}
