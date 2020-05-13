from os import system


def set_ram_size(name, ram_size):
    ram_size_mb = int(ram_size) * 1024

    vbox_set_ram_size_cmd = f'VBoxManage ' \
                            f'modifyvm {name} ' \
                            f'--memory {ram_size_mb} ' \
                            f'--vram 128'
    vbox_set_ram_size = system(vbox_set_ram_size_cmd)
    return vbox_set_ram_size
