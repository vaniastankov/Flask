import json


def split(dict):
    gen = {'name': dict['name'], 'aname': dict['aname'], 'phone': dict['phone'], 'aphone': dict['aphone'],
           'email': dict['email'], 'aemail': dict['aemail']}
    d_len = int((len(dict)-11)/2)
    devices = {dict["device"]: dict["device_description"]}
    for i in range(1, d_len):
        devices[dict["device" + str(i)]] = dict["device_description"+str(i)]
    texts = {"t": dict["t"], "h": dict["h"], "p": dict["p"]}
    return gen, devices, texts


def parse(form, user):
    if user.gen:
        gen = json.loads(user.gen)
        for key in gen:
            form[key].data = gen[key]
    if user.texts:
        texts = json.loads(user.texts)
        for key in texts:
            form[key].data = texts[key]
