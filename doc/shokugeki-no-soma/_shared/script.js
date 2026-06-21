/* ============================================
   《食戟之灵》料理内容图文文档 — 共享脚本
   ============================================ */

(function() {
  'use strict';

  // --- Sticky Offsets Sync ---
  function updateStickyOffsets() {
    var header = document.querySelector('.site-header');
    var filter = document.querySelector('.filter-bar');
    
    var headerH = header ? header.offsetHeight : 0;
    var filterH = filter ? filter.offsetHeight : 0;
    
    document.documentElement.style.setProperty('--header-height', headerH + 'px');
    document.documentElement.style.setProperty('--filter-height', filterH + 'px');
    document.documentElement.style.setProperty('--total-offset', (headerH + filterH) + 'px');
  }

  // --- Mobile Navigation Toggle ---


  function initNavToggle() {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.site-nav');
    if (!toggle || !nav) return;

    toggle.addEventListener('click', function() {
      nav.classList.toggle('open');
      toggle.textContent = nav.classList.contains('open') ? '✕' : '☰';
    });

    // Close nav when clicking a link
    nav.querySelectorAll('a').forEach(function(link) {
      link.addEventListener('click', function() {
        nav.classList.remove('open');
        toggle.textContent = '☰';
      });
    });
  }

  // --- Collapsible Sections ---
  function initCollapsibles() {
    document.querySelectorAll('.collapsible-toggle').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var content = btn.nextElementSibling;
        if (!content) return;
        var isOpen = btn.classList.contains('open');

        btn.classList.toggle('open');
        content.classList.toggle('open');

        if (!isOpen) {
          // Smooth scroll to reveal
          setTimeout(function() {
            btn.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }, 100);
        }
      });
    });
  }

  // --- Cuisine Filter ---
  function initFilter() {
    var filterBtns = document.querySelectorAll('.filter-btn');
    var dishCards = document.querySelectorAll('.dish-card[data-cuisine]');

    if (filterBtns.length === 0 || dishCards.length === 0) return;

    filterBtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
        var cuisine = btn.getAttribute('data-filter');

        // Update active state
        filterBtns.forEach(function(b) { b.classList.remove('active'); });
        btn.classList.add('active');

        // Filter cards and Sync Side TOC
        dishCards.forEach(function(card) {
          var isVisible = (cuisine === 'all' || card.getAttribute('data-cuisine') === cuisine);
          card.style.display = isVisible ? '' : 'none';

          // Sync Side TOC: Find the link that points to this card's ID
          var cardId = card.id;
          if (cardId) {
            var tocLink = document.querySelector('.side-toc a[href="#' + cardId + '"]');
            if (tocLink) {
              var li = tocLink.parentElement;
              li.style.display = isVisible ? '' : 'none';
            }
          }
        });
      });
    });
  }

  // --- Back to Top Button ---
  function initBackToTop() {
    var btn = document.querySelector('.back-to-top');
    if (!btn) return;

    window.addEventListener('scroll', function() {
      if (window.scrollY > 400) {
        btn.classList.add('visible');
      } else {
        btn.classList.remove('visible');
      }
    });

    btn.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // --- Side TOC Active Highlight ---
  function initSideTocActiveHighlight() {
    var tocLinks = document.querySelectorAll('.side-toc a');
    if (tocLinks.length === 0) return;

    var sections = [];
    tocLinks.forEach(function(link) {
      var id = link.getAttribute('href');
      if (id && id.startsWith('#')) {
        var el = document.querySelector(id);
        if (el) {
          sections.push({ el: el, link: link });
        }
      }
    });

    if (sections.length === 0) return;

    function updateActive() {
      var scrollPos = window.scrollY + 120; // Adjusted offset for better feel
      var active = null;

      // Find the last section that is above the current scroll position
      for (var i = sections.length - 1; i >= 0; i--) {
        if (sections[i].el.offsetTop <= scrollPos) {
          active = sections[i];
          break;
        }
      }

      // Special case: if we've scrolled almost to the bottom, highlight the last section
      if (!active && window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
        active = sections[sections.length - 1];
      }

      tocLinks.forEach(function(l) { l.classList.remove('active'); });
      if (active) {
        active.link.classList.add('active');
      }
    }

    window.addEventListener('scroll', updateActive);
    window.addEventListener('resize', updateActive);
    updateActive();
  }

  // --- Scroll Reveal Animations ---
  function initScrollReveal() {
    var observerOptions = {
      root: null,
      rootMargin: '0px',
      threshold: 0.1
    };

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('reveal-visible');
          // Once revealed, we can stop observing to optimize performance
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    // Targets for reveal animation
    var revealTargets = document.querySelectorAll('.dish-card, .battle-section, .arc-overview, .cuisine-card');
    revealTargets.forEach(function(target) {
      target.classList.add('reveal');
      observer.observe(target);
    });
  }

  // --- Mobile TOC Toggle ---
  function initMobileToc() {
    var toc = document.querySelector('.side-toc');
    if (!toc) return;

    // Create trigger button
    var trigger = document.createElement('button');
    trigger.className = 'toc-trigger';
    trigger.innerHTML = '☰';
    trigger.setAttribute('aria-label', '打开目录');
    document.body.appendChild(trigger);

    trigger.addEventListener('click', function(e) {
      e.stopPropagation();
      toc.classList.toggle('mobile-open');
    });

    // Close when clicking outside
    document.addEventListener('click', function(e) {
      if (toc.classList.contains('mobile-open') && !toc.contains(e.target) && e.target !== trigger) {
        toc.classList.remove('mobile-open');
      }
    });

    // Close when a link is clicked
    toc.querySelectorAll('a').forEach(function(link) {
      link.addEventListener('click', function() {
        toc.classList.remove('mobile-open');
      });
    });
  }

  // --- Smooth scroll for anchor links ---


  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function(link) {
      link.addEventListener('click', function(e) {
        var target = document.querySelector(link.getAttribute('href'));
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  // --- Initialize All ---
  document.addEventListener('DOMContentLoaded', function() {
    updateStickyOffsets();
    initNavToggle();
    initCollapsibles();
    initFilter();
    initBackToTop();
    initSideTocActiveHighlight();
    initSmoothScroll();
    initScrollReveal();
    initMobileToc();
  });

  window.addEventListener('resize', updateStickyOffsets);

})();
