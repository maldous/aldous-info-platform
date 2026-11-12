"""Center a selected mesh in its corridors without changing its topology.

The universal mesh chooses faces and minimum-corner routes first. A strictly
monotone piecewise coordinate transform then spaces the selected tracks evenly
between each pair of fixed walls. Equal coordinates stay equal; route ordering,
crossings, faces, bends and reserved-slot clearance are preserved. All cumulative
stages use their final selection's transform so routes do not move between stages.
"""
from mesh_layout import route_for, slot_at, simplify

def bands(plan, axis):
    extent=plan['viewBox'][axis+2]
    walls={0,extent}
    for box in plan['slots'].values():walls.update((box[axis],box[axis]+box[axis+2]))
    walls=sorted(walls)
    return list(zip(walls,walls[1:]))

def center_selection(edges,cells,plan):
    initial={}
    for edge in edges:
        a,b=(slot_at(cells[edge[k]],plan['spec']) for k in ('source','target'))
        initial[edge['id']]=route_for(plan,a,b)
    transforms=[];report=[]
    for axis in (0,1):
        coordinates={p[axis] for route in initial.values() for p in route['points']}
        mapping={};axis_report=[]
        for lo,hi in bands(plan,axis):
            values=sorted(v for v in coordinates if lo<v<hi)
            centered=[round(lo+(hi-lo)*(i+1)/(len(values)+1),6) for i in range(len(values))]
            mapping.update(zip(values,centered))
            if values:axis_report.append({'walls':[lo,hi],'initial':values,'centered':centered,'spacing':(hi-lo)/(len(values)+1)})
        transforms.append(mapping);report.append(axis_report)
    refined={}
    for eid,route in initial.items():
        points=[[transforms[0].get(x,x),transforms[1].get(y,y)] for x,y in route['points']]
        assert len(simplify(points))==len(points),'Centering must preserve the chosen corners'
        refined[eid]={**route,'initialPoints':route['points'],'initialLength':route['length'],'points':points,'length':round(sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip(points,points[1:])),6),'refinement':'centered-selected-corridors-v1'}
    return refined,report
