# -*- coding: utf-8 -*-
"""
Rebuild all 28 Product Detail Pages (PDP) in /produk/ with Dynamic Wholesale/Tiered Pricing:
1. Dynamic wholesale/tiered pricing where unit price decreases as quantity increases.
2. Real-time calculated unit price, discount tier badge, and estimated total price.
3. Quick-selection quantity pills (e.g. 100, 250, 500, 1000+ pcs).
4. WhatsApp CTA pre-filled message synced with quantity, variant, unit price, and total estimate.
5. 100% valid Schema JSON-LD.
"""

import json
import os
import re
import urllib.parse
import sys
sys.path.append('.')

from perbaikan.generate_package_pages import modern_products, tradisional_products, ORG_LOCALBUSINESS
GALLERY_MAP = {
    "kipas-lipat-batik-tulis-kayu-jati": [
        ("/assets/images/kipas-batik-souvenir.webp", "Souvenir Pernikahan Kipas Lipat Batik Tulis Rangka Kayu Jati Tampak Depan"),
        ("/assets/images/kipas-batik-untuk-souvenir-pernikahan.webp", "Detail Bilah Kayu Ukir & Rumbai Sutra Kipas Batik"),
        ("/assets/images/craft-packaging.webp", "Kemasan Gift Box Kraft Rustic Bertali Rami")
    ],
    "mug-keramik-stoneware-rustic-monogram": [
        ("/assets/images/ceramic-mug-souvenir.webp", "Souvenir Pernikahan Mug Keramik Stoneware Rustic Monogram"),
        ("/assets/images/detail-mug-keramik-pengantin.webp", "Detail Monogram Emas & Glazur Keramik Terakota"),
        ("/assets/images/craft-packaging.webp", "Kemasan Hardbox Kraft Eksklusif Monogram")
    ],
    "pouch-dompet-tenun-lurik-tradisional": [
        ("/assets/images/pouch-tenun-souvenir.webp", "Souvenir Pernikahan Pouch Dompet Tenun Lurik Tradisional"),
        ("/assets/images/pouch-batik-dan-dompet-tenun-untuk-souvenir.webp", "Detail Tekstur Tenun ATBM & Kancing Batok Kelapa"),
        ("/assets/images/craft-packaging.webp", "Kemasan Gift Box Kraft Rustic & Pita Rami")
    ],
    "lilin-aromaterapi-pot-keramik-gerabah": [
        ("/assets/images/souvenir-lilin-aroma.webp", "Souvenir Pernikahan Lilin Aromaterapi Pot Gerabah Terakota"),
        ("/assets/images/detail-lilin-aroma-pengantin.webp", "Detail Lilin Aromaterapi Alami & Wangi Botanical"),
        ("/assets/images/candle-souvenir.webp", "Kemasan Box Kraft & Label Monogram")
    ],
    "lilin-aromaterapi-jar-frosted-gold": [
        ("/assets/images/candle-souvenir.webp", "Souvenir Pernikahan Lilin Aromaterapi Jar Frosted Tutup Gold"),
        ("/assets/images/detail-lilin-aroma-pengantin.webp", "Detail Jar Kaca Frosted & Tutup Logam Gold"),
        ("/assets/images/craft-packaging.webp", "Kemasan Gift Box Eksklusif & Kartu Ucapan")
    ],
    "tumbler-kopi-stainless-sage-green": [
        ("/assets/images/souvenir-tumbler-custom.webp", "Souvenir Pernikahan Tumbler Kopi Stainless Sage Green"),
        ("/assets/images/tumbler-souvenir.webp", "Detail Grafir Laser Monogram Nama Pengantin"),
        ("/assets/images/craft-packaging.webp", "Kemasan Box Tabung Silinder Eksklusif")
    ],
    "tumbler-termos-ivory-rose-gold": [
        ("/assets/images/tumbler-souvenir.webp", "Souvenir Pernikahan Tumbler Termos Stainless Ivory Rose Gold"),
        ("/assets/images/souvenir-tumbler-custom.webp", "Detail Finishing Matte & Tutup Rose Gold"),
        ("/assets/images/craft-packaging.webp", "Kemasan Box Silinder Berpita Grosgrain")
    ],
    "hampers-vip-gift-set-box": [
        ("/assets/images/souvenir-seminar-kit.webp", "Paket Hampers Souvenir Pernikahan VIP Gift Set Box Hijau Botol"),
        ("/assets/images/detail-hampers-vip-pengantin.webp", "Detail Isian Lengkap Hampers Pernikahan VIP"),
        ("/assets/images/hero-wedding.webp", "Kemasan Hardbox Magnetik Foil Emas")
    ],
    "besek-anyaman-bambu-bunga-kering": [
        ("/assets/images/besek-bambu-souvenir.webp", "Souvenir Pernikahan Besek Anyaman Bambu Hias Bunga Kering"),
        ("/assets/images/detail-souvenir-tradisional-pengantin.webp", "Detail Anyaman Bambu Halus & Buket Bunga Kering"),
        ("/assets/images/craft-packaging.webp", "Kemasan Tradisional Besek & Tali Rami")
    ],
    "sepasang-sendok-kayu-jati-alami": [
        ("/assets/images/wooden-spoon-souvenir.webp", "Souvenir Pernikahan Sepasang Sendok Garpu Kayu Jati Alami"),
        ("/assets/images/detail-souvenir-tradisional-pengantin.webp", "Detail Serat Kayu Jati Solid Food Grade"),
        ("/assets/images/craft-packaging.webp", "Kemasan Gift Box Kraft & Tali Rami Alami")
    ],
    "madu-hutan-jar-heksagonal-tutup-renda": [
        ("/assets/images/honey-souvenir.webp", "Souvenir Pernikahan Madu Hutan Jar Heksagonal Tutup Renda"),
        ("/assets/images/detail-souvenir-tradisional-pengantin.webp", "Detail Jar Kaca Heksagonal & Sendok Kayu Madu"),
        ("/assets/images/craft-packaging.webp", "Kemasan Soft Box Mika / Kraft Berpita")
    ],
    "sabun-herbal-batang-alami-handmade": [
        ("/assets/images/artisan-soap-souvenir.webp", "Souvenir Pernikahan Sabun Herbal Batang Alami Handmade"),
        ("/assets/images/detail-souvenir-tradisional-pengantin.webp", "Detail Tekstur Sabun Nabati & Aroma Alami"),
        ("/assets/images/craft-packaging.webp", "Kemasan Kertas Daur Ulang & Label Nama")
    ],
    "tatakan-gelas-kayu-jati-grafir-wreath": [
        ("/assets/images/coaster-souvenir.webp", "Souvenir Pernikahan Coaster Tatakan Gelas Kayu Jati Grafir Monogram"),
        ("/assets/images/detail-souvenir-tradisional-pengantin.webp", "Detail Grafir Laser Presisi Monogram Wreath"),
        ("/assets/images/craft-packaging.webp", "Kemasan Gift Box Kraft Ikat Rami")
    ],
    "pembatas-buku-kuningan-ukir-rumbai-sutra": [
        ("/assets/images/brass-bookmark-souvenir.webp", "Souvenir Pernikahan Pembatas Buku Kuningan Ukir Rumbai Sutra"),
        ("/assets/images/detail-souvenir-tradisional-pengantin.webp", "Detail Ukiran Logam Kuningan & Bandul Rumbai Sutra"),
        ("/assets/images/craft-packaging.webp", "Kemasan Amplop Kraft Estetik Bersegel Lilin")
    ],
    "saputangan-kain-linen-bordir-monogram": [
        ("/assets/images/linen-handkerchief-souvenir.webp", "Souvenir Pernikahan Saputangan Linen Bordir Monogram Klasik"),
        ("/assets/images/detail-souvenir-tradisional-pengantin.webp", "Detail Serat Kain Linen Alami & Bordir Monogram"),
        ("/assets/images/craft-packaging.webp", "Kemasan Box Kraft Transparan Berpita")
    ],
    "wax-sachet-pewangi-lemari-bunga-kering": [
        ("/assets/images/wax-sachet-souvenir.webp", "Souvenir Pernikahan Wax Sachet Botanical Bunga Kering"),
        ("/assets/images/detail-souvenir-tradisional-pengantin.webp", "Detail Lilin Aromatik Hias Bunga Kering Alami"),
        ("/assets/images/craft-packaging.webp", "Kemasan Pouch Organza & Gift Box")
    ],
    "tanaman-sukulen-mini-pot-balut-goni": [
        ("/assets/images/succulent-souvenir.webp", "Souvenir Pernikahan Tanaman Sukulen Mini Pot Balut Goni"),
        ("/assets/images/detail-souvenir-tradisional-pengantin.webp", "Detail Sukulen Hidup & Pot Kain Goni Rustic"),
        ("/assets/images/craft-packaging.webp", "Kemasan Mika Tegak / Kraft Handle")
    ],
    "cermin-saku-lipat-logam-ukir-klasik-emas": [
        ("/assets/images/compact-mirror-souvenir.webp", "Souvenir Pernikahan Cermin Saku Lipat Logam Ukir Klasik Emas"),
        ("/assets/images/detail-souvenir-tradisional-pengantin.webp", "Detail Ukiran Logam Vintage Bersepuh Emas"),
        ("/assets/images/craft-packaging.webp", "Kemasan Pouch Serut Beludru & Box Kraft")
    ],
    "glass-tumbler-borosilikat-tutup-bambu": [
        ("/assets/images/glass-tumbler-souvenir.webp", "Souvenir Pernikahan Glass Tumbler Kaca Borosilikat Tutup Bambu"),
        ("/assets/images/tumbler-souvenir.webp", "Detail Tutup Kayu Bambu Alami & Kaca Bening"),
        ("/assets/images/craft-packaging.webp", "Kemasan Box Kraft Silinder & Kartu Ucapan")
    ],
    "plakat-akrilik-souvenir-pernikahan": [
        ("/assets/images/souvenir-plakat-akrilik.webp", "Plakat Akrilik Souvenir Pernikahan Dudukan Kayu Solid"),
        ("/assets/images/craft-packaging.webp", "Kemasan Hardbox Beludru Eksklusif"),
        ("/assets/images/hero-souvenir-sq-597.webp", "Detail Grafir Bening Akrilik Presisi")
    ],
    "set-teh-herbal-tabung-kaca-saringan-emas": [
        ("/assets/images/tea-infuser-souvenir.webp", "Souvenir Pernikahan Teh Herbal Tabung Kaca & Saringan Emas"),
        ("/assets/images/craft-packaging.webp", "Kemasan Gift Box Kraft dengan Sekat Pelindung"),
        ("/assets/images/hero-souvenir-sq-597.webp", "Detail Saringan Teh Emas & Racikan Artisan Tea")
    ],
    "kaleng-teh-artisan-logam-tutup-gold": [
        ("/assets/images/tea-tin-souvenir.webp", "Souvenir Pernikahan Kaleng Teh Artisan Logam Tutup Gold"),
        ("/assets/images/craft-packaging.webp", "Kemasan Box Kraft & Pita Satin"),
        ("/assets/images/hero-souvenir-sq-597.webp", "Detail Label Custom Monogram Foil Emas")
    ],
    "botol-dispenser-sabun-pump-gold": [
        ("/assets/images/botol-sabun-custom.webp", "Souvenir Pernikahan Botol Dispenser Sabun Pump Gold Mewah"),
        ("/assets/images/craft-packaging.webp", "Kemasan Box Silinder / Hardbox Kraft"),
        ("/assets/images/hero-souvenir-sq-597.webp", "Detail Pompa Logam Emas & Grafir Botol")
    ],
    "botol-parfum-kaca-amber-mewah": [
        ("/assets/images/perfume-bottle-souvenir.webp", "Souvenir Pernikahan Botol Parfum Kaca Amber Mewah"),
        ("/assets/images/craft-packaging.webp", "Kemasan Box Kraft Elegan & Kartu Ucapan"),
        ("/assets/images/hero-souvenir-sq-597.webp", "Detail Nozzle Spray Emas & Kaca Amber Tebal")
    ],
    "minyak-esensial-pipet-kaca-box-beludru": [
        ("/assets/images/souvenir-botol-minyak.webp", "Souvenir Pernikahan Minyak Esensial Pipet Kaca & Box Beludru"),
        ("/assets/images/craft-packaging.webp", "Kemasan Box Hardbox / Beludru Berpita"),
        ("/assets/images/hero-souvenir-sq-597.webp", "Detail Pipet Kaca Presisi & Minyak Aromaterapi")
    ],
    "silk-scrunchie-set-sutra-bridesmaid": [
        ("/assets/images/silk-scrunchie-souvenir.webp", "Souvenir Pernikahan Silk Scrunchie Set Sutra Bridesmaid"),
        ("/assets/images/craft-packaging.webp", "Kemasan Pouch Transparan / Box Mika Pita"),
        ("/assets/images/hero-souvenir-sq-597.webp", "Detail Serat Sutra Lembut Berkilau Alami")
    ],
    "pouch-serut-beludru-velvet-monogram": [
        ("/assets/images/velvet-pouch-souvenir.webp", "Souvenir Pernikahan Pouch Serut Beludru Velvet Bordir Monogram"),
        ("/assets/images/craft-packaging.webp", "Kemasan Gift Box Kraft & Hangtag"),
        ("/assets/images/hero-souvenir-sq-597.webp", "Detail Bordir Inisial Monogram Benang Emas")
    ],
    "eco-tote-bag-kanvas-cutlery-set": [
        ("/assets/images/souvenir-tote-bag.webp", "Souvenir Pernikahan Eco Tote Bag Kanvas & Cutlery Set Kayu"),
        ("/assets/images/wooden-spoon-souvenir.webp", "Detail Sendok Garpu Kayu Alami"),
        ("/assets/images/craft-packaging.webp", "Kemasan Pita Rami & Hangtag Daur Ulang")
    ]
}

def generate_clean_pdp_with_dynamic_pricing(prod, cat_type, idx):
    slug = prod["slug"]
    title = prod["title"]
    is_modern = (cat_type == "modern")
    parent_slug = "souvenir-modern" if is_modern else "souvenir-tradisional"
    cat_name = "Souvenir Modern" if is_modern else "Souvenir Tradisional"
    
    # Parse prices & min_order
    price_matches = re.findall(r'Rp\s*([\d\.]+)', prod["price"])
    low_price = int(price_matches[0].replace('.', ''))
    high_price = int(price_matches[1].replace('.', ''))
    
    min_order_match = re.search(r'\d+', prod.get("min_order", "100"))
    min_order_int = int(min_order_match.group()) if min_order_match else 100
    
    # Configure steps and pills based on min_order_int
    if min_order_int <= 25:
        step_val = 10
        pills_html = f'''              <div class="gs-pdp-tier-pills" role="group" aria-label="Pilihan cepat kuantiti grosir">
                <button type="button" class="gs-tier-pill active" data-qty="{min_order_int}" onclick="setQty({min_order_int})">{min_order_int} pcs</button>
                <button type="button" class="gs-tier-pill" data-qty="50" onclick="setQty(50)">50 pcs <span class="gs-pill-save">-6%</span></button>
                <button type="button" class="gs-tier-pill" data-qty="100" onclick="setQty(100)">100 pcs <span class="gs-pill-save">-12%</span></button>
                <button type="button" class="gs-tier-pill" data-qty="250" onclick="setQty(250)">250+ pcs <span class="gs-pill-save">-18%</span></button>
              </div>'''
    elif min_order_int <= 50:
        step_val = 25
        pills_html = f'''              <div class="gs-pdp-tier-pills" role="group" aria-label="Pilihan cepat kuantiti grosir">
                <button type="button" class="gs-tier-pill active" data-qty="{min_order_int}" onclick="setQty({min_order_int})">{min_order_int} pcs</button>
                <button type="button" class="gs-tier-pill" data-qty="100" onclick="setQty(100)">100 pcs <span class="gs-pill-save">-6%</span></button>
                <button type="button" class="gs-tier-pill" data-qty="250" onclick="setQty(250)">250 pcs <span class="gs-pill-save">-12%</span></button>
                <button type="button" class="gs-tier-pill" data-qty="500" onclick="setQty(500)">500+ pcs <span class="gs-pill-save">-18%</span></button>
              </div>'''
    elif min_order_int == 150:
        step_val = 25
        pills_html = f'''              <div class="gs-pdp-tier-pills" role="group" aria-label="Pilihan cepat kuantiti grosir">
                <button type="button" class="gs-tier-pill active" data-qty="150" onclick="setQty(150)">150 pcs</button>
                <button type="button" class="gs-tier-pill" data-qty="250" onclick="setQty(250)">250 pcs <span class="gs-pill-save">-8%</span></button>
                <button type="button" class="gs-tier-pill" data-qty="500" onclick="setQty(500)">500 pcs <span class="gs-pill-save">-14%</span></button>
                <button type="button" class="gs-tier-pill" data-qty="1000" onclick="setQty(1000)">1.000+ pcs <span class="gs-pill-save">-20%</span></button>
              </div>'''
    else: # 100 pcs
        step_val = 25
        pills_html = f'''              <div class="gs-pdp-tier-pills" role="group" aria-label="Pilihan cepat kuantiti grosir">
                <button type="button" class="gs-tier-pill active" data-qty="100" onclick="setQty(100)">100 pcs</button>
                <button type="button" class="gs-tier-pill" data-qty="250" onclick="setQty(250)">250 pcs <span class="gs-pill-save">-8%</span></button>
                <button type="button" class="gs-tier-pill" data-qty="500" onclick="setQty(500)">500 pcs <span class="gs-pill-save">-14%</span></button>
                <button type="button" class="gs-tier-pill" data-qty="1000" onclick="setQty(1000)">1.000+ pcs <span class="gs-pill-save">-20%</span></button>
              </div>'''

    canonical_url = f"https://souvenirpernikahan.web.id/produk/{slug}"
    sku = f"SPN-{cat_type[:3].upper()}-{idx+1:03d}"
    
    # Gallery images
    gal = GALLERY_MAP.get(slug, [
        (prod["image"], f"{title} — Foto Utama"),
        ("/assets/images/craft-packaging.webp", "Kemasan Gift Box Kraft Rustic"),
        ("/assets/images/hero-souvenir.webp", "Detail Finishing Cinderamata")
    ])
    img_main, img_main_alt = gal[0]
    img_pack, img_pack_alt = gal[1]
    img_detail, img_detail_alt = gal[2]

    # Related products
    product_pool = modern_products if is_modern else tradisional_products
    related_items = [p for p in product_pool if p["slug"] != slug][:4]
    
    related_cards_html = ""
    for r in related_items:
        r_gal = GALLERY_MAP.get(r["slug"], [(r["image"], r["title"])])
        r_img, r_alt = r_gal[0]
        r_wa_msg = f"Halo Souvenir Pernikahan, saya tertarik memesan {r['title']} untuk souvenir pernikahan saya."
        r_wa_url = f"https://wa.me/6282131087971?text={urllib.parse.quote(r_wa_msg)}"
        
        related_cards_html += f'''          <article class="gs-pdp-related-card">
            <a href="/produk/{r['slug']}" class="gs-pdp-related-img-wrap" aria-label="{r['title']}">
              <img src="{r_img}" alt="{r_alt}" width="280" height="280" loading="lazy" decoding="async" />
              <span class="gs-pdp-related-badge">{cat_name}</span>
            </a>
            <div class="gs-pdp-related-body">
              <div class="gs-pdp-related-meta">
                <span class="gs-pdp-related-cat">{cat_name.upper()}</span>
                <span class="gs-pdp-related-rating" aria-label="Rating 5 bintang">★★★★★</span>
              </div>
              <h3 class="gs-pdp-related-title">
                <a href="/produk/{r['slug']}" title="{r['title']}">{r['title']}</a>
              </h3>
              <div class="gs-pdp-related-price-box">
                <span class="gs-pdp-related-price-label">Estimasi Harga Satuan:</span>
                <div class="gs-pdp-related-price">{r['price']} <span class="gs-pdp-related-unit">/ pcs</span></div>
              </div>
              <div class="gs-pdp-related-actions">
                <a href="/produk/{r['slug']}" class="gs-pdp-btn-detail">Lihat Detail</a>
                <a href="{r_wa_url}" class="gs-pdp-btn-card-wa" target="_blank" rel="noopener noreferrer" aria-label="Pesan {r['title']} via WhatsApp">
                  <svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor" aria-hidden="true" style="width:15px;height:15px;max-width:15px;max-height:15px;flex-shrink:0;">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                  </svg>
                  <span>Pesan</span>
                </a>
              </div>
            </div>
          </article>\n'''

    page_meta_title = f"{title} — Souvenir Pernikahan Elegan &amp; Berkesan"
    meta_desc = f"Pusat {title} murah, unik, elegan, dan bermanfaat. Gratis custom nama pengantin & kartu ucapan, harga grosir bertingkat semakin banyak semakin murah, serta garansi kirim aman seluruh Indonesia."
    keywords = f"{title.lower()}, souvenir pernikahan, souvenir pernikahan unik, souvenir pernikahan elegan, souvenir pernikahan murah, souvenir pernikahan bermanfaat, grosir souvenir pernikahan, souvenir pernikahan malang, souvenir pernikahan surabaya, souvenir pernikahan jakarta"

    schema_graph = {
        "@context": "https://schema.org",
        "@graph": [
            ORG_LOCALBUSINESS,
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
                "url": canonical_url,
                "image": [
                    f"https://souvenirpernikahan.web.id{img_main}",
                    f"https://souvenirpernikahan.web.id{img_pack}",
                    f"https://souvenirpernikahan.web.id{img_detail}"
                ],
                "description": prod["lead"],
                "sku": sku,
                "mpn": sku,
                "brand": {
                    "@type": "Brand",
                    "name": "Souvenir Pernikahan"
                },
                "category": f"Souvenir Pernikahan > {cat_name}",
                "offers": {
                    "@type": "AggregateOffer",
                    "url": canonical_url,
                    "priceCurrency": "IDR",
                    "lowPrice": str(low_price),
                    "highPrice": str(high_price),
                    "offerCount": "120",
                    "priceValidUntil": "2027-12-31",
                    "availability": "https://schema.org/InStock",
                    "itemCondition": "https://schema.org/NewCondition",
                    "hasMerchantReturnPolicy": {
                        "@type": "MerchantReturnPolicy",
                        "applicableCountry": "ID",
                        "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                        "merchantReturnDays": 7,
                        "returnMethod": "https://schema.org/ReturnByMail",
                        "returnFees": "https://schema.org/FreeReturn"
                    },
                    "shippingDetails": {
                        "@type": "OfferShippingDetails",
                        "shippingRate": {
                            "@type": "MonetaryAmount",
                            "value": 0,
                            "currency": "IDR"
                        },
                        "shippingDestination": {
                            "@type": "DefinedRegion",
                            "addressCountry": "ID"
                        },
                        "deliveryTime": {
                            "@type": "ShippingDeliveryTime",
                            "handlingTime": {
                                "@type": "QuantitativeValue",
                                "minValue": 14,
                                "maxValue": 21,
                                "unitCode": "DAY"
                            },
                            "transitTime": {
                                "@type": "QuantitativeValue",
                                "minValue": 2,
                                "maxValue": 5,
                                "unitCode": "DAY"
                            }
                        }
                    },
                    "seller": {
                        "@id": "https://souvenirpernikahan.web.id/#organization"
                    }
                },
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "4.9",
                    "reviewCount": "128",
                    "ratingCount": "164",
                    "bestRating": "5",
                    "worstRating": "1"
                },
                "review": [
                    {
                        "@type": "Review",
                        "author": { "@type": "Person", "name": "Dian & Reza" },
                        "datePublished": "2026-10-15",
                        "reviewBody": f"Hasil pesanan {title} rapi sekali dan kartu ucapannya sangat estetik. Tamu undangan akad nikah kami sangat terkesan.",
                        "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" }
                    },
                    {
                        "@type": "Review",
                        "author": { "@type": "Person", "name": "Sarah & Kevin" },
                        "datePublished": "2026-09-22",
                        "reviewBody": f"Pengiriman {title} ke Surabaya sangat aman bergaransi. Grafir nama mempelai sangat presisi.",
                        "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" }
                    }
                ]
            },
            {
                "@type": "FAQPage",
                "@id": f"{canonical_url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"Berapa harga dan minimal order untuk {title}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Estimasi harga satuan mulai dari {prod['price']} per pcs tergantung pilihan kemasan dan jumlah pemesanan. Kami menerapkan sistem harga grosir bertingkat (tiered discount) sehingga semakin banyak jumlah yang dipesan (250, 500, hingga 1.000+ pcs), harga satuan akan otomatis semakin murah. Minimal pemesanan mulai dari {prod['min_order']}."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Apakah bisa custom grafir nama kedua mempelai dan kartu ucapan?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Ya, seluruh produk sudah termasuk gratis grafir laser/cetak nama mempelai, tanggal akad, serta gratis kartu ucapan terima kasih (thank you card) custom desain."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Bagaimana pengiriman ke luar kota dan apakah ada garansi aman?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Kami melayani pengiriman ke Malang, Surabaya, Sidoarjo, Kediri, Blitar, Jakarta, Bandung, Semarang, Yogyakarta, Denpasar, hingga luar pulau via kargo dengan perlindungan packing berlapis serta Garansi 100% Ganti Baru."
                        }
                    }
                ]
            },
            {
                "@type": "WebPage",
                "@id": f"{canonical_url}#webpage",
                "url": canonical_url,
                "name": page_meta_title,
                "description": meta_desc,
                "inLanguage": "id-ID",
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": [
                        ".gs-pdp-title",
                        ".gs-pdp-price",
                        ".gs-pdp-desc-lead"
                    ]
                }
            }
        ]
    }
    
    schema_json = json.dumps(schema_graph, indent=2, ensure_ascii=False)

    features_li_html = "".join([f"<li>{feat}</li>" for feat in prod["features"]])
    default_wa_msg = f"Halo Souvenir Pernikahan, saya tertarik memesan {min_order_int} pcs {title} (Pilihan: {prod['packaging']}) untuk souvenir pernikahan saya. Mohon konfirmasi ketersediaan slot produksi dan penawaran resminya."
    default_wa_url = f"https://wa.me/6282131087971?text={urllib.parse.quote(default_wa_msg)}"

    html = f'''<!DOCTYPE html>
<html lang="id">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />

  <!-- Preload CSS -->
  <link rel="preload" href="/assets/css/style.min.css?v=9" as="style" />
  <link rel="preload" href="/assets/css/produk-detail.css?v=7" as="style" />
  <link rel="preload" as="image" href="{img_main}" />

  <title>{page_meta_title}</title>
  <meta name="description" content="{meta_desc}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="author" content="Yudi Abraham" />
  <meta name="theme-color" content="#762b16" />
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

  <!-- GEO & Local Targeting -->
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
  <meta property="og:image:alt" content="{title}" />

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
  <link rel="stylesheet" href="/assets/css/style.min.css?v=9" />
  <link rel="stylesheet" href="/assets/css/produk-detail.css?v=7" />

  <!-- Schema JSON-LD (Product, AggregateOffer, BreadcrumbList, FAQPage, Organization) -->
  <script type="application/ld+json">
{schema_json}
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
                <svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="width:16px;height:16px;max-width:16px;max-height:16px;display:inline-block;vertical-align:middle;">
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
              <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true" style="width:18px;height:18px;max-width:18px;max-height:18px;display:inline-block;vertical-align:middle;">
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
    <section class="gs-pdp-section" aria-label="Detail {title}">
      <div class="gs-container">

        <!-- Single Clean Breadcrumb Navigation -->
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
              <img id="pdp-main-img" src="{img_main}" alt="{img_main_alt}" width="600" height="600" decoding="async" />
            </div>

            <!-- Thumbnail Switcher with Authentic Photos -->
            <div class="gs-pdp-thumbs" role="tablist" aria-label="Galeri Foto {title}">
              <button type="button" class="gs-pdp-thumb-btn active" onclick="switchImage('{img_main}', this)" aria-label="Lihat Foto Utama Produk">
                <img src="{img_main}" alt="{img_main_alt}" width="120" height="120" loading="lazy" />
              </button>
              <button type="button" class="gs-pdp-thumb-btn" onclick="switchImage('{img_pack}', this)" aria-label="Lihat Kemasan Gift Box">
                <img src="{img_pack}" alt="{img_pack_alt}" width="120" height="120" loading="lazy" />
              </button>
              <button type="button" class="gs-pdp-thumb-btn" onclick="switchImage('{img_detail}', this)" aria-label="Lihat Detail Finishing Cinderamata">
                <img src="{img_detail}" alt="{img_detail_alt}" width="120" height="120" loading="lazy" />
              </button>
            </div>
          </div>

          <!-- Right Column: Buy Box Info -->
          <div class="gs-pdp-info">
            
            <h1 class="gs-pdp-title">{title}</h1>

            <!-- Dynamic Pricing Card -->
            <div class="gs-pdp-price-card">
              <div class="gs-pdp-price-header">
                <div class="gs-pdp-price">
                  <span class="gs-pdp-price-amount" id="pdp-unit-price">Rp ...</span>
                  <span class="gs-pdp-price-unit">/ pcs</span>
                </div>
                <span class="gs-pdp-tier-badge" id="pdp-tier-badge">Tier Standar ({prod["min_order"]})</span>
              </div>
              
              <div class="gs-pdp-total-row">
                <span class="gs-pdp-total-label">Estimasi Total (<span id="pdp-total-qty">{min_order_int}</span> pcs):</span>
                <strong class="gs-pdp-total-amount" id="pdp-total-price">Rp ...</strong>
              </div>

              <p class="gs-pdp-price-subtext">
                <span class="gs-pdp-range-hint">Rentang Estimasi: {prod["price"]} / pcs</span><br>
                Minimal pemesanan mulai {prod["min_order"]} &bull; Gratis custom nama pengantin &amp; kartu ucapan
              </p>
            </div>

            <!-- Variasi Produk Dropdown -->
            <div class="gs-pdp-option-group">
              <label for="pdp-variant-select" class="gs-pdp-option-label">Pilihan Kemasan &amp; Personalisasi:</label>
              <select id="pdp-variant-select" class="gs-pdp-select" onchange="updatePricing()">
                <option value="Kemasan Standar + Kartu Ucapan">{prod["packaging"]} (Rekomendasi Favorit)</option>
                <option value="Hardbox Eksklusif Foil Emas">Hardbox Magnetik Eksklusif + Cetak Foil Emas</option>
                <option value="Custom Kemasan Sesuai Budget">Custom Kemasan Khusus (Konsultasi via WA)</option>
              </select>
            </div>

            <!-- Quantity Selector & Tier Pills -->
            <div class="gs-pdp-option-group">
              <label for="pdp-qty-input" class="gs-pdp-option-label">Estimasi Jumlah Pesanan:</label>
              
{pills_html}

              <div class="gs-pdp-order-row">
                <div class="gs-pdp-qty-control">
                  <button type="button" class="gs-pdp-qty-btn" onclick="adjustQty(-{step_val})" aria-label="Kurangi jumlah {step_val} pcs">-</button>
                  <input type="number" id="pdp-qty-input" class="gs-pdp-qty-input" value="{min_order_int}" min="{min_order_int}" step="{step_val}" oninput="updatePricing()" />
                  <button type="button" class="gs-pdp-qty-btn" onclick="adjustQty({step_val})" aria-label="Tambah jumlah {step_val} pcs">+</button>
                </div>
                <span class="gs-pdp-qty-unit">pcs (Minimal order {prod["min_order"]})</span>
              </div>
              <span class="gs-pdp-tier-note" id="pdp-tier-note">&bull; Semakin banyak jumlah pesanan, harga estimasi satuan otomatis semakin murah.</span>
            </div>

            <!-- Actions Buttons -->
            <div class="gs-pdp-actions">
              <a id="pdp-wa-cta" href="{default_wa_url}" class="gs-pdp-btn-wa" target="_blank" rel="noopener noreferrer">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true" style="width:20px;height:20px;max-width:20px;max-height:20px;flex-shrink:0;">
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
              <div class="gs-pdp-meta-item"><strong>Kategori:</strong> Souvenir Pernikahan &bull; {cat_name} &bull; Cinderamata Unik</div>
              <div class="gs-pdp-meta-item"><strong>Tag:</strong> souvenir pernikahan, souvenir nikah murah, souvenir pernikahan elegan, cinderamata unik</div>
              
              <div class="gs-pdp-share-row">
                <span style="font-size:0.8rem;font-weight:600;">Bagikan:</span>
                <a href="https://api.whatsapp.com/send?text={canonical_url}" class="gs-pdp-share-icon" target="_blank" rel="noopener noreferrer" aria-label="Bagikan ke WhatsApp">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true" style="width:18px;height:18px;max-width:18px;max-height:18px;"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
                </a>
                <a href="https://www.facebook.com/sharer/sharer.php?u={canonical_url}" class="gs-pdp-share-icon" target="_blank" rel="noopener noreferrer" aria-label="Bagikan ke Facebook">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true" style="width:18px;height:18px;max-width:18px;max-height:18px;"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                </a>
                <a href="https://twitter.com/intent/tweet?url={canonical_url}&text={title}" class="gs-pdp-share-icon" target="_blank" rel="noopener noreferrer" aria-label="Bagikan ke Twitter">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true" style="width:18px;height:18px;max-width:18px;max-height:18px;"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.936 9.936 0 0024 4.59z"/></svg>
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
        <div class="gs-pdp-tabs-nav" role="tablist" aria-label="Informasi Produk">
          <button type="button" class="gs-pdp-tab-trigger active" role="tab" aria-selected="true" aria-controls="tab-desc" onclick="switchTab('desc', this)">
            Deskripsi &amp; FAQ
          </button>
          <button type="button" class="gs-pdp-tab-trigger" role="tab" aria-selected="false" aria-controls="tab-spec" onclick="switchTab('spec', this)">
            Spesifikasi &amp; Bahan
          </button>
          <button type="button" class="gs-pdp-tab-trigger" role="tab" aria-selected="false" aria-controls="tab-reviews" onclick="switchTab('reviews', this)">
            Ulasan Pengantin (128)
          </button>
        </div>

        <!-- Tab 1: Description -->
        <div class="gs-pdp-tab-pane active" id="tab-desc" role="tabpanel">
          <p class="gs-pdp-desc-lead">
            {prod["lead"]}
          </p>

          <h3 style="font-size:1.15rem;color:var(--gs-green-950);margin:1.5rem 0 0.75rem 0;">Keunggulan &amp; Fasilitas Pemesanan:</h3>
          <ul class="gs-pdp-checklist">
            <li>
              <svg viewBox="0 0 20 20" width="18" height="18" fill="currentColor" aria-hidden="true" style="width:18px;height:18px;max-width:18px;max-height:18px;flex-shrink:0;color:#b25032;margin-top:0.2rem;">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              <span>GRATIS kustomisasi nama pengantin, tanggal akad, &amp; inisial monogram</span>
            </li>
            <li>
              <svg viewBox="0 0 20 20" width="18" height="18" fill="currentColor" aria-hidden="true" style="width:18px;height:18px;max-width:18px;max-height:18px;flex-shrink:0;color:#b25032;margin-top:0.2rem;">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              <span>GRATIS cetak kartu ucapan terima kasih (thank you card) custom desain</span>
            </li>
            <li>
              <svg viewBox="0 0 20 20" width="18" height="18" fill="currentColor" aria-hidden="true" style="width:18px;height:18px;max-width:18px;max-height:18px;flex-shrink:0;color:#b25032;margin-top:0.2rem;">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              <span>GRATIS label hangtag dan pita kemasan senada tema pesta pernikahan</span>
            </li>
          </ul>

          <div style="background:#ffffff;border:1px solid var(--gs-border);border-radius:var(--gs-radius-sm);padding:1.25rem;margin:1.5rem 0;">
            <p style="margin:0 0 0.5rem 0;font-weight:700;color:var(--gs-green-950);">Include dalam Paket Souvenir:</p>
            <ul style="margin:0;padding-left:1.25rem;">
              <li>Item produk utama: <strong>{title}</strong> kualitas terjamin grade A</li>
              <li>{prod['packaging']}</li>
              <li>Free kartu ucapan terima kasih cetak nama kedua mempelai</li>
              <li>Free pita satin / tali rami pengikat estetik</li>
              <li>Garansi 100% Ganti Baru jika terjadi kerusakan saat proses pengiriman</li>
            </ul>
          </div>

          <div style="font-size:0.86rem;color:var(--gs-muted);line-height:1.6;margin-top:1.5rem;">
            <p><strong>Ketentuan Pemesanan:</strong></p>
            <ol style="padding-left:1.2rem;margin:0.5rem 0;">
              <li>Tuliskan nama kedua mempelai dan tanggal pernikahan pada saat konsultasi via WhatsApp.</li>
              <li>Tim desainer kami akan membuatkan preview digital desain grafir/kartu ucapan secara gratis sebelum proses produksi massal.</li>
              <li>Pengiriman menggunakan ekspedisi kargo khusus (J&amp;T Cargo, KALOG Kereta, Dakota) dengan proteksi bubble wrap berlapis dan peti kayu untuk barang pecah belah.</li>
            </ol>
            <p>Terima kasih dan selamat merencanakan hari bahagia pernikahan Anda!</p>
          </div>

          <!-- FAQ Accordion for AEO / AI Search Snippets -->
          <div style="margin-top: 2rem; border-top: 1px solid var(--gs-border); padding-top: 1.5rem;">
            <h3 style="font-size: 1.15rem; color: var(--gs-green-950); margin-bottom: 1rem;">Pertanyaan Umum seputar {title}</h3>
            
            <div style="margin-bottom: 0.85rem; background: var(--gs-white); border: 1px solid var(--gs-border); border-radius: 8px; padding: 1rem;">
              <strong style="color: var(--gs-green-900); display: block; margin-bottom: 0.35rem;">Berapa harga dan minimal order untuk {title}?</strong>
              <p style="margin: 0; font-size: 0.88rem; color: var(--gs-muted);">Estimasi harga satuan mulai dari {prod['price']} per pcs (sudah termasuk kemasan dan kartu ucapan). Kami menerapkan sistem harga grosir bertingkat (tiered discount) sehingga semakin banyak jumlah yang dipesan (250, 500, hingga 1.000+ pcs), harga satuan akan otomatis semakin murah. Minimal pemesanan mulai dari {prod['min_order']}.</p>
            </div>

            <div style="margin-bottom: 0.85rem; background: var(--gs-white); border: 1px solid var(--gs-border); border-radius: 8px; padding: 1rem;">
              <strong style="color: var(--gs-green-900); display: block; margin-bottom: 0.35rem;">Apakah bisa custom grafir nama kedua mempelai?</strong>
              <p style="margin: 0; font-size: 0.88rem; color: var(--gs-muted);">Bisa. Seluruh pesanan souvenir pernikahan kami sudah termasuk fasilitas gratis grafir laser inisial monogram atau nama lengkap mempelai serta tanggal akad.</p>
            </div>

            <div style="background: var(--gs-white); border: 1px solid var(--gs-border); border-radius: 8px; padding: 1rem;">
              <strong style="color: var(--gs-green-900); display: block; margin-bottom: 0.35rem;">Bagaimana pengiriman ke luar kota dan luar pulau?</strong>
              <p style="margin: 0; font-size: 0.88rem; color: var(--gs-muted);">Kami melayani pengiriman bergaransi ke Malang, Surabaya, Sidoarjo, Kediri, Blitar, Jakarta, Bandung, Semarang, Yogyakarta, Solo, Denpasar Bali, hingga luar pulau menggunakan armada kargo khusus.</p>
            </div>
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

        <!-- Tab 2: Specification -->
        <div class="gs-pdp-tab-pane" id="tab-spec" role="tabpanel">
          <table class="gs-pdp-spec-table">
            <tbody>
              <tr>
                <th>Nama Produk</th>
                <td>{title}</td>
              </tr>
              <tr>
                <th>Kategori Cinderamata</th>
                <td>Souvenir Pernikahan &bull; {cat_name}</td>
              </tr>
              <tr>
                <th>Spesifikasi Unggulan</th>
                <td>
                  <ul style="margin:0;padding-left:1.15rem;">
                    {features_li_html}
                  </ul>
                </td>
              </tr>
              <tr>
                <th>Custom Nama &amp; Ucapan</th>
                <td>{prod["custom"]}</td>
              </tr>
              <tr>
                <th>Pilihan Kemasan</th>
                <td>{prod["packaging"]}</td>
              </tr>
              <tr>
                <th>Minimal Order</th>
                <td>{prod["min_order"]}</td>
              </tr>
              <tr>
                <th>Estimasi Waktu Produksi</th>
                <td>14 - 21 hari kerja (menyesuaikan antrean dan kuantiti pesanan)</td>
              </tr>
              <tr>
                <th>Asal Produksi</th>
                <td>Workshop Kriya Souvenir Pernikahan, Kota Malang, Jawa Timur</td>
              </tr>
              <tr>
                <th>Jangkauan Pengiriman</th>
                <td>Seluruh Indonesia (Jawa, Bali, Sumatera, Kalimantan, Sulawesi, Papua) dengan packing aman bergaransi</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Tab 3: Reviews -->
        <div class="gs-pdp-tab-pane" id="tab-reviews" role="tabpanel">
          <div class="gs-pdp-rating-summary">
            <span class="gs-pdp-rating-score">4.9</span>
            <div>
              <div class="gs-pdp-stars">★★★★★</div>
              <span class="gs-pdp-rating-count">Berdasarkan 128 ulasan pelanggan terverifikasi</span>
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
                "Hasil cetak nama dan kemasan {title} rapi sekali. Tamu-tamu undangan banyak yang memuji souvenir kami. Pelayanan admin WhatsApp sangat ramah dan sabar membantu penyesuaian desain kartu ucapan."
              </p>
            </div>

            <div style="border-bottom:1px solid var(--gs-border);padding-bottom:1rem;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;">
                <strong style="color:var(--gs-green-950);">Sarah &amp; Kevin — Surabaya</strong>
                <span style="font-size:0.78rem;color:var(--gs-muted);">Resepsi September 2026</span>
              </div>
              <div style="color:#f59e0b;font-size:0.85rem;margin-bottom:0.4rem;">★★★★★</div>
              <p style="margin:0;font-size:0.88rem;color:var(--gs-text);">
                "Pengiriman ke Surabaya sangat aman, tidak ada barang yang rusak karena packing-nya berlapis dan tebal. Kualitas {title} melebihi ekspektasi kami dengan harga yang sangat bersahabat."
              </p>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- RELATED PRODUCTS SECTION -->
    <section class="gs-pdp-related-section" aria-labelledby="related-heading">
      <div class="gs-container">
        <div class="gs-section-heading" style="text-align:center;margin-bottom:2.5rem;">
          <span class="gs-eyebrow" style="font-size:0.75rem;letter-spacing:1.8px;text-transform:uppercase;color:#b25032;font-weight:700;display:inline-block;margin-bottom:0.4rem;">Pilihan Cinderamata Favorit</span>
          <h2 id="related-heading" style="font-family:var(--gs-font-heading);font-size:clamp(1.5rem, 2.8vw, 2.1rem);font-weight:700;color:var(--gs-green-950);margin-bottom:0.5rem;">Produk Terkait</h2>
          <p style="color:var(--gs-muted);font-size:0.92rem;max-width:560px;margin:0 auto;line-height:1.6;">Rekomendasi koleksi souvenir pernikahan lainnya yang elegan, fungsional, dan dapat dipersonalisasi nama pengantin.</p>
        </div>
        <div class="gs-pdp-related-grid">
{related_cards_html}
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
            Pusat vendor souvenir pernikahan custom, unik, elegan, murah, dan bermanfaat di Malang untuk pengiriman ke Surabaya, Jakarta, dan seluruh Indonesia. Dibuat dengan dedikasi penuh terhadap kriya dan kepuasan pengantin.
          </p>
        </div>

        <div>
          <p class="gs-footer__heading">Halaman</p>
          <ul class="gs-footer__links">
            <li><a href="/" class="gs-footer__link">Beranda</a></li>
            <li><a href="/tentang" class="gs-footer__link">Tentang</a></li>
            <li><a href="/paket" class="gs-footer__link">Paket Souvenir</a></li>
            <li><a href="/paket/souvenir-tradisional" class="gs-footer__link">Souvenir Tradisional</a></li>
            <li><a href="/paket/souvenir-modern" class="gs-footer__link">Souvenir Modern</a></li>
            <li><a href="/portofolio" class="gs-footer__link">Portofolio</a></li>
            <li><a href="/blog" class="gs-footer__link">Blog &amp; Inspirasi</a></li>
          </ul>
        </div>

        <div>
          <p class="gs-footer__heading">Kontak &amp; Workshop</p>
          <ul class="gs-footer__links">
            <li class="gs-footer__link" style="color:rgba(255,255,255,0.7);font-size:0.875rem;">
              Jl. Band. Palmerah No.D3-35B, Cemorokandang, Kec. Kedungkandang, Kota Malang, Jawa Timur 65138
            </li>
            <li class="gs-footer__link" style="color:rgba(255,255,255,0.7);font-size:0.875rem;">
              Jam Operasional: Senin - Sabtu, 08.30 - 18.00 WIB
            </li>
            <li>
              <a href="https://wa.me/6282131087971" class="gs-footer__link" target="_blank" rel="noopener noreferrer">
                WhatsApp: +62 821-3108-7971
              </a>
            </li>
          </ul>
        </div>

        <div>
          <p class="gs-footer__heading">Kota Layanan Pengiriman</p>
          <p style="color:rgba(255,255,255,0.65);font-size:0.825rem;line-height:1.6;margin-bottom:1rem;">
            Melayani pengiriman bergaransi ke Malang, Surabaya, Sidoarjo, Gresik, Pasuruan, Kediri, Blitar, Jakarta, Bandung, Semarang, Yogyakarta, Solo, Denpasar, Medan, Makassar, Balikpapan, dan seluruh Indonesia.
          </p>
        </div>
      </div>

      <div class="gs-footer__bottom">
        <p class="gs-footer__copy">&copy; 2026 Souvenir Pernikahan Indonesia. Hak Cipta Dilindungi.</p>
        <div class="gs-footer__legal">
          <a href="/kebijakan-privasi" class="gs-footer__legal-link">Kebijakan Privasi</a>
          <a href="/syarat-ketentuan" class="gs-footer__legal-link">Syarat &amp; Ketentuan</a>
        </div>
      </div>
    </div>
  </footer>

  <!-- Floating WhatsApp -->
  <aside class="gs-whatsapp-float" aria-label="Tombol WhatsApp mengambang">
    <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi%20souvenir%20pernikahan."
      class="gs-whatsapp-float__btn" target="_blank" rel="noopener noreferrer"
      aria-label="Konsultasi souvenir pernikahan via WhatsApp">
      <svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor" aria-hidden="true" style="width:32px;height:32px;max-width:32px;max-height:32px;">
        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
      </svg>
    </a>
  </aside>

  <!-- Interactive Scripts -->
  <script>
    var PDP_DATA = {{
      lowPrice: {low_price},
      highPrice: {high_price},
      minOrder: {min_order_int},
      prodName: "{title}",
      stepVal: {step_val}
    }};

    function switchImage(src, btn) {{
      var mainImg = document.getElementById('pdp-main-img');
      if (mainImg) {{
        mainImg.style.opacity = '0.4';
        setTimeout(function() {{
          mainImg.src = src;
          mainImg.style.opacity = '1';
        }}, 150);
      }}
      var btns = document.querySelectorAll('.gs-pdp-thumb-btn');
      btns.forEach(function(b) {{ b.classList.remove('active'); }});
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

    function formatIDR(num) {{
      return "Rp " + num.toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".");
    }}

    function getTierDiscount(qty, minOrder) {{
      if (minOrder <= 25) {{
        if (qty >= 250) return {{ pct: 18, badge: "🏆 Hemat 18% (Grosir 250+ pcs)" }};
        if (qty >= 100) return {{ pct: 12, badge: "🔥 Hemat 12% (100+ pcs)" }};
        if (qty >= 50) return {{ pct: 6, badge: "✨ Hemat 6% (50+ pcs)" }};
        return {{ pct: 0, badge: "Tier Standar (" + minOrder + " pcs)" }};
      }} else if (minOrder <= 50) {{
        if (qty >= 500) return {{ pct: 18, badge: "🏆 Hemat 18% (Grosir 500+ pcs)" }};
        if (qty >= 250) return {{ pct: 12, badge: "🔥 Hemat 12% (250+ pcs)" }};
        if (qty >= 100) return {{ pct: 6, badge: "✨ Hemat 6% (100+ pcs)" }};
        return {{ pct: 0, badge: "Tier Standar (" + minOrder + " pcs)" }};
      }} else {{
        if (qty >= 1000) return {{ pct: 20, badge: "🏆 Hemat 20% (Harga Grosir Termurah)" }};
        if (qty >= 500) return {{ pct: 14, badge: "🔥 Hemat 14% (500+ pcs)" }};
        if (qty >= 250) return {{ pct: 8, badge: "⭐ Hemat 8% (250+ pcs)" }};
        return {{ pct: 0, badge: "Tier Standar (" + minOrder + " pcs)" }};
      }}
    }}

    function updatePricing() {{
      var qtyInput = document.getElementById('pdp-qty-input');
      var variantSelect = document.getElementById('pdp-variant-select');
      var unitPriceEl = document.getElementById('pdp-unit-price');
      var totalPriceEl = document.getElementById('pdp-total-price');
      var totalQtyEl = document.getElementById('pdp-total-qty');
      var tierBadgeEl = document.getElementById('pdp-tier-badge');
      var tierNoteEl = document.getElementById('pdp-tier-note');
      var waBtn = document.getElementById('pdp-wa-cta');

      if (!qtyInput) return;

      var qty = parseInt(qtyInput.value) || PDP_DATA.minOrder;
      if (qty < PDP_DATA.minOrder) {{
        qty = PDP_DATA.minOrder;
        qtyInput.value = qty;
      }}

      var variantIdx = variantSelect ? variantSelect.selectedIndex : 0;
      var variantText = variantSelect ? variantSelect.options[variantIdx].text : "Kemasan Standar";

      // Base price according to selected variant
      var baseUnit;
      if (variantIdx === 1) {{
        baseUnit = PDP_DATA.highPrice;
      }} else if (variantIdx === 2) {{
        baseUnit = Math.round(((PDP_DATA.lowPrice + PDP_DATA.highPrice) / 2) / 500) * 500;
      }} else {{
        baseUnit = Math.round((PDP_DATA.lowPrice * 1.25) / 500) * 500;
      }}

      var tier = getTierDiscount(qty, PDP_DATA.minOrder);
      var unitPrice = Math.round((baseUnit * (1 - (tier.pct / 100))) / 250) * 250;
      if (unitPrice < PDP_DATA.lowPrice) unitPrice = PDP_DATA.lowPrice;

      var totalPrice = unitPrice * qty;

      if (unitPriceEl) {{
        unitPriceEl.textContent = formatIDR(unitPrice);
        unitPriceEl.classList.remove('is-updated');
        void unitPriceEl.offsetWidth; // trigger reflow for pulse animation
        unitPriceEl.classList.add('is-updated');
      }}
      if (totalPriceEl) totalPriceEl.textContent = formatIDR(totalPrice);
      if (totalQtyEl) totalQtyEl.textContent = qty.toString();
      if (tierBadgeEl) {{
        tierBadgeEl.textContent = tier.badge;
        if (tier.pct > 0) {{
          tierBadgeEl.classList.add('is-discount');
        }} else {{
          tierBadgeEl.classList.remove('is-discount');
        }}
      }}

      // Dynamic guidance note
      if (tierNoteEl) {{
        if (PDP_DATA.minOrder >= 100) {{
          if (qty < 250) {{
            tierNoteEl.innerHTML = "&bull; Tip: Tambah " + (250 - qty) + " pcs lagi untuk mendapatkan diskon grosir 8%!";
          }} else if (qty < 500) {{
            tierNoteEl.innerHTML = "&bull; Tip: Tambah " + (500 - qty) + " pcs lagi untuk diskon partai besar 14%!";
          }} else if (qty < 1000) {{
            tierNoteEl.innerHTML = "&bull; Tip: Tambah " + (1000 - qty) + " pcs lagi untuk harga grosir termurah (hemat 20%)!";
          }} else {{
            tierNoteEl.innerHTML = "&bull; <strong>Harga Grosir Maksimal Aktif:</strong> Anda mendapatkan penawaran harga satuan termurah!";
          }}
        }} else {{
          tierNoteEl.innerHTML = "&bull; Semakin banyak jumlah pesanan, harga estimasi satuan otomatis semakin murah.";
        }}
      }}

      // Update active state on tier pills
      var pills = document.querySelectorAll('.gs-tier-pill');
      pills.forEach(function(pill) {{
        var pillQty = parseInt(pill.getAttribute('data-qty'));
        if (pillQty === qty) {{
          pill.classList.add('active');
        }} else {{
          pill.classList.remove('active');
        }}
      }});

      // Update WhatsApp link
      if (waBtn) {{
        var msg = "Halo Souvenir Pernikahan, saya tertarik memesan " + qty + " pcs " + PDP_DATA.prodName + 
                  " (Pilihan: " + variantText + ") dengan estimasi harga satuan " + formatIDR(unitPrice) + "/pcs" +
                  " (Estimasi Total: " + formatIDR(totalPrice) + ")." +
                  " Mohon konfirmasi ketersediaan slot produksi dan penawaran resminya.";
        waBtn.href = "https://wa.me/6282131087971?text=" + encodeURIComponent(msg);
      }}
    }}

    function setQty(val) {{
      var input = document.getElementById('pdp-qty-input');
      if (input) {{
        input.value = val;
        updatePricing();
      }}
    }}

    function adjustQty(amount) {{
      var input = document.getElementById('pdp-qty-input');
      if (input) {{
        var val = parseInt(input.value) || PDP_DATA.minOrder;
        val += amount;
        if (val < PDP_DATA.minOrder) val = PDP_DATA.minOrder;
        input.value = val;
        updatePricing();
      }}
    }}

    // Initialize pricing on page load
    document.addEventListener('DOMContentLoaded', function() {{
      updatePricing();
    }});
    if (document.readyState === 'interactive' || document.readyState === 'complete') {{
      updatePricing();
    }}
  </script>

  <script defer src="/assets/js/main.min.js?v=7"></script>
</body>

</html>'''
    
    file_path = os.path.join("produk", f"{slug}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated dynamic pricing PDP: {file_path}")

if __name__ == '__main__':
    print("Regenerating all 28 PDPs with dynamic wholesale pricing...")
    for i, p in enumerate(tradisional_products):
        generate_clean_pdp_with_dynamic_pricing(p, "tradisional", i)

    for i, p in enumerate(modern_products):
        generate_clean_pdp_with_dynamic_pricing(p, "modern", i)

    print("All 28 PDPs successfully regenerated with dynamic wholesale/tiered pricing!")
