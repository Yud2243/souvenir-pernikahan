# Prompt untuk AI Antigravity — SEO Crawl Souvenir Pernikahan

Perbaiki proyek website statis HTML/CSS/Bootstrap/JavaScript `souvenirpernikahan.web.id` yang saya buka di workspace.
Target SEO organik: homepage `/` untuk kueri **souvenir pernikahan**.
Target konversi: konsultasi dan permintaan harga lewat WhatsApp `6282131087971`.
Jangan pernah menampilkan harga, membuat harga palsu, atau menambahkan Offer.price. Jangan pindah framework, jangan merusak UI responsive, dan jangan menghapus konten asli tanpa peninjauan.

## Kerjakan dalam repo, bukan hanya menjelaskan
1. Backup file terdampak. Pertahankan `<title>`, H1 dan canonical homepage yang relevan, dan bandingkan dengan `index.html` revisi sebagai acuan desain/SEO.
2. Audit setiap file HTML nyata di repo. Pastikan path internal ke CSS, JS, gambar, dan halaman diawali `/`, bukan `./` atau relatif yang dapat salah resolve pada URL seperti `/penulis/` dan `/blog/artikel/`.
3. Tes semua internal href; status HTTP 200 untuk URL yang ditautkan. Perbaiki 404, link ganda, redirect loops, broken anchors. Jangan membuat URL fiktif.
4. Header/navigasi/desain katalog jelas berfokus souvenir pernikahan. Sediakan informasi bahan, opsi kustom, foto, dan CTA WhatsApp; tanpa harga. Jangan mengarang review, testimoni atau bukti pesanan.
5. Seluruh halaman penting harus punya title dan meta description unik, satu H1 relevan, self-canonical yang sesuai URL final; jangan index halaman error, duplikat, atau halaman yang tidak bermakna.
6. Pertahankan konten penting sebagai HTML server/static yang bisa dibaca tanpa menekan tombol JS. Pertahankan modal bila diinginkan tetapi beri tautan HTML ke halaman produk hanya bila halaman produk yang nyata sudah tersedia.
7. Pastikan `robots.txt` ada pada root domain dan mengizinkan Googlebot mengakses halaman, CSS, JS, gambar. Pastikan sitemap.xml hanya berisi halaman nyata yang indexable/kanonis; jika perlu gunakan `generate_sitemap.py` pada output hasil build. Cantumkan URL sitemap di robots.txt.
8. Cek duplicate Vercel host, www vs non-www, slash vs non-slash. Canonical konsisten ke https://souvenirpernikahan.web.id/; jika memiliki kendali, redirect 301 untuk host sekunder tanpa membuat loop.
9. Rapikan JSON-LD sesuai konten nyata. Jangan isi logo dengan foto hero. Jangan isi legalName atau Product Offer palsu. Tidak perlu metadata keyword spam atau schema berlebihan.
10. Uji desktop/mobile, aksesibilitas navigasi, layout shift, performa LCP. Jangan menjanjikan peringkat #1.

## Laporan yang harus diberikan
- Daftar file berubah serta alasan.
- Tabel URL penting, status HTTP, title, canonical, indexability, jumlah incoming internal links.
- Hasil validasi sitemap/robots, schema, broken links dan responsivitas.
- Instruksi deploy Vercel dan langkah URL Inspection Search Console.
- Catatan bahwa request recrawl tidak menjamin tampil untuk kueri utama dalam 8 jam.
