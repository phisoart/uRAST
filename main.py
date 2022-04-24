import after_rename.get_x_incubation_images as get_onlt_inc_time
import after_rename.CombineSameSettingImage
import after_rename.denoise_imgs as denoise
import ResizeAndRename as re
import helper.image_analysis as image_analysis
import helper.listup_imgs
from PIL import Image
import numpy as np
import pandas as pd
import after_rename.AlignImages
import multiprocess


# 이미지 정보 : Antibiotics, concentration, incubation time
data_path = '/Users/phiso_imac/uRAST/211213_PA_B0162_FDAv4_1,2_medium_X_control_O/'
file_name = 'PA_1213_FDA2_202112132300/'
running_time = 11
imaging_points = 12


def get_SorR(_path, _ref_img, _inc_img, _img_list, _imaging_points=12):
    tmp = 0
    for _img in _img_list:
        ref = np.array(Image.open(_path + _ref_img + _img))
        inc = np.array(Image.open(_path + _inc_img + _img))
        ref[ref > 0] = 1
        inc[inc > 0] = 1
        if np.sum(inc) > 1.5*np.sum(ref):
            tmp = tmp + 1
    if tmp > 1:
        return 'S'
    else:
        return 'R'

# \export PATH="/Users/phiso_imac/opt/anaconda3/bin:$PATH"

def get_result_longtime_ver(_path, _ref_img, _inc_img, _imaging_points=12):
    _ref_img_list = helper.listup_imgs.list_images(_path + _ref_img)
    result = []
    for _iter, _img in enumerate(_ref_img_list):
        if _iter % _imaging_points == 0:
            tmp = [_img.split('_')[0], float(_img.split('_')[1])]
            tmp.append(get_SorR(_path, _ref_img, _inc_img, _ref_img_list[_iter:_iter+_imaging_points]))
            result.append(tmp)
        else:
            continue
    return result


# images
if __name__ == '__main__':
    # rename_folder = re.resize_and_rename(data_path + file_name, _down_scale=2)
    rename_folder = re.resize_and_rename(data_path + file_name)

    # for short_anal
    # after_rename.AlignImages.get_align_images(rename_folder, '', running_time)
    #
    #
    # just for human
    # after_rename.CombineSameSettingImage.safe_combine_images(rename_folder, imaging_points)



    inc_0_folder = get_onlt_inc_time.get_x_incubation_images(rename_folder, 0)
    inc_4_folder = get_onlt_inc_time.get_x_incubation_images(rename_folder, 4)
    inc_6_folder = get_onlt_inc_time.get_x_incubation_images(rename_folder, 6)
    inc_12_folder = get_onlt_inc_time.get_x_incubation_images(rename_folder, 12)


    inc_0_denoise_folder = denoise.denoise_imgs(rename_folder, inc_0_folder)
    inc_4_denoise_folder = denoise.denoise_imgs(rename_folder, inc_4_folder)
    inc_6_denoise_folder = denoise.denoise_imgs(rename_folder, inc_6_folder)
    inc_12_denoise_folder = denoise.denoise_imgs(rename_folder, inc_12_folder)

    threshold_folder_ref, threshold_folder_inc = image_analysis.thresholding_imgs(rename_folder, inc_0_denoise_folder,
                                                                                  inc_4_denoise_folder)
    _res = get_result_longtime_ver(rename_folder, threshold_folder_ref, threshold_folder_inc)
    _res = sorted(_res, key=lambda x: (x[0], x[1]))
    pd.DataFrame(_res, columns=['Antibiotics', 'Concentration', 'S/R']).to_csv(data_path+file_name+"result_4.csv")


    threshold_folder_ref, threshold_folder_inc = image_analysis.thresholding_imgs(rename_folder, inc_0_denoise_folder,
                                                                                  inc_6_denoise_folder)
    _res = get_result_longtime_ver(rename_folder, threshold_folder_ref, threshold_folder_inc)
    _res = sorted(_res, key=lambda x: (x[0], x[1]))
    pd.DataFrame(_res, columns=['Antibiotics', 'Concentration', 'S/R']).to_csv(data_path+file_name+"result_6.csv")


    threshold_folder_ref, threshold_folder_inc = image_analysis.thresholding_imgs(rename_folder, inc_0_denoise_folder,
                                                                                  inc_12_denoise_folder)
    _res = get_result_longtime_ver(rename_folder, threshold_folder_ref, threshold_folder_inc)
    _res = sorted(_res, key=lambda x: (x[0], x[1]))
    pd.DataFrame(_res, columns=['Antibiotics', 'Concentration', 'S/R']).to_csv(data_path+file_name+"result_12.csv")
