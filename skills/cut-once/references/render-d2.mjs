// render-d2.mjs — compile every d2/*.d2 to diagrams/<name>.svg (self-contained inline SVG).
// Usage:  npm install @terrastruct/d2 && node render-d2.mjs [srcDir=d2] [outDir=diagrams]
// ESM only (the package is ESM); run with a modern Node. No headless browser needed.
import { D2 } from '@terrastruct/d2';
import { readFileSync, writeFileSync, readdirSync, mkdirSync } from 'fs';
import { join, basename } from 'path';

const srcDir = process.argv[2] || 'd2';
const outDir = process.argv[3] || 'diagrams';
mkdirSync(outDir, { recursive: true });

const d2 = new D2();
const files = readdirSync(srcDir).filter(f => f.endsWith('.d2'));
let failed = 0;

for (const f of files) {
  const name = basename(f, '.d2');
  try {
    const src = readFileSync(join(srcDir, f), 'utf8');
    const c   = await d2.compile(src, { layout: 'dagre', themeID: 0, sketch: false, pad: 16 });
    const svg = await d2.render(c.diagram, c.renderOptions);
    writeFileSync(join(outDir, name + '.svg'), svg);
    console.log(`OK   ${name}  (${(svg.length / 1024).toFixed(0)} KB)`);
  } catch (e) {
    failed++;
    console.log(`FAIL ${name}: ${String(e.message || e).split('\n')[0]}`);
  }
}
process.exit(failed ? 1 : 0);
