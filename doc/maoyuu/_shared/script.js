/* ============================================
   魔王勇者 政治经济学知识点手册 — 共享脚本
   ============================================ */
(function() {
  'use strict';

  /* --- Nav Toggle --- */
  function initNavToggle() {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.site-nav');
    if (!toggle || !nav) return;
    toggle.addEventListener('click', function() {
      nav.classList.toggle('open');
      var expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
    });
  }

  /* --- Collapsibles --- */
  function initCollapsibles() {
    var toggles = document.querySelectorAll('.collapsible-toggle');
    toggles.forEach(function(btn) {
      btn.addEventListener('click', function() {
        var target = document.getElementById(btn.getAttribute('aria-controls'));
        if (!target) return;
        var expanded = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', String(!expanded));
        target.hidden = expanded;
      });
    });
  }

  /* --- Filter --- */
  function initFilter() {
    var btns = document.querySelectorAll('.filter-btn');
    var cards = document.querySelectorAll('.topic-card');
    if (btns.length === 0 || cards.length === 0) return;
    btns.forEach(function(btn) {
      btn.addEventListener('click', function() {
        btns.forEach(function(b) { b.classList.remove('active'); });
        btn.classList.add('active');
        var filter = btn.getAttribute('data-filter');
        cards.forEach(function(card) {
          if (filter === 'all' || card.getAttribute('data-discipline') === filter) {
            card.style.display = '';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  /* --- Back to Top --- */
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

  /* --- Side TOC --- */
  function initSideToc() {
    var toc = document.querySelector('.side-toc');
    if (!toc) return;
    var links = toc.querySelectorAll('a');
    var sections = [];
    links.forEach(function(link) {
      var id = link.getAttribute('href');
      if (id && id.startsWith('#')) {
        var el = document.getElementById(id.slice(1));
        if (el) sections.push({ link: link, el: el });
      }
    });
    if (sections.length === 0) return;

    function updateActive() {
      var scrollY = window.scrollY + 100;
      var current = null;
      sections.forEach(function(s) {
        if (s.el.offsetTop <= scrollY) current = s;
      });
      links.forEach(function(l) { l.classList.remove('active'); });
      if (current) current.link.classList.add('active');
    }
    window.addEventListener('scroll', updateActive);
    updateActive();
  }

  /* --- Smooth Scroll --- */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function(a) {
      a.addEventListener('click', function(e) {
        var target = document.querySelector(a.getAttribute('href'));
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function() {
    initNavToggle();
    initCollapsibles();
    initFilter();
    initBackToTop();
    initSideToc();
    initSmoothScroll();
  });
})();
