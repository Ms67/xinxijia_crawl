from selenium import webdriver


from xinxi import test_url, cookie_f
import time
import pprint
import json, sqlite3
from url import get_url_list_with_page_num

login_url = 'https://member.zjtcn.com/common/login.html?url=https://gd.zjtcn.com/gov/c_cs_d_t_p1.html'
user_name = 'dongbujituan'
password = 'a88888888'
base_url = 'https://gd.zjtcn.com/gov/c2_cs3_d20181105_t_p1.html'

industry_list = []
city_list = []
reg_list = []
year_list = []
mon_list = []


def add_json(st, cookie_name):
    '''
    比较cookie的测试函数
    :param st: cookie
    :param cookie_name: cookie名字 自定义即可
    :return:
    '''
    st_s = json.dumps(st)
    with open(cookie_name + '.json', 'w') as f:
        f.write(st_s)


def crawl_one_page(url):
    '''
    爬取一个分页的数据
    :param cookie:
    :return: ([材料名称] [规格/型号] [除税价格] [除税价格] [含税价格][税率][单位][备注])
    '''
    # 添加cookie
    driver = webdriver.Chrome('./venv/chromedriver')
    driver.get(url)
    driver.delete_all_cookies()
    for k, v in cookie_f.items():
        driver.add_cookie({'name': k, 'value': v})
    driver.get(url)

    # eles_price = driver.find_elements_by_class_name('i_r_price')
    # price_list_chushui=[]
    # price_list_hanshui = []
    #
    # for i in eles_price:
    #     if
    #         price_list.append(i.text)
    # 材料名称
    eles_material = driver.find_elements_by_class_name('material')
    material_list = []
    for j in eles_material:
        material_list.append(j.text)
    # print(material_list)

    # 规格/型号
    eles_standard = driver.find_elements_by_class_name('standard')
    standard_list = []
    for j in eles_standard:
        standard_list.append(j.text)
    # print(standard_list)

    # 除税价格
    eles_price_withou_taxe = driver.find_elements_by_xpath("//td[@tip='priceImage']")
    price_withou_taxe_list = []
    for i in eles_price_withou_taxe:
        price_withou_taxe_list.append(i.text)
    # print(price_withou_taxe_list)

    # 含税价格
    eles_price_with_taxe = driver.find_elements_by_xpath("//td[@tip='pricem']")
    price_with_taxe_list = []
    for i in eles_price_with_taxe:
        price_with_taxe_list.append(i.text)
    # print(price_with_taxe_list)

    # 税率
    eles_taxe = driver.find_elements_by_xpath("//tr[@class='table2']")
    taxe_list = []
    for i in eles_taxe:
        eles_taxe_sub = i.find_element_by_xpath('./td[6]')
        taxe_list.append(eles_taxe_sub.text)
    # print(taxe_list)

    # 单位
    eles_unit = driver.find_elements_by_xpath("//tr[@class='table2']")
    unit_list = []
    for i in eles_unit:
        eles_unit_sub = i.find_element_by_xpath('./td[7]')
        unit_list.append(eles_unit_sub.text)
    # print(unit_list)

    # 备注
    eles_note = driver.find_elements_by_xpath("//tr[@class='table2']")
    note_list = []
    for i in eles_note:
        eles_note_sub = i.find_element_by_xpath('./td[8]')
        note_list.append(eles_note_sub.text)
    # print(note_list)

    # print(driver.page_source)
    driver.close()
    return material_list, standard_list, price_withou_taxe_list, price_with_taxe_list, taxe_list, unit_list, note_list


def craw_whole_pages(base_url,each_city,each_area,each_year,each_mon):
    '''
    爬取全部分页的数据
    :param url:
    :return:
    '''
    material = []
    standard = []
    price_withou_taxe = []
    price_with_taxe = []
    taxe_list = []
    unit_list = []
    note_list = []

    url_list = get_url_list_with_page_num(base_url)
    # print(len(url_list))
    if not url_list:
        print('全页爬取数据停止,因为没有分页数据url_list')
        return None
    cout = 0
    for url in url_list:
        cout += 1
        one_page_data = crawl_one_page(url)
        material += one_page_data[0]
        standard += one_page_data[1]
        price_withou_taxe += one_page_data[2]
        price_with_taxe += one_page_data[3]
        taxe_list += one_page_data[4]
        unit_list += one_page_data[5]
        note_list += one_page_data[6]
        print('正在爬取'+each_city+each_area+each_year+each_mon+'第%s页信息价'%cout)
    print(each_city+each_area+each_year+each_mon+"数据爬取成功,共%s条"%(len(material)))
    return material, standard, price_withou_taxe, price_with_taxe, taxe_list, unit_list, note_list


def save_into_database(data, city, region, year, mon):


    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    for i in range(len(data[0])):
        cur.execute(
            'insert into xinxijia (city,region,year,mon,material,standard,price_withou_taxe,price_with_taxe,unit,note) values (?,?,?,?,?,?,?,?,?,?)',
            ( city, region, year, mon, data[0][i], data[1][i], data[2][i], data[3][i], data[4][i], data[5][i]))
    conn.commit()
    conn.close()
    print(city+region+year+mon+"数据写入成功,共%s条"%(len(data[0])))

def creat_db():
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE xinxijia
             (id INTEGER primary key autoincrement ,
              city text,
              region text,
              year text,
              mon text,
              material text,
              standard text,
              price_withou_taxe text,
              price_with_taxe text,
              taxe text ,
              unit text,
              note text
              )''')

    conn.commit()
    conn.close()
    print('数据库创建完成')

if __name__ == "__main__":
    pass
