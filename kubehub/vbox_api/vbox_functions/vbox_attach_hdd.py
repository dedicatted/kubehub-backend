from os import system


def attach_hdd(name, storagectl, disk_type, medium):
    vbox_attach_hdd_cmd = f'VBoxManage ' \
                          f'storageattach {name} ' \
                          f'--storagectl "{storagectl}" ' \
                          f'--port 0 ' \
                          f'--device 0 ' \
                          f'--type {disk_type} ' \
                          f'--medium  {medium} '
    vbox_attach_hdd = system(vbox_attach_hdd_cmd)
    return vbox_attach_hdd

