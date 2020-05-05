from glob import glob


def get_images(path):
    vbox_imgs_list = glob(path + '/**/*.vdi', recursive=True)
    return vbox_imgs_list
