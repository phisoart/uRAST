from . import BeadDecoding
from . import CircleDetection
from . import ExtractBeadBrightness
from PIL import Image
import numpy as np
import cv2
import os
import shutil
from ..helper import listupImgs

def circle_detection(img_bf, beads, _dst):
    print('Qmap - Start Circle Detection')
    CircleDetection.circle_detection(img_bf, beads, _dst)
    print('Qmap - Complete Circle Detection')


def extract_bead_brightness(img_pe, beads):
    print('Qmap - Start Extract_Bead_Brightness')
    ExtractBeadBrightness.extract_bead_brightness(img_pe, beads)
    print('Qmap - Complete Extract_Bead_Brightness')


def bead_decoding(img_bf, beads, _dst):
    print('Qmap - Start Bead Decoding')
    BeadDecoding.bead_decoding(img_bf, beads, _dst)
    print('Qmap - Complete Bead Decoding')

def get_mean_from_image(_img):
    res = np.array(Image.open(_img))
    return int(np.mean(res))

def get_std_from_image(_img):
    res = np.array(Image.open(_img))
    return int(np.std(res))

def get_threshold(_img):
    # img = np.array(Image.open(_img))
    # result = img.flatten()
    # result = result.sort()
    # _l = result.size*9/10
    # return result(_l)

    return get_mean_from_image(_img) + 5 * get_std_from_image(_img)

def get_threshold_image(_img, _threshold = 40):
    img = np.array(Image.open(_img))
    ret, output_img = cv2.threshold(img, _threshold, 255, cv2.THRESH_BINARY)
    return Image.fromarray(output_img)

def thresholding_imgs(_path, _ref_input_folder, _inc_input_folder):
    _ref_img_list = listupImgs.list_images(_path + _ref_input_folder)

    _ref_output_folder = _ref_input_folder[:-1]+'_threshold/'
    _inc_output_folder = _inc_input_folder[:-1]+'_threshold/'

    if os.path.isdir(_path+_ref_output_folder):
        shutil.rmtree(_path+_ref_output_folder)
        os.mkdir(_path+_ref_output_folder)
    else:
        os.mkdir(_path+_ref_output_folder)
    if os.path.isdir(_path+_inc_output_folder):
        shutil.rmtree(_path+_inc_output_folder)
        os.mkdir(_path+_inc_output_folder)
    else:
        os.mkdir(_path+_inc_output_folder)

    for _img in _ref_img_list:
        # _ref_img = np.array(Image.open(_path + _ref_input_folder + _img))
        # _inc_img = np.array(Image.open(_path + _inc_input_folder + _img))
        # plt.hist(_inc_img.ravel(), 256, [0, 256]);
        # plt.savefig(_path + _inc_output_folder + _img[:-4] + '_hist.jpg')
        # plt.hist(_ref_img.ravel(), 256, [0, 256]);
        # plt.savefig(_path + _ref_input_folder + _img[:-4] + '_hist.jpg')
        # plt.clf()

        _threshold = get_threshold(_path + _inc_input_folder + _img)
        res = get_threshold_image(_path + _inc_input_folder + _img, _threshold)
        res.save(_path + _inc_output_folder + _img)

        res = get_threshold_image(_path + _ref_input_folder + _img, _threshold)
        res.save(_path + _ref_output_folder + _img)
    print('thresholding_images: Finish!')
    return _ref_output_folder, _inc_output_folder