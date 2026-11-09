/* Audit saiz fon dashboard (v170, 9 Nov 2026): lantai saiz — tiada teks yang dipapar lebih kecil daripada had.
 *
 * Melawat SETIAP tab utama, setiap kumpulan (#kumpSeg) dan setiap bahagian rel (.pnav-in), membuka helaian posisi
 * dan helaian kaedah (setiap sub-tab), pada komputer 1440px dan telefon 390px, lalu mengukur saiz fon SEBENAR setiap
 * elemen yang ada teks dan dipapar (teks SVG didarab skala carta pada skrin). Mencetak senarai di bawah had dan keluar 1
 * jika ada. Lantai semasa: label/cip 12.5px, penerangan 13px, carta 12px (blok v170 dalam dashboard_v2.html); had
 * lalai 11.8 memberi ruang pembundaran (12px x skala 0.99).
 *
 * Perlu Playwright dan folder db daripada jana_db.py; dijalankan TANGAN (tiada dalam semak_data.yml):
 *   python3 BacktestShariah2/standard/jana_db.py --keluar /tmp/db
 *   node BacktestShariah2/ujian/audit_fon.js /tmp/db [had] [fail-html]
 */
const fs=require('fs'),path=require('path'),os=require('os');const {chromium}=require('playwright');
const DB=process.argv[2],HAD=process.argv[3]||'11.8',HTML=process.argv[4]||path.join(__dirname,'..','standard','dashboard_v2.html');
if(!DB){console.error('guna: node audit_fon.js <folder-db> [had] [fail-html]');process.exit(2);}const D={};
for(const c of fs.readdirSync(DB)){const p=path.join(DB,c);if(!fs.statSync(p).isDirectory())continue;for(const f of fs.readdirSync(p))if(f.endsWith('.json'))D[c+'/'+f.slice(0,-5)]=JSON.parse(fs.readFileSync(path.join(p,f),'utf8'));}
const kumpul=()=>{const R=window.__R=window.__R||{};
  const ok=n=>n.nodeType===3&&n.textContent.trim().length>0;
  for(const el of document.body.querySelectorAll('*')){
    if(['SCRIPT','STYLE','TITLE','OPTION'].includes(el.tagName))continue;
    if(![...el.childNodes].some(ok))continue;
    const r=el.getClientRects();if(!r.length)continue; // hanya yang dipapar
    const cs=getComputedStyle(el);if(cs.visibility==='hidden'||+cs.opacity===0)continue;
    let fs=parseFloat(cs.fontSize);if(el.closest&&el.closest('svg')&&el.getScreenCTM){const m=el.getScreenCTM();if(m)fs=fs*Math.hypot(m.a,m.b);}
    const cl=x=>x&&x.getAttribute?((x.getAttribute('class')||'').trim().split(/\s+/).slice(0,2).join('.')):'';
    const k=el.tagName.toLowerCase()+(cl(el)?'.'+cl(el):'')+' < '+(el.parentElement?el.parentElement.tagName.toLowerCase()+(cl(el.parentElement)?'.'+cl(el.parentElement):''):'');
    const t=[...el.childNodes].filter(ok).map(n=>n.textContent.trim()).join(' ').slice(0,40);
    if(!R[k]||fs<R[k].fs)R[k]={fs,t,fam:cs.fontFamily.split(',')[0],n:(R[k]?R[k].n:0)+1};else R[k].n++;}};
(async()=>{const S=fs.mkdtempSync(path.join(os.tmpdir(),'a-'));fs.writeFileSync(path.join(S,'d.html'),'<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+fs.readFileSync(HTML,'utf8')+'</body></html>');
const br=await chromium.launch();const hasil={};
for(const [nm,vp,mob] of [['desk',{width:1440,height:1000},false],['fon',{width:390,height:844},true]]){
 const pg=await br.newPage({viewport:vp,isMobile:mob,hasTouch:mob,deviceScaleFactor:mob?2:1});const er=[];pg.on('pageerror',e=>er.push(String(e).slice(0,150)));
 await pg.addInitScript(([docs])=>{window.__D=docs;window.claude={use:async()=>({collection:c=>({limit:()=>({onSnapshot:(ok)=>{setTimeout(()=>ok({docs:Object.keys(window.__D).filter(k=>k.indexOf(c+'/')===0).map(k=>({id:k.slice(c.length+1),exists:true,data:()=>window.__D[k]}))}),0);return()=>{};}})}),doc:q=>({onSnapshot:(ok)=>{setTimeout(()=>ok({exists:!!window.__D[q],data:()=>window.__D[q]}),0);return()=>{};}})})};},[D]);
 await pg.goto('file://'+path.join(S,'d.html'));await pg.waitForTimeout(6000);
 const klik=async s=>{await pg.evaluate(s=>{const e=document.querySelector(s);if(e)e.click();},s);await pg.waitForTimeout(700);};
 const tabs=await pg.$$eval('#mainTabs button[data-tab]',bs=>bs.map(b=>b.dataset.tab));
 for(const t of tabs){await klik(`#mainTabs button[data-tab="${t}"]`);
  const kump=await pg.$$eval('#kumpSeg:not([hidden]) button',bs=>bs.map(b=>b.dataset.k)).catch(()=>[]);
  for(const k of (kump.length?kump:[null])){ if(k)await klik(`#kumpSeg button[data-k="${k}"]`);
   const n=await pg.$$eval('.pnav-in button',bs=>bs.filter(b=>b.getClientRects().length).length);
   for(let i=0;i<Math.max(1,n);i++){await pg.evaluate(i=>{const b=[...document.querySelectorAll('.pnav-in button')].filter(b=>b.getClientRects().length)[i];if(b)b.click();},i);await pg.waitForTimeout(500);await pg.evaluate(kumpul);}
  }}
 // helaian posisi + kaedah
 for(const [tab,sel,nmS] of [['posisi','[data-pos]','pos'],['analisis','[data-kd]','kd']]){
  await klik(`#mainTabs button[data-tab="${tab}"]`);
  await pg.evaluate(()=>{const b=document.querySelector('#kumpSeg:not([hidden]) button');if(b)b.click();});await pg.waitForTimeout(800);
  await pg.evaluate(rx=>{const b=[...document.querySelectorAll('.pnav-in button')].find(x=>x.getClientRects().length&&new RegExp(rx,'i').test(x.textContent));if(b)b.click();},nmS==='pos'?'keputusan':'Kad skor setiap');await pg.waitForTimeout(1200);
  const ada=await pg.evaluate(sel=>{const e=[...document.querySelectorAll(sel)].find(x=>x.getClientRects().length);if(!e)return false;e.scrollIntoView();e.click();
    if(!document.querySelector('#sheet .pv2')){const b=e.querySelector('.mbtn-b');if(b)b.click();}
    return !!document.querySelector('#sheet .pv2')||'tiada-helaian:'+e.tagName+'.'+e.className;},sel);
  await pg.waitForTimeout(1200);
  if(ada){const nt=await pg.$$eval('#sheet .pv2tabs button',bs=>bs.length);
   for(let i=0;i<Math.max(1,nt);i++){await pg.evaluate(i=>{const b=document.querySelectorAll('#sheet .pv2tabs button')[i];if(b)b.click();},i);await pg.waitForTimeout(600);await pg.evaluate(kumpul);}
   await pg.keyboard.press('Escape');await pg.evaluate(()=>{const c=document.querySelector('#sheet .pv2x,#sheet .close');if(c)c.click();});await pg.waitForTimeout(400);}
  console.log(nm,nmS,'helaian dibuka:',ada);}
 hasil[nm]=await pg.evaluate(()=>window.__R);if(er.length)console.log(nm,'ralat:',er.slice(0,3).join(' | '));await pg.close();}
await br.close();
let gagal=0;
for(const nm of Object.keys(hasil)){const L=Object.entries(hasil[nm]).filter(([k,v])=>v.fs<+HAD).sort((a,b)=>a[1].fs-b[1].fs);
 gagal+=L.length;console.log(`\n== ${nm}: ${L.length} jenis teks < ${HAD}px (daripada ${Object.keys(hasil[nm]).length})`);
 for(const [k,v] of L)console.log(v.fs.toFixed(1).padStart(5),'x'+String(v.n).padEnd(5),k.slice(0,70).padEnd(70),'|',v.t);}
if(gagal){console.error(`\nGAGAL: ${gagal} jenis teks di bawah ${HAD}px`);process.exit(1);}console.log('\nLULUS');
})();
