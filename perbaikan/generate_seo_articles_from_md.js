const fs = require('fs');
const path = require('path');

const mdPath = 'e:/tele/paket-artikel-seo-souvenir-pernikahan-unik.md';
const content = fs.readFileSync(mdPath, 'utf-8');

const SITE_ORIGIN = "https://souvenirpernikahan.web.id";
const UPLOAD_DATE_ISO = "2026-11-24T14:35:00+07:00";
const UPLOAD_DATE_STR = "24 November 2026";
const UPLOAD_TIME_SHORT = "2026-11-24";

function sanitize(text) {
  if (!text) return "";
  let t = text;
  t = t.replace(/\b(ekonomis)\b/gi, 'terjangkau');
  t = t.replace(/\b(murah)\b/gi, 'terjangkau');
  t = t.replace(/\b(low\s*budget)\b/gi, 'ramah anggaran');
  return t;
}

function slugify(text) {
  return text.toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-');
}

// Global area served & schema local business with parent organization Saka Souvenir
const areaServedList = [
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
];

const canonicalLocalBusiness = {
  "@type": ["Organization", "LocalBusiness"],
  "@id": `${SITE_ORIGIN}/#organization`,
  "name": "SEKATA",
  "url": `${SITE_ORIGIN}/`,
  "logo": {
    "@type": "ImageObject",
    "url": `${SITE_ORIGIN}/assets/profile/logo-navbar-120.webp`
  },
  "image": `${SITE_ORIGIN}/assets/images/hero-souvenir.webp`,
  "description": "SEKATA adalah spesialis souvenir pernikahan dari Saka Souvenir (sakasouvenir.com). Kami berfokus 100% pada souvenir pernikahan custom elegan, kriya bernilai budaya, dan kemasan berkelas di Malang dengan pengiriman ke seluruh Indonesia.",
  "parentOrganization": {
    "@type": "Organization",
    "name": "Saka Souvenir",
    "url": "https://sakasouvenir.com",
    "sameAs": [
      "https://sakasouvenir.com",
      "https://www.instagram.com/sakasouvenirmlg/"
    ]
  },
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
      "opens": "08:00",
      "closes": "17:00"
    }
  ],
  "areaServed": areaServedList,
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
  ],
  "alternateName": ["SEKATA Souvenir Pernikahan", "Souvenir Pernikahan"]
};

const canonicalWebsite = {
  "@type": "WebSite",
  "@id": `${SITE_ORIGIN}/#website`,
  "url": `${SITE_ORIGIN}/`,
  "name": "SEKATA",
  "description": "Pusat souvenir pernikahan elegan, cinderamata custom bernilai budaya, dan kemasan eksklusif di Malang dan seluruh Indonesia. Bagian dari Saka Souvenir (sakasouvenir.com).",
  "publisher": {
    "@id": `${SITE_ORIGIN}/#organization`
  },
  "inLanguage": "id-ID",
  "potentialAction": {
    "@type": "SearchAction",
    "target": `${SITE_ORIGIN}/blog?q={search_term_string}`,
    "query-input": "required name=search_term_string"
  },
  "alternateName": ["SEKATA Souvenir Pernikahan", "Souvenir Pernikahan"]
};

// Split markdown into 4 articles
const rawSections = content.split(/^# (ARTIKEL PILAR|CLUSTER 1|CLUSTER 2|CLUSTER 3)/m);
const articles = [];

for (let i = 1; i < rawSections.length; i += 2) {
  const type = rawSections[i];
  const body = rawSections[i + 1].trim();
  articles.push({ type, raw: body });
}

console.log(`Found ${articles.length} articles to process.`);

// Process each article
articles.forEach((art, idx) => {
  const raw = art.raw;
  const lines = raw.split('\n').map(l => l.trimEnd());
  
  // Extract Title (first line starting with # )
  let title = "";
  let lead = "";
  let metaTitle = "";
  let slug = "";
  let metaDesc = "";
  let focusKeyphrase = "";
  let primaryEntity = "";
  let secondaryEntities = "";
  let audience = "";
  
  let i = 0;
  // find first #
  while (i < lines.length) {
    if (lines[i].startsWith('# ')) {
      title = lines[i].replace(/^#\s+/, '').trim();
      i++;
      break;
    }
    i++;
  }
  
  // read lead (lines until **Meta Title:**)
  const leadLines = [];
  while (i < lines.length && !lines[i].startsWith('**Meta Title:')) {
    if (lines[i].trim()) leadLines.push(lines[i].trim());
    i++;
  }
  lead = leadLines.join(' ');
  
  // parse metadata block
  while (i < lines.length && !lines[i].startsWith('## ')) {
    const l = lines[i];
    if (l.startsWith('**Meta Title:**')) metaTitle = l.replace('**Meta Title:**', '').trim();
    if (l.startsWith('**Slug:**')) slug = l.replace('**Slug:**', '').trim();
    if (l.startsWith('**Meta Description:**')) {
      let desc = l.replace('**Meta Description:**', '').trim();
      let j = i + 1;
      while (j < lines.length && !lines[j].startsWith('**') && !lines[j].startsWith('## ')) {
        if (lines[j].trim()) desc += ' ' + lines[j].trim();
        j++;
      }
      metaDesc = desc;
      i = j - 1;
    }
    if (l.startsWith('**Focus Keyphrase:**')) focusKeyphrase = l.replace('**Focus Keyphrase:**', '').trim();
    if (l.startsWith('**Primary Entity:**')) primaryEntity = l.replace('**Primary Entity:**', '').trim();
    if (l.startsWith('**Secondary Entities:**')) secondaryEntities = l.replace('**Secondary Entities:**', '').trim();
    if (l.startsWith('**Audience:**')) audience = l.replace('**Audience:**', '').trim();
    i++;
  }
  
  // Content from first ## onwards
  const contentLines = lines.slice(i);
  
  art.title = sanitize(title);
  art.lead = sanitize(lead);
  art.metaTitle = sanitize(metaTitle);
  art.slug = slug;
  art.metaDesc = sanitize(metaDesc);
  art.focusKeyphrase = focusKeyphrase;
  art.primaryEntity = primaryEntity;
  art.secondaryEntities = secondaryEntities;
  art.contentLines = contentLines;
});

// Configure custom badges, read time, images, related
const configs = [
  {
    category: "Pilar Panduan",
    topicTag: "Ide Souvenir",
    readTime: "12 Menit Baca",
    wordCount: 2850,
    timeReq: "PT12M",
    heroAlt: "Koleksi 85 ide souvenir pernikahan unik dan berkesan untuk seluruh tamu undangan",
    coverCaption: "Inspirasi 85 pilihan souvenir pernikahan unik dari SEKATA (bagian dari Saka Souvenir) yang menggabungkan nilai fungsi, estetika, dan sentuhan kriya nusantara.",
    keyTakeaways: [
      "Souvenir pernikahan terbaik mengutamakan nilai manfaat sehari-hari dan keselarasan dengan konsep pesta (rustic, modern, etnik).",
      "Pilihan 85 ide terbagi dalam 6 kategori: fungsional, elegan, ramah lingkungan, kreatif, kuliner, dan personal bernilai kenangan.",
      "Personalisasi inisial nama dan tanggal pernikahan memperkuat ikatan emosional tanpa mengurangi fungsi barang.",
      "Konsultasikan pemilihan material, estimasi pengerjaan, dan proteksi pengiriman bersama workshop resmi SEKATA Malang."
    ],
    bacaJuga1: {
      title: "Tips Memilih Souvenir Pernikahan Unik Sesuai Konsep Acara",
      link: "/blog/tips-memilih-souvenir-pernikahan-unik"
    },
    bacaJuga2: {
      title: "Rekomendasi Souvenir Pernikahan Unik dan Bermanfaat",
      link: "/blog/souvenir-pernikahan-unik-dan-bermanfaat"
    },
    related: [
      { slug: "tips-memilih-souvenir-pernikahan-unik", title: "Tips Memilih Souvenir Pernikahan Unik Sesuai Tema & Konsep Acara", excerpt: "Panduan lengkap memilih souvenir sesuai karakter tamu, tema dekorasi, dan alur pemesanan aman.", img: "/assets/images/artikel/tips-memilih-souvenir-pernikahan-unik.webp", cat: "Cluster Panduan" },
      { slug: "souvenir-pernikahan-unik-dan-bermanfaat", title: "Rekomendasi Souvenir Pernikahan Unik dan Bermanfaat untuk Berbagai Kalangan", excerpt: "Perbandingan 12 souvenir fungsional: tumbler, mug, pouch, totebag, dan set kriya bernilai guna tinggi.", img: "/assets/images/artikel/souvenir-pernikahan-unik-dan-bermanfaat.webp", cat: "Cluster Produk" },
      { slug: "souvenir-pernikahan-unik-custom", title: "Souvenir Pernikahan Unik Custom untuk Momen Personal Hari Bahagia", excerpt: "Pilihan personalisasi grafir laser, cetak UV, kemasan hardbox mewah, dan tahapan konsultasi vendor.", img: "/assets/images/artikel/souvenir-pernikahan-unik-custom.webp", cat: "Cluster Custom" }
    ]
  },
  {
    category: "Tips Memilih",
    topicTag: "Konsep & Tema",
    readTime: "9 Menit Baca",
    wordCount: 2250,
    timeReq: "PT9M",
    heroAlt: "Tips memilih souvenir pernikahan unik sesuai konsep rustic, minimalis, elegan, dan tradisional",
    coverCaption: "Menyesuaikan souvenir pernikahan dengan tema dekorasi menciptakan harmoni visual yang memikat bagi para tamu undangan.",
    keyTakeaways: [
      "Kesesuaian tema pernikahan (rustic, modern minimalis, etnik, garden party) menjadi kunci keselarasan visual souvenir.",
      "Kenali demografi tamu undangan (keluarga, teman sebaya, rekan kerja) untuk menentukan fungsi souvenir yang tepat sasaran.",
      "Perhitungan jumlah souvenir harus mencakup kuantitas buffer stock (cadangan) guna mengantisipasi penambahan tamu.",
      "SEKATA (bagian dari Saka Souvenir) menyediakan konsultasi sampel gratis di workshop Malang maupun daring."
    ],
    bacaJuga1: {
      title: "85 Ide Souvenir Pernikahan Unik dan Berkesan untuk Tamu",
      link: "/blog/ide-souvenir-pernikahan-unik"
    },
    bacaJuga2: {
      title: "Souvenir Pernikahan Unik Custom dan Personal",
      link: "/blog/souvenir-pernikahan-unik-custom"
    },
    related: [
      { slug: "ide-souvenir-pernikahan-unik", title: "85 Ide Souvenir Pernikahan Unik dan Berkesan untuk Tamu Undangan", excerpt: "Eksplorasi 85 inspirasi cinderamata pernikahan fungsional, elegan, dan bernilai budaya.", img: "/assets/images/artikel/ide-souvenir-pernikahan-unik.webp", cat: "Pilar Utama" },
      { slug: "souvenir-pernikahan-unik-dan-bermanfaat", title: "Rekomendasi Souvenir Pernikahan Unik dan Bermanfaat untuk Berbagai Kalangan", excerpt: "Ulasan 12 produk fungsional yang paling dicari calon pengantin beserta tabel pertimbangan mutunya.", img: "/assets/images/artikel/souvenir-pernikahan-unik-dan-bermanfaat.webp", cat: "Cluster Produk" },
      { slug: "souvenir-pernikahan-unik-custom", title: "Souvenir Pernikahan Unik Custom untuk Momen Personal Hari Bahagia", excerpt: "Teknik personalisasi nama, tanggal, monogram, dan kemasan kustom bersama spesialis wedding SEKATA.", img: "/assets/images/artikel/souvenir-pernikahan-unik-custom.webp", cat: "Cluster Custom" }
    ]
  },
  {
    category: "Rekomendasi Produk",
    topicTag: "Souvenir Fungsional",
    readTime: "10 Menit Baca",
    wordCount: 2400,
    timeReq: "PT10M",
    heroAlt: "Rekomendasi souvenir pernikahan unik dan bermanfaat dari tumbler, pouch, hingga alat makan kriya",
    coverCaption: "Souvenir fungsional seperti tumbler grafir, pouch kanvas, dan set alat makan kayu memberikan nilai guna jangka panjang bagi para tamu.",
    keyTakeaways: [
      "Souvenir bernilai guna tinggi memastikan cinderamata tidak terbuang atau sekadar disimpan tanpa manfaat nyata.",
      "12 produk unggulan fungsional: tumbler, mug, pouch serbaguna, totebag, notebook, pulpen, coaster, handuk, alat makan, lilin, tanaman, dan gantungan kunci.",
      "Tabel komparasi fungsi dan material membantu calon pengantin memilih produk sesuai alokasi anggaran.",
      "Produksi resmi ditangani dengan standar kontrol kualitas ketat oleh workshop SEKATA di Malang."
    ],
    bacaJuga1: {
      title: "85 Ide Souvenir Pernikahan Unik dan Berkesan",
      link: "/blog/ide-souvenir-pernikahan-unik"
    },
    bacaJuga2: {
      title: "Souvenir Pernikahan Unik Custom untuk Sentuhan Personal",
      link: "/blog/souvenir-pernikahan-unik-custom"
    },
    related: [
      { slug: "ide-souvenir-pernikahan-unik", title: "85 Ide Souvenir Pernikahan Unik dan Berkesan untuk Tamu Undangan", excerpt: "Kumpulan inspirasi cinderamata lengkap dari berbagai kategori produk dan konsep pernikahan.", img: "/assets/images/artikel/ide-souvenir-pernikahan-unik.webp", cat: "Pilar Utama" },
      { slug: "tips-memilih-souvenir-pernikahan-unik", title: "Tips Memilih Souvenir Pernikahan Unik Sesuai Tema & Konsep Acara", excerpt: "Strategi mencocokkan tema pernikahan dengan bahan cinderamata dan penghitungan jumlah pesanan.", img: "/assets/images/artikel/tips-memilih-souvenir-pernikahan-unik.webp", cat: "Cluster Panduan" },
      { slug: "souvenir-pernikahan-unik-custom", title: "Souvenir Pernikahan Unik Custom untuk Momen Personal Hari Bahagia", excerpt: "Panduan teknis pembuatan souvenir custom nama mempelai, monogram eksklusif, dan kemasan mewah.", img: "/assets/images/artikel/souvenir-pernikahan-unik-custom.webp", cat: "Cluster Custom" }
    ]
  },
  {
    category: "Panduan Custom",
    topicTag: "Personalisasi",
    readTime: "10 Menit Baca",
    wordCount: 2500,
    timeReq: "PT10M",
    heroAlt: "Souvenir pernikahan unik custom dengan sentuhan nama pengantin, monogram, dan kemasan berkelas",
    coverCaption: "Sentuhan personalisasi nama, tanggal akad, dan kemasan premium menjadikan cinderamata pernikahan bernilai emosional tinggi.",
    keyTakeaways: [
      "Personalisasi nama, tanggal, dan inisial mempelai memberikan identitas khas yang abadi pada setiap souvenir.",
      "Teknik pengerjaan presisi: grafir laser pada kayu/logam, sablon & bordir pada kain pouch, serta cetak UV pada akrilik.",
      "Tahapan pemesanan terstruktur menjamin desain mockup disetujui calon pengantin sebelum produksi massal dimulai.",
      "SEKATA adalah spesialis souvenir pernikahan dari Saka Souvenir (sakasouvenir.com) yang menjamin garansi kirim 100% aman se-Indonesia."
    ],
    bacaJuga1: {
      title: "85 Ide Souvenir Pernikahan Unik dan Berkesan",
      link: "/blog/ide-souvenir-pernikahan-unik"
    },
    bacaJuga2: {
      title: "Tips Memilih Souvenir Pernikahan Unik Sesuai Konsep Acara",
      link: "/blog/tips-memilih-souvenir-pernikahan-unik"
    },
    related: [
      { slug: "ide-souvenir-pernikahan-unik", title: "85 Ide Souvenir Pernikahan Unik dan Berkesan untuk Tamu Undangan", excerpt: "Inspirasi 85 cinderamata pernikahan unik bernilai estetika dan guna tinggi.", img: "/assets/images/artikel/ide-souvenir-pernikahan-unik.webp", cat: "Pilar Utama" },
      { slug: "tips-memilih-souvenir-pernikahan-unik", title: "Tips Memilih Souvenir Pernikahan Unik Sesuai Tema & Konsep Acara", excerpt: "Panduan menyelaraskan souvenir dengan tema rustic, modern, etnik, dan tips komunikasi vendor.", img: "/assets/images/artikel/tips-memilih-souvenir-pernikahan-unik.webp", cat: "Cluster Panduan" },
      { slug: "souvenir-pernikahan-unik-dan-bermanfaat", title: "Rekomendasi Souvenir Pernikahan Unik dan Bermanfaat untuk Berbagai Kalangan", excerpt: "Rekomendasi 12 souvenir fungsional yang mudah diterima dan disukai oleh semua kelompok tamu.", img: "/assets/images/artikel/souvenir-pernikahan-unik-dan-bermanfaat.webp", cat: "Cluster Produk" }
    ]
  }
];

// Helper to convert markdown content into clean semantic HTML sections & extract FAQs
function parseMarkdownToHtml(contentLines, artConfig, artIdx) {
  const sections = [];
  const faqs = [];
  let currentH2 = null;
  let inFaq = false;
  let inTable = false;
  let tableRows = [];
  let inList = false;
  let listType = 'ul'; // 'ul' or 'ol'
  let listItems = [];

  function flushList() {
    if (!inList) return;
    const tag = listType;
    let html = `<${tag} class="gs-article__list">`;
    listItems.forEach(item => {
      html += `<li>${item}</li>`;
    });
    html += `</${tag}>`;
    if (currentH2) currentH2.elements.push(html);
    inList = false;
    listItems = [];
  }

  function flushTable() {
    if (!inTable) return;
    if (tableRows.length > 0) {
      let html = `<div class="gs-article__table-wrapper"><table class="gs-article__table">`;
      // first row header
      const headerRow = tableRows[0];
      html += `<thead><tr>`;
      headerRow.forEach(h => html += `<th scope="col">${h}</th>`);
      html += `</tr></thead><tbody>`;
      for (let r = 1; r < tableRows.length; r++) {
        html += `<tr>`;
        tableRows[r].forEach((c, ci) => {
          if (ci === 0) html += `<td><strong>${c}</strong></td>`;
          else html += `<td>${c}</td>`;
        });
        html += `</tr>`;
      }
      html += `</tbody></table></div>`;
      if (currentH2) currentH2.elements.push(html);
    }
    inTable = false;
    tableRows = [];
  }

  for (let idx = 0; idx < contentLines.length; idx++) {
    const rawLine = contentLines[idx];
    const trimmed = rawLine.trim();

    // Check FAQ Header
    if (trimmed.startsWith('## Yang Sering Ditanyakan') || trimmed.startsWith('## FAQ')) {
      flushList();
      flushTable();
      inFaq = true;
      currentH2 = {
        title: "Pertanyaan yang Sering Diajukan",
        id: "faq-pertanyaan",
        elements: []
      };
      sections.push(currentH2);
      continue;
    }

    if (inFaq) {
      if (trimmed.startsWith('### ')) {
        const q = sanitize(trimmed.replace(/^###\s+/, '').trim());
        let aLines = [];
        let j = idx + 1;
        while (j < contentLines.length && !contentLines[j].trim().startsWith('### ') && !contentLines[j].trim().startsWith('## ') && !contentLines[j].trim().startsWith('---')) {
          if (contentLines[j].trim()) aLines.push(contentLines[j].trim());
          j++;
        }
        const a = sanitize(aLines.join(' '));
        faqs.push({ q, a });
        idx = j - 1;
      }
      continue;
    }

    // Check H2
    if (trimmed.startsWith('## ')) {
      flushList();
      flushTable();
      const h2Text = sanitize(trimmed.replace(/^##\s+/, '').trim());
      const h2Id = slugify(h2Text);
      currentH2 = {
        title: h2Text,
        id: h2Id,
        elements: []
      };
      sections.push(currentH2);
      continue;
    }

    // Check H3
    if (trimmed.startsWith('### ')) {
      flushList();
      flushTable();
      const h3Text = sanitize(trimmed.replace(/^###\s+/, '').trim());
      const h3Id = slugify(h3Text);
      if (currentH2) {
        currentH2.elements.push(`<h3 id="${h3Id}">${h3Text}</h3>`);
      }
      continue;
    }

    // Check Table row (| ... |)
    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      flushList();
      inTable = true;
      if (trimmed.includes('---')) {
        // separator row, skip
        continue;
      }
      const cells = trimmed.split('|').slice(1, -1).map(c => sanitize(c.trim()));
      tableRows.push(cells);
      continue;
    } else if (inTable) {
      flushTable();
    }

    // Check Ordered List (1. item)
    const olMatch = trimmed.match(/^(\d+)\.\s+(.*)/);
    if (olMatch) {
      if (inList && listType !== 'ol') flushList();
      inList = true;
      listType = 'ol';
      let itemContent = sanitize(olMatch[2].trim());
      itemContent = itemContent.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      listItems.push(itemContent);
      continue;
    }

    // Check Unordered List (- item or * item)
    const ulMatch = trimmed.match(/^[-*]\s+(.*)/);
    if (ulMatch) {
      if (inList && listType !== 'ul') flushList();
      inList = true;
      listType = 'ul';
      let itemContent = sanitize(ulMatch[1].trim());
      itemContent = itemContent.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      // replace external image links or raw markdown links with clean mentions
      itemContent = itemContent.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
      listItems.push(itemContent);
      continue;
    }

    // If we were in a list, check continuation line
    if (inList) {
      if (trimmed === '') {
        flushList();
        continue;
      } else if (!trimmed.startsWith('#')) {
        let cont = sanitize(trimmed);
        cont = cont.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        cont = cont.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
        listItems[listItems.length - 1] += ' ' + cont;
        continue;
      } else {
        flushList();
      }
    }

    // Skip empty lines or horizontal rules
    if (!trimmed || trimmed === '---' || trimmed.startsWith('-----------------')) {
      continue;
    }

    // Regular paragraph
    let pContent = sanitize(trimmed);
    pContent = pContent.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    pContent = pContent.replace(/\*(.*?)\*/g, '<em>$1</em>');
    // Sanitize any raw OpenAI/Shopee markdown links
    pContent = pContent.replace(/\[([^\]]+)\]\(https?:\/\/[^)]+\)/g, '$1');
    pContent = pContent.replace(/Referensi visual:.*$/g, '');

    if (pContent.trim() && currentH2) {
      currentH2.elements.push(`<p>${pContent.trim()}</p>`);
    }
  }

  flushList();
  flushTable();

  return { sections, faqs };
}

// Generate each HTML file
articles.forEach((art, idx) => {
  const conf = configs[idx];
  const { sections, faqs } = parseMarkdownToHtml(art.contentLines, conf, idx);
  
  // Build TOC items
  const tocItems = sections.map(s => {
    return `<li><a href="#${s.id}">${s.title}</a></li>`;
  }).join('\n                ');
  
  // Build FAQ JSON-LD mainEntity
  const faqJsonLd = faqs.map(f => {
    return {
      "@type": "Question",
      "name": f.q,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": f.a
      }
    };
  });

  // Build ItemList for Schema
  const itemListElements = sections.map((s, si) => ({
    "@type": "ListItem",
    "position": si + 1,
    "name": s.title
  }));

  const structuredData = {
    "@context": "https://schema.org",
    "@graph": [
      canonicalLocalBusiness,
      canonicalWebsite,
      {
        "@type": "BlogPosting",
        "@id": `${SITE_ORIGIN}/blog/${art.slug}#article`,
        "isPartOf": {
          "@id": `${SITE_ORIGIN}/#website`
        },
        "headline": art.title,
        "description": art.metaDesc,
        "image": {
          "@type": "ImageObject",
          "url": `${SITE_ORIGIN}/assets/images/artikel/${art.slug}.webp`,
          "width": 1200,
          "height": 630
        },
        "datePublished": UPLOAD_DATE_ISO,
        "dateModified": UPLOAD_DATE_ISO,
        "inLanguage": "id-ID",
        "mainEntityOfPage": `${SITE_ORIGIN}/blog/${art.slug}`,
        "author": {
          "@type": "Person",
          "@id": `${SITE_ORIGIN}/penulis#person`,
          "name": "Yudi Abraham",
          "url": `${SITE_ORIGIN}/penulis`,
          "jobTitle": "Technology Writer & Wedding Favors Specialist",
          "description": "Penulis konten edukatif seputar souvenir pernikahan, tips cinderamata acara, inspirasi kemasan elegan, serta integrasi teknologi web di Souvenir Pernikahan."
        },
        "publisher": {
          "@id": `${SITE_ORIGIN}/#organization`
        },
        "speakable": {
          "@type": "SpeakableSpecification",
          "cssSelector": [
            ".gs-article__title",
            ".gs-article__lead",
            ".gs-article__key-takeaway p",
            ".gs-article__key-takeaway li"
          ]
        },
        "articleSection": conf.category,
        "keywords": `${art.focusKeyphrase}, souvenir pernikahan unik, wedding favors, souvenir pernikahan bermanfaat, souvenir custom malang, sekata souvenir`,
        "wordCount": conf.wordCount,
        "timeRequired": conf.timeReq,
        "isAccessibleForFree": true,
        "license": `${SITE_ORIGIN}/kebijakan-privasi`,
        "about": [
          {
            "@type": "Thing",
            "name": "Souvenir Pernikahan",
            "sameAs": "https://id.wikipedia.org/wiki/Cendera_mata"
          },
          {
            "@type": "Thing",
            "name": "Pernikahan",
            "sameAs": "https://id.wikipedia.org/wiki/Pernikahan"
          }
        ],
        "mentions": [
          {
            "@type": "Place",
            "name": "Kota Malang",
            "sameAs": "https://id.wikipedia.org/wiki/Kota_Malang"
          },
          {
            "@type": "Organization",
            "name": "Saka Souvenir",
            "url": "https://sakasouvenir.com"
          }
        ],
        "primaryImageOfPage": {
          "@type": "ImageObject",
          "url": `${SITE_ORIGIN}/assets/images/artikel/${art.slug}.webp`,
          "width": 1200,
          "height": 630
        }
      },
      {
        "@type": "BreadcrumbList",
        "@id": `${SITE_ORIGIN}/blog/${art.slug}#breadcrumb`,
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": "Beranda",
            "item": `${SITE_ORIGIN}/`
          },
          {
            "@type": "ListItem",
            "position": 2,
            "name": "Blog",
            "item": `${SITE_ORIGIN}/blog`
          },
          {
            "@type": "ListItem",
            "position": 3,
            "name": art.title,
            "item": `${SITE_ORIGIN}/blog/${art.slug}`
          }
        ]
      },
      {
        "@type": "ItemList",
        "@id": `${SITE_ORIGIN}/blog/${art.slug}#itemlist`,
        "name": `Poin Pembahasan: ${art.title}`,
        "numberOfItems": itemListElements.length,
        "itemListElement": itemListElements
      },
      {
        "@type": "FAQPage",
        "@id": `${SITE_ORIGIN}/blog/${art.slug}#faq`,
        "mainEntity": faqJsonLd
      }
    ]
  };

  // Build Sections HTML
  let sectionsHtml = "";
  sections.forEach((sec, sidx) => {
    if (sec.id === 'faq-pertanyaan') {
      // render FAQ accordion
      sectionsHtml += `
      <section class="gs-article__section gs-article__section--faq" id="${sec.id}" aria-labelledby="heading-${sec.id}">
        <h2 id="heading-${sec.id}">${sec.title}</h2>
        <div class="gs-accordion" id="accordion-${art.slug}">
      `;
      faqs.forEach((faq, fidx) => {
        sectionsHtml += `
          <div class="gs-accordion__item">
            <button class="gs-accordion__trigger" aria-expanded="false" aria-controls="faq-ans-${idx}-${fidx}">
              <span>${faq.q}</span>
              <span class="gs-accordion__icon" aria-hidden="true">
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 6l4 4 4-4" />
                </svg>
              </span>
            </button>
            <div class="gs-accordion__panel" id="faq-ans-${idx}-${fidx}">
              <p>${faq.a}</p>
            </div>
          </div>
        `;
      });
      sectionsHtml += `
        </div>
      </section>
      `;
      return;
    }

    sectionsHtml += `
      <section class="gs-article__section" id="${sec.id}" aria-labelledby="heading-${sec.id}">
        <h2 id="heading-${sec.id}">${sec.title}</h2>
        ${sec.elements.join('\n')}
      </section>
    `;

    // Interleave Baca Juga and Figures at strategic points
    if (sidx === 0) {
      sectionsHtml += `
      <!-- Baca Juga Box 1 -->
      <div class="gs-article__baca-juga" data-gs-animate>
        <div class="gs-article__baca-juga-icon" aria-hidden="true">
          <svg viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="gs-article__baca-juga-content">
          <strong>Rekomendasi Terkait:</strong> Baca juga panduan <a href="${conf.bacaJuga1.link}">${conf.bacaJuga1.title}</a> untuk referensi yang lebih lengkap.
        </div>
      </div>
      `;
    } else if (sidx === 2) {
      sectionsHtml += `
      <!-- Contextual Callout Sekata & Saka Souvenir -->
      <div class="gs-article__highlight-box" style="background:var(--gs-green-50);border-left:4px solid var(--gs-green-700);padding:1.25rem 1.5rem;border-radius:var(--gs-radius-md);margin:1.75rem 0;" data-gs-animate>
        <h4 style="margin:0 0 0.5rem 0;color:var(--gs-green-900);font-size:1.05rem;">💡 Butuh Konsultasi Pemilihan Souvenir Sesuai Konsep?</h4>
        <p style="margin:0;font-size:0.92rem;color:var(--gs-text);line-height:1.65;">
          <strong>SEKATA</strong> adalah spesialis souvenir pernikahan dari <strong><a href="https://sakasouvenir.com" target="_blank" rel="noopener noreferrer" style="color:var(--gs-green-800);text-decoration:underline;">Saka Souvenir</a></strong>. Kami berpusat di workshop Kota Malang dan melayani pemesanan souvenir custom, kartu ucapan eksklusif, hingga kemasan ramah lingkungan untuk pengiriman aman ke seluruh Indonesia. Diskusikan rencana Anda bersama konsultan kami via WhatsApp tanpa biaya konsultasi.
        </p>
      </div>

      <!-- Baca Juga Box 2 -->
      <div class="gs-article__baca-juga" data-gs-animate>
        <div class="gs-article__baca-juga-icon" aria-hidden="true">
          <svg viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="gs-article__baca-juga-content">
          <strong>Pelajari Juga:</strong> Simak inspirasi lengkap pada <a href="${conf.bacaJuga2.link}">${conf.bacaJuga2.title}</a>.
        </div>
      </div>
      `;
    }
  });

  // Build Related Articles Cards HTML
  const relatedCardsHtml = conf.related.map(r => `
    <article data-gs-animate class="gs-blog-card">
      <div class="gs-blog-card__image">
        <a href="/blog/${r.slug}" aria-label="Baca ${r.title}" style="display:block;width:100%;height:100%;">
          <img src="${r.img}" alt="${r.title}" loading="lazy" width="400" height="250" />
        </a>
      </div>
      <div class="gs-blog-card__body">
        <div class="gs-blog-card__meta">
          <span class="gs-blog-card__category">${r.cat}</span>
          <span aria-hidden="true">&bull;</span>
          <time datetime="${UPLOAD_TIME_SHORT}">${UPLOAD_DATE_STR}</time>
        </div>
        <h3 class="gs-blog-card__title">
          <a href="/blog/${r.slug}">${r.title}</a>
        </h3>
        <p class="gs-blog-card__excerpt">${r.excerpt}</p>
        <a href="/blog/${r.slug}" class="gs-blog-card__link">
          Baca Selengkapnya &rarr;
        </a>
      </div>
    </article>
  `).join('\n');

  // Key takeaways HTML
  const keyTakeawaysHtml = conf.keyTakeaways.map(k => `<li>${k}</li>`).join('\n                ');

  // Generate complete HTML string
  const fullHtml = `<!DOCTYPE html>
<html lang="id">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />

  <!-- Preload Critical CSS -->
  <link rel="preload" href="/assets/css/style.min.css?v=16" as="style" />

  <title>${art.metaTitle} | SEKATA Souvenir Pernikahan</title>
  <meta name="description" content="${art.metaDesc}" />
  <meta name="author" content="Yudi Abraham" />
  <meta name="language" content="Indonesian" />
  <meta name="theme-color" content="#762b16" />
  <meta name="format-detection" content="telephone=no" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />

  <!-- Favicon & App Icons -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/profile/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/profile/favicon-16x16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/profile/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />

  <!-- Canonical & Alternate Hreflang -->
  <link rel="canonical" href="${SITE_ORIGIN}/blog/${art.slug}" />
  <link rel="alternate" hreflang="id-ID" href="${SITE_ORIGIN}/blog/${art.slug}" />
  <link rel="alternate" hreflang="x-default" href="${SITE_ORIGIN}/blog/${art.slug}" />

  <!-- GEO & Local Engine Optimization (GEO) -->
  <meta name="geo.region" content="ID-JI" />
  <meta name="geo.placename" content="Kota Malang, Jawa Timur, Indonesia" />
  <meta name="geo.position" content="-7.9839;112.6214" />
  <meta name="ICBM" content="-7.9839, 112.6214" />
  <meta name="geo.country" content="ID" />

  <!-- Open Graph / Facebook / WhatsApp -->
  <meta property="og:site_name" content="SEKATA" />
  <meta property="og:type" content="article" />
  <meta property="og:locale" content="id_ID" />
  <meta property="og:url" content="${SITE_ORIGIN}/blog/${art.slug}" />
  <meta property="og:title" content="${art.metaTitle} | SEKATA" />
  <meta property="og:description" content="${art.metaDesc}" />
  <meta property="og:image" content="${SITE_ORIGIN}/assets/images/artikel/${art.slug}.webp" />
  <meta property="og:image:secure_url" content="${SITE_ORIGIN}/assets/images/artikel/${art.slug}.webp" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="${conf.heroAlt}" />
  <meta property="og:image:type" content="image/webp" />
  <meta property="article:published_time" content="${UPLOAD_DATE_ISO}" />
  <meta property="article:modified_time" content="${UPLOAD_DATE_ISO}" />
  <meta property="article:author" content="Yudi Abraham" />
  <meta property="article:section" content="${conf.category}" />
  <meta property="article:tag" content="Souvenir Pernikahan" />
  <meta property="article:tag" content="Wedding Favors" />
  <meta property="article:tag" content="Souvenir Pernikahan Unik" />
  <meta property="article:tag" content="Souvenir Pernikahan Malang" />

  <!-- Twitter / X Cards -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:url" content="${SITE_ORIGIN}/blog/${art.slug}" />
  <meta name="twitter:title" content="${art.metaTitle} | SEKATA" />
  <meta name="twitter:description" content="${art.metaDesc}" />
  <meta name="twitter:image" content="${SITE_ORIGIN}/assets/images/artikel/${art.slug}.webp" />
  <meta name="twitter:image:alt" content="${conf.heroAlt}" />

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
  <link rel="stylesheet" href="/assets/css/style.min.css?v=16" />

  <!-- Structured Data JSON-LD (BlogPosting, BreadcrumbList, ItemList, FAQPage) -->
  <script type="application/ld+json">
${JSON.stringify(structuredData, null, 2)}
  </script>
</head>

<body>

  <!-- NAVBAR -->
  <header>
    <nav class="gs-navbar" aria-label="Navigasi utama">
      <div class="gs-container">
        <div class="gs-navbar__inner">
          <a href="/" class="gs-navbar__logo" aria-label="Souvenir Pernikahan — Beranda">
            <img src="/assets/profile/logo-navbar-120.webp" alt="Logo SEKATA, souvenir pernikahan" class="gs-navbar__logo-img"
              width="60" height="60" decoding="async" />
            <span class="gs-navbar__brand-text">Souvenir Pernikahan</span>
          </a>
          <div class="gs-navbar__nav" role="menubar">
            <a href="/" class="gs-navbar__link" role="menuitem">Beranda</a>
            <a href="/tentang" class="gs-navbar__link" role="menuitem">Tentang</a>
            <!-- Dropdown Katalog -->
            <div class="gs-dropdown">
              <button class="gs-dropdown__toggle" aria-haspopup="true" aria-expanded="false"
                aria-controls="gs-dropdown-paket" id="gs-dropdown-paket-btn">
                Katalog
                <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round" aria-hidden="true">
                  <path d="M4 6l4 4 4-4" />
                </svg>
              </button>
              <div class="gs-dropdown__menu" id="gs-dropdown-paket" aria-labelledby="gs-dropdown-paket-btn">
                <a href="/paket" class="gs-dropdown__item">
                  <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path
                      d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM14 11a1 1 0 011 1v1h1a1 1 0 110 2h-1v1a1 1 0 11-2 0v-1h-1a1 1 0 110-2h1v-1a1 1 0 011-1z" />
                  </svg>
                  Katalog Souvenir
                </a>
                <div class="gs-dropdown__divider" role="separator"></div>
                <a href="/paket/souvenir-tradisional" class="gs-dropdown__item">
                  <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd"
                      d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
                      clip-rule="evenodd" />
                  </svg>
                  Essential Collection
                </a>
                <a href="/paket/souvenir-modern" class="gs-dropdown__item">
                  <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd"
                      d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2h-3a1 1 0 01-1-1v-2a1 1 0 00-1-1H9a1 1 0 00-1 1v2a1 1 0 01-1 1H4a1 1 0 110-2V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z"
                      clip-rule="evenodd" />
                  </svg>
                  Signature Collection
                </a>
              </div>
            </div>
            <a href="/portofolio" class="gs-navbar__link" role="menuitem">Portofolio</a>
            <a href="/blog" class="gs-navbar__link active" role="menuitem">Blog</a>
          </div>
          <div class="gs-navbar__cta">
            <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi%20souvenir%20pernikahan."
              class="gs-button gs-button--whatsapp gs-button--sm" target="_blank" rel="noopener noreferrer"
              aria-label="Konsultasi via WhatsApp">
              <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
              </svg>
              Konsultasi
            </a>
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
          <button class="gs-navbar__mobile-submenu-toggle" aria-expanded="false" aria-controls="gs-mobile-paket">
            Katalog
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" aria-hidden="true">
              <path d="M4 6l4 4 4-4" />
            </svg>
          </button>
          <div class="gs-navbar__mobile-submenu" id="gs-mobile-paket">
            <a href="/paket" class="gs-navbar__mobile-link">Katalog Souvenir</a>
            <a href="/paket/souvenir-tradisional" class="gs-navbar__mobile-link">Essential Collection</a>
            <a href="/paket/souvenir-modern" class="gs-navbar__mobile-link">Signature Collection</a>
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
    <section class="gs-section gs-article-section" style="padding-top: clamp(0.75rem, 1.5vw, 1.25rem);">
      <div class="gs-container">

        <article class="gs-article">

          <!-- Breadcrumb -->
          <nav aria-label="Breadcrumb">
            <ol class="gs-breadcrumb">
              <li><a href="/" class="gs-breadcrumb__item">Beranda</a></li>
              <li><a href="/blog" class="gs-breadcrumb__item">Blog</a></li>
              <li class="gs-breadcrumb__item gs-breadcrumb__item--active" aria-current="page">${art.title}</li>
            </ol>
          </nav>

          <!-- Header -->
          <header class="gs-article__header" data-gs-animate>
            <div class="gs-article__badge-wrap">
              <span class="gs-article__category">${conf.category}</span>
              <span class="gs-badge">${conf.topicTag}</span>
              <span class="gs-badge" style="background:var(--gs-green-100);color:var(--gs-green-800);border-color:var(--gs-green-300);">Bagian dari sakasouvenir.com</span>
            </div>
            <h1 class="gs-article__title">${art.title}</h1>
            <div class="gs-article__meta">
              <span class="gs-article__meta-item">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                </svg>
                <strong>Penulis:</strong> <a href="/penulis" class="gs-article__author-link" title="Lihat profil Yudi Abraham">Yudi Abraham</a>
              </span>
              <span class="gs-article__meta-item">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                    clip-rule="evenodd" />
                </svg>
                <strong>Publikasi:</strong> <time datetime="${UPLOAD_TIME_SHORT}">${UPLOAD_DATE_STR}</time>
              </span>
              <span class="gs-article__meta-item">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                    clip-rule="evenodd" />
                </svg>
                <strong>Pembaruan:</strong> <time datetime="${UPLOAD_TIME_SHORT}">${UPLOAD_DATE_STR}</time>
              </span>
              <span class="gs-article__meta-item">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                    clip-rule="evenodd" />
                </svg>
                <strong>Waktu Baca:</strong> ${conf.readTime}
              </span>
            </div>
          </header>

          <!-- Cover Image -->
          <div class="gs-article__cover" data-gs-animate="slide">
            <img src="/assets/images/artikel/${art.slug}.webp"
              alt="${conf.heroAlt}" width="1200" height="630"
              loading="eager" />
            <div class="gs-article__caption">
              ${conf.coverCaption}
            </div>
          </div>

          <!-- TOC (Daftar Isi) -->
          <nav data-gs-animate class="gs-article__toc" aria-label="Daftar Isi Artikel">
            <button type="button" class="gs-article__toc-toggle" aria-expanded="true" aria-controls="toc-list-body-${art.slug}">
              <span class="gs-article__toc-label">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1z"
                    clip-rule="evenodd" />
                </svg>
                Daftar Isi Pembahasan
              </span>
              <svg class="gs-article__toc-chevron" viewBox="0 0 16 16" fill="none" stroke="currentColor"
                stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M4 6l4 4 4-4" />
              </svg>
            </button>
            <div class="gs-article__toc-body" id="toc-list-body-${art.slug}">
              <ol class="gs-article__toc-list">
                ${tocItems}
              </ol>
            </div>
          </nav>

          <!-- Body Artikel -->
          <div class="gs-article__body">

            <!-- Lead Paragraph Pembuka Konteks -->
            <p class="gs-article__lead">
              ${art.lead}
            </p>

            <!-- Key Takeaways Box (AEO & GEO) -->
            <aside class="gs-article__key-takeaway" aria-labelledby="takeaway-${art.slug}">
              <div data-gs-animate class="gs-article__key-takeaway-head" id="takeaway-${art.slug}">
                <svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    clip-rule="evenodd" />
                </svg>
                Ringkasan Inti &amp; Jawaban Cepat (Key Takeaways)
              </div>
              <ul style="margin:0;padding-left:1.25rem;">
                ${keyTakeawaysHtml}
              </ul>
            </aside>

            <!-- Rendered Sections Content -->
            ${sectionsHtml}

            <!-- Rekomendasi Produk & Katalog Banner -->
            <div class="gs-article__product-rec" data-gs-animate>
              <div class="gs-article__product-rec-img">
                <img src="/assets/images/artikel/${art.slug}.webp"
                  alt="${art.title} koleksi resmi SEKATA" width="300"
                  height="300" loading="lazy" />
              </div>
              <div class="gs-article__product-rec-info">
                <span class="badge">Spesialis Souvenir Pernikahan</span>
                <h4>Wujudkan Souvenir Pernikahan Impian Anda Bersama SEKATA</h4>
                <p>SEKATA adalah unit spesialis souvenir pernikahan dari <strong><a href="https://sakasouvenir.com" target="_blank" rel="noopener noreferrer" style="color:var(--gs-green-800);text-decoration:underline;">Saka Souvenir</a></strong>. Dapatkan konsultasi desain gratis, visualisasi mockup nama pengantin, serta pengiriman aman bergaransi 100% ke seluruh Indonesia.</p>
                <div style="font-size:0.85rem;color:var(--gs-green-800);font-weight:600;">Workshop Resmi di Malang • Minimal Order Fleksibel • Garansi Bebas Risiko</div>
              </div>
              <div class="gs-article__product-rec-action">
                <a href="https://wa.me/6282131087971?text=Halo%20SEKATA%20Souvenir%20Pernikahan%2C%20saya%20tertarik%20konsultasi%20souvenir%20dari%20artikel%20${encodeURIComponent(art.title)}." class="gs-button gs-button--whatsapp gs-button--sm" target="_blank" rel="noopener noreferrer">Konsultasi WA</a>
                <a href="/paket" class="gs-button gs-button--primary gs-button--sm" style="margin-top:0.5rem;">Lihat Katalog</a>
              </div>
            </div>

            <!-- Author Box -->
            <div class="gs-article__author-box" data-gs-animate>
              <div class="gs-article__author-avatar">
                <img src="/assets/images/yudi-abraham.webp" alt="Yudi Abraham" width="80" height="80" loading="lazy" />
              </div>
              <div class="gs-article__author-info">
                <h4>Ditulis oleh <a href="/penulis">Yudi Abraham</a></h4>
                <p>Technology Writer &amp; Wedding Favors Specialist di SEKATA. Membagikan panduan praktis, riset material souvenir, dan inspirasi cinderamata bermakna bagi calon pengantin di seluruh Indonesia.</p>
              </div>
            </div>

            <!-- Bagikan Artikel -->
            <div class="gs-article__share" data-gs-animate>
              <span>Bagikan panduan ini:</span>
              <a href="https://api.whatsapp.com/send?text=${encodeURIComponent(art.title + ' ' + SITE_ORIGIN + '/blog/' + art.slug)}" target="_blank" rel="noopener noreferrer" class="gs-button gs-button--whatsapp gs-button--sm" aria-label="Bagikan ke WhatsApp">
                WhatsApp
              </a>
            </div>

          </div>

          <!-- Related Articles Grid -->
          <section class="gs-article__related" aria-labelledby="related-title-${art.slug}">
            <h2 class="gs-article__related-title" id="related-title-${art.slug}">Artikel Terkait dalam Seri Ini</h2>
            <div class="gs-article__related-grid">
              ${relatedCardsHtml}
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
          <a href="/" class="gs-footer__brand-name" aria-label="SEKATA – Beranda">
            <div class="gs-footer__brand-logo" aria-hidden="true"><img src="/assets/profile/logo-footer-108.webp"
                alt="Logo SEKATA" width="54" height="54" loading="lazy" decoding="async" /></div>
            <span>SEKATA</span>
          </a>
          <p class="gs-footer__desc">
            Unit spesialis souvenir pernikahan dari <strong><a href="https://sakasouvenir.com" target="_blank" rel="noopener noreferrer" style="color:inherit;text-decoration:underline;">Saka Souvenir</a></strong>. Menghadirkan cinderamata pernikahan custom elegan, berkelas, dan bernilai guna di Malang untuk pengiriman aman ke seluruh Indonesia.
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
          <p class="gs-footer__heading">Koleksi Souvenir</p>
          <ul class="gs-footer__links">
            <li><a href="/paket" class="gs-footer__link">Katalog Souvenir</a></li>
            <li><a href="/paket/souvenir-tradisional" class="gs-footer__link">Essential Collection</a></li>
            <li><a href="/paket/souvenir-modern" class="gs-footer__link">Signature Collection</a></li>
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
        <p>&copy; <span id="gs-year"></span> Souvenir Pernikahan (Bagian dari Saka Souvenir). Semua hak dilindungi.</p>
        <div class="gs-footer__bottom-links">
          <a href="/kebijakan-privasi" class="gs-footer__bottom-link">Kebijakan Privasi</a>
        </div>
      </div>
    </div>
  </footer>

  <div class="gs-whatsapp-float" aria-label="Hubungi via WhatsApp">
    <a href="https://wa.me/6282131087971?text=Halo%20Souvenir%20Pernikahan%2C%20saya%20ingin%20konsultasi%20souvenir."
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

  <script defer src="/assets/js/main.min.js?v=9"></script>
</body>

</html>
`;

  const outPath = path.join('blog', `${art.slug}.html`);
  fs.writeFileSync(outPath, fullHtml, 'utf-8');
  console.log(`Generated: ${outPath} (${fullHtml.length} bytes)`);
});

console.log("All 4 articles generated successfully!");
