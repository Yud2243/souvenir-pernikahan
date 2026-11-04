# -*- coding: utf-8 -*-
with open('blog.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace in Schema
old_schema_part = '''          "@type": "BlogPosting",
          "@id": "https://souvenirpernikahan.web.id/blog/panduan-souvenir-perusahaan#article",
          "headline": "Panduan Memilih Souvenir Perusahaan & Corporate Gift Eksklusif",
          "url": "https://souvenirpernikahan.web.id/blog/panduan-souvenir-perusahaan",
          "image": "https://souvenirpernikahan.web.id/assets/images/souvenir-plakat-akrilik.webp",
          "datePublished": "2026-09-12T09:00:00+07:00",
          "description": "Strategi cinderamata B2B untuk seminar kit, gathering tahunan, dan plakat penghargaan VIP yang memperkuat citra profesional institusi dan perusahaan Anda.",'''

new_schema_part = '''          "@type": "BlogPosting",
          "@id": "https://souvenirpernikahan.web.id/blog/panduan-souvenir-perusahaan#article",
          "headline": "Panduan Memilih Souvenir Elegan untuk Rekan Kerja & Acara Formal",
          "url": "https://souvenirpernikahan.web.id/blog/panduan-souvenir-perusahaan",
          "image": "https://souvenirpernikahan.web.id/assets/images/souvenir-seminar-kit.webp",
          "datePublished": "2026-09-12T09:00:00+07:00",
          "description": "Tips memilih souvenir pernikahan berkesan dan sopan untuk atasan kantor, rekan kerja, dan tamu kehormatan formal tanpa menguras anggaran.",'''

if old_schema_part in content:
    content = content.replace(old_schema_part, new_schema_part)
    print("Updated schema in blog.html")
else:
    print("Warning: old_schema_part not found")

# 2. Replace the HTML card
old_card_part = '''          <!-- Artikel 3 (Event - Referensi Screenshot) -->
          <article data-gs-animate class="gs-blog-card gs-blog-card-item" data-category="event">
            <div class="gs-blog-card__image">
              <span class="gs-blog-card__badge">Acara Perusahaan</span>
              <img src="/assets/images/souvenir-seminar-kit.webp"
                alt="Panduan souvenir untuk acara dan event perusahaan yang profesional" loading="lazy" width="400"
                height="250" />
            </div>
            <div class="gs-blog-card__body">
              <div class="gs-blog-card__meta">
                <span class="gs-blog-card__topic">Tips Acara</span>
                <span class="gs-blog-card__sep" aria-hidden="true">&bull;</span>
                <span class="gs-blog-card__readtime">5 Menit Baca</span>
              </div>
              <h2 class="gs-blog-card__title">
                <a href="/blog/panduan-souvenir-perusahaan">Panduan Souvenir untuk Acara dan Event Perusahaan yang
                  Profesional</a>
              </h2>
              <p class="gs-blog-card__excerpt">Hindari merchandise yang berakhir di tempat sampah. Ketahui barang-barang
                seminar kit yang fungsional, stylish, dan disukai peserta pelatihan.</p>
              <div class="gs-blog-card__footer">
                <a href="/blog/panduan-souvenir-perusahaan" class="gs-blog-card__link"
                  aria-label="Baca panduan souvenir acara perusahaan profesional">
                  Baca Panduan
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"
                    stroke-linejoin="round" aria-hidden="true" style="width:14px;height:14px;">
                    <path d="M3 8h10M9 4l4 4-4 4" />
                  </svg>
                </a>
              </div>
            </div>
          </article>'''

new_card_part = '''          <!-- Artikel 3 (Kolega & Relasi) -->
          <article data-gs-animate class="gs-blog-card gs-blog-card-item" data-category="event">
            <div class="gs-blog-card__image">
              <span class="gs-blog-card__badge">Tamu Kolega</span>
              <img src="/assets/images/souvenir-seminar-kit.webp"
                alt="Panduan memilih souvenir pernikahan elegan untuk rekan kerja dan tamu formal" loading="lazy" width="400"
                height="250" />
            </div>
            <div class="gs-blog-card__body">
              <div class="gs-blog-card__meta">
                <span class="gs-blog-card__topic">Kolega &amp; Relasi</span>
                <span class="gs-blog-card__sep" aria-hidden="true">&bull;</span>
                <span class="gs-blog-card__readtime">5 Menit Baca</span>
              </div>
              <h2 class="gs-blog-card__title">
                <a href="/blog/panduan-souvenir-perusahaan">Panduan Memilih Souvenir Elegan untuk Rekan Kerja &amp; Acara Formal</a>
              </h2>
              <p class="gs-blog-card__excerpt">Tips memilih souvenir pernikahan berkesan dan sopan untuk atasan kantor, rekan kerja, dan tamu kehormatan formal tanpa menguras anggaran.</p>
              <div class="gs-blog-card__footer">
                <a href="/blog/panduan-souvenir-perusahaan" class="gs-blog-card__link"
                  aria-label="Baca panduan souvenir pernikahan untuk rekan kerja">
                  Baca Panduan
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"
                    stroke-linejoin="round" aria-hidden="true" style="width:14px;height:14px;">
                    <path d="M3 8h10M9 4l4 4-4 4" />
                  </svg>
                </a>
              </div>
            </div>
          </article>'''

if old_card_part in content:
    content = content.replace(old_card_part, new_card_part)
    print("Updated card in blog.html")
else:
    print("Warning: old_card_part not found")

with open('blog.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished updating blog.html!")
