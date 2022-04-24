import cv2
import numpy as np
import os
import helper.get_characteristic_from_name as characs
import shutil
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
import helper.listup_imgs as list_img

MAX_FEATURES = 500
MIN_MATCH_PERCENT = 0.3
MAX_MATCH_PERCENT = 0.9
STEP_MATCH_PERCENT = 0.05
GOOD_MATCH_CONS = 0.03

output_folder_aligned = '02aligned/'
output_folder_subs = '03subs/'


def is_good_match(_h):
    tmp = max(abs(_h[0][0] - 1), abs(_h[1][1] - 1), abs(_h[2][2] - 1))
    if tmp > STEP_MATCH_PERCENT:
        return False
    return True


def save_images(_path, _name, _img):
    cv2.imwrite(_path + _name, _img)


def align_images_prev_h(im1, im2, MATCH_PERCENT, prev_h_list):
    # Convert images to grayscale
    im1Gray = cv2.imread(im1, cv2.IMREAD_COLOR)
    im2Gray = cv2.imread(im2, cv2.IMREAD_COLOR)
    im1 = cv2.imread(im1, cv2.IMREAD_COLOR)
    im2 = cv2.imread(im2, cv2.IMREAD_COLOR)

    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    sorted(matches, key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    # # Draw top matches
    # imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    # cv2.imwrite("matches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt
    if (len(points1) < 5) | (len(points2) < 5):
        return 'fail', [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use homography
    height, width, ch = im2.shape
    if h is None:
        return 'fail', [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    acc_h = h

    for tmp in prev_h_list:
        acc_h = np.matmul(h, tmp)

    im1Reg = cv2.warpPerspective(im1, acc_h, (width, height))

    return im1Reg, h, acc_h


# im1 : target_image
# im2 : ref_image
def align_images(im1, im2, MATCH_PERCENT):
    # Convert images to grayscale
    im1Gray = cv2.imread(im1, cv2.IMREAD_COLOR)
    im2Gray = cv2.imread(im2, cv2.IMREAD_COLOR)
    im1 = cv2.imread(im1, cv2.IMREAD_COLOR)
    im2 = cv2.imread(im2, cv2.IMREAD_COLOR)

    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    sorted(matches, key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    # # Draw top matches
    # imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    # cv2.imwrite("matches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt
    if (len(points1) < 5) | (len(points2) < 5):
        return 'fail', [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use homography
    height, width, ch = im2.shape
    if h is None:
        return 'fail', [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    im1Reg = cv2.warpPerspective(im1, h, (width, height))

    return im1Reg, h


def make_folders(_path):
    if os.path.isdir(_path + output_folder_aligned):
        shutil.rmtree(_path + output_folder_aligned)
        os.mkdir(_path + output_folder_aligned)
    else:
        os.mkdir(_path + output_folder_aligned)
    if os.path.isdir(_path + output_folder_subs):
        shutil.rmtree(_path + output_folder_subs)
        os.mkdir(_path + output_folder_subs)
    else:
        os.mkdir(_path + output_folder_subs)


def get_align_images(_path, input_folder, _running_time):
    _image_list = list_img.list_images(_path + input_folder)
    make_folders(_path)

    for _iter, _imgs in enumerate(_image_list):
        _h_list = []
        if _iter % _running_time == 0:
            for i in range(_iter + 1, _iter + _running_time):
                for _match_percent in np.arange(MIN_MATCH_PERCENT, MAX_MATCH_PERCENT, STEP_MATCH_PERCENT):
                    if i == _iter + 1:
                        _res, _h = align_images(_path + input_folder + _image_list[i],
                                                _path + input_folder + _image_list[i - 1], _match_percent)
                        if not is_good_match(_h):
                            continue
                    else:
                        _res, _h, _acc_h = align_images_prev_h(_path + input_folder + _image_list[i],
                                                _path + input_folder + _image_list[i - 1], _match_percent, _h_list)
                        if not is_good_match(_acc_h):
                            continue
                    _h_list.append(_h)
                    save_images(_path + output_folder_aligned, _image_list[i], _res)
                    # res_subs = cv2.subtract(_res,
                    #                         cv2.imread(_path + input_folder + _image_list[i - 1], cv2.IMREAD_GRAYSCALE))
                    res_subs = abs(_res - cv2.imread(_path + input_folder + _image_list[i - 1], cv2.IMREAD_COLOR))
                    difference = cv2.absdiff(cv2.imread(_path + input_folder + _image_list[_iter]), _res)
                    save_images(_path + output_folder_subs, _image_list[i][:-4] + '_be_th.jpg', difference)
                    _, difference = cv2.threshold(difference, 50, 255, cv2.THRESH_BINARY)

                    save_images(_path + output_folder_subs, _image_list[i], difference)
                    break

        else:
            continue
