"""Turn figma/data/*.json into ready-to-send use_figma call scripts in figma/calls/.
- marks repeated subtrees as components (cs)
- splits large screens into deferred chunks
- builds image-upload calls (base64 JPEG, downscaled)
"""
import json, os, glob, hashlib, base64, io, re
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); DATA = f'{D}/data'; CALLS = f'{D}/calls'
os.makedirs(CALLS, exist_ok=True)
PAGE = '1362:11953'; BUILDER = '1363:11954'
LIMIT = 42000
screens = sorted(os.path.basename(p)[:-5] for p in glob.glob(f'{DATA}/[0-9]*.json'))
trees = {s: json.load(open(f'{DATA}/{s}.json')) for s in screens}
imgs = json.load(open(f'{DATA}/images.json'))

NAMES = {'iosbar': 'Status bar', 'bcap': 'Tab bar', 'urow': 'Upcoming row', 'wpill': 'Pill button', 'quad': 'Scene tile',
         'avimg': 'Avatar', 'wicon': 'Icon button', 'bcir': 'Plus button', 'uthumb': 'Thumbnail'}

def size(n):
    return 1 + sum(size(c) for c in n.get('c', []))
def sig(n, ox, oy):
    k = n['k']
    if k == 'T': return 'T'
    g = f"{round(n['x']-ox)},{round(n['y']-oy)},{round(n['w'])},{round(n['h'])}"
    if k == 'S': return 'S' + g + hashlib.md5(n['svg'].encode()).hexdigest()[:6]
    st = json.dumps([n.get('r'), bool(n.get('st')), bool(n.get('img')), bool(n.get('gr')), n.get('clip'), n.get('rot'), n.get('sh') is not None])
    return 'F' + g + st + '[' + ','.join(sig(c, n['x'], n['y']) for c in n.get('c', [])) + ']'
def split_svgs(n):
    out = []
    for c in n.get('c', []):
        if c['k'] == 'S' and len(c['svg']) > 20000:
            svg = c['svg']; head = svg[:svg.index('>') + 1]
            paths = re.findall(r'<path [^>]*></path>|<path [^>]*/>', svg)
            pieces = []
            for p in paths:
                m = re.search(r' d="([^"]*)"', p)
                if len(p) < 18000: pieces.append(p); continue
                segs = re.findall(r'M[^M]*', m.group(1)); buf = ''
                for sg in segs:
                    if len(buf) + len(sg) > 18000: pieces.append(p.replace(m.group(1), buf)); buf = ''
                    buf += sg
                if buf: pieces.append(p.replace(m.group(1), buf))
            for p in pieces: out.append(dict(c, svg=head + p + '</svg>'))
        else:
            split_svgs(c); out.append(c)
    if 'c' in n: n['c'] = out
for t in trees.values(): split_svgs(t)
counts = {}; occ = []
def scan(n, screen):
    if n['k'] == 'F':
        s = sig(n, n['x'], n['y'])
        if size(n) >= 3 and not (n['w'] >= 390 and n['h'] >= 700):
            counts[s] = counts.get(s, 0) + 1
        for c in n.get('c', []): scan(c, screen)
for s, t in trees.items(): scan(t, s)
names = {}; used = {}
def mark(n):
    if n['k'] != 'F': return
    s = sig(n, n['x'], n['y'])
    if counts.get(s, 0) >= 2 and size(n) >= 3 and not (n['w'] >= 390 and n['h'] >= 700):
        if s not in names:
            base = NAMES.get(n['n'].lstrip('#').split('.')[-1], n['n'].lstrip('#').split('.')[-1])
            used[base] = used.get(base, 0) + 1
            names[s] = base if used[base] == 1 else f'{base} #{used[base]}'
        n['cs'] = names[s]
    for c in n.get('c', []): mark(c)
for t in trees.values(): mark(t)
print('components', len(names))

# ---- images ----
disp = {}
def walk_img(n):
    if n.get('img'):
        k = n['img'][0]; w, h = disp.get(k, (0, 0)); disp[k] = (max(w, n['w']), max(h, n['h']))
    for c in n.get('c', []): walk_img(c)
for t in trees.values(): walk_img(t)
b64s = {}
for k, (w, h) in disp.items():
    src = imgs[k]; m = re.match(r'data:image/[a-z]+;base64,(.*)', src)
    if not m: print('non-data image', k, src[:80]); continue
    im = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
    sc = min(1.0, max(w * 1.6 / im.width, h * 1.6 / im.height))
    if sc < 1: im = im.resize((max(1, round(im.width * sc)), max(1, round(im.height * sc))), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=70, optimize=True); b64s[k] = base64.b64encode(buf.getvalue()).decode()
print('images', len(b64s), sum(len(v) for v in b64s.values()))
batches = []; cur = {}
for k, v in sorted(b64s.items(), key=lambda kv: -len(kv[1])):
    if cur and sum(len(x) for x in cur.values()) + len(v) > 38000: batches.append(cur); cur = {}
    cur[k] = v
if cur: batches.append(cur)
for i, b in enumerate(batches):
    code = 'const D=' + json.dumps(b) + ';\nconst out={};for(const k in D){const img=figma.createImage(figma.base64Decode(D[k]));out[k]=img.hash;}\nreturn out;'
    open(f'{CALLS}/img_{i:02d}.js', 'w').write(code)
print('image calls', len(batches))

# ---- screen calls ----
LOAD = ("const P=await figma.getNodeByIdAsync('%s');await figma.setCurrentPageAsync(P);const T=await figma.getNodeByIdAsync('%s');"
        "const AF=Object.getPrototypeOf(async function(){}).constructor;const B=await new AF('figma',T.characters)(figma);\n") % (PAGE, BUILDER)
def keys_in(n, acc):
    if n.get('img'): acc.add(n['img'][0])
    for c in n.get('c', []): keys_in(c, acc)
    return acc
TITLES = {}
for i, s in enumerate(screens):
    t = trees[s]; X = i * (393 + 100)
    name = s[:2] + ' ' + s[3:].replace('-', ' ').title()
    # split: defer largest subtrees until root payload fits
    chunks = []; dn = [0]
    def js(o): return json.dumps(o, separators=(',', ':'))
    def defer_big(root):
        while len(js(root)) > LIMIT:
            # lowest frame whose json is over LIMIT (its children all fit); else root itself
            best = None
            def f(n):
                nonlocal best
                over = [c for c in n.get('c', []) if c['k'] == 'F' and c.get('c') and not c.get('cs') and len(js(c)) > LIMIT]
                if over:
                    for c in over: f(c)
                elif n is not root and best is None: best = (0, n)
            f(root)
            if not best:
                kids = [c for c in root.get('c', []) if c['k'] == 'F' and c.get('c') and not c.get('cs')]
                if not kids: break
                best = (0, max(kids, key=lambda c: len(js(c))))
            node = best[1]; dn[0] += 1; tag = f'⟨d{dn[0]}⟩'
            kids = node['c']; node['c'] = []; node['n'] = node['n'] + ' ' + tag
            # pack kids into chunk groups
            group = []
            for k in kids:
                if group and len(js(group)) + len(js(k)) > LIMIT: chunks.append((tag, node['x'], node['y'], group)); group = []
                group.append(k)
            if group: chunks.append((tag, node['x'], node['y'], group))
    defer_big(t)
    # chunks themselves could be too big: recursive handled by defer on each chunk group if needed
    calls = []
    ik = keys_in(t, set())
    code = LOAD + 'const H=JSON.parse(figma.root.getSharedPluginData("po","h")||"{}");\n' if False else LOAD
    code += 'const IMG=' + js({k: '@' + k for k in ik}) + ';\n'
    code += 'const D=' + js(t) + ';\n'
    code += f"const r=await B.build(D,P,{-X},0,IMG,{{pageId:'{PAGE}'}});const root=await figma.getNodeByIdAsync(r.id);root.name={json.dumps(name)};\n"
    code += "const marks={};root.findAll(n=>/⟨d\\d+⟩/.test(n.name)).forEach(n=>marks[n.name.match(/⟨d\\d+⟩/)[0]]=n.id);return {id:r.id,count:r.count,marks};"
    calls.append(code)
    for tag, hx, hy, group in reversed(chunks):
        ik = set();
        for g in group: keys_in(g, ik)
        c = LOAD + 'const IMG=' + js({k: '@' + k for k in ik}) + ';\n' + 'const D=' + js(group) + ';\n'
        c += f"const host=await figma.getNodeByIdAsync('@@{tag}');let n=0;for(const d of D){{const r=await B.build(d,host,{hx},{hy},IMG,{{pageId:'{PAGE}'}});n+=r.count;}}"
        c += f"host.name=host.name.replace(' {tag}','');const marks={{}};host.findAll(n=>/⟨d\\d+⟩/.test(n.name)).forEach(n=>marks[n.name.match(/⟨d\\d+⟩/)[0]]=n.id);return {{count:n,marks}};"
        calls.append(c)
    for j, c in enumerate(calls):
        open(f'{CALLS}/{s}_{j}.js', 'w').write(c)
    print(s, [len(c) for c in calls])
json.dump(names, open(f'{DATA}/components.json', 'w'), indent=0)
