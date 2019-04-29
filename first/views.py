import os
import re
import requests
import datetime
import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
from gensim.models.word2vec import Word2Vec
from gensim.parsing.preprocessing import remove_stopwords
from django.template.loader import get_template
from django import template
from django.shortcuts import render
from django.http import HttpResponse

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(BASE_DIR)
#browser = webdriver.Chrome('./chromedriver')
#browser.get('https://www.bloomberg.com/asia')
#soup2=BeautifulSoup(browser.page_source, "lxml")        
#browser.close()
header={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
cookie={'Cookie':'bbAbVisits=; _pxhd=13454216158b6040984aa59473f8e8c58afee405130bab7b7ce6760f0acbe119:0dba9291-6579-11e9-8a98-af765a57e617; _pxvid=0dba9291-6579-11e9-8a98-af765a57e617; _gcl_au=1.1.614990213.1555990622; bdfpc=004.1237252455.1555990622321; bb_geo_info={"country":"TW","region":"Asia"}|1556595422525; agent_id=a38696e7-22fc-4b11-bfed-991c13ad4029; session_id=5f66c929-d643-47be-a675-4b8ebaa01d7a; session_key=c7ab6f54c76a8b8802e41a374d168db4bb086027; _ga=GA1.2.113966775.1555990623; _fbp=fb.1.1555990623261.1136560034; __tbc=%7Bjzx%7Dt_3qvTkEkvt3AGEeiiNNgGxVi_KAWir-jO-bCXIvimUFYYPm2tuluc-P1WFZp68iGi0-r6dPDGWOwHlWrsLD2ytTUmHucBQFq-tXKiiMjB61llj0FW1eSq6m9GtEMwCpjylU0Z664w9lha1BgkmqDg; __pat=-14400000; __gads=ID=8617b4226f137b1e:T=1555990628:S=ALNI_MbqwvTUQqRmHIEYJPeGsSZYYk_D8A; optimizelyEndUserId=oeu1555990899693r0.8976113658748217; DigiTrust.v1.identity=eyJwcml2YWN5Ijp7Im9wdG91dCI6ZmFsc2V9LCJwcm9kdWNlciI6IjdjNk1QdGlpQWUiLCJ2ZXJzaW9uIjoyLCJpZCI6Ilp3TkdSV214SlIwdTFobkI4VUFxOVJ1bTRROHBXUUJzcXNyZDd6OWI2dkhDOFhiSXpOZzkzMjhWeFVZSUdYTmpoWGhUNDVETUd2WEw4SzduRUxUTndRb1VCOFN0UXVjTk5hVlZRQ1dQVDI0TVJkUXh4NmZibHFkQXhIOTVXTDYzMUlLMmNUWEJxY0VUOGZXcWdSWnE2TTljMDVZc1libVI5cHc1N3hWYXNjakhVL2Nsd3VrMzJ3Q2hndWtyNlltMzB5TElYVjZoL0N6SXpUalVkc294bWo2TTVEeWNESVVHR1hUR0t2VnF4MTFmRzVOVVZVQ3FPTExhMGNuNzhhQjFKc3YvOGFCWFJ5ZkxCcWVJaVBqRlRscDNRbkxjNk1KTitQZkIvU29oL09BcGNwK2srRkFONFVSc3Exd3h6MW1OaitQakRpOHMxOVY3OUtROTNzczdyUT09Iiwia2V5diI6NH0%3D; com.bloomberg.player.volume.level=1; _gid=GA1.2.57756858.1556339579; bb-mini-player-viewed=true; kw.pv_session=1; _sp_id.3377=b54bc0bc-dd57-4ffb-b504-4d9f9b451c60.1555991103.7.1556385219.1556381674.9ad9c642-e92d-43b4-bbb6-879c3c79cf2e; trc_cookie_storage=taboola%2520global%253Auser-id%3Df8e864c8-e7a5-466c-beb5-d7b6e218f321-tuct3bdb458; RT="sl=1&ss=1556384992206&tt=13607&obo=0&sh=1556385005861%3D1%3A0%3A13607&dm=www.bloomberg.com&si=2b192143-ef48-4fef-a322-83cddf9f78cc&bcn=%2F%2F0211c84d.akstat.io%2F&r=https%3A%2F%2Fwww.bloomberg.com%2Fopinion%2Farticles%2F2019-04-23%2Fbig-data-won-t-build-a-better-robot&ul=1556385494101&hd=1556385497265"; _user-status=anonymous; _user-ip=39.10.136.114; _user_newsletters=[]; notice_behavior=none; bbAbVisits=; _parsely_session={%22sid%22:7%2C%22surl%22:%22https://www.bloomberg.com/asia%22%2C%22sref%22:%22%22%2C%22sts%22:1556411634331%2C%22slts%22:1556381663323}; _parsely_visitor={%22id%22:%2234c49c6e-5506-4a8e-81ea-61f057b9bc01%22%2C%22session_count%22:7%2C%22last_session_ts%22:1556411634331}; _px2=eyJ1IjoiMmZmNGNkYTAtNjk1NS0xMWU5LWI0YTItNjE5NjJhZjVhOTUyIiwidiI6IjBkYmE5MjkxLTY1NzktMTFlOS04YTk4LWFmNzY1YTU3ZTYxNyIsInQiOjE1NTY0MTUzMjYwODYsImgiOiIwMTlmNTc5YmM2YTU4MGZkMTk0MjEzNTFjZmFmYTkwNjhkZmZlMDcxZDM0MDZjYWYzZGEyMmMwYWU1NTM4ZWY0In0=; _px3=4e0a1acfb3db6fb139ef7445776877ca9536e0cad05eb3eccfd6f69217915a56:V/7eNgjt61Nb5Pf2/Ckr7jd6jiy6NOSyfexaB4EOOO+e5SKr0HFbabZbic3b2HOrEP3+O/zx7/YLC5knYJj6pQ==:1000:EaQkwnKqPSN9FwE+uUlVIawkWo8LIN5vrVnwmw93+551amcLs53Ej/pxzWZAewFGBWMnOr9YCs00/LfnFCwf2ckidj72OartOTrd6RxeArdfbXrfZwhbNstDFs9aY7UBvP+zpvor4ibSB/oGdmp8qrx6lft67S9C4d+tLZ5VRtU=; __pvi=%7B%22id%22%3A%22v-2019-04-28-09-31-09-431-yabw0dtTn3RXxJoV-c5ab4b55a29298629ef86f4808c1c7a4%22%2C%22domain%22%3A%22.bloomberg.com%22%2C%22time%22%3A1556415069432%7D; xbc=%7Bjzx%7DKKPgcuOvyz7VNnjr58wXnxsTmLZtuPXEtmKHmbD7NT9R8UEVIxWbbZ3KBbZv62Zs_ZKFunNRAy3JcadfKT6YfOm5Aos1Dw-e21bs4s6LEPI1mAvK2Fy8GZADJR3zU6lQQjUrqlVAoJO1xMVEyjhiLeJspnrrbEkDwi4zvHKuj0CdEDSExcmMF4qhNVTvaGeNm7fqP2cZQgr39NiVOqq2o1dRUvid_NmqwSDYvGz6KsjXds-EE8YMmp4Xt_edTNVSPmWOMG9VPF4WGRN6JunBYBgKSOAnjYrayZvO3Aa19AL7bnsINozHLYtHtWM5rSJFCZldjPrWTyIWF68PSxlTmixuhGP1PX560w5B-B__60zPxMVPuJGmMGer-rUfRvZ0pti3gqGBVdzwGz7dy-0ObPxBTwcPF09JSJbiIoSfrp3gaMEbSYBrbGsKqrCgc7cL; _pxde=3a730bce2bb0431cb5126472b18cae5cc0f9936f9c47edc4c667aeb59cab0a31:eyJ0aW1lc3RhbXAiOjE1NTY0MTUxMzM5MzEsImlwY19pZCI6W119'}

bb=['artificial-intelligence','big-data','cloud-computing','mobile-phones']
data=[]
print('start to crawl tnw')
for i in range(20):
    if i ==0:    
        res1=requests.get('http://thenextweb.com/section/tech/')
    else:
        res1=requests.get('http://thenextweb.com/section/tech/page/'+str(i+1)+'/')
    
    soup1=BeautifulSoup(res1.text, "lxml")        
    news=soup1.find_all('h4')
    make=soup1.find_all(class_='story-byline')
    time=soup1.find_all('time')
    for j in range(len(news)):
        link=news[j].find('a')['href']
        title=re.sub(r'[^a-zA-Z\s.?()''/-:]','',news[j].text).strip()
        author=re.sub(r'[^a-zA-Z\s.?()''/-:]','',make[j].text).strip()
        date=time[j]['datetime'].split('T')[0]
        data.append([title,link,author,date,'tnw'])
    print (i)

print('start to crawl bloomberg')
for i in bb:
    print(i)
    res2=requests.get('https://www.bloomberg.com/topics/'+i,headers=header, cookies=cookie)
    soup2=BeautifulSoup(res2.text, "html.parser")   
    news=soup2.find_all(class_='index-page__headline')
    time=soup2.find_all(class_='published-at')
    a=soup2.find_all(class_='index-page__headline-link')
    for j in range(len(time)):
        title=re.sub(r'[^a-zA-Z\s.?()''/-:]','',news[j].text)
        link='https://www.bloomberg.com'+a[j]['href']
        date=time[j]['datetime'].split('T')[0]
        author=''
        data.append([title,link,author,date,'bloom'])
        

        
    
data1=pd.DataFrame(data,columns=['title','link','author','date','src'])
data1.drop_duplicates(subset='title',keep='first',inplace=True)
data1=data1.reset_index(drop=True)

x=[]

for i in data1['title']:
    i=re.sub(r'[^a-zA-Z0-9\s]','',i).strip().lower()
    x.append(remove_stopwords(i).split(' '))
#train word2vec model    
model = Word2Vec(x,size=150,min_count=1,iter=20,sg=1,window=5)
#title 2 vec
vec=[]
for i in range(len(x)):
    v=np.zeros(150)
    for j in x[i]:
        v=v+model.wv[j]
    vec.append((v/len(x[i])).tolist())

data2=pd.DataFrame(vec)
#print(np.dot(data2.loc[2],model['ai']))

def current_datetime():
    now = datetime.datetime.now().strftime('%Y/%m/%d')
    c={'date': now}
    return c
#    return render(request, 'index.html', c)


def hello_world(request):
    return HttpResponse("Hello World!")

def welcome(request):
    now=current_datetime()
    #now = datetime.datetime.now().strftime('%Y/%m/%d')
    return render(request,'index.html',now)


def similarity(x):
    cos=[]
    if x in model.wv.vocab:
        v1=np.array(model[x])
        for i in range(len(data2)):
            v2=np.array(data2.loc[i])
            cos.append([data1['title'][i],data1['link'][i],data1['author'][i],data1['date'][i],np.dot(v1,v2),data1['src'][i]])
        cos=pd.DataFrame(cos)
        tnw=cos[cos[5]=='tnw'].sort_values(by=4,ascending=False).head(10)
        bloom=cos[cos[5]=='bloom'].sort_values(by=4,ascending=False).head(10)
    else:
        tnw=[]
        bloom=[]
        print('not found')
        t=data1[data1['src']=='tnw'].reset_index(drop=True)
        b=data1[data1['src']=='bloom'].reset_index(drop=True)
        draw1=np.random.choice([i for i in t.index.tolist()],10,replace=False)
        draw2=np.random.choice([i for i in b.index.tolist()],10,replace=False)
        draw=np.concatenate((draw1,draw2))
        for i in range(20):
            if i<10:
                tnw.append([data1['title'][draw[i]],data1['link'][draw[i]],data1['author'][draw[i]],data1['date'][draw[i]]])
            else:
                bloom.append([data1['title'][draw[i]],data1['link'][draw[i]],data1['author'][draw[i]],data1['date'][draw[i]]])
                
        tnw=pd.DataFrame(tnw)
        bloom=pd.DataFrame(bloom)
    return tnw.reset_index(drop=True),bloom.reset_index(drop=True)

def others(x):
    if x in model.wv.vocab:
        return model.wv.most_similar(x,topn=10)
    else:
        return []
    
def scrape1(request):
    key=request.GET['keyword']
    site=request.GET['site']
    print(site)
    print(key)
    find= similarity(key.lower())
    if site=='TNW':
        result=find[0]
    else:
        result=find[1]

    more=others(key.lower())
   # print(result)
    c=current_datetime()
    c['s']=site    
    c['k']=key
    for i in range(10):
        c['r'+str(i+1)]=result[0][i]
        c['l'+str(i+1)]=result[1][i]
        c['a'+str(i+1)]=result[2][i]
        c['d'+str(i+1)]=result[3][i]
    return render(request, 'try.html', c)
    
#test=similarity('ai')
#print(test)
#for i in range(10):
#    print(test[0][i])
# Create your views here.