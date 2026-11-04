# -*- coding: utf-8 -*-
"""
Script to upgrade sitemap.xml with Google Image Sitemap schema (xmlns:image).
Attaches keyword-rich <image:image> tags to homepage, catalog pages, and all 28 PDP URLs.
"""

import sys
import re
sys.path.append('.')
from perbaikan.generate_package_pages import modern_products, tradisional_products

with open('sitemap.xml', 'r', encoding='utf-8') as f:
    text = f.read()

# Add xmlns:image to <urlset>
if 'xmlns:image=' not in text:
    text = text.replace(
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'
    )

all_prods = {p['slug']: p for p in tradisional_products + modern_products}

# For each product, inject image block if not present
for slug, p in all_prods.items():
    loc = f"https://souvenirpernikahan.web.id/produk/{slug}"
    img_url = f"https://souvenirpernikahan.web.id{p['image']}"
    title = p['title']
    lead = p['lead'][:120].replace('&', '&amp;')
    
    old_url_block = f'''  <url>
    <loc>{loc}</loc>
    <lastmod>2026-11-04</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>'''
    
    new_url_block = f'''  <url>
    <loc>{loc}</loc>
    <lastmod>2026-11-04</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
    <image:image>
      <image:loc>{img_url}</image:loc>
      <image:title>{title}</image:title>
      <image:caption>{lead}</image:caption>
    </image:image>
  </url>'''
    
    if old_url_block in text:
        text = text.replace(old_url_block, new_url_block)
    else:
        # try without exact indentation
        pattern = re.compile(rf'<url>\s*<loc>{re.escape(loc)}</loc>[\s\S]*?</url>')
        text = pattern.sub(new_url_block.strip(), text)

# Also enhance homepage and main paket pages with image tags
home_old = '''  <url>
    <loc>https://souvenirpernikahan.web.id/</loc>
    <lastmod>2026-11-04</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>'''

home_new = '''  <url>
    <loc>https://souvenirpernikahan.web.id/</loc>
    <lastmod>2026-11-04</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
    <image:image>
      <image:loc>https://souvenirpernikahan.web.id/assets/images/hero-souvenir.webp</image:loc>
      <image:title>Souvenir Pernikahan Custom Unik, Elegan &amp; Bermanfaat</image:title>
      <image:caption>Pusat vendor souvenir pernikahan custom kriya tradisional dan modern di Malang Indonesia</image:caption>
    </image:image>
  </url>'''

if home_old in text:
    text = text.replace(home_old, home_new)

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated sitemap.xml with Google Image Sitemap protocol!")
