import http from 'node:http';
import fs from 'node:fs';
import { issue, state } from './credits.mjs';
const server = http.createServer(async (req, res) => {
  res.setHeader('content-type', 'application/json');
  if (req.method === 'GET' && req.url === '/health') return res.end('{"ok":true}');
  if (req.method === 'GET' && req.url === '/balance') return res.end(JSON.stringify(state));
  if (req.method === 'GET' && req.url === '/') {
    res.setHeader('content-type', 'text/html');
    return res.end(fs.readFileSync(new URL('./web/index.html', import.meta.url)));
  }
  if (req.method === 'POST' && req.url === '/issue') {
    try {
      let body = '';
      for await (const chunk of req) body += chunk;
      return res.end(JSON.stringify(issue(JSON.parse(body).credits)));
    } catch {
      res.statusCode = 400;
      return res.end('{"error":"invalid input"}');
    }
  }
  res.statusCode = 404;
  res.end('{"error":"not found"}');
});
server.listen(Number(process.env.PORT ?? 4317), '127.0.0.1', () => console.log('credit-demo ready'));
