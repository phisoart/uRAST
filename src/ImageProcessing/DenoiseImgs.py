import numpy as np
from PIL import Image
from scipy.ndimage import filters
import os
import shutil
from ..helper import listupImgs


def denoise_imgs(_path, _input_folder):
    _img_list = listupImgs.list_images(_path + _input_folder)
    _output_folder = _input_folder[:-1] + '_sobel/'

    if os.path.isdir(_path+_output_folder):
        if (int(len(listupImgs.list_images(_path + _input_folder))) == len(
                listupImgs.list_images(_path + _output_folder))):
            print('denoise_images: Already Done!')
            return _output_folder

        shutil.rmtree(_path+_output_folder)
        os.mkdir(_path+_output_folder)

    else:
        os.mkdir(_path+_output_folder)

    for _img in _img_list:
        im_original = np.array(Image.open(_path + _input_folder + _img))

        # Construct two ndarrays of same size as the input image
        imx = np.zeros(im_original.shape)
        imy = np.zeros(im_original.shape)

        filters.sobel(im_original, 1, imx, cval=0.0)  # axis 1 is x
        filters.sobel(im_original, 0, imy, cval=0.0)  # axis 0 is y

        magnitude = np.sqrt(imx ** 2 + imy ** 2)
        magnitude = Image.fromarray(magnitude).convert('RGB')
        magnitude.save(_path + _output_folder + _img)
    print('denoise_images: Finish!')
    return _output_folder
