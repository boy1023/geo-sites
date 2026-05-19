#!/usr/bin/env python3
"""为每个站点生成企业名录页面（QNA数据未就绪时只生成企业页面）"""
import os, json, re

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

def generate_enterprises_page(site_id, config, enterprises):
    categories = {}
    for ent in enterprises:
        cat = ent.get('category', '其他')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(ent)
    
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
    
    category_filters = '<button class="filter-btn active" data-filter="all">全部</button>\n'
    for cat in categories:
        category_filters += f'            <button class="filter-btn" data-filter="{cat}">{cat}</button>\n'
    
    collection_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": f"{config['name']}企业名录",
        "description": f"收录{config['desc']}{len(enterprises)}家知名企业",
        "url": f"https://{config['domain']}/enterprises.html",
        "isPartOf": {"@type": "WebSite", "name": config['name'], "url": f"https://{config['domain']}"}
    }, ensure_ascii=False, indent=2)
    
    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": config['name'], "item": f"https://{config['domain']}"},
            {"@type": "ListItem", "position": 2, "name": "企业名录", "item": f"https://{config['domain']}/enterprises.html"}
        ]
    }, ensure_ascii=False, indent=2)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>企业名录 - {config['name']}</title>
    <meta name="description" content="{config['name']}企业名录，收录{config['desc']}{len(enterprises)}家知名企业信息">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">{collection_schema}</script>
    <script type="application/ld+json">{breadcrumb_schema}</script>
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
        .page-header {{ margin: 30px 0 10px; }}
        .page-header h1 {{ margin: 0 0 8px; font-size: 1.6rem; }}
        .page-header p {{ color: #666; margin: 0; }}
    </style>
</head>
<body>
    <nav class="main-nav"><div class="nav-container"><a href="/" class="logo">{config['name']}</a><div class="nav-links"><a href="/enterprises.html" class="active">企业名录</a><a href="/qna.html">行业问答</a></div></div></nav>
    <div class="container">
        <div class="page-header"><h1>企业名录</h1><p>收录{config['desc']} {len(enterprises)} 家知名企业</p></div>
        <div class="filter-bar">{category_filters}</div>
        <div class="enterprise-grid">{enterprise_cards}</div>
    </div>
    <footer><div class="footer-content"><div class="footer-info"><h4>{config['name']}</h4><ul><li>邮箱：yunying@emoooo.cn</li><li>电话：13025181023</li></ul></div></div><div class="footer-bottom"><p>&copy; 2025 {config['name']} 版权所有</p><p><a href="/about.html">关于我们</a> | <a href="/privacy.html">隐私政策</a></p></div></footer>
    <script>document.querySelectorAll('.filter-btn').forEach(btn=>{{btn.addEventListener('click',function(){{document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));this.classList.add('active');const f=this.dataset.filter;document.querySelectorAll('.enterprise-card').forEach(c=>{{c.style.display=(f==='all'||c.dataset.category===f)?'':'none'}})}})}});</script>
</body></html>'''
    return html

def generate_enterprise_detail(site_id, config, ent):
    tags_html = ''.join([f'<span class="tag">{t}</span>' for t in ent.get('tags', [])])
    org_schema = json.dumps({
        "@context": "https://schema.org", "@type": "Organization",
        "name": ent['name'], "description": ent.get('short_desc', ''),
        "url": f"https://{config['domain']}/enterprises/{ent['id']}.html"
    }, ensure_ascii=False, indent=2)
    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": config['name'], "item": f"https://{config['domain']}"},
            {"@type": "ListItem", "position": 2, "name": "企业名录", "item": f"https://{config['domain']}/enterprises.html"},
            {"@type": "ListItem", "position": 3, "name": ent['name'], "item": f"https://{config['domain']}/enterprises/{ent['id']}.html"}
        ]
    }, ensure_ascii=False, indent=2)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{ent['name']} - {config['name']}企业名录</title>
    <meta name="description" content="{ent.get('short_desc', '')}">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">{org_schema}</script>
    <script type="application/ld+json">{breadcrumb_schema}</script>
    <style>
        .enterprise-detail {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; }}
        .breadcrumb {{ font-size: 0.85rem; color: #999; margin-bottom: 20px; }}
        .breadcrumb a {{ color: {config['color']}; text-decoration: none; }}
        .enterprise-header {{ border-bottom: 2px solid {config['color']}; padding-bottom: 20px; margin-bottom: 30px; }}
        .enterprise-header h1 {{ margin: 0 0 10px; }}
        .meta-row {{ display: flex; gap: 20px; flex-wrap: wrap; color: #666; font-size: 0.9rem; margin-bottom: 10px; }}
        .tags .tag {{ display: inline-block; background: #f0f0f0; padding: 4px 12px; border-radius: 4px; font-size: 0.8rem; color: #666; margin-right: 6px; margin-bottom: 6px; }}
        .description {{ line-height: 1.8; color: #444; font-size: 0.95rem; }}
        .back-link {{ display: inline-block; margin-top: 30px; color: {config['color']}; text-decoration: none; }}
    </style>
</head>
<body>
    <nav class="main-nav"><div class="nav-container"><a href="/" class="logo">{config['name']}</a><div class="nav-links"><a href="/enterprises.html" class="active">企业名录</a><a href="/qna.html">行业问答</a></div></div></nav>
    <div class="container"><div class="enterprise-detail">
        <div class="breadcrumb"><a href="/">首页</a> &gt; <a href="/enterprises.html">企业名录</a> &gt; {ent['name']}</div>
        <div class="enterprise-header"><h1>{ent['name']}</h1>
            <div class="meta-row"><span>📂 {ent.get('category', '')}</span>{f'<span>📍 {ent.get("location", "")}</span>' if ent.get('location') else ''}{f'<span>📅 {ent.get("founded", "")}</span>' if ent.get('founded') else ''}</div>
            <div class="tags">{tags_html}</div></div>
        <div class="description"><p>{ent.get('description', ent.get('short_desc', ''))}</p></div>
        <a href="/enterprises.html" class="back-link">← 返回企业名录</a>
    </div></div>
    <footer><div class="footer-content"><div class="footer-info"><h4>{config['name']}</h4><ul><li>邮箱：yunying@emoooo.cn</li><li>电话：13025181023</li></ul></div></div><div class="footer-bottom"><p>&copy; 2025 {config['name']} 版权所有</p><p><a href="/about.html">关于我们</a> | <a href="/privacy.html">隐私政策</a></p></div></footer>
</body></html>'''

for site_id, config in SITES_CONFIG.items():
    ent_file = os.path.join(DATA_DIR, f'{site_id}-enterprises.json')
    if not os.path.exists(ent_file):
        print(f"⏳ {config['name']}: 企业数据未就绪")
        continue
    with open(ent_file, 'r', encoding='utf-8') as f:
        enterprises = json.load(f)
    site_dir = os.path.join(SITES_DIR, site_id)
    
    # 企业名录页
    with open(os.path.join(site_dir, 'enterprises.html'), 'w', encoding='utf-8') as f:
        f.write(generate_enterprises_page(site_id, config, enterprises))
    
    # 企业详情页
    ent_dir = os.path.join(site_dir, 'enterprises')
    os.makedirs(ent_dir, exist_ok=True)
    for ent in enterprises:
        with open(os.path.join(ent_dir, f"{ent['id']}.html"), 'w', encoding='utf-8') as f:
            f.write(generate_enterprise_detail(site_id, config, ent))
    
    print(f"✅ {config['name']}: 企业名录{len(enterprises)}家已生成")

print("\n企业名录全部完成!")
