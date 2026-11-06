/* Halaman mesti memuat PENUH walaupun pelanggan db mengehadkan langganan serentak.
 *
 * Pada 4 Nov 2026 diagnostik pada telefon pengguna melaporkan "Too many active subscriptions"
 * bagi analisis/papan_2, posisi/lorong2_18 dan posisi/jalur_2..4 — pada db yang SEMPURNA.
 * Halaman membuka 71 langganan serentak; yang didaftar terakhir ditolak, dan tab yang
 * bergantung padanya memapar "belum ditolak ke pangkalan data" sampai muat semula.
 *
 * Ujian ini meniru had itu: mock db menolak langganan melebihi had dengan ralat yang SAMA,
 * mengira puncak serentak, dan menghormati unsubscribe. Halaman lulus hanya jika setiap tab
 * tetap terisi DAN puncak serentak tidak melebihi had pelanggan.
 *
 * SEMPADAN YANG DIKETAHUI: langganan KEKAL (satu bagi setiap dokumen asas, supaya tolakan db
 * malam sampai ke halaman yang sudah terbuka) DAN kumpulan terbesar (ringkas_c: bilangan anaknya
 * tumbuh dengan Lejar; 26 pada 6 Nov 2026) mesti muat serentak, kerana slot anak hanya dilepaskan
 * selepas kumpulannya berhimpun. Angka semasa dicetak oleh ujian ini (puncak, aktif akhir), jadi
 * baca output dan bandingkan dengan KOLAM.maks dalam dashboard_v2.html - JANGAN salin nombor ke
 * komen ini (komen lama "22 kekal / 21 anak" hanyut dalam dua hari). Had sebenar yang
 * diperhatikan pada telefon pengguna ~60.
 * Kalau had pelanggan menjadi lebih ketat, pembetulan yang betul ialah menangguhkan
 * posisi/lorong2 (20 dokumen) sampai tab Posisi dibuka, bukan melonggarkan penghimpunan.
 *
 * Perlu Playwright (tiada dalam semak_data.yml) jadi ia dijalankan TANGAN:
 *   node BacktestShariah2/ujian/semak_kolam_langganan.js <folder-db> [had] [fail-html]
 */
const fs = require('fs'), path = require('path'), os = require('os');
const { chromium } = require('playwright');
const DB = process.argv[2];
const HAD = +(process.argv[3] || 30);
const HTML = process.argv[4] || path.join(__dirname, '..', 'standard', 'dashboard_v2.html');
if (!DB) { console.error('guna: node semak_kolam_langganan.js <folder-db> [had] [fail-html]'); process.exit(2); }

const D = {};
for (const c of fs.readdirSync(DB)) {
  const p = path.join(DB, c);
  if (!fs.statSync(p).isDirectory()) continue;
  for (const f of fs.readdirSync(p)) if (f.endsWith('.json')) D[c + '/' + f.slice(0, -5)] = JSON.parse(fs.readFileSync(path.join(p, f), 'utf8'));
}

(async () => {
  const S = fs.mkdtempSync(path.join(os.tmpdir(), 'kolam-'));
  let h = fs.readFileSync(HTML, 'utf8');
  if (!/^\s*<!doctype/i.test(h)) h = '<!doctype html><html><head><meta charset=utf8></head><body>' + h + '</body></html>';
  fs.writeFileSync(path.join(S, 'd.html'), h);
  const br = await chromium.launch({ args: ['--headless', '--no-sandbox'] });
  const pg = await br.newPage({ viewport: { width: 1400, height: 1000 } });
  const ralat = [];
  pg.on('pageerror', e => ralat.push(String(e).slice(0, 180)));
  await pg.addInitScript(([docs, had]) => {
    window.__D = docs; window.__aktif = 0; window.__puncak = 0; window.__tolak = 0; window.__had = had;
    /* Pelanggan db sebenar menghantar salinan CACHE dahulu, kemudian nilai pelayan. Salinan
       cache itu boleh datang dari sesi LAIN, jadi `induk`-nya tidak sepadan. Langganan yang
       ditutup selepas snapshot PERTAMA membeku pada salinan itu dan melaporkan "(induk lain)"
       selama-lamanya pada dokumen yang di pelayan sempurna — diperhatikan pada telefon
       pengguna 4 Nov 2026. Mock ini meniru urutan itu, jadi ujian menangkapnya. */
    const basi = (d) => {
      if (!d || typeof d !== 'object') return d;
      const c = Object.assign({}, d);
      if (c.induk) c.induk = 'CACHE-LAMA';
      if (c.bahagian && typeof c.bahagian === 'object') c.bahagian = Object.assign({}, c.bahagian, { id: 'CACHE-LAMA-2' });
      return c;
    };
    const buka = (kunci, cb) => {
      if (window.__aktif >= window.__had) { window.__tolak++; setTimeout(() => cb.err(new Error('Too many active subscriptions.')), 0); return function () {}; }
      window.__aktif++; window.__puncak = Math.max(window.__puncak, window.__aktif);
      let hidup = true;
      setTimeout(() => { if (hidup) cb.ok(true); }, 0);      // snapshot cache
      setTimeout(() => { if (hidup) cb.ok(false); }, 120);   // nilai pelayan
      return function () { if (hidup) { hidup = false; window.__aktif--; } };
    };
    window.claude = { use: async function () { return {
      collection: function (c) { return { limit: function () { return { onSnapshot: function (ok, err) {
        return buka('COL/' + c, { ok: () => ok({ docs: Object.keys(window.__D).filter(k => k.indexOf(c + '/') === 0).map(k => ({ id: k.slice(c.length + 1), exists: true, data: () => window.__D[k] })) }), err: err || function () {} });
      } }; } }; },
      doc: function (q) { return { onSnapshot: function (ok, err) {
        return buka(q, { ok: (cache) => ok({ exists: !!window.__D[q], data: () => cache ? basi(window.__D[q]) : window.__D[q] }), err: err || function () {} });
      } }; } }; } };
  }, [D, HAD]);
  await pg.goto('file://' + path.join(S, 'd.html'));
  await pg.waitForTimeout(25000);          // kolam + backoff perlu masa; 20s pemasa anti-tergantung juga lepas
  /* v155+: 5 tab atas; Posisi dan Rujukan ialah KUMPULAN yang bahagiannya dipilih dengan #kumpSeg.
     Setiap bahagian dinilai berasingan (kunci = data-k bahagian, cth `kaedahn`). */
  const atas = await pg.$$eval('#mainTabs button[data-tab]', bs => bs.map(b => b.dataset.tab));
  const tabs = [], out = {};
  const ukur = () => pg.evaluate(() => {
    const el = document.querySelector('section.view:not([hidden])');
    const ep = el.querySelector('.panel.empty');
    return { baris: el.querySelectorAll('table tbody tr').length, kosong: ep ? ep.textContent.trim().slice(0, 60) : null };
  });
  for (const t of atas) {
    await (await pg.$(`#mainTabs button[data-tab="${t}"]`)).click();
    await pg.waitForTimeout(900);
    const bhg = await pg.$$eval('#kumpSeg:not([hidden]) button', bs => bs.map(b => b.dataset.k)).catch(() => []);
    if (!bhg.length) { tabs.push(t); out[t] = await ukur(); continue; }
    for (const k of bhg) {
      await (await pg.$(`#kumpSeg button[data-k="${k}"]`)).click();
      await pg.waitForTimeout(900);
      tabs.push(k); out[k] = await ukur();
    }
  }
  const st = await pg.evaluate(() => ({ aktif: window.__aktif, puncak: window.__puncak, tolak: window.__tolak }));
  await br.close();
  console.log(`had pelanggan ${HAD} · puncak ${st.puncak} · aktif akhir ${st.aktif} · ditolak ${st.tolak}`);
  for (const t of tabs) console.log('  ' + t.padEnd(10), JSON.stringify(out[t]));
  const gagal = [];
  if (ralat.length) gagal.push('ralat halaman: ' + ralat.join(' | '));
  if (st.puncak > HAD) gagal.push(`puncak serentak ${st.puncak} melebihi had pelanggan ${HAD}`);
  // Tab yang bergantung pada dokumen berbahagi MESTI terisi walaupun had ketat.
  for (const [t, perlu] of [['analisis', 1], ['posisi', 1], ['prestasi', 1], ['kaedahn', 1]])
    if (!out[t] || out[t].baris < perlu) gagal.push(`${t}: ${out[t] ? out[t].baris : '?'} baris — ${out[t] && out[t].kosong || 'kosong'}`);
  if (gagal.length) { console.error('\nGAGAL:\n  ' + gagal.join('\n  ')); process.exit(1); }
  console.log('\nLULUS');
})();
