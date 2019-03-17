#coding:utf-8
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
import requests,json
from pprint import pprint
from multi_province_crawl import crawl_all_pages_data,inser_data_into_db

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

def crawl_and_save_data(url):
    data = crawl_all_pages_data(url['link'],url["province"],url["city"],url["area"],url["year"],url["mon"])
    inser_data_into_db(data,url["province"],url["city"],url["area"],url["year"],url["mon"])






if __name__ == "__main__":
    # startUrl = 'http://tj.fang.anjuke.com/?from=navigation'
    # web_data = requests.get(startUrl)
    # soup = BeautifulSoup(web_data.text, 'lxml')
    # urls = [url.get('href') for url in soup.select('.city-mod > dl > dd > a')]
    # main(urls)
    # get_urls()
    # main()
    # print(multiprocessing.cpu_count())
    # get_urls('url/省会查询_20190117.json')
    # urls=get_urls('url/省会查询_20190117.json')
    # pprint(urls)
  #   url = {'area': '深圳市',
  # 'city': '深圳市',
  # 'id': '8373996',
  # 'iscrawl': '0',
  # 'link': 'https://gd.zjtcn.com/gov/c7_cs8_d20180805_t_p1.html',
  # 'mon': '08月',
  # 'province': '广东',
  # 'year': '2018'}
  #   crawl_and_save_data(url)

    '''
    '''

    pool = Pool(30)
    urls = get_urls('url/省会查询_20190117.json')
    pool.map(crawl_and_save_data,urls)
    # pool.map(detailPage, urls)
    pool.close()
    pool.join()


