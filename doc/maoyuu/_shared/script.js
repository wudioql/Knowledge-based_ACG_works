/* =====================================================================
   《魔王勇者》政治经济学知识手册 — 作品级交互脚本
   设计哲学：交互围绕「手抄本研读」形态重新设计，不复用既有作品的通用筛选/折叠函数。
   全部以 IIFE 封装，DOMContentLoaded 统一调度，原生 DOM API + 事件委托。
   导航数据（本编/外传/辅助卷宗）在此集中定义一次，运行时注入各页 .rail__nav。
   ===================================================================== */
(function () {
  'use strict';

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  /* —— 共享导航数据：只在此处维护一次，各页运行时注入 —— */
  var NAV = {
    main: [
      { id: 'vol-01', num: '1', label: '「勇者啊，当我的人吧」「我拒绝！」', href: 'vol-01-pact-and-perpetual-war.html' },
      { id: 'vol-02', num: '2', label: '忽邻塔的阴谋', href: 'vol-02-kurultai-and-coin.html' },
      { id: 'vol-03', num: '3', label: '圣键远征军', href: 'vol-03-holy-key-and-firearms.html' },
      { id: 'vol-04', num: '4', label: '己所能为', href: 'vol-04-hands-and-famine.html' },
      { id: 'vol-05', num: '5', label: '在那山丘的彼方', href: 'vol-05-beyond-the-hill.html' }
    ],
    side: [
      { id: 'ep-01', num: '①', label: '榆之国的女魔法使', href: 'ep-01-magician-of-the-elm.html' },
      { id: 'ep-02', num: '②', label: '砂丘之国的弓使', href: 'ep-02-archer-of-the-desert.html' },
      { id: 'ep-03', num: '③', label: '花之国的女骑士', href: 'ep-03-knight-of-the-flowers.html' }
    ],
    aux: [
      { id: 'glossary', num: '●', label: '术语表', href: 'glossary.html' },
      { id: 'characters', num: '●', label: '人物与势力', href: 'characters.html' },
      { id: 'references', num: '●', label: '参考文献', href: 'references.html' }
    ]
  };

  /* —— 注入共享导航：写入 [data-nav-mount]，按 data-active 高亮当前页 —— */
  function initSharedNav() {
    var mount = document.querySelector('.rail__nav[data-nav-mount]');
    if (!mount) return;
    var active = mount.getAttribute('data-active') || '';
    var groups = [
      { sec: '本编', items: NAV.main },
      { sec: '外传', items: NAV.side },
      { sec: '辅助卷宗', items: NAV.aux }
    ];
    var html = '';
    groups.forEach(function (g) {
      html += '<div class="rail__sec">' + g.sec + '</div><ul class="rail__list">';
      g.items.forEach(function (it) {
        var cls = (it.id === active) ? ' class="is-here"' : '';
        html += '<li><a' + cls + ' href="' + it.href + '"><span class="num">' + it.num + '</span>' + it.label + '</a></li>';
      });
      html += '</ul>';
    });
    mount.innerHTML = html;
  }

  /* —— 卷轴阅读进度条：跟随对开页滚动，呼应"翻阅纶旨" —— */
  function initCodexProgress() {
    var bar = document.querySelector('.progress');
    if (!bar) return;
    function tick() {
      var h = document.documentElement;
      var scrolled = h.scrollTop || document.body.scrollTop;
      var max = (h.scrollHeight - h.clientHeight) || 1;
      bar.style.width = Math.min(100, (scrolled / max) * 100) + '%';
    }
    window.addEventListener('scroll', tick, { passive: true });
    tick();
  }

  /* —— 页边抽屉（移动端展开左侧目录） —— */
  function initFolioDrawer() {
    var btn = document.querySelector('.rail-toggle');
    var rail = document.querySelector('.rail');
    if (!btn || !rail) return;
    btn.addEventListener('click', function () {
      var open = rail.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    rail.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a || window.innerWidth > 992) return;
      // 页内 # 锚点由 initSmoothAnchor 负责：先收起抽屉、等待布局稳定，再计算滚动位置。
      // 若这里立即收起，目标 offset 会在折叠动画后上移，导致窄屏跳转“翻过头”。
      if ((a.getAttribute('href') || '').charAt(0) === '#') return;
      rail.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
    });
  }

  /* —— 页边索引随滚动高亮「本卷脉络」当前条目（scroll-spy，仅作用于页内 # 锚点） —— */
  function initGutterSpy() {
    var rail = document.querySelector('.rail');
    var folio = document.querySelector('.folio') || document.querySelector('.workindex');
    if (!rail || !folio) return;
    // 仅取页内锚点（href 以 # 开头），不误伤跨页导航链接
    var links = Array.prototype.slice.call(rail.querySelectorAll('.rail__list a[href^="#"]'));
    if (!links.length) return;
    var targets = links.map(function (l) {
      return document.getElementById(l.getAttribute('href').slice(1));
    }).filter(Boolean);
    if (!targets.length) return;
    var ticking = false;
    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var pos = (document.documentElement.scrollTop || document.body.scrollTop) + 120;
        var idx = 0;
        for (var i = 0; i < targets.length; i++) {
          if (targets[i].offsetTop <= pos) idx = i;
        }
        links.forEach(function (l, i) { l.classList.toggle('is-here', i === idx); });
        ticking = false;
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* —— 平滑滚动到页内锚点（修正 sticky 顶部偏移） —— */
  function initSmoothAnchor() {
    var rail = document.querySelector('.rail');
    if (!rail) return;
    var btn = document.querySelector('.rail-toggle');

    function isNarrow() {
      return window.matchMedia ? window.matchMedia('(max-width: 62rem)').matches : window.innerWidth <= 992;
    }
    function stickyOffset() {
      var brand = document.querySelector('.brand');
      var offset = brand ? brand.offsetHeight : 0;
      // 窄屏时 .rail-dock / .rail-toggle 会粘在顶栏下方，也需要计入遮挡高度。
      if (isNarrow() && btn && getComputedStyle(btn).display !== 'none') offset += btn.offsetHeight;
      return offset + 12; // 额外留一点羊皮纸呼吸空间
    }
    function jumpTo(el, id) {
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          var top = el.getBoundingClientRect().top + (window.pageYOffset || document.documentElement.scrollTop) - stickyOffset();
          window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
          history.replaceState(null, '', '#' + id);
        });
      });
    }

    rail.addEventListener('click', function (e) {
      var a = e.target.closest('a[href^="#"]');
      if (!a) return;
      var id = a.getAttribute('href').slice(1);
      var el = document.getElementById(id);
      if (!el) return;
      e.preventDefault();

      if (isNarrow() && rail.classList.contains('open')) {
        rail.classList.remove('open');
        if (btn) btn.setAttribute('aria-expanded', 'false');
        // 等待抽屉 max-height 折叠动画结束后再测量 target，否则会多滚过一个抽屉高度。
        window.setTimeout(function () { jumpTo(el, id); }, 280);
      } else {
        jumpTo(el, id);
      }
    });
  }

  /* —— 返回页顶（羊皮卷升卷） —— */
  function initVellumLift() {
    var btn = document.querySelector('.to-top');
    if (!btn) return;
    window.addEventListener('scroll', function () {
      btn.classList.toggle('show', (document.documentElement.scrollTop || document.body.scrollTop) > 600);
    }, { passive: true });
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* —— 账簿对照：点按某列以「钉选」高亮，便于逐条研读 —— */
  function initLedgerCompare() {
    var ledgers = document.querySelectorAll('.ledger');
    if (!ledgers.length) return;
    ledgers.forEach(function (lg) {
      var heads = lg.querySelectorAll('.ledger__cell');
      heads.forEach(function (cell) {
        cell.addEventListener('click', function () {
          heads.forEach(function (c) { c.classList.remove('is-pinned'); });
          cell.classList.add('is-pinned');
        });
      });
    });
    document.addEventListener('keydown', function (e) {
      if (!/^[123]$/.test(e.key)) return;
      var view = document.querySelector('.ledger.is-inview') || ledgers[ledgers.length - 1];
      if (!view) return;
      var cells = view.querySelectorAll('.ledger__cell');
      var idx = parseInt(e.key, 10) - 1;
      if (cells[idx]) cells[idx].scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (ents) {
        ents.forEach(function (en) {
          if (en.isIntersecting) {
            ledgers.forEach(function (l) { l.classList.remove('is-inview'); });
            en.target.classList.add('is-inview');
          }
        });
      }, { rootMargin: '-30% 0px -50% 0px' });
      ledgers.forEach(function (l) { io.observe(l); });
    }
  }

  /* —— 知识领域筛盘（仅作品首页 volgrid 使用）：按学科筛选卷目 —— */
  function initDomainSieve() {
    var sieve = document.querySelector('.domain-sieve');
    var cards = document.querySelectorAll('.volgrid .volcard');
    if (!sieve || !cards.length) return;
    sieve.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-domain]');
      if (!btn) return;
      var d = btn.getAttribute('data-domain');
      sieve.querySelectorAll('[data-domain]').forEach(function (b) {
        b.classList.toggle('on', b === btn);
      });
      cards.forEach(function (c) {
        var show = (d === 'all') || (c.getAttribute('data-domains') || '').indexOf(d) > -1;
        c.style.display = show ? '' : 'none';
      });
    });
  }

  /* —— ECharts 自适应尺寸：修复「图表内容挤在左侧小区域」的初始化宽度 bug ——
     根因：图表在 DOMContentLoaded 初始化时，容器宽度可能尚未确定（外部 CSS 未应用完、
     iframe 尺寸尚未稳定、移动端目录展开等），导致 ECharts 以近零宽度渲染并锁定。
     解法：在布局稳定后对所有实例调用 resize()，并通过 ResizeObserver 监听容器尺寸变化。
     无需改动各页内联初始化代码——通过 echarts.getInstanceByDom() 逐个调整。 —— */
  function resizeAllCharts() {
    if (typeof echarts === 'undefined') return;
    document.querySelectorAll('.chart').forEach(function (el) {
      var inst = echarts.getInstanceByDom(el);
      if (inst) inst.resize();
    });
  }
  function initChartAutoSize() {
    // 双重 rAF：确保首帧布局与绘制完成后校正一次
    requestAnimationFrame(function () { requestAnimationFrame(resizeAllCharts); });
    // window.load：外部 CSS、字体等全部就绪后最终校正（最可靠的兜底）
    window.addEventListener('load', resizeAllCharts);
    // 窗口尺寸变化（桌面端缩放、移动端旋转）
    var rt;
    window.addEventListener('resize', function () {
      clearTimeout(rt); rt = setTimeout(resizeAllCharts, 120);
    });
    // 容器尺寸变化（沙箱 iframe 调整、移动端目录抽屉展开/收起改变可用宽度）
    if (typeof ResizeObserver !== 'undefined') {
      var ct;
      var ro = new ResizeObserver(function () {
        clearTimeout(ct); ct = setTimeout(resizeAllCharts, 120);
      });
      // 仅观察容器盒子：其尺寸由 CSS 决定，ECharts resize 不会改变它，故无循环风险
      document.querySelectorAll('.chart').forEach(function (el) { ro.observe(el); });
    }
    // 字体加载完成后再校正一次（中文衬线字体回填可能改变高度计算）
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(resizeAllCharts);
    }
  }

  /* —— 目录栏停靠区：把 rail-toggle 与 rail 包裹进 .rail-dock，使其在窄屏可整块粘在顶栏下 ——
     集中处理，避免改动 11 个页面的 HTML。若二者已是 .rail-dock 的子元素则跳过（防重复）。 —— */
  function initRailDock() {
    var toggle = document.querySelector('.rail-toggle');
    var rail = document.querySelector('.rail');
    if (!toggle || !rail) return;
    if (toggle.parentNode && toggle.parentNode.classList.contains('rail-dock')) return;
    var layout = toggle.parentNode;            // .layout
    if (!layout) return;
    var dock = document.createElement('div');
    dock.className = 'rail-dock';
    layout.insertBefore(dock, toggle);          // 在 toggle 原位置插入停靠区
    dock.appendChild(toggle);
    dock.appendChild(rail);                      // toggle 在前、rail 在后，顺序不变
  }

  /* —— 测量顶栏实际高度，写入 --header-h，供 .rail-dock 精确贴在顶栏正下方 —— */
  function initHeaderVar() {
    var brand = document.querySelector('.brand');
    if (!brand) return;
    function set() {
      document.documentElement.style.setProperty('--header-h', brand.offsetHeight + 'px');
    }
    set();
    window.addEventListener('resize', set);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(set);
  }

  ready(function () {
    initRailDock();      // 先包裹出停靠区（改 DOM 结构），再注入共享导航与绑定交互
    initHeaderVar();
    initSharedNav();      // 先注入共享导航，再绑定交互
    initCodexProgress();
    initFolioDrawer();
    initSmoothAnchor();
    initGutterSpy();
    initVellumLift();
    initLedgerCompare();
    initDomainSieve();
    initChartAutoSize();  // 最后绑定图表自适应（此时各页内联脚本已完成图表初始化）
  });
})();
