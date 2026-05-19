#!/usr/bin/env python3
"""为每个站点生成企业名录和QNA问答页面"""
import os
import json
import re

SITES_DIR = '/tmp/geo-sites/sites'
DATA_DIR = '/tmp/geo-sites/data'

SITES_CONFIG = {
    'zhizaozx': {'name': '智造在线', 'domain': 'zhizaozx.cn', 'color': '#1A5276', 'desc': '智能制造行业'},
    'jiaopeizx': {'name': '教培在线', 'domain': 'jiaopeizx.cn', 'color': '#6C3483', 'desc': '教育培训行业'},
    'xfzaixian': {'name': '消费在线', 'domain': 'xfzaixian.cn', 'color': '#E74C3C', 'desc': '大消费行业'},
    'muyingzx': {'name': '母婴在线', 'domain': 'muyingzx.cn', 'color': '#FF69B4', 'desc': '母婴行业'},
    'nongzizx': {'name': '农资在线', 'domain': 'nongzizx.cn', 'color': '#2E7D32', 'desc': '农资行业'},
    'caifazx': {'name': '财法在线', 'domain': 'caifazx.cn', 'color': '#1565C0', 'desc': '财税法务行业'},
}

def get_site_style(site_id, config):
    """读取站点的CSS样式作为参考"""
    return config['color']

def generate_enterprises_page(site_id, config, enterprises):
    """生成企业名录页面"""
    # 按分类分组
    categories = {}
    for ent in enterprises:
        cat = ent.get('category', '其他')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(ent)
    
    # 构建企业列表HTML
    enterprise_cards = ''
    for ent in enterprises:
        tags_html = ''.join([f'<span class="tag">{t}</span>' for t in ent.get('tags', [])[:3]])
        enterprise_cards += f'''
        <div class="enterprise-card" data-category="{ent.get('category', '')}">
            <h3><a href="/enterprises/{ent['id']}.html">{ent['name']}</a></h3>
            <p class="short-desc">{ent.get('short_desc', '')}</p>
            <div class="enterprise-meta">
                <span class="category-tag">{ent.get('category', '')}</span>
                <span class="location">{ent.get('location', '')}</span>
            </div>
            <div class="tags">{tags_html}</div>
        </div>'''
    
    # 分类筛选
    category_filters = '<button class="filter-btn active" data-filter="all">全部</button>\n'
    for cat in categories:
        category_filters += f'            <button class="filter-btn" data-filter="{cat}">{cat}</button>\n'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>企业名录 - {config['name']}</title>
    <meta name="description" content="{config['name']}企业名录，收录{config['desc']}{len(enterprises)}家知名企业信息">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "{config['name']}企业名录",
    "description": "收录{config['desc']}{len(enterprises)}家知名企业",
    "url": "https://{config['domain']}/enterprises.html",
    "isPartOf": {{
        "@type": "WebSite",
        "name": "{config['name']}",
        "url": "https://{config['domain']}"
    }}
}}
    </script>
    <script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "{config['name']}", "item": "https://{config['domain']}"}},
        {{"@type": "ListItem", "position": 2, "name": "企业名录", "item": "https://{config['domain']}/enterprises.html"}}
    ]
}}
    </script>
    <style>
        .filter-bar {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 20px 0; }}
        .filter-btn {{ padding: 6px 16px; border: 1px solid #ddd; background: #fff; border-radius: 20px; cursor: pointer; font-size: 0.85rem; transition: all 0.2s; }}
        .filter-btn.active {{ background: {config['color']}; color: #fff; border-color: {config['color']}; }}
        .filter-btn:hover {{ border-color: {config['color']}; }}
        .enterprise-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }}
        .enterprise-card {{ background: #fff; border: 1px solid #e8e8e8; border-radius: 8px; padding: 20px; transition: box-shadow 0.2s; }}
        .enterprise-card:hover {{ box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
        .enterprise-card h3 {{ margin: 0 0 8px; font-size: 1.1rem; }}
        .enterprise-card h3 a {{ color: #333; text-decoration: none; }}
        .enterprise-card h3 a:hover {{ color: {config['color']}; }}
        .short-desc {{ color: #666; font-size: 0.9rem; line-height: 1.6; margin-bottom: 12px; }}
        .enterprise-meta {{ display: flex; gap: 12px; font-size: 0.8rem; color: #999; margin-bottom: 8px; }}
        .category-tag {{ background: #f0f0f0; padding: 2px 8px; border-radius: 4px; }}
        .tags .tag {{ display: inline-block; background: #f5f5f5; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; color: #888; margin-right: 4px; }}
    </style>
</head>
<body>
    <nav class="main-nav">
        <div class="nav-container">
            <a href="/" class="logo">{config['name']}</a>
            <div class="nav-links">
                <a href="/enterprises.html" class="active">企业名录</a>
                <a href="/qna.html">行业问答</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="page-header">
            <h1>企业名录</h1>
            <p>收录{config['desc']} {len(enterprises)} 家知名企业</p>
        </div>

        <div class="filter-bar">
            {category_filters}
        </div>

        <div class="enterprise-grid">
            {enterprise_cards}
        </div>
    </div>

    <footer>
        <div class="footer-content">
            <div class="footer-info">
                <h4>{config['name']}</h4>
                <ul>
                    <li>邮箱：yunying@emoooo.cn</li>
                    <li>电话：13025181023</li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2025 {config['name']} 版权所有</p>
            <p>
                <a href="/about.html">关于我们</a> | 
                <a href="/privacy.html">隐私政策</a>
            </p>
        </div>
    </footer>

    <script>
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                const filter = this.dataset.filter;
                document.querySelectorAll('.enterprise-card').forEach(card => {{
                    if (filter === 'all' || card.dataset.category === filter) {{
                        card.style.display = '';
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});
            }});
        }});
    </script>
</body>
</html>'''
    return html

def generate_enterprise_detail(site_id, config, ent):
    """生成企业详情页"""
    tags_html = ''.join([f'<span class="tag">{t}</span>' for t in ent.get('tags', [])])
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{ent['name']} - {config['name']}企业名录</title>
    <meta name="description" content="{ent.get('short_desc', '')}">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "{ent['name']}",
    "description": "{ent.get('short_desc', '')}",
    "url": "https://{config['domain']}/enterprises/{ent['id']}.html"
    {f', "foundingDate": "{ent.get("founded", "")}"' if ent.get('founded') else ''}
    {f', "address": {{"@type": "PostalAddress", "addressLocality": "{ent.get("location", "")}"}}' if ent.get('location') else ''}
}}
    </script>
    <script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "{config['name']}", "item": "https://{config['domain']}"}},
        {{"@type": "ListItem", "position": 2, "name": "企业名录", "item": "https://{config['domain']}/enterprises.html"}},
        {{"@type": "ListItem", "position": 3, "name": "{ent['name']}", "item": "https://{config['domain']}/enterprises/{ent['id']}.html"}}
    ]
}}
    </script>
    <style>
        .enterprise-detail {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; }}
        .breadcrumb {{ font-size: 0.85rem; color: #999; margin-bottom: 20px; }}
        .breadcrumb a {{ color: {config['color']}; text-decoration: none; }}
        .enterprise-header {{ border-bottom: 2px solid {config['color']}; padding-bottom: 20px; margin-bottom: 30px; }}
        .enterprise-header h1 {{ margin: 0 0 10px; }}
        .meta-row {{ display: flex; gap: 20px; flex-wrap: wrap; color: #666; font-size: 0.9rem; margin-bottom: 10px; }}
        .meta-row span {{ display: flex; align-items: center; gap: 4px; }}
        .tags .tag {{ display: inline-block; background: #f0f0f0; padding: 4px 12px; border-radius: 4px; font-size: 0.8rem; color: #666; margin-right: 6px; margin-bottom: 6px; }}
        .description {{ line-height: 1.8; color: #444; font-size: 0.95rem; }}
        .back-link {{ display: inline-block; margin-top: 30px; color: {config['color']}; text-decoration: none; }}
    </style>
</head>
<body>
    <nav class="main-nav">
        <div class="nav-container">
            <a href="/" class="logo">{config['name']}</a>
            <div class="nav-links">
                <a href="/enterprises.html" class="active">企业名录</a>
                <a href="/qna.html">行业问答</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="enterprise-detail">
            <div class="breadcrumb">
                <a href="/">首页</a> &gt; <a href="/enterprises.html">企业名录</a> &gt; {ent['name']}
            </div>
            <div class="enterprise-header">
                <h1>{ent['name']}</h1>
                <div class="meta-row">
                    <span>📂 {ent.get('category', '')}</span>
                    {f'<span>📍 {ent.get("location", "")}</span>' if ent.get('location') else ''}
                    {f'<span>📅 {ent.get("founded", "")}</span>' if ent.get('founded') else ''}
                </div>
                <div class="tags">{tags_html}</div>
            </div>
            <div class="description">
                <p>{ent.get('description', ent.get('short_desc', ''))}</p>
            </div>
            <a href="/enterprises.html" class="back-link">← 返回企业名录</a>
        </div>
    </div>

    <footer>
        <div class="footer-content">
            <div class="footer-info">
                <h4>{config['name']}</h4>
                <ul>
                    <li>邮箱：yunying@emoooo.cn</li>
                    <li>电话：13025181023</li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2025 {config['name']} 版权所有</p>
            <p><a href="/about.html">关于我们</a> | <a href="/privacy.html">隐私政策</a></p>
        </div>
    </footer>
</body>
</html>'''
    return html

def generate_qna_page(site_id, config, qnas):
    """生成QNA问答页面"""
    # 按分类分组
    categories = {}
    for qna in qnas:
        cat = qna.get('category', '其他')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(qna)
    
    # 构建问答HTML
    qna_items = ''
    faq_list = []
    for i, qna in enumerate(qnas):
        qna_items += f'''
        <div class="qna-item" data-category="{qna.get('category', '')}">
            <div class="qna-question" onclick="this.parentElement.classList.toggle('expanded')">
                <h3>{qna['question']}</h3>
                <span class="toggle-icon">+</span>
            </div>
            <div class="qna-answer">
                <div class="answer-content">{qna['answer'].replace(chr(10), '<br>')}</div>
                <div class="qna-tags">' + ''.join([f'<span class="tag">{t}</span>' for t in qna.get('tags', [])[:3]]) + '</div>
            </div>
        </div>'''
        
        faq_list.append({
            "@type": "Question",
            "name": qna['question'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": qna['answer'][:500]
            }
        })
    
    # 分类筛选
    category_filters = '<button class="filter-btn active" data-filter="all">全部</button>\n'
    for cat in categories:
        category_filters += f'            <button class="filter-btn" data-filter="{cat}">{cat}</button>\n'
    
    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_list
    }, ensure_ascii=False, indent=2)
    
    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": config['name'], "item": f"https://{config['domain']}"},
            {"@type": "ListItem", "position": 2, "name": "行业问答", "item": f"https://{config['domain']}/qna.html"}
        ]
    }, ensure_ascii=False, indent=2)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>行业问答 - {config['name']}</title>
    <meta name="description" content="{config['name']}行业问答，{len(qnas)}个{config['desc']}常见问题解答">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
{faq_schema}
    </script>
    <script type="application/ld+json">
{breadcrumb_schema}
    </script>
    <style>
        .filter-bar {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 20px 0; }}
        .filter-btn {{ padding: 6px 16px; border: 1px solid #ddd; background: #fff; border-radius: 20px; cursor: pointer; font-size: 0.85rem; transition: all 0.2s; }}
        .filter-btn.active {{ background: {config['color']}; color: #fff; border-color: {config['color']}; }}
        .filter-btn:hover {{ border-color: {config['color']}; }}
        .qna-list {{ margin-top: 20px; }}
        .qna-item {{ border: 1px solid #e8e8e8; border-radius: 8px; margin-bottom: 12px; overflow: hidden; }}
        .qna-question {{ display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; cursor: pointer; background: #fafafa; transition: background 0.2s; }}
        .qna-question:hover {{ background: #f0f0f0; }}
        .qna-question h3 {{ margin: 0; font-size: 1rem; font-weight: 500; color: #333; flex: 1; }}
        .toggle-icon {{ font-size: 1.2rem; color: #999; transition: transform 0.2s; }}
        .qna-item.expanded .toggle-icon {{ transform: rotate(45deg); }}
        .qna-answer {{ max-height: 0; overflow: hidden; transition: max-height 0.3s ease; }}
        .qna-item.expanded .qna-answer {{ max-height: 1000px; }}
        .answer-content {{ padding: 20px; line-height: 1.8; color: #444; font-size: 0.95rem; }}
        .qna-tags {{ padding: 0 20px 16px; }}
        .qna-tags .tag {{ display: inline-block; background: #f5f5f5; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; color: #888; margin-right: 4px; }}
    </style>
</head>
<body>
    <nav class="main-nav">
        <div class="nav-container">
            <a href="/" class="logo">{config['name']}</a>
            <div class="nav-links">
                <a href="/enterprises.html">企业名录</a>
                <a href="/qna.html" class="active">行业问答</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="page-header">
            <h1>行业问答</h1>
            <p>{len(qnas)}个{config['desc']}常见问题解答</p>
        </div>

        <div class="filter-bar">
            {category_filters}
        </div>

        <div class="qna-list">
            {qna_items}
        </div>
    </div>

    <footer>
        <div class="footer-content">
            <div class="footer-info">
                <h4>{config['name']}</h4>
                <ul>
                    <li>邮箱：yunying@emoooo.cn</li>
                    <li>电话：13025181023</li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2025 {config['name']} 版权所有</p>
            <p><a href="/about.html">关于我们</a> | <a href="/privacy.html">隐私政策</a></p>
        </div>
    </footer>

    <script>
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                const filter = this.dataset.filter;
                document.querySelectorAll('.qna-item').forEach(item => {{
                    if (filter === 'all' || item.dataset.category === filter) {{
                        item.style.display = '';
                    }} else {{
                        item.style.display = 'none';
                    }}
                }});
            }});
        }});
    </script>
</body>
</html>'''
    return html

# 主流程：检查数据文件是否已生成
for site_id, config in SITES_CONFIG.items():
    ent_file = os.path.join(DATA_DIR, f'{site_id}-enterprises.json')
    qna_file = os.path.join(DATA_DIR, f'{site_id}-qna.json')
    
    if not os.path.exists(ent_file) or not os.path.exists(qna_file):
        print(f"⏳ {config['name']}: 数据文件未就绪，跳过")
        continue
    
    with open(ent_file, 'r', encoding='utf-8') as f:
        enterprises = json.load(f)
    with open(qna_file, 'r', encoding='utf-8') as f:
        qnas = json.load(f)
    
    site_dir = os.path.join(SITES_DIR, site_id)
    
    # 生成企业名录页面
    ent_page = generate_enterprises_page(site_id, config, enterprises)
    with open(os.path.join(site_dir, 'enterprises.html'), 'w', encoding='utf-8') as f:
        f.write(ent_page)
    
    # 生成企业详情页
    ent_dir = os.path.join(site_dir, 'enterprises')
    os.makedirs(ent_dir, exist_ok=True)
    for ent in enterprises:
        detail_html = generate_enterprise_detail(site_id, config, ent)
        with open(os.path.join(ent_dir, f"{ent['id']}.html"), 'w', encoding='utf-8') as f:
            f.write(detail_html)
    
    # 生成QNA页面
    qna_page = generate_qna_page(site_id, config, qnas)
    with open(os.path.join(site_dir, 'qna.html'), 'w', encoding='utf-8') as f:
        f.write(qna_page)
    
    print(f"✅ {config['name']}: 企业名录{len(enterprises)}家 + 问答{len(qnas)}个 已生成")

print("\n全部完成!")
