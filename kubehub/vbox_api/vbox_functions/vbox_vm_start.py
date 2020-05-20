from os import system


def start_vm(vm_name, start_mode):
    vbox_start_vm_cmd = f'VBoxManage startvm {vm_name} --type {start_mode}'
    vbox_start_vm = system(vbox_start_vm_cmd)
    return vbox_start_vm
