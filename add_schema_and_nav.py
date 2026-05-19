#!/usr/bin/env python3
"""给所有站点的HTML添加Schema标签和导航更新"""
import os
import re
import json

SITES_DIR = '/tmp/geo-sites/sites'

SITES_CONFIG = {
    'zhizaozx': {'name': '智造在线', 'domain': 'zhizaozx.cn', 'desc': '智造在线是智能制造行业权威资讯平台，聚焦工业自动化、智能装备、机器人等技术领域'},
    'jiaopeizx': {'name': '教培在线', 'domain': 'jiaopeizx.cn', 'desc': '教培在线是教育培训行业专业媒体平台，聚焦K12教育、职业教育、教育科技等领域'},
    'xfzaixian': {'name': '消费在线', 'domain': 'xfzaixian.cn', 'desc': '消费在线是大消费行业专业媒体平台，聚焦新消费、餐饮零售、美妆个护等领域'},
    'muyingzx': {'name': '母婴在线', 'domain': 'muyingzx.cn', 'desc': '母婴在线是母婴行业专业媒体平台，专注母婴产品、育儿知识、消费指南'},
    'nongzizx': {'name': '农资在线', 'domain': 'nongzizx.cn', 'desc': '农资在线是农资行业专业媒体平台，聚焦化肥农药、种子种苗、农机装备等领域'},
    'caifazx': {'name': '财法在线', 'domain': 'caifazx.cn', 'desc': '财法在线是财税法务行业专业媒体平台，聚焦金税四期、企业合规、知识产权保护等'},
}

def add_website_schema(html, site_id, config):
    """添加WebSite Schema到首页"""
    schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": config['name'],
        "url": f"https://{config['domain']}",
        "description": config['desc'],
        "publisher": {
            "@type": "Organization",
            "name": config['name'],
            "url": f"https://{config['domain']}",
            "contactPoint": {
                "@type": "ContactPoint",
                "email": "yunying@emoooo.cn",
                "telephone": "+86-13025181023",
                "contactType": "customer service"
            }
        }
    }
    schema_json = json.dumps(schema, ensure_ascii=False, indent=2)
    schema_tag = f'<script type="application/ld+json">\n{schema_json}\n</script>'
    
    if 'schema.org/WebSite' not in html:
        html = html.replace('</head>', f'{schema_tag}\n</head>')
    return html

def add_article_schema(html, title, description, date, site_id, config):
    """添加Article Schema到文章页"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "datePublished": date,
        "author": {
            "@type": "Organization",
            "name": config['name']
        },
        "publisher": {
            "@type": "Organization",
            "name": config['name'],
            "url": f"https://{config['domain']}"
        }
    }
    schema_json = json.dumps(schema, ensure_ascii=False, indent=2)
    schema_tag = f'<script type="application/ld+json">\n{schema_json}\n</script>'
    
    if 'schema.org/Article' not in html:
        html = html.replace('</head>', f'{schema_tag}\n</head>')
    return html

def add_breadcrumb_schema(html, items):
    """添加BreadcrumbList Schema"""
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": []
    }
    for i, (name, url) in enumerate(items, 1):
        schema["itemListElement"].append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": url
        })
    schema_json = json.dumps(schema, ensure_ascii=False, indent=2)
    schema_tag = f'<script type="application/ld+json">\n{schema_json}\n</script>'
    
    if 'schema.org/BreadcrumbList' not in html:
        html = html.replace('</head>', f'{schema_tag}\n</head>')
    return html

def update_navigation(html, site_id):
    """更新导航栏，加入企业名录和行业问答链接"""
    # 在导航栏的最后一个分类链接后面加上两个新链接
    # 找到</nav>或导航结束位置前插入
    nav_additions = f'''
                    <a href="/enterprises.html">企业名录</a>
                    <a href="/qna.html">行业问答</a>'''
    
    # 在</nav>之前插入
    if '/enterprises.html' not in html:
        html = html.replace('</nav>', f'{nav_additions}\n                </nav>')
    return html

def process_site(site_id, config):
    """处理一个站点的所有HTML"""
    site_dir = os.path.join(SITES_DIR, site_id)
    
    for root, dirs, files in os.walk(site_dir):
        for fname in files:
            if not fname.endswith('.html'):
                continue
            
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            modified = False
            
            # 1. 添加导航
            if '/enterprises.html' not in html:
                html = update_navigation(html, site_id)
                modified = True
            
            # 2. 根据页面类型添加Schema
            if fname == 'index.html':
                if 'schema.org/WebSite' not in html:
                    html = add_website_schema(html, site_id, config)
                    modified = True
                # 首页面包屑
                if 'schema.org/BreadcrumbList' not in html:
                    html = add_breadcrumb_schema(html, [
                        (config['name'], f"https://{config['domain']}")
                    ])
                    modified = True
            
            elif fname == 'about.html':
                if 'schema.org/BreadcrumbList' not in html:
                    html = add_breadcrumb_schema(html, [
                        (config['name'], f"https://{config['domain']}"),
                        ('关于我们', f"https://{config['domain']}/about.html")
                    ])
                    modified = True
            
            elif 'articles' in root:
                # 文章页
                title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html)
                desc_match = re.search(r'<meta name="description" content="([^"]*)"', html)
                date_match = re.search(r'datePublished.*?content="([^"]*)"', html) or re.search(r'(\d{4}-\d{2}-\d{2})', html)
                
                title = title_match.group(1) if title_match else config['name']
                description = desc_match.group(1) if desc_match else ''
                date = date_match.group(1) if date_match else '2024-01-01'
                
                if 'schema.org/Article' not in html:
                    html = add_article_schema(html, title, description, date, site_id, config)
                    modified = True
                if 'schema.org/BreadcrumbList' not in html:
                    html = add_breadcrumb_schema(html, [
                        (config['name'], f"https://{config['domain']}"),
                        ('文章', f"https://{config['domain']}/articles/"),
                        (title[:20], f"https://{config['domain']}/articles/{fname}")
                    ])
                    modified = True
            
            elif 'categories' in root:
                if 'schema.org/BreadcrumbList' not in html:
                    cat_name = fname.replace('.html', '')
                    html = add_breadcrumb_schema(html, [
                        (config['name'], f"https://{config['domain']}"),
                        ('分类', f"https://{config['domain']}/categories/"),
                        (cat_name, f"https://{config['domain']}/categories/{fname}")
                    ])
                    modified = True
            
            if modified:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(html)
    
    print(f"✅ {config['name']} - Schema和导航已更新")

# 处理所有站点
for site_id, config in SITES_CONFIG.items():
    process_site(site_id, config)

print("\n全部完成!")
