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
    hamburger.addEventListener('click', function () {
      const expanded = this.getAttribute('aria-expanded') === 'true';
      this.setAttribute('aria-expanded', String(!expanded));
      mobileMenu.classList.toggle('is-open');
    });

    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        hamburger.setAttribute('aria-expanded', 'false');
        mobileMenu.classList.remove('is-open');
      }
    });

    // Close when clicking outside
    document.addEventListener('click', function (e) {
      if (!hamburger.contains(e.target) && !mobileMenu.contains(e.target)) {
        hamburger.setAttribute('aria-expanded', 'false');
        mobileMenu.classList.remove('is-open');
      }
    });

    // Close when a nav link is clicked
    mobileMenu.querySelectorAll('.gs-navbar__mobile-link').forEach(function (link) {
      link.addEventListener('click', function () {
        hamburger.setAttribute('aria-expanded', 'false');
        mobileMenu.classList.remove('is-open');
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
  const filterTabs = document.querySelectorAll('.gs-filter-tab');
  if (filterTabs.length) {
    filterTabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        const filter = this.dataset.filter;

        // Update active tab
        filterTabs.forEach(function (t) { t.classList.remove('active'); });
        this.classList.add('active');

        // Show/hide cards
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

        // Empty state
        const emptyState = document.getElementById('gs-empty-state');
        if (emptyState) {
          emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
        }
      });
    });
  }

  /* ============================================================
     ACTIVE NAV LINK (based on current path)
     ============================================================ */
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.gs-navbar__link, .gs-navbar__mobile-link').forEach(function (link) {
    const href = link.getAttribute('href');
    if (href && (href === currentPath || href.endsWith(currentPath))) {
      link.classList.add('active');
    }
  });

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
     SCROLL-BASED NAVBAR SHADOW
     ============================================================ */
  const navbar = document.querySelector('.gs-navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 10) {
        navbar.style.boxShadow = '0 4px 24px rgba(35, 71, 45, 0.12)';
      } else {
        navbar.style.boxShadow = '';
      }
    }, { passive: true });
  }

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

    function openModal(data) {
      if (modalImg)   { modalImg.src = data.image; modalImg.alt = data.title; }
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
    }

    function closeModal() {
      modalOverlay.classList.remove('is-open');
      document.body.style.overflow = '';
    }

    if (modalClose) modalClose.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', function (e) {
      if (e.target === modalOverlay) closeModal();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modalOverlay.classList.contains('is-open')) closeModal();
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
        });
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
  const blogSearchInput = document.getElementById('gs-blog-search-input');
  const blogFilterTabs  = document.querySelectorAll('.gs-blog-filter-tab');
  const blogCards       = document.querySelectorAll('.gs-blog-card-item');
  const blogEmptyState  = document.getElementById('gs-blog-empty-state');
  const blogCountEl     = document.getElementById('gs-blog-count');

  if (blogCards.length && (blogSearchInput || blogFilterTabs.length)) {
    let currentCategory = 'semua';
    let searchQuery = '';

    function filterBlogCards() {
      let visibleCount = 0;
      const q = searchQuery.toLowerCase().trim();

      blogCards.forEach(function (card) {
        const cat = (card.dataset.category || '').toLowerCase();
        const title = (card.querySelector('.gs-blog-card__title')?.textContent || '').toLowerCase();
        const excerpt = (card.querySelector('.gs-blog-card__excerpt')?.textContent || '').toLowerCase();

        const matchesCat = (currentCategory === 'semua' || cat === currentCategory);
        const matchesSearch = !q || title.includes(q) || excerpt.includes(q) || cat.includes(q);

        if (matchesCat && matchesSearch) {
          card.style.display = '';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      if (blogEmptyState) {
        blogEmptyState.style.display = visibleCount === 0 ? 'block' : 'none';
      }
      if (blogCountEl) {
        blogCountEl.textContent = 'Menampilkan ' + visibleCount + ' artikel';
      }
    }

    if (blogSearchInput) {
      blogSearchInput.addEventListener('input', function () {
        searchQuery = this.value;
        filterBlogCards();
      });
    }

    blogFilterTabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        blogFilterTabs.forEach(function (t) { t.classList.remove('active'); });
        this.classList.add('active');
        currentCategory = (this.dataset.filter || 'semua').toLowerCase();
        filterBlogCards();
      });
    });
  }

})();
