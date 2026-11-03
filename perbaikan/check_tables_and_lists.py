import os, re

blog_dir = 'blog'
files = [f for f in os.listdir(blog_dir) if f.endswith('.html')]

print(f"Total blog files: {len(files)}")
print(f"{'FILE':55} | {'TABLES':6} | {'UL':3} | {'OL':3}")
print("-" * 75)

for f in sorted(files):
    path = os.path.join(blog_dir, f)
    with open(path, encoding='utf-8') as fl:
        c = fl.read()
    
    tables = len(re.findall(r'<table', c))
    
    body_m = re.search(r'<div class="gs-article__body">(.*?)<section class="gs-article__faq-wrap"', c, re.DOTALL)
    body_text = body_m.group(1) if body_m else ''
    
    body_no_takeaway = re.sub(r'<aside class="gs-article__key-takeaway".*?</aside>', '', body_text, flags=re.DOTALL)
    lists_ul = len(re.findall(r'<ul', body_no_takeaway))
    lists_ol = len(re.findall(r'<ol', body_no_takeaway))
    
    print(f"{f:55} | {tables:6} | {lists_ul:3} | {lists_ol:3}")

