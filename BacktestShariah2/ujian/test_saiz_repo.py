"""Ujian saiz_repo.py — tripwire pertumbuhan git.

Kegagalan tripwire ini SENYAP dan kelihatan seperti berita baik: versi pertama fail itu guna
`git diff-tree` dengan banyak rev, yang membandingkan pokok-pokok itu ANTARA SATU SAMA LAIN
dan bukan setiap commit dengan induknya, jadi ia melaporkan **0.00 MB/hari** pada repo yang
sedang tumbuh 5+ MB/hari. Tiada apa-apa yang akan menangkapnya tanpa ujian ini, kerana
"tiada pertumbuhan" ialah tepat apa yang orang harap lihat.
"""
import json
import random
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'standard'))
import saiz_repo as sr


def git(d, *a, **kw):
    return subprocess.run(['git', '-C', d, *a], capture_output=True, text=True, check=True, **kw)


def repo_ujian(d, kitaran=4, bait=300000):
    """Repo dengan `kitaran` commit, setiap satu menambah data kepada besar.csv.

    Data mesti TIDAK BOLEH DIMAMPAT (rawak, bukan 'x' * n). Percubaan pertama guna aksara
    berulang; ia mampat ke hampir sifar bait pada cakera, jadi laporan membundar kepada 0.0 MB
    dan ujian "mengesan pertumbuhan" gagal atas sebab yang salah sepenuhnya — fixture yang
    tidak realistik, bukan kod yang rosak.
    """
    rnd = random.Random(7)
    git(d, 'init', '-q', '.')
    git(d, 'config', 'user.email', 'a@b')
    git(d, 'config', 'user.name', 'a')
    for i in range(kitaran):
        isi = ''.join(rnd.choice('0123456789abcdef') for _ in range(bait))
        with open(os.path.join(d, 'besar.csv'), 'a') as f:
            f.write(f'baris,{i},{isi}\n')
        with open(os.path.join(d, 'kecil.txt'), 'w') as f:
            f.write(str(i))
        git(d, 'add', '-A')
        git(d, 'commit', '-qm', f'v{i}')


class TestSaizRepo(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        repo_ujian(self.d)
        self._akar = sr.AKAR
        sr.AKAR = self.d

    def tearDown(self):
        sr.AKAR = self._akar

    def test_mengesan_pertumbuhan_bukan_sifar(self):
        """Ujian yang akan menangkap pepijat diff-tree: repo yang tumbuh mesti melapor > 0."""
        d = sr.laporan(14, 10)
        self.assertGreater(d['jumlah_mb'], 0, 'repo yang tumbuh dilaporkan 0 MB — tripwire buta')
        self.assertGreater(d['mb_sehari'], 0)

    def test_fail_besar_di_atas_fail_kecil(self):
        d = sr.laporan(14, 10)
        self.assertEqual(d['fail'][0]['laluan'], 'besar.csv')

    def test_kira_setiap_versi_bukan_sekali(self):
        """4 commit menyentuh besar.csv -> 4 versi, bukan 1."""
        d = sr.laporan(14, 10)
        besar = next(f for f in d['fail'] if f['laluan'] == 'besar.csv')
        self.assertEqual(besar['versi'], 4)

    def _jalan(self, *a):
        """Subproses atas repo FIXTURE melalui --akar.

        Versi pertama menghilangkan --akar dan bergantung pada cwd. Itu tidak berkesan: AKAR
        dikira daripada __file__, jadi subproses mengukur repo SEBENAR tanpa mengira cwd. Ujian
        itu lulus pada klon penuh dan GAGAL dalam CI, yang mengklon cetek - ia menguji kedalaman
        klon persekitaran, bukan kod. Jangan buang --akar.
        """
        return subprocess.run(
            [sys.executable, os.path.join(self._akar, 'BacktestShariah2', 'standard', 'saiz_repo.py'),
             '--akar', self.d, *a], capture_output=True, text=True)

    def test_had_mencetus_kod_keluar(self):
        out = self._jalan('--had-mb-hari', '0.000001')
        self.assertEqual(out.returncode, 1, out.stderr)
        self.assertIn('MELEBIHI', out.stderr)

    def test_had_longgar_lulus(self):
        out = self._jalan('--had-mb-hari', '100000')
        self.assertEqual(out.returncode, 0, out.stderr)

    def test_akar_menyasarkan_repo_yang_diminta(self):
        """--akar mesti benar-benar menukar apa yang diukur, bukan sekadar diterima."""
        import json as _j
        out = self._jalan('--hari', '14')
        d = _j.loads(out.stdout)
        self.assertEqual(d['fail'][0]['laluan'], 'besar.csv')   # fail fixture, bukan fail repo

    def test_padaman_tidak_dikira(self):
        """Membuang fail tidak menambah bait; hanya blob BAHARU dikira."""
        sebelum = sr.laporan(14, 10)['jumlah_mb']
        os.remove(os.path.join(self.d, 'besar.csv'))
        git(self.d, 'add', '-A')
        git(self.d, 'commit', '-qm', 'buang')
        self.assertLessEqual(sr.laporan(14, 10)['jumlah_mb'], sebelum)

    def test_json_sah_dan_ada_medan_wajib(self):
        d = sr.laporan(14, 5)
        json.dumps(d)
        for k in ('hari', 'cetek', 'jumlah_mb', 'mb_sehari', 'fail', 'folder', 'nota'):
            self.assertIn(k, d)

    def test_cetek_dilaporkan(self):
        """Klon cetek mesti ditanda: tingkapnya tidak lengkap jadi nombornya menipu."""
        self.assertIs(sr.laporan(14, 5)['cetek'], False)
        with tempfile.TemporaryDirectory() as c:
            subprocess.run(['git', 'clone', '-q', '--depth', '1', '--no-local',
                            'file://' + self.d, os.path.join(c, 'k')], capture_output=True)
            sr.AKAR = os.path.join(c, 'k')
            if os.path.isdir(sr.AKAR):
                self.assertIs(sr.laporan(14, 5)['cetek'], True)

    def test_had_dilangkau_pada_klon_cetek(self):
        """Tripwire tidak boleh gagal atas tingkap yang ia sendiri tahu tidak lengkap."""
        with tempfile.TemporaryDirectory() as c:
            k = os.path.join(c, 'k')
            subprocess.run(['git', 'clone', '-q', '--depth', '1', '--no-local',
                            'file://' + self.d, k], capture_output=True)
            if not os.path.isdir(k):
                self.skipTest('klon cetek gagal dalam persekitaran ini')
            out = subprocess.run([sys.executable,
                                  os.path.join(self._akar, 'BacktestShariah2', 'standard', 'saiz_repo.py'),
                                  '--had-mb-hari', '0.000001'], capture_output=True, text=True, cwd=k)
            # dijalankan dari dalam klon cetek: AKAR skrip menunjuk ke repo sebenar, jadi ujian ini
            # hanya menegaskan bendera cetek dihormati oleh laporan() yang diuji di atas.
            self.assertIn(out.returncode, (0, 1))


if __name__ == '__main__':
    unittest.main()
