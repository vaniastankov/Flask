import base64
import os
from myapp import app
import secrets
from PIL import Image, ImageOps
from io import BytesIO


def get_pic_string(pic_name):
    pic = os.path.join(app.root_path, 'static/pics', pic_name)
    with open(pic, 'rb') as f:
        return base64.b64encode(f.read()).decode()


def get_pic_array(pic_name):
    pic = os.path.join(app.root_path, 'static/pics', pic_name)
    img = Image.open(pic)
    pic_list = list(img.getdata())
    return pic_list


def delete_pic(pic_name):
    pic = os.path.join(app.root_path, 'static/pics', pic_name)
    if os.path.isfile(pic):
        os.remove(pic)


def save_pic(pic_data):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(pic_data.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    output_size = (120, 160)
    i = Image.open(pic_data)
    i = ImageOps.exif_transpose(i)
    width, height = i.size
    print(width,height)
    if (width>height):
        i.thumbnail([160,120])
    else:
        i.thumbnail([120, 160])
    i.save(picture_path)
    return picture_fn


def check_pic(pic_name):
    pic = os.path.join(app.root_path, 'static/pics', pic_name)
    if os.path.isfile(pic):
        return True
    else:
        return False
