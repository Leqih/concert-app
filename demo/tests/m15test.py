from playwright.sync_api import sync_playwright
import os
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__)); out=os.path.abspath(os.path.join(D,'..','dist','plusone-demo.html')); SH=os.path.join(D,'shots-m15'); os.makedirs(SH,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); fs=[]; errs=[]
    def page():
        pg=b.new_page(viewport={'width':393,'height':852}); pg.route('**/*ticketm.net/**',lambda r:r.abort()); pg.on('pageerror',lambda e:errs.append(str(e))); pg.goto('file://'+out); pg.wait_for_timeout(700); return pg
    def shot(pg,n): f=f'{SH}/{len(fs):02d}-{n}.png'; pg.screenshot(path=f); fs.append(f)
    pg=page(); pg.evaluate("go('tickets')"); pg.wait_for_timeout(400); pg.click('[data-act=itopen]'); pg.wait_for_timeout(400); shot(pg,'it-choose')
    pg.click('[data-act=itstep][data-v=email]'); pg.wait_for_timeout(1500); pg.click('[data-act=itpick][data-v="1"]'); pg.wait_for_timeout(300); shot(pg,'it-email')
    pg.click('[data-act=itadd]'); pg.wait_for_timeout(800); shot(pg,'it-added'); print('tix',pg.evaluate("MYTIX().length"))
    pg.click('[data-act=itopen]'); pg.wait_for_timeout(300); pg.click('[data-act=itstep][data-v=scan]'); pg.wait_for_timeout(1500); shot(pg,'it-scan'); pg.close()
    pg=page(); pg.evaluate("go('me')"); pg.wait_for_timeout(400); pg.click('[data-act=epopen]'); pg.wait_for_timeout(400); pg.fill('#epbio','Front row regular. Will sing every word.'); pg.click('[data-act=eptag][data-v=rock]'); pg.click('[data-act=epspot][data-v="Front row"]'); pg.wait_for_timeout(300); shot(pg,'ep-sheet')
    pg.click('[data-act=epsave]'); pg.wait_for_timeout(500); pg.evaluate("document.querySelector('.scroll').scrollTop=420"); pg.wait_for_timeout(300); shot(pg,'ep-saved'); pg.close()
    pg=page(); pg.evaluate("go('crew','t2')"); pg.wait_for_timeout(400); pg.click('[data-act=attach]'); pg.wait_for_timeout(300); shot(pg,'att-menu'); pg.click('[data-act=attsend][data-v=photo]'); pg.wait_for_timeout(300); pg.click('[data-act=attach]'); pg.click('[data-act=attsend][data-v=ticket]'); pg.wait_for_timeout(400); shot(pg,'att-sent')
    pg.click('[data-act=safety]'); pg.wait_for_timeout(400); pg.click('[data-act=secopen]'); pg.wait_for_timeout(400); shot(pg,'sec'); pg.click('[data-act=secsend]'); pg.wait_for_timeout(400); shot(pg,'sec-sent'); pg.close()
    pg=page(); pg.evaluate("go('show',A('Gorillaz').id)"); pg.wait_for_timeout(500); pg.evaluate("document.querySelector('[data-act=wrep]').click()"); pg.wait_for_timeout(300); pg.fill('.wtf input','See you at the bar!'); pg.press('.wtf input','Enter'); pg.wait_for_timeout(400); pg.evaluate("document.querySelector('.wth').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300); shot(pg,'wall-reply'); pg.close()
    print(errs)
    for k in range(0,len(fs),6):
        im=Image.new('RGB',(393*len(fs[k:k+6]),852)); [im.paste(Image.open(f),(i*393,0)) for i,f in enumerate(fs[k:k+6])]; im.save(f'{SH}/sheet{k//6}.jpg',quality=78)
