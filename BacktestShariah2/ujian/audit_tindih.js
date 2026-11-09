/* Audit tindihan paparan dashboard (v172, 9 Nov 2026, keputusan pengguna "cuba check keseluruhan dashboard").
 *
 * Mencari tiga jenis cacat yang dilihat pengguna pada telefon:
 *   TINDIH   — dua teks bertindih pada skrin dan tiada lapisan legap di antaranya (contoh: bulatan G1–G6
 *              terapung di atas butang kaki helaian; label 0% menindih bilangan bar).
 *   POTONG   — teks terpotong oleh induk overflow:hidden tanpa elipsis (contoh: cip "ISYARAT JUA").
 *   LEBAR    — halaman lebih lebar daripada skrin (skrol mendatar).
 * Melawat SETIAP tab, kumpulan (#kumpSeg) dan bahagian rel (.pnav-in), dan membuka helaian posisi dan kaedah (setiap
 * sub-tab), pada komputer 1440×1000 dan telefon 390×660 (tinggi paparan dalam app Claude di iPhone); setiap keadaan diskrol dari atas ke bawah (halaman atau helaian)
 * supaya unsur melekit (pengepala, kaki helaian, bar tab bawah) diuji pada setiap kedudukan. Telefon meniru ruang
 * selamat iPhone (env(safe-area-inset-bottom) = 34px) kerana Chromium ujian memulangkan 0.
 *
 * Perlu Playwright dan folder db daripada jana_db.py; dijalankan TANGAN (tiada dalam semak_data.yml):
 *   python3 BacktestShariah2/standard/jana_db.py --keluar /tmp/db
 *   node BacktestShariah2/ujian/audit_tindih.js /tmp/db [fail-html]
 * Keluar 1 jika ada cacat. Tab Rujukan memerlukan kaedah/katalog.json dan registry/<ID>.json dalam folder db
 * (lihat standard/dashboard.md v171).
 */
const fs = require('fs'), path = require('path'), os = require('os');
const { chromium } = require('playwright');
const DB = process.argv[2], HTML = process.argv[3] || path.join(__dirname, '..', 'standard', 'dashboard_v2.html');
if (!DB) { console.error('guna: node audit_tindih.js <folder-db> [fail-html]'); process.exit(2); }
const D = {};
for (const c of fs.readdirSync(DB)) { const p = path.join(DB, c); if (!fs.statSync(p).isDirectory()) continue;
  for (const f of fs.readdirSync(p)) if (f.endsWith('.json')) D[c + '/' + f.slice(0, -5)] = JSON.parse(fs.readFileSync(path.join(p, f), 'utf8')); }

/* pemeriksa dalam halaman: semak_papar.js (dikongsi dengan audit_terperinci.js) */
const { semak } = require('./semak_papar.js');

(async () => {
  const S = fs.mkdtempSync(path.join(os.tmpdir(), 'tindih-'));
  const asal = fs.readFileSync(HTML, 'utf8');
  const br = await chromium.launch();
  const semua = [];
  for (const [nm, vp, mob] of [['komputer', { width: 1440, height: 1000 }, false], ['telefon', { width: 390, height: 660 }, true]]) {
    // telefon: tiru ruang selamat bawah iPhone (Chromium memulangkan 0 untuk env())
    const h = mob ? asal.replace(/env\(safe-area-inset-bottom,\s*0px\)/g, '34px') : asal;
    fs.writeFileSync(path.join(S, nm + '.html'), '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>' + h + '</body></html>');
    const pg = await br.newPage({ viewport: vp, isMobile: mob, hasTouch: mob });
    const er = []; pg.on('pageerror', e => er.push(String(e).slice(0, 160)));
    await pg.addInitScript(([docs]) => { window.__D = docs; window.claude = { use: async () => ({
      collection: c => ({ limit: () => ({ onSnapshot: (ok) => { setTimeout(() => ok({ docs: Object.keys(window.__D).filter(k => k.indexOf(c + '/') === 0).map(k => ({ id: k.slice(c.length + 1), exists: true, data: () => window.__D[k] })) }), 0); return () => {}; } }) }),
      doc: q => ({ onSnapshot: (ok) => { setTimeout(() => ok({ exists: !!window.__D[q], data: () => window.__D[q] }), 0); return () => {}; } }) }) }; }, [D]);
    await pg.goto('file://' + path.join(S, nm + '.html')); await pg.waitForTimeout(6000);
    const klik = async (s, t = 600) => { await pg.evaluate(s => { const e = document.querySelector(s); if (e) e.click(); }, s); await pg.waitForTimeout(t); };
    // skrol halaman (atau helaian) dari atas ke bawah, semak pada setiap langkah
    const imbas = async (label, helaian) => {
      const tinggi = await pg.evaluate(h => { const e = h ? document.querySelector('#sheet') : document.scrollingElement; e.scrollTop = 0; return [e.scrollHeight, e.clientHeight]; }, helaian);
      const f = helaian ? 0.22 : 0.8, langkah = Math.max(1, Math.min(40, Math.ceil(tinggi[0] / (tinggi[1] * f))));
      for (let s = 0; s < langkah; s++) {
        await pg.evaluate(([h, s, ch, f]) => { const e = h ? document.querySelector('#sheet') : document.scrollingElement; e.scrollTop = s * ch * f; }, [helaian, s, tinggi[1], f]);
        await pg.waitForTimeout(120);
        for (const d of await pg.evaluate(semak, `${nm} · ${label} · skrol ${s + 1}/${langkah}`)) semua.push(d);
      }
      await pg.evaluate(h => { const e = h ? document.querySelector('#sheet') : document.scrollingElement; e.scrollTop = 0; }, helaian);
    };
    const tabs = await pg.$$eval('#mainTabs button[data-tab]', bs => bs.map(b => b.dataset.tab));
    for (const t of tabs) {
      await klik(`#mainTabs button[data-tab="${t}"]`);
      const kump = await pg.$$eval('#kumpSeg:not([hidden]) button', bs => bs.map(b => b.dataset.k)).catch(() => []);
      for (const k of (kump.length ? kump : [null])) {
        if (k) await klik(`#kumpSeg button[data-k="${k}"]`, 900);
        const bh = await pg.$$eval('.pnav-in button', bs => bs.filter(b => b.getClientRects().length).map(b => b.textContent.trim().slice(0, 24)));
        for (let i = 0; i < Math.max(1, bh.length); i++) {
          await pg.evaluate(i => { const b = [...document.querySelectorAll('.pnav-in button')].filter(b => b.getClientRects().length)[i]; if (b) b.click(); }, i);
          await pg.waitForTimeout(500);
          await imbas(`${t}${k ? '/' + k : ''}${bh[i] ? ' › ' + bh[i] : ''}`, false);
        }
      }
    }
    for (const [tab, rx, sel, nmS] of [['posisi', 'keputusan', '[data-pos]', 'helaian posisi'], ['analisis', 'Kad skor setiap', '[data-kd]', 'helaian kaedah']]) {
      await klik(`#mainTabs button[data-tab="${tab}"]`);
      await pg.evaluate(() => { const b = document.querySelector('#kumpSeg:not([hidden]) button'); if (b) b.click(); }); await pg.waitForTimeout(800);
      await pg.evaluate(rx => { const b = [...document.querySelectorAll('.pnav-in button')].find(x => x.getClientRects().length && new RegExp(rx, 'i').test(x.textContent)); if (b) b.click(); }, rx);
      await pg.waitForTimeout(1200);
      const ada = await pg.evaluate(sel => { const e = [...document.querySelectorAll(sel)].find(x => x.getClientRects().length); if (!e) return false; e.scrollIntoView(); e.click();
        const buka = () => !!document.querySelector('#sheet:not([hidden]) .pv2');
        if (!buka()) { const b = e.querySelector('.mbtn-b') || (e.closest('tr') && e.closest('tr').querySelector('.mbtn-b')); if (b) b.click(); }
        return buka(); }, sel);
      await pg.waitForTimeout(1200);
      if (!ada) { semua.push({ jenis: 'UJIAN', a: nmS + ' tidak dapat dibuka', b: '', label: nm }); continue; }
      const st = await pg.$$eval('#sheet .pv2tabs button', bs => bs.map(b => b.textContent.trim()));
      for (let i = 0; i < Math.max(1, st.length); i++) {
        await pg.evaluate(i => { const b = document.querySelectorAll('#sheet .pv2tabs button')[i]; if (b) b.click(); }, i);
        await pg.waitForTimeout(700);
        await imbas(`${nmS} › ${st[i] || ''}`, true);
      }
      await pg.evaluate(() => { const c = document.querySelector('#sheet .pv2x,#sheet .close'); if (c) c.click(); }); await pg.waitForTimeout(400);
    }
    if (er.length) semua.push({ jenis: 'RALAT', a: er.slice(0, 3).join(' | '), b: '', label: nm });
    await pg.close();
  }
  await br.close();
  // satukan: satu baris setiap cacat unik, dengan keadaan pertama dan bilangan kejadian
  const U = new Map();
  for (const d of semua) { const k = d.jenis + '|' + d.a + '|' + d.b; const u = U.get(k); if (u) u.n++; else U.set(k, Object.assign({ n: 1 }, d)); }
  const L = [...U.values()].sort((x, y) => x.jenis.localeCompare(y.jenis) || x.label.localeCompare(y.label));
  for (const d of L) console.log(`${d.jenis.padEnd(6)} ${d.a}  ×  ${d.b}   [${d.label}]${d.n > 1 ? ' (x' + d.n + ')' : ''}`);
  console.log(`\n${L.length} cacat unik`);
  process.exit(L.length ? 1 : 0);
})();
