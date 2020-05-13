from os import system


def add_network_card(name, status):
    vbox_add_network_card_cmd = f'VBoxManage ' \
                                f'modifyvm {name} ' \
                                f'--ioapic {status}'
    vbox_add_network_card = system(vbox_add_network_card_cmd)
    return vbox_add_network_card
