import datetime
import pandas as pd
import numpy as np
from gensim.models.word2vec import Word2Vec
from django.shortcuts import render
from django.http import HttpResponse

# from .config import header
from .utils import crawl_bloomberg, crawl_tnw, preprocessing

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)
# browser = webdriver.Chrome('./chromedriver')
# browser.get('https://www.bloomberg.com/asia')
# soup2=BeautifulSoup(browser.page_source, "lxml")
# browser.close()

# bb = ["artificial-intelligence", "big-data", "cloud-computing", "mobile-phones"]
bloomberg_topics = ["ai", "big-tech", "cybersecurity", "startups", "screentime"]
tnw_topics = [
    "deep-tech",
    "sustainability",
    "ecosystems",
    "data-security",
    "fintech-ecommerce",
    "future-of-work",
]

references = crawl_tnw("latest").head()

data = pd.concat(
    [crawl_bloomberg(topic) for topic in bloomberg_topics]
    + [crawl_tnw(topic) for topic in tnw_topics],
    ignore_index=True,
)
data = data.drop_duplicates(subset=["link"]).reset_index(drop=True)
data = data.fillna("")
x = data["title"].apply(lambda x: preprocessing(x)).tolist()
x = [sentence.split(" ") for sentence in x]
model = Word2Vec(vector_size=150, min_count=1, epochs=20, sg=1, window=5)
model.build_vocab(x)
model.train(x, total_examples=model.corpus_count, epochs=30)


# data1 = pd.DataFrame(data, columns=["title", "link", "author", "date", "src"])
# data1.drop_duplicates(subset="title", keep="first", inplace=True)
# data1 = data1.reset_index(drop=True)
# print(data1)
# x = []

# for i in data1["title"]:
#     i = re.sub(r"[^a-zA-Z0-9\s]", "", i).strip().lower()
#     x.append(remove_stopwords(i).split(" "))

# # train word2vec model
# model = Word2Vec(vector_size=150, min_count=1, epochs=20, sg=1, window=5)
# print(x)
# model.build_vocab(x)
# model.train(x)
# # title 2 vec
# vec = []
# for i in range(len(x)):
#     v = np.zeros(150)
#     for j in x[i]:
#         v = v + model.wv[j]
#     vec.append((v / len(x[i])).tolist())

# data2 = pd.DataFrame(vec)
# print(np.dot(data2.loc[2],model['ai']))


def current_datetime():
    now = datetime.datetime.now().strftime("%Y/%m/%d")
    c = {"date": now}
    return c


#    return render(request, 'index.html', c)


def hello_world(request):
    return HttpResponse("Hello World!")


def welcome(request):
    now = current_datetime()
    # now = datetime.datetime.now().strftime('%Y/%m/%d')
    now["references"] = references["link"].tolist()
    print(now)
    return render(request, "index.html", now)


def simlarity(word1, sentence):
    if word1 not in model.wv.key_to_index:
        print(word1, "not in vocab")
        return np.random.uniform(0, 1, 1)
    cosine = []
    for word2 in sentence:
        cosine.append(model.wv.similarity(word1, word2))
    return max(cosine)


# def similarity(x):
#     cos = []
#     print(model.wv)
#     if x in model.wv.Vocab:
#         v1 = np.array(model[x])
#         for i in range(len(data2)):
#             v2 = np.array(data2.loc[i])
#             cos.append(
#                 [
#                     data1["title"][i],
#                     data1["link"][i],
#                     data1["author"][i],
#                     data1["date"][i],
#                     np.dot(v1, v2),
#                     data1["src"][i],
#                 ]
#             )
#         cos = pd.DataFrame(cos)
#         tnw = cos[cos[5] == "tnw"].sort_values(by=4, ascending=False).head(10)
#         bloom = cos[cos[5] == "bloom"].sort_values(by=4, ascending=False).head(10)
#     else:
#         tnw = []
#         bloom = []
#         print("not found")
#         t = data1[data1["src"] == "tnw"].reset_index(drop=True)
#         b = data1[data1["src"] == "bloom"].reset_index(drop=True)
#         draw1 = np.random.choice([i for i in t.index.tolist()], 10, replace=False)
#         draw2 = np.random.choice([i for i in b.index.tolist()], 10, replace=False)
#         draw = np.concatenate((draw1, draw2))
#         for i in range(20):
#             if i < 10:
#                 tnw.append(
#                     [
#                         data1["title"][draw[i]],
#                         data1["link"][draw[i]],
#                         data1["author"][draw[i]],
#                         data1["date"][draw[i]],
#                     ]
#                 )
#             else:
#                 bloom.append(
#                     [
#                         data1["title"][draw[i]],
#                         data1["link"][draw[i]],
#                         data1["author"][draw[i]],
#                         data1["date"][draw[i]],
#                     ]
#                 )

#         tnw = pd.DataFrame(tnw)
#         bloom = pd.DataFrame(bloom)
#     return tnw.reset_index(drop=True), bloom.reset_index(drop=True)


# def others(x):
#     if x in model.wv.vocab:
#         return model.wv.most_similar(x, topn=10)
#     else:
#         return []


def scrape1(request):
    key = request.GET["keyword"]
    site = request.GET["site"]
    print(site)
    print(key)
    cosine = [simlarity(key.lower(), sentence) for sentence in x]
    data["similarity"] = cosine
    # find = similarity(key.lower())
    if site == "TNW":
        result = (
            data[data["src"] == "tnw"]
            .sort_values(by=["similarity"], ascending=False)
            .head(10)
        )
        # result = find[0]
    else:
        result = (
            data[data["src"] == "bloomberg"]
            .sort_values(by=["similarity"], ascending=False)
            .head(10)
        )
        # result = find[1]

    # more = others(key.lower())
    # print(result)
    c = current_datetime()
    c["s"] = site
    c["k"] = key
    for i in range(10):
        c["r" + str(i + 1)] = result["title"].iloc[i]
        c["l" + str(i + 1)] = result["link"].iloc[i]
        c["a" + str(i + 1)] = result["author"].iloc[i]
        c["d" + str(i + 1)] = result["date"].iloc[i]
    #         c["r" + str(i + 1)] = result[0][i]
    #         c["l" + str(i + 1)] = result[1][i]
    #         c["a" + str(i + 1)] = result[2][i]
    #         c["d" + str(i + 1)] = result[3][i]
    return render(request, "try.html", c)


# test=similarity('ai')
# print(test)
# for i in range(10):
#    print(test[0][i])
# Create your views here.
