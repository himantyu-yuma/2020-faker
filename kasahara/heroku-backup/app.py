# -*- coding: utf-8 -*-
from flask import *  # 必要なライブラリのインポート
import mask_test

import os
import numpy as np
import cv2

import datetime

# 画像保存ディレクトリを定義
SAVE_DIR = "./images"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

app = Flask(__name__)  # アプリの設定


@app.route('/')
def index():
    return render_template('index.html', images=os.listdir(SAVE_DIR)[::-1])

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory(SAVE_DIR, path)

@app.route('/upload', methods=['POST'])
def upload():
    if request.files['image']:
        # 画像として読み込み
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)

        # 変換
        # img = mask_test.collage(img)
        img = mask_test.collage(img)

        # 保存
        save_path = os.path.join(SAVE_DIR, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + ".jpg")
        cv2.imwrite(save_path, img)

        print("save", save_path)

        return redirect('/')

if __name__ == "__main__":  # 実行されたら
    # # デバッグモード、localhost:8888 で スレッドオンで実行
    # app.run(debug=True, host='0.0.0.0', port=8888, threaded=True)
    app.run()