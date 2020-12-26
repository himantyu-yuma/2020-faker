import numpy as np
import cv2
import matplotlib.pyplot as plt

import torch
import torchvision
from torchvision import transforms

from PIL import Image, ImageDraw, ImageFilter, ImageFont

import math

image_path = 'sample-img/human-sample2.jpg'
img = cv2.imread(image_path)
img = img[...,::-1] #BGR->RGB
h,w,_ = img.shape
img = cv2.resize(img,(320,320))

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model = torchvision.models.segmentation.deeplabv3_resnet101(pretrained=True)
model = model.to(device)
model.eval()

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

input_tensor = preprocess(img)
input_batch = input_tensor.unsqueeze(0).to(device)

with torch.no_grad():
    output = model(input_batch)['out'][0]
output = output.argmax(0)
mask = output.byte().cpu().numpy()
# 白塗り
mask = np.where(mask == 0, mask, 255)

# 元のサイズに戻す
mask = cv2.resize(mask,(w,h))
img = cv2.resize(img,(w,h))

pil_img = img.copy()
pil_img = Image.fromarray(pil_img)

pil_mask = mask.copy()
pil_mask = Image.fromarray(pil_mask)

bcg = Image.open('./sample-img/sample2.jpg').copy().resize((16*40, 9*40))
w, h = bcg.size

img_w, img_h = pil_img.size
pil_img = pil_img.resize((math.floor(img_w * h/img_h), math.floor(img_h * h/img_h)))
pil_mask = pil_mask.resize((math.floor(img_w * h/img_h), math.floor(img_h * h/img_h)))

# 下端に合わせる
bcg.paste(pil_img, (w//2-pil_img.size[0]//2,h-pil_img.size[1]), pil_mask)
bcg.save('out/mask-paste-test.jpg', quality=95)
