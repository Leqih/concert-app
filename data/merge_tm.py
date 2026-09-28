"""Merge a Ticketmaster snapshot (pipe-separated, see header) into demo/shows.js.
Columns: id|name|localDate|venue|city|genre|subGenre|attraction|attractionCount|img16x9|url
Existing shows keep their embedded images; new shows reference the Ticketmaster image URL.
Adds: sub (sub-genre), kind (concert|classical|festival|residency), size (arena|theatre)."""
import json, os, re
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(D,'..','demo')
t=open(os.path.join(R,'shows.js'),encoding='utf-8').read()
old=json.loads(t[t.index('['):t.rindex(']')+1])
KEEP_CITIES={'New York','Brooklyn','Belmont Park','Queens','Bronx','Newark','East Rutherford'}
ARENA={'Madison Square Garden','Barclays Center','UBS Arena','Prudential Center','MetLife Stadium'}
SUB={'Harry Styles':'Electro Pop','Dave Matthews Band':'Alternative Rock','Andrea Bocelli':'Classical/Vocal','Stevie Wonder':'R&B','Doja Cat':'Trap','Gorillaz':'Alternative Rock','Karan Aujla':'Urban','Lady A':'Country'}
N={'Gorillaz':3,"Z100's Jingle Ball":10}
rows=[l.rstrip('\n').split('|') for l in open(os.path.join(D,'tm_nyc_2026-09-28.psv'),encoding='utf-8') if l.strip()]
have={s['artist'] for s in old}
new={}
for r in rows:
    eid,name,date,venue,city,genre,sub,art,n,img,url=r
    if city not in KEEP_CITIES or art in have: continue
    art={'Usher Raymond & Chris Brown':'Usher & Chris Brown','World of Warcraft Orchestral Concert':'World of Warcraft: 20 Years of Music','LL Cool J':'Rock The Bells Festival',"Scott Bradlee's Postmodern Jukebox":"Postmodern Jukebox",'Trombone Shorty & Orleans Avenue':'Trombone Shorty'}.get(art,art)
    k=(art,venue)
    if k not in new: new[k]={'id':eid.replace('_',''),'artist':art,'title':name,'venue':venue,'city':city,'dates':[],'genre':genre,'sub':sub,'n':int(n),'url':url,'img':img}
    new[k]['dates'].append(date)
out=[]
for s in old+list(new.values()):
    s['dates']=sorted(set(s['dates'])); s.setdefault('sub',SUB.get(s['artist'],s['genre'])); s.setdefault('n',N.get(s['artist'],1))
    nm=(s['title']+' '+s['artist']).lower()
    s['kind']=('classical' if s['genre']=='Classical' else 'festival' if (s['n']>=4 or 'festival' in nm or 'jingle ball' in nm) else 'residency' if len(s['dates'])>=4 else 'concert')
    s['size']='arena' if s['venue'] in ARENA else 'theatre'
    out.append(s)
open(os.path.join(R,'shows.js'),'w',encoding='utf-8').write('const SHOWS='+json.dumps(out,ensure_ascii=False)+';')
from collections import Counter
print(len(out),Counter(s['kind'] for s in out),Counter(s['size'] for s in out),Counter(s['genre'] for s in out))
