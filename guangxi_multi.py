#coding:utf-8
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
import requests,json
from pprint import pprint
from danxiancheng_crawl import crawl_all_pages_data,inser_data_into_db

def get_urls(province):
    with open('url/guangxi_url_data.json','r') as f:
        urls = []
        d = json.loads(f.readline())
        for each_city, many_areas in d.items():
            for each_area, many_years in many_areas.items():
                for each_year, many_mons in many_years.items():
                    for each_mon, each_link in many_mons.items():
                        urls.append([province,each_city,each_area,each_year,each_mon,each_link])

    # pprint(urls)
    return urls

def crawl_and_save_data(url):
    data = crawl_all_pages_data(url[5],url[0],url[1],url[2],url[3],url[4])
    inser_data_into_db(data,url[0],url[1],url[2],url[3],url[4])

def main():
    pool = Pool(150)
    urls = get_urls('广西')
    pool.map(crawl_and_save_data,urls)
    # pool.map(detailPage, urls)
    pool.close()
    pool.join()





if __name__ == "__main__":
    # startUrl = 'http://tj.fang.anjuke.com/?from=navigation'
    # web_data = requests.get(startUrl)
    # soup = BeautifulSoup(web_data.text, 'lxml')
    # urls = [url.get('href') for url in soup.select('.city-mod > dl > dd > a')]
    # main(urls)
    # get_urls()
    main()
    # print(multiprocessing.cpu_count())



