const fs = require('fs');

const UPLOAD_DATE_ISO = "2026-11-24T14:35:00+07:00";
const UPLOAD_DATE_STR = "24 November 2026";
const UPLOAD_DATE_SHORT = "2026-11-24";
const UPLOAD_DATE_AUTHOR = "24 Nov 2026";

const newArticles = [
  {
    slug: "ide-souvenir-pernikahan-unik",
    title: "85 Ide Souvenir Pernikahan Unik dan Berkesan untuk Tamu Undangan",
    desc: "Temukan 85 ide souvenir pernikahan unik, menarik, dan bermanfaat untuk tamu undangan. Pilih kenang-kenangan yang sesuai dengan konsep acara Anda bersama SEKATA.",
    img: "/assets/images/artikel/ide-souvenir-pernikahan-unik.webp",
    category: "Pilar Panduan",
    topic: "Ide Souvenir",
    badge: "Pilar Utama",
    readTime: "12 Menit Baca",
    authorReadTime: "12 menit baca"
  },
  {
    slug: "tips-memilih-souvenir-pernikahan-unik",
    title: "Tips Memilih Souvenir Pernikahan Unik yang Sesuai dengan Tema dan Konsep Acara",
    desc: "Pelajari tips memilih souvenir pernikahan unik sesuai tema acara, kebutuhan tamu, desain, bahan, dan anggaran agar tampil serasi dan berkesan.",
    img: "/assets/images/artikel/tips-memilih-souvenir-pernikahan-unik.webp",
    category: "Tips Memilih",
    topic: "Konsep & Tema",
    badge: "Cluster Panduan",
    readTime: "9 Menit Baca",
    authorReadTime: "9 menit baca"
  },
  {
    slug: "souvenir-pernikahan-unik-dan-bermanfaat",
    title: "Rekomendasi Souvenir Pernikahan Unik dan Bermanfaat untuk Berbagai Kalangan",
    desc: "Temukan rekomendasi souvenir pernikahan unik dan bermanfaat untuk berbagai kalangan, mulai dari tumbler, pouch, totebag, hingga produk rumah tangga.",
    img: "/assets/images/artikel/souvenir-pernikahan-unik-dan-bermanfaat.webp",
    category: "Rekomendasi Produk",
    topic: "Souvenir Fungsional",
    badge: "Cluster Produk",
    readTime: "10 Menit Baca",
    authorReadTime: "10 menit baca"
  },
  {
    slug: "souvenir-pernikahan-unik-custom",
    title: "Souvenir Pernikahan Unik Custom untuk Menciptakan Kenangan yang Lebih Personal",
    desc: "Pelajari pilihan souvenir pernikahan unik custom, teknik personalisasi nama & tanggal, desain monogram, dan kemasan mewah bersama spesialis wedding SEKATA.",
    img: "/assets/images/artikel/souvenir-pernikahan-unik-custom.webp",
    category: "Panduan Custom",
    topic: "Personalisasi",
    badge: "Cluster Custom",
    readTime: "10 Menit Baca",
    authorReadTime: "10 menit baca"
  }
];

// 1. UPDATE blog.html
console.log("Updating blog.html...");
let blogHtml = fs.readFileSync('blog.html', 'utf-8');

// Build schema blogPost entries
const blogPostSchemas = newArticles.map(a => `        {
          "@type": "BlogPosting",
          "@id": "https://souvenirpernikahan.web.id/blog/${a.slug}#article",
          "headline": "${a.title}",
          "url": "https://souvenirpernikahan.web.id/blog/${a.slug}",
          "image": "https://souvenirpernikahan.web.id${a.img}",
          "datePublished": "${UPLOAD_DATE_ISO}",
          "dateModified": "${UPLOAD_DATE_ISO}",
          "description": "${a.desc}",
          "author": {
            "@type": "Person",
            "@id": "https://souvenirpernikahan.web.id/penulis#person",
            "name": "Yudi Abraham",
            "url": "https://souvenirpernikahan.web.id/penulis"
          }
        },`).join('\n');

// Insert schema entries into blogPost list
if (!blogHtml.includes('https://souvenirpernikahan.web.id/blog/ide-souvenir-pernikahan-unik#article')) {
  blogHtml = blogHtml.replace(
    /("blogPost":\s*\[\s*\n)/,
    `$1${blogPostSchemas}\n`
  );
}

// Build HTML cards
const blogCardsHtml = newArticles.map(a => `
          <!-- Artikel ${a.badge}: ${a.title} -->
          <article data-gs-animate class="gs-blog-card gs-blog-card-item" data-date="${UPLOAD_DATE_SHORT}" data-category="tips">
            <div class="gs-blog-card__image"><span class="gs-blog-card__badge-new"><span class="gs-badge-pulse" aria-hidden="true"></span>Artikel Terbaru</span>
              <span class="gs-blog-card__badge">${a.badge}</span>
              <a href="/blog/${a.slug}" aria-label="Baca ${a.title}" style="display:block;width:100%;height:100%;">
                <img src="${a.img}"
                alt="${a.title}" loading="lazy" width="400"
                height="250" />
              </a>
            </div>
            <div class="gs-blog-card__body">
              <div class="gs-blog-card__meta">
                <span class="gs-blog-card__topic">${a.topic}</span>
                <span class="gs-blog-card__sep" aria-hidden="true">&bull;</span>
                <span class="gs-blog-card__readtime">${a.readTime}</span>
              </div>
              <h2 class="gs-blog-card__title">
                <a href="/blog/${a.slug}">${a.title}</a>
              </h2>
              <p class="gs-blog-card__excerpt">${a.desc}</p>
              <div class="gs-blog-card__footer">
                <a href="/blog/${a.slug}" class="gs-blog-card__link"
                  aria-label="Baca ${a.title}">
                  Baca Panduan
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"
                    stroke-linejoin="round" aria-hidden="true" style="width:14px;height:14px;">
                    <path d="M3 8h10M9 4l4 4-4 4" />
                  </svg>
                </a>
              </div>
            </div>
          </article>
`).join('\n');

// Insert cards into .gs-blog-grid
if (!blogHtml.includes('/blog/ide-souvenir-pernikahan-unik"')) {
  blogHtml = blogHtml.replace(
    /(<div class="gs-blog-grid" id="gs-blog-grid">\s*)/,
    `$1${blogCardsHtml}\n`
  );
}

fs.writeFileSync('blog.html', blogHtml, 'utf-8');
console.log("blog.html updated.");

// 2. UPDATE penulis.html
console.log("Updating penulis.html...");
let penulisHtml = fs.readFileSync('penulis.html', 'utf-8');

const authorCardsHtml = newArticles.map(a => `
                <!-- Article Card: ${a.title} -->
                <a href="/blog/${a.slug}" class="gs-author-post-card">
                  <div class="gs-author-post-thumb">
                    <img src="${a.img}"
                      alt="${a.title}" loading="lazy" width="400"
                      height="250" />
                    <span class="gs-author-post-badge">${a.category}</span>
                  </div>
                  <div class="gs-author-post-body">
                    <h4 class="gs-author-post-title">${a.title}</h4>
                    <div class="gs-author-post-meta">
                      <span>
                        <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd"
                            d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                            clip-rule="evenodd" />
                        </svg>
                        ${UPLOAD_DATE_AUTHOR}
                      </span>
                      <span>
                        <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd"
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                            clip-rule="evenodd" />
                        </svg>
                        ${a.authorReadTime}
                      </span>
                    </div>
                  </div>
                </a>
`).join('\n');

if (!penulisHtml.includes('/blog/ide-souvenir-pernikahan-unik"')) {
  penulisHtml = penulisHtml.replace(
    /(<div class="gs-articles-grid" id="gs-author-articles-grid">\s*)/,
    `$1${authorCardsHtml}\n`
  );
}

fs.writeFileSync('penulis.html', penulisHtml, 'utf-8');
console.log("penulis.html updated.");

// 3. UPDATE sitemap.xml
console.log("Updating sitemap.xml...");
let sitemapXml = fs.readFileSync('sitemap.xml', 'utf-8');

// Update lastmod of main pages
sitemapXml = sitemapXml.replace(
  /<loc>https:\/\/souvenirpernikahan\.web\.id\/tentang<\/loc>\s*<lastmod>[^<]+<\/lastmod>/,
  `<loc>https://souvenirpernikahan.web.id/tentang</loc>\n    <lastmod>${UPLOAD_DATE_SHORT}</lastmod>`
);
sitemapXml = sitemapXml.replace(
  /<loc>https:\/\/souvenirpernikahan\.web\.id\/blog<\/loc>\s*<lastmod>[^<]+<\/lastmod>/,
  `<loc>https://souvenirpernikahan.web.id/blog</loc>\n    <lastmod>${UPLOAD_DATE_SHORT}</lastmod>`
);
sitemapXml = sitemapXml.replace(
  /<loc>https:\/\/souvenirpernikahan\.web\.id\/penulis<\/loc>\s*<lastmod>[^<]+<\/lastmod>/,
  `<loc>https://souvenirpernikahan.web.id/penulis</loc>\n    <lastmod>${UPLOAD_DATE_SHORT}</lastmod>`
);

// Append new URLs before </urlset>
const newSitemapUrls = newArticles.map(a => `  <url>
    <loc>https://souvenirpernikahan.web.id/blog/${a.slug}</loc>
    <lastmod>${UPLOAD_DATE_SHORT}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>`).join('\n');

if (!sitemapXml.includes('https://souvenirpernikahan.web.id/blog/ide-souvenir-pernikahan-unik</loc>')) {
  sitemapXml = sitemapXml.replace(
    /(<\/urlset>)/,
    `${newSitemapUrls}\n$1`
  );
}

fs.writeFileSync('sitemap.xml', sitemapXml, 'utf-8');
console.log("sitemap.xml updated.");

// 4. Update index.html hero eyebrow & description & schema
console.log("Updating index.html...");
let indexHtml = fs.readFileSync('index.html', 'utf-8');

// Eyebrow update
indexHtml = indexHtml.replace(
  /<div class="gs-hero-fullscreen__eyebrow">[\s\S]*?<\/div>/,
  `<div class="gs-hero-fullscreen__eyebrow">
            <span class="gs-hero-fullscreen__dot" aria-hidden="true"></span>
            SPESIALIS SOUVENIR PERNIKAHAN &bull; BAGIAN DARI SAKASOUVENIR.COM
          </div>`
);

// Hero desc update
indexHtml = indexHtml.replace(
  /<p class="gs-hero-fullscreen__desc">[\s\S]*?<\/p>/,
  `<p class="gs-hero-fullscreen__desc">
            SEKATA adalah spesialis souvenir pernikahan dari <strong>Saka Souvenir</strong> (<a href="https://sakasouvenir.com" target="_blank" rel="noopener noreferrer" style="color:#fff;text-decoration:underline;">sakasouvenir.com</a>). Kami mendedikasikan layanan 100% khusus untuk cinderamata pernikahan custom, akad, resepsi, dan hampers VIP dengan pengiriman aman ke seluruh Indonesia.
          </p>`
);

// Schema parentOrganization in index.html
if (!indexHtml.includes('"name": "Saka Souvenir"')) {
  indexHtml = indexHtml.replace(
    /("name":\s*"SEKATA",\s*\n\s*"url":\s*"https:\/\/souvenirpernikahan\.web\.id\/",\s*\n\s*"logo":)/,
    `"name": "SEKATA",
      "url": "https://souvenirpernikahan.web.id/",
      "parentOrganization": {
        "@type": "Organization",
        "name": "Saka Souvenir",
        "url": "https://sakasouvenir.com",
        "sameAs": [
          "https://sakasouvenir.com",
          "https://www.instagram.com/sakasouvenirmlg/"
        ]
      },
      "logo":`
  );
}

fs.writeFileSync('index.html', indexHtml, 'utf-8');
console.log("index.html updated.");

// 5. Update footer across all HTML pages
console.log("Updating footer brand description across all pages...");
const allHtmlFiles = fs.readdirSync('.').filter(f => f.endsWith('.html'));

const oldFooterTarget = `<p class="gs-footer__desc">
            Penyedia souvenir pernikahan elegan, cinderamata custom berkesan, dan kemasan berkelas di Malang untuk pengiriman ke seluruh Indonesia. Dibuat dengan perhatian penuh terhadap mutu dan detail.
          </p>`;

const newFooterReplacement = `<p class="gs-footer__desc">
            Unit spesialis souvenir pernikahan dari <strong><a href="https://sakasouvenir.com" target="_blank" rel="noopener noreferrer" style="color:inherit;text-decoration:underline;">Saka Souvenir</a></strong>. Menghadirkan cinderamata pernikahan custom elegan, berkelas, dan bernilai guna di Malang untuk pengiriman aman ke seluruh Indonesia.
          </p>`;

allHtmlFiles.forEach(f => {
  let content = fs.readFileSync(f, 'utf-8');
  if (content.includes('Penyedia souvenir pernikahan elegan, cinderamata custom berkesan')) {
    content = content.replace(
      /<p class="gs-footer__desc">[\s\S]*?Penyedia souvenir pernikahan elegan, cinderamata custom berkesan[\s\S]*?<\/p>/,
      newFooterReplacement
    );
    fs.writeFileSync(f, content, 'utf-8');
    console.log(`Updated footer in ${f}`);
  }
});

console.log("All updates completed successfully!");
