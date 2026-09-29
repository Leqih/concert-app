"""Build the single-file demo: inject data into demo2_tpl.html -> dist/plusone-demo.html
Usage: python3 demo/build.py
"""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
p = lambda f: os.path.join(D, f)
s = open(p('demo2_tpl.html'), encoding='utf-8').read()
shows = open(p('shows.js'), encoding='utf-8').read().replace('const SHOWS=', 'const NYC_SHOWS=', 1)
import base64
# Concert clips (Pexels, see clips/CREDITS.md): name -> duration in seconds
CLIPS = [('rock',8.8),('confetti',8),('crowd',12.5),('bluegtr',10),('ovation',12),('fest',9),('music',11),('club',10)]
def b64(f, mime): return 'data:%s;base64,%s' % (mime, base64.b64encode(open(p('clips/'+f),'rb').read()).decode())
# 's' = 8 fps WebP frame sheet (8 cols x 8 rows, 216x384 frames) used where <video> can't play (sandboxed previews)
clipv = [{'v': b64(n+'.mp4','video/mp4'), 'p': b64(n+'.jpg','image/jpeg'), 'd': d,
          's': b64(n+'.sprite.webp','image/webp'), 'sn': 64, 'sf': 8, 'sc': 8, 'sw': 216, 'sh': 384} for n, d in CLIPS]
av = json.load(open(p('avatars.json'))); ci = json.load(open(p('cities.json'))); mp = json.load(open(p('mapdots.json')))
out = (s.replace('/*SHOWS*/', shows)
        .replace('/*AVATARS*/', json.dumps([x['img'] for x in av]))
        .replace('/*CITIES*/', json.dumps(ci))
        .replace('/*MAP*/', json.dumps(mp))
        .replace('/*CLIPV*/', json.dumps(clipv)))
os.makedirs(p('dist'), exist_ok=True)
open(p('dist/plusone-demo.html'), 'w', encoding='utf-8').write(out)
print('built', len(out), 'bytes ->', p('dist/plusone-demo.html'))
