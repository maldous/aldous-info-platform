"""Render the user-approved plain C geometry in full and cumulative views."""
from pathlib import Path
from html import escape
import json,hashlib,math
from mesh_render import svg_text,wrap

def read():return json.loads(Path('current-architecture.json').read_text()),json.loads(Path('layout/approved-c.json').read_text())
def bounds(nodes,edges,layout):
    rectangles=[layout['boxes'][n['id']] for n in nodes]+[layout['labels'][e['id']]['box'] for e in edges if e['id'] in layout['labels']]
    points=[p for e in edges for p in layout['routes'][e['id']]['points']]
    xs=[r[0] for r in rectangles]+[r[0]+r[2] for r in rectangles]+[p[0] for p in points]
    ys=[r[1] for r in rectangles]+[r[1]+r[3] for r in rectangles]+[p[1] for p in points]
    x,y=math.floor(min(xs)-12),math.floor(min(ys)-12)
    return [x,y,math.ceil(max(xs)+12)-x,math.ceil(max(ys)+12)-y]

def graphic(d,layout,stage=None):
    nodes=[n for n in d['nodes'] if stage is None or n['chapter']<=stage];edges=[e for e in d['edges'] if stage is None or e['chapter']<=stage]
    missing={e['id'] for e in edges}-layout['labels'].keys()
    if missing:raise ValueError(f'Missing visible connection labels: {sorted(missing)}')
    introduced_nodes=[n for n in nodes if n['chapter']==stage] if stage is not None else []
    introduced_edges=[e for e in edges if e['chapter']==stage] if stage is not None else []
    focus_ids={n['id'] for n in introduced_nodes}|{e[k] for e in introduced_edges for k in ('source','target')}
    focus_nodes=[n for n in nodes if n['id'] in focus_ids]
    introduction=bounds(focus_nodes,introduced_edges,layout) if stage is not None else None
    intro_attr=' data-introduction-bounds="'+' '.join(map(str,introduction))+'"' if introduction else ''
    content=bounds(nodes,edges,layout);vb=' '.join(map(str,layout['viewBox']));cb=' '.join(map(str,content))
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" data-mesh="10x5" data-layout="approved-c" data-content-bounds="{cb}"{intro_attr} role="group" aria-label="{escape(d["title"] if stage is None else ["Compute","Review","Coding","Memory","Coordination","Jobs","Automation"][stage])}" font-family="OffMenuRoboto,Roboto,Arial,sans-serif"><defs>']
    for marker,color in [('current-arrow','var(--edge)'),('current-arrow-new','var(--active)')]:
        out.append(f'<marker id="{marker}" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{color}"/></marker>')
    out.append('</defs>')
    for e in edges:
        new=stage is not None and e['chapter']==stage;r=layout['routes'][e['id']];path='M'+' L'.join(f'{x:g} {y:g}' for x,y in r['points']);marker='current-arrow-new' if new else 'current-arrow';color='var(--active)' if new else 'var(--edge)';both=f'marker-start="url(#{marker})"' if e.get('direction')=='both' else ''
        out.append(f'<g data-current-edge="{e["id"]}" data-new="{str(new).lower()}" data-mesh-pair="{r["meshPair"]}" role="button" tabindex="0" aria-label="Inspect {escape(e["label"])}"><path d="{path}" fill="none" stroke="{color}" stroke-width="{2.5 if new else 1.5}" marker-end="url(#{marker})" {both}/><path d="{path}" fill="none" stroke="transparent" stroke-width="16" pointer-events="stroke"/>')
        if e['id'] in layout['labels']:
            label=layout['labels'][e['id']];x,y,w,h=label['box'];out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="var(--bg)"/>'+svg_text(label['lines'],x+w/2,y+h/2,16,'var(--subtle)'))
        out.append('</g>')
    for n in nodes:
        x,y,w,h=layout['boxes'][n['id']];new=stage is not None and n['chapter']==stage;primary=n['primary'];size=32 if primary else 26;fill='var(--primary-node-fill)' if primary else 'var(--step-node-fill)' if n.get('step') else 'var(--panel)';stroke='var(--active)' if primary or new else 'var(--edge)';weight=3.5 if new else 3 if primary else 1.5
        out.append(f'<g data-current-node="{n["id"]}" data-primary="{str(primary).lower()}" data-new="{str(new).lower()}" data-slot="{layout["slots"][n["id"]]}" role="button" tabindex="0" aria-label="Inspect {escape(n["name"])}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="{weight}"/>'+svg_text(wrap(n['name'],size,w-36),x+w/2,y+64,size,'var(--active)' if primary else 'var(--text)',700 if primary else 400)+svg_text(wrap(n['purpose'],18,w-36),x+w/2,y+112,18,'var(--subtle)')+svg_text(['PRIMARY' if primary else 'FLOW STEP' if n.get('step') else n['status']],x+w/2,y+170,14,'var(--active)' if primary else 'var(--subtle)')+'</g>')
    out.append('</svg>');svg=''.join(out)
    report={'stage':stage,'nodes':[n['id'] for n in nodes],'edges':[e['id'] for e in edges],'viewBox':layout['viewBox'],'contentBounds':content,'introductionBounds':introduction,'introductionNodes':[n['id'] for n in focus_nodes],'introductionEdges':[e['id'] for e in introduced_edges],'nodeSize':layout['nodeSize'],'nodeBoxes':{n['id']:layout['boxes'][n['id']] for n in nodes},'boxes':{n['id']:layout['boxes'][n['id']] for n in nodes},'slots':{n['id']:layout['slots'][n['id']] for n in nodes},'routes':{e['id']:layout['routes'][e['id']]['points'] for e in edges},'routeMetadata':{e['id']:{k:v for k,v in layout['routes'][e['id']].items() if k!='points'} for e in edges},'labels':{e['id']:layout['labels'][e['id']]['box'] for e in edges if e['id'] in layout['labels']},'deterministic':True,'approvedLayoutSHA256':hashlib.sha256(Path('layout/approved-c.json').read_bytes()).hexdigest(),'svgSHA256':hashlib.sha256(svg.encode()).hexdigest()}
    return svg,report

def generate_stages():
    d,layout=read();svgs=[];reports=[]
    for i in range(7):
        svg,report=graphic(d,layout,i);svgs.append(svg);reports.append(report);Path(f'review/graphical/stage-{i+1}.svg').write_text(svg)
    Path('dist/graph-layouts.js').write_text('export const graphSvgs='+json.dumps(svgs)+';\n')
    Path('review/graphical/connectivity.json').write_text(json.dumps(reports,indent=2)+'\n');print('Generated7cumulative approved-C chapters')

def generate_full():
    d,layout=read();svg,report=graphic(d,layout)
    Path('dist/current-architecture.js').write_text('export const currentArchitecture='+json.dumps(d)+';\nexport const currentArchitectureSvg='+json.dumps(svg)+';\nexport function currentArchitectureGraphic(){return currentArchitectureSvg.replace(\'<svg \',\'<svg style="width:'+str(layout['viewBox'][2])+'px;min-width:'+str(layout['viewBox'][2])+'px;max-height:none;height:auto;margin:auto" \');}\n')
    Path('review/current-architecture.svg').write_text(svg);Path('review/current-architecture-geometry.json').write_text(json.dumps(report,indent=2)+'\n');print(f'Generated approved plain C{len(d["nodes"])}nodes{len(d["edges"])}edges')
