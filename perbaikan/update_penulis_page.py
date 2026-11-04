# -*- coding: utf-8 -*-
"""
Script to update penulis.html to make Yudi Abraham's profile 100% relevant,
authoritative, and aligned with wedding souvenirs (E-E-A-T).
"""

import json
import re

with open('penulis.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Schema JSON-LD
schema_pattern = re.compile(r'<script type="application/ld\+json">([\s\S]*?)</script>')
m = schema_pattern.search(content)
if m:
    data = json.loads(m.group(1))
    for obj in data.get('@graph', []):
        if obj.get('@type') == 'Person':
            obj['jobTitle'] = 'Founder & Creative Lead'
            obj['description'] = 'Founder dan kurator kreatif Souvenir Pernikahan yang berdedikasi mendampingi calon pengantin menemukan cinderamata pernikahan unik, elegan, bernilai kriya budaya nusantara, serta kemasan berkelas.'
            obj['knowsAbout'] = [
                'Souvenir Pernikahan',
                'Souvenir Pernikahan Tradisional',
                'Souvenir Pernikahan Modern',
                'Hampers Pernikahan',
                'Kriya Nusantara & Kerajinan Lokal',
                'Cinderamata Akad Nikah',
                'Desain Kemasan Wedding Eksklusif',
                'Personalisasi Grafir Laser Monogram',
                'Wedding Favors Indonesia',
                'Manajemen Budget Souvenir Pernikahan'
            ]
        elif obj.get('@type') == 'ProfilePage':
            obj['description'] = 'Profil biografi Yudi Abraham, Founder & Creative Lead di Souvenir Pernikahan. Berpengalaman dalam kurasi cinderamata pernikahan kriya nusantara dan souvenir modern personal.'
    
    new_schema_str = json.dumps(data, indent=2, ensure_ascii=False)
    content = content[:m.start()] + f'<script type="application/ld+json">\n{new_schema_str}\n  </script>' + content[m.end():]
    print("Updated schema in penulis.html")

# 2. Update Role Badge & Subtitle
content = re.sub(
    r'<span class="gs-author-role-badge">Penulis Artikel</span>',
    '<span class="gs-author-role-badge">Founder &amp; Creative Lead</span>',
    content
)
content = re.sub(
    r'<p class="gs-author-subtitle">Penulis &amp; Web Development Enthusiast</p>',
    '<p class="gs-author-subtitle">Founder &amp; Kurator Kreatif Souvenir Pernikahan</p>',
    content
)

# 3. Update Author Bio
old_bio = '<p class="gs-author-bio">\n                  Penulis konten edukatif dan panduan praktis seputar souvenir pernikahan, tips cinderamata acara,\n                  inspirasi kemasan elegan, serta integrasi teknologi web di Souvenir Pernikahan.\n                </p>'
new_bio = '''<p class="gs-author-bio">
                  Founder dan kurator kreatif di Souvenir Pernikahan yang berdedikasi membantu calon pengantin menemukan
                  cinderamata pernikahan yang unik, elegan, bernilai guna tinggi, serta sarat filosofi budaya nusantara.
                  Berpengalaman dalam kurasi kerajinan kriya lokal, personalisasi grafir nama mempelai, dan standarisasi
                  pengemasan bergaransi aman ke seluruh Indonesia.
                </p>'''

if old_bio in content:
    content = content.replace(old_bio, new_bio)
else:
    content = re.sub(
        r'<p class="gs-author-bio">[\s\S]*?</p>',
        new_bio,
        content,
        count=1
    )
print("Updated author bio")

# 4. Update Tag Pills
old_tags = '''<div class="gs-author-tags-list">
                  <span class="gs-author-tag-pill">Souvenir Pernikahan</span>
                  <span class="gs-author-tag-pill">Tips Acara &amp; Event</span>
                  <span class="gs-author-tag-pill">Kemasan &amp; Desain</span>
                  <span class="gs-author-tag-pill">Web Development</span>
                </div>'''

new_tags = '''<div class="gs-author-tags-list">
                  <span class="gs-author-tag-pill">Souvenir Pernikahan</span>
                  <span class="gs-author-tag-pill">Kriya Nusantara</span>
                  <span class="gs-author-tag-pill">Kemasan Eksklusif</span>
                  <span class="gs-author-tag-pill">Hampers Wedding VIP</span>
                  <span class="gs-author-tag-pill">Personalisasi Grafir</span>
                </div>'''

if old_tags in content:
    content = content.replace(old_tags, new_tags)
else:
    content = re.sub(
        r'<div class="gs-author-tags-list">[\s\S]*?</div>',
        new_tags,
        content,
        count=1
    )
print("Updated tag pills")

# 5. Update Tentang Penulis section text
tentang_pattern = re.compile(r'(<h3 class="gs-author-card__title" id="about-author-heading">[\s\S]*?</h3>\s*)<p class="gs-author-text">[\s\S]*?</p>')
new_tentang_text = '''<p class="gs-author-text">
                Yudi Abraham merupakan Founder sekaligus Creative Lead di Souvenir Pernikahan yang berfokus mendampingi
                calon mempelai dalam merancang cinderamata pernikahan impian. Menggabungkan ketelitian estetika desain,
                apresiasi mendalam terhadap pengrajin kriya lokal (batik tulis, tenun lurik, dan keramik tembikar), serta
                sistem pemesanan yang transparan, ia berdedikasi menghadirkan panduan komprehensif mulai dari estimasi anggaran,
                pemilihan bahan ramah lingkungan, hingga proteksi logistik kargo aman ke berbagai kota di Indonesia.
              </p>'''

if tentang_pattern.search(content):
    content = tentang_pattern.sub(r'\1' + new_tentang_text, content)
    print("Updated Tentang Penulis text")

# 6. Update Skills Section (Keahlian dan Fokus)
skills_grid_pattern = re.compile(r'<div class="gs-skills-grid">[\s\S]*?</div>\s*</section>')
new_skills_grid = '''<div class="gs-skills-grid">
                <!-- Skill 1 -->
                <div class="gs-skill-item">
                  <div class="gs-skill-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"
                      stroke-linejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  </div>
                  <div class="gs-skill-content">
                    <h4 class="gs-skill-title">Kurasi Souvenir Pernikahan</h4>
                    <p class="gs-skill-desc">Souvenir tradisional, modern fungsional, dan hampers VIP</p>
                  </div>
                </div>

                <!-- Skill 2 -->
                <div class="gs-skill-item">
                  <div class="gs-skill-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"
                      stroke-linejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  </div>
                  <div class="gs-skill-content">
                    <h4 class="gs-skill-title">Personalisasi &amp; Grafir</h4>
                    <p class="gs-skill-desc">Laser engrave inisial, hotprint emas, dan monogram</p>
                  </div>
                </div>

                <!-- Skill 3 -->
                <div class="gs-skill-item">
                  <div class="gs-skill-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"
                      stroke-linejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  </div>
                  <div class="gs-skill-content">
                    <h4 class="gs-skill-title">Kriya Pengrajin Lokal</h4>
                    <p class="gs-skill-desc">Batik tulis jati, tenun lurik ATBM, dan stoneware</p>
                  </div>
                </div>

                <!-- Skill 4 -->
                <div class="gs-skill-item">
                  <div class="gs-skill-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"
                      stroke-linejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  </div>
                  <div class="gs-skill-content">
                    <h4 class="gs-skill-title">Packaging &amp; Kemasan</h4>
                    <p class="gs-skill-desc">Hardbox magnetik, pouch beludru, dan besek rustic</p>
                  </div>
                </div>

                <!-- Skill 5 -->
                <div class="gs-skill-item">
                  <div class="gs-skill-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"
                      stroke-linejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  </div>
                  <div class="gs-skill-content">
                    <h4 class="gs-skill-title">Manajemen Budget</h4>
                    <p class="gs-skill-desc">Simulasi anggaran hemat Rp 15rb hingga hampers mewah</p>
                  </div>
                </div>

                <!-- Skill 6 -->
                <div class="gs-skill-item">
                  <div class="gs-skill-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round"
                      stroke-linejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  </div>
                  <div class="gs-skill-content">
                    <h4 class="gs-skill-title">Logistik &amp; Quality Control</h4>
                    <p class="gs-skill-desc">Standar 4 lapis packing &amp; garansi 100% ganti baru</p>
                  </div>
                </div>
              </div>
            </section>'''

if skills_grid_pattern.search(content):
    content = skills_grid_pattern.sub(new_skills_grid, content)
    print("Updated Skills Section in penulis.html")

with open('penulis.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished updating penulis.html!")

