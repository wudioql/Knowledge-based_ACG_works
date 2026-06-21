/* ============================================
   《萌菌物语》微生物知识全鉴 — 共享脚本
   设计原则：本作品的交互集合与已有作品（filter/collapsible/side-toc/back-to-top/smoothScroll/navToggle）完全不同，
   专为微生物图鉴定制：标本卡翻转 / 菌种目录锚点跳转 / 培养基筛选
   ============================================ */
(function () {
  'use strict';

  /* --- Specimen-bar 移动端导航折叠（仅标本栏内） --- */
  function initSpecimenNavToggle() {
    var toggle = document.querySelector('.specimen-bar .nav-toggle');
    var nav = document.querySelector('.specimen-bar .specimen-nav');
    if (!toggle || !nav) return;
    toggle.addEventListener('click', function () {
      nav.classList.toggle('open');
      var open = nav.classList.contains('open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? '✕ 关闭' : '☰ 目录';
    });
  }

  /* --- 标本卡翻转：在移动端以 CSS-only 标签页切换替代三栏对照表 --- */
  // 移动端 CSS 通过 input:checked 处理，无需 JS。但提供 JS 兜底增强（键盘可达）。
  function initSpecimenTabs() {
    var wrappers = document.querySelectorAll('.mobile-tabs');
    wrappers.forEach(function (w) {
      var inputs = w.querySelectorAll('input[type="radio"]');
      inputs.forEach(function (inp) {
        inp.addEventListener('change', function () {
          inputs.forEach(function (i) { i.setAttribute('aria-checked', String(i === inp)); });
        });
      });
    });
  }

  /* --- 菌种目录锚点高亮（滚动到当前可见 specimen） --- */
  function initAtlasScrollSpy() {
    var atlasLinks = document.querySelectorAll('.atlas-list a');
    if (atlasLinks.length === 0) return;
    var targetMap = {};
    atlasLinks.forEach(function (a) {
      var href = a.getAttribute('href');
      if (href && href.startsWith('#')) targetMap[href.slice(1)] = a;
    });
    var targets = Object.keys(targetMap).map(function (id) {
      var el = document.getElementById(id);
      return el ? { id: id, el: el, link: targetMap[id] } : null;
    }).filter(Boolean);
    if (targets.length === 0) return;

    function update() {
      var scrollY = window.scrollY + 160;
      var current = targets[0];
      for (var i = 0; i < targets.length; i++) {
        if (targets[i].el.offsetTop <= scrollY) current = targets[i];
      }
      atlasLinks.forEach(function (a) {
        a.style.background = '';
        a.style.color = '';
        a.style.fontWeight = '';
      });
      if (current) {
        current.link.style.background = 'var(--agar)';
        current.link.style.color = 'var(--paper)';
        current.link.style.fontWeight = '700';
      }
    }
    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  /* --- 培养基筛选（首页 / 术语表页）：按学科 tag 过滤 --- */
  function initMediumFilter() {
    var btns = document.querySelectorAll('[data-medium-filter]');
    var cards = document.querySelectorAll('[data-medium]');
    if (btns.length === 0 || cards.length === 0) return;
    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        btns.forEach(function (b) {
          b.classList.remove('active');
          b.style.background = '';
          b.style.color = '';
        });
        btn.classList.add('active');
        btn.style.background = 'var(--agar-deep)';
        btn.style.color = 'var(--paper)';
        var f = btn.getAttribute('data-medium-filter');
        cards.forEach(function (card) {
          if (f === 'all' || card.getAttribute('data-medium') === f) {
            card.style.display = '';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  /* --- 返回顶部按钮（培养皿样式） --- */
  function initBackToTop() {
    var btn = document.querySelector('.back-to-top');
    if (!btn) return;
    window.addEventListener('scroll', function () {
      if (window.scrollY > 500) btn.classList.add('visible');
      else btn.classList.remove('visible');
    }, { passive: true });
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* --- 平滑滚动（标本目录的锚点链接） --- */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      var href = a.getAttribute('href');
      if (!href || href === '#') return;
      a.addEventListener('click', function (e) {
        var id = href.slice(1);
        var target = document.getElementById(id);
        if (target) {
          e.preventDefault();
          var offset = 110; // 标本栏 + 面包屑偏移
          var top = target.getBoundingClientRect().top + window.scrollY - offset;
          window.scrollTo({ top: top, behavior: 'smooth' });
          // 更新 URL hash 但不跳转
          if (history.pushState) history.pushState(null, '', '#' + id);
        }
      });
    });
  }

  /* --- 三栏对照表移动端 tab UI（自动为每个 tri-comp 生成移动端版本） --- */
  function buildMobileTabs() {
    var triComps = document.querySelectorAll('.tri-comp');
    var builtAny = false;

    function collectCells(tri, type) {
      return Array.prototype.slice.call(tri.querySelectorAll('.col-cell[data-col="' + type + '"]'));
    }

    function renderCells(cells) {
      return cells.map(function (cell) {
        return '<div class="mobile-tab-segment">' + cell.innerHTML + '</div>';
      }).join('');
    }

    triComps.forEach(function (tri, idx) {
      if (tri.nextElementSibling && tri.nextElementSibling.classList.contains('mobile-tabs')) return;

      var id = 'tri-' + idx + '-' + Math.random().toString(36).slice(2, 7);
      var fictionCells = collectCells(tri, 'fiction');
      var scienceCells = collectCells(tri, 'science');
      var cultureCells = collectCells(tri, 'culture');
      if (!fictionCells.length || !scienceCells.length || !cultureCells.length) return;

      var tabs = document.createElement('div');
      tabs.className = 'mobile-tabs';
      var radioF = id + '-fiction';
      var radioS = id + '-science';
      var radioC = id + '-culture';
      tabs.innerHTML =
        '<input type="radio" name="' + id + '" id="' + radioF + '" checked>' +
        '<input type="radio" name="' + id + '" id="' + radioS + '">' +
        '<input type="radio" name="' + id + '" id="' + radioC + '">' +
        '<div class="tab-labels">' +
          '<label for="' + radioF + '">虚构</label>' +
          '<label for="' + radioS + '">科学</label>' +
          '<label for="' + radioC + '">文化</label>' +
        '</div>' +
        '<div class="tab-content" data-tab="fiction">' + renderCells(fictionCells) + '</div>' +
        '<div class="tab-content" data-tab="science">' + renderCells(scienceCells) + '</div>' +
        '<div class="tab-content" data-tab="culture">' + renderCells(cultureCells) + '</div>';

      tri.parentNode.insertBefore(tabs, tri.nextSibling);
      builtAny = true;
    });
    if (builtAny) document.documentElement.classList.add('has-mobile-tabs');
  }

  /* --- 启动 --- */
  function boot() {
    initSpecimenNavToggle();
    buildMobileTabs();
    initSpecimenTabs();
    initAtlasScrollSpy();
    initMediumFilter();
    initBackToTop();
    initSmoothScroll();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
