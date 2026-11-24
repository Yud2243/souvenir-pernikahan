const fs = require('fs');

const files = [
  'blog/ide-souvenir-pernikahan-unik.html',
  'blog/tips-memilih-souvenir-pernikahan-unik.html',
  'blog/souvenir-pernikahan-unik-dan-bermanfaat.html',
  'blog/souvenir-pernikahan-unik-custom.html'
];

files.forEach(f => {
  const c = fs.readFileSync(f, 'utf-8');
  const m = c.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
  if (!m) throw new Error('No JSON-LD in ' + f);
  const data = JSON.parse(m[1]);
  console.log(f, 'JSON-LD VALID! Graph count:', data['@graph'].length);
});
