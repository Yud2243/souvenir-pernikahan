# FOLLOW-UP WAJIB — Perbaikan 3 inkonsistensi nyata (bukan redesign)

Website: https://souvenirpernikahan.web.id/
Keyword dan identitas utama: **souvenir pernikahan**.

**TUJUAN:** Selesaikan tiga masalah yang masih terlihat setelah audit sebelumnya. Perbaiki pada source proyek yang sedang terbuka; jangan sekadar menulis rekomendasi. Ini adalah tugas koreksi akurasi konten dan konsistensi UI, **bukan** tugas redesign atau refactoring.

## A. Statistik Penulis: tertulis 7, faktanya 18

- Periksa halaman `/penulis` dan data artikel yang benar-benar terdaftar/diterbitkan.
- Dalam HTML referensi yang telah diaudit, elemen `#gs-author-articles-grid` berisi **18** tautan kartu `.gs-author-post-card`, sedangkan `.gs-stat-value` untuk label `Artikel Ditulis` menampilkan **7**.
- Perbaiki menjadi **18 Artikel Ditulis** setelah memverifikasi bahwa semua 18 memang merupakan artikel terbit milik penulis tersebut.
- Pilihan terbaik: jika arsitektur mendukung, hitung berdasarkan data artikel yang valid secara otomatis; jangan membuat perhitungan yang bergantung pada jumlah kartu yang sedang ditampilkan (karena ada fitur *Lihat Selengkapnya* dan kartu tersembunyi). Jika implementasi otomatis berisiko mengganggu fitur, cukup ubah 7 menjadi 18 dan laporkan bahwa hitungan masih statis.
- **Jangan mengubah** desain halaman penulis, urutan artikel, link, tombol Load More, biografi, schema `Person`, canonical, maupun metadata SEO.

## B. Halaman paket: hilangkan framing perusahaan dari pengalaman wedding

Audit halaman `/paket`, `/paket/souvenir-modern`, dan `/paket/souvenir-tradisional` serta deskripsi yang tampil dalam kartu, modal, tooltip, FAQ, CTA, gambar alt, dan footer terkait. Temuan yang sudah terverifikasi di `/paket/souvenir-modern`:

- `Pertanyaan Pemesanan Korporat` → ganti menjadi `Pertanyaan Seputar Souvenir Pernikahan`.
- Kalimat yang menyebut `bagian procurement atau panitia acara kantor` → arahkan kepada calon pengantin/panitia pernikahan.
- `Kebutuhan Acara Kantor?` → `Sedang Menyiapkan Souvenir Pernikahan?`.
- `Dapatkan Proposal & Penawaran Resmi` → `Konsultasikan Souvenir Pernikahan Custom`.
- `Kebutuhan Pengadaan` / `SPJ/procurement` / `instansi, seminar` pada copy komersial untuk calon pengantin → ubah secara natural menjadi pembahasan kebutuhan resepsi/akad, jumlah tamu, pilihan custom, kemasan, dan waktu produksi. **Jangan menghilangkan informasi layanan yang benar apabila masih relevan**, cukup jangan dominan dalam konteks wedding.
- Deskripsi footer yang menonjolkan `organisasi serta perusahaan` → ganti menjadi deskripsi utama tentang layanan souvenir pernikahan, dan pastikan footer pada halaman lain konsisten.

**Penting untuk produk yang intrinsik korporat:** contoh `Executive Corporate Gift Set Box` dan plakat penghargaan. Jangan sekadar mengganti nama menjadi "souvenir pernikahan" jika produk dan visual sebenarnya masih jelas korporat. Jika produk memang layak untuk hadiah tamu VIP pernikahan, jelaskan penggunaannya secara benar tanpa mengubah spesifikasi produk; jika tidak cocok, **laporkan sebagai konten tidak relevan dan minta persetujuan sebelum menghapus/memindahkan produk**. Jangan membuat klaim palsu mengenai hasil produksi atau klien.

## C. Portofolio: tulisan pada hover/overlay masih bernuansa perusahaan

- Inspeksi `/portofolio` dan `/detail-portofolio` secara visual dalam browser, termasuk **hover desktop** dan tampilan/tap mobile.
- Temukan asal teks overlay: bisa berupa teks HTML, atribut `data-*`, `title`, `aria-label`, CSS `content`, atau JavaScript. Jangan berasumsi semuanya berasal dari CSS.
- Ubah **hanya** copy overlay/keterangan yang tidak cocok dengan konteks wedding pada kartu/karya yang benar-benar merupakan souvenir pernikahan.
- Untuk karya korporat asli, jangan mengarang bahwa itu pesanan pernikahan. Tandai untuk tinjauan atau usulkan pengelompokan terpisah, **jangan hapus kartu atau mengubah link/slug tanpa persetujuan**.
- Pertahankan gambar, posisi kartu, transisi hover, animasi, navigasi detail, link, dan klik/tap mobile. Jika teks tidak muat di overlay, sesuaikan styling lokal minimal tanpa mengganti struktur utama.

## Larangan mutlak / keamanan SEO

1. Jangan membuat ulang website, mengubah framework, melakukan redesign, atau refactoring besar.
2. Jangan mengubah URL, slug, routing, redirect, canonical, robots.txt, sitemap.xml, schema JSON-LD, title SEO, meta description, atau H1 tanpa persetujuan eksplisit.
3. Jangan menghapus artikel, portofolio, produk, aset asli, atau internal link yang berfungsi.
4. Jangan mengubah nomor WhatsApp, alur konsultasi, CTA yang berfungsi, ataupun strategi **harga tidak ditampilkan**.
5. Boleh mengedit copy yang **terlihat pengguna** pada tiga cakupan A/B/C; boleh edit HTML/CSS/JS secara **minimal** hanya jika diperlukan untuk memperbaiki masalah nyata dan tidak merusak fitur.
6. Jangan melakukan commit, push, atau deploy tanpa persetujuan saya.
7. Jangan memodifikasi artikel edukasi perusahaan yang berdiri sendiri bila tidak berada dalam lingkup halaman wedding, tanpa instruksi baru.

## Prosedur wajib

- Sebelum: buat branch/backup dan daftar file yang akan diedit. Buka halaman live atau local preview yang sesuai; catat kondisi visual dan teks sekarang.
- Implementasikan perubahan minimal dan pastikan setiap istilah yang diganti sesuai konteks, **bukan global find-and-replace buta**.
- Setelah: periksa `/penulis`, `/paket`, `/paket/souvenir-modern`, `/paket/souvenir-tradisional`, `/portofolio`, dan `/detail-portofolio` pada desktop + mobile. Uji hover, modal, tombol, navigasi, filter, load more, WhatsApp, dan keberadaan artikel.
- Jalankan `git diff` dan pastikan perubahan hanya pada file yang memang perlu. Lakukan pemeriksaan output HTML dan console error.
- Buat `LAPORAN_FIX_KONSISTENSI.md`: lokasi dan kutipan sebelum→sesudah; daftar file; jumlah artikel terverifikasi; screenshot portofolio hover; fitur yang diuji; item belum dikerjakan karena perlu persetujuan.
- Jangan menyatakan selesai jika ada inkonsistensi pada tiga cakupan ini yang belum ditangani atau dilaporkan secara jelas.

**DEFINISI SELESAI:** angka penulis sesuai daftar artikel terbit; seluruh narasi paket utama berfokus pada pernikahan; hover portofolio cocok dengan isi karya tanpa label perusahaan yang keliru; semua fungsi, halaman, dan SEO teknis tetap aman.
