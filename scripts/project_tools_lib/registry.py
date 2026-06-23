from __future__ import annotations

from typing import Any

from .common import DATA_PATH, HANDBOOKS_PATH, load_json, save_json
from .homepage import build_label_maps

FIELD_GUIDE = {
    "folder": "对应 doc/<folder>/ 的目录名；也是默认首页入口路径的一部分。",
    "title": "首页作品卡片主标题。",
    "subtitle": "首页作品卡片副标题；留空时使用通用默认值。",
    "domains": "知识领域数组，可多选；用于知识地图归类和领域筛选。",
    "medium": "媒介数组，可多选；用于媒介筛选。",
    "tags": "首页卡片上的标签列表，用于快速提示主题。",
    "summary": "首页卡片摘要。",
    "scale": "首页卡片中的“规模”说明；留空会按页面统计自动推导。",
    "structure": "首页卡片中的“结构亮点”说明；留空会按目录结构自动推导。",
    "startHere": "首页卡片中的“从这里开始”阅读建议；留空会自动推导。",
    "href": "覆盖默认入口地址；不填时默认使用 doc/<folder>/index.html。",
    "cta": "覆盖卡片底部入口文案；不填时自动生成为“进入《标题》手册”。",
    "domainLabel": "保留字段。当前首页未直接使用，一般无需填写。",
}

FIELD_EXAMPLES = {
    "folder": "new-work-folder",
    "title": "新作品名",
    "subtitle": "知识手册",
    "domains": "life, micro",
    "medium": "novel, manga, anime",
    "tags": "标签 A, 标签 B",
    "summary": "一句话说明该手册通向什么知识方向。",
    "scale": "共 12 个页面",
    "structure": "按主题整理 + 辅助页",
    "startHere": "先从手册首页总览开始。",
    "href": "doc/new-work-folder/index.html",
    "cta": "进入手册总览",
}

FIELD_GROUPS = [
    ("必填字段", ["folder", "title"]),
    ("常用展示字段", ["subtitle", "domains", "medium", "tags", "summary", "startHere"]),
    ("自动推导 / 可覆盖字段", ["scale", "structure", "href", "cta"]),
    ("保留字段", ["domainLabel"]),
]


def load_registry() -> list[dict[str, Any]]:
    registry = load_json(HANDBOOKS_PATH)
    if not isinstance(registry, list):
        raise ValueError("_data/handbooks.json 必须是数组。")
    return registry


def save_registry_entries(entries: list[dict[str, Any]]) -> None:
    save_json(HANDBOOKS_PATH, entries)


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def prompt(text: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default not in (None, "") else ""
    raw = input(f"{text}{suffix}: ").strip()
    if raw == "" and default is not None:
        return default
    return raw


def prompt_optional(text: str, current: str | None = None) -> str | None:
    if current not in (None, ""):
        print(f"当前值：{current}")
    raw = input(f"{text}（留空保留，输入 - 清空）: ").strip()
    if raw == "":
        return current
    if raw == "-":
        return None
    return raw


def prompt_list(text: str, default: list[str] | None = None) -> list[str]:
    default_text = ", ".join(default or [])
    raw = prompt(text, default_text)
    return split_csv(raw) if raw else []


def prompt_list_optional(text: str, current: list[str] | None = None) -> list[str] | None:
    current = current or []
    if current:
        print(f"当前值：{', '.join(current)}")
    raw = input(f"{text}（逗号分隔；留空保留，输入 - 清空）: ").strip()
    if raw == "":
        return current
    if raw == "-":
        return None
    return split_csv(raw)


def choose_handbook(entries: list[dict[str, Any]]) -> int | None:
    if not entries:
        print("当前没有已登记手册。")
        return None
    print("\n已登记手册：")
    for idx, item in enumerate(entries, start=1):
        print(f"  {idx}. {item.get('title', '(无标题)')}  [{item.get('folder', '')}]")
    raw = input("选择编号（留空取消）: ").strip()
    if not raw:
        return None
    try:
        index = int(raw)
    except ValueError:
        print("输入无效。")
        return None
    if not (1 <= index <= len(entries)):
        print("编号超出范围。")
        return None
    return index - 1


def print_registry() -> int:
    entries = load_registry()
    if not entries:
        print("当前没有已登记手册。")
        return 0
    print("\n当前已登记手册：")
    for idx, item in enumerate(entries, start=1):
        domains = item.get("domains") or item.get("domain") or []
        if isinstance(domains, str):
            domains = [domains]
        mediums = item.get("medium") or []
        if isinstance(mediums, str):
            mediums = [mediums]
        print(f"  {idx}. {item.get('title', '(无标题)')}  [{item.get('folder', '')}]")
        print(f"     domains: {', '.join(domains) if domains else '-'}")
        print(f"     medium : {', '.join(mediums) if mediums else '-'}")
    return 0


def _show_choices() -> tuple[list[str], list[str]]:
    homepage_data = load_json(DATA_PATH)
    domain_labels, medium_labels, _ = build_label_maps(homepage_data)
    available_domains = [key for key in domain_labels if key != 'uncategorized']
    available_mediums = [key for key in medium_labels if key != 'other']
    print("可用领域：", ", ".join(available_domains))
    print("示例：domains = life, micro")
    print("可用媒介：", ", ".join(available_mediums))
    print("示例：medium = novel, manga, anime")
    return available_domains, available_mediums


def print_registry_field_guide() -> None:
    print("\n字段速查")
    print("-" * 8)
    for title, keys in FIELD_GROUPS:
        print(f"{title}：")
        for key in keys:
            print(f"  - {key}: {FIELD_GUIDE[key]}")
        print("")


def print_form_section(title: str, keys: list[str], note: str = "") -> None:
    print(f"\n{title}")
    print("-" * max(len(title), 8))
    if note:
        print(note)
    for key in keys:
        print(f"  - {key}: {FIELD_GUIDE[key]}")


def print_field_prompt_intro(key: str) -> None:
    print(f"\n[{key}] {FIELD_GUIDE[key]}")
    example = FIELD_EXAMPLES.get(key)
    if example:
        print(f"示例：{key} = {example}")


def format_preview_value(item: dict[str, Any], key: str) -> str:
    if key == "domains":
        value = item.get("domains") or ([] if not item.get("domain") else [item["domain"]])
        return ", ".join(str(part) for part in value) if value else "(未填写，将回落到待归类)"
    if key == "medium":
        value = item.get("medium") or []
        return ", ".join(str(part) for part in value) if value else "(未填写，将回落到其他)"
    if key == "tags":
        value = item.get("tags") or []
        return ", ".join(str(part) for part in value) if value else "(未填写)"
    value = item.get(key)
    if value in (None, ""):
        if key == "href":
            folder = str(item.get("folder", "")).strip()
            if folder:
                return f"(未填写，将默认使用 doc/{folder}/index.html)"
        if key == "cta":
            title = str(item.get("title", "")).strip()
            if title:
                return f"(未填写，将默认使用 进入《{title}》手册)"
        if key in {"scale", "structure", "startHere"}:
            return "(未填写，将自动推导)"
        if key == "domainLabel":
            return "(未填写，当前也未直接使用)"
        return "(未填写)"
    return str(value)


def print_entry_preview(item: dict[str, Any]) -> None:
    print("\n当前登记信息预览")
    print("=" * 18)
    print(f"标题：{item.get('title', '(无标题)')}")
    print(f"目录：{item.get('folder', '-')}")
    for title, keys in FIELD_GROUPS:
        print(f"\n{title}")
        print("-" * max(len(title), 8))
        for key in keys:
            print(f"  - {key}: {format_preview_value(item, key)}")


def prompt_text_add(key: str, label: str) -> str:
    print_field_prompt_intro(key)
    return prompt(label)


def prompt_text_edit(key: str, current: str | None = None) -> str | None:
    print_field_prompt_intro(key)
    return prompt_optional(key, current)


def prompt_list_add(key: str, label: str) -> list[str]:
    print_field_prompt_intro(key)
    return prompt_list(label)


def prompt_list_edit(key: str, current: list[str] | None = None) -> list[str] | None:
    print_field_prompt_intro(key)
    return prompt_list_optional(key, current)


def _post_edit_hint(title: str, folder: str) -> None:
    print(f"\n已更新登记信息：{title} [{folder}]")
    print("建议接下来执行：")
    print("  1. python scripts/project_tools.py inject-home-buttons")
    print("  2. python scripts/project_tools.py verify")


def add_handbook_interactive() -> int:
    entries = load_registry()
    print("\n新增手册登记")
    _show_choices()
    print("\n这是一个分组表单：先填必填字段，再按需要补充展示字段。")
    print("最小可用输入只有 folder + title；其余字段都可稍后再补。")

    print_form_section("第 1 组 / 必填字段", ["folder", "title"], "这两项决定手册能否被正确登记。")
    folder = prompt_text_add("folder", "folder（对应 doc/<folder>/）")
    if not folder:
        print("已取消。")
        return 0
    title = prompt_text_add("title", "title")
    if not title:
        print("title 不能为空，已取消。")
        return 1

    entry: dict[str, Any] = {
        "folder": folder,
        "title": title,
    }

    print_form_section(
        "第 2 组 / 常用展示字段",
        ["subtitle", "domains", "medium", "tags", "summary", "startHere"],
        "这一组主要影响首页卡片、知识地图归类与筛选效果；推荐优先补全。",
    )
    subtitle = prompt_text_add("subtitle", "subtitle（可留空）")
    if subtitle:
        entry["subtitle"] = subtitle
    domains = prompt_list_add("domains", "domains（逗号分隔，可留空）")
    if domains:
        entry["domains"] = domains
    medium = prompt_list_add("medium", "medium（逗号分隔，可留空）")
    if medium:
        entry["medium"] = medium
    tags = prompt_list_add("tags", "tags（逗号分隔，可留空）")
    if tags:
        entry["tags"] = tags
    summary = prompt_text_add("summary", "summary（可留空）")
    if summary:
        entry["summary"] = summary
    start_here = prompt_text_add("startHere", "startHere（可留空；不填则自动推导）")
    if start_here:
        entry["startHere"] = start_here

    print_form_section(
        "第 3 组 / 自动推导 / 可覆盖字段",
        ["scale", "structure", "href", "cta"],
        "这一组通常可以先留空；只有你想覆盖默认推导或默认入口时再填写。",
    )
    scale = prompt_text_add("scale", "scale（可留空；不填则自动推导）")
    if scale:
        entry["scale"] = scale
    structure = prompt_text_add("structure", "structure（可留空；不填则自动推导）")
    if structure:
        entry["structure"] = structure
    href = prompt_text_add("href", "href（可留空；默认 doc/<folder>/index.html）")
    if href:
        entry["href"] = href
    cta = prompt_text_add("cta", "cta（可留空；默认自动生成）")
    if cta:
        entry["cta"] = cta

    print_form_section("第 4 组 / 保留字段", ["domainLabel"], "当前首页未直接使用，因此不在新增表单中开放。")

    entries.append(entry)
    save_registry_entries(entries)
    _post_edit_hint(title, folder)
    return 0


def edit_handbook_interactive() -> int:
    entries = load_registry()
    index = choose_handbook(entries)
    if index is None:
        return 0

    item = entries[index]
    print(f"\n编辑手册：{item.get('title')} [{item.get('folder')}]")
    print_entry_preview(item)
    _show_choices()
    print("\n这是一个分组表单：留空保留当前值，输入 - 可清空可选字段。")
    print("建议先看每组字段说明，再决定是否需要覆盖默认值。")

    print_form_section("第 1 组 / 必填字段", ["folder", "title"], "这两项始终应保持有效。")
    print_field_prompt_intro("folder")
    item['folder'] = prompt('folder', str(item.get('folder', '')))
    print_field_prompt_intro("title")
    item['title'] = prompt('title', str(item.get('title', '')))

    print_form_section(
        "第 2 组 / 常用展示字段",
        ["subtitle", "domains", "medium", "tags", "summary", "startHere"],
        "这一组主要影响首页卡片、归类与筛选；通常最值得维护。",
    )
    subtitle = prompt_text_edit('subtitle', str(item.get('subtitle', '')) or None)
    if subtitle:
        item['subtitle'] = subtitle
    else:
        item.pop('subtitle', None)

    domains_default = item.get('domains') or ([] if not item.get('domain') else [item['domain']])
    domains = prompt_list_edit('domains', domains_default)
    if domains:
        item['domains'] = domains
        item.pop('domain', None)
    else:
        item.pop('domains', None)
        item.pop('domain', None)

    medium_default = item.get('medium') or []
    medium = prompt_list_edit('medium', medium_default)
    if medium:
        item['medium'] = medium
    else:
        item.pop('medium', None)

    tags = prompt_list_edit('tags', item.get('tags') or [])
    if tags:
        item['tags'] = tags
    else:
        item.pop('tags', None)

    summary = prompt_text_edit('summary', str(item.get('summary', '')) or None)
    if summary:
        item['summary'] = summary
    else:
        item.pop('summary', None)

    start_here = prompt_text_edit('startHere', str(item.get('startHere', '')) or None)
    if start_here:
        item['startHere'] = start_here
    else:
        item.pop('startHere', None)

    print_form_section(
        "第 3 组 / 自动推导 / 可覆盖字段",
        ["scale", "structure", "href", "cta"],
        "这组字段通常可以继续留空；只有你想覆盖默认推导或默认入口时再修改。",
    )
    for key in ['scale', 'structure', 'href', 'cta']:
        value = prompt_text_edit(key, str(item.get(key, '')) or None)
        if value:
            item[key] = value
        else:
            item.pop(key, None)

    print_form_section("第 4 组 / 保留字段", ["domainLabel"], "当前首页未直接使用，因此不在编辑表单中开放。")
    if item.get('domainLabel'):
        print("已保留现有 domainLabel 值，但当前不会在首页直接生效。")

    save_registry_entries(entries)
    _post_edit_hint(str(item.get('title', '')), str(item.get('folder', '')))
    return 0


def remove_handbook_interactive() -> int:
    entries = load_registry()
    index = choose_handbook(entries)
    if index is None:
        return 0
    item = entries[index]
    print_entry_preview(item)
    confirm = input(f"确认删除 {item.get('title')} [{item.get('folder')}] 吗？输入 yes 确认: ").strip().lower()
    if confirm != 'yes':
        print('已取消。')
        return 0
    removed = entries.pop(index)
    save_registry_entries(entries)
    print(f"已删除手册登记：{removed.get('title')} [{removed.get('folder')}]")
    print("建议执行 python scripts/project_tools.py verify 确认项目状态。")
    return 0
