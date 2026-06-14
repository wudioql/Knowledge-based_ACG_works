/* ============================================================
   全站通用导航 / 交互脚本
   ------------------------------------------------------------
   说明：
     initNavToggle()           桌面导航汉堡按钮开关 (.nav-toggle ↔ .site-nav)
     initSidebarToggles()      通用 sidebar 开关 ([data-sidebar-toggle] + .hamburger/#hamburger)
     initCollapsibles()        可展开块 (.collapsible-toggle / h3[data-collapsible])
     initBackToTop()           back-to-top 按钮（滚动 >400px 显示，点击回顶）
     initSideTocHighlight()    side-TOC 滚动高亮当前章节
     initSmoothScroll()        锚点平滑滚动
     initCuisineFilter()       料理分类筛选 (.filter-btn[data-filter] ↔ .dish-card[data-cuisine])
     initTocTreeExpand()       maoyuu toc-tree 的展开 / 折叠 (.toc-toggle ↔ .toc-children)
     initAutoToc()             根据 <section> 和 <h3> 自动生成左侧 toc-tree（maoyuu 专用）

   对外暴露的全局函数（供 HTML 内联 onclick 使用）：
     window.expandAll()        展开所有 toc-children / collapsible / h3
     window.collapseAll()      收起所有 toc-children / collapsible / h3
     window.toggleSection()    切换单个 .collapsible 的展开状态

   约定：
     - 使用 querySelector / querySelectorAll 查询元素
     - 查询不到对应元素时直接 return，避免无关页面报错
     - 全部采用 ES5 语法，可在 file:// 下直接双击 HTML 运行
   ============================================================ */

(function() {
    'use strict';

    // (a) 桌面导航汉堡按钮
    function initNavToggle() {
        var toggle = document.querySelector('.nav-toggle');
        var nav = document.querySelector('.site-nav');
        if (!toggle || !nav) return;

        toggle.addEventListener('click', function() {
            nav.classList.toggle('open');
            toggle.textContent = nav.classList.contains('open') ? '✕' : '☰';
        });
    }

    // (b) 通用 sidebar 开关：支持 [data-sidebar-toggle] + #hamburger 旧用法
    function initSidebarToggles() {
        var toggles = document.querySelectorAll('[data-sidebar-toggle]');
        var hamburger = document.querySelector('.hamburger, #hamburger');
        var sidebar = document.querySelector('.sidebar, .sidebar-toc');
        var overlay = document.querySelector('.sidebar-overlay');

        toggles.forEach(function(toggle) {
            var targetId = toggle.dataset ? toggle.dataset.target : toggle.getAttribute('data-target');
            var target = targetId ? document.getElementById(targetId) : (document.querySelector('.sidebar') || document.querySelector('.sidebar-toc'));
            if (!target) return;

            toggle.addEventListener('click', function() {
                target.classList.toggle('open');
                if (overlay) overlay.classList.toggle('open');
            });
        });

        if (hamburger && sidebar) {
            hamburger.addEventListener('click', function() {
                sidebar.classList.toggle('open');
                if (overlay) overlay.classList.toggle('open');
            });
        }
    }

    // (c) 可展开块
    function initCollapsibles() {
        var toggleBtns = document.querySelectorAll('.collapsible-toggle');
        var h3Toggles = document.querySelectorAll('h3[data-collapsible]');
        if (toggleBtns.length === 0 && h3Toggles.length === 0) return;

        toggleBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                var content = btn.nextElementSibling;
                if (!content) return;
                var isOpen = btn.classList.contains('open');

                btn.classList.toggle('open');
                content.classList.toggle('open');

                if (!isOpen) {
                    setTimeout(function() {
                        btn.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }, 100);
                }
            });
        });

        h3Toggles.forEach(function(h3) {
            h3.addEventListener('click', function() {
                var content = h3.nextElementSibling;
                while (content && !content.classList.contains('collapsible')) {
                    content = content.nextElementSibling;
                }
                if (!content) return;

                h3.classList.toggle('expanded');
                content.classList.toggle('expanded');
            });
        });
    }

    // (d) back-to-top 按钮
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

    // (e) side-TOC 当前章节高亮
    function initSideTocHighlight() {
        var tocContainer = document.querySelector('.side-toc, .sidebar-toc');
        if (!tocContainer) return;

        var tocLinks = tocContainer.querySelectorAll('a[href^="#"]');
        if (tocLinks.length === 0) return;

        var sections = [];
        tocLinks.forEach(function(link) {
            var href = link.getAttribute('href');
            if (!href || href === '#') return;
            var el = document.querySelector(href);
            if (el) sections.push({ el: el, link: link });
        });
        if (sections.length === 0) return;

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
            if (active) active.link.classList.add('active');
        }

        window.addEventListener('scroll', updateActive);
        updateActive();
    }

    // (f) 锚点平滑滚动
    function initSmoothScroll() {
        var links = document.querySelectorAll('a[href^="#"]');
        if (links.length === 0) return;

        links.forEach(function(link) {
            link.addEventListener('click', function(e) {
                var href = link.getAttribute('href');
                if (!href || href === '#') return;
                var target = document.querySelector(href);
                if (!target) return;
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });
        });
    }

    // (g) 料理筛选
    function initCuisineFilter() {
        var filterBtns = document.querySelectorAll('.filter-btn[data-filter]');
        var dishCards = document.querySelectorAll('.dish-card[data-cuisine]');
        if (filterBtns.length === 0 || dishCards.length === 0) return;

        filterBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                var cuisine = btn.getAttribute('data-filter');

                filterBtns.forEach(function(b) { b.classList.remove('active'); });
                btn.classList.add('active');

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

    // (h) maoyuu toc-tree 展开/折叠
    function initTocTreeExpand() {
        var toggles = document.querySelectorAll('.toc-toggle');
        if (toggles.length === 0) return;

        toggles.forEach(function(toggle) {
            toggle.addEventListener('click', function(e) {
                if (e) e.stopPropagation();
                // 如果这是叶子节点，不做任何折叠操作
                if (toggle.classList.contains('leaf')) return;

                // 找到对应的 .toc-children（兄弟节点，或父节点内的子节点列表）
                var children = null;
                // 优先查找兄弟节点（node 结构中 toggle 是 node 的子元素，node 的兄弟是 toc-children）
                var parent = toggle.parentNode;
                if (parent) {
                    // 在同级兄弟中寻找 toc-children
                    var sibling = parent.nextElementSibling;
                    while (sibling) {
                        if (sibling.classList.contains('toc-children')) {
                            children = sibling;
                            break;
                        }
                        sibling = sibling.nextElementSibling;
                    }
                    // 如果未找到，则退回到在整个父 li 中查找
                    if (!children) {
                        var container = parent.parentNode;
                        if (container) {
                            children = container.querySelector(':scope > .toc-children');
                        }
                    }
                }
                if (!children) return;

                var isExpanded = children.classList.contains('expanded');
                if (isExpanded) {
                    toggle.classList.remove('expanded');
                    children.classList.remove('expanded');
                } else {
                    toggle.classList.add('expanded');
                    children.classList.add('expanded');
                }
            });
        });
    }

    // (i) 根据页面内容自动生成左侧 toc-tree（maoyuu 专用）
    // 规则：<section id="xxx"> 的第一个 <h2> 文本 → 一级节点；
    //       <section> 内的 <h3 id="yyy"> → 二级节点。
    function initAutoToc() {
        var tocTree = document.getElementById('tocTree');
        var main = document.getElementById('mainContent');
        if (!tocTree || !main) return;
        if (tocTree.children.length > 0) return; // 已有内容，跳过

        var sections = main.querySelectorAll('section[id]');
        if (sections.length === 0) return;

        for (var i = 0; i < sections.length; i++) {
            var sec = sections[i];
            var secId = sec.getAttribute('id');
            var h2 = sec.querySelector('h2');
            var secTitle = h2 ? h2.textContent.trim() : secId;

            // 子节点：所有 h3[id]（不递归到子 section）
            var subNodes = [];
            var directChildren = sec.children;
            for (var j = 0; j < directChildren.length; j++) {
                var child = directChildren[j];
                if (child.tagName === 'H3' && child.getAttribute('id')) {
                    subNodes.push({
                        id: child.getAttribute('id'),
                        title: child.textContent.replace(/^\s*▶\s*/, '').trim()
                    });
                }
            }

            var li = document.createElement('li');
            li.className = 'level-1';

            var node = document.createElement('div');
            node.className = 'toc-node';
            node.setAttribute('data-target', secId);

            var toggle = document.createElement('span');
            toggle.className = 'toc-toggle' + (subNodes.length === 0 ? ' leaf' : '');
            toggle.textContent = '▶';

            var textSpan = document.createElement('span');
            textSpan.textContent = secTitle;

            node.appendChild(toggle);
            node.appendChild(textSpan);

            // 点击行为
            (function(secIdInner, hasChildrenInner, toggleInner) {
                node.addEventListener('click', function(e) {
                    // 展开/收起子项
                    if (hasChildrenInner) {
                        var childrenUl = node.nextElementSibling;
                        if (childrenUl && childrenUl.classList.contains('toc-children')) {
                            var isOpen = toggleInner.classList.contains('expanded');
                            if (isOpen) {
                                toggleInner.classList.remove('expanded');
                                childrenUl.classList.remove('expanded');
                            } else {
                                toggleInner.classList.add('expanded');
                                childrenUl.classList.add('expanded');
                            }
                        }
                    }
                    // 跳转目标 section
                    var target = document.getElementById(secIdInner);
                    if (target) {
                        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                });
            })(secId, subNodes.length > 0, toggle);

            li.appendChild(node);

            if (subNodes.length > 0) {
                var childrenUl = document.createElement('ul');
                childrenUl.className = 'toc-children';
                // 不使用 style.display，让 CSS 的 expanded 类控制显示

                for (var k = 0; k < subNodes.length; k++) {
                    var sub = subNodes[k];
                    var childLi = document.createElement('li');
                    childLi.className = 'level-2';

                    var childNode = document.createElement('div');
                    childNode.className = 'toc-node';
                    childNode.setAttribute('data-target', sub.id);

                    var childToggle = document.createElement('span');
                    childToggle.className = 'toc-toggle leaf';

                    var childText = document.createElement('span');
                    childText.textContent = sub.title;

                    childNode.appendChild(childToggle);
                    childNode.appendChild(childText);

                    (function(subIdInner) {
                        childNode.addEventListener('click', function() {
                            var target = document.getElementById(subIdInner);
                            if (target) {
                                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                            }
                        });
                    })(sub.id);

                    childLi.appendChild(childNode);
                    childrenUl.appendChild(childLi);
                }

                li.appendChild(childrenUl);
            }

            tocTree.appendChild(li);
        }
    }

    // (j) 滚动高亮 —— 对 toc-tree 的通用版本
    function initTocTreeHighlight() {
        var tocNodes = document.querySelectorAll('#tocTree .toc-node[data-target]');
        if (tocNodes.length === 0) return;

        var sections = [];
        for (var i = 0; i < tocNodes.length; i++) {
            var node = tocNodes[i];
            var id = node.getAttribute('data-target');
            var el = id ? document.getElementById(id) : null;
            if (el) sections.push({ el: el, node: node });
        }
        if (sections.length === 0) return;

        var ticking = false;
        function update() {
            var scrollPos = window.scrollY + 120;
            var activeIdx = -1;
            for (var i = 0; i < sections.length; i++) {
                if (sections[i].el.offsetTop <= scrollPos) {
                    activeIdx = i;
                }
            }
            for (var j = 0; j < tocNodes.length; j++) {
                tocNodes[j].classList.remove('active');
            }
            if (activeIdx >= 0) {
                sections[activeIdx].node.classList.add('active');
            }
            ticking = false;
        }

        window.addEventListener('scroll', function() {
            if (!ticking) {
                window.requestAnimationFrame(update);
                ticking = true;
            }
        });
        update();
    }

    // --- 全局函数（供 HTML onclick 使用） ---
    window.expandAll = function() {
        var children = document.querySelectorAll('.toc-children');
        for (var i = 0; i < children.length; i++) {
            children[i].classList.add('expanded');
        }
        var toggles = document.querySelectorAll('.toc-toggle:not(.leaf)');
        for (var j = 0; j < toggles.length; j++) {
            toggles[j].classList.add('expanded');
        }
        var collapsibles = document.querySelectorAll('.collapsible');
        for (var k = 0; k < collapsibles.length; k++) {
            collapsibles[k].classList.add('expanded');
        }
        var headings = document.querySelectorAll('h3');
        for (var m = 0; m < headings.length; m++) {
            headings[m].classList.add('expanded');
        }
    };

    window.collapseAll = function() {
        var children = document.querySelectorAll('.toc-children');
        for (var i = 0; i < children.length; i++) {
            children[i].classList.remove('expanded');
        }
        var toggles = document.querySelectorAll('.toc-toggle');
        for (var j = 0; j < toggles.length; j++) {
            toggles[j].classList.remove('expanded');
        }
        var collapsibles = document.querySelectorAll('.collapsible');
        for (var k = 0; k < collapsibles.length; k++) {
            collapsibles[k].classList.remove('expanded');
        }
        var headings = document.querySelectorAll('h3');
        for (var m = 0; m < headings.length; m++) {
            headings[m].classList.remove('expanded');
        }
    };

    window.toggleSection = function(contentId, headingEl) {
        var content = document.getElementById(contentId);
        if (!content) return;
        var isCollapsed = !content.classList.contains('expanded');
        // 若未使用 expanded 类（例如部分页面用 style.display），再回退到 style 检测
        if (!content.classList.contains('collapsible') && !isCollapsed) {
            isCollapsed = (content.style.display === 'none' || content.style.display === '');
        }
        if (isCollapsed) {
            content.classList.add('expanded');
            if (headingEl) headingEl.classList.add('expanded');
        } else {
            content.classList.remove('expanded');
            if (headingEl) headingEl.classList.remove('expanded');
        }
    };

    // --- DOMContentLoaded 后统一初始化 ---
    document.addEventListener('DOMContentLoaded', function() {
        initNavToggle();
        initSidebarToggles();
        initCollapsibles();
        initBackToTop();
        initSideTocHighlight();
        initSmoothScroll();
        initCuisineFilter();
        initAutoToc();
        initTocTreeExpand();
        initTocTreeHighlight();
    });

})();
