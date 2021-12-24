import base64
from datetime import datetime


def decoding_img(img_binary):
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    filename = (
        f'D:\odoo\comunnity\odoo\custom_addons\PJ_TB\static\decoding_img\decoding_{timestamp}.jpg')

    imgdata = base64.b64decode(img_binary)
    with open(filename, 'wb') as f:
        f.write(imgdata)

    return filename
