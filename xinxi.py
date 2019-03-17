import requests
from bs4 import BeautifulSoup
import re
import http.cookiejar as cj
from pprint import pprint

def cookie_to_dict(cookie):
    cookie_dict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        cookie_dict[key] = value
    return cookie_dict


test_url = 'https://gd.zjtcn.com/gov/c_cs_d_t_p1.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection': 'keep-alive'
}
cookie ='lastHost=gd.zjtcn.com; fac_mat=%3B%E7%94%B5%E7%BC%86%3BAPI%20Q1; lastHost=gd.zjtcn.com; mainHost=gd.zjtcn.com; GOV_REMARK=2018%E5%B9%B4%E4%B8%8B%E5%8D%8A%E5%B9%B4%E4%BB%B7%E6%A0%BC%EF%BC%8C%E6%9C%AC%E4%BB%B7%E6%A0%BC%E8%A1%A8%E4%BB%B7%E6%A0%BC%E4%B8%BA%E5%88%B0%E8%BE%BE%E5%B7%A5%E5%9C%B0%E5%90%AB%E7%A8%8E%E5%8F%82%E8%80%83%E4%BB%B7%E6%A0%BC(%E5%B7%B2%E5%8C%85%E6%8B%AC%E8%BF%90%E6%9D%82%E8%B4%B9%E5%92%8C%E9%87%87%E4%BF%9D%E8%B4%B9)%EF%BC%9B%E7%BB%BC%E5%90%88%E6%8A%98%E7%A8%8E%E7%8E%879.9%20%EF%BC%85%E3%80%82%E5%BB%BA%E8%AE%BE%E5%90%84%E6%96%B9%E5%BA%94%E6%A0%B9%E6%8D%AE%E9%9C%80%E8%A6%81%E5%9C%A8%E5%90%88%E5%90%8C%E4%B8%AD%E6%98%8E%E7%A1%AE%E6%98%AF%E5%90%A6%E9%87%87%E7%94%A8%E3%80%82%E9%83%A8%E5%88%86%E8%A2%8B%E8%8B%97%E5%86%A0%E5%B9%85%E4%B8%BA%E5%85%A8%E5%86%A0%E3%80%82; UM_distinctid=167e506e130555-0de923d4dbe116-6c320a7a-1fa400-167e506e1315fc; lastHost=gd.zjtcn.com; user_uid=dongbujituan; userLoginCookie=0; user_pwd=a88888888; remUser=1; user_name=dongbujituan; cookie_indexScroll=; cookie_indexScroll_date=; Hm_lvt_517073f03fd5acbca941460cde99e5bb=1546183598; PHPSESSID=D0B6A9F714ECB67EF896AB87C2A41282; Hm_lpvt_517073f03fd5acbca941460cde99e5bb=1546381059; CNZZDATA1253320430=536837821-1546178601-%7C1546352259; GUESSINGHD=2019%2F1%2F3; Hm_lvt_a01b74f783ea1eda2c633ceefd483123=1546378575,1546378765,1546456224,1546474735; lastHost=gys.zjtcn.com; mainHost=gys.zjtcn.com; jsid=ff392824-f645-4908-b37f-248aa33fa431; Hm_lpvt_a01b74f783ea1eda2c633ceefd483123=1546483371'
cookie_f = cookie_to_dict(cookie)


def get_html(url):
    r = requests.get(test_url,headers=headers,cookies=cookie_f)
    print(r.text)
    # pprint(r.headers)
    return r


def get_info(r):
    s = BeautifulSoup(r.text)
    total_str = s.find(name='font').string
    total_int = re.findall(r'\d+', total_str)[0]
    # print(total_int)
    return (total_int)

def test_cookies(cookies):
    url = 'http://httpbin.org/cookies'


    r = requests.get(url, cookies=cookies)
    print(r.text)

if __name__ == "__main__":
    r = get_html('https://gd.zjtcn.com/gov/c9_cs_d_t_p1.html')
    # get_info(r)



