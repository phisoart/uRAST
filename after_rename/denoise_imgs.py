import numpy as np
import cv2
from matplotlib import pyplot as plt
import helper.listup_imgs
from PIL import Image
from scipy.ndimage import filters
import os
import shutil


def denoise_imgs(_path, _input_folder):
    _img_list = helper.listup_imgs.list_images(_path+_input_folder)
    _output_folder = _input_folder[:-1] + '_sobel/'

    # print(_path+_input_folder)
    # print(_path+_output_folder)

    if os.path.isdir(_path+_output_folder):
        if (int(len(helper.listup_imgs.list_images(_path+_input_folder))) == len(
                helper.listup_imgs.list_images(_path+_output_folder))):
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
