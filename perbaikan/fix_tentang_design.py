# Fix encoding and design in tentang.html and other files

import os, re

def fix_all_encodings():
    files = [
        r'c:/Untuk_PKL/Souvenirkeuda/blog.html',
        r'c:/Untuk_PKL/Souvenirkeuda/kebijakan-privasi.html',
        r'c:/Untuk_PKL/Souvenirkeuda/tentang.html',
        r'c:/Untuk_PKL/Souvenirkeuda/blog/checklist-pemesanan-souvenir-pernikahan.html',
        r'c:/Untuk_PKL/Souvenirkeuda/blog/kipas-batik-untuk-souvenir-pernikahan.html',
        r'c:/Untuk_PKL/Souvenirkeuda/blog/panduan-souvenir-perusahaan.html',
        r'c:/Untuk_PKL/Souvenirkeuda/blog/pouch-batik-dan-dompet-tenun-untuk-souvenir.html',
        r'c:/Untuk_PKL/Souvenirkeuda/blog/souvenir-pernikahan-elegan-untuk-acara-intim.html',
        r'c:/Untuk_PKL/Souvenirkeuda/blog/souvenir-pernikahan-premium-untuk-tamu-vip.html',
        r'c:/Untuk_PKL/Souvenirkeuda/blog/souvenir-pernikahan-tradisional-khas-indonesia.html',
        r'c:/Untuk_PKL/Souvenirkeuda/blog/souvenir-pernikahan-unik-bermanfaat.html'
    ]
    for p in files:
        if not os.path.exists(p):
            continue
        with open(p, 'rb') as f:
            raw = f.read()
        fixed = raw.replace(b'\x97', '—'.encode('utf-8')).replace(b'\x96', '–'.encode('utf-8'))
        fixed = fixed.replace(b'\x91', '‘'.encode('utf-8')).replace(b'\x92', '’'.encode('utf-8'))
        fixed = fixed.replace(b'\x93', '“'.encode('utf-8')).replace(b'\x94', '”'.encode('utf-8'))
        fixed = fixed.replace(b'\x85', '…'.encode('utf-8'))
        try:
            fixed.decode('utf-8')
            with open(p, 'wb') as f:
                f.write(fixed)
            print(f'Successfully fixed encoding for: {p}')
        except Exception as e:
            print(f'Failed fixing {p}: {e}')

def fix_tentang_design():
    path = r'c:/Untuk_PKL/Souvenirkeuda/tentang.html'
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    # 1. Replace the card in workshop location
    old_card_pattern = re.compile(
        r'<div style="background:var\(--gs-green-50\);\s*border:1px solid var\(--gs-border\);\s*border-radius:var\(--gs-radius-md\);\s*padding:1\.75rem;\s*display:flex;\s*flex-direction:column;\s*gap:1rem;">.*?</div>\s*</div>\s*</div>\s*</section>',
        re.DOTALL
    )

    new_card_html = '''<div class="gs-workshop-card" style="background:linear-gradient(145deg, #ffffff 0%, var(--gs-green-50, #fbf6f3) 100%); border:1px solid rgba(178,80,50,0.18); border-radius:var(--gs-radius-lg, 1.25rem); padding:clamp(1.5rem, 2.5vw, 2rem); box-shadow:0 10px 30px -5px rgba(118,43,22,0.07); display:flex; flex-direction:column; gap:1.25rem;">
            <div style="display:flex; align-items:flex-start; gap:1rem; padding-bottom:1.15rem; border-bottom:1px solid rgba(230,222,213,0.7);">
              <div style="width:46px; height:46px; flex-shrink:0; border-radius:12px; background:linear-gradient(135deg, var(--gs-green-100), var(--gs-green-200)); border:1px solid rgba(178,80,50,0.22); display:flex; align-items:center; justify-content:center; color:var(--gs-green-900); box-shadow:0 3px 8px rgba(118,43,22,0.08);" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="20 12 20 22 4 22 4 12"></polyline>
                  <rect x="2" y="7" width="20" height="5"></rect>
                  <line x1="12" y1="22" x2="12" y2="7"></line>
                  <path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"></path>
                  <path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"></path>
                </svg>
              </div>
              <div style="flex:1;">
                <h4 style="margin:0 0 0.25rem 0; font-family:var(--gs-font-heading); font-size:1.02rem; font-weight:700; color:var(--gs-green-900); line-height:1.35;">Survei Sampel Fisik Nyaman</h4>
                <p style="margin:0; color:var(--gs-muted); font-size:0.86rem; line-height:1.55;">Tersedia puluhan display sampel asli souvenir pernikahan di galeri workshop kami.</p>
              </div>
            </div>

            <div style="display:flex; align-items:flex-start; gap:1rem; padding-bottom:1.15rem; border-bottom:1px solid rgba(230,222,213,0.7);">
              <div style="width:46px; height:46px; flex-shrink:0; border-radius:12px; background:linear-gradient(135deg, var(--gs-green-100), var(--gs-green-200)); border:1px solid rgba(178,80,50,0.22); display:flex; align-items:center; justify-content:center; color:var(--gs-green-900); box-shadow:0 3px 8px rgba(118,43,22,0.08);" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="1" y="3" width="15" height="13"></rect>
                  <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
                  <circle cx="5.5" cy="18.5" r="2.5"></circle>
                  <circle cx="18.5" cy="18.5" r="2.5"></circle>
                </svg>
              </div>
              <div style="flex:1;">
                <h4 style="margin:0 0 0.25rem 0; font-family:var(--gs-font-heading); font-size:1.02rem; font-weight:700; color:var(--gs-green-900); line-height:1.35;">Pemesanan Luar Kota Sangat Mudah</h4>
                <p style="margin:0; color:var(--gs-muted); font-size:0.86rem; line-height:1.55;">Untuk calon pengantin luar Malang, konsultasi desain &amp; pengiriman sampel dilakukan via WhatsApp &amp; kurir ekspedisi.</p>
              </div>
            </div>

            <div style="display:flex; align-items:flex-start; gap:1rem;">
              <div style="width:46px; height:46px; flex-shrink:0; border-radius:12px; background:linear-gradient(135deg, var(--gs-green-100), var(--gs-green-200)); border:1px solid rgba(178,80,50,0.22); display:flex; align-items:center; justify-content:center; color:var(--gs-green-900); box-shadow:0 3px 8px rgba(118,43,22,0.08);" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                  <path d="M9 12l2 2 4-4"></path>
                </svg>
              </div>
              <div style="flex:1;">
                <h4 style="margin:0 0 0.25rem 0; font-family:var(--gs-font-heading); font-size:1.02rem; font-weight:700; color:var(--gs-green-900); line-height:1.35;">Garansi Kirim Bebas Risiko</h4>
                <p style="margin:0; color:var(--gs-muted); font-size:0.86rem; line-height:1.55;">Pengiriman ke seluruh kota diproteksi garansi 100% ganti baru jika terjadi kerusakan.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>'''

    if old_card_pattern.search(html):
        html = old_card_pattern.sub(new_card_html, html)
        print("Replaced workshop card successfully!")
    else:
        print("Workshop card pattern NOT matched! Checking manual replacement...")
        start_idx = html.find('Survei Sampel Fisik Nyaman')
        if start_idx != -1:
            div_start = html.rfind('<div style="background:var(--gs-green-50);', 0, start_idx)
            sec_end = html.find('</section>', start_idx)
            if div_start != -1 and sec_end != -1:
                html = html[:div_start] + new_card_html + html[sec_end + len('</section>'):]
                print("Manual replacement done!")

    # 2. Replace corrupted checkmarks in lists
    old_check = '<span style="color:var(--gs-green-700);">?</span>'
    new_check = '<svg viewBox="0 0 20 20" fill="currentColor" style="width:16px;height:16px;color:var(--gs-green-700);flex-shrink:0;" aria-hidden="true"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>'
    if old_check in html:
        count = html.count(old_check)
        html = html.replace(old_check, new_check)
        print(f"Replaced {count} broken checkmarks with SVG checkmark icons!")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("tentang.html successfully updated and saved as UTF-8!")

if __name__ == '__main__':
    fix_all_encodings()
    fix_tentang_design()

