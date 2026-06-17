/**
 * ACG Knowledge Handbook — Home Button Injector
 * Automatically adds a "Home" button to all non-root pages
 * that navigates back to the project homepage.
 */
(function() {
  'use strict';

  // Don't inject on the project homepage itself
  var path = window.location.pathname;
  var repoName = 'acg-knowledge-handbook'; // Repository name for GitHub Pages

  // Detect if we're at root (project homepage)
  function isProjectHomepage() {
    // Check various possible root URL patterns for GitHub Pages
    var isRoot = path === '/' ||
                 path === '/index.html' ||
                 path.endsWith('/' + repoName + '/') ||
                 path.endsWith('/' + repoName + '/index.html');
    return isRoot;
  }

  if (isProjectHomepage()) return;

  // Calculate relative path to project root based on URL depth
  function getRootPath() {
    // For GitHub Pages: /repo-name/doc/work/page.html
    // We need to go up to /repo-name/
    var parts = path.split('/').filter(function(p) { return p; });

    // Find repo name index
    var repoIndex = parts.indexOf(repoName);
    if (repoIndex >= 0) {
      // Count segments after repo name
      var depth = parts.length - repoIndex - 1;
      return '../'.repeat(depth);
    }

    // Fallback: count all segments as depth
    var depth = parts.length;
    if (path.endsWith('.html')) depth--;
    return '../'.repeat(Math.max(1, depth));
  }

  // Create home button element
  var btn = document.createElement('a');
  btn.id = 'home-button';
  btn.href = getRootPath() + 'index.html';
  btn.innerHTML = '<span>🏠</span><span class="home-label">主页</span>';
  btn.title = '返回项目主页';

  // Append to body
  document.body.appendChild(btn);
})();
