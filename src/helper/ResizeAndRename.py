import os
from PIL import Image
import shutil
from ..helper import GetCharacFromName as characs
from ..helper import listupImgs
import cv2

output_folder = '01resized(A_C_P_T)/'


def resize_and_rename(_path, _down_scale=4):
    if os.path.isdir(_path + output_folder):
        if (int(len(listupImgs.list_images(_path))) == len(listupImgs.list_images(_path + output_folder))):
            print('ResizeAndRename : Already Done!')
            return _path+output_folder
        shutil.rmtree(_path + output_folder)
        os.mkdir(_path + output_folder)
    else:
        os.mkdir(_path + output_folder)

    image_list = listupImgs.list_images(_path)
    incubation_time = 0
    tmp = ''
    width, height = Image.open(_path + image_list[0]).size
    _resize = (int(width / _down_scale), int(height / _down_scale))

    for _iter, _imgs in enumerate(image_list):
        _anitibiotic = characs.get_antibiotics(image_list[_iter])
        _conc = characs.get_conc(image_list[_iter])
        _pos = characs.get_position(image_list[_iter])
        if (_pos == '01'):
            incubation_time = incubation_time + 1

        if (tmp != _anitibiotic + _conc):
            incubation_time = 0
            tmp = _anitibiotic + _conc

        file_name = _anitibiotic + '_' + _conc + '_' + _pos + '_' + str(incubation_time).zfill(2) + '.jpg'

        res_img = cv2.imread(_path + _imgs, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(_path + output_folder + file_name, res_img)
    print('ResizeAndRename : Finish!')
    return _path+output_folder
