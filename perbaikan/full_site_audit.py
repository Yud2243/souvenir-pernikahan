import os, re, json

BASE = r'C:\Untuk_PKL\Souvenirkeuda'

PAGES = [
    'index.html',
    'tentang.html',
    'paket.html',
    'portofolio.html',
    'detail-portofolio.html',
    'penulis.html',
    'blog.html',
    'kebijakan-privasi.html',
    'paket/souvenir-tradisional.html',
    'paket/souvenir-modern.html',
    'blog/panduan-memilih-souvenir-pernikahan.html',
    'blog/souvenir-pernikahan-unik-bermanfaat.html',
    'blog/souvenir-pernikahan-tradisional-khas-indonesia.html',
    'blog/souvenir-pernikahan-modern-dan-minimalis.html',
    'blog/souvenir-pernikahan-ramah-lingkungan.html',
    'blog/souvenir-pernikahan-handmade-dari-pengrajin-lokal.html',
    'blog/souvenir-pernikahan-elegan-untuk-acara-intim.html',
    'blog/souvenir-pernikahan-premium-untuk-tamu-vip.html',
    'blog/kipas-batik-untuk-souvenir-pernikahan.html',
    'blog/pouch-batik-dan-dompet-tenun-untuk-souvenir.html',
    'blog/panduan-harga-souvenir-pernikahan-berdasarkan-jenis-produk.html',
    'blog/ide-souvenir-pernikahan-budget-rp5-000-per-pcs.html',
    'blog/rekomendasi-souvenir-pernikahan-budget-rp10-000.html',
    'blog/cara-menghitung-jumlah-souvenir.html',
    'blog/personalisasi-nama-dan-tanggal-souvenir.html',
    'blog/ide-kemasan-souvenir-pernikahan.html',
    'blog/checklist-pemesanan-souvenir-pernikahan.html',
    'blog/panduan-souvenir-perusahaan.html'
]

results = []

for rel_path in PAGES:
    abs_path = os.path.join(BASE, rel_path.replace('/', os.sep))
    if not os.path.exists(abs_path):
        results.append({'file': rel_path, 'status': 'NOT_FOUND'})
        continue

    with open(abs_path, encoding='utf-8') as f:
        c = f.read()

    # 1. SEO basic
    title_m = re.search(r'<title>(.*?)</title>', c, re.DOTALL)
    title = title_m.group(1).strip() if title_m else None
    
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', c, re.DOTALL)
    if not desc_m:
        desc_m = re.search(r'content="([^"]*)"\s+name="description"', c, re.DOTALL)
    desc = desc_m.group(1).strip() if desc_m else None

    canon_m = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', c)
    canon = canon_m.group(1) if canon_m else None

    h1_count = len(re.findall(r'<h1[^>]*>', c))

    # 2. OpenGraph
    og_title = re.search(r'<meta\s+property="og:title"\s+content="([^"]*)"', c)
    og_desc = re.search(r'<meta\s+property="og:description"\s+content="([^"]*)"', c)
    og_img = re.search(r'<meta\s+property="og:image"\s+content="([^"]*)"', c)
    og_type = re.search(r'<meta\s+property="og:type"\s+content="([^"]*)"', c)
    og_tags = re.findall(r'<meta\s+property="article:tag"\s+content="([^"]*)"', c)

    # 3. Twitter
    tw_card = re.search(r'<meta\s+name="twitter:card"\s+content="([^"]*)"', c)
    tw_title = re.search(r'<meta\s+name="twitter:title"\s+content="([^"]*)"', c)
    tw_img = re.search(r'<meta\s+name="twitter:image"\s+content="([^"]*)"', c)

    # 4. GEO tags
    geo_region = re.search(r'<meta\s+name="geo\.region"\s+content="([^"]*)"', c)
    geo_place = re.search(r'<meta\s+name="geo\.placename"\s+content="([^"]*)"', c)
    geo_pos = re.search(r'<meta\s+name="geo\.position"\s+content="([^"]*)"', c)
    icbm = re.search(r'<meta\s+name="ICBM"\s+content="([^"]*)"', c)
    geo_country = re.search(r'<meta\s+name="geo\.country"\s+content="([^"]*)"', c)

    # 5. Schema JSON-LD
    schemas = []
    schema_m = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', c)
    parsed_schemas = []
    for s_raw in schema_m:
        try:
            s_data = json.loads(s_raw)
            if '@graph' in s_data:
                for node in s_data['@graph']:
                    parsed_schemas.append(node)
            else:
                parsed_schemas.append(s_data)
        except Exception as e:
            parsed_schemas.append({'error': str(e)})

    schema_types = []
    for s in parsed_schemas:
        t = s.get('@type')
        if isinstance(t, list):
            schema_types.append('/'.join(t))
        elif t:
            schema_types.append(str(t))

    results.append({
        'file': rel_path,
        'title': title,
        'title_len': len(title) if title else 0,
        'desc': desc,
        'desc_len': len(desc) if desc else 0,
        'canonical': canon,
        'h1_count': h1_count,
        'og_title': bool(og_title),
        'og_desc': bool(og_desc),
        'og_img': bool(og_img),
        'og_type': og_type.group(1) if og_type else None,
        'og_tags_count': len(og_tags),
        'tw_card': bool(tw_card),
        'has_geo': bool(geo_region and geo_place and geo_pos and icbm),
        'has_geo_country': bool(geo_country),
        'schema_types': schema_types,
        'parsed_schemas': parsed_schemas
    })

print(f"Audited {len(results)} pages successfully.")

# Save json for detailed analysis
with open(r'perbaikan\audit_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Saved audit_results.json")

