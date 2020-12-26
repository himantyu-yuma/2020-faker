from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ベースイメージ読み込み＆コピー作成
base_img = Image.open('./base-img/base1.jpg').copy()
# 貼り付ける画像読み込み＆リサイズ
# img_1 = Image.open('./sample-img/sample1.jpg').resize((16*40, 9*40))
images = [
    Image.open('./sample-img/sample1.jpg').resize((16*40, 9*40)),
    Image.open('./sample-img/sample2.jpg').resize((16*40, 9*40)),
    Image.open('./sample-img/sample3.jpg').resize((16*40, 9*40))
]
captions = [
    '彼ぴとデート♡楽しかった♪',
    '離れていても同じ空の下だょ…',
    '縦画像だとこんなかんじ'
]

# キャプション追加
draw = ImageDraw.Draw(base_img)
font = ImageFont.truetype('./GenShinGothic-Medium.ttf', size=70)

for i, caption in enumerate(captions):
    draw.text((30,130+i*650), caption, fill=(0, 0, 0), font=font)

# 貼り付け
# base_img.paste(images[0], (200, 250))
# base_img.paste(images[1], (200, 900))
# base_img.paste(images[2], (200, 1550))
for i, img in enumerate(images):
    base_img.paste(img, (200, 250+i*650))
# 保存
base_img.save('./out/test.jpg', quality=95)
