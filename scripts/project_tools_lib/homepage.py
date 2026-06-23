from __future__ import annotations

from copy import deepcopy
from math import cos, pi, sin
from pathlib import Path

from .common import (
    CONTENT_PREFIXES,
    DATA_PATH,
    DEFAULT_DOMAIN_ID,
    DEFAULT_DOMAIN_LABEL,
    DEFAULT_MEDIUM_ID,
    DEFAULT_MEDIUM_LABEL,
    DOCS_ROOT,
    HANDBOOKS_PATH,
    METRICS_PATH,
    OUTPUT_PATH,
    ROOT,
    SUPPORT_PREFIXES,
    e,
    load_json,
    render_links,
    save_json,
    unique,
)

HERO_SVG = """<svg viewBox=\"0 0 520 420\" role=\"img\" aria-label=\"知识图谱示意图\">\n  <defs>\n    <linearGradient id=\"atlasPanel\" x1=\"0\" x2=\"1\">\n      <stop offset=\"0%\" stop-color=\"#f7f4ec\"/>\n      <stop offset=\"100%\" stop-color=\"#fbf8f1\"/>\n    </linearGradient>\n  </defs>\n  <rect x=\"12\" y=\"12\" width=\"496\" height=\"396\" rx=\"28\" fill=\"url(#atlasPanel)\" stroke=\"#d8d0be\"/>\n  <g opacity=\"0.10\" stroke=\"#1f2d44\">\n    <path d=\"M40 88H480\" />\n    <path d=\"M40 158H480\" />\n    <path d=\"M40 228H480\" />\n    <path d=\"M40 298H480\" />\n    <path d=\"M40 368H480\" />\n    <path d=\"M86 40V380\" />\n    <path d=\"M173 40V380\" />\n    <path d=\"M260 40V380\" />\n    <path d=\"M347 40V380\" />\n    <path d=\"M434 40V380\" />\n  </g>\n  <g stroke=\"#8da1bd\" stroke-width=\"2\" opacity=\"0.75\" fill=\"none\">\n    <path d=\"M260 205L124 92\"/>\n    <path d=\"M260 205L395 92\"/>\n    <path d=\"M260 205L110 186\"/>\n    <path d=\"M260 205L410 186\"/>\n    <path d=\"M260 205L124 320\"/>\n    <path d=\"M260 205L395 320\"/>\n  </g>\n  <g>\n    <rect x=\"172\" y=\"158\" width=\"176\" height=\"96\" rx=\"20\" fill=\"#18273b\" stroke=\"#c49a35\" stroke-width=\"3\"/>\n    <text x=\"260\" y=\"188\" text-anchor=\"middle\" fill=\"#f3eee0\" font-size=\"18\" font-weight=\"700\">ACG 知识手册库</text>\n    <text x=\"260\" y=\"214\" text-anchor=\"middle\" fill=\"#d7c48a\" font-size=\"12\" font-weight=\"700\">WORKS · DOMAINS · PATHS</text>\n    <text x=\"260\" y=\"238\" text-anchor=\"middle\" fill=\"#9bb0ca\" font-size=\"11\">MULTI-DOMAIN · MULTI-MEDIUM</text>\n  </g>\n  <g>\n    <rect x=\"45\" y=\"54\" width=\"150\" height=\"58\" rx=\"18\" fill=\"#ffffff\" stroke=\"#16867f\" stroke-width=\"3\"/>\n    <text x=\"120\" y=\"79\" text-anchor=\"middle\" fill=\"#16867f\" font-size=\"13\" font-weight=\"700\">生命、医学</text>\n    <text x=\"120\" y=\"98\" text-anchor=\"middle\" fill=\"#16867f\" font-size=\"13\" font-weight=\"700\">与公共卫生</text>\n  </g>\n  <g>\n    <rect x=\"325\" y=\"54\" width=\"150\" height=\"58\" rx=\"18\" fill=\"#ffffff\" stroke=\"#bf6d22\" stroke-width=\"3\"/>\n    <text x=\"400\" y=\"79\" text-anchor=\"middle\" fill=\"#bf6d22\" font-size=\"13\" font-weight=\"700\">食物、料理</text>\n    <text x=\"400\" y=\"98\" text-anchor=\"middle\" fill=\"#bf6d22\" font-size=\"13\" font-weight=\"700\">与食材</text>\n  </g>\n  <g>\n    <rect x=\"28\" y=\"156\" width=\"154\" height=\"60\" rx=\"18\" fill=\"#ffffff\" stroke=\"#5b8a2f\" stroke-width=\"3\"/>\n    <text x=\"105\" y=\"180\" text-anchor=\"middle\" fill=\"#5b8a2f\" font-size=\"12\" font-weight=\"700\">微生物、发酵</text>\n    <text x=\"105\" y=\"199\" text-anchor=\"middle\" fill=\"#5b8a2f\" font-size=\"12\" font-weight=\"700\">与农食系统</text>\n  </g>\n  <g>\n    <rect x=\"338\" y=\"156\" width=\"154\" height=\"60\" rx=\"18\" fill=\"#ffffff\" stroke=\"#b34f72\" stroke-width=\"3\"/>\n    <text x=\"415\" y=\"180\" text-anchor=\"middle\" fill=\"#b34f72\" font-size=\"12\" font-weight=\"700\">政治、经济</text>\n    <text x=\"415\" y=\"199\" text-anchor=\"middle\" fill=\"#b34f72\" font-size=\"12\" font-weight=\"700\">与制度</text>\n  </g>\n  <g>\n    <rect x=\"45\" y=\"292\" width=\"150\" height=\"58\" rx=\"18\" fill=\"#ffffff\" stroke=\"#7b4f2a\" stroke-width=\"3\"/>\n    <text x=\"120\" y=\"317\" text-anchor=\"middle\" fill=\"#7b4f2a\" font-size=\"13\" font-weight=\"700\">历史、文明</text>\n    <text x=\"120\" y=\"336\" text-anchor=\"middle\" fill=\"#7b4f2a\" font-size=\"13\" font-weight=\"700\">与社会结构</text>\n  </g>\n  <g>\n    <rect x=\"325\" y=\"292\" width=\"150\" height=\"58\" rx=\"18\" fill=\"#ffffff\" stroke=\"#4f73d2\" stroke-width=\"3\"/>\n    <text x=\"400\" y=\"317\" text-anchor=\"middle\" fill=\"#4f73d2\" font-size=\"13\" font-weight=\"700\">科幻、工程</text>\n    <text x=\"400\" y=\"336\" text-anchor=\"middle\" fill=\"#4f73d2\" font-size=\"13\" font-weight=\"700\">与宇宙</text>\n  </g>\n</svg>"""

# ... rest of file unchanged below ...


def discover_html_files(folder: str) -> list[Path]:
    work_dir = DOCS_ROOT / folder
    if not work_dir.exists():
        return []
    return sorted(work_dir.glob("*.html"))


def analyze_handbook_pages(folder: str) -> dict[str, object]:
    files = discover_html_files(folder)
    total = len(files)
    content_pages = 0
    support_pages = 0
    other_pages = 0
    first_content: str | None = None

    for file in files:
        stem = file.stem
        if stem == "index":
            continue
        if stem.startswith(CONTENT_PREFIXES):
            content_pages += 1
            first_content = first_content or file.name
        elif stem.startswith(SUPPORT_PREFIXES) or stem in SUPPORT_PREFIXES:
            support_pages += 1
        else:
            other_pages += 1
            first_content = first_content or file.name

    content_like_pages = content_pages + other_pages
    return {
        "totalPages": total,
        "contentPages": content_pages,
        "contentLikePages": content_like_pages,
        "supportPages": support_pages,
        "otherPages": other_pages,
        "firstContentPage": first_content,
    }


def build_label_maps(data: dict[str, object]) -> tuple[dict[str, str], dict[str, str], dict[str, int]]:
    domain_labels = {domain["id"]: domain["title"] for domain in data["domains"]}
    domain_labels.setdefault(DEFAULT_DOMAIN_ID, DEFAULT_DOMAIN_LABEL)
    domain_order = {domain["id"]: index for index, domain in enumerate(data["domains"])}
    medium_labels = {
        item["value"]: item["label"]
        for item in data["filters"]["medium"]
        if item["value"] != "all"
    }
    medium_labels.setdefault(DEFAULT_MEDIUM_ID, DEFAULT_MEDIUM_LABEL)
    return domain_labels, medium_labels, domain_order


HERO_THEME_COLORS = {
    "life": "#16867f",
    "food": "#bf6d22",
    "micro": "#5b8a2f",
    "society": "#b34f72",
    "history": "#7b4f2a",
    "space": "#4f73d2",
    "misc": "#7a6e58",
}


def split_title_lines(title: str) -> list[str]:
    if "、" in title:
        left, right = title.split("、", 1)
        return [left + "、", right]
    if "与" in title and len(title) > 6:
        left, right = title.split("与", 1)
        return [left + "与", right]
    if len(title) > 8:
        middle = len(title) // 2
        return [title[:middle], title[middle:]]
    return [title]


def render_hero_node_text(x: int, y: int, title: str, color: str) -> str:
    lines = split_title_lines(title)
    start_y = y - (len(lines) - 1) * 9
    tspans = []
    for index, line in enumerate(lines):
        tspans.append(f'<tspan x="{x}" y="{start_y + index * 18}">{e(line)}</tspan>')
    return (
        f'<text class="atlas-hero-node-text" x="{x}" y="{y}" text-anchor="middle" '
        f'fill="{color}" font-size="13" font-weight="700">{"".join(tspans)}</text>'
    )


def render_hero_svg(domains: list[dict[str, object]]) -> str:
    center_x, center_y = 260, 215
    node_w, node_h = 162, 66
    radius = 158
    total = max(len(domains), 1)

    positions: list[tuple[int, int]] = []
    for index in range(total):
        angle = (-pi / 2) + (2 * pi * index / total)
        x = int(center_x + cos(angle) * radius)
        y = int(center_y + sin(angle) * radius)
        positions.append((x, y))

    line_paths: list[str] = []
    node_blocks: list[str] = []
    for index, domain in enumerate(domains):
        x, y = positions[index]
        theme = str(domain.get("theme", "misc"))
        color = HERO_THEME_COLORS.get(theme, HERO_THEME_COLORS["misc"])
        ctrl_x = int((center_x + x) / 2)
        ctrl_y = int((center_y + y) / 2 + (-18 if y < center_y else 12))
        line_paths.append(
            f'<path class="atlas-hero-line delay-{(index % 4) + 1}" d="M {center_x} {center_y} Q {ctrl_x} {ctrl_y} {x} {y}" />'
        )
        card_x = x - node_w // 2
        card_y = y - node_h // 2
        node_blocks.append(
            "<g class=\"atlas-hero-node delay-%d\">" % ((index % 4) + 1)
            + f'<rect class="atlas-hero-node-card" x="{card_x}" y="{card_y}" width="{node_w}" height="{node_h}" rx="18" fill="#ffffff" stroke="{color}" stroke-width="3" />'
            + render_hero_node_text(x, y, str(domain["title"]), color)
            + "</g>"
        )

    return (
        '<svg class="atlas-hero-svg" viewBox="0 0 520 420" role="img" aria-label="与知识地图同步的首页知识结构示意图">'
        '<g class="atlas-hero-grid" opacity="0.11" stroke="#1f2d44">'
        '<path d="M40 78H480" /><path d="M40 148H480" /><path d="M40 218H480" /><path d="M40 288H480" /><path d="M40 358H480" />'
        '<path d="M86 30V390" /><path d="M173 30V390" /><path d="M260 30V390" /><path d="M347 30V390" /><path d="M434 30V390" />'
        '</g>'
        '<g fill="none">' + ''.join(line_paths) + '</g>'
        '<g class="atlas-hero-core">'
        f'<circle cx="{center_x}" cy="{center_y}" r="72" fill="#fffdf7" stroke="#c49a35" stroke-width="3" />'
        f'<circle cx="{center_x}" cy="{center_y}" r="48" fill="#f7f3e6" stroke="#d8d0be" />'
        f'<text x="{center_x}" y="{center_y - 12}" text-anchor="middle" fill="#162337" font-size="17" font-weight="800">知识地图</text>'
        f'<text x="{center_x}" y="{center_y + 12}" text-anchor="middle" fill="#6b5d3c" font-size="11" font-weight="700">DOMAINS · MEDIA · PATHS</text>'
        f'<text x="{center_x}" y="{center_y + 34}" text-anchor="middle" fill="#8f97aa" font-size="10">AUTO-SYNC WITH HOMEPAGE DATA</text>'
        '</g>'
        + ''.join(node_blocks)
        + '</svg>'
    )


def normalize_domains(raw_domain: object, domain_labels: dict[str, str]) -> list[str]:
    if raw_domain is None:
        return [DEFAULT_DOMAIN_ID]
    values = [raw_domain] if isinstance(raw_domain, str) else list(raw_domain)
    normalized: list[str] = []
    for value in values:
        domain = str(value).strip()
        if not domain or domain not in domain_labels:
            domain = DEFAULT_DOMAIN_ID
        normalized.append(domain)
    return unique(normalized or [DEFAULT_DOMAIN_ID])


def normalize_mediums(raw_medium: object, medium_labels: dict[str, str]) -> list[str]:
    if raw_medium is None:
        return [DEFAULT_MEDIUM_ID]
    values = [raw_medium] if isinstance(raw_medium, str) else list(raw_medium)
    normalized: list[str] = []
    for value in values:
        medium = str(value).strip()
        if not medium or medium not in medium_labels:
            medium = DEFAULT_MEDIUM_ID
        normalized.append(medium)
    return unique(normalized or [DEFAULT_MEDIUM_ID])


def infer_scale(entry: dict[str, object], page_stats: dict[str, object]) -> str:
    if entry.get("scale"):
        return str(entry["scale"])
    total = int(page_stats["totalPages"])
    content_like = int(page_stats["contentLikePages"])
    support = int(page_stats["supportPages"])
    if total == 0:
        return "已收录页面待补充"
    details: list[str] = []
    if content_like:
        details.append(f"{content_like} 个内容页")
    if support:
        details.append(f"{support} 个辅助页")
    if details:
        return f"共 {total} 个页面（含 {'，'.join(details)}）"
    return f"共 {total} 个页面"


def infer_structure(entry: dict[str, object], page_stats: dict[str, object]) -> str:
    if entry.get("structure"):
        return str(entry["structure"])
    total = int(page_stats["totalPages"])
    content_like = int(page_stats["contentLikePages"])
    support = int(page_stats["supportPages"])
    if total == 0:
        return "目录结构待整理。"
    parts = ["目录页"]
    if content_like:
        parts.append(f"{content_like} 个内容页")
    if support:
        parts.append(f"{support} 个辅助页")
    return " + ".join(parts) + "。"


def infer_start_here(entry: dict[str, object], page_stats: dict[str, object]) -> str:
    if entry.get("startHere"):
        return str(entry["startHere"])
    if page_stats.get("firstContentPage"):
        return "先从作品首页开始，再进入首个内容页。"
    return "先从作品首页开始。"


def normalize_handbooks(data: dict[str, object], registry: list[dict[str, object]]) -> list[dict[str, object]]:
    domain_labels, medium_labels, domain_order = build_label_maps(data)
    works: list[dict[str, object]] = []

    for index, entry in enumerate(registry):
        folder = str(entry["folder"]).strip()
        title = str(entry["title"]).strip()
        raw_domains = entry.get("domains", entry.get("domain"))
        domains = normalize_domains(raw_domains, domain_labels)
        primary_domain = next((domain for domain in domains if domain != DEFAULT_DOMAIN_ID), domains[0])
        medium_codes = normalize_mediums(entry.get("medium"), medium_labels)
        page_stats = analyze_handbook_pages(folder)
        page_count = int(page_stats["totalPages"])
        href = str(entry.get("href") or f"doc/{folder}/index.html")
        tags = [str(tag) for tag in (entry.get("tags") or [])]
        chips = entry.get("chips") or unique([
            *(medium_labels.get(code, DEFAULT_MEDIUM_LABEL) for code in medium_codes),
            *tags,
        ])
        scale = infer_scale(entry, page_stats)
        structure = infer_structure(entry, page_stats)
        start_here = infer_start_here(entry, page_stats)
        summary = str(entry.get("summary") or "进入该作品手册总览。")
        subtitle = str(entry.get("subtitle") or "知识手册")
        cta = str(entry.get("cta") or f"进入《{title}》手册")
        explicit_order = entry.get("order")
        auto_order = domain_order.get(primary_domain, len(domain_order)) * 1000 + index
        sort_order = explicit_order if explicit_order is not None else auto_order
        works.append(
            {
                "folder": folder,
                "title": title,
                "sub": subtitle,
                "summary": summary,
                "domain": primary_domain,
                "domains": domains,
                "domainLabel": entry.get("domainLabel") or domain_labels.get(primary_domain, DEFAULT_DOMAIN_LABEL),
                "medium": medium_codes,
                "chips": chips,
                "meta": [
                    {"term": "规模", "value": scale},
                    {"term": "结构亮点", "value": structure},
                    {"term": "从这里开始", "value": start_here},
                ],
                "href": href,
                "cta": cta,
                "pageCount": page_count,
                "pageStats": page_stats,
                "order": sort_order,
            }
        )

    return sorted(works, key=lambda item: (item["order"], item["title"]))


def build_filters(data: dict[str, object], works: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    domain_labels, medium_labels, _ = build_label_maps(data)
    filters = deepcopy(data["filters"])

    used_domains = {domain for work in works for domain in work["domains"] if domain != "all"}
    known_domain_values = {item["value"] for item in filters["domain"]}
    for value in sorted(used_domains - known_domain_values):
        filters["domain"].append({"label": domain_labels.get(value, DEFAULT_DOMAIN_LABEL), "value": value})

    used_mediums = {medium for work in works for medium in work["medium"] if medium != "all"}
    known_medium_values = {item["value"] for item in filters["medium"]}
    for value in sorted(used_mediums - known_medium_values):
        filters["medium"].append({"label": medium_labels.get(value, DEFAULT_MEDIUM_LABEL), "value": value})

    return filters


def build_domains(data: dict[str, object], works: list[dict[str, object]]) -> list[dict[str, object]]:
    rendered_domains: list[dict[str, object]] = []
    for domain in data["domains"]:
        domain_works = [work for work in works if domain["id"] in work["domains"]]
        entries = [{"label": f"从《{work['title']}》进入", "href": work["href"]} for work in domain_works]
        page_total = sum(work["pageCount"] for work in domain_works)
        count_text = f"{len(entries)} 部作品"
        if page_total:
            count_text += f" · {page_total} 个页面"
        if domain.get("countHint"):
            count_text += f" · {domain['countHint']}"
        rendered = dict(domain)
        rendered["count"] = count_text
        rendered["entries"] = entries
        rendered_domains.append(rendered)

    uncategorized_works = [work for work in works if DEFAULT_DOMAIN_ID in work["domains"]]
    if uncategorized_works:
        page_total = sum(work["pageCount"] for work in uncategorized_works)
        rendered_domains.append(
            {
                "id": DEFAULT_DOMAIN_ID,
                "theme": "misc",
                "code": "DOMAIN 00",
                "title": DEFAULT_DOMAIN_LABEL,
                "summary": "当新手册尚未补充完整领域信息时，会先在这里兜底展示，以保证它仍能进入首页系统。",
                "keywords": ["待补充", "未归类", "低成本接入"],
                "count": f"{len(uncategorized_works)} 部作品 · {page_total} 个页面 · 等待补充领域信息",
                "entries": [{"label": f"从《{work['title']}》进入", "href": work["href"]} for work in uncategorized_works],
            }
        )

    return rendered_domains


def build_project_metrics(works: list[dict[str, object]], domains: list[dict[str, object]]) -> dict[str, object]:
    domain_counts = {domain["id"]: 0 for domain in domains}
    domain_page_counts = {domain["id"]: 0 for domain in domains}
    medium_counts: dict[str, int] = {}
    total_content_like = 0
    total_support = 0
    uncategorized = 0
    fallback_medium = 0
    handbook_summaries = []

    for work in works:
        page_stats = work["pageStats"]
        for domain in work["domains"]:
            if domain in domain_counts:
                domain_counts[domain] += 1
                domain_page_counts[domain] += work["pageCount"]
        if DEFAULT_DOMAIN_ID in work["domains"]:
            uncategorized += 1
        if DEFAULT_MEDIUM_ID in work["medium"]:
            fallback_medium += 1
        for medium in work["medium"]:
            medium_counts[medium] = medium_counts.get(medium, 0) + 1
        total_content_like += int(page_stats["contentLikePages"])
        total_support += int(page_stats["supportPages"])
        handbook_summaries.append(
            {
                "folder": work["folder"],
                "title": work["title"],
                "domain": work["domain"],
                "domains": work["domains"],
                "medium": work["medium"],
                "pageCount": work["pageCount"],
                "contentLikePages": int(page_stats["contentLikePages"]),
                "supportPages": int(page_stats["supportPages"]),
            }
        )

    return {
        "totalHandbooks": len(works),
        "totalPages": sum(work.get("pageCount", 0) for work in works),
        "totalDomains": len(domains),
        "totalContentLikePages": total_content_like,
        "totalSupportPages": total_support,
        "uncategorizedHandbooks": uncategorized,
        "fallbackMediumHandbooks": fallback_medium,
        "domainCounts": domain_counts,
        "domainPageCounts": domain_page_counts,
        "mediumCounts": medium_counts,
        "registeredFolders": [work["folder"] for work in works],
        "handbooks": handbook_summaries,
    }


def sync_hero_stats(site: dict[str, object], metrics: dict[str, object]) -> dict[str, object]:
    hero = deepcopy(site["hero"])
    auto_values = {
        "AUTO_WORKS": str(metrics["totalHandbooks"]),
        "AUTO_PAGES": str(metrics["totalPages"]),
        "AUTO_DOMAINS": str(metrics["totalDomains"]),
        "AUTO_CONTENT_PAGES": str(metrics["totalContentLikePages"]),
        "AUTO_SUPPORT_PAGES": str(metrics["totalSupportPages"]),
    }
    for item in hero.get("stats", []):
        value = str(item.get("value", ""))
        if value in auto_values:
            item["value"] = auto_values[value]
    site = dict(site)
    site["hero"] = hero
    return site


def build_runtime_data() -> tuple[dict[str, object], list[dict[str, object]], dict[str, list[dict[str, object]]], list[dict[str, object]], dict[str, object]]:
    data = load_json(DATA_PATH)
    registry = load_json(HANDBOOKS_PATH)
    works = normalize_handbooks(data, registry)
    filters = build_filters(data, works)
    domains = build_domains(data, works)
    metrics = build_project_metrics(works, domains)
    return data, works, filters, domains, metrics


def render_header(site: dict[str, object]) -> str:
    nav_links = render_links(site["nav"])
    return f"""<header class="atlas-header" id="top">
  <div class="atlas-shell atlas-header__inner">
    <a class="atlas-brand" href="index.html" aria-label="回到 ACG 知识手册库首页">
      <span class="atlas-brand__mark" aria-hidden="true">◎</span>
      <span class="atlas-brand__text">
        <strong>{e(site['brandTitle'])}</strong>
        <small>{e(site['brandSubtitle'])}</small>
      </span>
    </a>

    <button class="atlas-nav-toggle" type="button" aria-expanded="false" aria-controls="atlas-nav">菜单</button>

    <nav class="atlas-nav" id="atlas-nav" aria-label="首页导航">
      {nav_links}
    </nav>
  </div>
</header>"""


def render_hero(site: dict[str, object], domains: list[dict[str, object]]) -> str:
    hero = site["hero"]
    actions = "\n".join(
        f'<a class="atlas-button atlas-button--{e(item["style"])}" href="{e(item["href"])}">{e(item["label"])}</a>'
        for item in hero["actions"]
    )
    stats = "\n".join(
        f'<li><strong>{e(item["value"])}</strong><span>{e(item["label"])}</span></li>'
        for item in hero["stats"]
    )
    entry_modes = "\n".join(
        f'<article class="atlas-entry-mode"><h2>{e(item["title"])}</h2><p>{e(item["text"])}</p></article>'
        for item in hero["entryModes"]
    )
    lead = e(hero["lead"]).replace("可阅读、可导航、可延伸", "<strong>可阅读、可导航、可延伸</strong>")
    return f"""<section class="atlas-hero">
  <div class="atlas-shell atlas-hero__grid">
    <div class="atlas-hero__copy">
      <p class="atlas-eyebrow">{e(hero['eyebrow'])}</p>
      <h1>{e(hero['title'])}</h1>
      <p class="atlas-hero__lead">{lead}</p>
      <p class="atlas-hero__body">{e(hero['body'])}</p>

      <div class="atlas-actions">
        {actions}
      </div>

      <ul class="atlas-stats" aria-label="当前收录规模">
        {stats}
      </ul>

      <div class="atlas-entry-modes" aria-label="首页使用方式">
        {entry_modes}
      </div>
    </div>

    <div class="atlas-hero__art" aria-hidden="true">
      {render_hero_svg(domains)}
    </div>
  </div>
</section>"""


def render_project_pulse(metrics: dict[str, object]) -> str:
    classification_status = (
        "分类信息完整"
        if metrics["uncategorizedHandbooks"] == 0 and metrics["fallbackMediumHandbooks"] == 0
        else "仍有待补充项"
    )
    summary_items = [
        ("手册目录", str(metrics["totalHandbooks"]), "已登记作品入口"),
        ("内容结构", f"{metrics['totalContentLikePages']} / {metrics['totalSupportPages']}", "内容页 / 辅助页"),
        ("分类状态", str(metrics["uncategorizedHandbooks"]), "待归类手册"),
        ("接入成本", "folder + title", "最低可用登记方式"),
    ]
    cards = "\n".join(
        f'''<article class="atlas-pulse-card">\n  <p class="atlas-pulse-card__label">{e(label)}</p>\n  <strong>{e(value)}</strong>\n  <span>{e(desc)}</span>\n</article>'''
        for label, value, desc in summary_items
    )
    status_class = "is-clean" if classification_status == "分类信息完整" else "is-warning"
    medium_note = (
        f"兜底媒介 {metrics['fallbackMediumHandbooks']} 个"
        if metrics["fallbackMediumHandbooks"]
        else "无兜底媒介项"
    )
    return f"""<section class="atlas-pulse" aria-label="项目摘要与自动统计">
  <div class="atlas-shell atlas-pulse__inner">
    <div class="atlas-pulse__intro">
      <p class="atlas-section__kicker">Project Pulse</p>
      <h2>项目摘要</h2>
      <p>首页统计由注册表和目录结构自动推导，用来快速确认当前收录规模、页面构成与分类完整度。</p>
      <p class="atlas-pulse__status {status_class}">{classification_status} · {medium_note}</p>
    </div>
    <div class="atlas-pulse__grid">
      {cards}
    </div>
  </div>
</section>"""


def render_section_head(section: dict[str, str]) -> str:
    return f"""<header class="atlas-section__head">
  <p class="atlas-section__kicker">{e(section['kicker'])}</p>
  <h2>{e(section['title'])}</h2>
  <p>{e(section['description'])}</p>
</header>"""


def render_domains_section(domains: list[dict[str, object]], section: dict[str, str]) -> str:
    cards = []
    for domain in domains:
        tags = "\n".join(f'<li>{e(tag)}</li>' for tag in domain["keywords"])
        links = render_links(domain["entries"]) if domain["entries"] else '<span class="atlas-domain__empty">待补充</span>'
        cards.append(
            f"""<article class="atlas-domain atlas-domain--{e(domain['theme'])}">
  <div class="atlas-domain__top">
    <p class="atlas-domain__code">{e(domain['code'])}</p>
    <h3>{e(domain['title'])}</h3>
    <p class="atlas-domain__count">{e(domain['count'])}</p>
  </div>
  <p class="atlas-domain__summary">{e(domain['summary'])}</p>
  <ul class="atlas-taglist" aria-label="{e(domain['title'])}关键词">
    {tags}
  </ul>
  <div class="atlas-domain__links">
    {links}
  </div>
</article>"""
        )
    return f"""<section class="atlas-section atlas-section--map" id="knowledge-map">
  <div class="atlas-shell">
    {render_section_head(section)}

    <div class="atlas-domain-grid">
      {'\n'.join(cards)}
    </div>
  </div>
</section>"""


def render_filter_group(label: str, group: str, options: list[dict[str, object]]) -> str:
    buttons = []
    for option in options:
        active = bool(option.get("active"))
        classes = "atlas-filter is-active" if active else "atlas-filter"
        buttons.append(
            f'<button class="{classes}" type="button" data-filter-group="{e(group)}" data-filter-value="{e(option["value"])}" aria-pressed="{str(active).lower()}">{e(option["label"])}</button>'
        )
    return f"""<div class="atlas-filter-group" role="group" aria-label="按{e(label)}筛选">
  <span class="atlas-filter-group__label">{e(label)}</span>
  {' '.join(buttons)}
</div>"""


def render_work(work: dict[str, object]) -> str:
    chips = "\n".join(f'<li>{e(chip)}</li>' for chip in work["chips"])
    meta_items = []
    for item in work["meta"]:
        meta_items.append(f"<div><dt>{e(item['term'])}</dt><dd>{e(item['value'])}</dd></div>")
    return f"""<li class="atlas-work-card" data-domain="{e(' '.join(work['domains']))}" data-domain-primary="{e(work['domain'])}" data-medium="{e(' '.join(work['medium']))}">
  <article>
    <div class="atlas-work-card__head">
      <p class="atlas-work-card__sub">{e(work['sub'])}</p>
      <h3>{e(work['title'])}</h3>
    </div>
    <p class="atlas-work-card__summary">{e(work['summary'])}</p>
    <ul class="atlas-chiplist" aria-label="{e(work['title'])}标签">
      {chips}
    </ul>
    <dl class="atlas-work-card__meta">
      {'\n'.join(meta_items)}
    </dl>
    <a class="atlas-inline-link" href="{e(work['href'])}">{e(work['cta'])}</a>
  </article>
</li>"""


def render_works_section(data: dict[str, object], works: list[dict[str, object]], filters: dict[str, list[dict[str, object]]]) -> str:
    section = data["sections"]["worksIndex"]
    chips = "\n".join(f'<li>{e(chip)}</li>' for chip in section["chips"])
    work_cards = "\n".join(render_work(work) for work in works)
    total = len(works)
    return f"""<section class="atlas-section atlas-section--works" id="works-index">
  <div class="atlas-shell">
    {render_section_head(section)}

    <div class="atlas-section-meta atlas-section-meta--works">
      <p class="atlas-results" aria-live="polite">当前显示 <strong data-results-count>{total}</strong> / <strong data-results-total>{total}</strong> 部作品</p>
      <div class="atlas-section-tools">
        <ul class="atlas-section-chips" aria-label="作品索引提示">
          {chips}
        </ul>
        <button class="atlas-reset" type="button" data-reset-filters>重置筛选</button>
      </div>
    </div>

    <div class="atlas-filters" aria-label="作品筛选">
      {render_filter_group('领域', 'domain', filters['domain'])}
      {render_filter_group('媒介', 'medium', filters['medium'])}
    </div>

    <ul class="atlas-work-grid">
      {work_cards}
    </ul>
    <p class="atlas-filter-empty" hidden>当前筛选组合下没有对应作品。你可以先切回“全部”，或换一个领域 / 媒介继续浏览。</p>
  </div>
</section>"""


def render_path(path: dict[str, object]) -> str:
    compact_class = " atlas-path-card--compact" if path.get("compact") else ""
    steps = "\n".join(f'<li><a href="{e(step["href"])}">{e(step["label"])}</a></li>' for step in path["steps"])
    return f"""<article class="atlas-path-card{compact_class}">
  <h3>{e(path['title'])}</h3>
  <p class="atlas-path-card__for">{e(path['for'])}</p>
  <p>{e(path['summary'])}</p>
  <ol>
    {steps}
  </ol>
</article>"""


def render_paths_section(data: dict[str, object]) -> str:
    section = data["sections"]["readingPaths"]
    chips = "\n".join(f'<li>{e(chip)}</li>' for chip in section["chips"])
    path_cards = "\n".join(render_path(path) for path in data["paths"])
    return f"""<section class="atlas-section atlas-section--paths" id="reading-paths">
  <div class="atlas-shell">
    {render_section_head(section)}

    <div class="atlas-section-meta atlas-section-meta--paths">
      <ul class="atlas-section-chips" aria-label="阅读路径概览">
        {chips}
      </ul>
    </div>

    <div class="atlas-path-grid">
      {path_cards}
    </div>
  </div>
</section>"""


def render_methodology(data: dict[str, object]) -> str:
    section = data["sections"]["methodology"]
    flow = "\n".join(
        f"""<li>
  <span class="atlas-method-flow__step">{e(item['step'])}</span>
  <h3>{e(item['title'])}</h3>
  <p>{e(item['text'])}</p>
</li>"""
        for item in data["methodology"]["flow"]
    )
    variants = "\n".join(
        f"""<article>
  <h3>{e(item['title'])}</h3>
  <p>{e(item['text'])}</p>
</article>"""
        for item in data["methodology"]["variants"]
    )
    return f"""<section class="atlas-section" id="methodology">
  <div class="atlas-shell">
    {render_section_head(section)}

    <ol class="atlas-method-flow" aria-label="项目方法流程">
      {flow}
    </ol>

    <div class="atlas-method-variants">
      {variants}
    </div>
  </div>
</section>"""


def render_notes(data: dict[str, object]) -> str:
    section = data["sections"]["notes"]
    paragraphs = [f'<p>{e(text)}</p>' for text in data["notes"]]
    if len(paragraphs) > 1:
        paragraphs[-1] = paragraphs[-1].replace('<p>', '<p class="atlas-note-block__minor">', 1)
    return f"""<section class="atlas-section atlas-section--notes" id="about-project">
  <div class="atlas-shell atlas-note-block">
    <header class="atlas-section__head atlas-section__head--compact">
      <p class="atlas-section__kicker">{e(section['kicker'])}</p>
      <h2>{e(section['title'])}</h2>
    </header>
    {'\n'.join(paragraphs)}
  </div>
</section>"""


def render_footer(site: dict[str, object]) -> str:
    lines = "\n".join(f'<p>{e(line)}</p>' for line in site["footer"])
    return f"""<footer class="atlas-footer">
  <div class="atlas-shell atlas-footer__inner">
    {lines}
  </div>
</footer>"""


def build_html(data: dict[str, object], works: list[dict[str, object]], domains: list[dict[str, object]], filters: dict[str, list[dict[str, object]]], metrics: dict[str, object]) -> str:
    site = sync_hero_stats(data["site"], metrics)
    return f"""<!DOCTYPE html>
<html lang="{e(site['lang'])}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(site['title'])}</title>
  <meta name="description" content="{e(site['description'])}">
  <link rel="stylesheet" href="_shared/homepage.css">
</head>
<body>
  <!-- Generated from _data/homepage-data.json + _data/handbooks.json by scripts/project_tools.py. -->
  <a class="skip-link" href="#main-content">跳到正文</a>

  {render_header(site)}

  <main id="main-content">
    {render_hero(site, domains)}
    {render_project_pulse(metrics)}
    {render_domains_section(domains, data['sections']['knowledgeMap'])}
    {render_works_section(data, works, filters)}
    {render_paths_section(data)}
    {render_methodology(data)}
    {render_notes(data)}
  </main>

  {render_footer(site)}

  <script src="_shared/homepage.js"></script>
</body>
</html>
"""


def write_metrics(metrics: dict[str, object]) -> None:
    save_json(METRICS_PATH, metrics)


def cmd_generate() -> int:
    data, works, filters, domains, metrics = build_runtime_data()
    html = build_html(data, works, domains, filters, metrics)
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    write_metrics(metrics)
    print(
        f"Generated {OUTPUT_PATH.relative_to(ROOT)} from "
        f"{DATA_PATH.relative_to(ROOT)} + {HANDBOOKS_PATH.relative_to(ROOT)}"
    )
    print(
        f"Metrics: {metrics['totalHandbooks']} handbooks / "
        f"{metrics['totalPages']} pages / {metrics['totalDomains']} domains"
    )
    return 0
