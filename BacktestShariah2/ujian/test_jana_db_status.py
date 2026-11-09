"""Ujian medan v172 jana_db (9 Nov 2026, keputusan pengguna; rekod/maklumat sahaja, bukan keputusan):
harian/status.kuarantin, harian/status.keputusan_terbuka, dan prestasi/portfolio_slot (jalur, persentil, spus_pct).
Semua gagal-lembut: fail tiada/rosak -> [] / None, bukan ralat."""
import os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
import jana_db as jd


def tulis(d, nama, isi):
    p = os.path.join(d, nama)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(isi)
    return p


class UjianKuarantin(unittest.TestCase):
    def test_aktif_sahaja_dan_sebab_dipotong(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, 'k.csv', 'ticker,tarikh_mula,sebab,dicatat,status\n'
                                 'AAA,2026-10-21,' + 'x' * 100 + ',2026-11-07 12:03 UTC,aktif\n'
                                 'BBB,2026-11-03,delist,2026-11-07 12:03 UTC,aktif\n'
                                 'BBB,2026-11-03,disemak dan dilepas,2026-11-08 09:00 UTC,lepas\n'
                                 'CCC,2026-11-01,pendek,2026-11-07 12:03 UTC,\n')
            q = jd.kuarantin_aktif(p)
            self.assertEqual([x['ticker'] for x in q], ['AAA', 'CCC'])          # BBB dilepas; status kosong = aktif
            self.assertLessEqual(len(q[0]['sebab']), 80)
            self.assertTrue(q[0]['sebab'].endswith('…'))
            self.assertEqual(q[1]['sebab'], 'pendek')
            self.assertEqual(q[0]['tarikh_mula'], '2026-10-21')

    def test_fail_tiada_atau_rosak(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(jd.kuarantin_aktif(os.path.join(d, 'tiada.csv')), [])
            self.assertEqual(jd.kuarantin_aktif(tulis(d, 'r.csv', 'bukan,lajur\n1,2\n')), [])

    def test_repo_sebenar_bentuk(self):
        for x in jd.kuarantin_aktif():
            self.assertEqual(set(x), {'ticker', 'tarikh_mula', 'sebab'})
            self.assertLessEqual(len(x['sebab']), 80)


class UjianKeputusanTerbuka(unittest.TestCase):
    def test_terbuka_sahaja(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, 'k.csv', 'tarikh,perkara,status,catatan\n'
                                 '2026-10-28,Selesai dahulu,selesai,x\n'
                                 '2026-11-06,"Pilih berat T4 (SPUS 80/20, 70/30 atau 50/50)",terbuka,"y"\n'
                                 '2026-11-07,Lagi satu, terbuka ,z\n')
            q = jd.keputusan_terbuka_db(p)
            self.assertEqual(q, [dict(tarikh='2026-11-06', perkara='Pilih berat T4 (SPUS 80/20, 70/30 atau 50/50)'),
                                 dict(tarikh='2026-11-07', perkara='Lagi satu')])

    def test_fail_tiada(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(jd.keputusan_terbuka_db(os.path.join(d, 'tiada.csv')), [])

    def test_repo_sebenar_melalui_koordinator(self):
        q = jd.keputusan_terbuka_db()
        self.assertIsInstance(q, list)
        for x in q:
            self.assertEqual(set(x), {'tarikh', 'perkara'})


class UjianPortfolioSlotJalur(unittest.TestCase):
    HARI = ['2026-10-16', '2026-10-19', '2026-10-20']
    SPUS = {20261016: (100.0, 101.0), 20261019: (101.0, 99.0), 20261020: (99.5, 102.0)}

    def lorong(self, d, k, ekuiti, hari=None):
        hari = hari or self.HARI
        tulis(d, f'{k}_ekuiti.csv', 'tarikh,ekuiti,tunai,bil_posisi,spy\n'
              + ''.join(f'{t},{e},0.0,10,1.0\n' for t, e in zip(hari, ekuiti)))
        tulis(d, f'{k}_posisi.csv', 'saham,id_kaedah,tarikh_isyarat,rs,tarikh_beli,harga_beli,saiz_pct,status,tarikh_keluar,'
                                    'harga_keluar,untung_pct,harga_terkini,untung_semasa_pct,lorong\n'
                                    f'AAA,M01,2026-10-15,90,{hari[0]},10,10,Pegang,,,,11,10.0,{k}\n'
                                    f'BBB,M01,2026-10-15,80,{hari[0]},10,10,Keluar,{hari[-1]},12,20.0,,,{k}\n')

    def test_jalur_persentil_dan_spus(self):
        with tempfile.TemporaryDirectory() as d:
            self.lorong(d, 'RS_10', [1.0, 1.02, 1.05])
            self.lorong(d, 'GABUNGAN_10', [1.0, 1.0], hari=self.HARI[1:])          # lorong beku bermula lewat
            # 4 cabutan: ekuiti terakhir 0.98, 1.00, 1.03, 1.10
            tulis(d, 'rawak_jalur_ekuiti.csv', 'benih,tarikh,ekuiti\n' + ''.join(
                f'{b},{t},{e}\n' for b, E in zip((1, 2, 3, 4), ([1.0, 0.99, 0.98], [1.0, 1.0, 1.0], [1.0, 1.01, 1.03], [1.0, 1.05, 1.10]))
                for t, e in zip(self.HARI, E)))
            ps = jd.portfolio_slot('x', folder=d, spus=self.SPUS)
            J = ps['jalur']
            self.assertEqual((J['n'], J['sesi'], J['min'], J['maks'], J['median']), (4, '2026-10-20', 0.98, 1.1, 1.015))
            rs = ps['portfolio']['RS_10']
            self.assertEqual(rs['persentil'], 75.0)                                 # +5% mengatasi 0.98, 1.00, 1.03
            self.assertEqual(rs['spus_pct'], 2.0)                                   # buka 100 -> tutup 102
            self.assertEqual(rs['spus_mdd_pct'], -1.98)                             # puncak tutup 101 -> 99
            gb = ps['portfolio']['GABUNGAN_10']
            # tingkap 19-20 Okt: asas cabutan = ekuiti 16 Okt (1.0): pulangan cabutan -2, 0, +3, +10; lorong 0% -> 1/4 di bawah
            self.assertEqual(gb['persentil'], 25.0)
            self.assertEqual(gb['spus_pct'], round((102.0 / 101.0 - 1) * 100, 2))   # buka 19 Okt, bukan tutup 16 Okt

    def test_tanpa_jalur_dan_tanpa_liputan_spus(self):
        with tempfile.TemporaryDirectory() as d:
            self.lorong(d, 'RS_10', [1.0, 1.02, 1.05])
            ps = jd.portfolio_slot('x', folder=d, spus={20261016: (100.0, 101.0)})
            self.assertIsNone(ps['jalur'])
            rs = ps['portfolio']['RS_10']
            self.assertIsNone(rs['persentil'])
            self.assertIsNone(rs['spus_pct'])
            self.assertIsNone(rs['spus_mdd_pct'])


if __name__ == '__main__':
    unittest.main()
