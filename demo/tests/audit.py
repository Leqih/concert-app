from playwright.sync_api import sync_playwright
import json, os, collections
out=os.path.abspath('dist/plusone-demo.html')
SCR=[('home',"0"),('explore',"go('explore')"),('search',"go('search')"),('crews',"go('crews')"),('tickets',"go('tickets')"),('spares',"go('tickets');setTimeout(()=>document.querySelector('[data-act=tview][data-v=spares]').click(),100)"),('me',"go('me')"),('person',"state.pid=1;go('person')"),('show',"go('show',A('Gorillaz').id)"),('scene',"go('scene','1')"),('crew',"go('crew','t1')"),('sell',"document.querySelector('[data-act=plusmenu]').click();setTimeout(()=>document.querySelector('[data-act=sellstart]').click(),600)")]
JS=r'''(()=>{ const R=[]; const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.top<900&&r.bottom>0};
 document.querySelectorAll('#view h1,#view h2,#view h3,#view .sub,#view .wcity,#view .slab,#view .ncl,#view .note').forEach(e=>{ if(!vis(e))return; const c=getComputedStyle(e), r=e.getBoundingClientRect();
   R.push({tag:e.tagName.toLowerCase(),cls:e.className,txt:e.textContent.trim().slice(0,28),fs:c.fontSize,fw:c.fontWeight,ff:c.fontFamily.split(',')[0],ls:c.letterSpacing,ta:c.textAlign,tt:c.textTransform,col:c.color,top:Math.round(r.top),cx:Math.round(r.left+r.width/2)}); });
 const rad={}; document.querySelectorAll('#view *').forEach(e=>{ if(!vis(e))return; const c=getComputedStyle(e); const br=c.borderTopLeftRadius; if(br&&br!=='0px'){ const r=e.getBoundingClientRect(); if(r.width>=60&&r.height>=40&&!br.includes('%')&&parseFloat(br)<r.height/2-1){ const k=br; (rad[k]=rad[k]||[]).push((e.className||e.tagName)+'').toString(); } } });
 return {text:R,rad:Object.fromEntries(Object.entries(rad).map(([k,v])=>[k,[...new Set(v)].slice(0,8)]))}; })()'''
res={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for n,js in SCR:
        pg=b.new_page(viewport={'width':393,'height':852}); pg.route('**/*ticketm.net/**',lambda r:r.abort()); pg.route('**/fonts.g*/**',lambda r:r.abort()); pg.goto('file://'+out); pg.wait_for_timeout(700); pg.evaluate(js); pg.wait_for_timeout(900)
        res[n]=pg.evaluate(JS); pg.close()
json.dump(res,open('/tmp/claude-0/-home-claude-concert-app/632dad76-ea66-5370-b8fa-1e3adb71d7ae/scratchpad/audit.json','w'),indent=1)
for n,r in res.items():
    print('=====',n)
    for t in r['text']:
        if t['tag'] in('h1','h2','h3') or 'sub' in t['cls'] or 'wcity' in t['cls'] or 'slab' in t['cls']:
            print(f"  {t['tag']:3} {t['cls'][:18]:18} {t['fs']:>6} {t['fw']} {t['ff'][:10]:10} {t['ta']:6} top{t['top']:4} cx{t['cx']} | {t['txt']}")
    print('  radii:',{k:len(v) for k,v in r['rad'].items()})
