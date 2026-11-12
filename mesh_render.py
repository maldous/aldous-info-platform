"""Rendering and label placement for selected paths from the complete mesh."""
from pathlib import Path
from html import escape
from PIL import ImageFont
import json,hashlib
from mesh_layout import load_plan,slot_at
from selected_layout import center_selection

FONT_PATH='dist/fonts/OffMenuRoboto-Regular.ttf'
def font(size):return ImageFont.truetype(FONT_PATH,size*64)
def wrap(value,size,maxwidth):
    lines=[];current='';f=font(size)
    for word in value.split():
        next=(current+' '+word).strip()
        if current and f.getlength(next)/64>maxwidth:lines.append(current);current=word
        else:current=next
    if current:lines.append(current)
    return lines

def overlaps(a,b,pad=0):return min(a[0]+a[2],b[0]+b[2])+pad>max(a[0],b[0]) and min(a[1]+a[3],b[1]+b[3])+pad>max(a[1],b[1])
def segment_hits(a,b,r):
    x,y,w,h=r
    return (a[0]==b[0] and x<a[0]<x+w and max(min(a[1],b[1]),y)<min(max(a[1],b[1]),y+h)) or (a[1]==b[1] and y<a[1]<y+h and max(min(a[0],b[0]),x)<min(max(a[0],b[0]),x+w))

def labels_for(edges,routes,plan):
    labels={};occupied=[];boxes=list(plan['slots'].values());width,height=plan['viewBox'][2:];f=font(16)
    for e in sorted(edges,key=lambda e:(-len(e['label']),e['id'])):
        candidates=[]
        for max_width in [260,140,88,48]:
            lines=wrap(e['label'],16,max_width);lw=max(f.getlength(s)/64 for s in lines)+16;lh=len(lines)*20+12
            for a,b in zip(routes[e['id']],routes[e['id']][1:]):
                if abs(a[0]-b[0])+abs(a[1]-b[1])<48:continue
                for ratio in [.5,.25,.75,.125,.875,.0625,.9375]:
                    cx=a[0]+(b[0]-a[0])*ratio;cy=a[1]+(b[1]-a[1])*ratio
                    for offset in [0,*[sign*v for v in range(8,241,8) for sign in (-1,1)]]:
                        x=cx+(offset if a[0]==b[0] else 0)-lw/2;y=cy+(offset if a[1]==b[1] else 0)-lh/2;rect=(x,y,lw,lh)
                        if x<8 or y<8 or x+lw>width-8 or y+lh>height-8:continue
                        if any(overlaps(rect,box,12) for box in boxes) or any(overlaps(rect,box,12) for box in occupied):continue
                        collisions=sum(segment_hits(c,d,rect) for other,pp in routes.items() if other!=e['id'] for c,d in zip(pp,pp[1:]))
                        candidates.append((collisions*100000+abs(offset)+abs(ratio-.5)*20+(len(lines)-1)*12,rect,lines))
        assert candidates,('No clear label position',e['id'])
        score,rect,lines=min(candidates,key=lambda v:v[0]);assert score<100000,('Label blocks another selected route',e['id'])
        labels[e['id']]={'box':list(rect),'lines':lines};occupied.append(rect)
    return labels

def svg_text(lines,x,y,size,color='var(--text)',weight=400):
    first=y-(len(lines)-1)*size*1.2/2+size*.34
    return f'<text x="{x}" y="{first}" text-anchor="middle" font-size="{size}" font-weight="{weight}" fill="{color}">'+''.join(f'<tspan x="{x}" dy="{0 if i==0 else size*1.2}">{escape(s)}</tspan>' for i,s in enumerate(lines))+'</text>'

def route_data(edges,cells,plan):
    return center_selection(edges,cells,plan)[0]

def generate_stages():
    plan=load_plan();spec=plan['spec'];cells=spec['walkthroughCells'];w,h=spec['nodeWidth'],spec['nodeHeight'];catalog=json.loads(Path('dist/engineering.json').read_text());resources={r['id']:r for r in catalog['resources']}
    stages=[['runner','code'],['workspace','github','pr','review','policy'],['isolated','provider'],['delivery','langgraph','sqlite'],['stokowski','supervisor','journal','linear'],['windmill','adapter','bridge','integration'],['durable','threads','tools','wm_mcp']]
    backbone=['runner->code','workspace->github','github->pr','pr->review','review->policy','isolated->code','isolated->workspace','isolated->provider','runner->delivery','delivery->langgraph','langgraph->sqlite','stokowski->supervisor','supervisor->isolated','stokowski->linear','stokowski->journal','stokowski->adapter','adapter->windmill','windmill->bridge','bridge->runner','windmill->integration','integration->delivery','threads->durable','durable->stokowski','durable->wm_mcp','wm_mcp->windmill','tools->wm_mcp']
    source={e['id']:e for e in catalog['relationships']};edges=[dict(source['edge-'+key],label=source['edge-'+key]['protocol']) for key in backbone];data=route_data(edges,cells,plan);routes={eid:r['points'] for eid,r in data.items()};labels=labels_for(edges,routes,plan)
    titles=[f['title'] for f in json.loads(Path('dist/operating-model.json').read_text())];out_svgs=[];reports=[];mesh_hash=hashlib.sha256(Path('layout/mesh-plan.json').read_bytes()).hexdigest()
    for stage,group in enumerate(stages):
        nodes=['node-'+name for gg in stages[:stage+1] for name in gg];visible=set(nodes);chosen=[e for e in edges if e['source'] in visible and e['target'] in visible]
        vb=' '.join(map(str,plan['viewBox']));out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" data-mesh="10x5" role="group" aria-label="{titles[stage]}: fixed grid architecture" font-family="OffMenuRoboto,Roboto,Arial,sans-serif"><defs><marker id="edge-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="var(--edge)"/></marker><marker id="edge-arrow-new" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="var(--active)"/></marker></defs>']
        for e in chosen:
            new=max(next(i for i,g in enumerate(stages) if e['source'][5:] in g),next(i for i,g in enumerate(stages) if e['target'][5:] in g))==stage
            path='M'+' L'.join(f'{x:g} {y:g}' for x,y in routes[e['id']]);x,y,lw,lh=labels[e['id']]['box'];color='var(--active)' if new else 'var(--edge)'
            out.append(f'<g data-handoff="{e["id"]}" data-new="{str(new).lower()}" data-mesh-pair="{data[e["id"]]["meshPair"]}" role="button" tabindex="0" aria-label="Inspect {escape(e["protocol"])}"><path d="{path}" fill="none" stroke="{color}" stroke-width="{2.5 if new else 1.5}" marker-end="url(#{"edge-arrow-new" if new else "edge-arrow"})"/><rect x="{x}" y="{y}" width="{lw}" height="{lh}" rx="5" fill="var(--bg)"/>'+svg_text(labels[e['id']]['lines'],x+lw/2,y+lh/2,16,'var(--subtle)')+'</g>')
        boxes={}
        for nid in nodes:
            box=plan['slots'][str(slot_at(cells[nid],spec))];boxes[nid]=box;x,y,_,_=box;new=nid[5:] in group;lines=wrap(resources[nid]['name'],26,w-40);assert len(lines)<=3
            out.append(f'<g data-actor="{nid}" data-new="{str(new).lower()}" data-slot="{slot_at(cells[nid],spec)}" role="button" tabindex="0" aria-label="Inspect {escape(resources[nid]["name"])}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="var(--panel)" stroke="{"var(--active)" if new else "var(--edge)"}" stroke-width="{2.5 if new else 1.5}"/>'+svg_text(lines,x+w/2,y+h/2,26)+'</g>')
        out.append('</svg>');svg=''.join(out);out_svgs.append(svg);Path('review/graphical').mkdir(parents=True,exist_ok=True);Path(f'review/graphical/stage-{stage+1}.svg').write_text(svg)
        remaining=set(nodes);components=[]
        while remaining:
            reach={min(remaining)}
            while True:
                previous=set(reach)
                for e in chosen:
                    if e['source'] in reach or e['target'] in reach:reach.update([e['source'],e['target']])
                if reach==previous:break
            components.append(sorted(reach));remaining-=reach
        reports.append({'stage':stage,'nodes':nodes,'edges':[e['id'] for e in chosen],'components':components,'deterministic':True,'meshPlanSHA256':mesh_hash,'centering':center_selection(edges,cells,plan)[1],'viewBox':plan['viewBox'],'nodeSize':[w,h],'nodeBoxes':boxes,'slots':{nid:slot_at(cells[nid],spec) for nid in nodes},'routes':{e['id']:routes[e['id']] for e in chosen},'routeMetadata':{e['id']:{k:v for k,v in data[e['id']].items() if k!='points'} for e in chosen},'labelBoxes':{e['id']:labels[e['id']]['box'] for e in chosen},'svgSHA256':hashlib.sha256(svg.encode()).hexdigest()})
    Path('dist/graph-layouts.js').write_text('export const graphSvgs = '+json.dumps(out_svgs)+';\n');Path('review/graphical/connectivity.json').write_text(json.dumps(reports,indent=2)+'\n');print('Generated seven views from the same10x5complete mesh; selected connections only.')

def generate_full():
    plan=load_plan();spec=plan['spec'];cells=spec['fullMapCells'];w,h=spec['nodeWidth'],spec['nodeHeight'];d=json.loads(Path('current-architecture.json').read_text());edges=d['edges'];data=route_data(edges,cells,plan);routes={eid:r['points'] for eid,r in data.items()};labels=labels_for(edges,routes,plan)
    vb=' '.join(map(str,plan['viewBox']));out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" data-mesh="10x5" role="group" aria-label="Complete end-state delivery architecture on a fixed10row5column grid" font-family="OffMenuRoboto,Roboto,Arial,sans-serif"><defs><marker id="current-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="var(--edge)"/></marker></defs>']
    for e in edges:
        path='M'+' L'.join(f'{x:g} {y:g}' for x,y in routes[e['id']]);x,y,lw,lh=labels[e['id']]['box'];both='marker-start="url(#current-arrow)"' if e.get('direction')=='both' else ''
        out.append(f'<g data-current-edge="{e["id"]}" data-mesh-pair="{data[e["id"]]["meshPair"]}" role="button" tabindex="0" aria-label="Inspect {escape(e["label"])}"><path d="{path}" fill="none" stroke="var(--edge)" stroke-width="1.5" marker-end="url(#current-arrow)" {both}/><rect x="{x}" y="{y}" width="{lw}" height="{lh}" rx="5" fill="var(--bg)"/>'+svg_text(labels[e['id']]['lines'],x+lw/2,y+lh/2,16,'var(--subtle)')+'</g>')
    boxes={}
    for n in d['nodes']:
        box=plan['slots'][str(slot_at(cells[n['id']],spec))];boxes[n['id']]=box;x,y,_,_=box
        out.append(f'<g data-current-node="{n["id"]}" data-primary="{str(n.get('primary',False)).lower()}" data-slot="{slot_at(cells[n["id"]],spec)}" role="button" tabindex="0" aria-label="Inspect {escape(n["name"])}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="var(--panel)" stroke="{'var(--active)' if n.get('primary') else 'var(--edge)'}" stroke-width="{3 if n.get('primary') else 1.5}"/>'+svg_text(wrap(n['name'],32 if n.get('primary') else 26,w-32),x+w/2,y+64,32 if n.get('primary') else 26,weight=700 if n.get('primary') else 400)+svg_text(wrap(n['purpose'],18,w-32),x+w/2,y+112,18,'var(--subtle)')+svg_text(wrap(n['status'],16,w-32),x+w/2,y+158,16,'var(--active)')+'</g>')
    out.append('</svg>');svg=''.join(out);Path('dist/current-architecture.js').write_text('export const currentArchitecture='+json.dumps(d)+';\nexport const currentArchitectureSvg='+json.dumps(svg)+';\nexport function currentArchitectureGraphic(){return currentArchitectureSvg.replace(\'<svg \',\'<svg style="width:'+str(plan['viewBox'][2])+'px;min-width:'+str(plan['viewBox'][2])+'px;max-height:none;height:auto;margin:auto" \');}\n')
    Path('review/current-architecture.svg').write_text(svg);Path('review/current-architecture-geometry.json').write_text(json.dumps({'viewBox':plan['viewBox'],'nodeSize':[w,h],'boxes':boxes,'slots':{n['id']:slot_at(cells[n['id']],spec) for n in d['nodes']},'routes':routes,'routeMetadata':{eid:{k:v for k,v in value.items() if k!='points'} for eid,value in data.items()},'labels':{eid:v['box'] for eid,v in labels.items()},'centering':center_selection(edges,cells,plan)[1],'meshPlanSHA256':hashlib.sha256(Path('layout/mesh-plan.json').read_bytes()).hexdigest(),'svgSHA256':hashlib.sha256(svg.encode()).hexdigest()},indent=2)+'\n');print('Generated full map from the same10x5complete mesh;28nodes36selected connections, centered after mesh selection.')
