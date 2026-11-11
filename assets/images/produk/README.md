# Direktori Foto Produk Souvenir Pernikahan

Direktori ini memisahkan foto-foto produk ke dalam dua kategori utama:

1. **`tradisional/`** (Souvenir Pernikahan Tradisional / Etnik / Nusantara)
   - Contoh produk: Kipas lipat batik, pouch tenun lurik, besek anyaman bambu, sendok kayu jati, madu hutan jar heksagonal, sabun herbal batang, lilin gerabah terakota, coaster tatakan kayu jati, mug keramik rustic, pembatas buku kuningan, saputangan linen bordir, wax sachet botanical, tanaman sukulen pot goni, cermin saku logam ukir.
   - **Simpan foto produk tradisional baru di folder ini:** `assets/images/produk/tradisional/` (atau `images/produk/tradisional/`)

2. **`modern/`** (Souvenir Pernikahan Modern / Eksklusif / Kontemporer)
   - Contoh produk: Hampers VIP gift set box, tumbler kopi stainless sage green, tumbler termos ivory rose gold, glass tumbler borosilikat tutup bambu, plakat akrilik dudukan kayu, teh herbal tabung kaca saringan emas, kaleng teh artisan gold, botol dispenser sabun pump gold, lilin aromaterapi frosted jar, botol parfum kaca amber, minyak esensial pipet kaca box beludru, silk scrunchie sutra, pouch serut beludru velvet, eco tote bag kanvas.
   - **Simpan foto produk modern baru di folder ini:** `assets/images/produk/modern/` (atau `images/produk/modern/`)

Format gambar yang direkomendasikan: `.webp` (rasio 4:3 atau 1:1, lebar minimum 600px - 1200px) untuk kecepatan loading optimal.

## Panduan Pengelolaan & Pemisahan Foto:
1. **Pemisahan Total dengan Foto Artikel:**
   - Seluruh halaman produk (`produk/*.html`), paket katalog (`paket/*.html`, `paket.html`), dan komponen kartu produk di beranda **hanya** boleh memuat foto dari folder `assets/images/produk/`.
   - Jangan pernah menghubungkan file produk ke folder `assets/images/artikel/`.
2. **Kemandirian Berkas (Decoupled Assets):**
   - Jika suatu produk dan artikel menggunakan basis visual yang serupa, berkas disimpan terpisah secara independen di folder masing-masing.
   - Perubahan, penggantian, atau optimasi foto produk tidak akan berdampak pada foto artikel, dan sebaliknya.
