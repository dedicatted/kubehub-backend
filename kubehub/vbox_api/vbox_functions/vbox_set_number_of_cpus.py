from os import system


def set_number_of_cpus(name, cpus):
    vbox_set_number_of_cpus_cmd = f'VBoxManage modifyvm {name} --cpus {cpus}'
    vbox_set_number_of_cpus= system(vbox_set_number_of_cpus_cmd)
    return vbox_set_number_of_cpus
