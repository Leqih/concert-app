from playwright.sync_api import sync_playwright
import os
out=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','dist','plusone-demo.html')
os.makedirs('/tmp/m7',exist_ok=True)
C="document.querySelector('[data-act=%s]').click()"
S=[
('crew-hold',"go('crew','t1')"),
('crew-held',"go('crew','t1');setTimeout(()=>{%s;setTimeout(()=>{%s},300)},300)"%(C%'hold',C%'vote')),
('crew-checkin',"go('crew','t1');setTimeout(()=>{%s;setTimeout(()=>{%s},300)},300)"%(C%'hold',C%'checkin')),
('safety-sheet',"go('crew','t3');setTimeout(()=>{%s;setTimeout(()=>{%s},300)},300)"%(C%'safety',C%'loc')),
('ride-home',"go('crew','t3');setTimeout(()=>{%s;setTimeout(()=>{%s;setTimeout(()=>{%s},600)},300)},300)"%(C%'safety',C%'homeplan',C%'homejoin')),
('profile-other',"state.pid=1;go('person')"),
('me-verify',"go('me')"),
('me-verified',"go('me');setTimeout(()=>{%s},300)"%(C%'idv')),
('show-harry',"go('show',A('Harry Styles').id);setTimeout(()=>document.querySelector('.scroll').scrollTop=420,200)"),
('show-locked',"go('show',SHOWS.find(LOCKED).id);setTimeout(()=>document.querySelector('.scroll').scrollTop=300,200)"),
('tickets-split',"go('tickets')"),
('kit-recrew',"go('crews');setTimeout(()=>{%s},300)"%(C%'kitopen')),
('recrew-done',"go('crews');setTimeout(()=>{%s;setTimeout(()=>{%s},300)},300)"%(C%'kitopen',C%'recrew')),
('claim-sheet',"go('crew','t1');setTimeout(()=>document.querySelector('[data-act=claim]').click(),300)"),
]
with sync_playwright() as p:
    b=p.chromium.launch()
    for i,(n,js) in enumerate(S):
        pg=b.new_page(viewport={'width':393,'height':852},device_scale_factor=1); pg.route('**/fonts.googleapis.com/**',lambda r:r.abort())
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('file://'+out); pg.wait_for_timeout(700)
        pg.evaluate(js); pg.wait_for_timeout(2600)
        pg.screenshot(path=f"/tmp/m7/{i:02d}-{n}.png")
        if errs: print(n,errs)
        pg.close()
    b.close()
from PIL import Image; import glob
fs=sorted(glob.glob('/tmp/m7/*.png'))
w,h=393,852
for k in range(0,len(fs),7):
    sh=Image.new('RGB',(w*7,h),'white')
    for j,f in enumerate(fs[k:k+7]): sh.paste(Image.open(f),(j*w,0))
    sh.save(f'/tmp/m7/sheet{k//7}.jpg',quality=85)
print('done',len(fs))
