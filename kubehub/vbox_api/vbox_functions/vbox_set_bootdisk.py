from os import system


def set_bootdisk(name, boot1, boot2, boot3, boot4):
    vbox_set_bootdisk_cmd = f'VBoxManage ' \
                            f'modifyvm {name} ' \
                            f'--boot1 {boot1} ' \
                            f'--boot2 {boot2} ' \
                            f'--boot3 {boot3} ' \
                            f'--boot4 {boot4}'
    vbox_set_bootdisk = system(vbox_set_bootdisk_cmd)
    return vbox_set_bootdisk
