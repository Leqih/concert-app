from playwright.sync_api import sync_playwright
import os
D=os.path.dirname(os.path.abspath(__file__)); out=os.path.abspath(os.path.join(D,'..','dist','plusone-demo.html')); SH=os.path.join(D,'shots-m9'); os.makedirs(SH,exist_ok=True)
Q=lambda sel:"document.querySelector('%s').click()"%sel
S=[
('explore-trending',"go('explore');setTimeout(()=>document.querySelector('.scroll').scrollTop=90,300)",1200),
('home-buddies',"setTimeout(()=>{document.getElementById('sc').scrollTop=560},300)",1200),
('bjoin',"setTimeout(()=>{%s},300)"%Q('[data-act=bjoin]'),1500),
('wall-readonly',"go('show',A('Harry Styles').id);setTimeout(()=>document.getElementById('wall').scrollIntoView(),300)",1200),
('wall-holder',"go('show',A('Gorillaz').id);setTimeout(()=>document.getElementById('wall').scrollIntoView(),300)",1200),
('wall-post',"go('show',A('Gorillaz').id);setTimeout(()=>{document.getElementById('wq').value='Meeting at the Section 105 bar at 7:30, come say hi';document.querySelector('.wcomp2 button').click();setTimeout(()=>%s,300)},300)"%Q('[data-act=wlike]'),1500),
('wall-mc',"go('show',A('Gorillaz').id);setTimeout(()=>{%s},300)"%Q('[data-act=wtag][data-v=\"Missed connections\"]'),1200),
('trend-to-wall',"go('explore');setTimeout(()=>{%s},300)"%Q('[data-act=wallgo]'),1500),
('scene-start',"go('scene','1');setTimeout(()=>{%s},400)"%Q('.wbar [data-act=ncopen]'),1500),
('plus-looking',"%s;setTimeout(()=>{%s;setTimeout(()=>{%s},500)},600)"%(Q('[data-act=plusmenu]'),Q('[data-act=lookon]'),Q('[data-act=plusmenu]')),1800),
]
with sync_playwright() as p:
    b=p.chromium.launch()
    for i,(n,js,w) in enumerate(S):
        pg=b.new_page(viewport={'width':393,'height':852}); pg.route('**/fonts.googleapis.com/**',lambda r:r.abort())
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('file://'+out); pg.wait_for_timeout(700); pg.evaluate(js); pg.wait_for_timeout(w)
        pg.screenshot(path=f"{SH}/{i:02d}-{n}.png")
        if errs: print(n,errs)
        pg.close()
    b.close()
from PIL import Image; import glob
fs=sorted(glob.glob(SH+'/*.png'))
for k in range(0,len(fs),5):
    sh=Image.new('RGB',(393*5,852),'white')
    for j,f in enumerate(fs[k:k+5]): sh.paste(Image.open(f),(j*393,0))
    sh.save(f'{SH}/sheet{k//5}.jpg',quality=80)
print('done',len(fs))
