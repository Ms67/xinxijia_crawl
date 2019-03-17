from multiprocessing import Process,Queue,Pool,Pipe,Manager
import os,time,random
import json
from multi_province_crawl import crawl_all_pages_data,inser_data_into_db
#写数据进程执行的代码：
def write(p):
    for value in ['A','B','C']:
        print ('Write---Before Put value---Put %s to queue...' % value)
        p.put(value)
        print ('Write---After Put value')
        time.sleep(random.random())
        print ('Write---After sleep')

def get_urls(url_address):
    '''
    {
            "id": "8275270",
            "province": "广西",
            "city": "南宁市",
            "area": "南宁市",
            "year": "2018",
            "mon": "10月",
            "link": "https://gx.zjtcn.com/gov/c128_cs129_d20181005_t_p1.html",
            "iscrawl": "0"
        },
    :param url_address:
    :return:
    '''
    with open(url_address, 'r') as f:

        url_str = f.read()
        url_list = json.loads(url_str)['RECORDS']

    return url_list

def crawl(q_urls,q_data):
    while True:
        if not q_urls.empty():
            url = q_urls.get()
            data = crawl_all_pages_data(url['link'],url["province"],url["city"],url["area"],url["year"],url["mon"])
            # print('把数据放进去%s'%data)
            q_data.put(data)
        else:
            print('url爬取完了')
            break







def save(q_data):
    while True:
        data =q_data.get()
        # print('拿出来了数据 %s'%(data))
        inser_data_into_db(data)


if __name__ == '__main__':
    # #父进程创建Queue，并传给各个子进程：
    # p = Manager().Queue()
    # pw = Process(target=write,args=(p,))
    # pr = Process(target=read,args=(p,))
    # #启动子进程pw，写入：
    # pw.start()
    # #启动子进程pr，读取:
    # pr.start()
    # #等待pw结束：
    # pw.join()
    # #pr进程里是死循环，无法等待其结束，只能强行终止：
    # pr.terminate()
    q_urls=Manager().Queue()
    q_data=Manager().Queue()
    urls = get_urls('url/省会查询_20190117.json')
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

    pr = Process(target=save,args=(q_data,))
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




