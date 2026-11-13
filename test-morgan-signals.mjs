import assert from 'node:assert/strict';
import fs from 'node:fs';
const html=fs.readFileSync('dist/index.html','utf8');
const css=fs.readFileSync('dist/portfolio.css','utf8');
const section=html.match(/<article[^>]*id="morgan-project"[^>]*>[\s\S]*?<\/article>/)?.[0];
assert(section,'Morgan has a project card');
assert(section.includes('concurrent, distributed multi-agent AI work'));
assert(section.includes('portfolio-assets/morgan-current.jpg'));
assert(section.includes('Morgan compact native-workstream snapshot'));
assert(section.includes('Captured image, not live status.'));
assert(!section.includes('Decorative Morgan'));
assert(!section.includes('Full worker coverage'));
for(const forbidden of ['morgan-signals','morgan-cix-glow','morgan-red-a','morgan-red-b','morgan-motion-toggle']) {
 assert(!section.includes(forbidden));assert(!css.includes(forbidden));
}
assert(!html.includes('morgan-signals.js'));
assert(html.includes('platform engineering, cloud delivery, release processes and production reliability'));
assert(!section.includes('In development')); // Published project card intentionally omits the retired status label.
assert(!section.includes('<details'));
assert.equal((html.match(/id="morgan-project"/g)||[]).length,1);
assert(html.includes('href="https://morgan.aldous.info/">Explore monitoring'));
for(const path of ['dist/index.html','dist/recruiters.html']) {
 const page=fs.readFileSync(path,'utf8');
 assert(page.includes('<h4>Australia (Academia)</h4><p class="career-group-label">Bachelor of Engineering (Software) Honours</p>'));
 assert(page.includes('<h4>Europe (Enterprise)</h4><p class="career-group-label">Materna, Immediate &amp; LGI</p>'));
 assert(page.includes('<h5>Immediate Solutions</h5>'));
 assert(page.includes('<h5>Liberty Global / UPC Europe</h5>'));
}
console.log('PASS the current Morgan project card uses a real dated screenshot with no fabricated status overlay, and career content remains synchronized.');
