export interface TocItem {
  depth: number;
  text: string;
  slug: string;
}

export interface TocNode {
  depth: number;
  text: string;
  slug: string;
  children: TocNode[];
}

export interface ChapterNavItem {
  id: string;
  title: string;
  order: number;
  href: string;
  headings?: { depth: number; text: string; slug?: string }[];
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/[\s_]+/g, '-')
    .replace(/[^\p{Letter}\p{Number}\-]/gu, '')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '') || 'heading';
}

/** 为同一 slug 自增后缀，避免 id 冲突 */
export function ensureUnique(slug: string, seen: Map<string, number>): string {
  if (!seen.has(slug)) {
    seen.set(slug, 1);
    return slug;
  }
  const n = seen.get(slug)! + 1;
  seen.set(slug, n);
  return `${slug}-${n}`;
}

export function buildToc(headings: { depth: number; text: string; slug?: string }[] = []): TocItem[] {
  const out: TocItem[] = [];
  const seen = new Map<string, number>();
  for (const h of headings) {
    if (h.depth < 2 || h.depth > 4) continue;
    let slug = h.slug ?? slugify(h.text);
    slug = ensureUnique(slug, seen);
    out.push({ depth: h.depth, text: h.text, slug });
  }
  return out;
}

/** 把扁平的 headings 构建为层级树（h2 → h3/h4） */
export function buildTocTree(headings: { depth: number; text: string; slug?: string }[] = []): TocNode[] {
  const root: TocNode[] = [];
  const stack: TocNode[] = [];
  const seen = new Map<string, number>();
  for (const h of headings) {
    if (h.depth < 2 || h.depth > 4) continue;
    let slug = h.slug ?? slugify(h.text);
    slug = ensureUnique(slug, seen);
    const node: TocNode = { depth: h.depth, text: h.text, slug, children: [] };
    // 把栈中 depth >= 当前深度的节点弹出
    while (stack.length > 0 && stack[stack.length - 1].depth >= h.depth) {
      stack.pop();
    }
    if (stack.length === 0) {
      root.push(node);
    } else {
      stack[stack.length - 1].children.push(node);
    }
    stack.push(node);
  }
  return root;
}

/** 为右侧 TOC rail 渲染可折叠的层级 HTML（h2 可展开/收起 h3） */
export function renderTocForRail(
  headings: { depth: number; text: string; slug?: string }[] = [],
  opts: { mode?: 'rail' | 'popover' } = {},
): string {
  const tree = buildTocTree(headings);
  if (tree.length === 0) return '';

  const mode = opts.mode ?? 'rail';

  function renderList(nodes: TocNode[]): string {
    let html = '<ul class="toc-list">';
    for (const node of nodes) {
      const hasChildren = node.children.length > 0;
      html += `<li class="toc-item" data-depth="${node.depth}">`;
      html += `<div class="toc-row">`;
      if (hasChildren) {
        html += `<button type="button" class="toc-toggle" aria-expanded="false" aria-controls="toc-${node.slug}" aria-label="展开 ${escapeAttr(node.text)}"><span class="toc-toggle-icon">▸</span></button>`;
      } else {
        html += `<span class="toc-spacer" aria-hidden="true"></span>`;
      }
      html += `<a class="toc-link" href="#${node.slug}" data-target="#${node.slug}">${escapeHtml(node.text)}</a>`;
      html += `</div>`;
      if (hasChildren) {
        html += `<div class="toc-children" id="toc-${node.slug}" hidden>`;
        html += renderList(node.children);
        html += `</div>`;
      }
      html += `</li>`;
    }
    html += '</ul>';
    return html;
  }

  return `<div class="toc-rail-inner" data-mode="${mode}">${renderList(tree)}</div>`;
}

/** 作品章节目录 HTML：支持每章展开其大纲子项 */
export function renderChaptersNav(
  chapters: ChapterNavItem[],
  currentId: string,
  opts: { workTitle: string } = { workTitle: '' },
): string {
  let html = `<div class="chap-nav">`;
  html += `<div class="chap-nav-header"><span class="chap-nav-title">《${escapeHtml(opts.workTitle)}》章节</span></div>`;
  html += `<div class="chap-nav-actions">
    <button type="button" class="chap-action-btn" data-chap-action="expand-all" aria-label="展开全部章节">全部展开</button>
    <button type="button" class="chap-action-btn" data-chap-action="collapse-all" aria-label="收起全部章节">全部收起</button>
  </div>`;
  html += `<ol class="chap-list" role="list">`;
  for (const c of chapters) {
    const isActive = c.id === currentId;
    const headings = c.headings && c.headings.length > 0 ? c.headings : [];
    const hasSubItems = headings.length > 0;
    const safeId = `chap-${c.id.replace(/[^a-zA-Z0-9_-]/g, '-')}`;
    html += `<li class="chap-item ${isActive ? 'active' : ''}" data-chap-id="${escapeAttr(c.id)}">`;
    html += `<div class="chap-row">`;
    if (hasSubItems) {
      html += `<button type="button" class="chap-toggle" aria-expanded="false" aria-controls="${safeId}" aria-label="展开 ${escapeAttr(c.title)}"><span class="chap-toggle-icon">▸</span></button>`;
    } else {
      html += `<span class="chap-spacer" aria-hidden="true"></span>`;
    }
    html += `<a class="chap-link ${isActive ? 'active' : ''}" href="${escapeAttr(c.href)}">`;
    html += `<span class="chap-num">${String(c.order).padStart(2, '0')}</span>`;
    html += `<span class="chap-text">${escapeHtml(c.title)}</span>`;
    html += `</a>`;
    html += `</div>`;
    if (hasSubItems) {
      const subTree = buildTocTree(headings);
      html += `<div class="chap-sub" id="${safeId}" hidden>`;
      html += renderSubToc(subTree, c.href);
      html += `</div>`;
    }
    html += `</li>`;
  }
  html += `</ol>`;
  html += `</div>`;
  return html;
}

function renderSubToc(nodes: TocNode[], chapterHref: string): string {
  if (nodes.length === 0) return '';
  let html = '<ul class="chap-sub-list" role="list">';
  for (const n of nodes) {
    const subHasChildren = n.children.length > 0;
    const safeId = `chap-sub-${n.slug}`;
    html += `<li class="chap-sub-item" data-depth="${n.depth}">`;
    html += `<div class="chap-sub-row">`;
    if (subHasChildren) {
      html += `<button type="button" class="chap-sub-toggle" aria-expanded="false" aria-controls="${safeId}" aria-label="展开 ${escapeAttr(n.text)}"><span class="chap-sub-toggle-icon">▸</span></button>`;
    } else {
      html += `<span class="chap-spacer" aria-hidden="true"></span>`;
    }
    html += `<a class="chap-sub-link" href="${escapeAttr(chapterHref)}#${n.slug}">${escapeHtml(n.text)}</a>`;
    html += `</div>`;
    if (subHasChildren) {
      html += `<div class="chap-sub-children" id="${safeId}" hidden>${renderSubToc(n.children, chapterHref)}</div>`;
    }
    html += `</li>`;
  }
  html += '</ul>';
  return html;
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function escapeAttr(s: string): string {
  return escapeHtml(s);
}
