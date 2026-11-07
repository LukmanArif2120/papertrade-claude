"""Ujian dashboard v160 (7 Nov 2026, audit papar): kontrak antara dashboard_v2.html dan kad_skor.py / lift_kaedah.py,
dan janji paparan yang boleh disemak tanpa pelayar.

Semakan pelayar penuh (Chromium + stub db) ialah `ujian/semak_keputusan_papar.js`; ujian ini menangkap hanyutan yang
paling murah ditangkap: medan yang halaman baca tetapi penulisnya berhenti tulis, ayat tindakan yang halaman pecah,
dan sumber "Dibeli pada buka" dalam panel Esok.
"""
import os
import re
import sys
import unittest

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STD = os.path.join(AKAR, 'BacktestShariah2', 'standard')
sys.path.insert(0, STD)
sys.path.insert(0, os.path.join(AKAR, 'BacktestShariah2', 'kod'))
import kad_skor as KS  # noqa: E402

HTML = open(os.path.join(STD, 'dashboard_v2.html'), encoding='utf-8').read()
SRC_KS = open(os.path.join(STD, 'kad_skor.py'), encoding='utf-8').read()
SRC_LK = open(os.path.join(STD, 'lift_kaedah.py'), encoding='utf-8').read()


def fungsi(nama):
    """Badan satu fungsi tingkat atas halaman (`function nama(` hingga `\\nfunction ` / `\\nconst ` seterusnya)."""
    m = re.search(r'\n(?:function %s\(|const %s=)' % (re.escape(nama), re.escape(nama)), HTML)
    assert m, nama
    akhir = re.search(r'\n(?:function |const |/\*)', HTML[m.end():])
    return HTML[m.start():m.end() + (akhir.start() if akhir else len(HTML))]


class TestKontrakKadSkor(unittest.TestCase):
    """Setiap medan pindaan 7 Nov 2026 yang halaman baca mesti masih ditulis oleh kad_skor.py."""

    META = ('rejim', 'tindakan', 'hari_on', 'hari_off', 'tajuk', 'kira', 'mula_langsung')
    AMBANG = ('G1_REJIM_MIN', 'G3_UFUK', 'G6_SESI', 'G6_MDD_HAD')
    BARIS = ('buku_harian', 'buku_ci_bawah', 'buku_ci_atas', 'buku_sesi', 'hari_on', 'hari_off', 'lift_n',
             'mula_langsung', 't4_r10', 't4_spus_r10', 't4_nisbah', 't4_jalur_nisbah_maks', 't4_mdd', 't4_spus_mdd')

    def test_meta_ditulis(self):
        for k in self.META:
            self.assertRegex(SRC_KS, r'\b%s=' % k, f'kad_skor.py tidak lagi menulis meta `{k}`')
            self.assertIn(f'.{k}', HTML, f'halaman tidak membaca meta `{k}`')

    def test_ambang_ditulis_dan_dibaca(self):
        for k in self.AMBANG:
            self.assertRegex(SRC_KS, r'\b%s=' % k)
            self.assertIn(k, HTML)

    def test_medan_baris_ditulis(self):
        for f in self.BARIS:
            if f.startswith('t4_'):
                # lajur t4_* dibina daripada senarai kunci lorong T4 dengan awalan 't4_'
                self.assertIn(f"'{f[3:]}'", SRC_KS, f'kad_skor.py tidak lagi menulis `{f}`')
            else:
                self.assertRegex(SRC_KS, r'\b%s\b' % f, f'kad_skor.py tidak lagi menulis `{f}`')
            self.assertIn(f'.{f}', HTML, f'halaman tidak membaca `{f}`')

    def test_dokumen_baru_dikenal_pasti_dengan_ambang_g3_ufuk(self):
        # ksBaru(): dokumen pindaan = ambang.G3_UFUK ada. Jika kad_skor.py berhenti menulisnya, setiap teks gate
        # halaman jatuh balik kepada versi LAMA sambil status dikira dengan gate baharu.
        self.assertIn('const ksBaru=d=>!!(d&&d.ambang&&d.ambang.G3_UFUK!=null);', HTML)
        self.assertRegex(SRC_KS, r'G3_UFUK=lk\.UFUK')

    def test_ayat_tindakan_dipecah_seperti_halaman(self):
        # Halaman memapar bahagian aksi sahaja dalam baris Tindakan dan memindah kesan rejim ke tooltip.
        js = re.search(r'const mR=R&&R\.label\?/(.+?)/\.exec\(tind\)', HTML)
        self.assertIsNotNone(js, 'regex pemecah tindakan tiada dalam halaman')
        rx = re.compile(js.group(1))
        rj = dict(on=False, label='OFF', sejak='2026-10-16', sesi=16)
        ayat = KS.tindakan_hari_ini({'TERBUKTI': 0}, rj)
        m = rx.match(ayat)
        self.assertIsNotNone(m, f'ayat tindakan kad_skor.py tidak lagi sepadan: {ayat!r}')
        self.assertIn('JANGAN guna wang sebenar', m.group(1))
        self.assertNotIn('Rejim', m.group(1))
        self.assertTrue(m.group(2))
        # rejim ON: tiada ayat rejim, jadi halaman memapar ayat penuh
        self.assertIsNone(rx.match(KS.tindakan_hari_ini({'TERBUKTI': 0}, dict(rj, on=True, label='ON'))))


class TestHalaman(unittest.TestCase):

    def test_jalur_keputusan_blok_pertama_hari_ini(self):
        b = fungsi('renderUtama')
        isi = b[b.index('el.innerHTML=`', b.index('const p3=')):]
        self.assertTrue(isi.split('`', 1)[1].lstrip().startswith('${ksKeputusan()}'),
                        'jalur keputusan mesti blok pertama Hari ini')
        self.assertIn('Rejim QQQ: belum dikira', fungsi('ksKeputusan'), 'dokumen tanpa rejim mesti merosot dengan jelas')

    def test_jalur_keputusan_kekal_dalam_setiap_bahagian(self):
        self.assertIn("c.matches('.foot,.pn-tetap')", fungsi('pnavTanda'))
        self.assertIn('pn-tetap', fungsi('ksKeputusan'))

    def test_esok_dibeli_dari_senarai_beli(self):
        b = fungsi('panelEsok')
        self.assertIn('sbRows(sbD)', b)
        self.assertNotIn('wLengkap(', b, 'Esok tidak boleh lagi mengira isyarat lengkap watchlist')
        self.assertIn('PAPERTRADE', b)
        self.assertIn('kertas, bukan wang sebenar', b)

    def test_panel_lift_tanpa_lift_sebulan(self):
        b = HTML[HTML.index('const panelLift=()=>{'):HTML.index('/* ================= Pilih kaedah: kad skor keputusan')]
        self.assertNotIn("k:'sebulan'", b)
        self.assertNotIn("t:'Lift/bulan'", b)
        self.assertIn('Belum ada kaedah cukup data langsung; ujian pertama ~5 minggu.', b)
        # sebulan kini None dalam lift.json; jika ia kembali, halaman perlu diputuskan semula
        self.assertIn('sebulan=None', SRC_LK)

    def test_kad_skor_tidak_disusun_ikut_bilangan_gate(self):
        b = fungsi('renderAnalisis')
        self.assertIn('let rows=ksSusun(R);', b)
        s = fungsi('ksSusun')
        self.assertIn('x.lift', s)
        self.assertNotIn('gate', s)

    def test_teks_gate_lama_hanya_untuk_dokumen_lama(self):
        g = fungsi('ksG')
        self.assertIn('if(!ksBaru(d))return KS_G_LAMA', g)
        for lama in ('padan hari beli', '26.82', 'p95'):
            self.assertNotIn(lama, g)

    def test_kombinasi_n_ada_status_kad_skor(self):
        b = fungsi('renderKaedahN')
        self.assertIn("{k:'ks',t:'Kad skor'", b)


if __name__ == '__main__':
    unittest.main()
