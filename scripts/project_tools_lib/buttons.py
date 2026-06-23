from __future__ import annotations

import re

from .common import CSS_TAG_RE, DOCS_ROOT, HOME_BUTTON_CSS, HOME_BUTTON_JS, JS_TAG_RE, ROOT, print_items


def compute_prefix(path):
    rel_parent = path.relative_to(ROOT).parent
    depth = len(rel_parent.parts)
    return "../" * depth


def remove_existing_tag_blocks(text: str, pattern) -> str:
    return pattern.sub("", text)


def insert_normalized_tag_block(text: str, desired_tag: str, closing_tag: str, error_message: str) -> str:
    closing_index = text.find(closing_tag)
    if closing_index == -1:
        raise ValueError(error_message)

    prefix = text[:closing_index]
    if prefix.endswith("\n"):
        prefix = re.sub(r"\n(?:[ \t]*\n)+$", "\n", prefix)
        prefix = re.sub(r"\n[ \t]+$", "\n", prefix)
    else:
        prefix = prefix.rstrip() + "\n"

    return f"{prefix}  {desired_tag}\n{text[closing_index:]}"


def normalize_tag_block(text: str, pattern, desired_tag: str, closing_tag: str):
    matches = list(pattern.finditer(text))
    expected_block = f"  {desired_tag}\n{closing_tag}"

    if not matches:
        return (
            insert_normalized_tag_block(text, desired_tag, closing_tag, f"缺少 {closing_tag}"),
            "inserted",
        )

    if len(matches) == 1:
        current = matches[0].group(0).strip()
        if current == desired_tag and expected_block in text:
            return text, "ok"
        cleaned_text = remove_existing_tag_blocks(text, pattern)
        return (
            insert_normalized_tag_block(cleaned_text, desired_tag, closing_tag, f"更新后缺少 {closing_tag}"),
            "updated",
        )

    cleaned_text = remove_existing_tag_blocks(text, pattern)
    return (
        insert_normalized_tag_block(cleaned_text, desired_tag, closing_tag, f"去重后缺少 {closing_tag}"),
        "deduped",
    )


def cmd_inject_home_buttons() -> int:
    if not HOME_BUTTON_CSS.exists() or not HOME_BUTTON_JS.exists():
        print("[FATAL] 缺少统一返回首页按钮资源文件。")
        return 1

    html_files = sorted(DOCS_ROOT.rglob("*.html")) if DOCS_ROOT.exists() else []
    if not html_files:
        print("[FATAL] doc/ 下没有可注入的 HTML 页面。")
        return 1

    summary = {
        "files": len(html_files),
        "css_inserted": 0,
        "css_updated": 0,
        "css_deduped": 0,
        "css_ok": 0,
        "js_inserted": 0,
        "js_updated": 0,
        "js_deduped": 0,
        "js_ok": 0,
    }
    errors: list[str] = []

    for path in html_files:
        prefix = compute_prefix(path)
        css_tag = f'<link rel="stylesheet" href="{prefix}_shared/home-button.css">'
        js_tag = f'<script src="{prefix}_shared/home-button.js" data-home-href="{prefix}index.html"></script>'

        try:
            text = path.read_text(encoding="utf-8")
            text, css_status = normalize_tag_block(text, CSS_TAG_RE, css_tag, "</head>")
            text, js_status = normalize_tag_block(text, JS_TAG_RE, js_tag, "</body>")
            path.write_text(text, encoding="utf-8")
            summary[f"css_{css_status}"] += 1
            summary[f"js_{js_status}"] += 1

            final_text = text
            if css_tag not in final_text:
                errors.append(f"{path.relative_to(ROOT)}: CSS 注入校验失败")
            if js_tag not in final_text:
                errors.append(f"{path.relative_to(ROOT)}: JS 注入校验失败")
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    print("Home button injection summary")
    print("=" * 29)
    print(f"处理页面数：{summary['files']}")
    print(
        "CSS -> inserted: {css_inserted}, updated: {css_updated}, deduped: {css_deduped}, ok: {css_ok}".format(
            **summary
        )
    )
    print(
        "JS  -> inserted: {js_inserted}, updated: {js_updated}, deduped: {js_deduped}, ok: {js_ok}".format(
            **summary
        )
    )
    print_items("Injection errors", errors)

    if errors:
        print("\n结果：失败（存在注入错误）")
        return 1

    print("\n结果：通过")
    return 0


def cmd_strip_home_buttons() -> int:
    html_files = sorted(DOCS_ROOT.rglob("*.html")) if DOCS_ROOT.exists() else []
    if not html_files:
        print("[FATAL] doc/ 下没有可处理的 HTML 页面。")
        return 1

    stripped_css = 0
    stripped_js = 0
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        new_text, css_count = CSS_TAG_RE.subn("", text)
        new_text, js_count = JS_TAG_RE.subn("", new_text)
        if css_count or js_count:
            new_text = new_text.replace("\n\n</head>", "\n</head>")
            new_text = new_text.replace("\n\n</body>", "\n</body>")
            path.write_text(new_text, encoding="utf-8")
        stripped_css += css_count
        stripped_js += js_count

    print("Home button strip summary")
    print("=" * 25)
    print(f"处理页面数：{len(html_files)}")
    print(f"移除 CSS 标签：{stripped_css}")
    print(f"移除 JS 标签：{stripped_js}")
    print("\n结果：通过")
    return 0


def cmd_check_home_buttons() -> int:
    html_files = sorted(DOCS_ROOT.rglob("*.html")) if DOCS_ROOT.exists() else []
    if not html_files:
        print("[FATAL] doc/ 下没有可检查的 HTML 页面。")
        return 1

    errors: list[str] = []
    summary = {
        "files": len(html_files),
        "ok": 0,
        "missing_css": 0,
        "missing_js": 0,
        "duplicate_css": 0,
        "duplicate_js": 0,
        "mismatch_css": 0,
        "mismatch_js": 0,
    }

    for path in html_files:
        prefix = compute_prefix(path)
        expected_css = f'<link rel="stylesheet" href="{prefix}_shared/home-button.css">'
        expected_js = f'<script src="{prefix}_shared/home-button.js" data-home-href="{prefix}index.html"></script>'
        text = path.read_text(encoding="utf-8")
        css_matches = list(CSS_TAG_RE.finditer(text))
        js_matches = list(JS_TAG_RE.finditer(text))
        file_ok = True

        if not css_matches:
            summary["missing_css"] += 1
            errors.append(f"{path.relative_to(ROOT)}: 缺少 home-button.css 标签")
            file_ok = False
        elif len(css_matches) > 1:
            summary["duplicate_css"] += 1
            errors.append(f"{path.relative_to(ROOT)}: home-button.css 标签重复")
            file_ok = False
        elif css_matches[0].group(0).strip() != expected_css:
            summary["mismatch_css"] += 1
            errors.append(f"{path.relative_to(ROOT)}: home-button.css 标签路径不匹配")
            file_ok = False

        if not js_matches:
            summary["missing_js"] += 1
            errors.append(f"{path.relative_to(ROOT)}: 缺少 home-button.js 标签")
            file_ok = False
        elif len(js_matches) > 1:
            summary["duplicate_js"] += 1
            errors.append(f"{path.relative_to(ROOT)}: home-button.js 标签重复")
            file_ok = False
        elif js_matches[0].group(0).strip() != expected_js:
            summary["mismatch_js"] += 1
            errors.append(f"{path.relative_to(ROOT)}: home-button.js 标签或 data-home-href 不匹配")
            file_ok = False

        if file_ok:
            summary["ok"] += 1

    print("Home button check summary")
    print("=" * 25)
    print(f"检查页面数：{summary['files']}")
    print(f"完全正常：{summary['ok']}")
    print(f"缺少 CSS：{summary['missing_css']}")
    print(f"缺少 JS：{summary['missing_js']}")
    print(f"重复 CSS：{summary['duplicate_css']}")
    print(f"重复 JS：{summary['duplicate_js']}")
    print(f"CSS 路径不匹配：{summary['mismatch_css']}")
    print(f"JS / data-home-href 不匹配：{summary['mismatch_js']}")
    print_items("Home button issues", errors)

    if errors:
        print("\n结果：失败（返回首页按钮状态不符合当前标准）")
        return 1

    print("\n结果：通过")
    return 0
