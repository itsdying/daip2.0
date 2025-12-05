import requests
from bs4 import BeautifulSoup

# 获取China Daily主页内容
response = requests.get('https://www.chinadaily.com.cn/')
html_content = response.text

# 解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 查看页面标题
print(f"页面标题: {soup.title.string}")

# 查找新闻相关的元素，通常新闻列表会在特定的div或ul中
# 先查看所有的div元素，寻找可能包含新闻的容器
print("\n=== 查找可能的新闻容器 ===")
divs = soup.find_all('div', limit=20)  # 只查看前20个div元素
for i, div in enumerate(divs):
    # 检查div是否包含新闻相关的类或id
    if div.get('class') or div.get('id'):
        print(f"Div {i}: class={div.get('class')}, id={div.get('id')}")
        # 查看div内部的内容摘要
        content = div.get_text(strip=True)[:100]
        if content:
            print(f"  内容摘要: {content}...")

# 尝试查找所有的a标签，新闻通常是链接形式
print("\n=== 查找可能的新闻链接 ===")
links = soup.find_all('a', limit=30)  # 只查看前30个链接
for i, link in enumerate(links):
    # 检查链接文本和href
    link_text = link.get_text(strip=True)
    href = link.get('href')
    if link_text and href:
        print(f"Link {i}: {link_text[:50]} -> {href[:100]}")

# 尝试查找特定的新闻区域，比如头条新闻
print("\n=== 查找头条新闻 ===")
# 尝试根据常见的新闻区域类名查找
headline_divs = soup.find_all(['div', 'h2', 'h3'], class_=lambda x: x and ('headline' in x.lower() or 'topnews' in x.lower() or 'mainnews' in x.lower()))
for div in headline_divs:
    print(f"Headline: {div.get_text(strip=True)} -> {div.find('a')['href'] if div.find('a') else 'No link'}")

# 查看页面的主要内容区域
print("\n=== 查看页面主要内容区域 ===")
main_content = soup.find('main') or soup.find('div', class_='main-content') or soup.find('div', id='content')
if main_content:
    print(f"找到主要内容区域: {main_content.get('class')}, {main_content.get('id')}")
    # 查看主要内容区域内的链接
    main_links = main_content.find_all('a', limit=20)
    for i, link in enumerate(main_links):
        link_text = link.get_text(strip=True)
        href = link.get('href')
        if link_text and href:
            print(f"  Link {i}: {link_text[:50]} -> {href[:100]}")
else:
    print("未找到明确的主要内容区域")