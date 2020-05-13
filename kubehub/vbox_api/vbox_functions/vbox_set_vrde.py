from os import system


def set_vrde(name, status):
    vbox_set_vrde_cmd = f'VBoxManage ' \
                   f'modifyvm {name} ' \
                   f'--vrde {status}'
    vbox_set_vrde = system(vbox_set_vrde_cmd)
    return vbox_set_vrde
