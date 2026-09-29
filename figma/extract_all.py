"""Run figma/extract.js on every demo screen -> figma/data/<screen>.json + figma/data/images.json
Screens and navigation steps are shared with demo/tests/capture_all.py."""
from playwright.sync_api import sync_playwright
import os, json, sys, importlib.util
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(D)
spec = importlib.util.spec_from_file_location('cap', os.path.join(ROOT, 'demo/tests/capture_all.py'))
src = open(os.path.join(ROOT, 'demo/tests/capture_all.py')).read()
S = eval(src[src.index('S=[') + 2: src.index(']\nwith') + 1])  # reuse the screen list
OUT = os.path.join(D, 'data'); os.makedirs(OUT, exist_ok=True)
EX = open(os.path.join(D, 'extract.js')).read()
html = os.path.join(ROOT, 'demo/dist/plusone-demo.html')
only = sys.argv[1:]
imgs = {}
if os.path.exists(f'{OUT}/images.json'): imgs = json.load(open(f'{OUT}/images.json'))
with sync_playwright() as p:
    b = p.chromium.launch()
    for n, js, after in S:
        if only and n not in only: continue
        pg = b.new_page(viewport={'width': 393, 'height': 852})
        pg.route('**/*ticketm.net/**', lambda r: r.abort())
        pg.route('**/fonts.g*/**', lambda r: r.abort())
        pg.emulate_media(reduced_motion='reduce')
        pg.goto('file://' + html); pg.wait_for_timeout(800); pg.evaluate(js); pg.wait_for_timeout(2600)
        if after: pg.evaluate(after); pg.wait_for_timeout(900)
        # freeze animations at their end state
        pg.add_style_tag(content='*,*::before,*::after{animation-play-state:paused!important;transition:none!important}')
        pg.wait_for_timeout(100)
        r = pg.evaluate(EX)
        # remap image keys globally by src
        rev = {v: k for k, v in imgs.items()}
        remap = {}
        for k, v in r['imgs'].items():
            if v not in rev:
                nk = 'm%d' % len(imgs); imgs[nk] = v; rev[v] = nk
            remap[k] = rev[v]
        def fix(nd):
            if nd.get('img'): nd['img'][0] = remap[nd['img'][0]]
            for c in nd.get('c', []): fix(c)
        fix(r['tree'])
        json.dump(r['tree'], open(f'{OUT}/{n}.json', 'w'), separators=(',', ':'))
        pg.close()
        print(n, os.path.getsize(f'{OUT}/{n}.json'))
    b.close()
json.dump(imgs, open(f'{OUT}/images.json', 'w'))
print('images', len(imgs))
