# -*- coding: utf-8 -*-
import re

with open('blog.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_card_pattern = re.compile(
    r'<article[^>]*data-category="event"[^>]*>[\s\S]*?panduan-souvenir-perusahaan[\s\S]*?</article>'
)

new_card = '''<article data-gs-animate class="gs-blog-card gs-blog-card-item" data-category="event">
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

if old_card_pattern.search(content):
    content = old_card_pattern.sub(new_card, content)
    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated blog archive card in blog.html!")
else:
    print("Could not match old card in blog.html!")

