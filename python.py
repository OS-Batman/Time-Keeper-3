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
def modify_report_params(params,change):
    for line in change:
        params[line[0]] = line[1]
    return params

def sent_report(cookies):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58"
    }
    params = {
        'sfzx': '0',
        'tw': '1',
        'area': '江苏省 南京市 玄武区',
        'city': '南京市',
        'province': '江苏省',
        'address': '江苏省南京市玄武区梅园新村街道南京外国语学校',
        'geo_api_info': '{"type":"complete","position":{"Q":32.056225585938,"R":118.801584201389,"lng":118.801584,"lat":32.056226},"location_type":"html5","message":"Get ipLocation failed.Get geolocation success.Convert Success.Get address success.","accuracy":50455,"isConverted":true,"status":1,"addressComponent":{"citycode":"025","adcode":"320102","businessAreas":[{"name":"梅园","id":"320102","location":{"Q":32.045543,"R":118.79988500000002,"lng":118.799885,"lat":32.045543}}],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"演武新村","streetNumber":"153-11号","country":"中国","province":"江苏省","city":"南京市","district":"玄武区","towncode":"320102002000","township":"梅园新村街道"},"formattedAddress":"江苏省南京市玄武区梅园新村街道南京外国语学校","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"}',
        'sfcyglq': '0',
        'sfyzz': '0',
        'qtqk':'',
        'ymtys':''
    }
    params = modify_report_params(params,custom_params)
    # print(params)
    params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    # print(params)
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
