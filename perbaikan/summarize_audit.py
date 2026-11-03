import json

with open(r'perbaikan\audit_results.json', encoding='utf-8') as f:
    results = json.load(f)

print("="*100)
print(f"{'FILE':<40} | {'H1':<3} | {'SCHEMA TYPES':<40} | {'GEO':<5} | {'OG':<8}")
print("="*100)

for r in results:
    f = r['file']
    h1 = r['h1_count']
    schemas = ', '.join(r['schema_types'])
    geo = "OK" if r['has_geo'] and r['has_geo_country'] else ("PART" if r['has_geo'] else "NO")
    og = "OK" if (r['og_title'] and r['og_desc'] and r['og_img']) else "FAIL"
    print(f"{f:<40} | {h1:<3} | {schemas:<40} | {geo:<5} | {og:<8}")

print("\n" + "="*100)
print("DETAILED GAPS ANALYSIS")
print("="*100)

for r in results:
    gaps = []
    f = r['file']
    
    # 1. SEO Gaps
    if not r['title']: gaps.append("Missing <title>")
    elif r['title_len'] < 30 or r['title_len'] > 70: gaps.append(f"Title length suboptimal ({r['title_len']} chars)")
    
    if not r['desc']: gaps.append("Missing <meta name='description'>")
    elif r['desc_len'] < 100 or r['desc_len'] > 165: gaps.append(f"Meta desc length suboptimal ({r['desc_len']} chars)")
    
    if not r['canonical']: gaps.append("Missing canonical URL")
    if r['h1_count'] != 1: gaps.append(f"H1 count is {r['h1_count']} (expected 1)")

    # 2. Schema Gaps
    st = r['schema_types']
    if 'Organization/LocalBusiness' not in st and 'LocalBusiness' not in st and 'Organization' not in st:
        gaps.append("Missing Organization / LocalBusiness Schema")
    if 'WebSite' not in st and f != 'kebijakan-privasi.html':
        gaps.append("Missing WebSite Schema")
    if 'BreadcrumbList' not in st and f != 'index.html' and f != 'kebijakan-privasi.html':
        gaps.append("Missing BreadcrumbList Schema")

    # Specific page schemas
    if f == 'tentang.html' and 'AboutPage' not in st:
        gaps.append("Missing AboutPage Schema")
    if f == 'penulis.html' and 'Person' not in st and 'ProfilePage' not in st:
        gaps.append("Missing Person / ProfilePage Schema")
    if f in ['paket.html', 'portofolio.html'] and 'CollectionPage' not in st:
        gaps.append("Missing CollectionPage Schema")
    if f.startswith('paket/') and 'Product' not in st and 'Service' not in st:
        gaps.append("Missing Product / Service Schema on package landing page")

    # 3. AEO Gaps
    if 'FAQPage' not in st and f not in ['kebijakan-privasi.html', 'penulis.html', 'detail-portofolio.html']:
        gaps.append("No FAQPage schema for Answer Engine Optimization")

    # 4. GEO Gaps
    if not r['has_geo']:
        gaps.append("Missing GEO coordinate meta tags (geo.region, placename, ICBM)")
    elif not r['has_geo_country']:
        gaps.append("Missing <meta name='geo.country' content='ID'>")

    # 5. OpenGraph Gaps
    if not (r['og_title'] and r['og_desc'] and r['og_img']):
        gaps.append("Incomplete OpenGraph tags")
    if r['og_tags_count'] == 0 and f.startswith('blog/'):
        gaps.append("Missing article:tag in blog article")

    if gaps:
        print(f"\n[{f}]")
        for g in gaps:
            print(f"  - {g}")

