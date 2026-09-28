from playwright.sync_api import sync_playwright
import os
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__)); out=os.path.abspath(os.path.join(D,'..','dist','plusone-demo.html')); SH=os.path.join(D,'shots-m11'); os.makedirs(SH,exist_ok=True)
S=[('explore',"go('explore')",None),('explore-scroll',"go('explore');setTimeout(()=>document.querySelector('.scroll').scrollTop=900,300)",None),
   ('search',"go('explore');setTimeout(()=>document.querySelector('[data-act=search]').click(),200)",None),
   ('search-type',"go('explore');setTimeout(()=>document.querySelector('[data-act=search]').click(),200)","pit"),
   ('search-people',"go('explore');setTimeout(()=>document.querySelector('[data-act=search]').click(),200)","ma"),
   ('vibe',"go('explore');setTimeout(()=>{document.querySelector('[data-act=search]').click();setTimeout(()=>document.querySelector('[data-act=svibe][data-v=\"2\"]').click(),300)},200)",None)]
with sync_playwright() as p:
    b=p.chromium.launch(); fs=[]
    for i,(n,js,typ) in enumerate(S):
        pg=b.new_page(viewport={'width':393,'height':852}); pg.route('**/fonts.googleapis.com/**',lambda r:r.abort()); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('file://'+out); pg.wait_for_timeout(600); pg.evaluate(js); pg.wait_for_timeout(900)
        if typ: pg.keyboard.type(typ,delay=80); pg.wait_for_timeout(500)
        f=f"{SH}/{i:02d}-{n}.png"; pg.screenshot(path=f); fs.append(f)
        if errs: print(n,errs)
        pg.close()
    im=Image.new('RGB',(393*len(fs),852)); [im.paste(Image.open(f),(i*393,0)) for i,f in enumerate(fs)]; im.save(SH+'/sheet.jpg',quality=80)
print('ok')
