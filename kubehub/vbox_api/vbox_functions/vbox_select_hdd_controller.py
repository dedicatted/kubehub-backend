from os import system


def select_hdd_controller(name, controller_name, controller):
    vbox_select_hdd_controller_cmd = f'VBoxManage ' \
                                f'storagectl {name} ' \
                                f'--name "{controller_name}" ' \
                                f'--add sata ' \
                                f'--controller {controller}'
    vbox_select_hdd_controller = system(vbox_select_hdd_controller_cmd)
    return vbox_select_hdd_controller
