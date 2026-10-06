import { rmSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

// Reject corrupted source styles before Vite can emit a partially styled app.
const decoder = new TextDecoder('utf-8', { fatal: true });
function validateStyles(directory) {
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) validateStyles(path);
    else if (entry.name.endsWith('.css')) {
      try { decoder.decode(readFileSync(path)); }
      catch { throw new Error(`Stylesheet is not valid UTF-8: ${path}`); }
    }
  }
}
validateStyles(join(process.cwd(), 'src'));
rmSync(join(process.cwd(), 'dist'), { recursive: true, force: true });
