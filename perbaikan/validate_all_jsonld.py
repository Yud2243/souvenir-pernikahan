import json
import re
import os

all_html = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', '.gemini', 'node_modules', 'perbaikan', 'scratch']):
        continue
    for f in files:
        if f.endswith('.html') and f != 'googleda790fa92f6b7c24.html':
            all_html.append(os.path.join(root, f))

errors = 0
for fpath in all_html:
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    m = re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', text)
    if not m:
        print(f"[FAIL] Missing JSON-LD: {fpath}")
        errors += 1
        continue
    try:
        data = json.loads(m.group(1))
        # check if areaServed has all cities
        graph = data.get('@graph', [data])
        org = None
        for n in graph:
            nt = n.get('@type')
            if (isinstance(nt, list) and 'LocalBusiness' in nt) or nt == 'LocalBusiness':
                org = n
                break
        if org:
            served = org.get('areaServed', [])
            if len(served) < 15:
                print(f"[WARN] {fpath} areaServed count: {len(served)}")
        else:
            print(f"[WARN] No LocalBusiness in {fpath}")
    except Exception as e:
        print(f"[FAIL] Invalid JSON-LD in {fpath}: {e}")
        errors += 1

if errors == 0:
    print(f"[SUCCESS] All {len(all_html)} HTML files have 100% valid JSON-LD schemas!")
else:
    print(f"[ERROR] Found {errors} errors.")

