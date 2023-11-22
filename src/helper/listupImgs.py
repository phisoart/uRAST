import os

def list_images(_path):
    _image_list = []

    for imgs in os.listdir(_path):
        if imgs.endswith(".jpg"):
            _image_list.append(imgs)
    _image_list.sort()
    return _image_list