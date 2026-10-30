---
title: "Audit SEO dan Rencana Perbaikan Souvenir Pernikahan"
document_type: seo_audit_and_implementation_plan
version: "1.2"
website_stack: "Static landing page — HTML5, CSS3, Bootstrap, JavaScript (tanpa Astro)"
audit_date: "2026-10-30"
language: id-ID
website: "https://souvenirpernikahan.web.id/"
primary_keyword: "souvenir pernikahan"
primary_search_intent: "commercial, transactional"
competitor_url: "https://dekayu.id/product-category/hampers-gift-set/souvenir/souvenir-wedding/"
status: "actionable; sebagian temuan memerlukan verifikasi tambahan"
---

# Audit SEO dan Rencana Perbaikan — Souvenirpernikahan.web.id

## 1. Tujuan dan ruang lingkup

- **Website:** https://souvenirpernikahan.web.id/
- **Fokus bisnis dan entitas utama:** Souvenir Pernikahan.
- **Keyword utama:** `souvenir pernikahan`.
- **Keyword pendukung:** `souvenir wedding`, `souvenir pernikahan custom`, `souvenir pernikahan unik`, `souvenir pernikahan modern`, `souvenir pernikahan tradisional`.
- **Intent utama:** pengguna ingin menemukan, membandingkan, dan memesan souvenir pernikahan.
- **Kompetitor pembanding:** https://dekayu.id/product-category/hampers-gift-set/souvenir/souvenir-wedding/
- **Tujuan bisnis:** meningkatkan visibilitas organik dan permintaan penawaran/pemesanan.
- **Prinsip:** seluruh bagian utama homepage harus membahas souvenir pernikahan. Corporate gift, seminar kit, dan merchandise perusahaan bukan fokus homepage.

## 2. Ringkasan eksekutif

**Diagnosis inti:** Homepage sudah diindeks Google. Tidak ada bukti dari screenshot Google Search Console bahwa homepage diblokir, terkena `noindex`, gagal di-crawl, atau menggunakan canonical yang salah. Masalah yang perlu ditangani adalah kesesuaian intent komersial, fokus tema homepage, informasi katalog, konsistensi identitas, struktur internal link, dan evaluasi ranking berdasarkan data Google Search Console.

**Batas kepastian:** Belum tersedia data kinerja kueri `souvenir pernikahan` di Google Search Console, sehingga posisi aktual, impressions, clicks, CTR, dan penyebab dominan ranking rendah **belum dapat dipastikan**. Kinerja atau otoritas backlink relatif terhadap Dekayu juga **belum diukur**.

## 3. Bukti terverifikasi dari Google Search Console

Sumber: screenshot URL Inspection homepage yang diberikan pemilik website pada 30 Oktober 2026.

| Indikator | Hasil | Interpretasi |
|---|---|---|
| URL yang diperiksa | `https://souvenirpernikahan.web.id/` | Homepage produksi |
| Status | `URL ada di Google` | Homepage terindeks |
| Pengindeksan halaman | `Halaman diindeks` | Sudah masuk indeks |
| Crawl terakhir | `30 Okt 2026, 09.25.35` | Googlebot baru-baru ini mengambil halaman |
| Crawler | `Smartphone Googlebot` | Crawl mobile |
| Crawl diizinkan | `Ya` | Bukan masalah blokir crawling pada URL ini |
| Pengambilan halaman | `Berhasil` | Fetch oleh Googlebot berhasil |
| Pengindeksan diizinkan | `Ya` | Bukan `noindex` pada hasil inspeksi |
| Canonical yang dinyatakan pengguna | `https://souvenirpernikahan.web.id/` | Sesuai domain utama |
| Canonical pilihan Google | `URL yang diperiksa` | Tidak terdeteksi konflik canonical pada homepage |
| Sitemap perujuk | `Tidak ada peta situs perujuk yang terdeteksi` | Perlu verifikasi keberadaan, isi, dan submission sitemap; bukan bukti sitemap tidak ada |
| HTTPS | `Halaman ditayangkan melalui HTTPS` | Status HTTPS baik |
| Halaman perujuk | URL kategori `/paket/souvenir-tradisional` dan domain `best-backlink-provider.com.in` | Satu domain perujuk patut diaudit; belum terbukti sebagai sumber penalti |

**Kesimpulan teknis:** Jangan melakukan migrasi domain, mengganti canonical homepage, atau mengubah DNS hanya karena ranking belum tinggi. Bukti Search Console memperlihatkan Googlebot berhasil mengakses homepage.

## 4. Temuan SEO, prioritas, dan rencana perbaikan

### P1-01 — Homepage belum sepenuhnya fokus pada souvenir pernikahan

- **Status bukti:** temuan dari pemeriksaan halaman pada analisis sebelumnya; verifikasi ulang setelah perubahan deployment.
- **Masalah:** konten unggulan bercampur dengan executive corporate gift, plakat, seminar kit, dan workshop.
- **Risiko:** homepage kurang selaras dengan intent pembeli souvenir pernikahan, dan bagian penting halaman dipakai untuk topik yang tidak relevan.
- **Tindakan:**
  1. Prioritaskan hero, foto, kategori, produk, copywriting, artikel, dan CTA untuk calon pengantin.
  2. Hapus dari area unggulan atau pindahkan konten corporate/seminar ke kategori atau website relevan.
  3. Jangan langsung menghapus URL yang sudah ada; audit trafik dan backlink, kemudian gunakan redirect 301 jika halaman dipindah permanen.
- **Kriteria selesai:** hero, kategori utama, katalog unggulan, artikel rekomendasi, dan CTA homepage seluruhnya relevan dengan souvenir pernikahan.

### P1-02 — Informasi harga dan MOQ tidak memadai

- **Status bukti:** temuan dari pemeriksaan katalog homepage pada analisis sebelumnya.
- **Masalah:** harga ditampilkan sebagai `harga sesuai kuantitas`, tanpa angka pembanding; informasi MOQ belum jelas untuk beberapa produk.
- **Risiko:** calon pembeli sulit membandingkan dan memperkirakan budget.
- **Tindakan:**
  1. Tampilkan `Harga mulai Rp .../pcs` berdasarkan harga yang benar, atau rentang harga berdasarkan jumlah jika tersedia.
  2. Cantumkan MOQ tiap produk, bahan, dimensi, warna, opsi custom, kemasan, estimasi produksi, dan ketentuan ongkir bila tersedia.
  3. Jangan mengarang harga, MOQ, stok, atau estimasi pengerjaan.
- **Kriteria selesai:** setiap produk prioritas memiliki spesifikasi dan informasi pembelian yang dapat diverifikasi.

### P1-03 — Artikel homepage tidak sepenuhnya relevan

- **Status bukti:** temuan dari pemeriksaan homepage sebelumnya.
- **Masalah:** artikel seminar kit/workshop ditampilkan pada situs yang menargetkan souvenir pernikahan.
- **Tindakan:** prioritaskan artikel tentang rekomendasi souvenir, penghitungan budget, souvenir modern/tradisional, jumlah tamu, personalisasi, dan tips memilih.
- **Kriteria selesai:** rekomendasi artikel homepage mengarah ke cluster souvenir pernikahan dan halaman kategori/produk yang relevan.

### P1-04 — Konsistensi identitas dan testimoni

- **Status bukti:** analisis sebelumnya menemukan testimoni yang menyebut `Green's Souvenir`.
- **Masalah:** penyebutan nama merek lain perlu dijelaskan atau diverifikasi.
- **Tindakan:** cocokkan dengan bukti testimoni asli; jika tidak dapat dibuktikan, jangan gunakan. Cantumkan identitas usaha, kontak, dan portofolio nyata secara konsisten. Jangan membuat ulasan atau rating fiktif.
- **Kriteria selesai:** semua klaim, testimoni, dan identitas usaha konsisten serta dapat diverifikasi.

### P1-05 — Performa keyword utama belum terukur

- **Status bukti:** belum ada screenshot/perolehan data Performance GSC untuk exact query.
- **Masalah:** klaim “tidak muncul” belum dapat dipisahkan antara tidak mendapat impresi, posisi rendah, atau hasil personalisasi SERP.
- **Tindakan:**
  1. Buka Search Console > Performa > Hasil penelusuran.
  2. Pilih rentang 3 bulan, query persis `souvenir pernikahan`.
  3. Ekspor klik, tayangan, CTR, posisi rata-rata, perangkat, negara, dan URL pada tab Halaman.
  4. Gunakan periode pembanding sesudah perubahan.
- **Kriteria selesai:** tersedia baseline metrik query dan landing page yang menerima impresi.

### P2-01 — Sitemap perujuk tidak terdeteksi

- **Status bukti:** terverifikasi di screenshot URL Inspection; tidak membuktikan file sitemap tidak ada.
- **Tindakan:** cek sitemap yang benar-benar tersedia (`/sitemap-index.xml` atau `/sitemap.xml`), pastikan berisi URL canonical yang valid, lalu submit di Search Console. Untuk landing page statis, buat atau perbarui `sitemap.xml` secara manual sesuai URL yang benar-benar tersedia di hosting.
- **Kriteria selesai:** sitemap dapat diakses, berhasil diproses di GSC, dan mencakup URL prioritas yang dapat diindeks.

### P2-02 — Arsitektur informasi dan internal linking perlu diperkuat

- **Status bukti:** rekomendasi strategis; audit seluruh URL belum lengkap.
- **Tindakan:** susun alur `homepage -> kategori -> detail produk`, dan tautkan artikel informatif ke kategori/produk terkait. Tambahkan breadcrumb yang konsisten. Jangan membuat beberapa landing page dengan intent yang hampir identik.
- **Kriteria selesai:** seluruh kategori penting mudah ditemukan melalui tautan HTML, bukan hanya pencarian internal atau JavaScript.

### P2-03 — Bukti bisnis dan portofolio wedding perlu diperkuat

- **Status bukti:** rekomendasi berdasarkan intent dan pembandingan halaman; belum ada audit menyeluruh seluruh portofolio.
- **Tindakan:** gunakan foto produk asli, studi kasus pesanan, proses produksi, spesifikasi, dan bukti hasil custom dengan izin yang sesuai. Cantumkan informasi vendor dan cara pesan yang jelas.
- **Kriteria selesai:** tersedia portofolio souvenir pernikahan yang autentik dan terhubung ke kategori produk.

### P2-04 — Tautan dari domain yang perlu diaudit

- **Status bukti:** `best-backlink-provider.com.in` muncul sebagai salah satu halaman perujuk pada URL Inspection.
- **Batasan:** satu tautan mencurigakan **tidak cukup** untuk menyimpulkan penalti, spam terstruktur, atau penyebab ranking turun.
- **Tindakan:** tinjau laporan Links dan Manual Actions di GSC serta profil backlink. Hindari membeli backlink. Pertimbangkan disavow hanya jika ada alasan kuat sesuai pedoman Google, bukan otomatis.
- **Kriteria selesai:** diketahui apakah tautan berkualitas rendah merupakan pola yang signifikan dan perlu ditangani.

### P3-01 — Performa mobile dan Core Web Vitals

- **Status bukti:** audit PageSpeed sebelumnya menunjukkan indikasi penundaan LCP, rantai CSS, dan forced reflow JavaScript; pengukuran aktual perlu diulang.
- **Tindakan:** optimalkan hero image, ukuran/resolusi gambar, muatan CSS kritis, JavaScript yang tidak perlu, dan layout mobile. Jangan lazy-load gambar LCP.
- **Kriteria selesai:** audit ulang Lighthouse dan data Core Web Vitals menunjukkan perbaikan tanpa menghilangkan konten atau fungsi penting.

### P3-02 — Metadata dan structured data

- **Status bukti:** perlu validasi menyeluruh per halaman; belum terbukti salah.
- **Tindakan:** audit title, meta description, H1, canonical, Open Graph, schema `Organization`, `WebSite`, `BreadcrumbList`, `Product` dan `Offer` bila sesuai. Gunakan `Article`/`BlogPosting` untuk artikel. Gunakan review hanya jika ada ulasan asli. `FAQPage` tidak menjamin tampilan rich result.
- **Kriteria selesai:** setiap tipe halaman memiliki metadata unik, canonical konsisten, dan schema valid sesuai isi yang terlihat.

## 5. Analisis kompetitor Dekayu

**URL:** https://dekayu.id/product-category/hampers-gift-set/souvenir/souvenir-wedding/

Pada pemeriksaan sebelumnya, kategori Dekayu menampilkan sekitar 53 produk souvenir wedding, harga/rentang harga, navigasi kategori, pagination, dan tautan detail produk. Halaman detail produk juga memberi informasi paket dan pemesanan. Jumlah ini adalah hasil pemeriksaan pada waktu audit, bukan angka permanen.

| Aspek | Souvenirpernikahan.web.id (homepage, pemeriksaan sebelumnya) | Dekayu (kategori wedding, pemeriksaan sebelumnya) | Implikasi |
|---|---|---|---|
| Fokus halaman | Bercampur dengan item corporate/seminar | Kategori khusus souvenir wedding | Perkuat relevansi halaman utama |
| Produk | Sekitar 6 produk unggulan homepage | Sekitar 53 produk kategori | Tambah ketercakupan produk secara bertahap, prioritaskan kualitas |
| Harga | `harga sesuai kuantitas` | Rentang harga tersedia | Tampilkan harga indikatif dan MOQ |
| Informasi pembelian | CTA konsultasi | Kategori dan detail produk mendukung pembandingan | Buat detail produk lebih informatif |
| Otoritas domain/backlink | Belum diukur | Belum diukur | Jangan membuat klaim peringkat atau otoritas tanpa data |

**Penting:** perbandingan jumlah produk di homepage vs halaman kategori bukan perbandingan halaman yang sepenuhnya setara; gunakan sebagai indikator pengalaman pembeli, bukan bukti tunggal penyebab ranking.

## 6. Arsitektur SEO yang direkomendasikan

```text
/                               -> Keyword utama: souvenir pernikahan
├── [kategori souvenir modern]   -> souvenir pernikahan modern
├── [kategori souvenir tradisional] -> souvenir pernikahan tradisional
├── [kategori souvenir custom]   -> souvenir pernikahan custom
├── [kategori berdasarkan budget] -> segmentasi harga
├── [detail produk]              -> query spesifik produk + wedding
├── [portofolio wedding]         -> bukti pekerjaan nyata
├── [panduan/artikel]            -> pertanyaan informasional
├── tentang/                     -> informasi identitas bisnis
└── kontak/                      -> pemesanan / konsultasi
```

Nama dalam tanda `[]` adalah **konsep halaman**, bukan URL yang diklaim sudah ada. Pertahankan slug aktual yang sudah aktif (misalnya `/paket/souvenir-tradisional`) apabila sesuai; hindari perubahan URL tanpa kebutuhan dan redirect 301 yang benar.

### Panduan internal linking

1. Homepage menautkan semua kategori prioritas.
2. Kategori menautkan produk yang terkait, dan produk kembali ke kategori utama.
3. Artikel edukasi mengarah secara kontekstual ke kategori/produk yang relevan.
4. Halaman produk dapat menautkan artikel panduan budget, bahan, atau customisasi jika membantu pembeli.
5. Gunakan anchor text natural, bukan repetisi keyword berlebihan.

## 7. Rekomendasi isi homepage

| Urutan | Section | Isi wajib |
|---|---|---|
| 1 | Hero | H1 relevan, deskripsi layanan, foto wedding souvenir, CTA lihat katalog |
| 2 | Kategori | Modern, tradisional, custom, berdasarkan budget |
| 3 | Katalog unggulan | Foto asli, nama, harga indikatif, MOQ, bahan, opsi custom |
| 4 | Pilihan populer | Produk berdasarkan bukti permintaan/penjualan, bukan label “terlaris” tanpa data |
| 5 | Portofolio wedding | Foto hasil nyata, spesifikasi, qty jika boleh dibagikan |
| 6 | Cara pesan | Konsultasi, pilih produk, mockup, persetujuan, produksi, QC, pengiriman |
| 7 | Artikel | Hanya topik yang mendukung souvenir pernikahan |
| 8 | FAQ | Harga, budget, MOQ, waktu produksi, personalisasi, pengiriman |
| 9 | Identitas dan CTA | Profil vendor, kontak, area layanan yang benar, WhatsApp |

### Usulan metadata homepage (untuk diuji)

- **Title:** `Souvenir Pernikahan Custom, Unik & Modern`
- **H1:** `Souvenir Pernikahan Custom, Unik & Berkesan`
- **Meta description:** `Temukan souvenir pernikahan modern dan tradisional yang bisa custom nama. Pilih produk sesuai tema, jumlah tamu, dan budget acara Anda.`
- **Canonical:** `https://souvenirpernikahan.web.id/`
- **Primary keyword:** `souvenir pernikahan`

Metadata adalah usulan; tetap bandingkan dengan title/CTR dan konten sebenarnya sebelum dipublikasikan.

## 8. Checklist khusus landing page statis (HTML, CSS, Bootstrap, JavaScript)

**Stack yang digunakan:** landing page statis dengan HTML5, CSS3, Bootstrap, dan JavaScript. Bootstrap dipertahankan sebagai kerangka UI responsif; CSS custom tetap digunakan untuk branding. **Jangan mengubah proyek menjadi Astro, React, Next.js, atau framework lain hanya demi SEO.**

- [ ] Periksa `index.html` pada root hosting; respons homepage HTTP 200.
- [ ] Konten penting (H1, deskripsi, produk, tautan kategori) langsung tersedia di HTML, bukan hanya dirender dengan JavaScript.
- [ ] Pasang `<title>`, `<meta name="description">`, `<meta name="robots">`, canonical absolut, serta Open Graph di bagian `<head>`.
- [ ] Buat `robots.txt` dan `sitemap.xml` pada root publik (`/robots.txt`, `/sitemap.xml`).
- [ ] Cantumkan hanya URL yang aktif, canonical, dan dapat diindeks dalam `sitemap.xml`; jika hanya punya satu halaman, sitemap boleh memuat homepage saja.
- [ ] Tautan navigasi dan produk menggunakan `<a href="...">` biasa, bukan hanya event `onclick`.
- [ ] Gunakan satu H1 utama dan struktur H2/H3 logis; alt text spesifik untuk foto produk asli.
- [ ] Gunakan JSON-LD `Organization`/`WebSite` yang akurat; `Product`/`Offer` hanya untuk produk nyata dengan data yang sesuai.
- [ ] Hero/LCP memakai ukuran gambar terdefinisi (`width` dan `height`), format gambar efisien, dan bukan `loading="lazy"` bila tampil di atas lipatan.
- [ ] Tambahkan `defer` pada JavaScript non-kritis dan hindari CSS/JS yang menghalangi render bila tidak diperlukan.
- [ ] Pastikan tampilan responsif serta tombol WhatsApp benar-benar berfungsi.
- [ ] Pertahankan komponen Bootstrap yang masih diperlukan (grid, navbar, collapse, carousel, modal) tanpa memasukkan duplikasi CSS atau JavaScript Bootstrap.
- [ ] Pastikan `bootstrap.min.css` dan bila diperlukan `bootstrap.bundle.min.js` dimuat satu kali saja; periksa kompatibilitas atribut komponen dengan versi Bootstrap yang terpasang.
- [ ] Jangan menjadikan konten produk, H1, dan internal link hanya tersedia setelah interaksi Bootstrap (tab, modal, atau carousel) jika konten utama bisa ditampilkan langsung di HTML.
- [ ] Audit CSS custom yang menimpa kelas Bootstrap dan periksa layout shift, breakpoint mobile, serta urutan loading CSS.
- [ ] Jika ada perpindahan URL, gunakan redirect 301 pada layanan hosting, jangan sekadar mengandalkan JavaScript redirect.
- [ ] Uji perubahan pada URL produksi memakai PageSpeed Insights, Rich Results Test, dan Google Search Console.

### Catatan implementasi Bootstrap

- **Tidak perlu migrasi framework** atau membangun ulang layout. Refactor hanya pada section yang mengganggu relevansi keyword atau konversi.
- Gunakan grid `container`, `row`, `col-*` untuk responsivitas dan pertahankan semantic HTML (`main`, `section`, `article`, `nav`) untuk struktur konten.
- Jika menggunakan Bootstrap JS, gunakan bundle yang sesuai versi proyek, tetapi jangan menambahkannya hanya untuk komponen yang tidak memerlukan interaksi.
- Untuk navigasi ke section halaman tunggal, gunakan `<a href="#id-section">`; jangan membuat URL halaman produk atau artikel jika halaman tersebut belum tersedia.
- Verifikasi LCP dan CLS setelah perubahan Bootstrap/CSS dengan PageSpeed Insights.

### Contoh metadata minimal di `index.html`

```html
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Souvenir Pernikahan Custom, Unik & Modern</title>
  <meta name="description" content="Temukan souvenir pernikahan modern dan tradisional yang bisa custom nama. Pilih produk sesuai tema, jumlah tamu, dan budget acara Anda.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://souvenirpernikahan.web.id/">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://souvenirpernikahan.web.id/">
  <meta property="og:title" content="Souvenir Pernikahan Custom, Unik & Modern">
  <meta property="og:description" content="Pilihan souvenir pernikahan modern dan tradisional yang dapat disesuaikan dengan kebutuhan acara.">
</head>
```

### Contoh `robots.txt`

```txt
User-agent: *
Allow: /

Sitemap: https://souvenirpernikahan.web.id/sitemap.xml
```

### Contoh `sitemap.xml` untuk landing page tunggal

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://souvenirpernikahan.web.id/</loc>
  </url>
</urlset>
```

**Catatan:** contoh di atas tidak harus diterapkan mentah-mentah; cocokkan dengan struktur URL, metadata, dan konfigurasi hosting yang sudah aktif. Tidak perlu membuat puluhan URL palsu demi sitemap. Jika seluruh konten hanya ada dalam satu landing page, optimasi SEO fokus pada satu URL tersebut. Jika ada halaman detail produk atau artikel nyata, baru masukkan ke sitemap dan internal link.

## 9. Roadmap implementasi 30 hari

### Minggu 1 — Perbaikan homepage dan baseline data

- [ ] Ekspor data GSC query persis `souvenir pernikahan` untuk 3 bulan terakhir.
- [ ] Audit hero, H1, CTA dan section utama homepage.
- [ ] Hapus atau pindahkan produk corporate/seminar dari area unggulan.
- [ ] Perbarui pilihan artikel homepage menjadi topik souvenir pernikahan.
- [ ] Verifikasi semua testimoni dan profil merek.

**Deliverable:** homepage berfokus pada wedding + baseline GSC.

### Minggu 2 — Katalog, sitemap, dan spesifikasi

- [ ] Tambahkan harga indikatif, MOQ, bahan dan pilihan custom untuk produk prioritas.
- [ ] Buat/optimalkan halaman kategori sesuai intent.
- [ ] Periksa URL detail produk, breadcrumb dan CTA.
- [ ] Validasi sitemap, robots.txt, canonical, indexability.

**Deliverable:** katalog dapat dibandingkan pengunjung dan sitemap valid.

### Minggu 3 — Topical authority dan data terstruktur

- [ ] Audit artikel yang sudah terbit untuk potensi duplikasi intent.
- [ ] Tautkan artikel ke kategori/produk relevan.
- [ ] Optimalkan title, meta description dan heading pada halaman prioritas.
- [ ] Validasi schema per template halaman.

**Deliverable:** cluster konten yang saling terhubung dan konsisten.

### Minggu 4 — Trust, performa, dan evaluasi

- [ ] Tambahkan portofolio wedding autentik.
- [ ] Audit backlink dan laporan tindakan manual, bila relevan.
- [ ] Periksa dan perbaiki performa mobile serta CWV.
- [ ] Bandingkan perubahan impressions, clicks, CTR dan posisi GSC.
- [ ] Catat hipotesis dan tindakan berikutnya menurut data.

**Deliverable:** laporan evaluasi pascaimplementasi dan backlog berikutnya.

## 10. KPI dan cara mengukur

| KPI | Sumber | Penggunaan |
|---|---|---|
| Status indeks homepage/kategori | GSC URL Inspection dan Page Indexing | Pastikan halaman target layak tampil |
| Impressions query utama | GSC Performance, exact query | Mengukur visibilitas |
| Average position | GSC Performance, exact query | Memantau tren ranking, bukan posisi absolut untuk semua pengguna |
| CTR | GSC Performance | Memantau daya tarik snippet dan relevansi intent |
| Organic clicks | GSC Performance | Mengukur kunjungan organik |
| WhatsApp leads dari organic | Tracking event analitik dengan atribusi sesuai persetujuan | Mengukur hasil bisnis |
| Core Web Vitals | GSC CWV / PageSpeed | Mengukur kualitas pengalaman halaman |

**Catatan:** implementasi selama 30 hari tidak menjamin ranking halaman pertama. Peringkat bergantung pada banyak sinyal dan memerlukan evaluasi berkelanjutan.

## 11. Hal-hal yang jangan dilakukan

- Jangan mengganti domain atau DNS tanpa bukti masalah teknis.
- Jangan membuat backlink massal atau membeli tautan spam.
- Jangan langsung disavow satu domain perujuk tanpa audit menyeluruh.
- Jangan membuat harga, testimoni, rating, atau portofolio palsu.
- Jangan menghapus URL aktif tanpa mengukur dampak dan merencanakan redirect.
- Jangan menambah banyak artikel serupa hanya demi frekuensi publikasi.
- Jangan menganggap schema otomatis meningkatkan ranking atau menjamin rich result.
- Jangan mengklaim website terkena penalti tanpa bukti Manual Actions atau kebijakan terkait.

## 12. Data tambahan untuk diagnosis ranking final

1. GSC Performance: exact query `souvenir pernikahan`, 3 bulan, metrik clicks, impressions, CTR, average position.
2. Tab Pages untuk query tersebut: halaman mana yang mendapatkan tayangan.
3. Data halaman/kategori prioritas dari Page Indexing.
4. Sitemap yang telah disubmit dan status pembacaannya.
5. Sampel URL produk dan kategori aktif, beserta data harga/MOQ yang benar.
6. Jika tersedia, laporan backlink dan halaman yang memberi tautan.

## 13. Definition of Done

Audit dan tahap implementasi awal dianggap selesai bila:

- [ ] Homepage dan semua area utama konsisten dengan tema souvenir pernikahan.
- [ ] Produk prioritas memiliki informasi pembelian yang nyata dan lengkap.
- [ ] Testimoni/portofolio yang tampil dapat diverifikasi.
- [ ] Sitemap berhasil diproses dan URL prioritas dapat diindeks.
- [ ] Struktur kategori dan internal link dapat di-crawl.
- [ ] Metadata dan schema setiap tipe halaman valid.
- [ ] Baseline serta evaluasi kinerja keyword utama terdokumentasi.
- [ ] Tidak ada migrasi URL atau disavow yang dilakukan tanpa alasan berbasis bukti.

---

**Ringkasan satu kalimat untuk AI/developer:** Pertahankan domain dan homepage yang sudah terindeks, ubah homepage menjadi landing page komersial khusus souvenir pernikahan, lengkapi katalog dengan data harga/MOQ asli, rapikan identitas bisnis, internal linking, sitemap, metadata dan schema, lalu ukur ranking query utama melalui Search Console sebelum menentukan optimasi lanjutan.
