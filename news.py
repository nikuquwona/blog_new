import requests
import json
from datetime import date
import os
import subprocess
from bs4 import BeautifulSoup
import re

def get_us_news():
    # 使用NewsAPI获取美国新闻
    API_KEY = "c06f14d0e7f74454b214d2afd3d3b300"
    #https://newsapi.org/v2/everything?q=tesla&from=2024-05-23&sortBy=publishedAt&apiKey=c06f14d0e7f74454b214d2afd3d3b300
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)['articles'][0]
    else:
        raise Exception("Failed to fetch news")

def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        img_name = f"news_image_{date.today().strftime('%Y%m%d')}.jpg"
        img_path = os.path.join('/Users/lhd/lhd_blog/source/images', img_name)
        with open(img_path, 'wb') as f:
            f.write(response.content)
        return f'/images/{img_name}'
    return None

def create_hexo_post(title, content, image_path,article):
    today = date.today().strftime("%Y-%m-%d")
    slug = re.sub(r'[^\w\-]', '-', title.lower())
    post_content = f"""---
title: '{title}'
date: {today}
tags: [news, us]
---

![News Image]({image_path})

{content}

[Read more]({article['url']})
"""
    post_path = f'/Users/lhd/lhd_blog/source/_posts/{today}-{slug}.md'
    with open(post_path, 'w') as f:
        f.write(post_content)
    return post_path

def push_to_git():
    os.chdir('/Users/lhd/lhd_blog')
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', f"Add news post for {date.today().strftime('%Y-%m-%d')}"])
    subprocess.run(['git', 'push'])

def main():
    # 获取新闻
    article = get_us_news()
    
    # 下载图片
    image_path = download_image(article['urlToImage'])
    
    # 创建Hexo文章
    post_path = create_hexo_post(article['title'], article['description'], image_path,article)
    
    # 生成静态文件
    subprocess.run(['hexo', 'generate'])
    
    # 推送到Git
    push_to_git()
    
    print(f"New blog post created and pushed: {post_path}")

if __name__ == "__main__":
    main()