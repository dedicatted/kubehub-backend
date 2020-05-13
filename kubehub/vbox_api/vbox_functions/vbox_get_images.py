from glob import glob


def get_images(path):
    vbox_imgs_list = glob(path + '/**/*.vmdk', recursive=True)
    return vbox_imgs_list
