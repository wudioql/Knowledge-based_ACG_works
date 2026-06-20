/**
 * ACG Knowledge Handbook — Home Button Injector
 *
 * 在每个非首页页面右下角注入"返回主页"按钮，指向项目主页
 * （仓库根目录的 index.html）。
 *
 * 设计要点（为何不在 JS 里推算路径）：
 *   跳转路径由部署工作流（deploy.yml）在【构建期】按各文件所在目录深度
 *   计算好，写入本 <script> 标签的 data-home-href 属性，形如：
 *       <script src="../../_shared/home-button.js" data-home-href="../../index.html"></script>
 *   本脚本只需【读取】该属性，无需从 window.location 或硬编码仓库名推算。
 *   这样适配任意目录深度，且避免了旧实现里"把文件名误算成一层目录"
 *   与"仓库名写成分支名"两类 bug。
 *
 * 重复注入保护：若页面同时被「手动引用 + CI 注入」加载两次，
 * 只渲染一个按钮（旧实现会渲染两个）。
 */
(function () {
  'use strict';

  // 防重复渲染（手动引用与 CI 注入并存时，避免出现两个相同 id 的按钮）
  if (document.getElementById('home-button')) return;

  // 跳转路径由 CI 构建期算定；读不到时回退到当前目录（仅防御性兜底）
  var current = document.currentScript;
  var home =
    (current && current.getAttribute('data-home-href')) || './index.html';

  var btn = document.createElement('a');
  btn.id = 'home-button';
  btn.href = home;
  btn.title = '返回项目主页';
  btn.innerHTML =
    '<span aria-hidden="true">🏠</span><span class="home-label">主页</span>';
  document.body.appendChild(btn);
})();
