"""Capture every screen / sheet of the current demo at 393x852 @2x -> docs/screens-v96/*.jpg (for Figma sync)."""
from playwright.sync_api import sync_playwright
from PIL import Image
import os, io
D=os.path.dirname(os.path.abspath(__file__)); out=os.path.abspath(os.path.join(D,'..','dist','plusone-demo.html')); OUT=os.path.abspath(os.path.join(D,'..','..','docs','screens-v96')); os.makedirs(OUT,exist_ok=True)
C="document.querySelector('%s').click()"
S=[('01-home',"0",0),('02-home-upcoming',"0","document.querySelector('.ufl').scrollIntoView({block:'start'});document.getElementById('sc').scrollBy(0,-140)"),
('03-home-filters',"0","document.querySelector('[data-act=ufopen]').click()"),
('04-plus-menu',"document.querySelector('#navroot [data-act=plusmenu]').click()",0),
('05-explore',"go('explore')",0),('06-search',"go('search')",0),('07-search-results',"go('search');state.sq='pit';render()",0),
('08-clips',"go('clips')",0),('09-clips-comments',"go('clips');setTimeout(()=>document.querySelector('.clp [data-act=clcom]').click(),300)",0),
('10-clips-share',"go('clips');setTimeout(()=>document.querySelector('[data-act=clshare]').click(),300)",0),
('11-chats',"go('crews')",0),('12-crew-chat',"go('crew','t1')",0),('13-crew-safety',"go('crew','t3');setTimeout(()=>document.querySelector('[data-act=safety]').click(),300)",0),
('14-tickets',"go('tickets')",0),('15-tickets-spares',"go('tickets');setTimeout(()=>document.querySelector('[data-act=tview][data-v=spares]').click(),200)",0),
('16-show',"go('show',A('Gorillaz').id)",0),('17-show-crews-wall',"go('show',A('Gorillaz').id)","document.querySelector('.scroll').scrollTop=560"),
('18-start-crew',"go('show',A('Gorillaz').id);setTimeout(()=>document.querySelector('[data-act=ncopen]').click(),300)",0),
('19-scene',"go('scene','1')",0),('20-me',"go('me')",0),('21-person',"state.pid=1;go('person')",0),
('22-sell',"document.querySelector('#navroot [data-act=plusmenu]').click();setTimeout(()=>document.querySelector('#psheet [data-act=sellstart]').click(),1800)",0),
('23-city',"document.querySelector('[data-act=citysheet]').click()",0)]
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]
    for n,js,after in S:
        pg=b.new_page(viewport={'width':393,'height':852},device_scale_factor=2); pg.route('**/*ticketm.net/**',lambda r:r.abort()); pg.on('pageerror',lambda e:errs.append((n,str(e))))
        pg.goto('file://'+out); pg.wait_for_timeout(800); pg.evaluate(js); pg.wait_for_timeout(2600)
        if after: pg.evaluate(after); pg.wait_for_timeout(900)
        Image.open(io.BytesIO(pg.screenshot())).convert('RGB').save(f'{OUT}/{n}.jpg',quality=86); pg.close()
    print('errors',errs, len(S))
