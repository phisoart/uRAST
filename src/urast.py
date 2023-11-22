from .helper import ResizeAndRename
from .helper import CombineSameSettingImage
from .helper import listupImgs
from .helper import getXIncubationImgs
from .ImageProcessing import DenoiseImgs
from .ImageProcessing import ImageProcessing
from PIL import Image
import numpy as np
import pandas as pd


def get_SorR(_path, _ref_img, _inc_img, _img_list, _imaging_points=12):
    tmp = 0
    for _img in _img_list:
        ref = np.array(Image.open(_path + _ref_img + _img))
        inc = np.array(Image.open(_path + _inc_img + _img))
        ref[ref > 0] = 1
        inc[inc > 0] = 1
        if np.sum(inc) > 1.5 * np.sum(ref):
            tmp = tmp + 1
    if tmp > 3:
        return 'S'
    else:
        return 'R'


def get_result_longtime_ver(_path, _ref_img, _inc_img, _imaging_points=12):
    _ref_img_list = listupImgs.list_images(_path + _ref_img)
    result = []
    for _iter, _img in enumerate(_ref_img_list):
        if _iter % _imaging_points == 0:
            tmp = [_img.split('_')[0], float(_img.split('_')[1])]
            tmp.append(get_SorR(_path, _ref_img, _inc_img, _ref_img_list[_iter:_iter + _imaging_points]))
            result.append(tmp)
        else:
            continue
    return result


def urast(_src, _dst):
    rename_folder = ResizeAndRename.resize_and_rename(_src)
    CombineSameSettingImage.safe_combine_images(rename_folder, 12)

    inc_0_folder = getXIncubationImgs.get_x_incubation_images(rename_folder, 0)
    inc_4_folder = getXIncubationImgs.get_x_incubation_images(rename_folder, 4)
    inc_6_folder = getXIncubationImgs.get_x_incubation_images(rename_folder, 6)
    inc_12_folder = getXIncubationImgs.get_x_incubation_images(rename_folder, 12)

    inc_0_denoise_folder = DenoiseImgs.denoise_imgs(rename_folder, inc_0_folder)
    inc_4_denoise_folder = DenoiseImgs.denoise_imgs(rename_folder, inc_4_folder)
    inc_6_denoise_folder = DenoiseImgs.denoise_imgs(rename_folder, inc_6_folder)
    inc_12_denoise_folder = DenoiseImgs.denoise_imgs(rename_folder, inc_12_folder)

    threshold_folder_ref, threshold_folder_inc = ImageProcessing.thresholding_imgs(rename_folder, inc_0_denoise_folder,
                                                                                   inc_4_denoise_folder)
    _res = get_result_longtime_ver(rename_folder, threshold_folder_ref, threshold_folder_inc)
    _res = sorted(_res, key=lambda x: (x[0], x[1]))
    pd.DataFrame(_res, columns=['Antibiotics', 'Concentration', 'S/R']).to_csv(_dst + "result_4.csv")

    threshold_folder_ref, threshold_folder_inc = ImageProcessing.thresholding_imgs(rename_folder, inc_0_denoise_folder,
                                                                                   inc_6_denoise_folder)
    _res = get_result_longtime_ver(rename_folder, threshold_folder_ref, threshold_folder_inc)
    _res = sorted(_res, key=lambda x: (x[0], x[1]))
    pd.DataFrame(_res, columns=['Antibiotics', 'Concentration', 'S/R']).to_csv(_dst + "result_6.csv")

    threshold_folder_ref, threshold_folder_inc = ImageProcessing.thresholding_imgs(rename_folder, inc_0_denoise_folder,
                                                                                   inc_12_denoise_folder)
    _res = get_result_longtime_ver(rename_folder, threshold_folder_ref, threshold_folder_inc)
    _res = sorted(_res, key=lambda x: (x[0], x[1]))
    pd.DataFrame(_res, columns=['Antibiotics', 'Concentration', 'S/R']).to_csv(_dst + "result_12.csv")
