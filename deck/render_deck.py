import json, os, sys, asyncio
from playwright.async_api import async_playwright

ROOT = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
OUT = __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'shots')
os.makedirs(OUT, exist_ok=True)
order = json.load(open(f'{ROOT}/deck.json'))['order']
only = sys.argv[1:] or order

HEAD = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Noto Sans SC';src:local('Noto Sans CJK SC');font-weight:400}
@font-face{font-family:'Noto Sans SC';src:local('Noto Sans CJK SC Medium'),local('Noto Sans CJK SC');font-weight:500}
@font-face{font-family:'Noto Sans SC';src:local('Noto Sans CJK SC Bold'),local('Noto Sans CJK SC');font-weight:700}
html,body{margin:0;padding:0}
*{margin:0;box-sizing:border-box}
section{position:relative;width:1920px;height:1080px;overflow:hidden}
section>aside{display:none}
h1,h2,h3{font-weight:600}
p,h1,h2,h3{line-height:1.4}
h2{line-height:1.15}
ul,ol{padding-left:1.2em}
table{border-collapse:collapse;width:100%}
th,td{border-bottom:1px solid #D6D6D2;padding:0.35em 0.6em;text-align:left;vertical-align:top}
th{font-weight:700}
x-connector{display:block;height:2px;background:#121213;align-self:center}
</style></head><body>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1920,'height':1080}, device_scale_factor=0.5)
        await pg.route('**/fonts.googleapis.com/**', lambda r: r.abort())
        for sid in only:
            html = open(f'{ROOT}/slides/{sid}.html').read()
            await pg.set_content(HEAD + html + '</body></html>')
            await pg.wait_for_timeout(150)
            await pg.screenshot(path=f'{OUT}/{order.index(sid):02d}-{sid}.png')
        await b.close()
asyncio.run(main())
