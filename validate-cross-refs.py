#!/usr/bin/env python3
import os
import re

base_dir = '/workspace/doc/maoyuu'

# 收集所有知识点ID
topic_ids = []
for filename in os.listdir(base_dir):
    if filename.endswith('.html') and not filename.startswith('_'):
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # 提取所有知识点ID
            matches = re.findall(r'id="topic-(\d+-\d+)"', content)
            for match in matches:
                topic_ids.append((filename, match))

# 构建知识点ID到文件的映射
id_to_file = {}
for filename, topic_id in topic_ids:
    id_to_file[topic_id] = filename

# 检查所有交叉引用链接
errors = []
warnings = []

for filename in os.listdir(base_dir):
    if filename.endswith('.html') and not filename.startswith('_'):
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # 提取所有交叉引用链接
            links = re.findall(r'<a href="([^"]+)" class="cross-ref"', content)
            for link in links:
                # 解析链接
                if '#' in link:
                    page_path, anchor = link.split('#', 1)
                    topic_id = anchor.replace('topic-', '')
                else:
                    page_path = link
                    anchor = ''
                    topic_id = ''
                
                # 检查页面是否存在
                full_page_path = os.path.join(base_dir, page_path)
                if not os.path.exists(full_page_path):
                    errors.append(f"{filename}: 链接指向不存在的页面: {link}")
                    continue
                
                # 检查锚点是否存在
                if anchor:
                    with open(full_page_path, 'r', encoding='utf-8') as pf:
                        page_content = pf.read()
                        if f'id="{anchor}"' not in page_content:
                            errors.append(f"{filename}: 锚点不存在: {link}")

# 检查引用对称性
# 构建引用关系图（正确方式：每个知识点只包含自己的交叉引用）
refs = {}
for filename in os.listdir(base_dir):
    if filename.endswith('.html') and not filename.startswith('_'):
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        topic_pattern = r'id="topic-(\d+-\d+)"'
        topic_matches = list(re.finditer(topic_pattern, content))
        
        for i, topic_match in enumerate(topic_matches):
            topic_id = topic_match.group(1)
            refs[topic_id] = []
            
            # 确定当前知识点的结束位置（下一个知识点开始或文件末尾）
            if i < len(topic_matches) - 1:
                topic_end = topic_matches[i + 1].start()
            else:
                topic_end = len(content)
            
            # 在当前知识点范围内查找交叉引用
            topic_content = content[topic_match.start():topic_end]
            links = re.findall(r'<a href="([^"]+)" class="cross-ref"', topic_content)
            
            for link in links:
                if '#' in link:
                    target_id = link.split('#')[1].replace('topic-', '')
                    if target_id != topic_id:
                        refs[topic_id].append(target_id)

# 检查对称性
for source, targets in refs.items():
    for target in targets:
        if source not in refs.get(target, []):
            warnings.append(f"引用不对称: {source} → {target}，但 {target} 没有反向引用 {source}")

# 输出结果
print("=" * 60)
print("交叉引用验证报告")
print("=" * 60)

if errors:
    print("\n❌ 错误（链接无效）:")
    for error in errors:
        print(f"  - {error}")
else:
    print("\n✅ 所有链接路径有效")

if warnings:
    print("\n⚠️ 警告（引用不对称）:")
    for warning in warnings:
        print(f"  - {warning}")
else:
    print("\n✅ 所有引用关系对称")

print(f"\n总知识点数: {len(topic_ids)}")
print(f"总文件数: {len([f for f in os.listdir(base_dir) if f.endswith('.html') and not f.startswith('_')])}")
