from flask import Flask, request, abort
import os
import base64
from pathlib import Path
from io import BytesIO
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (ImageMessage, ImageSendMessage, MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

m = 1
n = 0
d = []
montext = ""
captext = ""

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global montext
    global captext
    global m
    global n
    if m == n + 1:
        month_str = str(m)
        montext = month_str + "月"
        captext = event.message.text
        m = m + 1
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("次の月の画像を送信してください。"))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="画像を送信してください。"))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    global m
    global n
    if m == 1:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="テキストでキャプションを送信してください。"))
    else:
        n = n + 1
        message_id = event.message.id
        encoded_image = encode(message_id)
        d.append({"月": montext, "caption": captext, "img": encoded_image})
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="テキストで次の月の写真のキャプションを送信してください。"))

        if n > 12:
            print(d)


def encode(message_id):
    message_content = line_bot_api.get_message_content(message_id)
    image = message_content.content
    return base64.b64encode(image)


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)