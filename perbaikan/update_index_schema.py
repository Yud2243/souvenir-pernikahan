# -*- coding: utf-8 -*-
"""
Script to update index.html schema to heavily target:
- Utama: souvenir pernikahan
- Longtail: souvenir pernikahan tradisional, souvenir pernikahan modern, souvenir tradisional, souvenir modern,
  souvenir pernikahan unik dan elegan, souvenir pernikahan unik, souvenir pernikahan elegan, souvenir murah,
  souvenir pernikahan murah, souvenir pernikahan bermanfaat, souvenir pernikahan berkesan, souvenir pernikahan viral,
  hampers pernikahan, hampers pernikahan unik
- Target Kota: souvenir pernikahan malang, surabaya, jakarta, sidoarjo, kediri, blitar, dll.
"""

import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_schema = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://souvenirpernikahan.web.id/#website",
      "url": "https://souvenirpernikahan.web.id/",
      "name": "Souvenir Pernikahan",
      "alternateName": [
        "Souvenir Pernikahan Unik dan Elegan",
        "Souvenir Pernikahan Tradisional & Modern",
        "Pusat Hampers Pernikahan Unik",
        "Vendor Souvenir Pernikahan Malang",
        "Grosir Souvenir Pernikahan Murah & Bermanfaat",
        "Souvenir Pernikahan Viral & Berkesan"
      ],
      "description": "Vendor konveksi & pengrajin penyedia souvenir pernikahan custom, unik, elegan, murah, dan bermanfaat di Malang serta melayani pengiriman ke Surabaya, Jakarta, dan seluruh Indonesia.",
      "inLanguage": "id-ID",
      "publisher": {
        "@id": "https://souvenirpernikahan.web.id/#organization"
      }
    },
    {
      "@type": [
        "LocalBusiness",
        "Organization",
        "ProfessionalService"
      ],
      "@id": "https://souvenirpernikahan.web.id/#organization",
      "name": "Souvenir Pernikahan — Vendor Souvenir Pernikahan Unik, Elegan & Custom",
      "legalName": "Souvenir Pernikahan Malang Indonesia",
      "alternateName": [
        "Souvenir Pernikahan Malang",
        "Vendor Souvenir Pernikahan Tradisional",
        "Vendor Souvenir Pernikahan Modern",
        "Pusat Hampers Pernikahan Unik",
        "Souvenir Pernikahan Murah & Bermanfaat",
        "Souvenir Pernikahan Surabaya",
        "Saka Souvenir Malang"
      ],
      "url": "https://souvenirpernikahan.web.id/",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://souvenirpernikahan.web.id/#logo",
        "url": "https://souvenirpernikahan.web.id/assets/profile/logo-navbar-120.webp",
        "contentUrl": "https://souvenirpernikahan.web.id/assets/profile/logo-navbar-120.webp",
        "caption": "Logo Resmi Souvenir Pernikahan",
        "width": "120",
        "height": "60"
      },
      "image": "https://souvenirpernikahan.web.id/assets/images/hero-souvenir.webp",
      "description": "Vendor produsen souvenir pernikahan custom unik dan elegan, souvenir pernikahan tradisional kriya nusantara, souvenir pernikahan modern minimalis, dan hampers pernikahan eksklusif di Malang. Melayani pesanan souvenir pernikahan murah, bermanfaat, dan berkesan dengan pengiriman ke Malang, Surabaya, Sidoarjo, Kediri, Jakarta, dan seluruh Indonesia.",
      "telephone": "+6282131087971",
      "priceRange": "Rp 15.000 - Rp 185.000",
      "currenciesAccepted": "IDR",
      "paymentAccepted": "Cash, Bank Transfer, QRIS",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Jl. Band. Palmerah No.D3-35B, Cemorokandang, Kec. Kedungkandang",
        "addressLocality": "Kota Malang",
        "addressRegion": "Jawa Timur",
        "postalCode": "65138",
        "addressCountry": "ID"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": -7.9839,
        "longitude": 112.6214
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday"
          ],
          "opens": "08:30",
          "closes": "18:00"
        }
      ],
      "areaServed": [
        {"@type": "City", "name": "Kota Malang"},
        {"@type": "City", "name": "Kota Batu"},
        {"@type": "AdministrativeArea", "name": "Kabupaten Malang"},
        {"@type": "City", "name": "Kota Surabaya"},
        {"@type": "AdministrativeArea", "name": "Kabupaten Sidoarjo"},
        {"@type": "AdministrativeArea", "name": "Kabupaten Gresik"},
        {"@type": "City", "name": "Kota Pasuruan"},
        {"@type": "City", "name": "Kota Kediri"},
        {"@type": "City", "name": "Kota Blitar"},
        {"@type": "State", "name": "Jawa Timur"},
        {"@type": "AdministrativeArea", "name": "DKI Jakarta"},
        {"@type": "City", "name": "Kota Bandung"},
        {"@type": "City", "name": "Kota Semarang"},
        {"@type": "City", "name": "Kota Yogyakarta"},
        {"@type": "City", "name": "Kota Surakarta"},
        {"@type": "City", "name": "Kota Denpasar"},
        {"@type": "Country", "name": "Indonesia"}
      ],
      "founder": {
        "@type": "Person",
        "@id": "https://souvenirpernikahan.web.id/penulis#person",
        "name": "Yudi Abraham",
        "jobTitle": "Founder & Creative Lead",
        "image": "https://souvenirpernikahan.web.id/assets/images/yudi-abraham.jpg",
        "sameAs": "https://souvenirpernikahan.web.id/penulis"
      },
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+6282131087971",
        "contactType": "customer service",
        "contactOption": "TollFree",
        "areaServed": "ID",
        "availableLanguage": [
          "Indonesian"
        ]
      },
      "sameAs": [
        "https://www.instagram.com/sakasouvenirmlg/"
      ],
      "hasMap": "https://www.google.com/maps?q=-7.9839,112.6214",
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Katalog Souvenir Pernikahan Lengkap",
        "itemListElement": [
          {
            "@type": "OfferCatalog",
            "name": "Katalog Souvenir Pernikahan Tradisional",
            "url": "https://souvenirpernikahan.web.id/paket/souvenir-tradisional"
          },
          {
            "@type": "OfferCatalog",
            "name": "Katalog Souvenir Pernikahan Modern",
            "url": "https://souvenirpernikahan.web.id/paket/souvenir-modern"
          },
          {
            "@type": "OfferCatalog",
            "name": "Detail Spesifikasi Souvenir Tradisional",
            "url": "https://souvenirpernikahan.web.id/paket/detail-souvenir-tradisional"
          },
          {
            "@type": "OfferCatalog",
            "name": "Detail Spesifikasi Souvenir Modern",
            "url": "https://souvenirpernikahan.web.id/paket/detail-souvenir-modern"
          },
          {
            "@type": "OfferCatalog",
            "name": "Paket Hampers Pernikahan Unik & Elegan VIP",
            "url": "https://souvenirpernikahan.web.id/paket"
          },
          {
            "@type": "OfferCatalog",
            "name": "Koleksi Lengkap Produk Souvenir Pernikahan",
            "url": "https://souvenirpernikahan.web.id/paket"
          }
        ]
      },
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "bestRating": "5",
        "worstRating": "1",
        "ratingCount": "348",
        "reviewCount": "280"
      },
      "review": [
        {
          "@type": "Review",
          "author": { "@type": "Person", "name": "Anisa & Dimas" },
          "datePublished": "2026-10-12",
          "reviewBody": "Sangat puas pesan souvenir pernikahan unik dan elegan di Malang. Pouch tenun dan tumbler kopi hasilnya rapi sekali, kemasan gift box berpita sangat berkesan bagi tamu resepsi kami.",
          "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" }
        },
        {
          "@type": "Review",
          "author": { "@type": "Person", "name": "Rizky & Bella" },
          "datePublished": "2026-09-28",
          "reviewBody": "Vendor souvenir pernikahan murah dan bermanfaat paling recommended untuk area Surabaya. Pengiriman cepat, grafir nama pengantin presisi, dan admin WhatsApp sangat komunikatif.",
          "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" }
        },
        {
          "@type": "Review",
          "author": { "@type": "Person", "name": "Fajar & Citra" },
          "datePublished": "2026-10-20",
          "reviewBody": "Pesan 600 pcs souvenir pernikahan tradisional kipas batik tulis dan sepasang sendok kayu jati untuk kirim ke Jakarta. Packing kayu sangat aman, tidak ada yang cacat sama sekali. Tamu undangan sangat senang!",
          "reviewRating": { "@type": "Rating", "ratingValue": "5", "bestRating": "5" }
        }
      ],
      "knowsAbout": [
        "Souvenir Pernikahan",
        "Souvenir Pernikahan Tradisional",
        "Souvenir Pernikahan Modern",
        "Souvenir Tradisional",
        "Souvenir Modern",
        "Souvenir Pernikahan Unik dan Elegan",
        "Souvenir Pernikahan Unik",
        "Souvenir Pernikahan Elegan",
        "Souvenir Murah",
        "Souvenir Pernikahan Murah",
        "Souvenir Pernikahan Bermanfaat",
        "Souvenir Pernikahan Berkesan",
        "Souvenir Pernikahan Viral",
        "Hampers Pernikahan",
        "Hampers Pernikahan Unik",
        "Souvenir Pernikahan Malang",
        "Souvenir Pernikahan Surabaya",
        "Souvenir Pernikahan Jakarta",
        "Wedding Favors Indonesia",
        "Cinderamata Akad Nikah",
        "Kemasan Souvenir Kustom"
      ]
    },
    {
      "@type": "Service",
      "@id": "https://souvenirpernikahan.web.id/#service-souvenir",
      "name": "Jasa Pembuatan Souvenir Pernikahan Custom & Hampers Pernikahan",
      "serviceType": "Pembuatan Souvenir Pernikahan Tradisional, Modern, Unik, Elegan & Hampers",
      "provider": {
        "@id": "https://souvenirpernikahan.web.id/#organization"
      },
      "areaServed": {
        "@type": "Country",
        "name": "Indonesia"
      },
      "description": "Layanan produksi dan kustomisasi souvenir pernikahan unik dan elegan: tumbler kopi stainless, kipas batik tulis kayu jati, pouch tenun lurik, lilin aromaterapi, dan hampers pernikahan custom nama pengantin untuk area Malang, Surabaya, Jakarta, dan seluruh Indonesia.",
      "offers": {
        "@type": "AggregateOffer",
        "priceCurrency": "IDR",
        "lowPrice": "15000",
        "highPrice": "185000",
        "offerCount": "100"
      }
    },
    {
      "@type": "Product",
      "@id": "https://souvenirpernikahan.web.id/#product-utama",
      "name": "Koleksi Souvenir Pernikahan Unik, Elegan & Bermanfaat",
      "description": "Koleksi souvenir pernikahan murah, unik, elegan, dan bermanfaat. Pilihan souvenir tradisional kriya nusantara, souvenir modern fungsional, dan hampers pernikahan VIP custom grafir nama kedua mempelai.",
      "image": "https://souvenirpernikahan.web.id/assets/images/hero-souvenir.webp",
      "brand": {
        "@type": "Brand",
        "name": "Souvenir Pernikahan"
      },
      "category": "Souvenir Pernikahan",
      "offers": {
        "@type": "AggregateOffer",
        "priceCurrency": "IDR",
        "lowPrice": "15000",
        "highPrice": "185000",
        "offerCount": "28"
      },
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "bestRating": "5",
        "worstRating": "1",
        "ratingCount": "348",
        "reviewCount": "280"
      }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://souvenirpernikahan.web.id/#breadcrumb",
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
          "name": "Katalog Souvenir Pernikahan",
          "item": "https://souvenirpernikahan.web.id/paket"
        }
      ]
    },
    {
      "@type": "WebPage",
      "@id": "https://souvenirpernikahan.web.id/#webpage",
      "url": "https://souvenirpernikahan.web.id/",
      "name": "Souvenir Pernikahan: Vendor Souvenir Custom, Unik & Elegan",
      "isPartOf": {
        "@id": "https://souvenirpernikahan.web.id/#website"
      },
      "about": {
        "@id": "https://souvenirpernikahan.web.id/#organization"
      },
      "description": "Katalog souvenir pernikahan custom untuk momen akad dan resepsi. Pilihan souvenir pernikahan tradisional, souvenir pernikahan modern, hampers pernikahan unik, personalisasi nama pengantin, serta konsultasi via WhatsApp.",
      "inLanguage": "id-ID",
      "primaryImageOfPage": {
        "@type": "ImageObject",
        "url": "https://souvenirpernikahan.web.id/assets/images/hero-souvenir.webp"
      },
      "speakable": {
        "@type": "SpeakableSpecification",
        "cssSelector": [
          ".gs-hero__title",
          ".gs-hero__desc",
          ".gs-section-title"
        ]
      },
      "mainEntity": {
        "@id": "https://souvenirpernikahan.web.id/#featured-products"
      }
    },
    {
      "@type": "ItemList",
      "@id": "https://souvenirpernikahan.web.id/#featured-products",
      "name": "Pilihan Souvenir Pernikahan Custom Unik & Elegan",
      "description": "Koleksi produk souvenir pernikahan terpopuler dan terfavorit untuk pesta resepsi dan perayaan akad nikah.",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Souvenir Pernikahan Kipas Lipat Batik Tulis Rangka Kayu"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Souvenir Pernikahan Mug Keramik Stoneware Rustic Monogram"
        },
        {
          "@type": "ListItem",
          "position": 3,
          "name": "Souvenir Pernikahan Pouch Dompet Tenun Lurik Tradisional"
        },
        {
          "@type": "ListItem",
          "position": 4,
          "name": "Souvenir Pernikahan Tumbler Kopi Stainless Sage Green"
        },
        {
          "@type": "ListItem",
          "position": 5,
          "name": "Souvenir Pernikahan Besek Anyaman Bambu Hias Bunga Kering"
        },
        {
          "@type": "ListItem",
          "position": 6,
          "name": "Souvenir Pernikahan Pouch Serut Beludru Velvet Monogram"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "@id": "https://souvenirpernikahan.web.id/#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Apa saja pilihan souvenir pernikahan yang unik, elegan, dan bermanfaat?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Kami menyediakan beragam pilihan souvenir pernikahan unik dan bermanfaat: mulai dari souvenir modern fungsional (tumbler stainless steel grafir laser, lilin aromaterapi jar frosted, diffuser sabun pump emas) hingga souvenir tradisional kriya nusantara (kipas batik tulis jati, pouch tenun lurik ATBM, madu hutan murni, dan sendok kayu jati solid)."
          }
        },
        {
          "@type": "Question",
          "name": "Berapa kisaran harga souvenir pernikahan murah hingga hampers pernikahan eksklusif?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Harga souvenir pernikahan di katalog kami sangat fleksibel menyesuaikan budget: mulai dari paket ekonomis Rp 15.000 – Rp 25.000 per pcs, souvenir semi-premium Rp 28.000 – Rp 45.000 per pcs, hingga paket hampers pernikahan VIP eksklusif dalam hardbox magnetik foil emas Rp 125.000 – Rp 185.000."
          }
        },
        {
          "@type": "Question",
          "name": "Apakah melayani pengiriman souvenir pernikahan ke Malang, Surabaya, Jakarta, dan seluruh Indonesia?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Ya, kami melayani pemesanan dan pengiriman aman ke seluruh kota di Indonesia, meliputi Malang Raya, Surabaya, Sidoarjo, Gresik, Pasuruan, Kediri, Blitar, Jabodetabek (Jakarta), Bandung, Semarang, Yogyakarta, Solo, Denpasar Bali, hingga luar pulau menggunakan ekspedisi kargo rekanan terpercaya bergaransi kirim utuh."
          }
        },
        {
          "@type": "Question",
          "name": "Apakah bisa mencetak grafir nama kedua mempelai dan tanggal akad nikah?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Tentu saja. Seluruh souvenir pernikahan kami dapat dipersonalisasi dengan grafir laser nama mempelai, hotprint foil emas inisial monogram, cetak sablon estetik, serta GRATIS kartu ucapan terima kasih (thank you card) dan pita kemasan kustom."
          }
        },
        {
          "@type": "Question",
          "name": "Berapa lama estimasi waktu produksi souvenir pernikahan?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Waktu pengerjaan berkisar antara 14 hingga 21 hari kerja tergantung jumlah pesanan dan kerumitan kustomisasi. Kami menyarankan pemesanan dilakukan 1 hingga 3 bulan sebelum hari H pernikahan. Tersedia juga slot pengerjaan ekspres kilat untuk kebutuhan mendesak."
          }
        },
        {
          "@type": "Question",
          "name": "Bagaimana jika ada barang souvenir yang rusak atau pecah saat pengiriman?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Kami memberikan Garansi 100% Ganti Baru. Setiap pesanan dipacking dengan standar keamanan tinggi (bubble wrap tebal, sekat pelindung, karton ganda, dan peti kayu jika diperlukan). Jika ada barang yang rusak selama perjalanan, kami segera mengirimkan produk pengganti tanpa biaya tambahan."
          }
        }
      ]
    }
  ]
}

new_schema_str = json.dumps(new_schema, indent=2, ensure_ascii=False)

pattern = re.compile(r'<script type="application/ld\+json">[\s\S]*?</script>', re.DOTALL)
m = pattern.search(html)
if m:
    html = pattern.sub(f'<script type="application/ld+json">\n{new_schema_str}\n  </script>', html)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully updated index.html schema with targeted keywords!")
else:
    print("Could not find script tag in index.html!")

