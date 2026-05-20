#!/usr/bin/env python3
"""IndexNow推送脚本 - 向搜索引擎即时提交通知"""
import requests
import json
import sys
import os
import glob
import re

INDEXNOW_KEY = "gwcwqiimjsot76xgi4xs2jiudfvekmj7"

SITES = {
    "zhizaozx": "https://zhizaozx.cn",
    "jiaopeizx": "https://jiaopeizx.cn",
    "xfzaixian": "https://xfzaixian.cn",
    "muyingzx": "https://muyingzx.cn",
    "nongzizx": "https://nongzizx.cn",
    "caifazx": "https://caifazx.cn",
}

def push_to_indexnow(site_key, urls):
    """推送URL列表到IndexNow"""
    site_url = SITES[site_key]
    key_url = f"{site_url}/{INDEXNOW_KEY}.txt"
    
    payload = {
        "host": site_url.replace("https://", ""),
        "key": INDEXNOW_KEY,
        "keyLocation": key_url,
        "urlList": urls
    }
    
    # 推送到Bing IndexNow端点
    try:
        response = requests.post(
            "https://api.indexnow.org/indexnow",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"  Bing IndexNow: {response.status_code} {response.text if response.text else 'OK'}")
        return response.status_code == 200
    except Exception as e:
        print(f"  Bing IndexNow 失败: {e}")
        return False

def get_all_urls(site_key, sites_dir="/tmp/geo-sites/sites"):
    """从sitemap或HTML文件提取所有URL"""
    domain = SITES[site_key].replace("https://", "")
    site_path = os.path.join(sites_dir, site_key)
    urls = []
    
    # 从sitemap.xml提取
    sitemap = os.path.join(site_path, "sitemap.xml")
    if os.path.exists(sitemap):
        with open(sitemap, 'r') as f:
            content = f.read()
        url_matches = re.findall(r'<loc>(.*?)</loc>', content)
        urls = url_matches
    
    return urls

if __name__ == "__main__":
    if len(sys.argv) > 1:
        site_keys = [sys.argv[1]]
    else:
        site_keys = list(SITES.keys())
    
    for site_key in site_keys:
        if site_key not in SITES:
            print(f"未知站点: {site_key}")
            continue
        urls = get_all_urls(site_key)
        if urls:
            print(f"推送 {site_key}: {len(urls)} 个URL")
            # IndexNow每次最多10000个URL
            for i in range(0, len(urls), 10000):
                batch = urls[i:i+10000]
                push_to_indexnow(site_key, batch)
        else:
            print(f"{site_key}: 没有找到URL")
