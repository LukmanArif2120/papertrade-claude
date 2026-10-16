import contextlib, io, json, os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
import bahagi_db as bd


def dokumen(n):
    return {'dibina': '2026-10-16 20:15 MYT', 'tarikh_data': '2026-10-15', 'definisi': 'ujian',
            'rows': [{'saham': f'S{i:04d}', 'kaedah': 'M02', 'pemangkin': 'teks panjang ' * 30, 'skor': i} for i in range(n)]}


def gabung(hasil):
    """Tiru logik halaman: bahagian 2..n digabung jika induk sepadan."""
    asas = dict(hasil[0][1])
    b = asas['bahagian']
    rows = list(asas['rows'])
    lain = {d['bahagian']: d for _, d in hasil[1:]}
    for k in range(2, b['n'] + 1):
        if lain.get(k, {}).get('induk') == b['id']:
            rows += lain[k]['rows']
    return asas, rows


class TestBahagiDb(unittest.TestCase):
    def test_dokumen_kecil_satu_bahagian(self):
        doc = dokumen(10)
        hasil = bd.bahagi(doc, 'watchlist', 200000)
        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0][0], 'watchlist')
        self.assertEqual(hasil[0][1]['bahagian']['n'], 1)
        self.assertEqual(hasil[0][1]['rows'], doc['rows'])
        self.assertEqual(hasil[0][1]['dibina'], doc['dibina'])

    def test_dokumen_besar_dibahagi_dan_digabung_semula(self):
        doc = dokumen(900)
        hasil = bd.bahagi(doc, 'senarai_beli', 100000)
        self.assertGreater(len(hasil), 2)
        self.assertEqual([h[0] for h in hasil], ['senarai_beli'] + [f'senarai_beli_{k}' for k in range(2, len(hasil) + 1)])
        for _, d in hasil:
            self.assertLessEqual(bd.bait(d), 100000)
        asas, rows = gabung(hasil)
        self.assertEqual(rows, doc['rows'])
        self.assertEqual(asas['tarikh_data'], '2026-10-15')

    def test_bahagian_lama_diabaikan(self):
        lama = bd.bahagi(dokumen(900), 'watchlist', 100000)
        baru = bd.bahagi(dokumen(5), 'watchlist', 100000)
        self.assertNotEqual(lama[0][1]['bahagian']['id'], baru[0][1]['bahagian']['id'])
        _, rows = gabung(baru + lama[1:])  # bahagian lama masih wujud dalam db
        self.assertEqual(len(rows), 5)

    def test_cli_tulis_fail(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'penuh.json')
            json.dump({'data': dokumen(400)}, open(p, 'w'))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                kod = bd.main(['--json', p, '--nama', 'watchlist', '--keluar', os.path.join(d, 'o'), '--had', '60000'])
            self.assertEqual(kod, 0)
            r = json.loads(out.getvalue())
            self.assertEqual(sum(f['baris'] for f in r['fail']), 400)
            self.assertTrue(all(os.path.exists(f['fail']) for f in r['fail']))


if __name__ == '__main__':
    unittest.main()
