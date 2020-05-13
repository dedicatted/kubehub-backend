from os import system


def create_vm(name, os_type, basefolder):
    vbox_create_vm_cmd = f'VBoxManage ' \
                         f'createvm ' \
                         f'--name {name} ' \
                         f'--ostype {os_type} ' \
                         f'--register ' \
                         f'--basefolder {basefolder}'
    vbox_create_vm = system(vbox_create_vm_cmd)
    return vbox_create_vm
