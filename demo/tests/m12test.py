from playwright.sync_api import sync_playwright
import os
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__)); out=os.path.abspath(os.path.join(D,'..','dist','plusone-demo.html')); SH=os.path.join(D,'shots-m12'); os.makedirs(SH,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':393,'height':852}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+out); pg.wait_for_timeout(800); fs=[]
    def shot(n): f=f'{SH}/{len(fs):02d}-{n}.png'; pg.screenshot(path=f); fs.append(f)
    pg.evaluate("document.getElementById('sc').scrollTop=99999"); pg.wait_for_timeout(1500)
    pg.evaluate("document.getElementById('sc').scrollTop-=300"); pg.wait_for_timeout(300); shot('months')
    pg.evaluate("document.querySelector('.urow[data-m=\"10\"]').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300)
    pg.evaluate("document.querySelector('.urow[data-m=\"10\"]').click()"); pg.wait_for_timeout(180); shot('fly-mid'); pg.wait_for_timeout(700); shot('show')
    pg.evaluate("document.querySelector('[data-act=back]').click()"); pg.wait_for_timeout(200); shot('back-mid'); pg.wait_for_timeout(700); shot('back-done')
    pg.evaluate("document.getElementById('sc').scrollTop=0"); pg.wait_for_timeout(300)
    pg.mouse.move(200,400)
    for _ in range(6): pg.mouse.wheel(0,-60); pg.wait_for_timeout(20)
    pg.wait_for_timeout(60); shot('pull'); pg.wait_for_timeout(500); shot('spin'); pg.wait_for_timeout(900); shot('updated')
    print(errs)
    im=Image.new('RGB',(393*len(fs),852)); [im.paste(Image.open(f),(i*393,0)) for i,f in enumerate(fs)]; im.save(SH+'/sheet.jpg',quality=80)
