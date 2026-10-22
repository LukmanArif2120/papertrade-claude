# Ujian standard/tawaran_edgar.py (22 Okt 2026): penghurai indeks harian dan pengepala EDGAR, keputusan peranan sasaran,
# dan kemas kini data/ambil_alih.csv (tanpa rangkaian).
import os, sys, tempfile, unittest
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import tawaran_edgar as E  # noqa: E402

INDEKS = """Description:           Daily Index of EDGAR Dissemination Feed by Form Type
Last Data Received:    October 20, 2026
Comments:              webmaster@sec.gov
Anonymous FTP:         ftp://ftp.sec.gov/edgar/




Form Type   Company Name                                                  CIK         Date Filed  File Name
---------------------------------------------------------------------------------------------------------------------------------------------
10-Q             ACME CORP                                                     111111      20261020    edgar/data/111111/0000111111-26-000001.txt
425              BRAZE, INC.                                                   1676238     20261020    edgar/data/1676238/0001193125-26-400001.txt
425              SALESFORCE, INC.                                              1108524     20261020    edgar/data/1108524/0001193125-26-400001.txt
SC TO-T          BIG BIDDER LLC                                                2222222     20261020    edgar/data/2222222/0002222222-26-000009.txt
SC 14D9/A        TARGETCO INC                                                  3333333     20261020    edgar/data/3333333/0003333333-26-000002.txt
"""

KEPALA = """<html><body><pre>
<SEC-HEADER>0001193125-26-400001.hdr.sgml : 20261020
ACCESSION NUMBER:		0001193125-26-400001
CONFORMED SUBMISSION TYPE:	425
PUBLIC DOCUMENT COUNT:		1
FILED AS OF DATE:		20261020
SUBJECT COMPANY:

	COMPANY DATA:
		COMPANY CONFORMED NAME:			Braze, Inc.
		CENTRAL INDEX KEY:			0001676238

FILED BY:

	COMPANY DATA:
		COMPANY CONFORMED NAME:			Salesforce, Inc.
		CENTRAL INDEX KEY:			0001108524
</SEC-HEADER>
</pre></body></html>"""


class TestEdgar(unittest.TestCase):
    def test_hurai(self):
        ix = E.hurai_indeks(INDEKS)
        self.assertEqual(list(ix.borang), ['10-Q', '425', '425', 'SC TO-T', 'SC 14D9/A'])
        self.assertEqual((ix.cik.iloc[1], ix.tarikh.iloc[1], ix.akses.iloc[1]), (1676238, '2026-10-20', '0001193125-26-400001'))
        k = E.hurai_pengepala(KEPALA)
        self.assertEqual((k['borang'], k['subject'], k['filer']), ('425', [1676238], [1108524]))

    def test_putuskan(self):
        self.assertEqual(E.putuskan('425', dict(subject=[5], filer=[9])), ('aktif', 5))
        self.assertEqual(E.putuskan('425', dict(subject=[5, 7], filer=[9])), ('calon', 5))
        self.assertEqual(E.putuskan('SC TO-T/A', dict(subject=[5], filer=[9])), ('aktif', 5))
        self.assertEqual(E.putuskan('SC 14D9', dict(subject=[], filer=[5])), ('aktif', 5))
        self.assertEqual(E.putuskan('DEFM14A', dict(subject=[], filer=[5])), ('calon', 5))
        self.assertEqual(E.putuskan('25-NSE', dict(subject=[5], filer=[1])), ('tamat', 5))
        self.assertEqual(E.putuskan('SC TO-I', dict(subject=[5], filer=[5])), (None, None))
        self.assertEqual(E.peta_ticker({'0': dict(cik_str=5, ticker='BRK-B', title='x')}), {5: ['BRK.B']})

    def test_kemas_ambil(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'ambil_alih.csv')
            pd.DataFrame([dict(saham='PEN', tarikh_umum='2026-01-15', tarikh_tamat='', pembeli='Boston Scientific', harga_tawaran='374',
                               bayaran='campuran', sumber='x')]).to_csv(p, index=False)
            r = [dict(status='aktif', saham='BRZE', tarikh='2026-10-20', borang='425', akses='a1', pembeli='SALESFORCE'),
                 dict(status='aktif', saham='PEN', tarikh='2026-10-20', borang='425', akses='a2'),        # sudah aktif
                 dict(status='tamat', saham='PEN', tarikh='2026-10-21', borang='25-NSE', akses='a3')]
            self.assertEqual(E.kemas_ambil(r, p), (['BRZE'], ['PEN']))
            d2 = pd.read_csv(p, dtype=str, keep_default_na=False).set_index('saham')
            self.assertEqual((d2.loc['PEN', 'tarikh_tamat'], d2.loc['BRZE', 'bayaran'], d2.loc['BRZE', 'sumber']),
                             ('2026-10-21', 'edgar', 'EDGAR 425 a1'))
            self.assertEqual(E.kemas_ambil(r[:1], p), ([], []))


if __name__ == '__main__':
    unittest.main()
