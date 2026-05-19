# -*- coding: utf-8 -*-
"""
静态网站构建脚本
读取Markdown文章，生成静态HTML页面
"""

import os
import re
import json
import markdown
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown.extensions import fenced_code, codehilite, tables, toc

import config


class Article:
    """文章对象"""
    def __init__(self, slug, title, category, tags, summary, author, source, date, cover, content, top=False):
        self.slug = slug
        self.title = title
        self.category = category
        self.tags = tags
        self.summary = summary
        self.author = author
        self.source = source
        self.date = date
        self.cover = cover
        self.content = content
        self.top = top
        self.url = f"/articles/{slug}.html"
    
    @property
    def formatted_date(self):
        """格式化日期"""
        return self.date.strftime("%Y-%m-%d") if self.date else ""
    
    @property
    def iso_date(self):
        """ISO格式日期"""
        return self.date.isoformat() if self.date else ""


def parse_frontmatter(content):
    """解析Markdown前置参数"""
    frontmatter = {}
    body = content
    
    # 匹配 --- --- 之间的内容
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        body = match.group(2)
        
        # 解析键值对
        for line in fm_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().strip('"').strip("'")
                value = value.strip().strip('"').strip("'")
                
                if key == 'tags':
                    # 处理 tags: ["a", "b"] 或 tags: a, b
                    if value.startswith('['):
                        value = json.loads(value)
                    else:
                        value = [v.strip() for v in value.split(',')]
                
                if key in ('top',):
                    value = str(value).lower() in ('true', 'yes', '1')
                
                frontmatter[key] = value
    
    return frontmatter, body


def parse_article(filepath):
    """解析文章文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_content = f.read()
    
    frontmatter, body = parse_frontmatter(raw_content)
    
    # Markdown转HTML
    md = markdown.Markdown(extensions=[
        'fenced_code',
        'codehilite',
        'tables',
        'toc',
        'nl2br',
        'sane_lists',
    ])
    content_html = md.convert(body)
    
    # 日期处理
    date_str = frontmatter.get('date', '')
    try:
        article_date = datetime.strptime(date_str, '%Y-%m-%d')
    except:
        article_date = datetime.now()
    
    return Article(
        slug=frontmatter.get('slug', os.path.splitext(os.path.basename(filepath))[0]),
        title=frontmatter.get('title', '无标题'),
        category=frontmatter.get('category', '未分类'),
        tags=frontmatter.get('tags', []),
        summary=frontmatter.get('summary', ''),
        author=frontmatter.get('author', config.SITE_CONFIG['name']),
        source=frontmatter.get('source', ''),
        date=article_date,
        cover=frontmatter.get('cover', ''),
        content=content_html,
        top=frontmatter.get('top', False),
    )


def load_articles(articles_dir):
    """加载所有文章"""
    articles = []
    
    if not os.path.exists(articles_dir):
        print(f"警告: 文章目录不存在: {articles_dir}")
        return articles
    
    # 递归扫描所有.md文件
    for root, dirs, files in os.walk(articles_dir):
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                try:
                    article = parse_article(filepath)
                    articles.append(article)
                except Exception as e:
                    print(f"解析文章失败 {filename}: {e}")
    
    # 按日期倒序
    articles.sort(key=lambda x: x.date, reverse=True)
    
    return articles


def get_related_articles(current_article, all_articles, count=3):
    """获取相关文章"""
    related = []
    
    for article in all_articles:
        if article.slug == current_article.slug:
            continue
        
        # 计算相关度：同分类+2分，同标签+1分
        score = 0
        if article.category == current_article.category:
            score += 2
        for tag in article.tags:
            if tag in current_article.tags:
                score += 1
        
        if score > 0:
            related.append((score, article))
    
    # 按相关度排序
    related.sort(key=lambda x: x[0], reverse=True)
    
    return [a[1] for a in related[:count]]


def generate_breadcrumb(items):
    """生成面包屑数据"""
    return items


def build_site():
    """构建网站"""
    print("=" * 50)
    print(f"开始构建: {config.SITE_CONFIG['name']}")
    print("=" * 50)
    
    # 创建Jinja2环境
    env = Environment(
        loader=FileSystemLoader(config.BUILD_CONFIG['templates_dir']),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # 添加自定义过滤器
    env.filters['truncatewords'] = lambda s, n: s[:200] + '...' if len(s) > 200 else s
    
    # 加载模板
    base_template = env.get_template('base.html')
    index_template = env.get_template('index.html')
    article_template = env.get_template('article.html')
    category_template = env.get_template('category.html')
    about_template = env.get_template('about.html')
    
    # 确保输出目录存在
    output_dir = config.BUILD_CONFIG['output_dir']
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f"{output_dir}/articles", exist_ok=True)
    os.makedirs(f"{output_dir}/categories", exist_ok=True)
    os.makedirs(f"{output_dir}/css", exist_ok=True)
    os.makedirs(f"{output_dir}/assets/images", exist_ok=True)
    
    # 复制静态资源
    import shutil
    assets_src = config.BUILD_CONFIG['assets_dir']
    if os.path.exists(assets_src):
        for item in ['css', 'images', 'js']:
            src = f"{assets_src}/{item}"
            if os.path.exists(src):
                dst = f"{output_dir}/{item}" if item != 'images' else f"{output_dir}/assets/images"
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
    
    # 加载文章
    articles_dir = config.BUILD_CONFIG['articles_dir']
    articles = load_articles(articles_dir)
    print(f"加载文章: {len(articles)} 篇")
    
    # 构建上下文
    # 获取当前站点的配置
    active_site_id = getattr(config, 'ACTIVE_SITE', config.SITE_CONFIG['id'])
    site_categories_config = config.CATEGORIES.get(active_site_id, [])
    
    # 如果是字典结构（zhizaozx格式），取其中的categories列表；否则直接使用
    if isinstance(site_categories_config, dict):
        site_categories = site_categories_config.get('categories', [])
    else:
        site_categories = site_categories_config
    
    # 动态生成导航链接（首页 + 分类 + 关于我们）
    dynamic_nav_links = [
        {"name": "首页", "url": "/"},
    ]
    # 添加前3个分类作为导航
    for cat in site_categories[:4]:
        dynamic_nav_links.append({
            "name": cat['name'],
            "url": f"/categories/{cat['slug']}.html"
        })
    dynamic_nav_links.append({"name": "关于我们", "url": "/about.html"})
    
    context = {
        'site': config.SITE_CONFIG,
        'contact': config.CONTACT,
        'social': config.SOCIAL,
        'nav_links': dynamic_nav_links,  # 使用动态生成的导航
        'categories': site_categories,  # 使用当前站点的分类列表
        'active_site': active_site_id,
    }
    
    # ========== 生成首页 ==========
    print("生成首页...")
    top_articles = [a for a in articles if a.top][:1]
    recent_articles = articles[:config.PAGINATION['home_article_count']]
    
    home_context = {
        **context,
        'top_article': top_articles[0] if top_articles else None,
        'articles': recent_articles,
    }
    
    with open(f"{output_dir}/index.html", 'w', encoding='utf-8') as f:
        f.write(index_template.render(**home_context))
    
    # ========== 生成文章页 ==========
    print("生成文章页...")
    for article in articles:
        article_context = {
            **context,
            'article': article,
            'related_articles': get_related_articles(article, articles, config.PAGINATION['related_article_count']),
            'breadcrumb': generate_breadcrumb([
                {'name': '首页', 'url': '/'},
                {'name': article.category, 'url': f'/categories/{article.category}.html'},
                {'name': article.title, 'url': article.url},
            ]),
        }
        
        with open(f"{output_dir}/articles/{article.slug}.html", 'w', encoding='utf-8') as f:
            f.write(article_template.render(**article_context))
    
    # ========== 生成分类页 ==========
    print("生成分类页...")
    for cat in site_categories:
        cat_articles = [a for a in articles if a.category == cat['name']]
        cat_context = {
            **context,
            'category': cat,
            'articles': cat_articles,
            'breadcrumb': generate_breadcrumb([
                {'name': '首页', 'url': '/'},
                {'name': cat['name'], 'url': f'/categories/{cat["slug"]}.html'},
            ]),
        }
        
        with open(f"{output_dir}/categories/{cat['slug']}.html", 'w', encoding='utf-8') as f:
            f.write(category_template.render(**cat_context))
    
    # ========== 生成关于页 ==========
    print("生成关于页...")
    about_context = {
        **context,
        'about_content': config.ABOUT_CONTENT,
        'breadcrumb': generate_breadcrumb([
            {'name': '首页', 'url': '/'},
            {'name': '关于我们', 'url': '/about.html'},
        ]),
    }
    
    with open(f"{output_dir}/about.html", 'w', encoding='utf-8') as f:
        f.write(about_template.render(**about_context))
    
    # ========== 生成搜索页 ==========
    print("生成搜索页...")
    with open(f"{output_dir}/search.html", 'w', encoding='utf-8') as f:
        f.write(env.get_template('search.html').render(**context))
    
    # ========== 生成站点地图 ==========
    print("生成站点地图...")
    from generate_sitemap import generate_sitemap
    generate_sitemap(articles, config, output_dir)
    
    print("=" * 50)
    print(f"构建完成! 输出目录: {output_dir}")
    print("=" * 50)


if __name__ == '__main__':
    build_site()
