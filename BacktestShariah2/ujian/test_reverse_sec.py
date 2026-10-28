"""Masa ketersediaan data SEC (REVERSE/teras/sec.py; SPEC_FASA2.md §4.2).

52% earnings 8-K difail selepas tutup, jadi `tarikh_fail` sebagai tarikh ketersediaan memberi lebih
separuh peristiwa maklumat kira-kira satu sesi lebih awal. Ujian ini mengunci peraturan itu.
"""
import os, sys, unittest

import pandas as pd

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(AKAR, 'REVERSE'))
from teras import sec as S  # noqa: E402

# Isn 2026-10-19 .. Jum 2026-10-30, tanpa Rab 2026-10-21 (cuti ujian: sesi bukan kalendar kalendar).
SESI = [pd.Timestamp(x) for x in
        ['2026-10-19', '2026-10-20', '2026-10-22', '2026-10-23',
         '2026-10-26', '2026-10-27', '2026-10-28', '2026-10-29', '2026-10-30']]


def satu(masa, sesi=None, sandaran=None):
    return S.hari_tersedia([masa], sesi or SESI,
                           tarikh_sandaran=None if sandaran is None else [sandaran]).iloc[0]


class TestHariTersedia(unittest.TestCase):
    def test_pra_buka_sesi_sama(self):
        # 06:00 ET Selasa = 10:00 UTC (EDT, UTC-4): buka Selasa belum berlaku.
        self.assertEqual(satu('2026-10-20T10:00:00Z'), pd.Timestamp('2026-10-20'))

    def test_tepat_sebelum_buka_sesi_sama(self):
        self.assertEqual(satu('2026-10-20T13:29:00Z'), pd.Timestamp('2026-10-20'))

    def test_tepat_pada_buka_sesi_berikut(self):
        # 09:30 ET bukan lagi "sebelum buka": harga buka itu sendiri tidak boleh didagangkan atas maklumat ini.
        self.assertEqual(satu('2026-10-20T13:30:00Z'), pd.Timestamp('2026-10-22'))

    def test_intraday_sesi_berikut(self):
        self.assertEqual(satu('2026-10-20T15:00:00Z'), pd.Timestamp('2026-10-22'))

    def test_selepas_tutup_sesi_berikut(self):
        # 20:15 ET Selasa = 00:15 UTC Rabu. Rabu bukan sesi -> Khamis.
        self.assertEqual(satu('2026-10-21T00:15:00Z'), pd.Timestamp('2026-10-22'))

    def test_selepas_tutup_jumaat_langkau_hujung_minggu(self):
        self.assertEqual(satu('2026-10-23T21:00:00Z'), pd.Timestamp('2026-10-26'))

    def test_cuti_dilangkau(self):
        # Difail selepas tutup Selasa; Rabu cuti -> Khamis.
        self.assertEqual(satu('2026-10-20T21:00:00Z'), pd.Timestamp('2026-10-22'))

    def test_waktu_musim_sejuk_est(self):
        # 1 Dis 2026: EST (UTC-5). 14:00 UTC = 09:00 ET = pra-buka, sesi sama.
        sesi = [pd.Timestamp('2026-12-01'), pd.Timestamp('2026-12-02')]
        self.assertEqual(satu('2026-12-01T14:00:00Z', sesi), pd.Timestamp('2026-12-01'))
        # 14:00 UTC pada musim panas = 10:00 EDT = intraday, sesi berikut. Offset tetap akan tersalah.
        sesi = [pd.Timestamp('2026-07-01'), pd.Timestamp('2026-07-02')]
        self.assertEqual(satu('2026-07-01T14:00:00Z', sesi), pd.Timestamp('2026-07-02'))

    def test_peraturan_dst_sebelum_2007(self):
        # 2005: EDT bermula April (bukan Mac). 11 Mac 2005 ialah EST, jadi 14:00 UTC = 09:00 ET = pra-buka.
        sesi = [pd.Timestamp('2005-03-11'), pd.Timestamp('2005-03-14')]
        self.assertEqual(satu('2005-03-11T14:00:00Z', sesi), pd.Timestamp('2005-03-11'))

    def test_sandaran_dianggap_selepas_tutup(self):
        # sumber_tarikh == 'fail': waktu tidak diketahui -> konservatif, sesi SELEPAS tarikh itu.
        self.assertEqual(satu(None, sandaran='2026-10-20'), pd.Timestamp('2026-10-22'))

    def test_tiada_masa_dan_tiada_sandaran(self):
        self.assertTrue(pd.isna(satu(None)))

    def test_selepas_sesi_terakhir_nat(self):
        self.assertTrue(pd.isna(satu('2026-11-05T21:00:00Z')))

    def test_sesi_tidak_tersusun_tetap_betul(self):
        self.assertEqual(satu('2026-10-20T10:00:00Z', list(reversed(SESI))), pd.Timestamp('2026-10-20'))

    def test_tidak_mendahului_tarikh_fail_cuti_edgar(self):
        """28 Okt 2026: 8-K diterima Ahad, filingDate Selasa (EDGAR tutup Isnin, NYSE buka) -> Selasa, bukan Isnin."""
        self.assertEqual(satu('2026-10-25T22:00:00Z', sandaran='2026-10-27'), pd.Timestamp('2026-10-27'))
        # pra-buka pada filingDate kekal sesi sama
        self.assertEqual(satu('2026-10-27T12:00:00Z', sandaran='2026-10-27'), pd.Timestamp('2026-10-27'))

    def test_tidak_pernah_mendahului_pemfailan(self):
        """Sifat utama: hari tersedia mesti >= tarikh ET pemfailan, bagi setiap baris data sebenar."""
        p = os.path.join(AKAR, 'BacktestShariah2', 'data', 'sec', 'earnings_8k.csv')
        if not os.path.exists(p):
            self.skipTest('data/sec/earnings_8k.csv tiada')
        k = pd.read_csv(p, usecols=['masa_terima']).head(4000)
        ny = pd.to_datetime(k.masa_terima, utc=True, errors='coerce').dt.tz_convert(S.NY)
        sesi = pd.bdate_range('2004-01-01', '2027-06-30')
        h = S.hari_tersedia(k.masa_terima, sesi)
        ada = h.notna() & ny.notna()
        self.assertTrue(ada.any())
        self.assertTrue((h[ada].dt.normalize() >= ny[ada].dt.normalize().dt.tz_localize(None)).all())


if __name__ == '__main__':
    unittest.main()
