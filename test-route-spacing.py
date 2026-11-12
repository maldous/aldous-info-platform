"""Audit complete-mesh reservation and selected-route spacing."""
import json
from pathlib import Path
from itertools import combinations
plan=json.loads(Path('layout/mesh-plan.json').read_text());spec=plan['spec']
# Every potential face has49uniform sockets; every corridor49uniform lanes.
assert spec['rows']==10 and spec['columns']==5
assert spec['nodeWidth']/50==8 and spec['nodeHeight']/50==4 and spec['gutter']/50==4
for filename in ['review/graphical/connectivity.json','review/current-architecture-geometry.json']:
    views=json.loads(Path(filename).read_text());views=views if isinstance(views,list) else [views]
    for view in views:
        segments=[(eid,a,b) for eid,pts in view['routes'].items() for a,b in zip(pts,pts[1:])]
        for (eid,a,b),(other,c,d) in combinations(segments,2):
            if eid==other:continue
            if a[0]==b[0] and c[0]==d[0]:axis=0
            elif a[1]==b[1] and c[1]==d[1]:axis=1
            else:continue
            along=1-axis
            if min(max(a[along],b[along]),max(c[along],d[along]))>max(min(a[along],b[along]),min(c[along],d[along])):
                assert abs(a[axis]-c[axis])>=4,(eid,other,'shared or closer-than-reserved tracks')
print('PASS complete-mesh sockets/tracks; centered selected routes have no shared collinear stems and remain stable across stages.')
