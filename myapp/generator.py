import pdfkit
from flask import render_template
import numpy as np
import random
from myapp.picworks import get_pic_string, get_pic_array

color_schemes =[
    ["#D33F49","#E28413","#767B91","#302B27", "#F7F3E3", "#FFF8F0", "#B6C8A9"],
    ["#8D0801", "#1C0012","#EF6461","#7389AE","#E6DBD0", "#585123", "#FFFDED"],
    ["#FFBF00","#0A090C","#7B6D8D","#60AFFF","#F06543", "#FEFDFF", "F9F8F8"],
    ["#DE6A41","#636564","#540B0E","#3D1308","#C7D6D5", "#E8D6CB", "#EADEDA"],
    ["#220901","#B02E0C","#91ADA4","#817F82","#F2E5D7", "#385F71", "#D6A99A"]
]

def get_color():
    rand = random.randint(0, 4)
    tc1 = color_schemes[rand][0]
    tc2 = color_schemes[rand][1]
    bc1 = color_schemes[rand][2]
    bc2 = color_schemes[rand][3]
    bc3 = color_schemes[rand][4]
    sc1 = color_schemes[rand][5]
    sc2 = color_schemes[rand][6]
    return tc1, tc2, bc1, bc2,bc3, sc1, sc2



def get_img_color(image_path):
    rgbarr = get_pic_array(image_path)
    avg = (np.sum(rgbarr,axis=0)/len(rgbarr)).astype(int)
    brightest =max(rgbarr,key = lambda x: np.sum(x))
    darkest =  min(rgbarr,key = lambda x: np.sum(x))
    random1 = rgbarr[random.randint(0, len(rgbarr)-1)]
    random2 = rgbarr[random.randint(0, len(rgbarr)-1)]
    random3 = rgbarr[random.randint(0, len(rgbarr)-1)]
    random4 = rgbarr[random.randint(0, len(rgbarr) - 1)]
    tc1 = np.sum([np.asarray(darkest)*0.618, np.asarray(random1)*0.382], axis=0).astype(int)
    tc2 = np.sum([np.asarray(darkest)*0.618, np.asarray(random2)*0.382], axis=0).astype(int)
    bc1 = np.sum([np.asarray(brightest)*0.618, np.asarray(avg)*0.382], axis=0).astype(int)
    bc2 = np.sum([np.asarray(brightest)*0.618, np.asarray(random3)*0.382], axis=0).astype(int)
    bc3 = np.sum([np.asarray(brightest) * 0.5, np.asarray(random4) * 0.5], axis=0).astype(int)
    sc1 = np.sum([np.asarray(brightest)*0.618, np.asarray(random1)*0.382], axis=0).astype(int)
    sc2 = np.sum([np.asarray(brightest) * 0.618, np.asarray(random4) * 0.382], axis=0).astype(int)

    tc1 = "#{0:02x}{1:02x}{2:02x}".format(tc1[0], tc1[1], tc1[2])
    tc2 = "#{0:02x}{1:02x}{2:02x}".format(tc2[0], tc2[1], tc2[2])
    bc1 = "#{0:02x}{1:02x}{2:02x}".format(bc1[0], bc1[1], bc1[2])
    bc2 = "#{0:02x}{1:02x}{2:02x}".format(bc2[0], bc2[1], bc2[2])
    bc3 = "#{0:02x}{1:02x}{2:02x}".format(bc3[0], bc3[1], bc3[2])
    sc1 = "#{0:02x}{1:02x}{2:02x}".format(sc1[0], sc1[1], sc1[2])
    sc2 = "#{0:02x}{1:02x}{2:02x}".format(sc2[0], sc2[1], sc2[2])
    return tc1, tc2, bc1, bc2,bc3, sc1, sc2



render_options = {
    "enable-local-file-access": None
}

pdfjit_options = {}


def generate(gen, dev, texts, pic=False):
    devices = list(dev.keys())
    print(devices)
    descriptions = list(dev.values())
    if pic:
        pic_string = get_pic_string(pic)
        tc1,tc2,bc1,bc2,bc3,sc1,sc2 = get_img_color(pic)
        render = render_template("pdf_template.html",gen = gen, dev = devices, des = descriptions, tex = texts,
                                 tc1 = tc1, tc2 = tc2,bc1 = bc1,bc2 = bc2, bc3 = bc3, sc1=sc1, sc2=sc2,
                                 pic = pic_string, options=render_options)
    else:
        tc1, tc2, bc1, bc2, bc3, sc1, sc2 = get_color()
        render = render_template("pdf_template.html",gen = gen, dev = devices, des = descriptions, tex = texts,
                                 tc1 = tc1, tc2 = tc2,bc1 = bc1,bc2 = bc2, bc3 = bc3, sc1=sc1, sc2=sc2,
                                 options=render_options)
    #print(render)
    #random_hex = secrets.token_hex(8)
    #file_path = app.root_path + '/static/pics/{}.html'.format(random_hex)
    #with open(file_path, 'w') as f:
    #    f.write(render)
    #    f.close()
    #return pdfkit.from_file(file_path, False)
    return pdfkit.from_string(render, False)