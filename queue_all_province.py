from multiprocessing import Process, Queue, Pool, Pipe, Manager
import os, time, random
import json
from multi_province_crawl import crawl_all_pages_data
import sqlite3
from pprint import pprint

def inser_data_into_db(data,sql_table_name):
    if data:
        try:

            conn = sqlite3.connect('db/test/xinxijia_test.db')
            cur = conn.cursor()

            # pprint(new_data)
            cur.executemany(
                'insert into %s (ori_id,name,unit,xinghao,taxe,pricewithtaxe,note,pricewithoutaxe,province,city,area,year,mon) values (?,?,?,?,?,?,?,?,?,?,?,?,?)'%sql_table_name,
                (data))

            conn.commit()         #[id name 单位 型号 税率 含税价格 备注 除税价格 ]
            conn.close()
            print(data[0][-5]+data[0][-4]+data[0][-3]+data[0][-2]+data[0][-1]+"数据写入成功 共%s条"%len(data))
        except Exception as e:
            print(data[0][-5]+data[0][-4]+data[0][-3]+data[0][-2]+data[0][-1]+"数据写入失败,原因如下")
            print(e)
            # pprint(data)
    else:
        print(data[0][-5]+data[0][-4]+data[0][-3]+data[0][-2]+data[0][-1]+"数据为空,写入失败")




def get_urls(province):
    urls = []
    conn = sqlite3.connect('db/test/xinxijia_test.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM urls WHERE province='%s' " % province)
    result = cur.fetchall()
    conn.close()
    for i in result:
        urls.append({
            "province": i[1],
            "city": i[2],
            "area": i[3],
            "year": i[4],
            "mon": i[5],
            "link": i[6],

        })
    # pprint(urls)
    return urls


def crawl(q_urls, q_data):
    while True:
        if not q_urls.empty():
            url = q_urls.get()
            data = crawl_all_pages_data(url['link'], url["province"], url["city"], url["area"], url["year"], url["mon"])
            # print('把数据放进去%s'%data)
            q_data.put(data)
        else:
            print('url爬取完了')
            break


def save(q_data,sql_table_name):
    while True:
        data = q_data.get()
        # print('拿出来了数据 %s'%(data))
        inser_data_into_db(data,sql_table_name)


if __name__ == '__main__':
    # get_urls('广东')

    q_urls=Manager().Queue()
    q_data=Manager().Queue()
    urls = get_urls('广西')
    for i in urls:
        q_urls.put(i)

    pw1 = Process(target=crawl,args=(q_urls,q_data))
    pw2 = Process(target=crawl,args=(q_urls,q_data))
    pw3 = Process(target=crawl,args=(q_urls,q_data))
    pw4 = Process(target=crawl,args=(q_urls,q_data))
    pw5 = Process(target=crawl,args=(q_urls,q_data))
    pw6 = Process(target=crawl,args=(q_urls,q_data))
    pw7 = Process(target=crawl,args=(q_urls,q_data))
    pw8 = Process(target=crawl,args=(q_urls,q_data))
    pw9 = Process(target=crawl,args=(q_urls,q_data))
    pw10 = Process(target=crawl,args=(q_urls,q_data))
    pw11 = Process(target=crawl,args=(q_urls,q_data))
    pw12 = Process(target=crawl,args=(q_urls,q_data))
    pw13 = Process(target=crawl,args=(q_urls,q_data))
    pw14 = Process(target=crawl,args=(q_urls,q_data))
    pw15 = Process(target=crawl,args=(q_urls,q_data))
    pw16 = Process(target=crawl,args=(q_urls,q_data))
    pw17 = Process(target=crawl,args=(q_urls,q_data))
    pw18 = Process(target=crawl,args=(q_urls,q_data))
    pw19 = Process(target=crawl,args=(q_urls,q_data))
    pw20 = Process(target=crawl,args=(q_urls,q_data))

    pr = Process(target=save,args=(q_data,'广西全'))
    #启动子进程pw，写入：
    pw1.start()
    pw2.start()
    pw3.start()
    pw4.start()
    pw5.start()
    pw6.start()
    pw7.start()
    pw8.start()
    pw9.start()
    pw10.start()
    pw11.start()
    pw12.start()
    pw13.start()
    pw14.start()
    pw15.start()
    pw16.start()
    pw17.start()
    pw18.start()
    pw19.start()
    pw20.start()


    #启动子进程pr，读取:
    pr.start()
    #等待pw结束：
    pw1.join()
    pw2.join()
    pw3.join()
    pw4.join()
    pw5.join()
    pw6.join()
    pw7.join()
    pw8.join()
    pw9.join()
    pw10.join()
    pw11.join()
    pw12.join()
    pw13.join()
    pw14.join()
    pw15.join()
    pw16.join()
    pw17.join()
    pw18.join()
    pw19.join()
    pw20.join()

    pr.join()
