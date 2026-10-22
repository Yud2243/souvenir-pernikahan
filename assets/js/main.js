/**
 * Souvenir Pernikahan — main.js
 * JavaScript vanilla untuk: navbar, dropdown, mobile menu, accordion, filter katalog
 */

(function () {
  'use strict';

  /* ============================================================
     NAVBAR: Hamburger & Mobile Menu
     ============================================================ */
  const hamburger = document.getElementById('gs-hamburger');
  const mobileMenu = document.getElementById('gs-mobile-menu');

  if (hamburger && mobileMenu) {
    function setMobileMenu(isOpen) {
      hamburger.setAttribute('aria-expanded', String(isOpen));
      hamburger.setAttribute('aria-label', isOpen ? 'Tutup menu navigasi' : 'Buka menu navigasi');
      mobileMenu.classList.toggle('is-open', isOpen);
      mobileMenu.setAttribute('aria-hidden', String(!isOpen));
    }

    hamburger.addEventListener('click', function () {
      const isOpen = this.getAttribute('aria-expanded') === 'true';
      setMobileMenu(!isOpen);
    });

    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        setMobileMenu(false);
      }
    });

    // Close when clicking outside
    document.addEventListener('click', function (e) {
      if (!hamburger.contains(e.target) && !mobileMenu.contains(e.target)) {
        setMobileMenu(false);
      }
    });

    // Close when a nav link is clicked
    mobileMenu.querySelectorAll('.gs-navbar__mobile-link').forEach(function (link) {
      link.addEventListener('click', function () {
        setMobileMenu(false);
      });
    });
  }

  /* ============================================================
     MOBILE SUBMENU TOGGLE
     ============================================================ */
  const mobileSubmenuToggles = document.querySelectorAll('.gs-navbar__mobile-submenu-toggle');
  mobileSubmenuToggles.forEach(function (toggle) {
    toggle.addEventListener('click', function () {
      const controlsId = this.getAttribute('aria-controls');
      const submenu = document.getElementById(controlsId);
      if (!submenu) return;
      const expanded = this.getAttribute('aria-expanded') === 'true';
      this.setAttribute('aria-expanded', String(!expanded));
      submenu.classList.toggle('is-open');
    });
  });

  /* ============================================================
     DESKTOP DROPDOWN
     ============================================================ */
  const dropdowns = document.querySelectorAll('.gs-dropdown');
  dropdowns.forEach(function (dropdown) {
    const toggle = dropdown.querySelector('.gs-dropdown__toggle');
    const menu = dropdown.querySelector('.gs-dropdown__menu');
    if (!toggle || !menu) return;

    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      const expanded = this.getAttribute('aria-expanded') === 'true';
      // Close all other dropdowns
      closeAllDropdowns(dropdown);
      this.setAttribute('aria-expanded', String(!expanded));
      menu.classList.toggle('is-open');
    });

    dropdown.addEventListener('mouseenter', function () {
      if (window.innerWidth >= 992) {
        toggle.setAttribute('aria-expanded', 'true');
      }
    });

    dropdown.addEventListener('mouseleave', function () {
      if (window.innerWidth >= 992) {
        toggle.setAttribute('aria-expanded', 'false');
        menu.classList.remove('is-open');
      }
    });

    // Keyboard navigation
    toggle.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        menu.classList.add('is-open');
        toggle.setAttribute('aria-expanded', 'true');
        const firstItem = menu.querySelector('.gs-dropdown__item');
        if (firstItem) firstItem.focus();
      }
    });

    menu.querySelectorAll('.gs-dropdown__item').forEach(function (item, idx, items) {
      item.addEventListener('click', function () {
        closeAllDropdowns();
      });

      item.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          const next = items[idx + 1];
          if (next) next.focus();
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          const prev = items[idx - 1];
          if (prev) prev.focus();
          else toggle.focus();
        } else if (e.key === 'Escape') {
          closeAllDropdowns();
          toggle.focus();
        } else if (e.key === 'Tab') {
          closeAllDropdowns();
        }
      });
    });
  });

  function closeAllDropdowns(exceptDropdown) {
    dropdowns.forEach(function (dd) {
      if (dd === exceptDropdown) return;
      const t = dd.querySelector('.gs-dropdown__toggle');
      const m = dd.querySelector('.gs-dropdown__menu');
      if (t) t.setAttribute('aria-expanded', 'false');
      if (m) m.classList.remove('is-open');
    });
  }

  // Close dropdown when clicking outside
  document.addEventListener('click', function () {
    closeAllDropdowns();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAllDropdowns();
  });

  /* ============================================================
     FAQ ACCORDION
     ============================================================ */
  const accordionTriggers = document.querySelectorAll('.gs-accordion__trigger');
  accordionTriggers.forEach(function (trigger) {
    trigger.addEventListener('click', function () {
      const panelId = this.getAttribute('aria-controls');
      const panel = document.getElementById(panelId);
      if (!panel) return;
      const expanded = this.getAttribute('aria-expanded') === 'true';

      // Close siblings
      const accordion = this.closest('.gs-accordion');
      if (accordion) {
        accordion.querySelectorAll('.gs-accordion__trigger').forEach(function (t) {
          if (t !== trigger) {
            t.setAttribute('aria-expanded', 'false');
            const pId = t.getAttribute('aria-controls');
            const p = document.getElementById(pId);
            if (p) p.classList.remove('is-open');
          }
        });
      }

      this.setAttribute('aria-expanded', String(!expanded));
      panel.classList.toggle('is-open');
    });
  });

  /* ============================================================
     FILTER TABS (katalog / portofolio)
     ============================================================ */
  /* ============================================================
     KATALOG FILTER & LIHAT SELENGKAPNYA (paket/index.html)
     ============================================================ */
  const paketGrid = document.getElementById('gs-paket-grid');
  const paketFilterTabs = document.querySelectorAll('.gs-filter-tabs .gs-filter-tab');
  const loadMoreBtn = document.getElementById('gs-load-more-btn');
  const loadMoreWrap = document.getElementById('gs-load-more-wrap');

  if (paketGrid && paketFilterTabs.length) {
    const INITIAL_LIMIT = 6;
    let isExpanded = false;
    let currentFilter = 'semua';

    function updatePaketDisplay() {
      const cards = paketGrid.querySelectorAll('.gs-card[data-category]');
      let matchingCards = [];

      cards.forEach(function (card) {
        const cat = card.dataset.category;
        if (currentFilter === 'semua' || cat === currentFilter) {
          matchingCards.push(card);
        } else {
          card.style.display = 'none';
        }
      });

      if (currentFilter === 'semua') {
        if (!isExpanded && matchingCards.length > INITIAL_LIMIT) {
          matchingCards.forEach(function (card, index) {
            if (index < INITIAL_LIMIT) {
              card.style.display = '';
            } else {
              card.style.display = 'none';
            }
          });
          if (loadMoreWrap && loadMoreBtn) {
            loadMoreWrap.style.display = 'block';
            loadMoreBtn.innerHTML = `Lihat Selengkapnya (${matchingCards.length - INITIAL_LIMIT} Produk Lainnya) <svg viewBox="0 0 20 20" fill="currentColor" style="width:18px;height:18px;"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>`;
          }
        } else {
          matchingCards.forEach(function (card) {
            card.style.display = '';
          });
          if (loadMoreWrap && loadMoreBtn) {
            if (matchingCards.length > INITIAL_LIMIT) {
              loadMoreWrap.style.display = 'block';
              loadMoreBtn.innerHTML = `Tampilkan Lebih Sedikit <svg viewBox="0 0 20 20" fill="currentColor" style="width:18px;height:18px;transform:rotate(180deg);"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>`;
            } else {
              loadMoreWrap.style.display = 'none';
            }
          }
        }
      } else {
        // Kategori spesifik (Pernikahan / Perusahaan)
        matchingCards.forEach(function (card) {
          card.style.display = '';
        });
        if (loadMoreWrap) {
          loadMoreWrap.style.display = 'none';
        }
      }

      // Empty state
      const emptyState = document.getElementById('gs-empty-state');
      if (emptyState) {
        emptyState.style.display = matchingCards.length === 0 ? 'block' : 'none';
      }
    }

    if (loadMoreBtn) {
      loadMoreBtn.addEventListener('click', function () {
        isExpanded = !isExpanded;
        updatePaketDisplay();
        if (!isExpanded && paketGrid) {
          paketGrid.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    }

    paketFilterTabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        currentFilter = this.dataset.filter;
        isExpanded = false;

        paketFilterTabs.forEach(function (t) {
          t.classList.remove('active');
          t.setAttribute('aria-pressed', 'false');
        });
        this.classList.add('active');
        this.setAttribute('aria-pressed', 'true');

        updatePaketDisplay();
      });
    });

    updatePaketDisplay();
  } else {
    // Fallback filter tabs untuk portofolio atau halaman lain
    const otherFilterTabs = document.querySelectorAll('.gs-filter-tab');
    if (otherFilterTabs.length) {
      otherFilterTabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
          const filter = this.dataset.filter;
          otherFilterTabs.forEach(function (t) { t.classList.remove('active'); });
          this.classList.add('active');

          const cards = document.querySelectorAll('[data-category]');
          let visibleCount = 0;
          cards.forEach(function (card) {
            const cat = card.dataset.category;
            if (filter === 'semua' || cat === filter) {
              card.style.display = '';
              visibleCount++;
            } else {
              card.style.display = 'none';
            }
          });
        });
      });
    }
  }

  /* ============================================================
     ACTIVE NAV LINK (Robust Path Normalization)
     ============================================================ */
  function normalizeNavPath(rawPath) {
    if (!rawPath) return '/';
    let p = rawPath.replace(/\\/g, '/');
    try {
      const u = new URL(p, window.location.href);
      p = u.pathname;
    } catch (e) {}
    p = p.toLowerCase().replace(/\/index\.html$/i, '/').replace(/\/+$/, '');
    return p || '/';
  }

  const currentNorm = normalizeNavPath(window.location.pathname);
  const isBlogSection = currentNorm.endsWith('/blog') || currentNorm.includes('/blog/');
  const isPaketSection = currentNorm.endsWith('/paket') || currentNorm.includes('/paket/');

  // Remove existing active states first
  const allNavLinks = document.querySelectorAll(
    '.gs-navbar__link, .gs-navbar__mobile-link, .gs-dropdown__item, .gs-dropdown__toggle'
  );
  allNavLinks.forEach(function (el) {
    el.classList.remove('active');
    if (el.hasAttribute('aria-current')) {
      el.removeAttribute('aria-current');
    }
  });

  allNavLinks.forEach(function (link) {
    const href = link.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;

    const linkNorm = normalizeNavPath(link.pathname || href);

    let isActive = false;

    if (currentNorm === '/' || currentNorm.endsWith('/souvenirkeuda') || currentNorm.endsWith('/souvenirkeuda/')) {
      if (linkNorm === '/' || linkNorm.endsWith('/souvenirkeuda') || linkNorm.endsWith('/index.html')) isActive = true;
    } else if (isBlogSection) {
      if (linkNorm === currentNorm || (linkNorm.endsWith('/blog') && (currentNorm.endsWith('/blog') || currentNorm.includes('/blog/index')))) {
        isActive = true;
      }
    } else if (isPaketSection) {
      if (linkNorm === currentNorm) isActive = true;
      if (linkNorm.endsWith('/paket') && (currentNorm.endsWith('/paket') || currentNorm.includes('/paket/index'))) {
        isActive = true;
      }
    } else {
      if (linkNorm === currentNorm) isActive = true;
    }

    if (isActive) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
    }
  });

  // Highlight parent dropdown button if on any paket page
  if (isPaketSection) {
    const paketToggle = document.getElementById('gs-dropdown-paket-btn');
    if (paketToggle) paketToggle.classList.add('active');
    const mobilePaketToggle = document.querySelector('.gs-navbar__mobile-submenu-toggle[aria-controls="gs-mobile-paket"]');
    if (mobilePaketToggle) mobilePaketToggle.classList.add('active');
  }

  /* ============================================================
     PACKAGE GALLERY THUMBNAILS (detail paket)
     ============================================================ */
  const thumbs = document.querySelectorAll('.gs-paket-gallery__thumb');
  const mainImg = document.querySelector('.gs-paket-gallery__main img');
  if (thumbs.length && mainImg) {
    thumbs.forEach(function (thumb) {
      thumb.addEventListener('click', function () {
        thumbs.forEach(function (t) { t.classList.remove('active'); });
        this.classList.add('active');
        const src = this.querySelector('img')?.src;
        const alt = this.querySelector('img')?.alt;
        if (src) mainImg.src = src;
        if (alt) mainImg.alt = alt;
      });

      thumb.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          this.click();
        }
      });

      thumb.setAttribute('tabindex', '0');
    });
  }

  /* ============================================================
     YEAR IN FOOTER
     ============================================================ */
  const yearEl = document.getElementById('gs-year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();


  /* ============================================================
     PRODUCT DETAIL MODAL
     ============================================================ */
  const modalOverlay = document.getElementById('gs-product-modal');
  if (modalOverlay) {
    const modalClose = modalOverlay.querySelector('.gs-modal__close');
    const modalImg   = modalOverlay.querySelector('#gs-modal-img');
    const modalBadge = modalOverlay.querySelector('#gs-modal-badge');
    const modalTitle = modalOverlay.querySelector('#gs-modal-title');
    const modalDesc  = modalOverlay.querySelector('#gs-modal-desc');
    const modalFeats = modalOverlay.querySelector('#gs-modal-features');
    const modalWaBtn = modalOverlay.querySelector('#gs-modal-wa-btn');
    let lastFocusedTrigger = null;

    function openModal(data, triggerBtn) {
      lastFocusedTrigger = triggerBtn || document.activeElement;

      if (modalImg) {
        if (data.image) {
          modalImg.src = data.image;
          modalImg.alt = data.title ? 'Foto produk ' + data.title : 'Foto produk souvenir';
          modalImg.style.display = 'block';
        } else {
          modalImg.removeAttribute('src');
          modalImg.alt = '';
          modalImg.style.display = 'none';
        }
      }
      if (modalBadge) modalBadge.textContent = data.badge || '';
      if (modalTitle) modalTitle.textContent = data.title || '';
      if (modalDesc)  modalDesc.textContent  = data.desc  || '';
      if (modalFeats) {
        modalFeats.innerHTML = '';
        (data.features || []).forEach(function (f) {
          var li = document.createElement('li');
          li.textContent = f;
          modalFeats.appendChild(li);
        });
      }
      if (modalWaBtn && data.waText) {
        modalWaBtn.href = 'https://wa.me/6285810025485?text=' + encodeURIComponent(data.waText);
      }
      modalOverlay.classList.add('is-open');
      document.body.style.overflow = 'hidden';

      // Move focus into dialog
      setTimeout(function () {
        if (modalClose) modalClose.focus();
      }, 50);
    }

    function closeModal() {
      modalOverlay.classList.remove('is-open');
      document.body.style.overflow = '';

      // Return focus to trigger button
      if (lastFocusedTrigger && typeof lastFocusedTrigger.focus === 'function') {
        lastFocusedTrigger.focus();
      }
    }

    if (modalClose) modalClose.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', function (e) {
      if (e.target === modalOverlay) closeModal();
    });

    // Close on Escape & trap focus inside modal
    document.addEventListener('keydown', function (e) {
      if (!modalOverlay.classList.contains('is-open')) return;

      if (e.key === 'Escape') {
        closeModal();
        return;
      }

      if (e.key === 'Tab') {
        const focusables = modalOverlay.querySelectorAll(
          'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );
        if (!focusables.length) return;
        const first = focusables[0];
        const last = focusables[focusables.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === first) {
            e.preventDefault();
            last.focus();
          }
        } else {
          if (document.activeElement === last) {
            e.preventDefault();
            first.focus();
          }
        }
      }
    });

    // Bind trigger buttons
    document.querySelectorAll('[data-modal-trigger]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var card = this.closest('[data-product]');
        if (!card) return;
        openModal({
          image:    card.dataset.productImage   || '',
          badge:    card.dataset.productBadge   || '',
          title:    card.dataset.productTitle   || '',
          desc:     card.dataset.productDesc    || '',
          features: JSON.parse(card.dataset.productFeatures || '[]'),
          waText:   card.dataset.productWa      || 'Halo Green\u2019s Souvenir, saya ingin konsultasi produk.'
        }, this);
      });
    });
  }

  /* ============================================================
     ARTICLE: TABLE OF CONTENTS (TOC) TOGGLE
     ============================================================ */
  const tocWidgets = document.querySelectorAll('.gs-article__toc');
  tocWidgets.forEach(function (toc) {
    const toggleBtn = toc.querySelector('.gs-article__toc-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', function () {
        toc.classList.toggle('is-collapsed');
        const isCollapsed = toc.classList.contains('is-collapsed');
        toggleBtn.setAttribute('aria-expanded', String(!isCollapsed));
      });
    }
  });

  /* ============================================================
     ARTICLE: FAQ ACCORDION
     ============================================================ */
  const articleFaqQuestions = document.querySelectorAll('.gs-article__faq-question');
  articleFaqQuestions.forEach(function (btn) {
    btn.addEventListener('click', function () {
      const isExpanded = this.getAttribute('aria-expanded') === 'true';
      const answer = this.nextElementSibling;
      if (!answer) return;

      this.setAttribute('aria-expanded', String(!isExpanded));
      answer.classList.toggle('is-open');
    });
  });

  /* ============================================================
     ARTICLE: SHARE BUTTONS & COPY LINK
     ============================================================ */
  const copyBtns = document.querySelectorAll('.gs-article__share-btn--copy');
  copyBtns.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const url = window.location.href;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () {
          showCopyFeedback(btn);
        }).catch(function () {
          fallbackCopyText(url, btn);
        });
      } else {
        fallbackCopyText(url, btn);
      }
    });
  });

  function showCopyFeedback(btn) {
    const originalTitle = btn.getAttribute('title') || 'Salin Tautan';
    btn.setAttribute('title', 'Tautan berhasil disalin!');
    btn.style.borderColor = 'var(--gs-green-700)';
    btn.style.color = 'var(--gs-green-700)';
    setTimeout(function () {
      btn.setAttribute('title', originalTitle);
      btn.style.borderColor = '';
      btn.style.color = '';
    }, 2000);
  }

  function fallbackCopyText(text, btn) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand('copy');
      showCopyFeedback(btn);
    } catch (err) {
      console.warn('Copy failed:', err);
    }
    document.body.removeChild(textarea);
  }

  /* ============================================================
     BLOG LISTING: SEARCH & CATEGORY FILTER
     ============================================================ */
  const blogSearchInput  = document.getElementById('gs-blog-search-input');
  const blogFilterTabs   = document.querySelectorAll('.gs-blog-filter-tab');
  const blogCards        = document.querySelectorAll('.gs-blog-card-item');
  const blogEmptyState   = document.getElementById('gs-blog-empty-state');
  const blogCountEl      = document.getElementById('gs-blog-count');
  const blogLoadMoreBtn  = document.getElementById('gs-blog-load-more-btn');
  const blogLoadMoreWrap = document.getElementById('gs-blog-load-more-wrap');

  if (blogCards.length && (blogSearchInput || blogFilterTabs.length)) {
    let currentCategory = 'semua';
    let searchQuery = '';
    let mobileExpanded = false;
    const mobileMedia = window.matchMedia('(max-width: 767px)');

    function filterBlogCards() {
      const isMobile = mobileMedia.matches;
      let matchCount = 0;
      const q = searchQuery.toLowerCase().trim();

      blogCards.forEach(function (card) {
        const cat = (card.dataset.category || '').toLowerCase();
        const title = (card.querySelector('.gs-blog-card__title')?.textContent || '').toLowerCase();
        const excerpt = (card.querySelector('.gs-blog-card__excerpt')?.textContent || '').toLowerCase();

        const matchesCat = (currentCategory === 'semua' || cat === currentCategory);
        const matchesSearch = !q || title.includes(q) || excerpt.includes(q) || cat.includes(q);

        if (matchesCat && matchesSearch) {
          matchCount++;
          if (isMobile && !mobileExpanded && matchCount > 3) {
            card.style.display = 'none';
          } else {
            card.style.display = '';
          }
        } else {
          card.style.display = 'none';
        }
      });

      if (blogEmptyState) {
        blogEmptyState.style.display = matchCount === 0 ? 'block' : 'none';
      }
      if (blogCountEl) {
        blogCountEl.textContent = 'Menampilkan ' + matchCount + ' artikel';
      }
      if (blogLoadMoreWrap) {
        if (isMobile && !mobileExpanded && matchCount > 3) {
          blogLoadMoreWrap.style.display = 'block';
        } else {
          blogLoadMoreWrap.style.display = 'none';
        }
      }
    }

    if (blogLoadMoreBtn) {
      blogLoadMoreBtn.addEventListener('click', function () {
        mobileExpanded = true;
        filterBlogCards();
      });
    }

    if (blogSearchInput) {
      blogSearchInput.addEventListener('input', function () {
        searchQuery = this.value;
        mobileExpanded = false;
        filterBlogCards();
      });
    }

    blogFilterTabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        blogFilterTabs.forEach(function (t) { t.classList.remove('active'); });
        this.classList.add('active');
        currentCategory = (this.dataset.filter || 'semua').toLowerCase();
        mobileExpanded = false;
        filterBlogCards();
      });
    });

    if (mobileMedia && typeof mobileMedia.addEventListener === 'function') {
      mobileMedia.addEventListener('change', filterBlogCards);
    }

    // Run initial filter
    filterBlogCards();
  }

  /* ============================================================
     ANIMATED CONTENT — Scroll Reveal (React Bits inspired)
     Watches [data-gs-animate] elements and adds .is-visible
     when they enter the viewport via IntersectionObserver.
     ============================================================ */
  if ('IntersectionObserver' in window) {
    var animateObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          animateObserver.unobserve(entry.target); // animate once
        }
      });
    }, {
      threshold: 0.12,
      rootMargin: '0px 0px -40px 0px'
    });

    document.querySelectorAll('[data-gs-animate]').forEach(function (el) {
      animateObserver.observe(el);
    });
  } else {
    // Fallback: show all immediately if observer not supported
    document.querySelectorAll('[data-gs-animate]').forEach(function (el) {
      el.classList.add('is-visible');
    });
  }

  /* ============================================================
     OPTIMIZED SCROLL HANDLER (Navbar Shadow & Back-to-Top Button)
     Batched via requestAnimationFrame to eliminate Forced Reflow
     ============================================================ */
  const navbar = document.querySelector('.gs-navbar');
  let backToTopBtn = document.getElementById('gs-back-to-top');
  if (!backToTopBtn) {
    backToTopBtn = document.createElement('button');
    backToTopBtn.id = 'gs-back-to-top';
    backToTopBtn.className = 'gs-back-to-top';
    backToTopBtn.setAttribute('type', 'button');
    backToTopBtn.setAttribute('aria-label', 'Kembali ke atas');
    backToTopBtn.innerHTML = '<svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" /></svg>';
    document.body.appendChild(backToTopBtn);
  }

  backToTopBtn.addEventListener('click', function () {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  let scrollTicking = false;
  function updateScrollState() {
    scrollTicking = false;
    const y = window.scrollY || window.pageYOffset || 0;
    if (navbar) {
      if (y > 10) {
        navbar.classList.add('is-scrolled');
      } else {
        navbar.classList.remove('is-scrolled');
      }
    }
    if (backToTopBtn) {
      if (y > 300) {
        backToTopBtn.classList.add('is-visible');
      } else {
        backToTopBtn.classList.remove('is-visible');
      }
    }
  }

  window.addEventListener('scroll', function () {
    if (!scrollTicking) {
      window.requestAnimationFrame(updateScrollState);
      scrollTicking = true;
    }
  }, { passive: true });

  // Defer initial scroll state check via rAF to avoid synchronous forced reflow on initial page load
  window.requestAnimationFrame(updateScrollState);

  /* ============================================================
     HORIZONTAL SLIDERS (Mobile Wireframe: Produk & Testimoni)
     ============================================================ */
  function setupHorizontalSlider(wrapperId, trackId, dotsId) {
    const wrapper = document.getElementById(wrapperId);
    if (!wrapper) return;
    const track = document.getElementById(trackId);
    if (!track) return;
    const prevBtn = wrapper.querySelector('.gs-slider-arrow--prev');
    const nextBtn = wrapper.querySelector('.gs-slider-arrow--next');
    const dotsContainer = document.getElementById(dotsId);

    const cards = Array.from(track.children).filter(function (child) {
      return !child.classList.contains('gs-slider-arrow') && !child.classList.contains('gs-slider-hint');
    });

    if (cards.length === 0) return;

    // Build pagination dots
    if (dotsContainer) {
      dotsContainer.innerHTML = '';
      cards.forEach(function (_, idx) {
        const dot = document.createElement('button');
        dot.type = 'button';
        dot.className = 'gs-slider-dot' + (idx === 0 ? ' is-active' : '');
        dot.setAttribute('aria-label', 'Slide ' + (idx + 1));
        dot.addEventListener('click', function () {
          cards[idx].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
        });
        dotsContainer.appendChild(dot);
      });
    }

    function getCardStep() {
      if (cards[0]) {
        const rect = cards[0].getBoundingClientRect();
        return rect.width + 16;
      }
      return 300;
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        track.scrollBy({ left: -getCardStep(), behavior: 'smooth' });
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        track.scrollBy({ left: getCardStep(), behavior: 'smooth' });
      });
    }

    let sliderTicking = false;
    track.addEventListener('scroll', function () {
      if (sliderTicking) return;
      sliderTicking = true;
      window.requestAnimationFrame(function () {
        sliderTicking = false;
        if (!dotsContainer) return;
        const trackRect = track.getBoundingClientRect();
        const trackCenter = trackRect.left + trackRect.width / 2;

        let closestIdx = 0;
        let minDiff = Infinity;
        cards.forEach(function (card, idx) {
          const r = card.getBoundingClientRect();
          const cardCenter = r.left + r.width / 2;
          const diff = Math.abs(cardCenter - trackCenter);
          if (diff < minDiff) {
            minDiff = diff;
            closestIdx = idx;
          }
        });

        const dots = dotsContainer.querySelectorAll('.gs-slider-dot');
        dots.forEach(function (dot, idx) {
          if (idx === closestIdx) {
            dot.classList.add('is-active');
            dot.setAttribute('aria-current', 'true');
          } else {
            dot.classList.remove('is-active');
            dot.removeAttribute('aria-current');
          }
        });
      });
    }, { passive: true });
  }

  setupHorizontalSlider('gs-home-product-slider', 'gs-home-product-track', 'gs-home-product-dots');
  setupHorizontalSlider('gs-home-testi-slider', 'gs-home-testi-track', 'gs-home-testi-dots');

  /* ============================================================
     MOBILE VIEW SWITCHER (Grid vs Slide Mode)
     ============================================================ */
  const viewSwitchBtns = document.querySelectorAll('.gs-view-switch__btn');
  viewSwitchBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      const mode = this.dataset.viewMode;
      const targetGridId = this.dataset.targetGrid;
      const parentWrap = this.closest('.gs-view-switch-wrap');

      let grid = null;
      if (targetGridId) {
        grid = document.getElementById(targetGridId);
      } else if (parentWrap) {
        const nextSec = parentWrap.nextElementSibling;
        grid = nextSec ? (nextSec.matches('.gs-grid-3') ? nextSec : nextSec.querySelector('.gs-grid-3')) : null;
      }
      if (!grid) {
        grid = document.querySelector('.gs-grid-3');
      }
      if (!grid) return;

      const parentSwitch = this.closest('.gs-view-switch');
      if (parentSwitch) {
        parentSwitch.querySelectorAll('.gs-view-switch__btn').forEach(function (b) {
          b.classList.remove('active');
          b.setAttribute('aria-pressed', 'false');
        });
      }
      this.classList.add('active');
      this.setAttribute('aria-pressed', 'true');

      const slideHint = parentWrap ? parentWrap.querySelector('.gs-slide-hint') : null;

      if (mode === 'slide') {
        grid.classList.add('is-slide-mode');
        if (slideHint) slideHint.style.display = 'inline-flex';
      } else {
        grid.classList.remove('is-slide-mode');
        if (slideHint) slideHint.style.display = 'none';
      }
    });
  });

})();
