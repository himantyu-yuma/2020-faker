import json
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import base64
from io import BytesIO
import os
import datetime
import numpy as np
# import matplotlib.pyplot as plt

import math

# 3か月分の画像を処理するやつ
# def compile_images(json_file):
def compile_images(data, save_dir='./images'):

    # with open(json_file, mode='r', encoding='utf-8') as f:
    #     data = json.load(f)
    # # 何月から始まってるかで分岐
    # start = data[0]['month']
    # if start == '1月':
    #     base_img = Image.open('./base-img/base1.jpg').copy()
    # elif start == '4月':
    #     base_img = Image.open('./base-img/base2.jpg').copy()
    # elif start == '7月':
    #     base_img = Image.open('./base-img/base3.jpg').copy()
    # elif start == '10月':
    #     base_img = Image.open('./base-img/base4.jpg').copy()

    # 白色のベースイメージ
    base_img = Image.new('RGB', (1080, 1920), (255, 255, 255))
    # 月ごとのやつ
    month_images = [Image.open(f'./month_image/{datum["month"]}.png').copy() for datum in data]
    # まとめる対象の画像たち
    images = [datum['img'] for datum in data]
    # キャプション
    captions = [datum['caption'] for datum in data]

    # 月を貼り付け
    for i, month in enumerate(month_images):
        base_img.paste(month, (0, 0+650*i), mask=month.split()[3])

    # キャプション貼り付け
    draw = ImageDraw.Draw(base_img)
    font = ImageFont.truetype('./GenShinGothic-Medium.ttf', size=70)

    for i, caption in enumerate(captions):
        draw.text(((base_img.size[0]-draw.textsize(caption, font)[0])/2,130+i*650), caption, fill=(0, 0, 0), font=font)

    # 貼り付け
    for i, img in enumerate(images):
        # img_file = Image.open(BytesIO(base64.b64decode(img))).copy().resize((16*40, 9*40))
        img_file = Image.open(BytesIO(base64.b64decode(img))).copy()
        # 縦横比が16:9じゃなかったらトリミング
        w,h = img_file.size
        # if w/h != 16/9 and w/h <= 16/9:
        if w/h < 16/9:
            # 縦の方が長かったら
            img_file = img_file.crop((0, 200, w, 9*w/16+200))
        # elif w/h != 16/9 and w/h > 16/9:
        elif w/h > 16/9:
            # 横の方が長かったら
            img_file = img_file.crop((0, 200, 16*h/9, h+200))
        img_file = img_file.resize((16*40, 9*40))
        # 画像の貼り付け
        base_img.paste(img_file, (200, 250+i*650))

    # 保存
    save_path = os.path.join(save_dir, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + ".jpg")
    base_img.save(save_path, quality=95)

    return save_path


# def encode_test():
#     file_path = 'sample-img/sample1.jpg'
#     with open(file_path, "rb") as image_file:
#         data = base64.b64encode(image_file.read())
#     with open('base64.txt', mode='w', encoding='utf-8') as f:
#         f.write(data.decode('utf-8'))


if __name__ == "__main__":
    with open('../kasahara/image-processing/sample.json', mode='r', encoding='utf-8') as f:
        data = json.load(f)
    compile_images(data)
    # encode_test()