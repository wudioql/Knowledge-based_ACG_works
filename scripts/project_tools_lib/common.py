from __future__ import annotations

import json
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "_data" / "homepage-data.json"
HANDBOOKS_PATH = ROOT / "_data" / "handbooks.json"
METRICS_PATH = ROOT / "_data" / "project-metrics.json"
DOCS_ROOT = ROOT / "doc"
OUTPUT_PATH = ROOT / "index.html"
HOME_BUTTON_CSS = ROOT / "_shared" / "home-button.css"
HOME_BUTTON_JS = ROOT / "_shared" / "home-button.js"

DOC_LINK_FILES = [
    ROOT / "README.md",
    ROOT / "ARCHITECTURE.md",
    ROOT / "CONTRIBUTING.md",
]
HTML_LINK_ROOTS = [ROOT / "index.html", ROOT / "doc"]

DEFAULT_DOMAIN_ID = "uncategorized"
DEFAULT_DOMAIN_LABEL = "待归类"
DEFAULT_MEDIUM_ID = "other"
DEFAULT_MEDIUM_LABEL = "其他"

CONTENT_PREFIXES = (
    "vol-",
    "arc-",
    "ch-",
    "ep-",
    "part-",
    "section-",
    "lesson-",
    "unit-",
    "chapter-",
)
SUPPORT_PREFIXES = (
    "glossary",
    "references",
    "characters",
    "guidebooks",
    "specials",
    "spin-offs",
    "appendix",
    "appendices",
    "timeline",
    "timelines",
    "map",
    "maps",
    "guide",
    "guides",
    "notes",
    "note",
    "resources",
    "resource",
    "about",
    "faq",
)

IGNORE_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "javascript:",
    "data:",
    "#",
)

MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HTML_ATTR_RE = re.compile(r'(?:href|src)="([^"]+)"')
CSS_TAG_RE = re.compile(r'<link[^>]+href="[^"]*_shared/home-button\.css"[^>]*>')
JS_TAG_RE = re.compile(r'<script[^>]+src="[^"]*_shared/home-button\.js"[^>]*></script>')


class HTMLValidator(HTMLParser):
    def error(self, message: str) -> None:  # pragma: no cover
        raise Exception(message)


def e(text: object) -> str:
    return escape(str(text), quote=True)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def render_attrs(attrs: dict[str, object]) -> str:
    parts = []
    for key, value in attrs.items():
        if value is None:
            continue
        if value is True:
            parts.append(key)
        else:
            parts.append(f'{key}="{e(value)}"')
    return " ".join(parts)


def render_links(items: list[dict[str, object]], class_name: str = "") -> str:
    html = []
    for item in items:
        attrs = {"href": item["href"]}
        if item.get("external"):
            attrs["target"] = "_blank"
            attrs["rel"] = "noopener"
        class_attr = f' class="{class_name}"' if class_name else ""
        html.append(f'<a{class_attr} {render_attrs(attrs)}>{e(item["label"])}</a>')
    return "\n".join(html)


def print_items(label: str, items: Iterable[str]) -> None:
    items = list(items)
    if not items:
        return
    print(f"\n{label} ({len(items)}):")
    for item in items:
        print(f"  - {item}")
