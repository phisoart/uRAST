import os
import shutil
from PIL import Image

def get_incubation_time(_img_name):
    return _img_name.split('_')[3]

def get_x_incubation_images(_path, _x, _down_scale = 10):
    for imgs in os.listdir(_path):
        width, height = Image.open(_path + imgs).size
        _resize = (int(width/_down_scale), int(height/_down_scale))
        break

    _output_folder = str(_x)+'_hours/'
    if os.path.isdir(_path + _output_folder):
        shutil.rmtree(_path + _output_folder)
        os.mkdir(_path + _output_folder)
    else:
        os.mkdir(_path + _output_folder)

    for imgs in os.listdir(_path):
        if imgs.endswith(".jpg"):
            if get_incubation_time(imgs) == str(_x).zfill(2) + '.jpg':
                _res = Image.open(_path + imgs).resize(_resize)
                _res.save(_path + _output_folder + imgs[:-7] + '.jpg')
    print('get_x_incubation_images => '+str(_x)+'hours: Finish!')
    return _output_folder
