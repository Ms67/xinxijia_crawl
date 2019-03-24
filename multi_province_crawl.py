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
    'Connection': 'close',
    'Cookie': 'UM_distinctid=167e506e130555-0de923d4dbe116-6c320a7a-1fa400-167e506e1315fc; lastHost=gd.zjtcn.com; user_uid=dongbujituan; userLoginCookie=0; user_pwd=a88888888; remUser=1; user_name=dongbujituan; cookie_indexScroll=; cookie_indexScroll_date=; Hm_lvt_517073f03fd5acbca941460cde99e5bb=1546183598; GUESSINGHD=2019%2F1%2F2; jsid=6dc14bbe-0713-4086-85fc-911c007531c8; Hm_lvt_a01b74f783ea1eda2c633ceefd483123=1546173259,1546164579,1546378575,1546378765; PHPSESSID=D0B6A9F714ECB67EF896AB87C2A41282; Hm_lpvt_517073f03fd5acbca941460cde99e5bb=1546381059; CNZZDATA1253320430=536837821-1546178601-%7C1546352259; lastHost=gd.zjtcn.com; mainHost=gd.zjtcn.com; Hm_lpvt_a01b74f783ea1eda2c633ceefd483123=1546388400'
}
test_solo_url = 'https://gd.zjtcn.com/materialgov/searchById.json'


def get_url_with_page_list(url, per_page_num=20):
    r = requests.get(url, headers=headers, )
    # print(r.text)
    # pprint(r.headers)
    s = BeautifulSoup(r.text, features="html.parser")
    total_str = s.find(name='font').string
    total_int = int(re.findall(r'\d+', total_str)[0])

    url_witn_page_list = []
    if total_int == 0:
        print('页面 %s 数量为0,' % (url.replace('p1', '', 1)))
        return url_witn_page_list
    page_num = (total_int // per_page_num) + 1
    # print(page_num)
    for i in range(page_num):
        url_witn_page_list.append(url.replace('p1', 'p' + str(i + 1), 1))
    return url_witn_page_list


def cral_one_page_data(url, pro):
    '''
    爬取单个个月份的数据
    :param url: 分页url
    :return: [id name 单位 型号 税率 含税价格 备注 除税价格 ]
    '''

    r = requests.get(url, headers=headers)

    s = BeautifulSoup(r.text, features="html.parser")
    # print(s.prettify())
    eles = s.find_all('tr', {'class': 'table2'})
    # print(eles)
    # print(len(eles))
    data = []  # 多条数据列表,不含[含税价格 除税价格  备注] 只含[id 名称 单位 型号]
    id_data = []  # id列表
    for ele in eles:
        one_piece = []
        ele_id = ele.contents[len(ele.contents) - 2].contents[2]['value']  # id
        ele_name = ele.contents[len(ele.contents) - 2].contents[6]['value']  # 材料名称
        ele_unit = ele.contents[len(ele.contents) - 2].contents[8]['value']  # 材料单位
        ele_spec = ele.contents[len(ele.contents) - 2].contents[10]['value']  # 材料型号
        ele_taxe = ele.contents[11].text  # 税率
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

    params = {'ids': ' '.join(id_data) + ' ',
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
            if i[0] in j:  # id配对
                if j[0]:  # 只存在含税价
                    i.append(j[0])  # 含税价
                    i.append(j[1])  # 备注
                    i.append('')  # 除税价 统一格式添加
                else:  # 存在除税价,可能包含含税价
                    if j[3]:
                        i.append(j[3][1])  # 含税价
                        i.append(j[1])  # 备注
                        i.append(j[3][0])  #
                    else:
                        i.append('')  # 含税价
                        i.append(j[1])  # 备注
                        i.append('')  #

    # pprint(data)

    return data


def crawl_all_pages_data(url, pro, city, area, year, mon):
    '''

    :param url:
    :return: [[id name 单位 型号 税率  含税价格 备注 除税价格 ],...]
    '''
    all_data = []
    try:
        link_list = get_url_with_page_list(url)
        count = 0
        for each_link in link_list:
            one_page_data = cral_one_page_data(each_link, pro)
            all_data += one_page_data
            count += 1
            pprint('正在爬取%s%s%s%s%s第%s页数据' % (pro, city, area, year, mon, count))
    except Exception as e:
        print('爬取%s%s%s%s%s的数据出错了,原因如下' % (pro, city, area, year, mon))
        print(e)
    finally:
        new_data = []
        for i in all_data:
            new_data.append(i + [pro, city, area, year, mon])
        print('爬取%s%s%s%s%s的数据成功,数据量为%s' % (pro, city, area, year, mon, len(new_data)))
        return new_data


def inser_data_into_db(data):
    if data:
        try:

            conn = sqlite3.connect('db/test/xinxijia_test.db')
            cur = conn.cursor()

            # pprint(new_data)
            cur.executemany(
                'insert into 省会城市数据(ori_id,name,unit,xinghao,taxe,pricewithtaxe,note,pricewithoutaxe,province,city,area,year,mon) values (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                (data))

            conn.commit()  # [id name 单位 型号 税率 含税价格 备注 除税价格 ]
            conn.close()
            print(data[0][-5] + data[0][-4] + data[0][-3] + data[0][-2] + data[0][-1] + "数据写入成功 共%s条" % len(data))
        except Exception as e:
            print(data[0][-5] + data[0][-4] + data[0][-3] + data[0][-2] + data[0][-1] + "数据写入失败,原因如下")
            print(e)
            # pprint(data)
    else:
        print(data[0][-5] + data[0][-4] + data[0][-3] + data[0][-2] + data[0][-1] + "数据为空,写入失败")


if __name__ == "__main__":

    url_list201903 = [
        {"province": "陕西", "area": "西安市", "city": "西安市", "link": "https://sx.zjtcn.com/gov/c1_cs_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "陕西", "area": "西安市", "city": "西安市",
         "link": "https://sx.zjtcn.com/gov/c1_cs_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "广东", "area": "广州市", "city": "广州市",
         "link": "https://gd.zjtcn.com/gov/c2_cs3_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "广东", "area": "广州市", "city": "广州市",
         "link": "https://gd.zjtcn.com/gov/c2_cs3_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "广东", "area": "深圳市", "city": "深圳市",
         "link": "https://gd.zjtcn.com/gov/c7_cs8_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "广东", "area": "深圳市", "city": "深圳市",
         "link": "https://gd.zjtcn.com/gov/c7_cs8_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "广西", "area": "南宁市", "city": "南宁市",
         "link": "https://gx.zjtcn.com/gov/c128_cs129_d_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "海南", "area": "海口市", "city": "海口市",
         "link": "https://hainan.zjtcn.com/gov/c1075_cs1076_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "海南", "area": "海口市", "city": "海口市",
         "link": "https://hainan.zjtcn.com/gov/c1075_cs1076_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "湖南", "area": "长沙市", "city": "长沙市",
         "link": "https://hunan.zjtcn.com/gov/c646_cs647_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "海南", "area": "长沙市", "city": "长沙市",
         "link": "https://hunan.zjtcn.com/gov/c646_cs647_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "湖北", "area": "武汉市", "city": "武汉市",
         "link": "https://hubei.zjtcn.com/gov/c548_cs549_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "湖北", "area": "武汉市", "city": "武汉市",
         "link": "https://hubei.zjtcn.com/gov/c548_cs549_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "河南", "area": "郑州市", "city": "郑州市",
         "link": "https://henan.zjtcn.com/gov/c765_cs766_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "河南", "area": "郑州市", "city": "郑州市",
         "link": "https://henan.zjtcn.com/gov/c765_cs766_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "江西", "area": "南昌市", "city": "南昌市",
         "link": "https://jx.zjtcn.com/gov/c2265_cs2266_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "江西", "area": "南昌市", "city": "南昌市",
         "link": "https://jx.zjtcn.com/gov/c2265_cs2266_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "上海", "area": "上海市", "city": "上海市",
         "link": "https://sh.zjtcn.com/gov/c544_cs545_d20190305_t_p1.html",
         "year": "2019", "mon": "03月"},
        {"province": "上海", "area": "上海市", "city": "上海市",
         "link": "https://sh.zjtcn.com/gov/c544_cs545_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "上海", "area": "上海市", "city": "上海市",
         "link": "https://sh.zjtcn.com/gov/c544_cs545_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "浙江", "area": "杭州市", "city": "杭州市",
         "link": "https://zj.zjtcn.com/gov/c1241_cs1242_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "浙江", "area": "杭州市", "city": "杭州市",
         "link": "https://zj.zjtcn.com/gov/c1241_cs1242_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "江苏", "area": "南京市", "city": "南京市",
         "link": "https://js.zjtcn.com/gov/c2370_cs2371_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "江苏", "area": "南京市", "city": "南京市",
         "link": "https://js.zjtcn.com/gov/c2370_cs2371_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "山东", "area": "济南市", "city": "济南市",
         "link": "https://sd.zjtcn.com/gov/c1870_cs1871_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "山东", "area": "济南市", "city": "济南市",
         "link": "https://sd.zjtcn.com/gov/c1870_cs1871_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "安徽", "area": "合肥市", "city": "合肥市",
         "link": "https://ah.zjtcn.com/gov/c2594_cs2595_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "安徽", "area": "合肥市", "city": "合肥市",
         "link": "https://ah.zjtcn.com/gov/c2594_cs2595_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "福建", "area": "福州市", "city": "福州市",
         "link": "https://fj.zjtcn.com/gov/c2511_cs2512_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},
        {"province": "福建", "area": "厦门市", "city": "厦门市",
         "link": "https://fj.zjtcn.com/gov/c2521_cs2522_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "福建", "area": "厦门市", "city": "厦门市",
         "link": "https://fj.zjtcn.com/gov/c2521_cs2522_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "北京", "area": "北京市", "city": "北京市",
         "link": "https://bj.zjtcn.com/gov/c539_cs540_d20190305_t_p1.html",
         "year": "2019", "mon": "03月"},
        {"province": "北京", "area": "北京市", "city": "北京市",
         "link": "https://bj.zjtcn.com/gov/c539_cs540_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "北京", "area": "北京市", "city": "北京市",
         "link": "https://bj.zjtcn.com/gov/c539_cs540_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "天津", "area": "天津市", "city": "天津市",
         "link": "https://tj.zjtcn.com/gov/c125_cs126_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "天津", "area": "天津市", "city": "天津市",
         "link": "https://tj.zjtcn.com/gov/c125_cs126_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "河北", "area": "石家庄市", "city": "石家庄市",
         "link": "https://hebei.zjtcn.com/gov/c911_cs912_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},

        {"province": "山西", "area": "太原市", "city": "太原市",
         "link": "https://shanxi.zjtcn.com/gov/c1996_cs1997_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},

        {"province": "内蒙古", "area": "呼和浩特市", "city": "呼和浩特市",
         "link": "https://nmg.zjtcn.com/gov/c2689_cs2690_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},

        {"province": "辽宁", "area": "沈阳市", "city": "沈阳市",
         "link": "https://ln.zjtcn.com/gov/c2190_cs2191_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "辽宁", "area": "沈阳市", "city": "沈阳市",
         "link": "https://ln.zjtcn.com/gov/c2190_cs2191_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "吉林", "area": "长春市", "city": "长春市",
         "link": "https://jl.zjtcn.com/gov/c2451_cs2452_d20181205_t_p1.html",
         "year": "2018", "mon": "12月"},

        {"province": "黑龙江", "area": "哈尔滨市", "city": "哈尔滨市",
         "link": "https://hlj.zjtcn.com/gov/c431_cs432_d20190305_t_p1.html",
         "year": "2019", "mon": "03月"},
        {"province": "黑龙江", "area": "哈尔滨市", "city": "哈尔滨市",
         "link": "https://hlj.zjtcn.com/gov/c431_cs432_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "黑龙江", "area": "哈尔滨市", "city": "哈尔滨市",
         "link": "https://hlj.zjtcn.com/gov/c431_cs432_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "四川", "area": "成都市", "city": "成都市",
         "link": "https://sc.zjtcn.com/gov/c237_cs238_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "重庆", "area": "重庆市", "city": "重庆市",
         "link": "https://cq.zjtcn.com/gov/c1198_cs1199_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},
        {"province": "重庆", "area": "重庆市", "city": "重庆市",
         "link": "https://cq.zjtcn.com/gov/c1198_cs1199_d20190105_t_p1.html",
         "year": "2019", "mon": "01月"},

        {"province": "云南", "area": "昆明市", "city": "昆明市",
         "link": "https://yn.zjtcn.com/gov/c1325_cs1326_d20190305_t_p1.html",
         "year": "2019", "mon": "03月"},
        {"province": "云南", "area": "昆明市", "city": "昆明市",
         "link": "https://yn.zjtcn.com/gov/c1325_cs1326_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},

        {"province": "西藏", "area": "拉萨市", "city": "拉萨市",
         "link": "https://xz.zjtcn.com/gov/c1583_cs1584_d20181205_t_p1.html",
         "year": "2018", "mon": "12月"},

        {"province": "甘肃", "area": "兰州市", "city": "兰州市",
         "link": "https://gs.zjtcn.com/gov/c1771_cs1772_d20181205_t_p1.html",
         "year": "2018", "mon": "12月"},

        {"province": "宁夏", "area": "银川市", "city": "银川市",
         "link": "https://nx.zjtcn.com/gov/c2161_cs2162_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},

        {"province": "青海", "area": "西宁市", "city": "西宁市",
         "link": "https://qh.zjtcn.com/gov/c2105_cs2106_d20190205_t_p1.html",
         "year": "2019", "mon": "02月"},

        {"province": "新疆", "area": "乌鲁木齐市", "city": "乌鲁木齐市",
         "link": "https://xj.zjtcn.com/gov/c1476_cs1477_d20190105_t_p1.html",
         "year": "2019", "mon": "02月"},
    ]
    for i in url_list201903:
        data = crawl_all_pages_data(i['link'], i['province'], i['area'], i['city'], i['year'],
                                    i['mon'])
        inser_data_into_db(data)

