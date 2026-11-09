import os, sys, re, json

MD_PATH = r"c:\Users\Dibra\Downloads\4_artikel_seo_souvenir_pernikahan_sekata.md"
BLOG_DIR = r"c:\Untuk_PKL\Souvenirkeuda\blog"

with open(MD_PATH, 'r', encoding='utf-8') as f:
    full_text = f.read()

raw_articles = re.split(r'\n(?=\*\*(?:ARTIKEL PILAR|CLUSTER \d+)\*\*)', full_text)

def clean_inline(text):
    text = re.sub(r'\[([^\]]+)\]\(/artikel/([a-zA-Z0-9_\-]+)/?\)', r'<a href="/blog/\2">\1</a>', text)
    text = re.sub(r'\[([^\]]+)\]\(https://souvenirpernikahan\.web\.id/blog/?\)', r'<a href="/blog">\1</a>', text)
    text = re.sub(r'\[([^\]]+)\]\(https://souvenirpernikahan\.web\.id/?\)', r'<a href="/">\1</a>', text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)', r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', text)
    text = re.sub(r'\*\*\*([^*]+)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text

def parse_markdown_table(table_lines):
    if len(table_lines) < 2:
        return ""
    headers = [c.strip() for c in table_lines[0].strip().strip('|').split('|')]
    rows = []
    for line in table_lines[2:]:
        if not line.strip() or not line.strip().startswith('|'):
            continue
        cols = [c.strip() for c in line.strip().strip('|').split('|')]
        rows.append(cols)

    out = ['<div class="gs-article__table-wrapper">', '  <table class="gs-article__table">', '    <thead>', '      <tr>']
    for h in headers:
        out.append(f'        <th scope="col">{clean_inline(h)}</th>')
    out.extend(['      </tr>', '    </thead>', '    <tbody>'])
    for r in rows:
        out.append('      <tr>')
        for idx, col in enumerate(r):
            val = clean_inline(col)
            if idx == 0:
                out.append(f'        <td><strong>{val}</strong></td>')
            else:
                out.append(f'        <td>{val}</td>')
        out.append('      </tr>')
    out.extend(['    </tbody>', '  </table>', '</div>'])
    return '\n'.join(out)

def section_md_to_html(md_text):
    blocks = md_text.strip().split('\n\n')
    html_blocks = []
    i = 0
    while i < len(blocks):
        block = blocks[i].strip()
        if not block:
            i += 1
            continue

        if block.startswith('### '):
            h3_title = clean_inline(block[4:].strip())
            html_blocks.append(f'<h3>{h3_title}</h3>')
            i += 1
            continue

        if block.startswith('|') and '|' in block:
            table_lines = [l for l in block.splitlines() if l.strip().startswith('|')]
            html_blocks.append(parse_markdown_table(table_lines))
            i += 1
            continue

        if block.startswith('- ') or block.startswith('* '):
            items = []
            for l in block.splitlines():
                if l.strip().startswith(('- ', '* ')):
                    items.append(clean_inline(l.strip()[2:].strip()))
                elif items:
                    items[-1] += ' ' + clean_inline(l.strip())
            lis = ''.join([f'  <li>{it}</li>\n' for it in items])
            html_blocks.append(f'<ul>\n{lis}</ul>')
            i += 1
            continue

        if re.match(r'^\d+\.\s+', block):
            items = []
            for l in block.splitlines():
                m = re.match(r'^\d+\.\s+(.*)', l.strip())
                if m:
                    items.append(clean_inline(m.group(1).strip()))
                elif items:
                    items[-1] += ' ' + clean_inline(l.strip())
            lis = ''.join([f'  <li>{it}</li>\n' for it in items])
            html_blocks.append(f'<ol>\n{lis}</ol>')
            i += 1
            continue

        p_text = clean_inline(block.replace('\n', ' '))
        html_blocks.append(f'<p>{p_text}</p>')
        i += 1

    return '\n\n'.join(html_blocks)

cluster_articles_info = [
    {
        'slug': 'penyedia-souvenir-pernikahan',
        'title': 'Penyedia Souvenir Pernikahan Custom yang Elegan dan Berkesan',
        'meta_title': 'Penyedia Souvenir Pernikahan Custom Elegan — Souvenir Pernikahan',
        'badge': 'Panduan Utama',
        'category': 'Pilar Panduan',
        'read_time': '6 Menit',
        'date_published': '2026-11-09T08:30:00+07:00',
        'date_modified': '2026-11-09T08:30:00+07:00',
        'date_str': '9 November 2026',
        'word_count': 1650,
        'keywords': 'penyedia souvenir pernikahan, vendor souvenir pernikahan, souvenir pernikahan custom, souvenir wedding',
        'tags': ['#PenyediaSouvenir', '#SouvenirCustom', '#VendorPernikahan', '#SouvenirElegan'],
        'fig1_pos': 2, # after section index 2
        'fig2_pos': 6, # after section index 6
        'baca_juga_1': {
            'text': 'Ingin tahu ragam inspirasi cinderamata yang bermanfaat untuk tamu? Baca panduan',
            'link': '/blog/ide-souvenir-pernikahan-elegan',
            'title': 'ide souvenir pernikahan elegan dan fungsional'
        },
        'baca_juga_2': {
            'text': 'Sebelum memesan, pastikan Anda memahami cara memeriksa kredibilitas vendor di',
            'link': '/blog/cara-memilih-vendor-souvenir-pernikahan',
            'title': 'cara memilih vendor souvenir pernikahan terpercaya'
        }
    },
    {
        'slug': 'ide-souvenir-pernikahan-elegan',
        'title': 'Ide Souvenir Pernikahan Elegan, Fungsional, dan Berkesan',
        'meta_title': 'Ide Souvenir Pernikahan Elegan dan Bermanfaat — Souvenir Pernikahan',
        'badge': 'Inspirasi Produk',
        'category': 'Ide & Rekomendasi',
        'read_time': '5 Menit',
        'date_published': '2026-11-09T09:00:00+07:00',
        'date_modified': '2026-11-09T09:00:00+07:00',
        'date_str': '9 November 2026',
        'word_count': 1520,
        'keywords': 'ide souvenir pernikahan elegan, souvenir pernikahan fungsional, souvenir batik, souvenir tenun, souvenir eco-friendly',
        'tags': ['#IdeSouvenir', '#SouvenirBatik', '#SouvenirFungsional', '#SouvenirNusantara'],
        'fig1_pos': 1,
        'fig2_pos': 4,
        'baca_juga_1': {
            'text': 'Untuk panduan menyeluruh mulai dari kurasi hingga pengiriman, baca',
            'link': '/blog/penyedia-souvenir-pernikahan',
            'title': 'panduan penyedia souvenir pernikahan custom'
        },
        'baca_juga_2': {
            'text': 'Pelajari cara menghitung jumlah kebutuhan pesanan dan anggaran di',
            'link': '/blog/anggaran-jumlah-timeline-souvenir-pernikahan',
            'title': 'panduan anggaran, jumlah, dan timeline souvenir pernikahan'
        }
    },
    {
        'slug': 'cara-memilih-vendor-souvenir-pernikahan',
        'title': 'Cara Memilih Vendor Souvenir Pernikahan yang Terpercaya',
        'meta_title': 'Cara Memilih Vendor Souvenir Pernikahan Terpercaya — Souvenir Pernikahan',
        'badge': 'Tips Vendor',
        'category': 'Evaluasi & Vendor',
        'read_time': '5 Menit',
        'date_published': '2026-11-09T09:30:00+07:00',
        'date_modified': '2026-11-09T09:30:00+07:00',
        'date_str': '9 November 2026',
        'word_count': 1480,
        'keywords': 'cara memilih vendor souvenir pernikahan, vendor souvenir pernikahan, sampel produk souvenir, quality control souvenir',
        'tags': ['#PilihVendor', '#VendorTerpercaya', '#TipsPernikahan', '#QualityControl'],
        'fig1_pos': 2,
        'fig2_pos': 5,
        'baca_juga_1': {
            'text': 'Pelajari estimasi alokasi biaya dan jadwal produksi yang aman di',
            'link': '/blog/anggaran-jumlah-timeline-souvenir-pernikahan',
            'title': 'anggaran, jumlah dan timeline souvenir pernikahan'
        },
        'baca_juga_2': {
            'text': 'Cari inspirasi produk bernuansa Nusantara dan ramah lingkungan di',
            'link': '/blog/ide-souvenir-pernikahan-elegan',
            'title': 'ide souvenir pernikahan elegan dan bermanfaat'
        }
    },
    {
        'slug': 'anggaran-jumlah-timeline-souvenir-pernikahan',
        'title': 'Anggaran Souvenir Pernikahan: Hitung Jumlah dan Timeline Pesan',
        'meta_title': 'Anggaran, Jumlah dan Timeline Souvenir Pernikahan — Souvenir Pernikahan',
        'badge': 'Anggaran & Timeline',
        'category': 'Perencanaan Finansial',
        'read_time': '5 Menit',
        'date_published': '2026-11-09T10:00:00+07:00',
        'date_modified': '2026-11-09T10:00:00+07:00',
        'date_str': '9 November 2026',
        'word_count': 1580,
        'keywords': 'anggaran souvenir pernikahan, jumlah souvenir pernikahan, buffer stock souvenir, timeline pemesanan souvenir',
        'tags': ['#AnggaranSouvenir', '#HitungJumlah', '#TimelinePernikahan', '#BufferStock'],
        'fig1_pos': 1,
        'fig2_pos': 4,
        'baca_juga_1': {
            'text': 'Pastikan Anda telah mengevaluasi kredibilitas penyedia pilihan Anda di',
            'link': '/blog/cara-memilih-vendor-souvenir-pernikahan',
            'title': 'cara memilih vendor souvenir pernikahan terpercaya'
        },
        'baca_juga_2': {
            'text': 'Untuk tinjauan alur menyeluruh dari konsep hingga hari H, simak',
            'link': '/blog/penyedia-souvenir-pernikahan',
            'title': 'panduan penyedia souvenir pernikahan custom elegan'
        }
    }
]

# Parse raw articles into structured data
parsed_articles = []
for idx, raw in enumerate(raw_articles):
    meta = cluster_articles_info[idx].copy()
    
    # Description
    m_desc = re.search(r'\*\*Meta Description:\*\*\s*(.*?)\s*$', raw, re.M)
    meta['description'] = m_desc.group(1).strip() if m_desc else ""

    # Images
    imgs = []
    img_block = re.search(r'\*\*Images:\*\*\s*\n((?:- .*\n?)+)', raw)
    if img_block:
        for line in img_block.group(1).strip().splitlines():
            im_m = re.match(r'-\s*([\w\-.]+\.webp)\s*\|\s*Alt:\s*(.*)', line)
            if im_m:
                imgs.append({'src': '/assets/images/' + im_m.group(1).strip(), 'alt': im_m.group(2).strip()})
    meta['images'] = imgs

    # H1
    h1_m = re.search(r'^#\s+(.+)$', raw, re.M)
    meta['h1'] = h1_m.group(1).strip() if h1_m else meta['title']

    # Lead
    lead_m = re.search(r'^#\s+.+?\n\n(.*?)\n\n\*\*Ringkasan Inti\*\*', raw, re.DOTALL | re.M)
    meta['lead'] = lead_m.group(1).strip() if lead_m else ""

    # Ringkasan Inti
    rk_m = re.search(r'\*\*Ringkasan Inti\*\*\s*\n\n((?:- .*\n?)+)', raw)
    if rk_m:
        meta['ringkasan_inti'] = [l.strip().lstrip('- ').strip() for l in rk_m.group(1).strip().splitlines() if l.strip().startswith('- ')]
    else:
        meta['ringkasan_inti'] = []

    # TOC
    toc_m = re.search(r'### Daftar Isi\s*\n\n((?:\d+\..*\n?)+)', raw)
    toc_items = []
    if toc_m:
        for line in toc_m.group(1).strip().splitlines():
            t_m = re.match(r'\d+\.\s*\[([^\]]+)\]\(#([^\)]+)\)', line.strip())
            if t_m:
                toc_items.append({'title': t_m.group(1).strip(), 'anchor': t_m.group(2).strip()})
    meta['toc'] = toc_items

    # Sections
    content_start = raw.find('## ')
    content_raw = raw[content_start:]
    section_parts = re.split(r'\n(?=## )', content_raw)
    sections = []
    faqs = []

    for sp in section_parts:
        sp = sp.strip()
        if not sp: continue
        sec_h2_m = re.match(r'^##\s+(.+?)\s*$', sp.splitlines()[0])
        if not sec_h2_m: continue
        h2_title = sec_h2_m.group(1).strip()
        sec_body = '\n'.join(sp.splitlines()[1:]).strip()

        if h2_title.startswith('FAQ'):
            q_blocks = re.findall(r'### ([^\n\?]+\??)\n\n(.*?)(?=\n### |\Z)', sec_body, re.DOTALL)
            for q, a in q_blocks:
                faqs.append({'q': q.strip(), 'a': a.strip()})
            faq_anchor = [t['anchor'] for t in toc_items if 'faq' in t['anchor']][0] if any('faq' in t['anchor'] for t in toc_items) else 'faq'
            sections.append({
                'title': h2_title,
                'anchor': faq_anchor,
                'is_faq': True,
                'body_raw': sec_body
            })
            continue

        if h2_title.lower().startswith('kesimpulan'):
            ref_m = re.search(r'\*\*Referensi pendukung:\*\*\s*(.*)', sec_body, re.DOTALL)
            if ref_m:
                referensi_text = ref_m.group(1).strip()
                kesimpulan_text = sec_body[:sec_body.find('**Referensi pendukung:**')].strip()
            else:
                kesimpulan_text = sec_body
                referensi_text = ""
            kesimpulan_anchor = [t['anchor'] for t in toc_items if 'kesimpulan' in t['anchor']][0] if any('kesimpulan' in t['anchor'] for t in toc_items) else 'kesimpulan'
            sections.append({
                'title': h2_title,
                'anchor': kesimpulan_anchor,
                'is_kesimpulan': True,
                'body_raw': kesimpulan_text,
                'ref_raw': referensi_text
            })
            continue

        matching_anchor = ""
        for t in toc_items:
            if t['title'].lower() in h2_title.lower() or h2_title.lower() in t['title'].lower():
                matching_anchor = t['anchor']
                break
        if not matching_anchor:
            matching_anchor = re.sub(r'[^\w\-]', '', h2_title.lower().replace(' ', '-').replace('?', ''))

        sections.append({
            'title': h2_title,
            'anchor': matching_anchor,
            'is_faq': False,
            'is_kesimpulan': False,
            'body_raw': sec_body
        })

    meta['sections'] = sections
    meta['faqs'] = faqs
    parsed_articles.append(meta)

print("All metadata parsed. Generating HTML documents...")

# Shared LocalBusiness Schema
LOCAL_BUSINESS_SCHEMA = {
    "@type": ["Organization", "LocalBusiness"],
    "@id": "https://souvenirpernikahan.web.id/#organization",
    "name": "SEKATA",
    "url": "https://souvenirpernikahan.web.id/",
    "logo": {
        "@type": "ImageObject",
        "url": "https://souvenirpernikahan.web.id/assets/profile/logo-navbar-120.webp"
    },
    "image": "https://souvenirpernikahan.web.id/assets/images/hero-souvenir.webp",
    "description": "Penyedia souvenir pernikahan custom elegan, bernilai budaya, dan fungsional di Malang. Melayani pengiriman ke seluruh kota di Indonesia.",
    "telephone": "+6282131087971",
    "priceRange": "Rp 15.000 - Rp 500.000",
    "currenciesAccepted": "IDR",
    "paymentAccepted": "Cash, Bank Transfer, QRIS",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Jl. Band. Palmerah No.D3-35B, Cemorokandang, Kec. Kedungkandang",
        "addressLocality": "Kota Malang",
        "addressRegion": "Jawa Timur",
        "postalCode": "65138",
        "addressCountry": "ID"
    },
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": -7.9839,
        "longitude": 112.6214
    },
    "openingHoursSpecification": [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": "08:30",
            "closes": "18:00"
        }
    ],
    "areaServed": [
        {"@type": "City", "name": "Kota Malang"},
        {"@type": "City", "name": "Kota Batu"},
        {"@type": "AdministrativeArea", "name": "Kabupaten Malang"},
        {"@type": "City", "name": "Kota Surabaya"},
        {"@type": "AdministrativeArea", "name": "Kabupaten Sidoarjo"},
        {"@type": "State", "name": "Jawa Timur"},
        {"@type": "AdministrativeArea", "name": "DKI Jakarta"},
        {"@type": "City", "name": "Kota Bandung"},
        {"@type": "City", "name": "Kota Semarang"},
        {"@type": "City", "name": "Kota Yogyakarta"},
        {"@type": "Country", "name": "Indonesia"}
    ],
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+6282131087971",
        "contactType": "customer service",
        "areaServed": "ID",
        "availableLanguage": ["Indonesian"]
    },
    "sameAs": [
        "https://www.instagram.com/sakasouvenirmlg/"
    ],
    "hasMap": "https://www.google.com/maps?q=-7.9839,112.6214",
    "knowsAbout": [
        "Penyedia Souvenir Pernikahan",
        "Souvenir Pernikahan Custom",
        "Wedding Favors",
        "Cinderamata Acara",
        "Kemasan Souvenir",
        "Souvenir Fungsional",
        "Souvenir Khas Indonesia"
    ],
    "alternateName": [
        "SEKATA Souvenir Pernikahan",
        "Sekata"
    ]
}

WEBSITE_SCHEMA = {
    "@type": "WebSite",
    "@id": "https://souvenirpernikahan.web.id/#website",
    "url": "https://souvenirpernikahan.web.id/",
    "name": "SEKATA",
    "description": "Penyedia souvenir pernikahan elegan, cinderamata custom berkualitas, dan kemasan eksklusif di Malang dan seluruh Indonesia.",
    "publisher": {
        "@id": "https://souvenirpernikahan.web.id/#organization"
    },
    "inLanguage": "id-ID",
    "potentialAction": {
        "@type": "SearchAction",
        "target": "https://souvenirpernikahan.web.id/blog?q={search_term_string}",
        "query-input": "required name=search_term_string"
    },
    "alternateName": [
        "SEKATA Souvenir Pernikahan",
        "Sekata"
    ]
}

def build_article_html(art, all_arts):
    slug = art['slug']
    canonical_url = f"https://souvenirpernikahan.web.id/blog/{slug}"
    cover_img = art['images'][0] if art['images'] else {'src': '/assets/images/hero-souvenir.webp', 'alt': art['title']}
    fig1_img = art['images'][1] if len(art['images']) > 1 else None
    fig2_img = art['images'][2] if len(art['images']) > 2 else None

    # Sibling articles for related grid
    sibling_arts = [a for a in all_arts if a['slug'] != slug][:3]

    # TOC HTML
    toc_lis = []
    for item in art['toc']:
        toc_lis.append(f'                <li><a href="#{item["anchor"]}">{item["title"]}</a></li>')
    toc_html = '\n'.join(toc_lis)

    # Ringkasan Inti HTML
    rk_lis = []
    for p in art['ringkasan_inti']:
        rk_lis.append(f'                <li>{clean_inline(p)}</li>')
    rk_html = '\n'.join(rk_lis)

    # Body sections rendering
    body_html_parts = []
    
    # 1. Lead paragraph
    body_html_parts.append(f'            <!-- Lead Paragraph Pembuka Konteks -->\n            <p class="gs-article__lead">\n              {clean_inline(art["lead"])}\n            </p>')

    # 2. Key Takeaway Box
    body_html_parts.append(f'''            <!-- Key Takeaway Box -->
            <aside class="gs-article__key-takeaway" aria-labelledby="takeaway-{slug}">
              <div data-gs-animate class="gs-article__key-takeaway-head" id="takeaway-{slug}">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    clip-rule="evenodd" />
                </svg>
                Ringkasan Inti Artikel
              </div>
              <ul style="margin:0;padding-left:1.25rem;">
{rk_html}
              </ul>
            </aside>''')

    # Content sections
    non_faq_sections = [s for s in art['sections'] if not s.get('is_faq') and not s.get('is_kesimpulan') and s.get('anchor') != 'daftar-isi' and 'daftar isi' not in s.get('title', '').lower()]
    
    for s_idx, sec in enumerate(non_faq_sections):
        sec_title = clean_inline(sec['title'])
        sec_anchor = sec['anchor']
        sec_html = section_md_to_html(sec['body_raw'])

        body_html_parts.append(f'''            <h2 id="{sec_anchor}">{sec_title}</h2>\n{sec_html}''')

        # Insert Figure 1
        if s_idx == art['fig1_pos'] and fig1_img:
            body_html_parts.append(f'''            <!-- In-Article Figure 1 -->
            <figure class="gs-article__figure">
              <img src="{fig1_img['src']}"
                alt="{fig1_img['alt']}" width="900" height="500"
                loading="lazy" />
              <figcaption>{fig1_img['alt']}.</figcaption>
            </figure>''')

        # Insert Baca Juga 1
        if s_idx == 1 and 'baca_juga_1' in art:
            bj = art['baca_juga_1']
            body_html_parts.append(f'''            <!-- Baca Juga Box 1 -->
            <div class="gs-article__baca-juga">
              <div class="gs-article__baca-juga-icon" aria-hidden="true">
                <svg viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z"
                    clip-rule="evenodd" />
                </svg>
              </div>
              <div class="gs-article__baca-juga-content">
                <strong>Baca Juga:</strong> {bj['text']} <a href="{bj['link']}">{bj['title']}</a>.
              </div>
            </div>''')

        # Insert Figure 2
        if s_idx == art['fig2_pos'] and fig2_img:
            body_html_parts.append(f'''            <!-- In-Article Figure 2 -->
            <figure class="gs-article__figure">
              <img src="{fig2_img['src']}"
                alt="{fig2_img['alt']}" width="900" height="500"
                loading="lazy" />
              <figcaption>{fig2_img['alt']}.</figcaption>
            </figure>''')

        # Insert Baca Juga 2
        if s_idx == min(len(non_faq_sections)-1, 5) and 'baca_juga_2' in art:
            bj = art['baca_juga_2']
            body_html_parts.append(f'''            <!-- Baca Juga Box 2 -->
            <div class="gs-article__baca-juga">
              <div class="gs-article__baca-juga-icon" aria-hidden="true">
                <svg viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z"
                    clip-rule="evenodd" />
                </svg>
              </div>
              <div class="gs-article__baca-juga-content">
                <strong>Baca Juga:</strong> {bj['text']} <a href="{bj['link']}">{bj['title']}</a>.
              </div>
            </div>''')

    # CTA Banner before FAQ
    body_html_parts.append(f'''            <!-- In-Article CTA Banner -->
            <section class="gs-article__cta" aria-labelledby="cta-heading-{slug}">
              <h3 id="cta-heading-{slug}">Konsultasikan Kebutuhan Souvenir Anda Bersama Sekata</h3>
              <p>
                Dapatkan rekomendasi kurasi cinderamata yang elegan, preview mockup digital gratis, serta penyesuaian anggaran yang transparan untuk pernikahan Anda.
              </p>
              <a href="https://wa.me/6282131087971?text=Halo%20Sekata%2C%20saya%20ingin%20konsultasi%20souvenir%20pernikahan."
                class="gs-button gs-button--whatsapp" target="_blank" rel="noopener noreferrer">
                <svg viewBox="0 0 24 24" fill="currentColor" style="width:18px;height:18px;" aria-hidden="true">
                  <path
                    d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
                </svg>
                Konsultasi WhatsApp Sekarang
              </a>
            </section>''')

    # FAQ Section
    faq_sec = [s for s in art['sections'] if s.get('is_faq')]
    faq_anchor = faq_sec[0]['anchor'] if faq_sec else f"faq-{slug}"
    faq_items_html = []
    for f_idx, item in enumerate(art['faqs']):
        q_text = clean_inline(item['q'])
        a_text = clean_inline(item['a'].replace('\n', ' '))
        faq_items_html.append(f'''              <div class="gs-article__faq-item">
                <button type="button" class="gs-article__faq-question" aria-expanded="false" aria-controls="faq-{slug[:4]}-{f_idx+1}">
                  {q_text}
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" aria-hidden="true">
                    <path d="M4 6l4 4 4-4" />
                  </svg>
                </button>
                <div class="gs-article__faq-answer" id="faq-{slug[:4]}-{f_idx+1}">
                  {a_text}
                </div>
              </div>''')
    
    body_html_parts.append(f'''            <!-- FAQ Section -->
            <section class="gs-article__faq-wrap" id="{faq_anchor}" aria-labelledby="faq-title-{slug}">
              <h2 class="gs-article__faq-title" id="faq-title-{slug}">Pertanyaan Umum (FAQ)</h2>
{chr(10).join(faq_items_html)}
            </section>''')

    # Kesimpulan Section
    kesimpulan_sec = [s for s in art['sections'] if s.get('is_kesimpulan')]
    if kesimpulan_sec:
        k_sec = kesimpulan_sec[0]
        k_body = section_md_to_html(k_sec['body_raw'])
        k_anchor = k_sec['anchor']
        ref_html = ""
        if k_sec.get('ref_raw'):
            ref_clean = clean_inline(k_sec['ref_raw'])
            ref_html = f'''            <div class="gs-article__callout" style="margin-top:1.5rem;font-size:0.88rem;background:var(--gs-green-50);border-left:3px solid var(--gs-green-700);padding:1rem 1.25rem;">
              <strong>Referensi Pendukung:</strong> {ref_clean}
            </div>'''
        body_html_parts.append(f'''            <h2 id="{k_anchor}">{clean_inline(k_sec['title'])}</h2>\n{k_body}\n{ref_html}''')

    # Author Bio Box
    body_html_parts.append(f'''            <!-- Author Bio -->
            <div class="gs-article__author-box" data-nosnippet>
              <a href="/penulis" class="gs-article__author-avatar" title="Lihat Profil Yudi Abraham">
                <img src="/assets/images/yudi-abraham.jpg" alt="Yudi Abraham" width="68" height="68" loading="lazy" data-nosnippet/>
              </a>
              <div class="gs-article__author-info">
                <h4><a href="/penulis" class="gs-article__author-heading-link" title="Lihat Profil Penulis">Yudi Abraham</a></h4>
                <span class="gs-article__author-role">Konsultan &amp; Kurator Souvenir Pernikahan</span>
                <p>
                  Praktisi dan konsultan cinderamata pernikahan di Sekata dengan pengalaman mendampingi calon pengantin merancang souvenir yang elegan, berkesan, dan efisien secara anggaran.
                </p>
                <a href="/penulis" class="gs-article__author-more-link" title="Lihat profil dan karya tulisan Yudi Abraham">
                  Lihat Profil Lengkap &rarr;
                </a>
              </div>
            </div>''')

    # Tags & Social Share
    tag_elements = ''.join([f'\n                <a href="/blog" class="gs-article__tag">{t}</a>' for t in art['tags']])
    share_url_encoded = re.sub(r'[^a-zA-Z0-9]', lambda m: f'%{ord(m.group(0)):02X}', canonical_url)
    share_title_encoded = re.sub(r'[^a-zA-Z0-9]', lambda m: f'%{ord(m.group(0)):02X}', art['title'])

    body_html_parts.append(f'''            <!-- Tags & Social Share -->
            <div class="gs-article__tags-share">
              <div class="gs-article__tags">
                <span style="font-size:0.8rem;color:var(--gs-muted);font-weight:600;">Tags:</span>{tag_elements}
              </div>
              <div class="gs-article__share">
                <span class="gs-article__share-label">Bagikan:</span>
                <a href="https://api.whatsapp.com/send?text={share_title_encoded}%20{share_url_encoded}"
                  target="_blank" rel="noopener noreferrer" class="gs-article__share-btn gs-article__share-btn--wa"
                  title="Bagikan ke WhatsApp" aria-label="Bagikan ke WhatsApp">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path
                      d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
                  </svg>
                </a>
                <button type="button" class="gs-article__share-btn gs-article__share-btn--copy"
                  title="Salin Tautan Artikel" aria-label="Salin tautan artikel">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round">
                    <path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71" />
                    <path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71" />
                  </svg>
                </button>
              </div>
            </div>''')

    # Product Recommendation Card
    body_html_parts.append(f'''            <!-- Product Recommendation Card -->
            <div class="gs-article__product-rec">
              <div class="gs-article__product-rec-img">
                <img src="/assets/images/hero-souvenir.webp"
                  alt="Koleksi souvenir pernikahan elegan Sekata dengan kemasan eksklusif" width="300"
                  height="300" loading="lazy" />
              </div>
              <div class="gs-article__product-rec-info">
                <span class="badge">Katalog Rekomendasi</span>
                <h4>Koleksi Souvenir Pernikahan Custom Sekata</h4>
                <p>Jelajahi Essential dan Signature Collection kami dengan pilihan bahan berkualitas, gratis mockup inisial nama, dan garansi kirim aman seluruh Indonesia.</p>
                <div style="font-size:0.85rem;color:var(--gs-green-800);font-weight:600;">Minimum Pesanan Fleksibel &amp; Konsultasi WhatsApp Gratis</div>
              </div>
              <div class="gs-article__product-rec-action">
                <a href="/paket" class="gs-button gs-button--primary gs-button--sm">Lihat Koleksi</a>
              </div>
            </div>''')

    full_body_rendered = '\n\n'.join(body_html_parts)

    # Related articles HTML (3 siblings)
    related_cards_html = []
    for sb in sibling_arts:
        sb_img = sb['images'][0] if sb['images'] else {'src': '/assets/images/hero-souvenir.webp', 'alt': sb['title']}
        related_cards_html.append(f'''              <article data-gs-animate class="gs-blog-card">
                <div class="gs-blog-card__image">
                  <img src="{sb_img['src']}" alt="{sb['title']}"
                    loading="lazy" />
                </div>
                <div class="gs-blog-card__body">
                  <div class="gs-blog-card__meta">
                    <span class="gs-blog-card__category">{sb['category']}</span>
                    <span aria-hidden="true">&bull;</span>
                    <time datetime="{sb['date_published'][:10]}">{sb['date_str']}</time>
                  </div>
                  <h3 class="gs-blog-card__title">
                    <a href="/blog/{sb['slug']}">{sb['title']}</a>
                  </h3>
                  <p class="gs-blog-card__excerpt">{sb['description'][:110]}...</p>
                  <a href="/blog/{sb['slug']}" class="gs-blog-card__link">
                    Baca Selengkapnya &rarr;
                  </a>
                </div>
              </article>''')
    related_section_html = '\n'.join(related_cards_html)

    # JSON-LD Graph construction
    schema_graph = [
        LOCAL_BUSINESS_SCHEMA,
        WEBSITE_SCHEMA,
        {
            "@type": "BlogPosting",
            "@id": f"{canonical_url}#article",
            "isPartOf": {
                "@id": "https://souvenirpernikahan.web.id/#website"
            },
            "headline": art['title'],
            "description": art['description'],
            "image": {
                "@type": "ImageObject",
                "url": f"https://souvenirpernikahan.web.id{cover_img['src']}",
                "width": 1200,
                "height": 630
            },
            "datePublished": art['date_published'],
            "dateModified": art['date_modified'],
            "inLanguage": "id-ID",
            "mainEntityOfPage": canonical_url,
            "author": {
                "@type": "Person",
                "@id": "https://souvenirpernikahan.web.id/penulis#person",
                "name": "Yudi Abraham",
                "url": "https://souvenirpernikahan.web.id/penulis",
                "jobTitle": "Konsultan & Kurator Souvenir Pernikahan",
                "description": "Praktisi dan konsultan cinderamata pernikahan dengan pengalaman membantu calon pengantin merancang souvenir elegan, berkesan, dan efisien."
            },
            "publisher": {
                "@id": "https://souvenirpernikahan.web.id/#organization"
            },
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": [
                    ".gs-article__title",
                    ".gs-article__lead",
                    ".gs-article__key-takeaway p"
                ]
            },
            "articleSection": art['category'],
            "keywords": art['keywords'],
            "wordCount": art['word_count'],
            "timeRequired": f"PT{art['read_time'][0]}M",
            "isAccessibleForFree": True,
            "license": "https://souvenirpernikahan.web.id/kebijakan-privasi",
            "about": [
                {
                    "@type": "Thing",
                    "name": "Souvenir Pernikahan"
                },
                {
                    "@type": "Thing",
                    "name": "Wedding Favor",
                    "sameAs": "https://en.wikipedia.org/wiki/Wedding_favor"
                }
            ],
            "mentions": [
                {
                    "@type": "Place",
                    "name": "Kota Malang",
                    "sameAs": "https://id.wikipedia.org/wiki/Kota_Malang"
                },
                {
                    "@type": "Thing",
                    "name": "SEKATA Souvenir Pernikahan"
                }
            ],
            "primaryImageOfPage": {
                "@type": "ImageObject",
                "url": f"https://souvenirpernikahan.web.id{cover_img['src']}",
                "width": 1200,
                "height": 630
            }
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{canonical_url}#breadcrumb",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Beranda",
                    "item": "https://souvenirpernikahan.web.id/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Blog",
                    "item": "https://souvenirpernikahan.web.id/blog/"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": art['title'],
                    "item": canonical_url
                }
            ]
        },
        {
            "@type": "ItemList",
            "@id": f"{canonical_url}#itemlist",
            "name": f"Poin Pembahasan: {art['title']}",
            "numberOfItems": len(art['toc']),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": t_idx + 1,
                    "name": item['title']
                } for t_idx, item in enumerate(art['toc'])
            ]
        }
    ]

    # Add FAQPage schema if faqs exist
    if art['faqs']:
        schema_graph.append({
            "@type": "FAQPage",
            "@id": f"{canonical_url}#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item['q'],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item['a']
                    }
                } for item in art['faqs']
            ]
        })

    json_ld_string = json.dumps({"@context": "https://schema.org", "@graph": schema_graph}, ensure_ascii=False, indent=2)

    # Full HTML assembly
    html_content = f'''<!DOCTYPE html>
<html lang="id">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />

  <!-- Preload Critical CSS -->
  <link rel="preload" href="/assets/css/style.min.css?v=16" as="style" />

  <title>{art['meta_title']}</title>
  <meta name="description"
    content="{art['description']}" />
  <meta name="author" content="Yudi Abraham" />
  <meta name="language" content="Indonesian" />
  <meta name="theme-color" content="#762b16" />
  <meta name="format-detection" content="telephone=no" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />

  <!-- Favicon & App Icons -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/profile/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/profile/favicon-16x16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/profile/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />

  <!-- Canonical & Alternate Hreflang -->
  <link rel="canonical" href="{canonical_url}" />
  <link rel="alternate" hreflang="id-ID"
    href="{canonical_url}" />
  <link rel="alternate" hreflang="x-default"
    href="{canonical_url}" />

  <!-- GEO & Local Engine Optimization (GEO) -->
  <meta name="geo.region" content="ID-JI" />
  <meta name="geo.placename" content="Kota Malang, Jawa Timur, Indonesia" />
  <meta name="geo.position" content="-7.9839;112.6214" />
  <meta name="ICBM" content="-7.9839, 112.6214" />
  <meta name="geo.country" content="ID" />

  <!-- Open Graph / Facebook / WhatsApp -->
  <meta property="og:site_name" content="SEKATA" />
  <meta property="og:type" content="article" />
  <meta property="og:locale" content="id_ID" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:title"
    content="{art['meta_title']}" />
  <meta property="og:description"
    content="{art['description']}" />
  <meta property="og:image" content="https://souvenirpernikahan.web.id{cover_img['src']}" />
  <meta property="og:image:secure_url"
    content="https://souvenirpernikahan.web.id{cover_img['src']}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{cover_img['alt']}" />
  <meta property="og:image:type" content="image/webp" />
  <meta property="article:published_time" content="{art['date_published']}" />
  <meta property="article:modified_time" content="{art['date_modified']}" />
  <meta property="article:author" content="Yudi Abraham" />
  <meta property="article:section" content="{art['category']}" />
  <meta property="article:tag" content="Souvenir Pernikahan" />
  <meta property="article:tag" content="Wedding Favor" />
  <meta property="article:tag" content="Souvenir Custom" />
  <meta property="article:tag" content="Souvenir Elegan" />
  <meta property="article:tag" content="Souvenir Pernikahan Malang" />

  <!-- Twitter / X Cards -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:url" content="{canonical_url}" />
  <meta name="twitter:title"
    content="{art['meta_title']}" />
  <meta name="twitter:description"
    content="{art['description']}" />
  <meta name="twitter:image" content="https://souvenirpernikahan.web.id{cover_img['src']}" />
  <meta name="twitter:image:alt" content="{cover_img['alt']}" />

  <!-- Fonts (Non-blocking) -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" as="style"
    href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" />
  <link rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap"
    media="print" onload="this.media='all'" />
  <noscript>
    <link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" />
  </noscript>

  <!-- CSS -->
  <link rel="stylesheet" href="/assets/css/style.min.css?v=16" />

  <!-- Structured Data JSON-LD (BlogPosting, BreadcrumbList, ItemList, FAQPage) -->
  <script type="application/ld+json">
{json_ld_string}
</script>
  <style>
    .gs-article__header {{
      position: static !important;
      top: auto !important;
      z-index: auto !important;
      width: auto !important;
    }}
  </style>
</head>

<body>

  <!-- NAVBAR -->
  <header>
    <nav class="gs-navbar" aria-label="Navigasi utama">
      <div class="gs-container">
        <div class="gs-navbar__inner">
          <a href="/" class="gs-navbar__logo" aria-label="Souvenir Pernikahan — Beranda">
            <img src="/assets/profile/logo-navbar-120.webp" alt="Logo SEKATA, souvenir pernikahan" class="gs-navbar__logo-img"
              width="60" height="60" decoding="async" />
            <span class="gs-navbar__brand-text">Souvenir Pernikahan</span>
          </a>
          <div class="gs-navbar__nav" role="menubar">
            <a href="/" class="gs-navbar__link" role="menuitem">Beranda</a>
            <a href="/tentang" class="gs-navbar__link" role="menuitem">Tentang</a>
            <!-- Dropdown Katalog -->
            <div class="gs-dropdown">
              <button class="gs-dropdown__toggle" aria-haspopup="true" aria-expanded="false"
                aria-controls="gs-dropdown-paket" id="gs-dropdown-paket-btn">
                Katalog
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round" aria-hidden="true">
                  <path d="M4 6l4 4 4-4" />
                </svg>
              </button>
              <div class="gs-dropdown__menu" id="gs-dropdown-paket" aria-labelledby="gs-dropdown-paket-btn">
                <a href="/paket" class="gs-dropdown__item">
                  <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path
                      d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM14 11a1 1 0 011 1v1h1a1 1 0 110 2h-1v1a1 1 0 11-2 0v-1h-1a1 1 0 110-2h1v-1a1 1 0 011-1z" />
                  </svg>
                  Katalog Souvenir
                </a>
                <div class="gs-dropdown__divider" role="separator"></div>
                <a href="/paket/souvenir-tradisional" class="gs-dropdown__item">
                  <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd"
                      d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
                      clip-rule="evenodd" />
                  </svg>
                  Essential Collection
                </a>
                <a href="/paket/souvenir-modern" class="gs-dropdown__item">
                  <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd"
                      d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2h-3a1 1 0 01-1-1v-2a1 1 0 00-1-1H9a1 1 0 00-1 1v2a1 1 0 01-1 1H4a1 1 0 110-2V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z"
                      clip-rule="evenodd" />
                  </svg>
                  Signature Collection
                </a>
              </div>
            </div>
            <a href="/portofolio" class="gs-navbar__link" role="menuitem">Portofolio</a>
            <a href="/blog" class="gs-navbar__link active" role="menuitem">Blog</a>
          </div>
          <div class="gs-navbar__cta">
            <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi%20souvenir%20pernikahan."
              class="gs-button gs-button--whatsapp gs-button--sm" target="_blank" rel="noopener noreferrer"
              aria-label="Konsultasi via WhatsApp">Konsultasi</a>
          </div>
          <button class="gs-navbar__hamburger" id="gs-hamburger" aria-label="Buka menu navigasi" aria-expanded="false"
            aria-controls="gs-mobile-menu">
            <span class="gs-navbar__hamburger-line"></span><span class="gs-navbar__hamburger-line"></span><span
              class="gs-navbar__hamburger-line"></span>
          </button>
        </div>
        <div class="gs-navbar__mobile-menu" id="gs-mobile-menu" role="menu">
          <a href="/" class="gs-navbar__mobile-link" role="menuitem">Beranda</a>
          <a href="/tentang" class="gs-navbar__mobile-link" role="menuitem">Tentang</a>
          <button class="gs-navbar__mobile-submenu-toggle" aria-expanded="false" aria-controls="gs-mobile-paket">
            Katalog
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" aria-hidden="true">
              <path d="M4 6l4 4 4-4" />
            </svg>
          </button>
          <div class="gs-navbar__mobile-submenu" id="gs-mobile-paket">
            <a href="/paket" class="gs-navbar__mobile-link">Katalog Souvenir</a>
            <a href="/paket/souvenir-tradisional" class="gs-navbar__mobile-link">Essential Collection</a>
            <a href="/paket/souvenir-modern" class="gs-navbar__mobile-link">Signature Collection</a>
          </div>
          <a href="/portofolio" class="gs-navbar__mobile-link" role="menuitem">Portofolio</a>
          <a href="/blog" class="gs-navbar__mobile-link" role="menuitem">Blog</a>
          <div class="gs-navbar__mobile-cta">
            <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi."
              class="gs-button gs-button--whatsapp" target="_blank" rel="noopener noreferrer"
              style="width:100%;justify-content:center;">Konsultasi WhatsApp</a>
          </div>
        </div>
      </div>
    </nav>
  </header>

  <main id="main-content">
    <section class="gs-section" style="padding-top: clamp(2rem, 4vw, 3.5rem);">
      <div class="gs-container">

        <article class="gs-article">

          <!-- Breadcrumb -->
          <nav aria-label="Breadcrumb">
            <ol class="gs-breadcrumb">
              <li><a href="/" class="gs-breadcrumb__item">Beranda</a></li>
              <li><a href="/blog" class="gs-breadcrumb__item">Blog</a></li>
              <li class="gs-breadcrumb__item gs-breadcrumb__item--active" aria-current="page">{art['title']}</li>
            </ol>
          </nav>

          <!-- Header -->
          <header class="gs-article__header" data-gs-animate>
            <div class="gs-article__badge-wrap">
              <span class="gs-article__category">{art['category']}</span>
              <span class="gs-badge">{art['badge']}</span>
            </div>
            <h1 class="gs-article__title">{art['h1']}</h1>
            <div class="gs-article__meta">
              <span class="gs-article__meta-item">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                    clip-rule="evenodd" />
                </svg>
                <strong>Penulis:</strong> <a href="/penulis" class="gs-article__author-link" title="Lihat profil Yudi Abraham">Yudi Abraham</a>
              </span>
              <span class="gs-article__meta-item">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                    clip-rule="evenodd" />
                </svg>
                <strong>Publikasi:</strong> <time datetime="{art['date_published'][:10]}">{art['date_str']}</time>
              </span>
              <span class="gs-article__meta-item">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                    clip-rule="evenodd" />
                </svg>
                <strong>Pembaruan:</strong> <time datetime="{art['date_modified'][:10]}">{art['date_str']}</time>
              </span>
              <span class="gs-article__meta-item">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                    clip-rule="evenodd" />
                </svg>
                <strong>Waktu Baca:</strong> {art['read_time']}
              </span>
            </div>
          </header>

          <!-- Cover Image (Tepat Setelah Header) -->
          <div class="gs-article__cover" data-gs-animate="slide">
            <img src="{cover_img['src']}"
              alt="{cover_img['alt']}" width="1200" height="630"
              loading="eager" />
            <div class="gs-article__caption">
              {cover_img['alt']} — Koleksi resmi Sekata Souvenir Pernikahan.
            </div>
          </div>

          <!-- TOC (Tepat Setelah Gambar Utama) -->
          <nav data-gs-animate class="gs-article__toc" aria-label="Daftar Isi Artikel">
            <button type="button" class="gs-article__toc-toggle" aria-expanded="true" aria-controls="toc-list-body-{slug}">
              <span class="gs-article__toc-label">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1z"
                    clip-rule="evenodd" />
                </svg>
                Daftar Isi Artikel
              </span>
              <svg class="gs-article__toc-chevron" viewBox="0 0 16 16" fill="none" stroke="currentColor"
                stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M4 6l4 4 4-4" />
              </svg>
            </button>
            <div class="gs-article__toc-body" id="toc-list-body-{slug}">
              <ol class="gs-article__toc-list">
{toc_html}
              </ol>
            </div>
          </nav>

          <!-- Body (Dilanjutkan Setelah Daftar Isi) -->
          <div class="gs-article__body">

{full_body_rendered}

          </div>

          <!-- Related Articles Grid -->
          <section class="gs-article__related" aria-labelledby="related-title-{slug}">
            <h2 class="gs-article__related-title" id="related-title-{slug}">Artikel Panduan Terkait</h2>
            <div class="gs-article__related-grid">

{related_section_html}

            </div>
          </section>

        </article>

      </div>
    </section>
  </main>

  <!-- FOOTER -->
  <footer class="gs-footer">
    <div class="gs-container">
      <div class="gs-footer__grid">
        <!-- Brand -->
        <div>
          <a href="/" class="gs-footer__brand-name" aria-label="SEKATA — Beranda">
            <div class="gs-footer__brand-logo" aria-hidden="true"><img src="/assets/profile/logo-footer-108.webp"
                alt="Logo SEKATA" width="54" height="54" loading="lazy" decoding="async" /></div>
            <span>SEKATA</span>
          </a>
          <p class="gs-footer__desc">
            Penyedia souvenir pernikahan elegan, cinderamata custom berkesan, dan kemasan berkelas di Malang untuk pengiriman ke seluruh Indonesia. Dibuat dengan perhatian penuh terhadap mutu dan detail.
          </p>
          <a href="https://maps.app.goo.gl/fQQ1reAUBefTYWb27" class="gs-footer__location-item" target="_blank"
            rel="noopener noreferrer" aria-label="Lihat lokasi Souvenir Pernikahan di Google Maps">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path
                d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" />
            </svg>
            <span>Jl. Band. Palmerah No.D3-35B, Cemorokandang, Kec. Kedungkandang, Kota Malang, Jawa Timur 65138, Indonesia</span>
          </a>
        </div>

        <!-- Halaman -->
        <div>
          <p class="gs-footer__heading">Halaman</p>
          <ul class="gs-footer__links">
            <li><a href="/" class="gs-footer__link">Beranda</a></li>
            <li><a href="/tentang" class="gs-footer__link">Tentang Kami</a></li>
            <li><a href="/portofolio" class="gs-footer__link">Portofolio</a></li>
            <li><a href="/blog" class="gs-footer__link">Blog</a></li>
            <li><a href="/penulis" class="gs-footer__link">Penulis</a></li>
          </ul>
        </div>

        <!-- Kategori Paket -->
        <div>
          <p class="gs-footer__heading">Koleksi Souvenir</p>
          <ul class="gs-footer__links">
            <li><a href="/paket" class="gs-footer__link">Semua Souvenir</a></li>
            <li><a href="/paket/souvenir-tradisional" class="gs-footer__link">Souvenir Tradisional</a></li>
            <li><a href="/paket/souvenir-modern" class="gs-footer__link">Souvenir Modern</a></li>
          </ul>
        </div>

        <!-- Kontak -->
        <div>
          <p class="gs-footer__heading">Kontak</p>
          <div class="gs-footer__contact-list">
            <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi."
              class="gs-footer__contact-link" target="_blank" rel="noopener noreferrer"
              aria-label="WhatsApp Souvenir Pernikahan">
              <span class="gs-footer__contact-icon">
                <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path
                    d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
                </svg>
              </span>
              <span>+62 821-3108-7971</span>
            </a>
            <a href="https://www.instagram.com/sakasouvenirmlg/" class="gs-footer__contact-link" target="_blank"
              rel="noopener noreferrer" aria-label="Instagram @sakasouvenirmlg">
              <span class="gs-footer__contact-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round" aria-hidden="true">
                  <rect x="2" y="2" width="20" height="20" rx="5" ry="5" />
                  <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" />
                  <line x1="17.5" y1="6.5" x2="17.51" y2="6.5" />
                </svg>
              </span>
              <span>@sakasouvenirmlg</span>
            </a>
          </div>
        </div>
      </div>
      <div class="gs-footer__bottom">
        <p>&copy; <span id="gs-year"></span> Souvenir Pernikahan. Semua hak dilindungi.</p>
        <div class="gs-footer__bottom-links">
          <a href="/kebijakan-privasi" class="gs-footer__bottom-link">Kebijakan Privasi</a>
        </div>
      </div>
    </div>
  </footer>

  <div class="gs-whatsapp-float" aria-label="Hubungi via WhatsApp">
    <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi%20souvenir%20pernikahan."
      class="gs-whatsapp-float__btn" target="_blank" rel="noopener noreferrer" aria-label="Chat via WhatsApp">
      <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
        <path
          d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
      </svg>
    </a>
  </div>

  <!-- Back to Top Button -->
  <button type="button" class="gs-back-to-top" id="gs-back-to-top" aria-label="Kembali ke atas">
    <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
    </svg>
  </button>

  <script defer src="/assets/js/main.min.js?v=8"></script>
</body>

</html>'''

    return html_content

# Generate and write all 4 files
for art in parsed_articles:
    target_file = os.path.join(BLOG_DIR, f"{art['slug']}.html")
    content = build_article_html(art, parsed_articles)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated: {target_file} ({len(content)} bytes)")

print("All 4 article files written successfully!")

