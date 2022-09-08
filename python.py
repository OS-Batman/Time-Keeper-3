import requests
import urllib
# smtplib 用于邮件的发信动作
import smtplib
import os
# email 用于构建邮件内容
from email.mime.text import MIMEText
custom_params = [

]
use_proxy = False
proxy_detail = {
    'http':'127.0.0.1:8080'
}

def sent_report(cookies):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58"
    }
    params = {
        "sfzx":"1", #是否在校
        "tw":"1",   #体温（list）(0-"Below 36";1-"36-36.5";2-"36.5-36.9";3-"36.9-37.3"; ... , i<=8)
        "area":"陕西省 西安市 长安区",
        "city":"西安市",
        "province":"陕西省",
        "address":"陕西省西安市长安区郭杜街道西北大学南校区学生公寓10号楼西北大学长安校区",
        "geo_api_info":'{"type":"complete","info":"SUCCESS","status":1,"$Da":"jsonp_687452_","position":{"Q":34.14218,"R":108.87518999999998,"lng":108.87519,"lat":34.14218},"message":"Get ipLocation success.Get address success.","location_type":"ip","accuracy":null,"isConverted":true,"addressComponent":{"citycode":"029","adcode":"610116","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"文苑南路","streetNumber":"11号","country":"中国","province":"陕西省","city":"西安市","district":"长安区","township":"郭杜街道"},"formattedAddress":"陕西省西安市长安区郭杜街道西北大学南校区学生公寓10号楼西北大学长安校区","roads":[],"crosses":[],"pois":[]}',   #高德SDK返回值
        "sfcyglq":"0",  #是否隔离期
        "sfyzz":"0",    #是否有症状
        "qtqk":"",  #其他情况
        "ymtys":""  #不明（可能是一码通颜色，暂无用）
    }
    if(use_proxy==False):
        res = requests.post("https://app.nwu.edu.cn/ncov/wap/open-report/save",headers=headers,cookies=cookies,data=params)
    else:
        res = requests.post("https://app.nwu.edu.cn/ncov/wap/open-report/save",headers=headers,cookies=cookies,data=params,proxies=proxy_detail)
    json_res = res.json()
    # 邮件发送
    from_addr = os.environ['ADDRESS']
    password = os.environ['PASSWORD']
    # 收信方邮箱
    to_addr = os.environ['ADDRESS']
    # 发信服务器
    smtp_server = 'smtp.qq.com'
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(json_res['m'], 'plain', 'utf-8')
    msg['From'] = '时光守护者3号'
    msg['Subject'] = '西大晨午检填报结果'
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()
    return json_res['m']
stu_varify_cookies = {
    "UUkey":os.environ['UU'],
    "eai-sess":os.environ['EAI']
}
sent_report(stu_varify_cookies)
