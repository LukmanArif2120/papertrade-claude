"""Paksi CARA pada 45 masuk produksi — pradaftar `REVERSE/SPEC_PORTFOLIO_94B.md` §6.

`REVERSE/cara.csv` mengukur 6 cara pengisian pada `GB02_atau3 × X13` SAHAJA — konfigurasi
yang sudah bersara dan berpangkat 7/1,496. Skrip ini mengarahkan semula enjin CARA yang
SAMA (`step23_cara.py`, tiada enjin kedua) kepada kesatuan **45 masuk** yang 94 kombinasi
produksi pakai.

HAD YANG MESTI DINYATAKAN: keluar dikekalkan `X13` seperti kajian CARA asal. Itu reka
bentuk yang betul untuk MENGASINGKAN paksi CARA — memvariasikan masuk DAN keluar DAN cara
serentak akan mengelirukan ketiga-tiganya. Tetapi akibatnya, keputusan ini menjawab "cara
mana terbaik DIBERI X13", bukan "diberi setiap kombinasi dengan keluarnya sendiri". `X13`
memegang 6 daripada 94 slot produksi, jadi pemindahan kepada 5 keluar yang lain ialah
ANGGAPAN, bukan ukuran.

`cara.csv` dan `CARA.md` asal TIDAK ditulis ganti — `REVERSE/strategi.py --semak` membacanya
dan akan gagal dalam CI jika ia hanyut. Keluaran di sini berasingan.

Guna: python3 REVERSE/step35_cara_94.py
Output: REVERSE/CARA_94.md, REVERSE/cara_94.csv
"""
import csv
import sys
from pathlib import Path

AKAR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AKAR))
import REVERSE.step23_cara as S23  # noqa: E402

KELUAR = AKAR / 'REVERSE'
JEJAK = KELUAR / 'jejak_semua.csv'


def masuk_produksi():
    """45 masuk berbeza daripada 94 kombinasi — dibaca daripada fail keputusan, bukan tangan."""
    J = list(csv.DictReader(open(JEJAK, encoding='utf-8')))
    m = sorted({x['masuk'] for x in J})
    assert m, 'jejak_semua.csv kosong'
    return m


def main():
    asal = list(S23.KOLAM3)
    baru = masuk_produksi()
    S23.KOLAM3 = baru
    print(f'CARA diarahkan semula: kolam {asal} -> {len(baru)} masuk produksi', flush=True)
    print(f'  {" ".join(baru)}', flush=True)
    # S23.main() menulis ke cara.csv dan CARA.md. Fail itu dibaca oleh
    # `REVERSE/strategi.py --semak`, yang GAGAL dalam CI jika registry hanyut daripada
    # fail keputusan. Jadi simpan dahulu, jalankan, salin keluaran ke *_94, kemudian
    # PULIHKAN yang asal — jika tidak larian ini merosakkan semakan hanyut repo.
    simpan = {}
    for nama in ('cara.csv', 'CARA.md'):
        q = KELUAR / nama
        if q.exists():
            simpan[nama] = q.read_bytes()
    try:
        rc = S23.main([])
        for lama, baharu in (('cara.csv', 'cara_94.csv'), ('CARA.md', 'CARA_94.md')):
            q = KELUAR / lama
            if q.exists():
                (KELUAR / baharu).write_bytes(q.read_bytes())
                print(f'  {lama} -> {baharu}', flush=True)
    finally:
        for nama, isi in simpan.items():
            (KELUAR / nama).write_bytes(isi)
            print(f'  {nama} DIPULIHKAN kepada versi dikomit', flush=True)
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
