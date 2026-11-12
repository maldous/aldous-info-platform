"""Independently verify mesh selection followed by monotone corridor centering."""
import json
from pathlib import Path

def overlaps(a,b,pad=0):return min(a[0]+a[2],b[0]+b[2])+pad>max(a[0],b[0]) and min(a[1]+a[3],b[1]+b[3])+pad>max(a[1],b[1])
def hit(a,b,r):
    x,y,w,h=r
    return (a[0]==b[0] and x<a[0]<x+w and max(min(a[1],b[1]),y)<min(max(a[1],b[1]),y+h)) or (a[1]==b[1] and y<a[1]<y+h and max(min(a[0],b[0]),x)<min(max(a[0],b[0]),x+w))
def check_selected(view,boxes,slots,routes,metadata,labels,centering):
    plan=json.loads(Path('layout/mesh-plan.json').read_text());spec=plan['spec']
    assert view==plan['viewBox']
    for nid,box in boxes.items():assert box==plan['slots'][str(slots[nid])]
    transforms=[]
    for axis,report in enumerate(centering):
        mapping={}
        for band in report:
            lo,hi=band['walls'];values=band['initial'];centered=band['centered']
            assert values==sorted(set(values)) and all(lo<v<hi for v in values)
            expected=[round(lo+(hi-lo)*(i+1)/(len(values)+1),6) for i in range(len(values))]
            assert centered==expected,('nonuniform selected spacing',axis,lo,hi)
            mapping.update(zip(values,centered))
        transforms.append(mapping)
    for eid,pts in routes.items():
        meta=metadata[eid];a,b=meta['sourceSlot'],meta['targetSlot'];pair=plan['pairs'][f'{min(a,b)}:{max(a,b)}'];expected=pair['winner']['points']
        if a>b:expected=list(reversed(expected))
        assert meta['initialPoints']==expected,(eid,'initial route changed from complete mesh')
        refined=[[transforms[0].get(x,x),transforms[1].get(y,y)] for x,y in expected]
        assert pts==refined,(eid,'not the centered selected route')
        assert meta['corners']==len(pts)-2 and abs(meta['length']-sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip(pts,pts[1:])))<.00001
        for a,b in zip(pts,pts[1:]):assert not any(hit(a,b,box) for box in plan['slots'].values()),(eid,'reserved slot collision')
    for eid,rect in labels.items():
        for box in plan['slots'].values():assert not overlaps(rect,box),(eid,'label over reserved node')
        for other,other_rect in labels.items():
            if other!=eid:assert not overlaps(rect,other_rect),(eid,other,'label overlap')
        for other,pts in routes.items():
            if other!=eid:
                for a,b in zip(pts,pts[1:]):assert not hit(a,b,rect),(eid,other,'label obscures route')
