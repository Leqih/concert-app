from playwright.sync_api import sync_playwright
import os
D=os.path.dirname(os.path.abspath(__file__)); out=os.path.join(D,'..','dist','plusone-demo.html'); SH=os.path.join(D,'shots-m8'); os.makedirs(SH,exist_ok=True)
C="document.querySelector('[data-act=%s]').click()"
Q=lambda sel:"document.querySelector('%s').click()"%sel
S=[
('explore',"go('explore')"),
('explore-scroll',"go('explore');setTimeout(()=>document.querySelector('.scroll').scrollTop=700,300)"),
('show-crews',"go('show',A('Harry Styles').id);setTimeout(()=>document.querySelector('.scroll').scrollTop=520,300)"),
('nc-sheet',"go('show',A('Harry Styles').id);setTimeout(()=>{%s},300)"%(C%'ncopen')),
('nc-private',"go('show',A('Harry Styles').id);setTimeout(()=>{%s;setTimeout(()=>{%s;%s},200)},300)"%(C%'ncopen',Q('[data-k=vis][data-v=\"0\"]'),Q('[data-k=cap][data-v=\"4\"]'))),
('nc-women',"go('show',A('Harry Styles').id);setTimeout(()=>{%s;setTimeout(()=>{%s},200)},300)"%(C%'ncopen',Q('[data-k=j][data-v=\"7\"]'))),
('nc-created',"go('show',A('Harry Styles').id);setTimeout(()=>{%s;setTimeout(()=>{%s;setTimeout(()=>{%s},200)},200)},300)"%(C%'ncopen',Q('[data-k=vis][data-v=\"0\"]'),C%'nccreate')),
('nc-in-explore',"go('show',A('Doja Cat').id);setTimeout(()=>{%s;setTimeout(()=>{%s;setTimeout(()=>{go('explore')},3000)},200)},300)"%(C%'ncopen',C%'nccreate')),
('crew-t1-deposit',"go('crew','t1')"),
('crew-t2-light',"go('crew','t2')"),
('crew-t2-checkin',"go('crew','t2');setTimeout(()=>{%s;setTimeout(()=>{%s},300)},300)"%(C%'checkin',C%'pollopen')),
('plus-menu',"document.querySelector('[data-act=plusmenu]')&&document.querySelector('[data-act=plusmenu]').click()"),
]
with sync_playwright() as p:
    b=p.chromium.launch()
    for i,(n,js) in enumerate(S):
        pg=b.new_page(viewport={'width':393,'height':852}); pg.route('**/fonts.googleapis.com/**',lambda r:r.abort())
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('file://'+os.path.abspath(out)); pg.wait_for_timeout(700)
        pg.evaluate(js); pg.wait_for_timeout(3800 if 'created' in n or 'explore' in n and 'nc' in n else 1500)
        pg.screenshot(path=f"{SH}/{i:02d}-{n}.png")
        if errs: print(n,errs)
        pg.close()
    b.close()
from PIL import Image; import glob
fs=sorted(glob.glob(SH+'/*.png'))
for k in range(0,len(fs),6):
    sh=Image.new('RGB',(393*6,852),'white')
    for j,f in enumerate(fs[k:k+6]): sh.paste(Image.open(f),(j*393,0))
    sh.save(f'{SH}/sheet{k//6}.jpg',quality=80)
print('done',len(fs))
