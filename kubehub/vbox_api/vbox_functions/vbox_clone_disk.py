from os import system


def clone_disk(image_path, new_disk_path):
    vbox_clone_disk_cmd = f"VBoxManage clonehd {image_path} {new_disk_path}"
    vbox_clone_disk = system(vbox_clone_disk_cmd)
    return vbox_clone_disk
