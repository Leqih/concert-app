"""Full design-rule audit: every screen + sheets, whole scroll height. See DESIGN.md.
Rules: radii in {30,20,18,14,12} or pill/circle (+ listed exceptions); grayscale only (+ --like heart, --live green dot);
Inter / Inter Tight; chips 34 high; sheet titles 24; no emoji on page or sheet titles.
Usage: python3 demo/tests/audit_full.py [out.json]   (PW_CHROMIUM=/path/to/chrome to pick a browser)"""
from playwright.sync_api import sync_playwright
import json, os, sys
out=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','dist','plusone-demo.html'))
C="document.querySelector('[data-act=%s]').click()"
L=lambda js:"setTimeout(()=>{%s},300)"%js
ST=[('home',"0"),('explore',"go('explore')"),('search',"go('search')"),('search-q',"go('search');state.sq='ma';render()"),('crews',"go('crews')"),
('tickets',"go('tickets')"),('spares',"go('tickets');"+L("document.querySelector('[data-act=tview][data-v=spares]').click()")),
('me',"go('me')"),('person',"state.pid=1;go('person')"),('show',"go('show',A('Gorillaz').id)"),('show-locked',"go('show',SHOWS.find(LOCKED).id)"),('scene',"go('scene','1')"),
('crew',"go('crew','t1')"),('dm',"openThread(dmFor(4))"),('sell',"%s;setTimeout(()=>{%s},600)"%(C%'plusmenu',C%'sellstart')),
('plus',C%'plusmenu'),('city',C%'citysheet'),('filters',C%'ufopen'),('newcrew',"go('crews');"+L(C%'ncopen')),
('kit',"go('crews');"+L(C%'kitopen')),('activity',"go('crews');"+L(C%'actopen')),('chatinfo',"go('crew','t1');"+L(C%'kinfo')),
('ticketsheet',"go('crew','t1');"+L(C%'claim')),('privacy',"go('me');"+L(C%'privopen')),
('comments',"go('clips');"+L("document.querySelector('.clp [data-act=clcom]').click()")),('onboarding',"go('me');"+L(C%'onbopen'))]
JS=r'''(()=>{ const bad=[], T=[]; const ok=[30,20,18,14,12];
 // documented exceptions (DESIGN.md §3): Home Scenes quad 32, chat bubble 22, city-map pins 6, scene fan photos 12
 const okx={quad:32,igb:22,cs:6};
 const gray=c=>{ const m=c.match(/rgba?\(([^)]+)\)/); if(!m) return true; const [r,g,b,a]=m[1].split(',').map(parseFloat); if(a===0) return true; return Math.max(r,g,b)-Math.min(r,g,b)<=12; };
 const like=c=>/254, 44, 85|52, 199, 89/.test(c); // --like heart, --live online dot
 const emo=/\p{Extended_Pictographic}/u;
 document.querySelectorAll('#view *, #app .toast').forEach(e=>{ const c=getComputedStyle(e), r=e.getBoundingClientRect(); if(r.width<2||r.height<2||c.display==='none'||c.visibility==='hidden') return;
   const id=(e.className&&e.className.baseVal===undefined?e.className:e.tagName)+'';
   const br=parseFloat(c.borderTopLeftRadius), brs=c.borderTopLeftRadius, rb=Math.round(br);
   if(br>0&&!brs.includes('%')&&r.width>=40&&r.height>=36&&!(br>=Math.min(r.width,r.height)/2-1)&&!ok.includes(rb)&&!Object.entries(okx).some(([k,v])=>id.split(' ').includes(k)&&v===rb)) bad.push(['radius',rb,id,Math.round(r.width)+'x'+Math.round(r.height)]);
   if(e.children.length===0&&e.textContent.trim()){ const f=c.fontFamily.split(',')[0].replace(/"/g,''); if(!['Inter','Inter Tight','Noto Sans SC'].includes(f)&&!/emo|eb/.test(id)) bad.push(['font',f,id]); if(!gray(c.color)&&!like(c.color)) bad.push(['color',c.color,id,e.textContent.trim().slice(0,20)]); }
   if(!gray(c.backgroundColor)&&!like(c.backgroundColor)) bad.push(['bg',c.backgroundColor,id]);
   if(c.backgroundImage.includes('gradient')&&/rgb/.test(c.backgroundImage)){ const cols=c.backgroundImage.match(/rgba?\([^)]+\)/g)||[]; if(cols.some(x=>!gray(x))) bad.push(['gradient',id]); }
   if(/(^| )gch( |$)/.test(id)&&Math.round(r.height)!==34) bad.push(['chip-height',Math.round(r.height),id,e.textContent.trim().slice(0,16)]);
   if(e.tagName==='H3'&&e.closest('.sheet')&&emo.test(e.textContent)) bad.push(['emoji-on-sheet-title',e.textContent.trim().slice(0,24)]);
   if(e.tagName==='H1'&&e.classList.contains('sh1')&&emo.test(e.textContent)) bad.push(['emoji-on-page-title',e.textContent.trim().slice(0,24)]);
   if(e.tagName==='H3'&&e.closest('.csheet')&&!e.closest('.cms')&&c.fontSize!=='24px') bad.push(['sheet-title-size',c.fontSize,e.textContent.trim().slice(0,24)]);
   if(/^H[123]$/.test(e.tagName)||/(^| )(sub|wcity|slab|ncl|umon)( |$)/.test(id)) T.push([e.tagName.toLowerCase(),id.slice(0,20),c.fontSize,c.fontWeight,c.textAlign,Math.round(r.top+document.querySelector('#view .scroll')?.scrollTop||0),e.textContent.trim().slice(0,24)]); });
 const u={}; bad.forEach(b=>{ const k=b.join('|'); u[k]=b; }); return {bad:Object.values(u),T}; })()'''
res={}
with sync_playwright() as p:
    exe=os.environ.get('PW_CHROMIUM'); b=p.chromium.launch(**({'executable_path':exe} if exe else {}))
    for n,js in ST:
        pg=b.new_page(viewport={'width':393,'height':852}); pg.route('**/*ticketm.net/**',lambda r:r.abort()); pg.route('**/fonts.g*/**',lambda r:r.abort())
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('file://'+out+'?noonb'); pg.wait_for_timeout(700)
        try: pg.evaluate(js)
        except Exception as e: errs.append(str(e)[:120])
        pg.wait_for_timeout(1300)
        pg.evaluate("document.querySelectorAll('#view .scroll').forEach(s=>{s.style.overflow='visible';s.style.position='relative';s.style.height='auto'})")
        r=pg.evaluate(JS); r['err']=errs; res[n]=r; pg.close()
json.dump(res,open(sys.argv[1] if len(sys.argv)>1 else '/tmp/audit_full.json','w'),indent=1)
nbad=0
for n,r in res.items():
    print('=====',n,'errors' if r['err'] else '', r['err'][:1])
    for bd in r['bad']: print('  ✗',bd); nbad+=1
    for t in r['T']:
        if t[0] in('h1','h2','h3'): print('   ',t)
print('\nTOTAL ✗',nbad)
