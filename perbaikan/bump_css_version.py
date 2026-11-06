import os
import glob
import re

html_files = []
for root, dirs, files in os.walk('.'):
    # skip .git
    if '.git' in root or '.gemini' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

count = 0
for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace style.min.css?v=... with style.min.css?v=13
    new_content, n = re.subn(r'style\.min\.css\?v=\d+', 'style.min.css?v=13', content)
    if n > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"Updated style.min.css?v=13 in {count} HTML files out of {len(html_files)}")

