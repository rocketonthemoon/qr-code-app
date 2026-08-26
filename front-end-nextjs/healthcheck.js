const port = process.env.PORT || 3000;

fetch(`http://127.0.0.1:${port}/api/health`)
  .then((res) => process.exit(res.ok ? 0 : 1))
  .catch(() => process.exit(1));
