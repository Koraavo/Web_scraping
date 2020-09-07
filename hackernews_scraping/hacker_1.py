import requests
from bs4 import BeautifulSoup
import json

# html = requests.get("https://thehackernews.com/")
# print(html.text)

# with open("news.html", 'w') as news_html:
#     news_html.write(html.text)


results = []
html = ""
with open("news.html", 'r') as news_html:
    for line in news_html.read():
        html += line

content = BeautifulSoup(html, "lxml")
# print(content)

titles = [title.text for title in content.findAll("h2", {"class": "home-title"})]
links = [link["href"] for link in content.findAll("a", {"class": "story-link"})]
infos = content.findAll("div", {"class": "item-label"})
date = [[i for i in date][1] for date in infos]
authors = [[i for i in writer][2].text.strip()[1:] for writer in infos]
desc = [desc.text.strip() for desc in content.findAll("div", {"class": "home-desc"})]
next_page = content.find("a", {"class": "blog-pager-older-link-mobile"})["href"]

for index in range(len(titles)):
    results.append({
        'Titles': titles[index],
        'Links': links[index],
        'Date': date[index],
        'Authors': authors[index],
        'Description': desc[index]
    })

print(results)

