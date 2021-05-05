# ライブラリーのインポート

import requests
from bs4 import BeautifulSoup
import datetime
import time

# 講義情報のurlを取得


def get_urls():
    url = "https://mobile.matsuyama-u.jp/mbl/hpg010201.htm"
    # HTTPリクエスト
    res = requests.get(url)
    bsObj = BeautifulSoup(res.text, 'html.parser')
    body = bsObj.find('body')
    atags = body.find_all('a')
    hrefs = [elem.get('href') for elem in serch_data.find_all('a')]
    class_hrefs = dict("休講"=hrefs[0], "補講"=hrefs[2], "変更"=hrefs[4])
    return class_hrefs

# 今日のurl


def get_today_url(url):
    res = requests.get(url)
    bsObj = BeautifulSoup(res.text, 'html.parser')
    atag = bsObj.find('a')
    href = atag.get('href')
    return "https://mobile.matsuyama-u.jp/mbl/" + href

# messageを取得し講義情報を返す


def get_message(message):
    class_hrefs = get_urls()
    if message == "休講":
        url = class_hrefs[0]
    elif message == "補講":
        url = class_hrefs[1]
    elif message == "変更":
        url = class_hrefs[2]
    else:
        return "すみません\nメッセージを送る時は、休講、補講、変更のどれかを送ってください"
    url = "https://mobile.matsuyama-u.jp/mbl/" + url
    today_url = get_today_url(url)
    if today_url.split('=')[-1] == datetime.date.today().strftime('%Y%m%d'):
        print("date ok!!")
    else:
        return "今日の{}情報はありません。".format(message)
    res = requests.get(today_url)
    bsObj = BeautifulSoup(res.text, 'html.parser')

    # 不要なものを削除
    for script in bsObj(["script", "style", "title", "a"]):
        script.decompose()

    text = bsObj.get_text()

    # 空白で区切る
    lines = [line.strip() for line in text.splitlines()]

    text = "\n".join(line for line in lines if line)
    return text
