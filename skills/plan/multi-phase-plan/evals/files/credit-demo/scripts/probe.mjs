const port = process.env.PORT ?? 4317;
const times = [];
for (let i = 0; i < 30; i++) {
  const start = performance.now();
  const response = await fetch(`http://127.0.0.1:${port}/issue`, {
    method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify({credits:1})
  });
  if (!response.ok) throw new Error(`probe failed ${response.status}`);
  await response.json();
  times.push(performance.now() - start);
}
times.sort((a,b) => a-b);
console.log(JSON.stringify({metric:'issue_latency',unit:'ms',p95:times[Math.ceil(times.length * .95)-1],samples:times.length}));
