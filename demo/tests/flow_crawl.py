"""Click every visible data-act control on each main screen and record what happens.
Outputs a table: start screen | act | label | result (navigate / sheet / toast / changed / NOTHING / ERROR)."""
from playwright.sync_api import sync_playwright
import os, json, sys
D = os.path.dirname(os.path.abspath(__file__)); html = os.path.abspath(os.path.join(D, '..', 'dist', 'plusone-demo.html'))
STARTS = [('home', "0"), ('explore', "go('explore')"), ('clips', "go('clips')"), ('crews', "go('crews')"), ('tickets', "go('tickets')"),
          ('show', "go('show',A('Gorillaz').id)"), ('crew', "go('crew','t1')"), ('me', "go('me')"), ('person', "state.pid=1;go('person')"),
          ('scene', "go('scene','1')"), ('search', "go('search')"), ('wall', "go('wall',A('Gorillaz').id)"),
          ('plus', "document.querySelector('#navroot [data-act=plusmenu]').click()")]
SNAP = """() => { const t=document.getElementById('toast'); return {screen: state.screen, id: String(state.id),
  sheets: [...document.querySelectorAll('.sheet,[role=dialog]')].filter(e=>e.offsetParent).map(e=>e.id||e.className).join('|'),
  toast: (t && !t.hidden) ? t.textContent : '', html: document.getElementById('view').innerHTML.length + ':' + document.getElementById('view').innerText.length } }"""
LIST = """() => [...document.querySelectorAll('[data-act]')].filter(e => { const r=e.getBoundingClientRect(); return e.offsetParent && r.width>0 && r.bottom>0 && r.top<852 && r.right>0 && r.left<393; })
  .map((e,i)=>({i, act:e.dataset.act, label:(e.getAttribute('aria-label')||e.innerText||e.title||'').trim().replace(/\\s+/g,' ').slice(0,40)}))"""
rows = []
ONLY = sys.argv[1:]
with sync_playwright() as p:
    b = p.chromium.launch()
    def fresh(js):
        pg = b.new_page(viewport={'width': 393, 'height': 852}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.route('**/*ticketm.net/**', lambda r: r.abort()); pg.route('**/fonts.g*/**', lambda r: r.abort())
        pg.goto('file://' + html); pg.wait_for_timeout(500); pg.evaluate(js); pg.wait_for_timeout(900)
        return pg, errs
    for name, js in STARTS:
        if ONLY and name not in ONLY: continue
        pg, errs = fresh(js); items = pg.evaluate(LIST); pg.close()
        seen = set()
        for it in items:
            key = (it['act'], it['label'])
            if key in seen: continue
            seen.add(key)
            pg, errs = fresh(js)
            before = pg.evaluate(SNAP)
            els = pg.evaluate(LIST)
            idx = next((e['i'] for e in els if e['act'] == it['act'] and e['label'] == it['label']), None)
            if idx is None: pg.close(); continue
            try:
                pg.evaluate(f"""() => {{ const el=[...document.querySelectorAll('[data-act]')].filter(e => {{ const r=e.getBoundingClientRect(); return e.offsetParent && r.width>0 && r.bottom>0 && r.top<852 && r.right>0 && r.left<393; }})[{idx}]; el.click(); }}""")
            except Exception as e:
                errs.append(str(e))
            pg.wait_for_timeout(700)
            after = pg.evaluate(SNAP)
            if errs: res = 'ERROR ' + errs[0][:80]
            elif after['screen'] != before['screen'] or after['id'] != before['id']: res = f"→ {after['screen']}"
            elif after['sheets'] != before['sheets']: res = f"sheet {after['sheets'][:40]}"
            elif after['toast'] and after['toast'] != before['toast']: res = f"toast: {after['toast'][:70]}"
            elif after['html'] != before['html']: res = 'changed'
            else: res = 'NOTHING'
            rows.append((name, it['act'], it['label'], res)); pg.close()
    b.close()
json.dump(rows, open(os.path.join(D, 'flow_crawl_%s.json' % ('_'.join(ONLY) or 'all')), 'w'), ensure_ascii=False, indent=0)
for r in rows:
    if r[3] == 'NOTHING' or r[3].startswith('ERROR') or r[3].startswith('toast'): print(' | '.join(r))
print(len(rows), 'controls clicked')
