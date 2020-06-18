from os import system


def close_medium(image_name):
    vbox_close_medium_cmd = f"VBoxManage closemedium {image_name}"
    vbox_close_medium = system(vbox_close_medium_cmd)
    return vbox_close_medium
