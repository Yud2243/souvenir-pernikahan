const fs = require('fs');

// 1. Process 4 articles in blog/
const articles = [
  'blog/ide-souvenir-pernikahan-unik.html',
  'blog/tips-memilih-souvenir-pernikahan-unik.html',
  'blog/souvenir-pernikahan-unik-dan-bermanfaat.html',
  'blog/souvenir-pernikahan-unik-custom.html'
];

articles.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');

  // Replace '<strong>...</strong> --- ' with '<strong>...:</strong> '
  content = content.replace(/<strong>(.*?)<\/strong>\s*---\s*/g, '<strong>$1:</strong> ');

  // Replace remaining ' --- ' with ' : ' or ' – '
  content = content.replace(/\s+---\s+/g, ' &ndash; ');
  content = content.replace(/---/g, ' – ');

  // Clean out any raw openai links or markdown link leftovers
  const lines = content.split('\n');
  const cleanedLines = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.includes('images.openai.com') ||
        line.includes('purpose=inline') ||
        line.match(/^<p>\[.*?(Shopee|Etsy|Zazzle|Norway|Bodas|Canada).*?<\/p>$/i) ||
        line.match(/^<p>\[Referensi.*?<\/p>$/i) ||
        line.match(/^<p>\[.*?wedding favor.*?<\/p>$/i) ||
        line.match(/^<p>\[Contoh.*?<\/p>$/i) ||
        line.match(/^<p>\[Kipas batik.*?<\/p>$/i) ||
        line.match(/^<p>\[Gantungan kunci.*?<\/p>$/i) ||
        line.match(/^<p>pernikahan &ndash;<\/p>$/i) ||
        line.match(/^<p>pernikahan –<\/p>$/i) ||
        line.match(/^<p>favors &ndash;<\/p>$/i) ||
        line.match(/^<p>favors –<\/p>$/i) ||
        line.includes('------------ --------------------------------------------')) {
      // skip this raw draft artifact line
      continue;
    }
    cleanedLines.push(line);
  }
  content = cleanedLines.join('\n');

  fs.writeFileSync(file, content, 'utf8');
  console.log(`Cleaned ${file}`);
});

// 2. Update blog.html to add 4 new article cards at the top of gs-blog-grid
let blogHtml = fs.readFileSync('blog.html', 'utf8');

// Remove existing badge-new from older articles so only the 4 newest have them
blogHtml = blogHtml.replace(/<span class="gs-blog-card__badge-new"><span class="gs-badge-pulse" aria-hidden="true"><\/span>Artikel Terbaru<\/span>/g, '');

const newCardsHtml = `
          <!-- Artikel 1: 85 Ide Souvenir Pernikahan Unik (Pilar Utama) -->
          <article data-gs-animate class="gs-blog-card gs-blog-card-item" data-date="2026-11-24" data-category="ide">
            <div class="gs-blog-card__image">
              <span class="gs-blog-card__badge-new"><span class="gs-badge-pulse" aria-hidden="true"></span>Artikel Terbaru</span>
              <span class="gs-blog-card__badge">85 Rekomendasi</span>
              <a href="/blog/ide-souvenir-pernikahan-unik" aria-label="Baca 85 Ide Souvenir Pernikahan Unik dan Berkesan" style="display:block;width:100%;height:100%;">
                <img src="/assets/images/artikel/ide-souvenir-pernikahan-unik-400.webp"
                  alt="Koleksi 85 ide souvenir pernikahan unik dan berkesan untuk seluruh tamu undangan" loading="lazy" width="400" height="250" />
              </a>
            </div>
            <div class="gs-blog-card__body">
              <div class="gs-blog-card__meta">
                <span class="gs-blog-card__topic">Inspirasi &amp; Ide</span>
                <span class="gs-blog-card__sep" aria-hidden="true">&bull;</span>
                <span class="gs-blog-card__readtime">12 Menit Baca</span>
              </div>
              <h2 class="gs-blog-card__title">
                <a href="/blog/ide-souvenir-pernikahan-unik">85 Ide Souvenir Pernikahan Unik dan Berkesan untuk Tamu Undangan</a>
              </h2>
              <p class="gs-blog-card__excerpt">Temukan 85 ide souvenir pernikahan unik, menarik, dan bermanfaat untuk tamu undangan. Pilih kenang-kenangan yang sesuai dengan konsep pesta pernikahan Anda bersama SEKATA.</p>
              <div class="gs-blog-card__footer">
                <a href="/blog/ide-souvenir-pernikahan-unik" class="gs-blog-card__link" aria-label="Baca panduan 85 ide souvenir pernikahan unik">
                  Baca Panduan
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="width:14px;height:14px;">
                    <path d="M3 8h10M9 4l4 4-4 4" />
                  </svg>
                </a>
              </div>
            </div>
          </article>

          <!-- Artikel 2: Tips Memilih Souvenir Pernikahan Unik (Cluster 1) -->
          <article data-gs-animate class="gs-blog-card gs-blog-card-item" data-date="2026-11-24" data-category="tips">
            <div class="gs-blog-card__image">
              <span class="gs-blog-card__badge-new"><span class="gs-badge-pulse" aria-hidden="true"></span>Artikel Terbaru</span>
              <span class="gs-blog-card__badge">Panduan Tema</span>
              <a href="/blog/tips-memilih-souvenir-pernikahan-unik" aria-label="Baca Tips Memilih Souvenir Pernikahan Unik Sesuai Tema" style="display:block;width:100%;height:100%;">
                <img src="/assets/images/artikel/tips-memilih-souvenir-pernikahan-unik-400.webp"
                  alt="Panduan tips memilih souvenir pernikahan unik sesuai tema dan konsep pesta" loading="lazy" width="400" height="250" />
              </a>
            </div>
            <div class="gs-blog-card__body">
              <div class="gs-blog-card__meta">
                <span class="gs-blog-card__topic">Tips &amp; Panduan</span>
                <span class="gs-blog-card__sep" aria-hidden="true">&bull;</span>
                <span class="gs-blog-card__readtime">9 Menit Baca</span>
              </div>
              <h2 class="gs-blog-card__title">
                <a href="/blog/tips-memilih-souvenir-pernikahan-unik">Tips Memilih Souvenir Pernikahan Unik yang Sesuai dengan Tema dan Konsep Acara</a>
              </h2>
              <p class="gs-blog-card__excerpt">Pelajari tips memilih souvenir pernikahan unik sesuai tema acara, kebutuhan tamu, desain, bahan, dan anggaran agar tampil serasi dan berkesan.</p>
              <div class="gs-blog-card__footer">
                <a href="/blog/tips-memilih-souvenir-pernikahan-unik" class="gs-blog-card__link" aria-label="Baca panduan tips memilih souvenir pernikahan unik">
                  Baca Panduan
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="width:14px;height:14px;">
                    <path d="M3 8h10M9 4l4 4-4 4" />
                  </svg>
                </a>
              </div>
            </div>
          </article>

          <!-- Artikel 3: Souvenir Pernikahan Unik dan Bermanfaat (Cluster 2) -->
          <article data-gs-animate class="gs-blog-card gs-blog-card-item" data-date="2026-11-24" data-category="rekomendasi">
            <div class="gs-blog-card__image">
              <span class="gs-blog-card__badge-new"><span class="gs-badge-pulse" aria-hidden="true"></span>Artikel Terbaru</span>
              <span class="gs-blog-card__badge">Fungsional</span>
              <a href="/blog/souvenir-pernikahan-unik-dan-bermanfaat" aria-label="Baca Souvenir Pernikahan Unik dan Bermanfaat" style="display:block;width:100%;height:100%;">
                <img src="/assets/images/artikel/souvenir-pernikahan-unik-dan-bermanfaat-400.webp"
                  alt="Inspirasi souvenir pernikahan fungsional dan bermanfaat untuk tamu" loading="lazy" width="400" height="250" />
              </a>
            </div>
            <div class="gs-blog-card__body">
              <div class="gs-blog-card__meta">
                <span class="gs-blog-card__topic">Rekomendasi</span>
                <span class="gs-blog-card__sep" aria-hidden="true">&bull;</span>
                <span class="gs-blog-card__readtime">10 Menit Baca</span>
              </div>
              <h2 class="gs-blog-card__title">
                <a href="/blog/souvenir-pernikahan-unik-dan-bermanfaat">Souvenir Pernikahan Unik dan Bermanfaat yang Selalu Diingat Tamu</a>
              </h2>
              <p class="gs-blog-card__excerpt">Temukan inspirasi souvenir pernikahan unik dan fungsional yang benar-benar digunakan tamu dalam kehidupan sehari-hari, bukan sekadar pajangan.</p>
              <div class="gs-blog-card__footer">
                <a href="/blog/souvenir-pernikahan-unik-dan-bermanfaat" class="gs-blog-card__link" aria-label="Baca panduan souvenir pernikahan unik dan bermanfaat">
                  Baca Panduan
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="width:14px;height:14px;">
                    <path d="M3 8h10M9 4l4 4-4 4" />
                  </svg>
                </a>
              </div>
            </div>
          </article>

          <!-- Artikel 4: Souvenir Pernikahan Unik Custom (Cluster 3) -->
          <article data-gs-animate class="gs-blog-card gs-blog-card-item" data-date="2026-11-24" data-category="custom">
            <div class="gs-blog-card__image">
              <span class="gs-blog-card__badge-new"><span class="gs-badge-pulse" aria-hidden="true"></span>Artikel Terbaru</span>
              <span class="gs-blog-card__badge">Custom Desain</span>
              <a href="/blog/souvenir-pernikahan-unik-custom" aria-label="Baca Souvenir Pernikahan Unik Custom" style="display:block;width:100%;height:100%;">
                <img src="/assets/images/artikel/souvenir-pernikahan-unik-custom-400.webp"
                  alt="Inspirasi souvenir pernikahan kustom personalisasi inisial nama dan packaging elegan" loading="lazy" width="400" height="250" />
              </a>
            </div>
            <div class="gs-blog-card__body">
              <div class="gs-blog-card__meta">
                <span class="gs-blog-card__topic">Kustomisasi</span>
                <span class="gs-blog-card__sep" aria-hidden="true">&bull;</span>
                <span class="gs-blog-card__readtime">11 Menit Baca</span>
              </div>
              <h2 class="gs-blog-card__title">
                <a href="/blog/souvenir-pernikahan-unik-custom">Souvenir Pernikahan Unik Custom: Cara Personalisasi agar Lebih Berkesan</a>
              </h2>
              <p class="gs-blog-card__excerpt">Panduan lengkap personalisasi souvenir pernikahan custom: teknik grafir, emboss, kemasan khusus, hingga tips produksi tepat waktu.</p>
              <div class="gs-blog-card__footer">
                <a href="/blog/souvenir-pernikahan-unik-custom" class="gs-blog-card__link" aria-label="Baca panduan souvenir pernikahan unik custom">
                  Baca Panduan
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="width:14px;height:14px;">
                    <path d="M3 8h10M9 4l4 4-4 4" />
                  </svg>
                </a>
              </div>
            </div>
          </article>
`;

const pattern = /(class=["'][^"']*gs-blog-grid[^"']*["'][^>]*>)/i;
if (pattern.test(blogHtml)) {
  blogHtml = blogHtml.replace(pattern, `$1\r\n${newCardsHtml}`);
  fs.writeFileSync('blog.html', blogHtml, 'utf8');
  console.log('Successfully inserted 4 new article cards with badges and thumbnails to blog.html!');
} else {
  console.error('Could not find pattern in blog.html');
}
