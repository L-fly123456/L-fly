import requests
from pyquery import PyQuery as pq
import csv
from threading import Thread,Lock
import time
import os

def get_one_url(url):

    try:
        headers={
            'Referer':'https: // s1.ljcdn.com / matrix_pc / dist / pc / src / common / css / common.css?_v = 20191213202326259',
            'User - Agent':'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 76.0.3809.132Safari / 537.36',

        }
        # 获取响应
        response=requests.get(url,headers,proxies=None)
        # 判断请求状态
        if response.status_code==200:
            return response.text
        return None
    except requests.exceptions.ConnectionError as e:
        print('error',e.args)

def parse_one_url(html):
    doc=pq(html)
    items=doc('.content__list--item--main').items()
    for item in items:
        # 上锁,等待每个线程的解析执行完之后在执行其他线程
        mutes.acquire()
        info= {
            'content': item.find('a').text().split()[0],
            'room': item.find('a').text().split()[1],
            'direction': item.find('a').text().split()[2],
            'size':item.find('p.content__list--item--des').text().split('/')[1],
            'price':item.find('.content__list--item-price').text(),
            'location':item.find('.content__list--item--des a').text().replace(' ','-')
        }
        # 释放互斥锁
        mutes.release()
        print(info)
        # 生成器，使循环结束之后再返回
        yield info

# 创建互斥锁
mutes = Lock()

def man(page,city):
    url = 'https://sz.lianjia.com/zufang/%s/pg%d/#contentList'%(city,page)
    html = get_one_url(url)
    infos=parse_one_url(html)
    save(infos,city)


def save(infos,city):
    '''
    判断文件是否存在，如果存在就说明表头已经写了就不写表头，反之加上表头
    :param infos: 保存的信息
    :return:
    '''
    if os.path.exists('%s.csv' %(city)):
        with open('链家租房.csv', 'a', encoding='utf-8') as csvfile:
            fieldname = ['content', 'room', 'direction', 'size', 'location', 'price']
            writer = csv.DictWriter(csvfile, fieldname)
            for info in infos:
                writer.writerow(info)
    else:
        with open('%s.csv' %(city),'a',encoding='utf-8') as csvfile:
            fieldname=['content','room','direction','size','location','price']
            writer = csv.DictWriter(csvfile,fieldname) #DictWriter方法使csv文件可以写入字典
            writer.writeheader()
            for info in infos:
                writer.writerow(info)


if __name__=='__main__':
    cities = ['luohuqu', 'longhuaqu', 'futianqu']
    # 循环深圳各区的缩写
    for city in cities:
        ts =[]
        # 创建多个线程分页爬取，使爬虫效率大大提高
        for i in range(1,50):
            exec('t{0} = Thread(target=man,args=(i,city))'.format(i))
            exec('ts.append(t{0})'.format(i))
        for t in ts:
            t.start()
        # 等待所有线程全部执行结束
        time.sleep(4)
        print('%s租房信息存入成功' %(city))
    print('全部存入成功')

