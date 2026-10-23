# design.md — Green’s Souvenir
**Versi:** 1.0  
**Tanggal:** 20 Oktober 2026  
**Produk:** Website katalog souvenir pernikahan dan souvenir custom untuk organisasi/perusahaan  
**Implementasi:** HTML semantik + Bootstrap + CSS kustom + JavaScript vanilla

## 1. Arah Desain
Menciptakan pengalaman katalog yang **segar, lembut, romantis, elegan, dan tepercaya**. Hijau muda menjadi warna identitas, dipadukan dengan putih hangat dan hijau tua agar tetap terbaca serta terasa premium. Hindari tampilan terlalu ramai, terlalu banyak ornamen pernikahan, atau kesan template generik.

Urutan prioritas visual:
1. Foto produk/portofolio autentik.
2. Judul dan manfaat yang jelas.
3. Paket dan detailnya.
4. CTA konsultasi WhatsApp.
5. Elemen dekoratif seperlunya.

## 2. Design Tokens
Gunakan CSS custom properties supaya tema mudah diubah.

```css
:root {
  --gs-green-50: #f3f9f1;
  --gs-green-100: #e5f1df;
  --gs-green-200: #cfe5c4;
  --gs-green-300: #b5d7a6;
  --gs-green-500: #78a96b;
  --gs-green-700: #3f7044;
  --gs-green-900: #23472d;

  --gs-cream: #fffdf8;
  --gs-white: #ffffff;
  --gs-text: #26352a;
  --gs-muted: #657267;
  --gs-border: #dce7d8;
  --gs-whatsapp: #167c45;

  --gs-radius-sm: 0.5rem;
  --gs-radius-md: 1rem;
  --gs-radius-lg: 1.5rem;
  --gs-radius-pill: 999px;

  --gs-shadow-card: 0 12px 32px rgba(35, 71, 45, 0.08);
  --gs-shadow-hover: 0 18px 42px rgba(35, 71, 45, 0.13);

  --gs-container: 1140px;
  --gs-section-space: clamp(3.5rem, 7vw, 6.5rem);
}
```

### Aturan warna
- Background utama: `--gs-cream` atau putih.
- Section alternatif: `--gs-green-50`.
- Tombol utama: `--gs-green-700` dengan teks putih.
- Hover tombol utama: `--gs-green-900`.
- Heading: `--gs-green-900`.
- Body text: `--gs-text`.
- Hijau muda jangan dipakai untuk teks kecil di atas latar putih.
- WhatsApp boleh memakai warna hijau khusus agar fungsi CTA mudah dikenali, tetapi jangan jadikan seluruh website berwarna hijau WhatsApp.

## 3. Tipografi
- Gunakan font system stack untuk performa dan dukungan offline:
  `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`.
- Heading: tebal 650–750, line-height sekitar 1.1–1.2.
- Body: 16–18px desktop, line-height 1.6–1.75.
- Caption: minimal 13–14px dan tetap kontras.
- Gunakan maksimal 2 keluarga font jika kelak menambah font web.
- Hindari semua teks kapital panjang.

## 4. Grid dan Spacing
- Maksimal lebar konten: sekitar 1140px pada desktop.
- Gunakan container Bootstrap dan grid responsif; jangan membuat lebar fixed yang menyebabkan horizontal scroll.
- Jarak section besar: `clamp(3.5rem, 7vw, 6.5rem)`.
- Card padding: 1.25–1.5rem.
- Gunakan ruang kosong yang cukup untuk kesan premium.
- Foto dalam card memakai rasio konsisten; jangan meregangkan gambar.

## 5. Navbar
### Desktop
- Background putih semi-solid atau putih dengan shadow tipis.
- Logo/wordmark Green’s Souvenir di kiri.
- Menu di kanan: Beranda, Tentang, Paket ▼, Portofolio, Blog.
- CTA kecil “Konsultasi” opsional jika tidak membuat navbar penuh.
- Navbar sticky hanya jika tetap tidak menutupi anchor/heading.
- Dropdown Paket menampilkan kategori yang benar-benar tersedia.

### Mobile
- Logo dan tombol menu jelas.
- Menu dapat dibuka dengan tap dan ditutup dengan Escape, tap di luar, atau memilih tautan.
- Dropdown dapat dibuka dengan tap; jangan hanya mengandalkan hover.
- Gunakan `aria-expanded`, `aria-controls`, dan fokus keyboard.
- Pastikan tinggi header tidak memakan layar terlalu banyak.

## 6. Struktur dan Komposisi Halaman

### 6.1 Beranda
1. **Hero**
   - Layout dua kolom pada desktop: copy di kiri, foto produk/komposisi souvenir di kanan.
   - Mobile: judul, deskripsi, CTA, lalu gambar.
   - Eyebrow kecil: “Souvenir Pernikahan & Custom”.
   - H1 contoh: “Souvenir Pernikahan yang Berkesan, Dibuat Lebih Personal”.
   - Subteks singkat tentang pilihan paket dan personalisasi; hanya sebut opsi yang tersedia.
   - CTA primer: “Lihat Paket”.
   - CTA sekunder: “Konsultasi WhatsApp”.
2. **Kategori Paket**
   - Grid 2–4 kolom menyesuaikan breakpoint.
   - Foto, nama kategori, satu kalimat deskripsi, tautan “Lihat pilihan”.
3. **Mengapa Green’s Souvenir**
   - 3–4 poin dengan ikon sederhana dan penjelasan yang faktual.
4. **Cara Memesan**
   - 3–5 langkah: pilih inspirasi/paket → konsultasi → konfirmasi detail/penawaran → persetujuan → proses pesanan. Sesuaikan dengan alur bisnis sebenarnya.
5. **Portofolio Pilihan**
   - Grid foto dengan caption singkat dan tautan ke portofolio.
6. **Testimoni**
   - Hanya jika testimoni nyata dan izin penggunaan tersedia. Jika belum, hilangkan section, jangan isi dengan kutipan buatan.
7. **FAQ**
   - Accordion aksesibel atau daftar tanya-jawab sederhana.
8. **CTA Penutup**
   - Background hijau muda lembut, copy singkat, tombol WhatsApp.
9. **Footer**
   - Ringkasan brand, tautan halaman, kategori paket, kontak WhatsApp, social links jika akun resmi tersedia, dan copyright dinamis opsional.

### 6.2 Tentang
- Hero ringkas dengan foto proses/produk jika ada.
- Cerita brand dan tujuan layanan.
- Nilai layanan dalam 3 kolom.
- Jenis kebutuhan yang dilayani: pernikahan serta organisasi/perusahaan.
- CTA konsultasi.
- Hindari angka statistik dan klaim yang tidak terverifikasi.

### 6.3 Paket
- Intro dengan penjelasan singkat.
- Filter kategori opsional jika jumlah produk cukup banyak.
- Grid card: gambar, nama paket, deskripsi, ringkasan isi, badge “Custom” hanya bila benar, CTA detail/WhatsApp.
- Jangan tampilkan harga placeholder yang tampak seperti harga sebenarnya.
- Jika harga belum tersedia, gunakan CTA “Minta Penawaran”.
- Empty state filter: pesan yang jelas dan tombol reset.

### 6.4 Detail Paket
- Breadcrumb.
- Galeri foto dengan thumbnail yang dapat diakses keyboard.
- Nama paket, ringkasan, isi paket, opsi personalisasi, spesifikasi, ketentuan yang sudah dikonfirmasi.
- CTA WhatsApp menempel secara wajar di bawah ringkasan pada mobile, tidak menutupi konten.
- FAQ paket dan rekomendasi paket lain.

### 6.5 Portofolio
- Grid foto dengan crop konsisten dan object-fit yang tepat.
- Filter kategori jika konten cukup.
- Caption menyebut konteks yang dapat dipublikasikan.
- Klik foto dapat membuka detail/lightbox yang bisa ditutup dengan Escape dan fokus tetap terkelola.
- Jangan menampilkan data pribadi klien atau identitas acara tanpa izin.

### 6.6 Blog
- Header blog dan kategori.
- Card artikel: thumbnail, kategori, judul, ringkasan, tanggal.
- Detail artikel: judul, penulis jika nyata, tanggal terbit/pembaruan, gambar utama, isi dengan heading, daftar isi untuk artikel panjang, CTA kontekstual, sumber, dan artikel terkait.
- Lebar kolom artikel dibatasi agar nyaman dibaca; sekitar 680–760px.
- Sidebar hanya jika membantu dan tidak mengganggu layar mobile.

## 7. Komponen UI
- `gs-button`: primary, secondary, outline, WhatsApp.
- `gs-card`: paket, artikel, portofolio.
- `gs-breadcrumb`.
- `gs-dropdown`.
- `gs-accordion` untuk FAQ.
- `gs-badge` untuk label kategori yang faktual.
- `gs-section-heading`: eyebrow opsional, judul, deskripsi.
- `gs-whatsapp-cta`: tombol CTA inline dan floating (opsional).
- `gs-empty-state`.
- `gs-footer`.

Gunakan prefix `gs-` pada kelas kustom untuk menghindari benturan CSS. Bootstrap dipakai untuk grid/utilitas dan komponen yang diperlukan; CSS kustom mengatur identitas visual. Jangan mengubah selector global seperti `section`, `button`, `img`, atau `a` secara agresif.

## 8. Tombol WhatsApp
Nomor tujuan adalah `6282131087971`. Format link dasar:

```html
<a
  class="btn gs-button gs-button--whatsapp"
  href="https://wa.me/6282131087971?text=Halo%20Green%E2%80%99s%20Souvenir%2C%20saya%20ingin%20konsultasi%20souvenir%20pernikahan."
  target="_blank"
  rel="noopener noreferrer"
  aria-label="Konsultasi souvenir pernikahan melalui WhatsApp"
>
  Konsultasi WhatsApp
</a>
```

- Buat pesan berbeda untuk CTA paket, portofolio, dan blog bila relevan.
- Encode isi pesan dengan benar.
- Jangan masukkan informasi pribadi sensitif ke query string.
- Floating button bersifat opsional; pada mobile jangan menutupi CTA, footer, atau kontrol penting.
- Pastikan link tetap memiliki label teks, bukan ikon saja.

## 9. Motion dan Interaksi
- Transisi ringan 150–250ms untuk hover/focus.
- Hindari animasi masuk yang membuat konten terlambat terlihat.
- Hormati `prefers-reduced-motion: reduce`.
- Tidak ada video autoplay atau carousel otomatis.
- Semua fitur utama tetap dapat digunakan tanpa animasi.
- Dropdown dan menu mobile harus bekerja dengan keyboard dan touch.

## 10. Responsive Behavior
- **Mobile (<576px):** satu kolom, tombol utama mudah ditekan, grid 1–2 kolom sesuai konten, gambar hero tidak terlalu tinggi.
- **Tablet (576–991px):** grid 2 kolom, hero dapat menjadi dua kolom jika cukup lebar.
- **Desktop (≥992px):** hero dua kolom, grid 3–4 kolom bila sesuai.
- Uji pada lebar 320px, 375px, 768px, 1024px, dan 1440px.
- Tidak boleh ada horizontal scroll pada viewport normal.
- Ukuran target sentuh ideal sekitar 44×44px.
- Pastikan layout tetap baik pada zoom 200%.

## 11. Foto dan Asset
- Prioritaskan foto produk yang benar-benar tersedia dan memiliki izin.
- Jangan mengubah produk menjadi desain lain atau menyebut mockup sebagai hasil nyata.
- Gunakan format WebP/AVIF jika kompatibel dengan workflow, dengan fallback bila perlu.
- Set `width` dan `height` untuk mengurangi layout shift.
- Gambar hero utama jangan diberi `loading="lazy"`; gambar bawah fold boleh lazy-load.
- Beri nama file deskriptif, misalnya `souvenir-pernikahan-kemasan-hijau.webp`.
- Alt text menggambarkan isi gambar secara alami, tidak mengulang keyword secara berlebihan.
- Thumbnail sosial berbagi menggunakan gambar landscape sekitar 1200×630px.

## 12. SEO dan Metadata — Desain Implementasi
Setiap halaman perlu metadata unik dan sesuai konten:
- `<title>` unik dan ringkas.
- `meta name="description"` unik.
- `link rel="canonical"` hanya dengan URL domain produksi yang benar.
- `meta name="robots"` disesuaikan dengan environment.
- Open Graph: `og:title`, `og:description`, `og:type`, `og:url`, `og:image`, `og:site_name`, `og:locale`.
- Twitter/X: `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`.
- JSON-LD hanya untuk entitas/halaman yang benar-benar sesuai: `Organization` atau `LocalBusiness`, `WebSite`, `WebPage`, `BreadcrumbList`, `Product`/`Offer` bila faktual, dan `Article`/`BlogPosting` untuk artikel.
- Schema harus konsisten dengan konten yang terlihat. Jangan menambahkan rating, harga, alamat, jam, stok, atau testimoni fiktif.
- Untuk localhost, cegah indexing dan jangan memasang canonical ke domain contoh.
- Schema tidak menjamin rich result atau jawaban AI; validasi sebelum rilis.
- Gunakan satu H1 per halaman, heading terstruktur, internal linking, breadcrumb, dan alt text yang relevan.
- AEO/GEO: jawab pertanyaan dengan jelas, gunakan langkah dan FAQ bermanfaat, tampilkan sumber dan identitas penulis bila relevan, dan jangan menulis konten hanya untuk mengejar mesin jawaban.

## 13. Aksesibilitas
- Struktur landmark semantik.
- Kontras teks yang memadai.
- Fokus keyboard terlihat jelas.
- Dropdown/menu bisa dioperasikan tanpa mouse.
- Semua tombol punya nama aksesibel.
- Form memiliki label dan error yang jelas jika kelak ada.
- Alt gambar bermakna; gambar dekoratif memakai alt kosong.
- FAQ accordion memakai tombol dan atribut ARIA yang sesuai.
- Uji navigasi keyboard dan reduced motion.

## 14. Struktur File yang Disarankan
```text
greens-souvenir/
├── index.html
├── tentang.html
├── paket.html
├── paket/
│   ├── souvenir-tradisional.html
│   └── souvenir-modern.html
├── portofolio.html
├── blog.html
├── blog/
│   ├── cara-menghitung-jumlah-souvenir.html
│   ├── checklist-pemesanan-souvenir-pernikahan.html
│   ├── ide-kemasan-souvenir-pernikahan.html
│   ├── panduan-memilih-souvenir-pernikahan.html
│   ├── panduan-souvenir-perusahaan.html
│   └── personalisasi-nama-dan-tanggal-souvenir.html
├── 404.html
├── kebijakan-privasi.html
├── assets/
│   ├── css/
│   │   ├── style.css
│   │   └── style.min.css
│   ├── js/
│   │   ├── main.js
│   │   └── main.min.js
│   ├── images/
│   └── icons/
├── robots.txt
├── sitemap.xml
├── vercel.json
└── .htaccess
```

Catatan Arsitektur URL & Struktur Folder:
- Tidak ada file `index.html` di dalam subfolder `blog/`, `paket/`, maupun subfolder lainnya. Halaman katalog/listing berada di root (`blog.html` dan `paket.html`).
- Subfolder `blog/` dan `paket/` hanya berisi halaman detail artikel dan produk.
- URL routing pada web server (Vercel `vercel.json` dan Apache `.htaccess`) telah dikonfigurasi dengan `cleanUrls` dan URL rewrite agar saat pengguna mengakses `/blog` atau `/paket`, server langsung menampilkan file `blog.html` dan `paket.html` tanpa mencari `index.html` di dalam folder tersebut dan tanpa memunculkan `index` pada URL bar.
- Bila nanti dipindahkan ke WordPress, URL dan template akan menyesuaikan struktur WordPress; jangan menganggap struktur folder statis akan otomatis menjadi struktur WordPress.

## 15. Checklist Sebelum Rilis
- [ ] Brand, logo, paket, foto, dan konten sudah disetujui.
- [ ] Tidak ada data bisnis yang dikarang.
- [ ] Semua CTA WhatsApp diuji.
- [ ] Dropdown dan menu mobile dapat digunakan dengan keyboard dan sentuhan.
- [ ] Tampilan mobile, tablet, desktop, zoom, dan reduced motion diuji.
- [ ] Title, description, canonical, OG, dan Twitter metadata unik.
- [ ] Localhost noindex; konfigurasi produksi dipisahkan.
- [ ] JSON-LD divalidasi dan sesuai konten yang terlihat.
- [ ] Gambar dioptimalkan dan tidak menyebabkan layout shift berlebihan.
- [ ] Tautan internal, gambar, halaman 404, dan console diperiksa.
- [ ] Sitemap/robots/canonical menggunakan domain produksi yang benar setelah peluncuran.
