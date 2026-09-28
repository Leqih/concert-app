from playwright.sync_api import sync_playwright
import os
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__)); out=os.path.abspath(os.path.join(D,'..','dist','plusone-demo.html')); SH=os.path.join(D,'shots-m13'); os.makedirs(SH,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':393,'height':852}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+out); pg.wait_for_timeout(1200); fs=[]
    def shot(n): f=f'{SH}/{len(fs):02d}-{n}.png'; pg.screenshot(path=f); fs.append(f)
    pg.evaluate("document.querySelector('.ufl').scrollIntoView({block:'start'});document.getElementById('sc').scrollBy(0,-120)"); pg.wait_for_timeout(400); shot('row')
    pg.click('[data-act=ufopen]'); pg.wait_for_timeout(500); shot('sheet')
    pg.click('[data-act=ufk][data-v=classical]'); pg.wait_for_timeout(200); pg.click('[data-act=ufk][data-v=festival]'); pg.wait_for_timeout(300); shot('picked')
    pg.click('[data-act=ufapply]'); pg.wait_for_timeout(900); shot('applied')
    print('rows',pg.evaluate("document.querySelectorAll('.urow').length"))
    pg.click('[data-act=ufopen]'); pg.wait_for_timeout(300); pg.click('[data-act=ufreset]'); pg.click('[data-act=ufg][data-v=Jazz]'); pg.click('[data-act=ufz][data-v=theatre]'); pg.wait_for_timeout(300); shot('jazz')
    pg.click('[data-act=ufapply]'); pg.wait_for_timeout(900); shot('jazz-applied'); print('rows',pg.evaluate("document.querySelectorAll('.urow').length"))
    pg.evaluate("document.querySelector('.urow').click()"); pg.wait_for_timeout(1000); shot('show-fallback')
    print(errs)
    im=Image.new('RGB',(393*len(fs),852)); [im.paste(Image.open(f),(i*393,0)) for i,f in enumerate(fs)]; im.save(SH+'/sheet.jpg',quality=78)
