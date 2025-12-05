import requests
from bs4 import BeautifulSoup

# 获取China Daily主页内容
response = requests.get('https://www.chinadaily.com.cn/')
html_content = response.text

# 解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 查找包含新闻内容的div元素
print("=== 查找新闻内容div ===")
# 根据之前的分析，有些div包含了"Xi, Macron have friendly exchanges"这样的新闻内容
divs_with_news = soup.find_all('div')

for div in divs_with_news:
    content = div.get_text(strip=True)
    if 'Xi, Macron' in content:
        print(f"找到包含新闻的div: class={div.get('class')}, id={div.get('id')}")
        
        # 查看这个div的完整结构
        print("\n这个div的完整结构:")
        print(div.prettify())
        
        # 查看这个div的直接子元素
        print("\n这个div的直接子元素:")
        for child in div.children:
            if child.name:
                print(f"  {child.name}: class={child.get('class')}, id={child.get('id')}")
        break  # 只查看第一个包含该新闻的div

# 查找新闻列表，通常新闻列表会是ul或ol元素
print("\n=== 查找新闻列表 ===")
uls = soup.find_all('ul', limit=20)
for i, ul in enumerate(uls):
    # 检查ul是否包含多个新闻链接
    news_links = ul.find_all('a')
    if len(news_links) > 5:
        print(f"找到可能的新闻列表 {i}: {ul.get('class')}, {ul.get('id')}")
        print(f"  包含 {len(news_links)} 个链接")
        # 查看前3个链接
        for j, link in enumerate(news_links[:3]):
            link_text = link.get_text(strip=True)
            href = link.get('href')
            if link_text and href:
                print(f"    {j+1}. {link_text[:50]} -> {href}")

# 查找头条新闻
print("\n=== 查找头条新闻 ===")
# 尝试查找h1, h2, h3标签，通常头条新闻会用这些标题标签
headlines = soup.find_all(['h1', 'h2', 'h3'], limit=15)
for i, headline in enumerate(headlines):
    headline_text = headline.get_text(strip=True)
    if headline_text:
        # 查找标题对应的链接
        link = headline.find('a') or headline.parent.find('a')
        href = link['href'] if link else 'No link'
        print(f"Headline {i+1}: {headline_text[:60]} -> {href}")

# 尝试查找新闻区域的特定类
print("\n=== 查找特定类的新闻区域 ===")
# 根据常见的新闻区域类名查找
news_classes = ['news', 'headline', 'topnews', 'mainnews', 'latest', 'breaking']
for news_class in news_classes:
    elements = soup.find_all(['div', 'ul'], class_=lambda x: x and news_class in x.lower())
    if elements:
        print(f"找到 {len(elements)} 个包含 '{news_class}' 的元素")
        for i, element in enumerate(elements[:2]):  # 只查看前2个
            print(f"  {i+1}. {element.name}: class={element.get('class')}")
            # 查看内部的新闻链接
            links = element.find_all('a')[:3]
            for link in links:
                link_text = link.get_text(strip=True)
                href = link['href'] if link else 'No link'
                if link_text:
                    print(f"    - {link_text[:40]} -> {href}")

# 尝试查找主页上的所有新闻条目
print("\n=== 查找所有新闻条目 ===")
all_news = []
# 查找所有包含新闻标题的a标签
for link in soup.find_all('a'):
    link_text = link.get_text(strip=True)
    href = link.get('href')
    
    # 过滤条件：链接文本长度合适，href看起来是新闻链接
    if (link_text and len(link_text) > 10 and len(link_text) < 100 and 
        href and ('http' in href or href.startswith('//')) and 
        any(keyword in href for keyword in ['china', 'world', 'business', 'life', 'culture', 'sports', 'opinion'])):
        
        # 补全相对链接
        if href.startswith('//'):
            href = 'https:' + href
        elif not href.startswith('http'):
            href = 'https://www.chinadaily.com.cn' + href
            
        all_news.append((link_text, href))

# 去重并显示前20条新闻
print(f"\n共找到 {len(all_news)} 条可能的新闻")
seen = set()
unique_news = []
for news in all_news:
    if news[0] not in seen:
        seen.add(news[0])
        unique_news.append(news)

for i, (title, url) in enumerate(unique_news[:20]):
    print(f"{i+1}. {title} -> {url}")