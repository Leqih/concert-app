"""Build the single-file demo: inject data into demo2_tpl.html -> dist/plusone-demo.html
Usage: python3 demo/build.py
"""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
p = lambda f: os.path.join(D, f)
s = open(p('demo2_tpl.html'), encoding='utf-8').read()
shows = open(p('shows.js'), encoding='utf-8').read().replace('const SHOWS=', 'const NYC_SHOWS=', 1)
av = json.load(open(p('avatars.json'))); ci = json.load(open(p('cities.json'))); mp = json.load(open(p('mapdots.json')))
out = (s.replace('/*SHOWS*/', shows)
        .replace('/*AVATARS*/', json.dumps([x['img'] for x in av]))
        .replace('/*CITIES*/', json.dumps(ci))
        .replace('/*MAP*/', json.dumps(mp)))
os.makedirs(p('dist'), exist_ok=True)
open(p('dist/plusone-demo.html'), 'w', encoding='utf-8').write(out)
print('built', len(out), 'bytes ->', p('dist/plusone-demo.html'))
