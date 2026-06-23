from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .common import (
    DOCS_ROOT,
    DOC_LINK_FILES,
    HTML_ATTR_RE,
    HTML_LINK_ROOTS,
    HTMLValidator,
    IGNORE_PREFIXES,
    MD_LINK_RE,
    METRICS_PATH,
    ROOT,
    load_json,
    print_items,
)
from .homepage import build_html, build_label_maps, build_runtime_data


def normalize_target(raw: str) -> str | None:
    value = raw.strip()
    if not value or value.startswith(IGNORE_PREFIXES):
        return None
    value = value.split("#", 1)[0].strip()
    if not value or value.startswith(IGNORE_PREFIXES):
        return None
    return value


def extract_md_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [match.group(1) for match in MD_LINK_RE.finditer(text)]


def extract_html_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [match.group(1) for match in HTML_ATTR_RE.finditer(text)]


def iter_html_files() -> Iterable[Path]:
    for root in HTML_LINK_ROOTS:
        if root.is_file():
            yield root
        elif root.is_dir():
            yield from sorted(root.rglob("*.html"))


def resolve_target(base: Path, raw: str) -> Path:
    return (base.parent / raw).resolve()


def validate_paths(paths: Iterable[Path], extractor, label: str) -> tuple[list[str], list[str]]:
    checked: list[str] = []
    missing: list[str] = []
    for path in paths:
        for raw_link in extractor(path):
            link = normalize_target(raw_link)
            if not link:
                continue
            target = resolve_target(path, link)
            checked.append(f"{path.relative_to(ROOT)} -> {link}")
            if not target.exists():
                missing.append(f"{label}: {path.relative_to(ROOT)} -> {link}")
    return checked, missing


def cmd_validate() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    infos: list[str] = []

    try:
        homepage_data = load_json(ROOT / "_data" / "homepage-data.json")
    except Exception as exc:
        print(f"[FATAL] 无法读取首页数据：{exc}")
        return 1

    try:
        registry = load_json(ROOT / "_data" / "handbooks.json")
    except Exception as exc:
        print(f"[FATAL] 无法读取手册注册表：{exc}")
        return 1

    if not isinstance(registry, list):
        print("[FATAL] _data/handbooks.json 必须是数组。")
        return 1

    domain_labels, medium_labels, _ = build_label_maps(homepage_data)
    medium_ids = set(medium_labels)
    seen_folders: set[str] = set()
    seen_titles: set[str] = set()

    for index, item in enumerate(registry, start=1):
        if not isinstance(item, dict):
            errors.append(f"第 {index} 条手册记录不是对象。")
            continue

        folder = str(item.get("folder", "")).strip()
        title = str(item.get("title", "")).strip()

        if not folder:
            errors.append(f"第 {index} 条手册记录缺少 folder。")
            continue
        if not title:
            errors.append(f"手册 {folder} 缺少 title。")

        if folder in seen_folders:
            errors.append(f"folder 重复：{folder}")
        seen_folders.add(folder)

        if title in seen_titles:
            warnings.append(f"title 重复：{title}")
        seen_titles.add(title)

        folder_path = DOCS_ROOT / folder
        if not folder_path.exists():
            errors.append(f"手册目录不存在：doc/{folder}")
            continue
        if not folder_path.is_dir():
            errors.append(f"路径不是目录：doc/{folder}")
            continue

        index_path = folder_path / "index.html"
        if not index_path.exists():
            errors.append(f"缺少手册首页：doc/{folder}/index.html")

        page_count = len(list(folder_path.glob("*.html")))
        infos.append(f"{folder}: {page_count} 个 HTML 页面")

        raw_domains = item.get("domains", item.get("domain"))
        domains = [raw_domains] if isinstance(raw_domains, str) else list(raw_domains or [])
        if not domains:
            warnings.append(f"手册 {folder} 未填写 domain / domains；首页会以默认兜底方式展示。")
        else:
            unknown = [str(value) for value in domains if str(value).strip() not in domain_labels]
            if unknown:
                warnings.append(f"手册 {folder} 使用了未预定义的 domain：{', '.join(unknown)}（将回落到待归类）")

        raw_medium = item.get("medium")
        mediums = [raw_medium] if isinstance(raw_medium, str) else list(raw_medium or [])
        if not mediums:
            warnings.append(f"手册 {folder} 未填写 medium；首页会以默认兜底方式展示。")
        else:
            unknown = [str(value) for value in mediums if str(value).strip() not in medium_ids]
            if unknown:
                warnings.append(f"手册 {folder} 使用了未预定义的 medium：{', '.join(unknown)}（将回落到其他）")

        custom_href = str(item.get("href", "")).strip()
        if custom_href:
            custom_target = resolve_target(ROOT / "index.html", custom_href)
            if not custom_target.exists():
                errors.append(f"手册 {folder} 的自定义 href 不存在：{custom_href}")

    doc_dirs = sorted(path.name for path in DOCS_ROOT.iterdir() if path.is_dir()) if DOCS_ROOT.exists() else []
    unregistered_dirs = [name for name in doc_dirs if name not in seen_folders]
    if unregistered_dirs:
        warnings.append("以下手册目录尚未登记到 _data/handbooks.json：" + ", ".join(unregistered_dirs))

    try:
        data, works, filters, domains, metrics = build_runtime_data()
        rendered_html = build_html(data, works, domains, filters, metrics)
        HTMLValidator().feed(rendered_html)
    except Exception as exc:
        errors.append(f"首页生成校验失败：{exc}")

    print("Handbook registry validation summary")
    print("=" * 36)
    print(f"已登记手册：{len(registry)}")
    print(f"目录中手册文件夹：{len(doc_dirs)}")
    print_items("Info", infos)
    print_items("Warnings", warnings)
    print_items("Errors", errors)

    if errors:
        print("\n结果：失败（存在错误）")
        return 1
    if warnings:
        print("\n结果：通过（有警告，建议处理）")
        return 0
    print("\n结果：通过")
    return 0


def cmd_check_links() -> int:
    md_checked, md_missing = validate_paths(DOC_LINK_FILES, extract_md_links, "Markdown")
    html_files = list(iter_html_files())
    html_checked, html_missing = validate_paths(html_files, extract_html_links, "HTML")

    checked_total = len(md_checked) + len(html_checked)
    missing = md_missing + html_missing

    print("Project link check summary")
    print("=" * 28)
    print(f"检查文件数：{len(DOC_LINK_FILES) + len(html_files)}")
    print(f"检查链接数：{checked_total}")
    print_items("Broken links", missing)

    if missing:
        print("\n结果：失败（存在无效本地链接）")
        return 1
    print("\n结果：通过")
    return 0


def print_metrics_summary() -> None:
    if not METRICS_PATH.exists():
        return
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    print(
        "Metrics summary: "
        f"{metrics.get('totalHandbooks', 0)} handbooks / "
        f"{metrics.get('totalPages', 0)} pages / "
        f"{metrics.get('totalDomains', 0)} domains"
    )
