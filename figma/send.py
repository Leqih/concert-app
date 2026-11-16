"""Print a ready call with image hashes / host ids substituted.  usage: send.py <callfile> [--noimg]
Record results: send.py --hashes '<json>'  |  send.py --marks '<json>'"""
import sys, json, os, re
D = os.path.dirname(os.path.abspath(__file__)); H = f'{D}/data/hashes.json'; M = f'{D}/data/marks.json'
load = lambda p: json.load(open(p)) if os.path.exists(p) else {}
if sys.argv[1] == '--hashes':
    h = load(H); h.update(json.loads(sys.argv[2])); json.dump(h, open(H, 'w')); print(len(h)); sys.exit()
if sys.argv[1] == '--marks':
    m = load(M); m.update(json.loads(sys.argv[2])); json.dump(m, open(M, 'w')); print(m); sys.exit()
code = open(f'{D}/calls/{sys.argv[1]}').read()
h = load(H); m = load(M); noimg = '--noimg' in sys.argv
def rep(mo):
    k = mo.group(1)
    return json.dumps(h[k]) if (k in h and not noimg) else 'null'
code = re.sub(r'"@(m\d+)"', rep, code)
code = re.sub(r"'@@(⟨d\d+⟩)'", lambda mo: "'" + m[mo.group(1)] + "'", code)
out = f'{D}/calls/_ready_' + sys.argv[1]; open(out, 'w').write(code); print(len(code))
