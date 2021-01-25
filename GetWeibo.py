import urllib.request
import json
from pyquery import PyQuery as pq
import requests
from bs4 import BeautifulSoup
import re
import random
import time

def get_cookie(cookiestr):
  cookies = {}
  lines = cookiestr.split(';')
  for line in lines:
    key, value = line.strip().split('=', 1)
    cookies[key] = value
  return cookies
head = {
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',  # 通过ajax请求形式获取数据
    'X-XSRF-TOKEN': '7d7f53',
    'Accept': 'application/json, text/plain, */*'
}
cookiestr='H5_wentry=H5; backURL=https%3A%2F%2Fweibo.cn%2F; ALF=1613736931; SCF=AlveqEow4T3t1BworTzp8S4VdHvJng0H-cfz2c74CYEva6KUa2WB2nsq5kz4m6j4sWIQzfQ90ksSx_TkyKOx_RY.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWAh8knlA_qax648O5rFk4o5NHD95QfSoqpeK2XSK-XWs4DqcjZBc8_M24fdX9hBntt; SSOLoginState=1611160780; WEIBOCN_FROM=1110006030; loginScene=102003; SUB=_2A25NDBTqDeRhGeNI7VMQ8SrJzjiIHXVuDryirDV6PUJbkdAfLUrbkW1NSFkOtYOwE2g8GO4-8q4aVOyv_R9pr7Lk; _T_WM=67540108154; XSRF-TOKEN=7d7f53; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D231093_-_selffollowed%26fid%3D1005052803301701%26uicode%3D10000011'
cookie_m=get_cookie(cookiestr)

#爬取用户的id
id='2803301701'


def get_othercomment(url,id,comments):
  print("get others!!!")
  formaturl = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0"
  try:
    response = requests.get(url, headers=head, cookies=cookie_m)
    data = json.loads(response.text)
    content = data.get('data')
    datas = content.get('data')
    for i in range(0, len(datas)):
      comments.append(pq(datas[i].get('text')).text().replace('<span class=\"Text\".*?>.*?</span>', ''))
    maxid = data['data'].get('max_id')
    nexturl = formaturl.format(id, id, maxid)
    print(nexturl)
    get_othercomment(nexturl,id,comments)
  except Exception as e:
    print(e)
    pass
  return comments
#获取微博主页的containerid，爬取微博内容时需要此id
def get_containerid(url):
  response = requests.get(url, headers=head, cookies=cookie_m)
  data = json.loads(response.text)
  #content=json.loads(data).get('data')
  content = data.get('data')
  print(content)
  tabs=content.get('tabsInfo').get('tabs')
  for data in tabs:
    if(data.get('tab_type')=='weibo'):
      containerid=data.get('containerid')
  return containerid
#获取微博大V账号的用户基本信息，如：微博昵称、微博地址、微博头像、关注人数、粉丝数、性别、等级等
def get_userInfo(id):
  url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
  response = requests.get(url, headers=head, cookies=cookie_m)
  data = json.loads(response.text)
  print()
  #data=use_proxy(url,proxy_addr)
  content=data.get('data')
  print(content)
  profile_image_url=content.get('userInfo').get('profile_image_url')
  description=content.get('userInfo').get('description')
  profile_url=content.get('userInfo').get('profile_url')
  verified=content.get('userInfo').get('verified')
  guanzhu=content.get('userInfo').get('follow_count')
  name=content.get('userInfo').get('screen_name')
  fensi=content.get('userInfo').get('followers_count')
  gender=content.get('userInfo').get('gender')
  urank=content.get('userInfo').get('urank')
  print("微博昵称："+name+"\n"+"微博主页地址："+profile_url+"\n"+"微博头像地址："+profile_image_url+"\n"+"是否认证："+str(verified)+"\n"+"微博说明："+description+"\n"+"关注人数："+str(guanzhu)+"\n"+"粉丝数："+str(fensi)+"\n"+"性别："+gender+"\n"+"微博等级："+str(urank)+"\n")
#获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等
def get_weibo(id,file):
  List = []
  i=1000
  while True:
    time.sleep(random.random() * 4)
    url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
    weibo_url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id+'&containerid='+get_containerid(url)+'&page='+str(i)
    try:
      response = requests.get(weibo_url, headers=head, cookies=cookie_m)
      data = json.loads(response.text)
      print(data)
      content=data.get('data')
      cards=content.get('cards')
      print(cards)
      print('---------------------')
      print('999')
      print(len(cards))
      if(len(cards)==0):
        continue
      if(len(cards)>0):
        for j in range(len(cards)):
          print("-----正在爬取第"+str(i)+"页，第"+str(j)+"条微博------")
          card_type=cards[j].get('card_type')
          if(card_type==9):
            mblog=cards[j].get('mblog')
            attitudes_count=mblog.get('attitudes_count')
            comments_count=mblog.get('comments_count')
            created_at=mblog.get('created_at')
            print(created_at)
            reposts_count=mblog.get('reposts_count')
            scheme=cards[j].get('scheme')
            ids=mblog.get('id')
            # text=pq(mblog.get('text')).text().replace('\n','')
            dic = {}
            dic = {
                '微博地址:': scheme,
                 '发布时间:': created_at,
                '微博内容:': get_detail(ids),
                '点赞数:': attitudes_count,
                '评论数': comments_count,
                '转发数': reposts_count,
                '评论':get_comment(ids)
            }
            List.append(dic)
            with open(file,'w',encoding='utf-8') as fh:
              fh.write(json.dumps(List, indent=2, ensure_ascii=False))
        i+=1
      else:
        break
    except Exception as e:
      print(e)
      pass

def get_comment(id):
  comments = []
  try:
    url='https://m.weibo.cn/comments/hotflow?id='+id+'&mid='+id+'&max_id_type=0'
    formaturl = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0"
    response = requests.get(url, headers=head, cookies=cookie_m)
    data = json.loads(response.text)
    content=data.get('data')
    datas = content.get('data')
    for i in range(0,len(datas)):
      comments.append(pq(datas[i].get('text')).text().replace('<span class=\"Text\".*?>.*?</span>',''))
    #获得后续的评论url
    '''
    maxid = data['data'].get('max_id')
    nexturl = formaturl.format(id, id, maxid)
    get_othercomment(nexturl,id,comments)
    '''
  except Exception as e:
    print(e)
    pass
  return comments


def get_detail(id):
  try:
    url='https://m.weibo.cn/statuses/extend?id='+id
    response = requests.get(url, headers=head, cookies=cookie_m)
    data = json.loads(response.text)
    content=data.get('data')
    longTextContent = content.get('longTextContent')
    text=pq(longTextContent).text().replace('\n','')
  except Exception as e:
    print(e)
    pass
  return text

if __name__=="__main__":
  file=id+"new10"+".json"
  get_userInfo(id)
  get_weibo(id,file)