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
    hrefs = [elem.get('href') for elem in atags]
    class_hrefs = dict(休講=hrefs[0], 補講=hrefs[2], 教室=hrefs[4])
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
    messages = message.split()
    texts = []
    for m in messages:
        if m in ["休講", "休校", "きゅうこう"]:
            url = class_hrefs["休講"]
        elif m in ["補講", "ほこう"]:
            url = class_hrefs["補講"]
        elif m in ["教室", "きょうしつ", "教室変更"]:
            url = class_hrefs["教室"]
        elif m in ["お問合せ", "お問い合わせ"]:
            return "お問い合わせはこちらから!\nhttps://twitter.com/Koho_chan_"
        else:
            return "すみません\nメッセージを送る時は\n休講、補講、教室変更\nのどれかを送ってください"
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
        print(text)

        # 空白で区切る
        lines = [line.strip() for line in text.splitlines()]
        print(lines)

        text = "\n".join(line for line in lines if line)
        print(text)
        texts.append(text + "\nhttps://mobile.matsuyama-u.jp/")
    return texts
