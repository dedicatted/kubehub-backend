from os import system


def set_network_card(name, protocol):
    vbox_set_network_card_cmd = f'VBoxManage ' \
                                f'modifyvm {name} ' \
                                f'--nic1 {protocol} ' \
                                f'-bridgeadapter1 enp2s0'
    vbox_set_network_card = system(vbox_set_network_card_cmd)
    return vbox_set_network_card
