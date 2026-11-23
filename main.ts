// Entry for make.fun bounty gta6-meme-x-01 (node22, standard library only).
//
// The entry itself is a post on X: this program's whole job is to hand the
// house POST.json, which names the post. POST.json lives at the repository
// root (/bot in the grader, MAKEFUN_BOT_DIR outside it) and must land at
// /output/POST.json (MAKEFUN_OUTPUT_DIR outside the grader).
//
// The file is copied byte for byte so both runs write identical output; a
// quick shape check on the url first only warns, never changes what is
// written — the gate decides what counts as a post address.

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const postPath = join(botDir, 'POST.json');

interface PostFile {
  url?: unknown;
}

function postUrlLooksLikeStatus(post: PostFile): boolean {
  if (typeof post.url !== 'string') return false;
  return /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/[^/?#]+\/status\/\d+([?#].*)?$/.test(
    post.url,
  ) || /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/i\/web\/status\/\d+([?#].*)?$/.test(
    post.url,
  );
}

let post: PostFile;
try {
  post = JSON.parse(readFileSync(postPath, 'utf8')) as PostFile;
} catch (err) {
  console.error(`POST.json is not readable JSON at ${postPath}: ${(err as Error).message}`);
  process.exit(1);
}

if (!postUrlLooksLikeStatus(post)) {
  console.error(
    'warning: POST.json url does not look like https://x.com/<handle>/status/<id>; copying it anyway',
  );
}

mkdirSync(outputDir, { recursive: true });
try {
  copyFileSync(postPath, join(outputDir, 'POST.json'));
} catch (err) {
  console.error(`POST.json could not be copied to ${outputDir}: ${(err as Error).message}`);
  process.exit(1);
}
