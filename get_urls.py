# 获取分级菜单url字典模块
from selenium import webdriver
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import json
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection': 'keep-alive'
}


base_url = 'https://gx.zjtcn.com'

enter_url = base_url + '/gov/c_cs_d_t_p1.html' #建筑工程进入参数

'''    
最终想要获取的全部城市url数据格式 
{
    '广州市': {
        '广州市': {
            '2018': {
                '11': 'https://gd.zjtcn.com/gov/c2_cs3_d20181105_t_p1.html',
                '10': 'https://gd.zjtcn.com/gov/c2_cs3_d20181005_t_p1.html',
                ...
            },
            ...  
        },
        ...
    },
    ...
}
'''

def get_mon(each_year, each_year_link,each_area,each_city,provin):
    '''

    :param each_year: '2018'
    :param each_year_link: 'https://gd.zjtcn.com/gov/c17_cs122_d20181105_t_p1.html'
    :param each_area: '花都区'
    :param each_city:'广州市'
    :param provin:'广东省'
    :return:{
                '11': 'https://gd.zjtcn.com/gov/c2_cs3_d20181105_t_p1.html',
                '10': 'https://gd.zjtcn.com/gov/c2_cs3_d20181005_t_p1.html',
                ...
            }
    '''
    mon = {}


    print('开始爬取%s%s%s%s的月份数据' % (provin, each_city, each_area,each_year))  # 开始爬取广东省广州市花都区2018的年份数据
    driver = webdriver.Chrome('venv/chromedriver')
    try:
        # from selenium.webdriver.chrome.options import Options
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")  # define headless



        driver.get(each_year_link)
        # print(driver.page_source)
        ele_mon = driver.find_element_by_id('filter_month')  # 月份节点
        ele_mon_list = ele_mon.find_elements_by_xpath(".//a")
        # 广东省广州市花都区的2018年份节点数量为10个
        print('%s%s%s%s年月份数量为%s' % (provin, each_city, each_area,each_year,len(ele_mon_list)))
        # # # 拼凑字典
        for i in ele_mon_list:
            mon[i.text] = i.get_attribute("href") # 奇怪 这里明明只有半个url,为什么添加进去就全了?
            # print(i.get_attribute("href"))
            # print(i.get_attribute("tip"))
        # pprint(mon)
        print(list(mon.keys()))
    except Exception as e:
        print('%s%s%s%s%s'%(each_year, each_year_link,each_area,each_city,provin))
        print(e)

    finally:
        driver.close()
        # print(mon)
        return mon



def get_year(each_area, each_area_lick,each_city,provin):
    '''
    爬取年份节点数据
    :param each_area: '花都区'
    :param each_area_lick: 'https://gd.zjtcn.com/gov/c2_cs6_d_t_p1.html'
    :param each_city: '广州市'
    :param provin: '广东省'
    :return: {'2018年':"https://gd.zjtcn.com/gov/c2_cs3_d_t_p1.html",
            ...
            }
    '''




    print('开始爬取%s%s%s的年份数据'%(provin,each_city,each_area))  #开始爬取广东省广州市花都区的年份数据
    year = {}

    # from selenium.webdriver.chrome.options import Options
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # define headless

    driver = webdriver.Chrome('venv/chromedriver')
    driver.get(each_area_lick)
    # print(driver.page_source)
    ele_year = driver.find_element_by_id('filter_year')  # 时间节点
    ele_year_list = ele_year.find_elements_by_xpath(".//a")
    # 广东省广州市花都区的的年份节点数量为10个
    print('%s%s%s的年份数量为%s' % (provin, each_city, each_area,len(ele_year_list))) #广东省广州市花都区的年份数量为
    # # # 拼凑字典
    for i in ele_year_list:
        year[i.get_attribute("tip")] =  i.get_attribute("href")
        # print(i.get_attribute("href"))
        # print(i.get_attribute("tip"))
    # pprint(year)
    print(list(year.keys()))
    for each_year, each_year_link in year.items():
        mon = get_mon(each_year, each_year_link,each_area,each_city,provin)
        year[each_year] = mon

    driver.close()

    return year

def get_area(each_city,each_city_lick,provin):
    '''
    爬取区域数据
    :param each_city:'广州市'
    :param each_city_lick:'https://gd.zjtcn.com/gov/c2_cs_d_t_p1.html'
    :param provin:'广东省'
    :return:

    {
        '广州市': 'https://gd.zjtcn.com/gov/c2_cs3_d_t_p1.html',
        '花都市: 'https://gd.zjtcn.com/gov/c2_cs6_d_t_p1.html',
        ...
    },
    '''
    print('开始爬取%s%s的区域数据'%(provin,each_city)) #开始爬取广东省广州市的区域数据
    area = {}

    # from selenium.webdriver.chrome.options import Options
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # define headless

    driver = webdriver.Chrome('venv/chromedriver')
    driver.get(each_city_lick)
    # print(driver.page_source)
    ele_area = driver.find_element_by_id('country_ul')  # 区域节点
    ele_area_list = ele_area.find_elements_by_xpath(".//a")
    print('%s%s的区域数量为%s' % (provin,each_city,len(ele_area_list)))  #广东省广州市的区域节点数量为
    # # 拼凑字典
    for i in ele_area_list:
        area[i.text] = base_url + i.get_attribute("role")
        # print(i.get_attribute("role"))
        # print(i.text)
    # print(area)
    print(list(area.keys()))

    for each_area, each_area_lick in area.items():
        year = get_year(each_area, each_area_lick,each_city,provin)
        area[each_area] = year

    driver.close()
    return area



def get_city(enter_url,provin):
    '''
    爬取城市数据
    :param enter_url: base_url + '/gov/c_cs_d_t_p1.html'
    :param provin: '广东省'
    :return: {
                '广州市':https://gd.zjtcn.com/gov/c2_cs3_d_t_p1.html",
                ...
            }
    '''
    print('开始爬取%s省的城市数据'%provin) #开始爬取广东省的城市节点数据
    city = {}

    # from selenium.webdriver.chrome.options import Options
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # define headless

    driver = webdriver.Chrome('venv/chromedriver')
    driver.get(enter_url)
    # print(driver.page_source)
    ele_city = driver.find_element_by_id('areaUl') #城市节点
    ele_city_list = ele_city.find_elements_by_xpath(".//a")

    #拼凑字典
    for i in ele_city_list:
        city[i.text] = base_url + i.get_attribute("role")
        # print(i.get_attribute("role"))
        # print(i.text)
    # print(city)
    print('%s省的城市数量为%s '%(provin,len(ele_city_list))) #广东省的城市数量为
    print(list(city.keys()))

    # 遍历字典,讲字典值修改为下架菜单返回的字典
    for each_city,each_city_lick in city.items():
        area = get_area(each_city,each_city_lick,provin)
        city[each_city] = area

    # pprint(city)
    driver.close()
    return city

def get_urls_json(url,province):
    city = get_city(url, 'province')
    city_str = json.dumps(city, ensure_ascii=False)
    with open('url/%s.json'%province, 'w') as f:
        f.write(city_str)


if __name__ == '__main__':
    get_urls_json('https://gx.zjtcn.com/gov/c_cs_d_t_p1.html', '广西')

