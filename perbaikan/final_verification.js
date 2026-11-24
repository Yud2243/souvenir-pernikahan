const fs = require('fs');
const path = require('path');

console.log("=== FINAL VERIFICATION SCRIPT ===");

// 1. Check generated articles
const newArticles = [
  'blog/ide-souvenir-pernikahan-unik.html',
  'blog/tips-memilih-souvenir-pernikahan-unik.html',
  'blog/souvenir-pernikahan-unik-dan-bermanfaat.html',
  'blog/souvenir-pernikahan-unik-custom.html'
];

let allArticlesOk = true;
newArticles.forEach(f => {
  if (!fs.existsSync(f)) {
    console.error(`ERROR: Article file missing: ${f}`);
    allArticlesOk = false;
  } else {
    const stat = fs.statSync(f);
    const html = fs.readFileSync(f, 'utf-8');
    
    // Check JSON-LD
    const jsonLdMatch = html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
    let jsonOk = false;
    if (jsonLdMatch) {
      try {
        const parsed = JSON.parse(jsonLdMatch[1]);
        jsonOk = parsed['@graph'] && parsed['@graph'].length >= 5;
      } catch (e) {
        console.error(`Invalid JSON-LD in ${f}:`, e.message);
      }
    }
    
    // Check Date
    const hasDateIso = html.includes('2026-11-24T14:35:00+07:00');
    const hasDateStr = html.includes('24 November 2026');
    
    // Check Saka Souvenir mention
    const hasSaka = html.includes('sakasouvenir.com');

    // Check forbidden words
    const hasMurah = /\bmurah\b/i.test(html);
    const hasLowBudget = /\blow\s*budget\b/i.test(html);

    console.log(`[OK] ${f}: ${stat.size} bytes | JSON-LD: ${jsonOk ? 'PASS' : 'FAIL'} | Date: ${hasDateIso && hasDateStr ? 'PASS' : 'FAIL'} | SakaSouvenir: ${hasSaka ? 'PASS' : 'FAIL'} | Forbidden words: ${(!hasMurah && !hasLowBudget) ? 'CLEAN' : 'FOUND'}`);
  }
});

// 2. Check Thumbnails
const thumbnails = [
  'assets/images/artikel/ide-souvenir-pernikahan-unik.webp',
  'assets/images/artikel/ide-souvenir-pernikahan-unik-400.webp',
  'assets/images/artikel/tips-memilih-souvenir-pernikahan-unik.webp',
  'assets/images/artikel/tips-memilih-souvenir-pernikahan-unik-400.webp',
  'assets/images/artikel/souvenir-pernikahan-unik-dan-bermanfaat.webp',
  'assets/images/artikel/souvenir-pernikahan-unik-dan-bermanfaat-400.webp',
  'assets/images/artikel/souvenir-pernikahan-unik-custom.webp',
  'assets/images/artikel/souvenir-pernikahan-unik-custom-400.webp'
];

let allThumbsOk = true;
thumbnails.forEach(t => {
  if (!fs.existsSync(t)) {
    console.error(`ERROR: Thumbnail missing: ${t}`);
    allThumbsOk = false;
  } else {
    const stat = fs.statSync(t);
    console.log(`[OK] Thumbnail: ${t} (${stat.size} bytes)`);
  }
});

// 3. Check Hubs
const blogHtml = fs.readFileSync('blog.html', 'utf-8');
const penulisHtml = fs.readFileSync('penulis.html', 'utf-8');
const sitemapXml = fs.readFileSync('sitemap.xml', 'utf-8');
const tentangHtml = fs.readFileSync('tentang.html', 'utf-8');
const indexHtml = fs.readFileSync('index.html', 'utf-8');

console.log("Checking Hub Integrations:");
console.log("- blog.html contains all 4 slugs:", newArticles.every(a => blogHtml.includes(path.basename(a, '.html'))));
console.log("- penulis.html contains all 4 slugs:", newArticles.every(a => penulisHtml.includes(path.basename(a, '.html'))));
console.log("- sitemap.xml contains all 4 slugs:", newArticles.every(a => sitemapXml.includes(path.basename(a, '.html'))));
console.log("- tentang.html has parentOrganization Saka Souvenir:", tentangHtml.includes('https://sakasouvenir.com'));
console.log("- tentang.html FAQ explains wedding exclusivity & sakasouvenir:", tentangHtml.includes('faq-a-0') && tentangHtml.includes('sakasouvenir.com'));
console.log("- index.html eyebrow mentions sakasouvenir.com:", indexHtml.includes('BAGIAN DARI SAKASOUVENIR.COM'));
console.log("- index.html schema has parentOrganization Saka Souvenir:", indexHtml.includes('"name": "Saka Souvenir"'));

console.log("=== VERIFICATION COMPLETE ===");
