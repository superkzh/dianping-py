# 20190719 python3.6
import requests
import json
import re
from tqdm import tqdm

orgin_url = 'http://s.dianping.com/event/'


cookies = {
    '_lxsdk_cuid': '16c084f1d77c8-0233571fee7954-37667c02-13c680-16c084f1d77c8',
    '_lxsdk': '16c084f1d77c8-0233571fee7954-37667c02-13c680-16c084f1d77c8',
    '_hc.v': '459501aa-5325-5fd5-9a5f-b776e69a1aae.1563507499',
    'ctu': 'ad2e95b0518b8e5b0a35d7f6bdc2b5f23b1e2d1d2d92124dafae7234c68836d8',
    'cye': 'beijing',
    'dper': '41ec583ca2dbac008f81c505576f02f3c1f52b8875ce229c5e9e3a8845b0c61815577c5f461f68f41cfb11fc335bb0b768028ea4aba769a8b02e10a567db654f287e930c7c8561648b99fa26b3b6af275b17504931a45ad5786e3d78ae2efd68',
    'll': '7fd06e815b796be3df069dec7836c3df',
    'ua': '%E7%A7%8D%E8%8A%B1%E5%AE%B6%E7%9A%84%E5%BA%B7%E5%B0%8F%E5%8D%8E',
    'cy': '2',
    '_lx_utm': 'utm_source%3Dgoogle%26utm_medium%3Dorganic',
    '_lxsdk_s': '16c08e383cb-c2e-d34-8f5%7C%7C63',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'http://s.dianping.com/event/beijing',
    'Origin': 'http://s.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'Content-Type': 'application/json',
}


ids = []
activityTitles = []
data = {"cityId":"2","type":0,"mode":"","page":1}
for page in range(1,10):
    data["page"] = str(page)
    response = requests.post('http://m.dianping.com/activity/static/pc/ajaxList', headers=headers, cookies=cookies, data=str(json.dumps(data)))
    # print(page)
    for item in response.json()['data']['detail']:
        activityTitles.append(item['activityTitle'])
        ids.append(item['offlineActivityId'])

print('搜索到'+str(len(ids))+'条霸王餐')

cookies = {
    '_lxsdk_cuid': '16c084f1d77c8-0233571fee7954-37667c02-13c680-16c084f1d77c8',
    '_lxsdk': '16c084f1d77c8-0233571fee7954-37667c02-13c680-16c084f1d77c8',
    '_hc.v': '459501aa-5325-5fd5-9a5f-b776e69a1aae.1563507499',
    'ctu': 'ad2e95b0518b8e5b0a35d7f6bdc2b5f23b1e2d1d2d92124dafae7234c68836d8',
    'cye': 'beijing',
    'dper': '41ec583ca2dbac008f81c505576f02f3c1f52b8875ce229c5e9e3a8845b0c61815577c5f461f68f41cfb11fc335bb0b768028ea4aba769a8b02e10a567db654f287e930c7c8561648b99fa26b3b6af275b17504931a45ad5786e3d78ae2efd68',
    'll': '7fd06e815b796be3df069dec7836c3df',
    'ua': '%E7%A7%8D%E8%8A%B1%E5%AE%B6%E7%9A%84%E5%BA%B7%E5%B0%8F%E5%8D%8E',
    'cy': '2',
    '_lx_utm': 'utm_source%3Dgoogle%26utm_medium%3Dorganic',
    '_lxsdk_s': '16c08e383cb-c2e-d34-8f5%7C%7C63',
}

headers = {
    'Origin': 'http://s.dianping.com',
    'Accept-Encoding': 'gzip, deflate',
    'X-Request': 'JSON',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8;',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept': 'application/json, text/javascript',
    'Referer': 'http://s.dianping.com/event/753639142',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

data = {
  'offlineActivityId': '753639142',
  'phoneNo': '18612998187',
  'shippingAddress': '',
  'extraCount': '',
  'birthdayStr': '',
  'email': '',
  'marryDayStr': '',
  'babyBirths': '',
  'pregnant': '',
  'marryStatus': '0',
  'comboId': '',
  'branchId': '568675',
  'usePassCard': '0',
  'passCardNo': '',
  'isShareSina': 'false',
  'isShareQQ': 'false'
}
success = []
for _id in tqdm(ids):
    text = requests.get(orgin_url+str(_id),headers=headers,cookies=cookies).text
    shopid = re.search(r'shopid:[0-9]*',text).group() # 一个就够
    shopid = shopid.split('shopid:')[1]
    data['offlineActivityId'] = str(_id)
    data['branchId'] = shopid
    response = requests.post('http://s.dianping.com/ajax/json/activity/offline/saveApplyInfo', headers=headers,cookies=cookies, data=data)

    msg = json.loads(response.text)
    if response.text[0] != '{':
        print(activityTitles[ids.index(_id)]+' 登记成功')
        success.append(activityTitles[ids.index(_id)])
        continue
    if "不要重复报名" in msg["msg"]["html"]:
        success.append(activityTitles[ids.index(_id)])
    # print(activityTitles[ids.index(_id)]+' 登记失败')

print('成功登记活动：')
for i in success:
    print(i)
