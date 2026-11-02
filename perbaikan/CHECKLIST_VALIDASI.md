# Checklist verifikasi setelah implementasi

- [x] Statistik `/penulis` mencerminkan total artikel terbit yang sebenarnya (referensi audit: 18, bukan 7).
- [x] Total artikel mencakup kartu tersembunyi di fitur Lihat Selengkapnya (14 awal + 4 tersembunyi = 18 total).
- [x] Tombol Lihat Selengkapnya/Tutup Artikel berfungsi tanpa error.
- [x] `/paket/souvenir-modern` tidak lagi mempromosikan SPJ, procurement, acara kantor sebagai pesan utama.
- [x] FAQ dan CTA utama paket modern ditulis untuk calon pengantin, tanpa mengubah fakta layanan.
- [x] `/paket` dan `/paket/souvenir-tradisional` sudah dicek untuk teks perusahaan yang tidak relevan (tradisional 100% bersih, paket.html diselaraskan).
- [x] Hover/overlay portofolio desktop dan interaksi mobile sudah dicek seluruh kartu (Kartu 6 & 9 diselaraskan).
- [x] Produk/portofolio korporat asli tidak diklaim sebagai pesanan wedding tanpa bukti (Kartu 3 Executive Seminar Kit dipertahankan jujur).
- [x] Tidak ada produk/halaman yang dihapus atau slug yang diubah.
- [x] Semua link detail, modal, slider, filter, WA, navbar, footer tetap berfungsi.
- [x] Tidak ada harga produk ditambahkan ke kartu atau detail.
- [x] Tidak ada perubahan canonical, meta robots, sitemap, schema, title, H1, URL, redirect (28 JSON-LD tervalidasi).
- [x] Ada screenshot before/after dan laporan diff file (tersimpan dan terdokumentasi di LAPORAN_FIX_KONSISTENSI.md).
- [x] Tidak ada deploy/commit/push tanpa izin pemilik.
