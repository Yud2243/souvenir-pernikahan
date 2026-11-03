import zipfile
import xml.etree.ElementTree as ET
import re
import json
import html
import os
import sys

# 1. Parse raw paragraphs from docx
with zipfile.ZipFile('konten/4_Artikel_SEO_Vendor_Souvenir_Pernikahan_Revisi.docx') as z:
    xml_content = z.read('word/document.xml')
tree = ET.fromstring(xml_content)

raw_p = []
for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    texts = [t.text for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text]
    if texts:
        t = ''.join(texts).strip()
        if t:
            raw_p.append(t)

print(f"Total raw paragraphs: {len(raw_p)}")

area_served_list = [
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
]

canonical_local_business = {
    "@type": ["Organization", "LocalBusiness"],
    "@id": "https://souvenirpernikahan.web.id/#organization",
    "name": "Souvenir Pernikahan",
    "url": "https://souvenirpernikahan.web.id/",
    "logo": {
        "@type": "ImageObject",
        "url": "https://souvenirpernikahan.web.id/assets/profile/logo-navbar-120.webp"
    },
    "image": "https://souvenirpernikahan.web.id/assets/images/hero-souvenir.webp",
    "description": "Penyedia souvenir pernikahan custom elegan, bernilai budaya, dan ramah lingkungan di Malang. Melayani pengiriman ke Surabaya, Jabodetabek, dan seluruh kota di Indonesia.",
    "telephone": "+6282131087971",
    "priceRange": "Rp 15.000 - Rp 500.000",
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
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": "08:30",
            "closes": "18:00"
        }
    ],
    "areaServed": area_served_list,
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+6282131087971",
        "contactType": "customer service",
        "areaServed": "ID",
        "availableLanguage": ["Indonesian"]
    },
    "sameAs": ["https://www.instagram.com/sakasouvenirmlg/"],
    "hasMap": "https://www.google.com/maps?q=-7.9839,112.6214",
    "knowsAbout": [
        "Souvenir Pernikahan",
        "Wedding Favors",
        "Cinderamata Acara",
        "Kemasan Kustom",
        "Kriya Nusantara",
        "Souvenir Tradisional",
        "Souvenir Modern"
    ]
}

canonical_website = {
    "@type": "WebSite",
    "@id": "https://souvenirpernikahan.web.id/#website",
    "url": "https://souvenirpernikahan.web.id/",
    "name": "Souvenir Pernikahan",
    "description": "Penyedia souvenir pernikahan elegan, cinderamata custom berkualitas, dan kemasan eksklusif di Malang dan seluruh Indonesia.",
    "publisher": {
        "@id": "https://souvenirpernikahan.web.id/#organization"
    },
    "inLanguage": "id-ID",
    "potentialAction": {
        "@type": "SearchAction",
        "target": "https://souvenirpernikahan.web.id/blog?q={search_term_string}",
        "query-input": "required name=search_term_string"
    }
}

metadata_keys = [
    'Meta Title:', 'Slug:', 'Meta Description:', 'Focus Keyphrase:', 'Search Intent:',
    'Answer Intent:', 'Primary Entity:', 'Secondary Entities:', 'Query Fan-Out:',
    'Audience:', 'Main Questions Answered:', 'Suggested Schema:', 'Author:',
    'Reviewed By:', 'Last Updated:', 'Source Basis:', 'Images:'
]

def parse_article_data(start, end):
    slice_paras = raw_p[start:end]
    content_idx = 0
    for i, p in enumerate(slice_paras):
        if not any(p.startswith(k) for k in metadata_keys):
            content_idx = i
            break
            
    body = slice_paras[content_idx:]
    h1 = body[0]
    
    ringkasan = []
    r_idx = -1
    for i, p in enumerate(body):
        if p == 'Ringkasan Inti':
            r_idx = i
            break
            
    sections = []
    faqs = []
    kesimpulan = []
    
    in_faq = False
    in_kesimpulan = False
    
    i = r_idx + 1 if r_idx != -1 else 1
    while i < len(body):
        p = body[i]
        if p.endswith('?') or re.match(r'^\d+\.\s+', p) or p.startswith('Mengapa ') or p.startswith('Apa ') or p.startswith('Bagaimana ') or p.startswith('Kapan ') or p.startswith('Apakah '):
            break
        ringkasan.append(p)
        i += 1
        
    current_sec = None
    known_h3s = {
        'Souvenir Pernikahan Fungsional', 'Souvenir Pernikahan Tradisional',
        'Souvenir Pernikahan Modern', 'Souvenir Pernikahan Premium',
        'Segmen Ekonomis', 'Segmen Menengah Rendah', 'Segmen Menengah', 'Segmen Premium'
    }
    
    while i < len(body):
        p = body[i]
        if p.startswith('FAQ') or 'FAQ ' in p:
            in_faq = True
            in_kesimpulan = False
            i += 1
            continue
        elif p == 'Kesimpulan Praktis' or p.startswith('Kesimpulan'):
            in_faq = False
            in_kesimpulan = True
            i += 1
            continue
        elif p.startswith('CLUSTER'):
            i += 1
            continue
            
        if in_faq:
            if p.endswith('?') or p.startswith('Apakah ') or p.startswith('Bagaimana ') or p.startswith('Berapa ') or p.startswith('Apa '):
                q = p
                a = body[i+1] if i+1 < len(body) else ""
                faqs.append((q, a))
                i += 2
                continue
            else:
                i += 1
                continue
        elif in_kesimpulan:
            kesimpulan.append(p)
            i += 1
            continue
        else:
            if p in known_h3s:
                if current_sec:
                    current_sec['items'].append(('h3', p))
                i += 1
                continue
                
            is_h2 = False
            if p.endswith('?') and len(p) < 95:
                is_h2 = True
            elif re.match(r'^\d+\.\s+', p):
                is_h2 = True
            elif p in [
                'Apa Itu Vendor Souvenir Pernikahan?',
                'Mengapa Memilih Vendor Souvenir Pernikahan yang Tepat Itu Penting?',
                'Bagaimana Kondisi Kebutuhan Souvenir Pernikahan di Indonesia?',
                'Apa Saja Jenis Souvenir Pernikahan yang Bisa Dipilih?',
                'Bagaimana Menyesuaikan Souvenir dengan Konsep Pernikahan?',
                'Bagaimana Menentukan Anggaran Souvenir Pernikahan?',
                'Bagaimana Cara Memilih Vendor Souvenir Pernikahan yang Terpercaya?',
                'Bagaimana Proses Pemesanan Souvenir Pernikahan Custom?',
                'Kapan Sebaiknya Memesan Souvenir Pernikahan?',
                'Apa Perbedaan Vendor Souvenir Custom dan Supplier Souvenir Grosir?',
                'Apa Kesalahan yang Perlu Dihindari Saat Memesan Souvenir?',
                'Bagaimana Menyimpan Souvenir Sampai Hari Pernikahan?',
                'Mengapa Ciri Vendor Souvenir Pernikahan Perlu Diperiksa Sebelum Memesan?',
                'Apa Kesalahan Umum Saat Memilih Vendor Souvenir?',
                'Mengapa Anggaran Souvenir Pernikahan Perlu Dihitung Sejak Awal?',
                'Bagaimana Cara Menghitung Budget Souvenir Pernikahan?',
                'Apa Saja Pilihan Souvenir Berdasarkan Segmen Harga?',
                'Bagaimana Memilih Souvenir Murah tetapi Tetap Berkualitas?',
                'Apakah Pemesanan Souvenir Grosir Lebih Hemat?',
                'Bagaimana Menghemat Biaya Desain dan Kemasan?',
                'Apa Faktor yang Membuat Harga Souvenir Berbeda?',
                'Bagaimana Menghindari Pengeluaran Souvenir yang Tidak Perlu?',
                'Apa yang Perlu Disiapkan Sebelum Memesan Souvenir Pernikahan?',
                'Bagaimana Tahap Konsultasi dengan Vendor Souvenir?',
                'Bagaimana Proses Pemilihan Produk dan Material?',
                'Bagaimana Tahap Pembuatan Desain Souvenir Custom?',
                'Mengapa Persetujuan Mockup Penting Sebelum Produksi?',
                'Bagaimana Proses Produksi Souvenir Pernikahan?',
                'Berapa Lama Waktu Produksi Souvenir Pernikahan Custom?',
                'Apa Itu Quality Control pada Souvenir Pernikahan?',
                'Bagaimana Proses Pengemasan dan Pengiriman Souvenir?',
                'Bagaimana Menyimpan dan Mengelola Souvenir Sebelum Hari-H?',
                'Apa Kesalahan yang Sering Terjadi dalam Pemesanan Souvenir?'
            ]:
                is_h2 = True
                
            if is_h2:
                current_sec = {'h2': p, 'items': []}
                sections.append(current_sec)
            else:
                if current_sec:
                    current_sec['items'].append(('p', p))
            i += 1
            
    return h1, ringkasan, sections, faqs, kesimpulan

custom_section_ids = {
    # Art 1
    'Apa Itu Vendor Souvenir Pernikahan?': 'apa-itu-vendor-souvenir-pernikahan',
    'Mengapa Memilih Vendor Souvenir Pernikahan yang Tepat Itu Penting?': 'pentingnya-memilih-vendor-tepat',
    'Bagaimana Kondisi Kebutuhan Souvenir Pernikahan di Indonesia?': 'kebutuhan-souvenir-di-indonesia',
    'Apa Saja Jenis Souvenir Pernikahan yang Bisa Dipilih?': 'jenis-souvenir-pernikahan',
    'Bagaimana Menyesuaikan Souvenir dengan Konsep Pernikahan?': 'menyesuaikan-konsep-pernikahan',
    'Bagaimana Menentukan Anggaran Souvenir Pernikahan?': 'menentukan-anggaran-souvenir',
    'Bagaimana Cara Memilih Vendor Souvenir Pernikahan yang Terpercaya?': 'cara-memilih-vendor-terpercaya',
    'Bagaimana Proses Pemesanan Souvenir Pernikahan Custom?': 'proses-pemesanan-custom',
    'Kapan Sebaiknya Memesan Souvenir Pernikahan?': 'kapan-sebaiknya-memesan',
    'Apa Perbedaan Vendor Souvenir Custom dan Supplier Souvenir Grosir?': 'vendor-custom-vs-supplier-grosir',
    'Apa Kesalahan yang Perlu Dihindari Saat Memesan Souvenir?': 'kesalahan-dalam-memesan',
    'Bagaimana Menyimpan Souvenir Sampai Hari Pernikahan?': 'menyimpan-souvenir-sampai-hari-h',
    # Art 2
    'Mengapa Ciri Vendor Souvenir Pernikahan Perlu Diperiksa Sebelum Memesan?': 'mengapa-ciri-vendor-perlu-diperiksa',
    '1. Apakah Vendor Memiliki Portofolio Produksi yang Asli?': 'portofolio-produksi-asli',
    '2. Bagaimana Vendor Membuktikan Kualitas Material dan Finishing?': 'kualitas-material-dan-finishing',
    '3. Apakah Sampel Souvenir Bisa Diperiksa Sebelum Memesan?': 'sampel-souvenir-sebelum-memesan',
    '4. Apakah Rincian Harga dan Penawaran Vendor Transparan?': 'transparansi-harga-dan-penawaran',
    '5. Apakah Spesifikasi dan Ketentuan Pemesanan Dijelaskan?': 'spesifikasi-dan-ketentuan-pemesanan',
    '6. Bagaimana Kualitas Komunikasi dan Penanganan Revisi Vendor?': 'komunikasi-dan-penanganan-revisi',
    '7. Apakah Jadwal Produksi dan Pengiriman Vendor Realistis?': 'jadwal-produksi-dan-pengiriman-realistis',
    'Apa Kesalahan Umum Saat Memilih Vendor Souvenir?': 'kesalahan-umum-memilih-vendor',
    # Art 3
    'Mengapa Anggaran Souvenir Pernikahan Perlu Dihitung Sejak Awal?': 'mengapa-anggaran-perlu-dihitung-awal',
    'Bagaimana Cara Menghitung Budget Souvenir Pernikahan?': 'cara-menghitung-budget-souvenir',
    'Apa Saja Pilihan Souvenir Berdasarkan Segmen Harga?': 'pilihan-souvenir-segmen-harga',
    'Bagaimana Memilih Souvenir Murah tetapi Tetap Berkualitas?': 'memilih-souvenir-murah-berkualitas',
    'Apakah Pemesanan Souvenir Grosir Lebih Hemat?': 'apakah-pemesanan-grosir-lebih-hemat',
    'Bagaimana Menghemat Biaya Desain dan Kemasan?': 'menghemat-biaya-desain-dan-kemasan',
    'Apa Faktor yang Membuat Harga Souvenir Berbeda?': 'faktor-penentu-harga-souvenir',
    'Bagaimana Menghindari Pengeluaran Souvenir yang Tidak Perlu?': 'menghindari-pengeluaran-tidak-perlu',
    # Art 4
    'Apa yang Perlu Disiapkan Sebelum Memesan Souvenir Pernikahan?': 'persiapan-sebelum-memesan-souvenir',
    'Bagaimana Tahap Konsultasi dengan Vendor Souvenir?': 'tahap-konsultasi-dengan-vendor',
    'Bagaimana Proses Pemilihan Produk dan Material?': 'pemilihan-produk-dan-material',
    'Bagaimana Tahap Pembuatan Desain Souvenir Custom?': 'tahap-pembuatan-desain-custom',
    'Mengapa Persetujuan Mockup Penting Sebelum Produksi?': 'persetujuan-mockup-sebelum-produksi',
    'Bagaimana Proses Produksi Souvenir Pernikahan?': 'proses-produksi-souvenir',
    'Berapa Lama Waktu Produksi Souvenir Pernikahan Custom?': 'lama-waktu-produksi-custom',
    'Apa Itu Quality Control pada Souvenir Pernikahan?': 'quality-control-souvenir',
    'Bagaimana Proses Pengemasan dan Pengiriman Souvenir?': 'pengemasan-dan-pengiriman-souvenir',
    'Bagaimana Menyimpan dan Mengelola Souvenir Sebelum Hari-H?': 'menyimpan-dan-mengelola-souvenir',
    'Apa Kesalahan yang Sering Terjadi dalam Pemesanan Souvenir?': 'kesalahan-pemesanan-souvenir'
}

articles_config = [
    {
        "slug": "vendor-souvenir-pernikahan",
        "start": 1,
        "end": 113,
        "meta_title": "Vendor Souvenir Pernikahan Custom: Tips & Panduan Lengkap",
        "meta_desc": "Cari vendor souvenir pernikahan custom yang sesuai konsep dan anggaran? Kenali pilihan produk, kualitas, proses pemesanan, dan konsultasikan kebutuhan Anda.",
        "category": "Panduan Vendor",
        "topic_tag": "Vendor Souvenir",
        "read_time": "10 Menit Baca",
        "word_count": 2450,
        "time_req": "PT10M",
        "hero_img": "/assets/images/hero-souvenir.webp",
        "hero_alt": "Koleksi vendor souvenir pernikahan custom elegan untuk momen akad dan resepsi",
        "cover_caption": "Memilih vendor souvenir pernikahan custom yang tepat menjamin keselarasan konsep pesta, ketepatan jadwal produksi, dan kualitas cinderamata berkesan bagi para tamu.",
        "img1": (
            "jenis-souvenir-pernikahan",
            "/assets/images/craft-packaging.webp",
            "Pilihan kemasan souvenir pernikahan custom dan elegan",
            "Kemasan souvenir pernikahan custom memberikan impresi elegan dan berkelas bagi setiap tamu undangan."
        ),
        "img2": (
            "proses-pemesanan-custom",
            "/assets/images/detail-hampers-vip-pengantin.webp",
            "Executive hampers souvenir pernikahan tamu VIP",
            "Paket hampers souvenir pernikahan custom untuk tamu VIP dengan kemasan box premium dan kartu ucapan eksklusif."
        ),
        "tags": ["Vendor Souvenir Pernikahan", "Souvenir Pernikahan Custom", "Supplier Souvenir Wedding", "Souvenir Premium", "Souvenir Pernikahan Malang"],
        "product_rec": {
            "badge": "Konsultasi Vendor",
            "title": "Konsultasikan Kebutuhan Souvenir Pernikahan Custom Anda",
            "desc": "Dapatkan proposal penawaran transparan, sampel fisik, dan garansi produksi tepat waktu bersama tim spesialis Souvenir Pernikahan.",
            "note": "Jaminan 100% Ganti Baru & Pengiriman Aman se-Indonesia",
            "btn_text": "Konsultasi Vendor Sekarang",
            "btn_link": "https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi%20pemesanan%20souvenir%20custom."
        },
        "related": [
            ("panduan-memilih-souvenir-pernikahan", "Jenis Souvenir Pernikahan dan Cara Memilihnya yang Tepat", "Pelajari ragam jenis souvenir pernikahan dan tips memilihnya sesuai budget dan konsep acara.", "/assets/images/hero-wedding.webp", "Inspirasi"),
            ("panduan-harga-souvenir-pernikahan-berdasarkan-jenis-produk", "Panduan Harga Souvenir Pernikahan Berdasarkan Jenis Produk", "Estimasi biaya souvenir pernikahan dari yang ekonomis hingga premium.", "/assets/images/panduan-harga-souvenir-pernikahan-berdasarkan-jenis-produk-400.webp", "Estimasi Biaya"),
            ("checklist-pemesanan-souvenir-pernikahan", "Checklist Pemesanan Souvenir Pernikahan Jumlah Besar", "Daftar periksa lengkap timeline dan kontrol pesanan souvenir hari H.", "/assets/images/craft-packaging.webp", "Tips Order")
        ],
        "keywords": "vendor souvenir pernikahan, vendor souvenir pernikahan custom, supplier souvenir pernikahan, souvenir pernikahan malang, pesan souvenir pernikahan, cinderamata pernikahan"
    },
    {
        "slug": "ciri-vendor-souvenir-pernikahan-terpercaya",
        "start": 113,
        "end": 202,
        "meta_title": "7 Ciri Vendor Souvenir Pernikahan yang Terpercaya & Kredibel",
        "meta_desc": "Kenali 7 ciri vendor souvenir pernikahan yang layak dipilih: portofolio asli, sampel fisik, harga transparan, komunikasi jelas, dan jadwal produksi realistis.",
        "category": "Tips Memilih",
        "topic_tag": "Kriteria Vendor",
        "read_time": "9 Menit Baca",
        "word_count": 2150,
        "time_req": "PT9M",
        "hero_img": "/assets/images/hero-wedding.webp",
        "hero_alt": "Pemeriksaan kualitas dan ciri vendor souvenir pernikahan terpercaya",
        "cover_caption": "Menilai ciri vendor souvenir secara menyeluruh sebelum transaksi melindungi anggaran pesta dan memastikan cinderamata tiba sesuai ekspektasi.",
        "img1": (
            "portofolio-produksi-asli",
            "/assets/images/detail-souvenir-tradisional-pengantin.webp",
            "Portofolio asli produksi souvenir tradisional vendor profesional",
            "Dokumentasi portofolio pengerjaan asli souvenir tradisional khas nusantara hasil produksi pengrajin berpengalaman."
        ),
        "img2": (
            "sampel-souvenir-sebelum-memesan",
            "/assets/images/ceramic-mug-souvenir.webp",
            "Contoh sampel souvenir pernikahan mug keramik berkualitas",
            "Sampel fisik souvenir mug keramik custom untuk memastikan ketajaman cetak, kehalusan glasir, dan ketahanan material."
        ),
        "tags": ["Ciri Vendor Souvenir Pernikahan", "Tips Memilih Vendor", "Vendor Souvenir Terpercaya", "Kualitas Souvenir", "Sampel Souvenir"],
        "product_rec": {
            "badge": "Vendor Terverifikasi",
            "title": "Cari Vendor Souvenir Pernikahan Berpengalaman & Transparan?",
            "desc": "Kami mengedepankan portofolio produksi nyata, transparansi rincian biaya, dan tahapan approval sampel sebelum produksi massal.",
            "note": "Workshop Resmi di Malang • Melayani Pengiriman ke Seluruh Kota",
            "btn_text": "Lihat Katalog & Paket",
            "btn_link": "/paket"
        },
        "related": [
            ("vendor-souvenir-pernikahan", "Vendor Souvenir Pernikahan Custom untuk Berbagai Konsep Acara", "Panduan memilih vendor souvenir pernikahan custom bergaransi dan terpercaya.", "/assets/images/hero-souvenir.webp", "Panduan Vendor"),
            ("checklist-pemesanan-souvenir-pernikahan", "Checklist Pemesanan Souvenir Pernikahan Jumlah Besar", "Daftar periksa lengkap timeline dan kontrol pesanan souvenir hari H.", "/assets/images/craft-packaging.webp", "Tips Order"),
            ("cara-menghitung-jumlah-souvenir", "Cara Menghitung Kebutuhan Souvenir Pernikahan agar Pas", "Rumus matematis dan buffer stock agar souvenir pernikahan tidak kurang.", "/assets/images/pouch-tenun-souvenir.webp", "Kalkulasi")
        ],
        "keywords": "ciri vendor souvenir pernikahan, tips memilih vendor souvenir, vendor souvenir pernikahan terpercaya, kualitas souvenir pernikahan, sampel souvenir fisik"
    },
    {
        "slug": "souvenir-pernikahan-sesuai-budget",
        "start": 202,
        "end": 301,
        "meta_title": "Souvenir Pernikahan Sesuai Budget: Panduan Hemat & Elegan",
        "meta_desc": "Pelajari cara memilih souvenir pernikahan sesuai budget: simulasi hitung kebutuhan, segmen harga ekonomis hingga premium, dan tips hemat kemasan elegan.",
        "category": "Estimasi Biaya",
        "topic_tag": "Budgeting",
        "read_time": "9 Menit Baca",
        "word_count": 2200,
        "time_req": "PT9M",
        "hero_img": "/assets/images/panduan-harga-souvenir-pernikahan-berdasarkan-jenis-produk.webp",
        "hero_alt": "Perencanaan anggaran souvenir pernikahan sesuai budget tanpa mengurangi kualitas",
        "cover_caption": "Perencanaan alokasi dana souvenir yang terstruktur membantu calon pengantin memperoleh cinderamata bernilai fungsi tinggi tanpa melampaui batas anggaran.",
        "img1": (
            "cara-menghitung-budget-souvenir",
            "/assets/images/ide-souvenir-pernikahan-budget-rp5-000-per-pcs.webp",
            "Ide souvenir pernikahan hemat budget Rp 5.000 per pcs",
            "Pilihan souvenir pernikahan fungsional pada rentang anggaran ekonomis tetap tampil menawan dengan kemasan terkonsep."
        ),
        "img2": (
            "pilihan-souvenir-segmen-harga",
            "/assets/images/rekomendasi-souvenir-pernikahan-budget-rp10-000.webp",
            "Rekomendasi souvenir pernikahan budget Rp 10.000 favorit pengantin",
            "Ragam cinderamata pernikahan di segmen harga menengah dengan finishing rapi dan kemasan berkelas."
        ),
        "tags": ["Souvenir Pernikahan Sesuai Budget", "Harga Souvenir Pernikahan", "Budget Souvenir Pernikahan", "Souvenir Pernikahan Murah", "Simulasi Anggaran"],
        "product_rec": {
            "badge": "Solusi Anggaran",
            "title": "Dapatkan Rekomendasi Souvenir Sesuai Target Anggaran Anda",
            "desc": "Tim kami siap membantu menghitung simulasi kebutuhan unit, rekomendasi produk terbaik, serta opsi kemasan elegan tanpa membebani biaya.",
            "note": "Tersedia Pilihan Mulai Rp 10.000 hingga Paket Premium VIP",
            "btn_text": "Hitung Anggaran Souvenir",
            "btn_link": "https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi%20souvenir%20sesuai%20budget."
        },
        "related": [
            ("ide-souvenir-pernikahan-budget-rp5-000-per-pcs", "Ide Souvenir Pernikahan Budget Rp5.000 per Pcs", "Pilihan souvenir pernikahan hemat tetap elegan dan fungsional.", "/assets/images/ide-souvenir-pernikahan-budget-rp5-000-per-pcs-400.webp", "Budget Hemat"),
            ("rekomendasi-souvenir-pernikahan-budget-rp10-000", "Rekomendasi Souvenir Pernikahan Budget Rp10.000 Terpopuler", "Koleksi cinderamata nikah terfavorit harga terjangkau kualitas prima.", "/assets/images/rekomendasi-souvenir-pernikahan-budget-rp10-000-400.webp", "Rekomendasi"),
            ("panduan-harga-souvenir-pernikahan-berdasarkan-jenis-produk", "Panduan Harga Souvenir Pernikahan Berdasarkan Jenis Produk", "Estimasi biaya souvenir pernikahan dari yang ekonomis hingga premium.", "/assets/images/panduan-harga-souvenir-pernikahan-berdasarkan-jenis-produk-400.webp", "Estimasi Biaya")
        ],
        "keywords": "souvenir pernikahan sesuai budget, budget souvenir pernikahan, harga souvenir pernikahan, souvenir murah elegan, simulasi anggaran souvenir pernikahan"
    },
    {
        "slug": "proses-pemesanan-souvenir-pernikahan-custom",
        "start": 301,
        "end": len(raw_p),
        "meta_title": "Proses Pemesanan Souvenir Pernikahan Custom dari Awal Sampai Kirim",
        "meta_desc": "Pahami alur proses pemesanan souvenir pernikahan custom: tahap konsultasi, persetujuan mockup desain, quality control, hingga pengemasan ekspedisi aman.",
        "category": "Panduan Order",
        "topic_tag": "Alur Pemesanan",
        "read_time": "9 Menit Baca",
        "word_count": 2180,
        "time_req": "PT9M",
        "hero_img": "/assets/images/craft-packaging.webp",
        "hero_alt": "Alur tahapan proses pemesanan souvenir pernikahan custom dari konsultasi hingga kirim",
        "cover_caption": "Memahami setiap tahapan alur pemesanan souvenir custom memastikan desain, jumlah, dan jadwal pengiriman berjalan mulus hingga hari bahagia.",
        "img1": (
            "persetujuan-mockup-sebelum-produksi",
            "/assets/images/souvenir-tumbler-custom.webp",
            "Mockup grafir nama pada tumbler souvenir custom",
            "Persetujuan visual mockup grafir laser pada tumbler souvenir custom sebelum masuk tahapan produksi massal."
        ),
        "img2": (
            "pengemasan-dan-pengiriman-souvenir",
            "/assets/images/pouch-tenun-souvenir.webp",
            "Pouch tenun lurik proses packaging rapi siap kirim",
            "Pouch tenun lurik yang telah lolos quality control dan dikemas rapi dalam kardus berlapis siap dikirim ke ekspedisi."
        ),
        "tags": ["Proses Pemesanan Souvenir", "Souvenir Pernikahan Custom", "Mockup Souvenir", "Quality Control Souvenir", "Pemesanan Souvenir"],
        "product_rec": {
            "badge": "Alur Terencana",
            "title": "Siap Memulai Proses Pemesanan Souvenir Pernikahan Anda?",
            "desc": "Ikuti alur konsultasi mudah, persetujuan sampel digital & fisik, hingga pengemasan ekspedisi bergaransi untuk kelancaran hari istimewa Anda.",
            "note": "Quality Control 3 Tahap • Update Progres Produksi Berkala",
            "btn_text": "Mulai Konsultasi Desain",
            "btn_link": "https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20memulai%20alur%20pemesanan%20souvenir%20custom."
        },
        "related": [
            ("vendor-souvenir-pernikahan", "Vendor Souvenir Pernikahan Custom untuk Berbagai Konsep Acara", "Panduan memilih vendor souvenir pernikahan custom bergaransi dan terpercaya.", "/assets/images/hero-souvenir.webp", "Panduan Vendor"),
            ("personalisasi-nama-dan-tanggal-souvenir", "Personalisasi Nama dan Tanggal pada Souvenir Pernikahan", "Teknik grafir laser, sablon, dan monogram inisial nama pengantin.", "/assets/images/detail-lilin-aroma-pengantin.webp", "Kustomisasi"),
            ("checklist-pemesanan-souvenir-pernikahan", "Checklist Pemesanan Souvenir Pernikahan Jumlah Besar", "Daftar periksa lengkap timeline dan kontrol pesanan souvenir hari H.", "/assets/images/craft-packaging.webp", "Tips Order")
        ],
        "keywords": "proses pemesanan souvenir pernikahan custom, cara pesan souvenir custom, mockup souvenir pernikahan, alur order souvenir pernikahan, waktu produksi souvenir custom"
    }
]

def build_article_html(cfg):
    slug = cfg["slug"]
    h1, ringkasan, sections, faqs, kesimpulan = parse_article_data(cfg["start"], cfg["end"])
    canonical_url = f"https://souvenirpernikahan.web.id/blog/{slug}"
    
    # 1. Build TOC items
    toc_items = []
    itemlist_elements = []
    for idx, sec in enumerate(sections, 1):
        sec_h2 = sec["h2"]
        sec_id = custom_section_ids.get(sec_h2, f"sec-{idx}")
        toc_title = re.sub(r'^\d+\.\s*', '', sec_h2).rstrip('?')
        toc_items.append((sec_id, toc_title))
        itemlist_elements.append({
            "@type": "ListItem",
            "position": idx,
            "name": f"{idx}. {toc_title}"
        })
    toc_items.append(("faq-souvenir", "Pertanyaan Umum (FAQ)"))
    toc_items.append(("kesimpulan", "Kesimpulan Praktis"))
    
    # 2. Build JSON-LD Schema
    blog_posting = {
        "@type": "BlogPosting",
        "@id": f"{canonical_url}#article",
        "isPartOf": {
            "@id": "https://souvenirpernikahan.web.id/#website"
        },
        "headline": h1,
        "description": cfg["meta_desc"],
        "image": f"https://souvenirpernikahan.web.id{cfg['hero_img']}",
        "datePublished": "2026-11-03T09:00:00+07:00",
        "dateModified": "2026-11-03T09:00:00+07:00",
        "inLanguage": "id-ID",
        "mainEntityOfPage": canonical_url,
        "author": {
            "@type": "Person",
            "@id": "https://souvenirpernikahan.web.id/penulis#person",
            "name": "Yudi Abraham",
            "url": "https://souvenirpernikahan.web.id/penulis",
            "jobTitle": "Manajer Operasional & Produksi Cinderamata",
            "description": "Manajer operasional yang mengawal alur ketepatan jadwal produksi, standarisasi kemasan, dan pengiriman souvenir pernikahan agar selalu tiba tepat waktu di berbagai kota."
        },
        "publisher": {
            "@id": "https://souvenirpernikahan.web.id/#organization"
        },
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [
                ".gs-article__title",
                ".gs-article__lead",
                ".gs-article__key-takeaway p"
            ]
        },
        "articleSection": cfg["category"],
        "keywords": cfg["keywords"],
        "wordCount": cfg["word_count"],
        "timeRequired": cfg["time_req"],
        "isAccessibleForFree": True,
        "license": "https://souvenirpernikahan.web.id/kebijakan-privasi"
    }
    
    breadcrumb_list = {
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
                "name": "Blog",
                "item": "https://souvenirpernikahan.web.id/blog"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": h1,
                "item": canonical_url
            }
        ]
    }
    
    item_list = {
        "@type": "ItemList",
        "@id": f"{canonical_url}#itemlist",
        "name": f"Poin Pembahasan: {h1}",
        "numberOfItems": len(itemlist_elements),
        "itemListElement": itemlist_elements
    }
    
    faq_entities = []
    for q, a in faqs:
        faq_entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
        
    faq_page = {
        "@type": "FAQPage",
        "@id": f"{canonical_url}#faq",
        "mainEntity": faq_entities
    }
    
    schema_graph = {
        "@context": "https://schema.org",
        "@graph": [
            canonical_local_business,
            canonical_website,
            blog_posting,
            breadcrumb_list,
            item_list,
            faq_page
        ]
    }
    schema_json = json.dumps(schema_graph, ensure_ascii=False, indent=2)
    
    # 3. Build Body Sections HTML
    sections_html = []
    
    links_count = {
        "home_souvenir": 0,
        "home_vendor": 0,
        "home_custom": 0,
        "paket": 0,
        "tradisional": 0,
        "modern": 0,
        "tentang": 0,
        "sibling_vendor": 0,
        "sibling_ciri": 0,
        "sibling_budget": 0,
        "sibling_proses": 0
    }
    
    def contextualize(text, current_h2=""):
        # 1. Handle Source Citation notes cleanly as professional editorial callouts
        if "Sumber: BPS - Nikah dan Cerai" in text:
            return '<div class="gs-article__source-note" style="font-size:0.875rem;color:var(--gs-gray-600);background:#f8fafc;border-left:3px solid var(--gs-green-600);padding:0.6rem 0.9rem;border-radius:0 6px 6px 0;margin:0.75rem 0 1.25rem;"><strong>Sumber Rujukan Data:</strong> <a href="https://www.bps.go.id/id/statistics-table/3/VkhwVUszTXJPVmQ2ZFRKamNIZG9RMVo2VEdsbVVUMDkjMyMwMDAw/nikah-dan-cerai-menurut-provinsi-kejadian-.html?year=2024" target="_blank" rel="noopener noreferrer nofollow" style="color:var(--gs-green-800);text-decoration:underline;font-weight:600;">BPS RI &mdash; Statistik Nikah dan Cerai Menurut Provinsi (2024)</a> (Pembaruan data 27 Februari 2025).</div>'

        if "Sumber: ANTARA - Data pernikahan nasional" in text:
            return '<div class="gs-article__source-note" style="font-size:0.875rem;color:var(--gs-gray-600);background:#f8fafc;border-left:3px solid var(--gs-green-600);padding:0.6rem 0.9rem;border-radius:0 6px 6px 0;margin:0.75rem 0 1.25rem;"><strong>Sumber Rujukan Data:</strong> <a href="https://www.antaranews.com/berita/5328550/selama-2025-angka-pernikahan-nasional-tercatat-alami-kenaikan?page=1" target="_blank" rel="noopener noreferrer nofollow" style="color:var(--gs-green-800);text-decoration:underline;font-weight:600;">ANTARA News &mdash; Data Pernikahan Nasional (Kementerian Agama RI)</a> (Publikasi 31 Desember 2025).</div>'

        # 2. First, strip or convert draft docx notes in parentheses like (/panduan/...)
        text = text.replace('(/panduan/anggaran-souvenir-pernikahan/)', '')
        text = text.replace('(/panduan/memilih-vendor-souvenir-pernikahan/)', '')
        text = text.replace('(/panduan/proses-pemesanan-souvenir-pernikahan-custom/)', '')
        text = text.replace('(/vendor-souvenir-pernikahan/)', '')
        text = re.sub(r'\s*\(/[a-zA-Z0-9_\-\/]+\)\s*', ' ', text).strip()
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        
        # 3. Convert specific cross-link sentences gracefully and naturally
        if "7 ciri vendor souvenir pernikahan yang layak dipilih" in text:
            text = text.replace("7 ciri vendor souvenir pernikahan yang layak dipilih", '<a href="/blog/ciri-vendor-souvenir-pernikahan-terpercaya">7 ciri vendor souvenir pernikahan yang layak dipilih</a>')
            links_count["sibling_ciri"] += 1
            return re.sub(r'\s+([.,;:!?])', r'\1', text)
            
        if "proses pemesanan souvenir pernikahan custom" in text and slug != "proses-pemesanan-souvenir-pernikahan-custom":
            text = text.replace("proses pemesanan souvenir pernikahan custom", '<a href="/blog/proses-pemesanan-souvenir-pernikahan-custom">proses pemesanan souvenir pernikahan custom</a>')
            links_count["sibling_proses"] += 1
            return re.sub(r'\s+([.,;:!?])', r'\1', text)

        if "anggaran souvenir pernikahan sesuai kebutuhan" in text or "anggaran souvenir pernikahan" in text:
            if slug != "souvenir-pernikahan-sesuai-budget" and links_count["sibling_budget"] < 1:
                text = text.replace("anggaran souvenir pernikahan", '<a href="/blog/souvenir-pernikahan-sesuai-budget">anggaran souvenir pernikahan</a>')
                links_count["sibling_budget"] += 1
                return re.sub(r'\s+([.,;:!?])', r'\1', text)

        if "layanan vendor dan ragam produknya" in text and slug != "vendor-souvenir-pernikahan":
            text = 'Untuk memahami layanan vendor dan ragam produknya, simak panduan lengkap <a href="/blog/vendor-souvenir-pernikahan">vendor souvenir pernikahan custom</a>.'
            links_count["sibling_vendor"] += 1
            return text

        if "bandingkan harga bersama spesifikasi tertulis" in text and slug != "vendor-souvenir-pernikahan":
            text = 'Karena itu, bandingkan harga bersama spesifikasi tertulis. Untuk melihat kategori produk dan ragam layanannya, pelajari panduan <a href="/blog/vendor-souvenir-pernikahan">vendor souvenir pernikahan custom</a>.'
            links_count["sibling_vendor"] += 1
            return text

        if "pilihan layanan" in text and "vendor souvenir pernikahan custom" in text and slug != "vendor-souvenir-pernikahan":
            text = 'Untuk memahami gambaran layanan secara komprehensif, pelajari panduan lengkap <a href="/blog/vendor-souvenir-pernikahan">vendor souvenir pernikahan custom</a>.'
            links_count["sibling_vendor"] += 1
            return text

        if "panduan vendor souvenir pernikahan custom" in text or "vendor souvenir pernikahan custom untuk berbagai konsep acara" in text:
            if slug != "vendor-souvenir-pernikahan" and links_count["sibling_vendor"] < 1:
                text = re.sub(r'(?:panduan\s+)?vendor souvenir pernikahan custom(?: untuk berbagai konsep acara)?', '<a href="/blog/vendor-souvenir-pernikahan">vendor souvenir pernikahan custom</a>', text)
                links_count["sibling_vendor"] += 1
                return re.sub(r'\s+([.,;:!?])', r'\1', text)

        # 4. Standard Home anchors: souvenir pernikahan, vendor souvenir pernikahan, souvenir pernikahan custom
        if links_count["home_souvenir"] < 2 and "souvenir pernikahan" in text:
            text = re.sub(r'\bsouvenir pernikahan\b', r'<a href="/">souvenir pernikahan</a>', text, count=1)
            links_count["home_souvenir"] += 1
            
        if links_count["home_vendor"] < 2 and "vendor souvenir pernikahan" in text and '<a href="/">vendor souvenir pernikahan' not in text:
            text = re.sub(r'\bvendor souvenir pernikahan\b', r'<a href="/">vendor souvenir pernikahan</a>', text, count=1)
            links_count["home_vendor"] += 1
            
        if links_count["home_custom"] < 1 and "souvenir pernikahan custom" in text and '<a href="/">souvenir pernikahan custom' not in text:
            text = re.sub(r'\bsouvenir pernikahan custom\b', r'<a href="/">souvenir pernikahan custom</a>', text, count=1)
            links_count["home_custom"] += 1
            
        if links_count["paket"] < 1 and ("pilihan souvenir" in text or "paket souvenir" in text or "katalog" in text):
            if "paket souvenir" in text:
                text = re.sub(r'\bpaket souvenir\b', r'<a href="/paket">paket souvenir</a>', text, count=1)
                links_count["paket"] += 1
            elif "pilihan souvenir" in text:
                text = re.sub(r'\bpilihan souvenir\b', r'<a href="/paket">pilihan souvenir</a>', text, count=1)
                links_count["paket"] += 1
            
        return re.sub(r'\s+([.,;:!?])', r'\1', text)

    for sec in sections:
        sec_h2 = sec["h2"]
        sec_id = custom_section_ids.get(sec_h2, "sec")
        
        s_lines = []
        s_lines.append(f'            <section class="gs-article__section" id="{sec_id}">')
        s_lines.append(f'              <h2>{html.escape(sec_h2)}</h2>')
        
        items = sec["items"]
        idx = 0
        while idx < len(items):
            itype, itext = items[idx]
            if itype == 'h3':
                s_lines.append(f'              <h3>{html.escape(itext)}</h3>')
                idx += 1
            elif itype == 'p':
                # ARTICLE 3 TABLE 1: SIMULASI HITUNG BUDGET
                if itext == 'Jumlah Souvenir' and idx + 14 < len(items):
                    c_qty = itext
                    c_unit = items[idx+1][1]
                    c_tot = items[idx+2][1]
                    
                    r1 = (items[idx+3][1], items[idx+4][1], items[idx+5][1])
                    r2 = (items[idx+6][1], items[idx+7][1], items[idx+8][1])
                    r3 = (items[idx+9][1], items[idx+10][1], items[idx+11][1])
                    r4 = (items[idx+12][1], items[idx+13][1], items[idx+14][1])
                    
                    s_lines.append('              <div class="gs-article__table-wrapper">')
                    s_lines.append('                <table class="gs-article__table">')
                    s_lines.append('                  <thead>')
                    s_lines.append('                    <tr>')
                    s_lines.append(f'                      <th scope="col" style="min-width: 140px;">{html.escape(c_qty)}</th>')
                    s_lines.append(f'                      <th scope="col">{html.escape(c_unit)}</th>')
                    s_lines.append(f'                      <th scope="col">{html.escape(c_tot)}</th>')
                    s_lines.append('                    </tr>')
                    s_lines.append('                  </thead>')
                    s_lines.append('                  <tbody>')
                    for q, u, t in [r1, r2, r3, r4]:
                        s_lines.append('                    <tr>')
                        s_lines.append(f'                      <td><strong>{html.escape(q)}</strong></td>')
                        s_lines.append(f'                      <td>{html.escape(u)}</td>')
                        s_lines.append(f'                      <td>{html.escape(t)}</td>')
                        s_lines.append('                    </tr>')
                    s_lines.append('                  </tbody>')
                    s_lines.append('                </table>')
                    s_lines.append('              </div>')
                    idx += 15
                else:
                    proc_p = contextualize(itext, sec_h2)
                    if proc_p.startswith('<div'):
                        s_lines.append(f'              {proc_p}')
                    else:
                        s_lines.append(f'              <p>{proc_p}</p>')
                    idx += 1
                    
        # -------------------------------------------------------------
        # INJEKSI TABEL & LISTS KHUSUS TIAP SECTION
        # -------------------------------------------------------------
        
        # 1. ARTICLE 1 (vendor-souvenir-pernikahan)
        if slug == "vendor-souvenir-pernikahan":
            if sec_id == "jenis-souvenir-pernikahan":
                s_lines.append('''              <ul>
                <li><strong>Souvenir Fungsional:</strong> Cinderamata yang memiliki manfaat praktis sehari-hari seperti sendok-garpu kayu mahoni, botol minum tumbler, dan pouch serbaguna.</li>
                <li><strong>Souvenir Tradisional Khas:</strong> Menonjolkan kekayaan kriya nusantara seperti kain lurik, kipas batik cap, dompet anyaman pandan, dan gerabah estetik.</li>
                <li><strong>Souvenir Modern Minimalis:</strong> Mengutamakan estetika simpel, clean, dan elegan seperti reed diffuser ruangan, lilin aromaterapi soy wax, dan tatakan gelas marmer.</li>
                <li><strong>Souvenir Premium &amp; VIP:</strong> Dirancang khusus untuk keluarga inti dan tamu kehormatan dengan material eksklusif hardbox velvet dan kombinasi gift set berkelas.</li>
              </ul>''')
            elif sec_id == "vendor-custom-vs-supplier-grosir":
                s_lines.append('''              <div class="gs-article__table-wrapper">
                <table class="gs-article__table">
                  <thead>
                    <tr>
                      <th scope="col" style="min-width: 140px;">Parameter Pembanding</th>
                      <th scope="col">Vendor Souvenir Custom</th>
                      <th scope="col">Supplier Grosir Pasar</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Fleksibilitas Desain</strong></td>
                      <td>Sangat bebas; personalisasi grafir nama, inisial font, dan penyesuaian warna tema pesta.</td>
                      <td>Terbatas pada produk cetakan pabrik yang sudah jadi (ready stock umum).</td>
                    </tr>
                    <tr>
                      <td><strong>Layanan Sampel Fisik</strong></td>
                      <td>Menyediakan sampel proofing dan mockup digital sebelum masuk tahap produksi massal.</td>
                      <td>Jarang ada sampel kustom; pembeli hanya bisa melihat contoh pajangan di toko.</td>
                    </tr>
                    <tr>
                      <td><strong>Kemasan &amp; Kartu Ucapan</strong></td>
                      <td>Termasuk kemasan terkonsep (box mika, hardbox, pouch tenun) dan kartu ucapan kustom.</td>
                      <td>Umumnya kemasan plastik polos tipis tanpa kartu ucapan atau pita dekoratif.</td>
                    </tr>
                    <tr>
                      <td><strong>Minimum Pemesanan (MOQ)</strong></td>
                      <td>Fleksibel, mulai dari 50 hingga 100 pcs untuk intimate wedding maupun partai besar.</td>
                      <td>Harus per dus karton besar pabrikan tanpa opsi personalisasi satuan.</td>
                    </tr>
                    <tr>
                      <td><strong>Jaminan Mutu &amp; Garansi</strong></td>
                      <td>Quality control berlapis dengan garansi penggantian barang cacat produksi.</td>
                      <td>Sistem beli putus; barang pecah atau cacat cetak sulit ditukar kembali.</td>
                    </tr>
                  </tbody>
                </table>
              </div>''')
            elif sec_id == "kesalahan-dalam-memesan":
                s_lines.append('''              <ul>
                <li><strong>Pemesanan Terlalu Dekat Hari-H:</strong> Menyisakan sedikit waktu bila terjadi kendala bahan baku atau keterlambatan kurir kargo.</li>
                <li><strong>Tidak Meminta Sampel Proofing:</strong> Risiko ketidaksesuaian warna sablon, ukuran riil, atau hasil grafir laser nama pengantin.</li>
                <li><strong>Mengabaikan Perhitungan Buffer Cadangan (+10%):</strong> Berpotensi membuat cinderamata kurang saat tamu undangan membawa pendamping.</li>
                <li><strong>Lupa Menghitung Waktu Ekspedisi Kargo:</strong> Pengiriman darat/laut ke luar pulau membutuhkan waktu transit 4–7 hari kerja.</li>
              </ul>''')

        # 2. ARTICLE 2 (ciri-vendor-souvenir-pernikahan-terpercaya)
        elif slug == "ciri-vendor-souvenir-pernikahan-terpercaya":
            if sec_id == "mengapa-ciri-vendor-perlu-diperiksa":
                s_lines.append('''              <div class="gs-article__table-wrapper">
                <table class="gs-article__table">
                  <thead>
                    <tr>
                      <th scope="col" style="min-width: 140px;">7 Ciri Utama</th>
                      <th scope="col">Bukti Verifikasi yang Wajib Diminta</th>
                      <th scope="col">Risiko Jika Diabaikan</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>1. Portofolio Nyata</strong></td>
                      <td>Dokumentasi foto/video asli workshop, bukan mockup 3D atau comotan internet.</td>
                      <td>Hasil jadi berbeda jauh dengan ekspektasi katalog digital.</td>
                    </tr>
                    <tr>
                      <td><strong>2. Kualitas Material</strong></td>
                      <td>Spesifikasi ketebalan kain (gramasi), jenis kayu/keramik, dan kerapian jahitan.</td>
                      <td>Bahan tipis, mudah robek, atau finishing kasar saat dibagikan.</td>
                    </tr>
                    <tr>
                      <td><strong>3. Sampel Fisik</strong></td>
                      <td>Ketersediaan sampel fisik yang bisa dikirim atau dilihat di studio workshop.</td>
                      <td>Kecewa massal setelah ratusan souvenir selesai diproduksi.</td>
                    </tr>
                    <tr>
                      <td><strong>4. Transparansi Biaya</strong></td>
                      <td>Rincian nota formal mencakup produk, kemasan, kartu ucapan, dan estimasi ongkir.</td>
                      <td>Biaya siluman tak terduga menjelang pelunasan barang.</td>
                    </tr>
                    <tr>
                      <td><strong>5. Ketentuan Tertulis</strong></td>
                      <td>Invoice resmi dengan tanggal komitmen deadline, termin DP, dan klausa garansi.</td>
                      <td>Perselisihan bila terjadi cacat produk atau pesanan molor.</td>
                    </tr>
                    <tr>
                      <td><strong>6. Komunikasi Jelas</strong></td>
                      <td>Customer service responsif memberikan foto progres produksi berkala.</td>
                      <td>Stres berkepanjangan karena vendor sulit dihubungi jelang hari-H.</td>
                    </tr>
                    <tr>
                      <td><strong>7. Jadwal Realistis</strong></td>
                      <td>Timeline terstruktur dengan buffer pengiriman minimal 2 minggu sebelum acara.</td>
                      <td>Paket souvenir belum tiba di gedung saat resepsi berlangsung.</td>
                    </tr>
                  </tbody>
                </table>
              </div>''')
            elif sec_id == "kesalahan-umum-memilih-vendor":
                s_lines.append('''              <ul>
                <li><strong>Tergiur Tawaran Harga Sangat Murah di Bawah Pasar:</strong> Sering kali mengorbankan kualitas bahan baku utama, ketebalan kemasan, atau kerapian sablon.</li>
                <li><strong>Mengandalkan Foto Katalog Digital Semata:</strong> Banyak penjual perantara menggunakan foto unduhan tanpa memiliki workshop atau stok sendiri.</li>
                <li><strong>Tidak Meminta Sampel Fisik Terlebih Dahulu:</strong> Menilai tekstur, bobot, dan aroma produk mustahil dilakukan hanya melalui layar ponsel.</li>
                <li><strong>Menyetujui Transaksi Tanpa Kesepakatan Deadline Tertulis:</strong> Ketiadaan tanggal batas akhir pengiriman berisiko membuat pesanan dikerjakan secara terburu-buru.</li>
              </ul>''')

        # 3. ARTICLE 3 (souvenir-pernikahan-sesuai-budget)
        elif slug == "souvenir-pernikahan-sesuai-budget":
            if sec_id == "pilihan-souvenir-segmen-harga":
                s_lines.append('''              <div class="gs-article__table-wrapper">
                <table class="gs-article__table">
                  <thead>
                    <tr>
                      <th scope="col" style="min-width: 140px;">Segmen Anggaran</th>
                      <th scope="col">Kisaran Harga per Unit</th>
                      <th scope="col">Rekomendasi Produk Terpopuler</th>
                      <th scope="col">Opsi Kemasan Efisien</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Segmen Ekonomis</strong></td>
                      <td>Rp 5.000 – Rp 8.000</td>
                      <td>Sendok garpu kayu mahoni, pouch blacu mini, centong batik, gantungan kunci kulit sintetis.</td>
                      <td>Plastik seal bening berpita rami &amp; hangtag nama sederhana.</td>
                    </tr>
                    <tr>
                      <td><strong>Menengah Rendah</strong></td>
                      <td>Rp 9.000 – Rp 15.000</td>
                      <td>Kipas batik tangkai bambu, pouch tenun lurik, mangkok sambal keramik, coaster kayu grafir.</td>
                      <td>Paper pouch ramah lingkungan / paper belt motif estetik.</td>
                    </tr>
                    <tr>
                      <td><strong>Menengah</strong></td>
                      <td>Rp 16.000 – Rp 35.000</td>
                      <td>Tumbler stainless grafir laser, mug keramik custom, handuk bordir inisial, lilin aromaterapi soy wax.</td>
                      <td>Kardus kraft motif jendela mika &amp; pita satin elegan.</td>
                    </tr>
                    <tr>
                      <td><strong>Premium &amp; VIP</strong></td>
                      <td>Rp 40.000 – Rp 150.000+</td>
                      <td>Hampers set kriya nusantara, reed diffuser set eksklusif, clutch kulit asli, piring porselen dekoratif.</td>
                      <td>Hardbox velvet bermagnet, hot stamp foil emas &amp; kartu eksklusif.</td>
                    </tr>
                  </tbody>
                </table>
              </div>''')
            elif sec_id == "menghemat-biaya-desain-dan-kemasan":
                s_lines.append('''              <ul>
                <li><strong>Pilih Kemasan Berbahan Alami:</strong> Besek bambu, pouch kain blacu, atau kardus kraft cokelat memberikan kesan rustic elegan dengan biaya jauh lebih terjangkau dibanding hardbox mewah.</li>
                <li><strong>Manfaatkan Hangtag Minimalis:</strong> Daripada mencetak sablon terpisah di setiap kotak kemasan, menggantungkan label ucapan monogram di pita kemasan menghemat biaya cetak hingga 40%.</li>
                <li><strong>Pesan Kuantitas Sekaligus:</strong> Memesan seluruh total kebutuhan dalam satu kali antrean produksi memberikan potongan harga grosir bahan baku daripada pemesanan terpecah.</li>
                <li><strong>Hindari Desain Terlalu Rumit:</strong> Monogram inisial nama yang simpel lebih cepat dikerjakan, presisi, dan tidak membutuhkan biaya pembuatan pelat cetak tambahan.</li>
              </ul>''')

        # 4. ARTICLE 4 (proses-pemesanan-souvenir-pernikahan-custom)
        elif slug == "proses-pemesanan-souvenir-pernikahan-custom":
            if sec_id == "persiapan-sebelum-memesan-souvenir":
                s_lines.append('''              <ul>
                <li><strong>Tanggal Acara &amp; Lokasi Resepsi:</strong> Menentukan batas deadline pengiriman kargo tiba aman minimal H-14 hari sebelum acara.</li>
                <li><strong>Estimasi Kuantitas Tamu (+10% Buffer):</strong> Mencegah kekurangan cinderamata saat hari pernikahan berlangsung.</li>
                <li><strong>Tema Visual &amp; Palet Warna:</strong> Memudahkan vendor menyelaraskan warna pita, kemasan, atau material souvenir.</li>
                <li><strong>Teks Inisial Nama &amp; Tanggal Pernikahan:</strong> Format penulisan monogram resmi yang akan dicantumkan pada kartu ucapan dan fisik souvenir.</li>
                <li><strong>Batas Plafon Anggaran (Budget):</strong> Memberikan patokan jelas bagi tim konsultan dalam memberikan opsi produk terbaik.</li>
              </ul>''')
            elif sec_id == "lama-waktu-produksi-custom":
                s_lines.append('''              <div class="gs-article__table-wrapper">
                <table class="gs-article__table">
                  <thead>
                    <tr>
                      <th scope="col" style="min-width: 130px;">Fase Alur</th>
                      <th scope="col">Aktivitas Utama</th>
                      <th scope="col">Estimasi Durasi</th>
                      <th scope="col">Output yang Diterima Pengantin</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Fase 1: Konsultasi</strong></td>
                      <td>Diskusi konsep, kecocokan tema, pilihan produk, dan penetapan anggaran.</td>
                      <td>1 – 3 Hari</td>
                      <td>Katalog rekomendasi &amp; estimasi penawaran harga.</td>
                    </tr>
                    <tr>
                      <td><strong>Fase 2: Mockup &amp; Sampel</strong></td>
                      <td>Pembuatan layout digital grafir/cetak nama pengantin dan sampel fisik proofing.</td>
                      <td>3 – 5 Hari</td>
                      <td>File visual 2D/3D &amp; foto sampel nyata untuk approval.</td>
                    </tr>
                    <tr>
                      <td><strong>Fase 3: Produksi Massal</strong></td>
                      <td>Pengerjaan pemotongan bahan, cetak kustom, dan perakitan seluruh unit.</td>
                      <td>14 – 21 Hari</td>
                      <td>Update dokumentasi progres pengerjaan di workshop.</td>
                    </tr>
                    <tr>
                      <td><strong>Fase 4: Quality Control</strong></td>
                      <td>Pengecekan fisik 100%, sortir kecacatan, perakitan pita dan kartu ucapan.</td>
                      <td>2 – 3 Hari</td>
                      <td>Laporan inspeksi mutu siap bungkus kardus ekspedisi.</td>
                    </tr>
                    <tr>
                      <td><strong>Fase 5: Pengiriman</strong></td>
                      <td>Packing kardus berlapis, penyerahan ke kargo logistik, dan pelacakan resi.</td>
                      <td>3 – 6 Hari</td>
                      <td>Nomor resi kargo resmi &amp; paket tiba di alamat tujuan.</td>
                    </tr>
                  </tbody>
                </table>
              </div>''')
            elif sec_id == "quality-control-souvenir":
                s_lines.append('''              <ul>
                <li><strong>Tahap 1 — Inspeksi Bahan Baku Mentah:</strong> Memastikan kayu tidak lapuk, keramik tanpa retak rambut, kain tenun tanpa serat putus, dan tumbler bebas goresan pabrik.</li>
                <li><strong>Tahap 2 — Verifikasi Cetak &amp; Grafir Laser:</strong> Menguji ketajaman tipografi nama pengantin, ketepatan posisi logo, dan daya rekat sablon/tinta.</li>
                <li><strong>Tahap 3 — Uji Kelayakan Kemasan Akhir:</strong> Memastikan pita terpasang kencang simetris, kartu ucapan tidak terlipat, dan lapisan bubble wrap membungkus rapat setiap unit.</li>
              </ul>''')

        # -------------------------------------------------------------
        # INLINE IMAGES
        # -------------------------------------------------------------
        if cfg["img1"][0] == sec_id:
            s_lines.append('              <figure class="gs-article__figure">')
            s_lines.append(f'                <img src="{cfg["img1"][1]}" alt="{html.escape(cfg["img1"][2])}" width="900" height="500" loading="lazy" />')
            s_lines.append(f'                <figcaption>{html.escape(cfg["img1"][3])}</figcaption>')
            s_lines.append('              </figure>')
            
        if cfg["img2"][0] == sec_id:
            s_lines.append('              <figure class="gs-article__figure">')
            s_lines.append(f'                <img src="{cfg["img2"][1]}" alt="{html.escape(cfg["img2"][2])}" width="900" height="500" loading="lazy" />')
            s_lines.append(f'                <figcaption>{html.escape(cfg["img2"][3])}</figcaption>')
            s_lines.append('              </figure>')
            
        s_lines.append('            </section>')
        sections_html.append('\n'.join(s_lines))
        
    all_sections_str = '\n\n'.join(sections_html)
    
    # 4. Build FAQ Items HTML
    faq_html_list = []
    for f_idx, (fq, fa) in enumerate(faqs, 1):
        f_ans_proc = contextualize(fa)
        faq_html_list.append(f'''              <div class="gs-article__faq-item">
                <button type="button" class="gs-article__faq-question" aria-expanded="false" aria-controls="faq-ans-{f_idx}">
                  {html.escape(fq)}
                  <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" aria-hidden="true">
                    <path d="M4 6l4 4 4-4" />
                  </svg>
                </button>
                <div class="gs-article__faq-answer" id="faq-ans-{f_idx}">
                  <p>{f_ans_proc}</p>
                </div>
              </div>''')
    faq_items_str = '\n'.join(faq_html_list)
    
    # 5. Build Kesimpulan HTML
    kesimpulan_proc = [f"<p>{contextualize(kp)}</p>" for kp in kesimpulan]
    kesimpulan_proc.append(f'<p>Wujudkan momen spesial Anda dengan cinderamata yang berkesan bersama <a href="/">vendor souvenir pernikahan</a> profesional, atau diskusikan kebutuhan souvenir custom Anda langsung bersama tim kami.</p>')
    kesimpulan_str = '\n              '.join(kesimpulan_proc)
    
    # 6. Build TOC List
    toc_li_list = [f'                <li><a href="#{tid}">{html.escape(tname)}</a></li>' for tid, tname in toc_items]
    toc_list_str = '\n'.join(toc_li_list)
    
    # 7. Build Key Takeaway List
    takeaway_li = [f'<li>{html.escape(r)}</li>' for r in ringkasan]
    takeaway_str = f'''<ul style="margin: 0; padding-left: 1.25rem; display: flex; flex-direction: column; gap: 0.5rem; color: var(--gs-gray-700); font-size: 0.95rem; line-height: 1.6;">
                {' '.join(takeaway_li)}
              </ul>'''
              
    # 8. Build Tags HTML & OpenGraph article:tag
    tag_anchors = [f'<a href="/blog" class="gs-article__tag">#{t.replace(" ", "")}</a>' for t in cfg["tags"]]
    tags_str = '\n                '.join(tag_anchors)
    og_tags = [f'  <meta property="article:tag" content="{html.escape(t)}" />' for t in cfg["tags"]]
    og_tags_str = '\n'.join(og_tags)
    
    # 9. Build Related Articles Grid
    rel_cards = []
    for rslug, rtitle, rdesc, rimg, rcat in cfg["related"]:
        rel_cards.append(f'''              <article data-gs-animate class="gs-blog-card">
                <div class="gs-blog-card__image">
                  <img src="{rimg}" alt="{html.escape(rtitle)}" loading="lazy" />
                </div>
                <div class="gs-blog-card__body">
                  <div class="gs-blog-card__meta">
                    <span class="gs-blog-card__category">{rcat}</span>
                    <span aria-hidden="true">&bull;</span>
                    <time datetime="2026-11-03">3 Nov 2026</time>
                  </div>
                  <h3 class="gs-blog-card__title">
                    <a href="/blog/{rslug}">{html.escape(rtitle)}</a>
                  </h3>
                  <p class="gs-blog-card__excerpt">{html.escape(rdesc)}</p>
                  <a href="/blog/{rslug}" class="gs-blog-card__link">
                    Baca Selengkapnya &rarr;
                  </a>
                </div>
              </article>''')
    rel_cards_str = '\n\n'.join(rel_cards)
    
    # 10. Assemble full HTML template
    full_html = f'''<!DOCTYPE html>
<html lang="id">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />

  <!-- Preload Critical CSS -->
  <link rel="preload" href="/assets/css/style.min.css?v=8" as="style" />

  <title>{html.escape(cfg["meta_title"])}</title>
  <meta name="description"
    content="{html.escape(cfg["meta_desc"])}" />
  <meta name="author" content="Yudi Abraham" />
  <meta name="language" content="Indonesian" />
  <meta name="theme-color" content="#23472d" />
  <meta name="format-detection" content="telephone=no" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />

  <!-- Favicon & App Icons -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/profile/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/profile/favicon-16x16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/profile/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />

  <!-- Canonical & Alternate Hreflang -->
  <link rel="canonical" href="{canonical_url}" />
  <link rel="alternate" hreflang="id-ID"
    href="{canonical_url}" />
  <link rel="alternate" hreflang="x-default"
    href="{canonical_url}" />

  <!-- GEO & Local Engine Optimization (GEO) -->
  <meta name="geo.region" content="ID-JI" />
  <meta name="geo.placename" content="Kota Malang, Jawa Timur, Indonesia" />
  <meta name="geo.position" content="-7.9839;112.6214" />
  <meta name="ICBM" content="-7.9839, 112.6214" />
  <meta name="geo.country" content="ID" />

  <!-- Open Graph / Facebook / WhatsApp -->
  <meta property="og:site_name" content="Souvenir Pernikahan" />
  <meta property="og:type" content="article" />
  <meta property="og:locale" content="id_ID" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:title"
    content="{html.escape(cfg["meta_title"])}" />
  <meta property="og:description"
    content="{html.escape(cfg["meta_desc"])}" />
  <meta property="og:image" content="https://souvenirpernikahan.web.id{cfg["hero_img"]}" />
  <meta property="og:image:secure_url" content="https://souvenirpernikahan.web.id{cfg["hero_img"]}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{html.escape(cfg["hero_alt"])}" />
  <meta property="og:image:type" content="image/webp" />
  <meta property="article:published_time" content="2026-11-03T09:00:00+07:00" />
  <meta property="article:modified_time" content="2026-11-03T09:00:00+07:00" />
  <meta property="article:author" content="Yudi Abraham" />
  <meta property="article:section" content="{cfg["category"]}" />
{og_tags_str}

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:url" content="{canonical_url}" />
  <meta name="twitter:title"
    content="{html.escape(cfg["meta_title"])}" />
  <meta name="twitter:description"
    content="{html.escape(cfg["meta_desc"])}" />
  <meta name="twitter:image" content="https://souvenirpernikahan.web.id{cfg["hero_img"]}" />
  <meta name="twitter:image:alt" content="{html.escape(cfg["hero_alt"])}" />

  <!-- Stylesheet -->
  <link rel="stylesheet" href="/assets/css/style.min.css?v=8" />

  <!-- Structured Data JSON-LD (Schema.org) -->
  <script type="application/ld+json">
{schema_json}
  </script>
</head>

<body>

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
              <button class="gs-dropdown__toggle" aria-haspopup="true" aria-expanded="false"
                aria-controls="gs-dropdown-paket" id="gs-dropdown-paket-btn" role="menuitem">
                Paket
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round" aria-hidden="true">
                  <path d="M4 6l4 4 4-4" />
                </svg>
              </button>
              <div class="gs-dropdown__menu" id="gs-dropdown-paket" role="menu" aria-labelledby="gs-dropdown-paket-btn">
                <a href="/paket" class="gs-dropdown__item" role="menuitem"><svg viewBox="0 0 20 20"
                    fill="currentColor" aria-hidden="true">
                    <path
                      d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM14 11a1 1 0 011 1v1h1a1 1 0 110 2h-1v1a1 1 0 11-2 0v-1h-1a1 1 0 110-2h1v-1a1 1 0 011-1z" />
                  </svg>Semua Paket</a>
                <div class="gs-dropdown__divider" role="separator"></div>
                <a href="/paket/souvenir-tradisional" class="gs-dropdown__item" role="menuitem"><svg
                    viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd"
                      d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
                      clip-rule="evenodd" />
                  </svg>Souvenir Tradisional</a>
                <a href="/paket/souvenir-modern" class="gs-dropdown__item" role="menuitem"><svg
                    viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd"
                      d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2h-3a1 1 0 01-1-1v-2a1 1 0 00-1-1H9a1 1 0 00-1 1v2a1 1 0 01-1 1H4a1 1 0 110-2V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z"
                      clip-rule="evenodd" />
                  </svg>Souvenir Modern</a>
              </div>
            </div>
            <a href="/portofolio" class="gs-navbar__link" role="menuitem">Portofolio</a>
            <a href="/blog" class="gs-navbar__link active" role="menuitem">Blog</a>
          </div>
          <div class="gs-navbar__cta">
            <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi%20souvenir%20pernikahan."
              class="gs-button gs-button--whatsapp gs-button--sm" target="_blank" rel="noopener noreferrer"
              aria-label="Konsultasi via WhatsApp">Konsultasi</a>
          </div>
          <button class="gs-navbar__hamburger" id="gs-hamburger" aria-label="Buka menu navigasi" aria-expanded="false"
            aria-controls="gs-mobile-menu">
            <span class="gs-navbar__hamburger-line"></span><span class="gs-navbar__hamburger-line"></span><span
              class="gs-navbar__hamburger-line"></span>
          </button>
        </div>
        <div class="gs-navbar__mobile-menu" id="gs-mobile-menu" role="menu">
          <a href="/" class="gs-navbar__mobile-link" role="menuitem">Beranda</a>
          <a href="/tentang" class="gs-navbar__mobile-link" role="menuitem">Tentang</a>
          <button class="gs-navbar__mobile-submenu-toggle" aria-expanded="false" aria-controls="gs-mobile-paket">Paket
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" aria-hidden="true">
              <path d="M4 6l4 4 4-4" />
            </svg></button>
          <div class="gs-navbar__mobile-submenu" id="gs-mobile-paket" role="menu">
            <a href="/paket" class="gs-navbar__mobile-link" role="menuitem">Semua Paket</a>
            <a href="/paket/souvenir-tradisional" class="gs-navbar__mobile-link" role="menuitem">Souvenir
              Tradisional</a>
            <a href="/paket/souvenir-modern" class="gs-navbar__mobile-link" role="menuitem">Souvenir Modern</a>
          </div>
          <a href="/portofolio" class="gs-navbar__mobile-link" role="menuitem">Portofolio</a>
          <a href="/blog" class="gs-navbar__mobile-link" role="menuitem">Blog</a>
          <div class="gs-navbar__mobile-cta">
            <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi."
              class="gs-button gs-button--whatsapp" target="_blank" rel="noopener noreferrer"
              style="width:100%;justify-content:center;">Konsultasi WhatsApp</a>
          </div>
        </div>
      </div>
    </nav>
  </header>

  <main id="main-content">
    <section class="gs-section" style="padding-top: clamp(2rem, 4vw, 3.5rem);">
      <div class="gs-container">

        <article class="gs-article">

          <!-- Breadcrumb -->
          <nav aria-label="Breadcrumb">
            <ol class="gs-breadcrumb">
              <li><a href="/" class="gs-breadcrumb__item">Beranda</a></li>
              <li><a href="/blog" class="gs-breadcrumb__item">Blog</a></li>
              <li class="gs-breadcrumb__item gs-breadcrumb__item--active" aria-current="page">{html.escape(h1)}</li>
            </ol>
          </nav>

          <!-- Header -->
          <header class="gs-article__header" data-gs-animate>
            <div class="gs-article__badge-wrap">
              <span class="gs-article__category">{cfg["category"]}</span>
              <span class="gs-badge">{cfg["topic_tag"]}</span>
            </div>
            <h1 class="gs-article__title">{html.escape(h1)}</h1>
            <div class="gs-article__meta">
              <span class="gs-article__meta-item">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                    clip-rule="evenodd" />
                </svg>
                <strong>Penulis:</strong> <a href="/penulis" class="gs-article__author-link" title="Lihat profil Yudi Abraham">Yudi Abraham</a>
              </span>
              <span class="gs-article__meta-item">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                    clip-rule="evenodd" />
                </svg>
                <strong>Publikasi:</strong> <time datetime="2026-11-03">3 November 2026</time>
              </span>
              <span class="gs-article__meta-item">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                    clip-rule="evenodd" />
                </svg>
                <strong>Pembaruan:</strong> <time datetime="2026-11-03">3 November 2026</time>
              </span>
              <span class="gs-article__meta-item">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                    clip-rule="evenodd" />
                </svg>
                <strong>Waktu Baca:</strong> {cfg["read_time"]}
              </span>
            </div>
          </header>

          <!-- Cover Image (Tepat Setelah Header) -->
          <div class="gs-article__cover" data-gs-animate="slide">
            <img src="{cfg["hero_img"]}"
              alt="{html.escape(cfg["hero_alt"])}" width="1200"
              height="630" loading="eager" />
            <div class="gs-article__caption">
              {html.escape(cfg["cover_caption"])}
            </div>
          </div>

          <!-- TOC (Tepat Setelah Gambar Utama) -->
          <nav data-gs-animate class="gs-article__toc" aria-label="Daftar Isi Artikel">
            <button type="button" class="gs-article__toc-toggle" aria-expanded="true" aria-controls="toc-list-body">
              <span class="gs-article__toc-label">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1z"
                    clip-rule="evenodd" />
                </svg>
                Daftar Isi Artikel
              </span>
              <svg class="gs-article__toc-chevron" viewBox="0 0 16 16" fill="none" stroke="currentColor"
                stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M4 6l4 4 4-4" />
              </svg>
            </button>
            <div class="gs-article__toc-body" id="toc-list-body">
              <ol class="gs-article__toc-list">
{toc_list_str}
              </ol>
            </div>
          </nav>

          <!-- Body (Dilanjutkan Setelah Daftar Isi) -->
          <div class="gs-article__body">

            <!-- Lead Paragraph Pembuka Konteks -->
            <p class="gs-article__lead">
              Menemukan <a href="/">vendor souvenir pernikahan</a> yang mampu menerjemahkan konsep acara menjadi cinderamata berkesan memerlukan kecermatan pada aspek portofolio, transparansi biaya, dan komitmen jadwal. Panduan komprehensif ini menyajikan wawasan menyeluruh agar persiapan souvenir pernikahan Anda terkelola sempurna.
            </p>

            <!-- Key Takeaway Box -->
            <aside class="gs-article__key-takeaway" aria-labelledby="takeaway-head">
              <div data-gs-animate class="gs-article__key-takeaway-head" id="takeaway-head">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    clip-rule="evenodd" />
                </svg>
                Ringkasan Inti Panduan
              </div>
              {takeaway_str}
            </aside>

            <!-- Content Sections -->
{all_sections_str}

            <!-- FAQ Section -->
            <section class="gs-article__faq-wrap" id="faq-souvenir" aria-labelledby="faq-title">
              <h2 class="gs-article__faq-title" id="faq-title">Pertanyaan Umum (FAQ)</h2>
{faq_items_str}
            </section>

            <!-- Kesimpulan -->
            <section class="gs-article__section" id="kesimpulan">
              <h2>Kesimpulan Praktis</h2>
              {kesimpulan_str}
            </section>

            <!-- Author Bio -->
            <div class="gs-article__author-box">
              <a href="/penulis" class="gs-article__author-avatar" title="Lihat Profil Yudi Abraham">
                <img src="/assets/images/yudi-abraham.jpg" alt="Yudi Abraham" width="68" height="68" loading="lazy" />
              </a>
              <div class="gs-article__author-info">
                <h4><a href="/penulis" class="gs-article__author-heading-link" title="Lihat Profil Penulis">Yudi Abraham</a></h4>
                <span class="gs-article__author-role">Manajer Operasional &amp; Produksi Cinderamata</span>
                <p>
                  Mengawal ketepatan jadwal produksi, standarisasi kemasan premium, dan jaminan ekspedisi aman untuk ratusan acara pernikahan di seluruh nusantara.
                </p>
                <a href="/penulis" class="gs-article__author-more-link" title="Lihat profil dan karya tulisan Yudi Abraham">
                  Lihat Profil Lengkap &rarr;
                </a>
              </div>
            </div>

            <!-- Tags & Social Share -->
            <div class="gs-article__tags-share">
              <div class="gs-article__tags">
                <span style="font-size:0.8rem;color:var(--gs-muted);font-weight:600;">Tags:</span>
                {tags_str}
              </div>
              <div class="gs-article__share">
                <span class="gs-article__share-label">Bagikan:</span>
                <a href="https://api.whatsapp.com/send?text={html.escape(h1)}%20{canonical_url}"
                  target="_blank" rel="noopener noreferrer" class="gs-article__share-btn gs-article__share-btn--wa"
                  title="Bagikan ke WhatsApp" aria-label="Bagikan ke WhatsApp">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path
                      d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
                  </svg>
                </a>
                <button type="button" class="gs-article__share-btn gs-article__share-btn--copy"
                  title="Salin Tautan Artikel" aria-label="Salin tautan artikel">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round">
                    <path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71" />
                    <path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Product Recommendation Card -->
            <div class="gs-article__product-rec">
              <div class="gs-article__product-rec-img">
                <img src="{cfg["hero_img"]}"
                  alt="{html.escape(cfg["product_rec"]["title"])}" width="300" height="300" loading="lazy" />
              </div>
              <div class="gs-article__product-rec-info">
                <span class="badge">{cfg["product_rec"]["badge"]}</span>
                <h4>{html.escape(cfg["product_rec"]["title"])}</h4>
                <p>{html.escape(cfg["product_rec"]["desc"])}</p>
                <div style="font-size:0.85rem;color:var(--gs-green-800);font-weight:600;">{html.escape(cfg["product_rec"]["note"])}</div>
              </div>
              <div class="gs-article__product-rec-action">
                <a href="{cfg["product_rec"]["btn_link"]}" class="gs-button gs-button--primary gs-button--sm">{html.escape(cfg["product_rec"]["btn_text"])}</a>
              </div>
            </div>

          </div>

          <!-- Related Articles Grid -->
          <section class="gs-article__related" aria-labelledby="related-title">
            <h2 class="gs-article__related-title" id="related-title">Artikel Panduan Terkait</h2>
            <div class="gs-article__related-grid">
{rel_cards_str}
            </div>
          </section>

        </article>

      </div>
    </section>
  </main>

  <!-- FOOTER -->
  <footer class="gs-footer">
    <div class="gs-container">
      <div class="gs-footer__grid">
        <!-- Brand -->
        <div>
          <a href="/" class="gs-footer__brand-name" aria-label="Souvenir Pernikahan — Beranda">
            <div class="gs-footer__brand-logo" aria-hidden="true"><img src="/assets/profile/logo-footer-108.webp"
                alt="Logo Souvenir Pernikahan Footer" width="54" height="54" loading="lazy" decoding="async" /></div>
            <span>Souvenir Pernikahan</span>
          </a>
          <p class="gs-footer__desc">
            Penyedia souvenir pernikahan elegan, cinderamata custom unik, dan kemasan berkelas di Malang untuk pengiriman ke seluruh Indonesia. Dibuat dengan perhatian penuh terhadap mutu dan detail.
          </p>
          <a href="https://maps.app.goo.gl/fQQ1reAUBefTYWb27" class="gs-footer__location-item" target="_blank"
            rel="noopener noreferrer" aria-label="Lihat lokasi Souvenir Pernikahan di Google Maps">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path
                d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" />
            </svg>
            <span>Jl. Band. Palmerah No.D3-35B, Cemorokandang, Kec. Kedungkandang, Kota Malang, Jawa Timur 65138, Indonesia</span>
          </a>
        </div>

        <!-- Halaman -->
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

        <!-- Kategori Paket -->
        <div>
          <p class="gs-footer__heading">Kategori Paket</p>
          <ul class="gs-footer__links">
            <li><a href="/paket" class="gs-footer__link">Semua Paket</a></li>
            <li><a href="/paket/souvenir-tradisional" class="gs-footer__link">Souvenir Tradisional</a></li>
            <li><a href="/paket/souvenir-modern" class="gs-footer__link">Souvenir Modern</a></li>
          </ul>
        </div>

        <!-- Kontak -->
        <div>
          <p class="gs-footer__heading">Kontak</p>
          <div class="gs-footer__contact-list">
            <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi."
              class="gs-footer__contact-link" target="_blank" rel="noopener noreferrer"
              aria-label="WhatsApp Souvenir Pernikahan">
              <span class="gs-footer__contact-icon">
                <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path
                    d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
              </svg>
            </span>
            <span>+62 821-3108-7971</span>
          </a>
          <a href="https://www.instagram.com/sakasouvenirmlg/" class="gs-footer__contact-link" target="_blank"
            rel="noopener noreferrer" aria-label="Instagram @sakasouvenirmlg">
            <span class="gs-footer__contact-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                stroke-linejoin="round" aria-hidden="true">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5" />
                <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" />
                <line x1="17.5" y1="6.5" x2="17.51" y2="6.5" />
              </svg>
            </span>
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

<div class="gs-whatsapp-float" aria-label="Hubungi via WhatsApp">
  <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi%20souvenir%20pernikahan."
    class="gs-whatsapp-float__btn" target="_blank" rel="noopener noreferrer" aria-label="Chat via WhatsApp">
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path
        d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
    </svg>
  </a>
</div>

<!-- Back to Top Button -->
<button type="button" class="gs-back-to-top" id="gs-back-to-top" aria-label="Kembali ke atas">
  <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
    <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
  </svg>
</button>

<script defer src="/assets/js/main.min.js?v=7"></script>
</body>

</html>'''
    return full_html

# Generate all 4 articles
for cfg in articles_config:
    out_path = f"blog/{cfg['slug']}.html"
    content = build_article_html(cfg)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {out_path} ({len(content)} bytes)")

print("\nAll 4 articles cleanly generated with no raw docx notes!")
