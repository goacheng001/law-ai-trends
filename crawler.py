"""
法律AI工具热门内容抓取脚本
定时抓取公众号、B站、抖音、小红书相关内容
"""
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# 搜索关键词组合
KEYWORDS = [
    "律师 OpenClaw",
    "律师 龙虾", 
    "律师 Codex",
    "律师 AI 编程",
    "极客律师 AI"
]

def search_wechat(keyword):
    """搜狗微信搜索"""
    url = f"https://wx.sogou.com/weixin?type=2&query={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []
        for item in soup.select('.news-list li')[:5]:
            title = item.select_one('.txt-box h3')
            if title:
                results.append({
                    "title": title.get_text(strip=True),
                    "source": item.select_one('.txt-box .source') or "微信公众号",
                    "url": item.select_one('a')['href'] if item.select_one('a') else ""
                })
        return results
    except Exception as e:
        print(f"微信搜索失败: {e}")
        return []

def search_bilibili(keyword):
    """B站搜索"""
    url = f"https://search.bilibili.com/all?keyword={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []
        for item in soup.select('.video-list .video-item')[:5]:
            title = item.select_one('.title')
            if title:
                play = item.select_one('.stat .play')
                results.append({
                    "title": title.get_text(strip=True),
                    "play": play.get_text(strip=True) if play else "未知",
                    "url": "https:" + item.select_one('a')['href'] if item.select_one('a') else ""
                })
        return results
    except Exception as e:
        print(f"B站搜索失败: {e}")
        return []

def run_crawler():
    """执行抓取"""
    data = {
        "timestamp": datetime.now().isoformat(),
        "wechat": [],
        "bilibili": []
    }
    
    for kw in KEYWORDS:
        data["wechat"].extend(search_wechat(kw))
        data["bilibili"].extend(search_bilibili(kw))
    
    # 去重
    seen = set()
    unique_wechat = []
    for item in data["wechat"]:
        if item["title"] not in seen:
            seen.add(item["title"])
            unique_wechat.append(item)
    
    data["wechat"] = unique_wechat[:10]
    
    # 保存
    with open("data/content.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"抓取完成: {len(data['wechat'])} 条微信, {len(data['bilibili'])} 条B站")

if __name__ == "__main__":
    run_crawler()