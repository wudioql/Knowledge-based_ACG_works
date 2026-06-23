from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from project_tools_lib.buttons import (
    cmd_check_home_buttons,
    cmd_inject_home_buttons,
    cmd_strip_home_buttons,
)
from project_tools_lib.checks import cmd_check_links, cmd_validate, print_metrics_summary
from project_tools_lib.homepage import build_runtime_data, cmd_generate
from project_tools_lib.registry import (
    add_handbook_interactive,
    edit_handbook_interactive,
    print_registry,
    remove_handbook_interactive,
)


def cmd_verify() -> int:
    print("Project verification pipeline")
    print("=" * 28)

    print("\n[1/4] Validate handbook registry")
    result = cmd_validate()
    if result != 0:
        print("\n验证中止：手册注册表校验失败。")
        return result

    print("\n[2/4] Generate homepage")
    result = cmd_generate()
    if result != 0:
        print("\n验证中止：首页生成失败。")
        return result
    print_metrics_summary()

    print("\n[3/4] Check project links")
    result = cmd_check_links()
    if result != 0:
        print("\n验证中止：基础链接检查失败。")
        return result

    print("\n[4/4] Check home button state")
    result = cmd_check_home_buttons()
    if result != 0:
        print("\n验证中止：返回首页按钮状态检查失败。")
        return result

    print("\n结果：项目级校验全部通过")
    return 0


def ask_yes_no(message: str, default: bool = False) -> bool:
    prompt = "[Y/n]" if default else "[y/N]"
    raw = input(f"{message} {prompt}: ").strip().lower()
    if raw == "":
        return default
    return raw in {"y", "yes"}


def pause_before_menu(message: str = "按回车返回菜单...") -> None:
    try:
        input(f"\n{message}")
    except EOFError:
        pass


def print_menu_status() -> None:
    try:
        _, _, _, _, metrics = build_runtime_data()
    except Exception as exc:
        print(f"当前状态摘要读取失败：{exc}")
        return

    print("当前项目状态")
    print("-" * 12)
    print(f"已登记手册：{metrics['totalHandbooks']}")
    print(f"页面总数：{metrics['totalPages']}")
    print(f"知识领域：{metrics['totalDomains']}")
    print(f"内容页 / 辅助页：{metrics['totalContentLikePages']} / {metrics['totalSupportPages']}")
    print(f"待归类手册：{metrics['uncategorizedHandbooks']}")
    print(f"兜底媒介手册：{metrics['fallbackMediumHandbooks']}")


def workflow_sync_and_verify() -> int:
    print("\n执行推荐工作流：同步返回按钮 → 项目级总校验")
    result = cmd_inject_home_buttons()
    if result != 0:
        return result
    return cmd_verify()


def workflow_strip_and_check() -> int:
    print("\n执行推荐工作流：移除返回按钮 → 检查当前未注入状态")
    result = cmd_strip_home_buttons()
    if result != 0:
        return result
    return cmd_check_home_buttons()


def workflow_refresh_homepage() -> int:
    print("\n执行推荐工作流：生成首页 → 检查链接")
    result = cmd_generate()
    if result != 0:
        return result
    return cmd_check_links()


def show_help_panel() -> int:
    print("\n帮助 / 示例速查")
    print("=" * 18)
    print("常用领域：life, food, micro, society, history, space")
    print("常用媒介：novel, manga, anime, game")
    print("")
    print("最小手册登记示例：")
    print('{')
    print('  "folder": "new-work-folder",')
    print('  "title": "新作品名"')
    print('}')
    print("")
    print("推荐增强示例：")
    print('{')
    print('  "folder": "new-work-folder",')
    print('  "title": "新作品名",')
    print('  "subtitle": "知识手册",')
    print('  "domains": ["food", "micro"],')
    print('  "medium": ["novel", "manga", "anime"],')
    print('  "tags": ["示例标签 A", "示例标签 B"]')
    print('}')
    print("")
    print("推荐工作流：")
    print("  A. 同步按钮并总校验：")
    print("     python scripts/project_tools.py inject-home-buttons")
    print("     python scripts/project_tools.py verify")
    print("  B. 查看未注入状态：")
    print("     python scripts/project_tools.py strip-home-buttons")
    print("     python scripts/project_tools.py check-home-buttons")
    print("  C. 只刷新首页与统计：")
    print("     python scripts/project_tools.py generate")
    print("     python scripts/project_tools.py check-links")
    return 0


def print_full_menu(actions, workflow_keys, registry_keys, core_keys, button_keys, misc_keys) -> None:
    print("\n项目工具菜单")
    print("=" * 16)
    print_menu_status()
    print("\n推荐工作流")
    print("-" * 12)
    for key in workflow_keys:
        print(f"{key}. {actions[key][0]}")

    print("\n手册登记管理")
    print("-" * 12)
    for key in registry_keys:
        print(f"{key}. {actions[key][0]}")

    print("\n核心操作")
    print("-" * 12)
    for key in core_keys:
        print(f"{key}. {actions[key][0]}")

    print("\n返回首页按钮")
    print("-" * 12)
    for key in button_keys:
        print(f"{key}. {actions[key][0]}")

    print("\n其它")
    print("-" * 12)
    for key in misc_keys:
        print(f"{key}. {actions[key][0]}")

    print("\n提示：最常用的是 1（同步按钮并总校验）；回车可重新显示菜单。")


def run_menu() -> int:
    actions = {
        "1": ("推荐工作流：同步按钮并总校验", workflow_sync_and_verify),
        "2": ("推荐工作流：首页与链接刷新", workflow_refresh_homepage),
        "3": ("推荐工作流：查看未注入状态", workflow_strip_and_check),
        "4": ("列出已登记手册", print_registry),
        "5": ("新增手册登记", add_handbook_interactive),
        "6": ("编辑手册登记", edit_handbook_interactive),
        "7": ("删除手册登记", remove_handbook_interactive),
        "8": ("项目级总校验（verify）", cmd_verify),
        "9": ("生成首页与统计摘要（generate）", cmd_generate),
        "10": ("校验手册注册表（validate）", cmd_validate),
        "11": ("检查项目本地链接（check-links）", cmd_check_links),
        "12": ("注入返回首页按钮（inject-home-buttons）", cmd_inject_home_buttons),
        "13": ("检查返回首页按钮状态（check-home-buttons）", cmd_check_home_buttons),
        "14": ("移除返回首页按钮（strip-home-buttons）", cmd_strip_home_buttons),
        "15": ("帮助 / 示例速查", show_help_panel),
        "0": ("退出", None),
    }

    workflow_keys = ["1", "2", "3"]
    registry_keys = ["4", "5", "6", "7"]
    core_keys = ["8", "9", "10", "11"]
    button_keys = ["12", "13", "14"]
    misc_keys = ["15", "0"]

    while True:
        print_full_menu(actions, workflow_keys, registry_keys, core_keys, button_keys, misc_keys)
        choice = input("请选择操作编号: ").strip()
        if choice == "":
            continue
        if choice == "0":
            print("已退出。")
            return 0
        action = actions.get(choice)
        if not action:
            print("无效编号，请重试。")
            pause_before_menu()
            continue
        action_label, func = action
        if func is None:
            return 0
        result = func()
        if result not in (None, 0):
            print(f"操作结束，返回码：{result}")
            pause_before_menu(f"\n“{action_label}”已结束；按回车返回菜单...")
            continue

        if choice in {"5", "6"}:
            if ask_yes_no("是否立即执行推荐流程（注入返回按钮 + 项目级总校验）？"):
                inject_result = cmd_inject_home_buttons()
                if inject_result == 0:
                    cmd_verify()
        elif choice == "7":
            if ask_yes_no("是否立即执行项目级总校验以确认删除后的状态？"):
                cmd_verify()
        elif choice == "12":
            if ask_yes_no("按钮已同步，是否立即执行项目级总校验？"):
                cmd_verify()
        elif choice == "14":
            if ask_yes_no("已移除按钮，是否立即执行按钮状态检查（通常会失败，用于确认当前是未注入状态）？"):
                cmd_check_home_buttons()

        pause_before_menu(f"\n“{action_label}”已完成；按回车返回菜单...")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project-level tools for the handbook repository")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("verify", help="run validate + generate + check-links + check-home-buttons")
    subparsers.add_parser("generate", help="generate homepage and metrics")
    subparsers.add_parser("validate", help="validate handbook registry")
    subparsers.add_parser("check-links", help="check project local links")
    subparsers.add_parser("inject-home-buttons", help="inject shared home buttons into doc HTML pages")
    subparsers.add_parser("strip-home-buttons", help="remove shared home button tags from doc HTML pages")
    subparsers.add_parser("check-home-buttons", help="check whether handbook pages contain the expected home button tags")
    subparsers.add_parser("list-handbooks", help="list registered handbooks")
    subparsers.add_parser("add-handbook", help="interactive add handbook entry")
    subparsers.add_parser("edit-handbook", help="interactive edit handbook entry")
    subparsers.add_parser("remove-handbook", help="interactive remove handbook entry")
    subparsers.add_parser("menu", help="open interactive menu")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    command = args.command

    if command is None:
        if sys.stdin.isatty() and sys.stdout.isatty():
            return run_menu()
        print("未检测到交互式终端，已切换到默认校验模式。")
        print("如果你希望使用交互式菜单，请在终端中显式运行：python scripts/project_tools.py menu")
        result = cmd_verify()
        try:
            input("\n按回车退出...")
        except EOFError:
            pass
        return result

    if command == "verify":
        return cmd_verify()
    if command == "generate":
        return cmd_generate()
    if command == "validate":
        return cmd_validate()
    if command == "check-links":
        return cmd_check_links()
    if command == "inject-home-buttons":
        return cmd_inject_home_buttons()
    if command == "strip-home-buttons":
        return cmd_strip_home_buttons()
    if command == "check-home-buttons":
        return cmd_check_home_buttons()
    if command == "list-handbooks":
        return print_registry()
    if command == "add-handbook":
        return add_handbook_interactive()
    if command == "edit-handbook":
        return edit_handbook_interactive()
    if command == "remove-handbook":
        return remove_handbook_interactive()
    if command == "menu":
        return run_menu()

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
