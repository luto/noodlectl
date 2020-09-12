#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import qrcode
import json

libdir = os.path.join(os.path.dirname(__file__), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
import PIL.ImageOps
import traceback

logging.basicConfig(level=logging.DEBUG)

font24 = ImageFont.truetype(os.path.join('Font.ttc'), 24)
font32 = ImageFont.truetype(os.path.join('Font.ttc'), 32)
font52 = ImageFont.truetype(os.path.join('Font.ttc'), 52)

def make_qr_code(url):
    qr = qrcode.make(
        url,
        border=0, version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
    )
    qr = PIL.ImageOps.invert(qr.convert("L"))
    qr.thumbnail((80, 80))
    return qr

def render_slot(data):
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)

    sticks = PIL.ImageOps.invert(Image.open('sticks_long.bmp'))
    draw.bitmap((0, 0), sticks)

    qr = make_qr_code(data["url"])
    draw.bitmap((epd.height - 80 - 100, epd.width - 80), qr)

    draw.text((70, 25), data["name"], font = font32, fill = 0)

    if data["diet"]:
        s = font24.getsize(f'({data["diet"]})')
        draw.text((epd.height - s[0] - 3, epd.width - s[1] - 45), f'({data["diet"]})', font = font24, fill = 0)

    s = font52.getsize(f'{data["price_cents"]}c')
    draw.text((epd.height - s[0] - 3, epd.width - s[1] - 3), f'{data["price_cents"]}c', font = font52, fill = 0)

    return image


nood_data = json.load(open('noods.json'))
slot = "1"
logging.info("epd2in7 Demo")
epd = epd2in7.EPD()
epd.init()
Himage = render_slot(nood_data[slot])
epd.display(epd.getbuffer(Himage))
epd.Dev_exit()
