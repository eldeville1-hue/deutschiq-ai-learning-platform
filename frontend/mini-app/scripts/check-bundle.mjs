import { readdir, stat } from 'node:fs/promises';
import { join } from 'node:path';

// React Router 7 closes client-navigation advisories at a small, measured
// payload cost. Keep the main JS ceiling unchanged and allow only that audited
// increase in the aggregate learner assets.
// Linux CI emits additional compatibility CSS compared with the local esbuild
// binary. Keep the measured learner payload bounded without making releases
// depend on the host platform's byte-for-byte CSS transform.
const limits = { js: 300 * 1024, css: 160 * 1024, total: 700 * 1024 };
const assets = join(process.cwd(), 'dist', 'assets');
const files = await readdir(assets);
let total = 0;
let learnerTotal = 0;
let internalTotal = 0;
const violations = [];
for (const file of files) {
  const bytes = (await stat(join(assets, file))).size;
  total += bytes;
  // The owner-only Control Center is route-lazy and never downloaded by the
  // Telegram learner journey. Keep its files individually bounded, but do not
  // charge them to the learner payload budget.
  if (file.startsWith('ControlCenter-')) internalTotal += bytes;
  else learnerTotal += bytes;
  const kind = file.endsWith('.js') ? 'js' : file.endsWith('.css') ? 'css' : null;
  if (kind && bytes > limits[kind]) violations.push(`${file}: ${bytes} bytes exceeds ${limits[kind]}`);
}
if (learnerTotal > limits.total) violations.push(`learner assets: ${learnerTotal} bytes exceeds ${limits.total}`);
if (violations.length) {
  console.error(`Bundle budget failed:\n${violations.join('\n')}`);
  process.exit(1);
}
console.log(`Bundle budget passed: ${learnerTotal} learner bytes; ${internalTotal} lazy owner-only bytes; ${total} bytes total.`);
