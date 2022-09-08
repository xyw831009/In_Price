# This is a sample python project to get the daily news of inke and send to Dingtalk via robot
import re
import requests
import urllib.request
import urllib.parse
import urllib.response
import json
import hashlib
import base64
import hmac
import os
import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
import ssl
import _ssl

"""
#获取当日首条最新消息
def getnewsAddress():
    response = urllib.request.urlopen("http://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%98%A0%E5%AE%87%E5%AE%99%E8%82%A1%E4%BB%B7")
    str = response.read().decode('utf-8')
    #print(str)
    try:
        location = re.search('实时行情', str).span()
    except:
        print("cannot find it")
    news = str[location[1]:location[1] + 200]
    #先使用固定长度获取，后续再优化
    return news
content = getnewsAddress()
"""
#url setup
base_url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%98%A0%E5%AE%87%E5%AE%99'
def get_price():
    driver = webdriver.ChromeOptions()
    driver.add_argument("headless")
    driver = webdriver.Chrome(options=driver)
    driver.get(base_url)
    time.sleep(10)
    try:
        location = driver.find_element(By.CLASS_NAME, 'price_2jYb9')
    except:
        print("not found, error here!")
        content = 0
        driver.close()
        return content
    else:
        content = location.text
        driver.close()
        return content
class Messenger:
    def __init__(self, token=os.getenv("DD_ACCESS_TOKEN"), secret=os.getenv("DD_SECRET")):
        self.timestamp = str(round(time.time() * 1000))
        self.URL = "https://oapi.dingtalk.com/robot/send"
        self.headers = {'Content-Type': 'application/json'}
        secret = secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        self.params = {'access_token': token, "sign": self.sign}
    def send_text(self, content):

        data = {"msgtype": "text", "text": {"content": content}}
        self.params["timestamp"] = self.timestamp
        return requests.post(
            url=self.URL,
            data=json.dumps(data),
            params=self.params,
            headers=self.headers
        )
#the token and secret of Dingtalk robot
m = Messenger(
    token="51cd61253bab887c78b31f2bbace9c43d9a487cba39fca4da7cb3802c9265f4b",
    secret="SEC94fce2e40f1cf5ef56c506dd52d664775f56af3f2c206eff303bde39ce79b26a")
def increase():
    n = 0
    while True:
        n = n + 1
        yield n
it = increase()
def counter():
    return next(it)
def myjob():
    price = get_price()
    if float(price) > 1.30:
        m.send_text(price)
    else:
        print("lower price for shares", price, counter())


schedule. every(50).seconds.do(myjob)
while True:
    schedule.run_pending()
    time.sleep(1)