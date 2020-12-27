from flask import *
import os
import base64
from pathlib import Path
from io import BytesIO
import json
import re

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (ImageMessage, ImageSendMessage, MessageEvent, TextMessage, TextSendMessage, MessageAction, QuickReplyButton, QuickReply)

# 画像処理するやつ
import image_process


app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# 画像保存ディレクトリを定義
SAVE_DIR = 'images'
# デプロイしてるURL
DEPLOY_URL = 'https://faker-2020.herokuapp.com'


mlist = []
mdic = {}

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
    month_list = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    
    message_text = event.message.text

    if message_text == "まとめる":
        items = [QuickReplyButton(action=MessageAction(label=f"{month}", text=f"{month}")) for month in month_list]
        messages = TextSendMessage(text="何月の写真を送りますか？",quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)

    elif "月" in message_text:
        mdic['month'] = message_text.replace('月','')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="アルバムにする画像を送信してください"))

    elif len(mdic) != 0:
        mdic['caption'] = message_text
        print(mdic)
        mlist.append(mdic.copy())
        mdic.clear()
        print(mlist)
        if len(mlist) < 3:
            items = [QuickReplyButton(action=MessageAction(label=f"{month}", text=f"{month}")) for month in month_list]
            messages = TextSendMessage(text="何月の写真を送りますか？",quick_reply=QuickReply(items=items))
            line_bot_api.reply_message(event.reply_token, messages=messages)
            print(mlist)
        else:
            save_path = image_process.compile_images(mlist, SAVE_DIR)
            # json_data = json.dumps(mlist)
            # print(json_data)git 
            
            # 画像の送信
            image_message = ImageSendMessage(
                original_content_url=f'https://faker-2020.herokuapp.com/{save_path}',
                preview_image_url=f'https://faker-2020.herokuapp.com/{save_path}',
            )

            line_bot_api.reply_message(event.reply_token, image_message)
            mlist.clear()


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    message_id = event.message.id
    if len(mdic) != 0:
        encoded_image = encode(message_id)
        mdic['img'] = encoded_image
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="テキストでキャプションを送信してください。"))


def encode(message_id):
    message_content = line_bot_api.get_message_content(message_id)
    image = message_content.content
    return base64.b64encode(image)


@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory(SAVE_DIR, path)


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)