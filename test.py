import json,os
d1 = {
            "id": "4001",
            "city": "南宁市",
            "area": "南宁市",
            "year": "2018",
            "mon": "10月",
            "ori_id": "9332362",
            "name": "内衬PE钢塑复合给水管热水管组合价",
            "unit": "m",
            "xinghao": "DN65",
            "taxe": "",
            "pricewithtaxe": "85.40",
            "note": "(适用2015年新安装定额螺纹连接）",
            "pricewithoutaxe": "73.60",
            "NAVICAT_ROWID": "4001"
        }
d2 ={
            "id": "4002",
            "city": "南宁市",
            "area": "南宁市",
            "year": "2018",
            "mon": "10月",
            "ori_id": "9332363",
            "name": "内衬PE钢塑复合给水管热水管组合价",
            "unit": "m",
            "xinghao": "DN80",
            "taxe": "",
            "pricewithtaxe": "104.00",
            "note": "(适用2015年新安装定额螺纹连接）",
            "pricewithoutaxe": "89.60",
            "NAVICAT_ROWID": "4002"
        }
list=[{
            "id": "4001",
            "city": "南宁市",
            "area": "南宁市",
            "year": "2018",
            "mon": "10月",
            "ori_id": "9332362",
            "name": "内衬PE钢塑复合给水管热水管组合价",
            "unit": "m",
            "xinghao": "DN65",
            "taxe": "",
            "pricewithtaxe": "85.40",
            "note": "(适用2015年新安装定额螺纹连接）",
            "pricewithoutaxe": "73.60",
            "NAVICAT_ROWID": "4001"
        },
        {
            "id": "4002",
            "city": "南宁市",
            "area": "南宁市",
            "year": "2018",
            "mon": "10月",
            "ori_id": "9332363",
            "name": "内衬PE钢塑复合给水管热水管组合价",
            "unit": "m",
            "xinghao": "DN80",
            "taxe": "",
            "pricewithtaxe": "104.00",
            "note": "(适用2015年新安装定额螺纹连接）",
            "pricewithoutaxe": "89.60",
            "NAVICAT_ROWID": "4002"
        },
        {
            "id": "4003",
            "city": "南宁市",
            "area": "南宁市",
            "year": "2018",
            "mon": "10月",
            "ori_id": "9332364",
            "name": "内衬PE钢塑复合给水管热水管组合价",
            "unit": "m",
            "xinghao": "DN100",
            "taxe": "",
            "pricewithtaxe": "124.20",
            "note": "(适用2015年新安装定额螺纹连接）",
            "pricewithoutaxe": "107.10",
            "NAVICAT_ROWID": "4003"
        }]
list2 = ['123','234']
# with open('xx.json','w') as f:
#     for d in list:
#         json.dump(d,f)

with open('xx.json','r') as f:
    print(json.loads(f.readline()))