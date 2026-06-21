/* ==========================================================================
   星空清理者 · 知识手册 —— 作品交互脚本
   按本作品「任务控制台 / 飞行日志」形态定制，非复制他作。
   功能：移动端导航抽屉、三方对照标签页（手机端）、回到顶部、
        当前页高亮、ECharts 响应式重绘。
   ========================================================================== */
(function () {
  "use strict";

  /* —— 1. 移动端导航抽屉 —— */
  function initNavDrawer() {
    var shell = document.querySelector(".pl-shell");
    var toggle = document.querySelector(".pl-menu-toggle");
    var scrim = document.querySelector(".pl-nav-scrim");
    if (!shell || !toggle) return;

    function close() { shell.classList.remove("is-nav-open"); toggle.setAttribute("aria-expanded", "false"); }
    function open() { shell.classList.add("is-nav-open"); toggle.setAttribute("aria-expanded", "true"); }

    toggle.addEventListener("click", function () {
      shell.classList.contains("is-nav-open") ? close() : open();
    });
    if (scrim) scrim.addEventListener("click", close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
    // 点击导航项后关闭（移动端）
    document.querySelectorAll(".pl-nav a").forEach(function (a) {
      a.addEventListener("click", function () { if (window.innerWidth < 1024) close(); });
    });
  }

  /* —— 2. 三方对照：手机端标签页切换 —— */
  function initCompareTabs() {
    document.querySelectorAll(".pl-compare").forEach(function (block) {
      var tabs = block.querySelector(".pl-compare-tabs");
      var cols = block.querySelector(".pl-cols");
      if (!tabs || !cols) return;
      var buttons = tabs.querySelectorAll("button");

      function show(target) {
        cols.classList.add("is-tabbed");
        cols.querySelectorAll(".pl-col").forEach(function (c) {
          c.classList.toggle("is-shown", c.getAttribute("data-pane") === target);
        });
        buttons.forEach(function (b) {
          b.setAttribute("aria-selected", b.getAttribute("data-target") === target ? "true" : "false");
        });
      }
      buttons.forEach(function (b) {
        b.addEventListener("click", function () { show(b.getAttribute("data-target")); });
      });

      // 依据视口初始化（仅手机端启用标签模式）
      var mq = window.matchMedia("(max-width: 767px)");
      function sync() {
        if (mq.matches) { show("anime"); }
        else {
          cols.classList.remove("is-tabbed");
          cols.querySelectorAll(".pl-col").forEach(function (c) { c.classList.remove("is-shown"); });
        }
      }
      mq.addEventListener ? mq.addEventListener("change", sync) : mq.addListener(sync);
      sync();
    });
  }

  /* —— 3. 回到顶部 —— */
  function initBackToTop() {
    var btn = document.querySelector(".pl-totop");
    if (!btn) return;
    window.addEventListener("scroll", function () {
      btn.classList.toggle("is-visible", window.scrollY > 600);
    }, { passive: true });
    btn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* —— 4. 当前页导航高亮 —— */
  function initActiveNav() {
    var here = location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll(".pl-nav a").forEach(function (a) {
      var href = (a.getAttribute("href") || "").split("/").pop().split("#")[0];
      if (href === here) a.classList.add("is-active");
    });
  }

  /* —— 5. ECharts：响应式重绘（图表实例由各页注册到 window.__plCharts）—— */
  function initChartResize() {
    window.__plCharts = window.__plCharts || [];
    var t;
    window.addEventListener("resize", function () {
      clearTimeout(t);
      t = setTimeout(function () {
        window.__plCharts.forEach(function (c) { try { c.resize(); } catch (e) {} });
      }, 180);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initNavDrawer();
    initCompareTabs();
    initBackToTop();
    initActiveNav();
    initChartResize();
  });
})();
