// Pure, dependency-free matching. No networking, storage, DOM or telemetry.
const escape = value => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const normalize = value => value.normalize('NFKC').replace(/[\u200B-\u200D\uFEFF]/g, '').replace(/\s+/g, ' ').trim();
function pattern(alias) {
  return new RegExp(`(?<![\\p{L}\\p{N}_])${escape(normalize(alias)).replace(/ /g,'\\s+')}(?![\\p{L}\\p{N}_])`, 'iu');
}
export function compile(corpus) {
  if (!corpus || !Array.isArray(corpus.skills)) throw new TypeError('Missing evidence corpus');
  const seen = new Set();
  return corpus.skills.map(skill => {
    if (seen.has(skill.id) || !skill.id || !skill.label || !skill.evidence?.length) throw new TypeError('Invalid evidence');
    seen.add(skill.id);
    for (const item of skill.evidence) {
      if (!item.quote || !item.section || !['cv-listed','cv-role','education','project','profile-listed','self-reported'].includes(item.kind)) throw new TypeError('Incomplete citation');
      const url = new URL(item.url);
      if (url.protocol !== 'https:') throw new TypeError('Unsafe citation');
      if(item.contextUrl && !/^(?:\.\/)?#[a-z0-9-]+$/.test(item.contextUrl))throw new TypeError('Unsafe context link');
    }
    return {...skill, patterns:[skill.label,...(skill.aliases || [])].map(pattern)};
  });
}

function matchSkills(text, compiled) {
  const found=[];
  for(const skill of compiled) for(const re of skill.patterns){
    const all=new RegExp(re.source,'giu');
    for(const match of text.matchAll(all)){
      const term=match[0];
      if(skill.id==='c' && /^[+#]/.test(text.slice(match.index+term.length)))continue;
      if(skill.id==='react' && /^\s+native\b/i.test(text.slice(match.index+term.length)))continue;
      // Common English words need capitalization or an explicit technology context.
      // A standalone term remains an intentional skill query.
      if(['rest','react','alloy','go','basic','swift','pike','c'].includes(skill.id) && term===term.toLowerCase() && normalize(text).toLowerCase()!==term.toLowerCase()){
        const following=text.slice(match.index+term.length);
        if(!/^\s*(?:api|framework|developer|engineer|development|observability|tooling|component|frontend|front-end|language|programming)\b/i.test(following))continue;
      }
      found.push({skill,start:match.index,end:match.index+term.length});
    }
  }
  // Prefer explicit multiword products: Azure DevOps does not independently prove Azure.
  const selected=found.filter(m=>!found.some(other=>other.skill.id!==m.skill.id && other.start<=m.start && other.end>=m.end && (other.end-other.start)>(m.end-m.start)));
  const ids=new Set(selected.map(m=>m.skill.id));
  return compiled.filter(s=>ids.has(s.id));
}

export function searchRequirements(input, compiled) {
  if (typeof input !== 'string') throw new TypeError('Paste text only');
  if (input.length > 30000) throw new RangeError('Use 30,000 characters or fewer');
  const lines = input.split(/\r?\n/).map(normalize).filter(Boolean);
  return {
    disclaimer:'Matches show terms with résumé, profile or project evidence, not a suitability score. Review each full requirement, including years, seniority and qualifiers.',
    lines:lines.map((text,index) => {
      const matches = matchSkills(text,compiled).map(({patterns,...skill})=>skill);
      return {id:`requirement-${index+1}`,text,matches,status:matches.length?'Evidence for recognized terms':'No recognized terms in this evidence index',needsReview:true};
    }),
    // No aggregate fit percentage. Unrecognized text never implies a missing skill.
    matchedSkills:[...new Set(lines.flatMap(text=>matchSkills(text,compiled).map(s=>s.id)))],
  };
}
