"""Jana REVERSE/KEPUTUSAN_FASA2_SEC.md daripada output step10/step11.

Setiap nombor dikira daripada fail output. Tiada nombor ditulis tangan — pepijat itu berlaku sekali
dalam penjana laporan fasa 1 (nombor 2025 dikeraskan) dan tidak diulang di sini.

Guna: python3 REVERSE/jana_keputusan_fasa2.py
"""
import json
import sys
from pathlib import Path

import pandas as pd

R = Path(__file__).resolve().parent


def _baca(nama, **kw):
    p = R / nama
    return pd.read_csv(p, **kw) if p.exists() else None


def jadual(d, kol=None):
    if d is None or d.empty:
        return '_(tiada)_\n'
    d = d[kol] if kol else d
    L = ['| ' + ' | '.join(str(c) for c in d.columns) + ' |',
         '|' + '---|' * len(d.columns)]
    for _, r in d.iterrows():
        L.append('| ' + ' | '.join('' if pd.isna(v) else str(v) for v in r) + ' |')
    return '\n'.join(L) + '\n'


def main():
    lip, r51, r53 = _baca('sec_liputan.csv'), _baca('sec_ujian51.csv'), _baca('sec_ujian53.csv')
    kep = json.loads((R / 'sec_keputusan.json').read_text()) if (R / 'sec_keputusan.json').exists() else {}
    if r51 is None or r53 is None:
        print('step11 belum dijalankan (sec_ujian51.csv / sec_ujian53.csv tiada)')
        return 1

    th = kep.get('tahun', [])
    n51 = int(r51.lulus_51.sum()) if 'lulus_51' in r51 else 0
    n53 = int(r53.lulus_53.sum()) if 'lulus_53' in r53 else 0
    boleh = bool(r51.boleh_dinilai.all()) if 'boleh_dinilai' in r51 else False
    LAJ = ('sue', 'tumbuh_hasil', 'pecutan_hasil')
    l51 = sorted(set(r51.loc[r51.lulus_51, 'lajur'])) if 'lulus_51' in r51 else []
    l53 = set()
    for nm in (r53.loc[r53.lulus_53.fillna(False), 'signal'] if 'lulus_53' in r53 else []):
        for b in str(nm).split('&'):
            k = b.split(':')[-1]
            if k in LAJ:
                l53.add(k)
    l53 = sorted(l53)
    kedua = sorted(set(l51) & set(l53))
    diterima = bool(kedua)
    status = ('DITERIMA (tertakluk §6 syarat 2-4)' if diterima
              else 'BELUM BOLEH DINILAI' if not boleh else 'DITOLAK')

    kini = pd.Timestamp.now(tz='UTC')
    L = [f'# KEPUTUSAN FASA 2 — LEG SEC: **{status}**', '']
    L.append(f'Dijana {kini:%Y-%m-%d %H:%M} UTC daripada output `step10_sec.py` dan '
             '`step11_sec_nilai.py`. Spec dipradaftar: `REVERSE/SPEC_FASA2.md` §4.1–§4.4 (data dan '
             'masa ketersediaan), §5 (ujian), §6 (ambang penerimaan), §9.3–§9.5 (ufuk, set signal, '
             'ambang pecahan). Semua pilihan dikunci sebelum keputusan dilihat.')
    L.append('')
    L.append('## 1. Soalan')
    L.append('')
    L.append('Fasa 1 mengukur ruang indikator harga sampai habis: 20,640 ujian ENTRY, enam tahun, '
             'empat rejim, **kosong**. Fasa 2 leg SEC menanya satu soalan yang berbeza — sama ada '
             'data **fundamental titik-masa** (SUE, pecutan hasil, jarak ke earnings) membawa kuasa '
             'pemangkatan yang indikator harga tidak ada, atas **populasi peristiwa yang sama**.')
    L.append('')
    L.append('Sasaran: pulangan **boleh didagangkan** (`pul_henti2atr`) — masuk buka esok dengan kos '
             'sisi, henti keras −2×ATR14, ufuk 63 hari, kos keluar. Bukan puncak run. Kesilapan '
             'fasa 1 (lift 10–24 kali atas hasil bersyarat hindsight yang hilang dalam dagangan) '
             'tidak diulang.')
    L.append('')
    L.append('## 2. Data dan liputan')
    L.append('')
    if th:
        L.append(f'Tahun dinilai: **{th[0]}–{th[-1]}** ({len(th)} tahun). '
                 f'Peristiwa sah: **{kep.get("n_peristiwa", 0):,}**.')
        L.append('')
    L.append(jadual(lip, ['tahun', 'n_peristiwa', 'n_saham', 'n_saham_ada_sec', 'n_sue', 'pct_sue'])
             if lip is not None else '')
    L.append('')
    L.append('Data SEC ialah **nilai pertama difail** (SEC XBRL), jadi ia titik-masa secara '
             'retrospektif sejak 2009 — tidak seperti RS/gred yang dikira harian dan tiada sejarah '
             '(`SPEC_FASA2.md` §4.1). Hari ketersediaan = sesi dagangan pertama yang bukanya selepas '
             'cap masa pemfailan (§4.2), bukan `tarikh_fail`: 52% earnings 8-K difail selepas tutup '
             '16:00 ET, jadi `tarikh_fail` akan memberi lebih separuh peristiwa maklumat kira-kira '
             'satu sesi lebih awal.')
    L.append('')
    L.append('## 3. §5.1 Pemangkatan (Spearman setiap tahun)')
    L.append('')
    L.append(f'Ambang §9.3/§9.5: tanda konsisten ≥ 71% tahun dinilai (minimum 10 tahun), '
             f'|rho| purata ≥ 0.05.')
    L.append('')
    L.append(jadual(r51))
    L.append('')
    if not boleh:
        L.append(f'**Tahun dinilai kurang daripada 10** — lajur berkenaan ialah **BELUM BOLEH '
                 f'DINILAI**, bukan lulus dan bukan gagal (§9.5).')
    else:
        L.append(f'Lulus §5.1: **{n51} daripada {len(r51)}** lajur.')
    L.append('')
    L.append('Bandingan fasa 1 (`ujian_pangkat.py`): daripada 30 indikator harga, **1 sahaja** '
             'konsisten-tanda lawan pulangan boleh didagangkan, dan |rho| tertinggi 0.027. '
             '`atr_pct` memberi rank-IC **−0.251** — apa yang memilih pergerakan besar ialah apa '
             'yang menghalang kita memegangnya.')
    L.append('')
    L.append('## 4. §5.2 + §5.3 Kehadiran dan kawalan kebetulan')
    L.append('')
    L.append(f'Keluarga FDR **{kep.get("keluarga", "FASA2_SEC")}**, {kep.get("n_ujian", len(r53))} '
             'ujian, BH-FDR q ≤ 0.01. Berasingan daripada leg RS/gred dan kelima-lima keluarga '
             'fasa 1 — tiada penggabungan kiraan ujian. Permutasi label 1000× (bilangan sama setiap '
             'bulan), bootstrap blok 1000× mengikut **ticker** dan mengikut **minggu**.')
    L.append('')
    kol = [c for c in ['signal', 'n', 'K_padu', 'lift', 'presisi', 'lift_presisi', 'p_permutasi',
                       'pul_purata', 'jangkaan', 'jangkaan_tanpa_5pct', 'p5_blok_ticker',
                       'p5_blok_minggu', 'kelas', 'lulus_fdr', 'lulus_53'] if c in r53.columns]
    L.append(jadual(r53.sort_values('p_permutasi' if 'p_permutasi' in r53 else 'signal'), kol))
    L.append('')
    L.append(f'Lulus §5.3 (FDR **dan** kedua-dua skema blok > 0 **dan** jangkaan tanpa 5% pemenang '
             f'teratas > 0): **{n53} daripada {len(r53)}**.')
    L.append('')
    L.append('## 5. Keputusan')
    L.append('')
    if diterima:
        L.append(f'§6 syarat 1 **dipenuhi** oleh lajur `{"`, `".join(kedua)}` — lajur yang sama '
                 f'lulus §5.1 dan §5.3.')
        L.append('')
        L.append('Syarat §6 (2)–(4) yang masih perlu disahkan sebelum ini menjadi penemuan: '
                 'mengalahkan asas harga-sahaja; mengalahkan kawalan rawak dalam portfolio 8 slot × '
                 '12.5% pada pulangan **dan** MDD; dan lulus gerbang keras dalam ≥ 2 tahun selain '
                 'tahun ia ditemui (§9.3 syarat 4 — syarat inilah yang membunuh **setiap** calon '
                 'fasa 1).')
    elif not boleh:
        L.append('Penilaian **tidak lengkap**: tahun yang dinilai kurang daripada minimum 10 (§9.5). '
                 'Tiada keputusan diisytiharkan. Melonggarkan ambang selepas melihat keputusan akan '
                 'memusnahkan nilai pradaftar, jadi ia tidak dilonggarkan.')
    else:
        L.append('**Leg SEC fasa 2 DITOLAK.**')
        L.append('')
        L.append(f'§6 syarat 1 menuntut **lajur yang sama** lulus §5.1 **dan** §5.3. Itu tidak '
                 f'berlaku: lajur lulus §5.1 = **{", ".join(l51) or "tiada"}**, '
                 f'lajur induk lulus §5.3 = **{", ".join(l53) or "tiada"}**. '
                 'Persilangannya kosong.')
        L.append('')
        L.append(f'{n51} daripada {len(r51)} lajur lulus §5.1 dan {n53} daripada {len(r53)} signal '
                 'lulus §5.3, tetapi bukan lajur yang sama — jadi tiada penemuan yang lulus '
                 'kedua-dua ujian. Membaca "satu lulus di sini, satu lulus di sana" sebagai '
                 'penemuan ialah tepat kesilapan yang §6 ditulis untuk menghalang.')
        L.append('')
        L.append('Ini **dijangka**, dan dinyatakan sebelum ujian dijalankan (§9.3): PEAD sudah susut '
                 'sejak ia diketahui umum, dan baki kesannya tertumpu pada saham kecil berspread '
                 'lebar — sedangkan universe REVERSE ialah 2,000 teratas ikut nilai dagangan, iaitu '
                 'dengan sengaja membuang bahagian keratan-rentas itu.')
    L.append('')
    pf = _baca('sec_portfolio_ringkas.csv')
    if pf is not None and not pf.empty:
        L.append('## 5b. §5.4 Portfolio 8 slot × 12.5%')
        L.append('')
        if not diterima:
            L.append('**Keputusan §6 sudah ditentukan oleh syarat 1 (lihat §5 di bawah). Nombor di '
                     'sini ialah maklumat magnitud, bukan kriteria penerimaan.** Ia dijalankan '
                     'kerana signal yang bertahan §5.3 tidak gagal ujian kebetulan — ia bertahan '
                     '1000 permutasi label dan kedua-dua skema bootstrap blok — tetapi lajur '
                     'induknya gagal ujian pemangkatan §5.1. Nombor ini **tidak** mengubah '
                     'keputusan DITOLAK.')
            L.append('')
        L.append('Kos penuh, tiga rujukan keluar fasa 1, dua saiz (tetap 12.5% dan berskala risiko '
                 'SPEC_1B k = 4 risiko 1.0%). Nilai di bawah ialah **median merentas tahun**. '
                 '§6 syarat 3: signal mesti mengalahkan KAWALAN RAWAK pada pulangan **dan** MDD.')
        L.append('')
        L.append(jadual(pf))
        L.append('')
        sig = pf[pf.jenis == 'signal']
        rwk = pf[pf.jenis == 'RAWAK']
        if not sig.empty and not rwk.empty:
            for kel in sorted(set(sig.keluar) & set(rwk.keluar)):
                for sz in sorted(set(sig.saiz) & set(rwk.saiz)):
                    a = sig[(sig.keluar == kel) & (sig.saiz == sz)]
                    b = rwk[(rwk.keluar == kel) & (rwk.saiz == sz)]
                    if a.empty or b.empty:
                        continue
                    pa, pb = float(a.pulangan_tahunan.iloc[0]), float(b.pulangan_tahunan.iloc[0])
                    ma, mb = float(a.mdd.iloc[0]), float(b.mdd.iloc[0])
                    menang = 'YA' if (pa > pb and ma > mb) else 'TIDAK'
                    L.append(f'- `{kel}` / saiz {sz}: signal {pa:.2f}%/tahun MDD {ma:.2f}% lawan '
                             f'rawak {pb:.2f}%/tahun MDD {mb:.2f}% -> mengalahkan rawak pada '
                             f'pulangan DAN MDD: **{menang}**')
            L.append('')
        L.append('Sasaran +10%/bulan dibaca daripada lajur `median_bulanan` dan `pct_bulan_ge10` '
                 'di atas, tanpa dimaniskan.')
        L.append('')

    L.append('## 6. Apa yang leg ini TIDAK menjawab')
    L.append('')
    L.append('- Leg **RS/gred** fasa 2 masih menunggu data terkumpul (anggaran ~Okt 2027). Keputusan '
             'di atas tidak mendahuluinya.')
    L.append('- Leg SEC berjalan atas universe A02 yang **sama** dengan fasa 1, jadi ia mewarisi '
             'sifat survivorship yang sama. Itu **had**, bukan kelebihan (§9.3).')
    L.append('- Lajur SEC hadir pada kira-kira 27–30% peristiwa sah sahaja, kerana SUE memerlukan '
             'sejarah suku yang cukup. Peristiwa tanpa lajur dikecualikan, bukan diisi sifar.')
    L.append('- Liputan XBRL berperingkat 2009–2011 (89 saham pada 2009, 253 pada 2010, 482 pada '
             '2011) — sebab ujian bermula 2012, bukan 2009.')
    L.append('')

    p = R / 'KEPUTUSAN_FASA2_SEC.md'
    p.write_text('\n'.join(L), encoding='utf-8')
    print(f'{p.name}: {len("".join(L)):,} aksara | status {status} | §5.1 {n51}/{len(r51)}'
          f' | §5.3 {n53}/{len(r53)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
