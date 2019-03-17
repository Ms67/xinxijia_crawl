'''
爬取页面数据并存入数据库,数据库位于db文件夹中,一个省份一个数据库
'''
import sqlite3

import requests
import re
from bs4 import BeautifulSoup
import datetime
import json
from pprint import pprint

test_url = 'https://gd.zjtcn.com/gov/c2_cs3_d20181105_t_p1.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection': 'keep-alive',
    'Cookie':'UM_distinctid=167e506e130555-0de923d4dbe116-6c320a7a-1fa400-167e506e1315fc; lastHost=gd.zjtcn.com; user_uid=dongbujituan; userLoginCookie=0; user_pwd=a88888888; remUser=1; user_name=dongbujituan; cookie_indexScroll=; cookie_indexScroll_date=; Hm_lvt_517073f03fd5acbca941460cde99e5bb=1546183598; GUESSINGHD=2019%2F1%2F2; jsid=6dc14bbe-0713-4086-85fc-911c007531c8; Hm_lvt_a01b74f783ea1eda2c633ceefd483123=1546173259,1546164579,1546378575,1546378765; PHPSESSID=D0B6A9F714ECB67EF896AB87C2A41282; Hm_lpvt_517073f03fd5acbca941460cde99e5bb=1546381059; CNZZDATA1253320430=536837821-1546178601-%7C1546352259; lastHost=gd.zjtcn.com; mainHost=gd.zjtcn.com; Hm_lpvt_a01b74f783ea1eda2c633ceefd483123=1546388400'
}
test_solo_url ='https://gd.zjtcn.com/materialgov/searchById.json'



def get_url_with_page_list(url,per_page_num=20):
    r = requests.get(url,headers=headers,)
    # print(r.text)
    # pprint(r.headers)
    s = BeautifulSoup(r.text,features="html.parser")
    total_str = s.find(name='font').string
    total_int = int(re.findall(r'\d+', total_str)[0])

    url_witn_page_list = []
    if total_int == 0:
        print('页面 %s 数量为0,'%(url.replace('p1','',1)))
        return  url_witn_page_list
    page_num = (total_int // per_page_num) +1
    # print(page_num)
    for i in range(page_num):
        url_witn_page_list.append(url.replace('p1','p'+str(i+1),1))
    return url_witn_page_list


def cral_one_page_data(url,pro):
    '''
    爬取单个个月份的数据
    :param url: 分页url
    :return: [id name 单位 型号 税率 含税价格 备注 除税价格 ]
    '''

    r = requests.get(url, headers=headers)

    s = BeautifulSoup(r.text,features="html.parser")
    # print(s.prettify())
    eles = s.find_all('tr',{'class':'table2'})
    # print(eles)
    # print(len(eles))
    data = []      #多条数据列表,不含[含税价格 除税价格  备注] 只含[id 名称 单位 型号]
    id_data = []   #id列表
    for ele in eles:

        one_piece=[]
        ele_id=ele.contents[len(ele.contents)-2].contents[2]['value']     #id
        ele_name=ele.contents[len(ele.contents)-2].contents[6]['value']     #材料名称
        ele_unit=ele.contents[len(ele.contents)-2].contents[8]['value']     #材料单位
        ele_spec=ele.contents[len(ele.contents)-2].contents[10]['value']     #材料型号
        ele_taxe=ele.contents[11].text                                     #税率
        # print(ele_taxe)
        # print(ele_taxe)#材料型号
        # for k,v in enumerate(ele.contents):
        #     print("$$$$$$$$$$")
        #     print(k)
        #     print(v)
        #     print("$$$$$$$$$$")
        one_piece.append(ele_id)
        one_piece.append(ele_name)
        one_piece.append(ele_unit)
        one_piece.append(ele_spec)
        one_piece.append(ele_taxe)

        # print(type(ele_id))
        # print(type(ele_name))
        # print(type(ele_unit))
        # print(type(ele_spec))
        # print(type(ele_taxe))

        data.append(one_piece)
        id_data.append(ele_id)
    # pprint(data)
    # print('______________')
    # pprint(id_data)

    params = {'ids': ' '.join(id_data)+' ',
                 'province': pro,
                 'industryId': '1',
                 'industryName': '建筑工程'
                 }

    r_json = requests.get(test_solo_url, headers=headers, params=params)
    data2 = r_json.json()['results']['data']
    # pprint(data2)
    final_data = []
    for i in data:
        for j in data2:
            if i[0] in j: #id配对
                if j[0]: #只存在含税价
                    i.append(j[0]) #含税价
                    i.append(j[1]) #备注
                    i.append('')   #除税价 统一格式添加
                else: #存在除税价,可能包含含税价
                    if j[3]:
                        i.append(j[3][1]) #含税价
                        i.append(j[1])    #备注
                        i.append(j[3][0]) #
                    else:
                        i.append('')  # 含税价
                        i.append(j[1])  # 备注
                        i.append('')  #




    # pprint(data)

    return data


def crawl_all_pages_data(url,pro,city,area,year,mon):
    '''

    :param url:
    :return: [[id name 单位 型号 税率 含税价格 备注 除税价格 ],...]
    '''
    all_data = []
    try:
        link_list = get_url_with_page_list(url)
        count = 0
        for each_link in link_list:
            one_page_data = cral_one_page_data(each_link,pro)
            all_data += one_page_data
            count +=1
            pprint('正在爬取%s%s%s%s%s第%s页数据'%(pro,city,area,year,mon,count))
    except Exception as e:
        print('爬取%s%s%s%s%s的数据出错了'%(pro,city,area,year,mon))
        print(e)
    finally:
        return all_data

def creat_db_and_table():
    conn = sqlite3.connect('db/test/xinxijia_test.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE guangdong
             (id INTEGER primary key autoincrement ,
              city text,
              area text,
              year text,
              mon text,
              ori_id text,
              name text,
              unit text,
              xinghao text,
              taxe text,
              pricewithtaxe text,
              note text ,
              pricewithoutaxe text
              )''')

    conn.commit()
    conn.close()
    print('done')

def inser_data_into_db(data,city,area,year,mon):
    if data:
        try:
            conn = sqlite3.connect('db/test/xinxijia_test.db')
            cur = conn.cursor()
            for i in data:
                cur.execute(
                    'insert into guangdong (city,area,year,mon,ori_id,name,unit,xinghao,taxe,pricewithtaxe,note,pricewithoutaxe) values (?,?,?,?,?,?,?,?,?,?,?,?)',
                                     (city, area,  year, mon, i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))
            conn.commit()         #[id name 单位 型号 税率 含税价格 备注 除税价格 ]
            conn.close()
            print(city+area+year+mon+"数据写入成功 共%s条"%len(data))
        except Exception as e:
            print(city+area+year+mon+"数据写入成功,原因如下:")
            print(e)
    else:
        print(city+area+year+mon+"数据为空,写入失败")

def crawl_one_province_data_and_save(json_path_str,province):
    pass

if __name__ == "__main__":

    # with open('url/url_data.json','r') as f:
    #     d=json.loads(f.readline())
    #     for each_city, many_areas in d.items():
    #         for each_area, many_years in many_areas.items():
    #             for each_year, many_mons in many_years.items():
    #                 for each_mon, each_link in many_mons.items():
    #                     data = crawl_all_pages_data(each_link,'广东',each_city,each_area,each_year,each_mon)
    #                     inser_data_into_db(data,each_city,each_area,each_year,each_mon)
    # data = cral_one_page_data('https://gd.zjtcn.com/gov/c57_cs58_d20090105_t_p1.html', '广东', )
    data = crawl_all_pages_data('https://gd.zjtcn.com/gov/c7_cs8_d20181205_t_p1.html','广东',city='深圳市',area='深圳市',year='2018',mon='12')
    # pprint(data)
    # # creat_db_and_table()
    inser_data_into_db(data,city='深圳市',area='深圳市',year='2018',mon='11')