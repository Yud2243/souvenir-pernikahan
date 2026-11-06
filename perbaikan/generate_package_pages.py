# -*- coding: utf-8 -*-
"""
Script to generate:
1. paket/detail-souvenir-modern.html
2. paket/detail-souvenir-tradisional.html
and update:
3. paket/souvenir-modern.html (remove modal, update products/alt/SEO)
4. paket/souvenir-tradisional.html (remove modal, update products/alt/SEO)
5. sitemap.xml
"""

import json
import os
import re

# Load product data definitions
modern_products = [
    {
        "slug": "hampers-vip-gift-set-box",
        "title": "Paket Hampers Souvenir Pernikahan VIP Gift Set Box",
        "badge": "VIP Wedding Gift",
        "image": "/assets/images/souvenir-seminar-kit.webp",
        "alt": "Souvenir Pernikahan Paket Hampers VIP Gift Set Box Hijau Botol Monogram Emas",
        "lead": "Paket hampers souvenir pernikahan eksklusif untuk tamu VIP kehormatan dalam hardbox magnetik hijau botol beraksen foil emas, berisi buku agenda kenangan hardcover, pena metalik grafir laser inisial pengantin, mug keramik matte, dan dompet kartu kulit berkelas.",
        "price": "Rp 125.000 - Rp 185.000",
        "min_order": "50 pcs",
        "custom": "Grafir Laser Nama & Tanggal, Foil Emas",
        "packaging": "Hardbox Magnetik Hijau Botol + Pita Satin Emas",
        "features": [
            "Hardbox magnetik tebal hijau botol dengan cetak hotprint foil emas mewah",
            "Buku agenda hardcover faux leather A5 berpita pembatas monogram mempelai",
            "Pena metalik ballpoint premium berfinishing laser engrave nama pasangan",
            "Mug keramik matte hijau botol custom inisial pengantin & tanggal akad",
            "Card holder dompet kartu kulit eksklusif dengan ornamen pelat logam presisi"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Paket Hampers Souvenir Pernikahan VIP Gift Set Box untuk acara pernikahan saya."
    },
    {
        "slug": "tumbler-kopi-stainless-sage-green",
        "title": "Souvenir Pernikahan Tumbler Kopi Stainless Sage Green Monogram",
        "badge": "Tumbler Pernikahan",
        "image": "/assets/images/souvenir-tumbler-custom.webp",
        "alt": "Souvenir Pernikahan Tumbler Kopi Stainless Sage Green Monogram Grafir Laser",
        "lead": "Souvenir pernikahan tumbler kopi stainless steel double-wall tahan panas dan dingin warna sage green matte dengan grafir laser monogram nama pengantin, tutup flip anti tumpah dan gift box silinder eksklusif.",
        "price": "Rp 45.000 - Rp 65.000",
        "min_order": "100 pcs",
        "custom": "Grafir Laser Monogram Floral",
        "packaging": "Silinder Tabung Kaku + Pita Grosgrain",
        "features": [
            "Stainless steel SUS 304 food-grade double-wall tahan panas & dingin 8 jam",
            "Finishing powder coating matte warna sage green elegan tahan gores",
            "Grafir laser permanen presisi tinggi inisial monogram floral pengantin",
            "Tutup transparan anti tumpah dengan lubang teguk silikon ergonomis",
            "Gift box silinder tabung kaku tebal berpita grosgrain emerald mewah"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Tumbler Kopi Stainless Sage Green Monogram."
    },
    {
        "slug": "tumbler-termos-ivory-rose-gold",
        "title": "Souvenir Pernikahan Tumbler Termos Stainless Ivory Rose Gold",
        "badge": "Termos Pernikahan",
        "image": "/assets/images/tumbler-souvenir.webp",
        "alt": "Souvenir Pernikahan Tumbler Termos Stainless Ivory Aksen Rose Gold",
        "lead": "Termos travel souvenir pernikahan berbahan stainless steel SUS 304 food-grade warna ivory beraksen rose gold berkilau, grafir inisial tanggal akad nikah, dikemas gift box tabung tekstur anyam berpita satin dusty rose.",
        "price": "Rp 55.000 - Rp 75.000",
        "min_order": "100 pcs",
        "custom": "Grafir Laser Laser Engrave Rose Gold",
        "packaging": "Tabung Anyam Berserat + Pita Satin Dusty Rose",
        "features": [
            "Vacuum insulation double-wall tahan dingin & panas hingga 12 jam",
            "Bodi stainless steel berfinishing matte ivory beraksen pelat rose gold",
            "Grafir laser permanent monogram inisial mempelai dan tahun acara",
            "Gift box tabung silinder tekstur anyam berserat berpita satin dusty rose",
            "Kapasitas 450 ml praktis untuk mobilitas harian berkelas"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Tumbler Termos Stainless Ivory Rose Gold."
    },
    {
        "slug": "glass-tumbler-borosilikat-tutup-bambu",
        "title": "Souvenir Pernikahan Glass Tumbler Kaca Borosilikat Tutup Bambu",
        "badge": "Tumbler Kaca Estetik",
        "image": "/assets/images/glass-tumbler-souvenir.webp",
        "alt": "Souvenir Pernikahan Glass Tumbler Borosilikat Tutup Bambu Estetik",
        "lead": "Gelas can-tumbler souvenir pernikahan kaca borosilikat transparan tebal dengan tutup kayu bambu berukir monogram dan sedotan kaca reusable ramah lingkungan, cocok untuk resepsi modern minimalis.",
        "price": "Rp 35.000 - Rp 48.000",
        "min_order": "100 pcs",
        "custom": "Ukir Laser Kayu Bambu / Sablon Kaca",
        "packaging": "Box Kraft Jendela Mika + Pita Rami",
        "features": [
            "Kaca borosilikat ultra bening tahan perubahan suhu dingin & panas ekstrem",
            "Tutup kayu bambu alami dilengkapi seal karet silikon rapat anti tumpah",
            "Sedotan kaca bengkok reusable ramah lingkungan & mudah dibersihkan",
            "Grafir laser monogram nama pengantin pada tutup bambu atau bodi kaca",
            "Kemasan box craft jendela mika berpita rami dan thank you tag"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Glass Tumbler Borosilikat Tutup Bambu."
    },
    {
        "slug": "plakat-akrilik-souvenir-pernikahan",
        "title": "Plakat Akrilik Souvenir Pernikahan Dudukan Kayu Solid",
        "badge": "Akrilik Pernikahan",
        "image": "/assets/images/souvenir-plakat-akrilik.webp",
        "alt": "Souvenir Pernikahan Plakat Akrilik Kristal Bening Dudukan Kayu Solid",
        "lead": "Plakat akrilik souvenir pernikahan kristal bening potongan laser dengan dudukan kayu solid walnut, diukir grafir kaligrafi nama kedua mempelai dan tanggal pernikahan sebagai cinderamata kenangan saksi nikah & keluarga besar.",
        "price": "Rp 65.000 - Rp 95.000",
        "min_order": "20 pcs",
        "custom": "Grafir Laser Kaligrafi Nama Mempelai",
        "packaging": "Hardbox Beludru Kancing Magnetik Eksklusif",
        "features": [
            "Akrilik cor grade A ketebalan 8-10 mm ultra-clear jernih tanpa baret",
            "Dudukan alas kayu solid walnut berfinishing natural satin doff",
            "Grafir laser kaligrafi nama mempelai & tanggal akad nikah sangat tajam",
            "Sangat berkesan untuk cinderamata saksi nikah, orang tua, & tamu kehormatan",
            "Kemasan kotak bludru kancing magnetik eksklusif warna biru tua atau hijau"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Plakat Akrilik Souvenir Pernikahan Dudukan Kayu Solid."
    },
    {
        "slug": "set-teh-herbal-tabung-kaca-saringan-emas",
        "title": "Souvenir Pernikahan Teh Herbal Tabung Kaca & Saringan Emas",
        "badge": "Botanical Tea Favor",
        "image": "/assets/images/tea-infuser-souvenir.webp",
        "alt": "Souvenir Pernikahan Set Teh Herbal Tabung Kaca dan Saringan Bola Emas",
        "lead": "Set souvenir pernikahan botanical gift box berisi infuser saringan teh bola rantai logam warna emas berbandul inisial pengantin dan tabung kaca teh bunga Chamomile & Lavender wangi alami.",
        "price": "Rp 40.000 - Rp 58.000",
        "min_order": "100 pcs",
        "custom": "Bandul Koin Inisial Monogram & Hangtag",
        "packaging": "Slide Kraft Box + Pita Katun Sage Green",
        "features": [
            "Saringan teh bola logam stainless finishing warna emas anti karat",
            "Bandul koin gantungan inisial monogram personal pada rantai infuser",
            "Dua tabung kaca cork lid berisi teh bunga Chamomile & French Lavender",
            "Box slide kraft natural berpita katun botanical sage green",
            "Disertai kartu panduan seduh herbal tea wedding favor"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Teh Herbal Tabung Kaca & Saringan Emas."
    },
    {
        "slug": "kaleng-teh-artisan-logam-tutup-gold",
        "title": "Souvenir Pernikahan Kaleng Teh Artisan Logam Tutup Gold",
        "badge": "Artisan Tea Tin",
        "image": "/assets/images/tea-tin-souvenir.webp",
        "alt": "Souvenir Pernikahan Kaleng Teh Artisan Logam Tutup Gold Monogram",
        "lead": "Kaleng tabung logam tinplate kedap udara souvenir pernikahan dengan penutup ganda warna emas mewah dan label kustom inisial mempelai, berisi daun teh seduh melati artisan pilihan.",
        "price": "Rp 28.000 - Rp 42.000",
        "min_order": "100 pcs",
        "custom": "Label Linen Waterproof Inisial Mempelai",
        "packaging": "Kaleng Tinplate Double-Lid Emas + Tali Rami",
        "features": [
            "Kaleng logam tinplate food grade double-lid kedap udara tahan lembap",
            "Tutup dan alas logam dilapisi warna emas berkilau mewah",
            "Label botanical waterproof bertekstur linen kustom inisial nama mempelai",
            "Berisi daun teh melati kualitas ekspor pilihan beraroma harum",
            "Aksen lilitan tali rami rustic dan hangtag kartu ucapan terima kasih"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Kaleng Teh Artisan Logam Tutup Gold."
    },
    {
        "slug": "botol-dispenser-sabun-pump-gold",
        "title": "Souvenir Pernikahan Botol Dispenser Sabun Pump Gold Mewah",
        "badge": "Home Amenity Wedding",
        "image": "/assets/images/botol-sabun-custom.webp",
        "alt": "Souvenir Pernikahan Botol Dispenser Sabun Pump Gold Mewah Kustom Nama",
        "lead": "Botol dispenser sabun cair souvenir pernikahan model hotel estetik dengan kepala pompa warna emas mengkilap, label botanical kustom nama pengantin dan kemasan hardbox berpita satin zaitun.",
        "price": "Rp 32.000 - Rp 45.000",
        "min_order": "100 pcs",
        "custom": "Stiker Botanical Waterproof Monogram Pasangan",
        "packaging": "Hardbox Kokoh + Pita Satin Zaitun",
        "features": [
            "Botol bening tebal berkapasitas 350 ml model hotel estetik minimalis",
            "Kepala pompa dispenser sabun berlapis warna emas berkilau halus",
            "Stiker label botanical anti air kustom monogram nama pasangan pengantin",
            "Gantungan hangtag kraft foil emas dan kartu ucapan doa restu",
            "Dikemas dalam hardbox kokoh berpita satin zaitun atau dusty pink"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Botol Dispenser Sabun Pump Gold Mewah."
    },
    {
        "slug": "lilin-aromaterapi-jar-frosted-gold",
        "title": "Souvenir Pernikahan Lilin Aromaterapi Jar Frosted Tutup Gold",
        "badge": "Aromaterapi Pernikahan",
        "image": "/assets/images/candle-souvenir.webp",
        "alt": "Souvenir Pernikahan Lilin Aromaterapi Jar Kaca Frosted Tutup Logam Gold",
        "lead": "Lilin aromaterapi soy wax 100% alami souvenir pernikahan dalam jar kaca frosted putih buram berpenutup logam warna emas, diikat pita satin ivory dengan hangtag nama mempelai wangi Wild Rose & Oud.",
        "price": "Rp 25.000 - Rp 38.000",
        "min_order": "100 pcs",
        "custom": "Hotprint Foil Emas Inisial & Hangtag",
        "packaging": "Pita Satin Ivory + Box Kaca Jendela",
        "features": [
            "Jar kaca frosted semi-transparan berpenutup logam emas kedap aroma",
            "100% natural handpoured soy candle bebas asap beraroma Wild Rose & Oud",
            "Sumbu katun ramah lingkungan tanpa timbal dengan waktu bakar 25 jam",
            "Label sablon atau stiker hotprint foil emas inisial nama mempelai",
            "Pita satin ivory mewah dan kartu terima kasih wedding keepsake"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Lilin Aromaterapi Jar Frosted Tutup Gold."
    },
    {
        "slug": "botol-parfum-kaca-amber-mewah",
        "title": "Souvenir Pernikahan Botol Parfum Kaca Amber Mewah",
        "badge": "Parfum Souvenir Wedding",
        "image": "/assets/images/perfume-bottle-souvenir.webp",
        "alt": "Souvenir Pernikahan Botol Parfum Kaca Amber Rounded Pebble Mewah",
        "lead": "Botol parfum travel souvenir pernikahan kaca tebal bentuk rounded pebble dengan sprayer semprot halus dan tutup amber hangat, dikemas kotak beludru eksklusif berinisial nama pasangan.",
        "price": "Rp 30.000 - Rp 45.000",
        "min_order": "100 pcs",
        "custom": "Emboss Nama Pengantin & Pilihan Varian Parfum",
        "packaging": "Box Kado Beludru Velvet Berikat Pita",
        "features": [
            "Bodi botol kaca tebal jernih model rounded pebble eksklusif",
            "Tutup botol warna amber keemasan berkarakter modern dan hangat",
            "Pompa semprot nozzle spray halus berkabut merata tahan bocor",
            "Dapat dipesan kosong atau diisi eau de parfum pilihan aroma pengantin",
            "Box kado beludru velvet dengan cetak nama foil emas berkilau"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Botol Parfum Kaca Amber Mewah."
    },
    {
        "slug": "minyak-esensial-pipet-kaca-box-beludru",
        "title": "Souvenir Pernikahan Minyak Esensial Pipet Kaca & Box Beludru",
        "badge": "Essential Oil Wedding",
        "image": "/assets/images/souvenir-botol-minyak.webp",
        "alt": "Souvenir Pernikahan Minyak Esensial Pipet Kaca Gift Box Pita Beludru",
        "lead": "Minyak esensial aromaterapi murni souvenir pernikahan dalam botol kaca pipet tetes berlabel foil emas, berdampingan gift box putih berpita beludru sage green dan buket bunga lavender kering.",
        "price": "Rp 28.000 - Rp 42.000",
        "min_order": "100 pcs",
        "custom": "Foil Emas Nama Mempelai + Buket Lavender Kering",
        "packaging": "Gift Box Putih Berserat + Pita Beludru Sage Green",
        "features": [
            "Botol kaca penetes (dropper pipette) 10 ml dengan kerah logam emas",
            "Minyak esensial murni therapeutic grade Lavender & Geranium menenangkan",
            "Gift box tebal putih berserat berpita beludru sage green mewah",
            "Buket mini dried lavender asli dan hangtag nama kedua mempelai",
            "Sangat disukai tamu undangan karena fungsional dan menenangkan"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Minyak Esensial Pipet Kaca & Box Beludru."
    },
    {
        "slug": "silk-scrunchie-set-sutra-bridesmaid",
        "title": "Souvenir Pernikahan Silk Scrunchie Set Sutra Bridesmaid",
        "badge": "Silk Bridesmaid Favor",
        "image": "/assets/images/silk-scrunchie-souvenir.webp",
        "alt": "Souvenir Pernikahan Silk Scrunchie Set Sutra Mulberry Bridesmaid",
        "lead": "Set ikat rambut kuncir silk scrunchie souvenir pernikahan berbahan kain sutra mulberry anti kusut dalam gradasi warna feminin mewah, dikemas gift box mika berpita satin elegan.",
        "price": "Rp 26.000 - Rp 38.000",
        "min_order": "100 pcs",
        "custom": "Kartu Bridesmaid Kustom Nama Sahabat",
        "packaging": "Box Mika Tebal + Pita Satin Senada",
        "features": [
            "Bahan kain sutra satin mulberry halus anti kusut & menjaga rambut sehat",
            "Set gradasi 5 warna feminin: Ivory, Blush, Champagne, Nude, Dusty Rose",
            "Karet elastis premium awet tidak mudah melar atau putus",
            "Box kemasan mika transparan tebal berpita satin senada",
            "Sangat populer untuk souvenir bridesmaid, siraman, dan sahabat pengantin"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Silk Scrunchie Set Sutra Bridesmaid."
    },
    {
        "slug": "pouch-serut-beludru-velvet-monogram",
        "title": "Souvenir Pernikahan Pouch Serut Beludru Velvet Bordir Monogram",
        "badge": "Velvet Pouch Wedding",
        "image": "/assets/images/velvet-pouch-souvenir.webp",
        "alt": "Souvenir Pernikahan Pouch Serut Beludru Velvet Bordir Monogram Emas",
        "lead": "Pouch serut souvenir pernikahan berbahan kain beludru velvet tebal premium dengan bordir benang emas inisial nama pengantin, tali serut kepang ganda dan ornamen bandul kancing etnik.",
        "price": "Rp 18.000 - Rp 28.000",
        "min_order": "150 pcs",
        "custom": "Bordir Komputer Monogram Inisial Emas",
        "packaging": "Kemasan Mika Plastik / Kotak Kraft Bertali",
        "features": [
            "Kain beludru velvet premium ekstra lembut dan tebal",
            "Bordir inisial monogram detail dengan benang emas mengkilap",
            "Tali serut kepang ganda tebal dengan bandul aksen emas",
            "Pilihan warna mewah: Emerald Green, Midnight Navy, Burgundy, Rose Gold",
            "Multifungsi untuk wadah perhiasan, makeup kecil, maupun aksesoris"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Pouch Serut Beludru Velvet Bordir Monogram."
    },
    {
        "slug": "eco-tote-bag-kanvas-cutlery-set",
        "title": "Souvenir Pernikahan Eco Tote Bag Kanvas & Cutlery Set Kayu",
        "badge": "Eco Wedding Favor",
        "image": "/assets/images/souvenir-tote-bag.webp",
        "alt": "Souvenir Pernikahan Eco Tote Bag Kanvas dan Set Alat Makan Kayu Ramah Lingkungan",
        "lead": "Tas jinjing tote bag souvenir pernikahan berbahan kanvas katun tebal motif botanical dipadukan set sendok garpu kayu alami ramah lingkungan dalam pouch serut blacu berpita rami.",
        "price": "Rp 24.000 - Rp 35.000",
        "min_order": "100 pcs",
        "custom": "Sablon Nama Pasangan & Tanggal Resepsi",
        "packaging": "Pouch Blacu Serut + Pita Tali Rami Rustic",
        "features": [
            "Bahan kain kanvas katun twill tebal 10 oz jahitan rapi kuat",
            "Sablon cetak motif daun botanical minimalis nama pengantin",
            "Dilengkapi set alat makan sendok, garpu, & sumpit kayu jati alami",
            "Pouch serut blacu ramah lingkungan penyimpan cutlery",
            "Dikemas ikat tali rami rustic dan hangtag ucapan doa pengantin"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Eco Tote Bag Kanvas & Cutlery Set Kayu."
    }
]

tradisional_products = [
    {
        "slug": "kipas-lipat-batik-tulis-kayu-jati",
        "title": "Souvenir Pernikahan Kipas Lipat Batik Tulis Rangka Kayu Jati",
        "badge": "Kipas Batik Pernikahan",
        "image": "/assets/images/kipas-batik-souvenir.webp",
        "alt": "Souvenir Pernikahan Kipas Lipat Batik Tulis Rangka Kayu Jati Berukir",
        "lead": "Kipas lipat souvenir pernikahan kain katun batik tulis motif parang dan sekar jagad klasik dengan rangka bilah kayu jati berukir halus, rumbai sutra anggun, serta box kraft rustic bertali rami.",
        "price": "Rp 22.000 - Rp 35.000",
        "min_order": "100 pcs",
        "custom": "Ukir Inisial Nama Mempelai pada Bilah Kayu",
        "packaging": "Gift Box Kraft Rustic + Dried Flowers",
        "features": [
            "Kain katun batik tulis motif parang & sekar jagad klasik khas nusantara",
            "Rangka bilah kayu jati solid perhutani berukir halus kokoh",
            "Aksen rumbai benang sutra krem keemasan menjuntai anggun",
            "Kemasan gift box kraft rustic tebal bertali rami dan dried floral",
            "Dapat dicetak ukir inisial nama mempelai pada bilah utama kayu kipas"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Kipas Lipat Batik Tulis Rangka Kayu Jati."
    },
    {
        "slug": "pouch-dompet-tenun-lurik-tradisional",
        "title": "Souvenir Pernikahan Pouch Dompet Tenun Lurik Tradisional",
        "badge": "Tenun Etnik Pernikahan",
        "image": "/assets/images/pouch-tenun-souvenir.webp",
        "alt": "Souvenir Pernikahan Pouch Dompet Tenun Lurik Tradisional Kancing Kelapa",
        "lead": "Dompet pouch souvenir pernikahan tenun lurik handmade bertekstur etnik alami bergaris bumi dengan kancing batok kelapa alami, dikemas cantik dalam gift box kraft berpita rami.",
        "price": "Rp 18.000 - Rp 27.000",
        "min_order": "100 pcs",
        "custom": "Emboss Inisial Mempelai pada Label Kulit",
        "packaging": "Gift Box Kraft Natural + Tali Rami",
        "features": [
            "Kain tenun lurik asli alat tenun bukan mesin (ATBM) khas nusantara",
            "Kancing pengait dari tempurung batok kelapa alami ramah lingkungan",
            "Lapisan furing dalam blacu halus menjaga bentuk dompet tetap rapi",
            "Label kulit sintetis emboss inisial nama kedua mempelai",
            "Gift box kraft natural berhias tali rami dan thank you card"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Pouch Dompet Tenun Lurik Tradisional."
    },
    {
        "slug": "besek-anyaman-bambu-bunga-kering",
        "title": "Souvenir Pernikahan Besek Anyaman Bambu Hias Bunga Kering",
        "badge": "Anyaman Bambu Ramah Lingkungan",
        "image": "/assets/images/besek-bambu-souvenir.webp",
        "alt": "Souvenir Pernikahan Besek Anyaman Bambu Tradisional Hias Bunga Kering",
        "lead": "Wadah besek bambu souvenir pernikahan anyaman kubus tradisional karya pengrajin lokal, diikat tali rami natural dan dihias buket bunga kering asli berisi rempah wangi nusantara.",
        "price": "Rp 19.000 - Rp 29.000",
        "min_order": "100 pcs",
        "custom": "Hangtag Kaligrafi Nama Pengantin & Dried Flower",
        "packaging": "Anyaman Besek Bambu Natural + Tali Rami",
        "features": [
            "Anyaman bambu natural ramah lingkungan buatan perajin lokal nusantara",
            "Hiasan buket dried flower marigold, bunga gandum, & daun eukaliptus",
            "Diikat tali rami serat goni alami dengan lilitan pita simpul rapi",
            "Bisa diisi rempah wangi, teh melati, kue kering, atau dupa aromaterapi",
            "Hangtag kraft kaligrafi nama pengantin & tanggal resepsi pernikahan"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Besek Anyaman Bambu Hias Bunga Kering."
    },
    {
        "slug": "sepasang-sendok-kayu-jati-alami",
        "title": "Souvenir Pernikahan Sepasang Sendok Garpu Kayu Jati Alami",
        "badge": "Kayu Jati Pernikahan",
        "image": "/assets/images/wooden-spoon-souvenir.webp",
        "alt": "Souvenir Pernikahan Sepasang Sendok Kayu Jati Alami Food Grade",
        "lead": "Sepasang sendok makan souvenir pernikahan berbahan kayu jati solid perhutani halus bertekstur urat kayu eksotis non-toxic food-grade, diikat lilitan tali rami rustic dan hangtag inisial nama pengantin.",
        "price": "Rp 16.000 - Rp 24.000",
        "min_order": "150 pcs",
        "custom": "Grafir Laser Nama & Tanggal pada Gagang Sendok",
        "packaging": "Pouch Blacu Serut / Box Kraft Mika",
        "features": [
            "Kayu jati solid alami berkualitas food grade perhutani Jawa Timur",
            "Finishing natural beeswax non-toxic tahan panas dan aman makanan",
            "Grafir laser inisial kedua mempelai pada gagang sendok presisi",
            "Lilitan tali rami rustic beraksen daun pakis atau bunga kering",
            "Kemasan pouch serut blacu atau box kraft dengan jendela mika"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Sepasang Sendok Garpu Kayu Jati Alami."
    },
    {
        "slug": "madu-hutan-jar-heksagonal-tutup-renda",
        "title": "Souvenir Pernikahan Madu Hutan Jar Heksagonal Tutup Renda",
        "badge": "Madu Murni Pernikahan",
        "image": "/assets/images/honey-souvenir.webp",
        "alt": "Souvenir Pernikahan Madu Hutan Jar Heksagonal Tutup Renda Sendok Kayu",
        "lead": "Madu hutan murni souvenir pernikahan dalam jar kaca heksagonal bersegel kain renda putih cantik berikat tali emas, dilengkapi sendok madu ulir kayu (honey dipper) dan kartu doa keberkahan mempelai.",
        "price": "Rp 25.000 - Rp 37.000",
        "min_order": "100 pcs",
        "custom": "Sendok Kayu Madu + Label Kustom Doa Restu",
        "packaging": "Kain Renda Putih + Tali Emas + Jar Segel",
        "features": [
            "100% Madu hutan murni nusantara asli tanpa campuran gula/pemanis",
            "Jar kaca heksagonal tebal 50-100 ml dengan penutup kedap udara anti bocor",
            "Tutup berhias kain renda katun putih klasik dan tali emas elastis",
            "Sendok ulir madu kayu (honey dipper) mini berpelitur halus",
            "Hangtag doa keberkahan akad nikah dan khasiat madu alami"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Madu Hutan Jar Heksagonal Tutup Renda."
    },
    {
        "slug": "sabun-herbal-batang-alami-handmade",
        "title": "Souvenir Pernikahan Sabun Herbal Batang Alami Handmade",
        "badge": "Sabun Alami Pernikahan",
        "image": "/assets/images/artisan-soap-souvenir.webp",
        "alt": "Souvenir Pernikahan Sabun Herbal Batang Alami Handmade Kertas Samson",
        "lead": "Sabun mandi herbal souvenir pernikahan buatan tangan dari minyak kelapa murni dan ekstrak rempah alami beraroma menenangkan, dibalut kertas samson rustic berikat pita rami ramah lingkungan.",
        "price": "Rp 15.000 - Rp 22.000",
        "min_order": "150 pcs",
        "custom": "Cap Wax Seal Monogram Inisial Pengantin",
        "packaging": "Kertas Samson Kraft + Tali Rami",
        "features": [
            "Proses cold-process handmade tanpa SLS, paraben, atau bahan kimia keras",
            "Bahan dasar minyak kelapa murni, minyak zaitun & ekstrak rempah herbal",
            "Pilihan aroma: Kopi Jawa, Kunyit Asam, Serai Wangi, & Bunga Melati",
            "Kemasan kertas samson kraft ramah lingkungan berikat pita rami",
            "Cap segel lilin wax seal atau stiker inisial monogram pengantin"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Sabun Herbal Batang Alami Handmade."
    },
    {
        "slug": "lilin-aromaterapi-pot-keramik-gerabah",
        "title": "Souvenir Pernikahan Lilin Aromaterapi Pot Gerabah Terakota",
        "badge": "Lilin Gerabah Tradisional",
        "image": "/assets/images/souvenir-lilin-aroma.webp",
        "alt": "Souvenir Pernikahan Lilin Aromaterapi Pot Keramik Gerabah Terakota",
        "lead": "Lilin aromaterapi soy wax souvenir pernikahan dalam pot keramik gerabah tembikar matte berhias segel lilin wax seal botanical sage green, dikemas hardbox kado bertekstur berpita katun.",
        "price": "Rp 24.000 - Rp 36.000",
        "min_order": "100 pcs",
        "custom": "Wax Seal Botanical Inisial Pasangan",
        "packaging": "Hardbox Tekstur Anyaman + Pita Katun Natural",
        "features": [
            "Wadah pot keramik tembikar gerabah matte halus sentuhan bumi (earthy)",
            "100% soy wax alami bebas asap hitam dengan aroma Cendana & Kenanga",
            "Hiasan segel lilin botanical wax seal sage green inisial mempelai",
            "Disertai hardbox kado bertekstur anyaman berpita katun natural",
            "Dapat digunakan kembali sebagai pot tanaman mini setelah lilin habis"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Lilin Aromaterapi Pot Gerabah Terakota."
    },
    {
        "slug": "tatakan-gelas-kayu-jati-grafir-wreath",
        "title": "Souvenir Pernikahan Coaster Tatakan Gelas Kayu Jati Grafir Monogram",
        "badge": "Coaster Kayu Jati",
        "image": "/assets/images/coaster-souvenir.webp",
        "alt": "Souvenir Pernikahan Tatakan Gelas Coaster Kayu Jati Grafir Monogram",
        "lead": "Set tatakan gelas souvenir pernikahan berbahan kayu jati solid bundar berurat kayu mewah dengan grafir laser floral wreath dan inisial kedua mempelai, diikat tali rami dan daun zaitun alami.",
        "price": "Rp 19.000 - Rp 29.000",
        "min_order": "100 pcs",
        "custom": "Grafir Laser Floral Wreath & Inisial",
        "packaging": "Tali Serat Goni + Daun Zaitun Asli",
        "features": [
            "Kayu jati solid perhutani tebal tahan panas, gores, dan cipratan air",
            "Grafir laser presisi tinggi motif lingkaran floral wreath & nama pasangan",
            "Finishing natural oil menonjolkan serat kayu eksotis bernilai seni",
            "Set 2 atau 4 pcs terikat rapi dengan tali serat rami goni",
            "Sangat fungsional digunakan sehari-hari di ruang tamu maupun meja kerja"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Coaster Tatakan Gelas Kayu Jati Grafir Monogram."
    },
    {
        "slug": "mug-keramik-stoneware-rustic-monogram",
        "title": "Souvenir Pernikahan Mug Keramik Stoneware Rustic Monogram",
        "badge": "Mug Keramik Tradisional",
        "image": "/assets/images/ceramic-mug-souvenir.webp",
        "alt": "Souvenir Pernikahan Mug Keramik Stoneware Rustic Monogram Mempelai",
        "lead": "Cangkir cawan keramik stoneware souvenir pernikahan bertekstur bintik alami dengan rim gerabah terakota rustic, dicetak monogram nama mempelai dan dikemas hardbox kraft beralas serutan kayu.",
        "price": "Rp 28.000 - Rp 40.000",
        "min_order": "100 pcs",
        "custom": "Cetak Sablon / Emboss Inisial & Tanggal",
        "packaging": "Hardbox Kraft + Shredded Paper + Pita Katun",
        "features": [
            "Keramik stoneware handmade lokal bersuhu bakar 1200°C food-grade",
            "Warna krem berbintik alami dengan tepian rim terakota rustic estetik",
            "Cetak sablon atau emboss inisial nama pengantin & tanggal resepsi",
            "Gagang cangkir ergonomis kokoh nyaman digenggam",
            "Kemasan hardbox kraft kokoh beralas shredded paper berpita katun"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Mug Keramik Stoneware Rustic Monogram."
    },
    {
        "slug": "pembatas-buku-kuningan-ukir-rumbai-sutra",
        "title": "Souvenir Pernikahan Pembatas Buku Kuningan Ukir Rumbai Sutra",
        "badge": "Kriya Kuningan Pernikahan",
        "image": "/assets/images/brass-bookmark-souvenir.webp",
        "alt": "Souvenir Pernikahan Pembatas Buku Kuningan Ukir Klasik Rumbai Sutra",
        "lead": "Pembatas buku souvenir pernikahan berbahan plat logam kuningan asli finishing antique gold berukir relief bunga klasik abadi, dilengkapi rumbai benang sutra berkilau dan kartu ucapan terima kasih akad.",
        "price": "Rp 17.000 - Rp 26.000",
        "min_order": "100 pcs",
        "custom": "Ukiran Nama Pengantin & Rumbai Pilihan Warna",
        "packaging": "Sleeve Amplop Kraft Serat Daun + Pita",
        "features": [
            "Logam plat kuningan asli finishing antique gold mewah tahan karat",
            "Ukiran relief floral motif bunga teratai klasik mendetail dan presisi",
            "Rumbai benang sutra tenun warna emas berkilau halus",
            "Kancing cincin ornamen kuningan pengikat rumbai berukir monogram",
            "Kemasan sleeve amplop kraft berserat tekstur daun dan pita satin"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Pembatas Buku Kuningan Ukir Rumbai Sutra."
    },
    {
        "slug": "saputangan-kain-linen-bordir-monogram",
        "title": "Souvenir Pernikahan Saputangan Linen Bordir Monogram Klasik",
        "badge": "Linen Sulam Pernikahan",
        "image": "/assets/images/linen-handkerchief-souvenir.webp",
        "alt": "Souvenir Pernikahan Saputangan Kain Linen Bordir Monogram Tepian Hemstitch",
        "lead": "Saputangan souvenir pernikahan kain katun linen serat alami putih bersih dengan tepian sulam lubang hemstitch halus, dihiasi bordir inisial nama mempelai berikat pita kain satin lembut.",
        "price": "Rp 19.000 - Rp 29.000",
        "min_order": "100 pcs",
        "custom": "Bordir Inisial Monogram & Dried Flowers",
        "packaging": "Pita Satin Lembut + Baby's Breath Asli",
        "features": [
            "Bahan kain katun linen murni berserat alami lembut dan menyerap keringat",
            "Tepian keliman lubang sulam openwork hemstitch yang sangat rapi",
            "Bordir inisial monogram nama kedua mempelai warna putih atau emas",
            "Lipatan rapi berikat pita kain katun lembut dan dried baby's breath",
            "Hadiah klasik berkesan mendalam untuk tamu VIP dan keluarga"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Saputangan Linen Bordir Monogram Klasik."
    },
    {
        "slug": "wax-sachet-pewangi-lemari-bunga-kering",
        "title": "Souvenir Pernikahan Wax Sachet Pewangi Lemari Botanical Bunga Kering",
        "badge": "Wax Sachet Pernikahan",
        "image": "/assets/images/wax-sachet-souvenir.webp",
        "alt": "Souvenir Pernikahan Wax Sachet Pewangi Lemari Bunga Kering Alami",
        "lead": "Lilin aromaterapi gantung souvenir pernikahan pengharum lemari dari soy wax alami bertabur bunga kering lavender, kelopak mawar, dan irisan jeruk sitrus dalam gift box kraft bersekat jendela mika.",
        "price": "Rp 18.000 - Rp 28.000",
        "min_order": "100 pcs",
        "custom": "Taburan Bunga Pilihan + Kartu Terima Kasih",
        "packaging": "Gift Box Kraft Bersekat + Mika Bening",
        "features": [
            "100% lilin soy wax murni dipadu essential oil alami wangi tahan lama",
            "Hiasan dried flower asli: Lavender, kelopak mawar, & citrus slice",
            "Tali gantung serat rami natural dan mata itik logam kuningan pelindung",
            "Menyebarkan aroma segar saat digantung di lemari baju atau mobil",
            "Gift box kraft rustic bertingkap mika transparan berpita rami"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Wax Sachet Pewangi Lemari Botanical Bunga Kering."
    },
    {
        "slug": "tanaman-sukulen-mini-pot-balut-goni",
        "title": "Souvenir Pernikahan Tanaman Sukulen Mini Pot Balut Goni Rustic",
        "badge": "Sukulen Hidup Pernikahan",
        "image": "/assets/images/succulent-souvenir.webp",
        "alt": "Souvenir Pernikahan Tanaman Sukulen Mini Pot Balut Kain Goni Rustic",
        "lead": "Tanaman sukulen segar hidup souvenir pernikahan dalam pot mini gerabah terakota dibalut kain goni rustic dan pita tali rami, dilengkapi hangtag doa syukur dan panduan perawatan tanaman.",
        "price": "Rp 15.000 - Rp 24.000",
        "min_order": "100 pcs",
        "custom": "Hangtag 'Let Love Grow' Kustom Nama Mempelai",
        "packaging": "Pot Terakota + Kain Goni + Tali Rami",
        "features": [
            "Tanaman sukulen segar hidup aneka varietas cantik pilihan perawat lokal",
            "Pot mini tanah liat terakota ramah lingkungan berpori sehat",
            "Balutan kain goni bertekstur rustic alami dengan pita simpul rami",
            "Hangtag kartu bertuliskan 'Let Love Grow' dan nama kedua mempelai",
            "Simbol cinta yang terus bertumbuh subur dan tahan banting"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Tanaman Sukulen Mini Pot Balut Goni Rustic."
    },
    {
        "slug": "cermin-saku-lipat-logam-ukir-klasik-emas",
        "title": "Souvenir Pernikahan Cermin Saku Lipat Logam Ukir Klasik Emas",
        "badge": "Cermin Klasik Pernikahan",
        "image": "/assets/images/compact-mirror-souvenir.webp",
        "alt": "Souvenir Pernikahan Cermin Saku Lipat Logam Ukir Klasik Emas Antik",
        "lead": "Cermin saku portabel lipat dua sisi souvenir pernikahan berbingkai logam warna emas antik dengan ukiran relief bunga klasik timbul mewah, tombol buka otomatis dan kantong serut beludru pelindung.",
        "price": "Rp 20.000 - Rp 31.000",
        "min_order": "100 pcs",
        "custom": "Kartu Ucapan Kustom & Pouch Beludru",
        "packaging": "Pouch Beludru Hitam + Hardbox Mika",
        "features": [
            "Casing logam alloy warna antique gold berkilau tahan lama & anti pudar",
            "Ukiran relief floral motif bunga klasik timbul memukau berbobot mantap",
            "Dua cermin kaca: cermin normal jernih dan cermin pembesar 2x",
            "Tombol pembuka berpegas otomatis mudah dioperasikan satu tangan",
            "Disertai pouch pelindung beludru hitam dan kartu ucapan kustom"
        ],
        "wa_text": "Halo Souvenir Pernikahan, saya tertarik konsultasi Souvenir Pernikahan Cermin Saku Lipat Logam Ukir Klasik Emas."
    }
]

print("Product definitions loaded: %d Modern, %d Tradisional" % (len(modern_products), len(tradisional_products)))
# -*- coding: utf-8 -*-
import json
import os
import re



ORG_LOCALBUSINESS = {
    "@type": [
        "Organization",
        "LocalBusiness"
    ],
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
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+6282131087971",
        "contactType": "customer service",
        "areaServed": "ID",
        "availableLanguage": ["Indonesian"]
    },
    "sameAs": [
        "https://www.instagram.com/sakasouvenirmlg/"
    ],
    "hasMap": "https://www.google.com/maps?q=-7.9839,112.6214",
    "knowsAbout": [
        "Souvenir Pernikahan",
        "Souvenir Pernikahan Modern",
        "Souvenir Pernikahan Tradisional",
        "Hampers Pernikahan VIP",
        "Cinderamata Akad Nikah",
        "Kemasan Kustom Souvenir",
        "Tumbler Custom Monogram"
    ]
}

def extract_prices(price_str):
    nums = re.findall(r'\d+', price_str.replace('.', ''))
    if len(nums) >= 2:
        return int(nums[0]), int(nums[1])
    elif len(nums) == 1:
        return int(nums[0]), int(nums[0])
    return 15000, 50000

def generate_detail_page(package_type):
    is_modern = (package_type == "modern")
    products = modern_products if is_modern else tradisional_products
    
    slug_base = "detail-souvenir-modern" if is_modern else "detail-souvenir-tradisional"
    parent_slug = "souvenir-modern" if is_modern else "souvenir-tradisional"
    parent_name = "Souvenir Modern" if is_modern else "Souvenir Tradisional"
    other_slug = "detail-souvenir-tradisional" if is_modern else "detail-souvenir-modern"
    other_name = "Detail Souvenir Tradisional" if is_modern else "Detail Souvenir Modern"
    
    if is_modern:
        title = "Detail Paket Souvenir Pernikahan Modern &amp; Custom — Spesifikasi Lengkap"
        meta_desc = "Detail spesifikasi lengkap 14 koleksi paket souvenir pernikahan modern: tumbler kopi stainless, lilin aromaterapi, hampers VIP, dispenser sabun &amp; plakat akrilik custom nama via WhatsApp."
        keywords = "detail souvenir pernikahan modern, souvenir pernikahan tumbler, souvenir pernikahan lilin aromaterapi, souvenir pernikahan VIP hardbox, souvenir pernikahan malang, harga souvenir pernikahan modern, souvenir nikah minimalis"
        hero_title = "Detail Spesifikasi Paket Souvenir Pernikahan Modern"
        hero_desc = "Eksplorasi spesifikasi material, opsi personalisasi nama kedua mempelai, pilihan kemasan eksklusif, dan estimasi harga dari 14 koleksi souvenir pernikahan modern pilihan kami. Tanpa popup, informasi lengkap tersaji langsung untuk memudahkan perencanaan pesta pernikahan Anda."
        og_img = "https://souvenirpernikahan.web.id/assets/images/souvenir-tumbler-custom.webp"
        og_alt = "Koleksi Detail Paket Souvenir Pernikahan Modern"
    else:
        title = "Detail Paket Souvenir Pernikahan Tradisional — Kriya Nusantara &amp; Hasil Alam"
        meta_desc = "Detail spesifikasi lengkap 14 koleksi paket souvenir pernikahan tradisional: kipas batik tulis, pouch tenun lurik, besek bambu, madu hutan, sendok kayu jati &amp; lilin gerabah custom WhatsApp."
        keywords = "detail souvenir pernikahan tradisional, souvenir pernikahan kipas batik, souvenir pernikahan pouch tenun, souvenir pernikahan besek bambu, souvenir pernikahan kayu jati, souvenir pernikahan ramah lingkungan malang, souvenir nikah etnik"
        hero_title = "Detail Spesifikasi Paket Souvenir Pernikahan Tradisional"
        hero_desc = "Eksplorasi detail material alami, nilai kriya budaya nusantara, kemasan rustic ramah lingkungan, dan estimasi harga dari 14 koleksi souvenir pernikahan tradisional. Nikmati kehangatan karya pengrajin lokal untuk menyempurnakan hari bahagia pernikahan Anda."
        og_img = "https://souvenirpernikahan.web.id/assets/images/kipas-batik-souvenir.webp"
        og_alt = "Koleksi Detail Paket Souvenir Pernikahan Tradisional"
    
    canonical_url = f"https://souvenirpernikahan.web.id/paket/{slug_base}"
    
    # Build Schema ItemList
    item_list_elements = []
    for idx, p in enumerate(products):
        low_p, high_p = extract_prices(p["price"])
        item_list_elements.append({
            "@type": "ListItem",
            "position": idx + 1,
            "item": {
                "@type": "Product",
                "@id": f"{canonical_url}#{p['slug']}",
                "name": p["title"],
                "description": p["lead"],
                "image": f"https://souvenirpernikahan.web.id{p['image']}",
                "category": "Souvenir Pernikahan",
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
                    "availability": "https://schema.org/InStock",
                    "seller": {
                        "@id": "https://souvenirpernikahan.web.id/#organization"
                    }
                },
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "4.9",
                    "reviewCount": str(75 + idx * 2)
                }
            }
        })
    
    # FAQ elements
    if is_modern:
        faqs = [
            {
                "q": "Berapa lama waktu pengerjaan untuk souvenir pernikahan modern custom nama?",
                "a": "Waktu pengerjaan standar berkisar antara 10 hingga 21 hari kerja tergantung pada jenis produk, jumlah pesanan, dan kerumitan teknik personalisasi (grafir laser monogram, hotprint emas, atau bordir komputer). Untuk pesanan ekspres, tim kami siap mengakomodasi jadwal akad nikah Anda melalui konsultasi WhatsApp."
            },
            {
                "q": "Apakah bisa memesan sampel fisik souvenir pernikahan modern sebelum produksi massal?",
                "a": "Ya, kami melayani pemesanan paket sampel fisik untuk memastikan kualitas bodi tumbler, aroma lilin, ketebalan kaca, serta hasil cetak grafir nama pengantin sesuai ekspektasi sebelum pemesanan jumlah besar."
            },
            {
                "q": "Apakah kemasan hardbox dan pita sudah termasuk dalam harga souvenir pernikahan?",
                "a": "Setiap produk souvenir pernikahan modern kami hadir dengan opsi kemasan lengkap: mulai dari box silinder tebal, hardbox magnetik foil emas, hingga pita satin dan kartu ucapan terima kasih custom."
            },
            {
                "q": "Bagaimana keamanan pengiriman souvenir pernikahan berbahan kaca atau termos stainless ke luar kota?",
                "a": "Kami menerapkan standar pengemasan protektif berlapis (air cushion, bubble wrap ekstra tebal, partisi kardus ganda, dan peti kayu jika diperlukan) serta bekerja sama dengan ekspedisi kargo tepercaya bergaransi kirim utuh ke seluruh Indonesia."
            }
        ]
    else:
        faqs = [
            {
                "q": "Apakah souvenir pernikahan tradisional dibuat langsung oleh perajin lokal nusantara?",
                "a": "Ya, seluruh cinderamata tradisional kami dibuat secara etis dan langsung oleh komunitas perajin lokal: batik tulis dan lurik dari sentra tenun Jawa, anyaman bambu besek dari perajin bambu lokal, serta olahan kayu jati bersertifikasi Perhutani yang ramah lingkungan."
            },
            {
                "q": "Berapa minimal order (MOQ) untuk pemesanan souvenir pernikahan tradisional?",
                "a": "Minimal pemesanan untuk sebagian besar souvenir pernikahan tradisional adalah 100 pcs. Untuk beberapa item khusus seperti sepasang sendok kayu jati atau sabun herbal alami, minimal order mulai dari 100-150 pcs."
            },
            {
                "q": "Apakah bisa kustomisasi tulisan nama mempelai pada kayu jati atau kain tenun?",
                "a": "Tentu saja. Kami menyediakan teknik grafir laser permanen pada permukaan kayu jati, cap wax seal monogram pada gerabah/sabun, bordir halus pada saputangan linen, serta hangtag kaligrafi nama pengantin."
            },
            {
                "q": "Apakah bahan madu hutan dan sabun herbal aman dan memiliki masa simpan lama?",
                "a": "Madu hutan kami merupakan 100% madu murni alami yang tidak memiliki masa kedaluwarsa jika disimpan dalam wadah rapat. Sedangkan sabun herbal alami tahan hingga 18 bulan dengan aroma essential oil yang tetap wangi dan segar."
            }
        ]
    
    faq_schema = [
        {
            "@type": "Question",
            "name": f["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f["a"]
            }
        }
        for f in faqs
    ]
    
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
                "@type": "CollectionPage",
                "@id": f"{canonical_url}#webpage",
                "url": canonical_url,
                "name": title.replace("&amp;", "&"),
                "description": meta_desc.replace("&amp;", "&"),
                "isPartOf": {
                    "@id": "https://souvenirpernikahan.web.id/#website"
                },
                "primaryImageOfPage": {
                    "@type": "ImageObject",
                    "url": og_img
                },
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": [
                        ".gs-page-hero__title",
                        ".gs-page-hero__desc",
                        ".gs-detail-lead"
                    ]
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
                        "name": parent_name,
                        "item": f"https://souvenirpernikahan.web.id/paket/{parent_slug}"
                    },
                    {
                        "@type": "ListItem",
                        "position": 4,
                        "name": f"Detail {parent_name}",
                        "item": canonical_url
                    }
                ]
            },
            {
                "@type": "ItemList",
                "@id": f"{canonical_url}#itemlist",
                "name": f"Katalog Lengkap Detail {parent_name}",
                "description": meta_desc.replace("&amp;", "&"),
                "numberOfItems": len(products),
                "itemListElement": item_list_elements
            },
            {
                "@type": "FAQPage",
                "@id": f"{canonical_url}#faq",
                "mainEntity": faq_schema
            }
        ]
    }
    
    schema_json_str = json.dumps(schema_graph, indent=2, ensure_ascii=False)
    
    # Build Jump Pills HTML
    jump_pills_html = []
    for p in products:
        short_label = p["title"].replace("Souvenir Pernikahan ", "").replace("Paket Hampers ", "")
        if len(short_label) > 28:
            short_label = short_label[:26] + "..."
        jump_pills_html.append(f'<a href="#{p["slug"]}" class="gs-jump-pill" title="Loncat ke {p["title"]}">{short_label}</a>')
    jump_pills_joined = "\n          ".join(jump_pills_html)
    
    # Build Product Detail Articles HTML
    articles_html = []
    for idx, p in enumerate(products):
        order_idx = f"#{idx + 1:02d} dari {len(products):02d}"
        feature_rows = []
        for feat in p["features"]:
            feature_rows.append(f'''                <li class="gs-detail-highlight-row">
                  <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <span>{feat}</span>
                </li>''')
        features_joined = "\n".join(feature_rows)
        
        wa_url = "https://wa.me/6282131087971?text=" + p["wa_text"].replace(" ", "%20").replace("&", "%26")
        
        article = f'''          <!-- ========================================================
               PRODUK {idx + 1}: {p["title"]}
               ======================================================== -->
          <article class="gs-detail-item" id="{p["slug"]}" aria-labelledby="title-{p["slug"]}">
            <div class="gs-detail-visual">
              <div class="gs-detail-main-img-wrap">
                <span class="gs-detail-badge-overlay">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                  </svg>
                  Souvenir Pernikahan Pilihan
                </span>
                <img src="{p["image"]}"
                  alt="{p["alt"]}"
                  width="800" height="600" loading="{'eager' if idx < 2 else 'lazy'}" decoding="async" />
              </div>
            </div>

            <div class="gs-detail-info">
              <div class="gs-detail-eyebrow-row">
                <span class="gs-detail-category-badge">{p["badge"]}</span>
                <span class="gs-detail-order-index">{order_idx}</span>
              </div>

              <h2 class="gs-detail-title" id="title-{p["slug"]}">{p["title"]}</h2>

              <p class="gs-detail-lead">
                {p["lead"]}
              </p>

              <!-- Meta Info: Price, Min Order, Personalisasi -->
              <div class="gs-detail-meta-row">
                <span class="gs-detail-meta-pill" title="Estimasi Kisaran Harga">
                  <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M17.707 9.293a1 1 0 010 1.414l-7 7a1 1 0 01-1.414 0l-7-7A.997.997 0 012 10V5a3 3 0 013-3h5c.266 0 .52.105.707.293l7 7zM5 6a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd"/>
                  </svg>
                  <strong>Estimasi:</strong> {p["price"]}
                </span>
                <span class="gs-detail-meta-pill" title="Minimal Pemesanan">
                  <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
                  </svg>
                  <strong>Min. Order:</strong> {p["min_order"]}
                </span>
                <span class="gs-detail-meta-pill" title="Opsi Personalisasi">
                  <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
                  </svg>
                  <strong>Custom:</strong> {p["custom"]}
                </span>
              </div>

              <!-- Highlights Spesifikasi -->
              <div class="gs-detail-highlights">
                <div class="gs-detail-highlights-head">
                  <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                  </svg>
                  <span>Spesifikasi Produk &amp; Kemasan</span>
                </div>
                <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:0.45rem;">
{features_joined}
                </ul>
              </div>

              <!-- CTA Row -->
              <div class="gs-detail-actions">
                <a href="{wa_url}"
                  class="gs-button gs-button--whatsapp" target="_blank" rel="noopener noreferrer"
                  aria-label="Konsultasi {p["title"]} via WhatsApp">
                  <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" style="width:18px;height:18px;">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                  </svg>
                  Pesan via WhatsApp
                </a>
                <a href="/paket/{parent_slug}" class="gs-button gs-button--outline" title="Kembali ke ringkasan katalog">
                  Kembali ke Ringkasan Paket
                </a>
              </div>
            </div>
          </article>'''
        articles_html.append(article)
    
    articles_joined = "\n\n".join(articles_html)
    
    # Build FAQ HTML
    faq_cards_html = []
    for f in faqs:
        faq_cards_html.append(f'''        <div class="gs-faq-card">
          <h3 class="gs-faq-card__q">{f["q"]}</h3>
          <p class="gs-faq-card__a">{f["a"]}</p>
        </div>''')
    faq_cards_joined = "\n".join(faq_cards_html)
    
    html = f'''<!DOCTYPE html>
<html lang="id">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />

  <!-- Preload Critical CSS -->
  <link rel="preload" href="/assets/css/style.min.css?v=8" as="style" />
  <link rel="preload" href="/assets/css/detail-paket.css?v=1" as="style" />

  <title>{title}</title>
  <meta name="description" content="{meta_desc}" />
  <meta name="keywords" content="{keywords}" />
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
  <link rel="alternate" hreflang="id-ID" href="{canonical_url}" />
  <link rel="alternate" hreflang="x-default" href="{canonical_url}" />

  <!-- GEO & Local Engine Optimization (GEO) -->
  <meta name="geo.region" content="ID-JI" />
  <meta name="geo.placename" content="Kota Malang, Jawa Timur, Indonesia" />
  <meta name="geo.position" content="-7.9839;112.6214" />
  <meta name="ICBM" content="-7.9839, 112.6214" />
  <meta name="geo.country" content="ID" />

  <!-- Open Graph / Facebook / WhatsApp -->
  <meta property="og:site_name" content="Souvenir Pernikahan" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="id_ID" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{meta_desc}" />
  <meta property="og:image" content="{og_img}" />
  <meta property="og:image:secure_url" content="{og_img}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="675" />
  <meta property="og:image:alt" content="{og_alt}" />
  <meta property="og:image:type" content="image/webp" />

  <!-- Twitter / X Cards -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:url" content="{canonical_url}" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{meta_desc}" />
  <meta name="twitter:image" content="{og_img}" />
  <meta name="twitter:image:alt" content="{og_alt}" />

  <!-- Fonts (Non-blocking) -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" as="style"
    href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" />
  <link rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap"
    media="print" onload="this.media='all'" />
  <noscript>
    <link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" />
  </noscript>

  <!-- CSS -->
  <link rel="stylesheet" href="/assets/css/style.min.css?v=8" />
  <link rel="stylesheet" href="/assets/css/detail-paket.css?v=1" />

  <!-- Schema JSON-LD (CollectionPage, ItemList, Product, Breadcrumb & FAQPage) -->
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
            <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20tertarik%20dengan%20detail%20koleksi%20souvenir."
              class="gs-button gs-button--whatsapp gs-button--sm" target="_blank" rel="noopener noreferrer"
              aria-label="Konsultasi melalui WhatsApp">
              <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path
                  d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
              </svg>Konsultasi</a>
          </div>
          <button class="gs-navbar__hamburger" id="gs-hamburger" aria-label="Buka menu navigasi" aria-expanded="false"
            aria-controls="gs-mobile-menu"><span class="gs-navbar__hamburger-line"></span><span
              class="gs-navbar__hamburger-line"></span><span class="gs-navbar__hamburger-line"></span></button>
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
            <a href="/paket/souvenir-tradisional" class="gs-navbar__mobile-link" role="menuitem">Souvenir Tradisional</a>
            <a href="/paket/souvenir-modern" class="gs-navbar__mobile-link" role="menuitem">Souvenir Modern</a>
          </div>
          <a href="/portofolio" class="gs-navbar__mobile-link" role="menuitem">Portofolio</a>
          <a href="/blog" class="gs-navbar__mobile-link" role="menuitem">Blog</a>
          <div class="gs-navbar__mobile-cta"><a
              href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi."
              class="gs-button gs-button--whatsapp" target="_blank" rel="noopener noreferrer"
              style="width:100%;justify-content:center;"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"
                style="width:18px;height:18px;">
                <path
                  d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
              </svg>Konsultasi WhatsApp</a></div>
        </div>
      </div>
    </nav>
  </header>

  <main id="main-content">

    <!-- PAGE HERO -->
    <section class="gs-page-hero gs-page-hero--portofolio" aria-labelledby="gs-detail-hero-title">
      <div class="gs-container">
        <nav aria-label="Breadcrumb">
          <ol class="gs-breadcrumb">
            <li><a href="/" class="gs-breadcrumb__item">Beranda</a></li>
            <li><a href="/paket" class="gs-breadcrumb__item">Paket</a></li>
            <li><a href="/paket/{parent_slug}" class="gs-breadcrumb__item">{parent_name}</a></li>
            <li class="gs-breadcrumb__item gs-breadcrumb__item--active" aria-current="page">Detail {parent_name}</li>
          </ol>
        </nav>
        <h1 class="gs-page-hero__title" id="gs-detail-hero-title">{hero_title}</h1>
        <p class="gs-page-hero__desc">{hero_desc}</p>
      </div>
    </section>

    <!-- QUICK JUMP NAVIGATION BAR -->
    <section class="gs-jump-nav" aria-label="Navigasi cepat produk souvenir">
      <div class="gs-container">
        <div class="gs-jump-nav__inner">
          <span style="font-size:0.78rem;font-weight:700;color:var(--gs-green-950);text-transform:uppercase;letter-spacing:0.06em;margin-right:0.35rem;white-space:nowrap;">Pilih Produk:</span>
          {jump_pills_joined}
        </div>
      </div>
    </section>

    <!-- FEED DETAIL PRODUK SOUVENIR PERNIKAHAN -->
    <section class="gs-section gs-detail-feed" aria-label="Daftar spesifikasi lengkap produk souvenir pernikahan">
      <div class="gs-container">
        <div class="gs-detail-container">
{articles_joined}
        </div>
      </div>
    </section>

    <!-- AEO / FAQ SECTION -->
    <section class="gs-section gs-detail-faq" aria-labelledby="faq-title">
      <div class="gs-container">
        <div style="text-align:center;max-width:720px;margin:0 auto 1.5rem;">
          <span class="gs-section-tag">Tanya Jawab Seputar Pemesanan</span>
          <h2 class="gs-section-title" id="faq-title">Pertanyaan Umum Souvenir Pernikahan</h2>
          <p class="gs-section-desc">Informasi praktis terkait waktu pengerjaan, pemesanan sampel, keamanan ekspedisi, dan opsi kustomisasi nama mempelai.</p>
        </div>
        <div class="gs-faq-grid">
{faq_cards_joined}
        </div>
      </div>
    </section>

    <!-- CROSS-LINK BANNER SECTION -->
    <section class="gs-section" style="background:#ffffff;border-top:1px solid var(--gs-border);">
      <div class="gs-container" style="text-align:center;max-width:800px;margin:0 auto;">
        <span class="gs-section-tag">Koleksi Lainnya</span>
        <h2 class="gs-section-title" style="margin-bottom:1rem;">Tertarik dengan Alternatif {other_name}?</h2>
        <p class="gs-section-desc" style="margin-bottom:2rem;">
          Kami juga menghadirkan koleksi lengkap {other_name.lower()} dengan karakteristik bahan premium, kemasan estetik, dan opsi personalisasi nama pengantin.
        </p>
        <div style="display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;">
          <a href="/paket/{other_slug}" class="gs-button gs-button--primary">
            Lihat {other_name}
          </a>
          <a href="/paket" class="gs-button gs-button--outline">
            Katalog Semua Paket
          </a>
        </div>
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
            Penyedia souvenir pernikahan elegan, cinderamata custom berkesan, dan kemasan berkelas di Malang untuk pengiriman ke seluruh Indonesia. Dibuat dengan perhatian penuh terhadap mutu dan detail.
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
            <li><a href="/paket/detail-souvenir-tradisional" class="gs-footer__link">Detail Tradisional</a></li>
            <li><a href="/paket/detail-souvenir-modern" class="gs-footer__link">Detail Modern</a></li>
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
    <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi."
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
    
    out_path = os.path.join("paket", f"{slug_base}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {out_path} successfully ({len(html)} chars).")

generate_detail_page("modern")
generate_detail_page("tradisional")
