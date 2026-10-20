# PRD — Website Green’s Souvenir
**Versi:** 1.0  
**Tanggal:** 20 Oktober 2026  
**Status:** Draft untuk implementasi lokal  
**Platform:** HTML + Bootstrap + CSS murni (tanpa framework CSS tambahan); JavaScript vanilla seperlunya

## 1. Ringkasan Produk
Website katalog untuk **Green’s Souvenir**, dengan tema visual hijau muda yang elegan dan fokus pada souvenir pernikahan. Website membantu calon pelanggan menemukan inspirasi, membandingkan paket, melihat portofolio, membaca artikel panduan, lalu berkonsultasi melalui WhatsApp. Website juga dapat melayani kebutuhan souvenir perusahaan/organisasi sebagai segmen penting kedua.

Website pada tahap awal dijalankan di **localhost**, tanpa biaya hosting/domain dan tanpa checkout atau pembayaran online. Pemesanan dilakukan melalui katalog dan konsultasi WhatsApp.

## 2. Latar Belakang dan Masalah
Calon pelanggan sering perlu melihat contoh produk, memahami isi paket, mendapatkan inspirasi personalisasi, dan bertanya tentang jumlah, waktu pengerjaan, serta anggaran sebelum memesan. Website harus mengurangi kebingungan tersebut dan mengarahkan pengunjung ke konsultasi yang jelas.

## 3. Tujuan
- Menampilkan paket souvenir pernikahan secara rapi, mudah dijelajahi, dan mobile-friendly.
- Membantu pengunjung memahami pilihan paket, personalisasi, proses pemesanan, dan hal yang perlu disiapkan.
- Mengubah pengunjung menjadi prospek konsultasi melalui WhatsApp.
- Menampilkan portofolio dan artikel yang membangun kepercayaan.
- Menyiapkan fondasi SEO teknis, SEO lokal, AEO, GEO (Generative Engine Optimization), structured data, Open Graph, dan aksesibilitas.
- Menyediakan struktur yang mudah dikembangkan ketika website dipindahkan dari localhost ke hosting.

## 4. Target Pengguna
### Primer
- Calon pengantin, keluarga, dan panitia yang mencari souvenir pernikahan.
- Pengunjung yang membutuhkan inspirasi desain, pilihan paket, serta penyesuaian jumlah dan anggaran.

### Sekunder
- Perusahaan, kampus, komunitas, organisasi, dan instansi yang membutuhkan souvenir acara atau paket custom.

### Kebutuhan pengguna
- Melihat foto produk asli dan contoh hasil.
- Mengetahui isi paket, opsi personalisasi, minimum order jika berlaku, estimasi proses, serta faktor yang memengaruhi harga.
- Bertanya tanpa harus membuat akun.
- Mengakses website dengan nyaman dari ponsel.

## 5. Ruang Lingkup MVP
### Termasuk
- Navbar: **Beranda**, **Tentang**, **Paket** (dropdown), **Portofolio**, **Blog**.
- Beranda dengan hero, kategori paket, keunggulan, langkah pemesanan, portofolio pilihan, testimoni terverifikasi bila tersedia, FAQ, dan CTA WhatsApp.
- Halaman Tentang.
- Halaman Paket dan halaman detail/kategori paket melalui dropdown.
- Halaman Portofolio.
- Blog: daftar artikel dan halaman artikel.
- Tombol WhatsApp dengan nomor tujuan **6285810025485**.
- Pencarian/filter sederhana untuk katalog jika jumlah paket sudah cukup.
- SEO on-page dan teknis dasar; metadata sosial; schema JSON-LD sesuai konten nyata.
- Responsive layout, aksesibilitas dasar, halaman 404 sederhana, dan halaman kebijakan privasi bila formulir/analitik digunakan.
- Semua CSS ditulis sendiri dan/atau Bootstrap; tidak memakai Tailwind, Bulma, atau framework CSS lain.
- JavaScript vanilla hanya untuk dropdown, navbar mobile, filter, FAQ accordion jika tidak memakai komponen Bootstrap, dan interaksi kecil.

### Tidak termasuk pada MVP
- Checkout, keranjang belanja, payment gateway, akun pengguna, sistem stok real-time.
- Panel admin/CMS khusus, CRM, otomatisasi WhatsApp, atau integrasi API berbayar.
- Klaim harga, rating, testimoni, stok, waktu produksi, dan minimum order yang belum dikonfirmasi.
- Menjanjikan peringkat Google, jawaban AI, atau rich result.

## 6. Arsitektur Informasi dan Navigasi
1. **Beranda** — ringkasan brand dan CTA utama.
2. **Tentang** — cerita, nilai, layanan, alur kerja, dan komitmen yang dapat dibuktikan.
3. **Paket** (dropdown):
   - Semua Paket
   - Souvenir Pernikahan
   - Paket Hemat / Paket Praktis (nama dan isi perlu dikonfirmasi)
   - Souvenir Custom
   - Souvenir Perusahaan & Acara
   - FAQ Paket (opsional, bisa menjadi bagian di halaman paket)
4. **Portofolio** — proyek dan contoh hasil yang benar-benar dimiliki/diizinkan.
5. **Blog** — artikel inspirasi dan panduan.

Nama kategori di dropdown adalah struktur awal; sesuaikan dengan produk yang benar-benar tersedia. Jangan menampilkan kategori kosong.

## 7. Persyaratan Konten per Halaman

### 7.1 Beranda
- SEO title dan meta description unik.
- Hero: judul yang menjelaskan souvenir pernikahan/custom, deskripsi singkat, CTA “Lihat Paket” dan “Konsultasi WhatsApp”.
- Foto utama yang autentik, alt text deskriptif, dan ukuran file dioptimalkan.
- Kategori/paket unggulan dengan tautan ke detail.
- Keunggulan yang dapat dibuktikan: opsi personalisasi, pilihan produk, bantuan konsultasi, atau layanan lain yang memang tersedia.
- “Cara Memesan” dalam 3–5 langkah.
- Portofolio pilihan.
- Testimoni hanya dengan izin dan sumber nyata; jangan membuat testimoni fiktif.
- FAQ singkat yang menjawab pertanyaan umum.
- CTA akhir dengan pesan WhatsApp yang relevan.
- Tautan internal ke Tentang, Paket, Portofolio, dan Blog.

### 7.2 Tentang
- Siapa Green’s Souvenir dan siapa yang dilayani.
- Cerita/tujuan brand (hanya fakta yang disetujui).
- Nilai layanan dan pendekatan personalisasi.
- Jenis kebutuhan yang dilayani: pernikahan serta perusahaan/organisasi.
- Foto tim/proses jika tersedia dan disetujui.
- Kontak dan CTA WhatsApp.
- Hindari klaim “terbaik”, “nomor satu”, atau pengalaman bertahun-tahun jika tidak dapat dibuktikan.

### 7.3 Paket
Setiap kartu paket idealnya menampilkan:
- Nama paket dan ringkasan kegunaan.
- Foto asli/representatif yang diberi keterangan bila hanya mockup.
- Isi paket secara rinci.
- Pilihan warna/bahan/personalisasi yang benar-benar tersedia.
- Informasi kuantitas atau minimum order bila sudah ditetapkan.
- Harga hanya jika telah dikonfirmasi; bila belum, tulis “Hubungi kami untuk penawaran” dan jelaskan faktor penentu harga.
- Estimasi pengerjaan hanya setelah dikonfirmasi dan dengan catatan dapat berubah.
- Tombol detail dan CTA WhatsApp dengan nama paket pada pesan awal.
- Keterangan bahwa ketersediaan bahan dan desain perlu dikonfirmasi sebelum pemesanan.

### 7.4 Detail Paket
- Nama paket, galeri foto, isi paket, opsi custom, spesifikasi produk, jumlah, ketentuan pemesanan, waktu produksi yang terverifikasi, FAQ paket, paket terkait, dan CTA WhatsApp.
- Jangan mengarang harga, jumlah minimum, stok, atau jaminan waktu produksi.

### 7.5 Portofolio
- Foto proyek/produk yang benar-benar dibuat atau yang penggunaannya diizinkan.
- Nama proyek/kategori, jenis acara, item yang dibuat, dan ringkasan solusi.
- Tampilkan nama klien hanya dengan izin; jika tidak, gunakan deskripsi umum tanpa membuka identitas.
- Filter kategori opsional.
- Alt text menjelaskan isi foto, bukan menumpuk kata kunci.
- Jangan menyebut gambar mockup sebagai hasil proyek nyata.

### 7.6 Blog
- Daftar artikel dengan judul, ringkasan, kategori, tanggal publikasi dan pembaruan yang jujur, penulis/editor jika ada, dan gambar.
- Halaman artikel dengan satu H1, heading berurutan, daftar isi untuk artikel panjang, tautan internal, sumber rujukan jika klaim membutuhkan dukungan, penulis/reviewer yang nyata, tanggal terbit dan update yang nyata, CTA relevan, serta artikel terkait.
- Konten orisinal dan bermanfaat, bukan artikel tipis yang dibuat hanya untuk mengejar keyword.
- Ide artikel: panduan memilih souvenir pernikahan, cara menghitung jumlah souvenir, ide kemasan, personalisasi nama/tanggal, checklist pemesanan, perbandingan bahan, serta panduan souvenir acara perusahaan.

### 7.7 FAQ
Jawab secara langsung dan konsisten:
- Bagaimana cara memesan?
- Apakah desain/nama/tanggal dapat dicustom?
- Berapa harga paket?
- Apakah ada minimum order?
- Berapa lama proses produksi?
- Apakah bisa melihat sampel?
- Bagaimana pengiriman dan biaya kirim?
- Apakah bisa pesan untuk acara perusahaan?
Isi jawaban hanya setelah kebijakan bisnis dikonfirmasi. FAQ schema tidak menjamin FAQ rich results dan penggunaannya harus mengikuti kebijakan mesin pencari terkini.

### 7.8 Kontak dan WhatsApp
- Nomor tujuan: `6285810025485`.
- Gunakan link berbentuk `https://wa.me/6285810025485?text=...` dengan teks URL-encoded.
- Pesan default, misalnya: “Halo Green’s Souvenir, saya ingin konsultasi souvenir pernikahan. Boleh minta informasi paket yang tersedia?”
- Untuk CTA paket, sertakan nama paket dalam pesan.
- Jangan menampilkan tombol yang seolah-olah mengirim pesanan otomatis; WhatsApp dibuka dan pengguna menekan kirim sendiri.
- Informasikan jam layanan hanya jika sudah ditetapkan.
- Nomor harus ditulis dalam format internasional tanpa tanda `+`, spasi, atau tanda hubung pada URL.

## 8. Desain dan UX
- Nuansa hijau muda, putih hangat, dan hijau tua untuk teks/kontras.
- Visual elegan, romantis, modern, tidak terlalu ramai atau terlalu dekoratif.
- Foto produk autentik menjadi fokus.
- Navbar desktop dengan dropdown Paket; mobile menggunakan menu yang mudah dioperasikan.
- CTA WhatsApp jelas tetapi tidak menutupi konten.
- Card paket konsisten; tombol dan tautan punya state hover/focus.
- Gunakan layout responsive dan ukuran teks nyaman dibaca.
- Hormati `prefers-reduced-motion`; animasi harus ringan dan tidak wajib untuk memahami halaman.
- Hindari carousel otomatis yang sulit dikontrol.
- Ikon dekoratif tidak menggantikan label teks.

## 9. Persyaratan Teknis
- HTML semantik: `header`, `nav`, `main`, `section`, `article`, `footer`.
- Bootstrap versi stabil yang dipilih saat implementasi; catat versi dan gunakan dokumentasi resminya. Jika memakai CDN, gunakan URL versi tetap dan integrity/crossorigin bila tersedia; untuk penggunaan offline/local, simpan aset lokal.
- CSS kustom ditulis di file terpisah, misalnya `assets/css/style.css`, dan diberi prefix kelas bila diperlukan agar tidak bertabrakan.
- JavaScript vanilla di `assets/js/main.js`; hindari script yang tidak diperlukan.
- Semua halaman punya satu H1 utama yang jelas.
- Link internal relatif dan struktur URL konsisten.
- Gambar responsif (`width`/`height`, `srcset` bila ada beberapa ukuran, `loading="lazy"` untuk gambar di bawah fold; jangan lazy-load gambar hero utama).
- Jangan memuat font atau library eksternal berlebihan.
- Hindari konten utama yang hanya muncul setelah interaksi JavaScript.
- Tautan eksternal yang membuka tab baru harus memakai `rel="noopener noreferrer"`.

## 10. SEO, AEO, GEO, dan Social Metadata
### SEO teknis
- Satu title unik per halaman, meta description yang relevan, canonical absolut ketika domain produksi sudah tersedia, robots meta sesuai status indeksasi, sitemap XML, `robots.txt`, URL bersih, redirect 301 saat URL berubah, halaman 404 yang benar, dan tidak ada halaman duplikat yang bisa diindeks.
- Di localhost: gunakan `noindex`/blokir crawling selama pengembangan; jangan menerbitkan canonical atau sitemap dengan domain contoh. Hapus pengaturan noindex dan konfigurasi domain produksi sebelum peluncuran.
- Search Console dan Bing Webmaster Tools setelah situs online.
- Pantau Core Web Vitals dan aksesibilitas.
- Jangan menambahkan meta `keywords`; tidak menjadi sinyal ranking yang berguna di Google.
- Jangan mengandalkan `meta name="author"` sebagai sinyal ranking.

### SEO on-page
- Riset intent dan keyword sebelum membuat halaman.
- Title, H1, heading, teks, internal link, breadcrumb, dan alt gambar alami.
- Hindari keyword stuffing dan halaman doorway untuk banyak kota.
- Setiap halaman harus punya tujuan dan konten unik.
- Optimasi gambar dan teks tautan yang deskriptif.

### AEO dan GEO
- Jawab pertanyaan utama sejak awal halaman dengan bahasa lugas.
- Gunakan definisi singkat, langkah bernomor, tabel perbandingan jika berguna, dan FAQ yang benar-benar membantu.
- Tampilkan identitas brand, layanan, area layanan yang benar, detail produk, kontak, penulis dan sumber bila relevan.
- Buat informasi mudah dirayapi dan konsisten di halaman, profil bisnis, dan data terstruktur.
- Utamakan keaslian, pengalaman nyata, keahlian, transparansi, dan sumber tepercaya.
- `llms.txt` boleh diuji sebagai eksperimen opsional, bukan persyaratan SEO atau jaminan sitasi AI.
- Tidak ada schema, file, atau teknik yang menjamin website dikutip mesin jawaban/AI.

### Structured data (JSON-LD)
Gunakan JSON-LD valid, sesuai konten yang terlihat dan benar-benar ada:
- `Organization` atau `LocalBusiness` sesuai sifat bisnis dan informasi nyata.
- `WebSite` untuk identitas website; jangan menjanjikan sitelinks search box.
- `WebPage` pada halaman yang sesuai.
- `BreadcrumbList` pada halaman dalam.
- `Product` hanya jika halaman memang menawarkan produk tertentu dengan detail faktual; `Offer` dan `price` hanya jika harga/penawaran benar-benar tersedia. Jangan memakai harga palsu atau `AggregateRating` palsu.
- `Article` atau `BlogPosting` untuk artikel blog dengan judul, gambar, tanggal, penulis, dan publisher yang benar.
- `ImageObject` jika dibutuhkan dan informasinya valid.
- `FAQPage` hanya jika sesuai panduan mesin pencari dan konten FAQ terlihat; jangan berharap FAQ rich result di Google untuk situs komersial biasa.
- `LocalBusiness` hanya jika ada bisnis lokal nyata dan alamat/area/telepon dapat diverifikasi. Jangan mengarang alamat, koordinat, jam buka, atau rating.
- Validasi dengan Schema Markup Validator dan Google Rich Results Test; schema yang valid tidak menjamin tampilan rich result.

### Open Graph dan social sharing
- `og:title`, `og:description`, `og:type`, `og:url`, `og:image`, `og:site_name`, dan `og:locale=id_ID`.
- `twitter:card` (`summary_large_image`), `twitter:title`, `twitter:description`, `twitter:image`.
- Gunakan URL absolut untuk canonical dan gambar setelah domain produksi tersedia.
- Gambar sosial dengan rasio sekitar 1.91:1 (contoh 1200×630), teks aman dari tepi, dan ukuran file wajar.
- Metadata sosial tidak menggantikan SEO dan tidak menjamin preview yang sama di semua platform.
- Jangan membuat metadata produksi memakai URL localhost.

## 11. Aksesibilitas dan Kualitas
- Kontras teks memadai; jangan gunakan hijau muda sebagai teks kecil di atas putih.
- Dropdown dapat digunakan dengan keyboard; tombol mobile memiliki `aria-expanded` dan `aria-controls`.
- Gambar informatif punya alt yang bermakna; gambar dekoratif `alt=""`.
- Form (jika kelak ditambahkan) memiliki label, validasi jelas, dan pesan error yang dapat dibaca pembaca layar.
- Fokus keyboard terlihat.
- Uji ukuran ponsel, tablet, desktop, zoom 200%, dan navigasi keyboard.
- Periksa broken links, gambar, console errors, dan halaman 404.

## 12. Privasi dan Keamanan
- MVP tidak membutuhkan akun atau menyimpan data pribadi di website.
- Jangan mengumpulkan data formulir sebelum ada kebutuhan dan kebijakan privasi.
- Jika analytics, pixel, form, atau cookie non-esensial dipakai, tinjau kewajiban persetujuan dan pemberitahuan privasi yang berlaku.
- Jangan memasukkan data pelanggan sensitif ke URL atau parameter WhatsApp.
- Hindari menaruh API key atau rahasia di source code frontend.

## 13. Metrik Keberhasilan
- Klik CTA WhatsApp per halaman.
- Klik dari kartu paket ke detail/konsultasi.
- Pengunjung organik dan impresi/query di Search Console setelah live.
- Artikel yang mendapatkan kunjungan organik dan klik internal.
- Kecepatan, stabilitas visual, aksesibilitas, dan error teknis.
- Tingkat konversi konsultasi hanya dihitung jika pencatatan dilakukan secara transparan dan sesuai privasi.

## 14. Acceptance Criteria
- [ ] Navbar memuat Beranda, Tentang, Paket dropdown, Portofolio, Blog.
- [ ] Dropdown berfungsi dengan mouse, sentuhan, dan keyboard.
- [ ] Semua CTA WhatsApp mengarah ke `https://wa.me/6285810025485` dengan teks yang relevan.
- [ ] Tidak ada checkout atau pembayaran online pada MVP.
- [ ] Tidak ada harga, testimoni, alamat, jam layanan, rating, minimum order, atau klaim yang dibuat-buat.
- [ ] Layout bekerja pada mobile, tablet, dan desktop.
- [ ] Setiap halaman memiliki title, description, H1, internal links, dan metadata sosial yang sesuai.
- [ ] JSON-LD cocok dengan konten yang terlihat dan lolos validasi sintaks.
- [ ] Halaman localhost tidak terindeks; konfigurasi produksi disiapkan terpisah.
- [ ] Tidak ada tautan rusak, gambar rusak, atau error JavaScript yang diketahui.
- [ ] Gambar memiliki alt yang sesuai dan ukuran file dioptimalkan.

## 15. Risiko dan Mitigasi
- **Konten bisnis belum lengkap:** gunakan label “perlu dikonfirmasi” dan jangan publikasikan klaim yang belum valid.
- **Harga belum ditentukan:** gunakan konsultasi penawaran; jangan menampilkan harga contoh seolah-olah nyata.
- **SEO berubah:** cek dokumentasi resmi mesin pencari sebelum launch dan audit berkala.
- **Schema disalahgunakan:** pasang hanya tipe yang relevan dan sesuai konten.
- **Localhost terindeks/URL salah saat launch:** pisahkan konfigurasi development dan production.
- **Aset visual tidak berizin:** pastikan izin penggunaan foto, logo, dan testimoni.

## 16. Keputusan yang Masih Perlu Dikonfirmasi
- Apakah brand publik tetap **Green’s Souvenir** dan apakah fokus utama halaman depan adalah souvenir pernikahan, sementara perusahaan/organisasi menjadi kategori kedua.
- Daftar paket dan isi setiap paket yang benar-benar tersedia.
- Harga, minimum order, estimasi produksi, opsi bahan/warna/custom, kebijakan sampel, pengiriman, dan area layanan.
- Alamat bisnis dan jam layanan (jika ingin ditampilkan).
- Foto produk, portofolio, testimoni, identitas penulis, dan profil bisnis.
- Versi Bootstrap yang dipatok pada saat implementasi dan apakah aset perlu sepenuhnya offline.
- Domain produksi, nama domain canonical, email kontak, serta akun Search Console/Bing Webmaster Tools.
- Kebijakan privasi dan alat analytics jika digunakan.

## 17. Catatan Versi 2026–2027
SEO, AEO, dan GEO bukan paket metadata yang sekali pasang lalu selesai. Rekomendasi implementasi harus diperiksa terhadap dokumentasi resmi yang berlaku pada saat peluncuran. Prioritaskan konten bermanfaat, aksesibilitas, crawlability, performa, reputasi, dan informasi bisnis yang konsisten; hindari klaim bahwa markup tertentu menjamin ranking atau jawaban AI.
