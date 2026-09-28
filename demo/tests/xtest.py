from playwright.sync_api import sync_playwright
out=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','dist','plusone-demo.html')
S=[('x-crew',"go('explore')"),('x-crew-scroll',"go('explore');setTimeout(()=>document.querySelector('.scroll').scrollTop=520,300)"),('x-women',"state.xtag=7;go('explore')"),('x-ticket',"state.xmode='ticket';go('explore')"),('x-join',"go('explore');setTimeout(()=>document.querySelectorAll('.xjn')[1].click(),300)")]
with sync_playwright() as p:
    b=p.chromium.launch()
    for i,(n,js) in enumerate(S):
        pg=b.new_page(viewport={'width':393,'height':852}); pg.route('**/fonts.googleapis.com/**',lambda r:r.abort())
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('file://'+out); pg.wait_for_timeout(600); pg.evaluate(js); pg.wait_for_timeout(1200)
        pg.screenshot(path=f'/tmp/m7/x{i}.png'); 
        if errs: print(n,errs)
        pg.close()
    b.close()
from PIL import Image
sh=Image.new('RGB',(393*5,852),'white')
for i in range(5): sh.paste(Image.open(f'/tmp/m7/x{i}.png'),(i*393,0))
sh.save('/tmp/m7/xs.jpg',quality=85); print('ok')
