# -*- coding: utf-8 -*-
"""
Sitemap生成器
生成sitemap.xml和feed.xml
"""

from datetime import datetime


def generate_sitemap(articles, config, output_dir):
    """生成站点地图"""
    
    site = config.SITE_CONFIG
    base_url = f"https://{site['domain']}"
    
    # ========== sitemap.xml ==========
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    
    # 首页
    sitemap_lines.append('  <url>')
    sitemap_lines.append(f'    <loc>{base_url}/</loc>')
    sitemap_lines.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
    sitemap_lines.append('    <changefreq>daily</changefreq>')
    sitemap_lines.append('    <priority>1.0</priority>')
    sitemap_lines.append('  </url>')
    
    # 关于页
    sitemap_lines.append('  <url>')
    sitemap_lines.append(f'    <loc>{base_url}/about.html</loc>')
    sitemap_lines.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
    sitemap_lines.append('    <changefreq>monthly</changefreq>')
    sitemap_lines.append('    <priority>0.5</priority>')
    sitemap_lines.append('  </url>')
    
    # 分类页
    active_site_id = getattr(config, 'ACTIVE_SITE', config.SITE_CONFIG['id'])
    site_categories_config = config.CATEGORIES.get(active_site_id, [])
    if isinstance(site_categories_config, dict):
        site_categories = site_categories_config.get('categories', [])
    else:
        site_categories = site_categories_config
    for cat in site_categories:
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{base_url}/categories/{cat["slug"]}.html</loc>')
        sitemap_lines.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
        sitemap_lines.append('    <changefreq>daily</changefreq>')
        sitemap_lines.append('    <priority>0.8</priority>')
        sitemap_lines.append('  </url>')
    
    # 文章页
    for article in articles:
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{base_url}{article.url}</loc>')
        sitemap_lines.append(f'    <lastmod>{article.formatted_date}</lastmod>')
        sitemap_lines.append('    <changefreq>weekly</changefreq>')
        sitemap_lines.append('    <priority>0.9</priority>')
        sitemap_lines.append('  </url>')
    
    sitemap_lines.append('</urlset>')
    
    with open(f"{output_dir}/sitemap.xml", 'w', encoding='utf-8') as f:
        f.write('\n'.join(sitemap_lines))
    
    print(f"  - sitemap.xml: {len(articles) + len(config.CATEGORIES) + 2} URLs")
    
    # ========== feed.xml (RSS) ==========
    feed_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        '  <channel>',
        f'    <title>{site["name"]}</title>',
        f'    <link>{base_url}</link>',
        f'    <description>{site["description"]}</description>',
        f'    <language>zh-CN</language>',
        f'    <lastBuildDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0800")}</lastBuildDate>',
        f'    <atom:link href="{base_url}/feed.xml" rel="self" type="application/rss+xml"/>',
    ]
    
    for article in articles[:20]:  # RSS只显示最新20篇
        feed_lines.append('    <item>')
        feed_lines.append(f'      <title>{escape_xml(article.title)}</title>')
        feed_lines.append(f'      <link>{base_url}{article.url}</link>')
        feed_lines.append(f'      <guid>{base_url}{article.url}</guid>')
        feed_lines.append(f'      <pubDate>{article.date.strftime("%a, %d %b %Y %H:%M:%S +0800")}</pubDate>')
        feed_lines.append(f'      <description>{escape_xml(article.summary)}</description>')
        feed_lines.append('    </item>')
    
    feed_lines.extend([
        '  </channel>',
        '</rss>',
    ])
    
    with open(f"{output_dir}/feed.xml", 'w', encoding='utf-8') as f:
        f.write('\n'.join(feed_lines))
    
    print(f"  - feed.xml: {min(20, len(articles))} 篇文章")


def escape_xml(text):
    """转义XML特殊字符"""
    if not text:
        return ""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text
