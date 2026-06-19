#!/usr/bin/env python3

cross_refs = {
    # 第1卷：农业革命与启蒙
    '1-1': ['1-2', '1-3', '5-1'],
    '1-2': ['1-1', '2-3', '1-3'],
    '1-3': ['1-1', '1-2', '3-3', '5-2'],
    '1-4': ['1-5', '4-3', '6-2'],
    '1-5': ['1-4', '4-7', '1-6'],
    '1-6': ['3-4', '5-6', '1-5', '4-1'],
    
    # 第2卷：贸易网络与地缘政治
    '2-1': ['3-1', '4-5', '5-1'],
    '2-2': ['5-1', '2-1', '1-1'],
    '2-3': ['1-2', '4-5', '4-6'],
    '2-4': ['5-3', '3-2', '6-1'],
    '2-5': ['1-4', '4-7'],
    
    # 第3卷：军事外交与权力平衡
    '3-1': ['2-1', '4-5', '3-4'],
    '3-2': ['5-3', '2-4', '5-5'],
    '3-3': ['1-3', '5-2', '7-2'],
    '3-4': ['1-6', '4-6', '7-1'],
    
    # 第4卷：宗教改革与社会变革
    '4-1': ['4-4', '5-6', '1-6', '8-1'],
    '4-2': ['4-3', '5-4', '6-1'],
    '4-3': ['1-4', '4-2', '5-4'],
    '4-4': ['4-1', '4-7'],
    '4-5': ['2-1', '2-3', '3-1'],
    '4-6': ['4-5', '3-4', '4-7'],
    '4-7': ['1-5', '2-5', '4-4', '4-6'],
    
    # 第5卷：和平谈判与秩序重建
    '5-1': ['2-2', '1-1', '2-1'],
    '5-2': ['3-3', '1-3', '6-2'],
    '5-3': ['2-4', '3-2', '5-5'],
    '5-4': ['4-2', '4-3', '7-2', '8-2'],
    '5-5': ['3-2', '5-3', '1-6'],
    '5-6': ['1-6', '4-1'],
    
    # 番外卷
    '6-1': ['4-2', '2-4'],
    '6-2': ['1-4', '5-2'],
    '7-1': ['3-4'],
    '7-2': ['3-3', '5-4'],
    '8-1': ['4-1', '4-2'],
    '8-2': ['5-4', '3-3'],
}

# 添加反向引用
for source, targets in list(cross_refs.items()):
    for target in targets:
        if target not in cross_refs:
            cross_refs[target] = []
        if source not in cross_refs[target]:
            cross_refs[target].append(source)

# 知识点标题映射
topic_titles = {
    '1-1': '马铃薯引进与粮食革命',
    '1-2': '四圃轮作制与农业效率',
    '1-3': '风车技术与能源利用',
    '1-4': '活版印刷与知识传播',
    '1-5': '教育启蒙与人力资本投资',
    '1-6': '魔王的经济改革动机',
    '2-1': '商人同盟与行会垄断',
    '2-2': '开门都市的跨境贸易',
    '2-3': '供需关系与价格机制',
    '2-4': '忽邻塔氏族会议',
    '2-5': '信息不对称与商人网络',
    '3-1': '盐贸易与资源垄断',
    '3-2': '军事外交与同盟博弈',
    '3-3': '火绳枪与军事技术革命',
    '3-4': '战争经济与军事凯恩斯主义',
    '4-1': '"我是人类"演说与天赋人权',
    '4-2': '异端审判与宗教压迫',
    '4-3': '宗教改革与世俗化',
    '4-4': '农奴解放与劳动力流动',
    '4-5': '期货交易与价格操纵',
    '4-6': '通货膨胀与货币信用',
    '4-7': '人才流动与知识溢出',
    '5-1': '人魔自由贸易与比较优势',
    '5-2': '火绳枪与军事革命',
    '5-3': '三国联盟与多极体系',
    '5-4': '圣键远征军与宗教战争',
    '5-5': '光之玉与核威慑博弈',
    '5-6': '和平秩序与制度构建',
    '6-1': '魔界社会结构与知识垄断',
    '6-2': '知识获取与技术转移',
    '7-1': '战争经历与创伤经济学',
    '7-2': '旧制度下的军人社会角色',
    '8-1': '女性觉醒与女性主义萌芽',
    '8-2': '军事组织中的性别政治',
}

# 知识点ID到文件的映射
topic_to_file = {
    '1-1': 'vol-01-agricultural-revolution.html',
    '1-2': 'vol-01-agricultural-revolution.html',
    '1-3': 'vol-01-agricultural-revolution.html',
    '1-4': 'vol-01-agricultural-revolution.html',
    '1-5': 'vol-01-agricultural-revolution.html',
    '1-6': 'vol-01-agricultural-revolution.html',
    '2-1': 'vol-02-trade-network.html',
    '2-2': 'vol-02-trade-network.html',
    '2-3': 'vol-02-trade-network.html',
    '2-4': 'vol-02-trade-network.html',
    '2-5': 'vol-02-trade-network.html',
    '3-1': 'vol-03-military-diplomacy.html',
    '3-2': 'vol-03-military-diplomacy.html',
    '3-3': 'vol-03-military-diplomacy.html',
    '3-4': 'vol-03-military-diplomacy.html',
    '4-1': 'vol-04-religious-reform.html',
    '4-2': 'vol-04-religious-reform.html',
    '4-3': 'vol-04-religious-reform.html',
    '4-4': 'vol-04-religious-reform.html',
    '4-5': 'vol-04-religious-reform.html',
    '4-6': 'vol-04-religious-reform.html',
    '4-7': 'vol-04-religious-reform.html',
    '5-1': 'vol-05-peace-order.html',
    '5-2': 'vol-05-peace-order.html',
    '5-3': 'vol-05-peace-order.html',
    '5-4': 'vol-05-peace-order.html',
    '5-5': 'vol-05-peace-order.html',
    '5-6': 'vol-05-peace-order.html',
    '6-1': 'vol-06-mage-side-story.html',
    '6-2': 'vol-06-mage-side-story.html',
    '7-1': 'vol-07-archer-side-story.html',
    '7-2': 'vol-07-archer-side-story.html',
    '8-1': 'vol-08-knight-side-story.html',
    '8-2': 'vol-08-knight-side-story.html',
}

import os

base_dir = '/workspace/doc/maoyuu'

def generate_cross_ref_html(topic_id):
    targets = sorted(cross_refs.get(topic_id, []))
    links = []
    for target in targets:
        filename = topic_to_file[target]
        title = topic_titles[target]
        links.append(f'          <a href="{filename}#topic-{target}" class="cross-ref" data-ref="{target}">→{target} {title}</a>')
    return '\n'.join(links)

for topic_id, targets in cross_refs.items():
    filename = topic_to_file[topic_id]
    filepath = os.path.join(base_dir, filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_ref_html = generate_cross_ref_html(topic_id)
    
    pattern_start = f'<div class="cross-ref-group">\n'
    pattern_end = f'\n        </div>'
    
    import re
    
    topic_start = content.find(f'id="topic-{topic_id}"')
    if topic_start == -1:
        print(f"Warning: topic-{topic_id} not found in {filename}")
        continue
    
    ref_start = content.find('<div class="cross-ref-group">', topic_start)
    if ref_start == -1:
        print(f"Warning: cross-ref-group not found for topic-{topic_id} in {filename}")
        continue
    
    ref_end = content.find('</div>', ref_start)
    if ref_end == -1:
        print(f"Warning: closing </div> not found for topic-{topic_id} in {filename}")
        continue
    
    content = content[:ref_start] + pattern_start + new_ref_html + pattern_end + content[ref_end+6:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {filename}: topic-{topic_id}")

print("\nDone!")
