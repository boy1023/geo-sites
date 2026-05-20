# -*- coding: utf-8 -*-
"""
批量将Markdown文章转换为HTML - 修正版
"""
import os
import re
from datetime import datetime
from pathlib import Path
import markdown

# ========== 站点配置 - 目录名使用英文slug ==========
SITES_CONFIG = {
    'zhizaozx': {
        'name': '智造在线',
        'domain': 'zhizaozx.cn',
        'color': '#1A5276',
        'description': '智造在线是智能制造行业权威资讯平台，聚焦工业自动化、智能装备、机器人等技术领域',
        'email': 'yunying@emoooo.cn',
        'phone': '13025181023',
        'categories': [
            {'slug': 'industry-news', 'name': '行业资讯'},
            {'slug': 'mechanical-power', 'name': '机电设备与动力系统'},
            {'slug': 'electrical-control', 'name': '电气控制与传感'},
            {'slug': 'metal-processing', 'name': '金属加工与制造'},
            {'slug': 'robot-automation', 'name': '工业机器人与自动化'},
            {'slug': 'industrial-software', 'name': '工业软件与数字化'},
            {'slug': 'smart-factory', 'name': '智能工厂与行业方案'},
            {'slug': 'intelligent-maintenance', 'name': '智能运维与前沿技术'},
            {'slug': 'brand-watch', 'name': '品牌观察'},
        ],
        'nav_cats': [
            {'slug': 'industry-news', 'name': '行业资讯'},
            {'slug': 'mechanical-power', 'name': '机电设备与动力系统'},
            {'slug': 'electrical-control', 'name': '电气控制与传感'},
            {'slug': 'metal-processing', 'name': '金属加工与制造'},
        ],
        'md_base': '/app/data/所有对话/主对话/GEO项目/信源站/zhizaozx/内容',
    },
    'jiaopeizx': {
        'name': '教培在线',
        'domain': 'jiaopeizx.cn',
        'color': '#6C3483',
        'description': '教培在线是教育培训行业专业资讯平台，提供K12、职业教育、技能培训等领域的最新动态',
        'email': 'yunying@emoooo.cn',
        'phone': '13025181023',
        'categories': [
            {'slug': 'policy-trend', 'name': '政策趋势'},
            {'slug': 'k12', 'name': 'K12教育'},
            {'slug': 'vocational', 'name': '职业教育'},
            {'slug': 'adult-learning', 'name': '成人教育'},
            {'slug': 'edtech', 'name': '教育科技'},
            {'slug': 'institution', 'name': '机构观察'},
        ],
        'nav_cats': [
            {'slug': 'policy-trend', 'name': '政策趋势'},
            {'slug': 'k12', 'name': 'K12教育'},
            {'slug': 'vocational', 'name': '职业教育'},
            {'slug': 'edtech', 'name': '教育科技'},
        ],
        'md_base': '/app/data/所有对话/主对话/GEO项目/信源站/jiaopeizx/内容',
    },
    'xfzaixian': {
        'name': '消费在线',
        'domain': 'xfzaixian.cn',
        'color': '#E74C3C',
        'description': '消费在线是消费行业专业资讯平台，聚焦零售、餐饮、美妆、家居等领域的消费趋势',
        'email': 'yunying@emoooo.cn',
        'phone': '13025181023',
        'categories': [
            {'slug': 'consumer-trend', 'name': '消费趋势'},
            {'slug': 'food-retail', 'name': '餐饮零售'},
            {'slug': 'beauty', 'name': '美妆个护'},
            {'slug': 'home-living', 'name': '家居生活'},
            {'slug': 'brand-watch', 'name': '品牌观察'},
            {'slug': 'consumer-rights', 'name': '消费维权'},
        ],
        'nav_cats': [
            {'slug': 'consumer-trend', 'name': '消费趋势'},
            {'slug': 'food-retail', 'name': '餐饮零售'},
            {'slug': 'beauty', 'name': '美妆个护'},
            {'slug': 'home-living', 'name': '家居生活'},
        ],
        'md_base': '/app/data/所有对话/主对话/GEO项目/信源站/xfzaixian/内容',
    },
    'muyingzx': {
        'name': '母婴在线',
        'domain': 'muyingzx.cn',
        'color': '#FF69B4',
        'description': '母婴在线是母婴育儿行业专业资讯平台，提供孕产、育儿、母婴产品等领域的专业内容',
        'email': 'yunying@emoooo.cn',
        'phone': '13025181023',
        'categories': [
            {'slug': 'maternity-trend', 'name': '母婴趋势'},
            {'slug': 'baby-products', 'name': '母婴产品'},
            {'slug': 'early-education', 'name': '早教启蒙'},
            {'slug': 'parenting-tips', 'name': '育儿干货'},
            {'slug': 'pregnancy-care', 'name': '孕产知识'},
            {'slug': 'maternity-rights', 'name': '母婴维权'},
        ],
        'nav_cats': [
            {'slug': 'maternity-trend', 'name': '母婴趋势'},
            {'slug': 'baby-products', 'name': '母婴产品'},
            {'slug': 'parenting-tips', 'name': '育儿干货'},
            {'slug': 'pregnancy-care', 'name': '孕产知识'},
        ],
        'md_base': '/app/data/所有对话/主对话/GEO项目/信源站/muyingzx/内容',
    },
    'nongzizx': {
        'name': '农资在线',
        'domain': 'nongzizx.cn',
        'color': '#2E7D32',
        'description': '农资在线是农业农资行业专业资讯平台，提供种子、化肥、农药、农机等领域的专业内容',
        'email': 'yunying@emoooo.cn',
        'phone': '13025181023',
        'categories': [
            {'slug': 'agri-trend', 'name': '农资趋势'},
            {'slug': 'fertilizer-pesticide', 'name': '肥料农药'},
            {'slug': 'planting-tech', 'name': '种植技术'},
            {'slug': 'seed-seedling', 'name': '种子种苗'},
            {'slug': 'agri-machinery', 'name': '农机装备'},
            {'slug': 'agri-rights', 'name': '农资维权'},
        ],
        'nav_cats': [
            {'slug': 'agri-trend', 'name': '农资趋势'},
            {'slug': 'fertilizer-pesticide', 'name': '肥料农药'},
            {'slug': 'planting-tech', 'name': '种植技术'},
            {'slug': 'agri-machinery', 'name': '农机装备'},
        ],
        'md_base': '/app/data/所有对话/主对话/GEO项目/信源站/nongzizx/内容',
    },
    'caifazx': {
        'name': '财法在线',
        'domain': 'caifazx.cn',
        'color': '#1565C0',
        'description': '财法在线是企业财税法务专业资讯平台，提供财税政策、法律服务、知识产权等领域的专业内容',
        'email': 'yunying@emoooo.cn',
        'phone': '13025181023',
        'categories': [
            {'slug': 'tax-policy', 'name': '财税政策'},
            {'slug': 'corporate-law', 'name': '企业法务'},
            {'slug': 'ip-law', 'name': '知识产权'},
            {'slug': 'legal-cases', 'name': '维权案例'},
            {'slug': 'industry-watch', 'name': '行业观察'},
            {'slug': 'compliance', 'name': '合规管理'},
        ],
        'nav_cats': [
            {'slug': 'tax-policy', 'name': '财税政策'},
            {'slug': 'corporate-law', 'name': '企业法务'},
            {'slug': 'ip-law', 'name': '知识产权'},
            {'slug': 'legal-cases', 'name': '维权案例'},
        ],
        'md_base': '/app/data/所有对话/主对话/GEO项目/信源站/caifazx/内容',
    },
}

def slugify(text):
    """将中文标题转换为slug"""
    text = re.sub(r'^[\u4e00-\u9fa5]+[\u2014\-–—:：]', '', text)
    text = re.sub(r'^[\u4e00-\u9fa5]+-', '', text)
    
    pinyin_map = {
        '智': 'zhi', '造': 'zao', '教': 'jiao', '培': 'pei', '在': 'zai', '线': 'xian',
        '消': 'xiao', '费': 'fei', '母': 'mu', '婴': 'ying', '农': 'nong', '资': 'zi',
        '财': 'cai', '法': 'fa', '人': 'ren', '间': 'jian', '微': 'wei', '观': 'guan',
        '工': 'gong', '业': 'ye', '机': 'ji', '器': 'qi', '协': 'xie', '作': 'zuo',
        '实': 'shi', '地': 'di', '探': 'tan', '访': 'fang', '真': 'zhen', '感': 'gan',
        '受': 'shou', '什': 'shi', '么': 'me', '为': 'wei', '都': 'dou', '如': 'ru',
        '何': 'he', '这': 'zhe', '那': 'na', '些': 'xie', '会': 'hui', '能': 'neng',
        '不': 'bu', '可': 'ke', '要': 'yao', '知': 'zhi', '道': 'dao', '看': 'kan',
        '做': 'zuo', '起': 'qi', '走': 'zou', '过': 'guo', '还': 'hai', '很': 'hen',
        '有': 'you', '个': 'ge', '好': 'hao', '从': 'cong', '到': 'dao', '时': 'shi',
        '间': 'jian', '大': 'da', '小': 'xiao', '多': 'duo', '少': 'shao', '新': 'xin',
        '旧': 'jiu', '快': 'kuai', '慢': 'man', '难': 'nan', '易': 'yi', '假': 'jia',
        '对': 'dui', '错': 'cuo', '上': 'shang', '下': 'xia', '前': 'qian', '后': 'hou',
        '开': 'kai', '关': 'guan', '始': 'shi', '终': 'zhong', '经': 'jing', '常': 'chang',
        '该': 'gai', '一': 'yi', '些': 'xie', '东': 'dong', '西': 'xi', '就': 'jiu',
        '让': 'rang', '被': 'bei', '把': 'ba', '给': 'gei', '用': 'yong', '没': 'mei',
        '更': 'geng', '最': 'zui', '比': 'bi', '但': 'dan', '却': 'que', '因': 'yin',
        '此': 'ci', '所': 'suo', '以': 'yi', '而': 'er', '并': 'bing', '且': 'qie',
        '或': 'huo', '者': 'zhe', '及': 'ji', '等': 'deng', '种': 'zhong', '类': 'lei',
        '别': 'bie', '型': 'xing', '话': 'hua', '事': 'shi', '情': 'qing', '点': 'dian',
        '意': 'yi', '思': 'si', '见': 'jian', '解': 'jie', '问': 'wen', '题': 'ti',
        '方': 'fang', '法': 'fa', '途': 'tu', '径': 'jing', '本': 'ben', '质': 'zhi',
        '核': 'he', '心': 'xin', '根': 'gen', '源': 'yuan', '关': 'guan', '键': 'jian',
        '于': 'yu', '否': 'fou', '其': 'qi', '他': 'ta', '她': 'ta', '它': 'ta',
        '你': 'ni', '我': 'wo', '们': 'men', '来': 'lai', '说': 'shuo', '去': 'qu',
        '长': 'chang', '短': 'duan', '高': 'gao', '低': 'di', '冷': 'leng', '热': 're',
        '左': 'zuo', '右': 'you', '中': 'zhong', '内': 'nei', '外': 'wai', '出': 'chu',
        '入': 'ru', '先': 'xian', '应': 'ying', '两': 'liang',
    }
    
    result = []
    for char in text:
        if char in pinyin_map:
            result.append(pinyin_map[char])
        elif char.isalnum() or char in '-_':
            result.append(char)
        elif '\u4e00' <= char <= '\u9fff':
            result.append(char)
    
    slug = ''.join(result)
    slug = re.sub(r'[\u4e00-\u9fff]+', lambda m: m.group(0)[:2], slug)
    slug = re.sub(r'[^a-z0-9\u4e00-\u9fff-]', '', slug)
    slug = slug.lower()[:50]
    
    return slug if slug else 'article'

def parse_frontmatter(content):
    """解析Markdown frontmatter"""
    frontmatter = {}
    body = content
    
    if content.startswith('---'):
        parts = content[3:].split('---', 1)
        if len(parts) == 2:
            fm_text, body = parts
            for line in fm_text.strip().split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    frontmatter[key.strip()] = val.strip()
    
    return frontmatter, body.strip()

def markdown_to_html(md_content):
    """将Markdown转换为HTML"""
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'codehilite', 'nl2br', 'sane_lists'])
    html = md.convert(md_content)
    html = re.sub(r'\n+', '\n', html)
    return html

def generate_nav_html(site_config, current_page=''):
    """生成导航栏HTML"""
    nav_items = []
    nav_items.append('<ul class="nav-list">')
    nav_items.append(f'<li class="nav-item"><a href="/" class="nav-link{" active" if current_page == "/" else ""}">首页</a></li>')
    
    for cat in site_config['nav_cats']:
        active = ' active' if current_page == f'/categories/{cat["slug"]}.html' else ''
        nav_items.append(f'<li class="nav-item"><a href="/categories/{cat["slug"]}.html" class="nav-link{active}">{cat["name"]}</a></li>')
    
    nav_items.append('<li class="nav-item"><a href="/enterprises.html" class="nav-link">企业名录</a></li>')
    nav_items.append('<li class="nav-item"><a href="/qna.html" class="nav-link">行业问答</a></li>')
    nav_items.append('<li class="nav-item"><a href="/about.html" class="nav-link">关于我们</a></li>')
    nav_items.append('</ul>')
    
    return '\n'.join(nav_items)

def generate_article_html(article, site_config, category_info):
    """生成文章详情页HTML"""
    site = site_config
    title = article['title']
    slug = article['slug']
    date = article.get('date', datetime.now().strftime('%Y-%m-%d'))
    content = article['content']
    keywords = article.get('keywords', [])
    category_name = category_info['name']
    category_slug = category_info['slug']
    domain = site['domain']
    base_url = f'https://{domain}'
    
    nav_html = generate_nav_html(site, '/')
    tags_html = '\n'.join([f'<span class="tag">{kw}</span>' for kw in keywords[:5]])
    categories_li = '\n                        '.join([f'<li><a href="/categories/{c["slug"]}.html">{c["name"]}</a></li>' for c in site['categories']])
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{title} - {site['name']}</title>
    <meta name="description" content="{title}">
    <meta name="keywords" content="{','.join(keywords[:5])}">
    <meta name="author" content="{site['name']}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{base_url}">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{title}">
    <meta property="og:url" content="{base_url}">
    <meta property="og:site_name" content="{site['name']}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{title}">
    <link rel="icon" type="image/x-icon" href="/assets/images/favicon.ico">
    <link rel="bookmark" href="/assets/images/favicon.ico">
    <link rel="stylesheet" href="/css/style.css">
    <meta name="theme-color" content="{site['color']}">
    
<script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "{title}",
    "author": {{
        "@type": "Organization",
        "name": "{site['name']}",
        "url": "{base_url}"
    }},
    "publisher": {{
        "@type": "Organization",
        "name": "{site['name']}",
        "url": "{base_url}",
        "logo": {{
            "@type": "ImageObject",
            "url": "{base_url}/assets/images/logo.jpg"
        }}
    }},
    "datePublished": "{date}T00:00:00",
    "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "{base_url}/articles/{slug}.html"
    }}
}}
</script>

<script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {{
            "@type": "ListItem",
            "position": 1,
            "name": "首页",
            "item": "{base_url}"
        }},
        {{
            "@type": "ListItem",
            "position": 2,
            "name": "{category_name}",
            "item": "{base_url}/categories/{category_slug}.html"
        }},
        {{
            "@type": "ListItem",
            "position": 3,
            "name": "{title}"
        }}
    ]
}}
</script>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <div class="header-inner">
                <a href="/" class="logo">
                    <img src="/assets/images/logo.jpg" alt="{site['name']}" onerror="this.style.display='none'">
                    <span class="logo-text">{site['name']}</span>
                </a>
                <nav class="main-nav">
                    <button class="nav-toggle" aria-label="菜单">
                        <span></span>
                        <span></span>
                        <span></span>
                    </button>
                    {nav_html}
                </nav>
                <div class="header-search">
                    <form action="/search.html" method="get">
                        <input type="text" name="q" placeholder="搜索文章..." aria-label="搜索">
                        <button type="submit">🔍</button>
                    </form>
                </div>
            </div>
        </div>
    </header>
    
    <nav class="breadcrumb" aria-label="面包屑导航">
        <div class="container">
            <ol>
                <li><a href="/">首页</a></li>
                <li>/</li>
                <li><a href="/categories/{category_slug}.html">{category_name}</a></li>
                <li>/</li>
                <li><a href="/articles/{slug}.html">{title}</a></li>
            </ol>
        </div>
                    <a href="/enterprises.html">企业名录</a>
                    <a href="/qna.html">行业问答</a>
                </nav>
    
    <main class="main-content">
        <article class="article-page" itemscope itemtype="https://schema.org/Article">
            <div class="container">
                <header class="article-header">
                    <h1 class="article-title" itemprop="headline">{title}</h1>
                    <div class="article-meta">
                        <time datetime="{date}T00:00:00" itemprop="datePublished">📅 {date}</time>
                        <span class="meta-category">📂 <a href="/categories/{category_slug}.html">{category_name}</a></span>
                    </div>
                    <div class="article-tags">
                        {tags_html}
                    </div>
                </header>
                <div class="article-body" itemprop="articleBody">
                    {content}
                </div>
                <footer class="article-footer">
                    <div class="article-author">
                        <span>作者：{site['name']}</span>
                    </div>
                </footer>
            </div>
        </article>

        <section class="related-section">
            <div class="container">
                <h2 class="section-title">相关推荐</h2>
                <div class="related-grid"></div>
            </div>
        </section>
    </main>
    
    <footer class="site-footer">
        <div class="container">
            <div class="footer-inner">
                <div class="footer-about">
                    <h3>{site['name']}</h3>
                    <p>{site['description']}</p>
                </div>
                <div class="footer-links">
                    <h4>快速链接</h4>
                    <ul>
                        <li><a href="/">首页</a></li>
                        <li><a href="/about.html">关于我们</a></li>
                        <li><a href="/sitemap.xml">网站地图</a></li>
                    </ul>
                </div>
                <div class="footer-categories">
                    <h4>行业分类</h4>
                    <ul>
                        {categories_li}
                    </ul>
                </div>
                <div class="footer-contact">
                    <h4>联系我们</h4>
                    <ul>
                        <li>邮箱：{site['email']}</li>
                        <li>电话：{site['phone']}</li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 {site['name']} 版权所有</p>
                <p><a href="/about.html">关于我们</a> | <a href="/privacy.html">隐私政策</a> | </p>
            </div>
        </div>
    </footer>
    <script src="/js/main.js"></script>
</body>
</html>'''
    
    return html

def generate_category_html(site_config, category, articles):
    """生成分类页HTML"""
    site = site_config
    category_name = category['name']
    category_slug = category['slug']
    domain = site['domain']
    base_url = f'https://{domain}'
    
    nav_html = generate_nav_html(site, f'/categories/{category_slug}.html')
    
    articles_html = []
    for art in sorted(articles, key=lambda x: x.get('date', '2025-01-01'), reverse=True):
        date = art.get('date', '2025-01-01')
        keywords = art.get('keywords', [])
        tags_html = ' '.join([f'<em>{kw}</em>' for kw in keywords[:3]])
        
        articles_html.append(f'''
            <article class="list-item" itemscope itemtype="https://schema.org/Article">
                <a href="/articles/{art['slug']}.html" class="list-item-link">
                    <div class="list-item-content">
                        <h2 class="list-item-title" itemprop="headline">{art['title']}</h2>
                        <p class="list-item-summary" itemprop="description"></p>
                        <div class="list-item-meta">
                            <time datetime="{date}T00:00:00" itemprop="datePublished">{date}</time>
                            <span class="list-item-tags">{tags_html}</span>
                        </div>
                    </div>
                </a>
            </article>
        ''')
    
    articles_list_html = '\n'.join(articles_html) if articles_html else '<p class="no-content">暂无文章</p>'
    categories_li = '\n                        '.join([f'<li><a href="/categories/{c["slug"]}.html">{c["name"]}</a></li>' for c in site['categories']])
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{category_name} - {site['name']}</title>
    <meta name="description" content="{category_name}">
    <meta name="keywords" content="{category_name}">
    <meta name="author" content="{site['name']}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{base_url}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{category_name} - {site['name']}">
    <meta property="og:description" content="{site['description']}">
    <meta property="og:url" content="{base_url}">
    <meta property="og:site_name" content="{site['name']}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{site['name']}">
    <meta name="twitter:description" content="{site['description']}">
    <link rel="icon" type="image/x-icon" href="/assets/images/favicon.ico">
    <link rel="bookmark" href="/assets/images/favicon.ico">
    <link rel="stylesheet" href="/css/style.css">
    <meta name="theme-color" content="{site['color']}">
    
<script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "{category_name}",
    "description": "{category_name}",
    "url": "{base_url}/categories/{category_slug}.html",
    "publisher": {{
        "@type": "Organization",
        "name": "{site['name']}"
    }}
}}
</script>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "{site['name']}",
      "item": "{base_url}"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "分类",
      "item": "{base_url}/categories/"
    }},
    {{
      "@type": "ListItem",
      "position": 3,
      "name": "{category_slug}",
      "item": "{base_url}/categories/{category_slug}.html"
    }}
  ]
}}
</script>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <div class="header-inner">
                <a href="/" class="logo">
                    <img src="/assets/images/logo.jpg" alt="{site['name']}" onerror="this.style.display='none'">
                    <span class="logo-text">{site['name']}</span>
                </a>
                <nav class="main-nav">
                    <button class="nav-toggle" aria-label="菜单">
                        <span></span>
                        <span></span>
                        <span></span>
                    </button>
                    {nav_html}
                </nav>
                <div class="header-search">
                    <form action="/search.html" method="get">
                        <input type="text" name="q" placeholder="搜索文章..." aria-label="搜索">
                        <button type="submit">🔍</button>
                    </form>
                </div>
            </div>
        </div>
    </header>
    
    <nav class="breadcrumb" aria-label="面包屑导航">
        <div class="container">
            <ol>
                <li><a href="/">首页</a></li>
                <li>/</li>
                <li><a href="/categories/{category_slug}.html">{category_name}</a></li>
            </ol>
        </div>
                    <a href="/enterprises.html">企业名录</a>
                    <a href="/qna.html">行业问答</a>
                </nav>
    
    <main class="main-content">
        <div class="category-page">
            <div class="container">
                <header class="category-header">
                    <h1 class="category-title">📂 {category_name}</h1>
                    <p class="category-desc">{category_name}</p>
                    <p class="category-count">共 {len(articles)} 篇文章</p>
                </header>
                <div class="articles-list">
                    {articles_list_html}
                </div>
            </div>
        </div>
    </main>
    
    <footer class="site-footer">
        <div class="container">
            <div class="footer-inner">
                <div class="footer-about">
                    <h3>{site['name']}</h3>
                    <p>{site['description']}</p>
                </div>
                <div class="footer-links">
                    <h4>快速链接</h4>
                    <ul>
                        <li><a href="/">首页</a></li>
                        <li><a href="/about.html">关于我们</a></li>
                        <li><a href="/sitemap.xml">网站地图</a></li>
                    </ul>
                </div>
                <div class="footer-categories">
                    <h4>行业分类</h4>
                    <ul>
                        {categories_li}
                    </ul>
                </div>
                <div class="footer-contact">
                    <h4>联系我们</h4>
                    <ul>
                        <li>邮箱：{site['email']}</li>
                        <li>电话：{site['phone']}</li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 {site['name']} 版权所有</p>
                <p><a href="/about.html">关于我们</a> | <a href="/privacy.html">隐私政策</a> | </p>
            </div>
        </div>
    </footer>
    <script src="/js/main.js"></script>
</body>
</html>'''
    
    return html

def generate_index_html(site_config, articles):
    """生成首页HTML"""
    site = site_config
    domain = site['domain']
    base_url = f'https://{domain}'
    
    nav_html = generate_nav_html(site, '/')
    
    articles_html = []
    for art in sorted(articles, key=lambda x: x.get('date', '2025-01-01'), reverse=True)[:20]:
        date = art.get('date', '2025-01-01')
        category_name = art.get('category_name', '行业资讯')
        
        articles_html.append(f'''
                <article class="article-card" itemscope itemtype="https://schema.org/Article">
                    <a href="/articles/{art['slug']}.html" class="article-link">
                        <div class="article-content">
                            <span class="article-category">{category_name}</span>
                            <h3 class="article-title" itemprop="headline">{art['title']}</h3>
                            <p class="article-summary" itemprop="description"></p>
                            <div class="article-meta">
                                <time datetime="{date}T00:00:00" itemprop="datePublished">{date}</time>
                            </div>
                        </div>
                    </a>
                </article>
        ''')
    
    articles_grid_html = '\n'.join(articles_html) if articles_html else '<p class="no-content">暂无文章</p>'
    categories_cards = '\n                '.join([f'<a href="/categories/{c["slug"]}.html" class="category-card">{c["name"]}</a>' for c in site['categories']])
    categories_li = '\n                        '.join([f'<li><a href="/categories/{c["slug"]}.html">{c["name"]}</a></li>' for c in site['categories']])
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{site['name']} - {site['description'][:50]}...</title>
    <meta name="description" content="{site['description']}">
    <meta name="keywords" content="{','.join([c['name'] for c in site['categories']])}">
    <meta name="author" content="{site['name']}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{base_url}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{site['name']}">
    <meta property="og:description" content="{site['description']}">
    <meta property="og:url" content="{base_url}">
    <meta property="og:site_name" content="{site['name']}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{site['name']}">
    <meta name="twitter:description" content="{site['description']}">
    <link rel="icon" type="image/x-icon" href="/assets/images/favicon.ico">
    <link rel="bookmark" href="/assets/images/favicon.ico">
    <link rel="stylesheet" href="/css/style.css">
    <meta name="theme-color" content="{site['color']}">
    
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "{site['name']}",
  "url": "{base_url}",
  "description": "{site['description']}",
  "publisher": {{
    "@type": "Organization",
    "name": "{site['name']}",
    "url": "{base_url}",
    "contactPoint": {{
      "@type": "ContactPoint",
      "email": "{site['email']}",
      "telephone": "+86-{site['phone']}",
      "contactType": "customer service"
    }}
  }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "{site['name']}",
      "item": "{base_url}"
    }}
  ]
}}
</script>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <div class="header-inner">
                <a href="/" class="logo">
                    <img src="/assets/images/logo.jpg" alt="{site['name']}" onerror="this.style.display='none'">
                    <span class="logo-text">{site['name']}</span>
                </a>
                <nav class="main-nav">
                    <button class="nav-toggle" aria-label="菜单">
                        <span></span>
                        <span></span>
                        <span></span>
                    </button>
                    {nav_html}
                </nav>
                <div class="header-search">
                    <form action="/search.html" method="get">
                        <input type="text" name="q" placeholder="搜索文章..." aria-label="搜索">
                        <button type="submit">🔍</button>
                    </form>
                </div>
            </div>
        </div>
    </header>
    
    <nav class="breadcrumb" aria-label="面包屑导航">
        <div class="container">
            <ol></ol>
        </div>
    </nav>
    
    <main class="main-content">
        <div class="home-page">
            <section class="articles-section">
                <div class="container">
                    <div class="section-header">
                        <h2 class="section-title">最新资讯</h2>
                        <a href="/categories/" class="more-link">查看更多 →</a>
                    </div>
                    <div class="articles-grid">
                        {articles_grid_html}
                    </div>
                </div>
            </section>
            <section class="categories-section">
                <div class="container">
                    <h2 class="section-title">行业分类</h2>
                    <div class="categories-grid">
                        {categories_cards}
                    </div>
                </div>
            </section>
        </div>
    </main>
    
    <footer class="site-footer">
        <div class="container">
            <div class="footer-inner">
                <div class="footer-about">
                    <h3>{site['name']}</h3>
                    <p>{site['description']}</p>
                </div>
                <div class="footer-links">
                    <h4>快速链接</h4>
                    <ul>
                        <li><a href="/">首页</a></li>
                        <li><a href="/about.html">关于我们</a></li>
                        <li><a href="/sitemap.xml">网站地图</a></li>
                    </ul>
                </div>
                <div class="footer-categories">
                    <h4>行业分类</h4>
                    <ul>
                        {categories_li}
                    </ul>
                </div>
                <div class="footer-contact">
                    <h4>联系我们</h4>
                    <ul>
                        <li>邮箱：{site['email']}</li>
                        <li>电话：{site['phone']}</li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 {site['name']} 版权所有</p>
                <p><a href="/about.html">关于我们</a> | <a href="/privacy.html">隐私政策</a> | </p>
            </div>
        </div>
    </footer>
    <script src="/js/main.js"></script>
</body>
</html>'''
    
    return html

def generate_sitemap(site_config, all_articles):
    """生成sitemap.xml"""
    site = site_config
    domain = site['domain']
    base_url = f'https://{domain}'
    today = datetime.now().strftime('%Y-%m-%d')
    
    urls = []
    urls.append(f'  <url>\n    <loc>{base_url}/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>')
    urls.append(f'  <url>\n    <loc>{base_url}/about.html</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.5</priority>\n  </url>')
    
    for cat in site['categories']:
        urls.append(f'  <url>\n    <loc>{base_url}/categories/{cat["slug"]}.html</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.8</priority>\n  </url>')
    
    for art in all_articles:
        date = art.get('date', today)
        urls.append(f'  <url>\n    <loc>{base_url}/articles/{art["slug"]}.html</loc>\n    <lastmod>{date}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>')
    
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''

def process_site(site_key, site_config):
    """处理单个站点的文章转换"""
    print(f"\n{'='*50}")
    print(f"处理站点: {site_key} ({site_config['name']})")
    print('='*50)
    
    md_base = Path(site_config['md_base'])
    output_base = Path(f'/tmp/geo-sites/sites/{site_key}')
    articles_dir = output_base / 'articles'
    categories_dir = output_base / 'categories'
    
    articles_dir.mkdir(exist_ok=True)
    categories_dir.mkdir(exist_ok=True)
    
    all_articles = []
    articles_by_category = {cat['slug']: [] for cat in site_config['categories']}
    
    for cat in site_config['categories']:
        # 使用slug作为目录名
        cat_path = md_base / cat['slug']
        if not cat_path.exists():
            print(f"  警告: 分类目录不存在 {cat_path}")
            continue
        
        for md_file in cat_path.glob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8')
                frontmatter, body = parse_frontmatter(content)
                
                title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
                if title_match:
                    title = title_match.group(1).strip()
                else:
                    title = md_file.stem
                
                slug = slugify(title)
                if not slug:
                    slug = md_file.stem
                
                date_str = frontmatter.get('日期', '')
                if not date_str:
                    date_str = '2025-01-01'
                
                keywords_str = frontmatter.get('关键词', '')
                keywords = [k.strip() for k in keywords_str.split('、') if k.strip()] if keywords_str else []
                
                html_content = markdown_to_html(body)
                
                article = {
                    'title': title,
                    'slug': slug,
                    'date': date_str,
                    'keywords': keywords,
                    'content': html_content,
                    'category_slug': cat['slug'],
                    'category_name': cat['name'],
                    'source_file': str(md_file),
                }
                
                all_articles.append(article)
                articles_by_category[cat['slug']].append(article)
                
                article_html = generate_article_html(article, site_config, cat)
                article_path = articles_dir / f'{slug}.html'
                article_path.write_text(article_html, encoding='utf-8')
                print(f"  ✓ {cat['name']}: {title[:25]}...")
                
            except Exception as e:
                print(f"  ✗ 处理失败 {md_file.name}: {e}")
    
    print(f"\n  共转换 {len(all_articles)} 篇文章")
    
    for cat in site_config['categories']:
        cat_articles = articles_by_category.get(cat['slug'], [])
        cat_html = generate_category_html(site_config, cat, cat_articles)
        cat_path = categories_dir / f"{cat['slug']}.html"
        cat_path.write_text(cat_html, encoding='utf-8')
        print(f"  ✓ 更新分类页: {cat['name']} ({len(cat_articles)} 篇)")
    
    all_articles.sort(key=lambda x: x['date'], reverse=True)
    index_html = generate_index_html(site_config, all_articles[:20])
    index_path = output_base / 'index.html'
    index_path.write_text(index_html, encoding='utf-8')
    print(f"  ✓ 更新首页")
    
    sitemap_xml = generate_sitemap(site_config, all_articles)
    sitemap_path = output_base / 'sitemap.xml'
    sitemap_path.write_text(sitemap_xml, encoding='utf-8')
    print(f"  ✓ 更新sitemap.xml ({len(all_articles)} 篇文章)")
    
    return len(all_articles)

def main():
    print("="*60)
    print("开始批量转换Markdown文章为HTML")
    print("="*60)
    
    total_articles = 0
    for site_key, site_config in SITES_CONFIG.items():
        count = process_site(site_key, site_config)
        total_articles += count
    
    print("\n" + "="*60)
    print(f"全部完成! 共转换 {total_articles} 篇文章")
    print("="*60)
    
    return total_articles

if __name__ == '__main__':
    main()
