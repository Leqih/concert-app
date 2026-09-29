"""Build the single-file demo: inject data into demo2_tpl.html -> dist/plusone-demo.html
Usage: python3 demo/build.py
"""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
p = lambda f: os.path.join(D, f)
s = open(p('demo2_tpl.html'), encoding='utf-8').read()
shows = open(p('shows.js'), encoding='utf-8').read().replace('const SHOWS=', 'const NYC_SHOWS=', 1)
import base64
# Concert clips (Pexels, see clips/CREDITS.md). clips/index.json (from clips/make_index.py) carries duration
# plus the H.264 config and packet table used by the WebCodecs player where <video> is blocked.
def b64(f, mime): return 'data:%s;base64,%s' % (mime, base64.b64encode(open(p('clips/'+f),'rb').read()).decode())
import sys, shutil
WEB = '--web' in sys.argv   # web build: page + separate clip files (for the hosted artifact); default: one self-contained file
clipv = [{('src' if WEB else 'v'): ('clips/'+x['n']+'.mp4' if WEB else b64(x['n']+'.mp4','video/mp4')), 'p': ('clips/'+x['n']+'.jpg' if WEB else b64(x['n']+'.jpg','image/jpeg')), 'd': x['d'],
          'k': {'c': x['c'], 'dsc': x['dsc'], 'fps': x['fps'], 'pk': x['pk']}} for x in json.load(open(p('clips/index.json')))]
av = json.load(open(p('avatars.json'))); ci = json.load(open(p('cities.json'))); mp = json.load(open(p('mapdots.json')))
out = (s.replace('/*SHOWS*/', shows)
        .replace('/*AVATARS*/', json.dumps([x['img'] for x in av]))
        .replace('/*CITIES*/', json.dumps(ci))
        .replace('/*MAP*/', json.dumps(mp))
        .replace('/*CLIPV*/', json.dumps(clipv)))
if WEB:
    os.makedirs(p('dist-web/clips'), exist_ok=True)
    for x in json.load(open(p('clips/index.json'))):
        for ext in ('.mp4', '.jpg'): shutil.copy(p('clips/'+x['n']+ext), p('dist-web/clips/'+x['n']+ext))
    open(p('dist-web/index.html'), 'w', encoding='utf-8').write(out)
    print('built web', len(out), 'bytes ->', p('dist-web/index.html'), '+ clips/')
else:
    os.makedirs(p('dist'), exist_ok=True)
    open(p('dist/plusone-demo.html'), 'w', encoding='utf-8').write(out)
    print('built', len(out), 'bytes ->', p('dist/plusone-demo.html'))
