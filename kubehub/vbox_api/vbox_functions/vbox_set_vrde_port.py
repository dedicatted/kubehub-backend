from os import system


def set_vrde_port(name, vrdemulticon_status, vrdeport):
    vbox_set_vrde_port_cmd = f'VBoxManage ' \
                             f'modifyvm {name} ' \
                             f'--vrdemulticon {vrdemulticon_status} ' \
                             f'--vrdeport {vrdeport}'
    vbox_set_vrde_port = system(vbox_set_vrde_port_cmd)
    return vbox_set_vrde_port
