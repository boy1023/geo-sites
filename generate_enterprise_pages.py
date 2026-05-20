#!/usr/bin/env python3
"""为每个站点生成企业名录页面（使用统一导航栏和Footer）"""
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

SITES_CATEGORIES = {
    'zhizaozx': [
        {'name': '行业资讯', 'slug': 'industry-news'},
        {'name': '机电设备与动力系统', 'slug': 'mechanical-power'},
        {'name': '电气控制与传感', 'slug': 'electrical-control'},
        {'name': '金属加工与制造', 'slug': 'metal-processing'},
    ],
    'jiaopeizx': [
        {'name': '行业资讯', 'slug': 'industry-news'},
        {'name': '课程培训', 'slug': 'courses'},
        {'name': '教育技术', 'slug': 'edtech'},
        {'name': '素质教育', 'slug': 'quality-education'},
    ],
    'xfzaixian': [
        {'name': '行业资讯', 'slug': 'industry-news'},
        {'name': '零售业态', 'slug': 'retail'},
        {'name': '餐饮服务', 'slug': 'food-service'},
        {'name': '消费品', 'slug': 'consumer-goods'},
    ],
    'muyingzx': [
        {'name': '行业资讯', 'slug': 'industry-news'},
        {'name': '奶粉辅食', 'slug': 'formula-food'},
        {'name': '母婴用品', 'slug': 'baby-products'},
        {'name': '育儿教育', 'slug': 'parenting'},
    ],
    'nongzizx': [
        {'name': '行业资讯', 'slug': 'industry-news'},
        {'name': '种子种苗', 'slug': 'seeds'},
        {'name': '农药化肥', 'slug': 'pesticides'},
        {'name': '农业机械', 'slug': 'agri-machinery'},
    ],
    'caifazx': [
        {'name': '行业资讯', 'slug': 'industry-news'},
        {'name': '财税政策', 'slug': 'tax-policy'},
        {'name': '法律服务', 'slug': 'legal-service'},
        {'name': '知识产权', 'slug': 'ip-rights'},
    ],
}


def generate_nav(site_id, config, active_page=''):
    """生成统一导航栏HTML"""
    categories = SITES_CATEGORIES.get(site_id, [])
    
    nav_items = '''
    <header class="site-header">
        <div class="container">
            <div class="header-inner">
                <a href="/" class="logo">
                    <span class="logo-text">''' + config['name'] + '''</span>
                </a>
                <nav class="main-nav">
                    <button class="nav-toggle" aria-label="菜单">
                        <span></span><span></span><span></span>
                    </button>
                    <ul class="nav-list">
                        <li class="nav-item"><a href="/" class="nav-link''' + (' active' if active_page == 'home' else '') + '''">首页</a></li>'''
    
    for cat in categories[:4]:
        nav_items += '''
                        <li class="nav-item"><a href="/categories/''' + cat['slug'] + '''.html" class="nav-link''' + (' active' if active_page == 'cat-' + cat["slug"] else '') + '''">''' + cat['name'] + '''</a></li>'''
    
    nav_items += '''
                        <li class="nav-item"><a href="/enterprises.html" class="nav-link''' + (' active' if active_page == 'enterprises' else '') + '''">企业名录</a></li>
                        <li class="nav-item"><a href="/qna.html" class="nav-link''' + (' active' if active_page == 'qna' else '') + '''">行业问答</a></li>
                        <li class="nav-item"><a href="/about.html" class="nav-link''' + (' active' if active_page == 'about' else '') + '''">关于我们</a></li>
                    </ul>
                </nav>
                <div class="header-search">
                    <form action="/search.html" method="get">
                        <input type="text" name="q" placeholder="搜索文章..." aria-label="搜索">
                        <button type="submit">🔍</button>
                    </form>
                </div>
            </div>
        </div>
    </header>'''
    
    return nav_items


def generate_footer(config):
    """生成统一Footer HTML"""
    return '''
    <footer class="site-footer">
        <div class="container">
            <div class="footer-inner">
                <div class="footer-about">
                    <h3>''' + config['name'] + '''</h3>
                    <p>''' + config['desc'] + '''权威资讯平台，为从业者提供专业、前沿的行业资讯。</p>
                </div>
                <div class="footer-links">
                    <h4>快速链接</h4>
                    <ul>
                        <li><a href="/">首页</a></li>
                        <li><a href="/enterprises.html">企业名录</a></li>
                        <li><a href="/qna.html">行业问答</a></li>
                        <li><a href="/about.html">关于我们</a></li>
                        <li><a href="/sitemap.xml">网站地图</a></li>
                    </ul>
                </div>
                <div class="footer-categories">
                    <h4>行业分类</h4>
                    <ul>
                        <li><a href="/categories/industry-news.html">行业资讯</a></li>
                        <li><a href="/categories/">更多分类</a></li>
                    </ul>
                </div>
                <div class="footer-contact">
                    <h4>联系我们</h4>
                    <ul>
                        <li>邮箱：yunying@emoooo.cn</li>
                        <li>电话：13025181023</li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2025 ''' + config['name'] + ''' 版权所有</p>
                <p>
                    <a href="/about.html">关于我们</a> | 
                    <a href="/about.html">关于我们</a> | <a href="/privacy.html">隐私政策</a>
                </p>
            </div>
        </div>
    </footer>'''


def generate_enterprises_page(site_id, config, enterprises):
    """生成企业名录页面"""
    categories = {}
    for ent in enterprises:
        cat = ent.get('category', '其他')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(ent)
    
    enterprise_cards = ''
    for ent in enterprises:
        tags_html = ''.join(['<span class="tag">' + t + '</span>' for t in ent.get('tags', [])[:3]])
        enterprise_cards += '''
        <div class="enterprise-card" data-category="''' + (ent.get('category', '') or '') + '''">
            <h3><a href="/enterprises/''' + ent['id'] + '''.html">''' + ent['name'] + '''</a></h3>
            <p class="short-desc">''' + (ent.get('short_desc', '') or '') + '''</p>
            <div class="enterprise-meta">
                <span class="category-tag">''' + (ent.get('category', '') or '') + '''</span>
                <span class="location">📍 ''' + (ent.get('location', '') or '') + '''</span>
            </div>
            <div class="tags">''' + tags_html + '''</div>
        </div>'''
    
    category_filters = '<button class="filter-btn active" data-filter="all">全部</button>\n'
    for cat in categories:
        category_filters += '            <button class="filter-btn" data-filter="' + cat + '">' + cat + '</button>\n'
    
    collection_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": config['name'] + "企业名录",
        "description": "收录" + config['desc'] + str(len(enterprises)) + "家知名企业",
        "url": "https://" + config['domain'] + "/enterprises.html",
        "isPartOf": {"@type": "WebSite", "name": config['name'], "url": "https://" + config['domain']}
    }, ensure_ascii=False, indent=2)
    
    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": config['name'], "item": "https://" + config['domain']},
            {"@type": "ListItem", "position": 2, "name": "企业名录", "item": "https://" + config['domain'] + "/enterprises.html"}
        ]
    }, ensure_ascii=False, indent=2)
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>企业名录 - ''' + config['name'] + '''</title>
    <meta name="description" content="''' + config['name'] + '''企业名录，收录''' + config['desc'] + str(len(enterprises)) + '''家知名企业信息">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
''' + collection_schema + '''
    </script>
    <script type="application/ld+json">
''' + breadcrumb_schema + '''
    </script>
    <style>
        .filter-bar { display: flex; flex-wrap: wrap; gap: 8px; margin: 20px 0; }
        .filter-btn { padding: 6px 16px; border: 1px solid #ddd; background: #fff; border-radius: 20px; cursor: pointer; font-size: 0.85rem; transition: all 0.2s; }
        .filter-btn.active { background: ''' + config['color'] + '''; color: #fff; border-color: ''' + config['color'] + '''; }
        .filter-btn:hover { border-color: ''' + config['color'] + '''; }
        .enterprise-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
        .enterprise-card { background: #fff; border: 1px solid #e8e8e8; border-radius: 8px; padding: 20px; transition: box-shadow 0.2s; }
        .enterprise-card:hover { box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
        .enterprise-card h3 { margin: 0 0 8px; font-size: 1.1rem; }
        .enterprise-card h3 a { color: #333; text-decoration: none; }
        .enterprise-card h3 a:hover { color: ''' + config['color'] + '''; }
        .short-desc { color: #666; font-size: 0.9rem; line-height: 1.6; margin-bottom: 12px; }
        .enterprise-meta { display: flex; gap: 12px; font-size: 0.8rem; color: #999; margin-bottom: 8px; }
        .category-tag { background: #f0f0f0; padding: 2px 8px; border-radius: 4px; }
        .tags .tag { display: inline-block; background: #f5f5f5; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; color: #888; margin-right: 4px; }
        .page-header { text-align: center; padding: 40px 0 20px; }
        .page-header h1 { margin-bottom: 8px; }
        .page-header p { color: #666; }
        .main-content { min-height: 60vh; padding-bottom: 40px; }
    </style>
</head>
<body>
    ''' + generate_nav(site_id, config, 'enterprises') + '''

    <main class="main-content">
        <div class="container">
            <div class="page-header">
                <h1>企业名录</h1>
                <p>收录''' + config['desc'] + ''' ''' + str(len(enterprises)) + ''' 家知名企业</p>
            </div>

            <div class="filter-bar">
                ''' + category_filters + '''
            </div>

            <div class="enterprise-grid">
                ''' + enterprise_cards + '''
            </div>
        </div>
    </main>

    ''' + generate_footer(config) + '''

    <script>
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                const filter = this.dataset.filter;
                document.querySelectorAll('.enterprise-card').forEach(card => {
                    if (filter === 'all' || card.dataset.category === filter) {
                        card.style.display = '';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    </script>
</body>
</html>'''
    return html


def generate_enterprise_detail(site_id, config, ent, all_enterprises):
    """生成企业详情页"""
    tags_html = ''.join(['<span class="tag">' + t + '</span>' for t in ent.get('tags', [])])
    
    # 获取相关企业
    related = []
    current_cat = ent.get('category', '')
    for e in all_enterprises:
        if e['id'] != ent['id'] and e.get('category', '') == current_cat:
            related.append(e)
            if len(related) >= 4:
                break
    
    related_cards = ''
    for re in related:
        related_cards += '''
            <div class="related-enterprise-card">
                <h4><a href="/enterprises/''' + re['id'] + '''.html">''' + re['name'] + '''</a></h4>
                <p class="ent-desc">''' + (re.get('short_desc', '')[:60] if re.get('short_desc') else '') + '''...</p>
                <div class="ent-tags">
                    <span class="ent-category">''' + (re.get('category', '') or '') + '''</span>
                    <span class="ent-location">📍 ''' + (re.get('location', '') or '') + '''</span>
                </div>
            </div>'''
    
    related_section = ''
    if related_cards:
        related_section = '''
    <section class="related-enterprises">
        <div class="container">
            <h2 class="section-title">相关企业推荐</h2>
            <div class="related-enterprise-grid">
                ''' + related_cards + '''
            </div>
        </div>
    </section>'''
    
    founded_str = ', "foundingDate": "' + ent.get('founded', '') + '"' if ent.get('founded') else ''
    location_str = ', "address": {"@type": "PostalAddress", "addressLocality": "' + ent.get('location', '') + '"}' if ent.get('location') else ''
    
    org_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": ent['name'],
        "description": ent.get('short_desc', ''),
        "url": "https://" + config['domain'] + "/enterprises/" + ent['id'] + ".html" + founded_str + location_str
    }, ensure_ascii=False, indent=2)
    
    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": config['name'], "item": "https://" + config['domain']},
            {"@type": "ListItem", "position": 2, "name": "企业名录", "item": "https://" + config['domain'] + "/enterprises.html"},
            {"@type": "ListItem", "position": 3, "name": ent['name'], "item": "https://" + config['domain'] + "/enterprises/" + ent['id'] + ".html"}
        ]
    }, ensure_ascii=False, indent=2)
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>''' + ent['name'] + ''' - ''' + config['name'] + '''企业名录</title>
    <meta name="description" content="''' + (ent.get('short_desc', '') or '') + '''">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
''' + org_schema + '''
    </script>
    <script type="application/ld+json">
''' + breadcrumb_schema + '''
    </script>
    <style>
        .enterprise-detail { max-width: 800px; margin: 0 auto; padding: 40px 20px; }
        .breadcrumb { font-size: 0.85rem; color: #999; margin-bottom: 20px; }
        .breadcrumb a { color: ''' + config['color'] + '''; text-decoration: none; }
        .enterprise-header { border-bottom: 2px solid ''' + config['color'] + '''; padding-bottom: 20px; margin-bottom: 30px; }
        .enterprise-header h1 { margin: 0 0 10px; }
        .meta-row { display: flex; gap: 20px; flex-wrap: wrap; color: #666; font-size: 0.9rem; margin-bottom: 10px; }
        .tags .tag { display: inline-block; background: #f0f0f0; padding: 4px 12px; border-radius: 4px; font-size: 0.8rem; color: #666; margin-right: 6px; margin-bottom: 6px; }
        .description { line-height: 1.8; color: #444; font-size: 0.95rem; }
        .back-link { display: inline-block; margin-top: 30px; color: ''' + config['color'] + '''; text-decoration: none; }
        .main-content { min-height: 60vh; }
        .related-enterprises { background: #f8f9fa; padding: 40px 0; margin-top: 40px; }
        .related-enterprises .section-title { text-align: center; margin-bottom: 30px; color: #333; }
        .related-enterprise-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
        .related-enterprise-card { background: #fff; border: 1px solid #e8e8e8; border-radius: 8px; padding: 20px; transition: box-shadow 0.2s; }
        .related-enterprise-card:hover { box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
        .related-enterprise-card h4 { margin: 0 0 8px; font-size: 1rem; }
        .related-enterprise-card h4 a { color: #333; text-decoration: none; }
        .related-enterprise-card h4 a:hover { color: ''' + config['color'] + '''; }
        .related-enterprise-card .ent-desc { color: #666; font-size: 0.85rem; line-height: 1.5; margin-bottom: 10px; }
        .related-enterprise-card .ent-tags { display: flex; gap: 10px; font-size: 0.8rem; color: #999; }
        .related-enterprise-card .ent-category { background: #f0f0f0; padding: 2px 8px; border-radius: 4px; }
    </style>
</head>
<body>
    ''' + generate_nav(site_id, config, 'enterprises') + '''

    <main class="main-content">
        <div class="container">
            <div class="enterprise-detail">
                <div class="breadcrumb">
                    <a href="/">首页</a> &gt; <a href="/enterprises.html">企业名录</a> &gt; ''' + ent['name'] + '''
                </div>
                <div class="enterprise-header">
                    <h1>''' + ent['name'] + '''</h1>
                    <div class="meta-row">
                        <span>📂 ''' + (ent.get('category', '') or '') + '''</span>
                        ''' + ('<span>📍 ' + ent.get('location', '') + '</span>' if ent.get('location') else '') + '''
                        ''' + ('<span>📅 ' + ent.get('founded', '') + '</span>' if ent.get('founded') else '') + '''
                    </div>
                    <div class="tags">''' + tags_html + '''</div>
                </div>
                <div class="description">
                    <p>''' + (ent.get('description', ent.get('short_desc', '')) or '') + '''</p>
                </div>
                <a href="/enterprises.html" class="back-link">← 返回企业名录</a>
            </div>
        </div>
    </main>

    ''' + related_section + '''

    ''' + generate_footer(config) + '''
</body>
</html>'''
    return html


# 主流程
for site_id, config in SITES_CONFIG.items():
    ent_file = os.path.join(DATA_DIR, site_id + '-enterprises.json')
    if not os.path.exists(ent_file):
        print("⏳ " + config['name'] + ": 企业数据文件不存在，跳过")
        continue
    
    with open(ent_file, 'r', encoding='utf-8') as f:
        enterprises = json.load(f)
    
    site_dir = os.path.join(SITES_DIR, site_id)
    
    # 生成企业名录页面
    ent_page = generate_enterprises_page(site_id, config, enterprises)
    with open(os.path.join(site_dir, 'enterprises.html'), 'w', encoding='utf-8') as f:
        f.write(ent_page)
    
    # 生成企业详情页
    ent_dir = os.path.join(site_dir, 'enterprises')
    os.makedirs(ent_dir, exist_ok=True)
    for ent in enterprises:
        detail_html = generate_enterprise_detail(site_id, config, ent, enterprises)
        with open(os.path.join(ent_dir, ent['id'] + '.html'), 'w', encoding='utf-8') as f:
            f.write(detail_html)
    
    print("✅ " + config['name'] + ": 企业名录" + str(len(enterprises)) + "家页面已更新")

print("\n全部完成!")
