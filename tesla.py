import requests
import json
from datetime import date, timedelta
import os
import subprocess
from bs4 import BeautifulSoup
import re
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 配置请求会话
def create_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries,
                  backoff_factor=backoff_factor, status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# 全局会话
session = create_session()

def get_tesla_news():
    API_ENDPOINT = "https://newsapi.org/v2/everything?q=tesla&from=2024-05-23&sortBy=publishedAt&apiKey=c06f14d0e7f74454b214d2afd3d3b300"
    try:
        response = session.get(API_ENDPOINT)
        response.raise_for_status()
        return response.json()['articles']
    except requests.RequestException as e:
        logging.error(f"Error fetching news: {e}")
        return []

def download_image(image_url, index):
    try:
        response = session.get(image_url, timeout=10)
        response.raise_for_status()
        img_name = f"tesla_news_image_{date.today().strftime('%Y%m%d')}_{index}.jpg"
        img_path = os.path.join('/Users/lhd/lhd_blog/source/images', img_name)
        with open(img_path, 'wb') as f:
            f.write(response.content)
        return f'/images/{img_name}'
    except requests.RequestException as e:
        logging.warning(f"Failed to download image {image_url}: {e}")
        return None

def create_hexo_post(articles):
    today = date.today().strftime("%Y-%m-%d")
    post_content = f"""---
title: 'Tesla News Update {today}'
date: {today}
tags: [Tesla, news, technology]
---

# Tesla News Update for {today}

"""
    for index, article in enumerate(articles, 1):
        image_path = download_image(article.get('urlToImage'), index) if article.get('urlToImage') else None
        
        post_content += f"""
## {index}. {article['title']}

{f'![News Image {index}]({image_path})' if image_path else ''}

**Source:** {article['source']['name']}
**Author:** {article.get('author', 'Unknown')}
**Published at:** {article['publishedAt']}

{article.get('description', 'No description available.')}

{article.get('content', 'No content available.')}

[Read full article]({article['url']})

---

"""

    slug = f"tesla-news-update-{today}"
    post_path = f'/Users/lhd/lhd_blog/source/_posts/{today}-{slug}.md'
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(post_content)
    return post_path

def push_to_git():
    os.chdir('/Users/lhd/lhd_blog')
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', f"Add Tesla news update for {date.today().strftime('%Y-%m-%d')}"], check=True)
        subprocess.run(['git', 'push'], check=True)
        logging.info("Successfully pushed to git")
    except subprocess.CalledProcessError as e:
        logging.error(f"Git operation failed: {e}")

def main():
    # 获取Tesla相关新闻
    articles = get_tesla_news()
    if not articles:
        logging.error("No articles fetched. Exiting.")
        return
    
    # 创建包含所有Tesla新闻的Hexo文章
    post_path = create_hexo_post(articles)
    logging.info(f"Created new blog post: {post_path}")
    
    # 生成静态文件
    try:
        subprocess.run(['hexo', 'generate'], check=True)
        logging.info("Successfully generated static files")
    except subprocess.CalledProcessError as e:
        logging.error(f"Hexo generate failed: {e}")
        return
    
    # 推送到Git
    push_to_git()

if __name__ == "__main__":
    main()