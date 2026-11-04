"""Ujian tripwire kesegaran `koordinator.py --semak`.

Jurang yang ia tutup: `amaran_ntfy.yml` hanya berbunyi apabila workflow GAGAL, dan kesegaran()
sudah mengira status LEWAT tetapi hanya MEMAPARKANNYA dalam KOORDINATOR.md. Keadaan "workflow
hijau, data tidak bergerak" tidak kelihatan melainkan seseorang membuka fail itu.

Dua sifat yang mesti dikunci, dan kedua-duanya gagal secara SENYAP jika rosak:
  - tripwire mesti MENGESAN data yang berhenti bergerak (jika tidak ia tidak berguna);
  - tripwire mesti TIDAK berbunyi pada cuti panjang (jika tidak ia dilatih untuk diabaikan,
    pada saluran ntfy yang sama dengan amaran sebenar).
"""
import os
import subprocess
import sys
import unittest

STD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard')
sys.path.insert(0, STD)
import koordinator as ko


class TestSemakSegar(unittest.TestCase):
    def setUp(self):
        self._asal = ko.kesegaran

    def tearDown(self):
        ko.kesegaran = self._asal

    def _palsu(self, baris):
        ko.kesegaran = lambda: [(n, t, u, 'x') for n, t, u in baris]

    def test_semua_segar_lulus(self):
        self._palsu([('Stor harga', '2026-11-03', 1), ('Lejar Penuh', '2026-11-03', 1)])
        kod, buruk = ko.semak_segar()
        self.assertEqual(kod, 0)
        self.assertEqual(buruk, [])

    def test_data_berhenti_bergerak_dikesan(self):
        self._palsu([('Stor harga', '2026-10-20', 15)])
        kod, buruk = ko.semak_segar()
        self.assertEqual(kod, 1)
        self.assertEqual(buruk[0][0], 'Stor harga')

    def test_cuti_panjang_tidak_berbunyi(self):
        """Khamis tutup + Jumaat cuti + hujung minggu = 4 hari kalendar, tiada yang rosak."""
        self._palsu([('Stor harga', '2026-11-26', 4), ('Lejar Penuh', '2026-11-26', 4)])
        self.assertEqual(ko.semak_segar()[0], 0)

    def test_ambang_lebih_longgar_daripada_paparan(self):
        """Paparan guna LEWAT_HARI=3; tripwire mesti lebih longgar atau ia berbunyi pada cuti."""
        self.assertGreater(ko.SEMAK_HARI, ko.LEWAT_HARI)

    def test_umur_tiada_dilangkau(self):
        """umur None = fail/medan tiada, ditangani di tempat lain; jangan amaran berganda."""
        self._palsu([('SEC fundamental', None, None), ('Stor harga', '2026-11-03', 1)])
        self.assertEqual(ko.semak_segar()[0], 0)

    def test_ambang_boleh_dilaras(self):
        self._palsu([('Stor harga', '2026-11-01', 4)])
        self.assertEqual(ko.semak_segar(lewat=5)[0], 0)
        self.assertEqual(ko.semak_segar(lewat=3)[0], 1)

    def test_cli_kod_keluar_dan_json(self):
        """--semak mesti mencetak JSON ke stdout dan pulang kod keluar yang betul."""
        import json
        out = subprocess.run([sys.executable, os.path.join(STD, 'koordinator.py'), '--semak'],
                             capture_output=True, text=True)
        self.assertIn(out.returncode, (0, 1))
        d = json.loads(out.stdout.strip().splitlines()[-1])
        for k in ('lewat_hari', 'bil', 'sumber'):
            self.assertIn(k, d)
        self.assertEqual(d['bil'], len(d['sumber']))

    def test_cli_semak_tidak_menulis_koordinator_md(self):
        """--semak ialah semakan sahaja: ia tidak boleh menjana semula KOORDINATOR.md."""
        p = os.path.join(os.path.dirname(STD), '..', 'KOORDINATOR.md')
        p = os.path.abspath(p)
        sebelum = os.path.getmtime(p) if os.path.exists(p) else None
        subprocess.run([sys.executable, os.path.join(STD, 'koordinator.py'), '--semak'],
                       capture_output=True, text=True)
        if sebelum is not None:
            self.assertEqual(os.path.getmtime(p), sebelum)


if __name__ == '__main__':
    unittest.main()
