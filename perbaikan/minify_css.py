import re
import os

def minify_css(css_text):
    # 1. Remove comments
    css_text = re.sub(r'/\*[\s\S]*?\*/', '', css_text)
    
    # 2. Normalize whitespace
    css_text = re.sub(r'\s+', ' ', css_text)
    
    # 3. Remove spaces around special characters
    css_text = re.sub(r'\s*([\{\}\:;\,\>])\s*', r'\1', css_text)
    
    # 4. Remove unnecessary semicolons before closing brace
    css_text = re.sub(r';\}', '}', css_text)
    
    # 5. Fix spaces in media queries / calc if needed
    # Make sure 'and (' has a space
    css_text = re.sub(r'\band\(', 'and (', css_text)
    
    return css_text.strip()

if __name__ == '__main__':
    src = r'assets/css/style.css'
    dst = r'assets/css/style.min.css'
    
    with open(src, 'r', encoding='utf-8') as f:
        raw = f.read()
    
    minified = minify_css(raw)
    
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(minified)
        
    print(f"Minified {src} ({len(raw)} bytes) -> {dst} ({len(minified)} bytes)")

