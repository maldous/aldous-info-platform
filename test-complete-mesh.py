"""Independent complete-mesh feasibility and minimum-corner/length audit.

Rebuild the routing lattice independently and use queue-based Bellman-Ford,
not the production heap-based Dijkstra, for every source/target face case.
"""
import json,hashlib
from pathlib import Path
from collections import deque
from itertools import combinations,product

plan=json.loads(Path('layout/mesh-plan.json').read_text());spec=json.loads(Path('mesh-layout.json').read_text())
assert spec['rows']==10 and spec['columns']==5
N=50;W,H,G,M=(spec[k] for k in ['nodeWidth','nodeHeight','gutter','margin']);bounds=[0,0,2*M+5*W+4*G,2*M+10*H+9*G]
assert plan['viewBox']==bounds and len(plan['slots'])==50 and len(plan['pairs'])==1225
assert plan['counts']=={'slots':50,'unorderedPairs':1225,'directedConnections':2450,'faceCombinations':19600,'directedFaceCombinations':39200}
boxes={i:[M+(i%5)*(W+G),M+(i//5)*(H+G),W,H] for i in range(50)}
assert plan['slots']=={str(i):b for i,b in boxes.items()}
# Independent round-robin coloring proof: every node has 49 distinct sockets.
colors={}
for round_no in range(49):
    pairs=[(49,round_no)]+[((round_no+i)%49,(round_no-i)%49) for i in range(1,25)]
    for a,b in pairs:colors[tuple(sorted((a,b)))]=round_no*spec['portPermutation']%49
for node in range(50):assert len({colors[tuple(sorted((node,other)))] for other in range(50) if node!=other})==49
faces=('t','r','b','l');axis={'t':1,'r':0,'b':1,'l':0};normal={'t':(0,-1),'r':(1,0),'b':(0,1),'l':(-1,0)}

def hit(a,b,box):
    x,y,w,h=box
    if a[0]==b[0]:return x<a[0]<x+w and max(min(a[1],b[1]),y)<min(max(a[1],b[1]),y+h)
    return y<a[1]<y+h and max(min(a[0],b[0]),x)<min(max(a[0],b[0]),x+w)

face_cases=0;external_cases=0
for (a,b),color in sorted(colors.items()):
    pair=plan['pairs'][f'{a}:{b}'];assert pair['color']==color
    ratio=(color+1)/50
    xs=[M*ratio]+[M+c*(W+G)+W+G*ratio for c in range(4)]+[bounds[2]-M+M*ratio]
    ys=[M*ratio]+[M+r*(H+G)+H+G*ratio for r in range(9)]+[bounds[3]-M+M*ratio]
    ports={};anchors={}
    for node in (a,b):
        x,y,w,h=boxes[node];r,c=divmod(node,5);px=x+w*ratio;py=y+h*ratio
        ports[node]={'t':(px,y),'r':(x+w,py),'b':(px,y+h),'l':(x,py)}
        anchors[node]={'t':(px,ys[r]),'r':(xs[c+1],py),'b':(px,ys[r+1]),'l':(xs[c],py)}
    vertices=sorted(set(product(xs,ys))|{p for v in anchors.values() for p in v.values()});adj={v:[] for v in vertices}
    for coordinate,tracks in [(0,xs),(1,ys)]:
        for track in tracks:
            sequence=sorted([v for v in vertices if v[coordinate]==track],key=lambda v:v[1-coordinate])
            for u,v in zip(sequence,sequence[1:]):
                length=abs(u[1-coordinate]-v[1-coordinate]);adj[u].append((v,1-coordinate,length));adj[v].append((u,1-coordinate,length))
    cases={(c['sourceFace'],c['targetFace']):c for c in pair['faceCandidates']}
    assert set(cases)==set(product(faces,faces))
    for sf in faces:
        start=anchors[a][sf];stub=sum(abs(u-v) for u,v in zip(ports[a][sf],start));distance={(start,axis[sf]):(0,stub)};queue=deque([(start,axis[sf])]);queued=set(queue)
        while queue:
            state=queue.popleft();queued.remove(state);point,direction=state;corners,length=distance[state]
            for target,new_axis,weight in adj[point]:
                state2=(target,new_axis);cost=(corners+(new_axis!=direction),length+weight)
                if cost<distance.get(state2,(float('inf'),float('inf'))):
                    distance[state2]=cost
                    if state2 not in queued:queue.append(state2);queued.add(state2)
        for tf in faces:
            c=cases[(sf,tf)];points=c['points'];face_cases+=1
            assert points[0]==list(ports[a][sf]) and points[-1]==list(ports[b][tf])
            assert c['corners']==len(points)-2
            length=0
            for index,(u,v) in enumerate(zip(points,points[1:])):
                assert u!=v and (u[0]==v[0] or u[1]==v[1]);assert all(value%4==0 for value in u+v)
                assert all(0<=value<=bounds[2 if coordinate==0 else 3] for coordinate,value in enumerate(u))
                assert not any(hit(u,v,box) for box in boxes.values()),(a,b,sf,tf,'reserved-slot collision')
                length+=abs(u[0]-v[0])+abs(u[1]-v[1])
            assert length==c['length']
            first=[points[1][i]-points[0][i] for i in (0,1)];last=[points[-1][i]-points[-2][i] for i in (0,1)]
            assert sum(first[i]*normal[sf][i] for i in (0,1))>0
            assert sum(last[i]*normal[tf][i] for i in (0,1))<0
            target=anchors[b][tf];tail=sum(abs(u-v) for u,v in zip(target,ports[b][tf]));optimal=min((cost[0]+(direction!=axis[tf]),cost[1]+tail) for (point,direction),cost in distance.items() if point==target)
            assert (c['corners'],c['length'])==optimal,(a,b,sf,tf,'not minimum corner/length')
            if (sf=='l' and a%5==0) or (sf=='r' and a%5==4) or (sf=='t' and a//5==0) or (sf=='b' and a//5==9):external_cases+=1
    winner=min(cases.values(),key=lambda c:(c['corners'],c['length'],faces.index(c['sourceFace']),faces.index(c['targetFace'])))
    assert pair['winner']==winner
assert face_cases==19600 and external_cases>0
print('PASS complete 10x5 mesh: 50 uniform slots, 1225 pairs /2450directions, all19600face combinations feasible and independently optimal on the fixed routing lattice; unique reserved sockets, external/internal faces, no reserved-node collisions.')
