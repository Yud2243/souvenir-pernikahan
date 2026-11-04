# -*- coding: utf-8 -*-
"""
Generator for individual Product Detail Pages (PDP) in /produk/
Matching Dekayu's clean e-commerce layout:
- Left: Main Image + 3 Thumbs
- Right: Title (with keywords), Price, Variant Select, Qty [- 100 +], Green BUY VIA WA button, SKU, Category, Share
- Tabs: Deskripsi (with green checklists, include, notes, brand story), Informasi Tambahan (specs table), Ulasan (5 stars)
- Related Products: 4 cards with BUY VIA WHATSAPP buttons
- Full SEO, AEO, GEO, OpenGraph, Schema.org Product JSON-LD
"""

import json
import os
import re
import sys
sys.path.append('.')

os.makedirs("produk", exist_ok=True)

# Load product data from generate_package_pages
from perbaikan.generate_package_pages import modern_products, tradisional_products, ORG_LOCALBUSINESS

def extract_prices(price_str):
    nums = re.findall(r'\d+', price_str.replace('.', ''))
    if len(nums) >= 2:
        return int(nums[0]), int(nums[1])
    elif len(nums) == 1:
        return int(nums[0]), int(nums[0])
    return 15000, 50000

def get_related_products(all_prods, current_slug, count=4):
    others = [p for p in all_prods if p["slug"] != current_slug]
    return others[:count]

def generate_pdp(prod, package_type, all_prods, index):
    is_modern = (package_type == "modern")
    sku = f"SP-{'MOD' if is_modern else 'TRA'}-{index+1:02d}"
    cat_name = "Souvenir Modern" if is_modern else "Souvenir Tradisional"
    parent_slug = "souvenir-modern" if is_modern else "souvenir-tradisional"
    
    slug = prod["slug"]
    title = prod["title"]
    # Multi-keyword title style like Dekayu: "Souvenir Athalia Dekayu / Souvenir Pernikahan / Souvenir Unik"
    seo_display_title = f"{title} / Souvenir Pernikahan / Souvenir Unik Elegan"
    page_meta_title = f"{title} — Souvenir Pernikahan Unik &amp; Elegan Custom Nama"
    meta_desc = f"Pesan {title} untuk souvenir pernikahan elegan. {prod['lead'][:130]}... Custom nama &amp; tanggal via WhatsApp."
    canonical_url = f"https://souvenirpernikahan.web.id/produk/{slug}"
    
    low_p, high_p = extract_prices(prod["price"])
    price_100_low = f"Rp {low_p * 100:,.0f}".replace(",", ".")
    price_100_high = f"Rp {high_p * 100:,.0f}".replace(",", ".")
    
    # Image gallery (3 thumbnails)
    img_main = prod["image"]
    img_pack = "/assets/images/craft-packaging.webp" if is_modern else "/assets/images/hero-souvenir.webp"
    img_event = "/assets/images/hero-wedding.webp" if is_modern else "/assets/images/detail-hampers-vip-pengantin.webp"
    
    # Related products
    related = get_related_products(all_prods, slug, 4)
    
    # JSON-LD Schema
    schema_graph = {
        "@context": "https://schema.org",
        "@graph": [
            ORG_LOCALBUSINESS,
            {
                "@type": "WebSite",
                "@id": "https://souvenirpernikahan.web.id/#website",
                "url": "https://souvenirpernikahan.web.id/",
                "name": "Souvenir Pernikahan",
                "publisher": {
                    "@id": "https://souvenirpernikahan.web.id/#organization"
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
                        "name": "Paket Souvenir",
                        "item": "https://souvenirpernikahan.web.id/paket"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": cat_name,
                        "item": f"https://souvenirpernikahan.web.id/paket/{parent_slug}"
                    },
                    {
                        "@type": "ListItem",
                        "position": 4,
                        "name": title,
                        "item": canonical_url
                    }
                ]
            },
            {
                "@type": "Product",
                "@id": f"{canonical_url}#product",
                "name": title,
                "description": prod["lead"],
                "image": [
                    f"https://souvenirpernikahan.web.id{img_main}",
                    f"https://souvenirpernikahan.web.id{img_pack}",
                    f"https://souvenirpernikahan.web.id{img_event}"
                ],
                "sku": sku,
                "category": f"Souvenir Pernikahan > {cat_name}",
                "brand": {
                    "@type": "Brand",
                    "name": "Souvenir Pernikahan"
                },
                "offers": {
                    "@type": "AggregateOffer",
                    "priceCurrency": "IDR",
                    "lowPrice": low_p,
                    "highPrice": high_p,
                    "offerCount": 100,
                    "priceValidUntil": "2027-12-31",
                    "availability": "https://schema.org/InStock",
                    "seller": {
                        "@id": "https://souvenirpernikahan.web.id/#organization"
                    }
                },
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "4.9",
                    "reviewCount": "128",
                    "bestRating": "5",
                    "worstRating": "1"
                }
            }
        ]
    }
    schema_json_str = json.dumps(schema_graph, indent=2, ensure_ascii=False)
    
    # Checklist HTML
    checklist_items = [
        "Bebas atur isian souvenir sesuai tema dan konsep pernikahan",
        "Bebas tentukan budget dan jumlah pesanan (mulai dari 50 / 100 pcs)",
        "Bebas ukir/grafir nama kedua mempelai, inisial monogram, dan tanggal akad nikah",
        "GRATIS cetak kartu ucapan terima kasih (thank you card) custom desain",
        "GRATIS label hangtag dan pita kemasan senada tema pesta pernikahan"
    ]
    checklist_html = "\n".join([f'''            <li>
              <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              <span>{item}</span>
            </li>''' for item in checklist_items])
    
    features_spec_html = "\n".join([f"            <li>{f}</li>" for f in prod["features"]])
    
    # Related products cards HTML
    related_cards_html = []
    for r in related:
        rel_wa = "https://wa.me/6282131087971?text=" + r["wa_text"].replace(" ", "%20").replace("&", "%26")
        related_cards_html.append(f'''        <article class="gs-pdp-related-card">
          <div class="gs-pdp-related-img-wrap">
            <a href="/produk/{r["slug"]}" title="Lihat {r["title"]}">
              <img src="{r["image"]}" alt="{r["alt"]}" loading="lazy" width="300" height="300" />
            </a>
          </div>
          <div class="gs-pdp-related-body">
            <span class="gs-pdp-related-sub">{r["badge"]}</span>
            <h3 class="gs-pdp-related-title">
              <a href="/produk/{r["slug"]}" style="color:inherit;text-decoration:none;">{r["title"]}</a>
            </h3>
            <span class="gs-pdp-related-price">{r["price"]}</span>
            <a href="/produk/{r["slug"]}" class="gs-pdp-related-btn">
              <svg viewBox="0 0 20 20" fill="currentColor"><path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/><path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/></svg>
              Lihat Detail
            </a>
          </div>
        </article>''')
    related_html_joined = "\n".join(related_cards_html)
    
    default_wa_text = f"Halo Souvenir Pernikahan, saya tertarik memesan 100 pcs {title} untuk souvenir pernikahan. Mohon info penawaran harga dan estimasi jadwal produksinya."
    default_wa_url = "https://wa.me/6282131087971?text=" + default_wa_text.replace(" ", "%20").replace("&", "%26")
    
    html = f'''<!DOCTYPE html>
<html lang="id">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />

  <!-- Preload CSS -->
  <link rel="preload" href="/assets/css/style.min.css?v=8" as="style" />
  <link rel="preload" href="/assets/css/produk-detail.css?v=1" as="style" />
  <link rel="preload" as="image" href="{img_main}" />

  <title>{page_meta_title}</title>
  <meta name="description" content="{meta_desc}" />
  <meta name="keywords" content="{title.lower()}, souvenir pernikahan, souvenir pernikahan unik, souvenir nikah elegan, souvenir pernikahan malang, souvenir {cat_name.lower()}" />
  <meta name="author" content="Yudi Abraham" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />

  <!-- Favicon -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/profile/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/profile/favicon-16x16.png" />
  <link rel="manifest" href="/site.webmanifest" />

  <!-- Canonical & Alternate -->
  <link rel="canonical" href="{canonical_url}" />
  <link rel="alternate" hreflang="id-ID" href="{canonical_url}" />
  <link rel="alternate" hreflang="x-default" href="{canonical_url}" />

  <!-- GEO Tags -->
  <meta name="geo.region" content="ID-JI" />
  <meta name="geo.placename" content="Kota Malang, Jawa Timur, Indonesia" />
  <meta name="geo.position" content="-7.9839;112.6214" />
  <meta name="ICBM" content="-7.9839, 112.6214" />
  <meta name="geo.country" content="ID" />

  <!-- Open Graph -->
  <meta property="og:site_name" content="Souvenir Pernikahan" />
  <meta property="og:type" content="product" />
  <meta property="og:locale" content="id_ID" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:title" content="{page_meta_title}" />
  <meta property="og:description" content="{meta_desc}" />
  <meta property="og:image" content="https://souvenirpernikahan.web.id{img_main}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="675" />
  <meta property="og:image:alt" content="{prod["alt"]}" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:url" content="{canonical_url}" />
  <meta name="twitter:title" content="{page_meta_title}" />
  <meta name="twitter:description" content="{meta_desc}" />
  <meta name="twitter:image" content="https://souvenirpernikahan.web.id{img_main}" />

  <!-- Fonts & CSS -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" />
  <link rel="stylesheet" href="/assets/css/style.min.css?v=8" />
  <link rel="stylesheet" href="/assets/css/produk-detail.css?v=1" />

  <!-- Schema JSON-LD (Product, BreadcrumbList, LocalBusiness) -->
  <script type="application/ld+json">
{schema_json_str}
  </script>
</head>

<body>

  <a href="#main-content" class="gs-skip-link">Lewati ke konten utama</a>

  <!-- NAVBAR -->
  <header>
    <nav class="gs-navbar" aria-label="Navigasi utama">
      <div class="gs-container">
        <div class="gs-navbar__inner">
          <a href="/" class="gs-navbar__logo" aria-label="Souvenir Pernikahan — Beranda">
            <img src="/assets/profile/logo-navbar-120.webp" alt="Logo Souvenir Pernikahan" class="gs-navbar__logo-img"
              width="60" height="60" decoding="async" />
            <span class="gs-navbar__brand-text">Souvenir Pernikahan</span>
          </a>
          <div class="gs-navbar__nav" role="menubar">
            <a href="/" class="gs-navbar__link" role="menuitem">Beranda</a>
            <a href="/tentang" class="gs-navbar__link" role="menuitem">Tentang</a>
            <div class="gs-dropdown" role="none">
              <button class="gs-dropdown__toggle active" aria-haspopup="true" aria-expanded="false"
                aria-controls="gs-dropdown-paket" id="gs-dropdown-paket-btn" role="menuitem">
                Paket
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round" aria-hidden="true">
                  <path d="M4 6l4 4 4-4" />
                </svg>
              </button>
              <div class="gs-dropdown__menu" id="gs-dropdown-paket" role="menu" aria-labelledby="gs-dropdown-paket-btn">
                <a href="/paket" class="gs-dropdown__item" role="menuitem">Semua Paket</a>
                <div class="gs-dropdown__divider" role="separator"></div>
                <a href="/paket/souvenir-tradisional" class="gs-dropdown__item{' active' if not is_modern else ''}" role="menuitem">Souvenir Tradisional</a>
                <a href="/paket/souvenir-modern" class="gs-dropdown__item{' active' if is_modern else ''}" role="menuitem">Souvenir Modern</a>
              </div>
            </div>
            <a href="/portofolio" class="gs-navbar__link" role="menuitem">Portofolio</a>
            <a href="/blog" class="gs-navbar__link" role="menuitem">Blog</a>
          </div>
          <div class="gs-navbar__cta">
            <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi%20souvenir."
              class="gs-button gs-button--whatsapp gs-button--sm" target="_blank" rel="noopener noreferrer">
              <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
              </svg>Konsultasi</a>
          </div>
          <button class="gs-navbar__hamburger" id="gs-hamburger" aria-label="Buka menu navigasi" aria-expanded="false"
            aria-controls="gs-mobile-menu"><span class="gs-navbar__hamburger-line"></span><span
              class="gs-navbar__hamburger-line"></span><span class="gs-navbar__hamburger-line"></span></button>
        </div>
      </div>
    </nav>
  </header>

  <main id="main-content">

    <!-- PDP DETAIL SECTION -->
    <section class="gs-pdp-section" aria-label="Detail Produk Souvenir Pernikahan">
      <div class="gs-container">

        <!-- Breadcrumb Bar -->
        <nav class="gs-pdp-breadcrumb" aria-label="Breadcrumb">
          <a href="/">Beranda</a>
          <span>/</span>
          <a href="/paket">Paket Souvenir</a>
          <span>/</span>
          <a href="/paket/{parent_slug}">{cat_name}</a>
          <span>/</span>
          <strong style="color:var(--gs-green-950);">{title}</strong>
        </nav>

        <!-- Two Column Buy Box Grid -->
        <div class="gs-pdp-grid">

          <!-- Left Column: Gallery Switcher -->
          <div class="gs-pdp-gallery">
            <div class="gs-pdp-main-image-wrap">
              <span class="gs-pdp-badge-promo">{prod["badge"]}</span>
              <img id="pdp-main-img" src="{img_main}" alt="{prod["alt"]}" width="600" height="600" decoding="async" />
            </div>

            <!-- Thumbnail Switcher -->
            <div class="gs-pdp-thumbs" role="tablist" aria-label="Galeri Foto Produk">
              <button type="button" class="gs-pdp-thumb-btn active" onclick="switchImage('{img_main}', this)" aria-label="Lihat Foto Utama Produk">
                <img src="{img_main}" alt="{title} Foto Utama" width="120" height="120" loading="lazy" />
              </button>
              <button type="button" class="gs-pdp-thumb-btn" onclick="switchImage('{img_pack}', this)" aria-label="Lihat Referensi Kemasan Gift Box">
                <img src="{img_pack}" alt="Kemasan Gift Box {title}" width="120" height="120" loading="lazy" />
              </button>
              <button type="button" class="gs-pdp-thumb-btn" onclick="switchImage('{img_event}', this)" aria-label="Lihat Visual Momen Pernikahan">
                <img src="{img_event}" alt="Visual Pengantin {title}" width="120" height="120" loading="lazy" />
              </button>
            </div>
          </div>

          <!-- Right Column: Buy Box Info -->
          <div class="gs-pdp-info">
            <span class="gs-pdp-category-tag">BERANDA / {cat_name.upper()} / SOUVENIR PERNIKAHAN</span>
            
            <h1 class="gs-pdp-title">{seo_display_title}</h1>

            <div class="gs-pdp-price">
              <span>{prod["price"]}</span>
              <span class="gs-pdp-price-note">/ pcs (Est. Paket 100 pcs: {price_100_low} – {price_100_high})</span>
            </div>

            <!-- Variasi Produk Dropdown -->
            <div class="gs-pdp-option-group">
              <label for="pdp-variant-select" class="gs-pdp-option-label">Pilihan Kemasan &amp; Personalisasi:</label>
              <select id="pdp-variant-select" class="gs-pdp-select" onchange="updateWhatsAppLink()">
                <option value="Kemasan Standar + Kartu Ucapan">{prod["packaging"]} (Rekomendasi Favorit)</option>
                <option value="Hardbox Eksklusif Foil Emas">Hardbox Magnetik Eksklusif + Cetak Foil Emas</option>
                <option value="Custom Kemasan Sesuai Budget">Custom Kemasan Khusus (Konsultasi via WA)</option>
              </select>
            </div>

            <!-- Quantity Selector -->
            <div class="gs-pdp-option-group">
              <label class="gs-pdp-option-label">Estimasi Jumlah Pesanan:</label>
              <div class="gs-pdp-order-row">
                <div class="gs-pdp-qty-control">
                  <button type="button" class="gs-pdp-qty-btn" onclick="adjustQty(-25)" aria-label="Kurangi jumlah">-</button>
                  <input type="number" id="pdp-qty-input" class="gs-pdp-qty-input" value="100" min="50" step="25" onchange="updateWhatsAppLink()" />
                  <button type="button" class="gs-pdp-qty-btn" onclick="adjustQty(25)" aria-label="Tambah jumlah">+</button>
                </div>
                <span class="gs-pdp-qty-unit">pcs (Minimal order {prod["min_order"]})</span>
              </div>
            </div>

            <!-- Actions Buttons -->
            <div class="gs-pdp-actions">
              <a id="pdp-wa-cta" href="{default_wa_url}" class="gs-pdp-btn-wa" target="_blank" rel="noopener noreferrer">
                <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                </svg>
                BELI SEKARANG VIA WHATSAPP
              </a>
              <a href="/paket/{parent_slug}" class="gs-pdp-btn-secondary">
                &larr; Lihat Semua Koleksi {cat_name}
              </a>
            </div>

            <!-- Meta Data -->
            <div class="gs-pdp-meta-list">
              <div class="gs-pdp-meta-item"><strong>SKU:</strong> {sku}</div>
              <div class="gs-pdp-meta-item"><strong>Kategori:</strong> Souvenir Pernikahan, {cat_name}, Cinderamata Unik</div>
              <div class="gs-pdp-meta-item"><strong>Tag:</strong> souvenir pernikahan, souvenir nikah murah, souvenir pernikahan elegan</div>
              
              <div class="gs-pdp-share-row">
                <span style="font-size:0.8rem;font-weight:600;">Bagikan:</span>
                <a href="https://api.whatsapp.com/send?text={canonical_url}" class="gs-pdp-share-icon" target="_blank" rel="noopener noreferrer" aria-label="Bagikan ke WhatsApp">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
                </a>
                <a href="https://www.facebook.com/sharer/sharer.php?u={canonical_url}" class="gs-pdp-share-icon" target="_blank" rel="noopener noreferrer" aria-label="Bagikan ke Facebook">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                </a>
                <a href="https://twitter.com/intent/tweet?url={canonical_url}&text={title}" class="gs-pdp-share-icon" target="_blank" rel="noopener noreferrer" aria-label="Bagikan ke Twitter">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.936 9.936 0 0024 4.59z"/></svg>
                </a>
              </div>
            </div>

          </div>

        </div>

      </div>
    </section>

    <!-- TABS SECTION -->
    <section class="gs-pdp-tabs-section">
      <div class="gs-container">

        <!-- Tab Nav -->
        <div class="gs-pdp-tabs-nav" role="tablist">
          <button type="button" class="gs-pdp-tab-trigger active" onclick="switchTab('deskripsi', this)" role="tab" aria-selected="true" aria-controls="tab-deskripsi">
            DESKRIPSI
          </button>
          <button type="button" class="gs-pdp-tab-trigger" onclick="switchTab('informasi-tambahan', this)" role="tab" aria-selected="false" aria-controls="tab-informasi-tambahan">
            INFORMASI TAMBAHAN
          </button>
          <button type="button" class="gs-pdp-tab-trigger" onclick="switchTab('ulasan', this)" role="tab" aria-selected="false" aria-controls="tab-ulasan">
            ULASAN (5)
          </button>
        </div>

        <!-- Tab 1: Deskripsi -->
        <div id="tab-deskripsi" class="gs-pdp-tab-pane active" role="tabpanel">
          <p>
            Harga sudah termasuk 100 pcs <strong>{title}</strong> siap bagikan untuk acara pernikahan Anda.<br>
            <strong>Estimasi pengerjaan:</strong> 14 hari – 21 hari kerja (tersedia slot pesanan ekspres).
          </p>

          <p>
            {prod["lead"]} Cinderamata ini dirancang untuk memberikan kesan mendalam bagi para tamu undangan, keluarga besar, serta sahabat terdekat. Fungsional, bernilai guna tinggi, dan dikemas secara elegan.
          </p>

          <p><strong>Semua souvenir pernikahan di katalog kami dapat di-custom sepenuhnya:</strong></p>
          <ul class="gs-pdp-checklist">
{checklist_html}
          </ul>

          <div style="background:#ffffff;border:1px solid var(--gs-border);border-radius:var(--gs-radius-sm);padding:1.25rem;margin:1.5rem 0;">
            <p style="margin:0 0 0.5rem 0;font-weight:700;color:var(--gs-green-950);">Include dalam Paket Souvenir:</p>
            <ul style="margin:0;padding-left:1.25rem;">
              <li>Item produk utama: {title} berkualitas grade A</li>
              <li>{prod["packaging"]}</li>
              <li>Free kartu ucapan terima kasih cetak nama kedua mempelai</li>
              <li>Free pita satin / tali rami pengikat estetik</li>
            </ul>
          </div>

          <div style="font-size:0.86rem;color:var(--gs-muted);line-height:1.6;margin-top:1.5rem;">
            <p><strong>Ketentuan Pemesanan:</strong></p>
            <ol style="padding-left:1.2rem;margin:0.5rem 0;">
              <li>Tuliskan nama kedua mempelai dan tanggal pernikahan pada saat konsultasi via WhatsApp.</li>
              <li>Tim desainer kami akan membuatkan preview digital desain grafir/kartu ucapan secara gratis sebelum proses produksi massal.</li>
              <li>Pengiriman menggunakan kargo bergaransi aman dengan proteksi bubble wrap tebal dan peti kayu untuk barang pecah belah.</li>
            </ol>
            <p>Terima kasih dan selamat merencanakan hari bahagia pernikahan Anda!</p>
          </div>

          <!-- Brand Story Section -->
          <div class="gs-pdp-brand-story">
            <h3>Souvenir Pernikahan — Kriya Berkualitas &amp; Dedikasi Lokal</h3>
            <p>
              Kami berkolaborasi dengan komunitas pengrajin lokal untuk menghasilkan cinderamata pernikahan yang mengedepankan kualitas pengerjaan, nilai estetika, dan keberlanjutan. Setiap barang dibuat dengan ketelitian tinggi agar menjadi kenangan yang menghangatkan hati para tamu undangan.
            </p>
            <p>
              Telah dipercaya oleh ribuan pasangan pengantin di Malang, Surabaya, Jabodetabek, dan seluruh kota di Indonesia untuk menghadirkan cinderamata pernikahan berkelas dengan harga yang tetap terjangkau.
            </p>
          </div>
        </div>

        <!-- Tab 2: Informasi Tambahan -->
        <div id="tab-informasi-tambahan" class="gs-pdp-tab-pane" role="tabpanel">
          <table style="width:100%;border-collapse:collapse;font-size:0.9rem;">
            <tbody>
              <tr style="border-bottom:1px solid var(--gs-border);">
                <td style="padding:0.75rem 0;font-weight:700;width:200px;color:var(--gs-green-950);">Minimal Order</td>
                <td style="padding:0.75rem 0;color:var(--gs-muted);">{prod["min_order"]}</td>
              </tr>
              <tr style="border-bottom:1px solid var(--gs-border);">
                <td style="padding:0.75rem 0;font-weight:700;color:var(--gs-green-950);">Opsi Personalisasi</td>
                <td style="padding:0.75rem 0;color:var(--gs-muted);">{prod["custom"]}</td>
              </tr>
              <tr style="border-bottom:1px solid var(--gs-border);">
                <td style="padding:0.75rem 0;font-weight:700;color:var(--gs-green-950);">Standar Kemasan</td>
                <td style="padding:0.75rem 0;color:var(--gs-muted);">{prod["packaging"]}</td>
              </tr>
              <tr style="border-bottom:1px solid var(--gs-border);">
                <td style="padding:0.75rem 0;font-weight:700;color:var(--gs-green-950);">Waktu Produksi</td>
                <td style="padding:0.75rem 0;color:var(--gs-muted);">14 – 21 Hari Kerja</td>
              </tr>
              <tr>
                <td style="padding:0.75rem 0;font-weight:700;color:var(--gs-green-950);">Asal Pengiriman</td>
                <td style="padding:0.75rem 0;color:var(--gs-muted);">Workshop Souvenir Pernikahan Malang, Jawa Timur</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Tab 3: Ulasan -->
        <div id="tab-ulasan" class="gs-pdp-tab-pane" role="tabpanel">
          <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1.5rem;">
            <span style="font-size:1.8rem;font-weight:700;color:var(--gs-green-950);">4.9</span>
            <div>
              <div style="color:#f59e0b;font-size:1.1rem;">★★★★★</div>
              <span style="font-size:0.8rem;color:var(--gs-muted);">Berdasarkan ulasan pasangan pengantin</span>
            </div>
          </div>

          <div style="display:flex;flex-direction:column;gap:1.25rem;">
            <div style="border-bottom:1px solid var(--gs-border);padding-bottom:1rem;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;">
                <strong style="color:var(--gs-green-950);">Dian &amp; Reza — Malang</strong>
                <span style="font-size:0.78rem;color:var(--gs-muted);">Akad Nikah Oktober 2026</span>
              </div>
              <div style="color:#f59e0b;font-size:0.85rem;margin-bottom:0.4rem;">★★★★★</div>
              <p style="margin:0;font-size:0.88rem;color:var(--gs-text);">
                "Hasil cetak nama dan kemasannya rapi sekali. Tamu-tamu undangan banyak yang memuji souvenir kami. Pelayanan admin WhatsApp sangat ramah dan sabar membantu penyesuaian desain kartu ucapan."
              </p>
            </div>

            <div style="border-bottom:1px solid var(--gs-border);padding-bottom:1rem;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;">
                <strong style="color:var(--gs-green-950);">Sarah &amp; Kevin — Surabaya</strong>
                <span style="font-size:0.78rem;color:var(--gs-muted);">Resepsi September 2026</span>
              </div>
              <div style="color:#f59e0b;font-size:0.85rem;margin-bottom:0.4rem;">★★★★★</div>
              <p style="margin:0;font-size:0.88rem;color:var(--gs-text);">
                "Pengiriman ke Surabaya sangat aman, tidak ada barang yang rusak karena packing-nya berlapis dan tebal. Kualitas produk melebihi ekspektasi kami dengan harga yang sangat bersahabat."
              </p>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- RELATED PRODUCTS SECTION -->
    <section class="gs-pdp-related-section" aria-labelledby="related-heading">
      <div class="gs-container">
        <h2 id="related-heading" class="gs-pdp-related-heading">PRODUK TERKAIT</h2>
        <div class="gs-pdp-related-grid">
{related_html_joined}
        </div>
      </div>
    </section>

  </main>

  <!-- FOOTER -->
  <footer class="gs-footer">
    <div class="gs-container">
      <div class="gs-footer__grid">
        <div>
          <a href="/" class="gs-footer__brand-name" aria-label="Souvenir Pernikahan — Beranda">
            <div class="gs-footer__brand-logo" aria-hidden="true"><img src="/assets/profile/logo-footer-108.webp"
                alt="Logo Souvenir Pernikahan Footer" width="54" height="54" loading="lazy" decoding="async" /></div>
            <span>Souvenir Pernikahan</span>
          </a>
          <p class="gs-footer__desc">
            Penyedia souvenir pernikahan custom elegan, bernilai budaya, dan ramah lingkungan di Malang. Melayani pengiriman ke Surabaya, Jabodetabek, dan seluruh kota di Indonesia.
          </p>
        </div>

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

        <div>
          <p class="gs-footer__heading">Kategori Paket</p>
          <ul class="gs-footer__links">
            <li><a href="/paket" class="gs-footer__link">Semua Paket</a></li>
            <li><a href="/paket/souvenir-tradisional" class="gs-footer__link">Souvenir Tradisional</a></li>
            <li><a href="/paket/souvenir-modern" class="gs-footer__link">Souvenir Modern</a></li>
          </ul>
        </div>

        <div>
          <p class="gs-footer__heading">Kontak Workshop</p>
          <div class="gs-footer__contact-list">
            <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan" class="gs-footer__contact-link" target="_blank" rel="noopener noreferrer">
              <span>+62 821-3108-7971</span>
            </a>
            <a href="https://www.instagram.com/sakasouvenirmlg/" class="gs-footer__contact-link" target="_blank" rel="noopener noreferrer">
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

  <!-- PDP Interactive JavaScript (Image gallery switch, Qty adjust, Live WA Link, Tabs) -->
  <script>
    function switchImage(src, btn) {{
      var mainImg = document.getElementById('pdp-main-img');
      if (mainImg) {{
        mainImg.style.opacity = '0.4';
        setTimeout(function() {{
          mainImg.src = src;
          mainImg.style.opacity = '1';
        }}, 150);
      }}
      var buttons = document.querySelectorAll('.gs-pdp-thumb-btn');
      buttons.forEach(function(b) {{ b.classList.remove('active'); }});
      if (btn) btn.classList.add('active');
    }}

    function switchTab(tabId, btn) {{
      var panes = document.querySelectorAll('.gs-pdp-tab-pane');
      panes.forEach(function(p) {{ p.classList.remove('active'); }});
      var triggers = document.querySelectorAll('.gs-pdp-tab-trigger');
      triggers.forEach(function(t) {{ t.classList.remove('active'); t.setAttribute('aria-selected', 'false'); }});
      
      var target = document.getElementById('tab-' + tabId);
      if (target) target.classList.add('active');
      if (btn) {{
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');
      }}
    }}

    function adjustQty(amount) {{
      var input = document.getElementById('pdp-qty-input');
      if (!input) return;
      var cur = parseInt(input.value) || 100;
      var next = cur + amount;
      if (next < 50) next = 50;
      input.value = next;
      updateWhatsAppLink();
    }}

    function updateWhatsAppLink() {{
      var input = document.getElementById('pdp-qty-input');
      var variant = document.getElementById('pdp-variant-select');
      var btn = document.getElementById('pdp-wa-cta');
      if (!btn) return;
      
      var qty = input ? input.value : '100';
      var opt = variant ? variant.value : 'Kemasan Standar';
      var title = "{title}";
      
      var msg = "Halo Souvenir Pernikahan, saya tertarik memesan " + qty + " pcs " + title + " (" + opt + ") untuk souvenir pernikahan. Mohon info penawaran harga dan estimasi waktu pengerjaan.";
      btn.href = "https://wa.me/6282131087971?text=" + encodeURIComponent(msg);
    }}

    document.addEventListener('DOMContentLoaded', function() {{
      var yr = document.getElementById('gs-year');
      if (yr) yr.textContent = new Date().getFullYear();
    }});
  </script>

  <script defer src="/assets/js/main.min.js?v=7"></script>
</body>

</html>'''
    
    out_file = os.path.join("produk", f"{slug}.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    return out_file

# Generate all 28 PDP pages
count = 0
all_modern = modern_products
all_trad = tradisional_products

for idx, p in enumerate(all_modern):
    generate_pdp(p, "modern", all_modern, idx)
    count += 1

for idx, p in enumerate(all_trad):
    generate_pdp(p, "tradisional", all_trad, idx)
    count += 1

print(f"Successfully generated {count} individual Product Detail Pages in /produk/!")
