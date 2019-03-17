'''
将json格式的url数据存进sqlite,方便分类读取
'''
import json
from get_urls_faster import base_url
from pprint import pprint
import sqlite3


def get_url_list(province):
    with open('url/%s.json' % province, 'r') as f:
        url_list = []
        d = json.loads(f.readline())
        for each_city, many_areas in d.items():
            for each_area, many_years in many_areas.items():
                for each_year, many_mons in many_years.items():
                    for each_mon, each_link in many_mons.items():
                        url_list.append([province, each_city, each_area, each_year, each_mon, each_link])
        return url_list


def save(data):
    if data:
        try:
            conn = sqlite3.connect('db/test/xinxijia_test.db')
            cur = conn.cursor()
            cur.executemany(
                'insert into urls (province,city,area,year,mon,link) values (?,?,?,?,?,?)',
                (data))
            conn.commit()  # [id name 单位 型号 税率 含税价格 备注 除税价格 ]
            conn.close()
            print("数据写入成功 共%s条" % len(data))
        except Exception as e:
            print("数据写入失败,原因如下:")
            print(e)
    else:
        print("数据为空,写入失败")


if __name__ == '__main__':
    pprint(base_url.keys())
    for province in base_url.keys():
        print(province)
        url_list = get_url_list(province)
        print(len(url_list))
        save(url_list)

    # url_list = get_url_list('广西')
    # pprint(url_list)
    # print(len(url_list))
    # save(url_list)

