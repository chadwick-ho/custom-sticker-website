const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../custom-labels-stickers-website');
const config = JSON.parse(fs.readFileSync(path.join(root, 'vercel.json'), 'utf8'));
const mime = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.xml': 'application/xml', '.txt': 'text/plain', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg' };
http.createServer((req, res) => {
  let pathname;
  try { pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname); }
  catch { res.writeHead(400).end(); return; }
  const filename = path.resolve(root, '.' + (pathname === '/' ? '/index.html' : pathname));
  if (!filename.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
  const target = fs.existsSync(filename) && fs.statSync(filename).isFile() ? filename : filename + '.html';
  if (!fs.existsSync(target) || !fs.statSync(target).isFile()) { res.writeHead(404).end('Not found'); return; }
  const headers = Object.fromEntries(config.headers[0].headers.map(h => [h.key, h.value]));
  headers['Content-Type'] = mime[path.extname(target)] || 'application/octet-stream';
  headers['Cache-Control'] = 'no-store';
  res.writeHead(200, headers);
  fs.createReadStream(target).pipe(res);
}).listen(Number(process.env.RP_PREVIEW_PORT || 8100), '127.0.0.1', () => console.log('RP preview: http://127.0.0.1:' + (process.env.RP_PREVIEW_PORT || 8100)));
