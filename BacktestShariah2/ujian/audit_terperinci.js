/* Audit paparan MENDALAM dashboard (v173, 9 Nov 2026, keputusan pengguna "cuba check lebih detail lagi").
 *
 * Lapan saiz skrin (telefon kecil 360, iPhone dalam app 390×660 dengan ruang selamat 34px, telefon besar 430,
 * tablet potret 768, tablet landskap 1024, komputer kecil 1280, komputer 1440, skrin lebar 1920). Setiap saiz:
 * setiap tab, kumpulan (#kumpSeg), segmen sub-bar (#jenisSeg/#setSeg/#subSeg: akaun, set watchlist …) dan bahagian
 * rel (.pnav-in), diskrol dari atas ke bawah. Saiz UTAMA (390×660 dan 1440) juga: setiap butang segmen dalam panel
 * (Ringkas/Penuh/Risiko/Gred, Lilin/Garis, Terkini/Terbaik …), mod Biasa (bukan Padat), kad telefon yang dibuka,
 * helaian posisi/kaedah/watchlist/panduan/status data (setiap sub-tab, diskrol halus), dan petua (tooltip) komputer.
 * Pemeriksa: semak_papar.js — TINDIH, POTONG, LEBAR, DATA, KONTRAS, SENTUH, BUTANG, LIMPAH; ditambah PETUA
 * (petua terkeluar dari skrin) dan RALAT (ralat JavaScript).
 *
 *   node BacktestShariah2/ujian/audit_terperinci.js <folder-db> [fail-html] [--pantas]
 * --pantas: saiz utama sahaja. Mengambil masa ~30–60 minit penuh. Keluar 1 jika ada cacat.
 * Folder db: jana_db.py --keluar, ditambah kaedah/katalog.json dan registry/<ID>.json (standard/dashboard.md v171).
 */
const fs = require('fs'), path = require('path'), os = require('os');
const { chromium } = require('playwright');
const { semak, semakLanjut } = require('./semak_papar.js');
const arg = process.argv.slice(2).filter(a => !a.startsWith('--')), PANTAS = process.argv.includes('--pantas');
const DB = arg[0], HTML = arg[1] || path.join(__dirname, '..', 'standard', 'dashboard_v2.html');
if (!DB) { console.error('guna: node audit_terperinci.js <folder-db> [fail-html] [--pantas]'); process.exit(2); }
const D = {};
for (const c of fs.readdirSync(DB)) { const p = path.join(DB, c); if (!fs.statSync(p).isDirectory()) continue;
  for (const f of fs.readdirSync(p)) if (f.endsWith('.json')) D[c + '/' + f.slice(0, -5)] = JSON.parse(fs.readFileSync(path.join(p, f), 'utf8')); }

const SAIZ = [
  // [nama, viewport, telefon?, utama?]
  ['iPhone 390×660', { width: 390, height: 660 }, true, true],
  ['komputer 1440×1000', { width: 1440, height: 1000 }, false, true],
  ['telefon kecil 360×640', { width: 360, height: 640 }, true, false],
  ['telefon besar 430×800', { width: 430, height: 800 }, true, false],
  ['tablet 768×1024', { width: 768, height: 1024 }, true, false],
  ['tablet 1024×768', { width: 1024, height: 768 }, false, false],
  ['komputer 1280×720', { width: 1280, height: 720 }, false, false],
  ['skrin lebar 1920×1080', { width: 1920, height: 1080 }, false, false],
].filter(s => !PANTAS || s[3]);

(async () => {
  const S = fs.mkdtempSync(path.join(os.tmpdir(), 'terperinci-'));
  const asal = fs.readFileSync(HTML, 'utf8');
  const br = await chromium.launch();
  const semua = [];
  for (const [nm, vp, mob, utama] of SAIZ) {
    const t0 = Date.now();
    const h = mob ? asal.replace(/env\(safe-area-inset-bottom,\s*0px\)/g, '34px') : asal;
    const fail = path.join(S, nm.replace(/\W+/g, '_') + '.html');
    fs.writeFileSync(fail, '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>' + h + '</body></html>');
    const pg = await br.newPage({ viewport: vp, isMobile: mob, hasTouch: mob });
    const er = []; pg.on('pageerror', e => er.push(String(e).slice(0, 160)));
    await pg.addInitScript(([docs]) => { window.__D = docs; window.claude = { use: async () => ({
      collection: c => ({ limit: () => ({ onSnapshot: (ok) => { setTimeout(() => ok({ docs: Object.keys(window.__D).filter(k => k.indexOf(c + '/') === 0).map(k => ({ id: k.slice(c.length + 1), exists: true, data: () => window.__D[k] })) }), 0); return () => {}; } }) }),
      doc: q => ({ onSnapshot: (ok) => { setTimeout(() => ok({ exists: !!window.__D[q], data: () => window.__D[q] }), 0); return () => {}; } }) }) }; }, [D]);
    await pg.goto('file://' + fail); await pg.waitForTimeout(6000);
    await pg.addStyleTag({ content: '*{scroll-behavior:auto!important}' });
    const tunggu = t => pg.waitForTimeout(t);
    const periksa = async (label) => { for (const d of await pg.evaluate(semak, `${nm} · ${label}`)) semua.push(d);
      for (const d of await pg.evaluate(semakLanjut, { label: `${nm} · ${label}`, mob })) semua.push(d); };
    const imbas = async (label, helaian, f) => {
      const tg = await pg.evaluate(h => { const e = h ? document.querySelector('#sheet') : document.scrollingElement; e.scrollTop = 0; return [e.scrollHeight, e.clientHeight]; }, helaian);
      const langkah = Math.max(1, Math.min(40, Math.ceil(tg[0] / (tg[1] * f))));
      for (let s = 0; s < langkah; s++) {
        await pg.evaluate(([h, s, ch, f]) => { const e = h ? document.querySelector('#sheet') : document.scrollingElement; e.scrollTop = s * ch * f; }, [helaian, s, tg[1], f]);
        await tunggu(100); await periksa(`${label} · skrol ${s + 1}/${langkah}`);
      }
      await pg.evaluate(h => { const e = h ? document.querySelector('#sheet') : document.scrollingElement; e.scrollTop = 0; }, helaian);
    };
    const klikSel = async (sel, t = 600) => { await pg.evaluate(s => { const e = document.querySelector(s); if (e) e.click(); }, sel); await tunggu(t); };
    const klikTeks = async (sel, rx, t = 600) => { const ok = await pg.evaluate(([s, rx]) => { const b = [...document.querySelectorAll(s)].find(x => x.getClientRects().length && new RegExp(rx, 'i').test(x.textContent)); if (b) { b.click(); return true; } return false; }, [sel, rx]); await tunggu(t); return ok; };
    const bahagian = () => pg.$$eval('.pnav-in button', bs => bs.filter(b => b.getClientRects().length).map(b => b.textContent.trim().slice(0, 26)));
    const keBahagian = async i => { await pg.evaluate(i => { const b = [...document.querySelectorAll('.pnav-in button')].filter(b => b.getClientRects().length)[i]; if (b) b.click(); }, i); await tunggu(450); };
    // butang segmen dalam panel bagi paparan semasa: klik setiap satu, periksa skrin, pulihkan pilihan asal
    const segPanel = async (label) => {
      const kump = await pg.evaluate(() => [...document.querySelectorAll('section.view:not([hidden]) .seg')].filter(s => s.getClientRects().length && !s.closest('#subBar'))
        .map((s, gi) => { s.dataset.auditSeg = gi; const bs = [...s.querySelectorAll('button')]; return { gi, n: bs.length, asal: bs.findIndex(b => b.getAttribute('aria-pressed') === 'true' || b.getAttribute('aria-selected') === 'true') }; }));
      for (const g of kump.slice(0, 8)) {
        if (g.asal < 0) continue;   // kumpulan tanpa pilihan aktif = butang tindakan, bukan togol (tidak boleh dipulihkan)
        for (let i = 0; i < Math.min(g.n, 6); i++) {
          if (i === g.asal) continue;
          const t = await pg.evaluate(([gi, i]) => { const s = document.querySelector(`[data-audit-seg="${gi}"]`); if (!s) return null; const b = s.querySelectorAll('button')[i]; if (!b) return null; b.scrollIntoView({ block: 'center' }); b.click(); return b.textContent.trim().slice(0, 20); }, [g.gi, i]);
          if (t == null) continue; await tunggu(500);
          await periksa(`${label} › segmen "${t}"`);
          await pg.evaluate(([gi, a]) => { const s = document.querySelector(`[data-audit-seg="${gi}"]`); if (s && a >= 0) { const b = s.querySelectorAll('button')[a]; if (b) b.click(); } }, [g.gi, g.asal]); await tunggu(350);
        }
      }
    };
    // ===== 1. setiap tab / kumpulan / segmen sub-bar / bahagian =====
    const tabs = await pg.$$eval('#mainTabs button[data-tab]', bs => bs.map(b => b.dataset.tab));
    for (const t of tabs) {
      await klikSel(`#mainTabs button[data-tab="${t}"]`);
      const kump = await pg.$$eval('#kumpSeg:not([hidden]) button', bs => bs.map(b => b.dataset.k)).catch(() => []);
      for (const k of (kump.length ? kump : [null])) {
        if (k) await klikSel(`#kumpSeg button[data-k="${k}"]`, 900);
        const tag = `${t}${k ? '/' + k : ''}`;
        const bh = await bahagian();
        for (let i = 0; i < Math.max(1, bh.length); i++) {
          await keBahagian(i);
          const lb = `${tag}${bh[i] ? ' › ' + bh[i] : ''}`;
          await imbas(lb, false, 0.8);
          if (utama) await segPanel(lb);
        }
        // segmen sub-bar selain kumpulan (akaun Papertrade C·M / C·N / Moomoo, set watchlist …): bahagian pertama sahaja
        const sb = await pg.$$eval('#subBar .seg:not(#kumpSeg) button', bs => bs.filter(b => b.getClientRects().length).map((b, i) => ({ i, t: b.textContent.trim().slice(0, 22), on: b.getAttribute('aria-pressed') === 'true' || b.getAttribute('aria-selected') === 'true' })));
        const asalSb = sb.filter(x => x.on).map(x => x.i);
        for (const b of sb) { if (b.on) continue;
          await pg.evaluate(i => { const x = [...document.querySelectorAll('#subBar .seg:not(#kumpSeg) button')].filter(b => b.getClientRects().length)[i]; if (x) x.click(); }, b.i); await tunggu(800);
          await keBahagian(0); await imbas(`${tag} › sub-bar "${b.t}"`, false, 0.8); }
        for (const i of asalSb) { await pg.evaluate(i => { const x = [...document.querySelectorAll('#subBar .seg:not(#kumpSeg) button')].filter(b => b.getClientRects().length)[i]; if (x) x.click(); }, i); await tunggu(500); }
      }
    }
    if (utama) {
      // ===== 2. mod Biasa (bukan Padat): jadual utama =====
      await klikSel('#padTog', 700);
      for (const [t, rx] of [['posisi', 'keputusan'], ['rujukan', null]]) {
        await klikSel(`#mainTabs button[data-tab="${t}"]`); await klikSel('#kumpSeg:not([hidden]) button', 800);
        if (rx) await klikTeks('.pnav-in button', rx, 900);
        await imbas(`mod Biasa · ${t}`, false, 0.8);
      }
      await klikSel('#padTog', 700);
      // ===== 3. kad telefon dibuka (ketik baris) =====
      if (mob) {
        await klikSel('#mainTabs button[data-tab="posisi"]'); await klikSel('#kumpSeg:not([hidden]) button', 800); await klikTeks('.pnav-in button', 'keputusan', 900);
        const ok = await pg.evaluate(() => { const r = [...document.querySelectorAll('.tw-lp tr[data-lp], .tw-grd tr[data-pos]')].find(x => x.getClientRects().length); if (!r) return false; r.scrollIntoView({ block: 'start' }); r.click(); return true; });
        await tunggu(700); if (ok) await periksa('kad posisi telefon dibuka');
      }
      // ===== 4. helaian =====
      const bukaHelaian = async (tab, kumpI, rx, sel) => {
        await klikSel(`#mainTabs button[data-tab="${tab}"]`);
        if (kumpI != null) await pg.evaluate(i => { const b = document.querySelectorAll('#kumpSeg:not([hidden]) button')[i]; if (b) b.click(); }, kumpI);
        await tunggu(800); if (rx) await klikTeks('.pnav-in button', rx, 1100);
        const ok = await pg.evaluate(sel => { const e = [...document.querySelectorAll(sel)].find(x => x.getClientRects().length); if (!e) return false; e.scrollIntoView(); e.click();
          const buka = () => !!document.querySelector('#sheet:not([hidden])');
          if (!buka() || !document.querySelector('#sheet:not([hidden]) .pv2,#sheet:not([hidden]) h3')) { const b = e.querySelector('.mbtn-b') || (e.closest('tr') && e.closest('tr').querySelector('.mbtn-b')); if (b) b.click(); }
          return buka(); }, sel);
        await tunggu(1200); return ok;
      };
      const imbasHelaian = async (nmS) => {
        const st = await pg.$$eval('#sheet .pv2tabs button', bs => bs.map(b => b.textContent.trim()));
        for (let i = 0; i < Math.max(1, st.length); i++) {
          await pg.evaluate(i => { const b = document.querySelectorAll('#sheet .pv2tabs button')[i]; if (b) b.click(); }, i); await tunggu(700);
          await imbas(`${nmS}${st[i] ? ' › ' + st[i] : ''}`, true, 0.22);
          // segmen dalam helaian (Lilin/Garis, Terkini/Terbaik/Terburuk …)
          const n = await pg.$$eval('#sheet .seg button', bs => bs.length);
          for (let j = 0; j < Math.min(n, 8); j++) { const t = await pg.evaluate(j => { const b = document.querySelectorAll('#sheet .seg button')[j]; if (!b || b.getAttribute('aria-pressed') === 'true' || b.getAttribute('aria-selected') === 'true') return null; b.scrollIntoView({ block: 'center' }); b.click(); return b.textContent.trim().slice(0, 16); }, j);
            if (t) { await tunggu(400); await periksa(`${nmS}${st[i] ? ' › ' + st[i] : ''} › segmen "${t}"`); } }
        }
        await pg.evaluate(() => { const c = document.querySelector('#sheet .pv2x,#sheet .close'); if (c) c.click(); }); await tunggu(400);
      };
      for (const [tab, kumpI, rx, sel, nmS] of [['posisi', 0, 'keputusan', '[data-pos]', 'helaian posisi'], ['analisis', null, 'Kad skor setiap', '[data-kd]', 'helaian kaedah'],
        ['posisi', 1, null, '[data-wl]', 'helaian watchlist']]) {
        if (await bukaHelaian(tab, kumpI, rx, sel)) await imbasHelaian(nmS); else semua.push({ jenis: 'UJIAN', a: nmS + ' tidak dapat dibuka', b: '', label: nm });
      }
      for (const [sel, nmS] of [['[data-panduan]', 'helaian panduan'], ['#salH', 'helaian status data']]) {
        await klikSel('#mainTabs button[data-tab="utama"]');
        const ok = await pg.evaluate(s => { const e = [...document.querySelectorAll(s)].find(x => x.getClientRects().length); if (!e) return false; e.click(); return !document.querySelector('#sheet').hidden; }, sel);
        await tunggu(900); if (ok) await imbasHelaian(nmS); else semua.push({ jenis: 'UJIAN', a: nmS + ' tidak dapat dibuka', b: '', label: nm });
      }
      // ===== 5. petua (komputer): mesti berada dalam skrin =====
      if (!mob) for (const t of ['utama', 'analisis', 'posisi']) {
        await klikSel(`#mainTabs button[data-tab="${t}"]`); await keBahagian(0);
        const n = await pg.$$eval('[data-tip]', es => es.filter(e => { const r = e.getBoundingClientRect(); return r.width && r.top > 0 && r.bottom < innerHeight; }).length);
        for (let i = 0; i < Math.min(n, 12); i++) {
          const box = await pg.evaluate(i => { const e = [...document.querySelectorAll('[data-tip]')].filter(e => { const r = e.getBoundingClientRect(); return r.width && r.top > 0 && r.bottom < innerHeight; })[i]; if (!e) return null; const r = e.getBoundingClientRect(); return { x: r.left + Math.min(r.width / 2, 20), y: r.top + r.height / 2, k: e.dataset.tip }; }, i);
          if (!box) continue; await pg.mouse.move(box.x, box.y); await tunggu(350);
          const r = await pg.evaluate(() => { const t = document.querySelector('.tip'); if (!t || t.hidden || getComputedStyle(t).display === 'none') return null; const r = t.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom, innerWidth, innerHeight]; });
          if (r && (r[0] < 0 || r[1] < 0 || r[2] > r[4] + 1 || r[3] > r[5] + 1)) semua.push({ jenis: 'PETUA', a: `petua "${box.k}" keluar skrin`, b: r.slice(0, 4).map(Math.round).join(','), label: `${nm} · ${t}` });
        }
        await pg.mouse.move(1, 1);
      }
    }
    if (er.length) semua.push({ jenis: 'RALAT', a: er.slice(0, 3).join(' | '), b: '', label: nm });
    await pg.close();
    console.error(`[${nm}] siap dalam ${Math.round((Date.now() - t0) / 1000)} s`);
  }
  await br.close();
  const U = new Map();
  for (const d of semua) { const k = d.jenis + '|' + d.a + '|' + d.b; const u = U.get(k); if (u) { u.n++; u.saiz.add(d.label.split(' · ')[0]); } else U.set(k, Object.assign({ n: 1, saiz: new Set([d.label.split(' · ')[0]]) }, d)); }
  const L = [...U.values()].sort((x, y) => x.jenis.localeCompare(y.jenis) || x.a.localeCompare(y.a));
  for (const d of L) console.log(`${d.jenis.padEnd(7)} ${d.a}  ×  ${d.b}   [${d.label}]${d.n > 1 ? ' (x' + d.n + ', ' + [...d.saiz].join(' / ') + ')' : ''}`);
  const J = {}; for (const d of L) J[d.jenis] = (J[d.jenis] || 0) + 1;
  console.log(`\n${L.length} cacat unik: ${Object.entries(J).map(([k, v]) => k + ' ' + v).join(', ') || '-'}`);
  process.exit(L.length ? 1 : 0);
})();
