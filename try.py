import requests
from get_urls import headers

def main():
    res=requests.get("https://gx.zjtcn.com/gov/c1075_cs1076_d_t_p1.html",headers=headers)
    print(res.text)
if __name__ =="__main__":
    main()

    北京
    天津
    上海
    上海
    重庆
    重庆
    内蒙古
    呼和浩特
    新疆
    乌鲁木齐
    西藏
    拉萨
    宁夏
    银川
    广西
    南宁
    黑龙江
    哈尔滨
    吉林
    长春
    辽宁
    沈阳
    河北
    石家庄
    河南
    郑州
    湖北
    武汉
    湖南
    长沙