"""Urutan entri dalam fail batch ialah PROTOKOL, bukan butiran pelaksanaan.

`jana_db.batchkan` memutuskan dokumen mana ditolak bersama dan dalam urutan apa. Tiga pihak
bergantung padanya: `jadual/tolak_db.md` langkah 5 (satu panggilan ArtifactData setiap fail),
pengawal kelengkapan `subRingkas`/`subBhg` dalam `dashboard_v2.html` (tidak merender sehingga
setiap bahagian sepadan dengan `induk` dokumen asas), dan `bahagi_db.py`.

Yang diuji di sini ialah satu sifat sahaja, dan ia sifat yang gagal pada 3 Nov 2026: apabila
kumpulan TIDAK muat satu batch, dokumen ASAS mesti ditolak TERAKHIR. Asas membawa `induk`;
tolak ia dahulu dan untuk beberapa minit setiap malam asas mengisytiharkan induk baharu
sementara bahagiannya masih lama, jadi halaman tidak dapat berhimpun dan tab Posisi memapar
"Belum ada posisi dalam pangkalan data" - 1,641 posisi Nxx dilaporkan sebagai kosong.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
import jana_db as jd  # noqa: E402


def w(doc_id, kol='papertrade'):
    return dict(op='set', collection=kol, doc_id=doc_id)


def kump(asas, n, sz, kol='papertrade'):
    """Satu kumpulan pecahan: asas + n-1 bahagian, setiap satu `sz` bait."""
    k = f'{kol}/{asas}'
    return [(w(asas, kol), sz, k)] + [(w(f'{asas}_{i}', kol), sz, k) for i in range(2, n + 1)]


def susunan(batches):
    return [[x['doc_id'] for x in bt] for bt in batches]


class TestAsasTerakhir(unittest.TestCase):
    def test_kumpulan_terpecah_letak_asas_terakhir(self):
        b, tp = jd.batchkan(kump('ringkas_c', 4, 400_000))
        rata = [d for bt in susunan(b) for d in bt]
        self.assertEqual(rata[-1], 'ringkas_c', f'asas mesti terakhir, dapat {rata}')
        self.assertEqual(sorted(rata), sorted(['ringkas_c', 'ringkas_c_2', 'ringkas_c_3', 'ringkas_c_4']))
        self.assertEqual(len(tp), 1, 'kumpulan terpecah mesti direkod dalam ringkas.json')
        self.assertIn('papertrade/ringkas_c', tp[0], 'label terpecah mesti namakan dokumen asas')

    def test_kumpulan_yang_muat_kekal_satu_batch_dan_utuh(self):
        """Muat satu batch = atom; urutan tidak penting, jadi jangan ubah apa yang berfungsi."""
        b, tp = jd.batchkan(kump('kecil', 3, 1_000))
        self.assertEqual(susunan(b), [['kecil', 'kecil_2', 'kecil_3']])
        self.assertEqual(tp, [])

    def test_dokumen_tunggal_tidak_disusun_semula(self):
        b, tp = jd.batchkan([(w('claude_7'), 200_000, 'papertrade/claude_7'),
                             (w('claude_8'), 200_000, 'papertrade/claude_8')])
        self.assertEqual(susunan(b), [['claude_7', 'claude_8']])
        self.assertEqual(tp, [])

    def test_setiap_batch_dalam_had(self):
        t = kump('ringkas_c', 14, 250_000) + kump('lorong2', 13, 250_000, 'posisi')
        b, tp = jd.batchkan(t)
        for bt in b:
            self.assertLessEqual(len(bt), 50)
        self.assertEqual(len(tp), 2)
        for grp in ('ringkas_c', 'lorong2'):
            rata = [d for bt in susunan(b) for d in bt]
            self.assertGreater(rata.index(grp), max(i for i, d in enumerate(rata) if d.startswith(grp + '_')),
                               f'asas {grp} mesti selepas setiap bahagiannya')

    def test_tiada_dokumen_hilang_atau_berganda(self):
        t = kump('a', 5, 300_000) + kump('b', 2, 10) + [(w('c'), 50, 'papertrade/c')]
        b, _ = jd.batchkan(t)
        rata = [d for bt in susunan(b) for d in bt]
        self.assertEqual(sorted(rata), sorted([x[0]['doc_id'] for x in t]))
        self.assertEqual(len(rata), len(set(rata)))


class TestRingkasPtSatuKumpulan(unittest.TestCase):
    """`ringkas_pt` memulangkan ASAS dahulu, dan main() menolaknya sebagai SATU kumpulan.

    Dua invarian bergantung padanya. (1) batchkan menggerakkan `g[0]` ke hujung, jadi kalau asas
    bukan elemen pertama, dokumen yang SALAH dipindahkan. (2) Sebelum 4 Nov 2026 keluaran
    ringkas_pt dimasukkan ke `semua` sebagai dokumen BEBAS satu per satu, jadi 22 dokumen
    `ringkas_c` bertaburan merentas fail batch tanpa kumpulan - dan pembetulan asas-terakhir
    tidak terpakai langsung kepada dokumen yang menyebabkan kegagalan 3 Nov 2026.
    """

    def test_asas_elemen_pertama(self):
        R = [dict(saham=f'S{i:03d}', kaedah='M01', untung_pct=i / 7.0, keluar=False) for i in range(400)]
        out = jd.ringkas_pt(R, 'ringkas_x', {'dibina': 'ujian'}, had=4000)
        self.assertEqual(out[0][0], 'ringkas_x', 'asas mesti elemen PERTAMA')
        self.assertIn('bahagian', out[0][1])
        B = out[0][1]['bahagian']
        self.assertGreater(B['n'], 1, 'had kecil sepatutnya memaksa lebih satu bahagian')
        nama = [d for d, _ in out]
        self.assertEqual(nama[1:B['n']], [f'ringkas_x_{i}' for i in range(2, B['n'] + 1)])
        self.assertEqual(nama[B['n']:], [f'ringkas_x_kamus_{i}' for i in range(1, B['nk'] + 1)])
        for _, d in out[1:]:
            self.assertEqual(d['induk'], B['id'])

    def test_sebagai_kumpulan_asas_ditolak_terakhir(self):
        R = [dict(saham=f'S{i:03d}', kaedah='M01', untung_pct=i / 7.0, keluar=False) for i in range(400)]
        out = jd.ringkas_pt(R, 'ringkas_x', {'dibina': 'ujian'}, had=4000)
        # seperti main(): satu kumpulan, saiz dinaikkan supaya ia TIDAK muat satu batch
        t = [({'op': 'set', 'collection': 'papertrade', 'doc_id': d}, 500_000, 'papertrade/ringkas_x')
             for d, _ in out]
        b, tp = jd.batchkan(t)
        rata = [x['doc_id'] for bt in b for x in bt]
        self.assertEqual(rata[-1], 'ringkas_x')
        self.assertEqual(len(tp), 1)


if __name__ == '__main__':
    unittest.main()
