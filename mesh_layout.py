"""A fixed complete-graph routing lattice, independent of selected diagram edges.

Every pair tests all 16 face combinations. Dijkstra minimizes (corners, length)
on the declared orthogonal corridor graph; deterministic coordinate/face ordering
breaks ties. This is a per-connection optimum on that fixed lattice, not a claim
of a globally crossing-free K50 embedding or joint congestion optimization.
"""
from pathlib import Path
from collections import defaultdict
from itertools import combinations
import json,hashlib,heapq

SPEC_PATH=Path('mesh-layout.json')
PLAN_PATH=Path('layout/mesh-plan.json')
FACES=('t','r','b','l')
AXIS={'t':1,'b':1,'l':0,'r':0}

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def spec_hash(spec):return hashlib.sha256(canonical(spec)).hexdigest()
def read_spec():return json.loads(SPEC_PATH.read_text())
def slot_at(cell,spec):return cell[1]*spec['columns']+cell[0]
def slot_box(slot,spec):
    row,col=divmod(slot,spec['columns']);w,h,g,m=(spec[k] for k in ['nodeWidth','nodeHeight','gutter','margin'])
    return [m+col*(w+g),m+row*(h+g),w,h]
def view_box(spec):
    return [0,0,2*spec['margin']+spec['columns']*spec['nodeWidth']+(spec['columns']-1)*spec['gutter'],2*spec['margin']+spec['rows']*spec['nodeHeight']+(spec['rows']-1)*spec['gutter']]
def pair_key(a,b):return f'{min(a,b)}:{max(a,b)}'
def pair_color(a,b,spec):
    # Round-robin edge coloring of K50: each vertex has one distinct color per
    # neighbor, and both ends of a pair reserve the same port offset.
    n=spec['rows']*spec['columns'];q=n-1
    color=min(a,b) if max(a,b)==q else ((a+b)*pow(2,-1,q))%q
    return color*spec['portPermutation']%q

def pair_geometry(a,b,spec):
    n=spec['rows']*spec['columns'];rank=pair_color(a,b,spec)+1;fraction=rank/n
    w,h,g,m=(spec[k] for k in ['nodeWidth','nodeHeight','gutter','margin'])
    width,height=view_box(spec)[2:]
    # All 49 potential tracks are evenly distributed in every internal and
    # external corridor. No track or port depends on the visible edge subset.
    xbands=[(0,m)]+[(m+c*(w+g)+w,m+(c+1)*(w+g)) for c in range(spec['columns']-1)]+[(width-m,width)]
    ybands=[(0,m)]+[(m+r*(h+g)+h,m+(r+1)*(h+g)) for r in range(spec['rows']-1)]+[(height-m,height)]
    xs=[lo+(hi-lo)*fraction for lo,hi in xbands];ys=[lo+(hi-lo)*fraction for lo,hi in ybands]
    endpoints={};anchors={}
    for slot in (a,b):
        x,y,w,h=slot_box(slot,spec);row,col=divmod(slot,spec['columns']);px=x+w*fraction;py=y+h*fraction
        endpoints[slot]={'t':(px,y),'r':(x+w,py),'b':(px,y+h),'l':(x,py)}
        anchors[slot]={'t':(px,ys[row]),'r':(xs[col+1],py),'b':(px,ys[row+1]),'l':(xs[col],py)}
    points={(x,y) for x in xs for y in ys}|{p for aa in anchors.values() for p in aa.values()}
    points=sorted(points);index={p:i for i,p in enumerate(points)};adj=[[] for _ in points]
    for axis,tracks in [(0,xs),(1,ys)]:
        for track in tracks:
            line=sorted((p for p in points if p[axis]==track),key=lambda p:p[1-axis])
            for u,v in zip(line,line[1:]):
                i,j=index[u],index[v];length=abs(u[1-axis]-v[1-axis]);orientation=1-axis
                adj[i].append((j,orientation,length));adj[j].append((i,orientation,length))
    for row in adj:row.sort()
    return {'points':points,'index':index,'adj':adj,'endpoints':endpoints,'anchors':anchors,'xTracks':xs,'yTracks':ys}

def simplify(points):
    out=[]
    for p in points:
        p=tuple(round(v,6) for v in p)
        if out and p==out[-1]:continue
        while len(out)>1 and ((out[-2][0]==out[-1][0]==p[0]) or (out[-2][1]==out[-1][1]==p[1])):out.pop()
        out.append(p)
    return [list(p) for p in out]

def evaluate_pair(a,b,spec):
    graph=pair_geometry(a,b,spec);points,index,adj=(graph[k] for k in ['points','index','adj']);ends,anchors=graph['endpoints'],graph['anchors'];candidates=[]
    for face in FACES:
        start=index[anchors[a][face]];axis=AXIS[face];stub=sum(abs(u-v) for u,v in zip(ends[a][face],anchors[a][face]))
        dist={(start,axis):(0,stub)};parent={};queue=[(0,stub,start,axis)]
        while queue:
            bends,length,node,direction=heapq.heappop(queue)
            if dist.get((node,direction))!=(bends,length):continue
            for other,new_axis,weight in adj[node]:
                cost=(bends+(direction!=new_axis),length+weight);state=(other,new_axis)
                if cost<dist.get(state,(float('inf'),float('inf'))):
                    dist[state]=cost;parent[state]=(node,direction);heapq.heappush(queue,(*cost,*state))
        for target_face in FACES:
            target=index[anchors[b][target_face]];tail=sum(abs(u-v) for u,v in zip(ends[b][target_face],anchors[b][target_face]));options=[]
            for last_axis in (0,1):
                state=(target,last_axis)
                if state in dist:
                    bends,length=dist[state];options.append(((bends+(last_axis!=AXIS[target_face]),length+tail,last_axis),state))
            cost,state=min(options);chain=[points[state[0]]]
            while state in parent:state=parent[state];chain.append(points[state[0]])
            path=simplify([ends[a][face],*reversed(chain),ends[b][target_face]])
            candidates.append({'sourceFace':face,'targetFace':target_face,'corners':len(path)-2,'length':round(cost[1],6),'points':path})
            assert candidates[-1]['corners']==cost[0],(a,b,face,target_face,cost,path)
    winner=min(candidates,key=lambda c:(c['corners'],c['length'],FACES.index(c['sourceFace']),FACES.index(c['targetFace'])))
    return {'sourceSlot':a,'targetSlot':b,'color':pair_color(a,b,spec),'winner':winner,'faceCandidates':candidates}

def build_plan(progress=False):
    spec=read_spec();n=spec['rows']*spec['columns'];assert n==50 and n%2==0
    plan={'schema':'complete-orthogonal-mesh-v1','specHash':spec_hash(spec),'spec':spec,'viewBox':view_box(spec),'slots':{str(i):slot_box(i,spec) for i in range(n)},'objective':['minimum corners','minimum Manhattan length','source face order t,r,b,l','target face order t,r,b,l','coordinate-order shortest-path tie-break'],'optimalityScope':'Exact per-face shortest path on fixed reserved-port/corridor lattice; no joint congestion or crossing-free embedding claim.','pairs':{}}
    for count,(a,b) in enumerate(combinations(range(n),2),1):
        plan['pairs'][pair_key(a,b)]=evaluate_pair(a,b,spec)
        if progress and count%250==0:print('Evaluated',count,'of1225pairs /',count*16,'face combinations',flush=True)
    plan['counts']={'slots':n,'unorderedPairs':len(plan['pairs']),'directedConnections':n*(n-1),'faceCombinations':16*len(plan['pairs']),'directedFaceCombinations':16*n*(n-1)}
    PLAN_PATH.parent.mkdir(exist_ok=True);PLAN_PATH.write_bytes(canonical(plan)+b'\n');return plan

def load_plan():
    spec=read_spec();plan=json.loads(PLAN_PATH.read_text());assert plan['specHash']==spec_hash(spec),'Rebuild the full mesh after changing layout specification'
    return plan

def route_for(plan,a,b):
    assert a!=b
    item=plan['pairs'][pair_key(a,b)];route=dict(item['winner']);route['meshPair']=pair_key(a,b);route['sourceSlot']=a;route['targetSlot']=b
    if a>b:
        route['points']=list(reversed(route['points']));route['sourceFace'],route['targetFace']=route['targetFace'],route['sourceFace']
    return route

if __name__=='__main__':
    plan=build_plan(True);print('Mesh complete:',plan['counts'],flush=True)
