"""Ujian dokumen db dashboard `carian/f_utama` (standard/f_utama_db.py) dan pembacanya dalam dashboard_v2.html
(Rujukan -> Setup F, v181, 16 Nov 2026)."""
import os
import sys
import tempfile
import unittest

import pandas as pd

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SINI, '..', 'standard'))
import f_utama_db as F  # noqa: E402
from bahagi_db import HAD_DB, bait  # noqa: E402

CS13 = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS13')
HTML = os.path.join(SINI, '..', 'standard', 'dashboard_v2.html')


class TestFUtamaDb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = F.bina()
        cls.U = pd.read_csv(os.path.join(CS13, 'senarai_utama.csv'))
        cls.utama = cls.d['rows'][:cls.d['n_utama']]          # v189: baris senarai utama dahulu; baris sepanjang tahun selepasnya

    def test_bentuk_dan_bilangan(self):
        d, U = self.d, self.U
        self.assertEqual(d['kol'], F.KOL)
        ix = {k: i for i, k in enumerate(d['kol'])}
        self.assertEqual((d['n_utama'], d['n']), (len(U), len(d['rows'])))
        self.assertEqual(sum(1 for r in self.utama if r[ix['pil']]), int(U.pilihan.sum()))
        self.assertEqual(d['n_pilihan'], sum(1 for r in d['rows'] if r[ix['pil']]))
        self.assertEqual((d['n_lama'], d['n_baharu']), (int((U.asal == 'lama').sum()), int((U.asal == 'baharu').sum())))
        self.assertTrue(all(len(r) == len(F.KOL) for r in d['rows']))
        self.assertEqual([r[0] for r in self.utama], U.id.tolist())              # susunan senarai utama dikekalkan
        self.assertEqual(set(d['semak_masa']), {'pilih', 'lain'})

    def test_nyahkod_sepadan_dengan_sumber(self):
        d, U = self.d, self.U.set_index('id')
        ix = {k: i for i, k in enumerate(d['kol'])}
        for r in self.utama[:50] + self.utama[-50:]:
            u = U.loc[r[ix['id']]]
            self.assertEqual(bool(r[ix['pil']]), bool(u.pilihan))
            self.assertEqual('baharu' if r[ix['asal']] else 'lama', u.asal)
            self.assertAlmostEqual(r[ix['tangkap']] / 1000, u.terus, delta=6e-4)
            self.assertAlmostEqual(r[ix['menang']] / 1000, u.menang_B, delta=6e-4)
            self.assertAlmostEqual(r[ix['purata']] / 10000, u.purata_B, delta=6e-5)
            pra = d['kamus']['pra'][r[ix['pra']]]
            self.assertEqual(pra, '' if pd.isna(u.prasyarat) else u.prasyarat)

    def test_lajur_v182_sepadan_dengan_sumber(self):
        """Lajur v182 (jenis, am5, k10, k1, k2) dan median kawalan dibaca terus daripada CSV CS13, tanpa kiraan baharu."""
        d, U = self.d, self.U.set_index('id')
        ix = {k: i for i, k in enumerate(d['kol'])}
        self.assertEqual(d['kamus']['jenis'], F.JENIS)
        for r in self.utama[:50] + self.utama[-50:]:
            u = U.loc[r[ix['id']]]
            self.assertAlmostEqual(r[ix['am5']] / 1000, u.a_m5, delta=6e-4)
            self.assertAlmostEqual(r[ix['k10']] / 1000, u.k10_B, delta=6e-4)
            self.assertAlmostEqual(r[ix['k1']] / 10000, u.kl_terus_K1, delta=6e-5)
            self.assertAlmostEqual(r[ix['k2']] / 10000, u.kl_terus_K2, delta=6e-5)
            self.assertEqual(r[ix['jenis']], F.jenis(u.nama))
        self.assertEqual(F.jenis('K13.009 Stochastic(14) silang naik'), 0)
        self.assertEqual(F.jenis('M105 Supertrend tulen'), 1)
        self.assertEqual(F.jenis('N16 RSI2<10 tanpa penapis'), 6)
        K = pd.read_csv(os.path.join(CS13, 'kawalan.csv'))
        K = K[K.layak.astype(bool)]
        self.assertEqual(d['kawalan']['n'], len(K))
        self.assertAlmostEqual(d['kawalan']['menang'], K.menang_B.median(), places=3)

    def test_cara_pegang_kedua(self):
        """Keputusan pengguna 16 Nov 2026 ("B" selepas CS14): lajur "pegang lebih lama" (r0.t2.0) di sebelah cara sekarang."""
        d = self.d
        X = pd.read_csv(os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS14', 'setup.csv.gz')).set_index('id')
        ix = {k: i for i, k in enumerate(d['kol'])}
        self.assertEqual(d['kol'][:17], ['id', 'asal', 'pil', 'pra', 'nama', 'pen', 'beli', 'shar', 'tangkap', 'rawak', 'm5', 'menang', 'purata',
                                         'rugi15', 'hari', 'k3', 'n'])                      # lajur lama tidak berganjak (halaman lama masih membaca)
        self.assertEqual(d['kol'][17:21], ['menang2', 'purata2', 'rugi2', 'hari2'])
        self.assertEqual(d['kol'][21:26], ['jenis', 'am5', 'k10', 'k1', 'k2'])  # v182 reka bentuk, selepas CS14
        self.assertEqual((F.CARA1, F.CARA2), ('r0.t1.126', 'r0.t2.0'))
        for r in self.utama[:40] + self.utama[-40:]:
            x = X.loc[r[ix['id']]]
            self.assertAlmostEqual(r[ix['menang2']] / 1000, x['r0.t2.0:menang'], delta=6e-4)
            self.assertAlmostEqual(r[ix['purata2']] / 10000, x['r0.t2.0:purata'], delta=6e-5)
            self.assertAlmostEqual(r[ix['rugi2']] / 1000, x['r0.t2.0:rugi15'], delta=6e-4)
            self.assertEqual(r[ix['hari2']], int(round(x['r0.t2.0:sesi_med'])))
            self.assertAlmostEqual(r[ix['menang']] / 1000, x['r0.t1.126:menang'], delta=6e-4)   # cara sekarang = angka CS14 yang sama
        b = d['banding']
        self.assertEqual(set(b), {'kini', 'lama', 'rawak_kini', 'rawak_lama'})
        self.assertGreater(b['lama']['purata'], b['kini']['purata'])                       # pegang lebih lama: purata naik ...
        self.assertLess(b['lama']['menang'], b['kini']['menang'])                           # ... dan kadar menang turun
        self.assertIn('minimum, bukan had', d['pegang'])
        self.assertIn('purata 50 hari', d['pegang2'])

    def test_lajur_solid_cs16(self):
        """CS16 "ujian solid" (pindaan (z), 16 Nov 2026): lajur di HUJUNG `kol`, dibaca terus daripada hasil/CS16/solid.csv.gz."""
        d = self.d
        ix = {k: i for i, k in enumerate(d['kol'])}
        self.assertEqual(d['kol'][:26], F.KOL[:26])                                       # lajur sedia ada tidak berganjak
        self.assertEqual(d['kol'][26:37], ['solid', 'wakil', 'boleh', 'm10', 'am10', 'm10d', 'am10d', 'tpos', 'tbil', 'rugi8', 'serupa'])
        Z = pd.read_csv(os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS16', 'solid.csv.gz')).set_index('id')
        self.assertEqual(sum(r[ix['wakil']] for r in d['rows']), int(Z.wakil.sum()))
        self.assertEqual(sum(r[ix['solid']] for r in d['rows']), int(Z.solid.sum()))
        self.assertEqual((d['solid']['n_wakil'], d['solid']['n_solid']), (224, 290))
        for r in self.utama[:60] + self.utama[-60:] + [x for x in d['rows'] if x[0] in ('F43', 'F58', 'F89')]:
            z = Z.loc[r[ix['id']]]
            self.assertEqual(bool(r[ix['solid']]), bool(z.solid))
            self.assertEqual(bool(r[ix['wakil']]), bool(z.wakil))
            self.assertEqual(bool(r[ix['boleh']]), bool(z.boleh_dibuat))
            for k, a in (('m10', 'm10'), ('am10', 'a_m10'), ('m10d', 'm10d'), ('am10d', 'a_m10d'), ('rugi8', 'rugi8')):
                self.assertAlmostEqual(r[ix[k]] / 1000, z[a], delta=6e-4, msg=k)
            self.assertEqual((r[ix['tpos']], r[ix['tbil']]), (int(z.thn_pos), int(z.thn_bil)))
            self.assertEqual(r[ix['serupa']], None if pd.isna(z.serupa_dengan) else z.serupa_dengan)
        f43 = [x for x in d['rows'] if x[0] == 'F43'][0]
        self.assertEqual(f43[ix['solid']], 0)                                             # F43 TIDAK solid (gagal S5)
        a = d['solid']['asas']                                                            # "laporan kewangan 1-5 sesi" sahaja
        self.assertEqual(a['prasyarat'], F.ASAS_EARN)
        self.assertAlmostEqual(a['m5'], 0.2404, places=3)
        self.assertAlmostEqual(a['a_m5'], 0.135, places=3)

    def test_lajur_audit_cs19(self):
        """CS19 audit bebas (pindaan (ae), 16 Nov 2026): 7 lajur selepas lajur CS16, terus daripada hasil/CS19/audit.csv.gz."""
        import json
        d = self.d
        ix = {k: i for i, k in enumerate(d['kol'])}
        self.assertEqual(d['kol'][:37], F.KOL[:37])                                       # lajur sedia ada tidak berganjak
        self.assertEqual(d['kol'][37:44], ['j5', 'aj5', 'am', 'ap', 'aud', 'aun', 'pt'])
        d19 = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS19')
        A = pd.read_csv(os.path.join(d19, 'audit.csv.gz')).set_index('id')
        B = json.load(open(os.path.join(d19, 'bacaan.json'), encoding='utf-8'))
        for r in self.utama[:80] + self.utama[-60:]:
            a = A.loc[r[ix['id']]]
            self.assertAlmostEqual(r[ix['j5']] / 1000, a.j5, delta=6e-4)
            self.assertAlmostEqual(r[ix['aj5']] / 1000, a.a_j5, delta=6e-4)
            self.assertAlmostEqual(r[ix['am']] / 1000, a.a_menang_B, delta=6e-4)
            self.assertAlmostEqual(r[ix['ap']] / 10000, a.a_purata_B, delta=6e-5)
            self.assertEqual(F.GRED_AUDIT[r[ix['aud']]], a.gred)
            self.assertEqual(r[ix['aun']] or '', '' if pd.isna(a.nota) else a.nota)
        pt = [r[ix['id']] for r in d['rows'] if r[ix['pt']]]
        self.assertEqual(sorted(pt), sorted(B['kohort']))                                 # 29 setup papertrade
        self.assertTrue(all(F.GRED_AUDIT[r[ix['aud']]] == 'A' for r in d['rows'] if r[ix['pt']]))
        u = d['audit']
        self.assertEqual((u['n'], u['diaudit'], u['pariti']), (d['n_utama'], B['diaudit'], B['pariti']))
        self.assertEqual(sum(u['gred_300'].values()), 300)
        self.assertGreater(u['atas']['semua']['jatuh5'], u['atas']['semua']['r_jatuh5'])   # jatuh >= 5 % pun melebihi saham rawak
        h = open(HTML, encoding='utf-8').read()                                           # halaman membaca lajur ikut nama
        for frasa in ("j5:g(a,'j5',10)", "aud:ix.aud==null", 'sfAuditD(r,d)', "f.lihat==='pt'", 'sf_audit:', 'sf_jatuh:', 'sf_mrawak:'):
            self.assertIn(frasa, h)

    def test_mingguan_dan_ukuran_kedua(self):
        """v189 (17 Nov 2026): setup sepanjang tahun CS20 (+ CS22) sebagai baris tambahan, dan ukuran kedua CS21 bagi semua baris;
        7 lajur di HUJUNG `kol`. Papertrade dijeda."""
        import json
        d = self.d
        ix = {k: i for i, k in enumerate(d['kol'])}
        self.assertEqual(d['kol'][:44], F.KOL[:44])                                        # lajur sedia ada tidak berganjak
        self.assertEqual(d['kol'][44:51], ['mg', 'mgg', 'bs', 'c10', 'ac10', 'j8', 'aj8'])
        hs = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil')
        B20 = json.load(open(os.path.join(hs, 'CS20', 'bacaan.json'), encoding='utf-8'))
        M = pd.read_csv(os.path.join(hs, 'CS20', 'mingguan.csv')).set_index('id')
        T21 = pd.read_csv(os.path.join(hs, 'CS21', 'unit.csv.gz'))
        T21 = T21[T21.kumpulan.str.startswith('F ')].drop_duplicates('id').set_index('id')
        self.assertTrue(all(r[ix['mg']] == 0 and r[ix['mgg']] is None for r in self.utama))
        mg = d['rows'][d['n_utama']:]
        self.assertTrue(all(r[ix['mg']] in (1, 2) for r in mg))
        mg1 = [r for r in mg if r[ix['mg']] == 1]
        self.assertEqual((len(mg1), d['mingguan']['n'], d['n_mingguan']), (B20['n_berdaftar'], B20['n_berdaftar'], len(mg)))
        self.assertEqual([r[0] for r in mg1], [f'F{i}' for i in range(2055, 2055 + len(mg1))])
        larang = ('earnings dalam', 'selepas earnings', 'tiada earnings', 'hari earnings', 'Nov-Apr', 'Mei-Okt', 'hari pertama bulan', 'Januari')
        for r in mg1[:60] + mg1[-60:]:
            m = M.loc[r[0]]
            self.assertAlmostEqual(r[ix['tangkap']] / 1000, m.terus, delta=6e-4)
            self.assertAlmostEqual(r[ix['rawak']] / 1000, m.a_terus, delta=6e-4)
            self.assertAlmostEqual(r[ix['menang']] / 1000, m.menang_B, delta=6e-4)
            self.assertAlmostEqual(r[ix['am']] / 1000, m.a_menang_B, delta=6e-4)
            self.assertAlmostEqual(r[ix['purata']] / 10000, m.purata_B, delta=6e-5)
            self.assertAlmostEqual(r[ix['j5']] / 1000, m.j5, delta=6e-4)
            self.assertAlmostEqual(r[ix['mgg']] / 1000, m.mgg_semua, delta=6e-4)
            self.assertEqual(r[ix['bs']], int(round(m.setahun_semua)))
            self.assertGreaterEqual(r[ix['mgg']], 800)                                    # membeli hampir setiap minggu
            self.assertEqual((r[ix['solid']], r[ix['pt']], r[ix['aud']], r[ix['menang2']], r[ix['shar']]), (0, 0, 0, None, None))
            self.assertFalse(any(x in d['kamus']['pra'][r[ix['pra']]] for x in larang))
        for r in self.utama[:60] + mg1[:60]:                                              # ukuran kedua terus daripada CS21
            if r[0] in T21.index:
                t = T21.loc[r[0]]
                for k, a in (('c10', 'c10'), ('ac10', 'a_c10'), ('j8', 'j8'), ('aj8', 'a_j8')):
                    self.assertAlmostEqual(r[ix[k]] / 1000, t[a], delta=6e-4, msg=k)
            else:
                self.assertIsNone(r[ix['c10']])
        self.assertGreater(sum(1 for r in d['rows'] if r[ix['c10']] is not None), 0.98 * len(d['rows']))
        uk = d['ukuran_kedua']
        self.assertTrue(0.35 < uk['dasar']['c10'] < 0.45 and uk['had'] == 63 and {'M', 'N', 'mingguan', 'laporan'} <= set(uk['kumpulan']))
        self.assertEqual(d['jeda']['papertrade'], os.path.exists(os.path.join(SINI, '..', 'jejak_f2', 'JEDA')))
        h = open(HTML, encoding='utf-8').read()
        for frasa in ("mg:ix.mg==null?0:a[ix.mg]||0", "c10:g(a,'c10',10)", "f.lihat==='mg'?all.filter(r=>r.mg)", "['mg',`Mingguan (", 'sfMgB(r)',
                      'PAPERTRADE · DIJEDA', 'sf_c10:', 'sf_mingguan:', '+10% dahulu ${Math.round(r.c10)}', "if(nMg&&!f._mg){f._mg=1;f.lihat='mg';}"):
            self.assertIn(frasa, h)

    def test_markah_cs23(self):
        """v190 (17 Nov 2026): markah 0-100 dan "Kegunaan bila?" (CS23) bagi setiap baris; 11 lajur di HUJUNG `kol`."""
        import json
        d = self.d
        ix = {k: i for i, k in enumerate(d['kol'])}
        self.assertEqual(d['kol'][:51], F.KOL[:51])                                        # lajur sedia ada tidak berganjak
        self.assertEqual(d['kol'][51:], ['mk', 'mka', 'mkb', 'mkc', 'mkd', 'mke', 'gn', 'tk', 'tg', 'sr23', 'mgb'])
        hs = os.path.join(SINI, '..', 'kajian', 'carian_setup', 'hasil', 'CS23')
        B = json.load(open(os.path.join(hs, 'bacaan.json'), encoding='utf-8'))
        T = pd.read_csv(os.path.join(hs, 'skor.csv.gz')).set_index('id')
        self.assertEqual(set(r[0] for r in d['rows']), set(T.index))                       # setiap baris ada rekod CS23
        rows = {r[0]: r for r in d['rows']}
        for i in list(T.index[:80]) + list(T.sample(80, random_state=2).index) + list(T.index[-31:]):
            r, t = rows[i], T.loc[i]
            self.assertEqual(F.GUNA[r[ix['gn']]], t.kegunaan, i)
            if not t.dinilai:
                self.assertEqual(([r[ix[k]] for k in ('mk', 'mka', 'mkb', 'mkc', 'mkd', 'mke')], r[ix['tk']], r[ix['tg']]), ([None] * 6, 0, 0), i)
                continue
            self.assertEqual(r[ix['mk']], int(round(t.markah * 10)), i)
            for k, a in (('mka', 'mA'), ('mkb', 'mB'), ('mkc', 'mC'), ('mkd', 'mD'), ('mke', 'mE')):
                self.assertAlmostEqual(r[ix[k]] / 10, t[a], delta=0.051, msg=f'{i} {k}')
            self.assertEqual((r[ix['tk']], r[ix['tg']]), (int(t.kedudukan), int(t.kedudukan_guna)), i)
            self.assertEqual(r[ix['sr23']], t.serupa_dengan if isinstance(t.serupa_dengan, str) else None, i)
            self.assertAlmostEqual(r[ix['mgb']] / 1000, t.minggu, delta=6e-4, msg=i)
        top = [r for r in d['rows'] if 0 < r[ix['tk']] <= 100]
        self.assertEqual(len(top), 100)
        for g, nama in enumerate(F.GUNA):
            n = sum(1 for r in d['rows'] if r[ix['gn']] == g and 0 < r[ix['tg']] <= 100)
            self.assertEqual(n, min(100, B['disimpan_kegunaan'][nama]), nama)
            self.assertEqual(sum(1 for r in top if r[ix['gn']] == g), B['top_kegunaan'][nama], nama)
        self.assertTrue(all((r[ix['tk']] > 0) == (r[ix['tg']] > 0) for r in d['rows']))
        self.assertTrue(all(not (r[ix['tk']] and r[ix['sr23']]) for r in d['rows']))       # berkedudukan ATAU serupa, bukan kedua-dua
        k = d['skor']
        self.assertEqual((k['n'], k['dinilai'], k['serupa'], k['disimpan'], k['guna']), (len(d['rows']), B['dinilai'], B['serupa'], B['disimpan'], F.GUNA))
        self.assertEqual(k['berat'], {'A': 35, 'B': 15, 'C': 20, 'D': 20, 'E': 10})
        self.assertEqual(k['top_guna']['Setiap minggu']['n'], 100)
        import cs_skor23
        self.assertEqual(tuple(F.GUNA), cs_skor23.GUNA)
        h = open(HTML, encoding='utf-8').read()
        for frasa in ("mk:g(a,'mk',10)", "gn:ix.gn==null?null:a[ix.gn]", "['top','Top 100']", "segH('sfGuna',f.guna,", "th('markah','Markah',1,'sf_markah')",
                      "th('guna','Kegunaan bila?',0,'sf_guna')", 'sfSkorD(r,d)', 'sf_markah:', 'sf_guna:', "f.lihat='top';f.guna='minggu';f.sk='markah'",
                      "r.gn===G&&r.tg>0&&r.tg<=100", 'Markah menyusun; ia bukan ujian dan bukan bukti'):
            self.assertIn(frasa, h)
        self.assertEqual(__import__('re').findall(r"\['([^']+)','#[0-9A-F]{6}','#[0-9A-F]{6}','[^']+'\]", h.split('const SF_GN=')[1].split(';')[0]),
                         F.GUNA)                                                           # susunan label halaman = susunan GUNA

    def test_paparan_mudah_v191(self):
        """v191 (17 Nov 2026): paparan mudah ialah lalai; had warna dikunci di sini (ditulis sebelum dipasang,
        standard/dashboard.md v191). Mengubah had memerlukan keputusan pengguna + nota bertarikh."""
        h = open(HTML, encoding='utf-8').read()
        self.assertIn("if(f.mod===undefined)f.mod='mudah';", h)                           # lalai
        self.assertIn("if(f.mod==='mudah'){sfxLukis(el,d,f,all);return;}", h)
        self.assertIn('id="sfxKePenuh"', h)                                                # paparan lama kekal boleh dibuka
        self.assertIn('id="sfxKeMudah"', h)
        self.assertIn("nis>=1.6?{t:'Lebih baik',k:2,w:'h'}:nis>=1.1?{t:'Baik sedikit',k:1,w:'k'}", h)   # lawan rawak
        self.assertIn("r.menang>=55?'h':r.menang>=45?'k':'m'", h)                         # kerap untung
        self.assertIn("r.rugi8<=15?'h':r.rugi8<=25?'k':'m'", h)                           # jatuh >= 8 %
        for kehendak in ('Boleh beli setiap minggu', 'Bukan beli hari ini, jual hari ini', 'Lebih baik daripada pilih rawak',
                         'Rugi paling banyak 5%', 'Naik perlahan tapi stabil'):
            self.assertIn(kehendak, h)
        self.assertIn('backtest, belum bukti', h)                                          # kaveat kekal pada setiap kad
        for lajur in ('nama', 'pra', 'pen', 'tangkap', 'rawak', 'menang', 'rugi8', 'gn', 'mk', 'tg', 'tk', 'mgb'):
            self.assertIn(lajur, self.d['kol'])                                            # tiada lajur db baharu diperlukan

    def test_saiz_di_bawah_had_db(self):
        with tempfile.TemporaryDirectory() as t:
            out = F.main(['--keluar', t])
            self.assertGreaterEqual(len(out), 1)
            self.assertEqual(out[0]['doc_id'], 'f_utama')
            for o in out:
                self.assertEqual(o['collection'], 'carian')
                self.assertLess(o['bait'], HAD_DB)
                self.assertTrue(os.path.exists(o['file_path']))
        self.assertLess(bait(self.d), 4 * HAD_DB)

    def test_halaman_membaca_dengan_subbhg(self):
        """Dokumen ini dibahagi dengan bahagi(); halaman MESTI membacanya dengan subBhg() (pelajaran jana_db.PECAH)."""
        h = open(HTML, encoding='utf-8').read()
        self.assertIn("subBhg('carian/f_utama','sf',['setupf'])", h)
        self.assertIn('<section class="view" id="v-setupf" hidden></section>', h)
        self.assertIn("['setupf','Setup F']", h)
        self.assertIn('setupf:renderSetupF', h)
        for k in F.KOL:                                                         # setiap lajur yang dibaca halaman wujud dalam dokumen
            if k not in ('beli', 'n', 'm5'):
                self.assertRegex(h, r"ix\.%s\b|'%s'" % (k, k), k)


if __name__ == '__main__':
    unittest.main()
