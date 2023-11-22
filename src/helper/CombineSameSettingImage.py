import os
from PIL import Image
import shutil
from ..helper import GetCharacAfterRename as characs_after
from ..helper import listupImgs as listimgs

output_folder = 'combine_images(A_C_T)/'

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


# combine image
# 0 2 4 ... (+1)
# 6 8 10
def combine_same_condition_images(_path, _images, _down_scale = 4):
    width, height = Image.open(_path + _images[0]).size
    _resize = (int(width/_down_scale), int(height/_down_scale))

    im1 = get_concat_h(Image.open(_path + _images[0]).resize(_resize), Image.open(_path + _images[2]).resize(_resize))
    im1 = get_concat_h(im1, Image.open(_path + _images[4]).resize(_resize))

    im2 = get_concat_h(Image.open(_path + _images[6]).resize(_resize), Image.open(_path + _images[8]).resize(_resize))
    im2 = get_concat_h(im2, Image.open(_path + _images[10]).resize(_resize))
    im2 = get_concat_v(im1, im2)

    im3 = get_concat_h(Image.open(_path + _images[1]).resize(_resize), Image.open(_path + _images[3]).resize(_resize))
    im3 = get_concat_h(im3, Image.open(_path + _images[5]).resize(_resize))
    im3 = get_concat_v(im2, im3)

    im4 = get_concat_h(Image.open(_path + _images[7]).resize(_resize), Image.open(_path + _images[9]).resize(_resize))
    im4 = get_concat_h(im4, Image.open(_path + _images[11]).resize(_resize))
    return get_concat_v(im3, im4)


def safe_combine_images(_path, _down_scale = 4, _image_points = 12):

    if os.path.isdir(_path + output_folder):
        if(int(len(listimgs.list_images(_path)) / _image_points) == len(listimgs.list_images(_path + output_folder))):
            print('CombineSameSettingImage : Already Done!')
            return _path + output_folder
        shutil.rmtree(_path + output_folder)
        os.mkdir(_path + output_folder)
    else:
        os.mkdir(_path + output_folder)

    image_list = listimgs.list_images(_path)

    for _iter, _imgs in enumerate(image_list):
        if _iter % _image_points == 0:
            _img_list = []
            _anitibiotic = characs_after.get_antibiotics(image_list[_iter])
            _conc = characs_after.get_conc(image_list[_iter])
            _incubation_time = characs_after.get_time(image_list[_iter])
            for i in range(_image_points):
                _img_list.append(_anitibiotic+'_'+_conc+'_'+str(i+1).zfill(2)+'_'+_incubation_time+'.jpg')

            res_img = combine_same_condition_images(_path, _img_list, _down_scale)
            file_name = _anitibiotic + '_' + _conc + '_' + _incubation_time + '.jpg'
            res_img.save(_path + output_folder + file_name)
        else:
            continue
    print('CombineSameSettingImage : Finish!')

    return _path + output_folder
