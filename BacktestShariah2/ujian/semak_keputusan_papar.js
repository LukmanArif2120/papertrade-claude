// Semakan tingkah laku dashboard v160 (7 Nov 2026, audit papar): memuatkan dashboard_v2.html sebenar dalam Chromium
// dengan stub db daripada cakera (sama seperti semak_dashboard.js) dan menyemak JANJI halaman, bukan susun atur:
//   1  jalur keputusan 3 baris di atas Hari ini (status + tajuk, tindakan, rejim) dan ia kekal dalam setiap bahagian
//   2  "Dibeli pada buka" dalam Esok = bilangan baris papertrade/senarai_beli (sumber yang sama dengan Senarai beli)
//      dan cipnya membuka Senarai beli yang ditapis kepada saham itu
//   3  jadual kad skor memakai lajur gate pindaan 7 Nov 2026 (dokumen baharu) atau lajur lama (dokumen lama), dan
//      susunan lalai dalam setiap status = lift menurun (null di bawah), bukan bilangan gate lulus
//   4  panel Lift tiada lajur "Lift/bulan"; keadaan kosong jelas apabila tiada kaedah diuji
//   5  label purata setiap posisi kertas (bukan akaun) dalam Hari ini dan Akaun
//   6  jadual Produksi Kombinasi N ada lajur status kad skor
// Sifar ralat konsol / pageerror diwajibkan.
//
// Guna:
//   python3 BacktestShariah2/standard/jana_db.py --keluar /tmp/db
//   node BacktestShariah2/ujian/semak_keputusan_papar.js /tmp/db [lebar ...]
// Kod keluar 1 jika ada kegagalan.
const fs=require('fs'),path=require('path'),os=require('os');
const {chromium}=require('playwright');
const DB=process.argv[2];
if(!DB){console.error('guna: node semak_keputusan_papar.js <folder db jana_db> [lebar ...]');process.exit(2);}
const LEBAR=process.argv.slice(3).map(Number).filter(Boolean);
const HTML=path.join(path.dirname(__dirname),'standard','dashboard_v2.html');
const S=fs.mkdtempSync(path.join(os.tmpdir(),'dashk-'));
fs.writeFileSync(path.join(S,'live.html'),'<!doctype html><html><head><meta charset=utf8><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+fs.readFileSync(HTML,'utf8')+'</body></html>');
/* Semua fail <koleksi>/<doc>.json dalam folder (bukan hanya yang disenaraikan batch), supaya dokumen yang diganti
   dengan tangan untuk ujian (cth. kad_skor.json contoh) tetap dimuat. */
const D={};
for(const c of fs.readdirSync(DB))if(fs.statSync(path.join(DB,c)).isDirectory())
  for(const f of fs.readdirSync(path.join(DB,c)).filter(f=>f.endsWith('.json')))
    D[c+'/'+f.slice(0,-5)]=JSON.parse(fs.readFileSync(path.join(DB,c,f),'utf8'));
const KS=D['analisis/kad_skor']||null,LF=D['analisis/lift']||null,SB=D['papertrade/senarai_beli']||null;
const baruKS=!!(KS&&KS.ambang&&KS.ambang.G3_UFUK!=null);
/* senarai beli boleh dibahagi (bahagi_db.py): asas + <nama>_2.. dengan induk sama */
const sbN=SB?(SB.rows||[]).length+Object.keys(D).filter(k=>/^papertrade\/senarai_beli_\d+$/.test(k)&&SB.bahagian&&D[k].induk===SB.bahagian.id).reduce((t,k)=>t+(D[k].rows||[]).length,0):null;
const nf=n=>Number(n).toLocaleString('en-US');
let gagal=0;const ok=(c,m)=>{if(!c){gagal++;console.log('GAGAL '+m);}else console.log('ok    '+m);};

(async()=>{
  const b=await chromium.launch({args:['--no-sandbox']});
  for(const W of (LEBAR.length?LEBAR:[1400,390])){
    const ctx=await b.newContext({viewport:{width:W,height:W<700?844:900},deviceScaleFactor:1,isMobile:W<700,hasTouch:W<700});
    const p=await ctx.newPage();const ralat=[];
    p.on('console',m=>{if(m.type()==='error')ralat.push(m.text());});p.on('pageerror',e=>ralat.push(e.message));
    await p.addInitScript(docs=>{window.__D=docs;window.claude={use:async function(){return {
      collection:function(c){return {limit:function(){return {onSnapshot:function(cb){
        var ds=Object.keys(window.__D).filter(function(k){return k.indexOf(c+'/')===0;}).map(function(k){
          return {id:k.slice(c.length+1),exists:true,data:function(){return window.__D[k];}};});
        cb({docs:ds});return function(){};}};}};},
      doc:function(q){return {onSnapshot:function(cb){cb({exists:!!window.__D[q],data:function(){return window.__D[q];}});return function(){};}};}};}};},D);
    await p.goto('file://'+S+'/live.html');await p.waitForTimeout(3000);
    const pergi=async t=>{await p.evaluate(t=>document.querySelector(`#mainTabs button[data-tab="${t}"]`).click(),t);await p.waitForTimeout(700);};
    const pn=async awalan=>p.evaluate(a=>{const b=[...document.querySelectorAll('aside.rail .pnav-in button, section.view:not([hidden]) .pnav-in button')].filter(x=>x.offsetParent&&x.dataset.pnk.startsWith(a))[0];if(!b)return false;b.click();return true;},awalan);
    const T=`[${W}px]`;

    /* 1 jalur keputusan */
    await pergi('utama');
    const bn=await p.evaluate(()=>{const v=document.querySelector('#v-utama'),k=v&&v.querySelector(':scope>.kputus');if(!k)return null;
      const pertama=[...v.children].filter(c=>!c.classList.contains('pnav-rail'))[0]===k;
      return {pertama,baris:k.querySelectorAll(':scope>.kpl').length,teks:k.innerText,rj:(k.querySelector('.kprj')||{}).className||'',nampak:!!k.offsetParent};});
    ok(bn&&bn.pertama,`${T} jalur keputusan ialah blok pertama Hari ini`);
    ok(bn&&bn.baris===3&&bn.nampak,`${T} jalur keputusan 3 baris dan kelihatan`);
    if(bn){
      ok(/TERBUKTI \d/.test(bn.teks)&&/NEGATIF \d/.test(bn.teks),`${T} baris status memapar bilangan setiap status`);
      if(KS&&KS.tajuk)ok(bn.teks.includes(KS.tajuk.slice(0,30)),`${T} baris status memapar tajuk kad skor`);
      ok(/JANGAN guna wang sebenar|TERBUKTI —/.test(bn.teks),`${T} baris tindakan ada`);
      if(KS&&KS.rejim){ok(new RegExp('Rejim QQQ: '+KS.rejim.label).test(bn.teks)&&bn.rj.includes(KS.rejim.on?'on':'off'),`${T} rejim ${KS.rejim.label} berwarna betul`);
        ok(/dari puncak 52 minggu/.test(bn.teks)&&/SMA50/.test(bn.teks),`${T} rejim memapar QQQ lawan SMA50 dan jarak dari puncak`);
        if(KS.hari_on!=null)ok(bn.teks.includes(`Data hadapan: ON ${KS.hari_on} hari beli, OFF ${KS.hari_off}`),`${T} data hadapan ON/OFF dipapar`);}
      else ok(/Rejim QQQ: belum dikira/.test(bn.teks),`${T} dokumen tanpa rejim: "belum dikira"`);}
    const tip=await p.evaluate(()=>{const e=document.querySelector('#v-utama .kprj');if(!e)return '';e.dispatchEvent(new MouseEvent('mouseover',{bubbles:true}));const t=document.querySelector('.tip');return t&&!t.hidden?t.innerText:'';});
    ok(/ON =|ON\/OFF|ON \/ OFF/.test(tip),`${T} tooltip rejim memapar takrif`);
    if(await pn('esok')){
      const kekal=await p.evaluate(()=>{const k=document.querySelector('#v-utama>.kputus');return !!(k&&k.offsetParent);});
      ok(kekal,`${T} jalur keputusan kekal kelihatan dalam bahagian Esok`);}

    /* 2 Esok = senarai beli */
    const es=await p.evaluate(()=>{const h=[...document.querySelectorAll('#v-utama .esh')].find(x=>/Dibeli pada buka/i.test(x.textContent));if(!h)return null;
      return {n:(h.querySelector(':scope>b')||{}).textContent||'',teks:h.parentElement.innerText,cip:(h.parentElement.querySelector('[data-sbq]')||{}).dataset?.sbq??null};});
    ok(es&&/PAPERTRADE/i.test(es.teks)&&/kertas, bukan wang sebenar/.test(es.teks),`${T} Esok: belian dilabel PAPERTRADE (kertas)`);
    if(SB&&es){const tb=(()=>{const d=new Date(SB.tarikh_isyarat+'T00:00:00Z');do{d.setUTCDate(d.getUTCDate()+1);}while(d.getUTCDay()===0||d.getUTCDay()===6);return d.toISOString().slice(0,10);})();
      /* fungsi halaman tidak global; tarikh "esok" dibaca daripada tajuk panel Esok (format tkO: "9 Nov") */
      const BLN=['Jan','Feb','Mac','Apr','Mei','Jun','Jul','Ogo','Sep','Okt','Nov','Dis'],lbl=`${+tb.slice(8,10)} ${BLN[+tb.slice(5,7)-1]}`;
      const h2=await p.evaluate(()=>{const h=[...document.querySelectorAll('#v-utama .panel-h h2')].find(x=>/^Esok/.test(x.textContent));return h?h.textContent:'';});
      if(h2.includes('buka '+lbl))ok(es.n===nf(sbN),`${T} Esok "Dibeli pada buka" ${es.n} = senarai beli ${nf(sbN)}`);
      else ok((es.n==='0'&&/belum dijana/.test(es.teks))||(es.n===nf(sbN)&&es.teks.includes(lbl)),`${T} Esok: senarai beli bukan untuk esok dilabel dengan tarikhnya`);
      if(es.cip){await p.evaluate(s=>document.querySelector(`#v-utama [data-sbq="${s}"]`).click(),es.cip);await p.waitForTimeout(500);
        const sb=await p.evaluate(()=>{const q=document.querySelector('#sbQ');return q?{v:q.value,nampak:!!q.offsetParent}:null;});
        ok(sb&&sb.v===es.cip&&sb.nampak,`${T} ketik cip ${es.cip} membuka Senarai beli ditapis`);}}

    /* 5 label purata setiap posisi kertas */
    if(await pn('__g')){const t=await p.evaluate(()=>document.querySelector('#v-utama').innerText);
      ok(/purata setiap posisi kertas \(bukan akaun\)/i.test(t)&&!/Untung purata semua posisi lawan SPUS/.test(t),`${T} Hari ini: purata dilabel setiap posisi kertas (bukan akaun)`);}

    /* 3 kad skor + 4 lift */
    await pergi('analisis');
    if(await pn('kad skor')){
      const ks=await p.evaluate(()=>{const t=document.querySelector('table[data-st="kadskor"]');if(!t)return null;
        return {th:[...t.tHead.rows[0].cells].map(c=>c.textContent.replace(/[↕↓↑]/g,'').trim()),
          id:[...t.tBodies[0].rows].map(r=>r.dataset.kd).filter(Boolean)};});
      ok(!!ks,`${T} jadual kad skor ada`);
      if(ks&&KS){
        if(baruKS){['Buku harian % [95%]','MDD T4','Lift masuk 10 sesi'].forEach(h=>ok(ks.th.includes(h),`${T} kad skor: lajur "${h}"`));
          ok(ks.th.some(h=>/^T4 \/ SPUS pada MDD/.test(h)),`${T} kad skor: lajur T4 / SPUS pada MDD`);}
        else ok(ks.th.includes('Jangkaan')&&ks.th.includes('T4 kaedah'),`${T} kad skor dokumen lama: lajur lama`);
        /* susunan lalai: status, kemudian lift menurun (null terakhir) */
        const R={};KS.rows.forEach(v=>{const o={};KS.kol.forEach((k,i)=>{o[k]=v[i];});R[o.id]=o;});
        const ORD=['TERBUKTI','CALON','BELUM CUKUP','GAGAL','NEGATIF'];let susun=true,sebab='';
        for(let i=1;i<ks.id.length;i++){const a=R[ks.id[i-1]],c=R[ks.id[i]];if(!a||!c)continue;const sa=ORD.indexOf(a.status),sc=ORD.indexOf(c.status);
          if(sa>sc){susun=false;sebab=a.id+'>'+c.id+' status';break;}
          if(sa===sc&&!(a.lift==null&&c.lift==null)&&(a.lift==null||(c.lift!=null&&c.lift>a.lift))){susun=false;sebab=a.id+' lift '+a.lift+' sebelum '+c.id+' lift '+c.lift;break;}}
        ok(susun,`${T} kad skor disusun ikut status kemudian lift (null di bawah)${sebab?' — '+sebab:''}`);}
      const gl=await p.evaluate(()=>document.querySelector('#v-analisis').textContent);  /* textContent: termasuk bahagian yang disembunyi rel */
      if(baruKS)ok(!/≥ \d+ posisi ditutup \(SD|baldi hari pegang yang SAMA|> SPUS & p95/.test(gl),`${T} tiada penerangan gate lama dalam Pilih kaedah`);}
    if(await pn('lift')){
      const lf=await p.evaluate(()=>{const v=document.querySelector('#v-analisis');return v.innerText;});
      ok(!/Lift\/bulan/i.test(lf),`${T} panel Lift tanpa "Lift/bulan"`);
      if(LF&&String(LF.versi||'').startsWith('lift_masuk')){ok(/lift masuk 10 sesi \(bebas keluar\), lulus plasebo/i.test(lf),`${T} lift diterangkan sebagai lift masuk 10 sesi`);
        if(!LF.diuji)ok(/Belum ada kaedah cukup data langsung; ujian pertama ~5 minggu/.test(lf),`${T} keadaan kosong lift jelas`);}}

    /* 5 Akaun */
    await pergi('prestasi');
    {const t=await p.evaluate(()=>document.querySelector('section.view:not([hidden])').innerText);
      ok(/purata setiap posisi kertas \(bukan pulangan akaun\)/i.test(t),`${T} Akaun: peratus dilabel purata setiap posisi kertas`);}

    /* 6 Kombinasi N */
    await pergi('rujukan');
    if(await p.evaluate(()=>{const b=document.querySelector('#kumpSeg button[data-k="kaedahn"]');if(!b)return false;b.click();return true;})){
      await p.waitForTimeout(800);await pn('produksi');
      const th=await p.evaluate(()=>{const t=document.querySelector('table[data-st="knprod"]');return t?[...t.tHead.rows[0].cells].map(c=>c.textContent.replace(/[↕↓↑]/g,'').trim()):null;});
      ok(th&&th.includes('Kad skor'),`${T} Produksi Kombinasi N: lajur Kad skor`);}

    ok(!ralat.length,`${T} sifar ralat konsol${ralat.length?': '+ralat.slice(0,3).join(' | '):''}`);
    await ctx.close();
  }
  await b.close();
  console.log(`RINGKASAN: ${gagal} kegagalan`);process.exit(gagal?1:0);
})();
