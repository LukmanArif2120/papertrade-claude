# dagangan.py — lajur kaedah bagi SATU dagangan (22 Okt 2026, kajian/KAJIAN_DATA_TERCEMAR.md R10).
# Modul yang lajur exitc/tgt dikira oleh replika gelung enjin (`_exitc_*`, `_exit_ekor`, `_kunci`, `_kunci_tgt`, `_isi_tgt`,
# `_tgt_tetap`) memberi nilai bagi dagangan REPLIKA: bermula dari WARM, satu dagangan pada satu masa, isyarat semasa memegang
# diabaikan. Posisi hadapan (Lejar Penuh, Papertrade C) bermula Okt 2026, jadi isyaratnya boleh jatuh semasa replika masih
# memegang dagangan lain (cth. M81 DELL isyarat setiap hari 1–20 Okt): posisi itu mendapat bendera keluar/sasaran dagangan
# lain (Lejar 21 Okt: 543/711 posisi kaedah bergantung). sedia_dagangan() mengira semula modul atas satu saham dengan replika
# bermula pada bar isyarat posisi itu, jadi bendera = dagangan itu sendiri; sama dengan enjin apabila replika bebas pada bar itu.
import inspect

import pandas as pd

import enjin

# modul bukan SILANG dengan replika gelung enjin bermula pada WARM (semua modul kod/kaedah dengan 'while i < n' / 'i = WARM',
# disemak 22 Okt 2026; M40, M45 = replika portfolio merentas saham: tidak boleh dikira
# bagi satu saham; M18, M24, M56, M94, M96 = exitc setiap bar, tidak bergantung dagangan)
REPLIKA = {'M02', 'M19', 'M20', 'M26', 'M31', 'M38', 'M41', 'M47', 'M76', 'M78', 'M81', 'M82', 'M100'}
LAJUR_MENTAH = ['open', 'high', 'low', 'close', 'volume']


def perlu(mid, m=None):
    return mid in REPLIKA and not getattr(m, 'SILANG', False)


def sedia_dagangan(m, t, g, idx, ti):
    """Lajur kaedah (sig, stop, tgt, exitc, rank) bagi dagangan yang isyaratnya pada ti. g = bar mentah saham t (bar <= sesi
    semasa). Replika modul dimulakan pada bar ti (WARM modul dan lalai parameter `warm` ditukar sementara). Satu bar sementara
    (salinan bar akhir, volum 0) ditambah selepas bar akhir sebelum sedia() dan dibuang selepasnya: replika hanya menanda
    keluar pada bar j jika bar j+1 wujud (syarat boleh-laksana, bukan maklumat), jadi tanpanya bendera bar akhir hilang dan
    had masa pada bar itu didahulukan, tidak seperti enjin. Pulang DataFrame (tanpa bar sementara), atau None jika bar ti
    tiada atau isyarat ti tidak lagi benar (pemanggil memakai lajur biasa)."""
    try:
        i = g.index.get_loc(pd.Timestamp(ti))
    except KeyError:
        return None
    asal = m.WARM
    tukar = []
    for f in vars(m).values():
        if inspect.isfunction(f) and f.__defaults__ and 'warm' in inspect.signature(f).parameters:
            ps = [p for p in inspect.signature(f).parameters.values() if p.default is not inspect.Parameter.empty]
            tukar.append((f, f.__defaults__))
            f.__defaults__ = tuple(i if p.name == 'warm' else d for p, d in zip(ps, f.__defaults__))
    m.WARM = i
    try:
        sementara = g[LAJUR_MENTAH].iloc[[-1]].set_axis([g.index[-1] + pd.offsets.BDay(1)]).assign(volume=0.0)
        x = {t: pd.concat([g[LAJUR_MENTAH], sementara])}
        m.sedia(x, {k: v.copy() for k, v in idx.items()})
        h = enjin.siap(x[t]).iloc[:-1]
    finally:
        m.WARM = asal
        for f, d in tukar:
            f.__defaults__ = d
    return h if bool(h['sig'].iloc[i]) else None


# ---------------------------------------------------------------- pembetulan Papertrade C (rutin 6:02 langkah 2c)
def betul_c(folder, frames, idx, tulis=True):
    """Nilai semula lorong 1 posisi Papertrade C bagi kaedah REPLIKA dengan lajur dagangan sendiri (sama dengan harian_c.kerja
    dan Lejar sejak 22 Okt 2026). Hanya keputusan yang diliputi stor (keluar <= bar akhir saham) diubah: keluar salah tarikh/
    harga dibetulkan; keluar yang tidak berlaku dibuka semula (harga terkini = tutup bar akhir); posisi yang patut sudah keluar
    ditutup. Pulang senarai perubahan (fail, saham, kaedah, tarikh_beli, lama, baharu)."""
    import importlib
    import os
    import harian_c as H
    import sahkan as SH
    SES = list(idx['SPY'].index)
    mod, out = {}, []
    for p in sorted(os.path.join(folder, f) for f in os.listdir(folder) if f.startswith('claude') and f.endswith('.csv')):
        lajur, rows = SH.baca(p)
        ubah = False
        for r in rows:
            mid = r.get('id_kaedah') or r.get('kaedah') or ''
            if mid not in REPLIKA or SH.benar(r.get('tidak_dibeli')) or SH.benar(r.get('tidak_sah')) or r.get('sumber') == 'luar':
                continue
            t, ti, hb = r.get('saham'), r.get('tarikh_isyarat'), H.nombor(r.get('harga_beli'))
            g = frames.get(t)
            if g is None or not ti or not hb or not r.get('tarikh_beli') or pd.Timestamp(r['tarikh_beli']) > g.index[-1]:
                continue
            if mid not in mod:
                mod[mid] = importlib.import_module(f'kaedah.{mid}')
            m = mod[mid]
            if not perlu(mid, m):
                continue
            gd = sedia_dagangan(m, t, g, idx, ti)
            if gd is None:
                continue
            x = H.nilai_keluar(gd, gd.index.get_loc(pd.Timestamp(ti)), getattr(m, 'TMAX', None) or 0)
            akhir = str(g.index[-1].date())
            keluar = SH.benar(r.get('keluar'))
            lama = r.get('tarikh_keluar') if keluar else ''
            if keluar and lama > akhir:
                continue                        # keluar selepas bar akhir stor: tidak boleh disahkan
            baru = (x or {}).get('t') or ''
            if baru == lama:
                continue
            nota = f"keluar dinilai semula {pd.Timestamp.now(tz='Asia/Kuala_Lumpur'):%d %b %Y} (dagangan sendiri, kod/dagangan.py)"
            if baru:
                r.update(keluar='True', tarikh_keluar=baru, harga_keluar=f"{H.r4(x['p'])}", harga_terkini=f"{H.r4(x['p'])}",
                         untung_akhir_pct=f"{H.r2((x['p'] / hb - 1) * 100)}", untung_pct=f"{H.r2((x['p'] / hb - 1) * 100)}",
                         hari=str(H.hari_antara(r['tarikh_beli'], baru, SES)),
                         isyarat_keluar=f"Keluar: {x['why']} ({H.hb(baru)} @ {x['p']:.2f})")
            else:
                c = float(g.close.iloc[-1])
                r.update(keluar='False', tarikh_keluar='', harga_keluar='', untung_akhir_pct='', harga_terkini=f'{H.r4(c)}',
                         untung_pct=f'{H.r2((c / hb - 1) * 100)}', hari=str(H.hari_antara(r['tarikh_beli'], akhir, SES)))
                r['isyarat_keluar'] = (f"Isyarat keluar {H.hb(x['menunggu'])} — jual pada buka esok (menunggu)" if x and x.get('menunggu')
                                       else H.status_pegang(r))
            r['nota'] = ((r.get('nota') or '') + '; ' + nota).lstrip('; ')
            if 'tutup_semua' in lajur:
                r['tutup_semua'] = str(SH.benar(r.get('keluar')) and SH.benar(r.get('keluar_henti')))
            ubah = True
            out.append((os.path.basename(p), t, mid, r['tarikh_beli'], lama or 'terbuka', baru or 'terbuka'))
        if ubah and tulis:
            SH.tulis(p, lajur, rows)
    return out


def main(argv=None):
    import argparse
    import json
    import os
    import sys
    BS2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(BS2, 'standard'))
    from stor import muat, frames_dict
    ap = argparse.ArgumentParser(description='Nilai semula keluar posisi C kaedah replika (dagangan sendiri)')
    sp = ap.add_subparsers(dest='cmd', required=True)
    b = sp.add_parser('betul'); b.add_argument('--folder', default=os.path.join(BS2, 'papertrade'))
    b.add_argument('--stor', default=os.path.join(BS2, 'data', 'harga', 'stor')); b.add_argument('--tulis', action='store_true')
    a = ap.parse_args(argv)
    fr, idx = frames_dict(muat(a.stor))
    x = betul_c(a.folder, fr, idx, a.tulis)
    for y in x:
        print(*y, sep='\t')
    print(json.dumps(dict(dibetulkan=len(x), ditulis=bool(a.tulis)), ensure_ascii=False), file=sys.stderr)


if __name__ == '__main__':
    main()
