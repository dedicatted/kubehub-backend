from glob import glob


def get_images(path):
    vbox_vmdk_list = glob(path + '/**/*.vmdk', recursive=True)
    vbox_vdi_list = glob(path + '/**/*.vdi', recursive=True)
    vbox_imgs_list = vbox_vdi_list + vbox_vmdk_list
    return vbox_imgs_list
