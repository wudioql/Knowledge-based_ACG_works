/* ============================================
   ACG 知识库 — 全局共享脚本
   ============================================ */

(function() {
  'use strict';

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

  // --- Sidebar Toggle for Documentation ---
  function initSidebarToggle() {
    var toggle = document.querySelector('#sidebarToggle');
    var sidebar = document.querySelector('.sidebar-toc');
    if (!toggle || !sidebar) return;

    toggle.addEventListener('click', function() {
      sidebar.classList.toggle('open');
      toggle.setAttribute('aria-expanded', sidebar.classList.contains('open') ? 'true' : 'false');
    });

    // Close sidebar when clicking a link
    sidebar.querySelectorAll('a').forEach(function(link) {
      link.addEventListener('click', function() {
        sidebar.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
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

        // Filter cards
        dishCards.forEach(function(card) {
          if (cuisine === 'all' || card.getAttribute('data-cuisine') === cuisine) {
            card.style.display = '';
          } else {
            card.style.display = 'none';
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
  function initSideToc() {
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

    function updateActive() {
      var scrollPos = window.scrollY + 100;
      var active = null;

      for (var i = sections.length - 1; i >= 0; i--) {
        if (sections[i].el.offsetTop <= scrollPos) {
          active = sections[i];
          break;
        }
      }

      tocLinks.forEach(function(l) { l.classList.remove('active'); });
      if (active) {
        active.link.classList.add('active');
      }
    }

    window.addEventListener('scroll', updateActive);
    updateActive();
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
    initNavToggle();
    initSidebarToggle();
    initCollapsibles();
    initFilter();
    initBackToTop();
    initSideToc();
    initSmoothScroll();
  });

})();
