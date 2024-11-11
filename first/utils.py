import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from gensim.parsing.preprocessing import remove_stopwords

from .config import header


def crawl_bloomberg(topic):
    domain = "https://www.bloomberg.com"
    res = requests.get(f"{domain}/{topic}/", headers=header)
    soup = BeautifulSoup(res.text, "lxml")
    news = soup.find_all(class_="StoryBlock_storyLink__5nXw8")
    data = []
    for i in range(len(news)):
        link = news[i]["href"]
        if link.startswith("/news"):
            article = [news[i].text, link, link.split("/")[3]]
            data.append(article)
    data = pd.DataFrame(data, columns=["title", "link", "date"])
    data["link"] = domain + data["link"]
    data["src"] = "bloomberg"
    return data


def crawl_tnw(topic):
    domain = "https://thenextweb.com"
    data = []
    #     for i in range(1, ):
    #         res = requests.get(f"{domain}/{topic}/page/{i}", headers=header)
    res = requests.get(f"{domain}/{topic}", headers=header)
    soup = BeautifulSoup(res.text, "lxml")
    news = soup.find_all("article")
    for i in range(len(news)):
        article = [
            news[i].find("h2").text.strip(),
            f"{news[i].find('h2').find('a')['href']}",
        ]
        metadata = news[i].find_all(class_="c-meta__item")
        article.extend([content.text for content in metadata])
        data.append(article)
    data = pd.DataFrame(data, columns=["title", "link", "author", "date"])
    data["link"] = domain + data["link"]
    data["src"] = "tnw"
    return data


def preprocessing(sentence):
    sentence = re.sub(r"[^a-zA-Z0-9\s]", "", sentence).strip().lower()
    return remove_stopwords(sentence)
