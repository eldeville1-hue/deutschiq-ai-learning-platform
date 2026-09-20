import { readdir, stat } from 'node:fs/promises';
import { join } from 'node:path';

const limits = { js: 300 * 1024, css: 130 * 1024, total: 650 * 1024 };
const assets = join(process.cwd(), 'dist', 'assets');
const files = await readdir(assets);
let total = 0;
const violations = [];
for (const file of files) {
  const bytes = (await stat(join(assets, file))).size;
  total += bytes;
  const kind = file.endsWith('.js') ? 'js' : file.endsWith('.css') ? 'css' : null;
  if (kind && bytes > limits[kind]) violations.push(`${file}: ${bytes} bytes exceeds ${limits[kind]}`);
}
if (total > limits.total) violations.push(`all assets: ${total} bytes exceeds ${limits.total}`);
if (violations.length) {
  console.error(`Bundle budget failed:\n${violations.join('\n')}`);
  process.exit(1);
}
console.log(`Bundle budget passed: ${files.length} assets, ${total} bytes total.`);
