# -*- coding: utf-8 -*-
"""
Script to update index.html:
1. Fix eyebrow & hero description (remove rancu phrasing, strengthen wedding keywords)
2. Update 6 featured product cards:
   - Link image & title to /produk/[slug]
   - Add price tag with specific price
   - Replace modal button with <a href="/produk/[slug]" class="gs-card__btn-detail">
3. Add visual Aggregate Rating badge (⭐ 4.9 / 5.0 • 348+ Ulasan) above Testimoni slider
4. Align the 3 testimonials in HTML with Schema JSON-LD (Anisa & Dimas, Rizky & Bella, Fajar & Citra)
"""

import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Hero eyebrow & description
old_eyebrow = '<div class="gs-hero__eyebrow">\n              <span aria-hidden="true"></span>\n              Souvenir Pernikahan &amp; Custom\n            </div>'
new_eyebrow = '<div class="gs-hero__eyebrow">\n              <span aria-hidden="true"></span>\n              Vendor Souvenir Pernikahan Unik &amp; Elegan\n            </div>'

if old_eyebrow in content:
    content = content.replace(old_eyebrow, new_eyebrow)
    print("Updated hero eyebrow")
else:
    print("Could not find exact hero eyebrow, trying regex")
    content = re.sub(
        r'<div class="gs-hero__eyebrow">[\s\S]*?Souvenir Pernikahan &amp; Custom[\s\S]*?</div>',
        new_eyebrow,
        content
    )

old_hero_desc = '<p class="gs-hero__description">\n              Temukan souvenir pernikahan custom untuk momen akad dan resepsi Anda. Hadir dengan pilihan desain tradisional dan modern, personalisasi nama pengantin dan kemasan elegan, serta konsultasi ramah melalui WhatsApp.\n            </p>'
new_hero_desc = '<p class="gs-hero__description">\n              Pusat vendor souvenir pernikahan custom, unik, elegan, murah, dan bermanfaat untuk momen akad serta resepsi. Pilihan lengkap souvenir tradisional kriya nusantara, souvenir modern minimalis, dan hampers pernikahan eksklusif dengan grafir nama pengantin serta jaminan garansi kirim utuh ke seluruh Indonesia.\n            </p>'

if old_hero_desc in content:
    content = content.replace(old_hero_desc, new_hero_desc)
    print("Updated hero description")
else:
    content = re.sub(
        r'<p class="gs-hero__description">[\s\S]*?Temukan souvenir pernikahan custom[\s\S]*?</p>',
        new_hero_desc,
        content
    )
    print("Updated hero description via regex")

# 2. Update Featured Products
# The 6 products in index.html:
featured_data = {
    "Kipas Lipat Batik Tulis Rangka Kayu": {
        "slug": "kipas-lipat-batik-tulis-kayu-jati",
        "price": "Rp 22.000 – Rp 35.000",
        "full_title": "Souvenir Pernikahan Kipas Lipat Batik Tulis Rangka Kayu Jati"
    },
    "Mug Keramik Stoneware Rustic Monogram": {
        "slug": "mug-keramik-stoneware-rustic-monogram",
        "price": "Rp 28.000 – Rp 40.000",
        "full_title": "Souvenir Pernikahan Mug Keramik Stoneware Rustic Monogram"
    },
    "Pouch Dompet Tenun Lurik Tradisional": {
        "slug": "pouch-dompet-tenun-lurik-tradisional",
        "price": "Rp 18.000 – Rp 27.000",
        "full_title": "Souvenir Pernikahan Pouch Dompet Tenun Lurik Tradisional"
    },
    "Tumbler Kopi Stainless Sage Green": {
        "slug": "tumbler-kopi-stainless-sage-green",
        "price": "Rp 45.000 – Rp 65.000",
        "full_title": "Souvenir Pernikahan Tumbler Kopi Stainless Sage Green Monogram"
    },
    "Besek Anyaman Bambu Hias Bunga Kering": {
        "slug": "besek-anyaman-bambu-bunga-kering",
        "price": "Rp 19.000 – Rp 29.000",
        "full_title": "Souvenir Pernikahan Besek Anyaman Bambu Hias Bunga Kering"
    },
    "Pouch Serut Beludru Velvet Bordir Monogram": {
        "slug": "pouch-serut-beludru-velvet-monogram",
        "price": "Rp 18.000 – Rp 28.000",
        "full_title": "Souvenir Pernikahan Pouch Serut Beludru Velvet Bordir Monogram"
    }
}

for title_key, info in featured_data.items():
    slug = info["slug"]
    price = info["price"]
    full_title = info["full_title"]
    
    # Replace action block for this product:
    # Pattern looks for button with data-modal-trigger and aria-label containing title_key
    pattern = re.compile(
        rf'(<button type="button" class="gs-card__btn-detail" data-modal-trigger\s+aria-label="Lihat detail {re.escape(title_key)}">[\s\S]*?</button>)',
        re.I
    )
    new_btn = f'''<a href="/produk/{slug}" class="gs-card__btn-detail" aria-label="Lihat detail {full_title}">
                    <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                      <path fill-rule="evenodd"
                        d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                        clip-rule="evenodd" />
                    </svg>
                    Lihat Detail
                  </a>'''
    
    if pattern.search(content):
        content = pattern.sub(new_btn, content)
        print(f"Replaced modal button with link for: {title_key}")
    else:
        print(f"Warning: could not find button for: {title_key}")

    # Add price note before .gs-card__actions if not already there
    # Look for <p class="gs-card__desc">...{title_key}... then add price note
    card_pattern = re.compile(
        rf'(<h3 class="gs-card__title">{re.escape(title_key)}</h3>\s*<p class="gs-card__desc">[\s\S]*?</p>)(\s*<div class="gs-card__actions">)',
        re.I
    )
    def repl(m):
        return f'{m.group(1)}\n                <p class="gs-card__price-note" style="margin: 0.5rem 0 0.85rem; font-size: 0.85rem; color: var(--gs-muted);"><strong style="color: var(--gs-green-800); font-size: 0.95rem;">{price}</strong> &bull; Free Custom Nama &amp; Desain</p>{m.group(2)}'
    
    if card_pattern.search(content):
        content = card_pattern.sub(repl, content)
        print(f"Added price note for: {title_key}")

# 3. Add visual Aggregate Rating badge above Testimonials
testi_section_heading = '<h2 id="gs-testi-title">Testimoni</h2>\n          <p>Apa kata pelanggan kami?</p>\n        </div>'
new_testi_heading = '''<h2 id="gs-testi-title">Testimoni Pasangan Pengantin</h2>
          <p>Kisah kepuasan calon pengantin yang mempercayakan souvenir hari bahagianya bersama Souvenir Pernikahan.</p>
        </div>

        <!-- Rating Summary Box (Social Proof & Schema Match) -->
        <div style="max-width: 560px; margin: 0 auto 2.5rem; background: var(--gs-white); border: 1px solid var(--gs-border); border-radius: 999px; padding: 0.75rem 1.75rem; display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 0.75rem; box-shadow: var(--gs-shadow-sm); text-align: center;">
          <div style="display: flex; gap: 3px; color: #f59e0b; font-size: 1.15rem;" aria-hidden="true">★★★★★</div>
          <div style="font-size: 0.92rem; color: var(--gs-green-900);">
            <strong>4.9 / 5.0</strong> &bull; Berdasarkan <strong>348+ Ulasan</strong> Pasangan Pengantin Terverifikasi
          </div>
        </div>'''

if testi_section_heading in content:
    content = content.replace(testi_section_heading, new_testi_heading)
    print("Added Rating Summary Box above testimonials")
else:
    print("Warning: could not find exact testi_section_heading")

# 4. Align testimonials with Schema JSON-LD
old_testi_block = re.search(r'<div class="gs-testimonial-grid gs-testi-slider" id="gs-home-testi-track">[\s\S]*?</div>\s*<button type="button" class="gs-slider-arrow gs-slider-arrow--next"', content)

new_testi_cards = '''<div class="gs-testimonial-grid gs-testi-slider" id="gs-home-testi-track">

            <!-- Testimoni 1 -->
            <article class="gs-testimonial-card">
              <p class="gs-testimonial-quote">"Sangat puas pesan souvenir pernikahan unik dan elegan di Malang. Pouch tenun dan tumbler kopi hasilnya rapi sekali, kemasan gift box berpita sangat berkesan bagi tamu resepsi kami. Terima kasih Souvenir Pernikahan!"</p>
              <div class="gs-testimonial-author">
                <div class="gs-testimonial-avatar" aria-hidden="true">AD</div>
                <div>
                  <div class="gs-testimonial-name">Anisa &amp; Dimas</div>
                  <div class="gs-testimonial-event">Resepsi Pernikahan &bull; Malang</div>
                  <div class="gs-testimonial-stars" aria-label="Rating 5 dari 5 bintang">
                    ★★★★★
                  </div>
                </div>
              </div>
            </article>

            <!-- Testimoni 2 -->
            <article class="gs-testimonial-card">
              <p class="gs-testimonial-quote">"Vendor souvenir pernikahan murah dan bermanfaat paling recommended untuk area Surabaya. Pengiriman cepat, grafir nama pengantin presisi, dan admin WhatsApp sangat komunikatif melayani konsultasi kami."</p>
              <div class="gs-testimonial-author">
                <div class="gs-testimonial-avatar" aria-hidden="true">RB</div>
                <div>
                  <div class="gs-testimonial-name">Rizky &amp; Bella</div>
                  <div class="gs-testimonial-event">Intimate Wedding &bull; Surabaya</div>
                  <div class="gs-testimonial-stars" aria-label="Rating 5 dari 5 bintang">
                    ★★★★★
                  </div>
                </div>
              </div>
            </article>

            <!-- Testimoni 3 -->
            <article class="gs-testimonial-card">
              <p class="gs-testimonial-quote">"Pesan 600 pcs souvenir pernikahan tradisional kipas batik tulis dan sepasang sendok kayu jati untuk kirim ke Jakarta. Packing kayu sangat aman, tidak ada yang cacat sama sekali. Tamu undangan sangat senang!"</p>
              <div class="gs-testimonial-author">
                <div class="gs-testimonial-avatar" aria-hidden="true">FC</div>
                <div>
                  <div class="gs-testimonial-name">Fajar &amp; Citra</div>
                  <div class="gs-testimonial-event">Garden Wedding &bull; Jakarta</div>
                  <div class="gs-testimonial-stars" aria-label="Rating 5 dari 5 bintang">
                    ★★★★★
                  </div>
                </div>
              </div>
            </article>

          </div>
          <button type="button" class="gs-slider-arrow gs-slider-arrow--next"'''

if old_testi_block:
    content = content[:old_testi_block.start()] + new_testi_cards + content[old_testi_block.end():]
    print("Aligned testimonial cards with Schema reviews")
else:
    print("Warning: could not match old_testi_block")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished updating index.html!")
