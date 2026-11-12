"""Independent visible geometry checks for approved C."""
import json
from pathlib import Path
from itertools import combinations
from PIL import ImageFont
j=json.loads(Path('review/current-architecture-geometry.json').read_text());d=json.loads(Path('current-architecture.json').read_text());a=json.loads(Path('layout/approved-c.json').read_text())
assert j['nodeSize']==[400,200] and len(j['boxes'])==35 and len(j['routes'])==len(d['edges'])
assert len(set(j['slots'].values()))==35 and all(0<=s<50 for s in j['slots'].values())
for nid,b in j['boxes'].items():
 assert b[2:]==[400,200] and b==a['boxes'][nid]
for eid,points in j['routes'].items():
 assert points==a['routes'][eid]['points']
 for x,y in points:assert 0<=x<=j['viewBox'][2] and 0<=y<=j['viewBox'][3]
 for p,q in zip(points,points[1:]):
  assert (p[0]==q[0]) != (p[1]==q[1]),(eid,p,q)
  for nid,(x,y,w,h) in j['boxes'].items():
   if p[0]==q[0]:assert not (x<p[0]<x+w and min(max(p[1],q[1]),y+h)>max(min(p[1],q[1]),y)),(eid,nid)
   else:assert not (y<p[1]<y+h and min(max(p[0],q[0]),x+w)>max(min(p[0],q[0]),x)),(eid,nid)
for n in d['nodes']:
 for value,size in [(n['name'],32 if n['primary'] else 26),(n['purpose'],18),(n['status'],14)]:
  font=ImageFont.truetype('dist/fonts/OffMenuRoboto-Regular.ttf',size*64);assert font.getlength(value)/64<=368,(n['id'],value)
for stage in json.loads(Path('review/graphical/connectivity.json').read_text()):
 for nid,box in stage['nodeBoxes'].items():assert box==j['boxes'][nid]
 for eid,pts in stage['routes'].items():assert pts==j['routes'][eid]
svg=Path('dist/current-architecture.js').read_text();assert '/home/user/' not in svg and 'BEGIN PRIVATE' not in svg
print('PASS approved C: uniform nodes, reserved slots, orthogonal paths, no node intersections, stable chapter geometry and fitting text.')

# Labels are part of every connection, not an optional overview-only selection.
from lxml import etree as E
from mesh_render import overlaps,segment_hits
assert set(j['labels'])==set(j['routes'])
ns={'s':'http://www.w3.org/2000/svg'};tree=E.parse('review/current-architecture.svg')
for g in tree.xpath('//s:g[@data-current-edge]',namespaces=ns):
 eid=g.get('data-current-edge');label=g.find('s:text',ns)
 assert label is not None,('Missing full-map label',eid)
 assert ' '.join(label.itertext()).split()==next(e['label'] for e in d['edges'] if e['id']==eid).split()
for eid,box in j['labels'].items():
 assert all(not overlaps(box,node) for node in j['boxes'].values()),('Label overlaps node',eid)
 for other,pts in j['routes'].items():
  if other!=eid:assert all(not segment_hits(p,q,box) for p,q in zip(pts,pts[1:])),('Label hides another route',eid,other)
for (eid,box),(other,rect) in combinations(j['labels'].items(),2):assert not overlaps(box,rect),('Label overlap',eid,other)
print('PASS all45full-map connections labelled with correct text; no label/node/other-route/label collisions.')

from mesh_layout import load_plan,route_for
route=j['routeMetadata']['workspace-github'];reserved=route_for(load_plan(),j['slots']['workspace'],j['slots']['github'])
assert route['initialPoints']==reserved['points']
assert route['corners']==reserved['corners']==2
print('PASS restored source-control link uses its deterministically evaluated minimum-corner mesh route.')
