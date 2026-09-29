"""Write clips/index.json: per clip the H.264 decoder config and packet table (byte offset, size, keyframe)
so the demo can decode the same .mp4 with WebCodecs where <video> is blocked (e.g. Claude's preview panel).
Clips must be encoded with -bf 0 (decode order == display order). Needs ffprobe. Usage: python3 demo/clips/make_index.py"""
import json, os, subprocess, base64
D = os.path.dirname(os.path.abspath(__file__))
CLIPS = ['rock', 'crowd', 'bluegtr', 'ovation', 'fest', 'music', 'club']
def avcc(buf):
    i = buf.index(b'avcC'); n = int.from_bytes(buf[i-4:i], 'big'); return buf[i+4:i-4+n]
out = []
for n in CLIPS:
    f = os.path.join(D, n + '.mp4'); buf = open(f, 'rb').read(); c = avcc(buf)
    q = lambda *a: subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', *a, '-of', 'csv=p=0', f]).decode()
    num, den = map(int, q('-show_entries', 'stream=r_frame_rate').strip().split('/'))
    pk = []
    for line in q('-show_entries', 'packet=pos,size,flags').split():
        size, pos, fl = line.split(',')[:3]          # ffprobe prints size,pos,flags
        pk.append([int(pos), int(size), 1 if 'K' in fl else 0])
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))
    out.append({'n': n, 'd': round(dur, 2), 'fps': num / den, 'c': 'avc1.%02X%02X%02X' % (c[1], c[2], c[3]),
                'dsc': base64.b64encode(c).decode(), 'pk': pk})
json.dump(out, open(os.path.join(D, 'index.json'), 'w'), separators=(',', ':'))
print('\n'.join('%s %ss %d frames %s' % (x['n'], x['d'], len(x['pk']), x['c']) for x in out))
