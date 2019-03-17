from selenium import webdriver
from xinxi import test_url,cookie_f,cookie
import time
import pprint
import re

base_url='https://gx.zjtcn.com/gov/c_cs_d_t_p1.html' #都带p1的初始url

industry_list=[]
province_list=[]
district_list=[]
year_list=[]
mon_list=[]

def get_total_page_num(base_url):

    driver = webdriver.Chrome('venv/chromedriver')
    driver.get(base_url)
    total_str = driver.find_element_by_tag_name('font').text

    # print(total_str)
    total_num = int(re.findall("\d+",total_str)[0])
    driver.close()
    print('当前页总条数为%s'%(total_num))
    return total_num



def get_url_list_with_page_num(base_url,per_page_num=20):
    url_witn_page_list = []
    total_num = get_total_page_num(base_url)
    if total_num == 0:
        print('页面 %s 数据量为0,停止爬取'%(base_url))
        return  url_witn_page_list
    page_num = (total_num // per_page_num) +1
    # print(page_num)
    for i in range(page_num):
        url_witn_page_list.append(base_url.replace('p1','p'+str(i+1),1))
    print('页面%s总页数%s' % (base_url,len(url_witn_page_list)))
    return url_witn_page_list





if __name__ == "__main__":
    url_witn_page_list = get_url_list_with_page_num(base_url)
    print(url_witn_page_list)

