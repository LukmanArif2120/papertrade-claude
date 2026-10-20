import json, os, sys, unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
import jana_db as jd


def nyahkod(docs, nama):
    """Sama dengan nyahkod() dalam dashboard_v2.html (connect)."""
    asas = docs[nama]; B = asas['bahagian']; M = {}
    for i in range(1, B['nk'] + 1):
        d = docs[f'{nama}_kamus_{i}']
        assert d['induk'] == B['id']
        for c, mula, v in d['kamus']:
            L = M.setdefault(c, []); assert len(L) == mula; L += v
    rows = list(asas['rows'])
    for i in range(2, B['n'] + 1):
        d = docs[f'{nama}_{i}']; assert d['induk'] == B['id']; rows += d['rows']
    out = []
    for a in rows:
        r = {}
        for c, t, v in zip(asas['kolum'], asas['jenis'], a):
            if v is None or (t in ('k', 'j') and v == 0):
                continue
            if t in ('k', 'j'):
                v = M[c][v - 1]
                if t == 'j':
                    v = json.loads(v)
            elif t == 'b':
                v = bool(v)
            r[c] = v
        out.append(r)
    return out


class UjianRingkas(unittest.TestCase):
    """papertrade/ringkas_c|m: pengekodan padat ikut lajur mesti tanpa kehilangan (susunan, jenis, medan yang tiada)."""

    def baris(self, n):
        R = []
        for i in range(n):
            r = dict(saham=f'S{i % 37}', kaedah=f'M{i % 5:02d}', harga_beli=10 + i / 7, unit=1, keluar=i % 3 == 0,
                     isyarat_keluar=f'Pegang (henti {i}.5)', pemangkin_url=[{'url': f'https://x/{i % 4}'}],
                     catatan='x' * 200 if i % 11 == 0 else None, campur=i if i % 2 else 'teks')
            R.append({k: v for k, v in r.items() if v is not None})
        return R

    def test_pergi_balik_dan_bahagian(self):
        R = self.baris(900)
        docs = dict(jd.ringkas_pt(R, 'ringkas_c', dict(harga_pada='2026-10-19 tutup'), had=20000))
        B = docs['ringkas_c']['bahagian']
        self.assertGreater(B['n'], 1)
        self.assertTrue(all(jd.bait(d) < 20000 + 2000 for d in docs.values()))
        self.assertEqual(nyahkod(docs, 'ringkas_c'), R)
        self.assertEqual(docs['ringkas_c']['harga_pada'], '2026-10-19 tutup')

    def test_kosong(self):
        docs = dict(jd.ringkas_pt([], 'ringkas_m', {}))
        self.assertEqual(nyahkod(docs, 'ringkas_m'), [])

    def test_lebih_kecil(self):
        R = self.baris(2000)
        docs = dict(jd.ringkas_pt(R, 'ringkas_c', {}))
        self.assertLess(sum(jd.bait(d) for d in docs.values()), 0.6 * sum(jd.bait(r) for r in R))


if __name__ == '__main__':
    unittest.main()
