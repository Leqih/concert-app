"""Walk a user journey by clicking real controls; screenshot + list of visible controls after each step.
usage: journey.py NAME 'setup js' 'act[:text]' 'act[:text]' ...   (step 'js:<code>' runs code, 'wait:ms', 'type:<sel>|<text>')"""
from playwright.sync_api import sync_playwright
import os, sys
D = os.path.dirname(os.path.abspath(__file__)); html = os.path.abspath(os.path.join(D, '..', 'dist', 'plusone-demo.html'))
OUT = os.environ.get('JOUT', '/tmp/journeys'); os.makedirs(OUT, exist_ok=True)
name, setup, steps = sys.argv[1], sys.argv[2], sys.argv[3:]
VIS = """() => [...document.querySelectorAll('[data-act]')].filter(e=>{const r=e.getBoundingClientRect(); return e.offsetParent&&r.width>0&&r.bottom>0&&r.top<852&&!e.disabled})
 .map(e=>e.dataset.act+':'+(e.getAttribute('aria-label')||e.innerText||'').trim().replace(/\\s+/g,' ').slice(0,34))"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 393, 'height': 852}, device_scale_factor=1)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    pg.route('**/*ticketm.net/**', lambda r: r.abort()); pg.route('**/fonts.g*/**', lambda r: r.abort())
    pg.goto('file://' + html); pg.wait_for_timeout(600)
    if setup != '0': pg.evaluate(setup)
    pg.wait_for_timeout(1200)
    def shot(i, label):
        pg.screenshot(path=f'{OUT}/{name}_{i:02d}.png')
        t = pg.evaluate("()=>{const t=document.getElementById('toast');return t&&!t.hidden?t.textContent:''}")
        print(f'--- step {i} [{label}] screen={pg.evaluate("state.screen")} toast={t!r} errs={errs[-1:] }')
        print('   ', ' | '.join(pg.evaluate(VIS))[:1500])
    shot(0, 'start')
    for i, st in enumerate(steps, 1):
        if st.startswith('js:'): pg.evaluate(st[3:])
        elif st.startswith('wait:'): pg.wait_for_timeout(int(st[5:]))
        elif st.startswith('type:'):
            sel, txt = st[5:].split('|', 1); pg.fill(sel, txt)
        else:
            act, _, txt = st.partition(':')
            ok = pg.evaluate("""([a,t])=>{ const els=[...document.querySelectorAll('[data-act="'+a+'"]')].filter(e=>e.offsetParent&&!e.disabled);
              const el = t ? els.find(e=>((e.getAttribute('aria-label')||'')+' '+e.innerText).toLowerCase().includes(t.toLowerCase())) : els[0]; if(!el) return false; el.scrollIntoView({block:'center'}); el.click(); return true; }""", [act, txt])
            if not ok: print(f'!!! step {i}: no control {st}')
        pg.wait_for_timeout(1400)
        shot(i, st)
    b.close()
