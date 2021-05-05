# インポート
from flask import Flask, request, abort
from flask.logging import create_logger
import os
import scrape as sc
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
# lineでのイベント取得
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

app = False(__name__)
log = create_logger(app)

# 環境変数取得
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEK_SECRET = os.environ["CAHNNEL_SECRET"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEK_SECRET)

# アプリケーション本体をopenすると実効


@app.route("/")
def hello_world():
    return "hello world"

# /callbackにアクセスした時 webhook


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request boby as text
    body = request.get_data(as_text=True)
    log.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# メッセージ受信時のイベント


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )
