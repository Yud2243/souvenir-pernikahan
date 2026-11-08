"""
Fix meta title & description pada semua halaman /produk/:
1. Hapus kata "murah" dan "unik" dari description dan keywords
2. Persingkat title dari pola "X — Souvenir Pernikahan Elegan & Berkesan" menjadi "X | Souvenir Pernikahan Custom"
3. Rewrite description template: 160 char max, tanpa kata terlarang
4. Update keywords: hapus "souvenir pernikahan murah", "souvenir pernikahan unik"
"""
import os, re, glob

PRODUK_DIR = r"c:\Untuk_PKL\Souvenirkeuda\produk"

# Template description baru (tanpa murah/unik)
DESC_TEMPLATE = (
    "SEKATA menghadirkan {product_name} sebagai souvenir pernikahan custom yang elegan dan personal. "
    "Gratis custom nama pengantin, kartu ucapan, harga grosir, dan garansi kirim seluruh Indonesia."
)

# Template description pendek jika terlalu panjang
DESC_SHORT_TEMPLATE = (
    "{product_name} — souvenir pernikahan custom elegan dari SEKATA. "
    "Gratis custom nama pengantin & kartu ucapan. Harga grosir, kirim seluruh Indonesia."
)

# Title suffix baru (lebih pendek)
NEW_SUFFIX = " | SEKATA Souvenir Pernikahan"

results = []

for filepath in sorted(glob.glob(os.path.join(PRODUK_DIR, "*.html"))):
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changed = False

    # --- Fix TITLE ---
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    if title_match:
        old_title = title_match.group(1)
        # Pattern: "Souvenir Pernikahan X — Souvenir Pernikahan Elegan & Berkesan"
        # Atau: "Paket Hampers Souvenir Pernikahan X — Souvenir Pernikahan Elegan & Berkesan"
        # Ambil bagian sebelum " — " atau " – "
        part_before = re.split(r'\s*[–—]\s*', old_title)[0].strip()
        # Escape HTML entities sudah di-encode, decode dulu
        part_before = part_before.replace('&amp;', '&')

        new_title = part_before + NEW_SUFFIX
        # Jika masih > 60 char, trim product name
        if len(new_title) > 60:
            # Coba versi lebih pendek: strip "Souvenir Pernikahan " prefix dari product name
            short_part = part_before
            if short_part.startswith("Souvenir Pernikahan "):
                short_part = short_part[len("Souvenir Pernikahan "):]
            elif short_part.startswith("Paket Hampers Souvenir Pernikahan "):
                short_part = short_part[len("Paket Hampers Souvenir Pernikahan "):]
            new_title = short_part + " | Souvenir Pernikahan Custom SEKATA"
            if len(new_title) > 65:
                # Hard truncate if still too long
                max_product = 65 - len(" | Souvenir Pernikahan SEKATA")
                new_title = short_part[:max_product].rstrip() + " | Souvenir Pernikahan SEKATA"

        # Re-encode ampersand for HTML
        new_title_html = new_title.replace('&', '&amp;')
        content = content.replace(title_match.group(0), f'<title>{new_title_html}</title>', 1)
        if content != original:
            changed = True

    # --- Fix DESCRIPTION ---
    desc_match = re.search(r'(<meta name="description"\s+content=")([^"]*?)(")', content)
    if desc_match:
        old_desc = desc_match.group(2)

        # Extract product name from old description pattern:
        # "Pusat Souvenir Pernikahan X murah, unik..."
        # or "Pusat Paket Hampers Souvenir Pernikahan X murah..."
        prod_name_match = re.match(
            r'Pusat (?:Paket Hampers )?Souvenir Pernikahan (.+?) (?:murah|unik|elegan)',
            old_desc
        )

        if prod_name_match:
            product_name = prod_name_match.group(1).strip()
            new_desc = DESC_TEMPLATE.format(product_name=product_name)
            if len(new_desc) > 160:
                new_desc = DESC_SHORT_TEMPLATE.format(product_name=product_name)
            # Cap at 160
            if len(new_desc) > 160:
                new_desc = new_desc[:157] + "..."
        else:
            # Fallback: just remove forbidden words
            new_desc = old_desc
            new_desc = re.sub(r'\s*murah,?\s*', ' ', new_desc)
            new_desc = re.sub(r'\s*unik,?\s*', ' ', new_desc)
            new_desc = re.sub(r'semakin banyak semakin\s+\w+[,.]?\s*', '', new_desc)
            new_desc = re.sub(r'\s+', ' ', new_desc).strip()
            if new_desc.endswith(','):
                new_desc = new_desc[:-1] + '.'

        content = content.replace(desc_match.group(0),
                                  f'{desc_match.group(1)}{new_desc}{desc_match.group(3)}', 1)
        if content != original:
            changed = True

    # --- Fix KEYWORDS: remove forbidden words ---
    kw_match = re.search(r'(<meta name="keywords"\s+content=")([^"]*?)(")', content)
    if kw_match:
        old_kw = kw_match.group(2)
        # Remove entries containing "murah" or "unik"
        kw_list = [k.strip() for k in old_kw.split(',')]
        kw_filtered = [k for k in kw_list if 'murah' not in k.lower() and 'unik' not in k.lower()]
        new_kw = ', '.join(kw_filtered)
        if new_kw != old_kw:
            content = content.replace(kw_match.group(0),
                                      f'{kw_match.group(1)}{new_kw}{kw_match.group(3)}', 1)
            changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        results.append(f"FIXED: {filename}")
    else:
        results.append(f"SKIP:  {filename}")

print(f"\nTotal: {len(results)} files processed")
for r in results:
    print(r)

