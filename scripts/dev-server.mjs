// Serveur de développement local ECOPARK (zéro dépendance).
// Sert etape0-site-live/ en appliquant les réécritures et en-têtes de vercel.json,
// pour que /agenda, /reserver, /admin... fonctionnent comme en production.
import { createServer } from 'node:http';
import { readFileSync, existsSync, statSync, createReadStream } from 'node:fs';
import { join, extname, normalize, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..', 'etape0-site-live');
const PORT = Number(process.env.PORT) || 3000;
const vercel = JSON.parse(readFileSync(join(ROOT, 'vercel.json'), 'utf8'));
const rewrites = new Map((vercel.rewrites || []).map((r) => [r.source, r.destination]));
const globalHeaders = (vercel.headers || []).flatMap((h) => h.headers || []);

const TYPES = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif',
  '.ico': 'image/x-icon', '.mp4': 'video/mp4', '.webm': 'video/webm', '.woff2': 'font/woff2', '.pdf': 'application/pdf',
};

createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  let pathname = decodeURIComponent(url.pathname);
  if (rewrites.has(pathname)) pathname = rewrites.get(pathname);
  if (pathname === '/') pathname = '/index.html';

  const file = normalize(join(ROOT, pathname));
  for (const { key, value } of globalHeaders) res.setHeader(key, value);
  res.setHeader('Cache-Control', 'no-store');

  if (!file.startsWith(ROOT) || !existsSync(file) || !statSync(file).isFile()) {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end(`404 — ${url.pathname}`);
    console.log(`404 ${url.pathname}`);
    return;
  }
  res.writeHead(200, { 'Content-Type': TYPES[extname(file).toLowerCase()] || 'application/octet-stream' });
  createReadStream(file).pipe(res);
}).listen(PORT, () => {
  console.log(`ECOPARK — serveur local : http://localhost:${PORT}`);
  console.log(`Routes : /  /agenda  /reserver  /nos-tarifs  /guichet  /direction  /admin  (?demo=77 pour le mode démo)`);
});
