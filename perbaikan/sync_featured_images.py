# -*- coding: utf-8 -*-
"""
Sync Featured Images Engine
Harmonizes featuredImage as the single source of truth across:
1. Article header cover (.gs-article__cover img)
2. Blog cards (blog.html, penulis.html, index.html)
3. Open Graph (og:image, og:image:secure_url, og:image:alt)
4. Twitter Card (twitter:image, twitter:image:alt)
5. Schema JSON-LD BlogPosting (image, primaryImageOfPage)
6. Blog hub schema JSON-LD Blog (blogPost entries)
7. Generates 400px thumbnail variants on disk to guarantee zero 404s
8. Fixes CSS broken image references
"""

import os
import re
import json
from PIL import Image

SITE_ORIGIN = "https://souvenirpernikahan.web.id"
BLOG_DIR = "blog"
ASSETS_ARTIKEL_DIR = os.path.join("assets", "images", "artikel")

def sanitize_text(text):
    if not text:
        return ""
    # Purge forbidden words: murah, ekonomis, low budget
    t = re.sub(r'\b(ekonomis)\b', 'terjangkau', text, flags=re.IGNORECASE)
    t = re.sub(r'\b(murah)\b', 'terjangkau', t, flags=re.IGNORECASE)
    t = re.sub(r'\b(low\s*budget)\b', 'ramah anggaran', t, flags=re.IGNORECASE)
    return t

def get_articles_data():
    articles = sorted([f for f in os.listdir(BLOG_DIR) if f.endswith('.html')])
    data = []

    for a in articles:
        slug = a.replace('.html', '')
        path = os.path.join(BLOG_DIR, a)
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()

        # Find cover image in .gs-article__cover
        cover_m = re.search(r'class="gs-article__cover"[^>]*>.*?<img\b([^>]+)>', html, re.DOTALL)
        src = ''
        alt = ''
        if cover_m:
            img_attrs = cover_m.group(1)
            src_m = re.search(r'src=["\']([^"\']+)["\']', img_attrs)
            alt_m = re.search(r'alt=["\']([^"\']*)["\']', img_attrs)
            if src_m:
                src = src_m.group(1).strip()
            if alt_m:
                alt = alt_m.group(1).strip()

        # If not found in cover, fallback to og:image
        if not src:
            og_m = re.search(r'<meta\b[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', html, re.DOTALL | re.IGNORECASE)
            if og_m:
                src = og_m.group(1).replace(SITE_ORIGIN, '').strip()

        # Extract title & excerpt
        title_m = re.search(r'<h1\b[^>]*>(.*?)</h1>', html, re.DOTALL)
        title = title_m.group(1).strip() if title_m else slug.replace('-', ' ').title()
        title = re.sub(r'<[^>]+>', '', title)

        desc_m = re.search(r'<meta\b[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html, re.DOTALL | re.IGNORECASE)
        desc = desc_m.group(1).strip() if desc_m else ''

        date_m = re.search(r'<time\b[^>]*datetime=["\']([^"\']+)["\']', html)
        pub_date = date_m.group(1).strip() if date_m else '2026-10-30'

        data.append({
            'slug': slug,
            'file': a,
            'path': path,
            'featured_image': src,
            'featured_alt': sanitize_text(alt),
            'title': sanitize_text(title),
            'desc': sanitize_text(desc),
            'pub_date': pub_date
        })

    return data

def sync_article_html(article_info):
    path = article_info['path']
    slug = article_info['slug']
    feat_img = article_info['featured_image']
    feat_alt = article_info['featured_alt']
    abs_img_url = f"{SITE_ORIGIN}{feat_img}"

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update .gs-article__cover img alt and ensure src is feat_img
    def update_cover_img(match):
        attrs = match.group(1)
        # replace src
        attrs = re.sub(r'src=["\'][^"\']+["\']', f'src="{feat_img}"', attrs)
        # replace alt
        attrs = re.sub(r'alt=["\'][^"\']*["\']', f'alt="{feat_alt}"', attrs)
        return f'<img {attrs.strip()}>'

    html = re.sub(r'(<figure\b[^>]*class="gs-article__cover"[^>]*>\s*)<img\b([^>]+)>', 
                  lambda m: m.group(1) + update_cover_img(m), html, flags=re.DOTALL)

    # 2. Update og:image tags
    # Replace existing og:image or insert
    if '<meta property="og:image"' in html or '<meta content=' in html and 'property="og:image"' in html:
        html = re.sub(r'<meta\b[^>]*property=["\']og:image["\'][^>]*>', 
                      f'<meta property="og:image" content="{abs_img_url}" />', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<meta\b[^>]*content=["\'][^"\']*["\'][^>]*property=["\']og:image["\'][^>]*>', 
                      f'<meta property="og:image" content="{abs_img_url}" />', html, flags=re.DOTALL | re.IGNORECASE)
    else:
        # insert after og:url or og:title
        html = re.sub(r'(<meta property="og:title"[^>]*>)', 
                      r'\1\n  <meta property="og:image" content="' + abs_img_url + '" />', html)

    # og:image:secure_url
    if '<meta property="og:image:secure_url"' in html or 'property="og:image:secure_url"' in html:
        html = re.sub(r'<meta\b[^>]*property=["\']og:image:secure_url["\'][^>]*>', 
                      f'<meta property="og:image:secure_url" content="{abs_img_url}" />', html, flags=re.DOTALL | re.IGNORECASE)
    else:
        html = re.sub(r'(<meta property="og:image"[^>]*>)', 
                      r'\1\n  <meta property="og:image:secure_url" content="' + abs_img_url + '" />', html)

    # og:image:alt
    if '<meta property="og:image:alt"' in html or 'property="og:image:alt"' in html:
        html = re.sub(r'<meta\b[^>]*property=["\']og:image:alt["\'][^>]*>', 
                      f'<meta property="og:image:alt" content="{feat_alt}" />', html, flags=re.DOTALL | re.IGNORECASE)
    else:
        html = re.sub(r'(<meta property="og:image:secure_url"[^>]*>)', 
                      r'\1\n  <meta property="og:image:alt" content="' + feat_alt + '" />', html)

    # 3. Update twitter:image tags
    if '<meta name="twitter:image"' in html or 'name="twitter:image"' in html:
        html = re.sub(r'<meta\b[^>]*name=["\']twitter:image["\'][^>]*>', 
                      f'<meta name="twitter:image" content="{abs_img_url}" />', html, flags=re.DOTALL | re.IGNORECASE)
    else:
        html = re.sub(r'(<meta name="twitter:card"[^>]*>)', 
                      r'\1\n  <meta name="twitter:image" content="' + abs_img_url + '" />', html)

    if '<meta name="twitter:image:alt"' in html or 'name="twitter:image:alt"' in html:
        html = re.sub(r'<meta\b[^>]*name=["\']twitter:image:alt["\'][^>]*>', 
                      f'<meta name="twitter:image:alt" content="{feat_alt}" />', html, flags=re.DOTALL | re.IGNORECASE)
    else:
        html = re.sub(r'(<meta name="twitter:image"[^>]*>)', 
                      r'\1\n  <meta name="twitter:image:alt" content="' + feat_alt + '" />', html)

    # 4. Update Schema JSON-LD
    schema_pattern = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)
    schema_m = schema_pattern.search(html)
    if schema_m:
        try:
            schema_data = json.loads(schema_m.group(1))
            graph = schema_data.get('@graph', [])
            for item in graph:
                if item.get('@type') == 'BlogPosting':
                    item['image'] = {
                        "@type": "ImageObject",
                        "url": abs_img_url,
                        "width": 1024,
                        "height": 576
                    }
                    item['primaryImageOfPage'] = {
                        "@type": "ImageObject",
                        "url": abs_img_url,
                        "width": 1024,
                        "height": 576
                    }
                elif item.get('@type') == 'ImageObject' and ('primary' in item.get('@id', '') or 'hero' in item.get('@id', '') or 'cover' in item.get('@id', '')):
                    item['url'] = abs_img_url
                    item['contentUrl'] = abs_img_url
            
            new_schema_str = json.dumps(schema_data, indent=2, ensure_ascii=False)
            html = html[:schema_m.start()] + f'<script type="application/ld+json">\n{new_schema_str}\n  </script>' + html[schema_m.end():]
        except Exception as e:
            print(f"Error updating schema in {slug}: {e}")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

def sync_blog_html(articles_data):
    with open('blog.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Create mapping by slug
    art_map = {a['slug']: a for a in articles_data}

    # 1. Update article cards in blog.html
    def update_blog_card(match):
        card_content = match.group(0)
        link_m = re.search(r'href=["\'](?:/blog/|blog/)?([^"\']+)["\']', card_content)
        if not link_m:
            return card_content
        slug = link_m.group(1).replace('.html', '').replace('/blog/', '').replace('blog/', '')
        if slug in art_map:
            art = art_map[slug]
            feat_img = art['featured_image']
            feat_alt = art['featured_alt']
            # update img src & alt inside this card
            def replace_img(img_m):
                attrs = img_m.group(1)
                attrs = re.sub(r'src=["\'][^"\']+["\']', f'src="{feat_img}"', attrs)
                attrs = re.sub(r'alt=["\'][^"\']*["\']', f'alt="{feat_alt}"', attrs)
                return f'<img {attrs.strip().rstrip("/").strip()} />'

            card_content = re.sub(r'<img\b([^>]+)>', replace_img, card_content, count=1)
            # update title inside h2
            card_content = re.sub(r'(<h2\b[^>]*class="[^"]*gs-blog-card__title[^"]*"[^>]*>\s*<a\b[^>]*>).*?(</a>\s*</h2>)',
                                  rf'\g<1>{art["title"]}\g<2>', card_content, flags=re.DOTALL)
            # sanitize any 'ekonomis' or 'murah' in card
            card_content = re.sub(r'\bekonomis\b', 'terjangkau', card_content, flags=re.IGNORECASE)
            card_content = re.sub(r'\bmurah\b', 'terjangkau', card_content, flags=re.IGNORECASE)
        return card_content

    html = re.sub(r'<article\b[^>]*class="[^"]*gs-blog-card[^"]*"[^>]*>.*?</article>', 
                  update_blog_card, html, flags=re.DOTALL)

    # 2. Update Schema in blog.html
    schema_pattern = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)
    schema_m = schema_pattern.search(html)
    if schema_m:
        try:
            schema_data = json.loads(schema_m.group(1))
            for item in schema_data.get('@graph', []):
                if item.get('@type') == 'Blog':
                    new_blog_posts = []
                    for art in articles_data:
                        post_entry = {
                            "@type": "BlogPosting",
                            "@id": f"{SITE_ORIGIN}/blog/{art['slug']}#article",
                            "headline": art['title'],
                            "url": f"{SITE_ORIGIN}/blog/{art['slug']}",
                            "image": f"{SITE_ORIGIN}{art['featured_image']}",
                            "datePublished": f"{art['pub_date']}T09:00:00+07:00",
                            "description": art['desc'],
                            "author": {
                                "@type": "Person",
                                "@id": f"{SITE_ORIGIN}/penulis#person",
                                "name": "Yudi Abraham",
                                "url": f"{SITE_ORIGIN}/penulis"
                            }
                        }
                        new_blog_posts.append(post_entry)
                    item['blogPost'] = new_blog_posts
            
            new_schema_str = json.dumps(schema_data, indent=2, ensure_ascii=False)
            html = html[:schema_m.start()] + f'<script type="application/ld+json">\n{new_schema_str}\n  </script>' + html[schema_m.end():]
        except Exception as e:
            print(f"Error updating schema in blog.html: {e}")

    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Synchronized blog.html successfully")

def sync_penulis_html(articles_data):
    if not os.path.exists('penulis.html'):
        return

    with open('penulis.html', 'r', encoding='utf-8') as f:
        html = f.read()

    art_map = {a['slug']: a for a in articles_data}

    # Update existing cards in penulis.html
    def update_penulis_card(match):
        card_content = match.group(0)
        link_m = re.search(r'href=["\'](?:/blog/|blog/)?([^"\']+)["\']', card_content)
        if not link_m:
            return card_content
        slug = link_m.group(1).replace('.html', '').replace('/blog/', '').replace('blog/', '')
        if slug in art_map:
            art = art_map[slug]
            feat_img = art['featured_image']
            feat_alt = art['featured_alt']
            def replace_img(img_m):
                attrs = img_m.group(1)
                attrs = re.sub(r'src=["\'][^"\']+["\']', f'src="{feat_img}"', attrs)
                attrs = re.sub(r'alt=["\'][^"\']*["\']', f'alt="{feat_alt}"', attrs)
                return f'<img {attrs.strip().rstrip("/").strip()} />'
            card_content = re.sub(r'<img\b([^>]+)>', replace_img, card_content, count=1)
            # update title inside h4
            card_content = re.sub(r'(<h4\b[^>]*class="[^"]*gs-author-post-title[^"]*"[^>]*>).*?(</h4>)',
                                  rf'\g<1>{art["title"]}\g<2>', card_content, flags=re.DOTALL)
        return card_content

    html = re.sub(r'<a\b[^>]*class="[^"]*gs-author-post-card[^"]*"[^>]*>.*?</a>', 
                  update_penulis_card, html, flags=re.DOTALL)

    # Check which articles are in penulis.html
    existing_slugs = re.findall(r'href=["\'](?:/blog/)?([^"\']+)["\'][^>]*class="[^"]*gs-author-post-card[^"]*"', html)
    existing_slugs_set = set(s.replace('.html', '') for s in existing_slugs)

    # Add missing cards to grid
    grid_m = re.search(r'(<div\b[^>]*id="gs-author-articles-grid"[^>]*>)(.*?)(</div>\s*</section>)', html, re.DOTALL)
    if grid_m:
        header = grid_m.group(1)
        body = grid_m.group(2)
        footer = grid_m.group(3)

        new_cards_str = ""
        for art in articles_data:
            if art['slug'] not in existing_slugs_set:
                new_card = f"""
                <!-- Article Card: {art['title']} -->
                <a href="/blog/{art['slug']}" class="gs-author-post-card">
                  <div class="gs-author-post-thumb">
                    <img src="{art['featured_image']}"
                      alt="{art['featured_alt']}" loading="lazy" width="400"
                      height="250" />
                    <span class="gs-author-post-badge">Panduan Pilihan</span>
                  </div>
                  <div class="gs-author-post-body">
                    <h4 class="gs-author-post-title">{art['title']}</h4>
                    <div class="gs-author-post-meta">
                      <span>
                        <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd"
                            d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                            clip-rule="evenodd" />
                        </svg>
                        {art['pub_date']}
                      </span>
                      <span>
                        <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd"
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                            clip-rule="evenodd" />
                        </svg>
                        7 menit baca
                      </span>
                    </div>
                  </div>
                </a>"""
                new_cards_str += new_card

        if new_cards_str:
            body = body + new_cards_str

        # Deduplicate cards in grid
        all_cards = re.findall(r'(?:<!--[^>]*-->\s*)?<a\b[^>]*class="[^"]*gs-author-post-card[^"]*"[^>]*>.*?</a>', body, re.DOTALL)
        seen = set()
        deduped = []
        for c in all_cards:
            sm = re.search(r'href=["\'](?:/blog/|blog/)?([^"\']+)["\']', c)
            if sm:
                slg = sm.group(1).replace('.html', '').replace('/blog/', '').replace('blog/', '')
                if slg not in seen:
                    seen.add(slg)
                    deduped.append(c.strip())
        
        new_body = "\n\n                " + "\n\n                ".join(deduped) + "\n              "
        html = html[:grid_m.start()] + header + new_body + footer + html[grid_m.end():]

    with open('penulis.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Synchronized penulis.html successfully")

def sync_index_html(articles_data):
    if not os.path.exists('index.html'):
        return

    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    art_map = {a['slug']: a for a in articles_data}

    def update_index_card(match):
        card_content = match.group(0)
        link_m = re.search(r'href=["\'](?:/blog/|blog/)?([^"\']+)["\']', card_content)
        if not link_m:
            return card_content
        slug = link_m.group(1).replace('.html', '').replace('/blog/', '').replace('blog/', '')
        if slug in art_map:
            art = art_map[slug]
            feat_img = art['featured_image']
            feat_alt = art['featured_alt']
            def replace_img(img_m):
                attrs = img_m.group(1)
                attrs = re.sub(r'src=["\'][^"\']+["\']', f'src="{feat_img}"', attrs)
                attrs = re.sub(r'alt=["\'][^"\']*["\']', f'alt="{feat_alt}"', attrs)
                return f'<img {attrs.strip().rstrip("/").strip()} />'
            card_content = re.sub(r'<img\b([^>]+)>', replace_img, card_content, count=1)
        return card_content

    html = re.sub(r'<article\b[^>]*class="[^"]*gs-blog-card[^"]*"[^>]*>.*?</article>', 
                  update_index_card, html, flags=re.DOTALL)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Synchronized index.html successfully")

def fix_css_urls():
    css_files = ['assets/css/style.css', 'assets/css/style.min.css']
    replacements = {
        '../images/craft-packaging.webp': '../images/artikel/craft-packaging.webp',
        '../images/souvenir-lilin-aroma.webp': '../images/artikel/souvenir-lilin-aroma.webp',
        '../images/souvenir-seminar-kit.webp': '../images/artikel/souvenir-seminar-kit.webp',
        '../images/artisan-soap-souvenir.webp': '../images/artikel/artisan-soap-souvenir.webp',
        '../images/linen-handkerchief-souvenir.webp': '../images/artikel/linen-handkerchief-souvenir.webp',
        '../images/hero-souvenir.webp': '../images/artikel/hero-souvenir.webp',
        '../images/hero-wedding.webp': '../images/artikel/hero-wedding.webp',
    }

    for css_p in css_files:
        if os.path.exists(css_p):
            with open(css_p, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            for old_url, new_url in replacements.items():
                content = content.replace(old_url, new_url)
            with open(css_p, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed image URLs in {css_p}")

def generate_thumbnails(articles_data):
    """Generate 400px thumbnail variants on disk to guarantee zero 404s for any tool or legacy link."""
    for art in articles_data:
        feat_img = art['featured_image'].lstrip('/')
        slug = art['slug']
        if os.path.exists(feat_img):
            base_name = os.path.splitext(os.path.basename(feat_img))[0]
            targets = [
                os.path.join(ASSETS_ARTIKEL_DIR, f"{base_name}-400.webp"),
                os.path.join(ASSETS_ARTIKEL_DIR, f"{slug}-400.webp")
            ]
            for target_path in targets:
                if not os.path.exists(target_path):
                    try:
                        with Image.open(feat_img) as im:
                            w, h = im.size
                            target_w = 400
                            target_h = int(h * (400 / w))
                            thumb = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
                            thumb.save(target_path, 'WEBP', quality=82)
                            print(f"Generated thumbnail: {target_path} ({target_w}x{target_h})")
                    except Exception as e:
                        print(f"Error generating thumbnail for {feat_img}: {e}")

def sync_related_cards(articles_data):
    """Sync related article cards inside all articles to use target's true featuredImage."""
    art_map = {a['slug']: a for a in articles_data}

    for a in articles_data:
        path = a['path']
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()

        def update_related_card(match):
            card_html = match.group(0)
            link_m = re.search(r'href=["\'](?:/blog/|blog/)?([^"\']+)["\']', card_html)
            if not link_m:
                return card_html
            slug = link_m.group(1).replace('.html', '').replace('/blog/', '').replace('blog/', '')
            if slug in art_map:
                target_art = art_map[slug]
                feat_img = target_art['featured_image']
                feat_alt = target_art['featured_alt']
                def replace_img(img_m):
                    attrs = img_m.group(1)
                    attrs = re.sub(r'src=["\'][^"\']+["\']', f'src="{feat_img}"', attrs)
                    attrs = re.sub(r'alt=["\'][^"\']*["\']', f'alt="{feat_alt}"', attrs)
                    return f'<img {attrs.strip().rstrip("/").strip()} />'
                card_html = re.sub(r'<img\b([^>]+)>', replace_img, card_html, count=1)
                # sanitize any forbidden words in card excerpt/topic
                card_html = re.sub(r'\bekonomis\b', 'terjangkau', card_html, flags=re.IGNORECASE)
                card_html = re.sub(r'\bmurah\b', 'terjangkau', card_html, flags=re.IGNORECASE)
            return card_html

        new_html = re.sub(r'<article\b[^>]*class="[^"]*gs-blog-card[^"]*"[^>]*>.*?</article>', 
                          update_related_card, html, flags=re.DOTALL)
        if new_html != html:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"Updated related cards in {a['slug']}")

def main():
    print("=== STARTING FEATURED IMAGES SYNCHRONIZATION ===")
    fix_css_urls()
    articles_data = get_articles_data()
    print(f"Found {len(articles_data)} articles in {BLOG_DIR}")

    generate_thumbnails(articles_data)

    for art in articles_data:
        sync_article_html(art)
    print("Synchronized all articles successfully")

    sync_related_cards(articles_data)
    sync_blog_html(articles_data)
    sync_penulis_html(articles_data)
    sync_index_html(articles_data)
    print("=== FEATURED IMAGES SYNCHRONIZATION COMPLETE ===")

if __name__ == '__main__':
    main()
