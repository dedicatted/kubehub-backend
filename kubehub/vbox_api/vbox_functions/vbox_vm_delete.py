from os import system


def vm_delete(name):
    vbox_remove_vm_cmd = f'VBoxManage unregistervm {name} --delete'
    vbox_remove_vm = system(vbox_remove_vm_cmd)
    return vbox_remove_vm
