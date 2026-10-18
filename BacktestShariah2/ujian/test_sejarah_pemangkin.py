# Ujian pengurai data sejarah pemangkin: standard/sejarah_pemangkin_actions.py (Actions, sekali jalan)
import io, os, sys, unittest, zipfile
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'standard'))
import sejarah_pemangkin_actions as SP  # noqa: E402


def zip_sec(fail):
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z:
        for nama, baris in fail.items():
            z.writestr(nama, '\n'.join('\t'.join(r) for r in baris) + '\n')
    return b.getvalue()


class UjiSejarahPemangkin(unittest.TestCase):
    def test_baris_analisis_semua_sejarah(self):
        idx = pd.to_datetime(['2026-10-14 12:00', '2014-03-03 02:00'])
        df = pd.DataFrame({'Firm': ['UBS', 'Citi'], 'ToGrade': ['Buy', 'Sell'], 'FromGrade': ['Neutral', ''],
                           'Action': ['Up', 'init'], 'priceTargetAction': ['Raises', ''],
                           'currentPriceTarget': [150.0, float('nan')], 'priorPriceTarget': [130.0, 0.0]}, index=idx)
        a = SP.baris_analisis('ACME', df)
        self.assertEqual(a[0], ['ACME', '2026-10-14', 'UBS', 'Neutral', 'Buy', 'up', 'Raises', 150.0, 130.0])
        self.assertEqual(a[1][1], '2014-03-02')  # 02:00 UTC = petang sebelumnya di New York
        self.assertEqual(a[1][7], '')
        self.assertEqual(SP.baris_analisis('ACME', pd.DataFrame()), [])

    def test_baris_eps(self):
        idx = pd.DatetimeIndex(['2026-07-30 16:05'], tz='America/New_York')
        df = pd.DataFrame({'EPS Estimate': [1.2], 'Reported EPS': [1.5], 'Surprise(%)': [25.0]}, index=idx)
        self.assertEqual(SP.baris_eps('ACME', df), [['ACME', '2026-07-30', '16:05', 1.2, 1.5, 25.0]])

    def test_baca_sec_belian_jualan_sahaja(self):
        z = zip_sec({
            '2024q1/SUBMISSION.tsv': [['ACCESSION_NUMBER', 'FILING_DATE', 'DOCUMENT_TYPE', 'ISSUERTRADINGSYMBOL', 'AFF10B5ONE'],
                                      ['a1', '05-JAN-2024', '4', 'acme', '0'], ['a2', '06-JAN-2024', '4', 'ZZZ', '0'],
                                      ['a3', '07-JAN-2024', '3', 'ACME', '0']],
            '2024q1/NONDERIV_TRANS.tsv': [['ACCESSION_NUMBER', 'TRANS_DATE', 'TRANS_CODE', 'TRANS_SHARES', 'TRANS_PRICEPERSHARE',
                                           'TRANS_ACQUIRED_DISP_CD'],
                                          ['a1', '03-JAN-2024', 'P', '100', '10'], ['a1', '03-JAN-2024', 'P', '300', '12'],
                                          ['a1', '03-JAN-2024', 'M', '50', '1'], ['a2', '03-JAN-2024', 'P', '5', '1'],
                                          ['a3', '03-JAN-2024', 'P', '5', '1']],
            '2024q1/REPORTINGOWNER.tsv': [['ACCESSION_NUMBER', 'RPTOWNERCIK', 'RPTOWNERNAME', 'RPTOWNER_RELATIONSHIP', 'RPTOWNER_TITLE'],
                                          ['a1', '9', 'Doe John', 'Director', '']]})
        d = SP.baca_sec(z, ['ACME'])
        self.assertEqual(len(d), 1)
        r = d.iloc[0]
        self.assertEqual((r['ticker'], r['kod'], r['tarikh_fail'], r['tarikh_dagang'], r['pemilik']),
                         ('ACME', 'P', '2024-01-05', '2024-01-03', 'Doe John'))
        self.assertEqual(r['saham'], 400)
        self.assertAlmostEqual(r['harga'], 11.5)


if __name__ == '__main__':
    unittest.main()
