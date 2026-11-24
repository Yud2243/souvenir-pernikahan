const fs = require('fs');
const path = require('path');

// 1. Copy custom thumbnails using fs.copyFileSync to ensure they are created
const artDir = path.join('assets', 'images', 'artikel');
const srcHigh = path.join(artDir, 'detail-sampel-souvenir-custom.webp');
const src400 = path.join(artDir, 'modern-pouch-kain-custom.webp');

const dstHigh = path.join(artDir, 'souvenir-pernikahan-unik-custom.webp');
const dst400 = path.join(artDir, 'souvenir-pernikahan-unik-custom-400.webp');

fs.copyFileSync(srcHigh, dstHigh);
fs.copyFileSync(src400, dst400);

console.log("Created custom thumbnails:", fs.existsSync(dstHigh), fs.existsSync(dst400));

// 2. Update index.html schema
let indexHtml = fs.readFileSync('index.html', 'utf-8');

const targetOrg = `"legalName": "Souvenir Pernikahan Malang Indonesia",
      "alternateName": [
        "SEKATA Souvenir Pernikahan",
        "Souvenir Pernikahan"
      ],
      "url": "https://souvenirpernikahan.web.id/",`;

const replOrg = `"legalName": "Souvenir Pernikahan Malang Indonesia",
      "alternateName": [
        "SEKATA Souvenir Pernikahan",
        "Souvenir Pernikahan"
      ],
      "url": "https://souvenirpernikahan.web.id/",
      "parentOrganization": {
        "@type": "Organization",
        "name": "Saka Souvenir",
        "url": "https://sakasouvenir.com",
        "sameAs": [
          "https://sakasouvenir.com",
          "https://www.instagram.com/sakasouvenirmlg/"
        ]
      },`;

indexHtml = indexHtml.replace(targetOrg, replOrg);

// Also sanitize "murah" in index.html schema
indexHtml = indexHtml.replace('pesanan souvenir pernikahan murah, bermanfaat', 'pesanan souvenir pernikahan berkualitas, bermanfaat');

fs.writeFileSync('index.html', indexHtml, 'utf-8');
console.log("Updated index.html schema and sanitized text.");
