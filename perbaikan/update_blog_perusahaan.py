# -*- coding: utf-8 -*-
"""
Script to update blog/panduan-souvenir-perusahaan.html:
Re-frame from generic office merchandise to:
'Panduan Memilih Souvenir Elegan untuk Kolega Kantor & Acara Formal'
So it fits seamlessly into the wedding portal.
"""

import json
import re

with open('blog/panduan-souvenir-perusahaan.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update title and meta
content = re.sub(
    r'<title>[\s\S]*?</title>',
    '<title>Panduan Memilih Souvenir Elegan untuk Rekan Kerja &amp; Acara Formal — Souvenir Pernikahan</title>',
    content
)

content = re.sub(
    r'<meta name="description" content="[^"]*"',
    '<meta name="description" content="Panduan memilih souvenir pernikahan elegan dan cinderamata berkelas untuk rekan kerja kantor, atasan, dan tamu undangan formal dengan kemasan eksklusif."',
    content
)

# 2. Update H1 and Lead
content = re.sub(
    r'<h1 class="gs-article__title">[\s\S]*?</h1>',
    '<h1 class="gs-article__title">Panduan Memilih Souvenir Elegan untuk Rekan Kerja &amp; Acara Formal</h1>',
    content
)

old_lead = re.search(r'<p class="gs-article__lead">[\s\S]*?</p>', content)
new_lead = '''<p class="gs-article__lead">
              Mengundang rekan kerja, atasan kantor, maupun relasi formal ke acara resepsi pernikahan atau syukuran membutuhkan
              pertimbangan cinderamata yang matang. Souvenir yang dipilih di <a href="/">Souvenir Pernikahan</a> harus mampu
              mencerminkan rasa hormat, berkarakter elegan, bernilai guna tinggi, serta dikemas secara eksklusif. Simak panduan lengkapnya di sini.
            </p>'''

if old_lead:
    content = content[:old_lead.start()] + new_lead + content[old_lead.end():]

# 3. Update H2 #1
content = re.sub(
    r'1\. Perbedaan Mendasar Souvenir Perusahaan vs Pernikahan',
    '1. Karakter Souvenir yang Tepat untuk Tamu Kolega &amp; Rekan Kerja',
    content
)

# 4. Update Schema
schema_m = re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', content)
if schema_m:
    try:
        data = json.loads(schema_m.group(1))
        for obj in data.get('@graph', []):
            if obj.get('@type') in ['Article', 'BlogPosting']:
                obj['headline'] = 'Panduan Memilih Souvenir Elegan untuk Rekan Kerja & Acara Formal'
                obj['description'] = 'Panduan memilih souvenir pernikahan elegan dan cinderamata berkelas untuk rekan kerja kantor, atasan, dan tamu undangan formal.'
                if 'author' in obj and isinstance(obj['author'], dict):
                    obj['author']['jobTitle'] = 'Founder & Creative Lead'
                    obj['author']['description'] = 'Founder dan kurator kreatif Souvenir Pernikahan.'
        
        new_schema_str = json.dumps(data, indent=2, ensure_ascii=False)
        content = content[:schema_m.start()] + f'<script type="application/ld+json">\n{new_schema_str}\n  </script>' + content[schema_m.end():]
        print("Updated schema in blog/panduan-souvenir-perusahaan.html")
    except Exception as e:
        print("Schema update error:", e)

with open('blog/panduan-souvenir-perusahaan.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished updating blog/panduan-souvenir-perusahaan.html!")
