"""Check real flow coverage, supporting-node disposition and primary hierarchy."""
import json
from pathlib import Path
from lxml import etree as E
d=json.loads(Path('current-architecture.json').read_text())
audit=json.loads(Path('review/end-to-end-coverage.json').read_text())
nodes={n['id']:n for n in d['nodes']};edges={e['id']:e for e in d['edges']}
assert len(nodes)==len(d['nodes']) and len(nodes)<=50
assert len({tuple(n['cell']) for n in nodes.values()})==len(nodes)
assert {n['name'] for n in nodes.values() if n['primary']}=={'Compute','GitHub','Linear','Sokolovski','Windmill','LangGraph'}
adj={nid:set() for nid in nodes}
for e in edges.values():
    assert e['source'] in nodes and e['target'] in nodes
    adj[e['source']].add(e['target'])
    if e.get('direction')=='both':adj[e['target']].add(e['source'])
for source,target in zip(audit['flow'],audit['flow'][1:]):assert target in adj[source],(source,target,'missing end-to-end handoff')
assert adj['review']>={'coordinator','publisher'},'review must accept or return repair feedback'
assert 'readback-step' in adj['github'] and 'coordinator' in adj['readback-step']
assert 'linear' in adj['coordinator']
assert 'outcome' in adj['main']
assert 'product deployment' in nodes['outcome']['detail']
assert 'ownership split' in d['designNote'] and 'not settled' in d['designNote']
catalog=json.loads(Path('dist/engineering.json').read_text())
assert set(audit['catalogDisposition'])=={n['id'] for n in catalog['resources']}
assert sum(r['disposition']=='explicit' for r in audit['catalogDisposition'].values())==21
for r in audit['catalogDisposition'].values():
    if r['disposition']=='explicit':assert r['fullNode'] in nodes
    else:assert r['reason']
tree=E.parse('review/current-architecture.svg');ns={'s':'http://www.w3.org/2000/svg'}
for g in tree.xpath('//s:g[@data-current-node]',namespaces=ns):
    primary=nodes[g.get('data-current-node')]['primary'];rect=g.find('s:rect',ns)
    assert g.get('data-primary')==str(primary).lower()
    assert float(rect.get('stroke-width'))==(3 if primary else 1.5)
print('PASS 35-node end-to-end flow,21retained components,6primary nodes,repair/readback/release/outcome paths and separate deployment boundary.')

# Each chapter must join its new nodes to the story already shown.
previous=set()
for chapter in range(7):
 visible={n['id'] for n in d['nodes'] if n['chapter']<=chapter};neighbors={nid:set() for nid in visible}
 for e in d['edges']:
  if e['chapter']<=chapter:
   neighbors[e['source']].add(e['target']);neighbors[e['target']].add(e['source'])
 reached={next(iter(previous or visible))};pending=list(reached)
 for nid in pending:
  for other in neighbors[nid]-reached:reached.add(other);pending.append(other)
 assert reached==visible,('Chapter leaves nodes outside the continuing story',chapter,sorted(visible-reached))
 if chapter:
  bridges=[e for e in d['edges'] if e['chapter']==chapter and ((e['source'] in previous)!=(e['target'] in previous))]
  assert bridges,('No connection back to the previous page',chapter)
 previous=visible
print('PASS all7chapters connected; each new layer links back to nodes on the previous page.')

# The restored continuation is backed by the retained source architecture.
continuation=edges['workspace-github'];native=next(e for e in catalog['relationships'] if e['id']==continuation['sourceRelationship'])
assert audit['catalogDisposition'][native['source']]['fullNode']==continuation['source']
assert audit['catalogDisposition'][native['target']]['fullNode']==continuation['target']
assert continuation['chapter']==max(nodes[continuation['source']]['chapter'],nodes[continuation['target']]['chapter'])==1
