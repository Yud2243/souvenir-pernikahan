# -*- coding: utf-8 -*-
"""
Script to update paket.html:
1. Rebuild all 28 product cards in #gs-paket-grid:
   - No modal triggers
   - Direct link to /produk/[slug]
   - Exact price displayed
   - Wedding titles & descriptions
   - data-category="tradisional" or "modern"
2. Fix any rancu wording
3. Also add price tags to paket/souvenir-modern.html and paket/souvenir-tradisional.html
"""

import sys
sys.path.append('.')
from perbaikan.generate_package_pages import modern_products, tradisional_products
import re
import urllib.parse

def build_card(p, category):
    slug = p['slug']
    title = p['title']
    badge = p['badge']
    image = p['image']
    alt = p['alt']
    lead = p['lead']
    price = p['price']
    features_json = re.sub(r'"', '&quot;', str(p['features']).replace("'", '"'))
    wa_encoded = urllib.parse.quote(p['wa_text'])
    
    return f'''          <!-- Card: {title} -->
          <article data-gs-animate class="gs-card" data-category="{category}" data-product
            data-product-image="{image}" data-product-badge="{badge}"
            data-product-title="{title}"
            data-product-desc="{lead}"
            data-product-features='{features_json}'
            data-product-wa="{p['wa_text']}">
            <div class="gs-card__image">
              <a href="/produk/{slug}" aria-label="Lihat detail {title}">
                <img src="{image}" alt="{alt}"
                  style="width:100%;height:100%;object-fit:cover;" loading="lazy" decoding="async" width="400"
                  height="300" />
              </a>
            </div>
            <div class="gs-card__body">
              <span class="gs-card__badge">{badge}</span>
              <h3 class="gs-card__title"><a href="/produk/{slug}" style="color:inherit;text-decoration:none;">{title}</a></h3>
              <p class="gs-card__desc">{lead}</p>
              <p class="gs-card__price-note"><strong style="color:var(--gs-green-800);font-size:0.95rem;">{price}</strong> &bull; Free Custom Nama &amp; Kemasan</p>
              <div class="gs-card__actions">
                <a href="/produk/{slug}" class="gs-card__btn-detail"
                  aria-label="Lihat detail {title}">
                  <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                    <path fill-rule="evenodd"
                      d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                      clip-rule="evenodd" />
                  </svg>
                  Lihat Detail
                </a>
                <a href="https://wa.me/6282131087971?text={wa_encoded}"
                  class="gs-button gs-button--whatsapp gs-button--sm" target="_blank" rel="noopener noreferrer"
                  aria-label="Konsultasi {title} via WhatsApp">Minta Penawaran</a>
              </div>
            </div>
          </article>'''

# Generate all 28 cards
all_cards = []
for p in tradisional_products:
    all_cards.append(build_card(p, "tradisional"))
for p in modern_products:
    all_cards.append(build_card(p, "modern"))

cards_html = "\n\n".join(all_cards)

with open('paket.html', 'r', encoding='utf-8') as f:
    paket_content = f.read()

# Replace the grid content in paket.html
grid_pattern = re.compile(r'(<div class="gs-grid-3" id="gs-paket-grid"[^>]*>)[\s\S]*?(</div>\s*<!-- Pagination|</div>\s*<div class="gs-pagination"|</section>)')

m = grid_pattern.search(paket_content)
if m:
    # m.group(1) is the opening div, m.group(2) is the closing marker
    # Wait, let's see what m.group(2) is
    full_match = m.group(0)
    # Check closing
    closing_pos = paket_content.find('</div>', m.start() + len(m.group(1)))
    # Instead of fragile regex, let's inspect where #gs-paket-grid ends
    start_tag = '<div class="gs-grid-3" id="gs-paket-grid" aria-live="polite">'
    start_idx = paket_content.find(start_tag)
    if start_idx == -1:
        start_tag = '<div class="gs-grid-3" id="gs-paket-grid"'
        start_idx = paket_content.find(start_tag)
        end_tag_idx = paket_content.find('>', start_idx) + 1
    else:
        end_tag_idx = start_idx + len(start_tag)

    # find the matching closing </div>
    # in paket.html, after the cards there is:
    # </div> <!-- /Catalog Grid --> or similar, followed by pagination or </section>
    # Let's search for the end of the articles:
    last_article_pos = paket_content.rfind('</article>', start_idx)
    next_div_close = paket_content.find('</div>', last_article_pos)
    
    new_paket = (
        paket_content[:end_tag_idx] +
        "\n\n" + cards_html + "\n\n        " +
        paket_content[next_div_close:]
    )
    
    # Also update any title or subtitle in paket.html
    new_paket = re.sub(
        r'<h1 class="gs-page-hero__title"[^>]*>Semua Paket Souvenir</h1>',
        '<h1 class="gs-page-hero__title" id="gs-paket-title">Katalog Paket Souvenir Pernikahan Lengkap</h1>',
        new_paket
    )
    new_paket = re.sub(
        r'<p class="gs-page-hero__desc">[\s\S]*?</p>',
        '<p class="gs-page-hero__desc">Temukan 28+ pilihan souvenir pernikahan tradisional dan modern yang unik, elegan, murah, dan bermanfaat. Dilengkapi gratis konsultasi desain nama pengantin, kemasan estetik, dan garansi pengiriman aman seluruh Indonesia.</p>',
        new_paket,
        count=1
    )
    
    with open('paket.html', 'w', encoding='utf-8') as f:
        f.write(new_paket)
    print("Successfully updated paket.html with 28 PDP-linked cards!")
else:
    print("Could not match grid in paket.html!")

# Now add price notes to paket/souvenir-modern.html and paket/souvenir-tradisional.html
for pkg_file, products_list in [('paket/souvenir-modern.html', modern_products), ('paket/souvenir-tradisional.html', tradisional_products)]:
    with open(pkg_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    for p in products_list:
        slug = p['slug']
        price = p['price']
        # If price note not already in card:
        target_str = f'<p class="gs-card__desc">{p["lead"]}</p>'
        repl_str = f'<p class="gs-card__desc">{p["lead"]}</p>\n              <p class="gs-card__price-note"><strong style="color:var(--gs-green-800);font-size:0.95rem;">{price}</strong> &bull; Free Custom Nama &amp; Kemasan</p>'
        if target_str in html and f'<strong style="color:var(--gs-green-800);font-size:0.95rem;">{price}</strong>' not in html:
            html = html.replace(target_str, repl_str, 1)
            
    with open(pkg_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Added price notes to {pkg_file}!")
